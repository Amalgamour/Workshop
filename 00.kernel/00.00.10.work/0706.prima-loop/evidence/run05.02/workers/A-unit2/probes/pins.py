"""Static pin extractor (Worker A unit 2). ast only; nothing from the source room is executed."""
import ast, json, re, sys, os, hashlib
SR = "/workspace/prima/run0502/source-room"
HEX = re.compile(r"^[0-9a-f]{64}$")
def meas(rel):
    p = os.path.join(SR, rel)
    if not os.path.isfile(p): return {"present": False}
    b = open(p, "rb").read(); return {"present": True, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
pins = []
def lit(n, consts):
    if isinstance(n, ast.Constant): return n.value
    if isinstance(n, ast.Name) and n.id in consts: return consts[n.id]
    return None
for d, _, fs in os.walk(SR):
    for f in fs:
        if not f.endswith(".py"): continue
        rel = os.path.relpath(os.path.join(d, f), SR)
        tree = ast.parse(open(os.path.join(SR, rel), encoding="utf-8").read())
        consts = {}
        for n in tree.body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Constant):
                consts[n.targets[0].id] = n.value.value
        # module-level PREFIX_{REL,PATH,NAME} + PREFIX_SHA + PREFIX_BYTES
        for k, v in consts.items():
            if k.endswith("_SHA") and isinstance(v, str) and HEX.match(v):
                pre = k[:-4]; size = consts.get(pre + "_BYTES")
                path = next((consts[pre + s] for s in ("_REL", "_PATH", "_NAME") if isinstance(consts.get(pre + s), str)), None)
                line = next(n.lineno for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == k)
                pins.append({"declarer": rel, "line": line, "form": "constants", "key": pre, "path": path, "sha256": v, "bytes": size})
        for n in ast.walk(tree):
            if isinstance(n, ast.Dict):
                keys = [lit(k, {}) for k in n.keys]
                if {"path", "sha256", "bytes"} <= set(k for k in keys if isinstance(k, str)):
                    vals = {k: lit(v, consts) for k, v in zip(keys, n.values)}
                    if isinstance(vals.get("sha256"), str) and HEX.match(vals["sha256"]):
                        pins.append({"declarer": rel, "line": n.lineno, "form": "dict", "path": vals["path"], "sha256": vals["sha256"], "bytes": vals["bytes"]})
            if isinstance(n, ast.Tuple) and len(n.elts) == 3:
                a, b, c = (lit(e, consts) for e in n.elts)
                if isinstance(a, str) and isinstance(b, str) and HEX.match(b):
                    pins.append({"declarer": rel, "line": n.lineno, "form": "tuple", "path": a, "sha256": b, "bytes": c})
            if isinstance(n, ast.Call) and ast.unparse(n.func).endswith("pin_named") and len(n.args) >= 4:
                a, b, c = (lit(e, consts) for e in n.args[1:4])
                pins.append({"declarer": rel, "line": n.lineno, "form": "pin_named", "path": a, "sha256": b, "bytes": c})
for j in ("app/review-loop-v7.json","app/review-loop-v6.json","app/review-loop-v5.json","app/review-loop-v4.json","app/review-report-v1.json"):
    doc = json.load(open(os.path.join(SR, j)))
    tools = doc.get("tools") or {}
    items = tools.items() if isinstance(tools, dict) else []
    for k, v in items:
        if isinstance(v, dict) and "sha256" in v:
            pins.append({"declarer": j, "line": None, "form": "json", "key": k, "path": v.get("path"), "sha256": v.get("sha256"), "bytes": v.get("bytes")})
seen=set(); uniq=[]
for p in pins:
    t=(p["declarer"],p["line"],p["path"],p["sha256"])
    if t in seen: continue
    seen.add(t); uniq.append(p)
for p in uniq:
    m = meas(p["path"]) if isinstance(p["path"], str) and "/" in p["path"] else {"present": None}
    p["room"] = m
    p["match"] = None if not m.get("present") else (m["sha256"] == p["sha256"] and m["bytes"] == p["bytes"])
json.dump(uniq, open(sys.argv[1], "w"), indent=1)
print(len(uniq))
