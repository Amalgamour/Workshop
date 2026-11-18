#!/usr/bin/env python3
"""Reconstruct the 0707/05.18 candidate root from INDEX.json ONLY, then replay. Standalone (stdlib only;
imports nothing from the lab). NONPRODUCTION.

1. Refuse a room inside the live checkout. Copy every indexed file from its declared `from`
   (live:/snapshot:/lab: are paths under the live root, read-only), verifying sha256 and bytes; stop on any mismatch.
2. Run <room>/app/librarian.py review-loop prepare for each expected fixture as a NEW process.
3. Compare measurement, row_count, rows_sha, cuts_sha, finding codes and kind with the index.
usage: reconstruct.py --index INDEX.json --room NEW-DIR --out FILE
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--room", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    idx = json.loads(Path(a.index).read_text(encoding="utf-8"))
    live = Path(idx["live_root"])
    room = Path(a.room)
    if str(room.resolve()).lower().startswith(str(live.resolve()).lower()):
        sys.exit("refused: room inside the live checkout")
    room.mkdir(parents=True, exist_ok=False)
    for e in idx["files"]:
        kind, rel = e["from"].split(":", 1)
        data = (live / rel).read_bytes()
        if sha(data) != e["sha256"] or len(data) != e["bytes"]:
            sys.exit(f"refused: {e['path']} from {e['from']} does not match the index")
        dst = room / e["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    results = {}
    for key, want in idx["expected"].items():
        argv = [sys.executable, "-B", str(room / "app/librarian.py"), "review-loop", "prepare", "--book", str(room / idx["book"]),
                "--source", want["source"], "--pass", want["pass"]]
        p = subprocess.run(argv, capture_output=True, env=env, cwd=str(room), timeout=600)
        b = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else {}
        rows = ((b.get("form") or {}).get("bindings") or {}).get("rows") or []
        got = {"measurement": b.get("measurement"), "row_count": len(rows), "kind": b.get("kind"),
               "rows_sha": sha(json.dumps(sorted(json.dumps(r, sort_keys=True) for r in rows)).encode()),
               "cuts_sha": sha(json.dumps(b.get("cuts"), sort_keys=True).encode()),
               "finding_codes": sorted(f.get("code") for f in b.get("findings") or [])}
        diff = {k: (want[k], got[k]) for k in got if want.get(k) != got[k]}
        results[key] = {"exit": p.returncode, "equal": not diff and p.returncode == 0, "diff": diff, "intake_id": b.get("intake_id"),
                        "stderr": p.stderr.decode("utf-8", "replace")[-200:]}
        print(key, "equal" if results[key]["equal"] else f"DIFF {diff}")
    ok = all(r["equal"] for r in results.values())
    Path(a.out).write_text(json.dumps({"schema": "rie-reconstruct/1", "index_sha256": sha(Path(a.index).read_bytes()), "room": str(room),
                                       "files": len(idx["files"]), "ok": ok, "results": results}, indent=1) + "\n", encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
