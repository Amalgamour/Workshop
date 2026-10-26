#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""door.py — read and write a 00.md sentinel.

A one-line file is a proof. The line is the title.
A sentinel has Sentinel, Permission, and Authority.
The workshop door is the one-line form. The kernel desk door is the sentinel.
This program writes under the solo book. It also writes 00.md on 00.kernel and on that desk's two books.
It does not write either kernel.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, desk drill
# Law 0051 says the desk door is one line. Syntax 0014 says name the sections.
# The approved kernel desk door has the sections. Both forms stay readable.
# born: 2026-10-20
# source: director, >run.0511.05.04, and 0411.kernel-desk/06.04.md
# who: grok-builder
# write writes a sentinel. 00.kernel and its two books are allowed.
# The solo book still works. Any other path stops. The check kernel and the draft kernel stay closed.
# born: 2026-10-20
# source: director, >run.0513.05.05, and 0413.law-align/06.05.md
# who: grok-builder
# A new sentinel carries the century band rule. NN00 starts. NN99 is the end sentinel. Only 00NN is decades.

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from desk import SOLO
from face import EM, die, refuse_kernel_write
NEED = ("Sentinel", "Permission", "Authority")


DESK = "00.kernel"
BOOKS = ("00.00.00.syntax", "00.00.01.law")
CENTURY = (
    "Normal bands are centuries. A band starts at NN00. NN99 is the end sentinel. "
    "Only the 00NN range is decades. A user band may expand. One example is 1200 through 1499."
)


def in_solo(path: Path) -> None:
    refuse_kernel_write(path)
    folder = path.resolve()
    if SOLO in folder.parts:
        return
    if folder.name == DESK:
        return
    if folder.parent.name == DESK and folder.name in BOOKS:
        return
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
        "## Bands",
        "",
        CENTURY,
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


def take_flag(argv: list[str], flag: str) -> str:
    if flag not in argv:
        die(f"write needs {flag}")
    at = argv.index(flag)
    if at + 1 >= len(argv) or argv[at + 1].startswith("--"):
        die(f"write needs {flag}")
    return argv[at + 1]


def cmd_write(argv: list[str]) -> None:
    if not argv or argv[0].startswith("--"):
        die("write needs a folder")
    folder = Path(argv[0])
    who = take_flag(argv, "--who")
    keyword = take_flag(argv, "--keyword")
    why = take_flag(argv, "--why")
    rows = []
    if "--desk" in argv:
        rows.append(f"desk: {take_flag(argv, '--desk')}")
    if "--book" in argv:
        rows.append(f"book: {take_flag(argv, '--book')}")
    text = render_sentinel(
        keyword,
        why,
        rows,
        [f"This is the sentinel of `{folder.name}`. It proves the folder."],
        ["This file is the permission for this folder to exist."],
        ["Local: this file."],
        ["This file is not a page."],
        who,
    )
    made = write_door(folder, text)
    kind, detail = classify(made.read_text(encoding="utf-8"))
    if kind != "sentinel":
        die(f"write is not a sentinel: {detail}")
    print(f"wrote: {made}")


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
    check("NN99 is the end sentinel" in text, "century rule")
    check("no decades" not in text, "decade sentence")
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
        desk = root / "00.kernel"
        syntax = desk / "00.00.00.syntax"
        law = desk / "00.00.01.law"
        other = desk / "00.00.02.other"
        nested = syntax / "0100.band"
        for folder in (desk, syntax, law, other, nested):
            folder.mkdir(parents=True)
        cmd_write([
            str(syntax),
            "--who", "grok-builder",
            "--keyword", "syntax",
            "--why", "Book sentinel.",
            "--desk", "00.kernel",
            "--book", "00.00.00.syntax",
        ])
        check(classify((syntax / "00.md").read_text(encoding="utf-8"))[0] == "sentinel", "desk book sentinel")
        cmd_write([str(desk), "--who", "grok-builder", "--keyword", "kernel", "--why", "Desk sentinel."])
        check(classify((desk / "00.md").read_text(encoding="utf-8"))[0] == "sentinel", "desk sentinel")
        try:
            cmd_write([str(other), "--who", "grok-builder", "--keyword", "other", "--why", "No."])
            die("test wrote a third book")
        except SystemExit as exc:
            check("solo book" in str(exc), "third book stops")
        try:
            cmd_write([str(nested), "--who", "grok-builder", "--keyword", "band", "--why", "No."])
            die("test wrote a nested page")
        except SystemExit as exc:
            check("solo book" in str(exc), "nested page stops")
        import subprocess
        cold_root = root / "cold"
        cold_book = cold_root / "00.kernel" / "00.00.01.law"
        cold_book.mkdir(parents=True)
        proc = subprocess.run(
            [
                sys.executable, str(Path(__file__).resolve()), "write", str(cold_book),
                "--who", "grok-builder", "--keyword", "law", "--why", "Book sentinel.",
                "--desk", "00.kernel", "--book", "00.00.01.law",
            ],
            capture_output=True, text=True,
        )
        check(proc.returncode == 0 and "wrote:" in (proc.stdout or ""), "cold write")
        cold_text = (cold_book / "00.md").read_text(encoding="utf-8")
        check(classify(cold_text)[0] == "sentinel", "cold sentinel")
        check("NN99 is the end sentinel" in cold_text, "cold century rule")
        check("no decades" not in cold_text, "cold decade sentence")
        blocked = subprocess.run(
            [
                sys.executable, str(Path(__file__).resolve()), "write", str(cold_root / "12.other"),
                "--who", "grok-builder", "--keyword", "other", "--why", "No.",
            ],
            capture_output=True, text=True,
        )
        check(blocked.returncode != 0 and "solo book" in ((blocked.stdout or "") + (blocked.stderr or "")), "cold illegal stops")
        if (cold_root / "12.other" / "00.md").exists():
            die("test cold illegal wrote")
    print("test: pass")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        cmd_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "write":
        cmd_write(sys.argv[2:])
    else:
        die("use test or write")
