#!/usr/bin/env python3
"""Staging adapter for 0522/05.14. Drives the staged canonical pass04. Not a production module.

load_pass03 stays the pinned pass03 loader. candidate() loads the staged workbook at
D:\\Git\\lib-build\\labs\\workbook-review-pass04\\workbook.py and checks the production pin.
A call without --patch delegates to the pass02 baseline. A call with --patch strips
--repo-root and runs that canonical file. It does not copy the workbook into a fixture.
"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
REAL = LIVE / "labs/n7-intake-compat-pass02/n7compat2.py"
P4_REL = "labs/workbook-review-pass04/workbook.py"
PIN_SHA = "b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2"
PIN_BYTES = 6508
_P4 = None


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


real = _load(REAL, "n7compat2_real_0517")
load_pass03 = real.load_pass03


def _staged_bytes() -> bytes:
    path = LIVE / P4_REL
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != PIN_SHA or len(data) != PIN_BYTES:
        raise SystemExit("refused: staged pass04 differs from the production pin")
    return data


def candidate():
    global _P4
    if _P4 is None:
        _staged_bytes()
        _P4 = _load(LIVE / P4_REL, "workbook_review_pass04_staged")
    return _P4


def make_parser(p3=None, kind_fn=None):
    p4 = candidate()

    def parse_pointer(body):
        if kind_fn is None:
            return p4.parse_pointer(body)
        token = p4.KIND.set(kind_fn())
        try:
            return p4.parse_pointer(body)
        finally:
            p4.KIND.reset(token)

    return parse_pointer


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--patch" not in args:
        return real.main(args)
    args.remove("--patch")
    if "--repo-root" in args:
        index = args.index("--repo-root")
        del args[index:index + 2]
    _staged_bytes()
    proc = subprocess.run(
        [sys.executable, "-B", str(LIVE / P4_REL), *args],
        cwd=str(LIVE),
        env=dict(__import__("os").environ, PYTHONDONTWRITEBYTECODE="1"),
    )
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
