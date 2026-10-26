#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""words.py — store one private meaning on a stood page and retrieve it.

The page address is given. Face 01 holds the word.
This program does not use the concordance.
It lives on the words page. A later pack can seat it on 03NN.
"""
# born: 2026-10-22
# source: director, >run.0514.05.07, and 0414.test-desk/06.07.md
# who: grok-builder
# store writes one word and its private meaning on a stood face 01.
# get reads that meaning back by the word.
# 0013.concordance is not required.
# A second store of the same word stops.
# A kernel path stops.

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

CODE = None
_here = Path(__file__).resolve()
for _cand in (_here.parent, *_here.parents):
    _code = _cand / "10.10.11.solo-kernel" / "code"
    if not (_code / "face.py").is_file():
        _code = _cand / "10.workshop" / "10.10.work" / "10.10.11.solo-kernel" / "code"
    if (_code / "face.py").is_file():
        CODE = _code
        break
if CODE is None:
    sys.exit("stop: face.py is missing")
sys.path.insert(0, str(CODE))

from desk import need  # noqa: E402
from face import die, kind_of, parse_name, refuse_kernel_write  # noqa: E402

KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.-]*$")
COPY_BOOKS = {"00.00.01.law", "00.00.00.syntax"}
FACE = "01.md"
MARK = "## Words"


def refuse_copy(path: Path) -> None:
    refuse_kernel_write(path)
    names = {path.name, *(parent.name for parent in path.parents)}
    if names & COPY_BOOKS:
        die("a page is not minted in this book")


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if b"\r" in raw:
        die("face file is not LF")
    return raw.decode("utf-8")


def write_text(path: Path, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    path.write_bytes(text.encode("utf-8"))


def page_ok(page: Path) -> None:
    refuse_copy(page)
    if not page.is_dir():
        die("page folder is missing")
    match = re.fullmatch(r"(\d{4})\.(.+)", page.name)
    if not match:
        die("page address is PPPP.keyword")
    if not KEY_RE.fullmatch(match.group(2)):
        die("title needs a word")
    book = page.parent
    if not book.is_dir():
        die("book folder is missing")
    book_name = parse_name(book.name)
    if not book_name or kind_of(book_name[0]) != "book":
        die("page has no book folder")


def face_file(page: Path) -> Path:
    page_ok(page)
    path = page / FACE
    if not path.is_file():
        die("words face is missing")
    return path


def one_meaning(text: str) -> str:
    text = " ".join(text.split())
    if not text:
        die("meaning is empty")
    return text


def one_word(word: str) -> str:
    word = word.strip()
    if not KEY_RE.fullmatch(word):
        die("title needs a word")
    return word


def split_words(text: str) -> tuple[str, str, str]:
    if MARK not in text:
        return text, "", ""
    head, rest = text.split(MARK, 1)
    lines = rest.splitlines(keepends=True)
    body: list[str] = []
    tail: list[str] = []
    for index, line in enumerate(lines):
        if body and line.startswith("## "):
            tail = lines[index:]
            break
        body.append(line)
    return head, "".join(body), "".join(tail)


def entries(section: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    word = ""
    meaning = ""
    for line in section.splitlines():
        if line.startswith("word:"):
            if word:
                rows.append((word, meaning))
            word = line.split(":", 1)[1].strip()
            meaning = ""
        elif word and line.startswith("meaning:"):
            meaning = line.split(":", 1)[1].strip()
    if word:
        rows.append((word, meaning))
    return rows


def find_meaning(section: str, word: str) -> str | None:
    folded = word.casefold()
    for have, meaning in entries(section):
        if have.casefold() == folded:
            return meaning
    return None


def entry_block(word: str, meaning: str) -> str:
    return (
        f"word: {word}\n"
        "brand:\n"
        f"meaning: {meaning}\n"
        "example:\n"
        "see:\n"
        "owner: this words page\n"
    )


def store_word(page: Path, word: str, meaning: str) -> None:
    word = one_word(word)
    meaning = one_meaning(meaning)
    path = face_file(page)
    text = read_text(path)
    head, section, tail = split_words(text)
    if find_meaning(section, word) is not None:
        die("the word is already here")
    block = entry_block(word, meaning)
    if MARK not in text:
        if not head.endswith("\n"):
            head += "\n"
        if not head.endswith("\n\n"):
            head += "\n"
        write_text(path, head + MARK + "\n\n" + block)
        return
    if section and not section.endswith("\n"):
        section += "\n"
    if section and not section.endswith("\n\n"):
        section += "\n"
    write_text(path, head + MARK + section + block + tail)


def get_word(page: Path, word: str) -> tuple[str, str]:
    word = one_word(word)
    text = read_text(face_file(page))
    _head, section, _tail = split_words(text)
    meaning = find_meaning(section, word)
    if meaning is None:
        die("the word is not here")
    if not meaning:
        die("the meaning is missing")
    shown = word
    for have, _meaning in entries(section):
        if have.casefold() == word.casefold():
            shown = have
            break
    return shown, meaning


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def stood_face(body: str) -> bytes:
    return (
        "# 01\n\nstate: draft\n\n## Difference\n\n" + body + "\n"
    ).encode("utf-8")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / "10.10.99.trial"
        book.mkdir(parents=True)
        page = book / "0116.words"
        page.mkdir()
        custody = b"# 08\n\nstate: draft\n\n## Relationships\n\nthis: 0116.words\n"
        (page / "08.md").write_bytes(custody)
        (page / FACE).write_bytes(stood_face("Stood."))
        store_word(page, "leadline", "The three lines at the top of a return.")
        got, meaning = get_word(page, "leadline")
        check(got == "leadline" and meaning == "The three lines at the top of a return.", "stored meaning")
        text = read_text(page / FACE)
        check("state: draft" in text and "## Difference" in text and "Stood." in text, "stood body stays")
        check((page / "08.md").read_bytes() == custody, "custody stays")
        before = (page / FACE).read_bytes()
        try:
            store_word(page, "leadline", "A second meaning.")
            die("test stored the word twice")
        except SystemExit as exc:
            check("the word is already here" in str(exc), "second store stops")
        check((page / FACE).read_bytes() == before, "second store leaves the face")
        try:
            get_word(page, "missing")
            die("test found a missing word")
        except SystemExit as exc:
            check("the word is not here" in str(exc), "missing word stops")
        held = book / "0117.held"
        held.mkdir()
        (held / FACE).write_bytes(
            stood_face("Held.")
            + b"\n## Words\n\nword: readfirst\nbrand:\nmeaning: Open the note first.\nexample:\nsee:\nowner: this words page\n"
        )
        store_word(held, "quietdock", "A private name for a paused run.")
        older, old_meaning = get_word(held, "readfirst")
        newer, new_meaning = get_word(held, "quietdock")
        check(older == "readfirst" and old_meaning == "Open the note first.", "old word stays")
        check(newer == "quietdock" and new_meaning == "A private name for a paused run.", "new word returns")
        bare = book / "0118.plain"
        bare.mkdir()
        bare_body = stood_face("Plain.")
        (bare / FACE).write_bytes(bare_body)
        try:
            store_word(bare, "two words", "No.")
            die("test stored a broken word")
        except SystemExit as exc:
            check("title needs a word" in str(exc), "broken word stops")
            check((bare / FACE).read_bytes() == bare_body, "broken word leaves the face")
        blocked = root / "00.00.00.kernel.draft" / "00.00.99.law"
        blocked.mkdir(parents=True)
        kept = blocked / "0116.kept"
        kept.mkdir()
        kept_body = stood_face("Stay.")
        (kept / FACE).write_bytes(kept_body)
        try:
            store_word(kept, "leadline", "No.")
            die("test wrote on a kernel face")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel face stops")
            check((kept / FACE).read_bytes() == kept_body, "kernel face stays")
        try:
            store_word(blocked / "0116.nope", "leadline", "No.")
            die("test wrote in the kernel")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel path stops")
            check(not (blocked / "0116.nope").exists(), "no kernel folder")

        fresh = book / "0119.fresh"
        fresh.mkdir()
        (fresh / FACE).write_bytes(stood_face("Fresh."))

        def cold(args: list[str]) -> tuple[int, str]:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        code, shown = cold([
            "store", str(fresh), "coldpass",
            "--meaning", "A fresh process stored this meaning.",
        ])
        if code != 0 or "stored: coldpass" not in shown:
            die(f"test failed: cold store: {shown}")
        code, shown = cold(["get", str(fresh), "coldpass"])
        if code != 0 or "meaning: A fresh process stored this meaning." not in shown:
            die(f"test failed: cold get: {shown}")
        code, shown = cold(["get", str(blocked / "0116.kept"), "coldpass"])
        if code == 0 or "template kernel" not in shown:
            die(f"test failed: cold kernel get: {shown}")
        if (kept / FACE).read_bytes() != kept_body:
            die("test failed: cold kernel get wrote the face")
    print("test: pass")
    print("cold: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die("use test, store PAGE WORD --meaning TEXT, or get PAGE WORD")
    cmd = args[0]
    if cmd == "test":
        cmd_test()
        return
    if cmd == "store":
        if len(args) < 5 or "--meaning" not in args:
            die("store PAGE WORD --meaning TEXT")
        page = Path(args[1])
        word = args[2]
        store_word(page, word, need(args, "--meaning"))
        print(f"stored: {word}")
        print(f"page: {page.name}")
        return
    if cmd == "get":
        if len(args) < 3:
            die("get PAGE WORD")
        word, meaning = get_word(Path(args[1]), args[2])
        print(f"word: {word}")
        print(f"meaning: {meaning}")
        return
    die("use test, store PAGE WORD --meaning TEXT, or get PAGE WORD")


if __name__ == "__main__":
    main()
