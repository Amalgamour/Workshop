#!/usr/bin/env python3
"""DOCUMENTED TEST ADAPTER (0707/05.18): the unchanged historical pass01 cases against the ACTUAL candidate pass04.
The historical cases are N7 inputs, so make_parser() is the candidate parser in N7 context.
Results are ADAPTED author cases, not independent coverage; G7 is a labelled revised expectation (K1).
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import n7compat2  # noqa: E402   the 05.18 cases adapter (candidate pass04)

load_pass03 = n7compat2.load_pass03


def make_parser(p3):
    return n7compat2.make_parser(p3, kind_fn=lambda: "N7NN")


def main(argv=None):
    return n7compat2.main(argv)


if __name__ == "__main__":
    sys.exit(main())
