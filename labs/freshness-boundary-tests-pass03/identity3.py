#!/usr/bin/env python3
"""Execution proof v2 + identity extensions (0707/05.25; contract 0420/06.59). NONPRODUCTION.

Reuses the frozen pass02 identity reader (hash-pinned against pack05.25) for schema/path/legacy resolution and adds:
  * optional candidate fields loop_door / report_door (declared files; legacy baselines: derived and labelled);
  * execution_proof(): three runs of a fixed probe at ONE absolute path (control, control, tampered copy), each traced by
    the LAB AUDIT TRACER (tracer/sitecustomize.py on PYTHONPATH; doors copy os.environ, so it follows subprocesses).
Evidence classes (only 'executed' passes a gate):
  executed             the audit log of BOTH controls shows the declared target run (cpython.run_file) or exec'd
                       (exec of code compiled from it) under the disposable root, during the probe command; the tamper
                       run differs (corroboration). Bound to the executing pid/argv and the probe argv.
  verified-pin-check   the target was opened/read in the controls but never run/exec'd (e.g. a digest check)
  decoy                no audit access to the target and the tamper run is identical
  nondeterministic     the two untampered controls disagree
  unattributed-change  the tamper run differs, but the audit never shows the target run/exec'd or read
  contradictory        the audit shows execution but the tamper run is identical (fail closed)
An output delta or a target-named refusal alone can never set executed true. Absent/unreadable audit evidence fails.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE = Path(r"D:\Git\lib-build")
PACK25 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.25/source-manifest.json"
TRACER = HERE / "tracer"
I2_REL = "labs/freshness-boundary-tests-pass02/identity.py"


def _load_i2():
    row = {r["path"]: r for r in json.loads(PACK25.read_bytes())["files"]}[I2_REL]
    if hashlib.sha256((LIVE / I2_REL).read_bytes()).hexdigest() != row["sha256"]:
        raise SystemExit("refused: pass02 identity.py differs from its pack05.25 freeze")
    spec = importlib.util.spec_from_file_location("fbt_pass02_identity", LIVE / I2_REL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fbt_pass02_identity"] = mod
    spec.loader.exec_module(mod)
    return mod


I2 = _load_i2()
Refused = I2.Refused
path_problem = I2.path_problem
LEGACY_DOORS = {"proto-l": "app/review_loop_tools_v8.py", "staged-g": "app/review_loop_tools_v9.py"}


def resolve(inputs, root: Path, shape_v2) -> dict:
    ident = I2.resolve(inputs, root, shape_v2)
    cand = inputs.get("candidate") if isinstance(inputs, dict) else None
    declared = {f["path"] for f in ident["files"]}
    for key in ("loop_door", "report_door"):
        v = cand.get(key) if isinstance(cand, dict) and ident["mode"] == "explicit" else None
        if ident["mode"] == "legacy-discovery" and key == "loop_door":
            v = LEGACY_DOORS[ident["kind"]]                      # labelled legacy: the selected v8/v9 door
        if v is not None:
            pp = path_problem(v)
            if pp or v not in declared:
                raise Refused(f"candidate.{key} {v!r} {pp or 'is not a declared file'}")
        ident[key] = v
    return ident


# ------------------------------------------------------------------ traced execution
def traced_env(root: Path, log: Path) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LAB_AUDIT_LOG=str(log), LAB_AUDIT_ROOT=str(root))
    env["PYTHONPATH"] = str(TRACER) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def run(argv, root: Path, env: dict) -> dict:
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, env=env, cwd=str(root), timeout=600)
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout": p.stdout.decode("utf-8", "replace"),
            "stderr": p.stderr.decode("utf-8", "replace")}


def read_log(log: Path) -> list | None:
    if not log.is_file():
        return None
    out = []
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except Exception:
            return None
    return out


def _norm(text: str, root: Path) -> str:
    out = text
    for r in {str(root), str(root.resolve())}:
        for s in {r, r.replace("\\", "/"), r.replace("\\", "\\\\"), r.replace("/", "\\"), r.replace("/", "\\").replace("\\", "\\\\")}:
            out = out.replace(s, "<ROOT>")
    return out


def _target_events(events, target_abs: str) -> dict:
    hit = [e for e in events if e.get("path") == target_abs]
    return {"exec": [e for e in hit if e["event"] in ("run_file", "exec")], "open": [e for e in hit if e["event"] == "open"],
            "compile": [e for e in hit if e["event"] == "compile"]}


def execution_proof(cand_root: Path, ident: dict, target: str, probe, rooms: Path, tag: str) -> dict:
    """probe(root, env) -> run() result. Three runs at ONE stable path; each finished room is renamed aside."""
    if target not in {f["path"] for f in ident["files"]}:
        raise Refused(f"proof target {target} is not a declared file")
    nonce = uuid.uuid4().hex[:12]
    rooms.mkdir(parents=True, exist_ok=True)
    stable = rooms / f"{tag}-run"
    target_abs = os.path.normcase(os.path.abspath(stable / target))
    runs = {}
    for label in ("control-1", "control-2", "tamper"):
        shutil.copytree(cand_root, stable)
        if label == "tamper":
            f = stable / target
            f.write_bytes(f"raise SystemExit('LAB-TAMPER-{nonce}')\n".encode() + f.read_bytes())
        log = rooms / f"{tag}-{label}.audit.jsonl"
        res = probe(stable, traced_env(stable, log))
        events = read_log(log)
        runs[label] = {"res": res, "norm": _norm(res["stdout"], stable), "events": events}
        stable.rename(rooms / f"{tag}-{label}")
    c1, c2, t = runs["control-1"], runs["control-2"], runs["tamper"]
    out = {"target": target, "nonce": nonce, "probe_argv": c1["res"]["argv"], "stable_path": str(stable),
           "rooms": [str(rooms / f"{tag}-{x}") for x in runs], "audit_logs": [str(rooms / f"{tag}-{x}.audit.jsonl") for x in runs]}
    if c1["events"] is None or c2["events"] is None:
        out.update({"class": "no-audit-evidence", "executed": False, "why": "audit log absent or unreadable: fail closed"})
        return out
    deterministic = (c1["res"]["exit"], c1["norm"]) == (c2["res"]["exit"], c2["norm"])
    e1, e2 = _target_events(c1["events"], target_abs), _target_events(c2["events"], target_abs)
    changed = (c1["res"]["exit"], c1["norm"]) != (t["res"]["exit"], t["norm"])
    terr = t["res"]["stderr"]
    corroboration = ("nonce surfaced" if nonce in terr else "compile of the tampered target failed" if ("SyntaxError" in terr and "__future__" in terr)
                     else "refusal names the target" if target in terr.replace("\\", "/") else "output changed" if changed else "no change")
    if not deterministic:
        cls = "nondeterministic"
    elif e1["exec"] and e2["exec"]:
        cls = "executed" if changed else "contradictory"
    elif e1["open"] or e1["compile"]:
        cls = "verified-pin-check" if changed else "read-only (unchanged on tamper)"
    elif changed:
        cls = "unattributed-change"
    else:
        cls = "decoy"
    binding = [{"pid": e["pid"], "event": e["event"], "process_argv": e["argv"][:6]} for e in e1["exec"][:4]]
    out.update({"class": cls, "executed": cls == "executed", "deterministic_controls": deterministic,
                "control": {"exit": c1["res"]["exit"], "normalized_stdout_sha256": hashlib.sha256(c1["norm"].encode()).hexdigest(),
                            "stderr_tail": c1["res"]["stderr"][-300:], "target_events": {k: len(v) for k, v in e1.items()}},
                "control_2_target_events": {k: len(v) for k, v in e2.items()},
                "tamper": {"exit": t["res"]["exit"], "changed": changed, "corroboration": corroboration, "stderr_tail": terr[-300:]},
                "binding": binding})
    return out
