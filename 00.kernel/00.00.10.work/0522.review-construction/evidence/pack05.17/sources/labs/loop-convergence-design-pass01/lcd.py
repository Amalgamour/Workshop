#!/usr/bin/env python3
"""loop-convergence lab library (0707/05.19). NONPRODUCTION.

Reuses the accepted 0707/05.18 root builder (labs/review-entry-integration-pass01/rie.py, imported read-only) for
the CODE layer: live app files + v8-pinned labs + the disclosed one-line pass04 root adapter + lab v8 declaration.
The SOURCE layer differs from 05.18: page files come ONLY from pack05.19 snapshots (no live page globbing, so no
unfrozen lane output can enter a root). Declared submission/manifest and manifest rows are verified by hash.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LIVE / "labs/review-entry-integration-pass01"))
import rie  # noqa: E402

PACK19 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.19"
BOOK_REL = rie.BOOK_REL
FIX = {
    "n5-0512-0509": {"page": "0512.prime-review", "pass": "05.09", "pointer": "05.09.md", "kind": "N5NN"},
    "n5-0522-0514": {"page": "0522.review-construction", "pass": "05.14", "pointer": "05.14.md", "kind": "N5NN"},
    "n7-0515": {"page": "0707.app-use-check", "pass": "05.15", "pointer": "05.15.pack.md", "kind": "N7NN"},
    "n7-0517": {"page": "0707.app-use-check", "pass": "05.17", "pointer": "05.17.pack.md", "kind": "N7NN"},
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frozen() -> dict:
    m = json.loads((PACK19 / "source-manifest.json").read_text(encoding="utf-8"))
    return {f["path"]: f for f in m["files"]}


def put_frozen(root: "rie.Root", rel: str, fz: dict) -> None:
    f = fz[rel]
    data = (PACK19 / f["snapshot"]).read_bytes()
    if sha(data) != f["sha256"]:
        raise SystemExit(f"refused: snapshot {rel}")
    root.put_bytes(rel, data, "pack05.19-snapshot", "pack05.19")


def build_source(root: "rie.Root", key: str, omit: tuple = ()) -> dict:
    fx = FIX[key]
    fz = frozen()
    page_rel = f"{BOOK_REL}/{fx['page']}"
    for rel in sorted(fz):
        if rel.startswith(page_rel + "/") and rel.count("/") == page_rel.count("/") + 1 and rel.endswith(".md"):
            if rel.rsplit("/", 1)[1] not in omit and not (root.path / rel).exists():
                put_frozen(root, rel, fz)
    pointer = (root.path / page_rel / fx["pointer"]).read_text(encoding="utf-8")
    declared = rie.declared_from_pointer(pointer, page_rel, fx["kind"])
    for role in ("Submission", "Artifact manifest"):
        rel, h, n = declared[role]
        if not (root.path / rel).exists():
            if rel in fz:
                put_frozen(root, rel, fz)
            else:
                root.put_live(rel, h, n, "pointer")
        if sha((root.path / rel).read_bytes()) != h:
            raise SystemExit(f"refused: declared {role} differs")
    man = json.loads((root.path / declared["Artifact manifest"][0]).read_bytes())
    for row in man["files"]:
        if not (root.path / row["path"]).exists():
            if row["path"] in fz and fz[row["path"]]["sha256"] == row["sha256"]:
                put_frozen(root, row["path"], fz)
            else:
                root.put_live(row["path"], row["sha256"], row["bytes"], "manifest-row")
    return {"declared": {k: list(v) for k, v in declared.items()}, "manifest_rows": [r["path"] for r in man["files"]]}


def make_root(path: Path, keys: list, omit: tuple = (), dispatcher: str = "v8") -> tuple:
    rie.refuse_inside(path)
    path.mkdir(parents=True, exist_ok=False)
    r = rie.Root(path)
    rie.build_code(r)
    info = {k: build_source(r, k, omit) for k in keys}
    rie.select(path, dispatcher)
    (path / "ROOT-INDEX.json").write_text(json.dumps({"schema": "lcd-root/1", "fixtures": keys, "omit": list(omit), "copied": r.copied}, indent=1) + "\n",
                                          encoding="utf-8")
    return r, info


def args(root: Path, key: str, cmd: str, *extra) -> list:
    fx = FIX[key] if isinstance(key, str) else key
    return [cmd, "--book", str(Path(root) / BOOK_REL), "--source", fx["page"], "--pass", fx["pass"], *extra]


def body(res: dict) -> dict:
    return res.get("body") if isinstance(res.get("body"), dict) else {}


def codes(res: dict) -> list:
    return sorted({f.get("code") for f in body(res).get("findings") or [] if isinstance(f, dict)})


def book_sources(res: dict) -> int:
    """Rows pass03 prime_record would emit: root book, roles assignment/return/artifact/submission/verification,
    grouped by path (the record groups by resolved key)."""
    rows = rie.rows_of(body(res))
    keep = {r.get("path") for r in rows if r.get("root", "book") == "book" and r.get("role") in {"assignment", "return", "artifact", "submission", "verification"}}
    return len(keep)
