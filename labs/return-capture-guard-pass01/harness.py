#!/usr/bin/env python3
"""One-process selector from the packed handoff onto the guard.

The handoff file and its TOOL_FILES stay as sealed. check_pins still
requires the historical capture, inspect, and clerk bytes. A capture
launch in this process uses return_capture_guard.py. Inspect and verify
keep the packed paths. This module does not edit app files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HANDOFF_REL = "labs/capture-handoff-pass01/handoff.py"
HANDOFF_SHA = "a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a"
HANDOFF_BYTES = 51828
GUARD_REL = "labs/return-capture-guard-pass01/return_capture_guard.py"


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def guard_path() -> str:
    return os.path.join(repo_root(), *GUARD_REL.split("/"))


def handoff_path() -> str:
    return os.path.join(repo_root(), *HANDOFF_REL.split("/"))


def pin_ok() -> tuple[bool, str]:
    path = handoff_path()
    if not os.path.isfile(path):
        return False, "handoff pin is missing"
    with open(path, "rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != HANDOFF_SHA or len(data) != HANDOFF_BYTES:
        return False, "handoff pin mismatch"
    return True, digest


def load_handoff():
    ok, detail = pin_ok()
    if not ok:
        raise RuntimeError(detail)
    path = handoff_path()
    spec = importlib.util.spec_from_file_location("capture_handoff_pass01_pinned", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("handoff did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perform(binding: str) -> int:
    """Run the packed handoff once, with capture selected to the guard."""
    handoff = load_handoff()
    real = handoff.launch
    selected = guard_path()

    def launch(script: str, args: list[str], pins: dict):
        if args and args[0] == "capture":
            script = selected
        return real(script, args, pins)

    handoff.launch = launch
    try:
        return handoff.perform(binding)
    finally:
        handoff.launch = real
