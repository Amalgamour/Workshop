#!/usr/bin/env python3
"""Author lab tests for the task-agreement reference CLI (0707/05.14). NONPRODUCTION.

Written from SPEC.md before ta.py existed (hostile H1 = T06 fenced heading, H2 = T10 revocation
outside the cut were written first). Each case runs ta.py as a NEW PROCESS on retained external
synthetic fixtures. Assertions are concrete values (states, exit codes, hashes computed here by the
test's own slicing), never a comparison of the tool's view with itself. Labels: author lab test.
usage: test_ta.py --root DIR(new, outside the checkout) --out FILE(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TA = HERE.parent / "ta.py"
CHECKOUT = HERE.parents[2]
M = "SYNTHETIC FIXTURE - 0707/05.14 lab. Not live work, not a Director record, not authority."
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(*args) -> tuple[int, dict | None, str]:
    p = subprocess.run([sys.executable, "-B", str(TA), *map(str, args)], capture_output=True, timeout=60, env=ENV)
    out = p.stdout.decode("utf-8", "replace")
    try:
        body = json.loads(out) if out.strip() else None
    except json.JSONDecodeError:
        body = None
    return p.returncode, body, p.stderr.decode("utf-8", "replace")


def tree(root: Path) -> str:
    rows = [f"{q.relative_to(root).as_posix()} {sha(q.read_bytes())}" for q in sorted(root.rglob("*")) if q.is_file()]
    return sha("\n".join(rows).encode())


def write(p: Path, text: str, crlf=False) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    data = text.replace("\n", "\r\n") if crlf else text
    p.write_bytes(data.encode("utf-8"))
    return p


def heading_cut(b: bytes, heading: str) -> bytes:
    """The test's own independent cut: from '## heading' line to before the next '## ' line, ignoring fences."""
    lines = b.splitlines(keepends=True)
    fence, start, end = False, None, None
    for i, l in enumerate(lines):
        s = l.rstrip(b"\r\n")
        if s.startswith(b"```"):
            fence = not fence
            continue
        if fence:
            continue
        if start is None and s == b"## " + heading.encode():
            start = i
        elif start is not None and s.startswith(b"## "):
            end = i
            break
    return b"".join(lines[start:end if end is not None else len(lines)])


def book(root: Path, crlf=False) -> Path:
    w = root / "book" / "00.00.10.work"
    write(w / "0412x.standing/01.md", f"# 01\n{M}\n\n## Local work agreement\nA work page records goal, scope, independent Prime choices, Director-required choices, finish conditions and decisions.\n\n## Other\nunrelated\n", crlf)
    write(w / "0412x.standing/evidence/director-agreement.md", f"# Director agreement (SYNTHETIC)\n{M}\nHard stop on judgment or forks.\n", crlf)
    write(w / "0599.fixture-task/06.02.decisions.md", f"# 06.02\n{M}\n\n## Director - verbatim\nSYNTHETIC: Ok pack it\n\n## Prime - exact proposal this reply approves\nBuild the parser in labs/x only.\n", crlf)
    write(w / "0599.fixture-task/05.02.md", f"# 05.02 - Fixture task\n{M}\n\n## Goal\nAdd a parser.\n\n## Scope\nIncluded: labs/x. Excluded: app edits.\n\n## Finish\nReturn tests and first failures.\n\n## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n", crlf)
    return w


