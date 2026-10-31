"""Bounded demonstration of depdecl.py (0517.dependencies 05.01). Every step runs the real CLI in a new process.

  python -B demo.py --snapshots ABS_PACK_SNAPSHOTS_DIR --out ABS_NEW_DIR

Uses: the lab's prototype prime-cycle-chain set (read-only); a disposable copy of that set plus fixture copies of the four
pinned implementation snapshots for identity checks; one labelled SYNTHETIC changed copy of clerk_adapter; and a labelled
SYNTHETIC set for a complete declared chain, an explicit dependency-free module and a missing record. Nothing named by a
declaration is imported or executed. The transcript (argv, exit, stdout sha) is written to OUT/transcript.json.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
TOOL = LAB / "depdecl.py"
CHAIN = LAB / "examples" / "prime-cycle-chain"
SNAPS = {"labs/prime-cycle-pass01/prime_cycle.py": "0008.blob", "labs/batch-observation-pass01/batch_observe.py": "0010.blob",
         "labs/prime-support-pass01/clerk_adapter.py": "0011.blob", "labs/prime-support-pass01/prime_support.py": "0012.blob"}
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    snaps = Path(sys.argv[sys.argv.index("--snapshots") + 1])
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    out.mkdir(parents=False, exist_ok=False)
    steps = []

    def run(label, *args, expect):
        p = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, timeout=120)
        text = p.stdout.decode("utf-8")
        name = f"{len(steps) + 1:02d}.json"
        (out / name).write_bytes(p.stdout)
        steps.append({"step": label, "argv": ["python", "-B", "labs/module-dependencies-pass01/depdecl.py", *map(str, args)], "exit": p.returncode,
                      "expected_exit": expect, "stdout": name, "stdout_sha256": sha(p.stdout), "stderr": p.stderr.decode("utf-8")})
        print(f"{label}: exit {p.returncode} (expected {expect})")
        return json.loads(text) if text.startswith("{") else text

    real = CHAIN / "set.json"
    run("validate the prototype chain set", "validate", "--set", real, expect=0)
    run("prime_cycle transitive requirements (caller: members-book applicable)", "requires", "--set", real,
        "--module", "lib-build:labs/prime-cycle-pass01/prime_cycle.py", "--transitive", "--condition", "members-book=applicable", expect=1)
    run("prime_support with every condition stated inapplicable", "requires", "--set", real, "--module", "lib-build:labs/prime-support-pass01/prime_support.py",
        "--transitive", "--condition", "git-read=inapplicable", "--condition", "clerk-job=inapplicable", expect=1)
    run("explain prime_cycle -> clerk_adapter (shared dependency)", "explain", "--set", real, "--module", "lib-build:labs/prime-cycle-pass01/prime_cycle.py",
        "--to", "lib-build:labs/prime-support-pass01/clerk_adapter.py", expect=1)
    run("record-missing root: prime_review has no declaration", "requires", "--set", real, "--module", "lib-build:labs/prime-review-pass01/prime_review.py", expect=1)

    work = out / "disposable-set"
    shutil.copytree(CHAIN, work)
    fx = work / "fixtures"
    fx.mkdir()
    rows = []
    for path, blob in SNAPS.items():
        data = (snaps / blob).read_bytes()
        (fx / blob).write_bytes(data)
        rows.append({"module": {"repository": "lib-build", "path": path}, "file": f"fixtures/{blob}", "sha256": sha(data)})
    changed = (snaps / SNAPS["labs/prime-support-pass01/clerk_adapter.py"]).read_bytes() + b"\n# SYNTHETIC change for the 0517 demo; not the real module\n"
    (fx / "clerk_adapter.SYNTHETIC-changed.py").write_bytes(changed)
    rows.append({"module": {"repository": "lib-build", "path": "labs/prime-support-pass01/clerk_adapter.py"},
                 "file": "fixtures/clerk_adapter.SYNTHETIC-changed.py", "sha256": sha(changed)})
    s = json.loads((work / "set.json").read_text(encoding="utf-8"))
    s["set_id"] = "prime-cycle-chain-proto-1-with-fixtures"
    s["coverage"] += " Disposable copy with fixture copies of the four pinned snapshots and one SYNTHETIC changed clerk_adapter."
    s["fixtures"] = rows
    (work / "set.json").write_text(json.dumps(s, indent=1) + "\n", encoding="utf-8")
    run("identity: four snapshot copies identical, SYNTHETIC copy changed", "identity", "--set", work / "set.json", expect=1)
    run("reverse impact of the SYNTHETIC changed clerk_adapter", "impacted", "--set", work / "set.json",
        "--module", "lib-build:labs/prime-support-pass01/clerk_adapter.py", "--implementation", sha(changed), expect=1)  # undeclared bytes: a finding
    run("derived index into a new folder", "index", "--set", work / "set.json", "--out", out / "index", expect=0)

    syn = out / "synthetic-set"
    (syn / "d").mkdir(parents=True)
    base = lambda did, path, reqs, zero=False: {
        "schema": "module-declaration/1", "declaration_id": did, "version": 1, "status": "prototype",
        "module": {"repository": "lib-build", "path": path, "name": did, "purpose": "SYNTHETIC demo module", "interface": ["main"],
                   "limits": ["SYNTHETIC"], "home": None},
        "implementation": {"sha256": sha(did.encode()), "bytes": len(did), "basis": {"kind": "git-blob", "repository": "lib-build", "commit": "0" * 40, "path": path}},
        "coverage": {"entry_points": ["main"], "method": "SYNTHETIC demo record", "complete_claim": False},
        "no_requirements": zero, "requirements": reqs, "withheld": [],
        "provenance": {"links": [{"role": "assignment", "address": {"repository": "lib-build", "book": "00.00.10.work", "page": "0599.synthetic",
                                                                     "face_or_pass": "05.01", "file": "05.01.md"},
                                  "sha256": sha(b"synthetic page"), "commit": "0" * 40, "status": "pinned", "note": "SYNTHETIC address"}], "unknown": []},
        "supersedes": None}
    r = lambda rid, path: {"id": rid, "kind": "runtime-code", "target": {"module": {"repository": "lib-build", "path": path}},
                           "pin": {"sha256": sha(rid.encode()), "bytes": len(rid)}, "pin_required": True, "mechanism": "import",
                           "condition": {"applies": "always", "id": None, "statement": None, "status": "applicable"},
                           "availability": "not-applicable", "reason": "SYNTHETIC", "source_ref": None}
    decls = [base("top", "syn/top.py", [r("mid", "syn/mid.py")]), base("mid", "syn/mid.py", [r("leaf", "syn/leaf.py")]),
             base("leaf", "syn/leaf.py", [], zero=True), base("orphan", "syn/orphan.py", [r("ghost", "syn/ghost.py")])]
    srows = []
    for d in decls:
        b = (json.dumps(d, indent=1) + "\n").encode()
        (syn / "d" / f"{d['declaration_id']}.json").write_bytes(b)
        srows.append({"file": f"d/{d['declaration_id']}.json", "sha256": sha(b)})
    (syn / "set.json").write_text(json.dumps({"schema": "module-declaration-set/1", "set_id": "synthetic-demo", "coverage": "SYNTHETIC demo set",
                                              "declarations": srows, "fixtures": [], "select": [],
                                              "bounds": {"max_records": 10, "max_file_bytes": 65536, "max_depth": 8, "max_output_bytes": 262144}}, indent=1))
    run("SYNTHETIC complete declared chain top -> mid -> leaf", "requires", "--set", syn / "set.json", "--module", "lib-build:syn/top.py", "--transitive", expect=0)
    run("SYNTHETIC explicit dependency-free module", "requires", "--set", syn / "set.json", "--module", "lib-build:syn/leaf.py", expect=0)
    run("SYNTHETIC missing record ghost", "requires", "--set", syn / "set.json", "--module", "lib-build:syn/orphan.py", "--transitive", expect=1)
    run("05.02 reverse bound one level too shallow: leaf <- mid <- top at depth 1 (truncated)", "impacted", "--set", syn / "set.json",
        "--module", "lib-build:syn/leaf.py", "--depth", "1", expect=1)
    run("05.02 reverse bound exactly enough: depth 2 ends naturally", "impacted", "--set", syn / "set.json", "--module", "lib-build:syn/leaf.py",
        "--depth", "2", expect=0)
    pair = out / "pair-set"
    (pair / "d").mkdir(parents=True)
    leaf_b = (syn / "d" / "leaf.json").read_bytes()
    (pair / "d" / "leaf.json").write_bytes(leaf_b)
    bad = base("pairpin", "syn/pairpin.py", [dict(r("leaf", "syn/leaf.py"), pin={"sha256": sha(b"leaf"), "bytes": 999})])
    bad_b = (json.dumps(bad, indent=1) + "\n").encode()
    (pair / "d" / "pairpin.json").write_bytes(bad_b)
    (pair / "set.json").write_text(json.dumps({"schema": "module-declaration-set/1", "set_id": "synthetic-pair", "coverage": "SYNTHETIC pair-mismatch set",
                                               "declarations": [{"file": "d/leaf.json", "sha256": sha(leaf_b)}, {"file": "d/pairpin.json", "sha256": sha(bad_b)}],
                                               "fixtures": [], "select": [],
                                               "bounds": {"max_records": 10, "max_file_bytes": 65536, "max_depth": 8, "max_output_bytes": 262144}}, indent=1))
    run("05.02 identity pair: right digest, length 999 against declared 4", "requires", "--set", pair / "set.json", "--module", "lib-build:syn/pairpin.py",
        expect=1)
    create = out / "create"
    create.mkdir()
    fresh = base("fresh", "syn/fresh.py", [r("leaf", "syn/leaf.py")])
    fresh_b = (json.dumps(fresh, indent=1) + "\n").encode()
    (create / "new.json").write_bytes(fresh_b)
    (create / "change.json").write_text(json.dumps({
        "schema": "module-change/1", "module": {"repository": "lib-build", "path": "syn/fresh.py"},
        "authorized_by": {"address": {"repository": "lib-build", "book": "00.00.10.work", "page": "0599.synthetic", "face_or_pass": "05.02",
                                      "file": "05.02.md"}, "item": "#03"},
        "old": None, "new": {"declaration_id": "fresh", "version": 1, "sha256": sha(fresh_b)},
        "implementation": {"sha256": fresh["implementation"]["sha256"], "bytes": fresh["implementation"]["bytes"]},
        "evidence": [{"role": "test", "address": None, "sha256": None, "note": "SYNTHETIC"}],
        "relationships": {"introduced": [{"requirement_id": "leaf", "reason": "SYNTHETIC initial requirement"}], "changed": [], "removed": []}}, indent=1))
    run("05.02 new-module creation: no predecessor, every initial requirement introduced", "delta", "--create", "--new", create / "new.json",
        "--change", create / "change.json", expect=0)
    run("05.02 creation refuses a supplied --old", "delta", "--create", "--old", create / "new.json", "--new", create / "new.json",
        "--change", create / "change.json", expect=2)
    seam = out / "completion-seam"  # worked example of CONTRACT §8; every new identity below is SYNTHETIC
    seam.mkdir()
    old_b = (CHAIN / "declarations" / "batch-observe.v1.json").read_bytes()
    new = json.loads(old_b)
    new.update(version=2, supersedes={"declaration_id": "batch-observe", "version": 1})
    new["implementation"]["sha256"] = sha(b"SYNTHETIC batch_observe v2 bytes")
    for q in new["requirements"]:
        if q["id"] == "clerk-adapter":
            q["pin"] = {"sha256": sha(changed), "bytes": len(changed)}
            q["reason"] += " (SYNTHETIC v2: re-pinned to the changed adapter)"
    new_b = (json.dumps(new, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    (seam / "old.json").write_bytes(old_b)
    (seam / "new.json").write_bytes(new_b)
    change = {"schema": "module-change/1", "module": {"repository": "lib-build", "path": "labs/batch-observation-pass01/batch_observe.py"},
              "authorized_by": {"address": {"repository": "lib-build", "book": "00.00.10.work", "page": "0599.synthetic", "face_or_pass": "05.01",
                                            "file": "05.01.md"}, "item": "#02"},
              "old": {"declaration_id": "batch-observe", "version": 1, "sha256": sha(old_b)},
              "new": {"declaration_id": "batch-observe", "version": 2, "sha256": sha(new_b)},
              "implementation": {"sha256": new["implementation"]["sha256"], "bytes": new["implementation"]["bytes"]},
              "evidence": [{"role": "test", "address": None, "sha256": None, "note": "SYNTHETIC: the builder's test run would be bound here"}],
              "relationships": {"introduced": [], "removed": [],
                                "changed": [{"requirement_id": "clerk-adapter", "fields": ["pin", "reason"], "reason": "SYNTHETIC: adapter bytes changed"}]}}
    (seam / "change.json").write_text(json.dumps(change, indent=1) + "\n", encoding="utf-8")
    run("completion seam: consistent change record (SYNTHETIC v2)", "delta", "--old", seam / "old.json", "--new", seam / "new.json",
        "--change", seam / "change.json", expect=0)
    change["relationships"]["changed"] = []
    (seam / "change-omits.json").write_text(json.dumps(change, indent=1) + "\n", encoding="utf-8")
    run("completion seam: change record omits the changed pin", "delta", "--old", seam / "old.json", "--new", seam / "new.json",
        "--change", seam / "change-omits.json", expect=1)
    (out / "transcript.json").write_text(json.dumps({"schema": "module-dependencies-demo/1", "steps": steps,
                                                     "all_exits_as_expected": all(s["exit"] == s["expected_exit"] for s in steps)}, indent=1) + "\n",
                                         encoding="utf-8")
    print("all exits as expected:", all(s["exit"] == s["expected_exit"] for s in steps))
    return 0 if all(s["exit"] == s["expected_exit"] for s in steps) else 1


if __name__ == "__main__":
    sys.exit(main())
