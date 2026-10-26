#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 009
# Authorization: draft — 2026-10-24
# who: grok-builder
# state: draft
# Face: 02
# PPPP: 0305
# desk: 10.workshop
# shelf: 10.10.work
# book: 10.10.12.rebuild
# keyword: clerk
# why: Retire an order bullet without writing it back at column 0. Revise accepts 00.md.
#
# cite: 3.1
# source path: 10.workshop/10.10.work/10.10.10.lib/code/clerk.py
# source hash: 0ee0b8045a96db7afa6eff2b626cf824d133f67a091671f5ef52388e95272419
# kept: 02.clerk.009.py is the previous module.
"""clerk.py — place a section on a face.

jobs.py places batches. This places face pieces.
It does not sign, approve, or promote.

Now: stamp, drop, draft, derive, revise, versions, import, seat, live, and lint.
Dev mode writes kernel.draft. The check kernel stays closed.
Later, in this same program: cite, and the gate.
Clerk mode reads 00.00.00.kernel and does not write a face.

A seated face is FF.md. Version 001 is also FF.md. A later draft is FF.VVV.md.
A .draft tail stops. FF.001.md stops. Empty version counts as 001.
draft copies the seat, applies the notes on 06, and leaves the seat unchanged.
versions lists every FF.VVV.md, marks the highest version, and stops for a name.
import writes the named version as the seated FF.md and keeps the source block.
It does not choose the highest by itself. It does not copy face 06.
It reads CRLF and writes LF. It stores one source block.
seat writes a bare version 001 face as the seated FF.md and keeps the source block.
The check kernel and 00.kernel stop. The draft law book is the seat.
live writes 00.live on the draft law book.
The file has four lines: last, when, goal, pages. It overwrites. A model write stops.
lint reads one 05.NN file and reports pass or fail with the reason.
It does not write the pack or rename a file.
On pass it writes a short note and a promote request. On fail it writes the reason.
It does not mark the pack ready and it does not run promote.
FF.VVV.md stays on import. Face 06 stays off.
derive reads ## Relationships on that draft.
A missing relationship is reported and no file is written.
A seated 08.md is reported and no file is written.
A built face is 08.md at version 001, or 08.VVV.md after that.
It keeps the seat identity and the draft identity.
It does not write over a seated 08.md. It does not sign.
"""
# ## notes
# born: 2026-10-13
# source: director, >run.05.04
# who: grok-prime
# #02 draft reads CRLF and writes LF. The source hash is the original bytes.
# #03 and #11 one source block. A second write replaces that block.
# #04 the draft address comes from the folder it is written in. The source path stays.
# #05 drop and revise refuse a signed draft. #06 the clerk still does not sign.
# #09 every note is copied. The model merges the body.
# #10 revise replaces one exact sentence and records the old sentence.
# #12 draft can read a seat in one book and write the draft in another page.
# #14 a seated 08.md is named and left. #07 a missing relationship stays missing.
# #17 the built face keeps the seat hash and the draft hash as two identities.
# #18 a copied Relationships section is marked extract. why and cite stay empty.
# #19 seating, approval, and the stale check were not run.
# #20 the preserve check is the test: same text, version plus one, notes kept, source hash unchanged.
# #21 the kernel checker does not validate these drafts.
# Director 2026-10-13: a draft file is FF.VVV.draft.md until the faces are a database.
# The .md can come off later. The seated face stays FF.md.
# Director 2026-10-17: the .draft tail is off. Version 001 is FF.md. A later draft is FF.VVV.md.
# An empty version counts as 001. The next file is one higher. The seat gains no version line.
# A clean rewrite of this file can come later. Keep this note until those facts move with it.
# born: 2026-10-20
# source: director, >run.0513.05.04, and 0413.law-align/06.04.md
# who: grok-builder
# versions lists FF.VVV.md, marks the highest, and stops. The model names the stronger face.
# import writes that named version as seated FF.md with the source block. Face 06 stays off.
# born: 2026-10-22
# source: director, >run.0514.05.13, and 0114.test-desk/05.12.return.md
# who: grok-builder
# revise accepts 00.start.md and 00.readme.md. A random name still stops.
# born: 2026-10-22
# source: director, >run.0513.05.12, and 0113.law-align/05.11.return.md #05
# who: grok-builder
# seat writes a bare version 001 face and keeps the source block.
# The check kernel and 00.kernel stop. The draft law book is the seat.
# born: 2026-10-23
# source: director, >run.0513.05.19, and 0113.law-align/05.18.return.md #06
# who: grok-builder
# revise accepts 00.order.md. A random name still stops.
# born: 2026-10-23
# source: director, >run.0513.05.20, and 0413.law-align/06.12.md
# who: grok-builder
# live writes 00.live with last, when, goal, and pages. It overwrites. A model write stops.
# born: 2026-10-24
# source: director, >run.0517.05.02, and 0417.pack-lint/01.md
# who: grok-builder
# lint reads one 05.NN file and reports pass or fail. It does not write the pack.
# born: 2026-10-24
# source: director, >run.0517.05.03, and 0417.pack-lint/06.02.md
# who: grok-builder
# On a lint pass, write a note and a promote request. On fail, write the reason.
# The pack file stays. Lint does not mark it ready and does not run promote.
# born: 2026-10-24
# source: director, >run.0518.05.01
# who: grok-builder
# An order bullet retired with new text retired: NAME replaces every column-0 copy.
# The note records retired: NAME and does not write the bullet back at column 0.
# revise accepts 00.md. A random name still stops.

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

EM = "\u2014"
NAME_RE = re.compile(r"^((?:\d{2}\.)*\d{2,4})\.(.+)$")
CHECK_KERNEL = "00.00.00.kernel"
DRAFT_KERNEL = "00.00.00.kernel.draft"
HEADING_RE = re.compile(r"(?m)^## .*$")
TRAILER_RE = re.compile(r"(?m)^### notes[ \t]*$")
VERSION_RE = re.compile(r"(?m)^version:[ \t]*(\d+)[ \t]*$")
VERSION_ANY_RE = re.compile(r"(?m)^version:[ \t]*(.*)$")
AUTH_RE = re.compile(r"(?m)^Authorization:[ \t]*.*$")
STATE_RE = re.compile(r"(?m)^state:[ \t]*(\S+)[ \t]*$")
IDENTITY_LINE = re.compile(
    r"^(?:source path|source version|source hash|seat path|seat version|seat hash|"
    r"draft path|draft version|draft hash|extract|source):[ \t]*"
)


def die(msg: str) -> None:
    sys.exit(f"stop: {msg}")


def clerk_mode() -> str:
    mode = os.environ.get("CLERK_MODE", "dev")
    if mode not in ("dev", "clerk"):
        die("mode is dev or clerk")
    return mode


def kernel_root(repo: Path) -> Path:
    if clerk_mode() == "dev":
        return repo / DRAFT_KERNEL
    return repo / CHECK_KERNEL


def guarded(path: Path, *, write: bool = True) -> None:
    names = [parent.name for parent in (path.resolve(), *path.resolve().parents)]
    in_check = CHECK_KERNEL in names
    in_draft = DRAFT_KERNEL in names
    if clerk_mode() == "dev":
        if in_check:
            die("dev mode writes kernel.draft. the check kernel is closed")
        return
    if write:
        die("clerk mode reads the kernel. it does not write a face")
    if in_draft:
        die("clerk mode reads the kernel, not the draft")


def closed_kernel(path: Path) -> None:
    """00.kernel stays closed. The draft law book is a different folder."""
    names = [parent.name for parent in (path.resolve(), *path.resolve().parents)]
    if "00.kernel" in names:
        die("the kernel is not edited")


def parse_name(name: str):
    hit = NAME_RE.fullmatch(name)
    if not hit:
        return None
    address, title = hit.group(1), hit.group(2)
    parts = address.split(".")
    return parts, title


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


def face_filename(face_no: str, version: str) -> str:
    """Version 001 is FF.md. A later version is FF.VVV.md."""
    if version == "001":
        return f"{face_no}.md"
    return f"{face_no}.{version}.md"


def face_ref(face: Path):
    if ".draft" in face.name:
        die("a draft is FF.VVV.md")
    bare = re.fullmatch(r"(\d{2})\.md", face.name)
    if bare:
        number = bare.group(1)
        if face.is_file() and face_state(read_face(face)) == "draft":
            return "draft", number, "001"
        return "seat", number, None
    numbered = re.fullmatch(r"(\d{2})\.(\d{3})\.md", face.name)
    if numbered:
        if numbered.group(2) == "001":
            die("version 001 is FF.md")
        return "draft", numbered.group(1), numbered.group(2)
    die("face file is FF.md or FF.VVV.md")


def page_rows(face: Path):
    page = parse_name(face.parent.name)
    if not page or kind_of(page[0]) != "page":
        die("folder is not a page")
    number, keyword = page[0][0], page[1]
    book_dir = face.parent.parent
    book = parse_name(book_dir.name)
    if not book or kind_of(book[0]) != "book":
        die("page has no book folder")
    rows = []
    cursor = book_dir.parent
    found = []
    for _ in range(2):
        parsed = parse_name(cursor.name)
        if not parsed:
            break
        kind = kind_of(parsed[0])
        if kind not in ("shelf", "desk"):
            break
        found.append((kind, cursor.name))
        cursor = cursor.parent
    for key in ("desk", "shelf"):
        for kind, name in found:
            if kind == key:
                rows.append(f"{key}: {name}")
    rows.append(f"book: {book_dir.name}")
    # Desk, shelf, book. A level that is not there is left out.
    ordered = []
    for key in ("desk", "shelf", "book"):
        for line in rows:
            if line.startswith(key + ":"):
                ordered.append(line)
    return number, keyword, ordered


def identity(face: Path):
    face_ref(face)
    return page_rows(face)


def stamp(face: Path, who: str) -> str:
    _kind, face_no, _ver = face_ref(face)
    number, keyword, rows = page_rows(face)
    day = date.today().isoformat()
    lines = [
        f"# {face_no}",
        "",
        f"Authorization: draft {EM} {day}",
        f"who: {who}",
        "state: draft",
        f"Face: {face_no}",
        f"PPPP: {number}",
        *rows,
        f"keyword: {keyword}",
        "why:",
        "",
        "cite:",
        "",
    ]
    return "\n".join(lines) + "\n"


def face_state(text: str) -> str:
    hit = STATE_RE.search(text)
    return hit.group(1) if hit else ""


def insert_after_title(text: str, line: str) -> str:
    if not text.startswith("# "):
        return line + "\n\n" + text
    nl = text.find("\n")
    if nl < 0:
        return text + "\n\n" + line + "\n"
    rest = text[nl + 1:]
    if rest.startswith("\n"):
        return text[: nl + 1] + "\n" + line + "\n" + rest[1:]
    return text[: nl + 1] + "\n" + line + "\n" + rest


def insert_after(text: str, pattern: re.Pattern, line: str) -> str:
    hit = pattern.search(text)
    if not hit:
        return insert_after_title(text, line)
    return text[: hit.end()] + "\n" + line + text[hit.end():]


def next_version(text: str) -> str:
    """A missing or empty version counts as 001. The next number is one higher."""
    loose = VERSION_ANY_RE.search(text)
    plain = VERSION_RE.search(text)
    if loose and not plain and loose.group(1).strip() != "":
        die("version line is not a number")
    current = int(plain.group(1)) if plain else 1
    nxt = current + 1
    if nxt > 999:
        die("version is past 999")
    return f"{nxt:03d}"


def retarget(text: str, version: str) -> str:
    day = date.today().isoformat()
    auth = f"Authorization: draft {EM} {day}"
    if VERSION_RE.search(text):
        text = VERSION_RE.sub(f"version: {version}", text, count=1)
    else:
        text = insert_after_title(text, f"version: {version}")
    if AUTH_RE.search(text):
        text = AUTH_RE.sub(auth, text, count=1)
    else:
        text = insert_after_title(text, auth)
    if STATE_RE.search(text):
        text = STATE_RE.sub("state: draft", text, count=1)
    else:
        text = insert_after(text, AUTH_RE, "state: draft")
    return text


def repo_root() -> Path | None:
    here = Path(__file__).resolve()
    for cand in (here.parent, *here.parents):
        if (cand / "10.workshop").is_dir() and (cand / DRAFT_KERNEL).is_dir():
            return cand
    return None


def show_path(path: Path) -> str:
    resolved = path.resolve()
    root = repo_root()
    if root is not None:
        try:
            return resolved.relative_to(root).as_posix()
        except ValueError:
            pass
    return resolved.as_posix()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalize(raw: bytes) -> str:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n").decode("utf-8")


