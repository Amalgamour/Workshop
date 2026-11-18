#!/usr/bin/env python3
"""STUB - NOT THE LOOP. Harness self-test only. Its outputs are never loop evidence.

usage: STUB_loop.py ok | fail | sleep PIDFILE | crash
"""

import json
import subprocess
import sys
import time

STUB = {"stub": True, "note": "STUB output, not a review loop", "accepted": False, "authority": "none",
        "custody": "not-established", "allocated": False, "closes_work": False, "releases_action": False}

mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "ok":
    print(json.dumps(STUB))
    sys.exit(0)
if mode == "fail":
    print(json.dumps(dict(STUB, result="stub-fail")))
    sys.exit(3)
if mode == "sleep":
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(str(child.pid))
    time.sleep(120)
    sys.exit(0)
if mode == "crash":
    raise RuntimeError("STUB crash for harness self-test")
print("STUB: unknown mode", file=sys.stderr)
sys.exit(2)
