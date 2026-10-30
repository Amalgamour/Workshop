"""Prime read-record-read cycle over one registered work book (0515.prime-cycle/05.01). Standard library only.

  python -B prime_cycle.py read     --registration ABS [--json] [--templates DIR]
  python -B prime_cycle.py record   --registration ABS --decision ABS
  python -B prime_cycle.py inspect  --registration ABS --work ID
  python -B prime_cycle.py packet   --registration ABS --work ID --out DIR

Contract: 00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/CONTRACT.md. Compute gathers evidence through the
pinned reader (which runs the pinned inspector), validates Prime's supplied judgment through the pinned prime_review, writes
one work-local review record with a completion marker, and derives the next view from those records. Prime supplies the
judgment. Nothing here authenticates an actor, grants authority, elects work or dispatches anything.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = Path(__file__).resolve().parent.parent
PINS = {
    "batch_observe": ("batch-observation-pass01/batch_observe.py", "8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4"),
    "return_inspect": ("return-capture-pass01/return_inspect.py", "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"),
    "return_capture": ("return-capture-pass01/return_capture.py", "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"),
    "prime_review": ("prime-review-pass01/prime_review.py", "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"),
    "review_packet": ("review-packet-pass01/review_packet.py", "f658cbe48a3a76b908e5af0bcf0b7a68abc90571d983ca785e36667268f6ee72"),
}
AUTHORITY = "none; this tool records supplied judgment and derives a view; it authenticates no actor and grants no work"
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
PASS = re.compile(r"^05\.\d\d$")
MEMBER = re.compile(r"^01\d\d\.[a-z0-9][a-z0-9.-]*$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_DOC = 262144
CAPS = {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152}
REVIEW_FILES = ("record.json", "REVIEW.md", "COMMITTED.json")
DECISION_KEYS = {"schema", "review_id", "supersedes", "recovers", "binding", "attribution", "judgment"}
JUDGMENT_KEYS = {"outcome", "disposition", "pass_terminal", "goal", "finding", "reasons", "source_refs", "next_action",
                 "unresolved", "semantic_conflict", "design_fork", "holds", "answers", "sections"}
SECTION_KEYS = ["return_result", "prime_finding", "within_direction", "next_bounded_action", "for_model", "issue",
                "consequences", "options", "recommendation", "question", "affected", "proposed_plan", "exploration",
                "assumptions", "open_questions", "outcome_evidence", "limits", "tests_note", "tests_passed", "learning",
                "preservation", "remaining_choices", "findings_account", "finish_assessments"]


class Refusal(Exception):
    pass


class PartialWrite(Exception):
    pass


def need(cond, message):
    if not cond:
        raise Refusal(message)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical(v) -> bytes:
    return (json.dumps(v, sort_keys=True, indent=1, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


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


def m(rx, v) -> bool:
    return isinstance(v, str) and rx.fullmatch(v) is not None


def exact(obj, keys, where):
    need(isinstance(obj, dict) and set(obj) == set(keys), f"{where} must have exactly {sorted(keys)}")


# ---------- paths ----------

def is_link(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool((getattr(st, "st_file_attributes", 0) or 0) & 0x400)


def abs_path(text, where) -> Path:
    need(isinstance(text, str) and os.path.isabs(text) and not text.startswith(("\\\\", "//")), f"{where} must be an absolute local path")
    p = Path(os.path.abspath(text))
    for anc in [p, *p.parents]:
        need(not is_link(anc), f"{where} passes through a link: {anc}")
    return p


def rel_ok(text) -> bool:
    if not isinstance(text, str) or not text or "\\" in text or ":" in text or text.startswith("/"):
        return False
    return all(part not in ("", ".", "..") for part in text.split("/"))


def read_bounded(p: Path, limit: int, where: str) -> bytes:
    need(p.is_file() and not is_link(p), f"{where} must be a regular file")
    need(p.stat().st_size <= limit, f"{where} is over the {limit}-byte bound")
    return p.read_bytes()


def pin_path(name: str) -> Path:
    rel, digest = PINS[name]
    p = LABS / rel
    got = sha(p.read_bytes()) if p.is_file() and not is_link(p) else None
    need(got == digest, f"{name} at {p} is not the pinned code (sha256 {got}); nothing was launched")
    return p


def run(name: str, args: list[str], timeout=300) -> subprocess.CompletedProcess:
    for dep in (["batch_observe", "return_inspect", "return_capture"] if name == "batch_observe" else
                ["review_packet", "return_inspect", "return_capture"] if name == "review_packet" else [name]):
        pin_path(dep)
    return subprocess.run([sys.executable, "-B", str(pin_path(name)), *args], capture_output=True, timeout=timeout,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))


# ---------- registration ----------

def load_registration(path: Path) -> dict:
    reg = strict_json(read_bounded(path, MAX_DOC, "registration"), "registration")
    exact(reg, {"schema", "repository", "book", "book_label", "source", "members_book", "output_root", "bounds", "works"}, "registration")
    need(reg["schema"] == "prime-cycle-registration/1", "registration: unsupported schema")
    repo = abs_path(reg["repository"], "repository")
    need(repo.is_dir(), "repository must be a directory")
    need(rel_ok(reg["book"]), "book must be a relative path")
    need(m(LABEL, reg["book_label"]) and reg["book"].split("/")[-1] == reg["book_label"], "book_label must equal the book's last segment")
    src = reg["source"]
    exact(src, {"kind", "commit"}, "source")
    need((src["kind"] == "git-blob" and m(HEX40, src["commit"])) or (src["kind"] == "live-file" and src["commit"] is None),
         "source must be git-blob with a 40-hex commit, or live-file with commit null")
    if reg["members_book"] is not None:
        abs_path(reg["members_book"], "members_book")
    out = abs_path(reg["output_root"], "output_root")
    b = reg["bounds"]
    exact(b, set(CAPS), "bounds")
    for k, cap in CAPS.items():
        need(type(b[k]) is int and 1 <= b[k] <= cap, f"bounds.{k} must be an integer 1..{cap}")
    need(isinstance(reg["works"], list) and 1 <= len(reg["works"]) <= b["max_works"], "works must be a list within max_works")
    ids = set()
    for i, w in enumerate(reg["works"]):
        wh = f"works[{i}]"
        exact(w, {"work_id", "page", "pass", "member", "goal", "agreement", "review_location"}, wh)
        need(m(LABEL, w["work_id"]) and w["work_id"] not in ids, f"{wh}.work_id must be a unique label")
        ids.add(w["work_id"])
        need(m(PASS, w["pass"]), f"{wh}.pass must be 05.NN")
        need(rel_ok(w["page"]) and w["page"].startswith(reg["book"] + "/") and w["page"].endswith("/" + w["pass"] + ".md")
             and len(w["page"][len(reg["book"]) + 1:].split("/")) == 2, f"{wh}.page must be <book>/<lane>/<pass>.md")
        need(w["member"] is None or m(MEMBER, w["member"]), f"{wh}.member must be null or a member name")
        exact(w["goal"], {"goal_id", "statement"}, f"{wh}.goal")
        need(m(LABEL, w["goal"]["goal_id"]) and isinstance(w["goal"]["statement"], str) and w["goal"]["statement"].strip()
             and len(w["goal"]["statement"]) <= 4000, f"{wh}.goal must be {{goal_id label, statement text}}")
        need(isinstance(w["agreement"], dict), f"{wh}.agreement must be an object (prime-review agreement)")
        lane_dir = w["page"].rsplit("/", 1)[0]
        need(rel_ok(w["review_location"]) and w["review_location"].startswith(lane_dir + "/evidence/"),
             f"{wh}.review_location must lie under {lane_dir}/evidence/ (work-local)")
        rl = repo / w["review_location"]
        need(not str(out).lower().startswith(str(rl).lower()) and not str(rl).lower().startswith(str(out).lower()),
             f"{wh}: output_root and review_location must not contain one another")
    return reg


def goal_sha(w) -> str:
    return sha(w["goal"]["statement"].encode("utf-8"))


# ---------- observation ----------

def observe(reg, w) -> dict:
    args = ["observe", "--json", "--repo", reg["repository"]]
    args += ["--commit", reg["source"]["commit"]] if reg["source"]["kind"] == "git-blob" else ["--live"]
    args += ["--path", w["page"]]
    if reg["members_book"] is not None:
        args += ["--members-book", reg["members_book"]]
    p = run("batch_observe", args)
    rec = {"exit": p.returncode, "stdout_sha256": sha(p.stdout), "stderr": p.stderr.decode("utf-8", "replace")[:2000]}
    if p.returncode not in (0, 1) or len(p.stdout) > reg["bounds"]["max_output_bytes"]:
        return dict(rec, failed=f"reader exit {p.returncode}")
    try:
        o = strict_json(p.stdout, "reader report")
    except Refusal as exc:
        return dict(rec, failed=str(exc))
    src, page = o.get("source") or {}, o.get("page")
    if not isinstance(src, dict) or not m(HEX64, src.get("sha256")) or type(src.get("bytes")) is not int:
        return dict(rec, failed="reader report lacks a usable source identity")
    if src["bytes"] > reg["bounds"]["max_page_bytes"]:
        return dict(rec, failed="page is over max_page_bytes")
    cu = o.get("custody") if isinstance(o.get("custody"), dict) else {}
    members = []
    for x in cu.get("observations") or []:
        ins = x.get("inspection") if isinstance(x.get("inspection"), dict) else None
        cap = (ins or {}).get("capture") if isinstance((ins or {}).get("capture"), dict) else None
        members.append({"member": x.get("member"), "role": x.get("role"), "status": (ins or {}).get("status"),
                        "submission_id": (cap or {}).get("submission_id"),
                        "receipt_sha256": (cap or {}).get("receipt_sha256"), "origin": (cap or {}).get("origin"),
                        "retrospective": (cap or {}).get("retrospective")})
    review = o.get("review") if isinstance(o.get("review"), dict) else {}
    return dict(rec, failed=None, page=page, source={k: src.get(k) for k in ("kind", "commit", "path", "sha256", "bytes", "live_observed_at")},
                primary=cu.get("primary"), members=members, review_text=review.get("text_raw"),
                ambiguities=o.get("ambiguities") or [], attention=o.get("attention") or [])


def current_binding(reg, w, obs, prior) -> dict:
    """The mechanical fields of a decision template; the fingerprint binds them."""
    want = w["member"]
    pick = None
    if obs.get("failed") is None:
        named = [x for x in obs["members"] if x["member"] == (want or obs["primary"])]
        pick = named[0] if named else None
    primary_ok = bool(pick and pick["role"] == "primary-current-candidate" and pick["status"] == "complete")
    b = {"work_id": w["work_id"], "page": w["page"], "pass": w["pass"],
         "source": {"kind": reg["source"]["kind"], "commit": reg["source"]["commit"],
                    "page_sha256": None if obs.get("failed") else obs["source"]["sha256"],
                    "page_bytes": None if obs.get("failed") else obs["source"]["bytes"]},
         "member": pick["member"] if pick else want, "member_role": pick["role"] if pick else None,
         "receipt_sha256": pick["receipt_sha256"] if primary_ok else None,
         "submission_id": pick["submission_id"] if primary_ok else None,
         "origin": pick["origin"] if primary_ok else None, "retrospective": pick["retrospective"] if pick else None,
         "goal": {"goal_id": w["goal"]["goal_id"], "goal_sha256": goal_sha(w)},
         "expected_prior": prior}
    b["fingerprint"] = sha(canonical(b))
    return b


# ---------- review records ----------

def review_dir(reg, w) -> Path:
    return Path(reg["repository"]) / w["review_location"]


def scan_reviews(reg, w) -> dict:
    root = review_dir(reg, w)
    out = {"committed": {}, "partial": [], "invalid": []}
    if not root.exists():
        return out
    need(root.is_dir() and not is_link(root), f"review location {root} must be a plain directory")
    for d in sorted(p for p in root.iterdir()):
        if not d.is_dir() or is_link(d) or not m(LABEL, d.name):
            out["invalid"].append({"review_id": d.name, "phase": "invalid", "reason": "not a plain review directory"})
            continue
        files = {n: (d / n) for n in REVIEW_FILES}
        if not files["COMMITTED.json"].is_file():
            out["partial"].append({"review_id": d.name, "phase": "partial-no-marker",
                                   "present": sorted(p.name for p in d.iterdir())})
            continue
        try:
            marker = strict_json(read_bounded(files["COMMITTED.json"], MAX_DOC, "marker"), "marker")
            rb = read_bounded(files["record.json"], MAX_DOC, "record")
            mb = read_bounded(files["REVIEW.md"], MAX_DOC, "REVIEW.md")
        except (Refusal, OSError) as exc:
            out["partial"].append({"review_id": d.name, "phase": "partial-marker-mismatch", "reason": str(exc)})
            continue
        if not isinstance(marker, dict) or marker.get("record_sha256") != sha(rb) or marker.get("review_md_sha256") != sha(mb):
            out["partial"].append({"review_id": d.name, "phase": "partial-marker-mismatch", "reason": "marker hashes do not match the files"})
            continue
        try:
            rec = strict_json(rb, "record")
            need(isinstance(rec, dict) and rec.get("schema") == "prime-cycle-review/1", "unknown record schema")
        except Refusal as exc:
            out["invalid"].append({"review_id": d.name, "phase": "invalid", "reason": str(exc)})
            continue
        out["committed"][d.name] = {"record": rec, "record_sha256": sha(rb), "dir": str(d)}
    return out


def latest(scan) -> tuple[list, list]:
    """Heads of the committed lineage: committed reviews no other committed review supersedes."""
    superseded = {r["record"]["decision"]["supersedes"]["review_id"] for r in scan["committed"].values()
                  if r["record"]["decision"]["supersedes"]}
    heads = [rid for rid in scan["committed"] if rid not in superseded]
    return heads, sorted(superseded)


def prior_of(scan):
    heads, _ = latest(scan)
    if len(heads) != 1:
        return None if not heads else "fork"
    h = heads[0]
    return {"review_id": h, "record_sha256": scan["committed"][h]["record_sha256"]}


# ---------- read ----------

def derive(reg, w, obs, scan) -> dict:
    heads, _ = latest(scan)
    attention = []
    prior = prior_of(scan)
    if prior == "fork":
        attention.append(f"lineage-fork: {len(heads)} committed heads; no head is chosen")
        prior_value = None
    else:
        prior_value = prior
    binding = current_binding(reg, w, obs, prior_value)
    item = {"work_id": w["work_id"], "page": w["page"], "pass": w["pass"],
            "source": {"kind": reg["source"]["kind"], "commit": reg["source"]["commit"],
                       "page_sha256": binding["source"]["page_sha256"]},
            "reader": {"exit": obs["exit"], "stdout_sha256": obs["stdout_sha256"], "failed": obs.get("failed"),
                       "ambiguities": obs.get("ambiguities", []), "attention": obs.get("attention", [])},
            "custody": {"member": binding["member"], "role": binding["member_role"], "receipt_sha256": binding["receipt_sha256"],
                        "retrospective": binding["retrospective"], "basis": "live inspection at read time; custody is not acceptance"},
            "reviews": {"committed": sorted(scan["committed"]), "partial": scan["partial"], "invalid": scan["invalid"], "heads": heads},
            "goal": {"goal_id": w["goal"]["goal_id"], "goal_sha256": goal_sha(w)}}
    if obs.get("failed"):
        attention.append(f"observation-failed: {obs['failed']}")
    for p in scan["partial"]:
        attention.append(f"partial review {p['review_id']} ({p['phase']}); see inspect; recover with a new review_id")
    for p in scan["invalid"]:
        attention.append(f"invalid review directory {p['review_id']}: {p['reason']}")
    head = scan["committed"][heads[0]] if len(heads) == 1 else None
    if binding["receipt_sha256"] is None:
        pass_state = "no-return"
    elif head is None:
        pass_state = "awaiting-review"
    else:
        hb = head["record"]["decision"]["binding"]
        same = (hb["source"]["page_sha256"], hb["receipt_sha256"]) == (binding["source"]["page_sha256"], binding["receipt_sha256"])
        pass_state = "reviewed" if same else "review-stale"
        if not same:
            attention.append("review-stale: the latest review binds a different page or receipt; re-review required")
    if head is None and (obs.get("review_text") or "").strip() not in ("", "PENDING."):  # exact-literal PENDING is not a review
        attention.append("legacy-review-unmapped: the page has review prose and no recorded cycle review; adopt only by an attributed review")
        item["legacy_review_text"] = obs["review_text"]
    if head:
        j = head["record"]["decision"]["judgment"]
        g = j["goal"]
        same_goal = (g["goal_id"], g["goal_sha256"]) == (w["goal"]["goal_id"], goal_sha(w))
        if g["terminal"] == "completed" and same_goal:
            goal_terminal = "completed"
        elif g["terminal"] == "completed":
            goal_terminal = f"open (prior completion bound to goal {g['goal_id']} {g['goal_sha256'][:12]})"
        else:
            goal_terminal = "open"
        rep = head["record"]["report"]
        item.update(latest_review={"review_id": heads[0], "record_sha256": head["record_sha256"],
                                   "author": head["record"]["decision"]["attribution"]["actor_label"],
                                   "outcome": j["outcome"], "effective": rep["effective"]},
                    disposition=j["disposition"], pass_terminal=j["pass_terminal"], goal_terminal=goal_terminal,
                    holds=rep["holds"], next_action=(dict(j["next_action"], author=head["record"]["decision"]["attribution"]["actor_label"],
                                                          source=f"{w['review_location']}/{heads[0]}/record.json",
                                                          record_sha256=head["record_sha256"]) if j["next_action"] else None),
                    unresolved=j["unresolved"])
        if any(h["status"] != "reply-bound" for h in rep["holds"]):
            attention.append("hold open: " + ", ".join(f"{h['hold_id']} ({h['status']}) blocks {h['dependent_scope']}" for h in rep["holds"]))
    else:
        item.update(latest_review=None, disposition="unknown", pass_terminal="unknown", goal_terminal="unknown", holds=[],
                    next_action=None, unresolved=[])
        if pass_state == "awaiting-review":
            attention.append("awaiting-review: a captured return has no recorded review")
    item["pass_state"] = pass_state
    item["attention"] = attention
    tmpl_judgment = {k: None for k in JUDGMENT_KEYS}
    tmpl_judgment.update(goal={"terminal": None, "goal_id": w["goal"]["goal_id"], "goal_sha256": goal_sha(w), "evidence": []},
                         reasons=[], source_refs=[], unresolved=[], holds=[], answers=[], sections={k: None for k in SECTION_KEYS})
    n = len(scan["committed"]) + len(scan["partial"]) + len(scan["invalid"]) + 1
    item["template"] = {"schema": "prime-cycle-decision/1", "review_id": f"{w['pass']}-r{n}",
                        "supersedes": prior_value, "recovers": None, "binding": binding,
                        "attribution": {"actor_label": None, "role": "prime", "evidence": None}, "judgment": tmpl_judgment}
    return item


def guard_actions(reg, items, scans) -> None:
    """Each recorded next action checked by prime_review check-next against every other work's latest holds."""
    for it in items:
        na = it.get("next_action")
        it["next_action_guard"] = []
        if not na or not na.get("action_id"):
            continue
        for other, scan in zip(items, scans):
            heads, _ = latest(scan)
            if len(heads) != 1:
                continue
            rec = scan["committed"][heads[0]]["record"]
            if not rec["report"]["holds"]:
                continue
            review = json.loads(json.dumps(rec["prime_review_input"]))
            for src in review["sources"]:
                src["bind"] = False  # hold evaluation needs the recorded identities, not a re-read of changed bytes
            doc = {"schema": "prime-review-guard/1", "review": review,
                   "proposed_action": {"action_id": na["action_id"], "label": na["action_id"],
                                       "grant_ref": f"recorded next action of {it['work_id']}", "authorized_in_grant": na.get("authorized_in_grant")}}
            with tempfile.TemporaryDirectory(prefix="pcycle-") as t:
                f = Path(t) / "guard.json"
                f.write_bytes(canonical(doc))
                p = run("prime_review", ["check-next", "--input", str(f), "--json"])
            try:
                res = json.loads(p.stdout)["result"]
            except (ValueError, KeyError, TypeError):
                res = f"guard-failed (exit {p.returncode})"
            it["next_action_guard"].append({"against_work": other["work_id"], "review_id": heads[0], "result": res, "exit": p.returncode})
            if res not in ("independent-of-holds",):
                it["attention"].append(f"next action {na['action_id']} is {res} by holds in {other['work_id']}")


