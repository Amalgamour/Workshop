"""Bounded tests for the file-backed Clerk handoff lab.

Stores are temporary directories outside the Git working tree.
A link type this process cannot create is a visible skip, not a pass.
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


LAB = Path(__file__).resolve().parents[1]
CLERK = LAB / "clerk.py"
sys.path.insert(0, str(LAB))
import clerk  # noqa: E402


INSTRUCTION = b"Count lines containing at least one non-whitespace character.\n"
COUNT = (
    b"def count_lines(text):\n"
    b"    return sum(1 for line in text.splitlines() if line.strip())\n"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(root: Path):
    files = {}
    dirs = set()
    if not root.exists():
        return files, dirs
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        current = Path(dirpath)
        dirs.add(current.relative_to(root).as_posix())
        for name in filenames:
            path = current / name
            rel = path.relative_to(root).as_posix()
            files[rel] = sha256(path.read_bytes())
    return files, dirs


def sections(text: str):
    out = {"queued": [], "claimed": [], "returned": [], "incomplete": []}
    current = None
    for line in text.splitlines():
        if line.startswith("section "):
            current = line.split(" ", 1)[1]
            continue
        if line.startswith("result ") or current is None or line == "none":
            if line.startswith("result "):
                current = None
            continue
        out[current].append(line)
    return out


class ClerkTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="clerk-pass02-"))
        self.base = self.root / "base"
        self.base.mkdir()
        (self.base / "task.txt").write_bytes(INSTRUCTION)
        self.digest = sha256(INSTRUCTION)
        self.store = self.root / "store"
        (self.root / "sentinel.txt").write_text("sentinel", encoding="ascii")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def cli(self, args, cwd=None):
        return subprocess.run(
            [sys.executable, "-B", str(CLERK), *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def job(self, name="job.json", **overrides):
        body = {
            "assignee": "builder-b",
            "expected_outputs": ["count.py"],
            "instructions": {"path": "task.txt", "sha256": self.digest},
            "job_id": "demo-0001",
            "release": "fixture release",
            "reviewer": "codex-prime",
            "routed_by": "router-fixture",
        }
        body.update(overrides)
        path = self.root / name
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    def raw_job(self, text, name="job.json"):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def queue(self, job_path=None, store=None):
        return self.cli([
            "queue",
            "--store", str(store or self.store),
            "--job", str(job_path or self.job()),
            "--instructions-base", str(self.base),
        ])

    def claim(self, *extra, actor="builder-b", job="demo-0001"):
        return self.cli([
            "claim",
            "--store", str(self.store),
            "--job", job,
            "--as", actor,
            "--instructions-base", str(self.base),
            *extra,
        ])

    def ret(self, token, delivery="d-1", evidence="scripted fixture", actor="builder-b", job="demo-0001"):
        return self.cli([
            "return",
            "--store", str(self.store),
            "--job", job,
            "--as", actor,
            "--claim", token,
            "--delivery", delivery,
            "--evidence", evidence,
        ])

    def token_of(self, text):
        for line in text.splitlines():
            if line.startswith("token "):
                return line.split(" ", 1)[1]
        self.fail("no token in:\n" + text)

    def write_output(self, payload=COUNT, name="count.py"):
        outbox = self.store / "jobs" / "demo-0001" / "outbox"
        (outbox / name).write_bytes(payload)

    def event_bytes(self, name, job="demo-0001"):
        return (self.store / "jobs" / job / name).read_bytes()

    def assert_code(self, proc, code):
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)

    def assert_store_absent(self):
        self.assertFalse(self.store.exists(), "store was created on a refusal")

    def assert_files_unchanged(self, before, prefix):
        after, _dirs = snapshot(self.root)
        for rel, digest in before.items():
            if rel == prefix or rel.startswith(prefix + "/"):
                continue
            self.assertEqual(after.get(rel), digest, rel)
        for rel in after:
            if rel in before:
                continue
            self.assertTrue(rel == prefix or rel.startswith(prefix + "/"), rel)

    def test_happy_path_chain_and_projection(self):
        job_path = self.job()
        before, _dirs = snapshot(self.root)
        queued = self.queue(job_path)
        self.assert_code(queued, 0)
        self.assertIn("queued demo-0001", queued.stdout)
        claimed = self.claim()
        self.assert_code(claimed, 0)
        token = self.token_of(claimed.stdout)
        self.write_output()
        returned = self.ret(token)
        self.assert_code(returned, 0)
        self.assertIn("returned demo-0001", returned.stdout)
        checked = self.cli([
            "verify",
            "--store", str(self.store),
            "--instructions-base", str(self.base),
        ])
        self.assert_code(checked, 0)
        self.assertIn("chain ok", checked.stdout)
        self.assertIn("states queued claimed returned", checked.stdout)
        self.assertIn("instructions-usable", checked.stdout)
        first = self.event_bytes("0001.queued.json")
        second = self.event_bytes("0002.claimed.json")
        third = self.event_bytes("0003.returned.json")
        self.assertEqual(json.loads(second)["prev"], sha256(first))
        self.assertEqual(json.loads(third)["prev"], sha256(second))
        self.assertIsNone(json.loads(first)["prev"])
        self.assert_files_unchanged(before, "store")

    def test_unknown_and_missing_keys_write_nothing(self):
        unknown = dict(self._body(), note="no")
        self.raw_job(json.dumps(unknown))
        proc = self.queue(self.root / "job.json")
        self.assert_code(proc, 2)
        self.assertIn("unknown job key note", proc.stdout)
        self.assert_store_absent()
        body = self._body()
        del body["reviewer"]
        self.raw_job(json.dumps(body), "missing.json")
        proc = self.queue(self.root / "missing.json")
        self.assert_code(proc, 2)
        self.assertIn("missing job key reviewer", proc.stdout)
        self.assert_store_absent()

    def test_assignee_must_differ_including_case(self):
        proc = self.queue(self.job(name="same.json", reviewer="builder-b"))
        self.assert_code(proc, 2)
        self.assertIn("must differ", proc.stdout)
        self.assert_store_absent()
        proc = self.queue(self.job(name="case.json", reviewer="Builder-B"))
        self.assert_code(proc, 2)
        self.assertIn("must differ", proc.stdout)
        self.assert_store_absent()

    def test_duplicate_and_case_colliding_job_id(self):
        self.assert_code(self.queue(), 0)
        first = snapshot(self.store)
        proc = self.queue(self.job(name="again.json"))
        self.assert_code(proc, 2)
        self.assertIn("collides", proc.stdout)
        self.assertEqual(snapshot(self.store), first)
        proc = self.queue(self.job(name="fold.json", job_id="Demo-0001"))
        self.assert_code(proc, 2)
        self.assertIn("collides", proc.stdout)
        self.assertEqual(os.listdir(self.store / "jobs"), ["demo-0001"])

    def test_nonfinite_and_duplicate_json(self):
        text = json.dumps(self._body()).replace('"fixture release"', "NaN", 1)
        proc = self.queue(self.raw_job(text))
        self.assert_code(proc, 2)
        self.assertIn("nonfinite JSON", proc.stdout)
        self.assert_store_absent()
        raw = '{"job_id":"demo-0001","job_id":"other"}'
        proc = self.queue(self.raw_job(raw, "dup.json"))
        self.assert_code(proc, 2)
        self.assertIn("duplicate JSON key", proc.stdout)
        self.assert_store_absent()

    def test_claim_and_return_refusals_write_no_event(self):
        self.assert_code(self.queue(), 0)
        outsider = self.claim(actor="colab")
        self.assert_code(outsider, 2)
        self.assertIn("not assignee", outsider.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0002.claimed.json").exists())
        early = self.ret("a" * 32)
        self.assert_code(early, 2)
        self.assertIn("return before claim", early.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())
        claimed = self.claim()
        self.assert_code(claimed, 0)
        token = self.token_of(claimed.stdout)
        frozen = self.event_bytes("0002.claimed.json")
        again = self.claim()
        self.assert_code(again, 2)
        self.assertIn("already claimed", again.stdout)
        self.assertEqual(self.event_bytes("0002.claimed.json"), frozen)
        wrong = self.ret("b" * 32)
        self.assert_code(wrong, 2)
        self.assertIn("wrong token", wrong.stdout)
        named = self.ret(token, actor="colab")
        self.assert_code(named, 2)
        self.assertIn("not assignee", named.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())

    def test_output_shape_refusals(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        missing = self.ret(token)
        self.assert_code(missing, 2)
        self.assertIn("expected output missing", missing.stdout)
        self.write_output()
        self.write_output(b"extra", "notes.py")
        extra = self.ret(token)
        self.assert_code(extra, 2)
        self.assertIn("extra outbox file", extra.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())

    def test_hardlink_output_refused(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        other = self.root / "outside.py"
        other.write_bytes(COUNT)
        try:
            os.link(other, self.store / "jobs" / "demo-0001" / "outbox" / "count.py")
        except OSError as exc:
            self.skipTest(f"SKIP hard link unsupported: {exc}")
        proc = self.ret(token)
        self.assert_code(proc, 2)
        self.assertIn("link count is not one", proc.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())

    def test_junction_output_refused(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        target = self.root / "tdir"
        target.mkdir()
        link = self.store / "jobs" / "demo-0001" / "outbox" / "count.py"
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            self.skipTest("SKIP junction unsupported: " + proc.stderr.strip())
        refused = self.ret(token)
        self.assert_code(refused, 2)
        self.assertIn("reparse point", refused.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())

    def test_symlink_output_refused_or_skipped(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        source = self.root / "outside.py"
        source.write_bytes(COUNT)
        link = self.store / "jobs" / "demo-0001" / "outbox" / "count.py"
        try:
            os.symlink(source, link)
        except OSError as exc:
            self.skipTest(f"SKIP symlink unsupported: {exc}")
        refused = self.ret(token)
        self.assert_code(refused, 2)
        self.assertIn("reparse point", refused.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())

    def test_output_and_instruction_paths(self):
        samples = {
            "escape.json": "../count.py",
            "nested.json": "sub/count.py",
            "device.json": "CON",
            "nulname.json": "nul.txt",
        }
        for filename, output in samples.items():
            proc = self.queue(self.job(name=filename, expected_outputs=[output], job_id="demo-0001"))
            self.assert_code(proc, 2)
            self.assertIn("output path is not a simple filename", proc.stdout)
            self.assert_store_absent()
        proc = self.queue(self.job(name="walk.json", instructions={"path": "../task.txt", "sha256": self.digest}))
        self.assert_code(proc, 2)
        self.assertIn("traversal", proc.stdout)
        self.assert_store_absent()
        proc = self.queue(self.job(
            name="abs.json",
            instructions={"path": str(self.base / "task.txt"), "sha256": self.digest},
        ))
        self.assert_code(proc, 2)
        self.assertIn("forward-slash", proc.stdout)
        self.assert_store_absent()
        folded = self.queue(self.job(name="fold-out.json", expected_outputs=["Count.py", "count.py"]))
        self.assert_code(folded, 2)
        self.assertIn("case-colliding output names", folded.stdout)
        self.assert_store_absent()

    def test_instruction_hash_and_cwd_are_not_ambient(self):
        proc = self.queue(self.job(
            name="bad-hash.json",
            instructions={"path": "task.txt", "sha256": "a" * 64},
        ))
        self.assert_code(proc, 2)
        self.assertIn("instruction hash mismatch", proc.stdout)
        self.assert_store_absent()
        self.assert_code(self.queue(), 0)
        (self.base / "task.txt").write_bytes(INSTRUCTION + b"changed\n")
        frozen = self.event_bytes("0001.queued.json")
        refused = self.claim()
        self.assert_code(refused, 2)
        self.assertIn("instruction hash mismatch", refused.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0002.claimed.json").exists())
        self.assertEqual(self.event_bytes("0001.queued.json"), frozen)
        other = self.root / "elsewhere"
        other.mkdir()
        (other / "task.txt").write_bytes(INSTRUCTION)
        cwd_digest = sha256(INSTRUCTION)
        lonely = self.root / "lonely-base"
        lonely.mkdir()
        body = self._body()
        body["job_id"] = "demo-0002"
        body["instructions"] = {"path": "task.txt", "sha256": cwd_digest}
        job_path = self.root / "cwd-job.json"
        job_path.write_text(json.dumps(body), encoding="utf-8")
        store = self.root / "other-store"
        proc = self.cli([
            "queue",
            "--store", str(store),
            "--job", str(job_path),
            "--instructions-base", str(lonely),
        ], cwd=other)
        self.assert_code(proc, 2)
        self.assertIn("instruction file is missing", proc.stdout)
        self.assertFalse(store.exists())

    def test_resume_returns_the_same_token_without_a_write(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        before = snapshot(self.store)
        resumed = self.claim("--resume")
        self.assert_code(resumed, 0)
        self.assertIn("resume demo-0001", resumed.stdout)
        self.assertEqual(self.token_of(resumed.stdout), token)
        self.assertNotIn("event ", resumed.stdout)
        self.assertEqual(snapshot(self.store), before)
        queued = self.queue(self.job(name="second.json", job_id="demo-0002"))
        self.assert_code(queued, 0)
        early = self.cli([
            "claim", "--store", str(self.store), "--job", "demo-0002",
            "--as", "builder-b", "--instructions-base", str(self.base), "--resume",
        ])
        self.assert_code(early, 2)
        self.assertIn("resume requires a complete claim", early.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0002" / "0002.claimed.json").exists())

    def test_resend_identity_is_per_job_and_does_not_restamp(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        self.write_output()
        first = self.ret(token)
        self.assert_code(first, 0)
        recorded = self.event_bytes("0003.returned.json")
        stamp = json.loads(recorded)["at"]
        again = self.ret(token)
        self.assert_code(again, 0)
        self.assertIn("already-recorded demo-0001", again.stdout)
        self.assertEqual(self.event_bytes("0003.returned.json"), recorded)
        self.assertEqual(json.loads(recorded)["at"], stamp)
        changed = self.ret(token, evidence="different evidence")
        self.assert_code(changed, 2)
        self.assertIn("delivery conflict", changed.stdout)
        self.assertEqual(self.event_bytes("0003.returned.json"), recorded)
        self.write_output(COUNT + b"# changed\n")
        artifact = self.ret(token)
        self.assert_code(artifact, 2)
        self.assertIn("delivery conflict", artifact.stdout)
        self.assertEqual(self.event_bytes("0003.returned.json"), recorded)
        other = self.ret(token, delivery="d-2")
        self.assert_code(other, 2)
        self.assertIn("already returned", other.stdout)
        self.assertEqual(self.event_bytes("0003.returned.json"), recorded)
        self.write_output(COUNT)
        second_job = self.job(name="job-2.json", job_id="demo-0002")
        self.assert_code(self.queue(second_job), 0)
        token_2 = self.token_of(self.cli([
            "claim", "--store", str(self.store), "--job", "demo-0002",
            "--as", "builder-b", "--instructions-base", str(self.base),
        ]).stdout)
        (self.store / "jobs" / "demo-0002" / "outbox" / "count.py").write_bytes(COUNT)
        reused = self.ret(token_2, job="demo-0002")
        self.assert_code(reused, 0)
        self.assertIn("returned demo-0002", reused.stdout)

    def test_event_tamper_missing_extra_and_planted_return(self):
        self.assert_code(self.queue(), 0)
        planted = self.store / "jobs" / "demo-0001" / "0003.returned.json"
        planted.write_bytes(b'{"planted":true}\n')
        refused = self.claim()
        self.assert_code(refused, 2)
        self.assertIn("planted return before claim", refused.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0002.claimed.json").exists())
        self.assertEqual(planted.read_bytes(), b'{"planted":true}\n')
        planted.unlink()
        token = self.token_of(self.claim().stdout)
        original = self.event_bytes("0001.queued.json")
        tampered = original.replace(b"fixture release", b"fixturX release", 1)
        self.assertNotEqual(tampered, original)
        (self.store / "jobs" / "demo-0001" / "0001.queued.json").write_bytes(tampered)
        shown = self.cli(["show", "--store", str(self.store), "--job", "demo-0001"])
        self.assert_code(shown, 2)
        self.assertIn("bad state:", shown.stdout)
        self.assertIn("hash chain mismatch", shown.stdout)
        self.assertNotIn("no matching job", shown.stdout)
        checked = self.cli(["verify", "--store", str(self.store)])
        self.assert_code(checked, 2)
        self.assertIn("bad state:", checked.stdout)
        (self.store / "jobs" / "demo-0001" / "0001.queued.json").write_bytes(original)
        self.write_output()
        self.assert_code(self.ret(token), 0)
        returned = self.event_bytes("0003.returned.json")
        (self.store / "jobs" / "demo-0001" / "0002.claimed.json").unlink()
        missing = self.ret(token)
        self.assert_code(missing, 2)
        self.assertIn("bad state:", missing.stdout)
        self.assertEqual(self.event_bytes("0003.returned.json"), returned)
        absent = self.cli(["show", "--store", str(self.store), "--job", "missing-job"])
        self.assert_code(absent, 2)
        self.assertIn("no matching job", absent.stdout)
        self.assertNotIn("bad state:", absent.stdout)

    def test_extra_event_and_inbox_disclosure(self):
        self.assert_code(self.queue(), 0)
        extra = self.store / "jobs" / "demo-0001" / "0004.returned.json"
        extra.write_bytes(b"{}\n")
        inbox = self.cli(["inbox", "--store", str(self.store), "--as", "colab"])
        self.assert_code(inbox, 2)
        self.assertIn("demo-0001", inbox.stdout)
        self.assertIn("bad state:", inbox.stdout)
        self.assertIn("extra file 0004.returned.json", inbox.stdout)
        parsed = sections(inbox.stdout)
        self.assertEqual(parsed["queued"], [])
        self.assertEqual(parsed["returned"], [])
        self.assertTrue(parsed["incomplete"])
        self.assertNotIn("result ok", inbox.stdout)
        stranger = self.cli(["inbox", "--store", str(self.store), "--as", "codex-prime"])
        self.assertIn("bad state:", stranger.stdout)
        self.assertNotIn("result ok", stranger.stdout)
        claim = self.claim()
        self.assert_code(claim, 2)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0002.claimed.json").exists())

    def test_artifact_changed_is_not_a_clean_return(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        self.write_output()
        self.assert_code(self.ret(token), 0)
        self.write_output(COUNT + b"\n")
        shown = self.cli(["show", "--store", str(self.store), "--job", "demo-0001"])
        self.assert_code(shown, 1)
        self.assertIn("artifact changed", shown.stdout)
        self.assertIn("not-returned-clean", shown.stdout)
        self.assertNotIn("no matching job", shown.stdout)
        reviewer = self.cli(["inbox", "--store", str(self.store), "--as", "codex-prime"])
        self.assert_code(reviewer, 1)
        self.assertIn("artifact changed", reviewer.stdout)
        checked = self.cli(["verify", "--store", str(self.store)])
        self.assert_code(checked, 1)
        self.assertIn("chain ok", checked.stdout)
        self.assertIn("artifact changed", checked.stdout)

    def test_interruptions_stay_incomplete(self):
        refused = clerk.queue(
            str(self.store), str(self.job()), str(self.base), interrupt="publish"
        )
        self.assertEqual(refused.code, 2)
        self.assertIn("event publication interrupted", refused.text)
        partial = self.event_bytes("0001.queued.json")
        self.assertLess(len(partial), 20)
        inbox = self.cli(["inbox", "--store", str(self.store), "--as", "builder-b"])
        self.assertNotEqual(inbox.returncode, 0)
        self.assertIn("bad state: incomplete:", inbox.stdout)
        self.assertIn("demo-0001", inbox.stdout)
        parsed = sections(inbox.stdout)
        self.assertEqual(parsed["queued"], [])
        self.assertEqual(parsed["returned"], [])
        reviewer = self.cli(["inbox", "--store", str(self.store), "--as", "codex-prime"])
        self.assertEqual(sections(reviewer.stdout)["returned"], [])
        self.assertIn("bad state:", reviewer.stdout)
        shutil.rmtree(self.store)
        self.assert_code(self.queue(), 0)
        stopped = clerk.claim(
            str(self.store), "demo-0001", "builder-b", str(self.base), interrupt="outbox"
        )
        self.assertEqual(stopped.code, 2)
        self.assertIn("interrupted before outbox setup", stopped.text)
        self.assertTrue((self.store / "jobs" / "demo-0001" / "0002.claimed.json").is_file())
        self.assertFalse((self.store / "jobs" / "demo-0001" / "outbox").exists())
        frozen = self.event_bytes("0002.claimed.json")
        resume = self.claim("--resume")
        self.assert_code(resume, 2)
        self.assertIn("outbox is missing", resume.stdout)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "outbox").exists())
        self.assertEqual(self.event_bytes("0002.claimed.json"), frozen)
        again = self.claim()
        self.assert_code(again, 2)
        self.assertEqual(self.event_bytes("0002.claimed.json"), frozen)
        returned = self.ret("a" * 32)
        self.assert_code(returned, 2)
        self.assertFalse((self.store / "jobs" / "demo-0001" / "0003.returned.json").exists())
        reviewer = self.cli(["inbox", "--store", str(self.store), "--as", "codex-prime"])
        self.assertEqual(sections(reviewer.stdout)["returned"], [])
        self.assertIn("bad state: incomplete:", reviewer.stdout)

    def test_interrupted_return_is_not_reviewer_success(self):
        self.assert_code(self.queue(), 0)
        token = self.token_of(self.claim().stdout)
        self.write_output()
        stopped = clerk.return_job(
            str(self.store), "demo-0001", "builder-b", token, "d-1", "scripted fixture",
            interrupt="publish",
        )
        self.assertEqual(stopped.code, 2)
        partial = self.event_bytes("0003.returned.json")
        retry = self.ret(token)
        self.assert_code(retry, 2)
        self.assertEqual(self.event_bytes("0003.returned.json"), partial)
        reviewer = self.cli(["inbox", "--store", str(self.store), "--as", "codex-prime"])
        self.assertEqual(sections(reviewer.stdout)["returned"], [])
        self.assertIn("bad state: incomplete:", reviewer.stdout)
        self.assertNotIn("result ok", reviewer.stdout)

    def test_git_store_and_unknown_flags_write_nothing(self):
        directory = self.root / "repo-dir"
        directory.mkdir()
        (directory / ".git").mkdir()
        store = directory / "store"
        proc = self.queue(store=store)
        self.assert_code(proc, 2)
        self.assertIn("Git working tree", proc.stdout)
        self.assertFalse(store.exists())
        worktree = self.root / "repo-file"
        worktree.mkdir()
        (worktree / ".git").write_text("gitdir: C:/nowhere\n", encoding="ascii")
        store = worktree / "store"
        proc = self.queue(store=store)
        self.assert_code(proc, 2)
        self.assertIn("Git working tree", proc.stdout)
        self.assertFalse(store.exists())
        inside = LAB / "_not_created_store"
        self.assertFalse(inside.exists())
        try:
            proc = self.queue(store=inside)
            self.assert_code(proc, 2)
            self.assertIn("Git working tree", proc.stdout)
            self.assertFalse(inside.exists())
        finally:
            if inside.exists():
                shutil.rmtree(inside, ignore_errors=True)
        proc = self.cli([
            "queue",
            "--store", str(self.store),
            "--job", str(self.job()),
            "--instructions-base", str(self.base),
            "--allow-repo-store",
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(self.store.exists())
        proc = self.cli([
            "queue", "--store", "relative-store", "--job", str(self.job(name="rel.json")),
            "--instructions-base", str(self.base),
        ], cwd=self.root)
        self.assert_code(proc, 2)
        self.assertIn("must be absolute", proc.stdout)
        self.assertFalse((self.root / "relative-store").exists())
        proc = self.cli(["accept", "--store", str(self.store)])
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(self.store.exists())

    def test_empty_store_differs_from_a_missing_store(self):
        self.store.mkdir()
        empty = self.cli(["verify", "--store", str(self.store)])
        self.assert_code(empty, 0)
        self.assertIn("jobs 0", empty.stdout)
        self.assertIn("result ok", empty.stdout)
        inbox = self.cli(["inbox", "--store", str(self.store), "--as", "builder-b"])
        self.assert_code(inbox, 0)
        self.assertEqual(sections(inbox.stdout)["incomplete"], [])
        missing = self.cli(["verify", "--store", str(self.root / "no-such-store")])
        self.assert_code(missing, 2)
        self.assertIn("no matching store", missing.stdout)
        self.assertNotIn("jobs 0", missing.stdout)

    def test_module_is_stdlib_only_and_does_not_delete(self):
        tree = ast.parse(CLERK.read_text(encoding="utf-8"))
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
        allowed = {
            "__future__", "argparse", "hashlib", "json", "os", "re", "secrets",
            "stat", "sys", "unicodedata", "datetime", "pathlib",
        }
        self.assertLessEqual(modules, allowed)
        source = CLERK.read_text(encoding="utf-8")
        for banned in ("os.remove", "os.unlink", "rmtree", "shutil", "sqlite3", "subprocess", "allow-repo-store"):
            self.assertNotIn(banned, source)

    def _body(self):
        return {
            "assignee": "builder-b",
            "expected_outputs": ["count.py"],
            "instructions": {"path": "task.txt", "sha256": self.digest},
            "job_id": "demo-0001",
            "release": "fixture release",
            "reviewer": "codex-prime",
            "routed_by": "router-fixture",
        }


if __name__ == "__main__":
    unittest.main(verbosity=1)
