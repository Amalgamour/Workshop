#!/usr/bin/env python3
"""Referenced-source successor of labs/prime-review-pass02/prime_review.py.

The historical module stays byte-for-byte. This loader rebinds as_list so only
the sources collection uses MAX_SOURCES, rebinds count so only source
content_bytes and transport_bytes use MAX_SOURCE_BYTES, and rebinds bind_file
so a bound source is hashed in chunks under that same source limit.

MAX_LIST, MAX_DOC, and MAX_TEXT stay on the historical module. read_regular,
strict_json, and load_input stay on MAX_DOC. This file does not assign
MAX_LIST or MAX_DOC. The 16 MiB figure is a referenced-source limit, not an
inline budget and not a prompt-context budget. The pass01 successor stays at
its 32-source bound. The pass02 successor stays at its 64-source bound and
still caps source byte fields at MAX_DOC.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HELPER = Path(r"D:\Git\lib-build")
PASS02_REL = "labs/prime-review-pass02/prime_review.py"
PASS02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
PASS02_BYTES = 58560
PASS01_CAPACITY_REL = "labs/review-source-capacity-pass01/prime_review.py"
PASS01_CAPACITY_SHA = "a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87"
PASS01_CAPACITY_BYTES = 2031
PASS02_CAPACITY_REL = "labs/review-source-capacity-pass02/prime_review.py"
PASS02_CAPACITY_SHA = "32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f"
PASS02_CAPACITY_BYTES = 2160
MAX_SOURCES = 64
MAX_SOURCE_BYTES = 16777216
CHUNK = 65536
SOURCE_STEP = (
    "keep every source identity on this record and stop for a versioned successor "
    "whose source bound covers the count"
)
SOURCE_SIZE_STEP = (
    "keep the source file and its declared hash intact and stop for a versioned successor "
    "whose referenced-source bound covers the length"
)


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def pin_file(rel: str, digest: str, size: int, label: str) -> None:
    path = HELPER / rel
    data = path.read_bytes() if path.is_file() else b""
    if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
        refuse_boot(f"{label} pin mismatch")


def load_pass02():
    path = HELPER / PASS02_REL
    data = path.read_bytes()
    if len(data) != PASS02_BYTES or hashlib.sha256(data).hexdigest() != PASS02_SHA:
        refuse_boot("prime-review pass02 pin mismatch")
    spec = importlib.util.spec_from_file_location("prime_review_pass02_source16m", path)
    if spec is None or spec.loader is None:
        refuse_boot("prime-review pass02 did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pin_file(PASS01_CAPACITY_REL, PASS01_CAPACITY_SHA, PASS01_CAPACITY_BYTES, "capacity pass01")
pin_file(PASS02_CAPACITY_REL, PASS02_CAPACITY_SHA, PASS02_CAPACITY_BYTES, "capacity pass02")
base = load_pass02()


def as_list(value, where: str):
    base.need(isinstance(value, list), f"bad type {where}")
    if where == "sources":
        count = len(value)
        if count > MAX_SOURCES:
            raise base.Refusal(
                f"limit sources: {count} sources exceeds supported limit {MAX_SOURCES}; {SOURCE_STEP}"
            )
        return value
    base.need(len(value) <= base.MAX_LIST, f"limit {where}")
    return value


def count(value, where: str) -> int:
    base.need(isinstance(value, int) and not isinstance(value, bool), f"bad type {where}")
    if where.endswith(".content_bytes") or where.endswith(".transport_bytes"):
        if value < 0:
            raise base.Refusal(f"limit {where}")
        if value > MAX_SOURCE_BYTES:
            raise base.Refusal(
                f"limit {where}: {value} bytes exceeds supported referenced-source limit "
                f"{MAX_SOURCE_BYTES}; {SOURCE_SIZE_STEP}"
            )
        return value
    base.need(0 <= value <= base.MAX_DOC, f"limit {where}")
    return value


def bind_file(root: Path, source: dict) -> None:
    parts = source["logical_path"].split("/")
    current = root
    base.refuse_link(base.lstat_kind(current), "root")
    for part in parts[:-1]:
        current = current / part
        info = base.lstat_kind(current)
        base.refuse_link(info, part)
        base.need(stat.S_ISDIR(info.st_mode), f"not a directory {part}")
    candidate = current / parts[-1]
    base.need(base.inside(candidate, root), "path escapes root")
    where = source["logical_path"]
    info = base.lstat_kind(candidate)
    base.refuse_link(info, where)
    base.need(stat.S_ISREG(info.st_mode), f"not a regular file {where}")
    base.need(info.st_nlink == 1, f"hard link {where}")
    actual = info.st_size
    if actual > MAX_SOURCE_BYTES:
        raise base.Refusal(
            f"limit {where}: bound file length {actual} exceeds supported referenced-source limit "
            f"{MAX_SOURCE_BYTES}; {SOURCE_SIZE_STEP}"
        )
    digest = hashlib.sha256()
    read = 0
    try:
        with candidate.open("rb") as handle:
            while True:
                block = handle.read(CHUNK)
                if not block:
                    break
                read += len(block)
                if read > MAX_SOURCE_BYTES:
                    raise base.Refusal(
                        f"limit {where}: bound file length {read} exceeds supported referenced-source limit "
                        f"{MAX_SOURCE_BYTES}; {SOURCE_SIZE_STEP}"
                    )
                digest.update(block)
    except OSError as exc:
        raise base.Refusal(f"cannot read {where}: {exc.errno}") from None
    base.need(read == source["transport_bytes"], "bound file length mismatch")
    base.need(digest.hexdigest() == source["transport_sha256"], "bound file hash mismatch")


base.as_list = as_list
base.count = count
base.bind_file = bind_file


def main(argv: list[str] | None = None) -> int:
    return base.main(argv)


if __name__ == "__main__":
    sys.exit(main())
