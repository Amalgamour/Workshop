#!/usr/bin/env python3
"""One designated-live copy rehearsal for return-lines pass03.

Runs the focused tests, then one retained copy through retirement, lookup,
synthetic filings, the historical reader, and the descriptor seam.
It also writes a read-only live plan and refuses the release candidate.
It does not delete a work root, create the proposed archive, or migrate the live book.
"""

from __future__ import annotations

import hashlib
import io
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
EVIDENCE = LIVE / "0521.return-placement" / "evidence" / "build05.05"
TOOL_FILE = REPO / "labs" / "return-lines-pass03" / "return_lines.py"
UNIT = REPO / "labs" / "return-lines-pass03" / "tests" / "test_pass03.py"
SEAM = REPO / "colab" / "labs" / "0709.return-migration-check" / "pass01" / "seam.py"
READER = REPO / "labs" / "return-capture-pass01" / "return_capture.py"
EXTERNAL = Path(r"D:\librarian\temp\0521-0505")
PASS01 = REPO / "labs" / "return-lines-pass01" / "return_lines.py"
PASS02 = REPO / "labs" / "return-lines-pass02" / "return_lines.py"
PRIOR_PLAN = "52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66"
PROPOSED = {
    "backup": Path(r"D:\librarian\return-placement\0521-backup"),
    "retired": Path(r"D:\Git\lib-build\00.archive\0521.return-lines"),
    "staging": Path(r"D:\librarian\return-placement\0521-staging"),
}
sys.path.insert(0, str(REPO / "labs" / "return-lines-pass03"))
import return_lines as tool  # noqa: E402

LINES = tool.load_pass02().load_lines()
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
PINS = {
    "labs/return-lines-pass02/return_lines.py": ("6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908", 82908),
    "labs/return-lines-pass01/return_lines.py": ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "labs/return-placement-pass01/return_placement.py": ("db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754", 66097),
    "labs/return-capture-pass01/return_capture.py": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
    "00.kernel/00.00.10.work/0417.return-placement/evidence/audit-corrected.json": ("c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606", 391778),
    "00.kernel/00.00.10.work/0100.band.returns/01.md": ("c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d", 10206),
    "colab/labs/0709.return-migration-check/pass01/seam.py": ("dccd66af39dc8ca688610ca67a7b8903e6631191df2f232c3cd21574e8f08a4f", 5625),
    "labs/review-loop-pass03/review_loop.py": ("47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b", 55474),
    "labs/prime-cycle-pass03/prime_cycle.py": ("496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c", 76045),
}
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
LOG: list[dict] = []
TEST_TEXT = "TEST RECORDING for the 05.05 designated-live copy. Not a Director release. Not live authority.\n"


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


def record(argv: list[str], code: int, raw: bytes, stderr: bytes, designated: bool) -> dict:
    body = {}
    if raw.strip():
        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            body = {}
    LOG.append({
        "argv": argv,
        "check": body.get("check"),
        "designated_live": designated,
        "exit": code,
        "stderr_bytes": len(stderr),
        "stderr_sha256": sha(stderr),
        "stdout_bytes": len(raw),
        "stdout_sha256": sha(raw),
    })
    return body


def cli(args: list[str], designated: str | None = None) -> tuple[int, dict, bytes]:
    buf = io.BytesIO()

    class Out:
        buffer = buf

    old = sys.stdout
    sys.stdout = Out()
    if designated:
        tool.designate_live(designated)
    else:
        tool.clear_designation()
    try:
        code = tool.main(args)
    finally:
        sys.stdout = old
        tool.clear_fault()
        tool.clear_designation()
    raw = buf.getvalue()
    body = record([str(TOOL_FILE), *args], code, raw, b"", designated is not None)
    if code not in (0, 1, 2, 3) or (code != 0 and not body):
        fail(f"unreadable command {args[0]} exit {code}")
    return code, body, raw


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


def counts(audit: dict) -> dict:
    records = audit["records"]
    return {
        "incomplete_count": sum(1 for record in records if record.get("verify_exit") != 0),
        "page_local_count": sum(1 for record in records if record.get("route") == "page-local-colab"),
        "record_count": len(records),
    }


