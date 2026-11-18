"""Extract selected top-level functions/constants from the frozen sources by AST and exec them
into isolated namespaces. No module import, no module-level side effects run."""
import ast, types, hashlib
ROOM = "/workspace/prima/run0502/source-room/labs"
P1 = ROOM + "/review-report-pass01/report.py"
P2 = ROOM + "/review-report-pass02/report.py"
P3 = ROOM + "/review-report-pass03/report.py"

def pick(path, names, ns):
    src = open(path, "rb").read()
    ns.setdefault("__hashes__", {})[path] = hashlib.sha256(src).hexdigest()
    tree = ast.parse(src)
    body = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            body.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
            body.append(node)
    mod = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias("annotations")], level=0)] + body, type_ignores=[])
    ast.fix_missing_locations(mod)
    exec(compile(mod, path, "exec"), ns)
    return ns

def load():
    p1 = types.SimpleNamespace(**{k: v for k, v in pick(P1, {"same", "word", "publication_class", "ENVELOPE", "apply_envelope"}, {}).items() if not k.startswith("__")})
    ns2 = {"p1": p1}
    pick(P2, {"HEX", "counter", "unknown_counter", "sum_bytes", "row_item", "integrity_of", "sha_key", "unique_files", "artifacts_of", "PAYLOAD_MISSING", "counter_text", "changed_keys"}, ns2)
    p2 = types.SimpleNamespace(**{k: v for k, v in ns2.items() if not k.startswith("__")})
    ns3 = {"p2": p2, "_artifacts_of": p2.artifacts_of}
    pick(P3, {"SCOPE_ADDRESSED", "SCOPE_CONTENT", "SCOPE_PHYSICAL", "PROVENANCE_MEASURED", "PROVENANCE_PHYSICAL",
              "ASSUMPTION_ADDRESSED", "ASSUMPTION_CONTENT", "REASON_ADDRESSED_MEASUREMENT", "REASON_ADDRESSED_ROWS",
              "REASON_ADDRESSED_MISSING", "REASON_ADDRESSED_SIZE", "REASON_CONTENT_MEASUREMENT", "REASON_CONTENT_ROWS",
              "REASON_CONTENT_MISSING", "REASON_CONTENT_SIZE", "REASON_PHYSICAL", "_unknown", "_measured", "_sizes",
              "addressed_sources", "content_blobs", "physical_files", "artifacts_of"}, ns3)
    return p1, p2, types.SimpleNamespace(**{k: v for k, v in ns3.items() if not k.startswith("__")}), ns3["__hashes__"] | ns2["__hashes__"]
