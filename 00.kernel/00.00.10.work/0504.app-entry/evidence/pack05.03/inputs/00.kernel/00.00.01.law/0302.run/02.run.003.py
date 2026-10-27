#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 003
# Authorization: draft — 2026-10-26
# who: grok-4.7
# state: draft
# Face: 02
# PPPP: 0302
# desk: 00.kernel
# shelf: 00.kernel
# book: 00.00.01.law
# keyword: run
# why: Development runner for one declared fixture inventory. A designated container may sit inside the work book. Normal run stays refused.
#
# cite: 00.kernel/00.00.10.work/0504.app-entry/05.02.md

"""Development runner candidate. The app entry loads this file by path after a hash match.

Direct execution is refused. This module does not choose a page by climbing, by
the current directory, or by the highest version number. It does not import
02.run.001.py or 02.run.002.py. The adaptation notes are 06.02.md on this page.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

FACE_RE = re.compile(r"^02\.([A-Za-z_][A-Za-z0-9_]*)\.py$")
STAMP_KEYS = (
    "version",
    "Authorization",
    "who",
    "state",
    "Face",
    "PPPP",
    "desk",
    "shelf",
    "book",
    "keyword",
    "why",
    "cite",
)
OWN_STAMP = {
    "version": "003",
    "PPPP": "0302",
    "desk": "00.kernel",
    "shelf": "00.kernel",
    "book": "00.00.01.law",
    "keyword": "run",
    "Face": "02",
}


def die(msg: str) -> None:
    print(f"stop: {msg}", file=sys.stderr)
    raise SystemExit(2)


def first_fence(text: str) -> str:
    lines = text.splitlines()
    start = None
    mark = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if start is None:
            opened = re.match(r"^(```+|~~~+)(.*)$", stripped)
            if not opened:
                continue
            start = i + 1
            mark = opened.group(1)
            continue
        closed = re.match(r"^(```+|~~~+)\s*$", stripped)
        if closed and closed.group(1)[0] == mark[0] and len(closed.group(1)) >= len(mark):
            return "\n".join(lines[start:i])
    if start is None:
        die("card has no fence")
    die("card fence does not close")


def parse_uses(body: str) -> tuple[str, str]:
    parts = body.split()
    if len(parts) == 1:
        return parts[0], ""
    if len(parts) == 3 and parts[1] == "as":
        return parts[0], parts[2]
    die(f"uses line is not a face: {body}")


def parse_card(text: str) -> dict:
    fence = first_fence(text)
    runs = None
    uses = []
    args = None
    for raw in fence.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("runs:"):
            if runs is not None:
                die("card has two runs")
            runs = line.split(":", 1)[1].strip()
        elif line.startswith("uses:"):
            uses.append(parse_uses(line.split(":", 1)[1].strip()))
        elif line.startswith("args:"):
            if args is not None:
                die("card has two args")
            args = shlex.split(line.split(":", 1)[1].strip())
        else:
            die(f"card line is not runs, uses, or args: {line}")
    if not runs:
        die("card has no runs")
    return {"runs": runs, "uses": uses, "args": args or []}


def plain_name(filename: str, alias: str) -> str:
    if filename != Path(filename).name:
        die(f"module has no face address: {filename}")
    hit = FACE_RE.fullmatch(filename)
    if not hit:
        die(f"module has no face address: {filename}")
    stem = hit.group(1)
    if alias and alias != stem:
        die(f"uses name does not match the face: {filename}")
    return stem


def stamp_text(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeError:
        die(f"code face is not utf-8: {path.name}")
    got = []
    for line in lines[2:]:
        if line.startswith("#"):
            got.append(line[1:].strip())
            continue
        if line.strip() == "":
            continue
        break
    return "\n".join(got)


def stamp_map(path: Path) -> dict[str, str]:
    text = stamp_text(path)
    found = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        found[key.strip()] = value.strip()
    return found


def require_stamp(path: Path) -> None:
    found = stamp_map(path)
    for key in STAMP_KEYS:
        if not found.get(key):
            die(f"code face has no stamp: {path.name}")


def require_own_stamp(path: Path) -> None:
    require_stamp(path)
    found = stamp_map(path)
    for key, value in OWN_STAMP.items():
        if found.get(key) != value:
            die(f"runner stamp is not the law address: {key}")


def run_main(path: Path, argv: list[str]) -> None:
    before = list(sys.path)
    spec = importlib.util.spec_from_file_location("__main__", path)
    if spec is None or spec.loader is None:
        die(f"face did not load: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["__main__"] = module
    old = sys.argv
    try:
        sys.argv = argv
        spec.loader.exec_module(module)
    finally:
        sys.argv = old
        sys.path[:] = before


def _blocks_live_book(context, path: Path, live: Path, code_root: Path) -> bool:
    """True when path is in a live book and outside every designated container.

    Runner 002 refuses every payload inside the live work book. This page's
    fixtures directory is inside that book and is a designated container.
    Every other live-book path still refuses.
    """
    if not context.is_inside(path, live):
        return False
    return not context.inside_designated(path, code_root)


def perform(
    context,
    *,
    code_root: Path,
    fixture_root: Path,
    candidate: str,
    payload_sha256: str,
    config: dict,
    fixture: dict,
) -> None:
    """Run the one declared inventory. context is the app's only validator."""
    require_own_stamp(Path(__file__).resolve())
    runner_file = context.resolve_under(code_root, config["runner"]["path"])
    if context.norm(runner_file) != context.norm(Path(__file__).resolve()):
        die("runner path does not match the loaded candidate")
    digest = context.sha256_file(runner_file)
    if digest != config["runner"]["sha256"]:
        die("runner hash does not match")
    if context.overlaps_live(fixture_root, code_root, config):
        die("fixture root is the live workspace")
    context.check_allowed_root(fixture_root, fixture)
    resolved = context.validate_context(
        fixture_root, config, execute=True, runner_root=code_root
    )
    page = context.unique_page(
        resolved.runtime_dir, resolved.runtime_space, _keyword(fixture["compute_page"])
    )
    if page.name != fixture["compute_page"]:
        die("compute page is not the unique band page")
    payload = context.resolve_under(fixture_root, candidate)
    if context.norm(payload.parent) != context.norm(page):
        die("payload is outside its compute page")
    if not payload.is_file():
        die(f"face is missing: {payload.name}")
    file_hash = context.sha256_file(payload)
    if payload_sha256 != fixture["payload_sha256"]:
        die("payload hash does not match the fixture")
    if file_hash != payload_sha256:
        die("payload hash does not match")
    live_law = code_root / config["desk"] / config["runtime_book"]
    live_work = code_root / config["desk"] / config["work_book"]
    if _blocks_live_book(context, payload, live_law, code_root):
        die("payload is inside the live runtime book")
    if _blocks_live_book(context, payload, live_work, code_root):
        die("payload is inside the live work book")
    plain_name(payload.name, "")
    require_stamp(payload)
    card = _card(page)
    if card["runs"] != payload.name:
        die("card runs a different face")
    book = context.resolve_under(fixture_root / config["desk"], fixture["inventory_book"])
    if book.name in (config["work_book"], config["runtime_book"]):
        die("inventory book is the work book or the runtime book")
    if not book.is_dir():
        die("inventory book is missing")
    output = context.resolve_under(fixture_root, fixture["output"])
    if _blocks_live_book(context, output, live_work, code_root) or _blocks_live_book(
        context, output, live_law, code_root
    ):
        die("output is inside a live book")
    argv = [
        str(payload),
        "--book",
        str(book),
        "--output",
        str(output),
        "--required-face",
        fixture["required_face"],
    ]
    try:
        run_main(payload, argv)
    except SystemExit as exc:
        if exc.code not in (0, None):
            raise
    if not output.is_file():
        die("inventory output is missing")
    if _blocks_live_book(context, output, live_work, code_root):
        die("output is inside a live book")
    out_hash = context.sha256_file(output)
    sys.stdout.write("\n".join(context.report_lines(resolved) + [
        f"fixture: {fixture['identity']}",
        f"runner_resolved: {runner_file}",
        f"payload: {candidate.replace(chr(92), '/')}",
        f"payload_sha256: {file_hash}",
        f"output: {fixture['output']}",
        f"output_sha256: {out_hash}",
        "result: pass",
    ]) + "\n")


def _keyword(page_name: str) -> str:
    parts = page_name.split(".", 1)
    if len(parts) != 2 or not parts[1]:
        die("compute page has no keyword")
    return parts[1]


def _card(page: Path) -> dict:
    card_path = page / "02.md"
    if not card_path.is_file():
        die("card is missing: 02.md")
    try:
        text = card_path.read_text(encoding="utf-8")
    except UnicodeError:
        die("card is not utf-8: 02.md")
    card = parse_card(text)
    if card["uses"]:
        die("uses are not loaded in this development slice")
    if card["args"]:
        die("card args are not used in this development slice")
    plain_name(card["runs"], "")
    return card


def main(argv: list[str] | None = None) -> None:
    del argv
    die("normal run is not activated")


if __name__ == "__main__":
    main()
