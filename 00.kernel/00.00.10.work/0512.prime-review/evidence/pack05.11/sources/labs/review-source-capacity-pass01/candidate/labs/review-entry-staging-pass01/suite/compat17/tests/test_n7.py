#!/usr/bin/env python3
"""Grammar and integration cases for the N7 intake lab (0707/05.16). NONPRODUCTION. Author tests.

G* in-process parser cases (the pinned pass03 is loaded read-only; original parsers are kept for comparison).
I* integration cases: each builds a NEW disposable fixture with make_fixture.py, edits only the copied pack's
   Return pointer, and runs prepare as a new process (unpatched and/or patched).
H* two author hostile cases. D2 tests the namespace hypothesis.
usage: test_n7.py --root NEW-DIR (outside the checkout) --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
LIVE = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LAB))
import n7compat  # noqa: E402

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
PAGE = "00.kernel/00.00.10.work/0707.app-use-check"
FROZEN_PACK = LIVE / PAGE / "evidence/pack05.16/sources" / PAGE / "05.15.pack.md"
P3 = n7compat.load_pass03()
ORIG_P3 = P3.parse_pointer
ORIG_P2 = P3.p2.parse_pointer
NEW = n7compat.make_parser(P3)
H64 = "a" * 64


def codes(p):
    return sorted({f["code"] for f in p["findings"]})


def block_of(raw: bytes) -> str:
    return P3.wb.pointer_block(raw.decode("utf-8", "replace"))


CASES = []


def case(cid, label, says):
    def deco(fn):
        CASES.append((cid, label, says, fn))
        return fn
    return deco


@case("G1", "author test", "old N5 Submission / Artifact manifest / Verification / counted forms parse exactly as the pinned pass03 parser does")
def g1(r):
    bodies = [f"Submission: 0599.x/evidence/build05.02/submission.md sha256 {H64}, 120 bytes.\nArtifact manifest: 0599.x/evidence/build05.02/m.json sha256 {H64}, 99 bytes.",
              f"Submission: s.md sha256 {H64}, 1 bytes.\nVerification: v.md sha256 {H64}, 2 bytes.",
              f"Artifact manifest: m.json sha256 {H64}, 9 bytes, 3 files.\nSubmission: s.md sha256 {H64}, 1 bytes.",
              "PENDING."]
    same = [NEW(b) == ORIG_P3(b) for b in bodies]
    return all(same), {"identical": same}


@case("G2", "known-failure reproduction + author test", "the real frozen 05.15 pointer: pass03 loses Returned and keeps the comma; the lab parser binds both exactly")
def g2(r):
    blk = block_of(FROZEN_PACK.read_bytes())
    old, new = ORIG_P3(blk), NEW(blk)
    ok = (old["submission"] is None and old["manifest"]["path"].endswith(",") and new["submission"]["path"] == "05.15.return.md"
          and new["submission"]["declared_form"] == "n7-returned" and new["manifest"]["path"] == "evidence/design05.15/artifact-manifest.json"
          and codes(new) == ["unparsed-return-line"])
    return ok, {"old_manifest_path": old["manifest"]["path"], "old_codes": codes(old), "new_submission": new["submission"], "new_codes": codes(new)}


@case("G3", "author test", "the same pointer from a CRLF copy of the pack parses identically")
def g3(r):
    raw = FROZEN_PACK.read_bytes()
    crlf = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return NEW(block_of(raw)) == NEW(block_of(crlf)), {"crlf_bytes": len(crlf)}


@case("G4", "author test", "two Returned lines -> ambiguous-submission; nothing bound")
def g4(r):
    b = f"Returned: a.md (x, y), sha256 {H64}, 1 bytes.\nReturned: b.md (x, y), sha256 {H64}, 1 bytes."
    p = NEW(b)
    return p["submission"] is None and "ambiguous-submission" in codes(p), {"codes": codes(p)}


@case("G5", "author test", "Returned plus an N5 Submission line conflict -> ambiguous-submission")
def g5(r):
    b = f"Returned: a.md (x, y), sha256 {H64}, 1 bytes.\nSubmission: s.md sha256 {H64}, 1 bytes."
    p = NEW(b)
    return p["submission"] is None and "ambiguous-submission" in codes(p), {"codes": codes(p)}


@case("G6", "author test", "N7 and N5 manifest lines together -> ambiguous-manifest")
def g6(r):
    b = f"Returned: a.md (x, y), sha256 {H64}, 1 bytes.\nArtifact manifest: m.json, sha256 {H64}, 1 bytes.\nArtifact manifest: m2.json sha256 {H64}, 1 bytes."
    p = NEW(b)
    return p["manifest"] is None and "ambiguous-manifest" in codes(p), {"codes": codes(p)}


@case("G7", "author test", "unrecognized punctuation is refused, never stripped: ';' after a path, double comma, and an N5 path ending in ','")
def g7(r):
    out = {}
    for name, b in (("semicolon", f"Returned: a.md; (x, y), sha256 {H64}, 1 bytes."),
                    ("double-comma", f"Returned: a.md (x, y), sha256 {H64}, 1 bytes.\nArtifact manifest: m.json,, sha256 {H64}, 1 bytes."),
                    ("n5-trailing-comma", f"Submission: s.md, sha256 {H64}, 1 bytes.")):
        p = NEW(b)
        out[name] = codes(p)
    # run01 expected one specific code for the double comma; either refusal code is correct as long as nothing binds
    refused = {"unparsed-return-line", "unrecognized-path-punctuation"}
    double = NEW(f"Returned: a.md (x, y), sha256 {H64}, 1 bytes.\nArtifact manifest: m.json,, sha256 {H64}, 1 bytes.")
    ok = ("unparsed-return-line" in out["semicolon"] and bool(refused & set(out["double-comma"])) and double["manifest"] is None
          and "unrecognized-path-punctuation" in out["n5-trailing-comma"])
    return ok, out


@case("G8", "author test", "a path starting with '.' or '/' does not match the grammar")
def g8(r):
    p1 = NEW(f"Returned: ../x.md (x, y), sha256 {H64}, 1 bytes.")
    p2 = NEW(f"Returned: /x.md (x, y), sha256 {H64}, 1 bytes.")
    return p1["submission"] is None and p2["submission"] is None, {"codes": [codes(p1), codes(p2)]}


@case("H1", "author hostile", "attribution text that smuggles a hash or a label is refused as not descriptive")
def h1(r):
    p1 = NEW(f"Returned: a.md (sha256 {H64}), sha256 {H64}, 1 bytes.")
    p2 = NEW(f"Returned: a.md (Submission: b.md), sha256 {H64}, 1 bytes.")
    ok = p1["submission"] is None and p2["submission"] is None and "attribution-not-descriptive" in codes(p1) and "attribution-not-descriptive" in codes(p2)
    return ok, {"codes": [codes(p1), codes(p2)]}


@case("D2", "author test (hypothesis REFUTED in run01; now asserts the true fact)", "pass03 installs its parser into pass02's namespace too, so intake uses pass03's grammar (counted form reachable)")
def d2(r):
    b = f"Submission: s.md sha256 {H64}, 1 bytes.\nArtifact manifest: m.json sha256 {H64}, 9 bytes, 3 files."
    by_p3, by_p2 = ORIG_P3(b), ORIG_P2(b)
    resolved = P3.p2.build_intake.__globals__["parse_pointer"] is ORIG_P2 if hasattr(P3.p2.build_intake, "__globals__") else None
    orig_build_globals = P3._original_build.__globals__["parse_pointer"] is ORIG_P2
    ok = by_p3["manifest"] is not None and by_p2 == by_p3 and ORIG_P2 is ORIG_P3
    return ok, {"pass03_parses_counted": by_p3["manifest"] is not None, "pass02_parses_counted": by_p2["manifest"] is not None,
                "intake_build_uses_pass02_parser": orig_build_globals}


# ---------- integration on fresh fixtures ----------
def fixture(r: Path) -> Path:
    subprocess.run([sys.executable, "-B", str(LAB / "make_fixture.py"), "--room", str(r / "fx")], check=True, capture_output=True, env=ENV)
    return r / "fx/repo"


def set_pointer(repo: Path, lines: list[str]):
    pack = repo / PAGE / "05.15.pack.md"
    raw = pack.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    head, rest = raw.split(b"## Return pointer" + nl, 1)
    tail = rest[rest.index(b"## Review - Codex Prime"):] if b"## Review - Codex Prime" in rest else b""
    pack.write_bytes(head + b"## Return pointer" + nl + nl.join(x.encode() for x in lines) + nl + nl + tail)


def prepare(repo: Path, patch: bool):
    argv = [sys.executable, "-B", str(LAB / "n7compat.py")] + (["--patch"] if patch else []) + ["--repo-root", str(repo), "prepare",
            "--book", str(repo / "00.kernel/00.00.10.work"), "--source", "0707.app-use-check", "--pass", "05.15"]
    p = subprocess.run(argv, capture_output=True, env=ENV, timeout=300)
    body = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else {}
    return p.returncode, body


def real_lines():
    blk = block_of(FROZEN_PACK.read_bytes())
    return [l for l in blk.split("\n") if l.strip()]


def mutate(lines, prefix, fn):
    return [fn(l) if l.startswith(prefix) else l for l in lines]


def icase(cid, says, lines_fn, expect_code, patch=True, prep=None):
    def fn(r):
        repo = fixture(r)
        if prep:
            prep(repo)
        set_pointer(repo, lines_fn())
        rc, body = prepare(repo, patch)
        cs = sorted({f.get("code") for f in body.get("findings", [])})
        return rc == 0 and body.get("measurement") == "incomplete" and expect_code in cs, {"exit": rc, "measurement": body.get("measurement"), "codes": cs}
    case(cid, "author test", says)(fn)


icase("I1", "wrong hash on the Returned line -> declared-hash-mismatch, incomplete",
      lambda: mutate(real_lines(), "Returned:", lambda l: re.sub(r"sha256 [0-9a-f]{64}", "sha256 " + "0" * 64, l)), "declared-hash-mismatch")
icase("I2", "wrong length on the manifest line -> declared-hash-mismatch, incomplete",
      lambda: mutate(real_lines(), "Artifact manifest:", lambda l: re.sub(r", (\d+) bytes\.", ", 1 bytes.", l)), "declared-hash-mismatch")
icase("I3", "manifest file missing -> declared-file-missing",
      real_lines, "declared-file-missing", prep=lambda repo: (repo / PAGE / "evidence/design05.15/artifact-manifest.json").unlink())
icase("I4", "one manifest payload missing -> artifact-missing",
      real_lines, "artifact-missing", prep=lambda repo: (repo / PAGE / "evidence/design05.15/COMPAT.md").unlink())
icase("I5", "traversal inside an accepted path shape (a/../../x.md) -> malformed-declared-path",
      lambda: mutate(real_lines(), "Returned:", lambda l: l.replace("Returned: 05.15.return.md", "Returned: a/../../05.15.return.md")), "malformed-declared-path")


@case("H2", "author hostile", "a decoy file literally named 'artifact-manifest.json,' exists: unpatched intake binds the decoy (hash mismatch); the lab parser binds the real manifest and never the decoy")
def h2(r):
    repo = fixture(r)
    decoy = repo / PAGE / "evidence/design05.15/artifact-manifest.json,"
    decoy.write_bytes(b'{"files": []}\n')
    rc0, b0 = prepare(repo, False)
    rc1, b1 = prepare(repo, True)
    c0 = sorted({f.get("code") for f in b0.get("findings", [])})
    c1 = sorted({f.get("code") for f in b1.get("findings", [])})
    ok = "declared-hash-mismatch" in c0 and b0.get("measurement") == "incomplete" and b1.get("measurement") == "complete" and "declared-hash-mismatch" not in c1
    return ok, {"unpatched": {"measurement": b0.get("measurement"), "codes": c0}, "patched": {"measurement": b1.get("measurement"), "codes": c1}}


@case("I6", "author test (expectation corrected after run01)", "a counted manifest line is parsed by UNPATCHED intake too (only Returned is lost); the patched intake is complete")
def i6(r):
    repo = fixture(r)
    man = repo / PAGE / "evidence/design05.15/artifact-manifest.json"
    data = man.read_bytes()
    n = len(json.loads(data)["files"])
    lines = [l for l in real_lines() if not l.startswith("Artifact manifest:")] + [
        f"Artifact manifest: evidence/design05.15/artifact-manifest.json sha256 {hashlib.sha256(data).hexdigest()}, {len(data)} bytes, {n} files."]
    set_pointer(repo, lines)
    rc0, b0 = prepare(repo, False)
    rc1, b1 = prepare(repo, True)
    c0 = sorted({f.get("code") for f in b0.get("findings", [])})
    ok = (not any("files." in (f.get("text") or "") for f in b0.get("findings", [])) and "submission-not-declared" in c0
          and b1.get("measurement") == "complete")
    return ok, {"unpatched_codes": c0, "patched_measurement": b1.get("measurement")}


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
        print(f"{status:5} {cid:4} {label[:34]:34} {says[:80]}")
    agg = {s: sum(1 for x in rows if x["status"] == s) for s in ("PASS", "FAIL", "ERROR")}
    Path(a.out).write_text(json.dumps({"schema": "n7-intake-tests/1", "root": str(root), "aggregate": agg, "first_failure": first, "rows": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg, "first failure", first)
    return 0 if agg["FAIL"] == 0 and agg["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
