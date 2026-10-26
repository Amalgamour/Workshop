#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slot.py — the lowest open member in a band.

Law 0034. A door ends in 0 and is not a member.
The lowest missing number in the next nine is the slot.
A folder that exists is taken, including a .test page.
A name ending in .09 is not free.
This program lists. It does not make a folder.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, law band 0000-0100
# who: grok-prime

from __future__ import annotations

import re
import sys
from pathlib import Path

NUM_RE = re.compile(r"^(\d{4})(?:\.|$)")


def die(msg: str) -> None:
    sys.exit(f"stop: {msg}")


def number_of(name: str) -> int | None:
    hit = NUM_RE.match(name)
    if not hit:
        return None
    return int(hit.group(1))


def parse_door(text: str) -> int:
    if not re.fullmatch(r"\d{1,4}", str(text).strip()):
        die("door ends in 0")
    door = int(text)
    if door % 10 != 0 or door > 9990:
        die("door ends in 0")
    return door


def model_door(door: int) -> str:
    """A full decade below 1000 names the next model door. It does not open door + 10 in the reserved band."""
    if 100 <= door <= 180:
        return f"{door + 10:04d}"
    if door == 190:
        return ""
    if door < 1000:
        return "0100"
    return ""


def next_member(door: int, taken) -> str:
    door = parse_door(str(door))
    used = used_numbers(taken)
    for number in range(door + 1, door + 10):
        if number not in used:
            return f"{number:04d}"
    nxt = model_door(door)
    if nxt:
        die(f"no slot. the next model door is {nxt}")
    if door == 190:
        die("no slot. model range 0100 through 0199 is full")
    die("no slot")


def used_numbers(taken) -> set[int]:
    used = set()
    for name in taken:
        number = number_of(str(name))
        if number is not None:
            used.add(number)
    return used


def next_open(start: int, taken) -> str:
    """Lowest free number at or after start. An open band does not stop on 9."""
    if not isinstance(start, int) or start < 0 or start > 9999:
        die("start is out of range")
    used = used_numbers(taken)
    for number in range(start, 10000):
        if number not in used:
            return f"{number:04d}"
    die("no slot")


def taken_names(book: Path) -> list[str]:
    if not book.is_dir():
        die("book folder is missing")
    return sorted(path.name for path in book.iterdir() if path.is_dir())


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    got = next_member(10, ["0011.contents", "0012.old.09", "0014.test"])
    check(got == "0013", "lowest missing")
    check(next_member(0, []) == "0001", "first member")
    check(next_member(10, ["0010.about"]) == "0011", "door is not a member")
    full = [f"{n:04d}.item" for n in range(21, 30)]
    try:
        next_member(20, full)
        die("test returned a slot from a full band")
    except SystemExit as exc:
        check("no slot" in str(exc), "full band stops")
    try:
        next_member(21, [])
        die("test accepted a door")
    except SystemExit as exc:
        check("door ends in 0" in str(exc), "door stops")
    full60 = [f"{n:04d}.item" for n in range(601, 610)]
    try:
        next_member(600, full60)
        die("test returned a slot from 0600")
    except SystemExit as exc:
        check("no slot" in str(exc) and "0100" in str(exc), "0600 names 0100")
        check("0610" not in str(exc), "0610 is not the next door")
    full01 = [f"{n:04d}.item" for n in range(101, 110)]
    try:
        next_member(100, full01)
        die("test returned a slot from 0100")
    except SystemExit as exc:
        check("0110" in str(exc), "0100 names 0110")
    taken = [f"{n:04d}.item" for n in range(1000, 1010)]
    check(next_open(1001, taken) == "1010", "open band continues")
    check(next_open(1001, []) == "1001", "open band starts at the first member")
    print("test: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, or next DOOR --book PATH")
    if args[0] == "test":
        cmd_test()
        return
    if args[0] == "next":
        if "--book" not in args or len(args) < 4:
            die("next DOOR --book PATH")
        door = parse_door(args[1])
        book = Path(args[args.index("--book") + 1])
        print(next_member(door, taken_names(book)))
        return
    die("use test, or next DOOR --book PATH")


if __name__ == "__main__":
    main()
