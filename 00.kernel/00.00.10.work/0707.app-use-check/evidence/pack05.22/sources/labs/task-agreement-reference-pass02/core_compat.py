#!/usr/bin/env python3
"""Exact-observation adapter for the frozen core helper `measured_agreement` (0707/05.15). NONPRODUCTION.

It does NOT import labs/workbook-review-pass01/workbook.py (no module top level runs). It reads the
pinned bytes, checks sha256, extracts by AST only `IDENT`, `sha256_bytes`, `section_between`,
`first_paragraph`, `finish_items` and `measured_agreement`, and executes those definitions in a clean
namespace holding only `re` and `hashlib`. `observe(page_bytes)` reproduces the core's call
(workbook.py line 734: data.decode("utf-8", "replace") then measured_agreement(text)).
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

PIN = {"path": "labs/workbook-review-pass01/workbook.py", "sha256": None, "bytes": 79131}
NAMES = ("IDENT", "sha256_bytes", "section_between", "first_paragraph", "finish_items", "measured_agreement")
_NS: dict | None = None


def load(checkout: Path, expected_sha256: str) -> dict:
    global _NS
    src = (checkout / PIN["path"]).read_bytes()
    got = hashlib.sha256(src).hexdigest()
    if got != expected_sha256 or len(src) != PIN["bytes"]:
        raise RuntimeError(f"frozen helper differs from its pin: {got} {len(src)}")
    text = src.decode("utf-8")
    tree = ast.parse(text)
    parts = {}
    for node in tree.body:
        name = node.name if isinstance(node, ast.FunctionDef) else (node.targets[0].id if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) else None)
        if name in NAMES:
            parts[name] = ast.get_source_segment(text, node)
    missing = [n for n in NAMES if n not in parts]
    if missing:
        raise RuntimeError(f"helper parts not found: {missing}")
    ns = {"re": re, "hashlib": hashlib, "__builtins__": __builtins__}
    exec("from __future__ import annotations\n" + "\n\n".join(parts[n] for n in NAMES), ns)
    _NS = ns
    return {"path": PIN["path"], "sha256": got, "bytes": len(src), "extracted": list(NAMES),
            "extracted_sha256": hashlib.sha256("\n\n".join(parts[n] for n in NAMES).encode()).hexdigest()}


def observe(page_bytes: bytes) -> dict:
    if _NS is None:
        raise RuntimeError("load() first")
    text = page_bytes.decode("utf-8", "replace")          # as workbook.py line 734
    agreement, goal, director = _NS["measured_agreement"](text)
    return {"agreement": agreement, "goal": goal, "director_text": director}
