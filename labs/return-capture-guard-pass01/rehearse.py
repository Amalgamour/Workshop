#!/usr/bin/env python3
"""Run the disposable guard suite. This does not select the app."""

from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "tests" / "run_suite.py"), run_name="__main__")
