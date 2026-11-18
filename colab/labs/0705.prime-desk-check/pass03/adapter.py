"""0705 pass03 adapter: prepare requests for the pinned prime-desk-pass01 candidate, and normalize its raw
JSON output into desk-observation/1 (pass02 CONTRACT). Lab code. Not product code.

prepare_request(...) builds SYNTHETIC REQUEST ARTIFACTS from a fixture's catalog and files. It has no access to
expected.json, and its shadow selector is the same for every case (CONTRACT R1).
normalize(...) maps only values present in the candidate's raw output plus the declared transformations in
mapping.json; everything else is listed in producer.unmapped. It refuses when raw bytes, candidate identity or
request identity differ from the run record.
"""
import hashlib
import json
import os
import re
from pathlib import Path

ADAPTER_ID = "0705-pass03-adapter/1"
BOOK = "00.kernel/00.00.10.work/"
SELECTOR_FILE = "prime-desk-shadow-selector.json"
CATALOG_FILE = "prime-desk-catalog.json"
REQUEST_FILE = "request.json"
LABEL = "SYNTHETIC REQUEST ARTIFACT (0705 pass03): built by the lab adapter for the pinned candidate interface; not an authority"
ROLE_MAP = {"decision record": "director", "goal": "goal", "previous selector": "other", "catalogued pin": None}
GAP_TO_ATTENTION = {"stale": "stale-source", "changed": "stale-source", "missing": "missing-evidence",
                    "selector": "conflict", "catalog-not-chosen": "conflict", "same-address": "conflict",
                    "packet-selection": "conflict"}
GAP_TO_REFUSAL = {"assignment-record", "selector-shape", "foreign"}
STATUS_MAP = {"matched": "ok", "stale": "changed", "changed": "changed", "missing": "absent"}
UNMAPPED = ["works", "parallel", "coverage", "workers", ["selected", "source"]]


