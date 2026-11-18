#!/usr/bin/env python3
"""Author suite for the unselected pass02 candidate (0522/05.18).

External books only. The active app is not a record target. Inspection
checkpoints are lab provenance. This suite does not require a filed pack to
stay PENDING, and it does not write a real pack back to PENDING.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LAB = REPO / "labs" / "review-loop-convergence-pass02"
KEEP = Path(r"D:\librarian\temp\0522-0518-report")
CANDIDATE = KEEP / "candidate"
APP = CANDIDATE / "app" / "librarian.py"
WB = CANDIDATE / "labs" / "review-loop-convergence-pass02" / "workbook.py"
LIVE = REPO / "00.kernel" / "00.00.10.work"
N7 = "0799.n7-convergence"
N5 = "0599.n5-convergence"
CAP = "0599.capacity-lab"
PASS = "05.01"
REL = "labs/review-loop-convergence-pass02"
SECTION_KEYS = (
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits", "next_bounded_action",
    "open_questions", "options", "outcome_evidence", "preservation", "prime_finding",
    "proposed_plan", "question", "recommendation", "remaining_choices", "return_result",
    "tests_note", "tests_passed", "within_direction",
)
ACTIVE_LIBRARIAN = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
README_SHA = "3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920"
FREEZE = "da2ecde8219de8d9e3a4416b1c91c8070479465e1a9563b635c43a0c2eb8e74e"
PASS01_WB = "ef021d4ae4066f97bfb21017d5a7952ac5161dce82e82ebec1ca756e3f58f9d9"
FILED_17 = "74015ef210f3ba7dd3ef8d3c4b27c2d7f9e4e06ab9c1536e70fe88ae0b967d20"
JUDGMENT_0509 = LIVE / "0512.prime-review" / "evidence" / "prime-review05.09" / "core-review" / "judgment.json"
JUDGMENT_OPEN = LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "core-review" / "judgment-open.json"
JUDGMENT_BAD = LIVE / "0512.prime-review" / "evidence" / "prime-review05.10" / "core-review" / "judgment.json"
OVER = LIVE / "0512.prime-review" / "evidence" / "build05.10" / "hostile" / "over-document.json"
PAGE_18 = LIVE / "0522.review-construction" / "05.18.md"
PAGE_17 = LIVE / "0522.review-construction" / "05.17.md"
FAILS: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_bytes(path: Path, data: bytes) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def expect(cond: bool, message: str) -> None:
    if not cond:
        raise AssertionError(message)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def judgment(action: str, reasons: list[str] | None = None) -> dict:
    return {
        "finding": "LAB-ONLY synthetic judgment for the convergence candidate.",
        "reasons": reasons or ["LAB-ONLY: exercise the combined chain on an external book."],
        "operation": "continue",
        "disposition": "held",
        "pass_terminal": "open",
        "goal_terminal": "open",
        "next_action": action,
        "semantic_conflict": None,
        "design_fork": None,
        "findings": [],
        "sections": {key: None for key in SECTION_KEYS} | {
            "findings_account": [],
            "next_bounded_action": "LAB-ONLY: none.",
            "prime_finding": "LAB-ONLY synthetic.",
            "return_result": "LAB-ONLY synthetic.",
            "tests_note": "LAB-ONLY.",
            "tests_passed": None,
        },
        "holds": [],
        "answers": [],
        "review_passes": [],
        "gaps": ["LAB-ONLY synthetic judgment"],
    }


def run(args: list[str]) -> dict:
    proc = subprocess.run(
        [str(PY), "-B", *args],
        cwd=str(REPO),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        shell=False,
        check=False,
    )
    body = None
    if proc.stdout:
        try:
            body = json.loads(proc.stdout.decode("utf-8"))
        except json.JSONDecodeError:
            body = None
    return {
        "exit": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr.decode("utf-8", "replace"),
        "body": body if isinstance(body, dict) else {},
    }


def loop(book: Path, command: str, source: str, pas: str = PASS, extra: list[str] | None = None) -> dict:
    args = [str(APP), "review-loop", command, "--book", str(book), "--source", source, "--pass", pas]
    if extra:
        args.extend(extra)
    return run(args)


def report(book: Path, source: str, pas: str = PASS, extra: list[str] | None = None, app: Path | None = None) -> dict:
    args = [str(app or APP), "review-report", "--book", str(book), "--source", source, "--pass", pas]
    if extra:
        args.extend(extra)
    return run(args)


def opened(book: Path, source: str, pas: str = PASS) -> dict:
    return run([str(WB), "open", "--book", str(book), "--source", source, "--pass", pas])


def save_judgment(path: Path, body: dict) -> Path:
    write_bytes(path, (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return path


def n7_pack(book: Path, source: str, pas: str, body: str, pointer: str, review: str) -> None:
    text = (
        f"# {pas} synthetic N7 pack\n\n## Goal\n{body}\n\n"
        f"## Reviewer\nA reviewer note stays in the task body.\n\n"
        f"## Reviews\nA reviews line is not the review heading.\n\n"
        f"```\n## Return pointer\nReturned: example (fenced), sha256 {'a' * 64}, 1 bytes.\n"
        f"## Review - Example\nnot the boundary\n```\n\n"
        f"~~~\n## Return pointer\nPENDING example.\n\n## Review - Codex Prime\nExample.\n~~~\n\n"
        f"## Return pointer\n{pointer}\n\n## Review - Codex Prime\n{review}\n"
    )
    write_bytes(book / source / f"{pas}.pack.md", text.encode("utf-8"))


def n7_return(book: Path, source: str, pas: str) -> dict:
    page = book / source
    artifact = write_bytes(page / "evidence" / "a.md", f"LAB artifact {source} {pas}\n".encode())
    other = write_bytes(page / "evidence" / "b.md", f"LAB other {source} {pas}\n".encode())
    returned = write_bytes(page / f"{pas}.return.md", f"# {pas} synthetic return\nLAB-ONLY.\n".encode())
    rows = [
        {"bytes": len(returned), "path": f"{pas}.return.md", "sha256": sha(returned)},
        {"bytes": len(artifact), "path": "evidence/a.md", "sha256": sha(artifact)},
        {"bytes": len(other), "path": "evidence/b.md", "sha256": sha(other)},
    ]
    blob = (json.dumps({"files": rows}, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes(page / "evidence" / "artifact-manifest.json", blob)
    return {"ret": returned, "man": blob}


def fill(book: Path, source: str, pas: str, made: dict, extra: str = "") -> None:
    ret_line = (
        f"Returned: {pas}.return.md (lab, 2026-11-04), sha256 {sha(made['ret'])}, {len(made['ret'])} bytes."
    )
    man_line = (
        f"Artifact manifest: evidence/artifact-manifest.json, sha256 {sha(made['man'])}, {len(made['man'])} bytes."
    )
    path = book / source / f"{pas}.pack.md"
    text = path.read_bytes().decode("utf-8")
    needle = "## Return pointer\nPENDING."
    if text.count(needle) != 1:
        raise AssertionError("pack pointer marker was not unique")
    path.write_bytes(text.replace(needle, "## Return pointer\n" + ret_line + "\n" + man_line + extra, 1).encode("utf-8"))


def n7_book(book: Path, source: str = N7, pas: str = PASS, review: str = "PENDING.") -> dict:
    if book.exists():
        shutil.rmtree(book)
    n7_pack(book, source, pas, "LAB-ONLY SYNTHETIC pack for the convergence candidate.", "PENDING.", review)
    proc = opened(book, source, pas)
    made = n7_return(book, source, pas)
    fill(book, source, pas, made)
    return {"open": proc, "made": made}


def record(book: Path, source: str, judgment_path: Path, pas: str = PASS) -> dict:
    prepared = loop(book, "prepare", source, pas)
    recorded = loop(
        book, "record", source, pas,
        ["--intake", prepared["body"].get("intake_id") or "missing", "--judgment", str(judgment_path)],
    )
    return {"prepare": prepared, "record": recorded}


def case(name: str, fn) -> None:
    try:
        detail = fn()
        print(f"PASS {name} {detail or ''}")
    except Exception as exc:
        FAILS.append({"name": name, "error": str(exc), "trace": traceback.format_exc()})
        print(f"FAIL {name} {exc}")


def fresh_pages(page_18: bytes) -> None:
    data = (REPO / "app" / "librarian.py").read_bytes()
    expect(sha(data) == ACTIVE_LIBRARIAN and len(data) == 12204, "active librarian moved")
    readme = (REPO / "app" / "README.md").read_bytes()
    expect(sha(readme) == README_SHA and len(readme) == 39687, "README moved")
    freeze = (LIVE / "0522.review-construction" / "evidence" / "pack05.18" / "source-manifest.json").read_bytes()
    expect(sha(freeze) == FREEZE, "pack05.18 freeze moved")
    pass01 = (REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py").read_bytes()
    expect(sha(pass01) == PASS01_WB and len(pass01) == 20034, "pass01 workbook moved")
    filed = PAGE_17.read_bytes()
    expect(FILED_17.encode() in filed, "05.17 pointer moved")
    expect(b"\n## Return pointer\nPENDING.\n" not in filed, "05.17 was reset to PENDING")
    expect(PAGE_18.read_bytes() == page_18, "05.18 changed during the suite")


def build_candidate() -> None:
    if CANDIDATE.exists():
        shutil.rmtree(CANDIDATE)
    made = run([str(LAB / "make_candidate.py"), "--output", str(CANDIDATE)])
    expect(made["exit"] == 0, made["stderr"][-500:])
    occupied = KEEP / "occupied-root"
    if occupied.exists():
        shutil.rmtree(occupied)
    occupied.mkdir()
    write_bytes(occupied / "keep.txt", b"keep\n")
    refused = run([str(LAB / "make_candidate.py"), "--output", str(occupied)])
    expect(refused["exit"] == 2 and "occupied" in refused["stderr"], refused["stderr"][-300:])
    expect((occupied / "keep.txt").read_bytes() == b"keep\n", "occupied output was overwritten")


def test_fences() -> str:
    module = load_module(LAB / "workbook.py", "pass02_workbook_fences")
    clear = (
        b"## Goal\nTask.\n\n## Reviewer\nnote\n\n## Reviews\nnote\n\n"
        b"## Return pointer example\nnot the pointer\n\n"
        b"~~~\n## Return pointer\nINSIDE\n\n## Review - Codex Prime\ninside\n~~~\n\n"
        b"## Return pointer\nOUT\n\n## Review - Codex Prime\nreal\n"
    )
    info = module.classify_pack(clear)
    expect(info["structure"] == "clear" and info["bound_sha256"], info["structure"])
    expect(module.pointer_block(clear.decode("utf-8")) == "OUT", module.pointer_block(clear.decode("utf-8")))
    backtick = clear.replace(b"~~~", b"```")
    expect(module.classify_pack(backtick)["structure"] == "clear", "backtick fence was not clear")
    unclosed = b"~~~\n## Return pointer\nIN\n\n## Review - Codex Prime\nIN\n"
    expect(module.classify_pack(unclosed)["structure"] == "ambiguous", "unclosed tilde was clear")
    mismatch = (
        b"~~~\n## Return pointer\nIN\n\n## Review - Codex Prime\nIN\n```\n\n"
        b"## Return pointer\nOUT\n\n## Review - Codex Prime\nreal\n"
    )
    expect(module.classify_pack(mismatch)["structure"] == "ambiguous", "a backtick closed a tilde fence")
    longer = (
        b"````\n## Return pointer\nIN\n\n## Review - Codex Prime\nIN\n```\n\n"
        b"## Return pointer\nOUT\n\n## Review - Codex Prime\nreal\n"
    )
    expect(module.classify_pack(longer)["structure"] == "ambiguous", "a short fence closed a longer opener")
    closed = (
        b"````\n## Return pointer\nIN\n\n## Review - Codex Prime\nIN\n````\n\n"
        b"## Return pointer\nOUT\n\n## Review - Codex Prime\nreal\n"
    )
    expect(module.classify_pack(closed)["structure"] == "clear", "matching longer fence was not clear")
    expect(module.pointer_block(closed.decode("utf-8")) == "OUT", "longer fence hid the declaration")
    duplicate = b"## Return pointer\nONE\n\n## Review - Codex Prime\nA\n\n## Review - Codex Prime\nB\n"
    dup = module.classify_pack(duplicate)
    expect(dup["structure"] == "ambiguous" and dup["bound_sha256"] is None, dup["structure"])
    missing = b"## Goal\nOnly.\n\n## Return pointer\nPENDING.\n"
    expect(module.classify_pack(missing)["structure"] == "missing", "missing review was not missing")
    return "tilde and backtick fences; lookalikes; unclosed; duplicate; missing"


def test_reporter_observations() -> str:
    module = load_module(LAB / "report.py", "pass02_report_observations")
    original = module._run

    def envelope(**extra) -> dict:
        body = {
            "accepted": False,
            "approved": False,
            "authority": "none",
            "closes_work": False,
            "releases_action": False,
            "task_association": "not-established",
            "exit": 0,
            "stale": False,
            "review_id": "lab-id",
            "judgment": {"finding": "LAB-ONLY"},
            "next_action": "LAB-ONLY",
            "custody": "not-applicable",
        }
        body.update(extra)
        return body

    def scripted(mapping):
        def _run(command, book, source, pass_id):
            item = mapping[command]
            if item == "boom":
                raise module.Refuse("workbook returned no observation")
            return dict(item)
        return _run

    def prepare(**extra):
        body = envelope(measurement="complete", exchange={"state": "matched", "chronology": "unverified", "n1_custody": "not-applicable"})
        body.update(extra)
        return body

    def run_case(mapping):
        module._run = scripted(mapping)
        return module.observe("D:\\books", "0799.lab", PASS)

    try:
        positive = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": envelope(),
        })
        expect(positive["state"] == "readable" and positive["stale"] is False, positive["state"])
        expect(positive["judgment"]["finding"] == "LAB-ONLY", "positive judgment dropped")
        expect(positive["authority"] == "none" and positive["accepted"] is False, "positive flags")
        bad = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(authority="prime", accepted=True),
            "recover": envelope(),
        })
        expect(bad["state"] == "noncurrent" and bad["stale"] is not False, bad["state"])
        expect(bad["judgment"] is None and bad["authority"] is None and bad["accepted"] is None, "unsupported flags stayed current")
        expect(bad["historical_supplied"]["judgment"]["finding"] == "LAB-ONLY", "historical judgment dropped")
        expect(bad["historical_supplied"]["envelope"]["authority"] == "prime", "raw authority dropped")
        missing = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": {key: value for key, value in envelope().items() if key != "accepted"},
        })
        expect(missing["state"] == "noncurrent" and missing["judgment"] is None and missing["authority"] is None, missing["envelope_problem"])
        typed = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(authority=1),
            "recover": envelope(),
        })
        expect(typed["state"] == "noncurrent" and typed["judgment"] is None, "wrong type stayed readable")
        no_id = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": envelope(review_id=None),
        })
        expect(no_id["state"] == "noncurrent" and no_id["judgment"] is None and no_id["authority"] is None, no_id["identity"])
        mismatch = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": envelope(review_id="other-id"),
        })
        expect(mismatch["state"] == "noncurrent" and mismatch["judgment"] is None, mismatch["identity"])
        stale = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": envelope(stale=True, exit=0),
        })
        expect(stale["state"] == "noncurrent" and stale["judgment"] is None and stale["authority"] is None, stale["identity"])
        nonzero = run_case({
            "prepare": prepare(),
            "inspect": envelope(),
            "read": envelope(),
            "recover": envelope(exit=1),
        })
        expect(nonzero["state"] == "noncurrent" and nonzero["judgment"] is None, "nonzero recover stayed current")
        try:
            module._run = scripted({"prepare": "boom", "inspect": envelope(), "read": envelope(), "recover": envelope()})
            module.observe("D:\\books", "0799.lab", PASS)
            raise AssertionError("malformed core returned a report")
        except module.Refuse as exc:
            expect("no observation" in exc.message, exc.message)
    finally:
        module._run = original
    return "positive then withhold; malformed refuses"


def test_identity() -> str:
    identity = json.loads((LAB / "harness-inputs.json").read_bytes())
    runner = load_module(REPO / "labs" / "freshness-boundary-tests-pass01" / "run.py", "freshness_runner_pass01")
    checked = runner.verify(identity, CANDIDATE)
    expect(checked["open_entry"] == f"{REL}/workbook.py", checked["open_entry"])
    document = json.loads((CANDIDATE / "CANDIDATE.json").read_bytes())
    paths = {item["path"] for item in document["files"]}
    expect(document["entry"] == "app/librarian.py" and document["entry"] in paths, "entry is not declared")
    expect(document["workbook_entry"] == document["open_entry"] and document["workbook_entry"] in paths, "workbook is not declared")
    for rel in (
        f"{REL}/report.py",
        f"{REL}/review_loop_tools.py",
        f"{REL}/review_report_tools.py",
        f"{REL}/review-loop.json",
    ):
        expect(rel in paths, f"executed file missing from identity: {rel}")
    expect("labs/n7-local-lifecycle-pass01/workbook.py" not in {item["path"] for item in document["dependencies"]}, "unused N7 prototype was claimed")
    door = load_module(CANDIDATE / REL / "review_loop_tools.py", "pass02_loop_door")
    try:
        door.executed_workbook({"tools": {"workbook": {"path": "labs/decoy-workbook.py"}}})
        raise AssertionError("purported workbook was accepted")
    except door.Refuse as exc:
        expect("purported workbook" in exc.message, exc.message)
    librarian = (CANDIDATE / "app" / "librarian.py").read_text(encoding="utf-8")
    door_text = (CANDIDATE / REL / "review_loop_tools.py").read_text(encoding="utf-8")
    expect(f"{REL}/review_loop_tools.py" in librarian, "dispatcher does not name the loop door")
    expect(f"{REL}/workbook.py" in door_text, "door does not name the workbook")
    expect("decoy-workbook.py" not in librarian and "decoy-workbook.py" not in door_text, "decoy is executed")
    expect("review_loop_tools_v" not in librarian, "a versioned door name was inserted")
    write_bytes(CANDIDATE / "labs" / "decoy-workbook.py", b"print('unused')\n")
    again = runner.verify(identity, CANDIDATE)
    expect(again["open_entry"] == document["open_entry"], "identity changed after an unused file")
    return "external identity verified; purported workbook refused"


def test_n7_cycle() -> str:
    book = KEEP / "books" / "n7-cycle"
    judge = save_judgment(KEEP / "judgment-n7.json", judgment("LAB-ONLY publish separately."))
    made = n7_book(book)
    expect(made["open"]["exit"] == 0, made["open"]["stderr"])
    expect(made["open"]["body"].get("schema") == "n7-local-open/0", "open schema")
    prepared = loop(book, "prepare", N7)
    expect(prepared["exit"] == 0, prepared["stderr"] or str(prepared["body"].get("correction")))
    exchange = prepared["body"].get("exchange") or {}
    expect(exchange.get("state") == "matched", json.dumps(exchange)[:500])
    expect(exchange.get("pack", {}).get("structure") == "clear", "tilde example made the pack ambiguous")
    expect(exchange.get("chronology") == "recorded-before-return", exchange.get("chronology"))
    expect(exchange.get("n1_custody") == "not-applicable", "n1 custody")
    codes = [item.get("code") for item in prepared["body"].get("findings") or [] if isinstance(item, dict)]
    expect("n1-not-applicable" in codes and "custody-missing" not in codes, codes)
    expect(prepared["body"].get("measurement") == "complete", prepared["body"].get("measurement"))
    form = loop(book, "form", N7)
    expect(form["exit"] == 0 and "exchange" not in form["body"], "form carried exchange")
    recorded = loop(book, "record", N7, PASS, ["--intake", prepared["body"]["intake_id"], "--judgment", str(judge)])
    expect(recorded["exit"] == 0, recorded["body"].get("correction") or recorded["stderr"])
    expect(recorded["body"].get("custody") == "not-applicable", recorded["body"].get("custody"))
    expect(recorded["body"].get("mode") == "preliminary", recorded["body"].get("mode"))
    expect(recorded["body"].get("authority") == "none" and recorded["body"].get("accepted") is False, "flags")
    target = book / N7 / "06.01.review.md"
    expect(not target.exists(), "record created the target")
    inspected = loop(book, "inspect", N7)
    expect(inspected["exit"] == 0 and "not-applicable" in (inspected["body"].get("rendered") or ""), "inspect render")
    expect("custody: missing" not in (inspected["body"].get("rendered") or ""), "render still says missing")
    write_bytes(KEEP / "checkpoints" / "n7-inspect.stdout", inspected["stdout"])
    published = loop(book, "publish", N7, PASS, ["--review", recorded["body"]["review_id"]])
    expect(published["exit"] == 0, published["body"].get("correction") or published["stderr"])
    expect(published["body"].get("published") is True and published["body"].get("published_work") is False, "publish flags")
    expect(target.is_file() and b"workbook-review-id:" in target.read_bytes(), "publish missed the absent target")
    read = loop(book, "read", N7)
    recover = loop(book, "recover", N7)
    expect(read["exit"] == 0 and read["body"].get("stale") is False, read["body"])
    expect(read["body"].get("custody") == "not-applicable", read["body"].get("custody"))
    expect(read["body"].get("judgment", {}).get("finding") == judgment("x")["finding"], "judgment drifted")
    expect(recover["exit"] == 0 and recover["body"].get("review_id") == read["body"].get("review_id"), "recover identity")
    return recorded["body"]["review_id"]


def test_region_and_rows() -> str:
    book = KEEP / "books" / "n7-region"
    judge = KEEP / "judgment-n7.json"
    n7_book(book)
    done = record(book, N7, judge)
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction"))
    review_id = done["record"]["body"]["review_id"]
    loop(book, "publish", N7, PASS, ["--review", review_id])
    pack = book / N7 / "05.01.pack.md"
    keep = pack.read_bytes()
    pack.write_bytes(keep.replace(b"## Review - Codex Prime\nPENDING.", b"## Review - Codex Prime\nLAB summary only."))
    review_edit = loop(book, "read", N7)
    pack.write_bytes(keep.replace(b"## Reviewer\nA reviewer note stays in the task body.", b"## Reviewer\nA reviewer note was edited."))
    reviewer_edit = loop(book, "read", N7)
    pack.write_bytes(keep.replace(b"Returned: 05.01.return.md", b"Returned: 05.01.return.md "))
    pointer_edit = loop(book, "read", N7)
    pack.write_bytes(keep)
    (book / N7 / "evidence" / "a.md").write_bytes(b"changed artifact\n")
    row_edit = loop(book, "read", N7)
    expect(review_edit["exit"] == 0 and review_edit["body"].get("stale") is False, "review edit was stale")
    expect(reviewer_edit["body"].get("stale") is True, "Reviewer edit was exempt")
    expect(pointer_edit["body"].get("stale") is True, "pointer edit was exempt")
    expect(row_edit["body"].get("stale") is True, "artifact edit was current")
    publish = loop(book, "publish", N7, PASS, ["--review", review_id])
    expect(publish["exit"] != 0 and not (book / N7 / "06.01.review.md").read_bytes().endswith(b"changed"), "stale publish wrote")
    return "review current; reviewer, pointer, and artifact stale"


def test_lifecycle_filing() -> str:
    book = KEEP / "books" / "lifecycle"
    if book.exists():
        shutil.rmtree(book)
    n7_pack(book, N7, PASS, "LAB-ONLY lifecycle copy.", "PENDING.", "PENDING.")
    page = book / N7 / "05.01.pack.md"
    expect(b"\n## Return pointer\nPENDING.\n" in page.read_bytes(), "disposable pack did not start pending")
    proc = opened(book, N7, PASS)
    expect(proc["exit"] == 0, proc["stderr"][:300])
    made = n7_return(book, N7, PASS)
    fill(book, N7, PASS, made)
    filed = page.read_bytes()
    expect(b"\n## Return pointer\nPENDING.\n" not in filed, "filing left the disposable pointer pending")
    expect(b"Returned: 05.01.return.md" in filed, "filing did not write the return line")
    judge = KEEP / "judgment-n7.json"
    done = record(book, N7, judge)
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction") or done["record"]["stderr"][:300])
    review_id = done["record"]["body"]["review_id"]
    loop(book, "publish", N7, PASS, ["--review", review_id])
    keep = page.read_bytes()
    page.write_bytes(keep.replace(b"## Review - Codex Prime\nPENDING.", b"## Review - Codex Prime\nLAB review update."))
    review_edit = loop(book, "read", N7)
    page.write_bytes(keep.replace(b"## Goal\nLAB-ONLY lifecycle copy.", b"## Goal\nLAB-ONLY lifecycle copy changed."))
    task_edit = loop(book, "read", N7)
    page.write_bytes(keep)
    (book / N7 / "05.01.return.md").write_bytes((book / N7 / "05.01.return.md").read_bytes() + b"LAB append\n")
    returned = report(book, N7)
    expect(review_edit["exit"] == 0 and review_edit["body"].get("stale") is False, "review update was stale")
    expect(task_edit["body"].get("stale") is True, "task edit stayed current")
    expect(returned["body"].get("state") == "held" and returned["body"].get("judgment") is None, returned["body"].get("state"))
    expect(b"\n## Return pointer\nPENDING.\n" not in PAGE_17.read_bytes(), "real 05.17 was reset")
    return "filed copy is not pending; review current; task stale; return held"


def test_hostile_fenced_boundary() -> str:
    book = KEEP / "books" / "hostile-fenced-boundary"
    judge = KEEP / "judgment-n7.json"
    n7_book(book)
    done = record(book, N7, judge)
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction"))
    loop(book, "publish", N7, PASS, ["--review", done["record"]["body"]["review_id"]])
    pack = book / N7 / "05.01.pack.md"
    keep = pack.read_bytes()
    pack.write_bytes(keep.replace(b"Returned: 05.01.return.md", b"Returned: 05.99.return.md"))
    pointer = loop(book, "read", N7)
    pack.write_bytes(keep + b"\n```\n## Review - Codex Prime\nfenced after the real heading\n")
    unclosed = loop(book, "read", N7)
    pack.write_bytes(keep.replace(b"## Review - Codex Prime\n", b"## Review - Codex Prime\n## Review - Codex Prime\n", 1))
    duplicate = loop(book, "read", N7)
    expect(pointer["body"].get("stale") is True, "fenced example hid the real pointer edit")
    expect(unclosed["body"].get("stale") is True, "unclosed fence kept the exemption")
    expect(duplicate["body"].get("stale") is True, "duplicate heading kept the exemption")
    return "hostile-fenced-boundary"


def test_hostile_missing_intake() -> str:
    book = KEEP / "books" / "hostile-missing-intake"
    judge = KEEP / "judgment-n7.json"
    n7_book(book)
    done = record(book, N7, judge)
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction"))
    review_id = done["record"]["body"]["review_id"]
    finding = done["record"]["body"]["judgment"]["finding"]
    target = book / N7 / "06.01.review.md"
    intake = book / "workbook-review" / N7 / PASS / "intake.json"
    intake.unlink()
    missing = loop(book, "read", N7)
    expect(missing["exit"] != 0 and missing["body"].get("stale") is True, "missing intake read current")
    hold = missing["body"].get("current_applicability") or {}
    expect(hold.get("state") == "unknown" and hold.get("reason") == "comparison-intake-missing", hold)
    expect(missing["body"].get("judgment", {}).get("finding") == finding, "judgment dropped")
    blocked = loop(book, "publish", N7, PASS, ["--review", review_id])
    expect(blocked["exit"] != 0 and blocked["body"].get("published") is False, "missing intake published")
    expect(blocked["body"].get("judgment", {}).get("finding") == finding, "publish dropped the judgment")
    expect(not target.exists(), "publish created a target from a missing intake")
    write_bytes(intake, b"[]\n")
    non_object = loop(book, "read", N7)
    expect((non_object["body"].get("current_applicability") or {}).get("reason") == "comparison-intake-not-object", non_object["body"])
    expect(non_object["body"].get("judgment", {}).get("finding") == finding, "non-object dropped the judgment")
    write_bytes(intake, b"{")
    invalid = loop(book, "read", N7)
    expect(invalid["exit"] != 0 and "Traceback" not in invalid["stderr"] and "refused:" in invalid["stderr"], invalid["stderr"][:300])
    fresh = KEEP / "books" / "n7-unreviewed"
    n7_book(fresh)
    prepared = loop(fresh, "prepare", N7)
    expect(prepared["exit"] == 0 and prepared["body"].get("stale") is False, "a new book was held")
    expect(prepared["body"].get("current_applicability") is None, "a new book invented a hold")
    return "hostile-missing-intake"


def test_malformed_and_mismatch() -> str:
    book = KEEP / "books" / "n7-malformed"
    if book.exists():
        shutil.rmtree(book)
    n7_pack(book, N7, PASS, "LAB malformed.", "PENDING.", "PENDING.")
    made = n7_return(book, N7, PASS)
    fill(
        book, N7, PASS, made,
        extra="\nArtifact manifest: evidence/artifact-manifest.json, sha256 " + sha(made["man"]) + f", {len(made['man'])} bytes. note",
    )
    prepared = loop(book, "prepare", N7)
    codes = [item.get("code") for item in prepared["body"].get("findings") or [] if isinstance(item, dict)]
    expect("malformed-n7-declaration" in codes, codes)
    expect(prepared["body"].get("measurement") == "incomplete", prepared["body"].get("measurement"))
    judge = KEEP / "judgment-n7.json"
    recorded = loop(book, "record", N7, PASS, ["--intake", prepared["body"].get("intake_id") or "missing", "--judgment", str(judge)])
    expect(recorded["exit"] != 0 and recorded["body"].get("recorded") is not True, "malformed recorded")
    mismatch = KEEP / "books" / "n7-mismatch"
    if mismatch.exists():
        shutil.rmtree(mismatch)
    n7_pack(mismatch, N7, PASS, "LAB mismatch.", "PENDING.", "PENDING.")
    made = n7_return(mismatch, N7, PASS)
    ret_line = f"Returned: 05.02.return.md (lab, 2026-11-04), sha256 {sha(made['ret'])}, {len(made['ret'])} bytes."
    man_line = f"Artifact manifest: evidence/artifact-manifest.json, sha256 {sha(made['man'])}, {len(made['man'])} bytes."
    path = mismatch / N7 / "05.01.pack.md"
    path.write_bytes(path.read_bytes().replace(b"## Return pointer\nPENDING.", f"## Return pointer\n{ret_line}\n{man_line}".encode(), 1))
    prepared = loop(mismatch, "prepare", N7)
    expect((prepared["body"].get("exchange") or {}).get("state") == "return-not-local", prepared["body"].get("exchange"))
    recorded = loop(mismatch, "record", N7, PASS, ["--intake", prepared["body"].get("intake_id") or "missing", "--judgment", str(judge)])
    expect(recorded["exit"] != 0, "same-NN mismatch recorded")
    historical = KEEP / "books" / "n7-historical"
    if historical.exists():
        shutil.rmtree(historical)
    n7_pack(historical, N7, PASS, "LAB historical.", "PENDING.", "PENDING.")
    made = n7_return(historical, N7, PASS)
    fill(historical, N7, PASS, made)
    prepared = loop(historical, "prepare", N7)
    expect((prepared["body"].get("exchange") or {}).get("chronology") == "unverified", prepared["body"].get("exchange"))
    recorded = loop(historical, "record", N7, PASS, ["--intake", prepared["body"]["intake_id"], "--judgment", str(judge)])
    expect(recorded["exit"] == 0, recorded["body"].get("correction"))
    return "malformed refused; mismatch refused; historical unverified recorded"


def test_target_guards() -> str:
    judge = KEEP / "judgment-n7.json"
    manual = KEEP / "books" / "n7-manual"
    n7_book(manual)
    done = record(manual, N7, judge)
    target = manual / N7 / "06.01.review.md"
    planted = b"# Prime review - LAB manual text\nDirector text: keep.\n"
    write_bytes(target, planted)
    published = loop(manual, "publish", N7, PASS, ["--review", done["record"]["body"]["review_id"]])
    expect(published["exit"] != 0 and target.read_bytes() == planted, "manual text was replaced")
    expect(published["body"].get("judgment", {}).get("finding"), "manual publish dropped the judgment")
    appeared = KEEP / "books" / "n7-appeared"
    n7_book(appeared)
    done = record(appeared, N7, judge)
    target = appeared / N7 / "06.01.review.md"
    planted = b"# appeared after inspect\n"
    write_bytes(target, planted)
    published = loop(appeared, "publish", N7, PASS, ["--review", done["record"]["body"]["review_id"]])
    expect(published["exit"] != 0 and target.read_bytes() == planted, "appeared target was replaced")
    return "manual and appeared targets kept"


def test_n5_instance_and_custody() -> str:
    book = KEEP / "books" / "n5-same"
    if book.exists():
        shutil.rmtree(book)
    page = book / N5
    artifact = write_bytes(page / "evidence" / "b" / "artifact.md", b"LAB N5 artifact\n")
    submission = write_bytes(page / "evidence" / "b" / "submission.md", b"LAB N5 submission\n")
    manifest_body = {"files": [{"bytes": len(artifact), "path": f"{N5}/evidence/b/artifact.md", "sha256": sha(artifact)}]}
    manifest = (json.dumps(manifest_body, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes(page / "evidence" / "b" / "artifact-manifest.json", manifest)
    write_bytes(page / "05.01.md", (
        "# 05.01 synthetic N5\n\n## Goal\nLAB-ONLY.\n\n## Return pointer\n"
        f"Submission: {N5}/evidence/b/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
        f"Artifact manifest: {N5}/evidence/b/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n\n"
        "## Review - Codex Prime\nPENDING.\n"
    ).encode("utf-8"))
    judge = KEEP / "judgment-n7.json"
    done = record(book, N5, judge)
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction") or done["record"]["stderr"])
    expect(done["record"]["body"].get("custody") == "missing", done["record"]["body"].get("custody"))
    read = loop(book, "read", N5)
    expect(read["exit"] == 0 and read["body"].get("stale") is False, "same-instance N5 was not current")
    expect(read["body"].get("custody") == "missing", "N5 custody changed")
    copied = KEEP / "books" / "n5-copy"
    if copied.exists():
        shutil.rmtree(copied)
    shutil.copytree(book, copied)
    foreign = loop(copied, "read", N5)
    held = foreign["exit"] != 0 or foreign["body"].get("stale") is True or (foreign["body"].get("instance_applicability") or {}).get("state") == "held"
    expect(held, "copied N5 read current")
    expect((foreign["body"].get("instance_applicability") or {}).get("reason") == "different-root", foreign["body"].get("instance_applicability"))
    occupied = book / N5 / "05.01.md"
    original = occupied.read_bytes()
    occupied.write_bytes(original.replace(b"## Review - Codex Prime\nPENDING.\n", b"## Review - Codex Prime\nworkbook-review-id: wa000000000000000\nforeign\n"))
    published = loop(book, "publish", N5, PASS, ["--review", done["record"]["body"]["review_id"]])
    expect(published["exit"] != 0 and b"workbook-review-id: wa000000000000000" in occupied.read_bytes(), "occupied section was replaced")
    return "N5 same current; copy held; N5 custody missing"


def test_limits() -> str:
    judge = JUDGMENT_0509

    def write_cap(book: Path, count: int, big: int | None = None) -> None:
        if book.exists():
            shutil.rmtree(book)
        files = []
        for index in range(count):
            rel = f"{CAP}/evidence/a{index:02d}.txt"
            data = f"artifact {index}\n".encode()
            if big is not None and index == 0:
                data = b"B" * big
                rel = f"{CAP}/evidence/big.bin"
            write_bytes(book / rel, data)
            files.append({"bytes": len(data), "path": rel, "sha256": sha(data)})
        submission = b"submission\n"
        write_bytes(book / CAP / "evidence" / "submission.md", submission)
        manifest = {"excludes_self": True, "file_count": len(files), "files": files, "schema": "review-report-artifact-manifest/2"}
        blob = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        write_bytes(book / CAP / "evidence" / "artifact-manifest.json", blob)
        pointer = (
            f"Submission: {CAP}/evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: {CAP}/evidence/artifact-manifest.json sha256 {sha(blob)}, {len(blob)} bytes, {len(files)} files. Excludes itself.\n"
        )
        page = (
            "Intro OUTSIDE\n\n## Goal\nReview one disposable capture.\n\n## Return pointer\n"
            + pointer + "## Review - Codex Prime\nPENDING.\n"
        ).encode()
        write_bytes(book / CAP / "05.99.md", page)

    def sources_of(book: Path) -> int:
        path = book / "workbook-review" / "tmp" / "prime-input.json"
        return len(json.loads(path.read_text(encoding="utf-8"))["sources"])

    at = KEEP / "books" / "cap-64"
    write_cap(at, 62)
    done = record(at, CAP, judge, "05.99")
    expect(done["record"]["exit"] == 0, done["record"]["body"].get("correction") or done["record"]["stderr"][:400])
    expect(sources_of(at) == 64, sources_of(at))
    over = KEEP / "books" / "cap-65"
    write_cap(over, 63)
    done = record(over, CAP, judge, "05.99")
    expect(done["record"]["exit"] != 0 and "limit sources" in str(done["record"]["body"].get("correction")), done["record"]["body"].get("correction"))
    expect(sources_of(over) == 65, "65-source input was not retained")
    write_cap(KEEP / "books" / "cap-list", 3)
    listed = record(KEEP / "books" / "cap-list", CAP, save_judgment(KEEP / "judgment-list.json", judgment("LAB list.", [f"LAB-ONLY reason {i}" for i in range(25)])), "05.99")
    expect(listed["record"]["exit"] != 0 and "limit" in str(listed["record"]["body"].get("correction")) and "reasons" in str(listed["record"]["body"].get("correction")), listed["record"]["body"].get("correction"))
    write_cap(KEEP / "books" / "cap-doc", 3)
    huge = judgment("LAB document.", [f"LAB-ONLY {i} " + ("x" * 11000) for i in range(24)])
    path = save_judgment(KEEP / "judgment-doc.json", huge)
    expect(path.stat().st_size > 262144, "document fixture is not over the JSON bound")
    documented = record(KEEP / "books" / "cap-doc", CAP, path, "05.99")
    text = str(documented["record"]["body"].get("correction") or "") + documented["record"]["stderr"]
    expect(documented["record"]["exit"] != 0 and ("262144" in text or "exceeds" in text), text[:400])
    bound = KEEP / "books" / "cap-16m"
    write_cap(bound, 1, 16777216)
    accepted = record(bound, CAP, judge, "05.99")
    expect(accepted["record"]["exit"] == 0, accepted["record"]["body"].get("correction") or accepted["record"]["stderr"][:400])
    prime = json.loads((bound / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
    row = next(item for item in prime["sources"] if item["logical_path"].endswith("big.bin"))
    expect(row["content_bytes"] == 16777216 and row["record"] is None, row.get("record"))
    above = KEEP / "books" / "cap-16m-plus"
    write_cap(above, 1, 16777217)
    refused = record(above, CAP, judge, "05.99")
    expect(refused["record"]["exit"] != 0 and "16777216" in str(refused["record"]["body"].get("correction")), refused["record"]["body"].get("correction"))
    return "64 recorded; 65, list, document, and 16MiB+1 refused; 16MiB recorded"


def test_replay_0510() -> str:
    book = KEEP / "books" / "replay-0510"
    if book.exists():
        shutil.rmtree(book)
    book.mkdir(parents=True)
    shutil.copytree(LIVE / "0512.prime-review", book / "0512.prime-review")
    prepared = loop(book, "prepare", "0512.prime-review", "05.10")
    expect(prepared["exit"] == 0 and prepared["body"].get("measurement") == "complete", prepared["stderr"][:400] or prepared["body"].get("measurement"))
    refused = loop(book, "record", "0512.prime-review", "05.10", ["--intake", prepared["body"]["intake_id"], "--judgment", str(JUDGMENT_BAD)])
    expect(refused["exit"] != 0 and refused["body"].get("correction") == "a held review keeps the pass and the goal open", refused["body"].get("correction"))
    recorded = loop(book, "record", "0512.prime-review", "05.10", ["--intake", prepared["body"]["intake_id"], "--judgment", str(JUDGMENT_OPEN)])
    expect(recorded["exit"] == 0, recorded["body"].get("correction") or recorded["stderr"][:400])
    prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
    expect(len(prime["sources"]) == 44, len(prime["sources"]))
    expect((book / "workbook-review" / "tmp" / "prime-input.json").stat().st_size == 137328, "prime input size")
    row = next(item for item in prime["sources"] if str(item.get("logical_path", "")).endswith("hostile/over-document.json"))
    expect(row["content_bytes"] == 276423 and row["record"] is None, row)
    copied = book / "0512.prime-review" / "evidence" / "build05.10" / "hostile" / "over-document.json"
    expect(copied.read_bytes() == OVER.read_bytes() and copied.stat().st_size == 276423, "over-document bytes")
    read = loop(book, "read", "0512.prime-review", "05.10")
    expect(read["exit"] == 0 and read["body"].get("custody") == "missing", read["body"].get("custody"))
    return "44-source open judgment recorded; finished terminal refused; record null"


def test_reporter_command() -> str:
    book = KEEP / "books" / "report-current"
    judge = KEEP / "judgment-n7.json"
    n7_book(book)
    done = record(book, N7, judge)
    review_id = done["record"]["body"]["review_id"]
    loop(book, "publish", N7, PASS, ["--review", review_id])
    current = report(book, N7)
    expect(current["exit"] == 0, current["stderr"][:400])
    body = current["body"]
    core = loop(book, "read", N7)["body"]
    prepare = loop(book, "prepare", N7)["body"]
    expect(body.get("schema") == "review-report-convergence/2", body.get("schema"))
    for key, value in {
        "authority": "none", "accepted": False, "work_complete": False, "action_released": False, "releases_action": False,
    }.items():
        expect(body.get(key) == value, f"{key}={body.get(key)!r}")
    expect(body.get("state") == "readable" and body.get("stale") is False, body.get("state"))
    expect(body.get("review_id") == core.get("review_id") == review_id, "review id")
    expect(body.get("custody") == core.get("custody") == "not-applicable", body.get("custody"))
    exchange = body.get("exchange") or {}
    core_exchange = prepare.get("exchange") or {}
    for key in ("state", "chronology", "n1_custody"):
        expect(exchange.get(key) == core_exchange.get(key), key)
    empty = KEEP / "books" / "report-empty"
    if empty.exists():
        shutil.rmtree(empty)
    n7_pack(empty, N7, PASS, "LAB empty.", "PENDING.", "PENDING.")
    made = n7_return(empty, N7, PASS)
    fill(empty, N7, PASS, made)
    vacant = report(empty, N7)
    expect(vacant["exit"] == 0 and vacant["body"].get("state") == "not-recorded", vacant["body"].get("state") or vacant["stderr"][:300])
    expect(vacant["body"].get("judgment") is None and vacant["body"].get("stale") is not False, "empty review looked current")
    stale_book = KEEP / "books" / "report-stale"
    if stale_book.exists():
        shutil.rmtree(stale_book)
    shutil.copytree(book, stale_book)
    pack = stale_book / N7 / "05.01.pack.md"
    pack.write_bytes(pack.read_bytes().replace(
        b"## Reviewer\nA reviewer note stays in the task body.",
        b"## Reviewer\nA reviewer note was edited after publish.",
        1,
    ))
    stale = report(stale_book, N7)
    expect(stale["exit"] == 0 and stale["body"].get("state") == "stale" and stale["body"].get("stale") is True, stale["body"].get("state"))
    expect(stale["body"].get("judgment") is None and stale["body"].get("authority") == "none", "stale judgment was current")
    expect((stale["body"].get("historical_supplied") or {}).get("judgment", {}).get("finding"), "historical judgment dropped")
    held_book = KEEP / "books" / "report-held"
    if held_book.exists():
        shutil.rmtree(held_book)
    n7_book(held_book)
    (held_book / N7 / "evidence" / "b.md").unlink()
    held = report(held_book, N7)
    expect(held["exit"] == 0 and held["body"].get("state") == "held", held["body"].get("state") or held["stderr"][:300])
    expect(held["body"].get("judgment") is None and held["body"].get("authority") == "none", "held grew a judgment")
    room = KEEP / "rooms" / "report-pins"
    if room.exists():
        shutil.rmtree(room)
    shutil.copytree(CANDIDATE, room)
    control = report(book, N7, app=room / "app" / "librarian.py")
    expect(control["exit"] == 0 and control["body"].get("state") == "readable", "positive control")
    before = (REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py").read_bytes()
    librarian = room / "app" / "librarian.py"
    original = librarian.read_bytes()
    librarian.write_bytes(original + b"\n# tamper\n")
    wrong = report(book, N7, app=room / "app" / "librarian.py")
    librarian.write_bytes(original)
    expect(wrong["exit"] != 0 and "Traceback" not in wrong["stderr"], wrong["stderr"][:300])
    workbook = room / "labs" / "review-loop-convergence-pass02" / "workbook.py"
    original_wb = workbook.read_bytes()
    workbook.write_bytes(original_wb + b"\n# tamper\n")
    wrong_wb = report(book, N7, app=room / "app" / "librarian.py")
    workbook.write_bytes(original_wb)
    expect(wrong_wb["exit"] != 0 and "Traceback" not in wrong_wb["stderr"] and "pin mismatch" in wrong_wb["stderr"], wrong_wb["stderr"][:300])
    reporter = room / "labs" / "review-loop-convergence-pass02" / "report.py"
    original_report = reporter.read_bytes()
    reporter.write_bytes(original_report + b"\n# tamper\n")
    wrong_report = report(book, N7, app=room / "app" / "librarian.py")
    reporter.write_bytes(original_report)
    expect(wrong_report["exit"] != 0 and "Traceback" not in wrong_report["stderr"], wrong_report["stderr"][:300])
    expect((REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py").read_bytes() == before, "canonical workbook was tampered")
    probes = [
        report(book, N7, extra=["--bogus", "x"]),
        report(book, N7, extra=["--pass", PASS]),
        run([str(APP), "review-report", "--book", "00.kernel/00.00.10.work", "--source", N7, "--pass", PASS]),
        report(book, N7, pas="5.1"),
        run([str(APP), "review-report", "--book", str(book), "--pass", PASS]),
    ]
    for probe in probes:
        expect(probe["exit"] != 0 and "Traceback" not in probe["stderr"] and probe["body"].get("state") in (None, "refused"), probe["stderr"][:240])
    again = report(book, N7)
    expect(again["exit"] == 0, "control after refusals")
    frozen = run([str(REPO / "app" / "review_report_tools_v3.py"), "--book", str(book), "--source", N7, "--pass", PASS])
    expect(frozen["exit"] != 0 and "Traceback" not in frozen["stderr"], frozen["stderr"][:300])
    return "reporter agrees; disposable pins refuse; v3 baseline refuses"


def test_same_path_limit() -> str:
    left = KEEP / "books" / "id-left"
    right = KEEP / "books" / "id-right"
    n7_book(left)
    n7_book(right)
    a = loop(left, "prepare", N7)["body"]
    b = loop(right, "prepare", N7)["body"]
    expect(a.get("instance_id") != b.get("instance_id"), "different directories shared an instance id")
    expect(len(a.get("instance_id") or "") == 64, "instance id shape")
    return "instance id follows the path; same-path clone detection is not claimed"


def test_copied_workbook() -> str:
    copied = KEEP / "copied-pass01-workbook.py"
    shutil.copyfile(REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py", copied)
    proc = run([str(copied), "prepare", "--book", str(KEEP / "books" / "n7-cycle"), "--source", N7, "--pass", PASS])
    expect(proc["exit"] == 2 and "canonical" in proc["stderr"], proc["stderr"][:300])
    external = KEEP / "copied-pass02-workbook.py"
    shutil.copyfile(WB, external)
    ran = run([str(external), "prepare", "--book", str(KEEP / "books" / "n7-cycle"), "--source", N7, "--pass", PASS])
    expect(ran["exit"] == 0 and ran["body"].get("measurement") == "complete", ran["stderr"][:300])
    return "frozen pass01 copy refused; pass02 copy ran from an external path"


def _finish() -> None:
    log = {"failed": len(FAILS), "fails": FAILS}
    write_bytes(KEEP / "author-suite.json", (json.dumps(log, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(f"FAILED {len(FAILS)}")


def main() -> int:
    page_18 = PAGE_18.read_bytes()
    KEEP.mkdir(parents=True, exist_ok=True)
    (KEEP / "checkpoints").mkdir(parents=True, exist_ok=True)
    fresh_pages(page_18)
    build_candidate()
    case("fences", test_fences)
    case("reporter-observations", test_reporter_observations)
    case("identity", test_identity)
    case("n7-cycle", test_n7_cycle)
    if FAILS:
        _finish()
        return 1
    case("region-and-rows", test_region_and_rows)
    case("lifecycle-filing", test_lifecycle_filing)
    case("hostile-fenced-boundary", test_hostile_fenced_boundary)
    case("hostile-missing-intake", test_hostile_missing_intake)
    case("malformed-and-mismatch", test_malformed_and_mismatch)
    case("target-guards", test_target_guards)
    case("n5-instance", test_n5_instance_and_custody)
    case("same-path-limit", test_same_path_limit)
    case("copied-workbook", test_copied_workbook)
    case("limits", test_limits)
    case("replay-0510", test_replay_0510)
    case("reporter", test_reporter_command)
    fresh_pages(page_18)
    _finish()
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
