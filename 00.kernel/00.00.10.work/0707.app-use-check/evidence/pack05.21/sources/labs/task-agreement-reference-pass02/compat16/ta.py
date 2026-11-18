#!/usr/bin/env python3
"""Documented shim (0707/05.15): lets the UNCHANGED pass01 test file (copied byte-identical into
compat16/tests/) drive pass02 ta2.py. It only inserts --lab-root from TA_LAB_ROOT for write commands.
Results through this shim are ADAPTED author cases, not independent coverage.
"""
import os
import subprocess
import sys
from pathlib import Path

TA2 = Path(__file__).resolve().parents[1] / "ta2.py"
args = sys.argv[1:]
if args and args[0] in ("construct", "assemble", "bind") and "--lab-root" not in args:
    args = [args[0], "--lab-root", os.environ["TA_LAB_ROOT"], *args[1:]]
sys.exit(subprocess.call([sys.executable, "-B", str(TA2), *args]))
