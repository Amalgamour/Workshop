"""Prime read-record-read cycle over one registered work book (0515.prime-cycle/05.01, corrected in 05.02 and 05.03). Standard library only.

  python -B prime_cycle.py read     --registration ABS [--json] [--templates DIR]   [JOURNAL]
  python -B prime_cycle.py record   --registration ABS --decision ABS               [JOURNAL]
  python -B prime_cycle.py inspect  --registration ABS --work ID                    [JOURNAL]
  python -B prime_cycle.py packet   --registration ABS --work ID --out DIR          [JOURNAL]
  python -B prime_cycle.py day      --journal-root ABS [--date YYYY-MM-DD] [--registration ABS] [--json]
  JOURNAL = --journal-root ABS [--caller TEXT] [--note TEXT]

Contracts: 0515.prime-cycle/evidence/build05.01/CONTRACT.md and its deltas build05.02 and build05.03/CONTRACT.md. Compute gathers evidence
through the pinned reader (which runs the pinned inspector), validates Prime's supplied judgment through the pinned
prime_review, writes one work-local review record with a completion marker, and derives the next view from those records.
A review's declarations are current only while its binding (page, custody, direction) still holds; otherwise they are shown
as historical. A failed observation is never shown as absent custody (no-return) or as stale; its reader diagnostic is
kept, bounded, with the full child output retained under the journal. An explicit journal root logs each operation as start/end events. Prime supplies the judgment. Nothing here
authenticates an actor, grants authority, elects work or dispatches anything.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
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
DIRECTION_FIELDS = ("goal", "scope", "prime_discretion", "director_required", "finish_criteria", "recorded_decisions")
RECORD_SCHEMAS = ("prime-cycle-review/1", "prime-cycle-review/2")  # /1 is legacy: read, kept, never current (05.02 C04)
CURRENT_KEYS = ("member", "member_role", "receipt_sha256", "submission_id", "origin", "retrospective", "direction")
MAX_STDOUT_SNAPSHOT = 2097152
JSON_EXCERPT = 2000   # characters of child diagnostic kept in JSON views (05.03 §1)
TEXT_EXCERPT = 240    # characters on one line in text views
ABSENT_ROLES = {"missing", "reserved", "origin-mismatch", "cross-book-origin", "secondary-historical", "same-page-retrospective"}
MAX_DAY_OPS = 5000
DATE = re.compile(r"^\d{4}-\d\d-\d\d$")


class Refusal(Exception):
    pass


class PartialWrite(Exception):
    def __init__(self, message, target=None):
        super().__init__(message)
        self.target = target


class JournalError(Exception):
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

def one_line(text: str, limit: int = TEXT_EXCERPT) -> str:
    """A bounded single-line rendering of child output for text views: control characters escaped, never unbounded."""
    out = []
    for ch in text.strip():
        out.append({"\n": "\\n", "\r": "\\r", "\t": "\\t"}.get(ch) or (f"\\x{ord(ch):02x}" if ord(ch) < 32 or ord(ch) == 127 else ch))
    s = "".join(out).strip()
    return s if len(s) <= limit else s[:limit - 12] + "…[truncated]"


def reader_diagnostic(w, p, reason: str, retain) -> dict:
    """Bounded diagnostic for a failed reader call, with the full child output retained when a journal is given (05.03 §1)."""
    err = p.stderr.decode("utf-8", "replace")
    text = err if err.strip() else reason
    diag = {"source": "batch_observe stderr" if err.strip() else "prime_cycle reason (reader stderr was empty)",
            "reader_exit": p.returncode, "stderr_sha256": sha(p.stderr), "stderr_bytes": len(p.stderr),
            "stdout_sha256": sha(p.stdout), "stdout_bytes": len(p.stdout),
            "excerpt": text if len(text) <= JSON_EXCERPT else text[:JSON_EXCERPT] + "…[truncated]",
            "retained": None, "retained_note": "not retained: no --journal-root on this operation"}
    if retain is not None:
        try:
            diag["retained"] = {"stdout": retain(f"reader-{w['work_id']}-stdout.txt", p.stdout),
                                "stderr": retain(f"reader-{w['work_id']}-stderr.txt", p.stderr)}
            diag["retained_note"] = "full child output retained in this operation's journal folder"
        except (OSError, JournalError) as exc:
            diag["retained_note"] = f"retention failed: {type(exc).__name__}: {exc}"
    return diag


def observe(reg, w, retain=None) -> dict:
    args = ["observe", "--json", "--repo", reg["repository"]]
    args += ["--commit", reg["source"]["commit"]] if reg["source"]["kind"] == "git-blob" else ["--live"]
    args += ["--path", w["page"]]
    if reg["members_book"] is not None:
        args += ["--members-book", reg["members_book"]]
    p = run("batch_observe", args)
    rec = {"exit": p.returncode, "stdout_sha256": sha(p.stdout), "stderr": p.stderr.decode("utf-8", "replace")[:JSON_EXCERPT]}

    def failed(kind, reason):
        return dict(rec, failed=reason, failed_kind=kind, diagnostic=reader_diagnostic(w, p, reason, retain))
    if p.returncode not in (0, 1):
        return failed(f"reader-exit-{p.returncode}", f"reader exit {p.returncode}")
    if len(p.stdout) > reg["bounds"]["max_output_bytes"]:
        return failed("reader-output-over-bound", f"reader output {len(p.stdout)} bytes is over max_output_bytes")
    try:
        o = strict_json(p.stdout, "reader report")
    except Refusal as exc:
        return failed("reader-report-invalid", str(exc))
    src, page = o.get("source") or {}, o.get("page")
    if not isinstance(src, dict) or not m(HEX64, src.get("sha256")) or type(src.get("bytes")) is not int:
        return failed("no-source-identity", "reader report lacks a usable source identity")
    if src["bytes"] > reg["bounds"]["max_page_bytes"]:
        return failed("page-over-bound", "page is over max_page_bytes")
    cu = o.get("custody") if isinstance(o.get("custody"), dict) else {}
    members = []
    for x in cu.get("observations") or []:
        ins = x.get("inspection") if isinstance(x.get("inspection"), dict) else None
        cap = (ins or {}).get("capture") if isinstance((ins or {}).get("capture"), dict) else None
        members.append({"member": x.get("member"), "role": x.get("role"), "status": (ins or {}).get("status"),
                        "submission_id": (cap or {}).get("submission_id"),
                        "receipt_sha256": (cap or {}).get("receipt_sha256"), "origin": (cap or {}).get("origin"),
                        "retrospective": (cap or {}).get("retrospective"),
                        "inspect_exit": x.get("exit"), "attention": list(x.get("attention") or [])})
    review = o.get("review") if isinstance(o.get("review"), dict) else {}
    return dict(rec, failed=None, page=page, source={k: src.get(k) for k in ("kind", "commit", "path", "sha256", "bytes", "live_observed_at")},
                primary=cu.get("primary"), members=members, review_text=review.get("text_raw"),
                ambiguities=o.get("ambiguities") or [], attention=o.get("attention") or [])


def observation_outcome(w, obs) -> dict:
    """observed / failed (source or custody), plus the custody state when observed (05.03 §1-2)."""
    if obs.get("failed"):
        return {"state": "failed", "part": "source", "kind": obs["failed_kind"], "reason": obs["failed"],
                "diagnostic": obs["diagnostic"], "custody_state": "unknown", "custody_reason": "the page could not be observed"}
    members = [x for x in obs["members"] if x["role"] != "assignment-mention"]
    want = w["member"]
    if want:
        sel = [x for x in members if x["member"] == want]
        if not sel:
            return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "unresolved",
                    "custody_reason": f"registered member {want} is not named by the page"}
        x = sel[0]
    elif obs["primary"]:
        x = next((y for y in members if y["member"] == obs["primary"]), None)
    else:
        bad = [y for y in members if y["role"] not in ABSENT_ROLES]
        if not members:
            return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "absent",
                    "custody_reason": "no member is named by the page and none is registered"}
        x = bad[0] if bad else members[0]
    if x is None:
        return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "unresolved",
                "custody_reason": "the reader named a primary member it did not list"}
    role = x["role"]
    if role == "observation-failed":
        text = f"member {x['member']} inspection could not be observed (inspect exit {x['inspect_exit']}; attention {', '.join(x['attention']) or 'none'})"
        return {"state": "failed", "part": "custody", "kind": "member-observation-failed", "reason": text,
                "diagnostic": {"source": "batch_observe custody observation", "reader_exit": obs["exit"], "inspect_exit": x["inspect_exit"],
                               "excerpt": text, "retained": None,
                               "retained_note": "the reader reports the inspector's exit and attention only; run return_inspect.py inspect for the member"},
                "custody_state": "unknown", "custody_reason": text}
    if role == "primary-current-candidate":
        return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "present", "custody_reason": None}
    if role in ABSENT_ROLES:
        return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "absent",
                "custody_reason": f"member {x['member']} role {role}: no current return for this page"}
    return {"state": "observed", "part": None, "kind": None, "diagnostic": None, "custody_state": "unresolved",
            "custody_reason": f"member {x['member']} role {role}"}


def failure_line(out: dict) -> str:
    d = out["diagnostic"] or {}
    where = (f"full output {d['retained']['stderr']}" if d.get("retained") else d.get("retained_note") or "no retained output")
    return f"observation-failed ({out['part']}): {out['kind']}: {one_line(d.get('excerpt') or out.get('reason') or '')}; {where}"


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
         "direction": direction_of(reg, w),
         "expected_prior": prior}
    b["fingerprint"] = sha(canonical(b))
    return b


def direction_of(reg, w) -> dict:
    """The review direction a decision is judged under (05.02 CONTRACT §2). Clock- and layout-only fields are excluded."""
    a = w["agreement"]
    return {"schema": "prime-cycle-direction/1", "agreement_sha256": sha(canonical(a)),
            "fields": {k: sha(canonical(a.get(k))) for k in DIRECTION_FIELDS},
            "review_location": w["review_location"], "book": reg["book"]}


def direction_diff(now: dict, then) -> list:
    if not isinstance(then, dict):
        return ["direction (absent from the template)"]
    names = [f"agreement.{k}" for k in DIRECTION_FIELDS if now["fields"][k] != (then.get("fields") or {}).get(k)]
    if not names and now["agreement_sha256"] != then.get("agreement_sha256"):
        names.append("agreement (other keys)")
    names += [k for k in ("review_location", "book", "schema") if now[k] != then.get(k)]
    return names


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
        try:  # a marker that does not parse is torn (interrupted); a parsed marker that does not bind means altered after commit
            marker = strict_json(read_bounded(files["COMMITTED.json"], MAX_DOC, "marker"), "marker")
            need(isinstance(marker, dict), "marker: not an object")
        except (Refusal, OSError) as exc:
            out["partial"].append({"review_id": d.name, "phase": "partial-marker-mismatch", "marker": "torn", "reason": str(exc)})
            continue
        try:
            rb = read_bounded(files["record.json"], MAX_DOC, "record")
            mb = read_bounded(files["REVIEW.md"], MAX_DOC, "REVIEW.md")
        except (Refusal, OSError) as exc:
            out["partial"].append({"review_id": d.name, "phase": "partial-marker-mismatch", "marker": "hash-mismatch", "reason": str(exc)})
            continue
        if marker.get("record_sha256") != sha(rb) or marker.get("review_md_sha256") != sha(mb):
            out["partial"].append({"review_id": d.name, "phase": "partial-marker-mismatch", "marker": "hash-mismatch",
                                   "reason": "marker hashes do not match the files"})
            continue
        try:
            rec = strict_json(rb, "record")
            need(isinstance(rec, dict) and rec.get("schema") in RECORD_SCHEMAS, "unknown record schema")
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
    out = observation_outcome(w, obs)
    obs_failed = out["state"] == "failed"
    item["observation"] = {k: out[k] for k in ("state", "part", "kind", "diagnostic")}
    item["custody"].update(state=out["custody_state"], state_reason=out["custody_reason"])
    if obs_failed:
        attention.append(failure_line(out))
    for p in scan["partial"]:
        attention.append(f"partial review {p['review_id']} ({p['phase']}); see inspect; recover with a new review_id")
    for p in scan["invalid"]:
        attention.append(f"invalid review directory {p['review_id']}: {p['reason']}")
    head = scan["committed"][heads[0]] if len(heads) == 1 else None
    if head is None:  # no-return only for successfully observed absent custody (05.03 §2)
        pass_state = {"present": "awaiting-review", "absent": "no-return", "unresolved": "custody-unresolved"}.get(out["custody_state"], "observation-failed")
        if pass_state == "awaiting-review" and binding["receipt_sha256"] is None:
            pass_state = "custody-unresolved"
        if pass_state == "custody-unresolved":
            attention.append(f"custody-unresolved: {out['custody_reason'] or 'no verified receipt'}; not treated as no-return")
    if head is None and (obs.get("review_text") or "").strip() not in ("", "PENDING."):  # exact-literal PENDING is not a review
        attention.append("legacy-review-unmapped: the page has review prose and no recorded cycle review; adopt only by an attributed review")
        item["legacy_review_text"] = obs["review_text"]
    item["historical"] = None
    if head:
        rid = heads[0]
        dec = head["record"]["decision"]
        j, hb = dec["judgment"], dec["binding"]
        g = j["goal"]
        same_goal = (g["goal_id"], g["goal_sha256"]) == (w["goal"]["goal_id"], goal_sha(w))
        if g["terminal"] == "completed" and same_goal:
            goal_terminal = "completed"
        elif g["terminal"] == "completed":
            goal_terminal = f"open (prior completion bound to goal {g['goal_id']} {g['goal_sha256'][:12]})"
        else:
            goal_terminal = "open"
        recovered = {r["record"]["decision"].get("recovers") for r in scan["committed"].values()}
        altered = [p["review_id"] for p in scan["partial"] if p.get("marker") == "hash-mismatch" and p["review_id"] not in recovered]
        changed = (["page"] if hb["source"]["page_sha256"] != binding["source"]["page_sha256"] else []) + \
                  [k for k in CURRENT_KEYS if hb.get(k) != binding[k]]
        if obs_failed:  # unobservable evidence is neither current nor stale
            pass_state, reason = "observation-failed", "observation-failed"
            attention.append(f"observation-failed: {rid} declarations are historical; the current evidence could not be observed")
        elif head["record"]["schema"] != "prime-cycle-review/2":
            pass_state, reason = "review-unusable", "legacy-binding"
            attention.append(f"review-unusable: {rid} is a {head['record']['schema']} record without a direction binding; "
                             "its declarations are historical only; record a successor review")
        elif altered:
            pass_state, reason = "review-unusable", "altered-review"
            attention.append(f"review-unusable: {', '.join(altered)} altered after commit (hash-mismatch) and not recovered; "
                             f"{rid} declarations are historical; record a successor with recovers")
        elif changed:
            pass_state, reason = "review-stale", "review-stale"
            attention.append(f"review-stale: {rid} binds a different {', '.join(changed)}; its declarations are historical; re-review required")
        else:
            pass_state, reason = "reviewed", None
        rep = head["record"]["report"]
        author = dec["attribution"]["actor_label"]
        na = (dict(j["next_action"], author=author, source=f"{w['review_location']}/{rid}/record.json",
                   record_sha256=head["record_sha256"]) if j["next_action"] else None)
        item.update(latest_review={"review_id": rid, "record_sha256": head["record_sha256"], "author": author,
                                   "outcome": j["outcome"], "effective": rep["effective"], "current": reason is None},
                    holds=rep["holds"], unresolved=j["unresolved"])
        if reason is None:
            item.update(disposition=j["disposition"], pass_terminal=j["pass_terminal"], goal_terminal=goal_terminal, next_action=na)
        else:  # PC-01: keep the old declarations, never as current status
            item.update(disposition="unknown", pass_terminal="unknown", goal_terminal="unknown", next_action=None,
                        historical={"review_id": rid, "record_sha256": head["record_sha256"], "reason": reason,
                                    "disposition": j["disposition"], "pass_terminal": j["pass_terminal"],
                                    "goal_terminal": goal_terminal, "goal_id": g["goal_id"], "next_action": na})
        if any(h["status"] != "reply-bound" for h in rep["holds"]):
            attention.append("hold open: " + ", ".join(f"{h['hold_id']} ({h['status']}) blocks {h['dependent_scope']}" for h in rep["holds"])
                             + ("" if reason is None else " (from a non-current review; still blocking)"))
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
    item["template"] = {"schema": "prime-cycle-decision/2", "review_id": f"{w['pass']}-r{n}",
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


def inside(child: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath([os.path.normcase(str(child)), os.path.normcase(str(parent))]) == os.path.normcase(str(parent))
    except ValueError:  # different drives
        return False


def read(reg_path: Path, templates: Path | None = None, forbid: Path | None = None, retain=None) -> dict:
    reg = load_registration(reg_path)
    items, scans = [], []
    for w in reg["works"]:
        obs = observe(reg, w, retain)
        scan = scan_reviews(reg, w)
        items.append(derive(reg, w, obs, scan))
        scans.append(scan)
    guard_actions(reg, items, scans)
    summary = {"works": len(items), "awaiting_review": sum(i["pass_state"] == "awaiting-review" for i in items),
               "reviewed_current": sum(i["pass_state"] == "reviewed" for i in items),
               "stale_or_unusable": sum(i["pass_state"] in ("review-stale", "review-unusable") for i in items),
               "finished_passes": sum(i["pass_terminal"] == "finished" for i in items),
               "completed_goals": sum(i["goal_terminal"] == "completed" for i in items),
               "open_holds": sum(h["status"] != "reply-bound" for i in items for h in i["holds"]),
               "observation_failed": sum(i["pass_state"] == "observation-failed" for i in items),
               "custody_unresolved": sum(i["pass_state"] == "custody-unresolved" for i in items),
               "basis": "current values only; historical declarations of stale or unusable reviews are not counted"}
    view = {"schema": "prime-cycle-view/3", "registration_sha256": sha(reg_path.read_bytes()), "book": reg["book"],
            "source": reg["source"], "summary": summary, "works": items, "elected": None,
            "attention_count": sum(len(i["attention"]) for i in items), "authority": AUTHORITY,
            "note": "derived from work-local review records and fresh reader observations; noncanonical; rebuildable"}
    out = canonical(view)
    need(len(out) <= reg["bounds"]["max_output_bytes"], "view is over max_output_bytes")
    if templates is not None:
        root = abs_path(str(templates), "--templates")
        need(str(root).lower().startswith(str(Path(reg["output_root"])).lower()), "--templates must be under output_root")
        need(forbid is None or not inside(root, forbid), "--templates must not lie inside the journal root")
        root.mkdir(parents=False, exist_ok=True)
        for it in items:
            with open(root / f"template-{it['work_id']}.json", "xb") as h:
                h.write(canonical(it["template"]))
    return view


def view_text(v: dict) -> str:
    out = [f"Prime cycle view  book {v['book']}  source {v['source']['kind']} {v['source']['commit'] or '(live files)'}",
           "Derived from work-local review records. Noncanonical. Nothing is elected or dispatched."]
    s = v["summary"]
    out += [f"summary (current only): works {s['works']}, awaiting review {s['awaiting_review']}, reviewed current {s['reviewed_current']}, "
            f"stale or unusable {s['stale_or_unusable']}, finished passes {s['finished_passes']}, completed goals {s['completed_goals']}, "
            f"open holds {s['open_holds']}, observation failed {s['observation_failed']}, custody unresolved {s['custody_unresolved']}", ""]
    for it in v["works"]:
        hist = it.get("historical")

        def shown(key):
            return it[key] if not hist else f"unknown (historical {hist[key]} in {hist['review_id']}, {hist['reason']})"
        out.append(f"{it['work_id']}  {it['page']}")
        out.append(f"  pass state: {it['pass_state']}   review disposition: {shown('disposition')}   pass terminal: {shown('pass_terminal')}")
        out.append(f"  goal {it['goal']['goal_id']}: {shown('goal_terminal')}")
        c = it["custody"]
        out.append(f"  custody: {c['member']} role {c['role']} state {c['state']} receipt {(c['receipt_sha256'] or 'none')[:16]} (custody is not acceptance)")
        if it["latest_review"]:
            lr = it["latest_review"]
            out.append(f"  latest review: {lr['review_id']} by {lr['author']} outcome {lr['outcome']} (prime_review effective {lr['effective']})"
                       + ("" if lr["current"] else "  [not current]"))
        for h in it["holds"]:
            out.append(f"  hold {h['hold_id']} {h['status']}: blocks {', '.join(h['dependent_scope']) or 'nothing'}"
                       + ("" if not hist else " (from a non-current review; still blocking)"))
        if it["next_action"]:
            na = it["next_action"]
            out.append(f"  recorded next action ({na['author']}, {na['source']}): {na['action_id']}: {na['text']}")
            for g in it.get("next_action_guard", []):
                out.append(f"    holds in {g['against_work']}: {g['result']}")
        if hist and hist["next_action"]:
            na = hist["next_action"]
            out.append(f"  historical next action (not current; {na['author']}, {na['source']}): {na['action_id']}: {na['text']}")
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


def record(reg_path: Path, decision_path: Path, retain=None) -> tuple[int, str]:
    reg = load_registration(reg_path)
    d = strict_json(read_bounded(decision_path, MAX_DOC, "decision"), "decision")
    exact(d, DECISION_KEYS, "decision")
    need(d["schema"] == "prime-cycle-decision/2",
         f"decision schema {d['schema']!r} is not prime-cycle-decision/2; the template is from an older read; read again")
    need(m(LABEL, d["review_id"]), "review_id must be a label")
    exact(d["attribution"], {"actor_label", "role", "evidence"}, "attribution")
    need(isinstance(d["attribution"]["actor_label"], str) and d["attribution"]["actor_label"].strip(), "attribution.actor_label is required")
    b = d["binding"]
    need(isinstance(b, dict) and isinstance(b.get("work_id"), str), "binding must name a work_id")
    w = next((x for x in reg["works"] if x["work_id"] == b["work_id"]), None)
    need(w is not None, f"work {b.get('work_id')} is not registered")
    check_judgment(d["judgment"], w)
    bsrc = b.get("source") if isinstance(b.get("source"), dict) else {}
    need(m(HEX64, bsrc.get("page_sha256")) and type(bsrc.get("page_bytes")) is int and bsrc["page_bytes"] >= 0,
         "template binding has no observed source identity (made from a failed read); read again")
    rdir = review_dir(reg, w)
    lane_evidence = Path(reg["repository"]) / w["page"].rsplit("/", 1)[0] / "evidence"
    need(lane_evidence.is_dir() and not is_link(lane_evidence), "the lane's evidence directory must exist as a plain directory")
    target = rdir / d["review_id"]
    scan = scan_reviews(reg, w)
    if target.exists() and d["review_id"] not in scan["committed"]:
        raise Refusal(f"partial review present at {target}; run inspect, then record under a new review_id with recovers")
    prior = prior_of(scan)
    need(prior != "fork", "lineage-fork: more than one committed head; record a successor of one head explicitly is not supported here")
    obs = observe(reg, w, retain)
    out = observation_outcome(w, obs)
    if out["state"] == "failed":
        raise Refusal(failure_line(out).replace("observation-failed", "observation failed", 1) + "; nothing was recorded")
    replay = target.exists()
    if not replay:  # the prior-state check comes first so a stale template gets the specific reason
        need(b.get("expected_prior") == prior, f"expected_prior {b.get('expected_prior')} does not equal the latest committed review {prior}")
    expected_now = current_binding(reg, w, obs, b.get("expected_prior"))
    ddiff = direction_diff(expected_now["direction"], b.get("direction"))  # PC-02: the direction the decision was judged under
    need(not ddiff, "direction changed since read: " + ", ".join(ddiff) + "; read again for a new template")
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
    rec = {"schema": "prime-cycle-review/2", "work_id": w["work_id"], "review_id": d["review_id"], "decision": d,
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
        raise PartialWrite(f"write failed in {target}: {type(exc).__name__}: {exc}; files so far are kept; use inspect", target) from None
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


def packet(reg_path: Path, work_id: str, out_dir: str, forbid: Path | None = None) -> tuple[int, str]:
    reg = load_registration(reg_path)
    w = next((x for x in reg["works"] if x["work_id"] == work_id), None)
    need(w is not None, f"work {work_id} is not registered")
    need(w["member"] and reg["members_book"], "packet needs a registered member and members_book")
    out = abs_path(out_dir, "--out")
    need(str(out).lower().startswith(str(Path(reg["output_root"])).lower()), "--out must be under output_root")
    need(forbid is None or not inside(out, forbid), "--out must not lie inside the journal root")
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
    text = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    cov = packet_coverage(out, req) if p.returncode == 0 else {"available": False, "reason": f"review_packet exit {p.returncode}"}
    return (0 if p.returncode == 0 else 2), text + coverage_text(cov), cov


def packet_coverage(out: Path, req: dict) -> dict:
    """What this packet's own request gathered, and the member's captured payloads it did not gather (05.03 §4).
    Read-only over the packet output; the request and default gathering are unchanged."""
    try:
        pk = strict_json(read_bounded(out / "packet.json", MAX_STDOUT_SNAPSHOT, "packet.json"), "packet.json")
        cu = strict_json(read_bounded(out / "custody.json", MAX_STDOUT_SNAPSHOT, "custody.json"), "custody.json")
    except (Refusal, OSError) as exc:
        return {"available": False, "reason": str(exc)}
    srcs = [{"id": x.get("id"), "role": x.get("role"), "kind": x.get("kind"), "status": x.get("status"),
             "bytes": x.get("bytes"), "sha256": x.get("sha256")} for x in pk.get("sources") or [] if isinstance(x, dict)]
    gathered = {x["id"] for x in srcs if x["status"] == "present"}
    cap = cu.get("capture") if isinstance(cu.get("capture"), dict) else {}
    payloads = [x.get("logical") for x in cap.get("payloads") or [] if isinstance(x, dict)]
    requested_payloads = {x.get("name") for x in req["sources"] if x.get("kind") == "member-file"}
    return {"available": True, "basis": "this packet's own request; not a complete artifact inventory",
            "requested": srcs, "gathered": sorted(gathered),
            "absent_or_unverified": [x["id"] for x in srcs if x["status"] != "present"],
            "artifact_checks_requested": sum(1 for x in req["sources"] if x.get("artifact_manifest")),
            "page_included": any(x.get("id") == "page" for x in req["sources"]),
            "page_note": None if any(x.get("id") == "page" for x in req["sources"]) else
            "not requested: the default request adds the page only for a git-blob registration",
            "member_payloads_not_gathered": [lp for lp in payloads if lp and not any(n.startswith("payload/") for n in requested_payloads)],
            "custody_status": cu.get("status")}


def coverage_text(cov: dict) -> str:
    if not cov.get("available"):
        return f"coverage: unavailable ({cov.get('reason')})\n"
    lines = [f"coverage ({cov['basis']}):",
             "  requested: " + "; ".join(f"{x['id']} ({x['kind']}) {x['status']} {x['bytes']} b sha {(x['sha256'] or 'none')[:16]}" for x in cov["requested"]),
             f"  artifact checks requested: {cov['artifact_checks_requested']}",
             f"  page included: {'yes' if cov['page_included'] else 'no (' + cov['page_note'] + ')'}",
             f"  member captured payloads not gathered: {len(cov['member_payloads_not_gathered'])}"
             + ("" if not cov["member_payloads_not_gathered"] else " - " + ", ".join(cov["member_payloads_not_gathered"]))]
    if cov["absent_or_unverified"]:
        lines.append("  absent or unverified: " + ", ".join(cov["absent_or_unverified"]))
    return "\n".join(lines) + "\n"


# ---------- journal (05.02 CONTRACT §5) ----------

def now_stamp() -> tuple[str, str]:
    t = datetime.now(timezone.utc)
    return t.astimezone().isoformat(), t.isoformat()


def jwrite(path: Path, data: bytes) -> None:
    """Exclusive create of one journal file; a hook point for journal-failure tests."""
    with open(path, "xb") as h:
        h.write(data)
        h.flush()
        os.fsync(h.fileno())


def review_ref(target: Path) -> dict:
    """What is on disk now for one review directory: a committed record's identity, or the files present."""
    files = {p.name: sha(p.read_bytes()) for p in sorted(target.iterdir()) if p.is_file()} if target.is_dir() else {}
    ref = {"dir": str(target), "review_id": target.name, "files": files}
    rb = target / "record.json"
    if "COMMITTED.json" in files and rb.is_file():
        try:
            rec = json.loads(rb.read_bytes().decode("utf-8"))
            ref.update(work_id=rec.get("work_id"), schema=rec.get("schema"))
        except ValueError:
            pass
        ref.update(record_sha256=files.get("record.json"), marker_sha256=files["COMMITTED.json"])
    return ref


