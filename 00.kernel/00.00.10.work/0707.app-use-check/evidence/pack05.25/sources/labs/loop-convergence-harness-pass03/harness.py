#!/usr/bin/env python3
"""Executable acceptance harness pass03 (0707/05.24): explicit candidate identity (0420/06.57). NONPRODUCTION.
This file began as a byte copy of labs/loop-convergence-harness-pass02/harness.py. pass03 changes ONLY identity:
  - inputs: harness-inputs/3 explicit identity, or labelled legacy harness-inputs/2 for the two frozen baselines
    (labs/freshness-boundary-tests-pass02/identity.py); PENDING candidate stays all-blocked;
  - an execution-proof gate (controlled tamper of the declared workbook/open/reporter in NEW disposable copies)
    before any case; a DECOY refuses (exit 2);
  - the open entry, CTX-1's workbook and RP-2's tampered workbook come from the declared identity, not from a
    review_loop_tools_vN.py filename rule; RC-1 uses the declared builder (legacy: the frozen pass01 builder).
The 37 required ids, case requirements, verdict.py, judges.py and inputs_check.py are pass02's, imported hash-pinned.

(pass02 header follows)
Executable acceptance harness, versioned SUCCESSOR (0707/05.22) of labs/loop-convergence-harness-pass01 (0707/05.21).
NONPRODUCTION. Standard library only. pass01 stays frozen evidence; this file began as a byte copy of pass01/harness.py.

Successor changes (06.21.review H1-H4 and #04):
  H1  CAP-4, RP-1, RP-2 and IN-2 are executable callbacks: real candidate commands, judged by judges.py. Blocked
      while their input is pending; never an unconditional 'not-run' or a synthetic pass.
  H2  inputs are shape-checked (inputs_check.py) before anything runs; verdict.py type-checks every collection.
  H3  strict cases require 'malformed-n7-declaration', an unbound rejected alternative, record/publish refusal.
  H4  readiness is measured against the immutable full required baseline; --suite is a diagnostic subset (exit 4
      when every selected required case passed, still NOT READY).
  #04 N7-3 (N7 not-applicable on record and render); LR-6 requires the same-.NN destination; full inspect stdout kept.
All candidate commands go through RUN (default: a new process on the candidate's own app/librarian.py); unit tests
replace RUN with LABELLED scripted responses to test callback logic only, never app acceptance.

usage: harness.py --candidate DIR --inputs INPUTS.json --rooms NEW-DIR --out RESULT.json [--suite all|GROUP[,GROUP]]
exit:  0 READY (full scope only) · 1 NOT READY · 2 inputs refused before execution · 3 harness crash
       4 subset: every selected required case passed, but full coverage was not run (NOT READY)

Before anything runs: the inputs manifest is validated (schema, dependency rows, PENDING rows carry no pins, accepted
rows' files match live bytes, the frozen fixture manifest and retained judgments match), and the candidate root must
match the declared candidate file list exactly (every declared file, sha256, bytes). Any mismatch refuses (exit 2).
Every case runs the candidate's OWN app/librarian.py review-loop in a NEW process on a NEW copy of the candidate root,
with fixture sources copied from pack05.21 snapshots (or hash-verified manifest rows). Expected values come from fixture
facts and frozen Prime evidence computed by the harness, never from the candidate's own functions.
A case whose dependencies are not 'accepted' is recorded 'blocked' and not executed. Known baseline failures are
separate non-required records ('known-failure-reproduced') and never count toward readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LIVE = Path(r"D:\Git\lib-build")
P2 = LIVE / "labs/loop-convergence-harness-pass02"
_ROWS24 = {r["path"]: r for r in json.loads((LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.24/source-manifest.json").read_bytes())["files"]}
for _f in ("verdict.py", "judges.py", "inputs_check.py"):
    if hashlib.sha256((P2 / _f).read_bytes()).hexdigest() != _ROWS24[f"labs/loop-convergence-harness-pass02/{_f}"]["sha256"]:
        raise SystemExit(f"refused: pass02 {_f} differs from its pack05.24 freeze")
sys.path.insert(0, str(P2))                    # pass02's verdict/judges/inputs_check, unchanged and pinned above
sys.path.insert(0, str(LIVE / "labs/freshness-boundary-tests-pass02"))
from verdict import aggregate  # noqa: E402
import judges  # noqa: E402
from inputs_check import shape_problems  # noqa: E402
import identity as IDN  # noqa: E402
IDENT: dict = {}

sys.path.insert(0, str(LIVE / "labs/n7-local-lifecycle-pass01"))
import run_matrix as M  # noqa: E402   (fixture helpers from the accepted 05.20 lab; read-only import)
from run_matrix import rie, lifecycle, B, codes  # noqa: E402

RUN = rie.run                          # replaced only by labelled unit-test fixtures (test_callbacks.py)
PROVENANCE = "harness case (Claude, 0707/05.22 successor; 0707/05.24 explicit-identity pass03); not independent Prime review"
P1_BUILDER = LIVE / "labs/loop-convergence-harness-pass01/make_candidate.py"
BOOK = "00.kernel/00.00.10.work"
PACK21 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.21"
PACK22 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.22"
DISPATCHER_V7 = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
FIX = {
    "n5-0512-0506": ("0512.prime-review", "05.06", "05.06.md", "N5NN"),
    "n5-0522-0513": ("0522.review-construction", "05.13", "05.13.md", "N5NN"),
    "n5-0512-0509": ("0512.prime-review", "05.09", "05.09.md", "N5NN"),
    "n5-0522-0514": ("0522.review-construction", "05.14", "05.14.md", "N5NN"),
    "n5-0512-0510": ("0512.prime-review", "05.10", "05.10.md", "N5NN"),
    "n7-0515": ("0707.app-use-check", "05.15", "05.15.pack.md", "N7NN"),
    "n7-0517": ("0707.app-use-check", "05.17", "05.17.pack.md", "N7NN"),
}
LPAGE, OTHER, N5P = "0799.n7-local-lab", "0798.n7-other-lab", "0599.n5-control-lab"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    return sha(Path(p).read_bytes())


class Refused(Exception):
    pass


# ---------------------------------------------------------------- validation
def _pin_matches(f: dict) -> bool:
    p = LIVE / f["path"]
    return p.is_file() and p.stat().st_size == f["bytes"] and sha_file(p) == f["sha256"]


def validate(inputs, cand_root: Path | None):
    """pass03: PENDING candidate -> pass02 shape rules (all cases blocked); otherwise identity.resolve (explicit v3 or
    labelled legacy v2 baseline), then the unchanged pass02 dependency/fixture/judgment pins. Returns the identity."""
    if isinstance(inputs, dict) and inputs.get("candidate") != "PENDING":
        try:
            ident = IDN.resolve(inputs, cand_root, shape_problems) if cand_root is not None else None
        except IDN.Refused as exc:
            raise Refused(str(exc))
        if ident is None:
            raise Refused("no candidate root given")
        _deps_fixture_judgments(inputs)
        return ident
    problems = shape_problems(inputs)                       # H2: shapes first; nothing malformed reaches execution
    if problems:
        raise Refused("inputs malformed: " + "; ".join(problems[:12]))
    _deps_fixture_judgments(inputs)
    return None


def _deps_fixture_judgments(inputs) -> None:
    for dep in inputs["dependencies"]:
        if dep["status"] != "accepted":
            continue
        if not _pin_matches(dep["review_ref"]):
            raise Refused(f"accepted dependency {dep['id']}: frozen review reference differs: {dep['review_ref']['path']}")
        for f in dep["files"]:
            if not _pin_matches(f):
                raise Refused(f"accepted dependency {dep['id']} file differs: {f['path']}")
    if not _pin_matches(inputs["fixture_source"]):
        raise Refused("frozen fixture manifest differs")
    for j in inputs["judgments"]:
        if not _pin_matches(j):
            raise Refused(f"retained judgment differs: {j['id']}")
    # pass03: candidate file identity is checked by identity.resolve (every declared file, contained, hash+length).


# ---------------------------------------------------------------- fixtures (frozen sources only)
def frozen_map() -> dict:
    m = json.loads((PACK21 / "source-manifest.json").read_text(encoding="utf-8"))
    return {f["path"]: f for f in m["files"]}


FROZEN = None
CANDIDATE_FILES: set = set()


def put_source(root: Path, rel: str, want_sha: str | None = None, want_bytes: int | None = None) -> str:
    global FROZEN
    FROZEN = FROZEN or frozen_map()
    dst = root / rel
    if dst.exists():
        if want_sha and sha_file(dst) != want_sha:
            if rel in CANDIDATE_FILES:                 # run01: declared evidence at a candidate-owned path
                return "collision-candidate-owned"
            raise Refused(f"root already holds different bytes at {rel}")
        return "present"
    f = FROZEN.get(rel)
    if f and (want_sha is None or f["sha256"] == want_sha):
        data = (PACK21 / f["snapshot"]).read_bytes()
        if sha(data) != f["sha256"]:
            raise Refused(f"snapshot differs {rel}")
        src = "pack05.21-snapshot"
    else:
        if want_sha is None:
            raise Refused(f"{rel} is not frozen and has no declared hash")
        data = (LIVE / rel).read_bytes()
        if sha(data) != want_sha or (want_bytes is not None and len(data) != want_bytes):
            raise Refused(f"declared row {rel} differs from its manifest hash")
        src = "live-row-verified"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return src


def build_fixture(root: Path, key: str) -> dict:
    page, pas, pointer, kind = FIX[key]
    page_rel = f"{BOOK}/{page}"
    global FROZEN
    FROZEN = FROZEN or frozen_map()
    for rel in sorted(FROZEN):
        if rel.startswith(page_rel + "/") and rel.count("/") == page_rel.count("/") + 1 and rel.endswith(".md"):
            put_source(root, rel)
    text = (root / page_rel / pointer).read_bytes().decode("utf-8")
    declared = rie.declared_from_pointer(text, page_rel, kind)
    for role in ("Submission", "Artifact manifest"):
        rel, h, n = declared[role]
        put_source(root, rel, h, n)
    man = json.loads((root / declared["Artifact manifest"][0]).read_bytes())
    collisions = []
    for row in man["files"]:
        if put_source(root, row["path"], row["sha256"], row["bytes"]) == "collision-candidate-owned":
            collisions.append(row["path"])               # never overwritten; the measurement is expected to show it changed
    return {"declared": declared, "manifest_rows": [r["path"] for r in man["files"]], "page": page, "pass": pas, "kind": kind,
            "collisions": collisions}


def independent_source_count(root: Path, key: str, fx: dict) -> int:
    """Harness's own count of sources the record would carry: unique BOOK-root paths among the assignment page, the declared
    submission, the local N7 return (if present) and the book-rooted manifest rows. The manifest itself is not a source."""
    page, pas, pointer, kind = FIX[key]
    s = {f"{page}/{pointer}"}
    sub = fx["declared"]["Submission"][0]
    if sub.startswith(BOOK + "/"):
        s.add(sub[len(BOOK) + 1:])
    if kind == "N7NN" and (root / BOOK / page / f"{pas}.return.md").is_file():
        s.add(f"{page}/{pas}.return.md")
    for r in fx["manifest_rows"]:
        if r.startswith(BOOK + "/"):
            s.add(r[len(BOOK) + 1:])
    return len(s)


# ---------------------------------------------------------------- execution helpers
class Ctx:
    def __init__(self, cand: Path, inputs: dict, rooms: Path):
        self.cand, self.inputs, self.rooms = cand, inputs, rooms
        self.n = 0
        self.jf = rooms / "lab-judgment.json"
        self.jf.write_text(json.dumps(lifecycle.JUDGMENT, indent=1) + "\n", encoding="utf-8")
        self.open_entry = IDENT["open_entry"]                  # pass03: from the declared/legacy-resolved identity
        self.files = {f["path"]: f for f in IDENT["files"]}
        CANDIDATE_FILES.update(self.files)

    def room(self, cid: str) -> Path:
        dst = self.rooms / cid
        shutil.copytree(self.cand, dst)
        for rel, f in self.files.items():                      # identity re-checked on every copy
            if sha_file(dst / rel) != f["sha256"]:
                raise Refused(f"copied candidate differs at {rel}")
        return dst


def cmd(root: Path, page: str, pas: str, c: str, *extra) -> dict:
    root = Path(root)
    return RUN([root / "app/librarian.py", "review-loop", c, "--book", str(root / BOOK), "--source", page, "--pass", pas, *extra], root)


def report(root: Path, *args) -> dict:
    """The reporter through the candidate's own dispatcher route 'review-report' (the R interface in CONTRACT.md)."""
    root = Path(root)
    return RUN([root / "app/librarian.py", "review-report", *args], root)


