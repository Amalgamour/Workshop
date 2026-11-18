"""Integration tests for prime_brief.py (0507.prime-support/05.13), keyed to CONTRACT.md §C (E01-E19).
Custody uses the real pinned return_capture.py (reserve, capture) and return_inspect.py on disposable books under
the system temp directory. Reader observations are labelled fixtures; Grok-2's reader is never launched or imported.

  python -B -X dev tests/test_prime_brief.py -v
"""
import copy
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

LAB = Path(__file__).resolve().parents[1]
TOOL = LAB / "prime_brief.py"
LABS = LAB.parent
RC = LABS / "return-capture-pass01"
sys.path.insert(0, str(LAB))
import prime_brief as pb  # noqa: E402

BOOK = "00.00.10.work"
LANE = "0507.prime-support"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def robs(batch="05.01", lane=LANE, members=(), kind="live-file", commit=None, review_text=None, release_raw=None,
         ambiguities=(), reader_primary=None, typed_declaration=None, page_text=None):
    """A SYNTHETIC batch-observation/1 fixture in the accepted reader's actual shape (05.14: live-file, source time keys)."""
    path = f"00.kernel/{BOOK}/{lane}/{batch}.md"
    return {"schema": "batch-observation/1", "tool": {"name": "fixture", "path": None, "sha256": None}, "authority": "none",
            "source": {"kind": kind, "repository": None, "path": path, "commit": commit,
                       "sha256": sha(page_text or f"{lane}/{batch}"), "bytes": 10, "label": "SYNTHETIC fixture",
                       "time_basis": "live-read" if kind == "live-file" else kind,
                       "live_observed_at": "2026-10-28T00:00:00Z" if kind == "live-file" else None,
                       "observation_started_at": "2026-10-28T00:00:00Z" if kind == "live-file" else None,
                       "observation_finished_at": "2026-10-28T00:00:00Z" if kind == "live-file" else None},
            "page": {"book": BOOK, "page": lane, "batch": batch},
            "document": {"header_state_raw": "draft"},
            "assignment": {"executor_raw": "Executor: fixture.", "release_raw": release_raw, "claim_raw": None},
            "legacy": {"tool": None, "sha256": None, "sibling": None, "sibling_sha256": None, "kind": "page-return",
                       "status": "unsupported", "reason": "fixture", "revision_id": None, "execution": None, "whole": None, "review": None},
            "channels": {"legacy": True, "inventory": True, "revision_repaired": False},
            "sections": [], "fenced_headings": [],
            "pointers": [{"line": 40, "form": "return-pointer", "title": "Return pointer", "execution_raw": None,
                          "members": [{"name": m, "line": 41, "receipts": []} for m in members]}] if members else [],
            "assignment_mentions": [],
            "custody": {"basis": "live", "members_book": None, "package_at_commit": "not-established", "primary": reader_primary,
                        "primary_rule": "fixture", "observations": [{"member": m, "role": "not-observed"} for m in members]},
            "review": {"parser_object": None, "sections": [{"line": 50, "title": "Review", "text_raw": review_text}] if review_text else [],
                       "text_raw": review_text, "legacy_hashes": [], "binding": "unbound", "typed_declaration": typed_declaration},
            "ambiguities": list(ambiguities), "attention": []}


def coord(o, release="recorded", claim="recorded", candidate=None, review=None, publication=None):
    return {"label": "SUPPLIED", "batch_id": f"{o['page']['page']}/{o['page']['batch']}", "source_sha256": o["source"]["sha256"],
            "release": release, "claim": claim, "claim_actor": "fixture-actor", "candidate": candidate, "review": review,
            "publication": publication or {"status": "unknown", "ref": None, "commit": None}}


def decision(member, receipt, disposition="accepted", terminal="completed", followup=None):
    return {"member": member, "receipt_sha256": receipt, "disposition": disposition, "terminal": terminal,
            "reviewer": "fixture-prime", "followup": followup}


def tree(root: Path):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