class Journal:
    """One operation's start/end events under an explicit root. Nothing is rewritten; a missing end means incomplete."""

    def __init__(self, root_text: str, operation: str, argv: list, inputs: dict, supplied: dict):
        try:
            self.root = abs_path(root_text, "--journal-root")
        except Refusal as exc:
            raise JournalError(str(exc)) from None
        snaps, info = {}, {}
        for name, text in inputs.items():
            if text is None:
                continue
            try:
                p = abs_path(text, f"--{name}")
                b = read_bounded(p, MAX_DOC, name)
                snaps[name], info[name] = b, {"path": str(p), "sha256": sha(b), "bytes": len(b), "snapshot": f"{name}.json"}
            except (Refusal, OSError) as exc:
                info[name] = {"path": text, "error": str(exc)}
        try:  # containment: never inside the repository or members book a registration names
            reg = json.loads(snaps["registration"].decode("utf-8")) if "registration" in snaps else {}
            for key in ("repository", "members_book"):
                v = reg.get(key) if isinstance(reg, dict) else None
                if isinstance(v, str) and os.path.isabs(v):
                    need_j(not inside(self.root, Path(os.path.abspath(v))), f"the journal root must not lie inside the {key}")
        except (ValueError, AttributeError):
            pass
        if not self.root.exists():  # created only after the containment check
            need_j(self.root.parent.is_dir(), f"the journal root's parent {self.root.parent} must exist")
            os.mkdir(self.root)
        need_j(self.root.is_dir() and not is_link(self.root), "the journal root must be a plain directory")
        local, utc = now_stamp()
        self.t0 = time.monotonic()
        self.op_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + secrets.token_hex(6)
        day = self.root / local[:10]
        if not day.exists():
            os.mkdir(day)
        need_j(day.is_dir() and not is_link(day), f"journal day {day} must be a plain directory")
        self.dir = day / self.op_id
        os.mkdir(self.dir)  # exclusive: a collision refuses
        start = {"schema": "prime-cycle-journal-start/1", "op_id": self.op_id, "operation": operation,
                 "machine": {"started_at_local": local, "started_at_utc": utc,
                             "clock_basis": "system clock at operation start; local offset from the OS timezone",
                             "pid": os.getpid(), "python": sys.version.split()[0], "tool_path": str(Path(__file__).resolve()),
                             "tool_sha256": sha(Path(__file__).read_bytes()), "pins": {k: v[1] for k, v in PINS.items()},
                             "argv": argv, "cwd": os.getcwd(), "inputs": info},
                 "supplied": {"caller_label": supplied.get("caller"), "note": supplied.get("note"),
                              "basis": "as supplied on the command line; not authenticated"}}
        for name, b in snaps.items():
            jwrite(self.dir / f"{name}.json", b)
        jwrite(self.dir / "start.json", canonical(start))
        self.info = {"enabled": True, "root": str(self.root), "op_id": self.op_id, "dir": str(self.dir)}

    def retain(self, name: str, data: bytes) -> str:
        """Keep one exact child output beside this operation's events (exclusive create); return its path."""
        need_j(m(LABEL, name), f"retained name {name!r} is not a plain label")
        jwrite(self.dir / name, data)
        return str(self.dir / name)

    def end(self, code: int, status: str, stdout: bytes, result: dict) -> None:
        local, utc = now_stamp()
        snap = stdout[:MAX_STDOUT_SNAPSHOT]
        jwrite(self.dir / "stdout.txt", snap)
        jwrite(self.dir / "end.json", canonical({
            "schema": "prime-cycle-journal-end/1", "op_id": self.op_id,
            "machine": {"ended_at_local": local, "ended_at_utc": utc, "duration_seconds": round(time.monotonic() - self.t0, 6),
                        "exit": code, "status": status,
                        "stdout": {"sha256": sha(stdout), "bytes": len(stdout), "snapshot": "stdout.txt", "truncated": len(snap) < len(stdout)},
                        "result": result}}))