def report_page(root: Path, page: str, pas: str) -> dict:
    return report(root, "--book", str(Path(root) / BOOK), "--source", page, "--pass", pas)


def baseline(root: Path, page: str, pas: str, c: str) -> dict:
    return rie.baseline(root, c, "--book", str(root / BOOK), "--source", page, "--pass", pas)


def open_(ctx: Ctx, root: Path, page: str, pas: str) -> dict | None:
    if not ctx.open_entry:
        return None
    return RUN([root / ctx.open_entry, "open", "--book", str(root / BOOK), "--source", page, "--pass", pas], root)


def summ(res: dict) -> dict:
    b = B(res)
    rows = rie.rows_of(b)
    return {"exit": res["exit"], "intake_id": b.get("intake_id"), "measurement": b.get("measurement"), "codes": codes(res),
            "rows_sha": sha(json.dumps(sorted(json.dumps(r, sort_keys=True) for r in rows)).encode()),
            "cuts_sha": sha(json.dumps(b.get("cuts"), sort_keys=True).encode())}


def local_pair(root: Path, page: str, pas: str, ctx: Ctx, opened: bool = True) -> dict:
    M.make_pack(root, page, pas)
    o = open_(ctx, root, page, pas) if opened else None
    m = M.make_return(root, page, pas)
    M.fill_pointer(root, page, pas, m["ret"], m["man"])
    return {"open": None if o is None else o["exit"], "m": m}


def ex_state(res: dict):
    return (B(res).get("exchange") or {}).get("state")


