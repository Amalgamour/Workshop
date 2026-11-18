#!/usr/bin/env python3
"""0709 pass01: READ-ONLY end verification (NONPRODUCTION).

Re-checks every pack05.01 frozen input, confirms no live layout or authorization was
created, recomputes the live fingerprint with the pinned rehearse.fingerprint, and
lists the live 01NN member directories.
usage: verify.py --out FILE   (FILE must not exist)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE = CHECKOUT / "00.kernel" / "00.00.10.work"
PAGE = LIVE / "0709.return-migration-check"
PACK = PAGE / "evidence" / "pack05.01" / "source-manifest.json"
REHEARSE_PIN = "labs/return-lines-pass01/rehearse.py"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    if out.exists():
        raise SystemExit("refused: output exists")
    files = json.loads(PACK.read_text(encoding="utf-8"))["files"]
    rows, bad = [], []
    for r in files:
        p = CHECKOUT / Path(*r["path"].split("/"))
        b = p.read_bytes() if p.is_file() else None
        ok = b is not None and sha(b) == r["sha256"] and len(b) == r.get("bytes", len(b))
        rows.append({"path": r["path"], "ok": ok})
        if not ok:
            bad.append(r["path"])
    pins = {r["path"]: r["sha256"] for r in files}
    if sha((CHECKOUT / REHEARSE_PIN).read_bytes()) != pins[REHEARSE_PIN]:
        raise SystemExit("refused: rehearse.py differs from its pin")
    sys.path.insert(0, str(CHECKOUT / "labs" / "return-lines-pass01"))
    import rehearse  # noqa: E402  (pinned; only fingerprint/member_names are called, both read-only)
    audit = json.loads((LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json").read_text(encoding="utf-8"))
    recs = sorted(audit["records"], key=lambda r: rehearse.rl.member_key(r["old_member"]))
    names = [r["old_member"] for r in recs]
    tails = [r["target_return"] for r in recs if r.get("route") == "page-local-colab"]
    fp = rehearse.fingerprint(str(LIVE), names, tails)
    door = LIVE / "0100.band.returns" / "01.md"
    body = {
        "schema": "0709-end-verification/1",
        "pack_inputs": len(rows), "pack_ok": len(rows) - len(bad), "pack_bad": bad,
        "live_layout_present": (LIVE / "return-line-layout.json").exists(),
        "live_authorization_files": sorted(p.name for p in LIVE.glob("*authorization*")),
        "live_fingerprint": fp,
        "expected_fingerprint": "60f798f3 (rehearsal before/after; full value in rehearse report)",
        "live_member_dirs": len(rehearse.member_names(str(LIVE))),
        "audit_members": len(names), "tails": len(tails),
        "door_01_sha256": sha(door.read_bytes()), "door_01_bytes": len(door.read_bytes()),
        "line_0184_exists": any(p.name.startswith("0184.") for p in LIVE.iterdir()),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in body.items()}, indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
