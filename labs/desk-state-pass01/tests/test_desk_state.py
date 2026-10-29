"""Desk-state transitions. Disposable repositories only; the live book is not a fixture."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

LIB = r"D:\Git\lib-build"
PY = r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe"
MODULE = str(Path(LIB) / "labs" / "desk-state-pass01" / "desk_state.py")
CAPTURE = str(Path(LIB) / "labs" / "return-capture-pass01" / "return_capture.py")
INSPECT = str(Path(LIB) / "labs" / "return-capture-pass01" / "return_inspect.py")

import sys

sys.path.insert(0, str(Path(LIB) / "labs" / "desk-state-pass01"))
import desk_state  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-B", MODULE, *argv], capture_output=True)


def git(repo: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if check and proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc


def commit_all(repo: str) -> str:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=Desk Test", "-c", "user.email=desk@example.com", "commit", "-m", "desk")
    return git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def tools() -> dict:
    out = {}
    for name, (rel, pin) in desk_state.PINS.items():
        out[name] = {"path": os.path.abspath(os.path.join(LIB, *rel.split("/"))), "sha256": pin}
    return out


def page_body(title: str, member: str | None = None, receipt: str | None = None, extra: str = "") -> str:
    pointer = "PENDING."
    if member:
        pointer = f"Member: {member}\nReceipt: {receipt}"
    return (
        f"# 05 — {title}\n"
        "version: 001\n"
        "Authorization: draft — 2026-10-29\n"
        "who: Codex Prime\n"
        "state: draft\n"
        "Face: 05\n"
        "PPPP: 0508\n"
        "book: 00.00.10.work\n"
        "\n"
        "## Assignment\n"
        "Executor: Tester.\n"
        "Release and claim: recorded in the Return pointer. This draft grants no release.\n"
        "\n"
        "## Return pointer\n"
        f"{pointer}\n"
        "\n"
        "## Review — Codex Prime\n"
        "PENDING.\n"
        f"{extra}"
    )


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def record(repo: str, output: str, pages: list, lanes: list, legacy: dict, **over) -> dict:
    doc = {
        "schema": "desk-state/1",
        "desk": "desk-test",
        "book": "00.00.10.work",
        "goal": {"statement": "Keep two declared lanes visible.", "evidence": []},
        "milestone": {"statement": "This fixture is a step, not a handover.", "evidence": []},
        "lanes": lanes,
        "blockers": [],
        "handoff": {"statement": "The recorded next step stays on the record.", "author": "Codex-Prime", "evidence": []},
        "pages": pages,
        "members": [],
        "coordination": [],
        "uninspected": [],
        "legacy": legacy,
        "tools": tools(),
        "bounds": {
            "max_sources": 32,
            "max_source_bytes": 262144,
            "max_total_bytes": 1048576,
            "max_output_bytes": 1048576,
        },
        "roots": {"repository": repo, "tools": LIB, "members_book": repo, "output": output},
        "revision": {"reason": "fixture", "authorizing": "0508.return-capture/05.19 #05", "predecessor": None},
        "custody": "commit-facts-only",
    }
    doc.update(over)
    return doc


def coord(batch: str, digest: str, **over) -> dict:
    item = {
        "label": "SUPPLIED",
        "batch_id": batch,
        "source_sha256": digest,
        "release": "recorded",
        "claim": "absent",
        "claim_actor": None,
        "candidate": None,
        "review": None,
        "publication": {"status": "unknown", "ref": None, "commit": None},
    }
    item.update(over)
    return item


def save(directory: str, name: str, doc: dict) -> str:
    path = os.path.join(directory, name)
    Path(path).write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def view_json(proc: subprocess.CompletedProcess) -> dict:
    return json.loads(proc.stdout.decode("utf-8"))


class DeskStateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="desk-state-")
        self.repo = os.path.abspath(os.path.join(self.tmp, "repo"))
        self.out = os.path.abspath(os.path.join(self.tmp, "out"))
        os.makedirs(self.repo)
        os.makedirs(self.out)
        git(self.repo, "init")
        write(os.path.join(self.repo, "legacy.md"), "legacy\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def legacy(self, commit: str) -> dict:
        data = Path(self.repo, "legacy.md").read_bytes()
        return {
            "repository": self.repo,
            "path": "legacy.md",
            "commit": commit,
            "sha256": sha(data),
            "note": "fixture legacy",
        }

    def page(self, rel: str, title: str, **kwargs) -> str:
        path = os.path.join(self.repo, *rel.split("/"))
        write(path, page_body(title, **kwargs))
        return rel

    def test_two_lanes_and_unbound_source(self):
        self.page("00.kernel/00.00.10.work/0508.desk-alpha/05.01.md", "Alpha")
        self.page("00.kernel/00.00.10.work/0509.desk-beta/05.01.md", "Beta")
        gamma = self.page("00.kernel/00.00.10.work/0510.desk-gamma/05.01.md", "Gamma")
        commit = commit_all(self.repo)
        pages = []
        lanes = []
        coords = []
        for rel, lane_id, page_id, batch in (
            ("00.kernel/00.00.10.work/0508.desk-alpha/05.01.md", "alpha", "p-alpha", "0508.desk-alpha/05.01"),
            ("00.kernel/00.00.10.work/0509.desk-beta/05.01.md", "beta", "p-beta", "0509.desk-beta/05.01"),
        ):
            digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
            pages.append({"id": page_id, "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"})
            lanes.append({"id": lane_id, "page_id": page_id, "worker": None if lane_id == "beta" else "Grok-Builder-2", "task": f"Task {lane_id} stays declared."})
            coords.append(coord(batch, digest))
        gamma_digest_before = sha(Path(self.repo, *gamma.split("/")).read_bytes())
        pages.append({"id": "p-gamma", "repository": self.repo, "path": gamma, "commit": commit, "observation": "git-blob"})
        lanes.append({"id": "gamma", "page_id": "p-gamma", "worker": None, "task": "Unbound source stays visible."})
        doc = record(self.repo, self.out, pages, lanes, self.legacy(commit), coordination=coords)
        path = save(self.out, "record.json", doc)
        before = Path(path).read_bytes()
        first = run(["view", "--input", path, "--json"])
        self.assertEqual(first.returncode, 1, first.stderr.decode())
        body = view_json(first)
        self.assertIsNone(body["elected"])
        self.assertEqual([lane["id"] for lane in body["lanes"]], ["alpha", "beta", "gamma"])
        self.assertEqual(body["lanes"][0]["lifecycle"], "released")
        self.assertEqual(body["lanes"][0]["worker_meaning"], "label")
        self.assertEqual(body["lanes"][1]["worker"], None)
        self.assertEqual(body["lanes"][1]["worker_meaning"], "unrecorded")
        self.assertEqual(body["lanes"][2]["lifecycle"], "unprojected")
        self.assertIn("no SUPPLIED coordination", body["lanes"][2]["unprojected_reason"])
        self.assertNotIn("available", json.dumps(body["lanes"]))
        second = run(["view", "--input", path, "--json"])
        self.assertEqual(second.returncode, 1)
        again = view_json(second)
        self.assertEqual(again["lanes"], body["lanes"])
        self.assertEqual(again["unknowns"], body["unknowns"])
        self.assertEqual(again["attention"], body["attention"])
        self.assertEqual(again["handoff"], body["handoff"])
        self.assertEqual(again["elected"], None)
        self.assertEqual(Path(path).read_bytes(), before)
        self.assertEqual(sha(Path(self.repo, *gamma.split("/")).read_bytes()), gamma_digest_before)

    def test_review_then_held_and_terminal_contrast(self):
        book = os.path.abspath(os.path.join(self.tmp, "book"))
        os.makedirs(book)
        note = "notes/one.md"
        write(os.path.join(self.repo, note), "note\n")
        ret = os.path.join(self.repo, "notes", "return.md")
        write(ret, "Did.\nBlocked.\nNeed.\n")
        base = commit_all(self.repo)
        common = [PY, "-B", CAPTURE]
        reserved = subprocess.run(
            common + ["reserve", "--book", book, "--submission", "desk-held", "--name", "held-return",
                      "--origin-book", "00.00.10.work", "--origin-page", "0508.desk-alpha", "--origin-batch", "05.01",
                      "--expected-output", note, "--submitter", "Desk Test", "--reviewer", "Codex Prime",
                      "--release", "fixture"],
            capture_output=True,
        )
        self.assertEqual(reserved.returncode, 0, reserved.stdout.decode() + reserved.stderr.decode())
        member = reserved.stdout.decode().splitlines()[0].split(" ", 1)[1]
        captured = subprocess.run(
            common + ["capture", "--book", book, "--submission", "desk-held", "--return-file", ret,
                      "--source-root", self.repo, "--artifact", f"{note}|{note}"],
            capture_output=True,
        )
        self.assertEqual(captured.returncode, 0, captured.stdout.decode() + captured.stderr.decode())
        inspected = subprocess.run([PY, "-B", INSPECT, "inspect", "--book", book, "--member", member, "--json"], capture_output=True)
        receipt = json.loads(inspected.stdout)["capture"]["receipt_sha256"]
        rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        self.page(rel, "Held", member=member, receipt=receipt)
        live_rel = "00.kernel/00.00.10.work/0509.desk-beta/05.02.md"
        self.page(live_rel, "Live")
        commit = commit_all(self.repo)
        digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
        pages = [
            {"id": "p-held", "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"},
            {"id": "p-live", "repository": self.repo, "path": live_rel, "commit": None, "observation": "live-file"},
        ]
        lanes = [
            {"id": "held", "page_id": "p-held", "worker": None, "task": "Named return with no bound review yet."},
            {"id": "live", "page_id": "p-live", "worker": None, "task": "Live page waits for its own coordination."},
        ]
        waiting = coord("0508.desk-alpha/05.01", digest, candidate=member)
        doc = record(
            self.repo, self.out, pages, lanes, self.legacy(base),
            coordination=[waiting], members=[{"name": member, "role": "declared"}],
            custody="inspect-named-members",
        )
        doc["roots"]["members_book"] = book
        path = save(self.out, "waiting.json", doc)
        waiting_bytes = Path(path).read_bytes()
        first = run(["view", "--input", path, "--json"])
        self.assertEqual(first.returncode, 1, first.stderr.decode())
        body = view_json(first)
        self.assertEqual(body["lanes"][0]["lifecycle"], "returned-awaiting-review")
        self.assertIsNone(body["lanes"][0]["followup"])
        self.assertIsNone(body["elected"])
        held = coord(
            "0508.desk-alpha/05.01", digest, candidate=member,
            review={
                "member": member, "receipt_sha256": receipt, "disposition": "held",
                "terminal": None, "reviewer": "Codex-Prime", "followup": "0508.desk-alpha/05.02",
            },
        )
        revised = dict(doc)
        revised["coordination"] = [held]
        revised["lanes"] = [
            {"id": "held", "page_id": "p-held", "worker": None, "task": "Held review remains visible."},
            lanes[1],
        ]
        revised["revision"] = {
            "reason": "Bind the held review.",
            "authorizing": "0508.return-capture/05.19 #05",
            "predecessor": sha(Path(path).read_bytes()),
        }
        submission = save(self.out, "held-submission.json", revised)
        new_path = os.path.join(self.out, "held.json")
        changed = run(["revise", "--record", path, "--expected", revised["revision"]["predecessor"], "--submission", submission, "--out", new_path])
        self.assertEqual(changed.returncode, 0, changed.stderr.decode())
        self.assertEqual(Path(path).read_bytes(), waiting_bytes)
        second = run(["view", "--input", new_path, "--json"])
        self.assertEqual(second.returncode, 1, second.stderr.decode())
        held_body = view_json(second)
        self.assertEqual(held_body["lanes"][0]["lifecycle"], "open-held")
        self.assertEqual(held_body["lanes"][0]["followup"], "0508.desk-alpha/05.02")

    def test_accepted_terminal_and_commit_basis(self):
        book = os.path.abspath(os.path.join(self.tmp, "book"))
        os.makedirs(book)
        note = "notes/done.md"
        write(os.path.join(self.repo, note), "done\n")
        ret = os.path.join(self.repo, "notes", "return.md")
        write(ret, "Did.\nBlocked.\nNeed.\n")
        commit_all(self.repo)
        common = [PY, "-B", CAPTURE]
        made = []
        for submission, name, page, batch in (
            ("desk-open", "open-return", "0508.desk-alpha", "05.01"),
            ("desk-done", "done-return", "0509.desk-beta", "05.02"),
            ("desk-commit", "commit-return", "0510.desk-gamma", "05.03"),
        ):
            reserved = subprocess.run(
                common + ["reserve", "--book", book, "--submission", submission, "--name", name,
                          "--origin-book", "00.00.10.work", "--origin-page", page, "--origin-batch", batch,
                          "--expected-output", note, "--submitter", "Desk Test", "--reviewer", "Codex Prime",
                          "--release", "fixture"],
                capture_output=True,
            )
            self.assertEqual(reserved.returncode, 0, reserved.stdout.decode())
            member = reserved.stdout.decode().splitlines()[0].split(" ", 1)[1]
            captured = subprocess.run(
                common + ["capture", "--book", book, "--submission", submission, "--return-file", ret,
                          "--source-root", self.repo, "--artifact", f"{note}|{note}"],
                capture_output=True,
            )
            self.assertEqual(captured.returncode, 0, captured.stdout.decode() + captured.stderr.decode())
            inspected = subprocess.run([PY, "-B", INSPECT, "inspect", "--book", book, "--member", member, "--json"], capture_output=True)
            made.append((member, json.loads(inspected.stdout)["capture"]["receipt_sha256"], page, batch))
        open_member, open_receipt, _, _ = made[0]
        done_member, done_receipt, _, _ = made[1]
        commit_member, commit_receipt, _, _ = made[2]
        open_rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        done_rel = "00.kernel/00.00.10.work/0509.desk-beta/05.02.md"
        commit_rel = "00.kernel/00.00.10.work/0510.desk-gamma/05.03.md"
        self.page(open_rel, "Open", member=open_member, receipt=open_receipt)
        self.page(done_rel, "Done", member=done_member, receipt=done_receipt)
        self.page(commit_rel, "Commit", member=commit_member, receipt=commit_receipt)
        commit = commit_all(self.repo)
        def one(page_id, rel, observation):
            return {
                "id": page_id, "repository": self.repo, "path": rel,
                "commit": None if observation == "live-file" else commit,
                "observation": observation,
            }
        pages = [
            one("p-open", open_rel, "live-file"),
            one("p-done", done_rel, "live-file"),
            one("p-commit", commit_rel, "git-blob"),
        ]
        lanes = [
            {"id": "open", "page_id": "p-open", "worker": None, "task": "Accepted without a terminal declaration."},
            {"id": "done", "page_id": "p-done", "worker": None, "task": "Explicit terminal completion on a live file."},
            {"id": "commit", "page_id": "p-commit", "worker": None, "task": "The same terminal claim on a commit stays unverified."},
        ]
        def review(member, receipt, terminal):
            return {
                "member": member, "receipt_sha256": receipt, "disposition": "accepted",
                "terminal": terminal, "reviewer": "Codex-Prime", "followup": None,
            }
        coords = [
            coord("0508.desk-alpha/05.01", sha(Path(self.repo, *open_rel.split("/")).read_bytes()), candidate=open_member, review=review(open_member, open_receipt, None)),
            coord("0509.desk-beta/05.02", sha(Path(self.repo, *done_rel.split("/")).read_bytes()), candidate=done_member, review=review(done_member, done_receipt, "completed")),
            coord("0510.desk-gamma/05.03", sha(Path(self.repo, *commit_rel.split("/")).read_bytes()), candidate=commit_member, review=review(commit_member, commit_receipt, "completed")),
        ]
        doc = record(
            self.repo, self.out, pages, lanes, self.legacy(commit), coordination=coords,
            members=[
                {"name": open_member, "role": "declared"},
                {"name": done_member, "role": "declared"},
                {"name": commit_member, "role": "declared"},
            ],
            custody="inspect-named-members",
        )
        doc["roots"]["members_book"] = book
        path = save(self.out, "terminal.json", doc)
        proc = run(["view", "--input", path, "--json"])
        self.assertEqual(proc.returncode, 1, proc.stderr.decode())
        body = view_json(proc)
        lives = {lane["id"]: lane["lifecycle"] for lane in body["lanes"]}
        self.assertEqual(lives["open"], "open-accepted-not-terminal")
        self.assertEqual(lives["done"], "completed")
        self.assertEqual(lives["commit"], "open-commit-custody-unverified")
        self.assertIsNone(body["elected"])

    def test_missing_partial_retrospective_ambiguous_and_stale(self):
        book = os.path.abspath(os.path.join(self.tmp, "book"))
        os.makedirs(book)
        note = "notes/old.md"
        write(os.path.join(self.repo, note), "old\n")
        ret = os.path.join(self.repo, "notes", "return.md")
        write(ret, "Did.\nBlocked.\nNeed.\n")
        commit = commit_all(self.repo)
        common = [PY, "-B", CAPTURE]
        reserved = subprocess.run(
            common + ["reserve", "--book", book, "--submission", "desk-retro", "--name", "retro-return",
                      "--origin-book", "00.00.10.work", "--origin-page", "0508.desk-alpha", "--origin-batch", "05.01",
                      "--expected-output", note, "--submitter", "Desk Test", "--reviewer", "Codex Prime",
                      "--release", "fixture"],
            capture_output=True,
        )
        self.assertEqual(reserved.returncode, 0, reserved.stdout.decode())
        retro = reserved.stdout.decode().splitlines()[0].split(" ", 1)[1]
        captured = subprocess.run(
            common + ["capture", "--book", book, "--submission", "desk-retro", "--return-file", ret,
                      "--source-root", self.repo, "--artifact", f"{note}|{note}",
                      "--retrospective", "--source-commit", commit],
            capture_output=True,
        )
        self.assertEqual(captured.returncode, 0, captured.stdout.decode() + captured.stderr.decode())
        inspected = subprocess.run([PY, "-B", INSPECT, "inspect", "--book", book, "--member", retro, "--json"], capture_output=True)
        receipt = json.loads(inspected.stdout)["capture"]["receipt_sha256"]
        partial = subprocess.run(
            common + ["reserve", "--book", book, "--submission", "desk-partial", "--name", "partial-return",
                      "--origin-book", "00.00.10.work", "--origin-page", "0509.desk-beta", "--origin-batch", "05.02",
                      "--expected-output", note, "--submitter", "Desk Test", "--reviewer", "Codex Prime",
                      "--release", "fixture"],
            capture_output=True,
        )
        self.assertEqual(partial.returncode, 0, partial.stdout.decode())
        partial_member = partial.stdout.decode().splitlines()[0].split(" ", 1)[1]
        retro_rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        partial_rel = "00.kernel/00.00.10.work/0509.desk-beta/05.02.md"
        missing_rel = "00.kernel/00.00.10.work/0510.desk-gamma/05.03.md"
        ambiguous_rel = "00.kernel/00.00.10.work/0511.desk-delta/05.04.md"
        stale_rel = "00.kernel/00.00.10.work/0512.desk-epsilon/05.05.md"
        self.page(retro_rel, "Retro", member=retro, receipt=receipt)
        self.page(partial_rel, "Partial", member=partial_member, receipt="ab" * 32)
        self.page(missing_rel, "Missing", member="0199.missing-member-0001", receipt="cd" * 32)
        self.page(ambiguous_rel, "Ambiguous", extra="## Return later\nNot a pointer.\n")
        self.page(stale_rel, "Stale")
        commit = commit_all(self.repo)
        specs = [
            ("p-retro", retro_rel, "retro", "0508.desk-alpha/05.01", retro),
            ("p-partial", partial_rel, "partial", "0509.desk-beta/05.02", partial_member),
            ("p-missing", missing_rel, "missing", "0510.desk-gamma/05.03", "0199.missing-member-0001"),
            ("p-ambiguous", ambiguous_rel, "ambiguous", "0511.desk-delta/05.04", None),
            ("p-stale", stale_rel, "stale", "0512.desk-epsilon/05.05", None),
        ]
        pages, lanes, coords, members = [], [], [], []
        for page_id, rel, lane_id, batch, member in specs:
            digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
            pages.append({"id": page_id, "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"})
            lanes.append({"id": lane_id, "page_id": page_id, "worker": None, "task": f"{lane_id} stays attention."})
            if lane_id == "stale":
                coords.append(coord(batch, "a" * 64))
            elif member:
                coords.append(coord(batch, digest, candidate=member))
                members.append({"name": member, "role": "declared"})
            else:
                coords.append(coord(batch, digest))
        doc = record(
            self.repo, self.out, pages, lanes, self.legacy(commit), coordination=coords, members=members,
            custody="inspect-named-members",
        )
        doc["roots"]["members_book"] = book
        path = save(self.out, "custody.json", doc)
        proc = run(["view", "--input", path, "--json"])
        self.assertEqual(proc.returncode, 1, proc.stderr.decode())
        body = view_json(proc)
        lives = {lane["id"]: lane for lane in body["lanes"]}
        self.assertEqual(lives["retro"]["lifecycle"], "conflict-candidate")
        self.assertIn("reserved", " ".join(body["attention"]))
        self.assertTrue(any("0199.missing-member-0001" in item for item in body["attention"]))
        self.assertTrue(any("ambiguous" in item.lower() or "return pointer" in item.lower() for item in body["attention"] + [lives["ambiguous"]["lifecycle"]]))
        self.assertEqual(lives["stale"]["lifecycle"], "unprojected")
        self.assertIn("different source sha256", lives["stale"]["unprojected_reason"])

    def test_revise_refuses_stale_hash_and_derived_view(self):
        self.page("00.kernel/00.00.10.work/0508.desk-alpha/05.01.md", "Alpha")
        commit = commit_all(self.repo)
        rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
        pages = [{"id": "p-alpha", "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"}]
        lanes = [{"id": "alpha", "page_id": "p-alpha", "worker": None, "task": "Original goal lane."}]
        doc = record(self.repo, self.out, pages, lanes, self.legacy(commit), coordination=[coord("0508.desk-alpha/05.01", digest)])
        path = save(self.out, "original.json", doc)
        original = Path(path).read_bytes()
        changed = json.loads(original)
        changed["goal"]["statement"] = "Director changed the goal through a new record."
        changed["revision"] = {
            "reason": "Director changed the goal.",
            "authorizing": "0508.return-capture/05.19 #04",
            "predecessor": sha(original),
        }
        submission = save(self.out, "submission.json", changed)
        stale = run(["revise", "--record", path, "--expected", "b" * 64, "--submission", submission, "--out", os.path.join(self.out, "stale.json")])
        self.assertEqual(stale.returncode, 2)
        self.assertIn(b"expected hash", stale.stderr)
        self.assertEqual(Path(path).read_bytes(), original)
        self.assertFalse(os.path.exists(os.path.join(self.out, "stale.json")))
        new_path = os.path.join(self.out, "revised.json")
        ok = run(["revise", "--record", path, "--expected", sha(original), "--submission", submission, "--out", new_path])
        self.assertEqual(ok.returncode, 0, ok.stderr.decode())
        self.assertEqual(Path(path).read_bytes(), original)
        wrote = json.loads(ok.stdout)
        self.assertEqual(wrote["authority"], "not a worker command")
        self.assertEqual(json.loads(Path(new_path).read_text(encoding="utf-8"))["goal"]["statement"], changed["goal"]["statement"])
        viewed = run(["view", "--input", path, "--json"])
        self.assertEqual(viewed.returncode, 0, viewed.stderr.decode())
        candidate = os.path.join(self.out, "candidate.md")
        rendered = run(["view", "--input", path, "--json", "--candidate", candidate])
        self.assertEqual(rendered.returncode, 0, rendered.stderr.decode())
        text = Path(candidate).read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# DERIVED VIEW"))
        Path(candidate).write_text(text + "\nEdited by hand.\n", encoding="utf-8")
        rejected = run(["view", "--input", candidate, "--json"])
        self.assertEqual(rejected.returncode, 2)
        self.assertEqual(Path(self.repo, "legacy.md").read_text(encoding="utf-8"), "legacy\n")

    def test_malformed_paths_pins_failure_and_output(self):
        self.page("00.kernel/00.00.10.work/0508.desk-alpha/05.01.md", "Alpha")
        commit = commit_all(self.repo)
        rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
        pages = [{"id": "p-alpha", "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"}]
        lanes = [{"id": "alpha", "page_id": "p-alpha", "worker": None, "task": "Guard this lane."}]
        doc = record(self.repo, self.out, pages, lanes, self.legacy(commit), coordination=[coord("0508.desk-alpha/05.01", digest)])
        path = save(self.out, "good.json", doc)
        bad_json = os.path.join(self.out, "bad.json")
        Path(bad_json).write_text("{", encoding="utf-8")
        self.assertEqual(run(["view", "--input", bad_json]).returncode, 2)
        duplicate = Path(path).read_text(encoding="utf-8").replace("{", '{"schema": "desk-state/1", ', 1)
        dup = os.path.join(self.out, "dup.json")
        Path(dup).write_text(duplicate, encoding="utf-8")
        self.assertEqual(run(["view", "--input", dup]).returncode, 2)
        unknown = json.loads(Path(path).read_text(encoding="utf-8"))
        unknown["extra"] = True
        unk = save(self.out, "unknown.json", unknown)
        self.assertEqual(run(["view", "--input", unk]).returncode, 2)
        typed = json.loads(Path(path).read_text(encoding="utf-8"))
        typed["lanes"][0]["worker"] = 4
        self.assertEqual(run(["view", "--input", save(self.out, "type.json", typed)]).returncode, 2)
        escaped = json.loads(Path(path).read_text(encoding="utf-8"))
        escaped["pages"][0]["path"] = "00.kernel/../../secret.md"
        self.assertEqual(run(["view", "--input", save(self.out, "escape.json", escaped)]).returncode, 2)
        pinned = json.loads(Path(path).read_text(encoding="utf-8"))
        pinned["tools"]["batch_observe"]["sha256"] = "c" * 64
        self.assertEqual(run(["view", "--input", save(self.out, "pin.json", pinned)]).returncode, 2)
        flag = os.path.join(self.tmp, "LAUNCHED")
        fake = os.path.join(self.tmp, "fake-observe.py")
        Path(fake).write_text(f"open(r'{flag}', 'w', encoding='utf-8').write('x')\n", encoding="utf-8")
        moved = json.loads(Path(path).read_text(encoding="utf-8"))
        moved["tools"]["batch_observe"]["path"] = fake
        moved["tools"]["batch_observe"]["sha256"] = sha(Path(fake).read_bytes())
        self.assertEqual(run(["view", "--input", save(self.out, "moved.json", moved)]).returncode, 2)
        self.assertFalse(os.path.exists(flag))
        missing = json.loads(Path(path).read_text(encoding="utf-8"))
        missing["pages"][0]["path"] = "00.kernel/00.00.10.work/0508.desk-alpha/05.99.md"
        missed = run(["view", "--input", save(self.out, "missing-blob.json", missing), "--json"])
        self.assertEqual(missed.returncode, 1, missed.stderr.decode())
        missed_body = view_json(missed)
        self.assertEqual(missed_body["lanes"][0]["lifecycle"], "observation-failed")
        self.assertIsNone(missed_body["lanes"][0]["source"])
        raised = json.loads(Path(path).read_text(encoding="utf-8"))
        raised["bounds"]["max_sources"] = 100
        self.assertEqual(run(["view", "--input", save(self.out, "cap.json", raised)]).returncode, 2)
        tiny = json.loads(Path(path).read_text(encoding="utf-8"))
        tiny["bounds"]["max_source_bytes"] = 20
        self.assertEqual(run(["view", "--input", save(self.out, "tiny.json", tiny)]).returncode, 2)
        keep = os.path.join(self.repo, "00.kernel", "00.live.md")
        write(keep, "KEEP\n")
        protected = run(["view", "--input", path, "--candidate", keep])
        self.assertEqual(protected.returncode, 2)
        self.assertEqual(Path(keep).read_text(encoding="utf-8"), "KEEP\n")
        goal = os.path.join(self.repo, "00.kernel", "00.00.10.work", "0401.goal", "06.01.md")
        write(goal, "KEEP GOAL\n")
        self.assertEqual(run(["view", "--input", path, "--candidate", goal]).returncode, 2)
        self.assertEqual(Path(goal).read_text(encoding="utf-8"), "KEEP GOAL\n")
        out_dir = os.path.join(self.out, "run")
        os.makedirs(out_dir)
        candidate = os.path.join(out_dir, "missing-dir", "candidate.md")
        partial = run(["view", "--input", path, "--out", out_dir, "--candidate", candidate])
        self.assertEqual(partial.returncode, 2, partial.stderr.decode())
        self.assertTrue(os.path.exists(os.path.join(out_dir, "view.json")))
        self.assertTrue(os.path.exists(os.path.join(out_dir, "PARTIAL.txt")))
        written = Path(out_dir, "view.json").read_bytes()
        again = run(["view", "--input", path, "--out", out_dir, "--candidate", candidate])
        self.assertEqual(again.returncode, 2)
        self.assertEqual(Path(out_dir, "view.json").read_bytes(), written)
        self.assertFalse(os.path.exists(candidate))

    def test_linked_path_is_refused_when_the_platform_allows_it(self):
        self.page("00.kernel/00.00.10.work/0508.desk-alpha/05.01.md", "Alpha")
        commit = commit_all(self.repo)
        rel = "00.kernel/00.00.10.work/0508.desk-alpha/05.01.md"
        digest = sha(Path(self.repo, *rel.split("/")).read_bytes())
        pages = [{"id": "p-alpha", "repository": self.repo, "path": rel, "commit": commit, "observation": "git-blob"}]
        lanes = [{"id": "alpha", "page_id": "p-alpha", "worker": None, "task": "Link guard."}]
        doc = record(self.repo, self.out, pages, lanes, self.legacy(commit), coordination=[coord("0508.desk-alpha/05.01", digest)])
        link = os.path.join(self.repo, "linked.md")
        linked = False
        try:
            os.symlink(os.path.join(self.repo, "legacy.md"), link)
            doc["legacy"] = {"repository": self.repo, "path": "linked.md", "commit": commit, "sha256": sha(b"legacy\n"), "note": "link"}
            linked = True
        except OSError:
            real = os.path.join(self.tmp, "real")
            os.makedirs(real)
            write(os.path.join(real, "legacy.md"), "legacy\n")
            junction = os.path.join(self.repo, "via")
            made = subprocess.run(["cmd", "/c", "mklink", "/J", junction, real], capture_output=True)
            if made.returncode != 0:
                self.skipTest(made.stderr.decode("utf-8", "replace") or "link creation unavailable")
            doc["legacy"] = {"repository": self.repo, "path": "via/legacy.md", "commit": commit, "sha256": sha(b"legacy\n"), "note": "junction"}
            linked = True
        self.assertTrue(linked)
        proc = run(["view", "--input", save(self.out, "link.json", doc)])
        self.assertEqual(proc.returncode, 2, proc.stderr.decode())
        self.assertIn(b"link", proc.stderr.lower())


if __name__ == "__main__":
    unittest.main()