def record_and_inspect(root, page, pas, ctx, tag):
    p = cmd(root, page, pas, "prepare")
    rec = cmd(root, page, pas, "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    ins = cmd(root, page, pas, "inspect")
    chk = ctx.rooms / f"{tag}-inspect-checkpoint.json"
    full = ctx.rooms / f"{tag}-inspect.stdout"
    full.write_bytes(ins["stdout"].encode("utf-8"))           # successor: the FULL inspect output is kept, not only its hash
    rendered = B(ins).get("rendered")
    chk.write_text(json.dumps({"mechanism": "automated checkpoint: the harness captured the full inspect stdout to "
                                            f"{full.name}, required a non-empty 'rendered' text and stored hashes BEFORE invoking publish; "
                                            "this is not a human/model read. Prime's actual read stays a separate live gate.",
                               "inspect_stdout_file": full.name, "inspect_stdout_sha256": sha(ins["stdout"].encode()),
                               "rendered_sha256": sha(rendered.encode()) if isinstance(rendered, str) else None},
                              indent=1) + "\n", encoding="utf-8")
    return p, rec, ins, isinstance(rendered, str) and rendered.strip() != ""


# ---------------------------------------------------------------- cases
CASES = []


def case(cid, group, requirement, needs=(), required=True):
    def deco(fn):
        CASES.append({"id": cid, "group": group, "requirement": requirement, "needs": list(needs), "required": required, "fn": fn})
        return fn
    return deco


def V(ok: bool) -> str:
    return "pass" if ok else "fail"


@case("N5-1", "n5-same-cut", "N5 0512/05.06: candidate prepare equals the faithful pass03 baseline on the same root (intake_id, rows, cuts, findings)")
def n5_1(ctx):
    root = ctx.room("N5-1")
    build_fixture(root, "n5-0512-0506")
    c, b = summ(cmd(root, "0512.prime-review", "05.06", "prepare")), summ(baseline(root, "0512.prime-review", "05.06", "prepare"))
    keys = ("intake_id", "measurement", "codes", "rows_sha", "cuts_sha")
    diff = {k: (b[k], c[k]) for k in keys if b[k] != c[k]}
    return "baseline == candidate", {"diff": diff, "candidate": c}, V(not diff and c["exit"] == 0)


@case("N5-2", "n5-same-cut", "N5 0522/05.13: same-state equality with the baseline; the declared selection-induced change (app/librarian.py artifact) appears iff the dispatcher differs from c3a5be3b")
def n5_2(ctx):
    root = ctx.room("N5-2")
    fx = build_fixture(root, "n5-0522-0513")
    c, b = summ(cmd(root, "0522.review-construction", "05.13", "prepare")), summ(baseline(root, "0522.review-construction", "05.13", "prepare"))
    keys = ("intake_id", "measurement", "codes", "rows_sha", "cuts_sha")
    diff = {k: (b[k], c[k]) for k in keys if b[k] != c[k]}
    differs = sha_file(root / "app/librarian.py") != DISPATCHER_V7
    delta = "artifact-hash-mismatch" in c["codes"]
    expected_collisions = sorted(p for p in fx["collisions"])
    return ({"equal_to_baseline": True, "selection_delta_expected": differs, "declared_collisions": "candidate-owned paths only"},
            {"diff": diff, "selection_delta_observed": delta, "collisions": expected_collisions, "candidate": c},
            V(not diff and delta == bool(expected_collisions) and (not differs or "app/librarian.py" in expected_collisions)))


@case("N5-3", "n5-same-cut", "N5 legitimate filename punctuation (return.md, / ; / ) ) binds as before (candidate == baseline, file resolved)")
def n5_3(ctx):
    root = ctx.room("N5-3")
    out = {}
    for sfx in (",", ";", ")"):
        page = f"0597.n5-punct{('comma', 'semi', 'paren')[(',', ';', ')').index(sfx)]}"
        pdir = root / BOOK / page
        ev = pdir / "evidence/b"
        a = M.write(ev / "artifact.md", "LAB artifact\n")
        r = M.write(ev / f"return.md{sfx}", "LAB return with a legal punctuated name\n")
        man = M.write(ev / f"artifact-manifest.json{sfx}", json.dumps({"files": [{"path": f"{BOOK}/{page}/evidence/b/artifact.md", "bytes": len(a), "sha256": sha(a)}]}) + "\n")
        M.write(pdir / "05.01.md", f"# 05.01 LAB N5\n\n## Return pointer\nSubmission: {BOOK}/{page}/evidence/b/return.md{sfx} sha256 {sha(r)}, {len(r)} bytes.\n"
                                   f"Artifact manifest: {BOOK}/{page}/evidence/b/artifact-manifest.json{sfx} sha256 {sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")
        c, b = summ(cmd(root, page, "05.01", "prepare")), summ(baseline(root, page, "05.01", "prepare"))
        out[sfx] = {"equal": c["rows_sha"] == b["rows_sha"] and c["intake_id"] == b["intake_id"], "measurement": c["measurement"]}
    return "equal and complete for , ; )", out, V(all(v["equal"] and v["measurement"] == "complete" for v in out.values()))


def n7_valid(ctx, cid, key, expected):
    root = ctx.room(cid)
    fx = build_fixture(root, key)
    page, pas = FIX[key][0], FIX[key][1]
    r = cmd(root, page, pas, "prepare")
    rows = rie.rows_of(B(r))
    arts = {x.get("path") for x in rows if x.get("role") == "artifact"}
    exp_rows = len(fx["manifest_rows"])
    ex = B(r).get("exchange") or {}
    obs = {"measurement": B(r).get("measurement"), "artifacts": len(arts), "exchange_state": ex.get("state"), "n1_custody": ex.get("n1_custody"),
           "chronology": ex.get("chronology"), "codes": codes(r)}
    ok = (obs["measurement"] == "complete" and len(arts) == exp_rows == expected and obs["exchange_state"] == "matched"
          and obs["n1_custody"] == "not-applicable" and "custody-missing" not in obs["codes"])
    return {"artifacts": expected, "manifest_rows_counted_by_harness": exp_rows, "exchange": "matched", "n1_custody": "not-applicable"}, obs, V(ok)


@case("N7-1", "n7-valid", "N7 0707/05.15: complete, 26/26 artifacts, local pair matched, N1 not applicable", needs=("G", "L"))
def n7_1(ctx):
    return n7_valid(ctx, "N7-1", "n7-0515", 26)


@case("N7-2", "n7-valid", "N7 0707/05.17: complete, 33/33 artifacts, local pair matched, N1 not applicable", needs=("G", "L"))
def n7_2(ctx):
    return n7_valid(ctx, "N7-2", "n7-0517", 33)


def strict_case(ctx, cid, mutate, alternative):
    root = ctx.room(cid)
    fx = build_fixture(root, "n7-0515")
    pf = root / BOOK / "0707.app-use-check/05.15.pack.md"
    raw = pf.read_bytes().decode("utf-8")
    head, rest = raw.split("## Return pointer\n", 1)
    lines = [x for x in rest.split("\n## ", 1)[0].splitlines() if x.strip()]
    tail = ("\n## " + rest.split("\n## ", 1)[1]) if "\n## " in rest else ""
    lines = mutate(root, lines)
    pf.write_bytes((head + "## Return pointer\n" + "\n".join(lines) + "\n" + tail).encode("utf-8"))
    tgt = root / BOOK / "0707.app-use-check/06.15.review.md"
    before = tgt.read_bytes() if tgt.exists() else None
    p = cmd(root, "0707.app-use-check", "05.15", "prepare")
    rec = cmd(root, "0707.app-use-check", "05.15", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    pub = cmd(root, "0707.app-use-check", "05.15", "publish", "--review", B(rec).get("review_id") or "none")
    after = tgt.read_bytes() if tgt.exists() else None
    obs = {"measurement": B(p).get("measurement"), "codes": codes(p) if isinstance(B(p).get("findings"), list) else None,
           "bound_rows": [{"role": x.get("role"), "path": x.get("path")} for x in (rie.rows_of(B(p)) or B(p).get("rows") or []) if isinstance(x, dict)]
           if B(p) else None,
           "record_exit": rec["exit"], "publish_exit": pub["exit"], "destination_unchanged": before == after}
    return judges.strict(obs, alternative)                 # H3: the specific strict-grammar reason is required


@case("ST-1", "strict-n7", "trailing-text manifest line with a self-consistent decoy 'artifact-manifest.json,': reason malformed-n7-declaration; decoy not bound as artifact-manifest; record/publication refused", needs=("G",))
def st_1(ctx):
    def mut(root, lines):
        ev = root / BOOK / "0707.app-use-check/evidence/design05.15"
        ret = root / BOOK / "0707.app-use-check/05.15.return.md"
        d = json.dumps({"files": [{"path": f"{BOOK}/0707.app-use-check/05.15.return.md", "bytes": ret.stat().st_size, "sha256": sha_file(ret)}]}).encode() + b"\n"
        (ev / "artifact-manifest.json,").write_bytes(d)
        return [x for x in lines if not x.startswith("Artifact manifest:")] + [f"Artifact manifest: evidence/design05.15/artifact-manifest.json, sha256 {sha(d)}, {len(d)} bytes. note"]
    return strict_case(ctx, "ST-1", mut, ({"artifact-manifest"}, "evidence/design05.15/artifact-manifest.json,"))


@case("ST-2", "strict-n7", "a refused declaration (hash in attribution) beside a valid alternative Returned line: reason malformed-n7-declaration; the alternative 06.15.notes.md not bound as submission/return; refused", needs=("G",))
def st_2(ctx):
    def mut(root, lines):
        nb = (root / BOOK / "0707.app-use-check/06.15.notes.md").read_bytes()
        lines = [x.replace("(claude-opus-5-5, 2026-11-03)", f"(sha256 {'b' * 64})") if x.startswith("Returned:") else x for x in lines]
        return lines + [f"Returned: 06.15.notes.md (second line), sha256 {sha(nb)}, {len(nb)} bytes."]
    return strict_case(ctx, "ST-2", mut, ({"submission", "return"}, "06.15.notes.md"))


@case("ST-3", "strict-n7", "an incomplete recognized label ('Verification:' with no value): reason malformed-n7-declaration; record/publication refused", needs=("G",))
def st_3(ctx):
    return strict_case(ctx, "ST-3", lambda root, lines: lines + ["Verification:"], None)


@case("ST-4", "strict-n7", "control: legitimate N5 filename punctuation is NOT a malformed N7 declaration (no malformed-n7-declaration code; complete)")
def st_4(ctx):
    root = ctx.room("ST-4")
    out = {}
    for sfx, tag in ((",", "comma"), (";", "semi"), (")", "paren")):
        page = f"0596.n5-strict-ctl-{tag}"
        pdir = root / BOOK / page
        ev = pdir / "evidence/b"
        a = M.write(ev / "artifact.md", "LAB artifact\n")
        r = M.write(ev / f"return.md{sfx}", "LAB return with a legal punctuated name\n")
        man = M.write(ev / f"artifact-manifest.json{sfx}", json.dumps({"files": [{"path": f"{BOOK}/{page}/evidence/b/artifact.md", "bytes": len(a), "sha256": sha(a)}]}) + "\n")
        M.write(pdir / "05.01.md", f"# 05.01 LAB N5\n\n## Return pointer\nSubmission: {BOOK}/{page}/evidence/b/return.md{sfx} sha256 {sha(r)}, {len(r)} bytes.\n"
                                   f"Artifact manifest: {BOOK}/{page}/evidence/b/artifact-manifest.json{sfx} sha256 {sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")
        p = cmd(root, page, "05.01", "prepare")
        out[sfx] = {"measurement": B(p).get("measurement"), "codes": codes(p) if isinstance(B(p).get("findings"), list) else None}
    ok = all(v["measurement"] == "complete" and isinstance(v["codes"], list) and "malformed-n7-declaration" not in v["codes"] for v in out.values())
    return {"measurement": "complete", "malformed-n7-declaration": "absent"}, out, V(ok)


@case("LR-1", "n7-local", "orphan return (no pack): not matched; record refused; return bytes kept", needs=("L",))
def lr_1(ctx):
    root = ctx.room("LR-1")
    M.make_return(root, LPAGE, "05.01")
    rb = (root / BOOK / LPAGE / "05.01.return.md").read_bytes()
    p = cmd(root, LPAGE, "05.01", "prepare")
    rec = cmd(root, LPAGE, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    obs = {"state": ex_state(p), "measurement": B(p).get("measurement"), "record_exit": rec["exit"], "bytes_kept": (root / BOOK / LPAGE / "05.01.return.md").read_bytes() == rb}
    return {"state": "orphan-return", "record": "refused", "bytes_kept": True}, obs, V(obs["state"] == "orphan-return" and rec["exit"] != 0 and obs["bytes_kept"])


@case("LR-2", "n7-local", "wrong pass: pack 05.02 pointing at the 05.01 return is not a local match", needs=("L",))
def lr_2(ctx):
    root = ctx.room("LR-2")
    m = M.make_return(root, LPAGE, "05.01")
    M.make_pack(root, LPAGE, "05.02")
    M.fill_pointer(root, LPAGE, "05.02", m["ret"], m["man"])
    p = cmd(root, LPAGE, "05.02", "prepare")
    return {"state": "return-not-local", "measurement": "incomplete"}, {"state": ex_state(p), "measurement": B(p).get("measurement")}, \
        V(ex_state(p) == "return-not-local" and B(p).get("measurement") == "incomplete")


@case("LR-3", "n7-local", "wrong page: a return copied to another N7 page with no pack does not borrow a nearby pack", needs=("L",))
def lr_3(ctx):
    root = ctx.room("LR-3")
    local_pair(root, LPAGE, "05.01", ctx)
    M.write(root / BOOK / OTHER / "05.01.return.md", (root / BOOK / LPAGE / "05.01.return.md").read_bytes().decode("utf-8"))
    p = cmd(root, OTHER, "05.01", "prepare")
    return {"state": "orphan-return"}, {"state": ex_state(p), "assignment": B(p).get("assignment_path"), "measurement": B(p).get("measurement")}, \
        V(ex_state(p) == "orphan-return" and B(p).get("measurement") == "incomplete")


@case("LR-4", "n7-local", "foreign book: an N7 record copied into another book instance is not current there", needs=("L",))
def lr_4(ctx):
    root = ctx.room("LR-4")
    local_pair(root, LPAGE, "05.01", ctx)
    p = cmd(root, LPAGE, "05.01", "prepare")
    cmd(root, LPAGE, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    other = ctx.rooms / "LR-4-bookB"
    shutil.copytree(root, other)
    r = cmd(other, LPAGE, "05.01", "read")
    return "read in the copy: not current (exit != 0 or stale)", {"exit": r["exit"], "stale": B(r).get("stale")}, V(r["exit"] != 0 or B(r).get("stale") is True)


@case("LR-5", "n7-local", "existing history (0707/05.15): matched with chronology 'unverified' (Director 06.20)", needs=("L",))
def lr_5(ctx):
    root = ctx.room("LR-5")
    build_fixture(root, "n7-0515")
    p = cmd(root, "0707.app-use-check", "05.15", "prepare")
    ex = B(p).get("exchange") or {}
    return {"state": "matched", "chronology": "unverified"}, {"state": ex.get("state"), "chronology": ex.get("chronology")}, \
        V(ex.get("state") == "matched" and ex.get("chronology") == "unverified")


@case("LR-6", "n7-local", "new work: pack observed before return -> chronology 'recorded-before-return'; same .NN throughout", needs=("L",))
def lr_6(ctx):
    root = ctx.room("LR-6")
    lp = local_pair(root, LPAGE, "05.01", ctx)
    p = cmd(root, LPAGE, "05.01", "prepare")
    ex = B(p).get("exchange") or {}
    obs = {"open_exit": lp["open"], "state": ex.get("state"), "chronology": ex.get("chronology"), "return": (ex.get("return") or {}).get("path"),
           "destination": B(p).get("destination") or ex.get("destination")}
    want_dest = f"{LPAGE}/06.01.review.md"
    ok = (lp["open"] == 0 and ex.get("chronology") == "recorded-before-return" and ex.get("state") == "matched"
          and obs["return"] == f"{LPAGE}/05.01.return.md" and obs["destination"] == want_dest)
    return {"open_exit": 0, "chronology": "recorded-before-return", "return": f"{LPAGE}/05.01.return.md", "destination": want_dest}, obs, V(ok)


@case("N7-3", "n7-valid", "N7 not-applicable on record and render: a recorded local N7 pair stores and renders custody 'not-applicable' (never 'missing'); an N5 control keeps its N5 custody value", needs=("G", "L"))
def n7_3(ctx):
    root = ctx.room("N7-3")
    local_pair(root, LPAGE, "05.01", ctx)
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, "N7-3")
    rd = cmd(root, LPAGE, "05.01", "read")
    n5_page(root)
    q = cmd(root, N5P, "05.01", "prepare")
    cmd(root, N5P, "05.01", "record", "--intake", B(q).get("intake_id") or "none", "--judgment", str(ctx.jf))
    r5 = cmd(root, N5P, "05.01", "read")
    obs = {"record_exit": rec["exit"], "read_custody": B(rd).get("custody"), "rendered": B(ins).get("rendered"),
           "exchange": B(p).get("exchange"), "n5_control_custody": B(r5).get("custody")}
    e, o, v = judges.n7_custody(obs)
    o["rendered"] = None if not isinstance(o.get("rendered"), str) else f"{len(o['rendered'])} chars (full text in N7-3-inspect.stdout)"
    return e, o, v


@case("LR-7", "n7-local", "second pass binds only itself; the first pass's files and record stay byte-equal and current", needs=("L",))
def lr_7(ctx):
    root = ctx.room("LR-7")
    local_pair(root, LPAGE, "05.01", ctx)
    p, rec, ins, ok_ins = record_and_inspect(root, LPAGE, "05.01", ctx, "LR-7-p1")
    cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    before = {k: v for k, v in rie.tree_hashes(root).items() if "/05.01" in k or "/06.01" in k or "e0501" in k}
    local_pair(root, LPAGE, "05.02", ctx)
    p2, rec2, _i, _o = record_and_inspect(root, LPAGE, "05.02", ctx, "LR-7-p2")
    pub2 = cmd(root, LPAGE, "05.02", "publish", "--review", B(rec2).get("review_id") or "none")
    after = rie.tree_hashes(root)
    r1 = cmd(root, LPAGE, "05.01", "read")
    kept = all(after.get(k) == v for k, v in before.items())
    obs = {"pass2_state": ex_state(p2), "pass2_publish": pub2["exit"], "pass2_target": (root / BOOK / LPAGE / "06.02.review.md").is_file(),
           "pass1_kept": kept, "pass1_read": r1["exit"], "pass1_review_id_same": B(r1).get("review_id") == B(rec).get("review_id")}
    return "pass 2 matched and published to 06.02; pass 1 unchanged and current", obs, \
        V(obs["pass2_state"] == "matched" and pub2["exit"] == 0 and obs["pass2_target"] and kept and r1["exit"] == 0 and obs["pass1_review_id_same"])


@case("CAP-0", "capacity", "harness self-check: independently counted emitted sources equal Prime's measured 29 / 20 / 44")
def cap_0(ctx):
    root = ctx.room("CAP-0")
    got = {}
    for j in ctx.inputs["judgments"]:
        key = {"05.09": "n5-0512-0509", "05.14": "n5-0522-0514", "05.10": "n5-0512-0510"}[j["pass"]]
        fx = build_fixture(root, key)
        got[j["id"]] = {"expected": j["expected_sources"], "counted": independent_source_count(root, key, fx), "artifact_rows": len(fx["manifest_rows"])}
    return {k: v["expected"] for k, v in got.items()}, got, V(all(v["expected"] == v["counted"] for v in got.values()))


def cap_record(ctx, cid, jid):
    j = next(x for x in ctx.inputs["judgments"] if x["id"] == jid)
    key = {"05.09": "n5-0512-0509", "05.14": "n5-0522-0514", "05.10": "n5-0512-0510"}[j["pass"]]
    root = ctx.room(cid)
    build_fixture(root, key)
    p = cmd(root, j["page"], j["pass"], "prepare")
    rec = cmd(root, j["page"], j["pass"], "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(LIVE / j["path"]))
    rd = cmd(root, j["page"], j["pass"], "read")
    want = json.loads((LIVE / j["path"]).read_bytes())
    obs = {"measurement": B(p).get("measurement"), "record_exit": rec["exit"], "correction": B(rec).get("correction"),
           "judgment_canonically_equal": B(rd).get("judgment") == want}
    return obs


@case("CAP-1", "capacity", "retained 29-source judgment (0512/05.09) records and reads back canonically equal", needs=("K",))
def cap_1(ctx):
    o = cap_record(ctx, "CAP-1", "j-0512-0509")
    return "record exit 0; judgment equal", o, V(o["record_exit"] == 0 and o["judgment_canonically_equal"])


@case("CAP-2", "capacity", "retained 20-source judgment (0522/05.14) records and reads back canonically equal", needs=("K",))
def cap_2(ctx):
    o = cap_record(ctx, "CAP-2", "j-0522-0514")
    return "record exit 0; judgment equal", o, V(o["record_exit"] == 0 and o["judgment_canonically_equal"])


@case("CAP-3", "capacity", "retained 44-source judgment (0512/05.10, judgment-open) records and reads back canonically equal", needs=("K",))
def cap_3(ctx):
    o = cap_record(ctx, "CAP-3", "j-0512-0510")
    return "record exit 0; judgment equal", o, V(o["record_exit"] == 0 and o["judgment_canonically_equal"])


def cap_page(root: Path, page: str, n_sources: int) -> int:
    """LAB-ONLY synthetic N5 page whose harness-counted emitted sources are exactly n_sources: the assignment page,
    the submission and n_sources-2 distinct book-root artifact rows (the manifest itself is not a source; CAP-0
    checks this counting rule against Prime's measured 29/20/44). Returns the harness count."""
    pdir = root / BOOK / page
    ev = pdir / "e"
    rows = []
    for i in range(n_sources - 2):
        c = M.write(ev / f"a{i:02d}.md", f"LAB {page} artifact {i}\n")
        rows.append({"path": f"{BOOK}/{page}/e/a{i:02d}.md", "bytes": len(c), "sha256": sha(c)})
    s = M.write(ev / "s.md", f"LAB {page} submission\n")
    man = M.write(ev / "m.json", json.dumps({"files": rows}) + "\n")
    M.write(pdir / "05.01.md", f"# 05.01 LAB N5 capacity fixture\n\n## Goal\nLAB-ONLY.\n\n## Return pointer\n"
                               f"Submission: {BOOK}/{page}/e/s.md sha256 {sha(s)}, {len(s)} bytes.\n"
                               f"Artifact manifest: {BOOK}/{page}/e/m.json sha256 {sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")
    srcs = {f"{page}/05.01.md", f"{page}/e/s.md"} | {r["path"][len(BOOK) + 1:] for r in rows}
    return len(srcs)


def cap_try(ctx, root: Path, page: str, n: int, judgment: dict, tag: str) -> dict:
    count = cap_page(root, page, n)
    jf = ctx.rooms / f"{tag}-judgment.json"
    jf.write_bytes((json.dumps(judgment, indent=1) + "\n").encode("utf-8"))
    p = cmd(root, page, "05.01", "prepare")
    rec = cmd(root, page, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(jf))
    o = {"harness_count": count, "measurement": B(p).get("measurement"), "exit": rec["exit"], "record_exit": rec["exit"],
         "diagnostic": (json.dumps(B(rec).get("correction")) + " | " + rec["stderr"][-300:]), "stderr": rec["stderr"][-600:],
         "judgment_bytes": jf.stat().st_size}
    if rec["exit"] == 0:
        rd = cmd(root, page, "05.01", "read")
        o.update({"read_exit": rd["exit"], "judgment_equal": B(rd).get("judgment") == judgment})
    return o


@case("CAP-4", "capacity", "declared bound: 64 harness-counted sources record and read back equal; 65 refuse with an explicit 'sources' diagnostic; "
                           "separately, MAX_LIST 24 (25 reasons refused) and the 262144-byte document bound still hold with few sources", needs=("K",))
def cap_4(ctx):
    root = ctx.room("CAP-4")
    j = lifecycle.JUDGMENT
    j25 = dict(j, reasons=[f"LAB-ONLY reason {i}" for i in range(25)])
    jdoc = dict(j, reasons=[f"LAB-ONLY {i} " + "x" * 11000 for i in range(24)])
    obs = {"at_bound": cap_try(ctx, root, "0590.cap-64", 64, j, "CAP-4-64"),
           "over_bound": cap_try(ctx, root, "0591.cap-65", 65, j, "CAP-4-65"),
           "list25": cap_try(ctx, root, "0592.cap-list25", 3, j25, "CAP-4-list25"),
           "doc": cap_try(ctx, root, "0593.cap-doc", 3, jdoc, "CAP-4-doc")}
    return judges.cap4(obs, 64)


@case("KF-CAP", "capacity", "KNOWN FAILURE (baseline): the 29- and 44-source retained judgments are refused 'limit sources' at the old 24 bound", required=False)
def kf_cap(ctx):
    o29 = cap_record(ctx, "KF-CAP-29", "j-0512-0509")
    o44 = cap_record(ctx, "KF-CAP-44", "j-0512-0510")
    rep = all(o["record_exit"] == 2 and "limit sources" in str(o["correction"]) for o in (o29, o44))
    return "both refused 'limit sources'", {"29": o29, "44": o44}, "known-failure-reproduced" if rep else "known-failure-not-reproduced"


@case("LC-1", "lifecycle", "prepare/form -> record (supplied judgment) -> inspect checkpoint (full rendered output) -> SEPARATE publish -> read/recover x2 equal, no writes; no approval/release", needs=("L",))
def lc_1(ctx):
    root = ctx.room("LC-1")
    local_pair(root, LPAGE, "05.01", ctx)
    f = cmd(root, LPAGE, "05.01", "form")
    p, rec, ins, ok_ins = record_and_inspect(root, LPAGE, "05.01", ctx, "LC-1")
    pub = cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    t0 = rie.tree_hashes(root)
    rr = [cmd(root, LPAGE, "05.01", c) for c in ("read", "recover", "read", "recover")]
    t1 = rie.tree_hashes(root)
    flags = {k: B(pub).get(k) for k in ("accepted", "approved", "authority", "closes_work", "releases_action")}
    obs = {"form_exit": f["exit"], "record_exit": rec["exit"], "inspect_rendered_present": ok_ins, "publish_exit": pub["exit"],
           "target": (root / BOOK / LPAGE / "06.01.review.md").is_file(), "reads": [r["exit"] for r in rr],
           "repeat_equal": rr[0]["stdout"] == rr[2]["stdout"] and rr[1]["stdout"] == rr[3]["stdout"], "no_writes": t0 == t1,
           "judgment_equal": B(rr[0]).get("judgment") == lifecycle.JUDGMENT, "flags": flags}
    ok = (f["exit"] == 0 and rec["exit"] == 0 and ok_ins and pub["exit"] == 0 and obs["target"] and all(x == 0 for x in obs["reads"])
          and obs["repeat_equal"] and obs["no_writes"] and obs["judgment_equal"]
          and flags == {"accepted": False, "approved": False, "authority": "none", "closes_work": False, "releases_action": False})
    return "complete cycle; checkpoint stored before publish", obs, V(ok)


def preserve_room(ctx, cid):
    root = ctx.room(cid)
    local_pair(root, LPAGE, "05.01", ctx)
    return root


@case("PR-1", "preservation", "manual text present at the destination: publish held, bytes preserved, judgment retained", needs=("L",))
def pr_1(ctx):
    root = preserve_room(ctx, "PR-1")
    tgt = root / BOOK / LPAGE / "06.01.review.md"
    manual = b"# Prime review - LAB manual text\nDirector text: keep.\n"
    tgt.write_bytes(manual)
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, "PR-1")
    pub = cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    rd = cmd(root, LPAGE, "05.01", "read")
    obs = {"publish_exit": pub["exit"], "correction": B(pub).get("correction"), "bytes_kept": tgt.read_bytes() == manual, "judgment_equal": B(rd).get("judgment") == lifecycle.JUDGMENT}
    return "held; preserved; judgment equal", obs, V(pub["exit"] != 0 and obs["bytes_kept"] and obs["judgment_equal"])


@case("PR-2", "preservation", "a destination file appearing between inspect and publish: held, bytes preserved", needs=("L",))
def pr_2(ctx):
    root = preserve_room(ctx, "PR-2")
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, "PR-2")
    tgt = root / BOOK / LPAGE / "06.01.review.md"
    manual = b"# appeared after inspect\n"
    tgt.write_bytes(manual)
    pub = cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    return "held; preserved", {"publish_exit": pub["exit"], "bytes_kept": tgt.read_bytes() == manual}, V(pub["exit"] != 0 and tgt.read_bytes() == manual)


def changed(ctx, cid, act):
    root = preserve_room(ctx, cid)
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, cid)
    act(root / BOOK / LPAGE)
    rd = cmd(root, LPAGE, "05.01", "read")
    pub = cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    obs = {"read_exit": rd["exit"], "stale": B(rd).get("stale"), "publish_exit": pub["exit"], "target": (root / BOOK / LPAGE / "06.01.review.md").exists()}
    return obs


@case("PR-3", "preservation", "pack task-body change after record: stale; publication held", needs=("L",))
def pr_3(ctx):
    def act(d):
        x = d / "05.01.pack.md"
        x.write_bytes(x.read_bytes().replace(b"LAB-ONLY SYNTHETIC pack", b"LAB-ONLY SYNTHETIC pack CHANGED"))
    o = changed(ctx, "PR-3", act)
    return "stale; held", o, V(o["stale"] is True and o["publish_exit"] != 0 and not o["target"])


@case("PR-4", "preservation", "return change after record: stale; publication held", needs=("L",))
def pr_4(ctx):
    o = changed(ctx, "PR-4", lambda d: (d / "05.01.return.md").write_bytes((d / "05.01.return.md").read_bytes() + b"x\n"))
    return "stale; held", o, V(o["stale"] is True and o["publish_exit"] != 0 and not o["target"])


@case("PR-5", "preservation", "declared artifact changed or missing after record: stale; publication held", needs=("L",))
def pr_5(ctx):
    o1 = changed(ctx, "PR-5a", lambda d: (d / "evidence/e0501/a.md").write_bytes(b"changed\n"))
    o2 = changed(ctx, "PR-5b", lambda d: (d / "evidence/e0501/b.md").unlink())
    return "stale; held (both)", {"changed": o1, "missing": o2}, V(all(o["stale"] is True and o["publish_exit"] != 0 and not o["target"] for o in (o1, o2)))


@case("PR-6", "preservation", "review-region-only pack edit after publish keeps the exchange current; a task edit does not", needs=("L",))
def pr_6(ctx):
    root = preserve_room(ctx, "PR-6")
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, "PR-6")
    cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    pk = root / BOOK / LPAGE / "05.01.pack.md"
    keep = pk.read_bytes()
    pk.write_bytes(keep.replace(b"## Review - Codex Prime\nPENDING.", b"## Review - Codex Prime\nAccepted (LAB summary)."))
    a = cmd(root, LPAGE, "05.01", "read")
    pk.write_bytes(keep.replace(b"LAB-ONLY SYNTHETIC pack", b"LAB-ONLY SYNTHETIC pack (task edited)"))
    b = cmd(root, LPAGE, "05.01", "read")
    return {"review_edit": "current", "task_edit": "stale"}, {"review_edit": {"exit": a["exit"], "stale": B(a).get("stale")}, "task_edit": {"exit": b["exit"], "stale": B(b).get("stale")}}, \
        V(a["exit"] == 0 and B(a).get("stale") is False and B(b).get("stale") is True)


