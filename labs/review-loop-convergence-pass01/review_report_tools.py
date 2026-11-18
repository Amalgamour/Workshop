#!/usr/bin/env python3
"""Unselected review-report door for the convergence candidate (0522/05.17).

Pins the candidate dispatcher under the supplied code root and the canonical
workbook and reporter under D:\\Git\\lib-build. Exit 0 is an observation.
A hash mismatch is a refusal, not a report.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
CANONICAL_FILE = REPO / "labs" / "review-loop-convergence-pass01" / "review_report_tools.py"
REPORT_REL = "labs/review-loop-convergence-pass01/report.py"
WORKBOOK_REL = "labs/review-loop-convergence-pass01/workbook.py"
LIBRARIAN_REL = "app/librarian.py"
LIBRARIAN_SHA = "bb9ee7363e88da77f088e7e1c9a57f2a1ab94436defec25b6a50cbe9e5a48efc"
LIBRARIAN_BYTES = 12936
REPORT_SHA = "b399b9a901bedcfb1ab97e6ee2c4d3e2730b5115f8bb583d983e3f1d660cb568"
REPORT_BYTES = 6494
WORKBOOK_SHA = "ef021d4ae4066f97bfb21017d5a7952ac5161dce82e82ebec1ca756e3f58f9d9"
WORKBOOK_BYTES = 20034
PASS = re.compile(r"^05\.\d\d$")
FLAGS = ("--book", "--source", "--pass")
REPARSE = 0x400


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _linked(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _pin(path: Path, size: int, digest: str, label: str) -> None:
    if _linked(path) or not path.is_file():
        refuse(f"{label} pin is missing")
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if len(data) != size or got != digest:
        refuse(f"{label} pin mismatch got {len(data)} bytes sha256 {got} want {size} bytes sha256 {digest}")


def parse_call(args: list[str]) -> dict[str, str]:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    values: dict[str, str] = {}
    index = 0
    while index < len(args):
        item = args[index]
        if not item.startswith("--"):
            refuse(f"unknown argument {item}")
        if "=" in item or item not in FLAGS:
            refuse(f"unknown flag {item.split('=', 1)[0]}")
        if item in values:
            refuse(f"repeated {item}")
        if index + 1 >= len(args) or args[index + 1].startswith("--") or args[index + 1] == "":
            refuse(f"missing value for {item}")
        values[item] = args[index + 1]
        index += 2
    for flag in FLAGS:
        if flag not in values:
            refuse(f"missing {flag}")
    if PASS.fullmatch(values["--pass"]) is None:
        refuse("pass is not 05.NN")
    source = values["--source"]
    if source.strip() == "" or source.startswith("-") or "/" in source or "\\" in source or "\n" in source or "\r" in source:
        refuse("source is a page id")
    book = values["--book"]
    if book.startswith("\\\\") or book.startswith("//"):
        refuse("book must be an absolute directory and was not followed when linked")
    path = Path(book)
    if not path.is_absolute() or ".." in path.parts:
        refuse("book must be an absolute directory and was not followed when linked")
    if _linked(path) or not path.is_dir():
        refuse("book must be an absolute directory and was not followed when linked")
    return {"book": book, "pass": values["--pass"], "source": source}


def _load_report():
    path = REPO / REPORT_REL
    spec = importlib.util.spec_from_file_location("convergence_report_runtime", path)
    if spec is None or spec.loader is None:
        refuse("reporter did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perform(args: list[str], code_root: Path) -> int:
    here = Path(__file__).resolve()
    if os.path.normcase(str(here)) != os.path.normcase(str(CANONICAL_FILE)):
        refuse("convergence report door is not at its canonical root")
    call = parse_call(args)
    _pin(Path(code_root) / LIBRARIAN_REL, LIBRARIAN_BYTES, LIBRARIAN_SHA, "dispatcher")
    _pin(REPO / WORKBOOK_REL, WORKBOOK_BYTES, WORKBOOK_SHA, "workbook")
    _pin(REPO / REPORT_REL, REPORT_BYTES, REPORT_SHA, "reporter")
    module = _load_report()
    try:
        body = module.observe(call["book"], call["source"], call["pass"])
    except module.Refuse as exc:
        refuse(exc.message)
    module.emit(body)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, REPO)
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