def header_field(text: str, key: str) -> str:
    hit = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*)$", text)
    return hit.group(1).strip() if hit else ""


def numbered_version(text: str) -> str:
    plain = VERSION_RE.search(text)
    if not plain:
        return ""
    return f"{int(plain.group(1)):03d}"


def restamp_address(text: str, face: Path) -> str:
    number, keyword, rows = page_rows(face)
    header, sections, trailer = split_document(text)
    kept = []
    for line in header.splitlines(keepends=True):
        if re.match(r"^(?:desk|shelf|book|PPPP|keyword):[ \t]*", line):
            continue
        kept.append(line)
    header = "".join(kept)
    block = "\n".join([f"PPPP: {number}", *rows, f"keyword: {keyword}"])
    if re.search(r"(?m)^Face:[ \t]*", header):
        header = re.sub(r"(?m)^(Face:[ \t]*.*)$", rf"\1\n{block}", header, count=1)
    elif re.search(r"(?m)^why:", header):
        header = re.sub(r"(?m)^why:", block + "\nwhy:", header, count=1)
    else:
        header = header.rstrip("\n") + "\n" + block + "\n"
    return join_document(header, sections, trailer)


def strip_identity(header: str) -> str:
    kept = []
    for line in header.splitlines(keepends=True):
        if IDENTITY_LINE.match(line):
            continue
        kept.append(line)
    return "".join(kept)


def insert_source_block(text: str, lines: list[str]) -> str:
    header, sections, trailer = split_document(text)
    header = strip_identity(header)
    block = "\n".join(lines)
    if VERSION_RE.search(header):
        header = VERSION_RE.sub(lambda hit: hit.group(0) + "\n" + block, header, count=1)
    elif AUTH_RE.search(header):
        header = AUTH_RE.sub(lambda hit: block + "\n" + hit.group(0), header, count=1)
    else:
        header = insert_after_title(header, block)
    return join_document(header, sections, trailer)


def source_lines(seat: Path, raw: bytes, text: str) -> list[str]:
    lines = [f"source path: {show_path(seat)}"]
    version = numbered_version(text)
    if version:
        lines.append(f"source version: {version}")
    lines.append(f"source hash: {sha256(raw)}")
    return lines


def open_named(folder: Path, number: str) -> list[Path]:
    found = []
    if not folder.is_dir():
        return found
    for path in folder.iterdir():
        if not path.is_file():
            continue
        if re.fullmatch(rf"{number}\.\d{{3}}\.draft\.md", path.name):
            die("a draft is FF.VVV.md")
        numbered = re.fullmatch(rf"{number}\.(\d{{3}})\.md", path.name)
        if numbered:
            if numbered.group(1) == "001":
                die("version 001 is FF.md")
            found.append(path)
            continue
        if path.name == f"{number}.md" and face_state(read_face(path)) == "draft":
            found.append(path)
    return sorted(found)


def apply_notes(text: str, notes_face: Path) -> tuple[str, str]:
    if not notes_face.is_file():
        return text, "none"
    raw = read_face(notes_face)
    _header, src_sections, src_trailer = split_document(raw)
    pieces = [block for name, block in src_sections if is_history(name)]
    if src_trailer.strip():
        pieces.append(src_trailer)
    if not pieces:
        return text, "none"
    header, sections, trailer = split_document(text)
    added = 0
    for block in pieces:
        current = join_document(header, sections, trailer)
        if block.strip() in current:
            continue
        if block.lstrip().startswith("### notes"):
            extra = block.strip("\n") + "\n"
            trailer = (trailer.rstrip("\n") + "\n\n" + extra) if trailer.strip() else extra
        else:
            first = block.split("\n", 1)[0]
            name = first[3:].strip() if first.startswith("## ") else "Note"
            sections.append((name, block.strip("\n") + "\n\n"))
        added += 1
    if added == 0:
        return text, "none"
    return join_document(header, sections, trailer), str(added)


def make_draft(seat: Path, who: str, dest_dir: Path | None = None) -> tuple[Path, str]:
    guarded(seat)
    kind, number, _ver = face_ref(seat)
    if kind != "seat":
        die("draft starts from the seated face")
    if not seat.is_file():
        die("seated face is missing")
    folder = seat.parent if dest_dir is None else dest_dir
    if dest_dir is not None:
        guarded(folder)
        if not folder.is_dir():
            die("page folder is missing")
        page_rows(folder / f"{number}.md")
    if open_named(folder, number):
        die("one draft is open")
    raw = seat.read_bytes()
    text = normalize(raw)
    version = next_version(text)
    dest = folder / face_filename(number, version)
    if dest.exists():
        die("one draft is open")
    copied = insert_source_block(
        restamp_address(retarget(text, version), dest),
        source_lines(seat, raw, text),
    )
    copied, notes = apply_notes(copied, seat.parent / "06.md")
    copied = copied.replace("\r\n", "\n").replace("\r", "\n")
    dest.write_bytes(copied.encode("utf-8"))
    return dest, notes


VERSIONED_RE = re.compile(r"^(0[1-8])\.(\d{3})\.md$")


def require_page(page: Path) -> None:
    if not page.is_dir():
        die("page folder is missing")
    parsed = parse_name(page.name)
    if not parsed or kind_of(parsed[0]) != "page":
        die("folder is not a page")


def versioned_faces(page: Path) -> list[tuple[str, str, Path]]:
    require_page(page)
    found = []
    for path in page.iterdir():
        if not path.is_file():
            continue
        hit = VERSIONED_RE.fullmatch(path.name)
        if not hit:
            continue
        if hit.group(2) == "001":
            die("version 001 is FF.md")
        found.append((hit.group(1), hit.group(2), path))
    return sorted(found, key=lambda row: (row[0], row[1]))


def cmd_versions(page: Path) -> None:
    rows = versioned_faces(page)
    print(f"page: {page.name}")
    if not rows:
        print("versions: none")
        print("writes: no")
        sys.exit("stop: no versioned face")
    highest: dict[str, str] = {}
    for face, ver, _path in rows:
        if face not in highest or ver > highest[face]:
            highest[face] = ver
    for _face, ver, path in rows:
        mark = " highest" if ver == highest[path.name[:2]] else ""
        print(f"{path.name}{mark}")
    print("writes: no")
    sys.exit("stop: name the stronger face")


def make_import(page: Path, source: Path, who: str) -> Path:
    guarded(page)
    guarded(source)
    require_page(page)
    if not source.is_file():
        die("named face is missing")
    kind, number, ver = face_ref(source)
    if kind != "draft" or not ver or ver == "001":
        die("import starts from the named version")
    page_rows(page / f"{number}.md")
    dest = page / f"{number}.md"
    if dest.exists():
        die("a seat is here")
    if open_named(page, number):
        die("one draft is open")
    raw = source.read_bytes()
    text = normalize(raw)
    copied = insert_source_block(
        restamp_address(retarget(text, "001"), dest),
        source_lines(source, raw, text),
    )
    if re.search(r"(?m)^who:[ \t]*", copied):
        copied = re.sub(r"(?m)^who:[ \t]*.*$", f"who: {who}", copied, count=1)
    else:
        copied = insert_after(copied, STATE_RE, f"who: {who}")
    copied = copied.replace("\r\n", "\n").replace("\r", "\n")
    dest.write_bytes(copied.encode("utf-8"))
    return dest


def cmd_import(page: Path, source: Path, who: str) -> None:
    dest = make_import(page, source, who)
    print(f"seat: {dest.name}")
    print(f"source: {source.name}")
    print("writes: yes")


def make_seat(page: Path, source: Path, who: str) -> Path:
    guarded(page)
    guarded(source)
    closed_kernel(page)
    closed_kernel(source)
    if not source.is_file():
        die("named face is missing")
    kind, number, ver = face_ref(source)
    if kind != "draft" or ver != "001":
        die("import starts from the named version")
    if number == "06":
        die("face 06 stays off")
    raw = source.read_bytes()
    text = normalize(raw)
    if numbered_version(text) not in ("", "001"):
        die("import starts from the named version")
    created = False
    if page.is_dir():
        require_page(page)
    else:
        if page.exists():
            die("folder is not a page")
        parent = page.parent
        if not parent.is_dir():
            die("book folder is missing")
        parsed = parse_name(page.name)
        if not parsed or kind_of(parsed[0]) != "page":
            die("folder is not a page")
        book = parse_name(parent.name)
        if not book or kind_of(book[0]) != "book":
            die("page has no book folder")
        if page.name != source.parent.name:
            die("page name does not match the source")
        page.mkdir()
        created = True
    dest = page / f"{number}.md"
    try:
        page_rows(dest)
        if dest.exists():
            die("a seat is here")
        if open_named(page, number):
            die("one draft is open")
        copied = insert_source_block(
            restamp_address(retarget(text, "001"), dest),
            source_lines(source, raw, text),
        )
        if re.search(r"(?m)^who:[ \t]*", copied):
            copied = re.sub(r"(?m)^who:[ \t]*.*$", f"who: {who}", copied, count=1)
        else:
            copied = insert_after(copied, STATE_RE, f"who: {who}")
        copied = copied.replace("\r\n", "\n").replace("\r", "\n")
        dest.write_bytes(copied.encode("utf-8"))
    except BaseException as exc:
        if created:
            if not isinstance(exc, SystemExit) and dest.is_file():
                dest.unlink()
            try:
                page.rmdir()
            except OSError:
                pass
        raise
    return dest


def cmd_seat(page: Path, source: Path, who: str) -> None:
    dest = make_seat(page, source, who)
    print(f"seat: {dest.name}")
    print(f"source: {source.name}")
    print("writes: yes")


def section_body(block: str) -> str:
    parts = block.split("\n", 1)
    return parts[1].strip() if len(parts) > 1 else ""


def built_header(draft: Path, who: str, version: str, extra: list[str]) -> str:
    page_no, keyword, rows = page_rows(draft)
    day = date.today().isoformat()
    lines = [
        "# 08",
        "",
        f"version: {version}",
        f"Authorization: draft {EM} {day}",
        f"who: {who}",
        "state: built",
        "Face: 08",
        f"PPPP: {page_no}",
        *rows,
        f"keyword: {keyword}",
        "why:",
        "",
        "cite:",
        "",
        *extra,
        "",
    ]
    return "\n".join(lines) + "\n"


def identity_lines(draft: Path, text: str, number: str, version: str) -> list[str]:
    lines = []
    seat_path = header_field(text, "source path")
    seat_version = header_field(text, "source version")
    seat_hash = header_field(text, "source hash")
    if not seat_path:
        seat = draft.parent / f"{number}.md"
        if seat.is_file():
            raw = seat.read_bytes()
            seat_path = show_path(seat)
            seat_hash = sha256(raw)
            seat_version = numbered_version(normalize(raw))
    if seat_path:
        lines.append(f"seat path: {seat_path}")
    if seat_version:
        lines.append(f"seat version: {seat_version}")
    if seat_hash:
        lines.append(f"seat hash: {seat_hash}")
    raw_draft = draft.read_bytes()
    lines.extend([
        f"draft path: {show_path(draft)}",
        f"draft version: {version}",
        f"draft hash: {sha256(raw_draft)}",
        "extract: Relationships",
    ])
    return lines


def make_derived(draft: Path, who: str) -> tuple[str, str]:
    guarded(draft)
    kind, number, version = face_ref(draft)
    if kind != "draft":
        die("derive reads a draft")
    if number == "08":
        die("08 is the built face")
    if not draft.is_file():
        die("draft is missing")
    seated = draft.parent / "08.md"
    if seated.is_file():
        return "seated", seated.name
    if open_named(draft.parent, "08"):
        die("one built draft is open")
    text = read_face(draft)
    _header, sections, _trailer = split_document(text)
    found = [block for name, block in sections if name == "Relationships"]
    if len(found) > 1:
        die("heading is there twice")
    if not found or not section_body(found[0]):
        return "missing", ""
    extra = identity_lines(draft, text, number, version)
    dest = draft.parent / face_filename("08", version)
    body = found[0].strip("\n") + "\n"
    written = insert_source_block(built_header(draft, who, version, []) + "\n" + body, extra)
    dest.write_bytes(written.encode("utf-8"))
    return "built", dest.name


def is_history(heading: str) -> bool:
    return heading == "Note" or heading.startswith("Note ")


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
        first = block.split("\n", 1)[0]
        sections.append((first[3:].strip(), block))
    return header, sections, trailer


def render_section(heading: str, body: str) -> str:
    body = body.replace("\r\n", "\n").strip("\n")
    if body:
        return f"## {heading}\n\n{body}\n\n"
    return f"## {heading}\n\n"


