"""Disposable fixture proof for 0504.app-entry/05.16.

This file is retained evidence. It is not an adapter, not app wiring, and
not a second capture implementation. It composes the pinned CLIs with
subprocess argument arrays and records what those tools actually do.
A successful sequence in this file is not the proposed guard.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


REPO = Path(r"D:\Git\lib-build")
EVIDENCE = REPO / "00.kernel" / "00.00.10.work" / "0504.app-entry" / "evidence" / "capture-hand05.16"
CLERK = REPO / "labs" / "clerk-handoff-pass02" / "clerk.py"
CAPTURE = REPO / "labs" / "return-capture-pass01" / "return_capture.py"
INSPECT = REPO / "labs" / "return-capture-pass01" / "return_inspect.py"
PINS = {
    CLERK: ("f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c", 52279),
    CAPTURE: ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
    INSPECT: ("947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", 11402),
}
ORIGIN = ("00.00.10.work", "0504.app-entry", "05.16")
RELEASE = "Reservation only; fixture label, not a Director release."
JOB_RELEASE = "fixture job label; not a release"
EVIDENCE_LINE = "transport line only"
DELIVERY = "fixture-delivery"
ASSIGNEE = "fixture-builder"
REVIEWER = "fixture-reviewer"

INSTRUCTIONS = b"Fixture instructions for 05.16. Not a job execution.\n"
PIECE = b"fixture piece bytes\n"
REPORT = (
    b"# Fixture final report\n"
    b"This file is the builder report.\n"
    b"The transport record is a different field.\n"
)
DIRTY_SUFFIX = b"mutated\n"
CLAIMED_PIECE = b"claimed piece bytes\n"
CLAIMED_REPORT = b"# Claimed fixture report\nThis job was not returned.\n"
OUTSIDE_REPORT = (
    b"# Outside report\n"
    b"The capture tool may copy this absolute file.\n"
    b"The proposed adapter would refuse it.\n"
)
OTHER_REPORT = b"# Different report bytes\nThis must not replace the captured report.\n"
PARTIAL = b"partial-planted\n"
LINK_BYTES = b"hardlink piece bytes\n"
JUNCTION_BYTES = b"junction target bytes\n"
SYMLINK_BYTES = b"symlink target bytes\n"
ESCAPE_BYTES = b"should-not-be-captured\n"

STEPS: list[dict] = []
CASES: list[dict] = []
JUNCTIONS: list[Path] = []
SYMLINKS: list[Path] = []
FAILURE: str | None = None


class Stop(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def git_ancestor(path: Path) -> Path | None:
    current = path
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def pins() -> dict:
    observed = {}
    for path, (digest, size) in PINS.items():
        data = path.read_bytes()
        actual = sha256_bytes(data)
        observed[str(path.relative_to(REPO)).replace("\\", "/")] = {
            "sha256": actual,
            "bytes": len(data),
            "matches": actual == digest and len(data) == size,
        }
        if actual != digest or len(data) != size:
            raise Stop(f"pin mismatch {path.name}")
    return observed


def normalize(data: bytes) -> str:
    return data.decode("utf-8").replace("\r\n", "\n")


def run(step_id: str, script: Path, args: list[str], exit_code: int, contains=(), absent=(), label="", enforced=None, adapter=None) -> str:
    argv = [sys.executable, "-B", str(script), *args]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(
        argv,
        cwd=str(REPO),
        env=env,
        capture_output=True,
        shell=False,
        timeout=60,
    )
    text = normalize(proc.stdout)
    err = normalize(proc.stderr)
    step = {
        "id": step_id,
        "argv": argv,
        "shell": False,
        "exit": proc.returncode,
        "stdout_sha256": sha256_bytes(proc.stdout),
        "stdout_bytes": len(proc.stdout),
        "stdout_crlf": b"\r\n" in proc.stdout,
        "stdout_text": text,
        "stderr_text": err,
        "label": label,
        "enforced_by_current_tools": enforced,
        "adapter_expectation": adapter,
    }
    STEPS.append(step)
    problems = []
    if proc.returncode != exit_code:
        problems.append(f"exit {proc.returncode} != {exit_code}")
    for item in contains:
        if item not in text:
            problems.append("missing text " + item)
    for item in absent:
        if item in text:
            problems.append("unexpected text " + item)
    if problems:
        step["problems"] = problems
        raise Stop(step_id + ": " + "; ".join(problems))
    print(f"{step_id} exit {proc.returncode}", flush=True)
    return text


def parse_json(step_id: str, text: str) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise Stop(f"{step_id}: json {exc}") from exc
    if not isinstance(value, dict):
        raise Stop(f"{step_id}: json is not an object")
    STEPS[-1]["json"] = value
    return value


def one(text: str, prefix: str) -> str:
    found = [line[len(prefix):] for line in text.splitlines() if line.startswith(prefix)]
    if len(found) != 1:
        raise Stop(f"expected one {prefix!r}, found {found!r}")
    return found[0]


def member_listing(path: Path) -> list[str]:
    names = []
    for dirpath, dirnames, filenames in os.walk(path):
        base = Path(dirpath)
        for name in dirnames + filenames:
            names.append((base / name).relative_to(path).as_posix())
    return sorted(names)


def reserve(step_id: str, book: Path, submission: str, name: str, expected: str) -> str:
    text = run(
        step_id,
        CAPTURE,
        [
            "reserve",
            "--book", str(book),
            "--submission", submission,
            "--name", name,
            "--origin-book", ORIGIN[0],
            "--origin-page", ORIGIN[1],
            "--origin-batch", ORIGIN[2],
            "--expected-output", expected,
            "--submitter", "Grok Builder 1",
            "--reviewer", "Codex Prime",
            "--release", RELEASE,
        ],
        0,
        contains=("result reserved", "submission " + submission),
        label="fixture reserve in the disposable book",
        enforced=True,
    )
    return one(text, "member ")


def capture(step_id: str, book: Path, submission: str, return_file: Path, root: Path, artifact: str, exit_code: int, contains=(), absent=(), label="", enforced=None, adapter=None) -> str:
    return run(
        step_id,
        CAPTURE,
        [
            "capture",
            "--book", str(book),
            "--submission", submission,
            "--return-file", str(return_file),
            "--source-root", str(root),
            "--artifact", artifact,
        ],
        exit_code,
        contains=contains,
        absent=absent,
        label=label,
        enforced=enforced,
        adapter=adapter,
    )


def inspect(step_id: str, book: Path, member: str, exit_code: int, label: str) -> dict:
    text = run(
        step_id,
        INSPECT,
        ["inspect", "--book", str(book), "--member", member, "--json"],
        exit_code,
        label=label,
        enforced=True,
    )
    return parse_json(step_id, text)


def verify(step_id: str, book: Path, member: str) -> str:
    return run(
        step_id,
        CAPTURE,
        ["verify", "--book", str(book), "--member", member],
        0,
        contains=("result complete", "not approved", "not accepted", "not published"),
        label="verify is custody, not acceptance",
        enforced=True,
    )


def show(step_id: str, store: Path, job: str, base: Path | None, exit_code: int, label: str, enforced, adapter) -> dict:
    args = ["show", "--store", str(store), "--job", job, "--json"]
    if base is not None:
        args.extend(["--instructions-base", str(base)])
    text = run(step_id, CLERK, args, exit_code, label=label, enforced=enforced, adapter=adapter)
    return parse_json(step_id, text)


def job_file(path: Path, job_id: str, digest: str) -> None:
    body = {
        "assignee": ASSIGNEE,
        "expected_outputs": ["piece.txt"],
        "instructions": {"path": "task.txt", "sha256": digest},
        "job_id": job_id,
        "release": JOB_RELEASE,
        "reviewer": REVIEWER,
        "routed_by": "fixture-router",
    }
    write_bytes(path, (json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))


def event_hash(store: Path, job: str) -> str:
    path = store / "jobs" / job / "0003.returned.json"
    return sha256_bytes(path.read_bytes())


def assert_reserved_only(path: Path) -> None:
    names = member_listing(path)
    if names != ["01.md", "reservation.json"]:
        raise Stop(f"{path.name} listing {names}")


def add_case(case_id: str, adapter: str, enforced: bool | None, observed: str, detail: str) -> None:
    CASES.append({
        "id": case_id,
        "adapter_expectation": adapter,
        "enforced_by_current_tools": enforced,
        "observed": observed,
        "detail": detail,
    })


def cleanup(root: Path | None) -> None:
    for path in SYMLINKS:
        if os.path.lexists(path):
            os.remove(path)
    for path in JUNCTIONS:
        if os.path.lexists(path):
            os.rmdir(path)
    if root is not None and os.path.lexists(root):
        shutil.rmtree(root)


def write_proof(header: dict) -> None:
    document = {
        "schema": "capture-hand05.16-proof/1",
        "kind": "disposable-fixture",
        "not_an_adapter": True,
        "hand_composed_capture_is_not_the_guard": True,
        "double_read_raced": False,
        "header": header,
        "cases": CASES,
        "steps": STEPS,
        "failure": FAILURE,
    }
    payload = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    (EVIDENCE / "proof.json").write_bytes(payload.encode("utf-8"))
    lines = [
        "# capture-hand05.16 disposable proof",
        "# This transcript composes pinned tools. It does not implement the adapter guard.",
        "# The bytes-changed-before-capture race was not reproduced.",
        "",
    ]
    if FAILURE:
        lines.extend(["# FAILURE", FAILURE, ""])
    for step in STEPS:
        lines.append("## " + step["id"])
        lines.append("exit " + str(step.get("exit")))
        lines.append("stdout_sha256 " + str(step.get("stdout_sha256")))
        lines.append("stdout_crlf " + str(step.get("stdout_crlf")))
        lines.append("label " + str(step.get("label")))
        lines.append("enforced_by_current_tools " + str(step.get("enforced_by_current_tools")))
        lines.append("adapter_expectation " + str(step.get("adapter_expectation")))
        if step.get("problems"):
            lines.append("problems " + " | ".join(step["problems"]))
        lines.append("--- stdout ---")
        lines.append(step.get("stdout_text", "").rstrip("\n"))
        if step.get("stderr_text"):
            lines.append("--- stderr ---")
            lines.append(step["stderr_text"].rstrip("\n"))
        lines.append("")
    lines.append("## cases")
    lines.append(json.dumps(CASES, ensure_ascii=False, indent=2))
    lines.append("")
    text = "\n".join(lines)
    (EVIDENCE / "proof.txt").write_bytes(text.replace("\n", "\r\n").encode("utf-8"))


def fixture(pin_report: dict) -> dict:
    root = Path(tempfile.mkdtemp(prefix="handoff0516-"))
    try:
        if git_ancestor(root) is not None or str(root).casefold().startswith(str(REPO).casefold()):
            raise Stop("temp root is inside a Git working tree or the live checkout")
        instructions = root / "instructions"
        source = root / "source"
        book = root / "book"
        jobs = root / "jobs"
        store = root / "clerk-store"
        outside = root / "outside-report"
        target = root / "junction-target"
        for path in (instructions, source, book, jobs, outside, target):
            path.mkdir(parents=True)
        write_bytes(instructions / "task.txt", INSTRUCTIONS)
        digest = sha256_bytes(INSTRUCTIONS)
        write_bytes(source / "piece.txt", PIECE)
        write_bytes(source / "final-report.md", REPORT)
        write_bytes(outside / "final-report.md", OUTSIDE_REPORT)
        write_bytes(root / "outside.txt", ESCAPE_BYTES)
        write_bytes(target / "piece.txt", JUNCTION_BYTES)
        mismatch = {
            "schema": "clerk-capture-handoff/1",
            "kind": "side-document",
            "origin": {"book": ORIGIN[0], "page": ORIGIN[1], "batch": "05.99"},
            "note": "No pinned command in this proof receives this file.",
        }
        mismatch_path = root / "binding-mismatch.json"
        write_bytes(mismatch_path, (json.dumps(mismatch, indent=2) + "\n").encode("utf-8"))
        happy_job = jobs / "fixture-0516.json"
        claimed_job = jobs / "fixture-claimed.json"
        job_file(happy_job, "fixture-0516", digest)
        job_file(claimed_job, "fixture-claimed", digest)

        run(
            "queue-happy",
            CLERK,
            ["queue", "--store", str(store), "--job", str(happy_job), "--instructions-base", str(instructions)],
            0,
            contains=("queued fixture-0516", "result ok"),
            label="fixture queue",
            enforced=True,
        )
        claim_text = run(
            "claim-happy",
            CLERK,
            ["claim", "--store", str(store), "--job", "fixture-0516", "--as", ASSIGNEE, "--instructions-base", str(instructions)],
            0,
            contains=("claimed fixture-0516", "result ok", "instructions-usable sha256=" + digest),
            label="fixture claim",
            enforced=True,
        )
        token = one(claim_text, "token ")
        write_bytes(store / "jobs" / "fixture-0516" / "outbox" / "piece.txt", PIECE)
        returned = run(
            "return-happy",
            CLERK,
            ["return", "--store", str(store), "--job", "fixture-0516", "--as", ASSIGNEE, "--claim", token, "--delivery", DELIVERY, "--evidence", EVIDENCE_LINE],
            0,
            contains=("returned fixture-0516", "delivery " + DELIVERY, "result ok"),
            label="fixture return records the transport line, not the builder report",
            enforced=True,
        )
        event = one(returned, "event 0003.returned.json sha256=")
        if event_hash(store, "fixture-0516") != event:
            raise Stop("returned event file hash differs from the printed event sha256")
        artifact_line = one(returned, "artifact piece.txt ")
        piece_sha = sha256_bytes(PIECE)
        if f"sha256={piece_sha} bytes={len(PIECE)}" not in artifact_line:
            raise Stop("returned artifact line does not match piece bytes")
        if EVIDENCE_LINE.encode("utf-8") in REPORT or DELIVERY.encode("utf-8") in REPORT:
            raise Stop("fixture report accidentally contains the transport record")

        clean = show(
            "show-happy-json",
            store,
            "fixture-0516",
            instructions,
            0,
            "clean returned inspection is schema clerk-handoff-inspection/2",
            True,
            "require this shape before capture",
        )
        if clean.get("schema") != "clerk-handoff-inspection/2":
            raise Stop("inspection schema")
        if clean.get("state") != "returned" or clean.get("returned") is None:
            raise Stop("clean show is not returned")
        if clean["returned"].get("event_sha256") != event:
            raise Stop("json event_sha256 differs")
        if clean["returned"].get("delivery") != DELIVERY or clean["returned"].get("evidence") != EVIDENCE_LINE:
            raise Stop("transport fields were not preserved on the inspection")
        if clean["returned"].get("by") != ASSIGNEE:
            raise Stop("returned.by differs")
        if clean["checks"] != {"events": "ok", "completion": "ok", "artifacts": "ok", "instructions": "usable"}:
            raise Stop("clean checks " + json.dumps(clean["checks"]))
        if clean.get("problems") != []:
            raise Stop("clean problems are not empty")
        artifacts = clean["returned"].get("artifacts")
        if artifacts != [{"bytes": len(PIECE), "path": "piece.txt", "sha256": piece_sha}]:
            raise Stop("returned artifacts " + json.dumps(artifacts))
        run(
            "show-happy-text",
            CLERK,
            ["show", "--store", str(store), "--job", "fixture-0516", "--instructions-base", str(instructions)],
            0,
            contains=("state returned", "instructions-usable sha256=" + digest),
            absent=("not-returned-clean",),
            label="human show of a clean return",
            enforced=True,
        )
        unchecked = show(
            "show-happy-no-base",
            store,
            "fixture-0516",
            None,
            0,
            "exit 0 with instructions not-checked is not a clean handoff for the adapter",
            False,
            "refuse before capture",
        )
        if unchecked["checks"].get("instructions") != "not-checked" or unchecked.get("problems") != []:
            raise Stop("unchecked instructions projection differs")
        add_case(
            "instructions-not-checked",
            "refuse before capture",
            False,
            "show --json without a base exits 0, state returned, instructions not-checked, problems empty",
            "The tool exit is not the adapter guard.",
        )
        before_names = sorted(os.listdir(store / "jobs" / "fixture-0516"))
        before_event = event_hash(store, "fixture-0516")
        run(
            "return-already-recorded",
            CLERK,
            ["return", "--store", str(store), "--job", "fixture-0516", "--as", ASSIGNEE, "--claim", token, "--delivery", DELIVERY, "--evidence", EVIDENCE_LINE],
            0,
            contains=("already-recorded fixture-0516", "delivery " + DELIVERY, "result ok"),
            label="identical return writes nothing",
            enforced=True,
        )
        if sorted(os.listdir(store / "jobs" / "fixture-0516")) != before_names or event_hash(store, "fixture-0516") != before_event:
            raise Stop("already-recorded changed the job directory or event hash")

        happy = reserve("reserve-happy", book, "fixture-happy", "happy", "piece.txt")
        reserved_doc = inspect("inspect-happy-reserved", book, happy, 1, "reserved inspection exits 1 and is not acceptance")
        if reserved_doc.get("schema") != "return-capture-inspection/1" or reserved_doc.get("status") != "reserved":
            raise Stop("reserved inspection status")
        if reserved_doc.get("capture") is not None or reserved_doc.get("problems") != ["reservation only"]:
            raise Stop("reserved inspection body")
        origin = reserved_doc["reservation"]["origin"]
        if (origin.get("book"), origin.get("page"), origin.get("batch")) != ORIGIN:
            raise Stop("reserved origin differs")
        if reserved_doc["reservation"].get("expected_outputs") != ["piece.txt"]:
            raise Stop("reserved outputs differ")
        if reserved_doc["reservation"].get("release") != RELEASE:
            raise Stop("stored release text differs")
        captured = capture(
            "capture-happy",
            book,
            "fixture-happy",
            source / "final-report.md",
            source,
            "piece.txt|piece.txt",
            0,
            contains=("result captured",),
            label="happy capture copies the named report and artifact; it does not read Clerk",
            enforced=True,
            adapter="call capture only after the binding checks",
        )
        receipt = one(captured, "receipt ")
        manifest = one(captured, "manifest ")
        verified = verify("verify-happy", book, happy)
        if one(verified, "receipt ") != receipt or one(verified, "manifest ") != manifest:
            raise Stop("verify hashes differ from capture stdout")
        if one(verified, "payload 0001.blob ") != piece_sha:
            raise Stop("payload hash differs from piece bytes")
        member = book / happy
        return_bytes = (member / "return.md").read_bytes()
        payload_bytes = (member / "payload" / "0001.blob").read_bytes()
        if return_bytes != REPORT or payload_bytes != PIECE:
            raise Stop("captured bytes were not preserved")
        if EVIDENCE_LINE.encode("utf-8") in return_bytes or DELIVERY.encode("utf-8") in return_bytes:
            raise Stop("return.md contains the transport record")
        complete = inspect("inspect-happy-complete", book, happy, 0, "complete inspection exits 0 and does not approve")
        if complete.get("status") != "complete" or complete.get("problems") != []:
            raise Stop("complete inspection status")
        viewed = complete["capture"]["return"]
        if viewed.get("sha256") != sha256_bytes(REPORT) or viewed.get("includes_prime_review") is not False:
            raise Stop("complete return view differs")
        if complete["capture"].get("retrospective") is not False or complete["capture"].get("source_commit") is not None:
            raise Stop("complete capture flags differ")
        if complete["reservation"]["origin"].get("batch") != "05.16":
            raise Stop("complete origin batch differs")
        if "05.99" in captured:
            raise Stop("happy capture stdout unexpectedly contains the side batch")
        add_case(
            "mismatched-origin",
            "refuse before capture",
            False,
            "side file batch 05.99 was not passed to any command; inspect origin.batch stayed 05.16; capture has no origin argument",
            "A hand-composed capture does not read that side file. The tool success is not the guard.",
        )
        again = capture(
            "capture-happy-again",
            book,
            "fixture-happy",
            source / "final-report.md",
            source,
            "piece.txt|piece.txt",
            0,
            contains=("result already-captured",),
            label="identical second capture writes nothing",
            enforced=True,
        )
        if one(again, "receipt ") != receipt:
            raise Stop("already-captured printed a different receipt")
        if sha256_bytes((member / "receipt.json").read_bytes()) != receipt:
            raise Stop("receipt file hash changed after already-captured")

        mutated = PIECE + DIRTY_SUFFIX
        write_bytes(store / "jobs" / "fixture-0516" / "outbox" / "piece.txt", mutated)
        if event_hash(store, "fixture-0516") != event:
            raise Stop("outbox mutation changed the returned event file")
        dirty = show(
            "show-dirty-json",
            store,
            "fixture-0516",
            instructions,
            1,
            "dirty outbox keeps event_sha256 and exits 1",
            True,
            "refuse before capture",
        )
        if dirty["returned"].get("event_sha256") != event:
            raise Stop("dirty inspection changed event_sha256")
        if dirty["checks"].get("artifacts") != "changed":
            raise Stop("dirty artifacts check")
        kinds = [item.get("kind") for item in dirty.get("problems", [])]
        if "artifact-changed" not in kinds:
            raise Stop("dirty problems " + json.dumps(kinds))
        run(
            "show-dirty-text",
            CLERK,
            ["show", "--store", str(store), "--job", "fixture-0516", "--instructions-base", str(instructions)],
            1,
            contains=("not-returned-clean", "artifact changed", "result findings"),
            label="human show names not-returned-clean",
            enforced=True,
        )
        run(
            "return-delivery-conflict",
            CLERK,
            ["return", "--store", str(store), "--job", "fixture-0516", "--as", ASSIGNEE, "--claim", token, "--delivery", DELIVERY, "--evidence", EVIDENCE_LINE],
            2,
            contains=("refused: delivery conflict", "result refused"),
            label="same delivery id with changed artifact bytes writes nothing",
            enforced=True,
        )
        run(
            "return-delivery-conflict-evidence",
            CLERK,
            ["return", "--store", str(store), "--job", "fixture-0516", "--as", ASSIGNEE, "--claim", token, "--delivery", DELIVERY, "--evidence", "transport line changed"],
            2,
            contains=("refused: delivery conflict", "result refused"),
            label="same delivery id with different evidence writes nothing",
            enforced=True,
        )
        if event_hash(store, "fixture-0516") != event:
            raise Stop("delivery conflict rewrote the returned event")
        same_after_dirty = capture(
            "capture-happy-after-dirty-outbox",
            book,
            "fixture-happy",
            source / "final-report.md",
            source,
            "piece.txt|piece.txt",
            0,
            contains=("result already-captured",),
            label="the original source bytes are unchanged, so the tool still reports already-captured",
            enforced=True,
            adapter="a new capture of the dirty bytes is a different request and must be refused",
        )
        if one(same_after_dirty, "receipt ") != receipt:
            raise Stop("receipt changed after the dirty outbox")
        write_bytes(source / "piece-dirty.txt", mutated)
        dirty_member = reserve("reserve-dirty", book, "fixture-dirty", "dirty", "piece.txt")
        dirty_capture = capture(
            "capture-dirty",
            book,
            "fixture-dirty",
            source / "final-report.md",
            source,
            "piece-dirty.txt|piece.txt",
            0,
            contains=("result captured",),
            label="GAP: capture copies the mutated bytes because it does not read the Clerk event",
            enforced=False,
            adapter="refuse before capture",
        )
        dirty_payload = sha256_bytes((book / dirty_member / "payload" / "0001.blob").read_bytes())
        if dirty_payload == piece_sha or dirty_payload != sha256_bytes(mutated):
            raise Stop("dirty payload hash was not the mutated bytes")
        verify("verify-dirty", book, dirty_member)
        add_case(
            "dirty-artifact",
            "refuse before capture",
            False,
            "show exits 1 with artifact-changed and the same event_sha256; a new member capture still exits 0 and stores the mutated payload",
            "The capture command does not compare payload bytes to returned.artifacts. Its success is not the guard.",
        )
        del dirty_capture

        run(
            "queue-claimed",
            CLERK,
            ["queue", "--store", str(store), "--job", str(claimed_job), "--instructions-base", str(instructions)],
            0,
            contains=("queued fixture-claimed", "result ok"),
            label="second fixture job",
            enforced=True,
        )
        run(
            "claim-claimed",
            CLERK,
            ["claim", "--store", str(store), "--job", "fixture-claimed", "--as", ASSIGNEE, "--instructions-base", str(instructions)],
            0,
            contains=("claimed fixture-claimed", "result ok"),
            label="claim without return",
            enforced=True,
        )
        write_bytes(store / "jobs" / "fixture-claimed" / "outbox" / "piece.txt", CLAIMED_PIECE)
        claimed_doc = show(
            "show-claimed-json",
            store,
            "fixture-claimed",
            instructions,
            0,
            "claimed projection has returned null",
            True,
            "refuse before capture",
        )
        if claimed_doc.get("state") != "claimed" or claimed_doc.get("returned") is not None:
            raise Stop("claimed projection is not claimed")
        if claimed_doc["checks"].get("completion") != "not-applicable" or claimed_doc["checks"].get("artifacts") != "not-applicable":
            raise Stop("claimed checks differ")
        write_bytes(source / "claimed-piece.txt", CLAIMED_PIECE)
        write_bytes(source / "claimed-report.md", CLAIMED_REPORT)
        claimed_member = reserve("reserve-claimed", book, "fixture-claimed", "claimed", "claimed-piece.txt")
        capture(
            "capture-claimed",
            book,
            "fixture-claimed",
            source / "claimed-report.md",
            source,
            "claimed-piece.txt|claimed-piece.txt",
            0,
            contains=("result captured",),
            label="GAP: capture does not read the claimed Clerk job",
            enforced=False,
            adapter="refuse before capture",
        )
        verify("verify-claimed", book, claimed_member)
        add_case(
            "claimed-not-returned",
            "refuse before capture",
            False,
            "show state is claimed and returned is null; a separate capture still exits 0",
            "The capture command has no Clerk argument. Its success is not the guard.",
        )

        partial_member = reserve("reserve-partial", book, "fixture-partial", "partial", "piece.txt")
        write_bytes(book / partial_member / "return.md", PARTIAL)
        capture(
            "capture-partial",
            book,
            "fixture-partial",
            source / "final-report.md",
            source,
            "piece.txt|piece.txt",
            2,
            contains=("partial " + partial_member, "retained return.md", "result refused"),
            absent=("result captured",),
            label="planted partial member stays partial; the CLI has no interrupt flag",
            enforced=True,
            adapter="stop, keep retained bytes, do not allocate another member",
        )
        if (book / partial_member / "return.md").read_bytes() != PARTIAL:
            raise Stop("partial return.md was rewritten")
        partial_names = member_listing(book / partial_member)
        if "receipt.json" in partial_names or "manifest.json" in partial_names or "payload" in partial_names:
            raise Stop("partial member gained capture files " + json.dumps(partial_names))
        partial_doc = inspect("inspect-partial", book, partial_member, 2, "incomplete inspection exits 2")
        if partial_doc.get("status") != "incomplete" or "missing manifest.json" not in partial_doc.get("problems", []):
            raise Stop("partial inspection " + json.dumps(partial_doc.get("problems")))
        add_case(
            "partial-capture",
            "stop, keep retained bytes, do not allocate another member",
            True,
            "planted return.md was retained, capture wrote nothing, inspect status is incomplete",
            "The plant is a fixture. interrupt is not a CLI flag. The refusal is the tool's partial behavior.",
        )

        escape_member = reserve("reserve-escape", book, "fixture-escape", "escape", "piece.txt")
        capture(
            "capture-escape",
            book,
            "fixture-escape",
            source / "final-report.md",
            source,
            "../outside.txt|piece.txt",
            2,
            contains=("artifact path has an unsafe segment", "result refused"),
            absent=("result captured",),
            label="path escape is refused before a write",
            enforced=True,
        )
        assert_reserved_only(book / escape_member)
        add_case(
            "path-escape",
            "refuse",
            True,
            "capture refused artifact path has an unsafe segment and left the member reserved",
            "The tool walks the declared relative path and rejects ..",
        )

        write_bytes(source / "plain-piece.txt", LINK_BYTES)
        os.link(source / "plain-piece.txt", source / "linked.txt")
        hard_member = reserve("reserve-hardlink", book, "fixture-hardlink", "hardlink", "linked.txt")
        capture(
            "capture-hardlink",
            book,
            "fixture-hardlink",
            source / "final-report.md",
            source,
            "linked.txt|linked.txt",
            2,
            contains=("link-count: linked.txt", "result refused"),
            absent=("result captured",),
            label="hard link is refused and is not copied",
            enforced=True,
        )
        assert_reserved_only(book / hard_member)
        add_case(
            "hardlink",
            "refuse and do not follow",
            True,
            "capture refused link-count: linked.txt and left the member reserved",
            "plain_file_problem requires link count one",
        )

        linkdir = source / "linkdir"
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(linkdir), str(target)],
            capture_output=True,
            shell=False,
            timeout=30,
        )
        if completed.returncode != 0:
            raise Stop("junction create failed " + completed.stderr.decode("utf-8", errors="backslashreplace"))
        JUNCTIONS.append(linkdir)
        junction_member = reserve("reserve-junction", book, "fixture-junction", "junction", "piece.txt")
        junction_text = capture(
            "capture-junction",
            book,
            "fixture-junction",
            source / "final-report.md",
            source,
            "linkdir/piece.txt|piece.txt",
            2,
            contains=("link:", "result refused"),
            absent=("result captured",),
            label="junction is refused and is not followed",
            enforced=True,
        )
        if "junction target bytes" in junction_text:
            raise Stop("junction target text appeared in the refusal")
        assert_reserved_only(book / junction_member)
        add_case(
            "junction",
            "refuse and do not follow",
            True,
            "capture refused link: on the junction segment and left the member reserved",
            "The reparse point is not followed.",
        )

        symlink_path = source / "sym-piece.txt"
        write_bytes(source / "sym-target.txt", SYMLINK_BYTES)
        try:
            os.symlink(source / "sym-target.txt", symlink_path)
        except OSError as exc:
            winerror = getattr(exc, "winerror", None)
            if winerror != 1314:
                raise Stop(f"symlink create failed winerror {winerror}: {exc}") from exc
            add_case(
                "file-symlink",
                "refuse and do not follow",
                None,
                "skipped",
                "File symlink creation returned WinError 1314. The tool was not asked to follow one.",
            )
        else:
            SYMLINKS.append(symlink_path)
            sym_member = reserve("reserve-symlink", book, "fixture-symlink", "symlink", "sym-piece.txt")
            capture(
                "capture-symlink",
                book,
                "fixture-symlink",
                source / "final-report.md",
                source,
                "sym-piece.txt|sym-piece.txt",
                2,
                contains=("link:", "result refused"),
                absent=("result captured",),
                label="file symlink is refused and is not followed",
                enforced=True,
            )
            assert_reserved_only(book / sym_member)
            add_case(
                "file-symlink",
                "refuse and do not follow",
                True,
                "capture refused link: and left the member reserved",
                "The symlink was not followed.",
            )

        outside_member = reserve("reserve-outside", book, "fixture-outside", "outside", "piece.txt")
        outside_capture = capture(
            "capture-outside",
            book,
            "fixture-outside",
            outside / "final-report.md",
            source,
            "piece.txt|piece.txt",
            0,
            contains=("result captured",),
            label="GAP: the tool accepts a return file outside the source root",
            enforced=False,
            adapter="refuse",
        )
        outside_return = (book / outside_member / "return.md").read_bytes()
        if outside_return != OUTSIDE_REPORT:
            raise Stop("outside report bytes were not copied whole")
        try:
            (outside / "final-report.md").resolve().relative_to(source.resolve())
            outside_inside = True
        except ValueError:
            outside_inside = False
        if outside_inside:
            raise Stop("outside report resolved inside the source root")
        verify("verify-outside", book, outside_member)
        add_case(
            "report-outside-source-root",
            "refuse",
            False,
            "capture exit 0 copied the absolute return file that is outside source_root",
            "The proposed adapter keeps the report under source_root. The tool does not. This success is not the guard.",
        )
        del outside_capture

        write_bytes(source / "other-report.md", OTHER_REPORT)
        capture(
            "capture-changed-report",
            book,
            "fixture-happy",
            source / "other-report.md",
            source,
            "piece.txt|piece.txt",
            2,
            contains=("conflict submission fixture-happy", "existing " + happy, "result refused"),
            absent=("result captured",),
            label="changed return bytes on a complete member write nothing",
            enforced=True,
        )
        if (member / "return.md").read_bytes() != REPORT:
            raise Stop("conflict overwrote return.md")
        if sha256_bytes((member / "receipt.json").read_bytes()) != receipt:
            raise Stop("conflict changed the receipt")
        add_case(
            "changed-return-on-complete",
            "refuse and require attention",
            True,
            "capture reported conflict and left return.md and the receipt unchanged",
            "An already complete member is read-only unless the bytes and flags are identical.",
        )

        final = verify("verify-happy-final", book, happy)
        if one(final, "receipt ") != receipt:
            raise Stop("final verify receipt changed")
        book_names = sorted(path.name for path in book.iterdir())
        if "05.16.md" in book_names:
            raise Stop("disposable book contains a batch page")
        add_case(
            "missing-batch-pointer",
            "do not rewrite the batch page in the first adapter",
            True,
            "verify still says result complete while the disposable book has no 05.16.md",
            "A missing pointer after complete capture is a later projection.",
        )
        return {
            "temp_root_existed": True,
            "store_outside_repo": True,
            "book_outside_repo": True,
            "instruction_sha256": digest,
            "piece_sha256": piece_sha,
            "report_sha256": sha256_bytes(REPORT),
            "mutated_sha256": sha256_bytes(mutated),
            "returned_event_sha256": event,
            "happy_member": happy,
            "reservation_release_text": RELEASE,
            "manifest_sha256": manifest,
            "receipt_sha256": receipt,
            "return_md_equals_report": True,
            "payload_equals_piece": True,
            "transport_absent_from_return_md": True,
            "side_file_sha256": sha256_bytes(mismatch_path.read_bytes()),
            "book_entries": book_names,
            "no_batch_page": True,
            "pins": pin_report,
        }
    finally:
        holder = root
        try:
            cleanup(holder)
        except OSError as exc:
            raise Stop(f"cleanup failed: {exc}") from exc


def main() -> int:
    global FAILURE
    header: dict = {"python": sys.executable, "repo": str(REPO)}
    try:
        pin_report = pins()
        header.update(fixture(pin_report))
    except Stop as exc:
        FAILURE = str(exc)
    except Exception:
        FAILURE = traceback.format_exc()
    write_proof(header)
    if FAILURE:
        print("FAILURE " + FAILURE, file=sys.stderr, flush=True)
        return 1
    print("proof cases " + str(len(CASES)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
