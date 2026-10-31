"""Regression tests for the 0517 05.02 repair: D-01 honest reverse bound, D-02 identity pairs, D-03 creation without a
predecessor, and the forward bound. Labelled SYNTHETIC declarations in disposable folders.

  python -B -X dev tests/test_repair.py -v
"""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_depdecl import Desk, H, addr, decl, mref, req  # noqa: E402


class TestReverseBound(Desk):
    def chain(self):
        c = decl("c", "lab/c.py", zero=True)
        b = decl("b", "lab/b.py", [req("c", "lab/c.py")])
        a = decl("a", "lab/a.py", [req("b", "lab/b.py")], links=[], unknown=["SYNTHETIC: no workflow page"])
        return self.write_set([a, b, c], name="chain")

    def test_16_one_too_shallow_is_truncated_and_exactly_enough_is_complete(self):
        s = self.chain()
        code, r = self.cli("impacted", "--set", s, "--module", "lib-build:lab/c.py", "--depth", "1")
        self.assertEqual((code, r["status"], [c["consumer"] for c in r["consumers"]]), (1, "truncated", ["lib-build:lab/b.py"]))
        self.assertEqual(r["unexpanded"][0]["module"], "lib-build:lab/b.py")
        self.assertEqual(r["unexpanded"][0]["direct_declared_consumers"], 1)
        self.assertEqual(r["findings"][0]["finding"], "depth-limit")
        self.assertIn("rerun with a larger --depth", r["note"])
        code, r = self.cli("impacted", "--set", s, "--module", "lib-build:lab/c.py", "--depth", "2")
        self.assertEqual((code, r["status"], r["unexpanded"], r["finding_counts"]), (0, "candidates-for-review", [], {}))
        a = [c for c in r["consumers"] if c["consumer"] == "lib-build:lab/a.py"][0]
        self.assertEqual((a["depth"], a["provenance"]["unknown"]), (2, ["SYNTHETIC: no workflow page"]))  # provenance kept

    def test_17_shared_and_cycle_in_reverse(self):
        d = decl("d", "lab/d.py", zero=True)
        b, c = decl("b", "lab/b.py", [req("d", "lab/d.py")]), decl("c", "lab/c.py", [req("d", "lab/d.py")])
        a = decl("a", "lab/a.py", [req("b", "lab/b.py"), req("c", "lab/c.py")])
        code, r = self.cli("impacted", "--set", self.write_set([a, b, c, d]), "--module", "lib-build:lab/d.py", "--depth", "2")
        rows = [(x["consumer"].split(":")[1], x["revisit"] or "") for x in r["consumers"]]
        self.assertEqual((code, sorted(rows)), (0, [("lab/a.py", ""), ("lab/a.py", "shared"), ("lab/b.py", ""), ("lab/c.py", "")]))
        x, y = decl("x", "lab/x.py", [req("y", "lab/y.py")]), decl("y", "lab/y.py", [req("x", "lab/x.py")])
        code, r = self.cli("impacted", "--set", self.write_set([x, y], name="cyc"), "--module", "lib-build:lab/x.py", "--depth", "8")
        self.assertEqual((code, [c["revisit"] for c in r["consumers"]], r["finding_counts"]), (1, [None, "cycle"], {"cycle": 1}))

    def test_18_forward_bound_ends_naturally_at_a_dependency_free_leaf(self):
        chain = [decl(f"n{i}", f"lab/n{i}.py", [req(f"n{i+1}", f"lab/n{i+1}.py")]) for i in range(3)] + [decl("n3", "lab/n3.py", zero=True)]
        s = self.write_set(chain)
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/n0.py", "--transitive", "--depth", "3")
        self.assertEqual((code, r["status"]), (0, "complete-for-declared-coverage"))
        self.assertNotIn("depth-limit", self.finds(r))
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/n0.py", "--transitive", "--depth", "2")
        self.assertEqual(code, 1)
        lim = [f for e in r["requirements"] for f in e["findings"] if f["finding"] == "depth-limit"]
        self.assertEqual(lim[0]["unwalked"], "lib-build:lab/n2.py")


class TestIdentityPairs(Desk):
    def test_19_pairs_resolve_mismatch_differ_and_versions(self):
        t1 = decl("t", "lab/t.py", zero=True, impl=H("t1"))
        t2 = decl("t", "lab/t.py", zero=True, version=2, impl=H("t2"), supersedes={"declaration_id": "t", "version": 1})
        good = req("ok", "lab/t.py", pin=H("t2"))
        badlen = copy.deepcopy(good)
        badlen["id"], badlen["pin"]["bytes"] = "badlen", 999
        wrong = req("wrong", "lab/t.py", pin=H("other"))
        unp = req("unp", "lab/t.py")
        u = decl("u", "lab/u.py", [good, badlen, wrong, unp])
        s = self.write_set([t1, t2, u], select=[{"module": mref("lab/t.py"), "declaration_id": "t", "version": 1}])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/u.py", "--transitive")
        by = {e["requirement_id"]: e for e in r["requirements"]}
        self.assertEqual((by["ok"]["resolution"], by["ok"]["resolved_to"]["version"]), ("resolved", 2))
        self.assertEqual((by["badlen"]["resolution"], by["badlen"]["resolved_to"]), ("identity-pair-mismatch", None))
        f = by["badlen"]["findings"][0]
        self.assertEqual((f["pinned"]["bytes"], f["declared"][0]["bytes"]), (999, 1))
        self.assertIn("no module file was measured", f["note"])
        self.assertEqual(by["wrong"]["resolution"], "pin-differs")
        self.assertEqual((by["unp"]["resolution"], by["unp"]["resolved_to"]["version"]), ("selected", 1))  # explicit selection kept
        self.assertEqual(code, 1)

    def test_20_impacted_and_identity_report_pair_contradictions(self):
        t = decl("t", "lab/t.py", zero=True, impl=hashlib.sha256(b"real bytes").hexdigest())  # declares bytes 1; real file is 10
        q = req("t", "lab/t.py", pin=t["implementation"]["sha256"])
        q["pin"]["bytes"] = 7
        u = decl("u", "lab/u.py", [q])
        s = self.write_set([t, u], fixtures=[("lab/t.py", b"real bytes")])
        code, r = self.cli("impacted", "--set", s, "--module", "lib-build:lab/t.py")
        self.assertEqual((code, r["consumers"][0]["pin_vs_declarations"], r["implementation_compared"]), (1, "pair-mismatch", "sha256 only"))
        code, r = self.cli("identity", "--set", s)
        row = r["fixtures"][0]
        self.assertEqual((code, row["result"], row["measured"], row["bytes"], row["length_contradicted_by"][0]["declared_bytes"]),
                         (1, "declaration-length-wrong", True, 10, 1))


