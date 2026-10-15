#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""face.py — create one face draft.

The template is 00.00.00.kernel.draft. This program reads it.
It writes FF.VVV.draft.md in the destination page.
Every stored face has a header and a stamp.
Face 03 is that header and the menu lines. It does not need a heading.
A large menu divided into sections is a later job.
Another face needs a heading. The heading is the lookup.
It does not open face 06. It does not sign, approve, or promote.
It does not write either kernel.
"""
# ## notes
# born: 2026-10-13
# source: director, >go
# who: grok-prime
# The useful part of clerk.py is the stamp, the source hash, and the draft name.
# The part that does not work is copying face 06 onto the draft. This program does not do that.

from __future__ import annotations

import hashlib
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

from desk import CHECK_KERNEL, DRAFT_KERNEL, need, repo_root, solo_root

EM = "\u2014"
NAME_RE = re.compile(r"^((?:\d{2}\.)*\d{2,4})\.(.+)$")
HEADING_RE = re.compile(r"(?m)^## .*$")
TRAILER_RE = re.compile(r"(?m)^### notes[ \t]*$")
VERSION_RE = re.compile(r"(?m)^version:[ \t]*(\d+)[ \t]*$")
WHO_RE = re.compile(r"(?m)^who:[ \t]*(.*)$")
WHY_RE = re.compile(r"(?m)^why:[ \t]*(.*)$")
CITE_RE = re.compile(r"(?m)^cite:[ \t]*(.*)$")
FIELD_KEYS = (
    "version", "Authorization", "state", "Face", "PPPP",
    "desk", "shelf", "book", "keyword", "why", "cite", "who",
)
FIELD_SPLIT_RE = re.compile(
    " (?=(?:" + "|".join(FIELD_KEYS) + "):)"
)


def die(msg: str) -> None:
    sys.exit(f"stop: {msg}")


def parse_name(name: str):
    hit = NAME_RE.fullmatch(name)
    if not hit:
        return None
    parts = hit.group(1).split(".")
    return parts, hit.group(2)


def kind_of(parts: list[str]) -> str:
    if len(parts) == 3 and all(len(p) == 2 for p in parts):
        return "book"
    if len(parts) == 2 and all(len(p) == 2 for p in parts):
        return "shelf"
    if len(parts) == 1 and len(parts[0]) == 2:
        return "desk"
    if len(parts) == 1 and len(parts[0]) == 4:
        return "page"
    return ""


def refuse_kernel_write(path: Path) -> None:
    names = [parent.name for parent in (path.resolve(), *path.resolve().parents)]
    if CHECK_KERNEL in names or DRAFT_KERNEL in names:
        die("the template kernel is not edited")


def page_rows(page: Path) -> tuple[str, str, list[str]]:
    parsed = parse_name(page.name)
    if not parsed or kind_of(parsed[0]) != "page":
        die("folder is not a page")
    number, keyword = parsed[0][0], parsed[1]
    book_dir = page.parent
    book = parse_name(book_dir.name)
    if not book or kind_of(book[0]) != "book":
        die("page has no book folder")
    found = []
    cursor = book_dir.parent
    for _ in range(2):
        got = parse_name(cursor.name)
        if not got:
            break
        kind = kind_of(got[0])
        if kind not in ("shelf", "desk"):
            break
        found.append((kind, cursor.name))
        cursor = cursor.parent
    rows = []
    for key in ("desk", "shelf", "book"):
        if key == "book":
            rows.append(f"book: {book_dir.name}")
            continue
        for kind, name in found:
            if kind == key:
                rows.append(f"{key}: {name}")
    return number, keyword, rows


def normalize(raw: bytes) -> str:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def header_field(text: str, pattern: re.Pattern) -> str:
    hit = pattern.search(text)
    return hit.group(1).strip() if hit else ""


def is_field(part: str) -> bool:
    return any(part.startswith(f"{key}:") for key in FIELD_KEYS)


def unmash_header(text: str) -> str:
    """Split a one-line header before the first section. The body stays one block."""
    starts = list(HEADING_RE.finditer(text))
    end = starts[0].start() if starts else len(text)
    header, rest = text[:end], text[end:]
    out = []
    for line in header.split("\n"):
        if not is_field(line):
            out.append(line)
            continue
        parts = FIELD_SPLIT_RE.split(line)
        if len(parts) > 1 and all(is_field(part) for part in parts):
            out.extend(parts)
        else:
            out.append(line)
    return "\n".join(out) + rest


def split_document(text: str):
    trailer = ""
    hit = TRAILER_RE.search(text)
    if hit:
        trailer = text[hit.start():]
        text = text[: hit.start()]
    starts = list(HEADING_RE.finditer(text))
    if not starts:
        return text, [], trailer
    header = text[: starts[0].start()]
    sections = []
    for i, mark in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[mark.start():end]
        sections.append(block.strip("\n") + "\n\n")
    return header, sections, trailer


def open_draft(page: Path, number: str) -> Path | None:
    found = [
        path for path in page.glob(f"{number}.*.draft.md")
        if path.is_file() and re.fullmatch(rf"{number}\.\d{{3}}\.draft\.md", path.name)
    ]
    if len(found) > 1:
        die("one draft is open")
    return found[0] if found else None


def next_version(text: str) -> str:
    hit = VERSION_RE.search(text)
    nxt = int(hit.group(1)) + 1 if hit else 1
    if nxt > 999:
        die("version is past 999")
    return f"{nxt:03d}"


def show_path(path: Path) -> str:
    resolved = path.resolve()
    for cand in (resolved, *resolved.parents):
        if (cand / "10.workshop").is_dir() and (cand / DRAFT_KERNEL).is_dir():
            try:
                return resolved.relative_to(cand).as_posix()
            except ValueError:
                break
    return resolved.as_posix()


def header_text(
    face_no: str,
    page_no: str,
    keyword: str,
    rows: list[str],
    version: str,
    who: str,
    why: str,
    cite: str,
    source: list[str] | None,
) -> str:
    lines = [f"# {face_no}", "", f"version: {version}"]
    if source:
        lines.extend(source)
    lines.extend([
        f"Authorization: draft {EM} {date.today().isoformat()}",
        f"who: {who}",
        "state: draft",
        f"Face: {face_no}",
        f"PPPP: {page_no}",
        *rows,
        f"keyword: {keyword}",
        f"why: {why}",
        "",
        f"cite: {cite}",
        "",
    ])
    return "\n".join(lines) + "\n"


def write_draft(page: Path, face_no: str, version: str, text: str) -> Path:
    refuse_kernel_write(page)
    if not page.is_dir():
        die("page folder is missing")
    if open_draft(page, face_no):
        die("one draft is open")
    dest = page / f"{face_no}.{version}.draft.md"
    if dest.exists():
        die("one draft is open")
    dest.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
    return dest


def make_new(page: Path, face_no: str, who: str, why: str, cite: str, body: str) -> Path:
    if not re.fullmatch(r"\d{2}", face_no) or not ("01" <= face_no <= "08"):
        die("face is 01 through 08")
    seat = page / f"{face_no}.md"
    if seat.exists():
        die("a seat is here. use draft")
    page_no, keyword, rows = page_rows(page)
    if not body.strip():
        die("body is empty")
    text = header_text(face_no, page_no, keyword, rows, "001", who, why, cite, None)
    if face_no == "03":
        # A small menu has no heading. Dividing a large menu is a later job.
        if HEADING_RE.search(body):
            die("a heading does not belong on the menu")
        text += body.strip() + "\n"
        return write_draft(page, face_no, "001", text)
    _header, sections, trailer = split_document(body if body.lstrip().startswith("## ") else "\n" + body)
    if not sections:
        die("body needs a heading")
    text += "".join(sections)
    if trailer.strip():
        text += trailer if trailer.endswith("\n") else trailer + "\n"
    return write_draft(page, face_no, "001", text)


def make_draft(page: Path, source: Path, who: str) -> Path:
    if not source.is_file():
        die("template face is missing")
    seat_name = re.fullmatch(r"(\d{2})\.md", source.name)
    if not seat_name:
        die("template face is FF.md")
    face_no = seat_name.group(1)
    raw = source.read_bytes()
    text = unmash_header(normalize(raw))
    page_no, keyword, rows = page_rows(page)
    version = next_version(text)
    source_lines = [
        f"source path: {show_path(source)}",
        f"source version: {header_field(text, VERSION_RE) or 'none'}",
        f"source hash: {sha256(raw)}",
    ]
    _header, sections, trailer = split_document(text)
    if not sections:
        die("template face has no section")
    kept_who = header_field(text, WHO_RE) or who
    drafted = header_text(
        face_no,
        page_no,
        keyword,
        rows,
        version,
        kept_who,
        header_field(text, WHY_RE),
        header_field(text, CITE_RE),
        source_lines,
    )
    drafted += "".join(sections)
    if trailer.strip():
        drafted += trailer if trailer.endswith("\n") else trailer + "\n"
    return write_draft(page, face_no, version, drafted)


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source_page = root / DRAFT_KERNEL / "00.00.01.law" / "0000.invariant"
        source_page.mkdir(parents=True)
        seat = source_page / "01.md"
        seat_bytes = (
            "# 01\r\n\r\n"
            "version: 003\r\n"
            "Authorization: approved \u2014 2026-10-11\r\n"
            "who: grok-prime\r\n"
            "state: approved\r\n"
            "Face: 01\r\n"
            "PPPP: 0000\r\n"
            "book: 00.00.01.law\r\n"
            "keyword: invariant\r\n"
            "why: Template.\r\n"
            "cite: 7.8\r\n\r\n"
            "## Read\r\n\r\n"
            "The seat body.\r\n"
        ).encode("utf-8")
        seat.write_bytes(seat_bytes)
        (source_page / "06.md").write_bytes(
            b"# 06\n\n## Note\n\nborn: 2026-09-26\nUNIQUE face 06 note stays off the draft.\n"
        )
        book = root / "10.workshop" / "10.10.work" / "10.10.11.solo-kernel"
        page = book / "0601.face"
        page.mkdir(parents=True)
        made = make_draft(page, seat, "grok-prime")
        check(made.name == "01.004.draft.md", "draft name")
        check(seat.read_bytes() == seat_bytes, "template unchanged")
        drafted = made.read_text(encoding="utf-8")
        check("The seat body." in drafted, "seat section copied")
        check("UNIQUE face 06 note" not in drafted, "face 06 stayed off")
        check(f"source hash: {sha256(seat_bytes)}" in drafted, "source hash")
        check("source version: 003" in drafted, "source version")
        check("book: 10.10.11.solo-kernel" in drafted, "dest book")
        check("shelf: 10.10.work" in drafted, "dest shelf")
        check("state: draft" in drafted, "state draft")
        check("\n\n## Read\n" in drafted, "blank line before the body")
        check("state: approved" not in drafted, "approved stays off")
        check(b"\r" not in made.read_bytes(), "lf write")
        try:
            make_draft(page, seat, "grok-prime")
            die("test opened a second draft")
        except SystemExit as exc:
            check("one draft is open" in str(exc), "second draft stops")
        blocked = root / DRAFT_KERNEL / "00.00.01.law" / "0001.law"
        blocked.mkdir()
        try:
            make_draft(blocked, seat, "grok-prime")
            die("test wrote the template")
        except SystemExit as exc:
            check("template kernel is not edited" in str(exc), "kernel write stops")
        fresh = book / "0609.trial"
        fresh.mkdir()
        made_new = make_new(
            fresh,
            "01",
            "grok-prime",
            "A new face.",
            "2.8",
            "## Job\n\nMade here.\n",
        )
        check(made_new.name == "01.001.draft.md", "new name")
        new_text = made_new.read_text(encoding="utf-8")
        check("PPPP: 0609" in new_text and "keyword: trial" in new_text, "new address")
        check("## Job" in new_text and "source path:" not in new_text, "new has no source")
        menu_page = book / "0604.menu"
        menu_page.mkdir()
        made_menu = make_new(
            menu_page,
            "03",
            "grok-prime",
            "The job of the menu. A selection does not permit.",
            "3.5",
            "Menu: [01 — Job](01.md#job).\n",
        )
        menu_text = made_menu.read_text(encoding="utf-8")
        check(made_menu.name == "03.001.draft.md", "menu name")
        check(menu_text.startswith("# 03\n"), "menu header")
        check("Authorization: draft" in menu_text and "state: draft" in menu_text, "menu stamp")
        check("cite: 3.5" in menu_text, "menu cite")
        check("Menu: [01 — Job](01.md#job)." in menu_text, "menu section")
        check("\n## " not in menu_text, "menu has no heading")
        check(b"\r" not in made_menu.read_bytes(), "menu lf")
        plain = book / "0605.plain"
        plain.mkdir()
        try:
            make_new(plain, "01", "grok-prime", "A new face.", "2.8", "Just prose.\n")
            die("test stored a section face with no heading")
        except SystemExit as exc:
            check("body needs a heading" in str(exc), "section face needs a heading")
        try:
            make_new(
                plain,
                "03",
                "grok-prime",
                "The job of the menu. A selection does not permit.",
                "3.5",
                "## Sections\n\nMenu: [01 — Job](01.md#job).\n",
            )
            die("test stored a heading on the menu")
        except SystemExit as exc:
            check("a heading does not belong on the menu" in str(exc), "menu heading stops")
        mashed_home = root / DRAFT_KERNEL / "00.00.01.law" / "0060.drafting"
        mashed_home.mkdir()
        mashed = mashed_home / "01.md"
        mashed_bytes = (
            "# 01\n\n"
            "version: 003 Authorization: approved \u2014 2026-10-08 "
            "state: approved Face: 01 PPPP: 0060 book: 00.00.01.law "
            "keyword: drafting why: The order a draft is made. Not from memory.\n"
            "\n## Order\n\nOpen current faces first.\n"
        ).encode("utf-8")
        mashed.write_bytes(mashed_bytes)
        mash_page = book / "0608.mash"
        mash_page.mkdir()
        made_mash = make_draft(mash_page, mashed, "grok-prime")
        mash_text = made_mash.read_text(encoding="utf-8")
        check(made_mash.name == "01.004.draft.md", "mashed version")
        check("why: The order a draft is made. Not from memory." in mash_text, "mashed why")
        check("\nversion: 004\n" in mash_text, "mashed next version")
        check("source version: 003" in mash_text, "mashed source version")
        check(f"source hash: {sha256(mashed_bytes)}" in mash_text, "mashed hash")
        check(mashed.read_bytes() == mashed_bytes, "mashed template unchanged")
        check("state: approved" not in mash_text, "mashed approved stays off")
    sample = solo_root() / "sample"
    report = check_hashes(sample, repo_root())
    misses = [line for line in report if not line.startswith("match:")]
    check(not misses, "hash " + "; ".join(misses))
    check(report[-1] == "match: 52", "hash count " + report[-1])
    print("test: pass")


def check_hashes(sample: Path, repo: Path) -> list[str]:
    """Compare each stored source hash with the template file. This writes nothing."""
    path_re = re.compile(r"(?m)^source path:[ \t]*(.+?)[ \t]*$")
    hash_re = re.compile(r"(?m)^source hash:[ \t]*([0-9a-f]{64})[ \t]*$")
    lines = []
    matched = 0
    for draft in sorted(sample.rglob("*.draft.md")):
        text = draft.read_text(encoding="utf-8")
        path_hit = path_re.search(text)
        hash_hit = hash_re.search(text)
        if path_hit is None and hash_hit is None:
            continue
        if path_hit is None or hash_hit is None:
            lines.append(f"missing stamp {draft.relative_to(sample).as_posix()}")
            continue
        source = repo / path_hit.group(1).strip()
        if not source.is_file():
            lines.append(f"missing file {path_hit.group(1).strip()}")
            continue
        if sha256(source.read_bytes()) != hash_hit.group(1):
            lines.append(f"mismatch {draft.relative_to(sample).as_posix()}")
            continue
        matched += 1
    lines.append(f"match: {matched}")
    return lines


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use new, draft, hashes, or test")
    cmd = args[0]
    if cmd == "test":
        cmd_test()
        return
    if cmd == "hashes":
        for line in check_hashes(solo_root() / "sample", repo_root()):
            print(line)
        return
    if cmd == "new":
        if len(args) < 9 or "--who" not in args or "--why" not in args or "--cite" not in args or "--body-file" not in args:
            die("new PAGE FF --who TEXT --why TEXT --cite TEXT --body-file PATH")
        page = Path(args[1])
        face_no = args[2]
        who = need(args, "--who")
        why = args[args.index("--why") + 1]
        cite = args[args.index("--cite") + 1]
        body = Path(args[args.index("--body-file") + 1]).read_text(encoding="utf-8")
        made = make_new(page, face_no, who, why, cite, body)
        print(f"draft: {made.name}")
        return
    if cmd == "draft":
        if "--from" not in args or "--who" not in args:
            die("draft PAGE --from SOURCE --who TEXT")
        page = Path(args[1])
        source = Path(args[args.index("--from") + 1])
        who = need(args, "--who")
        made = make_draft(page, source, who)
        print(f"draft: {made.name}")
        return
    die("use new, draft, hashes, or test")


if __name__ == "__main__":
    main()
