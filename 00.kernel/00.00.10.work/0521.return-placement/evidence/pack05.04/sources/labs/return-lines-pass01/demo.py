#!/usr/bin/env python3
"""File one synthetic pass on a temporary book and print its descriptor.

The book is disposable. This demo does not touch the live work book.
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import return_lines as rl


def main() -> int:
    with tempfile.TemporaryDirectory() as outer:
        book = os.path.join(outer, "book")
        os.mkdir(book)
        note = os.path.join(outer, "note.md")
        ret = os.path.join(outer, "return.md")
        with open(note, "wb") as handle:
            handle.write(b"SYNTHETIC NEW WORK\n")
        with open(ret, "wb") as handle:
            handle.write(b"SYNTHETIC RETURN\n")
        opened = rl.init_run(book, "00.00.10.work")
        if opened["exit"] != 0:
            sys.stdout.buffer.write(rl.dump(opened))
            return int(opened["exit"])
        reserved = rl.reserve_run(
            book, "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic",
            ["note.md"], "grok-1", "codex-prime", "prepared", None,
        )
        if reserved["exit"] != 1:
            sys.stdout.buffer.write(rl.dump(reserved))
            return int(reserved["exit"])
        captured = rl.capture_run(
            book, "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic",
            ret, [("note.md", note)],
        )
        if captured["exit"] != 0 or captured["descriptor"] is None:
            sys.stdout.buffer.write(rl.dump(captured))
            return int(captured["exit"])
        sys.stdout.buffer.write(rl.dump(captured["descriptor"]))
        return 0


if __name__ == "__main__":
    sys.exit(main())
