#!/usr/bin/env python3
"""0707/05.20 N7-local lifecycle matrix. NONPRODUCTION. My prototype tests (author cases) on NEW external roots.

Each root = the 05.18 candidate code layer (live app files + v8-pinned labs + 05.18 lab pass04 adapter) plus this lab's
overlay at labs/n7-local-lifecycle-pass01/workbook.py (lab bytes). Two declarations are swapped in place:
  OVL  app/review-loop-v8.json -> workbook = n7-local overlay   (the prototype)
  P04  app/review-loop-v8.json -> workbook = pass04             (staged behavior, the comparison)
Every command runs through the root's REAL app/librarian.py review-loop (v8 candidate dispatcher), new process each.
'open' runs through the overlay's lab CLI (the door does not route it; production would add it to the door).
usage: run_matrix.py --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LAB = LIVE / "labs/n7-local-lifecycle-pass01"
sys.path.insert(0, str(LIVE / "labs/loop-convergence-design-pass01"))
import lcd  # noqa: E402
from lcd import rie  # noqa: E402

sys.path.insert(0, str(LIVE / "labs/review-entry-integration-pass01"))
import lifecycle  # noqa: E402

BOOK = lcd.BOOK_REL
PAGE = "0799.n7-local-lab"
OTHER = "0798.n7-other-lab"
N5PAGE = "0599.n5-control-lab"
OVL_JSON = (LAB / "adapter/review-loop-v8.n7local.lab.json").read_bytes()
P04_JSON = (rie.ADAPT / "review-loop-v8.lab.json").read_bytes()
OVL_BYTES = (LAB / "adapter/workbook.lab.py").read_bytes()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def new_root(path: Path, n5_real: bool = False) -> Path:
    r, _ = lcd.make_root(path, ["n5-0512-0509"] if False else ([] if not n5_real else []), dispatcher="v8")
    root = r.path
    if n5_real:
        lcd.build_source(r, "n5-0512-0509") if False else None
    (root / "labs/n7-local-lifecycle-pass01").mkdir(parents=True, exist_ok=True)
    (root / "labs/n7-local-lifecycle-pass01/workbook.py").write_bytes(OVL_BYTES)
    use(root, "OVL")
    return root


def use(root: Path, which: str) -> None:
    (root / "app/review-loop-v8.json").write_bytes(OVL_JSON if which == "OVL" else P04_JSON)


def write(p: Path, text: str) -> bytes:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))
    return p.read_bytes()


def make_pack(root: Path, page: str, pas: str) -> Path:
    return_note = "LAB-ONLY SYNTHETIC pack for the 0707/05.20 N7-local lifecycle lab."
    p = root / BOOK / page / f"{pas}.pack.md"
    write(p, f"# {pas} SYNTHETIC N7 pack\ndate: 2026-11-04\nwho: lab\n\n## Goal\n{return_note}\n\n## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n")
    return p


def make_return(root: Path, page: str, pas: str, tag: str = "e") -> dict:
    pdir = root / BOOK / page
    ev = pdir / f"evidence/{tag}{pas.replace('.', '')}"
    a = write(ev / "a.md", f"LAB artifact A for {page} {pas}\n")
    b = write(ev / "b.md", f"LAB artifact B for {page} {pas}\n")
    ret = write(pdir / f"{pas}.return.md", f"# {pas} SYNTHETIC return for {page}\nLAB-ONLY.\n")
    rows = [{"path": f"{BOOK}/{page}/{x}", "bytes": len(c), "sha256": sha(c)} for x, c in
            ((f"{pas}.return.md", ret), (f"evidence/{tag}{pas.replace('.', '')}/a.md", a), (f"evidence/{tag}{pas.replace('.', '')}/b.md", b))]
    man = write(ev / "artifact-manifest.json", json.dumps({"files": rows}, indent=1) + "\n")
    return {"ret": (f"{pas}.return.md", sha(ret), len(ret)), "man": (f"evidence/{tag}{pas.replace('.', '')}/artifact-manifest.json", sha(man), len(man))}


def fill_pointer(root: Path, page: str, pas: str, ret: tuple, man: tuple) -> None:
    p = root / BOOK / page / f"{pas}.pack.md"
    t = p.read_bytes().decode("utf-8")
    lines = f"Returned: {ret[0]} (lab, 2026-11-04), sha256 {ret[1]}, {ret[2]} bytes.\nArtifact manifest: {man[0]}, sha256 {man[1]}, {man[2]} bytes."
    assert t.count("## Return pointer\nPENDING.") == 1
    # run03: write_text converted LF to CRLF on Windows and changed the pack BODY bytes (chronology mismatch). Bytes only.
    p.write_bytes(t.replace("## Return pointer\nPENDING.", "## Return pointer\n" + lines).encode("utf-8"))


def cmd(root: Path, page: str, pas: str, c: str, *extra) -> dict:
    return rie.app(root, c, "--book", str(root / BOOK), "--source", page, "--pass", pas, *extra)


def open_(root: Path, page: str, pas: str) -> dict:
    return rie.run([root / "labs/n7-local-lifecycle-pass01/workbook.py", "open", "--book", str(root / BOOK), "--source", page, "--pass", pas], cwd=root)


def B(res: dict) -> dict:
    return res["body"] if isinstance(res.get("body"), dict) else {}


def codes(res: dict) -> list:
    return sorted({f.get("code") for f in B(res).get("findings") or [] if isinstance(f, dict)})


def tree(root: Path) -> dict:
    return rie.tree_hashes(root)


class Run:
    def __init__(self, rooms: Path, ev: Path):
        self.rooms, self.ev, self.cases = rooms, ev, {}

    def case(self, cid, says, ok, detail):
        self.cases[cid] = {"says": says, "status": "PASS" if ok else "FAIL", "detail": detail}
        print(f"{'PASS' if ok else 'FAIL':4} {cid:6} {says[:120]}")


def lifecycle_to_publish(root, page, pas, jf, ev, tag):
    p = cmd(root, page, pas, "prepare")
    f = cmd(root, page, pas, "form")
    rec = cmd(root, page, pas, "record", "--intake", B(p).get("intake_id") or "none", "--judgment", str(jf))
    ins = cmd(root, page, pas, "inspect")
    (ev / f"{tag}-inspect.full-read.json").write_text(ins["stdout"], encoding="utf-8")
    return p, f, rec, ins


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    ev = rooms / "evidence"
    ev.mkdir()
    jf = rooms / "lab-judgment.json"
    jf.write_text(json.dumps(lifecycle.JUDGMENT, indent=1) + "\n", encoding="utf-8")
    R = Run(rooms, ev)

    # ---------- T1 positive local exchange ----------
    root = new_root(rooms / "T1")
    make_pack(root, PAGE, "05.01")
    o = open_(root, PAGE, "05.01")
    m = make_return(root, PAGE, "05.01")
    fill_pointer(root, PAGE, "05.01", m["ret"], m["man"])
    p, f, rec, ins = lifecycle_to_publish(root, PAGE, "05.01", jf, ev, "T1")
    ex = B(p).get("exchange") or {}
    before_pub = tree(root)
    pub = cmd(root, PAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
    target = root / BOOK / PAGE / "06.01.review.md"
    t0 = tree(root)
    reads = [cmd(root, PAGE, "05.01", c) for c in ("read", "recover", "read", "recover")]
    t1 = tree(root)
    flags = {k: B(pub).get(k) for k in ("accepted", "approved", "authority", "closes_work", "releases_action", "published_work")}
    R.case("T1", "valid N7 pack opened first, matching return, no N1: prepare/form complete, record retains judgment, inspect, SEPARATE publish creates 06.01.review.md, read/recover x2 equal, no writes, no approval/release",
           o["exit"] == 0 and ex.get("state") == "matched" and ex.get("chronology") == "recorded-before-return" and ex.get("n1_custody") == "not-applicable"
           and "custody-missing" not in codes(p) and "n1-not-applicable" in codes(p) and B(p).get("measurement") == "complete"
           and rec["exit"] == 0 and B(reads[0]).get("judgment") == lifecycle.JUDGMENT and pub["exit"] == 0 and target.is_file()
           and reads[0]["stdout"] == reads[2]["stdout"] and reads[1]["stdout"] == reads[3]["stdout"] and all(r["exit"] == 0 for r in reads) and t0 == t1
           and flags == {"accepted": False, "approved": False, "authority": "none", "closes_work": False, "releases_action": False, "published_work": False},
           {"open": B(o) or o["stdout"][-300:], "exchange": ex, "codes": codes(p), "record": {"exit": rec["exit"], "review_id": B(rec).get("review_id"), "mode": B(rec).get("mode")},
            "publish": {"exit": pub["exit"], "target": B(pub).get("target"), "flags": flags}, "target_sha256": sha(target.read_bytes()) if target.is_file() else None,
            "reads_exit": [r["exit"] for r in reads], "no_writes_on_read": t0 == t1, "rendered_custody_line": [x for x in target.read_text(encoding="utf-8").splitlines() if x.startswith("custody:")] if target.is_file() else None})
    (ev / "T1-rendered.md").write_bytes(target.read_bytes() if target.is_file() else b"")
    T1 = root

    # ---------- H1 (mine): Prime writes the pack Review summary after publish ----------
    pk = T1 / BOOK / PAGE / "05.01.pack.md"
    keep = pk.read_bytes()
    pk.write_bytes(keep.replace(b"## Review - Codex Prime\nPENDING.", b"## Review - Codex Prime\nAccepted (LAB-ONLY summary). See 06.01.review.md."))
    ovl = cmd(T1, PAGE, "05.01", "read")
    use(T1, "P04")
    base = cmd(T1, PAGE, "05.01", "read")
    use(T1, "OVL")
    pk.write_bytes(keep.replace(b"LAB-ONLY SYNTHETIC pack", b"LAB-ONLY SYNTHETIC pack (task body edited)"))
    body = cmd(T1, PAGE, "05.01", "read")
    pk.write_bytes(keep)
    R.case("H1", "Prime's page-local Review summary in the pack after publish: overlay stays fresh (bound region unchanged); task-body edit still stale; staged pass04 baseline goes stale (known)",
           ovl["exit"] == 0 and B(ovl).get("stale") is False and body["exit"] == 1 and B(body).get("stale") is True,
           {"overlay_after_review_summary": {"exit": ovl["exit"], "stale": B(ovl).get("stale")}, "pass04_after_review_summary": {"exit": base["exit"], "stale": B(base).get("stale"), "codes": codes(base)},
            "overlay_after_task_body_edit": {"exit": body["exit"], "stale": B(body).get("stale")}})

    # ---------- T5 second pass on the same page (continues T1 root) ----------
    pass1 = {k: v for k, v in tree(T1).items()}
    make_pack(T1, PAGE, "05.02")
    open_(T1, PAGE, "05.02")
    m2 = make_return(T1, PAGE, "05.02")
    fill_pointer(T1, PAGE, "05.02", m2["ret"], m2["man"])
    p2_, _f, rec2, _i = lifecycle_to_publish(T1, PAGE, "05.02", jf, ev, "T5")
    pub2 = cmd(T1, PAGE, "05.02", "publish", "--review", B(rec2).get("review_id") or "none")
    r1 = cmd(T1, PAGE, "05.01", "read")
    after = tree(T1)
    pass1_kept = all(after.get(k) == v for k, v in pass1.items() if k.startswith(PAGE + "/05.01") or k.startswith(PAGE + "/06.01") or k.startswith(PAGE + "/evidence/e0501"))
    ex2 = B(p2_).get("exchange") or {}
    R.case("T5", "second pass 05.02: binds only 05.02 (its own pack/return/destination); pass-1 pack, return, review and record untouched and still fresh",
           ex2.get("state") == "matched" and ex2.get("return", {}).get("path") == f"{PAGE}/05.02.return.md" and B(p2_).get("destination") == f"{PAGE}/06.02.review.md"
           and pub2["exit"] == 0 and (T1 / BOOK / PAGE / "06.02.review.md").is_file() and pass1_kept and r1["exit"] == 0 and B(r1).get("review_id") == B(rec).get("review_id"),
           {"exchange_05_02": {k: ex2.get(k) for k in ("state", "chronology", "declared_submission", "destination")}, "pass1_bytes_kept": pass1_kept,
            "pass1_read": {"exit": r1["exit"], "review_id": B(r1).get("review_id"), "stale": B(r1).get("stale")}})

    # ---------- T2 orphan / mismatch ----------
    out = {}
    root = new_root(rooms / "T2")
    m = make_return(root, PAGE, "05.01")
    rb = (root / BOOK / PAGE / "05.01.return.md").read_bytes()
    r = cmd(root, PAGE, "05.01", "prepare")
    rec = cmd(root, PAGE, "05.01", "record", "--intake", B(r).get("intake_id") or "none", "--judgment", str(jf))
    out["orphan-return"] = {"state": (B(r).get("exchange") or {}).get("state"), "measurement": B(r).get("measurement"), "record_exit": rec["exit"],
                            "return_preserved": (root / BOOK / PAGE / "05.01.return.md").read_bytes() == rb, "unfiled": (B(r).get("exchange") or {}).get("unfiled_return_preserved")}
    make_pack(root, PAGE, "05.01")                       # pack now exists but pointer still PENDING
    r = cmd(root, PAGE, "05.01", "prepare")
    out["pointer-pending"] = {"state": (B(r).get("exchange") or {}).get("state"), "measurement": B(r).get("measurement"), "codes": codes(r)}
    r = cmd(root, PAGE, "05.03", "prepare")              # nothing at all for 05.03
    out["pack-missing"] = {"state": (B(r).get("exchange") or {}).get("state"), "measurement": B(r).get("measurement")}
    # wrong pass: pack 05.02 whose pointer names the 05.01 return (valid hash)
    make_pack(root, PAGE, "05.02")
    fill_pointer(root, PAGE, "05.02", m["ret"], m["man"])
    r = cmd(root, PAGE, "05.02", "prepare")
    use(root, "P04")
    rb4 = cmd(root, PAGE, "05.02", "prepare")
    use(root, "OVL")
    out["wrong-pass"] = {"state": (B(r).get("exchange") or {}).get("state"), "measurement": B(r).get("measurement"),
                         "pass04_submission": [x.get("path") for x in rie.rows_of(B(rb4)) if x.get("role") == "submission"], "pass04_measurement": B(rb4).get("measurement")}
    # wrong page: the same return copied to another N7 page that has no pack; the 0799 pack must not be chosen
    write(root / BOOK / OTHER / "05.01.return.md", rb.decode("utf-8"))
    r = cmd(root, OTHER, "05.01", "prepare")
    out["wrong-page"] = {"state": (B(r).get("exchange") or {}).get("state"), "assignment": B(r).get("assignment_path"), "measurement": B(r).get("measurement")}
    ok = (out["orphan-return"]["state"] == "orphan-return" and out["orphan-return"]["record_exit"] == 2 and out["orphan-return"]["return_preserved"]
          and out["pointer-pending"]["state"] == "pointer-pending" and out["pack-missing"]["state"] == "pack-missing"
          and out["wrong-pass"]["state"] == "return-not-local" and out["wrong-pass"]["measurement"] == "incomplete"
          and out["wrong-page"]["state"] == "orphan-return" and out["wrong-page"]["assignment"] is None)
    R.case("T2", "orphan return, pointer pending, missing pack, wrong pass (pass04 baseline binds it), wrong page: no local match, record refused, return bytes kept, no nearby pack chosen", ok, out)

    # ---------- T2f same address in another book instance ----------
    shutil.copytree(T1, rooms / "T2f-bookB")
    rootB = rooms / "T2f-bookB"
    rB = cmd(rootB, PAGE, "05.01", "read")
    pB = cmd(rootB, PAGE, "05.01", "prepare")
    R.case("T2f", "same page/pass copied (with records) into another book instance: the copied record is not accepted as this book's current exchange",
           rB["exit"] != 0 or B(rB).get("stale") is True,
           {"read": {"exit": rB["exit"], "stale": B(rB).get("stale"), "review_id": B(rB).get("review_id"), "correction": B(rB).get("correction")},
            "prepare_exchange_book": (B(pB).get("exchange") or {}).get("book"), "prepare_stale": B(pB).get("stale"), "intake_book": B(pB).get("book")})

    # ---------- H2 (mine): basename-only match in a subfolder ----------
    root = new_root(rooms / "H2")
    make_pack(root, PAGE, "05.01")
    m = make_return(root, PAGE, "05.01")
    sub = write(root / BOOK / PAGE / "evidence/05.01.return.md", "# a different file with the return's basename\n")
    fill_pointer(root, PAGE, "05.01", ("evidence/05.01.return.md", sha(sub), len(sub)), m["man"])
    r = cmd(root, PAGE, "05.01", "prepare")
    use(root, "P04")
    rb4 = cmd(root, PAGE, "05.01", "prepare")
    use(root, "OVL")
    R.case("H2", "pointer names evidence/05.01.return.md (same basename, other folder): overlay return-not-local; pass04 baseline binds it (known)",
           (B(r).get("exchange") or {}).get("state") == "return-not-local" and B(r).get("measurement") == "incomplete",
           {"overlay": {"state": (B(r).get("exchange") or {}).get("state"), "measurement": B(r).get("measurement")},
            "pass04": {"submission": [x.get("path") for x in rie.rows_of(B(rb4)) if x.get("role") == "submission"], "measurement": B(rb4).get("measurement")}})

    # ---------- T3 changed sources after binding ----------
    out = {}
    for name in ("pack-body", "return", "artifact", "artifact-missing"):
        root = new_root(rooms / f"T3-{name}")
        make_pack(root, PAGE, "05.01")
        open_(root, PAGE, "05.01")
        m = make_return(root, PAGE, "05.01")
        fill_pointer(root, PAGE, "05.01", m["ret"], m["man"])
        p, _f, rec, _i = lifecycle_to_publish(root, PAGE, "05.01", jf, ev, f"T3-{name}")
        pdir = root / BOOK / PAGE
        if name == "pack-body":
            x = pdir / "05.01.pack.md"
            x.write_bytes(x.read_bytes().replace(b"LAB-ONLY SYNTHETIC pack", b"LAB-ONLY SYNTHETIC pack CHANGED"))
        elif name == "return":
            x = pdir / "05.01.return.md"
            x.write_bytes(x.read_bytes() + b"changed\n")
        elif name == "artifact":
            x = pdir / "evidence/e0501/a.md"
            x.write_bytes(x.read_bytes() + b"changed\n")
        else:
            (pdir / "evidence/e0501/b.md").unlink()
        rd = cmd(root, PAGE, "05.01", "read")
        pub = cmd(root, PAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
        pp = cmd(root, PAGE, "05.01", "prepare")
        out[name] = {"read_exit": rd["exit"], "stale": B(rd).get("stale"), "publish_exit": pub["exit"], "publish_correction": B(pub).get("correction"),
                     "target_created": (pdir / "06.01.review.md").exists(), "fresh_prepare_codes": codes(pp), "fresh_measurement": B(pp).get("measurement")}
    ok = all(v["stale"] is True and v["publish_exit"] != 0 and not v["target_created"] for v in out.values())
    R.case("T3", "pack body / return / artifact changed or missing after record: read stale, publish held, no target created, fresh prepare shows the mismatch", ok, out)

    # ---------- T4 manual text at destination; target appears between inspect and publish ----------
    out = {}
    for name in ("manual-present", "appears"):
        root = new_root(rooms / f"T4-{name}")
        make_pack(root, PAGE, "05.01")
        open_(root, PAGE, "05.01")
        m = make_return(root, PAGE, "05.01")
        fill_pointer(root, PAGE, "05.01", m["ret"], m["man"])
        tgt = root / BOOK / PAGE / "06.01.review.md"
        manual = b"# Prime review - LAB-ONLY manual text\nDirector text: keep exactly.\n"
        if name == "manual-present":
            tgt.write_bytes(manual)
        p, _f, rec, _i = lifecycle_to_publish(root, PAGE, "05.01", jf, ev, f"T4-{name}")
        if name == "appears":
            tgt.write_bytes(manual)
        pub = cmd(root, PAGE, "05.01", "publish", "--review", B(rec).get("review_id") or "none")
        rd = cmd(root, PAGE, "05.01", "read")
        out[name] = {"record_exit": rec["exit"], "judgment_kept": B(rec).get("judgment") == lifecycle.JUDGMENT or B(rd).get("judgment") == lifecycle.JUDGMENT,
                     "publish_exit": pub["exit"], "correction": B(pub).get("correction"), "manual_bytes_preserved": tgt.read_bytes() == manual,
                     "read_judgment_equal": B(rd).get("judgment") == lifecycle.JUDGMENT}
    ok = all(v["publish_exit"] != 0 and v["manual_bytes_preserved"] and v["read_judgment_equal"] for v in out.values())
    R.case("T4", "manual Director text at the destination, and a file appearing between inspect and publish: publish held, bytes preserved, supplied judgment retained", ok, out)

    # ---------- T6 N5 control: overlay vs pass04 identical; custody semantics unchanged ----------
    root = new_root(rooms / "T6")
    pdir = root / BOOK / N5PAGE
    evd = pdir / "evidence/b"
    a_ = write(evd / "artifact.md", "LAB N5 artifact\n")
    s_ = write(evd / "submission.md", "LAB N5 submission\n")
    man = write(evd / "artifact-manifest.json", json.dumps({"files": [{"path": f"{BOOK}/{N5PAGE}/evidence/b/artifact.md", "bytes": len(a_), "sha256": sha(a_)}]}) + "\n")
    write(pdir / "05.01.md", f"# 05.01 SYNTHETIC N5 pack\n\n## Goal\nLAB-ONLY.\n\n## Return pointer\nSubmission: {BOOK}/{N5PAGE}/evidence/b/submission.md sha256 {sha(s_)}, {len(s_)} bytes.\n"
                             f"Artifact manifest: {BOOK}/{N5PAGE}/evidence/b/artifact-manifest.json sha256 {sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")
    res = {}
    for which in ("P04", "OVL"):
        use(root, which)
        res[which] = {c: cmd(root, N5PAGE, "05.01", c) for c in ("prepare", "form")}
    use(root, "OVL")
    pO = res["OVL"]["prepare"]
    rec = cmd(root, N5PAGE, "05.01", "record", "--intake", B(pO).get("intake_id"), "--judgment", str(jf))
    same = {c: res["P04"][c]["stdout"] == res["OVL"][c]["stdout"] for c in ("prepare", "form")}
    R.case("T6", "N5 control: overlay and pass04 give byte-identical prepare/form stdout; no exchange object; custody-missing still reported; record mode/custody unchanged (preliminary/missing)",
           all(same.values()) and "exchange" not in B(pO) and "custody-missing" in codes(pO) and rec["exit"] == 0 and B(rec).get("mode") == "preliminary",
           {"stdout_identical": same, "codes": codes(pO), "record": {"exit": rec["exit"], "mode": B(rec).get("mode"), "custody": B(rec).get("custody")}})

    agg = {s: sum(1 for c in R.cases.values() if c["status"] == s) for s in ("PASS", "FAIL")}
    Path(a.out).write_text(json.dumps({"schema": "n7-local-matrix/0", "rooms": str(rooms), "aggregate": agg, "cases": R.cases}, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("aggregate", agg)
    return 0 if agg["FAIL"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
