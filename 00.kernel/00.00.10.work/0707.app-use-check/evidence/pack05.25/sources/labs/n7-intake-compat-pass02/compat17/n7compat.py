#!/usr/bin/env python3
"""Documented adapter (0707/05.17): lets the UNCHANGED pass01 test file (copied byte-identical into
compat17/tests/) drive pass02. The old API had one context-free parser; the historical cases are N7
inputs, so make_parser() here is the pass02 parser fixed to N7 context. The CLI forwards unchanged
(the 0707.app-use-check page is N7, so intake sets N7 context itself).
Results through this adapter are ADAPTED author cases, not independent coverage.
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import n7compat2  # noqa: E402

load_pass03 = n7compat2.load_pass03


def make_parser(p3):
    return n7compat2.make_parser(p3, kind_fn=lambda: "N7NN")


def main(argv=None):
    return n7compat2.main(argv)


if __name__ == "__main__":
    sys.exit(main())
