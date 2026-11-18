#!/usr/bin/env python3
"""Unselected review-report door for the pass02 candidate (0522/05.18).

Pins the dispatcher, workbook, and reporter under the supplied candidate root.
A hash mismatch is a refusal, not a report. Exit 0 is an observation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ENTRY = "app/librarian.py"
REPORT_REL = "labs/review-loop-convergence-pass02/report.py"
WORKBOOK_REL = "labs/review-loop-convergence-pass02/workbook.py"
LIBRARIAN_SHA = "dab1ab2e03ca779be5266a78d56f429878b93ce72d870fc3a40b702aa7973d10"
LIBRARIAN_BYTES = 13055
REPORT_SHA = "d17da33c4ea7a8b3ab65c16b0b339b4485010b3e938dfb8c42e2408652f6bc38"
REPORT_BYTES = 11434
WORKBOOK_SHA = "a013e4466c79794eb62c7f697d222e693d8453af91571a404fedb0b4dcc4ef3f"
WORKBOOK_BYTES = 6613
PASS = re.compile(r"^05\.\d\d$")
FLAGS = ("--book", "--source", "--pass")


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _pin(root: Path, rel: str, size: int, digest: str, label: str) -> Path:
    if rel.startswith(("/", "\\")) or ".." in rel.split("/"):
        refuse(f"{label} path escapes")
    path = root
    for part in rel.split("/"):
        path = path / part
        if path.is_symlink():
            refuse(f"{label} pin is linked")
    if not path.is_file():
        refuse(f"{label} pin is missing")
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if len(data) != size or got != digest:
        refuse(f"{label} pin mismatch got {len(data)} bytes sha256 {got} want {size} bytes sha256 {digest}")
    return path


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
    if path.is_symlink() or not path.is_dir():
        refuse("book must be an absolute directory and was not followed when linked")
    return {"book": book, "pass": values["--pass"], "source": source}


def perform(args: list[str], code_root: Path) -> int:
    call = parse_call(args)
    root = Path(code_root)
    _pin(root, ENTRY, LIBRARIAN_BYTES, LIBRARIAN_SHA, "dispatcher")
    _pin(root, WORKBOOK_REL, WORKBOOK_BYTES, WORKBOOK_SHA, "workbook")
    path = _pin(root, REPORT_REL, REPORT_BYTES, REPORT_SHA, "reporter")
    spec = importlib.util.spec_from_file_location("convergence_pass02_report_runtime", path)
    if spec is None or spec.loader is None:
        refuse("reporter did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        body = module.observe(call["book"], call["source"], call["pass"])
    except module.Refuse as exc:
        refuse(exc.message)
    module.emit(body)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
