#!/usr/bin/env python3
"""Unseated front door for the 05.03 review loop.

The declaration is app/review-loop.json. librarian.py does not load it.
A report, a render, or a recorded judgment is not authority and is not a release.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "review-loop-pins/1"
VERSION = 1
DECLARATION_NAME = "review-loop.json"
REPARSE = 0x400
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256"}
TOOLS = {
    "construct": {
        "path": "labs/review-construction-pass01/construct.py",
        "sha256": "8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a",
    },
    "prime_cycle_pass02": {
        "path": "labs/prime-cycle-pass02/prime_cycle.py",
        "sha256": "689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50",
    },
    "prime_review_pass01": {
        "path": "labs/prime-review-pass01/prime_review.py",
        "sha256": "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0",
    },
    "prime_review_pass02": {
        "path": "labs/prime-review-pass02/prime_review.py",
        "sha256": "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e",
    },
    "review_loop": {
        "path": "labs/review-loop-pass01/review_loop.py",
        "sha256": "fac0881d1e7e991b630d1deab688a3e28745e2f7b2075c7eb5148251b8ac5595",
    },
}
BANNED = {
    "capture",
    "reserve",
    "draft",
    "--dest",
    "--repo",
    "--tool",
    "--module",
    "--executable",
    "--python",
    "--pins",
    "--capture",
    "--reserve",
}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


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
    parts = rel.split("/")
    return any(part in ("", ".", "..") for part in parts)


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("tool path is linked and was not followed")
    if not path.is_file():
        refuse("review loop declaration is missing")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        refuse("review loop declaration is not utf-8")
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        refuse("review loop declaration is not strict json")
    if not isinstance(document, dict):
        refuse("review loop declaration is not strict json")
    if set(document) != TOP_KEYS:
        refuse("review loop declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("review loop declaration schema is not review-loop-pins/1")
    if document["version"] != VERSION:
        refuse("review loop declaration version is not 1")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("review loop declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("review loop declaration does not match the pinned tools")
    for name, expected in TOOLS.items():
        item = tools[name]
        if not isinstance(item, dict) or set(item) != TOOL_KEYS:
            refuse("review loop declaration does not match the pinned tools")
        if item["path"] != expected["path"] or item["sha256"] != expected["sha256"]:
            refuse("review loop declaration does not match the pinned tools")
        if _escapes(item["path"]):
            refuse("tool path escapes the code root")
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
    if not current.is_file() or not _inside(current, code_root):
        refuse(f"pinned tool is missing: {label}")
    digest = hashlib.sha256(current.read_bytes()).hexdigest()
    if digest != TOOLS[label]["sha256"]:
        refuse(f"pinned tool hash does not match: {label}")
    return current


def pin_tools(code_root: Path) -> dict[str, Path]:
    load_declaration(code_root)
    return {name: resolve_tool(code_root, name) for name in TOOLS}


def perform(args: list[str], code_root: Path) -> int:
    if not args or args[0] != "review-loop":
        refuse("unknown review-loop command")
    rest = args[1:]
    for item in rest:
        if item in BANNED or item.startswith("--tool") or item.startswith("--dest") or item.startswith("--capture") or item.startswith("--reserve"):
            refuse("caller tool override is refused")
    pinned = pin_tools(code_root)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", os.fspath(pinned["review_loop"]), *rest],
        cwd=os.fspath(code_root),
        env=env,
        check=False,
        shell=False,
    )
    code = proc.returncode
    if type(code) is not int:
        refuse("pinned review loop returned no exit code")
    return code


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    code_root = Path(__file__).resolve().parents[1]
    try:
        return perform(args, code_root)
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
