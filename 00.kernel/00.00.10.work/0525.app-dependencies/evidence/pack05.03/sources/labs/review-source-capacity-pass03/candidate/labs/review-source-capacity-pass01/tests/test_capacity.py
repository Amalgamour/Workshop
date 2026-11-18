#!/usr/bin/env python3
"""Author cases for the source-capacity candidate. Disposable books only."""

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
LAB = ROOT / "labs" / "review-source-capacity-pass01"
CANDIDATE = LAB / "candidate"
APP = CANDIDATE / "app" / "librarian.py"
HELPER_APP = ROOT / "app" / "librarian.py"
KEEP = Path(r"D:\librarian\temp\0512-0510-report")
LIVE = ROOT / "00.kernel" / "00.00.10.work"
PY = Path(sys.executable)
PAGE = "0599.capacity-lab"
PASS = "05.99"
JUDGMENT_0509 = LIVE / "0512.prime-review" / "evidence" / "prime-review05.09" / "core-review" / "judgment.json"
JUDGMENT_0514 = LIVE / "0522.review-construction" / "evidence" / "prime-review05.14" / "core-review" / "judgment.json"
PACK = LIVE / "0512.prime-review" / "05.10.md"
BODY_SHA = "cd03ee24eca855c53eb5512dcfb3f7aea964c7f5289bc249fb18f25b7c4bce1c"
ACTIVE_LIBRARIAN = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
HISTORICAL_PRIME = "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"
RESULTS: list[dict] = []
README_BYTES = (ROOT / "app" / "README.md").read_bytes()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


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


