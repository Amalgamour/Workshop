#!/usr/bin/env python3
"""Build a disposable copy root with the production layout for the 0707/05.15 N7 return (0707/05.16 lab).

Copies, each verified by sha256 before use:
- the 17 files pinned by app/review-loop-v7.json (labs and app), plus app/review-loop-v7.json itself;
- the frozen 0707/05.15 pack and 06.15.review.md from pack05.16 snapshots;
- every row of the 05.15 artifact manifest (repo-relative paths), from the live checkout.
The live checkout is only READ. Nothing is written outside --room.
usage: make_fixture.py --room NEW-DIR (outside the checkout) [--omit-review]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
PAGE = "00.kernel/00.00.10.work/0707.app-use-check"
PACK16 = LIVE / PAGE / "evidence/pack05.16"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--omit-review", action="store_true", help="leave out 06.15.review.md (variant for a publish demonstration)")
    a = ap.parse_args()
    room = Path(a.room)
    if str(room.resolve()).lower().startswith(str(LIVE).lower()):
        sys.exit("refused: room inside the checkout")
    repo = room / "repo"
    repo.mkdir(parents=True, exist_ok=False)
    pins = json.loads((PACK16 / "source-manifest.json").read_text(encoding="utf-8"))
    frozen = {f["path"]: f for f in pins["files"]}
    copied = []

    def put(rel: str, src: Path, want_sha: str, want_bytes: int | None):
        data = src.read_bytes()
        if sha(data) != want_sha or (want_bytes is not None and len(data) != want_bytes):
            raise SystemExit(f"refused: {rel} does not match its pin")
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        copied.append({"path": rel, "sha256": want_sha, "bytes": len(data), "from": str(src)})

    v7 = json.loads((LIVE / "app/review-loop-v7.json").read_bytes())
    put("app/review-loop-v7.json", LIVE / "app/review-loop-v7.json", frozen["app/review-loop-v7.json"]["sha256"], None)
    for item in v7["tools"].values():
        put(item["path"], LIVE / item["path"], item["sha256"], item["bytes"])
    for name in ("05.15.pack.md", "06.15.review.md"):
        if name == "06.15.review.md" and a.omit_review:
            continue
        rel = f"{PAGE}/{name}"
        put(rel, PACK16 / frozen[rel]["snapshot"], frozen[rel]["sha256"], frozen[rel]["bytes"])
    man = json.loads((LIVE / PAGE / "evidence/design05.15/artifact-manifest.json").read_bytes())
    put(f"{PAGE}/evidence/design05.15/artifact-manifest.json", LIVE / PAGE / "evidence/design05.15/artifact-manifest.json",
        frozen[f"{PAGE}/evidence/design05.15/artifact-manifest.json"]["sha256"], None)
    for row in man["files"]:
        if not (repo / row["path"]).exists():
            put(row["path"], LIVE / row["path"], row["sha256"], row["bytes"])
    (room / "fixture-manifest.json").write_text(json.dumps({"schema": "n7-intake-fixture/1", "repo": str(repo), "omit_review": a.omit_review,
                                                            "copied": copied}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"repo": str(repo), "files": len(copied), "omit_review": a.omit_review}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
