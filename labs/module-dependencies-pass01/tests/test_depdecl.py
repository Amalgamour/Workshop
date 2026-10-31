"""Tests for depdecl.py (0517.dependencies 05.01). Labelled SYNTHETIC declarations in disposable folders, plus a read-only
query of the lab's prime-cycle-chain prototype set. Nothing named by a declaration is imported or executed.

  python -B -X dev tests/test_depdecl.py -v
"""
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
sys.path.insert(0, str(LAB))
import depdecl as dd  # noqa: E402

TOOL = LAB / "depdecl.py"
CHAIN = LAB / "examples" / "prime-cycle-chain" / "set.json"
CUT = "f" * 40
H = lambda s: hashlib.sha256(s.encode()).hexdigest()


def addr(page="0599.synthetic", face="05.01", file="05.01.md", book="00.00.10.work", repo="lib-build"):
    return {"repository": repo, "book": book, "page": page, "face_or_pass": face, "file": file}


def mref(path, repo="lib-build"):
    return {"repository": repo, "path": path}


def req(rid, target_path=None, pin=None, kind="runtime-code", mech="import", cond=None, target=None, avail="not-applicable", pin_required=None):
    c = {"applies": "always", "id": None, "statement": None, "status": "applicable"} if cond is None else \
        {"applies": "conditional", "id": cond[0], "statement": "SYNTHETIC condition " + cond[0], "status": cond[1]}
    return {"id": rid, "kind": kind, "target": target or {"module": mref(target_path)},
            "pin": None if pin is None else {"sha256": pin, "bytes": 1}, "pin_required": (pin is not None) if pin_required is None else pin_required,
            "mechanism": mech, "condition": c, "availability": avail, "reason": "SYNTHETIC reason", "source_ref": None}


def decl(did, path, reqs=(), version=1, impl=None, zero=False, links=None, unknown=None, supersedes=None, repo="lib-build"):
    return {"schema": "module-declaration/1", "declaration_id": did, "version": version, "status": "prototype",
            "module": {"repository": repo, "path": path, "name": did, "purpose": "SYNTHETIC fixture module", "interface": ["x"],
                       "limits": ["SYNTHETIC"], "home": None},
            "implementation": {"sha256": impl or H(did + str(version)), "bytes": 1,
                               "basis": {"kind": "git-blob", "repository": repo, "commit": CUT, "path": path}},
            "coverage": {"entry_points": ["main"], "method": "SYNTHETIC fixture", "complete_claim": False},
            "no_requirements": zero, "requirements": list(reqs), "withheld": [],
            "provenance": {"links": [{"role": "assignment", "address": addr(), "sha256": H("page"), "commit": CUT, "status": "pinned", "note": ""}]
                           if links is None else links, "unknown": unknown or []},
            "supersedes": supersedes}


class Desk(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dd-" + self._testMethodName[5:18] + "-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_set(self, decls, name="set", fixtures=(), select=(), bounds=None, raw_files=None):
        root = self.tmp / name
        (root / "d").mkdir(parents=True)
        rows = []
        for i, d in enumerate(decls):
            b = d if isinstance(d, bytes) else (json.dumps(d, indent=1) + "\n").encode()
            (root / "d" / f"{i:02d}.json").write_bytes(b)
            rows.append({"file": f"d/{i:02d}.json", "sha256": hashlib.sha256(b).hexdigest()})
        fx = []
        for i, (path, data) in enumerate(fixtures):
            (root / "f").mkdir(exist_ok=True)
            (root / "f" / f"{i}.bin").write_bytes(data)
            fx.append({"module": mref(path), "file": f"f/{i}.bin", "sha256": hashlib.sha256(data).hexdigest()})
        s = {"schema": "module-declaration-set/1", "set_id": "synthetic", "coverage": "SYNTHETIC fixtures", "declarations": raw_files or rows,
             "fixtures": fx, "select": list(select), "bounds": bounds or {"max_records": 50, "max_file_bytes": 65536, "max_depth": 16, "max_output_bytes": 1048576}}
        (root / "set.json").write_text(json.dumps(s, indent=1))
        return root / "set.json"

    def cli(self, *args):
        p = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, timeout=120)
        out = p.stdout.decode("utf-8")
        return p.returncode, (json.loads(out) if out.startswith("{") else out)

    def finds(self, r):
        return [f["finding"] for e in (r["requirements"] or []) for f in e["findings"]]


