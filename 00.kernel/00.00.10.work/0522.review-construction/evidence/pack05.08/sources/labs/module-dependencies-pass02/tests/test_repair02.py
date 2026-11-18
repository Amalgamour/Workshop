"""Successor tests for 0525.app-dependencies 05.02. SYNTHETIC records, plus a stdout comparison
of the predecessor and this reader on the unchanged /1 fixtures.

  python -B -X dev labs/module-dependencies-pass02/tests/test_repair02.py -v
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
ROOT = LAB.parents[1]
NEW = LAB / "depdecl.py"
OLD = ROOT / "labs" / "module-dependencies-pass01" / "depdecl.py"
CUT = "a" * 40
HEAD = "b" * 40
H = lambda s: hashlib.sha256(s.encode()).hexdigest()


def addr():
    return {"repository": "lib-build", "book": "00.00.10.work", "page": "0599.synthetic", "face_or_pass": "05.02", "file": "05.02.md"}


def mref(path):
    return {"repository": "lib-build", "path": path}


def basis_obs(path, form="working-tree", head=HEAD):
    return {"kind": "observed-file", "repository": "lib-build", "path": path, "form": form, "context_head": head}


def basis_git(path):
    return {"kind": "git-blob", "repository": "lib-build", "commit": CUT, "path": path, "verification": "supplied-unverified"}


def req(rid, path, pin="absent", mech="import"):
    if pin == "absent":
        body, required = None, False
    elif pin == "digest":
        body, required = {"sha256": H(path), "bytes": None}, True
    else:
        body, required = {"sha256": pin[0], "bytes": pin[1]}, True
    return {"id": rid, "kind": "runtime-code", "target": {"module": mref(path)}, "pin": body, "pin_required": required,
            "mechanism": mech, "condition": {"applies": "always", "id": None, "statement": None, "status": "applicable"},
            "availability": "not-applicable", "reason": "SYNTHETIC reason", "source_ref": None}


def decl(did, path, reqs=(), version=1, schema="module-declaration/2", basis=None, impl=None, nbytes=1, zero=False, supersedes=None):
    return {"schema": schema, "declaration_id": did, "version": version, "status": "prototype",
            "module": {"repository": "lib-build", "path": path, "name": did, "purpose": "SYNTHETIC fixture module",
                       "interface": ["x"], "limits": ["SYNTHETIC"], "home": None},
            "implementation": {"sha256": impl or H(did + str(version)), "bytes": nbytes, "basis": basis or basis_obs(path)},
            "coverage": {"entry_points": ["main"], "method": "SYNTHETIC fixture", "complete_claim": False},
            "no_requirements": zero or not reqs, "requirements": list(reqs), "withheld": [],
            "provenance": {"links": [{"role": "assignment", "address": addr(), "sha256": H("page"), "commit": None,
                                      "status": "pinned", "note": ""}], "unknown": []},
            "supersedes": supersedes}


class Desk(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dd2-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_set(self, decls, name="set", schema="module-declaration-set/2", fixtures=(), select=()):
        root = self.tmp / name
        (root / "d").mkdir(parents=True)
        rows = []
        for i, d in enumerate(decls):
            raw = (json.dumps(d, indent=1) + "\n").encode()
            (root / "d" / f"{i:02d}.json").write_bytes(raw)
            rows.append({"file": f"d/{i:02d}.json", "sha256": hashlib.sha256(raw).hexdigest()})
        fx = []
        for i, (path, data) in enumerate(fixtures):
            (root / "f").mkdir(exist_ok=True)
            (root / "f" / f"{i}.bin").write_bytes(data)
            fx.append({"module": mref(path), "file": f"f/{i}.bin", "sha256": hashlib.sha256(data).hexdigest()})
        body = {"schema": schema, "set_id": "synthetic", "coverage": "SYNTHETIC fixtures", "declarations": rows,
                "fixtures": fx, "select": list(select),
                "bounds": {"max_records": 50, "max_file_bytes": 65536, "max_depth": 16, "max_output_bytes": 1048576}}
        path = root / "set.json"
        path.write_text(json.dumps(body, indent=1), encoding="utf-8", newline="\n")
        return path

    def run_tool(self, tool, args):
        p = subprocess.run([sys.executable, "-B", str(tool), *map(str, args)], capture_output=True, timeout=120)
        out = p.stdout.decode("utf-8")
        return p.returncode, (json.loads(out) if out.startswith("{") else out), p.stderr.decode("utf-8")

    def cli(self, *args):
        code, out, err = self.run_tool(NEW, args)
        self.assertEqual(err, "")
        return code, out


class TestPositive(Desk):
    def test_observed_file_validates(self):
        code, r = self.cli("validate", "--set", self.write_set([decl("leaf", "lab/leaf.py", zero=True)]))
        self.assertEqual((code, r["status"]), (0, "valid"))
        self.assertEqual(r["records"][0]["basis"]["kind"], "observed-file")

    def test_digest_only_resolves_without_a_length(self):
        target = decl("helper", "lab/helper.py", zero=True, impl=H("helper"), nbytes=99)
        pin = req("helper", "lab/helper.py")
        pin["pin"] = {"sha256": H("helper"), "bytes": None}
        pin["pin_required"] = True
        caller = decl("caller", "lab/caller.py", [pin])
        code, r = self.cli("requires", "--set", self.write_set([caller, target]), "--module", "lib-build:lab/caller.py", "--transitive")
        edge = r["requirements"][0]
        self.assertEqual((code, edge["resolution"], edge["pin_form"], edge["resolved_to"]["declaration_id"]),
                         (0, "resolved", "digest-only", "helper"))
        self.assertNotIn("identity-pair-mismatch", [f["finding"] for f in edge["findings"]])
        code, hit = self.cli("impacted", "--set", self.write_set([caller, target], name="rev"), "--module", "lib-build:lab/helper.py",
                             "--implementation", H("helper"))
        row = hit["consumers"][0]
        self.assertEqual((code, row["pin_form"], row["pin_vs_declarations"], row["against_implementation"]),
                         (0, "digest-only", "digest-matches", "pin-matches"))


class TestMalformed(Desk):
    def test_unsupported_kind_and_false_verification_are_refused(self):
        bad_kind = decl("a", "lab/a.py", zero=True, basis={"kind": "blob", "repository": "lib-build", "commit": CUT,
                                                           "path": "lab/a.py", "verification": "supplied-unverified"})
        code, out = self.cli("validate", "--set", self.write_set([bad_kind]))
        self.assertEqual(code, 2)
        self.assertIn("not a supported source basis", out)
        verified = decl("b", "lab/b.py", zero=True, basis=dict(basis_git("lab/b.py"), verification="verified"))
        code, out = self.cli("validate", "--set", self.write_set([verified], name="ver"))
        self.assertEqual(code, 2)
        self.assertIn("supplied-unverified", out)
        coerced = decl("c", "lab/c.py", zero=True, basis=dict(basis_obs("lab/c.py"), commit=CUT))
        code, out = self.cli("validate", "--set", self.write_set([coerced], name="coerced"))
        self.assertEqual(code, 2)
        self.assertIn("must have exactly", out)

    def test_v1_rejects_the_new_shapes(self):
        v1 = decl("a", "lab/a.py", zero=True, schema="module-declaration/1",
                  basis={"kind": "observed-file", "repository": "lib-build", "commit": CUT, "path": "lab/a.py"})
        code, out = self.cli("validate", "--set", self.write_set([v1], schema="module-declaration-set/1"))
        self.assertEqual(code, 2)
        self.assertIn("must be git-blob", out)
        pair = decl("b", "lab/b.py", [req("x", "lab/x.py")], schema="module-declaration/1",
                    basis={"kind": "git-blob", "repository": "lib-build", "commit": CUT, "path": "lab/b.py"})
        pair["requirements"][0]["pin"] = {"sha256": H("x"), "bytes": None}
        code, out = self.cli("validate", "--set", self.write_set([pair], schema="module-declaration-set/1", name="nullpin"))
        self.assertEqual(code, 2)
        self.assertIn("non-negative integer", out)
        newer = decl("n", "lab/n.py", zero=True)
        code, out = self.cli("validate", "--set", self.write_set([newer], schema="module-declaration-set/1", name="mix"))
        self.assertEqual(code, 2)
        self.assertIn("refused by a module-declaration-set/1", out)


class TestRelationships(Desk):
    def test_mismatch_unpinned_truncation_missing_and_shared(self):
        helper = decl("helper", "lab/helper.py", zero=True, impl=H("helper"), nbytes=99)
        digest_bad = req("bad", "lab/helper.py")
        digest_bad["pin"] = {"sha256": H("other"), "bytes": None}
        digest_bad["pin_required"] = True
        pair_bad = req("pair", "lab/helper.py", pin=(H("helper"), 7))
        unpinned = req("open", "lab/helper.py")
        caller = decl("caller", "lab/caller.py", [digest_bad, pair_bad, unpinned])
        s = self.write_set([caller, helper])
        code, r = self.cli("requires", "--set", s, "--module", "lib-build:lab/caller.py", "--transitive")
        by = {e["requirement_id"]: e for e in r["requirements"]}
        self.assertEqual(code, 1)
        self.assertEqual(by["bad"]["resolution"], "pin-differs")
        self.assertEqual(by["bad"]["pin_form"], "digest-only")
        self.assertEqual(by["pair"]["resolution"], "identity-pair-mismatch")
        self.assertEqual(by["open"]["resolution"], "single-unpinned")
        self.assertEqual(by["open"]["pin_form"], "unpinned")
        code, hit = self.cli("impacted", "--set", s, "--module", "lib-build:lab/helper.py", "--implementation", H("helper"))
        forms = {c["requirement_id"]: (c["pin_vs_declarations"], c["against_implementation"]) for c in hit["consumers"]}
        self.assertEqual(forms["bad"], ("digest-differs", "pin-differs"))
        self.assertEqual(forms["pair"], ("pair-mismatch", "pin-matches"))
        self.assertEqual(forms["open"], ("unpinned", "unpinned"))
        self.assertEqual(code, 1)
        self.assertEqual(hit["finding_counts"]["digest-differs"], 1)
        self.assertEqual(hit["finding_counts"]["pair-mismatch"], 1)
        leaf = decl("leaf", "lab/leaf.py", zero=True)
        mid = decl("mid", "lab/mid.py", [req("leaf", "lab/leaf.py")])
        top = decl("top", "lab/top.py", [req("mid", "lab/mid.py")])
        chain = self.write_set([top, mid, leaf], name="chain")
        code, r = self.cli("requires", "--set", chain, "--module", "lib-build:lab/top.py", "--transitive", "--depth", "1")
        self.assertEqual(code, 1)
        self.assertIn("depth-limit", [f["finding"] for e in r["requirements"] for f in e["findings"]])
        missing = self.write_set([decl("only", "lab/only.py", [req("gone", "lab/gone.py")])], name="miss")
        code, r = self.cli("requires", "--set", missing, "--module", "lib-build:lab/only.py", "--transitive")
        self.assertEqual((code, r["requirements"][0]["resolution"]), (1, "record-missing"))
        left = decl("left", "lab/left.py", [req("leaf", "lab/leaf.py")])
        left["requirements"][0]["pin"] = {"sha256": H("leaf1"), "bytes": None}
        left["requirements"][0]["pin_required"] = True
        right = decl("right", "lab/right.py", [req("leaf", "lab/leaf.py")])
        shared_leaf = decl("leaf", "lab/leaf.py", zero=True, impl=H("leaf1"))
        parent = decl("parent", "lab/parent.py", [req("left", "lab/left.py"), req("right", "lab/right.py")])
        shared = self.write_set([parent, left, right, shared_leaf], name="shared")
        code, r = self.cli("requires", "--set", shared, "--module", "lib-build:lab/parent.py", "--transitive")
        shared_edges = [e for e in r["requirements"] if any(f["finding"] == "shared" for f in e["findings"])]
        self.assertEqual(code, 0)
        self.assertEqual(len(shared_edges), 1)

    def test_identity_keeps_digest_only_distinct_from_length(self):
        raw = b"helper-bytes"
        digest = hashlib.sha256(raw).hexdigest()
        helper = decl("helper", "lab/helper.py", zero=True, impl=digest, nbytes=len(raw))
        caller = decl("caller", "lab/caller.py", [req("helper", "lab/helper.py")])
        caller["requirements"][0]["pin"] = {"sha256": digest, "bytes": None}
        caller["requirements"][0]["pin_required"] = True
        s = self.write_set([caller, helper], fixtures=[("lab/helper.py", raw)])
        code, r = self.cli("identity", "--set", s)
        row = r["fixtures"][0]
        self.assertEqual((code, row["result"], row["bytes"]), (0, "identical", len(raw)))
        self.assertEqual(row["incoming_pins"][0]["relation"], "digest-matches")
        self.assertNotIn("pair-matches", [x["relation"] for x in row["incoming_pins"]])


class TestDelta(Desk):
    def change(self, new, introduced, old=None):
        return {"schema": "module-change/1", "module": mref(new["module"]["path"]),
                "authorized_by": {"address": addr(), "item": "#02"}, "old": old,
                "new": {"declaration_id": new["declaration_id"], "version": new["version"], "sha256": None},
                "implementation": {"sha256": new["implementation"]["sha256"], "bytes": new["implementation"]["bytes"]},
                "evidence": [{"role": "test", "address": None, "sha256": None, "note": "SYNTHETIC"}],
                "relationships": {"introduced": [{"requirement_id": i, "reason": "SYNTHETIC initial"} for i in introduced],
                                  "changed": [], "removed": []}}

    def dump(self, name, obj):
        path = self.tmp / name
        path.write_text(json.dumps(obj), encoding="utf-8", newline="\n")
        return path

    def test_create_and_revision(self):
        fresh = decl("fresh", "lab/fresh.py", [req("x", "lab/x.py")])
        fresh["requirements"][0]["pin"] = {"sha256": H("x"), "bytes": None}
        fresh["requirements"][0]["pin_required"] = True
        ch = self.change(fresh, ["x"])
        newp = self.dump("new.json", fresh)
        ch["new"]["sha256"] = hashlib.sha256(newp.read_bytes()).hexdigest()
        code, r = self.cli("delta", "--create", "--new", newp, "--change", self.dump("change.json", ch))
        self.assertEqual((code, r["mode"], r["status"], r["computed"]["introduced"]), (0, "create", "consistent", ["x"]))
        old = decl("mod", "lab/mod.py", [req("helper", "lab/helper.py")], schema="module-declaration/1",
                   basis={"kind": "git-blob", "repository": "lib-build", "commit": CUT, "path": "lab/mod.py"})
        new = decl("mod", "lab/mod.py", [req("helper", "lab/helper.py")], version=2,
                   supersedes={"declaration_id": "mod", "version": 1}, basis=basis_obs("lab/mod.py"))
        new["requirements"][0]["pin"] = {"sha256": H("helper"), "bytes": None}
        new["requirements"][0]["pin_required"] = True
        oldp, newp = self.dump("old.json", old), self.dump("new2.json", new)
        ch = self.change(new, [], old={"declaration_id": "mod", "version": 1, "sha256": hashlib.sha256(oldp.read_bytes()).hexdigest()})
        ch["new"]["sha256"] = hashlib.sha256(newp.read_bytes()).hexdigest()
        ch["relationships"]["changed"] = [{"requirement_id": "helper", "fields": ["pin", "pin_required"], "reason": "digest-only pin"}]
        code, r = self.cli("delta", "--old", oldp, "--new", newp, "--change", self.dump("rev.json", ch))
        self.assertEqual((code, r["mode"], r["status"], r["computed"]["changed"]), (0, "revise", "consistent", ["helper"]))


class TestV1Fixtures(Desk):
    def test_predecessor_stdout_matches_on_unchanged_sets(self):
        app = ROOT / "labs" / "app-dependencies-pass01" / "set.json"
        chain = ROOT / "labs" / "module-dependencies-pass01" / "examples" / "prime-cycle-chain" / "set.json"
        cases = [
            ("validate", "--set", app),
            ("requires", "--set", app, "--module", "lib-build:app/librarian.py", "--transitive"),
            ("identity", "--set", app),
            ("explain", "--set", app, "--module", "lib-build:app/librarian.py", "--to", "lib-build:labs/return-capture-pass01/return_capture.py"),
            ("impacted", "--set", app, "--module", "lib-build:labs/return-capture-pass01/return_capture.py", "--depth", "1"),
            ("impacted", "--set", app, "--module", "lib-build:labs/return-capture-pass01/return_capture.py", "--depth", "8"),
            ("validate", "--set", chain),
            ("requires", "--set", chain, "--module", "lib-build:labs/prime-cycle-pass01/prime_cycle.py", "--transitive"),
            ("identity", "--set", chain),
            ("impacted", "--set", chain, "--module", "lib-build:labs/batch-observation-pass01/batch_observe.py", "--depth", "2"),
        ]
        for args in cases:
            with self.subTest(command=args[0], target=Path(args[2]).parent.name):
                old = self.run_tool(OLD, args)
                new = self.run_tool(NEW, args)
                self.assertEqual(old[0], new[0])
                self.assertEqual(old[1] if isinstance(old[1], str) else json.dumps(old[1], sort_keys=True),
                                 new[1] if isinstance(new[1], str) else json.dumps(new[1], sort_keys=True))
                self.assertEqual(old[2], "")
                self.assertEqual(new[2], "")


if __name__ == "__main__":
    unittest.main()
