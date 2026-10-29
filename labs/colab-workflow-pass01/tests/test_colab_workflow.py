"""Fixture tests for the N7NN workflow adapter. No model and no live book writes."""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import colab_workflow as cw  # noqa: E402


PY = sys.executable
CAPTURE = LAB.parent / "return-capture-pass01" / "return_capture.py"
HELPERS = CAPTURE.parent
COMMIT = "0123456789abcdef0123456789abcdef01234567"
FORBIDDEN = "Scores first. Opinion second."
NOTE = "\n".join(
    [
        "# Subject page",
        "",
        "## Alpha",
        "",
        "alpha body",
        "",
        "## Beta",
        "",
        "beta body",
        "",
        "section-id: S1",
        "",
    ]
).encode("utf-8")
DUP = "\n".join(["# Subject page", "", "## Alpha", "", "one", "", "## Alpha", "", "two", ""]).encode("utf-8")


class Skip(Exception):
    pass


EXECUTED = 0
FAILED = 0
SKIPPED = 0


def check(name, fn) -> None:
    global EXECUTED, FAILED, SKIPPED
    cw.WRITE_HOOK = None
    cw.RUN_PROCESS = None
    try:
        fn()
    except Skip as exc:
        SKIPPED += 1
        print(f"skip {name}: {exc}")
        return
    except Exception:
        FAILED += 1
        print(f"FAIL {name}")
        traceback.print_exc()
        return
    EXECUTED += 1
    print(f"ok {name}")


def run(argv: list[str]):
    code, out, err = cw.execute(argv)
    body = json.loads(out.decode("utf-8")) if out else None
    return code, body, err


def heading(value: str, occurrence=None) -> dict:
    return {"kind": "heading", "occurrence": occurrence, "value": value}


def section_id(value: str, occurrence=None) -> dict:
    return {"kind": "id", "occurrence": occurrence, "value": value}


def target(tid: str, path: str, section, data: bytes, file: str = "05.19.md") -> dict:
    return {
        "book": "00.00.10.work",
        "file": file,
        "id": tid,
        "page": "0508.return-capture",
        "section": section,
        "source": {
            "commit": COMMIT,
            "path": path,
            "repository": "synthetic",
            "sha256": cw.sha256(data),
        },
    }


def request_for(targets: list[dict], page: str = "0701.sample", pass_id: str = "05.01", title: str = "Sample question") -> dict:
    return {
        "assumptions": ["The supplied bytes are the source."],
        "book": "00.00.10.work",
        "capabilities": {"execute": "none", "network": "none", "read": "snapshots", "write": "none"},
        "challenge": "A better method may be proposed.",
        "dependencies": {"supplied": ["snapshots"], "unavailable": ["git objects"], "withheld": ["live book"]},
        "known_gaps": ["The workflow route is not seated."],
        "method": "Read the named section and challenge the claim.",
        "mode": "open-design",
        "page": page,
        "pass": pass_id,
        "permissions": "No live book write and no model call.",
        "purpose": "Learn the current design gap.",
        "question": "What is the bounded question?",
        "reading_order": ["subj/note.md"],
        "reasons": ["Prime still assembles this by hand."],
        "return_shape": "Qualitative findings with Hostile, Factfind, Overflow, and Unprompted.",
        "schema": "colab-open/1",
        "scope": "The named sections only.",
        "stop": "Stop on a missing source or an unsafe path.",
        "targets": targets,
        "title": title,
    }


def write_json(path: Path, value) -> None:
    path.write_bytes(cw.canonical(value))


def hashes(root: Path) -> dict[str, str]:
    found = {}
    if not root.exists():
        return found
    for dirpath, _dirs, filenames in os.walk(root):
        for name in filenames:
            file = Path(dirpath) / name
            if os.path.islink(file) or cw.is_reparse(file):
                continue
            found[file.relative_to(root).as_posix()] = cw.sha256(file.read_bytes())
    return found


def make_world(root: Path, note: bytes = NOTE, targets: list[dict] | None = None, page: str = "0701.sample", title: str = "Sample question", pass_id: str = "05.01"):
    book = root / "book"
    book.mkdir()
    sources = root / "sources"
    (sources / "subj").mkdir(parents=True)
    (sources / "subj" / "note.md").write_bytes(note)
    chosen = targets or [
        target("T01", "subj/note.md", heading("## Alpha"), note, "05.19.md"),
        target("T02", "subj/note.md", heading("## Beta"), note, "05.20.md"),
    ]
    request = request_for(chosen, page=page, pass_id=pass_id, title=title)
    path = root / "request.json"
    write_json(path, request)
    return book, request, sources, path, note


