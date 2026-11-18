"""Desk app integration lab (0519.desk-app/05.01). Standard library only. Lab code, not app wiring.

  python -B desk_lab.py view      --repo ABS [--book REL] [--as LABEL]... [--registration ABS] [--member NAME]... [--json]
  python -B desk_lab.py construct --template NAME --input ABS --target ABS --expect-sha256 HEX|absent [--repo ABS] [--book REL] [--write]

view: a read-only desk view derived on every call from records that already exist. Reservations (01NN/reservation.json)
are the open-task index, the pinned return_inspect gives custody, the pinned batch_observe gives the page's Release, Claim,
pointer and Review lines, and an optional pinned prime_cycle read gives the typed review and its next action. Nothing is
cached, so a restarted process sees the same state.

construct: a deterministic template renderer for the records the return-review loop hand-types today (batch page,
Return-pointer lines, Review section). The caller supplies content and judgment; compute supplies addresses, hashes and
layout. It may only create an absent file, replace a declared placeholder or append inside a declared section. Any other
byte change is refused. It refuses any target inside the checkout that contains this lab (disposable books only).

Neither command releases, approves, accepts or closes anything. Labels are not authentication.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCHEMA_VIEW = "desk-view/1"
SCHEMA_CONSTRUCT = "desk-construct/1"
LAB = Path(__file__).resolve().parent
LABS = LAB.parent
CHECKOUT = LABS.parent
PINS = {
    "return_capture": ("return-capture-pass01/return_capture.py", "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"),
    "return_inspect": ("return-capture-pass01/return_inspect.py", "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"),
    "batch_observe": ("batch-observation-pass01/batch_observe.py", "8bea18171b723650e8c0b07f5de334d2c5fd004c5d65c4fa8c4b85cf0bc830d4"),
    "prime_cycle": ("prime-cycle-pass01/prime_cycle.py", "19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d"),
}
DEPS = {"return_inspect": ["return_capture"], "batch_observe": ["return_inspect", "return_capture"],
        "prime_cycle": ["batch_observe", "return_inspect", "return_capture"]}
MEMBER_RE = re.compile(r"^01(0[1-9]|[1-9][0-9])\.[A-Za-z0-9][A-Za-z0-9._-]*$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PENDING = {"", "PENDING", "PENDING."}
RETURN_HEADING = "## Return pointer"
REVIEW_HEADING = "## Review — Codex Prime"
DEFAULT_BOOK = "00.kernel/00.00.10.work"


class Refused(Exception):
    pass


def need(ok, msg):
    if not ok:
        raise Refused(msg)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical(o) -> bytes:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def strict_json(data: bytes, where: str):
    def pairs(items):
        keys = [k for k, _ in items]
        need(len(keys) == len(set(keys)), f"{where}: duplicate key")
        return dict(items)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda c: (_ for _ in ()).throw(Refused(f"{where}: non-finite number")))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Refused(f"{where}: not strict JSON: {e}")


def pinned(name: str) -> Path:
    for dep in [name, *DEPS.get(name, [])]:
        rel, digest = PINS[dep]
        p = LABS / rel
        got = sha(p.read_bytes()) if p.is_file() and not p.is_symlink() else None
        need(got == digest, f"{dep} at {p} is not the pinned code (sha256 {got}); nothing was launched")
    return LABS / PINS[name][0]


def launch(name: str, args: list[str]) -> subprocess.CompletedProcess:
    tool = pinned(name)
    return subprocess.run([sys.executable, "-I", "-B", str(tool), *args], capture_output=True, timeout=600,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))


def emit(text: str) -> None:
    """UTF-8 bytes whatever the console code page (a redirected -I run on Windows is cp1252 otherwise)."""
    sys.stdout.flush()
    sys.stdout.buffer.write(text.encode("utf-8"))
    sys.stdout.buffer.flush()


def abs_path(text: str, label: str) -> Path:
    p = Path(text)
    need(p.is_absolute(), f"{label} must be absolute")
    return p


# ---------------------------------------------------------------- page regions

def split_lines(text: str):
    """Unfenced level-2 headings with their line index. Fenced blocks are skipped."""
    lines = text.split("\n")
    heads, fenced = [], False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if not fenced and line.startswith("## "):
            heads.append((i, line))
    return lines, heads


def assignment_sha256(page: bytes) -> str | None:
    """sha256 of the page bytes before the first unfenced Return-pointer heading: the assignment a claim binds."""
    lines, heads = split_lines(page.decode("utf-8"))
    at = [i for i, h in heads if h == RETURN_HEADING]
    if len(at) != 1:
        return None
    return sha("\n".join(lines[:at[0]]).encode("utf-8") + b"\n")


def section_span(lines, heads, heading):
    at = [k for k, (i, h) in enumerate(heads) if h == heading]
    need(len(at) == 1, f"page must have exactly one unfenced '{heading}' heading (found {len(at)})")
    k = at[0]
    start = heads[k][0] + 1
    end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
    while end > start and lines[end - 1] == "":
        end -= 1
    return start, end


# ---------------------------------------------------------------- view

def read_reservation(member_dir: Path):
    p = member_dir / "reservation.json"
    if not p.is_file() or p.is_symlink():
        return None
    try:
        return strict_json(p.read_bytes(), f"{member_dir.name}/reservation.json")
    except Refused:
        return None


def inspect(book: Path, member: str):
    p = launch("return_inspect", ["inspect", "--book", str(book), "--member", member, "--json"])
    try:
        doc = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else None
    except (UnicodeDecodeError, json.JSONDecodeError):
        doc = None
    return p.returncode, doc


def observe(repo: Path, book: Path, page_rel: str):
    p = launch("batch_observe", ["observe", "--json", "--repo", str(repo), "--live", "--path", page_rel,
                                 "--members-book", str(book)])
    try:
        doc = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else None
    except (UnicodeDecodeError, json.JSONDecodeError):
        doc = None
    return p.returncode, doc, p.stderr.decode("utf-8", "replace")[:400]


def prime_cycle_view(registration: Path):
    p = launch("prime_cycle", ["read", "--registration", str(registration), "--json"])
    try:
        doc = json.loads(p.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return p.returncode, None, p.stderr.decode("utf-8", "replace")[:400]
    return p.returncode, doc, ""


def lines_with(obs, field, prefix):
    return [l for l in (obs or {}).get("assignment", {}).get(field, []) if l["text"].startswith(prefix)]


def bound_assignment(claim_text: str):
    m = re.search(r"assignment-sha256 ([0-9a-f]{64})", claim_text)
    return m.group(1) if m else None


def derive_task(member, ins_exit, ins, obs_entry, typed, successors):
    res = (ins or {}).get("reservation") or {}
    status = (ins or {}).get("status") or "unknown"
    origin = res.get("origin") or {}
    task = {"member": member, "submission_id": res.get("submission_id"), "submitter": res.get("submitter"),
            "reviewer": res.get("reviewer"), "origin": origin, "expected_outputs": res.get("expected_outputs"),
            "supersedes": res.get("supersedes"), "superseded_by": successors.get(member),
            "custody": {"status": status, "inspect_exit": ins_exit, "problems": (ins or {}).get("problems"),
                        "receipt_sha256": ((ins or {}).get("capture") or {}).get("receipt_sha256"),
                        "retrospective": ((ins or {}).get("capture") or {}).get("retrospective")},
            "page": None, "typed_review": None, "attention": []}
    att = task["attention"]
    obs_exit, obs, obs_err, page_bytes = obs_entry if obs_entry else (None, None, "", None)
    if obs is None:
        task["page"] = {"observed": False, "exit": obs_exit, "error": obs_err}
        att.append(f"page not observed (batch_observe exit {obs_exit}): {obs_err.strip()[:160]}")
        releases, claims, review_text, stated = [], [], None, []
    else:
        releases = lines_with(obs, "release_lines", "Release:")
        claims = lines_with(obs, "claim_lines", "Claim:")
        review_text = (obs.get("review") or {}).get("text_raw")
        stated = []
        for o in (obs.get("custody") or {}).get("observations", []):
            if o.get("member") == member:
                stated = o.get("stated_receipts") or []
        a_sha = assignment_sha256(page_bytes) if page_bytes is not None else None
        task["page"] = {"observed": True, "path": obs["source"]["path"], "sha256": obs["source"]["sha256"],
                        "assignment_sha256": a_sha,
                        "release_lines": [l["line"] for l in releases], "claim_lines": [l["line"] for l in claims],
                        "review": None if review_text is None else review_text.strip().split("\n")[0][:200],
                        "reader_ambiguities": len(obs.get("ambiguities") or [])}
        for c in claims:
            bound = bound_assignment(c["text"])
            if bound and a_sha and bound != a_sha:
                att.append(f"assignment-changed-after-claim: claim line {c['line']} binds {bound[:12]}, page assignment is now {a_sha[:12]}")
        if len(releases) > 1:
            att.append(f"{len(releases)} Release: lines; the latest does not silently replace the earlier")
    receipt = task["custody"]["receipt_sha256"]
    for r in stated:
        if receipt is None:
            att.append(f"page states receipt {r[:12]} but custody is {status}")
        elif r != receipt:
            att.append(f"page states receipt {r[:12]}, custody receipt is {receipt[:12]}")
    if typed is not None:
        task["typed_review"] = {"work_id": typed.get("work_id"), "pass_state": typed.get("pass_state"),
                                "disposition": typed.get("disposition"), "pass_terminal": typed.get("pass_terminal"),
                                "next_action": typed.get("next_action"), "attention": typed.get("attention")}
    pending_review = review_text is None or review_text.strip() in PENDING
    reviewer, submitter = res.get("reviewer"), res.get("submitter")
    # state, the actor who moves it, and the next step
    if task["superseded_by"]:
        state, actor, nxt = "superseded", None, f"read {task['superseded_by']} instead"
    elif status in ("incomplete", "refused") or ins is None:
        state, actor, nxt = "custody-problem", "prime", "inspect the member; partial captures are evidence, not returns"
    elif status == "reserved":
        if not releases:
            state, actor, nxt = "awaiting-release", "director", "record the Director's release on the page"
        elif not claims:
            state, actor, nxt = "released", submitter, "claim on the page, then do the work"
        else:
            state, actor, nxt = "claimed", submitter, "capture and verify the return into this member"
    elif status == "complete":
        if task["custody"]["retrospective"]:
            state, actor, nxt = "historical-capture", None, "none (retrospective capture)"
        elif typed is not None and typed.get("pass_state") == "reviewed":
            na = typed.get("next_action")
            state, actor = "reviewed", (na or {}).get("author")
            nxt = na["text"] if na else f"none recorded (pass {typed.get('pass_terminal')})"
        elif typed is not None and typed.get("pass_state") in ("review-stale", "review-unusable"):
            state, actor, nxt = typed["pass_state"], reviewer, "re-read and record a successor review"
        elif pending_review:
            state, actor, nxt = "awaiting-review", reviewer, "verify the member, review the return, record the judgment"
        else:
            state, actor, nxt = "reviewed-untyped", None, "next action is page prose only; not machine-readable"
    else:
        state, actor, nxt = "custody-problem", "prime", f"custody status {status}"
    task.update(state=state, actor=actor, next=nxt)
    return task


DERIVED_KEYS = ("member", "state", "actor", "next", "custody", "page", "typed_review", "attention", "superseded_by")


def cmd_view(a) -> int:
    repo = abs_path(a.repo, "--repo")
    book = repo / a.book
    need(book.is_dir(), f"book {book} is not a directory")
    want = set(a.member or [])
    labels = set(a.as_ or [])
    members, reservations = [], {}
    for d in sorted(book.iterdir()):
        if d.is_dir() and MEMBER_RE.match(d.name) and (not want or d.name in want):
            r = read_reservation(d)
            reservations[d.name] = r
            if labels and (r is None or r.get("submitter") not in labels):
                continue
            members.append(d.name)
    successors = {}
    for name, r in reservations.items():
        if r and r.get("supersedes"):
            successors[r["supersedes"]] = name
    typed_by_member, pc_note = {}, None
    if a.registration:
        code, doc, err = prime_cycle_view(abs_path(a.registration, "--registration"))
        if doc is None:
            pc_note = f"prime_cycle read exit {code}: {err.strip()[:200]}"
        else:
            for w in doc.get("works", []):
                m = (w.get("custody") or {}).get("member")
                if m:
                    typed_by_member[m] = {"work_id": w.get("work_id"), "pass_state": w.get("pass_state"),
                                          "disposition": w.get("disposition"), "pass_terminal": w.get("pass_terminal"),
                                          "next_action": w.get("next_action"), "attention": w.get("attention")}
    inspected = {m: inspect(book, m) for m in members}
    pages = {}
    for m in members:
        res = (inspected[m][1] or {}).get("reservation") or {}
        o = res.get("origin") or {}
        if o.get("page") and o.get("batch"):
            rel = f"{a.book}/{o['page']}/{o['batch']}.md"
            if rel not in pages:
                pfile = repo / rel
                if pfile.is_file():
                    code, doc, err = observe(repo, book, rel)
                    data = pfile.read_bytes()
                    if doc and doc["source"]["sha256"] != sha(data):
                        data = None  # page changed between observation and our read; no assignment hash
                    pages[rel] = (code, doc, err, data)
                else:
                    pages[rel] = (None, None, "page file is missing", None)
    tasks = []
    for m in members:
        ins_exit, ins = inspected[m]
        res = (ins or {}).get("reservation") or {}
        o = res.get("origin") or {}
        rel = f"{a.book}/{o.get('page')}/{o.get('batch')}.md"
        tasks.append(derive_task(m, ins_exit, ins, pages.get(rel), typed_by_member.get(m), successors))
    by_state, by_actor = {}, {}
    for t in tasks:
        by_state[t["state"]] = by_state.get(t["state"], 0) + 1
        if t["actor"]:
            by_actor[t["actor"]] = by_actor.get(t["actor"], 0) + 1
    free = 99 - sum(1 for d in book.iterdir() if re.match(r"^01(0[1-9]|[1-9][0-9])", d.name))
    view = {"schema": SCHEMA_VIEW, "authority": "none", "repository": str(repo), "book": a.book,
            "filter": {"as": sorted(labels), "member": sorted(want)},
            "tools": {k: v[1] for k, v in PINS.items()}, "prime_cycle": pc_note or ("merged" if a.registration else "not requested"),
            "return_band_free": free, "tasks": tasks, "summary": {"tasks": len(tasks), "by_state": by_state, "by_actor": by_actor}}
    view["state_digest"] = sha(canonical([{k: t[k] for k in DERIVED_KEYS} for t in tasks]))
    if a.json:
        emit(json.dumps(view, ensure_ascii=False, indent=1) + "\n")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"desk view of {a.book}  (authority: none; derived now from reservations, custody, pages)")
        print(f"return band free: {free}   state digest: {view['state_digest'][:16]}   prime_cycle: {view['prime_cycle']}")
        for t in tasks:
            print(f"- {t['member']}  [{t['state']}]  submitter={t['submitter']}  actor={t['actor']}")
            print(f"    page {t['origin'].get('page')}/{t['origin'].get('batch')}  next: {t['next']}")
            for x in t["attention"]:
                print(f"    ! {x}")
        print(f"summary: {json.dumps(view['summary'], ensure_ascii=False)}")
    return 1 if any(t["attention"] or t["state"] == "custody-problem" for t in tasks) else 0


# ---------------------------------------------------------------- construct

def text_field(d, key, limit=4000, one_line=True):
    v = d.get(key)
    need(isinstance(v, str) and v.strip() and len(v) <= limit, f"input.{key} must be non-empty text up to {limit} characters")
    need(not one_line or ("\n" not in v and "\r" not in v), f"input.{key} must be one line")
    return v


def exact(d, keys, where):
    need(isinstance(d, dict) and set(d) == set(keys), f"{where} keys must be exactly {sorted(keys)}")


def render_batch_page(inp):
    exact(inp, {"template", "title", "pppp", "pass", "who", "executor", "reviewer", "workspace", "branch", "goal", "steps",
                "allowed_writes", "capture"}, "input")
    need(re.fullmatch(r"\d{4}", inp["pppp"] or "") and re.fullmatch(r"05\.\d{2}", inp["pass"] or ""), "pppp and pass must be NNNN and 05.NN")
    for k in ("title", "who", "executor", "reviewer", "workspace", "branch"):
        text_field(inp, k, 200)
    text_field(inp, "goal", 4000, one_line=False)
    text_field(inp, "allowed_writes", 2000, one_line=False)
    need(isinstance(inp["steps"], list) and 1 <= len(inp["steps"]) <= 12, "steps must be 1..12 items")
    cap = inp["capture"]
    exact(cap, {"member", "submission", "return_file", "artifacts"}, "input.capture")
    need(MEMBER_RE.match(cap["member"] or ""), "capture.member must be a 01NN member name")
    body = [f"# 05 — {inp['title']}", "version: 001", "Authorization: draft — constructed", f"who: {inp['who']}",
            "state: prepared for named Director invocation", "Face: 05", f"PPPP: {inp['pppp']}", "book: 00.00.10.work", "",
            "## Assignment", f"Executor: {inp['executor']}. Reviewer: {inp['reviewer']}.",
            "The release and the claim are recorded in the Return pointer. This draft grants no release.",
            f"Workspace {inp['workspace']}, branch {inp['branch']}.", "", "## Goal", inp["goal"].rstrip("\n"), ""]
    for i, s in enumerate(inp["steps"], 1):
        exact(s, {"title", "text"}, f"steps[{i}]")
        body += [f"## #{i:02d} - {text_field(s, 'title', 120)}", text_field(s, "text", 4000, one_line=False).rstrip("\n"), ""]
    arts = cap["artifacts"]
    need(isinstance(arts, list) and arts and all(isinstance(x, str) and x and "|" not in x and "\n" not in x for x in arts),
         "capture.artifacts must be relative paths")
    body += ["## Allowed writes", inp["allowed_writes"].rstrip("\n"), "", "## Local capture",
             f"Dedicated submission starts Did, Blocked, Need. Use reserved {cap['member']}:", "```text",
             "python -B labs/return-capture-pass01/return_capture.py capture --book BOOK --submission "
             f"{cap['submission']} --return-file {cap['return_file']} --source-root ROOT "
             + " ".join(f'--artifact "{x}|{x}"' for x in arts),
             f"python -B labs/return-capture-pass01/return_capture.py verify --book BOOK --member {cap['member']}", "```", "",
             RETURN_HEADING, "PENDING.", "", REVIEW_HEADING, "PENDING.", ""]
    return "\n".join(body)


def render_pointer_line(inp, page: bytes, repo, book):
    kind = inp.get("kind")
    if kind == "release":
        exact(inp, {"template", "kind", "by", "date", "quote"}, "input")
        need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", inp["date"] or ""), "date must be YYYY-MM-DD")
        q = text_field(inp, "quote", 6000)
        need('"' not in q, "quote must not contain a double quote; it is quoted verbatim")
        return f"Release: {text_field(inp, 'by', 200)}, {inp['date']}: \"{q}\""
    if kind == "claim":
        exact(inp, {"template", "kind", "actor", "at_commit", "scope"}, "input")
        a = assignment_sha256(page)
        need(a is not None, "page has no single Return pointer heading; the assignment cannot be bound")
        commit = inp["at_commit"]
        need(commit is None or re.fullmatch(r"[0-9a-f]{40}", commit), "at_commit must be null or 40 hex")
        at = f" at {commit}" if commit else ""
        return (f"Claim: {text_field(inp, 'actor', 300)}{at}; assignment-sha256 {a}. "
                f"Scope: {text_field(inp, 'scope', 300)}")
    if kind == "execution":
        exact(inp, {"template", "kind", "by", "member", "summary"}, "input")
        need(repo is not None, "execution needs --repo and --book to inspect the member")
        member = inp["member"]
        need(MEMBER_RE.match(member or ""), "member must be a 01NN member name")
        code, ins = inspect(repo / book, member)
        need(code == 0 and ins and ins.get("status") == "complete",
             f"member {member} is not complete (inspect exit {code}, status {(ins or {}).get('status')}); nothing constructed")
        c = ins["capture"]
        return (f"Execution: returned by {text_field(inp, 'by', 200)}. Member {member}, submission {c['submission_id']}. "
                f"Receipt sha256 {c['receipt_sha256']} (manifest {c['manifest_sha256']}). "
                f"Inspect: complete; {len(c['payloads'])} payloads; not approved, not accepted, not published. "
                f"{text_field(inp, 'summary', 3000)}")
    raise Refused("return-pointer kind must be release, claim or execution")


def render_review(inp, repo):
    exact(inp, {"template", "by", "date", "summary", "record"}, "input")
    need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", inp["date"] or ""), "date must be YYYY-MM-DD")
    summary = text_field(inp, "summary", 3000)
    rec_dir = abs_path(inp["record"], "record")
    need((rec_dir / "COMMITTED.json").is_file(), "record has no COMMITTED.json; a partial review is not a review")
    rec = strict_json((rec_dir / "record.json").read_bytes(), "record.json")
    d = rec.get("decision") or {}
    j = d.get("judgment") or {}
    na = j.get("next_action")
    nxt = na.get("text") if isinstance(na, dict) else "none"
    where = os.path.relpath(rec_dir, repo).replace("\\", "/") if repo else str(rec_dir)
    return [f"{inp['date']} ({text_field(inp, 'by', 200)}): {j.get('disposition')}; pass {j.get('pass_terminal')}; "
            f"goal {(j.get('goal') or {}).get('terminal')}. {summary}",
            f"Typed record: {where}/record.json (sha256 {sha((rec_dir / 'record.json').read_bytes())}).",
            f"Next action: {nxt}"]


def cmd_construct(a) -> int:
    target = abs_path(a.target, "--target")
    rt = target.resolve()
    need(not str(rt).lower().startswith(str(CHECKOUT.resolve()).lower() + os.sep.lower()),
         f"target is inside the checkout {CHECKOUT}; this lab constructs in disposable books only")
    inp = strict_json(abs_path(a.input, "--input").read_bytes(), "input")
    need(isinstance(inp, dict) and inp.get("template") == a.template, "input.template must equal --template")
    repo = abs_path(a.repo, "--repo") if a.repo else None
    exists = target.is_file()
    if a.expect_sha256 == "absent":
        need(not exists and not target.exists(), "target exists; expected absent")
        old = None
    else:
        need(HEX64.match(a.expect_sha256 or ""), "--expect-sha256 must be 64 hex or 'absent'")
        need(exists and not target.is_symlink(), "target is not a plain file")
        old = target.read_bytes()
        need(sha(old) == a.expect_sha256, f"target sha256 {sha(old)} is not the expected {a.expect_sha256}; read again")
        need(b"\r" not in old, "target has CR line endings")
    if a.template == "batch-page/1":
        need(old is None, "batch-page/1 only creates a new page")
        new = render_batch_page(inp).encode("utf-8")
        op = {"op": "create"}
    elif a.template in ("return-pointer/1", "review-section/1"):
        need(old is not None, f"{a.template} edits an existing page")
        lines, heads = split_lines(old.decode("utf-8"))
        heading = RETURN_HEADING if a.template == "return-pointer/1" else REVIEW_HEADING
        start, end = section_span(lines, heads, heading)
        current = [l for l in lines[start:end] if l.strip()]
        add = [render_pointer_line(inp, old, repo, a.book)] if a.template == "return-pointer/1" else render_review(inp, repo)
        if len(current) == 1 and current[0].strip() in PENDING and start < end:
            # replace exactly the placeholder line(s); nothing else
            new_lines = lines[:start] + add + lines[end:]
            op = {"op": "replace-placeholder", "section": heading, "removed": lines[start:end]}
        else:
            need(a.template == "return-pointer/1",
                 "review section already holds text; a successor review is appended by a new record, not by rewriting this one")
            new_lines = lines[:end] + add + lines[end:]
            op = {"op": "append", "section": heading, "removed": []}
        new = "\n".join(new_lines).encode("utf-8")
        # structural check: the only bytes removed are the declared placeholder
        prefix, suffix = "\n".join(lines[:start]), "\n".join(lines[end:])
        newt = new.decode("utf-8")
        need(newt.startswith(prefix) and newt.endswith(suffix), "construction changed bytes outside its section; refused")
        need(all(l.strip() in PENDING for l in op["removed"]), "construction would remove non-placeholder text; refused")
    else:
        raise Refused("unknown template; known: batch-page/1, return-pointer/1, review-section/1")
    result = {"schema": SCHEMA_CONSTRUCT, "authority": "none", "template": a.template, "target": str(target),
              "before_sha256": None if old is None else sha(old), "after_sha256": sha(new), "operation": op,
              "written": False}
    if a.write:
        tmp = target.with_name(target.name + ".construct.tmp")
        need(not tmp.exists(), f"temporary name {tmp} is present; nothing written")
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp, "xb") as f:
            f.write(new)
            f.flush()
            os.fsync(f.fileno())
        if old is not None:
            need(sha(target.read_bytes()) == sha(old), "target changed during construction; temporary kept, target untouched")
            os.replace(tmp, target)
        else:
            os.rename(tmp, target)  # fails if the target appeared meanwhile on Windows
        result["written"] = True
    else:
        result["preview"] = new.decode("utf-8")
    emit(json.dumps(result, ensure_ascii=False, indent=1) + "\n")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="desk_lab.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("view")
    v.add_argument("--repo", required=True)
    v.add_argument("--book", default=DEFAULT_BOOK)
    v.add_argument("--as", dest="as_", action="append")
    v.add_argument("--registration")
    v.add_argument("--member", action="append")
    v.add_argument("--json", action="store_true")
    c = sub.add_parser("construct")
    c.add_argument("--template", required=True)
    c.add_argument("--input", required=True)
    c.add_argument("--target", required=True)
    c.add_argument("--expect-sha256", required=True)
    c.add_argument("--repo")
    c.add_argument("--book", default=DEFAULT_BOOK)
    c.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    try:
        return cmd_view(a) if a.cmd == "view" else cmd_construct(a)
    except Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