def displaced_names(audit: dict) -> set[str]:
    """Names publish moves into occupants/.

    Pass02 scans lines.occupants(book, route target_number, route target_page).
    The target number is the line a directory currently occupies. It is not
    the record's own audit target_line. 0102.prime-support-0501 is displaced
    by 0118.workflow-start-0501, whose route number is 0102, even though
    0102's own logical home is 0107.prime-support.
    """
    names = [record["old_member"] for record in audit["records"]]
    found: set[str] = set()
    for record in audit["records"]:
        origin = record["origin"]
        route = LINES.route_for(origin["book"], origin["page"], origin["batch"])
        prefix = route["target_number"] + "."
        page = route["target_page"]
        for name in names:
            if name != page and name.startswith(prefix):
                found.add(name)
    return found


def write_pair(root: Path, plan: Path) -> None:
    audit_raw = AUDIT_PATH.read_bytes()
    plan_raw = plan.read_bytes()
    release = {
        "audit_bytes": len(audit_raw),
        "audit_sha256": sha(audit_raw),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(root / "book"),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(OPS),
        "plan_bytes": len(plan_raw),
        "plan_sha256": sha(plan_raw),
        "release_text": TEST_TEXT,
        "retired_root": str(root / "retired"),
        "schema": "return-line-director-release/1",
        "staging_root": str(root / "staging"),
    }
    raw = dump(release)
    (root / "release.json").write_bytes(raw)
    auth = {key: release[key] for key in (
        "audit_bytes", "audit_sha256", "backup_root", "book", "book_path", "executor",
        "layout_sha256", "operations", "plan_bytes", "plan_sha256", "retired_root", "staging_root",
    )}
    auth.update({
        "release_bytes": len(raw),
        "release_path": str(root / "release.json"),
        "release_sha256": sha(raw),
        "schema": "return-line-recorded-release/1",
        "synthetic": False,
    })
    (root / "auth.json").write_bytes(dump(auth))


def auth_args(root: Path, plan: Path) -> list[str]:
    return [
        "--authorization", str(root / "auth.json"),
        "--audit", str(AUDIT_PATH),
        "--plan", str(plan),
        "--backup", str(root / "backup"),
        "--staging", str(root / "staging"),
        "--retired", str(root / "retired"),
    ]


def through_retire(root: Path, audit: dict) -> dict:
    book = root / "book"
    plan = root / "plan.json"
    code, body, _raw = cli(["plan", "--book", str(book), "--audit", str(AUDIT_PATH), "--out", str(plan)])
    expect(code, body, 0, "plan")
    write_pair(root, plan)
    code, body, _raw = cli(["preflight", "--book", str(book), *auth_args(root, plan)], str(book))
    expect(code, body, 0, "preflight")
    if body.get("detail", {}).get("mutated") is not False or (book / "return-line-layout.json").exists():
        fail("preflight wrote or claimed a mutation")
    code, body, _raw = cli(["init", "--book", str(book), "--name", "00.00.10.work", *auth_args(root, plan)])
    expect(code, body, 2, "init without designation")
    if body.get("check") != "return-line-recorded-release/1":
        fail(f"undesignated init check {body.get('check')}")
    derived = counts(audit)
    code, body, _raw = cli(["init", "--book", str(book), "--name", "00.00.10.work", *auth_args(root, plan)], str(book))
    expect(code, body, 0, "init")
    code, body, _raw = cli(["stage", "--book", str(book), *auth_args(root, plan)], str(book))
    expect(code, body, 0, "stage")
    for command in ("reconstruct", "publish"):
        code, body, _raw = cli([command, "--book", str(book), *auth_args(root, plan)], str(book))
        expect(code, body, 0, command)
        detail = body.get("detail") or {}
        for key, value in derived.items():
            if detail.get(key) != value:
                fail(f"{command} {key} {detail.get(key)} derived {value}")
        if detail.get("accepted") is not False or detail.get("published") is not False:
            fail(f"{command} claimed acceptance")
    code, body, _raw = cli(["retire", "--book", str(book), *auth_args(root, plan)], str(book))
    expect(code, body, 0, "retire")
    detail = body.get("detail") or {}
    if detail.get("record_count") != derived["record_count"] or detail.get("remaining_old_members") != 0:
        fail(f"retire counts {detail}")
    return {"plan_sha256": sha(plan.read_bytes()), "plan_bytes": plan.stat().st_size, "retire": body}


