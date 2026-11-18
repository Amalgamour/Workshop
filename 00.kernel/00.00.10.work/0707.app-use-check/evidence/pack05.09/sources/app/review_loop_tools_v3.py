#!/usr/bin/env python3
"""Pinned front door for the reviewed 05.09 review-loop app entry.

The declaration is app/review-loop-v3.json. librarian.py loads this module
for the review-loop command only. The launched module is review-loop pass03.
construct_pass04 is the direct constructor. construct_pass02 is the cycle
bind and is not substituted for pass04. A report, a render, or a recorded
judgment is not authority and is not a release. reproduce is a lab command
and is not exposed here. Workflow pass04 is not selected.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "review-loop-pins/2"
VERSION = 1
DECLARATION_NAME = "review-loop-v3.json"
REPARSE = 0x400
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE_BOOK = CHECKOUT / "00.kernel" / "00.00.10.work"
TOP_KEYS = {"schema", "version", "_note", "tools"}
TOOL_KEYS = {"path", "sha256", "bytes"}
TOOLS = {
    "construct_pass04": {
        "path": "labs/review-construction-pass04/construct.py",
        "sha256": "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20",
        "bytes": 42582,
    },
    "construct_pass02": {
        "path": "labs/review-construction-pass02/construct.py",
        "sha256": "b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc",
        "bytes": 36188,
    },
    "prime_cycle_pass03": {
        "path": "labs/prime-cycle-pass03/prime_cycle.py",
        "sha256": "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c",
        "bytes": 76045,
    },
    "prime_review_pass01": {
        "path": "labs/prime-review-pass01/prime_review.py",
        "sha256": "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0",
        "bytes": 58324,
    },
    "prime_review_pass02": {
        "path": "labs/prime-review-pass02/prime_review.py",
        "sha256": "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e",
        "bytes": 58560,
    },
    "return_inspect": {
        "path": "labs/return-capture-pass01/return_inspect.py",
        "sha256": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
        "bytes": 11402,
    },
    "return_lines": {
        "path": "labs/return-lines-pass01/return_lines.py",
        "sha256": "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a",
        "bytes": 100897,
    },
    "return_placement": {
        "path": "labs/return-placement-pass01/return_placement.py",
        "sha256": "db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754",
        "bytes": 66097,
    },
    "review_loop": {
        "path": "labs/review-loop-pass03/review_loop.py",
        "sha256": "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b",
        "bytes": 55474,
    },
}
COMMANDS = {
    "describe-legacy": ("--book", "--member"),
    "prepare": ("--fixture-root", "--request"),
    "record": ("--fixture-root", "--request", "--decision"),
    "render": ("--fixture-root", "--request"),
    "read": ("--fixture-root", "--request"),
    "recover": ("--fixture-root", "--request"),
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
PREFIXES = ("--tool", "--dest", "--capture", "--reserve", "--module", "--executable", "--python", "--pins")


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
    if not isinstance(rel, str) or rel == "" or "\\" in rel or rel.startswith("/") or rel.startswith("//"):
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
        refuse("review loop declaration schema is not review-loop-pins/2")
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
        if item["path"] != expected["path"] or item["sha256"] != expected["sha256"] or item["bytes"] != expected["bytes"]:
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
    data = current.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != TOOLS[label]["sha256"] or len(data) != TOOLS[label]["bytes"]:
        refuse(f"pinned tool hash does not match: {label}")
    return current


def pin_tools(code_root: Path) -> dict[str, Path]:
    load_declaration(code_root)
    return {name: resolve_tool(code_root, name) for name in ("review_loop", *TOOLS)}


def _absolute_directory(text: str, label: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        refuse(f"{label} is empty")
    if text.startswith("\\\\") or text.startswith("//"):
        refuse(f"UNC path {label}")
    path = Path(text)
    if not path.is_absolute():
        refuse(f"{label} must be absolute")
    if ".." in path.parts:
        refuse(f"unsafe path {label}")
    if _is_link(path) or not path.exists() or not path.is_dir():
        refuse(f"{label} is not a directory")
    return path


def disposable_root(text: str) -> Path:
    path = _absolute_directory(text, "fixture root")
    if _inside(path, CHECKOUT) or _inside(CHECKOUT, path):
        refuse("fixture root must stay outside D:\\Git\\lib-build")
    if _inside(path, LIVE_BOOK) or _inside(LIVE_BOOK, path):
        refuse("fixture root must not be the live work book")
    return path


def relative_argument(text: str, label: str) -> str:
    if not isinstance(text, str) or text.strip() == "":
        refuse(f"empty path {label}")
    if "\\" in text or text.startswith("/") or text.startswith("//") or len(text) >= 2 and text[1] == ":":
        refuse(f"unsafe path {label}")
    parts = text.split("/")
    if any(part in ("", ".", "..") for part in parts):
        refuse(f"unsafe path {label}")
    return text


def member_argument(text: str) -> str:
    if not isinstance(text, str) or text.strip() == "" or "/" in text or "\\" in text or text in {".", ".."}:
        refuse("unsafe path member")
    return text


def parse_call(args: list[str]) -> tuple[str, dict[str, str]]:
    if args and args[0] == "review-loop":
        args = args[1:]
    if not args:
        refuse("unknown review-loop command")
    command = args[0]
    if command == "reproduce":
        refuse("reproduce is a lab command and is not an app command")
    if command == "run":
        refuse("run is not a review-loop command")
    if command in {"capture", "reserve", "draft"}:
        refuse("caller tool override is refused")
    if command not in COMMANDS:
        refuse("unknown review-loop command")
    allowed = COMMANDS[command]
    values: dict[str, str] = {}
    index = 1
    while index < len(args):
        token = args[index]
        if token in BANNED or token.startswith(PREFIXES):
            refuse("caller tool override is refused")
        if token not in allowed:
            refuse("unknown argument")
        if token in values:
            refuse(f"repeated {token}")
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            refuse(f"missing value for {token}")
        values[token] = args[index + 1]
        index += 2
    for flag in allowed:
        if flag not in values:
            refuse(f"missing {flag}")
    return command, values


def forward_args(command: str, values: dict[str, str]) -> list[str]:
    if command == "describe-legacy":
        member_argument(values["--member"])
        _absolute_directory(values["--book"], "book")
        return [command, "--book", values["--book"], "--member", values["--member"]]
    disposable_root(values["--fixture-root"])
    relative_argument(values["--request"], "request")
    forwarded = [command, "--fixture-root", values["--fixture-root"], "--request", values["--request"]]
    if command == "record":
        relative_argument(values["--decision"], "decision")
        forwarded.extend(["--decision", values["--decision"]])
    return forwarded


def perform(args: list[str], code_root: Path) -> int:
    command, values = parse_call(list(args))
    forwarded = forward_args(command, values)
    pinned = pin_tools(code_root)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", os.fspath(pinned["review_loop"]), *forwarded],
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
