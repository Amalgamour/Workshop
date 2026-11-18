#!/usr/bin/env python3
"""Disposable rehearsal for return-lines pass02.

Runs the unit tests, then full retirement, lookup, rollback, and synthetic
filings on external copies. It does not delete a work root or write the live book.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(r"D:\Git\lib-build")
LIVE = REPO / "00.kernel" / "00.00.10.work"
AUDIT_PATH = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
TOOL = REPO / "labs" / "return-lines-pass02" / "return_lines.py"
UNIT = REPO / "labs" / "return-lines-pass02" / "tests" / "test_pass02.py"
SEAM = REPO / "colab" / "labs" / "0709.return-migration-check" / "pass01" / "seam.py"
EXTERNAL = Path(r"D:\librarian\temp\0521-0504")
PASS01 = REPO / "labs" / "return-lines-pass01" / "return_lines.py"
PRIOR_PLAN = "52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66"

sys.path.insert(0, str(REPO / "labs" / "return-lines-pass02"))
import return_lines as tool  # noqa: E402

LINES = tool.load_lines()
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
PINS = {
    "labs/return-lines-pass01/return_lines.py": ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "labs/return-placement-pass01/return_placement.py": ("db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754", 66097),
    "labs/return-capture-pass01/return_capture.py": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
    "00.kernel/00.00.10.work/0417.return-placement/evidence/audit-corrected.json": ("c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606", 391778),
    "00.kernel/00.00.10.work/0100.band.returns/01.md": ("c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d", 10206),
    "00.kernel/00.00.10.work/0521.return-placement/evidence/pack05.04/source-manifest.json": ("e9e2d7af52c12b0643444704b4183e18ea9e0fee15812962ddad7d2b86d2fe21", 12387),
    "colab/labs/0709.return-migration-check/pass01/seam.py": ("dccd66af39dc8ca688610ca67a7b8903e6631191df2f232c3cd21574e8f08a4f", 5625),
    "labs/review-loop-pass03/review_loop.py": ("47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b", 55474),
}
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
LOG: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def fail(message: str) -> None:
    print("FAIL", message)
    raise SystemExit(1)


def pins_ok() -> None:
    for rel, (digest, size) in PINS.items():
        data = (REPO / rel).read_bytes()
        if sha(data) != digest or len(data) != size:
            fail(f"pin mismatch {rel}")


def cli(args: list[str]) -> tuple[int, dict, bytes]:
    proc = subprocess.run(
        [sys.executable, "-B", str(TOOL), *args],
        cwd=str(REPO),
        capture_output=True,
        env=ENV,
    )
    raw = proc.stdout
    body = {}
    if raw.strip():
        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            body = {}
    LOG.append({
        "argv": [str(TOOL), *args],
        "check": body.get("check"),
        "exit": proc.returncode,
        "stderr_sha256": sha(proc.stderr),
        "stderr_bytes": len(proc.stderr),
        "stdout_sha256": sha(raw),
        "stdout_bytes": len(raw),
    })
    if proc.returncode not in (0, 1, 2, 3) or (proc.returncode != 0 and not body):
        tail = proc.stderr.decode("utf-8", "replace")[-500:]
        fail(f"unreadable command {args[0]} exit {proc.returncode} stderr {tail}")
    return proc.returncode, body, raw


def expect(code: int, body: dict, wanted: int, label: str) -> None:
    if code != wanted:
        fail(f"{label} exit {code} check {body.get('check')} correction {str(body.get('correction'))[:500]}")


def copy_tree(src: Path, dest: Path) -> None:
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [item for item in dirnames if not LINES.is_reparse(os.path.join(dirpath, item))]
        for filename in filenames:
            source = Path(dirpath) / filename
            if LINES.is_reparse(str(source)):
                fail(f"reparse file in copy source {source}")
            rel = source.relative_to(src)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())


def fingerprint(audit: dict) -> str:
    rows = []
    paths = [REPO / entry["path"].replace("\\", "/") for entry in audit["files"]]
    paths.append(LIVE / "0100.band.returns" / "01.md")
    for path in paths:
        data = path.read_bytes()
        rows.append({"bytes": len(data), "path": path.relative_to(REPO).as_posix(), "sha256": sha(data)})
    rows.sort(key=lambda row: row["path"])
    return sha(dump(rows))


def layout_sha() -> str:
    return LINES.sha(LINES.dump(LINES.layout_body("00.00.10.work")))


def make_book(root: Path, audit: dict) -> None:
    book = root / "book"
    for part in ("book", "backup", "staging", "retired"):
        (root / part).mkdir(parents=True)
    copy_tree(LIVE / "0100.band.returns", book / "0100.band.returns")
    members = sorted({record["old_member"] for record in audit["records"]})
    for member in members:
        copy_tree(LIVE / member, book / member)
    for record in audit["records"]:
        if record.get("route") != "page-local-colab":
            continue
        rel = Path(record["target_return"])
        dest = book / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((LIVE / rel).read_bytes())
    print("copied", root.name, "members", len(members))


def write_auth(root: Path, audit_path: Path, plan: Path) -> None:
    raw = audit_path.read_bytes()
    body = {
        "audit_bytes": len(raw),
        "audit_sha256": sha(raw),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(root / "book"),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(OPS),
        "plan_sha256": sha(plan.read_bytes()),
        "release": tool.RELEASE_TEXT,
        "retired_root": str(root / "retired"),
        "schema": "return-line-authorization/1",
        "staging_root": str(root / "staging"),
        "synthetic": True,
    }
    (root / "auth.json").write_bytes(dump(body))


def auth_args(root: Path, plan: Path) -> list[str]:
    return [
        "--authorization", str(root / "auth.json"),
        "--audit", str(AUDIT_PATH),
        "--plan", str(plan),
        "--backup", str(root / "backup"),
        "--staging", str(root / "staging"),
        "--retired", str(root / "retired"),
    ]


def counts(audit: dict) -> dict:
    records = audit["records"]
    return {
        "incomplete_count": sum(1 for record in records if record.get("verify_exit") != 0),
        "page_local_count": sum(1 for record in records if record.get("route") == "page-local-colab"),
        "record_count": len(records),
    }


def occupant(record: dict) -> bool:
    prefix = str(record["target_line"]) + "."
    name = record["old_member"]
    return name.startswith(prefix) and name != record["target_page"]


def run_plan(root: Path) -> Path:
    plan = root / "plan.json"
    code, body, _raw = cli(["plan", "--book", str(root / "book"), "--audit", str(AUDIT_PATH), "--out", str(plan)])
    expect(code, body, 0, "plan")
    if body.get("detail", {}).get("live_moves") is not False or body.get("detail", {}).get("live_apply") is not False:
        # Plan detail may omit the flags. The plan file itself carries them.
        planned = json.loads(plan.read_bytes())
        if planned.get("live_moves") is not False or planned.get("live_apply") is not False:
            fail("plan live flags are not false")
    return plan


def through_retire(root: Path, audit: dict) -> dict:
    plan = run_plan(root)
    write_auth(root, AUDIT_PATH, plan)
    book = str(root / "book")
    code, body, _raw = cli(["init", "--book", book, "--name", "00.00.10.work", *auth_args(root, plan)])
    expect(code, body, 0, "init")
    derived = counts(audit)
    code, body, _raw = cli(["stage", "--book", book, *auth_args(root, plan)])
    expect(code, body, 0, "stage")
    for command in ("reconstruct", "publish"):
        code, body, _raw = cli([command, "--book", book, *auth_args(root, plan)])
        expect(code, body, 0, command)
        detail = body.get("detail") or {}
        for key, value in derived.items():
            if detail.get(key) != value:
                fail(f"{command} {key} {detail.get(key)} derived {value}")
        if detail.get("accepted") is not False or detail.get("published") is not False:
            fail(f"{command} claimed acceptance")
    code, body, _raw = cli(["retire", "--book", book, *auth_args(root, plan)])
    expect(code, body, 0, "retire")
    detail = body.get("detail") or {}
    if detail.get("record_count") != derived["record_count"] or detail.get("remaining_old_members") != 0:
        fail(f"retire counts {detail}")
    if detail.get("accepted") is not False or detail.get("published") is not False:
        fail("retire claimed acceptance")
    return {"plan_sha256": sha(plan.read_bytes()), "retire": body}


def assert_retired(root: Path, audit: dict) -> None:
    book = root / "book"
    for record in audit["records"]:
        if (book / record["old_member"]).exists():
            fail(f"old member still present {record['old_member']}")
    door = book / "0100.band.returns" / "01.md"
    if door.read_bytes() != (LIVE / "0100.band.returns" / "01.md").read_bytes():
        fail("copy door bytes changed")
    for record in audit["records"]:
        if record.get("route") != "page-local-colab":
            continue
        rel = Path(record["target_return"])
        if (book / rel).read_bytes() != (LIVE / rel).read_bytes():
            fail(f"tail changed {record['target_return']}")
    invented = book / "0110.colab-tools" / "05.01.return.md"
    if invented.exists():
        fail("invented 0154 return")
    manifest = json.loads((root / "staging" / "reconstruction-manifest.json").read_bytes())
    if manifest["record_count"] != counts(audit)["record_count"]:
        fail("manifest record_count is not the derived count")
    for item in manifest["records"]:
        if item["archived_identity"] == item["logical_return_path"]:
            fail(f"identity collapsed {item['archived_identity']}")
        if item["state"] == "incomplete" and (root / "staging" / "pages" / item["logical_return_path"]).exists():
            fail(f"incomplete path reconstructed {item['logical_return_path']}")


def lookup(book: Path, member: str) -> dict:
    code, body, raw = cli(["lookup", "--book", str(book), "--member", member])
    (book.parent / "lookups").mkdir(exist_ok=True)
    (book.parent / "lookups" / f"lookup-{member.split('.')[0]}.json").write_bytes(raw)
    return {"code": code, "body": body}


def assert_lookup(audit: dict, book: Path, member: str, where: str) -> dict:
    found = lookup(book, member)
    body = found["body"]
    record = next(item for item in audit["records"] if item["old_member"] == member)
    if record.get("verify_exit") != 0:
        expect(found["code"], body, 1, f"lookup {member}")
        described = body["descriptor"]
        if described.get("return_sha256") is not None or described.get("return_bytes") is not None:
            fail("incomplete lookup invented a return hash")
        if described.get("state") != "incomplete":
            fail("incomplete lookup state")
    else:
        expect(found["code"], body, 0, f"lookup {member}")
        described = body["descriptor"]
        if described.get("state") != "complete":
            fail(f"lookup {member} state {described.get('state')}")
    if set(body["descriptor"]) != set(LINES.DESCRIPTOR_KEYS):
        fail(f"lookup {member} descriptor keys")
    if body["descriptor"]["verification"]["tool_path"] != "labs/return-lines-pass01/return_lines.py":
        fail("lookup delegated to a tool other than pass01")
    retained = body["detail"]["retained_original"]
    if retained["book_member_present"] is not False:
        fail(f"lookup {member} still sees the book member")
    prefix = "occupants/" if occupant(record) else "originals/"
    if retained.get("retired_rel") != prefix + member:
        fail(f"lookup {member} retired_rel {retained.get('retired_rel')}")
    home = body["detail"]["new_home"]
    if home.get("logical_return_path") != record["target_return"] or home.get("target_page") != record["target_page"]:
        fail(f"lookup {member} new home {home}")
    if where == "legacy" and body["descriptor"].get("custody_format") != "legacy-relocated/1":
        fail(f"lookup {member} custody format")
    return body


def file_one(root: Path, plan: Path, page: str, batch: str, submission: str, target: str) -> None:
    folder = root / "filings" / submission
    folder.mkdir(parents=True)
    return_file = folder / "return.md"
    note = folder / "note.txt"
    text = (
        f"# SYNTHETIC fixture filing\n\n"
        f"submission: {submission}\n"
        f"page: {page}\n"
        f"batch: {batch}\n\n"
        f"This is not custody, acceptance, or a Prime receipt.\n"
    )
    return_file.write_bytes(text.encode("utf-8"))
    note.write_bytes(f"SYNTHETIC note {submission}\n".encode("utf-8"))
    book = str(root / "book")
    common = ["--book", book, "--page", page, "--batch", batch, "--submission", submission, *auth_args(root, plan)]
    code, body, _raw = cli([
        "reserve", *common, "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "synthetic fixture filing",
    ])
    expect(code, body, 1, f"reserve {submission}")
    code, body, _raw = cli([
        "capture", *common, "--return-file", str(return_file),
        "--artifact", "note.txt", str(note),
    ])
    expect(code, body, 0, f"capture {submission}")
    described = body.get("descriptor") or {}
    if described.get("custody_format") != "return-line-capture/1" or described.get("state") != "complete":
        fail(f"capture {submission} descriptor {described.get('custody_format')} {described.get('state')}")
    if set(described) != set(LINES.DESCRIPTOR_KEYS):
        fail(f"capture {submission} descriptor keys")
    if (body.get("detail") or {}).get("accepted") is not False:
        fail(f"capture {submission} accepted")
    receipt = root / "book" / target / f"{batch}.custody" / "receipt.json"
    parsed = json.loads(receipt.read_bytes())
    if parsed.get("accepted") is not False or parsed.get("schema") != "return-line-capture/1":
        fail(f"receipt {submission}")
    logical = root / "book" / target / f"{batch}.return.md"
    if logical.read_bytes() != return_file.read_bytes():
        fail(f"filed return bytes {submission}")


def filings(root: Path, audit: dict) -> None:
    plan = root / "plan.json"
    specs = [
        ("0521.synthetic-filing", "05.01", "synthetic-0521-0501", "0121.synthetic-filing"),
        ("0521.synthetic-filing", "05.02", "synthetic-0521-0502", "0121.synthetic-filing"),
        ("0522.synthetic-filing", "05.01", "synthetic-0522-0501", "0122.synthetic-filing"),
        ("0523.synthetic-filing", "05.01", "synthetic-0523-0501", "0123.synthetic-filing"),
        ("0524.synthetic-filing", "05.01", "synthetic-0524-0501", "0124.synthetic-filing"),
        ("0525.synthetic-filing", "05.01", "synthetic-0525-0501", "0125.synthetic-filing"),
        ("0721.synthetic-local", "05.01", "synthetic-0721-0501", "0721.synthetic-local"),
    ]
    for page, batch, submission, target in specs:
        file_one(root, plan, page, batch, submission, target)
    book = root / "book"
    for record in audit["records"]:
        if record["old_member"][:5] in {"0121.", "0122.", "0123.", "0124.", "0125."}:
            if (book / record["old_member"]).exists():
                fail(f"filing revived {record['old_member']}")
    first = book / "0121.synthetic-filing" / "05.01.return.md"
    second = book / "0121.synthetic-filing" / "05.02.return.md"
    if not first.is_file() or not second.is_file() or first.read_bytes() == second.read_bytes():
        fail("0121 did not keep two distinct passes")
    local = book / "0721.synthetic-local" / "05.01.return.md"
    if not local.is_file() or (book / "0171.synthetic-local").exists():
        fail("band 7 filing left its page")
    code, body, raw = cli([
        "descriptor", "--book", str(book), "--page", "0521.synthetic-filing", "--batch", "05.01",
    ])
    expect(code, body, 0, "descriptor synthetic")
    if body.get("schema") != "return-line-descriptor/1":
        fail("synthetic descriptor schema")
    (root / "lookups").mkdir(exist_ok=True)
    (root / "lookups" / "synthetic-descriptor.json").write_bytes(raw)
    code, body, _raw = cli(["verify", "--book", str(book), "--page", "0521.synthetic-filing", "--batch", "05.02"])
    expect(code, body, 0, "verify second pass")
    if (body.get("detail") or {}).get("accepted") is not False:
        fail("verify claimed acceptance")


def seam(primary: Path) -> dict:
    copy = primary.parent / "seam-book"
    copy_tree(primary / "book", copy)
    evidence = primary.parent / "seam-evidence"
    if evidence.exists():
        fail("seam evidence already exists")
    proc = subprocess.run(
        [sys.executable, "-B", str(SEAM), "--book", str(copy), "--evidence", str(evidence), "--lookups", str(primary / "lookups")],
        cwd=str(REPO),
        capture_output=True,
        env=ENV,
        timeout=600,
    )
    print("seam exit", proc.returncode)
    print(proc.stdout.decode("utf-8", "replace")[-1000:])
    if proc.returncode != 0:
        fail(proc.stderr.decode("utf-8", "replace")[-500:])
    report = json.loads((evidence / "seam.json").read_bytes())
    rows = report.get("rows") or []
    if len(rows) != 2:
        fail(f"seam rows {len(rows)}")
    for row in rows:
        obs = row.get("observation") or {}
        print("seam", row.get("label"), row.get("exit"), row.get("pass_state"), obs)
        if row.get("exit") != 0 or obs.get("state") != "complete" or obs.get("custody_verified") is not True:
            fail(f"seam case {row.get('label')} {obs}")
        if obs.get("task_association") != "not-established":
            fail(f"seam task association {obs.get('task_association')}")
    return {"rows": [{"label": row["label"], "exit": row["exit"], "observation": row["observation"], "pass_state": row["pass_state"]} for row in rows]}


def rollback(root: Path, audit: dict) -> None:
    by_member = {record["old_member"]: record for record in audit["records"]}
    book = root / "book"
    sample = by_member["0101.app-entry-0506"]
    occupied = by_member["0104.app-entry-0508"]
    tail_record = by_member["0165.bench-method-colab-0501"]
    sample_bytes = (book / sample["old_member"] / "return.md").read_bytes()
    occupied_bytes = (book / occupied["old_member"] / "return.md").read_bytes()
    tail_bytes = (book / tail_record["target_return"]).read_bytes()
    door_bytes = (book / "0100.band.returns" / "01.md").read_bytes()
    through_retire(root, audit)
    plan = root / "plan.json"
    logical = book / sample["target_return"]
    if not logical.is_file():
        fail("rollback copy did not publish the sample return")
    code, body, _raw = cli(["rollback-retire", "--book", str(book), *auth_args(root, plan)])
    expect(code, body, 0, "rollback-retire")
    if (book / sample["old_member"] / "return.md").read_bytes() != sample_bytes:
        fail("rolled-back original bytes differ")
    if (book / occupied["old_member"]).exists():
        fail("occupant returned before publication rollback")
    if logical.read_bytes() != (LIVE / sample["old_member"] / "return.md").read_bytes():
        fail("logical page changed during retirement rollback")
    code, body, _raw = cli(["rollback-publish", "--book", str(book), *auth_args(root, plan)])
    expect(code, body, 0, "rollback-publish")
    if logical.exists():
        fail("rollback-publish left the created return")
    if (book / occupied["target_return"]).exists():
        fail("rollback-publish left the occupant logical return")
    if (book / occupied["old_member"] / "return.md").read_bytes() != occupied_bytes:
        fail("restored occupant bytes differ")
    if (book / tail_record["target_return"]).read_bytes() != tail_bytes:
        fail("rollback removed or changed a page-local tail")
    if (book / "0100.band.returns" / "01.md").read_bytes() != door_bytes:
        fail("rollback changed the door")
    if (book / sample["old_member"] / "return.md").read_bytes() != sample_bytes:
        fail("sample original changed after publication rollback")


def main() -> None:
    pins_ok()
    live_layout = LIVE / "return-line-layout.json"
    layout_before = live_layout.read_bytes() if live_layout.exists() else None
    pass01_before = PASS01.read_bytes()
    audit = json.loads(AUDIT_PATH.read_bytes())
    before = fingerprint(audit)
    print("live fingerprint", before)
    unit = subprocess.run([sys.executable, "-B", str(UNIT)], cwd=str(REPO), capture_output=True, env=ENV)
    print("unit exit", unit.returncode)
    if unit.returncode != 0:
        print(unit.stderr.decode("utf-8", "replace")[-2000:])
        fail("unit tests")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = EXTERNAL / f"{stamp}-suite"
    primary = root / "primary"
    rolled = root / "rollback"
    make_book(primary, audit)
    make_book(rolled, audit)
    primary_result = through_retire(primary, audit)
    assert_retired(primary, audit)
    (primary / "lookups").mkdir()
    looked = assert_lookup(audit, primary / "book", "0101.app-entry-0506", "legacy")
    (primary / "lookups" / "lookup-0101.json").write_bytes(dump(looked))
    assert_lookup(audit, primary / "book", "0104.app-entry-0508", "legacy")
    assert_lookup(audit, primary / "book", "0121.archive-resolution-0508", "legacy")
    assert_lookup(audit, primary / "book", "0154.colab-support-first-0501", "legacy")
    assert_lookup(audit, primary / "book", "0165.bench-method-colab-0501", "legacy")
    filings(primary, audit)
    again = assert_lookup(audit, primary / "book", "0101.app-entry-0506", "legacy")
    if again["descriptor"]["return_sha256"] != looked["descriptor"]["return_sha256"]:
        fail("filing changed the relocated return hash")
    rollback(rolled, audit)
    seam_report = seam(primary)
    after = fingerprint(audit)
    layout_after = live_layout.read_bytes() if live_layout.exists() else None
    if after != before or layout_after != layout_before or PASS01.read_bytes() != pass01_before:
        fail("live bytes or pass01 changed")
    report = {
        "accepted": False,
        "approved": False,
        "archive_director_approved": False,
        "commands": len(LOG),
        "custody": "pending",
        "derived_counts": counts(audit),
        "live_fingerprint_after": after,
        "live_fingerprint_before": before,
        "live_mutation": False,
        "pass01_unchanged": True,
        "plan_sha256": primary_result["plan_sha256"],
        "prior_plan_sha256": PRIOR_PLAN,
        "prior_plan_required": False,
        "published": False,
        "receipt": None,
        "retired_root": str(primary / "retired"),
        "schema": "return-line-pass02-suite/1",
        "seam": seam_report,
        "unit_exit": unit.returncode,
        "work_root": str(root),
    }
    (root / "suite-report.json").write_bytes(dump(report))
    (root / "commands.json").write_bytes(dump({"commands": LOG}))
    print("OK", root)
    print("plan", primary_result["plan_sha256"])
    print("counts", counts(audit))


if __name__ == "__main__":
    main()
