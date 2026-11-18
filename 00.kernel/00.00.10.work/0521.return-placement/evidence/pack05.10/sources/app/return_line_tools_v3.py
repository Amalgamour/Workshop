#!/usr/bin/env python3
"""Pinned front door for source/pass return access and pass04 writes.

The declaration is app/return-lines-v3.json. A later dispatcher selection
loads this module for the return-lines command. Status, lookup, and verify
launch the return-access successor. Writes launch pinned pass04.
Reserve and capture also require the exact line-pass layout.
A return is not acceptance. App selection is not this file.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "return-lines-pins/1"
VERSION = 1
DECLARATION_NAME = "return-lines-v3.json"
DECLARATION_NOTE = (
    "Pinned declaration for the 0521/05.09 return-lines successor. "
    "A later selection loads app/return_line_tools_v3.py for the return-lines command. "
    "Status, lookup, and verify launch labs/return-access-pass02/return_access.py. "
    "Writes launch labs/return-lines-pass04/return_lines.py and meet its recorded-release validator. "
    "Reserve and capture also require the exact line-pass layout. "
    "A synthetic fixture is copy evidence. This file is not app selection, release, or a live migration. "
    "Supported-route closure is prepared and is not total. No sentinel is declared."
)
REPARSE = 0x400
TOP_KEYS = {
    "schema", "version", "_note", "adapter", "backend", "pass03", "pass02", "pass01", "placement", "reader",
}
FILE_KEYS = {"path", "sha256", "bytes"}
ADAPTER = {
    "path": "labs/return-access-pass02/return_access.py",
    "sha256": "f5a62ecb90d1a2ce8739df92e7df2e399057b3c1a059ae66ce8368d3c8abb5a8",
    "bytes": 27831,
}
BACKEND = {
    "path": "labs/return-lines-pass04/return_lines.py",
    "sha256": "708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6",
    "bytes": 12124,
}
PASS03 = {
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
    "pass03": PASS03,
    "pass02": PASS02,
    "pass01": PASS01,
    "placement": PLACEMENT,
    "reader": READER,
}
READ_COMMANDS = {"status", "lookup", "verify"}
PREFLIGHT_COMMANDS = {"preflight"}
PLAN_COMMANDS = {"plan"}
ADOPT_COMMANDS = {"adopt", "adopt-resume", "rollback-adopt"}
LINE_COMMANDS = {"reserve", "capture"}
OTHER_WRITES = {
    "init",
    "stage",
    "stage-resume",
    "reconstruct",
    "reconstruct-resume",
    "publish",
    "publish-resume",
    "retire",
    "retire-resume",
    "rollback-stage",
    "rollback-publish",
    "rollback-retire",
}
COMMANDS = READ_COMMANDS | PREFLIGHT_COMMANDS | PLAN_COMMANDS | ADOPT_COMMANDS | LINE_COMMANDS | OTHER_WRITES
AUTH_COMMANDS = PREFLIGHT_COMMANDS | LINE_COMMANDS | OTHER_WRITES
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
LAYOUT_SCHEMA = "return-line-layout/1"
LAYOUT_KEYS = {"schema", "book", "allocation", "sequential_allocation", "bands"}
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


def pairs(items: list) -> dict:
    value: dict = {}
    for key, item in items:
        if key in value:
            refuse("return-lines declaration repeats a field")
        value[key] = item
    return value


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
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except Refuse:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("return-lines declaration is not strict json")
    if not isinstance(document, dict) or set(document) != TOP_KEYS:
        refuse("return-lines declaration does not match the pinned tools")
    if document["schema"] != SCHEMA or document["version"] != VERSION:
        refuse("return-lines declaration does not match the pinned tools")
    if document["_note"] != DECLARATION_NOTE:
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


def same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(os.path.abspath(left)) == os.path.normcase(os.path.abspath(right))


def inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return False
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def flag_value(args: list[str], flag: str) -> str:
    if args.count(flag) != 1:
        refuse(f"missing or repeated {flag}")
    index = args.index(flag)
    if index + 1 >= len(args) or args[index + 1].startswith("--"):
        refuse(f"missing value for {flag}")
    return args[index + 1]


def require_authority(args: list[str]) -> None:
    for flag in AUTH_FLAGS:
        if args.count(flag) != 1:
            refuse("authorization is required")


def layout_dump(body: dict) -> bytes:
    text = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return (text + "\n").encode("utf-8")


def layout_pairs(items: list) -> dict:
    value: dict = {}
    for key, item in items:
        if key in value:
            refuse("layout is not an accepted line-pass declaration")
        value[key] = item
    return value


def require_line_pass(book: Path) -> None:
    door = book / "0100.band.returns"
    layout_path = book / "return-line-layout.json"
    if is_link(door) or not door.exists() or is_link(layout_path) or not layout_path.is_file():
        refuse("book is not a declared line-pass book")
    info = os.lstat(layout_path)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        refuse("layout is not an accepted line-pass declaration")
    raw = layout_path.read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=layout_pairs)
    except Refuse:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        refuse("layout is not an accepted line-pass declaration")
    if not isinstance(document, dict) or set(document) != LAYOUT_KEYS:
        refuse("layout is not an accepted line-pass declaration")
    name = document.get("book")
    if not isinstance(name, str) or name == "" or len(name) > 4096 or any(ch in name for ch in "/\\\n\r"):
        refuse("layout is not an accepted line-pass declaration")
    expected = {
        "allocation": "line-pass",
        "bands": dict(BANDS),
        "book": name,
        "schema": LAYOUT_SCHEMA,
        "sequential_allocation": False,
    }
    if document != expected or raw != layout_dump(expected):
        refuse("layout is not an accepted line-pass declaration")


def require_plan_out(args: list[str], book: Path, code_root: Path) -> None:
    text = flag_value(args, "--out")
    path = Path(text)
    if not path.is_absolute():
        refuse("plan output must be an absolute path outside the book")
    if same_path(path, book) or inside(path, book):
        refuse("plan output must be an absolute path outside the book")
    live = live_book(code_root)
    if same_path(path, live) or inside(path, live):
        refuse("plan output must be an absolute path outside the live book")


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
    if command in ADOPT_COMMANDS:
        return launch(pin_file(code_root, BACKEND), args, code_root)
    book = refuse_linked_book(book_argument(args[1:]))
    if command in READ_COMMANDS:
        return launch(pin_file(code_root, ADAPTER), args, code_root)
    if command in PLAN_COMMANDS:
        require_plan_out(args[1:], book, code_root)
        return launch(pin_file(code_root, BACKEND), args, code_root)
    if command in AUTH_COMMANDS:
        require_authority(args[1:])
    if command in LINE_COMMANDS:
        require_line_pass(book)
    return launch(pin_file(code_root, BACKEND), args, code_root)


def main(argv: list[str] | None = None) -> int:
    chosen = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(chosen, Path(__file__).resolve().parent.parent)
    except Refuse as exc:
        sys.stderr.write(exc.message + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
