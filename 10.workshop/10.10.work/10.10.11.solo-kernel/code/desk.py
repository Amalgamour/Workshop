#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""desk.py — the repo walk and the desk live file.

The kernel folder names stay here. The other programs import them.
The repo is the folder that holds 10.workshop and 00.00.00.kernel.draft.
A machine path is not stored.
"""
# ## notes
# born: 2026-10-15
# source: grok-prime, colab solo-kernel pass 01
# who is passed by the command or the brief. This module does not choose a who.

from __future__ import annotations

import sys
from pathlib import Path

CHECK_KERNEL = "00.00.00.kernel"
DRAFT_KERNEL = "00.00.00.kernel.draft"
KERNEL_OWNER = "00.00.00.kernel"
SOLO = "10.10.11.solo-kernel"
LIVE_KEYS = ("book", "owner", "sitting")


def die(msg: str) -> None:
    sys.exit(f"stop: {msg}")


def repo_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for cand in (here, *here.parents):
        if (cand / "10.workshop").is_dir() and (cand / DRAFT_KERNEL).is_dir():
            return cand
    die("repo root not found")


def solo_root(start: Path | None = None) -> Path:
    return repo_root(start) / "10.workshop" / "10.10.work" / SOLO


def live_fields(text: str) -> dict[str, str]:
    found = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        if key in LIVE_KEYS and key not in found:
            found[key] = val.strip().strip("`")
    return found


def read_live(desk: Path) -> dict[str, str]:
    path = desk / "00.live.md"
    if not path.is_file():
        die("00.live is missing")
    return live_fields(path.read_text(encoding="utf-8"))


def need(args: list[str], flag: str) -> str:
    if flag not in args:
        die(f"{flag} is required")
    slot = args.index(flag) + 1
    if slot >= len(args):
        die(f"{flag} is required")
    return args[slot]
