#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""page.py — make one page folder in the lowest open slot.

Law 0055. A page is PPPP.title. Face 01 binds.
The slot comes from slot.py. stand takes the number it is given.
stand writes face 01 and face 08 on the draft law book.
It does not write the check kernel, 00.kernel, or the sample copy.
A 04NN page waits until 01NN, 02NN, 03NN, and 05NN are clear.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, law band 0000-0100
# who: grok-prime
# born: 2026-10-21
# source: director, >run.0514.05.02, and 0414.test-desk/06.02.md
# who: grok-builder
# stand takes a book, a number, and a keyword.
# The number is given. slot.py next is not used.
# It writes face 01 and face 08.
# An existing folder with no 01.md and no 08.md receives the faces.
# A face already there stops. An illegal path stops.
# born: 2026-10-22
# source: director, >run.0514.05.10, and 0114.test-desk/05.01.return.md #11
# who: grok-builder
# The make test looks for 01.md. Version 001 is 01.md.
# born: 2026-10-22
# source: director, >run.0513.05.16, and 0113.law-align/05.14.return.md #05
# who: grok-builder
# stand writes face 01 and face 08 on the draft law book.
# The check kernel and 00.kernel stay closed.
# The sample copy stays closed.
# write_draft still refuses both kernels, so stand writes those two faces.
# born: 2026-10-24
# source: director, >run.0517.05.01, and 0417.pack-lint/01.md
# who: grok-builder
# A 04NN page waits until 01NN, 02NN, 03NN, and 05NN are clear.
# The stop names the taken number and the title. No folder is written.
# Previous hash d20d265303f4ef7cca6b3244cb3be665a0e95fcd13f23b49441903898bdf0b75.
# page.py has no seated copy, so no older file was kept.

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from desk import CHECK_KERNEL, DRAFT_KERNEL, need
from face import (
    die,
    face_filename,
    header_text,
    kind_of,
    make_new,
    open_draft,
    page_rows,
    parse_name,
    refuse_kernel_write,
    split_document,
)
from slot import next_member, next_open, taken_names

KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.-]*$")
COPY_BOOKS = {"00.00.01.law", "00.00.00.syntax"}


def refuse_copy(book: Path) -> None:
    refuse_kernel_write(book)
    if book.name in COPY_BOOKS:
        die("a page is not minted in this book")


def path_names(path: Path) -> list[str]:
    return [parent.name for parent in (path.resolve(), *path.resolve().parents)]


def refuse_stand(book: Path) -> None:
    """Stand may write the draft law book. The check kernel and 00.kernel stay closed."""
    names = path_names(book)
    if "00.kernel" in names:
        die("the kernel is not edited")
    if CHECK_KERNEL in names:
        die("the template kernel is not edited")
    if DRAFT_KERNEL in names:
        if book.name == "00.00.01.law":
            return
        die("the template kernel is not edited")
    if book.name in COPY_BOOKS:
        die("a page is not minted in this book")


DECISION_BANDS = ("01", "02", "03", "05")


def clear_for_decision(book: Path, number: str) -> None:
    """A 04NN page waits until 01NN, 02NN, 03NN, and 05NN are clear."""
    if len(number) != 4 or not number.startswith("04"):
        return
    tail = number[2:]
    taken = []
    for child in sorted(book.iterdir()):
        if not child.is_dir():
            continue
        parsed = parse_name(child.name)
        if not parsed:
            continue
        parts, title = parsed
        if kind_of(parts) != "page":
            continue
        num = parts[0]
        if num[:2] in DECISION_BANDS and num[2:] == tail:
            taken.append(f"{num} is taken by {title}")
    if taken:
        die("; ".join(taken))


def place_page(book: Path, number: str, keyword: str, who: str, why: str, cite: str, body: str) -> Path:
    refuse_copy(book)
    if not re.fullmatch(r"\d{4}", number):
        die("page number is four digits")
    if not KEY_RE.fullmatch(keyword):
        die("title needs a word")
    if not book.is_dir():
        die("book folder is missing")
    page = book / f"{number}.{keyword}"
    if page.exists():
        die("slot is taken")
    clear_for_decision(book, number)
    page.mkdir()
    try:
        make_new(page, "01", who, why, cite, body)
    except SystemExit:
        if page.is_dir() and not any(page.iterdir()):
            page.rmdir()
        raise
    return page


