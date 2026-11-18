#!/usr/bin/env python3
"""#05 hostile integration cases through the REAL entry on disposable roots (0707/05.18). NONPRODUCTION.
Author cases with lab fault injection; each case builds its own NEW root. Labels:
  PACK = a case from the 05.18 pack list; NEW = one of my two additional hostile cases; DISPATCH = unchanged routes.
usage: hostile.py --rooms NEW-DIR --out FILE [--only ID ...]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402
import lifecycle  # noqa: E402

CASES = []
H = "a" * 64


def case(cid, label, says):
    def deco(fn):
        CASES.append((cid, label, says, fn))
        return fn
    return deco


def root_for(rooms, cid, key="n7-0515", omit=(), dispatcher="v8"):
    root, info = rie.make_root(rooms / cid, key, omit=omit, dispatcher=dispatcher)
    return root.path, info


def prep(root, key="n7-0515"):
    return rie.app(root, *rie.wb_args(root, key, "prepare"))


def codes(res):
    b = res.get("body") if isinstance(res.get("body"), dict) else {}
    return sorted({f.get("code") for f in b.get("findings") or [] if isinstance(f, dict)})


def tamper(p: Path):
    p.write_bytes(p.read_bytes() + b"\n# LAB tamper\n")


def edit_decl(root, fn):
    p = root / "app/review-loop-v8.json"
    d = json.loads(p.read_bytes())
    fn(d)
    p.write_bytes((json.dumps(d, indent=2, sort_keys=True) + "\n").encode())


def set_pointer(root, key, lines):
    fx = rie.FIXTURES[key]
    pf = root / rie.BOOK_REL / fx["page"] / fx["pointer"]
    t = pf.read_text(encoding="utf-8")
    head, rest = t.split("## Return pointer\n", 1)
    parts = rest.split("\n## ", 1)                        # hostile01: the pointer can be the LAST section
    tail = ("\n## " + parts[1]) if len(parts) == 2 else ""
    pf.write_text(head + "## Return pointer\n" + "\n".join(lines) + "\n" + tail, encoding="utf-8")


def real_pointer_lines(root, key="n7-0515"):
    fx = rie.FIXTURES[key]
    t = (root / rie.BOOK_REL / fx["page"] / fx["pointer"]).read_text(encoding="utf-8")
    return [x for x in t.split("## Return pointer\n", 1)[1].split("\n## ", 1)[0].splitlines() if x.strip()]


def refused(res, text):
    return res["exit"] == 2 and text in res["stderr"]


@case("P01", "PACK", "wrong v8 tool hash: a pinned tool (review_loop pass03) altered in the root -> the door refuses before the workbook runs")
def p01(rooms):
    root, _ = root_for(rooms, "P01")
    tamper(root / "labs/review-loop-pass03/review_loop.py")
    r = prep(root)
    return refused(r, "pinned tool hash does not match: labs/review-loop-pass03/review_loop.py"), {"exit": r["exit"], "stderr": r["stderr"][-200:]}


@case("P02", "PACK", "wrong transitive dependency: pass02 / pass03 altered in the root -> refused (door predecessor pins)")
def p02(rooms):
    out = {}
    for name, rel, text in (("pass02", "labs/workbook-review-pass02/workbook.py", "pass02 pin mismatch"),
                            ("pass03", "labs/workbook-review-pass03/workbook.py", "pass03 pin mismatch")):   # hostile01 expected the RESOLVE text; the predecessor pin fires first
        root, _ = root_for(rooms, f"P02-{name}")
        tamper(root / rel)
        r = prep(root)
        out[name] = {"exit": r["exit"], "stderr": r["stderr"][-200:], "ok": refused(r, text)}
    return all(v["ok"] for v in out.values()), out


@case("P03", "PACK", "wrong schema / unknown key / wrong length in review-loop-v8.json -> refused")
def p03(rooms):
    out = {}
    muts = {"schema": (lambda d: d.__setitem__("schema", "review-loop-pins/5"), "schema is not review-loop-pins/6"),
            "extra-key": (lambda d: d["tools"]["workbook"].__setitem__("note", "x"), "does not match the pinned tools"),
            "length": (lambda d: d["tools"]["workbook"].__setitem__("bytes", d["tools"]["workbook"]["bytes"] + 1), "pinned tool hash does not match"),
            "v7-declaration-name": (lambda d: d["tools"].pop("workbook_pass03"), "does not match the pinned tools")}
    for name, (fn, text) in muts.items():
        root, _ = root_for(rooms, f"P03-{name}")
        edit_decl(root, fn)
        r = prep(root)
        out[name] = {"exit": r["exit"], "stderr": r["stderr"][-200:], "ok": refused(r, text)}
    return all(v["ok"] for v in out.values()), out


@case("P04", "PACK", "missing dependency: prime_cycle pass03 removed from the root -> refused as missing")
def p04(rooms):
    root, _ = root_for(rooms, "P04")
    (root / "labs/prime-cycle-pass03/prime_cycle.py").unlink()
    r = prep(root)
    return refused(r, "pinned tool is missing: labs/prime-cycle-pass03/prime_cycle.py"), {"exit": r["exit"], "stderr": r["stderr"][-200:]}


@case("P05", "PACK", "missing / tampered manifest artifact on the real N7 0517 copy -> artifact-missing / artifact-hash-mismatch, incomplete")
def p05(rooms):
    out = {}
    for name, act, code in (("missing", "unlink", "artifact-missing"), ("tampered", "tamper", "artifact-hash-mismatch")):
        root, info = root_for(rooms, f"P05-{name}", key="n7-0517")
        target = root / info["manifest_rows"][2]
        target.unlink() if act == "unlink" else tamper(target)
        r = prep(root, "n7-0517")
        b = r["body"] or {}
        out[name] = {"target": info["manifest_rows"][2], "codes": codes(r), "measurement": b.get("measurement"),
                     "ok": code in codes(r) and b.get("measurement") == "incomplete"}
    return all(v["ok"] for v in out.values()), out


@case("P06", "PACK", "conflicting duplicate pointer (two Returned lines) on the real N7 page -> ambiguous-submission, nothing bound")
def p06(rooms):
    root, _ = root_for(rooms, "P06")
    lines = real_pointer_lines(root)
    ret = [x for x in lines if x.startswith("Returned:")][0]
    set_pointer(root, "n7-0515", lines + [ret.replace("05.15.return.md", "06.15.notes.md")])
    r = prep(root)
    rows = rie.rows_of(r["body"])
    return "ambiguous-submission" in codes(r) and not any(x.get("role") == "submission" for x in rows), {"codes": codes(r)}


@case("P07", "PACK", "illegal traversal inside an accepted path shape (Returned: a/../../x.md) -> malformed-declared-path")
def p07(rooms):
    root, _ = root_for(rooms, "P07")
    lines = [x for x in real_pointer_lines(root) if not x.startswith("Returned:")]
    set_pointer(root, "n7-0515", [f"Returned: evidence/../../x.md (lab), sha256 {H}, 1 bytes."] + lines)
    r = prep(root)
    return "malformed-declared-path" in codes(r), {"codes": codes(r), "measurement": (r["body"] or {}).get("measurement")}


@case("P08", "PACK", "misleading attribution (a hash / a label inside the parentheses) -> attribution-not-descriptive, not bound")
def p08(rooms):
    out = {}
    for name, attr in (("hash", f"sha256 {'b' * 64}"), ("label", "Submission: 06.15.notes.md")):
        root, _ = root_for(rooms, f"P08-{name}")
        lines = real_pointer_lines(root)
        lines = [x.replace("(claude-opus-5-5, 2026-11-03)", f"({attr})") if x.startswith("Returned:") else x for x in lines]
        set_pointer(root, "n7-0515", lines)
        r = prep(root)
        out[name] = {"codes": codes(r), "ok": "attribution-not-descriptive" in codes(r) and not any(x.get("role") == "submission" for x in rie.rows_of(r["body"]))}
    return all(v["ok"] for v in out.values()), out


@case("P09", "PACK", "source change between prepare and record -> record refused (the intake no longer matches)")
def p09(rooms):
    root, info = root_for(rooms, "P09")
    p = prep(root)
    iid = (p["body"] or {}).get("intake_id")
    tamper(root / info["declared"]["Submission"][0])
    jf = rooms / "P09-judgment.json"
    jf.write_text(json.dumps(lifecycle.JUDGMENT), encoding="utf-8")
    r = rie.app(root, *rie.wb_args(root, "n7-0515", "record", "--intake", iid, "--judgment", str(jf)))
    store = sorted(str(x.relative_to(root)) for x in (root / rie.BOOK_REL).rglob("*") if "workbook-review" in str(x) and x.is_file())
    return r["exit"] != 0 and not any("record" in s for s in store), {"exit": r["exit"], "stdout_tail": r["stdout"][-400:], "stderr": r["stderr"][-200:], "store": store}


@case("P10", "PACK", "existing manual review: see lifecycle L3 (06.15.review.md preserved, publish held manual-review)")
def p10(rooms):
    return None, {"see": "life01.json L3"}


@case("P11", "PACK", "a manual target appears between record and publish -> publish held, the manual text preserved byte-for-byte")
def p11(rooms):
    root, _ = root_for(rooms, "P11", omit=("06.15.review.md",))
    p = prep(root)
    jf = rooms / "P11-judgment.json"
    jf.write_text(json.dumps(lifecycle.JUDGMENT), encoding="utf-8")
    rec = rie.app(root, *rie.wb_args(root, "n7-0515", "record", "--intake", (p["body"] or {}).get("intake_id"), "--judgment", str(jf)))
    target = root / rie.BOOK_REL / "0707.app-use-check/06.15.review.md"
    manual = b"# Prime review - LAB-ONLY manual text that appeared before publish\nDirector text: keep.\n"
    target.write_bytes(manual)
    pub = rie.app(root, *rie.wb_args(root, "n7-0515", "publish", "--review", (rec["body"] or {}).get("review_id") or "none"))
    b = pub["body"] or {}
    return pub["exit"] != 0 and target.read_bytes() == manual, {"exit": pub["exit"], "correction": b.get("correction"), "preserved": target.read_bytes() == manual}


@case("P12", "PACK", "stale selection after rollback: v8 files left inert, v7 dispatcher selected -> review-loop runs the v7 door (N7 incomplete again); see rollback.json")
def p12(rooms):
    root, _ = root_for(rooms, "P12", dispatcher="v8")
    c = prep(root)
    rie.select(root, "v7")
    v = prep(root)
    return (c["body"] or {}).get("measurement") == "complete" and (v["body"] or {}).get("measurement") == "incomplete" and \
        "unparsed-return-line" in codes(v), {"v8": (c["body"] or {}).get("measurement"), "after_rollback": (v["body"] or {}).get("measurement"), "codes": codes(v)}


@case("P13", "PACK", "LF vs CRLF pack page on the real N7 entry -> identical declared/artifact rows (assignment bytes differ by design)")
def p13(rooms):
    out = {}
    for name in ("lf", "crlf"):
        root, _ = root_for(rooms, f"P13-{name}")
        pf = root / rie.BOOK_REL / "0707.app-use-check/05.15.pack.md"
        raw = pf.read_bytes().replace(b"\r\n", b"\n")
        pf.write_bytes(raw.replace(b"\n", b"\r\n") if name == "crlf" else raw)
        r = prep(root)
        rows = sorted(json.dumps(x, sort_keys=True) for x in rie.rows_of(r["body"]) if x.get("role") != "assignment")
        out[name] = {"measurement": (r["body"] or {}).get("measurement"), "rows_sha": rie.sha("\n".join(rows).encode()), "n": len(rows)}
    return out["lf"]["rows_sha"] == out["crlf"]["rows_sha"] and out["crlf"]["measurement"] == "complete", out


@case("N01", "NEW", "PRODUCTION pass04 bytes + PRODUCTION v8 declaration in a copied root: the door accepts the pins, the workbook REFUSES (canonical-root guard) instead of silently mixing roots")
def n01(rooms):
    root, _ = root_for(rooms, "N01")
    (root / "labs/workbook-review-pass04/workbook.py").write_bytes((rie.CAND / "labs/workbook-review-pass04/workbook.py").read_bytes())
    (root / "app/review-loop-v8.json").write_bytes((rie.CAND / "app/review-loop-v8.json").read_bytes())
    r = prep(root)
    return r["exit"] == 2 and "not at its canonical root" in r["stderr"] and not r["stdout"].strip(), {"exit": r["exit"], "stderr": r["stderr"][-200:]}


@case("N02", "NEW", "a decoy file literally named 'artifact-manifest.json,' beside the real manifest on the real N7 entry: the decoy is never bound")
def n02(rooms):
    root, _ = root_for(rooms, "N02")
    ev = root / rie.BOOK_REL / "0707.app-use-check/evidence/design05.15"
    (ev / "artifact-manifest.json,").write_bytes(b'{"files": []}\n')
    r = prep(root)
    rows = rie.rows_of(r["body"])
    man = [x.get("path") for x in rows if x.get("role") == "artifact-manifest"]
    return man == ["0707.app-use-check/evidence/design05.15/artifact-manifest.json"] and (r["body"] or {}).get("measurement") == "complete", {"manifest_rows": man}


@case("D01", "DISPATCH", "authoring / return-lines / review-loop / unknown command: harmless no-argument calls give identical exit, stdout and stderr under v7 and v8 selection")
def d01(rooms):
    root, _ = root_for(rooms, "D01", dispatcher="v7")
    calls = [["authoring"], ["return-lines"], ["review-loop"], ["review-loop", "nonsense"], ["authoring", "inspect"], ["return-lines", "status"], ["run"]]
    res = {}
    for which in ("v7", "v8"):
        rie.select(root, which)
        before = rie.tree_hashes(root, "")
        for c in calls:
            r = rie.run([root / "app/librarian.py", *c], cwd=root, timeout=120)
            res.setdefault(" ".join(c), {})[which] = {"exit": r["exit"], "stdout": r["stdout"][-300:], "stderr": r["stderr"][-300:]}
        after = rie.tree_hashes(root, "")
        changed = sorted(k for k in after if after.get(k) != before.get(k) and k != "app/librarian.py")
        res.setdefault("_writes", {})[which] = changed
    same = {k: v["v7"] == v["v8"] for k, v in res.items() if not k.startswith("_")}
    return all(same.values()) and not res["_writes"]["v7"] and not res["_writes"]["v8"], {"same": same, "calls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", action="append")
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    rows = []
    for cid, label, says, fn in CASES:
        if a.only and cid not in a.only:
            continue
        try:
            ok, detail = fn(rooms)
            status = "SEE" if ok is None else ("PASS" if ok else "FAIL")
        except SystemExit as ex:
            ok, detail, status = False, {"exit": str(ex)}, "ERROR"
        except Exception as ex:
            ok, detail, status = False, {"exception": f"{ex.__class__.__name__}: {ex}"[:400]}, "ERROR"
        rows.append({"id": cid, "label": label, "says": says, "status": status, "detail": detail})
        print(f"{status:5} {cid:4} {label:8} {says[:110]}")
    agg = {s: sum(1 for x in rows if x["status"] == s) for s in ("PASS", "FAIL", "ERROR", "SEE")}
    Path(a.out).write_text(json.dumps({"schema": "rie-hostile/1", "rooms": str(rooms), "aggregate": agg, "rows": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg)
    return 0 if agg["FAIL"] == 0 and agg["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
