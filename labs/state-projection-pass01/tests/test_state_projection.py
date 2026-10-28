"""Countercase tests for state_projection.py (0507.prime-support/05.12). Custody cases use the real pinned
return_capture.py (reserve, capture) and return_inspect.py on disposable books under the system temp directory.

  python -B -X dev tests/test_state_projection.py -v
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
TOOL = LAB / "state_projection.py"
RC = LAB.parent / "return-capture-pass01"
sys.path.insert(0, str(LAB))
import state_projection as sp  # noqa: E402

BOOK = "00.00.10.work"
R0 = "0" * 64


def obs(lane="0507.prime-support", batch="05.01", **over):
    o = {"id": f"{lane}/{batch}", "lane": lane, "batch": batch,
         "provenance": {"kind": "supplied-live", "commit": None, "page_sha256": None},
         "document": {"header_state": "draft"},
         "release": {"status": "recorded", "text": "Release: fixture"},
         "claim": {"status": "recorded", "actor": "fixture-actor"},
         "return": {"pointer": "absent", "members": [], "candidate": None},
         "review": {"status": "absent", "text": None, "binding": None},
         "publication": {"status": "unknown", "ref": None, "commit": None}}
    for k, v in over.items():
        o[k] = v
    return o


def bound(member, receipt, disposition="accepted", terminal="completed", followup=None):
    return {"status": "bound", "text": "fixture review", "binding": {"member": member, "receipt_sha256": receipt,
            "disposition": disposition, "terminal": terminal, "reviewer": "fixture-prime", "followup": followup}}


def tree(root: Path):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


def writable_retry(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="sp-" + self._testMethodName[5:25] + "-"))
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

    def member(self, name, page="0507.prime-support", batch="05.01", book=BOOK, capture=True, retrospective=False):
        self.n += 1
        out = self.rc("reserve", "--book", self.mbook, "--submission", f"fx-{name}", "--name", name, "--origin-book", book,
                      "--origin-page", page, "--origin-batch", batch, "--expected-output", "note.txt", "--submitter", "fixture",
                      "--reviewer", "fixture", "--release", "fixture only")
        folder = out.split()[1]
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

    def doc(self, batches, lanes=None):
        lanes = lanes or sorted({b["lane"] for b in batches}) or ["0507.prime-support"]
        return {"schema": "state-observations/1", "scope": {"book": BOOK, "lanes": lanes}, "members_book": str(self.mbook),
                "batches": batches}

    def run_cli(self, doc, inspect=True, code=None, raw=None):
        path = self.tmp / f"in-{len(list(self.tmp.glob('in-*')))}.json"
        path.write_bytes(raw if raw is not None else json.dumps(doc).encode())
        args = [sys.executable, "-B", str(TOOL), "project", "--input", str(path), "--json"] + (["--inspect"] if inspect else [])
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=300)
        self.assertEqual(r.stderr, "", r.stderr)
        if code is not None:
            self.assertEqual(r.returncode, code, r.stdout[:2000])
        return r.returncode, (json.loads(r.stdout) if r.stdout.startswith("{") else r.stdout)

    def row(self, proj, ident):
        return next(b for b in proj["batches"] if b["id"] == ident)


class TestClosure(Fixture):
    def test_01_text_only_accepted_cannot_close(self):
        m = self.member("alpha")
        o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None},
                   "review": {"status": "text", "text": "Accepted within scope,2026-10-27.", "binding": None}})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual(r["lifecycle"], "open-review-unresolved")
        self.assertEqual(p["lanes"]["0507.prime-support"]["open"], [o["id"]])
        self.assertEqual(p["lanes"]["0507.prime-support"]["completed"], [])
        _, p2 = self.run_cli(self.doc([o]), inspect=False, code=1)
        self.assertEqual(self.row(p2, o["id"])["lifecycle"], "open-review-unresolved")

    def test_02_bound_held_and_correction_remain_open_with_followup(self):
        for disp, life in (("held", "open-held"), ("correction-required", "open-correction-required")):
            with self.subTest(disposition=disp):
                m = self.member(f"held-{disp[:4]}")
                o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None},
                           "review": bound(m, self.receipt(m), disposition=disp, terminal=None, followup="0507.prime-support/05.02")})
                _, p = self.run_cli(self.doc([o]), code=1)
                r = self.row(p, o["id"])
                self.assertEqual((r["lifecycle"], r["followup"], r["facets"]["review"]["binding_check"]),
                                 (life, "0507.prime-support/05.02", "current"))
                self.assertEqual(p["lanes"]["0507.prime-support"]["open"], [o["id"]])

    def test_03_bound_accepted_with_terminal_completes_only_with_live_primary(self):
        m = self.member("done")
        o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": bound(m, self.receipt(m))})
        code, p = self.run_cli(self.doc([o]), code=0)
        r = self.row(p, o["id"])
        self.assertEqual((r["lifecycle"], r["attention"]), ("completed", []))
        self.assertEqual(r["facets"]["return"]["primary"], m)
        self.assertEqual(p["lanes"]["0507.prime-support"]["completed"], [o["id"]])
        self.assertEqual(p["authority"], sp.AUTHORITY)
        _, p2 = self.run_cli(self.doc([o]), inspect=False, code=1)
        self.assertEqual(self.row(p2, o["id"])["lifecycle"], "open-review-unresolved")
        nt = copy.deepcopy(o)
        nt["review"]["binding"]["terminal"] = None
        _, p3 = self.run_cli(self.doc([nt]), code=1)
        self.assertEqual(self.row(p3, o["id"])["lifecycle"], "open-accepted-not-terminal")

    def test_04_stale_receipt_or_member_requires_re_review(self):
        m = self.member("cur")
        old = self.member("old", batch="05.09")
        for name, binding in (("receipt", bound(m, "f" * 64)), ("member", bound(old, self.receipt(old)))):
            with self.subTest(stale=name):
                o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": binding})
                _, p = self.run_cli(self.doc([o]), code=1)
                r = self.row(p, o["id"])
                self.assertEqual((r["lifecycle"], r["facets"]["review"]["binding_check"]), ("open-re-review-required", "stale"))

    def test_05_two_matching_members_are_ambiguous_until_explicit_candidate(self):
        a, b = self.member("one"), self.member("two")
        o = obs(**{"return": {"pointer": "present", "members": [a, b], "candidate": None}, "review": bound(a, self.receipt(a))})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual(r["facets"]["return"]["custody"], "ambiguous")
        self.assertEqual(sorted(r["facets"]["return"]["ambiguous"]), sorted([a, b]))
        self.assertEqual(r["lifecycle"], "open-review-unresolved")
        nob = copy.deepcopy(o)
        nob["review"] = {"status": "absent", "text": None, "binding": None}
        _, p0 = self.run_cli(self.doc([nob]), code=1)
        self.assertEqual(self.row(p0, o["id"])["lifecycle"], "open-candidate-ambiguous")
        sel = copy.deepcopy(o)
        sel["return"]["candidate"] = a
        _, p2 = self.run_cli(self.doc([sel]), code=0)
        self.assertEqual((self.row(p2, o["id"])["lifecycle"], self.row(p2, o["id"])["facets"]["return"]["primary"]), ("completed", a))

    def test_06_same_page_batch_in_a_different_origin_book_is_not_primary(self):
        other = self.member("otherbook", book="00.00.99.other")
        o = obs(**{"return": {"pointer": "present", "members": [other], "candidate": None}, "review": bound(other, self.receipt(other))})
        _, p = self.run_cli(self.doc([o]), code=1)
        ret = self.row(p, o["id"])["facets"]["return"]
        self.assertEqual((ret["custody"], ret["primary"]), ("none", None))
        self.assertEqual(ret["secondary"][0]["origin"]["book"], "00.00.99.other")
        self.assertNotEqual(self.row(p, o["id"])["lifecycle"], "completed")
        cand = copy.deepcopy(o)
        cand["return"]["candidate"] = other
        _, p2 = self.run_cli(self.doc([cand]), code=1)
        self.assertEqual(self.row(p2, o["id"])["lifecycle"], "conflict-candidate")

    def test_07_primary_versus_historical_secondary_regardless_of_pointer_order(self):
        hist = self.member("hist", page="0509.pack-assembly", batch="05.01", retrospective=True)
        own = self.member("own", page="0508.return-capture", batch="05.10")
        o = obs(lane="0508.return-capture", batch="05.10",
                **{"return": {"pointer": "present", "members": [hist, own], "candidate": None}, "review": bound(own, self.receipt(own))})
        _, p = self.run_cli(self.doc([o]), code=0)
        ret = self.row(p, o["id"])["facets"]["return"]
        self.assertEqual((ret["primary"], [s["member"] for s in ret["secondary"]]), (own, [hist]))
        self.assertTrue(ret["secondary"][0]["retrospective"])
        self.assertEqual(self.row(p, o["id"])["lifecycle"], "completed")
        wrong = copy.deepcopy(o)
        wrong["review"] = bound(hist, self.receipt(hist))
        _, p2 = self.run_cli(self.doc([wrong]), code=1)
        self.assertEqual(self.row(p2, o["id"])["lifecycle"], "open-re-review-required")

    def test_08_live_custody_never_sets_a_commit_time_return(self):
        m = self.member("commit")
        o = obs(provenance={"kind": "supplied-commit", "commit": "c" * 40, "page_sha256": "d" * 64},
                **{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": bound(m, self.receipt(m))})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual(r["facets"]["return"]["custody"], "not-verifiable-here")
        self.assertEqual(r["live_custody"]["custody"], "primary")
        self.assertEqual(r["lifecycle"], "open-commit-custody-unverified")
        self.assertTrue(all(i["basis"] == "live" and i["observed_at"] for i in r["inspections"]))

    def test_09_published_held_work_stays_held(self):
        m = self.member("pub")
        o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None},
                   "review": bound(m, self.receipt(m), disposition="held", terminal=None, followup="next draft"),
                   "publication": {"status": "at-ref", "ref": "refs/remotes/origin/workshop", "commit": "e" * 40}})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual(r["lifecycle"], "open-held")
        self.assertIn("published bytes at a ref do not complete work", r["attention"])
        self.assertEqual(r["facets"]["publication"]["status"], "at-ref")

    def test_10_multiple_open_lanes_and_items_are_all_listed(self):
        rows = [obs(lane="0504.app-entry", batch="05.15", **{"return": {"pointer": "present", "members": [], "candidate": None}}),
                obs(lane="0507.prime-support", batch="05.11"),
                obs(lane="0507.prime-support", batch="05.12", claim={"status": "absent", "actor": None}),
                obs(lane="0508.return-capture", batch="05.12", release={"status": "pending", "text": None},
                    claim={"status": "pending", "actor": None})]
        _, p = self.run_cli(self.doc(rows, lanes=["0504.app-entry", "0506.clerk-handoff", "0507.prime-support", "0508.return-capture"]),
                            inspect=False)
        L = p["lanes"]
        self.assertEqual(L["0504.app-entry"]["open"], ["0504.app-entry/05.15"])
        self.assertEqual(L["0507.prime-support"]["open"], ["0507.prime-support/05.11", "0507.prime-support/05.12"])
        self.assertEqual(L["0508.return-capture"]["awaiting_release"], ["0508.return-capture/05.12"])
        self.assertEqual(L["0508.return-capture"]["open"], [])
        self.assertEqual(L["0506.clerk-handoff"], {"open": [], "awaiting_release": [], "completed": [], "conflicts": []})
        self.assertNotIn("current", json.dumps(L))

    def test_11_missing_release_is_a_conflict_not_an_inferred_release(self):
        m = self.member("norel")
        o = obs(release={"status": "pending", "text": None},
                **{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": bound(m, self.receipt(m))})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual(r["lifecycle"], "conflict-missing-release")
        self.assertEqual(r["facets"]["release"]["status"], "pending")
        self.assertEqual(p["lanes"]["0507.prime-support"]["conflicts"], [o["id"]])

    def test_12_contradictory_review_and_incomplete_member(self):
        m = self.member("contra")
        o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None},
                   "review": bound(m, self.receipt(m), disposition="held", terminal="completed")})
        _, p = self.run_cli(self.doc([o]), code=1)
        self.assertEqual(self.row(p, o["id"])["lifecycle"], "conflict-contradictory-review")
        res = self.member("resv", capture=False)
        broken = self.member("broken")
        with open(self.mbook / broken / "return.md", "ab") as h:
            h.write(b"tampered\n")
        o2 = obs(batch="05.02", **{"return": {"pointer": "present", "members": [res, broken], "candidate": None}})
        _, p2 = self.run_cli(self.doc([o2]), code=1)
        ret = self.row(p2, o2["id"])["facets"]["return"]
        self.assertEqual(ret["custody"], "none")
        self.assertEqual(sorted(ret["problems"]), sorted([f"{res}: reserved", f"{broken}: incomplete"]))
        self.assertEqual(self.row(p2, o2["id"])["lifecycle"], "returned-awaiting-review")

    def test_13_malformed_or_duplicate_inputs_refuse_before_projection(self):
        good = self.doc([obs()])
        bad_cases = {
            "schema": dict(good, schema="state-observations/2"),
            "extra-key": dict(good, extra=1),
            "scope-lanes": dict(good, scope={"book": BOOK, "lanes": "0507.prime-support"}),
            "lane-out-of-scope": self.doc([obs(lane="0599.other")], lanes=["0507.prime-support"]),
            "dup-id": self.doc([obs(), obs()]),
            "id-mismatch": self.doc([dict(obs(), id="0507.prime-support/05.99")]),
            "binding-without-bound": self.doc([obs(review={"status": "text", "text": "x", "binding": bound("0101.a", R0)["binding"]})]),
            "bound-without-binding": self.doc([obs(review={"status": "bound", "text": "x", "binding": None})]),
            "candidate-not-member": self.doc([obs(**{"return": {"pointer": "present", "members": ["0101.a"], "candidate": "0102.b"}})]),
            "commit-without-hash": self.doc([obs(provenance={"kind": "supplied-commit", "commit": None, "page_sha256": None})]),
            "live-with-commit": self.doc([obs(provenance={"kind": "supplied-live", "commit": "c" * 40, "page_sha256": None})]),
            "members-type": self.doc([obs(**{"return": {"pointer": "present", "members": "0101.a", "candidate": None}})]),
            "disposition": self.doc([obs(review=bound("0101.a", R0, disposition="approved"))]),
            "terminal": self.doc([obs(review=bound("0101.a", R0, terminal="done"))]),
            "status-null": self.doc([obs(release={"status": None, "text": None})]),
            "batches-dict": dict(good, batches={}),
        }
        for name, doc in bad_cases.items():
            with self.subTest(case=name):
                _, out = self.run_cli(doc, code=2)
                self.assertTrue(isinstance(out, str) and out.startswith("refused: "), out)
        for name, raw in {"dup-key": b'{"schema": "state-observations/1", "schema": "x"}', "nan": b'{"a": NaN}',
                          "not-json": b"{", "list": b"[]"}.items():
            with self.subTest(raw=name):
                _, out = self.run_cli(None, raw=raw, code=2)
                self.assertTrue(out.startswith("refused: "))

    def test_14_wrong_or_missing_reader_or_helper_pin_refuses_before_launch(self):
        m = self.member("pin")
        doc = self.doc([obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}})])
        book_before = tree(self.mbook)
        for what in ("inspector-drift", "helper-drift", "inspector-missing"):
            with self.subTest(case=what):
                copy_dir = self.tmp / f"rc-{what}"
                copy_dir.mkdir()
                for f in ("return_inspect.py", "return_capture.py"):
                    shutil.copy(RC / f, copy_dir / f)
                target = copy_dir / ("return_capture.py" if what == "helper-drift" else "return_inspect.py")
                if what == "inspector-missing":
                    target.unlink()
                else:
                    with open(target, "ab") as h:
                        h.write(b"\n# drift\n")
                with mock.patch.object(sp, "RC_DIR", copy_dir), mock.patch.object(sp.subprocess, "run") as run:
                    with self.assertRaises(sp.Refusal):
                        sp.project(copy.deepcopy(doc), True, "x")
                    run.assert_not_called()
        self.assertEqual(tree(self.mbook), book_before)

    def test_15_malformed_inspector_report_is_a_failed_observation(self):
        m = self.member("mal")
        doc = self.doc([obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}})])
        for name, (stdout, exit_code) in {"not-json": (b"{x", 0), "schema": (b'{"schema":"other","member":"%s","status":"complete"}', 0),
                                          "exit-mismatch": (None, 1)}.items():
            with self.subTest(case=name):
                real = subprocess.run

                def fake(argv, **kw):
                    if "inspect" in argv:
                        out = real(argv, **kw)
                        body = out.stdout if stdout is None else stdout.replace(b"%s", m.encode())
                        return subprocess.CompletedProcess(argv, exit_code, body, b"")
                    return real(argv, **kw)
                with mock.patch.object(sp.subprocess, "run", fake):
                    p = sp.project(copy.deepcopy(doc), True, "x")
                r = p["batches"][0]
                self.assertEqual(r["inspections"][0]["observation"], "failed")
                self.assertEqual(r["facets"]["return"]["custody"], "observation-failed")
                self.assertNotEqual(r["lifecycle"], "completed")

    def test_16_worked_cases_w1_to_w7_with_corrected_expectations(self):
        own = self.member("w3", page="0504.app-entry", batch="05.15")
        res = self.member("w2", page="0507.prime-support", batch="05.11", capture=False)
        hist = self.member("w6h", page="0509.pack-assembly", batch="05.01", retrospective=True)
        prim = self.member("w6p", page="0508.return-capture", batch="05.10")
        broken = self.member("w5", page="0507.prime-support", batch="05.05")
        (self.mbook / broken / "receipt.json").unlink()
        text = {"status": "text", "text": "Accepted within scope,2026-10-27.", "binding": None}
        rows = [
            obs(lane="0504.app-entry", batch="05.14", review=text),                                                     # W1
            obs(lane="0507.prime-support", batch="05.11", **{"return": {"pointer": "pending", "members": [res], "candidate": None}}),  # W2
            obs(lane="0504.app-entry", batch="05.15", **{"return": {"pointer": "present", "members": [own], "candidate": None}}),     # W3
            obs(lane="0507.prime-support", batch="05.09", document={"header_state": "draft; awaiting Director release"}, review=text),  # W4
            obs(lane="0507.prime-support", batch="05.05", **{"return": {"pointer": "present", "members": [broken], "candidate": None}}),  # W5
            obs(lane="0508.return-capture", batch="05.10", review=bound(prim, "f" * 64),
                **{"return": {"pointer": "present", "members": [hist, prim], "candidate": None}}),                        # W6
        ]
        lanes = ["0504.app-entry", "0506.clerk-handoff", "0507.prime-support", "0508.return-capture"]
        _, p = self.run_cli(self.doc(rows, lanes=lanes), code=1)
        life = {r["id"]: r["lifecycle"] for r in p["batches"]}
        self.assertEqual(life, {"0504.app-entry/05.14": "open-review-unresolved", "0507.prime-support/05.11": "claimed",
                                "0504.app-entry/05.15": "returned-awaiting-review", "0507.prime-support/05.09": "open-review-unresolved",
                                "0507.prime-support/05.05": "returned-awaiting-review", "0508.return-capture/05.10": "open-re-review-required"})
        self.assertEqual(self.row(p, "0507.prime-support/05.09")["facets"]["document"]["header_state"], "draft; awaiting Director release")
        w5 = self.row(p, "0507.prime-support/05.05")["facets"]["return"]
        self.assertEqual((w5["custody"], w5["problems"]), ("none", [f"{broken}: incomplete"]))
        w6 = self.row(p, "0508.return-capture/05.10")["facets"]["return"]
        self.assertEqual((w6["primary"], w6["secondary"][0]["member"]), (prim, hist))
        self.assertEqual(p["lanes"]["0506.clerk-handoff"]["open"], [])                                                    # W7
        self.assertEqual(p["lanes"]["0504.app-entry"]["completed"], [])

    def test_17_no_input_store_code_or_git_mutation(self):
        m = self.member("still")
        o = obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": bound(m, self.receipt(m))})
        path = self.tmp / "frozen.json"
        path.write_bytes(json.dumps(self.doc([o])).encode())
        ws = LAB.parent.parent

        def git(*a):
            return subprocess.run(["git", "-C", str(ws), *a], capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0")).stdout
        before = (tree(self.mbook), path.read_bytes(), tree(LAB.parent / "state-projection-pass01"), tree(RC),
                  git("rev-parse", "HEAD"), git("diff", "--cached", "--name-only"))
        tmp_before = sorted(p.name for p in self.tmp.iterdir())
        r = subprocess.run([sys.executable, "-B", str(TOOL), "project", "--input", str(path), "--inspect"], capture_output=True,
                           text=True, encoding="utf-8", timeout=300)
        self.assertEqual((r.returncode, r.stderr), (0, ""), r.stdout)
        self.assertIn("completed", r.stdout)
        self.assertIn(sp.AUTHORITY, r.stdout)
        after = (tree(self.mbook), path.read_bytes(), tree(LAB.parent / "state-projection-pass01"), tree(RC),
                 git("rev-parse", "HEAD"), git("diff", "--cached", "--name-only"))
        self.assertEqual(before, after)
        self.assertEqual(sorted(p.name for p in self.tmp.iterdir()), tmp_before)
        self.assertFalse(any(p.suffix == ".pyc" for p in LAB.rglob("*")))


class TestRetrospective(Fixture):
    """05.13, SP-05: a same-origin retrospective capture is historical, never a current primary."""

    def test_18_sole_same_origin_retrospective_cannot_complete(self):
        retro = self.member("retro", retrospective=True)
        o = obs(**{"return": {"pointer": "present", "members": [retro], "candidate": None}, "review": bound(retro, self.receipt(retro))})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        ret = r["facets"]["return"]
        self.assertEqual((ret["custody"], ret["primary"]), ("none", None))
        self.assertEqual(ret["secondary"], [{"member": retro, "origin": {"book": BOOK, "page": "0507.prime-support", "batch": "05.01"},
                                             "retrospective": True, "historical": "same-origin retrospective"}])
        self.assertEqual(r["lifecycle"], "open-review-unresolved")
        self.assertEqual(p["lanes"]["0507.prime-support"]["completed"], [])

    def test_19_explicit_historical_candidate_is_a_conflict(self):
        retro = self.member("retroc", retrospective=True)
        o = obs(**{"return": {"pointer": "present", "members": [retro], "candidate": retro}, "review": bound(retro, self.receipt(retro))})
        _, p = self.run_cli(self.doc([o]), code=1)
        r = self.row(p, o["id"])
        self.assertEqual((r["facets"]["return"]["custody"], r["lifecycle"]), ("candidate-historical", "conflict-candidate"))
        self.assertIn("declared candidate is a retrospective (historical) capture", r["attention"])
        self.assertEqual(p["lanes"]["0507.prime-support"]["conflicts"], [o["id"]])

    def test_20_historical_plus_current_in_both_orders(self):
        retro = self.member("hist2", retrospective=True)
        cur = self.member("cur2")
        for order in ([retro, cur], [cur, retro]):
            with self.subTest(order=order):
                o = obs(**{"return": {"pointer": "present", "members": order, "candidate": None}, "review": bound(cur, self.receipt(cur))})
                _, p = self.run_cli(self.doc([o]), code=0)
                r = self.row(p, o["id"])
                ret = r["facets"]["return"]
                self.assertEqual((ret["custody"], ret["primary"], ret["ambiguous"]), ("primary", cur, []))
                self.assertEqual([x["member"] for x in ret["secondary"]], [retro])
                self.assertEqual(r["lifecycle"], "completed")
                wrong = copy.deepcopy(o)
                wrong["review"] = bound(retro, self.receipt(retro))
                _, p2 = self.run_cli(self.doc([wrong]), code=1)
                self.assertEqual(self.row(p2, o["id"])["lifecycle"], "open-re-review-required")
                cand = copy.deepcopy(o)
                cand["return"]["candidate"] = retro
                _, p3 = self.run_cli(self.doc([cand]), code=1)
                self.assertEqual(self.row(p3, o["id"])["lifecycle"], "conflict-candidate")

    def test_21_retrospective_must_be_an_actual_boolean(self):
        m = self.member("flag")
        doc = self.doc([obs(**{"return": {"pointer": "present", "members": [m], "candidate": None}, "review": bound(m, self.receipt(m))})])
        real = subprocess.run
        for name, change in {"missing": lambda c: c.pop("retrospective"), "string": lambda c: c.update(retrospective="false"),
                             "int": lambda c: c.update(retrospective=0), "null": lambda c: c.update(retrospective=None)}.items():
            with self.subTest(case=name):
                def fake(argv, change=change, **kw):
                    out = real(argv, **kw)
                    if "inspect" in argv:
                        d = json.loads(out.stdout)
                        change(d["capture"])
                        return subprocess.CompletedProcess(argv, out.returncode, json.dumps(d).encode(), b"")
                    return out
                with mock.patch.object(sp.subprocess, "run", fake):
                    p = sp.project(copy.deepcopy(doc), True, "x")
                r = p["batches"][0]
                self.assertEqual((r["inspections"][0]["observation"], r["inspections"][0]["reason"]),
                                 ("failed", "complete report lacks a boolean retrospective flag"))
                self.assertNotEqual(r["lifecycle"], "completed")


if __name__ == "__main__":
    unittest.main()