def assert_retired(root: Path, audit: dict) -> dict:
    book = root / "book"
    displaced = displaced_names(audit)
    originals = 0
    occupants = 0
    for record in audit["records"]:
        name = record["old_member"]
        if (book / name).exists():
            fail(f"old member still present {name}")
        side = "occupants" if name in displaced else "originals"
        other = "originals" if side == "occupants" else "occupants"
        if (root / "retired" / other / name).exists():
            fail(f"{name} is on both sides")
        if not (root / "retired" / side / name).is_dir():
            fail(f"missing {side} {name}")
        if side == "occupants":
            occupants += 1
        else:
            originals += 1
    if (book / "0110.colab-tools" / "05.01.return.md").exists():
        fail("invented 0154 return")
    if not (root / "retired" / "originals" / "0101.app-entry-0506").is_dir():
        fail("0101 is not under originals")
    if not (root / "retired" / "occupants" / "0104.app-entry-0508").is_dir():
        fail("0104 is not under occupants")
    print("retired originals", originals, "occupants", occupants)
    return {
        "displaced": displaced,
        "occupants": occupants,
        "old_members_left": 0,
        "originals": originals,
    }


def assert_retained(body: dict, member: str, displaced: set[str], audit: dict) -> None:
    record = next(item for item in audit["records"] if item["old_member"] == member)
    described = body.get("descriptor") or {}
    if set(described) != set(LINES.DESCRIPTOR_KEYS):
        fail(f"lookup {member} descriptor keys")
    if described.get("verification", {}).get("tool_path") != "labs/return-lines-pass01/return_lines.py":
        fail(f"lookup {member} did not delegate to pass01")
    if record.get("verify_exit") != 0:
        if described.get("state") != "incomplete":
            fail(f"lookup {member} state {described.get('state')}")
        if described.get("return_sha256") is not None or described.get("return_bytes") is not None:
            fail(f"lookup {member} invented a return hash")
    else:
        if described.get("state") != "complete":
            fail(f"lookup {member} state {described.get('state')}")
        if described.get("custody_format") != "legacy-relocated/1":
            fail(f"lookup {member} custody format")
    retained = (body.get("detail") or {}).get("retained_original") or {}
    side = "occupants" if member in displaced else "originals"
    if retained.get("retired_rel") != f"{side}/{member}" or retained.get("book_member_present") is not False:
        fail(f"lookup {member} retained {retained.get('retired_rel')}")
    home = (body.get("detail") or {}).get("new_home") or {}
    if home.get("logical_return_path") != record["target_return"] or home.get("target_page") != record["target_page"]:
        fail(f"lookup {member} new home {home}")


def lookup(book: Path, member: str) -> tuple[dict, bytes]:
    code, body, raw = cli(["lookup", "--book", str(book), "--member", member])
    return {"code": code, "body": body}, raw


def file_one(root: Path, plan: Path, page: str, batch: str, submission: str, target: str) -> None:
    folder = root / "filings" / submission
    folder.mkdir(parents=True)
    return_file = folder / "return.md"
    note = folder / "note.txt"
    text = (
        f"# SYNTHETIC fixture filing\n\nsubmission: {submission}\npage: {page}\nbatch: {batch}\n\n"
        "This is not custody, acceptance, or a Prime receipt.\n"
    )
    return_file.write_bytes(text.encode("utf-8"))
    note.write_bytes(f"SYNTHETIC note {submission}\n".encode("utf-8"))
    book = str(root / "book")
    common = ["--book", book, "--page", page, "--batch", batch, "--submission", submission, *auth_args(root, plan)]
    code, body, _raw = cli([
        "reserve", *common, "--output", "note.txt", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "synthetic fixture filing",
    ], book)
    expect(code, body, 1, f"reserve {submission}")
    code, body, _raw = cli([
        "capture", *common, "--return-file", str(return_file), "--artifact", "note.txt", str(note),
    ], book)
    expect(code, body, 0, f"capture {submission}")
    if (body.get("detail") or {}).get("accepted") is not False:
        fail(f"capture {submission} accepted")
    logical = root / "book" / target / f"{batch}.return.md"
    if logical.read_bytes() != return_file.read_bytes():
        fail(f"filed return bytes {submission}")