class TestRootsAndRecords(Desk):
    def test_01_absent_root_differs_from_explicit_zero_requirements(self):
        s = self.write_set([decl("leaf", "lab/leaf.py", zero=True)])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/leaf.py", "--transitive")
        self.assertEqual((code, r["root"]["state"], r["requirements"], r["status"]), (0, "declared-dependency-free", [], "complete-for-declared-coverage"))
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/absent.py")
        self.assertEqual((code, r["root"]["state"], r["requirements"], r["status"]), (1, "undeclared", None, "incomplete"))
        bad = decl("ambig", "lab/a.py")
        code, out = self.cli("validate", "--set", self.write_set([bad], name="s2"))
        self.assertEqual(code, 2)
        self.assertIn("an empty requirements list needs no_requirements true", out)
        both = decl("both", "lab/b.py", [req("x", "lab/leaf.py")], zero=True)
        self.assertIn("no_requirements true needs an empty requirements list", self.cli("validate", "--set", self.write_set([both], name="s3"))[1])

    def test_02_missing_transitive_record_is_a_finding_not_an_empty_list(self):
        s = self.write_set([decl("a", "lab/a.py", [req("b", "lab/b.py")]), decl("b", "lab/b.py", [req("c", "lab/c.py")])])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/a.py", "--transitive")
        self.assertEqual(code, 1)
        miss = [e for e in r["requirements"] if e["resolution"] == "record-missing"]
        self.assertEqual([(e["requirement_id"], e["path"]) for e in miss], [("c", ["lib-build:lab/a.py", "lib-build:lab/b.py"])])
        code, d = self.cli("requires", "--set", s, "--module", "lib-build:lab/a.py")  # direct only
        self.assertEqual([e["requirement_id"] for e in d["requirements"]], ["b"])

    def test_03_duplicate_and_conflicting_identity(self):
        a = decl("a", "lab/a.py", zero=True)
        code, r = self.cli("validate", "--set", self.write_set([a, a]))
        self.assertEqual((code, [f["finding"] for f in r["set_findings"]]), (1, ["duplicate"]))
        a2 = copy.deepcopy(a)
        a2["module"]["purpose"] = "SYNTHETIC different content, same id and version"
        code, r = self.cli("validate", "--set", self.write_set([a, a2], name="s2"))
        self.assertIn("identity-conflict", [f["finding"] for f in r["set_findings"]])
        twin = decl("a-other", "lab/a.py", zero=True, impl=a["implementation"]["sha256"])
        cons = decl("c", "lab/c.py", [req("a", "lab/a.py", pin=a["implementation"]["sha256"])])
        code, r = self.cli("requires", "--set", self.write_set([a, twin, cons], name="s3"), "--module", "lib-build:lab/c.py")
        self.assertEqual(r["requirements"][0]["resolution"], "identity-conflict")
        self.assertIn("identity-conflict", [f["finding"] for f in r["set_findings"]])

    def test_04_same_path_other_repository_and_same_page_other_book_are_distinct(self):
        here = decl("here", "lab/x.py", zero=True, links=[{"role": "review", "address": addr(page="0599.synthetic", face="05.01", book="00.00.10.work"),
                                                          "sha256": H("a"), "commit": CUT, "status": "pinned", "note": ""}])
        there = decl("there", "lab/x.py", zero=True, repo="other-repo",
                     links=[{"role": "review", "address": addr(page="0599.synthetic", face="05.01", book="00.00.20.other"),
                             "sha256": H("b"), "commit": CUT, "status": "pinned", "note": ""}])
        cons = decl("c", "lab/c.py", [req("x", "lab/x.py")])
        s = self.write_set([here, there, cons])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/c.py")
        self.assertEqual((code, r["requirements"][0]["resolution"], r["requirements"][0]["resolved_to"]["declaration_id"]), (0, "single-unpinned", "here"))
        _, r2 = self.cli("requires", "--set", s, "--module", "other-repo:lab/x.py")
        self.assertEqual(r2["root"]["provenance"]["links"][0]["address"]["book"], "00.00.20.other")
        bare = copy.deepcopy(here)
        bare["provenance"]["links"][0]["address"]["book"] = "0515"
        self.assertIn("must be a full book name", self.cli("validate", "--set", self.write_set([bare], name="s2"))[1])


