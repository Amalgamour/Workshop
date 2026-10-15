#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nav.py — walk a desk, a shelf, and a book from the 00.md door.

A missing 00.md means the container is not real.
A one-line door is a proof. A sentinel has three sections.
Pages 0010 through 0014 are how a book functions.
A missing one of those means the book is not finished.
This program does not mint a second law and does not edit either kernel.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, desk drill
# Folder shape follows the live tree: desk DD.title, shelf DD.SS.title, book DD.SS.BB.title.
# Law 0052 still says SS.title. Law 0054 still says BB.title. Those sentences stay.

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from desk import KERNEL_OWNER, live_fields, need, repo_root, solo_root
from door import SOLO, classify, in_solo, render_sentinel, write_door, write_furniture
from face import die, kind_of, make_new, parse_name, show_path
from menu import anchor, make_menu

FURNITURE = ("00.start", "00.about", "00.readme", "00.live")
FUNCTION = ("0010", "0011", "0012", "0013", "0014")
LINK_RE = re.compile(r"\(([^)#\s]+)#([^)]+)\)")
REPO = repo_root()
SOLO_ROOT = solo_root()


def find_file(folder: Path, stem: str) -> Path | None:
    for name in (f"{stem}.md", stem):
        path = folder / name
        if path.is_file():
            return path
    return None


def page_dir(book: Path, number: str) -> Path | None:
    if not book.is_dir():
        return None
    found = [
        path for path in book.iterdir()
        if path.is_dir() and path.name.startswith(number + ".")
    ]
    if len(found) > 1:
        die("one page slot is open")
    return found[0] if found else None


def face_file(page: Path, number: str = "01") -> Path | None:
    drafts = [
        path for path in page.glob(f"{number}.*.draft.md")
        if path.is_file() and re.fullmatch(rf"{number}\.\d{{3}}\.draft\.md", path.name)
    ]
    if len(drafts) > 1:
        die("one draft is open")
    if drafts:
        return drafts[0]
    seat = page / f"{number}.md"
    return seat if seat.is_file() else None


def heading_slugs(path: Path) -> set[str]:
    slugs = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            slugs.add(anchor(line[3:].strip()))
    return slugs


def resolve_book(desk: Path, raw: str) -> Path | None:
    raw = raw.strip().strip("`")
    path = Path(raw)
    if path.is_absolute() and path.is_dir():
        return path
    for base in (desk, REPO, Path.cwd()):
        cand = (base / raw).resolve()
        if cand.is_dir():
            return cand
    return None


def door_line(folder: Path, lines: list[str]) -> str:
    door = folder / "00.md"
    if not door.is_file():
        lines.append(f"finding {folder.name} 00.md is missing. the container is not real")
        return "missing"
    kind, detail = classify(door.read_text(encoding="utf-8"))
    if kind == "proof":
        parsed = parse_name(folder.name)
        title = parsed[1] if parsed else ""
        if detail != title:
            lines.append(f"finding {folder.name} proof line is {detail}")
        else:
            lines.append(f"ok {folder.name} proof {detail}")
        return kind
    if kind == "sentinel":
        lines.append(f"ok {folder.name} sentinel")
        return kind
    lines.append(f"finding {folder.name} door {detail}")
    return kind


def check_menu(page: Path, lines: list[str]) -> None:
    menu = face_file(page, "03")
    if menu is None:
        return
    for name, slug in LINK_RE.findall(menu.read_text(encoding="utf-8")):
        target = page / name
        if not target.is_file():
            lines.append(f"finding {page.name} menu link {name} is missing")
            continue
        if slug not in heading_slugs(target):
            lines.append(f"finding {page.name} menu anchor {slug} is missing")
            continue
        lines.append(f"ok {page.name} menu {name}#{slug}")


def walk_book(book: Path, lines: list[str], seen: set[Path]) -> None:
    key = book.resolve()
    if key in seen:
        return
    seen.add(key)
    kind = door_line(book, lines)
    if kind == "missing":
        return
    for number in FUNCTION:
        page = page_dir(book, number)
        if page is None:
            lines.append(f"finding {book.name} {number} is not here. the book is not finished")
            continue
        face = face_file(page)
        if face is None:
            lines.append(f"finding {page.name} face 01 is missing")
            continue
        lines.append(f"ok {page.name} {face.name}")
        check_menu(page, lines)


