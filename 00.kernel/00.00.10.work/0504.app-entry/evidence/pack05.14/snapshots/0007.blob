#!/usr/bin/env python3
"""Disposable checks for the development pack-tool entry.

The suite copies the entry and the pinned tools. It does not hard-code a
machine path. The accepted assembler's own tests are not modified.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
REAL_GIT = shutil.which("git.exe") or shutil.which("git")
CHECKER_SHA = "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d"
ASSEMBLY_SHA = "75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c"
SOURCES = (
    "app/librarian.py",
    "app/prime_tools.py",
    "app/prime-tools.json",
    "app/README.md",
    "app/context.py",
    "app/tests/test_entry.py",
    "labs/pack-custody-pass01/pack_check.py",
    "labs/pack-assembly-pass01/pack_assembly.py",
    "labs/pack-assembly-pass01/tests/test_pack_assembly.py",
)
COPY = (
    "app/librarian.py",
    "app/prime_tools.py",
    "app/prime-tools.json",
    "labs/pack-custody-pass01/pack_check.py",
    "labs/pack-assembly-pass01/pack_assembly.py",
)
BANNED = {
    "fetch", "pull", "push", "ls-remote", "clone", "checkout", "config",
    "status", "add", "commit", "reset", "clean", "update-index", "update-ref",
    "symbolic-ref", "show",
}
TEXT = "\n".join([
    "Keep this sentence exact.",
    ">run.0504.05.08",
    "```",
    "print('do not run')",
    "```",
])


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_originals() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in SOURCES}


ORIGINALS = find_originals()


class PrimeToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="wf0508-")
        self.root = Path(self.tmp.name)
        self.junctions: list[Path] = []
        self.old_path = os.environ.get("PATH", "")
        self.wrap = self.root / "wrap"
        self.wrap.mkdir()
        (self.wrap / "gitwrap.py").write_bytes(WRAPPER.encode("utf-8"))
        cmd = '@echo off\r\n"' + PYTHON + '" -B "%~dp0gitwrap.py" %*\r\n'
        (self.wrap / "git.cmd").write_bytes(cmd.encode("ascii"))
        os.environ["PATH"] = str(self.wrap) + os.pathsep + self.old_path
        os.environ["PACK_PRIME_TOOLS_REAL_GIT"] = REAL_GIT or ""
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        self.log = self.wrap / "git.log"
        self.sentinel = self.root / "ran.txt"

    def tearDown(self) -> None:
        os.environ["PATH"] = self.old_path
        for link in self.junctions:
            if os.path.lexists(link):
                os.rmdir(link)
        self.tmp.cleanup()
        for rel, data in ORIGINALS.items():
            self.assertEqual((REPO / rel).read_bytes(), data, rel)

    def copy_code(self) -> Path:
        code = self.root / "code"
        for rel in COPY:
            dest = code / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(ORIGINALS[rel])
        return code

    def app(self, code: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [PYTHON, "-B", str(code / "app" / "librarian.py"), *args],
            capture_output=True,
            env=env,
        )

    def tool(self, code: Path, rel: str, *args: str) -> subprocess.CompletedProcess[bytes]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [PYTHON, "-B", str(code / rel), *args],
            capture_output=True,
            env=env,
        )

    def checker(self, code: Path) -> Path:
        return code / "labs" / "pack-custody-pass01" / "pack_check.py"

    def assembler(self, code: Path) -> str:
        return "labs/pack-assembly-pass01/pack_assembly.py"

    def git(self, repo: Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
        if not REAL_GIT:
            self.fail("git was not found")
        return subprocess.run(
            [REAL_GIT, "-C", str(repo), *args],
            input=input_bytes,
            capture_output=True,
            check=True,
        )

    def init_repo(self) -> Path:
        repo = self.root / "repo"
        repo.mkdir()
        self.git(repo, "init", "-q")
        for key, value in (
            ("user.email", "pack-entry@example.invalid"),
            ("user.name", "pack-entry-test"),
            ("core.autocrlf", "false"),
            ("commit.gpgsign", "false"),
        ):
            self.git(repo, "config", key, value)
        return repo

    def commit_worktree(self, repo: Path, message: str) -> str:
        self.git(repo, "-c", "commit.gpgsign=false", "add", "-A")
        self.git(repo, "-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
        return self.git(repo, "rev-parse", "HEAD").stdout.decode().strip()

    def git_state(self, repo: Path) -> tuple[bytes, bytes, bytes, bytes]:
        env = os.environ.copy()
        env["GIT_OPTIONAL_LOCKS"] = "0"
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["PATH"] = self.old_path

        def run(*args: str) -> bytes:
            assert REAL_GIT
            return subprocess.run(
                [REAL_GIT, "--no-optional-locks", "-C", str(repo), *args],
                capture_output=True,
                check=True,
                env=env,
            ).stdout

        return (
            run("rev-parse", "HEAD"),
            run("for-each-ref", "--format=%(objectname) %(refname)"),
            run("ls-files", "--stage"),
            run("status", "--porcelain=v1", "-uall"),
        )

    def request_bytes(self, revision: str, paths: list[str]) -> bytes:
        body = {
            "schema": "pack-assembly-request/1",
            "template": "pack-assembly-draft/1",
            "title": "Fixture draft",
            "date": "2026-10-27",
            "author": "Codex Prime",
            "origin": {"book": "00.00.10.work", "page": "0504.app-entry", "batch": "05.08"},
            "identity": {"book": "00.00.10.work", "pppp": "0504", "keyword": "fixture", "batch": "05.01"},
            "executor": "Fixture executor",
            "reviewer": "Codex Prime",
            "goal": "Build a disposable draft.",
            "scope": ["the disposable pack directory"],
            "revision": revision,
            "paths": paths,
            "instructions": [{"nn": "01", "heading": "Keep the sentence", "text": TEXT}],
            "evidence": "A disposable transcript.",
            "dependencies": {"state": "unresolved"},
            "return_destination": {"state": "unresolved"},
        }
        return (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    def write_request(self, raw: bytes) -> Path:
        path = self.root / "request.json"
        path.write_bytes(raw)
        return path

    def log_rows(self) -> list[dict]:
        if not self.log.exists():
            return []
        return [ast.literal_eval(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def assert_git_read_only(self) -> None:
        rows = self.log_rows()
        self.assertTrue(rows)
        verbs = []
        for row in rows:
            self.assertEqual(row["env"]["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(row["env"]["GIT_TERMINAL_PROMPT"], "0")
            self.assertFalse(set(row["argv"]) & BANNED)
            verbs.append(row["argv"][3])
        self.assertTrue(set(verbs) <= {"rev-parse", "cat-file"})
        self.assertIn("cat-file", verbs)

    def argparse_error(self, stderr: bytes) -> bytes:
        lines = [line for line in stderr.splitlines() if b": error:" in line]
        self.assertEqual(len(lines), 1, stderr)
        return lines[0].replace(b"librarian.py", b"pack_assembly.py")

    def assert_no_traceback(self, proc: subprocess.CompletedProcess[bytes]) -> None:
        self.assertNotIn(b"Traceback", proc.stdout + proc.stderr)

    def assert_stop(self, proc: subprocess.CompletedProcess[bytes], text: str) -> None:
        self.assert_no_traceback(proc)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, b"")
        self.assertTrue(proc.stderr.startswith(b"stop: "), proc.stderr)
        self.assertIn(text.encode("utf-8"), proc.stderr)

    def tree(self, root: Path) -> dict[str, bytes]:
        found = {}
        for path in root.rglob("*"):
            if path.is_file():
                found[path.relative_to(root).as_posix()] = path.read_bytes()
        return found

    def prepare(self) -> tuple[Path, Path, Path, str]:
        code = self.copy_code()
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one\n")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["keep.txt"]))
        return code, repo, request, commit

    def preview(self, code: Path, request: Path, repo: Path) -> tuple[subprocess.CompletedProcess[bytes], subprocess.CompletedProcess[bytes]]:
        user = ["--request", str(request), "--repo", str(repo), "--json"]
        app_proc = self.app(code, "pack-preview", *user)
        direct = self.tool(
            code, self.assembler(code), "preview", *user, "--checker", str(self.checker(code)),
        )
        return app_proc, direct

    def test_sources_match_the_declaration(self) -> None:
        document = json.loads(ORIGINALS["app/prime-tools.json"].decode("utf-8"))
        self.assertEqual(document["tools"]["pack_check"]["sha256"], CHECKER_SHA)
        self.assertEqual(document["tools"]["pack_assembly"]["sha256"], ASSEMBLY_SHA)
        self.assertEqual(sha256(ORIGINALS["labs/pack-custody-pass01/pack_check.py"]), CHECKER_SHA)
        self.assertEqual(sha256(ORIGINALS["labs/pack-assembly-pass01/pack_assembly.py"]), ASSEMBLY_SHA)
        text = ORIGINALS["app/prime_tools.py"].decode("utf-8")
        for banned in ("subprocess", "os.system", "shell=True", "Popen"):
            self.assertNotIn(banned, text)

    def test_preview_assemble_verify_and_pack_check_match_direct(self) -> None:
        code, repo, request, _commit = self.prepare()
        before = self.git_state(repo)
        app_preview, direct_preview = self.preview(code, request, repo)
        self.assert_no_traceback(app_preview)
        self.assertEqual(app_preview.returncode, 0)
        self.assertEqual(app_preview.stdout, direct_preview.stdout)
        self.assertEqual(app_preview.stderr, direct_preview.stderr)
        again = self.app(code, "pack-preview", "--request", str(request), "--repo", str(repo), "--json")
        self.assertEqual(again.stdout, app_preview.stdout)
        text_app = self.app(code, "pack-preview", "--request", str(request), "--repo", str(repo))
        text_direct = self.tool(
            code, self.assembler(code), "preview",
            "--request", str(request), "--repo", str(repo), "--checker", str(self.checker(code)),
        )
        self.assertEqual(text_app.returncode, 0)
        self.assertEqual(text_app.stdout, text_direct.stdout)
        self.assertEqual(text_app.stderr, text_direct.stderr)
        digest = json.loads(app_preview.stdout.decode("utf-8"))["digest"]
        out_app = self.root / "pack-app"
        out_direct = self.root / "pack-direct"
        user = [
            "--request", str(request), "--repo", str(repo),
            "--output", str(out_app), "--digest", digest, "--json",
        ]
        app_pack = self.app(code, "pack-assemble", *user)
        direct_user = [
            "--request", str(request), "--repo", str(repo),
            "--output", str(out_direct), "--digest", digest, "--json",
            "--checker", str(self.checker(code)),
        ]
        direct_pack = self.tool(code, self.assembler(code), "assemble", *direct_user)
        self.assertEqual(app_pack.returncode, 0, app_pack.stderr)
        self.assertEqual(direct_pack.returncode, 0, direct_pack.stderr)
        self.assertEqual(app_pack.stderr, b"")
        left = json.loads(app_pack.stdout.decode("utf-8"))
        right = json.loads(direct_pack.stdout.decode("utf-8"))
        self.assertEqual(left.pop("target"), str(out_app))
        self.assertEqual(right.pop("target"), str(out_direct))
        self.assertEqual(left, right)
        self.assertEqual(self.tree(out_app), self.tree(out_direct))
        draft = (out_app / "05.01.md").read_bytes()
        self.assertIn(b"state: draft", draft)
        self.assertIn(b"Release: PENDING.", draft)
        self.assertIn(b">run.0504.05.08", draft)
        self.assertFalse(self.sentinel.exists())
        app_verify = self.app(code, "pack-verify", "--pack", str(out_app), "--json")
        direct_verify = self.tool(
            code, self.assembler(code), "verify",
            "--pack", str(out_app), "--json", "--checker", str(self.checker(code)),
        )
        self.assertEqual(app_verify.returncode, 0)
        self.assertEqual(app_verify.stdout, direct_verify.stdout)
        self.assertEqual(app_verify.stderr, direct_verify.stderr)
        logged = len(self.log_rows())
        manifest = out_app / "source-manifest.json"
        app_check = self.app(
            code, "pack-check", "--format", "prime-pack-sources/1",
            "--manifest", str(manifest), "--json",
        )
        direct_check = self.tool(
            code, "labs/pack-custody-pass01/pack_check.py",
            "--format", "prime-pack-sources/1", "--manifest", str(manifest), "--json",
        )
        self.assertEqual(app_check.returncode, 0)
        self.assertEqual(app_check.stdout, direct_check.stdout)
        self.assertEqual(app_check.stderr, direct_check.stderr)
        self.assertEqual(len(self.log_rows()), logged)
        self.assertEqual(self.git_state(repo), before)
        self.assertEqual((repo / "keep.txt").read_bytes(), b"one\n")
        self.assert_git_read_only()

    def test_snapshot_mutation_fails_and_keeps_the_receipt(self) -> None:
        code, repo, request, _commit = self.prepare()
        preview, _direct = self.preview(code, request, repo)
        digest = json.loads(preview.stdout.decode("utf-8"))["digest"]
        output = self.root / "pack"
        assembled = self.app(
            code, "pack-assemble", "--request", str(request), "--repo", str(repo),
            "--output", str(output), "--digest", digest, "--json",
        )
        self.assertEqual(assembled.returncode, 0, assembled.stderr)
        receipt = (output / "completion-receipt.json").read_bytes()
        blob = output / "snapshots" / "0001.blob"
        raw = blob.read_bytes()
        blob.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        app_verify = self.app(code, "pack-verify", "--pack", str(output), "--json")
        direct_verify = self.tool(
            code, self.assembler(code), "verify",
            "--pack", str(output), "--json", "--checker", str(self.checker(code)),
        )
        self.assertEqual(app_verify.returncode, 1)
        self.assertEqual(app_verify.stdout, direct_verify.stdout)
        self.assertEqual(app_verify.stderr, direct_verify.stderr)
        report = json.loads(app_verify.stdout.decode("utf-8"))
        self.assertEqual(report["result"], "mismatch")
        self.assertEqual((output / "completion-receipt.json").read_bytes(), receipt)
        app_check = self.app(
            code, "pack-check", "--format", "prime-pack-sources/1",
            "--manifest", str(output / "source-manifest.json"), "--json",
        )
        direct_check = self.tool(
            code, "labs/pack-custody-pass01/pack_check.py",
            "--format", "prime-pack-sources/1",
            "--manifest", str(output / "source-manifest.json"), "--json",
        )
        self.assertEqual(app_check.returncode, 1)
        self.assertEqual(app_check.stdout, direct_check.stdout)

    def test_wrong_hash_and_missing_tool_write_nothing(self) -> None:
        code, repo, request, _commit = self.prepare()
        output = self.root / "pack"
        checker = self.checker(code)
        raw = checker.read_bytes()
        checker.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        proc = self.app(
            code, "pack-preview", "--request", str(request), "--repo", str(repo), "--json",
        )
        self.assert_stop(proc, "pinned tool hash does not match: pack_check")
        self.assertFalse(output.exists())
        checker.write_bytes(raw)
        declaration = code / "app" / "prime-tools.json"
        document = json.loads(declaration.read_text(encoding="utf-8"))
        document["tools"]["pack_assembly"]["sha256"] = "0" * 64
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = self.app(
            code, "pack-assemble", "--request", str(request), "--repo", str(repo),
            "--output", str(output), "--digest", "0" * 64, "--json",
        )
        self.assert_stop(proc, "prime tool declaration does not match the pinned tools")
        self.assertFalse(output.exists())
        code = self.copy_code()
        (code / "labs" / "pack-assembly-pass01" / "pack_assembly.py").unlink()
        proc = self.app(
            code, "pack-assemble", "--request", str(request), "--repo", str(repo),
            "--output", str(output), "--digest", "0" * 64, "--json",
        )
        self.assert_stop(proc, "pinned tool is missing: pack_assembly")
        self.assertFalse(output.exists())

    def test_path_escape_is_refused(self) -> None:
        code = self.copy_code()
        outside = self.root / "outside.py"
        script = "from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(self.sentinel)
        outside.write_bytes(script.encode("utf-8"))
        declaration = code / "app" / "prime-tools.json"
        document = json.loads(declaration.read_bytes().decode("utf-8"))
        document["tools"]["pack_check"]["path"] = "../outside.py"
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = self.app(code, "pack-check", "--format", "prime-pack-sources/1", "--manifest", str(self.root / "no.json"), "--json")
        self.assert_stop(proc, "tool path escapes the code root")
        self.assertFalse(self.sentinel.exists())
        document["tools"]["pack_check"]["path"] = "C:/Windows/notepad.exe"
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = self.app(code, "pack-check", "--format", "tsv", "--manifest", str(self.root / "no.tsv"), "--root", str(self.root))
        self.assert_stop(proc, "tool path escapes the code root")
        document["tools"]["pack_check"]["path"] = "labs\\pack-custody-pass01\\pack_check.py"
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = self.app(code, "pack-check", "--format", "prime-pack-sources/1", "--manifest", str(self.root / "no.json"))
        self.assert_stop(proc, "tool path escapes the code root")
        document["tools"]["pack_check"]["path"] = "labs/pack-custody-pass01/pack_check.py.bak"
        document["tools"]["pack_check"]["sha256"] = CHECKER_SHA
        declaration.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
        proc = self.app(code, "pack-preview", "--json")
        self.assert_stop(proc, "prime tool declaration does not match the pinned tools")

    def test_junction_pin_is_not_followed(self) -> None:
        code = self.copy_code()
        outside = self.root / "outside-lab"
        outside.mkdir()
        source = self.checker(code).read_bytes()
        (outside / "pack_check.py").write_bytes(source)
        lab = code / "labs" / "pack-custody-pass01"
        shutil.rmtree(lab)
        subprocess.run(["cmd", "/c", "mklink", "/J", str(lab), str(outside)], check=True, capture_output=True)
        self.junctions.append(lab)
        proc = self.app(
            code, "pack-check", "--format", "prime-pack-sources/1",
            "--manifest", str(self.root / "missing.json"), "--json",
        )
        self.assert_stop(proc, "tool path is linked and was not followed")
        self.assertEqual((outside / "pack_check.py").read_bytes(), source)

    def test_file_symlink_pin_is_not_followed(self) -> None:
        code = self.copy_code()
        outside = self.root / "linked-checker.py"
        source = self.checker(code).read_bytes()
        outside.write_bytes(source)
        tool = self.checker(code)
        tool.unlink()
        try:
            os.symlink(outside, tool)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("file symlink privilege WinError 1314")
            raise
        proc = self.app(
            code, "pack-check", "--format", "prime-pack-sources/1",
            "--manifest", str(self.root / "missing.json"), "--json",
        )
        self.assert_stop(proc, "tool path is linked and was not followed")
        self.assertEqual(outside.read_bytes(), source)

    def test_checker_injection_writes_nothing(self) -> None:
        code, repo, request, _commit = self.prepare()
        preview, _direct = self.preview(code, request, repo)
        digest = json.loads(preview.stdout.decode("utf-8"))["digest"]
        evil = self.root / "evil.py"
        evil.write_bytes(
            ("from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(self.sentinel)).encode("utf-8")
        )
        output = self.root / "pack"
        proc = self.app(
            code, "pack-assemble", "--request", str(request), "--repo", str(repo),
            "--output", str(output), "--digest", digest, "--checker", str(evil), "--json",
        )
        self.assert_stop(proc, "caller checker override is refused")
        self.assertFalse(output.exists())
        self.assertFalse(self.sentinel.exists())
        proc = self.app(
            code, "pack-verify", "--pack", str(output), f"--checker={evil}", "--json",
        )
        self.assert_stop(proc, "caller checker override is refused")
        self.assertFalse(self.sentinel.exists())
        self.assertFalse(output.exists())

    def test_stale_digest_and_malformed_request_match_direct(self) -> None:
        code, repo, request, _commit = self.prepare()
        output = self.root / "stale"
        user = [
            "--request", str(request), "--repo", str(repo),
            "--output", str(output), "--digest", "0" * 64, "--json",
        ]
        app_proc = self.app(code, "pack-assemble", *user)
        direct = self.tool(
            code, self.assembler(code), "assemble", *user, "--checker", str(self.checker(code)),
        )
        self.assert_no_traceback(app_proc)
        self.assertEqual(app_proc.returncode, 2)
        self.assertEqual(app_proc.stdout, direct.stdout)
        self.assertEqual(app_proc.stderr, direct.stderr)
        self.assertFalse(output.exists())
        report = json.loads(app_proc.stdout.decode("utf-8"))
        self.assertEqual(report["result"], "invalid")
        self.assertIn("digest", report["findings"][0]["detail"])
        bad = self.write_request(b"{")
        app_bad = self.app(code, "pack-preview", "--request", str(bad), "--repo", str(repo), "--json")
        direct_bad = self.tool(
            code, self.assembler(code), "preview",
            "--request", str(bad), "--repo", str(repo), "--json", "--checker", str(self.checker(code)),
        )
        self.assertEqual(app_bad.returncode, 2)
        self.assertEqual(app_bad.stdout, direct_bad.stdout)
        self.assertEqual(app_bad.stderr, direct_bad.stderr)
        self.assertFalse(output.exists())
        self.assert_git_read_only()

    def test_occupied_linked_and_live_book_targets_match_direct(self) -> None:
        code, repo, request, _commit = self.prepare()
        preview, _direct = self.preview(code, request, repo)
        digest = json.loads(preview.stdout.decode("utf-8"))["digest"]

        def both(output: Path) -> tuple[dict, dict]:
            user = [
                "--request", str(request), "--repo", str(repo),
                "--output", str(output), "--digest", digest, "--json",
            ]
            app_proc = self.app(code, "pack-assemble", *user)
            direct = self.tool(
                code, self.assembler(code), "assemble", *user, "--checker", str(self.checker(code)),
            )
            self.assertEqual(app_proc.returncode, 2, app_proc.stdout + app_proc.stderr)
            self.assertEqual(app_proc.stdout, direct.stdout)
            self.assertEqual(app_proc.stderr, direct.stderr)
            self.assertFalse(app_proc.stderr.startswith(b"stop:"))
            return json.loads(app_proc.stdout.decode("utf-8")), json.loads(direct.stdout.decode("utf-8"))

        occupied = self.root / "occupied"
        occupied.mkdir()
        (occupied / "keep").write_bytes(b"stay")
        report, _same = both(occupied)
        self.assertIn("empty", report["findings"][0]["detail"])
        self.assertEqual((occupied / "keep").read_bytes(), b"stay")
        self.assertFalse((occupied / "completion-receipt.json").exists())

        real = self.root / "real-target"
        real.mkdir()
        link = self.root / "link-target"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], check=True, capture_output=True)
        self.junctions.append(link)
        report, _same = both(link)
        self.assertIn("linked", report["findings"][0]["detail"])
        self.assertEqual(list(real.iterdir()), [])

        inside = repo / "pack"
        report, _same = both(inside)
        self.assertIn("repository", report["findings"][0]["detail"])
        self.assertFalse(inside.exists())

        book = self.root / "book"
        (book / "00.kernel").mkdir(parents=True)
        target = book / "draft"
        report, _same = both(target)
        self.assertIn("book", report["findings"][0]["detail"])
        self.assertFalse(target.exists())
        self.assertEqual(self.git_state(repo)[0], self.git(repo, "rev-parse", "HEAD").stdout)

    def test_argparse_diagnostics_match_and_create_nothing(self) -> None:
        code = self.copy_code()
        app_proc = self.app(code, "pack-preview", "--json")
        direct = self.tool(
            code, self.assembler(code), "preview", "--json", "--checker", str(self.checker(code)),
        )
        self.assert_no_traceback(app_proc)
        self.assertEqual(app_proc.returncode, 2)
        self.assertEqual(app_proc.stdout, b"")
        self.assertEqual(direct.stdout, b"")
        self.assertTrue(app_proc.stderr.startswith(b"usage: librarian.py preview"))
        self.assertTrue(direct.stderr.startswith(b"usage: pack_assembly.py preview"))
        self.assertEqual(self.argparse_error(app_proc.stderr), self.argparse_error(direct.stderr))
        output = self.root / "missing-digest"
        repo = self.root / "unused-repo"
        request = self.root / "unused-request.json"
        user = ["--request", str(request), "--repo", str(repo), "--output", str(output), "--json"]
        app_asm = self.app(code, "pack-assemble", *user)
        direct_asm = self.tool(
            code, self.assembler(code), "assemble", *user, "--checker", str(self.checker(code)),
        )
        self.assertEqual(app_asm.returncode, 2)
        self.assertEqual(app_asm.stdout, b"")
        self.assertEqual(direct_asm.stdout, b"")
        self.assertEqual(self.argparse_error(app_asm.stderr), self.argparse_error(direct_asm.stderr))
        self.assertIn(b"--digest", self.argparse_error(app_asm.stderr))
        self.assertFalse(output.exists())

    def test_declaration_faults_and_normal_run(self) -> None:
        code = self.copy_code()
        declaration = code / "app" / "prime-tools.json"
        raw = declaration.read_bytes()
        declaration.write_bytes(raw.replace(b'"version": 1', b'"version": true', 1))
        proc = self.app(code, "pack-check", "--help")
        self.assert_stop(proc, "prime tool declaration version is not 1")
        declaration.write_bytes(raw.replace(b'"version": 1', b'"version": 1, "version": 1', 1))
        proc = self.app(code, "pack-verify", "--pack", str(self.root / "none"))
        self.assert_stop(proc, "prime tool declaration repeats version")
        document = json.loads(raw.decode("utf-8"))
        document["extra"] = True
        declaration.write_bytes((json.dumps(document) + "\n").encode("utf-8"))
        proc = self.app(code, "pack-preview")
        self.assert_stop(proc, "unknown field")
        declaration.write_bytes(raw + b"\n[]\n")
        proc = self.app(code, "pack-assemble")
        self.assert_stop(proc, "prime tool declaration is not strict json")
        run = self.app(code, "run", "--root", str(self.root))
        self.assert_stop(run, "normal run is not activated")
        self.assertFalse(self.log.exists())


WRAPPER = r"""
import os
import subprocess
import sys
from pathlib import Path

log = Path(__file__).with_name("git.log")
argv = sys.argv[1:]
recorded = {
    "argv": argv,
    "env": {
        "GIT_OPTIONAL_LOCKS": os.environ.get("GIT_OPTIONAL_LOCKS", ""),
        "GIT_TERMINAL_PROMPT": os.environ.get("GIT_TERMINAL_PROMPT", ""),
    },
}
with log.open("a", encoding="utf-8", newline="\n") as handle:
    handle.write(repr(recorded) + "\n")
banned = {
    "fetch", "pull", "push", "ls-remote", "clone", "checkout", "config",
    "status", "add", "commit", "reset", "clean", "update-index", "update-ref",
    "symbolic-ref", "show",
}
if set(argv) & banned:
    sys.exit(97)
real = os.environ["PACK_PRIME_TOOLS_REAL_GIT"]
proc = subprocess.run([real, *argv], input=sys.stdin.buffer.read())
sys.exit(proc.returncode)
"""


if __name__ == "__main__":
    unittest.main()
