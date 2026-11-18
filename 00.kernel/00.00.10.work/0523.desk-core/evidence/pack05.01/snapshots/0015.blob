#!/usr/bin/env python3
"""Pinned front door for the accepted read-only batch observation tool.

The paths and hashes below are development wiring. They are not kernel law.
An observation is not closure and is not release readiness.
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

SCHEMA = "librarian-batch-observer"
VERSION = 1
DECLARATION_NAME = "batch-observer.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256"}
TOOLS = {
    "batch_observe": {
        "path": "labs/batch-observation-pass01/batch_observe.py",
        "sha256": "8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4",
    },
    "prime_support": {
        "path": "labs/prime-support-pass01/prime_support.py",
        "sha256": "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
    },
    "clerk_adapter": {
        "path": "labs/prime-support-pass01/clerk_adapter.py",
        "sha256": "2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4",
    },
    "return_inspect": {
        "path": "labs/return-capture-pass01/return_inspect.py",
        "sha256": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
    },
    "return_capture": {
        "path": "labs/return-capture-pass01/return_capture.py",
        "sha256": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
    },
}
DRIVE = re.compile(r"^[A-Za-z]:")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
TIMEOUT_S = 60


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
            refuse(f"batch observer declaration repeats {key}")
        value[key] = item
    return value


def _inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def _escapes(rel: str) -> bool:
    if rel == "" or "\\" in rel or rel.startswith("/") or rel.startswith("//"):
        return True
    if DRIVE.match(rel):
        return True
    for part in rel.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith("."):
            return True
    return False


def _relative_problem(value: str) -> bool:
    if not isinstance(value, str) or value == "" or len(value) > 4000:
        return True
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return True
    if "\\" in value or value.startswith("/") or DRIVE.match(value) or ":" in value:
        return True
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(".") or part.endswith(" "):
            return True
    return False


def parse_declaration(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("batch observer declaration is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("batch observer declaration is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("batch observer declaration is not strict json")
    if text[end:].strip():
        refuse("batch observer declaration is not strict json")
    if not isinstance(value, dict):
        refuse("batch observer declaration is not strict json")
    return value


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("batch observer declaration is missing")
    document = parse_declaration(path.read_bytes())
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra:
        refuse("batch observer declaration has an unknown field: " + ", ".join(extra))
    if missing:
        refuse("batch observer declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("batch observer declaration schema is not librarian-batch-observer")
    version = document["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != VERSION:
        refuse("batch observer declaration version is not 1")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("batch observer declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("batch observer declaration does not match the pinned tools")
    for name in TOOLS:
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("batch observer declaration does not match the pinned tools")
        if item["path"] != TOOLS[name]["path"] or item["sha256"] != TOOLS[name]["sha256"]:
            if isinstance(item["path"], str) and _escapes(item["path"]):
                refuse("tool path escapes the code root")
            refuse("batch observer declaration does not match the pinned tools")
        if not isinstance(item["path"], str) or not isinstance(item["sha256"], str):
            refuse("batch observer declaration does not match the pinned tools")
    return document


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


def parse_call(args: list[str]) -> dict[str, str | None]:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    repo = None
    commit = None
    path = None
    members_book = None
    saw_json = False
    index = 0
    while index < len(args):
        item = args[index]
        if item == "--json":
            if saw_json:
                refuse("repeated --json")
            saw_json = True
            index += 1
            continue
        if item == "--live" or item.startswith("--live="):
            refuse("live mode is not exposed")
        if item == "--supplied" or item.startswith("--supplied="):
            refuse("supplied text is not exposed")
        if item == "--declaration" or item.startswith("--declaration="):
            refuse("declaration override is not exposed")
        if item == "--repo":
            if repo is not None:
                refuse("repeated --repo")
            repo = _take(args, index, "--repo")
            if not Path(repo).is_absolute():
                refuse("repository path must be absolute")
            index += 2
            continue
        if item == "--commit":
            if commit is not None:
                refuse("repeated --commit")
            commit = _take(args, index, "--commit")
            if HEX40.fullmatch(commit) is None:
                refuse("commit must be 40 lowercase hex")
            index += 2
            continue
        if item == "--path":
            if path is not None:
                refuse("repeated --path")
            path = _take(args, index, "--path")
            if _relative_problem(path):
                refuse("path is not a contained relative path")
            index += 2
            continue
        if item == "--members-book":
            if members_book is not None:
                refuse("repeated --members-book")
            members_book = _take(args, index, "--members-book")
            if not Path(members_book).is_absolute():
                refuse("members book path must be absolute")
            index += 2
            continue
        refuse("unsupported argument")
    if repo is None:
        refuse("missing --repo")
    if commit is None:
        refuse("missing --commit")
    if path is None:
        refuse("missing --path")
    if not saw_json:
        refuse("missing --json")
    return {
        "repo": repo,
        "commit": commit,
        "path": path,
        "members_book": members_book,
    }


def _run(tool: Path, call: dict[str, str | None]) -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [
        sys.executable,
        "-B",
        os.fspath(tool),
        "observe",
        "--repo",
        call["repo"],
        "--commit",
        call["commit"],
        "--path",
        call["path"],
    ]
    if call["members_book"] is not None:
        argv.extend(["--members-book", call["members_book"]])
    argv.append("--json")
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
        refuse("pinned observation tool timed out")
    except OSError as exc:
        refuse("pinned observation tool failed to start: " + (exc.strerror or str(exc)))
    if type(proc.returncode) is not int:
        refuse("pinned observation tool returned no exit code")
    sys.stdout.buffer.write(proc.stdout)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(proc.stderr)
    sys.stderr.buffer.flush()
    return proc.returncode


def perform(args: list[str], code_root: Path) -> int:
    """Check the call, hash the five pinned files, then observe one committed page."""
    call = parse_call(list(args))
    pinned = pin_tools(code_root)
    return _run(pinned["batch_observe"], call)