def walk_shelf(shelf: Path, lines: list[str], seen: set[Path]) -> None:
    door_line(shelf, lines)
    if not shelf.is_dir():
        return
    books = []
    for child in sorted(path for path in shelf.iterdir() if path.is_dir()):
        parsed = parse_name(child.name)
        if parsed and kind_of(parsed[0]) == "book":
            books.append(child)
    if not books:
        lines.append(f"finding {shelf.name} has no book. the shelf is not finished")
    for book in books:
        walk_book(book, lines, seen)


def walk_desk(desk: Path) -> list[str]:
    lines: list[str] = []
    seen: set[Path] = set()
    door_line(desk, lines)
    for stem in FURNITURE:
        found = find_file(desk, stem)
        if found is None:
            lines.append(f"finding {stem} is missing")
        else:
            lines.append(f"ok {found.name}")
    live = find_file(desk, "00.live")
    target = ""
    if live is not None:
        fields = live_fields(live.read_text(encoding="utf-8"))
        for key in ("book", "owner", "sitting"):
            if key not in fields:
                lines.append(f"finding 00.live has no {key}")
        if fields.get("owner") != KERNEL_OWNER:
            lines.append("finding 00.live owner is not the kernel address")
        target = fields.get("book", "")
    if not desk.is_dir():
        return lines
    for child in sorted(path for path in desk.iterdir() if path.is_dir()):
        parsed = parse_name(child.name)
        if not parsed:
            continue
        parts, _title = parsed
        kind = kind_of(parts)
        if kind == "shelf":
            if len(parts) >= 2 and parts[1] == "00":
                lines.append(f"finding {child.name} uses shelf number 00")
                continue
            walk_shelf(child, lines, seen)
        elif kind == "book":
            walk_book(child, lines, seen)
    if target:
        opened = resolve_book(desk, target)
        if opened is None:
            lines.append(f"finding 00.live book cannot be opened {target}")
        else:
            lines.append(f"ok live {show_path(opened)}")
            walk_book(opened, lines, seen)
    return lines


def walk_path(folder: Path) -> list[str]:
    parsed = parse_name(folder.name)
    if not parsed:
        die("folder is not a desk, a shelf, or a book")
    kind = kind_of(parsed[0])
    if kind == "desk":
        return walk_desk(folder)
    lines: list[str] = []
    seen: set[Path] = set()
    if kind == "shelf":
        walk_shelf(folder, lines, seen)
        return lines
    if kind == "book":
        walk_book(folder, lines, seen)
        return lines
    die("folder is not a desk, a shelf, or a book")


def findings(lines: list[str]) -> list[str]:
    return [line for line in lines if line.startswith("finding ")]


def furniture_text(title: str, why: str, body: str, who: str) -> str:
    from datetime import date
    from face import EM
    if not who.strip():
        die("who is required")
    return (
        f"# {title}\n\n"
        f"Authorization: draft {EM} {date.today().isoformat()}\n"
        f"who: {who}\n"
        "state: draft\n"
        f"why: {why}\n\n"
        f"{body.rstrip()}\n"
    )


