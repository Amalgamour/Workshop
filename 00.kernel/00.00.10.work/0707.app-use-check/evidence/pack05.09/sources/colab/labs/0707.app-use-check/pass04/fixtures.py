#!/usr/bin/env python3
"""0707/05.04 pass04: NONPRODUCTION fixture builders. Copy-only; every source is pin-checked first.

Books are built in NEW directories under the config's output_root (outside the
checkout). Old evidence and snapshots are read, never written. The decision recipe
is pass01 decide.py, imported read-only after its hash check; its words are pass01's
SUPPLIED judgment (synthetic, not Prime's or the Director's).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

CHECKOUT = Path(r"D:\Git\lib-build")
PAGE = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check"
PACK1 = PAGE / "evidence" / "pack05.01"
PACK4 = PAGE / "evidence" / "pack05.04"
OLD = PAGE / "evidence" / "build05.01"
MEMBER = "0182.desk-app-integration-design-0501"
TARGET = "0519.desk-app/05.01.md"
PENDING = (
    "# SYNTHETIC PENDING target - 0707 lab05.04\n"
    "Not a real page. Disposable book only. OUTSIDE-0504-TOKEN\n\n"
    "## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n## Notes\nTAIL-0504-TOKEN\n"
).encode("utf-8")
NO_HEADING = b"# SYNTHETIC page without a review heading - lab05.04\n\n## Return pointer\nPENDING.\n"
DUPLICATE = b"# SYNTHETIC two review headings - lab05.04\n\n## Review - Codex Prime\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n"
ASSIGNMENT = b"SYNTHETIC assignment for lab05.04: review the copied 0182 return in a disposable book.\n"
NOTE = b"SYNTHETIC note for lab05.04: the copied return bytes are the evidence file.\n"


class FixtureError(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pins(manifest: Path) -> dict:
    return {r["path"]: r for r in json.loads(manifest.read_text(encoding="utf-8"))["files"]}


def pinned_snapshot(pack: Path, rel: str) -> bytes:
    row = pins(pack / "source-manifest.json")[rel]
    data = Path(row["snapshot"]).read_bytes() if Path(row["snapshot"]).is_absolute() else (CHECKOUT / row["snapshot"]).read_bytes()
    if sha(data) != row["sha256"] or len(data) != row["bytes"]:
        raise FixtureError(f"snapshot {rel} differs from its pin")
    return data


def old_artifact(rel_in_run: str) -> Path:
    """A file of 0707/05.01 evidence, checked against that pass's artifact manifest."""
    path = OLD / "runs" / "run1" / rel_in_run
    manifest = {r["path"]: r for r in json.loads((OLD / "artifact-manifest.json").read_text(encoding="utf-8"))["files"]}
    key = path.relative_to(CHECKOUT).as_posix()
    row = manifest.get(key)
    if row is None or sha(path.read_bytes()) != row["sha256"]:
        raise FixtureError(f"05.01 artifact {key} is not bound by its manifest")
    return path


def page_bytes(kind: str) -> bytes | None:
    return {
        "pending": PENDING,
        "pending-crlf": PENDING.replace(b"\n", b"\r\n"),
        "substantive": pinned_snapshot(PACK1, "00.kernel/00.00.10.work/0519.desk-app/05.01.md"),
        "no-heading": NO_HEADING,
        "duplicate-heading": DUPLICATE,
        "absent": None,
    }[kind]


def build_book(root: Path, kind: str) -> dict:
    """A fresh disposable book; returns the source identities used."""
    root.mkdir(parents=True, exist_ok=False)
    used = {}
    if kind == "legacy-v1-recorded":
        src = OLD / "runs" / "run1" / "books" / "A.after-record"
        tree = json.loads(old_artifact("books/A.after-record.tree.json").read_text(encoding="utf-8"))
        shutil.copytree(src, root, dirs_exist_ok=True)
        for rel, digest in tree.items():
            if sha((root / rel).read_bytes()) != digest:
                raise FixtureError(f"legacy book copy differs at {rel}")
        return {"legacy_book_tree_sha256": sha(json.dumps(tree, sort_keys=True).encode())}
    pack_pins = pins(PACK1 / "source-manifest.json")
    prefix = f"00.kernel/00.00.10.work/{MEMBER}/"
    for rel, row in pack_pins.items():
        if rel.startswith(prefix):
            data = pinned_snapshot(PACK1, rel)
            dest = root / MEMBER / rel[len(prefix):]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            used[rel] = row["sha256"]
    page = page_bytes(kind)
    if page is not None:
        (root / TARGET).parent.mkdir(parents=True)
        (root / TARGET).write_bytes(page)
        used["target"] = sha(page)
    (root / "assignment.txt").write_bytes(ASSIGNMENT)
    (root / "note.md").write_bytes(NOTE)
    (root / "registration.json").write_bytes(pinned_snapshot(PACK4, "labs/prime-entry-pilot-pass01/example-registration.json"))
    (root / "request.json").write_bytes(pinned_snapshot(PACK4, "labs/prime-entry-pilot-pass01/example-request.json"))
    return used


def plant_descriptor(root: Path, describe_json: dict) -> None:
    (root / "descriptor.json").write_bytes(
        (json.dumps(describe_json["descriptor"], ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def decide_module():
    path = CHECKOUT / "colab/labs/0707.app-use-check/pass01/decide.py"
    data = path.read_bytes()
    row = pins(PACK4 / "source-manifest.json")["colab/labs/0707.app-use-check/pass01/decide.py"]
    if sha(data) != row["sha256"]:
        raise FixtureError("pass01 decide.py differs from its pin")
    spec = importlib.util.spec_from_file_location("pass01_decide_readonly", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def supplied_words(next_action: str | None = None) -> dict:
    words = json.loads(pinned_snapshot(PACK4, "colab/labs/0707.app-use-check/pass01/supplied-judgment.json"))
    if next_action is not None:
        words["record_judgment"]["next_action"] = next_action
        words["record_judgment"]["sections_text"]["next_bounded_action"] = next_action
    return words


def write_decision(root: Path, template: dict, next_action: str | None = None) -> bytes:
    decision = decide_module().build(root, template, supplied_words(next_action))
    raw = (json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (root / "decision.json").write_bytes(raw)
    return raw


# ---------------------------------------------------------------- state and mutations
def tree(root: Path) -> dict[str, str]:
    out = {}
    if root.exists():
        for p in sorted(root.rglob("*")):
            if p.is_file():
                out[p.relative_to(root).as_posix()] = sha(p.read_bytes())
    return out


def cycle_dir(root: Path) -> Path:
    dirs = [p for p in (root / "cycle").iterdir() if p.is_dir()] if (root / "cycle").is_dir() else []
    if len(dirs) != 1:
        raise FixtureError(f"expected one cycle review directory, found {len(dirs)}")
    return dirs[0]


def edit_json(path: Path, fn) -> None:
    body = json.loads(path.read_text(encoding="utf-8"))
    fn(body)
    path.write_bytes((json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))).encode("utf-8"))


def change_target_outside_section(root: Path) -> None:
    page = root / TARGET
    data = page.read_bytes()
    new = data.replace(b"OUTSIDE-0504-TOKEN", b"OUTSIDE-0504-TOKEX", 1)
    if new == data:
        raise FixtureError("outside token not found")
    page.write_bytes(new)
