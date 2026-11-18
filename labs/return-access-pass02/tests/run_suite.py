#!/usr/bin/env python3
"""Combined copied-book proof for the 05.09 successors.

Roots stay under D:\\librarian\\temp\\0521-0509\\. This file does not delete
a root, does not write a live layout, and does not select the app.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIVE = REPO / "00.kernel" / "00.00.10.work"
AUDIT_PATH = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
EVIDENCE = LIVE / "0521.return-placement" / "evidence" / "build05.09"
FACADE = REPO / "app" / "return_line_tools_v3.py"
HANDOFF_FACADE = REPO / "app" / "handoff_tools_v2.py"
GUARD = REPO / "labs" / "return-capture-guard-pass01" / "return_capture_guard.py"
WRITER = REPO / "labs" / "return-capture-pass01" / "return_capture.py"
READER = WRITER
ACCESS = REPO / "labs" / "return-access-pass02" / "return_access.py"
NEW_HANDOFF = REPO / "labs" / "capture-handoff-guard-pass01" / "handoff.py"
CLERK = REPO / "labs" / "clerk-handoff-pass02" / "clerk.py"
SNAPSHOT = (
    LIVE / "0522.review-construction" / "evidence" / "pack05.11" / "sources" / "app" / "librarian.py"
)
PRIOR_PLAN = "52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66"
PROPOSED = {
    "backup": Path(r"D:\librarian\return-placement\0521-backup"),
    "retired": Path(r"D:\Git\lib-build\00.archive\0521.return-lines"),
    "staging": Path(r"D:\librarian\return-placement\0521-staging"),
}
ENV = dict(os.environ)
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
PINS = {
    "pass04": ("labs/return-lines-pass04/return_lines.py", "708443c5b3af457f930e8751be4224234d1494f2a2b4e18e3cf08bd7a7af1df6", 12124),
    "pass03": ("labs/return-lines-pass03/return_lines.py", "78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63", 33349),
    "pass02": ("labs/return-lines-pass02/return_lines.py", "6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908", 82908),
    "pass01": ("labs/return-lines-pass01/return_lines.py", "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "guard": ("labs/return-capture-guard-pass01/return_capture_guard.py", "ca2707845a033901053620c70512a0a6a5ebf52d1b3069704aae8a93e17c7b2a", 8931),
    "handoff": ("labs/capture-handoff-pass01/handoff.py", "a8380136a84469b8975b38f084a4d34802ccf079ed69cf85d107f6ca3643426a", 51828),
    "access01": ("labs/return-access-pass01/return_access.py", "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5", 26561),
}
sys.path.insert(0, str(REPO / "labs" / "return-lines-pass04"))
import return_lines as pass04  # noqa: E402

LINES = pass04.load_pass03().load_pass02().load_lines()
RELEASE_TEXT = pass04.load_pass03().load_pass02().RELEASE_TEXT
LOG: list[dict] = []
CLAIMS: list[dict] = []
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
ROOT = Path(r"D:\librarian\temp\0521-0509") / f"{STAMP}-suite"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonical(value: dict) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return (text + "\n").encode("utf-8")


def fail(message: str) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "first-failure.txt").write_bytes((message + "\n").encode("utf-8"))
    (ROOT / "first-failure.txt").write_bytes((message + "\n").encode("utf-8"))
    (EVIDENCE / "commands.json").write_bytes(dump({"commands": LOG, "schema": "return-access-handoff-commands/0509"}))
    (EVIDENCE / "claims.json").write_bytes(dump({"claims": CLAIMS, "schema": "return-access-handoff-claims/0509"}))
    print("FAIL", message)
    raise SystemExit(1)


def claim(name: str, case: str, run: str, outcome: str, limit: str, kind: str) -> None:
    CLAIMS.append({
        "case": case,
        "claim": name,
        "kind": kind,
        "limit": limit,
        "outcome": outcome,
        "run": run,
    })


def run(script: Path, args: list[str]) -> tuple[int, bytes, bytes]:
    proc = subprocess.run(
        [str(PY), "-B", str(script), *args],
        cwd=str(REPO),
        env=ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    LOG.append({
        "argv0": script.name,
        "command": args[0] if args else "",
        "exit": proc.returncode,
        "stderr_bytes": len(proc.stderr),
        "stdout_bytes": len(proc.stdout),
        "stdout_sha256": sha(proc.stdout),
    })
    print(script.name, args[0] if args else "", proc.returncode)
    return proc.returncode, proc.stdout, proc.stderr


def parse_out(raw: bytes) -> dict:
    text = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if not text.strip():
        return {}
    try:
        body = json.loads(text.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return body if isinstance(body, dict) else {}


def cli(args: list[str]) -> tuple[int, dict, str]:
    code, out, err = run(FACADE, args)
    err_text = err.decode("utf-8", "replace")
    if code not in {0, 1, 2, 3}:
        fail(f"unexpected exit {code} {args[0]} stderr {err_text[:400]}")
    return code, parse_out(out), err_text


def expect(code: int, body: dict, wanted: int, label: str) -> None:
    if code != wanted:
        fail(f"{label} exit {code} check {body.get('check')} correction {str(body.get('correction'))[:500]}")


def layout_sha() -> str:
    return LINES.sha(LINES.dump(LINES.layout_body("00.00.10.work")))


def layout_bytes(name: str) -> bytes:
    return LINES.dump(LINES.layout_body(name))


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


def write_fixture(root: Path, book: Path, plan: Path, audit: Path, operations: list[str] | None = None) -> None:
    raw = audit.read_bytes()
    body = {
        "audit_bytes": len(raw),
        "audit_sha256": sha(raw),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": layout_sha(),
        "operations": list(operations or OPS),
        "plan_sha256": sha(plan.read_bytes()),
        "release": RELEASE_TEXT,
        "retired_root": str(root / "retired"),
        "schema": "return-line-authorization/1",
        "staging_root": str(root / "staging"),
        "synthetic": True,
    }
    if str(book) == str(LIVE) or body["book_path"] == str(LIVE):
        fail("refusing to write fixture authority for the live book")
    (root / "auth.json").write_bytes(dump(body))


def auth_args(root: Path, plan: Path, audit: Path) -> list[str]:
    return [
        "--authorization", str(root / "auth.json"),
        "--audit", str(audit),
        "--plan", str(plan),
        "--backup", str(root / "backup"),
        "--staging", str(root / "staging"),
        "--retired", str(root / "retired"),
    ]


def filtered_audit(members: list[str]) -> dict:
    body = json.loads(AUDIT_PATH.read_bytes())
    wanted = set(members)
    body["records"] = [record for record in body["records"] if record["old_member"] in wanted]
    files = []
    for entry in body["files"]:
        path = entry["path"].replace("\\", "/")
        if any(f"/{name}/" in f"/{path}" for name in wanted):
            files.append(entry)
    body["files"] = files
    return body


def tree_rows(root: Path) -> list[str]:
    rows = []
    if not root.exists():
        return rows
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if not LINES.is_reparse(os.path.join(dirpath, name))]
        for name in filenames:
            path = Path(dirpath) / name
            if LINES.is_reparse(str(path)):
                continue
            data = path.read_bytes()
            rows.append(f"{path.relative_to(root).as_posix()} {len(data)} {sha(data)}")
    rows.sort()
    return rows


def tree_sha(root: Path) -> str:
    return sha(("\n".join(tree_rows(root)) + "\n").encode("utf-8"))


def fingerprint(audit: dict) -> str:
    rows = []
    paths = [REPO / entry["path"].replace("\\", "/") for entry in audit["files"]]
    paths.append(LIVE / "0100.band.returns" / "01.md")
    for path in paths:
        data = path.read_bytes()
        rows.append({"bytes": len(data), "path": path.relative_to(REPO).as_posix(), "sha256": sha(data)})
    rows.sort(key=lambda row: row["path"])
    return sha(dump(rows))


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    fail(f"missing {prefix!r}")
    return ""


def migrate(root: Path, audit: dict, audit_path: Path) -> None:
    book = root / "book"
    plan = root / "plan.json"
    code, body, _err = cli(["plan", "--book", str(book), "--audit", str(audit_path), "--out", str(plan)])
    expect(code, body, 0, f"{root.name} plan")
    if (book / "return-line-layout.json").exists():
        fail(f"{root.name} plan wrote a layout")
    missing = root / "missing-authorization.json"
    code, body, _err = cli(["preflight", "--book", str(book), "--authorization", str(missing), *auth_args(root, plan, audit_path)[2:]])
    expect(code, body, 2, f"{root.name} missing preflight")
    if body.get("check") != "authorization" or "authorization is absent" not in str(body.get("correction")):
        fail(f"{root.name} missing preflight check {body.get('check')}")
    if (book / "return-line-layout.json").exists():
        fail(f"{root.name} missing preflight wrote a layout")
    claim("missing release refuses and writes nothing", f"{root.name} preflight", "ran", "passed", "fixture file was absent", "author")
    write_fixture(root, book, plan, audit_path, ["stage"])
    code, body, _err = cli(["init", "--book", str(book), "--name", "00.00.10.work", *auth_args(root, plan, audit_path)])
    expect(code, body, 2, f"{root.name} wrong operation")
    if "not authorized" not in str(body.get("correction")):
        fail(f"{root.name} wrong operation reason")
    if (book / "return-line-layout.json").exists():
        fail(f"{root.name} wrong operation wrote a layout")
    claim("operations list that omits init refuses init", f"{root.name} init", "ran", "passed", "synthetic fixture, copy evidence", "author")
    write_fixture(root, book, plan, audit_path)
    code, body, _err = cli(["preflight", "--book", str(book), *auth_args(root, plan, audit_path)])
    expect(code, body, 0, f"{root.name} preflight")
    detail = body.get("detail") or {}
    if detail.get("mutated") is not False or detail.get("executed") is not False or detail.get("canonical") is not False:
        fail(f"{root.name} preflight claimed execution")
    if (book / "return-line-layout.json").exists():
        fail(f"{root.name} preflight wrote a layout")
    claim("fixture preflight is readiness only", f"{root.name} preflight", "ran", "passed", "synthetic true, not a Director release", "reproduced")
    for command in ("init", "stage", "reconstruct", "publish", "retire"):
        args = [command, "--book", str(book), *auth_args(root, plan, audit_path)]
        if command == "init":
            args = ["init", "--book", str(book), "--name", "00.00.10.work", *auth_args(root, plan, audit_path)]
        code, body, _err = cli(args)
        expect(code, body, 0, f"{root.name} {command}")
        if command in {"reconstruct", "publish"}:
            found = body.get("detail") or {}
            for key, value in counts(audit).items():
                if found.get(key) != value:
                    fail(f"{root.name} {command} {key} {found.get(key)} derived {value}")
            if found.get("accepted") is not False:
                fail(f"{root.name} {command} claimed acceptance")
    detail = body.get("detail") or {}
    if detail.get("remaining_old_members") != 0:
        fail(f"{root.name} retire remaining {detail}")
    claim("staged rebuild and retirement through the facade", root.name, "ran", "passed", "fixture authority on a copy", "reproduced")


def assert_retired(root: Path, audit: dict) -> None:
    book = root / "book"
    names = [record["old_member"] for record in audit["records"]]
    displaced: set[str] = set()
    for record in audit["records"]:
        origin = record["origin"]
        route = LINES.route_for(origin["book"], origin["page"], origin["batch"])
        prefix = route["target_number"] + "."
        page = route["target_page"]
        for name in names:
            if name != page and name.startswith(prefix):
                displaced.add(name)
    originals = occupants = 0
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
    if originals + occupants != len(audit["records"]):
        fail("retirement sides do not cover the audit")
    if (book / "0110.colab-tools" / "05.01.return.md").exists():
        fail("invented 0154 return")
    print("retired originals", originals, "occupants", occupants)


def file_one(root: Path, plan: Path, audit_path: Path, page: str, batch: str, submission: str, target: str) -> None:
    text = f"SYNTHETIC return {submission}\n"
    return_file = root / f"{submission}.return.md"
    note = root / f"{submission}.note.txt"
    return_file.write_bytes(text.encode("utf-8"))
    note.write_bytes(f"SYNTHETIC note {submission}\n".encode("utf-8"))
    book = str(root / "book")
    common = ["--book", book, "--page", page, "--batch", batch, "--submission", submission, *auth_args(root, plan, audit_path)]
    code, body, _err = cli([
        "reserve", *common, "--output", "note.txt", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "synthetic fixture filing",
    ])
    expect(code, body, 1, f"reserve {submission}")
    code, body, _err = cli(["capture", *common, "--return-file", str(return_file), "--artifact", "note.txt", str(note)])
    expect(code, body, 0, f"capture {submission}")
    if (body.get("detail") or {}).get("accepted") is not False:
        fail(f"capture {submission} accepted")
    logical = root / "book" / target / f"{batch}.return.md"
    if logical.read_bytes() != return_file.read_bytes():
        fail(f"filed return bytes {submission}")


def filings(root: Path, audit_path: Path) -> None:
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
        file_one(root, plan, audit_path, page, batch, submission, target)
    book = root / "book"
    first = book / "0121.synthetic-filing" / "05.01.return.md"
    second = book / "0121.synthetic-filing" / "05.02.return.md"
    if first.read_bytes() == second.read_bytes():
        fail("0121 did not keep two distinct passes")
    local = book / "0721.synthetic-local" / "05.01.return.md"
    if not local.is_file() or (book / "0121.synthetic-local").exists():
        fail("N7NN local return was retargeted")
    sealed = first.read_bytes()
    common = [
        "--book", str(book), "--page", "0521.synthetic-filing", "--batch", "05.01",
        *auth_args(root, plan, audit_path),
    ]
    code, body, _err = cli([
        "reserve", *common, "--submission", "synthetic-0521-conflict", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "conflicting fixture filing",
    ])
    if code == 0 or body.get("state") != "conflict" or first.read_bytes() != sealed:
        fail(f"conflicting submission {code} {body.get('state')}")
    code, body, _err = cli([
        "reserve", *common, "--submission", "synthetic-0521-0501", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "synthetic fixture filing",
    ])
    if (body.get("detail") or {}).get("rewritten") is not False or first.read_bytes() != sealed:
        fail("repeated submission rewrote the sealed pass")
    changed = root / "changed-payload.return.md"
    changed.write_bytes(b"CHANGED payload\n")
    code, body, _err = cli([
        "capture", *common, "--submission", "synthetic-0521-0501", "--return-file", str(changed),
        "--artifact", "note.txt", str(root / "synthetic-0521-0501.note.txt"),
    ])
    if code != 2 or body.get("state") != "conflict" or first.read_bytes() != sealed:
        fail(f"changed payload {code} {body.get('state')}")
    claim("repeated and conflicting submissions keep the sealed pass", "0121 05.01", "ran", "passed", "author case on the marked copy", "author")
    claim("changed payload does not replace a sealed return", "0121 05.01 capture", "ran", "passed", "author case on the marked copy", "author")


def readers(root: Path) -> None:
    book = root / "book"
    retired = root / "retired"
    rows = [
        ("originals", retired / "originals", "0101.app-entry-0506", 0),
        ("occupants", retired / "occupants", "0104.app-entry-0508", 0),
        ("retired-root", retired, "0101.app-entry-0506", None),
        ("cross-originals", retired / "originals", "0104.app-entry-0508", None),
        ("cross-occupants", retired / "occupants", "0101.app-entry-0506", None),
        ("synthetic", book, "0121.synthetic-filing", None),
    ]
    seen: dict[str, set[str]] = {}
    for _label, parent, member, _wanted in rows:
        code, out, _err = run(READER, ["verify", "--book", str(parent), "--member", member])
        text = out.decode("utf-8", "replace")
        if code == 0:
            seen.setdefault(str(parent), set()).add(member)
        if _label == "originals" and (code != 0 or "not approved" not in text):
            fail(f"originals reader {code}")
        if _label == "occupants" and (code != 0 or "not approved" not in text):
            fail(f"occupants reader {code}")
        if _label == "retired-root" and code == 0:
            fail("retired root verified a nested member")
        if _label.startswith("cross") and code == 0:
            fail(f"{_label} verified the other side")
        if _label == "synthetic" and (code == 0 or "unexpected 05.01.custody" not in text):
            fail(f"synthetic reader gap {code} {text[:180]}")
    for members in seen.values():
        if "0101.app-entry-0506" in members and "0104.app-entry-0508" in members:
            fail("one reader book verified both archive sides")
    claim("historical reads keep originals, occupants, and the synthetic gap", "marked copy", "ran", "passed", "reader result is not approval", "reproduced")


def lookups(book: Path) -> None:
    for member, wanted in (
        ("0101.app-entry-0506", 0),
        ("0104.app-entry-0508", 0),
        ("0154.colab-support-first-0501", 1),
    ):
        code, body, _err = cli(["lookup", "--book", str(book), "--member", member])
        expect(code, body, wanted, f"lookup {member}")
        if body.get("task_association") != "not-established":
            fail(f"lookup {member} task association")
        if body.get("approved") is not False or body.get("accepted") is not False:
            fail(f"lookup {member} claimed approval")
    claim("historical lookup keeps complete members and incomplete 0154", "marked copy", "ran", "passed", "0154 stays incomplete; a reader result is not approval", "reproduced")


def verify_filing(book: Path) -> None:
    code, body, _err = cli([
        "verify", "--book", str(book), "--source", "0521.synthetic-filing", "--pass", "05.01",
    ])
    expect(code, body, 0, "verify synthetic")
    if body.get("task_association") != "not-established":
        fail("verify established task association")
    claim("source/pass verify of a new filing stays unassociated", "0121 05.01", "ran", "passed", "verify follows the filing", "reproduced")


def changed_evidence(root: Path) -> None:
    target = root / "book" / "0121.synthetic-filing" / "05.02.return.md"
    sealed = target.read_bytes()
    target.write_bytes(sealed[:-1] + bytes([sealed[-1] ^ 1]))
    code, body, _err = cli([
        "verify", "--book", str(root / "book"), "--source", "0521.synthetic-filing", "--pass", "05.02",
    ])
    if code == 0 or target.read_bytes() == sealed:
        fail(f"changed evidence verify {code}")
    if target.read_bytes()[: len(sealed) - 1] != sealed[:-1]:
        fail("verify rewrote the changed return")
    target.write_bytes(sealed)
    claim("changed evidence is reported and left in place", "0121 05.02", "ran", "passed", "the suite restored the byte after the observation", "author")


def guard_marked(book: Path) -> None:
    door = (book / "0100.band.returns" / "01.md").read_bytes()
    before = tree_sha(book)
    code, out, err = run(GUARD, [
        "reserve", "--book", str(book), "--submission", "marked-guard", "--name", "marked",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.app-entry",
        "--origin-batch", "05.09", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "marked guard refusal",
    ])
    text = out.decode("utf-8", "replace")
    if err or code != 2 or "writer_started: false" not in text or "result refused" not in text.splitlines():
        fail(f"marked guard reserve {code} {text[:300]}")
    code, out, err = run(GUARD, [
        "capture", "--book", str(book), "--submission", "marked-guard",
        "--return-file", str(book / "missing-return.md"), "--source-root", str(book),
    ])
    text = out.decode("utf-8", "replace")
    if err or code != 2 or "writer_started: false" not in text:
        fail(f"marked guard capture {code} {text[:300]}")
    if tree_sha(book) != before or (book / "0100.band.returns" / "01.md").read_bytes() != door:
        fail("guard changed the marked book")
    claim("guard refuses legacy reserve and capture on the marked copy", "primary book", "ran", "passed", "writer module was not executed", "author")


def side_layout_cases(root: Path) -> None:
    labels = root / "unused-auth-labels"
    flags = []
    for flag, name in (
        ("--authorization", "a.txt"), ("--audit", "b.json"), ("--plan", "c.json"),
        ("--backup", "d"), ("--staging", "e"), ("--retired", "f"),
    ):
        flags.extend((flag, str(labels / name)))
    duplicate = root / "duplicate-layout"
    (duplicate / "0100.band.returns").mkdir(parents=True)
    (duplicate / "0100.band.returns" / "01.md").write_bytes(b"door\n")
    (duplicate / "return-line-layout.json").write_bytes(
        b'{"schema":"return-line-layout/1","schema":"return-line-layout/1"}\n'
    )
    code, _body, err = cli(["reserve", "--book", str(duplicate), "--page", "0509.side", "--batch", "05.01",
                            "--submission", "side-dup", *flags])
    if code != 2 or "layout is not an accepted line-pass declaration" not in err:
        fail(f"duplicate layout facade {code} {err[:240]}")
    if (duplicate / "0121.side").exists() or (duplicate / "0101.side").exists():
        fail("duplicate layout allocated")
    code, out, err = run(GUARD, [
        "reserve", "--book", str(duplicate), "--submission", "side-dup", "--name", "side",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.side", "--origin-batch", "05.01",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "side",
    ])
    text = out.decode("utf-8", "replace")
    if err or code != 2 or "writer_started: false" not in text:
        fail(f"duplicate layout guard {code} {text[:240]}")
    directory = root / "directory-layout"
    (directory / "0100.band.returns").mkdir(parents=True)
    (directory / "return-line-layout.json").mkdir()
    code, _body, err = cli(["capture", "--book", str(directory), *flags])
    if code != 2 or "book is not a declared line-pass book" not in err:
        fail(f"directory layout facade {code} {err[:240]}")
    claim("malformed layouts refuse before launch", "side books", "ran", "passed", "duplicate key and directory; main layout untouched", "author")


def doorless_handoff(base: Path) -> None:
    instructions = base / "instructions"
    instructions.mkdir(parents=True)
    (instructions / "task.txt").write_bytes("fixture task\n".encode("utf-8"))
    store = base / "store"
    book = base / "book"
    book.mkdir()
    source = base / "source"
    source.mkdir()
    report = "final café — report\n".encode("utf-8")
    piece = "piece-body-0509\n".encode("utf-8")
    (source / "final-report.md").write_bytes(report)
    (source / "piece.txt").write_bytes(piece)
    job = {
        "assignee": "fixture-builder",
        "expected_outputs": ["final-report.md", "piece.txt"],
        "instructions": {"path": "task.txt", "sha256": sha((instructions / "task.txt").read_bytes())},
        "job_id": "fixture-0509",
        "release": "fixture job label; not a release",
        "reviewer": "fixture-reviewer",
        "routed_by": "fixture-router",
    }
    job_path = base / "job.json"
    job_path.write_bytes(canonical(job))
    code, out, err = run(CLERK, ["queue", "--store", str(store), "--job", str(job_path), "--instructions-base", str(instructions)])
    if code != 0 or err:
        fail(f"clerk queue {code} {err[:240]!r}")
    code, out, err = run(CLERK, ["claim", "--store", str(store), "--job", "fixture-0509", "--as", "fixture-builder", "--instructions-base", str(instructions)])
    if code != 0 or err:
        fail(f"clerk claim {code} {err[:240]!r}")
    token = field(out.decode("utf-8"), "token ")
    outbox = store / "jobs" / "fixture-0509" / "outbox"
    (outbox / "final-report.md").write_bytes(report)
    (outbox / "piece.txt").write_bytes(piece)
    code, out, err = run(CLERK, [
        "return", "--store", str(store), "--job", "fixture-0509", "--as", "fixture-builder",
        "--claim", token, "--delivery", "fixture-delivery", "--evidence", "transport line only",
    ])
    if code != 0 or err:
        fail(f"clerk return {code} {err[:240]!r}")
    event = field(out.decode("utf-8"), "event 0003.returned.json sha256=")
    code, out, err = run(GUARD, [
        "reserve", "--book", str(book), "--submission", "guard-0509", "--name", "guard-demo",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.app-entry", "--origin-batch", "05.09",
        "--expected-output", "final-report.md", "--expected-output", "piece.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "résumé — not a release",
    ])
    text = out.decode("utf-8")
    if err or code != 0 or "result reserved" not in text.splitlines() or "has not gained line-pass protection" not in text:
        fail(f"undeclared reserve {code} {text[:300]}")
    claim("undeclared doorless reserve keeps legacy behavior and the notice", "doorless book", "ran", "passed", "a marked door cannot show this delegation", "author")
    member = field(text, "member ")
    (book / "return-line-layout.json").write_bytes(layout_bytes("disposable-copy"))
    before = tree_sha(book)
    binding = {
        "artifact_base": str(outbox),
        "artifacts": [
            {"bytes": len(report), "clerk_path": "final-report.md", "logical": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
            {"bytes": len(piece), "clerk_path": "piece.txt", "logical": "piece.txt", "sha256": sha(piece), "source": "piece.txt"},
        ],
        "assignee": "fixture-builder",
        "book": str(book),
        "clerk_store": str(store),
        "failure_log": str(base / "failure.log"),
        "instructions_base": str(instructions),
        "job_id": "fixture-0509",
        "member": member,
        "origin": {"batch": "05.09", "book": "00.00.10.work", "page": "0509.app-entry"},
        "record": str(base / "handoff-record"),
        "report": {"bytes": len(report), "clerk_path": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
        "returned_event_sha256": event,
        "schema": "clerk-capture-handoff/1",
        "source_root": str(source),
        "submission_id": "guard-0509",
        "work_ref": "guard-0509-work-ref",
    }
    binding_path = base / "binding.json"
    binding_path.write_bytes(canonical(binding))
    code, out, err = run(HANDOFF_FACADE, ["--binding", str(binding_path)])
    first = out.decode("utf-8")
    (base / "perform-1.txt").write_bytes(out)
    if err or code == 0 or "result ok" in first.splitlines() or "result attention" not in first.splitlines():
        fail(f"handoff facade {code} {first[:400]} {err[:200]}")
    log_path = base / "failure.log"
    log_bytes = log_path.read_bytes()
    payload = json.loads(log_bytes.decode("utf-8"))
    blob = log_bytes.decode("utf-8")
    if payload.get("schema") != "clerk-capture-handoff-failure/1" or "result refused" not in blob or "writer_started: false" not in blob:
        fail("failure log did not retain the guard refusal")
    if tree_sha(book) != before:
        fail("declared handoff changed the book")
    code, out, err = run(HANDOFF_FACADE, ["--binding", str(binding_path)])
    second = out.decode("utf-8")
    (base / "perform-2.txt").write_bytes(out)
    if err or code == 0 or "result ok" in second.splitlines() or log_path.read_bytes() != log_bytes or "intent is retained" not in second:
        fail("retry replaced the failure log or succeeded")
    claim("old reservation then declared handoff retains the failure", "doorless book", "ran", "passed", "selected facade, not the current app", "author")
    bad = dict(binding)
    bad["artifacts"] = [dict(binding["artifacts"][0]), dict(binding["artifacts"][1])]
    bad["artifacts"][1]["sha256"] = "0" * 64
    bad_path = base / "binding-changed.json"
    bad_path.write_bytes(canonical(bad))
    plain = base / "plain-book"
    plain.mkdir()
    code, out, err = run(GUARD, [
        "reserve", "--book", str(plain), "--submission", "payload-0509", "--name", "payload",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.payload", "--origin-batch", "05.09",
        "--expected-output", "final-report.md", "--expected-output", "piece.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "payload",
    ])
    payload_text = out.decode("utf-8")
    if code != 0:
        fail(f"payload reserve {code} {payload_text[:200]}")
    bad["book"] = str(plain)
    bad["member"] = field(payload_text, "member ")
    bad["submission_id"] = "payload-0509"
    bad["failure_log"] = str(base / "payload-failure.log")
    bad["record"] = str(base / "payload-record")
    bad_path.write_bytes(canonical(bad))
    before_plain = tree_sha(plain)
    code, out, err = run(NEW_HANDOFF, ["perform", "--binding", str(bad_path)])
    text = out.decode("utf-8")
    if code == 0 or "result ok" in text.splitlines() or tree_sha(plain) != before_plain:
        fail(f"changed handoff payload {code} {text[:300]}")
    claim("changed handoff payload does not complete capture", "plain book", "ran", "passed", "identity check happens before a successful capture", "author")


def guard_mismatch(base: Path) -> None:
    base.mkdir(parents=True)
    tampered = base / "tampered-guard.py"
    tampered.write_bytes(b"not-the-guard\n")
    binding = base / "mismatch-binding.json"
    binding.write_bytes(b"{}\n")
    spec = __import__("importlib.util").util.spec_from_file_location("guarded_handoff_0509", NEW_HANDOFF)
    module = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.require_guard(str(tampered))
        fail("require_guard accepted a tampered file")
    except module.GuardMismatch:
        pass
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = module.perform(str(binding), guard_path=str(tampered))
    text = buf.getvalue()
    (base / "mismatch.txt").write_bytes(text.encode("utf-8"))
    sidecar = base / "mismatch-binding.json.guard-mismatch.json"
    if code != 2 or "launched: false" not in text or "writer_started: false" not in text or "result refused" not in text.splitlines():
        fail(f"mismatch stdout {code} {text}")
    if not sidecar.is_file() or json.loads(sidecar.read_bytes())["schema"] != "capture-handoff-guard-mismatch/1":
        fail("mismatch sidecar missing")
    if json.loads(sidecar.read_bytes())["launched"] is not False:
        fail("sidecar claimed a launch")
    claim("guard mismatch refuses before launch", "tampered path", "ran", "passed", "the real guard file was not edited", "author")


def historical_still_runs(root: Path) -> None:
    book = root / "book"
    book.mkdir(parents=True)
    (book / "return-line-layout.json").write_bytes(layout_bytes("doorless-declared"))
    code, out, err = run(WRITER, [
        "reserve", "--book", str(book), "--submission", "old-0509", "--name", "old",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.app-entry",
        "--origin-batch", "05.09", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "historical script",
    ])
    text = out.decode("utf-8")
    if err or code != 0 or "result reserved" not in text.splitlines():
        fail(f"historical writer on a declared copy {code} {text[:240]}")
    marked = root / "marked"
    (marked / "0100.band.returns").mkdir(parents=True)
    shutil.copyfile(LIVE / "0100.band.returns" / "01.md", marked / "0100.band.returns" / "01.md")
    (marked / "return-line-layout.json").write_bytes(layout_bytes("side-marked"))
    code, out, err = run(WRITER, [
        "reserve", "--book", str(marked), "--submission", "marked-old", "--name", "marked-old",
        "--origin-book", "00.00.10.work", "--origin-page", "0509.marked",
        "--origin-batch", "05.09", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "historical marked",
    ])
    text = out.decode("utf-8")
    if code != 0 or "result reserved" not in text.splitlines():
        fail(f"historical writer on a marked side copy {code} {text[:240]} {err[:120]!r}")
    claim("historical writer still reserves when the guard is not selected", "side copies", "ran", "passed", "supported-route closure is not total and not same-user confinement", "author")


def static_callers() -> None:
    for rel in ("labs/capture-handoff-pass01/demo.py", "labs/capture-flow-rehearsal-pass01/rehearse.py"):
        text = (REPO / rel).read_text(encoding="utf-8")
        if "labs/return-capture-pass01/return_capture.py" not in text or "reserve" not in text:
            fail(f"{rel} no longer selects the historical reserve")
    facade = FACADE.read_text(encoding="utf-8")
    if "canonical live book is refused" in facade or "--force" not in facade:
        fail("facade veto or force ban drifted")
    claim("demo and rehearsal still select the old writer", "static read", "ran", "passed", "they were not executed and were not edited", "author")


def recovery(root: Path) -> None:
    root.mkdir(parents=True)
    audit = filtered_audit(["0101.app-entry-0506"])
    audit_path = root / "audit.json"
    audit_path.write_bytes(dump(audit))
    before = (LIVE / "0101.app-entry-0506" / "return.md").read_bytes()
    make_book(root, audit)
    sample = root / "book" / "0101.app-entry-0506" / "return.md"
    sample_before = sample.read_bytes()
    migrate(root, audit, audit_path)
    code, body, _err = cli(["rollback-retire", "--book", str(root / "book"), *auth_args(root, root / "plan.json", audit_path)])
    expect(code, body, 0, "rollback-retire")
    if sample.read_bytes() != sample_before:
        fail("rollback-retire bytes differ")
    code, body, _err = cli(["rollback-publish", "--book", str(root / "book"), *auth_args(root, root / "plan.json", audit_path)])
    expect(code, body, 0, "rollback-publish")
    if sample.read_bytes() != sample_before:
        fail("rollback-publish bytes differ")
    if before != sample_before:
        fail("copy did not preserve the source return")
    claim("rollback-retire and rollback-publish restore the member bytes", "one-member copy", "ran", "passed", "recovery case, not a second full migration", "reproduced")


def interrupt(root: Path) -> None:
    root.mkdir(parents=True)
    audit = filtered_audit(["0101.app-entry-0506"])
    audit_path = root / "audit.json"
    audit_path.write_bytes(dump(audit))
    make_book(root, audit)
    plan = root / "plan.json"
    code, body, _err = cli(["plan", "--book", str(root / "book"), "--audit", str(audit_path), "--out", str(plan)])
    expect(code, body, 0, "interrupt plan")
    write_fixture(root, root / "book", plan, audit_path)
    for command in ("init", "stage", "reconstruct"):
        args = [command, "--book", str(root / "book"), *auth_args(root, plan, audit_path)]
        if command == "init":
            args = ["init", "--book", str(root / "book"), "--name", "00.00.10.work", *auth_args(root, plan, audit_path)]
        code, body, _err = cli(args)
        expect(code, body, 0, f"interrupt {command}")
    code, body, _err = cli(["publish", "--book", str(root / "book"), "--interrupt-after", "1", *auth_args(root, plan, audit_path)])
    expect(code, body, 3, "interrupt publish")
    code, body, _err = cli(["publish-resume", "--book", str(root / "book"), *auth_args(root, plan, audit_path)])
    expect(code, body, 0, "interrupt resume")
    claim("partial publish stays partial until resume", "one-member copy", "ran", "passed", "interrupt exit 3 then resume exit 0", "reproduced")


def live_probes(root: Path) -> dict:
    for path in PROPOSED.values():
        if path.exists():
            fail(f"proposed path already exists {path}")
    door = (LIVE / "0100.band.returns" / "01.md").read_bytes()
    plan = root / "live-plan.json"
    code, body, err = cli(["plan", "--book", str(LIVE), "--audit", str(AUDIT_PATH), "--out", str(plan)])
    expect(code, body, 0, "live plan")
    if err or (LIVE / "return-line-layout.json").exists():
        fail("live plan wrote a layout or stderr")
    raw = plan.read_bytes()
    planned = json.loads(raw)
    if planned.get("live_moves") is not False or planned.get("live_apply") is not False:
        fail("live plan flags")
    code, body, _err = cli([
        "preflight", "--book", str(LIVE), "--authorization", str(root / "missing-live-auth.json"),
        "--audit", str(AUDIT_PATH), "--plan", str(plan),
        "--backup", str(root / "backup"), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
    ])
    expect(code, body, 2, "live missing preflight")
    if "canonical live book is refused" in str(body.get("correction")):
        fail("facade pre-launch veto returned")
    if (LIVE / "return-line-layout.json").exists():
        fail("live preflight wrote a layout")
    auth = root / "primary" / "auth.json"
    code, body, err = cli(["init", "--book", str(LIVE), "--name", "00.00.10.work", "--authorization", str(auth),
                           "--audit", str(AUDIT_PATH), "--plan", str(plan),
                           "--backup", str(root / "primary" / "backup"), "--staging", str(root / "primary" / "staging"),
                           "--retired", str(root / "primary" / "retired")])
    text = json.dumps(body)
    if code == 0 or "canonical live book is refused" in text or "canonical live book is refused" in err:
        fail(f"live init {code} {text[:300]} {err[:200]}")
    if (LIVE / "return-line-layout.json").exists() or (LIVE / "0100.band.returns" / "01.md").read_bytes() != door:
        fail("live init mutated the book")
    claim("live plan and missing authority write nothing", "live book", "ran", "passed", "read-only readiness; init stayed refused", "author")
    return {"bytes": len(raw), "matches_05_06_plan": sha(raw) == PRIOR_PLAN, "sha256": sha(raw)}


def fixture_entry(book: Path, binding: Path) -> None:
    app = ROOT / "fixture-app"
    app.mkdir()
    source = SNAPSHOT.read_text(encoding="utf-8")
    old_lines = 'parent / "return_line_tools_v2.py"'
    old_hand = 'parent / "handoff_tools.py"'
    if source.count(old_lines) != 1 or source.count(old_hand) != 1:
        fail("snapshot load lines are not unique")
    if "authoring_tools_v2.py" not in source or "review_loop_tools_v4.py" not in source:
        fail("snapshot lost authoring or review-loop")
    header = (
        "# FIXTURE DISPATCHER NOT THE APP.\n"
        "# Generated for 0521/05.09 from the pre-Grok-1 snapshot.\n"
        "# Do not copy this file over app/librarian.py.\n"
    )
    replaced = source.replace(old_lines, 'parent / "return_line_tools_v3.py"', 1)
    replaced = replaced.replace(old_hand, 'parent / "handoff_tools_v2.py"', 1)
    if not replaced.startswith("#!/usr/bin/env python3\n"):
        fail("snapshot shebang changed")
    fixture_text = replaced.replace("#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n" + header, 1)
    fixture = app / "librarian.py"
    fixture.write_bytes(fixture_text.encode("utf-8"))
    shutil.copyfile(FACADE, app / "return_line_tools_v3.py")
    shutil.copyfile(HANDOFF_FACADE, app / "handoff_tools_v2.py")
    if "Path(r'D:\\Git\\lib-build')" in fixture_text:
        fail("fixture file contains the driver code_root override")
    driver = ROOT / "fixture-driver.py"
    driver.write_bytes(
        "import sys\nfrom pathlib import Path\n"
        "fixture = Path(sys.argv[1])\ncommand = sys.argv[2:]\n"
        "source = fixture.read_text(encoding='utf-8')\n"
        "old = 'code_root = Path(__file__).resolve().parent.parent'\n"
        "if source.count(old) != 1:\n    raise SystemExit(2)\n"
        "source = source.replace(old, 'code_root = Path(r\"D:\\\\Git\\\\lib-build\")', 1)\n"
        "ns = {'__name__': 'fixture_dispatcher', '__file__': str(fixture)}\n"
        "exec(compile(source, str(fixture), 'exec'), ns)\n"
        "try:\n    ns['main'](command)\n"
        "except SystemExit as exc:\n"
        "    code = exc.code\n    raise SystemExit(0 if code is None else int(code))\n".encode("utf-8")
    )
    code, out, err = run(driver, [str(fixture), "return-lines", "status", "--book", str(book)])
    if code != 0 or err or b'"legacy_writer_closure": "supported-routes-prepared"' not in out.replace(b"\r\n", b"\n"):
        fail(f"fixture status {code} {err[:200]!r}")
    code, out, err = run(driver, [str(fixture), "capture-return", "--binding", str(binding)])
    text = out.decode("utf-8", "replace")
    if code == 0 or "result ok" in text.splitlines():
        fail(f"fixture capture-return succeeded {code} {text[:240]}")
    claim("fixture dispatcher exercises the two substituted branches", "temp fixture-app", "ran", "passed", "driver code_root override is not in the fixture file and the file was not copied onto the app", "author")


def index_root() -> None:
    rows = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name != "__pycache__"]
        for name in filenames:
            path = Path(dirpath) / name
            data = path.read_bytes()
            rows.append({"bytes": len(data), "path": path.relative_to(ROOT).as_posix(), "sha256": sha(data)})
    rows.sort(key=lambda row: row["path"])
    body = {
        "files": rows,
        "retention": "temporary",
        "root": str(ROOT),
        "schema": "return-access-handoff-fixture-index/0509",
    }
    raw = dump(body)
    (ROOT / "fixture-index.json").write_bytes(raw)
    (EVIDENCE / "fixture-index.json").write_bytes(raw)


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if ROOT.exists():
        fail(f"work root already exists {ROOT}")
    ROOT.mkdir(parents=True)
    print("work root", ROOT)
    if (LIVE / "return-line-layout.json").exists():
        fail("live layout already exists")
    for path in PROPOSED.values():
        if path.exists():
            fail(f"proposed path already exists {path}")
    for _name, (rel, digest, size) in PINS.items():
        data = (REPO / rel).read_bytes()
        if sha(data) != digest or len(data) != size:
            fail(f"pin drifted {rel}")
    audit = json.loads(AUDIT_PATH.read_bytes())
    before = fingerprint(audit)
    door = (LIVE / "0100.band.returns" / "01.md").read_bytes()
    static_callers()
    recovery(ROOT / "recovery")
    interrupt(ROOT / "interrupt")
    primary = ROOT / "primary"
    make_book(primary, audit)
    migrate(primary, audit, AUDIT_PATH)
    assert_retired(primary, audit)
    lookups(primary / "book")
    filings(primary, AUDIT_PATH)
    verify_filing(primary / "book")
    readers(primary)
    changed_evidence(primary)
    guard_marked(primary / "book")
    side_layout_cases(ROOT / "sides")
    doorless_handoff(ROOT / "handoff")
    guard_mismatch(ROOT / "mismatch")
    historical_still_runs(ROOT / "historical")
    plan_identity = live_probes(ROOT)
    fixture_entry(primary / "book", ROOT / "handoff" / "binding.json")
    after = fingerprint(audit)
    if after != before or (LIVE / "0100.band.returns" / "01.md").read_bytes() != door:
        fail("live bytes changed")
    if (LIVE / "return-line-layout.json").exists():
        fail("live layout written")
    for path in PROPOSED.values():
        if path.exists():
            fail(f"proposed path created {path}")
    for _name, (rel, digest, size) in PINS.items():
        data = (REPO / rel).read_bytes()
        if sha(data) != digest or len(data) != size:
            fail(f"pin changed during the suite {rel}")
    claim("Prime independent probes", "reviewer", "not-run", "not-run", "author cases do not substitute", "reviewer-independent")
    claim("app selection and live migration", "current app", "not-run", "not-run", "dispatcher and README were not edited", "not-selected")
    claim("demo.py and rehearse.py execution", "historical fixtures", "not-run", "not-run", "static selection only; future disposition is a new file", "unselected")
    claim("colab seam replay", "05.06 seam", "not-run", "not-run", "outside this pack's facade sequence", "not-run")
    report = {
        "accepted": False,
        "approved": False,
        "claims_passed": sum(1 for item in CLAIMS if item["outcome"] == "passed"),
        "claims_not_run": sum(1 for item in CLAIMS if item["outcome"] == "not-run"),
        "commands": len(LOG),
        "committed": False,
        "custody": "pending",
        "live_fingerprint_after": after,
        "live_fingerprint_before": before,
        "live_layout_written": False,
        "live_plan": plan_identity,
        "published": False,
        "schema": "return-access-handoff-suite/0509",
        "seated": False,
        "work_root": str(ROOT),
    }
    (ROOT / "suite-report.json").write_bytes(dump(report))
    (EVIDENCE / "suite-report.json").write_bytes(dump(report))
    (EVIDENCE / "commands.json").write_bytes(dump({"commands": LOG, "schema": "return-access-handoff-commands/0509"}))
    (EVIDENCE / "claims.json").write_bytes(dump({"claims": CLAIMS, "schema": "return-access-handoff-claims/0509"}))
    (EVIDENCE / "first-failure.txt").write_bytes(b"No command failed in the official run.\n")
    index_root()
    print("OK", ROOT)


if __name__ == "__main__":
    main()