class CapacityAuthor(unittest.TestCase):
    def command(self, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        args = [str(APP), "review-loop", command, "--book", str(book), "--source", source, "--pass", pass_id]
        for key, value in flags.items():
            args.extend(["--" + key.replace("_", "-"), value])
        proc = run(args, CANDIDATE)
        return proc, load_json(proc)

    def replay(self, book: Path, command: str, source: str, pass_id: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
        args = [str(LAB / "historical_replay.py"), str(CANDIDATE), command, "--book", str(book), "--source", source, "--pass", pass_id]
        for key, value in flags.items():
            args.extend(["--" + key.replace("_", "-"), value])
        proc = run(args, CANDIDATE)
        return proc, load_json(proc)

    def record_generated(self, name: str, count: int, entry: str) -> tuple[Path, dict, subprocess.CompletedProcess]:
        book = KEEP / "books" / name
        write_book(book, count)
        caller = self.command if entry == "candidate" else self.replay
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
        self.assertNotIn(b"review_loop_tools_source_capacity.py", librarian)
        self.assertEqual((ROOT / "app" / "README.md").read_bytes(), README_BYTES)
        page = PACK.read_bytes()
        self.assertNotIn(b"\r", page)
        body, marker, rest = page.partition(b"\n## Return pointer\n")
        self.assertEqual(marker, b"\n## Return pointer\n")
        self.assertEqual(sha(body), BODY_SHA)
        self.assertTrue(rest.startswith(b"PENDING.\n"))
        self.assertIn(b"state: PREPARED; execute on Director handoff; candidate only", page)
        self.assertTrue(rest.endswith(b"## Review - Codex Prime\nPENDING.\n"))
        sample = b"\n## Return pointer\nSubmission: evidence/build05.10/submission.md sha256 " + (b"a" * 64) + b", 10 bytes.\nArtifact manifest: evidence/build05.10/artifact-manifest.json sha256 " + (b"b" * 64) + b", 10 bytes. The manifest lists 1 files and excludes itself.\n## Review - Codex Prime\nPENDING.\n"
        synthetic = body + sample
        _, _, filled = synthetic.partition(b"\n## Return pointer\n")
        self.assertTrue(filled.startswith(b"Submission: "))
        self.assertIn(b"Artifact manifest: ", filled)
        self.assertTrue(filled.endswith(b"## Review - Codex Prime\nPENDING.\n"))
        note("active-surface", librarian_sha256=sha(librarian), readme_sha256=sha(README_BYTES))

    def test_author_historical_modules_stay(self) -> None:
        expected = {
            "labs/prime-review-pass02/prime_review.py": (HISTORICAL_PRIME, 58560),
            "labs/workbook-review-pass03/workbook.py": ("9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c", 19533),
            "labs/workbook-review-pass02/workbook.py": ("6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a", 52574),
            "labs/workbook-review-pass01/workbook.py": ("60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a", 79131),
            "app/review_loop_tools_v7.py": ("93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d", 10291),
            "app/review-loop-v7.json": ("bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8", 3515),
        }
        for rel, (digest, size) in expected.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual((sha(data), len(data)), (digest, size), rel)
            copied = (CANDIDATE / rel).read_bytes()
            self.assertEqual(copied, data, rel)
        declaration = json.loads((CANDIDATE / "app" / "review-loop-source-capacity.json").read_text(encoding="utf-8"))
        self.assertEqual(declaration["schema"], "review-loop-source-capacity/1")
        self.assertEqual(declaration["tools"]["workbook"]["path"], "labs/review-source-capacity-pass01/workbook.py")
        self.assertEqual(declaration["tools"]["prime_review_pass02"]["sha256"], HISTORICAL_PRIME)
        self.assertNotEqual(declaration["tools"]["prime_review_capacity"]["sha256"], HISTORICAL_PRIME)
        note("historical-modules")

    def test_author_naive_external_copy_is_ambiguous(self) -> None:
        stdout = (KEEP / "known-reproductions" / "record.stdout").read_bytes()
        self.assertIn(b"The artifact measurement is incomplete. The judgment was not recorded.", stdout)
        self.assertNotIn(b"limit sources", stdout)
        prepare = (KEEP / "known-reproductions" / "prepare.stdout").read_text(encoding="utf-8")
        self.assertIn("ambiguous-declared-root", prepare)
        note("naive-external-copy", provenance="known-reproduction")

    def test_author_historical_replay_refuses_0509(self) -> None:
        book = KEEP / "books" / "author-hist-0509"
        if book.exists():
            shutil.rmtree(book)
        book.mkdir(parents=True)
        shutil.copytree(LIVE / "0512.prime-review", book / "0512.prime-review")
        proc, prepared = self.replay(book, "prepare", "0512.prime-review", "05.09")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(prepared.get("measurement"), "complete")
        recorded, payload = self.replay(
            book, "record", "0512.prime-review", "05.09",
            intake=prepared["intake_id"], judgment=str(JUDGMENT_0509),
        )
        self.assertEqual(recorded.returncode, 2)
        self.assertEqual(payload.get("correction"), "refused: limit sources")
        self.assertFalse(payload.get("recorded"))
        self.assertEqual(recorded.stderr, b"")
        folder = KEEP / "author-cycles" / "historical-0509"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "record.stdout").write_bytes(recorded.stdout)
        note("historical-replay-0509", provenance="known-reproduction", correction=payload.get("correction"))

    def assert_cycle(self, folder: str, source: str, pass_id: str, judgment_path: Path, sources: int, document_bytes: int) -> None:
        book = KEEP / "books" / f"author-{folder}"
        if book.exists():
            shutil.rmtree(book)
        book.mkdir(parents=True)
        shutil.copytree(LIVE / source, book / source)
        proc, prepared = self.command(book, "prepare", source, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[:400])
        self.assertEqual(prepared.get("measurement"), "complete")
        form, _ = self.command(book, "form", source, pass_id)
        self.assertEqual(form.returncode, 0, form.stderr)
        page = book / source / f"{pass_id}.md"
        before = page.read_bytes()
        marker = b"## Review - Codex Prime\n"
        self.assertIn(marker, before)
        prefix = before[: before.index(marker) + len(marker)]
        suffix = before[before.index(marker) + len(marker):]
        occupied = b"workbook-review-id:" in suffix
        recorded, payload = self.command(
            book, "record", source, pass_id, intake=prepared["intake_id"], judgment=str(judgment_path),
        )
        self.assertEqual(recorded.returncode, 0, payload.get("correction") or recorded.stderr)
        self.assertTrue(payload.get("recorded"))
        self.assertEqual(payload.get("mode"), "preliminary")
        self.assertEqual(payload.get("custody"), "missing")
        self.assertFalse(payload["cycle"]["called"])
        self.assertFalse(payload["cycle"]["committed"])
        self.assertFalse(payload.get("published_work"))
        self.assertFalse(payload.get("accepted"))
        self.assertEqual(payload.get("authority"), "none")
        supplied = json.loads(judgment_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["judgment"]["finding"], supplied["finding"])
        self.assertEqual(payload["next_action"], supplied["next_action"])
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
        again, recovered = self.command(book, "recover", source, pass_id)
        self.assertEqual(again.returncode, 0, recovered.get("correction"))
        self.assertEqual(recovered["judgment"]["finding"], supplied["finding"])
        self.assertEqual(recovered["next_action"], supplied["next_action"])
        self.assertEqual(recovered.get("custody"), "missing")
        self.assertEqual(recovered.get("target_state"), expected_state)
        label = folder
        folder = KEEP / "author-cycles" / label
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "record.stdout").write_bytes(recorded.stdout)
        (folder / "publish.stdout").write_bytes(published.stdout)
        (folder / "recover.stdout").write_bytes(again.stdout)
        note(label, sources=sources, document_bytes=document_bytes, review_id=payload["review_id"], mode="preliminary", custody="missing", publish=pub.get("correction") or "published")

    def test_author_cycle_0509(self) -> None:
        self.assert_cycle("cycle-0509", "0512.prime-review", "05.09", JUDGMENT_0509, 29, 125955)

    def test_author_cycle_0514(self) -> None:
        self.assert_cycle("cycle-0514", "0522.review-construction", "05.14", JUDGMENT_0514, 20, 62200)

    def test_author_generated_bounds(self) -> None:
        _, old24, proc24 = self.record_generated("bound-24-old", 22, "historical")
        self.assertEqual(proc24.returncode, 0, old24.get("correction"))
        self.assertEqual(old24.get("recorded"), True)
        _, old25, proc25 = self.record_generated("bound-25-old", 23, "historical")
        self.assertEqual(proc25.returncode, 2)
        self.assertEqual(old25.get("correction"), "refused: limit sources")
        book24, new24, newproc = self.record_generated("bound-24-new", 22, "candidate")
        self.assertEqual(newproc.returncode, 0, new24.get("correction"))
        prime = book24 / "workbook-review" / "tmp" / "prime-input.json"
        historical = CANDIDATE / "labs" / "prime-review-pass02" / "prime_review.py"
        successor = CANDIDATE / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        left = run([str(historical), "report", "--input", str(prime), "--root", str(book24), "--json"], CANDIDATE)
        right = run([str(successor), "report", "--input", str(prime), "--root", str(book24), "--json"], CANDIDATE)
        self.assertEqual(left.returncode, 0, left.stderr)
        self.assertEqual(right.returncode, 0, right.stderr)
        self.assertEqual(load_json(left)["sources"], load_json(right)["sources"])
        self.assertEqual(load_json(left)["finding"], load_json(right)["finding"])
        self.assertEqual(load_json(left)["next_action"], load_json(right)["next_action"])
        _, new25, proc = self.record_generated("bound-25-new", 23, "candidate")
        self.assertEqual(proc.returncode, 0, new25.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-25-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 25)
        _, new32, proc32 = self.record_generated("bound-32-new", 30, "candidate")
        self.assertEqual(proc32.returncode, 0, new32.get("correction"))
        self.assertEqual(len(json.loads((KEEP / "books" / "bound-32-new" / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))["sources"]), 32)
        _, new33, proc33 = self.record_generated("bound-33-new", 31, "candidate")
        self.assertEqual(proc33.returncode, 2)
        self.assertIn("33 sources exceeds supported limit 32", new33.get("correction", ""))
        self.assertIn("split the return so one record binds at most 32 sources", new33.get("correction", ""))
        self.assertFalse(new33.get("recorded"))
        pending = (KEEP / "books" / "bound-33-new" / PAGE / f"{PASS}.md").read_text(encoding="utf-8")
        self.assertIn("## Review - Codex Prime\nPENDING.\n", pending)
        note("generated-bounds", old_24=True, old_25="limit sources", new_32=32, new_33=33)

    def test_author_holds_stay_24(self) -> None:
        book = KEEP / "books" / "bound-24-new"
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        prime["holds"] = [{} for _ in range(25)]
        path = KEEP / "books" / "holds-25.json"
        path.write_bytes((json.dumps(prime) + "\n").encode("utf-8"))
        successor = CANDIDATE / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--root", str(book), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: limit holds", proc.stderr)
        self.assertNotIn(b"32", proc.stderr)
        note("holds-stay-24")

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
        self.assertLessEqual(len(document["sources"]), 32)
        self.assertGreater(len(blob), 262144)
        path = KEEP / "books" / "over-document.json"
        path.write_bytes(blob)
        successor = CANDIDATE / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused: input: input exceeds 262144 bytes", proc.stderr)
        self.assertNotIn(b"limit sources", proc.stderr)
        note("document-bound", bytes=len(blob), sources=22)

    def test_author_hostile_count_is_not_trimmed(self) -> None:
        sources = []
        for index in range(32):
            sources.append({"logical_path": f"p{index}"})
        sources.append({"logical_path": "p0"})
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
        path = KEEP / "books" / "hostile-33.json"
        path.write_bytes((json.dumps(document) + "\n").encode("utf-8"))
        successor = CANDIDATE / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        text = proc.stderr.decode("utf-8")
        self.assertIn("33 sources exceeds supported limit 32", text)
        self.assertNotIn("32 sources exceeds", text)
        note("hostile-count", provenance="author-hostile")

    def test_author_hostile_document_bound_stays(self) -> None:
        self.test_author_document_bound()
        note("hostile-document", provenance="author-hostile")

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
        note("duplicate-and-conflict")

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
        note("code-root-excluded", emitted=len(prime["sources"]))

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
        note("changed-and-missing")

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
        successor = CANDIDATE / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        proc = run([str(successor), "report", "--input", str(path), "--root", str(KEEP / "books" / "bound-24-new"), "--json"], CANDIDATE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"bad type sources[0].content_bytes", proc.stderr)
        note("malformed-and-unknown-size")

    def test_author_wrong_pins(self) -> None:
        tampered = KEEP / "books" / "tampered-successor"
        if tampered.exists():
            shutil.rmtree(tampered)
        shutil.copytree(CANDIDATE, tampered, ignore=shutil.ignore_patterns("__pycache__"))
        target = tampered / "labs" / "review-source-capacity-pass01" / "prime_review.py"
        data = bytearray(target.read_bytes())
        data[-1] = data[-1] ^ 1
        target.write_bytes(data)
        book = KEEP / "books" / "pin-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run([str(tampered / "app" / "librarian.py"), "review-loop", "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS], tampered)
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pinned tool hash does not match: labs/review-source-capacity-pass01/prime_review.py", proc.stderr)
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
        note("wrong-pins")

    def test_author_lab_door_is_not_an_install(self) -> None:
        book = KEEP / "books" / "pin-book"
        book.mkdir(parents=True, exist_ok=True)
        proc = run(
            [str(LAB / "review_loop_tools_source_capacity.py"), "prepare", "--book", str(book), "--source", PAGE, "--pass", PASS],
            LAB,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"review loop declaration is missing", proc.stderr)
        self.assertEqual(proc.stdout, b"")
        note("lab-door-not-install")

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
        note("linked-pin")


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