def filings(root: Path) -> None:
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
    first = book / "0121.synthetic-filing" / "05.01.return.md"
    second = book / "0121.synthetic-filing" / "05.02.return.md"
    if not first.is_file() or not second.is_file() or first.read_bytes() == second.read_bytes():
        fail("0121 did not keep two distinct passes")


def run_reader(book: Path, member: str) -> dict:
    proc = subprocess.run(
        [sys.executable, "-B", str(READER), "verify", "--book", str(book), "--member", member],
        cwd=str(REPO), capture_output=True, env=ENV,
    )
    body = record(
        [str(READER), "verify", "--book", str(book), "--member", member],
        proc.returncode, proc.stdout, proc.stderr, False,
    )
    text = proc.stdout.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    return {
        "book": str(book),
        "exit": proc.returncode,
        "member": member,
        "not_approved": "not approved" in text and "not accepted" in text and "not published" in text,
        "stderr_bytes": len(proc.stderr),
        "stdout": text[:240],
    }


def readers(root: Path) -> dict:
    book = root / "book"
    retired = root / "retired"
    rows = [
        run_reader(retired, "0101.app-entry-0506"),
        run_reader(retired, "0104.app-entry-0508"),
        run_reader(retired / "originals", "0101.app-entry-0506"),
        run_reader(retired / "originals", "0104.app-entry-0508"),
        run_reader(retired / "occupants", "0101.app-entry-0506"),
        run_reader(retired / "occupants", "0104.app-entry-0508"),
        run_reader(book, "0121.synthetic-filing"),
    ]
    by_book: dict[str, set[str]] = {}
    for row in rows:
        if row["exit"] == 0:
            by_book.setdefault(row["book"], set()).add(row["member"])
    for members in by_book.values():
        if "0101.app-entry-0506" in members and "0104.app-entry-0508" in members:
            fail("one reader book verified both archive sides")
    found = {(row["book"], row["member"]): row for row in rows}

    def one(path: Path, member: str) -> dict:
        return found[(str(path), member)]

    original = one(retired / "originals", "0101.app-entry-0506")
    occupant = one(retired / "occupants", "0104.app-entry-0508")
    if original["exit"] != 0 or not original["not_approved"]:
        fail(f"originals reader {original['exit']}")
    if occupant["exit"] != 0 or not occupant["not_approved"]:
        fail(f"occupants reader {occupant['exit']}")
    if one(retired, "0101.app-entry-0506")["exit"] == 0 or one(retired, "0104.app-entry-0508")["exit"] == 0:
        fail("retired root verified a nested member")
    if one(retired / "originals", "0104.app-entry-0508")["exit"] == 0:
        fail("originals verified an occupant")
    if one(retired / "occupants", "0101.app-entry-0506")["exit"] == 0:
        fail("occupants verified an original")
    synthetic = one(book, "0121.synthetic-filing")
    if synthetic["exit"] == 0 or "unexpected 05.01.custody" not in synthetic["stdout"]:
        fail(f"synthetic reader gap changed {synthetic['exit']} {synthetic['stdout']}")
    return {
        "logical_page_verifies": False,
        "occupants_member_exit": occupant["exit"],
        "originals_member_exit": original["exit"],
        "rows": rows,
        "single_book_archive": False,
        "synthetic_gap": "unexpected 05.01.custody",
    }


