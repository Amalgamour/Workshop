"""Disposable handoff against the accepted producer envelope. No live book write."""

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
ENVELOPE = ROOT / "00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer05.02"
PRODUCER = ROOT / "labs/colab-support-pass01/colab_support.py"
HELPER = ROOT / "labs/return-capture-pass01/return_capture.py"
PY = sys.executable
DIGEST = "a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4"
PAGE = "0701.colab-compute-ops"


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
        "helper": str(helper or (ROOT / "labs/return-capture-pass01/return_capture.py")),
        "inspector": str(ROOT / "labs/return-capture-pass01/return_inspect.py"),
        "python": str(PY),
        "repositories": {"workshop": str(ROOT)},
        "schema": "colab-config/1",
    }
    path.write_bytes(cw.canonical(cfg))


def one_line(value: str) -> str:
    text = " ".join(value.split())
    if not text or any(ord(ch) < 32 for ch in text):
        raise AssertionError("supplied text is not one line")
    return text


def open_request(binding: dict, packaged: dict, page: str, title: str) -> dict:
    env = packaged["environment"]
    return {
        "assumptions": [one_line(packaged["prior_involvement"])],
        "book": binding["investigation"]["book"],
        "capabilities": {
            "execute": one_line(env["execute"]),
            "network": one_line(env["network"]),
            "read": one_line(env["read"]),
            "write": one_line(env["write"]),
        },
        "challenge": one_line(" ".join(item["text"] for item in packaged["cases"])),
        "dependencies": {
            "supplied": [item["path"] for item in packaged["required_sources"]],
            "unavailable": [item["item"] for item in packaged["unavailable"]],
            "withheld": [item["item"] for item in packaged["withheld"]],
        },
        "known_gaps": [one_line(item) for item in packaged["known_gaps"]],
        "method": one_line(packaged["method"]),
        "mode": packaged["mode"],
        "page": page,
        "pass": binding["investigation"]["pass"],
        "permissions": one_line(" ".join(packaged["permissions"])),
        "purpose": one_line(packaged["why"]),
        "question": one_line(packaged["question"]),
        "reading_order": [binding["targets"][0]["source"]["path"], *[item["path"] for item in packaged["required_sources"]]],
        "reasons": [one_line(packaged["why"])],
        "return_shape": one_line(packaged["return_route"]["destination"]),
        "schema": "colab-open/1",
        "scope": one_line(packaged["context"]),
        "stop": one_line(" ".join(packaged["stop"])),
        "targets": binding["targets"],
        "title": title,
    }


