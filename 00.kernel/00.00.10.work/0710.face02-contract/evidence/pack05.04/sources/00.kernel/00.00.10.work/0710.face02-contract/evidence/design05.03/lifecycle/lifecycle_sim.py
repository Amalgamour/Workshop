#!/usr/bin/env python3
"""0710/05.03 NONPRODUCTION lifecycle simulator, driven by lifecycle.template.json.

Runs stage -> sign -> approve (SYNTHETIC Director record) -> seat with retirement on
fixture law pages only. Each stage's preconditions are the template's `requires` names; an
unknown name refuses. Not a seating tool; never touches the kernel; lock/promote refused.
usage: lifecycle_sim.py --runs DIR(new)
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
T = json.loads((HERE / "lifecycle.template.json").read_text(encoding="utf-8"))
STAGES = {s["id"]: s for s in T["stages"]}
PAGES = {"0001.law": "law", "0002.schema": "schema"}
DATE = "2026-11-02"


class Stop(Exception):
    def __init__(self, outcome, code, detail):
        super().__init__(detail)
        self.outcome, self.code, self.detail = outcome, code, detail


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def header_end(b: bytes) -> int:
    i = b.find(b"\r\n## ")
    return len(b) if i < 0 else i


def content_sha(b: bytes) -> str:
    h, rest = b[:header_end(b)], b[header_end(b):]
    kept = b"\r\n".join(l for l in h.split(b"\r\n") if not re.match(rb"^(Authorization|state):", l))
    return sha(kept + rest)


def stamp(b: bytes, values: dict) -> bytes:
    h, rest = b[:header_end(b)], b[header_end(b):]
    out = []
    for l in h.split(b"\r\n"):
        m = re.match(rb"^(Authorization|state):", l)
        out.append(f"{m.group(1).decode()}: {values[m.group(1).decode()]}".encode() if m else l)
    nb = b"\r\n".join(out) + rest
    if content_sha(nb) != content_sha(b):
        raise Stop("refused", "transition-not-mechanical", "a stamp change altered content")
    return nb


def face(page, version, auth, state, body):
    lines = ["# 01", "", f"version: {version}", f"Authorization: {auth}", f"state: {state}", "Face: 01",
             f"PPPP: {page[:4]}", "book: 00.00.01.law", f"keyword: {PAGES[page]}", "", "## Job", "", body, ""]
    return "\r\n".join(lines).encode("utf-8")


class Book:
    def __init__(self, root: Path, layout="paged"):
        self.root, self.layout = root, layout
        self.law = root / "book" / "00.00.01.law"
        self.rec = root / "records"
        self.rec.mkdir(parents=True)
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

    def r(self, p):
        f = self.rec / f"{p}.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

    def save(self, p, d):
        (self.rec / f"{p}.json").write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8")

    def draft(self, p):
        return self.law / p / "01.005.md"

    def warehouse(self, p):
        base = self.law / "00.retire.09"
        return (base / p / "01.004.09.md") if self.layout == "paged" else (base / "01.004.09.md")

    # ---- preconditions named by the template ----
    def check(self, name, p, ctx):
        r = self.r(p)
        d = self.draft(p)
        cur = d.read_bytes() if d.exists() else None
        fns = {
            "candidate-matches-reviewed": lambda: sha((self.inbox / f"{p}.candidate.md").read_bytes()) == self.reviewed[p],
            "seat-matches-source": lambda: sha((self.law / p / "01.md").read_bytes()) == self.source_seat[p],
            "draft-name-free": lambda: not d.exists(),
            "staged": lambda: "stage" in r,
            "draft-bytes-equal-staged": lambda: cur is not None and sha(cur) == r["stage"]["staged_sha256"],
            "align-checks": lambda: cur is not None and all(re.search(rf"^{k}: ".encode(), cur, re.M) for k in ("version", "Authorization", "state", "Face", "PPPP", "book", "keyword"))
                                     and len(re.findall(rb"^## (.+)$", cur, re.M)) == len(set(re.findall(rb"^## (.+)$", cur, re.M))),
            "signed": lambda: "sign" in r,
            "approval-names-signed-sha": lambda: ctx.get("approval", {}).get("approved_sha256") == r.get("sign", {}).get("signed_sha256"),
            "draft-bytes-equal-signed": lambda: cur is not None and sha(cur) == r.get("sign", {}).get("signed_sha256"),
            "approved": lambda: "approve" in r,
            "draft-bytes-equal-approved": lambda: cur is not None and sha(cur) == r.get("approve", {}).get("approved_sha256"),
            "seat-unchanged": lambda: (self.law / p / "01.md").exists() and sha((self.law / p / "01.md").read_bytes()) == self.source_seat[p],
            "warehouse-name-free": lambda: not self.warehouse(p).exists(),
            "pair-approved": lambda: all("approve" in self.r(q) for q in ctx["release"]),
            "seated": lambda: "seat" in r,
            "journal-complete": lambda: r.get("seat", {}).get("journal", [])[-1:] == ["J5"],
        }
        if name not in fns:
            raise Stop("refused", "unknown-precondition", f"template names {name}, which compute does not implement")
        return fns[name]()

    def require(self, stage, p, ctx):
        for name in STAGES[stage]["requires"]:
            if not self.check(name, p, ctx):
                held = {"approved": "approval-missing", "pair-approved": "approval-missing"}.get(name)
                raise Stop("held" if held else "refused", held or name, f"{stage} {p}: precondition {name} failed")

    # ---- stages ----
    def stage(self, p):
        self.require("stage", p, {})
        b = (self.inbox / f"{p}.candidate.md").read_bytes()
        fd = os.open(self.draft(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0))
        os.write(fd, b)
        os.close(fd)
        self.save(p, {"stage": {"draft_file": self.draft(p).name, "staged_sha256": sha(b), "content_sha256": content_sha(b),
                                "source_seat_sha256": self.source_seat[p], "grounds": "SYNTHETIC fixture grounds"}})

    def sign(self, p):
        self.require("sign", p, {})
        b = self.draft(p).read_bytes()
        nb = stamp(b, {k: v.format(date=DATE, by="claude-opus-5-5 (fixture)") for k, v in T["mechanical_transitions"]["stamps"]["sign"].items()})
        self.draft(p).write_bytes(nb)
        r = self.r(p)
        r["sign"] = {"signed_sha256": sha(nb), "content_sha256": content_sha(nb), "requested_by": "model (fixture)", "checks": STAGES["sign"]["requires"]}
        self.save(p, r)

    def approve(self, p, approved_sha=None):
        r = self.r(p)
        appr = {"by": "Director (SYNTHETIC fixture record)", "words": "SYNTHETIC: approved.", "ref": "fixture",
                "approved_sha256": approved_sha or r.get("sign", {}).get("signed_sha256")}
        self.require("approve", p, {"approval": appr})
        r["approve"] = appr
        self.save(p, r)

    def seat(self, release, crash_after=None, start_journal=None):
        ctx = {"release": release}
        if not all(self.check("pair-approved", q, ctx) for q in release):
            raise Stop("held", "approval-missing", "the release has a face without an approval; nothing renamed")
        done = []
        for p in release:
            try:
                self.require("seat", p, ctx)
                self._seat_one(p, crash_after if p == release[0] else None)
            except Stop as s:
                if done:
                    raise Stop("held", "half-seated", f"seated {done}; {p} stopped at {s.code}; Director decides finish or rollback")
                raise
            done.append(p)
        return done

    def _seat_one(self, p, crash_after):
        r = self.r(p)
        seat_f, wh, d = self.law / p / "01.md", self.warehouse(p), self.draft(p)
        before = seat_f.read_bytes()
        r["seat"] = {"journal": ["J1"], "seat_before_sha256": sha(before), "warehouse_file": wh.relative_to(self.law).as_posix()}
        r["seat"]["retired_sha256"] = sha(stamp(before, {k: v.format(date=DATE, new="005") for k, v in T["mechanical_transitions"]["stamps"]["retire"].items()}))
        r["seat"]["seated_sha256"] = sha(stamp(d.read_bytes(), T["mechanical_transitions"]["stamps"]["approve"] | {"Authorization": f"approved — {DATE}"}))
        self.save(p, r)
        self._steps(p, ["J2", "J3", "J4", "J5"], crash_after)

    def _steps(self, p, steps, crash_after=None):
        r = self.r(p)
        s = r["seat"]
        seat_f, wh, d = self.law / p / "01.md", self.law / s["warehouse_file"], self.draft(p)
        for step in steps:
            if step == "J2":
                wh.parent.mkdir(parents=True, exist_ok=True)
                ledger = self.law / "00.retire.09" / "09.md"
                with open(ledger, "ab") as f:
                    f.write(f"retired: {p}/01.004.md -> {s['warehouse_file']} · by version 005 · before {s['seat_before_sha256'][:12]} · retired {s['retired_sha256'][:12]} · approval SYNTHETIC · {DATE}\n".encode())
            elif step == "J3":
                if wh.exists():
                    raise Stop("refused", "warehouse-name-taken", f"{wh.relative_to(self.law).as_posix()} already exists")
                if sha(seat_f.read_bytes()) != s["seat_before_sha256"]:
                    raise Stop("held", "restart-hash-mismatch", "seat bytes are not the recorded seat")
                os.rename(seat_f, wh)
                wh.write_bytes(stamp(wh.read_bytes(), {k: v.format(date=DATE, new="005") for k, v in T["mechanical_transitions"]["stamps"]["retire"].items()}))
                if sha(wh.read_bytes()) != s["retired_sha256"]:
                    raise Stop("held", "restart-hash-mismatch", "retired bytes differ from the plan")
            elif step == "J4":
                if sha(d.read_bytes()) != r["approve"]["approved_sha256"]:
                    raise Stop("held", "restart-hash-mismatch", "draft bytes are not the approved bytes")
                os.rename(d, seat_f)
                seat_f.write_bytes(stamp(seat_f.read_bytes(), {"Authorization": f"approved — {DATE}", "state": "approved"}))
            elif step == "J5":
                ok = sha(seat_f.read_bytes()) == s["seated_sha256"] and sha(wh.read_bytes()) == s["retired_sha256"]
                if not ok:
                    raise Stop("held", "restart-hash-mismatch", "read-back differs")
            s["journal"].append(step)
            self.save(p, r)
            if crash_after == step:
                raise Stop("interrupted", "interrupted", f"simulated stop after {step}")

    def restart(self, p):
        r = self.r(p)
        s = r["seat"]
        seat_f, wh, d = self.law / p / "01.md", self.law / s["warehouse_file"], self.draft(p)
        last = s["journal"][-1]
        if last == "J3":
            if not (wh.exists() and sha(wh.read_bytes()) == s["retired_sha256"] and not seat_f.exists()):
                raise Stop("held", "restart-hash-mismatch", "warehouse state does not match the journal")
            self._steps(p, ["J4", "J5"])
        elif last == "J5":
            return "already-complete"
        else:
            raise Stop("held", "restart-unhandled", f"restart after {last} not modelled")
        return "completed"

    def rollback(self, p):
        self.require("rollback", p, {})
        r = self.r(p)
        s = r["seat"]
        seat_f, wh, d = self.law / p / "01.md", self.law / s["warehouse_file"], self.draft(p)
        os.rename(seat_f, d)
        d.write_bytes(stamp(d.read_bytes(), {k: v.format(date=DATE, by="claude-opus-5-5 (fixture)") for k, v in T["mechanical_transitions"]["stamps"]["sign"].items()}))
        os.rename(wh, seat_f)
        seat_f.write_bytes(stamp(seat_f.read_bytes(), {"Authorization": "approved — 2026-10-10", "state": "approved"}))
        with open(self.law / "00.retire.09" / "09.md", "ab") as f:
            f.write(f"struck: {p} retirement rolled back · {DATE}\n".encode())
        return {"seat_restored": sha(seat_f.read_bytes()) == s["seat_before_sha256"], "draft_restored_to_signed": sha(d.read_bytes()) == r["sign"]["signed_sha256"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    runs = Path(ap.parse_args().runs)
    runs.mkdir(parents=True, exist_ok=False)
    rows = []

    def prep(name, layout="paged", sign=True, approve=True):
        b = Book(runs / name, layout)
        for p in PAGES:
            b.stage(p)
            if sign:
                b.sign(p)
            if approve:
                b.approve(p)
        return b

    def case(cid, says, expect, fn):
        try:
            got = {"outcome": "ok", "code": "ok", "detail": fn()}
        except Stop as s:
            got = {"outcome": s.outcome, "code": s.code, "detail": s.detail}
        match = (got["outcome"], got["code"]) == expect
        rows.append({"id": cid, "says": says, "expect": list(expect), "actual": got, "match": match})
        print(f"{'PASS' if match else 'FAIL'} {cid:<4} {says[:66]:<66} -> {got['outcome']}/{got['code']}")

    rel = list(PAGES)

    def l1():
        b = prep("L1")
        done = b.seat(rel)
        wh = sorted(p.relative_to(b.law).as_posix() for p in (b.law / "00.retire.09").rglob("*.md"))
        same = all(b.r(p)["stage"]["content_sha256"] == b.r(p)["sign"]["content_sha256"] == content_sha((b.law / p / "01.md").read_bytes()) for p in rel)
        retired_same = all(content_sha((b.law / b.r(p)["seat"]["warehouse_file"]).read_bytes()) == content_sha(face(p, "004", "x", "y", f"SYNTHETIC seat body of {p}.")) for p in rel)
        if not (same and retired_same):
            raise Stop("refused", "content-changed", "a stamp transition changed content")
        return {"seated": done, "warehouse": wh, "content_kept_through_stamps": same and retired_same}
    case("L1", "pair seats; equal 01.004.09.md from two pages do not collide", ("ok", "ok"), l1)

    def l2():
        b = prep("L2", approve=False)
        d = b.draft("0001.law")
        d.write_bytes(d.read_bytes().replace(b"changed.", b"changed again."))
        b.approve("0001.law")
    case("L2", "content changed after signing: approval refused", ("refused", "draft-bytes-equal-signed"), l2)

    def l2b():
        b = prep("L2b")
        d = b.draft("0002.schema")
        d.write_bytes(d.read_bytes().replace(b"changed.", b"changed after approval."))
        b.seat(rel)
    case("L2b", "content changed after approval: first face seats, second held", ("held", "half-seated"), l2b)

    def l3():
        b = prep("L3", approve=False)
        b.approve("0001.law")
        before = {p: sha((b.law / p / "01.md").read_bytes()) for p in rel}
        try:
            b.seat(rel)
        finally:
            after = {p: sha((b.law / p / "01.md").read_bytes()) for p in rel}
            assert before == after
    case("L3", "missing approval for one face: release held, nothing renamed", ("held", "approval-missing"), l3)

    def l4():
        b = prep("L4")
        try:
            b.seat(["0001.law"], crash_after="J3")
        except Stop as s:
            assert s.code == "interrupted"
        return b.restart("0001.law")
    case("L4", "interrupted after J3; restart checks hashes and completes", ("ok", "ok"), l4)

    def l4b():
        b = prep("L4b")
        try:
            b.seat(["0001.law"], crash_after="J3")
        except Stop as s:
            assert s.code == "interrupted"
        d = b.draft("0001.law")
        d.write_bytes(d.read_bytes() + b"tampered\r\n")
        return b.restart("0001.law")
    case("L4b", "interrupted, draft changed before restart: held", ("held", "restart-hash-mismatch"), l4b)

    def l5():
        b = prep("L5")
        s = b.law / "0002.schema" / "01.md"
        s.write_bytes(s.read_bytes() + b"edited seat\r\n")
        b.seat(rel)
    case("L5", "second seat changed after approval: half-seated, held for Director", ("held", "half-seated"), l5)

    def l6():
        b = prep("L6")
        b.seat(rel)
        res = {p: b.rollback(p) for p in rel}
        if not all(all(v.values()) for v in res.values()):
            raise Stop("refused", "rollback-mismatch", json.dumps(res))
        return res
    case("L6", "rollback restores both versions byte-for-byte", ("ok", "ok"), l6)

    def l7():
        b = Book(runs / "L7")
        b.stage("0001.law")
        b.seat(["0001.law"])
    case("L7", "seat before sign/approve: held, approval missing", ("held", "approval-missing"), l7)

    def l7b():
        b = Book(runs / "L7b")
        b.sign("0001.law")
    case("L7b", "sign before stage: refused", ("refused", "staged"), l7b)

    def l8():
        b = prep("L8", approve=False)
        b.approve("0001.law", approved_sha=b.r("0001.law")["stage"]["staged_sha256"])
    case("L8", "approval names the pre-sign bytes: refused", ("refused", "approval-names-signed-sha"), l8)

    def l9():
        if "lock" not in STAGES:
            raise Stop("refused", "not-in-template", "lock and promote are separate (0023)")
    case("L9", "lock or promote requested", ("refused", "not-in-template"), l9)

    def l10():
        b = prep("L10", layout="flat")
        b.seat(rel)
    case("L10", "flat warehouse: second 01.004.09.md collides; held half-seated", ("held", "half-seated"), l10)

    bad = sum(not r["match"] for r in rows)
    (runs / "results.json").write_text(json.dumps({"schema": "0710-lifecycle-sim/1", "cases": rows, "mismatches": bad}, indent=1) + "\n", encoding="utf-8")
    print("cases", len(rows), "mismatches", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
