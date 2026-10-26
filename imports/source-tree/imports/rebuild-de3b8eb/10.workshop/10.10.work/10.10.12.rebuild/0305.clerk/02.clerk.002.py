#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 001
# Authorization: draft — 2026-10-18
# who: grok-builder
# state: draft
# Face: 02
# PPPP: 0305
# desk: 10.workshop
# shelf: 10.10.work
# book: 10.10.12.rebuild
# keyword: clerk
# why: The clerk, ported unchanged from the lib tool.
#
# cite: 3.1
# source path: 10.workshop/10.10.work/10.10.10.lib/code/clerk.py
# source hash: 12fcdba73fe4651431f30ee7dd745f1c8db56b12ca907d4af4f014023120b7c1
"""clerk.py — place a section on a face.

jobs.py places batches. This places face pieces.
It does not sign, approve, or promote.

Now: stamp, drop, draft, derive, and revise.
Dev mode writes kernel.draft. The check kernel stays closed.
Later, in this same program: cite, and the gate.
Clerk mode reads 00.00.00.kernel and does not write a face.

A seated face is FF.md. Version 001 is also FF.md. A later draft is FF.VVV.md.
A .draft tail stops. FF.001.md stops. Empty version counts as 001.
draft copies the seat, applies the notes on 06, and leaves the seat unchanged.
It reads CRLF and writes LF. It stores one source block.
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

from __future__ import annotations

import argparse
import hashlib
import os
import re
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


def revise(face: Path, old: str, new: str, who: str) -> str:
    guarded(face)
    kind, _number, _ver = face_ref(face)
    if old == "":
        die("sentence is empty")
    if not face.is_file():
        die("face is missing")
    existing = read_face(face)
    if kind == "draft" and not existing:
        die("a draft is a copy of the seat")
    refuse_settled(existing, kind)
    count = existing.count(old)
    if count == 0:
        die("sentence is missing")
    if count > 1:
        die("sentence is there twice")
    text = existing.replace(old, new, 1)
    day = date.today().isoformat()
    note = (
        f"## Note — revise {day}\n\n"
        f"born: {day}\n"
        f"source: {who}\n\n"
        f"{old.rstrip()}\n"
    )
    header, sections, trailer = split_document(text)
    sections.append((f"Note — revise {day}", note + "\n"))
    face.write_bytes(join_document(header, sections, trailer).encode("utf-8"))
    return "revised"


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
    elif args.cmd == "test":
        cmd_test()


if __name__ == "__main__":
    main()