def need_j(cond, message):
    if not cond:
        raise JournalError(message)


JOURNAL_OFF = {"enabled": False, "note": "no --journal-root; this operation is not logged"}


def operate(a, forbid, retain=None) -> tuple[int, object, str, dict]:
    """Run one command; return (exit, payload dict-or-text, journal status, journal result). Never raises Refusal."""
    try:
        reg = abs_path(a.registration, "--registration")
        if a.command == "read":
            v = read(reg, Path(a.templates) if a.templates else None, forbid, retain)
            code = 1 if v["attention_count"] else 0
            tpl = [{"path": str(p), "sha256": sha(p.read_bytes())} for p in
                   ([Path(os.path.abspath(a.templates)) / f"template-{it['work_id']}.json" for it in v["works"]] if a.templates else [])]
            result = {"view_sha256": sha(canonical(v)), "summary": v["summary"], "templates": tpl,
                      "works": [{"work_id": it["work_id"], "page_sha256": it["source"]["page_sha256"], "pass_state": it["pass_state"]} for it in v["works"]]}
            return code, (v if a.json else view_text(v)), ("ok-attention" if code else "ok"), result
        if a.command == "record":
            code, text = record(reg, abs_path(a.decision, "--decision"), retain)
            word, _, rest = text.partition(" ")
            ref = review_ref(Path(rest.splitlines()[0])) if word in ("recorded", "already-recorded") else {}
            status = "replay" if word == "already-recorded" else ("recorded" if code == 0 else "recorded-attention")
            return code, text, status, {"review": ref}
        if a.command == "inspect":
            code, out = inspect(reg, a.work)
            return code, out, ("ok-attention" if code else "ok"), {"phases": {r["review_id"]: r["phase"] for r in out["reviews"]}}
        code, text, cov = packet(reg, a.work, a.out, forbid)
        st = Path(os.path.abspath(a.out)) / "assembly-status.json"
        return code, text, ("ok" if code == 0 else "refused"), {"out": str(Path(os.path.abspath(a.out))),
                                                                  "assembly_status_sha256": sha(st.read_bytes()) if st.is_file() else None,
                                                                  "coverage": cov}
    except PartialWrite as exc:
        return 3, f"partial: {exc}\n", "partial", {"review": review_ref(exc.target) if exc.target else {}}
    except Refusal as exc:
        return 2, f"refused: {exc}\n", "refused", {}
    except (OSError, subprocess.SubprocessError) as exc:
        return 2, f"refused: {type(exc).__name__}: {exc}\n", "refused", {}