def names_under(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def main() -> int:
    binding = json.loads((ENVELOPE / "package/binding.json").read_text(encoding="utf-8"))
    packaged = json.loads((ENVELOPE / "package/colab-request.json").read_text(encoding="utf-8"))
    before_envelope = {
        path.relative_to(ENVELOPE).as_posix(): cw.sha256(path.read_bytes())
        for path in ENVELOPE.rglob("*")
        if path.is_file()
    }
    report = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = root / "config.json"
        write_config(config)
        book = root / "book"
        book.mkdir()
        door = book / "0700.band.colabs"
        door.mkdir()
        (door / "01.md").write_bytes(b"Door only. Not an investigation.\n")
        request = open_request(binding, packaged, PAGE, packaged["title"])
        request_path = root / "open.json"
        request_path.write_bytes(cw.canonical(request))
        code, body, _err = run(["open", "--book", str(book), "--request", str(request_path), "--closure", str(ENVELOPE)])
        report.append(("open", code, body.get("result"), body.get("reason")))
        if code != 0:
            raise AssertionError(body)
        if "07.md" in names_under(book / PAGE):
            raise AssertionError("emitted 07")
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("attach", code, body.get("result"), body.get("digest")))
        if code != 0 or body.get("digest") != DIGEST:
            raise AssertionError(body)
        page = book / PAGE
        stored = page / "artifacts/05.01"
        for rel, digest in (
            ("package/colab-request.json", "460e8ef45e5095e1af91133a475524a727d4aa21a4d3d1d84801bc0d5e2a3e25"),
            ("package/binding.json", "e1311900743bde2274e9ceb729150673fb815d9d47320602d4de71ada1136a21"),
            ("package/snapshots/0001.blob", "1a9b2ce890e1ab4078154ed26b218cdea7bf9d6624d06ca5b1d43dfb5f29e3e0"),
            ("verification.json", "444094243dcd1c5cef418cd75e93543228167cefb7bded407715f33e82bec11d"),
            ("prepared-colab.zip", "f44c4bf1985ba893a4e09d80593438ac011cb1fe35d695a378c811ec41f44c60"),
        ):
            data = (stored / rel).read_bytes()
            if cw.sha256(data) != digest or data != (ENVELOPE / rel).read_bytes():
                raise AssertionError(rel)
        kept = names_under(stored)
        if any(name.startswith("evaluator/") or name.endswith(".colab") or name.endswith("/07.md") or name == "07.md" for name in kept):
            raise AssertionError(kept)
        if any(name in ("assembler-request.json", "assembler-run.json") for name in kept):
            raise AssertionError(kept)
        provenance = (stored / "provenance.json").read_bytes()
        if str(config).encode("utf-8") in provenance or b"colab-config" in provenance or b"EVALUATOR" in provenance:
            raise AssertionError("provenance leaked")
        page_hash = cw.sha256((page / "investigation.json").read_bytes())
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("repeat", code, body.get("result"), body.get("wrote")))
        if body.get("result") != "repeat" or body.get("wrote") is not False:
            raise AssertionError(body)
        if cw.sha256((page / "investigation.json").read_bytes()) != page_hash:
            raise AssertionError("repeat wrote")
        code, shown, _err = run(["show", "--book", str(book)])
        report.append(("show", code, shown.get("wrote"), None))
        if code != 0 or shown.get("wrote") is not False or (book / "00.live.md").exists():
            raise AssertionError(shown)
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--expect-digest",
                "0" * 64,
            ]
        )
        report.append(("wrong-digest", code, body.get("reason"), None))
        if body.get("reason") != "stale expected hash":
            raise AssertionError(body)
        other = root / "other-book"
        other.mkdir()
        sources = root / "sources"
        manifest = json.loads((ENVELOPE / "package/source-manifest.json").read_text(encoding="utf-8"))
        for row in manifest["sources"]:
            blob = (ENVELOPE / "package" / row["snapshot"]).read_bytes()
            dest = sources / row["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
        wrong_request = open_request(binding, packaged, "0702.other-question", "Wrong page probe")
        wrong_path = root / "wrong-open.json"
        wrong_path.write_bytes(cw.canonical(wrong_request))
        code, body, _err = run(["open", "--book", str(other), "--request", str(wrong_path), "--sources", str(sources)])
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
                "05.01",
                "--output",
                str(ENVELOPE),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("wrong-origin", code, body.get("reason"), None))
        if body.get("reason") != "wrong origin" or (other / "0702.other-question/artifacts").exists():
            raise AssertionError(body)
        tampered = root / "tampered"
        shutil.copytree(ENVELOPE, tampered)
        blob = tampered / "package/snapshots/0001.blob"
        blob.write_bytes(blob.read_bytes() + b"\n")
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(other),
                "--page",
                "0702.other-question",
                "--pass",
                "05.01",
                "--output",
                str(tampered),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("tampered", code, body.get("reason"), None))
        if body.get("reason") != "conflicting bytes":
            raise AssertionError(body)
        missing = root / "missing"
        shutil.copytree(ENVELOPE, missing)
        (missing / "verification.json").unlink()
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(other),
                "--page",
                "0702.other-question",
                "--pass",
                "05.01",
                "--output",
                str(missing),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("missing-envelope", code, body.get("reason"), None))
        if body.get("reason") != "malformed package":
            raise AssertionError(body)
        extra = root / "extra"
        shutil.copytree(ENVELOPE, extra)
        (extra / "package/EXTRA.md").write_bytes(b"extra\n")
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(other),
                "--page",
                "0702.other-question",
                "--pass",
                "05.01",
                "--output",
                str(extra),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("extra", code, body.get("reason"), None))
        if body.get("reason") != "conflicting bytes":
            raise AssertionError(body)
        leaked = root / "leaked"
        shutil.copytree(ENVELOPE, leaked)
        (leaked / "evaluator").mkdir()
        (leaked / "evaluator/secret.md").write_bytes(b"EVALUATOR-SECRET-NOT-FOR-PACKAGE\n")
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--output",
                str(leaked),
                "--config",
                str(config),
                "--expect-digest",
                DIGEST,
            ]
        )
        report.append(("evaluator", code, body.get("reason"), None))
        if body.get("reason") != "conflicting bytes":
            raise AssertionError(body)
        if b"EVALUATOR-SECRET-NOT-FOR-PACKAGE" in b"".join(path.read_bytes() for path in page.rglob("*") if path.is_file()):
            raise AssertionError("evaluator bytes were copied")

        def boom(_argv):
            raise AssertionError("launched")

        bad_producer = root / "bad-producer.py"
        data = PRODUCER.read_bytes()
        bad_producer.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
        cw.RUN_PROCESS = boom
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    PAGE,
                    "--pass",
                    "05.01",
                    "--output",
                    str(ENVELOPE),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                    "--producer",
                    str(bad_producer),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        report.append(("bad-producer", code, body.get("reason"), None))
        if body.get("reason") != "pin mismatch":
            raise AssertionError(body)
        bad_helper = root / "bad-helper.py"
        helper_bytes = HELPER.read_bytes()
        bad_helper.write_bytes(helper_bytes[:-1] + bytes([helper_bytes[-1] ^ 1]))
        bad_config = root / "bad-config.json"
        write_config(bad_config, bad_helper)
        cw.RUN_PROCESS = boom
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(book),
                    "--page",
                    PAGE,
                    "--pass",
                    "05.01",
                    "--output",
                    str(ENVELOPE),
                    "--config",
                    str(bad_config),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        report.append(("bad-helper", code, body.get("reason"), None))
        if body.get("reason") != "pin mismatch":
            raise AssertionError(body)

        partial_book = root / "partial-book"
        partial_book.mkdir()
        code, body, _err = run(["open", "--book", str(partial_book), "--request", str(request_path), "--closure", str(ENVELOPE)])
        if code != 0:
            raise AssertionError(body)

        def stop(path, _data):
            if "artifacts" in path.as_posix():
                raise RuntimeError("stop")

        cw.WRITE_HOOK = stop
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(partial_book),
                    "--page",
                    PAGE,
                    "--pass",
                    "05.01",
                    "--output",
                    str(ENVELOPE),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.WRITE_HOOK = None
        report.append(("interrupt", code, body.get("reason"), body.get("wrote")))
        partial_page = partial_book / PAGE
        if body.get("reason") != "interrupted write" or body.get("wrote") is not True or not (partial_page / "partial.json").exists():
            raise AssertionError(body)
        kept_partial = (partial_page / "investigation.json").read_bytes()
        cw.RUN_PROCESS = boom
        try:
            code, body, _err = run(
                [
                    "attach",
                    "--book",
                    str(partial_book),
                    "--page",
                    PAGE,
                    "--pass",
                    "05.01",
                    "--output",
                    str(ENVELOPE),
                    "--config",
                    str(config),
                    "--expect-digest",
                    DIGEST,
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        report.append(("resume", code, body.get("reason"), None))
        if body.get("reason") != "resume refused" or (partial_page / "investigation.json").read_bytes() != kept_partial:
            raise AssertionError(body)

        code, reserve_out, reserve_err = tool(
            [
                str(HELPER),
                "reserve",
                "--book",
                str(book),
                "--submission",
                "fixture-0701-0501",
                "--name",
                "colab-fixture-0501",
                "--origin-book",
                "00.00.10.work",
                "--origin-page",
                PAGE,
                "--origin-batch",
                "05.01",
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
        report.append(("reserve", code, reserve_out.decode("utf-8", "replace").strip(), None))
        if code != 0:
            raise AssertionError(reserve_err.decode("utf-8", "replace"))
        member = next(item.name for item in book.iterdir() if item.name.endswith(".colab-fixture-0501"))
        response = root / "synthetic-return.md"
        response.write_bytes(
            "\n".join(
                [
                    "# Synthetic fixture response",
                    "",
                    "This file is a labelled fixture. It is not a model result.",
                    "",
                    "## Question",
                    "Supplied question only.",
                    "",
                    "## Evidence",
                    "The packaged snapshot.",
                    "",
                    "## Hostile",
                    "A later reader may disagree.",
                    "",
                    "## Factfind",
                    "Prepare, verify and intake are built. Review and find are not.",
                    "",
                    "## Overflow",
                    "None supplied.",
                    "",
                    "## Unprompted",
                    "None supplied.",
                    "",
                    "## Qualitative result",
                    "The split remains a question for a later Colab.",
                    "",
                    "## Director replies",
                    "hypothetical-fixture: Keep review manual for now.",
                    "",
                    "Do not manufacture a number.",
                    "",
                ]
            ).encode("utf-8")
        )
        note = root / "note.md"
        note.write_bytes(b"labelled fixture artifact\n")
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
        intake = json.loads(intake_out.decode("utf-8"))
        report.append(("intake", code, intake.get("result"), None))
        if code != 0 or intake.get("result") != "captured":
            raise AssertionError(intake_out.decode("utf-8", "replace") + intake_err.decode("utf-8", "replace"))
        code, body, _err = run(
            ["return-pointer", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--member", member]
        )
        report.append(("return-pointer", code, body.get("result"), body.get("member")))
        if code != 0 or body.get("member") != member:
            raise AssertionError(body)
        findings = root / "findings.json"
        findings.write_bytes(
            cw.canonical(
                [
                    {
                        "affected_file": "01.md",
                        "affected_page": "0411.colab",
                        "consequential": True,
                        "evidence_kind": "supplied",
                        "id": "F01",
                        "observation": "Prime supplied this finding. The tool does not judge it.",
                        "target": "T01",
                        "topic": "operation split",
                    },
                    {
                        "affected_file": "01.md",
                        "affected_page": "0411.colab",
                        "consequential": False,
                        "evidence_kind": "supplied",
                        "id": "F02",
                        "observation": "Section ids stay unsupported in this slice.",
                        "target": "T01",
                        "topic": "section syntax",
                    },
                ]
            )
        )
        code, body, _err = run(
            ["record-findings", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--findings", str(findings)]
        )
        if code != 0:
            raise AssertionError(body)
        held = root / "held.json"
        held.write_bytes(
            cw.canonical(
                [
                    {
                        "action": "held",
                        "director_reply": "hypothetical-fixture: Keep review manual for now.",
                        "director_reply_ref": "D02",
                        "finding_id": "F01",
                        "followup_ref": "later-colab",
                        "park": None,
                        "reason": "Prime held the operation split for a later Colab.",
                        "reviewer": "Codex Prime",
                        "source_binding": "T01",
                    }
                ]
            )
        )
        code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--dispositions", str(held)]
        )
        if code != 0:
            raise AssertionError(body)
        review = root / "review.json"
        review.write_bytes(
            cw.canonical({"by": "Codex Prime", "kind": "review", "on": "2026-10-29", "text": "PENDING"})
        )
        code, body, _err = run(
            ["record-statement", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--statement", str(review)]
        )
        if code != 0:
            raise AssertionError(body)
        _code, shown, _err = run(["show", "--book", str(book)])
        flags = shown["index"]["investigations"][0]["passes"][0]["flags"]
        report.append(("pending", 0, flags.get("explicit_completion"), flags.get("review_pending")))
        if flags["explicit_completion"] or not flags["review_pending"] or not flags["held_followup"] or not flags["custody_complete"]:
            raise AssertionError(flags)
        both = root / "both.json"
        both.write_bytes(
            cw.canonical(
                [
                    json.loads(held.read_text(encoding="utf-8"))[0],
                    {
                        "action": "rejected",
                        "director_reply": "hypothetical-fixture: no section-id syntax is enacted.",
                        "director_reply_ref": None,
                        "finding_id": "F02",
                        "followup_ref": None,
                        "park": None,
                        "reason": "Prime refused a new section-id convention.",
                        "reviewer": "Codex Prime",
                        "source_binding": "T01",
                    },
                ]
            )
        )
        code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--dispositions", str(both)]
        )
        if code != 0:
            raise AssertionError(body)
        proposal = root / "proposal.json"
        proposal.write_bytes(
            cw.canonical(
                {
                    "affected_file": "01.md",
                    "affected_page": "0411.colab",
                    "finding_id": "F01",
                    "schema": "colab-subject-proposal/1",
                    "target": "T01",
                    "text": "A later reviewed pass may write the local why on 0411.colab. This proposal is not that write.",
                }
            )
        )
        code, body, _err = run(
            ["propose-note", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--proposal", str(proposal)]
        )
        if code != 0:
            raise AssertionError(body)
        early = root / "early.json"
        early.write_bytes(cw.canonical({"by": "Codex Prime", "explicit": False, "on": "2026-10-29", "text": "not yet"}))
        code, body, _err = run(["close", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--closure", str(early)])
        if body.get("reason") != "explicit close required":
            raise AssertionError(body)
        closure = root / "closure.json"
        closure.write_bytes(
            cw.canonical(
                {
                    "by": "Codex Prime",
                    "explicit": True,
                    "on": "2026-10-29",
                    "text": "Supplied explicit closure for this disposable investigation only.",
                }
            )
        )
        code, body, _err = run(["close", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--closure", str(closure)])
        report.append(("close", code, body.get("result"), None))
        if code != 0:
            raise AssertionError(body)
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        actions = {item["finding_id"]: item["action"] for item in record["passes"]["05.01"]["dispositions"]}
        if actions != {"F01": "held", "F02": "rejected"}:
            raise AssertionError(actions)
        _code, shown, _err = run(["show", "--book", str(book)])
        flags = shown["index"]["investigations"][0]["passes"][0]["flags"]
        report.append(("explicit", 0, flags.get("explicit_completion"), flags.get("review_pending")))
        if not flags["explicit_completion"] or not flags["review_pending"]:
            raise AssertionError(flags)
        if (door / "01.md").read_bytes() != b"Door only. Not an investigation.\n":
            raise AssertionError("door changed")
    after_envelope = {
        path.relative_to(ENVELOPE).as_posix(): cw.sha256(path.read_bytes())
        for path in ENVELOPE.rglob("*")
        if path.is_file()
    }
    if after_envelope != before_envelope:
        raise AssertionError("envelope changed")
    for step, code, result, extra in report:
        print(f"{step} exit {code} result {result} extra {extra}")
    print("handoff exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