def join_document(header: str, sections, trailer: str) -> str:
    if header and not header.endswith("\n"):
        header += "\n"
    body = header + "".join(block for _, block in sections) + trailer
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def read_face(path: Path) -> str:
    if not path.exists():
        return ""
    return normalize(path.read_bytes())


def refuse_settled(text: str, kind: str) -> None:
    state = face_state(text)
    if kind == "seat" and state != "draft":
        die("the seat stays. make a draft")
    if state == "signed":
        die("a signed draft stays")
    if state == "built":
        die("a built face stays")


def drop(face: Path, heading: str, body: str, who: str) -> str:
    guarded(face)
    if face.name == "00.live":
        die("a model does not write 00.live")
    kind, _number, _ver = face_ref(face)
    heading = " ".join(heading.split())
    if not heading:
        die("heading is empty")
    if "\n" in heading or heading.startswith("#"):
        die("heading is the words, not a markdown line")
    if is_history(heading):
        die("a note is history")
    if not face.parent.is_dir():
        die("page folder is missing")
    existing = read_face(face)
    if kind == "draft" and not existing:
        die("a draft is a copy of the seat")
    if existing:
        refuse_settled(existing, kind)
    if existing:
        header, sections, trailer = split_document(existing)
    else:
        header, sections, trailer = stamp(face, who), [], ""
    hits = [i for i, (name, _) in enumerate(sections) if name == heading]
    if len(hits) > 1:
        die("heading is there twice")
    block = render_section(heading, body)
    if hits:
        sections[hits[0]] = (heading, block)
        action = "replaced"
    else:
        at = next((i for i, (name, _) in enumerate(sections) if is_history(name)), len(sections))
        sections.insert(at, (heading, block))
        action = "added"
    face.write_bytes(join_document(header, sections, trailer).encode("utf-8"))
    return action


# These desk names only. A random name still stops in face_ref.
REVISE_DESK = frozenset({"00.start.md", "00.readme.md", "00.order.md", "00.md"})
ORDER_BULLET_RE = re.compile(r"^- (\d{4}\.[\w.\-]+)$")


def revise(face: Path, old: str, new: str, who: str) -> str:
    guarded(face)
    if face.name == "00.live":
        die("a model does not write 00.live")
    if face.name in REVISE_DESK:
        kind = "draft"
    else:
        kind, _number, _ver = face_ref(face)
    if old == "":
        die("sentence is empty")
    if not face.is_file():
        die("face is missing")
    existing = read_face(face)
    if kind == "draft" and not existing:
        die("a draft is a copy of the seat")
    refuse_settled(existing, kind)
    bullet = ORDER_BULLET_RE.fullmatch(old.strip("\r\n"))
    retiring = (
        face.name == "00.order.md"
        and bullet is not None
        and new.strip().startswith("retired:")
    )
    if retiring:
        if re.search(r"(?m)^- (\d{4}\.[\w.\-]+)", new):
            die("retired text is still a bullet")
        token = bullet.group(1)
        repl = new.strip()
        lines = existing.split("\n")
        hits = 0
        out_lines = []
        for line in lines:
            if line.strip() == old.strip("\r\n"):
                out_lines.append(repl)
                hits += 1
            else:
                out_lines.append(line)
        if hits == 0:
            die("sentence is missing")
        text = "\n".join(out_lines)
        if re.search(rf"(?m)^- {re.escape(token)}\b", text):
            die("retired line came back")
        recorded = f"retired: {token}"
    else:
        count = existing.count(old)
        if count == 0:
            die("sentence is missing")
        if count > 1:
            die("sentence is there twice")
        text = existing.replace(old, new, 1)
        recorded = old.rstrip()
    day = date.today().isoformat()
    note = (
        f"## Note — revise {day}\n\n"
        f"born: {day}\n"
        f"source: {who}\n\n"
        f"{recorded}\n"
    )
    header, sections, trailer = split_document(text)
    sections.append((f"Note — revise {day}", note + "\n"))
    document = join_document(header, sections, trailer)
    if retiring and re.search(rf"(?m)^- {re.escape(token)}\b", document):
        die("retired line came back")
    face.write_bytes(document.encode("utf-8"))
    return "revised"


LIVE_KEYS = ("last", "when", "goal", "pages")


def live_path(book: Path) -> Path:
    if book.name == "00.live":
        book = book.parent
    guarded(book)
    closed_kernel(book)
    names = [book.name, *(parent.name for parent in book.parents)]
    if book.name != "00.00.01.law" or DRAFT_KERNEL not in names:
        die("00.live is written on the draft law book")
    if not book.is_dir():
        die("law book is missing")
    return book / "00.live"


def live_lines(last: str, when: str, goal: str, pages: str) -> str:
    fields = {"last": last, "when": when, "goal": goal, "pages": pages}
    for key in LIVE_KEYS:
        value = fields[key].strip()
        if value == "":
            die(f"{key} is empty")
        if "\n" in fields[key] or "\r" in fields[key]:
            die(f"{key} is one line")
        fields[key] = value
    return "".join(f"{key}: {fields[key]}\n" for key in LIVE_KEYS)


def write_live(book: Path, last: str, when: str, goal: str, pages: str) -> str:
    dest = live_path(book)
    text = live_lines(last, when, goal, pages)
    dest.write_bytes(text.encode("utf-8"))
    return text


def read_live(book: Path) -> str:
    dest = live_path(book)
    if not dest.is_file():
        die("00.live is missing")
    raw = dest.read_bytes()
    if b"\r" in raw:
        die("00.live is not LF")
    text = raw.decode("utf-8")
    lines = text.splitlines()
    if len(lines) != 4:
        die("00.live needs four lines")
    for key, line in zip(LIVE_KEYS, lines):
        prefix = f"{key}: "
        if not line.startswith(prefix) or line[len(prefix):].strip() == "":
            die("00.live needs four lines")
    if not text.endswith("\n"):
        text += "\n"
    return text


def cmd_live(
    book: Path,
    last: str | None,
    when: str | None,
    goal: str | None,
    pages: str | None,
) -> None:
    given = (last, when, goal, pages)
    if all(value is None for value in given):
        sys.stdout.write(read_live(book))
        return
    if any(value is None for value in given):
        die("00.live needs last, when, goal, and pages")
    sys.stdout.write(write_live(book, last or "", when or "", goal or "", pages or ""))


def cmd_draft(seat: Path, who: str, source: Path | None = None) -> None:
    if source is None:
        dest, notes = make_draft(seat, who)
    else:
        folder = seat if seat.is_dir() else seat.parent
        if not folder.is_dir():
            die("page folder is missing")
        dest, notes = make_draft(source, who, folder)
    print(f"draft: {dest.name}")
    print(f"notes: {notes}")


def cmd_derive(draft: Path, who: str) -> None:
    result, name = make_derived(draft, who)
    if result == "missing":
        print("missing: Relationships")
        print("writes: no")
        sys.exit(2)
    if result == "seated":
        print(f"seated: {name}")
        print("writes: no")
        sys.exit(2)
    print(f"built: {name}")


def cmd_revise(face: Path, old: str, new: str, who: str) -> None:
    action = revise(face, old, new, who)
    print(f"{action}: {face}")


def cmd_drop(face: Path, heading: str, body_file: Path, who: str) -> None:
    raw = body_file.read_bytes()
    if b"\r" in raw:
        die("body file is not LF")
    text = raw.decode("utf-8")
    if text.lstrip().startswith("## "):
        die("the heading belongs in --heading")
    action = drop(face, heading, text, who)
    print(f"{action}: {face} ## {heading}")


LINT_BATCH_RE = re.compile(r"05\.(\d{2})(?:\.(draft|pack|open|replied|closed))?\.md")
LINT_PAGE_RE = re.compile(r"\b(\d{4}\.[A-Za-z][A-Za-z0-9.-]*)\b")
LINT_FOLDER_RE = re.compile(r"^(\d{2})(\d{2})\.(.+)$")


def lint_page_index(pack_file: Path) -> dict[str, Path]:
    """Page folders a name may live on. A sample folder counts. This does not write."""
    found: dict[str, Path] = {}

    def add(folder: Path) -> None:
        if not folder.is_dir():
            return
        try:
            children = list(folder.iterdir())
        except OSError:
            return
        for child in children:
            if not child.is_dir():
                continue
            if LINT_FOLDER_RE.fullmatch(child.name):
                found.setdefault(child.name, child)
                continue
            try:
                grands = list(child.iterdir())
            except OSError:
                continue
            for grand in grands:
                if grand.is_dir() and LINT_FOLDER_RE.fullmatch(grand.name):
                    found.setdefault(grand.name, grand)

    add(pack_file.parent.parent)
    repo = repo_root()
    if repo is None:
        return found
    try:
        inside = pack_file.resolve().is_relative_to(repo.resolve())
    except OSError:
        inside = False
    if not inside:
        return found
    work = repo / "10.workshop" / "10.10.work"
    if work.is_dir():
        for book in work.iterdir():
            add(book)
    draft = repo / DRAFT_KERNEL
    if draft.is_dir():
        for book in draft.iterdir():
            add(book)
    sample = work / "10.10.11.solo-kernel" / "sample"
    if sample.is_dir():
        for book in sample.iterdir():
            add(book)
    return found


