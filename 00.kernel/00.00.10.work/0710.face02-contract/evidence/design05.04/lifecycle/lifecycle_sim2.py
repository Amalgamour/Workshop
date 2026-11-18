#!/usr/bin/env python3
"""0710/05.04 NONPRODUCTION lifecycle simulator, successor of design05.03 lifecycle_sim.py.

Repairs Prime's 06.03 findings:
- L-P1: restart never trusts a step label. It derives the state from the actual file hashes
  and the recorded plan, including after completion. Unknown states and malformed journals hold.
- L-P2: rollback needs a SYNTHETIC Director decision bound to the current identities, and a full
  preflight runs before the first rename. It is journaled and restartable, and it restores from
  raw retained before-images, not reconstructed stamps.
Held operations write nothing (checked by a tree hash). The ledger is append-only and typed.
Fixture pages only. Not a seating tool. Lock and promote are refused.
usage: lifecycle_sim2.py --runs DIR(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
T = json.loads((HERE / "lifecycle2.template.json").read_text(encoding="utf-8"))
STAGES = {s["id"]: s for s in T["stages"]}
MUTABLE = tuple(T["mechanical_transitions"]["mutable_stamp_lines"])
PAGES = {"0001.law": "law", "0002.schema": "schema"}
DATE = "2026-11-02"
SEAT_STEPS = [s["id"] for s in T["seat_steps"]]
ROLL_STEPS = [s["id"] for s in T["rollback_steps"]]


class Stop(Exception):
    def __init__(self, outcome, code, detail, extra=None):
        super().__init__(detail)
        self.outcome, self.code, self.detail, self.extra = outcome, code, detail, extra or {}


class Crash(Exception):
    pass


def sha(b: bytes | None) -> str | None:
    return None if b is None else hashlib.sha256(b).hexdigest()


def header_end(b: bytes) -> int:
    i = b.find(b"\r\n## ")
    return len(b) if i < 0 else i


def content_sha(b: bytes) -> str:
    h, rest = b[:header_end(b)], b[header_end(b):]
    kept = b"\r\n".join(l for l in h.split(b"\r\n") if not any(l.startswith(k.encode() + b":") for k in MUTABLE))
    return sha(kept + rest)


def stamp(b: bytes, values: dict) -> bytes:
    h, rest = b[:header_end(b)], b[header_end(b):]
    out = []
    for l in h.split(b"\r\n"):
        k = next((k for k in MUTABLE if l.startswith(k.encode() + b":")), None)
        out.append(f"{k}: {values[k]}".encode() if k else l)
    nb = b"\r\n".join(out) + rest
    if content_sha(nb) != content_sha(b):
        raise Stop("refused", "transition-not-mechanical", "a stamp change altered content")
    return nb


def face(page, version, auth, state, body):
    lines = ["# 01", "", f"version: {version}", f"Authorization: {auth}", f"state: {state}", "Face: 01",
             f"PPPP: {page[:4]}", "book: 00.00.01.law", f"keyword: {PAGES[page]}", "", "## Job", "", body, ""]
    return "\r\n".join(lines).encode("utf-8")


def read(p: Path) -> bytes | None:
    return p.read_bytes() if p.is_file() else None


def replace_with(path: Path, data: bytes, crash_mid: bool = False) -> None:
    tmp = path.with_name(path.name + ".partial")
    with open(tmp, "xb") as f:
        f.write(data)
    if crash_mid:
        raise Crash("stopped after the partial write, before replace")
    os.replace(tmp, path)


class Book:
    def __init__(self, root: Path, layout="paged"):
        self.root, self.layout = root, layout
        self.law = root / "book" / "00.00.01.law"
        self.rec = root / "records"
        (self.rec / "images").mkdir(parents=True)
        self.inbox = root / "inbox"
        self.inbox.mkdir()
        self.reviewed = {}
        for p in PAGES:
            d = self.law / p
            d.mkdir(parents=True)
            (d / "01.md").write_bytes(face(p, "004", "approved — 2026-10-10", "approved", f"SYNTHETIC seat body of {p}."))
            cand = face(p, "005", f"draft — {DATE}", "draft. SYNTHETIC candidate.", f"SYNTHETIC candidate body of {p}, changed.")
            (self.inbox / f"{p}.candidate.md").write_bytes(cand)
            self.reviewed[p] = sha(cand)
        self.source_seat = {p: sha((self.law / p / "01.md").read_bytes()) for p in PAGES}

    # ---- records, images, ledger ----
    def put(self, b: bytes) -> str:
        h = sha(b)
        f = self.rec / "images" / f"{h}.bin"
        if not f.exists():
            f.write_bytes(b)
        return h

    def image(self, h: str) -> bytes:
        f = self.rec / "images" / f"{h}.bin"
        b = read(f)
        if b is None or sha(b) != h:
            raise Stop("held", "before-image-missing", f"raw image {h[:12]} is missing or damaged; no write")
        return b

    def r(self, p):
        f = self.rec / f"{p}.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

    def save(self, p, d):
        (self.rec / f"{p}.json").write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8")

    def ledger(self, kind, p, detail):
        led = self.law / "00.retire.09" / "09.md"
        led.parent.mkdir(parents=True, exist_ok=True)
        with open(led, "ab") as f:
            f.write(f"{kind}: {p}/01.md (version 004) · {detail} · {DATE}\n".encode())

    def ledger_lines(self):
        led = self.law / "00.retire.09" / "09.md"
        return led.read_text(encoding="utf-8").splitlines() if led.exists() else []

    def tree(self) -> str:
        rows = [f"{q.relative_to(self.root).as_posix()} {sha(q.read_bytes())}" for q in sorted(self.root.rglob("*")) if q.is_file()]
        return sha("\n".join(rows).encode())

    def paths(self, p):
        wh = (self.law / "00.retire.09" / p / "01.004.09.md") if self.layout == "paged" else (self.law / "00.retire.09" / "01.004.09.md")
        return self.law / p / "01.md", wh, self.law / p / "01.005.md"

    # ---- preconditions named by the template ----
    def check(self, name, p, ctx):
        r = self.r(p)
        seat, wh, d = self.paths(p)
        cur = read(d)
        fns = {
            "candidate-matches-reviewed": lambda: sha(read(self.inbox / f"{p}.candidate.md")) == self.reviewed[p],
            "seat-matches-source": lambda: sha(read(seat)) == self.source_seat[p],
            "draft-name-free": lambda: not d.exists(),
            "staged": lambda: "stage" in r,
            "draft-bytes-equal-staged": lambda: sha(cur) == r["stage"]["staged_sha256"],
            "align-checks": lambda: cur is not None and all(re.search(rf"^{k}: ".encode(), cur, re.M) for k in ("version", "Authorization", "state", "Face", "PPPP", "book", "keyword"))
                                     and len(re.findall(rb"^## (.+)$", cur, re.M)) == len(set(re.findall(rb"^## (.+)$", cur, re.M))),
            "signed": lambda: "sign" in r,
            "approval-names-signed-sha": lambda: ctx.get("approval", {}).get("approved_sha256") == r.get("sign", {}).get("signed_sha256"),
            "draft-bytes-equal-signed": lambda: sha(cur) == r.get("sign", {}).get("signed_sha256"),
            "approved": lambda: "approve" in r,
            "draft-bytes-equal-approved": lambda: sha(cur) == r.get("approve", {}).get("approved_sha256"),
            "seat-unchanged": lambda: sha(read(seat)) == self.source_seat[p],
            "warehouse-name-free": lambda: not wh.exists(),
            "pair-approved": lambda: all("approve" in self.r(q) for q in ctx["release"]),
        }
        if name not in fns:
            raise Stop("refused", "unknown-precondition", f"template names {name}, which compute does not implement")
        return fns[name]()

    def require(self, stage, p, ctx):
        for name in STAGES[stage]["requires"]:
            if not self.check(name, p, ctx):
                held = {"approved": "approval-missing", "pair-approved": "approval-missing"}.get(name)
                raise Stop("held" if held else "refused", held or name, f"{stage} {p}: precondition {name} failed")

    # ---- stage, sign, approve ----
    def stage(self, p):
        self.require("stage", p, {})
        b = read(self.inbox / f"{p}.candidate.md")
        _, _, d = self.paths(p)
        with open(d, "xb") as f:
            f.write(b)
        self.save(p, {"stage": {"staged_sha256": self.put(b), "content_sha256": content_sha(b), "source_seat_sha256": self.source_seat[p]}})

    def sign(self, p):
        self.require("sign", p, {})
        _, _, d = self.paths(p)
        b = d.read_bytes()
        nb = stamp(b, {"Authorization": f"signed — {DATE}", "state": "signed. claude-opus-5-5 (fixture); compute checks passed. Not approved."})
        replace_with(d, nb)
        r = self.r(p)
        r["sign"] = {"pre_sign_sha256": self.put(b), "signed_sha256": self.put(nb), "content_sha256": content_sha(nb)}
        self.save(p, r)

    def approve(self, p, approved_sha=None):
        r = self.r(p)
        appr = {"by": "Director (SYNTHETIC fixture record)", "ref": "fixture", "approved_sha256": approved_sha or r.get("sign", {}).get("signed_sha256")}
        self.require("approve", p, {"approval": appr})
        r["approve"] = appr
        self.save(p, r)

    # ---- seat: plan, then hash-derived steps ----
    def plan(self, p):
        seat, wh, d = self.paths(p)
        before, draft = seat.read_bytes(), d.read_bytes()
        retired = stamp(before, {"Authorization": f"retired — {DATE}, by version 005", "state": "retired"})
        seated = stamp(draft, {"Authorization": f"approved — {DATE}", "state": "approved"})
        return {"seat_file": seat.relative_to(self.law).as_posix(), "warehouse_file": wh.relative_to(self.law).as_posix(),
                "draft_file": d.relative_to(self.law).as_posix(), "before": self.put(before), "approved": self.put(draft),
                "retired": self.put(retired), "seated": self.put(seated)}

    def observe(self, plan):
        return tuple(sha(read(self.law / plan[k])) for k in ("seat_file", "warehouse_file", "draft_file"))

    def seat_state(self, plan):
        o = self.observe(plan)
        table = {(plan["before"], None, plan["approved"]): "S-ready", (None, plan["before"], plan["approved"]): "S-moved",
                 (None, plan["retired"], plan["approved"]): "S-retired", (plan["approved"], plan["retired"], None): "S-installed",
                 (plan["seated"], plan["retired"], None): "S-seated"}
        return table.get(o), o

    def seat(self, release, crash=None):
        ctx = {"release": release}
        if not all(self.check("pair-approved", q, ctx) for q in release):
            raise Stop("held", "approval-missing", "the release has a face without an approval; nothing renamed")
        done = []
        for p in release:
            try:
                self.require("seat", p, ctx)
                r = self.r(p)
                r["seat"] = {"plan": self.plan(p), "journal": [{"step": "J1", "status": "done"}]}
                self.save(p, r)
                if crash == ("J1", "after"):
                    raise Crash("stopped after J1")
                self.advance(p, crash)
            except Stop as s:
                if done:
                    raise Stop("held", "half-seated", f"seated {done}; {p} stopped at {s.code}; Director decides finish or rollback")
                raise
            done.append(p)
        return done

    def journal_ok(self, r, key, steps):
        j = r.get(key, {})
        plan = j.get("plan")
        need = {"seat_file", "warehouse_file", "draft_file", "before", "approved", "retired", "seated"}
        if not isinstance(plan, dict) or set(plan) != need or not isinstance(j.get("journal"), list):
            raise Stop("held", "journal-malformed", f"{key} record is missing or malformed; nothing guessed, no write")
        for e in j["journal"]:
            if not isinstance(e, dict) or e.get("step") not in steps or e.get("status") not in ("done",):
                raise Stop("held", "journal-malformed", f"unknown journal entry {e}; no write")
        return plan

    def advance(self, p, crash=None):
        """Move a seating forward from whatever state the hashes show. Used for the first run and for restart."""
        r = self.r(p)
        plan = self.journal_ok(r, "seat", SEAT_STEPS)
        seat, wh, d = (self.law / plan[k] for k in ("seat_file", "warehouse_file", "draft_file"))
        steps_done = [e["step"] for e in r["seat"]["journal"]]
        for _ in range(8):
            state, obs = self.seat_state(plan)
            leftover = [q for q in (seat.with_name(seat.name + ".partial"), wh.with_name(wh.name + ".partial")) if q.exists()]
            for q in leftover:
                want = plan["retired"] if q.name.startswith("01.004.09") else plan["seated"]
                if sha(q.read_bytes()) != want or state not in ("S-moved", "S-installed"):
                    raise Stop("held", "restart-state-unknown", f"partial file {q.name} does not match the plan; no write")
            if state is None:
                raise Stop("held", "completed-drift" if "J7" in steps_done else "restart-state-unknown",
                           "observed hashes match no planned state; no write", {"observed": [x and x[:12] for x in obs]})
            if state == "S-ready":
                if "J2" not in steps_done:
                    self.ledger("planned", p, f"to {plan['warehouse_file']} · before {plan['before'][:12]} · retired {plan['retired'][:12]}")
                    self.mark(p, "J2"); steps_done.append("J2")
                    if crash == ("J2", "after"): raise Crash("stopped after J2")
                if wh.exists():
                    raise Stop("held", "warehouse-name-taken", f"{plan['warehouse_file']} is occupied; no write")
                wh.parent.mkdir(parents=True, exist_ok=True)
                os.rename(seat, wh)
                if crash == ("J3", "action"): raise Crash("stopped after the J3 move")
                self.mark(p, "J3"); steps_done.append("J3")
            elif state == "S-moved":
                pending = wh.with_name(wh.name + ".partial")
                if pending.exists():
                    os.replace(pending, wh)
                else:
                    replace_with(wh, self.image(plan["retired"]), crash_mid=crash == ("J4", "mid"))
                if crash == ("J4", "action"): raise Crash("stopped after the J4 write")
                self.mark(p, "J4"); steps_done.append("J4")
            elif state == "S-retired":
                os.rename(d, seat)
                if crash == ("J5", "action"): raise Crash("stopped after the J5 move")
                self.mark(p, "J5"); steps_done.append("J5")
            elif state == "S-installed":
                pending = seat.with_name(seat.name + ".partial")
                if pending.exists():
                    os.replace(pending, seat)
                else:
                    replace_with(seat, self.image(plan["seated"]), crash_mid=crash == ("J6", "mid"))
                if crash == ("J6", "action"): raise Crash("stopped after the J6 write")
                self.mark(p, "J6"); steps_done.append("J6")
            elif state == "S-seated":
                if "J7" in steps_done:
                    return "verified-complete"
                if not any(l.startswith("retired:") and p in l for l in self.ledger_lines()):
                    self.ledger("retired", p, f"at {plan['warehouse_file']} · retired {plan['retired'][:12]} · seated {plan['seated'][:12]}")
                self.mark(p, "J7")
                return "completed"
        raise Stop("held", "restart-state-unknown", "no progress; no write")

    def mark(self, p, step, key="seat"):
        r = self.r(p)
        r[key]["journal"].append({"step": step, "status": "done"})
        self.save(p, r)

    def restart(self, p, crash=None):
        return self.advance(p, crash)

    # ---- rollback ----
    def roll_state(self, plan):
        o = self.observe(plan)
        table = {(plan["seated"], plan["retired"], None): "R-ready", (None, plan["retired"], plan["seated"]): "R-moved",
                 (None, plan["retired"], plan["approved"]): "R-draft", (plan["retired"], None, plan["approved"]): "R-returned",
                 (plan["before"], None, plan["approved"]): "R-restored"}
        return table.get(o), o

    def rollback(self, p, decision, crash=None):
        before_tree = self.tree()
        r = self.r(p)
        plan = self.journal_ok(r, "seat", SEAT_STEPS)
        try:
            if not decision:
                raise Stop("held", "rollback-decision-missing", "no Director rollback decision; no write")
            want = {"page": p, "seated_sha256": plan["seated"], "retired_sha256": plan["retired"], "restore_seat_sha256": plan["before"], "restore_draft_sha256": plan["approved"]}
            if any(decision.get(k) != v for k, v in want.items()):
                raise Stop("held", "rollback-decision-mismatch", "the decision names other identities; no write")
            if "rollback" not in r:
                state, obs = self.roll_state(plan)
                if state != "R-ready":
                    seat_now, wh_now, d_now = obs
                    code = ("rollback-current-changed" if seat_now != plan["seated"] else
                            "rollback-retired-changed" if wh_now != plan["retired"] else "destination-occupied")
                    raise Stop("held", code, "current bytes or destinations differ from the plan; Director review; no write",
                               {"observed": [x and x[:12] for x in obs]})
                self.image(plan["before"]); self.image(plan["approved"])
                r["rollback"] = {"decision": decision, "journal": [{"step": "R1", "status": "done"}]}
                self.save(p, r)
                self.ledger("rollback-planned", p, f"seated {plan['seated'][:12]} -> draft; retired {plan['retired'][:12]} -> seat")
                if crash == ("R1", "after"):
                    raise Crash("stopped after R1")
        except Stop as s:
            if self.tree() != before_tree:
                raise Stop("refused", "held-but-wrote", f"{s.code} changed files")
            raise
        return self.roll_advance(p, crash)

    def roll_advance(self, p, crash=None):
        r = self.r(p)
        plan = r["seat"]["plan"]
        seat, wh, d = (self.law / plan[k] for k in ("seat_file", "warehouse_file", "draft_file"))
        for _ in range(6):
            state, obs = self.roll_state(plan)
            if state is None:
                raise Stop("held", "rollback-state-unknown", "observed hashes match no rollback state; no write", {"observed": [x and x[:12] for x in obs]})
            if state == "R-ready":
                if d.exists():
                    raise Stop("held", "destination-occupied", "draft name is occupied; no write")
                os.rename(seat, d)
                if crash == ("R2", "action"): raise Crash("stopped after the R2 move")
                self.mark(p, "R2", "rollback")
            elif state == "R-moved":
                replace_with(d, self.image(plan["approved"]))
                if crash == ("R3", "action"): raise Crash("stopped after the R3 write")
                self.mark(p, "R3", "rollback")
            elif state == "R-draft":
                if seat.exists():
                    raise Stop("held", "destination-occupied", "seat name is occupied; no write")
                os.rename(wh, seat)
                if crash == ("R4", "action"): raise Crash("stopped after the R4 move")
                self.mark(p, "R4", "rollback")
            elif state == "R-returned":
                replace_with(seat, self.image(plan["before"]))
                if crash == ("R5", "action"): raise Crash("stopped after the R5 write")
                self.mark(p, "R5", "rollback")
            elif state == "R-restored":
                if not any(l.startswith("rolled-back:") and p in l for l in self.ledger_lines()):
                    self.ledger("rolled-back", p, f"seat restored {plan['before'][:12]} · draft restored {plan['approved'][:12]} · seated version kept as image {plan['seated'][:12]}")
                return {"seat_restored": sha(read(seat)) == plan["before"], "draft_restored": sha(read(d)) == plan["approved"],
                        "seated_image_kept": (self.rec / "images" / f"{plan['seated']}.bin").exists()}
        raise Stop("held", "rollback-state-unknown", "no progress")

    def roll_restart(self, p, crash=None):
        r = self.r(p)
        if "rollback" not in r:
            raise Stop("held", "journal-malformed", "no rollback journal")
        return self.roll_advance(p, crash)


def decision_for(b: Book, p: str, **override):
    plan = b.r(p)["seat"]["plan"]
    d = {"by": "Director (SYNTHETIC fixture decision)", "page": p, "seated_sha256": plan["seated"], "retired_sha256": plan["retired"],
         "restore_seat_sha256": plan["before"], "restore_draft_sha256": plan["approved"]}
    d.update(override)
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    runs = Path(ap.parse_args().runs)
    runs.mkdir(parents=True, exist_ok=False)
    rows = []
    rel = list(PAGES)
    P = "0001.law"

    def prep(name, layout="paged", sign=True, approve=True, seat=False):
        b = Book(runs / name, layout)
        for p in PAGES:
            b.stage(p)
            if sign:
                b.sign(p)
            if approve:
                b.approve(p)
        if seat:
            b.seat(rel)
        return b

    def case(cid, says, expect, fn, nowrite=None):
        b_holder = {}
        try:
            got = {"outcome": "ok", "code": "ok", "detail": fn(b_holder)}
        except Stop as s:
            got = {"outcome": s.outcome, "code": s.code, "detail": s.detail, **s.extra}
        except Crash as c:
            got = {"outcome": "crash", "code": "unexpected-crash", "detail": str(c)}
        if nowrite and "tree" in b_holder:
            got["no_write"] = b_holder["book"].tree() == b_holder["tree"]
        match = (got["outcome"], got["code"]) == expect and (not nowrite or got.get("no_write") is True)
        rows.append({"id": cid, "says": says, "expect": list(expect), "actual": got, "match": match})
        print(f"{'PASS' if match else 'FAIL'} {cid:<6} {says[:70]:<70} -> {got['outcome']}/{got['code']}{' no-write' if got.get('no_write') else ''}")

    # carried from 05.03, re-expressed
    def l1(h):
        b = prep("L1", seat=True)
        return {"warehouse": sorted(q.relative_to(b.law).as_posix() for q in (b.law / "00.retire.09").rglob("*.md")), "ledger": b.ledger_lines(),
                "restart": [b.restart(p) for p in rel]}
    case("L1", "pair seats; no collision; completed restart re-verifies", ("ok", "ok"), l1)

    def l2(h):
        b = prep("L2", approve=False)
        _, _, d = b.paths(P)
        d.write_bytes(d.read_bytes().replace(b"changed.", b"changed again."))
        b.approve(P)
    case("L2", "content changed after signing: approval refused", ("refused", "draft-bytes-equal-signed"), l2)

    def l2b(h):
        b = prep("L2b")
        _, _, d = b.paths("0002.schema")
        d.write_bytes(d.read_bytes().replace(b"changed.", b"changed after approval."))
        b.seat(rel)
    case("L2b", "content changed after approval: half-seated, held", ("held", "half-seated"), l2b)

    def l3(h):
        b = prep("L3", approve=False)
        b.approve(P)
        h.update(book=b, tree=b.tree())
        b.seat(rel)
    case("L3", "missing approval: held, nothing written", ("held", "approval-missing"), l3, nowrite=True)

    def l5(h):
        b = prep("L5")
        s, _, _ = b.paths("0002.schema")
        s.write_bytes(s.read_bytes() + b"edited seat\r\n")
        b.seat(rel)
    case("L5", "second seat changed after approval: half-seated", ("held", "half-seated"), l5)

    def l7(h):
        b = Book(runs / "L7")
        b.stage(P)
        b.seat([P])
    case("L7", "seat before sign/approve: held", ("held", "approval-missing"), l7)

    def l7b(h):
        Book(runs / "L7b").sign(P)
    case("L7b", "sign before stage: refused", ("refused", "staged"), l7b)

    def l8(h):
        b = prep("L8", approve=False)
        b.approve(P, approved_sha=b.r(P)["stage"]["staged_sha256"])
    case("L8", "approval names the pre-sign bytes: refused", ("refused", "approval-names-signed-sha"), l8)

    def l9(h):
        if "lock" not in STAGES:
            raise Stop("refused", "not-in-template", "lock and promote are separate (0023)")
    case("L9", "lock or promote requested", ("refused", "not-in-template"), l9)

    def l10(h):
        prep("L10", layout="flat").seat(rel)
    case("L10", "flat warehouse: collision; half-seated", ("held", "half-seated"), l10)

    # Prime's two probes, exactly
    def pp1(h):
        b = prep("PP1", seat=True)
        s, _, _ = b.paths(P)
        s.write_bytes(s.read_bytes() + b"TAMPERED AFTER COMPLETE\r\n")
        h.update(book=b, tree=b.tree())
        return b.restart(P)
    case("PP1", "Prime L-P1: completed restart after changed seated bytes", ("held", "completed-drift"), pp1, nowrite=True)

    def pp2(h):
        b = prep("PP2", seat=True)
        s, _, _ = b.paths(P)
        s.write_bytes(s.read_bytes() + b"TAMPERED AFTER COMPLETE\r\n")
        h.update(book=b, tree=b.tree())
        return b.rollback(P, decision_for(b, P))
    case("PP2", "Prime L-P2: rollback after changed seated bytes", ("held", "rollback-current-changed"), pp2, nowrite=True)

    # interruption windows: crash at every seat point, then restart
    windows = [("J1", "after"), ("J2", "after"), ("J3", "action"), ("J4", "mid"), ("J4", "action"), ("J5", "action"), ("J6", "mid"), ("J6", "action")]
    ref = None
    for i, w in enumerate(windows, 1):
        def cw(h, w=w, i=i):
            nonlocal ref
            b = prep(f"W{i}")
            try:
                b.seat([P], crash=w)
                raise Stop("refused", "no-crash", "crash point not reached")
            except Crash:
                pass
            res = b.restart(P)
            s, wh, _ = b.paths(P)
            final = (sha(read(s)), sha(read(wh)))
            ref = ref or final
            if final != ref:
                raise Stop("refused", "final-differs", "restart ended in a different state")
            planned = [l for l in b.ledger_lines() if l.startswith("planned:")]
            retired = [l for l in b.ledger_lines() if l.startswith("retired:")]
            if len(planned) != 1 or len(retired) != 1:
                raise Stop("refused", "ledger-wrong", f"{b.ledger_lines()}")
            return res
        case(f"W{i}", f"stop at {w[0]} {w[1]}; restart completes to the same bytes; ledger planned+retired once", ("ok", "ok"), cw)

    def lg1(h):
        b = prep("LG1")
        try:
            b.seat([P], crash=("J2", "after"))
        except Crash:
            pass
        lines = b.ledger_lines()
        if any(l.startswith("retired:") for l in lines) or not any(l.startswith("planned:") for l in lines):
            raise Stop("refused", "ledger-implies-move", f"{lines}")
        return lines
    case("LG1", "stop after J2: ledger says planned, never retired", ("ok", "ok"), lg1)

    def m1(h):
        b = prep("M1")
        try:
            b.seat([P], crash=("J3", "action"))
        except Crash:
            pass
        r = b.r(P)
        r["seat"]["journal"].append({"step": "J9", "status": "done"})
        b.save(P, r)
        h.update(book=b, tree=b.tree())
        return b.restart(P)
    case("M1", "malformed journal entry: held, no write", ("held", "journal-malformed"), m1, nowrite=True)

    def m2(h):
        b = prep("M2")
        try:
            b.seat([P], crash=("J3", "action"))
        except Crash:
            pass
        _, _, d = b.paths(P)
        d.unlink()
        h.update(book=b, tree=b.tree())
        return b.restart(P)
    case("M2", "draft removed during interruption: unknown state held", ("held", "restart-state-unknown"), m2, nowrite=True)

    # rollback cases
    def rb_ok(h):
        b = prep("RB0", seat=True)
        return b.rollback(P, decision_for(b, P))
    case("RB0", "rollback with a bound decision restores both versions", ("ok", "ok"), rb_ok)

    def rb1(h):
        b = prep("RB1", seat=True)
        _, wh, _ = b.paths(P)
        wh.write_bytes(wh.read_bytes() + b"edited retired\r\n")
        h.update(book=b, tree=b.tree())
        return b.rollback(P, decision_for(b, P))
    case("RB1", "retired file changed: held, no write", ("held", "rollback-retired-changed"), rb1, nowrite=True)

    def rb2(h):
        b = prep("RB2", seat=True)
        (b.rec / "images" / f"{b.r(P)['seat']['plan']['before']}.bin").unlink()
        h.update(book=b, tree=b.tree())
        return b.rollback(P, decision_for(b, P))
    case("RB2", "before-image missing: held, no write", ("held", "before-image-missing"), rb2, nowrite=True)

    def rb3(h):
        b = prep("RB3", seat=True)
        h.update(book=b, tree=b.tree())
        return b.rollback(P, None)
    case("RB3", "no rollback decision: held, no write", ("held", "rollback-decision-missing"), rb3, nowrite=True)

    def rb4(h):
        b = prep("RB4", seat=True)
        h.update(book=b, tree=b.tree())
        return b.rollback(P, decision_for(b, P, seated_sha256="0" * 64))
    case("RB4", "decision names other identities: held, no write", ("held", "rollback-decision-mismatch"), rb4, nowrite=True)

    def rb5(h):
        b = prep("RB5", seat=True)
        _, _, d = b.paths(P)
        d.write_bytes(b"NEW WORK in the draft name\r\n")
        h.update(book=b, tree=b.tree())
        return b.rollback(P, decision_for(b, P))
    case("RB5", "draft name occupied by new work: held, no write", ("held", "destination-occupied"), rb5, nowrite=True)

    rwin = [("R1", "after"), ("R2", "action"), ("R3", "action"), ("R4", "action"), ("R5", "action")]
    for i, w in enumerate(rwin, 1):
        def rw(h, w=w, i=i):
            b = prep(f"RW{i}", seat=True)
            try:
                b.rollback(P, decision_for(b, P), crash=w)
                raise Stop("refused", "no-crash", "crash point not reached")
            except Crash:
                pass
            res = b.roll_restart(P)
            if not all(res.values()):
                raise Stop("refused", "rollback-incomplete", json.dumps(res))
            return res
        case(f"RW{i}", f"rollback stopped at {w[0]} {w[1]}; restart restores both versions", ("ok", "ok"), rw)

    def rw6(h):
        b = prep("RW6", seat=True)
        try:
            b.rollback(P, decision_for(b, P), crash=("R2", "action"))
        except Crash:
            pass
        _, _, d = b.paths(P)
        d.write_bytes(d.read_bytes() + b"edited during rollback\r\n")
        h.update(book=b, tree=b.tree())
        return b.roll_restart(P)
    case("RW6", "rollback interrupted, then the moved file changed: held, no write", ("held", "rollback-state-unknown"), rw6, nowrite=True)

    bad = sum(not r["match"] for r in rows)
    first = next((r for r in rows if not r["match"]), None)
    (runs / "results.json").write_text(json.dumps({"schema": "0710-lifecycle-sim/2", "cases": rows, "mismatches": bad,
                                                   "first_failure": first and first["id"]}, indent=1) + "\n", encoding="utf-8")
    print("cases", len(rows), "mismatches", bad, "first failure", first and first["id"])
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
