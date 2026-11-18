#!/usr/bin/env python3
"""Pinned front door for source/pass return access.

The declaration is app/return-lines-v2.json. librarian.py loads this module
for the return-lines command only. Status, lookup, and verify are read-only.
Reserve and capture forward to pinned pass03 on a declared line-pass book.
A return is not acceptance. Legacy writer closure is not established.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "return-lines-pins/1"
VERSION = 1
DECLARATION_NAME = "return-lines-v2.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "adapter", "backend", "pass02", "pass01", "placement", "reader"}
FILE_KEYS = {"path", "sha256", "bytes"}
ADAPTER = {
    "path": "labs/return-access-pass01/return_access.py",
    "sha256": "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5",
    "bytes": 26561,
}
BACKEND = {
    "path": "labs/return-lines-pass03/return_lines.py",
    "sha256": "78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63",
    "bytes": 33349,
}
PASS02 = {
    "path": "labs/return-lines-pass02/return_lines.py",
    "sha256": "6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908",
    "bytes": 82908,
}
PASS01 = {
    "path": "labs/return-lines-pass01/return_lines.py",
    "sha256": "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a",
    "bytes": 100897,
}
PLACEMENT = {
    "path": "labs/return-placement-pass01/return_placement.py",
    "sha256": "db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754",
    "bytes": 66097,
}
READER = {
    "path": "labs/return-capture-pass01/return_capture.py",
    "sha256": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    "bytes": 45767,
}
FILES = {
    "adapter": ADAPTER,
    "backend": BACKEND,
    "pass02": PASS02,
    "pass01": PASS01,
    "placement": PLACEMENT,
    "reader": READER,
}
READ_COMMANDS = {"status", "lookup", "verify"}
WRITE_COMMANDS = {"reserve", "capture"}
COMMANDS = READ_COMMANDS | WRITE_COMMANDS
BANNED = (
    "--adapter",
    "--allow-live",
    "--backend",
    "--designate",
    "--executable",
    "--force",
    "--lines",
    "--module",
    "--pins",
    "--python",
    "--reader",
    "--tool",
)
AUTH_FLAGS = ("--authorization", "--audit", "--plan", "--backup", "--staging", "--retired")
BANDS = {"5": "matched-workflow-return-line", "7": "page-local-colab"}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def ancestor_is_linked(path: Path) -> bool:
    current = path
    while True:
        parent = current.parent
        if parent == current:
            return False
        try:
            os.lstat(parent)
        except FileNotFoundError:
            return False
        if is_link(parent):
            return True
        current = parent


def pin_file(code_root: Path, spec: dict) -> Path:
    rel = spec["path"]
    current = code_root
    if is_link(current):
        refuse("code root is linked and was not followed")
    for part in rel.split("/"):
        current = current / part
        if is_link(current):
            refuse("tool path is linked and was not followed")
    if not current.is_file():
        refuse(f"pinned tool is missing: {rel}")
    raw = current.read_bytes()
    if hashlib.sha256(raw).hexdigest() != spec["sha256"] or len(raw) != spec["bytes"]:
        refuse(f"pinned tool hash does not match: {rel}")
    return current


def load_declaration(code_root: Path) -> None:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if is_link(app_dir) or is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("return-lines declaration is missing")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("return-lines declaration is not utf-8")
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("return-lines declaration is not strict json")
    if not isinstance(document, dict) or set(document) != TOP_KEYS:
        refuse("return-lines declaration does not match the pinned tools")
    if document["schema"] != SCHEMA or document["version"] != VERSION:
        refuse("return-lines declaration does not match the pinned tools")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("return-lines declaration does not match the pinned tools")
    for key, spec in FILES.items():
        item = document[key]
        if not isinstance(item, dict) or set(item) != FILE_KEYS or item != spec:
            refuse("return-lines declaration does not match the pinned tools")
        pin_file(code_root, spec)


def book_argument(args: list[str]) -> str:
    found = None
    index = 0
    while index < len(args):
        token = args[index]
        if token in BANNED or any(token.startswith(prefix + "=") for prefix in BANNED):
            refuse("backend override is refused")
        if token == "--book":
            if index + 1 >= len(args) or args[index + 1].startswith("--"):
                refuse("missing value for --book")
            if found is not None:
                refuse("repeated --book")
            found = args[index + 1]
            index += 2
            continue
        index += 1
    if found is None:
        refuse("missing --book")
    return found


def refuse_linked_book(text: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        refuse("book root is empty")
    if text.startswith("\\\\") or text.startswith("//"):
        refuse("UNC path book root")
    path = Path(text)
    if not path.is_absolute():
        refuse("book root must be absolute")
    if ".." in path.parts:
        refuse("unsafe path book root")
    if is_link(path) or not path.exists() or not path.is_dir():
        refuse("book root is not a directory")
    if ancestor_is_linked(path):
        refuse("book root ancestor is linked and was not followed")
    return path


def live_book(code_root: Path) -> Path:
    return code_root / "00.kernel" / "00.00.10.work"


def is_live(book: Path, code_root: Path) -> bool:
    return os.path.normcase(os.path.abspath(book)) == os.path.normcase(os.path.abspath(live_book(code_root)))


def require_line_pass(book: Path) -> None:
    door = book / "0100.band.returns"
    layout_path = book / "return-line-layout.json"
    if is_link(door) or is_link(layout_path) or not door.exists() or not layout_path.is_file():
        refuse("book is not a declared line-pass book")
    try:
        document = json.loads(layout_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        refuse("book is not a declared line-pass book")
    if not isinstance(document, dict):
        refuse("book is not a declared line-pass book")
    if document.get("allocation") != "line-pass" or document.get("sequential_allocation") is not False:
        refuse("book is not a declared line-pass book")
    if document.get("bands") != BANDS:
        refuse("book is not a declared line-pass book")


def require_authority(args: list[str]) -> None:
    for flag in AUTH_FLAGS:
        if args.count(flag) != 1:
            refuse("authorization is required")


def launch(script: Path, args: list[str], code_root: Path) -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(script), *args],
            cwd=code_root,
            shell=False,
            capture_output=True,
            env=env,
        )
    except OSError as exc:
        refuse(f"pinned return tool could not start: {exc.strerror or exc}")
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    if type(result.returncode) is not int:
        refuse("pinned return tool returned no exit code")
    return result.returncode


def perform(args: list[str], code_root: Path) -> int:
    load_declaration(code_root)
    if not args or args[0] not in COMMANDS:
        refuse("command is not on this door")
    command = args[0]
    book = refuse_linked_book(book_argument(args[1:]))
    if command in WRITE_COMMANDS:
        if is_live(book, code_root):
            refuse("canonical live book is refused")
        require_line_pass(book)
        require_authority(args[1:])
        script = pin_file(code_root, BACKEND)
    else:
        script = pin_file(code_root, ADAPTER)
    return launch(script, args, code_root)
