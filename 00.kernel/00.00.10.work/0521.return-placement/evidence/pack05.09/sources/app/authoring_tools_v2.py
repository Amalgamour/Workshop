#!/usr/bin/env python3
"""Pinned front door for the authoring successor.

The declaration is app/authoring-v2.json. librarian.py loads this module for
the authoring command only. A linked ancestor of the book is refused before
the authoring module starts. A draft is not approval, release, or a return.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "authoring-pins/2"
VERSION = 2
DECLARATION_NAME = "authoring-v2.json"
REPARSE = 0x400
TOP_KEYS = {
    "schema",
    "version",
    "_note",
    "module",
    "form",
    "profiles",
    "predecessor",
    "dependency_reader",
    "dependency_set",
    "pack_checker",
}
FILE_KEYS = {"path", "sha256", "bytes"}
MODULE = {
    "path": "labs/pack-authoring-pass02/pack_author.py",
    "sha256": "345c2f79a325ace9e3c0c42847d9ba9ce626ada5be205dbdd26f195907dcf6c2",
    "bytes": 40491,
}
FORM = {
    "path": "labs/pack-authoring-pass02/forms/build-pack-v1.json",
    "sha256": "b3d18c26699674d7aa0607e491210664b31e90a63dba13860befb5409b0416ab",
    "bytes": 19453,
}
PROFILES = {
    "0423-to-0526": {
        "path": "labs/pack-authoring-pass01/profiles/0423-to-0526.json",
        "sha256": "5845d229daeff045e1422dd6b7273f5d876b287be316f1aa87d0bcaaa7a44013",
        "bytes": 1091,
    },
    "fixture-authoring": {
        "path": "labs/pack-authoring-pass01/profiles/fixture-authoring.json",
        "sha256": "026d3561814ecdfa046224ea4b828e9cb23f4036dfd6f07203a782105c0c5823",
        "bytes": 1094,
    },
}
PREDECESSOR = {
    "path": "labs/pack-authoring-pass01/pack_author.py",
    "sha256": "30908475162fe9b1a566018d217d26465151b1243bb3a8f391cb54254f3ba10c",
    "bytes": 67547,
}
READER = {
    "path": "labs/module-dependencies-pass02/depdecl.py",
    "sha256": "a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7",
    "bytes": 53693,
}
SET = {
    "path": "labs/app-dependencies-pass02/set.json",
    "sha256": "444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706",
    "bytes": 7054,
}
CHECKER = {
    "path": "labs/pack-custody-pass01/pack_check.py",
    "sha256": "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d",
    "bytes": 21563,
}
COMMANDS = {"form", "start", "add-note", "add-item", "revise", "inspect", "review", "freeze"}
BANNED = ("--template", "--executable", "--module", "--set", "--dest", "--output", "--tool", "--python", "--pins")


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
        refuse("authoring declaration is missing")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("authoring declaration is not utf-8")
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("authoring declaration is not strict json")
    if not isinstance(document, dict) or set(document) != TOP_KEYS:
        refuse("authoring declaration does not match the pinned tools")
    if document["schema"] != SCHEMA or document["version"] != VERSION:
        refuse("authoring declaration does not match the pinned tools")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("authoring declaration does not match the pinned tools")
    expected = {
        "module": MODULE,
        "form": FORM,
        "predecessor": PREDECESSOR,
        "dependency_reader": READER,
        "dependency_set": SET,
        "pack_checker": CHECKER,
    }
    for key, spec in expected.items():
        item = document[key]
        if not isinstance(item, dict) or set(item) != FILE_KEYS or item != spec:
            refuse("authoring declaration does not match the pinned tools")
    profiles = document["profiles"]
    if not isinstance(profiles, dict) or set(profiles) != set(PROFILES):
        refuse("authoring declaration does not match the pinned tools")
    for name, spec in PROFILES.items():
        item = profiles[name]
        if not isinstance(item, dict) or item != spec:
            refuse("authoring declaration does not match the pinned tools")
    for spec in (MODULE, FORM, PREDECESSOR, READER, SET, CHECKER, *PROFILES.values()):
        pin_file(code_root, spec)


def book_argument(args: list[str]) -> str | None:
    if not args or args[0] not in COMMANDS:
        refuse("unknown authoring command")
    found = None
    index = 1
    while index < len(args):
        token = args[index]
        if token in BANNED or any(token.startswith(prefix + "=") for prefix in BANNED):
            refuse("caller tool override is refused")
        if token == "--json":
            index += 1
            continue
        if not token.startswith("--"):
            refuse("unknown argument")
        if index + 1 >= len(args):
            refuse(f"missing value for {token}")
        if token == "--book":
            if found is not None:
                refuse("repeated --book")
            found = args[index + 1]
        index += 2
    return found


def refuse_linked_book(text: str) -> None:
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


def perform(args: list[str], code_root: Path) -> int:
    load_declaration(code_root)
    book = book_argument(args)
    if book is None:
        refuse("missing --book")
    refuse_linked_book(book)
    module = pin_file(code_root, MODULE)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(module), *args],
            cwd=code_root,
            shell=False,
            capture_output=True,
            env=env,
        )
    except OSError as exc:
        refuse(f"authoring module could not start: {exc.strerror or exc}")
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    if type(result.returncode) is not int:
        refuse("pinned authoring tool returned no exit code")
    return result.returncode