@case("PR-7", "preservation", "missing or altered pinned tool refuses before work (door pin)")
def pr_7(ctx):
    root = ctx.room("PR-7")
    build_fixture(root, "n5-0512-0506")
    (root / "labs/prime-cycle-pass03/prime_cycle.py").write_bytes((root / "labs/prime-cycle-pass03/prime_cycle.py").read_bytes() + b"\n# tamper\n")
    r = cmd(root, "0512.prime-review", "05.06", "prepare")
    return "exit 2 with a pin refusal", {"exit": r["exit"], "stderr": r["stderr"][-200:]}, V(r["exit"] == 2 and "pin" in r["stderr"].lower())


@case("CTX-1", "preservation", "source-kind context resets: in-process N5 -> N7 -> N5 intakes equal fresh-process prepares", needs=("L",))
def ctx_1(ctx):
    root = ctx.room("CTX-1")
    build_fixture(root, "n5-0512-0506")
    build_fixture(root, "n7-0515")
    calls = [("0512.prime-review", "05.06"), ("0707.app-use-check", "05.15"), ("0512.prime-review", "05.06")]
    fresh = [B(cmd(root, pg, ps, "prepare")).get("intake_id") for pg, ps in calls]
    wbrel = IDENT["workbook_entry"]          # pass03: the declared workbook (proved executed by the gate), no filename rule
    spec = importlib.util.spec_from_file_location("harness_candidate_workbook", root / wbrel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    build = getattr(mod, "build_intake", None) or mod.p3.p2.build_intake
    inproc = [build(root / BOOK, pg, ps)["intake_id"] for pg, ps in calls]
    return "in-process ids == fresh-process ids", {"fresh": fresh, "in_process": inproc, "workbook": wbrel}, V(fresh == inproc and fresh[0] == fresh[2])


def core_obs(root: Path, page: str, pas: str) -> dict:
    rd = cmd(root, page, pas, "read")
    p = cmd(root, page, pas, "prepare")
    return {"exit": rd["exit"], "stale": B(rd).get("stale"), "review_id": B(rd).get("review_id"), "custody": B(rd).get("custody"),
            "exchange": B(p).get("exchange"), "measurement": B(p).get("measurement")}


def rep_obs(res: dict) -> dict:
    return {"exit": res["exit"], "body": res.get("body") if isinstance(res.get("body"), dict) else None, "stderr": res["stderr"][-400:]}


def published_pair(ctx, cid: str) -> Path:
    root = ctx.room(cid)
    local_pair(root, LPAGE, "05.01", ctx)
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, cid)
    cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    return root