class TestVersionsAndChange(Desk):
    def test_05_changed_bytes_identity_and_pin_differs(self):
        a1 = decl("a", "lab/a.py", zero=True, impl=H("bytes-1"))
        b = decl("b", "lab/b.py", [req("a", "lab/a.py", pin=H("bytes-1"))])
        a2 = decl("a", "lab/a.py", zero=True, version=2, impl=hashlib.sha256(b"changed bytes").hexdigest(), supersedes={"declaration_id": "a", "version": 1})
        s = self.write_set([a2, b], fixtures=[("lib-build:lab/a.py".split(":")[1], b"changed bytes"), ("lab/a.py", b"unknown bytes")])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/b.py")
        e = r["requirements"][0]
        self.assertEqual((code, e["resolution"]), (1, "pin-differs"))
        self.assertEqual(e["findings"][0]["pinned"], H("bytes-1"))
        code, r = self.cli("identity", "--set", s)
        self.assertEqual([x["result"] for x in r["fixtures"]], ["identical", "changed"])
        code, r = self.cli("impacted", "--set", s, "--module", "lib-build:lab/a.py", "--implementation", a2["implementation"]["sha256"])
        self.assertEqual([(c["consumer"], c["against_implementation"]) for c in r["consumers"]], [("lib-build:lab/b.py", "pin-differs")])
        self.assertEqual(r["status"], "candidates-for-review")

    def test_06_ambiguous_versions_need_an_explicit_selection_never_the_highest(self):
        v1, v2 = decl("a", "lab/a.py", zero=True), decl("a", "lab/a.py", zero=True, version=2, supersedes={"declaration_id": "a", "version": 1})
        c = decl("c", "lab/c.py", [req("a", "lab/a.py")])
        code, r = self.cli("requires", "--set", self.write_set([v1, v2, c]), "--module", "lib-build:lab/c.py")
        self.assertEqual((code, r["requirements"][0]["resolution"]), (1, "ambiguous-version"))
        _, r = self.cli("requires", "--set", self.write_set([v1, v2, c], name="s2"), "--module", "lib-build:lab/a.py")
        self.assertEqual(r["root"]["state"], "ambiguous-version")
        s3 = self.write_set([v1, v2, c], name="s3", select=[{"module": mref("lab/a.py"), "declaration_id": "a", "version": 1}])
        code, r = self.cli("requires", "--set", s3, "--module", "lib-build:lab/c.py")
        self.assertEqual((code, r["requirements"][0]["resolution"], r["requirements"][0]["resolved_to"]["version"]), (0, "selected", 1))
        bad = self.write_set([v1, c], name="s4", select=[{"module": mref("lab/a.py"), "declaration_id": "a", "version": 9}])
        self.assertIn("does not declare", self.cli("validate", "--set", bad)[1])

    def test_07_multiple_consumers_and_transitive_impact_with_provenance(self):
        base = decl("base", "lab/base.py", zero=True)
        p = base["implementation"]["sha256"]
        u1 = decl("u1", "lab/u1.py", [req("base", "lab/base.py", pin=p)])
        u2 = decl("u2", "lab/u2.py", [req("base", "lab/base.py")], links=[], unknown=["SYNTHETIC: no workflow page recorded"])
        top = decl("top", "lab/top.py", [req("u1", "lab/u1.py")])
        code, r = self.cli("impacted", "--set", self.write_set([base, u1, u2, top]), "--module", "lib-build:lab/base.py", "--implementation", p)
        self.assertEqual((code, r["finding_counts"]), (0, {}))  # declared bytes, no findings: exit 0 (CONTRACT §7)
        got ={(c["consumer"].split(":")[1], c["against_implementation"]) for c in r["consumers"]}
        self.assertEqual(got, {("lab/u1.py", "pin-matches"), ("lab/u2.py", "unpinned"), ("lab/top.py", "transitive: via lib-build:lab/u1.py")})
        u2row = next(c for c in r["consumers"] if c["consumer"].endswith("u2.py"))
        self.assertEqual(u2row["provenance"]["unknown"], ["SYNTHETIC: no workflow page recorded"])
        code, r = self.cli("impacted", "--set", self.write_set([base, u1], name="s2"), "--module", "lib-build:lab/base.py", "--implementation", H("never declared"))
        self.assertEqual(code, 1)
        self.assertIn("implementation-undeclared", r["finding_counts"])


