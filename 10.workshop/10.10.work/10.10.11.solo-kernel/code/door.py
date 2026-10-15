#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""door.py — read and write a 00.md sentinel.

A one-line file is a proof. The line is the title.
A sentinel has Sentinel, Permission, and Authority.
The workshop door is the one-line form. The kernel desk door is the sentinel.
This program writes only under the solo book. It does not write either kernel.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, desk drill
# Law 0051 says the desk door is one line. Syntax 0014 says name the sections.
# The approved kernel desk door has the sections. Both forms stay readable.

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from desk import SOLO
from face import EM, die, refuse_kernel_write
NEED = ("Sentinel", "Permission", "Authority")


def in_solo(path: Path) -> None:
    refuse_kernel_write(path)
    if SOLO not in path.resolve().parts:
        die("writes stay in the solo book")


def headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def one_line(text: str) -> str:
    body = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not body or "\n" in body or body.startswith("#") or ":" in body:
        return ""
    return body


def classify(text: str) -> tuple[str, str]:
    proof = one_line(text)
    if proof:
        return "proof", proof
    have = headings(text)
    missing = [name for name in NEED if name not in have]
    if not missing and text.lstrip().startswith("#"):
        return "sentinel", ""
    if missing:
        return "broken", "missing " + ", ".join(missing)
    return "broken", "not a sentinel"


def render_sentinel(
    keyword: str,
    why: str,
    rows: list[str],
    sentinel: list[str],
    permission: list[str],
    authority: list[str],
    not_this: list[str],
    who: str,
) -> str:
    if not who.strip():
        die("who is required")
    lines = [
        "# 00",
        "",
        "version: 001",
        f"Authorization: draft {EM} {date.today().isoformat()}",
        f"who: {who}",
        "state: draft",
        f"keyword: {keyword}",
        *rows,
        f"why: {why}",
        "",
        "## Sentinel",
        "",
        *sentinel,
        "",
        "## Permission",
        "",
        *permission,
        "",
        "## Authority",
        "",
        *authority,
        "",
        "## Not this file",
        "",
        *not_this,
        "",
    ]
    return "\n".join(lines)


def write_door(folder: Path, text: str, replace: bool = False) -> Path:
    in_solo(folder)
    if not folder.is_dir():
        die("folder is missing")
    dest = folder / "00.md"
    if dest.exists() and not replace:
        die("00.md is already here")
    if dest.exists() and replace:
        kind, _detail = classify(dest.read_text(encoding="utf-8"))
        if kind == "sentinel":
            die("door is already solved")
    dest.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
    return dest


def write_furniture(folder: Path, name: str, text: str) -> Path:
    in_solo(folder)
    dest = folder / name
    if dest.exists():
        die(f"{name} is already here")
    dest.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
    return dest


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    check(one_line("workshop\n") == "workshop", "one line")
    check(classify("# 00\n\n## Sentinel\n\n## Permission\n\n## Authority\n")[0] == "sentinel", "sections")
    kind, detail = classify("# 00\n\n## Sentinel\n")
    check(kind == "broken" and "Permission" in detail and "Authority" in detail, "missing sections")
    text = render_sentinel(
        "guide",
        "Book sentinel.",
        ["book: 10.10.10.guide"],
        ["This is the book sentinel of `10.10.10.guide`. It proves the book."],
        ["This file is the permission for this book to exist."],
        ["Kernel: `00.00.00.kernel`."],
        ["This file is not the template sentinel."],
        "grok-prime",
    )
    check("## Permission" in text and "proves the book" in text, "render")
    check("state: draft" in text, "draft")
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / SOLO / "drill" / "10.10.10.guide"
        book.mkdir(parents=True)
        made = write_door(book, "guide\n")
        check(made.read_text(encoding="utf-8") == "guide\n", "proof write")
        made = write_door(book, text, replace=True)
        check(classify(made.read_text(encoding="utf-8"))[0] == "sentinel", "replaced")
        try:
            write_door(book, text, replace=True)
            die("test replaced a solved door")
        except SystemExit as exc:
            check("already solved" in str(exc), "second replace stops")
        blocked = root / "00.00.00.kernel.draft" / "00.00.01.law"
        blocked.mkdir(parents=True)
        try:
            write_door(blocked, text)
            die("test wrote the template")
        except SystemExit as exc:
            check("template kernel is not edited" in str(exc) or "solo book" in str(exc), "kernel write stops")
        outside = root / "12.other"
        outside.mkdir()
        try:
            write_door(outside, "other\n")
            die("test wrote outside the solo book")
        except SystemExit as exc:
            check("solo book" in str(exc), "outside stops")
    print("test: pass")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        cmd_test()
    else:
        die("use test")
