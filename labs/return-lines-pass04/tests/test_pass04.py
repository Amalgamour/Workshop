"""Bounded pass04 checks on disposable copies. These tests do not migrate the live book."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(r"D:\Git\lib-build")
LIVE = REPO / "00.kernel" / "00.00.10.work"
AUDIT_PATH = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
PASS01 = REPO / "labs" / "return-lines-pass01" / "return_lines.py"
PASS02 = REPO / "labs" / "return-lines-pass02" / "return_lines.py"
PASS03 = REPO / "labs" / "return-lines-pass03" / "return_lines.py"
TOOL_PATH = REPO / "labs" / "return-lines-pass04" / "return_lines.py"
EXTERNAL = Path(r"D:\librarian\temp\0521-0506")
sys.path.insert(0, str(REPO / "labs" / "return-lines-pass04"))
import return_lines as tool  # noqa: E402

P2 = tool.load_pass03().load_pass02()
LINES = P2.load_lines()
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
PASS01_BEFORE = PASS01.read_bytes()
PASS02_BEFORE = PASS02.read_bytes()
PASS03_BEFORE = PASS03.read_bytes()
OTHER_VOLUME = Path(r"C:\Users\misg\AppData\Local\Temp")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def invoke_tool(args: list[str], classify: str | None = None) -> tuple[int, dict, bytes]:
    buf = io.BytesIO()

    class Out:
        buffer = buf

    old = sys.stdout
    sys.stdout = Out()
    if classify:
        tool.classify_canonical(classify)
    else:
        tool.clear_classification()
    try:
        code = tool.main(args)
    finally:
        sys.stdout = old
        tool.clear_fault()
        tool.clear_classification()
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


def auth_args(root: Path, audit: Path, plan: Path) -> list[str]:
    return [
        "--authorization", str(root / "auth.json"),
        "--audit", str(audit),
        "--plan", str(plan),
        "--backup", str(root / "backup"),
        "--staging", str(root / "staging"),
        "--retired", str(root / "retired"),
    ]


def seed(root: Path, members: list[str]) -> tuple[Path, dict]:
    book = root / "book"
    copy_door(book)
    audit_path, body = write_audit(root, members)
    for record in body["records"]:
        copy_member(book, record["old_member"])
        if record.get("route") == "page-local-colab":
            copy_file(LIVE / record["target_return"], book / record["target_return"])
    return audit_path, body


def plan(root: Path, audit: Path) -> Path:
    out = root / "plan.json"
    code, body, _raw = invoke_tool(["plan", "--book", str(root / "book"), "--audit", str(audit), "--out", str(out)])
    if code != 0:
        raise AssertionError(body)
    return out


def release_body(book: Path, plan_path: Path, audit: Path, backup: Path, staging: Path, retired: Path,
                 text: str) -> dict:
    plan_raw = plan_path.read_bytes()
    audit_raw = audit.read_bytes()
    return {
        "audit_bytes": len(audit_raw),
        "audit_sha256": sha(audit_raw),
        "backup_root": str(backup),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(OPS),
        "plan_bytes": len(plan_raw),
        "plan_sha256": sha(plan_raw),
        "release_text": text,
        "retired_root": str(retired),
        "schema": "return-line-director-release/1",
        "staging_root": str(staging),
    }


def write_pair(root: Path, body: dict, auth_overrides: dict | None = None) -> None:
    raw = dump(body)
    release = root / "release.json"
    release.write_bytes(raw)
    auth = {key: body[key] for key in (
        "audit_bytes", "audit_sha256", "backup_root", "book", "book_path", "executor",
        "layout_sha256", "operations", "plan_bytes", "plan_sha256", "retired_root", "staging_root",
    )}
    auth.update({
        "release_bytes": len(raw),
        "release_path": str(release),
        "release_sha256": sha(raw),
        "schema": "return-line-recorded-release/1",
        "synthetic": False,
    })
    if auth_overrides:
        auth.update(auth_overrides)
    (root / "auth.json").write_bytes(dump(auth))


def write_fixture(root: Path, book: Path, plan_path: Path, audit: Path, **overrides) -> None:
    raw = audit.read_bytes()
    body = {
        "audit_bytes": len(raw),
        "audit_sha256": sha(raw),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(OPS),
        "plan_sha256": sha(plan_path.read_bytes()),
        "release": P2.RELEASE_TEXT,
        "retired_root": str(root / "retired"),
        "schema": "return-line-authorization/1",
        "staging_root": str(root / "staging"),
        "synthetic": True,
    }
    body.update(overrides)
    (root / "auth.json").write_bytes(dump(body))


TEST_TEXT = "TEST RECORDING for a disposable copy. Not a Director release. Not live authority.\n"
ALT_TEXT = "SECOND TEST RECORDING. Different bytes. Still not a Director release.\n"


def prepare_recorded(root: Path, members: list[str], text: str = TEST_TEXT):
    audit, body = seed(root, members)
    planned = plan(root, audit)
    write_pair(root, release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", text))
    return audit, planned, body


def invoke(root: Path, audit: Path, plan_path: Path, command: str, extra: list[str] | None = None,
           classify: bool = False) -> tuple[int, dict, bytes]:
    args = [command, "--book", str(root / "book"), *auth_args(root, audit, plan_path)]
    if command == "init":
        args = ["init", "--book", str(root / "book"), "--name", "00.00.10.work", *auth_args(root, audit, plan_path)]
    if extra:
        args.extend(extra)
    return invoke_tool(args, str(root / "book") if classify else None)


class Pass04Tests(unittest.TestCase):
    def test_pins_and_no_bypass_flag(self) -> None:
        self.assertEqual(sha(PASS03.read_bytes()), tool.PASS03_SHA)
        self.assertEqual(len(PASS03.read_bytes()), tool.PASS03_BYTES)
        self.assertEqual(sha(PASS02.read_bytes()), tool.load_pass03().PASS02_SHA)
        self.assertEqual(len(PASS02.read_bytes()), tool.load_pass03().PASS02_BYTES)
        text = TOOL_PATH.read_text(encoding="utf-8")
        self.assertNotIn("--force", text)
        self.assertNotIn("--allow-live", text)
        self.assertNotIn("--designate", text)
        self.assertNotIn("designate_live", text)
        self.assertNotIn("this pack does not execute the canonical live book", text)
        self.assertNotIn("this pack stays refused", text)
        self.assertNotIn("bounded tooling build", text)
        self.assertNotIn("== 83", text)
        self.assertNotIn("== 18", text)
        self.assertNotIn("\r", text)
        predecessor = PASS03.read_text(encoding="utf-8")
        self.assertIn("this pack does not execute the canonical live book", predecessor)
        readme = (REPO / "labs" / "return-lines-pass04" / "README.md").read_text(encoding="utf-8")
        self.assertIn("remaining audited old member", readme)
        self.assertNotIn("only colliding", readme)
        self.assertFalse(hasattr(tool, "designate_live"))

    def test_no_unconditional_canonical_deny(self) -> None:
        text = TOOL_PATH.read_text(encoding="utf-8")
        inspect = text.split("def inspect(", 1)[1].split("\ndef ", 1)[0]
        recorded_at = inspect.index("if schema == RECORDED_SCHEMA")
        head = inspect[:recorded_at]
        fixture_at = head.index("if schema == FIXTURE_SCHEMA")
        self.assertNotIn("live execution", head)
        self.assertNotIn("is_real_live", text)
        self.assertNotIn("does not execute", head)
        self.assertNotIn("is_canonical", head[:fixture_at])
        self.assertIn("is_canonical", head[fixture_at:])
        self.assertNotIn("is_canonical", inspect[recorded_at:])
        refusal = text.split("def live_refusal", 1)[1].split("\ndef ", 1)[0]
        self.assertNotIn("refuse", refusal)
        self.assertNotIn("LineError", refusal)
        self.assertNotIn("is_canonical", refusal)
        tool.live_refusal(str(LIVE))
        pass02 = tool.load_pass03().load_pass02()
        pass02.live_refusal(str(LIVE))
        self.assertIs(pass02.live_refusal, tool.live_refusal)
        self.assertIs(pass02.require_authorization, tool.require_authorization)
        self.assertIs(pass02.patched_assert, tool.patched_assert)
        self.assertIs(pass02.needs_auth, tool.needs_auth)
        self.assertIs(pass02.load_lines().assert_mutable, tool.patched_assert)
        with self.assertRaises(ValueError):
            tool.classify_canonical(str(LIVE))

    def test_live_book_absent_authority_is_not_a_veto(self) -> None:
        root = work("live-absent")
        before = (LIVE / "0100.band.returns" / "01.md").read_bytes()
        missing = root / "missing-authorization.json"
        code, body, _raw = invoke_tool([
            "preflight", "--book", str(LIVE), "--authorization", str(missing),
            "--audit", str(AUDIT_PATH), "--plan", str(root / "plan.json"),
            "--backup", str(root / "backup"), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ])
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "authorization")
        self.assertIn("authorization is absent", body["correction"])
        self.assertIn("0521.return-placement/05.06", body["correction"])
        self.assertNotIn("does not execute", body["correction"])
        self.assertNotIn("designated-live", body["correction"])
        self.assertFalse((LIVE / "return-line-layout.json").exists())
        self.assertEqual((LIVE / "0100.band.returns" / "01.md").read_bytes(), before)
        self.assertFalse((root / "backup" / "stage-journal.json").exists())

    def test_classified_canonical_uses_the_same_recorded_validator(self) -> None:
        root = work("classified")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        write_fixture(root, root / "book", planned, audit)
        code, body, _raw = invoke(root, audit, planned, "init", classify=True)
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "return-line-authorization/1")
        self.assertIn("fixture authorization cannot authorize the canonical book", body["correction"])
        self.assertIn("0521.return-placement/05.06", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        write_pair(root, release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", TEST_TEXT))
        code, body, _raw = invoke_tool(
            ["preflight", "--book", str(root / "book"), *auth_args(root, audit, planned)],
            str(root / "book"),
        )
        self.assertEqual(code, 0, body)
        self.assertEqual(body["check"], "readiness")
        self.assertFalse(body["detail"]["mutated"])
        self.assertFalse(body["detail"]["executed"])
        self.assertFalse(body["detail"]["live_execution"])
        self.assertTrue(body["detail"]["canonical"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        code, body, _raw = invoke(root, audit, planned, "init", classify=True)
        self.assertEqual(code, 0, body)
        self.assertTrue((root / "book" / "return-line-layout.json").is_file())
        self.assertFalse((LIVE / "return-line-layout.json").exists())

    def test_fixture_still_authorizes_ordinary_copy(self) -> None:
        root = work("fixture-ordinary")
        audit, _body = seed(root, ["0101.app-entry-0506"])
        planned = plan(root, audit)
        write_fixture(root, root / "book", planned, audit)
        code, body, _raw = invoke_tool(["preflight", "--book", str(root / "book"), *auth_args(root, audit, planned)])
        self.assertEqual(code, 0, body)
        self.assertEqual(body["check"], "readiness")
        self.assertFalse(body["detail"]["mutated"])
        self.assertFalse(body["detail"]["canonical"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        code, body, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 0, body)
        self.assertTrue((root / "book" / "return-line-layout.json").is_file())

    def test_recorded_copy_needs_no_designation(self) -> None:
        root = work("recorded-copy")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        code, body, _raw = invoke_tool(["preflight", "--book", str(root / "book"), *auth_args(root, audit, planned)])
        self.assertEqual(code, 0, body)
        self.assertFalse(body["detail"]["canonical"])
        self.assertFalse(body["detail"]["executed"])
        code, body, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 0, body)
        self.assertTrue((root / "book" / "return-line-layout.json").is_file())

    def test_cli_recorded_init_without_designation(self) -> None:
        root = work("cli-init")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        proc = subprocess.run(
            [sys.executable, "-B", str(TOOL_PATH), "init", "--book", str(root / "book"), "--name", "00.00.10.work",
             *auth_args(root, audit, planned)],
            cwd=str(REPO), capture_output=True, env=ENV,
        )
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(proc.returncode, 0, body)
        self.assertTrue((root / "book" / "return-line-layout.json").is_file())
        self.assertNotIn(b"designate", proc.stdout)
        self.assertFalse((LIVE / "return-line-layout.json").exists())

    def test_adopt_refused(self) -> None:
        code, body, _raw = invoke_tool(["adopt"])
        self.assertEqual(code, 2)
        self.assertEqual(body["check"], "successor command")
        self.assertFalse((LIVE / "return-line-layout.json").exists())

    def test_synthetic_recorded_release_refuses(self) -> None:
        root = work("synthetic-recorded")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        auth = json.loads((root / "auth.json").read_bytes())
        auth["synthetic"] = True
        (root / "auth.json").write_bytes(dump(auth))
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 2, body)
        self.assertIn("synthetic fixture is not a recorded release", body["correction"])
        self.assertIn("0521.return-placement/05.06", body["correction"])
        self.assertNotIn("designated-live", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())

    def test_candidate_is_not_authority(self) -> None:
        root = work("candidate")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        release = json.loads((root / "release.json").read_bytes())
        candidate = dict(release)
        candidate["schema"] = "return-line-release-candidate/1"
        candidate["active"] = False
        candidate["unresolved"] = ["Director has not approved a path."]
        (root / "auth.json").write_bytes(dump(candidate))

        def listed() -> list[str]:
            return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.name != "auth.json")

        before = listed()
        code, body, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "return-line-release-candidate/1")
        self.assertIn("candidate is not authority", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        code, body, _raw = invoke_tool(["preflight", "--book", str(root / "book"), *auth_args(root, audit, planned)])
        self.assertEqual(code, 2, body)
        self.assertIn("candidate is not authority", body["correction"])
        candidate["active"] = True
        (root / "auth.json").write_bytes(dump(candidate))
        code, body, _raw = invoke(root, audit, planned, "init", classify=True)
        self.assertEqual(code, 2, body)
        self.assertIn("candidate claims active authority", body["correction"])
        self.assertEqual(before, listed())

    def test_label_alone_is_not_authority(self) -> None:
        root = work("label-alone")
        copy_door(root / "book")
        (root / "auth.json").write_bytes(dump({"executor": "Codex Prime", "synthetic": False}))
        (root / "audit.json").write_bytes(b"{}\n")
        (root / "plan.json").write_bytes(b"{}\n")
        code, body, _raw = invoke_tool([
            "init", "--book", str(root / "book"), "--name", "00.00.10.work",
            *auth_args(root, root / "audit.json", root / "plan.json"),
        ])
        self.assertEqual(code, 2, body)
        self.assertFalse((root / "book" / "return-line-layout.json").exists())

    def test_changed_plan_and_pin_conflict(self) -> None:
        root = work("plan-pin")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        original = planned.read_bytes()
        flipped = bytearray(original)
        flipped[-2] ^= 0x01
        planned.write_bytes(bytes(flipped))
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "return-line-plan/1")
        self.assertIn("plan hash or length", body["correction"])
        planned.write_bytes(original)
        auth = json.loads((root / "auth.json").read_bytes())
        auth["plan_sha256"] = "0" * 64
        (root / "auth.json").write_bytes(dump(auth))
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 2, body)
        self.assertIn("authorization binding disagrees with the release file", body["correction"])
        write_pair(root, release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", TEST_TEXT))
        release = json.loads((root / "release.json").read_bytes())
        release["release_text"] = release["release_text"] + "edited\n"
        (root / "release.json").write_bytes(dump(release))
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 2, body)
        self.assertIn("release bytes no longer match", body["correction"])

    def test_two_release_texts_and_invocation_path(self) -> None:
        root = work("two-texts")
        audit, _body = seed(root, ["0101.app-entry-0506"])
        planned = plan(root, audit)
        for text in (TEST_TEXT, ALT_TEXT):
            write_pair(root, release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", text))
            code, body, _raw = invoke(root, audit, planned, "preflight")
            self.assertEqual(code, 0, body)
            self.assertFalse(body["detail"]["executed"])
        invocation = LIVE / "0521.return-placement" / "evidence" / "build05.05" / "invocation.txt"
        write_pair(
            root,
            release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", TEST_TEXT),
            {"release_path": str(invocation), "release_sha256": sha(invocation.read_bytes()), "release_bytes": invocation.stat().st_size},
        )
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 2, body)
        self.assertIn("inside the live work book", body["correction"])

    def test_wrong_operation_volume_and_missing_parent(self) -> None:
        root = work("operation-volume")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        auth = json.loads((root / "auth.json").read_bytes())
        release = json.loads((root / "release.json").read_bytes())
        release["operations"] = ["stage"]
        auth["operations"] = ["stage"]
        raw = dump(release)
        (root / "release.json").write_bytes(raw)
        auth["release_sha256"] = sha(raw)
        auth["release_bytes"] = len(raw)
        (root / "auth.json").write_bytes(dump(auth))
        code, body, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 2, body)
        self.assertIn("not authorized", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        write_pair(root, release_body(
            root / "book", planned, audit, OTHER_VOLUME, root / "staging", root / "retired", TEST_TEXT,
        ))
        code, body, _raw = invoke_tool([
            "init", "--book", str(root / "book"), "--name", "00.00.10.work",
            "--authorization", str(root / "auth.json"), "--audit", str(audit), "--plan", str(planned),
            "--backup", str(OTHER_VOLUME), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ])
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "filesystem")
        self.assertIn("not on the book volume", body["correction"])
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        missing_root = root.parent / f"{root.name}-missing-parent" / "backup"
        self.assertFalse(missing_root.parent.exists())
        write_pair(root, release_body(
            root / "book", planned, audit, missing_root, root / "staging", root / "retired", TEST_TEXT,
        ))
        code, body, _raw = invoke_tool([
            "preflight", "--book", str(root / "book"),
            "--authorization", str(root / "auth.json"), "--audit", str(audit), "--plan", str(planned),
            "--backup", str(missing_root), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ])
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "filesystem")
        self.assertIn("parent is missing", body["correction"])
        self.assertFalse(missing_root.parent.exists())
        self.assertFalse((root / "book" / "return-line-layout.json").exists())

    def test_stale_source_refuses_before_layout(self) -> None:
        root = work("stale")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        target = root / "book" / "0101.app-entry-0506" / "return.md"
        live = (LIVE / "0101.app-entry-0506" / "return.md").read_bytes()
        self.assertEqual(target.read_bytes(), live)
        flipped = bytearray(target.read_bytes())
        flipped[-1] ^= 0x01
        target.write_bytes(bytes(flipped))
        code, body, _raw = invoke(root, audit, planned, "init")
        self.assertEqual(code, 2, body)
        self.assertEqual(body["check"], "stale source")
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        self.assertEqual((LIVE / "0101.app-entry-0506" / "return.md").read_bytes(), live)

    def test_flow_interrupt_partial_and_rollback(self) -> None:
        members = ["0101.app-entry-0506", "0154.colab-support-first-0501", "0165.bench-method-colab-0501"]
        root = work("recorded-flow")
        audit, planned, body = prepare_recorded(root, members)
        code, result, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["detail"]["mutated"], False)
        self.assertFalse((root / "book" / "return-line-layout.json").exists())
        for command in ("init", "stage", "reconstruct", "publish", "retire"):
            code, result, _raw = invoke(root, audit, planned, command)
            self.assertEqual(code, 0, result)
            self.assertEqual(result["detail"]["accepted"], False)
            self.assertEqual(result["detail"]["published"], False)
        self.assertEqual(result["detail"]["remaining_old_members"], 0)
        for record in body["records"]:
            self.assertFalse((root / "book" / record["old_member"]).exists())
        self.assertFalse((root / "book" / "0110.colab-tools" / "05.01.return.md").exists())
        self.assertEqual(
            (root / "book" / "0701.bench-method" / "05.01.return.md").read_bytes(),
            (LIVE / "0701.bench-method" / "05.01.return.md").read_bytes(),
        )
        code, looked, _raw = invoke_tool(["lookup", "--book", str(root / "book"), "--member", "0154.colab-support-first-0501"])
        self.assertEqual(code, 1, looked)
        self.assertIsNone(looked["descriptor"]["return_sha256"])
        self.assertEqual(looked["detail"]["retained_original"]["book_member_present"], False)
        code, looked, _raw = invoke_tool(["descriptor", "--book", str(root / "book"), "--member", "0101.app-entry-0506"])
        self.assertEqual(code, 0, looked)
        self.assertEqual(set(looked), set(LINES.DESCRIPTOR_KEYS))
        self.assertEqual(looked["verification"]["tool_path"], "labs/return-lines-pass01/return_lines.py")

        root = work("interrupt")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        self.assertEqual(invoke(root, audit, planned, "init")[0], 0)
        self.assertEqual(invoke(root, audit, planned, "stage")[0], 0)
        self.assertEqual(invoke(root, audit, planned, "reconstruct")[0], 0)
        code, result, _raw = invoke(root, audit, planned, "publish", ["--interrupt-after", "1"])
        self.assertEqual(code, 3, result)
        code, result, _raw = invoke(root, audit, planned, "publish-resume")
        self.assertEqual(code, 0, result)
        fresh = work("partial")
        audit, planned, _body = prepare_recorded(fresh, ["0101.app-entry-0506"])
        for command in ("init", "stage", "reconstruct"):
            self.assertEqual(invoke(fresh, audit, planned, command)[0], 0)
        code, result, _raw = run_armed(fresh, audit, planned)
        self.assertEqual(code, 3, result)
        code, result, _raw = invoke(fresh, audit, planned, "publish-resume")
        self.assertEqual(code, 2, result)
        self.assertIn("publication bytes differ", result["correction"])

        root = work("rollback")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        before = (root / "book" / "0101.app-entry-0506" / "return.md").read_bytes()
        for command in ("init", "stage", "reconstruct", "publish", "retire"):
            code, result, _raw = invoke(root, audit, planned, command)
            self.assertEqual(code, 0, result)
        code, result, _raw = invoke(root, audit, planned, "rollback-retire")
        self.assertEqual(code, 0, result)
        self.assertEqual((root / "book" / "0101.app-entry-0506" / "return.md").read_bytes(), before)
        code, result, _raw = invoke(root, audit, planned, "rollback-publish")
        self.assertEqual(code, 0, result)
        self.assertFalse((root / "book" / "0104.app-entry" / "05.06.return.md").exists())
        self.assertEqual((root / "book" / "0101.app-entry-0506" / "return.md").read_bytes(), before)

    def test_consistent_new_release_replaces_the_pin(self) -> None:
        root = work("new-pin")
        audit, planned, _body = prepare_recorded(root, ["0101.app-entry-0506"])
        code, _body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 0)
        edited = release_body(root / "book", planned, audit, root / "backup", root / "staging", root / "retired", ALT_TEXT)
        write_pair(root, edited)
        code, body, _raw = invoke(root, audit, planned, "preflight")
        self.assertEqual(code, 0, body)
        self.assertNotEqual(TEST_TEXT, ALT_TEXT)


def run_armed(root: Path, audit: Path, plan_path: Path) -> tuple[int, dict, bytes]:
    buf = io.BytesIO()

    class Out:
        buffer = buf

    old = sys.stdout
    sys.stdout = Out()
    tool.clear_classification()
    tool.arm_fault("publish", 0, "partial")
    try:
        code = tool.main(["publish", "--book", str(root / "book"), *auth_args(root, audit, plan_path)])
    finally:
        sys.stdout = old
        tool.clear_fault()
        tool.clear_classification()
    raw = buf.getvalue()
    body = json.loads(raw.decode("utf-8")) if raw.strip() else {}
    return code, body, raw


def tearDownModule() -> None:
    if PASS01.read_bytes() != PASS01_BEFORE or PASS02.read_bytes() != PASS02_BEFORE or PASS03.read_bytes() != PASS03_BEFORE:
        raise AssertionError("pass01, pass02, or pass03 bytes changed during the disposable tests")
    if (LIVE / "return-line-layout.json").exists():
        raise AssertionError("live layout appeared during the disposable tests")


if __name__ == "__main__":
    unittest.main(verbosity=2)
