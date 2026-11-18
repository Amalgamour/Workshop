#!/usr/bin/env python3
"""0709 pass02 H4: does a deliberate allocation-lock sentinel stop the UNCHANGED helper reserve
while legacy capture/verify/inspect keep working? (NONPRODUCTION, disposable book only.)
usage: probe_lock.py --root ABS(new, outside checkout) --evidence ABS(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
PACK = CHECKOUT / "00.kernel/00.00.10.work/0709.return-migration-check/evidence/pack05.02/source-manifest.json"
RL = "labs/return-lines-pass01/return_lines.py"
RC = "labs/return-capture-pass01/return_capture.py"
RI = "labs/return-capture-pass01/return_inspect.py"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
SENTINEL = (b"return-line-allocation-stop/1 (SYNTHETIC probe)\n"
            b"This book is declared line-pass. Sequential return_capture.py reserve is refused here.\n"
            b"Not a crash leftover: do not delete. Use the line tool. See 0100.band.returns/01.md.\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--evidence", required=True)
    a = ap.parse_args()
    root, ev = Path(a.root), Path(a.evidence)
    if str(root).lower().startswith(str(CHECKOUT).lower()):
        raise SystemExit("refused: fixture root inside the checkout")
    root.mkdir(parents=True, exist_ok=False)
    ev.mkdir(parents=True, exist_ok=False)
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    for rel in (RL, RC, RI):
        b = (CHECKOUT / rel).read_bytes()
        if (sha(b), len(b)) != (pins[rel]["sha256"], pins[rel]["bytes"]):
            raise SystemExit(f"refused: {rel} differs from its pack05.02 pin")
    steps = []

    def run(label, tool, args):
        argv = [sys.executable, "-B", str(CHECKOUT / tool), *args]
        t = time.monotonic()
        p = subprocess.run(argv, cwd=str(CHECKOUT), capture_output=True, timeout=120, env=ENV)
        (ev / f"{label}.stdout").write_bytes(p.stdout)
        (ev / f"{label}.stderr").write_bytes(p.stderr)
        steps.append({"label": label, "argv": argv, "exit": p.returncode, "seconds": round(time.monotonic() - t, 2),
                      "out": (p.stdout + p.stderr).decode("utf-8", "replace")[-600:]})
        return p

    src = root / "src"
    src.mkdir()
    (src / "return.md").write_bytes(b"SYNTHETIC RETURN\n")
    book = root / "book"
    book.mkdir()
    common = ["--origin-book", "00.00.10.work", "--submitter", "probe", "--reviewer", "probe", "--release", "SYNTHETIC probe"]
    # an in-flight legacy reservation made before the stop
    run("h4-01-helper-reserve-inflight", RC, ["reserve", "--book", str(book), "--submission", "probe-inflight", "--name", "inflight-0507",
                                               "--origin-page", "0507.beta", "--origin-batch", "05.01", *common])
    lock = book / "0100.band.returns" / ".allocation.lock"
    lock.write_bytes(SENTINEL)
    run("h4-02-helper-reserve-new", RC, ["reserve", "--book", str(book), "--submission", "probe-new", "--name", "new-0508",
                                          "--origin-page", "0508.gamma", "--origin-batch", "05.01", *common])
    run("h4-03-helper-reserve-inflight-again", RC, ["reserve", "--book", str(book), "--submission", "probe-inflight", "--name", "inflight-0507",
                                                     "--origin-page", "0507.beta", "--origin-batch", "05.01", *common])
    run("h4-04-helper-capture-inflight", RC, ["capture", "--book", str(book), "--submission", "probe-inflight",
                                              "--return-file", str(src / "return.md"), "--source-root", str(src)])
    run("h4-05-helper-verify-inflight", RC, ["verify", "--book", str(book), "--member", "0101.inflight-0507"])
    run("h4-06-inspect-inflight", RI, ["inspect", "--book", str(book), "--member", "0101.inflight-0507", "--json"])
    run("h4-07-line-init-door-present", RL, ["init", "--book", str(book), "--name", "00.00.10.work"])
    body = {"schema": "0709-lock-probe/1", "root": str(root), "sentinel_sha256": sha(SENTINEL), "steps": steps,
            "lock_still_present": lock.exists(), "lock_bytes_unchanged": lock.exists() and lock.read_bytes() == SENTINEL,
            "book_dirs": sorted(e.name for e in book.iterdir())}
    (ev / "probe.json").write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    for s in steps:
        print(s["label"], "exit", s["exit"], f"{s['seconds']}s", "|", s["out"].strip().replace("\n", " / ")[:220])
    print({k: body[k] for k in ("lock_still_present", "lock_bytes_unchanged", "book_dirs")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
