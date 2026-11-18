#!/usr/bin/env python3
"""0707/05.05 pass05: static path boundary checks (H02). NONPRODUCTION.

A path is accepted only if every EXISTING component from the drive root down is
a plain directory or file (no symlink, junction or other reparse point), and its
resolved form is outside every protected root (or inside an explicitly
authorized evidence parent). This is a static check, not an OS sandbox, and it
does not prevent a same-user race between check and use.
"""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path

CHECKOUT = Path(r"D:\Git\lib-build")
LIVE_BOOK = CHECKOUT / "00.kernel" / "00.00.10.work"
PROTECTED = (CHECKOUT, LIVE_BOOK)
EVIDENCE_PARENT = LIVE_BOOK / "0707.app-use-check" / "evidence"
EVIDENCE_NAME = re.compile(r"^lab05\.(0[5-9]|[1-9][0-9])$")
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class Boundary(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def is_link_like(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(st.st_mode) or (getattr(st, "st_file_attributes", 0) & REPARSE):
        return True
    is_junction = getattr(os.path, "isjunction", None)
    return bool(is_junction and is_junction(p))


def chain_without_links(path: Path) -> None:
    """Refuse if the path or any existing ancestor is a link or reparse point."""
    p = Path(os.path.abspath(path))
    for part in [p, *p.parents]:
        if is_link_like(part):
            raise Boundary("reparse", f"{part} is a symlink, junction or reparse point")


def canonical(path: Path) -> Path:
    """Resolve the existing part strictly; the non-existing tail is appended lexically."""
    p = Path(os.path.abspath(path))
    existing, tail = p, []
    while not existing.exists():
        tail.append(existing.name)
        if existing.parent == existing:
            break
        existing = existing.parent
    resolved = Path(os.path.realpath(existing, strict=True)) if existing.exists() else existing
    for name in reversed(tail):
        resolved = resolved / name
    return resolved


def within(child: Path, parent: Path) -> bool:
    c = os.path.normcase(str(child))
    p = os.path.normcase(str(parent)).rstrip("\\/")
    return c == p or c.startswith(p + os.sep)


def protected_hit(resolved: Path) -> Path | None:
    for root in PROTECTED:
        r = canonical(root)
        if within(resolved, r) or within(r, resolved):
            return root
    return None


def output_root(path_text) -> Path:
    if not isinstance(path_text, str) or not path_text:
        raise Boundary("shape", "output_root must be a non-empty string")
    p = Path(path_text)
    if not p.is_absolute():
        raise Boundary("output-root", "output_root must be absolute")
    chain_without_links(p)
    if not p.is_dir():
        raise Boundary("output-root", "output_root must be an existing directory")
    resolved = canonical(p)
    hit = protected_hit(resolved)
    if hit is not None:
        raise Boundary("protected", f"output_root resolves to {resolved}, which overlaps protected {hit}")
    return resolved


def evidence_root(path_text) -> Path:
    if not isinstance(path_text, str) or not path_text:
        raise Boundary("evidence", "--evidence is required")
    p = Path(path_text)
    if not p.is_absolute():
        raise Boundary("evidence", "--evidence must be absolute")
    chain_without_links(p)
    resolved = canonical(p)
    parent = canonical(EVIDENCE_PARENT)
    if not within(resolved, parent) or resolved == parent:
        raise Boundary("evidence", f"evidence must be under {EVIDENCE_PARENT}")
    first = resolved.relative_to(parent).parts[0]
    if not EVIDENCE_NAME.fullmatch(first):
        raise Boundary("evidence", f"evidence must be inside a lab05.NN directory (05 or later), not {first}")
    return resolved


def fresh_dir(path: Path, inside_root: Path) -> Path:
    """Create a NEW directory under an already-checked root; refuse occupied or escaping paths."""
    chain_without_links(path.parent)
    resolved = canonical(path)
    if not within(resolved, inside_root):
        raise Boundary("escape", f"{resolved} is not under {inside_root}")
    if os.path.lexists(path):
        raise Boundary("occupied", f"{path} already exists; it is not cleared or reused")
    path.mkdir(parents=True, exist_ok=False)
    return resolved
