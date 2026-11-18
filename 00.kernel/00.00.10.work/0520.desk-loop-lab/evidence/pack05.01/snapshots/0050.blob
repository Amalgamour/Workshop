"""Module dependency declarations prototype (0517.dependencies 05.01). Standard library only.

  python -B depdecl.py validate --set ABS
  python -B depdecl.py requires --set ABS --module REPO:PATH [--transitive] [--depth N] [--condition ID=STATE ...]
  python -B depdecl.py explain  --set ABS --module REPO:PATH --to REPO:PATH [--condition ID=STATE ...]
  python -B depdecl.py impacted --set ABS --module REPO:PATH [--implementation SHA] [--depth N]
  python -B depdecl.py identity --set ABS
  python -B depdecl.py index    --set ABS --out ABS
  python -B depdecl.py delta    --old ABS --new ABS --change ABS        (revision)
  python -B depdecl.py delta    --create --new ABS --change ABS         (new module; no predecessor)

Contract: 00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/CONTRACT.md. Reads a caller-supplied, hash-pinned set
of module-local declarations and answers dependency questions from them. It never imports, executes or follows anything a
declaration names, never scans beyond the set, and writes only a new index folder. Findings are answers, not failures:
missing records, pin differences, ambiguity, cycles and unknown conditions are reported, never turned into empty success.
A declaration is a model-authored prototype record, not proof of runtime closure; a digest proves bytes, not compatibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
BOOK = re.compile(r"^\d{2}\.\d{2}\.\d{2}\.[a-z0-9][a-z0-9-]*$")
PAGE = re.compile(r"^\d{4}\.[a-z0-9][a-z0-9.-]*$")
FACE = re.compile(r"^\d{2}(\.\d{2,3})?$")
ITEM = re.compile(r"^#\d{2}$")
KINDS = ("runtime-code", "runtime-resource", "environment", "evidence", "task-context")
MECHANISMS = ("subprocess", "import", "dynamic-import", "hash-check", "path-reference", "read", "document")
STATUSES = ("prototype", "experimental", "partial")
CONDITION_STATES = ("applicable", "inapplicable", "unknown")
LINK_ROLES = ("design", "assignment", "return", "review", "source-stated")
CAPS = {"max_records": 500, "max_file_bytes": 1048576, "max_depth": 64, "max_output_bytes": 4194304}
BENIGN = {"shared", "environment-unverified", "condition-inapplicable"}
DECL_KEYS = {"schema", "declaration_id", "version", "status", "module", "implementation", "coverage", "no_requirements",
             "requirements", "withheld", "provenance", "supersedes"}


class Refusal(Exception):
    pass


class PartialWrite(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Refusal(msg)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical(v) -> bytes:
    return (json.dumps(v, sort_keys=True, indent=1, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def strict_json(data: bytes, where: str):
    def pairs(seq):
        out = {}
        for k, v in seq:
            need(k not in out, f"{where}: duplicate key {k}")
            out[k] = v
        return out

    def nonfinite(name):
        raise Refusal(f"{where}: non-finite number {name}")
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)
    except UnicodeDecodeError:
        raise Refusal(f"{where}: not UTF-8") from None
    except json.JSONDecodeError as exc:
        raise Refusal(f"{where}: invalid JSON ({exc.msg})") from None


def exact(obj, keys, where):
    need(isinstance(obj, dict) and set(obj) == set(keys), f"{where} must have exactly {sorted(keys)}")


def text(v, where, allow_empty=False):
    need(isinstance(v, str) and (allow_empty or v.strip()) and len(v) <= 4000, f"{where} must be text")
    return v


def label(v, where):
    need(isinstance(v, str) and LABEL.fullmatch(v) is not None, f"{where} must be a label")
    return v


def hexval(v, rx, where, nullable=False):
    if nullable and v is None:
        return v
    need(isinstance(v, str) and rx.fullmatch(v) is not None, f"{where} must be {'null or ' if nullable else ''}lowercase hex")
    return v


def count(v, where):
    need(type(v) is int and v >= 0, f"{where} must be a non-negative integer")
    return v


def rel_ok(v) -> bool:
    return (isinstance(v, str) and 0 < len(v) <= 1000 and "\\" not in v and ":" not in v and not v.startswith("/")
            and all(p not in ("", ".", "..") for p in v.split("/")))


def is_link(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool((getattr(st, "st_file_attributes", 0) or 0) & 0x400)


def abs_path(t, where) -> Path:
    need(isinstance(t, str) and os.path.isabs(t) and not t.startswith(("\\\\", "//")), f"{where} must be an absolute local path")
    p = Path(os.path.abspath(t))
    for a in [p, *p.parents]:
        need(not is_link(a), f"{where} passes through a link: {a}")
    return p


def read_file(p: Path, limit: int, where: str) -> bytes:
    need(p.is_file() and not is_link(p), f"{where} must be a regular file: {p}")
    need(p.stat().st_size <= limit, f"{where} is over the {limit}-byte bound")
    return p.read_bytes()


def key(mod) -> str:
    return f"{mod['repository']}:{mod['path']}"


def parse_module_arg(v: str) -> dict:
    need(isinstance(v, str) and ":" in v, "--module/--to must be REPOSITORY:PATH")
    repo, _, path = v.partition(":")
    label(repo, "module repository")
    need(rel_ok(path), "module path must be repository-relative")
    return {"repository": repo, "path": path}


# ---------- validation ----------

def check_module_ref(m, where):
    exact(m, {"repository", "path"}, where)
    label(m["repository"], f"{where}.repository")
    need(rel_ok(m["path"]), f"{where}.path must be repository-relative")


def check_address(a, where):
    exact(a, {"repository", "book", "page", "face_or_pass", "file"}, where)
    label(a["repository"], f"{where}.repository")
    need(isinstance(a["book"], str) and BOOK.fullmatch(a["book"]), f"{where}.book must be a full book name such as 00.00.10.work")
    need(isinstance(a["page"], str) and PAGE.fullmatch(a["page"]), f"{where}.page must be PPPP.slug")
    need(a["face_or_pass"] is None or (isinstance(a["face_or_pass"], str) and FACE.fullmatch(a["face_or_pass"])),
         f"{where}.face_or_pass must be null, NN or NN.NN")
    need(rel_ok(a["file"]), f"{where}.file must be a relative file name")


def check_declaration(d, where):
    exact(d, DECL_KEYS, where)
    need(d["schema"] == "module-declaration/1", f"{where}: unsupported schema")
    label(d["declaration_id"], f"{where}.declaration_id")
    need(type(d["version"]) is int and d["version"] >= 1, f"{where}.version must be an integer >= 1")
    need(d["status"] in STATUSES, f"{where}.status must be one of {STATUSES}")
    m = d["module"]
    exact(m, {"repository", "path", "name", "purpose", "interface", "limits", "home"}, f"{where}.module")
    check_module_ref({"repository": m["repository"], "path": m["path"]}, f"{where}.module")
    text(m["name"], f"{where}.module.name")
    text(m["purpose"], f"{where}.module.purpose")
    for k in ("interface", "limits"):
        need(isinstance(m[k], list) and all(isinstance(x, str) and x.strip() for x in m[k]), f"{where}.module.{k} must be a list of text")
    if m["home"] is not None:
        check_address(m["home"], f"{where}.module.home")
    imp = d["implementation"]
    exact(imp, {"sha256", "bytes", "basis"}, f"{where}.implementation")
    hexval(imp["sha256"], HEX64, f"{where}.implementation.sha256")
    count(imp["bytes"], f"{where}.implementation.bytes")
    b = imp["basis"]
    exact(b, {"kind", "repository", "commit", "path"}, f"{where}.implementation.basis")
    need(b["kind"] == "git-blob", f"{where}.implementation.basis.kind must be git-blob")
    label(b["repository"], f"{where}.implementation.basis.repository")
    hexval(b["commit"], HEX40, f"{where}.implementation.basis.commit")
    need(rel_ok(b["path"]), f"{where}.implementation.basis.path must be relative")
    cov = d["coverage"]
    exact(cov, {"entry_points", "method", "complete_claim"}, f"{where}.coverage")
    need(isinstance(cov["entry_points"], list) and cov["entry_points"] and all(isinstance(x, str) and x.strip() for x in cov["entry_points"]),
         f"{where}.coverage.entry_points must be a non-empty list of text")
    text(cov["method"], f"{where}.coverage.method")
    need(cov["complete_claim"] is False, f"{where}.coverage.complete_claim must be false in this prototype")
    need(type(d["no_requirements"]) is bool, f"{where}.no_requirements must be boolean")
    reqs = d["requirements"]
    need(isinstance(reqs, list), f"{where}.requirements must be a list")
    if d["no_requirements"]:
        need(reqs == [], f"{where}: no_requirements true needs an empty requirements list")
    else:
        need(reqs != [], f"{where}: an empty requirements list needs no_requirements true (ambiguous: none declared, or not filled in?)")
    ids = set()
    for i, r in enumerate(reqs):
        check_requirement(r, f"{where}.requirements[{i}]")
        need(r["id"] not in ids, f"{where}.requirements: duplicate id {r['id']}")
        ids.add(r["id"])
    need(isinstance(d["withheld"], list), f"{where}.withheld must be a list")
    for i, w in enumerate(d["withheld"]):
        exact(w, {"what", "reason"}, f"{where}.withheld[{i}]")
        text(w["what"], f"{where}.withheld[{i}].what")
        text(w["reason"], f"{where}.withheld[{i}].reason")
    pv = d["provenance"]
    exact(pv, {"links", "unknown"}, f"{where}.provenance")
    need(isinstance(pv["links"], list) and isinstance(pv["unknown"], list), f"{where}.provenance links/unknown must be lists")
    need(all(isinstance(x, str) and x.strip() for x in pv["unknown"]), f"{where}.provenance.unknown must be text")
    need(pv["links"] or pv["unknown"], f"{where}.provenance: no links needs at least one 'unknown' statement")
    for i, ln in enumerate(pv["links"]):
        exact(ln, {"role", "address", "sha256", "commit", "status", "note"}, f"{where}.provenance.links[{i}]")
        need(ln["role"] in LINK_ROLES, f"{where}.provenance.links[{i}].role must be one of {LINK_ROLES}")
        check_address(ln["address"], f"{where}.provenance.links[{i}].address")
        hexval(ln["sha256"], HEX64, f"{where}.provenance.links[{i}].sha256", nullable=True)
        hexval(ln["commit"], HEX40, f"{where}.provenance.links[{i}].commit", nullable=True)
        need(ln["status"] in ("pinned", "unpinned") and (ln["status"] == "pinned") == (ln["sha256"] is not None),
             f"{where}.provenance.links[{i}]: status pinned if and only if sha256 is given")
        text(ln["note"], f"{where}.provenance.links[{i}].note", allow_empty=True)
    if d["supersedes"] is not None:
        exact(d["supersedes"], {"declaration_id", "version"}, f"{where}.supersedes")
        label(d["supersedes"]["declaration_id"], f"{where}.supersedes.declaration_id")
        need(type(d["supersedes"]["version"]) is int and d["supersedes"]["version"] >= 1, f"{where}.supersedes.version")


def check_requirement(r, where):
    exact(r, {"id", "kind", "target", "pin", "pin_required", "mechanism", "condition", "availability", "reason", "source_ref"}, where)
    label(r["id"], f"{where}.id")
    need(r["kind"] in KINDS, f"{where}.kind must be one of {KINDS}")
    t = r["target"]
    need(isinstance(t, dict) and len(t) == 1 and next(iter(t)) in ("module", "external", "environment", "address"),
         f"{where}.target must be exactly one of module, external, environment, address")
    tk, tv = next(iter(t.items()))
    if tk == "module":
        check_module_ref(tv, f"{where}.target.module")
    elif tk == "external":
        exact(tv, {"name", "sha256"}, f"{where}.target.external")
        text(tv["name"], f"{where}.target.external.name")
        hexval(tv["sha256"], HEX64, f"{where}.target.external.sha256", nullable=True)
    elif tk == "environment":
        exact(tv, {"name", "detail"}, f"{where}.target.environment")
        text(tv["name"], f"{where}.target.environment.name")
        text(tv["detail"], f"{where}.target.environment.detail")
    else:
        check_address(tv, f"{where}.target.address")
    need((tk == "environment") == (r["kind"] == "environment"), f"{where}: kind environment if and only if the target is an environment")
    if r["pin"] is not None:
        exact(r["pin"], {"sha256", "bytes"}, f"{where}.pin")
        hexval(r["pin"]["sha256"], HEX64, f"{where}.pin.sha256")
        count(r["pin"]["bytes"], f"{where}.pin.bytes")
    need(type(r["pin_required"]) is bool, f"{where}.pin_required must be boolean")
    need(not r["pin_required"] or r["pin"] is not None, f"{where}: pin_required true needs a pin")
    need(r["mechanism"] in MECHANISMS, f"{where}.mechanism must be one of {MECHANISMS}")
    c = r["condition"]
    exact(c, {"applies", "id", "statement", "status"}, f"{where}.condition")
    need(c["applies"] in ("always", "conditional"), f"{where}.condition.applies must be always or conditional")
    need(c["status"] in CONDITION_STATES, f"{where}.condition.status must be one of {CONDITION_STATES}")
    if c["applies"] == "always":
        need(c["id"] is None and c["statement"] is None and c["status"] == "applicable", f"{where}: an always condition has no id or statement and is applicable")
    else:
        label(c["id"], f"{where}.condition.id")
        text(c["statement"], f"{where}.condition.statement")
    want = ("unverified", "declared-unavailable") if r["kind"] == "environment" else ("not-applicable",)
    need(r["availability"] in want, f"{where}.availability must be one of {want}")
    text(r["reason"], f"{where}.reason")
    if r["source_ref"] is not None:
        exact(r["source_ref"], {"path", "lines"}, f"{where}.source_ref")
        need(rel_ok(r["source_ref"]["path"]), f"{where}.source_ref.path must be relative")
        text(r["source_ref"]["lines"], f"{where}.source_ref.lines")


# ---------- set and index ----------

def load_set(set_text: str) -> dict:
    sp = abs_path(set_text, "--set")
    raw = read_file(sp, CAPS["max_file_bytes"], "set")
    s = strict_json(raw, "set")
    exact(s, {"schema", "set_id", "coverage", "declarations", "fixtures", "select", "bounds"}, "set")
    need(s["schema"] == "module-declaration-set/1", "set: unsupported schema")
    label(s["set_id"], "set.set_id")
    text(s["coverage"], "set.coverage")
    b = s["bounds"]
    exact(b, set(CAPS), "set.bounds")
    for k, cap in CAPS.items():
        need(type(b[k]) is int and 1 <= b[k] <= cap, f"set.bounds.{k} must be an integer 1..{cap}")
    need(isinstance(s["declarations"], list) and len(s["declarations"]) <= b["max_records"], "set.declarations must be a list within max_records")
    root = sp.parent
    findings, records, seen_bytes, by_id = [], [], {}, {}
    for i, e in enumerate(s["declarations"]):
        exact(e, {"file", "sha256"}, f"set.declarations[{i}]")
        need(rel_ok(e["file"]), f"set.declarations[{i}].file must be relative to the set folder")
        hexval(e["sha256"], HEX64, f"set.declarations[{i}].sha256")
        data = read_file(abs_path(str(root / e["file"]), f"declaration {e['file']}"), b["max_file_bytes"], f"declaration {e['file']}")
        need(sha(data) == e["sha256"], f"set-pin-mismatch: {e['file']} is sha256 {sha(data)}, the set pins {e['sha256']}")
        if e["sha256"] in seen_bytes:
            findings.append({"finding": "duplicate", "files": [seen_bytes[e["sha256"]], e["file"]], "note": "identical record listed twice; kept once"})
            continue
        seen_bytes[e["sha256"]] = e["file"]
        d = strict_json(data, f"declaration {e['file']}")
        check_declaration(d, f"declaration {e['file']}")
        ident = (d["declaration_id"], d["version"])
        if ident in by_id:
            findings.append({"finding": "identity-conflict", "declaration": f"{ident[0]} v{ident[1]}",
                             "files": [by_id[ident]["file"], e["file"]], "note": "one declaration id and version, different bytes"})
            by_id[ident]["conflict"] = True
            records.append({"file": e["file"], "sha256": e["sha256"], "decl": d, "conflict": True})
            continue
        rec = {"file": e["file"], "sha256": e["sha256"], "decl": d, "conflict": False}
        by_id[ident] = rec
        records.append(rec)
    need(isinstance(s["fixtures"], list) and len(s["fixtures"]) <= b["max_records"], "set.fixtures must be a list within max_records")
    fixtures = []
    for i, f in enumerate(s["fixtures"]):
        exact(f, {"module", "file", "sha256"}, f"set.fixtures[{i}]")
        check_module_ref(f["module"], f"set.fixtures[{i}].module")
        need(rel_ok(f["file"]), f"set.fixtures[{i}].file must be relative")
        hexval(f["sha256"], HEX64, f"set.fixtures[{i}].sha256")
        data = read_file(abs_path(str(root / f["file"]), f"fixture {f['file']}"), b["max_file_bytes"], f"fixture {f['file']}")
        need(sha(data) == f["sha256"], f"set-pin-mismatch: fixture {f['file']} is sha256 {sha(data)}, the set pins {f['sha256']}")
        fixtures.append(dict(f, bytes=len(data)))
    need(isinstance(s["select"], list), "set.select must be a list")
    select = {}
    for i, x in enumerate(s["select"]):
        exact(x, {"module", "declaration_id", "version"}, f"set.select[{i}]")
        check_module_ref(x["module"], f"set.select[{i}].module")
        need(key(x["module"]) not in select, f"set.select: module {key(x['module'])} selected twice")
        select[key(x["module"])] = (label(x["declaration_id"], f"set.select[{i}].declaration_id"), x["version"])
    by_module = {}
    for r in records:
        by_module.setdefault(key(r["decl"]["module"]), []).append(r)
    for mk, rs in by_module.items():  # one implementation in two different non-superseding records is ambiguous identity
        for a in rs:
            for c in rs:
                if a is c or a["decl"]["implementation"]["sha256"] != c["decl"]["implementation"]["sha256"]:
                    continue
                sup = lambda x, y: x["decl"]["supersedes"] == {"declaration_id": y["decl"]["declaration_id"], "version": y["decl"]["version"]}
                if not (sup(a, c) or sup(c, a)) and a["file"] < c["file"]:
                    findings.append({"finding": "identity-conflict", "module": mk, "files": [a["file"], c["file"]],
                                     "note": "the same implementation bytes are declared by two records that do not supersede each other"})
                    a["conflict"] = c["conflict"] = True
    for mk, sel in select.items():
        need(any((r["decl"]["declaration_id"], r["decl"]["version"]) == sel for r in by_module.get(mk, [])),
             f"set.select names {sel[0]} v{sel[1]} for {mk}, which the set does not declare")
    return {"path": str(sp), "sha256": sha(raw), "set": s, "records": records, "by_module": by_module, "fixtures": fixtures,
            "select": select, "findings": findings, "bounds": b}


def summary(r) -> dict:
    d = r["decl"]
    return {"declaration_id": d["declaration_id"], "version": d["version"], "file": r["file"], "record_sha256": r["sha256"],
            "implementation_sha256": d["implementation"]["sha256"], "status": d["status"]}


def resolve_root(S, mk):
    rs = S["by_module"].get(mk, [])
    if not rs:
        return None, "undeclared"
    if mk in S["select"]:
        r = next(x for x in rs if (x["decl"]["declaration_id"], x["decl"]["version"]) == S["select"][mk])
        return r, "selected"
    if len(rs) == 1:
        return rs[0], "single"
    return None, "ambiguous-version"


def resolve_target(S, req):
    """(resolution, record or None, detail) for a module target (CONTRACT §5)."""
    mk = key(req["target"]["module"])
    rs = S["by_module"].get(mk, [])
    if not rs:
        return "record-missing", None, {"module": mk}
    if req["pin"] is not None:  # a pin is the pair {sha256, bytes}; declarations are compared with each other, no file is measured
        hits = [r for r in rs if r["decl"]["implementation"]["sha256"] == req["pin"]["sha256"]]
        if not hits:
            return "pin-differs", None, {"pinned": req["pin"]["sha256"], "declared": sorted({r["decl"]["implementation"]["sha256"] for r in rs})}
        pairs = [r for r in hits if r["decl"]["implementation"]["bytes"] == req["pin"]["bytes"]]
        if not pairs:
            return "identity-pair-mismatch", None, {"pinned": req["pin"],
                                                    "declared": [{"declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}",
                                                                  "bytes": r["decl"]["implementation"]["bytes"]} for r in hits],
                                                    "note": "declared identities disagree; no module file was measured"}
        if len(pairs) == 1 and not pairs[0]["conflict"]:
            return "resolved", pairs[0], None
        return "identity-conflict", None, {"records": [r["file"] for r in pairs]}
    r, how = resolve_root(S, mk)
    if r is None:
        return how if how != "undeclared" else "record-missing", None, {"declared_versions": [summary(x) for x in rs]}
    return ("selected" if how == "selected" else "single-unpinned"), r, None


def record_findings(r):
    d, out = r["decl"], []
    for w in d["withheld"]:
        out.append({"finding": "withheld", "what": w["what"], "reason": w["reason"]})
    if not d["provenance"]["links"]:
        out.append({"finding": "provenance-unknown", "unknown": d["provenance"]["unknown"]})
    for ln in d["provenance"]["links"]:
        if ln["status"] == "unpinned":
            out.append({"finding": "provenance-unpinned", "role": ln["role"], "address": ln["address"]})
    return out


def condition_state(req, overrides):
    c = req["condition"]
    if c["applies"] == "always":
        return "applicable", "record"
    if c["id"] in overrides:
        return overrides[c["id"]], "caller"
    return c["status"], "record"


def edge_entry(S, r, req, path, depth, overrides):
    state, by = condition_state(req, overrides)
    tk, tv = next(iter(req["target"].items()))
    e = {"from": key(r["decl"]["module"]), "from_declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}",
         "requirement_id": req["id"], "kind": req["kind"], "mechanism": req["mechanism"], "target": req["target"], "pin": req["pin"],
         "condition": dict(req["condition"], effective=state, stated_by=by), "reason": req["reason"], "source_ref": req["source_ref"],
         "path": path, "depth": depth, "resolution": None, "resolved_to": None, "findings": []}
    nxt = None
    if state == "inapplicable":
        e["findings"].append({"finding": "condition-inapplicable", "condition": req["condition"]["id"]})
    elif state == "unknown":
        e["findings"].append({"finding": "condition-unknown", "condition": req["condition"]["id"], "statement": req["condition"]["statement"]})
    if tk == "module":
        res, tr, detail = resolve_target(S, req)
        e["resolution"] = res
        if tr is not None:
            e["resolved_to"] = summary(tr)
            nxt = tr if state != "inapplicable" else None
        else:
            e["findings"].append(dict({"finding": res}, **(detail or {})))
    elif tk == "external":
        e["resolution"] = "not-a-module"
        e["findings"].append({"finding": "external-unverified", "name": tv["name"], "sha256": tv["sha256"]})
    elif tk == "environment":
        e["resolution"] = "not-a-module"
        e["findings"].append({"finding": "environment-unavailable" if req["availability"] == "declared-unavailable" else "environment-unverified",
                              "name": tv["name"]})
    else:
        e["resolution"] = "not-a-module"
        e["findings"].append({"finding": "address-unresolved", "address": tv, "note": "listed, not opened or verified"})
    return e, nxt


def walk(S, root, transitive, max_depth, overrides):
    """Bounded iterative walk; cycles and shared nodes are findings, never recursion."""
    edges, extra = [], []
    seen_nodes = {}
    stack = [(root, [key(root["decl"]["module"])], 0)]
    visited_records = {root["sha256"]: root}
    while stack:
        r, path, depth = stack.pop()
        children = []
        for req in r["decl"]["requirements"]:  # edges in declared order; children walked first-declared first
            e, nxt = edge_entry(S, r, req, path, depth + 1, overrides)
            edges.append(e)
            if nxt is None or not transitive:
                continue
            nk = key(nxt["decl"]["module"])
            if nk in path:
                e["findings"].append({"finding": "cycle", "cycle": path[path.index(nk):] + [nk]})
                continue
            if nxt["sha256"] in seen_nodes:
                e["findings"].append({"finding": "shared", "first_reached_by": seen_nodes[nxt["sha256"]]})
                continue
            if depth + 1 >= max_depth:  # only a module with requirements left unwalked is a truncation (05.02 §4)
                if nxt["decl"]["requirements"]:
                    e["findings"].append({"finding": "depth-limit", "max_depth": max_depth, "unwalked": nk})
                else:
                    seen_nodes[nxt["sha256"]] = path + [nk]
                    visited_records[nxt["sha256"]] = nxt
                continue
            seen_nodes[nxt["sha256"]] = path + [nk]
            visited_records[nxt["sha256"]] = nxt
            children.append((nxt, path + [nk], depth + 1))
        stack.extend(reversed(children))
    for r in visited_records.values():
        for f in record_findings(r):
            extra.append(dict(f, declaration=f"{r['decl']['declaration_id']} v{r['decl']['version']}", module=key(r["decl"]["module"])))
    return edges, extra, list(visited_records.values())


def result(S, command, query, root_state, root_rec, edges, extra, visited, more=None):
    names = [f["finding"] for e in edges for f in e["findings"]] + [f["finding"] for f in extra] + [f["finding"] for f in S["findings"]]
    if root_state in ("undeclared", "ambiguous-version"):
        names.append(root_state)
    status = "complete-for-declared-coverage" if all(n in BENIGN for n in names) else "incomplete"
    out = {"schema": "module-dependency-result/1", "command": command, "query": query,
           "set": {"path": S["path"], "sha256": S["sha256"], "set_id": S["set"]["set_id"], "coverage": S["set"]["coverage"],
                   "records": len(S["records"])},
           "root": {"state": root_state, "declaration": summary(root_rec) if root_rec else None,
                    "provenance": root_rec["decl"]["provenance"] if root_rec else None},
           "requirements": None if root_rec is None else edges,
           "record_findings": extra, "set_findings": S["findings"],
           "finding_counts": {n: names.count(n) for n in sorted(set(names))},
           "coverage": [{"declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}", "module": key(r["decl"]["module"]),
                         "entry_points": r["decl"]["coverage"]["entry_points"], "method": r["decl"]["coverage"]["method"],
                         "complete_claim": False} for r in visited],
           "status": status,
           "note": "Prototype declarations: answers cover only the declared edges and listed records; not proof of runtime closure."}
    if more:
        out.update(more)
    return out


def parse_conditions(items):
    out = {}
    for it in items or []:
        cid, _, st = it.partition("=")
        label(cid, "--condition id")
        need(st in CONDITION_STATES, f"--condition {cid}: state must be one of {CONDITION_STATES}")
        need(cid not in out, f"--condition {cid} given twice")
        out[cid] = st
    return out


def cmd_requires(S, module, transitive, depth, overrides):
    mk = key(module)
    md = min(depth or S["bounds"]["max_depth"], S["bounds"]["max_depth"])
    root, how = resolve_root(S, mk)
    q = {"module": mk, "transitive": transitive, "max_depth": md, "caller_conditions": overrides}
    if root is None:
        state = how
        return result(S, "requires", q, state, None, [], [], [],
                      {"declared_versions": [summary(x) for x in S["by_module"].get(mk, [])]})
    edges, extra, visited = walk(S, root, transitive, md, overrides)
    state = "declared-dependency-free" if root["decl"]["no_requirements"] else "declared"
    return result(S, "requires", q, state, root, edges, extra, visited, {"selection": how})


def cmd_explain(S, module, to, overrides):
    full = cmd_requires(S, module, True, None, overrides)
    tk = key(to)
    if full["requirements"] is None:
        return dict(full, command="explain", paths=[])
    paths = []
    for e in full["requirements"]:
        t = e["target"].get("module")
        if t and key(t) == tk:
            paths.append({"path": e["path"] + [tk], "via_requirement": e["requirement_id"], "from_declaration": e["from_declaration"],
                          "mechanism": e["mechanism"], "condition": e["condition"]["effective"], "resolution": e["resolution"]})
    return dict(full, command="explain", query=dict(full["query"], to=tk), paths=paths,
                explain_note="every declared edge into the target found in the bounded walk; none means no declared path, not proof of independence")


def cmd_impacted(S, module, implementation, depth):
    mk = key(module)
    md = min(depth or S["bounds"]["max_depth"], S["bounds"]["max_depth"])
    reverse = {}
    for r in S["records"]:
        for req in r["decl"]["requirements"]:
            t = req["target"].get("module")
            if t:
                reverse.setdefault(key(t), []).append((r, req))
    out, frontier, seen, unexpanded = [], [(mk, [mk], 0)], {mk}, []
    while frontier:  # breadth-first to md levels; a consumer at the last level with consumers of its own is unexpanded, not absent
        tk, path, d = frontier.pop(0)
        for r, req in reverse.get(tk, []):
            ck = key(r["decl"]["module"])
            pin = req["pin"]
            targets = [x for x in S["by_module"].get(tk, [])]
            same = [x for x in targets if pin and x["decl"]["implementation"]["sha256"] == pin["sha256"]]
            row = {"consumer": ck, "consumer_declaration": summary(r), "requirement_id": req["id"], "requires": tk, "mechanism": req["mechanism"],
                   "kind": req["kind"], "pin": pin, "condition": req["condition"], "depth": d + 1, "path": path + [ck],
                   "pin_vs_declarations": ("unpinned" if pin is None else "undeclared-bytes" if not same else
                                           "matches-declared" if any(x["decl"]["implementation"]["bytes"] == pin["bytes"] for x in same) else "pair-mismatch"),
                   "revisit": "cycle" if ck in path else ("shared" if ck in seen else None),
                   "provenance": r["decl"]["provenance"]}
            if d == 0 and implementation:
                row["against_implementation"] = "unpinned" if pin is None else ("pin-matches" if pin["sha256"] == implementation else "pin-differs")
            elif d > 0:
                row["against_implementation"] = "transitive: via " + tk
            out.append(row)
            if row["revisit"]:
                continue
            seen.add(ck)
            if d + 1 < md:
                frontier.append((ck, path + [ck], d + 1))
            elif reverse.get(ck):
                unexpanded.append({"module": ck, "direct_declared_consumers": len(reverse[ck]), "path": path + [ck]})
    declared = [summary(x) for x in S["by_module"].get(mk, [])]
    names = [f["finding"] for f in S["findings"]] + [f"{r['revisit']}" for r in out if r["revisit"] == "cycle"] + \
            ["pair-mismatch" for r in out if r["pin_vs_declarations"] == "pair-mismatch"]
    if not declared:
        names.append("record-missing")
    if implementation and not any(x["implementation_sha256"] == implementation for x in declared):
        names.append("implementation-undeclared")
    findings = [{"finding": "depth-limit", "max_depth": md, "unexpanded": unexpanded}] if unexpanded else []
    names += [f["finding"] for f in findings]
    return {"schema": "module-dependency-result/1", "command": "impacted",
            "query": {"module": mk, "implementation": implementation, "max_depth": md},
            "implementation_compared": "sha256 only",
            "set": {"path": S["path"], "sha256": S["sha256"], "set_id": S["set"]["set_id"], "coverage": S["set"]["coverage"], "records": len(S["records"])},
            "target_declarations": declared, "consumers": out, "unexpanded": unexpanded, "findings": findings, "set_findings": S["findings"],
            "finding_counts": {n: names.count(n) for n in sorted(set(names))},
            "status": "truncated" if unexpanded else "candidates-for-review",
            "note": ("Derived from declared edges in this set only. These are candidates for Prime review; nothing is upgraded, invalidated, retested "
                     "or edited." + (" The walk stopped at max_depth with consumers left unexpanded: rerun with a larger --depth." if unexpanded else ""))}


def cmd_identity(S):
    rows = []
    for f in S["fixtures"]:
        mk = key(f["module"])
        decls = S["by_module"].get(mk, [])
        digest = [r for r in decls if r["decl"]["implementation"]["sha256"] == f["sha256"]]
        same = [summary(r) for r in digest if r["decl"]["implementation"]["bytes"] == f["bytes"]]
        result = ("identical" if same else "declaration-length-wrong" if digest else "changed" if decls else "record-missing")
        rows.append({"module": mk, "file": f["file"], "sha256": f["sha256"], "bytes": f["bytes"], "measured": True,
                     "result": result, "matches": same,
                     "length_contradicted_by": [{"declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}",
                                                 "declared_bytes": r["decl"]["implementation"]["bytes"]} for r in digest if not
                                                r["decl"]["implementation"]["bytes"] == f["bytes"]],
                     "declared_implementations": sorted({r["decl"]["implementation"]["sha256"] for r in decls})})
    names = [r["result"] for r in rows if r["result"] != "identical"] + [f["finding"] for f in S["findings"]]
    return {"schema": "module-dependency-result/1", "command": "identity", "set": {"path": S["path"], "sha256": S["sha256"]},
            "fixtures": rows, "finding_counts": {n: names.count(n) for n in sorted(set(names))},
            "status": "complete-for-declared-coverage" if not names else "incomplete",
            "note": "Byte identity of the listed fixture copies only; identical bytes are not semantic compatibility."}


def cmd_index(S, out_text):
    out = abs_path(out_text, "--out")
    need(not os.path.lexists(out), f"--out {out} already exists; nothing was written")
    need(out.parent.is_dir() and not is_link(out.parent), "--out parent must be an existing plain directory")
    set_dir = Path(S["path"]).parent
    need(os.path.commonpath([os.path.normcase(str(out)), os.path.normcase(str(set_dir))]) != os.path.normcase(str(set_dir)),
         "--out must not lie inside the set folder")
    edges, reverse = [], {}
    for r in S["records"]:
        for req in r["decl"]["requirements"]:
            tk, tv = next(iter(req["target"].items()))
            tkey = key(tv) if tk == "module" else f"{tk}:{json.dumps(tv, sort_keys=True)}"
            edges.append({"from": key(r["decl"]["module"]), "declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}",
                          "requirement_id": req["id"], "kind": req["kind"], "target": tkey, "pin": req["pin"]})
            reverse.setdefault(tkey, []).append({"consumer": key(r["decl"]["module"]), "requirement_id": req["id"],
                                                 "declaration": f"{r['decl']['declaration_id']} v{r['decl']['version']}"})
    idx = {"schema": "module-dependency-index/1", "derived_from": {"set": S["path"], "set_sha256": S["sha256"], "set_id": S["set"]["set_id"],
                                                                   "coverage": S["set"]["coverage"], "records": [summary(r) for r in S["records"]]},
           "modules": {mk: [summary(r) for r in rs] for mk, rs in sorted(S["by_module"].items())},
           "edges": edges, "reverse": dict(sorted(reverse.items())), "set_findings": S["findings"],
           "note": "derived and rebuildable from the set; not an authoritative module list"}
    data = canonical(idx)
    need(len(data) <= S["bounds"]["max_output_bytes"], "index is over max_output_bytes")
    os.mkdir(out)
    try:
        write_file(out / "index.json", data)
        write_file(out / "INDEX-STATUS.json", canonical({"status": "complete", "index_sha256": sha(data)}))
    except OSError as exc:
        raise PartialWrite(f"index write failed in {out}: {type(exc).__name__}: {exc}; files so far are kept") from None
    return {"schema": "module-dependency-result/1", "command": "index", "out": str(out), "index_sha256": sha(data),
            "modules": len(idx["modules"]), "edges": len(edges), "status": "written"}


def write_file(p: Path, data: bytes) -> None:
    """Exclusive create; a hook point for partial-write tests."""
    with open(p, "xb") as h:
        h.write(data)


def cmd_delta(old_text, new_text, change_text, create=False):
    def load(t, where, check):
        p = abs_path(t, where)
        raw = read_file(p, CAPS["max_file_bytes"], where)
        d = strict_json(raw, where)
        check(d, where)
        return d, sha(raw)
    if create:  # creation route (05.02 §5): no predecessor exists and none may be supplied
        need(old_text is None, "--old cannot be used with --create: a new module has no predecessor")
    else:
        need(old_text is not None, "a revision needs --old; for a new module use --create")
    new, new_sha = load(new_text, "--new", check_declaration)
    ch, ch_sha = load(change_text, "--change", check_change)
    f = []

    def mismatch(what, detail):
        f.append({"finding": "change-mismatch", "what": what, "detail": detail})
    if create:
        return create_delta(new, new_sha, ch, ch_sha, new_text, change_text, f, mismatch)
    old, old_sha = load(old_text, "--old", check_declaration)  # the predecessor path is validated before the record's claim about it
    need(ch["old"] is not None, "a revision needs change.old; for a new module use --create")
    if key(old["module"]) != key(new["module"]) or key(ch["module"]) != key(new["module"]):
        mismatch("module", [key(old["module"]), key(new["module"]), key(ch["module"])])
    if new["supersedes"] != {"declaration_id": old["declaration_id"], "version": old["version"]}:
        mismatch("supersedes", new["supersedes"])
    if ch["old"] is None or (ch["old"]["declaration_id"], ch["old"]["version"], ch["old"]["sha256"]) != (old["declaration_id"], old["version"], old_sha):
        mismatch("old", ch["old"])
    if (ch["new"]["declaration_id"], ch["new"]["version"], ch["new"]["sha256"]) != (new["declaration_id"], new["version"], new_sha):
        mismatch("new", ch["new"])
    if ch["implementation"] != {"sha256": new["implementation"]["sha256"], "bytes": new["implementation"]["bytes"]}:
        mismatch("implementation", ch["implementation"])
    o = {r["id"]: r for r in old["requirements"]}
    n = {r["id"]: r for r in new["requirements"]}
    computed = {"introduced": sorted(set(n) - set(o)), "removed": sorted(set(o) - set(n)),
                "changed": sorted(i for i in set(o) & set(n) if o[i] != n[i])}
    fields = {i: sorted(k for k in n[i] if n[i][k] != o[i].get(k)) for i in computed["changed"]}
    submitted = {k: sorted(x["requirement_id"] for x in ch["relationships"][k]) for k in ("introduced", "removed", "changed")}
    for k in computed:
        if computed[k] != submitted[k]:
            mismatch(f"relationships.{k}", {"computed": computed[k], "submitted": submitted[k]})
    for x in ch["relationships"]["changed"]:
        if x["requirement_id"] in fields and sorted(x["fields"]) != fields[x["requirement_id"]]:
            mismatch(f"changed {x['requirement_id']} fields", {"computed": fields[x["requirement_id"]], "submitted": sorted(x["fields"])})
    return {"schema": "module-dependency-result/1", "command": "delta", "mode": "revise",
            "inputs": {"old": {"path": old_text, "sha256": old_sha}, "new": {"path": new_text, "sha256": new_sha}, "change": {"path": change_text, "sha256": ch_sha}},
            "computed": computed, "changed_fields": fields, "authorized_by": ch["authorized_by"], "evidence": ch["evidence"],
            "findings": f, "status": "consistent" if not f else "inconsistent",
            "prime_reviews": "whether the relationships are true and sufficient, the reasons and conditions, and readiness for reuse; compute checked identities and the declared delta only"}


def create_delta(new, new_sha, ch, ch_sha, new_text, change_text, f, mismatch):
    """A new module: every initial requirement is introduced with a reason; nothing is changed or removed."""
    if ch["old"] is not None:
        mismatch("old", {"submitted": ch["old"], "expected": None})
    if new["supersedes"] is not None:
        mismatch("supersedes", {"submitted": new["supersedes"], "expected": None})
    if new["version"] != 1:
        mismatch("version", {"submitted": new["version"], "expected": 1})
    if key(ch["module"]) != key(new["module"]):
        mismatch("module", [key(ch["module"]), key(new["module"])])
    if (ch["new"]["declaration_id"], ch["new"]["version"], ch["new"]["sha256"]) != (new["declaration_id"], new["version"], new_sha):
        mismatch("new", ch["new"])
    if ch["implementation"] != {"sha256": new["implementation"]["sha256"], "bytes": new["implementation"]["bytes"]}:
        mismatch("implementation", ch["implementation"])
    ids = sorted(r["id"] for r in new["requirements"])
    submitted = sorted(x["requirement_id"] for x in ch["relationships"]["introduced"])
    if ids != submitted:
        mismatch("relationships.introduced", {"computed": ids, "submitted": submitted})
    for k in ("changed", "removed"):
        if ch["relationships"][k]:
            mismatch(f"relationships.{k}", {"submitted": ch["relationships"][k], "expected": []})
    return {"schema": "module-dependency-result/1", "command": "delta", "mode": "create",
            "inputs": {"old": None, "new": {"path": new_text, "sha256": new_sha}, "change": {"path": change_text, "sha256": ch_sha}},
            "computed": {"introduced": ids, "removed": [], "changed": []}, "changed_fields": {},
            "dependency_free": new["no_requirements"], "authorized_by": ch["authorized_by"], "evidence": ch["evidence"],
            "findings": f, "status": "consistent" if not f else "inconsistent",
            "prime_reviews": "whether the initial relationships are true and sufficient, the reasons and conditions, and readiness for reuse; compute checked identities and the declared creation only"}


def check_change(c, where):
    exact(c, {"schema", "module", "authorized_by", "old", "new", "implementation", "evidence", "relationships"}, where)
    need(c["schema"] == "module-change/1", f"{where}: unsupported schema")
    check_module_ref(c["module"], f"{where}.module")
    exact(c["authorized_by"], {"address", "item"}, f"{where}.authorized_by")
    check_address(c["authorized_by"]["address"], f"{where}.authorized_by.address")
    need(isinstance(c["authorized_by"]["item"], str) and ITEM.fullmatch(c["authorized_by"]["item"]), f"{where}.authorized_by.item must be #NN")
    for k in ("old", "new"):
        if k == "old" and c[k] is None:
            continue
        exact(c[k], {"declaration_id", "version", "sha256"}, f"{where}.{k}")
        hexval(c[k]["sha256"], HEX64, f"{where}.{k}.sha256")
    exact(c["implementation"], {"sha256", "bytes"}, f"{where}.implementation")
    need(isinstance(c["evidence"], list), f"{where}.evidence must be a list")
    for i, e in enumerate(c["evidence"]):
        exact(e, {"role", "address", "sha256", "note"}, f"{where}.evidence[{i}]")
        need(e["role"] in ("return", "test", "demo"), f"{where}.evidence[{i}].role")
        if e["address"] is not None:
            check_address(e["address"], f"{where}.evidence[{i}].address")
        hexval(e["sha256"], HEX64, f"{where}.evidence[{i}].sha256", nullable=True)
    rel = c["relationships"]
    exact(rel, {"introduced", "changed", "removed"}, f"{where}.relationships")
    for k in ("introduced", "removed"):
        for i, x in enumerate(rel[k]):
            exact(x, {"requirement_id", "reason"}, f"{where}.relationships.{k}[{i}]")
            text(x["reason"], f"{where}.relationships.{k}[{i}].reason")
    for i, x in enumerate(rel["changed"]):
        exact(x, {"requirement_id", "fields", "reason"}, f"{where}.relationships.changed[{i}]")
        text(x["reason"], f"{where}.relationships.changed[{i}].reason")


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace", newline="\n")
    ap = argparse.ArgumentParser(prog="depdecl.py")
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("validate", "requires", "explain", "impacted", "identity", "index"):
        p = sub.add_parser(name)
        p.add_argument("--set", required=True)
        if name in ("requires", "explain", "impacted"):
            p.add_argument("--module", required=True)
        if name in ("requires", "impacted"):
            p.add_argument("--depth", type=int)
        if name in ("requires", "explain"):
            p.add_argument("--condition", action="append")
        if name == "requires":
            p.add_argument("--transitive", action="store_true")
        if name == "explain":
            p.add_argument("--to", required=True)
        if name == "impacted":
            p.add_argument("--implementation")
        if name == "index":
            p.add_argument("--out", required=True)
    d = sub.add_parser("delta")
    d.add_argument("--old")
    d.add_argument("--new", required=True)
    d.add_argument("--change", required=True)
    d.add_argument("--create", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.command == "delta":
            r = cmd_delta(a.old, a.new, a.change, a.create)
            return emit(r, None, 0 if r["status"] == "consistent" else 1)
        S = load_set(a.set)
        if a.command == "validate":
            r = {"schema": "module-dependency-result/1", "command": "validate", "set": {"path": S["path"], "sha256": S["sha256"]},
                 "records": [summary(x) for x in S["records"]], "fixtures": len(S["fixtures"]), "set_findings": S["findings"],
                 "status": "valid" if not S["findings"] else "valid-with-findings"}
            return emit(r, S, 0 if not S["findings"] else 1)
        if getattr(a, "depth", None) is not None:
            need(1 <= a.depth <= CAPS["max_depth"], f"--depth must be 1..{CAPS['max_depth']}")
        if a.command == "requires":
            r = cmd_requires(S, parse_module_arg(a.module), a.transitive, a.depth, parse_conditions(a.condition))
        elif a.command == "explain":
            r = cmd_explain(S, parse_module_arg(a.module), parse_module_arg(a.to), parse_conditions(a.condition))
        elif a.command == "impacted":
            if a.implementation is not None:
                hexval(a.implementation, HEX64, "--implementation")
            r = cmd_impacted(S, parse_module_arg(a.module), a.implementation, a.depth)
        elif a.command == "identity":
            r = cmd_identity(S)
        else:
            r = cmd_index(S, a.out)
            return emit(r, S, 0)
        ok = (not r["finding_counts"]) if a.command == "impacted" else r["status"] == "complete-for-declared-coverage"
        return emit(r, S, 0 if ok else 1)  # CONTRACT §7: 0 with no findings, 1 answered with findings
    except PartialWrite as exc:
        sys.stdout.write(f"partial: {exc}\n")
        return 3
    except Refusal as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except OSError as exc:
        sys.stdout.write(f"refused: {type(exc).__name__}: {exc}\n")
        return 2


def emit(r, S, code) -> int:
    data = canonical(r)
    limit = S["bounds"]["max_output_bytes"] if S else CAPS["max_output_bytes"]
    if len(data) > limit:
        sys.stdout.write(f"refused: result is {len(data)} bytes, over max_output_bytes {limit}\n")
        return 2
    sys.stdout.write(data.decode("utf-8"))
    return code


if __name__ == "__main__":
    sys.exit(main())