def choices(page="0599.fixture-task", pas="05.02", **over) -> dict:
    c = {"schema": "task-agreement-choices/1", "for": {"page": page, "pass": pas},
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


def authored(root: Path, crlf=False, ch=None) -> tuple[Path, Path]:
    """construct -> assemble into a copy -> replace the pack. Returns (work root, pack)."""
    w = book(root, crlf)
    cf = write(root / "in" / "choices.json", json.dumps(ch or choices()))
    rc, body, err = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", root / "out" / "construct.json")
    assert rc == 0, (rc, err)
    pack = w / "0599.fixture-task/05.02.md"
    rc, body, err = run("assemble", "--pack", pack, "--construct", root / "out" / "construct.json", "--out", root / "out" / "assembled.md")
    assert rc == 0, (rc, err)
    pack.write_bytes((root / "out" / "assembled.md").read_bytes())   # the authoring tool would freeze this
    return w, pack


CASES = []


def case(cid, says, label="author lab test"):
    def deco(fn):
        CASES.append((cid, says, label, fn))
        return fn
    return deco


# ---- hostile cases written first, from the spec ----
@case("T06", "H1 hostile: a heading that appears only inside a code fence is not a target; a real one beside a fenced twin resolves once")
def t06(r: Path):
    w = book(r)
    write(w / "0599.fixture-task/06.03.notes.md", f"# notes\n{M}\n```\n## Hidden\nnot a heading\n```\n\n## Twin\nreal\n\n```text\n## Twin\nfenced copy\n```\n")
    ch = choices(scope={"state": "cited", "refs": [{"source": "0599.fixture-task/06.03.notes.md", "heading": "Hidden"}]})
    cf = write(r / "in/c1.json", json.dumps(ch))
    rc1, b1, e1 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c1.json")
    ch2 = choices(scope={"state": "cited", "refs": [{"source": "0599.fixture-task/06.03.notes.md", "heading": "Twin"}]})
    cf2 = write(r / "in/c2.json", json.dumps(ch2))
    rc2, b2, e2 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf2, "--out", r / "out/c2.json")
    ok = rc1 == 2 and "Hidden" in e1 and rc2 == 0
    return ok, {"fenced_only_exit": rc1, "fenced_only_stderr": e1.strip()[-200:], "real_twin_exit": rc2}


@case("T10", "H2 hostile: cited cut unchanged but a revocation added elsewhere in the same record -> context-changed, not current")
def t10(r: Path):
    w, pack = authored(r)
    rc, b, e = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/binding.json")
    rec = w / "0599.fixture-task/06.02.decisions.md"
    rec.write_bytes(rec.read_bytes() + b"\n## Later note\nSYNTHETIC: the earlier approval is withdrawn.\n")
    t0 = tree(r)
    rc2, b2, e2 = run("compare", "--binding", r / "out/binding.json", "--book", w)
    st = {x["field"] + ":" + x["ref"]: x["status"] for x in (b2 or {}).get("refs", [])}
    verb = [v for k, v in st.items() if k.startswith("recorded_decisions") and "verbatim" in k]
    ok = rc == 0 and rc2 == 1 and verb == ["context-changed"] and tree(r) == t0
    return ok, {"bind_exit": rc, "compare_exit": rc2, "verbatim_status": verb, "no_write": tree(r) == t0}


# ---- the rest of the matrix ----
@case("T01", "ordinary task: construct -> assemble -> bind -> inspect -> new-process compare; late Return-pointer write keeps the pack cut; CRLF bytes kept")
def t01(r: Path):
    w, pack = authored(r, crlf=True)
    rc, b, e = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/binding.json")
    raw = pack.read_bytes()
    goal_independent = sha(heading_cut(raw, "Goal"))
    goal_bound = next(x for x in b["fields"]["goal"]["refs"])["cut_sha256"] if b else None
    rc_i, bi, _ = run("inspect", "--binding", r / "out/binding.json")
    pack.write_bytes(raw.replace(b"## Return pointer\r\nPENDING.", b"## Return pointer\r\nReturned: 05.02.return.md (SYNTHETIC)."))
    rc_c, bc, _ = run("compare", "--binding", r / "out/binding.json", "--book", w)
    states = {k: v["state"] for k, v in b["fields"].items()} if b else {}
    ok = (rc == 0 and rc_i == 0 and rc_c == 0 and goal_bound == goal_independent and b"\r\n" in raw
          and bc["pack_cut"]["status"] == "current" and set(states.values()) == {"cited"} and b["policy"] == "passive")
    return ok, {"bind": rc, "inspect": rc_i, "compare_after_pointer_write": rc_c, "pack_cut_status": bc and bc["pack_cut"]["status"],
                "goal_cut_matches_independent_slice": goal_bound == goal_independent, "states": states}


