"""Focused pass04 checks. Producer calls in this file are stubbed.

The real pinned verifier is test_real_two_pass.py. Mid-write failures inject
os.write after bytes have been accepted. They are not power-loss trials.
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
import run_suite  # noqa: E402


ROOT = Path(r"D:\Git\lib-build")
PASS02 = ROOT / "labs/colab-workflow-pass02/colab_workflow.py"
PASS03 = ROOT / "labs/colab-workflow-pass03/colab_workflow.py"
PASS02_SHA = "4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec"
PASS03_SHA = "fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944"
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


def open_page(root: Path, page: str, pass_id: str = "05.01") -> Path:
    note = b"# Notes\n"
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
    return book


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


def review_body(route: str, next_pass) -> dict:
    return {
        "assessment": "Supplied fixture assessment. The tool does not judge it.",
        "by": "Codex Prime",
        "findings": [
            {
                "consequential": True,
                "director_reply": "Recorded for the fixture.",
                "disposition": "answered",
                "id": "F01",
                "observation": "A reader could mistake notes for a review.",
                "pending": False,
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


def stage_attached(root: Path, page: str) -> tuple[Path, Path]:
    book = open_page(root, page)
    config = root / "config.json"
    write_config(config)
    output = mini_output(root, page, "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
    code, body, _err = attach(book, page, "05.01", output, config, DIGEST)
    if code != 0:
        raise AssertionError(body)
    return book, book / page


def prepare_second(root: Path, page: str) -> tuple[Path, Path, dict[str, bytes]]:
    book, folder = stage_attached(root, page)
    code, body, _err = seal(book, page, "05.01", b"pass-one\r\nkept\r\n", "desk copy", root)
    if code != 0:
        raise AssertionError(body)
    asking = root / "ask.json"
    asking.write_bytes(cw.canonical(review_body("request-next", "05.02")))
    code, body, _err = invoke(
        ["record-review", "--book", str(book), "--page", page, "--pass", "05.01", "--review", str(asking)]
    )
    if code != 0:
        raise AssertionError(body)
    code, body, _err = invoke(["open-pass", "--book", str(book), "--page", page, "--pass", "05.02"])
    if code != 0:
        raise AssertionError(body)
    output = mini_output(root, page, "05.02", b"# Pack two\n", b"# Notes two\n", DIGEST_B)
    code, body, _err = attach(book, page, "05.02", output, root / "config.json", DIGEST_B)
    if code != 0:
        raise AssertionError(body)
    saved = {
        "artifact": (folder / "artifacts/05.01/return.md").read_bytes(),
        "pack": (folder / "artifacts/05.01/package/05.01.pack.md").read_bytes(),
        "review": (folder / "06.01.review.md").read_bytes(),
        "projection": (folder / "05.01.return.md").read_bytes(),
    }
    return book, folder, saved


def install_midwrite(match):
    real_open = cw.os.open
    real_write = cw.os.write
    state = {"fd": None, "calls": 0, "done": False}

    def op(path, *args, **kwargs):
        fd = real_open(path, *args, **kwargs)
        text = str(path).replace("\\", "/")
        if state["fd"] is None and match(text):
            state["fd"] = fd
        return fd

    def wr(fd, data):
        if fd == state["fd"] and not state["done"]:
            state["calls"] += 1
            if state["calls"] == 1:
                return real_write(fd, data[: max(1, len(data) // 2)])
            state["done"] = True
            raise OSError("SYNTHETIC mid-write failure after partial record write")
        return real_write(fd, data)

    cw.os.open = op
    cw.os.write = wr
    return real_open, real_write, state


def restore_io(real_open, real_write) -> None:
    cw.os.open = real_open
    cw.os.write = real_write


def staging_record(text: str) -> bool:
    return "/staging/" in text and text.endswith("/investigation.json")


def projection_pointer(text: str) -> bool:
    return "/projections/" in text and text.endswith("/08.md")


def assert_refused(body, folder: Path) -> None:
    if body["result"] == "complete" or body["reason"] != "interrupted write" or body["wrote"] is not True:
        raise AssertionError(body)
    if not (folder / "partial.json").exists() or not (folder / "attempt.json").exists():
        raise AssertionError("missing partial identity")
    if (folder / ".write.lock").exists():
        raise AssertionError("lock left behind")
    partial = json.loads((folder / "partial.json").read_text(encoding="utf-8"))
    attempt = json.loads((folder / "attempt.json").read_text(encoding="utf-8"))
    if partial["publication_id"] != attempt["publication_id"]:
        raise AssertionError("publication identity differs")
    if partial["retained_checkpoint"] != attempt["retained_checkpoint"]:
        raise AssertionError("checkpoint identity differs")
    if partial["reason"] != "interrupted write":
        raise AssertionError(partial)


def assert_blocked(book: Path) -> None:
    code, body, _err = invoke(["show", "--book", str(book)])
    row = body["pages"][0]
    if body["result"] != "complete" or row["partial"] is not True or row["transitions"] is not None:
        raise AssertionError(body)
    code, later, _err = invoke(["append-note", "--book", str(book), "--page", row["page"], "--pass", "05.01", "--text", "later"])
    if later["reason"] != "resume refused" or later["wrote"] is not False:
        raise AssertionError(later)


def test_successor_midwrite_keeps_root_pair() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-wf01-") as tmp:
        root = Path(tmp)
        book = open_page(root, "0721.wf01")
        folder = book / "0721.wf01"
        before_open = (folder / "investigation.json").read_bytes()
        record = cw.require_loaded(folder)
        try:
            cw.commit(folder, record)
        except cw.Refuse as exc:
            if exc.reason != "publication collision" or exc.wrote is not False:
                raise AssertionError(exc.reason) from exc
        else:
            raise AssertionError("identical republish completed")
        if (folder / "investigation.json").read_bytes() != before_open or (folder / "partial.json").exists():
            raise AssertionError("identical republish changed the root pair")
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0721.wf01", "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
        code, body, _err = attach(book, "0721.wf01", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()
        real_open, real_write, state = install_midwrite(staging_record)
        try:
            code, body, _err = seal(book, "0721.wf01", "05.01", b"kept\n", "desk copy", root)
        finally:
            restore_io(real_open, real_write)
        assert_refused(body, folder)
        if state["fd"] is None or state["calls"] < 2:
            raise AssertionError("mid-write was not injected during the staged record")
        if (folder / "investigation.json").read_bytes() != before or (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("root pair changed")
        checkpoint = folder / "checkpoints" / cw.sha256(before)
        if (checkpoint / "investigation.json").read_bytes() != before or (checkpoint / "seal.json").read_bytes() != old_seal:
            raise AssertionError("checkpoint is not the prior pair")
        partial = json.loads((folder / "partial.json").read_text(encoding="utf-8"))
        if partial["predecessor"] != "retained-prior" or partial["retained_checkpoint"] != cw.sha256(before):
            raise AssertionError(partial)
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["pages"][0]["partial"] is not True or body["pages"][0]["transitions"] is not None:
            raise AssertionError(body)


def test_open_midwrite_invents_nothing() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-open-") as tmp:
        root = Path(tmp)
        page = "0722.open"
        note = b"# Notes\n"
        sources = root / "sources"
        dest = sources / "subj" / "note.md"
        dest.parent.mkdir(parents=True)
        dest.write_bytes(note)
        body = {
            "book": "00.00.10.work",
            "page": page,
            "pass": "05.01",
            "schema": "colab-exchange-open/1",
            "targets": [target("subj/note.md", note)],
            "title": "Exchange question",
        }
        request = root / "open.json"
        request.write_bytes(cw.canonical(body))
        book = root / "book"
        book.mkdir()
        real_open, real_write, state = install_midwrite(staging_record)
        try:
            code, result, _err = invoke(
                ["open", "--book", str(book), "--request", str(request), "--sources", str(sources)]
            )
        finally:
            restore_io(real_open, real_write)
        folder = book / page
        if result["result"] == "complete" or result["reason"] != "interrupted write":
            raise AssertionError(result)
        if state["calls"] < 2:
            raise AssertionError("open did not fail during the write")
        if (folder / "investigation.json").exists() or (folder / "seal.json").exists() or (folder / "checkpoints").exists():
            raise AssertionError("initial open published authority or a prior pair")
        partial = json.loads((folder / "partial.json").read_text(encoding="utf-8"))
        if partial["predecessor"] != "none":
            raise AssertionError(partial)


def test_replace_and_projection_failures() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-repl-") as tmp:
        root = Path(tmp)
        book, folder = stage_attached(root, "0723.replace")
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()

        def stop_record(_src, dest):
            if Path(dest).name == "investigation.json" and "staging" not in Path(dest).as_posix():
                raise OSError("SYNTHETIC record replace failure")

        cw.REPLACE_HOOK = stop_record
        try:
            code, body, _err = seal(book, "0723.replace", "05.01", b"x\n", "desk copy", root)
        finally:
            cw.REPLACE_HOOK = None
        assert_refused(body, folder)
        if (folder / "investigation.json").read_bytes() != before or (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("record replace failure moved the root pair")
        checkpoint = folder / "checkpoints" / cw.sha256(before)
        if (checkpoint / "investigation.json").read_bytes() != before or (checkpoint / "seal.json").read_bytes() != old_seal:
            raise AssertionError("checkpoint is not the prior pair")
        assert_blocked(book)

    with tempfile.TemporaryDirectory(prefix="0511-0505-seal-") as tmp:
        root = Path(tmp)
        book, folder = stage_attached(root, "0724.seal")
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()
        transitions_before = len(json.loads(before.decode("utf-8"))["transitions"])

        def stop_seal(_src, dest):
            if Path(dest).name == "seal.json" and Path(dest).parent == folder:
                raise OSError("SYNTHETIC seal replace failure")

        cw.REPLACE_HOOK = stop_seal
        try:
            code, body, _err = seal(book, "0724.seal", "05.01", b"y\n", "desk copy", root)
        finally:
            cw.REPLACE_HOOK = None
        assert_refused(body, folder)
        if (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("seal replace wrote the root seal")
        if (folder / "investigation.json").read_bytes() == before:
            raise AssertionError("investigation replace did not publish the candidate")
        checkpoint = folder / "checkpoints" / cw.sha256(before)
        retained = json.loads((checkpoint / "investigation.json").read_text(encoding="utf-8"))
        if len(retained["transitions"]) != transitions_before:
            raise AssertionError("checkpoint gained the failed transition")
        if json.loads((checkpoint / "seal.json").read_text(encoding="utf-8"))["sha256"] != cw.sha256(before):
            raise AssertionError("checkpoint seal does not verify")
        assert_blocked(book)

    with tempfile.TemporaryDirectory(prefix="0511-0505-proj-") as tmp:
        root = Path(tmp)
        book, folder, saved = prepare_second(root, "0725.proj")
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()
        pointer = (folder / "08.md").read_bytes()
        real_open, real_write, state = install_midwrite(projection_pointer)
        try:
            code, body, _err = seal(book, "0725.proj", "05.02", b"second\n", "desk copy", root)
        finally:
            restore_io(real_open, real_write)
        assert_refused(body, folder)
        if state["calls"] < 2:
            raise AssertionError("projection write was not partial")
        if (folder / "08.md").read_bytes() != pointer:
            raise AssertionError("live projection changed during a staged write")
        if (folder / "investigation.json").read_bytes() != before or (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("projection failure moved the root pair")
        for name, data in saved.items():
            path = folder / "artifacts/05.01/return.md" if name == "artifact" else None
            if name == "pack":
                path = folder / "artifacts/05.01/package/05.01.pack.md"
            elif name == "review":
                path = folder / "06.01.review.md"
            elif name == "projection":
                path = folder / "05.01.return.md"
            if path.read_bytes() != data:
                raise AssertionError(name)


def test_second_pass_midwrite() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-two-") as tmp:
        root = Path(tmp)
        book, folder, saved = prepare_second(root, "0726.two")
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()
        real_open, real_write, state = install_midwrite(staging_record)
        try:
            code, body, _err = seal(book, "0726.two", "05.02", b"second\n", "desk copy", root)
        finally:
            restore_io(real_open, real_write)
        assert_refused(body, folder)
        if state["calls"] < 2:
            raise AssertionError("second pass record write was not partial")
        if (folder / "investigation.json").read_bytes() != before or (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("second pass mid-write changed the root pair")
        checkpoint = folder / "checkpoints" / cw.sha256(before)
        if (checkpoint / "investigation.json").read_bytes() != before:
            raise AssertionError("checkpoint does not hold the sealed prior record")
        retained = json.loads((checkpoint / "investigation.json").read_text(encoding="utf-8"))
        if retained["passes"]["05.02"]["return"] is not None:
            raise AssertionError("failed seal is visible in the retained record")
        for name, data in saved.items():
            if name == "artifact":
                path = folder / "artifacts/05.01/return.md"
            elif name == "pack":
                path = folder / "artifacts/05.01/package/05.01.pack.md"
            elif name == "review":
                path = folder / "06.01.review.md"
            else:
                path = folder / "05.01.return.md"
            if path.read_bytes() != data:
                raise AssertionError(name)
        (folder / "partial.json").unlink()
        code, shown, _err = invoke(["show", "--book", str(book)])
        if shown["pages"][0]["partial"] is not True:
            raise AssertionError("attempt.json alone did not keep the page partial")
        code, later, _err = invoke(
            ["seal-return-local", "--book", str(book), "--page", "0726.two", "--pass", "05.02", "--return-file", str(root / "return-05.02.bin"), "--declared-transport", "desk copy"]
        )
        if later["reason"] != "resume refused" or later["wrote"] is not False:
            raise AssertionError(later)


def test_collision_replay_and_bytes() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-keep-") as tmp:
        root = Path(tmp)
        book = open_page(root, "0727.keep")
        folder = book / "0727.keep"
        if (folder / "checkpoints").exists() or (folder / "attempt.json").exists():
            raise AssertionError("initial open retained a predecessor")
        publication = next((folder / "publications").glob("*.json"))
        opened = json.loads(publication.read_text(encoding="utf-8"))
        if opened["predecessor"] != "none" or opened["retained_checkpoint"] is not None:
            raise AssertionError(opened)
        if not publication.with_suffix(".published").exists() and not (folder / "publications" / (publication.stem + ".published")).exists():
            raise AssertionError("open has no published marker")
        config = root / "config.json"
        write_config(config)
        output = mini_output(root, "0727.keep", "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
        current = cw.sha256((folder / "investigation.json").read_bytes())
        planted = folder / "checkpoints" / current
        planted.mkdir(parents=True)
        (planted / "planted").write_bytes(b"do not overwrite\n")
        code, body, _err = attach(book, "0727.keep", "05.01", output, config, DIGEST)
        if body["reason"] != "checkpoint collision" or body["wrote"] is not False or (folder / "partial.json").exists():
            raise AssertionError(body)
        if (planted / "planted").read_bytes() != b"do not overwrite\n":
            raise AssertionError("collision overwrote the checkpoint")
        if cw.sha256((folder / "investigation.json").read_bytes()) != current:
            raise AssertionError("collision changed authority")
        shutil_rm = planted
        for child in list(planted.iterdir()):
            child.unlink()
        shutil_rm.rmdir()
        code, body, _err = attach(book, "0727.keep", "05.01", output, config, DIGEST)
        if code != 0:
            raise AssertionError(body)
        payload = b"exact-lf\n"
        code, body, _err = seal(book, "0727.keep", "05.01", payload, "desk copy", root)
        if code != 0 or (folder / "05.01.return.md").read_bytes() != payload:
            raise AssertionError(body)
        if (folder / "artifacts/05.01/return.md").read_bytes() != payload:
            raise AssertionError("artifact bytes differ")
        checkpoints = [item.name for item in (folder / "checkpoints").iterdir()]
        code, body, _err = seal(book, "0727.keep", "05.01", payload, "desk copy", root)
        if body["result"] != "repeat" or body["wrote"] is not False:
            raise AssertionError(body)
        if sorted(item.name for item in (folder / "checkpoints").iterdir()) != sorted(checkpoints):
            raise AssertionError("replay added a checkpoint")
        code, body, _err = seal(book, "0727.keep", "05.01", payload, "other label", root)
        if body["reason"] != "declared transport differs" or body["wrote"] is not False:
            raise AssertionError(body)
        if (folder / "05.01.return.md").read_bytes() != payload:
            raise AssertionError("transport refusal rewrote the return")
        crlf = b"exact\r\nreturn\r\n"
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0727.keep", "--pass", "05.02"])
        if body["reason"] != "next pass not requested":
            raise AssertionError(body)
        asking = root / "ask.json"
        asking.write_bytes(cw.canonical(review_body("request-next", "05.02")))
        code, body, _err = invoke(
            ["record-review", "--book", str(book), "--page", "0727.keep", "--pass", "05.01", "--review", str(asking)]
        )
        if code != 0:
            raise AssertionError(body)
        before_count = len(json.loads((folder / "investigation.json").read_text(encoding="utf-8"))["transitions"])
        code, body, _err = invoke(["open-pass", "--book", str(book), "--page", "0727.keep", "--pass", "05.02"])
        if code != 0 or body["result"] != "complete":
            raise AssertionError(body)
        after = json.loads((folder / "investigation.json").read_text(encoding="utf-8"))
        if len(after["transitions"]) != before_count + 1 or after["transitions"][-1]["action"] != "open-pass":
            raise AssertionError(after["transitions"])
        output_b = mini_output(root, "0727.keep", "05.02", b"# Pack two\n", b"# Notes two\n", DIGEST_B)
        code, body, _err = attach(book, "0727.keep", "05.02", output_b, config, DIGEST_B)
        if code != 0:
            raise AssertionError(body)
        code, body, _err = seal(book, "0727.keep", "05.02", crlf, "desk copy", root)
        if code != 0 or (folder / "artifacts/05.02/return.md").read_bytes() != crlf:
            raise AssertionError(body)
        if b"\r\n" not in (folder / "05.02.return.md").read_bytes():
            raise AssertionError("CRLF return was normalized")
        decoy = folder / "checkpoints" / ("f" * 64)
        decoy.mkdir()
        (decoy / "investigation.json").write_bytes(b"{\"title\":\"not authority\"}\n")
        code, shown, _err = invoke(["show", "--book", str(book)])
        if shown["wrote"] is not False or shown["pages"][0]["partial"] is not False:
            raise AssertionError(shown)
        if shown["pages"][0]["passes"][0]["return_kind"] != "page-local":
            raise AssertionError(shown["pages"][0]["passes"])
        loaded = json.loads((folder / "investigation.json").read_text(encoding="utf-8"))
        if loaded["title"] != "Exchange question":
            raise AssertionError("show selected another checkpoint")
        if (folder / "attempt.json").exists() or (folder / "partial.json").exists():
            raise AssertionError("success left an in-flight marker")


def test_legacy_live_and_links() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-old-") as tmp:
        root = Path(tmp)
        book = root / "book"
        folder = book / "0728.legacy"
        folder.mkdir(parents=True)
        data = cw.canonical({"schema": "colab-exchange-investigation/1"})
        (folder / "investigation.json").write_bytes(data)
        (folder / "seal.json").write_bytes(cw.canonical({"schema": cw.SEAL_SCHEMA, "sha256": cw.sha256(data)}))
        code, body, _err = invoke(["show", "--book", str(book)])
        if body["reason"] != "unknown schema" or body["wrote"] is not False:
            raise AssertionError(body)
    code, body, _err = invoke(["propose", "--book", r"D:\Git\lib-build\00.kernel\00.00.10.work"])
    if body["reason"] != "live work book is not a fixture":
        raise AssertionError(body)
    with tempfile.TemporaryDirectory(prefix="0511-0505-link-") as tmp:
        root = Path(tmp)
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
    with tempfile.TemporaryDirectory(prefix="0511-0505-sym-") as tmp:
        root = Path(tmp)
        book = open_page(root, "0729.sym")
        output = mini_output(root, "0729.sym", "05.01", b"# Pack\n", b"# Notes\n", DIGEST)
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
                    "0729.sym",
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
    with tempfile.TemporaryDirectory(prefix="0511-0505-pin-") as tmp:
        root = Path(tmp)
        book = open_page(root, "0730.pin")
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
                    "0730.pin",
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
        if body["reason"] != "pin mismatch" or body["wrote"] is not False:
            raise AssertionError(body)


def test_write_hook_before_staged_record() -> None:
    with tempfile.TemporaryDirectory(prefix="0511-0505-hook-") as tmp:
        root = Path(tmp)
        book, folder = stage_attached(root, "0728.hook")
        before = (folder / "investigation.json").read_bytes()
        old_seal = (folder / "seal.json").read_bytes()
        seen = {"calls": 0}

        def stop(path, _data):
            text = str(path).replace("\\", "/")
            if "/staging/" in text and text.endswith("/investigation.json"):
                seen["calls"] += 1
                raise OSError("SYNTHETIC write hook before staged record open")

        cw.WRITE_HOOK = stop
        try:
            _code, body, _err = seal(book, "0728.hook", "05.01", b"hook\n", "desk copy", root)
        finally:
            cw.WRITE_HOOK = None
        assert_refused(body, folder)
        if seen["calls"] != 1:
            raise AssertionError(seen)
        if (folder / "investigation.json").read_bytes() != before or (folder / "seal.json").read_bytes() != old_seal:
            raise AssertionError("write hook moved the root pair")
        checkpoint = folder / "checkpoints" / cw.sha256(before)
        if (checkpoint / "investigation.json").read_bytes() != before or (checkpoint / "seal.json").read_bytes() != old_seal:
            raise AssertionError("checkpoint is not the prior pair")
        staged = folder / "staging"
        if any(path.name == "investigation.json" for path in staged.rglob("*")):
            raise AssertionError("staged record was opened")
        assert_blocked(book)


def test_source_and_runner() -> None:
    text = (LAB / "colab_workflow.py").read_text(encoding="utf-8")
    if "handoff_check" in text:
        raise AssertionError("standalone checker is referenced")
    if 'write_bytes(page / "investigation.json"' in text or 'write_bytes(page / "seal.json"' in text:
        raise AssertionError("authority files are still truncated in place")
    for path, digest, size in (
        (PASS02, PASS02_SHA, 47247),
        (PASS03, PASS03_SHA, 68410),
    ):
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest or len(raw) != size or b"\r" in raw:
            raise AssertionError(path.name)
    seen = []

    def ok():
        seen.append("kept")
        return 0

    def bad():
        seen.append("still-here")
        return 7

    if run_suite.aggregate([ok, bad, ok]) != 1 or seen != ["kept", "still-here", "kept"]:
        raise AssertionError(seen)


def main() -> int:
    tests = [
        test_successor_midwrite_keeps_root_pair,
        test_open_midwrite_invents_nothing,
        test_replace_and_projection_failures,
        test_second_pass_midwrite,
        test_collision_replay_and_bytes,
        test_legacy_live_and_links,
        test_symlink_refusal,
        test_bad_producer_pin,
        test_write_hook_before_staged_record,
        test_source_and_runner,
    ]
    failed = []
    skipped = 0
    for test in tests:
        try:
            test()
        except Skip as exc:
            skipped += 1
            print(f"skip {test.__name__}: {exc.reason}", flush=True)
        except Exception as exc:
            failed.append(test.__name__)
            print(f"FAIL {test.__name__}: {exc}", flush=True)
        else:
            print(f"ok {test.__name__}", flush=True)
    print(f"executed {len(tests) - skipped}", flush=True)
    print(f"skipped {skipped}", flush=True)
    print(f"failed {len(failed)}", flush=True)
    if failed:
        print(f"first-failure {failed[0]}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
