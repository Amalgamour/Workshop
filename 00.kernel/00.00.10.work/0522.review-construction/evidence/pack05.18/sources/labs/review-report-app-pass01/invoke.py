#!/usr/bin/env python3
"""Run the proposed dispatcher with __file__ pointed at the installed app.

This refuses when app/librarian.py is not the pinned bytes. It does not
write that file. Executing labs/review-report-app-pass01/librarian.py
directly is a different process and is not this harness.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

PIN_BYTES = 12204
PIN_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    lab = Path(__file__).resolve().parent
    root = lab.parents[1]
    live = root / "app" / "librarian.py"
    data = live.read_bytes()
    if len(data) != PIN_BYTES or hashlib.sha256(data).hexdigest() != PIN_SHA:
        print("stop: installed dispatcher is not the pinned bytes", file=sys.stderr)
        raise SystemExit(2)
    proposed_path = lab / "librarian.py"
    proposed = proposed_path.read_bytes()
    if b"\r" in proposed:
        print("stop: proposed dispatcher is not lf", file=sys.stderr)
        raise SystemExit(2)
    filename = str(live)
    sys.argv = [filename, *args]
    namespace = {"__name__": "__main__", "__file__": filename, "__package__": None}
    exec(compile(proposed.decode("utf-8"), filename, "exec"), namespace)


if __name__ == "__main__":
    main()