def writable_retry(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pbr-" + self._testMethodName[5:25] + "-"))
        self.mbook = self.tmp / "book"
        self.mbook.mkdir()
        self.src = self.tmp / "src"
        self.src.mkdir()
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, onexc=writable_retry)

    def rc(self, *args):
        r = subprocess.run([sys.executable, "-B", str(RC / "return_capture.py"), *map(str, args)], capture_output=True,
                           text=True, encoding="utf-8", timeout=120)
        self.assertEqual((r.returncode, r.stderr), (0, ""), r.stdout)
        return r.stdout

    def member(self, name, page=LANE, batch="05.01", retrospective=False, capture=True):
        self.n += 1
        folder = self.rc("reserve", "--book", self.mbook, "--submission", f"fx-{name}", "--name", name, "--origin-book", BOOK,
                         "--origin-page", page, "--origin-batch", batch, "--expected-output", "note.txt", "--submitter", "fixture",
                         "--reviewer", "fixture", "--release", "fixture only").split()[1]
        if capture:
            (self.src / "note.txt").write_bytes(f"note {self.n}\n".encode())
            (self.src / f"{name}.md").write_bytes(f"Did {name}.\n".encode())
            extra = ["--retrospective", "--source-commit", "a" * 40] if retrospective else []
            self.rc("capture", "--book", self.mbook, "--submission", f"fx-{name}", "--return-file", self.src / f"{name}.md",
                    "--source-root", self.src, "--artifact", "note.txt|note.txt", *extra)
        return folder

    def receipt(self, folder):
        r = subprocess.run([sys.executable, "-B", str(RC / "return_inspect.py"), "inspect", "--book", str(self.mbook), "--member",
                            folder, "--json"], capture_output=True, timeout=120)
        return json.loads(r.stdout)["capture"]["receipt_sha256"]

    def doc(self, pairs, lanes=None):
        """pairs: [(reader observation, coordination record or None, label)]"""
        lanes = lanes or sorted({o["page"]["page"] for o, _, _ in pairs if o["page"]}) or [LANE]
        return {"schema": "prime-brief-input/1", "scope": {"book": BOOK, "lanes": lanes}, "members_book": str(self.mbook),
                "observations": [{"label": lab, "note": "fixture", "observation": o} for o, _, lab in pairs],
                "coordination": [c for _, c, _ in pairs if c is not None]}

    def run_cli(self, doc, inspect=True, code=None, raw=None, json_out=True):
        path = self.tmp / f"in-{len(list(self.tmp.glob('in-*')))}.json"
        path.write_bytes(raw if raw is not None else json.dumps(doc, ensure_ascii=False).encode("utf-8"))
        args = [sys.executable, "-B", str(TOOL), "brief", "--input", str(path)] + (["--json"] if json_out else []) + (["--inspect"] if inspect else [])
        r = subprocess.run(args, capture_output=True, timeout=300)
        self.assertEqual(r.stderr, b"", r.stderr)
        out = r.stdout.decode("utf-8")
        if code is not None:
            self.assertEqual(r.returncode, code, out[:3000])
        return r.returncode, (json.loads(out) if out.startswith("{") else out)

    def ids(self, b, key):
        return [x["id"] for x in b["brief"][key]]


