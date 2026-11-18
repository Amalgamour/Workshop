#!/usr/bin/env python3
"""0710/05.03: write fixture.json, cases.json and case inputs for validate2.py (new suite only).

The original 27 cases are read unchanged from design05.02/validation by validate2.py.
P1-P4 are Prime's four hostile probes (06.02 review), taken from prime-review05.02/hostile-probes.json;
a compute-owned key that was part of Prime's recorded OUTPUT (output_path, #NN) is removed to form the INPUT.
usage: make_cases2.py   (refuses to overwrite)
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE.parents[2]
CASES = HERE / "cases"
if CASES.exists() or (HERE / "cases.json").exists() or (HERE / "fixture.json").exists():
    sys.exit("refused: outputs exist")
CASES.mkdir()

old_fx = json.loads((PAGE / "evidence/design05.02/validation/fixture.json").read_text(encoding="utf-8"))
fx = dict(old_fx)
fx["note"] = "SYNTHETIC fixture registry for validate2.py (0710/05.03). Derived from the 05.02 fixture; adds resolver states and the register."
fx["resolver"] = [{"ref": "lib-build:app/librarian.py", "state": "resolved"},
                  {"ref": "lib-build:labs/review-loop-pass02/review_loop.py", "state": "conditional"}]
fx["register"] = ["Tom Wren"]
fx.pop("revisions", None)
(HERE / "fixture.json").write_text(json.dumps(fx, indent=2) + "\n", encoding="utf-8")

probes = json.loads((PAGE / "evidence/prime-review05.02/hostile-probes.json").read_text(encoding="utf-8"))


def strip(a):
    a = json.loads(json.dumps(a))
    a.pop("output_path", None)
    for it in a.get("items", []):
        it.pop("#NN", None)
    return a


def w(name, obj):
    (CASES / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


w("p1.json", strip(probes[0]["artifact"]))
w("p2.json", strip(probes[1]["artifact"]))
w("p3.json", probes[2]["artifact"])
w("p4.artifact.json", probes[3]["artifact"])

good = json.loads((PAGE / "evidence/design05.02/validation/cases/v1-pack-create.json").read_text(encoding="utf-8"))
person = json.loads((PAGE / "evidence/design05.02/validation/cases/v3-person-create.json").read_text(encoding="utf-8"))


def art(mut=None):
    a = json.loads(json.dumps(good))
    for i, it in enumerate(a["items"], 1):
        it["#NN"] = f"#{i:02d}"
    a["output_path"] = "0526.dev-authoring/05.03.md"
    a["dependencies"] = fx["resolver"]
    if mut:
        mut(a)
    return a


def mutd(i, k, v):
    def f(a):
        a["note_dispositions"][i][k] = v
    return f


w("r1.json", {**person, "aliases": []})
w("r2.json", {**good, "items": [{**good["items"][0], "open_choices": {"not_applicable": ""}}]})
w("r3.json", {"item": "#02", "changes": {"title": 5}, "reason": "x"})
w("r4.json", {"item": "#02", "changes": {"acceptance": ""}, "reason": "x"})
w("r5.json", {"item": "#09", "changes": {"acceptance": "y"}, "reason": "x"})
w("r6.json", {"item": "#02", "changes": {"#NN": "#01"}, "reason": "renumber"})
w("r7.artifact.json", art(mutd(0, "disposition", "unresolved")))
(CASES / "r8.artifact.json").write_bytes((PAGE / "evidence/design05.02/validation/run01/V1.artifact.json").read_bytes())
w("r9.artifact.json", art(mutd(0, "item", "#05")))
w("r10.artifact.json", art(lambda a: a["note_dispositions"][1].pop("why")))
w("r11.json", {**person, "name": "Tom Wren"})
w("r12.json", {**good, "items": [{**good["items"][0], "risk_note": "low"}]})
w("r14.json", {**person, "description": []})
w("r15.artifact.json", art())
w("m3.json", {"menus": [{"page": "00.00.10.work/0423.dev-authoring", "entries": [{"section": "Pack", "rule": "01#Pack", "forms_at": "02#Pack", "forms": [{"name": "pack-create", "kind": "template", "purpose": "x"}]}]}]})

ALL4 = ["required-answered", "items-contiguous", "note-dispositions-adequate", "dependency-states-present"]


def C(i, says, op, s, sel, inp, oc, code, **k):
    return {"id": i, "says": says, "op": op, "set": s, "select": sel, "input": inp, "expect": {"outcome": oc, "code": code}, **k}


cases = [
    C("P1", "Prime probe 1: list-shaped aliases given as empty text", "build", "person", {"name": "person-create"}, "p1.json", "refused", "shape"),
    C("P2", "Prime probe 2: not-applicable reason is a number", "build", "pack", {"name": "pack-create"}, "p2.json", "refused", "na-reason"),
    C("P3", "Prime probe 3: patch holds #NN, output_path, tests_passed", "build", "pack", {"name": "pack-revise"}, "p3.json", "refused", "compute-owned"),
    C("P4", "Prime probe 4: vacuous artifact; every claimed check must run", "check", "pack", {"name": "pack-check"}, None, "refused", "required-missing",
      artifact_file="p4.artifact.json", expect_checks_ran=ALL4),
    C("R1", "empty list for a list field is accepted", "build", "person", {"name": "person-create"}, "r1.json", "ok", "ok"),
    C("R2", "not-applicable with an empty reason", "build", "pack", {"name": "pack-create"}, "r2.json", "refused", "na-reason"),
    C("R3", "patch field with the wrong shape", "build", "pack", {"name": "pack-revise"}, "r3.json", "refused", "shape"),
    C("R4", "patch empties a value-only field", "build", "pack", {"name": "pack-revise"}, "r4.json", "refused", "answer-not-accepted"),
    C("R5", "patch names an item that is not in the draft", "build", "pack", {"name": "pack-revise"}, "r5.json", "refused", "unresolved-reference"),
    C("R6", "patch tries to renumber", "build", "pack", {"name": "pack-revise"}, "r6.json", "refused", "compute-owned"),
    C("R7", "schema: an unresolved disposition fails", "check", "pack", {"name": "pack-check"}, None, "refused", "note-dispositions-adequate", artifact_file="r7.artifact.json", expect_checks_ran=ALL4),
    C("R8", "schema: the 05.02 V1 artifact has no dependency states", "check", "pack", {"name": "pack-check"}, None, "refused", "dependency-states-present", artifact_file="r8.artifact.json", expect_checks_ran=ALL4),
    C("R9", "schema: integrated names a missing item", "check", "pack", {"name": "pack-check"}, None, "refused", "note-dispositions-adequate", artifact_file="r9.artifact.json", expect_checks_ran=ALL4),
    C("R10", "schema: deferred without a reason", "check", "pack", {"name": "pack-check"}, None, "refused", "note-dispositions-adequate", artifact_file="r10.artifact.json", expect_checks_ran=ALL4),
    C("R11", "collision: Tom Wren already in the register", "build", "person", {"name": "person-create"}, "r11.json", "ok", "ok", expect_output_path="0202.register/01.md#Tom Wren (2)"),
    C("R12", "bound to stored 001: a field only in 002 is unknown", "build", "pack", {"name": "pack-create"}, "r12.json", "refused", "unknown-field", bind={"revision": "001"}),
    C("R13", "bound to stored 002: the same input is accepted", "build", "pack", {"name": "pack-create"}, "r12.json", "ok", "ok", bind={"revision": "002"}),
    C("R14", "empty answer of the wrong shape for a text field", "build", "person", {"name": "person-create"}, "r14.json", "refused", "shape"),
    C("R15", "schema: a complete artifact passes every check", "check", "pack", {"name": "pack-check"}, None, "ok", "ok", artifact_file="r15.artifact.json", expect_checks_ran=ALL4),
    C("M1", "menu: qualified route to pack-create", "menu", None, {"page": "00.00.10.work/0423.dev-authoring", "section": "Pack", "form": "pack-create", "set": "pack"}, None, "ok", "ok"),
    C("M2", "menu: qualified route to person-create", "menu", None, {"page": "10.00.01.people/0201.person", "section": "Person", "form": "person-create", "set": "person"}, None, "ok", "ok"),
    C("M3", "menu: the 05.02 relative routes", "menu", None, {"page": "00.00.10.work/0423.dev-authoring", "section": "Pack", "form": "pack-create", "set": "pack"}, "m3.json", "refused", "route-unqualified"),
    C("M4", "menu: a form the menu does not list", "menu", None, {"page": "00.00.10.work/0423.dev-authoring", "section": "Pack", "form": "pack-template", "set": "pack"}, None, "refused", "select-none"),
]
(HERE / "cases.json").write_text(json.dumps({"cases": cases}, indent=1) + "\n", encoding="utf-8")
print(len(cases), "new cases")