def open_cmd(book: Path, request: Path, sources: Path):
    return run(["open", "--book", str(book), "--request", str(request), "--sources", str(sources)])


def must_open(root: Path, **kwargs):
    book, request, sources, path, note = make_world(root, **kwargs)
    code, body, err = open_cmd(book, path, sources)
    if code != 0 or body["result"] != "complete":
        raise AssertionError((code, body, err))
    return book, request, sources, path, note


def record(book: Path, page: str = "0701.sample") -> dict:
    return json.loads((book / page / "investigation.json").read_text(encoding="utf-8"))


def flags(book: Path, page: str = "0701.sample", pass_id: str = "05.01") -> dict:
    code, body, err = run(["show", "--book", str(book)])
    if code != 0:
        raise AssertionError((body, err))
    for item in body["index"]["investigations"]:
        if item["page"] != page:
            continue
        for row in item["passes"]:
            if row["pass"] == pass_id:
                return row["flags"]
    raise AssertionError(body)


def tool(args: list[str]) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([PY, "-B", str(CAPTURE), *args], capture_output=True, env=env, shell=False)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout.decode() + proc.stderr.decode())


def capture_return(book: Path, slug: str, origin_page: str, origin_batch: str, retrospective: bool = False, prime: bool = False, do_capture: bool = True) -> str:
    tool(
        [
            "reserve",
            "--book",
            str(book),
            "--submission",
            slug,
            "--name",
            slug,
            "--origin-book",
            "00.00.10.work",
            "--origin-page",
            origin_page,
            "--origin-batch",
            origin_batch,
            "--expected-output",
            "note.md",
            "--submitter",
            "synthetic",
            "--reviewer",
            "Codex Prime",
            "--release",
            "Reservation only",
        ]
    )
    member = next(item.name for item in book.iterdir() if item.name.endswith("." + slug))
    if not do_capture:
        return member
    folder = book.parent / "returns"
    folder.mkdir(exist_ok=True)
    ret = folder / f"{slug}-return.md"
    art = folder / f"{slug}-note.md"
    ret.write_bytes(b"Qualitative result.\nDo not manufacture a number.\n")
    art.write_bytes(b"artifact\n")
    args = [
        "capture",
        "--book",
        str(book),
        "--submission",
        slug,
        "--return-file",
        str(ret),
        "--source-root",
        str(folder),
        "--artifact",
        f"{art.name}|note.md",
    ]
    if retrospective:
        args.extend(["--retrospective", "--source-commit", COMMIT])
    if prime:
        args.append("--return-includes-prime-review")
    tool(args)
    return member


def finding(fid: str, consequential: bool = False, target_id: str = "T01") -> dict:
    return {
        "affected_file": "05.19.md",
        "affected_page": "0508.return-capture",
        "consequential": consequential,
        "evidence_kind": "supplied",
        "id": fid,
        "observation": "The route is still manual.",
        "target": target_id,
        "topic": "route",
    }


def disposition(fid: str, action: str, followup=None, park=None, reply: str = "stored reply", target_id: str = "T01") -> dict:
    return {
        "action": action,
        "director_reply": reply,
        "director_reply_ref": None,
        "finding_id": fid,
        "followup_ref": followup,
        "park": park,
        "reason": "The caller supplied this reason.",
        "reviewer": "Codex Prime",
        "source_binding": target_id,
    }


def put(root: Path, name: str, value) -> Path:
    path = root / name
    write_json(path, value)
    return path


def package_for(root: Path, request: dict, note: bytes) -> tuple[Path, str]:
    dest = root / "package"
    digest = cw.build_synthetic_package(dest, request, {"subj/note.md": note})
    return dest, digest


def test_template() -> None:
    text = (LAB / "TEMPLATE.md").read_text(encoding="utf-8")
    if FORBIDDEN in text:
        raise AssertionError("template uses the scored-exam line")
    for item in cw.BRIEF_HEADINGS:
        if item not in text:
            raise AssertionError(item)
    if "Do not manufacture a number." not in text:
        raise AssertionError("qualitative line missing")


