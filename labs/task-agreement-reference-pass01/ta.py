#!/usr/bin/env python3
"""Task-agreement reference CLI (0707/05.14). NONPRODUCTION reference lab.

A passive resolver: it constructs a references-only `task-agreement` block from explicit
choices, assembles it into a pack copy, binds (measures) the references of a frozen pack, and
compares or inspects a binding. It applies no release, terminal or hold rule. It never runs or
imports referenced files, has no network, and writes only to an explicitly named NEW output.
Spec: 00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.14/SPEC.md

commands:
  construct --book DIR --page PAGE --pass 05.NN --choices FILE --out NEWFILE
  assemble  --pack FILE --construct FILE --out NEWFILE
  bind      --book DIR --page PAGE --pass 05.NN --out NEWFILE [--profile FILE]
  inspect   --binding FILE
  compare   --binding FILE --book DIR
  reconcile-request --binding FILE --field NAME --proposal TEXT --reason TEXT --by NAME --out NEWFILE
exit: 0 ok · 1 completed with findings · 2 refused (stderr 'stop: ...' with a correction hint)
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
FIELDS = ("goal", "scope", "finish_criteria", "prime_discretion", "director_required", "recorded_decisions")
STATES = {"cited", "unknown", "none-recorded", "not-applicable"}
PASS = re.compile(r"^05\.\d\d$")
PAGE = re.compile(r"^\d{4}\.[a-z0-9][a-z0-9-]*$")
POLICY = "passive: this resolver applies no release, terminal or hold rule; a host applies its own declared policy"


class Stop(Exception):
    pass


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def emit(obj) -> None:
    sys.stdout.buffer.write((json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))


def new_out(path: str, data: bytes) -> None:
    p = Path(path)
    if os.path.lexists(p):
        raise Stop(f"output exists: {p}; choose a NEW path (outputs are never overwritten)")
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "xb") as f:
        f.write(data)


def is_link(p: Path) -> bool:
    try:
        st = os.lstat(p)
    except OSError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & 0x400)


def safe_path(root: Path, rel: str, what: str) -> Path:
    if not isinstance(rel, str) or not rel or rel.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", rel) or "\\" in rel:
        raise Stop(f"{what}: source '{rel}' must be a book-relative path with '/' separators")
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise Stop(f"{what}: source '{rel}' would escape the book root; name a path inside the book")
    cur = root
    for part in parts:
        cur = cur / part
        if is_link(cur):
            raise Stop(f"{what}: source '{rel}' passes through a link or junction at '{part}'; cite the real file")
    if not str(cur.resolve()).lower().startswith(str(root.resolve()).lower() + os.sep.lower()):
        raise Stop(f"{what}: source '{rel}' would escape the book root")
    return cur


def lines_of(b: bytes) -> list[bytes]:
    return b.splitlines(keepends=True)


def real_headings(b: bytes) -> list[tuple[int, bytes]]:
    """(line index, heading text) for '## ' lines outside code fences."""
    out, fence = [], False
    for i, l in enumerate(lines_of(b)):
        s = l.rstrip(b"\r\n")
        if s.startswith(b"```"):
            fence = not fence
            continue
        if not fence and s.startswith(b"## "):
            out.append((i, s[3:]))
    return out


def cut_heading(b: bytes, heading: str) -> tuple[bytes | None, int]:
    hs = real_headings(b)
    hits = [i for i, (_, t) in enumerate(hs) if t == heading.encode("utf-8")]
    if len(hits) != 1:
        return None, len(hits)
    ls = lines_of(b)
    start = hs[hits[0]][0]
    end = hs[hits[0] + 1][0] if hits[0] + 1 < len(hs) else len(ls)
    return b"".join(ls[start:end]), 1


def pack_cut(b: bytes) -> bytes:
    for i, t in real_headings(b):
        if t == b"Return pointer":
            return b"".join(lines_of(b)[:i])
    return b


def decode(b: bytes, what: str) -> str:
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Stop(f"{what} is not valid UTF-8 at byte {e.start}; fix the encoding (bytes are never rewritten by this tool)")


def find_pack(book: Path, page: str, pas: str) -> Path:
    if not PAGE.match(page):
        raise Stop(f"page '{page}' is not PPPP.title")
    if not PASS.match(pas):
        raise Stop(f"pass '{pas}' is not 05.NN; an explicit pass is required (there is no 'latest')")
    cands = [p for p in (book / page / f"{pas}.md", book / page / f"{pas}.pack.md") if p.is_file()]
    if len(cands) != 1:
        raise Stop(f"pack for {page}/{pas}: {len(cands)} candidates ({pas}.md / {pas}.pack.md); exactly one is required")
    if is_link(cands[0]):
        raise Stop("the pack is a link; use the real file")
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
        path = safe_path(book, src, where)
    row = {"source": src, "path": path.relative_to(book).as_posix(), "applicability": ref.get("applicability", "this-pass")}
    if not path.is_file():
        return dict(row, status="unresolved", help=f"record '{row['path']}' is missing; cite an existing record or set the field state to unknown")
    raw = path.read_bytes()
    decode(raw, row["path"])
    if src == "self":
        # a self reference's context is the frozen pack cut, not the later Return-pointer/Review area
        # (lab run02 T01: whole-file context made the tool's own pointer write look like context drift)
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
            row["reason"] = v["reason"]
            row["status"] = "declared"
            if st == "none-recorded":
                row["limit"] = "Prime declares that no recorded Director decision applies; not proof that none exists anywhere"
        elif st == "unknown":
            row["status"] = "unknown"
        elif name == "recorded_decisions":
            ds, bad = [], False
            for i, d in enumerate(v["decisions"]):
                rec = safe_path(book, d["record"], f"decision {i}")
                vb = measure_ref(book, pack, {"source": d["record"], "heading": d["verbatim"]}, f"decision {i} verbatim")
                it = measure_ref(book, pack, {"source": d["record"], "heading": d["interpretation"]}, f"decision {i} interpretation")
                an = measure_ref(book, pack, d["answers"], f"decision {i} answers", same=rec)
                an["heading"] = d["answers"].get("heading")
                pairing = "distinct" if vb.get("cut_sha256") != it.get("cut_sha256") or vb["status"] != "resolved" else "same-bytes"
                one = {"record": d["record"], "verbatim": vb, "interpretation": it, "answers": an, "pairing": pairing,
                       "answers_scope": "only the cited question or proposal", "evidence": "inspectable pairing, not authenticated approval"}
                for part, label in ((vb, "verbatim"), (it, "interpretation"), (an, "answers")):
                    if part["status"] != "resolved":
                        bad = True
                        if strict:
                            raise Stop(f"decision {i} {label}: {part.get('help')}")
                ds.append(one)
            row["decisions"] = ds
            row["status"] = "unresolved" if bad else "resolved"
            if bad:
                row["help"] = "a cited decision part did not resolve; fix the citation or set recorded_decisions to unknown"
        else:
            refs = [measure_ref(book, pack, r, f"{name}[{i}]") for i, r in enumerate(v["refs"])]
            for r in refs:
                if r["status"] != "resolved" and strict:
                    raise Stop(f"{name}: {r.get('help')}")
            row["refs"] = refs
            row["status"] = "resolved" if all(r["status"] == "resolved" for r in refs) else "unresolved"
        unresolved |= row["status"] == "unresolved"
        out[name] = row
    return out, unresolved


def extract_block(text_bytes: bytes) -> tuple[str | None, bytes | None]:
    ls, fence, start, blocks = lines_of(text_bytes), False, None, []
    for i, l in enumerate(ls):
        s = l.rstrip(b"\r\n")
        if not fence and s == b"```task-agreement":
            fence, start = True, i
        elif fence and start is not None and s == b"```":
            blocks.append((start, i))
            fence, start = False, None
        elif s.startswith(b"```"):
            fence = not fence
    if len(blocks) > 1:
        raise Stop("the pack holds more than one task-agreement block; exactly one is allowed")
    if not blocks:
        return None, None
    a, b = blocks[0]
    raw = b"".join(ls[a:b + 1])
    return b"".join(ls[a + 1:b]).decode("utf-8"), raw


def cmd_construct(a) -> int:
    book = Path(a.book).resolve()
    pack = find_pack(book, a.page, a.pass_)
    c = json.loads(decode(Path(a.choices).read_bytes(), "choices"))
    check_choices(c, a.page, a.pass_)
    resolve_fields(book, pack, c["fields"], strict=True)       # every cited reference must resolve now
    block = {"schema": "task-agreement/2", "for": c["for"], "fields": c["fields"],
             "semantic_findings": c.get("semantic_findings") or [], "gloss": c.get("gloss")}
    text = "```task-agreement\n" + json.dumps(block, indent=1, ensure_ascii=False) + "\n```\n"
    out = {"schema": "task-agreement-construct/1", "block_text": text,
           "provenance": {"choices_sha256": sha(Path(a.choices).read_bytes()), "pack_at_construct_sha256": sha(pack.read_bytes()),
                          "tool_sha256": sha(Path(__file__).read_bytes())}}
    new_out(a.out, (json.dumps(out, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    emit({"ok": True, "out": a.out})
    return 0


def cmd_assemble(a) -> int:
    raw = Path(a.pack).read_bytes()
    decode(raw, "pack")
    con = json.loads(Path(a.construct).read_text(encoding="utf-8"))
    if extract_block(raw)[0] is not None:
        raise Stop("the pack already holds a task-agreement block; assemble into a fresh copy")
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    idx = [i for i, t in real_headings(raw) if t == b"Return pointer"]
    if len(idx) != 1:
        raise Stop("the pack needs exactly one '## Return pointer' heading to place the block before it")
    ls = lines_of(raw)
    block = ("## Task agreement\n" + con["block_text"] + "\n").replace("\n", nl.decode()).encode("utf-8")
    new_out(a.out, b"".join(ls[:idx[0]]) + block + b"".join(ls[idx[0]:]))
    emit({"ok": True, "out": a.out})
    return 0


def cmd_bind(a) -> int:
    book = Path(a.book).resolve()
    pack = find_pack(book, a.page, a.pass_)
    raw = pack.read_bytes()
    decode(raw, "pack")
    text, block_raw = extract_block(raw)
    binding = {"schema": "task-agreement-binding/1", "book_instance": sha(str(book).lower().encode("utf-8")), "page": a.page, "pass": a.pass_,
               "pack": {"path": pack.relative_to(book).as_posix(), "file_sha256": sha(raw), "cut_sha256": sha(pack_cut(raw)), "cut_bytes": len(pack_cut(raw))},
               "policy": "passive", "policy_note": POLICY, "structural_findings": [], "semantic_findings": [], "profile": None,
               "provenance": {"tool_sha256": sha(Path(__file__).read_bytes()), "immutable": True}}
    unresolved = False
    if text is None:
        binding["block"] = "absent"
        fields = {n: {"state": "unknown", "status": "unknown", "provenance": "block-absent"} for n in FIELDS}
        if a.profile:
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
    new_out(a.out, (json.dumps(binding, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    # stdout is the binding record itself (spec 5); after lab run01 a lossy summary was replaced
    emit(dict(binding, refs_unresolved=unresolved, out=a.out))
    return 1 if unresolved else 0


def iter_refs(binding: dict):
    for name, v in binding["fields"].items():
        for i, r in enumerate(v.get("refs", [])):
            yield name, f"{name}[{i}]", r
        for i, d in enumerate(v.get("decisions", [])):
            for part in ("verbatim", "interpretation", "answers"):
                yield name, f"decision[{i}].{part}", d[part]


def cmd_compare(a) -> int:
    b = json.loads(Path(a.binding).read_text(encoding="utf-8"))
    book = Path(a.book).resolve()
    if sha(str(book).lower().encode("utf-8")) != b["book_instance"]:
        raise Stop("book instance differs from the binding's; the same short address in another book is a different source (instance-mismatch)")
    pack = book / b["pack"]["path"]
    raw = pack.read_bytes() if pack.is_file() else None
    pc = "missing" if raw is None else ("current" if sha(pack_cut(raw)) == b["pack"]["cut_sha256"] else "cut-changed")
    rows = []
    for field, label, r in iter_refs(b):
        if r.get("status") != "resolved":
            rows.append({"field": field, "ref": label, "status": "unresolved-at-bind"})
            continue
        p = book / r["path"]
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
            if cut is None:
                st = "missing"
            elif sha(cut) != r["cut_sha256"]:
                st = "cut-changed"
            elif sha(now) != r["record_sha256"]:
                st = "context-changed"
            else:
                st = "current"
        rows.append({"field": field, "ref": label, "status": st})
    drift = pc != "current" or any(x["status"] != "current" for x in rows)
    emit({"schema": "task-agreement-compare/1", "page": b["page"], "pass": b["pass"], "pack_cut": {"status": pc}, "refs": rows,
          "note": "read-only; nothing rebound; context-changed means applicability is unconfirmed until reconciled"})
    return 1 if drift else 0


def cmd_inspect(a) -> int:
    b = json.loads(Path(a.binding).read_text(encoding="utf-8"))
    emit({"page": b["page"], "pass": b["pass"], "block": b["block"], "policy": b["policy"],
          "fields": {n: {k: v[k] for k in ("state", "status", "provenance") if k in v} for n, v in b["fields"].items()},
          "decisions": [{"record": d["record"], "answers": d["answers"].get("heading"), "pairing": d["pairing"], "evidence": d["evidence"]}
                        for d in b["fields"]["recorded_decisions"].get("decisions", [])],
          "semantic_findings": b.get("semantic_findings", [])})
    return 0


def cmd_reconcile(a) -> int:
    b = Path(a.binding).read_bytes()
    req = {"schema": "task-agreement-reconcile-request/1", "binding_sha256": sha(b), "field": a.field, "proposal": a.proposal,
           "reason": a.reason, "by": a.by, "applies": False, "decided_by": "Prime for task cuts; the Director for any change to Director records"}
    new_out(a.out, (json.dumps(req, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    emit({"ok": True, "out": a.out})
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ta.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("construct", "bind"):
        s = sub.add_parser(name)
        s.add_argument("--book", required=True)
        s.add_argument("--page", required=True)
        s.add_argument("--pass", dest="pass_", required=True)
        s.add_argument("--out", required=True)
        if name == "construct":
            s.add_argument("--choices", required=True)
        else:
            s.add_argument("--profile")
    s = sub.add_parser("assemble"); s.add_argument("--pack", required=True); s.add_argument("--construct", required=True); s.add_argument("--out", required=True)
    s = sub.add_parser("inspect"); s.add_argument("--binding", required=True)
    s = sub.add_parser("compare"); s.add_argument("--binding", required=True); s.add_argument("--book", required=True)
    s = sub.add_parser("reconcile-request")
    for k in ("binding", "field", "proposal", "reason", "by", "out"):
        s.add_argument(f"--{k}", required=True)
    a = ap.parse_args(argv)
    try:
        return {"construct": cmd_construct, "assemble": cmd_assemble, "bind": cmd_bind, "inspect": cmd_inspect,
                "compare": cmd_compare, "reconcile-request": cmd_reconcile}[a.cmd](a)
    except Stop as s:
        sys.stderr.write(f"stop: {s}\n")
        return 2
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"stop: {e.__class__.__name__}: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
