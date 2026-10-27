"""Reproduce Prime review probes BR-01, BR-02 and BR-03 against one lab source tree, inside lab scratch only.

  python -B tests/probes_pass02.py <lab source dir> <scratch dir>     -> prints one JSON object

BR-01: a child that never reads stdin, a valid ~1 MB envelope, timeout 0.2 s (Prime's settings).
BR-02: status('../outside') and recover('../outside') against a sentinel receipt outside the store.
BR-03: validate() with an infinite timeout, a fractional byte cap and bool limits.
The child is a self-terminating script written into the scratch copy (sleep 3, never reads stdin).
"""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

src, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
if scratch.exists():
    sys.exit(f"stop: {scratch} exists")
copy = scratch / "lab"
shutil.copytree(src, copy, ignore=shutil.ignore_patterns("scratch", "evidence", "__pycache__"))
(copy / "fixtures" / "noread_probe.py").write_text("import time\ntime.sleep(3)\n", encoding="utf-8")
sys.path.insert(0, str(copy))
from bridge.adapter import LocalProcessAdapter  # noqa: E402
from bridge.canon import canonical  # noqa: E402
from bridge.envelope import validate  # noqa: E402

inp, out, store, outside = (scratch / n for n in ("in", "out", "store", "outside"))
for d in (inp, out, store, outside):
    d.mkdir(parents=True)
(inp / "i.txt").write_bytes(b"x\n")
(outside / "receipt.json").write_bytes(b'{"sentinel":"outside the configured store"}')
import hashlib  # noqa: E402
base = {"schema": "worker-bridge/request@1", "delivery_id": "probe-timeout", "job_id": "probe", "role": "builder", "work_ref": "probe",
        "inputs": [{"name": "i", "path": "i.txt", "sha256": hashlib.sha256(b"x\n").hexdigest(), "bytes": 2}],
        "input_root": str(inp), "output_root": str(out), "limits": {"timeout_s": 0.2, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000},
        "release": {"by": "probe", "ref": "probe"}, "backend": "fixture-noread"}
result = {"source": str(src)}

ad = LocalProcessAdapter(store, {"fixture-noread": {"kind": "protocol test worker", "argv": ["{python}", "-B", "-I", "fixtures/noread_probe.py"]}}, copy)
for name, call in (("status", ad.status), ("recover", ad.recover)):
    try:
        r = call("../outside")
        result[f"BR-02 {name}('../outside')"] = "READ OUTSIDE THE STORE" if "sentinel" in json.dumps(r) else f"no outside read: {r.get('transport') or r.get('state')}"
    except Exception as e:
        result[f"BR-02 {name}('../outside')"] = f"raised {type(e).__name__} (no outside read)"
result["BR-02 sentinel unchanged"] = (outside / "receipt.json").read_bytes() == b'{"sentinel":"outside the configured store"}'

for name, lim in (("infinite timeout", {"timeout_s": float("inf"), "max_stdout_bytes": 1000, "max_stderr_bytes": 1000}),
                  ("fractional byte cap", {"timeout_s": 1, "max_stdout_bytes": 1.5, "max_stderr_bytes": 1000}),
                  ("bool limits", {"timeout_s": True, "max_stdout_bytes": True, "max_stderr_bytes": True})):
    try:
        validate(dict(base, limits=lim))
        result[f"BR-03 {name}"] = "ACCEPTED"
    except Exception as e:
        result[f"BR-03 {name}"] = f"refused: {e}"

big = dict(base, work_ref="x" * 1_000_000)
t = time.monotonic()
r = ad.deliver(big)
result["BR-01 elapsed_s"] = round(time.monotonic() - t, 3)
result["BR-01 transport"] = r.get("transport")
result["BR-01 configured_timeout_s"] = 0.2
print(json.dumps(result, indent=1))
