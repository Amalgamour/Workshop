#!/usr/bin/env python3
"""Development pin for the return-line tool. Not kernel law.

The paths and hashes below are development wiring. They are not kernel law.
A receipt is custody. It is not review, acceptance, or publication.
This door does not allocate a sequential member and it does not edit a shared facade.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPARSE = 0x400
PINS = {
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


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def check_pins(root: str) -> str | None:
    for name, pin in PINS.items():
        path = os.path.join(root, *pin["path"].split("/"))
        if not os.path.lexists(path):
            return f"pin missing: {name}"
        st = os.lstat(path)
        attrs = getattr(st, "st_file_attributes", 0) or 0
        if attrs & REPARSE or stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            return f"pin is not a regular file: {name}"
        with open(path, "rb") as handle:
            data = handle.read()
        digest = hashlib.sha256(data).hexdigest()
        if digest != pin["sha256"] or len(data) != pin["bytes"]:
            return f"pin mismatch: {name}"
    return None


def main(argv: list[str] | None = None) -> int:
    root = repo_root()
    problem = check_pins(root)
    if problem:
        sys.stderr.write(problem + "\n")
        return 2
    script = os.path.join(root, *PINS["return_lines"]["path"].split("/"))
    command = [sys.executable, "-B", script, *(sys.argv[1:] if argv is None else argv)]
    return subprocess.run(command, cwd=root).returncode


if __name__ == "__main__":
    sys.exit(main())