def read(reg_path: Path, templates: Path | None = None) -> dict:
    reg = load_registration(reg_path)
    items, scans = [], []
    for w in reg["works"]:
        obs = observe(reg, w)
        scan = scan_reviews(reg, w)
        items.append(derive(reg, w, obs, scan))
        scans.append(scan)
    guard_actions(reg, items, scans)
    view = {"schema": "prime-cycle-view/1", "registration_sha256": sha(reg_path.read_bytes()), "book": reg["book"],
            "source": reg["source"], "works": items, "elected": None,
            "attention_count": sum(len(i["attention"]) for i in items), "authority": AUTHORITY,
            "note": "derived from work-local review records and fresh reader observations; noncanonical; rebuildable"}
    out = canonical(view)
    need(len(out) <= reg["bounds"]["max_output_bytes"], "view is over max_output_bytes")
    if templates is not None:
        root = abs_path(str(templates), "--templates")
        need(str(root).lower().startswith(str(Path(reg["output_root"])).lower()), "--templates must be under output_root")
        root.mkdir(parents=False, exist_ok=True)
        for it in items:
            with open(root / f"template-{it['work_id']}.json", "xb") as h:
                h.write(canonical(it["template"]))
    return view


def view_text(v: dict) -> str:
    out = [f"Prime cycle view  book {v['book']}  source {v['source']['kind']} {v['source']['commit'] or '(live files)'}",
           "Derived from work-local review records. Noncanonical. Nothing is elected or dispatched.", ""]
    for it in v["works"]:
        out.append(f"{it['work_id']}  {it['page']}")
        out.append(f"  pass state: {it['pass_state']}   review disposition: {it['disposition']}   pass terminal: {it['pass_terminal']}")
        out.append(f"  goal {it['goal']['goal_id']}: {it['goal_terminal']}")
        c = it["custody"]
        out.append(f"  custody: {c['member']} role {c['role']} receipt {(c['receipt_sha256'] or 'none')[:16]} (custody is not acceptance)")
        if it["latest_review"]:
            lr = it["latest_review"]
            out.append(f"  latest review: {lr['review_id']} by {lr['author']} outcome {lr['outcome']} (prime_review effective {lr['effective']})")
        for h in it["holds"]:
            out.append(f"  hold {h['hold_id']} {h['status']}: blocks {', '.join(h['dependent_scope']) or 'nothing'}")
        if it["next_action"]:
            na = it["next_action"]
            out.append(f"  recorded next action ({na['author']}, {na['source']}): {na['action_id']}: {na['text']}")
            for g in it.get("next_action_guard", []):
                out.append(f"    holds in {g['against_work']}: {g['result']}")
        for u in it["unresolved"]:
            out.append(f"  unresolved: {u}")
        for a in it["attention"]:
            out.append(f"  ! {a}")
        out.append("")
    out.append(f"authority {AUTHORITY}")
    return "\n".join(out) + "\n"


