#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""timer.py — name, start, status, stop, and record one timer page.

The page address is given. Face 01 holds the duration and the state.
A stood face keeps its text. name writes the timer onto it.
The record is a note this program writes.
It lives on the test desk. A later pack can seat it on 03NN.
"""
# born: 2026-10-21
# source: director, >run.0514.05.03, and 0414.test-desk/06.03.md
# who: grok-builder
# Commands are name, start, status, stop, and record.
# The address is the page the caller names. slot.py next is not used.
# Face 07 stays empty. Face 01 of the named page holds the timer.
# born: 2026-10-21
# source: director, >run.0514.05.05, and 0414.test-desk/06.04.md
# who: grok-builder
# name keeps a stood face 01.
# It writes the duration and the state onto that face.
# A stood page is not refused.

from __future__ import annotations

import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

CODE = None
_here = Path(__file__).resolve()
for _cand in (_here.parent, *_here.parents):
    _code = _cand / "10.10.11.solo-kernel" / "code"
    if not (_code / "face.py").is_file():
        _code = _cand / "10.workshop" / "10.10.work" / "10.10.11.solo-kernel" / "code"
    if (_code / "face.py").is_file():
        CODE = _code
        break
if CODE is None:
    sys.exit("stop: face.py is missing")
sys.path.insert(0, str(CODE))

from desk import need  # noqa: E402
from face import EM, die, kind_of, make_new, parse_name, refuse_kernel_write  # noqa: E402

KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.-]*$")
DUR_RE = re.compile(r"^[1-9]\d*[smh]$")
COPY_BOOKS = {"00.00.01.law", "00.00.00.syntax"}
FACE = "01.md"


def refuse_copy(path: Path) -> None:
    refuse_kernel_write(path)
    names = {path.name, *(parent.name for parent in path.parents)}
    if names & COPY_BOOKS:
        die("a page is not minted in this book")


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if b"\r" in raw:
        die("face file is not LF")
    return raw.decode("utf-8")


def write_text(path: Path, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    path.write_bytes(text.encode("utf-8"))


def split_timer(text: str) -> tuple[str, str]:
    mark = "## Timer"
    if mark not in text:
        die("timer face is missing")
    head, section = text.split(mark, 1)
    return head, section


def section_field(section: str, key: str) -> str:
    match = re.search(rf"(?m)^{key}:[ \t]*(.*)$", section)
    if not match or not match.group(1).strip():
        die(f"{key} is missing")
    return match.group(1).strip()


def set_section_field(section: str, key: str, value: str) -> str:
    updated, count = re.subn(
        rf"(?m)^{key}:[ \t]*.*$",
        f"{key}: {value}",
        section,
        count=1,
    )
    if count != 1:
        die(f"{key} is missing")
    return updated


def header_value(head: str, key: str) -> str:
    match = re.search(rf"(?m)^{key}:[ \t]*(.*)$", head)
    return match.group(1).strip() if match else ""


def face_file(page: Path) -> Path:
    if not page.is_dir():
        die("page folder is missing")
    path = page / FACE
    if not path.is_file():
        die("timer face is missing")
    return path


def load(page: Path) -> tuple[Path, str, str]:
    path = face_file(page)
    head, section = split_timer(read_text(path))
    return path, head, section


def save(path: Path, head: str, section: str) -> None:
    write_text(path, head + "## Timer" + section)


def timer_state(section: str) -> str:
    return section_field(section, "state")


def require_state(section: str, want: str) -> None:
    got = timer_state(section)
    if got != want:
        die(f"state is {got}")


def page_ok(page: Path) -> None:
    refuse_copy(page)
    if page.exists() and not page.is_dir():
        die("page path is not a folder")
    match = re.fullmatch(r"(\d{4})\.(.+)", page.name)
    if not match:
        die("page address is PPPP.keyword")
    if not KEY_RE.fullmatch(match.group(2)):
        die("title needs a word")
    book = page.parent
    if not book.is_dir():
        die("book folder is missing")
    book_name = parse_name(book.name)
    if not book_name or kind_of(book_name[0]) != "book":
        die("page has no book folder")
    number = match.group(1)
    for child in book.iterdir():
        if child.is_dir() and child.name.startswith(number + ".") and child != page:
            die("number is taken")


def prepare(page: Path) -> bool:
    """Create the folder when it is missing. Return whether this call created it."""
    page_ok(page)
    created = not page.exists()
    if created:
        page.mkdir()
    if (page / FACE).exists():
        die("a face is already here")
    return created


def add_timer(page: Path, duration: str) -> None:
    """Write the duration and the state onto a face that is already here."""
    path = page / FACE
    text = read_text(path)
    if "## Timer" in text:
        die("a timer is already here")
    if not text.endswith("\n"):
        text += "\n"
    if not text.endswith("\n\n"):
        text += "\n"
    write_text(path, text + f"## Timer\n\nduration: {duration}\nstate: named\n")


def name_timer(page: Path, duration: str, who: str, why: str, cite: str) -> None:
    if not DUR_RE.fullmatch(duration):
        die("duration needs a number and a unit")
    if not who.strip() or not why.strip() or not cite.strip():
        die("who, why, and cite are required")
    page_ok(page)
    if (page / FACE).is_file():
        add_timer(page, duration)
        return
    created = False
    try:
        created = prepare(page)
        body = f"## Timer\n\nduration: {duration}\nstate: named\n"
        make_new(page, "01", who, why, cite, body)
    except SystemExit:
        made = page / FACE
        if made.is_file() and created:
            made.unlink()
        if created and page.is_dir() and not any(page.iterdir()):
            page.rmdir()
        raise


def start_timer(page: Path) -> None:
    path, head, section = load(page)
    require_state(section, "named")
    save(path, head, set_section_field(section, "state", "running"))


def status_timer(page: Path) -> tuple[str, str]:
    _path, _head, section = load(page)
    return section_field(section, "duration"), timer_state(section)


def stop_timer(page: Path) -> None:
    path, head, section = load(page)
    require_state(section, "running")
    save(path, head, set_section_field(section, "state", "stopped"))


def next_note(page: Path) -> str:
    nums = []
    for path in page.iterdir():
        match = re.fullmatch(r"06\.(\d{2})\.md", path.name)
        if match:
            nums.append(int(match.group(1)))
    nxt = (max(nums) + 1) if nums else 1
    if nxt > 99:
        die("no note number left")
    return f"{nxt:02d}"


def record_exists(page: Path) -> bool:
    for path in page.iterdir():
        if re.fullmatch(r"06\.\d{2}\.md", path.name) and "## Record" in read_text(path):
            return True
    return False


def record_timer(page: Path) -> tuple[str, str]:
    _path, head, section = load(page)
    require_state(section, "stopped")
    if record_exists(page):
        die("a record is already here")
    nn = next_note(page)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = section_field(section, "duration")
    rows = ["desk", "shelf", "book"]
    lines = [
        f"# 06.{nn}",
        "",
        f"Authorization: draft {EM} {stamp[:10]}",
        f"who: {header_value(head, 'who') or 'grok-builder'}",
        f"created: {stamp}",
        f"written: {stamp}",
        "state: draft",
        f"task: {nn}",
        "Face: 06",
        f"PPPP: {header_value(head, 'PPPP')}",
    ]
    for key in rows:
        value = header_value(head, key)
        if value:
            lines.append(f"{key}: {value}")
    lines.extend([
        f"keyword: {header_value(head, 'keyword')}",
        "why: Record of the timer run.",
        "",
        f"cite: {header_value(head, 'cite') or '3.1'}",
        "",
        "## Record",
        "",
        f"duration: {duration}",
        "state: stopped",
        f"page: {page.name}",
        "",
    ])
    dest = page / f"06.{nn}.md"
    write_text(dest, "\n".join(lines))
    return dest.name, duration


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / "10.10.99.trial"
        book.mkdir(parents=True)
        (book / "0109.open").mkdir()
        page = book / "0114.held"
        name_timer(page, "25m", "grok-builder", "A timer.", "3.1")
        check(page.name == "0114.held", "named address")
        check(not (book / "0115.held").exists(), "no next slot")
        text = read_text(page / FACE)
        head, section = split_timer(text)
        check("state: draft" in head, "face stays draft")
        check(section_field(section, "duration") == "25m", "duration")
        check(timer_state(section) == "named", "state named")
        start_timer(page)
        _path, head, section = load(page)
        check("state: draft" in head and timer_state(section) == "running", "state running")
        try:
            start_timer(page)
            die("test started twice")
        except SystemExit as exc:
            check("state is running" in str(exc), "second start stops")
        stop_timer(page)
        _path, head, section = load(page)
        check("state: draft" in head and timer_state(section) == "stopped", "state stopped")
        try:
            start_timer(page)
            die("test restarted a stopped run")
        except SystemExit as exc:
            check("state is stopped" in str(exc), "stopped stays stopped")
        record_timer(page)
        note = page / "06.01.md"
        check(note.is_file(), "record note")
        noted = read_text(note)
        check("## Record" in noted and "duration: 25m" in noted and "state: stopped" in noted, "note body")
        check(timer_state(split_timer(read_text(page / FACE))[1]) == "stopped", "face stays stopped")
        try:
            record_timer(page)
            die("test recorded twice")
        except SystemExit as exc:
            check("a record is already here" in str(exc), "second record stops")
        try:
            name_timer(page, "10m", "grok-builder", "A timer.", "3.1")
            die("test wrote over a face")
        except SystemExit as exc:
            check("a timer is already here" in str(exc), "second name stops")
        try:
            name_timer(book / "0114.other", "10m", "grok-builder", "A timer.", "3.1")
            die("test reused a number")
        except SystemExit as exc:
            check("number is taken" in str(exc), "number stays taken")
            check(not (book / "0114.other").exists(), "no twin folder")
        try:
            name_timer(book / "0116.held", "25", "grok-builder", "A timer.", "3.1")
            die("test accepted a bare number")
        except SystemExit as exc:
            check("duration needs a number and a unit" in str(exc), "bare duration stops")
            check(not (book / "0116.held").exists(), "no folder for a bad duration")
        stood = book / "0117.stood"
        stood.mkdir()
        stood_body = "# 01\n\nversion: 001\nstate: draft\nwho: grok-builder\n\n## Difference\n\nThe stood page.\n"
        (stood / FACE).write_bytes(stood_body.encode("utf-8"))
        custody = b"# 08\n\n## Relationships\n\nthis: 0117.stood\n"
        (stood / "08.md").write_bytes(custody)
        name_timer(stood, "25m", "grok-builder", "A timer.", "3.1")
        stood_text = read_text(stood / FACE)
        stood_head, stood_section = split_timer(stood_text)
        check("## Difference" in stood_head and "The stood page." in stood_head, "stood body stays")
        check("state: draft" in stood_head, "stood header stays draft")
        check(section_field(stood_section, "duration") == "25m", "stood duration")
        check(timer_state(stood_section) == "named", "stood state named")
        check((stood / "08.md").read_bytes() == custody, "custody stays")
        try:
            name_timer(stood, "10m", "grok-builder", "A timer.", "3.1")
            die("test named a stood timer twice")
        except SystemExit as exc:
            check("a timer is already here" in str(exc), "second stood name stops")
        check("duration: 25m" in read_text(stood / FACE), "stood duration stays")
        plain = book / "0118.plain"
        plain.mkdir()
        plain_body = b"# 01\n\nstate: draft\n\n## Difference\n\nPlain.\n"
        (plain / FACE).write_bytes(plain_body)
        try:
            name_timer(plain, "25", "grok-builder", "A timer.", "3.1")
            die("test accepted a bare number on a stood face")
        except SystemExit as exc:
            check("duration needs a number and a unit" in str(exc), "stood bare duration stops")
            check((plain / FACE).read_bytes() == plain_body, "bad duration leaves the face")
        blocked = root / "00.00.00.kernel.draft" / "00.00.99.law"
        blocked.mkdir(parents=True)
        kept = blocked / "0114.kept"
        kept.mkdir()
        kept_body = b"# 01\n\nstate: draft\n\n## Difference\n\nStay.\n"
        (kept / FACE).write_bytes(kept_body)
        try:
            name_timer(kept, "25m", "grok-builder", "A timer.", "3.1")
            die("test wrote on a kernel face")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel face stops")
            check((kept / FACE).read_bytes() == kept_body, "kernel face stays")
        try:
            name_timer(blocked / "0114.nope", "25m", "grok-builder", "A timer.", "3.1")
            die("test wrote in the kernel")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel path stops")
            check(not (blocked / "0114.nope").exists(), "no kernel folder")
    print("test: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, name PAGE DURATION, start PAGE, status PAGE, stop PAGE, or record PAGE")
    cmd = args[0]
    if cmd == "test":
        cmd_test()
        return
    if cmd == "name":
        if len(args) < 8 or any(flag not in args for flag in ("--who", "--why", "--cite")):
            die("name PAGE DURATION --who TEXT --why TEXT --cite TEXT")
        page = Path(args[1])
        duration = args[2]
        name_timer(page, duration, need(args, "--who"), need(args, "--why"), need(args, "--cite"))
        print(f"named: {page.name}")
        print(f"duration: {duration}")
        print("state: named")
        print(f"face: {FACE}")
        return
    if cmd in ("start", "status", "stop", "record"):
        if len(args) < 2:
            die(f"{cmd} PAGE")
        page = Path(args[1])
        if cmd == "start":
            start_timer(page)
            print(f"started: {page.name}")
            print("state: running")
        elif cmd == "status":
            duration, state = status_timer(page)
            print(f"duration: {duration}")
            print(f"state: {state}")
        elif cmd == "stop":
            stop_timer(page)
            print(f"stopped: {page.name}")
            print("state: stopped")
        else:
            noted, duration = record_timer(page)
            print(f"noted: {noted}")
            print(f"duration: {duration}")
            print("state: stopped")
        return
    die("use test, name PAGE DURATION, start PAGE, status PAGE, stop PAGE, or record PAGE")


if __name__ == "__main__":
    main()