# ---------- day view (05.02 CONTRACT §6) ----------

def load_event(p: Path):
    if not p.is_file() or is_link(p):
        return None
    try:
        return strict_json(read_bounded(p, MAX_DOC, p.name), p.name)
    except Refusal:
        return "unreadable"


def verify_review(dir_text: str, record_sha: str) -> dict:
    d = Path(dir_text)
    try:
        rb, mb = (d / "record.json").read_bytes(), (d / "REVIEW.md").read_bytes()
        marker = json.loads((d / "COMMITTED.json").read_bytes().decode("utf-8"))
    except (OSError, ValueError) as exc:
        return {"verified": False, "reason": f"{type(exc).__name__}: {exc}"}
    ok = sha(rb) == record_sha and marker.get("record_sha256") == record_sha and marker.get("review_md_sha256") == sha(mb)
    if not ok:
        return {"verified": False, "reason": "record or marker no longer matches the journalled record hash"}
    rec = json.loads(rb.decode("utf-8"))
    j = rec["decision"]["judgment"]
    return {"verified": True, "schema": rec["schema"], "work_id": rec["work_id"], "author": rec["decision"]["attribution"]["actor_label"],
            "disposition": j["disposition"], "pass_terminal": j["pass_terminal"], "goal_terminal": j["goal"]["terminal"],
            "goal_id": j["goal"]["goal_id"], "goal_sha256": j["goal"]["goal_sha256"], "page": rec["decision"]["binding"]["page"],
            "holds": [h["hold_id"] + " " + h["status"] for h in rec["report"]["holds"]]}


