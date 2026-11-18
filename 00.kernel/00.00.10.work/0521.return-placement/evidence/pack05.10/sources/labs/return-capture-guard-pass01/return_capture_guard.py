#!/usr/bin/env python3
"""Guarded front for the historical return writer.

Reserve and capture load the pinned writer only when the book has no
line-pass layout. An accepted return-line-layout/1 declaration refuses
before that module is executed. Verify still uses the pinned writer.
An undeclared book has not gained line-pass protection.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import stat
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

CAPTURE_REL = "labs/return-capture-pass01/return_capture.py"
CAPTURE_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
CAPTURE_BYTES = 45767
LINES_REL = "labs/return-lines-pass01/return_lines.py"
LINES_SHA = "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a"
LINES_BYTES = 100897
REPARSE = 0x400
WRITE_COMMANDS = {"reserve", "capture"}
ABSENT_LINE = (
    "line-pass protection: absent. "
    "An undeclared book has not gained line-pass protection.\n"
)
_LINES = None


class PinMismatch(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_reparse(path: str) -> bool:
    info = os.lstat(path)
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE) or stat.S_ISLNK(info.st_mode)


def read_regular(path: str, label: str) -> bytes:
    if not os.path.lexists(path):
        raise PinMismatch(f"{label} is missing")
    if is_reparse(path):
        raise PinMismatch(f"{label} is linked")
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        raise PinMismatch(f"{label} is not a regular file")
    if info.st_nlink != 1:
        raise PinMismatch(f"{label} link count is not 1")
    with open(path, "rb") as handle:
        return handle.read()


def load_pinned(rel: str, digest: str, size: int, name: str):
    path = os.path.join(repo_root(), *rel.split("/"))
    data = read_regular(path, rel)
    if sha256_bytes(data) != digest or len(data) != size:
        raise PinMismatch(f"{rel} pin mismatch")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PinMismatch(f"{rel} did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_lines():
    global _LINES
    if _LINES is None:
        _LINES = load_pinned(LINES_REL, LINES_SHA, LINES_BYTES, "return_lines_pass01_layout_rules")
    return _LINES


def assert_writer_bytes() -> None:
    path = os.path.join(repo_root(), *CAPTURE_REL.split("/"))
    data = read_regular(path, CAPTURE_REL)
    if sha256_bytes(data) != CAPTURE_SHA or len(data) != CAPTURE_BYTES:
        raise PinMismatch(f"{CAPTURE_REL} pin mismatch")


def load_writer():
    return load_pinned(CAPTURE_REL, CAPTURE_SHA, CAPTURE_BYTES, "return_capture_pass01_pinned")


def classify(book: str) -> dict:
    """Read the layout only. This does not load the historical writer."""
    lines = load_lines()
    root = os.path.abspath(book)
    path = os.path.join(root, lines.LAYOUT_NAME)
    if not os.path.lexists(path):
        return {
            "protection": "absent",
            "reason": "layout is absent",
            "status": "undeclared",
        }
    if is_reparse(path):
        return {
            "protection": "not-declared",
            "reason": "layout is linked",
            "status": "linked",
        }
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        return {
            "protection": "not-declared",
            "reason": "layout is not a regular file",
            "status": "malformed",
        }
    if info.st_nlink != 1:
        return {
            "protection": "not-declared",
            "reason": "layout link count is not 1",
            "status": "linked",
        }
    try:
        body = lines.read_layout(root)
    except lines.LineError as exc:
        status = "linked" if "link" in exc.reason else "malformed"
        if exc.state == "conflict":
            status = "conflict"
        return {
            "protection": "not-declared",
            "reason": exc.reason,
            "status": status,
        }
    raw = lines.read_exact(path)
    expected = lines.dump(lines.layout_body(body["book"]))
    if raw != expected:
        return {
            "protection": "not-declared",
            "reason": "layout bytes differ from the accepted declaration",
            "status": "conflict",
        }
    return {
        "book": body["book"],
        "protection": "declared",
        "reason": "layout is the accepted line-pass declaration",
        "status": "declared",
    }


def refusal(found: dict) -> str:
    status = found["status"]
    state = "refused" if status in {"declared", "undeclared"} else "attention"
    if status == "declared":
        correction = (
            "Use the line-pass route. This legacy writer does not reserve or "
            "capture on a declared book. No receipt was written."
        )
    elif status == "linked":
        correction = "The layout path is linked. It was not followed. Sequential allocation was not used."
    elif status == "conflict":
        correction = (
            "The layout conflicts with the accepted line-pass declaration. "
            "Sequential allocation was not used."
        )
    else:
        correction = (
            "The layout is not an accepted line-pass declaration. "
            "Sequential allocation was not used."
        )
    lines = [
        "check: return-line-layout/1",
        f"state: {state}",
        "writer_started: false",
        f"line-pass protection: {found['protection']}",
        "sequential_allocation: not-used",
        f"correction: {correction}",
        "result refused",
    ]
    return "\n".join(lines) + "\n"


def pin_refusal(detail: str) -> str:
    lines = [
        "check: pin",
        "state: refused",
        "writer_started: false",
        "sequential_allocation: not-used",
        f"correction: {detail}. Nothing was written.",
        "result refused",
    ]
    return "\n".join(lines) + "\n"


def with_absent_notice(text: str) -> str:
    if not text.endswith("\n"):
        text += "\n"
    return text + ABSENT_LINE


def parse(argv: list[str]):
    parser = argparse.ArgumentParser(prog="return_capture_guard.py")
    sub = parser.add_subparsers(dest="command", required=True)
    reserve = sub.add_parser("reserve")
    reserve.add_argument("--book", required=True)
    reserve.add_argument("--submission", required=True)
    reserve.add_argument("--name", required=True)
    reserve.add_argument("--origin-book", required=True)
    reserve.add_argument("--origin-page", required=True)
    reserve.add_argument("--origin-batch", required=True)
    reserve.add_argument("--expected-output", action="append", default=None)
    reserve.add_argument("--submitter", required=True)
    reserve.add_argument("--reviewer", required=True)
    reserve.add_argument("--release", required=True)
    reserve.add_argument("--supersedes", default=None)
    capture = sub.add_parser("capture")
    capture.add_argument("--book", required=True)
    capture.add_argument("--submission", required=True)
    capture.add_argument("--return-file", required=True)
    capture.add_argument("--source-root", required=True)
    capture.add_argument("--artifact", action="append", default=None)
    capture.add_argument("--retrospective", action="store_true")
    capture.add_argument("--source-commit", default=None)
    capture.add_argument("--return-includes-prime-review", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--book", required=True)
    verify.add_argument("--member", required=True)
    return parser.parse_args(argv)


def run(argv: list[str], loader=load_writer) -> tuple[int, str]:
    args = parse(argv)
    assert_writer_bytes()
    if args.command in WRITE_COMMANDS:
        found = classify(args.book)
        if found["status"] != "undeclared":
            return 2, refusal(found)
        result = loader().execute(argv)
        return result.code, with_absent_notice(result.text)
    result = loader().execute(argv)
    return result.code, result.text


def main(argv: list[str] | None = None) -> int:
    chosen = list(sys.argv[1:] if argv is None else argv)
    try:
        code, text = run(chosen)
    except PinMismatch as exc:
        code, text = 2, pin_refusal(exc.detail)
    except SystemExit as exc:
        code = exc.code
        return 2 if code is None else int(code)
    sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
