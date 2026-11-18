#!/usr/bin/env python3
"""N5 book-instance applicability (0522/05.16, note 06.34).

A thin successor of the pinned pass05 workbook. Pass05, pass04, pass03, pass02, and pass01
stay byte-identical. N7 strict parsing stays the pass05 parser. This layer holds N5 current
applicability when the stored book identity and the live book identity disagree.
Same-instance N5 checks, and every non-N5 check, stay on the predecessor source_changed.
This file refuses to run from any root other than D:\\Git\\lib-build.
"""

from __future__ import annotations

import contextvars
import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
CANONICAL_FILE = REPO / "labs" / "review-instance-binding-pass01" / "workbook.py"
PASS05_REL = "labs/workbook-review-pass05/workbook.py"
PASS05_SHA = "86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991"
PASS05_BYTES = 6994
HEX = set("0123456789abcdef")
HOLD = contextvars.ContextVar("review_instance_n5_hold", default=None)


def load_pass05():
    here = Path(__file__).resolve()
    if os.path.normcase(str(here)) != os.path.normcase(str(CANONICAL_FILE)):
        print("refused: review-instance workbook is not at its canonical root", file=sys.stderr)
        raise SystemExit(2)
    path = REPO / PASS05_REL
    data = path.read_bytes()
    if len(data) != PASS05_BYTES or hashlib.sha256(data).hexdigest() != PASS05_SHA:
        print("refused: pass05 workbook pin mismatch", file=sys.stderr)
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location("workbook_review_pass05", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p5 = load_pass05()
p2 = p5.p3.p2
wb = p5.p3.wb
BASE_CHANGED = p2.source_changed
BASE_RESULT = wb.result
BASE_PERFORM = wb.perform


def instance_id_for(book_text: str, source: str, pass_id: str) -> str:
    return wb.sha256_bytes(wb.canonical({"book": book_text, "pass": pass_id, "source": source}))


def plausible_book(text: str) -> bool:
    if not isinstance(text, str) or text.strip() == "":
        return False
    if text.startswith("\\\\") or text.startswith("//"):
        return False
    path = Path(text)
    return path.is_absolute() and ".." not in path.parts


def resolved_directory(text: str) -> str | None:
    if not plausible_book(text):
        return None
    path = Path(text)
    if wb.is_link(path) or not path.is_dir():
        return None
    try:
        current = path.resolve()
    except OSError:
        return None
    walked = current
    while True:
        if wb.is_link(walked):
            return None
        parent = walked.parent
        if parent == walked:
            break
        walked = parent
    return str(current)


def _instance_ok(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in HEX for char in value)


def _hold(reason: str, stored_book, live_text: str, stored_instance, live_instance) -> dict:
    return {
        "current": False,
        "live_book": live_text,
        "live_instance_id": live_instance,
        "reason": reason,
        "state": "held",
        "stored_book": stored_book if isinstance(stored_book, str) else None,
        "stored_instance_id": stored_instance if isinstance(stored_instance, str) else None,
    }


def n5_instance_hold(stored, live, book: Path) -> dict | None:
    """None means this layer leaves the predecessor comparison in place."""
    if not isinstance(live, dict) or live.get("kind") != "N5NN" or not isinstance(stored, dict):
        return None
    live_text = str(book)
    page = live.get("page")
    pass_id = live.get("pass")
    stored_book = stored.get("book")
    stored_instance = stored.get("instance_id")
    if not isinstance(page, str) or not isinstance(pass_id, str):
        return _hold("unbound", stored_book, live_text, stored_instance, None)
    live_instance = instance_id_for(live_text, page, pass_id)
    if live.get("book") != live_text:
        return _hold("identifier-disagreement", stored_book, live_text, stored_instance, live_instance)
    if not isinstance(stored_book, str) or not _instance_ok(stored_instance):
        return _hold("unbound", stored_book, live_text, stored_instance, live_instance)
    resolved = resolved_directory(stored_book)
    if resolved == live_text and stored_instance == live_instance:
        return None
    if resolved == live_text or stored_instance == live_instance:
        return _hold("identifier-disagreement", stored_book, live_text, stored_instance, live_instance)
    if resolved is not None:
        return _hold("different-root", stored_book, live_text, stored_instance, live_instance)
    if plausible_book(stored_book):
        return _hold("relocation-or-clone", stored_book, live_text, stored_instance, live_instance)
    return _hold("unbound", stored_book, live_text, stored_instance, live_instance)


def source_changed(book: Path, stored, live: dict, journal: dict) -> bool:
    HOLD.set(None)
    hold = n5_instance_hold(stored, live, book)
    if hold is not None:
        HOLD.set(hold)
        return True
    return BASE_CHANGED(book, stored, live, journal)


def result(command: str, intake, exit_code: int, **extra) -> dict:
    body = BASE_RESULT(command, intake, exit_code, **extra)
    hold = HOLD.get()
    if hold is not None and "instance_applicability" not in body:
        body = dict(body)
        body["instance_applicability"] = hold
        HOLD.set(None)
    return body


def perform(args: list[str]) -> int:
    HOLD.set(None)
    return BASE_PERFORM(args)


p2.source_changed = source_changed
wb.result = result
wb.perform = perform
p2.perform = perform


def main(argv: list[str] | None = None) -> int:
    return p5.main(argv)


if __name__ == "__main__":
    sys.exit(main())
