#!/usr/bin/env python3
"""Successor rehearsal. It does not delete its work root or any earlier run."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    target = Path(__file__).resolve().parent / "tests" / "run_suite.py"
    sys.argv = [str(target), *sys.argv[1:]]
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
