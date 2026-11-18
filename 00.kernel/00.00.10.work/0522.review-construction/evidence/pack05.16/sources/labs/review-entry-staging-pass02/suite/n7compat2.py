#!/usr/bin/env python3
"""Staging adapter for 0522/05.15. Drives the staged canonical pass05. Not a production module.

load_pass03 stays the pinned pass03 loader. candidate() loads the staged workbook at
D:\\Git\\lib-build\\labs\\workbook-review-pass05\\workbook.py and checks its pin.
A call without --patch delegates to the pass02 baseline. A call with --patch strips
--repo-root and runs that canonical file. It does not copy the workbook into a fixture
and it does not retarget REPO.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
REAL = LIVE / "labs/n7-intake-compat-pass02/n7compat2.py"
P5_REL = "labs/workbook-review-pass05/workbook.py"
PIN_SHA = "86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991"
PIN_BYTES = 6994
_P5 = None


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


real = _load(REAL, "n7compat2_real_0517")
load_pass03 = real.load_pass03


def _staged_bytes() -> bytes:
    path = LIVE / P5_REL
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != PIN_SHA or len(data) != PIN_BYTES:
        raise SystemExit("refused: staged pass05 differs from the production pin")
    return data


def candidate():
    global _P5
    if _P5 is None:
        _staged_bytes()
        _P5 = _load(LIVE / P5_REL, "workbook_review_pass05_staged")
    return _P5


def make_parser(p3=None, kind_fn=None):
    p5 = candidate()

    def parse_pointer(body):
        if kind_fn is None:
            return p5.parse_pointer(body)
        token = p5.KIND.set(kind_fn())
        try:
            return p5.parse_pointer(body)
        finally:
            p5.KIND.reset(token)

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
        [sys.executable, "-B", str(LIVE / P5_REL), *args],
        cwd=str(LIVE),
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
    )
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
