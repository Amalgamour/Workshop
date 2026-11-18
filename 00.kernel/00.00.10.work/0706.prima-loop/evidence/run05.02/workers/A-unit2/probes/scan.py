"""Static AST scan (Worker A unit 2). Parses source-room .py files (and the .proposal) with ast only; executes nothing from them."""
import ast, json, re, sys, hashlib, os
SR = "/workspace/prima/run0502/source-room"
HEX = re.compile(r"^[0-9a-f]{64}$")
PATHLIKE = re.compile(r"(^|/)(app|labs|00\.kernel)/|\.(py|json|md)$|^[A-Za-z]:\\\\|^[A-Za-z]:\\|D:")
files = []
for d, _, fs in os.walk(SR):
    for f in fs:
        if f.endswith(".py") or f.endswith(".proposal"):
            files.append(os.path.relpath(os.path.join(d, f), SR))
files.sort()
out = {}
for rel in files:
    src = open(os.path.join(SR, rel), encoding="utf-8").read()
    tree = ast.parse(src)
    rec = {"imports": [], "strings": [], "hex_pins": [], "loaders": [], "subprocess": [], "fixed_roots": []}
    parents = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node): parents[ch] = node
    def owner(n):
        while n in parents:
            n = parents[n]
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)): return n.name
        return "<module>"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            rec["imports"] += [{"name": a.name, "line": node.lineno} for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            rec["imports"].append({"name": (node.module or "") , "level": node.level, "line": node.lineno})
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if HEX.match(v):
                rec["hex_pins"].append({"value": v, "line": node.lineno, "in": owner(node)})
            elif PATHLIKE.search(v) and len(v) < 200 and "\n" not in v:
                rec["strings"].append({"value": v, "line": node.lineno, "in": owner(node)})
            if v.startswith("D:") or v.startswith("C:"):
                rec["fixed_roots"].append({"value": v, "line": node.lineno, "in": owner(node)})
        elif isinstance(node, ast.Call):
            fn = ast.unparse(node.func)
            if fn.endswith("spec_from_file_location") or fn.endswith("exec_module") or fn in ("load_module", "runpy.run_path") or fn.endswith("import_module"):
                rec["loaders"].append({"call": fn, "args": [ast.unparse(a)[:160] for a in node.args], "line": node.lineno, "in": owner(node)})
            if fn.startswith("subprocess.") or fn in ("os.system", "os.popen"):
                rec["subprocess"].append({"call": fn, "args": [ast.unparse(a)[:200] for a in node.args], "line": node.lineno, "in": owner(node)})
    out[rel] = rec
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(files), "files scanned")