def day(root_text: str, date: str | None, reg_text: str | None) -> tuple[int, dict]:
    root = abs_path(root_text, "--journal-root")
    need(root.is_dir() and not is_link(root), "--journal-root must be an existing plain directory")
    date = date or datetime.now().astimezone().isoformat()[:10]
    need(m(DATE, date), "--date must be YYYY-MM-DD")
    ddir = root / date
    need(ddir.is_dir() and not is_link(ddir), f"no journal day {date} under {root}")
    dirs = sorted(p for p in ddir.iterdir())
    need(len(dirs) <= MAX_DAY_OPS, f"the day holds more than {MAX_DAY_OPS} entries")
    ops, reviews, counts = [], {}, {}
    for p in dirs:
        if not p.is_dir() or is_link(p):
            ops.append({"op_id": p.name, "status": "unreadable", "reason": "not a plain operation directory"})
            continue
        st, en = load_event(p / "start.json"), load_event(p / "end.json")
        if not isinstance(st, dict) or st.get("schema") != "prime-cycle-journal-start/1":
            ops.append({"op_id": p.name, "status": "unreadable", "reason": "start.json missing or invalid"})
            continue
        row = {"op_id": p.name, "operation": st["operation"], "started_at_local": st["machine"]["started_at_local"],
               "caller_label": st["supplied"]["caller_label"], "note": st["supplied"]["note"]}
        if en is None:
            row.update(status="incomplete", exit=None, duration_seconds=None, detail="no end event: end state unknown")
        elif not isinstance(en, dict) or en.get("schema") != "prime-cycle-journal-end/1":
            row.update(status="unreadable", exit=None, duration_seconds=None, detail="end.json invalid")
        else:
            mm = en["machine"]
            row.update(status=mm["status"], exit=mm["exit"], duration_seconds=mm["duration_seconds"])
            if mm["status"] in ("refused", "error") and (p / "stdout.txt").is_file():
                row["detail"] = (p / "stdout.txt").read_bytes()[:2000].decode("utf-8", "replace").splitlines()[0:1]
            rv = mm["result"].get("review") or {}
            if rv:
                row["review"] = {k: rv.get(k) for k in ("review_id", "dir", "record_sha256")}
                if rv.get("record_sha256") and mm["status"] in ("recorded", "recorded-attention", "replay"):
                    key = (rv["dir"], rv["record_sha256"])
                    reviews.setdefault(key, {"review_id": rv["review_id"], "dir": rv["dir"], "record_sha256": rv["record_sha256"],
                                             "invocations": [], "replays": 0})
                    reviews[key]["invocations"].append(p.name)
                    reviews[key]["replays"] += mm["status"] == "replay"
        ops.append(row)
        c = counts.setdefault(row["operation"], {})
        c[row["status"]] = c.get(row["status"], 0) + 1
    uniq = []
    for r in reviews.values():
        r.update(verify_review(r["dir"], r["record_sha256"]))
        uniq.append(r)
    good = [r for r in uniq if r["verified"]]
    declared = {"finished_passes": len({(r["work_id"], r["page"]) for r in good if r["pass_terminal"] == "finished"}),
                "completed_goals": len({(r["work_id"], r["goal_id"], r["goal_sha256"]) for r in good if r["goal_terminal"] == "completed"}),
                "holds": sorted({f"{r['work_id']}:{h}" for r in good for h in r["holds"]}),
                "basis": ("declared in unique committed records journalled this day and re-verified now; each work's pass and each "
                          "work goal counts once however many reviews or replays declare it; declared is not current")}
    current = {"checked": False, "note": "not checked (no --registration)"}
    if reg_text:
        v = read(abs_path(reg_text, "--registration"))
        heads = {(it["latest_review"]["review_id"], it["latest_review"]["record_sha256"]): it for it in v["works"] if it["latest_review"]}
        for r in uniq:
            it = heads.get((r["review_id"], r["record_sha256"]))
            r["current_head"] = bool(it and it["latest_review"]["current"])
        current = {"checked": True, "registration_sha256": v["registration_sha256"], "summary": v["summary"],
                   "finished_passes": [it["work_id"] for it in v["works"] if it["pass_terminal"] == "finished"],
                   "completed_goals": [it["work_id"] for it in v["works"] if it["goal_terminal"] == "completed"],
                   "open_holds": [f"{it['work_id']}:{h['hold_id']}" for it in v["works"] for h in it["holds"] if h["status"] != "reply-bound"],
                   "not_current": [it["work_id"] for it in v["works"] if it.get("historical")]}
    out = {"schema": "prime-cycle-day/1", "date": date, "journal_root": str(root), "operations": ops, "counts": counts,
           "unique_reviews": uniq, "record_invocations": sum(len(r["invocations"]) for r in uniq), "declared": declared,
           "current": current, "incomplete": [o["op_id"] for o in ops if o["status"] == "incomplete"],
           "unreadable": [o["op_id"] for o in ops if o["status"] == "unreadable"],
           "time": "per-operation durations only; incomplete operations have unknown duration; no totals or productivity are derived",
           "note": "read-only; this view is not itself logged; reasons and decisions stay on the work-local review records"}
    bad = out["incomplete"] or out["unreadable"] or any(not r["verified"] for r in uniq)
    return (1 if bad else 0), out