class TestGraph(Desk):
    def test_08_diamond_is_shared_and_cycle_is_bounded(self):
        d = decl("d", "lab/d.py", zero=True)
        b, c = decl("b", "lab/b.py", [req("d", "lab/d.py")]), decl("c", "lab/c.py", [req("d", "lab/d.py")])
        a = decl("a", "lab/a.py", [req("b", "lab/b.py"), req("c", "lab/c.py")])
        code, r = self.cli("requires", "--set", self.write_set([a, b, c, d]), "--module", "lib-build:lab/a.py", "--transitive")
        self.assertEqual((code, r["status"], self.finds(r).count("shared")), (0, "complete-for-declared-coverage", 1))
        _, ex = self.cli("explain", "--set", self.write_set([a, b, c, d], name="s2"), "--module", "lib-build:lab/a.py", "--to", "lib-build:lab/d.py")
        self.assertEqual(sorted(p["path"][1] for p in ex["paths"]), ["lib-build:lab/b.py", "lib-build:lab/c.py"])
        x, y = decl("x", "lab/x.py", [req("y", "lab/y.py")]), decl("y", "lab/y.py", [req("x", "lab/x.py")])
        code, r = self.cli("requires", "--set", self.write_set([x, y], name="s3"), "--module", "lib-build:lab/x.py", "--transitive")
        cyc = [f for e in r["requirements"] for f in e["findings"] if f["finding"] == "cycle"]
        self.assertEqual((code, cyc[0]["cycle"]), (1, ["lib-build:lab/x.py", "lib-build:lab/y.py", "lib-build:lab/x.py"]))
        chain = [decl(f"n{i}", f"lab/n{i}.py", [req(f"n{i+1}", f"lab/n{i+1}.py")]) for i in range(6)] + [decl("n6", "lab/n6.py", zero=True)]
        code, r = self.cli("requires", "--set", self.write_set(chain, name="s4"), "--module", "lib-build:lab/n0.py", "--transitive", "--depth", "3")
        self.assertIn("depth-limit", self.finds(r))

    def test_09_conditions_and_environment_states_stay_distinct(self):
        e = decl("e", "lab/e.py", zero=True)
        a = decl("a", "lab/a.py", [req("e", "lab/e.py", cond=("flag", "unknown")),
                                   req("git", kind="environment", mech="subprocess", target={"environment": {"name": "git", "detail": "SYNTHETIC"}}, avail="unverified"),
                                   req("gpu", kind="environment", mech="read", target={"environment": {"name": "gpu", "detail": "SYNTHETIC"}}, avail="declared-unavailable"),
                                   req("tool", target={"external": {"name": "SYNTHETIC tool", "sha256": None}})])
        s = self.write_set([a, e])
        _, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/a.py", "--transitive")
        by = {x["requirement_id"]: x for x in r["requirements"]}
        self.assertEqual(by["e"]["condition"]["effective"], "unknown")
        self.assertIn("condition-unknown", [f["finding"] for f in by["e"]["findings"]])
        self.assertEqual([f["finding"] for f in by["git"]["findings"]], ["environment-unverified"])
        self.assertEqual([f["finding"] for f in by["gpu"]["findings"]], ["environment-unavailable"])
        self.assertEqual([f["finding"] for f in by["tool"]["findings"]], ["external-unverified"])
        self.assertEqual(r["status"], "incomplete")
        _, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/a.py", "--transitive", "--condition", "flag=inapplicable")
        e2 = next(x for x in r["requirements"] if x["requirement_id"] == "e")
        self.assertEqual((e2["condition"]["effective"], e2["condition"]["stated_by"]), ("inapplicable", "caller"))
        self.assertEqual(r["query"]["caller_conditions"], {"flag": "inapplicable"})
        self.assertNotIn("lib-build:lab/e.py", [c["module"] for c in r["coverage"]])  # not followed
        self.assertEqual(self.cli("requires", "--set", s, "--module", "lib-build:lab/a.py", "--condition", "flag=maybe")[0], 2)

    def test_10_provenance_unknown_unpinned_and_missing(self):
        nolinks = decl("n", "lab/n.py", zero=True, links=[], unknown=["SYNTHETIC: built before records were kept"])
        unp = decl("u", "lab/u.py", zero=True, links=[{"role": "source-stated", "address": addr(), "sha256": None, "commit": None, "status": "unpinned", "note": "x"}])
        _, r = self.cli("requires", "--set", self.write_set([nolinks]), "--module", "lib-build:lab/n.py")
        self.assertEqual(([f["finding"] for f in r["record_findings"]], r["status"]), (["provenance-unknown"], "incomplete"))
        _, r = self.cli("requires", "--set", self.write_set([unp], name="s2"), "--module", "lib-build:lab/u.py")
        self.assertEqual([f["finding"] for f in r["record_findings"]], ["provenance-unpinned"])
        silent = decl("s", "lab/s.py", zero=True, links=[], unknown=[])
        self.assertIn("no links needs at least one 'unknown'", self.cli("validate", "--set", self.write_set([silent], name="s3"))[1])
        lying = copy.deepcopy(unp)
        lying["provenance"]["links"][0]["status"] = "pinned"
        self.assertIn("pinned if and only if", self.cli("validate", "--set", self.write_set([lying], name="s4"))[1])


