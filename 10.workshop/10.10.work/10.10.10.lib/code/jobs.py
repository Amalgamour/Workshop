#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jobs.py — place a 05.NN batch. It does not approve or promote.

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
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "colab", "Research"}
NAME_RE = re.compile(r"^((?:\d{2}\.)*\d{2,4})\.(.+)$")
BATCH_RE = re.compile(r"^05\.(\d{2})(?:\.(open|replied|closed))?\.md$")
ITEM_RE = re.compile(r"^#(\d{2})\b", re.M)
REPLY_RE = re.compile(r"^[Rr]eply:[ \t]*(.*)$")
KEEP_RE = re.compile(
    r"^(issue|face|recommend|choice|how|now|later|ask|path|scale):",
    re.I,
)
ITEM_FIELD_RE = re.compile(
    r"^(placed|issue|face|recommend|choice|how|now|later|path|scale|ask|reason):[ \t]*(.*)$",
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
    for line in (issue, face, choice, how, now, later, recommend, path, scale):
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
        elif state == "open":
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


def cmd_close(root: Path, query: str) -> None:
    folder = resolve(root, query)
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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="jobs.py",
        description="Place a 05.NN batch. ran marks the batch. It does not sign a face.",
    )
    p.add_argument("--root", type=Path, default=None)
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
    add("close")
    add("ran")
    add("carry")
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
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
    elif args.cmd == "close":
        cmd_close(root, args.page)
    elif args.cmd == "ran":
        cmd_ran(root, args.page)
    elif args.cmd == "carry":
        cmd_carry(root, args.page)


if __name__ == "__main__":
    main()
