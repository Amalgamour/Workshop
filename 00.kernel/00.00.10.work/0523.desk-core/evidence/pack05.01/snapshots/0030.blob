#!/usr/bin/env python3
"""Pinned front door for the accepted pack checker and assembler.

The paths and hashes below are development wiring. They are not kernel law.
A clean custody result is not release readiness.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "librarian-prime-tools"
VERSION = 1
DECLARATION_NAME = "prime-tools.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256"}
TOOLS = {
    "pack_check": {
        "path": "labs/pack-custody-pass01/pack_check.py",
        "sha256": "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d",
    },
    "pack_assembly": {
        "path": "labs/pack-assembly-pass01/pack_assembly.py",
        "sha256": "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c",
    },
}
COMMANDS = {
    "pack-check": "pack_check",
    "pack-preview": "pack_assembly",
    "pack-assemble": "pack_assembly",
    "pack-verify": "pack_assembly",
}
SUBCOMMANDS = {
    "pack-preview": "preview",
    "pack-assemble": "assemble",
    "pack-verify": "verify",
}
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
            refuse(f"prime tool declaration repeats {key}")
        value[key] = item
    return value


def _inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def refuse_override(args: list[str]) -> None:
    for item in args:
        if item == "--checker" or item.startswith("--checker="):
            refuse("caller checker override is refused")


def parse_declaration(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("prime tool declaration is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("prime tool declaration is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("prime tool declaration is not strict json")
    if text[end:].strip():
        refuse("prime tool declaration is not strict json")
    if not isinstance(value, dict):
        refuse("prime tool declaration is not strict json")
    return value


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("prime tool declaration is missing")
    document = parse_declaration(path.read_bytes())
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra:
        refuse("prime tool declaration has an unknown field: " + ", ".join(extra))
    if missing:
        refuse("prime tool declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("prime tool declaration schema is not librarian-prime-tools")
    version = document["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != VERSION:
        refuse("prime tool declaration version is not 1")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("prime tool declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("prime tool declaration does not match the pinned tools")
    for name in TOOLS:
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("prime tool declaration does not match the pinned tools")
        if item["path"] != TOOLS[name]["path"] or item["sha256"] != TOOLS[name]["sha256"]:
            # A path that leaves the code root is reported as an escape.
            # Any other substitution is a different tool identity.
            if isinstance(item["path"], str) and _escapes(item["path"]):
                refuse("tool path escapes the code root")
            refuse("prime tool declaration does not match the pinned tools")
        if not isinstance(item["path"], str) or not isinstance(item["sha256"], str):
            refuse("prime tool declaration does not match the pinned tools")
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


def load_tool(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, os.fspath(path))
    if spec is None or spec.loader is None:
        refuse(f"pinned tool is missing: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perform(command: str, args: list[str], code_root: Path) -> int:
    """Hash both pinned tools, then call the one this command names.

    A caller-supplied checker is refused before either tool is loaded.
    The assembler's own --checker argument is the pinned checker path.
    """
    if command not in COMMANDS:
        refuse("unknown pack command")
    received = list(args)
    refuse_override(received)
    pinned = pin_tools(code_root)
    if command == "pack-check":
        module = load_tool(pinned["pack_check"], "prime_pack_check_pinned")
        code = module.main(received)
    else:
        module = load_tool(pinned["pack_assembly"], "prime_pack_assembly_pinned")
        checker = os.path.abspath(os.fspath(pinned["pack_check"]))
        code = module.main([SUBCOMMANDS[command], *received, "--checker", checker])
    if isinstance(code, bool) or not isinstance(code, int):
        refuse("tool returned no exit code")
    return code