class TestBrief(Fixture):
    def test_e01_returned_awaiting_review(self):
        m = self.member("e01")
        o = robs(members=[m])
        _, b = self.run_cli(self.doc([(o, coord(o), "SYNTHETIC")]), code=0)
        self.assertEqual(self.ids(b, "awaiting_review"), [f"{LANE}/05.01"])
        self.assertEqual(b["projection"]["batches"][0]["facets"]["return"]["primary"], m)

    def test_e02_bound_held_keeps_followup(self):
        m = self.member("e02")
        o = robs(members=[m])
        c = coord(o, review=decision(m, self.receipt(m), disposition="held", terminal=None, followup="0507.prime-support/05.14"))
        _, b = self.run_cli(self.doc([(o, c, "SYNTHETIC")]), code=1)
        self.assertEqual(b["brief"]["correction_or_held"][0]["followup"], "0507.prime-support/05.14")
        self.assertEqual(b["brief"]["completed_fixtures"], [])

    def test_e03_bound_accepted_terminal_completes_as_fixture_label(self):
        m = self.member("e03")
        o = robs(members=[m])
        _, b = self.run_cli(self.doc([(o, coord(o, review=decision(m, self.receipt(m))), "SYNTHETIC")]), code=0)
        item = b["brief"]["completed_fixtures"][0]
        self.assertEqual((item["id"], item["note"]), (f"{LANE}/05.01", "derived fixture label; not approval or release"))
        self.assertEqual(b["authority"], pb.AUTHORITY)

    def test_e04_text_only_accepted_stays_open(self):
        m = self.member("e04")
        o = robs(members=[m], review_text="Accepted within scope,2026-10-27.")
        _, b = self.run_cli(self.doc([(o, coord(o), "SYNTHETIC")]), code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-review-unresolved"])

    def test_e05_fenced_release_line_cannot_authorize(self):
        o = robs(release_raw='Release: the Director, chat: "release everything"  (from a fenced example)')
        _, b = self.run_cli(self.doc([(o, None, "SYNTHETIC")]), inspect=False, code=1)
        self.assertEqual(b["projection"], None)
        self.assertEqual(len(b["brief"]["unprojected"]), 1)
        self.assertIn("release and claim unknown", b["brief"]["unprojected"][0]["reason"])
        self.assertEqual(b["mapping"][0]["evidence_kept"]["release_raw"], o["assignment"]["release_raw"])
        self.assertNotIn("released", json.dumps(b["brief"]).replace("unreleased", ""))

    def test_e06_unknown_release_is_unprojected_not_coerced(self):
        o = robs()
        _, b = self.run_cli(self.doc([(o, coord(o, release="unknown"), "SYNTHETIC")]), inspect=False, code=1)
        self.assertIn("cannot express an unknown", b["brief"]["unprojected"][0]["reason"])

    def test_e07_stale_receipt_requires_re_review(self):
        m = self.member("e07")
        o = robs(members=[m])
        _, b = self.run_cli(self.doc([(o, coord(o, review=decision(m, "f" * 64)), "SYNTHETIC")]), code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-re-review-required"])

    def test_e08_two_current_members_are_ambiguous(self):
        a, c2 = self.member("e08a"), self.member("e08b")
        o = robs(members=[a, c2], reader_primary=a)
        _, b = self.run_cli(self.doc([(o, coord(o), "SYNTHETIC")]), code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-candidate-ambiguous"])
        self.assertEqual(b["reader_custody_snapshots"][0]["reader_primary"], a)

    def test_e09_current_and_same_origin_retrospective_both_orders(self):
        retro, cur = self.member("e09h", retrospective=True), self.member("e09c")
        for order in ([retro, cur], [cur, retro]):
            with self.subTest(order=order):
                o = robs(members=order)
                _, b = self.run_cli(self.doc([(o, coord(o, review=decision(cur, self.receipt(cur))), "SYNTHETIC")]), code=0)
                ret = b["projection"]["batches"][0]["facets"]["return"]
                self.assertEqual((ret["primary"], [s["member"] for s in ret["secondary"]]), (cur, [retro]))
                self.assertEqual(self.ids(b, "completed_fixtures"), [f"{LANE}/05.01"])

    def test_e10_sole_retrospective_never_completes(self):
        retro = self.member("e10", retrospective=True)
        o = robs(members=[retro])
        _, b = self.run_cli(self.doc([(o, coord(o, review=decision(retro, self.receipt(retro))), "SYNTHETIC")]), code=1)
        self.assertEqual(b["brief"]["completed_fixtures"], [])
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-review-unresolved"])

    def test_e11_explicit_retrospective_candidate_is_a_conflict(self):
        retro = self.member("e11", retrospective=True)
        o = robs(members=[retro])
        _, b = self.run_cli(self.doc([(o, coord(o, candidate=retro, review=decision(retro, self.receipt(retro))), "SYNTHETIC")]), code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["conflicts"]], ["conflict-candidate"])

    def test_e12_changed_source_against_decision(self):
        m = self.member("e12")
        o = robs(members=[m])
        c = coord(o, review=decision(m, self.receipt(m)))
        c["source_sha256"] = sha("an earlier page version")
        _, b = self.run_cli(self.doc([(o, c, "SYNTHETIC")]), code=1)
        self.assertEqual(b["projection"], None)
        self.assertIn("different source sha256", b["brief"]["unprojected"][0]["reason"])

    def test_e13_commit_source_is_not_recast_live(self):
        m = self.member("e13")
        o = robs(members=[m], kind="git-blob", commit="c" * 40)
        _, b = self.run_cli(self.doc([(o, coord(o, review=decision(m, self.receipt(m))), "SYNTHETIC")]), code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-commit-custody-unverified"])
        row = b["projection"]["batches"][0]
        self.assertEqual((row["provenance"]["kind"], row["facets"]["return"]["custody"], row["live_custody"]["custody"]),
                         ("supplied-commit", "not-verifiable-here", "primary"))
        self.assertTrue(all(i["basis"] == "live" for i in row["inspections"]))
        self.assertIn("supplied, not verified here", " ".join(b["mapping"][0]["decisions"]))

    def test_e14_published_held_stays_held(self):
        m = self.member("e14")
        o = robs(members=[m])
        c = coord(o, review=decision(m, self.receipt(m), disposition="held", terminal=None),
                  publication={"status": "at-ref", "ref": "refs/remotes/origin/fixture", "commit": "e" * 40})
        _, b = self.run_cli(self.doc([(o, c, "SYNTHETIC")]), code=1)
        self.assertEqual(self.ids(b, "correction_or_held"), [f"{LANE}/05.01"])
        self.assertIn("published bytes at a ref do not complete work", b["brief"]["correction_or_held"][0]["reason"])

    def test_e15_multiple_lanes_all_listed(self):
        m = self.member("e15", page="0504.app-entry", batch="05.15")
        o1 = robs(lane="0504.app-entry", batch="05.15", members=[m])
        o2 = robs(lane=LANE, batch="05.13")
        o3 = robs(lane="0508.return-capture", batch="05.14")
        pairs = [(o1, coord(o1), "SYNTHETIC"), (o2, coord(o2), "SYNTHETIC"), (o3, coord(o3, release="pending", claim="pending"), "SYNTHETIC")]
        _, b = self.run_cli(self.doc(pairs, lanes=["0504.app-entry", LANE, "0508.return-capture"]), code=0)
        self.assertEqual(self.ids(b, "awaiting_review"), ["0504.app-entry/05.15"])
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["claimed"])
        self.assertEqual(self.ids(b, "unreleased"), ["0508.return-capture/05.14"])
        self.assertNotIn("current_work", json.dumps(b))

    def test_e16_derived_from_retained_reader_summary(self):
        """DERIVED-FROM-RETAINED-SUMMARY: facts from 0508 reader05.13/verification.json demo summary only."""
        ws = LABS.parent
        page = "00.kernel/00.00.10.work/0508.return-capture/05.10.md"
        blob = subprocess.run(["git", "-C", str(ws), "show", f"4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5:{page}"], capture_output=True).stdout
        o = robs(lane="0508.return-capture", batch="05.10", members=["0128.pack-assembly-0501", "0129.assembly-capture-0510"],
                 kind="git-blob", commit="4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5",
                 review_text="Accepted within scope,2026-10-27. (summary placeholder: full review text not retained)",
                 reader_primary="0129.assembly-capture-0510")
        o["source"].update(sha256=hashlib.sha256(blob).hexdigest(), bytes=len(blob), label="DERIVED-FROM-RETAINED-SUMMARY")
        o["legacy"].update(status="unsupported", reason="ambiguous heading line 47", revision_id=None)
        doc = self.doc([(o, coord(o), "DERIVED-FROM-RETAINED-SUMMARY")])
        doc["members_book"] = None
        _, b = self.run_cli(doc, inspect=False, code=1)
        self.assertEqual(b["inputs"][0]["label"], "DERIVED-FROM-RETAINED-SUMMARY")
        self.assertIsNone(b["mapping"][0]["evidence_kept"]["legacy"]["revision_id"])
        self.assertEqual(b["reader_custody_snapshots"][0]["reader_primary"], "0129.assembly-capture-0510")
        row = b["projection"]["batches"][0]
        self.assertEqual((row["facets"]["return"]["custody"], row["lifecycle"]), ("not-verifiable-here", "open-review-unresolved"))

    def test_e17_malformed_inputs_refuse(self):
        o = robs()
        good = self.doc([(o, coord(o), "SYNTHETIC")])
        cases = {"schema": dict(good, schema="prime-brief-input/2"), "extra": dict(good, extra=1),
                 "label": self.doc([(o, coord(o), "REAL")]),
                 "reader-schema": self.doc([(dict(o, schema="batch-observation/2"), coord(o), "SYNTHETIC")]),
                 "reader-authority": self.doc([(dict(o, authority="Prime"), coord(o), "SYNTHETIC")]),
                 "pointer-members-type": self.doc([(dict(o, pointers=[{"members": "0101.a"}]), coord(o), "SYNTHETIC")]),
                 "ambiguities-type": self.doc([(dict(o, ambiguities=[1]), coord(o), "SYNTHETIC")]),
                 "coord-label": self.doc([(o, dict(coord(o), label="DIRECTOR"), "SYNTHETIC")]),
                 "coord-release": self.doc([(o, dict(coord(o), release="approved"), "SYNTHETIC")]),
                 "coord-review": self.doc([(o, coord(o, review={"member": "0101.a"}), "SYNTHETIC")]),
                 "dup-coord": dict(good, coordination=[coord(o), coord(o)]),
                 "orphan-coord": dict(good, coordination=[coord(robs(batch="05.09"))]),
                 "dup-observation": self.doc([(o, coord(o), "SYNTHETIC"), (copy.deepcopy(o), None, "SYNTHETIC")]),
                 "out-of-scope-lane": dict(self.doc([(robs(lane="0599.other"), None, "SYNTHETIC")]), scope={"book": BOOK, "lanes": [LANE]}),
                 "other-book": self.doc([(dict(o, page={"book": "00.00.99.x", "page": LANE, "batch": "05.01"}), None, "SYNTHETIC")])}
        for name, doc in cases.items():
            with self.subTest(case=name):
                _, out = self.run_cli(doc, inspect=False, code=2)
                self.assertTrue(isinstance(out, str) and out.startswith("refused: "), out)
        for name, raw in {"dup-key": b'{"schema": "prime-brief-input/1", "schema": "x"}', "nan": b'{"a": NaN}', "bad": b"{"}.items():
            with self.subTest(raw=name):
                _, out = self.run_cli(None, raw=raw, code=2)
                self.assertTrue(out.startswith("refused: "))

    def test_e18_projection_inspector_or_helper_drift_refuses_before_launch(self):
        m = self.member("e18")
        o = robs(members=[m])
        doc = self.doc([(o, coord(o), "SYNTHETIC")])
        work = self.tmp / "labs"
        for what in ("projection", "inspector", "helper"):
            with self.subTest(case=what):
                if work.exists():
                    shutil.rmtree(work, onexc=writable_retry)
                shutil.copytree(LABS / "state-projection-pass01", work / "state-projection-pass01", ignore=shutil.ignore_patterns("tests", "__pycache__"))
                (work / "return-capture-pass01").mkdir()
                for f in ("return_capture.py", "return_inspect.py"):
                    shutil.copy(RC / f, work / "return-capture-pass01" / f)
                target = {"projection": work / "state-projection-pass01" / "state_projection.py",
                          "inspector": work / "return-capture-pass01" / "return_inspect.py",
                          "helper": work / "return-capture-pass01" / "return_capture.py"}[what]
                with open(target, "ab") as h:
                    h.write(b"\n# drift\n")
                with mock.patch.object(pb, "PROJECTION", work / "state-projection-pass01" / "state_projection.py"):
                    if what == "projection":
                        with mock.patch("subprocess.run") as run:
                            with self.assertRaises(pb.Refusal):
                                pb.build(copy.deepcopy(doc), True, "x")
                            run.assert_not_called()
                    else:
                        with mock.patch.object(pb, "PROJECTION_SHA256", hashlib.sha256(target.parent.parent.joinpath(
                                "state-projection-pass01", "state_projection.py").read_bytes()).hexdigest()):
                            with mock.patch("subprocess.run") as run:
                                with self.assertRaises(pb.Refusal):
                                    pb.build(copy.deepcopy(doc), True, "x")
                                run.assert_not_called()

    def test_e19_utf8_and_no_mutation(self):
        m = self.member("e19")
        o = robs(members=[m], review_text="Prüfung offen — 未決")
        doc = self.doc([(o, coord(o), "SYNTHETIC")])
        path = self.tmp / "frozen.json"
        path.write_bytes(json.dumps(doc, ensure_ascii=False).encode("utf-8"))
        ws = LABS.parent

        def git(*a):
            return subprocess.run(["git", "-C", str(ws), *a], capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0")).stdout
        before = (tree(self.mbook), path.read_bytes(), tree(LAB), tree(LABS / "state-projection-pass01"), tree(RC),
                  tree(LABS / "batch-observation-pass01"), git("rev-parse", "HEAD"), git("diff", "--cached", "--name-only"))
        tmp_before = sorted(p.name for p in self.tmp.iterdir())
        r = subprocess.run([sys.executable, "-B", str(TOOL), "brief", "--input", str(path), "--inspect"], capture_output=True, timeout=300)
        text = r.stdout.decode("utf-8")
        self.assertEqual((r.returncode, r.stderr), (1, b""))
        self.assertIn("Other open (1)", text)
        jr = subprocess.run([sys.executable, "-B", str(TOOL), "brief", "--input", str(path), "--json"], capture_output=True, timeout=300)
        self.assertIn("Prüfung offen — 未決", jr.stdout.decode("utf-8"))
        after = (tree(self.mbook), path.read_bytes(), tree(LAB), tree(LABS / "state-projection-pass01"), tree(RC),
                 tree(LABS / "batch-observation-pass01"), git("rev-parse", "HEAD"), git("diff", "--cached", "--name-only"))
        self.assertEqual(before, after)
        self.assertEqual(sorted(p.name for p in self.tmp.iterdir()), tmp_before)
        self.assertFalse(any(p.suffix == ".pyc" for p in LAB.rglob("*")))
        src = TOOL.read_text(encoding="utf-8")
        self.assertNotIn("batch_observe", src)
        self.assertNotIn("import prime_support", src)


# ---------- 05.14: the real accepted reader on disposable Git/book fixtures ----------

READER = LABS / "batch-observation-pass01" / "batch_observe.py"
PAGE_DIR = f"00.kernel/{BOOK}/{LANE}"
GENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
            GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")


def page_text(lines, review="PENDING."):
    body = "\n".join(lines)
    return (f"# 05 — Fixture batch\nversion: 001\nstate: draft\nFace: 05\nPPPP: 0507\nbook: {BOOK}\n\n## Assignment\n"
            f"Executor: Claude. Reviewer: Codex Prime.\nRelease and claim: recorded in the Return pointer.\n\n"
            f"## #01 — Do it\nWrite out.txt.\n\n## Return pointer\nRelease: fixture release.\nClaim: fixture claim.\n{body}\n\n"
            f"## Review — Codex Prime\n{review}\n")


class RealReader(Fixture):
    def setUp(self):
        super().setUp()
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.mbook = self.repo / "00.kernel" / BOOK
        self.mbook.mkdir(parents=True)

    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.repo), *a], capture_output=True, env=GENV, check=True).stdout.decode().strip()

    def write_page(self, batch, text):
        path = self.repo / PAGE_DIR / f"{batch}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return f"{PAGE_DIR}/{batch}.md"

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")
        return self.git("rev-parse", "HEAD")

    def observe(self, rel, mode="live", commit=None, members=True):
        args = [sys.executable, "-B", str(READER), "observe", "--json"]
        if mode == "live":
            args += ["--repo", str(self.repo), "--live", "--path", rel]
        elif mode == "git":
            args += ["--repo", str(self.repo), "--commit", commit, "--path", rel]
        else:
            args += ["--supplied", str(self.repo / rel), "--path", rel]
        if members and mode != "supplied":
            args += ["--members-book", str(self.mbook)]
        r = subprocess.run(args, capture_output=True, timeout=120)
        self.assertEqual(r.stderr, b"", r.stderr)
        self.assertIn(r.returncode, (0, 1), r.stdout[:500])
        return r.stdout, json.loads(r.stdout)

    def brief(self, obs, coords, inspect=True, code=None):
        doc = {"schema": "prime-brief-input/1", "scope": {"book": BOOK, "lanes": [LANE]}, "members_book": str(self.mbook),
               "observations": [{"label": "SUPPLIED", "note": "real reader report, unchanged", "observation": o} for o in obs],
               "coordination": coords}
        return self.run_cli(doc, inspect=inspect, code=code)

    def stated(self, member, receipt):
        return f"Execution: returned. Member {member}. Receipt sha256 {receipt}. Fresh verify: result complete."


