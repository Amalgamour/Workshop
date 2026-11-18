#!/usr/bin/env python3
"""0710/05.03 NONPRODUCTION validator, repaired successor of design05.02/validation/validate.py.

Repairs (Prime 06.02 R2): an empty answer keeps its field's shape; a not-applicable answer
needs its declared reason; a revision patch is validated against the editable item fields;
a schema runs every check it lists and reports each one. Adds real fixture behaviour for
collision suffixes and stored revision contents, and qualified menu selection.
Evidence only: not a production validator, no installs, nothing executed from input.
usage: validate2.py --out DIR(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FORMS = HERE.parent / "forms"
OLD = HERE.parent.parent / "design05.02" / "validation"
ROUTE = re.compile(r"^\d\d\.\d\d\.\d\d\.[a-z]+/\d{4}\.[a-z0-9-]+/0\d(#.+)?$")
CTX: dict = {}


class Stop(Exception):
    def __init__(self, outcome: str, code: str, detail: str, extra: dict | None = None):
        super().__init__(detail)
        self.outcome, self.code, self.detail, self.extra = outcome, code, detail, extra or {}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(v) -> bytes:
    return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def load_set(name: str) -> dict:
    return json.loads((FORMS / f"{name}.forms.json").read_text(encoding="utf-8"))


def select(fset: dict, sel: dict) -> dict:
    if "name" in sel:
        hits = [f for f in fset["forms"] if f["name"] == sel["name"]]
    elif "kind" in sel:
        hits = [f for f in fset["forms"] if f["kind"] == sel["kind"]]
        if len(hits) == 1:
            raise Stop("refused", "select-by-kind", "selection must name the form; kind alone is not a selection")
    else:
        hits = []
    if len(hits) != 1:
        raise Stop("refused", "select-ambiguous" if hits else "select-none", f"{len(hits)} forms match {sel}")
    return hits[0]


def answer_of(present: bool, value) -> str:
    if not present:
        return "not_supplied"
    if value is None:
        return "null"
    if isinstance(value, dict) and set(value) == {"not_applicable"}:
        return "not_applicable"
    if value == "" or value == []:
        return "empty"
    return "value"


def check_shape(field: str, shape, value) -> None:
    def bad(expected):
        raise Stop("refused", "shape", f"field {field}: expected {expected}, observed {type(value).__name__} {json.dumps(value, ensure_ascii=False)[:60]}")
    if shape == "text":
        if not isinstance(value, str): bad("text")
    elif shape == "bool":
        if not isinstance(value, bool): bad("bool")
    elif shape in ("text-list", "ref-list"):
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value): bad(shape)
    elif shape == "address":
        if not isinstance(value, str): bad("address")
    elif shape == "item-ref":
        if not isinstance(value, str) or not re.fullmatch(r"#\d\d", value): bad("item reference #NN")
    elif shape == "item-patch":
        if not isinstance(value, dict) or not value: bad("non-empty object of item fields")
    elif shape == "dispositions":
        if not isinstance(value, list): bad("list of dispositions")
        for d in value:
            if not isinstance(d, dict) or d.get("disposition") not in ("integrated", "deferred", "rejected", "unresolved"): bad("disposition entries")
    elif shape == "relations":
        if not isinstance(value, list) or not all(isinstance(r, dict) and set(r) == {"relation", "other"} for r in value): bad("relations")
    elif isinstance(shape, dict):
        if not isinstance(value, dict) or set(value) != set(shape): bad(f"object with keys {sorted(shape)}")
        for k, s in shape.items():
            check_shape(f"{field}.{k}", s, value[k])
    else:
        raise Stop("refused", "form-shape-unknown", f"field {field}: the form declares an unknown shape {shape}")


def resolve(field: dict, value, fx: dict) -> None:
    kind = field.get("resolve")
    if kind == "relation" and value not in fx["relations"]:
        raise Stop("refused", "unresolved-reference", f"field {field['name']}: no registered relation for {value}")
    if kind == "page" and value not in fx["pages"]:
        raise Stop("refused", "unresolved-reference", f"field {field['name']}: page {value} does not resolve")
    if kind == "draft-item" and value not in fx["draft_items"]:
        raise Stop("refused", "unresolved-reference", f"field {field['name']}: item {value} is not in the draft")
    if kind == "record":
        for r in value:
            if r["other"] not in fx["records"]:
                raise Stop("refused", "unresolved-reference", f"field {field['name']}: record {r['other']} does not resolve")


def editable_fields(ref: str) -> list:
    form_name, block = ref.split(".")
    form = next(f for f in CTX["set"]["forms"] if f["name"] == form_name)
    assert block == "items"
    # a patch leaves out the fields it does not change; a supplied field keeps its own answers and shape
    return [dict(f, required=False, answers=sorted(set(f["answers"]) | {"not_supplied"})) for f in form["repeat"]["fields"]]


def check_fields(fields: list, data: dict, owned: list, fx: dict, where: str) -> list:
    notes = []
    names = {f["name"] for f in fields}
    for k in data:
        if k in owned:
            raise Stop("refused", "compute-owned", f"{where}: {k} is generated by compute, not supplied")
        if k not in names:
            raise Stop("refused", "unknown-field", f"{where}: unknown field {k}")
    for f in fields:
        g = f.get("meaning_ground")
        if f.get("required") and g is None:
            raise Stop("held", "no-ground", f"{where}: required field {f['name']} names no meaning ground; Director review")
        if g is not None:
            state = fx["grounds"].get(g)
            if state is None:
                raise Stop("held", "ground-missing", f"{where}: ground {g} of {f['name']} does not exist; Director review")
            if state == "draft":
                notes.append(f"{f['name']}: ground {g} is a draft (illustrative)")
        if f.get("adds_gate"):
            raise Stop("held", "form-adds-condition", f"{where}: {f['name']} adds a gate the source does not state; Director review")
        present = f["name"] in data
        ans = answer_of(present, data.get(f["name"]))
        if ans not in f["answers"]:
            code = "required-missing" if ans == "not_supplied" else "answer-not-accepted"
            raise Stop("refused", code, f"{where}: field {f['name']} answered {ans}; accepts {f['answers']}")
        v = data.get(f["name"])
        if ans == "not_applicable":
            reason = v["not_applicable"]
            if not isinstance(reason, str) or not reason.strip():
                raise Stop("refused", "na-reason", f"{where}: field {f['name']}: not applicable needs a reason text, observed {json.dumps(reason)}")
        if ans in ("value", "empty"):
            check_shape(f["name"], f["shape"], v)
            if ans == "value" and isinstance(f["shape"], dict) and "subanswers" in f:
                for k, sv in v.items():
                    if answer_of(True, sv) not in f["subanswers"]:
                        raise Stop("refused", "answer-not-accepted", f"{where}: {f['name']}.{k} answer not accepted")
            if ans == "value" and f["shape"] == "item-patch":
                notes += check_fields(editable_fields(f["editable"]), v, owned, fx, "changes")
            if ans == "value":
                resolve(f, v, fx)
    return notes


def heading_for(name: str, fx: dict) -> str:
    taken = set(fx["register"])
    if name not in taken:
        return name
    n = 2
    while f"{name} ({n})" in taken:
        n += 1
    return f"{name} ({n})"


def build(form: dict, data: dict, fx: dict, owned: list) -> tuple[dict, list]:
    notes = check_fields(form["fields"], {k: v for k, v in data.items() if k != "items"}, owned, fx, form["name"])
    rep = form.get("repeat")
    items_out = []
    if rep:
        items = data.get("items")
        if not isinstance(items, list) or len(items) < rep.get("min", 0):
            raise Stop("refused", "required-missing", f"{form['name']}: repeating block {rep['name']} needs at least {rep.get('min', 0)}")
        for i, it in enumerate(items, 1):
            if not isinstance(it, dict):
                raise Stop("refused", "shape", f"item {i}: expected object")
            notes += check_fields(rep["fields"], it, owned, fx, f"item {i}")
            items_out.append({"#NN": f"#{i:02d}", **it})
    elif "items" in data:
        raise Stop("refused", "unknown-field", f"{form['name']}: declares no repeating block; items refused")
    out = {k: v for k, v in data.items() if k != "items"}
    if items_out:
        out["items"] = items_out
    if form["name"] == "pack-create":
        rel = fx["relations"][data["source"]]
        out["output_path"] = f"{rel['work']}/{rel['next_pass']}.md"
        out["dependencies"] = fx["resolver"]
    if form["name"] == "person-create":
        out["output_path"] = f"{form['output']['page']}#{heading_for(data['name'], fx)}"
    if form["name"] == "pack-revise":
        out["item_kept"] = data["item"]
    return out, notes


def run_checks(form: dict, art: dict, fx: dict) -> list:
    create = next(f for f in CTX["set"]["forms"] if f["name"] == "pack-create")
    owned = CTX["set"]["compute_owned_keys"]
    results = []

    def one(name, fn):
        try:
            fn()
            results.append({"check": name, "ran": True, "pass": True})
        except Stop as s:
            results.append({"check": name, "ran": True, "pass": False, "code": s.code, "detail": s.detail})

    def required():
        top = {k: v for k, v in art.items() if k not in ("items", "output_path", "dependencies", "review")}
        check_fields(create["fields"], top, owned, fx, "artifact")
        items = art.get("items")
        if not isinstance(items, list) or len(items) < create["repeat"]["min"]:
            raise Stop("refused", "required-missing", "artifact: no items")
        for it in items:
            check_fields(create["repeat"]["fields"], {k: v for k, v in it.items() if k != "#NN"}, owned, fx, f"artifact {it.get('#NN')}")

    def contiguous():
        ids = [i.get("#NN") for i in art.get("items", [])]
        if not ids or ids != [f"#{n:02d}" for n in range(1, len(ids) + 1)]:
            raise Stop("refused", "items-contiguous", f"item ids {ids}")

    def dispositions():
        ds = art.get("note_dispositions")
        if not isinstance(ds, list):
            raise Stop("refused", "note-dispositions-adequate", "no dispositions")
        ids = {i.get("#NN") for i in art.get("items", [])}
        seen = {}
        for d in ds:
            seen.setdefault(d.get("note"), []).append(d)
        for note in fx["notes"]:
            got = seen.get(note, [])
            if len(got) != 1:
                raise Stop("refused", "note-dispositions-adequate", f"note {note}: {len(got)} dispositions")
            d = got[0]
            if d["disposition"] == "unresolved":
                raise Stop("refused", "note-dispositions-adequate", f"note {note} is unresolved")
            if d["disposition"] == "integrated" and d.get("item") not in ids:
                raise Stop("refused", "note-dispositions-adequate", f"note {note} names item {d.get('item')} that does not exist")
            if d["disposition"] in ("deferred", "rejected") and not (isinstance(d.get("why"), str) and d["why"].strip()):
                raise Stop("refused", "note-dispositions-adequate", f"note {note}: {d['disposition']} needs a reason")
        extra = set(seen) - set(fx["notes"])
        if extra:
            raise Stop("refused", "note-dispositions-adequate", f"dispositions for undeclared notes {sorted(extra)}")

    def deps():
        ds = art.get("dependencies")
        if not isinstance(ds, list) or not ds:
            raise Stop("refused", "dependency-states-present", "no dependency states")
        for d in ds:
            if d.get("state") not in ("resolved", "missing", "stale", "conditional", "ambiguous"):
                raise Stop("refused", "dependency-states-present", f"bad state {d}")

    table = {"required-answered": required, "items-contiguous": contiguous, "note-dispositions-adequate": dispositions, "dependency-states-present": deps}
    for name in form["checks"]:
        if name not in table:
            results.append({"check": name, "ran": False, "pass": False, "code": "check-not-implemented"})
        else:
            one(name, table[name])
    return results


def check_menu(menus: dict, sel: dict) -> dict:
    for m in menus["menus"]:
        for e in m["entries"]:
            for r in [e["rule"], e["forms_at"]] + [x["route"] for x in e.get("external", [])]:
                if not ROUTE.match(r):
                    raise Stop("refused", "route-unqualified", f"route {r} is not qualified book/page/face")
    page = [m for m in menus["menus"] if m["page"] == sel["page"]]
    if len(page) != 1:
        raise Stop("refused", "menu-page", f"no single menu for {sel['page']}")
    ent = [e for e in page[0]["entries"] if e["section"] == sel["section"]]
    if len(ent) != 1:
        raise Stop("refused", "menu-section", f"no single entry {sel['section']}")
    if not ent[0]["forms_at"].startswith(sel["page"] + "/02#"):
        raise Stop("refused", "route-external", "forms route leaves the page")
    names = [f["name"] for f in ent[0]["forms"] if f["name"] == sel["form"]]
    if len(names) != 1:
        raise Stop("refused", "select-none", f"menu has no form {sel['form']}")
    fset = load_set(sel["set"])
    form = select(fset, {"name": sel["form"]})
    if not sel["page"].endswith(fset["section"]["page"]) or fset["section"]["heading"] != sel["section"]:
        raise Stop("refused", "menu-form-mismatch", "menu route and form set disagree")
    return {"route": ent[0]["forms_at"], "form": form["name"], "kind": form["kind"], "revision": form["revision"]}


def run_case(case: dict, fx: dict, outdir: Path, cdir: Path) -> dict:
    raw = (cdir / case["input"]).read_bytes() if case.get("input") else b"{}"
    try:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise Stop("refused", "encoding", f"input is not UTF-8 at byte {e.start}; input kept unchanged")
        data = json.loads(text)
        op = case["op"]
        if op == "menu":
            menus = data if data.get("menus") else json.loads((FORMS / "menus.json").read_text(encoding="utf-8"))
            return {"outcome": "ok", "code": "ok", **check_menu(menus, case["select"])}
        fset = load_set(case["set"])
        CTX["set"] = fset
        form = select(fset, case["select"])
        bind = case.get("bind")
        result = {"form": form["name"], "kind": form["kind"]}
        if bind:
            stored = FORMS / "revisions" / f"{form['name']}.{bind['revision']}.json"
            if not stored.is_file():
                raise Stop("refused", "binding-missing", f"revision {bind['revision']} of {form['name']} is not stored")
            sb = stored.read_bytes()
            if bind.get("form_sha256") and bind["form_sha256"] != sha(sb):
                raise Stop("stale", "binding-stale", f"bound form bytes {bind['form_sha256'][:12]} differ from stored {sha(sb)[:12]}; recheck before use")
            form = json.loads(sb)
            newer = sorted(p.name for p in (FORMS / "revisions").glob(f"{form['name']}.*.json") if p.name.split(".")[1] > bind["revision"])
            if newer:
                result["note"] = f"newer stored revision(s) {newer} exist; the selected {bind['revision']} stays bound"
            result.update({"bound_revision": bind["revision"], "bound_sha256": sha(sb)})
        if op == "read":
            if form["kind"] != "card":
                raise Stop("refused", "kind", "read expects a card")
            result["body"] = form["body"]
        elif op == "build":
            if form["kind"] != "template":
                raise Stop("refused", "kind", f"{form['kind']} {form['name']} cannot build")
            art, notes = build(form, data, fx, fset["compute_owned_keys"])
            b = canon(art)
            (outdir / f"{case['id']}.artifact.json").write_bytes(b)
            result.update({"artifact_sha256": sha(b), "output_path": art.get("output_path"), "notes": notes,
                           "item_ids": [i["#NN"] for i in art.get("items", [])], "item_kept": art.get("item_kept")})
        elif op == "check":
            if form["kind"] != "schema":
                raise Stop("refused", "kind", "check expects a schema")
            src = outdir / f"{case['artifact_of']}.artifact.json" if case.get("artifact_of") else cdir / case["artifact_file"]
            art = json.loads(src.read_text(encoding="utf-8"))
            checks = run_checks(form, art, fx)
            first = next((c for c in checks if not c["pass"]), None)
            if first:
                raise Stop("refused", first.get("code", first["check"]), f"first failing check {first['check']}", {"checks": checks})
            result["checks"] = checks
        elif op == "review":
            art_b = (outdir / f"{case['artifact_of']}.artifact.json").read_bytes()
            candidate = sha(art_b)
            if case.get("change_before_review"):
                art = json.loads(art_b)
                art["items"][0]["acceptance"] += " (revised)"
                art_b = canon(art)
            named = candidate if data["candidate_sha256"] == "AS-INSPECTED" else data["candidate_sha256"]
            now = sha(art_b)
            if named != now:
                raise Stop("stale", "review-target-changed", f"review names {named[:12]}, the candidate is now {now[:12]}")
            final = json.loads(art_b)
            final["review"] = {"candidate_sha256": named, "assessment": data["assessment"]}
            fb = canon(final)
            result.update({"candidate_sha256": now, "final_sha256": sha(fb), "candidate_equals_final": now == sha(fb)})
        return {"outcome": "ok", "code": "ok", **result}
    except Stop as s:
        return {"outcome": s.outcome, "code": s.code, "detail": s.detail, **s.extra}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    out.mkdir(parents=True, exist_ok=False)
    fx = json.loads((HERE / "fixture.json").read_text(encoding="utf-8"))
    suites = [("orig", OLD / "cases.json", OLD / "cases"), ("new", HERE / "cases.json", HERE / "cases")]
    rows, mismatches = [], 0
    for suite, cfile, cdir in suites:
        for c in json.loads(cfile.read_text(encoding="utf-8"))["cases"]:
            r = run_case(c, fx, out, cdir)
            exp = c.get("expect_v2", c["expect"])
            match = r["outcome"] == exp["outcome"] and r["code"] == exp["code"]
            if "expect_output_path" in c:
                match = match and r.get("output_path") == c["expect_output_path"]
            if "expect_checks_ran" in c:
                ran = [x["check"] for x in r.get("checks", []) if x.get("ran")]
                match = match and ran == c["expect_checks_ran"]
            mismatches += not match
            rows.append({"suite": suite, "id": c["id"], "says": c["says"], "expect": exp, "expect_changed_from": c["expect"] if "expect_v2" in c else None,
                         "actual": r, "match": match})
            print(f"{'PASS' if match else 'FAIL'} {suite:<4} {c['id']:<5} expect {exp['outcome']}/{exp['code']:<28} got {r['outcome']}/{r['code']}")
    (out / "results.json").write_text(json.dumps({"schema": "0710-form-validation/2", "cases": len(rows), "mismatches": mismatches, "rows": rows},
                                                 indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"cases {len(rows)} mismatches {mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
