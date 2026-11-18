"""Isolated pure-function probe (Worker A, prima-0706-0502). Reads the frozen sources READ-ONLY, compiles only
selected top-level AST nodes (constants and pure functions) into private namespaces. Nothing in the source
modules' top-level side effects (load_pass02/load_pass03, D:\\ paths, installs) is executed."""
import ast, json, re, sys, types, hashlib
SR = "/workspace/prima/run0502/source-room/"
P2 = SR + "labs/workbook-review-pass02/workbook.py"
P3 = SR + "labs/workbook-review-pass03/workbook.py"
N7 = SR + "labs/n7-intake-compat-pass02/n7compat2.py"
PR = SR + "00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.17/proposal/workbook-review-pass04.workbook.py.proposal"

def pick(path, names, ns):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef,)) and node.name in names: keep.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets): keep.append(node)
    got = {n.name if isinstance(n, ast.FunctionDef) else n.targets[0].id for n in keep}
    missing = set(names) - got
    assert not missing, (path, missing)
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    return sorted(got)

ran = {}
p2 = {"__builtins__": __builtins__}
ran["pass02"] = pick(P2, {"SHA_RE", "LABELS", "suffix_ok"}, p2)
p3 = {"__builtins__": __builtins__, "re": re}
ran["pass03"] = pick(P3, {"FIELD_RE", "COUNT_RE", "COUNT_TAILS", "LABEL_CODE", "accept_field", "parse_pointer"}, p3)
p3["p2"] = types.SimpleNamespace(suffix_ok=p2["suffix_ok"])
P3NS = types.SimpleNamespace(**{k: v for k, v in p3.items() if k != "__builtins__"})
P3NS.p2 = p3["p2"]
n7 = {"__builtins__": __builtins__, "re": re, "contextvars": __import__("contextvars")}
ran["n7compat2"] = pick(N7, {"PATH", "RETURNED_RE", "N7_MANIFEST_RE", "SHA_ANY", "LABEL_WORDS", "KIND", "make_parser"}, n7)
pr = {"__builtins__": __builtins__, "re": re, "contextvars": __import__("contextvars"), "p3": P3NS}
ran["proposal"] = pick(PR, {"PATH", "RETURNED_RE", "N7_MANIFEST_RE", "SHA_ANY", "LABEL_WORDS", "parse_n7"}, pr)

parse_n7_lab = n7["make_parser"](P3NS, kind_fn=lambda: "N7NN")
parse_n5_lab = n7["make_parser"](P3NS, kind_fn=lambda: "N5NN")
pass03 = p3["parse_pointer"]
parse_n7_prop = pr["parse_n7"]

H1 = "a" * 64; H2 = "b" * 64; HU = "A" * 64
cases = {
 "C1_rejected_returned_plus_submission": f"Returned: r.md (by {H2}), sha256 {H1}, 10 bytes.\nSubmission: s.md sha256 {H2}, 20 bytes.",
 "C2_uppercase_hex_attribution": f"Returned: r.md (copy of {HU}), sha256 {H1}, 10 bytes.",
 "C3_lowercase_label_attribution": f"Returned: r.md (see submission: other.md), sha256 {H1}, 10 bytes.",
 "C4_collision_with_suffix": f"Submission: s.md sha256 {H1}, 1 bytes.\nArtifact manifest: m.json, sha256 {H2}, 5 bytes. note",
 "C5_collision_plain": f"Submission: s.md sha256 {H1}, 1 bytes.\nArtifact manifest: m.json, sha256 {H2}, 5 bytes.",
 "C6_returned_plus_submission_same_target": f"Returned: s.md (author copy), sha256 {H1}, 1 bytes.\nSubmission: s.md sha256 {H1}, 1 bytes.",
 "C7_whitespace_attribution": f"Returned: r.md ( ), sha256 {H1}, 10 bytes.",
 "C8_dotdot_path_returned": f"Returned: a/../b.md (x), sha256 {H1}, 10 bytes.",
 "C9_returned_with_suffix": f"Returned: r.md (x), sha256 {H1}, 10 bytes. note",
 "C10_rejected_manifest_dup_then_valid": f"Submission: s.md sha256 {H1}, 1 bytes.\nArtifact manifest: m.json, sha256 {H2}, 5 bytes. Verification: v sha256\nArtifact manifest: n.json, sha256 {H2}, 5 bytes.",
}
def norm(p):
    def f(x): return None if x is None else {k: x[k] for k in sorted(x)}
    return {"state": p["state"], "submission": f(p["submission"]), "manifest": f(p["manifest"]), "verification": f(p["verification"]),
            "codes": [x["code"] for x in p["findings"]]}
out = {"functions_ran": ran, "cases": {}}
for name, body in cases.items():
    r = {"n7_lab": norm(parse_n7_lab(body)), "n7_proposal": norm(parse_n7_prop(body)), "n5_lab": norm(parse_n5_lab(body)), "pass03": norm(pass03(body))}
    r["lab_eq_proposal"] = r["n7_lab"] == r["n7_proposal"]
    r["n5_eq_pass03"] = r["n5_lab"] == r["pass03"]
    out["cases"][name] = r
json.dump(out, sys.stdout, indent=1, sort_keys=True)
