"""Command line for the lab adapter. Read-only except `deliver` and `recover`, which write only in --store.

  python -B -m bridge.cli deliver --store S --request R      # R is a request.json; prints the receipt
  python -B -m bridge.cli status  --store S --delivery D     # a fresh process reads the recorded state
  python -B -m bridge.cli recover --store S --delivery D     # rebuild a missing receipt, never relaunch

The request file is read with the strict loader (no NaN or Infinity, no duplicate keys). A delivery id is checked
by the same rules as the library (bridge/ids.py) before any file is touched. Exit 0, or 2 on a refusal.
"""
import argparse, json, sys
from pathlib import Path
from .adapter import LocalProcessAdapter
from .canon import StrictJSONError, strict_loads

LAB = Path(__file__).resolve().parents[1]


def refuse(reason):
    print(json.dumps({"transport": "refused", "reason": reason, "launched": False, "review": "not performed"}, indent=1, sort_keys=True))
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("deliver", "status", "recover"))
    ap.add_argument("--store", required=True)
    ap.add_argument("--request")
    ap.add_argument("--delivery")
    a = ap.parse_args()
    profiles = {k: v for k, v in strict_loads((LAB / "profiles.json").read_bytes()).items() if not k.startswith("_")}
    ad = LocalProcessAdapter(a.store, profiles, LAB)
    if a.cmd == "deliver":
        if not a.request:
            refuse("deliver needs --request")
        try:
            env = strict_loads(Path(a.request).read_bytes())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, StrictJSONError) as e:
            refuse(f"request file: {type(e).__name__}: {e}")
        out = ad.deliver(env)
    else:
        if a.delivery is None:
            refuse(f"{a.cmd} needs --delivery")
        out = ad.status(a.delivery) if a.cmd == "status" else ad.recover(a.delivery)
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(2 if out.get("transport") == "refused" else 0)


if __name__ == "__main__":
    main()
