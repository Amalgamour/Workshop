import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
H = D / "forms" / "hostile.forms.json"
base = {"answers_written_as": "as pack.forms.json", "compute_owned_keys": ["#NN", "path", "output_path", "sha256"],
        "section": {"page": "0423.dev-authoring", "face": "02", "heading": "Pack", "governing": {"face": "01", "heading": "Pack", "state": "unresolved"}}}
H.write_text(json.dumps({**base, "format_note": "HOSTILE variants for 0710/05.02 negative cases. Not proposed forms.", "forms": [
    {"name": "pack-create-gated", "kind": "template", "purpose": "HOSTILE: adds a release gate the source does not state", "revision": "001",
     "source": {"ref": "0423/01#4", "state": "draft"},
     "fields": [{"name": "goal", "shape": "text", "required": True, "answers": ["value"], "supplier": "intelligence", "meaning_ground": "0423/01#4"},
                {"name": "risk_at_most_2", "shape": "bool", "required": True, "answers": ["value"], "supplier": "intelligence", "meaning_ground": "0423/01#4", "adds_gate": True}]},
    {"name": "pack-create-ungrounded", "kind": "template", "purpose": "HOSTILE: requires a meaning no ground requires", "revision": "001",
     "source": {"ref": "0423/01#4", "state": "draft"},
     "fields": [{"name": "goal", "shape": "text", "required": True, "answers": ["value"], "supplier": "intelligence", "meaning_ground": "0423/01#4"},
                {"name": "budget", "shape": "text", "required": True, "answers": ["value"], "supplier": "intelligence", "meaning_ground": None}]}]}, indent=2) + "\n", encoding="utf-8")

CASES = D / "validation" / "cases"
intent = {"source": "0423.dev-authoring", "goal": "Reduce manual pack and review setup.",
          "scope": {"included": ["source-linked start", "per-item input"], "excluded": [], "allowed_writes": ["new authoring draft on the linked work page"]},
          "finish": ["Prime authors one real next pack with the tool."], "executor": "Grok-1", "reviewer": "Codex Prime",
          "note_dispositions": [{"note": "0423/06.01", "disposition": "integrated", "item": "#01"},
                                {"note": "0423/06.02", "disposition": "deferred", "why": "kernel registration later"}]}
it1 = {"title": "Derive registration and source hashes", "purpose": "Derive hashes from explicit work and authority references.",
       "requirements": "Preserve missing or ambiguous data; never invent it.", "acceptance": "Prime starts from the source page and gets a usable form.",
       "breaking_change": False, "interfaces": [], "open_choices": {"not_applicable": "nothing to choose"}}
it2 = {"title": "Typed fields and UTF-8 — café", "purpose": "Serialize typed fields and UTF-8 consistently.",
       "requirements": "Prose meaning never needs a hand-computed hash.", "acceptance": "A boolean given prose is refused at that field.",
       "breaking_change": None}