def test_schema_rules() -> None:
    schema = cw.load_binding_schema()
    data = NOTE
    document = {
        "investigation": {
            "book": "00.00.10.work",
            "page": "0701.sample",
            "pass": "05.01",
        },
        "schema": "colab-binding/1",
        "targets": [target("T01", "subj/note.md", heading("## Alpha"), data)],
    }
    cw.check_schema(document, schema)
    extra = copy.deepcopy(document)
    extra["extra"] = True
    try:
        cw.check_schema(extra, schema)
    except cw.Refuse as exc:
        if exc.reason != "unknown field":
            raise
    else:
        raise AssertionError("extra field accepted")
    bad = copy.deepcopy(document)
    bad["targets"][0]["section"]["occurrence"] = True
    try:
        cw.check_schema(bad, schema)
    except cw.Refuse as exc:
        if exc.reason != "malformed type":
            raise
    else:
        raise AssertionError("bool accepted as integer")


def test_band_and_open() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, sources, path, _note = make_world(root)
        door = book / "0700.band.colabs"
        door.mkdir()
        (door / "01.md").write_bytes(b"door\n")
        code, body, _err = open_cmd(book, path, sources)
        if code != 0 or body["wrote"] is not True:
            raise AssertionError(body)
        page = book / "0701.sample"
        names = sorted(item.name for item in page.iterdir())
        for required in ("01.md", "03.md", "05.01.md", "06.01.md", "06.md", "08.md", "investigation.json", "seal.json"):
            if required not in names:
                raise AssertionError(names)
        if "07.md" in names or any(name.endswith(".colab") for name in names):
            raise AssertionError(names)
        text = (page / "01.md").read_text(encoding="utf-8")
        for item in cw.BRIEF_HEADINGS:
            if item not in text:
                raise AssertionError(item)
        if FORBIDDEN in text or "One file is not the whole page." not in text:
            raise AssertionError("brief projection")
        if (door / "01.md").read_bytes() != b"door\n":
            raise AssertionError("door changed")
        before = hashes(page)
        code, body, _err = open_cmd(book, path, sources)
        if body["result"] != "repeat" or body["wrote"] is not False or hashes(page) != before:
            raise AssertionError(body)
        code, proposal, _err = run(["propose", "--book", str(book)])
        if proposal["proposal"] != "0702" or proposal["wrote"] is not False:
            raise AssertionError(proposal)
        if (book / "0702.anything").exists():
            raise AssertionError("propose allocated")


def test_band_refusals() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, request, sources, path, note = make_world(root)
        for page in ("0601.compute", "0700.door", "0800.nope", "0504.app"):
            request["page"] = page
            write_json(path, request)
            _code, body, _err = open_cmd(book, path, sources)
            if body["reason"] != "outside declared band":
                raise AssertionError((page, body))
        request["page"] = "0701"
        write_json(path, request)
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "malformed page":
            raise AssertionError(body)
        request = request_for(
            [target("T01", "subj/note.md", None, note)],
            page="0701.whole",
            title="Whole file",
        )
        write_json(path, request)
        code, body, _err = open_cmd(book, path, sources)
        if code != 0 or "whole named file" not in (book / "0701.whole" / "01.md").read_text(encoding="utf-8"):
            raise AssertionError(body)


def test_conflicts_and_second_pass() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, request, sources, path, note = must_open(root)
        first = copy.deepcopy(record(book)["passes"]["05.01"])
        other = book.parent / "other.json"
        changed = copy.deepcopy(request)
        changed["question"] = "A different question?"
        write_json(other, changed)
        _code, body, _err = open_cmd(book, other, sources)
        if body["reason"] != "occupied different content":
            raise AssertionError(body)
        changed = copy.deepcopy(request)
        changed["page"] = "0702.other"
        changed["pass"] = "05.01"
        write_json(other, changed)
        _code, body, _err = open_cmd(book, other, sources)
        if body["reason"] != "duplicate title":
            raise AssertionError(body)
        changed["title"] = "Second investigation"
        write_json(other, changed)
        before = hashes(book / "0701.sample")
        code, body, _err = open_cmd(book, other, sources)
        if code != 0 or hashes(book / "0701.sample") != before:
            raise AssertionError("existing investigation changed")
        changed = copy.deepcopy(request)
        changed["pass"] = "05.02"
        write_json(other, changed)
        code, body, _err = open_cmd(book, other, sources)
        if code != 0 or body["pass"] != "05.02":
            raise AssertionError(body)
        loaded = record(book)
        if loaded["passes"]["05.01"] != first:
            raise AssertionError("first pass rewritten")
        if "05.02.md" not in os.listdir(book / "0701.sample"):
            raise AssertionError("second pass projection missing")