@case("T02", "hold/reply/successor: the decision answers only the cited question; no release field exists in the binding")
def t02(r: Path):
    w = book(r)
    write(w / "0799.fixture-colab/06.01.review.md", f"# review\n{M}\n\n## Question Q1\nMay the cache write outside evidence?\n\n## Question Q2\nWhich format?\n\n## Holds\nD1 waits for Q1.\n")
    write(w / "0799.fixture-colab/06.02.decisions.md", f"# 06.02\n{M}\n\n## Director - verbatim\n#Q1 SYNTHETIC: Yes, only under evidence.\n\n## Prime - interpretation\nQ1 answered for location only.\n")
    write(w / "0799.fixture-colab/05.01.pack.md", f"# 05.01.pack\n{M}\n\n## Goal\nDesign the cache.\n\n## Scope\nDesign only.\n\n## Finish\nReturn options.\n\n## Return pointer\nPENDING.\n")
    ch = choices(page="0799.fixture-colab", pas="05.01", recorded_decisions={"state": "cited", "decisions": [{"record": "0799.fixture-colab/06.02.decisions.md", "verbatim": "Director - verbatim",
                 "interpretation": "Prime - interpretation", "answers": {"source": "0799.fixture-colab/06.01.review.md", "heading": "Question Q1"}}]})
    cf = write(r / "in/c.json", json.dumps(ch))
    run("construct", "--book", w, "--page", "0799.fixture-colab", "--pass", "05.01", "--choices", cf, "--out", r / "out/c.json")
    pack = w / "0799.fixture-colab/05.01.pack.md"
    run("assemble", "--pack", pack, "--construct", r / "out/c.json", "--out", r / "out/a.md")
    pack.write_bytes((r / "out/a.md").read_bytes())
    rc, b, e = run("bind", "--book", w, "--page", "0799.fixture-colab", "--pass", "05.01", "--out", r / "out/binding.json")
    d = b["fields"]["recorded_decisions"]["decisions"][0] if b else {}
    flat = json.dumps(b or {})
    ok = rc == 0 and d.get("answers", {}).get("heading") == "Question Q1" and d.get("pairing") == "distinct" and "Q2" not in json.dumps(d) and "release" not in flat.lower().replace("no release", "")
    return ok, {"bind": rc, "answers": d.get("answers", {}).get("heading"), "pairing": d.get("pairing")}


@case("T03", "block absent -> block-absent and all unknown; with an explicitly selected exact-heading profile -> profile provenance")
def t03(r: Path):
    w = book(r)
    rc, b, e = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b1.json")
    rc2, b2, e2 = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b2.json", "--profile", HERE.parent / "profiles/legacy-headings-v0.json")
    s1 = {k: v["state"] for k, v in b["fields"].items()} if b else {}
    s2 = {k: (v["state"], v.get("provenance")) for k, v in b2["fields"].items()} if b2 else {}
    ok = (rc == 0 and b["block"] == "absent" and set(s1.values()) == {"unknown"} and rc2 == 0 and s2.get("goal") == ("cited", "profile")
          and s2.get("recorded_decisions", ("", ""))[0] == "unknown")
    return ok, {"no_profile": s1, "profile": s2}


@case("T04", "old record missing: that decision is unresolved with help; other fields still bind")
def t04(r: Path):
    w, pack = authored(r)
    (w / "0599.fixture-task/06.02.decisions.md").unlink()
    rc, b, e = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    d = b["fields"]["recorded_decisions"] if b else {}
    ok = rc == 1 and d.get("status") == "unresolved" and b["fields"]["goal"]["status"] == "resolved" and "help" in json.dumps(d)
    return ok, {"exit": rc, "decisions_status": d.get("status"), "goal": b and b["fields"]["goal"]["status"]}


@case("T05", "duplicate heading in a cited record -> refused at construct with the count")
def t05(r: Path):
    w = book(r)
    rec = w / "0412x.standing/01.md"
    rec.write_bytes(rec.read_bytes() + b"\n## Local work agreement\nsecond copy\n")
    cf = write(r / "in/c.json", json.dumps(choices()))
    rc, b, e = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    ok = rc == 2 and "count 2" in e and not (r / "out/c.json").exists()
    return ok, {"exit": rc, "stderr": e.strip()[-160:]}


