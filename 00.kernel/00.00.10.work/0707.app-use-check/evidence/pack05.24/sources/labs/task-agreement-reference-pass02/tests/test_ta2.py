#!/usr/bin/env python3
"""pass02 tests (0707/05.15). NONPRODUCTION. Every case runs the CLI as a NEW process on retained external fixtures.

Labels:
  known-failure reproduction: Prime's disclosed 06.14 failures (J1 fences, J2 binding path), run against
    pass01 FIRST (must reproduce) and then pass02 (must be fixed);
  author test: new targeted cases written for J1-J3 and compatibility;
  compat observation: exact frozen-helper behavior, recorded as observed (not changed to fit).
Assertions use concrete values; independent slices are computed by the test itself.
usage: test_ta2.py --root DIR(new, outside the checkout) --out FILE(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TA2 = HERE.parent / "ta2.py"
TA1 = HERE.parents[1] / "task-agreement-reference-pass01" / "ta.py"
CHECKOUT = HERE.parents[2]
M = "SYNTHETIC FIXTURE - 0707/05.15 lab. Not live work, not a Director record, not authority."
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(tool: Path, *args):
    p = subprocess.run([sys.executable, "-B", str(tool), *map(str, args)], capture_output=True, timeout=60, env=ENV)
    out = p.stdout.decode("utf-8", "replace")
    try:
        body = json.loads(out) if out.strip() else None
    except json.JSONDecodeError:
        body = None
    return p.returncode, body, p.stderr.decode("utf-8", "replace")


def tree(root: Path) -> str:
    return sha("\n".join(f"{q.relative_to(root).as_posix()} {sha(q.read_bytes())}" for q in sorted(root.rglob("*")) if q.is_file()).encode())


def write(p: Path, text: str, crlf=False) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    return p


def book(r: Path, goal_extra: str = "", crlf=False) -> Path:
    w = r / "book" / "00.00.10.work"
    write(w / "0412x.standing/01.md", f"# 01\n{M}\n\n## Local work agreement\nRecords goal, scope, choices.\n\n## Other\nx\n", crlf)
    write(w / "0412x.standing/evidence/director-agreement.md", f"# agreement\n{M}\nHard stop on forks.\n", crlf)
    write(w / "0599.fixture-task/06.02.decisions.md", f"# 06.02\n{M}\n\n## Director - verbatim\nSYNTHETIC: Ok pack it\n\n## Prime - exact proposal this reply approves\nParser in labs/x only.\n", crlf)
    write(w / "0599.fixture-task/05.02.md", f"# 05.02\n{M}\n\n## Goal\nAdd a parser.\n{goal_extra}\n## Scope\nLabs only.\n\n## Finish\nReturn tests.\n\n## Return pointer\nPENDING.\n", crlf)
    return w


def choices(**over):
    c = {"schema": "task-agreement-choices/1", "for": {"page": "0599.fixture-task", "pass": "05.02"},
         "fields": {"goal": {"state": "cited", "refs": [{"source": "self", "heading": "Goal"}]},
                    "scope": {"state": "cited", "refs": [{"source": "self", "heading": "Scope"}]},
                    "finish_criteria": {"state": "cited", "refs": [{"source": "self", "heading": "Finish"}]},
                    "prime_discretion": {"state": "cited", "refs": [{"source": "0412x.standing/01.md", "heading": "Local work agreement", "applicability": "standing"}]},
                    "director_required": {"state": "cited", "refs": [{"source": "0412x.standing/evidence/director-agreement.md", "whole": True, "applicability": "standing"}]},
                    "recorded_decisions": {"state": "cited", "decisions": [{"record": "0599.fixture-task/06.02.decisions.md", "verbatim": "Director - verbatim",
                                                                            "interpretation": "Prime - exact proposal this reply approves",
                                                                            "answers": {"source": "same", "heading": "Prime - exact proposal this reply approves"}}]}},
         "semantic_findings": [], "gloss": None}
    c["fields"].update(over)
    return c


def flow2(r: Path, w: Path, ch=None) -> Path:
    """pass02 construct -> assemble -> freeze-copy -> bind; returns the binding path."""
    cf = write(r / "in/choices.json", json.dumps(ch or choices()))
    rc, _, e = run(TA2, "construct", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/construct.json")
    assert rc == 0, e
    pack = w / "0599.fixture-task/05.02.md"
    rc, _, e = run(TA2, "assemble", "--lab-root", r, "--pack", pack, "--construct", r / "out/construct.json", "--out", r / "out/assembled.md")
    assert rc == 0, e
    pack.write_bytes((r / "out/assembled.md").read_bytes())
    rc, _, e = run(TA2, "bind", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/binding.json")
    assert rc == 0, e
    return r / "out/binding.json"


CASES = []


def case(cid, label, says):
    def deco(fn):
        CASES.append((cid, label, says, fn))
        return fn
    return deco


FENCES = {"tilde": "~~~\n## Goal\nexample\n~~~\n", "long_backtick": "````\n```\n## Goal\n```\n````\n", "indented": "   ```\n## Goal\n   ```\n"}


def fence_case(kind):
    def fn(r: Path):
        out = {}
        for tool, name in ((TA1, "pass01"), (TA2, "pass02")):
            rr = r / name
            w = book(rr, goal_extra="\n" + FENCES[kind])
            cf = write(rr / "in/c.json", json.dumps(choices()))
            extra = ["--lab-root", rr] if tool is TA2 else []
            rc, _, e = run(tool, "construct", *extra, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", rr / "out/c.json")
            out[name] = {"exit": rc, "count2": "count 2" in e}
        ok = out["pass01"]["exit"] == 2 and out["pass01"]["count2"] and out["pass02"]["exit"] == 0
        return ok, out
    return fn


for k in FENCES:
    case(f"KR-{k}", "known-failure reproduction", f"J1 {k} fence: pass01 counts a fenced Goal (count 2); pass02 selects only the real Goal")(fence_case(k))


@case("KR-pointer", "known-failure reproduction", "J1 consequence: a fenced '## Return pointer' truncates the pass01 pack cut; pass02 keeps the block inside the cut")
def kr_pointer(r: Path):
    res = {}
    for tool, name in ((TA1, "pass01"), (TA2, "pass02")):
        rr = r / name
        w = book(rr, goal_extra="\n~~~\n## Return pointer\nexample only\n~~~\n")
        cf = write(rr / "in/c.json", json.dumps(choices()))
        lab = ["--lab-root", rr] if tool is TA2 else []
        rc1, _, e1 = run(tool, "construct", *lab, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", rr / "out/c.json")
        pack = w / "0599.fixture-task/05.02.md"
        rc2, _, e2 = run(tool, "assemble", *lab, "--pack", pack, "--construct", rr / "out/c.json", "--out", rr / "out/a.md")
        res[name] = {"construct": rc1, "construct_err": e1.strip()[-160:], "assemble": rc2, "assemble_err": e2.strip()[-120:]}
        # pass01 cuts at the fenced pointer, so the cited Scope falls outside its pack cut (count 0): the truncation evidence
        res[name]["truncated_scope"] = rc1 == 2 and "'Scope' occurs 0 times" in e1
        if rc2 == 0:
            pack.write_bytes((rr / "out/a.md").read_bytes())
            rc3, b, _ = run(tool, "bind", *lab, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", rr / "out/b.json")
            raw = pack.read_bytes()
            real = raw.rfind(b"\n## Return pointer\n")
            independent = sha(raw[:real + 1])
            res[name].update(bind=rc3, cut_is_true_cut=(b or {}).get("pack", {}).get("cut_sha256") == independent)
    # run01 asserted 'not cut_is_true_cut' with a default, which passed vacuously when pass01 stopped at construct.
    # The reproduction must be POSITIVE evidence: pass01 truncation observed, pass02 true cut observed.
    ok = res["pass01"]["truncated_scope"] is True and res["pass02"].get("cut_is_true_cut") is True and res["pass02"]["truncated_scope"] is False
    return ok, res


@case("KR-binding-path", "known-failure reproduction", "J2: a binding ref path changed to ../outside-source.md: pass01 compare reports current; pass02 refuses before reading")
def kr_path(r: Path):
    res = {}
    # pass01
    r1 = r / "pass01"
    w1 = book(r1)
    cf = write(r1 / "in/c.json", json.dumps(choices()))
    run(TA1, "construct", "--book", w1, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r1 / "out/c.json")
    pack1 = w1 / "0599.fixture-task/05.02.md"
    run(TA1, "assemble", "--pack", pack1, "--construct", r1 / "out/c.json", "--out", r1 / "out/a.md")
    pack1.write_bytes((r1 / "out/a.md").read_bytes())
    run(TA1, "bind", "--book", w1, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r1 / "out/b.json")
    b = json.loads((r1 / "out/b.json").read_text(encoding="utf-8"))
    b["fields"]["prime_discretion"]["refs"][0]["path"] = "../outside-source.md"
    shutil.copyfile(w1 / "0412x.standing/01.md", w1.parent / "outside-source.md")
    write(r1 / "out/changed.json", json.dumps(b))
    rc, body, e = run(TA1, "compare", "--binding", r1 / "out/changed.json", "--book", w1)
    st1 = [x["status"] for x in (body or {}).get("refs", []) if x["field"] == "prime_discretion"]
    res["pass01"] = {"exit": rc, "status": st1}
    # pass02
    r2 = r / "pass02"
    w2 = book(r2)
    bp = flow2(r2, w2)
    b2 = json.loads(bp.read_text(encoding="utf-8"))
    b2["fields"]["prime_discretion"]["refs"][0]["path"] = "../outside-source.md"
    b2["fields"]["prime_discretion"]["refs"][0]["source"] = "../outside-source.md"
    write(r2 / "out/changed.json", json.dumps(b2))      # outside-source.md deliberately ABSENT: a read would show 'missing', a refusal shows exit 2
    rc2, body2, e2 = run(TA2, "compare", "--binding", r2 / "out/changed.json", "--book", w2)
    res["pass02"] = {"exit": rc2, "stderr": e2.strip()[-140:]}
    ok = rc == 0 and st1 == ["current"] and rc2 == 2 and "escape" in e2
    return ok, res


@case("A-pack-path", "author test", "J2: a binding whose pack path points elsewhere (../x/05.02.md) is refused on compare and inspect")
def a_pack(r: Path):
    w = book(r)
    bp = flow2(r, w)
    b = json.loads(bp.read_text(encoding="utf-8"))
    b["pack"]["path"] = "../x/05.02.md"
    write(r / "out/bad.json", json.dumps(b))
    rc1, _, e1 = run(TA2, "compare", "--binding", r / "out/bad.json", "--book", w)
    rc2, _, e2 = run(TA2, "inspect", "--binding", r / "out/bad.json")
    return rc1 == 2 and rc2 == 2 and "pack path" in e1, {"compare": rc1, "inspect": rc2, "stderr": e1.strip()[-120:]}


@case("A-binding-shape", "author test", "J2: missing field, unsupported schema version and record_basis on a non-self ref are each refused with a correction message")
def a_shape(r: Path):
    w = book(r)
    bp = flow2(r, w)
    b = json.loads(bp.read_text(encoding="utf-8"))
    out = {}
    for name, mut in (("missing", lambda d: d.pop("fields")), ("version", lambda d: d.__setitem__("schema", "task-agreement-binding/1")),
                      ("basis", lambda d: d["fields"]["prime_discretion"]["refs"][0].__setitem__("record_basis", "pack-cut"))):
        d = json.loads(json.dumps(b))
        mut(d)
        write(r / f"out/{name}.json", json.dumps(d))
        rc, _, e = run(TA2, "compare", "--binding", r / f"out/{name}.json", "--book", w)
        out[name] = {"exit": rc, "stderr": e.strip()[-110:]}
    return all(v["exit"] == 2 for v in out.values()), out


@case("A-unclosed", "author test", "J1: an unclosed fence is refused before any heading is selected")
def a_unclosed(r: Path):
    w = book(r, goal_extra="\n```\nnever closed\n")
    cf = write(r / "in/c.json", json.dumps(choices()))
    rc, _, e = run(TA2, "construct", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    return rc == 2 and "unclosed" in e and not (r / "out/c.json").exists(), {"exit": rc, "stderr": e.strip()[-120:]}


@case("A-longer-close", "author test", "J1: a fence closed by a LONGER run of the same character closes; a shorter one does not")
def a_longer(r: Path):
    w = book(r, goal_extra="\n````\n```\n## Goal\n`````\n")
    cf = write(r / "in/c.json", json.dumps(choices()))
    rc, _, e = run(TA2, "construct", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    return rc == 0, {"exit": rc, "stderr": e.strip()[-120:]}


@case("A-indented-heading", "author test", "J1: an indented (1-3 spaces) line equal to the cited heading is refused as ambiguous")
def a_ind(r: Path):
    w = book(r, goal_extra="\n  ## Goal\n")
    cf = write(r / "in/c.json", json.dumps(choices()))
    rc, _, e = run(TA2, "construct", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    return rc == 2 and "indented" in e, {"exit": rc}


@case("A-room", "author test", "J3: outside-room, sibling-prefix and source-book outputs are refused before anything is created; occupied is untouched")
def a_room(r: Path):
    room = r / "lab"
    room.mkdir()
    w = book(room)
    cf = write(room / "in/c.json", json.dumps(choices()))
    common = ["construct", "--lab-root", room, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf]
    res = {}
    for name, out in (("outside", r / "elsewhere/x.json"), ("sibling", r / "lab2/x.json"), ("in-book", w / "0599.fixture-task/x.json")):
        rc, _, e = run(TA2, *common, "--out", out)
        res[name] = {"exit": rc, "created": out.exists() or out.parent.exists() and name != "in-book", "stderr": e.strip()[-90:]}
    occ = write(room / "out/occ.json", "OCCUPIED")
    rc, _, e = run(TA2, *common, "--out", occ)
    res["occupied"] = {"exit": rc, "untouched": occ.read_bytes() == b"OCCUPIED"}
    rc, _, e = run(TA2, *common, "--out", room / "out/ok.json")
    res["inside"] = {"exit": rc, "created": (room / "out/ok.json").exists()}
    ok = all(res[k]["exit"] == 2 and not res[k]["created"] for k in ("outside", "sibling", "in-book")) and res["occupied"]["exit"] == 2 and res["occupied"]["untouched"] and res["inside"]["exit"] == 0
    return ok, res


@case("A-mock-checkout", "author test (mocked boundary)", "J3: a lab root inside a MOCKED checkout (.git and 00.kernel markers in a temp copy) is refused before any write; no real live path is probed")
def a_mock(r: Path):
    mock = r / "mock-checkout"
    (mock / ".git").mkdir(parents=True)
    (mock / "00.kernel").mkdir()
    room = mock / "room"
    room.mkdir()
    w = book(r / "src")
    cf = write(r / "in/c.json", json.dumps(choices()))
    before = tree(mock)
    rc, _, e = run(TA2, "construct", "--lab-root", room, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", room / "x.json")
    return rc == 2 and "checkout" in e and tree(mock) == before, {"exit": rc, "no_write": tree(mock) == before}


@case("A-junction", "author test", "J2/J3: a junction in a source path or an output path is refused (SKIP declared if a junction cannot be created)")
def a_junction(r: Path):
    room = r / "lab"
    room.mkdir()
    w = book(room)
    (room / "real").mkdir()
    j = room / "jn"
    p = subprocess.run(["cmd", "/c", "mklink", "/J", str(j), str(room / "real")], capture_output=True)
    if p.returncode != 0 or not j.exists():
        return True, {"status": "SKIP: junction could not be created here", "stderr": p.stderr.decode("utf-8", "replace")[-120:]}
    cf = write(room / "in/c.json", json.dumps(choices()))
    rc1, _, e1 = run(TA2, "construct", "--lab-root", room, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", j / "x.json")
    sj = w / "0599.fixture-task/jn"
    p2 = subprocess.run(["cmd", "/c", "mklink", "/J", str(sj), str(w / "0412x.standing")], capture_output=True)
    ch = choices(prime_discretion={"state": "cited", "refs": [{"source": "0599.fixture-task/jn/01.md", "heading": "Local work agreement"}]})
    cf2 = write(room / "in/c2.json", json.dumps(ch))
    rc2, _, e2 = run(TA2, "construct", "--lab-root", room, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf2, "--out", room / "out/c2.json")
    ok = rc1 == 2 and "junction" in e1 and not (room / "real/x.json").exists() and rc2 == 2 and "junction" in e2
    return ok, {"output_through_junction": rc1, "source_through_junction": rc2, "junction_created": p2.returncode == 0}


@case("A-readonly", "author test", "inspect and compare create nothing and need no lab root")
def a_ro(r: Path):
    w = book(r)
    bp = flow2(r, w)
    t0 = tree(r)
    rc1, _, _ = run(TA2, "inspect", "--binding", bp)
    rc2, _, _ = run(TA2, "compare", "--binding", bp, "--book", w)
    return t0 == tree(r) and rc1 == 0 and rc2 == 0, {"inspect": rc1, "compare": rc2, "no_write": t0 == tree(r)}


@case("W-flow", "author test", "whole flow in a lab room: construct -> assemble -> freeze-copy -> bind -> inspect -> new-process compare; own pointer write stays current; outside-cut revocation -> context-changed; nothing written outside the room")
def w_flow(r: Path):
    room = r / "room"
    room.mkdir()
    w = book(room, crlf=True)
    outside_before = sorted(p.name for p in r.iterdir())
    bp = flow2(room, w)
    rc_i, bi, _ = run(TA2, "inspect", "--binding", bp)
    pack = w / "0599.fixture-task/05.02.md"
    pack.write_bytes(pack.read_bytes().replace(b"## Return pointer\r\nPENDING.", b"## Return pointer\r\nReturned: SYNTHETIC."))
    rc_c1, b1, _ = run(TA2, "compare", "--binding", bp, "--book", w)
    rec = w / "0599.fixture-task/06.02.decisions.md"
    rec.write_bytes(rec.read_bytes() + b"\r\n## Later\r\nSYNTHETIC: approval withdrawn.\r\n")
    rc_c2, b2, _ = run(TA2, "compare", "--binding", bp, "--book", w)
    verb = [x["status"] for x in (b2 or {}).get("refs", []) if x["ref"] == "decision[0].verbatim"]
    ok = (rc_i == 0 and rc_c1 == 0 and (b1 or {}).get("pack_cut", {}).get("status") == "current" and rc_c2 == 1 and verb == ["context-changed"]
          and sorted(p.name for p in r.iterdir()) == outside_before)
    return ok, {"inspect": rc_i, "compare_after_own_pointer": rc_c1, "compare_after_revocation": rc_c2, "verbatim": verb}


# ---------- compatibility with the frozen core helper (observed, not changed) ----------
LEGACY = ("# legacy pack\n" + M + "\n\n## Goal\nGoal first paragraph.\n\nGoal second paragraph.\n\n## Scope\nScope text.\n\n## Prime discretion\nRoutine fixes.\n\n"
          "## Director required\nForks and judgment.\n\n## Finish\n- f1: tests run\n- bad id: dropped\n- f2: return written\n\n## Director — verbatim\nSYNTHETIC: Ok.\n\n## Return pointer\nPENDING.\n")


def legacy_bind(r: Path, text: str, crlf=False):
    w = r / "book" / "00.00.10.work"
    write(w / "0599.fixture-task/05.02.md", text, crlf)
    rc, b, e = run(TA2, "bind", "--lab-root", r, "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json", "--profile", "core-measured-agreement-v1")
    return rc, b, e


@case("C-lf-six", "compat observation", "LF legacy page: the helper observes all six fields (first paragraphs, id:text Finish bullets, em-dash Director with its body hash); pass02 stores exactly that, no decision pairing")
def c_lf(r: Path):
    rc, b, e = legacy_bind(r, LEGACY)
    ag = (b or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {})
    body = "SYNTHETIC: Ok."
    ok = (rc == 0 and ag.get("goal") == "Goal first paragraph." and ag.get("scope") == "Scope text." and ag.get("prime_discretion") == "Routine fixes."
          and ag.get("director_required") == "Forks and judgment." and ag.get("finish_criteria") == [{"id": "f1", "text": "tests run"}, {"id": "f2", "text": "return written"}]
          and ag.get("recorded_decisions", [{}])[0].get("source_sha256") == sha(body.encode()) and "decisions" not in b["fields"]["recorded_decisions"]
          and b["fields"]["goal"]["state"] == "observed-legacy")
    return ok, {"exit": rc, "agreement": ag, "goal_state": (b or {}).get("fields", {}).get("goal", {}).get("state")}


@case("C-crlf", "compat observation", "the SAME page with CRLF: the frozen helper observes NOTHING (all six None). Recorded as an existing helper defect, not fixed")
def c_crlf(r: Path):
    rc, b, e = legacy_bind(r, LEGACY, crlf=True)
    ag = (b or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {})
    return rc == 0 and ag and all(v is None for v in ag.values()), {"exit": rc, "agreement": ag}


@case("C-absent-empty", "compat observation", "absent vs explicit-empty: Finish absent -> None, Finish present without valid bullets -> []; an empty Goal section -> None (indistinguishable from absent)")
def c_ae(r: Path):
    t = f"# p\n{M}\n\n## Goal\n\n## Scope\nS.\n\n## Finish\nno bullets here\n\n## Return pointer\nPENDING.\n"
    rc, b, e = legacy_bind(r / "a", t)
    ag = (b or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {})
    t2 = f"# p\n{M}\n\n## Scope\nS.\n\n## Return pointer\nPENDING.\n"
    rc2, b2, _ = legacy_bind(r / "b", t2)
    ag2 = (b2 or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {})
    ok = rc == 0 and ag.get("goal") is None and ag.get("finish_criteria") == [] and rc2 == 0 and ag2.get("goal") is None and ag2.get("finish_criteria") is None
    return ok, {"present_empty": {"goal": ag.get("goal"), "finish": ag.get("finish_criteria")}, "absent": {"goal": ag2.get("goal"), "finish": ag2.get("finish_criteria")}}


@case("C-hyphen", "compat observation", "the hyphen variant '## Director - verbatim' is observed the same way as the em-dash variant")
def c_hy(r: Path):
    rc, b, e = legacy_bind(r, LEGACY.replace("Director — verbatim", "Director - verbatim"))
    d = (b or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {}).get("recorded_decisions")
    return rc == 0 and d and d[0]["text"] == "SYNTHETIC: Ok.", {"exit": rc, "decisions": d}


@case("C-fenced-goal", "compat observation", "a fenced '## Goal' before the real one: the helper takes the FENCED text (an existing helper ambiguity); pass02 block mode would select the real heading")
def c_fg(r: Path):
    t = LEGACY.replace("## Goal\nGoal first paragraph.", "~~~\n## Goal\nfenced example\n~~~\n\n## Goal\nGoal first paragraph.")
    rc, b, e = legacy_bind(r, t)
    g = (b or {}).get("legacy_observation", {}).get("observation", {}).get("agreement", {}).get("goal")
    return rc == 0 and g is not None and "fenced example" in g, {"exit": rc, "helper_goal": g}


@case("C-helper-pin", "compat observation", "the adapter refuses a helper whose bytes differ from the pin and records the pinned identity")
def c_pin(r: Path):
    rc, b, e = legacy_bind(r, LEGACY)
    h = (b or {}).get("legacy_observation", {}).get("helper", {})
    # run01 checked only the recorded pin; the refusal itself is now exercised with a wrong expected pin
    code = ("import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import core_compat\n"
            "try:\n core_compat.load(Path(sys.argv[2]), '0'*64)\nexcept RuntimeError as e:\n print('refused:', e); sys.exit(3)\nsys.exit(0)")
    p = subprocess.run([sys.executable, "-B", "-c", code, str(TA2.parent), str(CHECKOUT)], capture_output=True, env=ENV)
    refused = p.returncode == 3 and b"refused" in p.stdout
    ok = rc == 0 and h.get("sha256") == "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a" and h.get("bytes") == 79131 and refused
    return ok, {"helper": h, "wrong_pin_refused": refused}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root, out = Path(a.root), Path(a.out)
    if str(root.resolve()).lower().startswith(str(CHECKOUT.resolve()).lower()):
        sys.exit("refused: fixture root inside the checkout")
    root.mkdir(parents=True, exist_ok=False)
    rows, first = [], None
    for cid, label, says, fn in CASES:
        r = root / cid
        r.mkdir()
        try:
            ok, detail = fn(r)
            status = "PASS" if ok else "FAIL"
            if "SKIP" in json.dumps(detail):
                status = "SKIP"
        except Exception as ex:
            ok, detail, status = False, {"exception": f"{ex.__class__.__name__}: {ex}"[:400]}, "ERROR"
        rows.append({"id": cid, "label": label, "says": says, "status": status, "check_ran": status in ("PASS", "FAIL"), "detail": detail})
        if status in ("FAIL", "ERROR") and first is None:
            first = cid
        print(f"{status:5} {cid:18} {label[:30]:30} {says[:70]}")
    agg = {s: sum(1 for x in rows if x["status"] == s) for s in ("PASS", "FAIL", "ERROR", "SKIP")}
    out.write_text(json.dumps({"schema": "task-agreement-lab2-results/1", "root": str(root), "aggregate": agg, "first_failure": first, "rows": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg, "first failure", first)
    return 0 if agg["FAIL"] == 0 and agg["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
