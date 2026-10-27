"""Test helper for 05.03 (BR-01b): deliver one request in a separate process, report how long deliver() took,
which I/O threads were still alive when it returned, and when (if ever, within 15 s) they finished.
The descendant that holds the pipes is a self-terminating fixture (5 s), so nothing persists.

  python -B tests/_driver_pass03.py <store> <request.json>
"""
import json, sys, threading, time
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from bridge.adapter import LocalProcessAdapter  # noqa: E402
from bridge.canon import strict_loads  # noqa: E402

profiles = {k: v for k, v in strict_loads((LAB / "profiles.json").read_bytes()).items() if not k.startswith("_")}
env = strict_loads(Path(sys.argv[2]).read_bytes())
ad = LocalProcessAdapter(sys.argv[1], profiles, LAB)
before = set(threading.enumerate())
t = time.monotonic()
rec = ad.deliver(env)
elapsed = time.monotonic() - t
left = [th for th in threading.enumerate() if th not in before and th.is_alive()]
names = sorted(th.name for th in left)
t2 = time.monotonic()
while any(th.is_alive() for th in left) and time.monotonic() - t2 < 15:
    time.sleep(0.05)
print(json.dumps({"elapsed_s": round(elapsed, 3), "alive_at_return": names,
                  "background_finished_after_s": None if any(th.is_alive() for th in left) else round(time.monotonic() - t, 3),
                  "receipt": rec}))