@case("T07", "invalid shape (not-applicable without reason; sha256 key in choices) and invalid UTF-8 pack are refused")
def t07(r: Path):
    w = book(r)
    a = write(r / "in/a.json", json.dumps(choices(finish_criteria={"state": "not-applicable"})))
    rc1, _, e1 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", a, "--out", r / "out/a.json")
    ch = choices(); ch["fields"]["goal"]["refs"][0]["sha256"] = "0" * 64
    bq = write(r / "in/b.json", json.dumps(ch))
    rc2, _, e2 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", bq, "--out", r / "out/b.json")
    pack = w / "0599.fixture-task/05.02.md"
    pack.write_bytes(pack.read_bytes() + b"\xff\xfe broken\n")
    rc3, _, e3 = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/c.json")
    ok = rc1 == 2 and "reason" in e1 and rc2 == 2 and "sha256" in e2 and rc3 == 2 and "UTF-8" in e3
    return ok, {"na_without_reason": rc1, "hash_in_choices": rc2, "bad_utf8": rc3}


@case("T08", "path escape refused; link refused where the OS allows creating one (otherwise SKIP declared)")
def t08(r: Path):
    w = book(r)
    write(r / "book" / "outside.md", f"# outside\n{M}\n\n## X\nx\n")
    ch = choices(scope={"state": "cited", "refs": [{"source": "../outside.md", "heading": "X"}]})
    cf = write(r / "in/c.json", json.dumps(ch))
    rc, _, e = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    link = "skipped"
    try:
        os.symlink(w / "0412x.standing/01.md", w / "0599.fixture-task/link.md")
        ch2 = choices(scope={"state": "cited", "refs": [{"source": "0599.fixture-task/link.md", "heading": "Local work agreement"}]})
        cf2 = write(r / "in/c2.json", json.dumps(ch2))
        rc2, _, e2 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf2, "--out", r / "out/c2.json")
        link = "refused" if rc2 == 2 and "link" in e2 else f"NOT refused ({rc2})"
    except OSError as ex:
        link = f"SKIP: cannot create symlink here ({ex.__class__.__name__})"
    ok = rc == 2 and "escape" in e and (link == "refused" or link.startswith("SKIP"))
    return ok, {"escape_exit": rc, "link": link}


@case("T09", "changed selected cut -> cut-changed for that field only")
def t09(r: Path):
    w, pack = authored(r)
    run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    rec = w / "0412x.standing/01.md"
    rec.write_bytes(rec.read_bytes().replace(b"independent Prime choices", b"no independent Prime choices"))
    rc, b, e = run("compare", "--binding", r / "out/b.json", "--book", w)
    st = {x["field"]: x["status"] for x in (b or {}).get("refs", [])}
    ok = rc == 1 and st.get("prime_discretion") == "cut-changed" and st.get("goal") == "current"
    return ok, {"exit": rc, "statuses": st}


@case("T11", "equal short address in another book instance -> instance-mismatch refusal")
def t11(r: Path):
    w, pack = authored(r / "A")
    run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    w2, _ = authored(r / "B")
    rc, b, e = run("compare", "--binding", r / "out/b.json", "--book", w2)
    ok = rc == 2 and "instance" in e
    return ok, {"exit": rc, "stderr": e.strip()[-160:]}


@case("T12", "declared identity conflict (block 'for' names another pass) is structural; a supplied semantic conflict is stored attributed, not computed")
def t12(r: Path):
    w = book(r)
    ch = choices(pas="05.03")
    cf = write(r / "in/c.json", json.dumps(ch))
    rc1, _, e1 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    ch2 = choices()
    ch2["semantic_findings"] = [{"between": ["scope", "recorded_decisions[0]"], "finding": "SYNTHETIC: scope excludes app edits; decision mentions none", "by": "Codex Prime (SYNTHETIC)"}]
    w2, pack = authored(r / "S", ch=ch2)
    rc2, b2, _ = run("bind", "--book", w2, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    sf = (b2 or {}).get("semantic_findings", [])
    ok = rc1 == 2 and "for" in e1 and rc2 == 0 and len(sf) == 1 and sf[0].get("source") == "supplied" and sf[0].get("by", "").startswith("Codex Prime")
    return ok, {"identity_conflict_exit": rc1, "semantic_findings": sf}


@case("T13", "a new revision (05.03) does not replace the selected 05.02 binding; there is no 'latest' selection")
def t13(r: Path):
    w, pack = authored(r)
    run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    write(w / "0599.fixture-task/05.03.md", f"# 05.03\n{M}\n\n## Goal\nA different goal.\n\n## Return pointer\nPENDING.\n")
    rc, b, _ = run("compare", "--binding", r / "out/b.json", "--book", w)
    rc2, _, e2 = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "latest", "--out", r / "out/x.json")
    ok = rc == 0 and b["pass"] == "05.02" and rc2 == 2
    return ok, {"compare_exit": rc, "bound_pass": b and b["pass"], "latest_exit": rc2}