@case("RP-1", "reporter", "review-report (candidate route) agrees with the core: published N7 current -> readable/stale false; changed return -> stale; "
                          "incomplete intake -> held; N7 exchange state/chronology/n1_custody, custody and review_id equal to the core; "
                          "authority none and accepted/work_complete/action_released/releases_action false", needs=("R",))
def rp_1(ctx):
    cur = published_pair(ctx, "RP-1-current")
    o_cur = {"core": core_obs(cur, LPAGE, "05.01"), "report": rep_obs(report_page(cur, LPAGE, "05.01"))}
    st = published_pair(ctx, "RP-1-stale")
    f = st / BOOK / LPAGE / "05.01.return.md"
    f.write_bytes(f.read_bytes() + b"LAB change after publish\n")
    o_st = {"core": core_obs(st, LPAGE, "05.01"), "report": rep_obs(report_page(st, LPAGE, "05.01"))}
    hd = ctx.room("RP-1-held")
    local_pair(hd, LPAGE, "05.01", ctx)
    (hd / BOOK / LPAGE / "evidence/e0501/b.md").unlink()
    o_hd = {"core": core_obs(hd, LPAGE, "05.01"), "report": rep_obs(report_page(hd, LPAGE, "05.01"))}
    return judges.rp1({"current": o_cur, "stale": o_st, "held": o_hd})