def day_text(o: dict) -> str:
    out = [f"Prime cycle day {o['date']}  journal {o['journal_root']}  (read-only; this view is not logged)",
           "attempts: " + "; ".join(f"{op} " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) for op, c in sorted(o["counts"].items())), ""]
    for r in o["operations"]:
        dur = "unknown" if r.get("duration_seconds") is None else f"{r['duration_seconds']:.3f}s"
        line = f"  {r['op_id']}  {r.get('operation', '?'):7} {r['status']:18} exit {r.get('exit')}  {r.get('started_at_local', '?')}  {dur}"
        line += f"  caller {r.get('caller_label') or '-'}"
        out.append(line)
        if r.get("detail"):
            out.append(f"      {r['detail'] if isinstance(r['detail'], str) else ' '.join(r['detail'])}")
        if r.get("review"):
            out.append(f"      review {r['review']['review_id']} record {(r['review']['record_sha256'] or 'none')[:16]}")
    out.append("")
    out.append(f"unique reviews (re-verified now): {len(o['unique_reviews'])} from {o['record_invocations']} record invocations")
    for r in o["unique_reviews"]:
        if r["verified"]:
            out.append(f"  {r['work_id']} {r['review_id']} by {r['author']}: {r['disposition']}, pass {r['pass_terminal']}, goal {r['goal_id']} "
                       f"{r['goal_terminal']}; invocations {len(r['invocations'])} (replays {r['replays']})"
                       + ("" if "current_head" not in r else f"; current head {'yes' if r['current_head'] else 'no'}"))
        else:
            out.append(f"  {r['review_id']}: NOT VERIFIED now ({r['reason']})")
    dcl = o["declared"]
    out.append(f"declared in unique verified records (each work pass and goal once; not current status): finished passes "
               f"{dcl['finished_passes']}, completed goals {dcl['completed_goals']}, holds {', '.join(dcl['holds']) or 'none'}")
    cur = o["current"]
    if cur["checked"]:
        out.append(f"current (fresh read): finished passes {', '.join(cur['finished_passes']) or 'none'}; completed goals "
                   f"{', '.join(cur['completed_goals']) or 'none'}; open holds {', '.join(cur['open_holds']) or 'none'}; "
                   f"not current {', '.join(cur['not_current']) or 'none'}")
    else:
        out.append("current: not checked (no --registration)")
    for k in ("incomplete", "unreadable"):
        if o[k]:
            out.append(f"! {k}: {', '.join(o[k])}")
    out.append(o["time"])
    return "\n".join(out) + "\n"


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
    for p in (r, rc, i, pk):
        p.add_argument("--journal-root")
        p.add_argument("--caller")
        p.add_argument("--note")
    dy = sub.add_parser("day")
    dy.add_argument("--journal-root", required=True)
    dy.add_argument("--date")
    dy.add_argument("--registration")
    dy.add_argument("--json", action="store_true")
    argv_list = list(sys.argv[1:] if argv is None else argv)
    a = ap.parse_args(argv_list)
    if a.command == "day":
        try:
            code, o = day(a.journal_root, a.date, a.registration)
        except (Refusal, OSError, subprocess.SubprocessError) as exc:
            sys.stdout.write(f"refused: {exc}\n")
            return 2
        sys.stdout.write(canonical(o).decode("utf-8") if a.json else day_text(o))
        return code
    j = None
    if a.journal_root:
        try:
            j = Journal(a.journal_root, a.command, argv_list, {"registration": a.registration, "decision": getattr(a, "decision", None)},
                        {"caller": a.caller, "note": a.note})
        except (JournalError, Refusal, OSError) as exc:
            sys.stdout.write(f"refused: journal start failed: {type(exc).__name__}: {exc}; nothing was run\n")
            return 4
    try:
        code, payload, status, result = operate(a, j.root if j else None, j.retain if j else None)
    except Exception as exc:  # unexpected: say so, log it as error, never as success
        code, payload, status, result = 6, f"error: {type(exc).__name__}: {exc}\n", "error", {}
    jinfo = j.info if j else JOURNAL_OFF
    if isinstance(payload, dict):
        out = canonical(dict(payload, journal=jinfo)).decode("utf-8")
    else:
        out = payload + (f"journal: {jinfo['root']} op {jinfo['op_id']}\n" if j else
                         "journal: disabled (no --journal-root; this operation is not logged)\n")
    sys.stdout.write(out)
    sys.stdout.flush()
    if j:
        try:
            j.end(code, status, out.encode("utf-8"), result)
        except Exception as exc:  # the operation's result stands and is stated; the journal stays incomplete
            what = ""
            rv = result.get("review") or {}
            if rv.get("dir"):
                what = (f"; the review IS {'committed' if rv.get('record_sha256') else 'present as a partial'} at {rv['dir']}")
            sys.stderr.write(f"journal: end event FAILED for op {j.op_id} ({type(exc).__name__}: {exc}); operation exit was {code} "
                             f"({status}){what}; this journal entry stays incomplete; nothing was retried\n")
            return 5
    return code


if __name__ == "__main__":
    sys.exit(main())
