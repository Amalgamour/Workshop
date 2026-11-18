#!/usr/bin/env python3
"""0709 pass01: run the accepted prior rehearsal UNCHANGED, keeping its disposable copy (NONPRODUCTION).

Imports labs/return-lines-pass01/rehearse.py after a hash check and replaces only its
final `cleanup` with a no-op, in memory, so the copy, the backup and the journals
survive as evidence. The live book is read only. Then records post-adopt facts and
an inclusion/exclusion manifest.
usage: rehearse_0709.py --work-root ABS(new, outside checkout) --evidence ABS(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE = CHECKOUT / "00.kernel" / "00.00.10.work"
RL_DIR = CHECKOUT / "labs" / "return-lines-pass01"
PACK = LIVE / "0709.return-migration-check" / "evidence" / "pack05.01" / "source-manifest.json"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tree(root: Path) -> dict[str, dict]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            b = p.read_bytes()
            out[p.relative_to(root).as_posix()] = {"sha256": sha(b), "bytes": len(b)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-root", required=True)
    ap.add_argument("--evidence", required=True)
    args = ap.parse_args()
    evidence = Path(args.evidence)
    evidence.mkdir(parents=True, exist_ok=False)
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    for rel in ("labs/return-lines-pass01/rehearse.py", "labs/return-lines-pass01/return_lines.py",
                "labs/return-placement-pass01/return_placement.py", "labs/return-capture-pass01/return_capture.py",
                "labs/return-capture-pass01/return_inspect.py"):
        data = (CHECKOUT / rel).read_bytes()
        if sha(data) != pins[rel]["sha256"]:
            raise SystemExit(f"refused: {rel} differs from its pack05.01 pin")
    sys.path.insert(0, str(RL_DIR))
    import rehearse  # noqa: E402  (unchanged accepted rehearsal)

    kept = []
    rehearse.cleanup = lambda root: kept.append(root)  # in-memory only: keep the disposable copy and journals
    code = rehearse.main(["--work-root", args.work_root, "--evidence", str(evidence / "rehearse")])
    work = Path(args.work_root)
    book, backup = work / "book", work / "backup"
    facts = {"schema": "0709-rehearsal-run/1", "rehearse_exit": code, "cleanup_suppressed_for": [str(p) for p in kept],
             "work_root": str(work), "marker_in_copy": (book / "0100.band.returns").exists(),
             "marker_note": "the copy has no 0100.band.returns door: the tool refuses a book that contains it; live differs here"}
    audit_members = {r["old_member"] for r in json.loads(
        (LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json").read_text(encoding="utf-8"))["records"]}
    if book.is_dir():
        names = sorted(e.name for e in os.scandir(book) if e.is_dir())
        facts["book_dirs_after"] = names
        facts["old_members_still_in_place"] = [n for n in names if n in audit_members]
        facts["line_pages_after"] = [n for n in names if n[:2] == "01" and n not in audit_members]
        (evidence / "book-tree.json").write_text(json.dumps(tree(book), indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if backup.is_dir():
        facts["backup_dirs"] = sorted(p.name for p in backup.iterdir())
        facts["backup_retired"] = sorted(p.name for p in (backup / "retired").iterdir()) if (backup / "retired").is_dir() else []
        facts["backup_sources_count"] = len(list((backup / "sources").iterdir())) if (backup / "sources").is_dir() else 0
        journals = sorted(str(p.relative_to(backup)) for p in backup.rglob("*journal*"))
        facts["journals"] = journals
        (evidence / "backup-tree.json").write_text(json.dumps(tree(backup), indent=1, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json").read_text(encoding="utf-8"))
    included = sorted(r["old_member"] for r in audit["records"])
    tails = sorted(r["target_return"] for r in audit["records"] if r.get("route") == "page-local-colab")
    (evidence / "inclusion-manifest.json").write_text(json.dumps({
        "included_member_dirs": included, "included_tails": tails, "source": "audit-corrected.json via rehearse.py",
        "excluded": ["0100.band.returns door and its marker", "every page other than the five Colab tail files",
                     "every evidence tree, pack snapshot and nested copy", "return-line-layout.json (created only in the copy by init)"]},
        indent=2) + "\n", encoding="utf-8")
    (evidence / "rehearsal-facts.json").write_text(json.dumps(facts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in facts.items() if k not in ("book_dirs_after",)}, indent=1)[:3000])
    return code


if __name__ == "__main__":
    sys.exit(main())
