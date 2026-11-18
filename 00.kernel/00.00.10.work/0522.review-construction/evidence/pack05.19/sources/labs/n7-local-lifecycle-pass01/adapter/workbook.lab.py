#!/usr/bin/env python3
"""PROTOTYPE (0707/05.20) - N7-local exchange overlay on the accepted pass04 chain. NOT production, NOT selected.

Director (06.19.director.md): N7 is self-contained: 05.NN.pack.md -> 05.NN.return.md -> 06.NN.review.md on the same
page/pass/book; the pack must exist before the return; N5's paired N1 model does not apply.

What this overlay changes, for source kind N7NN ONLY (N5 and unrouted calls return the pass04 result untouched):
  build_intake   adds intake["exchange"] (route n7-local, n1_custody not-applicable, pack/return/destination identity,
                 state, chronology) and replaces the N1 finding 'custody-missing' with 'n1-not-applicable'.
                 Any state other than 'matched' adds 'n7-exchange-<state>' and makes measurement 'incomplete',
                 so the existing record refusal applies. Nothing is written; unmatched return bytes stay in place.
  source_changed for N7 with an unchanged pack BOUND REGION (bytes before the pack's '## Review' heading), a change of the
                 assignment row alone is not staleness (Prime's page-local Review summary). Task body or pointer change
                 still is. All other rows unchanged.
  open           (lab CLI only) records the pack body hash and whether a return exists, BEFORE the return is accepted.
                 It is the only chronology the overlay reports as observed; nothing is inferred from mtime or dates.
Not changed (documented label): record 'custody' and its rendered line stay 'missing' (pass02.do_record / pass01.render_body).
usage: workbook.py open --book ABS --source PAGE --pass 05.NN
       workbook.py <prepare|form|record|inspect|publish|read|recover> ...   (delegates to pass04/pass02 main)
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(__file__).resolve().parents[2]  # LAB ADAPTER: the candidate root (production: D:\Git\lib-build)
HERE_ROOT = Path(__file__).resolve().parents[2]
PASS04_REL = "labs/workbook-review-pass04/workbook.py"
PASS04_SHA = "c6be0b97d7274e0393116a4f449848744a2afba0ad9dd694c569276490c62a97"  # LAB ADAPTER: 05.18 lab pass04 (production b7b8776c...)
PASS04_BYTES = 6584  # LAB ADAPTER (production 6508)
OPEN_NAME = "exchange-open.json"
REVIEW_HEADING = b"\n## Review"
POINTER_HEADING = b"\n## Return pointer"


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_pass04():
    if os.path.normcase(str(HERE_ROOT)) != os.path.normcase(str(REPO)):
        refuse_boot("n7-local overlay is not at its canonical root")
    path = REPO / PASS04_REL
    data = path.read_bytes()
    if len(data) != PASS04_BYTES or hashlib.sha256(data).hexdigest() != PASS04_SHA:
        refuse_boot("pass04 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_pass04", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p4 = load_pass04()
p3 = p4.p3
p2 = p3.p2
wb = p3.wb
for _ns in (p3, p2, wb):
    _ns.REPO = REPO
BASE_BUILD = p2.build_intake          # pass04's kind-setting build_intake
BASE_CHANGED = p2.source_changed


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def regions(blob: bytes) -> dict:
    """body = before '## Return pointer'; bound = body + pointer, i.e. before the first '## Review' after the pointer."""
    p = blob.find(POINTER_HEADING)
    body = blob if p < 0 else blob[:p]
    r = blob.find(REVIEW_HEADING, p if p >= 0 else 0)
    bound = blob if r < 0 else blob[:r]
    return {"body_sha256": sha(body), "bound_sha256": sha(bound), "sha256": sha(blob)}


def open_path(book: Path, page: str, pass_id: str) -> Path:
    return book / wb.STORE / page / pass_id / OPEN_NAME


def exchange_of(book: Path, intake: dict) -> dict:
    page, pass_id = intake["page"], intake["pass"]
    pack_rel, ret_rel = f"{page}/{pass_id}.pack.md", f"{page}/{pass_id}.return.md"
    pack, ret = book / pack_rel, book / ret_rel
    pack_ok = pack.is_file() and not wb.is_link(pack)
    ret_ok = ret.is_file() and not wb.is_link(ret)
    codes = {f.get("code") for f in intake.get("findings") or [] if isinstance(f, dict)}
    subs = sorted(r.get("path") for r in intake.get("rows") or [] if r.get("role") == "submission")
    if not pack_ok:
        legacy = intake.get("assignment_path") == f"{page}/{pass_id}.md"
        state = "assignment-not-pack" if legacy else ("orphan-return" if ret_ok else "pack-missing")
    elif "return-pending" in codes or "return-pointer-empty" in codes or "return-pointer-absent" in codes:
        state = "pointer-pending"
    elif subs != [ret_rel]:
        state = "return-not-local"
    else:
        state = "matched"
    pack_id = regions(pack.read_bytes()) if pack_ok else None
    chronology, opened = "unverified", None
    op = open_path(book, page, pass_id)
    if op.is_file():
        opened = json.loads(op.read_bytes())
        if pack_id and opened.get("pack_body_sha256") == pack_id["body_sha256"] and opened.get("return_present") is False:
            chronology = "recorded-before-return"
        else:
            chronology = "open-record-mismatch"
    return {
        "schema": "n7-local-exchange/0",
        "route": "n7-local",
        "n1_custody": "not-applicable",
        "book": str(book.resolve()),
        "page": page,
        "pass": pass_id,
        "pack": {"path": pack_rel, "present": pack_ok, **(pack_id or {})},
        "return": {"path": ret_rel, "present": ret_ok, "sha256": sha(ret.read_bytes()) if ret_ok else None},
        "declared_submission": subs,
        "destination": intake.get("destination"),
        "state": state,
        "unfiled_return_preserved": bool(ret_ok and state != "matched"),
        "chronology": chronology,
        "open_record": opened,
    }


def build_intake(book: Path, source: str, pass_id: str) -> dict:
    intake = BASE_BUILD(book, source, pass_id)
    if intake.get("kind") != "N7NN":
        return intake                                  # N5 and unrouted: pass04 result, byte-for-byte
    ex = exchange_of(book, intake)
    findings = [f for f in intake["findings"] if not (isinstance(f, dict) and f.get("code") == "custody-missing")]
    findings.append({"code": "n1-not-applicable", "path": None})
    if ex["state"] != "matched":
        findings.append({"code": f"n7-exchange-{ex['state']}", "path": ex["return"]["path"]})
        intake["measurement"] = "incomplete"
    intake["findings"] = findings
    intake["exchange"] = ex
    intake["intake_id"] = wb.sha256_bytes(wb.canonical({k: v for k, v in intake.items() if k not in ("intake_id", "cuts", "artifact_paths")}))
    return intake


def source_changed(book: Path, stored, live: dict, journal: dict) -> bool:
    if live.get("kind") == "N7NN" and isinstance(stored, dict):
        if stored.get("book") != live.get("book"):     # run01 T2f: a copied book carried another instance's record
            return True
        a, b = (stored.get("exchange") or {}).get("pack") or {}, (live.get("exchange") or {}).get("pack") or {}
        if a.get("bound_sha256") and a.get("bound_sha256") == b.get("bound_sha256"):
            old = {k: v for k, v in p2.row_map(stored).items() if k[1] != "assignment"}
            new = {k: v for k, v in p2.row_map(live).items() if k[1] != "assignment"}
            return old != new
    return BASE_CHANGED(book, stored, live, journal)


BASE_RESULT = wb.result


def result(command: str, intake, exit_code: int, **extra) -> dict:
    """N7 results also carry the exchange (run01: it was computed but not visible). N5 payloads unchanged."""
    body = BASE_RESULT(command, intake, exit_code, **extra)
    if isinstance(intake, dict) and isinstance(intake.get("exchange"), dict) and "exchange" not in body:
        body["exchange"] = intake["exchange"]
    return body


for _ns in (p3, p2, wb):
    _ns.build_intake = build_intake
p2.source_changed = source_changed
wb.result = result


def do_open(args: list) -> int:
    vals = {}
    i = 0
    while i < len(args):
        if args[i] not in ("--book", "--source", "--pass") or i + 1 >= len(args) or args[i] in vals:
            refuse_boot("usage: open --book ABS --source PAGE --pass 05.NN")
        vals[args[i]] = args[i + 1]
        i += 2
    if set(vals) != {"--book", "--source", "--pass"}:
        refuse_boot("usage: open --book ABS --source PAGE --pass 05.NN")
    book = wb.book_dir(vals["--book"])
    address = wb.address_of(vals["--source"], vals["--pass"])
    if address.get("kind") != "N7NN":
        refuse_boot("open is for N7 pages only")
    wb.writable(book)
    wb._active_book = book                             # run01: pass02 exclusive_write needs the owned book (as perform sets)
    wb._allowed_target = None
    page, pass_id = vals["--source"], vals["--pass"]
    pack, ret = book / f"{page}/{pass_id}.pack.md", book / f"{page}/{pass_id}.return.md"
    if not pack.is_file() or wb.is_link(pack):
        refuse_boot("no pack to open")
    target = open_path(book, page, pass_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = {"schema": "n7-local-open/0", "page": page, "pass": pass_id, "pack_path": f"{page}/{pass_id}.pack.md",
           "pack_body_sha256": regions(pack.read_bytes())["body_sha256"], "return_present": ret.is_file(),
           "note": "observed by this command at this moment; not a historical timestamp"}
    wb.exclusive_write(target, wb.pretty(doc))
    print(json.dumps(doc, indent=2, sort_keys=True))
    return 0


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "open":
        return do_open(args[1:])
    return p3.main(args)


if __name__ == "__main__":
    sys.exit(main())
