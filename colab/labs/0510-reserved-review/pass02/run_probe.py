#!/usr/bin/env python3
"""0510/05.06 pass02 probe runner. Every execution gets a NEW run directory (0708 F01).

usage: run_probe.py
Creates evidence/design05.06/runs/<UTC>-<6 hex>/ by exclusive mkdir; never deletes.
Steps (each a subprocess with -B; raw stdout/stderr/exit kept):
  P1  reproduce C03 on the SEALED pass01 rules (imported read-only)
  P2  pass02 focused tests
  P3  write the pass02 SYNTHETIC examples into the run directory
"""

from __future__ import annotations

import datetime
import json
import os
import secrets
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKOUT = Path(r"D:\Git\lib-build")
RUNS = CHECKOUT / "00.kernel" / "00.00.10.work" / "0510.colab-tools" / "evidence" / "design05.06" / "runs"
PASS01 = CHECKOUT / "colab" / "labs" / "0510-reserved-review" / "pass01"

P1_CODE = r"""
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import reserved_rules as Q
raw = open(sys.argv[1] + '/examples/05.01.return.SYNTHETIC.md', 'rb').read().replace(b'\r\n', b'\n')
rows = []
for name, data in (('LF', raw), ('CRLF', raw.replace(b'\n', b'\r\n'))):
    try:
        Q.first_findings(data); rows.append({'case': name, 'observed': 'accepted'})
    except Exception as exc:
        rows.append({'case': name, 'observed': type(exc).__name__ + ': ' + str(exc)})
print(json.dumps(rows, indent=2))
"""


def main() -> int:
    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = RUNS / f"{stamp}-{secrets.token_hex(3)}"
    run.mkdir()  # exclusive: an existing name raises
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    steps = [
        ("P1-pass01-crlf", [sys.executable, "-B", "-c", P1_CODE, str(PASS01)]),
        ("P2-tests", [sys.executable, "-B", str(HERE / "test_rules2.py")]),
        ("P3-examples", [sys.executable, "-B", str(HERE / "examples.py"), "--write", str(run / "examples")]),
    ]
    log = []
    for name, argv in steps:
        p = subprocess.run(argv, cwd=str(HERE), capture_output=True, env=env)
        (run / f"{name}.stdout").write_bytes(p.stdout)
        (run / f"{name}.stderr").write_bytes(p.stderr)
        log.append({"step": name, "argv": argv, "exit": p.returncode})
    (run / "run.json").write_text(json.dumps({"interpreter": sys.executable, "version": sys.version, "run": run.name, "steps": log}, indent=2) + "\n", encoding="utf-8")
    print(run.name)
    for row in log:
        print(row["step"], row["exit"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