def seam(primary: Path) -> dict:
    copy = primary.parent / "seam-book"
    if copy.exists():
        fail("seam book already exists")
    copy_tree(primary / "book", copy)
    evidence = primary.parent / "seam-evidence"
    proc = subprocess.run(
        [sys.executable, "-B", str(SEAM), "--book", str(copy), "--evidence", str(evidence), "--lookups", str(primary / "lookups")],
        cwd=str(REPO), capture_output=True, env=ENV, timeout=600,
    )
    record([str(SEAM), "--book", str(copy), "--evidence", str(evidence), "--lookups", str(primary / "lookups")], proc.returncode, proc.stdout, proc.stderr, False)
    print("seam exit", proc.returncode)
    if proc.returncode != 0:
        fail(proc.stderr.decode("utf-8", "replace")[-500:])
    report = json.loads((evidence / "seam.json").read_bytes())
    rows = report.get("rows") or []
    if len(rows) != 2:
        fail(f"seam rows {len(rows)}")
    saved = []
    for row in rows:
        obs = row.get("observation") or {}
        if row.get("exit") != 0 or obs.get("state") != "complete" or obs.get("custody_verified") is not True:
            fail(f"seam case {row.get('label')} {obs}")
        if obs.get("task_association") != "not-established":
            fail(f"seam task association {obs.get('task_association')}")
        saved.append({"exit": row["exit"], "label": row["label"], "pass_state": row["pass_state"], "task_association": obs["task_association"]})
    return {"rows": saved}


def live_proposal(audit: dict) -> dict:
    for path in PROPOSED.values():
        if path.exists():
            fail(f"proposed path already exists {path}")
    plan = EVIDENCE / "live-plan.json"
    code, body, raw = cli(["plan", "--book", str(LIVE), "--audit", str(AUDIT_PATH), "--out", str(plan)])
    expect(code, body, 0, "live plan")
    if (LIVE / "return-line-layout.json").exists():
        fail("live plan wrote a layout")
    planned = json.loads(plan.read_bytes())
    if planned.get("live_moves") is not False or planned.get("live_apply") is not False:
        fail("live plan flags")
    raw_plan = plan.read_bytes()
    raw_audit = AUDIT_PATH.read_bytes()
    candidate = {
        "active": False,
        "audit_bytes": len(raw_audit),
        "audit_sha256": sha(raw_audit),
        "backup_root": str(PROPOSED["backup"]),
        "book": "00.00.10.work",
        "book_path": str(LIVE),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(OPS),
        "plan_bytes": len(raw_plan),
        "plan_sha256": sha(raw_plan),
        "release_text": "CANDIDATE only. The Director has not released execution of this plan.\n",
        "retired_root": str(PROPOSED["retired"]),
        "schema": "return-line-release-candidate/1",
        "staging_root": str(PROPOSED["staging"]),
        "unresolved": [
            "Director has not approved the staging, backup, or retirement paths.",
            "This invocation is not an execution release, and Prime has not recorded one.",
            "The executing identity is not recorded for a live cutover.",
            "0154.colab-support-first-0501 stays incomplete. No return is invented.",
            "Pending captures 0121 through 0126 have no receipt and no task association.",
            "Retained bytes are split across occupants and originals. The historical reader has no adapter.",
            "Old sequential reserve closure is not built. The allocation-lock sentinel is not adopted.",
        ],
    }
    candidate_path = EVIDENCE / "release-candidate.json"
    candidate_path.write_bytes(dump(candidate))
    code, body, raw = cli([
        "preflight", "--book", str(LIVE), "--authorization", str(candidate_path),
        "--audit", str(AUDIT_PATH), "--plan", str(plan),
        "--backup", str(PROPOSED["backup"]), "--staging", str(PROPOSED["staging"]), "--retired", str(PROPOSED["retired"]),
    ])
    (EVIDENCE / "preflight.json").write_bytes(raw)
    expect(code, body, 2, "live candidate preflight")
    if body.get("check") != "return-line-release-candidate/1" or "candidate is not authority" not in body.get("correction", ""):
        fail(f"candidate preflight {body.get('check')}")
    if (LIVE / "return-line-layout.json").exists():
        fail("preflight wrote a live layout")
    for path in PROPOSED.values():
        if path.exists():
            fail(f"preflight created {path}")
    return {
        "candidate_bytes": candidate_path.stat().st_size,
        "candidate_sha256": sha(candidate_path.read_bytes()),
        "change_count": (body.get("detail") or {}).get("source_mismatch_count"),
        "plan_bytes": len(raw_plan),
        "plan_sha256": sha(raw_plan),
        "preflight_check": body.get("check"),
        "preflight_exit": code,
        "source_files_checked": (body.get("detail") or {}).get("source_files_checked"),
        "source_mismatch_count": (body.get("detail") or {}).get("source_mismatch_count"),
    }


