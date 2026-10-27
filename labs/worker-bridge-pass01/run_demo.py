"""Batch 0503.worker-bridge/05.01 #02 demonstration, with a PROTOCOL TEST WORKER (not a model).

  python -B run_demo.py evidence/demo-<name>

Steps, each in its own process where it matters:
  1. prepare: write the fixture input and request.json (the stand-in for a Clerk-released request)
  2. deliver: `python -m bridge.cli deliver` -> the adapter launches the allowlisted fixture-ok profile
  3. a fresh process: `python -m bridge.cli status` reads the durable receipt
  4. trace.md: every boundary with its bytes' hash
Refuses an existing output folder.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
from bridge.canon import canonical, sha256, sha256_file  # noqa: E402


def main(out):
    out = (LAB / out).resolve()
    if out.exists():
        sys.exit(f"stop: {out} exists")
    inp, res, store = out / "input", out / "output", out / "store"
    for d in (inp, res, store):
        d.mkdir(parents=True)
    text = "the bridge carries one request\n\nto one worker\n   \nand brings back evidence\n".encode("utf-8")
    (inp / "input.txt").write_bytes(text)
    env = {"schema": "worker-bridge/request@1", "delivery_id": "demo-0001", "job_id": "job-count-lines", "role": "builder",
           "work_ref": "00.kernel/00.00.10.work/0503.worker-bridge/05.01.md#02",
           "inputs": [{"name": "text", "path": "input.txt", "sha256": sha256(text), "bytes": len(text)}],
           "input_root": str(inp), "output_root": str(res),
           "limits": {"timeout_s": 20, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000},
           "release": {"by": "fixture producer (lab only; not a Clerk)", "ref": "run_demo.py"}, "backend": "fixture-ok"}
    req = out / "request.json"
    req.write_bytes(canonical(env))
    d = subprocess.run([sys.executable, "-B", "-m", "bridge.cli", "deliver", "--store", str(store), "--request", str(req)],
                       cwd=LAB, capture_output=True, text=True)
    (out / "deliver.stdout.json").write_text(d.stdout, encoding="utf-8", newline="\n")
    s = subprocess.run([sys.executable, "-B", "-m", "bridge.cli", "status", "--store", str(store), "--delivery", "demo-0001"],
                       cwd=LAB, capture_output=True, text=True)
    (out / "status-fresh-process.json").write_text(s.stdout, encoding="utf-8", newline="\n")
    rec = json.loads(s.stdout)
    dd = store / "demo-0001"
    rows = [("request (prepared)", req), ("request (as stored by the adapter)", dd / "request.json"),
            ("launch record (exclusive create, before the process)", dd / "launch.json"),
            ("input read by the worker", inp / "input.txt"), ("artifact written by the worker", res / "result.json"),
            ("worker stdout = result", dd / "attempt" / "stdout.bin"), ("worker stderr", dd / "attempt" / "stderr.bin"),
            ("exit record", dd / "attempt" / "exit.json"), ("receipt", dd / "receipt.json")]
    lines = ["# Demonstration trace (protocol test worker, not a model)", "",
             f"delivery `demo-0001`, job `job-count-lines`, request_sha256 `{rec['request_sha256']}`", "",
             "| Boundary | File | Bytes | sha256 |", "|---|---|---|---|"]
    for name, p in rows:
        lines.append(f"| {name} | `{p.relative_to(out).as_posix()}` | {p.stat().st_size} | `{sha256_file(p)}` |")
    lines += ["", f"deliver exit {d.returncode}; fresh-process status exit {s.returncode}",
              f"transport `{rec['transport']}`, claimed outcome `{rec['claimed_outcome']}`, collection `{rec['collection']}`, "
              f"worker kind `{rec['worker_kind']}`, review `{rec['review']}`",
              f"artifact content: `{(res / 'result.json').read_text(encoding='utf-8')}`", ""]
    (out / "trace.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines))
    sys.exit(0 if rec.get("collection") == "collected" else 1)


if __name__ == "__main__":
    main(sys.argv[1])
