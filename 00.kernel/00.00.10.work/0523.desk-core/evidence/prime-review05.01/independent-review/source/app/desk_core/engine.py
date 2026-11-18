"""Desk-core commands. Records are authoritative. Faces are projections."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from . import face
from .bookio import (
    atomic_write,
    exclusive_write,
    file_lock,
    header_body,
    open_book,
    outside_book,
    read_bytes,
    read_json,
    write_json,
)
from .identity import (
    DATE_RE,
    HEX64_RE,
    LIMITS,
    SLUG_RE,
    Placement,
    Refused,
    agreement_sha,
    canonical,
    evidence_rows,
    evidence_sha,
    exact_keys,
    one_line,
    place,
    prose,
    require_object,
    review_binding,
    sha256,
    string_list,
    task_binding,
)

RESULT = "desk-core-result/1"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _result(command: str, **fields: object) -> dict[str, object]:
    body: dict[str, object] = {
        "schema": RESULT,
        "ok": True,
        "command": command,
        "accepted": False,
        "limitations": list(LIMITS),
    }
    body.update(fields)
    return body


def _logical(name: object) -> str:
    text = one_line(name, "artifact", 128)
    if "\\" in text or text.startswith("/"):
        raise Refused("artifact", "artifact name is refused")
    parts = text.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise Refused("artifact", "artifact name is refused")
    return text


def _scope(value: object) -> dict[str, list[str]]:
    obj = require_object(value, "scope")
    exact_keys(obj, {"in", "out"}, "scope")
    return {
        "in": string_list(obj["in"], "scope.in", empty_ok=False),
        "out": string_list(obj["out"], "scope.out", empty_ok=True),
    }


def _task_input(raw: dict[str, object]) -> dict[str, object]:
    exact_keys(
        raw,
        {
            "page",
            "subject",
            "pass",
            "title",
            "body",
            "expected_outputs",
            "scope",
            "agreement",
            "bound_evidence",
            "synthetic",
        },
        "task",
    )
    if raw["synthetic"] is not True:
        raise Refused("synthetic", "task must be labeled synthetic")
    located = place(raw["page"], raw["subject"], raw["pass"])
    title = one_line(raw["title"], "title", 160)
    body = prose(raw["body"], "body", 20000)
    agreement = prose(raw["agreement"], "agreement", 20000)
    outputs = string_list(raw["expected_outputs"], "expected_outputs", empty_ok=False)
    scope = _scope(raw["scope"])
    evidence = evidence_rows(raw["bound_evidence"])
    fields: dict[str, object] = {
        "title": title,
        "body": body,
        "expected_outputs": outputs,
        "scope": scope,
        "agreement": agreement,
        "bound_evidence": evidence,
    }
    binding = task_binding(fields)
    fields.update(
        {
            "schema": "desk-core-task/1",
            "page": located.page,
            "subject": located.subject,
            "pass": located.pass_id,
            "kind": located.kind,
            "synthetic": True,
            "task_binding_sha256": binding,
            "agreement_sha256": agreement_sha(agreement),
            "evidence_sha256": evidence_sha(evidence),
        }
    )
    return fields


def _paths(book: Path, located: Placement) -> dict[str, Path]:
    source = book / located.source_name
    custody_root = book / located.custody_name
    stem = f"05.{located.pass_id}"
    review_stem = f"06.{located.pass_id}" if located.kind == "N7NN" else stem
    return {
        "source": source,
        "custody": custody_root,
        "task": source / f"{stem}.task.json",
        "face": source / located.face_name,
        "release": source / f"{stem}.release.json",
        "claim": source / f"{stem}.claim.json",
        "assertion": source / f"{stem}.assertion.json",
        "claim_conflict": source / f"{stem}.claim-conflict.json",
        "release_conflict": source / f"{stem}.release-conflict.json",
        "review_conflict": source / f"{stem}.review-conflict.json",
        "review_json": source / f"{review_stem}.review.json",
        "review_md": source / f"{review_stem}.review.md",
        "return_md": custody_root / f"{stem}.return.md",
        "receipt": custody_root / f"{stem}.receipt.json",
        "artifacts": custody_root / f"{stem}.artifacts",
        "partial": custody_root / f"{stem}.partial.json",
        "staging": custody_root / f"{stem}.staging",
        "conflicts": custody_root / f"{stem}.conflicts",
        "line": custody_root / "line.json",
        "index": custody_root / "01.md",
        "page_index": source / "01.md",
        "lock": source / f"{stem}.lock",
        "book_lock": book / ".desk.lock",
    }


def _load_task(paths: dict[str, Path]) -> dict[str, object]:
    if not paths["task"].is_file():
        raise Refused("task-missing", "no task record at this page and pass")
    task = read_json(paths["task"], "task")
    if task.get("schema") != "desk-core-task/1":
        raise Refused("task-schema", "task schema is not desk-core-task/1")
    binding = task_binding(
        {
            "title": task["title"],
            "body": task["body"],
            "expected_outputs": task["expected_outputs"],
            "scope": task["scope"],
            "agreement": task["agreement"],
            "bound_evidence": task["bound_evidence"],
        }
    )
    if binding != task.get("task_binding_sha256"):
        raise Refused("task-binding", "stored task binding does not recompute")
    return task


def _write_page_index(book: Path, source: Path, located: Placement) -> None:
    passes: list[str] = []
    if source.is_dir():
        for entry in sorted(source.iterdir(), key=lambda item: item.name):
            if entry.is_symlink() or not entry.is_file():
                continue
            name = entry.name
            if name.startswith("05.") and name.endswith(".task.json"):
                passes.append(name[len("05.") : -len(".task.json")])
    lines = [
        f"# {located.source_name}",
        "",
        "schema: desk-core-page/1",
        f"kind: {located.kind}",
        "note: this index is a projection, not assignment authority",
        "",
        "passes:",
    ]
    if not passes:
        lines.append("(none)")
    else:
        lines.extend(f"- {item}" for item in passes)
    lines.append("")
    atomic_write(source / "01.md", ("\n".join(lines)).encode("utf-8"))


def _projection_conflicts(task: dict[str, object], paths: dict[str, Path]) -> list[str]:
    conflicts: list[str] = []
    if not paths["face"].is_file():
        return ["face-missing"]
    data = read_bytes(paths["face"])
    prefix, _suffix = face.split_before_release(data)
    if prefix != face.render_prefix(task):
        conflicts.append("assignment-projection-conflict")
    release = read_json(paths["release"], "release") if paths["release"].is_file() else None
    claim = read_json(paths["claim"], "claim") if paths["claim"].is_file() else None
    if face.section_body(data, face.RELEASE) != face._normalize(face.release_body(release)):
        conflicts.append("release-projection-conflict")
    if face.section_body(data, face.CLAIM) != face._normalize(face.claim_body(claim)):
        conflicts.append("claim-projection-conflict")
    return conflicts


def _artifact_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(directory, followlinks=False):
        base = Path(dirpath)
        if base.is_symlink():
            raise Refused("symlink", "artifact directory is a symlink")
        for name in dirnames:
            if (base / name).is_symlink():
                raise Refused("symlink", "artifact symlink is refused")
        for name in filenames:
            path = base / name
            if path.is_symlink() or not path.is_file():
                raise Refused("artifact", f"artifact is not a plain file: {name}")
            found.append(path)
    return found


def _verify_receipt(paths: dict[str, Path]) -> dict[str, object] | None:
    if not paths["receipt"].is_file():
        return None
    receipt = read_json(paths["receipt"], "receipt")
    if receipt.get("schema") != "desk-core-receipt/1":
        raise Refused("receipt-schema", "receipt schema mismatch")
    core = _receipt_core(receipt)
    if sha256(canonical(core)) != receipt.get("receipt_sha256"):
        raise Refused("receipt-hash", "receipt hash does not recompute")
    blob = read_bytes(paths["return_md"])
    if sha256(blob) != receipt.get("return_sha256") or len(blob) != receipt.get("return_bytes"):
        raise Refused("receipt-bytes", "return bytes do not match the receipt")
    declared = receipt.get("artifacts")
    if type(declared) is not list:
        raise Refused("receipt-artifacts", "receipt artifacts are not a list")
    expected = {str(item["logical"]): item for item in declared if isinstance(item, dict)}
    files = _artifact_files(paths["artifacts"]) if paths["artifacts"].exists() else []
    seen: set[str] = set()
    root = paths["artifacts"]
    for path in files:
        logical = path.relative_to(root).as_posix()
        seen.add(logical)
        meta = expected.get(logical)
        data = read_bytes(path)
        if meta is None or sha256(data) != meta.get("sha256") or len(data) != meta.get("bytes"):
            raise Refused("receipt-bytes", "artifact bytes do not match the receipt")
    if seen != set(expected):
        raise Refused("receipt-bytes", "artifact set does not match the receipt")
    return receipt


def _receipt_core(receipt: dict[str, object]) -> dict[str, object]:
    keys = (
        "schema_core",
        "page",
        "subject",
        "pass",
        "kind",
        "placement",
        "worker",
        "task_binding_sha256",
        "return_sha256",
        "return_bytes",
        "artifacts",
        "unresolved_questions",
        "synthetic_record",
    )
    core = {key: receipt[key] for key in keys}
    return core


def _capture_phase(paths: dict[str, Path]) -> tuple[str, dict[str, object] | None, str | None]:
    problem = None
    receipt = None
    try:
        receipt = _verify_receipt(paths)
    except Refused as exc:
        problem = exc.code
        receipt = None
    if receipt is not None:
        return "captured", receipt, problem
    partial = paths["partial"].exists() or paths["staging"].exists() or paths["return_md"].exists()
    if partial or problem:
        return "partial", None, problem or "partial"
    return "absent", None, None


def _review_record(paths: dict[str, Path]) -> dict[str, object] | None:
    path = paths["review_json"]
    if not path.is_file():
        return None
    record = read_json(path, "review")
    if record.get("schema") != "desk-core-review/1":
        raise Refused("review-schema", "review schema mismatch")
    return record


def _binding_now(task: dict[str, object], receipt: dict[str, object] | None, review: dict[str, object] | None) -> str | None:
    if receipt is None or review is None:
        return None
    return review_binding(
        str(task["task_binding_sha256"]),
        str(receipt["receipt_sha256"]),
        str(task["agreement_sha256"]),
        str(task["evidence_sha256"]),
        str(review["review_identity"]),
    )


def derive(book: Path, located: Placement) -> dict[str, object]:
    paths = _paths(book, located)
    task = _load_task(paths)
    conflicts = _projection_conflicts(task, paths)
    if paths["claim_conflict"].is_file():
        conflicts.append("claim-conflict")
    if paths["release_conflict"].is_file():
        conflicts.append("release-conflict")
    if paths["review_conflict"].is_file():
        conflicts.append("review-conflict")
    if paths["conflicts"].is_dir() and any(paths["conflicts"].iterdir()):
        conflicts.append("receipt-conflict")
    phase, receipt, problem = _capture_phase(paths)
    if problem and problem not in ("partial",):
        conflicts.append(problem)
    release = read_json(paths["release"], "release") if paths["release"].is_file() else None
    claim = read_json(paths["claim"], "claim") if paths["claim"].is_file() else None
    assertion = read_json(paths["assertion"], "assertion") if paths["assertion"].is_file() else None
    review = _review_record(paths)
    current = str(task["task_binding_sha256"])
    release_fresh = bool(release) and release.get("task_binding_sha256") == current
    claim_fresh = bool(claim) and claim.get("task_binding_sha256") == current
    if release and not release_fresh:
        conflicts.append("release-stale")
    if claim and not claim_fresh:
        conflicts.append("claim-stale")
    expected_review = _binding_now(task, receipt, review)
    review_fresh = bool(review) and receipt is not None and review.get("review_binding_sha256") == expected_review
    if review and not review_fresh:
        conflicts.append("review-stale")
    pointer_conflict = _pointer_conflict(paths, task, receipt)
    if pointer_conflict:
        conflicts.append(pointer_conflict)
    questions: list[str] = []
    if receipt and isinstance(receipt.get("unresolved_questions"), list):
        questions.extend(str(item) for item in receipt["unresolved_questions"])
    if review and isinstance(review.get("unresolved_questions"), list):
        for item in review["unresolved_questions"]:
            if str(item) not in questions:
                questions.append(str(item))
    capture_present = phase == "captured"
    assignment_conflict = "assignment-projection-conflict" in conflicts
    if assignment_conflict:
        state, actor, action, derived_next = (
            "assignment-conflict",
            "prime",
            "projection disagrees with the task record; neither is accepted",
            True,
        )
    elif phase == "partial":
        state, actor, action, derived_next = (
            "partial",
            "worker",
            "interrupted or unverified write; not complete",
            True,
        )
    elif capture_present and review_fresh:
        action_record = review["next_action"] if review else {}
        if not isinstance(action_record, dict):
            raise Refused("review", "next action is not an object")
        state, actor, action, derived_next = (
            "reviewed",
            action_record.get("actor"),
            action_record.get("action"),
            False,
        )
    elif capture_present and review and not review_fresh:
        state, actor, action, derived_next = (
            "review-stale",
            "prime",
            "supplied review remains readable and is not current authority",
            True,
        )
    elif capture_present:
        state, actor, action, derived_next = (
            "awaiting-review",
            "prime",
            "retrieve the captured return and record a supplied judgment",
            True,
        )
    elif assertion and assertion.get("said_done") is True:
        state, actor, action, derived_next = (
            "said-done-without-capture",
            "worker",
            "worker says done but no captured return is present",
            True,
        )
    elif claim and not claim_fresh:
        state, actor, action, derived_next = (
            "claim-stale",
            "worker",
            "claim does not match the current task binding and is not accepted",
            True,
        )
    elif release and not release_fresh:
        state, actor, action, derived_next = (
            "release-stale",
            "director",
            "release does not match the current task binding and is not accepted",
            True,
        )
    elif claim_fresh:
        state, actor, action, derived_next = (
            "claimed",
            claim.get("worker") if claim else "worker",
            "submit the return on the matching custody line",
            True,
        )
    elif release_fresh:
        state, actor, action, derived_next = (
            "awaiting-claim",
            "worker",
            "claim the released task",
            True,
        )
    else:
        state, actor, action, derived_next = (
            "awaiting-release",
            "director",
            "record a supplied release",
            True,
        )
    complete = capture_present and not assignment_conflict and phase == "captured"
    if state in ("partial", "said-done-without-capture", "assignment-conflict"):
        complete = False
    return {
        "state": state,
        "complete": complete,
        "accepted": False,
        "next_actor": actor,
        "next_action": action,
        "derived": derived_next,
        "task_binding_sha256": current,
        "receipt_sha256": None if receipt is None else receipt.get("receipt_sha256"),
        "review_binding_sha256": None if review is None else review.get("review_binding_sha256"),
        "review_fresh": review_fresh,
        "conflicts": conflicts,
        "unresolved_questions": questions,
        "capture_phase": phase,
        "task": task,
        "receipt": receipt,
        "review": review,
        "release": release,
        "claim": claim,
        "kind": located.kind,
        "custody": located.custody_name,
    }


def _pointer_conflict(paths: dict[str, Path], task: dict[str, object], receipt: dict[str, object] | None) -> str | None:
    if not paths["face"].is_file():
        return None
    data = read_bytes(paths["face"])
    expected = face._normalize(face.pointer_body(_pointer_record(task, receipt)))
    actual = face.section_body(data, face.POINTER)
    if actual != expected:
        return "pointer-projection-conflict"
    return None


def _pointer_record(task: dict[str, object], receipt: dict[str, object] | None) -> dict[str, object] | None:
    if receipt is None:
        return None
    return {
        "placement": receipt["placement"],
        "custody": receipt["placement"],
        "return_file": f"05.{task['pass']}.return.md",
        "receipt_sha256": receipt["receipt_sha256"],
        "return_sha256": receipt["return_sha256"],
    }


def _located_from_record(record: dict[str, object]) -> Placement:
    return place(record["page"], record["subject"], record["pass"])


def init_book(book_text: str, label: str) -> dict[str, object]:
    label_text = one_line(label, "label", 80)
    book = outside_book(book_text)
    header = book / "00.desk.json"
    if book.exists():
        if not book.is_dir() or book.is_symlink():
            raise Refused("book-path", "book path is not a directory")
        if header.is_file() and not header.is_symlink():
            current = read_json(header, "00.desk.json")
            if current.get("schema") != "desk-core-book/1" or current.get("label") != label_text:
                raise Refused("book-exists", "book header already exists with different identity")
            return _result("init", idempotent=True, book=str(book), label=label_text)
        if any(book.iterdir()):
            raise Refused("book-not-empty", "refusing to adopt an unknown directory")
    else:
        book.mkdir(parents=False)
    write_json(header, header_body(label_text), exclusive=True)
    return _result("init", idempotent=False, book=str(book), label=label_text)


def record_task(book_text: str, raw: dict[str, object]) -> dict[str, object]:
    book = open_book(book_text)
    task = _task_input(raw)
    located = _located_from_record(task)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        _ensure_return_slot_unused(book, located, creating=False)
        paths["source"].mkdir(parents=True, exist_ok=True)
        with file_lock(paths["lock"]):
            if paths["task"].is_file():
                current = read_json(paths["task"], "task")
                if canonical(_public_task(current)) == canonical(_public_task(task)):
                    return _result(
                        "record-task",
                        idempotent=True,
                        task_binding_sha256=task["task_binding_sha256"],
                        page=located.source_name,
                        kind=located.kind,
                    )
                raise Refused("task-exists", "this pass already has different task bytes; use revise-task")
            write_json(paths["task"], task, exclusive=True)
            exclusive_write(paths["face"], face.render_face(task, located.kind))
            _write_page_index(book, paths["source"], located)
    return _result(
        "record-task",
        idempotent=False,
        task_binding_sha256=task["task_binding_sha256"],
        page=located.source_name,
        face=located.face_name,
        kind=located.kind,
        return_line=located.return_name,
    )


def _public_task(task: dict[str, object]) -> dict[str, object]:
    keys = (
        "title",
        "body",
        "expected_outputs",
        "scope",
        "agreement",
        "bound_evidence",
        "page",
        "subject",
        "pass",
        "kind",
    )
    return {key: task[key] for key in keys}


def _ensure_return_slot_unused(book: Path, located: Placement, creating: bool) -> None:
    if located.kind != "N5NN" or located.return_name is None:
        return
    prefix = located.return_name.split(".", 1)[0] + "."
    if not book.is_dir():
        return
    occupants = []
    for entry in book.iterdir():
        if entry.is_symlink():
            raise Refused("symlink", "book entry symlink is refused")
        if entry.name.startswith(prefix) and entry.name != located.return_name:
            occupants.append(entry.name)
    if occupants:
        raise Refused(
            "return-line-occupied",
            "matching N1NN number is already occupied by a different subject",
            occupants=sorted(occupants),
        )
    target = book / located.return_name
    if target.exists() and not creating:
        return
    if target.exists() and creating:
        line = target / "line.json"
        if line.is_file():
            current = read_json(line, "line")
            if current.get("source_page") != located.page or current.get("subject") != located.subject:
                raise Refused("return-line-occupied", "return line identity does not match this source")


def revise_task(book_text: str, raw: dict[str, object]) -> dict[str, object]:
    book = open_book(book_text)
    task = _task_input(raw)
    located = _located_from_record(task)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        with file_lock(paths["lock"]):
            if not paths["task"].is_file():
                raise Refused("task-missing", "cannot revise a missing task")
            previous = _load_task(paths)
            if previous["task_binding_sha256"] == task["task_binding_sha256"]:
                return _result("revise-task", idempotent=True, task_binding_sha256=task["task_binding_sha256"])
            data = read_bytes(paths["face"])
            _prefix, suffix = face.split_before_release(data)
            updated = face.render_prefix(task) + suffix
            write_json(paths["task"], task, exclusive=False)
            atomic_write(paths["face"], updated)
    return _result(
        "revise-task",
        idempotent=False,
        task_binding_sha256=task["task_binding_sha256"],
        previous_task_binding_sha256=previous["task_binding_sha256"],
        stale=True,
        accepted=False,
    )


def _party(raw: object, label: str, keys: set[str]) -> dict[str, object]:
    obj = require_object(raw, label)
    exact_keys(obj, keys, label)
    return obj


def register(book_text: str, raw: dict[str, object]) -> dict[str, object]:
    exact_keys(raw, {"page", "subject", "pass", "release", "claim", "synthetic"}, "register")
    if raw["synthetic"] is not True:
        raise Refused("synthetic", "register must be labeled synthetic")
    located = place(raw["page"], raw["subject"], raw["pass"])
    release_in = _party(raw["release"], "release", {"who", "date", "text"})
    claim_in = _party(raw["claim"], "claim", {"worker", "date", "text"})
    who = one_line(release_in["who"], "release.who", 80)
    worker = one_line(claim_in["worker"], "claim.worker", 80)
    for label, value in (("release.date", release_in["date"]), ("claim.date", claim_in["date"])):
        text = one_line(value, label, 10)
        if not DATE_RE.fullmatch(text):
            raise Refused("date", f"{label} must be YYYY-MM-DD")
    release_text = prose(release_in["text"], "release.text", 20000)
    claim_text = prose(claim_in["text"], "claim.text", 20000)
    book = open_book(book_text)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        with file_lock(paths["lock"]):
            task = _load_task(paths)
            binding = str(task["task_binding_sha256"])
            release_record = {
                "schema": "desk-core-release/1",
                "page": located.page,
                "subject": located.subject,
                "pass": located.pass_id,
                "task_binding_sha256": binding,
                "who": who,
                "date": release_in["date"],
                "text": release_text,
                "synthetic_record": True,
                "fabricated": False,
            }
            claim_record = {
                "schema": "desk-core-claim/1",
                "page": located.page,
                "subject": located.subject,
                "pass": located.pass_id,
                "task_binding_sha256": binding,
                "worker": worker,
                "date": claim_in["date"],
                "text": claim_text,
                "synthetic_record": True,
                "not_authentication": True,
            }
            if paths["release"].is_file() or paths["claim"].is_file():
                same_release = paths["release"].is_file() and _same(read_json(paths["release"], "release"), release_record)
                same_claim = paths["claim"].is_file() and _same(read_json(paths["claim"], "claim"), claim_record)
                if same_release and same_claim:
                    return _result("register", idempotent=True, task_binding_sha256=binding, accepted=False)
                if not same_release:
                    write_json(
                        paths["release_conflict"],
                        {"schema": "desk-core-conflict/1", "kind": "release", "refused_who": who, "accepted": False},
                    )
                    raise Refused("release-conflict", "different release bytes under the same pass were refused")
                write_json(
                    paths["claim_conflict"],
                    {
                        "schema": "desk-core-conflict/1",
                        "kind": "claim",
                        "refused_worker": worker,
                        "accepted": False,
                    },
                )
                raise Refused("claim-conflict", "different claim bytes under the same pass were refused")
            write_json(paths["release"], release_record, exclusive=True)
            write_json(paths["claim"], claim_record, exclusive=True)
            data = read_bytes(paths["face"])
            data = face.replace_body(data, face.RELEASE, face.release_body(release_record))
            data = face.replace_body(data, face.CLAIM, face.claim_body(claim_record))
            atomic_write(paths["face"], data)
    return _result("register", idempotent=False, task_binding_sha256=binding, worker=worker, accepted=False)


def _same(stored: dict[str, object], proposed: dict[str, object]) -> bool:
    ignore = {"recorded_at"}
    left = {key: value for key, value in stored.items() if key not in ignore}
    right = {key: value for key, value in proposed.items() if key not in ignore}
    return canonical(left) == canonical(right)


def assert_done(book_text: str, page: str, subject: str, pass_id: str, worker: str) -> dict[str, object]:
    located = place(page, subject, pass_id)
    worker_name = one_line(worker, "worker", 80)
    book = open_book(book_text)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        with file_lock(paths["lock"]):
            task = _load_task(paths)
            claim = read_json(paths["claim"], "claim") if paths["claim"].is_file() else None
            if claim is None or claim.get("worker") != worker_name:
                raise Refused("claim-missing", "assert-done requires the registered worker")
            if claim.get("task_binding_sha256") != task["task_binding_sha256"]:
                raise Refused("claim-stale", "stale claim cannot be treated as done")
            record = {
                "schema": "desk-core-assertion/1",
                "said_done": True,
                "worker": worker_name,
                "task_binding_sha256": task["task_binding_sha256"],
                "note": "assertion is not a capture",
                "synthetic_record": True,
            }
            if paths["assertion"].is_file() and _same(read_json(paths["assertion"], "assertion"), record):
                view = derive(book, located)
                return _result("assert-done", idempotent=True, state=view["state"], complete=False, accepted=False)
            if paths["assertion"].is_file():
                raise Refused("assertion-conflict", "a different done assertion is already recorded")
            write_json(paths["assertion"], record, exclusive=True)
            view = derive(book, located)
    return _result(
        "assert-done",
        idempotent=False,
        state=view["state"],
        complete=view["complete"],
        accepted=False,
        note="saying done does not capture a return",
    )


def _artifacts(value: object) -> list[dict[str, object]]:
    if type(value) is not list or len(value) > 20:
        raise Refused("artifact", "artifacts must be a short list")
    rows = []
    seen: set[str] = set()
    for item in value:
        obj = require_object(item, "artifact")
        exact_keys(obj, {"logical", "text"}, "artifact")
        logical = _logical(obj["logical"])
        if logical in seen:
            raise Refused("artifact", "artifact name repeats")
        seen.add(logical)
        text = prose(obj["text"], "artifact.text", 200000, empty_ok=True)
        blob = text.encode("utf-8")
        rows.append({"logical": logical, "text": text, "sha256": sha256(blob), "bytes": len(blob)})
    rows.sort(key=lambda row: str(row["logical"]))
    return rows


def submit_return(
    book_text: str,
    raw: dict[str, object],
    interrupt: bool,
    force_line: str | None,
    force_pass: str | None,
) -> dict[str, object]:
    exact_keys(
        raw,
        {
            "page",
            "subject",
            "pass",
            "worker",
            "return_text",
            "unresolved_questions",
            "artifacts",
            "synthetic",
            "task_binding_sha256",
        },
        "return",
    )
    if raw["synthetic"] is not True:
        raise Refused("synthetic", "return must be labeled synthetic")
    located = place(raw["page"], raw["subject"], raw["pass"])
    if force_pass is not None and force_pass != located.pass_id:
        raise Refused("wrong-pass", "return pass does not match the source pass", expected=located.pass_id)
    if force_line is not None and force_line != located.custody_name:
        raise Refused(
            "wrong-return-line",
            "return line does not match corrected placement",
            expected=located.custody_name,
        )
    worker = one_line(raw["worker"], "worker", 80)
    return_text = prose(raw["return_text"], "return_text", 200000)
    questions = string_list(raw["unresolved_questions"], "unresolved_questions", empty_ok=True)
    artifacts = _artifacts(raw["artifacts"])
    supplied_binding = one_line(raw["task_binding_sha256"], "task_binding_sha256", 64)
    if not HEX64_RE.fullmatch(supplied_binding):
        raise Refused("task-binding", "task binding hash is refused")
    book = open_book(book_text)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        with file_lock(paths["lock"]):
            task = _load_task(paths)
            if supplied_binding != task["task_binding_sha256"]:
                raise Refused("wrong-source-hash", "return source hash does not match the task binding")
            claim = read_json(paths["claim"], "claim") if paths["claim"].is_file() else None
            release = read_json(paths["release"], "release") if paths["release"].is_file() else None
            if release is None:
                raise Refused("release-missing", "a release record is required before capture")
            if release.get("task_binding_sha256") != task["task_binding_sha256"]:
                raise Refused("release-stale", "stale release cannot authorize a capture")
            if claim is None or claim.get("worker") != worker:
                raise Refused("claim-missing", "claim is missing or for a different worker")
            if claim.get("task_binding_sha256") != task["task_binding_sha256"]:
                raise Refused("claim-stale", "stale claim cannot authorize a capture")
            _ensure_return_slot_unused(book, located, creating=True)
            blob = return_text.encode("utf-8")
            art_meta = [{"logical": row["logical"], "sha256": row["sha256"], "bytes": row["bytes"]} for row in artifacts]
            placement_name = "page-local" if located.kind == "N7NN" else located.custody_name
            core = {
                "schema_core": "desk-core-receipt-core/1",
                "page": located.page,
                "subject": located.subject,
                "pass": located.pass_id,
                "kind": located.kind,
                "placement": placement_name,
                "worker": worker,
                "task_binding_sha256": task["task_binding_sha256"],
                "return_sha256": sha256(blob),
                "return_bytes": len(blob),
                "artifacts": art_meta,
                "unresolved_questions": questions,
                "synthetic_record": True,
            }
            receipt_sha = sha256(canonical(core))
            receipt = {
                "schema": "desk-core-receipt/1",
                **core,
                "receipt_sha256": receipt_sha,
                "recorded_at": _now(),
                "not_acceptance": True,
            }
            phase, existing, problem = _capture_phase(paths)
            if phase == "captured" and existing is not None:
                if _same(existing, receipt):
                    return _result(
                        "submit-return",
                        idempotent=True,
                        receipt_sha256=existing["receipt_sha256"],
                        complete=True,
                        accepted=False,
                        custody=located.custody_name,
                    )
                paths["conflicts"].mkdir(parents=True, exist_ok=True)
                conflict = paths["conflicts"] / f"{receipt_sha}.json"
                if not conflict.exists():
                    write_json(
                        conflict,
                        {
                            "schema": "desk-core-conflict/1",
                            "kind": "receipt",
                            "refused_receipt_sha256": receipt_sha,
                            "refused_return_sha256": core["return_sha256"],
                            "existing_receipt_sha256": existing.get("receipt_sha256"),
                            "accepted": False,
                        },
                        exclusive=True,
                    )
                raise Refused(
                    "receipt-conflict",
                    "changed bytes under the same return identity were refused",
                    existing_receipt_sha256=existing.get("receipt_sha256"),
                )
            if problem and phase != "partial" and existing is None and paths["receipt"].is_file():
                raise Refused("receipt-unusable", "existing receipt does not verify")
            _write_staging(paths, blob, artifacts)
            if interrupt:
                write_json(
                    paths["partial"],
                    {
                        "schema": "desk-core-partial/1",
                        "state": "partial",
                        "complete": False,
                        "note": "interrupted before receipt commit",
                    },
                )
                view = derive(book, located)
                return _result(
                    "submit-return",
                    ok=False,
                    state="partial",
                    complete=False,
                    accepted=False,
                    interrupted=True,
                    derived_state=view["state"],
                )
            _publish(book, located, paths, task, receipt, blob, artifacts)
            view = derive(book, located)
    return _result(
        "submit-return",
        idempotent=False,
        state=view["state"],
        complete=view["complete"],
        accepted=False,
        receipt_sha256=receipt_sha,
        custody=located.custody_name,
        task_binding_sha256=task["task_binding_sha256"],
    )


def _write_staging(paths: dict[str, Path], blob: bytes, artifacts: list[dict[str, object]]) -> None:
    staging = paths["staging"]
    if staging.is_symlink():
        raise Refused("symlink", "staging symlink is refused")
    if staging.exists():
        _remove_tree(staging)
    staging.mkdir(parents=True)
    exclusive_write(staging / "return.md", blob)
    art_root = staging / "artifacts"
    art_root.mkdir()
    for row in artifacts:
        target = art_root / str(row["logical"])
        if target.is_symlink():
            raise Refused("symlink", "artifact symlink is refused")
        target.parent.mkdir(parents=True, exist_ok=True)
        exclusive_write(target, str(row["text"]).encode("utf-8"))


def _remove_tree(path: Path) -> None:
    if path.is_symlink():
        raise Refused("symlink", "refusing to remove a symlink tree")
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        base = Path(dirpath)
        for name in filenames:
            item = base / name
            if item.is_symlink() or not item.is_file():
                raise Refused("symlink", "refusing to remove a non-file")
            item.unlink()
        for name in dirnames:
            item = base / name
            if item.is_symlink():
                raise Refused("symlink", "refusing to remove a symlink directory")
            item.rmdir()
    path.rmdir()


def _publish(
    book: Path,
    located: Placement,
    paths: dict[str, Path],
    task: dict[str, object],
    receipt: dict[str, object],
    blob: bytes,
    artifacts: list[dict[str, object]],
) -> None:
    custody = paths["custody"]
    custody.mkdir(parents=True, exist_ok=True)
    if located.kind == "N5NN":
        line = {
            "schema": "desk-core-return-line/1",
            "page": located.return_name.split(".", 1)[0] if located.return_name else "",
            "subject": located.subject,
            "source_page": located.page,
            "kind": "N1NN",
            "authority": False,
        }
        if not paths["line"].exists():
            write_json(paths["line"], line, exclusive=True)
    if paths["return_md"].exists() or paths["receipt"].exists():
        raise Refused("partial", "custody files exist without a verifying receipt; not publishing over them")
    exclusive_write(paths["return_md"], blob)
    for row in artifacts:
        target = paths["artifacts"] / str(row["logical"])
        target.parent.mkdir(parents=True, exist_ok=True)
        exclusive_write(target, str(row["text"]).encode("utf-8"))
    write_json(paths["receipt"], receipt, exclusive=True)
    if paths["staging"].exists():
        _remove_tree(paths["staging"])
    if paths["partial"].exists() and not paths["partial"].is_symlink():
        paths["partial"].unlink()
    data = read_bytes(paths["face"])
    data = face.replace_body(data, face.POINTER, face.pointer_body(_pointer_record(task, receipt)))
    atomic_write(paths["face"], data)
    if located.kind == "N5NN":
        _write_return_index(paths["custody"], located)
    _ = book


def _write_return_index(custody: Path, located: Placement) -> None:
    lines = [
        f"# {located.return_name}",
        "",
        "schema: desk-core-return-line/1",
        f"source: {located.page}.{located.subject}",
        "note: index is a projection, not custody authority",
        "",
        "passes:",
    ]
    found = False
    for entry in sorted(custody.iterdir(), key=lambda item: item.name):
        name = entry.name
        if name.startswith("05.") and name.endswith(".receipt.json") and entry.is_file() and not entry.is_symlink():
            lines.append(f"- {name[len('05.') : -len('.receipt.json')]}")
            found = True
    if not found:
        lines.append("(none)")
    lines.append("")
    atomic_write(custody / "01.md", "\n".join(lines).encode("utf-8"))


def retrieve(book_text: str, page: str, subject: str, pass_id: str) -> dict[str, object]:
    book = open_book(book_text)
    located = place(page, subject, pass_id)
    view = derive(book, located)
    receipt = view["receipt"]
    if not isinstance(receipt, dict):
        raise Refused("return-missing", "no verifying captured return to retrieve", state=view["state"], complete=False)
    text = read_bytes(_paths(book, located)["return_md"]).decode("utf-8")
    return _result(
        "retrieve",
        state=view["state"],
        complete=view["complete"],
        accepted=False,
        return_text=text,
        artifacts=receipt["artifacts"],
        unresolved_questions=view["unresolved_questions"],
        receipt_sha256=receipt["receipt_sha256"],
        task_binding_sha256=view["task_binding_sha256"],
        conflicts=view["conflicts"],
        note="retrieval is not a review and not acceptance",
    )


def review(book_text: str, raw: dict[str, object]) -> dict[str, object]:
    exact_keys(
        raw,
        {
            "page",
            "subject",
            "pass",
            "reviewer",
            "review_identity",
            "disposition",
            "findings",
            "dissent",
            "director_text",
            "unresolved_questions",
            "assessment",
            "next_action",
            "synthetic",
        },
        "review",
    )
    if raw["synthetic"] is not True:
        raise Refused("synthetic", "review must be labeled synthetic")
    located = place(raw["page"], raw["subject"], raw["pass"])
    reviewer = one_line(raw["reviewer"], "reviewer", 80)
    identity = one_line(raw["review_identity"], "review_identity", 80)
    disposition = one_line(raw["disposition"], "disposition", 400)
    findings = string_list(raw["findings"], "findings", empty_ok=True)
    dissent = prose(raw["dissent"], "dissent", 20000, empty_ok=True)
    director_text = prose(raw["director_text"], "director_text", 20000, empty_ok=True)
    questions = string_list(raw["unresolved_questions"], "unresolved_questions", empty_ok=True)
    assessment = prose(raw["assessment"], "assessment", 50000)
    action = require_object(raw["next_action"], "next_action")
    exact_keys(action, {"actor", "action"}, "next_action")
    actor = one_line(action["actor"], "next_action.actor", 40)
    if not SLUG_RE.fullmatch(actor):
        raise Refused("next-action", "next actor slug is refused")
    action_text = prose(action["action"], "next_action.action", 4000)
    book = open_book(book_text)
    with file_lock(book / ".desk.lock"):
        paths = _paths(book, located)
        with file_lock(paths["lock"]):
            task = _load_task(paths)
            phase, receipt, _problem = _capture_phase(paths)
            if phase != "captured" or receipt is None:
                raise Refused("return-missing", "review requires a verifying captured return", complete=False)
            binding = review_binding(
                str(task["task_binding_sha256"]),
                str(receipt["receipt_sha256"]),
                str(task["agreement_sha256"]),
                str(task["evidence_sha256"]),
                identity,
            )
            record = {
                "schema": "desk-core-review/1",
                "page": located.page,
                "subject": located.subject,
                "pass": located.pass_id,
                "reviewer": reviewer,
                "review_identity": identity,
                "disposition": disposition,
                "findings": findings,
                "dissent": dissent,
                "director_text": director_text,
                "unresolved_questions": questions,
                "assessment": assessment,
                "next_action": {"actor": actor, "action": action_text},
                "bound_task_binding_sha256": task["task_binding_sha256"],
                "bound_receipt_sha256": receipt["receipt_sha256"],
                "bound_agreement_sha256": task["agreement_sha256"],
                "bound_evidence_sha256": task["evidence_sha256"],
                "review_binding_sha256": binding,
                "synthetic_record": True,
                "not_acceptance": True,
            }
            if paths["review_json"].is_file():
                current = read_json(paths["review_json"], "review")
                if _same(current, record):
                    return _result("review", idempotent=True, review_binding_sha256=binding, accepted=False)
                write_json(
                    paths["review_conflict"],
                    {
                        "schema": "desk-core-conflict/1",
                        "kind": "review",
                        "refused_review_identity": identity,
                        "accepted": False,
                    },
                )
                raise Refused("review-conflict", "a different review under this pass was refused")
            before = read_bytes(paths["face"])
            if located.kind == "N5NN":
                rendered = face.replace_body(before, face.REVIEW, face.review_body(record))
                review_mark = face.REVIEW.encode("utf-8")
                note_mark = face.NOTE.encode("utf-8")
                if not rendered.startswith(before.split(review_mark, 1)[0] + review_mark):
                    raise Refused("review-bytes", "review splice changed bytes before the review heading")
                if not rendered.endswith(_suffix_from(before, note_mark)):
                    raise Refused("review-bytes", "review splice changed the record-note tail")
                atomic_write(paths["face"], rendered)
            else:
                exclusive_write(paths["review_md"], face.render_colab_review(record))
                after = read_bytes(paths["face"])
                if after != before:
                    raise Refused("review-bytes", "N7NN review must not modify the pack")
            write_json(paths["review_json"], record, exclusive=True)
            view = derive(book, located)
    return _result(
        "review",
        idempotent=False,
        state=view["state"],
        complete=view["complete"],
        accepted=False,
        review_binding_sha256=binding,
        task_binding_sha256=task["task_binding_sha256"],
        next_actor=view["next_actor"],
        next_action=view["next_action"],
        derived=False,
        unresolved_questions=questions,
        findings=findings,
    )


def _suffix_from(data: bytes, mark: bytes) -> bytes:
    index = data.find(b"\n" + mark)
    if index < 0:
        raise Refused("face", "record note heading is missing")
    return data[index + 1 :]


def show(book_text: str, page: str, subject: str, pass_id: str) -> dict[str, object]:
    book = open_book(book_text)
    located = place(page, subject, pass_id)
    view = derive(book, located)
    task = view["task"]
    if not isinstance(task, dict):
        raise Refused("task-missing", "task record is missing")
    return _result(
        "show",
        state=view["state"],
        complete=view["complete"],
        accepted=False,
        derived=view["derived"],
        next_actor=view["next_actor"],
        next_action=view["next_action"],
        task_binding_sha256=view["task_binding_sha256"],
        title=task["title"],
        body=task["body"],
        expected_outputs=task["expected_outputs"],
        scope=task["scope"],
        agreement=task["agreement"],
        bound_evidence=task["bound_evidence"],
        kind=view["kind"],
        custody=view["custody"],
        receipt_sha256=view["receipt_sha256"],
        conflicts=view["conflicts"],
        unresolved_questions=view["unresolved_questions"],
        review_fresh=view["review_fresh"],
    )


def recover(book_text: str, page: str, subject: str, pass_id: str) -> dict[str, object]:
    shown = show(book_text, page, subject, pass_id)
    shown["command"] = "recover"
    shown["recovered_from"] = "records"
    return shown


def pending(book_text: str) -> dict[str, object]:
    book = open_book(book_text)
    items = []
    for entry in sorted(book.iterdir(), key=lambda item: item.name):
        if entry.is_symlink() or not entry.is_dir():
            continue
        name = entry.name
        if "." not in name:
            continue
        page, subject = name.split(".", 1)
        if len(page) != 4 or page[1] not in ("5", "7"):
            continue
        for task_path in sorted(entry.iterdir(), key=lambda item: item.name):
            if task_path.is_symlink() or not task_path.is_file():
                continue
            if not (task_path.name.startswith("05.") and task_path.name.endswith(".task.json")):
                continue
            pass_id = task_path.name[len("05.") : -len(".task.json")]
            view = derive(book, place(page, subject, pass_id))
            items.append(
                {
                    "page": f"{page}.{subject}",
                    "pass": pass_id,
                    "state": view["state"],
                    "complete": view["complete"],
                    "accepted": False,
                    "next_actor": view["next_actor"],
                    "next_action": view["next_action"],
                    "derived": view["derived"],
                    "conflicts": view["conflicts"],
                }
            )
    return _result("pending", items=items, scan="book-root-and-source-page-only", task_ledger=False)
