"""Fixture state projection with explicit closure (0507.prime-support/05.12). Standard library only.

  python -B state_projection.py project --input OBS.json [--inspect] [--json]

Contract: 00.kernel/00.00.10.work/0507.prime-support/evidence/projection05.12/CONTRACT.md. Input is a strict list of
supplied batch observations over a declared fixture scope; no page, Git blob or prose is read. Member custody comes only
from the pinned accepted inspector, as live observations kept apart from supplied commit-time facets. Output goes to
stdout. A projection is not a v1 assignment record and grants no release, acceptance, seat or work.
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
from datetime import datetime, timezone
from pathlib import Path

PINS = {"return_inspect": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
        "return_capture": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"}
RC_DIR = Path(__file__).resolve().parent.parent / "return-capture-pass01"
INSPECTION_SCHEMA = "return-capture-inspection/1"
INSPECTION_EXIT = {"complete": 0, "reserved": 1, "missing": 1, "incomplete": 2, "refused": 2}
AUTHORITY = "none; a projection grants no release, acceptance, seat or work"
NOTE = "not a v1 assignment record and not canonical"
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
LANE = re.compile(r"^\d{4}\.[a-z0-9][a-z0-9-]*$")
BATCH = re.compile(r"^05\.\d\d$")
MEMBER = re.compile(r"^01\d\d\.[a-z0-9][a-z0-9.-]*$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
OBS_KEYS = {"id", "lane", "batch", "provenance", "document", "release", "claim", "return", "review", "publication"}


class Refusal(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def strict_json(data: bytes, label: str):
    def pairs(seq):
        out = {}
        for key, value in seq:
            if key in out:
                raise Refusal(f"{label}: duplicate key {key}")
            out[key] = value
        return out

    def constant(name):
        raise Refusal(f"{label}: nonfinite number {name}")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError:
        raise Refusal(f"{label}: not UTF-8") from None
    except json.JSONDecodeError as exc:
        raise Refusal(f"{label}: invalid JSON ({exc.msg})") from None


# ---------- strict input ----------

def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def exact(obj, keys: set, where: str) -> None:
    need(isinstance(obj, dict) and set(obj) == keys, f"{where} must be an object with exactly {sorted(keys)}")


def opt_str(v) -> bool:
    return v is None or isinstance(v, str)


def match(rx, v) -> bool:
    return isinstance(v, str) and rx.fullmatch(v) is not None


def validate(doc) -> dict:
    exact(doc, {"schema", "scope", "members_book", "batches"}, "input")
    need(doc["schema"] == "state-observations/1", "input: unsupported schema")
    scope = doc["scope"]
    exact(scope, {"book", "lanes"}, "scope")
    need(match(LABEL, scope["book"]), "scope.book must be a plain label")
    need(isinstance(scope["lanes"], list) and scope["lanes"] and all(match(LANE, x) for x in scope["lanes"]),
         "scope.lanes must be a non-empty list of lane page names")
    need(len(set(scope["lanes"])) == len(scope["lanes"]), "scope.lanes lists a lane twice")
    need(doc["members_book"] is None or (isinstance(doc["members_book"], str) and os.path.isabs(doc["members_book"])),
         "members_book must be null or absolute")
    need(isinstance(doc["batches"], list), "batches must be a list")
    seen = set()
    for i, o in enumerate(doc["batches"]):
        w = f"batches[{i}]"
        exact(o, OBS_KEYS, w)
        need(match(LANE, o["lane"]) and match(BATCH, o["batch"]), f"{w}: lane or batch has the wrong form")
        need(o["id"] == f"{o['lane']}/{o['batch']}", f"{w}: id must be lane/batch")
        need(o["id"] not in seen, f"{w}: duplicate id {o['id']}")
        seen.add(o["id"])
        need(o["lane"] in scope["lanes"], f"{w}: lane {o['lane']} is outside the declared scope")
        p = o["provenance"]
        exact(p, {"kind", "commit", "page_sha256"}, f"{w}.provenance")
        need(p["kind"] in ("supplied-commit", "supplied-live"), f"{w}.provenance.kind is unknown")
        need((p["kind"] == "supplied-commit") == match(HEX40, p["commit"]) and (p["commit"] is None or match(HEX40, p["commit"])),
             f"{w}.provenance.commit must be 40 hex exactly for supplied-commit")
        need(p["page_sha256"] is None or match(HEX64, p["page_sha256"]), f"{w}.provenance.page_sha256 must be null or 64 hex")
        exact(o["document"], {"header_state"}, f"{w}.document")
        need(opt_str(o["document"]["header_state"]), f"{w}.document.header_state must be a string or null")
        for k, extra in (("release", "text"), ("claim", "actor")):
            exact(o[k], {"status", extra}, f"{w}.{k}")
            need(o[k]["status"] in ("recorded", "pending", "absent") and opt_str(o[k][extra]), f"{w}.{k} has a wrong value")
        r = o["return"]
        exact(r, {"pointer", "members", "candidate"}, f"{w}.return")
        need(r["pointer"] in ("present", "pending", "absent", "ambiguous"), f"{w}.return.pointer is unknown")
        need(isinstance(r["members"], list) and all(match(MEMBER, m) for m in r["members"]), f"{w}.return.members must be member names")
        need(len(set(r["members"])) == len(r["members"]), f"{w}.return.members lists a member twice")
        need(r["candidate"] is None or (match(MEMBER, r["candidate"]) and r["candidate"] in r["members"]),
             f"{w}.return.candidate must be null or one of members")
        v = o["review"]
        exact(v, {"status", "text", "binding"}, f"{w}.review")
        need(v["status"] in ("absent", "pending", "text", "bound") and opt_str(v["text"]), f"{w}.review has a wrong value")
        b = v["binding"]
        need((v["status"] == "bound") == (b is not None), f"{w}.review.binding is required exactly when status is bound")
        if b is not None:
            exact(b, {"member", "receipt_sha256", "disposition", "terminal", "reviewer", "followup"}, f"{w}.review.binding")
            need(match(MEMBER, b["member"]) and match(HEX64, b["receipt_sha256"]), f"{w}.review.binding member/receipt has the wrong form")
            need(b["disposition"] in ("accepted", "held", "correction-required"), f"{w}.review.binding.disposition is unknown")
            need(b["terminal"] in ("completed", None), f"{w}.review.binding.terminal must be completed or null")
            need(match(LABEL, b["reviewer"]) and opt_str(b["followup"]), f"{w}.review.binding reviewer/followup has the wrong form")
        pub = o["publication"]
        exact(pub, {"status", "ref", "commit"}, f"{w}.publication")
        need(pub["status"] in ("unknown", "at-ref") and opt_str(pub["ref"]) and (pub["commit"] is None or match(HEX40, pub["commit"])),
             f"{w}.publication has a wrong value")
    return doc


# ---------- pinned inspector ----------

def plain_sha(path: Path) -> str | None:
    try:
        st = os.lstat(path)
    except OSError:
        return None
    if not stat.S_ISREG(st.st_mode) or (getattr(st, "st_file_attributes", 0) or 0) & 0x400:
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins() -> Path:
    inspector, helper = RC_DIR / "return_inspect.py", RC_DIR / "return_capture.py"
    for name, path in (("return_inspect", inspector), ("return_capture", helper)):
        got = plain_sha(path)
        if got != PINS[name]:
            raise Refusal(f"{name} at {path} is not the pinned code (sha256 {got}); nothing was launched")
    return inspector


def inspect(members_book: str, member: str) -> dict:
    inspector = check_pins()  # before every launch
    observed_at = now()
    proc = subprocess.run([sys.executable, "-I", "-B", str(inspector), "inspect", "--book", members_book, "--member", member,
                           "--json"], capture_output=True, timeout=120, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    rec = {"member": member, "observed_at": observed_at, "basis": "live", "exit": proc.returncode,
           "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(), "status": None, "origin": None, "receipt_sha256": None,
           "retrospective": None, "observation": "ok"}
    try:
        d = strict_json(proc.stdout, "inspector report")
    except Refusal as exc:
        return dict(rec, observation="failed", reason=str(exc))
    if proc.stderr or not isinstance(d, dict) or d.get("schema") != INSPECTION_SCHEMA or d.get("member") != member \
            or d.get("status") not in INSPECTION_EXIT or INSPECTION_EXIT.get(d.get("status")) != proc.returncode:
        return dict(rec, observation="failed", reason="inspector report failed interface checks")
    cap = d.get("capture") if isinstance(d.get("capture"), dict) else None
    origin = (cap or {}).get("origin") if cap else None
    if d["status"] == "complete" and (not isinstance(origin, dict) or not all(isinstance(origin.get(k), str) for k in ("book", "page", "batch"))
                                      or not match(HEX64, cap.get("receipt_sha256"))):
        return dict(rec, observation="failed", reason="complete report lacks a usable origin or receipt")
    return dict(rec, status=d["status"], origin=origin, receipt_sha256=(cap or {}).get("receipt_sha256"),
                retrospective=(cap or {}).get("retrospective"))


# ---------- projection ----------

def custody(o: dict, scope_book: str, inspections: list[dict] | None) -> dict:
    r = o["return"]
    out = {"pointer": r["pointer"], "members_named": r["members"], "candidate_declared": r["candidate"],
           "custody": "not-observed", "primary": None, "primary_receipt_sha256": None, "secondary": [], "ambiguous": [],
           "problems": []}
    if inspections is None or not r["members"]:
        if inspections is not None and not r["members"]:
            out["custody"] = "none"
        return out
    want = {"book": scope_book, "page": o["lane"], "batch": o["batch"]}
    matching, failed = [], []
    for ins in inspections:
        if ins["observation"] != "ok":
            failed.append(ins["member"])
        elif ins["status"] == "complete" and ins["origin"] == want:
            matching.append(ins)
        elif ins["status"] == "complete":
            out["secondary"].append({"member": ins["member"], "origin": ins["origin"], "retrospective": ins["retrospective"]})
        else:
            out["problems"].append(f"{ins['member']}: {ins['status']}")
    out["problems"] += [f"{m}: observation failed" for m in failed]
    cand = r["candidate"]
    if cand is not None:
        hit = next((m for m in matching if m["member"] == cand), None)
        if hit is None:
            out["custody"] = "candidate-mismatch"
            return out
        out.update(custody="primary", primary=cand, primary_receipt_sha256=hit["receipt_sha256"])
    elif len(matching) == 1:
        out.update(custody="primary", primary=matching[0]["member"], primary_receipt_sha256=matching[0]["receipt_sha256"])
    elif len(matching) > 1:
        out.update(custody="ambiguous", ambiguous=[m["member"] for m in matching])
    elif failed and not out["secondary"]:
        out["custody"] = "observation-failed"
    else:
        out["custody"] = "none"
    return out


def project_batch(o: dict, scope_book: str, inspections: list[dict] | None) -> dict:
    commit_basis = o["provenance"]["kind"] == "supplied-commit"
    live = custody(o, scope_book, inspections)
    ret = live if not commit_basis else dict(live, custody="not-verifiable-here", primary=None, primary_receipt_sha256=None,
                                              secondary=[], ambiguous=[], problems=[])
    v, b = o["review"], o["review"]["binding"]
    review = {"status": v["status"], "text": v["text"], "binding_check": None, "disposition": None, "terminal": None,
              "reviewer": None, "followup": None}
    if b is not None:
        review.update(disposition=b["disposition"], terminal=b["terminal"], reviewer=b["reviewer"], followup=b["followup"])
        if live["custody"] != "primary":
            review["binding_check"] = "unverifiable"
        elif b["member"] == live["primary"] and b["receipt_sha256"] == live["primary_receipt_sha256"]:
            review["binding_check"] = "current"
        else:
            review["binding_check"] = "stale"
    attention = []
    rel = o["release"]["status"] == "recorded"
    activity = o["claim"]["status"] == "recorded" or o["return"]["pointer"] == "present" or v["status"] in ("text", "bound")
    bc = review["binding_check"]
    if not rel and activity:
        life = "conflict-missing-release"
        attention.append("execution evidence without a recorded release; no release is inferred")
    elif not rel:
        life = "unreleased"
    elif b is not None and b["terminal"] == "completed" and b["disposition"] != "accepted":
        life = "conflict-contradictory-review"
        attention.append("a terminal completion with a non-accepted disposition")
    elif live["custody"] == "candidate-mismatch":
        life = "conflict-candidate"
        attention.append("the declared candidate is not a complete member with this origin book/page/batch")
    elif bc == "stale":
        life = "open-re-review-required"
        attention.append("the bound review names a different member or receipt than the current primary")
    elif bc == "current" and b["disposition"] in ("held", "correction-required"):
        life = "open-held" if b["disposition"] == "held" else "open-correction-required"
        attention.append(f"review {b['disposition']}; the item stays open until an explicit resolution")
    elif bc == "current" and b["disposition"] == "accepted" and b["terminal"] == "completed":
        if commit_basis:
            life = "open-commit-custody-unverified"
            attention.append("commit-time custody cannot be established by a live inspection")
        else:
            life = "completed"
    elif bc == "current" and b["disposition"] == "accepted":
        life = "open-accepted-not-terminal"
        attention.append("accepted without an explicit terminal declaration")
    elif v["status"] == "text" or bc == "unverifiable":
        life = "open-review-unresolved"
        attention.append("review present without a validated candidate binding; nothing is closed")
    elif live["custody"] == "ambiguous" and not commit_basis:
        life = "open-candidate-ambiguous"
        attention.append("more than one complete member matches origin; no explicit candidate")
    elif o["return"]["pointer"] in ("present", "ambiguous"):
        life = "returned-awaiting-review"
    elif o["claim"]["status"] == "recorded":
        life = "claimed"
    else:
        life = "released"
    if live["custody"] == "ambiguous" and life != "open-candidate-ambiguous":
        attention.append("candidate ambiguous")
    if o["return"]["pointer"] == "ambiguous":
        attention.append("return pointer ambiguous in the supplied observation")
    attention += [f"custody: {p}" for p in live["problems"]]
    if o["publication"]["status"] == "at-ref" and life != "completed":
        attention.append("published bytes at a ref do not complete work")
    return {"id": o["id"], "lane": o["lane"], "batch": o["batch"], "provenance": o["provenance"],
            "facets": {"document": o["document"], "release": o["release"], "claim": o["claim"], "return": ret,
                       "review": review, "publication": o["publication"]},
            "live_custody": live if commit_basis and inspections is not None else None,
            "inspections": inspections, "lifecycle": life, "attention": attention, "followup": review["followup"]}


def project(doc: dict, do_inspect: bool, input_sha: str) -> dict:
    validate(doc)
    if do_inspect and any(o["return"]["members"] for o in doc["batches"]):
        need(doc["members_book"] is not None, "members_book is required with --inspect when members are named")
        check_pins()
    rows = []
    for o in doc["batches"]:
        ins = [inspect(doc["members_book"], m) for m in o["return"]["members"]] if do_inspect else None
        rows.append(project_batch(o, doc["scope"]["book"], ins))
    lanes = {lane: {"open": [], "awaiting_release": [], "completed": [], "conflicts": []} for lane in doc["scope"]["lanes"]}
    for r in rows:
        bucket = ("completed" if r["lifecycle"] == "completed" else "awaiting_release" if r["lifecycle"] == "unreleased"
                  else "conflicts" if r["lifecycle"].startswith("conflict") else "open")
        lanes[r["lane"]][bucket].append(r["id"])
    return {"schema": "state-projection/1", "tool": {"path": str(Path(__file__).resolve()),
                                                     "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            "input_sha256": input_sha, "scope": doc["scope"], "projected_at": now(), "inspected": do_inspect,
            "batches": rows, "lanes": lanes, "attention_count": sum(len(r["attention"]) for r in rows),
            "authority": AUTHORITY, "note": NOTE}


def view(p: dict) -> str:
    out = [f"state-projection/1  scope {p['scope']['book']}  inspected {p['inspected']}  ({NOTE})"]
    for r in p["batches"]:
        f = r["facets"]
        out.append(f"{r['id']}  {r['lifecycle']}  [{r['provenance']['kind']}]  release {f['release']['status']}  "
                   f"claim {f['claim']['status']}  custody {f['return']['custody']}  review {f['review']['status']}"
                   f"{'/' + f['review']['binding_check'] if f['review']['binding_check'] else ''}  publication {f['publication']['status']}")
        out += [f"    ! {a}" for a in r["attention"]]
        if r["followup"]:
            out.append(f"    followup: {r['followup']}")
    for lane, buckets in p["lanes"].items():
        out.append(f"lane {lane}: " + "; ".join(f"{k} {v}" for k, v in buckets.items()))
    out.append(f"authority {AUTHORITY}")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(prog="state_projection.py")
    sub = ap.add_subparsers(dest="command", required=True)
    pr = sub.add_parser("project")
    pr.add_argument("--input", required=True)
    pr.add_argument("--inspect", action="store_true")
    pr.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        raw = Path(args.input).read_bytes()
        result = project(strict_json(raw, "input"), args.inspect, hashlib.sha256(raw).hexdigest())
    except Refusal as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except OSError as exc:
        sys.stdout.write(f"refused: filesystem error: {type(exc).__name__}: {exc.strerror}\n")
        return 2
    sys.stdout.write(json.dumps(result, indent=1, ensure_ascii=False) + "\n" if args.json else view(result))
    return 1 if result["attention_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
