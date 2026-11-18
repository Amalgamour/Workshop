#!/usr/bin/env python3
"""0707/05.06 pass06: static path boundary checks (H02) with H04 path-input refusals. NONPRODUCTION.

Successor of pass05/guards.py (unchanged). H04 delta: path text is validated before
any filesystem call (non-empty, <= 32767 characters, no NUL or other C0 control),
and ValueError/OSError raised by a filesystem call here becomes Boundary("path-os").
Every other exception propagates.

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


MAX_PATH_TEXT = 32767
CONTROL = re.compile(r"[\x00-\x1f]")


def path_text(value, label: str) -> str:
    """Shape-only check of path text. Touches no filesystem."""
    if not isinstance(value, str) or not value:
        raise Boundary("path", f"{label} must be a non-empty string")
    if len(value) > MAX_PATH_TEXT:
        raise Boundary("path", f"{label} is longer than {MAX_PATH_TEXT} characters")
    if CONTROL.search(value):
        raise Boundary("path", f"{label} contains NUL or another control character")
    return value


def fs(call, what: str, *args, **kwargs):
    """Run one filesystem call; translate only ValueError/OSError into a coded refusal."""
    try:
        return call(*args, **kwargs)
    except (ValueError, OSError) as exc:
        raise Boundary("path-os", f"{what}: {type(exc).__name__}: {exc}") from None


def is_link_like(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except (FileNotFoundError, NotADirectoryError):
        return False
    except (ValueError, OSError) as exc:
        raise Boundary("path-os", f"lstat: {type(exc).__name__}: {exc}") from None
    if stat.S_ISLNK(st.st_mode) or (getattr(st, "st_file_attributes", 0) & REPARSE):
        return True
    is_junction = getattr(os.path, "isjunction", None)
    return bool(is_junction and fs(is_junction, "isjunction", p))


def chain_without_links(path: Path) -> None:
    """Refuse if the path or any existing ancestor is a link or reparse point."""
    p = Path(fs(os.path.abspath, "abspath", path))
    for part in [p, *p.parents]:
        if is_link_like(part):
            raise Boundary("reparse", f"{part} is a symlink, junction or reparse point")


def canonical(path: Path) -> Path:
    """Resolve the existing part strictly; the non-existing tail is appended lexically."""
    p = Path(fs(os.path.abspath, "abspath", path))
    existing, tail = p, []
    while not fs(os.path.lexists, "lexists", existing):
        tail.append(existing.name)
        if existing.parent == existing:
            break
        existing = existing.parent
    resolved = Path(fs(os.path.realpath, "realpath", existing, strict=True)) if fs(os.path.lexists, "lexists", existing) else existing
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


def output_root(text) -> Path:
    p = Path(path_text(text, "output_root"))
    if not p.is_absolute():
        raise Boundary("output-root", "output_root must be absolute")
    chain_without_links(p)
    if not fs(os.path.isdir, "isdir", p):
        raise Boundary("output-root", "output_root must be an existing directory")
    resolved = canonical(p)
    hit = protected_hit(resolved)
    if hit is not None:
        raise Boundary("protected", f"output_root resolves to {resolved}, which overlaps protected {hit}")
    return resolved


def evidence_root(text) -> Path:
    if not isinstance(text, str) or not text:
        raise Boundary("evidence", "--evidence is required")
    p = Path(path_text(text, "--evidence"))
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
    if fs(os.path.lexists, "lexists", path):
        raise Boundary("occupied", f"{path} already exists; it is not cleared or reused")
    try:
        path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise Boundary("occupied", f"{path} appeared before creation; it is not cleared or reused") from None
    except (ValueError, OSError) as exc:
        raise Boundary("path-os", f"mkdir: {type(exc).__name__}: {exc}") from None
    return resolved
