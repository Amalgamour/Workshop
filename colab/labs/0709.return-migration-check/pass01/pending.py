#!/usr/bin/env python3
"""0709 pass01: READ-ONLY scan for submissions marked pending matching-line custody.

Reads only page-level *.md files directly inside 05NN and 07NN page directories of the
live work book (no evidence trees). Reports exact matching lines and file hashes.
Identities that the text does not state stay unknown.
usage: pending.py --out FILE   (FILE must not exist)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")
PAGE = re.compile(r"^0[57](0[1-9]|[1-9][0-9])\.[a-z0-9-]+$")
LINE = re.compile(r"(?i)(custody|matching|0[1-9]?1\d\d\.|return line).*(pending|not filed|unfiled)|(pending).*(custody|matching line|0\d{3}\.)")
MEMBER_REF = re.compile(r"\b01\d\d\.[a-z0-9-]+\b")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    if out.exists():
        raise SystemExit("refused: output exists")
    hits = []
    for page in sorted(p for p in LIVE.iterdir() if p.is_dir() and PAGE.match(p.name)):
        for f in sorted(page.glob("*.md")):
            raw = f.read_bytes()
            text = raw.decode("utf-8", "replace")
            for n, line in enumerate(text.splitlines(), 1):
                if LINE.search(line):
                    hits.append({"page": page.name, "file": f.name, "line": n, "text": line.strip()[:400],
                                 "file_sha256": hashlib.sha256(raw).hexdigest(),
                                 "named_return_lines": sorted(set(MEMBER_REF.findall(line)))})
    by_source = {}
    for h in hits:
        by_source.setdefault(f"{h['page']}/{h['file']}", []).append(h)
    body = {"schema": "0709-pending-custody-scan/1", "scope": "page-level *.md in 05NN and 07NN pages only; evidence trees not read",
            "pattern": LINE.pattern, "hit_count": len(hits), "sources": len(by_source), "hits": hits}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    for src, rows in by_source.items():
        print(src, len(rows), rows[0]["text"][:140])
    return 0


if __name__ == "__main__":
    sys.exit(main())
