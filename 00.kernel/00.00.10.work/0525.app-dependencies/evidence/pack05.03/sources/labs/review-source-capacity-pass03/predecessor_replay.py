#!/usr/bin/env python3
"""32-bound reproduction. Points prime_review at the byte-copied pass01 successor.

Does not edit labs/review-source-capacity-pass01. The copy must already match
the pass01 successor hash.
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
PASS03_REL = "labs/workbook-review-pass03/workbook.py"
PASS03_SHA = "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c"
PASS03_BYTES = 19533
PRIOR_REL = "labs/review-source-capacity-pass01/prime_review.py"
PRIOR_SHA = "a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87"
PRIOR_BYTES = 2031


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_pass03():
    path = HELPER / PASS03_REL
    data = path.read_bytes()
    if len(data) != PASS03_BYTES or hashlib.sha256(data).hexdigest() != PASS03_SHA:
        refuse_boot("pass03 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_pass03_prior32", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass03 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        refuse_boot("predecessor replay requires a code root")
    root = Path(args[0]).resolve()
    if root == HELPER.resolve():
        refuse_boot("predecessor replay root is the helper checkout")
    if (root / "00.kernel" / "00.00.10.work").exists():
        refuse_boot("predecessor replay root contains the work book")
    successor = root / PRIOR_REL
    data = successor.read_bytes() if successor.is_file() else b""
    if len(data) != PRIOR_BYTES or hashlib.sha256(data).hexdigest() != PRIOR_SHA:
        refuse_boot("pass01 capacity pin mismatch")
    module = load_pass03()
    wb = module.wb
    wb.REPO = root
    original = wb.pin_file

    def pin_file(key: str) -> Path:
        if key == "prime_review":
            return successor
        return original(key)

    wb.pin_file = pin_file
    return module.main(args[1:])


if __name__ == "__main__":
    sys.exit(main())
