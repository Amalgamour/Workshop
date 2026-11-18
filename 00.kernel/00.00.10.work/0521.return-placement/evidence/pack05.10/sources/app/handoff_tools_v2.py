#!/usr/bin/env python3
"""Pinned front door for the guarded capture handoff.

The paths and hashes below are development wiring. They are not kernel law.
A receipt is custody. It is not review, acceptance, or publication.
This door checks the guard pin before launch. It does not launch a worker.
App selection is not this file.
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

SCHEMA = "librarian-capture-handoff-v2"
VERSION = 1
DECLARATION_NAME = "capture-handoff-v2.json"
DECLARATION_NOTE = (
    "Development wiring for the guarded capture handoff successor. Not kernel law. "
    "Capture launches labs/capture-handoff-guard-pass01/handoff.py after the reviewed guard pin matches. "
    "The sealed handoff remains directly runnable. Boot and batch are not repinned. "
    "This file is not app selection. A receipt is custody, not review, acceptance, or publication."
)
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256", "bytes"}
TOOLS = {
    "handoff": {
        "path": "labs/capture-handoff-guard-pass01/handoff.py",
        "sha256": "1b2e76915965d3a48bf158e01c96057e72bddf1cfa3b7c9abd53efa4a76b13c5",
        "bytes": 7851,
    },
    "guard": {
        "path": "labs/return-capture-guard-pass01/return_capture_guard.py",
        "sha256": "ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a",
        "bytes": 8931,
    },
    "clerk": {
        "path": "labs/clerk-handoff-pass02/clerk.py",
        "sha256": "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c",
        "bytes": 52279,
    },
    "return_capture": {
        "path": "labs/return-capture-pass01/return_capture.py",
        "sha256": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
        "bytes": 45767,
    },
    "return_inspect": {
        "path": "labs/return-capture-pass01/return_inspect.py",
        "sha256": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
        "bytes": 11402,
    },
}
OVERRIDE_FLAGS = (
    "--handoff",
    "--clerk",
    "--guard",
    "--tool",
    "--pins",
    "--capture",
    "--inspect",
    "--executable",
    "--python",
)
KNOWN_EXIT = (0, 2)
UNKNOWN_NOTE = (
    "attention: handoff outcome is unknown; inspect retained state; this call does not retry\n"
)


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


def _pairs(found: list[tuple[str, object]]) -> dict:
    value: dict = {}
    for key, item in found:
        if key in value:
            refuse(f"capture handoff declaration repeats {key}")
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
    if len(rel) >= 2 and rel[1] == ":":
        return True
    for part in rel.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith("."):
            return True
    return False


def parse_declaration(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("capture handoff declaration is not utf-8")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("capture handoff declaration is not utf-8")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("capture handoff declaration is not strict json")
    if text[end:].strip():
        refuse("capture handoff declaration is not strict json")
    if not isinstance(value, dict):
        refuse("capture handoff declaration is not strict json")
    return value


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("capture handoff declaration is missing")
    document = parse_declaration(path.read_bytes())
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra:
        refuse("capture handoff declaration has an unknown field: " + ", ".join(extra))
    if missing:
        refuse("capture handoff declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("capture handoff declaration schema is not librarian-capture-handoff-v2")
    version = document["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version != VERSION:
        refuse("capture handoff declaration version is not 1")
    if document.get("_note") != DECLARATION_NOTE:
        refuse("capture handoff declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("capture handoff declaration does not match the pinned tools")
    for name in TOOLS:
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("capture handoff declaration does not match the pinned tools")
        if item != TOOLS[name]:
            if isinstance(item.get("path"), str) and _escapes(item["path"]):
                refuse("tool path escapes the code root")
            if name == "guard":
                refuse("guard pin mismatch before launch")
            refuse("capture handoff declaration does not match the pinned tools")
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
    digest = hashlib.sha256(raw).hexdigest()
    if digest != TOOLS[label]["sha256"] or len(raw) != TOOLS[label]["bytes"]:
        if label == "guard":
            refuse("guard pin mismatch before launch")
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


def _require_binding(text: str) -> None:
    if text == "" or any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        refuse("binding path must be absolute")
    if not os.path.isabs(text):
        refuse("binding path must be absolute")
    path = Path(text)
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
            refuse("binding path is linked and was not followed")
    if not path.is_file():
        refuse("binding path is not a plain file")


def parse_call(args: list[str]) -> str:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    binding = None
    index = 0
    while index < len(args):
        item = args[index]
        if item == "--timeout" or item.startswith("--timeout="):
            refuse("caller timeout is refused")
        if _override(item):
            refuse("caller tool override is refused")
        if item == "--binding":
            if binding is not None:
                refuse("repeated --binding")
            binding = _take(args, index, "--binding")
            index += 2
            continue
        refuse("unsupported argument")
    if binding is None:
        refuse("missing --binding")
    _require_binding(binding)
    return binding


def _run(tool: Path, binding: str) -> int:
    """Launch the pinned handoff once. No outer timeout and no retry."""
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, "-B", os.fspath(tool), "perform", "--binding", binding]
    try:
        proc = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
            shell=False,
        )
    except OSError as exc:
        refuse("pinned handoff tool failed to start: " + (exc.strerror or str(exc)))
    out = proc.stdout if type(proc.stdout) is bytes else b""
    err = proc.stderr if type(proc.stderr) is bytes else b""
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.write(err)
    code = proc.returncode
    if type(code) is int and code in KNOWN_EXIT:
        sys.stderr.buffer.flush()
        return code
    sys.stderr.buffer.write(UNKNOWN_NOTE.encode("utf-8"))
    sys.stderr.buffer.flush()
    if type(code) is int:
        return code
    return 2


def perform(args: list[str], code_root: Path) -> int:
    """Check the binding, hash the guard before launch, then perform once."""
    binding = parse_call(list(args))
    pinned = pin_tools(code_root)
    return _run(pinned["handoff"], binding)


def main(argv: list[str] | None = None) -> int:
    chosen = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(chosen, Path(__file__).resolve().parent.parent)
    except Refuse as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