def test_targets_and_sources() -> None:
    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, sources, path, note = make_world(root)
        duplicate = request_for(
            [
                target("T01", "subj/note.md", heading("## Alpha"), note),
                target("T01", "subj/note.md", heading("## Beta"), note, "05.20.md"),
            ]
        )
        write_json(path, duplicate)
        _code, body, _err = open_cmd(book, path, sources)
        cases.append(body["reason"] == "duplicate target")
        same = request_for(
            [
                target("T01", "subj/note.md", heading("## Alpha"), note),
                target("T02", "subj/note.md", heading("## Alpha"), note),
            ]
        )
        write_json(path, same)
        _code, body, _err = open_cmd(book, path, sources)
        cases.append(body["reason"] == "duplicate target")
        stale = request_for([target("T01", "subj/note.md", heading("## Alpha"), note)])
        stale["targets"][0]["source"]["sha256"] = "0" * 64
        write_json(path, stale)
        _code, body, _err = open_cmd(book, path, sources)
        cases.append(body["reason"] == "stale source hash")
        missing = request_for([target("T01", "subj/note.md", heading("## Missing"), note)])
        write_json(path, missing)
        _code, body, _err = open_cmd(book, path, sources)
        cases.append(body["reason"] == "unresolved section")
        escape = request_for([target("T01", "../note.md", heading("## Alpha"), note)])
        write_json(path, escape)
        _code, body, _err = open_cmd(book, path, sources)
        cases.append(body["reason"] == "unsafe path")
        if (book / "0701.sample").exists():
            raise AssertionError("refused open wrote a page")
        if not all(cases):
            raise AssertionError(cases)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "book"
        book.mkdir()
        sources = root / "sources"
        (sources / "subj").mkdir(parents=True)
        (sources / "subj" / "other.md").write_bytes(NOTE)
        request = request_for([target("T01", "subj/note.md", heading("## Alpha"), NOTE)])
        path = root / "request.json"
        write_json(path, request)
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "unresolved section":
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, sources, path, _note = make_world(root, note=DUP, targets=[target("T01", "subj/note.md", heading("## Alpha"), DUP)])
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "ambiguous section":
            raise AssertionError(body)
        request = request_for([target("T01", "subj/note.md", heading("## Alpha", 2), DUP)], title="Second occurrence")
        write_json(path, request)
        code, body, _err = open_cmd(book, path, sources)
        if code != 0:
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = request_for([target("T01", "subj/note.md", section_id("S1"), NOTE)], title="By id")
        book, _request, sources, path, _note = make_world(root, targets=good["targets"], title="By id")
        code, body, _err = open_cmd(book, path, sources)
        if code != 0:
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bad = [target("T01", "subj/note.md", section_id("S9"), NOTE)]
        book, _request, sources, path, _note = make_world(root, targets=bad, title="Missing id")
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "unresolved section":
            raise AssertionError(body)


def test_malformed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, request, sources, path, note = make_world(root)
        path.write_bytes(b'{"schema":"colab-open/1","schema":"again"}\n')
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "duplicate key":
            raise AssertionError(body)
        request["extra"] = 1
        write_json(path, request)
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "unknown field":
            raise AssertionError(body)
        request.pop("extra")
        request["targets"] = "T01"
        write_json(path, request)
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "malformed targets":
            raise AssertionError(body)
        many = []
        for index in range(33):
            many.append(target(f"T{index:02d}", "subj/note.md", None, note, f"f{index}.md"))
        broad = request_for(many)
        write_json(path, broad)
        _code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "limit":
            raise AssertionError(body)
        _code, body, _err = run(["propose", "--book", "relative-book"])
        if body["reason"] != "book path is not absolute":
            raise AssertionError(body)


