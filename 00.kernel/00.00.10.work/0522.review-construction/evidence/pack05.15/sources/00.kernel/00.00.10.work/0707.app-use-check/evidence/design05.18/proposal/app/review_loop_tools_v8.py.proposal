#!/usr/bin/env python3
"""Pinned front door for the N7 return-intake repair (0707/05.17 contract, 0707/05.18 candidate).

librarian.py loads this module for the review-loop command only.
Workbook commands call labs/workbook-review-pass04/workbook.py.
Fixture-root commands are forwarded to app/review_loop_tools_v4.py unchanged.
Pass03, pass02, pass01, v7, v6, and v5 stay pinned and are not the selected door.
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

SCHEMA = "review-loop-pins/6"
VERSION = 1
DECLARATION_NAME = "review-loop-v8.json"
V4_NAME = "review_loop_tools_v4.py"
V4_SHA = "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296"
V4_BYTES = 13381
V4_JSON_SHA = "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723"
V4_JSON_BYTES = 2519
V5_SHA = "b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9"
V5_BYTES = 7875
V5_JSON_SHA = "eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3"
V5_JSON_BYTES = 1964
V6_SHA = "e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94"
V6_BYTES = 9175
V6_JSON_SHA = "c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa"
V6_JSON_BYTES = 2743
V7_SHA = "93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d"
V7_BYTES = 10291
V7_JSON_SHA = "bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8"
V7_JSON_BYTES = 3515
PASS03_SHA = "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c"
PASS03_BYTES = 19533
PASS01_SHA = "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"
PASS01_BYTES = 79131
PASS01_FORM_SHA = "152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f"
PASS01_FORM_BYTES = 4532
PASS02_SHA = "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a"
PASS02_BYTES = 52574
PASS02_FORM_SHA = "66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645"
PASS02_FORM_BYTES = 4532
REPARSE = 0x400
TOOL_KEYS = {"bytes", "path", "sha256"}
TOP_KEYS = {"_note", "schema", "tools", "version"}
TOOL_NAMES = {
    "construct_pass04",
    "form",
    "form_pass01",
    "form_pass02",
    "prime_cycle_pass03",
    "prime_review_pass02",
    "return_access",
    "review_loop",
    "review_loop_v4",
    "review_loop_v4_json",
    "review_loop_v5",
    "review_loop_v5_json",
    "review_loop_v6",
    "review_loop_v6_json",
    "review_loop_v7",
    "review_loop_v7_json",
    "workbook",
    "workbook_pass01",
    "workbook_pass02",
    "workbook_pass03",
}
WORKBOOK = {"prepare", "form", "record", "inspect", "publish", "read", "recover"}
V4_COMMANDS = {"describe-legacy", "prepare", "record", "render", "read", "recover", "reproduce", "run"}
BANNED = {"--dest", "--executable", "--module", "--pins", "--python", "--tool"}
RESOLVE = (
    "return_access",
    "review_loop",
    "construct_pass04",
    "prime_cycle_pass03",
    "prime_review_pass02",
    "form",
    "form_pass01",
    "form_pass02",
    "workbook",
    "workbook_pass01",
    "workbook_pass02",
    "workbook_pass03",
    "review_loop_v5",
    "review_loop_v5_json",
    "review_loop_v6",
    "review_loop_v6_json",
    "review_loop_v7",
    "review_loop_v7_json",
)


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
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
    if not isinstance(rel, str) or rel == "" or "\\" in rel or rel.startswith("/"):
        return True
    parts = rel.split("/")
    return any(part in ("", ".", "..") for part in parts)


def load_declaration(code_root: Path) -> dict:
    path = code_root / "app" / DECLARATION_NAME
    if _is_link(path):
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
    if not isinstance(document, dict) or set(document) != TOP_KEYS:
        refuse("review loop declaration does not match the pinned tools")
    if document["schema"] != SCHEMA or document["version"] != VERSION:
        refuse("review loop declaration schema is not review-loop-pins/6")
    if not isinstance(document["_note"], str) or document["_note"].strip() == "":
        refuse("review loop declaration does not match the pinned tools")
    tools = document["tools"]
    if not isinstance(tools, dict) or set(tools) != TOOL_NAMES:
        refuse("review loop declaration does not match the pinned tools")
    for item in tools.values():
        if not isinstance(item, dict) or set(item) != TOOL_KEYS or _escapes(item["path"]):
            refuse("review loop declaration does not match the pinned tools")
        if not isinstance(item["sha256"], str) or not isinstance(item["bytes"], int):
            refuse("review loop declaration does not match the pinned tools")
    return document


def resolve_tool(code_root: Path, item: dict) -> Path:
    current = code_root
    for part in item["path"].split("/"):
        current = current / part
        if _is_link(current):
            refuse("tool path is linked and was not followed")
    if not current.is_file() or not _inside(current, code_root):
        refuse(f"pinned tool is missing: {item['path']}")
    data = current.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != item["sha256"] or len(data) != item["bytes"]:
        refuse(f"pinned tool hash does not match: {item['path']}")
    return current


def pin_named(code_root: Path, rel: str, digest: str, size: int, label: str) -> None:
    path = code_root / rel
    if _is_link(path) or not path.is_file():
        refuse(f"{label} pin is missing")
    data = path.read_bytes()
    if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
        refuse(f"{label} pin mismatch")


def pin_predecessors(code_root: Path) -> None:
    pin_named(code_root, "app/review_loop_tools_v4.py", V4_SHA, V4_BYTES, "v4")
    pin_named(code_root, "app/review-loop-v4.json", V4_JSON_SHA, V4_JSON_BYTES, "v4")
    pin_named(code_root, "app/review_loop_tools_v5.py", V5_SHA, V5_BYTES, "v5")
    pin_named(code_root, "app/review-loop-v5.json", V5_JSON_SHA, V5_JSON_BYTES, "v5")
    pin_named(code_root, "app/review_loop_tools_v6.py", V6_SHA, V6_BYTES, "v6")
    pin_named(code_root, "app/review-loop-v6.json", V6_JSON_SHA, V6_JSON_BYTES, "v6")
    pin_named(code_root, "labs/workbook-review-pass01/workbook.py", PASS01_SHA, PASS01_BYTES, "pass01")
    pin_named(code_root, "labs/workbook-review-pass01/forms/workbook-review-v1.json", PASS01_FORM_SHA, PASS01_FORM_BYTES, "pass01 form")
    pin_named(code_root, "labs/workbook-review-pass02/workbook.py", PASS02_SHA, PASS02_BYTES, "pass02")
    pin_named(code_root, "labs/workbook-review-pass02/forms/workbook-review-v1.json", PASS02_FORM_SHA, PASS02_FORM_BYTES, "pass02 form")
    pin_named(code_root, "app/review_loop_tools_v7.py", V7_SHA, V7_BYTES, "v7")
    pin_named(code_root, "app/review-loop-v7.json", V7_JSON_SHA, V7_JSON_BYTES, "v7")
    pin_named(code_root, "labs/workbook-review-pass03/workbook.py", PASS03_SHA, PASS03_BYTES, "pass03")


def load_v4(code_root: Path):
    pin_predecessors(code_root)
    path = code_root / "app" / V4_NAME
    import importlib.util
    spec = importlib.util.spec_from_file_location("librarian_review_loop_tools_v4", path)
    if spec is None or spec.loader is None:
        refuse("v4 door did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def workbook_call(code_root: Path, args: list[str], tools: dict) -> int:
    script = resolve_tool(code_root, tools["workbook"])
    for name in RESOLVE:
        resolve_tool(code_root, tools[name])
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", os.fspath(script), *args],
        cwd=os.fspath(code_root),
        env=env,
        check=False,
        shell=False,
    )
    if type(proc.returncode) is not int:
        refuse("workbook returned no exit code")
    return proc.returncode


def perform(args: list[str], code_root: Path) -> int:
    if not args:
        refuse("unknown review-loop command")
    command = args[0]
    document = load_declaration(code_root)
    tools = document["tools"]
    resolve_tool(code_root, tools["review_loop_v4"])
    resolve_tool(code_root, tools["review_loop_v4_json"])
    resolve_tool(code_root, tools["review_loop_v5"])
    resolve_tool(code_root, tools["review_loop_v5_json"])
    resolve_tool(code_root, tools["review_loop_v6"])
    resolve_tool(code_root, tools["review_loop_v6_json"])
    pin_predecessors(code_root)
    fixture = "--fixture-root" in args
    if command == "describe-legacy" or command in {"render", "reproduce", "run"} or fixture:
        if "--book" in args and command != "describe-legacy":
            refuse("book and fixture-root are different scopes")
        if any(token in BANNED or token.startswith("--tool") or token.startswith("--dest") for token in args):
            refuse("caller tool override is refused")
        door = load_v4(code_root)
        try:
            return door.perform(args, code_root)
        except door.Refuse as exc:
            refuse(str(exc))
    if command in WORKBOOK and "--book" in args:
        if any(token in BANNED or token.startswith("--tool") or token.startswith("--dest") for token in args):
            refuse("caller tool override is refused")
        return workbook_call(code_root, args, tools)
    if command in V4_COMMANDS:
        door = load_v4(code_root)
        try:
            return door.perform(args, code_root)
        except door.Refuse as exc:
            refuse(str(exc))
    refuse("unknown review-loop command")


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
