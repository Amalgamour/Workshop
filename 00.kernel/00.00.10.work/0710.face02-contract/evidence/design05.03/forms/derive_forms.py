#!/usr/bin/env python3
"""0710/05.03: derive the revised illustrative form sets from the preserved 05.02 files.

Changes, and only these:
- pack-revise `changes` validates against the editable pack-create item fields;
- pack-create item fields declare only the answers they need (unchanged where already minimal);
- stored revision contents for pack-create 001 and 002 (002 adds one optional item field);
- per-page machine menus with qualified routes.
usage: derive_forms.py   (writes beside itself; refuses to overwrite)
"""

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent.parent / "design05.02" / "forms"


def write(name, obj):
    p = HERE / name
    if p.exists():
        sys.exit(f"refused: {p} exists")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


pack = json.loads((OLD / "pack.forms.json").read_text(encoding="utf-8"))
pack["format_note"] = "PROPOSED example format for 0710/05.03, derived from the 05.02 set. ILLUSTRATIVE: the local subject owner is proposed, not seated (pack-subject.0423.01.proposal.md)."
create = next(f for f in pack["forms"] if f["name"] == "pack-create")
revise = next(f for f in pack["forms"] if f["name"] == "pack-revise")
for fld in revise["fields"]:
    if fld["name"] == "changes":
        fld["shape"] = "item-patch"
        fld["editable"] = "pack-create.items"
        fld["job"] = "the changed item fields; each key is an editable item field and is validated by that field's declaration"
check = next(f for f in pack["forms"] if f["name"] == "pack-check")
check["checks"] = ["required-answered", "items-contiguous", "note-dispositions-adequate", "dependency-states-present"]
check["check_notes"] = {"required-answered": "every pack-create field and item field, by its declaration",
                        "note-dispositions-adequate": "one disposition per declared note; integrated names an existing item; deferred and rejected carry a reason; unresolved fails",
                        "dependency-states-present": "a non-empty dependency list, each with a declared state"}
write("pack.forms.json", pack)
write("hostile.forms.json", json.loads((OLD / "hostile.forms.json").read_text(encoding="utf-8")))

person = json.loads((OLD / "person.forms.json").read_text(encoding="utf-8"))
person["format_note"] = "PROPOSED example format for 0710/05.03, derived from the 05.02 set. SYNTHETIC subject book."
write("person.forms.json", person)

r1 = copy.deepcopy(create)
r2 = copy.deepcopy(create)
r2["revision"] = "002"
r2["repeat"]["fields"].append({"name": "risk_note", "shape": "text", "required": False, "answers": ["value", "not_supplied"],
                               "supplier": "intelligence", "meaning_ground": None})
write("revisions/pack-create.001.json", r1)
write("revisions/pack-create.002.json", r2)

write("menus.json", {
    "format_note": "PROPOSED machine menus (face 03), one per page. Routes are qualified book/page/face#heading; a route outside the page is marked external.",
    "menus": [
        {"page": "00.00.10.work/0423.dev-authoring", "entries": [
            {"section": "Pack", "rule": "00.00.10.work/0423.dev-authoring/01#Pack", "forms_at": "00.00.10.work/0423.dev-authoring/02#Pack",
             "forms": [{"name": n, "kind": k, "purpose": p} for n, k, p in [
                 ("pack-card", "card", "What a pack holds."), ("pack-create", "template", "Build a new pack draft from its N4NN source."),
                 ("pack-revise", "template", "Change one item of an unfrozen draft."), ("pack-check", "schema", "Check a built draft before review.")]],
             "external": [{"route": "00.00.01.law/0005.ticket/01#Task", "why": "generic work-item law"}]}]},
        {"page": "10.00.01.people/0201.person", "entries": [
            {"section": "Person", "rule": "10.00.01.people/0201.person/01#Person", "forms_at": "10.00.01.people/0201.person/02#Person",
             "forms": [{"name": "person-card", "kind": "card", "purpose": "What a person record holds."},
                       {"name": "person-create", "kind": "template", "purpose": "Create one person record."}],
             "external": [{"route": "10.00.01.people/0202.register/01", "why": "where created records are written"}]}]},
    ],
    "rejected_05_02_form": {"routes": ["01#Pack", "01#Person"], "why": "relative routes for two pages in different books in one menu"},
})
print("derived")
