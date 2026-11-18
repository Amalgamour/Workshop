#!/usr/bin/env python3
"""Pinned front door for the accepted recorded-boot tool.

The paths and hashes below are development wiring. They are not kernel law.
An orientation result is not authorization. A reviewer label is not authentication.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "librarian-prime-boot"
VERSION = 1
DECLARATION_NAME = "prime-boot.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256"}
TOOLS = {
    "prime_boot": {
        "path": "labs/prime-boot-pass01/prime_boot.py",
        "sha256": "54b23484f9e0812db92a623a8588175702682ebe14f8b0b915111daf51a91534",
    },
    "prime_support": {
        "path": "labs/prime-support-pass01/prime_support.py",
        "sha256": "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
    },
    "clerk_adapter": {
        "path": "labs/prime-support-pass01/clerk_adapter.py",
        "sha256": "2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4",
    },
    "check_book": {
        "path": "labs/book-orientation-pass01/check_book.py",
        "sha256": "fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4",
    },
    "return_capture": {
        "path": "labs/return-capture-pass01/return_capture.py",
        "sha256": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    },
    "return_inspect": {
        "path": "labs/return-capture-pass01/return_inspect.py",
        "sha256": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
    },
    "clerk": {
        "path": "labs/clerk-handoff-pass02/clerk.py",
        "sha256": "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c",
    },
}
COMMANDS = {
    "boot-prepare": ("prepare", ("--request", "--records", "--attempt"), ()),
    "boot-check": ("check", ("--attempt", "--answers"), ()),
    "boot-judge": ("judge", ("--attempt", "--judgement"), ()),
    "boot-show": ("show", ("--attempt",), ("--json",)),
}
DRIVE = re.compile(r"^[A-Za-z]:")
TIMEOUT_S = 180


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def refuse(message: str) -> None:
    raise Refuse(message)


def _is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    value: dict = {}
    for key, item in pairs:
        if key in value:
            refuse(f"prime boot declaration repeats {key}")
        value[key] = item
    return value


def _inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def parse_declaration(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("prime boot declaration is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("prime boot declaration is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("prime boot declaration is not strict json")
    if text[end:].strip():
        refuse("prime boot declaration is not strict json")
    if not isinstance(value, dict):
        refuse("prime boot declaration is not strict json")
    return value


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("prime boot declaration is missing")
    document = parse_declaration(path.read_bytes())
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra:
        refuse("prime boot declaration has an unknown field: " + ", ".join(extra))
    if missing:
        refuse("prime boot declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("prime boot declaration schema is not librarian-prime-boot")
    version = document["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != VERSION:
        refuse("prime boot declaration version is not 1")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("prime boot declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("prime boot declaration does not match the pinned tools")
    for name in TOOLS:
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("prime boot declaration does not match the pinned tools")
        if item["path"] != TOOLS[name]["path"] or item["sha256"] != TOOLS[name]["sha256"]:
            if isinstance(item["path"], str) and _escapes(item["path"]):
                refuse("tool path escapes the code root")
            refuse("prime boot declaration does not match the pinned tools")
        if not isinstance(item["path"], str) or not isinstance(item["sha256"], str):
            refuse("prime boot declaration does not match the pinned tools")
    return document


def _escapes(rel: str) -> bool:
    if rel == "" or "\\" in rel or rel.startswith("/") or rel.startswith("//"):
        return True
    if DRIVE.match(rel):
        return True
    for part in rel.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith("."):
            return True
    return False


def resolve_tool(code_root: Path, label: str) -> Path:
    rel = TOOLS[label]["path"]
    if _escapes(rel):
        refuse("tool path escapes the code root")
    current = code_root
    for part in rel.split("/"):
        current = current / part
        if _is_link(current):
            refuse("tool path is linked and was not followed")
    if not current.is_file():
        refuse(f"pinned tool is missing: {label}")
    if not _inside(current, code_root):
        refuse("tool path escapes the code root")
    try:
        raw = current.read_bytes()
    except OSError:
        refuse(f"pinned tool is missing: {label}")
    if hashlib.sha256(raw).hexdigest() != TOOLS[label]["sha256"]:
        refuse(f"pinned tool hash does not match: {label}")
    return current


def pin_tools(code_root: Path) -> dict[str, Path]:
    load_declaration(code_root)
    return {name: resolve_tool(code_root, name) for name in TOOLS}


def parse_call(command: str, args: list[str]) -> list[str]:
    if command not in COMMANDS:
        refuse("unknown boot command")
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    backend, required, optional = COMMANDS[command]
    values: dict[str, str] = {}
    flags: set[str] = set()
    index = 0
    while index < len(args):
        item = args[index]
        if item in optional:
            if item in flags:
                refuse(f"repeated {item}")
            flags.add(item)
            index += 1
            continue
        if item in required:
            if item in values:
                refuse(f"repeated {item}")
            if index + 1 >= len(args) or args[index + 1].startswith("--") or args[index + 1].strip() == "":
                refuse(f"missing value for {item}")
            values[item] = args[index + 1]
            index += 2
            continue
        refuse("unsupported argument")
    missing = [flag for flag in required if flag not in values]
    if missing:
        refuse(f"missing {missing[0]}")
    forwarded = [backend]
    for flag in required:
        forwarded.extend((flag, values[flag]))
    for flag in optional:
        if flag in flags:
            forwarded.append(flag)
    return forwarded


def _run(tool: Path, forwarded: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, "-B", os.fspath(tool), *forwarded]
    try:
        proc = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=TIMEOUT_S,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        refuse("pinned boot tool timed out")
    except OSError as exc:
        refuse("pinned boot tool failed to start: " + (exc.strerror or str(exc)))
    if type(proc.returncode) is not int:
        refuse("pinned boot tool returned no exit code")
    sys.stdout.buffer.write(proc.stdout)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(proc.stderr)
    sys.stderr.buffer.flush()
    return proc.returncode


def perform(command: str, args: list[str], code_root: Path) -> int:
    """Check the call, hash the seven pinned files, then run one boot command."""
    forwarded = parse_call(command, list(args))
    pinned = pin_tools(code_root)
    return _run(pinned["prime_boot"], forwarded)
