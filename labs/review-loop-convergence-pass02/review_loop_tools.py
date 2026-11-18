#!/usr/bin/env python3
"""Unselected review-loop door for the pass02 candidate (0522/05.18).

Resolves the workbook under the supplied candidate root. Does not require a
canonical path. Does not load a live-repo door when the candidate file is absent.
"""

from __future__ import annotations

import hashlib
import os
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "review-loop-pins/10"
WORKBOOK_REL = "labs/review-loop-convergence-pass02/workbook.py"
DECLARATION_REL = "labs/review-loop-convergence-pass02/review-loop.json"
WORKBOOK_SHA = "a013e4466c79794eb62c7f697d222e693d8453af91571a404fedb0b4dcc4ef3f"
WORKBOOK_BYTES = 6613
DECLARATION_SHA = "d7b1b6297c12d618a3a452f71e14fc4b326a94fcd39a96bca81984b011b421b8"
DECLARATION_BYTES = 746
COMMANDS = {"prepare", "form", "record", "inspect", "publish", "read", "recover"}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _pin(root: Path, rel: str, size: int, digest: str, label: str) -> Path:
    if rel.startswith(("/", "\\")) or ".." in rel.split("/"):
        refuse(f"{label} path escapes")
    path = root
    for part in rel.split("/"):
        path = path / part
        if path.is_symlink():
            refuse(f"{label} pin is linked")
    if not path.is_file():
        refuse(f"{label} pin is missing")
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if len(data) != size or got != digest:
        refuse(f"{label} pin mismatch got {len(data)} bytes sha256 {got} want {size} bytes sha256 {digest}")
    return path


def executed_workbook(document) -> str:
    tools = document.get("tools") if isinstance(document, dict) else None
    workbook = tools.get("workbook") if isinstance(tools, dict) else None
    path = workbook.get("path") if isinstance(workbook, dict) else None
    if path != WORKBOOK_REL:
        refuse("purported workbook is not the executed workbook")
    return path


def perform(args: list[str], code_root: Path) -> int:
    if not isinstance(args, list) or not args or type(args[0]) is not str:
        refuse("unknown review-loop command")
    command = args[0]
    if command not in COMMANDS:
        refuse("fixture and unknown review-loop commands are refused")
    root = Path(code_root)
    declaration = _pin(root, DECLARATION_REL, DECLARATION_BYTES, DECLARATION_SHA, "declaration")
    document = json.loads(declaration.read_bytes().decode("utf-8"))
    if document.get("schema") != SCHEMA:
        refuse("review loop declaration schema is not review-loop-pins/10")
    executed_workbook(document)
    script = _pin(root, WORKBOOK_REL, WORKBOOK_BYTES, WORKBOOK_SHA, "workbook")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", os.fspath(script), *args],
        cwd=os.fspath(root),
        env=env,
        check=False,
        shell=False,
    )
    if type(proc.returncode) is not int:
        refuse("workbook returned no exit code")
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
