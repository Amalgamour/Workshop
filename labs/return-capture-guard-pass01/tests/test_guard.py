"""Unit seams for the guarded legacy writer. These tests do not touch the live book."""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(REPO / "labs" / "return-capture-guard-pass01"))
import return_capture_guard as tool  # noqa: E402

PINS = {
    "labs/return-capture-pass01/return_capture.py": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
    "labs/return-lines-pass01/return_lines.py": ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "labs/return-capture-pass01/return_inspect.py": ("947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", 11402),
    "labs/return-lines-pass04/return_lines.py": ("708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6", 12124),
    "labs/return-access-pass01/return_access.py": ("501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5", 26561),
    "labs/capture-handoff-pass01/handoff.py": ("a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a", 51828),
}
ROOT = Path(tempfile.mkdtemp(prefix="0521-0508-unit-", dir=r"D:\librarian\temp"))


def reserve_argv(book: Path) -> list[str]:
    return [
        "reserve", "--book", str(book), "--submission", "unit-0508",
        "--name", "unit", "--origin-book", "00.00.10.work",
        "--origin-page", "0508.guard", "--origin-batch", "05.08",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "unit label",
    ]


class Result:
    def __init__(self) -> None:
        self.code = 0
        self.text = "member 0101.unit\nresult reserved\n"
        self.calls = 0

    def execute(self, argv: list[str]):
        self.calls += 1
        return self


class GuardTests(unittest.TestCase):
    def test_source_has_no_force_flag(self) -> None:
        text = (REPO / "labs/return-capture-guard-pass01/return_capture_guard.py").read_text(encoding="utf-8")
        self.assertNotIn("--force", text)
        self.assertNotIn("--allow-live", text)
        self.assertNotIn("designate_live", text)

    def test_tampered_writer_is_not_executed(self) -> None:
        marker = ROOT / "marker.txt"
        bad = ROOT / "tampered.py"
        bad.write_bytes(b"open(r'%s', 'w', encoding='utf-8').write('started')\n" % str(marker).encode())
        with self.assertRaises(tool.PinMismatch):
            tool.load_pinned(str(bad), tool.CAPTURE_SHA, bad.stat().st_size, "tampered_writer")
        self.assertFalse(marker.exists())

    def test_folder_name_is_not_a_declaration(self) -> None:
        book = ROOT / "named-only"
        (book / "0121.synthetic-filing").mkdir(parents=True)
        found = tool.classify(str(book))
        self.assertEqual(found["status"], "undeclared")
        self.assertEqual(found["protection"], "absent")

    def test_declared_reserve_does_not_load_the_writer(self) -> None:
        book = ROOT / "declared"
        book.mkdir()
        lines = tool.load_lines()
        (book / "return-line-layout.json").write_bytes(lines.dump(lines.layout_body("disposable-copy")))
        writer = Result()
        code, text = tool.run(reserve_argv(book), loader=lambda: writer)
        self.assertEqual(code, 2)
        self.assertEqual(writer.calls, 0)
        self.assertIn("writer_started: false", text)
        self.assertIn("result refused", text)
        self.assertNotIn("result reserved", text.splitlines())
        self.assertFalse((book / "0100.band.returns").exists())

    def test_undeclared_states_the_missing_protection(self) -> None:
        book = ROOT / "undeclared"
        book.mkdir()
        writer = Result()
        code, text = tool.run(reserve_argv(book), loader=lambda: writer)
        self.assertEqual(code, 0)
        self.assertEqual(writer.calls, 1)
        self.assertIn("result reserved", text.splitlines())
        self.assertIn("has not gained line-pass protection", text)

    def test_malformed_and_conflict_do_not_allocate(self) -> None:
        lines = tool.load_lines()
        malformed = ROOT / "malformed"
        malformed.mkdir()
        (malformed / "return-line-layout.json").write_bytes(b"{")
        writer = Result()
        code, text = tool.run(reserve_argv(malformed), loader=lambda: writer)
        self.assertEqual(code, 2)
        self.assertEqual(writer.calls, 0)
        self.assertIn("state: attention", text)
        conflict = ROOT / "conflict"
        conflict.mkdir()
        body = lines.layout_body("disposable-copy")
        (conflict / "return-line-layout.json").write_bytes(
            ( __import__("json").dumps(body, separators=(",", ":")) + "\n").encode("utf-8")
        )
        code, text = tool.run(reserve_argv(conflict), loader=lambda: writer)
        self.assertEqual(code, 2)
        self.assertEqual(writer.calls, 0)
        self.assertIn("state: attention", text)
        self.assertIn("conflicts with the accepted line-pass declaration", text)
        self.assertIn("Sequential allocation was not used", text)


def tearDownModule() -> None:
    for rel, (digest, size) in PINS.items():
        data = (REPO / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest or len(data) != size:
            raise AssertionError(rel)


if __name__ == "__main__":
    unittest.main()
