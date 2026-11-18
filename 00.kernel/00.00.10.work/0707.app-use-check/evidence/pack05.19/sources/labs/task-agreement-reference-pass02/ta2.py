#!/usr/bin/env python3
"""Task-agreement reference CLI, pass02 (0707/05.15). NONPRODUCTION reference lab.

Successor of labs/task-agreement-reference-pass01/ta.py (preserved byte-identical). It changes:
- J1: a bounded Markdown fence grammar (backtick/tilde, length, up to 3 spaces of indent,
  closing rule). An unclosed fence is refused BEFORE any heading or cut is selected.
- J2: every binding is revalidated on inspect/compare/reconcile (schema, types, identities,
  pack and ref paths) through ONE checked path resolver, before any source read.
- J3: write commands require --lab-root, an ordinary external room. The output must be a NEW
  path inside it with no link ancestors, checked before any directory or file is created.
- compatibility: profile `core-measured-agreement-v1` records the EXACT observation of the frozen
  core helper (core_compat.py); it never creates a decision pairing.
It applies no release, terminal or hold rule. It never imports or runs referenced files.

commands:
  construct --lab-root DIR --book DIR --page PAGE --pass 05.NN --choices FILE --out NEW
  assemble  --lab-root DIR --pack FILE --construct FILE --out NEW
  bind      --lab-root DIR --book DIR --page PAGE --pass 05.NN --out NEW [--profile FILE|core-measured-agreement-v1]
  inspect   --binding FILE
  compare   --binding FILE --book DIR
  reconcile-request --lab-root DIR --binding FILE --book DIR --field NAME --proposal TEXT --reason TEXT --by NAME --out NEW
exit: 0 ok · 1 completed with findings · 2 refused ('stop: ...' with a correction hint)
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FIELDS = ("goal", "scope", "finish_criteria", "prime_discretion", "director_required", "recorded_decisions")
STATES = {"cited", "unknown", "none-recorded", "not-applicable"}
PASS = re.compile(r"^05\.\d\d$")
PAGE = re.compile(r"^\d{4}\.[a-z0-9][a-z0-9-]*$")
OPEN = re.compile(rb"^( {0,3})(`{3,}|~{3,})(.*)$")
POLICY = "passive: this resolver applies no release, terminal or hold rule; a host applies its own declared policy"
CORE_PROFILE = "core-measured-agreement-v1"
CORE_PIN = "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"
BINDING_SCHEMA = "task-agreement-binding/2"


class Stop(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def emit(obj) -> None:
    sys.stdout.buffer.write((json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))


# ---------- one checked path resolver (J2, J3) ----------
def is_link(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & 0x400)


def under(child: Path, parent: Path) -> bool:
    c, p = os.path.normcase(str(child)), os.path.normcase(str(parent))
    return c == p or c.startswith(p.rstrip("\\/") + os.sep)


def checked(root: Path, rel: str, what: str) -> Path:
    """Resolve a book-relative '/'-separated path; refuse absolute, '..', backslash and link/reparse ancestors."""
    if not isinstance(rel, str) or not rel or rel.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", rel) or "\\" in rel:
        raise Stop(f"{what}: path '{rel}' must be book-relative with '/' separators")
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise Stop(f"{what}: path '{rel}' would escape the book root; name a path inside the book")
    cur = root
    for part in parts:
        cur = cur / part
        if is_link(cur):
            raise Stop(f"{what}: path '{rel}' passes through a link or junction at '{part}'; cite the real file")
    if not under(Path(os.path.abspath(cur)), Path(os.path.abspath(root))):
        raise Stop(f"{what}: path '{rel}' would escape the book root")
    return cur


def book_root(text: str) -> Path:
    p = Path(os.path.abspath(text))
    if not p.is_dir():
        raise Stop(f"book '{p}' is not a directory")
    for a in [p, *p.parents]:
        if is_link(a):
            raise Stop(f"book path passes through a link or junction at '{a}'")
    return p


def lab_out(lab_root: str, out: str, book: Path | None = None) -> Path:
    """J3: check the room and the target fully before anything is created."""
    room = Path(os.path.abspath(lab_root))
    if not room.is_dir():
        raise Stop(f"--lab-root '{room}' must be an existing directory; create the room first")
    for a in [room, *room.parents]:
        if is_link(a):
            raise Stop(f"--lab-root passes through a link or junction at '{a}'")
        if (a / ".git").exists() or (a / "00.kernel").exists():
            raise Stop(f"--lab-root '{room}' lies inside a checkout or book tree (marker at '{a}'); choose an ordinary external room")
    target = Path(os.path.abspath(out))
    if not under(target, room) or target == room:
        raise Stop(f"output '{target}' is outside the lab room '{room}'; write only inside --lab-root")
    if book is not None and under(target, book):
        raise Stop(f"output '{target}' is inside the source book; write outputs elsewhere in the room")
    rel = target.relative_to(room).parts
    cur = room
    for part in rel[:-1]:
        cur = cur / part
        if is_link(cur):
            raise Stop(f"output path passes through a link or junction at '{cur}'")
        if cur.exists() and not cur.is_dir():
            raise Stop(f"output ancestor '{cur}' is not a directory")
    if os.path.lexists(target):
        raise Stop(f"output exists: {target}; choose a NEW path (outputs are never overwritten)")
    return target


def write_new(target: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "xb") as f:
        f.write(data)


# ---------- J1: bounded fence grammar ----------
def lines_of(b: bytes) -> list[bytes]:
    return b.splitlines(keepends=True)


def scan(b: bytes) -> dict:
    """Classify lines: real '## ' headings at column 0, indented '## ' lines, fence spans with info.
    Refuse an unclosed fence (we cannot safely know where it ends)."""
    heads, indented, fences = [], [], []
    ls = lines_of(b)
    i = 0
    while i < len(ls):
        s = ls[i].rstrip(b"\r\n")
        m = OPEN.match(s)
        if m and not (m.group(2)[:1] == b"`" and b"`" in m.group(3)):
            ch, n, info = m.group(2)[:1], len(m.group(2)), m.group(3).strip()
            close = re.compile(rb"^ {0,3}" + re.escape(ch) + b"{" + str(n).encode() + rb",}[ \t]*$")
            j = i + 1
            while j < len(ls) and not close.match(ls[j].rstrip(b"\r\n")):
                j += 1
            if j >= len(ls):
                raise Stop(f"unclosed code fence opened at line {i + 1}; close it (same character, at least {n} long) before citing or binding")
            fences.append((i, j, info))
            i = j + 1
            continue
        if s.startswith(b"## "):
            heads.append((i, s[3:]))
        elif re.match(rb"^ {1,3}## ", s):
            indented.append((i, s.lstrip(b" ")[3:]))
        i += 1
    return {"lines": ls, "heads": heads, "indented": indented, "fences": fences}


def cut_heading(b: bytes, heading: str) -> tuple[bytes | None, int]:
    sc = scan(b)
    hb = heading.encode("utf-8")
    if any(t == hb for _, t in sc["indented"]):
        raise Stop(f"heading '{heading}' also appears indented (1-3 spaces); ambiguous under Markdown rules; remove the indent or rename")
    hits = [k for k, (_, t) in enumerate(sc["heads"]) if t == hb]
    if len(hits) != 1:
        return None, len(hits)
    ls, hs = sc["lines"], sc["heads"]
    start = hs[hits[0]][0]
    end = hs[hits[0] + 1][0] if hits[0] + 1 < len(hs) else len(ls)
    return b"".join(ls[start:end]), 1


def pack_cut(b: bytes) -> bytes:
    sc = scan(b)
    for i, t in sc["heads"]:
        if t == b"Return pointer":
            return b"".join(sc["lines"][:i])
    return b


def extract_block(b: bytes) -> tuple[str | None, bytes | None]:
    sc = scan(b)
    blocks = [(i, j) for i, j, info in sc["fences"] if info == b"task-agreement"]
    if len(blocks) > 1:
        raise Stop("the pack holds more than one task-agreement block; exactly one is allowed")
    if not blocks:
        return None, None
    i, j = blocks[0]
    ls = sc["lines"]
    return b"".join(ls[i + 1:j]).decode("utf-8"), b"".join(ls[i:j + 1])


def decode(b: bytes, what: str) -> str:
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Stop(f"{what} is not valid UTF-8 at byte {e.start}; fix the encoding (bytes are never rewritten by this tool)")


def find_pack(book: Path, page: str, pas: str) -> Path:
    if not isinstance(page, str) or not PAGE.match(page):
        raise Stop(f"page '{page}' is not PPPP.title")
    if not isinstance(pas, str) or not PASS.match(pas):
        raise Stop(f"pass '{pas}' is not 05.NN; an explicit pass is required (there is no 'latest')")
    cands = [p for p in (checked(book, f"{page}/{pas}.md", "pack"), checked(book, f"{page}/{pas}.pack.md", "pack")) if p.is_file()]
    if len(cands) != 1:
        raise Stop(f"pack for {page}/{pas}: {len(cands)} candidates ({pas}.md / {pas}.pack.md); exactly one is required")
    return cands[0]


def no_hash_keys(o, where="choices"):
    if isinstance(o, dict):
        for k, v in o.items():
            if "sha256" in k.lower() or k.lower() in ("hash", "digest"):
                raise Stop(f"{where}: key '{k}' carries a hash; the block holds references only (hashes are measured at bind)")
            no_hash_keys(v, f"{where}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            no_hash_keys(v, f"{where}[{i}]")


def measure_ref(book: Path, pack: Path, ref: dict, where: str, same: Path | None = None) -> dict:
    src = ref.get("source")
    if src == "self":
        path = pack
    elif src == "same":
        if same is None:
            raise Stop(f"{where}: 'same' is only valid inside a decision")
        path = same
    else:
        path = checked(book, src, where)
    row = {"source": src, "path": path.relative_to(book).as_posix(), "applicability": ref.get("applicability", "this-pass")}
    if not path.is_file():
        return dict(row, status="unresolved", help=f"record '{row['path']}' is missing; cite an existing record or set the field state to unknown")
    raw = path.read_bytes()
    decode(raw, row["path"])
    if src == "self":
        raw = pack_cut(raw)
        row["record_basis"] = "pack-cut"
    row.update(record_sha256=sha(raw), record_bytes=len(raw))
    if ref.get("whole") is True:
        return dict(row, kind="whole", cut_sha256=sha(raw), cut_bytes=len(raw), count=1, status="resolved", raw_cut_b64=base64.b64encode(raw).decode())
    h = ref.get("heading")
    if not isinstance(h, str) or not h:
        raise Stop(f"{where}: a reference needs 'heading' or 'whole': true")
    cut, n = cut_heading(raw, h)
    if cut is None:
        return dict(row, kind="heading", heading=h, count=n, status="unresolved",
                    help=f"heading '{h}' occurs {n} times outside code fences in {row['path']} (count {n}); it must occur exactly once")
    return dict(row, kind="heading", heading=h, count=1, cut_sha256=sha(cut), cut_bytes=len(cut), status="resolved", raw_cut_b64=base64.b64encode(cut).decode())


def check_choices(c: dict, page: str, pas: str) -> None:
    if not isinstance(c, dict) or c.get("schema") not in ("task-agreement-choices/1", "task-agreement/2"):
        raise Stop("choices: schema must be task-agreement-choices/1")
    no_hash_keys(c)
    if c.get("for") != {"page": page, "pass": pas}:
        raise Stop(f"choices: 'for' names {c.get('for')}, but the pack is {page}/{pas}; declared identity conflict")
    f = c.get("fields")
    if not isinstance(f, dict) or set(f) != set(FIELDS):
        raise Stop(f"choices: fields must be exactly {list(FIELDS)}")
    for name, v in f.items():
        st = v.get("state") if isinstance(v, dict) else None
        if st not in STATES or (st == "none-recorded" and name != "recorded_decisions"):
            raise Stop(f"choices: field {name}: state '{st}' is not allowed")
        if st in ("not-applicable", "none-recorded") and not (isinstance(v.get("reason"), str) and v["reason"].strip()):
            raise Stop(f"choices: field {name}: state {st} needs a reason text")
        if st == "cited":
            if name == "recorded_decisions":
                ds = v.get("decisions")
                if not isinstance(ds, list) or not ds:
                    raise Stop("choices: recorded_decisions cited needs a non-empty decisions list")
                for i, d in enumerate(ds):
                    if not all(isinstance(d.get(k), str) and d[k] for k in ("record", "verbatim", "interpretation")) or not isinstance(d.get("answers"), dict):
                        raise Stop(f"choices: decision {i} needs record, verbatim, interpretation and answers")
                    if d["verbatim"] == d["interpretation"]:
                        raise Stop(f"choices: decision {i}: verbatim and interpretation must be distinct cuts")
            elif not isinstance(v.get("refs"), list) or not v["refs"]:
                raise Stop(f"choices: field {name}: cited needs refs")
    for s in c.get("semantic_findings") or []:
        if not (isinstance(s, dict) and isinstance(s.get("finding"), str) and isinstance(s.get("by"), str) and s["by"].strip()):
            raise Stop("choices: each semantic finding needs 'finding' and an attributed 'by'")


def resolve_fields(book: Path, pack: Path, fields: dict, strict: bool) -> tuple[dict, bool]:
    out, unresolved = {}, False
    for name in FIELDS:
        v = fields[name]
        st = v["state"]
        row = {"state": st, "provenance": "block"}
        if st in ("not-applicable", "none-recorded"):
            row.update(reason=v["reason"], status="declared")
            if st == "none-recorded":
                row["limit"] = "Prime declares that no recorded Director decision applies; not proof that none exists anywhere"
        elif st == "unknown":
            row["status"] = "unknown"
        elif name == "recorded_decisions":
            ds, bad = [], False
            for i, d in enumerate(v["decisions"]):
                rec = checked(book, d["record"], f"decision {i}")
                vb = measure_ref(book, pack, {"source": d["record"], "heading": d["verbatim"]}, f"decision {i} verbatim")
                it = measure_ref(book, pack, {"source": d["record"], "heading": d["interpretation"]}, f"decision {i} interpretation")
                an = measure_ref(book, pack, d["answers"], f"decision {i} answers", same=rec)
                an["heading"] = d["answers"].get("heading")
                pairing = "distinct" if vb.get("cut_sha256") != it.get("cut_sha256") or vb["status"] != "resolved" else "same-bytes"
                for part, label in ((vb, "verbatim"), (it, "interpretation"), (an, "answers")):
                    if part["status"] != "resolved":
                        bad = True
                        if strict:
                            raise Stop(f"decision {i} {label}: {part.get('help')}")
                ds.append({"record": d["record"], "verbatim": vb, "interpretation": it, "answers": an, "pairing": pairing,
                           "answers_scope": "only the cited question or proposal", "evidence": "inspectable pairing, not authenticated approval"})
            row.update(decisions=ds, status="unresolved" if bad else "resolved")
            if bad:
                row["help"] = "a cited decision part did not resolve; fix the citation or set recorded_decisions to unknown"
        else:
            refs = [measure_ref(book, pack, r, f"{name}[{i}]") for i, r in enumerate(v["refs"])]
            if strict:
                for r in refs:
                    if r["status"] != "resolved":
                        raise Stop(f"{name}: {r.get('help')}")
            row.update(refs=refs, status="resolved" if all(r["status"] == "resolved" for r in refs) else "unresolved")
        unresolved |= row["status"] == "unresolved"
        out[name] = row
    return out, unresolved


def instance_of(book: Path) -> str:
    return sha(os.path.normcase(str(book)).encode("utf-8"))


# ---------- commands ----------
def cmd_construct(a) -> int:
    book = book_root(a.book)
    target = lab_out(a.lab_root, a.out, book)
    pack = find_pack(book, a.page, a.pass_)
    c = json.loads(decode(Path(a.choices).read_bytes(), "choices"))
    check_choices(c, a.page, a.pass_)
    resolve_fields(book, pack, c["fields"], strict=True)
    block = {"schema": "task-agreement/2", "for": c["for"], "fields": c["fields"], "semantic_findings": c.get("semantic_findings") or [], "gloss": c.get("gloss")}
    text = "```task-agreement\n" + json.dumps(block, indent=1, ensure_ascii=False) + "\n```\n"
    out = {"schema": "task-agreement-construct/1", "block_text": text,
           "provenance": {"choices_sha256": sha(Path(a.choices).read_bytes()), "pack_at_construct_sha256": sha(pack.read_bytes()), "tool_sha256": sha(Path(__file__).read_bytes())}}
    write_new(target, (json.dumps(out, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    emit({"ok": True, "out": str(target)})
    return 0


def cmd_assemble(a) -> int:
    target = lab_out(a.lab_root, a.out)
    raw = Path(a.pack).read_bytes()
    decode(raw, "pack")
    con = json.loads(Path(a.construct).read_text(encoding="utf-8"))
    if extract_block(raw)[0] is not None:
        raise Stop("the pack already holds a task-agreement block; assemble into a fresh copy")
    sc = scan(raw)
    idx = [i for i, t in sc["heads"] if t == b"Return pointer"]
    if len(idx) != 1:
        raise Stop("the pack needs exactly one real '## Return pointer' heading to place the block before it")
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    ls = sc["lines"]
    block = ("## Task agreement\n" + con["block_text"] + "\n").replace("\n", nl.decode()).encode("utf-8")
    write_new(target, b"".join(ls[:idx[0]]) + block + b"".join(ls[idx[0]:]))
    emit({"ok": True, "out": str(target)})
    return 0


def core_observation(pack_bytes: bytes) -> dict:
    sys.path.insert(0, str(HERE))
    import core_compat
    checkout = HERE.parents[1]
    pin = core_compat.load(checkout, CORE_PIN)
    return {"profile": CORE_PROFILE, "helper": pin, "observation": core_compat.observe(pack_bytes),
            "label": "exact legacy observation of the frozen core helper; not a new grant; no decision pairing is created from it"}


def cmd_bind(a) -> int:
    book = book_root(a.book)
    target = lab_out(a.lab_root, a.out, book)
    pack = find_pack(book, a.page, a.pass_)
    raw = pack.read_bytes()
    decode(raw, "pack")
    text, block_raw = extract_block(raw)
    pc = pack_cut(raw)
    binding = {"schema": BINDING_SCHEMA, "book_instance": instance_of(book), "page": a.page, "pass": a.pass_,
               "pack": {"path": pack.relative_to(book).as_posix(), "file_sha256": sha(raw), "cut_sha256": sha(pc), "cut_bytes": len(pc)},
               "policy": "passive", "policy_note": POLICY, "structural_findings": [], "semantic_findings": [], "profile": None,
               "provenance": {"tool_sha256": sha(Path(__file__).read_bytes()), "immutable": True}}
    unresolved = False
    if text is None:
        binding["block"] = "absent"
        fields = {n: {"state": "unknown", "status": "unknown", "provenance": "block-absent"} for n in FIELDS}
        if a.profile == CORE_PROFILE:
            obs = core_observation(raw)
            binding["profile"] = {"id": CORE_PROFILE, "helper_sha256": obs["helper"]["sha256"]}
            binding["legacy_observation"] = obs
            for n in FIELDS:
                val = obs["observation"]["agreement"][n]
                if val is not None:
                    fields[n] = {"state": "observed-legacy", "status": "observed", "provenance": "profile:" + CORE_PROFILE,
                                 "note": "value is in legacy_observation; it is not a cited cut and not a new grant"}
        elif a.profile:
            prof = json.loads(Path(a.profile).read_text(encoding="utf-8"))
            binding["profile"] = {"id": prof["id"], "sha256": sha(Path(a.profile).read_bytes())}
            for name, heads in prof.get("exact_headings", {}).items():
                for h in heads:
                    m = measure_ref(book, pack, {"source": "self", "heading": h}, f"profile {name}")
                    if m["status"] == "resolved":
                        fields[name] = {"state": "cited", "status": "resolved", "provenance": "profile", "refs": [m]}
                        break
        binding["fields"] = fields
    else:
        try:
            blk = json.loads(text)
        except json.JSONDecodeError as e:
            raise Stop(f"the task-agreement block is not valid JSON ({e.msg} at line {e.lineno}); correct the block")
        binding["block"] = "present"
        binding["block_sha256"] = sha(block_raw)
        check_choices(blk, a.page, a.pass_)
        binding["fields"], unresolved = resolve_fields(book, pack, blk["fields"], strict=False)
        binding["semantic_findings"] = [dict(s, source="supplied", computed=False) for s in blk.get("semantic_findings") or []]
        if blk.get("gloss"):
            binding["gloss"] = dict(blk["gloss"], label="interpretation; never authority")
    write_new(target, (json.dumps(binding, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    emit(dict(binding, refs_unresolved=unresolved, out=str(target)))
    return 1 if unresolved else 0


def iter_refs(b: dict):
    for name, v in b["fields"].items():
        for i, r in enumerate(v.get("refs", [])):
            yield name, f"{name}[{i}]", r
        for i, d in enumerate(v.get("decisions", [])):
            for part in ("verbatim", "interpretation", "answers"):
                yield name, f"decision[{i}].{part}", d[part]


def load_binding(path: str, book: Path | None) -> dict:
    """J2: revalidate the binding before any source read."""
    try:
        b = json.loads(decode(Path(path).read_bytes(), "binding"))
    except json.JSONDecodeError as e:
        raise Stop(f"binding is not valid JSON ({e.msg}); use the file bind wrote")
    if not isinstance(b, dict) or b.get("schema") != BINDING_SCHEMA:
        raise Stop(f"binding schema must be {BINDING_SCHEMA} (got {b.get('schema') if isinstance(b, dict) else type(b).__name__}); re-bind with this tool version")
    need = {"book_instance": str, "page": str, "pass": str, "pack": dict, "fields": dict, "policy": str, "block": str}
    for k, t in need.items():
        if not isinstance(b.get(k), t):
            raise Stop(f"binding field '{k}' is missing or not {t.__name__}")
    if not PAGE.match(b["page"]) or not PASS.match(b["pass"]):
        raise Stop("binding page or pass is malformed")
    if b["pack"].get("path") not in (f"{b['page']}/{b['pass']}.md", f"{b['page']}/{b['pass']}.pack.md"):
        raise Stop(f"binding pack path '{b['pack'].get('path')}' does not match its page and pass")
    if set(b["fields"]) != set(FIELDS):
        raise Stop("binding fields are not exactly the six agreement fields")
    if book is not None:
        if instance_of(book) != b["book_instance"]:
            raise Stop("book instance differs from the binding's; the same short address in another book is a different source (instance-mismatch)")
        checked(book, b["pack"]["path"], "binding pack")
    for field, label, r in iter_refs(b):
        if not isinstance(r, dict) or not isinstance(r.get("path"), str):
            raise Stop(f"binding {label}: missing path")
        src = r.get("source")
        if src == "self":
            if r["path"] != b["pack"]["path"] or r.get("record_basis") != "pack-cut":
                raise Stop(f"binding {label}: a self reference must name the pack path with record_basis pack-cut")
        elif r.get("record_basis") is not None:
            raise Stop(f"binding {label}: record_basis is only valid on self references")
        elif src != "same" and src != r["path"] and not label.endswith((".verbatim", ".interpretation")):
            raise Stop(f"binding {label}: path '{r['path']}' does not match its source '{src}'")
        if r.get("status") == "resolved":
            if r.get("kind") not in ("whole", "heading") or (r.get("kind") == "heading" and not isinstance(r.get("heading"), str)):
                raise Stop(f"binding {label}: kind must be whole or heading (with a heading)")
            for k in ("record_sha256", "cut_sha256"):
                if not (isinstance(r.get(k), str) and re.fullmatch(r"[0-9a-f]{64}", r[k])):
                    raise Stop(f"binding {label}: {k} is missing or malformed")
        if book is not None:
            checked(book, r["path"], f"binding {label}")
    return b


def cmd_compare(a) -> int:
    book = book_root(a.book)
    b = load_binding(a.binding, book)
    pack = checked(book, b["pack"]["path"], "binding pack")
    raw = pack.read_bytes() if pack.is_file() else None
    pc = "missing" if raw is None else ("current" if sha(pack_cut(raw)) == b["pack"]["cut_sha256"] else "cut-changed")
    rows = []
    for field, label, r in iter_refs(b):
        if r.get("status") != "resolved":
            rows.append({"field": field, "ref": label, "status": "unresolved-at-bind"})
            continue
        p = checked(book, r["path"], f"binding {label}")
        if not p.is_file():
            rows.append({"field": field, "ref": label, "status": "missing"})
            continue
        now = p.read_bytes()
        if r.get("record_basis") == "pack-cut":
            now = pack_cut(now)
        if r["kind"] == "whole":
            st = "current" if sha(now) == r["cut_sha256"] else "cut-changed"
        else:
            cut, n = cut_heading(now, r["heading"])
            st = "missing" if cut is None else ("cut-changed" if sha(cut) != r["cut_sha256"] else ("context-changed" if sha(now) != r["record_sha256"] else "current"))
        rows.append({"field": field, "ref": label, "status": st})
    drift = pc != "current" or any(x["status"] != "current" for x in rows)
    emit({"schema": "task-agreement-compare/2", "page": b["page"], "pass": b["pass"], "pack_cut": {"status": pc}, "refs": rows,
          "note": "read-only; binding revalidated; nothing rebound; context-changed means applicability is unconfirmed until reconciled"})
    return 1 if drift else 0


def cmd_inspect(a) -> int:
    b = load_binding(a.binding, None)
    emit({"page": b["page"], "pass": b["pass"], "block": b["block"], "policy": b["policy"],
          "fields": {n: {k: v[k] for k in ("state", "status", "provenance") if k in v} for n, v in b["fields"].items()},
          "decisions": [{"record": d["record"], "answers": d["answers"].get("heading"), "pairing": d["pairing"], "evidence": d["evidence"]}
                        for d in b["fields"]["recorded_decisions"].get("decisions", [])],
          "legacy_observation": b.get("legacy_observation", {}).get("observation"),
          "semantic_findings": b.get("semantic_findings", []),
          "note": "paths are not read by inspect; compare revalidates them against a book"})
    return 0


def cmd_reconcile(a) -> int:
    target = lab_out(a.lab_root, a.out)
    book = book_root(a.book)
    load_binding(a.binding, book)
    if a.field not in FIELDS:
        raise Stop(f"field must be one of {list(FIELDS)}")
    req = {"schema": "task-agreement-reconcile-request/1", "binding_sha256": sha(Path(a.binding).read_bytes()), "field": a.field, "proposal": a.proposal,
           "reason": a.reason, "by": a.by, "applies": False, "decided_by": "Prime for task cuts; the Director for any change to Director records"}
    write_new(target, (json.dumps(req, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    emit({"ok": True, "out": str(target)})
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ta2.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("construct", "bind"):
        s = sub.add_parser(name)
        s.add_argument("--lab-root", required=True)
        s.add_argument("--book", required=True)
        s.add_argument("--page", required=True)
        s.add_argument("--pass", dest="pass_", required=True)
        s.add_argument("--out", required=True)
        if name == "construct":
            s.add_argument("--choices", required=True)
        else:
            s.add_argument("--profile")
    s = sub.add_parser("assemble")
    for k in ("lab-root", "pack", "construct", "out"):
        s.add_argument(f"--{k}", required=True)
    s = sub.add_parser("inspect"); s.add_argument("--binding", required=True)
    s = sub.add_parser("compare"); s.add_argument("--binding", required=True); s.add_argument("--book", required=True)
    s = sub.add_parser("reconcile-request")
    for k in ("lab-root", "binding", "book", "field", "proposal", "reason", "by", "out"):
        s.add_argument(f"--{k}", required=True)
    a = ap.parse_args(argv)
    try:
        return {"construct": cmd_construct, "assemble": cmd_assemble, "bind": cmd_bind, "inspect": cmd_inspect,
                "compare": cmd_compare, "reconcile-request": cmd_reconcile}[a.cmd](a)
    except Stop as s:
        sys.stderr.write(f"stop: {s}\n")
        return 2
    except (OSError, json.JSONDecodeError, RuntimeError) as e:
        sys.stderr.write(f"stop: {e.__class__.__name__}: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