def selected_workbook(root: Path) -> str:
    """pass03: the declared workbook_entry (legacy baselines: the labelled legacy discovery), never a filename guess."""
    return IDENT["workbook_entry"]


def tampered(root: Path, rel: str, fn):
    f = root / rel
    keep = f.read_bytes()
    f.write_bytes(keep + b"\n# LAB tamper (RP-2)\n")
    try:
        return fn()
    finally:
        f.write_bytes(keep)


@case("RP-2", "reporter", "review-report refuses (nonzero, no traceback) a wrong dispatcher pin, a wrong chain (workbook) pin and malformed envelopes "
                          "(unknown flag, repeated flag, relative book, bad pass, missing source), after an untampered positive control succeeds", needs=("R",))
def rp_2(ctx):
    root = published_pair(ctx, "RP-2")
    bk = str(root / BOOK)
    base = ["--book", bk, "--source", LPAGE, "--pass", "05.01"]
    obs = {"control": rep_obs(report(root, *base))}
    obs["wrong-dispatcher"] = rep_obs(tampered(root, "app/librarian.py", lambda: report(root, *base)))
    obs["wrong-chain-pin"] = rep_obs(tampered(root, selected_workbook(root), lambda: report(root, *base)))
    obs["unknown-flag"] = rep_obs(report(root, *base, "--bogus", "x"))
    obs["repeated-flag"] = rep_obs(report(root, *base, "--pass", "05.01"))
    obs["relative-book"] = rep_obs(report(root, "--book", BOOK, "--source", LPAGE, "--pass", "05.01"))
    obs["bad-pass"] = rep_obs(report(root, "--book", bk, "--source", LPAGE, "--pass", "5.1"))
    obs["missing-source"] = rep_obs(report(root, "--book", bk, "--pass", "05.01"))
    obs["control_after"] = rep_obs(report(root, *base))
    return judges.rp2(obs)