class TestInputsAndOutput(Desk):
    def test_11_malformed_inputs_are_refused(self):
        ok = decl("a", "lab/a.py", zero=True)
        cases = {
            "duplicate key": b'{"schema": "module-declaration/1", "schema": "x"}',
            "nan": json.dumps(dict(ok, version=1)).replace('"version": 1', '"version": NaN').encode(),
            "complete claim": dict(ok, coverage=dict(ok["coverage"], complete_claim=True)),
            "pin required without pin": decl("b", "lab/b.py", [req("x", "lab/x.py", pin_required=True)]),
            "unknown key": dict(ok, extra=1),
            "bad kind": decl("c", "lab/c.py", [dict(req("x", "lab/x.py"), kind="magic")]),
            "env kind mismatch": decl("e", "lab/e.py", [req("x", kind="environment", mech="read", target={"module": mref("lab/x.py")}, avail="unverified")]),
            "bad item": None,
        }
        for name, d in cases.items():
            if d is None:
                continue
            with self.subTest(case=name):
                code, out = self.cli("validate", "--set", self.write_set([d], name=name.replace(" ", "-")))
                self.assertEqual(code, 2, out)
                self.assertTrue(out.startswith("refused: "))

    def test_12_unsafe_paths_and_set_pins(self):
        s = self.write_set([decl("a", "lab/a.py", zero=True)])
        raw = json.loads(s.read_text())
        for name, f in {"dotdot": "../x.json", "absolute": "C:/x.json", "backslash": "d\\00.json"}.items():
            with self.subTest(path=name):
                bad = dict(raw, declarations=[{"file": f, "sha256": raw["declarations"][0]["sha256"]}])
                s.write_text(json.dumps(bad))
                self.assertEqual(self.cli("validate", "--set", s)[0], 2)
        s.write_text(json.dumps(dict(raw, declarations=[{"file": "d/00.json", "sha256": H("other")}])))
        code, out = self.cli("validate", "--set", s)
        self.assertEqual(code, 2)
        self.assertIn("set-pin-mismatch", out)
        self.assertEqual(self.cli("validate", "--set", "relative/set.json")[0], 2)
        target = self.tmp / "real"
        target.mkdir()
        link = self.tmp / "junction"
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
        if made.returncode != 0:
            self.skipTest("junction creation unavailable on this host")
        shutil.copytree(s.parent, target / "set")
        s2 = link / "set" / "set.json"
        s2.write_text(json.dumps(raw))
        code, out = self.cli("validate", "--set", s2)
        self.assertEqual(code, 2)
        self.assertIn("passes through a link", out)

    def test_13_bounds_and_occupied_or_partial_index(self):
        many = [decl(f"m{i}", f"lab/m{i}.py", zero=True) for i in range(5)]
        small = {"max_records": 3, "max_file_bytes": 65536, "max_depth": 16, "max_output_bytes": 1048576}
        self.assertIn("max_records", self.cli("validate", "--set", self.write_set(many, bounds=small))[1])
        tiny = dict(small, max_records=50, max_output_bytes=200)
        self.assertIn("over max_output_bytes", self.cli("requires", "--set", self.write_set(many, name="s2", bounds=tiny), "--module", "lib-build:lab/m0.py")[1])
        cap = dict(small, max_records=50, max_file_bytes=100)
        self.assertIn("byte bound", self.cli("validate", "--set", self.write_set(many, name="s3", bounds=cap))[1])
        s = self.write_set(many, name="s4")
        out = self.tmp / "index"
        code, r = self.cli("index", "--set", s, "--out", out)
        self.assertEqual((code, r["status"], r["modules"]), (0, "written", 5))
        idx = json.loads((out / "index.json").read_text())
        self.assertEqual(idx["derived_from"]["set_sha256"], hashlib.sha256(s.read_bytes()).hexdigest())
        code, again = self.cli("index", "--set", s, "--out", out)
        self.assertEqual(code, 2)
        self.assertIn("already exists", again)
        self.assertEqual(self.cli("index", "--set", s, "--out", s.parent / "inside")[0], 2)
        real = dd.write_file

        def flaky(p, data):
            if p.name == "INDEX-STATUS.json":
                raise OSError("injected interruption")
            return real(p, data)
        with mock.patch.object(dd, "write_file", flaky):
            with self.assertRaises(dd.PartialWrite):
                dd.cmd_index(dd.load_set(str(s)), str(self.tmp / "partial"))
        self.assertEqual(sorted(p.name for p in (self.tmp / "partial").iterdir()), ["index.json"])  # kept, not removed

    def test_14_delta_checks_the_declared_change_record(self):
        old = decl("a", "lab/a.py", [req("x", "lab/x.py"), req("y", "lab/y.py")])
        new = decl("a", "lab/a.py", [req("x", "lab/x.py", pin=H("x")), req("z", "lab/z.py")], version=2, impl=H("new"),
                   supersedes={"declaration_id": "a", "version": 1})
        f = {}
        for n, d in (("old", old), ("new", new)):
            f[n] = self.tmp / f"{n}.json"
            f[n].write_text(json.dumps(d))
        sh = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        ch = {"schema": "module-change/1", "module": mref("lab/a.py"), "authorized_by": {"address": addr(), "item": "#02"},
              "old": {"declaration_id": "a", "version": 1, "sha256": sh(f["old"])}, "new": {"declaration_id": "a", "version": 2, "sha256": sh(f["new"])},
              "implementation": {"sha256": H("new"), "bytes": 1}, "evidence": [{"role": "test", "address": None, "sha256": None, "note": "SYNTHETIC"}],
              "relationships": {"introduced": [{"requirement_id": "z", "reason": "SYNTHETIC"}],
                                "changed": [{"requirement_id": "x", "fields": ["pin", "pin_required"], "reason": "SYNTHETIC pin added"}],
                                "removed": [{"requirement_id": "y", "reason": "SYNTHETIC"}]}}
        cp = self.tmp / "change.json"
        cp.write_text(json.dumps(ch))
        code, r = self.cli("delta", "--old", f["old"], "--new", f["new"], "--change", cp)
        self.assertEqual((code, r["status"], r["computed"]), (0, "consistent", {"introduced": ["z"], "removed": ["y"], "changed": ["x"]}))
        ch["relationships"]["removed"] = []
        cp.write_text(json.dumps(ch))
        code, r = self.cli("delta", "--old", f["old"], "--new", f["new"], "--change", cp)
        self.assertEqual((code, r["status"], [x["what"] for x in r["findings"]]), (1, "inconsistent", ["relationships.removed"]))
        ch["authorized_by"]["item"] = "02"
        cp.write_text(json.dumps(ch))
        self.assertEqual(self.cli("delta", "--old", f["old"], "--new", f["new"], "--change", cp)[0], 2)


