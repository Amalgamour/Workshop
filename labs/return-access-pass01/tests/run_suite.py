#!/usr/bin/env python3
"""Retained-copy seam for source/pass return access.

Producer commands call pinned pass03. Consumer commands call app/librarian.py.
Nothing here writes the live book. The tree under D:\\librarian\\temp\\0521-0507
is kept, including the first run's stdout.
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
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LIVE = REPO / "00.kernel" / "00.00.10.work"
AUDIT_PATH = LIVE / "0417.return-placement" / "evidence" / "audit-corrected.json"
PASS03 = REPO / "labs" / "return-lines-pass03" / "return_lines.py"
APP = REPO / "app" / "librarian.py"
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
BASE = Path(r"D:\librarian\temp\0521-0507")
LAYOUT_SHA = "2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804"
LAYOUT_BYTES = 216
NATIVE_REASON = "native line-pass return is not a legacy single-envelope page"
RELEASE_TEXT = (
    "Work in D:\\Git\\lib-build.\n"
    "\n"
    "Run:\n"
    "D:\\Git\\lib-build\\00.kernel\\00.00.10.work\\0521.return-placement\\05.04.md\n"
    "\n"
    "This releases the bounded tooling build described there.\n"
    "Reconstruct and verify the correct return pages before retirement.\n"
    "Test full retirement, old-identity lookup, rollback and first new filings\n"
    "on disposable copies, preserving all original bytes.\n"
    "\n"
    "No live moves or app/caller changes. Return with evidence and stop\n"
    "for Codex Prime review.\n"
)
OPS = [
    "init", "reserve", "capture", "stage", "stage-resume", "rollback-stage",
    "reconstruct", "reconstruct-resume", "publish", "publish-resume",
    "retire", "retire-resume", "rollback-publish", "rollback-retire",
]
MEMBERS = [
    "0103.return-capture-0502",
    "0104.app-entry-0508",
    "0121.archive-resolution-0508",
    "0122.bridge-overlap-0513",
    "0123.boot-validation-0508",
    "0124.clerk-seam-design-0503",
    "0125.mapping-capture-0509",
    "0154.colab-support-first-0501",
    "0165.bench-method-colab-0501",
]
HISTORICAL = {
    "0121.archive-resolution-0508": ("0508.return-capture", "05.08", "0108.return-capture", "originals"),
    "0122.bridge-overlap-0513": ("0504.app-entry", "05.13", "0104.app-entry", "originals"),
    "0123.boot-validation-0508": ("0507.prime-support", "05.08", "0107.prime-support", "originals"),
    "0124.clerk-seam-design-0503": ("0506.clerk-handoff", "05.03", "0106.clerk-handoff", "originals"),
    "0125.mapping-capture-0509": ("0508.return-capture", "05.09", "0108.return-capture", "originals"),
}
FILINGS = [
    ("0521.return-placement", "05.01", "filing-0521-0501", "0121.return-placement"),
    ("0522.review-construction", "05.01", "filing-0522-0501", "0122.review-construction"),
    ("0523.desk-core", "05.01", "filing-0523-0501", "0123.desk-core"),
    ("0524.prime-desk", "05.01", "filing-0524-0501", "0124.prime-desk"),
    ("0525.app-dependencies", "05.01", "filing-0525-0501", "0125.app-dependencies"),
]
PINS = {
    "app/authoring_tools_v2.py": ("f191e43337ab9b6ac2c863b0c0f0eb91a0b55d00d2df99c2897a96a0965e1124", 8049),
    "app/authoring-v2.json": ("14965030b2344f77e196a1d6a29b8cb74400cc3cf237e4f5ecc44c2adf332d11", 2106),
    "app/review_loop_tools_v4.py": ("0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296", 13381),
    "app/review-loop-v4.json": ("769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723", 2519),
    "labs/return-access-pass01/return_access.py": ("501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5", 26561),
    "labs/return-lines-pass03/return_lines.py": ("78cc4d8679bb6e54b3f2456ce777643da7a9a650ef5c79c216abd38a4c209c63", 33349),
    "labs/return-lines-pass02/return_lines.py": ("6691d0587ab97ba24a1709c9950b506961152939e2d112ee608f9dbd23e92908", 82908),
    "labs/return-lines-pass01/return_lines.py": ("863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897),
    "labs/return-placement-pass01/return_placement.py": ("db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754", 66097),
    "labs/return-capture-pass01/return_capture.py": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
}

ENV = os.environ.copy()
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
CASES: list[dict] = []
ROOT: Path
BOOK: Path
RETIRED: Path
BACKUP: Path
CMD: Path
SEQ = 0


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def fail(name: str, detail: dict) -> None:
    record = {"name": name, "ok": False, "detail": detail}
    CASES.append(record)
    (ROOT / "cases.jsonl").open("a", encoding="utf-8", newline="\n").write(json.dumps(record, ensure_ascii=False) + "\n")
    (ROOT / "first-failure.json").write_bytes(dump({"schema": "return-access-entry-run/1", "first_failure": name, "detail": detail, "case_count": len(CASES)}))
    print(f"FAIL {name}", flush=True)
    raise SystemExit(1)


def ok(name: str, detail: dict | None = None) -> None:
    record = {"name": name, "ok": True}
    if detail is not None:
        record["detail"] = detail
    CASES.append(record)
    (ROOT / "cases.jsonl").open("a", encoding="utf-8", newline="\n").write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"ok {name}", flush=True)


def run(which: str, args: list[str], name: str) -> subprocess.CompletedProcess:
    global SEQ
    SEQ += 1
    script = APP if which == "app" else PASS03
    proc = subprocess.run(
        [str(PY), "-B", str(script), *args],
        cwd=REPO,
        env=ENV,
        capture_output=True,
        shell=False,
    )
    (CMD / f"{SEQ:03d}-{name}.out").write_bytes(proc.stdout)
    (CMD / f"{SEQ:03d}-{name}.err").write_bytes(proc.stderr)
    return proc


def as_json(proc: subprocess.CompletedProcess, name: str) -> dict:
    try:
        body = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(name, {
            "error": str(exc),
            "code": proc.returncode,
            "stderr": proc.stderr.decode("utf-8", "replace")[:2000],
            "stdout_head": proc.stdout[:400].decode("utf-8", "replace"),
        })
    if not isinstance(body, dict):
        fail(name, {"error": "result is not an object", "code": proc.returncode})
    return body


def require_producer(args: list[str], name: str) -> dict:
    proc = run("pass03", args, name)
    body = as_json(proc, name)
    if proc.returncode != 0 or body.get("state") != "complete":
        fail(name, {"code": proc.returncode, "state": body.get("state"), "check": body.get("check"), "correction": body.get("correction"), "detail": body.get("detail")})
    ok(name, {"code": proc.returncode, "state": body.get("state")})
    return body


def auth_args(audit: Path, plan: Path) -> list[str]:
    return [
        "--authorization", str(ROOT / "auth.json"),
        "--audit", str(audit),
        "--plan", str(plan),
        "--backup", str(BACKUP),
        "--staging", str(ROOT / "staging"),
        "--retired", str(RETIRED),
    ]


def rel_under(path: str, member: str) -> str | None:
    normed = path.replace("\\", "/")
    token = "/" + member + "/"
    wrapped = "/" + normed
    index = wrapped.find(token)
    if index < 0:
        return None
    return wrapped[index + len(token):]


def filtered_audit() -> dict:
    body = json.loads(AUDIT_PATH.read_bytes().decode("utf-8"))
    wanted = set(MEMBERS)
    body["records"] = [record for record in body["records"] if record.get("old_member") in wanted]
    files = []
    for entry in body["files"]:
        path = str(entry.get("path", "")).replace("\\", "/")
        if any(rel_under(path, name) is not None for name in wanted):
            files.append(entry)
    body["files"] = files
    return body


def copy_exact(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())


def seed(audit_body: dict) -> dict:
    before: dict = {"members": {}, "tails": {}, "omitted_extra_files": {}}
    copy_exact(LIVE / "0100.band.returns" / "01.md", BOOK / "0100.band.returns" / "01.md")
    by_member: dict[str, list[tuple[str, dict]]] = {name: [] for name in MEMBERS}
    for entry in audit_body["files"]:
        path = str(entry["path"])
        matches = [name for name in MEMBERS if rel_under(path, name) is not None]
        if len(matches) != 1:
            fail("seed-audit-path", {"path": path, "matches": matches})
        member = matches[0]
        rel = rel_under(path, member)
        if not rel:
            fail("seed-audit-path", {"path": path, "member": member})
        by_member[member].append((rel, entry))
    for member, rows in by_member.items():
        src_root = LIVE / member
        present = {}
        for dirpath, dirnames, filenames in os.walk(src_root):
            dirnames[:] = [item for item in dirnames if not (Path(dirpath) / item).is_symlink()]
            for filename in filenames:
                src = Path(dirpath) / filename
                present[src.relative_to(src_root).as_posix()] = src
        expected = {rel for rel, _entry in rows}
        extra = sorted(set(present) - expected)
        missing = sorted(expected - set(present))
        before["omitted_extra_files"][member] = extra
        if missing:
            fail("seed-missing-audited-file", {"member": member, "missing": missing[:20]})
        stored = {}
        for rel, entry in rows:
            src = src_root / rel
            data = src.read_bytes()
            digest = sha(data)
            if digest != entry.get("sha256") or len(data) != entry.get("bytes"):
                fail("seed-stale-source", {"member": member, "rel": rel, "live": digest, "audit": entry.get("sha256")})
            copy_exact(src, BOOK / member / rel)
            stored[rel] = {"bytes": len(data), "sha256": digest}
        before["members"][member] = stored
    for record in audit_body["records"]:
        if record.get("route") != "page-local-colab":
            continue
        rel = str(record["target_return"]).replace("\\", "/")
        src = LIVE.joinpath(*rel.split("/"))
        if not src.is_file():
            fail("seed-missing-tail", {"path": rel})
        data = src.read_bytes()
        member_return = (BOOK / record["old_member"] / "return.md").read_bytes()
        if data != member_return:
            fail("seed-tail-differs", {"path": rel, "member": record["old_member"]})
        copy_exact(src, BOOK.joinpath(*rel.split("/")))
        before["tails"][rel] = {"bytes": len(data), "sha256": sha(data)}
    (ROOT / "source-before.json").write_bytes(dump(before))
    ok("seed", {"members": len(MEMBERS), "omitted_extra_counts": {key: len(value) for key, value in before["omitted_extra_files"].items()}})
    return before


def layout_bytes() -> bytes:
    body = {
        "allocation": "line-pass",
        "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
        "book": "00.00.10.work",
        "schema": "return-line-layout/1",
        "sequential_allocation": False,
    }
    return dump(body)


def write_fixture(audit: Path, plan: Path) -> None:
    raw = audit.read_bytes()
    planned = plan.read_bytes()
    body = {
        "audit_bytes": len(raw),
        "audit_sha256": sha(raw),
        "backup_root": str(BACKUP),
        "book": "00.00.10.work",
        "book_path": str(BOOK),
        "executor": "Codex Prime",
        "layout_sha256": sha(layout_bytes()),
        "operations": list(OPS),
        "plan_sha256": sha(planned),
        "release": RELEASE_TEXT,
        "retired_root": str(RETIRED),
        "schema": "return-line-authorization/1",
        "staging_root": str(ROOT / "staging"),
        "synthetic": True,
    }
    (ROOT / "auth.json").write_bytes(dump(body))


def migrate(audit: Path, plan: Path) -> None:
    flags = auth_args(audit, plan)
    require_producer(["init", "--book", str(BOOK), "--name", "00.00.10.work", *flags], "producer-init")
    require_producer(["stage", "--book", str(BOOK), *flags], "producer-stage")
    require_producer(["reconstruct", "--book", str(BOOK), *flags], "producer-reconstruct")
    require_producer(["publish", "--book", str(BOOK), *flags], "producer-publish")
    require_producer(["retire", "--book", str(BOOK), *flags], "producer-retire")


def app_json(args: list[str], name: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = run("app", ["return-lines", *args], name)
    return proc, as_json(proc, name)


def access_flags(body: dict, name: str) -> None:
    for key, expected in (
        ("schema", "return-access-result/1"),
        ("accepted", False),
        ("approved", False),
        ("published", False),
        ("custody_is_acceptance", False),
        ("task_association", "not-established"),
    ):
        if body.get(key) != expected:
            fail(name, {"field": key, "value": body.get(key)})
    detail = body.get("detail") if isinstance(body.get("detail"), dict) else {}
    if detail.get("sentinel_policy") != "not-adopted" or detail.get("successor_consumed") is not False:
        fail(name, {"detail": detail})


def consume(body: dict, name: str) -> dict:
    described = body.get("descriptor")
    if not isinstance(described, dict):
        fail(name, {"error": "consumer received no descriptor", "state": body.get("state")})
    view = {
        "custody_path": described.get("custody_path"),
        "return_path": described.get("return_path"),
        "target_page": described.get("target_page"),
    }
    for label, rel in view.items():
        if not isinstance(rel, str) or not rel:
            fail(name, {"field": label, "value": rel})
    return view


def expect_access(args: list[str], name: str, code: int, state: str) -> dict:
    proc, body = app_json(args, name)
    access_flags(body, name)
    if proc.returncode != code or body.get("exit") != code or body.get("state") != state:
        fail(name, {"code": proc.returncode, "exit": body.get("exit"), "state": body.get("state"), "correction": body.get("correction"), "missing": body.get("missing")})
    ok(name, {"state": state, "exit": code})
    return body


def expect_stop(args: list[str], name: str, text: str) -> None:
    proc = run("app", ["return-lines", *args], name)
    err = proc.stderr.decode("utf-8", "replace")
    if proc.returncode != 2 or proc.stdout != b"" or not err.startswith("stop:") or text not in err:
        fail(name, {"code": proc.returncode, "stderr": err[:500], "stdout": proc.stdout[:200].decode("utf-8", "replace")})
    ok(name, {"stderr": err.strip()})


def parent_kind(member: str) -> str:
    originals = RETIRED / "originals" / member
    occupants = RETIRED / "occupants" / member
    if originals.is_dir() and occupants.is_dir():
        fail("legacy-parent", {"member": member, "error": "both parents exist"})
    if originals.is_dir():
        return "originals"
    if occupants.is_dir():
        return "occupants"
    fail("legacy-parent", {"member": member, "error": "no retired parent"})
    return ""


def check_historical(before: dict) -> None:
    for member, (page, batch, target, kind) in HISTORICAL.items():
        found = parent_kind(member)
        if found != kind:
            fail(f"parent-{member}", {"found": found, "expected": kind})
        body = expect_access(
            ["verify", "--book", str(BOOK), "--member", member],
            f"verify-member-{member}",
            0,
            "complete",
        )
        view = consume(body, f"consume-{member}")
        if view["target_page"] != target or not str(view["return_path"]).endswith(f"/{batch}.return.md"):
            fail(f"route-{member}", view)
        origin = body["descriptor"]["origin"]
        if origin.get("page") != page or origin.get("batch") != batch:
            fail(f"origin-{member}", origin)
        legacy = body.get("legacy") if isinstance(body.get("legacy"), dict) else {}
        parent = str(legacy.get("parent") or "")
        if legacy.get("called") is not True or legacy.get("exit") != 0 or legacy.get("member") != member:
            fail(f"reader-{member}", legacy)
        if not parent.replace("\\", "/").rstrip("/").endswith("/" + kind):
            fail(f"reader-parent-{member}", legacy)
        if "not accepted" not in str(legacy.get("text")):
            fail(f"reader-text-{member}", {"text": legacy.get("text")})
        ok(f"historical-{member}", view)
    for batch, member in (("05.02", "0103.return-capture-0502"), ("05.08", "0121.archive-resolution-0508")):
        body = expect_access(
            ["verify", "--book", str(BOOK), "--source", "0508.return-capture", "--pass", batch],
            f"verify-0508-{batch}",
            0,
            "complete",
        )
        view = consume(body, f"consume-0508-{batch}")
        if view["target_page"] != "0108.return-capture" or view["return_path"] != f"0108.return-capture/{batch}.return.md":
            fail(f"two-pass-{batch}", view)
        if body["legacy"].get("member") != member or not str(body["legacy"].get("parent")).replace("\\", "/").endswith("/originals"):
            fail(f"two-pass-reader-{batch}", body.get("legacy"))
        ok(f"two-pass-{batch}", view)
    occupant = expect_access(
        ["verify", "--book", str(BOOK), "--member", "0104.app-entry-0508"],
        "verify-occupant-0104",
        0,
        "complete",
    )
    if occupant["legacy"].get("member") != "0104.app-entry-0508" or not str(occupant["legacy"].get("parent")).replace("\\", "/").endswith("/occupants"):
        fail("occupant-parent", occupant.get("legacy"))
    if occupant["descriptor"]["target_page"] != "0104.app-entry":
        fail("occupant-target", occupant["descriptor"])
    ok("occupant-0104", {"parent": occupant["legacy"].get("parent")})
    incomplete = expect_access(
        ["lookup", "--book", str(BOOK), "--member", "0154.colab-support-first-0501"],
        "lookup-0154",
        1,
        "incomplete",
    )
    if incomplete.get("partial") is not False:
        fail("0154-partial", {"partial": incomplete.get("partial")})
    missing = incomplete.get("missing") if isinstance(incomplete.get("missing"), list) else []
    if "return" not in missing or "route" in missing:
        fail("0154-missing", {"missing": missing})
    if incomplete.get("descriptor") is None or incomplete["descriptor"].get("return_sha256") not in (None, ""):
        fail("0154-invented", incomplete.get("descriptor"))
    legacy = incomplete.get("legacy") if isinstance(incomplete.get("legacy"), dict) else {}
    if legacy.get("called") is not True or legacy.get("exit") == 0:
        fail("0154-reader", legacy)
    if "legacy-envelope" not in missing:
        fail("0154-legacy-missing", {"missing": missing, "legacy": legacy})
    ok("incomplete-0154", {"missing": missing, "parent": legacy.get("parent")})
    local = expect_access(
        ["verify", "--book", str(BOOK), "--source", "0701.bench-method", "--pass", "05.01"],
        "verify-n7",
        0,
        "complete",
    )
    view = consume(local, "consume-n7")
    if view["target_page"] != "0701.bench-method" or view["return_path"] != "0701.bench-method/05.01.return.md":
        fail("n7-route", view)
    if local["descriptor"].get("route") != "page-local-colab":
        fail("n7-route-name", local["descriptor"])
    if local["legacy"].get("member") != "0165.bench-method-colab-0501":
        fail("n7-legacy", local.get("legacy"))
    tail = (BOOK / "0701.bench-method" / "05.01.return.md").read_bytes()
    if sha(tail) != before["tails"]["0701.bench-method/05.01.return.md"]["sha256"]:
        fail("n7-tail-bytes", {"sha256": sha(tail)})
    ok("n7", view)
    for member, files in before["members"].items():
        kind = parent_kind(member)
        if (BOOK / member).exists():
            fail("member-still-in-book", {"member": member})
        for rel, meta in files.items():
            dest = RETIRED / kind / member / rel
            if not dest.is_file():
                fail("retired-missing", {"member": member, "rel": rel, "kind": kind})
            data = dest.read_bytes()
            if sha(data) != meta["sha256"] or len(data) != meta["bytes"]:
                fail("retired-bytes", {"member": member, "rel": rel})
    ok("source-after", {"members": len(before["members"])})


def file_pair(submission: str) -> tuple[Path, Path]:
    folder = ROOT / "filings" / submission
    folder.mkdir(parents=True, exist_ok=True)
    ret = folder / "return.md"
    note = folder / "note.md"
    ret.write_bytes(f"synthetic filing {submission}\nnot acceptance\n".encode("utf-8"))
    note.write_bytes(f"note for {submission}\n".encode("utf-8"))
    return ret, note


def reserve_capture(page: str, batch: str, submission: str, name: str) -> dict:
    flags = auth_args(ROOT / "audit.json", ROOT / "plan.json")
    proc, body = app_json([
        "reserve", "--book", str(BOOK), "--page", page, "--batch", batch,
        "--submission", submission, "--output", "note.md",
        "--submitter", "grok-1", "--reviewer", "Codex Prime",
        "--release", "synthetic filing on a disposable copy",
        *flags,
    ], f"reserve-{name}")
    if proc.returncode != 1 or body.get("schema") != "return-line-result/1" or body.get("state") != "reserved":
        fail(f"reserve-{name}", {"code": proc.returncode, "schema": body.get("schema"), "state": body.get("state"), "correction": body.get("correction")})
    ok(f"reserve-{name}", {"state": body.get("state")})
    ret, note = file_pair(submission)
    proc, body = app_json([
        "capture", "--book", str(BOOK), "--page", page, "--batch", batch,
        "--submission", submission, "--return-file", str(ret),
        "--artifact", "note.md", str(note),
        *flags,
    ], f"capture-{name}")
    if proc.returncode != 0 or body.get("schema") != "return-line-result/1" or body.get("state") != "complete":
        fail(f"capture-{name}", {"code": proc.returncode, "state": body.get("state"), "correction": body.get("correction"), "detail": body.get("detail")})
    ok(f"capture-{name}", {"state": body.get("state")})
    return body


def check_filings() -> dict:
    views = {}
    hashes = {}
    for page, batch, submission, target in FILINGS:
        if not (LIVE / page).is_dir():
            fail("real-source-page", {"page": page})
        reserve_capture(page, batch, submission, submission)
        body = expect_access(
            ["verify", "--book", str(BOOK), "--source", page, "--pass", batch],
            f"verify-filing-{submission}",
            0,
            "complete",
        )
        view = consume(body, f"consume-{submission}")
        if view["target_page"] != target or view["return_path"] != f"{target}/{batch}.return.md":
            fail(f"filing-route-{submission}", view)
        legacy = body.get("legacy") if isinstance(body.get("legacy"), dict) else {}
        if legacy.get("called") is not False or legacy.get("reason") != NATIVE_REASON or legacy.get("parent") is not None:
            fail(f"native-{submission}", legacy)
        ret = (BOOK / view["return_path"]).read_bytes()
        if sha(ret) != body["descriptor"].get("return_sha256"):
            fail(f"consumer-bytes-{submission}", {"file": sha(ret), "descriptor": body["descriptor"].get("return_sha256")})
        views[submission] = view
        hashes[submission] = sha(ret)
        ok(f"filing-{submission}", view)
    reserve_capture("0521.return-placement", "05.02", "filing-0521-0502", "filing-0521-0502")
    second = expect_access(
        ["verify", "--book", str(BOOK), "--source", "0521.return-placement", "--pass", "05.02"],
        "verify-0521-0502",
        0,
        "complete",
    )
    view = consume(second, "consume-0521-0502")
    if view["return_path"] != "0121.return-placement/05.02.return.md" or second["legacy"].get("reason") != NATIVE_REASON:
        fail("second-pass", {"view": view, "legacy": second.get("legacy")})
    if second["descriptor"].get("return_sha256") == hashes["filing-0521-0501"]:
        fail("second-pass-hash", {"hash": second["descriptor"].get("return_sha256")})
    hashes["filing-0521-0502"] = second["descriptor"]["return_sha256"]
    views["filing-0521-0502"] = view
    ok("new-two-pass", view)
    flags = auth_args(ROOT / "audit.json", ROOT / "plan.json")
    ret, note = file_pair("filing-0521-0502")
    proc, body = app_json([
        "capture", "--book", str(BOOK), "--page", "0521.return-placement", "--batch", "05.02",
        "--submission", "filing-0521-0502", "--return-file", str(ret),
        "--artifact", "note.md", str(note), *flags,
    ], "capture-replay")
    if proc.returncode != 0 or body.get("state") != "complete" or body.get("detail", {}).get("rewritten") is not False:
        fail("capture-replay", {"code": proc.returncode, "state": body.get("state"), "detail": body.get("detail")})
    sealed = (BOOK / "0121.return-placement" / "05.02.return.md").read_bytes()
    ok("capture-replay", {"rewritten": False})
    other = ROOT / "filings" / "filing-0521-0502" / "other-return.md"
    other.write_bytes(b"conflicting synthetic bytes\nnot acceptance\n")
    proc, body = app_json([
        "capture", "--book", str(BOOK), "--page", "0521.return-placement", "--batch", "05.02",
        "--submission", "filing-0521-0502", "--return-file", str(other),
        "--artifact", "note.md", str(note), *flags,
    ], "capture-conflict")
    if proc.returncode != 2 or body.get("state") != "conflict":
        fail("capture-conflict", {"code": proc.returncode, "state": body.get("state"), "correction": body.get("correction")})
    if (BOOK / "0121.return-placement" / "05.02.return.md").read_bytes() != sealed:
        fail("capture-conflict-sealed", {"error": "sealed return changed"})
    attempt = BOOK / "0121.return-placement" / "05.02.refused" / "attempt-001" / "return.md"
    if not attempt.is_file() or attempt.read_bytes() != other.read_bytes():
        fail("capture-conflict-attempt", {"exists": attempt.is_file()})
    ok("capture-conflict", {"evidence": body.get("evidence")})
    proc, reserved = app_json([
        "reserve", "--book", str(BOOK), "--page", "0522.review-construction", "--batch", "05.02",
        "--submission", "filing-0522-0502", "--output", "note.md",
        "--submitter", "grok-1", "--reviewer", "Codex Prime",
        "--release", "synthetic filing on a disposable copy", *flags,
    ], "reserve-0522-0502")
    if proc.returncode != 1 or reserved.get("state") != "reserved":
        fail("reserve-only", {"code": proc.returncode, "state": reserved.get("state"), "correction": reserved.get("correction")})
    held = expect_access(
        ["lookup", "--book", str(BOOK), "--source", "0522.review-construction", "--pass", "05.02"],
        "lookup-reserved",
        1,
        "reserved",
    )
    if held.get("partial") is not False or "route" in (held.get("missing") or []) or held.get("descriptor") is None:
        fail("reserved-shape", {"partial": held.get("partial"), "missing": held.get("missing")})
    ok("reserved-not-missing-route", {"return_path": held["descriptor"].get("return_path")})
    proc, partial_reserve = app_json([
        "reserve", "--book", str(BOOK), "--page", "0523.desk-core", "--batch", "05.02",
        "--submission", "filing-0523-0502", "--output", "note.md",
        "--submitter", "grok-1", "--reviewer", "Codex Prime",
        "--release", "synthetic filing on a disposable copy", *flags,
    ], "reserve-partial")
    if proc.returncode != 1 or not isinstance(partial_reserve.get("descriptor"), dict):
        fail("reserve-partial", {"code": proc.returncode, "state": partial_reserve.get("state"), "correction": partial_reserve.get("correction")})
    custody = BOOK / str(partial_reserve["descriptor"]["custody_path"])
    (custody / "payload").mkdir(parents=True, exist_ok=True)
    (custody / "payload" / "0001.blob").write_bytes(b"partial planted bytes\n")
    partial = expect_access(
        ["verify", "--book", str(BOOK), "--source", "0523.desk-core", "--pass", "05.02"],
        "verify-partial",
        1,
        "incomplete",
    )
    if partial.get("partial") is not True or "route" in (partial.get("missing") or []):
        fail("partial-shape", {"partial": partial.get("partial"), "missing": partial.get("missing"), "state": partial.get("state")})
    ok("partial-custody", {"custody": str(partial["descriptor"].get("custody_path"))})
    payload = BOOK / "0125.app-dependencies" / "05.01.custody" / "payload" / "0001.blob"
    sealed_return = (BOOK / "0125.app-dependencies" / "05.01.return.md").read_bytes()
    sealed_hash = sha(sealed_return)
    payload.write_bytes(payload.read_bytes() + b"\nchanged\n")
    changed = expect_access(
        ["verify", "--book", str(BOOK), "--source", "0525.app-dependencies", "--pass", "05.01"],
        "verify-changed-payload",
        2,
        "conflict",
    )
    if (BOOK / "0125.app-dependencies" / "05.01.return.md").read_bytes() != sealed_return:
        fail("changed-payload-sealed", {"error": "return.md changed"})
    if changed["descriptor"].get("return_sha256") != sealed_hash or changed["legacy"].get("called") is not False:
        fail("changed-payload-descriptor", {"hash": changed["descriptor"].get("return_sha256"), "legacy": changed.get("legacy")})
    ok("changed-payload", {"return_sha256": sealed_hash})
    (ROOT / "consumer-view.json").write_bytes(dump({"filings": views, "hashes": hashes}))
    return hashes


def check_refusals(first_hash: str) -> None:
    wrong_band = expect_access(
        ["lookup", "--book", str(BOOK), "--source", "0201.no-such", "--pass", "05.01"],
        "lookup-wrong-band",
        2,
        "refused",
    )
    if wrong_band.get("descriptor") is not None or "route" not in (wrong_band.get("missing") or []):
        fail("wrong-band-shape", {"descriptor": wrong_band.get("descriptor"), "missing": wrong_band.get("missing")})
    ok("wrong-band")
    wrong_subject = expect_access(
        ["lookup", "--book", str(BOOK), "--source", "0521.not-the-subject", "--pass", "05.01"],
        "lookup-wrong-subject",
        1,
        "incomplete",
    )
    view = consume(wrong_subject, "consume-wrong-subject")
    if view["target_page"] != "0121.not-the-subject" or view["target_page"] == "0121.return-placement":
        fail("wrong-subject-target", view)
    if "return" not in (wrong_subject.get("missing") or []) or "route" in (wrong_subject.get("missing") or []):
        fail("wrong-subject-missing", wrong_subject.get("missing"))
    ok("wrong-subject", view)
    wrong_pass = expect_access(
        ["lookup", "--book", str(BOOK), "--source", "0521.return-placement", "--pass", "05.99"],
        "lookup-wrong-pass",
        1,
        "incomplete",
    )
    if wrong_pass["descriptor"].get("return_path") != "0121.return-placement/05.99.return.md":
        fail("wrong-pass-path", wrong_pass["descriptor"])
    if wrong_pass["descriptor"].get("return_sha256") == first_hash:
        fail("wrong-pass-hash", {"hash": wrong_pass["descriptor"].get("return_sha256")})
    ok("wrong-pass")
    for args, name in (
        (["lookup", "--book", str(BOOK), "--source", "0521.return-placement", "--pass", "05.01", "--member", "0121.archive-resolution-0508"], "two-selectors"),
        (["lookup", "--book", str(BOOK), "--source", "0521.return-placement"], "source-without-pass"),
        (["lookup", "--book", str(BOOK), "--pass", "05.01"], "pass-without-source"),
    ):
        body = expect_access(args, name, 2, "refused")
        if body.get("descriptor") is not None:
            fail(name + "-descriptor", body.get("descriptor"))
        ok(name + "-empty")
    page_member = expect_access(
        ["lookup", "--book", str(BOOK), "--member", "0121.return-placement"],
        "lookup-line-page-name",
        2,
        "refused",
    )
    legacy = page_member.get("legacy") if isinstance(page_member.get("legacy"), dict) else {}
    if page_member.get("descriptor") is not None or legacy.get("called") is True:
        fail("line-page-as-member", {"descriptor": page_member.get("descriptor"), "legacy": legacy})
    ok("line-page-not-an-envelope")
    (BOOK / "0198.blocker").mkdir()
    (BOOK / "0198.blocker" / "keep.txt").write_bytes(b"occupied\n")
    flags = auth_args(ROOT / "audit.json", ROOT / "plan.json")
    proc, occupied = app_json([
        "reserve", "--book", str(BOOK), "--page", "0598.occupied-line", "--batch", "05.01",
        "--submission", "filing-0598-0501", "--output", "note.md",
        "--submitter", "grok-1", "--reviewer", "Codex Prime",
        "--release", "synthetic filing on a disposable copy", *flags,
    ], "reserve-occupied")
    if proc.returncode != 2 or occupied.get("state") != "conflict" or occupied.get("evidence") != "0198.blocker":
        fail("occupied", {"code": proc.returncode, "state": occupied.get("state"), "evidence": occupied.get("evidence"), "correction": occupied.get("correction")})
    if (BOOK / "0198.occupied-line").exists():
        fail("occupied-wrote", {"error": "target page was created"})
    ok("occupied-number")
    other = ROOT / "ambiguity-book"
    left = other / "0199.one" / "05.01.custody"
    right = other / "0199.two" / "05.02.custody"
    left.mkdir(parents=True)
    right.mkdir(parents=True)
    (left / "relocation.json").write_bytes(dump({"old_member": "0188.same"}))
    (right / "relocation.json").write_bytes(dump({"old_member": "0188.same"}))
    ambiguous = expect_access(["lookup", "--book", str(other), "--member", "0188.same"], "lookup-ambiguous-member", 2, "refused")
    if ambiguous.get("descriptor") is not None or "member" not in (ambiguous.get("missing") or []):
        fail("ambiguous-member-shape", {"descriptor": ambiguous.get("descriptor"), "missing": ambiguous.get("missing")})
    ok("ambiguous-member")
    source_left = other / "0180.left" / "05.01.custody"
    source_right = other / "0180.right" / "05.03.custody"
    source_left.mkdir(parents=True)
    source_right.mkdir(parents=True)
    origin = {"batch": "05.01", "book": "00.00.10.work", "page": "0580.same-source"}
    (source_left / "reservation.json").write_bytes(dump({"origin": origin}))
    (source_right / "reservation.json").write_bytes(dump({"origin": origin}))
    ambiguous_source = expect_access(
        ["lookup", "--book", str(other), "--source", "0580.same-source", "--pass", "05.01"],
        "lookup-ambiguous-source",
        2,
        "refused",
    )
    if ambiguous_source.get("descriptor") is not None or "source" not in (ambiguous_source.get("missing") or []):
        fail("ambiguous-source-shape", {"missing": ambiguous_source.get("missing")})
    ok("ambiguous-source")


def check_status_and_door() -> None:
    status = expect_access(["status", "--book", str(BOOK)], "status-migrated", 0, "reported")
    layout = status["detail"]["layout"]
    authority = status["detail"]["authority"]
    if layout.get("present") is not True or layout.get("sha256") != LAYOUT_SHA or "layout" in (status.get("missing") or []):
        fail("status-layout", layout)
    if authority.get("established") is not False or authority.get("live_release") is not False or authority.get("successor_consumed") is not False:
        fail("status-authority", authority)
    if "return-line-authorization/1" not in authority.get("requirement", "") or "in-process" not in authority.get("requirement", ""):
        fail("status-requirement", authority)
    if status["detail"].get("incomplete_closure") != "not-established" or status["detail"].get("legacy_writer_closure") != "not-established":
        fail("status-closure", status["detail"])
    if status["detail"].get("sentinel_policy") != "not-adopted":
        fail("status-sentinel", status["detail"])
    writers = status["detail"].get("legacy_writers")
    if not isinstance(writers, list) or len(writers) != 6 or not any(item.get("allocates") is True for item in writers):
        fail("status-writers", writers)
    routes = {item.get("route") for item in writers}
    expected_routes = {
        "return_capture reserve",
        "capture-handoff demo",
        "capture-flow rehearsal",
        "librarian capture-return",
        "librarian boot",
        "librarian batch-observe",
    }
    if routes != expected_routes:
        fail("status-writer-routes", {"routes": sorted(routes)})
    findings = status["detail"].get("incomplete_findings")
    witness = None
    if isinstance(findings, list):
        for item in findings:
            if item.get("completed_by_this_tool") is True:
                fail("status-completed-finding", item)
            if item.get("member") == "0154.colab-support-first-0501":
                witness = item
    if witness is None:
        extra = status["detail"].get("incomplete_witness")
        if not isinstance(extra, dict) or extra.get("present_in_index") is not False or extra.get("completed_by_this_tool") is not False:
            fail("status-0154-witness", {"findings": findings, "witness": extra})
    elif witness.get("state") == "complete":
        fail("status-0154-complete", witness)
    ok("status-migrated", {"writers": len(writers), "witness": witness or status["detail"].get("incomplete_witness")})
    empty = ROOT / "empty-book"
    empty.mkdir()
    bare = expect_access(["status", "--book", str(empty)], "status-no-layout", 0, "reported")
    if "layout" not in (bare.get("missing") or []) or bare["detail"]["authority"].get("established") is not False:
        fail("status-no-layout-shape", {"missing": bare.get("missing"), "authority": bare["detail"].get("authority")})
    ok("status-no-layout")
    expect_stop(["stage", "--book", str(BOOK)], "door-stage", "command is not on this door")
    expect_stop(["status", "--book", str(BOOK), "--backend", "other"], "door-backend", "backend override is refused")
    link = ROOT / "junction-book"
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(BOOK)], capture_output=True)
    (CMD / "mklink.out").write_bytes(proc.stdout)
    (CMD / "mklink.err").write_bytes(proc.stderr)
    if proc.returncode != 0:
        fail("junction-create", {"code": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")[:500]})
    expect_stop(["status", "--book", str(link)], "door-junction", "book root is not a directory")
    before = (LIVE / "return-line-layout.json").exists()
    expect_stop(["reserve", "--book", str(LIVE)], "door-live", "canonical live book is refused")
    if before or (LIVE / "return-line-layout.json").exists():
        fail("live-layout", {"before": before, "after": True})
    ok("live-book-unwritten")


def pin_file(rel: str, digest: str, size: int, name: str) -> None:
    path = REPO / rel
    data = path.read_bytes()
    if sha(data) != digest or len(data) != size:
        fail(name, {"path": rel, "sha256": sha(data), "bytes": len(data)})


def walk_specs(document: object, label: str) -> None:
    if isinstance(document, dict) and {"path", "sha256", "bytes"} <= set(document):
        pin_file(document["path"], document["sha256"], document["bytes"], label)
        return
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, dict):
                walk_specs(value, f"{label}-{key}")


def check_pins() -> None:
    for rel, (digest, size) in PINS.items():
        pin_file(rel, digest, size, f"pin-{rel}")
    librarian = (REPO / "app" / "librarian.py").read_text(encoding="utf-8")
    for snippet in (
        'authoring_tools_v2.py", "librarian_authoring_tools_v2"',
        'review_loop_tools_v4.py", "librarian_review_loop_tools_v4"',
        'return_line_tools_v2.py", "librarian_return_line_tools_v2"',
    ):
        if snippet not in librarian:
            fail("dispatch-pin", {"missing": snippet})
    adapter = (REPO / "labs" / "return-access-pass01" / "return_access.py").read_text(encoding="utf-8")
    if "return-lines-pass04" in adapter or "pass04" in adapter:
        fail("pass04-import", {"error": "adapter names the unfinished successor"})
    ok("pass04-not-consumed", {"directory_present": (REPO / "labs" / "return-lines-pass04").exists()})
    declaration = json.loads((REPO / "app" / "return-lines-v2.json").read_text(encoding="utf-8"))
    if declaration["adapter"]["sha256"] != PINS["labs/return-access-pass01/return_access.py"][0]:
        fail("declaration-adapter", declaration["adapter"])
    walk_specs(json.loads((REPO / "app" / "authoring-v2.json").read_text(encoding="utf-8")), "authoring")
    walk_specs(json.loads((REPO / "app" / "review-loop-v4.json").read_text(encoding="utf-8")), "review")
    before = REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "evidence" / "build05.07" / "before" / "librarian.py"
    data = before.read_bytes()
    if sha(data) != "3f9dbfec25f71b4b3e0845d367d1d08138854bc1862b3b5b150aa6ce9250bc22" or len(data) != 11581:
        fail("before-librarian", {"sha256": sha(data), "bytes": len(data)})
    readme = (REPO / "00.kernel" / "00.00.10.work" / "0521.return-placement" / "evidence" / "build05.07" / "before" / "README.md").read_bytes()
    if sha(readme) != "82f839d211e1e4471f89cbc53f04b427d2929b9e67f139f4edd228925415355c" or len(readme) != 35626:
        fail("before-readme", {"sha256": sha(readme), "bytes": len(readme)})
    ok("bounded-pins", {"files": len(PINS)})


def main() -> None:
    global ROOT, BOOK, RETIRED, BACKUP, CMD
    if (LIVE / "return-line-layout.json").exists():
        raise SystemExit("live book already has return-line-layout.json; refusing to run")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ROOT = BASE / stamp
    if ROOT.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        ROOT = BASE / stamp
    BOOK = ROOT / "book"
    BACKUP = ROOT / "backup"
    RETIRED = ROOT / "retired"
    CMD = ROOT / "commands"
    for path in (BOOK, BACKUP, ROOT / "staging", RETIRED, CMD):
        path.mkdir(parents=True)
    print(f"root {ROOT}", flush=True)
    raw_layout = layout_bytes()
    if sha(raw_layout) != LAYOUT_SHA or len(raw_layout) != LAYOUT_BYTES:
        fail("layout-pin", {"sha256": sha(raw_layout), "bytes": len(raw_layout)})
    ok("layout-pin")
    audit_body = filtered_audit()
    if len(audit_body["records"]) != len(MEMBERS):
        fail("audit-records", {"count": len(audit_body["records"])})
    audit = ROOT / "audit.json"
    audit.write_bytes(dump(audit_body))
    before = seed(audit_body)
    plan = ROOT / "plan.json"
    proc = run("pass03", ["plan", "--book", str(BOOK), "--audit", str(audit), "--out", str(plan)], "producer-plan")
    planned = as_json(proc, "producer-plan")
    if proc.returncode != 0 or not plan.is_file() or planned.get("state") != "incomplete" or planned.get("detail", {}).get("live_moves") is not False:
        fail("producer-plan", {"code": proc.returncode, "state": planned.get("state"), "correction": planned.get("correction"), "detail": planned.get("detail")})
    ok("producer-plan", {"bytes": planned.get("detail", {}).get("bytes"), "occupancy_conflict_count": planned.get("detail", {}).get("occupancy_conflict_count")})
    write_fixture(audit, plan)
    migrate(audit, plan)
    check_historical(before)
    hashes = check_filings()
    check_refusals(hashes["filing-0521-0501"])
    check_status_and_door()
    check_pins()
    summary = {
        "schema": "return-access-entry-run/1",
        "root": str(ROOT),
        "cases": len(CASES),
        "failed": 0,
        "first_failure": None,
        "live_layout_written": (LIVE / "return-line-layout.json").exists(),
    }
    (ROOT / "summary.json").write_bytes(dump(summary))
    print(f"summary {json.dumps(summary)}", flush=True)


if __name__ == "__main__":
    main()