# ---------- record ----------

def check_judgment(j, w) -> None:
    exact(j, JUDGMENT_KEYS, "judgment")
    need(j["outcome"] in ("continue", "director-input", "develop", "complete"), "judgment.outcome must be continue, director-input, develop or complete")
    need(j["disposition"] in ("accepted", "held", "correction-required"), "judgment.disposition must be accepted, held or correction-required")
    need(j["pass_terminal"] in ("finished", "open"), "judgment.pass_terminal must be finished or open")
    g = j["goal"]
    exact(g, {"terminal", "goal_id", "goal_sha256", "evidence"}, "judgment.goal")
    need(g["terminal"] in ("open", "completed"), "judgment.goal.terminal must be open or completed")
    need((g["goal_id"], g["goal_sha256"]) == (w["goal"]["goal_id"], goal_sha(w)),
         "judgment.goal must name the registration's current goal_id and goal_sha256")
    need(isinstance(g["evidence"], list) and all(isinstance(x, str) and x.strip() for x in g["evidence"]), "judgment.goal.evidence must be a list of strings")
    for k in ("reasons", "source_refs", "unresolved"):
        need(isinstance(j[k], list) and all(isinstance(x, str) and x.strip() for x in j[k]), f"judgment.{k} must be a list of strings")
    need(isinstance(j["finding"], str) and j["finding"].strip(), "judgment.finding must be text")
    na = j["next_action"]
    if na is not None:
        exact(na, {"action_id", "text", "authorized_in_grant"}, "judgment.next_action")
        need(m(LABEL, na["action_id"]) and isinstance(na["text"], str) and na["text"].strip()
             and na["authorized_in_grant"] in (True, False, None), "judgment.next_action has a wrong value")
    # terminal rules (CONTRACT §6)
    need((j["outcome"] == "complete") == (g["terminal"] == "completed"), "outcome complete if and only if goal.terminal completed")
    if g["terminal"] == "completed":
        need(j["disposition"] == "accepted" and j["pass_terminal"] == "finished", "a completed goal needs disposition accepted and pass finished")
        need(g["evidence"], "a completed goal needs at least one evidence reference")
    if j["disposition"] in ("held", "correction-required"):
        need(j["pass_terminal"] == "open" and g["terminal"] == "open", f"a {j['disposition']} review keeps the pass and the goal open")
    if j["outcome"] == "director-input":
        need(j["disposition"] == "held", "director-input requires disposition held")