def write_stood(page: Path, face_no: str, version: str, text: str) -> Path:
    """Write one stood face. refuse_stand has already allowed this book."""
    if not page.is_dir():
        die("page folder is missing")
    if open_draft(page, face_no):
        die("one draft is open")
    dest = page / face_filename(face_no, version)
    if dest.exists():
        die("one draft is open")
    dest.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
    return dest


def stand_face(page: Path, face_no: str, who: str, why: str, cite: str, body: str) -> Path:
    """Faces 01 and 08. make_new is not used. write_draft refuses the draft kernel."""
    if face_no not in ("01", "08"):
        die("stand writes face 01 and face 08")
    if open_draft(page, face_no):
        die("one draft is open")
    seat = page / f"{face_no}.md"
    if seat.exists():
        die("a seat is here. use draft")
    page_no, keyword, rows = page_rows(page)
    if not body.strip():
        die("body is empty")
    text = header_text(face_no, page_no, keyword, rows, "001", who, why, cite, None)
    _header, sections, trailer = split_document(
        body if body.lstrip().startswith("## ") else "\n" + body
    )
    if not sections:
        die("body needs a heading")
    text += "".join(sections)
    if trailer.strip():
        text += trailer if trailer.endswith("\n") else trailer + "\n"
    return write_stood(page, face_no, "001", text)


def stand_page(
    book: Path,
    number: str,
    keyword: str,
    who: str,
    why: str,
    cite: str,
    body: str,
    custody: str,
) -> Path:
    """Open PPPP.keyword and write face 01 and face 08. The number is given."""
    refuse_stand(book)
    if not re.fullmatch(r"\d{4}", number):
        die("page number is four digits")
    if not KEY_RE.fullmatch(keyword):
        die("title needs a word")
    if not book.is_dir():
        die("book folder is missing")
    book_name = parse_name(book.name)
    if not book_name or kind_of(book_name[0]) != "book":
        die("page has no book folder")
    clear_for_decision(book, number)
    page = book / f"{number}.{keyword}"
    for child in book.iterdir():
        if child.is_dir() and child.name.startswith(number + ".") and child != page:
            die("number is taken")
    if page.exists() and not page.is_dir():
        die("page path is not a folder")
    if page.is_dir() and ((page / "01.md").exists() or (page / "08.md").exists()):
        die("a face is already here")
    created = not page.exists()
    if created:
        page.mkdir()
    try:
        stand_face(page, "01", who, why, cite, body)
        stand_face(page, "08", who, why, cite, custody)
    except SystemExit:
        for name in ("01.md", "08.md"):
            made = page / name
            if made.is_file():
                made.unlink()
        if created and page.is_dir() and not any(page.iterdir()):
            page.rmdir()
        raise
    return page


def make_open(book: Path, start: int, keyword: str, who: str, why: str, cite: str, body: str) -> Path:
    slot = next_open(start, taken_names(book))
    return place_page(book, slot, keyword, who, why, cite, body)


