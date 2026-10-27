"""Test helper: deliver one request file in a separate process and print the elapsed time and receipt as JSON.
Runs inside the test's outer watchdog (subprocess timeout), so a regression in the deadline cannot hang the suite.

  python -B tests/_deliver_driver.py <store> <request.json>
"""
import json, sys, time
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from bridge.adapter import LocalProcessAdapter  # noqa: E402
from bridge.canon import strict_loads  # noqa: E402

profiles = {k: v for k, v in strict_loads((LAB / "profiles.json").read_bytes()).items() if not k.startswith("_")}
env = strict_loads(Path(sys.argv[2]).read_bytes())
ad = LocalProcessAdapter(sys.argv[1], profiles, LAB)
t = time.monotonic()
rec = ad.deliver(env)
print(json.dumps({"elapsed_s": round(time.monotonic() - t, 3), "receipt": rec}))
