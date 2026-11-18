#!/usr/bin/env python3
"""0522/05.16 author suite for N5 book-instance applicability.

External roots only. Compares the unselected candidate with frozen pass05.
Does not record or publish on D:\\Git\\lib-build.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LAB = REPO / "labs" / "review-instance-binding-pass01"
STAMP = Path(r"D:\librarian\temp\0522-0516\suite-20261104")
N5 = "0599.n5-instance-lab"
N7 = "0799.n7-instance-lab"
N7_BAD = "0799.n7-malformed-lab"
PASS = "05.01"
CANDIDATE = [str(LAB / "workbook.py")]
PASS05 = [str(REPO / "labs" / "workbook-review-pass05" / "workbook.py")]
DOOR = [str(LAB / "review_loop_tools.py")]
APP = [str(LAB / "candidate" / "app" / "librarian.py"), "review-loop"]
SECTION_KEYS = (
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits", "next_bounded_action",
    "open_questions", "options", "outcome_evidence", "preservation", "prime_finding",
    "proposed_plan", "question", "recommendation", "remaining_choices", "return_result",
    "tests_note", "tests_passed", "within_direction",
)
CLOSED = (
    "accepted", "approved", "authority", "closes_work", "eligible_for_custody_completion",
    "published_work", "releases_action",
)
FROZEN = (
    "app/librarian.py",
    "app/README.md",
    "README.md",
    "app/review_loop_tools_v4.py",
    "app/review-loop-v4.json",
    "app/review_loop_tools_v5.py",
    "app/review-loop-v5.json",
    "app/review_loop_tools_v6.py",
    "app/review-loop-v6.json",
    "app/review_loop_tools_v7.py",
    "app/review-loop-v7.json",
    "app/review_loop_tools_v8.py",
    "app/review-loop-v8.json",
    "app/review_loop_tools_v9.py",
    "app/review-loop-v9.json",
    "labs/workbook-review-pass01/workbook.py",
    "labs/workbook-review-pass01/forms/workbook-review-v1.json",
    "labs/workbook-review-pass02/workbook.py",
    "labs/workbook-review-pass02/forms/workbook-review-v1.json",
    "labs/workbook-review-pass03/workbook.py",
    "labs/workbook-review-pass03/forms/workbook-review-v1.json",
    "labs/workbook-review-pass04/workbook.py",
    "labs/workbook-review-pass05/workbook.py",
    "labs/n7-local-lifecycle-pass01/workbook.py",
    "00.kernel/00.00.10.work/0522.review-construction/06.31.md",
    "00.kernel/00.00.10.work/0522.review-construction/06.32.md",
    "00.kernel/00.00.10.work/0522.review-construction/06.33.md",
    "00.kernel/00.00.10.work/0522.review-construction/05.15.md",
)
FAILS: list[dict] = []
CASES: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frozen_map() -> dict:
    found = {}
    for rel in FROZEN:
        path = REPO / rel
        data = path.read_bytes()
        found[rel] = {"sha256": sha(data), "bytes": len(data)}
    for rel in (
        "labs/review-source-capacity-pass01",
        "labs/review-source-capacity-pass02",
    ):
        root = REPO / rel
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            if path.is_file():
                key = path.relative_to(REPO).as_posix()
                data = path.read_bytes()
                found[key] = {"sha256": sha(data), "bytes": len(data)}
    return found


def write_text(path: Path, text: str) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    path.write_bytes(data)
    return data


def judgment(next_action: str) -> dict:
    return {
        "finding": "LAB-ONLY synthetic judgment for the 0522/05.16 instance-binding suite.",
        "reasons": ["LAB-ONLY: exercise N5 current applicability on an external book."],
        "operation": "continue",
        "disposition": "held",
        "pass_terminal": "open",
        "goal_terminal": "open",
        "next_action": next_action,
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


def run(entry: list[str], book: Path, command: str, source: str, extra: list[str] | None = None) -> dict:
    args = [str(PY), "-B", *entry, command, "--book", str(book), "--source", source, "--pass", PASS]
    if extra:
        args.extend(extra)
    proc = subprocess.run(
        args,
        cwd=str(REPO),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        shell=False,
        check=False,
    )
    body = None
    try:
        body = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        body = None
    return {
        "exit": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "body": body if isinstance(body, dict) else {},
    }


def codes(row: dict) -> list:
    return sorted({item.get("code") for item in row["body"].get("findings") or [] if isinstance(item, dict)})


def tree(root: Path) -> dict:
    found = {}
    for path in root.rglob("*"):
        if path.is_file():
            found[path.relative_to(root).as_posix()] = sha(path.read_bytes())
    return found


def store_of(book: Path, source: str) -> Path:
    return book / "workbook-review" / source / PASS


def file_sha(path: Path) -> str | None:
    if path.is_file():
        return sha(path.read_bytes())
    return None


def durable(book: Path, source: str, review_id: str | None) -> dict:
    store = store_of(book, source)
    found = {
        "intake.json": file_sha(store / "intake.json"),
        "journal.json": file_sha(store / "journal.json"),
    }
    if isinstance(review_id, str):
        found["record.json"] = file_sha(store / "reviews" / review_id / "record.json")
        found["rendered.md"] = file_sha(store / "reviews" / review_id / "rendered.md")
    return found


def closed_ok(body: dict) -> bool:
    return (
        body.get("accepted") is False
        and body.get("approved") is False
        and body.get("authority") == "none"
        and body.get("closes_work") is False
        and body.get("eligible_for_custody_completion") is False
        and body.get("published_work") is False
        and body.get("releases_action") is False
    )


def hold_of(body: dict) -> dict:
    value = body.get("instance_applicability")
    return value if isinstance(value, dict) else {}


def case(name: str, ok: bool, detail: dict) -> None:
    CASES.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    print(("PASS" if ok else "FAIL") + " " + name)
    if not ok:
        FAILS.append({"name": name, "detail": detail})


def make_n5(book: Path, artifact_text: str, review_body: str) -> None:
    page = book / N5
    artifact = write_text(page / "evidence" / "b" / "artifact.md", artifact_text)
    submission = write_text(page / "evidence" / "b" / "submission.md", "LAB N5 submission for instance binding\n")
    manifest_body = {
        "files": [{
            "bytes": len(artifact),
            "path": f"{N5}/evidence/b/artifact.md",
            "sha256": sha(artifact),
        }]
    }
    manifest = write_text(
        page / "evidence" / "b" / "artifact-manifest.json",
        json.dumps(manifest_body, indent=2, sort_keys=True) + "\n",
    )
    write_text(
        page / "05.01.md",
        "# 05.01 synthetic N5 page\n\n## Goal\nLAB-ONLY instance binding.\n\n"
        "## Return pointer\n"
        f"Submission: {N5}/evidence/b/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
        f"Artifact manifest: {N5}/evidence/b/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n\n"
        f"## Review - Codex Prime\n{review_body}\n",
    )


def make_n7(book: Path, source: str, malformed: bool) -> None:
    page = book / source
    artifact = write_text(page / "evidence" / "a" / "artifact.md", f"LAB N7 artifact for {source}\n")
    returned = write_text(page / "05.01.return.md", f"# 05.01 synthetic return for {source}\nLAB-ONLY.\n")
    manifest_body = {
        "files": [{
            "bytes": len(artifact),
            "path": f"{source}/evidence/a/artifact.md",
            "sha256": sha(artifact),
        }]
    }
    manifest = write_text(
        page / "evidence" / "a" / "artifact-manifest.json",
        json.dumps(manifest_body, indent=2, sort_keys=True) + "\n",
    )
    if malformed:
        manifest_line = (
            f"Artifact manifest: {source}/evidence/a/artifact-manifest.json, sha256 {sha(manifest)}, {len(manifest)} bytes. note"
        )
    else:
        manifest_line = (
            f"Artifact manifest: {source}/evidence/a/artifact-manifest.json, sha256 {sha(manifest)}, {len(manifest)} bytes."
        )
    write_text(
        page / "05.01.pack.md",
        f"# 05.01 synthetic N7 pack\n\n## Goal\nLAB-ONLY N7 control.\n\n"
        "## Return pointer\n"
        f"Returned: {source}/05.01.return.md (lab record, 2026-11-04), sha256 {sha(returned)}, {len(returned)} bytes.\n"
        f"{manifest_line}\n\n"
        "## Review - Codex Prime\nPENDING.\n",
    )


def record(book: Path, source: str, judgment_path: Path) -> dict:
    prepared = run(CANDIDATE, book, "prepare", source)
    recorded = run(
        CANDIDATE,
        book,
        "record",
        source,
        ["--intake", prepared["body"].get("intake_id") or "missing", "--judgment", str(judgment_path)],
    )
    return {"prepare": prepared, "record": recorded}


def rewrite_intake(book: Path, source: str, mutate) -> None:
    path = store_of(book, source) / "intake.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def main() -> int:
    if STAMP.exists():
        print("stamp exists", STAMP)
        return 2
    if str(STAMP).lower().startswith(str(REPO).lower()):
        print("stamp is inside the checkout")
        return 2
    before = frozen_map()
    STAMP.mkdir(parents=True)
    judgment_path = STAMP / "judgment.json"
    judgment_path.write_bytes((json.dumps(judgment("LAB-ONLY: keep the stored review historical when the book root differs."), indent=2, sort_keys=True) + "\n").encode("utf-8"))
    other_judgment = STAMP / "judgment-other.json"
    other_judgment.write_bytes((json.dumps(judgment("LAB-ONLY: this second book has its own review."), indent=2, sort_keys=True) + "\n").encode("utf-8"))

    life = STAMP / "life"
    make_n5(life, "LAB artifact on the same-instance book\n", "PENDING.")
    base_prepare = run(PASS05, life, "prepare", N5)
    cand_prepare = run(CANDIDATE, life, "prepare", N5)
    base_form = run(PASS05, life, "form", N5)
    cand_form = run(CANDIDATE, life, "form", N5)
    case(
        "same-instance-prepare-form",
        base_prepare["stdout"] == cand_prepare["stdout"]
        and base_form["stdout"] == cand_form["stdout"]
        and cand_prepare["exit"] == 0
        and cand_prepare["body"].get("stale") is False
        and "instance_applicability" not in cand_prepare["body"]
        and cand_prepare["body"].get("measurement") == "complete",
        {"prepare_exit": cand_prepare["exit"], "stdout_equal": base_prepare["stdout"] == cand_prepare["stdout"]},
    )
    recorded = record(life, N5, judgment_path)
    review_id = recorded["record"]["body"].get("review_id")
    life_durable = durable(life, N5, review_id if isinstance(review_id, str) else None)
    base_read = run(PASS05, life, "read", N5)
    cand_read = run(CANDIDATE, life, "read", N5)
    case(
        "same-instance-read",
        recorded["record"]["exit"] == 0
        and base_read["stdout"] == cand_read["stdout"]
        and cand_read["exit"] == 0
        and cand_read["body"].get("stale") is False
        and "instance_applicability" not in cand_read["body"]
        and cand_read["body"].get("judgment") == json.loads(judgment_path.read_text(encoding="utf-8"))
        and closed_ok(cand_read["body"]),
        {"record_exit": recorded["record"]["exit"], "read_exit": cand_read["exit"], "stderr": recorded["record"]["stderr"].decode("utf-8", "replace")[-300:]},
    )
    stored_book = json.loads((store_of(life, N5) / "intake.json").read_text(encoding="utf-8")).get("book")
    spelling_ok = []
    variants = [str(stored_book).replace("\\", "/"), str(stored_book) + "\\"]
    chars = list(str(stored_book))
    for index, char in enumerate(chars):
        if char.isalpha() and index > 2:
            chars[index] = char.lower() if char.isupper() else char.upper()
            variants.append("".join(chars))
            break
    for variant in variants:
        try:
            resolved = str(Path(variant).resolve())
        except OSError:
            resolved = ""
        if resolved != stored_book:
            spelling_ok.append({"variant": variant, "resolved_equal": False})
            continue
        row = run(CANDIDATE, Path(variant), "read", N5)
        spelling_ok.append({
            "variant": variant,
            "resolved_equal": True,
            "exit": row["exit"],
            "stale": row["body"].get("stale"),
            "held": "instance_applicability" in row["body"],
        })
    case(
        "same-root-spelling",
        any(item.get("resolved_equal") for item in spelling_ok)
        and all(item.get("exit") == 0 and item.get("stale") is False and item.get("held") is False for item in spelling_ok if item.get("resolved_equal")),
        {"variants": spelling_ok},
    )

    copied = STAMP / "copied"
    shutil.copytree(life, copied)
    base_copy = run(PASS05, copied, "read", N5)
    cand_copy = run(CANDIDATE, copied, "read", N5)
    recover_tree_before = tree(copied)
    recover_1 = run(CANDIDATE, copied, "recover", N5)
    recover_2 = run(CANDIDATE, copied, "recover", N5)
    recover_tree_after = tree(copied)
    door_copy = run(DOOR, copied, "read", N5)
    app_copy = run(APP, copied, "read", N5)
    prepared_copy = run(CANDIDATE, copied, "prepare", N5)
    form_copy = run(CANDIDATE, copied, "form", N5)
    inspect_copy = run(CANDIDATE, copied, "inspect", N5)
    page_before = file_sha(copied / N5 / "05.01.md")
    publish_copy = run(CANDIDATE, copied, "publish", N5, ["--review", review_id or "missing"])
    page_after = file_sha(copied / N5 / "05.01.md")
    repin = run(
        CANDIDATE,
        copied,
        "record",
        N5,
        ["--intake", prepared_copy["body"].get("intake_id") or "missing", "--judgment", str(judgment_path)],
    )
    copied_durable = durable(copied, N5, review_id if isinstance(review_id, str) else None)
    life_after = durable(life, N5, review_id if isinstance(review_id, str) else None)
    hold = hold_of(cand_copy["body"])
    case(
        "baseline-copy-still-current",
        base_copy["exit"] == 0 and base_copy["body"].get("stale") is False,
        {"exit": base_copy["exit"], "stale": base_copy["body"].get("stale")},
    )
    case(
        "candidate-copy-held",
        cand_copy["exit"] == 1
        and cand_copy["body"].get("stale") is True
        and hold.get("reason") == "different-root"
        and hold.get("current") is False
        and hold.get("state") == "held"
        and cand_copy["body"].get("judgment") == json.loads(judgment_path.read_text(encoding="utf-8"))
        and cand_copy["body"].get("next_action") == "LAB-ONLY: keep the stored review historical when the book root differs."
        and closed_ok(cand_copy["body"])
        and door_copy["exit"] == 1
        and hold_of(door_copy["body"]).get("reason") == "different-root"
        and app_copy["exit"] == 1
        and hold_of(app_copy["body"]).get("reason") == "different-root"
        and recover_1["stdout"] == recover_2["stdout"]
        and recover_1["exit"] == 1
        and recover_tree_before == recover_tree_after
        and prepared_copy["body"].get("stale") is True
        and hold_of(prepared_copy["body"]).get("reason") == "different-root"
        and "instance_applicability" not in form_copy["body"]
        and inspect_copy["exit"] == 0
        and inspect_copy["body"].get("stale") is True
        and inspect_copy["body"].get("judgment") == cand_copy["body"].get("judgment")
        and publish_copy["exit"] == 1
        and publish_copy["body"].get("published") is False
        and publish_copy["body"].get("correction") == "Publication is blocked because the selected source changed after intake."
        and publish_copy["body"].get("judgment") == cand_copy["body"].get("judgment")
        and page_before == page_after
        and closed_ok(publish_copy["body"])
        and repin["exit"] == 2
        and repin["body"].get("correction") == "The stored intake was kept. This entry does not repin."
        and repin["body"].get("recorded") is False
        and copied_durable["record.json"] == life_durable["record.json"]
        and copied_durable["journal.json"] == life_durable["journal.json"]
        and life_after == life_durable,
        {
            "reason": hold.get("reason"),
            "publish_correction": publish_copy["body"].get("correction"),
            "repin_correction": repin["body"].get("correction"),
            "form_has_hold": "instance_applicability" in form_copy["body"],
            "recover_equal": recover_1["stdout"] == recover_2["stdout"],
            "original_unchanged": life_after == life_durable,
        },
    )

    published = run(CANDIDATE, life, "publish", N5, ["--review", review_id or "missing"])
    published_read = run(CANDIDATE, life, "read", N5)
    published_page = file_sha(life / N5 / "05.01.md")
    published_copy = STAMP / "published-copy"
    shutil.copytree(life, published_copy)
    published_target = file_sha(published_copy / N5 / "05.01.md")
    published_again = run(CANDIDATE, published_copy, "publish", N5, ["--review", review_id or "missing"])
    case(
        "same-instance-publish-then-copy-holds",
        published["exit"] == 0
        and published["body"].get("published") is True
        and closed_ok(published["body"])
        and published_read["exit"] == 0
        and published_read["body"].get("stale") is False
        and "instance_applicability" not in published_read["body"]
        and published_target == published_page
        and published_again["exit"] == 1
        and published_again["body"].get("published") is False
        and hold_of(published_again["body"]).get("reason") == "different-root"
        and file_sha(published_copy / N5 / "05.01.md") == published_target,
        {"publish_exit": published["exit"], "copy_publish_exit": published_again["exit"], "stderr": published["stderr"].decode("utf-8", "replace")[-300:]},
    )

    manual = STAMP / "manual"
    make_n5(manual, "LAB artifact beside a manual review\n", "Director response: keep this sentence.")
    manual_bytes = (manual / N5 / "05.01.md").read_bytes()
    manual_record = record(manual, N5, judgment_path)
    manual_publish = run(CANDIDATE, manual, "publish", N5, ["--review", manual_record["record"]["body"].get("review_id") or "missing"])
    manual_copy = STAMP / "manual-copy"
    shutil.copytree(manual, manual_copy)
    manual_copy_publish = run(CANDIDATE, manual_copy, "publish", N5, ["--review", manual_record["record"]["body"].get("review_id") or "missing"])
    case(
        "manual-review-preserved",
        manual_publish["exit"] == 1
        and manual_publish["body"].get("correction") == "manual-review"
        and (manual / N5 / "05.01.md").read_bytes() == manual_bytes
        and manual_copy_publish["exit"] == 1
        and manual_copy_publish["body"].get("correction") == "Publication is blocked because the selected source changed after intake."
        and manual_copy_publish["body"].get("published") is False
        and manual_copy_publish["body"].get("judgment") == json.loads(judgment_path.read_text(encoding="utf-8"))
        and (manual_copy / N5 / "05.01.md").read_bytes() == manual_bytes,
        {"same": manual_publish["body"].get("correction"), "copy": manual_copy_publish["body"].get("correction")},
    )

    left = STAMP / "independent-left"
    right = STAMP / "independent-right"
    make_n5(left, "LAB artifact left\n", "PENDING.")
    make_n5(right, "LAB artifact right\n", "PENDING.")
    left_rec = record(left, N5, judgment_path)
    right_rec = record(right, N5, other_judgment)
    left_read = run(CANDIDATE, left, "read", N5)
    right_read = run(CANDIDATE, right, "read", N5)
    case(
        "independent-books",
        left_read["exit"] == 0
        and right_read["exit"] == 0
        and left_read["body"].get("stale") is False
        and right_read["body"].get("stale") is False
        and left_read["body"].get("review_id") != right_read["body"].get("review_id")
        and left_read["body"].get("next_action") != right_read["body"].get("next_action")
        and "instance_applicability" not in left_read["body"]
        and "instance_applicability" not in right_read["body"],
        {"left": left_read["body"].get("review_id"), "right": right_read["body"].get("review_id"), "left_record": left_rec["record"]["exit"], "right_record": right_rec["record"]["exit"]},
    )

    edited = STAMP / "edited-copy"
    shutil.copytree(copied, edited)
    record_before = file_sha(store_of(edited, N5) / "reviews" / str(review_id) / "record.json")
    artifact = edited / N5 / "evidence" / "b" / "artifact.md"
    artifact.write_bytes(b"LAB artifact changed after the copy\n")
    edited_prepare = run(CANDIDATE, edited, "prepare", N5)
    edited_read = run(CANDIDATE, edited, "read", N5)
    case(
        "changed-source-after-copy",
        edited_prepare["body"].get("measurement") == "incomplete"
        and hold_of(edited_prepare["body"]).get("reason") == "different-root"
        and edited_read["exit"] == 1
        and edited_read["body"].get("judgment") == json.loads(judgment_path.read_text(encoding="utf-8"))
        and file_sha(store_of(edited, N5) / "reviews" / str(review_id) / "record.json") == record_before,
        {"measurement": edited_prepare["body"].get("measurement"), "reason": hold_of(edited_prepare["body"]).get("reason")},
    )

    def live_instance(root: Path) -> str:
        raw = json.dumps(
            {"book": str(root.resolve()), "pass": PASS, "source": N5},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return sha(raw)

    def read_reason(name: str, mutate, reason: str) -> None:
        root = STAMP / name
        shutil.copytree(copied, root)
        before_record = file_sha(store_of(root, N5) / "reviews" / str(review_id) / "record.json")
        rewrite_intake(root, N5, lambda payload: mutate(payload, root))
        row = run(CANDIDATE, root, "read", N5)
        case(
            name,
            row["exit"] == 1
            and hold_of(row["body"]).get("reason") == reason
            and row["body"].get("judgment") == json.loads(judgment_path.read_text(encoding="utf-8"))
            and file_sha(store_of(root, N5) / "reviews" / str(review_id) / "record.json") == before_record,
            {"reason": hold_of(row["body"]).get("reason"), "exit": row["exit"]},
        )

    read_reason("missing-instance-field", lambda payload, _root: payload.pop("instance_id", None), "unbound")
    read_reason(
        "H1-book-rewritten-instance-kept",
        lambda payload, root: payload.__setitem__("book", str(root.resolve())),
        "identifier-disagreement",
    )
    read_reason(
        "H2-instance-rewritten-book-kept",
        lambda payload, root: payload.__setitem__("instance_id", live_instance(root)),
        "identifier-disagreement",
    )
    missing_root = str(STAMP / "missing-book-root")
    read_reason(
        "relocation-or-clone",
        lambda payload, _root: payload.__setitem__("book", missing_root),
        "relocation-or-clone",
    )
    read_reason(
        "unbound-book-spelling",
        lambda payload, _root: payload.__setitem__("book", "..\\outside"),
        "unbound",
    )

    n7 = STAMP / "n7"
    make_n7(n7, N7, False)
    n7_base = run(PASS05, n7, "prepare", N7)
    n7_cand = run(CANDIDATE, n7, "prepare", N7)
    n7_recorded = record(n7, N7, judgment_path)
    n7_base_read = run(PASS05, n7, "read", N7)
    n7_cand_read = run(CANDIDATE, n7, "read", N7)
    n7_copy = STAMP / "n7-copy"
    shutil.copytree(n7, n7_copy)
    n7_base_copy = run(PASS05, n7_copy, "read", N7)
    n7_cand_copy = run(CANDIDATE, n7_copy, "read", N7)
    bad = STAMP / "n7-bad"
    make_n7(bad, N7_BAD, True)
    bad_base = run(PASS05, bad, "prepare", N7_BAD)
    bad_cand = run(CANDIDATE, bad, "prepare", N7_BAD)
    bad_record = run(
        CANDIDATE,
        bad,
        "record",
        N7_BAD,
        ["--intake", bad_cand["body"].get("intake_id") or "missing", "--judgment", str(judgment_path)],
    )
    case(
        "n7-baseline-unchanged",
        n7_base["stdout"] == n7_cand["stdout"]
        and n7_base_read["stdout"] == n7_cand_read["stdout"]
        and n7_recorded["record"]["exit"] == 0
        and "custody-missing" in codes(n7_cand)
        and "n1-not-applicable" not in codes(n7_cand)
        and "malformed-n7-declaration" not in codes(n7_cand)
        and n7_base_copy["stdout"] == n7_cand_copy["stdout"]
        and n7_cand_copy["exit"] == n7_base_copy["exit"]
        and n7_cand_copy["body"].get("stale") == n7_base_copy["body"].get("stale")
        and bad_base["stdout"] == bad_cand["stdout"]
        and bad_cand["body"].get("measurement") == "incomplete"
        and "malformed-n7-declaration" in codes(bad_cand)
        and codes(bad_cand) == codes(bad_base)
        and bad_record["exit"] == 2
        and bad_record["body"].get("correction") == "The artifact measurement is incomplete. The judgment was not recorded.",
        {
            "n7_codes": codes(n7_cand),
            "bad_codes": codes(bad_cand),
            "copy_stale": n7_cand_copy["body"].get("stale"),
            "bad_record": bad_record["body"].get("correction"),
        },
    )

    spec = importlib.util.spec_from_file_location("review_instance_door_suite", LAB / "review_loop_tools.py")
    door = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(door)
    empty = STAMP / "pins-empty"
    empty.mkdir()
    missing_message = None
    try:
        door.perform(["prepare", "--book", str(life), "--source", N5, "--pass", PASS], empty)
    except door.Refuse as exc:
        missing_message = exc.message
    schema_root = STAMP / "pins-schema"
    schema_path = schema_root / "labs" / "review-instance-binding-pass01" / "review-loop.json"
    schema_path.parent.mkdir(parents=True)
    document = json.loads((LAB / "review-loop.json").read_text(encoding="utf-8"))
    document["schema"] = "review-loop-pins/7"
    schema_path.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    schema_message = None
    try:
        door.perform(["prepare", "--book", str(life), "--source", N5, "--pass", PASS], schema_root)
    except door.Refuse as exc:
        schema_message = exc.message
    missing_tool_root = STAMP / "pins-missing-tool"
    tool_path = missing_tool_root / "labs" / "review-instance-binding-pass01" / "review-loop.json"
    tool_path.parent.mkdir(parents=True)
    tool_path.write_bytes((LAB / "review-loop.json").read_bytes())
    missing_tool = None
    try:
        door.perform(["prepare", "--book", str(life), "--source", N5, "--pass", PASS], missing_tool_root)
    except door.Refuse as exc:
        missing_tool = exc.message
    tamper = STAMP / "pins-tamper"
    canonical_doc = json.loads((LAB / "review-loop.json").read_text(encoding="utf-8"))
    for item in canonical_doc["tools"].values():
        src = REPO / item["path"]
        dest = tamper / item["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
    decl_dest = tamper / "labs" / "review-instance-binding-pass01" / "review-loop.json"
    decl_dest.parent.mkdir(parents=True, exist_ok=True)
    decl_dest.write_bytes((LAB / "review-loop.json").read_bytes())
    wb_copy = tamper / "labs" / "review-instance-binding-pass01" / "workbook.py"
    flipped = bytearray(wb_copy.read_bytes())
    flipped[-1] = flipped[-1] ^ 1
    wb_copy.write_bytes(bytes(flipped))
    tamper_message = None
    try:
        door.perform(["prepare", "--book", str(life), "--source", N5, "--pass", PASS], tamper)
    except door.Refuse as exc:
        tamper_message = exc.message
    copied_wb = STAMP / "copied-workbook.py"
    sentinel = STAMP / "hostile-sentinel.txt"
    sentinel.write_bytes(b"sentinel\n")
    sentinel_sha = sha(sentinel.read_bytes())
    copied_wb.write_bytes((LAB / "workbook.py").read_bytes())
    copied_run = subprocess.run(
        [str(PY), "-B", str(copied_wb), "prepare", "--book", str(life), "--source", N5, "--pass", PASS],
        cwd=str(STAMP),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        check=False,
    )
    copied_door = STAMP / "copied-door.py"
    copied_door.write_bytes((LAB / "review_loop_tools.py").read_bytes())
    copied_door_run = subprocess.run(
        [str(PY), "-B", str(copied_door), "prepare", "--book", str(life), "--source", N5, "--pass", PASS],
        cwd=str(STAMP),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        check=False,
    )
    case(
        "dependency-and-root-refusals",
        missing_message == "review loop declaration is missing"
        and schema_message == "review loop declaration schema is not review-loop-pins/8"
        and missing_tool == "pinned tool is missing: app/review_loop_tools_v4.py"
        and tamper_message == "review-instance pin mismatch"
        and copied_run.returncode == 2
        and b"not at its canonical root" in copied_run.stderr
        and copied_door_run.returncode == 2
        and b"not at its canonical root" in copied_door_run.stderr
        and sha(sentinel.read_bytes()) == sentinel_sha,
        {
            "missing": missing_message,
            "schema": schema_message,
            "tool": missing_tool,
            "tamper": tamper_message,
            "copied_workbook": copied_run.returncode,
            "copied_door": copied_door_run.returncode,
        },
    )

    after = frozen_map()
    case("frozen-inputs-unchanged", before == after, {"changed": sorted(set(before) ^ set(after)) or [key for key in before if before.get(key) != after.get(key)]})
    authored = [
        LAB / "workbook.py",
        LAB / "review_loop_tools.py",
        LAB / "review-loop.json",
        LAB / "INTEGRATION.md",
        LAB / "drive.py",
        LAB / "candidate" / "app" / "librarian.py",
    ]
    cr = [str(path.relative_to(REPO)) for path in authored if b"\r" in path.read_bytes()]
    case("authored-lf", cr == [], {"cr": cr})
    report = {
        "schema": "review-instance-binding-suite/1",
        "stamp": str(STAMP),
        "passed": len([item for item in CASES if item["status"] == "PASS"]),
        "failed": len(FAILS),
        "cases": CASES,
    }
    (STAMP / "suite.json").write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(f"PASS {report['passed']} FAIL {report['failed']}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