def lint_reasons(path: Path) -> list[str]:
    """Reasons this pack fails. Empty means pass. Reads the file and does not write it."""
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        die("pack is not utf-8")
    reasons: list[str] = []
    seen: set[str] = set()

    def add(msg: str) -> None:
        if msg not in seen:
            seen.add(msg)
            reasons.append(msg)

    live = re.split(r"(?m)^## Note\b", text, maxsplit=1)[0]
    overview_match = re.search(r"(?ms)^Overview:\n(.*?)(?=^#\d{2} |\Z)", live)
    overview = overview_match.group(1) if overview_match else ""
    if overview == "":
        add("shape: overview is missing")
    else:
        if not re.search(r"(?m)^Do:[ \t]*\S", overview):
            add("shape: Do is missing")
        if not re.search(r"(?m)^Stop if:[ \t]*\S", overview):
            add("shape: Stop if is missing")
        if not re.search(r"(?m)^File:[ \t]*\S", overview):
            add("shape: File is missing")
        if not re.search(r"(?m)^.*\bDid\b.*\bBlocked\b.*\bNeed\b", overview):
            add("shape: return line is missing")

    index = lint_page_index(path)

    def placeholder(token: str) -> bool:
        return re.search(r"05\.NN\b|\bNN\b|PPPP|04NN|01NN|05NN", token) is not None

    def forbidden(token: str) -> bool:
        norm = token.replace("\\", "/").strip().strip("`").rstrip("/")
        if re.search(r"(^|/)00\.00\.00\.kernel(?!\.draft)(/|$)", norm):
            return True
        if re.search(r"(^|/)00\.kernel(/|$)", norm):
            return True
        return False

    def path_exists(piece: str) -> bool:
        rel = piece.replace("\\", "/").strip().strip("`").rstrip("/")
        if rel == "":
            return False
        book = path.parent.parent
        cands = [book / rel, path.parent / rel]
        repo = repo_root()
        inside = False
        if repo is not None:
            try:
                inside = path.resolve().is_relative_to(repo.resolve())
            except OSError:
                inside = False
        if inside and repo is not None:
            cands.extend(
                [
                    repo / rel,
                    repo / "10.workshop" / rel,
                    repo / DRAFT_KERNEL / "00.00.01.law" / rel,
                    repo / "10.workshop/10.10.work/10.10.10.lib/code" / rel,
                    repo / "10.workshop/10.10.work/10.10.11.solo-kernel/code" / rel,
                ]
            )
        for cand in cands:
            if cand.exists():
                return True
        if "/" in rel:
            page_name, _, rest = rel.partition("/")
            folder = index.get(page_name)
            if folder is not None and rest and (folder / rest).exists():
                return True
        return rel in index

    def note_name(tok: str) -> None:
        if placeholder(tok):
            return
        if tok in index:
            return
        add(f"names: {tok} is missing")

    def return_ok(piece: str) -> bool:
        rel = piece.replace("\\", "/").rstrip("/")
        if not re.search(r"05\.\d{2}\.return\.md$", rel):
            return False
        toks = LINT_PAGE_RE.findall(rel)
        if not toks:
            return True
        return all(tok in index for tok in toks)

    def examine(piece: str, kind: str) -> None:
        piece = piece.strip().strip("`").strip()
        head = re.match(r"^(.*?\.md)\b", piece)
        if head:
            piece = head.group(1)
        else:
            piece = piece.rstrip(".")
        if not piece or placeholder(piece):
            return
        if piece.startswith("the "):
            for tok in LINT_PAGE_RE.findall(piece):
                note_name(tok)
            for tok in re.findall(r"\d{4}\.[A-Za-z][\w.-]*(?:/[\w.-]+)?", piece):
                examine(tok, kind)
            return
        if forbidden(piece):
            add(f"forbidden: {piece.rstrip('/')}")
            return
        if kind != "read-first" and return_ok(piece):
            return
        if path_exists(piece):
            return
        if kind == "read-first":
            add(f"read-first: {piece} is missing")
        else:
            add(f"names: {piece} is missing")

    saw_read = False
    for line in live.splitlines():
        if line.startswith("status:"):
            continue
        kind = ""
        if line.startswith("Read first:"):
            kind = "read-first"
            saw_read = True
        elif line.startswith("path:"):
            kind = "path"
        elif line.startswith("source:"):
            kind = "source"
        if kind:
            value = line.split(":", 1)[1]
            parts = re.split(r"\s+or\s+|\s+and\s+|,\s*", value.strip())
            for part in parts:
                if part.strip():
                    examine(part, kind)
        for tok in LINT_PAGE_RE.findall(line):
            note_name(tok)
    if not saw_read:
        add("read-first: line is missing")

    batch = LINT_BATCH_RE.fullmatch(path.name)
    if not batch:
        add("number: file is not 05.NN")
    else:
        nn = batch.group(1)
        tail = batch.group(2) or ""
        header = re.search(r"(?m)^# 05\.(\d{2})\s*$", text)
        if not header or header.group(1) != nn:
            add(f"number: header is not 05.{nn}")
        task = header_field(text, "task")
        if task and (not task.isdigit() or int(task) != int(nn)):
            add("number: task does not match")
        folder = LINT_FOLDER_RE.fullmatch(path.parent.name)
        if not folder or folder.group(1) != "05":
            add("number: folder is not 05NN.title")
        else:
            page_num, keyword = folder.group(2), folder.group(3)
            decided = f"04{page_num}.{keyword}"
            decided_dir = index.get(decided)
            if decided_dir is None:
                add(f"number: {decided} is missing")
            elif not (decided_dir / "01.md").is_file():
                add(f"number: {decided}/01.md is missing")
            kw = header_field(text, "keyword")
            if kw and kw != keyword:
                add("number: keyword does not match")
            pppp = header_field(text, "PPPP")
            if pppp and pppp != f"05{page_num}":
                add("number: PPPP does not match")
            if tail == "draft":
                nums = []
                for sib in path.parent.iterdir():
                    hit = LINT_BATCH_RE.fullmatch(sib.name)
                    if hit:
                        nums.append(int(hit.group(1)))
                others = [n for n in nums if n != int(nn)]
                expect = (max(others) + 1) if others else 1
                if int(nn) != expect:
                    add(f"number: 05.{nn} is not the next number")
            if header_field(text, "state") == "closed":
                ret_page = f"01{page_num}.{keyword}"
                ret_file = f"05.{nn}.return.md"
                named = header_field(text, "return")
                label = named or f"{ret_page}/{ret_file}"
                target: Path | None = None
                if named and "/" in named:
                    page_name, _, rest = named.partition("/")
                    folder_path = index.get(page_name)
                    if folder_path is not None and rest and (folder_path / rest).is_file():
                        target = folder_path / rest
                    elif (path.parent.parent / named).is_file():
                        target = path.parent.parent / named
                else:
                    folder_path = index.get(ret_page)
                    if folder_path is not None and (folder_path / ret_file).is_file():
                        target = folder_path / ret_file
                    elif folder_path is not None and (folder_path / f"05.{nn}.md").is_file():
                        target = folder_path / f"05.{nn}.md"
                if target is None:
                    add(f"return: {label} is missing")
                else:
                    try:
                        ret_text = target.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        add("return: is not utf-8")
                    else:
                        head = re.split(r"(?m)^#\d{2} ", ret_text, maxsplit=1)[0]
                        did = re.search(r"(?m)^Did:", head)
                        blocked = re.search(r"(?m)^Blocked:", head)
                        need = re.search(r"(?m)^Need:", head)
                        if not (did and blocked and need and did.start() < blocked.start() < need.start()):
                            add("return: does not start with Did, Blocked, Need")

    surface = []
    for line in live.splitlines():
        if line.startswith("status:"):
            continue
        if re.match(r"^(Do:|recommend:|Ask:|why:)", line):
            surface.append(line)
    asks = False
    for sentence in re.split(r"(?<=\.)\s+", " ".join(surface)):
        if re.search(r"(?i)\b(do not|does not|did not|never|not a|not the|is not|not to)\b", sentence):
            negated = True
        else:
            negated = False
        if negated:
            continue
        if re.search(r"(?i)\bask(?:s|ing)? the director\b", sentence) or re.search(
            r"(?i)\bdirector (?:decides|answers|must decide)\b", sentence
        ):
            asks = True
        if re.search(r"(?i)\bpromote (?:the |an )?approved\b", sentence):
            add("must-not-own: promotes an approved seat")
        if re.search(r"(?i)\b(decide|choose|pick) which law book\b", sentence) or re.search(
            r"(?i)\bwhich law book is the seat\b", sentence
        ):
            add("must-not-own: decides the law book")
    if asks:
        if not re.search(r"(?i)\bissue\b", overview):
            add("decision: issue is missing")
        if not re.search(r"(?i)\boptions?\b", overview):
            add("decision: options are missing")
        if not re.search(r"(?i)what each|each option|\beffects?\b", overview):
            add("decision: effects are missing")
    return reasons


def refuse_closed(path: Path) -> None:
    closed_kernel(path)
    names = [parent.name for parent in (path.resolve(), *path.resolve().parents)]
    if CHECK_KERNEL in names:
        die("dev mode writes kernel.draft. the check kernel is closed")


def lint_home(path: Path) -> Path:
    """The queue when this book has one. Otherwise the pack page."""
    book = path.parent.parent
    queue = book / "0415.queue"
    if queue.is_dir():
        return queue
    return path.parent


def lint_pack_rel(path: Path, home: Path) -> str:
    book = home.parent
    try:
        return path.resolve().relative_to(book.resolve()).as_posix()
    except ValueError:
        return path.name


def lint_held(home: Path, rel: str, digest: str) -> Path | None:
    for child in sorted(home.glob("06.*.md")):
        if not re.fullmatch(r"06\.\d+\.md", child.name):
            continue
        try:
            text = child.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if f"\npack: {rel}\n" in text and f"\nhash: {digest}\n" in text:
            return child
    return None


def lint_next_nn(home: Path) -> str:
    nums = []
    for child in home.glob("06.*.md"):
        hit = re.fullmatch(r"06\.(\d+)\.md", child.name)
        if hit:
            nums.append(int(hit.group(1)))
    nxt = (max(nums) + 1) if nums else 1
    if nxt > 99:
        die("note number is full")
    return f"{nxt:02d}"


def lint_note_text(
    pack_text: str,
    rel: str,
    digest: str,
    reasons: list[str],
    home: Path,
    nn: str,
) -> str:
    day = date.today().isoformat()
    if home.name == "0415.queue":
        pppp = "0415"
        keyword = "queue"
    else:
        pppp = header_field(pack_text, "PPPP")
        keyword = header_field(pack_text, "keyword")
    if reasons:
        why = "A lint fail leaves the file and records the reason."
    else:
        why = "A lint pass asks the Director to promote."
    lines = [
        f"# 06.{nn}",
        "",
        f"Authorization: draft {EM} {day}",
        "who: grok-builder",
        "state: draft",
        "Face: 06",
        f"PPPP: {pppp}",
    ]
    for key in ("desk", "shelf", "book"):
        value = header_field(pack_text, key)
        if value:
            lines.append(f"{key}: {value}")
    if keyword:
        lines.append(f"keyword: {keyword}")
    lines.extend(
        [
            f"why: {why}",
            "",
            f"lint: {'fail' if reasons else 'pass'}",
            f"pack: {rel}",
            f"hash: {digest}",
        ]
    )
    if reasons:
        for reason in reasons:
            lines.append(f"reason: {reason}")
        lines.append("The file stays. No promote request.")
    else:
        lines.append("request: promote")
        lines.append("The Director promotes. This note does not mark the pack ready.")
    lines.append("")
    return "\n".join(lines)


def lint_record(path: Path, raw: bytes, reasons: list[str]) -> str:
    """Write one note for this pack hash. Leave the pack file alone."""
    home = lint_home(path)
    refuse_closed(home)
    rel = lint_pack_rel(path, home)
    digest = sha256(raw)
    held = lint_held(home, rel, digest)
    if held is None:
        nn = lint_next_nn(home)
        dest = home / f"06.{nn}.md"
        if dest.exists():
            die("note is already there")
        body = lint_note_text(raw.decode("utf-8"), rel, digest, reasons, home, nn)
        dest.write_bytes(body.encode("utf-8"))
        held = dest
    return f"{home.name}/{held.name}"


def cmd_lint(path: Path) -> None:
    if not path.is_file():
        die("pack is missing")
    before = path.read_bytes()
    reasons = lint_reasons(path)
    if path.read_bytes() != before:
        die("pack hash changed")
    label = lint_record(path, before, reasons)
    if path.read_bytes() != before:
        die("pack hash changed")
    if reasons:
        for reason in reasons:
            print(f"fail: {reason}")
        print(f"note: {label}")
        raise SystemExit(1)
    print("pass")
    print(f"note: {label}")
    print("request: promote")