def prime_review_record(reg, w, d, binding) -> dict:
    j = d["judgment"]
    page_source = {"kind": "page", "logical_path": w["page"], "content_sha256": binding["source"]["page_sha256"],
                   "content_bytes": binding["source"]["page_bytes"], "transport_sha256": binding["source"]["page_sha256"],
                   "transport_bytes": binding["source"]["page_bytes"], "prior_content_sha256": None, "prior_transport_sha256": None,
                   "record": None, "bind": reg["source"]["kind"] == "live-file", "identity": {"schema": "page-bytes/1"}}
    sources = [page_source]
    if binding["receipt_sha256"]:
        rb = (Path(reg["members_book"]) / binding["member"] / "receipt.json").read_bytes() if reg["members_book"] else b""
        need(sha(rb) == binding["receipt_sha256"], "receipt bytes no longer match the bound receipt")
        sources.append({"kind": "capture", "logical_path": f"{binding['member']}/receipt.json", "content_sha256": binding["receipt_sha256"],
                        "content_bytes": len(rb), "transport_sha256": binding["receipt_sha256"], "transport_bytes": len(rb),
                        "prior_content_sha256": None, "prior_transport_sha256": None, "record": None, "bind": False,
                        "identity": {"schema": "return-capture/1", "member": binding["member"],
                                     "submission_id": binding["submission_id"],
                                     "receipt_sha256": binding["receipt_sha256"], "origin": binding["origin"]}})
    return {"schema": "prime-review-record/1", "attribution": d["attribution"], "sources": sources, "agreement": w["agreement"],
            "judgment": {"outcome": j["outcome"], "finding": j["finding"], "reasons": j["reasons"], "semantic_conflict": j["semantic_conflict"],
                         "design_fork": j["design_fork"], "next_action": j["next_action"]["text"] if j["next_action"] else None,
                         "sections": j["sections"]},
            "holds": j["holds"], "answers": j["answers"], "review_passes": [], "gaps": j["unresolved"]}


