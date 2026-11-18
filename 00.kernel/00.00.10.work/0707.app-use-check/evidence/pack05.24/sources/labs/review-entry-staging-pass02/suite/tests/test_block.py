#!/usr/bin/env python3
"""0522/05.15 block cases. NONPRODUCTION.

Parser cases run in process against the staged pass05. One measurement case uses a new external book.
usage: test_block.py --root NEW-DIR (outside the checkout) --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
LIVE = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LAB))
import n7compat2  # noqa: E402

P5 = n7compat2.candidate()
OLD = P5.PASS03_PARSE
H = "a" * 64
EXACT = f"Artifact manifest: m.json, sha256 {H}, 5 bytes."
SUFFIX = EXACT + " note"
RETURNED = f"Returned: good.md (desk), sha256 {H}, 5 bytes."
REFUSED = f"Returned: bad.md (Submission: injected), sha256 {H}, 5 bytes."
VALID_SUB = f"Submission: good.md sha256 {H}, 5 bytes."
CASES = []


def case(cid, label, says):
    def deco(fn):
        CASES.append((cid, label, says, fn))
        return fn
    return deco


def n7(body):
    token = P5.KIND.set("N7NN")
    try:
        return P5.parse_pointer(body)
    finally:
        P5.KIND.reset(token)


def n5(body):
    token = P5.KIND.set("N5NN")
    try:
        return P5.parse_pointer(body)
    finally:
        P5.KIND.reset(token)


def codes(parsed):
    return [item["code"] for item in parsed["findings"]]


def paths(parsed):
    return {
        "state": parsed["state"],
        "codes": codes(parsed),
        "submission": None if parsed["submission"] is None else parsed["submission"].get("path"),
        "manifest": None if parsed["manifest"] is None else parsed["manifest"].get("path"),
    }


@case("B1", "author test", "exact N7 manifest still binds m.json")
def b1(r):
    got = paths(n7(EXACT))
    ok = got["manifest"] == "m.json" and got["state"] == "parsed" and "malformed-n7-declaration" not in got["codes"]
    return ok, got


@case("B2", "author test", "A-01 trailing note blocks and does not bind m.json,")
def b2(r):
    got = paths(n7(SUFFIX))
    ok = got["manifest"] is None and got["state"] == "blocked" and "malformed-n7-declaration" in got["codes"]
    return ok, got


@case("H-before", "author hostile", "malformed manifest before a valid Returned line binds neither field")
def h_before(r):
    got = paths(n7(SUFFIX + "\n" + RETURNED))
    ok = got["manifest"] is None and got["submission"] is None and got["state"] == "blocked"
    return ok, got


@case("H-after", "author hostile", "valid manifest before a non-descriptive Returned line binds neither field")
def h_after(r):
    got = paths(n7(EXACT + "\n" + REFUSED))
    ok = (
        got["manifest"] is None
        and got["submission"] is None
        and got["state"] == "blocked"
        and "attribution-not-descriptive" in got["codes"]
        and "malformed-n7-declaration" in got["codes"]
    )
    return ok, got


@case("B3", "author test", "A-02 refused declaration plus a later valid Submission binds nothing")
def b3(r):
    got = paths(n7(REFUSED + "\n" + VALID_SUB))
    ok = got["submission"] is None and got["state"] == "blocked"
    return ok, got


@case("B4", "author test", "labels with no value and the double-comma near-match block in N7")
def b4(r):
    labels = ["Returned:", "Submission:", "Artifact manifest:", "Verification:"]
    out = {label: paths(n7(label)) for label in labels}
    double = paths(n7(f"Artifact manifest: m.json,, sha256 {H}, 1 bytes."))
    ok = all(item["state"] == "blocked" and item["submission"] is None and item["manifest"] is None for item in out.values())
    ok = ok and double["state"] == "blocked" and double["manifest"] is None
    return ok, {"labels": out, "double": double}


@case("B5", "author test", "Notes beside a valid manifest stays diagnostic and keeps the manifest")
def b5(r):
    got = paths(n7("Notes: something.\n" + EXACT))
    ok = got["manifest"] == "m.json" and got["state"] == "parsed" and got["codes"] == ["unparsed-return-line", "submission-not-declared"]
    return ok, got


@case("B6", "author test", "duplicate Returned lines stay ambiguous and unblocked")
def b6(r):
    body = f"Returned: a.md (x, y), sha256 {H}, 1 bytes.\nReturned: b.md (x, y), sha256 {H}, 1 bytes."
    got = paths(n7(body))
    ok = got["submission"] is None and got["state"] == "ambiguous" and "ambiguous-submission" in got["codes"]
    ok = ok and "malformed-n7-declaration" not in got["codes"]
    return ok, got


@case("B7", "author test", "N5 punctuation and the A-01 suffix stay on the pass03 parser object")
def b7(r):
    bodies = {
        "comma": f"Submission: return.md, sha256 {H}, 6 bytes.",
        "semicolon": f"Submission: return.md; sha256 {H}, 6 bytes.",
        "paren": f"Submission: return.md) sha256 {H}, 6 bytes.",
        "suffix": SUFFIX,
        "double": f"Artifact manifest: m.json,, sha256 {H}, 1 bytes.",
    }
    same = {name: n5(body) == OLD(body) == P5.parse_pointer(body) for name, body in bodies.items()}
    return all(same.values()), same


@case("B8", "author test", "LF and CRLF pointer blocks parse equally in N7")
def b8(r):
    raw = (LIVE / "00.kernel/00.00.10.work/0707.app-use-check/05.15.pack.md").read_bytes().replace(b"\r\n", b"\n")
    crlf = raw.replace(b"\n", b"\r\n")
    b_lf = P5.p3.wb.pointer_block(raw.decode("utf-8"))
    b_cr = P5.p3.wb.pointer_block(crlf.decode("utf-8"))
    return n7(b_lf) == n7(b_cr), {"equal": n7(b_lf) == n7(b_cr)}


@case("B9", "author test", "a blocked build resets kind and the block flag, and the sibling file is unbound")
def b9(r):
    book = r / "book"
    source = "0799.block-measure"
    page = book / source
    (page / "evidence").mkdir(parents=True)
    returned = b"Disposable return for the block measurement.\n"
    (page / "evidence/return.md").write_bytes(returned)
    digest = hashlib.sha256(returned).hexdigest()
    ret_rel = f"{source}/evidence/return.md"
    pointer = (
        f"Artifact manifest: m.json, sha256 {H}, 5 bytes. note\n"
        f"Returned: {ret_rel} (desk), sha256 {digest}, {len(returned)} bytes.\n"
    )
    text = f"# 05.01\n\n## Goal\n\nLab.\n\n## Scope\n\nLab.\n\n## Return pointer\n\n{pointer}\n"
    (page / "05.01.pack.md").write_bytes(text.encode("utf-8"))
    intake = P5.build_intake(book, source, "05.01")
    roles = sorted((row.get("role"), row.get("path")) for row in intake["rows"])
    found = [item.get("code") for item in intake["findings"]]
    try:
        P5.build_intake(None, source, "05.01")
        raised = False
    except Exception:
        raised = True
    comma = f"Submission: return.md, sha256 {H}, 6 bytes."
    ok = (
        intake["measurement"] == "incomplete"
        and "malformed-n7-declaration" in found
        and not any(role == "submission" for role, _path in roles)
        and P5.KIND.get() is None
        and P5.BLOCKED.get() is False
        and raised
        and P5.parse_pointer(comma) == OLD(comma)
    )
    return ok, {"measurement": intake["measurement"], "codes": found, "roles": roles, "raised": raised, "kind": P5.KIND.get()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    if str(root.resolve()).lower().startswith(str(LIVE).lower()):
        sys.exit("refused: root inside the checkout")
    root.mkdir(parents=True, exist_ok=False)
    rows = []
    first = None
    for cid, label, says, fn in CASES:
        folder = root / cid
        folder.mkdir()
        try:
            ok, detail = fn(folder)
            status = "PASS" if ok else "FAIL"
        except Exception as ex:
            ok, detail, status = False, {"exception": f"{ex.__class__.__name__}: {ex}"[:400]}, "ERROR"
        rows.append({"id": cid, "label": label, "says": says, "status": status, "detail": detail})
        first = first or (cid if status != "PASS" else None)
        print(f"{status:5} {cid:10} {says[:80]}", flush=True)
    agg = {name: sum(1 for row in rows if row["status"] == name) for name in ("PASS", "FAIL", "ERROR")}
    Path(args.out).write_text(
        json.dumps({"schema": "n7-block-tests/1", "root": str(root), "aggregate": agg, "first_failure": first, "rows": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    print("aggregate", agg, "first failure", first, flush=True)
    return 0 if agg["FAIL"] == 0 and agg["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
