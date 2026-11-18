#!/usr/bin/env python3
"""DOCUMENTED TEST ADAPTER (0707/05.18). Lets the UNCHANGED 05.17 test files drive the ACTUAL candidate pass04.

Same API as labs/n7-intake-compat-pass02/n7compat2.py, but every patched path is the candidate workbook bytes:
- load_pass03(): the PURE pinned pass03 (the real 05.17 loader), so OLD comparisons stay against pass03.
- make_parser(p3, kind_fn): calls the candidate pass04 module's parse_pointer with pass04.KIND set from kind_fn
  (None: no context). p3 is ignored. The candidate module is imported from RIE_CANDIDATE_ROOT (required),
  a disposable root built by rie.py, so its canonical-root guard is satisfied by the lab adapter line.
- CLI without --patch: the real 05.17 baseline (pinned pass03, explicit --repo-root).
- CLI with --patch: copies the candidate adapter pass04 bytes (verified against the lab v8 pin) into the
  fixture repo and runs THAT file as a new process; no in-process patching.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LABDIR = LIVE / "labs/review-entry-integration-pass01"
REAL = LIVE / "labs/n7-intake-compat-pass02/n7compat2.py"
P4_REL = "labs/workbook-review-pass04/workbook.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


real = _load(REAL, "n7compat2_real_0517")
load_pass03 = real.load_pass03
_PIN = json.loads((LABDIR / "adapter/review-loop-v8.lab.json").read_bytes())["tools"]["workbook"]
_P4 = None


def candidate():
    global _P4
    if _P4 is None:
        root = os.environ.get("RIE_CANDIDATE_ROOT")
        if not root:
            raise SystemExit("refused: RIE_CANDIDATE_ROOT is not set")
        path = Path(root) / P4_REL
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != _PIN["sha256"] or len(data) != _PIN["bytes"]:
            raise SystemExit("refused: candidate pass04 differs from the lab v8 pin")
        _P4 = _load(path, "workbook_review_pass04_candidate")
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
    i = args.index("--repo-root")
    repo = Path(args[i + 1])
    del args[i:i + 2]
    src = Path(os.environ["RIE_CANDIDATE_ROOT"]) / P4_REL
    data = src.read_bytes()
    if hashlib.sha256(data).hexdigest() != _PIN["sha256"]:
        raise SystemExit("refused: candidate pass04 differs from the lab v8 pin")
    dst = repo / P4_REL
    if dst.exists():
        if dst.read_bytes() != data:
            raise SystemExit("refused: a different pass04 is already in the fixture repo")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
    return subprocess.run([sys.executable, "-B", str(dst), *args], env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")).returncode


if __name__ == "__main__":
    sys.exit(main())