def write_file(path: Path, data: bytes) -> None:
    """Exclusive create; a hook point for interruption tests."""
    with open(path, "xb") as h:
        h.write(data)
        h.flush()
        os.fsync(h.fileno())


def record(reg_path: Path, decision_path: Path) -> tuple[int, str]:
    reg = load_registration(reg_path)
    d = strict_json(read_bounded(decision_path, MAX_DOC, "decision"), "decision")
    exact(d, DECISION_KEYS, "decision")
    need(d["schema"] == "prime-cycle-decision/1", "decision: unsupported schema")
    need(m(LABEL, d["review_id"]), "review_id must be a label")
    exact(d["attribution"], {"actor_label", "role", "evidence"}, "attribution")
    need(isinstance(d["attribution"]["actor_label"], str) and d["attribution"]["actor_label"].strip(), "attribution.actor_label is required")
    b = d["binding"]
    need(isinstance(b, dict) and isinstance(b.get("work_id"), str), "binding must name a work_id")
    w = next((x for x in reg["works"] if x["work_id"] == b["work_id"]), None)
    need(w is not None, f"work {b.get('work_id')} is not registered")
    check_judgment(d["judgment"], w)
    rdir = review_dir(reg, w)
    lane_evidence = Path(reg["repository"]) / w["page"].rsplit("/", 1)[0] / "evidence"
    need(lane_evidence.is_dir() and not is_link(lane_evidence), "the lane's evidence directory must exist as a plain directory")
    target = rdir / d["review_id"]
    scan = scan_reviews(reg, w)
    if target.exists() and d["review_id"] not in scan["committed"]:
        raise Refusal(f"partial review present at {target}; run inspect, then record under a new review_id with recovers")
    prior = prior_of(scan)
    need(prior != "fork", "lineage-fork: more than one committed head; record a successor of one head explicitly is not supported here")
    obs = observe(reg, w)
    need(obs.get("failed") is None, f"observation failed: {obs.get('failed')}")
    replay = target.exists()
    if not replay:  # the prior-state check comes first so a stale template gets the specific reason
        need(b.get("expected_prior") == prior, f"expected_prior {b.get('expected_prior')} does not equal the latest committed review {prior}")
    expected_now = current_binding(reg, w, obs, b.get("expected_prior"))
    diffs = [k for k in ("source", "member", "member_role", "receipt_sha256", "submission_id", "origin", "retrospective", "goal", "page", "pass")
             if expected_now.get(k) != b.get(k)]
    need(not diffs, "source changed since read: " + ", ".join(diffs))
    need(expected_now["fingerprint"] == b.get("fingerprint"), "binding fingerprint does not match the current observation")
    if not replay:
        if prior is not None:
            need(d["supersedes"] == prior, "a review over an existing one must set supersedes to that review")
        else:
            need(d["supersedes"] is None, "supersedes names a review that is not the latest committed review")
    if d["recovers"] is not None:
        need(any(p["review_id"] == d["recovers"] for p in scan["partial"]), "recovers must name a partial review directory")
    need(b["receipt_sha256"] is not None or d["judgment"]["disposition"] != "accepted",
         "an accepted review needs a bound captured return")
    pr = prime_review_record(reg, w, d, b)
    with tempfile.TemporaryDirectory(prefix="pcycle-") as t:
        f = Path(t) / "review.json"
        f.write_bytes(canonical(pr))
        args = ["report", "--input", str(f), "--json"] + (["--root", reg["repository"]] if reg["source"]["kind"] == "live-file" else [])
        p = run("prime_review", args)
    need(p.returncode in (0, 1), "prime_review refused the review: " + (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip()[:600])
    rep = json.loads(p.stdout)
    if d["judgment"]["goal"]["terminal"] == "completed":
        need(rep["effective"] == "complete-as-supplied", f"a completed goal needs prime_review effective complete-as-supplied (got {rep['effective']})")
    summary = {k: rep[k] for k in ("effective", "holds", "attention", "agreement_gaps", "permission", "markdown_sha256", "closes_work", "authority")}
    rec = {"schema": "prime-cycle-review/1", "work_id": w["work_id"], "review_id": d["review_id"], "decision": d,
           "observed_binding": expected_now, "prime_review_input": pr, "prime_review_input_sha256": sha(canonical(pr)),
           "report": summary, "report_exit": p.returncode,
           "tools": {k: v[1] for k, v in PINS.items()}, "tool": sha(Path(__file__).read_bytes()),
           "lineage": {"supersedes": d["supersedes"], "recovers": d["recovers"]},
           "note": "work-local authoritative review record; REVIEW.md is its readable projection; COMMITTED.json marks it usable"}
    rec_bytes = canonical(rec)
    if replay:
        old = (target / "record.json").read_bytes()
        need(old == rec_bytes, "conflict: a different review is already committed under this review_id; use a new review_id with supersedes")
        return 0, f"already-recorded {target}\n"
    j = d["judgment"]
    md = (f"# Prime cycle review {d['review_id']} — {w['work_id']}\n\n"
          f"Readable projection of `record.json` (sha256 {sha(rec_bytes)}). The record is authoritative; this file is not edited separately.\n\n"
          f"- page: `{w['page']}` at {reg['source']['kind']} {reg['source']['commit'] or '(live)'} sha256 {b['source']['page_sha256']}\n"
          f"- return: {b['member']} receipt {b['receipt_sha256']}\n"
          f"- review disposition: **{j['disposition']}**; pass terminal: **{j['pass_terminal']}**; "
          f"goal `{j['goal']['goal_id']}` terminal: **{j['goal']['terminal']}**\n"
          f"- prime_review effective: {rep['effective']}; closes_work {str(rep['closes_work']).lower()}; authority {rep['authority']}\n"
          f"- supersedes: {d['supersedes']}; recovers: {d['recovers']}\n\n---\n\n").encode("utf-8") + rep["markdown"].encode("utf-8")
    need(len(rec_bytes) + len(md) <= reg["bounds"]["max_output_bytes"], "review is over max_output_bytes")
    rdir.mkdir(parents=True, exist_ok=True)
    need(not is_link(rdir), "review location is a link")
    os.mkdir(target)
    try:
        write_file(target / "record.json", rec_bytes)
        write_file(target / "REVIEW.md", md)
        write_file(target / "COMMITTED.json", canonical({"record_sha256": sha(rec_bytes), "review_md_sha256": sha(md)}))
    except OSError as exc:
        raise PartialWrite(f"write failed in {target}: {type(exc).__name__}: {exc}; files so far are kept; use inspect") from None
    return (0 if p.returncode == 0 else 1), f"recorded {target}\nprime_review effective {rep['effective']}\n"


# ---------- inspect / packet ----------

def inspect(reg_path: Path, work_id: str) -> tuple[int, dict]:
    reg = load_registration(reg_path)
    w = next((x for x in reg["works"] if x["work_id"] == work_id), None)
    need(w is not None, f"work {work_id} is not registered")
    root = review_dir(reg, w)
    scan = scan_reviews(reg, w)
    rows = []
    if root.exists():
        for d in sorted(root.iterdir()):
            files = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(d.iterdir()) if p.is_file()} if d.is_dir() else {}
            phase = ("committed" if d.name in scan["committed"] else
                     next((p["phase"] for p in scan["partial"] + scan["invalid"] if p["review_id"] == d.name), "invalid"))
            rows.append({"review_id": d.name, "phase": phase, "files": files})
    out = {"schema": "prime-cycle-inspect/1", "work_id": work_id, "location": str(root), "reviews": rows,
           "recovery": "never edit or delete a partial; record again under a new review_id with recovers set to the partial id"}
    return (0 if all(r["phase"] == "committed" for r in rows) else 1), out


