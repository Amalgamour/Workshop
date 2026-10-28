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


def robs(batch="05.01", lane=LANE, members=(), kind="live", commit=None, review_text=None, release_raw=None,
         ambiguities=(), reader_primary=None, typed_declaration=None, page_text=None):
    """A SYNTHETIC batch-observation/1 fixture in Grok-2's reader shape (reader05.13 CONTRACT §3)."""
    path = f"00.kernel/{BOOK}/{lane}/{batch}.md"
    return {"schema": "batch-observation/1", "tool": {"name": "fixture", "path": None, "sha256": None}, "authority": "none",
            "source": {"kind": kind, "repository": None, "path": path, "commit": commit,
                       "sha256": sha(page_text or f"{lane}/{batch}"), "bytes": 10, "label": "SYNTHETIC fixture"},
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


if __name__ == "__main__":
    unittest.main()