def stand(who: str) -> Path:
    if not who.strip():
        die("who is required")
    drill = SOLO_ROOT / "drill"
    desk = drill / "10.trial"
    in_solo(drill if drill.exists() else SOLO_ROOT)
    if desk.exists():
        die("desk is already stood")
    shelf = desk / "10.10.shelf"
    book = shelf / "10.10.10.guide"
    book.mkdir(parents=True)
    pages = {
        "0010.about": (
            "How to read a page in this book.",
            "## How\n\nA page is a folder, PPPP.title.\n"
            "Face 01 binds. Face 03 is the menu. Face 04 is the person read.\n"
            "Open the face the job names. A missing face stays missing.\n\n"
            "## This book\n\nThis book is `10.10.10.guide`.\n"
            "It is the drill book on desk `10.trial`.\nIt is not law.\n",
            "## Job\n\nWhy: because a reader needs the short form.\n\n"
            "Body: Read face 01 section How, then section This book.\n"
            "This book is the drill. It is not law.\n",
        ),
        "0011.contents": (
            "The bands this book uses.",
            "## Bands\n\nAbout is `0010` through `0019`.\n"
            "This book uses `0010`, `0011`, and `0014`.\n"
            "`0012` and `0013` are absent. They stay absent.\n\n"
            "## Chain\n\nThe desk is `10.trial`. The shelf is `10.10.shelf`. This book is the child.\n",
            "## Job\n\nWhy: because the bands come after the book exists.\n\n"
            "Body: This book has three pages. The missing numbers stay missing.\n",
        ),
        "0014.design": (
            "Where the designs for this book are.",
            "## Design\n\nRead this page first.\n"
            "The designs for the 00 files are on the template, syntax page `0014`, face `01` and face `02`.\n"
            "This page points there. It does not copy them.\n",
            "## Job\n\nWhy: because the design already has a home.\n\n"
            "Body: Open the template page. Do not copy it into this book.\n",
        ),
    }
    for name, (why, face01, face04) in pages.items():
        page = book / name
        page.mkdir()
        make_new(page, "01", who, why, "2.8", face01)
        make_new(page, "04", who, why, "2.8", face04)
        make_menu(page, who)
    write_door(desk, render_sentinel(
        "trial",
        "Desk sentinel. Permission to exist.",
        ["desk: 10.trial"],
        [
            "`00` is the highest position on this desk. This file is that position.",
            "There is no shelf sentinel. Shelf number `00` does not exist.",
            "This drill does not mint a second law.",
        ],
        [
            "This file holds the permission for this desk to exist, where that authority comes from, and how this desk controls its space.",
            "The owner address is `00.00.00.kernel`. A sitting name is not this address.",
            "A book carries its own `00.md`. This file does not replace a book sentinel.",
            "This file is not the proof. The proof is `address.proof`.",
        ],
        [
            "Local: this file.",
            "Parent: book `10.10.11.solo-kernel`. This desk is a drill inside that book. It is not the workshop desk.",
            "Kernel: `00.00.00.kernel`. That is the owner address.",
            "Start is `00.start`. `00.live` names the law book.",
        ],
        [
            "`00.start`, `00.about`, `00.readme`, and `00.live` are furniture. They are not books.",
        ],
        who,
    ))
    write_furniture(desk, "00.start.md", furniture_text(
        "00.start",
        "The run for this desk.",
        "## Run\n\nOpen `00.about`. If unsure, open `00.readme`.\n"
        "The walk is template syntax page `0014`, face `01`, section Order.\n"
        "This file keeps that pointer. It does not copy the route.\n"
        "`00.live` names the law book. It is not a step.\n",
        who,
    ))
    write_furniture(desk, "00.about.md", furniture_text(
        "00.about",
        "Why this desk exists.",
        "## Why\n\nThis desk is a drill. Compute walks it from `00.md`.\n"
        "It is not the workshop desk. The workshop door stays one line.\n",
        who,
    ))
    write_furniture(desk, "00.readme.md", furniture_text(
        "00.readme",
        "How to find.",
        "## Find\n\nThe shelf is `10.10.shelf`. The book is `10.10.10.guide`.\n"
        "Open `0010`, then `0011`, then `0014`.\n"
        "The law book is the path in `00.live`.\n",
        who,
    ))
    write_furniture(desk, "00.live.md", furniture_text(
        "00.live",
        "Which law book this desk climbs. Desk only.",
        "book: 10.workshop/10.10.work/10.10.11.solo-kernel/sample/00.00.01.law\n"
        "owner: 00.00.00.kernel\n"
        "sitting: 10.workshop/10.10.work/10.10.11.solo-kernel/drill/10.trial\n",
        who,
    ))
    write_door(shelf, render_sentinel(
        "shelf",
        "Shelf sentinel. Permission to exist.",
        ["desk: 10.trial", "shelf: 10.10.shelf"],
        [
            "This file is the sentinel of shelf `10.10.shelf`.",
            "It is not shelf number `00`. Shelf number `00` does not exist.",
        ],
        [
            "This file is the permission for this shelf to exist.",
            "Books sit beside this file. A shelf with no book is not finished.",
        ],
        [
            "Local: this file.",
            "Parent: desk `10.trial`.",
            "This shelf is part of the drill. It is not a shelf of the workshop.",
        ],
        ["This file is not a book sentinel."],
        who,
    ))
    write_door(book, render_sentinel(
        "guide",
        "Book sentinel. What this is, the first page, and what this is not.",
        ["desk: 10.trial", "shelf: 10.10.shelf", "book: 10.10.10.guide"],
        [
            "This is the book sentinel of `10.10.10.guide`. It proves the book.",
            "The first page to open is `0010`, title about.",
            "This is not a page. This is not the desk walk. This is not the proof. The proof is address.proof.",
        ],
        [
            "This file is the permission for this book to exist.",
            "The parent shelf is `10.10.shelf`. The desk is `10.trial`.",
            "This book controls its pages. It does not control the desk.",
        ],
        [
            "Local: this file.",
            "Parent: shelf `10.10.shelf`, desk `10.trial`.",
            "Kernel: `00.00.00.kernel`. That is the owner address. This sitting is not that address.",
            "This book is not law.",
        ],
        [
            "This file is not the template sentinel.",
            "This file is not `00.start`. A book does not get a start file.",
        ],
        who,
    ))
    return desk


