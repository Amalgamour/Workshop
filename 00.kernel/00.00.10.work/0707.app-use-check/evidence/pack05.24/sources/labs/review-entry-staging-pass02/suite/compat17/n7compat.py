#!/usr/bin/env python3
"""DOCUMENTED TEST ADAPTER (0522/05.15): the unchanged historical pass01 cases against pass05.

The historical cases are N7 inputs, so make_parser() is the candidate parser in N7 context.
Results are adapted author cases. G7 stays a labelled revised expectation.
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
