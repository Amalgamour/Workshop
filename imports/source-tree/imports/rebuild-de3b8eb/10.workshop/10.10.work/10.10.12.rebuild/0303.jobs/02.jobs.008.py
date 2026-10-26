#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 008
# Authorization: draft — 2026-10-20
# who: grok-builder
# state: draft
# Face: 02
# PPPP: 0303
# desk: 10.workshop
# shelf: 10.10.work
# book: 10.10.12.rebuild
# keyword: jobs
# why: The jobs module. The prime gives a pack with the pack command.
#
# cite: 3.1
# source path: 10.workshop/10.10.work/10.10.10.lib/code/jobs.py
# source hash: d9604dc69d951399111792cbbdd20a5116da3f5393210578c5253a038787d978
"""jobs.py — place a 05.NN batch. It does not approve a face.

The page address is DD.SS.BB.PPPP.title.
A folder name is the address and the title.
Desk folder: DD.title. Shelf folder: DD.SS.title.
Book folder: DD.SS.BB.title. Page folder: PPPP.title.

Tails go one way: open, then replied, then closed.
A bare 05.NN.md with state open is still the open batch.
A reviewed batch is filed with ran.
That file is 05.NN.md and its state is ran.
Authorization: signed on that file is the run mark.
It is not a signature on a face.
ran does not choose closed or next.
Each line already has a reply and a status.
Closed is not reopened. The number is not reused.
A reply line is never rewritten.

A run marks each line closed or next.
closed: approved, sent to colab, or the director closed it.
next: the work continues on the next 05.NN.
The new line names the old one. `carry` checks that link.

A #NN lists issue, then the choice fields when this is a choice.
choice, how, now, and later are that form. recommend is the older form.
A face line is PPPP.FF when one page has more than one line.
Then path, scale, and Ask.
Ask holds the command and the reason on one line.
A blank line sits before reply.
"""
# ## notes
# born: 2026-10-13
# source: director, >patch jobs.py
# who: grok-prime
# The run was a hand script. This file had status, ready, and close, and no ran command.
# ready renames the batch to 05.NN.replied.md.
# close renames it to 05.NN.closed.md and refuses a next line.
# The batches that were filed are 05.NN.md with state: ran.
# 05.01, 05.02, and 05.03 on 2002.face were filed that way by hand.
# ran files that shape. It does not invent the status. The status lines are already there.
# It does not change a reply line. A changed section stops the command before the write.
# A next line must say Carried to 05.NN #NN, and that batch number must be later.
# The later file may still be missing. carry checks the file after it exists.
# Authorization: signed on the batch is the run mark. ran does not sign a face.
# A page under code/ for this tool was not added.
# The note stays in this script so the next change can see why ran exists.
# A clean rewrite can come later. Keep this note until the same facts are in the new file.
# born: 2026-10-13
# source: director, >run.05.05
# A page can hold more than one #NN. That was already true.
# Show the face as PPPP.FF on the face: line. Example: 0000.01.
# Gravity stays with the model. This tool does not split one conflict into many lines.
# Conflicts that belong together stay one line. Separate conflicts are separate lines.
# born: 2026-10-17
# source: director, chat 2026-10-17: "Change the live jobs.py so its batch reader treats state ready like open (status, piece, find)."
# who: claude-opus-5-5
# A batch's states are open, ready, ran (10.10.12.rebuild 0401.project 05.02 #04). ready means the prime's check passed and a worker may run it.
# batches() reads state: ready as the open role, so status, piece, find and pick take a ready batch as they take an open one.
# ran still needs every reply filled. A work batch keeps its replies blank, so filing a returned work batch is not done by ran yet.
# Tested on a copy of 10.10.12.rebuild 0501.stand-book: find, status and piece on a ready batch; find on nine pages is unchanged but for that batch.
# find still prints the state, so a ready batch shows as "open: 05.NN.md state ready".
# The ready command below is the old rename to 05.NN.replied.md. It does not set state: ready.
# born: 2026-10-19
# source: director, >run0507.05.03, and 0407.workflow/06.03.md
# who: grok-builder
# pack renames 05.NN.draft.md to 05.NN.pack.md and sets state ready. The prime gives the pack.
# pack prints Read first for each 04NN/01.md and 04NN/06.NN the draft cites.
# A missing cited path stops. A draft with no 04NN face stops. A filled reply stops.
# copy copies 05.NN.pack.md onto the matching 01NN page as 05.NN.return.md.
# mark writes the status line on one #NN of that return.
# close closes the pack. It writes the return path, copies each status, and sets state closed.
# returned stops. The finish is close.
# A request #NN names its purpose and points at the #NN it continues.
# section adds Unprompted or Overflow on the return. note writes 01NN/06.NN.md.
# The older close still renames a replied batch to 05.NN.closed.md.
# A folder that has both a replied batch and a .return.md stops. The prime chooses.
# pack does not approve a face. The word promote is the old name.
# --who prime may pack and close. --who builder may returned and hand.
# hand writes 05.NN.return.md on the 01NN page. It does not append to an older open batch.
# ready remains the old rename to 05.NN.replied.md. It is not the pack command.
# born: 2026-10-20
# source: director, >run.0507.05.04, and 0407.workflow/06.05.md
# who: grok-builder
# pack rewrites the tool-hash lines to the hashes on the branch, then renames the draft.
# It stamps hashed: with the time. door.py is included when the draft names it.
# copy and close stop when a recorded hash differs from the file. That is the mid-run stop.
# born: 2026-10-20
# source: director, >run.0507.05.05, and 0407.workflow/06.06.md
# who: grok-builder
# close looks at the tails of its own 05.NN.
# A .return.md from another batch stays in the folder.
# The same 05.NN still stops when its own return tail is present.
# born: 2026-10-20
# source: director, >run.0507.05.06, and 0407.workflow/06.07.md
# who: grok-builder
# copy and close take 05.NN when the folder holds more than one pack.
# One pack may omit it. A missing argument stops.
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "colab", "Research"}
NAME_RE = re.compile(r"^((?:\d{2}\.)*\d{2,4})\.(.+)$")
BATCH_RE = re.compile(r"^05\.(\d{2})(?:\.(open|replied|closed))?\.md$")
LIFE_RE = re.compile(r"^05\.(\d{2})\.([A-Za-z0-9]+)\.md$")
OLD_TAILS = {"open", "replied", "closed"}
ITEM_RE = re.compile(r"^#(\d{2})\b", re.M)
REPLY_RE = re.compile(r"^[Rr]eply:[ \t]*(.*)$")
KEEP_RE = re.compile(
    r"^(issue|face|recommend|choice|how|now|later|ask|path|scale|status|purpose|points):",
    re.I,
)
ITEM_FIELD_RE = re.compile(
    r"^(placed|issue|face|recommend|choice|how|now|later|path|scale|ask|reason|status|purpose|points):[ \t]*(.*)$",
    re.I,
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for cand in (here.parent, *here.parents):
        if (cand / "10.workshop").is_dir() and (cand / "00.00.00.kernel.draft").is_dir():
            return cand
    sys.exit("repo root not found")


def parse_name(name: str):
    m = NAME_RE.fullmatch(name)
    if not m:
        return None
    address, title = m.group(1), m.group(2)
    parts = address.split(".")
    return parts, title, address


def classify(parts: list[str]) -> str:
    if len(parts) == 4 and all(len(p) == 2 for p in parts[:3]) and len(parts[3]) == 4:
        return "page"
    if len(parts) == 3 and all(len(p) == 2 for p in parts):
        return "book"
    if len(parts) == 2 and all(len(p) == 2 for p in parts):
        return "shelf"
    if len(parts) == 1 and len(parts[0]) == 2:
        return "desk"
    if len(parts) == 1 and len(parts[0]) == 4:
        return "page"
    return ""


def real_dirs(root: Path) -> set[Path]:
    keep: set[Path] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith(".zip")]
        if not filenames:
            continue
        p = Path(dirpath)
        while True:
            if p in keep:
                break
            keep.add(p)
            if p == root or p.parent == p:
                break
            p = p.parent
    return keep


def composed(folder: Path) -> str:
    parsed = parse_name(folder.name)
    if not parsed:
        return folder.name
    parts, title, address = parsed
    if classify(parts) == "page" and len(parts) == 1:
        parent = parse_name(folder.parent.name)
        if parent and classify(parent[0]) == "book":
            return f"{parent[2]}.{address}.{title}"
    return f"{address}.{title}"


def ancestors_ok(folder: Path, parts: list[str]) -> bool:
    book = parse_name(folder.parent.name)
    if not book or classify(book[0]) != "book" or book[2] != ".".join(parts[:3]):
        return False
    shelf = parse_name(folder.parent.parent.name)
    if shelf and classify(shelf[0]) == "shelf":
        if shelf[2] != ".".join(parts[:2]):
            return False
        desk = parse_name(folder.parent.parent.parent.name)
        if desk and classify(desk[0]) == "desk" and desk[2] != parts[0]:
            return False
    return True


def resolve(root: Path, query: str) -> Path:
    query = query.strip().strip('"')
    root = root.resolve()
    named = Path(query)
    if not named.is_absolute():
        named = root / query
    named = named.resolve()
    try:
        named.relative_to(root)
        inside = True
    except ValueError:
        inside = False
    if inside and named.is_dir() and any(named.iterdir()):
        return named
    query = query.strip().strip("/\\")
    found: list[Path] = []
    seen: set[Path] = set()
    parsed = parse_name(query)

    def add(path: Path) -> None:
        if path not in seen:
            seen.add(path)
            found.append(path)

    for folder in real_dirs(root):
        if parsed:
            if folder.name == query:
                add(folder)
            parts, title, _address = parsed
            if classify(parts) == "page" and len(parts) == 4:
                if folder.name == f"{parts[3]}.{title}" and ancestors_ok(folder, parts):
                    add(folder)
        elif parse_name(folder.name) and parse_name(folder.name)[1] == query:
            add(folder)
    if not found and parsed:
        _parts, title, _address = parsed
        for folder in real_dirs(root):
            got = parse_name(folder.name)
            if got and got[1] == title:
                add(folder)
    if not found:
        sys.exit(f"missing: {query}")
    if len(found) > 1:
        print("stop: more than one folder", file=sys.stderr)
        for path in found:
            print(path, file=sys.stderr)
        sys.exit(2)
    return found[0]


