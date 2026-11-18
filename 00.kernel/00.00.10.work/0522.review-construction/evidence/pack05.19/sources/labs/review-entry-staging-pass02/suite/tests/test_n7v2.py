#!/usr/bin/env python3
"""pass02 tests (0707/05.17). NONPRODUCTION. Author tests and known-failure reproductions.

KR: reproduce K1 and the pass01 collision defect on preserved pass01 FIRST.
P:  parser cases (in-process, pinned pass03 loaded read-only): N5 context == pass03; N7 exactness.
I:  integration on disposable copy roots (new processes): real legal punctuation filenames on an N5 page.
usage: test_n7v2.py --root NEW-DIR (outside the checkout) --out FILE
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
LAB = HERE.parent
LIVE = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LAB))
import n7compat2  # noqa: E402

sys.path.insert(0, str(LIVE / "labs/n7-intake-compat-pass01"))
import n7compat as pass01  # noqa: E402   preserved pass01 lab

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
P3 = n7compat2.load_pass03()
OLD = P3.parse_pointer                       # selected pass03 parser
V2_N5 = n7compat2.make_parser(P3, kind_fn=lambda: "N5NN")
V2_N7 = n7compat2.make_parser(P3, kind_fn=lambda: "N7NN")
V2_NONE = n7compat2.make_parser(P3)          # no intake context set
P01 = pass01.make_parser(pass01.load_pass03())
H = "a" * 64
PAGE7 = "00.kernel/00.00.10.work/0707.app-use-check"
FROZEN_PACK = LIVE / PAGE7 / "evidence/pack05.16/sources" / PAGE7 / "05.15.pack.md"

N5_INPUTS = {
    "plain": f"Submission: s.md sha256 {H}, 1 bytes.\nArtifact manifest: m.json sha256 {H}, 9 bytes.",
    "verification": f"Submission: s.md sha256 {H}, 1 bytes.\nVerification: v.md sha256 {H}, 2 bytes.",
    "counted": f"Submission: s.md sha256 {H}, 1 bytes.\nArtifact manifest: m.json sha256 {H}, 9 bytes, 3 files. Excludes itself.",
    "comma-file": f"Submission: return.md, sha256 {H}, 6 bytes.",
    "semicolon-file": f"Submission: return.md; sha256 {H}, 6 bytes.",
    "paren-file": f"Submission: return.md) sha256 {H}, 6 bytes.",
    "collision-manifest": f"Submission: s.md sha256 {H}, 1 bytes.\nArtifact manifest: m.json, sha256 {H}, 9 bytes.",
    "duplicate-submission": f"Submission: a.md sha256 {H}, 1 bytes.\nSubmission: b.md sha256 {H}, 1 bytes.",
    "conflicting-manifests": f"Submission: s.md sha256 {H}, 1 bytes.\nArtifact manifest: m.json sha256 {H}, 9 bytes.\nArtifact manifest: m.json, sha256 {H}, 9 bytes.",
    "returned-on-n5": f"Returned: r.md (x, y), sha256 {H}, 1 bytes.",
    "pending": "PENDING.",
    "empty": "",
    "garbage": "Notes: something.\nSubmission:",
}

CASES = []


def case(cid, label, says):
    def deco(fn):
        CASES.append((cid, label, says, fn))
        return fn
    return deco


def codes(p):
    return sorted({f["code"] for f in p["findings"]})


@case("KR1", "known-failure reproduction", "K1: preserved pass01 refuses legal N5 filenames ending in , ; ) that pass03 accepts")
def kr1(r):
    out = {}
    for k in ("comma-file", "semicolon-file", "paren-file"):
        b = N5_INPUTS[k]
        out[k] = {"pass03": (OLD(b)["submission"] or {}).get("path"), "pass01": (P01(b)["submission"] or {}).get("path"), "pass01_codes": codes(P01(b))}
    ok = all(v["pass03"] and v["pass01"] is None and "unrecognized-path-punctuation" in v["pass01_codes"] for v in out.values())
    return ok, out


@case("KR2", "known-failure reproduction (found by Claude's reread)", "pass01 ALSO changed N5 meaning silently: `Artifact manifest: m.json, sha256` means file 'm.json,' in pass03 but 'm.json' in pass01")
def kr2(r):
    b = N5_INPUTS["collision-manifest"]
    a, p = OLD(b)["manifest"]["path"], P01(b)["manifest"]["path"]
    return a == "m.json," and p == "m.json", {"pass03": a, "pass01": p}


@case("P1", "author test", "N5 context: every N5 input (including , ; ) filenames, the collision line, duplicates, conflicts, Returned-on-N5, PENDING, empty, garbage) parses EXACTLY as pass03")
def p1(r):
    same = {k: V2_N5(b) == OLD(b) for k, b in N5_INPUTS.items()}
    return all(same.values()), same


@case("P2", "author test", "no intake context (any other caller): exactly pass03, including on the real N7 pointer")
def p2(r):
    blk = P3.wb.pointer_block(FROZEN_PACK.read_bytes().decode("utf-8"))
    same = {k: V2_NONE(b) == OLD(b) for k, b in list(N5_INPUTS.items()) + [("real-n7", blk)]}
    return all(same.values()), same


@case("P3", "author test", "N7 context: the real 05.15 pointer binds the exact return and manifest; the collision line is the N7 delimiter here")
def p3(r):
    blk = P3.wb.pointer_block(FROZEN_PACK.read_bytes().decode("utf-8"))
    n = V2_N7(blk)
    c = V2_N7(N5_INPUTS["collision-manifest"])
    ok = (n["submission"]["path"] == "05.15.return.md" and n["submission"]["declared_form"] == "n7-returned"
          and n["manifest"]["path"] == "evidence/design05.15/artifact-manifest.json" and c["manifest"]["path"] == "m.json")
    return ok, {"submission": n["submission"], "manifest": n["manifest"], "collision_in_n7": c["manifest"]}


@case("P4", "author test", "N7 context keeps old meaning for N5-form lines that are not an N7 form: `Submission: return.md, sha256` -> 'return.md,'")
def p4(r):
    out = {k: (V2_N7(N5_INPUTS[k])["submission"] or {}).get("path") for k in ("comma-file", "semicolon-file", "paren-file")}
    return out == {"comma-file": "return.md,", "semicolon-file": "return.md;", "paren-file": "return.md)"}, out


@case("P5", "author test", "N7 context duplicates and cross-form conflicts are ambiguous (nothing bound)")
def p5(r):
    a = V2_N7(f"Returned: a.md (x, y), sha256 {H}, 1 bytes.\nReturned: b.md (x, y), sha256 {H}, 1 bytes.")
    b = V2_N7(f"Returned: a.md (x, y), sha256 {H}, 1 bytes.\nSubmission: s.md sha256 {H}, 1 bytes.")
    c = V2_N7(f"Returned: a.md (x, y), sha256 {H}, 1 bytes.\nArtifact manifest: m.json, sha256 {H}, 1 bytes.\nArtifact manifest: n.json sha256 {H}, 1 bytes.")
    ok = a["submission"] is None and b["submission"] is None and c["manifest"] is None and "ambiguous-submission" in codes(a) + codes(b) and "ambiguous-manifest" in codes(c)
    return ok, {"dup": codes(a), "cross": codes(b), "manifests": codes(c)}


@case("P6", "author test", "malformed N7 lines bind nothing: missing comma after ')', missing final period, trailing text, hash or label in attribution")
def p6(r):
    bad = {"no-comma": f"Returned: a.md (x, y) sha256 {H}, 1 bytes.", "no-period": f"Returned: a.md (x, y), sha256 {H}, 1 bytes",
           "trailing": f"Returned: a.md (x, y), sha256 {H}, 1 bytes. extra", "hash-attr": f"Returned: a.md (sha256 {H}), sha256 {H}, 1 bytes.",
           "label-attr": f"Returned: a.md (Submission: b), sha256 {H}, 1 bytes."}
    out = {k: (V2_N7(b)["submission"] is None, codes(V2_N7(b))) for k, b in bad.items()}
    return all(v[0] for v in out.values()), out


@case("P7", "author test", "LF and CRLF pointer blocks give identical parses in both contexts")
def p7(r):
    raw = FROZEN_PACK.read_bytes().replace(b"\r\n", b"\n")
    crlf = raw.replace(b"\n", b"\r\n")
    b1 = P3.wb.pointer_block(raw.decode("utf-8"))
    b2 = P3.wb.pointer_block(crlf.decode("utf-8"))
    return V2_N7(b1) == V2_N7(b2) and V2_N5(b1) == V2_N5(b2), {"n7_equal": V2_N7(b1) == V2_N7(b2), "n5_equal": V2_N5(b1) == V2_N5(b2)}


# ---------- integration: real legal punctuation files on an N5 page ----------
def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def n5_fixture(r: Path, suffix: str) -> Path:
    subprocess.run([sys.executable, "-B", str(LAB / "compat17/make_fixture.py"), "--room", str(r / "fx")], check=True, capture_output=True, env=ENV)
    repo = r / "fx/repo"
    book = repo / "00.kernel/00.00.10.work"
    page = book / "0599.fixture-n5"
    ev = page / "evidence/b"
    ev.mkdir(parents=True)
    art = ev / "artifact.md"
    art.write_bytes(b"SYNTHETIC artifact for the 0707/05.17 N5 punctuation case\n")
    ret = ev / f"return.md{suffix}"
    ret.write_bytes(b"SYNTHETIC N5 return in a legally punctuated filename\n" + b"x" * 420 + b"\n")
    man = ev / f"artifact-manifest.json{suffix}"
    man.write_bytes(json.dumps({"files": [{"path": "0599.fixture-n5/evidence/b/artifact.md", "bytes": art.stat().st_size, "sha256": sha(art.read_bytes())}]}).encode())
    rb, mb = ret.read_bytes(), man.read_bytes()
    pointer = (f"Submission: 0599.fixture-n5/evidence/b/return.md{suffix} sha256 {sha(rb)}, {len(rb)} bytes.\n"
               f"Artifact manifest: 0599.fixture-n5/evidence/b/artifact-manifest.json{suffix} sha256 {sha(mb)}, {len(mb)} bytes.\n")
    if suffix == ",":
        pointer = pointer.replace("return.md, sha256", "return.md, sha256")   # the collision form: ', sha256'
    (page / "05.01.md").write_text(f"# 05.01 SYNTHETIC N5 pack\n\n## Goal\nLab only.\n\n## Return pointer\n{pointer}\n## Review - Codex Prime\nPENDING.\n", encoding="utf-8")
    return repo


def prepare(repo: Path, patch: bool, source="0599.fixture-n5", pas="05.01"):
    argv = [sys.executable, "-B", str(LAB / "n7compat2.py")] + (["--patch"] if patch else []) + ["--repo-root", str(repo), "prepare",
            "--book", str(repo / "00.kernel/00.00.10.work"), "--source", source, "--pass", pas]
    p = subprocess.run(argv, capture_output=True, env=ENV, timeout=300)
    return p.returncode, (json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else {}), p.stderr.decode("utf-8", "replace")[-300:]


def rows_of(body):
    def find(o):
        if isinstance(o, dict):
            if isinstance(o.get("rows"), list):
                return o["rows"]
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        return None
    return sorted((x.get("role"), x.get("path"), x.get("sha256")) for x in (find(body) or []))


for sfx, name in ((",", "comma"), (")", "paren"), (";", "semicolon")):
    def make(sfx=sfx, name=name):
        def fn(r):
            repo = n5_fixture(r, sfx)
            rc0, b0, e0 = prepare(repo, False)
            rc1, b1, e1 = prepare(repo, True)
            same = (b0.get("intake_id") == b1.get("intake_id") and rows_of(b0) == rows_of(b1) and b0.get("measurement") == b1.get("measurement")
                    and sorted(f.get("code") for f in b0.get("findings", [])) == sorted(f.get("code") for f in b1.get("findings", [])))
            resolved = any(p and p.endswith("return.md" + sfx) for _, p, _ in rows_of(b1))
            return rc0 == 0 and rc1 == 0 and same and resolved, {"unpatched": {"intake_id": b0.get("intake_id"), "measurement": b0.get("measurement")},
                                                                  "patched": {"intake_id": b1.get("intake_id"), "measurement": b1.get("measurement")},
                                                                  "identical": same, "punctuated_file_resolved": resolved, "stderr": e1[-120:]}
        return fn
    case(f"I-N5-{name}", "author test", f"N5 page with REAL legal files return.md{sfx} and artifact-manifest.json{sfx}: unpatched (v7 path) and patched intake are identical (intake_id, rows, findings, measurement)")(make())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    if str(root.resolve()).lower().startswith(str(LIVE).lower()):
        sys.exit("refused: root inside the checkout")
    root.mkdir(parents=True, exist_ok=False)
    rows, first = [], None
    for cid, label, says, fn in CASES:
        r = root / cid
        r.mkdir()
        try:
            ok, detail = fn(r)
            status = "PASS" if ok else "FAIL"
        except Exception as ex:
            ok, detail, status = False, {"exception": f"{ex.__class__.__name__}: {ex}"[:400]}, "ERROR"
        rows.append({"id": cid, "label": label, "says": says, "status": status, "detail": detail})
        first = first or (cid if status != "PASS" else None)
        print(f"{status:5} {cid:13} {label[:40]:40} {says[:70]}")
    agg = {s: sum(1 for x in rows if x["status"] == s) for s in ("PASS", "FAIL", "ERROR")}
    Path(a.out).write_text(json.dumps({"schema": "n7-intake-tests/2", "root": str(root), "aggregate": agg, "first_failure": first, "rows": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg, "first failure", first)
    return 0 if agg["FAIL"] == 0 and agg["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
