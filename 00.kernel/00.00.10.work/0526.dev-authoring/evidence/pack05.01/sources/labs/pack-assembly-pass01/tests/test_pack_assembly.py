#!/usr/bin/env python3
"""Disposable tests for the fixture-only pack assembler."""

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

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import pack_assembly

PYTHON = os.environ.get("PACK_ASSEMBLY_PYTHON", sys.executable)
REAL_GIT = shutil.which("git")
TOOL = LAB / "pack_assembly.py"
CHECKER_SRC = Path(r"D:\Git\lib-build\labs\pack-custody-pass01\pack_check.py")
PIN = "9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d"
BANNED = {
    "fetch", "pull", "push", "ls-remote", "clone", "checkout", "config",
    "status", "add", "commit", "reset", "clean", "update-index", "update-ref",
    "symbolic-ref", "show",
}
TEXT = "\n".join([
    "Keep this sentence exact.",
    ">run.0509.05.01",
    "```",
    "## #99 — fenced example",
    "print('do not run')",
    "```",
])


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class PackAssemblyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="wf0501-")
        self.root = Path(self.tmp.name)
        self.junctions = []
        self.old_path = os.environ.get("PATH", "")
        wrap = self.root / "wrap"
        wrap.mkdir()
        (wrap / "gitwrap.py").write_bytes(WRAPPER.encode("utf-8"))
        cmd = '@echo off\r\n"' + PYTHON + '" -B "%~dp0gitwrap.py" %*\r\n'
        (wrap / "git.cmd").write_bytes(cmd.encode("ascii"))
        os.environ["PATH"] = str(wrap) + os.pathsep + self.old_path
        os.environ["PACK_ASSEMBLY_REAL_GIT"] = REAL_GIT
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
        self.log = wrap / "git.log"
        self.checker = self.root / "pack_check.py"
        self.checker.write_bytes(CHECKER_SRC.read_bytes())
        self.sentinel = self.root / "ran.txt"

    def tearDown(self):
        os.environ["PATH"] = self.old_path
        for link in self.junctions:
            if os.path.lexists(link):
                os.rmdir(link)
        self.tmp.cleanup()

    def git(self, repo, *args, input_bytes=None, check=True):
        return subprocess.run(
            [REAL_GIT, "-C", str(repo), *args],
            input=input_bytes, capture_output=True, check=check,
        )

    def init_repo(self):
        repo = self.root / "repo"
        repo.mkdir()
        self.git(repo, "init", "-q")
        for key, value in (
            ("user.email", "pack-assembly@example.invalid"),
            ("user.name", "pack-assembly-test"),
            ("core.autocrlf", "false"),
            ("commit.gpgsign", "false"),
        ):
            self.git(repo, "config", key, value)
        return repo

    def commit_worktree(self, repo, message):
        self.git(repo, "-c", "commit.gpgsign=false", "add", "-A")
        self.git(repo, "-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
        return self.git(repo, "rev-parse", "HEAD").stdout.decode().strip()

    def git_state(self, repo):
        env = os.environ.copy()
        env["GIT_OPTIONAL_LOCKS"] = "0"
        env["GIT_TERMINAL_PROMPT"] = "0"

        def run(*args):
            return subprocess.run(
                [REAL_GIT, "--no-optional-locks", "-C", str(repo), *args],
                capture_output=True, check=True, env=env,
            ).stdout

        return (
            run("rev-parse", "HEAD"),
            run("for-each-ref", "--format=%(objectname) %(refname)"),
            run("ls-files", "--stage"),
            run("status", "--porcelain=v1", "-uall"),
        )

    def request_bytes(self, revision, paths, **updates):
        body = {
            "schema": "pack-assembly-request/1",
            "template": "pack-assembly-draft/1",
            "title": "Fixture draft",
            "date": "2026-10-27",
            "author": "Codex Prime",
            "origin": {"book": "00.00.10.work", "page": "0509.pack-assembly", "batch": "05.01"},
            "identity": {"book": "00.00.10.work", "pppp": "0509", "keyword": "fixture", "batch": "05.01"},
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
        for key, value in updates.items():
            if isinstance(value, dict) and isinstance(body.get(key), dict):
                body[key] = {**body[key], **value}
            else:
                body[key] = value
        return (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    def write_request(self, raw):
        path = self.root / "request.json"
        path.write_bytes(raw)
        return path

    def cli(self, *args):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [PYTHON, "-B", str(TOOL), *args],
            capture_output=True, env=env,
        )
        self.assertNotIn(b"Traceback", proc.stdout + proc.stderr)
        report = json.loads(proc.stdout.decode("utf-8")) if proc.stdout else None
        return report, proc.returncode, proc.stderr

    def log_rows(self):
        if not self.log.exists():
            return []
        return [ast.literal_eval(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def assert_git_read_only(self):
        rows = self.log_rows()
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["env"]["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(row["env"]["GIT_TERMINAL_PROMPT"], "0")
            self.assertFalse(set(row["argv"]) & BANNED)
        verbs = [row["argv"][3] for row in rows]
        self.assertTrue(set(verbs) <= {"rev-parse", "cat-file"})
        self.assertIn("cat-file", verbs)

    def test_preview_is_deterministic_and_writes_nothing(self):
        repo = self.init_repo()
        payload = "Authorization: signed — 1999-01-01\nhashed: old\nopen(r'%s', 'w').write('ran')\n" % self.sentinel
        (repo / "keep.txt").write_bytes(payload.encode("utf-8"))
        (repo / "my file.txt").write_bytes(b"space")
        (repo / "café.txt").write_bytes("café".encode("utf-8"))
        (repo / "crlf.bin").write_bytes(b"a\r\nb")
        commit = self.commit_worktree(repo, "base")
        raw = self.request_bytes(commit, ["keep.txt", "my file.txt", "café.txt", "crlf.bin"], repository_label="Amalgamour/Librarian")
        request = self.write_request(raw)
        output = self.root / "pack"
        state = self.git_state(repo)
        first, code, err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        second, code2, _err2 = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(err, b"")
        self.assertEqual(code, 0)
        self.assertEqual(code2, 0)
        self.assertEqual(first["result"], "preview")
        self.assertEqual(first["digest"], second["digest"])
        self.assertEqual(first["planned"], second["planned"])
        self.assertEqual(first["commit"], commit)
        self.assertFalse(output.exists())
        self.assertFalse(self.sentinel.exists())
        self.assertEqual(self.git_state(repo), state)
        self.assert_git_read_only()
        human = subprocess.run(
            [PYTHON, "-B", str(TOOL), "preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker)],
            capture_output=True, env=os.environ.copy(),
        )
        self.assertEqual(human.returncode, 0)
        self.assertIn(first["digest"].encode("ascii"), human.stdout)
        self.assertNotIn(b"Traceback", human.stderr)

    def test_clean_assemble_and_exact_draft(self):
        repo = self.init_repo()
        payload = "Authorization: signed — 1999-01-01\nhashed: old\n"
        (repo / "keep.txt").write_bytes(payload.encode("utf-8"))
        (repo / "crlf.bin").write_bytes(b"a\r\nb")
        commit = self.commit_worktree(repo, "base")
        raw = self.request_bytes(
            commit, ["keep.txt", "crlf.bin"],
            repository_label="Amalgamour/Librarian",
            return_destination={"state": "supplied", "path": "0109.pack-assembly/05.01.return.md"},
            dependencies={"state": "supplied", "items": [{"name": "custody checker", "detail": "pinned hash only"}]},
        )
        request = self.write_request(raw)
        output = self.root / "pack"
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 0)
        state = self.git_state(repo)
        report, code, err = self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker),
            "--output", str(output), "--digest", preview["digest"], "--json",
        )
        self.assertEqual(err, b"")
        self.assertEqual(code, 0)
        self.assertEqual(report["result"], "completed")
        self.assertEqual(report["checker"]["result"], "pass")
        self.assertEqual(report["checker"]["exit"], 0)
        self.assertEqual(report["checker"]["sha256"], PIN)
        self.assertEqual(report["commit"], commit)
        self.assertEqual(self.git_state(repo), state)
        self.assertFalse((repo / "0109.pack-assembly").exists())
        draft = (output / "05.01.md").read_bytes()
        self.assertIn(b"Keep this sentence exact.", draft)
        self.assertIn(">run.0509.05.01".encode("utf-8"), draft)
        self.assertIn("## #99 — fenced example".encode("utf-8"), draft)
        self.assertIn("Authorization: draft — 2026-10-27".encode("utf-8"), draft)
        self.assertIn(b"state: draft", draft)
        self.assertIn(b"Release: PENDING.", draft)
        self.assertIn(b"Claim: PENDING.", draft)
        self.assertIn("## Return — Fixture executor\nPENDING.".encode("utf-8"), draft)
        self.assertIn("## Review — Codex Prime\nPENDING.".encode("utf-8"), draft)
        self.assertIn("Return destination: 0109.pack-assembly/05.01.return.md".encode("utf-8"), draft)
        self.assertIn(b"Live return-slot allocation is not checked.", draft)
        self.assertIn(b"Clerk readiness is not checked.", draft)
        self.assertIn(b"Dependencies: supplied", draft)
        self.assertNotIn(b"Authorization: signed", draft)
        self.assertNotIn(b"hashed:", draft)
        self.assertNotIn(b"state: ready", draft)
        self.assertNotIn(b"state: ran", draft)
        self.assertNotIn(str(repo).encode("utf-8"), draft)
        self.assertNotIn(b"D:\\", draft)
        self.assertEqual((output / "request.snapshot").read_bytes(), raw)
        self.assertEqual((output / "snapshots" / "0002.blob").read_bytes(), b"a\r\nb")
        manifest = json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "prime-pack-sources/1")
        self.assertEqual(manifest["commit"], commit)
        self.assertEqual(manifest["repository"], "Amalgamour/Librarian")
        self.assertEqual([row["snapshot"] for row in manifest["sources"]], ["snapshots/0001.blob", "snapshots/0002.blob"])
        self.assertEqual(manifest["sources"][0]["path"], "keep.txt")
        receipt_bytes = (output / "completion-receipt.json").read_bytes()
        receipt = json.loads(receipt_bytes.decode("utf-8"))
        self.assertNotIn(sha256(receipt_bytes), receipt_bytes.decode("utf-8"))
        self.assertEqual(receipt["request_sha256"], sha256(raw))
        self.assertEqual(receipt["batch_sha256"], sha256(draft))
        self.assertEqual(receipt["result"], "completed")
        self.assertNotIn("completion-receipt.json", [row["snapshot"] for row in receipt["sources"]])
        self.assert_git_read_only()

    def test_pinned_commit_ignores_later_head_index_and_worktree(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"original")
        commit_a = self.commit_worktree(repo, "A")
        raw = self.request_bytes(commit_a, ["keep.txt"])
        request = self.write_request(raw)
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 0)
        (repo / "README").write_bytes(b"other")
        commit_b = self.commit_worktree(repo, "B")
        (repo / "keep.txt").write_bytes(b"staged")
        self.git(repo, "add", "--", "keep.txt")
        (repo / "keep.txt").write_bytes(b"worktree")
        self.assertNotEqual(commit_b, commit_a)
        state = self.git_state(repo)
        output = self.root / "pack"
        report, code, err = self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker),
            "--output", str(output), "--digest", preview["digest"], "--json",
        )
        self.assertEqual(err, b"")
        self.assertEqual(code, 0)
        self.assertEqual((output / "snapshots" / "0001.blob").read_bytes(), b"original")
        self.assertEqual(report["commit"], commit_a)
        self.assertEqual(self.git_state(repo), state)
        self.assertEqual((repo / "keep.txt").read_bytes(), b"worktree")

    def test_stale_digest_writes_nothing(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        raw = self.request_bytes(commit, ["keep.txt"])
        request = self.write_request(raw)
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        changed = self.request_bytes(commit, ["keep.txt"], title="Changed title")
        request.write_bytes(changed)
        output = self.root / "pack"
        state = self.git_state(repo)
        report, code, err = self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker),
            "--output", str(output), "--digest", preview["digest"], "--json",
        )
        self.assertEqual(code, 2)
        self.assertEqual(err, b"")
        self.assertEqual(report["result"], "invalid")
        self.assertEqual(report["findings"][0]["code"], "digest-mismatch")
        self.assertNotEqual(report["digest"], preview["digest"])
        self.assertFalse(output.exists())
        self.assertEqual(self.git_state(repo), state)
        selected = self.request_bytes(commit, ["keep.txt", "missing-later.txt"])
        # Source selection changed, and the new path is also absent. The old digest must not write.
        request.write_bytes(self.request_bytes(commit, ["keep.txt"]))
        (repo / "other.txt").write_bytes(b"two")
        later = self.commit_worktree(repo, "later")
        request.write_bytes(self.request_bytes(later, ["keep.txt", "other.txt"]))
        output2 = self.root / "pack2"
        report2, code2, _err2 = self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker),
            "--output", str(output2), "--digest", preview["digest"], "--json",
        )
        self.assertEqual(code2, 2)
        self.assertFalse(output2.exists())
        self.assertNotEqual(report2["digest"], preview["digest"])

    def test_invalid_shapes_write_nothing(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        output = self.root / "pack"
        cases = [
            self.request_bytes(commit, ["keep.txt"], template="pack-assembly-draft/2"),
            self.request_bytes(commit, ["../secret"]),
            self.request_bytes(commit, ["C:/Windows/notepad.exe"]),
            self.request_bytes(commit, ["File.txt", "file.txt"]),
            self.request_bytes(commit, []),
            self.request_bytes(commit, ["keep.txt"], instructions=[
                {"nn": "01", "heading": "One", "text": "alpha"},
                {"nn": "01", "heading": "Two", "text": "beta"},
            ]),
            self.request_bytes(commit, ["keep.txt"], instructions=[
                {"nn": "01", "heading": "Planted", "text": "## #07 — planted"},
            ]),
            b'{"schema":"pack-assembly-request/1","schema":"again"}\n',
            b'{"schema":"nope"}\n',
        ]
        for raw in cases:
            request = self.write_request(raw if isinstance(raw, bytes) else raw)
            before = list(self.root.iterdir())
            report, code, err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
            self.assertEqual(code, 2, report)
            self.assertEqual(err, b"")
            self.assertEqual(report["result"], "invalid")
            self.assertFalse(output.exists())
            self.assertEqual(list(self.root.iterdir()), before)

    def test_absent_symlink_and_submodule_sources(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["missing.txt"]))
        state = self.git_state(repo)
        report, code, err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 2)
        self.assertEqual(err, b"")
        self.assertIn("absent", report["findings"][0]["detail"])
        self.assertEqual(self.git_state(repo), state)

        link_blob = self.git(repo, "hash-object", "-w", "--stdin", input_bytes=b"target").stdout.decode().strip()
        link_tree = self.mktree(repo, [("120000", "blob", link_blob, "link.txt")])
        link_commit = self.commit_tree(repo, link_tree, "link")
        request.write_bytes(self.request_bytes(link_commit, ["link.txt"]))
        report, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 2)
        self.assertIn("symlink", report["findings"][0]["detail"])

        sub_tree = self.mktree(repo, [("160000", "commit", commit, "nested")])
        sub_commit = self.commit_tree(repo, sub_tree, "sub")
        request.write_bytes(self.request_bytes(sub_commit, ["nested"]))
        report, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 2)
        self.assertIn("submodule", report["findings"][0]["detail"])
        self.assertFalse((self.root / "pack").exists())

    def test_refuses_occupied_linked_repo_and_book_targets(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["keep.txt"]))
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 0)
        occupied = self.root / "occupied"
        occupied.mkdir()
        (occupied / "keep").write_bytes(b"stay")
        report, code, _err = self.assemble(request, repo, occupied, preview["digest"])
        self.assertEqual(code, 2)
        self.assertEqual((occupied / "keep").read_bytes(), b"stay")
        self.assertFalse((occupied / "completion-receipt.json").exists())

        real = self.root / "real"
        real.mkdir()
        link = self.root / "link"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], check=True, capture_output=True)
        self.junctions.append(link)
        report, code, _err = self.assemble(request, repo, link, preview["digest"])
        self.assertEqual(code, 2)
        self.assertEqual(list(real.iterdir()), [])

        inside = repo / "pack"
        report, code, _err = self.assemble(request, repo, inside, preview["digest"])
        self.assertEqual(code, 2)
        self.assertFalse(inside.exists())
        self.assertIn("repository", report["findings"][0]["detail"])

        book = self.root / "book"
        (book / "00.kernel").mkdir(parents=True)
        target = book / "draft"
        report, code, _err = self.assemble(request, repo, target, preview["digest"])
        self.assertEqual(code, 2)
        self.assertFalse(target.exists())
        self.assertIn("book", report["findings"][0]["detail"])

        empty = self.root / "empty"
        empty.mkdir()
        report, code, err = self.assemble(request, repo, empty, preview["digest"])
        self.assertEqual(err, b"")
        self.assertEqual(code, 0)
        self.assertEqual(report["result"], "completed")
        self.assertTrue((empty / "completion-receipt.json").is_file())

    def test_wrong_checker_writes_nothing(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["keep.txt"]))
        bad = self.root / "bad_check.py"
        raw = self.checker.read_bytes()
        bad.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        output = self.root / "pack"
        report, code, err = self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(bad),
            "--output", str(output), "--digest", "0" * 64, "--json",
        )
        self.assertEqual(code, 2)
        self.assertEqual(err, b"")
        self.assertIn("checker sha256", report["findings"][0]["detail"])
        self.assertFalse(output.exists())
        self.assertEqual(sha256(CHECKER_SRC.read_bytes()), PIN)

    def test_checker_refusal_and_interruption_leave_a_partial(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        raw = self.request_bytes(commit, ["keep.txt"])
        request = self.write_request(raw)
        preview, _code = pack_assembly.preview(str(request), str(repo), str(self.checker))
        output = self.root / "pack"

        def corrupt(target):
            blob = target / "snapshots" / "0001.blob"
            blob.write_bytes(b"two")

        report, code = pack_assembly.assemble(
            str(request), str(repo), str(self.checker), str(output), preview["digest"], before_check=corrupt,
        )
        self.assertEqual(code, 1)
        self.assertEqual(report["result"], "partial")
        self.assertEqual((output / "snapshots" / "0001.blob").read_bytes(), b"two")
        self.assertTrue((output / "05.01.md").is_file())
        self.assertFalse((output / "completion-receipt.json").exists())
        again, code2 = pack_assembly.assemble(
            str(request), str(repo), str(self.checker), str(output), preview["digest"],
        )
        self.assertEqual(code2, 2)
        self.assertEqual((output / "snapshots" / "0001.blob").read_bytes(), b"two")
        self.assertFalse((output / "completion-receipt.json").exists())

        other = self.root / "partial"
        def stop(_target):
            raise pack_assembly.AssemblyError("interrupted before the checker")
        report, code = pack_assembly.assemble(
            str(request), str(repo), str(self.checker), str(other), preview["digest"], before_check=stop,
        )
        self.assertEqual(code, 2)
        self.assertTrue((other / "05.01.md").is_file())
        self.assertFalse((other / "completion-receipt.json").exists())
        verified, vcode, err = self.cli("verify", "--pack", str(other), "--checker", str(self.checker), "--json")
        self.assertEqual(vcode, 1)
        self.assertEqual(err, b"")
        self.assertEqual(verified["result"], "partial")
        self.assertFalse((other / "completion-receipt.json").exists())

    def test_verify_detects_tamper_without_rewriting_the_receipt(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["keep.txt"]))
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        output = self.root / "pack"
        report, code, _err = self.assemble(request, repo, output, preview["digest"])
        self.assertEqual(code, 0)
        receipt_path = output / "completion-receipt.json"
        receipt_bytes = receipt_path.read_bytes()
        intact, code, err = self.cli("verify", "--pack", str(output), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 0)
        self.assertEqual(err, b"")
        self.assertEqual(intact["result"], "intact")
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
        blob = output / "snapshots" / "0001.blob"
        original = blob.read_bytes()
        blob.write_bytes(b"mutated")
        mismatch, code, _err = self.cli("verify", "--pack", str(output), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 1)
        self.assertEqual(mismatch["result"], "mismatch")
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
        blob.write_bytes(original)
        draft = output / "05.01.md"
        draft_bytes = draft.read_bytes()
        draft.write_bytes(draft_bytes + b"\nextra\n")
        mismatch, code, _err = self.cli("verify", "--pack", str(output), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 1)
        self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
        draft.write_bytes(draft_bytes)
        receipt_path.unlink()
        partial, code, _err = self.cli("verify", "--pack", str(output), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 1)
        self.assertEqual(partial["result"], "partial")
        self.assertFalse(receipt_path.exists())

    def test_long_git_path_is_not_checked_out(self):
        repo = self.init_repo()
        blob = self.git(repo, "hash-object", "-w", "--stdin", input_bytes=b"long-path-bytes\n").stdout.decode().strip()
        tree = self.mktree(repo, [("100644", "blob", blob, "file.txt")])
        for _ in range(28):
            tree = self.mktree(repo, [("040000", "tree", tree, "directory")])
        pinned = self.commit_tree(repo, tree, "long")
        readme = self.git(repo, "hash-object", "-w", "--stdin", input_bytes=b"readme\n").stdout.decode().strip()
        head_tree = self.mktree(repo, [("100644", "blob", readme, "README")])
        head = self.commit_tree(repo, head_tree, "head")
        self.git(repo, "update-ref", "HEAD", head)
        path = "directory/" * 28 + "file.txt"
        self.assertEqual(len(path), 288)
        request = self.write_request(self.request_bytes(pinned, [path]))
        preview, code, err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(err, b"")
        self.assertEqual(code, 0, preview)
        self.assertEqual(preview["sources"][0]["bytes"], len(b"long-path-bytes\n"))
        output = self.root / "pack"
        report, code, _err = self.assemble(request, repo, output, preview["digest"])
        self.assertEqual(code, 0, report)
        self.assertEqual((output / "snapshots" / "0001.blob").read_bytes(), b"long-path-bytes\n")
        self.assertFalse((repo / "directory").exists())
        self.assertFalse((repo / "file.txt").exists())
        self.assert_git_read_only()

    def test_digest_binds_template_request_commit_and_outputs(self):
        sources = [{"path": "keep.txt", "sha256": "a" * 64, "bytes": 1, "snapshot": "snapshots/0001.blob"}]
        planned = [{"path": "05.01.md", "sha256": "b" * 64, "bytes": 2}]
        commit = "c" * 40
        first = pack_assembly.compute_digest(b"{}\n", commit, sources, planned)
        second = pack_assembly.compute_digest(b"{ }\n", commit, sources, planned)
        self.assertNotEqual(first, second)
        self.assertEqual(manual_digest(pack_assembly.TEMPLATE, b"{}\n", commit, sources, planned), first)
        self.assertNotEqual(manual_digest("pack-assembly-draft/2", b"{}\n", commit, sources, planned), first)

    def test_cli_syntax_uses_argparse(self):
        proc = subprocess.run([PYTHON, "-B", str(TOOL)], capture_output=True)
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr)

    def test_file_symlink_target_is_not_followed(self):
        repo = self.init_repo()
        (repo / "keep.txt").write_bytes(b"one")
        commit = self.commit_worktree(repo, "base")
        request = self.write_request(self.request_bytes(commit, ["keep.txt"]))
        preview, code, _err = self.cli("preview", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker), "--json")
        self.assertEqual(code, 0)
        target = self.root / "real-file"
        target.write_bytes(b"secret")
        link = self.root / "link-file"
        try:
            os.symlink(target, link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("file symlink privilege WinError 1314")
            raise
        report, code, _err = self.assemble(request, repo, link, preview["digest"])
        self.assertEqual(code, 2)
        self.assertEqual(target.read_bytes(), b"secret")

    def mktree(self, repo, rows):
        payload = "".join(f"{mode} {kind} {sha}\t{name}\n" for mode, kind, sha, name in rows).encode("utf-8")
        return self.git(repo, "mktree", input_bytes=payload).stdout.decode().strip()

    def commit_tree(self, repo, tree, message):
        proc = self.git(repo, "-c", "commit.gpgsign=false", "commit-tree", tree, "-m", message)
        return proc.stdout.decode().strip()

    def assemble(self, request, repo, output, digest):
        return self.cli(
            "assemble", "--request", str(request), "--repo", str(repo), "--checker", str(self.checker),
            "--output", str(output), "--digest", digest, "--json",
        )


def manual_digest(template, request_raw, commit, sources, planned):
    parts = [pack_assembly.DIGEST_DOMAIN, template, request_raw, commit]
    for source in sources:
        parts.extend([source["path"], source["sha256"], str(source["bytes"])])
    for item in planned:
        parts.extend([item["path"], item["sha256"], str(item["bytes"])])
    digest = hashlib.sha256()
    for part in parts:
        digest.update(pack_assembly.length_prefix(part))
    return digest.hexdigest()


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
real = os.environ["PACK_ASSEMBLY_REAL_GIT"]
proc = subprocess.run([real, *argv], input=sys.stdin.buffer.read())
sys.exit(proc.returncode)
"""


if __name__ == "__main__":
    unittest.main()
