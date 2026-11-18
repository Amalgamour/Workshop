#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 001
# Authorization: draft — 2026-10-26
# who: grok-4.7
# state: draft
# Face: 02
# PPPP: 0310
# desk: 00.kernel
# shelf: 00.kernel
# book: 00.00.20.sample
# keyword: inventory
# why: Fixture payload. List one synthetic book's pages and report a missing face.
#
# cite: 00.kernel/00.00.10.work/0504.app-entry/05.01.md

"""Write a JSON inventory of one book. Paths come from arguments, not the current directory."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def die(message: str) -> None:
    print(f"stop: {message}", file=sys.stderr)
    raise SystemExit(2)


def norm(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def inside(child: Path, parent: Path) -> bool:
    child_s = norm(child.resolve())
    parent_s = norm(parent.resolve())
    if child_s == parent_s:
        return True
    sep = os.path.normcase(os.sep)
    prefix = parent_s if parent_s.endswith(sep) else parent_s + sep
    return child_s.startswith(prefix)


def take(args: list[str], flag: str) -> str:
    if args.count(flag) != 1:
        die(f"missing {flag}")
    index = args.index(flag)
    if index + 1 >= len(args):
        die(f"missing value for {flag}")
    value = args[index + 1]
    del args[index : index + 2]
    return value


def main(argv: list[str]) -> None:
    args = list(argv)
    book = Path(take(args, "--book"))
    output = Path(take(args, "--output"))
    required = take(args, "--required-face")
    if args:
        die("unknown argument")
    if required != Path(required).name or required in ("", ".", ".."):
        die("required face is not a file name")
    if not book.is_dir():
        die("inventory book is missing")
    pages = []
    for page in sorted((item for item in book.iterdir() if item.is_dir()), key=lambda item: item.name):
        if not inside(page, book):
            die("page escapes the book")
        files = []
        for child in sorted((item for item in page.iterdir() if item.is_file()), key=lambda item: item.name):
            if not inside(child, page):
                die("file escapes the page")
            files.append(child.name)
        pages.append({
            "files": files,
            "missing_required_face": None if required in files else required,
            "page": page.name,
        })
    body = {
        "book": book.name,
        "pages": pages,
        "schema": "librarian-book-inventory",
        "version": 1,
    }
    if not inside(output, book.parent.parent):
        die("output escapes the fixture desk")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_bytes((json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    os.replace(temporary, output)


if __name__ == "__main__":
    main(sys.argv[1:])
