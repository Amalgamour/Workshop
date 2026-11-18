#!/usr/bin/env python3
"""Lab adapter for the 64-source successor.

Loads the pinned pass03 workbook from the helper checkout D:\\Git\\lib-build.
Pass03 loads pass02 and pass01 from that same helper. This file then points
the pass01 REPO at Path(__file__).resolve().parents[2] and points
pin_file("prime_review") at the sibling successor.

In the proof tree that directory holds the pinned code files and omits the
work book. At the same relative path in the checkout, that directory is the
checkout. Source grouping, root filtering, and freshness stay on pass03.
This adapter is not the pass01 adapter and it is not the production pin.
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
SUCCESSOR_NAME = "prime_review.py"
SUCCESSOR_SHA = "32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f"
SUCCESSOR_BYTES = 2160


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def digest(path: Path) -> bytes:
    return path.read_bytes()


def load_pass03():
    path = HELPER / PASS03_REL
    data = digest(path)
    if len(data) != PASS03_BYTES or hashlib.sha256(data).hexdigest() != PASS03_SHA:
        refuse_boot("pass03 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_pass03_capacity64", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass03 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    successor = here / SUCCESSOR_NAME
    module = load_pass03()
    wb = module.wb
    try:
        wb.REPO = root
        copy = root / PASS03_REL
        if wb.is_link(copy) or not copy.is_file():
            wb.refuse("pass03 workbook copy is missing")
        copied = digest(copy)
        if len(copied) != PASS03_BYTES or hashlib.sha256(copied).hexdigest() != PASS03_SHA:
            wb.refuse("pass03 workbook copy pin mismatch")
        if wb.is_link(successor) or not successor.is_file():
            wb.refuse("prime_review capacity pin is missing")
        data = digest(successor)
        if len(data) != SUCCESSOR_BYTES or hashlib.sha256(data).hexdigest() != SUCCESSOR_SHA:
            wb.refuse("prime_review capacity pin mismatch")
        original = wb.pin_file

        def pin_file(key: str) -> Path:
            if key == "prime_review":
                return successor
            return original(key)

        wb.pin_file = pin_file
        return module.main(argv)
    except wb.Refusal as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