def check(cond: bool, msg: str) -> None:
    if not cond:
        die(f"test {msg}")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        page = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2099.trial"
        page.mkdir(parents=True)
        face = page / "01.md"
        drop(face, "Job", "First body.\n", "grok-prime")
        drop(face, "Next", "Second body.\n", "grok-prime")
        text = face.read_text(encoding="utf-8")
        check(text.count("Authorization:") == 1, "header once")
        check("shelf: 10.10.work" in text, "shelf present")
        check(text.index("## Job") < text.index("## Next"), "order")
        check("First body." in text and "Second body." in text, "both bodies")
        drop(face, "Job", "Replaced body.\n", "grok-prime")
        text = face.read_text(encoding="utf-8")
        check("Replaced body." in text, "replaced")
        check("First body." not in text, "old body gone")
        check("Second body." in text, "neighbor stayed")
        check(text.count("Authorization:") == 1, "header still once")
        seeded = page / "04.md"
        seeded.write_bytes(
            (
                stamp(seeded, "grok-prime")
                + "## Job\n\nOld.\n\n## Note — keep\n\nkeep this\n\n### notes\n\nborn: x\n"
            ).encode("utf-8")
        )
        before_note = seeded.read_text(encoding="utf-8")
        note = before_note[before_note.index("## Note — keep"):]
        drop(seeded, "Next", "above the note\n", "grok-prime")
        after = seeded.read_text(encoding="utf-8")
        check(after.index("## Next") < after.index("## Note — keep"), "note stays last")
        check(note in after, "note bytes stayed")
        bare = root / "sample" / "00.00.00.syntax" / "0000.invariant"
        bare.mkdir(parents=True)
        desk_book = bare / "01.md"
        drop(desk_book, "Job", "No shelf here.\n", "grok-prime")
        bare_text = desk_book.read_text(encoding="utf-8")
        check("book: 00.00.00.syntax" in bare_text, "book line")
        check("shelf:" not in bare_text, "missing shelf is a desk book")
        check("desk:" not in bare_text, "no invented desk")
        draft = root / DRAFT_KERNEL / "00.00.00.syntax" / "0000.invariant"
        draft.mkdir(parents=True)
        drop(draft / "01.md", "Job", "dev write\n", "grok-prime")
        check((draft / "01.md").is_file(), "dev writes the draft")
        check_kernel = root / CHECK_KERNEL / "00.00.00.syntax" / "0000.invariant"
        check_kernel.mkdir(parents=True)
        try:
            drop(check_kernel / "01.md", "Job", "nope\n", "grok-prime")
        except SystemExit as exc:
            check("closed" in str(exc), "check kernel stays closed")
        else:
            die("test check kernel was written")
        check(not (check_kernel / "01.md").exists(), "check kernel file absent")
        os.environ["CLERK_MODE"] = "clerk"
        try:
            try:
                drop(draft / "02.md", "Job", "nope\n", "grok-prime")
            except SystemExit as exc:
                check("does not write" in str(exc), "clerk mode does not write")
            else:
                die("clerk mode wrote a face")
            check(kernel_root(root) == root / CHECK_KERNEL, "clerk points at the kernel")
        finally:
            os.environ.pop("CLERK_MODE", None)
        check(kernel_root(root) == root / DRAFT_KERNEL, "dev points at the draft")
        check(not (draft / "02.md").exists(), "clerk write absent")
        trial = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2098.trial"
        trial.mkdir(parents=True)
        seat = trial / "01.md"
        seat_bytes = (
            "# 01\n\n"
            "version: 002\n"
            f"Authorization: approved {EM} 2026-10-12\n"
            "who: grok-prime\n"
            "state: approved\n"
            "Face: 01\n"
            "PPPP: 2098\n"
            "keyword: trial\n"
            "why: Seat.\n\n"
            "cite:\n\n"
            "## Job\n\n"
            "The seat body.\n\n"
            "## Note — one\n\n"
            "born: 2026-10-13\n"
            "Keep the seat.\n"
        ).encode("utf-8")
        seat.write_bytes(seat_bytes)
        (trial / "06.md").write_bytes(
            (
                "# 06\n\n"
                "## Note — one\n\n"
                "born: 2026-10-13\n"
                "Keep the seat.\n\n"
                "## Note — two\n\n"
                "born: 2026-10-13\n"
                "The draft is the working copy.\n\n"
                "### notes\n"
                "born: 2026-10-13\n"
            ).encode("utf-8")
        )
        made, notes = make_draft(seat, "grok-prime")
        check(made.name == "01.003.md", "draft name")
        check(notes == "2", "new notes applied")
        check(seat.read_bytes() == seat_bytes, "seat unchanged")
        copied = made.read_text(encoding="utf-8")
        check("state: draft" in copied, "draft state")
        check(f"Authorization: draft {EM} " in copied, "draft authorization")
        check("Authorization: approved" not in copied, "approved stamp stays off the draft")
        check("version: 003" in copied, "draft version")
        check(copied.count("## Note — one") == 1, "note already on the seat")
        check("## Note — two" in copied, "note from 06")
        check("### notes" in copied, "notes trailer")
        check("The seat body." in copied, "seat body copied")
        check(f"source hash: {sha256(seat_bytes)}" in copied, "source hash")
        check("source version: 002" in copied, "source version")
        check(copied.count("\nsource path:") == 1, "one source path")
        check("book: 10.10.10.lib" in copied, "draft address")
        check("\r" not in copied, "draft is LF")
        again = insert_source_block(copied, ["source path: again", "source hash: abc"])
        check(again.count("\nsource path:") == 1, "second write replaces the block")
        try:
            make_draft(seat, "grok-prime")
        except SystemExit as exc:
            check("one draft is open" in str(exc), "one draft")
        else:
            die("test opened a second draft")
        check(len(open_named(trial, "01")) == 1, "still one draft")
        try:
            drop(seat, "Job", "nope\n", "grok-prime")
        except SystemExit as exc:
            check("make a draft" in str(exc), "approved seat stays")
        else:
            die("test wrote the seat")
        check(seat.read_bytes() == seat_bytes, "seat bytes after drop")
        result, built_name = make_derived(made, "grok-prime")
        check(result == "missing", "missing relationship")
        check(built_name == "", "missing writes nothing")
        check(not (trial / "08.md").exists(), "08.md absent")
        check(not open_named(trial, "08"), "no built draft yet")
        drop(made, "Relationships", "Parent is the door.\n", "grok-prime")
        check(seat.read_bytes() == seat_bytes, "drop stayed on the draft")
        result, built_name = make_derived(made, "grok-prime")
        check(result == "built", "built")
        check(built_name == "08.003.md", "built name")
        built = (trial / built_name).read_text(encoding="utf-8")
        check("state: built" in built, "built state")
        check("seat version: 002" in built, "seat version")
        check("draft version: 003" in built, "draft version")
        check("extract: Relationships" in built, "extraction mark")
        check(built.count("\nseat path:") == 1, "one seat path")
        check(built.count("\ndraft path:") == 1, "one draft path")
        check(f"seat hash: {sha256(seat_bytes)}" in built, "seat hash is the baseline")
        check(f"draft hash: {sha256(made.read_bytes())}" in built, "draft hash is the input")
        check("\nwhy:\n\ncite:\n" in built, "why and cite stay empty")
        check("source version:" not in built, "one identity block")
        check("Parent is the door." in built, "supplied body")
        check("The seat body." not in built, "seat body stays off 08")
        check(not (trial / "08.md").exists(), "08.md still absent")
        try:
            make_derived(made, "grok-prime")
        except SystemExit as exc:
            check("one built draft is open" in str(exc), "one built draft")
        else:
            die("test built a second 08")
        try:
            drop(trial / built_name, "Job", "nope\n", "grok-prime")
        except SystemExit as exc:
            check("built face stays" in str(exc), "built face stays")
        else:
            die("test wrote the built face")
        bad = trial / "01.002.draft.md"
        bad.write_bytes(b"# 01\n")
        try:
            drop(bad, "Job", "x\n", "grok-prime")
        except SystemExit as exc:
            check("a draft is FF.VVV.md" in str(exc), "draft tail stops")
        else:
            die("test accepted a draft tail")
        bad.unlink()
        numbered = trial / "01.001.md"
        numbered.write_bytes(b"# 01\n")
        try:
            drop(numbered, "Job", "x\n", "grok-prime")
        except SystemExit as exc:
            check("version 001 is FF.md" in str(exc), "version 001 is FF.md")
        else:
            die("test accepted FF.001.md")
        numbered.unlink()
        record = root / "sample" / "00.00.00.syntax" / "2097.record"
        record.mkdir(parents=True)
        plain = record / "01.md"
        plain_bytes = (
            "# 01\n\n"
            f"Authorization: approved {EM} 2026-10-12\n"
            "state: approved\n"
            "Face: 01\n\n"
            "## Relationships\n\n"
            "On record.\n"
        ).encode("utf-8")
        plain.write_bytes(plain_bytes)
        made_plain, plain_notes = make_draft(plain, "grok-prime")
        check(made_plain.name == "01.002.md", "versionless seat drafts 002")
        check(plain_notes == "none", "missing 06")
        check(plain.read_bytes() == plain_bytes, "seat gained no version")
        check("version:" not in plain.read_text(encoding="utf-8"), "version stays off the seat")
        result, built_name = make_derived(made_plain, "grok-prime")
        check(result == "built" and built_name == "08.002.md", "on record")
        on_record = (record / built_name).read_text(encoding="utf-8")
        check("On record." in on_record, "recorded body")
        check("seat version:" not in on_record, "no invented seat version")
        check("book: 00.00.00.syntax" in on_record, "built book line")
        check("shelf:" not in on_record, "built desk book")
        try:
            make_draft(check_kernel / "01.md", "grok-prime")
        except SystemExit as exc:
            check("closed" in str(exc), "draft stays off the check kernel")
        else:
            die("test drafted the check kernel")
        os.environ["CLERK_MODE"] = "clerk"
        try:
            try:
                make_draft(seat, "grok-prime")
            except SystemExit as exc:
                check("does not write" in str(exc), "clerk mode does not draft")
            else:
                die("clerk mode drafted a face")
            check(len(open_named(trial, "01")) == 1, "clerk draft absent")
        finally:
            os.environ.pop("CLERK_MODE", None)
        crlf_page = root / "sample" / "00.00.01.law" / "0002.schema"
        crlf_page.mkdir(parents=True)
        crlf_text = (
            "# 01\n\n"
            "version: 004\n"
            f"Authorization: approved {EM} 2026-10-12\n"
            "state: approved\n"
            "Face: 01\n"
            "PPPP: 0002\n"
            "book: 00.00.01.law\n"
            "keyword: schema\n"
            "why:\n\n"
            "cite:\n\n"
            "## Job\n\n"
            "Cross book body.\n"
        )
        crlf_raw = crlf_text.replace("\n", "\r\n").encode("utf-8")
        crlf_seat = crlf_page / "01.md"
        crlf_seat.write_bytes(crlf_raw)
        (crlf_page / "06.md").write_bytes(
            "## Note — from source\n\nborn: 2026-10-13\nKeep this note.\n".encode("utf-8")
        )
        cross = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2096.cross"
        cross.mkdir(parents=True)
        crossed, cross_notes = make_draft(crlf_seat, "grok-prime", cross)
        check(crossed.parent == cross, "draft lands in the other page")
        check(crlf_seat.read_bytes() == crlf_raw, "source seat unchanged")
        cross_text = crossed.read_text(encoding="utf-8")
        check("\r" not in cross_text, "crlf seat drafts as LF")
        check("Cross book body." in cross_text, "body preserved")
        check("version: 005" in cross_text, "version plus one")
        check("source version: 004" in cross_text, "source version kept")
        check(f"source hash: {sha256(crlf_raw)}" in cross_text, "hash is the crlf bytes")
        check("book: 10.10.10.lib" in cross_text, "dest book")
        check("shelf: 10.10.work" in cross_text, "dest shelf")
        check("book: 00.00.01.law" not in cross_text, "old book line replaced")
        check(show_path(crlf_seat) in cross_text, "source path kept")
        check(cross_notes == "1", "source notes copied")
        check("Keep this note." in cross_text, "note text")
        signed = trial / "03.002.md"
        signed_bytes = made.read_bytes().replace(b"state: draft", b"state: signed")
        signed.write_bytes(signed_bytes)
        try:
            drop(signed, "Job", "nope\n", "grok-prime")
        except SystemExit as exc:
            check("signed draft stays" in str(exc), "drop refuses signed")
        else:
            die("test dropped a signed draft")
        try:
            revise(signed, "The seat body.", "No.\n", "grok-prime")
        except SystemExit as exc:
            check("signed draft stays" in str(exc), "revise refuses signed")
        else:
            die("test revised a signed draft")
        check(signed.read_bytes() == signed_bytes, "signed bytes stayed")
        revise(made, "The seat body.", "The new body.", "grok-prime")
        revised = made.read_text(encoding="utf-8")
        check("The new body." in revised, "sentence replaced")
        check("The seat body." in revised, "old sentence recorded")
        check("## Note — revise " in revised, "revise note")
        twice = trial / "02.md"
        twice_bytes = b"# 02\n\nstate: draft\n\nSame. Same.\n"
        twice.write_bytes(twice_bytes)
        try:
            revise(twice, "Same.", "Once.", "grok-prime")
        except SystemExit as exc:
            check("there twice" in str(exc), "repeated sentence stops")
        else:
            die("test revised a repeated sentence")
        check(twice.read_bytes() == twice_bytes, "repeated sentence unchanged")
        try:
            revise(made, "Not in the file.", "No.\n", "grok-prime")
        except SystemExit as exc:
            check("missing" in str(exc), "missing sentence stops")
        else:
            die("test revised a missing sentence")
        held = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2095.held"
        held.mkdir(parents=True)
        held_draft = held / "01.md"
        held_draft.write_bytes(
            (stamp(held_draft, "grok-prime") + "## Relationships\n\nRow.\n").encode("utf-8")
        )
        held_seat = b"# 08\n\nstate: approved\n"
        (held / "08.md").write_bytes(held_seat)
        result, seated_name = make_derived(held_draft, "grok-prime")
        check(result == "seated" and seated_name == "08.md", "seated 08")
        check(
            not any(path.name.startswith("08") and path.name != "08.md" for path in held.iterdir()),
            "seated 08 writes nothing",
        )
        check((held / "08.md").read_bytes() == held_seat, "seated 08 unchanged")
        source_page = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2096.source"
        source_page.mkdir(parents=True)
        low = source_page / "01.003.md"
        high = source_page / "01.005.md"
        other = source_page / "02.002.md"
        low.write_bytes(
            b"# 01\n\nversion: 003\nwho: grok-prime\nstate: draft\n\n## Job\n\nLow body.\n"
        )
        high.write_bytes(
            b"# 01\n\nversion: 005\nwho: grok-prime\nstate: draft\n\n## Job\n\nHigh body.\n"
        )
        other.write_bytes(
            b"# 02\n\nversion: 002\nwho: grok-prime\nstate: draft\n\n## Job\n\nOther.\n"
        )
        before = sorted(path.name for path in source_page.iterdir())
        listed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "versions", str(source_page)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        shown = (listed.stdout or "") + (listed.stderr or "")
        check(listed.returncode != 0, "versions stops")
        check("name the stronger face" in shown, "versions asks for a name")
        check("writes: no" in shown, "versions writes no")
        check("01.005.md highest" in shown, "highest marked")
        check("02.002.md highest" in shown, "other face highest")
        check("01.003.md" in shown and "01.003.md highest" not in shown, "lower stays unmarked")
        check(sorted(path.name for path in source_page.iterdir()) == before, "versions writes nothing")
        dest_page = root / "10.workshop" / "10.10.work" / "10.10.10.lib" / "2094.named"
        dest_page.mkdir()
        imported = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "import",
                str(dest_page),
                "--from",
                str(low),
                "--who",
                "grok-builder",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        imported_shown = (imported.stdout or "") + (imported.stderr or "")
        check(imported.returncode == 0, "import exits 0 " + imported_shown)
        seat = dest_page / "01.md"
        seat_bytes = seat.read_bytes()
        seat_text = seat_bytes.decode("utf-8")
        check("Low body." in seat_text, "named body")
        check("High body." not in seat_text, "highest was not chosen")
        check("source version: 003" in seat_text, "source version kept")
        check(f"source hash: {sha256(low.read_bytes())}" in seat_text, "source hash kept")
        check("\nversion: 001\n" in seat_text, "seat version 001")
        check("state: draft" in seat_text, "seat state draft")
        check("who: grok-builder" in seat_text, "import who")
        check(b"\r" not in seat_bytes, "import lf")
        again = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "import",
                str(dest_page),
                "--from",
                str(high),
                "--who",
                "grok-builder",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        again_shown = (again.stdout or "") + (again.stderr or "")
        check(again.returncode != 0 and "a seat is here" in again_shown, "second import stops")
        check(seat.read_bytes() == seat_bytes, "seat unchanged")
        bare = source_page / "04.md"
        bare.write_bytes(
            b"# 04\n\nversion: 001\nstate: approved\nwho: grok-prime\n\n## Job\n\nSeat.\n"
        )
        refused = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "import",
                str(dest_page),
                "--from",
                str(bare),
                "--who",
                "grok-builder",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        refused_shown = (refused.stdout or "") + (refused.stderr or "")
        check(
            refused.returncode != 0 and "import starts from the named version" in refused_shown,
            "bare seat is not an import",
        )
        repo = repo_root()
        check(repo is not None, "repo root")
        live_q = repo / "10.workshop/10.10.work/10.10.12.rebuild/0415.queue"
        live_q_before = sorted(p.name for p in live_q.iterdir()) if live_q.is_dir() else []
        kept = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.002.py"
        check(kept.is_file(), "older clerk kept")
        check(
            sha256(kept.read_bytes())
            == "8bda14f92539a6db8f73c5bac5c2c0566cf1b7bd96ffc944e24379776ad77623",
            "older clerk hash",
        )
        kept3 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.003.py"
        check(kept3.is_file(), "clerk 003 kept")
        check(
            sha256(kept3.read_bytes())
            == "57605d4481f53e9c6bddb87ea449632327f11131368dd1f557ff3cbf45d2a9b6",
            "clerk 003 hash",
        )
        kept4 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.004.py"
        check(kept4.is_file(), "clerk 004 kept")
        check(
            sha256(kept4.read_bytes())
            == "0a74e32a32fd7d9a1117936b89fbdd5aaf283881e4f6257d9cafbee459aa7ee9",
            "clerk 004 hash",
        )
        kept5 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.005.py"
        check(kept5.is_file(), "clerk 005 kept")
        check(
            sha256(kept5.read_bytes())
            == "8c5198958a3f9a252e5aee39cc82038ddfc11ada870d12c93c752a19c487a5ab",
            "clerk 005 hash",
        )
        kept6 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.006.py"
        check(kept6.is_file(), "clerk 006 kept")
        check(
            sha256(kept6.read_bytes())
            == "40fb6883b9cfb95fcd8b0068a542e64be7e260e9f0227eb8934243bed049e0cd",
            "clerk 006 hash",
        )
        kept7 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.007.py"
        check(kept7.is_file(), "clerk 007 kept")
        check(
            sha256(kept7.read_bytes())
            == "64557b89a9739d36340f6d7334e2b0fd6b8fdda8e7817f22b3d2f4db0786e7c1",
            "clerk 007 hash",
        )
        kept8 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.008.py"
        check(kept8.is_file(), "clerk 008 kept")
        check(
            sha256(kept8.read_bytes())
            == "4118252d7b368c26865624b68dcc59fe055ceb00d7de837cc7c2ea0cb812e0b0",
            "clerk 008 hash",
        )
        kept9 = repo / "10.workshop/10.10.work/10.10.12.rebuild/0305.clerk/02.clerk.009.py"
        check(kept9.is_file(), "clerk 009 kept")
        check(
            sha256(kept9.read_bytes())
            == "0e3fce695dd1ec58e34d7278788d1727998c81fa4b36f9cdf99466c0c5457f15",
            "clerk 009 hash",
        )
        desk = root / "10.workshop"
        desk.mkdir(parents=True, exist_ok=True)
        start = desk / "00.start.md"
        start.write_bytes("# 00.start\n\nThe check is `00.00.00.kernel`.\n".encode("utf-8"))
        revise(
            start,
            "The check is `00.00.00.kernel`.",
            "The check is `00.00.00.kernel.draft`.",
            "grok-builder",
        )
        got = start.read_text(encoding="utf-8")
        check("The check is `00.00.00.kernel.draft`." in got, "desk start revised")
        check("The check is `00.00.00.kernel`." in got, "old start sentence kept")
        readme = desk / "00.readme.md"
        readme.write_bytes("The book is `10.10.10.lib`.\n".encode("utf-8"))
        revise(
            readme,
            "The book is `10.10.10.lib`.",
            "The book is `10.10.12.rebuild`.",
            "grok-builder",
        )
        got = readme.read_text(encoding="utf-8")
        check("The book is `10.10.12.rebuild`." in got, "desk readme revised")
        check("The book is `10.10.10.lib`." in got, "old book sentence kept")
        order = desk / "00.order.md"
        order.write_bytes("- 0160.structure-door.temp\n".encode("utf-8"))
        revise(
            order,
            "- 0160.structure-door.temp",
            "- 0160.structure-door.temp\n## work\n- 1000.work",
            "grok-builder",
        )
        got = order.read_text(encoding="utf-8")
        check("- 1000.work" in got, "desk order lists the page")
        check("- 0160.structure-door.temp" in got, "old order line kept")
        stayed_order = order.read_bytes()
        try:
            drop(order, "Job", "nope\n", "grok-builder")
        except SystemExit as exc:
            check("face file is FF.md or FF.VVV.md" in str(exc), "drop still refuses the order name")
        else:
            die("drop wrote the order")
        check(order.read_bytes() == stayed_order, "drop left the order")
        about = desk / "00.about.md"
        before = b"# 00.about\n\nHello.\n"
        about.write_bytes(before)
        try:
            revise(about, "Hello.", "No.", "grok-builder")
        except SystemExit as exc:
            check("face file is FF.md or FF.VVV.md" in str(exc), "random desk name stops")
        else:
            die("random desk name was revised")
        check(about.read_bytes() == before, "random desk name unchanged")
        sentinel = desk / "00.md"
        sentinel.write_bytes("Then `00.live` names the law book.\n".encode("utf-8"))
        revise(
            sentinel,
            "Then `00.live` names the law book.",
            "`00.live` holds last, when, goal, pages.",
            "grok-builder",
        )
        got = sentinel.read_text(encoding="utf-8")
        check("`00.live` holds last, when, goal, pages." in got, "desk 00 revised")
        check("Then `00.live` names the law book." in got, "old 00 sentence kept")
        order.write_bytes(
            (
                "- 0159.commands-door.temp\n"
                "- 0160.structure-door.temp\n"
                "## work\n"
                "- 1000.work\n"
                "## Note — revise 2026-10-23\n"
                "\n"
                "born: 2026-10-23\n"
                "source: grok-builder\n"
                "\n"
                "- 0160.structure-door.temp\n"
            ).encode("utf-8")
        )
        try:
            revise(order, "- 0160.structure-door.temp", "- 1000.work", "grok-builder")
        except SystemExit as exc:
            check("sentence is there twice" in str(exc), "two bullets still stop")
        else:
            die("two bullets were replaced")
        revise(
            order,
            "- 0160.structure-door.temp",
            "retired: 0160.structure-door.temp",
            "grok-builder",
        )
        got = order.read_text(encoding="utf-8")
        check(
            not any(line.startswith("- 0160") for line in got.splitlines()),
            "retired bullet is gone",
        )
        check("retired: 0160.structure-door.temp" in got, "retired mark kept")
        check("- 0159.commands-door.temp" in got, "other bullet stays")
        check("- 1000.work" in got, "work bullet stays")
        stayed = start.read_bytes()
        try:
            drop(start, "Job", "nope\n", "grok-builder")
        except SystemExit as exc:
            check("face file is FF.md or FF.VVV.md" in str(exc), "drop still refuses the desk name")
        else:
            die("drop wrote a desk file")
        check(start.read_bytes() == stayed, "drop left the desk file")
        bare_src = root / "sample" / "00.00.01.law" / "1001.accounting"
        bare_src.mkdir(parents=True)
        bare_face = bare_src / "01.md"
        bare_raw = (
            "# 01\n\n"
            "version: 001\n"
            f"Authorization: draft {EM} 2026-10-15\n"
            "who: grok-prime\n"
            "state: draft\n"
            "Face: 01\n"
            "PPPP: 1001\n"
            "book: 00.00.01.law\n"
            "keyword: accounting\n"
            "why: The rule for dates on this page.\n\n"
            "cite: 2.8\n\n"
            "## Date format\n\n"
            "Dates on this page are written day, month, year, as DD-MM-YYYY.\n"
        ).encode("utf-8")
        bare_face.write_bytes(bare_raw)
        law = root / DRAFT_KERNEL / "00.00.01.law"
        law.mkdir(parents=True)
        clerk = str(Path(__file__).resolve())
        seated = subprocess.run(
            [sys.executable, clerk, "seat", str(law / "1001.accounting"), "--from", str(bare_face), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        seated_shown = (seated.stdout or "") + (seated.stderr or "")
        check(seated.returncode == 0, "seat exits 0 " + seated_shown)
        seated_face = law / "1001.accounting" / "01.md"
        seated_bytes = seated_face.read_bytes()
        seated_text = seated_bytes.decode("utf-8")
        check("Dates on this page are written day, month, year, as DD-MM-YYYY." in seated_text, "seat body")
        check(f"source hash: {sha256(bare_raw)}" in seated_text, "seat source hash")
        check("source path:" in seated_text, "seat source path")
        check("\nversion: 001\n" in seated_text, "seat version 001")
        check("state: draft" in seated_text, "seat state draft")
        check("who: grok-builder" in seated_text, "seat who")
        check("keyword: accounting" in seated_text, "seat keyword")
        check("book: 00.00.01.law" in seated_text, "seat book")
        check(b"\r" not in seated_bytes, "seat lf")
        check(bare_face.read_bytes() == bare_raw, "seat source unchanged")
        again = subprocess.run(
            [sys.executable, clerk, "seat", str(law / "1001.accounting"), "--from", str(bare_face), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        again_shown = (again.stdout or "") + (again.stderr or "")
        check(again.returncode != 0 and "a seat is here" in again_shown, "second seat stops")
        check(seated_face.read_bytes() == seated_bytes, "second seat wrote nothing")
        numbered = bare_src / "01.002.md"
        numbered.write_bytes(bare_raw.replace(b"version: 001", b"version: 002"))
        named = subprocess.run(
            [sys.executable, clerk, "seat", str(law / "1002.other"), "--from", str(numbered), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        named_shown = (named.stdout or "") + (named.stderr or "")
        check(named.returncode != 0 and "import starts from the named version" in named_shown, "named version is not a bare seat")
        check(not (law / "1002.other").exists(), "named version wrote no folder")
        closed_book = root / CHECK_KERNEL / "00.00.01.law"
        closed_book.mkdir(parents=True)
        closed = subprocess.run(
            [sys.executable, clerk, "seat", str(closed_book / "1001.accounting"), "--from", str(bare_face), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        closed_shown = (closed.stdout or "") + (closed.stderr or "")
        check(closed.returncode != 0 and "the check kernel is closed" in closed_shown, "seat stays off the check kernel")
        check(not (closed_book / "1001.accounting").exists(), "check kernel folder absent")
        bare_kernel = root / "00.kernel" / "00.00.01.law"
        bare_kernel.mkdir(parents=True)
        kernel_stop = subprocess.run(
            [sys.executable, clerk, "seat", str(bare_kernel / "1001.accounting"), "--from", str(bare_face), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        kernel_shown = (kernel_stop.stdout or "") + (kernel_stop.stderr or "")
        check(kernel_stop.returncode != 0 and "the kernel is not edited" in kernel_shown, "00.kernel stops")
        check(not (bare_kernel / "1001.accounting").exists(), "00.kernel folder absent")
        imported = subprocess.run(
            [sys.executable, clerk, "import", str(law / "1001.accounting"), "--from", str(bare_face), "--who", "grok-builder"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        imported_shown = (imported.stdout or "") + (imported.stderr or "")
        check(imported.returncode != 0 and "import starts from the named version" in imported_shown, "bare draft is not an import")
        check(seated_face.read_bytes() == seated_bytes, "import left the bare seat")
        junk = bare_src / "readme.txt"
        junk.write_bytes(b"no\n")
        try:
            make_seat(law / "1001.accounting", junk, "grok-builder")
        except SystemExit as exc:
            check("face file is FF.md or FF.VVV.md" in str(exc), "random file stops")
        else:
            die("a random file was seated")
        check(seated_face.read_bytes() == seated_bytes, "random file wrote nothing")
        six_src = root / "sample" / "00.00.01.law" / "1005.notes"
        six_src.mkdir()
        six = six_src / "06.md"
        six.write_bytes(b"# 06\n\nversion: 001\nstate: draft\nwho: grok-prime\n\n## Note\n\nStay.\n")
        try:
            make_seat(law / "1005.notes", six, "grok-builder")
        except SystemExit as exc:
            check("face 06 stays off" in str(exc), "face 06 stays off")
        else:
            die("face 06 was seated")
        check(not (law / "1005.notes").exists(), "face 06 wrote no folder")
        try:
            make_seat(law / "1003.nope", bare_face, "grok-builder")
        except SystemExit as exc:
            check("page name does not match the source" in str(exc), "page name must match")
        else:
            die("a mismatched page was created")
        check(not (law / "1003.nope").exists(), "mismatched page absent")
        try:
            make_seat(root / DRAFT_KERNEL / "00.00.09.missing" / "1001.accounting", bare_face, "grok-builder")
        except SystemExit as exc:
            check("book folder is missing" in str(exc), "missing book stops")
        else:
            die("a missing book was created")
        check(not (root / DRAFT_KERNEL / "00.00.09.missing").exists(), "missing book absent")
        card = bare_src / "02.md"
        card.write_bytes(
            b"# 02\n\nversion: 001\nstate: draft\nwho: grok-prime\n\n## Date format\n\nDD-MM-YYYY.\n"
        )
        (law / "1001.accounting" / "02.002.md").write_bytes(b"# 02\n\nversion: 002\nstate: draft\n")
        try:
            make_seat(law / "1001.accounting", card, "grok-builder")
        except SystemExit as exc:
            check("one draft is open" in str(exc), "open draft stops")
        else:
            die("an open draft was seated over")
        check(not (law / "1001.accounting" / "02.md").exists(), "open draft wrote nothing")
        claimed = bare_src / "07.md"
        claimed.write_bytes(b"# 07\n\nversion: 002\nstate: draft\nwho: grok-prime\n\n## Job\n\nClaimed.\n")
        try:
            make_seat(law / "1001.accounting", claimed, "grok-builder")
        except SystemExit as exc:
            check("import starts from the named version" in str(exc), "header 002 is not a bare seat")
        else:
            die("header 002 was seated")
        check(not (law / "1001.accounting" / "07.md").exists(), "header 002 wrote nothing")
        plain_src = root / "sample" / "00.00.01.law" / "1006.plain"
        plain_src.mkdir()
        plain_face = plain_src / "05.md"
        plain_raw = b"# 05\n\nstate: draft\nwho: grok-prime\n\n## Job\n\nNo version line.\n"
        plain_face.write_bytes(plain_raw)
        plain_seat = make_seat(law / "1006.plain", plain_face, "grok-builder")
        plain_text = plain_seat.read_text(encoding="utf-8")
        check("No version line." in plain_text, "empty version body")
        check("\nversion: 001\n" in plain_text, "empty version becomes 001")
        check("source version:" not in plain_text, "empty version has no source version")
        check(f"source hash: {sha256(plain_raw)}" in plain_text, "empty version hash")
        cleanup_src = root / "sample" / "00.00.01.law" / "1004.cleanup"
        cleanup_src.mkdir()
        cleanup_face = cleanup_src / "03.md"
        cleanup_face.write_bytes(b"# 03\n\nversion: 001\nstate: draft\nwho: grok-prime\n\n## Job\n\nGone.\n")
        cleanup_dest = law / "1004.cleanup"
        real_write = Path.write_bytes

        def boom(self, data):
            if self.name == "03.md" and self.parent.name == "1004.cleanup" and DRAFT_KERNEL in self.parts:
                raise OSError("disk full")
            return real_write(self, data)

        Path.write_bytes = boom
        try:
            try:
                make_seat(cleanup_dest, cleanup_face, "grok-builder")
            except OSError as exc:
                check("disk full" in str(exc), "seat write can fail")
            else:
                die("seat write was supposed to fail")
        finally:
            Path.write_bytes = real_write
        check(not cleanup_dest.exists(), "failed seat removes the new folder")
        live_text = (
            "last: 0513/05.19 closed\n"
            "when: now\n"
            "goal: law-align seating closed\n"
            "pages: 0513.law-align, 0415.queue\n"
        )
        written = write_live(
            law,
            "0513/05.19 closed",
            "now",
            "law-align seating closed",
            "0513.law-align, 0415.queue",
        )
        check(written == live_text, "live four lines")
        check((law / "00.live").read_bytes() == live_text.encode("utf-8"), "live bytes")
        check(read_live(law) == live_text, "live read")
        replaced = write_live(law, "later", "now", "next", "one")
        check(replaced.count("last:") == 1, "live overwrites")
        check("0513/05.19 closed" not in replaced, "live dropped the old line")
        (law / "00.live").write_bytes(live_text.encode("utf-8"))
        stayed_live = (law / "00.live").read_bytes()
        try:
            drop(law / "00.live", "Job", "nope\n", "grok-builder")
        except SystemExit as exc:
            check("a model does not write 00.live" in str(exc), "drop refuses 00.live")
        else:
            die("drop wrote 00.live")
        try:
            revise(law / "00.live", "now", "later", "grok-builder")
        except SystemExit as exc:
            check("a model does not write 00.live" in str(exc), "revise refuses 00.live")
        else:
            die("revise wrote 00.live")
        check((law / "00.live").read_bytes() == stayed_live, "model write left 00.live")
        try:
            write_live(law, " ", "now", "goal", "pages")
        except SystemExit as exc:
            check("last is empty" in str(exc), "empty last stops")
        else:
            die("empty last wrote")
        check((law / "00.live").read_bytes() == stayed_live, "empty last wrote nothing")
        other = root / DRAFT_KERNEL / "00.00.00.syntax"
        other.mkdir(parents=True, exist_ok=True)
        try:
            write_live(other, "a", "b", "c", "d")
        except SystemExit as exc:
            check("draft law book" in str(exc), "live stays on the law book")
        else:
            die("live wrote another book")
        check(not (other / "00.live").exists(), "other book live absent")
        (law / "00.live").unlink()
        try:
            read_live(law)
        except SystemExit as exc:
            check("00.live is missing" in str(exc), "missing live stops")
        else:
            die("missing live was read")
        (law / "00.live").write_bytes(stayed_live)
        clerk = str(Path(__file__).resolve())
        partial = subprocess.run(
            [sys.executable, clerk, "live", str(law), "--last", "only"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        partial_shown = (partial.stdout or "") + (partial.stderr or "")
        check(
            partial.returncode != 0 and "needs last, when, goal, and pages" in partial_shown,
            "partial live stops",
        )
        check((law / "00.live").read_bytes() == stayed_live, "partial live wrote nothing")
        read_back = subprocess.run(
            [sys.executable, clerk, "live", str(law)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(read_back.returncode == 0 and read_back.stdout == live_text, "live command reads")
        closed = subprocess.run(
            [
                sys.executable,
                clerk,
                "live",
                str(root / CHECK_KERNEL / "00.00.01.law"),
                "--last", "a",
                "--when", "b",
                "--goal", "c",
                "--pages", "d",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        closed_shown = (closed.stdout or "") + (closed.stderr or "")
        check(
            closed.returncode != 0 and "the check kernel is closed" in closed_shown,
            "live stays off the check kernel",
        )
        check(not (root / CHECK_KERNEL / "00.00.01.law" / "00.live").exists(), "check kernel live absent")
        kernel_stop = subprocess.run(
            [
                sys.executable,
                clerk,
                "live",
                str(root / "00.kernel" / "00.00.01.law"),
                "--last", "a",
                "--when", "b",
                "--goal", "c",
                "--pages", "d",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        kernel_shown = (kernel_stop.stdout or "") + (kernel_stop.stderr or "")
        check(kernel_stop.returncode != 0 and "the kernel is not edited" in kernel_shown, "00.kernel live stops")
        check(not (root / "00.kernel" / "00.00.01.law" / "00.live").exists(), "00.kernel live absent")

        def lint_case(case: str, filename: str, body: str) -> Path:
            book = root / case
            dec = book / "0417.pack-lint"
            dec.mkdir(parents=True, exist_ok=True)
            (dec / "01.md").write_bytes(b"# 01\n")
            (dec / "06.01.md").write_bytes(b"# 06.01\n")
            (book / "0117.pack-lint").mkdir(exist_ok=True)
            folder = book / "0517.pack-lint"
            folder.mkdir(exist_ok=True)
            dest = folder / filename
            dest.write_bytes(body.encode("utf-8"))
            return dest

        def lint_body(
            nn: str = "01",
            do: str = "Add one check. The check kernel stays closed.",
            state: str = "draft",
            extra: str = "",
        ) -> str:
            return (
                f"# 05.{nn}\n\n"
                "Authorization: draft\n"
                "who: grok\n"
                f"state: {state}\n"
                f"task: {nn}\n"
                "Face: 05\n"
                "PPPP: 0517\n"
                "keyword: pack-lint\n"
                "why: Pack.\n\n"
                "cite: 3.1\n\n"
                "Overview:\n"
                f"This file is 05.{nn}.draft.md. It is ready.\n"
                "Read first: 0417.pack-lint/01.md and 0417.pack-lint/06.01.md.\n"
                f"Do: {do}\n"
                "Stop if: the file changes.\n"
                "File: the return.\n"
                "Start the return with Did, Blocked, and Need.\n\n"
                "#01 >build work\n"
                "recommend: Write 0117.pack-lint/05.01.return.md when the work is done.\n"
                "path: 0417.pack-lint/01.md\n"
                "Ask: >build Do the work.\n"
                f"{extra}"
            )

        clean = lint_case("lint-clean", "05.01.draft.md", lint_body())
        clean_bytes = clean.read_bytes()
        got = lint_reasons(clean)
        check(got == [], "clean lint " + " | ".join(got))
        check(clean.read_bytes() == clean_bytes, "clean lint wrote nothing")
        shape = lint_case(
            "lint-shape",
            "05.01.draft.md",
            lint_body().replace("Do: Add one check. The check kernel stays closed.\n", ""),
        )
        shape_bytes = shape.read_bytes()
        got = lint_reasons(shape)
        check("shape: Do is missing" in got, "missing Do")
        check(shape.read_bytes() == shape_bytes, "shape lint wrote nothing")
        named = lint_case(
            "lint-name",
            "05.01.draft.md",
            lint_body(extra="path: 0199.missing-page/01.md\n"),
        )
        named_bytes = named.read_bytes()
        got = lint_reasons(named)
        check(any("0199.missing-page" in item for item in got), "missing name " + " | ".join(got))
        check(named.read_bytes() == named_bytes, "name lint wrote nothing")
        missed = lint_case(
            "lint-0160",
            "05.01.draft.md",
            lint_body(extra="recommend: Fix 0160.structure-door.temp in the note.\n"),
        )
        got = lint_reasons(missed)
        check(any("0160.structure-door.temp" in item for item in got), "missing temp name")
        forbidden_pack = lint_case(
            "lint-forbid",
            "05.01.draft.md",
            lint_body(extra="path: 00.kernel/00.00.01.law/\n"),
        )
        got = lint_reasons(forbidden_pack)
        check(any(item.startswith("forbidden:") and "00.kernel" in item for item in got), "forbidden kernel")
        checked = lint_case(
            "lint-check",
            "05.01.draft.md",
            lint_body(extra="path: 00.00.00.kernel/00.00.01.law/\n"),
        )
        got = lint_reasons(checked)
        check(any(item.startswith("forbidden:") and "00.00.00.kernel" in item for item in got), "forbidden check kernel")
        law_pack = lint_case(
            "lint-law",
            "05.01.draft.md",
            lint_body(extra="path: 00.00.00.kernel.draft/made/\n"),
        )
        (law_pack.parent.parent / "00.00.00.kernel.draft" / "made").mkdir(parents=True)
        got = lint_reasons(law_pack)
        check(got == [], "draft law path " + " | ".join(got))
        decision = lint_case(
            "lint-decide",
            "05.01.draft.md",
            lint_body(do="Ask the Director to pick a title."),
        )
        got = lint_reasons(decision)
        check("decision: issue is missing" in got and "decision: options are missing" in got, "decision pack")
        check("decision: effects are missing" in got, "decision effects")
        owned = lint_case("lint-own", "05.01.draft.md", lint_body(do="Promote the approved seat."))
        check("must-not-own: promotes an approved seat" in lint_reasons(owned), "promote seat")
        book_choice = lint_case(
            "lint-book",
            "05.01.draft.md",
            lint_body(do="Decide which law book is the seat."),
        )
        check("must-not-own: decides the law book" in lint_reasons(book_choice), "law book choice")
        negated = lint_case(
            "lint-not",
            "05.01.draft.md",
            lint_body(
                do="Do not promote an approved seat. Do not decide which law book is the seat."
            ),
        )
        got = lint_reasons(negated)
        check(not any(item.startswith("must-not-own:") for item in got), "negated own " + " | ".join(got))
        closed = lint_case("lint-noret", "05.01.md", lint_body(state="closed"))
        got = lint_reasons(closed)
        check(any(item.startswith("return:") for item in got), "closed needs a return " + " | ".join(got))
        returned = lint_body(state="closed").replace(
            "state: closed\n",
            "state: closed\nreturn: 0117.pack-lint/05.01.return.md\n",
            1,
        )
        returned_path = lint_case("lint-ret", "05.01.md", returned)
        (returned_path.parent.parent / "0117.pack-lint" / "05.01.return.md").write_bytes(
            b"# 05.01\n\nDid: yes\nBlocked: none\nNeed: none\n\n#01 >build work\n"
        )
        (returned_path.parent / "05.02.md").write_bytes(b"# 05.02\n")
        got = lint_reasons(returned_path)
        check(got == [], "closed lint " + " | ".join(got))
        check(returned_path.read_bytes() == returned.encode("utf-8"), "closed lint wrote nothing")
        skipped = lint_case("lint-next", "05.03.draft.md", lint_body(nn="03"))
        check("number: 05.03 is not the next number" in lint_reasons(skipped), "draft not next")
        sequenced = lint_case("lint-seq", "05.02.draft.md", lint_body(nn="02"))
        (sequenced.parent / "05.01.md").write_bytes(b"# 05.01\n")
        got = lint_reasons(sequenced)
        check(got == [], "draft is next " + " | ".join(got))
        pointed = lint_body().replace(
            "Read first: 0417.pack-lint/01.md and 0417.pack-lint/06.01.md.\n",
            "Read first: 0117.pack-lint/05.01.return.md Overflow.\n",
        )
        pointed_path = lint_case("lint-over", "05.01.draft.md", pointed)
        (pointed_path.parent.parent / "0117.pack-lint" / "05.01.return.md").write_bytes(b"Did: x\n")
        got = lint_reasons(pointed_path)
        check(got == [], "read-first section " + " | ".join(got))
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(clean)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 0 and ran.stdout.splitlines()[0] == "pass", "lint command passes")
        check("request: promote" in ran.stdout, "lint pass requests promote")
        check("note: 0517.pack-lint/06.01.md" in ran.stdout, "note on the pack page")
        check(clean.read_bytes() == clean_bytes, "lint command left the bytes")
        check(clean.name == "05.01.draft.md", "lint left the draft name")
        check(not (clean.parent / "05.01.pack.md").exists(), "lint did not pack")
        page_note = (clean.parent / "06.01.md").read_text(encoding="utf-8")
        check("request: promote" in page_note, "pack-page note requests promote")
        check("0517.pack-lint/05.01.draft.md" in page_note, "pack-page note names the pack")
        check("state: ready" not in page_note, "note is not ready")
        check(b"\r" not in (clean.parent / "06.01.md").read_bytes(), "pack-page note is LF")
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(clean)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 0 and "note: 0517.pack-lint/06.01.md" in ran.stdout, "same pack-page note")
        check(not (clean.parent / "06.02.md").exists(), "no second pack-page note")
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(named)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 1 and "fail: names:" in ran.stdout, "lint command fails")
        check("request: promote" not in ran.stdout, "fail raises no request")
        check(named.read_bytes() == named_bytes, "lint fail left the bytes")
        fail_note = (named.parent / "06.01.md").read_text(encoding="utf-8")
        check("reason:" in fail_note and "0199.missing-page" in fail_note, "fail writes the reason")
        check("request: promote" not in fail_note, "fail note has no request")
        check("The file stays." in fail_note, "fail leaves the file")
        queued = lint_case("lint-queue", "05.01.draft.md", lint_body())
        qdir = queued.parent.parent / "0415.queue"
        qdir.mkdir()
        (qdir / "06.02.md").write_bytes(b"# 06.02\n")
        (qdir / "06.24.md").write_bytes(b"# 06.24\n")
        q_bytes = queued.read_bytes()
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(queued)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 0 and "request: promote" in ran.stdout, "queue request")
        check("note: 0415.queue/06.25.md" in ran.stdout, "queue note number")
        check(queued.read_bytes() == q_bytes, "queue lint left the draft")
        check("state: draft" in queued.read_text(encoding="utf-8"), "queue lint left state draft")
        check(not (queued.parent / "05.01.pack.md").exists(), "queue lint did not pack")
        check(not (queued.parent / "06.01.md").exists(), "queue lint did not note the pack page")
        queue_note = (qdir / "06.25.md").read_text(encoding="utf-8")
        check("request: promote" in queue_note, "queue note requests promote")
        check("0517.pack-lint/05.01.draft.md" in queue_note, "queue note names the pack")
        check("does not mark the pack ready" in queue_note, "queue note leaves ready to the Director")
        check(b"\r" not in (qdir / "06.25.md").read_bytes(), "queue note is LF")
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(queued)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 0 and "note: 0415.queue/06.25.md" in ran.stdout, "same queue note")
        check(not (qdir / "06.26.md").exists(), "no second queue note")
        bad = lint_case(
            "lint-qfail",
            "05.01.draft.md",
            lint_body(extra="path: 0199.missing-page/01.md\n"),
        )
        bdir = bad.parent.parent / "0415.queue"
        bdir.mkdir()
        bad_bytes = bad.read_bytes()
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(bad)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(ran.returncode == 1 and "fail: names:" in ran.stdout, "queue fail")
        check("request: promote" not in ran.stdout, "queue fail has no request")
        bad_note = (bdir / "06.01.md").read_text(encoding="utf-8")
        check("reason:" in bad_note and "0199.missing-page" in bad_note, "queue fail writes the reason")
        check("request: promote" not in bad_note, "queue fail note has no request")
        check(bad.read_bytes() == bad_bytes, "queue fail left the bytes")
        check(not (bad.parent / "05.01.pack.md").exists(), "queue fail did not pack")
        kbook = root / "00.kernel" / "book"
        kdec = kbook / "0417.pack-lint"
        kdec.mkdir(parents=True)
        (kdec / "01.md").write_bytes(b"# 01\n")
        (kdec / "06.01.md").write_bytes(b"# 06.01\n")
        kfolder = kbook / "0517.pack-lint"
        kfolder.mkdir()
        kpack = kfolder / "05.01.draft.md"
        kpack.write_bytes(lint_body().encode("utf-8"))
        kraw = kpack.read_bytes()
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(kpack)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        kshown = (ran.stdout or "") + (ran.stderr or "")
        check(ran.returncode != 0 and "the kernel is not edited" in kshown, "00.kernel note stops")
        check(kpack.read_bytes() == kraw, "00.kernel pack stayed")
        check(list(kfolder.glob("06.*.md")) == [], "00.kernel note absent")
        cbook = root / CHECK_KERNEL / "book"
        cdec = cbook / "0417.pack-lint"
        cdec.mkdir(parents=True)
        (cdec / "01.md").write_bytes(b"# 01\n")
        (cdec / "06.01.md").write_bytes(b"# 06.01\n")
        cfolder = cbook / "0517.pack-lint"
        cfolder.mkdir()
        cpack = cfolder / "05.01.draft.md"
        cpack.write_bytes(lint_body().encode("utf-8"))
        craw = cpack.read_bytes()
        ran = subprocess.run(
            [sys.executable, clerk, "lint", str(cpack)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        cshown = (ran.stdout or "") + (ran.stderr or "")
        check(ran.returncode != 0 and "the check kernel is closed" in cshown, "check kernel note stops")
        check(cpack.read_bytes() == craw, "check kernel pack stayed")
        check(list(cfolder.glob("06.*.md")) == [], "check kernel note absent")
        missing_pack = subprocess.run(
            [sys.executable, clerk, "lint", str(root / "no-such-pack.md")],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        missing_shown = (missing_pack.stdout or "") + (missing_pack.stderr or "")
        check(missing_pack.returncode != 0 and "pack is missing" in missing_shown, "missing pack stops")
        live_q = repo / "10.workshop/10.10.work/10.10.12.rebuild/0415.queue"
        live_q_after = sorted(p.name for p in live_q.iterdir()) if live_q.is_dir() else []
        check(live_q_after == live_q_before, "live queue gained no note")
    print("cold: pass")
    print("test: pass")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clerk.py", description="Place a section on a face. Does not sign.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    drop_cmd = sub.add_parser("drop")
    drop_cmd.add_argument("face", type=Path)
    drop_cmd.add_argument("--heading", required=True)
    drop_cmd.add_argument("--body-file", type=Path, required=True)
    drop_cmd.add_argument("--who", default="grok-prime")
    draft_cmd = sub.add_parser("draft")
    draft_cmd.add_argument("seat", type=Path)
    draft_cmd.add_argument("--from", dest="source", type=Path, default=None)
    draft_cmd.add_argument("--who", default="grok-prime")
    derive_cmd = sub.add_parser("derive")
    derive_cmd.add_argument("draft", type=Path)
    derive_cmd.add_argument("--who", default="grok-prime")
    revise_cmd = sub.add_parser("revise")
    revise_cmd.add_argument("face", type=Path)
    revise_cmd.add_argument("--old", required=True)
    revise_cmd.add_argument("--new", required=True)
    revise_cmd.add_argument("--who", default="grok-prime")
    versions_cmd = sub.add_parser("versions")
    versions_cmd.add_argument("page", type=Path)
    import_cmd = sub.add_parser("import")
    import_cmd.add_argument("page", type=Path)
    import_cmd.add_argument("--from", dest="source", type=Path, required=True)
    import_cmd.add_argument("--who", default="grok-prime")
    seat_cmd = sub.add_parser("seat")
    seat_cmd.add_argument("page", type=Path)
    seat_cmd.add_argument("--from", dest="source", type=Path, required=True)
    seat_cmd.add_argument("--who", default="grok-prime")
    live_cmd = sub.add_parser("live")
    live_cmd.add_argument("book", type=Path)
    live_cmd.add_argument("--last", default=None)
    live_cmd.add_argument("--when", default=None)
    live_cmd.add_argument("--goal", default=None)
    live_cmd.add_argument("--pages", default=None)
    live_cmd.add_argument("--who", default="grok-prime")
    lint_cmd = sub.add_parser("lint")
    lint_cmd.add_argument("pack", type=Path)
    sub.add_parser("test")
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.cmd == "drop":
        cmd_drop(args.face, args.heading, args.body_file, args.who)
    elif args.cmd == "draft":
        cmd_draft(args.seat, args.who, args.source)
    elif args.cmd == "derive":
        cmd_derive(args.draft, args.who)
    elif args.cmd == "revise":
        cmd_revise(args.face, args.old, args.new, args.who)
    elif args.cmd == "versions":
        cmd_versions(args.page)
    elif args.cmd == "import":
        cmd_import(args.page, args.source, args.who)
    elif args.cmd == "seat":
        cmd_seat(args.page, args.source, args.who)
    elif args.cmd == "live":
        cmd_live(args.book, args.last, args.when, args.goal, args.pages)
    elif args.cmd == "lint":
        cmd_lint(args.pack)
    elif args.cmd == "test":
        cmd_test()


if __name__ == "__main__":
    main()
