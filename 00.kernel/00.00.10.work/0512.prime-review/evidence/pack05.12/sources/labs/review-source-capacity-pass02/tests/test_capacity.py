#!/usr/bin/env python3
"""Lifecycle author cases for the 64-source candidate. Disposable books only.

The pass01 suite stays untouched. Revised expectations are labeled revised.
The preserved 05.10 author log is read and is not re-run.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(r"D:\Git\lib-build")
LAB = ROOT / "labs" / "review-source-capacity-pass02"
CANDIDATE = LAB / "candidate"
APP = CANDIDATE / "app" / "librarian.py"
HELPER_APP = ROOT / "app" / "librarian.py"
KEEP = Path(r"D:\librarian\temp\0512-0511-report")
LIVE = ROOT / "00.kernel" / "00.00.10.work"
PY = Path(sys.executable)
PAGE = "0599.capacity-lab"
PASS = "05.99"
JUDGMENT_0509 = LIVE / "0512.prime-review" / "evidence" / "prime-review05.09" / "core-review" / "judgment.json"
JUDGMENT_0514 = LIVE / "0522.review-construction" / "evidence" / "prime-review05.14" / "core-review" / "judgment.json"
JUDGMENT_OPEN = LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "core-review" / "judgment-open.json"
JUDGMENT_BAD = LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "core-review" / "judgment.json"
PACK = LIVE / "0512.prime-review" / "05.11.md"
PACK_0510 = LIVE / "0512.prime-review" / "05.10.md"
BODY_SHA = "a1ee0f06510bed7c4e5467e4608375c6f9eaecdec6f4adcac126d8ed16e56427"
BODY_0510 = "cd03ee24eca855c53eb5512dcfb3f7aea964c7f5289bc249fb18f25b7c4bce1c"
ACTIVE_LIBRARIAN = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
CANDIDATE_LIBRARIAN = "a4e0ec03095a43291a997fbf9e9899f89409863a3df718c7ba9e219ed63ea6bf"
HISTORICAL_PRIME = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
SUCCESSOR_SHA = "32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f"
PRIOR_SHA = "a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87"
DECLARATION_SHA = "c64a83f82331fb89d405aa93bf9707fdf913366d241c313b764d8bdcf91906cd"
STEP64 = (
    "keep every source identity on this record and stop for a versioned successor "
    "whose source bound covers the count"
)
STEP32 = "split the return so one record binds at most 32 sources"
HELD_OPEN = "a held review keeps the pass and the goal open"
UNKNOWN = (
    "agreement.goal is unknown",
    "agreement.scope is unknown",
    "agreement.prime_discretion is unknown",
    "agreement.director_required is unknown",
    "agreement.finish_criteria is unknown",
    "agreement.recorded_decisions is unknown",
)
OLD_CASES = {
    "active_surface": "revised",
    "historical_modules": "preserved",
    "naive_external_copy": "preserved",
    "historical_replay_0509": "preserved",
    "cycle_0509": "preserved",
    "cycle_0514": "preserved",
    "generated_bounds": "revised",
    "holds_stay_24": "preserved",
    "document_bound": "preserved",
    "hostile_count": "revised",
    "hostile_document": "revised",
    "duplicate_and_conflict": "preserved",
    "code_root": "preserved",
    "changed_and_missing": "preserved",
    "malformed_row": "preserved",
    "wrong_pins": "preserved",
    "lab_door": "preserved",
    "linked_pin": "preserved",
}
RESULTS: list[dict] = []
README_BYTES = (ROOT / "app" / "README.md").read_bytes()
OPEN_BYTES = JUDGMENT_OPEN.read_bytes()
BAD_BYTES = JUDGMENT_BAD.read_bytes()
RAW_JUDGMENTS = {
    str(JUDGMENT_0509): JUDGMENT_0509.read_bytes(),
    str(JUDGMENT_0514): JUDGMENT_0514.read_bytes(),
    str(JUDGMENT_OPEN): OPEN_BYTES,
    str(JUDGMENT_BAD): BAD_BYTES,
}
PACK_BYTES = PACK.read_bytes()
PACK_0510_BYTES = PACK_0510.read_bytes()
PASS01_SUCCESSOR = (ROOT / "labs" / "review-source-capacity-pass01" / "prime_review.py").read_bytes()
PASS01_TESTS = (ROOT / "labs" / "review-source-capacity-pass01" / "tests" / "test_capacity.py").read_bytes()
FROZEN_AUTHOR = (
    LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "author-suite.txt"
).read_bytes()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def refusal(count: int, limit: int, step: str) -> str:
    return f"refused: limit sources: {count} sources exceeds supported limit {limit}; {step}"


def note(name: str, **payload) -> None:
    item = {"name": str(name), "provenance": payload.pop("provenance", "author")}
    item.update(payload)
    RESULTS.append(item)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(PY), "-B", *args],
        cwd=str(cwd),
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        shell=False,
    )


def load_json(proc: subprocess.CompletedProcess) -> dict:
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def classify(page: bytes, expected_body: str) -> tuple[str, str]:
    if b"\r" in page:
        raise AssertionError("page contains CR")
    body, marker, rest = page.partition(b"\n## Return pointer\n")
    if marker != b"\n## Return pointer\n" or sha(body) != expected_body:
        raise AssertionError("task body changed")
    head, review_marker, review = rest.partition(b"## Review - Codex Prime\n")
    if review_marker != b"## Review - Codex Prime\n":
        raise AssertionError("review heading missing")
    lines = head.split(b"\n")
    while lines and lines[-1] == b"":
        lines.pop()
    if lines == [b"PENDING."]:
        pointer = "pending"
    elif (
        len(lines) == 2
        and lines[0].startswith(b"Submission: ")
        and b" sha256 " in lines[0]
        and lines[0].endswith(b" bytes.")
        and lines[1].startswith(b"Artifact manifest: ")
        and b" sha256 " in lines[1]
        and b"The manifest lists " in lines[1]
        and lines[1].endswith(b"excludes itself.")
    ):
        pointer = "filed"
    else:
        raise AssertionError("malformed return pointer")
    if review == b"PENDING.\n":
        region = "pending"
    elif review.strip() != b"":
        region = "reviewed"
    else:
        raise AssertionError("empty review region")
    return pointer, region


def page_text(pointer: str) -> bytes:
    text = (
        "Intro OUTSIDE\n\n"
        "## Goal\n"
        "Review one disposable capture.\n\n"
        "## Scope\n"
        "The disposable book only.\n\n"
        "## Prime discretion\n"
        "Prime may record a judgment inside that grant.\n\n"
        "## Director required\n"
        "A design change is not in this grant.\n\n"
        "## Finish\n"
        "- piece: The disposable note stays one file.\n\n"
        "## Director - verbatim\n"
        "Pack it up.\n\n"
        "## Return pointer\n"
        f"{pointer}"
        "## Review - Codex Prime\n"
        "PENDING.\n"
        "## Notes\n"
        "TAIL\n"
    )
    return text.encode("utf-8")


def write_book(book: Path, count: int, *, repeat: bool = False, conflict: bool = False, code: bool = False, malformed: bool = False) -> None:
    if book.exists():
        shutil.rmtree(book)
    files = []
    for index in range(count):
        rel = f"{PAGE}/evidence/a{index:02d}.txt"
        data = f"artifact {index}\n".encode("utf-8")
        path = book / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        files.append({"bytes": len(data), "path": rel, "sha256": sha(data)})
    if repeat and files:
        files.append(dict(files[0]))
    if conflict and files:
        bad = dict(files[0])
        bad["sha256"] = "0" * 64
        files.append(bad)
    if code:
        rel = "app/review-loop-v7.json"
        data = (CANDIDATE / rel).read_bytes()
        files.append({"bytes": len(data), "path": rel, "sha256": sha(data)})
    if malformed:
        files.append({"bytes": "unknown", "path": f"{PAGE}/evidence/a00.txt", "sha256": "not-a-hash"})
    submission_rel = f"{PAGE}/evidence/submission.md"
    submission = b"submission\n"
    (book / submission_rel).parent.mkdir(parents=True, exist_ok=True)
    (book / submission_rel).write_bytes(submission)
    manifest = {
        "excludes_self": True,
        "file_count": len(files),
        "files": files,
        "schema": "review-report-artifact-manifest/2",
    }
    blob = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    manifest_rel = f"{PAGE}/evidence/artifact-manifest.json"
    (book / manifest_rel).write_bytes(blob)
    pointer = (
        f"Submission: {submission_rel} sha256 {sha(submission)}, {len(submission)} bytes.\n"
        f"Artifact manifest: {manifest_rel} sha256 {sha(blob)}, {len(blob)} bytes, {len(files)} files. Excludes itself.\n"
    )
    (book / PAGE / f"{PASS}.md").write_bytes(page_text(pointer))


def copy_page(book: Path, source: str) -> None:
    if book.exists():
        shutil.rmtree(book)
    book.mkdir(parents=True)
    shutil.copytree(LIVE / source, book / source)


class SurfaceError(AssertionError):
    pass


class CapacityAuthor(unittest.TestCase):
    def command(self, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        args = [str(APP), "review-loop", command, "--book", str(book), "--source", source, "--pass", pass_id]
        for key, value in flags.items():
            args.extend(["--" + key.replace("_", "-"), value])
        proc = run(args, CANDIDATE)
        return proc, load_json(proc)

    def replay(self, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        return self._replay(LAB / "historical_replay.py", book, command, source, pass_id, **flags)

    def prior(self, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        return self._replay(LAB / "predecessor_replay.py", book, command, source, pass_id, **flags)

    def _replay(self, script: Path, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        args = [str(script), str(CANDIDATE), command, "--book", str(book), "--source", source, "--pass", pass_id]
        for key, value in flags.items():
            args.extend(["--" + key.replace("_", "-"), value])
        proc = run(args, CANDIDATE)
        return proc, load_json(proc)

    def record_generated(self, name: str, count: int, entry: str) -> tuple[Path, dict, subprocess.CompletedProcess]:
        book = KEEP / "books" / name
        write_book(book, count)
        callers = {"candidate": self.command, "historical": self.replay, "predecessor": self.prior}
        caller = callers[entry]
        proc, prepared = caller(book, "prepare", PAGE, PASS)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[:500])
        self.assertEqual(prepared.get("measurement"), "complete", prepared.get("findings"))
        recorded, payload = caller(
            book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509),
        )
        return book, payload, recorded

    def test_author_active_surface_stays(self) -> None:
        librarian = HELPER_APP.read_bytes()
        self.assertEqual(sha(librarian), ACTIVE_LIBRARIAN)
        self.assertEqual(len(librarian), 12204)
        self.assertIn(b"review_loop_tools_v7.py", librarian)
        self.assertNotIn(b"review_loop_tools_source_capacity", librarian)
        self.assertEqual((ROOT / "app" / "README.md").read_bytes(), README_BYTES)
        pointer, region = classify(PACK.read_bytes(), BODY_SHA)
        self.assertIn(pointer, {"pending", "filed"})
        self.assertIn(region, {"pending", "reviewed"})
        page = PACK.read_bytes()
        self.assertIn(b"state: PREPARED; execute on Director handoff; versioned candidate only", page)
        filed_pointer, filed_region = classify(self.synthetic(PACK.read_bytes(), "filed", "pending"), BODY_SHA)
        self.assertEqual((filed_pointer, filed_region), ("filed", "pending"))
        reviewed_pointer, reviewed_region = classify(self.synthetic(PACK.read_bytes(), "filed", "reviewed"), BODY_SHA)
        self.assertEqual((reviewed_pointer, reviewed_region), ("filed", "reviewed"))
        pending_pointer, pending_region = classify(self.synthetic(PACK.read_bytes(), "pending", "pending"), BODY_SHA)
        self.assertEqual((pending_pointer, pending_region), ("pending", "pending"))
        with self.assertRaises(AssertionError):
            classify(self.synthetic(PACK.read_bytes(), "malformed", "pending"), BODY_SHA)
        mutated = bytearray(PACK.read_bytes())
        mutated[20] = mutated[20] ^ 1
        with self.assertRaises(AssertionError):
            classify(bytes(mutated), BODY_SHA)
        prior_pointer, _prior_region = classify(PACK_0510.read_bytes(), BODY_0510)
        self.assertEqual(prior_pointer, "filed")
        self.assertEqual(PACK_0510.read_bytes(), PACK_0510_BYTES)
        note("active-surface", expectation="revised", pointer=pointer, review=region, librarian_sha256=sha(librarian), readme_sha256=sha(README_BYTES))

    def synthetic(self, page: bytes, pointer_kind: str, review_kind: str) -> bytes:
        body, _marker, _rest = page.partition(b"\n## Return pointer\n")
        if pointer_kind == "pending":
            pointer = b"PENDING.\n"
        elif pointer_kind == "filed":
            pointer = (
                b"Submission: evidence/build05.11/submission.md sha256 " + (b"a" * 64) + b", 10 bytes.\n"
                b"Artifact manifest: evidence/build05.11/artifact-manifest.json sha256 " + (b"b" * 64)
                + b", 20 bytes. The manifest lists 1 files and excludes itself.\n"
            )
        else:
            pointer = b"FILED.\n"
        review = b"PENDING.\n" if review_kind == "pending" else b"Prime review recorded the successor as unselected.\n"
        return body + b"\n## Return pointer\n" + pointer + b"\n## Review - Codex Prime\n" + review

    def test_author_limits_answers_stay_24(self) -> None:
        book = KEEP / "books" / "bound-24-new"
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        prime["answers"] = [{} for _ in range(25)]
        prime["holds"] = []
        path = KEEP / "books" / "answers-25.json"
        path.write_bytes((json.dumps(prime) + "\n").encode("utf-8"))
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--root", str(book), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: limit answers", proc.stderr)
        self.assertNotIn(b"64", proc.stderr)
        self.assertNotIn(b"limit sources", proc.stderr)
        note("answers-stay-24", expectation="preserved", provenance="author")

    def test_author_case_reconciliation(self) -> None:
        self.assertEqual(len(OLD_CASES), 18)
        revised = sorted(name for name, kind in OLD_CASES.items() if kind == "revised")
        preserved = sorted(name for name, kind in OLD_CASES.items() if kind == "preserved")
        self.assertEqual(revised, ["active_surface", "generated_bounds", "hostile_count", "hostile_document"])
        self.assertEqual(len(preserved), 14)
        self.assertEqual(len(revised) + len(preserved), 18)
        note("case-reconciliation", expectation="revised", revised=revised, preserved_count=len(preserved), unchanged_18=False)

    def test_author_changed_and_missing(self) -> None:
        book = KEEP / "books" / "changed-before"
        write_book(book, 1)
        proc, prepared = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(prepared.get("measurement"), "complete")
        target = book / PAGE / "evidence" / "a00.txt"
        target.write_bytes(b"changed\n")
        recorded, payload = self.command(book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 2)
        self.assertFalse(payload.get("recorded"))
        self.assertIn("incomplete", payload.get("correction", ""))
        viewed, again = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(viewed.returncode, 0)
        codes = [item.get("code") for item in again.get("findings", []) if isinstance(item, dict)]
        self.assertIn("artifact-hash-mismatch", codes)
        missing = KEEP / "books" / "missing-before"
        write_book(missing, 1)
        proc, prepared = self.command(missing, "prepare", PAGE, PASS)
        (missing / PAGE / "evidence" / "a00.txt").unlink()
        recorded, payload = self.command(missing, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 2)
        self.assertIn("incomplete", payload.get("correction", ""))
        self.assertFalse(payload.get("recorded"))
        viewed, again = self.command(missing, "prepare", PAGE, PASS)
        codes = [item.get("code") for item in again.get("findings", []) if isinstance(item, dict)]
        self.assertIn("artifact-missing", codes)
        stored = KEEP / "books" / "changed-after"
        write_book(stored, 1)
        proc, prepared = self.command(stored, "prepare", PAGE, PASS)
        recorded, payload = self.command(stored, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 0, payload.get("correction"))
        finding = payload["judgment"]["finding"]
        (stored / PAGE / "evidence" / "a00.txt").write_bytes(b"later\n")
        read_proc, read_payload = self.command(stored, "read", PAGE, PASS)
        self.assertEqual(read_proc.returncode, 1)
        self.assertTrue(read_payload.get("stale"))
        self.assertEqual(read_payload["judgment"]["finding"], finding)
        (stored / PAGE / "evidence" / "a00.txt").unlink()
        read_proc, read_payload = self.command(stored, "read", PAGE, PASS)
        self.assertEqual(read_proc.returncode, 1)
        self.assertEqual(read_payload["judgment"]["finding"], finding)
        note("changed-and-missing", expectation="preserved")

    def test_author_code_root_is_excluded(self) -> None:
        book = KEEP / "books" / "code-root"
        write_book(book, 1, code=True)
        proc, prepared = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(prepared.get("measurement"), "complete", prepared.get("findings"))
        rows = prepared["form"]["bindings"]["rows"]
        code_rows = [row for row in rows if row.get("root") == "code"]
        self.assertEqual(len(code_rows), 1)
        self.assertEqual(code_rows[0]["path"], "app/review-loop-v7.json")
        recorded, payload = self.command(book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 0, payload.get("correction"))
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        self.assertNotIn("app/review-loop-v7.json", [item["logical_path"] for item in prime["sources"]])
        note("code-root-excluded", expectation="preserved", emitted=len(prime["sources"]))

    def assert_cycle(self, folder: str, source: str, pass_id: str, judgment_path: Path, sources: int, document_bytes: int, *, bad: Path | None = None, extra_attention: tuple[str, ...] = ()) -> None:
        book = KEEP / "books" / f"author-{folder}"
        copy_page(book, source)
        proc, prepared = self.command(book, "prepare", source, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[:400])
        self.assertEqual(prepared.get("measurement"), "complete")
        form, _form_payload = self.command(book, "form", source, pass_id)
        self.assertEqual(form.returncode, 0, form.stderr)
        page = book / source / f"{pass_id}.md"
        before = page.read_bytes()
        marker = b"## Review - Codex Prime\n"
        self.assertIn(marker, before)
        prefix = before[: before.index(marker) + len(marker)]
        suffix = before[before.index(marker) + len(marker):]
        occupied = b"workbook-review-id:" in suffix
        if bad is not None:
            refused, refusal_body = self.command(
                book, "record", source, pass_id, intake=prepared["intake_id"], judgment=str(bad),
            )
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(refusal_body.get("correction"), HELD_OPEN)
            self.assertFalse(refusal_body.get("recorded"))
            self.assertEqual(bad.read_bytes(), BAD_BYTES)
            invalid_dir = KEEP / "author-cycles" / folder
            invalid_dir.mkdir(parents=True, exist_ok=True)
            (invalid_dir / "record-invalid.stdout").write_bytes(refused.stdout.replace(b"\r\n", b"\n"))
        recorded, payload = self.command(
            book, "record", source, pass_id, intake=prepared["intake_id"], judgment=str(judgment_path),
        )
        self.assertEqual(recorded.returncode, 0, payload.get("correction") or recorded.stderr)
        self.assertTrue(payload.get("recorded"))
        self.assertEqual(payload.get("mode"), "preliminary")
        self.assertEqual(payload.get("custody"), "missing")
        self.assertFalse(payload["cycle"]["called"])
        self.assertFalse(payload["cycle"]["committed"])
        for key in ("accepted", "approved", "closes_work", "published_work", "releases_action", "eligible_for_custody_completion"):
            self.assertFalse(payload.get(key))
        self.assertEqual(payload.get("authority"), "none")
        self.assertEqual(payload.get("task_association"), "not-established")
        supplied = json.loads(judgment_path.read_text(encoding="utf-8"))
        self.assertEqual(canonical(payload["judgment"]), canonical(supplied))
        self.assertEqual(judgment_path.read_bytes(), RAW_JUDGMENTS[str(judgment_path)])
        self.assertEqual(payload["next_action"], supplied["next_action"])
        for item in (*UNKNOWN, *extra_attention):
            self.assertIn(item, payload.get("attention"))
        prime_path = book / "workbook-review" / "tmp" / "prime-input.json"
        prime = json.loads(prime_path.read_text(encoding="utf-8"))
        self.assertEqual(len(prime["sources"]), sources)
        self.assertEqual(prime_path.stat().st_size, document_bytes)
        self.assertEqual(len({item["logical_path"] for item in prime["sources"]}), sources)
        inspected, view = self.command(book, "inspect", source, pass_id)
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertEqual(view.get("mode"), "preliminary")
        self.assertEqual(view["judgment"]["finding"], supplied["finding"])
        rendered = view.get("rendered")
        self.assertIsInstance(rendered, str)
        self.assertIn(supplied["finding"], rendered)
        self.assertIn(supplied["next_action"], rendered)
        read_proc, read_payload = self.command(book, "read", source, pass_id)
        self.assertEqual(read_proc.returncode, 0, read_payload.get("correction"))
        self.assertEqual(read_payload["judgment"]["finding"], supplied["finding"])
        self.assertEqual(read_payload.get("custody"), "missing")
        published, pub = self.command(book, "publish", source, pass_id, review=payload["review_id"])
        self.assertFalse(pub.get("published_work"))
        self.assertEqual(pub["next_action"], supplied["next_action"])
        after = page.read_bytes()
        self.assertTrue(after.startswith(prefix))
        if occupied:
            self.assertEqual(published.returncode, 1)
            self.assertEqual(pub.get("correction"), "stale-own-review")
            self.assertFalse(pub.get("published"))
            self.assertEqual(after, before)
            expected_state = "not-published"
        else:
            self.assertEqual(published.returncode, 0, pub.get("correction") or published.stderr)
            self.assertTrue(pub.get("published"))
            self.assertIn(b"workbook-review-id: " + payload["review_id"].encode("ascii"), after)
            expected_state = "section-verified"
        reread, reread_payload = self.command(book, "read", source, pass_id)
        self.assertEqual(reread.returncode, 0, reread_payload.get("correction"))
        self.assertEqual(reread_payload["judgment"]["finding"], supplied["finding"])
        again, recovered = self.command(book, "recover", source, pass_id)
        self.assertEqual(again.returncode, 0, recovered.get("correction"))
        self.assertEqual(recovered["judgment"]["finding"], supplied["finding"])
        self.assertEqual(recovered["next_action"], supplied["next_action"])
        self.assertEqual(recovered.get("custody"), "missing")
        self.assertEqual(recovered.get("target_state"), expected_state)
        label = folder
        folder_path = KEEP / "author-cycles" / label
        folder_path.mkdir(parents=True, exist_ok=True)
        (folder_path / "record.stdout").write_bytes(recorded.stdout.replace(b"\r\n", b"\n"))
        (folder_path / "publish.stdout").write_bytes(published.stdout.replace(b"\r\n", b"\n"))
        (folder_path / "read-after-publish.stdout").write_bytes(reread.stdout.replace(b"\r\n", b"\n"))
        (folder_path / "recover.stdout").write_bytes(again.stdout.replace(b"\r\n", b"\n"))
        (folder_path / "rendered.md").write_bytes(rendered.encode("utf-8"))
        note(label, expectation="preserved" if folder != "cycle-0510" else "new", sources=sources, document_bytes=document_bytes, review_id=payload["review_id"], mode="preliminary", custody="missing", publish=pub.get("correction") or "published")

    def test_author_cycle_0509(self) -> None:
        self.assert_cycle("cycle-0509", "0512.prime-review", "05.09", JUDGMENT_0509, 29, 125955)

    def test_author_cycle_0510(self) -> None:
        book = KEEP / "books" / "author-cycle-0510"
        copy_page(book, "0512.prime-review")
        proc, prepared = self.command(book, "prepare", "0512.prime-review", "05.10")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[:400])
        self.assertEqual(prepared.get("measurement"), "complete")
        form, _form_payload = self.command(book, "form", "0512.prime-review", "05.10")
        self.assertEqual(form.returncode, 0, form.stderr)
        page = book / "0512.prime-review" / "05.10.md"
        before = page.read_bytes()
        refused, refusal_body = self.command(
            book, "record", "0512.prime-review", "05.10",
            intake=prepared["intake_id"], judgment=str(JUDGMENT_BAD),
        )
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(refusal_body.get("correction"), HELD_OPEN)
        self.assertFalse(refusal_body.get("recorded"))
        self.assertEqual(JUDGMENT_BAD.read_bytes(), BAD_BYTES)
        recorded, payload = self.command(
            book, "record", "0512.prime-review", "05.10",
            intake=prepared["intake_id"], judgment=str(JUDGMENT_OPEN),
        )
        self.assertEqual(recorded.returncode, 2)
        self.assertFalse(payload.get("recorded"))
        self.assertFalse(payload.get("published_work"))
        prime_path = book / "workbook-review" / "tmp" / "prime-input.json"
        prime = json.loads(prime_path.read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(len(paths), 44)
        self.assertEqual(len(set(paths)), 44)
        self.assertIn("0512.prime-review/05.10.md", paths)
        self.assertIn("0512.prime-review/evidence/build05.10/submission.md", paths)
        self.assertEqual(prime_path.stat().st_size, 137328)
        self.assertLess(prime_path.stat().st_size, 262144)
        index = next(i for i, item in enumerate(prime["sources"]) if item["logical_path"].endswith("hostile/over-document.json"))
        self.assertEqual(index, 24)
        self.assertEqual(prime["sources"][index]["content_bytes"], 276423)
        self.assertIsNone(prime["sources"][index]["record"])
        self.assertEqual(payload.get("correction"), f"refused: limit sources[{index}].content_bytes")
        self.assertEqual(page.read_bytes(), before)
        self.assertEqual(JUDGMENT_OPEN.read_bytes(), OPEN_BYTES)
        folder = KEEP / "author-cycles" / "cycle-0510"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "record-invalid.stdout").write_bytes(refused.stdout.replace(b"\r\n", b"\n"))
        (folder / "record.stdout").write_bytes(recorded.stdout.replace(b"\r\n", b"\n"))
        note(
            "cycle-0510",
            expectation="blocked-by-preserved-content-bytes",
            sources=44,
            document_bytes=137328,
            content_bytes=276423,
            correction=payload.get("correction"),
            recorded=False,
        )

    def test_author_cycle_0514(self) -> None:
        self.assert_cycle("cycle-0514", "0522.review-construction", "05.14", JUDGMENT_0514, 20, 62200)

    def test_author_document_bound(self) -> None:
        source = {
            "bind": False,
            "content_bytes": 1,
            "content_sha256": "a" * 64,
            "identity": {"schema": "supplied-text/1", "label": "SUPPLIED"},
            "kind": "supplied-text",
            "logical_path": "0599.capacity-lab/evidence/a00.txt",
            "prior_content_sha256": None,
            "prior_transport_sha256": None,
            "record": "x" * 12000,
            "transport_bytes": 1,
            "transport_sha256": "a" * 64,
        }
        document = {
            "agreement": {},
            "answers": [],
            "attribution": {"actor_label": "Codex Prime (supplied)", "evidence": "label", "role": "prime"},
            "gaps": [],
            "holds": [],
            "judgment": {},
            "review_passes": [],
            "schema": "prime-review-record/1",
            "sources": [dict(source, logical_path=f"0599.capacity-lab/evidence/a{index:02d}.txt") for index in range(22)],
        }
        blob = (json.dumps(document, indent=2) + "\n").encode("utf-8")
        self.assertLessEqual(len(document["sources"]), 64)
        self.assertGreater(len(blob), 262144)
        path = KEEP / "books" / "over-document.json"
        path.write_bytes(blob)
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: input: input exceeds 262144 bytes", proc.stderr)
        self.assertNotIn(b"limit sources", proc.stderr)
        note("document-bound", expectation="preserved", bytes=len(blob), sources=22)

    def test_author_duplicate_and_conflict(self) -> None:
        book = KEEP / "books" / "duplicate-same"
        write_book(book, 2, repeat=True)
        proc, prepared = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(prepared.get("measurement"), "complete", prepared.get("findings"))
        recorded, payload = self.command(book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 0, payload.get("correction"))
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(paths.count(f"{PAGE}/evidence/a00.txt"), 1)
        conflict = KEEP / "books" / "duplicate-conflict"
        write_book(conflict, 2, conflict=True)
        refused, body = self.command(conflict, "prepare", PAGE, PASS)
        self.assertEqual(refused.returncode, 0)
        self.assertEqual(body.get("measurement"), "incomplete")
        recorded, payload = self.command(
            conflict, "record", PAGE, PASS, intake=body["intake_id"], judgment=str(JUDGMENT_0509),
        )
        self.assertEqual(recorded.returncode, 2)
        self.assertIn("incomplete", payload.get("correction", ""))
        self.assertFalse(payload.get("recorded"))
        note("duplicate-and-conflict", expectation="preserved")

    def test_author_generated_bounds(self) -> None:
        _book, old24, proc24 = self.record_generated("bound-24-old", 22, "historical")
        self.assertEqual(proc24.returncode, 0, old24.get("correction"))
        self.assertEqual(old24.get("recorded"), True)
        _book, old25, proc25 = self.record_generated("bound-25-old", 23, "historical")
        self.assertEqual(proc25.returncode, 2)
        self.assertEqual(old25.get("correction"), "refused: limit sources")
        book24, new24, newproc = self.record_generated("bound-24-new", 22, "candidate")
        self.assertEqual(newproc.returncode, 0, new24.get("correction"))
        prime = book24 / "workbook-review" / "tmp" / "prime-input.json"
        historical = CANDIDATE / "labs" / "prime-review-pass02" / "prime_review.py"
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        left = run([str(historical), "report", "--input", str(prime), "--root", str(book24), "--json"], CANDIDATE)
        right = run([str(successor), "report", "--input", str(prime), "--root", str(book24), "--json"], CANDIDATE)
        self.assertEqual(left.returncode, 0, left.stderr)
        self.assertEqual(right.returncode, 0, right.stderr)
        self.assertEqual(load_json(left)["sources"], load_json(right)["sources"])
        self.assertEqual(load_json(left)["finding"], load_json(right)["finding"])
        self.assertEqual(load_json(left)["next_action"], load_json(right)["next_action"])
        _book, new25, proc = self.record_generated("bound-25-new", 23, "candidate")
        self.assertEqual(proc.returncode, 0, new25.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-25-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 25)
        _book, prior32, prior_proc = self.record_generated("bound-32-prior", 30, "predecessor")
        self.assertEqual(prior_proc.returncode, 0, prior32.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-32-prior" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 32)
        _book, prior33, prior33_proc = self.record_generated("bound-33-prior", 31, "predecessor")
        self.assertEqual(prior33_proc.returncode, 2)
        self.assertEqual(prior33.get("correction"), refusal(33, 32, STEP32))
        self.assertFalse(prior33.get("recorded"))
        _book, new32, proc32 = self.record_generated("bound-32-new", 30, "candidate")
        self.assertEqual(proc32.returncode, 0, new32.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-32-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 32)
        _book, new33, proc33 = self.record_generated("bound-33-new", 31, "candidate")
        self.assertEqual(proc33.returncode, 0, new33.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-33-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 33)
        _book, new64, proc64 = self.record_generated("bound-64-new", 62, "candidate")
        self.assertEqual(proc64.returncode, 0, new64.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-64-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 64)
        _book, new65, proc65 = self.record_generated("bound-65-new", 63, "candidate")
        self.assertEqual(proc65.returncode, 2)
        self.assertEqual(new65.get("correction"), refusal(65, 64, STEP64))
        self.assertFalse(new65.get("recorded"))
        stored = json.loads((KEEP / "books" / "bound-65-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        self.assertEqual(len(stored["sources"]), 65)
        pending = (KEEP / "books" / "bound-65-new" / PAGE / f"{PASS}.md").read_text(encoding="utf-8")
        self.assertIn("## Review - Codex Prime\nPENDING.\n", pending)
        text = (CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py").read_text(encoding="utf-8")
        self.assertIn("MAX_SOURCES = 64", text)
        self.assertNotIn("MAX_LIST =", text)
        self.assertIn("keep every source identity on this record and stop for a versioned successor ", text)
        self.assertIn("whose source bound covers the count", text)
        self.assertNotIn(STEP32, text)
        note("generated-bounds", expectation="revised", old_24=True, old_25="limit sources", prior_32=32, prior_33=33, new_33=33, new_64=64, new_65=65)

    def test_author_historical_modules_stay(self) -> None:
        expected = {
            "labs/prime-review-pass02/prime_review.py": (HISTORICAL_PRIME, 58560),
            "labs/workbook-review-pass03/workbook.py": ("9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c", 19533),
            "labs/workbook-review-pass02/workbook.py": ("6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a", 52574),
            "labs/workbook-review-pass01/workbook.py": ("60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a", 79131),
            "app/review_loop_tools_v7.py": ("93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d", 10291),
            "app/review-loop-v7.json": ("bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8", 3515),
            "labs/review-source-capacity-pass01/prime_review.py": (PRIOR_SHA, 2031),
        }
        for rel, (digest, size) in expected.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual((sha(data), len(data)), (digest, size), rel)
            copied = (CANDIDATE / rel).read_bytes()
            self.assertEqual(copied, data, rel)
        successor = (CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py").read_bytes()
        self.assertEqual((sha(successor), len(successor)), (SUCCESSOR_SHA, 2160))
        librarian = (CANDIDATE / "app" / "librarian.py").read_bytes()
        self.assertEqual((sha(librarian), len(librarian)), (CANDIDATE_LIBRARIAN, 12246))
        self.assertIn(b"to the pinned source-capacity-64 door.", librarian)
        self.assertNotIn(b"to the pinned v7 door.", librarian)
        declaration_bytes = (CANDIDATE / "app" / "review-loop-source-capacity-v2.json").read_bytes()
        self.assertEqual((sha(declaration_bytes), len(declaration_bytes)), (DECLARATION_SHA, 4753))
        declaration = json.loads(declaration_bytes.decode("utf-8"))
        self.assertEqual(declaration["schema"], "review-loop-source-capacity/2")
        self.assertEqual(declaration["tools"]["workbook"]["path"], "labs/review-source-capacity-pass02/workbook.py")
        self.assertEqual(declaration["tools"]["prime_review_pass02"]["sha256"], HISTORICAL_PRIME)
        self.assertEqual(declaration["tools"]["prime_review_capacity"]["sha256"], SUCCESSOR_SHA)
        self.assertEqual(declaration["tools"]["capacity_pass01"]["sha256"], PRIOR_SHA)
        self.assertEqual(declaration["tools"]["candidate_app"]["sha256"], CANDIDATE_LIBRARIAN)
        self.assertNotEqual(declaration["tools"]["prime_review_capacity"]["sha256"], HISTORICAL_PRIME)
        self.assertFalse((CANDIDATE / "00.kernel").exists())
        self.assertNotEqual(CANDIDATE.resolve(), ROOT.resolve())
        note("historical-modules", expectation="preserved")

    def test_author_historical_replay_refuses_0509(self) -> None:
        book = KEEP / "books" / "pin-book"
        book.mkdir(parents=True, exist_ok=True)
        helper = run(
            [str(LAB / "historical_replay.py"), str(ROOT), "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS],
            CANDIDATE,
        )
        self.assertEqual(helper.returncode, 2)
        self.assertIn(b"historical replay root is the helper checkout", helper.stderr)
        decoy = KEEP / "roots" / "with-book"
        (decoy / "00.kernel" / "00.00.10.work").mkdir(parents=True, exist_ok=True)
        mixed = run(
            [str(LAB / "historical_replay.py"), str(decoy), "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS],
            CANDIDATE,
        )
        self.assertEqual(mixed.returncode, 2)
        self.assertIn(b"historical replay root contains the work book", mixed.stderr)
        page_book = KEEP / "books" / "author-hist-0509"
        copy_page(page_book, "0512.prime-review")
        proc, prepared = self.replay(page_book, "prepare", "0512.prime-review", "05.09")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(prepared.get("measurement"), "complete")
        recorded, payload = self.replay(
            page_book, "record", "0512.prime-review", "05.09",
            intake=prepared["intake_id"], judgment=str(JUDGMENT_0509),
        )
        self.assertEqual(recorded.returncode, 2)
        self.assertEqual(payload.get("correction"), "refused: limit sources")
        self.assertFalse(payload.get("recorded"))
        self.assertEqual(recorded.stderr, b"")
        folder = KEEP / "author-cycles" / "historical-0509"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "record.stdout").write_bytes(recorded.stdout.replace(b"\r\n", b"\n"))
        note("historical-replay-0509", expectation="preserved", provenance="known-reproduction", correction=payload.get("correction"))

    def test_author_holds_stay_24(self) -> None:
        book = KEEP / "books" / "bound-24-new"
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        prime["holds"] = [{} for _ in range(25)]
        path = KEEP / "books" / "holds-25.json"
        path.write_bytes((json.dumps(prime) + "\n").encode("utf-8"))
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--root", str(book), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: limit holds", proc.stderr)
        self.assertNotIn(b"64", proc.stderr)
        note("holds-stay-24", expectation="preserved")

    def test_author_hostile_count_is_not_trimmed(self) -> None:
        sources = [{"logical_path": f"p{index}"} for index in range(65)]
        document = {
            "agreement": {},
            "answers": [],
            "attribution": {},
            "gaps": [],
            "holds": [],
            "judgment": {},
            "review_passes": [],
            "schema": "prime-review-record/1",
            "sources": sources,
        }
        path = KEEP / "books" / "hostile-65.json"
        raw = (json.dumps(document) + "\n").encode("utf-8")
        path.write_bytes(raw)
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        text = proc.stderr.decode("utf-8")
        self.assertIn("65 sources exceeds supported limit 64", text)
        self.assertNotIn("split the return", text)
        self.assertNotIn("discard", text)
        self.assertEqual(path.read_bytes(), raw)
        self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))["sources"]), 65)
        note("hostile-count", expectation="revised", provenance="author-hostile")

    def test_author_hostile_document_bound_stays(self) -> None:
        source = {
            "bind": False,
            "content_bytes": 1,
            "content_sha256": "a" * 64,
            "identity": {"schema": "supplied-text/1", "label": "SUPPLIED"},
            "kind": "supplied-text",
            "logical_path": "0599.capacity-lab/evidence/a00.txt",
            "prior_content_sha256": None,
            "prior_transport_sha256": None,
            "record": "x" * 12000,
            "transport_bytes": 1,
            "transport_sha256": "a" * 64,
        }
        document = {
            "agreement": {},
            "answers": [],
            "attribution": {"actor_label": "Codex Prime (supplied)", "evidence": "label", "role": "prime"},
            "gaps": [],
            "holds": [],
            "judgment": {},
            "review_passes": [],
            "schema": "prime-review-record/1",
            "sources": [dict(source, logical_path=f"0599.capacity-lab/evidence/a{index:02d}.txt") for index in range(40)],
        }
        blob = (json.dumps(document, indent=2) + "\n").encode("utf-8")
        self.assertLessEqual(len(document["sources"]), 64)
        self.assertGreater(len(document["sources"]), 32)
        self.assertGreater(len(blob), 262144)
        path = KEEP / "books" / "hostile-over-document.json"
        path.write_bytes(blob)
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: input: input exceeds 262144 bytes", proc.stderr)
        self.assertNotIn(b"limit sources", proc.stderr)
        self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))["sources"]), 40)
        note("hostile-document", expectation="revised", provenance="author-hostile", bytes=len(blob), sources=40)

    def test_author_known_pending_failure_stays_recorded(self) -> None:
        text = FROZEN_AUTHOR.decode("utf-8")
        self.assertIn("FAIL: test_author_active_surface_stays", text)
        self.assertIn("PENDING", text)
        self.assertIn("Ran 18 tests in 43.148s", text)
        self.assertIn("FAILED (failures=1)", text)
        self.assertEqual(
            (LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "author-suite.txt").read_bytes(),
            FROZEN_AUTHOR,
        )
        note("known-pending-failure", expectation="known-failure", provenance="known-reproduction")

    def test_author_lab_door_is_not_an_install(self) -> None:
        book = KEEP / "books" / "pin-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run(
            [str(LAB / "review_loop_tools_source_capacity_v2.py"), "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS],
            LAB,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"review loop declaration is missing", proc.stderr)
        self.assertEqual(proc.stdout, b"")
        note("lab-door-not-install", expectation="preserved")

    def test_author_linked_candidate_pin(self) -> None:
        dest = KEEP / "books" / "linked-candidate"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(CANDIDATE, dest, ignore=shutil.ignore_patterns("__pycache__"))
        labs = dest / "labs"
        moved = dest / "labs-real"
        if moved.exists():
            shutil.rmtree(moved)
        labs.rename(moved)
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(labs), str(moved)], capture_output=True, shell=False)
        self.assertEqual(made.returncode, 0, made.stderr)
        try:
            book = KEEP / "books" / "pin-book"
            book.mkdir(parents=True, exist_ok=True)
            proc = run(
                [str(dest / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS],
                dest,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn(b"tool path is linked and was not followed", proc.stderr)
        finally:
            subprocess.run(["cmd", "/c", "rmdir", str(labs)], capture_output=True, shell=False)
        note("linked-pin", expectation="preserved")

    def test_author_malformed_row_and_unknown_size(self) -> None:
        book = KEEP / "books" / "malformed-row"
        write_book(book, 1, malformed=True)
        proc, prepared = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(prepared.get("measurement"), "incomplete")
        recorded, payload = self.command(book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_0509))
        self.assertEqual(recorded.returncode, 2)
        self.assertFalse(payload.get("recorded"))
        prime = json.loads((KEEP / "books" / "bound-24-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        prime["sources"][0]["content_bytes"] = "unknown"
        path = KEEP / "books" / "unknown-size.json"
        path.write_bytes((json.dumps(prime) + "\n").encode("utf-8"))
        successor = CANDIDATE / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--root", str(KEEP / "books" / "bound-24-new"), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"bad type sources[0].content_bytes", proc.stderr)
        note("malformed-and-unknown-size", expectation="preserved")

    def test_author_naive_external_copy_is_ambiguous(self) -> None:
        stdout = (LIVE / "0512.prime-review" / "evidence" / "build05.10" / "known-reproductions" / "record.stdout").read_bytes()
        self.assertIn(b"The artifact measurement is incomplete. The judgment was not recorded.", stdout)
        self.assertNotIn(b"limit sources", stdout)
        prepare = (LIVE / "0512.prime-review" / "evidence" / "build05.10" / "known-reproductions" / "prepare.stdout").read_text(encoding="utf-8")
        self.assertIn("ambiguous-declared-root", prepare)
        note("naive-external-copy", expectation="preserved", provenance="known-reproduction")

    def test_author_predecessor_refuses_0510(self) -> None:
        book = KEEP / "books" / "author-prior-0510"
        copy_page(book, "0512.prime-review")
        proc, prepared = self.prior(book, "prepare", "0512.prime-review", "05.10")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[:400])
        self.assertEqual(prepared.get("measurement"), "complete")
        recorded, payload = self.prior(
            book, "record", "0512.prime-review", "05.10",
            intake=prepared["intake_id"], judgment=str(JUDGMENT_OPEN),
        )
        self.assertEqual(recorded.returncode, 2)
        self.assertEqual(payload.get("correction"), refusal(44, 32, STEP32))
        self.assertFalse(payload.get("recorded"))
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(len(paths), 44)
        self.assertEqual(len(set(paths)), 44)
        folder = KEEP / "author-cycles" / "predecessor-0510"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "record.stdout").write_bytes(recorded.stdout.replace(b"\r\n", b"\n"))
        note("predecessor-0510", expectation="revised", provenance="known-reproduction", sources=44, correction=payload.get("correction"))

    def test_author_semantic_versus_raw(self) -> None:
        opened = json.loads(OPEN_BYTES)
        rejected = json.loads(BAD_BYTES)
        self.assertEqual(opened["disposition"], "correction-required")
        self.assertEqual(opened["pass_terminal"], "open")
        self.assertEqual(opened["goal_terminal"], "open")
        self.assertEqual(rejected["disposition"], "correction-required")
        self.assertEqual(rejected["pass_terminal"], "finished")
        self.assertNotEqual(canonical(opened), canonical(rejected))
        self.assertNotEqual(sha(OPEN_BYTES), sha(BAD_BYTES))
        book = KEEP / "books" / "semantic-raw"
        write_book(book, 1)
        proc, prepared = self.command(book, "prepare", PAGE, PASS)
        self.assertEqual(prepared.get("measurement"), "complete")
        refused, body = self.command(
            book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_BAD),
        )
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(body.get("correction"), HELD_OPEN)
        self.assertFalse(body.get("recorded"))
        self.assertEqual(JUDGMENT_BAD.read_bytes(), BAD_BYTES)
        recorded, payload = self.command(
            book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(JUDGMENT_OPEN),
        )
        self.assertEqual(recorded.returncode, 0, payload.get("correction"))
        self.assertEqual(canonical(payload["judgment"]), canonical(opened))
        self.assertEqual(JUDGMENT_OPEN.read_bytes(), OPEN_BYTES)
        variant = KEEP / "books" / "judgment-open-variant.json"
        variant.write_bytes((json.dumps(opened, indent=4, sort_keys=True) + "\n").encode("utf-8"))
        self.assertNotEqual(sha(variant.read_bytes()), sha(OPEN_BYTES))
        self.assertEqual(canonical(json.loads(variant.read_text(encoding="utf-8"))), canonical(opened))
        again, second = self.command(
            book, "record", PAGE, PASS, intake=prepared["intake_id"], judgment=str(variant),
        )
        self.assertEqual(again.returncode, 0, second.get("correction"))
        self.assertTrue(second.get("already_recorded"))
        self.assertEqual(canonical(second["judgment"]), canonical(opened))
        self.assertEqual(JUDGMENT_OPEN.read_bytes(), OPEN_BYTES)
        note("semantic-versus-raw", expectation="new", already_recorded=True)

    def test_author_wrong_pins(self) -> None:
        book = KEEP / "books" / "pin-book"
        book.mkdir(parents=True, exist_ok=True)
        tampered = KEEP / "books" / "tampered-successor"
        if tampered.exists():
            shutil.rmtree(tampered)
        shutil.copytree(CANDIDATE, tampered, ignore=shutil.ignore_patterns("__pycache__"))
        target = tampered / "labs" / "review-source-capacity-pass02" / "prime_review.py"
        data = bytearray(target.read_bytes())
        data[-1] = data[-1] ^ 1
        target.write_bytes(data)
        proc = run([str(tampered / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], tampered)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pinned tool hash does not match: labs/review-source-capacity-pass02/prime_review.py", proc.stderr)
        transitive = KEEP / "books" / "tampered-pass02"
        if transitive.exists():
            shutil.rmtree(transitive)
        shutil.copytree(CANDIDATE, transitive, ignore=shutil.ignore_patterns("__pycache__"))
        workbook = transitive / "labs" / "workbook-review-pass02" / "workbook.py"
        blob = bytearray(workbook.read_bytes())
        blob[-1] = blob[-1] ^ 1
        workbook.write_bytes(blob)
        proc = run([str(transitive / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], transitive)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pass02 pin mismatch", proc.stderr)
        runtime = KEEP / "books" / "tampered-runtime"
        if runtime.exists():
            shutil.rmtree(runtime)
        shutil.copytree(CANDIDATE, runtime, ignore=shutil.ignore_patterns("__pycache__"))
        prime = runtime / "labs" / "prime-review-pass02" / "prime_review.py"
        raw = bytearray(prime.read_bytes())
        raw[-1] = raw[-1] ^ 1
        prime.write_bytes(raw)
        proc = run([str(runtime / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], runtime)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pinned tool hash does not match: labs/prime-review-pass02/prime_review.py", proc.stderr)
        declared = KEEP / "books" / "tampered-declaration"
        if declared.exists():
            shutil.rmtree(declared)
        shutil.copytree(CANDIDATE, declared, ignore=shutil.ignore_patterns("__pycache__"))
        declaration = json.loads((declared / "app" / "review-loop-source-capacity-v2.json").read_text(encoding="utf-8"))
        declaration["tools"]["candidate_app"]["sha256"] = "0" * 64
        (declared / "app" / "review-loop-source-capacity-v2.json").write_bytes(
            (json.dumps(declaration, indent=2, sort_keys=True) + "\n").encode("utf-8")
        )
        proc = run([str(declared / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], declared)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pinned tool hash does not match: app/librarian.py", proc.stderr)
        broken = KEEP / "books" / "tampered-declaration-json"
        if broken.exists():
            shutil.rmtree(broken)
        shutil.copytree(CANDIDATE, broken, ignore=shutil.ignore_patterns("__pycache__"))
        (broken / "app" / "review-loop-source-capacity-v2.json").write_bytes(b"{")
        proc = run([str(broken / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], broken)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"review loop declaration is not strict json", proc.stderr)
        note("wrong-pins", expectation="preserved")

    def test_author_z_no_live_write(self) -> None:
        self.assertFalse((LIVE / "0512.prime-review" / "workbook-review").exists())
        self.assertFalse((LIVE / "0522.review-construction" / "workbook-review").exists())
        self.assertEqual(HELPER_APP.read_bytes(), (ROOT / "app" / "librarian.py").read_bytes())
        self.assertEqual(sha(HELPER_APP.read_bytes()), ACTIVE_LIBRARIAN)
        self.assertEqual((ROOT / "app" / "README.md").read_bytes(), README_BYTES)
        self.assertEqual((ROOT / "labs" / "review-source-capacity-pass01" / "prime_review.py").read_bytes(), PASS01_SUCCESSOR)
        self.assertEqual((ROOT / "labs" / "review-source-capacity-pass01" / "tests" / "test_capacity.py").read_bytes(), PASS01_TESTS)
        self.assertEqual(PACK_0510.read_bytes(), PACK_0510_BYTES)
        self.assertEqual(JUDGMENT_OPEN.read_bytes(), OPEN_BYTES)
        self.assertEqual(JUDGMENT_BAD.read_bytes(), BAD_BYTES)
        for path, raw in RAW_JUDGMENTS.items():
            self.assertEqual(Path(path).read_bytes(), raw)
        body, marker, _rest = PACK.read_bytes().partition(b"\n## Return pointer\n")
        self.assertEqual(marker, b"\n## Return pointer\n")
        self.assertEqual(sha(body), BODY_SHA)
        start_body, _start_marker, _start_rest = PACK_BYTES.partition(b"\n## Return pointer\n")
        self.assertEqual(body, start_body)
        note("no-live-write", expectation="new")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CapacityAuthor)
    stream_path = KEEP / "author-suite-last.txt"
    KEEP.mkdir(parents=True, exist_ok=True)
    with stream_path.open("w", encoding="utf-8", newline="\n") as handle:
        result = unittest.TextTestRunner(stream=handle, verbosity=2).run(suite)
    payload = (json.dumps(RESULTS, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (KEEP / "author-results.json").write_bytes(payload)
    text = stream_path.read_bytes().replace(b"\r\n", b"\n")
    stream_path.write_bytes(text)
    first = KEEP / "author-suite-first.txt"
    if not first.exists():
        first.write_bytes(text)
    print(stream_path.read_text(encoding="utf-8"))
    sys.exit(0 if result.wasSuccessful() else 1)