def w(name, obj):
    (CASES / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


good = {**intent, "items": [it1, it2]}
w("v1-pack-create.json", good)
w("v2-pack-revise.json", {"item": "#02", "changes": {"acceptance": "A boolean given prose is refused, with the expected shape named."},
                          "reason": "Make the acceptance observable."})
w("v3-person-create.json", {"name": "Ada Wren", "first_appearance": "10.00.01.people/0301.harbour", "role": "harbour pilot", "description": "",
                            "aliases": ["the Wren"], "relations": [{"relation": "sister of", "other": "0202.register#Tom Wren"}], "date_of_death": None})
w("v4-person-not-applicable.json", {"name": "The Harbour Bell", "first_appearance": "10.00.01.people/0302.market",
                                    "date_of_death": {"not_applicable": "an object, not a living person"}})
w("r-review.json", {"candidate_sha256": "AS-INSPECTED", "assessment": "SYNTHETIC: meaning matches source; ready for Director release review."})


def mut(name, f):
    d = json.loads(json.dumps(good))
    f(d)
    w(name, d)


mut("n1-typed.json", lambda d: d["items"][0].__setitem__("breaking_change", "no, it does not"))
mut("n2-null.json", lambda d: d.__setitem__("goal", None))
mut("n3-na-not-accepted.json", lambda d: d.__setitem__("goal", {"not_applicable": "none"}))
mut("n4-na-as-string.json", lambda d: d["items"][0].__setitem__("open_choices", "not-applicable"))
mut("n5-required-missing.json", lambda d: d.pop("finish"))
mut("n6-compute-owned.json", lambda d: d["items"][0].__setitem__("#NN", "#07"))
mut("n6b-output-path.json", lambda d: d.__setitem__("output_path", "0526.dev-authoring/05.09.md"))
mut("n8-unknown.json", lambda d: d["items"][1].__setitem__("tests_passed", "yes"))
w("n7-unresolved.json", {"name": "Ada Wren", "first_appearance": "10.00.01.people/0399.nowhere"})
w("n15-person-nn.json", {"name": "Ada Wren", "first_appearance": "10.00.01.people/0301.harbour", "items": [{"#NN": "#01", "alias": "the Wren"}]})
w("n12-gated.json", {"goal": "x", "risk_at_most_2": True})
w("n13-ungrounded.json", {"goal": "x", "budget": "small"})
(CASES / "n14-cp1252.json").write_bytes(json.dumps({**intent, "goal": "PLACEHOLDER", "items": [it1]}).replace("PLACEHOLDER", "café").encode("cp1252"))


def C(i, says, op, s, sel, inp, oc, code, **k):
    return {"id": i, "says": says, "op": op, "set": s, "select": sel, "input": inp, "expect": {"outcome": oc, "code": code}, **k}


cases = [
    C("V1", "valid pack create: N/A tagged, empty list, null bool, non-ASCII; compute assigns #NN and path", "build", "pack", {"name": "pack-create"}, "v1-pack-create.json", "ok", "ok"),
    C("V2", "valid pack revise names an item (semantic ref)", "build", "pack", {"name": "pack-revise"}, "v2-pack-revise.json", "ok", "ok"),
    C("V3", "valid person create: address resolves, empty description, null death date", "build", "person", {"name": "person-create"}, "v3-person-create.json", "ok", "ok"),
    C("V4", "person not-applicable is distinct from null", "build", "person", {"name": "person-create"}, "v4-person-not-applicable.json", "ok", "ok"),
    C("V5", "card read by name", "read", "pack", {"name": "pack-card"}, None, "ok", "ok"),
    C("V6", "schema checks the V1 artifact", "check", "pack", {"name": "pack-check"}, None, "ok", "ok", artifact_of="V1"),
    C("V7", "selected revision 001 stays bound although a newer draft 002 exists", "build", "pack", {"name": "pack-create"}, "v1-pack-create.json", "ok", "ok", bind={"revision": "001"}),
    C("V8", "review binds the inspected candidate; the final artifact has its own identity", "review", "pack", {"name": "pack-create"}, "r-review.json", "ok", "ok", artifact_of="V1"),
    C("N1", "typed field: prose for a boolean (0707/05.09 attempt 1)", "build", "pack", {"name": "pack-create"}, "n1-typed.json", "refused", "shape"),
    C("N2", "null where the field does not accept null", "build", "pack", {"name": "pack-create"}, "n2-null.json", "refused", "answer-not-accepted"),
    C("N3", "not applicable where not accepted", "build", "pack", {"name": "pack-create"}, "n3-na-not-accepted.json", "refused", "answer-not-accepted"),
    C("N4", "the 05.01 example bug: not-applicable written as a plain string", "build", "pack", {"name": "pack-create"}, "n4-na-as-string.json", "refused", "shape"),
    C("N5", "required field not supplied", "build", "pack", {"name": "pack-create"}, "n5-required-missing.json", "refused", "required-missing"),
    C("N6", "model supplies #NN", "build", "pack", {"name": "pack-create"}, "n6-compute-owned.json", "refused", "compute-owned"),
    C("N6b", "model supplies an output path", "build", "pack", {"name": "pack-create"}, "n6b-output-path.json", "refused", "compute-owned"),
    C("N7", "semantic reference that does not resolve", "build", "person", {"name": "person-create"}, "n7-unresolved.json", "refused", "unresolved-reference"),
    C("N8", "unknown field (tests_passed)", "build", "pack", {"name": "pack-create"}, "n8-unknown.json", "refused", "unknown-field"),
    C("N9", "selection by kind with two templates", "build", "pack", {"kind": "template"}, "v1-pack-create.json", "refused", "select-ambiguous"),
    C("N10", "card selected to build", "build", "pack", {"name": "pack-card"}, "v1-pack-create.json", "refused", "kind"),
    C("N11", "bound form bytes changed", "build", "pack", {"name": "pack-create"}, "v1-pack-create.json", "stale", "binding-stale", bind={"revision": "001", "form_sha256": "0" * 64}),
    C("N12", "template adds a gate the source does not state", "build", "hostile", {"name": "pack-create-gated"}, "n12-gated.json", "held", "form-adds-condition"),
    C("N13", "required meaning with no ground", "build", "hostile", {"name": "pack-create-ungrounded"}, "n13-ungrounded.json", "held", "no-ground"),
    C("N14", "input in platform encoding cp1252 (0707/05.09 attempt 2)", "build", "pack", {"name": "pack-create"}, "n14-cp1252.json", "refused", "encoding"),
    C("N15", "person input copies the pack #NN habit", "build", "person", {"name": "person-create"}, "n15-person-nn.json", "refused", "unknown-field"),
    C("N16", "review after the candidate changed", "review", "pack", {"name": "pack-create"}, "r-review.json", "stale", "review-target-changed", artifact_of="V1", change_before_review=True),
    C("N17", "selected revision that does not exist", "build", "pack", {"name": "pack-create"}, "v1-pack-create.json", "refused", "binding-missing", bind={"revision": "009"}),
    C("N18", "selection names no form", "read", "pack", {"name": "pack-template"}, None, "refused", "select-none"),
]
(D / "validation" / "cases.json").write_text(json.dumps({"cases": cases}, indent=1) + "\n", encoding="utf-8")
print(len(cases), "cases")
