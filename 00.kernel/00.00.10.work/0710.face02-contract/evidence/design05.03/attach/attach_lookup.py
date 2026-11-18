#!/usr/bin/env python3
"""0710/05.03 NONPRODUCTION attachment lookup demo.

Builds a disposable fixture book (two pages, each with a payload named 02.check.001.py,
different bytes), writes each page's face 02 with an `attach` block, then runs lookups:
through the owning face (exact), by filename alone (ambiguous), an orphan payload, a
changed payload, and the same lookups from a row store (sqlite3 in memory) to show the
attachment survives another representation. No registry implementation, no execution.
usage: attach_lookup.py --book DIR(new) --out FILE(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ATTACH = re.compile(r"```attach\n(.*?)\n```", re.S)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def make_book(book: Path) -> None:
    pages = {
        ("00.00.01.law", "0304.check", "Check"): b"# SYNTHETIC payload A: law-book checker\nprint('checker A')\n",
        ("00.00.10.work", "0526.dev-authoring", "Pack"): b"# SYNTHETIC payload B: pack checker\nprint('checker B')\n",
    }
    for (bk, page, section), body in pages.items():
        d = book / bk / page
        d.mkdir(parents=True)
        (d / "02.check.001.py").write_bytes(body)
        att = {"attach": "payload-attachment/1",
               "owner": {"book": bk, "page": page, "face": "02", "section": section},
               "payload": {"file": "02.check.001.py", "revision": "001", "sha256": sha(body), "bytes": len(body), "state": "draft"},
               "serves": {"section": section, "form": f"{section.lower()}-check"},
               "requires": [{"kind": "environment", "ref": "python>=3.12"}],
               "invoke": {"runner": "python -B", "args": ["--artifact", "<absolute path>"], "permission": "not granted by this attachment"},
               "outputs": [{"kind": "exit", "values": {"0": "pass", "1": "finding", "2": "refused"}}]}
        face = (f"# 02\n\nversion: 001\nAuthorization: draft — 2026-11-02\nwho: claude-opus-5-5\nstate: draft. SYNTHETIC fixture face.\n"
                f"Face: 02\nPPPP: {page[:4]}\nbook: {bk}\nkeyword: {page[5:]}\n\n## {section}\n\nform: {section.lower()}-check\nkind: schema\n\n"
                f"```attach\n{json.dumps(att, indent=1)}\n```\n")
        (d / "02.md").write_bytes(face.encode("utf-8"))
    orphan = book / "00.00.10.work" / "0527.orphan"
    orphan.mkdir(parents=True)
    (orphan / "02.check.001.py").write_bytes(b"# SYNTHETIC orphan payload, no attachment\n")


def attachments(book: Path) -> list[dict]:
    rows = []
    for face in sorted(book.rglob("02.md")):
        for block in ATTACH.findall(face.read_bytes().decode("utf-8")):
            rows.append(json.loads(block))
    return rows


def resolve(book: Path, att: dict) -> dict:
    o, p = att["owner"], att["payload"]
    f = book / o["book"] / o["page"] / p["file"]
    if not f.is_file():
        return {"result": "finding", "code": "payload-missing", "file": str(f)}
    b = f.read_bytes()
    if sha(b) != p["sha256"] or len(b) != p["bytes"]:
        return {"result": "finding", "code": "payload-bytes-differ", "expected": p["sha256"][:12], "observed": sha(b)[:12]}
    return {"result": "found", "owner": f"{o['book']}/{o['page']}/02#{o['section']}", "file": f"{o['book']}/{o['page']}/{p['file']}",
            "revision": p["revision"], "state": p["state"], "sha256": p["sha256"], "invoke": att["invoke"]}


def by_owner(atts, book, bk, page, file):
    hits = [a for a in atts if a["owner"]["book"] == bk and a["owner"]["page"] == page and a["payload"]["file"] == file]
    if len(hits) != 1:
        return {"result": "refused", "code": "no-attachment" if not hits else "ambiguous", "count": len(hits)}
    return resolve(book, hits[0])


def by_filename(atts, file):
    hits = [f"{a['owner']['book']}/{a['owner']['page']}" for a in atts if a["payload"]["file"] == file]
    if len(hits) != 1:
        return {"result": "refused", "code": "ambiguous-filename", "owners": hits}
    return {"result": "found-unique", "owner": hits[0]}


def orphans(book: Path, atts) -> list[str]:
    attached = {f"{a['owner']['book']}/{a['owner']['page']}/{a['payload']['file']}" for a in atts}
    found = [p.relative_to(book).as_posix() for p in book.rglob("02.*") if p.name != "02.md" and not p.name.endswith(".md")]
    return sorted(x for x in found if x not in attached)


def to_rows(atts) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("create table attachment (book text, page text, face text, section text, file text, revision text, sha256 text, bytes int, state text, body text)")
    for a in atts:
        o, p = a["owner"], a["payload"]
        db.execute("insert into attachment values (?,?,?,?,?,?,?,?,?,?)",
                   (o["book"], o["page"], o["face"], o["section"], p["file"], p["revision"], p["sha256"], p["bytes"], p["state"], json.dumps(a)))
    return db


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    book, out = Path(a.book), Path(a.out)
    if book.exists() or out.exists():
        raise SystemExit("refused: book or output exists")
    make_book(book)
    atts = attachments(book)
    cases = []

    def case(cid, says, expect, actual):
        ok = actual.get("result") == expect["result"] and actual.get("code", None) == expect.get("code", None)
        cases.append({"id": cid, "says": says, "expect": expect, "actual": actual, "match": ok})
        print(f"{'PASS' if ok else 'FAIL'} {cid:<4} {says[:70]:<70} -> {actual.get('result')}/{actual.get('code', '')}")

    case("A1", "exact lookup through law page face 02", {"result": "found"}, by_owner(atts, book, "00.00.01.law", "0304.check", "02.check.001.py"))
    case("A2", "exact lookup through work page face 02 (same filename, other bytes)", {"result": "found"}, by_owner(atts, book, "00.00.10.work", "0526.dev-authoring", "02.check.001.py"))
    case("A3", "filename alone is ambiguous", {"result": "refused", "code": "ambiguous-filename"}, by_filename(atts, "02.check.001.py"))
    case("A4", "payload with no attachment is reported", {"result": "finding", "code": "orphan-payload"},
         {"result": "finding", "code": "orphan-payload", "files": orphans(book, atts)} if orphans(book, atts) else {"result": "none"})
    case("A5", "owner with no such attachment", {"result": "refused", "code": "no-attachment"}, by_owner(atts, book, "00.00.10.work", "0527.orphan", "02.check.001.py"))
    db = to_rows(atts)
    row = db.execute("select body from attachment where book=? and page=? and file=?", ("00.00.10.work", "0526.dev-authoring", "02.check.001.py")).fetchall()
    case("A6", "same lookup from a row store gives the same result", {"result": "found"},
         resolve(book, json.loads(row[0][0])) if len(row) == 1 else {"result": "refused", "code": "rows"})
    same = resolve(book, json.loads(row[0][0])) == by_owner(atts, book, "00.00.10.work", "0526.dev-authoring", "02.check.001.py")
    case("A7", "row-store and face lookups are identical", {"result": "equal"}, {"result": "equal" if same else "differ"})
    target = book / "00.00.10.work" / "0526.dev-authoring" / "02.check.001.py"
    target.write_bytes(target.read_bytes() + b"# changed\n")
    case("A8", "payload bytes changed after attachment", {"result": "finding", "code": "payload-bytes-differ"},
         by_owner(atts, book, "00.00.10.work", "0526.dev-authoring", "02.check.001.py"))
    for c in cases:
        if c["actual"].get("invoke"):
            c["note"] = "invoke is data; nothing was run"
    bad = sum(not c["match"] for c in cases)
    out.write_text(json.dumps({"schema": "0710-attach-lookup/1", "book": str(book), "cases": cases, "mismatches": bad}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("cases", len(cases), "mismatches", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