def echo(root: Path, folder: Path, writes: str) -> None:
    print(f"address: {composed(folder)}")
    print(f"folder: {folder}")
    names = []
    p = folder.parent
    while p != root and p != p.parent:
        names.append(p.name)
        p = p.parent
    if names:
        print("chain: " + " > ".join(names))
    print(f"writes: {writes}")


def read_keep(path: Path):
    raw = path.read_bytes()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8"), nl


def write_keep(path: Path, text: str, nl: str) -> None:
    text = text.replace("\r\n", "\n")
    if nl == "\r\n":
        text = text.replace("\n", "\r\n")
    if not text.endswith(nl):
        text += nl
    path.write_bytes(text.encode("utf-8"))


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def header_stamp(text: str):
    for key in ("written", "created"):
        m = re.search(
            rf"^{key}:[ \t]*(\d{{4}}-\d{{2}}-\d{{2}})[ T](\d{{2}}:\d{{2}}(?::\d{{2}})?)\s*$",
            text,
            re.M,
        )
        if not m:
            continue
        raw = f"{m.group(1)} {m.group(2)}"
        fmt = "%Y-%m-%d %H:%M:%S" if raw.count(":") == 2 else "%Y-%m-%d %H:%M"
        return datetime.strptime(raw, fmt)
    return None


def director_took(path: Path, text: str) -> bool:
    stamp = header_stamp(text)
    if stamp is None:
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    if mtime <= stamp + timedelta(seconds=2):
        return False
    _header, sections = split_sections(text)
    return any(reply_text(section) for section in sections)


def touch_written(text: str, stamp: str) -> str:
    if re.search(r"^written:[ \t]*", text, re.M):
        return re.sub(r"^written:[ \t]*.*$", f"written: {stamp}", text, count=1, flags=re.M)
    if re.search(r"^created:[ \t]*", text, re.M):
        return re.sub(r"^(created:[ \t]*.*)$", rf"\1\nwritten: {stamp}", text, count=1, flags=re.M)
    return re.sub(r"^(Authorization:[ \t]*.*)$", rf"\1\nwritten: {stamp}", text, count=1, flags=re.M)


def stamp_piece(block: str, stamp: str) -> str:
    if re.search(r"^placed:[ \t]*", block, re.M):
        return block
    lines = block.splitlines()
    lines.insert(1, f"placed: {stamp}")
    return "\n".join(lines) + "\n"


def ask_command(section: str) -> str:
    m = re.search(r"^ask:[ \t]*(.*)$", section, re.M | re.I)
    if not m:
        return ">amend"
    body = m.group(1).strip()
    if not body:
        return ">amend"
    first = body.split()[0]
    if first.startswith(">"):
        return first
    return body


def shape_block(block: str) -> str:
    """Put path and scale above Ask. The reason sits on the Ask line. One blank line sits before reply."""
    text = block.replace("\r\n", "\n").strip("\n")
    lines = text.splitlines()
    if not lines or not re.match(r"^#\d{2}\b", lines[0]):
        return text + "\n"
    title = lines[0]
    reply_i = None
    for i, line in enumerate(lines):
        if REPLY_RE.match(line):
            reply_i = i
            break
    head = lines[1:reply_i] if reply_i is not None else lines[1:]
    tail = lines[reply_i:] if reply_i is not None else ["reply:"]
    while tail and tail[0].strip() == "":
        tail = tail[1:]
    if not tail:
        tail = ["reply:"]
    placed = issue = face = recommend = path = scale = None
    choice = how = now = later = None
    status = purpose = points = None
    ask = reason = None
    extra = []
    for line in head:
        if line.strip() == "":
            continue
        hit = ITEM_FIELD_RE.match(line)
        if not hit:
            extra.append(line)
            continue
        key = hit.group(1).lower()
        body = hit.group(2).strip()
        if key == "placed" and placed is None:
            placed = line
        elif key == "issue" and issue is None:
            issue = line
        elif key == "face" and face is None:
            face = line
        elif key == "choice" and choice is None:
            choice = line
        elif key == "how" and how is None:
            how = line
        elif key == "now" and now is None:
            now = line
        elif key == "later" and later is None:
            later = line
        elif key == "recommend" and recommend is None:
            recommend = line
        elif key == "path" and path is None:
            path = line
        elif key == "scale" and scale is None:
            scale = line
        elif key == "status" and status is None:
            status = line
        elif key == "purpose" and purpose is None:
            purpose = line
        elif key == "points" and points is None:
            points = line
        elif key == "ask" and ask is None:
            ask = body
        elif key == "reason" and reason is None:
            reason = body
        else:
            extra.append(line)
    if ask is None:
        ask_line = None
    elif reason and reason not in ask:
        ask_line = f"Ask: {ask} {reason}".rstrip()
    else:
        ask_line = f"Ask: {ask}" if ask else "Ask:"
    out = [title]
    if placed:
        out.append(placed)
    for line in (status, purpose, points, issue, face, choice, how, now, later, recommend, path, scale):
        if line:
            out.append(line)
    out.extend(extra)
    if ask_line:
        out.append(ask_line)
    out.append("")
    out.extend(tail)
    return "\n".join(out) + "\n"


