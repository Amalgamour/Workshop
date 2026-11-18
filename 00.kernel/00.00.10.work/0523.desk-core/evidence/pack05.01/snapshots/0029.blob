#!/usr/bin/env python3
"""Pinned front door for the accepted read-only Prime review tool.

The paths and hashes below are development wiring. They are not kernel law.
A report or a hold check is not authority and is not a release.
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

SCHEMA = "librarian-prime-review"
VERSION = 1
DECLARATION_NAME = "prime-review.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256"}
TOOLS = {
    "prime_review": {
        "path": "labs/prime-review-pass01/prime_review.py",
        "sha256": "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0",
    },
}
COMMANDS = {
    "prime-review": "report",
    "prime-guard": "guard",
    "prime-check-next": "check-next",
}
OVERRIDE_FLAGS = (
    "--tool",
    "--module",
    "--executable",
    "--python",
    "--pins",
    "--review-tool",
    "--prime-review",
    "--checker",
)
DRAFT_FLAGS = ("--dest", "--repo", "--expect-sha256")
DRIVE = re.compile(r"^[A-Za-z]:")


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
            refuse(f"prime review declaration repeats {key}")
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
        refuse("prime review declaration is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("prime review declaration is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("prime review declaration is not strict json")
    if text[end:].strip():
        refuse("prime review declaration is not strict json")
    if not isinstance(value, dict):
        refuse("prime review declaration is not strict json")
    return value


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("prime review declaration is missing")
    document = parse_declaration(path.read_bytes())
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra:
        refuse("prime review declaration has an unknown field: " + ", ".join(extra))
    if missing:
        refuse("prime review declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("prime review declaration schema is not librarian-prime-review")
    version = document["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != VERSION:
        refuse("prime review declaration version is not 1")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("prime review declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("prime review declaration does not match the pinned tools")
    for name in TOOLS:
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("prime review declaration does not match the pinned tools")
        if item["path"] != TOOLS[name]["path"] or item["sha256"] != TOOLS[name]["sha256"]:
            if isinstance(item["path"], str) and _escapes(item["path"]):
                refuse("tool path escapes the code root")
            refuse("prime review declaration does not match the pinned tools")
        if not isinstance(item["path"], str) or not isinstance(item["sha256"], str):
            refuse("prime review declaration does not match the pinned tools")
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


def _take(args: list[str], index: int, flag: str) -> str:
    if index + 1 >= len(args) or args[index + 1].startswith("--") or args[index + 1].strip() == "":
        refuse(f"missing value for {flag}")
    return args[index + 1]


def _override(item: str) -> bool:
    for flag in OVERRIDE_FLAGS:
        if item == flag or item.startswith(flag + "="):
            return True
    return False


def _draft(item: str) -> bool:
    if item == "draft":
        return True
    for flag in DRAFT_FLAGS:
        if item == flag or item.startswith(flag + "="):
            return True
    return False


def _require_path(text: str, flag: str) -> None:
    if text == "" or any(ord(char) < 32 or ord(char) == 127 for char in text):
        refuse(f"{flag} path must be absolute")
    if text.startswith("\\\\") or text.startswith("//"):
        refuse(f"UNC path {flag}")
    if not os.path.isabs(text):
        refuse(f"{flag} path must be absolute")
    if os.name == "nt" and DRIVE.match(text) is None:
        refuse(f"{flag} path must be absolute")
    path = Path(text)
    if ".." in path.parts:
        refuse(f"unsafe path {flag}")
    current = path
    chain = []
    while True:
        chain.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent
    for item in reversed(chain):
        if _is_link(item):
            refuse(f"{flag} path is linked and was not followed")


def parse_call(args: list[str]) -> dict:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    incoming = None
    root = None
    saw_json = False
    index = 0
    while index < len(args):
        item = args[index]
        if item == "--timeout" or item.startswith("--timeout="):
            refuse("caller timeout is refused")
        if _override(item):
            refuse("caller tool override is refused")
        if _draft(item):
            refuse("draft is not exposed")
        if item == "--json":
            if saw_json:
                refuse("repeated --json")
            saw_json = True
            index += 1
            continue
        if item == "--input":
            if incoming is not None:
                refuse("repeated --input")
            incoming = _take(args, index, "--input")
            index += 2
            continue
        if item == "--root":
            if root is not None:
                refuse("repeated --root")
            root = _take(args, index, "--root")
            index += 2
            continue
        refuse("unsupported argument")
    if incoming is None:
        refuse("missing --input")
    _require_path(incoming, "input")
    if root is not None:
        _require_path(root, "root")
    return {"input": incoming, "root": root, "json": saw_json}


def _run(tool: Path, subcommand: str, call: dict, code_root: Path) -> int:
    """Launch the pinned review tool once. No outer timeout and no retry."""
    if _is_link(code_root) or not code_root.is_dir():
        refuse("working root is not a directory")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, "-B", os.fspath(tool), subcommand, "--input", call["input"]]
    if call["root"] is not None:
        argv.extend(["--root", call["root"]])
    if call["json"]:
        argv.append("--json")
    try:
        proc = subprocess.run(
            argv,
            cwd=os.fspath(code_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
            shell=False,
        )
    except OSError as exc:
        refuse("pinned review tool failed to start: " + (exc.strerror or str(exc)))
    out = proc.stdout if type(proc.stdout) is bytes else b""
    err = proc.stderr if type(proc.stderr) is bytes else b""
    buffer = getattr(sys.stdout, "buffer", None)
    err_buffer = getattr(sys.stderr, "buffer", None)
    if buffer is None or err_buffer is None:
        refuse("stdout is not a byte stream")
    buffer.write(out)
    buffer.flush()
    err_buffer.write(err)
    err_buffer.flush()
    code = proc.returncode
    if type(code) is not int:
        refuse("pinned review tool returned no exit code")
    return code


def perform(command: str, args: list[str], code_root: Path) -> int:
    """Check the call, hash the pinned review tool, then launch that command only."""
    if command not in COMMANDS:
        refuse("unknown review command")
    call = parse_call(list(args))
    pinned = pin_tools(code_root)
    return _run(pinned["prime_review"], COMMANDS[command], call, code_root)