class TestCreation(Desk):
    def files(self, new, change):
        n = self.tmp / "new.json"
        n.write_text(json.dumps(new))
        change["new"]["sha256"] = hashlib.sha256(n.read_bytes()).hexdigest()
        c = self.tmp / "change.json"
        c.write_text(json.dumps(change))
        return n, c

    def change(self, d, introduced):
        return {"schema": "module-change/1", "module": mref(d["module"]["path"]), "authorized_by": {"address": addr(), "item": "#03"}, "old": None,
                "new": {"declaration_id": d["declaration_id"], "version": d["version"], "sha256": None},
                "implementation": {"sha256": d["implementation"]["sha256"], "bytes": d["implementation"]["bytes"]},
                "evidence": [{"role": "test", "address": None, "sha256": None, "note": "SYNTHETIC"}],
                "relationships": {"introduced": [{"requirement_id": i, "reason": "SYNTHETIC initial"} for i in introduced], "changed": [], "removed": []}}

    def test_21_creation_accounts_every_initial_requirement(self):
        d = decl("fresh", "lab/fresh.py", [req("x", "lab/x.py"), req("y", "lab/y.py")])
        n, c = self.files(d, self.change(d, ["x", "y"]))
        code, r = self.cli("delta", "--create", "--new", n, "--change", c)
        self.assertEqual((code, r["mode"], r["status"], r["computed"]["introduced"], r["inputs"]["old"]), (0, "create", "consistent", ["x", "y"], None))
        free = decl("leaf", "lab/leaf.py", zero=True)
        n, c = self.files(free, self.change(free, []))
        code, r = self.cli("delta", "--create", "--new", n, "--change", c)
        self.assertEqual((code, r["status"], r["dependency_free"]), (0, "consistent", True))

    def test_22_creation_refuses_or_flags_bad_records(self):
        d = decl("fresh", "lab/fresh.py", [req("x", "lab/x.py"), req("y", "lab/y.py")])
        cases = {"missing initial": (d, lambda ch: ch["relationships"]["introduced"].pop(), "relationships.introduced"),
                 "bogus predecessor": (d, lambda ch: ch.update(old={"declaration_id": "fresh", "version": 0, "sha256": H("x")}), "old"),
                 "changed listed": (d, lambda ch: ch["relationships"]["changed"].append({"requirement_id": "x", "fields": ["pin"], "reason": "r"}),
                                    "relationships.changed"),
                 "wrong implementation": (d, lambda ch: ch["implementation"].update(bytes=5), "implementation")}
        for name, (dd_, edit, what) in cases.items():
            with self.subTest(case=name):
                ch = self.change(dd_, ["x", "y"])
                edit(ch)
                n, c = self.files(dd_, ch)
                code, r = self.cli("delta", "--create", "--new", n, "--change", c)
                self.assertEqual(code, 1, r)
                self.assertIn(what, [f["what"] for f in r["findings"]])
        sup = dict(copy.deepcopy(d), supersedes={"declaration_id": "fresh", "version": 1}, version=2)
        n, c = self.files(sup, self.change(sup, ["x", "y"]))
        code, r = self.cli("delta", "--create", "--new", n, "--change", c)
        self.assertEqual((code, sorted(f["what"] for f in r["findings"])), (1, ["supersedes", "version"]))
        n, c = self.files(d, self.change(d, ["x", "y"]))
        c2 = json.loads(c.read_text())
        c2["new"]["sha256"] = H("not the file")
        c.write_text(json.dumps(c2))
        self.assertIn("new", [f["what"] for f in self.cli("delta", "--create", "--new", n, "--change", c)[1]["findings"]])
        n, c = self.files(d, self.change(d, ["x", "y"]))
        for argv, msg in ((["delta", "--create", "--old", n, "--new", n, "--change", c], "cannot be used with --create"),
                          (["delta", "--new", n, "--change", c], "for a new module use --create"),
                          (["delta", "--old", "", "--new", n, "--change", c], "absolute local path"),
                          (["delta", "--old", n, "--new", n, "--change", c], "a revision needs change.old"),
                          (["delta", "--create", "--new", self.tmp / "absent.json", "--change", c], "regular file")):
            with self.subTest(argv=argv[1:3]):
                code, out = self.cli(*argv)
                self.assertEqual(code, 2, out)
                self.assertIn(msg, out)


if __name__ == "__main__":
    unittest.main()
