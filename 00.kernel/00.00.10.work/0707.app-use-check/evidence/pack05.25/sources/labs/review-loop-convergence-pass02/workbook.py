#!/usr/bin/env python3
"""Convergence workbook successor (0522/05.18, note 06.39).

Loads the frozen pass01 workbook from its canonical pin and replaces fence
classification. This file is the executed workbook on a disposable candidate
root. It does not require its own path to be canonical, and it does not copy
or rewrite predecessor modules. A pin mismatch refuses. There is no other root.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PASS01_REL = "labs/review-loop-convergence-pass01/workbook.py"
PASS01_SHA = "ef021d4ae4066f97bfb21017d5a7952ac5161dce82e82ebec1ca756e3f58f9d9"
PASS01_BYTES = 20034
POINTER_MARK = b"## Return pointer"
REVIEW_MARK = b"## Review"


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def _sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def load_pass01():
    path = REPO / PASS01_REL
    if path.is_symlink() or not path.is_file():
        refuse_boot("pass01 workbook pin is missing")
    data = path.read_bytes()
    if len(data) != PASS01_BYTES or _sha(data) != PASS01_SHA:
        refuse_boot("pass01 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_loop_convergence_pass01", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass01 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_pass01()


def _lines(blob: bytes) -> list[tuple[int, bytes]]:
    lines: list[tuple[int, bytes]] = []
    index = 0
    size = len(blob)
    while index < size:
        found = blob.find(b"\n", index)
        if found < 0:
            chunk = blob[index:]
            if chunk.endswith(b"\r"):
                chunk = chunk[:-1]
            lines.append((index, chunk))
            break
        chunk = blob[index:found]
        if chunk.endswith(b"\r"):
            chunk = chunk[:-1]
        lines.append((index, chunk))
        index = found + 1
    if not lines:
        lines.append((0, b""))
    return lines


def _is_pointer(text: bytes) -> bool:
    if not text.startswith(POINTER_MARK):
        return False
    return text[len(POINTER_MARK):].strip() == b""


def _is_review(text: bytes) -> bool:
    return text == REVIEW_MARK or text.startswith(REVIEW_MARK + b" ")


def _marker_run(stripped: bytes):
    if not stripped:
        return None
    mark = stripped[:1]
    if mark not in (b"`", b"~"):
        return None
    count = 0
    while count < len(stripped) and stripped[count:count + 1] == mark:
        count += 1
    if count < 3:
        return None
    return mark, count, stripped[count:]


def _open_fence(stripped: bytes):
    parsed = _marker_run(stripped)
    if parsed is None:
        return None
    mark, count, rest = parsed
    if mark == b"`" and b"`" in rest:
        return None
    return mark, count


def _close_fence(stripped: bytes, mark: bytes, count: int) -> bool:
    parsed = _marker_run(stripped)
    if parsed is None:
        return False
    got, length, rest = parsed
    return got == mark and length >= count and rest.strip() == b""


def classify_pack(blob: bytes) -> dict:
    """One unfenced pointer and one unfenced review. Ambiguous structure has no bound hash."""
    if not isinstance(blob, (bytes, bytearray)):
        return {"bound_sha256": None, "body_sha256": None, "sha256": None, "structure": "ambiguous"}
    raw = bytes(blob)
    pointers: list[int] = []
    reviews: list[int] = []
    unclosed = False
    mark = None
    length = 0
    for start, text in _lines(raw):
        stripped = text.strip()
        if mark is None:
            opened = _open_fence(stripped)
            if opened is not None:
                mark, length = opened
                continue
        elif _close_fence(stripped, mark, length):
            mark = None
            length = 0
            continue
        else:
            continue
        if _is_pointer(text):
            pointers.append(start)
        elif _is_review(text):
            reviews.append(start)
    unclosed = mark is not None
    status = "clear"
    if unclosed:
        status = "ambiguous"
    elif not pointers or not reviews:
        status = "missing"
    elif len(pointers) != 1 or len(reviews) != 1 or reviews[0] <= pointers[0]:
        status = "ambiguous"
    full = _sha(raw)
    if status != "clear":
        return {"bound_sha256": None, "body_sha256": None, "sha256": full, "structure": status}
    return {
        "bound_sha256": _sha(raw[: reviews[0]]),
        "body_sha256": _sha(raw[: pointers[0]]),
        "sha256": full,
        "structure": "clear",
    }


def pointer_body(blob: bytes) -> str | None:
    mark = None
    length = 0
    pointer_at = None
    for start, text in _lines(blob):
        stripped = text.strip()
        if mark is None:
            opened = _open_fence(stripped)
            if opened is not None:
                mark, length = opened
                continue
        elif _close_fence(stripped, mark, length):
            mark = None
            length = 0
            continue
        else:
            continue
        if pointer_at is None and _is_pointer(text):
            newline = blob.find(b"\n", start)
            pointer_at = len(blob) if newline < 0 else newline + 1
        elif pointer_at is not None and _is_review(text):
            if start < pointer_at:
                return None
            return blob[pointer_at:start].decode("utf-8", "replace").strip("\n")
    return None


def pointer_block(text):
    """Use the unfenced declaration when backtick or tilde fences leave one clear pair.

    Pages with no fence marker keep the historical cutter. Ambiguous or missing
    structure keeps it too. This function does not choose among several headings.
    """
    if not isinstance(text, str) or ("```" not in text and "~~~" not in text):
        return base.BASE_POINTER(text)
    blob = text.encode("utf-8")
    if classify_pack(blob).get("structure") != "clear":
        return base.BASE_POINTER(text)
    body = pointer_body(blob)
    if body is None:
        return base.BASE_POINTER(text)
    return body


base.classify_pack = classify_pack
base.pointer_block = pointer_block
base.wb.pointer_block = pointer_block


def main(argv: list[str] | None = None) -> int:
    return base.main(argv)


if __name__ == "__main__":
    sys.exit(main())
