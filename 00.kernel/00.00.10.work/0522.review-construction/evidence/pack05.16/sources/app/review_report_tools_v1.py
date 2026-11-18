#!/usr/bin/env python3
"""Staged read-only connector for the accepted pass03 review reporter.

The shared dispatcher is unchanged. This module checks the reporter chain
and the pass01 dependency cut, then forwards one reporter process.
Exit 0 is not a release.
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

SCHEMA = "review-report-command/1"
VERSION = 1
DECLARATION_NAME = "review-report-v1.json"
REPARSE = 0x400
PASS = re.compile(r"^05\.\d\d$")
DRIVE = re.compile(r"^[A-Za-z]:")
TOP_KEYS = {"_note", "schema", "tools", "version"}
VALUE_KEYS = {"bytes", "sha256"}
FLAGS = ("--book", "--source", "--pass")
BANNED = ("--code-root", "--record", "--publish", "--prepare", "--form", "--tool")
REPORTER = "labs/review-report-pass03/report.py"
TOOLS = {
    "app/librarian.py": {
        "bytes": 12204,
        "sha256": "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9",
    },
    "app/review-loop-v4.json": {
        "bytes": 2519,
        "sha256": "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723",
    },
    "app/review-loop-v5.json": {
        "bytes": 1964,
        "sha256": "eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3",
    },
    "app/review-loop-v6.json": {
        "bytes": 2743,
        "sha256": "c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa",
    },
    "app/review-loop-v7.json": {
        "bytes": 3515,
        "sha256": "bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8",
    },
    "app/review_loop_tools_v4.py": {
        "bytes": 13381,
        "sha256": "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296",
    },
    "app/review_loop_tools_v5.py": {
        "bytes": 7875,
        "sha256": "b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9",
    },
    "app/review_loop_tools_v6.py": {
        "bytes": 9175,
        "sha256": "e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94",
    },
    "app/review_loop_tools_v7.py": {
        "bytes": 10291,
        "sha256": "93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d",
    },
    "labs/prime-cycle-pass03/prime_cycle.py": {
        "bytes": 76045,
        "sha256": "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c",
    },
    "labs/prime-review-pass02/prime_review.py": {
        "bytes": 58560,
        "sha256": "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e",
    },
    "labs/return-access-pass01/return_access.py": {
        "bytes": 26561,
        "sha256": "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5",
    },
    "labs/review-construction-pass04/construct.py": {
        "bytes": 42582,
        "sha256": "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20",
    },
    "labs/review-loop-pass03/review_loop.py": {
        "bytes": 55474,
        "sha256": "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b",
    },
    "labs/review-report-pass01/report.py": {
        "bytes": 42127,
        "sha256": "72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc",
    },
    "labs/review-report-pass02/report.py": {
        "bytes": 38323,
        "sha256": "d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e",
    },
    "labs/review-report-pass03/report.py": {
        "bytes": 8091,
        "sha256": "70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade",
    },
    "labs/workbook-review-pass01/forms/workbook-review-v1.json": {
        "bytes": 4532,
        "sha256": "152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f",
    },
    "labs/workbook-review-pass01/workbook.py": {
        "bytes": 79131,
        "sha256": "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a",
    },
    "labs/workbook-review-pass02/forms/workbook-review-v1.json": {
        "bytes": 4532,
        "sha256": "66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645",
    },
    "labs/workbook-review-pass02/workbook.py": {
        "bytes": 52574,
        "sha256": "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a",
    },
    "labs/workbook-review-pass03/forms/workbook-review-v1.json": {
        "bytes": 4532,
        "sha256": "4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b",
    },
    "labs/workbook-review-pass03/workbook.py": {
        "bytes": 19533,
        "sha256": "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c",
    },
}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def refuse(message: str) -> None:
    raise Refuse(message)


def installed_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _pairs(pairs: list[tuple[str, object]]) -> dict:
    value: dict = {}
    for key, item in pairs:
        if key in value:
            refuse(f"review report declaration repeats {key}")
        value[key] = item
    return value


def escapes(rel: str) -> bool:
    if rel == "" or "\\" in rel or rel.startswith("/") or rel.startswith("//"):
        return True
    if DRIVE.match(rel):
        return True
    return any(part in {"", ".", ".."} or part.endswith(" ") or part.endswith(".") for part in rel.split("/"))


def assess_tools(tools: object) -> None:
    if isinstance(tools, dict):
        for key in tools:
            if isinstance(key, str) and escapes(key):
                refuse("tool path escapes the code root")
    if not isinstance(tools, dict) or set(tools) != set(TOOLS):
        refuse("declaration does not match the pinned tools")
    for key, want in TOOLS.items():
        item = tools[key]
        if not isinstance(item, dict) or set(item) != VALUE_KEYS:
            refuse("declaration does not match the pinned tools")
        if type(item["bytes"]) is not int or type(item["sha256"]) is not str:
            refuse("declaration does not match the pinned tools")
        if item["bytes"] != want["bytes"] or item["sha256"] != want["sha256"]:
            refuse("declaration does not match the pinned tools")


def parse_declaration(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        refuse("review report declaration is not strict json")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        refuse("review report declaration is not strict json")
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs).raw_decode(text)
    except Refuse:
        raise
    except json.JSONDecodeError:
        refuse("review report declaration is not strict json")
    if text[end:].strip():
        refuse("review report declaration is not strict json")
    if not isinstance(value, dict):
        refuse("review report declaration is not strict json")
    return value


def assess_declaration(raw: bytes) -> dict:
    document = parse_declaration(raw)
    extra = sorted(set(document) - TOP_KEYS)
    missing = sorted(TOP_KEYS - set(document))
    if extra or missing:
        refuse("declaration does not match the pinned tools")
    if document["schema"] != SCHEMA:
        refuse("declaration does not match the pinned tools")
    version = document["version"]
    if type(version) is not int or version != VERSION:
        refuse("declaration does not match the pinned tools")
    if type(document["_note"]) is not str or document["_note"].strip() == "":
        refuse("declaration does not match the pinned tools")
    assess_tools(document["tools"])
    return document


def load_declaration(code_root: Path) -> dict:
    app_dir = code_root / "app"
    path = app_dir / DECLARATION_NAME
    if _is_link(app_dir) or _is_link(path):
        refuse("review report declaration is linked and was not followed")
    if not path.is_file():
        refuse("review report declaration is missing")
    return assess_declaration(path.read_bytes())


def audit_dependencies(code_root: Path) -> None:
    load_declaration(code_root)
    for rel, want in TOOLS.items():
        if escapes(rel):
            refuse("tool path escapes the code root")
        cursor = code_root
        for part in rel.split("/"):
            cursor = cursor / part
            if _is_link(cursor):
                refuse(f"dependency conflict {rel} is linked and was not followed")
        if not cursor.is_file():
            refuse(
                f"dependency conflict {rel} got missing want {want['bytes']} bytes sha256 {want['sha256']}"
            )
        data = cursor.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if len(data) != want["bytes"] or got != want["sha256"]:
            refuse(
                f"dependency conflict {rel} got {len(data)} bytes sha256 {got} "
                f"want {want['bytes']} bytes sha256 {want['sha256']}"
            )


def _require_book(text: str) -> None:
    if text.startswith("\\\\") or text.startswith("//"):
        refuse("book must be an absolute directory and was not followed when linked")
    path = Path(text)
    if not path.is_absolute() or ".." in path.parts:
        refuse("book must be an absolute directory and was not followed when linked")
    if _is_link(path) or not path.is_dir():
        refuse("book must be an absolute directory and was not followed when linked")


def _banned(item: str) -> str | None:
    for flag in BANNED:
        if item == flag or item.startswith(flag + "="):
            return flag
    return None


def parse_call(args: list[str]) -> dict:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    values: dict[str, str] = {}
    index = 0
    while index < len(args):
        item = args[index]
        if not item.startswith("--"):
            refuse(f"unknown argument {item}")
        banned = _banned(item)
        if banned is not None:
            refuse(f"unknown flag {banned}")
        if "=" in item:
            refuse(f"unknown flag {item.split('=', 1)[0]}")
        if item not in FLAGS:
            refuse(f"unknown flag {item}")
        if item in values:
            refuse(f"repeated {item}")
        if index + 1 >= len(args) or args[index + 1].startswith("--") or args[index + 1] == "":
            refuse(f"missing value for {item}")
        values[item] = args[index + 1]
        index += 2
    for flag in FLAGS:
        if flag not in values:
            refuse(f"missing {flag}")
    if PASS.fullmatch(values["--pass"]) is None:
        refuse("pass is not 05.NN")
    source = values["--source"]
    if (
        source.strip() == ""
        or source.startswith("-")
        or "/" in source
        or "\\" in source
        or "\n" in source
        or "\r" in source
    ):
        refuse("source is a page id")
    _require_book(values["--book"])
    return {"book": values["--book"], "pass": values["--pass"], "source": source}


def seating(code_root: Path) -> Path:
    here = Path(__file__).resolve()
    derived = here.parent.parent
    expected = (derived / "app" / "review_report_tools_v1.py").resolve()
    try:
        supplied = Path(code_root).resolve()
    except OSError:
        refuse(f"copied fixture root {code_root} is not the installed app root {derived}")
    if here != expected:
        refuse(f"copied fixture root {here.parent} is not the installed app root {supplied}")
    if supplied != derived:
        refuse(f"copied fixture root {supplied} is not the installed app root {derived}")
    return derived


def _launch(root: Path, call: dict) -> int:
    script = root / REPORTER
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [
        sys.executable,
        "-B",
        os.fspath(script),
        "--code-root",
        os.fspath(root),
        "--book",
        call["book"],
        "--source",
        call["source"],
        "--pass",
        call["pass"],
    ]
    try:
        proc = subprocess.run(
            argv,
            cwd=os.fspath(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
            shell=False,
        )
    except OSError as exc:
        refuse("pinned reporter failed to start: " + (exc.strerror or str(exc)))
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
        refuse("pinned reporter returned no exit code")
    return code


def perform(args: list[str], code_root: Path) -> int:
    call = parse_call(args)
    root = seating(code_root)
    audit_dependencies(root)
    return _launch(root, call)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, installed_root())
    except Refuse as exc:
        print(f"stop: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
