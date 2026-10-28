"""Fixture reader-to-projection adapter and readable Prime brief (0507.prime-support/05.13). Standard library only.

  python -B prime_brief.py brief --input IN.json [--inspect] [--json]

Contract: 00.kernel/00.00.10.work/0507.prime-support/evidence/brief05.13/CONTRACT.md. Input is labelled
batch-observation/1 fixtures (Grok-2's reader shape; the reader is never launched or imported) plus explicit SUPPLIED
coordination records. Facts the projection schema cannot express stay visible as unprojected; nothing is coerced.
The pinned, repaired state projection does lifecycle and custody. Output goes to stdout. A brief selects, releases,
accepts and dispatches nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

PROJECTION = Path(__file__).resolve().parent.parent / "state-projection-pass01" / "state_projection.py"
PROJECTION_SHA256 = "b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb"
AUTHORITY = "none; a brief selects, releases, accepts and dispatches nothing"
LABELS = {"SYNTHETIC", "SUPPLIED", "DERIVED-FROM-RETAINED-SUMMARY"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MEMBER = re.compile(r"^01\d\d\.[a-z0-9][a-z0-9.-]*$")
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
STATUS4 = ("recorded", "pending", "absent", "unknown")
OPEN_OTHER = ("open-re-review-required", "open-review-unresolved", "open-candidate-ambiguous", "open-accepted-not-terminal",
              "open-commit-custody-unverified", "claimed", "released")


class Refusal(Exception):
    pass


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def strict_json(data: bytes, label: str):
    def pairs(seq):
        out = {}
        for k, v in seq:
            need(k not in out, f"{label}: duplicate key {k}")
            out[k] = v
        return out

    def constant(name):
        raise Refusal(f"{label}: nonfinite number {name}")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError:
        raise Refusal(f"{label}: not UTF-8") from None
    except json.JSONDecodeError as exc:
        raise Refusal(f"{label}: invalid JSON ({exc.msg})") from None


def canonical_sha(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def is_str(v) -> bool:
    return isinstance(v, str)


def opt_str(v) -> bool:
    return v is None or isinstance(v, str)


def m(rx, v) -> bool:
    return isinstance(v, str) and rx.fullmatch(v) is not None


def load_projection():
    """Hash-check the repaired projection, then import it from that exact file."""
    try:
        data = PROJECTION.read_bytes()
    except OSError:
        data = None
    got = hashlib.sha256(data).hexdigest() if data is not None else None
    need(got == PROJECTION_SHA256, f"state projection at {PROJECTION} is not the pinned code (sha256 {got}); nothing was run")
    spec = importlib.util.spec_from_file_location("state_projection_pinned", PROJECTION)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------- strict input ----------

def check_reader(o, w: str) -> None:
    """Only the batch-observation/1 fields this adapter reads (contract §B2), type-checked before use."""
    need(isinstance(o, dict) and o.get("schema") == "batch-observation/1", f"{w}: not a batch-observation/1 object")
    need(o.get("authority") == "none", f"{w}: authority must be none")
    src = o.get("source")
    need(isinstance(src, dict) and all(k in src for k in ("kind", "repository", "path", "commit", "sha256", "bytes", "label")), f"{w}.source has the wrong shape")
    need(is_str(src["kind"]) and opt_str(src["repository"]) and is_str(src["path"]) and opt_str(src["label"])
         and (src["commit"] is None or m(HEX40, src["commit"])) and m(HEX64, src["sha256"]) and type(src["bytes"]) is int,
         f"{w}.source has a wrong value")
    page = o.get("page")
    need(page is None or (isinstance(page, dict) and set(page) == {"book", "page", "batch"} and all(is_str(page[k]) for k in page)),
         f"{w}.page must be null or {{book, page, batch}} strings")
    need(isinstance(o.get("document"), dict) and opt_str(o["document"].get("header_state_raw")), f"{w}.document has the wrong shape")
    a = o.get("assignment")
    need(isinstance(a, dict) and all(opt_str(a.get(k)) for k in ("executor_raw", "release_raw", "claim_raw")), f"{w}.assignment has the wrong shape")
    leg = o.get("legacy")
    need(isinstance(leg, dict) and opt_str(leg.get("status")) and opt_str(leg.get("reason")) and opt_str(leg.get("revision_id")),
         f"{w}.legacy has the wrong shape")
    ptr = o.get("pointers")
    need(isinstance(ptr, list) and all(isinstance(p, dict) and isinstance(p.get("members"), list)
                                       and all(isinstance(x, dict) and m(MEMBER, x.get("name")) for x in p["members"]) for p in ptr),
         f"{w}.pointers must be a list of pointers whose members have member names")
    am = o.get("assignment_mentions")
    need(isinstance(am, list) and all(isinstance(x, dict) and is_str(x.get("member")) for x in am), f"{w}.assignment_mentions has the wrong shape")
    cu = o.get("custody")
    need(isinstance(cu, dict) and opt_str(cu.get("basis")) and opt_str(cu.get("primary")) and isinstance(cu.get("observations"), list)
         and all(isinstance(x, dict) and is_str(x.get("member")) and opt_str(x.get("role")) for x in cu["observations"]),
         f"{w}.custody has the wrong shape")
    rv = o.get("review")
    need(isinstance(rv, dict) and isinstance(rv.get("sections"), list) and all(isinstance(x, dict) and opt_str(x.get("text_raw")) for x in rv["sections"])
         and opt_str(rv.get("text_raw")) and "binding" in rv and "typed_declaration" in rv, f"{w}.review has the wrong shape")
    need(isinstance(o.get("ambiguities"), list) and all(is_str(x) for x in o["ambiguities"]), f"{w}.ambiguities must be strings")
    need(isinstance(o.get("attention"), list) and all(is_str(x) for x in o["attention"]), f"{w}.attention must be strings")


def check_coordination(c, w: str) -> None:
    keys = {"label", "batch_id", "source_sha256", "release", "claim", "claim_actor", "candidate", "review", "publication"}
    need(isinstance(c, dict) and set(c) == keys, f"{w} must have exactly {sorted(keys)}")
    need(c["label"] == "SUPPLIED", f"{w}.label must be SUPPLIED")
    need(is_str(c["batch_id"]) and m(HEX64, c["source_sha256"]), f"{w}: batch_id or source_sha256 has the wrong form")
    need(c["release"] in STATUS4 and c["claim"] in STATUS4 and opt_str(c["claim_actor"]), f"{w}: release/claim has a wrong value")
    need(c["candidate"] is None or m(MEMBER, c["candidate"]), f"{w}.candidate must be null or a member name")
    r = c["review"]
    if r is not None:
        rk = {"member", "receipt_sha256", "disposition", "terminal", "reviewer", "followup"}
        need(isinstance(r, dict) and set(r) == rk, f"{w}.review must have exactly {sorted(rk)}")
        need(m(MEMBER, r["member"]) and m(HEX64, r["receipt_sha256"]) and r["disposition"] in ("accepted", "held", "correction-required")
             and r["terminal"] in ("completed", None) and m(LABEL, r["reviewer"]) and opt_str(r["followup"]), f"{w}.review has a wrong value")
    pub = c["publication"]
    need(isinstance(pub, dict) and set(pub) == {"status", "ref", "commit"} and pub["status"] in ("unknown", "at-ref")
         and opt_str(pub["ref"]) and (pub["commit"] is None or m(HEX40, pub["commit"])), f"{w}.publication has a wrong value")


def validate(doc) -> None:
    need(isinstance(doc, dict) and set(doc) == {"schema", "scope", "members_book", "observations", "coordination"},
         "input must have exactly schema, scope, members_book, observations, coordination")
    need(doc["schema"] == "prime-brief-input/1", "input: unsupported schema")
    sc = doc["scope"]
    need(isinstance(sc, dict) and set(sc) == {"book", "lanes"} and m(LABEL, sc["book"]) and isinstance(sc["lanes"], list)
         and sc["lanes"] and all(is_str(x) for x in sc["lanes"]) and len(set(sc["lanes"])) == len(sc["lanes"]), "scope has the wrong shape")
    need(doc["members_book"] is None or (is_str(doc["members_book"]) and os.path.isabs(doc["members_book"])), "members_book must be null or absolute")
    need(isinstance(doc["observations"], list) and isinstance(doc["coordination"], list), "observations and coordination must be lists")
    for i, e in enumerate(doc["observations"]):
        need(isinstance(e, dict) and set(e) == {"label", "note", "observation"} and e["label"] in LABELS and is_str(e["note"]),
             f"observations[{i}] must be {{label, note, observation}} with a known label")
        check_reader(e["observation"], f"observations[{i}].observation")
    for i, c in enumerate(doc["coordination"]):
        check_coordination(c, f"coordination[{i}]")


# ---------- mapping ----------

def batch_id(o) -> str | None:
    p = o["page"]
    return None if p is None else f"{p['page']}/{p['batch']}"


def map_one(entry, coord, scope) -> tuple[dict | None, dict]:
    """(state-observations/1 batch or None, mapping record). Unknowns become an unprojected reason, never a default."""
    o = entry["observation"]
    src = o["source"]
    rec = {"label": entry["label"], "note": entry["note"], "observation_sha256": canonical_sha(o),
           "source_ref": {k: src[k] for k in ("kind", "repository", "path", "commit", "sha256", "bytes", "label")},
           "evidence_kept": {"header_state_raw": o["document"]["header_state_raw"], "release_raw": o["assignment"]["release_raw"],
                             "claim_raw": o["assignment"]["claim_raw"], "executor_raw": o["assignment"]["executor_raw"],
                             "legacy": {"status": o["legacy"]["status"], "reason": o["legacy"]["reason"], "revision_id": o["legacy"]["revision_id"]},
                             "reader_ambiguities": o["ambiguities"], "reader_attention": o["attention"],
                             "typed_declaration_ignored": o["review"]["typed_declaration"] is not None},
           "decisions": [], "unprojected_reason": None}
    if o["page"] is None:
        rec["unprojected_reason"] = "page unidentified: reader gives no book/page/batch"
        return None, rec
    bid = batch_id(o)
    rec["batch_id"] = bid
    if src["kind"] == "git-blob":
        need(src["commit"] is not None, f"{bid}: a git-blob source must name a commit")
        prov = {"kind": "supplied-commit", "commit": src["commit"], "page_sha256": src["sha256"]}
        rec["decisions"].append("provenance supplied-commit from source.kind git-blob (supplied, not verified here)")
    elif src["kind"] == "live":
        prov = {"kind": "supplied-live", "commit": None, "page_sha256": src["sha256"]}
        rec["decisions"].append("provenance supplied-live from source.kind live")
    else:
        rec["unprojected_reason"] = f"schema gap: no commit/live basis for source kind {src['kind']}"
        return None, rec
    if coord is None:
        rec["unprojected_reason"] = "release and claim unknown: no SUPPLIED coordination record (raw reader lines are evidence, not decisions)"
        return None, rec
    if coord["source_sha256"] != src["sha256"]:
        rec["unprojected_reason"] = "coordination is bound to a different source sha256 (changed source against decision)"
        return None, rec
    if "unknown" in (coord["release"], coord["claim"]):
        rec["unprojected_reason"] = "schema gap: state-observations/1 cannot express an unknown release or claim"
        return None, rec
    members = []
    for p in o["pointers"]:
        for x in p["members"]:
            if x["name"] not in members:
                members.append(x["name"])
    if not o["pointers"]:
        pointer = "absent"
    elif any("pointer" in a for a in o["ambiguities"]):
        pointer = "ambiguous"
    else:
        pointer = "present" if members else "pending"
    if coord["candidate"] is not None and coord["candidate"] not in members:
        rec["unprojected_reason"] = "coordination candidate is not a member named by a reader pointer"
        return None, rec
    rec["decisions"] += [f"return.pointer {pointer}; members from pointer sections only ({len(members)})",
                         "release/claim from SUPPLIED coordination only", "reader custody.primary not used as candidate"]
    if coord["review"] is not None:
        review = {"status": "bound", "text": o["review"]["text_raw"], "binding": coord["review"]}
        rec["decisions"].append("review bound from SUPPLIED coordination (a declared fixture decision, not authenticated)")
    else:
        text = o["review"]["text_raw"]
        if not o["review"]["sections"]:
            review = {"status": "absent", "text": None, "binding": None}
        elif text is not None and text.strip() == "PENDING.":
            review = {"status": "pending", "text": text, "binding": None}
        else:
            review = {"status": "text", "text": text, "binding": None}
        rec["decisions"].append(f"review {review['status']} from reader text (exact-literal PENDING rule)")
    batch = {"id": bid, "lane": o["page"]["page"], "batch": o["page"]["batch"], "provenance": prov,
             "document": {"header_state": o["document"]["header_state_raw"]},
             "release": {"status": coord["release"], "text": "SUPPLIED coordination"},
             "claim": {"status": coord["claim"], "actor": coord["claim_actor"]},
             "return": {"pointer": pointer, "members": members, "candidate": coord["candidate"]},
             "review": review, "publication": coord["publication"]}
    return batch, rec


def build(doc: dict, do_inspect: bool, input_sha: str) -> dict:
    validate(doc)
    sp = load_projection()
    scope = doc["scope"]
    coords = {}
    for c in doc["coordination"]:
        need(c["batch_id"] not in coords, f"duplicate coordination for {c['batch_id']}")
        coords[c["batch_id"]] = c
    seen, batches, mapping, unprojected, snapshots = set(), [], [], [], []
    for i, e in enumerate(doc["observations"]):
        o = e["observation"]
        bid = batch_id(o)
        if o["page"] is not None:
            need(o["page"]["book"] == scope["book"], f"observations[{i}]: book {o['page']['book']} is outside the declared scope")
            need(o["page"]["page"] in scope["lanes"], f"observations[{i}]: lane {o['page']['page']} is outside the declared scope")
            need(bid not in seen, f"duplicate observation for {bid}")
            seen.add(bid)
        b, rec = map_one(e, coords.get(bid) if bid else None, scope)
        mapping.append(rec)
        snapshots.append({"batch_id": bid, "basis": o["custody"]["basis"], "reader_primary": o["custody"]["primary"],
                          "roles": [{"member": x["member"], "role": x["role"]} for x in o["custody"]["observations"]],
                          "note": "earlier reader observation; not used for custody here"})
        if b is None:
            unprojected.append({"id": bid, "source_ref": rec["source_ref"], "reason": rec["unprojected_reason"]})
        else:
            batches.append(b)
    for bid in coords:
        need(bid in seen, f"coordination for {bid} has no observation")
    projection = None
    if batches:
        sdoc = {"schema": "state-observations/1", "scope": {"book": scope["book"], "lanes": scope["lanes"]},
                "members_book": doc["members_book"], "batches": batches}
        try:
            projection = sp.project(sdoc, do_inspect, input_sha)
        except sp.Refusal as exc:
            raise Refusal(f"projection refused the mapped input: {exc}") from None
    lists = {k: [] for k in ("awaiting_review", "correction_or_held", "completed_fixtures", "conflicts", "other_open", "unreleased")}
    src_by_id = {r.get("batch_id"): r["source_ref"] for r in mapping}
    for r in (projection or {}).get("batches", []):
        life = r["lifecycle"]
        notes = list(r["attention"])
        hist = [x["member"] for x in r["facets"]["return"]["secondary"] if x.get("historical")]
        if hist:
            notes.append("historical retrospective member(s), never current: " + ", ".join(hist))
        item = {"id": r["id"], "source_ref": src_by_id.get(r["id"]), "lifecycle": life,
                "reason": "; ".join(notes), "followup": r["followup"]}
        if life == "returned-awaiting-review":
            lists["awaiting_review"].append(item)
        elif life in ("open-held", "open-correction-required"):
            lists["correction_or_held"].append(item)
        elif life == "completed":
            lists["completed_fixtures"].append(dict(item, note="derived fixture label; not approval or release"))
        elif life.startswith("conflict"):
            lists["conflicts"].append(item)
        elif life == "unreleased":
            lists["unreleased"].append(item)
        else:
            lists["other_open"].append(item)
    lists["unprojected"] = unprojected
    return {"schema": "prime-brief/1", "tool": {"path": str(Path(__file__).resolve()), "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            "projection_tool": {"path": str(PROJECTION), "sha256": PROJECTION_SHA256}, "input_sha256": input_sha, "scope": scope,
            "inspected": do_inspect, "inputs": [{"label": e["label"], "note": e["note"], "observation_sha256": rec["observation_sha256"],
                                                 "source_ref": rec["source_ref"]} for e, rec in zip(doc["observations"], mapping)],
            "mapping": mapping, "reader_custody_snapshots": snapshots, "projection": projection, "brief": lists,
            "attention": (projection or {}).get("attention_count", 0) + len(unprojected), "authority": AUTHORITY}


def view(b: dict) -> str:
    out = [f"Prime brief (fixture)  scope {b['scope']['book']}  inspected {b['inspected']}",
           "Every state below is derived from SUPPLIED fixtures. Nothing here is a decision.", ""]
    titles = [("awaiting_review", "Awaiting review"), ("correction_or_held", "Correction required / held"),
              ("completed_fixtures", "Completed FIXTURES (derived label; not approval)"), ("conflicts", "Conflicts"),
              ("other_open", "Other open"), ("unreleased", "Unreleased"), ("unprojected", "Unprojected / needs resolution")]
    for key, title in titles:
        items = b["brief"][key]
        out.append(f"{title} ({len(items)})")
        for it in items:
            ref = it.get("source_ref") or {}
            line = f"  - {it['id'] or '(no page)'}  [{ref.get('kind')} {(ref.get('commit') or '')[:12]} {ref.get('path')}]"
            if key == "unprojected":
                line += f"  {it['reason']}"
            else:
                line += f"  {it['lifecycle']}" + (f": {it['reason']}" if it["reason"] else "")
            out.append(line)
            if it.get("followup"):
                out.append(f"      followup: {it['followup']}")
        out.append("")
    out.append(f"authority {AUTHORITY}")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(prog="prime_brief.py")
    sub = ap.add_subparsers(dest="command", required=True)
    br = sub.add_parser("brief")
    br.add_argument("--input", required=True)
    br.add_argument("--inspect", action="store_true")
    br.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        raw = Path(args.input).read_bytes()
        result = build(strict_json(raw, "input"), args.inspect, hashlib.sha256(raw).hexdigest())
    except Refusal as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except OSError as exc:
        sys.stdout.write(f"refused: filesystem error: {type(exc).__name__}: {exc.strerror}\n")
        return 2
    sys.stdout.write(json.dumps(result, indent=1, ensure_ascii=False) + "\n" if args.json else view(result))
    return 1 if result["attention"] else 0


if __name__ == "__main__":
    sys.exit(main())
