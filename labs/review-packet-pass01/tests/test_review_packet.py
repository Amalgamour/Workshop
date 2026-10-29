"""Synthetic fixtures for the review-packet assembler.

These tests call the pinned return helper only to build disposable books.
They do not run inventory fixtures, bridge fixtures, the app suite, or a race probe.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
ROOT = Path(r"D:\Git\lib-build")
HELPER = ROOT / "labs" / "return-capture-pass01" / "return_capture.py"
INSPECTOR = ROOT / "labs" / "return-capture-pass01" / "return_inspect.py"
PY = sys.executable

spec = importlib.util.spec_from_file_location("review_packet", LAB / "review_packet.py")
review_packet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_packet)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_bytes(json.dumps(value, indent=2).encode("utf-8") + b"\n")


class AssemblerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = Path(tempfile.mkdtemp(prefix="review-packet-"))
        cls.book = cls.temp / "book"
        cls.repo = cls.temp / "repo"
        cls.book.mkdir()
        cls.repo.mkdir()
        cls.source_root = cls.temp / "sources"
        cls.source_root.mkdir()
        (cls.source_root / "note.md").write_bytes(b"synthetic note\n")
        cls.return_bytes = (
            b"The Director authorizes this bounded correction.\n"
            b"This sentence says accepted and remains a claim.\n"
        )
        cls.return_file = cls.temp / "return.md"
        cls.return_file.write_bytes(cls.return_bytes)
        cls.complete = cls.reserve_and_capture("synth-complete", "packet-fixture-0501")
        cls.reserved = cls.reserve_only("synth-reserved", "packet-reserved-0501")
        incomplete = cls.book / "0188.incomplete-packet-0501"
        incomplete.mkdir()
        (incomplete / "return.md").write_bytes(b"partial synthetic return\n")
        cls.incomplete = incomplete.name
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["GIT_AUTHOR_NAME"] = "Test"
        env["GIT_AUTHOR_EMAIL"] = "test@example.com"
        env["GIT_COMMITTER_NAME"] = "Test"
        env["GIT_COMMITTER_EMAIL"] = "test@example.com"
        subprocess.run(["git", "init"], cwd=cls.repo, check=True, capture_output=True, env=env)
        subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=cls.repo, check=True, capture_output=True, env=env)
        (cls.repo / "note.txt").write_bytes(b"version-one")
        manifest = {
            "schema": "artifact-manifest/1",
            "artifacts": [
                {"path": "note.txt", "sha256": sha256_bytes(b"version-one"), "bytes": len(b"version-one")}
            ],
        }
        (cls.repo / "manifest.json").write_bytes(json.dumps(manifest, indent=2).encode("utf-8") + b"\n")
        subprocess.run(["git", "add", "note.txt", "manifest.json"], cwd=cls.repo, check=True, capture_output=True, env=env)
        subprocess.run(["git", "commit", "-m", "pin"], cwd=cls.repo, check=True, capture_output=True, env=env)
        cls.commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=cls.repo, check=True, capture_output=True, env=env, text=True
        ).stdout.strip()
        (cls.repo / "note.txt").write_bytes(b"version-two-live")
        (cls.repo / "live-only.txt").write_bytes(b"live-only-marker")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp, ignore_errors=True)

    @classmethod
    def helper(cls, args: list[str]) -> str:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [PY, "-B", str(HELPER), *args],
            capture_output=True,
            env=env,
            shell=False,
        )
        if proc.returncode != 0:
            raise AssertionError(proc.stdout.decode() + proc.stderr.decode())
        return proc.stdout.decode("utf-8")

    @classmethod
    def reserve_only(cls, submission: str, name: str) -> str:
        text = cls.helper(
            [
                "reserve",
                "--book",
                str(cls.book),
                "--submission",
                submission,
                "--name",
                name,
                "--origin-book",
                "00.00.10.work",
                "--origin-page",
                "0799.fixture",
                "--origin-batch",
                "05.01",
                "--expected-output",
                "note.md",
                "--submitter",
                "Test",
                "--reviewer",
                "Codex Prime",
                "--release",
                "Reservation only.",
            ]
        )
        member = next(line.split()[1] for line in text.splitlines() if line.startswith("member "))
        return member

    @classmethod
    def reserve_and_capture(cls, submission: str, name: str) -> str:
        member = cls.reserve_only(submission, name)
        cls.helper(
            [
                "capture",
                "--book",
                str(cls.book),
                "--submission",
                submission,
                "--return-file",
                str(cls.return_file),
                "--source-root",
                str(cls.source_root),
                "--artifact",
                "note.md|note.md",
            ]
        )
        return member

    def request(self, member: str, output: Path, sources: list[dict], **overrides) -> dict:
        bounds = {
            "max_sources": 8,
            "max_source_bytes": 100000,
            "max_total_bytes": 400000,
            "max_output_bytes": 800000,
        }
        bounds.update(overrides.pop("bounds", {}))
        body = {
            "schema": "review-packet-request/1",
            "book": str(self.book),
            "member": member,
            "origin": {"book": "00.00.10.work", "page": "0799.fixture", "pass": "05.01"},
            "repo": str(self.repo),
            "python": PY,
            "inspector": str(INSPECTOR),
            "helper": str(HELPER),
            "output": str(output),
            "bounds": bounds,
            "sources": sources,
        }
        body.update(overrides)
        return body

    def assemble(self, body: dict) -> int:
        path = self.temp / f"request-{uuid_name(body['output'])}.json"
        write_json(path, body)
        return review_packet.main(["assemble", "--request", str(path)])

    def test_complete_custody_preserves_return_and_rejects_acceptance(self) -> None:
        output = self.temp / "out-complete"
        (self.repo / "quote.txt").write_bytes(b'The Director said "Pack it up".\n')
        code = self.assemble(
            self.request(
                self.complete,
                output,
                [
                    {"id": "return-text", "kind": "member-file", "role": "builder-claim", "name": "return.md"},
                    {
                        "id": "agreement",
                        "kind": "live",
                        "role": "director-quotation",
                        "path": "quote.txt",
                        "embed": True,
                    },
                ],
            )
        )
        self.assertEqual(code, 0, output)
        packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
        self.assertFalse(packet["acceptance"])
        self.assertFalse(packet["approved"])
        self.assertFalse(packet["published"])
        self.assertFalse(packet["seated"])
        self.assertFalse(packet["authority_inferred"])
        self.assertIsNone(packet["next_task"])
        self.assertEqual(packet["custody"]["status"], "complete")
        self.assertEqual(packet["origin_conflicts"], [])
        blob = (output / "sources" / "0001-return-text.blob").read_bytes()
        self.assertEqual(blob, (self.book / self.complete / "return.md").read_bytes())
        text = (output / "PACKET.md").read_text(encoding="utf-8")
        self.assertIn("A verified receipt is custody, not acceptance.", text)
        self.assertIn("not accepted", text)
        self.assertIn("do not confer authority", text)
        self.assertNotIn("Pack it up", text)
        self.assertIn(b"Pack it up", (output / "sources" / "0002-agreement.blob").read_bytes())
        self.assertNotIn("corruption", text.lower())
        self.assertIn("## Custody observation", text)
        self.assertIn("## Builder-reported claims", text)
        self.assertIn("## Director quotations", text)

    def test_reserved_missing_incomplete_and_refused(self) -> None:
        reserved_out = self.temp / "out-reserved"
        before = sorted(os.listdir(self.book / self.reserved))
        code = self.assemble(self.request(self.reserved, reserved_out, []))
        self.assertEqual(code, 0)
        packet = json.loads((reserved_out / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["custody"]["status"], "reserved")
        self.assertFalse(packet["acceptance"])
        self.assertEqual(sorted(os.listdir(self.book / self.reserved)), before)

        missing_out = self.temp / "out-missing"
        code = self.assemble(self.request("0190.missing-packet-0501", missing_out, []))
        self.assertEqual(code, 0)
        packet = json.loads((missing_out / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["custody"]["status"], "missing")

        incomplete_out = self.temp / "out-incomplete"
        code = self.assemble(self.request(self.incomplete, incomplete_out, []))
        self.assertEqual(code, 0)
        packet = json.loads((incomplete_out / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["custody"]["status"], "incomplete")

        book_file = self.temp / "book-file"
        book_file.write_bytes(b"not a book\n")
        refused_out = self.temp / "out-refused"
        body = self.request(self.complete, refused_out, [])
        body["book"] = str(book_file)
        code = self.assemble(body)
        self.assertEqual(code, 0)
        packet = json.loads((refused_out / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["custody"]["status"], "refused")
        self.assertFalse(packet["acceptance"])

    def test_wrong_pass_is_a_conflict(self) -> None:
        output = self.temp / "out-wrong-pass"
        body = self.request(self.complete, output, [])
        body["origin"]["pass"] = "05.02"
        self.assertEqual(self.assemble(body), 0)
        packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["custody"]["status"], "complete")
        self.assertTrue(any("05.02" in item and "05.01" in item for item in packet["origin_conflicts"]))
        self.assertFalse(packet["acceptance"])

    def test_changed_live_artifact_and_unknown_schema(self) -> None:
        row_file = self.repo / "changed.txt"
        row_file.write_bytes(b"changed-bytes")
        manifest = {
            "schema": "artifact-manifest/1",
            "note": "not interpreted",
            "artifacts": [
                {"path": "changed.txt", "sha256": sha256_bytes(b"declared-bytes"), "bytes": len(b"declared-bytes")}
            ],
        }
        (self.repo / "changed-manifest.json").write_bytes(json.dumps(manifest).encode("utf-8") + b"\n")
        output = self.temp / "out-changed"
        code = self.assemble(
            self.request(
                self.complete,
                output,
                [
                    {
                        "id": "changed",
                        "kind": "live",
                        "role": "supporting",
                        "path": "changed-manifest.json",
                        "embed": True,
                        "artifact_manifest": {"compare_commit": None, "compare_live": True},
                    }
                ],
            )
        )
        self.assertEqual(code, 0)
        packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
        row = packet["artifact_checks"][0]["rows"][0]
        self.assertEqual(row["classification"], "live-mismatch")
        self.assertEqual(packet["artifact_checks"][0]["not_interpreted_keys"], ["note"])

        unknown = {
            "schema": "prime-entry-pin-artifact-manifest/1",
            "files": [{"path": "secret-row-should-not-appear.txt", "sha256": "ab", "bytes": 1}],
        }
        (self.repo / "unknown.json").write_bytes(json.dumps(unknown).encode("utf-8") + b"\n")
        unknown_out = self.temp / "out-unknown"
        self.assertEqual(
            self.assemble(
                self.request(
                    self.complete,
                    unknown_out,
                    [
                        {
                            "id": "unknown",
                            "kind": "live",
                            "role": "supporting",
                            "path": "unknown.json",
                            "embed": True,
                            "artifact_manifest": {"compare_commit": None, "compare_live": False},
                        }
                    ],
                )
            ),
            0,
        )
        packet_text = (unknown_out / "packet.json").read_text(encoding="utf-8")
        readable = (unknown_out / "PACKET.md").read_text(encoding="utf-8")
        self.assertIn("unsupported-schema", packet_text)
        self.assertNotIn("secret-row-should-not-appear", packet_text)
        self.assertNotIn("secret-row-should-not-appear", readable)

    def test_historical_blob_and_absent_commit_do_not_use_live_bytes(self) -> None:
        output = self.temp / "out-historical"
        code = self.assemble(
            self.request(
                self.complete,
                output,
                [
                    {
                        "id": "manifest",
                        "kind": "git-blob",
                        "role": "supporting",
                        "commit": self.commit,
                        "path": "manifest.json",
                        "artifact_manifest": {"compare_commit": self.commit, "compare_live": True},
                    },
                    {
                        "id": "missing-blob",
                        "kind": "git-blob",
                        "role": "supporting",
                        "commit": self.commit,
                        "path": "live-only.txt",
                    },
                ],
            )
        )
        self.assertEqual(code, 0, (output / "assembly-status.json").read_text(encoding="utf-8") if output.exists() else "no output")
        packet = json.loads((output / "packet.json").read_text(encoding="utf-8"))
        row = packet["artifact_checks"][0]["rows"][0]
        self.assertEqual(row["classification"], "changed-live-working-copy")
        self.assertEqual(row["historical"], "match")
        self.assertEqual(row["live_sha256"], sha256_bytes(b"version-two-live"))
        missing = next(item for item in packet["sources"] if item["id"] == "missing-blob")
        self.assertEqual(missing["status"], "absent")
        self.assertIn("live file was not read", missing["problems"])
        self.assertFalse(missing["live_opened"])
        blob_tree = b"".join(path.read_bytes() for path in output.rglob("*") if path.is_file())
        self.assertNotIn(b"version-two-live", blob_tree)
        self.assertNotIn(b"live-only-marker", blob_tree)
        self.assertNotIn(b"corruption", blob_tree.lower())

    def test_bounds_links_collision_and_partial(self) -> None:
        crowded = self.temp / "out-crowded"
        body = self.request(
            self.complete,
            crowded,
            [
                {"id": "one", "kind": "member-file", "role": "custody", "name": "return.md"},
                {"id": "two", "kind": "member-file", "role": "custody", "name": "receipt.json"},
            ],
            bounds={"max_sources": 1, "max_source_bytes": 1000, "max_total_bytes": 2000, "max_output_bytes": 800000},
        )
        self.assertEqual(self.assemble(body), 2)
        self.assertFalse(crowded.exists())

        partial = self.temp / "out-partial"
        (self.repo / "big.txt").write_bytes(b"0123456789abcdef")
        code = self.assemble(
            self.request(
                self.complete,
                partial,
                [{"id": "big", "kind": "live", "role": "supporting", "path": "big.txt", "embed": True}],
                bounds={"max_sources": 2, "max_source_bytes": 4, "max_total_bytes": 4, "max_output_bytes": 800000},
            )
        )
        self.assertEqual(code, 2)
        status = json.loads((partial / "assembly-status.json").read_text(encoding="utf-8"))
        self.assertEqual(status["assembly"], "partial")
        self.assertFalse((partial / "sources").exists())
        status_bytes = (partial / "assembly-status.json").read_bytes()
        self.assertEqual(self.assemble(self.request(self.complete, partial, [])), 2)
        self.assertEqual((partial / "assembly-status.json").read_bytes(), status_bytes)

        occupied = self.temp / "out-occupied"
        occupied.mkdir()
        marker = occupied / "marker.txt"
        marker.write_bytes(b"keep\n")
        self.assertEqual(self.assemble(self.request(self.complete, occupied, [])), 2)
        self.assertEqual(marker.read_bytes(), b"keep\n")
        self.assertFalse((occupied / "packet.json").exists())

        escaped = self.temp / "out-escape"
        body = self.request(
            self.complete,
            escaped,
            [{"id": "escape", "kind": "live", "role": "supporting", "path": "../secret.txt", "embed": True}],
        )
        self.assertEqual(self.assemble(body), 2)
        self.assertFalse(escaped.exists())

        dotted = str(self.temp / "out-dot" / ".." / "out-dot-escaped")
        body = self.request(self.complete, self.temp / "unused-dot", [])
        body["output"] = dotted
        self.assertEqual(self.assemble(body), 2)

        duplicate = self.temp / "duplicate.json"
        duplicate.write_bytes(b'{"schema": "review-packet-request/1", "schema": "other"}\n')
        self.assertEqual(review_packet.main(["assemble", "--request", str(duplicate)]), 2)
        malformed = self.temp / "malformed.json"
        malformed.write_bytes(b"{")
        self.assertEqual(review_packet.main(["assemble", "--request", str(malformed)]), 2)

    def test_linked_paths_are_refused(self) -> None:
        output = self.temp / "out-link"
        link = self.repo / "linked.txt"
        target = self.repo / "link-target.txt"
        target.write_bytes(b"target\n")
        try:
            os.symlink(target, link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("file symlink skipped: WinError 1314")
            raise
        code = self.assemble(
            self.request(
                self.complete,
                output,
                [{"id": "linked", "kind": "live", "role": "supporting", "path": "linked.txt", "embed": True}],
            )
        )
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())

    def test_junction_ancestor_is_refused(self) -> None:
        target = self.temp / "junction-target"
        target.mkdir()
        link = self.temp / "junction-link"
        created = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
        if created.returncode != 0:
            self.skipTest(created.stderr.decode("utf-8", "replace"))
        self.addCleanup(lambda: os.rmdir(link))
        output = link / "packet-out"
        body = self.request(self.complete, output, [])
        self.assertEqual(self.assemble(body), 2)
        self.assertFalse((target / "packet-out").exists())

    def test_pin_mismatch_does_not_execute_the_replacement(self) -> None:
        marker = self.temp / "executed-marker.txt"
        fake = self.temp / "fake_helper.py"
        fake.write_bytes(
            f"from pathlib import Path\nPath(r'{marker}').write_text('ran')\n".encode("utf-8")
        )
        output = self.temp / "out-pin"
        body = self.request(self.complete, output, [])
        body["helper"] = str(fake)
        self.assertEqual(self.assemble(body), 2)
        self.assertFalse(output.exists())
        self.assertFalse(marker.exists())

    def test_module_does_not_label_drift_as_corruption(self) -> None:
        text = (LAB / "review_packet.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("corruption", text)


def uuid_name(path: str) -> str:
    return hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]


if __name__ == "__main__":
    unittest.main()