class TestRealReader(RealReader):
    def test_r01_live_file_report_maps_unchanged(self):
        m = self.member("r01", batch="05.01")
        rel = self.write_page("05.01", page_text([self.stated(m, self.receipt(m))]))
        raw, o = self.observe(rel)
        self.assertEqual(o["source"]["kind"], "live-file")
        _, b = self.brief([o], [coord(o)], code=0)
        self.assertEqual(b["inputs"][0]["observation_sha256"], pb.canonical_sha(json.loads(raw)))
        self.assertEqual(self.ids(b, "awaiting_review"), [f"{LANE}/05.01"])
        self.assertEqual(b["projection"]["batches"][0]["provenance"]["kind"], "supplied-live")
        self.assertEqual(b["mapping"][0]["evidence_kept"]["live_read"]["live_observed_at"], o["source"]["live_observed_at"])

    def test_r02_git_blob_report_is_commit_basis(self):
        m = self.member("r02", batch="05.02")
        rel = self.write_page("05.02", page_text([self.stated(m, self.receipt(m))]))
        commit = self.commit()
        _, o = self.observe(rel, mode="git", commit=commit)
        self.assertEqual((o["source"]["kind"], o["source"]["commit"]), ("git-blob", commit))
        _, b = self.brief([o], [coord(o, review=decision(m, self.receipt(m)))], code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-commit-custody-unverified"])

    def test_r03_supplied_text_stays_unprojected(self):
        rel = self.write_page("05.03", page_text(["Execution: IN PROGRESS"]))
        _, o = self.observe(rel, mode="supplied")
        self.assertEqual(o["source"]["kind"], "supplied-text")
        _, b = self.brief([o], [coord(o)], code=1)
        self.assertIn("supplied text has no commit or live basis", b["brief"]["unprojected"][0]["reason"])

    def test_r04_current_versus_same_origin_retrospective_both_orders(self):
        retro, cur = self.member("r04h", batch="05.04", retrospective=True), self.member("r04c", batch="05.04")
        for i, order in enumerate(([retro, cur], [cur, retro])):
            with self.subTest(order=order):
                rel = self.write_page("05.04", page_text([self.stated(x, self.receipt(x)) for x in order]))
                _, o = self.observe(rel)
                _, b = self.brief([o], [coord(o, review=decision(cur, self.receipt(cur)))], code=0)
                ret = b["projection"]["batches"][0]["facets"]["return"]
                self.assertEqual((ret["primary"], [x["member"] for x in ret["secondary"]]), (cur, [retro]))
                self.assertEqual(self.ids(b, "completed_fixtures"), [f"{LANE}/05.04"])
                roles = {x["member"]: x["role"] for x in b["reader_custody_snapshots"][0]["roles"]}
                self.assertEqual(roles[retro], "same-page-retrospective")

    def test_r05_stale_receipt_requires_re_review(self):
        m = self.member("r05", batch="05.05")
        rel = self.write_page("05.05", page_text([self.stated(m, self.receipt(m))]))
        _, o = self.observe(rel)
        _, b = self.brief([o], [coord(o, review=decision(m, "f" * 64))], code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-re-review-required"])

    def test_r06_stale_source_against_decision(self):
        m = self.member("r06", batch="05.06")
        rel = self.write_page("05.06", page_text([self.stated(m, self.receipt(m))]))
        _, old = self.observe(rel)
        c = coord(old, review=decision(m, self.receipt(m)))
        self.write_page("05.06", page_text([self.stated(m, self.receipt(m)), "Note: page edited after the decision."]))
        _, new = self.observe(rel)
        self.assertNotEqual(old["source"]["sha256"], new["source"]["sha256"])
        _, b = self.brief([new], [c], code=1)
        self.assertIn("different source sha256", b["brief"]["unprojected"][0]["reason"])

    def test_r07_conflicting_stated_receipts_make_the_pointer_ambiguous(self):
        m = self.member("r07", batch="05.07")
        rel = self.write_page("05.07", page_text([self.stated(m, self.receipt(m)), "Again. Member " + m + ". Receipt sha256 " + "e" * 64 + "."]))
        _, o = self.observe(rel)
        self.assertIn("conflicting-stated-receipts", o["attention"])
        _, b = self.brief([o], [coord(o)], code=1)
        row = b["projection"]["batches"][0]
        self.assertEqual(row["facets"]["return"]["pointer"], "ambiguous")
        item = (b["brief"]["awaiting_review"] + b["brief"]["other_open"])[0]
        self.assertIn("conflicting-stated-receipts", item["reason"])

    def test_r08_real_pending_review_section(self):
        m = self.member("r08", batch="05.08")
        rel = self.write_page("05.08", page_text([self.stated(m, self.receipt(m))], review="PENDING."))
        _, o = self.observe(rel)
        _, b = self.brief([o], [coord(o)], code=0)
        self.assertEqual(b["projection"]["batches"][0]["facets"]["review"]["status"], "pending")
        self.assertEqual(self.ids(b, "awaiting_review"), [f"{LANE}/05.08"])

    def test_r09_accepted_without_terminal_stays_open(self):
        m = self.member("r09", batch="05.09")
        rel = self.write_page("05.09", page_text([self.stated(m, self.receipt(m))], review="Accepted within scope."))
        _, o = self.observe(rel)
        _, b = self.brief([o], [coord(o, review=decision(m, self.receipt(m), terminal=None))], code=1)
        self.assertEqual([x["lifecycle"] for x in b["brief"]["other_open"]], ["open-accepted-not-terminal"])
        self.assertEqual(b["brief"]["completed_fixtures"], [])

    def test_r10_assignment_mention_is_not_pointer_ambiguity(self):
        m = self.member("r10", batch="05.10")
        other = self.member("r10b", batch="05.10")  # named only in an assignment sentence, never by a pointer
        text = page_text([self.stated(m, self.receipt(m))]).replace("Write out.txt.", f"Write out.txt.\n{other} captures the evidence.")
        rel = self.write_page("05.10", text)
        _, o = self.observe(rel)
        self.assertIn("assignment-mention-not-pointer", o["ambiguities"])
        _, b = self.brief([o], [coord(o)], code=0)  # reader codes are shown on items; exit counts projection attention + unprojected
        self.assertIn("assignment-mention-not-pointer", b["brief"]["awaiting_review"][0]["reason"])
        ret = b["projection"]["batches"][0]["facets"]["return"]
        self.assertEqual((ret["pointer"], ret["members_named"]), ("present", [m]))

    def test_v_malformed_real_reports_refuse_before_projection_or_launch(self):
        m = self.member("v", batch="05.11")
        rel = self.write_page("05.11", page_text([self.stated(m, self.receipt(m))]))
        _, o = self.observe(rel)

        def drop(path):
            def f(x):
                t = x
                for k in path[:-1]:
                    t = t[k]
                del t[path[-1]]
            return f

        def put(path, value):
            def f(x):
                t = x
                for k in path[:-1]:
                    t = t[k]
                t[path[-1]] = value
            return f
        variants = {"missing-document-header": drop(("document", "header_state_raw")), "missing-release-raw": drop(("assignment", "release_raw")),
                    "missing-source-time": drop(("source", "live_observed_at")), "missing-custody": drop(("custody",)),
                    "missing-review-sections": drop(("review", "sections")), "missing-legacy-reason": drop(("legacy", "reason")),
                    "pointer-member-no-name": put(("pointers", 0, "members", 0), {}), "source-bytes-str": put(("source", "bytes"), "10"),
                    "ambiguities-int": put(("ambiguities",), [1]), "schema": put(("schema",), "batch-observation/2"),
                    "custody-obs-role-list": put(("custody", "observations", 0, "role"), [])}
        for name, mutate in variants.items():
            with self.subTest(case=name):
                bad = copy.deepcopy(o)
                mutate(bad)
                doc = {"schema": "prime-brief-input/1", "scope": {"book": BOOK, "lanes": [LANE]}, "members_book": str(self.mbook),
                       "observations": [{"label": "SUPPLIED", "note": "x", "observation": bad}], "coordination": [coord(o)]}
                with mock.patch.object(pb, "load_projection") as lp, mock.patch("subprocess.run") as run:
                    with self.assertRaises(pb.Refusal):
                        pb.build(doc, True, "x")
                    lp.assert_not_called()
                    run.assert_not_called()
        for name, label in {"list-label": ["SUPPLIED"], "dict-label": {"a": 1}, "int-label": 1}.items():
            with self.subTest(label=name):
                doc = {"schema": "prime-brief-input/1", "scope": {"book": BOOK, "lanes": [LANE]}, "members_book": str(self.mbook),
                       "observations": [{"label": label, "note": "x", "observation": o}], "coordination": [coord(o)]}
                _, out = self.run_cli(doc, code=2)
                self.assertTrue(out.startswith("refused: "), out)
        for name, raw in {"nan": b'{"schema": "prime-brief-input/1", "x": NaN}', "dup": b'{"schema": "a", "schema": "b"}'}.items():
            with self.subTest(raw=name):
                _, out = self.run_cli(None, raw=raw, code=2)
                self.assertTrue(out.startswith("refused: "))

    def test_m01_reader_and_brief_leave_repo_book_and_git_unchanged(self):
        m = self.member("m01", batch="05.12")
        rel = self.write_page("05.12", page_text([self.stated(m, self.receipt(m))]))
        commit = self.commit()
        before = tree(self.repo)
        _, o1 = self.observe(rel)
        _, o2 = self.observe(rel, mode="git", commit=commit)
        self.brief([o1], [coord(o1)])
        self.brief([o2], [coord(o2)])
        self.assertEqual(tree(self.repo), before)
        self.assertEqual(self.git("rev-parse", "HEAD"), commit)
        self.assertEqual(self.git("status", "--porcelain=v1", "-uall"), "")


if __name__ == "__main__":
    unittest.main()