@case("KF-RP", "reporter", "KNOWN FAILURE (baseline): the frozen reporter v3 refuses this candidate's dispatcher (pins only f1d23d45)", required=False)
def kf_rp(ctx):
    root = ctx.room("KF-RP")
    build_fixture(root, "n5-0512-0506")
    decl = json.loads((LIVE / "app/review-report-v3.json").read_bytes())
    for rel in ("app/review_report_tools_v3.py", "app/review-report-v3.json"):
        (root / rel).write_bytes((LIVE / rel).read_bytes())
    for rel, pin in decl["tools"].items():
        if rel == "app/librarian.py" or (root / rel).exists():
            continue
        data = (LIVE / rel).read_bytes()
        if sha(data) == pin["sha256"]:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(data)
    disp = (root / "app/librarian.py").read_bytes()
    if b"review-report" not in disp:
        return "refusal", {"note": "candidate dispatcher has no review-report route at all"}, "known-failure-reproduced"
    r = rie.run([root / "app/librarian.py", "review-report", "--book", str(root / BOOK), "--source", "0512.prime-review", "--pass", "05.06"], cwd=root)
    return "refusal", {"exit": r["exit"], "stderr": r["stderr"][-200:]}, "known-failure-reproduced" if r["exit"] != 0 else "known-failure-not-reproduced"


def n5_page(root: Path) -> None:
    pdir = root / BOOK / N5P
    ev = pdir / "evidence/b"
    a = M.write(ev / "artifact.md", "LAB N5 artifact\n")
    s = M.write(ev / "submission.md", "LAB N5 submission\n")
    man = M.write(ev / "artifact-manifest.json", json.dumps({"files": [{"path": f"{BOOK}/{N5P}/evidence/b/artifact.md", "bytes": len(a), "sha256": sha(a)}]}) + "\n")
    M.write(pdir / "05.01.md", f"# 05.01 LAB N5\n\n## Goal\nLAB.\n\n## Return pointer\nSubmission: {BOOK}/{N5P}/evidence/b/submission.md sha256 {sha(s)}, {len(s)} bytes.\n"
                               f"Artifact manifest: {BOOK}/{N5P}/evidence/b/artifact-manifest.json sha256 {sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")


