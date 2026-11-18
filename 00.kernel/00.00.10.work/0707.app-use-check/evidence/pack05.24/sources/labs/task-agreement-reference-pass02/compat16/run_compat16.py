#!/usr/bin/env python3
"""Run the unchanged pass01 16-case test file against pass02 through the shim. usage: run_compat16.py --root NEW --out NEW"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
env = dict(os.environ, TA_LAB_ROOT=str(Path(a.root).resolve()), PYTHONDONTWRITEBYTECODE="1")
test = Path(__file__).resolve().parent / "tests" / "test_ta.py"
sys.exit(subprocess.call([sys.executable, "-B", str(test), "--root", a.root, "--out", a.out], env=env))