def patch_doors(who: str) -> list[str]:
    if not who.strip():
        die("who is required")
    jobs = [
        (
            SOLO_ROOT,
            "solo-kernel",
            "Book sentinel. What this is, the first page, and what this is not.",
            ["desk: 10.workshop", "shelf: 10.10.work", "book: 10.10.11.solo-kernel"],
            [
                "This is the book sentinel of `10.10.11.solo-kernel`. It proves the book.",
                "The first page to open is `0600`, title compute.",
                "This is not a page. This is not the desk walk. This is not the proof. The proof is address.proof.",
            ],
            [
                "This file is the permission for this book to exist.",
                "This book controls band `0600`, `sample/`, and `drill/`.",
                "The template is read. This file does not edit it.",
            ],
            [
                "Local: this file.",
                "Parent: shelf `10.10.work`. Desk `10.workshop`.",
                "Kernel: `00.00.00.kernel`. That is the owner address. This sitting is not that address.",
            ],
            [
                "This file is not the template sentinel.",
                "This file is not a promote. It is not a sign. It is not an approve.",
            ],
        ),
        (
            SOLO_ROOT / "sample" / "00.00.01.law",
            "law",
            "Book sentinel. What this is, the first page, and what this is not.",
            ["book: 00.00.01.law"],
            [
                "This is the book sentinel of `00.00.01.law`. It proves the book.",
                "The first page to open is `0000`, title invariant.",
                "This is not a page. This is not the desk walk. This is not the proof. The proof is address.proof.",
            ],
            [
                "This file is the permission for this sample to exist.",
                "These faces are drafts. A draft does not govern.",
            ],
            [
                "The template sentinel stays at `00.00.00.kernel.draft/00.00.01.law/00.md`.",
                "This copy is not that file.",
                "Kernel: `00.00.00.kernel`. That is the owner address.",
            ],
            ["This file is not the template sentinel."],
        ),
        (
            SOLO_ROOT / "sample" / "00.00.00.syntax",
            "syntax",
            "Book sentinel. What this is, the first page, and what this is not.",
            ["book: 00.00.00.syntax"],
            [
                "This is the book sentinel of `00.00.00.syntax`. It proves the book.",
                "The first page to open is `0000`, title invariant.",
                "This is not a page. This is not the desk walk. This is not the proof. The proof is address.proof.",
            ],
            [
                "This file is the permission for this sample to exist.",
                "This sample holds one drafted face. It is not a finished book.",
            ],
            [
                "The template sentinel stays at `00.00.00.kernel.draft/00.00.00.syntax/00.md`.",
                "This copy is not that file.",
                "Kernel: `00.00.00.kernel`. That is the owner address.",
            ],
            ["This file is not the template sentinel."],
        ),
    ]
    written = []
    for folder, keyword, why, rows, sentinel, permission, authority, not_this in jobs:
        text = render_sentinel(keyword, why, rows, sentinel, permission, authority, not_this, who)
        write_door(folder, text, replace=True)
        written.append(show_path(folder / "00.md"))
    return written


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "10.workshop" / "10.10.work" / SOLO / "drill"
        desk = root / "10.trial"
        shelf = desk / "10.10.shelf"
        book = shelf / "10.10.10.guide"
        page = book / "0010.about"
        page.mkdir(parents=True)
        (book / "0011.contents").mkdir()
        (book / "0012.dictionary").mkdir()
        (book / "0013.concordance").mkdir()
        (book / "0014.design").mkdir()
        for folder, title in (
            (page, "about"),
            (book / "0011.contents", "contents"),
            (book / "0012.dictionary", "dictionary"),
            (book / "0013.concordance", "concordance"),
            (book / "0014.design", "design"),
        ):
            (folder / "01.md").write_text(f"# 01\n\n## Job\n\n{title}.\n", encoding="utf-8")
        (page / "03.md").write_text(
            "# 03\n\n## Job\n\nMenu: [01 — Job](01.md#job).\n\n## Missing\n\nMenu: [01 — Missing](01.md#missing).\n",
            encoding="utf-8",
        )
        (desk / "00.md").write_text("trial\n", encoding="utf-8")
        for stem in FURNITURE:
            name = stem + ".md"
            (desk / name).write_text(
                "book: 10.10.shelf/10.10.10.guide\nowner: 00.00.00.kernel\nsitting: 10.trial\n",
                encoding="utf-8",
            )
        (shelf / "00.md").write_text("shelf\n", encoding="utf-8")
        (book / "00.md").write_text("# 00\n\n## Sentinel\n\n", encoding="utf-8")
        broken = findings(walk_desk(desk))
        check(any("door missing Permission" in line for line in broken), "broken book door")
        check(any("menu anchor missing" in line for line in broken), "bad anchor")
        (book / "00.md").write_text(
            "# 00\n\n## Sentinel\n\n## Permission\n\n## Authority\n",
            encoding="utf-8",
        )
        (page / "03.md").write_text("# 03\n\n## Job\n\nMenu: [01 — Job](01.md#job).\n", encoding="utf-8")
        clean = walk_desk(desk)
        check(not findings(clean), "clean walk " + "; ".join(findings(clean)))
        check(any("ok live" in line for line in clean), "live book")
        check(any("0010.about 01.md" in line for line in clean), "page 0010")
        bare = Path(tmp) / "10.workshop" / "10.10.work" / SOLO / "bare"
        bare.mkdir(parents=True)
        (bare / "12.plain").mkdir()
        (bare / "12.plain" / "00.md").write_text("plain\n", encoding="utf-8")
        # proof title must match the folder title
        proof_lines = walk_path(bare / "12.plain")
        check(any(line.startswith("ok 12.plain proof plain") for line in proof_lines), "proof desk")
    print("test: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, walk PATH, stand, or patch")
    if args[0] == "test":
        cmd_test()
        return
    if args[0] == "walk":
        if len(args) < 2:
            die("walk PATH")
        lines = walk_path(Path(args[1]))
        print("\n".join(lines))
        if findings(lines):
            sys.exit(1)
        return
    if args[0] == "stand":
        if "--who" not in args:
            die("stand --who TEXT")
        desk = stand(need(args, "--who"))
        lines = walk_desk(desk)
        print("\n".join(lines))
        if findings(lines):
            sys.exit(1)
        print(f"stood: {show_path(desk)}")
        return
    if args[0] == "patch":
        if "--who" not in args:
            die("patch --who TEXT")
        for path in patch_doors(need(args, "--who")):
            print(f"patched: {path}")
        return
    die("use test, walk PATH, stand, or patch")


if __name__ == "__main__":
    main()