@case("T14", "verbatim == interpretation pairing refused; unresolvable answers cut refused")
def t14(r: Path):
    w = book(r)
    d = choices()["fields"]["recorded_decisions"]
    d["decisions"][0]["interpretation"] = "Director - verbatim"
    cf = write(r / "in/c.json", json.dumps(choices(recorded_decisions=d)))
    rc1, _, e1 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf, "--out", r / "out/c.json")
    d2 = choices()["fields"]["recorded_decisions"]
    d2["decisions"][0]["answers"] = {"source": "same", "heading": "No such proposal"}
    cf2 = write(r / "in/c2.json", json.dumps(choices(recorded_decisions=d2)))
    rc2, _, e2 = run("construct", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--choices", cf2, "--out", r / "out/c2.json")
    ok = rc1 == 2 and "distinct" in e1 and rc2 == 2 and "No such proposal" in e2
    return ok, {"same_pairing_exit": rc1, "bad_answers_exit": rc2}


@case("T15", "occupied output -> refusal, the existing file unchanged")
def t15(r: Path):
    w, pack = authored(r)
    occ = write(r / "out/b.json", "OCCUPIED")
    rc, _, e = run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", occ)
    ok = rc == 2 and occ.read_bytes() == b"OCCUPIED" and "exists" in e
    return ok, {"exit": rc}


@case("T16", "inspect and compare write nothing; none-recorded needs a reason and is reported as declared, not as proof")
def t16(r: Path):
    w, pack = authored(r, ch=choices(recorded_decisions={"state": "none-recorded", "reason": "SYNTHETIC: no Director decision applies to this routine pass"}))
    run("bind", "--book", w, "--page", "0599.fixture-task", "--pass", "05.02", "--out", r / "out/b.json")
    t0 = tree(r)
    rc_i, bi, _ = run("inspect", "--binding", r / "out/b.json")
    rc_c, bc, _ = run("compare", "--binding", r / "out/b.json", "--book", w)
    nr = json.loads((r / "out/b.json").read_text(encoding="utf-8"))["fields"]["recorded_decisions"]
    ok = tree(r) == t0 and rc_i == 0 and rc_c == 0 and nr["state"] == "none-recorded" and "not proof" in nr.get("limit", "")
    return ok, {"no_write": tree(r) == t0, "none_recorded": nr}


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
    for cid, says, label, fn in CASES:
        r = root / cid
        r.mkdir()
        try:
            ok, detail = fn(r)
            status = "PASS" if ok else "FAIL"
        except Exception as ex:
            ok, detail, status = False, {"exception": f"{ex.__class__.__name__}: {ex}"[:400]}, "ERROR"
        if "SKIP" in json.dumps(detail):
            detail["note"] = "contains a declared environment skip"
        rows.append({"id": cid, "says": says, "label": label, "status": status, "check_ran": status != "ERROR", "detail": detail})
        first = first or (cid if status != "PASS" else None)
        print(f"{status:5} {cid} {says[:90]}")
    body = {"schema": "task-agreement-lab-results/1", "root": str(root), "cases": len(rows), "failed": sum(r["status"] != "PASS" for r in rows), "first_failure": first, "rows": rows}
    out.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("cases", len(rows), "failed", body["failed"], "first failure", first)
    return 0 if not body["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