class AdapterRefused(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def work_id(work_ref: str) -> str:
    return "w-" + re.sub(r"[^A-Za-z0-9]+", "-", work_ref).strip("-")


def canonical_snapshot_current_work(snapshot_selector_bytes: bytes) -> str:
    """R1: the pinned pack05.02 selector's current_work, as a work_ref. Same input for every case."""
    for line in snapshot_selector_bytes.decode("utf-8").split("\n"):
        if line.startswith("current_work: "):
            p = line[len("current_work: "):]
            assert p.startswith(BOOK) and p.endswith(".md")
            page, pss = p[len(BOOK):-3].split("/")
            return f"{page}/{pss}"
    raise AdapterRefused("pinned selector snapshot has no current_work")


def _fact(root: Path, rel: str):
    p = root / rel
    if not p.is_file():
        return None
    b = p.read_bytes()
    return sha(b), len(b)


def prepare_request(fixture_case_dir: Path, run_book: Path, tools_root: Path, shadow_work_ref: str) -> dict:
    """Write the shadow selector, candidate catalog and request into run_book (a copy of instance-A).
    Returns {request_path, request_sha256, artifacts}. Never reads expected.json."""
    cat = json.loads((fixture_case_dir / "catalog.json").read_bytes())
    fm = json.loads((fixture_case_dir / "fixture-manifest.json").read_bytes())
    declared = {d["path"]: d for d in cat.get("declared_sources", [])}
    selector = {"schema": "prime-desk-selector/1", "selected_work_id": work_id(shadow_work_ref),
                "checkpoint": None, "verified_result": None, "next_route": None}
    sel_b = (json.dumps(selector, indent=1) + "\n").encode("utf-8")
    (run_book / SELECTOR_FILE).write_bytes(sel_b)
    items = [{"work_id": work_id(w["work_ref"]), "address": w["work_ref"], "label": "work"} for w in cat["works"]]
    items += [{"work_id": work_id(w["work_ref"]), "address": w["work_ref"], "label": "supplied (catalog index)"} for w in cat["parallel"]
              if work_id(w["work_ref"]) not in {i["work_id"] for i in items}]
    cat_b = (json.dumps({"schema": "prime-desk-catalog/1", "items": items}, indent=1) + "\n").encode("utf-8")
    (run_book / CATALOG_FILE).write_bytes(cat_b)
    work = []
    for w in cat["works"] + [p for p in cat["parallel"] if p["work_ref"] not in {x["work_ref"] for x in cat["works"]}]:
        f = _fact(run_book, w["path"])
        pin = declared.get(w["path"], {}).get("sha256")
        h, n = (pin, f[1]) if pin and f else (f if f else ("0" * 64, 0))
        work.append({"id": work_id(w["work_ref"]), "address": w["work_ref"], "path": w["path"], "sha256": h, "bytes": n})
    references = []
    sel_fact = _fact(run_book, cat["selector"])
    if sel_fact:
        references.append({"id": "canonical-selector", "role": "assignment", "path": cat["selector"], "sha256": sel_fact[0],
                           "bytes": sel_fact[1], "label": "canonical assignment record 0401/06.01 (reference only in this interface)"})
    for path, d in declared.items():
        role = ROLE_MAP.get(d.get("role"), "other")
        if role is None or any(w["path"] == path for w in work):
            continue
        f = _fact(run_book, path)
        h, n = (d.get("sha256") or (f[0] if f else "0" * 64)), (f[1] if f else 0)
        references.append({"id": "ref-" + re.sub(r"[^A-Za-z0-9]+", "-", d.get("role", "other")).strip("-"), "role": role,
                           "path": path, "sha256": h, "bytes": n, "label": f"catalog role: {d.get('role')}"})
    workers, supplied = [], []
    for x in cat.get("workers", []):
        workers.append({"id": x["name"], "work_id": "unassigned", "evidence": None})
        supplied.append({"id": f"sup-{x['name']}", "speaker": "catalog (supplied)", "about": x["name"],
                         "text": f"{x['name']} {x['state']} (supplied label; source {x.get('source')})",
                         "limit": "supplied label from the fixture catalog; not a process check"})
    foreign = []
    xr = cat.get("cross_instance_reference")
    if xr:
        foreign.append({"id": "foreign-1", "root": fm["instances"][xr["instance"]]["root"], "address": xr["work_ref"],
                        "note": f"catalog points to {xr['instance']} for {xr['work_ref']}"})
    req = {"schema": "prime-desk-request/1",
           "instance": {"root": str(run_book), "book": "00.00.10.work", "role": "prime", "tools_root": str(tools_root)},
           "selector": {"path": SELECTOR_FILE, "sha256": sha(sel_b), "bytes": len(sel_b)},
           "references": references, "work": work, "workers": workers, "supplied": supplied,
           "attention": [], "history": [], "catalog": {"path": CATALOG_FILE, "sha256": sha(cat_b), "bytes": len(cat_b)},
           "operations": [], "legacy": [], "foreign": foreign}
    req_b = (json.dumps(req, indent=1) + "\n").encode("utf-8")
    (run_book / REQUEST_FILE).write_bytes(req_b)
    return {"request_path": str(run_book / REQUEST_FILE), "request_sha256": sha(req_b), "label": LABEL,
            "shadow_selected_work_id": selector["selected_work_id"], "artifacts": [SELECTOR_FILE, CATALOG_FILE, REQUEST_FILE]}


def _load_verified(run_dir: Path, rec: dict, key: str):
    entry = rec.get(key)
    if entry is None:
        return None, None
    raw = (run_dir / entry["stdout_file"]).read_bytes()
    if sha(raw) != entry["stdout_sha256"]:
        raise AdapterRefused(f"{key}: raw stdout bytes do not match the run record")
    try:
        return json.loads(raw.decode("utf-8")), raw
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise AdapterRefused(f"{key}: raw stdout is not JSON: {e}")


def normalize(run_dir: Path, pinned_candidate_sha256: str, fixture_case_dir: Path, view_key: str = "view"):
    """Return (observation, mapping_trace, conflicts) or raise AdapterRefused. view_key selects which recorded
    view process to map ("view", or "view_second" for the C14 second process)."""
    rec = json.loads((run_dir / "run-record.json").read_bytes())
    if rec.get("candidate_sha256") != pinned_candidate_sha256:
        raise AdapterRefused("candidate identity in the run record is not the pinned candidate")
    req_b = (run_dir / "book" / REQUEST_FILE).read_bytes()
    if sha(req_b) != rec.get("request_sha256"):
        raise AdapterRefused("request bytes do not match the run record")
    fm_b = (fixture_case_dir / "fixture-manifest.json").read_bytes()
    if sha(fm_b) != rec.get("fixture_manifest_sha256"):
        raise AdapterRefused("fixture manifest does not match the run record")
    req, fm = json.loads(req_b), json.loads(fm_b)
    view, view_raw = _load_verified(run_dir, rec, view_key)
    packet, _ = _load_verified(run_dir, rec, "packet")
    if view is None:
        raise AdapterRefused("no view output recorded")
    trace, conflicts = [], []
    roots = {os.path.normcase(os.path.abspath(v["root"])): k for k, v in fm["instances"].items()}
    roots[os.path.normcase(os.path.abspath(str(run_dir / "book")))] = "instance-A"
    path_to_addr = {w["path"]: w["address"] for w in req["work"]}
    req_sha = {x["path"]: x["sha256"] for x in req["work"] + req["references"]}

    def t(field, pointer, how="copy"):
        trace.append({"field": field, "raw": pointer, "transform": how})

    obs = {"schema": "desk-observation/1", "case_id": rec["case"],
           "producer": {"kind": "candidate",
                        "adapter": {"id": ADAPTER_ID, "sha256": sha(Path(__file__).read_bytes()), "status": "connected"},
                        "raw_outputs": [{"path": rec[k]["stdout_file"], "sha256": rec[k]["stdout_sha256"]} for k in ("view", "packet", "view_second") if rec.get(k)],
                        "unmapped": UNMAPPED},
           "instance": {"selected": None}, "selected": {"work_ref": None, "basis": None, "source": {"path": None, "sha256": None}},
           "parallel": [], "works": [], "attention": {"total": 0, "shown": 0, "overflow_route": None, "items": []},
           "holds": [], "coverage": [], "sources": [], "quotes": [], "workers": [], "refusals": [], "identity_fingerprint": None}
    inst = view.get("instance") or {}
    if inst.get("root") is not None:
        obs["instance"]["selected"] = roots.get(os.path.normcase(os.path.abspath(inst["root"])))
        t("instance.selected", "/instance/root", "root path -> fixture instance label by exact path equality")
    sel = view.get("selected")
    if "selected" not in view:
        obs["producer"]["unmapped"] = obs["producer"]["unmapped"] + ["selected"]
        t("selected", None, "key absent in raw output -> unmapped (nothing invented)")
    elif sel is None:
        obs["selected"].update(work_ref=None, basis="unknown")
        t("selected", "/selected", "explicit null selection -> work_ref null, basis unknown (declared)")
    else:
        obs["selected"].update(work_ref=sel.get("address"), basis=sel.get("basis"))
        t("selected.work_ref", "/selected/address")
        t("selected.basis", "/selected/basis", "copy verbatim (no upgrade)")
    # attention: declared candidate attention + gaps (declared kind map)
    items = []
    for i, a in enumerate(view.get("attention") or []):
        items.append({"kind": a.get("kind"), "ref": path_to_addr.get((a.get("source") or {}).get("path"))})
        t(f"attention.items[{len(items) - 1}]", f"/attention/{i}", "kind copy; ref via request path->address join")
        if a.get("kind") == "hold":
            obs["holds"].append({"id": a.get("id"), "work_ref": items[-1]["ref"], "visible": True})
            t(f"holds[{len(obs['holds']) - 1}]", f"/attention/{i}", "kind hold -> holds row")
    for i, g in enumerate(view.get("gaps") or []):
        k = GAP_TO_ATTENTION.get(g.get("kind"), "coverage-gap")
        items.append({"kind": k, "ref": path_to_addr.get(g.get("path"))})
        t(f"attention.items[{len(items) - 1}]", f"/gaps/{i}", f"gap kind {g.get('kind')} -> {k}; ref via request path->address join")
        if g.get("kind") in GAP_TO_REFUSAL:
            obs["refusals"].append({"rule_ref": g.get("check"), "target_path": g.get("path"), "target_instance": "instance-A"})
            t(f"refusals[{len(obs['refusals']) - 1}]", f"/gaps/{i}", "gap of a refusal kind -> refusals row; rule_ref = gap.check")
    obs["attention"].update(total=len(items), shown=len(items), items=items)
    t("attention.total/shown", "/attention + /gaps", "count of mapped items; the candidate shows every declared item (no overflow concept)")
    # sources: every file fact the candidate reports
    def add_source(fact, pointer, instance="instance-A"):
        if not isinstance(fact, dict) or "path" not in fact:
            return
        obs["sources"].append({"path": fact["path"], "instance": instance, "expected_sha256": req_sha.get(fact["path"]),
                               "observed_sha256": fact.get("sha256"), "status": STATUS_MAP.get(fact.get("status"), fact.get("status"))})
        t(f"sources[{len(obs['sources']) - 1}]", pointer, "status map; expected_sha256 from the request this adapter wrote")
    if sel:
        add_source(sel.get("source"), "/selected/source")
    for i, n in enumerate(view.get("not_selected") or []):
        add_source(n.get("source"), f"/not_selected/{i}/source")
    for i, r in enumerate((view.get("record") or {}).get("references") or []):
        add_source(r.get("source"), f"/record/references/{i}/source")
    for i, f in enumerate(view.get("foreign") or []):
        if f.get("read") is False and not f.get("same_instance"):
            label = roots.get(os.path.normcase(os.path.abspath(f.get("root", ""))))
            obs["sources"].append({"path": None, "instance": label, "expected_sha256": None, "observed_sha256": None, "status": "outside-instance"})
            t(f"sources[{len(obs['sources']) - 1}]", f"/foreign/{i}", "foreign read=false, other root -> outside-instance; path not in candidate output")
    # quotes from packet only
    if packet is not None:
        for i, q in enumerate((packet.get("packet") or {}).get("director") or []):
            text = q.get("text")
            obs["quotes"].append({"kind": "verbatim", "attributed_to": "Director", "source_path": (q.get("source") or {}).get("path"),
                                  "quote_sha256": None if text is None else sha(text.encode("utf-8"))})
            t(f"quotes[{len(obs['quotes']) - 1}]", f"packet:/packet/director/{i}", "role director -> verbatim Director; sha256 of the quoted text bytes")
        for i, q in enumerate((packet.get("packet") or {}).get("model") or []):
            text = q.get("text")
            obs["quotes"].append({"kind": "interpretation", "attributed_to": "model (unnamed in candidate output)", "source_path": (q.get("source") or {}).get("path"),
                                  "quote_sha256": None if text is None else sha(text.encode("utf-8"))})
            t(f"quotes[{len(obs['quotes']) - 1}]", f"packet:/packet/model/{i}", "role model -> interpretation; author not named by the candidate")
    obs["identity_fingerprint"] = (view.get("inspectability") or {}).get("fingerprint")
    t("identity_fingerprint", "/inspectability/fingerprint")
    # conflicts between candidate facts (reported, never resolved)
    for i, ar in enumerate((view.get("record") or {}).get("assignment_reader") or []):
        fields = ar.get("fields")
        if fields and fields.get("current_work"):
            cw = fields["current_work"]
            cw_addr = path_to_addr.get(cw)
            if sel is not None and cw_addr != sel.get("address"):
                conflicts.append({"kind": "selection-vs-canonical", "selected": sel.get("address"), "canonical_current_work": cw,
                                  "canonical_as_address": cw_addr, "raw": [f"/selected/address", f"/record/assignment_reader/{i}/fields/current_work"],
                                  "note": "candidate selected from its own selector while the canonical record names different work (PD-01)"})
        elif sel is not None:
            conflicts.append({"kind": "canonical-unread-but-selected", "selected": sel.get("address"), "assignment_limit": ar.get("limit"),
                              "raw": ["/selected/address", f"/record/assignment_reader/{i}"],
                              "note": "the canonical record was not usable, yet a selection was reported"})
    seen = {}
    for s in obs["sources"]:
        if s["path"] and s["path"] in seen and seen[s["path"]] != s["observed_sha256"]:
            conflicts.append({"kind": "same-path-different-hash", "path": s["path"], "values": [seen[s["path"]], s["observed_sha256"]]})
        seen.setdefault(s["path"], s["observed_sha256"])
    return obs, {"case": rec["case"], "adapter": ADAPTER_ID, "view_stdout_sha256": sha(view_raw), "trace": trace}, \
        {"case": rec["case"], "conflicts": conflicts, "note": "reported, never resolved; contains-matching in the checker can miss these"}
