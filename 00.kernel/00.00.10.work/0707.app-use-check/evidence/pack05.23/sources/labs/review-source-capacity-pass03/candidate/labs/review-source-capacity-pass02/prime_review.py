#!/usr/bin/env python3
"""Source-capacity successor of labs/prime-review-pass02/prime_review.py.

The historical module stays byte-for-byte. This loader rebinds as_list so only
the sources collection uses MAX_SOURCES. MAX_LIST, MAX_DOC, and MAX_TEXT stay
on the historical module. This file does not assign MAX_LIST. The pass01
successor stays at its own 32-source bound.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HELPER = Path(r"D:\Git\lib-build")
PASS02_REL = "labs/prime-review-pass02/prime_review.py"
PASS02_SHA = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
PASS02_BYTES = 58560
MAX_SOURCES = 64
SOURCE_STEP = (
    "keep every source identity on this record and stop for a versioned successor "
    "whose source bound covers the count"
)


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_pass02():
    path = HELPER / PASS02_REL
    data = path.read_bytes()
    if len(data) != PASS02_BYTES or hashlib.sha256(data).hexdigest() != PASS02_SHA:
        refuse_boot("prime-review pass02 pin mismatch")
    spec = importlib.util.spec_from_file_location("prime_review_pass02_capacity64", path)
    if spec is None or spec.loader is None:
        refuse_boot("prime-review pass02 did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


base.as_list = as_list


def main(argv: list[str] | None = None) -> int:
    return base.main(argv)


if __name__ == "__main__":
    sys.exit(main())