def make_page(book: Path, door: int, keyword: str, who: str, why: str, cite: str, body: str) -> Path:
    refuse_copy(book)
    if not book.is_dir():
        die("book folder is missing")
    if not KEY_RE.fullmatch(keyword):
        die("title needs a word")
    slot = next_member(door, taken_names(book))
    clear_for_decision(book, slot)
    page = book / f"{slot}.{keyword}"
    if page.exists():
        die("slot is taken")
    page.mkdir()
    try:
        make_new(page, "01", who, why, cite, body)
    except SystemExit:
        if page.is_dir() and not any(page.iterdir()):
            page.rmdir()
        raise
    return page


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def check_stand() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / "10.10.99.trial"
        book.mkdir(parents=True)
        (book / "0109.open").mkdir()
        held = book / "0114.held"
        held.mkdir()
        (held / "05.01.return.md").write_bytes(b"# 05.01\n")
        made = stand_page(
            book, "0114", "held", "grok-builder", "A return.", "3.1",
            "## Job\n\nThe return page.\n",
            "## Relationships\n\nparent: 0100.band.returns\n",
        )
        check(made.name == "0114.held", "named number")
        check(not (book / "0115.held").exists(), "no next slot")
        check((made / "01.md").is_file() and (made / "08.md").is_file(), "faces 01 and 08")
        check((made / "05.01.return.md").is_file(), "return file stays")
        text = (made / "01.md").read_text(encoding="utf-8")
        check("PPPP: 0114" in text and "state: draft" in text, "face 01 stamp")
        check("## Relationships" in (made / "08.md").read_text(encoding="utf-8"), "face 08 body")
        try:
            stand_page(
                book, "0114", "held", "grok-builder", "A return.", "3.1",
                "## Job\n\nAgain.\n",
                "## Relationships\n\nparent: 0100.band.returns\n",
            )
            die("test wrote over a face")
        except SystemExit as exc:
            check("a face is already here" in str(exc), "second stand stops")
        blocked = root / "00.00.00.kernel.draft" / "00.00.99.law"
        blocked.mkdir(parents=True)
        try:
            stand_page(
                blocked, "0114", "nope", "grok-builder", "A return.", "3.1",
                "## Job\n\nNo.\n",
                "## Relationships\n\nparent: none\n",
            )
            die("test wrote in the kernel")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel path stops")
            check(not (blocked / "0114.nope").exists(), "no kernel folder")
        law = root / DRAFT_KERNEL / "00.00.01.law"
        law.mkdir(parents=True)
        stood = stand_page(
            law, "1000", "work", "grok-builder",
            "1000 work: normal working pages. open", "3.1",
            "## Job\n\n1000 work: normal working pages. open\n",
            "## Relationships\n\n1000 work: normal working pages. open\n",
        )
        check(stood.name == "1000.work", "draft law door")
        check((stood / "01.md").is_file() and (stood / "08.md").is_file(), "draft law faces")
        check_law = root / CHECK_KERNEL / "00.00.01.law"
        check_law.mkdir(parents=True)
        try:
            stand_page(
                check_law, "1000", "work", "grok-builder",
                "1000 work: normal working pages. open", "3.1",
                "## Job\n\nNo.\n",
                "## Relationships\n\nNo.\n",
            )
            die("test wrote in the check kernel")
        except SystemExit as exc:
            check("template kernel" in str(exc), "check kernel stops")
            check(not (check_law / "1000.work").exists(), "check kernel folder absent")
        bare = root / "00.kernel" / "00.00.01.law"
        bare.mkdir(parents=True)
        try:
            stand_page(
                bare, "1000", "work", "grok-builder",
                "1000 work: normal working pages. open", "3.1",
                "## Job\n\nNo.\n",
                "## Relationships\n\nNo.\n",
            )
            die("test wrote in 00.kernel")
        except SystemExit as excl:
            check("the kernel is not edited" in str(excl), "00.kernel stops")
            check(not (bare / "1000.work").exists(), "00.kernel folder absent")
        sample = root / "sample" / "00.00.01.law"
        sample.mkdir(parents=True)
        try:
            stand_page(
                sample, "1000", "work", "grok-builder",
                "1000 work: normal working pages. open", "3.1",
                "## Job\n\nNo.\n",
                "## Relationships\n\nNo.\n",
            )
            die("test minted in the law copy")
        except SystemExit as exc:
            check("not minted" in str(exc), "stand law copy stays")
            check(not (sample / "1000.work").exists(), "stand copy folder absent")
        (book / "0116.words").mkdir()
        (book / "0516.pack-lint").mkdir()
        try:
            stand_page(
                book, "0416", "probe", "grok-builder", "A decision.", "3.1",
                "## Job\n\nNo.\n",
                "## Relationships\n\nparent: none\n",
            )
            die("test opened a taken decision")
        except SystemExit as exc:
            shown = str(exc)
            check("0116 is taken by words" in shown, "clear-check names the return")
            check("0516 is taken by pack-lint" in shown, "clear-check names the pack")
            check(not (book / "0416.probe").exists(), "taken decision writes nothing")
        opened = stand_page(
            book, "0499", "open", "grok-builder", "A decision.", "3.1",
            "## Job\n\nYes.\n",
            "## Relationships\n\nparent: none\n",
        )
        check(opened.name == "0499.open", "clear decision stands")
        back = stand_page(
            book, "0199", "back", "grok-builder", "A return.", "3.1",
            "## Job\n\nYes.\n",
            "## Relationships\n\nparent: 0100.band.returns\n",
        )
        check(back.name == "0199.back", "return stands beside a decision")
        gate = root / "10.workshop" / "10.10.work" / "10.10.99.gate"
        gate.mkdir()
        (gate / "0101.returns").mkdir()
        try:
            make_page(gate, 400, "lint", "grok-prime", "A page.", "2.8", "## Job\n\nNo.\n")
            die("test made a taken decision")
        except SystemExit as exc:
            check("0101 is taken by returns" in str(exc), "make waits on the return")
            check(not (gate / "0401.lint").exists(), "make writes nothing")