@case("IN-1", "instance", "N5 same book: record then read is current (exit 0, not stale)")
def in_1(ctx):
    root = ctx.room("IN-1")
    n5_page(root)
    p = cmd(root, N5P, "05.01", "prepare")
    rec = cmd(root, N5P, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    rd = cmd(root, N5P, "05.01", "read")
    return "current", {"record_exit": rec["exit"], "read_exit": rd["exit"], "stale": B(rd).get("stale")}, V(rec["exit"] == 0 and rd["exit"] == 0 and B(rd).get("stale") is False)


def read_obs(res: dict) -> dict:
    b = B(res)
    app = b.get("applicable")
    return {"exit": res["exit"], "stale": b.get("stale"), "applicable": app if isinstance(app, bool) else None,
            "judgment": b.get("judgment"), "stderr": res["stderr"][-400:]}


@case("IN-2", "instance", "N5 foreign copied book: the copy's current applicability is held (positive evidence: nonzero read, stale or applicable=false), "
                          "the historical judgment stays available (read or recover), publish is refused with no destination; "
                          "the original stays current and byte-unchanged", needs=("I",))
def in_2(ctx):
    a = ctx.room("IN-2")
    n5_page(a)
    p = cmd(a, N5P, "05.01", "prepare")
    rec = cmd(a, N5P, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    a0 = read_obs(cmd(a, N5P, "05.01", "read"))
    t_a = rie.tree_hashes(a)
    b = ctx.rooms / "IN-2-bookB"
    shutil.copytree(a, b)
    br = read_obs(cmd(b, N5P, "05.01", "read"))
    bc = read_obs(cmd(b, N5P, "05.01", "recover"))
    page_before = {k: v for k, v in rie.tree_hashes(b).items() if k.startswith(N5P + "/")}
    bp = cmd(b, N5P, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    page_after = {k: v for k, v in rie.tree_hashes(b).items() if k.startswith(N5P + "/")}
    a1 = read_obs(cmd(a, N5P, "05.01", "read"))
    obs = {"a_record_exit": rec["exit"], "a_read_before": a0, "a_read_after": a1, "a_bytes_unchanged": rie.tree_hashes(a) == t_a,
           "b_read": br, "b_recover": bc, "b_publish": {"exit": bp["exit"], "stderr": bp["stderr"][-400:]},
           "b_destination_created": sorted(set(page_after) - set(page_before)) != [] or page_after != page_before}
    e, o, v = judges.in2(obs, lifecycle.JUDGMENT)
    for k in ("a_read_before", "a_read_after", "b_read", "b_recover"):
        o[k] = dict(o[k], judgment="(equal to the lab judgment)" if o[k].get("judgment") == lifecycle.JUDGMENT else o[k].get("judgment") and "(differs)")
    return e, o, v


@case("KF-IN", "instance", "KNOWN FAILURE (baseline): an N5 record in a byte-copied book reads current in the copy", required=False)
def kf_in(ctx):
    root = ctx.room("KF-IN")
    n5_page(root)
    p = cmd(root, N5P, "05.01", "prepare")
    cmd(root, N5P, "05.01", "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(ctx.jf))
    other = ctx.rooms / "KF-IN-bookB"
    shutil.copytree(root, other)
    rd = cmd(other, N5P, "05.01", "read")
    rep = rd["exit"] == 0 and B(rd).get("stale") is False
    return "copy reads current (defect)", {"exit": rd["exit"], "stale": B(rd).get("stale")}, "known-failure-reproduced" if rep else "known-failure-not-reproduced"


@case("RC-1", "reconstruction", "a NEW root rebuilt by the declared builder from frozen sources has the identical candidate file list, and reproduces N7-1 rows")
def rc_1(ctx):
    import subprocess
    new = ctx.rooms / "RC-1-rebuilt"
    kind = ctx.inputs["candidate"]["kind"]
    if IDENT["mode"] == "explicit":       # pass03: a new candidate must declare its own frozen builder
        bld = ctx.inputs["candidate"].get("builder")
        if not (isinstance(bld, dict) and isinstance(bld.get("args"), list) and all(isinstance(x, str) for x in bld["args"])
                and IDN.path_problem(bld.get("path")) is None and (LIVE / bld["path"]).is_file()
                and sha_file(LIVE / bld["path"]) == bld.get("sha256") and (LIVE / bld["path"]).stat().st_size == bld.get("bytes")):
            return "a declared, frozen builder {path, sha256, bytes, args}", {"builder": bld}, "fail"
        p = subprocess.run([sys.executable, "-B", str(LIVE / bld["path"]), *bld["args"], "--root", str(new)], capture_output=True, text=True)
        if p.returncode != 0:
            return "rebuild ok", {"exit": p.returncode, "stderr": p.stderr[-300:]}, "fail"
        same = all((new / f["path"]).is_file() and sha_file(new / f["path"]) == f["sha256"] for f in IDENT["files"])
        r1 = ctx.room("RC-1-orig")
        build_fixture(r1, "n7-0515")
        shutil.copytree(new, ctx.rooms / "RC-1-new")
        r2 = ctx.rooms / "RC-1-new"
        build_fixture(r2, "n7-0515")
        s1, s2 = summ(cmd(r1, "0707.app-use-check", "05.15", "prepare")), summ(cmd(r2, "0707.app-use-check", "05.15", "prepare"))
        return "identical declared files; identical rows/cuts", {"files_equal": same, "rows_equal": s1["rows_sha"] == s2["rows_sha"]}, \
            V(same and s1["rows_sha"] == s2["rows_sha"] and s1["cuts_sha"] == s2["cuts_sha"])
    want = json.loads((PACK22 / "source-manifest.json").read_bytes())
    row = next(f for f in want["files"] if f["path"] == "labs/loop-convergence-harness-pass01/make_candidate.py")
    if sha_file(P1_BUILDER) != row["sha256"]:
        raise Refused("the declared candidate builder (pass01 make_candidate.py) differs from its pack05.22 freeze")
    p = subprocess.run([sys.executable, "-B", str(P1_BUILDER), "--kind", kind, "--root", str(new)], capture_output=True, text=True)
    if p.returncode != 0:
        return "rebuild ok", {"exit": p.returncode, "stderr": p.stderr[-300:]}, "fail"
    a = {f["path"]: f["sha256"] for f in json.loads((new / "CANDIDATE.json").read_bytes())["files"]}
    b = {f["path"]: f["sha256"] for f in ctx.inputs["candidate"]["files"]}
    r1 = ctx.room("RC-1-orig")
    build_fixture(r1, "n7-0515")
    shutil.copytree(new, ctx.rooms / "RC-1-new")
    r2 = ctx.rooms / "RC-1-new"
    build_fixture(r2, "n7-0515")
    s1, s2 = summ(cmd(r1, "0707.app-use-check", "05.15", "prepare")), summ(cmd(r2, "0707.app-use-check", "05.15", "prepare"))
    return "identical files; identical rows/cuts", {"files_equal": a == b, "rows_equal": s1["rows_sha"] == s2["rows_sha"], "cuts_equal": s1["cuts_sha"] == s2["cuts_sha"]}, \
        V(a == b and s1["rows_sha"] == s2["rows_sha"] and s1["cuts_sha"] == s2["cuts_sha"])


@case("RB-1", "rollback", "restore the v7 dispatcher on a copy: new N7 records are kept byte-equal and reported non-current (held), not silently fresh; re-selecting restores current", needs=("L",))
def rb_1(ctx):
    root = ctx.room("RB-1")
    local_pair(root, LPAGE, "05.01", ctx)
    p, rec, ins, _ = record_and_inspect(root, LPAGE, "05.01", ctx, "RB-1")
    cmd(root, LPAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    cand_disp = (root / "app/librarian.py").read_bytes()
    store = {k: v for k, v in rie.tree_hashes(root).items() if k.startswith("workbook-review/")}
    (root / "app/librarian.py").write_bytes((LIVE / "app/librarian.py").read_bytes())
    r7 = cmd(root, LPAGE, "05.01", "read")
    kept = all(rie.tree_hashes(root).get(k) == v for k, v in store.items())
    (root / "app/librarian.py").write_bytes(cand_disp)
    r8 = cmd(root, LPAGE, "05.01", "read")
    obs = {"v7_read_exit": r7["exit"], "v7_stale": B(r7).get("stale"), "records_kept": kept, "reselect_exit": r8["exit"], "reselect_stale": B(r8).get("stale")}
    return "v7: non-current; records kept; reselect current", obs, V(r7["exit"] != 0 and kept and r8["exit"] == 0 and B(r8).get("stale") is False)


# ---------------------------------------------------------------- driver
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate")
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--suite", default="all")
    a = ap.parse_args()
    inputs = json.loads(Path(a.inputs).read_text(encoding="utf-8"))
    cand = Path(a.candidate) if a.candidate else None
    out = {"schema": "harness-result/1", "inputs": a.inputs, "inputs_sha256": sha_file(a.inputs), "candidate": str(cand) if cand else None}
    try:
        resolved = validate(inputs, cand)
        if resolved is not None:                     # pass03: identity + execution proof BEFORE any case
            IDENT.clear()
            IDENT.update(resolved)
            _s = importlib.util.spec_from_file_location("fbt_pass02_run", LIVE / "labs/freshness-boundary-tests-pass02/run.py")
            FBT2 = importlib.util.module_from_spec(_s)       # explicit path: gate + probes (no sys.path name lookup)
            _s.loader.exec_module(FBT2)
            try:
                out["execution_proof"] = FBT2.gate(resolved, cand, Path(a.rooms + "-proof"))
            except IDN.Refused as exc:
                raise Refused(str(exc))
            out.update({"identity_mode": resolved["mode"], "workbook_entry": resolved["workbook_entry"], "open_entry": resolved["open_entry"]})
    except Refused as exc:
        out.update({"refused": str(exc), "ready": False, "records": []})
        Path(a.out).write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
        print("REFUSED:", exc)
        return 2
    try:
        selected = select(CASES, a.suite)
    except Refused as exc:
        out.update({"refused": str(exc), "ready": False, "records": []})
        Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print("REFUSED:", exc)
        return 2
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    ctx = None if inputs["candidate"] == "PENDING" else Ctx(cand, inputs, rooms)
    ident = {"candidate_json_sha256": None if ctx is None else inputs["candidate"]["candidate_json_sha256"], "kind": None if ctx is None else inputs["candidate"]["kind"]}
    records = run_cases(selected, inputs["dependencies"], ctx, rooms, ident, echo=True)
    agg, code = decide(CASES, selected, records, inputs["dependencies"])
    out.update({"suite": a.suite, "ready": agg["ready"], "exit_meaning": EXIT_MEANING[code], "aggregate": agg, "records": records})
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("READY" if agg["ready"] else "NOT READY", f"scope={agg['scope']}", agg["counts"])
    for r in agg["reasons"][:40]:
        print("  -", r)
    return code


EXIT_MEANING = {0: "READY (full scope)", 1: "NOT READY", 2: "refused before execution", 3: "harness crash",
                4: "NOT READY: subset passed but full required coverage was not run"}


def full_required(registry: list) -> list:
    """The immutable readiness baseline: every required case in the registry, regardless of --suite (06.21 H4)."""
    return [c["id"] for c in registry if c["required"]]


def select(registry: list, suite) -> list:
    if suite == "all":
        return list(registry)
    if not isinstance(suite, str) or not suite.strip():
        raise Refused("--suite must be 'all' or a comma-separated list of group names")
    groups = [g for g in suite.split(",")]
    known = {c["group"] for c in registry}
    unknown = [g for g in groups if g not in known]
    if unknown or not groups:
        raise Refused(f"--suite names unknown groups {unknown}; known: {sorted(known)}")
    return [c for c in registry if c["group"] in set(groups)]


def run_cases(selected: list, dependencies: list, ctx, rooms: Path, ident: dict, echo: bool = False) -> list:
    deps = {d["id"]: d for d in dependencies}
    records = []
    for c in selected:
        rec = {"id": c["id"], "group": c["group"], "requirement": c["requirement"], "required": c["required"], "needs": c["needs"],
               "candidate": ident, "provenance": PROVENANCE}
        pending = [n for n in c["needs"] if deps.get(n, {}).get("status") != "accepted"]
        if ctx is None:
            rec.update({"expected": "-", "observed": "candidate PENDING", "verdict": "blocked", "evidence": "no candidate declared"})
        elif pending:
            rec.update({"expected": "-", "observed": f"dependencies not accepted: {pending}", "verdict": "blocked", "evidence": "inputs manifest"})
        else:
            try:
                expected, observed, verdict = c["fn"](ctx)
                rec.update({"expected": expected, "observed": observed, "verdict": verdict, "evidence": str(rooms / c["id"])})
            except Exception as exc:
                rec.update({"expected": "-", "observed": f"{exc.__class__.__name__}: {exc}"[:500], "verdict": "error",
                            "evidence": traceback.format_exc()[-1500:]})
        records.append(rec)
        if echo:
            print(f"{rec['verdict']:28} {c['id']:7} {c['group']:15} {c['requirement'][:90]}")
    return records


def decide(registry: list, selected: list, records: list, dependencies) -> tuple:
    full = full_required(registry)
    sel = [c["id"] for c in selected if c["required"]]
    agg = aggregate(records, full, dependencies, selected_required=sel)
    if agg["ready"]:
        return agg, 0
    if agg["scope"] == "subset" and agg["subset"]["all_selected_required_pass"] and not any(
            r.startswith("dependency") or r.startswith("malformed") for r in agg["reasons"]):
        return agg, 4
    return agg, 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(3)
