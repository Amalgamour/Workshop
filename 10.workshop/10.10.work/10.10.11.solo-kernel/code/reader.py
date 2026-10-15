#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reader.py — the syntax read order, then the sitting.

Syntax page 0014, section Order, is the walk.
This program reads that section. It does not copy the route onto a door.
A local card is a proposal. The kernel seat governs.
"""
# ## notes
# born: 2026-10-14
# source: grok-prime, syntax read order
# who: grok-prime
# Law 0001: an override names source, scope, difference, reason, and an approving record.
# A row does not approve itself. A draft stamp grants no authority.
# A halt line is the whole line. A note that mentions the sentence is not a claim.
# A start may point at Order. It may not copy the book door or page 0010.
# Syntax 0012 is gravity. A journal 0012 can be a dictionary. Read the book first.

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from door import classify
from face import die, kind_of, make_new, parse_name, show_path
from journal import lookup
from desk import CHECK_KERNEL, DRAFT_KERNEL, live_fields, need
from nav import REPO, SOLO_ROOT, face_file, page_dir

TEMPLATE = REPO / "00.00.00.kernel.draft" / "00.00.00.syntax"
SAMPLE = SOLO_ROOT / "sample" / "00.00.00.syntax"
DESIGN = TEMPLATE / "0014.design" / "01.md"
OWNER = "00.00.00.kernel"
KERNEL_GOVERNS = "The kernel seat governs. This draft does not replace it. A row does not approve itself."

# Pages 0001 through 0009. 0000 already has a draft copy. A second card stays unopened.
BAND = (
    ("0001", "rules", "The seated page is the jump. This card tells a cold sitting to open 0014 Order and not restate it."),
    ("0002", "schema", "Open the seated page only when the work needs a schema. The journal does not."),
    ("0003", "operate", "The seated page says how a sitting is allowed to act. The order stays on 0014."),
    ("0004", "user", "The body stays in the law book. This card does not copy it."),
    ("0005", "ticket", "The body stays in the law book. This card does not copy it."),
    ("0006", "note", "The body stays in the law book. This card does not copy it."),
    ("0007", "reserved", "The seated page has no job. This card does not open one."),
    ("0008", "map", "Map law is law page 0008. The override rule is law page 0001. This card does not keep a second map."),
    ("0009", "retire", "The retire law stays in the law book. This card does not copy it."),
)


def header_block(text: str) -> str:
    parts = re.split(r"(?m)^## ", text, maxsplit=1)
    return parts[0]


def field(text: str, key: str) -> str:
    hit = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*)$", header_block(text))
    return hit.group(1).strip() if hit else ""


def section(text: str, name: str) -> str:
    hit = re.search(rf"(?m)^## {re.escape(name)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.S)
    if not hit:
        die(f"section {name} is missing")
    return hit.group(1).strip("\n")


def order_tokens(text: str) -> list[str]:
    """First backtick of each name. A later mention is not a second step."""
    body = section(text, "Order")
    seen: list[str] = []
    for token in re.findall(r"`([^`]+)`", body):
        if token not in seen:
            seen.append(token)
    return seen


def order_steps(text: str) -> list[dict[str, str]]:
    tokens = order_tokens(text)
    if tokens[:3] != ["00.start", "00.about", "00.readme"]:
        die("order does not open start, about, readme")
    if "00.live" not in tokens:
        die("order does not name 00.live")
    optional = {"00.readme", "0002.schema"}
    steps = []
    for token in tokens:
        if token == "0001.rules":
            steps.append({"token": "book-door", "kind": "door", "optional": ""})
            steps.append({"token": "axioms", "kind": "axioms", "optional": "climb"})
        kind = "live" if token == "00.live" else "page" if re.fullmatch(r"\d{4}\..+", token) else "furniture"
        steps.append({
            "token": token,
            "kind": kind,
            "optional": "yes" if token in optional else "",
        })
    return steps


def authority_lines(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "## Authority":
            start = index + 1
            break
    if start is None:
        return []
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            body.append(line.strip())
    return body


def claim_higher(text: str) -> str:
    """A local file that seats itself, or claims the kernel, does not govern."""
    state = field(text, "state").lower()
    auth = field(text, "Authorization").lower()
    if state in ("approved", "signed", "locked"):
        return "local override does not govern"
    if auth.startswith("approved") or auth.startswith("signed") or auth.startswith("locked"):
        return "local override does not govern"
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"(?i)owner:\s*kernel-only\s*$", stripped):
            return "local override does not govern"
        if re.match(r"(?i)this (draft|page|file) (governs|replaces) the kernel\.?$", stripped):
            return "local override does not govern"
    section = authority_lines(text)
    if section and section != [KERNEL_GOVERNS]:
        return "local override does not govern"
    return ""


def read_face(page: Path) -> tuple[Path, str] | None:
    path = face_file(page, "01")
    if path is None:
        return None
    return path, path.read_text(encoding="utf-8")


def kernel_face(token: str) -> tuple[Path, str]:
    page = TEMPLATE / token
    found = read_face(page)
    if found is None:
        die(f"kernel page {token} has no face 01")
    return found


def lesson_why(kernel_text: str, local_text: str = "") -> str:
    if local_text:
        bad = claim_higher(local_text)
        if bad:
            die(bad)
    why = field(kernel_text, "why")
    if not why:
        die("kernel face has no why")
    return why


def card_body(source: str, difference: str) -> str:
    return (
        "## Source\n\n"
        f"The kernel seat is `{source}`.\n\n"
        "## Scope\n\n"
        "This card is the solo sample of book `00.00.00.syntax`.\n"
        "A cold sitting in a user journal may read it.\n\n"
        "## Difference\n\n"
        f"{difference}\n\n"
        "## Reason\n\n"
        "A cold model needs the source and one sentence. The seated face stays the authority.\n\n"
        "## Authority\n\n"
        f"{KERNEL_GOVERNS}\n"
    )


def write_card(book: Path, number: str, keyword: str, difference: str, who: str) -> Path | None:
    if not who.strip():
        die("who is required")
    names = {parent.name for parent in (book.resolve(), *book.resolve().parents)}
    if CHECK_KERNEL in names or DRAFT_KERNEL in names:
        die("the template kernel is not edited")
    folder = book / f"{number}.{keyword}"
    if folder.exists():
        return None
    folder.mkdir()
    source = f"00.00.00.kernel.draft/00.00.00.syntax/{number}.{keyword}/01.md"
    try:
        return make_new(
            folder, "01", who, difference, "01.law.0001",
            card_body(source, difference),
        )
    except SystemExit:
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
        raise


def write_band(book: Path, who: str) -> list[str]:
    if not who.strip():
        die("who is required")
    lines = []
    for number, keyword, difference in BAND:
        made = write_card(book, number, keyword, difference, who)
        if made is None:
            lines.append(f"kept: {number}.{keyword}")
            continue
        text = made.read_text(encoding="utf-8")
        bad = claim_higher(text)
        if bad or KERNEL_GOVERNS not in text:
            die(bad or "local card lost the authority line")
        lines.append(f"local: {number}.{keyword}")
    return lines


def find_desk(start: Path) -> Path:
    for cand in (start.resolve(), *start.resolve().parents):
        if (cand / "00.start.md").is_file() and (cand / "00.live.md").is_file():
            return cand
    die("the desk is missing")


def find_journal(desk: Path) -> Path:
    found = []
    for child in desk.iterdir():
        if not child.is_dir():
            continue
        parsed = parse_name(child.name)
        if not parsed or kind_of(parsed[0]) != "shelf":
            continue
        if len(parsed[0]) >= 2 and parsed[0][1] == "00":
            continue
        for book in child.iterdir():
            if not book.is_dir():
                continue
            got = parse_name(book.name)
            if not got or kind_of(got[0]) != "book":
                continue
            if page_dir(book, "1000") and page_dir(book, "0012"):
                found.append(book)
    if len(found) != 1:
        die("the journal is missing")
    return found[0]


# A start may name 00.about and point at Order. These are later steps.
PROSE_ROUTE = ("book door", "page `0010`", "syntax page `0001`", "then the axioms")


def copies_route(text: str, steps: list[dict[str, str]]) -> bool:
    pages = [step["token"] for step in steps if step["kind"] == "page"]
    if sum(token in text for token in pages) >= 2:
        return True
    low = text.lower()
    return any(bit in low for bit in PROSE_ROUTE)


def resolve_book(desk: Path, raw: str) -> Path | None:
    path = Path(raw)
    if path.is_absolute() and path.is_dir():
        return path
    for base in (desk, REPO, Path.cwd()):
        cand = (base / raw).resolve()
        if cand.is_dir():
            return cand
    return None


def local_proposal(token: str) -> str:
    page = page_dir(SAMPLE, token.split(".", 1)[0])
    if page is None:
        return ""
    found = read_face(page)
    if found is None:
        return ""
    _path, text = found
    bad = claim_higher(text)
    if bad:
        die(bad)
    if "The kernel seat governs" not in text and "source path:" not in text:
        return f"note: local {token} has no source and no authority line"
    return f"teach: local {token} is a proposal. The kernel seat governs."


def cold(start: Path, need_schema: bool = False) -> list[str]:
    design_path, design = kernel_face("0014.design")
    steps = order_steps(design)
    desk = find_desk(start)
    journal = start if page_dir(start, "0010") else find_journal(desk)
    if page_dir(journal, "0010") is None:
        journal = find_journal(desk)
    lines = [f"teach: walk is {show_path(design_path)} section Order"]
    start_text = (desk / "00.start.md").read_text(encoding="utf-8")
    if "0014" not in start_text or "Order" not in start_text:
        lines.append("stop: 00.start does not point at Order")
    if copies_route(start_text, steps):
        lines.append("stop: 00.start copies the route")
    else:
        lines.append("teach: 00.start points at Order and does not copy the route")
    about = desk / "00.about.md"
    if not about.is_file():
        lines.append("stop: 00.about is missing")
    else:
        lines.append("teach: 00.about is why. It is not the walk.")
    door = journal / "00.md"
    if not door.is_file():
        lines.append("stop: the book door is missing")
    else:
        kind, _detail = classify(door.read_text(encoding="utf-8"))
        lines.append(f"teach: book door is {kind}")
    axioms = TEMPLATE / "00.axioms" / "01.md"
    journal_axioms = journal / "00.axioms.md"
    if journal_axioms.is_file() or (journal / "00.axioms").exists():
        lines.append("teach: this book has local axioms. Read them, then climb.")
    elif axioms.is_file():
        lines.append(f"teach: axioms absent. Climbed to {show_path(axioms)}")
        lines.append(f"teach: axioms why: {field(axioms.read_text(encoding='utf-8'), 'why')}")
    else:
        lines.append("stop: axioms have nowhere to climb")
    for step in steps:
        if step["kind"] != "page":
            continue
        if step["token"] == "0002.schema" and not need_schema:
            lines.append("teach: 0002.schema stays closed. This work does not need a schema.")
            continue
        path, text = kernel_face(step["token"])
        why = lesson_why(text)
        lines.append(f"teach: {step['token']} — {why}")
        lines.append(f"teach: source {show_path(path)}")
        proposal = local_proposal(step["token"])
        if proposal:
            lines.append(proposal)
        else:
            lines.append(f"teach: no local card for {step['token']}. The kernel face is the read.")
        if step["token"] == "0003.operate" and proposal.startswith("teach:"):
            local = page_dir(SAMPLE, "0003")
            found = read_face(local) if local else None
            menu = face_file(local, "03") if local else None
            if found and "## Schema" in found[1] and menu is not None:
                one = found[1]
                if any(line.startswith("Menu:") for line in one.splitlines()):
                    lines.append("stop: face 01 carries the menu")
                else:
                    lines.append("teach: face 01 holds the sections. The menu is face 03.")
                    lines.append("teach: face 02 holds the schema. Face 04 holds the why. The kernel seat governs.")
    if any(step["token"] == "0012.gravity" for step in steps):
        _path, gravity = kernel_face("0012.gravity")
        lines.append(f"teach: syntax 0012 keyword is {field(gravity, 'keyword') or 'gravity'}")
    journal_dict = page_dir(journal, "0012")
    if journal_dict is not None:
        lines.append(f"teach: this book 0012 is {journal_dict.name}. Read the book before the number.")
    live = live_fields((desk / "00.live.md").read_text(encoding="utf-8"))
    if live.get("owner") != OWNER:
        lines.append("stop: 00.live owner is not the kernel address")
    else:
        lines.append(f"teach: owner is {OWNER}. The sitting is not that address.")
    law = resolve_book(desk, live.get("book", ""))
    if law is None:
        lines.append("stop: the law book named by 00.live cannot be opened")
    else:
        lines.append(f"teach: law book {show_path(law)}. It is named. It is not eaten.")
    about_page = page_dir(journal, "0010")
    if about_page is None:
        lines.append("stop: journal 0010 is missing")
    else:
        found = read_face(about_page)
        if found is None:
            lines.append("stop: journal 0010 has no face 01")
        else:
            _path, text = found
            lines.append("teach: face 01 binds. Open the face the job names.")
            if field(text, "state") == "draft":
                lines.append("teach: a draft stamp grants no authority.")
            if "0014" not in text and "Order" not in text:
                lines.append("note: journal 0010 does not name the walk. The desk start does. Leave the journal page.")
    try:
        found = lookup(journal, "slack water")
    except SystemExit:
        lines.append("stop: slack water has no place")
        found = None
    if found:
        lines.append(f"teach: slack water place is {found['place']}")
        if found["place"].endswith(".sunday"):
            lines.append("stop: the Sunday page took the word")
        else:
            lines.append("teach: the Sunday page is not the place of slack water.")
    lines.append("teach: the work pages are the list. A number is an aim. Do not invent a page to meet a count.")
    lines.append("note: nav asks every book for 0010 through 0014. Syntax 0011 is a hole. Syntax 0012 is gravity. The reader uses Order.")
    lines.append("note: sample 0000 is already a draft copy. A second card was not opened.")
    lines.append("note: cite forms stay on their pages. This read picks no winner.")
    return lines


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    design = DESIGN.read_text(encoding="utf-8")
    steps = order_steps(design)
    tokens = [step["token"] for step in steps]
    check(tokens == [
        "00.start", "00.about", "00.readme", "book-door", "axioms",
        "0001.rules", "0003.operate", "0002.schema",
        "0012.gravity", "0013.triangulate", "0010.about", "00.live",
    ], "order")
    check("0012.dictionary" not in tokens, "gravity is not a dictionary")
    check(all(step["token"] != "0002.schema" or step["optional"] == "yes" for step in steps), "schema is optional")
    bad_state = "# 01\n\nstate: approved\nAuthorization: draft — 2026-10-14\n\n## Authority\n\nThis draft governs the kernel.\n"
    check(claim_higher(bad_state) == "local override does not govern", "approved state stops")
    bad_owner = "# 01\n\nstate: draft\n\n## Scope\n\nowner: kernel-only\n"
    check(claim_higher(bad_owner) == "local override does not govern", "kernel-only stops")
    bad_line = "# 01\n\nstate: draft\nAuthorization: draft — 2026-10-14\n\n## Authority\n\nThis draft replaces the kernel.\n"
    check(claim_higher(bad_line) == "local override does not govern", "replace stops")
    mention = (
        "# 01\n\nstate: draft\n\n"
        "It does not govern when a line says this draft governs the kernel.\n"
    )
    check(claim_higher(mention) == "", "a mention is not a claim")
    card_claim = "# 01\n\nstate: draft\n\n## Authority\n\nThis card replaces the kernel.\n"
    draft_claim = "# 01\n\nstate: draft\n\n## Authority\n\nThis draft overrides the kernel.\n"
    check(claim_higher(card_claim) == "local override does not govern", "card replace stops")
    check(claim_higher(draft_claim) == "local override does not govern", "draft override stops")
    kept_auth = "# 01\n\nstate: draft\n\n## Authority\n\n" + KERNEL_GOVERNS + "\n"
    check(claim_higher(kept_auth) == "", "fixed authority stands")
    good = card_body("00.00.00.kernel.draft/00.00.00.syntax/0001.rules/01.md", "A short card.")
    good = "state: draft\nAuthorization: draft — 2026-10-14\n\n" + good
    check(claim_higher(good) == "", "proposal stands")
    kernel = kernel_face("0001.rules")[1]
    check(lesson_why(kernel, good) == field(kernel, "why"), "kernel why governs")
    try:
        lesson_why(kernel, bad_line)
        die("test taught from a higher claim")
    except SystemExit as exc:
        check("does not govern" in str(exc), "higher claim stops the lesson")
    copied = "Open `0001.rules` then `0012.gravity`.\n"
    check(copies_route(copied, steps), "copied route")
    prose = "Then the shelf book door. Then page `0010`.\n"
    check(copies_route(prose, steps), "prose route")
    kept = "Open `00.about`. The walk is template syntax page `0014`, face `01`, section Order.\n"
    check(not copies_route(kept, steps), "pointer stands")
    pointed = (SOLO_ROOT / "use" / "10.ned" / "00.start.md").read_text(encoding="utf-8")
    check(not copies_route(pointed, steps), "Ned start points")
    with tempfile.TemporaryDirectory() as tmp:
        book = Path(tmp) / "10.workshop" / "10.10.work" / "10.10.11.solo-kernel" / "sample" / "00.00.00.syntax"
        book.mkdir(parents=True)
        made = write_card(book, "0001", "rules", BAND[0][2], "grok-prime")
        check(made is not None and made.name == "01.001.draft.md", "local card")
        text = made.read_text(encoding="utf-8")
        check(claim_higher(text) == "", "written card does not govern")
        check("01.law.0001" in text and KERNEL_GOVERNS in text, "override row")
        check(write_card(book, "0001", "rules", BAND[0][2], "grok-prime") is None, "second card stays unopened")
        blocked = Path(tmp) / "00.00.00.kernel.draft" / "00.00.00.syntax"
        blocked.mkdir(parents=True)
        try:
            write_card(blocked, "0004", "user", "No.", "grok-prime")
            die("test wrote the template")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel write stops")
    journal = SOLO_ROOT / "use" / "10.ned" / "10.10.cabin" / "10.10.10.journal"
    if not journal.is_dir():
        die("journal is missing")
    lines = cold(journal)
    text = "\n".join(lines)
    check(not any(line.startswith("stop:") for line in lines), "cold stops " + " ; ".join(line for line in lines if line.startswith("stop:")))
    check("slack water place is 1001.slack-water" in text, "arrived")
    check("Sunday page is not the place" in text, "sunday stays")
    check("0012.gravity" in text and "dictionary" in text, "two 0012s")
    check("a draft stamp grants no authority" in text, "draft teaches")
    check("face 01 holds the sections. The menu is face 03." in text, "0003 teach")
    check("face 02 holds the schema" in text, "0003 schema")
    print("test: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, local, or cold PATH")
    if args[0] == "test":
        cmd_test()
        return
    if args[0] == "local":
        if "--who" not in args:
            die("local --who TEXT")
        for line in write_band(SAMPLE, need(args, "--who")):
            print(line)
        return
    if args[0] == "cold":
        if len(args) < 2:
            die("cold PATH")
        lines = cold(Path(args[1]))
        print("\n".join(lines))
        if any(line.startswith("stop:") for line in lines):
            sys.exit(1)
        return
    die("use test, local, or cold PATH")


if __name__ == "__main__":
    main()