def main() -> None:
    pins_ok()
    for path in PROPOSED.values():
        if path.exists():
            fail(f"proposed path already exists {path}")
    live_layout = LIVE / "return-line-layout.json"
    if live_layout.exists():
        fail("live layout already exists")
    pass01_before = PASS01.read_bytes()
    pass02_before = PASS02.read_bytes()
    audit = json.loads(AUDIT_PATH.read_bytes())
    before = fingerprint(audit)
    print("live fingerprint", before)
    unit = subprocess.run([sys.executable, "-B", str(UNIT)], cwd=str(REPO), capture_output=True, env=ENV)
    (EVIDENCE / "unit-stdout.txt").write_bytes(unit.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    (EVIDENCE / "unit-stderr.txt").write_bytes(unit.stderr.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    print("unit exit", unit.returncode)
    if unit.returncode != 0:
        fail("unit tests")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = EXTERNAL / f"{stamp}-suite"
    primary = root / "primary"
    make_book(primary, audit)
    primary_result = through_retire(primary, audit)
    retired = assert_retired(primary, audit)
    (primary / "lookups").mkdir()
    found, raw = lookup(primary / "book", "0101.app-entry-0506")
    expect(found["code"], found["body"], 0, "lookup 0101")
    assert_retained(found["body"], "0101.app-entry-0506", retired["displaced"], audit)
    (primary / "lookups" / "lookup-0101.json").write_bytes(raw)
    for member, wanted in (
        ("0104.app-entry-0508", 0),
        ("0121.archive-resolution-0508", 0),
        ("0154.colab-support-first-0501", 1),
        ("0165.bench-method-colab-0501", 0),
    ):
        looked, _raw = lookup(primary / "book", member)
        expect(looked["code"], looked["body"], wanted, f"lookup {member}")
        assert_retained(looked["body"], member, retired["displaced"], audit)
    filings(primary)
    code, body, raw = cli(["descriptor", "--book", str(primary / "book"), "--page", "0521.synthetic-filing", "--batch", "05.01"])
    expect(code, body, 0, "descriptor synthetic")
    (primary / "lookups" / "synthetic-descriptor.json").write_bytes(raw)
    reader_report = readers(primary)
    seam_report = seam(primary)
    proposal = live_proposal(audit)
    after = fingerprint(audit)
    if after != before or PASS01.read_bytes() != pass01_before or PASS02.read_bytes() != pass02_before:
        fail("live bytes, pass01, or pass02 changed")
    if live_layout.exists():
        fail("live layout written")
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
        "measured_retirement": {key: value for key, value in retired.items() if key != "displaced"},
        "pass01_unchanged": True,
        "pass02_unchanged": True,
        "plan_bytes": primary_result["plan_bytes"],
        "plan_sha256": primary_result["plan_sha256"],
        "prior_plan_required": False,
        "prior_plan_sha256": PRIOR_PLAN,
        "proposal": proposal,
        "published": False,
        "reader": reader_report,
        "receipt": None,
        "release_text": TEST_TEXT,
        "retired_root": str(primary / "retired"),
        "schema": "return-line-pass03-suite/1",
        "seam": seam_report,
        "sentinel_installed": False,
        "unit_exit": unit.returncode,
        "work_root": str(root),
    }
    (root / "suite-report.json").write_bytes(dump(report))
    (root / "commands.json").write_bytes(dump({"commands": LOG, "schema": "return-line-pass03-commands/1"}))
    (EVIDENCE / "suite-report.json").write_bytes(dump(report))
    (EVIDENCE / "commands.json").write_bytes(dump({"commands": LOG, "schema": "return-line-pass03-commands/1"}))
    print("OK", root)
    print("copy plan", primary_result["plan_sha256"])
    print("live plan", proposal["plan_sha256"], proposal["plan_bytes"])
    print("counts", counts(audit))
    print("retired", retired)
    print("preflight", proposal["preflight_exit"], proposal["preflight_check"], "mismatches", proposal["source_mismatch_count"])


if __name__ == "__main__":
    main()
