"""Synthetic checks for workflow pass03. The producer process is stubbed here.

The real pinned verifier is test_real_two_pass.py. This file does not claim that
stubbed attach output was produced by the v2 preparer.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import colab_workflow as cw  # noqa: E402
from run_suite import aggregate  # noqa: E402


ROOT = Path(r"D:\Git\lib-build")
PASS02 = ROOT / "labs/colab-workflow-pass02/colab_workflow.py"
PASS02_SHA = "4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec"
DIGEST = "ab" * 32
DIGEST_B = "cd" * 32


class Skip(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def invoke(argv):
    code, out, err = cw.execute(argv)
    body = json.loads(out.decode("utf-8")) if out else None
    return code, body, err


def write_config(path: Path) -> None:
    cfg = {
        "assembler": str(ROOT / "labs/pack-assembly-pass01/pack_assembly.py"),
        "checker": str(ROOT / "labs/pack-custody-pass01/pack_check.py"),
        "helper": str(ROOT / "labs/return-capture-pass01/return_capture.py"),
        "inspector": str(ROOT / "labs/return-capture-pass01/return_inspect.py"),
        "producer_v1": str(ROOT / "labs/colab-support-pass01/colab_support.py"),
        "python": str(sys.executable),
        "repositories": {"workshop": str(ROOT)},
        "schema": "colab-config/2",
    }
    path.write_bytes(cw.canonical(cfg))


def target(relative: str, data: bytes) -> dict:
    return {
        "book": "00.00.10.work",
        "file": Path(relative).name,
        "id": "T01",
        "page": "0411.colab",
        "section": None,
        "source": {
            "commit": "6896224510fe0bcebac291fce7ed311a2cd085cb",
            "path": relative,
            "repository": "workshop",
            "sha256": cw.sha256(data),
        },
    }


def open_page(root: Path, page: str, note: bytes = b"# Notes\n", pass_id: str = "05.01") -> tuple[Path, dict]:
    sources = root / f"sources-{page}"
    dest = sources / "subj" / "note.md"
    dest.parent.mkdir(parents=True)
    dest.write_bytes(note)
    body = {
        "book": "00.00.10.work",
        "page": page,
        "pass": pass_id,
        "schema": "colab-exchange-open/1",
        "targets": [target("subj/note.md", note)],
        "title": "Exchange question",
    }
    path = root / f"open-{page}.json"
    path.write_bytes(cw.canonical(body))
    book = root / f"book-{page}"
    book.mkdir()
    code, result, _err = invoke(
        ["open", "--book", str(book), "--request", str(path), "--sources", str(sources)]
    )
    if code != 0:
        raise AssertionError(result)
    return book, body


def mini_output(root: Path, page: str, pass_id: str, pack: bytes, notes: bytes, digest: str) -> Path:
    nn = pass_id.split(".")[1]
    output = root / f"output-{page}-{pass_id}"
    package = output / "package"
    package.mkdir(parents=True)
    (package / f"05.{nn}.pack.md").write_bytes(pack)
    (package / f"06.{nn}.notes.md").write_bytes(notes)
    (output / "prepared-colab.zip").write_bytes(b"zip-" + pass_id.encode("ascii"))
    files = {
        f"package/05.{nn}.pack.md": pack,
        f"package/06.{nn}.notes.md": notes,
        "prepared-colab.zip": b"zip-" + pass_id.encode("ascii"),
    }
    recorded = {
        "digest": digest,
        "investigation": {"book": "00.00.10.work", "page": page, "pass": pass_id},
        "out_files": [
            {"bytes": len(data), "path": name, "sha256": cw.sha256(data)} for name, data in sorted(files.items())
        ],
        "result": "prepared",
        "schema": "colab-package-verification/2",
    }
    (output / "verification.json").write_bytes(cw.canonical(recorded))
    return output


def intact(page: str, pass_id: str, digest: str) -> bytes:
    nn = pass_id.split(".")[1]
    return cw.canonical(
        {
            "digest": digest,
            "exchange": {
                "notes": f"06.{nn}.notes.md",
                "pack": f"05.{nn}.pack.md",
                "pass": pass_id,
                "return_name": f"05.{nn}.return.md",
                "review_name": f"06.{nn}.review.md",
            },
            "investigation": {"book": "00.00.10.work", "page": page, "pass": pass_id},
            "result": "intact",
        }
    )


def attach(book: Path, page: str, pass_id: str, output: Path, config: Path, digest: str):
    cw.RUN_PROCESS = lambda argv: (0, intact(page, pass_id, digest), b"")
    try:
        return invoke(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                page,
                "--pass",
                pass_id,
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


def review_body(route: str, disposition: str, pending: bool, next_pass) -> dict:
    return {
        "assessment": "Supplied fixture assessment. The tool does not judge it.",
        "by": "Codex Prime",
        "findings": [
            {
                "consequential": True,
                "director_reply": "Recorded for the fixture.",
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


def write_review(root: Path, name: str, body: dict) -> Path:
    path = root / name
    path.write_bytes(cw.canonical(body))
    return path


def seal(book: Path, page: str, pass_id: str, data: bytes, transport: str, root: Path):
    path = root / f"return-{pass_id}.bin"
    path.write_bytes(data)
    return invoke(
        [
            "seal-return-local",
            "--book",
            str(book),
            "--page",
            page,
            "--pass",
            pass_id,
            "--return-file",
            str(path),
            "--declared-transport",
            transport,
        ]
    )


def transitions(page: Path) -> list[dict]:
    record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
    return record["transitions"]


def file_map(page: Path) -> dict[str, bytes]:
    found = {}
    for path in page.rglob("*"):
        if path.is_file():
            found[path.relative_to(page).as_posix()] = path.read_bytes()
    return found


def test_paths_and_schema() -> None:
    code, body, err = invoke(["propose", "--book", r"D:\Git\lib-build\00.kernel\00.00.10.work"])
    if body["reason"] != "live work book is not a fixture":
        raise AssertionError(body)
    code, body, err = invoke(["propose", "--book", "book"])
    if body["reason"] != "book path is not absolute" or err:
        raise AssertionError((body, err))
    code, _out, err = cw.execute(["nope"])
    if code != 2 or err != b"usage\n":
        raise AssertionError((code, err))
    with tempfile.TemporaryDirectory(prefix="0511-0504-band-") as tmp:
        root = Path(tmp)
        book, _request = open_page(root, "0701.sample")
        code, body, _err = invoke(["propose", "--book", str(book)])
        if body.get("page") != "0702.free":
            raise AssertionError(body)
        path = root / "open-0701.sample.json"
        code, body, _err = invoke(
            ["open", "--book", str(book), "--request", str(path), "--sources", str(root / "sources-0701.sample")]
        )
        if body["reason"] != "occupied page":
            raise AssertionError(body)
        bad = {
            "book": "00.00.10.work",
            "page": "0700.door",
            "pass": "05.01",
            "schema": "colab-exchange-open/1",
            "targets": [target("subj/note.md", b"# Notes\n")],
            "title": "Exchange question",
        }
        bad_path = root / "bad-open.json"
        bad_path.write_bytes(cw.canonical(bad))
        code, body, _err = invoke(
            ["open", "--book", str(book), "--request", str(bad_path), "--sources", str(root / "sources-0701.sample")]
        )
        if body["reason"] != "outside declared band":
            raise AssertionError(body)
        legacy = book / "0703.legacy"
        legacy.mkdir()
        record = {"schema": "colab-exchange-investigation/1", "page": "0703.legacy"}
        data = cw.canonical(record)
        (legacy / "investigation.json").write_bytes(data)
        (legacy / "seal.json").write_bytes(cw.canonical({"schema": cw.SEAL_SCHEMA, "sha256": cw.sha256(data)}))
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["reason"] != "unknown schema" or body["wrote"] is not False:
            raise AssertionError(body)


def test_local_return_and_next_pass() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-local-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        book, _request = open_page(root, "0701.sample", note)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0701.sample", "05.01", pack, note, DIGEST)
        code, body, _err = attach(book, "0701.sample", "05.01", output, config, DIGEST)
        if code != 0 or body["result"] != "complete":
            raise AssertionError(body)
        code, body, _err = attach(book, "0701.sample", "05.01", output, config, DIGEST)
        if body["result"] != "repeat" or body["wrote"] is not False:
            raise AssertionError(body)
        page = book / "0701.sample"
        before_notes = (page / "artifacts/05.01/package/06.01.notes.md").read_bytes()
        code, body, _err = invoke(
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
        if code != 0 or (page / "artifacts/05.01/package/06.01.notes.md").read_bytes() != before_notes:
            raise AssertionError(body)
        lf = b"local line\n"
        crlf = b"local line\r\nsecond\r\n"
        code, body, _err = seal(book, "0701.sample", "05.01", lf, "desk copy", root)
        if code != 0 or (page / "05.01.return.md").read_bytes() != lf:
            raise AssertionError(body)
        if (page / "artifacts/05.01/return.md").read_bytes() != lf or b"\r" in lf:
            raise AssertionError("lf bytes")
        seal_bytes = (page / "seal.json").read_bytes()
        count = len(transitions(page))
        code, again, _err = seal(book, "0701.sample", "05.01", lf, "desk copy", root)
        if again["result"] != "repeat" or again["wrote"] is not False or len(transitions(page)) != count:
            raise AssertionError(again)
        if (page / "seal.json").read_bytes() != seal_bytes:
            raise AssertionError("replay wrote a seal")
        code, body, _err = seal(book, "0701.sample", "05.01", crlf, "desk copy", root)
        if body["reason"] != "occupied different content" or body["wrote"] is not False:
            raise AssertionError(body)
        if (page / "05.01.return.md").read_bytes() != lf:
            raise AssertionError("conflicting return rewrote bytes")
        code, body, _err = seal(book, "0701.sample", "05.01", lf, "other label", root)
        if body["reason"] != "declared transport differs" or body["wrote"] is not False:
            raise AssertionError(body)
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        if record["passes"]["05.01"]["return"]["declared_transport"] != "desk copy":
            raise AssertionError("transport label was rewritten")
        code, body, _err = seal(book, "0701.sample", "05.02", lf, "desk copy", root)
        if body["reason"] != "missing investigation":
            raise AssertionError(body)
        huge = root / "huge.bin"
        huge.write_bytes(b"x" * (cw.RETURN_LIMIT + 1))
        code, body, _err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--return-file",
                str(huge),
                "--declared-transport",
                "desk copy",
            ]
        )
        if body["reason"] != "declared limit" or body["wrote"] is not False:
            raise AssertionError(body)
        code, body, _err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--return-file",
                str(root),
                "--declared-transport",
                "desk copy",
            ]
        )
        if body["reason"] != "return file is missing":
            raise AssertionError(body)
        empty = root / "empty-label.txt"
        empty.write_bytes(b"x")
        code, body, _err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--return-file",
                str(empty),
                "--declared-transport",
                "",
            ]
        )
        if body["reason"] != "malformed declared transport":
            raise AssertionError(body)
        held = write_review(root, "hold.json", review_body("hold", "held", True, None))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--review", str(held)]
        )
        if code != 0:
            raise AssertionError(body)
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0701.sample", "--pass", "05.02"])
        if body["reason"] != "next pass not requested":
            raise AssertionError(body)
        # The held review occupies the slot. A second book covers request-next.
    with tempfile.TemporaryDirectory(prefix="0511-0504-next-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack\n"
        book, _request = open_page(root, "0704.next", note)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0704.next", "05.01", pack, note, DIGEST)
        code, body, _err = attach(book, "0704.next", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        page = book / "0704.next"
        code, body, _err = seal(book, "0704.next", "05.01", b"first\n", "desk copy", root)
        if code != 0:
            raise AssertionError(body)
        planted = page / "05.02.pack.md"
        planted.write_bytes(b"planted\n")
        asking = write_review(root, "ask.json", review_body("request-next", "answered", False, "05.02"))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", "0704.next", "--pass", "05.01", "--review", str(asking)]
        )
        if body["reason"] != "malformed review" or body["wrote"] is not True:
            raise AssertionError(body)
        planted.unlink()
        # The review was committed before the pack-file check. Continue on a clean book.
    with tempfile.TemporaryDirectory(prefix="0511-0504-two-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        pack = b"# Pack one\n"
        pack_b = b"# Pack two\n"
        book, _request = open_page(root, "0705.two", note)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0705.two", "05.01", pack, note, DIGEST)
        code, body, _err = attach(book, "0705.two", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        page = book / "0705.two"
        first = b"pass-one\r\nkept\r\n"
        code, body, _err = seal(book, "0705.two", "05.01", first, "desk copy", root)
        if code != 0 or (page / "05.01.return.md").read_bytes() != first:
            raise AssertionError(body)
        asking = write_review(root, "ask.json", review_body("request-next", "answered", False, "05.02"))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", "0705.two", "--pass", "05.01", "--review", str(asking)]
        )
        if code != 0:
            raise AssertionError(body)
        saved = {
            "05.01.pack.md": (page / "05.01.pack.md").read_bytes(),
            "05.01.return.md": (page / "05.01.return.md").read_bytes(),
            "06.01.review.md": (page / "06.01.review.md").read_bytes(),
            "06.01.notes.md": (page / "06.01.notes.md").read_bytes(),
            "snapshot": (page / "artifacts/05.01/package/06.01.notes.md").read_bytes(),
        }
        face_before = (page / "01.md").read_bytes()
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0705.two", "--pass", "05.02"])
        if code != 0 or body["result"] != "complete":
            raise AssertionError(body)
        if (page / "01.md").read_bytes() == face_before:
            raise AssertionError("index projection did not gain the new pass")
        for name, data in saved.items():
            path = page / "artifacts/05.01/package/06.01.notes.md" if name == "snapshot" else page / name
            if path.read_bytes() != data:
                raise AssertionError(name)
        for name in ("05.02.pack.md", "05.02.return.md", "06.02.notes.md", "06.02.review.md"):
            if (page / name).exists():
                raise AssertionError(name)
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0705.two", "--pass", "05.01"])
        if body["reason"] != "next pass not requested" or body["wrote"] is not False:
            raise AssertionError(body)
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0705.two", "--pass", "05.03"])
        if body["reason"] != "next pass not requested":
            raise AssertionError(body)
        output_b = mini_output(root, "0705.two", "05.02", pack_b, b"# Notes two\n", DIGEST_B)
        code, body, _err = attach(book, "0705.two", "05.02", output_b, config, DIGEST_B)
        if code != 0:
            raise AssertionError(body)
        count = len(transitions(page))
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0705.two", "--pass", "05.02"])
        if body["result"] != "repeat" or body["wrote"] is not False or len(transitions(page)) != count:
            raise AssertionError(body)
        if (page / "artifacts/05.02/package/05.02.pack.md").read_bytes() != pack_b:
            raise AssertionError("replay erased the second package")
        second = b"pass-two\n"
        code, body, _err = seal(book, "0705.two", "05.02", second, "later desk", root)
        if (page / "05.02.return.md").read_bytes() != second or (page / "05.01.return.md").read_bytes() != first:
            raise AssertionError("return bytes moved")
        finish = write_review(root, "finish.json", review_body("finish", "answered", False, None))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", "0705.two", "--pass", "05.02", "--review", str(finish)]
        )
        if code != 0:
            raise AssertionError(body)
        for name, data in saved.items():
            path = page / "artifacts/05.01/package/06.01.notes.md" if name == "snapshot" else page / name
            if path.read_bytes() != data:
                raise AssertionError("later work changed " + name)
        before_tree = file_map(page)
        code, shown, _err = invoke(["show", "--book", str(book)])
        if shown["wrote"] is not False or file_map(page) != before_tree:
            raise AssertionError("show wrote")
        row = shown["pages"][0]
        flags = {item["pass"]: item for item in row["passes"]}
        if flags["05.01"]["return_kind"] != "page-local" or flags["05.01"]["request_next"] != "05.02":
            raise AssertionError(flags["05.01"])
        if flags["05.02"]["explicit_finish"] is not True or flags["05.02"]["review_pending"] is not False:
            raise AssertionError(flags["05.02"])
        if "complete" in flags["05.02"]:
            raise AssertionError("review_pending false was stored as complete")
        actions = [item["action"] for item in row["transitions"]]
        if actions != ["open", "attach", "seal-return", "review", "open-pass", "attach", "seal-return", "review"]:
            raise AssertionError(actions)
        if [item["seq"] for item in row["transitions"]] != list(range(1, 9)):
            raise AssertionError("sequence")
        names = sorted(path.name for path in page.iterdir() if path.is_file())
        wanted = {
            "01.md",
            "05.01.pack.md",
            "05.01.return.md",
            "05.02.pack.md",
            "05.02.return.md",
            "06.01.notes.md",
            "06.01.review.md",
            "06.02.notes.md",
            "06.02.review.md",
            "08.md",
            "investigation.json",
            "seal.json",
        }
        if set(names) != wanted:
            raise AssertionError(names)
        pointer = (page / "08.md").read_text(encoding="utf-8")
        if "member " in pointer or "05.02: page-local return" not in pointer:
            raise AssertionError(pointer)


def test_legacy_place_is_not_the_seal() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-n1-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        book, _request = open_page(root, "0706.legacy", note)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0706.legacy", "05.01", b"# Pack\n", note, DIGEST)
        code, body, _err = attach(book, "0706.legacy", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        member = "0161.fixture-return"
        data = b"captured\n"
        member_dir = book / member
        member_dir.mkdir()
        (member_dir / "return.md").write_bytes(data)
        observed = {
            "capture": {
                "manifest_sha256": "c" * 64,
                "origin": {"batch": "05.01", "book": "00.00.10.work", "page": "0706.legacy"},
                "receipt_sha256": "d" * 64,
                "return": {"bytes": len(data), "sha256": cw.sha256(data)},
            },
            "status": "complete",
        }
        verify = f"receipt {'d' * 64}\nresult complete\nnot approved\nnot accepted\nnot published\n".encode("utf-8")

        def run_proc(argv):
            if Path(argv[0]).name.startswith("return_inspect"):
                return 0, cw.canonical(observed), b""
            return 0, verify, b""

        cw.RUN_PROCESS = run_proc
        try:
            code, body, _err = invoke(
                [
                    "place-return",
                    "--book",
                    str(book),
                    "--page",
                    "0706.legacy",
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
        if code != 0 or body.get("member") != member:
            raise AssertionError(body)
        page = book / "0706.legacy"
        if (page / "05.01.return.md").read_bytes() != data:
            raise AssertionError("placed bytes")
        code, body, _err = seal(book, "0706.legacy", "05.01", data, "desk copy", root)
        if body["reason"] != "occupied different content" or (page / "05.01.return.md").read_bytes() != data:
            raise AssertionError(body)
        asking = write_review(root, "ask.json", review_body("request-next", "answered", False, "05.02"))
        code, body, _err = invoke(
            [
                "record-review",
                "--book",
                str(book),
                "--page",
                "0706.legacy",
                "--pass",
                "05.01",
                "--review",
                str(asking),
            ]
        )
        if code != 0:
            raise AssertionError(body)
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0706.legacy", "--pass", "05.02"])
        if body["reason"] != "local return required" or (page / "05.02.pack.md").exists():
            raise AssertionError(body)


def test_earlier_pass() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-earlier-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        page_name = "0715.earlier"
        book, _request = open_page(root, page_name, note, "05.03")
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, page_name, "05.03", b"# Pack three\n", note, DIGEST)
        code, body, _err = attach(book, page_name, "05.03", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        first = b"third\n"
        code, body, _err = seal(book, page_name, "05.03", first, "desk copy", root)
        if code != 0:
            raise AssertionError(body)
        asking = write_review(root, "ask.json", review_body("request-next", "answered", False, "05.04"))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", page_name, "--pass", "05.03", "--review", str(asking)]
        )
        if code != 0:
            raise AssertionError(body)
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", page_name, "--pass", "05.04"])
        if code != 0:
            raise AssertionError(body)
        output_b = mini_output(root, page_name, "05.04", b"# Pack four\n", b"# Notes four\n", DIGEST_B)
        code, body, _err = attach(book, page_name, "05.04", output_b, config, DIGEST_B)
        if code != 0:
            raise AssertionError(body)
        code, body, _err = seal(book, page_name, "05.04", b"fourth\n", "later desk", root)
        if code != 0:
            raise AssertionError(body)
        back = write_review(root, "back.json", review_body("request-next", "answered", False, "05.02"))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", page_name, "--pass", "05.04", "--review", str(back)]
        )
        if code != 0:
            raise AssertionError(body)
        page = book / page_name
        before = (page / "investigation.json").read_bytes()
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", page_name, "--pass", "05.02"])
        if body["reason"] != "earlier pass" or body["wrote"] is not False:
            raise AssertionError(body)
        if (page / "investigation.json").read_bytes() != before or (page / "05.03.return.md").read_bytes() != first:
            raise AssertionError("earlier refusal changed the sealed pass")
        if (page / "05.02.pack.md").exists():
            raise AssertionError("earlier refusal created a pass")


def test_open_pass_predicates() -> None:
    local = {"kind": "page-local", "schema": cw.LOCAL_RETURN_SCHEMA}

    def review(next_pass: str) -> dict:
        return {"route": "request-next", "next_pass": next_pass}

    def one(pid: str, nxt: str | None) -> dict:
        return {
            "notes": [],
            "package": {"digest": DIGEST},
            "return": local,
            "review": None if nxt is None else review(nxt),
        }

    both = {"passes": {"05.01": one("05.01", "05.03"), "05.02": one("05.02", "05.03")}, "transitions": []}
    if cw.open_pass_decision(both, "05.03")[0] != "conflicting requests":
        raise AssertionError("conflict")
    occupied = {
        "passes": {"05.01": one("05.01", "05.03"), "05.03": one("05.03", None)},
        "transitions": [{"action": "open", "pass": "05.03", "facts": {}}],
    }
    if cw.open_pass_decision(occupied, "05.03")[0] != "occupied pass":
        raise AssertionError("occupied")
    different = {
        "passes": {"05.01": one("05.01", "05.02"), "05.02": one("05.02", None)},
        "transitions": [
            {
                "action": "open-pass",
                "pass": "05.02",
                "facts": {"opened_pass": "05.02", "requested_by": "05.01", "review_sha256": "0" * 64},
            }
        ],
    }
    if cw.open_pass_decision(different, "05.02")[0] != "occupied different state":
        raise AssertionError("different")
    missing = {"passes": {"05.01": one("05.01", "05.02")}, "transitions": []}
    missing["passes"]["05.01"]["return"] = None
    if cw.open_pass_decision(missing, "05.02")[0] != "sealed return missing":
        raise AssertionError("missing seal")


def test_tamper_and_recomputed_chain() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-tamper-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        book, _request = open_page(root, "0707.tamper", note)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0707.tamper", "05.01", b"# Pack\n", note, DIGEST)
        code, body, _err = attach(book, "0707.tamper", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        page = book / "0707.tamper"
        data = b"sealed\r\n"
        code, body, _err = seal(book, "0707.tamper", "05.01", data, "desk copy", root)
        if code != 0:
            raise AssertionError(body)
        projected = page / "05.01.return.md"
        original = projected.read_bytes()
        projected.write_bytes(original + b" ")
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["reason"] != "hash conflict" or body["wrote"] is not False or projected.read_bytes() != original + b" ":
            raise AssertionError(body)
        projected.write_bytes(original)
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        record["passes"]["05.01"]["return"]["return_sha256"] = "e" * 64
        rewritten = cw.canonical(record)
        (page / "investigation.json").write_bytes(rewritten)
        (page / "seal.json").write_bytes(cw.canonical({"schema": cw.SEAL_SCHEMA, "sha256": cw.sha256(rewritten)}))
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["reason"] != "hash conflict":
            raise AssertionError(body)
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        record["passes"]["05.01"]["return"]["return_sha256"] = cw.sha256(data)
        record["title"] = "Rewritten title"
        previous = []
        rebuilt = []
        for item in record["transitions"]:
            facts = dict(item["facts"])
            if item["action"] == "open":
                facts["title"] = record["title"]
            rebuilt.append(cw.make_transition(previous, item["action"], item["pass"], facts))
            previous = rebuilt
        record["transitions"] = rebuilt
        cw.commit(page, record)
        code, shown, _err = invoke(["show", "--book", str(book)])
        if code != 0 or shown["pages"][0]["transitions"][0]["facts"]["title"] != "Rewritten title":
            raise AssertionError(shown)
        raw = (page / "investigation.json").read_bytes()
        (page / "investigation.json").write_bytes(raw + b" ")
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["reason"] != "resume refused":
            raise AssertionError(body)


def test_interrupts() -> None:
    def stage(root: Path, page: str) -> tuple[Path, Path]:
        book, _request = open_page(root, page)
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, page, "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
        code, body, _err = attach(book, page, "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        return book, book / page

    def fail_once(marker: str):
        def hook(path, _data):
            text = path.as_posix()
            if marker == "artifact" and text.endswith("/artifacts/05.01/return.md"):
                raise RuntimeError("stop")
            if marker == "projection" and path.name == "05.01.return.md":
                raise RuntimeError("stop")
            if marker == "record" and path.name == "investigation.json":
                raise RuntimeError("stop")
            if marker == "seal" and path.name == "seal.json":
                raise RuntimeError("stop")

        return hook

    with tempfile.TemporaryDirectory(prefix="0511-0504-stop-") as tmp:
        root = Path(tmp)
        book, page = stage(root, "0708.stop")
        before = (page / "investigation.json").read_bytes()
        cw.WRITE_HOOK = fail_once("artifact")
        try:
            code, body, _err = seal(book, "0708.stop", "05.01", b"x\n", "desk copy", root)
        finally:
            cw.WRITE_HOOK = None
        if body["reason"] != "interrupted write" or body["wrote"] is not True or not (page / "partial.json").exists():
            raise AssertionError(body)
        if (page / "investigation.json").read_bytes() != before or (page / ".write.lock").exists():
            raise AssertionError("authoritative record moved")
        code, body, _err = invoke(["show", "--book", str(book)])
        row = body["pages"][0]
        if body["result"] != "complete" or row["partial"] is not True or row["transitions"] is not None:
            raise AssertionError(body)
        code, body, _err = seal(book, "0708.stop", "05.01", b"x\n", "desk copy", root)
        if body["reason"] != "resume refused" or body["wrote"] is not False:
            raise AssertionError(body)

    for marker, page_name in (("projection", "0709.proj"), ("record", "0710.record"), ("seal", "0711.seal")):
        with tempfile.TemporaryDirectory(prefix=f"0511-0504-{marker}-") as tmp:
            root = Path(tmp)
            book, page = stage(root, page_name)
            before = (page / "investigation.json").read_bytes()
            old_seal = (page / "seal.json").read_bytes()
            cw.WRITE_HOOK = fail_once(marker)
            try:
                code, body, _err = seal(book, page_name, "05.01", b"y\n", "desk copy", root)
            finally:
                cw.WRITE_HOOK = None
            if body["reason"] != "interrupted write" or body["wrote"] is not True or not (page / "partial.json").exists():
                raise AssertionError((marker, body))
            if marker in ("projection", "record") and (page / "investigation.json").read_bytes() != before:
                raise AssertionError(marker)
            if marker == "seal":
                if (page / "seal.json").read_bytes() != old_seal:
                    raise AssertionError("seal truncated")
                if cw.sha256((page / "investigation.json").read_bytes()) == json.loads(old_seal.decode())["sha256"]:
                    raise AssertionError("seal still matches the new record")
            code, later, _err = invoke(["show", "--book", str(book)])
            if later["pages"][0]["partial"] is not True:
                raise AssertionError(marker)


def test_interrupt_attach_and_links() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-link-") as tmp:
        root = Path(tmp)
        book, _request = open_page(root, "0712.link")
        output = mini_output(root, "0712.link", "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
        config = root / "config.json"
        write_config(config)

        def stop(path, _data):
            if "artifacts" in path.as_posix():
                raise RuntimeError("stop")

        cw.WRITE_HOOK = stop
        cw.RUN_PROCESS = lambda argv: (0, intact("0712.link", "05.01", DIGEST), b"")
        try:
            code, body, _err = invoke(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0712.link",
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
        page = book / "0712.link"
        if body["reason"] != "interrupted write" or body["wrote"] is not True or not (page / "partial.json").exists():
            raise AssertionError(body)
        real = root / "real"
        real.mkdir()
        link = root / "link"
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], capture_output=True)
        try:
            if proc.returncode != 0:
                raise AssertionError(proc.stderr.decode())
            code, body, _err = invoke(["propose", "--book", str(link)])
            if body["reason"] != "unsafe path":
                raise AssertionError(body)
        finally:
            if os.path.lexists(link):
                os.rmdir(link)


def test_symlink_refusal() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0504-sym-") as tmp:
        root = Path(tmp)
        book, _request = open_page(root, "0713.sym")
        output = mini_output(root, "0713.sym", "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
        link = output / "package" / "linked.md"
        try:
            os.symlink(output / "package" / "05.01.pack.md", link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                raise Skip("WinError 1314")
            raise
        cw.RUN_PROCESS = lambda argv: (_ for _ in ()).throw(AssertionError("launched"))
        try:
            code, body, _err = invoke(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0713.sym",
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
    with tempfile.TemporaryDirectory(prefix="0511-0504-pin-") as tmp:
        root = Path(tmp)
        book, _request = open_page(root, "0714.pin")
        producer = root / "bad-producer.py"
        data = (ROOT / "labs/colab-support-pass02/colab_support.py").read_bytes()
        producer.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
        cw.RUN_PROCESS = lambda argv: (_ for _ in ()).throw(AssertionError("launched"))
        try:
            code, body, _err = invoke(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    "0714.pin",
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


def test_source_and_runner() -> None:
    text = (LAB / "colab_workflow.py").read_text(encoding="utf-8")
    if "handoff_check" in text:
        raise AssertionError("standalone checker is referenced")
    raw = PASS02.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PASS02_SHA or len(raw) != 47247:
        raise AssertionError("pass02 changed")
    seen = []

    def ok():
        seen.append("kept")
        return 0

    def bad():
        seen.append("still-here")
        return 7

    def later():
        seen.append("after")
        return 0

    if aggregate([ok, bad, later]) != 1 or seen != ["kept", "still-here", "after"]:
        raise AssertionError(seen)


def main() -> int:
    tests = [
        test_paths_and_schema,
        test_local_return_and_next_pass,
        test_earlier_pass,
        test_legacy_place_is_not_the_seal,
        test_open_pass_predicates,
        test_tamper_and_recomputed_chain,
        test_interrupts,
        test_interrupt_attach_and_links,
        test_symlink_refusal,
        test_bad_producer_pin,
        test_source_and_runner,
    ]
    failed = 0
    skipped = 0
    for test in tests:
        try:
            test()
        except Skip as exc:
            skipped += 1
            print(f"skip {test.__name__}: {exc.reason}", flush=True)
        except Exception as exc:  # noqa: BLE001 - the runner must keep going
            failed += 1
            print(f"FAIL {test.__name__}: {exc}", flush=True)
        else:
            print(f"ok {test.__name__}", flush=True)
    print(f"executed {len(tests) - skipped}")
    print(f"skipped {skipped}")
    print(f"failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
