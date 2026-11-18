"""Bounded pass02 checks on disposable copies. These tests do not touch the live book."""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(r"D:\Git\lib-build")
LIVE = REPO / "00.kernel" / "00.00.10.work"
AUDIT_PATH = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
RELEASE_PATH = LIVE / "0521.return-placement" / "evidence" / "build05.04" / "release.txt"
PASS01 = REPO / "labs" / "return-lines-pass01" / "return_lines.py"
EXTERNAL = Path(r"D:\librarian\temp\0521-0504")
sys.path.insert(0, str(REPO / "labs" / "return-lines-pass02"))
import return_lines as tool  # noqa: E402

LINES = tool.load_lines()
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
PASS01_BEFORE = PASS01.read_bytes()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def run(args: list[str]) -> tuple[int, dict, bytes]:
    buf = io.BytesIO()

    class Out:
        buffer = buf

    old = sys.stdout
    sys.stdout = Out()
    try:
        code = tool.main(args)
    finally:
        sys.stdout = old
        tool.clear_fault()
    raw = buf.getvalue()
    body = json.loads(raw.decode("utf-8")) if raw.strip() else {}
    return code, body, raw


def work(name: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = EXTERNAL / f"{stamp}-{name}"
    root.mkdir(parents=True)
    for part in ("book", "backup", "staging", "retired"):
        (root / part).mkdir()
    return root


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())


def copy_member(book: Path, member: str) -> None:
    src_root = LIVE / member
    for dirpath, dirnames, filenames in os.walk(src_root):
        dirnames[:] = [item for item in dirnames if not LINES.is_reparse(os.path.join(dirpath, item))]
        for filename in filenames:
            src = Path(dirpath) / filename
            rel = src.relative_to(src_root).as_posix()
            copy_file(src, book / member / rel)


def copy_door(book: Path) -> None:
    copy_file(LIVE / "0100.band.returns" / "01.md", book / "0100.band.returns" / "01.md")


def audit_body() -> dict:
    return json.loads(AUDIT_PATH.read_bytes())


def filtered(members: list[str]) -> dict:
    body = audit_body()
    wanted = set(members)
    body["records"] = [record for record in body["records"] if record["old_member"] in wanted]
    files = []
    for entry in body["files"]:
        path = entry["path"].replace("\\", "/")
        if any(f"/{name}/" in f"/{path}" for name in wanted):
            files.append(entry)
    body["files"] = files
    return body


def write_audit(root: Path, members: list[str]) -> tuple[Path, dict]:
    body = filtered(members)
    path = root / "audit.json"
    path.write_bytes(dump(body))
    return path, body


def layout_sha() -> str:
    return LINES.sha(LINES.dump(LINES.layout_body("00.00.10.work")))


def write_auth(path: Path, book: Path, plan: Path, audit: Path, backup: Path, staging: Path, retired: Path,
               operations: list[str] | None = None, **overrides) -> None:
    raw = audit.read_bytes()
    body = {
        "audit_bytes": len(raw),
        "audit_sha256": sha(raw),
        "backup_root": str(backup),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(operations or OPS),
        "plan_sha256": sha(plan.read_bytes()),
        "release": tool.RELEASE_TEXT,
        "retired_root": str(retired),
        "schema": "return-line-authorization/1",
        "staging_root": str(staging),
        "synthetic": True,
    }
    body.update(overrides)
    path.write_bytes(dump(body))


def auth_args(root: Path, audit: Path, plan: Path) -> list[str]:
    return [
        "--authorization", str(root / "auth.json"),
        "--audit", str(audit),
        "--plan", str(plan),
        "--backup", str(root / "backup"),
        "--staging", str(root / "staging"),
        "--retired", str(root / "retired"),
    ]


def seed(root: Path, members: list[str], plant: str | None = None) -> tuple[Path, dict]:
    book = root / "book"
    copy_door(book)
    audit_path, body = write_audit(root, members)
    for record in body["records"]:
        copy_member(book, record["old_member"])
        if record.get("route") == "page-local-colab":
            copy_file(LIVE / record["target_return"], book / record["target_return"])
    if plant:
        (book / plant).mkdir(parents=True)
        (book / plant / "note.txt").write_bytes(b"planted occupant\n")
    return audit_path, body


