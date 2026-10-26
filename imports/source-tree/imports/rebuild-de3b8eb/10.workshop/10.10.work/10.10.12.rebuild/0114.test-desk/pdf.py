#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf.py — read existing note faces and write one PDF.

The note paths are given. Each one is 06.md or 06.NN.md.
This program reads those files and writes one PDF.
It does not edit the faces. It does not write into the kernel.
It does not create a page. It lives on the test desk. It is not seated.
"""
# born: 2026-10-22
# source: director, >run.0514.05.09, and 0414.test-desk/06.08.md
# who: grok-builder
# write reads existing note faces and writes one PDF.
# It does not edit the faces.
# It does not write into the kernel.
# It does not create a page.

from __future__ import annotations

import io
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

from face import die, refuse_kernel_write  # noqa: E402

NOTE_RE = re.compile(r"^06(?:\.\d{2})?\.md$")
USAGE = "use test, or write OUT NOTE [NOTE ...]"


def refuse_out(path: Path) -> None:
    refuse_kernel_write(path)
    names = [parent.name for parent in (path.resolve(), *path.resolve().parents)]
    if "00.kernel" in names:
        die("the kernel is not edited")
    if NOTE_RE.fullmatch(path.name):
        die("the pdf is not a note face")
    if path.suffix != ".pdf":
        die("the output is a pdf")
    if not path.parent.is_dir():
        die("pdf folder is missing")


def note_ok(path: Path) -> None:
    if not path.is_file():
        die("note face is missing")
    if not NOTE_RE.fullmatch(path.name):
        die("note face is 06.md or 06.NN.md")


def read_note(path: Path) -> str:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(notes: list[Path]) -> bytes:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError:
        die("reportlab is missing")
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        title="Notes",
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )
    head = ParagraphStyle("head", fontName="Times-Bold", fontSize=11, leading=14, spaceAfter=8)
    body = ParagraphStyle("body", fontName="Times-Roman", fontSize=9, leading=12)
    story = []
    for note in notes:
        story.append(Paragraph(escape(note.as_posix()), head))
        for line in read_note(note).split("\n"):
            story.append(Paragraph(escape(line) if line else "&nbsp;", body))
        story.append(Spacer(1, 14))
    doc.build(story)
    data = buf.getvalue()
    if not data.startswith(b"%PDF"):
        die("pdf is missing")
    return data


def write_pdf(out: Path, notes: list[Path]) -> None:
    if not notes:
        die("name the note faces")
    refuse_out(out)
    for note in notes:
        note_ok(note)
    before = [note.read_bytes() for note in notes]
    data = render(notes)
    if [note.read_bytes() for note in notes] != before:
        die("a note face changed")
    refuse_out(out)
    out.write_bytes(data)


def check(ok: bool, name: str) -> None:
    if not ok:
        die(f"test failed: {name}")


def cmd_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        page = root / "10.workshop" / "10.10.work" / "10.10.99.trial" / "0114.test-desk"
        page.mkdir(parents=True)
        seated = page / "06.md"
        batch = page / "06.01.md"
        seated.write_bytes("Authorization: draft \u2014 kept.\r\nPDFMARK seated.\r\n".encode("utf-8"))
        batch.write_bytes(b"# 06.01\n\nPDFMARK batch.\n")
        kept_seated = seated.read_bytes()
        kept_batch = batch.read_bytes()
        out = page / "notes.pdf"
        write_pdf(out, [seated, batch])
        data = out.read_bytes()
        check(data.startswith(b"%PDF"), "pdf header")
        check(seated.read_bytes() == kept_seated, "seated note stays")
        check(batch.read_bytes() == kept_batch, "batch note stays")
        check(not (page / "01.md").exists(), "no page created")
        try:
            write_pdf(page / "missing" / "out.pdf", [seated])
            die("test created a folder")
        except SystemExit as exc:
            check("pdf folder is missing" in str(exc), "missing folder stops")
            check(not (page / "missing").exists(), "no folder")
        try:
            write_pdf(out, [page / "06.02.md"])
            die("test wrote a missing note")
        except SystemExit as exc:
            check("note face is missing" in str(exc), "missing note stops")
            check(seated.read_bytes() == kept_seated, "missing note leaves the face")
        other = page / "01.md"
        other.write_bytes(b"# 01\n\nStay.\n")
        try:
            write_pdf(out, [other])
            die("test wrote a non-note")
        except SystemExit as exc:
            check("note face is 06.md or 06.NN.md" in str(exc), "non-note stops")
            check(other.read_bytes() == b"# 01\n\nStay.\n", "non-note stays")
        try:
            write_pdf(page / "06.md", [batch])
            die("test overwrote a note")
        except SystemExit as exc:
            check("the pdf is not a note face" in str(exc), "note name stops")
            check(seated.read_bytes() == kept_seated, "note name leaves the face")
        blocked = root / "00.00.00.kernel.draft" / "00.00.99.law"
        blocked.mkdir(parents=True)
        try:
            write_pdf(blocked / "out.pdf", [seated])
            die("test wrote the template kernel")
        except SystemExit as exc:
            check("template kernel" in str(exc), "kernel path stops")
            check(not (blocked / "out.pdf").exists(), "no kernel pdf")
        live = root / "00.kernel" / "00.00.01.law"
        live.mkdir(parents=True)
        try:
            write_pdf(live / "out.pdf", [seated])
            die("test wrote the kernel")
        except SystemExit as exc:
            check("the kernel is not edited" in str(exc), "00.kernel stops")
            check(not (live / "out.pdf").exists(), "no 00.kernel pdf")
        fresh = page / "06.02.md"
        fresh.write_bytes(b"# 06.02\n\nPDFMARK cold.\n")

        def cold(args: list[str]) -> tuple[int, str]:
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return proc.returncode, (proc.stdout or "") + (proc.stderr or "")

        cold_out = page / "cold.pdf"
        code, shown = cold(["write", str(cold_out), str(fresh)])
        if code != 0 or "notes: 1" not in shown or not cold_out.read_bytes().startswith(b"%PDF"):
            die(f"test failed: cold write: {shown}")
        if fresh.read_bytes() != b"# 06.02\n\nPDFMARK cold.\n":
            die("test failed: cold write edited the note")
        code, shown = cold(["write", str(blocked / "cold.pdf"), str(fresh)])
        if code == 0 or "template kernel" not in shown:
            die(f"test failed: cold kernel write: {shown}")
        if (blocked / "cold.pdf").exists():
            die("test failed: cold kernel write created a pdf")
    print("test: pass")
    print("cold: pass")


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        die(USAGE)
    if args[0] == "test":
        cmd_test()
        return
    if args[0] == "write":
        if len(args) < 3:
            die("write OUT NOTE")
        write_pdf(Path(args[1]), [Path(note) for note in args[2:]])
        print(f"pdf: {args[1]}")
        print(f"notes: {len(args) - 2}")
        return
    die(USAGE)


if __name__ == "__main__":
    main()
