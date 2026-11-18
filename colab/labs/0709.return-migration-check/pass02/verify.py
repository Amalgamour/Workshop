#!/usr/bin/env python3
"""0709 pass02: READ-ONLY end verification (NONPRODUCTION).
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
PACK = LIVE / "0709.return-migration-check" / "evidence" / "pack05.02" / "source-manifest.json"
FP_0501 = "60f798f3394b00ba66a4e1db6c3fd606f6bfcccc4f0f2fd6d13d9d3e9f4f4334"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    if out.exists():
        raise SystemExit("refused: output exists")
    files = json.loads(PACK.read_text(encoding="utf-8"))["files"]
    bad = []
    for r in files:
        p = CHECKOUT / Path(*r["path"].split("/"))
        b = p.read_bytes() if p.is_file() else b""
        if (sha(b), len(b)) != (r["sha256"], r["bytes"]):
            bad.append(r["path"])
    pins = {r["path"]: r for r in files}
    reh = "labs/return-lines-pass01/rehearse.py"
    if sha((CHECKOUT / reh).read_bytes()) != pins[reh]["sha256"]:
        raise SystemExit("refused: rehearse.py differs from its pin")
    sys.path.insert(0, str(CHECKOUT / "labs" / "return-lines-pass01"))
    import rehearse  # noqa: E402  (pinned; fingerprint and member_names are read-only)
    audit = json.loads((LIVE / "0417.return-placement/evidence/audit-corrected.json").read_text(encoding="utf-8"))
    recs = sorted(audit["records"], key=lambda r: rehearse.rl.member_key(r["old_member"]))
    fp = rehearse.fingerprint(str(LIVE), [r["old_member"] for r in recs],
                              [r["target_return"] for r in recs if r.get("route") == "page-local-colab"])
    door = LIVE / "0100.band.returns"
    body = {"schema": "0709-end-verification/2", "pack05_02_inputs": len(files), "pack05_02_bad": bad,
            "live_fingerprint": fp, "fingerprint_equals_0501": fp == FP_0501,
            "live_layout_present": (LIVE / "return-line-layout.json").exists(),
            "live_line_index_present": (LIVE / "return-line-index.json").exists(),
            "live_sentinel_present": (door / ".allocation.lock").exists(),
            "door_entries": sorted(p.name for p in door.iterdir()),
            "door_01_sha256": sha((door / "01.md").read_bytes()),
            "live_member_dirs": len(rehearse.member_names(str(LIVE))),
            "line_0184_exists": any(p.name.startswith("0184.") for p in LIVE.iterdir())}
    out.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(body, indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
