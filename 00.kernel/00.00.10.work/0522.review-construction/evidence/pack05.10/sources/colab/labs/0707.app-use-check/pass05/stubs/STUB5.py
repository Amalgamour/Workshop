#!/usr/bin/env python3
"""STUB - NOT THE LOOP. pass05 harness self-test only; outputs are never loop evidence.

usage: STUB5.py MODE [PIDFILE]
  ok                    JSON, exit 0
  fail                  JSON, exit 3
  crash                 traceback, exit 1
  flush-sleep           writes STDOUT-MARK/STDERR-MARK, flushes, sleeps (timeout)
  flush-sleep-child     as flush-sleep plus a grandchild that inherits the pipes
  exit-leave-child      JSON, starts a grandchild with its own null streams, exits 0
  exit-hold-child       JSON, starts a grandchild that inherits the pipes, exits 0
  crash-leave-child     starts a grandchild with null streams, then crashes
"""

import json
import subprocess
import sys
import time

STUB = {"stub": True, "note": "STUB output, not a review loop", "accepted": False, "authority": "none",
        "custody": "not-established", "allocated": False, "closes_work": False, "releases_action": False}
SLEEPER = [sys.executable, "-c", "import time; time.sleep(120)"]


def child(inherit: bool):
    kw = {} if inherit else {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    p = subprocess.Popen(SLEEPER, **kw)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(str(p.pid))


mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "ok":
    print(json.dumps(STUB))
elif mode == "fail":
    print(json.dumps(dict(STUB, result="stub-fail")))
    sys.exit(3)
elif mode == "crash":
    raise RuntimeError("STUB crash for harness self-test")
elif mode in ("flush-sleep", "flush-sleep-child"):
    sys.stdout.write("STDOUT-MARK before timeout\n")
    sys.stdout.flush()
    sys.stderr.write("STDERR-MARK before timeout\n")
    sys.stderr.flush()
    if mode == "flush-sleep-child":
        child(inherit=True)
    time.sleep(120)
elif mode == "exit-leave-child":
    child(inherit=False)
    print(json.dumps(STUB))
elif mode == "exit-hold-child":
    child(inherit=True)
    print(json.dumps(STUB))
    sys.stdout.flush()
elif mode == "crash-leave-child":
    child(inherit=False)
    raise RuntimeError("STUB crash after leaving a child")
else:
    print("STUB5: unknown mode", file=sys.stderr)
    sys.exit(2)