def test_package_attach() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, request, _sources, _path, note = must_open(root)
        dest, digest = package_for(root, request, note)
        before = hashes(dest)
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(dest),
                "--expect-digest",
                digest,
            ]
        )
        if code != 0 or hashes(dest) != before:
            raise AssertionError(body)
        page_before = hashes(book / "0701.sample")
        code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(dest),
                "--expect-digest",
                digest,
            ]
        )
        if body["result"] != "repeat" or body["wrote"] is not False or hashes(book / "0701.sample") != page_before:
            raise AssertionError(body)
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(dest),
                "--expect-digest",
                "0" * 64,
            ]
        )
        if body["reason"] != "stale expected hash" or hashes(book / "0701.sample") != page_before:
            raise AssertionError(body)
        files = cw.read_package(dest)
        files["05.01.md"] = b"# 05.01\n\nDifferent supplied instructions.\n"
        files.pop("verification.json")
        digest2 = cw.digest_preimage(files)
        listed = [{"bytes": len(files[name]), "path": name, "sha256": cw.sha256(files[name])} for name in sorted(files)]
        files["verification.json"] = cw.canonical(
            {
                "binding_sha256": cw.sha256(files["binding.json"]),
                "digest": digest2,
                "digest_alg": cw.DIGEST_ALG,
                "files": listed,
                "request_sha256": cw.sha256(files["request.json"]),
                "schema": "colab-package-verification/1",
            }
        )
        other = root / "other-package"
        for name, data in files.items():
            path = other / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(other),
                "--expect-digest",
                digest2,
            ]
        )
        if body["reason"] != "conflicting bytes":
            raise AssertionError(body)
        files = cw.read_package(dest)
        binding = json.loads(files["binding.json"].decode("utf-8"))
        binding["investigation"]["page"] = "0702.other"
        wrong = root / "wrong-package"
        shutil.copytree(dest, wrong)
        (wrong / "binding.json").write_bytes(cw.canonical(binding))
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(wrong),
                "--expect-digest",
                digest,
            ]
        )
        if body["reason"] != "wrong origin":
            raise AssertionError(body)
        tail = root / "tail-package"
        shutil.copytree(dest, tail)
        (tail / "note.colab").write_bytes(b"tail\n")
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(tail),
                "--expect-digest",
                digest,
            ]
        )
        if body["reason"] != "colab tail":
            raise AssertionError(body)
        scored = root / "scored-package"
        shutil.copytree(dest, scored)
        (scored / "ENTRY.md").write_bytes((FORBIDDEN + "\n").encode("utf-8"))
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(scored),
                "--expect-digest",
                digest,
            ]
        )
        if body["reason"] != "scored-exam default in ENTRY.md":
            raise AssertionError(body)


