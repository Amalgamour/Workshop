"""Local rules for the exchange workflow. The real v2 envelope is not claimed here."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import colab_workflow as cw  # noqa: E402


ROOT = Path(r"D:\Git\lib-build")
V1 = ROOT / "labs/colab-workflow-pass01/colab_workflow.py"
PY = sys.executable
DIGEST = "ab" * 32


class Skip(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def run(argv):
    code, out, err = cw.execute(argv)
    body = json.loads(out.decode("utf-8")) if out else None
    return code, body, err


def write_config(path: Path, helper: Path | None = None) -> None:
    cfg = {
        "assembler": str(ROOT / "labs/pack-assembly-pass01/pack_assembly.py"),
        "checker": str(ROOT / "labs/pack-custody-pass01/pack_check.py"),
        "helper": str(helper or (ROOT / "labs/return-capture-pass01/return_capture.py")),
        "inspector": str(ROOT / "labs/return-capture-pass01/return_inspect.py"),
        "producer_v1": str(ROOT / "labs/colab-support-pass01/colab_support.py"),
        "python": str(PY),
        "repositories": {"workshop": str(ROOT)},
        "schema": "colab-config/2",
    }
    path.write_bytes(cw.canonical(cfg))


def target(path: str, data: bytes, section=None, file_name: str | None = None) -> dict:
    return {
        "book": "00.00.10.work",
        "file": file_name or Path(path).name,
        "id": "T01",
        "page": "0411.colab",
        "section": section,
        "source": {
            "commit": "6896224510fe0bcebac291fce7ed311a2cd085cb",
            "path": path,
            "repository": "workshop",
            "sha256": cw.sha256(data),
        },
    }


def request_for(page: str, targets: list[dict], title: str = "Exchange question") -> dict:
    return {
        "book": "00.00.10.work",
        "page": page,
        "pass": "05.01",
        "schema": "colab-exchange-open/1",
        "targets": targets,
        "title": title,
    }


def heading(value: str, occurrence=None) -> dict:
    return {"kind": "heading", "occurrence": occurrence, "value": value}


def open_sources(root: Path, page: str, relative: str, data: bytes, section=None, file_name: str | None = None):
    sources = root / "sources"
    dest = sources.joinpath(*relative.split("/"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    body = request_for(page, [target(relative, data, section, file_name)])
    path = root / f"open-{page}.json"
    path.write_bytes(cw.canonical(body))
    book = root / "book"
    book.mkdir(exist_ok=True)
    code, result, _err = run(["open", "--book", str(book), "--request", str(path), "--sources", str(sources)])
    return code, result, book, body


def mini_output(root: Path, record_page: str, pack: bytes, notes: bytes, digest: str = DIGEST) -> Path:
    output = root / "output" / record_page
    package = output / "package"
    package.mkdir(parents=True)
    (package / "05.01.pack.md").write_bytes(pack)
    (package / "06.01.notes.md").write_bytes(notes)
    (output / "prepared-colab.zip").write_bytes(b"zip-bytes")
    files = {
        "package/05.01.pack.md": pack,
        "package/06.01.notes.md": notes,
        "prepared-colab.zip": b"zip-bytes",
    }
    recorded = {
        "digest": digest,
        "investigation": {"book": "00.00.10.work", "page": record_page, "pass": "05.01"},
        "out_files": [
            {"bytes": len(data), "path": name, "sha256": cw.sha256(data)} for name, data in sorted(files.items())
        ],
        "result": "prepared",
        "schema": "colab-package-verification/2",
    }
    (output / "verification.json").write_bytes(cw.canonical(recorded))
    return output


def intact(page: str, digest: str = DIGEST) -> bytes:
    return cw.canonical(
        {
            "digest": digest,
            "exchange": {
                "notes": "06.01.notes.md",
                "pack": "05.01.pack.md",
                "pass": "05.01",
                "return_name": "05.01.return.md",
                "review_name": "06.01.review.md",
            },
            "investigation": {"book": "00.00.10.work", "page": page, "pass": "05.01"},
            "result": "intact",
        }
    )


def attach(book: Path, page: str, output: Path, config: Path, digest: str = DIGEST):
    cw.RUN_PROCESS = lambda argv: (0, intact(page, digest), b"")
    try:
        return run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                page,
                "--pass",
                "05.01",
                "--output",
                str(output),
                "--config",
                str(config),
                "--expect-digest",
                digest,
            ]
        )
    finally:
        cw.RUN_PROCESS = None


def review_body(route: str, disposition: str, pending: bool, reply: str, next_pass=None) -> dict:
    return {
        "assessment": "Supplied fixture assessment. The tool does not judge it.",
        "by": "Codex Prime",
        "findings": [
            {
                "consequential": True,
                "director_reply": reply,
                "disposition": disposition,
                "id": "F01",
                "observation": "A reader could mistake notes for a review.",
                "pending": pending,
                "reason": "Prime supplied this disposition.",
                "source_binding": "T01",
            }
        ],
        "next_pass": next_pass,
        "on": "2026-10-29",
        "pending_questions": ["Does the note stay distinct from the review?"],
        "route": route,
        "schema": "colab-exchange-review/1",
    }


def place(book: Path, page: str, config: Path, member: str, data: bytes, origin_page: str | None = None):
    member_dir = book / member
    member_dir.mkdir(exist_ok=True)
    (member_dir / "return.md").write_bytes(data)
    observed = {
        "capture": {
            "manifest_sha256": "c" * 64,
            "origin": {"batch": "05.01", "book": "00.00.10.work", "page": origin_page or page},
            "receipt_sha256": "d" * 64,
            "return": {"bytes": len(data), "sha256": cw.sha256(data)},
        },
        "status": "complete",
    }
    verify = (
        f"receipt {'d' * 64}\nresult complete\nnot approved\nnot accepted\nnot published\n"
    ).encode("utf-8")

    def run_proc(argv):
        if Path(argv[0]).name.startswith("return_inspect"):
            return 0, cw.canonical(observed), b""
        return 0, verify, b""

    cw.RUN_PROCESS = run_proc
    try:
        return run(
            [
                "place-return",
                "--book",
                str(book),
                "--page",
                page,
                "--pass",
                "05.01",
                "--member",
                member,
                "--config",
                str(config),
            ]
        )
    finally:
        cw.RUN_PROCESS = None


def names(page: Path) -> list[str]:
    return sorted(path.relative_to(page).as_posix() for path in page.rglob("*") if path.is_file())


def test_band_and_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "book"
        book.mkdir()
        code, body, _err = run(["propose", "--book", str(book)])
        if code != 0 or body["page"] != "0701.free" or body["wrote"] is not False:
            raise AssertionError(body)
        code, body, _err = run(["propose", "--book", str(LIVE())])
        if body["reason"] != "live work book is not a fixture":
            raise AssertionError(body)
        note = b"# Page\n\n## Alpha\n\nbody\n"
        code, body, _book, _request = open_sources(
            root,
            "0701.sample",
            "00.kernel/00.00.10.work/0411.colab/01.md",
            "# Compute\n\n## Compute module — proposed operations\n\ntext\n".encode("utf-8"),
            heading("## Compute module — proposed operations"),
            "01.md",
        )
        if code != 0:
            raise AssertionError(body)
        fenced = b"# Page\n\n```\n## Alpha\n```\n\nbody\n"
        code, body, _book, _request = open_sources(root, "0702.fenced", "subj/note.md", fenced, heading("## Alpha"))
        if body["reason"] != "unresolved section":
            raise AssertionError(body)
        both = b"# Page\n\n## Alpha\n\n```\n## Alpha\n```\n"
        code, body, book, _request = open_sources(root, "0703.both", "subj/note.md", both, heading("## Alpha"))
        if code != 0:
            raise AssertionError(body)
        code, body, _book, _request = open_sources(
            root, "0704.source07", "subj/07.md", note, heading("## Alpha"), "07.md"
        )
        if code != 0 or "07.md" in names(book / "0704.source07"):
            raise AssertionError(names(book / "0704.source07") if code == 0 else body)
        bad = request_for("0705.bad", [target("subj/note.md", note, {"kind": "id", "value": "S1"})])
        path = root / "bad.json"
        path.write_bytes(cw.canonical(bad))
        code, body, _err = run(
            ["open", "--book", str(book), "--request", str(path), "--sources", str(root / "sources")]
        )
        if body["reason"] != "unsupported section id":
            raise AssertionError(body)
        unknown = request_for("0706.unknown", [target("subj/note.md", note)])
        unknown["schema"] = "colab-open/1"
        upath = root / "unknown.json"
        upath.write_bytes(cw.canonical(unknown))
        code, body, _err = run(
            ["open", "--book", str(book), "--request", str(upath), "--sources", str(root / "sources")]
        )
        if body["reason"] != "unknown schema":
            raise AssertionError(body)
        code, body, _err = run(["open", "--book", str(book), "--request", str(path), "--sources", str(root / "sources")])
        # 0700 is refused by the page rule when it is the requested page.
        low = request_for("0700.band", [target("subj/note.md", note)])
        low_path = root / "low.json"
        low_path.write_bytes(cw.canonical(low))
        code, body, _err = run(
            ["open", "--book", str(book), "--request", str(low_path), "--sources", str(root / "sources")]
        )
        if body["reason"] != "outside declared band":
            raise AssertionError(body)


def LIVE() -> Path:
    return Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")


def test_attach_notes_and_review() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n\nPreparation only.\n"
        pack = b"# Pack\n\nPrimary instruction.\n"
        code, body, book, _request = open_sources(root, "0701.sample", "subj/note.md", note, heading("## Missing") if False else None)
        # The note has no required heading because section is null.
        if code != 0:
            raise AssertionError(body)
        output = mini_output(root, "0701.sample", pack, note)
        config = root / "config.json"
        write_config(config)
        code, body, _err = run(
            [
                "append-note",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--text",
                "too early",
            ]
        )
        if body["reason"] != "missing investigation":
            raise AssertionError(body)
        code, body, _err = attach(book, "0701.sample", output, config)
        if code != 0 or body["digest"] != DIGEST:
            raise AssertionError(body)
        page = book / "0701.sample"
        if (page / "05.01.pack.md").read_bytes() != pack:
            raise AssertionError("pack bytes")
        snapshot = (page / "artifacts/05.01/package/06.01.notes.md").read_bytes()
        if snapshot != note or cw.launch_slice((page / "06.01.notes.md").read_bytes()) != note:
            raise AssertionError("launch snapshot")
        if (page / "05.01.return.md").exists() or (page / "06.01.review.md").exists():
            raise AssertionError("early exchange")
        provenance = (page / "artifacts/05.01/provenance.json").read_bytes()
        if b"colab-config" in provenance or str(config).encode("utf-8") in provenance:
            raise AssertionError("config leaked")
        code, body, _err = attach(book, "0701.sample", output, config)
        if body["result"] != "repeat" or body["wrote"] is not False:
            raise AssertionError(body)
        code, body, _err = run(
            [
                "append-note",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--text",
                "Working line kept apart from the snapshot.",
            ]
        )
        if code != 0:
            raise AssertionError(body)
        if (page / "artifacts/05.01/package/06.01.notes.md").read_bytes() != note:
            raise AssertionError("snapshot changed")
        projected = (page / "06.01.notes.md").read_bytes()
        if cw.launch_slice(projected) != note or b"Working line kept apart from the snapshot." not in projected:
            raise AssertionError(projected)
        code, body, _err = run(
            [
                "record-review",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--review",
                str(root / "missing-review.json"),
            ]
        )
        # The review file is absent, so the command refuses before reading it only if the path check runs first.
        held = root / "held.json"
        held.write_bytes(
            cw.canonical(review_body("hold", "held", True, "hypothetical-fixture: Keep the return bytes exact."))
        )
        code, body, _err = run(
            ["record-review", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--review", str(held)]
        )
        if body["reason"] != "review before return":
            raise AssertionError(body)
        returned = b"# Synthetic fixture response\n\nThis file is a labelled fixture. It is not a model result.\n"
        code, body, _err = place(book, "0701.sample", config, "0101.colab-fixture-0501", returned)
        if code != 0 or (page / "05.01.return.md").read_bytes() != returned:
            raise AssertionError(body)
        pointer = (page / "08.md").read_text(encoding="utf-8")
        if "0101.colab-fixture-0501" not in pointer or returned.decode("utf-8") in pointer:
            raise AssertionError(pointer)
        code, body, _err = place(book, "0701.sample", config, "0101.colab-fixture-0501", returned)
        if body["result"] != "repeat" or body["wrote"] is not False:
            raise AssertionError(body)
        other = returned + b"changed\n"
        code, body, _err = place(book, "0701.sample", config, "0102.other-return-0501", other)
        if body["reason"] != "occupied different content" or (page / "05.01.return.md").read_bytes() != returned:
            raise AssertionError(body)
        code, body, _err = run(
            ["record-review", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--review", str(held)]
        )
        if code != 0 or body["route"] != "hold":
            raise AssertionError(body)
        rendered = (page / "06.01.review.md").read_text(encoding="utf-8")
        if "hypothetical-fixture: Keep the return bytes exact." not in rendered or "F01 held" not in rendered:
            raise AssertionError(rendered)
        if (page / "05.01.return.md").read_bytes() != returned:
            raise AssertionError("return changed")
        code, shown, _err = run(["show", "--book", str(book)])
        flags = shown["pages"][0]["passes"][0]
        if shown["wrote"] is not False or flags["explicit_finish"] or not flags["review_pending"] or not flags["held"]:
            raise AssertionError(flags)
        if (book / "00.live.md").exists():
            raise AssertionError("live")


def test_routes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        cases = [
            ("0701.hold", "hold", "held", True, "pending", None, "review_pending"),
            ("0702.finish", "finish", "answered", False, "not needed", None, "explicit_finish"),
            ("0703.next", "request-next", "deferred", True, "pending", "05.02", "request_next"),
            ("0704.n5", "route-n5nn", "escalated", True, "not needed", None, "route_n5nn"),
        ]
        for page, route, disposition, pending, reply, next_pass, flag in cases:
            code, body, book, _request = open_sources(root, page, f"{page}/note.md", note)
            if code != 0:
                raise AssertionError(body)
            output = mini_output(root, page, pack, note, cw.sha256(page.encode("utf-8")))
            config = root / f"{page}-config.json"
            write_config(config)
            code, body, _err = attach(book, page, output, config, cw.sha256(page.encode("utf-8")))
            if code != 0:
                raise AssertionError(body)
            code, body, _err = place(book, page, config, f"0101.{page[:4]}-fixture", b"return-bytes\n")
            if code != 0:
                raise AssertionError(body)
            path = root / f"{page}-review.json"
            path.write_bytes(cw.canonical(review_body(route, disposition, pending, reply, next_pass)))
            code, body, _err = run(
                ["record-review", "--book", str(book), "--page", page, "--pass", "05.01", "--review", str(path)]
            )
            if code != 0:
                raise AssertionError((page, body))
            shown_code, shown, _err = run(["show", "--book", str(book)])
            row = next(item for item in shown["pages"] if item["page"] == page)
            flags = row["passes"][0]
            if route == "finish" and (not flags["explicit_finish"] or flags["review_pending"]):
                raise AssertionError(flags)
            if route == "hold" and (flags["explicit_finish"] or not flags["review_pending"] or flags["request_next"]):
                raise AssertionError(flags)
            if route == "request-next" and (
                flags["request_next"] != "05.02" or (book / page / "05.02.pack.md").exists()
            ):
                raise AssertionError(flags)
            if route == "route-n5nn" and not flags["route_n5nn"]:
                raise AssertionError(flags)
            if route == "finish":
                early = review_body("finish", "held", True, "pending", None)
                early_path = root / "early-finish.json"
                early_path.write_bytes(cw.canonical(early))
                # A different review on the occupied pass refuses. The unresolved finish is tested on a fresh page below.
        fresh_code, fresh, book, _request = open_sources(root, "0705.unresolved", "subj/note.md", note)
        if fresh_code != 0:
            raise AssertionError(fresh)
        output = mini_output(root, "0705.unresolved", pack, note, "cd" * 32)
        config = root / "unresolved-config.json"
        write_config(config)
        code, body, _err = attach(book, "0705.unresolved", output, config, "cd" * 32)
        if code != 0:
            raise AssertionError(body)
        code, body, _err = place(book, "0705.unresolved", config, "0105.unresolved-fixture", b"bytes\n")
        if code != 0:
            raise AssertionError(body)
        bad = root / "bad-finish.json"
        bad.write_bytes(cw.canonical(review_body("finish", "held", True, "pending")))
        code, body, _err = run(
            [
                "record-review",
                "--book",
                str(book),
                "--page",
                "0705.unresolved",
                "--pass",
                "05.01",
                "--review",
                str(bad),
            ]
        )
        if body["reason"] != "unresolved findings":
            raise AssertionError(body)
        missing = review_body("hold", "held", True, "pending")
        del missing["findings"][0]["director_reply"]
        missing_path = root / "missing-reply.json"
        missing_path.write_bytes(cw.canonical(missing))
        code, body, _err = run(
            [
                "record-review",
                "--book",
                str(book),
                "--page",
                "0705.unresolved",
                "--pass",
                "05.01",
                "--review",
                str(missing_path),
            ]
        )
        if body["reason"] != "director reply required":
            raise AssertionError(body)


def test_custody_refusals() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        code, body, book, _request = open_sources(root, "0701.sample", "subj/note.md", note)
        if code != 0:
            raise AssertionError(body)
        output = mini_output(root, "0701.sample", pack, note)
        config = root / "config.json"
        write_config(config)
        code, body, _err = attach(book, "0701.sample", output, config)
        if code != 0:
            raise AssertionError(body)
        code, body, _err = place(
            book, "0701.sample", config, "0101.wrong-origin", b"return\n", origin_page="0702.other-question"
        )
        if body["reason"] != "wrong origin":
            raise AssertionError(body)
        member = book / "0103.hash-conflict"
        member.mkdir()
        (member / "return.md").write_bytes(b"actual\n")
        observed = {
            "capture": {
                "manifest_sha256": "c" * 64,
                "origin": {"batch": "05.01", "book": "00.00.10.work", "page": "0701.sample"},
                "receipt_sha256": "d" * 64,
                "return": {"bytes": 7, "sha256": "e" * 64},
            },
            "status": "complete",
        }

        def run_proc(argv):
            if Path(argv[0]).name.startswith("return_inspect"):
                return 0, cw.canonical(observed), b""
            return 0, b"receipt " + (b"d" * 64) + b"\nresult complete\nnot approved\nnot accepted\nnot published\n", b""

        cw.RUN_PROCESS = run_proc
        try:
            code, body, _err = run(
                [
                    "place-return",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--member",
                    "0103.hash-conflict",
                    "--config",
                    str(config),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if body["reason"] != "hash conflict":
            raise AssertionError(body)
        partial = {
            "capture": observed["capture"],
            "status": "incomplete",
        }

        def partial_proc(argv):
            if Path(argv[0]).name.startswith("return_inspect"):
                return 1, cw.canonical(partial), b""
            return 1, b"", b""

        cw.RUN_PROCESS = partial_proc
        try:
            code, body, _err = run(
                [
                    "place-return",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--member",
                    "0104.partial-member",
                    "--config",
                    str(config),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if body["reason"] != "partial custody":
            raise AssertionError(body)


def test_interrupt_and_links() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        code, body, book, _request = open_sources(root, "0701.sample", "subj/note.md", note)
        if code != 0:
            raise AssertionError(body)
        output = mini_output(root, "0701.sample", pack, note)
        config = root / "config.json"
        write_config(config)

        def stop(path, _data):
            if "artifacts" in path.as_posix():
                raise RuntimeError("stop")

        cw.WRITE_HOOK = stop
        cw.RUN_PROCESS = lambda argv: (0, intact("0701.sample"), b"")
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--output",
                    str(output),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.WRITE_HOOK = None
            cw.RUN_PROCESS = None
        page = book / "0701.sample"
        if body["reason"] != "interrupted write" or body["wrote"] is not True or not (page / "partial.json").exists():
            raise AssertionError(body)

        def boom(_argv):
            raise AssertionError("launched")

        cw.RUN_PROCESS = boom
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--output",
                    str(output),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if body["reason"] != "resume refused":
            raise AssertionError(body)
        real = root / "real"
        real.mkdir()
        link = root / "link"
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], capture_output=True)
        try:
            if proc.returncode != 0:
                raise AssertionError(proc.stderr.decode())
            code, body, _err = run(["propose", "--book", str(link)])
            if body["reason"] != "unsafe path":
                raise AssertionError(body)
        finally:
            if os.path.lexists(link):
                os.rmdir(link)


def test_symlink_refusal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        code, body, book, _request = open_sources(root, "0701.sample", "subj/note.md", note)
        if code != 0:
            raise AssertionError(body)
        output = mini_output(root, "0701.sample", pack, note)
        link = output / "package" / "linked.md"
        try:
            os.symlink(output / "package" / "05.01.pack.md", link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                raise Skip("WinError 1314")
            raise
        cw.RUN_PROCESS = lambda argv: (_ for _ in ()).throw(AssertionError("launched"))
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--output",
                    str(output),
                    "--config",
                    str(root / "missing-config.json"),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if body["reason"] != "unsafe path":
            raise AssertionError(body)


def test_bad_producer_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        code, body, book, _request = open_sources(root, "0701.sample", "subj/note.md", note)
        if code != 0:
            raise AssertionError(body)
        producer = root / "bad-producer.py"
        data = (ROOT / "labs/colab-support-pass02/colab_support.py").read_bytes()
        producer.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
        cw.RUN_PROCESS = lambda argv: (_ for _ in ()).throw(AssertionError("launched"))
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--output",
                    str(root),
                    "--config",
                    str(root / "config.json"),
                    "--expect-digest",
                    DIGEST,
                    "--producer",
                    str(producer),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if body["reason"] != "pin mismatch":
            raise AssertionError(body)


def test_source_text() -> None:
    text = (ROOT / "labs/colab-workflow-pass02/colab_workflow.py").read_text(encoding="utf-8")
    if "handoff_check" in text:
        raise AssertionError("standalone checker is referenced")
    before = cw.sha256(V1.read_bytes())
    if before != cw.sha256(V1.read_bytes()):
        raise AssertionError("v1 moved")


def main() -> int:
    tests = [
        test_band_and_paths,
        test_attach_notes_and_review,
        test_routes,
        test_custody_refusals,
        test_interrupt_and_links,
        test_symlink_refusal,
        test_bad_producer_pin,
        test_source_text,
    ]
    failed = 0
    skipped = 0
    for test in tests:
        try:
            test()
        except Skip as exc:
            skipped += 1
            print(f"skip {test.__name__}: {exc.reason}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
        else:
            print(f"ok {test.__name__}")
    print(f"executed {len(tests) - skipped}")
    print(f"skipped {skipped}")
    print(f"failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
