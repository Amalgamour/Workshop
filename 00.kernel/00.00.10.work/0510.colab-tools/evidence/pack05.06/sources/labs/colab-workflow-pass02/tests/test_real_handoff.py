"""Disposable exchange against the accepted v2 envelope. The live book is not an argument.

Unit tests stub the producer. This file does not. It calls the pinned v2 verifier
and the accepted intake. It does not call the standalone checker.
"""

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
ENVELOPE = ROOT / "00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer-v2-05.03"
PRODUCER = ROOT / "labs/colab-support-pass02/colab_support.py"
HELPER = ROOT / "labs/return-capture-pass01/return_capture.py"
V1 = ROOT / "labs/colab-workflow-pass01/colab_workflow.py"
PY = sys.executable
DIGEST = "42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184"
PAGE = "0701.colab-exchange-layout"
PASS = "05.01"
V1_SHA = "4507760c3b374d89add77d66a02dc5df437dd7c2f4d1214e09ff309381cd2da3"
PACK_SHA = "b46713a78cea87597d04578949d21f4539518133ff58a8c007377fb222ea5a29"
NOTES_SHA = "2d7fe940fcfbd2a9b88c655ebbbd3f113c290182a18e8f875c2c10758c5349f9"
REQUEST_SHA = "5778b69507ff4eadd67e0b3eb2bdb3aa7d22440110d1ddb16e09b5e5e7c0b1fa"
BINDING_SHA = "d6bfabb615200c91009deb8631bd834c52286037aae2cfb14e5827f49a1a81b1"
SNAPSHOT_SHA = "1cff00588bde14723b7058aa3698a30eb727a3632892bb8ad7029b4d049617d9"
ZIP_SHA = "5f77b08318a40b9329f51a9178e274637271d1cf06d4aa3e9e1ea3c354862cfe"


def run(argv):
    code, out, err = cw.execute(argv)
    body = json.loads(out.decode("utf-8")) if out else None
    return code, body, err


def tool(args):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([PY, "-B", *args], capture_output=True, env=env, shell=False)
    return proc.returncode, proc.stdout, proc.stderr


def write_config(path: Path, helper: Path | None = None) -> None:
    cfg = {
        "assembler": str(ROOT / "labs/pack-assembly-pass01/pack_assembly.py"),
        "checker": str(ROOT / "labs/pack-custody-pass01/pack_check.py"),
        "helper": str(helper or HELPER),
        "inspector": str(ROOT / "labs/return-capture-pass01/return_inspect.py"),
        "producer_v1": str(ROOT / "labs/colab-support-pass01/colab_support.py"),
        "python": str(PY),
        "repositories": {"workshop": str(ROOT)},
        "schema": "colab-config/2",
    }
    path.write_bytes(cw.canonical(cfg))


def envelope_hashes() -> dict[str, str]:
    return {
        path.relative_to(ENVELOPE).as_posix(): cw.sha256(path.read_bytes())
        for path in ENVELOPE.rglob("*")
        if path.is_file()
    }


def request_bytes(page: str, binding: dict, title: str) -> bytes:
    body = {
        "book": binding["investigation"]["book"],
        "page": page,
        "pass": binding["investigation"]["pass"],
        "schema": "colab-exchange-open/1",
        "targets": binding["targets"],
        "title": title,
    }
    return cw.canonical(body)


def open_closure(book: Path, request_path: Path, closure: Path) -> tuple[int, dict]:
    book.mkdir()
    code, body, err = run(
        ["open", "--book", str(book), "--request", str(request_path), "--closure", str(closure)]
    )
    if code != 0:
        raise AssertionError(err.decode("utf-8", "replace") + str(body))
    return code, body


def attach(book: Path, output: Path, config: Path, digest: str = DIGEST):
    return run(
        [
            "attach",
            "--book",
            str(book),
            "--page",
            PAGE,
            "--pass",
            PASS,
            "--output",
            str(output),
            "--config",
            str(config),
            "--expect-digest",
            digest,
        ]
    )