def cmd_test() -> None:
    check_stand()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / "10.10.99.trial"
        book.mkdir(parents=True)
        (book / "0010.about").mkdir()
        (book / "0011.contents").mkdir()
        (book / "0016.old.09").mkdir()
        made = make_page(book, 10, "trial", "grok-prime", "A page.", "2.8", "## Job\n\nMade here.\n")
        check(made.name == "0012.trial", "lowest slot")
        check((made / "01.md").is_file(), "face 01 binds")
        text = (made / "01.md").read_text(encoding="utf-8")
        check("PPPP: 0012" in text and "keyword: trial" in text, "page address")
        check("state: draft" in text, "state draft")
        second = make_page(book, 10, "next", "grok-prime", "A page.", "2.8", "## Job\n\nNext.\n")
        check(second.name == "0013.next", "next slot")
        try:
            make_page(book, 21, "nope", "grok-prime", "A page.", "2.8", "## Job\n\nNo.\n")
            die("test accepted a door")
        except SystemExit as exc:
            check("door ends in 0" in str(exc), "door stops")
        copy = root / "10.workshop" / "10.10.work" / "10.10.11.solo-kernel" / "sample" / "00.00.01.law"
        copy.mkdir(parents=True)
        (copy / "0010.about").mkdir()
        try:
            make_page(copy, 10, "mint", "grok-prime", "A page.", "2.8", "## Job\n\nNo.\n")
            die("test minted in the law copy")
        except SystemExit as exc:
            check("not minted" in str(exc), "law copy stays")
            check(not (copy / "0011.mint").exists(), "no folder left behind")
        work = root / "10.workshop" / "10.10.work" / "10.10.99.open"
        work.mkdir()
        for number in range(1001, 1010):
            (work / f"{number:04d}.item").mkdir()
        try:
            make_page(work, 1000, "more", "grok-prime", "A page.", "2.8", "## Job\n\nNo.\n")
            die("test found a slot in a full decade")
        except SystemExit as exc:
            check("no slot" in str(exc), "full decade stops")
        opened = make_open(work, 1001, "more", "grok-prime", "A page.", "2.8", "## Job\n\nYes.\n")
        check(opened.name == "1010.more", "open band passes the decade")
    print("test: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, make BOOK DOOR KEYWORD, or stand BOOK NUMBER KEYWORD")
    if args[0] == "test":
        cmd_test()
        return
    if args[0] == "make":
        if len(args) < 10 or "--who" not in args or "--why" not in args or "--cite" not in args or "--body-file" not in args:
            die("make BOOK DOOR KEYWORD --who TEXT --why TEXT --cite TEXT --body-file PATH")
        who = need(args, "--who")
        body = Path(args[args.index("--body-file") + 1]).read_text(encoding="utf-8")
        made = make_page(
            Path(args[1]),
            int(args[2]),
            args[3],
            who,
            args[args.index("--why") + 1],
            args[args.index("--cite") + 1],
            body,
        )
        print(f"page: {made.name}")
        return
    if args[0] == "stand":
        need_flags = ("--who", "--why", "--cite", "--body-file", "--custody-file")
        if len(args) < 14 or any(flag not in args for flag in need_flags):
            die("stand BOOK NUMBER KEYWORD --who TEXT --why TEXT --cite TEXT --body-file PATH --custody-file PATH")
        who = need(args, "--who")
        body = Path(args[args.index("--body-file") + 1]).read_text(encoding="utf-8")
        custody = Path(args[args.index("--custody-file") + 1]).read_text(encoding="utf-8")
        made = stand_page(
            Path(args[1]),
            args[2],
            args[3],
            who,
            args[args.index("--why") + 1],
            args[args.index("--cite") + 1],
            body,
            custody,
        )
        print(f"stood: {made.name}")
        print("faces: 01.md 08.md")
        return
    die("use test, make BOOK DOOR KEYWORD, or stand BOOK NUMBER KEYWORD")


if __name__ == "__main__":
    main()