def packet(reg_path: Path, work_id: str, out_dir: str) -> tuple[int, str]:
    reg = load_registration(reg_path)
    w = next((x for x in reg["works"] if x["work_id"] == work_id), None)
    need(w is not None, f"work {work_id} is not registered")
    need(w["member"] and reg["members_book"], "packet needs a registered member and members_book")
    out = abs_path(out_dir, "--out")
    need(str(out).lower().startswith(str(Path(reg["output_root"])).lower()), "--out must be under output_root")
    rc = LABS / PINS["return_capture"][0]
    req = {"schema": "review-packet-request/1", "book": reg["members_book"], "member": w["member"],
           "origin": {"book": reg["book_label"], "page": w["page"].split("/")[-2], "pass": w["pass"]}, "repo": reg["repository"],
           "python": sys.executable, "inspector": str(LABS / PINS["return_inspect"][0]), "helper": str(rc), "output": str(out),
           "bounds": {"max_sources": 8, "max_source_bytes": 262144, "max_total_bytes": 1048576, "max_output_bytes": 2097152},
           "sources": [{"id": "return", "role": "builder-claim", "kind": "member-file", "name": "return.md"},
                       {"id": "receipt", "role": "custody", "kind": "member-file", "name": "receipt.json"}]
                      + ([{"id": "page", "role": "supporting", "kind": "git-blob", "commit": reg["source"]["commit"], "path": w["page"]}]
                         if reg["source"]["kind"] == "git-blob" else [])}
    with tempfile.TemporaryDirectory(prefix="pcycle-") as t:
        f = Path(t) / "packet-request.json"
        f.write_bytes(canonical(req))
        p = run("review_packet", ["assemble", "--request", str(f)])
    return (0 if p.returncode == 0 else 2), p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace", newline="\n")  # LF on every platform
    ap = argparse.ArgumentParser(prog="prime_cycle.py")
    sub = ap.add_subparsers(dest="command", required=True)
    r = sub.add_parser("read")
    r.add_argument("--registration", required=True)
    r.add_argument("--json", action="store_true")
    r.add_argument("--templates")
    rc = sub.add_parser("record")
    rc.add_argument("--registration", required=True)
    rc.add_argument("--decision", required=True)
    i = sub.add_parser("inspect")
    i.add_argument("--registration", required=True)
    i.add_argument("--work", required=True)
    pk = sub.add_parser("packet")
    pk.add_argument("--registration", required=True)
    pk.add_argument("--work", required=True)
    pk.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        reg = abs_path(a.registration, "--registration")
        if a.command == "read":
            v = read(reg, Path(a.templates) if a.templates else None)
            sys.stdout.write(canonical(v).decode("utf-8") if a.json else view_text(v))
            return 1 if v["attention_count"] else 0
        if a.command == "record":
            code, text = record(reg, abs_path(a.decision, "--decision"))
            sys.stdout.write(text)
            return code
        if a.command == "inspect":
            code, out = inspect(reg, a.work)
            sys.stdout.write(canonical(out).decode("utf-8"))
            return code
        code, text = packet(reg, a.work, a.out)
        sys.stdout.write(text)
        return code
    except PartialWrite as exc:
        sys.stdout.write(f"partial: {exc}\n")
        return 3
    except Refusal as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except (OSError, subprocess.SubprocessError) as exc:
        sys.stdout.write(f"refused: {type(exc).__name__}: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
