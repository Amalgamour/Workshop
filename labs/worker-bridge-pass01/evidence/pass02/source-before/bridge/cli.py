"""Command line for the lab adapter. Read-only except `deliver` and `recover`, which write only in --store.

  python -B -m bridge.cli deliver --store S --request R      # R is a request.json; prints the receipt
  python -B -m bridge.cli status  --store S --delivery D     # a fresh process reads the recorded state
  python -B -m bridge.cli recover --store S --delivery D     # rebuild a missing receipt, never relaunch
"""
import argparse, json, sys
from pathlib import Path
from .adapter import LocalProcessAdapter

LAB = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("deliver", "status", "recover"))
    ap.add_argument("--store", required=True)
    ap.add_argument("--request")
    ap.add_argument("--delivery")
    a = ap.parse_args()
    profiles = {k: v for k, v in json.loads((LAB / "profiles.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
    ad = LocalProcessAdapter(a.store, profiles, LAB)
    if a.cmd == "deliver":
        out = ad.deliver(json.loads(Path(a.request).read_bytes()))
    elif a.cmd == "status":
        out = ad.status(a.delivery)
    else:
        out = ad.recover(a.delivery)
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if out.get("transport") not in ("refused",) else 2)


if __name__ == "__main__":
    main()