def header_value(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    text, _nl = read_keep(path)
    m = re.search(rf"^{re.escape(key)}:[ \t]*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def split_sections(text: str):
    matches = list(ITEM_RE.finditer(text))
    if not matches:
        return text, []
    header = text[: matches[0].start()]
    sections = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append(text[m.start() : end])
    return header, sections


def item_nn(section: str) -> str:
    m = re.match(r"^#(\d{2})\b", section)
    return m.group(1) if m else ""


def reply_text(section: str) -> str | None:
    for line in section.splitlines():
        m = REPLY_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def batches(folder: Path):
    rows = []
    if not folder.is_dir():
        return rows
    for path in folder.iterdir():
        m = BATCH_RE.fullmatch(path.name)
        if not m:
            continue
        text, _nl = read_keep(path)
        state = ""
        sm = re.search(r"^state:[ \t]*(.+)$", text, re.M)
        if sm:
            state = sm.group(1).strip()
        tail = m.group(2)
        if tail in ("open", "replied", "closed"):
            role = tail
        elif state in ("open", "ready"):
            role = "open"
        elif state == "replied":
            role = "replied"
        elif state in ("closed", "ran"):
            role = state
        else:
            role = "other"
        rows.append({"nn": m.group(1), "tail": tail, "role": role, "state": state, "path": path})
    rows.sort(key=lambda r: r["nn"])
    return rows


def pick(folder: Path, role: str):
    hits = [r for r in batches(folder) if r["role"] == role]
    if len(hits) > 1:
        print(f"stop: more than one {role}", file=sys.stderr)
        for row in hits:
            print(row["path"], file=sys.stderr)
        sys.exit(2)
    return hits[0] if hits else None


def next_nn(folder: Path) -> str:
    nums = [int(r["nn"]) for r in batches(folder)]
    nxt = (max(nums) + 1) if nums else 1
    if nxt > 99:
        sys.exit("stop: no 05 number left")
    return f"{nxt:02d}"


def stamps(folder: Path) -> dict[str, str]:
    page = parse_name(folder.name)
    book_00 = folder.parent / "00.md"
    page_01 = folder / "01.md"
    out = {
        "pppp": page[0][-1] if page else "",
        "keyword": header_value(page_01, "keyword") or header_value(book_00, "keyword") or (page[1] if page else ""),
        "desk": header_value(page_01, "desk") or header_value(book_00, "desk"),
        "shelf": header_value(page_01, "shelf") or header_value(book_00, "shelf"),
        "book": header_value(page_01, "book") or header_value(book_00, "book"),
        "cite": header_value(page_01, "cite") or header_value(book_00, "cite") or "2.8",
    }
    if not out["book"]:
        parent = parse_name(folder.parent.name)
        if parent:
            out["book"] = f"{parent[2]}.{parent[1]}"
    return out


def render_open(nn: str, info: dict[str, str]) -> str:
    stamp = now_stamp()
    lines = [
        f"# 05.{nn}",
        "",
        f"Authorization: draft \u2014 {stamp[:10]}",
        "who: grok-prime",
        f"created: {stamp}",
        f"written: {stamp}",
        "state: open",
        f"task: {nn}",
        "Face: 05",
        f"PPPP: {info['pppp']}",
        f"desk: {info['desk']}",
    ]
    if info["shelf"]:
        lines.append(f"shelf: {info['shelf']}")
    lines.extend([
        f"book: {info['book']}",
        f"keyword: {info['keyword']}",
        "why: Batch. A blank reply does not release a line.",
        "",
        f"cite: {info['cite']}",
        "",
        "Overview:",
        "Learned:",
        "How: One job is one #NN. The reply stays blank until the director writes it.",
        "Scale: 1 a literal walk halts. 2 two lawful lines. 3 a careful sitting survives. 4 wording. 5 no break.",
        "",
    ])
    return "\n".join(lines) + "\n"


def set_header_state(text: str, state: str) -> str:
    header, sections = split_sections(text)
    new, n = re.subn(r"^state:[ \t]*.*$", f"state: {state}", header, count=1, flags=re.M)
    if n != 1:
        sys.exit("header has no state")
    return new + "".join(sections)


def set_header_auth(text: str, line: str) -> str:
    header, sections = split_sections(text)
    new, n = re.subn(r"^Authorization:[ \t]*.*$", line, header, count=1, flags=re.M)
    if n != 1:
        sys.exit("header has no Authorization")
    return new + "".join(sections)


def cmd_confirm(root: Path, query: str) -> None:
    folder = resolve(root, query)
    echo(root, folder, "no")


def cmd_find(root: Path, query: str) -> None:
    folder = resolve(root, query)
    echo(root, folder, "no")
    rows = batches(folder)
    if not rows:
        print("batch: none")
        return
    for row in rows:
        print(f"{row['role']}: {row['path'].name} state {row['state']}")


def hand_off(row) -> None:
    text, nl = read_keep(row["path"])
    stamp = now_stamp()
    text = set_header_state(text, "replied")
    text = touch_written(text, stamp)
    write_keep(row["path"], text, nl)
    print(f"handed: {row['path'].name}")


def cmd_open(root: Path, query: str) -> None:
    folder = resolve(root, query)
    live = pick(folder, "open")
    if live:
        text, _nl = read_keep(live["path"])
        if director_took(live["path"], text):
            hand_off(live)
            live = None
    if live:
        print(f"open: {live['path'].name}")
        print("kept: yes")
        print("writes: no")
        return
    replied = pick(folder, "replied")
    if replied:
        print(f"waiting: {replied['path'].name}")
    nn = next_nn(folder)
    path = folder / f"05.{nn}.open.md"
    body = render_open(nn, stamps(folder))
    write_keep(path, body, "\n")
    print(f"open: {path.name}")
    print(f"created: {header_value(path, 'created')}")


def echo_job(folder: Path, nn: str) -> None:
    print(f"address: {composed(folder)}")
    print(f"folder: {folder}")
    print(f"#NN: {nn}")


def check_piece(text: str) -> str:
    m = re.match(r"^#(\d{2})\b", text)
    if not m:
        sys.exit("piece needs #NN")
    if not re.search(r"^path:[ \t]*\S", text, re.M | re.I):
        sys.exit("piece needs a path")
    if not re.search(r"^ask:[ \t]*\S", text, re.M | re.I):
        sys.exit("piece needs an ask")
    replies = [REPLY_RE.match(line) for line in text.splitlines()]
    replies = [hit for hit in replies if hit]
    if not replies:
        sys.exit("piece needs a blank reply")
    if any(hit.group(1).strip() for hit in replies):
        sys.exit("piece reply must be blank")
    return m.group(1)


def cmd_piece(root: Path, query: str, file: Path) -> None:
    folder = resolve(root, query)
    live = pick(folder, "open")
    block, _nl = read_keep(file)
    block = block.replace("\r\n", "\n").strip("\n") + "\n"
    nn = check_piece(block)
    block = shape_block(block)
    if live:
        text, _nl = read_keep(live["path"])
        if director_took(live["path"], text):
            hand_off(live)
            if nn != "01":
                sys.exit(f"stop: director replied. next batch starts at #01. this piece is #{nn}")
            live = None
    if not live:
        number = next_nn(folder)
        path = folder / f"05.{number}.open.md"
        write_keep(path, render_open(number, stamps(folder)), "\n")
        print(f"open: {path.name}")
        live = {"nn": number, "path": path}
    text, nl = read_keep(live["path"])
    _header, sections = split_sections(text)
    have = [item_nn(s) for s in sections]
    if nn in have:
        sys.exit(f"stop: #{nn} is already on the batch")
    expect = f"{(int(have[-1]) + 1):02d}" if have else "01"
    if nn != expect:
        sys.exit(f"stop: next is #{expect}")
    stamp = now_stamp()
    block = stamp_piece(block, stamp)
    text = touch_written(text, stamp)
    if not text.endswith("\n"):
        text += "\n"
    if not text.endswith("\n\n"):
        text += "\n"
    write_keep(live["path"], text + block, nl)
    print(f"placed: {live['path'].name} #{nn}")


def target_run(folder: Path):
    replied = pick(folder, "replied")
    if replied:
        return replied
    live = pick(folder, "open")
    if live:
        return live
    sys.exit("stop: no open batch")


def place(lines, at, text):
    line = text if text.endswith("\n") else text + "\n"
    if at == len(lines) and lines and lines[-1].strip() == "":
        at -= 1
    lines.insert(at, line)
    return lines


def rewrite_item(section: str, new_lines_fn) -> str:
    lines = section.splitlines(keepends=True)
    reply_at = None
    for i, line in enumerate(lines):
        if REPLY_RE.match(line.rstrip("\r\n")):
            reply_at = i
            break
    amend_at = []
    status_at = None
    if reply_at is not None:
        for i in range(reply_at + 1, len(lines)):
            body = lines[i].rstrip("\r\n")
            if body.startswith("amend:"):
                amend_at.append(i)
            elif body.startswith("status:"):
                status_at = i
                break
    lines = new_lines_fn(lines, reply_at, amend_at, status_at)
    return "".join(lines)


def cmd_ready(root: Path, query: str) -> None:
    folder = resolve(root, query)
    live = pick(folder, "open")
    if not live:
        sys.exit("stop: no open batch")
    text, nl = read_keep(live["path"])
    _header, sections = split_sections(text)
    if not sections:
        sys.exit("stop: no #NN")
    for section in sections:
        got = reply_text(section)
        if got is None or got == "":
            sys.exit(f"stop: #{item_nn(section)} reply is blank")
    updated = touch_written(set_header_state(text, "replied"), now_stamp())
    dest = live["path"].with_name(f"05.{live['nn']}.replied.md")
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    write_keep(dest, updated, nl)
    live["path"].unlink()
    print(f"replied: {dest.name}")
    sys.stdout.write(updated if updated.endswith("\n") else updated + "\n")


def norm_nn(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("#"):
        raw = raw[1:]
    if not re.fullmatch(r"\d{1,2}", raw):
        sys.exit("nn must be a number")
    n = int(raw)
    if n < 1 or n > 99:
        sys.exit("nn must be 01 through 99")
    return f"{n:02d}"


def batch_nn(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = raw.strip()
    if not text:
        return None
    if text.lower().startswith("05."):
        text = text[3:]
    return norm_nn(text)


def cmd_amend(root: Path, query: str, nn: str, amend: str) -> None:
    nn = norm_nn(nn)
    amend = " ".join(amend.split())
    if not amend:
        sys.exit("amend needs text")
    folder = resolve(root, query)
    row = target_run(folder)
    text, nl = read_keep(row["path"])
    header, sections = split_sections(text)
    hit = None
    for i, section in enumerate(sections):
        if item_nn(section) == nn:
            hit = i
            break
    if hit is None:
        sys.exit(f"missing: #{nn}")
    before = reply_text(sections[hit])

    def edit(lines, reply_at, amend_at, status_at):
        if reply_at is None:
            sys.exit(f"stop: #{nn} has no reply")
        if amend_at:
            at = amend_at[-1] + 1
        elif status_at is not None:
            at = status_at
        else:
            at = len(lines)
        return place(lines, at, f"amend: {amend}")

    sections[hit] = rewrite_item(sections[hit], edit)
    if reply_text(sections[hit]) != before:
        sys.exit("reply changed")
    stamp = now_stamp()
    body = touch_written(header + "".join(sections), stamp)
    write_keep(row["path"], body, nl)
    print(f"amend: {row['path'].name} #{nn}")


def cmd_bump(root: Path, query: str, nn: str, reason: str) -> None:
    nn = norm_nn(nn)
    reason = " ".join(reason.split())
    if not reason:
        sys.exit("bump needs a reason")
    folder = resolve(root, query)
    source = pick(folder, "replied")
    if not source:
        ran = [r for r in batches(folder) if r["role"] == "ran"]
        source = ran[-1] if ran else None
    if not source:
        sys.exit("stop: no replied or ran batch")
    text, _nl = read_keep(source["path"])
    _header, sections = split_sections(text)
    section = next((s for s in sections if item_nn(s) == nn), None)
    if section is None:
        sys.exit(f"missing: #{nn}")
    kept = []
    first = section.splitlines()[0]
    rest = re.match(r"^#\d{2}(.*)$", first).group(1)
    for line in section.splitlines():
        if KEEP_RE.match(line) and not re.match(r"^ask:", line, re.I):
            kept.append(line)
    dest = pick(folder, "open")
    if not dest:
        number = next_nn(folder)
        dest_path = folder / f"05.{number}.open.md"
        write_keep(dest_path, render_open(number, stamps(folder)), "\n")
        dest = {"nn": number, "path": dest_path}
    body, nl = read_keep(dest["path"])
    _h, have = split_sections(body)
    new_nn = f"{(int(item_nn(have[-1])) + 1):02d}" if have else "01"
    command = ask_command(section)
    block = [f"#{new_nn}{rest}", f"placed: {now_stamp()}"]
    block.extend(kept)
    block.append(f"Ask: {command} From 05.{source['nn']} #{nn}. {reason}")
    block.append("reply:")
    piece = shape_block("\n".join(block) + "\n")
    if not body.endswith("\n"):
        body += "\n"
    if not body.endswith("\n\n"):
        body += "\n"
    stamp = now_stamp()
    body = touch_written(body, stamp)
    write_keep(dest["path"], body + piece, nl)
    print(f"bumped: {source['path'].name} #{nn} -> {dest['path'].name} #{new_nn}")


def batch_row(folder: Path, batch: str | None):
    if batch:
        want = norm_nn(batch)
        hits = [r for r in batches(folder) if r["nn"] == want]
        if len(hits) != 1:
            sys.exit(f"stop: 05.{want} not found" if not hits else f"stop: more than one 05.{want}")
        row = hits[0]
        if row["role"] not in ("open", "replied", "ran"):
            sys.exit("stop: batch is not open, replied, or ran")
        return row
    row = target_run(folder)
    if row["role"] not in ("open", "replied"):
        sys.exit("stop: batch is not open or replied")
    return row


def cmd_status(root: Path, query: str, nn: str, kind: str, command: str, batch: str | None) -> None:
    nn = norm_nn(nn)
    if kind not in ("closed", "next"):
        sys.exit("kind is closed or next")
    command = " ".join(command.split())
    if not command:
        sys.exit("status needs the command")
    folder = resolve(root, query)
    row = batch_row(folder, batch)
    text, nl = read_keep(row["path"])
    header, sections = split_sections(text)
    hit = None
    for i, section in enumerate(sections):
        if item_nn(section) == nn:
            hit = i
            break
    if hit is None:
        sys.exit(f"missing: #{nn}")
    before = reply_text(sections[hit])
    line = f"status: {kind}. {command}"

    def edit(lines, reply_at, amend_at, status_at):
        if reply_at is None:
            sys.exit(f"stop: #{nn} has no reply")
        if status_at is not None:
            lines[status_at] = line + "\n"
            return lines
        at = (amend_at[-1] + 1) if amend_at else len(lines)
        return place(lines, at, line)

    sections[hit] = rewrite_item(sections[hit], edit)
    if reply_text(sections[hit]) != before:
        sys.exit("reply changed")
    body = touch_written(header + "".join(sections), now_stamp())
    write_keep(row["path"], body, nl)
    print(f"status: {row['path'].name} #{nn} {kind}")


def lifecycle_rows(folder: Path):
    rows = []
    if not folder.is_dir():
        return rows
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        match = LIFE_RE.fullmatch(path.name)
        if not match or match.group(2) in OLD_TAILS:
            continue
        rows.append({"nn": match.group(1), "tail": match.group(2), "path": path})
    return rows


def chosen_pack(folder: Path, nn: str | None):
    """The named pack. One pack may omit nn. More than one pack requires it."""
    packs = [row for row in lifecycle_rows(folder) if row["tail"] == "pack"]
    want = batch_nn(nn)
    if want is None:
        if len(packs) > 1:
            sys.exit("stop: name the 05.NN")
        if len(packs) == 1:
            return packs[0]
        return None
    hits = [row for row in packs if row["nn"] == want]
    if len(hits) != 1:
        sys.exit(f"stop: no 05.{want}.pack")
    return hits[0]


def own_conflict(folder: Path, nn: str) -> None:
    own = [row for row in lifecycle_rows(folder) if row["nn"] == nn]
    if any(row["tail"] == "return" for row in own):
        sys.exit("stop: pack and return tails")
    others = [row for row in own if row["tail"] not in ("pack", "return")]
    if others:
        sys.exit(f"stop: tail .{others[0]['tail']} is not pack")


def one_tail(folder: Path, want: str):
    rows = lifecycle_rows(folder)
    hits = [row for row in rows if row["tail"] == want]
    if len(hits) > 1:
        sys.exit(f"stop: more than one .{want}")
    if len(hits) == 1:
        return hits[0]
    others = [row for row in rows if row["tail"] != want]
    if others:
        sys.exit(f"stop: tail .{others[0]['tail']} is not {want}")
    sys.exit(f"stop: no .{want}")


def find_return_page(pack_folder: Path) -> Path | None:
    match = re.fullmatch(r"05(\d{2})\.(.+)", pack_folder.name)
    if not match:
        sys.exit("stop: page is not a 05NN pack")
    want = f"01{match.group(1)}.{match.group(2)}"
    book = pack_folder.parent.parent
    if not book.is_dir():
        return None
    found = []
    for band in book.iterdir():
        if not band.is_dir():
            continue
        page = band / want
        if page.is_dir():
            found.append(page)
    if len(found) > 1:
        sys.exit("stop: more than one return page")
    return found[0] if found else None


def return_batch_exists(pack_folder: Path, nn: str) -> bool:
    page = find_return_page(pack_folder)
    if page is None:
        return False
    pattern = re.compile(rf"^05\.{re.escape(nn)}(?:\.[A-Za-z0-9]+)?\.md$")
    return any(path.is_file() and pattern.fullmatch(path.name) for path in page.iterdir())


def rename_life(row, new_tail: str | None, state: str) -> Path:
    text, nl = read_keep(row["path"])
    text = set_header_state(text, state)
    text = touch_written(text, now_stamp())
    dest_name = f"05.{row['nn']}.md" if new_tail is None else f"05.{row['nn']}.{new_tail}.md"
    dest = row["path"].with_name(dest_name)
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    write_keep(dest, text, nl)
    row["path"].unlink()
    print(f"{state}: {dest.name}")
    return dest


def require_role(who: str | None, role: str, command: str) -> None:
    if who != role:
        if who not in ("builder", "prime"):
            sys.exit(f"stop: {command} needs --who {role}")
        sys.exit(f"stop: {who} does not {command}")


CITE_RE = re.compile(r"(04\d{2}\.[A-Za-z0-9-]+)/(01\.md|06\.\d{2}\.md)")


def find_named_page(book: Path, page_name: str) -> Path | None:
    if not book.is_dir():
        return None
    found = []
    for band in book.iterdir():
        if not band.is_dir():
            continue
        page = band / page_name
        if page.is_dir():
            found.append(page)
    if len(found) > 1:
        sys.exit("stop: more than one dev page")
    return found[0] if found else None


def read_first_paths(pack_folder: Path, text: str) -> list[str]:
    cites = []
    for match in CITE_RE.finditer(text):
        rel = f"{match.group(1)}/{match.group(2)}"
        if rel not in cites:
            cites.append(rel)
    if not any(rel.endswith("/01.md") for rel in cites):
        sys.exit("stop: pack cites no 04NN face")
    book = pack_folder.parent.parent
    for rel in cites:
        page_name, face_name = rel.split("/", 1)
        page = find_named_page(book, page_name)
        if page is None or not (page / face_name).is_file():
            sys.exit(f"stop: missing: {rel}")
    return cites


HASH_ANY_RE = re.compile(r"^- (face\.py|clerk\.py|jobs\.py|door\.py)\b.*$", re.M)
HASH_HEX_RE = re.compile(r"^- (face\.py|clerk\.py|jobs\.py|door\.py)[ \t]+([0-9a-f]{64})\s*$", re.M)


def tool_file(name: str) -> Path:
    root = repo_root()
    work = root / "10.workshop" / "10.10.work"
    if name in ("face.py", "door.py"):
        path = work / "10.10.11.solo-kernel" / "code" / name
    else:
        path = work / "10.10.10.lib" / "code" / name
    if not path.is_file():
        sys.exit(f"stop: missing: {name}")
    return path


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wanted_tools(text: str) -> list[str]:
    names = ["face.py", "clerk.py", "jobs.py"]
    if re.search(r"\bdoor\.py\b", text):
        names.append("door.py")
    return names


def rewrite_hashes(text: str, stamp: str) -> str:
    names = wanted_tools(text)
    digests = {name: file_sha(tool_file(name)) for name in names}
    found: list[str] = []

    def repl(match: re.Match) -> str:
        name = match.group(1)
        if name not in digests:
            digests[name] = file_sha(tool_file(name))
        found.append(name)
        return f"- {name} {digests[name]}"

    new = HASH_ANY_RE.sub(repl, text)
    missing = [name for name in names if name not in found]
    if missing:
        block = "\n".join(f"- {name} {digests[name]}" for name in missing)
        if not re.search(r"^Tool hashes:", new, re.M):
            block = "Tool hashes:\n" + block
        header, sections = split_sections(new)
        if not header.endswith("\n"):
            header += "\n"
        if not header.endswith("\n\n"):
            header += "\n"
        new = header + block + "\n\n" + "".join(sections)
    if re.search(r"^hashed:", new, re.M):
        new = re.sub(r"^hashed:[ \t]*.*$", f"hashed: {stamp}", new, count=1, flags=re.M)
    else:
        new, n = re.subn(
            r"^(state:[ \t]*.*)$",
            rf"\1\nhashed: {stamp}",
            new,
            count=1,
            flags=re.M,
        )
        if n != 1:
            sys.exit("header has no state")
    return new


def guard_hashes(text: str) -> None:
    for match in HASH_HEX_RE.finditer(text):
        name, recorded = match.group(1), match.group(2)
        if recorded != file_sha(tool_file(name)):
            sys.exit(f"stop: {name} hash changed")


def cmd_pack(root: Path, query: str, who: str | None) -> None:
    require_role(who, "prime", "pack")
    folder = resolve(root, query)
    row = one_tail(folder, "draft")
    text, nl = read_keep(row["path"])
    cites = read_first_paths(folder, text)
    _header, sections = split_sections(text)
    for section in sections:
        if reply_text(section):
            sys.exit(f"stop: #{item_nn(section)} reply is not blank")
    dest = row["path"].with_name(f"05.{row['nn']}.pack.md")
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    stamped = rewrite_hashes(text, now_stamp())
    write_keep(row["path"], stamped, nl)
    rename_life(row, "pack", "ready")
    for rel in cites:
        print(f"Read first: {rel}")
    print(f"pack: {folder.name} 05.{row['nn']}")


def status_body(section: str) -> str | None:
    match = re.search(r"^status:[ \t]*(.*)$", section, re.M | re.I)
    if not match:
        return None
    return match.group(1).strip()


def status_line(text: str) -> str:
    return "status:" if text == "" else f"status: {text}"


def set_status_line(section: str, text: str) -> str:
    lines = section.splitlines()
    out = []
    hit = False
    for line in lines:
        if not hit and re.match(r"^status:", line, re.I):
            out.append(status_line(text))
            hit = True
        else:
            out.append(line)
    if not hit:
        again = []
        placed = False
        for line in out:
            if not placed and REPLY_RE.match(line):
                again.append(status_line(text))
                placed = True
            again.append(line)
        if not placed:
            again.append(status_line(text))
        out = again
    return "\n".join(out) + "\n"


def ensure_status(section: str) -> str:
    if re.search(r"^status:", section, re.M | re.I):
        return section if section.endswith("\n") else section + "\n"
    return set_status_line(section, "")


def return_path(pack_folder: Path, nn: str) -> Path | None:
    page = find_return_page(pack_folder)
    if page is None:
        return None
    path = page / f"05.{nn}.return.md"
    return path if path.is_file() else None


def cmd_returned(root: Path, query: str, who: str | None) -> None:
    require_role(who, "builder", "returned")
    sys.exit("stop: close the pack")


def cmd_copy(root: Path, query: str, who: str | None, nn: str | None = None) -> None:
    require_role(who, "builder", "copy")
    folder = resolve(root, query)
    row = chosen_pack(folder, nn)
    if row is None:
        row = one_tail(folder, "pack")
    text, nl = read_keep(row["path"])
    guard_hashes(text)
    page = find_return_page(folder)
    if page is None:
        sys.exit("stop: return page is missing")
    dest = page / f"05.{row['nn']}.return.md"
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    header, sections = split_sections(text)
    header = set_header_state(header + "".join(sections), "return")
    header, sections = split_sections(header)
    header = header.replace("who: grok-prime", "who: grok-builder", 1)
    source = f"{folder.name}/05.{row['nn']}.pack.md"
    if not re.search(r"^source:[ \t]", header, re.M):
        header = re.sub(
            r"^(state:[ \t]*.*)$",
            rf"\1\nsource: {source}",
            header,
            count=1,
            flags=re.M,
        )
    sections = [ensure_status(section) for section in sections]
    body = touch_written(header + "".join(sections), now_stamp())
    write_keep(dest, body, nl)
    print(f"copy: {page.name}/05.{row['nn']}.return.md")
    for section in sections:
        print(section.splitlines()[0])
        print(f"ask: {ask_command(section)}")


def cmd_mark(root: Path, query: str, nn: str, item: str, text: str, who: str | None) -> None:
    require_role(who, "builder", "mark")
    nn = norm_nn(nn)
    item = norm_nn(item)
    text = " ".join(text.split())
    if not text:
        sys.exit("stop: status needs text")
    folder = resolve(root, query)
    if not re.fullmatch(r"01\d{2}\..+", folder.name):
        sys.exit("stop: a status is written on 01NN")
    path = folder / f"05.{nn}.return.md"
    if not path.is_file():
        sys.exit("stop: return file is missing")
    body, nl = read_keep(path)
    header, sections = split_sections(body)
    hit = None
    for i, section in enumerate(sections):
        if item_nn(section) == item:
            hit = i
            break
    if hit is None:
        sys.exit(f"missing: #{item}")
    sections[hit] = set_status_line(sections[hit], text)
    write_keep(path, touch_written(header + "".join(sections), now_stamp()), nl)
    print(f"mark: {path.name} #{item}")


def read_body_file(file: Path) -> str:
    raw = file.read_bytes()
    if b"\r" in raw:
        sys.exit("stop: body file is not LF")
    text = raw.decode("utf-8").replace("\r\n", "\n").strip("\n")
    if text.lstrip().startswith("## "):
        sys.exit("stop: the heading belongs on the command")
    if not text:
        sys.exit("stop: body is empty")
    return text + "\n"


def cmd_section(root: Path, query: str, nn: str, heading: str, file: Path, who: str | None) -> None:
    require_role(who, "builder", "section")
    if heading not in ("Unprompted", "Overflow"):
        sys.exit("stop: section is Unprompted or Overflow")
    nn = norm_nn(nn)
    folder = resolve(root, query)
    if not re.fullmatch(r"01\d{2}\..+", folder.name):
        sys.exit("stop: a section is written on 01NN")
    path = folder / f"05.{nn}.return.md"
    if not path.is_file():
        sys.exit("stop: return file is missing")
    body = read_body_file(file)
    text, nl = read_keep(path)
    if re.search(rf"^## {re.escape(heading)}\s*$", text, re.M):
        sys.exit(f"exists: {heading}")
    text = touch_written(text, now_stamp())
    if not text.endswith("\n"):
        text += "\n"
    text += f"\n## {heading}\n\n{body}"
    write_keep(path, text, nl)
    print(f"section: {path.name} {heading}")


def render_note(nn: str, info: dict[str, str]) -> str:
    stamp = now_stamp()
    lines = [
        f"# 06.{nn}",
        "",
        f"Authorization: draft \u2014 {stamp[:10]}",
        "who: grok-builder",
        f"created: {stamp}",
        f"written: {stamp}",
        "state: draft",
        f"task: {nn}",
        "Face: 06",
        f"PPPP: {info['pppp']}",
        f"desk: {info['desk']}",
    ]
    if info["shelf"]:
        lines.append(f"shelf: {info['shelf']}")
    lines.extend([
        f"book: {info['book']}",
        f"keyword: {info['keyword']}",
        f"why: Notes for 05.{nn}.",
        "",
        f"cite: {info['cite']}",
        "",
    ])
    return "\n".join(lines) + "\n"


def cmd_note(root: Path, query: str, nn: str, file: Path, who: str | None) -> None:
    require_role(who, "builder", "note")
    nn = norm_nn(nn)
    folder = resolve(root, query)
    if not re.fullmatch(r"01\d{2}\..+", folder.name):
        sys.exit("stop: a note is written on 01NN")
    path = folder / f"06.{nn}.md"
    body = read_body_file(file)
    if not path.is_file():
        write_keep(path, render_note(nn, stamps(folder)), "\n")
        print(f"notes: {path.name}")
    text, nl = read_keep(path)
    text = touch_written(text, now_stamp())
    if not text.endswith("\n"):
        text += "\n"
    write_keep(path, text + "\n" + body, nl)
    print(f"noted: {path.name}")


def finish_row(folder: Path, nn: str | None = None):
    chosen = chosen_pack(folder, nn)
    if chosen is not None:
        own_conflict(folder, chosen["nn"])
        return chosen
    rows = lifecycle_rows(folder)
    returns = [row for row in rows if row["tail"] == "return"]
    if len(returns) > 1:
        sys.exit("stop: more than one pack tail")
    if len(returns) == 1:
        return returns[0]
    others = [row for row in rows if row["tail"] not in ("pack", "return")]
    if others:
        sys.exit(f"stop: tail .{others[0]['tail']} is not pack")
    return None


def close_pack(folder: Path, row) -> None:
    pack_text, _nl = read_keep(row["path"])
    guard_hashes(pack_text)
    ret = return_path(folder, row["nn"])
    if ret is None:
        sys.exit("stop: return file is missing")
    ret_text, _nl = read_keep(ret)
    _header, ret_sections = split_sections(ret_text)
    if not ret_sections:
        sys.exit("stop: return has no #NN")
    statuses = {}
    for section in ret_sections:
        item = item_nn(section)
        got = status_body(section)
        if not got:
            sys.exit(f"stop: #{item} has no status")
        statuses[item] = got
    text, nl = read_keep(row["path"])
    header, sections = split_sections(text)
    for i, section in enumerate(sections):
        item = item_nn(section)
        if item in statuses:
            sections[i] = set_status_line(section, statuses[item])
        elif not status_body(section):
            sys.exit(f"stop: #{item} has no status")
    page = find_return_page(folder)
    pointer = f"{page.name}/05.{row['nn']}.return.md"
    if re.search(r"^return:[ \t]", header, re.M):
        header = re.sub(r"^return:[ \t]*.*$", f"return: {pointer}", header, count=1, flags=re.M)
    else:
        header = re.sub(
            r"^(state:[ \t]*.*)$",
            rf"\1\nreturn: {pointer}",
            header,
            count=1,
            flags=re.M,
        )
    body = touch_written(set_header_state(header + "".join(sections), "closed"), now_stamp())
    dest = row["path"].with_name(f"05.{row['nn']}.md")
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    write_keep(dest, body, nl)
    row["path"].unlink()
    print(f"closed: {dest.name}")
    print(f"return: {pointer}")
    note = page / f"06.{row['nn']}.md"
    if note.is_file():
        print(f"notes: {page.name}/06.{row['nn']}.md")
    else:
        print("notes: none")


def check_hand(text: str) -> str:
    match = re.match(r"^#(\d{2})\b", text)
    if not match:
        sys.exit("hand needs #NN")
    if not re.search(r"^path:[ \t]*\S", text, re.M | re.I):
        sys.exit("hand needs a path")
    if not re.search(r"^ask:[ \t]*\S", text, re.M | re.I):
        sys.exit("hand needs an ask")
    replies = [hit for hit in (REPLY_RE.match(line) for line in text.splitlines()) if hit]
    if not replies:
        sys.exit("hand needs a reply")
    return match.group(1)


def cmd_hand(root: Path, query: str, nn: str, file: Path, who: str | None) -> None:
    require_role(who, "builder", "hand")
    nn = norm_nn(nn)
    folder = resolve(root, query)
    if not re.fullmatch(r"01\d{2}\..+", folder.name):
        sys.exit("stop: a return is written on 01NN")
    path = folder / f"05.{nn}.return.md"
    block, _nl = read_keep(file)
    block = block.replace("\r\n", "\n").strip("\n") + "\n"
    got = check_hand(block)
    block = ensure_status(shape_block(block))
    if not path.is_file():
        body = render_open(nn, stamps(folder))
        body = body.replace("who: grok-prime", "who: grok-builder", 1)
        body = body.replace(
            "why: Batch. A blank reply does not release a line.",
            "why: The builder's return.",
            1,
        )
        body = set_header_state(body, "return")
        write_keep(path, body, "\n")
        print(f"return: {path.name}")
    text, nl = read_keep(path)
    _header, sections = split_sections(text)
    have = [item_nn(section) for section in sections]
    if got in have:
        sys.exit(f"stop: #{got} is already on the return")
    expect = f"{(int(have[-1]) + 1):02d}" if have else "01"
    if got != expect:
        sys.exit(f"stop: next is #{expect}")
    stamp = now_stamp()
    block = stamp_piece(block, stamp)
    text = touch_written(text, stamp)
    if not text.endswith("\n\n"):
        text = text if text.endswith("\n") else text + "\n"
        text += "\n"
    write_keep(path, text + block, nl)
    print(f"placed: {path.name} #{got}")


def cmd_close(root: Path, query: str, who: str | None, nn: str | None = None) -> None:
    folder = resolve(root, query)
    if lifecycle_rows(folder):
        require_role(who, "builder", "close")
        replied = [row for row in batches(folder) if row["role"] == "replied"]
        if len(replied) > 1:
            sys.exit("stop: more than one replied")
        if replied:
            sys.exit("stop: replied batch and a return tail")
        row = finish_row(folder, nn)
        if row is None:
            sys.exit("stop: no pack")
        close_pack(folder, row)
        return
    require_role(who, "prime", "close")
    row = pick(folder, "replied")
    if not row:
        sys.exit("stop: ready the batch first")
    text, nl = read_keep(row["path"])
    _header, sections = split_sections(text)
    if not sections:
        sys.exit("stop: no #NN")
    for section in sections:
        m = re.search(r"^status:[ \t]*(\S+)", section, re.M)
        if not m:
            sys.exit(f"stop: #{item_nn(section)} has no status")
        if m.group(1).rstrip(".").lower() == "next":
            sys.exit(f"stop: #{item_nn(section)} is next. carry it before close")
    updated = touch_written(set_header_state(text, "closed"), now_stamp())
    dest = row["path"].with_name(f"05.{row['nn']}.closed.md")
    if dest.exists():
        sys.exit(f"exists: {dest.name}")
    write_keep(dest, updated, nl)
    row["path"].unlink()
    print(f"closed: {dest.name}")


def cmd_ran(root: Path, query: str) -> None:
    folder = resolve(root, query)
    live = pick(folder, "open")
    replied = pick(folder, "replied")
    if live and replied:
        sys.exit("stop: both an open batch and a replied batch")
    row = live or replied
    if not row:
        sys.exit("stop: no open batch")
    text, nl = read_keep(row["path"])
    _header, before = split_sections(text)
    if not before:
        sys.exit("stop: no #NN")
    link = re.compile(r"Carried to 05\.(\d{2}) #(\d{2})")
    for section in before:
        nn = item_nn(section)
        got = reply_text(section)
        if got is None or got == "":
            sys.exit(f"stop: #{nn} reply is blank")
        mark = re.search(r"^status:[ \t]*(.+)$", section, re.M)
        if not mark:
            sys.exit(f"stop: #{nn} has no status")
        body = mark.group(1).strip()
        kind = body.split()[0].rstrip(".").lower()
        if kind == "closed":
            continue
        if kind != "next":
            sys.exit(f"stop: #{nn} status {kind} is not closed or next")
        hit = link.search(body)
        if not hit:
            sys.exit(f"stop: #{nn} is next and names no later batch")
        if int(hit.group(1)) <= int(row["nn"]):
            sys.exit(f"stop: #{nn} carries to 05.{hit.group(1)}, not a later batch")
    day = now_stamp()[:10]
    updated = set_header_auth(text, f"Authorization: signed \u2014 {day}")
    updated = set_header_state(updated, "ran")
    updated = touch_written(updated, now_stamp())
    _after_header, after = split_sections(updated)
    if after != before:
        sys.exit("reply changed")
    dest = row["path"].with_name(f"05.{row['nn']}.md")
    if dest.exists() and dest.resolve() != row["path"].resolve():
        sys.exit(f"exists: {dest.name}")
    echo_job(folder, row["nn"])
    write_keep(dest, updated, nl)
    if dest.resolve() != row["path"].resolve():
        row["path"].unlink()
    print(f"ran: {dest.name}")
    print(f"items: {len(before)}")


def cmd_carry(root: Path, query: str) -> None:
    folder = resolve(root, query)
    ran = [r for r in batches(folder) if r["role"] == "ran"]
    if not ran:
        sys.exit("stop: no ran batch")
    source = ran[-1]
    text, _nl = read_keep(source["path"])
    _header, sections = split_sections(text)
    if not sections:
        sys.exit("stop: no #NN")
    problems = []
    carried = []
    link = re.compile(r"Carried to 05\.(\d{2}) #(\d{2})")
    for section in sections:
        m = re.search(r"^status:[ \t]*(.+)$", section, re.M)
        nn = item_nn(section)
        if not m:
            problems.append(f"#{nn} has no status")
            continue
        body = m.group(1).strip()
        kind = body.split()[0].rstrip(".").lower()
        if kind == "closed":
            continue
        if kind != "next":
            problems.append(f"#{nn} status {kind} is not closed or next")
            continue
        hit = link.search(body)
        if not hit:
            problems.append(f"#{nn} is next and names no later batch")
            continue
        later, item = hit.group(1), hit.group(2)
        if int(later) <= int(source["nn"]):
            problems.append(f"#{nn} carries to 05.{later}, not a later batch")
            continue
        dest = next((r for r in batches(folder) if r["nn"] == later), None)
        if dest is None:
            problems.append(f"#{nn} carries to 05.{later}, and that file is missing")
            continue
        dtext, _nl = read_keep(dest["path"])
        if not re.search(rf"^#{item}\b", dtext, re.M):
            problems.append(f"05.{later} has no #{item}")
            continue
        if f"05.{source['nn']} #{nn}" not in dtext:
            problems.append(f"05.{later} #{item} does not name 05.{source['nn']} #{nn}")
            continue
        carried.append(f"05.{source['nn']} #{nn} -> 05.{later} #{item}")
    if problems:
        print("stop: unfinished work has no next batch", file=sys.stderr)
        for problem in problems:
            print(problem, file=sys.stderr)
        sys.exit(2)
    print(f"carry: {source['path'].name}")
    if not carried:
        print("next: none")
    for line in carried:
        print(line)
    print("writes: no")


def expect_stop(fn, *args, contains: str) -> str:
    try:
        fn(*args)
    except SystemExit as exc:
        text = str(exc.code)
        if contains not in text:
            sys.exit(f"stop: test wanted {contains} in {text}")
        return text
    sys.exit(f"stop: test wanted a refuse containing {contains}")


def write_batch(path: Path, state: str) -> None:
    path.write_bytes(
        (
            f"# {path.stem}\n\nstate: {state}\n\n#01 example\nstatus: closed\nreply:\n"
        ).encode("utf-8")
    )


def plant_dev(pack: Path) -> None:
    dev = pack.parent.parent / "0400.band.dev" / "0407.workflow"
    dev.mkdir(parents=True)
    (dev / "01.md").write_bytes("# 01\n".encode("utf-8"))
    (dev / "06.03.md").write_bytes("# 06.03\n".encode("utf-8"))


def write_cited_draft(path: Path, line: str) -> None:
    path.write_bytes(
        (
            f"# {path.stem}\n\nstate: open\n\nRead first: {line}\n\n"
            "#01 example\nstatus: closed\nreply:\n"
        ).encode("utf-8")
    )


def make_book(root: Path):
    book = root / "10.workshop" / "10.10.work" / "10.10.12.rebuild"
    pack = book / "0500.band.packs" / "0507.workflow"
    ret = book / "0100.band.returns" / "0107.workflow"
    pack.mkdir(parents=True)
    ret.mkdir(parents=True)
    return pack, ret


def cmd_test() -> None:
    import io
    import tempfile
    from contextlib import redirect_stdout

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        plant_dev(pack)
        write_batch(pack / "05.01.md", "ready")
        write_cited_draft(
            pack / "05.03.draft.md",
            "0407.workflow/01.md and 0407.workflow/06.03.md.",
        )
        expect_stop(cmd_pack, root, "0507.workflow", "builder", contains="builder does not pack")
        printed = io.StringIO()
        with redirect_stdout(printed):
            cmd_pack(root, "0507.workflow", "prime")
        shown = printed.getvalue()
        if "Read first: 0407.workflow/01.md" not in shown:
            sys.exit("stop: test pack did not print the dev face")
        if "Read first: 0407.workflow/06.03.md" not in shown:
            sys.exit("stop: test pack did not print the note")
        check = pack / "05.03.pack.md"
        if not check.is_file() or (pack / "05.03.draft.md").exists():
            sys.exit("stop: test pack did not rename the draft")
        if "state: ready" not in check.read_text(encoding="utf-8"):
            sys.exit("stop: test pack did not set ready")
        if not (pack / "05.01.md").is_file():
            sys.exit("stop: test pack moved a bare batch")
        expect_stop(cmd_pack, root, "0507.workflow", "prime", contains="not draft")
        if not check.is_file():
            sys.exit("stop: test second pack changed the pack")
        write_batch(ret / "05.01.open.md", "open")
        expect_stop(cmd_returned, root, "0507.workflow", "prime", contains="prime does not returned")
        expect_stop(cmd_returned, root, "0507.workflow", "builder", contains="close the pack")
        if not check.is_file():
            sys.exit("stop: test returned renamed the pack")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        write_batch(pack / "05.03.pack.md", "ready")
        expect_stop(cmd_close, root, "0507.workflow", "prime", contains="prime does not close")
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="return file is missing")
        if not (pack / "05.03.pack.md").is_file():
            sys.exit("stop: test close on a pack renamed it")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        (pack / "05.03.pack.md").write_bytes(
            (
                "# 05.03\n\nstate: ready\nwho: grok-prime\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        expect_stop(cmd_copy, root, "0507.workflow", "prime", contains="prime does not copy")
        cmd_copy(root, "0507.workflow", "builder")
        made = ret / "05.03.return.md"
        copied = made.read_text(encoding="utf-8")
        if "state: return" not in copied or "\nstatus:\n" not in copied:
            sys.exit("stop: test copy did not make the return")
        if "who: grok-builder" not in copied:
            sys.exit("stop: test copy did not name the builder")
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="has no status")
        if not (pack / "05.03.pack.md").is_file():
            sys.exit("stop: test close renamed a pack with a blank status")
        cmd_mark(
            root,
            "0107.workflow",
            "03",
            "01",
            "timer build located in 0303.jobs/02.jobs.py",
            "builder",
        )
        cmd_close(root, "0507.workflow", "builder")
        closed = (pack / "05.03.md").read_text(encoding="utf-8")
        if "state: closed" not in closed:
            sys.exit("stop: test close did not set closed")
        if "return: 0107.workflow/05.03.return.md" not in closed:
            sys.exit("stop: test close did not point at the return")
        if "timer build located in 0303.jobs/02.jobs.py" not in closed:
            sys.exit("stop: test close did not copy the status")
        if not made.is_file() or (pack / "05.03.pack.md").exists():
            sys.exit("stop: test close removed the return or left the pack")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        (pack / "05.04.pack.md").write_bytes(
            (
                "# 05.04\n\nstate: ready\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        older = (
            "# 05.03\n\nstate: return\n\n#01 old\nstatus: kept\nreply:\n"
        ).encode("utf-8")
        (pack / "05.03.return.md").write_bytes(older)
        (pack / "05.03.draft.md").write_bytes(b"# 05.03\n\nstate: open\n\n")
        (ret / "05.04.return.md").write_bytes(
            (
                "# 05.04\n\nstate: return\n\n"
                "#01 Build timer\nstatus: timer build located in 0303.jobs/02.jobs.py\nreply:\n"
            ).encode("utf-8")
        )
        cmd_close(root, "0507.workflow", "builder")
        if not (pack / "05.04.md").is_file() or (pack / "05.04.pack.md").exists():
            sys.exit("stop: test close left the pack beside an older return")
        if (pack / "05.03.return.md").read_bytes() != older:
            sys.exit("stop: test close changed the older return")
        if not (pack / "05.03.draft.md").is_file():
            sys.exit("stop: test close removed an older draft")
        closed = (pack / "05.04.md").read_text(encoding="utf-8")
        if "state: closed" not in closed or "return: 0107.workflow/05.04.return.md" not in closed:
            sys.exit("stop: test close did not file the matching batch")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        (pack / "05.04.pack.md").write_bytes(
            (
                "# 05.04\n\nstate: ready\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        (pack / "05.04.return.md").write_bytes(
            b"# 05.04\n\nstate: return\n\n#01 Build timer\nstatus: here\nreply:\n"
        )
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="pack and return tails")
        if not (pack / "05.04.pack.md").is_file() or not (pack / "05.04.return.md").is_file():
            sys.exit("stop: test own return tail was removed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        write_batch(pack / "05.04.pack.md", "ready")
        write_batch(pack / "05.05.pack.md", "ready")
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="name the 05.NN")
        if not (pack / "05.04.pack.md").is_file() or not (pack / "05.05.pack.md").is_file():
            sys.exit("stop: test two packs were renamed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        for nn in ("04", "05"):
            (pack / f"05.{nn}.pack.md").write_bytes(
                (
                    f"# 05.{nn}\n\nstate: ready\nwho: grok-prime\n\n"
                    "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                    "ask: >build the timer\nreply:\n"
                ).encode("utf-8")
            )
        expect_stop(cmd_copy, root, "0507.workflow", "builder", contains="name the 05.NN")
        cmd_copy(root, "0507.workflow", "builder", "05.05")
        made = ret / "05.05.return.md"
        if not made.is_file() or (ret / "05.04.return.md").exists():
            sys.exit("stop: test copy did not take 05.05")
        if not (pack / "05.04.pack.md").is_file() or not (pack / "05.05.pack.md").is_file():
            sys.exit("stop: test copy removed a pack")
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="name the 05.NN")
        expect_stop(cmd_close, root, "0507.workflow", "builder", "04", contains="return file is missing")
        if not (pack / "05.04.pack.md").is_file():
            sys.exit("stop: test named close removed the other pack")
        cmd_mark(
            root,
            "0107.workflow",
            "05",
            "01",
            "timer build located in 0303.jobs/02.jobs.py",
            "builder",
        )
        cmd_close(root, "0507.workflow", "builder", "05")
        if not (pack / "05.05.md").is_file() or (pack / "05.05.pack.md").exists():
            sys.exit("stop: test close 05.05 left its pack")
        if not (pack / "05.04.pack.md").is_file():
            sys.exit("stop: test close 05.05 removed the other pack")
        closed = (pack / "05.05.md").read_text(encoding="utf-8")
        if "state: closed" not in closed or "return: 0107.workflow/05.05.return.md" not in closed:
            sys.exit("stop: test close 05.05 did not file the named batch")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        write_batch(pack / "05.03.nope.md", "open")
        expect_stop(cmd_pack, root, "0507.workflow", "prime", contains="not draft")
        expect_stop(cmd_returned, root, "0507.workflow", "builder", contains="close the pack")
        expect_stop(cmd_close, root, "0507.workflow", "prime", contains="prime does not close")
        expect_stop(cmd_close, root, "0507.workflow", "builder", contains="not pack")
        if not (pack / "05.03.nope.md").is_file():
            sys.exit("stop: test illegal tail was renamed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        write_batch(pack / "05.01.replied.md", "replied")
        cmd_close(root, "0507.workflow", "prime")
        if not (pack / "05.01.closed.md").is_file():
            sys.exit("stop: test the older close did not file 05.01.closed.md")
        if (pack / "05.01.md").exists():
            sys.exit("stop: test the older close wrote a bare file")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        write_batch(pack / "05.03.draft.md", "open")
        expect_stop(cmd_pack, root, "0507.workflow", "prime", contains="cites no 04NN")
        if not (pack / "05.03.draft.md").is_file():
            sys.exit("stop: test a draft with no dev face was renamed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        plant_dev(pack)
        write_cited_draft(pack / "05.03.draft.md", "0499.missing/01.md")
        expect_stop(cmd_pack, root, "0507.workflow", "prime", contains="missing: 0499.missing/01.md")
        if not (pack / "05.03.draft.md").is_file() or (pack / "05.03.pack.md").exists():
            sys.exit("stop: test a missing dev face was renamed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        plant_dev(pack)
        (pack / "05.03.draft.md").write_bytes(
            (
                "# 05.03.draft\n\nstate: open\n\n"
                "Read first: 0407.workflow/01.md and 0407.workflow/06.03.md.\n\n"
                "#01 example\nstatus: closed\nreply: filled\n"
            ).encode("utf-8")
        )
        expect_stop(cmd_pack, root, "0507.workflow", "prime", contains="reply is not blank")
        if not (pack / "05.03.draft.md").is_file():
            sys.exit("stop: test a filled reply was renamed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        plant_dev(pack)
        old = "a" * 64
        (pack / "05.04.draft.md").write_bytes(
            (
                "# 05.04\n\nstate: open\n\n"
                "Read first: 0407.workflow/01.md and 0407.workflow/06.03.md.\n"
                f"- jobs.py {old}\n\n"
                "#01 example\nreply:\n"
            ).encode("utf-8")
        )
        cmd_pack(root, "0507.workflow", "prime")
        packed = (pack / "05.04.pack.md").read_text(encoding="utf-8")
        live = file_sha(tool_file("jobs.py"))
        if old in packed or live not in packed:
            sys.exit("stop: test pack did not rewrite the jobs.py hash")
        if "hashed:" not in packed or file_sha(tool_file("face.py")) not in packed:
            sys.exit("stop: test pack did not stamp the tool hashes")
        if "door.py" in packed:
            sys.exit("stop: test pack added door.py without a citation")
        broken = packed.replace(live, "0" * 64)
        (pack / "05.04.pack.md").write_text(broken, encoding="utf-8", newline="\n")
        expect_stop(cmd_copy, root, "0507.workflow", "builder", contains="jobs.py hash changed")
        if (ret / "05.04.return.md").exists() or not (pack / "05.04.pack.md").is_file():
            sys.exit("stop: test a changed hash wrote the return")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        plant_dev(pack)
        (pack / "05.04.draft.md").write_bytes(
            (
                "# 05.04\n\nstate: open\n\n"
                "Read first: 0407.workflow/01.md and 0407.workflow/06.03.md.\n"
                "Use door.py.\n\n"
                "#01 example\nreply:\n"
            ).encode("utf-8")
        )
        cmd_pack(root, "0507.workflow", "prime")
        packed = (pack / "05.04.pack.md").read_text(encoding="utf-8")
        if file_sha(tool_file("door.py")) not in packed:
            sys.exit("stop: test pack omitted a cited door.py")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        plant_dev(pack)
        old = "b" * 64
        (pack / "05.04.draft.md").write_bytes(
            (
                "# 05.04\n\nstate: open\n\n"
                "Read first: 0407.workflow/01.md and 0407.workflow/06.03.md.\n"
                f"- jobs.py {old}\n\n"
                "#01 example\nreply:\n"
            ).encode("utf-8")
        )

        def cold_hash(args: list[str]) -> tuple[int, str]:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--root", str(root), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        code, shown = cold_hash(["--who", "prime", "pack", "0507.workflow"])
        if code != 0 or "pack:" not in shown:
            sys.exit(f"stop: cold hash pack failed: {shown}")
        packed_path = pack / "05.04.pack.md"
        packed = packed_path.read_text(encoding="utf-8")
        live = file_sha(tool_file("jobs.py"))
        if old in packed or live not in packed or "hashed:" not in packed:
            sys.exit("stop: cold pack did not rewrite the jobs.py hash")
        packed_path.write_text(packed.replace(live, "0" * 64), encoding="utf-8", newline="\n")
        code, shown = cold_hash(["--who", "builder", "copy", "0507.workflow"])
        if code == 0 or "jobs.py hash changed" not in shown:
            sys.exit(f"stop: cold changed hash did not stop: {shown}")
        if (pack / "05.04.pack.md").is_file() is False:
            sys.exit("stop: cold changed hash removed the pack")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        write_batch(ret / "05.01.open.md", "open")
        kept = (ret / "05.01.open.md").read_bytes()
        plant_dev(pack)
        write_cited_draft(
            pack / "05.03.draft.md",
            "0407.workflow/01.md and 0407.workflow/06.03.md.",
        )
        piece = root / "hand-01.md"
        piece.write_bytes(
            (
                "#02 >note a request\n"
                "purpose: Ask for the closed pack to name the return.\n"
                "points: #01\n"
                "path: 0107.workflow/05.03.return.md\n"
                "ask: >note request the pointer\n"
                "reply:\n"
            ).encode("utf-8")
        )
        (root / "unprompted.md").write_bytes(
            b"The live pack was left unclosed so the prime can see the hole.\n"
        )
        (root / "note.md").write_bytes(
            b"Prime, read this note with the return.\n"
        )

        def cold(args: list[str]) -> tuple[int, str]:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--root", str(root), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        def want(args: list[str], contains: str, code_ok: bool = False) -> str:
            code, text = cold(args)
            if contains not in text:
                sys.exit(f"stop: cold wanted {contains} in {text}")
            if code_ok and code != 0:
                sys.exit(f"stop: cold {args} exited {code}: {text}")
            if not code_ok and code == 0:
                sys.exit(f"stop: cold {args} should have stopped: {text}")
            return text

        want(["pack", "0507.workflow"], "needs --who prime")
        want(["--who", "builder", "pack", "0507.workflow"], "builder does not pack")
        shown = want(
            ["--who", "prime", "pack", "0507.workflow"],
            "Read first: 0407.workflow/01.md",
            code_ok=True,
        )
        if "Read first: 0407.workflow/06.03.md" not in shown:
            sys.exit("stop: cold pack did not print the note")
        if not (pack / "05.03.pack.md").is_file() or (pack / "05.03.draft.md").exists():
            sys.exit("stop: cold pack did not leave 05.03.pack.md")
        want(["promote", "0507.workflow"], "invalid choice")
        want(["--who", "prime", "copy", "0507.workflow"], "prime does not copy")
        want(["--who", "builder", "copy", "0507.workflow"], "copy:", code_ok=True)
        made = (ret / "05.03.return.md").read_text(encoding="utf-8")
        if "state: return" not in made or "status:" not in made:
            sys.exit("stop: cold copy did not make the return")
        want(
            ["--who", "builder", "hand", "0107.workflow", "--nn", "03", "--file", str(piece)],
            "placed:",
            code_ok=True,
        )
        if "purpose: Ask for the closed pack to name the return." not in (ret / "05.03.return.md").read_text(encoding="utf-8"):
            sys.exit("stop: cold hand dropped the request")
        if (ret / "05.01.open.md").read_bytes() != kept:
            sys.exit("stop: cold hand changed 05.01.open.md")
        want(
            ["--who", "builder", "mark", "0107.workflow", "--nn", "03", "--item", "01", "--text", "timer build located in 0303.jobs/02.jobs.py"],
            "mark:",
            code_ok=True,
        )
        want(
            ["--who", "builder", "mark", "0107.workflow", "--nn", "03", "--item", "02", "--text", "request recorded on the return"],
            "mark:",
            code_ok=True,
        )
        want(
            ["--who", "builder", "section", "0107.workflow", "--nn", "03", "--heading", "Unprompted", "--file", str(root / "unprompted.md")],
            "section:",
            code_ok=True,
        )
        want(
            ["--who", "builder", "note", "0107.workflow", "--nn", "03", "--file", str(root / "note.md")],
            "notes:",
            code_ok=True,
        )
        if not (ret / "06.03.md").is_file():
            sys.exit("stop: cold note did not write 06.03.md")
        want(["--who", "prime", "close", "0507.workflow"], "prime does not close")
        want(["--who", "builder", "close", "0507.workflow"], "return: 0107.workflow/05.03.return.md", code_ok=True)
        closed = (pack / "05.03.md").read_text(encoding="utf-8")
        if "state: closed" not in closed or "timer build located in 0303.jobs/02.jobs.py" not in closed:
            sys.exit("stop: cold close did not keep the status")
        if not (ret / "05.03.return.md").is_file() or (pack / "05.03.pack.md").exists():
            sys.exit("stop: cold close removed the return or left the pack")
        want(["--who", "builder", "returned", "0507.workflow"], "close the pack")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        (pack / "05.04.pack.md").write_bytes(
            (
                "# 05.04\n\nstate: ready\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        older = (
            "# 05.03\n\nstate: return\n\n#01 old\nstatus: kept\nreply:\n"
        ).encode("utf-8")
        (pack / "05.03.return.md").write_bytes(older)
        (ret / "05.04.return.md").write_bytes(
            (
                "# 05.04\n\nstate: return\n\n"
                "#01 Build timer\nstatus: timer build located in 0303.jobs/02.jobs.py\nreply:\n"
            ).encode("utf-8")
        )

        def cold_close() -> tuple[int, str]:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--root",
                    str(root),
                    "--who",
                    "builder",
                    "close",
                    "0507.workflow",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        code, shown = cold_close()
        if code != 0 or "closed: 05.04.md" not in shown:
            sys.exit(f"stop: cold close beside an older return failed: {shown}")
        if (pack / "05.03.return.md").read_bytes() != older or (pack / "05.04.pack.md").exists():
            sys.exit("stop: cold close moved the older return or left the pack")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, _ret = make_book(root)
        (pack / "05.04.pack.md").write_bytes(
            (
                "# 05.04\n\nstate: ready\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        (pack / "05.04.return.md").write_bytes(
            b"# 05.04\n\nstate: return\n\n#01 Build timer\nstatus: here\nreply:\n"
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--root",
                str(root),
                "--who",
                "builder",
                "close",
                "0507.workflow",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        shown = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode == 0 or "pack and return tails" not in shown:
            sys.exit(f"stop: cold own return tail did not stop: {shown}")
        if not (pack / "05.04.pack.md").is_file() or not (pack / "05.04.return.md").is_file():
            sys.exit("stop: cold own return tail was removed")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        for nn in ("04", "05"):
            (pack / f"05.{nn}.pack.md").write_bytes(
                (
                    f"# 05.{nn}\n\nstate: ready\nwho: grok-prime\n\n"
                    "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                    "ask: >build the timer\nreply:\n"
                ).encode("utf-8")
            )
        (ret / "05.05.return.md").write_bytes(
            (
                "# 05.05\n\nstate: return\n\n"
                "#01 Build timer\nstatus: timer build located in 0303.jobs/02.jobs.py\nreply:\n"
            ).encode("utf-8")
        )

        def cold_job(args: list[str]) -> tuple[int, str]:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--root", str(root), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        code, shown = cold_job(["--who", "builder", "close", "0507.workflow"])
        if code == 0 or "name the 05.NN" not in shown:
            sys.exit(f"stop: cold missing 05.NN did not stop: {shown}")
        if not (pack / "05.04.pack.md").is_file() or not (pack / "05.05.pack.md").is_file():
            sys.exit("stop: cold missing 05.NN renamed a pack")
        code, shown = cold_job(["--who", "builder", "close", "0507.workflow", "--nn", "05.05"])
        if code != 0 or "closed: 05.05.md" not in shown:
            sys.exit(f"stop: cold close 05.05 failed: {shown}")
        if not (pack / "05.04.pack.md").is_file() or (pack / "05.05.pack.md").exists():
            sys.exit("stop: cold close 05.05 moved the other pack or left its own")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pack, ret = make_book(root)
        (ret / "01.md").write_bytes("# 01\n\nkeyword: workflow\n".encode("utf-8"))
        (pack / "05.03.pack.md").write_bytes(
            (
                "# 05.03\n\nstate: ready\nwho: grok-prime\n\n"
                "#01 Build timer\npath: 0303.jobs/02.jobs.py\n"
                "ask: >build the timer\nreply:\n"
            ).encode("utf-8")
        )
        (ret / "05.03.return.md").write_bytes(
            (
                "# 05.03\n\nstate: return\n\n"
                "#01 Build timer\nstatus: timer build located in 0303.jobs/02.jobs.py\nreply:\n"
            ).encode("utf-8")
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--root",
                str(root),
                "--who",
                "builder",
                "close",
                "0507.workflow",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        shown = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0 or "closed: 05.03.md" not in shown:
            sys.exit(f"stop: cold single pack close failed: {shown}")
        if (pack / "05.03.pack.md").exists():
            sys.exit("stop: cold single pack close left the pack")

    print("cold: pass")
    print("test: pass")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="jobs.py",
        description=(
            "Place a 05.NN batch. ran marks the batch. It does not sign a face. "
            "ready is the old rename to 05.NN.replied.md. "
            "pack is prime-only. It moves 05.NN.draft.md to 05.NN.pack.md."
        ),
    )
    p.add_argument("--root", type=Path, default=None)
    p.add_argument(
        "--who",
        choices=["builder", "prime"],
        default=None,
        help="builder may copy, mark, hand, note, section, and close. prime may pack.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name: str):
        sp = sub.add_parser(name)
        sp.add_argument("page")
        return sp

    add("confirm")
    add("find")
    add("open")
    piece = add("piece")
    piece.add_argument("--file", type=Path, required=True)
    add("ready")
    amend = add("amend")
    amend.add_argument("--nn", required=True)
    amend.add_argument("--text", required=True)
    bump = add("bump")
    bump.add_argument("--nn", required=True)
    bump.add_argument("--reason", required=True)
    status = add("status")
    status.add_argument("--nn", required=True)
    status.add_argument("--kind", required=True)
    status.add_argument("--command", required=True)
    status.add_argument("--batch", default=None)
    add("pack")
    add("returned")
    copy = add("copy")
    copy.add_argument("--nn", default=None)
    mark = add("mark")
    mark.add_argument("--nn", required=True)
    mark.add_argument("--item", required=True)
    mark.add_argument("--text", required=True)
    section = add("section")
    section.add_argument("--nn", required=True)
    section.add_argument("--heading", required=True)
    section.add_argument("--file", type=Path, required=True)
    note = add("note")
    note.add_argument("--nn", required=True)
    note.add_argument("--file", type=Path, required=True)
    hand = add("hand")
    hand.add_argument("--nn", required=True)
    hand.add_argument("--file", type=Path, required=True)
    close = add("close")
    close.add_argument("--nn", default=None)
    add("ran")
    add("carry")
    sub.add_parser("test")
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.cmd == "test":
        cmd_test()
        return
    root = args.root.resolve() if args.root else repo_root()
    if args.cmd == "confirm":
        cmd_confirm(root, args.page)
    elif args.cmd == "find":
        cmd_find(root, args.page)
    elif args.cmd == "open":
        cmd_open(root, args.page)
    elif args.cmd == "piece":
        cmd_piece(root, args.page, args.file)
    elif args.cmd == "ready":
        cmd_ready(root, args.page)
    elif args.cmd == "amend":
        cmd_amend(root, args.page, args.nn, args.text)
    elif args.cmd == "bump":
        cmd_bump(root, args.page, args.nn, args.reason)
    elif args.cmd == "status":
        cmd_status(root, args.page, args.nn, args.kind, args.command, args.batch)
    elif args.cmd == "pack":
        cmd_pack(root, args.page, args.who)
    elif args.cmd == "returned":
        cmd_returned(root, args.page, args.who)
    elif args.cmd == "copy":
        cmd_copy(root, args.page, args.who, args.nn)
    elif args.cmd == "mark":
        cmd_mark(root, args.page, args.nn, args.item, args.text, args.who)
    elif args.cmd == "section":
        cmd_section(root, args.page, args.nn, args.heading, args.file, args.who)
    elif args.cmd == "note":
        cmd_note(root, args.page, args.nn, args.file, args.who)
    elif args.cmd == "hand":
        cmd_hand(root, args.page, args.nn, args.file, args.who)
    elif args.cmd == "close":
        cmd_close(root, args.page, args.who, args.nn)
    elif args.cmd == "ran":
        cmd_ran(root, args.page)
    elif args.cmd == "carry":
        cmd_carry(root, args.page)


if __name__ == "__main__":
    main()
