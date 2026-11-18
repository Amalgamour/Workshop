#!/usr/bin/env python3
"""Author controls for the 0525/05.03 preflight. External roots only."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LAB = REPO / "labs" / "app-dependencies-pass03"
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
FAMILY = Path(r"D:\librarian\temp\0525-0503")
STAMP = FAMILY / "run-20261104b"
RECON = FAMILY / "reconstruct-20261104b"
FROZEN = (
    "labs/module-dependencies-pass02/depdecl.py",
    "labs/module-dependencies-pass01/depdecl.py",
    "app/librarian.py",
    "app/README.md",
    "labs/workbook-review-pass05/workbook.py",
    "app/review_loop_tools_v9.py",
    "labs/review-instance-binding-pass01/workbook.py",
    "labs/review-source-capacity-pass03/workbook.py",
    "labs/n7-local-lifecycle-pass01/workbook.py",
    "labs/review-report-hardening-pass01/report.py",
)
HOLD = (
    "Hold activation. The declared rows are a preflight of accepted pieces. "
    "Combined workbook W and reporter-on-W are pending. "
    "This report is not closure, compatibility, or release."
)


def sha(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def frozen_map() -> dict:
    out = {}
    for rel in FROZEN:
        body = (REPO / rel).read_bytes()
        out[rel] = {"sha256": sha(body), "bytes": len(body)}
    return out


def dump(path: Path, obj) -> str:
    raw = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return sha(raw)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def copy_set(dest: Path) -> None:
    dest.mkdir()
    shutil.copytree(LAB / "declarations", dest / "declarations")
    shutil.copytree(LAB / "fixtures", dest / "fixtures")
    shutil.copyfile(LAB / "set.json", dest / "set.json")


def retarget(dest: Path, decl_file: str, mutator) -> None:
    path = dest / decl_file
    doc = load(path)
    mutator(doc)
    digest = dump(path, doc)
    document = load(dest / "set.json")
    for row in document["declarations"]:
        if row["file"] == decl_file:
            row["sha256"] = digest
    dump(dest / "set.json", document)


def requirement(doc, rid):
    for item in doc["requirements"]:
        if item["id"] == rid:
            return item
    raise SystemExit("missing requirement " + rid)


def run_preflight(set_json: Path) -> tuple[int, dict, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [str(PY), "-B", str(LAB / "preflight.py"), "--set", str(set_json)],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        check=False,
        shell=False,
    )
    out = proc.stdout.decode("utf-8", errors="backslashreplace")
    err = proc.stderr.decode("utf-8", errors="backslashreplace")
    try:
        report = json.loads(out)
    except json.JSONDecodeError:
        report = {"raw": out, "stderr": err}
    return proc.returncode, report, err


def check(failures: list, name: str, cond: bool, detail: str) -> None:
    if not cond:
        failures.append("%s: %s" % (name, detail))


def closed(report) -> bool:
    return (
        report.get("activation_ready") is False
        and report.get("closure") is False
        and report.get("compatibility") is False
        and report.get("release") is False
        and report.get("recommendation") == HOLD
        and report.get("commit_authenticated") is False
        and "ready for activation" not in json.dumps(report)
    )


def pending_ok(report) -> bool:
    slots = report.get("pending_slots")
    if not isinstance(slots, list) or len(slots) != 2:
        return False
    ids = {item.get("id") for item in slots}
    return ids == {"combined-workbook-W", "reporter-on-W"} and all(
        item.get("path") is None and item.get("sha256") is None and item.get("state") == "pending"
        for item in slots
    )


def main() -> int:
    if STAMP.exists() or RECON.exists():
        sys.stderr.write("refused: stamp already exists\n")
        return 2
    FAMILY.mkdir(exist_ok=True)
    before = frozen_map()
    STAMP.mkdir()
    positive = STAMP / "positive"
    copy_set(positive)
    failures = []
    results = []

    code, report, err = run_preflight(positive / "set.json")
    (STAMP / "positive-preflight.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    (STAMP / "positive-preflight.err").write_text(err, encoding="utf-8", newline="\n")
    check(failures, "positive-exit", code == 0, str(code))
    check(failures, "positive-closed", closed(report), "flags")
    check(failures, "positive-pending", pending_ok(report), "slots")
    check(failures, "positive-validate", report.get("validate", {}).get("status") == "valid", str(report.get("validate")))
    identical = [row for row in report.get("identity", {}).get("rows", []) if row.get("result") == "identical"]
    check(failures, "positive-identity", len(identical) == 17 and not report.get("measured_faults"), str(report.get("measured_faults")))
    check(failures, "positive-basis", all(item.get("kind") == "observed-file" for item in report.get("basis", [])), "basis")
    check(failures, "positive-truncation", report.get("truncation", {}).get("depth_limit") is True, str(report.get("truncation")))
    check(failures, "positive-depth-exit", report.get("truncation", {}).get("depth1_exit") == 1, str(report.get("truncation")))
    check(failures, "positive-explain", report.get("truncation", {}).get("explain_paths", 0) >= 1, str(report.get("truncation")))
    unpinned = [
        edge for edge in report.get("edges", [])
        if edge.get("requirement_id") == "selected-v7" and edge.get("pin_form") == "unpinned"
    ]
    check(failures, "positive-unpinned", len(unpinned) == 1 and unpinned[0].get("resolution") == "selected", str(unpinned))
    disclosed = report.get("disclosed_dispatcher_difference") or []
    check(failures, "positive-disclosed", len(disclosed) == 1 and disclosed[0].get("resolution") == "pin-differs", str(disclosed))
    envs = set(report.get("unknown_environment") or [])
    check(failures, "positive-env", "python" in envs and "canonical-helper-root" in envs, str(envs))
    results.append({"case": "positive", "exit": code, "faults": report.get("measured_faults")})

    digest_only = STAMP / "digest-only"
    copy_set(digest_only)

    def make_digest(doc):
        requirement(doc, "pass05-workbook")["pin"]["bytes"] = None

    retarget(digest_only, "declarations/review-instance-workbook.json", make_digest)
    code, report, _err = run_preflight(digest_only / "set.json")
    forms = [
        edge for edge in report.get("edges", [])
        if edge.get("from") == "lib-build:labs/review-instance-binding-pass01/workbook.py"
        and edge.get("requirement_id") == "pass05-workbook"
    ]
    check(failures, "digest-exit", code == 0, str(code) + " " + str(report.get("measured_faults")))
    check(failures, "digest-form", len(forms) == 1 and forms[0].get("pin_form") == "digest-only" and forms[0].get("resolution") == "resolved", str(forms))
    check(failures, "digest-closed", closed(report) and pending_ok(report), "flags")
    results.append({"case": "digest-only", "exit": code, "pin_form": forms[0].get("pin_form") if forms else None})

    wrong = STAMP / "wrong-digest"
    copy_set(wrong)

    def flip_sha(doc):
        pin = requirement(doc, "pass04-workbook")["pin"]
        pin["sha256"] = ("0" if pin["sha256"][-1] != "0" else "1") + pin["sha256"][:-1]

    retarget(wrong, "declarations/workbook-review-pass05.json", flip_sha)
    code, report, _err = run_preflight(wrong / "set.json")
    check(failures, "wrong-digest-exit", code == 1, str(code))
    check(failures, "wrong-digest-fault", any("pin-differs" in item for item in report.get("measured_faults", [])), str(report.get("measured_faults")))
    check(failures, "wrong-digest-closed", closed(report), "flags")
    results.append({"case": "wrong-digest", "exit": code})

    length = STAMP / "wrong-length"
    copy_set(length)

    def bump(doc):
        doc["implementation"]["bytes"] = doc["implementation"]["bytes"] + 1

    retarget(length, "declarations/workbook-review-pass05.json", bump)
    code, report, _err = run_preflight(length / "set.json")
    length_rows = [
        row for row in report.get("identity", {}).get("rows", [])
        if row.get("module") == "lib-build:labs/workbook-review-pass05/workbook.py"
    ]
    check(failures, "wrong-length-exit", code == 1, str(code))
    check(failures, "wrong-length-result", len(length_rows) == 1 and length_rows[0].get("result") == "declaration-length-wrong", str(length_rows))
    check(failures, "wrong-length-fault", any("identity-pair-mismatch" in item for item in report.get("measured_faults", [])), str(report.get("measured_faults")))
    check(failures, "wrong-length-closed", closed(report), "flags")
    results.append({"case": "wrong-length", "exit": code})

    missing = STAMP / "missing-record"
    copy_set(missing)
    document = load(missing / "set.json")
    document["declarations"] = [row for row in document["declarations"] if row["file"] != "declarations/workbook-review-pass04.json"]
    document["select"] = [row for row in document["select"] if row["declaration_id"] != "workbook-review-pass04"]
    dump(missing / "set.json", document)
    code, report, _err = run_preflight(missing / "set.json")
    check(failures, "missing-record-exit", code == 1, str(code))
    check(failures, "missing-record-fault", any("record-missing" in item for item in report.get("measured_faults", [])), str(report.get("measured_faults")))
    check(failures, "missing-record-closed", closed(report), "flags")
    results.append({"case": "missing-record", "exit": code})

    gone = STAMP / "missing-file"
    copy_set(gone)
    (gone / "fixtures" / "labs__workbook-review-pass04__workbook.py").unlink()
    code, report, _err = run_preflight(gone / "set.json")
    check(failures, "missing-file-exit", code == 2, str(code))
    check(failures, "missing-file-refused", report.get("reader_refused") is True and report.get("activation_ready") is False, str(report.get("validate")))
    results.append({"case": "missing-file", "exit": code})

    hostile1 = STAMP / "hostile-digest-length"
    copy_set(hostile1)
    retarget(hostile1, "declarations/review-instance-workbook.json", make_digest)
    retarget(hostile1, "declarations/workbook-review-pass05.json", bump)
    code, report, _err = run_preflight(hostile1 / "set.json")
    h_rows = [
        row for row in report.get("identity", {}).get("rows", [])
        if row.get("module") == "lib-build:labs/workbook-review-pass05/workbook.py"
    ]
    h_in = []
    if h_rows:
        h_in = [
            item for item in h_rows[0].get("incoming", [])
            if item.get("requirement_id") == "pass05-workbook"
            and item.get("from") == "lib-build:labs/review-instance-binding-pass01/workbook.py"
        ]
    check(failures, "h1-exit", code == 1, str(code))
    check(failures, "h1-length", len(h_rows) == 1 and h_rows[0].get("result") == "declaration-length-wrong", str(h_rows))
    check(failures, "h1-digest", len(h_in) == 1 and h_in[0].get("form") == "digest-only" and h_in[0].get("relation") == "digest-matches", str(h_in))
    check(failures, "h1-closed", closed(report) and pending_ok(report), "flags")
    results.append({"case": "hostile-digest-length", "exit": code})

    hostile2 = STAMP / "hostile-git-blob"
    copy_set(hostile2)

    def git_blob(doc):
        doc["implementation"]["basis"] = {
            "kind": "git-blob",
            "repository": "lib-build",
            "commit": "0" * 40,
            "path": doc["module"]["path"],
            "verification": "supplied-unverified",
        }

    retarget(hostile2, "declarations/review-report-hardening.json", git_blob)
    code, report, _err = run_preflight(hostile2 / "set.json")
    bases = [item for item in report.get("basis", []) if item.get("declaration_id") == "review-report-hardening"]
    check(failures, "h2-exit", code == 0, str(code) + " " + str(report.get("measured_faults")))
    check(failures, "h2-basis", len(bases) == 1 and bases[0].get("kind") == "git-blob" and bases[0].get("verification") == "supplied-unverified", str(bases))
    check(failures, "h2-closed", closed(report) and report.get("commit_authenticated") is False, "flags")
    results.append({"case": "hostile-git-blob", "exit": code})

    RECON.mkdir()
    recon_set = RECON / "from-checkout"
    recon_set.mkdir()
    shutil.copytree(LAB / "declarations", recon_set / "declarations")
    (recon_set / "fixtures").mkdir()
    document = load(LAB / "set.json")
    for row in document["fixtures"]:
        rel = row["module"]["path"]
        source = (REPO / rel).read_bytes()
        if sha(source) != row["sha256"]:
            failures.append("reconstruct-source-drift: " + rel)
        target = recon_set / row["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source)
    dump(recon_set / "set.json", document)
    code, report, _err = run_preflight(recon_set / "set.json")
    check(failures, "reconstruct-exit", code == 0, str(code) + " " + str(report.get("measured_faults")))
    check(failures, "reconstruct-identity", all(row.get("result") == "identical" for row in report.get("identity", {}).get("rows", [])), "identity")
    recon_bad = RECON / "wrong-digest"
    copy_from = recon_set
    recon_bad.mkdir()
    shutil.copytree(copy_from / "declarations", recon_bad / "declarations")
    shutil.copytree(copy_from / "fixtures", recon_bad / "fixtures")
    shutil.copyfile(copy_from / "set.json", recon_bad / "set.json")
    retarget(recon_bad, "declarations/workbook-review-pass05.json", flip_sha)
    code, report, _err = run_preflight(recon_bad / "set.json")
    check(failures, "reconstruct-negative", code == 1 and any("pin-differs" in item for item in report.get("measured_faults", [])), str(code))
    results.append({"case": "reconstruct", "positive_exit": 0, "negative_exit": code})

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [str(PY), "-B", "-X", "dev", str(REPO / "labs" / "module-dependencies-pass02" / "tests" / "test_repair02.py"), "-v"],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        check=False,
        shell=False,
    )
    (STAMP / "reader-regression.stdout").write_bytes(proc.stdout)
    (STAMP / "reader-regression.stderr").write_bytes(proc.stderr)
    check(failures, "reader-regression", proc.returncode == 0, "exit %s" % proc.returncode)
    results.append({"case": "reader-regression", "exit": proc.returncode})

    after = frozen_map()
    check(failures, "frozen", before == after, "frozen inputs changed")
    reader_now = sha((REPO / "labs" / "module-dependencies-pass02" / "depdecl.py").read_bytes())
    check(failures, "reader-pin", reader_now == before["labs/module-dependencies-pass02/depdecl.py"]["sha256"], reader_now)

    summary = {
        "schema": "app-dependency-preflight-suite/1",
        "failures": failures,
        "results": results,
        "frozen": before,
        "stamp": str(STAMP),
        "reconstruct": str(RECON),
    }
    dump(STAMP / "suite.json", summary)
    print("failures", len(failures))
    for item in failures:
        print(item)
    print("cases", len(results))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