def plan(root: Path, audit: Path) -> Path:
    out = root / "plan.json"
    code, body, _raw = run(["plan", "--book", str(root / "book"), "--audit", str(audit), "--out", str(out)])
    if code != 0:
        raise AssertionError(body)
    return out


def prepare(root: Path, members: list[str], plant: str | None = None) -> tuple[Path, Path, dict]:
    audit, body = seed(root, members, plant)
    planned = plan(root, audit)
    write_auth(root / "auth.json", root / "book", planned, audit, root / "backup", root / "staging", root / "retired")
    return audit, planned, body


def invoke(root: Path, audit: Path, plan_path: Path, command: str, extra: list[str] | None = None) -> tuple[int, dict, bytes]:
    args = [command, "--book", str(root / "book"), *auth_args(root, audit, plan_path)]
    if extra:
        args.extend(extra)
    if command == "init":
        args[1:1] = ["--name", "00.00.10.work"]
        # command is args[0]; insert name after book. Rebuild cleanly.
        args = ["init", "--book", str(root / "book"), "--name", "00.00.10.work", *auth_args(root, audit, plan_path)]
        if extra:
            args.extend(extra)
    return run(args)


class Pass02Tests(unittest.TestCase):
    def test_release_text_matches_file(self) -> None:
        self.assertEqual(tool.RELEASE_TEXT.encode("utf-8"), RELEASE_PATH.read_bytes())

    def test_source_has_no_magic_counts(self) -> None:
        text = (REPO / "labs" / "return-lines-pass02" / "return_lines.py").read_text(encoding="utf-8")
        self.assertNotIn("== 83", text)
        self.assertNotIn("== 18", text)
        self.assertNotIn("import return_capture", text)

    def test_adopt_refused(self) -> None:
        code, body, _raw = run(["adopt"])
        self.assertEqual(code, 2)
        self.assertEqual(body["check"], "successor command")
        self.assertFalse((LIVE / "return-line-layout.json").exists())

    def test_live_book_refuses_even_with_authorization(self) -> None:
        root = work("live-auth")
        audit = root / "audit.json"
        audit.write_bytes(b"{}")
        plan_path = root / "plan.json"
        plan_path.write_bytes(b"{}\n")
        write_auth(root / "auth.json", LIVE, plan_path, audit, root / "backup", root / "staging", root / "retired",
                   book_path=str(LIVE))
        before = (LIVE / "0100.band.returns" / "01.md").read_bytes()
        code, body, _raw = invoke(root, audit, plan_path, "init")
        # book argument is the disposable root; point the command at the live book.
        code, body, _raw = run([
            "init", "--book", str(LIVE), "--name", "00.00.10.work",
            "--authorization", str(root / "auth.json"), "--audit", str(audit), "--plan", str(plan_path),
            "--backup", str(root / "backup"), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ])
        self.assertEqual(code, 2)
        self.assertEqual(body["check"], "live book")
        self.assertFalse((LIVE / "return-line-layout.json").exists())
        self.assertEqual((LIVE / "0100.band.returns" / "01.md").read_bytes(), before)

    def test_authorization_naming_live_path_refuses(self) -> None:
        root = work("auth-names-live")
        audit = root / "audit.json"
        audit.write_bytes(b"{}")
        plan_path = root / "plan.json"
        plan_path.write_bytes(b"{}\n")
        copy_door(root / "book")
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   book_path=str(LIVE))
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertEqual(body["check"], "live book")
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        self.assertFalse((LIVE / "return-line-layout.json").exists())

    def test_synthetic_false_and_bad_identity(self) -> None:
        root = work("bad-auth")
        copy_door(root / "book")
        audit = root / "audit.json"
        audit.write_bytes(b"{}\n")
        plan_path = root / "plan.json"
        plan_path.write_bytes(b"{}\n")
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   synthetic=False)
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertIn("synthetic", body["correction"])
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   executor="Grok-2")
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertIn("executor", body["correction"])
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   release=tool.RELEASE_TEXT.replace("bounded", "UNBOUNDED"))
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertIn("release", body["correction"])
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   operations=["stage"])
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertIn("not authorized", body["correction"])
        write_auth(root / "auth.json", root / "book", plan_path, audit, root / "backup", root / "staging", root / "retired",
                   layout_sha256="0" * 64)
        code, body, _raw = invoke(root, audit, plan_path, "init")
        self.assertEqual(code, 2)
        self.assertIn("layout hash", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())

    def test_door_without_authorization_file_is_rejected_by_cli_shape(self) -> None:
        root = work("no-auth-flag")
        copy_door(root / "book")
        with self.assertRaises(SystemExit):
            run(["init", "--book", str(root / "book"), "--name", "00.00.10.work"])

    def test_small_reconstruct_publish_retire(self) -> None:
        members = ["0101.app-entry-0506", "0154.colab-support-first-0501", "0165.bench-method-colab-0501"]
        root = work("small-flow")
        audit, planned, body = prepare(root, members)
        book = root / "book"
        code, result, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "stage")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "reconstruct")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["detail"]["record_count"], len(body["records"]))
        self.assertEqual(result["detail"]["page_local_count"], sum(1 for record in body["records"] if record["route"] == "page-local-colab"))
        self.assertEqual(result["detail"]["incomplete_count"], sum(1 for record in body["records"] if record.get("verify_exit") != 0))
        self.assertEqual(result["detail"]["accepted"], False)
        manifest = json.loads((root / "staging" / "reconstruction-manifest.json").read_bytes())
        found = {item["archived_identity"]: item for item in manifest["records"]}
        self.assertNotEqual(found["0101.app-entry-0506"]["archived_identity"], found["0101.app-entry-0506"]["logical_return_path"])
        self.assertEqual(found["0154.colab-support-first-0501"]["state"], "incomplete")
        self.assertFalse((root / "staging" / "pages" / "0110.colab-tools" / "05.01.return.md").exists())
        tail = (book / "0701.bench-method" / "05.01.return.md").read_bytes()
        self.assertEqual(tail, (LIVE / "0701.bench-method" / "05.01.return.md").read_bytes())
        code, result, _raw = invoke(root, audit, planned, "publish")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["detail"]["published"], False)
        code, result, _raw = invoke(root, audit, planned, "retire")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["detail"]["remaining_old_members"], 0)
        for record in body["records"]:
            self.assertFalse((book / record["old_member"]).exists(), record["old_member"])
        self.assertTrue((book / "0100.band.returns" / "01.md").is_file())
        self.assertEqual((book / "0701.bench-method" / "05.01.return.md").read_bytes(), tail)
        self.assertFalse((book / "0110.colab-tools" / "05.01.return.md").exists())
        code, looked, _raw = run(["lookup", "--book", str(book), "--member", "0154.colab-support-first-0501"])
        self.assertEqual(code, 1, looked)
        self.assertEqual(looked["state"], "incomplete")
        self.assertIsNone(looked["descriptor"]["return_sha256"])
        self.assertIsNone(looked["descriptor"]["return_bytes"])
        self.assertEqual(set(looked["descriptor"]), LINES.DESCRIPTOR_KEYS)
        self.assertEqual(looked["descriptor"]["verification"]["tool_path"], "labs/return-lines-pass01/return_lines.py")
        self.assertEqual(looked["detail"]["retained_original"]["book_member_present"], False)
        self.assertTrue(looked["detail"]["retained_original"]["retired_rel"].startswith("originals/") or looked["detail"]["retained_original"]["retired_rel"].startswith("occupants/"))
        code, looked, _raw = run(["descriptor", "--book", str(book), "--member", "0101.app-entry-0506"])
        self.assertEqual(code, 0, looked)
        self.assertEqual(set(looked), LINES.DESCRIPTOR_KEYS)
        self.assertEqual(looked["custody_format"], "legacy-relocated/1")
        self.assertEqual(looked["state"], "complete")
        code, looked, _raw = run(["lookup", "--book", str(book), "--member", "0165.bench-method-colab-0501"])
        self.assertEqual(code, 0, looked)
        self.assertEqual(looked["descriptor"]["route"], "page-local-colab")
        self.assertEqual(looked["detail"]["new_home"]["target_page"], "0701.bench-method")

    def test_interrupt_resume_partial_and_rollback(self) -> None:
        root = work("interrupt")
        audit, planned, body = prepare(root, ["0101.app-entry-0506"])
        code, result, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "stage", ["--interrupt-after", "0"])
        self.assertEqual(code, 3, result)
        self.assertFalse((root / "backup" / "stage-complete.json").exists())
        code, result, _raw = invoke(root, audit, planned, "stage-resume")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "reconstruct", ["--interrupt-after", "1"])
        self.assertEqual(code, 3, result)
        self.assertFalse((root / "staging" / "reconstruction-complete.json").exists())
        code, result, _raw = invoke(root, audit, planned, "reconstruct-resume")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "publish", ["--interrupt-after", "1"])
        self.assertEqual(code, 3, result)
        code, result, _raw = invoke(root, audit, planned, "publish-resume")
        self.assertEqual(code, 0, result)
        before = (root / "book" / "0101.app-entry-0506" / "return.md").read_bytes()
        code, result, _raw = invoke(root, audit, planned, "retire", ["--interrupt-after", "0"])
        self.assertEqual(code, 3, result)
        self.assertTrue((root / "book" / "0101.app-entry-0506").is_dir())
        code, result, _raw = invoke(root, audit, planned, "retire-resume")
        self.assertEqual(code, 0, result)
        self.assertFalse((root / "book" / "0101.app-entry-0506").exists())
        code, result, _raw = invoke(root, audit, planned, "rollback-retire")
        self.assertEqual(code, 0, result)
        self.assertEqual((root / "book" / "0101.app-entry-0506" / "return.md").read_bytes(), before)
        code, result, _raw = invoke(root, audit, planned, "rollback-publish")
        self.assertEqual(code, 0, result)
        self.assertFalse((root / "book" / "0104.app-entry" / "05.06.return.md").exists())
        self.assertEqual((root / "book" / "0101.app-entry-0506" / "return.md").read_bytes(), before)
        self.assertEqual(len(body["records"]), 1)

    def test_partial_reconstruct_is_kept(self) -> None:
        root = work("partial-recon")
        audit, planned, _body = prepare(root, ["0101.app-entry-0506"])
        self.assertEqual(invoke(root, audit, planned, "init")[0], 0)
        self.assertEqual(invoke(root, audit, planned, "stage")[0], 0)
        tool.arm_fault("reconstruct", 0, "partial")
        code, result, _raw = invoke(root, audit, planned, "reconstruct")
        self.assertEqual(code, 3, result)
        partials = [path for path in (root / "staging" / "pages").rglob("*") if path.is_file()]
        self.assertTrue(partials)
        kept = partials[0].read_bytes()
        code, result, _raw = invoke(root, audit, planned, "reconstruct-resume")
        self.assertEqual(code, 2, result)
        self.assertIn("reconstruction bytes differ", result["correction"])
        self.assertEqual(partials[0].read_bytes(), kept)
        self.assertFalse((root / "staging" / "reconstruction-complete.json").exists())
        fresh = root / "staging-fresh"
        fresh.mkdir()
        write_auth(root / "auth.json", root / "book", planned, audit, root / "backup", fresh, root / "retired")
        code, result, _raw = run([
            "reconstruct", "--book", str(root / "book"), "--authorization", str(root / "auth.json"),
            "--audit", str(audit), "--plan", str(planned), "--backup", str(root / "backup"),
            "--staging", str(fresh), "--retired", str(root / "retired"),
        ])
        self.assertEqual(code, 0, result)
        self.assertEqual(partials[0].read_bytes(), kept)

    def test_partial_publish_is_kept(self) -> None:
        root = work("partial-publish")
        audit, planned, _body = prepare(root, ["0101.app-entry-0506"])
        for command in ("init", "stage", "reconstruct"):
            code, result, _raw = invoke(root, audit, planned, command)
            self.assertEqual(code, 0, result)
        tool.arm_fault("publish", 0, "partial")
        code, result, _raw = invoke(root, audit, planned, "publish")
        self.assertEqual(code, 3, result)
        code, result, _raw = invoke(root, audit, planned, "publish-resume")
        self.assertEqual(code, 2, result)
        self.assertIn("publication bytes differ", result["correction"])
        self.assertFalse((root / "backup" / "publish-complete.json").exists())

    def test_occupied_destination_and_archive(self) -> None:
        root = work("occupied")
        audit, planned, _body = prepare(root, ["0101.app-entry-0506"], plant="0104.not-staged")
        for command in ("init", "stage", "reconstruct"):
            self.assertEqual(invoke(root, audit, planned, command)[0], 0)
        code, result, _raw = invoke(root, audit, planned, "publish")
        self.assertEqual(code, 2, result)
        self.assertEqual(result["check"], "occupied-line")
        self.assertTrue((root / "book" / "0104.not-staged" / "note.txt").is_file())
        self.assertFalse((root / "backup" / "publish-complete.json").exists())

        root = work("occupied-archive")
        member = "0104.app-entry-0508"
        audit, planned, _body = prepare(root, [member])
        (root / "retired" / "occupants" / member).mkdir(parents=True)
        (root / "retired" / "occupants" / member / "keep.txt").write_bytes(b"archive\n")
        for command in ("init", "stage", "reconstruct"):
            self.assertEqual(invoke(root, audit, planned, command)[0], 0)
        code, result, _raw = invoke(root, audit, planned, "publish")
        self.assertEqual(code, 2, result)
        self.assertEqual(result["check"], "occupied-archive")
        self.assertEqual((root / "retired" / "occupants" / member / "keep.txt").read_bytes(), b"archive\n")
        self.assertTrue((root / "book" / member).is_dir())

    def test_changed_source_refuses_and_live_bytes_stay(self) -> None:
        root = work("changed-source")
        audit, _planned, _body = prepare(root, ["0101.app-entry-0506"])
        # prepare() already ran plan against the intact copy. Flip the copy after that.
        target = root / "book" / "0101.app-entry-0506" / "return.md"
        live = (LIVE / "0101.app-entry-0506" / "return.md").read_bytes()
        self.assertEqual(target.read_bytes(), live)
        flipped = bytearray(target.read_bytes())
        flipped[-1] ^= 0x01
        target.write_bytes(bytes(flipped))
        code, result, _raw = invoke(root, audit, root / "plan.json", "init")
        self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, root / "plan.json", "stage")
        self.assertEqual(code, 2, result)
        self.assertEqual(result["check"], "audit identity")
        self.assertFalse((root / "backup" / "stage-complete.json").exists())
        self.assertEqual((LIVE / "0101.app-entry-0506" / "return.md").read_bytes(), live)

    def test_rollback_hash_mismatch_stops(self) -> None:
        root = work("rollback-mismatch")
        audit, planned, _body = prepare(root, ["0101.app-entry-0506"])
        for command in ("init", "stage", "reconstruct", "publish", "retire"):
            code, result, _raw = invoke(root, audit, planned, command)
            self.assertEqual(code, 0, result)
        retired = root / "retired" / "originals" / "0101.app-entry-0506" / "return.md"
        if not retired.is_file():
            retired = root / "retired" / "occupants" / "0101.app-entry-0506" / "return.md"
        blob = bytearray(retired.read_bytes())
        blob[-1] ^= 0x01
        retired.write_bytes(bytes(blob))
        code, result, _raw = invoke(root, audit, planned, "rollback-retire")
        self.assertEqual(code, 2, result)
        self.assertFalse((root / "book" / "0101.app-entry-0506").exists())
        self.assertTrue(retired.is_file())


def tearDownModule() -> None:
    if PASS01.read_bytes() != PASS01_BEFORE:
        raise AssertionError("pass01 bytes changed during the disposable tests")


if __name__ == "__main__":
    unittest.main(verbosity=2)
