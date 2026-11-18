#!/usr/bin/env python3
"""Guarded capture handoff in front of the sealed handoff.

This file pin-checks the sealed handoff, the Clerk, the historical writer,
the inspector, and the reviewed guard. Capture and reserve launches use the
guard only after its bytes match that pin. The check runs again immediately
before the subprocess. Verify and inspect keep the historical scripts.
The sealed handoff is not edited. The public CLI has no --guard override.
App selection is not this file.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HANDOFF_REL = "labs/capture-handoff-pass01/handoff.py"
HANDOFF_SHA = "a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a"
HANDOFF_BYTES = 51828
CLERK_REL = "labs/clerk-handoff-pass02/clerk.py"
CLERK_SHA = "f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c"
CLERK_BYTES = 52279
CAPTURE_REL = "labs/return-capture-pass01/return_capture.py"
CAPTURE_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
CAPTURE_BYTES = 45767
INSPECT_REL = "labs/return-capture-pass01/return_inspect.py"
INSPECT_SHA = "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"
INSPECT_BYTES = 11402
GUARD_REL = "labs/return-capture-guard-pass01/return_capture_guard.py"
GUARD_SHA = "ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a"
GUARD_BYTES = 8931
REPARSE = 0x400
SWITCHED = {"capture", "reserve"}
SIBLINGS = (
    (HANDOFF_REL, HANDOFF_SHA, HANDOFF_BYTES),
    (CLERK_REL, CLERK_SHA, CLERK_BYTES),
    (CAPTURE_REL, CAPTURE_SHA, CAPTURE_BYTES),
    (INSPECT_REL, INSPECT_SHA, INSPECT_BYTES),
    (GUARD_REL, GUARD_SHA, GUARD_BYTES),
)
_HANDOFF = None


class GuardMismatch(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class PinMismatch(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def live_book() -> str:
    return os.path.join(repo_root(), "00.kernel", "00.00.10.work")


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


def default_guard() -> str:
    return os.path.join(repo_root(), *GUARD_REL.split("/"))


def require_guard(path: str) -> str:
    """Return the absolute guard path when its bytes match the reviewed pin."""
    if not isinstance(path, str) or path.strip() == "":
        raise GuardMismatch("guard path is empty")
    absolute = os.path.abspath(path)
    try:
        data = read_regular(absolute, "guard")
    except PinMismatch as exc:
        raise GuardMismatch(exc.detail) from None
    if sha256_bytes(data) != GUARD_SHA or len(data) != GUARD_BYTES:
        raise GuardMismatch("guard pin mismatch before launch")
    return absolute


def assert_siblings() -> None:
    root = repo_root()
    for rel, digest, size in SIBLINGS:
        path = os.path.join(root, *rel.split("/"))
        try:
            data = read_regular(path, rel)
        except PinMismatch as exc:
            raise PinMismatch(exc.detail) from None
        if sha256_bytes(data) != digest or len(data) != size:
            raise PinMismatch(f"{rel} pin mismatch")


def load_handoff():
    global _HANDOFF
    if _HANDOFF is not None:
        return _HANDOFF
    assert_siblings()
    path = os.path.join(repo_root(), *HANDOFF_REL.split("/"))
    spec = importlib.util.spec_from_file_location("capture_handoff_pass01_pinned", path)
    if spec is None or spec.loader is None:
        raise PinMismatch(f"{HANDOFF_REL} did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _HANDOFF = module
    return module


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def outside_live(parent: Path) -> bool:
    live = os.path.normcase(os.path.abspath(live_book()))
    found = os.path.normcase(os.path.abspath(parent))
    if found == live:
        return False
    prefix = live if live.endswith(os.sep) else live + os.sep
    return not found.startswith(prefix)


def write_sidecar(binding_path: str, detail: str) -> str | None:
    path = Path(binding_path)
    parent = path.parent
    if not outside_live(parent):
        return None
    try:
        if not parent.exists() or not parent.is_dir() or is_reparse(str(parent)):
            return None
    except OSError:
        return None
    sidecar = parent / (path.name + ".guard-mismatch.json")
    if sidecar.exists():
        return str(sidecar)
    body = {
        "bytes": GUARD_BYTES,
        "detail": detail,
        "launched": False,
        "reason": "guard pin mismatch before launch",
        "schema": "capture-handoff-guard-mismatch/1",
        "sha256": GUARD_SHA,
        "writer_started": False,
    }
    try:
        sidecar.write_bytes(dump(body))
    except OSError:
        return None
    return str(sidecar)


def refusal_text(check: str, reason: str) -> str:
    lines = [
        f"check: {check}",
        "state: refused",
        "launched: false",
        "writer_started: false",
        f"reason: {reason}",
        "result refused",
    ]
    return "\n".join(lines) + "\n"


def emit_refusal(text: str) -> int:
    sys.stdout.write(text)
    return 2


def perform(binding_path: str, *, hook=None, pins=None, fault=None, guard_path: str | None = None) -> int:
    selected = default_guard() if guard_path is None else guard_path
    try:
        chosen = require_guard(selected)
        assert_siblings()
    except GuardMismatch as exc:
        write_sidecar(binding_path, exc.detail)
        return emit_refusal(refusal_text("guard-pin", "guard pin mismatch before launch"))
    except PinMismatch as exc:
        return emit_refusal(refusal_text("pin", exc.detail))
    module = load_handoff()
    original = module.launch

    def wrapped_launch(script: str, args: list[str], active_pins: dict):
        command = args[0] if args else ""
        if command in SWITCHED:
            try:
                script = require_guard(chosen)
            except GuardMismatch:
                module.refuse("guard pin mismatch before launch")
        return original(script, args, active_pins)

    module.launch = wrapped_launch
    try:
        return module.perform(binding_path, hook=hook, pins=pins, fault=fault)
    finally:
        module.launch = original


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if any(item == "--guard" or item.startswith("--guard=") for item in args):
        return emit_refusal(refusal_text("guard-pin", "guard override is refused"))
    if len(args) != 3 or args[0] != "perform" or args[1] != "--binding":
        sys.stderr.write("refused: usage is perform --binding PATH\n")
        return 2
    return perform(args[2])


if __name__ == "__main__":
    sys.exit(main())