def test_statements_and_close() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        statement = put(
            root,
            "release.json",
            {"by": "Director", "kind": "release", "on": "2026-10-29", "text": "released by the Director, 2026-10-29"},
        )
        code, body, _err = run(
            ["record-statement", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--statement", str(statement)]
        )
        if code != 0:
            raise AssertionError(body)
        shown = flags(book)
        if shown["draft"] is not True or shown["explicit_completion"] is not False:
            raise AssertionError(shown)
        loaded = record(book)
        if loaded["passes"]["05.01"]["statements"][0]["authority"] != "recorded-statement":
            raise AssertionError("statement became authority")
        unknown = put(root, "unknown.json", {"by": "Director", "kind": "seal", "on": "2026-10-29", "text": "seal it"})
        _code, body, _err = run(
            ["record-statement", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--statement", str(unknown)]
        )
        if body["reason"] != "claim/release unknown":
            raise AssertionError(body)
        findings = put(root, "findings.json", [finding("F01"), finding("F02", True)])
        code, _body, _err = run(
            ["record-findings", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--findings", str(findings)]
        )
        if code != 0:
            raise AssertionError(_body)
        held = put(root, "held-bad.json", [disposition("F01", "held")])
        _code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--dispositions", str(held)]
        )
        if body["reason"] != "malformed disposition":
            raise AssertionError(body)
        proposal = put(
            root,
            "proposal.json",
            {
                "affected_file": "05.19.md",
                "affected_page": "0508.return-capture",
                "finding_id": "F02",
                "schema": "colab-subject-proposal/1",
                "target": "T01",
                "text": "Keep the local why on the subject page after review.",
            },
        )
        subject = root / "subject"
        subject.mkdir()
        subject_file = subject / "05.19.md"
        subject_file.write_bytes(b"subject bytes\n")
        before = subject_file.read_bytes()
        code, body, _err = run(
            ["propose-note", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--proposal", str(proposal)]
        )
        if code != 0 or body["wrote_subject"] is not False or subject_file.read_bytes() != before:
            raise AssertionError(body)
        if not (book / "0701.sample" / "proposals" / "F02.md").exists():
            raise AssertionError("proposal missing")
        good_held = put(root, "held.json", [disposition("F01", "held", followup="proposal:F01")])
        code, _body, _err = run(
            ["record-disposition", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--dispositions", str(good_held)]
        )
        if code != 0 or flags(book)["held_followup"] is not True or flags(book)["explicit_completion"] is not False:
            raise AssertionError(flags(book))
        accepted = put(root, "accepted.json", [disposition("F02", "accepted")])
        calls = []

        def spy(argv):
            calls.append(argv)
            raise AssertionError("director reply was launched")

        cw.RUN_PROCESS = spy
        try:
            code, body, _err = run(
                [
                    "record-disposition",
                    "--book",
                    str(book),
                    "--page",
                    "0701.sample",
                    "--pass",
                    "05.01",
                    "--dispositions",
                    str(accepted),
                ]
            )
        finally:
            cw.RUN_PROCESS = None
        if code != 0 or calls:
            raise AssertionError(body)
        if flags(book)["accepted_without_terminal"] is not True or flags(book)["explicit_completion"] is not False:
            raise AssertionError(flags(book))
        stored = record(book)["passes"]["05.01"]["dispositions"]
        if not any(item["director_reply"] == "stored reply" for item in stored):
            raise AssertionError("reply was not stored")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        write_json(root / "findings.json", [finding("F01"), finding("F02", True)])
        run(["record-findings", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--findings", str(root / "findings.json")])
        write_json(
            root / "proposal.json",
            {
                "affected_file": "05.19.md",
                "affected_page": "0508.return-capture",
                "finding_id": "F02",
                "schema": "colab-subject-proposal/1",
                "target": "T01",
                "text": "Subject-local why.",
            },
        )
        soft = put(root, "soft.json", {"by": "Codex Prime", "explicit": False, "on": "2026-10-29", "text": "close"})
        _code, body, _err = run(["close", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--closure", str(soft)])
        if body["reason"] != "explicit close required":
            raise AssertionError(body)
        both = put(
            root,
            "both.json",
            [disposition("F01", "rejected", reply="import os; os.system('echo hi')"), disposition("F02", "accepted")],
        )
        code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--dispositions", str(both)]
        )
        if code != 0:
            raise AssertionError(body)
        if flags(book)["accepted_without_terminal"] is not True:
            raise AssertionError(flags(book))
        hard = put(root, "hard.json", {"by": "Codex Prime", "explicit": True, "on": "2026-10-29", "text": "close"})
        _code, body, _err = run(["close", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--closure", str(hard)])
        if body["reason"] != "consequential finding needs a proposal":
            raise AssertionError(body)
        run(["propose-note", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--proposal", str(root / "proposal.json")])
        code, body, _err = run(["close", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--closure", str(root / "hard.json")])
        if code != 0:
            raise AssertionError(body)
        loaded = record(book)["passes"]["05.01"]
        if flags(book)["explicit_completion"] is not True:
            raise AssertionError(flags(book))
        if not any(item["finding_id"] == "F01" and item["action"] == "rejected" for item in loaded["dispositions"]):
            raise AssertionError("rejection dropped")


def test_reconciliation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, note = must_open(root)
        current = root / "current.md"
        current.write_bytes(note + b"\nchanged\n")
        before = hashes(book / "0701.sample")
        code, body, _err = run(
            ["check-subject", "--book", str(book), "--page", "0701.sample", "--target", "T01", "--current", str(current)]
        )
        if code != 0 or body["match"] is not False or body["wrote"] is not False or hashes(book / "0701.sample") != before:
            raise AssertionError(body)
        historical = body["historical_sha256"]
        code, _body, _err = run(
            ["flag-reconciliation", "--book", str(book), "--page", "0701.sample", "--target", "T01", "--current", str(current)]
        )
        if code != 0:
            raise AssertionError(_body)
        write_json(root / "findings.json", [finding("F01")])
        run(["record-findings", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--findings", str(root / "findings.json")])
        write_json(root / "disp.json", [disposition("F01", "accepted")])
        _code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--dispositions", str(root / "disp.json")]
        )
        if body["reason"] != "reconciliation required":
            raise AssertionError(body)
        if record(book)["targets"][0]["source"]["sha256"] != historical:
            raise AssertionError("historical hash changed")
        write_json(root / "retain.json", {"decision": "retarget", "reason": "use the new bytes", "target": "T01"})
        _code, body, _err = run(
            ["retain-historical", "--book", str(book), "--page", "0701.sample", "--statement", str(root / "retain.json")]
        )
        if body["reason"] != "retarget":
            raise AssertionError(body)
        write_json(root / "retain.json", {"decision": "retain-historical", "reason": "Keep the original binding.", "target": "T01"})
        code, _body, _err = run(
            ["retain-historical", "--book", str(book), "--page", "0701.sample", "--statement", str(root / "retain.json")]
        )
        if code != 0 or record(book)["targets"][0]["source"]["sha256"] != historical:
            raise AssertionError("retain rewrote the hash")
        code, body, _err = run(
            ["record-disposition", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--dispositions", str(root / "disp.json")]
        )
        if code != 0:
            raise AssertionError(body)


def test_show_and_live() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        before = hashes(book)
        code, body, _err = run(["show", "--book", str(book)])
        if code != 0 or body["wrote"] is not False or hashes(book) != before or (book / "00.live.md").exists():
            raise AssertionError("show wrote")
        if "00.live" in json.dumps(body):
            raise AssertionError("show named 00.live")
    code, body, _err = run(["propose", "--book", r"D:\Git\lib-build\00.kernel\00.00.10.work"])
    if body["reason"] != "live work book is not a fixture":
        raise AssertionError(body)


def test_interrupt() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, sources, path, _note = make_world(root)

        def hook(file, _data):
            if file.name == "01.md":
                raise RuntimeError("stop")

        cw.WRITE_HOOK = hook
        try:
            code, body, _err = open_cmd(book, path, sources)
        finally:
            cw.WRITE_HOOK = None
        page = book / "0701.sample"
        if code != 2 or body["reason"] != "interrupted write" or body["wrote"] is not True:
            raise AssertionError(body)
        if not (page / "investigation.json").exists() or not (page / "partial.json").exists() or (page / "seal.json").exists():
            raise AssertionError("partial evidence missing")
        before = (page / "investigation.json").read_bytes()
        code, body, _err = open_cmd(book, path, sources)
        if body["reason"] != "resume refused" or (page / "investigation.json").read_bytes() != before:
            raise AssertionError(body)
        shown_before = hashes(page)
        code, body, _err = run(["show", "--book", str(book)])
        if body["index"]["investigations"][0]["attention"] != ["partial"] or hashes(page) != shown_before:
            raise AssertionError(body)


def test_junction() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        real = root / "real"
        real.mkdir()
        link = root / "link"
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)], capture_output=True)
        try:
            if proc.returncode != 0:
                raise AssertionError(proc.stderr.decode())
            _code, body, _err = run(["propose", "--book", str(link)])
            if body["reason"] != "unsafe path":
                raise AssertionError(body)
        finally:
            if os.path.lexists(link):
                os.rmdir(link)


def test_symlink() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, request, _sources, _path, note = must_open(root)
        dest, digest = package_for(root, request, note)
        link = dest / "linked.md"
        try:
            os.symlink(dest / "ENTRY.md", link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                raise Skip("WinError 1314")
            raise
        _code, body, _err = run(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--package",
                str(dest),
                "--expect-digest",
                digest,
            ]
        )
        if body["reason"] != "unsafe path":
            raise AssertionError(body)


def test_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)

        def boom(_argv):
            raise AssertionError("launched")

        for name in ("return_capture.py", "return_inspect.py"):
            helpers = root / name
            if helpers.exists():
                shutil.rmtree(helpers)
            shutil.copytree(HELPERS, helpers)
            file = helpers / name
            data = file.read_bytes()
            file.write_bytes(data[:-1] + bytes([data[-1] ^ 0x01]))
            cw.RUN_PROCESS = boom
            try:
                _code, body, _err = run(
                    [
                        "return-pointer",
                        "--book",
                        str(book),
                        "--page",
                        "0701.sample",
                        "--pass",
                        "05.01",
                        "--helpers",
                        str(helpers),
                    ]
                )
            finally:
                cw.RUN_PROCESS = None
            if body["reason"] != "pin mismatch":
                raise AssertionError((name, body))


def test_custody() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        member = capture_return(book, "primary-return", "0701.sample", "05.01", prime=True)
        calls = []

        def spy(argv):
            calls.append(list(argv))
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            return subprocess.run(argv, shell=False, capture_output=True, env=env)

        cw.RUN_PROCESS = spy
        try:
            code, body, _err = run(
                ["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"]
            )
        finally:
            cw.RUN_PROCESS = None
        if code != 0:
            raise AssertionError(body)
        commands = [item[3] for item in calls]
        if commands != ["inspect", "verify"]:
            raise AssertionError(commands)
        pointer = record(book)["passes"]["05.01"]["return_pointer"]
        if pointer["member"] != member or pointer["custody"] != list(cw.CUSTODY_LINES):
            raise AssertionError(pointer)
        if pointer["includes_prime_review"] is not True:
            raise AssertionError(pointer)
        shown = flags(book)
        if not (shown["custody_complete"] and shown["review_pending"] and not shown["explicit_completion"] and not shown["accepted_without_terminal"]):
            raise AssertionError(shown)
        text = (book / "0701.sample" / "05.01.md").read_text(encoding="utf-8")
        if member not in text or "Qualitative result" in text:
            raise AssertionError("pass page copied the return body or dropped the pointer")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        before = hashes(book / "0701.sample")
        capture_return(book, "subject-0508", "0508.return-capture", "05.19")
        _code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if body["reason"] != "wrong origin" or hashes(book / "0701.sample") != before:
            raise AssertionError(body)
        capture_return(book, "impl-0510", "0510.colab-tools", "05.02")
        _code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if body["reason"] != "wrong origin":
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        capture_return(book, "reserved-only", "0701.sample", "05.01", do_capture=False)
        before = hashes(book / "0701.sample")
        _code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if body["reason"] != "partial custody" or hashes(book / "0701.sample") != before:
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        first = capture_return(book, "first-return", "0701.sample", "05.01")
        second = capture_return(book, "second-return", "0701.sample", "05.01")
        _code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if body["reason"] != "ambiguous custody":
            raise AssertionError(body)
        code, body, _err = run(
            ["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01", "--member", first]
        )
        if code != 0 or body["member"] != first or second == first:
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        retro = capture_return(book, "retro-return", "0701.sample", "05.01", retrospective=True)
        _code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if body["reason"] != "retrospective capture is secondary":
            raise AssertionError(body)
        code, body, _err = run(
            [
                "return-pointer",
                "--book",
                str(book),
                "--page",
                "0701.sample",
                "--pass",
                "05.01",
                "--member",
                retro,
                "--secondary",
            ]
        )
        if code != 0 or record(book)["passes"]["05.01"]["return_pointer"]["secondary"] is not True:
            raise AssertionError(body)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book, _request, _sources, _path, _note = must_open(root)
        primary = capture_return(book, "primary-return", "0701.sample", "05.01")
        capture_return(book, "retro-return", "0701.sample", "05.01", retrospective=True)
        code, body, _err = run(["return-pointer", "--book", str(book), "--page", "0701.sample", "--pass", "05.01"])
        if code != 0 or body["member"] != primary:
            raise AssertionError(body)


def main() -> int:
    check("template", test_template)
    check("schema rules", test_schema_rules)
    check("band and open", test_band_and_open)
    check("band refusals", test_band_refusals)
    check("conflicts and second pass", test_conflicts_and_second_pass)
    check("targets and sources", test_targets_and_sources)
    check("malformed", test_malformed)
    check("package attach", test_package_attach)
    check("statements and close", test_statements_and_close)
    check("reconciliation", test_reconciliation)
    check("show and live", test_show_and_live)
    check("interrupt", test_interrupt)
    check("junction", test_junction)
    check("file symlink", test_symlink)
    check("pin", test_pin)
    check("custody", test_custody)
    print(f"executed {EXECUTED}")
    print(f"skipped {SKIPPED}")
    print(f"failed {FAILED}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