class TestRealChain(Desk):
    def test_15_prototype_chain_answers_without_modifying_inputs(self):
        before = {p: p.read_bytes() for p in CHAIN.parent.rglob("*") if p.is_file()}
        code, r = self.cli("requires", "--set", CHAIN, "--module", "lib-build:labs/prime-cycle-pass01/prime_cycle.py", "--transitive",
                           "--condition", "members-book=applicable")
        self.assertEqual((code, r["root"]["state"], r["status"]), (1, "declared", "incomplete"))
        missing = sorted({e["target"]["module"]["path"] for e in r["requirements"] if e["resolution"] == "record-missing"})
        self.assertEqual(missing, ["labs/prime-review-pass01/prime_review.py", "labs/return-capture-pass01/return_capture.py",
                                   "labs/return-capture-pass01/return_inspect.py", "labs/review-packet-pass01/review_packet.py"])
        self.assertEqual(self.finds(r).count("shared"), 1)
        code, imp = self.cli("impacted", "--set", CHAIN, "--module", "lib-build:labs/prime-support-pass01/clerk_adapter.py",
                             "--implementation", hashlib.sha256(b"SYNTHETIC changed clerk_adapter").hexdigest())
        got = sorted((c["consumer"].split("/")[-1], c["against_implementation"].split(":")[0]) for c in imp["consumers"])
        self.assertEqual(got, [("batch_observe.py", "pin-differs"), ("batch_observe.py", "transitive"), ("prime_cycle.py", "transitive"),
                               ("prime_support.py", "pin-differs")])
        self.assertEqual({p: p.read_bytes() for p in CHAIN.parent.rglob("*") if p.is_file()}, before)
        self.assertNotIn("import subprocess", TOOL.read_text(encoding="utf-8"))  # the tool cannot launch what it reads


if __name__ == "__main__":
    unittest.main()
