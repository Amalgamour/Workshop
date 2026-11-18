"""Read-only check of the pinned pack identities. Nothing here is imported as a runtime dependency."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .bookio import repo_root
from .identity import Refused

MANIFEST = Path("00.kernel/00.00.10.work/0523.desk-core/evidence/pack05.01/source-manifest.json")


def verify(root: Path | None = None) -> dict[str, object]:
    repo = (root or repo_root()).resolve()
    path = repo / MANIFEST
    if not path.is_file() or path.is_symlink():
        raise Refused("pins", "source manifest is missing")
    manifest = json.loads(path.read_bytes().decode("utf-8"))
    if manifest.get("schema") != "prime-pack-sources/1":
        raise Refused("pins", "source manifest schema mismatch")
    rows = manifest.get("sources")
    if type(rows) is not list:
        raise Refused("pins", "source manifest has no sources")
    failed: list[str] = []
    for row in rows:
        rel = row["path"]
        blob = (repo / rel).read_bytes()
        snap = (path.parent / row["snapshot"]).read_bytes()
        digest = hashlib.sha256(blob).hexdigest()
        if blob != snap or len(blob) != row["bytes"] or digest != row["sha256"]:
            failed.append(rel)
    if failed:
        raise Refused("pins", "source pins mismatch", failed=failed)
    return {
        "schema": "desk-core-result/1",
        "ok": True,
        "command": "pins",
        "accepted": False,
        "sources": len(rows),
        "matched": len(rows),
        "runtime_imports": [],
        "runtime_dependencies": ["python-stdlib"],
        "note": "pinned app and lab modules are not imported by desk_core",
    }