def names_under(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def refuse_case(root: Path, name: str, request_path: Path, output: Path, config: Path, reason: str):
    book = root / name
    _code, _body = open_closure(book, request_path, ENVELOPE)
    code, body, _err = attach(book, output, config)
    page = book / PAGE
    if body.get("reason") != reason or (page / "artifacts").exists():
        raise AssertionError((name, body))
    return code, body


def main() -> int:
    if "handoff_check" in (LAB / "colab_workflow.py").read_text(encoding="utf-8"):
        raise AssertionError("standalone checker is referenced")
    before_v1 = cw.sha256(V1.read_bytes())
    if before_v1 != V1_SHA or len(V1.read_bytes()) != 83008:
        raise AssertionError(before_v1)
    before_envelope = envelope_hashes()
    binding = json.loads((ENVELOPE / "package/binding.json").read_text(encoding="utf-8"))
    title = json.loads((ENVELOPE / "package/colab-request.json").read_text(encoding="utf-8"))["title"]
    report = [("v1-before", 0, before_v1, len(V1.read_bytes()))]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = root / "config.json"
        write_config(config)
        happy_request = root / "open.json"
        happy_request.write_bytes(request_bytes(PAGE, binding, title))
        book = root / "happy"
        code, body = open_closure(book, happy_request, ENVELOPE)
        report.append(("open", code, body.get("result"), body.get("page")))
        door = book / "0700.band.colabs"
        door.mkdir()
        (door / "01.md").write_bytes(b"Door only. Not an investigation.\n")
        code, body, _err = attach(book, ENVELOPE, config)
        report.append(("attach", code, body.get("result"), body.get("digest")))
        if code != 0 or body.get("digest") != DIGEST:
            raise AssertionError(body)
        page = book / PAGE
        stored = page / "artifacts" / PASS
        pack = (page / "05.01.pack.md").read_bytes()
        notes = (stored / "package/06.01.notes.md").read_bytes()
        wanted = {
            "package/05.01.pack.md": (PACK_SHA, 3584),
            "package/06.01.notes.md": (NOTES_SHA, 2552),
            "package/colab-request.json": (REQUEST_SHA, 6270),
            "package/binding.json": (BINDING_SHA, 642),
            "package/snapshots/0001.blob": (SNAPSHOT_SHA, 3776),
            "prepared-colab.zip": (ZIP_SHA, 43099),
        }
        for rel, (digest, size) in wanted.items():
            data = (stored / rel).read_bytes()
            if data != (ENVELOPE / rel).read_bytes() or cw.sha256(data) != digest or len(data) != size:
                raise AssertionError(rel)
            report.append(("stored", 0, rel, digest))
        if (stored / "verification.json").read_bytes() != (ENVELOPE / "verification.json").read_bytes():
            raise AssertionError("verification bytes")
        projected = (page / "06.01.notes.md").read_bytes()
        if cw.launch_slice(projected) != notes or cw.sha256(notes) != NOTES_SHA:
            raise AssertionError("launch snapshot")
        provenance = (stored / "provenance.json").read_bytes()
        if b"colab-config" in provenance or str(config).encode("utf-8") in provenance or b":\\" in provenance:
            raise AssertionError("config leaked")
        listing = names_under(page)
        banned = ("handoff.json", "assembler-request.json", "assembler-run.json", "07.md")
        if any(name.endswith(banned) or "/evaluator/" in name or name.startswith("evaluator/") for name in listing):
            raise AssertionError(listing)
        if any(part.endswith(".colab") for name in listing for part in name.split("/")):
            raise AssertionError(listing)
        template = (stored / "package/templates/05.01.return.TEMPLATE.md").read_bytes()
        review_template = (stored / "package/templates/06.01.review.TEMPLATE.md").read_bytes()
        if b"THIS IS A TEMPLATE" not in template or b"THIS IS A TEMPLATE" not in review_template:
            raise AssertionError("template marker")
        if (page / "05.01.return.md").exists() or (page / "06.01.review.md").exists():
            raise AssertionError("early exchange")
        code, body, _err = attach(book, ENVELOPE, config)
        report.append(("repeat", code, body.get("result"), body.get("wrote")))
        if body.get("result") != "repeat" or body.get("wrote") is not False:
            raise AssertionError(body)
        code, body, _err = run(
            [
                "append-note",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                PASS,
                "--text",
                "Working line kept apart from the snapshot.",
            ]
        )
        report.append(("note", code, body.get("result"), body.get("wrote")))
        if code != 0 or (stored / "package/06.01.notes.md").read_bytes() != notes:
            raise AssertionError(body)
        if cw.launch_slice((page / "06.01.notes.md").read_bytes()) != notes:
            raise AssertionError("snapshot changed")
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        if record["passes"][PASS]["package"]["digest"] != DIGEST:
            raise AssertionError("digest changed")
        code, shown, _err = run(["show", "--book", str(book)])
        report.append(("show", code, shown.get("wrote"), None))
        if shown.get("wrote") is not False or (book / "00.live.md").exists():
            raise AssertionError(shown)
        code, body, _err = attach(book, ENVELOPE, config, "0" * 64)
        report.append(("wrong-digest", code, body.get("reason"), body.get("wrote")))
        if body.get("reason") != "stale expected hash" or body.get("wrote") is not False:
            raise AssertionError(body)
        other = root / "origin"
        other.mkdir()
        source_root = root / "sources"
        relative = binding["targets"][0]["source"]["path"]
        source_file = source_root.joinpath(*relative.split("/"))
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.write_bytes((ENVELOPE / "package/snapshots/0001.blob").read_bytes())
        other_request = root / "other.json"
        other_request.write_bytes(request_bytes("0702.other-question", binding, title))
        code, body, _err = run(
            ["open", "--book", str(other), "--request", str(other_request), "--sources", str(source_root)]
        )
        if code != 0:
            raise AssertionError(body)
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(other),
                "--page",
                "0702.other-question",
                "--pass",
                PASS,
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("wrong-origin", code, body.get("reason"), (other / "0702.other-question" / "artifacts").exists()))
        if body.get("reason") != "wrong origin":
            raise AssertionError(body)

        def copied(name: str) -> Path:
            dest = root / name
            shutil.copytree(ENVELOPE, dest)
            return dest

        hc01 = copied("hc01")
        handoff = hc01 / "handoff.json"
        raw = handoff.read_text(encoding="utf-8")
        needle = (
            '\n  "investigation": {\n    "book": "00.00.10.work",\n'
            '    "page": "0701.colab-exchange-layout",\n    "pass": "05.01"\n  }'
        )
        if raw.count(needle) != 1:
            raise AssertionError("handoff investigation shape")
        handoff.write_text(
            raw.replace(needle, needle.replace("0701.colab-exchange-layout", "0799.wrong-investigation"), 1),
            encoding="utf-8",
            newline="\n",
        )
        code, body = refuse_case(root, "book-hc01", happy_request, hc01, config, "conflicting bytes")
        report.append(("hc01", code, body.get("reason"), "0799.wrong-investigation"))
        tampered = copied("tampered")
        blob = tampered / "package/snapshots/0001.blob"
        blob.write_bytes(blob.read_bytes() + b"\n")
        code, body = refuse_case(root, "book-tamper", happy_request, tampered, config, "conflicting bytes")
        report.append(("tampered", code, body.get("reason"), None))
        missing = copied("missing")
        (missing / "verification.json").unlink()
        code, body = refuse_case(root, "book-missing", happy_request, missing, config, "malformed package")
        report.append(("missing-verification", code, body.get("reason"), None))
        extra = copied("extra")
        (extra / "package/EXTRA.md").write_bytes(b"extra\n")
        code, body = refuse_case(root, "book-extra", happy_request, extra, config, "conflicting bytes")
        report.append(("extra", code, body.get("reason"), None))
        leaked = copied("evaluator")
        (leaked / "evaluator").mkdir()
        (leaked / "evaluator/secret.md").write_bytes(b"EVALUATOR-SECRET-NOT-FOR-PACKAGE\n")
        code, body = refuse_case(root, "book-evaluator", happy_request, leaked, config, "conflicting bytes")
        report.append(("evaluator", code, body.get("reason"), None))
        if b"EVALUATOR-SECRET-NOT-FOR-PACKAGE" in b"".join(path.read_bytes() for path in page.rglob("*") if path.is_file()):
            raise AssertionError("evaluator leaked")
        producer = root / "bad-producer.py"
        original = PRODUCER.read_bytes()
        producer.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))

        def boom(argv):
            raise AssertionError("launched")

        cw.RUN_PROCESS = boom
        try:
            pin_book = root / "pin"
            _code, _body = open_closure(pin_book, happy_request, ENVELOPE)
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(pin_book),
                    "--page",
                    PAGE,
                    "--pass",
                    PASS,
                    "--output",
                    str(ENVELOPE),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                    "--producer",
                    str(producer),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        report.append(("bad-producer", code, body.get("reason"), body.get("wrote")))
        if body.get("reason") != "pin mismatch":
            raise AssertionError(body)
        helper = root / "bad-helper.py"
        helper_bytes = HELPER.read_bytes()
        helper.write_bytes(helper_bytes[:-1] + bytes([helper_bytes[-1] ^ 1]))
        bad_config = root / "bad-config.json"
        write_config(bad_config, helper)
        cw.RUN_PROCESS = boom
        try:
            helper_book = root / "helper"
            _code, _body = open_closure(helper_book, happy_request, ENVELOPE)
            code, body, _err = attach(helper_book, ENVELOPE, bad_config)
        finally:
            cw.RUN_PROCESS = None
        report.append(("bad-helper", code, body.get("reason"), body.get("wrote")))
        if body.get("reason") != "pin mismatch":
            raise AssertionError(body)

        def hook(path, _data):
            if "artifacts" in str(path):
                raise RuntimeError("stop")

        interrupt_book = root / "interrupt"
        _code, _body = open_closure(interrupt_book, happy_request, ENVELOPE)
        kept = (interrupt_book / PAGE / "investigation.json").read_bytes()
        cw.WRITE_HOOK = hook
        try:
            code, body, _err = attach(interrupt_book, ENVELOPE, config)
        finally:
            cw.WRITE_HOOK = None
        report.append(("interrupt", code, body.get("reason"), body.get("wrote")))
        partial_page = interrupt_book / PAGE
        if body.get("reason") != "interrupted write" or body.get("wrote") is not True or not (partial_page / "partial.json").exists():
            raise AssertionError(body)
        cw.RUN_PROCESS = boom
        try:
            code, body, _err = attach(interrupt_book, ENVELOPE, config)
        finally:
            cw.RUN_PROCESS = None
        report.append(("resume", code, body.get("reason"), None))
        if body.get("reason") != "resume refused" or (partial_page / "investigation.json").read_bytes() != kept:
            raise AssertionError(body)
        code, reserve_out, reserve_err = tool(
            [
                str(HELPER),
                "reserve",
                "--book",
                str(book),
                "--submission",
                "fixture-exchange-0503",
                "--name",
                "colab-fixture-0501",
                "--origin-book",
                "00.00.10.work",
                "--origin-page",
                PAGE,
                "--origin-batch",
                PASS,
                "--expected-output",
                "note.md",
                "--submitter",
                "synthetic fixture",
                "--reviewer",
                "Codex Prime",
                "--release",
                "Reservation only",
            ]
        )
        if code != 0:
            raise AssertionError(reserve_err.decode("utf-8", "replace"))
        member = next(item.name for item in book.iterdir() if item.name.endswith(".colab-fixture-0501"))
        report.append(("reserve", code, member, "reserved"))
        returned = "\n".join(
            [
                "# Synthetic fixture response",
                "",
                "This file is a labelled fixture. It is not a model result.",
                "",
                "## Answer",
                "The exchange files stay separate in this fixture.",
                "",
                "Do not manufacture a number.",
                "",
            ]
        ).encode("utf-8")
        response = root / "synthetic-return.md"
        response.write_bytes(returned)
        (root / "note.md").write_bytes(b"labelled fixture artifact\n")
        code, intake_out, intake_err = tool(
            [
                str(PRODUCER),
                "intake",
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--book",
                str(book),
                "--member",
                member,
                "--return-file",
                str(response),
                "--source-root",
                str(root),
                "--artifact",
                "note.md|note.md",
                "--json",
            ]
        )
        intake = json.loads(intake_out.decode("utf-8")) if intake_out else {}
        report.append(("intake", code, intake.get("result"), None))
        if code != 0 or intake.get("result") != "captured" or (book / member / "return.md").read_bytes() != returned:
            raise AssertionError(intake_out.decode("utf-8", "replace") + intake_err.decode("utf-8", "replace"))
        code, body, _err = run(
            [
                "place-return",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                PASS,
                "--member",
                member,
                "--config",
                str(config),
            ]
        )
        report.append(("place", code, body.get("result"), body.get("member")))
        if code != 0 or (page / "05.01.return.md").read_bytes() != returned:
            raise AssertionError(body)
        if (page / "artifacts" / PASS / "return.md").read_bytes() != returned:
            raise AssertionError("stored return")
        pointer = (page / "08.md").read_text(encoding="utf-8")
        if member not in pointer or returned.decode("utf-8") in pointer:
            raise AssertionError(pointer)
        review = {
            "assessment": "Supplied fixture assessment. The tool does not judge it.",
            "by": "Codex Prime",
            "findings": [
                {
                    "consequential": True,
                    "director_reply": "hypothetical-fixture: Keep the return bytes exact.",
                    "disposition": "held",
                    "id": "F01",
                    "observation": "A reader could mistake notes for a review.",
                    "pending": True,
                    "reason": "Prime supplied this disposition.",
                    "source_binding": "T01",
                }
            ],
            "next_pass": None,
            "on": "2026-10-29",
            "pending_questions": ["Does the note stay distinct from the review?"],
            "route": "hold",
            "schema": "colab-exchange-review/1",
        }
        review_path = root / "review.json"
        review_path.write_bytes(cw.canonical(review))
        code, body, _err = run(
            ["record-review", "--book", str(book), "--page", PAGE, "--pass", PASS, "--review", str(review_path)]
        )
        report.append(("review", code, body.get("result"), body.get("route")))
        if code != 0 or (page / "05.01.return.md").read_bytes() != returned:
            raise AssertionError(body)
        rendered = (page / "06.01.review.md").read_text(encoding="utf-8")
        if "hypothetical-fixture: Keep the return bytes exact." not in rendered or "F01" not in rendered or "held" not in rendered:
            raise AssertionError(rendered)
        if "So this is how I see the flow" in rendered:
            raise AssertionError("invented a Director quote")
        if (page / "05.02.pack.md").exists():
            raise AssertionError("next pack")
        _code, shown, _err = run(["show", "--book", str(book)])
        flags = next(item for item in shown["pages"] if item["page"] == PAGE)["passes"][0]
        report.append(
            (
                "held-show",
                0,
                shown.get("wrote"),
                f"route={flags['route']};explicit_finish={flags['explicit_finish']};review_pending={flags['review_pending']};held={flags['held']}",
            )
        )
        if shown.get("wrote") is not False or flags["explicit_finish"] or not flags["review_pending"] or not flags["held"]:
            raise AssertionError(flags)
        if flags["route"] != "hold" or (book / "00.live.md").exists():
            raise AssertionError(flags)
        if (door / "01.md").read_bytes() != b"Door only. Not an investigation.\n":
            raise AssertionError("door changed")
        report.append(("return-bytes", 0, cw.sha256(returned), len(returned)))
    if envelope_hashes() != before_envelope:
        raise AssertionError("envelope changed")
    after_v1 = cw.sha256(V1.read_bytes())
    report.append(("v1-after", 0, after_v1, after_v1 == before_v1))
    report.append(("envelope", 0, "unchanged", True))
    if after_v1 != before_v1:
        raise AssertionError(after_v1)
    for step, code, result, extra in report:
        print(f"{step} exit {code} result {result} extra {extra}")
    print("handoff exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
