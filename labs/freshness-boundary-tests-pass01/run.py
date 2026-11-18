#!/usr/bin/env python3
"""Independent freshness-boundary acceptance runner (0707/05.23). NONPRODUCTION. Standard library only.

Tests requirements 0522/06.37 §1-4 through a candidate's OWN entry. Independent of Grok-1's combined implementation
(not read). Written with declared prior knowledge of the L prototype (see 06.23 notes).

usage: run.py --candidate ROOT --identity MANIFEST.json --rooms NEW-DIR --out RESULT.json [--cases ID,ID]
  MANIFEST.json  a frozen 'harness-inputs/2' manifest (e.g. labs/loop-convergence-harness-pass02/inputs/*.json, read-only):
                 candidate identity (CANDIDATE.json sha256 + every file), open_entry, dependency rows.
exit: 0 every required case passed · 1 otherwise (fail/blocked/not-reached/error) · 2 refused before execution · 3 crash
Before anything runs: shapes (pass02 inputs_check, hash-pinned) + every candidate file + CANDIDATE.json + accepted
dependency pins are verified; the root must be outside the live repo; the entry must be a declared file. Every case
runs in a NEW copy of the candidate, re-verified. No live repin, no root substitution, no fallback.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judges  # noqa: E402

LIVE = Path(r"D:\Git\lib-build")
BOOK = "00.kernel/00.00.10.work"
ENTRY = "app/librarian.py"
PACK23 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.23/source-manifest.json"
INPUTS_CHECK = "labs/loop-convergence-harness-pass02/inputs_check.py"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
JUDGMENT = {
    "finding": "LAB-ONLY SYNTHETIC judgment for the 0707/05.23 freshness-boundary lab; not a review of any real pass.",
    "reasons": ["LAB-ONLY: exercises record, inspect, read, recover and publish refusal on a disposable copy."],
    "operation": "continue", "disposition": "held", "pass_terminal": "open", "goal_terminal": "open",
    "next_action": "LAB-ONLY: no real action.", "semantic_conflict": None, "design_fork": None,
    "findings": [], "holds": [], "answers": [], "review_passes": [], "gaps": ["LAB-ONLY: synthetic judgment"],
    "sections": {k: None for k in ("affected", "assumptions", "consequences", "exploration", "finish_assessments", "for_model", "issue",
                                   "learning", "limits", "open_questions", "options", "outcome_evidence", "preservation", "proposed_plan",
                                   "question", "recommendation", "remaining_choices", "within_direction", "tests_passed")}
    | {"findings_account": [], "next_bounded_action": "LAB-ONLY: none.", "prime_finding": "LAB-ONLY synthetic.",
       "return_result": "LAB-ONLY synthetic.", "tests_note": "LAB-ONLY: no tests judged."},
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    return sha(Path(p).read_bytes())


class Refused(Exception):
    pass


# ------------------------------------------------------------------ identity
def frozen_rows() -> dict:
    return {r["path"]: r for r in json.loads(PACK23.read_bytes())["files"]}


def load_inputs_check():
    row = frozen_rows()[INPUTS_CHECK]
    if sha_file(LIVE / INPUTS_CHECK) != row["sha256"]:
        raise Refused("pass02 inputs_check.py differs from its pack05.23 freeze")
    spec = importlib.util.spec_from_file_location("frozen_inputs_check", LIVE / INPUTS_CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pin_ok(base: Path, f: dict) -> bool:
    p = base / f["path"]
    return p.is_file() and p.stat().st_size == f["bytes"] and sha_file(p) == f["sha256"]


def verify(identity, root: Path) -> dict:
    probs = load_inputs_check().shape_problems(identity)
    if probs:
        raise Refused("identity manifest malformed: " + "; ".join(probs[:10]))
    cand = identity["candidate"]
    if cand == "PENDING":
        raise Refused("candidate is PENDING: nothing to run (a combined run waits for Prime's identity manifest)")
    try:
        root.resolve().relative_to(LIVE.resolve())
        raise Refused("candidate root is inside the live repo; refusing root substitution")
    except ValueError:
        pass
    if not (root / "CANDIDATE.json").is_file() or sha_file(root / "CANDIDATE.json") != cand["candidate_json_sha256"]:
        raise Refused("CANDIDATE.json differs from the declared identity")
    paths = {f["path"] for f in cand["files"]}
    for need in [ENTRY] + ([cand["open_entry"]] if cand.get("open_entry") else []):
        if need not in paths:
            raise Refused(f"entry {need} is not a declared candidate file")
    for f in cand["files"]:
        if not pin_ok(root, f):
            raise Refused(f"candidate file differs: {f['path']}")
    for d in identity["dependencies"]:
        if d["status"] == "accepted":
            for f in d["files"] + [d["review_ref"]]:
                if not pin_ok(LIVE, f):
                    raise Refused(f"accepted dependency {d['id']} differs: {f['path']}")
    kind = json.loads((root / "CANDIDATE.json").read_bytes()).get("kind")
    return {"kind": kind, "candidate_json_sha256": cand["candidate_json_sha256"], "open_entry": cand.get("open_entry"), "files": cand["files"]}


# ------------------------------------------------------------------ execution
class Ctx:
    def __init__(self, cand: Path, ident: dict, rooms: Path):
        self.cand, self.ident, self.rooms = cand, ident, rooms
        self.jf = rooms / "lab-judgment.json"
        self.jf.write_bytes((json.dumps(JUDGMENT, indent=1) + "\n").encode("utf-8"))

    def room(self, cid: str) -> Path:
        dst = self.rooms / cid
        shutil.copytree(self.cand, dst)
        for f in self.ident["files"]:
            if not pin_ok(dst, f):
                raise Refused(f"copied candidate differs at {f['path']}")
        return dst


def run(argv, cwd: Path) -> dict:
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, env=ENV, cwd=str(cwd), timeout=600)
    out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    try:
        body = json.loads(out)
    except Exception:
        body = None
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout": out, "stderr": err, "body": body if isinstance(body, dict) else None}


def cmd(root: Path, page: str, c: str, *extra, pas: str = "05.01") -> dict:
    return run([root / ENTRY, "review-loop", c, "--book", root / BOOK, "--source", page, "--pass", pas, *extra], root)


def B(res) -> dict:
    return res["body"] if isinstance(res.get("body"), dict) else {}


def obs(res: dict) -> dict:
    """The observation a judge sees: exit, stale, judgment, a message (correction + stderr tail), no stdout dump."""
    b = B(res)
    return {"exit": res["exit"], "stale": b.get("stale"), "judgment": b.get("judgment"), "measurement": b.get("measurement"),
            "codes": sorted({f.get("code") for f in b.get("findings") or [] if isinstance(f, dict)}),
            "message": (json.dumps(b.get("correction")) if b.get("correction") is not None else "") + " " + res["stderr"][-300:],
            "stderr": res["stderr"][-600:]}


def write(p: Path, data) -> bytes:
    p.parent.mkdir(parents=True, exist_ok=True)
    b = data if isinstance(data, bytes) else data.encode("utf-8")
    p.write_bytes(b)
    return b


def page_tree(root: Path, page: str) -> dict:
    base = root / BOOK / page
    return {str(p.relative_to(base)).replace("\\", "/"): sha_file(p) for p in sorted(base.rglob("*")) if p.is_file()}


def edit(p: Path, old: bytes, new: bytes) -> None:
    b = p.read_bytes()
    if b.count(old) != 1:
        raise Refused(f"fixture edit anchor not unique in {p.name}: {old[:40]!r} x{b.count(old)}")
    p.write_bytes(b.replace(old, new))


# ------------------------------------------------------------------ fixtures (LAB-ONLY synthetic books)
N5P, N7P = "0589.fbt-n5", "0789.fbt-n7"   # smoke-01: 0588 was classified N5 (N7 pages are 07NN); kept as first failure


def n5_book(root: Path, page: str = N5P) -> None:
    pd = root / BOOK / page
    a = write(pd / "e/a.md", f"LAB-ONLY N5 artifact for {page}\n")
    s = write(pd / "e/s.md", f"LAB-ONLY N5 submission for {page}\n")
    m = write(pd / "e/m.json", json.dumps({"files": [{"path": f"{BOOK}/{page}/e/a.md", "bytes": len(a), "sha256": sha(a)}]}) + "\n")
    write(pd / "05.01.md", f"# 05.01 LAB N5 (0707/05.23 freshness fixture)\n\n## Goal\nLAB-ONLY.\n\n## Return pointer\n"
                           f"Submission: {BOOK}/{page}/e/s.md sha256 {sha(s)}, {len(s)} bytes.\n"
                           f"Artifact manifest: {BOOK}/{page}/e/m.json sha256 {sha(m)}, {len(m)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")


BASE_TASK = "## Goal\nLAB-ONLY task text: alpha.\n"
REVIEW = "## Review - Codex Prime\nREVIEW-TEXT pending.\n"
POINTER_SLOT = "## Return pointer\nPOINTER-SLOT\n"
FENCE_EX = "```text\n## Return pointer\nReturned: example.md (example), sha256 " + "0" * 64 + ", 1 bytes.\n\n## Review - Codex Prime\nExample review.\n```\n"


def pack_text(variant: str) -> str:
    head = "# 05.01 LAB N7 pack (0707/05.23 freshness fixture)\ndate: 2026-11-04\nwho: lab\n\n"
    t = {
        "normal": BASE_TASK + "\n" + POINTER_SLOT + "\n" + REVIEW,
        "F1": BASE_TASK + "\nExample of a filled pack:\n\n" + FENCE_EX + "\nAfter-fence task text: bravo.\n\n" + POINTER_SLOT + "\n" + REVIEW,
        # smoke-02: on proto-l F1 never reaches record (the fenced example's pointer is bound). F1b repeats the REAL
        # pointer lines inside the fence, so either reading binds the same files and the exemption itself is tested.
        "F1b": BASE_TASK + "\nExample of this filled pack:\n\n```text\n" + POINTER_SLOT + "\n## Review - Codex Prime\nExample review.\n```\n"
               "\nAfter-fence task text: bravo.\n\n" + POINTER_SLOT + "\n" + REVIEW,
        "F2": BASE_TASK + "\n" + POINTER_SLOT + "\n## Reviewer checklist\nchecklist-item: charlie.\n\n" + REVIEW,
        "F3": BASE_TASK + "\n" + POINTER_SLOT + "\n## Reviews - Codex Prime\nlookalike-text: delta.\n",
        "F4": BASE_TASK + "\n## Return pointer\nNothing here yet.\n\nMore task text: echo.\n\n" + POINTER_SLOT + "\n" + REVIEW,
        "F5": BASE_TASK + "\n" + POINTER_SLOT + "\n" + REVIEW + "\nbetween-text: foxtrot.\n\n## Review - Codex Prime\nSecond review heading.\n",
        "F6": BASE_TASK + "\n" + POINTER_SLOT,
        "F7": BASE_TASK + "\n" + POINTER_SLOT + "\n" + REVIEW + "\nExample block kept in the review:\n\n" + FENCE_EX.replace("Example review.", "Example review two."),
        "E1": BASE_TASK + "\n~~~\n## Return pointer\nPENDING example.\n\n## Review - Codex Prime\nExample.\n~~~\n\nAfter-tilde task text: golf.\n\n" + POINTER_SLOT + "\n" + REVIEW,
        "E2": BASE_TASK + "\nAn unclosed example follows:\n```text\nexample line\n\n" + POINTER_SLOT + "\n" + REVIEW,
        "E3": BASE_TASK + "\n## Return pointer example\nThis heading only looks like the pointer.\n\nLater task text: hotel.\n\n" + POINTER_SLOT + "\n" + REVIEW,
    }[variant]
    return head + t


def n7_pair(ctx: Ctx, root: Path, variant: str = "normal", page: str = N7P) -> dict:
    pd = root / BOOK / page
    write(pd / "05.01.pack.md", pack_text(variant))
    oe = ctx.ident.get("open_entry")
    opened = None
    if oe:
        opened = run([root / oe, "open", "--book", root / BOOK, "--source", page, "--pass", "05.01"], root)["exit"]
    a = write(pd / "evidence/e0501/a.md", f"LAB-ONLY artifact A for {page}\n")
    b = write(pd / "evidence/e0501/b.md", f"LAB-ONLY artifact B for {page}\n")
    ret = write(pd / "05.01.return.md", f"# 05.01 SYNTHETIC return for {page}\nLAB-ONLY.\n")
    rows = [{"path": f"{BOOK}/{page}/{x}", "bytes": len(c), "sha256": sha(c)} for x, c in
            (("05.01.return.md", ret), ("evidence/e0501/a.md", a), ("evidence/e0501/b.md", b))]
    man = write(pd / "evidence/e0501/artifact-manifest.json", json.dumps({"files": rows}, indent=1) + "\n")
    lines = (f"Returned: 05.01.return.md (lab, 2026-11-04), sha256 {sha(ret)}, {len(ret)} bytes.\n"
             f"Artifact manifest: evidence/e0501/artifact-manifest.json, sha256 {sha(man)}, {len(man)} bytes.")
    pk = pd / "05.01.pack.md"
    raw = pk.read_bytes()
    if raw.count(b"POINTER-SLOT") < 1:
        raise Refused("pack fixture has no pointer slot")
    pk.write_bytes(raw.replace(b"POINTER-SLOT", lines.encode("utf-8")))    # F1b fills the fenced copy too (same lines)
    return {"open_exit": opened}


def record_inspect(ctx: Ctx, root: Path, page: str, tag: str) -> dict:
    p = cmd(root, page, "prepare")
    f = cmd(root, page, "form")
    rec = cmd(root, page, "record", "--intake", B(p).get("intake_id") or "none", "--judgment", ctx.jf)
    ins = cmd(root, page, "inspect")
    (ctx.rooms / f"{tag}-inspect.stdout").write_bytes(ins["stdout"].encode("utf-8"))   # full text; automated, not a Prime read
    return {"prepare": p, "form": f, "record": rec, "inspect": ins, "review_id": B(rec).get("review_id")}


def store_intake(root: Path, page: str) -> Path:
    hits = sorted((root / BOOK / "workbook-review" / page / "05.01").glob("intake.json"))
    if len(hits) != 1:
        raise Refused(f"cannot locate exactly one stored comparison intake for {page} (found {len(hits)})")
    return hits[0]


# ------------------------------------------------------------------ cases
CASES = []


def case(cid, group, requirement, required=True):
    def deco(fn):
        CASES.append({"id": cid, "group": group, "requirement": requirement, "required": required, "fn": fn})
        return fn
    return deco


def missing_case(ctx: Ctx, cid: str, variant: str, kind: str):
    root = ctx.room(cid)
    page = N5P if kind == "N5" else N7P
    if kind == "N5":
        n5_book(root)
    else:
        n7_pair(ctx, root)
    art = root / BOOK / page / ("e/a.md" if kind == "N5" else "evidence/e0501/a.md")
    if variant == "M5":
        p = cmd(root, page, "prepare")
        before = page_tree(root, page)
        rd = cmd(root, page, "read")
        pub = cmd(root, page, "publish", "--review", "none")
        o = {"prepare_measurement": B(p).get("measurement"), "after_read": obs(rd), "publish": obs(pub),
             "destination_created": page_tree(root, page) != before}
        return judges.missing(o, "M5", JUDGMENT) + (o,)
    ri = record_inspect(ctx, root, page, cid)
    control = cmd(root, page, "read")
    intake = store_intake(root, page)
    moved = intake.with_name("intake.json.lab-moved")
    keep_art = art.read_bytes()
    if variant in ("M0", "M1", "M3", "M4"):
        art.write_bytes(keep_art + b"LAB change after record\n")
    if variant in ("M1", "M2"):
        intake.rename(moved)
    elif variant == "M3":
        intake.rename(moved)
        intake.write_bytes(b"[]\n")
    elif variant == "M4":
        intake.rename(moved)
        intake.write_bytes(b"{\"intake_id\": \n")
    before = page_tree(root, page)
    rd = cmd(root, page, "read")
    rc = cmd(root, page, "recover")
    pub = cmd(root, page, "publish", "--review", ri["review_id"] or "none")
    o = {"record_exit": ri["record"]["exit"], "control_read": obs(control), "after_read": obs(rd), "after_recover": obs(rc),
         "publish": obs(pub), "destination_created": page_tree(root, page) != before}
    if variant == "M1":
        art.write_bytes(keep_art)
        if intake.exists():
            intake.rename(intake.with_name("intake.json.lab-written-during-test"))
        moved.rename(intake)
        o["restored_read"] = obs(cmd(root, page, "read"))
    return judges.missing(o, variant, JUDGMENT) + (o,)


for _k in ("N5", "N7"):
    for _v, _txt in (("M0", "control: artifact changed, comparison intake intact -> stale; publish refused"),
                     ("M1", "artifact changed, comparison intake.json moved away -> not current; publish refused; history kept; restore recovers"),
                     ("M2", "no source change, comparison intake.json moved away (review exists) -> not current"),
                     ("M3", "artifact changed, intake.json is valid JSON but not an object -> not current; publish refused"),
                     ("M4", "artifact changed, intake.json is malformed JSON -> not current (refusal allowed); publish refused"),
                     ("M5", "a new, never-recorded book -> read not current; publish refused")):
        def _fn(ctx, _k=_k, _v=_v):
            return missing_case(ctx, f"{_v}-{_k}", _v, _k)
        case(f"{_v}-{_k}", "missing-intake", f"{_k}: {_txt}")(_fn)


REGION = {   # id: (variant, edit_anchor, edit_replacement or callable, expectation)
    "R0": ("normal", b"REVIEW-TEXT pending.", b"REVIEW-TEXT accepted (LAB summary).", "current"),
    "R1": ("normal", b"task text: alpha.", b"task text: alpha CHANGED.", "not-current"),
    "R2": ("normal", b"(lab, 2026-11-04)", b"(lab, 2026-11-05)", "not-current"),
    "R3": ("normal", "return", None, "not-current"),
    "R4": ("normal", "artifact", None, "not-current"),
    "F1": ("F1", b"After-fence task text: bravo.", b"After-fence task text: bravo CHANGED.", "not-current"),
    "F1b": ("F1b", b"After-fence task text: bravo.", b"After-fence task text: bravo CHANGED.", "not-current"),
    "F2": ("F2", b"checklist-item: charlie.", b"checklist-item: charlie CHANGED.", "not-current"),
    "F3": ("F3", b"lookalike-text: delta.", b"lookalike-text: delta CHANGED.", "not-current"),
    "F4": ("F4", b"More task text: echo.", b"More task text: echo CHANGED.", "not-current"),
    "F5": ("F5", b"between-text: foxtrot.", b"between-text: foxtrot CHANGED.", "not-current"),
    "F6": ("F6", None, b"Appended task text: india.\n", "not-current"),
    "F7a": ("F7", b"REVIEW-TEXT pending.", b"REVIEW-TEXT accepted (LAB summary).", "current"),
    "F7b": ("F7", b"task text: alpha.", b"task text: alpha CHANGED.", "not-current"),
    "E1": ("E1", b"After-tilde task text: golf.", b"After-tilde task text: golf CHANGED.", "not-current"),
    "E2": ("E2", b"REVIEW-TEXT pending.", b"REVIEW-TEXT accepted (LAB summary).", "not-current"),
    "E3": ("E3", b"Later task text: hotel.", b"Later task text: hotel CHANGED.", "not-current"),
}
REGION_TXT = {
    "R0": "normal headings: a Review-only edit stays current (permitted)",
    "R1": "normal headings: a task-text edit is not current",
    "R2": "normal headings: a pointer edit (attribution text) is not current",
    "R3": "normal headings: a changed return is not current",
    "R4": "normal headings: a changed artifact is not current",
    "F1": "a ``` fenced example with pointer/Review headings in the task: a task edit AFTER the fence is not current",
    "F1b": "the fenced example repeats the REAL pointer lines (so the pair records): a task edit AFTER the fence is not current",
    "F2": "a '## Reviewer checklist' section after the pointer: an edit inside it is not current",
    "F3": "the only review-like heading is '## Reviews - Codex Prime': an edit under it is not current",
    "F4": "duplicate '## Return pointer' headings: a task edit between them is not current (strict refusal kept as not-reached)",
    "F5": "duplicate '## Review - Codex Prime' headings: an edit between them is not current (ambiguity grants no exemption)",
    "F6": "no Review heading: appended text is not current",
    "F7a": "a fenced example inside the real Review region: a real Review-only edit stays current",
    "F7b": "a fenced example inside the real Review region: a task edit is not current",
    "E1": "NEW: a ~~~ tilde-fenced example with headings in the task: a task edit after it is not current",
    "E2": "NEW: an unclosed ``` before the real headings (missing boundary): a Review-text edit is not current",
    "E3": "NEW: a task heading '## Return pointer example' (prefix lookalike): a task edit after it is not current",
}


def region_case(ctx: Ctx, cid: str):
    variant, anchor, repl, expect = REGION[cid]
    root = ctx.room(cid)
    n7_pair(ctx, root, variant)
    ri = record_inspect(ctx, root, N7P, cid)
    pub = cmd(root, N7P, "publish", "--review", ri["review_id"] or "none")
    reached = ri["record"]["exit"] == 0 and pub["exit"] == 0
    o = {"reached": reached, "prepare": obs(ri["prepare"]), "record_exit": ri["record"]["exit"], "publish_exit": pub["exit"]}
    if reached:
        o["pre_read"] = obs(cmd(root, N7P, "read"))
        pd = root / BOOK / N7P
        if anchor == "return":
            (pd / "05.01.return.md").write_bytes((pd / "05.01.return.md").read_bytes() + b"LAB change\n")
        elif anchor == "artifact":
            (pd / "evidence/e0501/a.md").write_bytes(b"LAB changed artifact\n")
        elif anchor is None:
            (pd / "05.01.pack.md").write_bytes((pd / "05.01.pack.md").read_bytes() + repl)
        else:
            edit(pd / "05.01.pack.md", anchor, repl)
        o["post_read"] = obs(cmd(root, N7P, "read"))
    return judges.region(o, expect) + (o,)


for _cid in REGION:
    case(_cid, "pack-region", REGION_TXT[_cid], required=_cid != "F4")((lambda c: (lambda ctx: region_case(ctx, c)))(_cid))


@case("C1", "composition", "N5 foreign instance: a byte-copied book does not read the source review current; the original stays current")
def c1(ctx):
    a = ctx.room("C1")
    n5_book(a)
    ri = record_inspect(ctx, a, N5P, "C1")
    a0 = obs(cmd(a, N5P, "read"))
    before = page_tree(a, "workbook-review") if (a / BOOK / "workbook-review").is_dir() else {}
    b = ctx.rooms / "C1-bookB"
    shutil.copytree(a, b)
    br = obs(cmd(b, N5P, "read"))
    a1 = obs(cmd(a, N5P, "read"))
    o = {"record_exit": ri["record"]["exit"], "a_read_before": a0, "b_read": br, "a_read_after": a1,
         "a_unchanged": (page_tree(a, "workbook-review") if (a / BOOK / "workbook-review").is_dir() else {}) == before}
    return judges.instance(o) + (o,)


@case("C2", "composition", "N7 local exchange/body: a Review-only edit stays current and a task-body edit is not current (same entry)")
def c2(ctx):
    root = ctx.room("C2")
    n7_pair(ctx, root)
    ri = record_inspect(ctx, root, N7P, "C2")
    cmd(root, N7P, "publish", "--review", ri["review_id"] or "none")
    pk = root / BOOK / N7P / "05.01.pack.md"
    o = {"pre_read": obs(cmd(root, N7P, "read"))}
    edit(pk, b"REVIEW-TEXT pending.", b"REVIEW-TEXT accepted (LAB summary).")
    o["review_edit_read"] = obs(cmd(root, N7P, "read"))
    edit(pk, b"task text: alpha.", b"task text: alpha CHANGED.")
    o["task_edit_read"] = obs(cmd(root, N7P, "read"))
    return judges.n7_body(o) + (o,)


@case("C3", "composition", "ordinary source-row change: an N5 artifact change after record is stale")
def c3(ctx):
    root = ctx.room("C3")
    n5_book(root)
    record_inspect(ctx, root, N5P, "C3")
    o = {"pre_read": obs(cmd(root, N5P, "read"))}
    (root / BOOK / N5P / "e/a.md").write_bytes(b"LAB changed artifact\n")
    o["post_read"] = obs(cmd(root, N5P, "read"))
    return judges.row_change(o) + (o,)


@case("C4", "composition", "one chain: in ONE root through ONE entry, the N5 instance, N7 region/exchange and row-change guards all hold")
def c4(ctx):
    if ctx.ident.get("kind") != "combined":
        return {"needs": "a combined candidate"}, [f"candidate kind {ctx.ident.get('kind')!r} is not the combined candidate; not executed"], "blocked", {}
    root = ctx.room("C4")
    n5_book(root)
    n7_pair(ctx, root)
    r5 = record_inspect(ctx, root, N5P, "C4-n5")
    r7 = record_inspect(ctx, root, N7P, "C4-n7")
    cmd(root, N7P, "publish", "--review", r7["review_id"] or "none")
    o = {"n5_record": r5["record"]["exit"], "pre5": obs(cmd(root, N5P, "read")), "pre7": obs(cmd(root, N7P, "read"))}
    b = ctx.rooms / "C4-bookB"
    shutil.copytree(root, b)
    o["copy5"] = obs(cmd(b, N5P, "read"))
    edit(root / BOOK / N7P / "05.01.pack.md", b"REVIEW-TEXT pending.", b"REVIEW-TEXT accepted (LAB summary).")
    o["review7"] = obs(cmd(root, N7P, "read"))
    edit(root / BOOK / N7P / "05.01.pack.md", b"task text: alpha.", b"task text: alpha CHANGED.")
    o["task7"] = obs(cmd(root, N7P, "read"))
    (root / BOOK / N5P / "e/a.md").write_bytes(b"LAB changed artifact\n")
    o["row5"] = obs(cmd(root, N5P, "read"))
    r = []
    for k in ("pre5", "pre7", "review7"):
        if not judges.is_current(o[k]):
            r.append(f"{k} not current")
    for k in ("copy5", "task7", "row5"):
        if not judges.not_current(o[k]):
            r.append(f"{k} still current (a guard layer dropped)")
    return {"all three guards": "hold in one chain"}, r, ("pass" if not r else "fail"), o


@case("D1", "identity-limit", "DEFERRED (06.37 §4): a same-path byte-identical replacement clone is not distinguishable by path/page/pass-derived ids; "
                              "policy deferred to a Director-reviewed design. Never executed, never credited.", required=False)
def d1(ctx):
    return {"policy": "deferred"}, ["not tested by design"], "deferred", {}


# ------------------------------------------------------------------ driver
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--identity", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", default="all")
    a = ap.parse_args()
    out = {"schema": "freshness-boundary-result/1", "candidate": a.candidate, "identity": a.identity, "identity_sha256": sha_file(a.identity),
           "provenance": "Claude 0707/05.23 author cases; independent of Grok-1's combined implementation; not Prime review"}
    try:
        ident = verify(json.loads(Path(a.identity).read_text(encoding="utf-8")), Path(a.candidate))
        known = {c["id"] for c in CASES}
        sel = list(CASES) if a.cases == "all" else [c for c in CASES if c["id"] in set(a.cases.split(","))]
        if a.cases != "all" and set(a.cases.split(",")) - known:
            raise Refused(f"unknown cases {sorted(set(a.cases.split(',')) - known)}")
    except Refused as exc:
        out.update({"refused": str(exc), "records": []})
        Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print("REFUSED:", exc)
        return 2
    rooms = Path(a.rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    ctx = Ctx(Path(a.candidate), ident, rooms)
    out["candidate_kind"] = ident["kind"]
    recs = []
    for c in sel:
        rec = {"id": c["id"], "group": c["group"], "requirement": c["requirement"], "required": c["required"]}
        try:
            expected, reasons, verdict, observed = c["fn"](ctx)
            rec.update({"expected": expected, "verdict": verdict, "reasons": reasons, "observed": observed})
        except Exception as exc:
            rec.update({"verdict": "error", "reasons": [f"{exc.__class__.__name__}: {exc}"[:400]], "trace": traceback.format_exc()[-1500:]})
        recs.append(rec)
        print(f"{rec['verdict']:12} {c['id']:6} {c['group']:15} {'; '.join(rec['reasons'])[:150]}")
    req = [r for r in recs if r["required"]]
    counts = {}
    for r in recs:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    full = a.cases == "all"
    all_pass = full and bool(req) and all(r["verdict"] == "pass" for r in req)
    out.update({"records": recs, "counts": counts, "scope": "full" if full else "subset",
                "all_required_pass": all_pass, "note": "test evidence only; never approval, selection, release or global readiness"})
    Path(a.out).write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    print("ALL REQUIRED PASS" if all_pass else "NOT ALL REQUIRED PASS", counts)
    return 0 if all_pass else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(3)
