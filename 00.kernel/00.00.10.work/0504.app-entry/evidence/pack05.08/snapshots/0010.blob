#!/usr/bin/env python3
"""Command-path checks for the development entry.

Expected refusals are counted apart from passes and from unexpected failures.
These checks are not an operating-system sandbox.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
RUNNER_002 = REPO / "00.kernel/00.00.01.law/0302.run/02.run.002.py"
RUNNER = REPO / "00.kernel/00.00.01.law/0302.run/02.run.003.py"
PAYLOAD = REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/02.inventory.py"
CARD = REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/02.md"
SAMPLE = REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/sample-book"
EXPECTED = REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/expected-inventory.json"
CONFIG = REPO / "app" / "development-workspace.json"
CANDIDATE = "00.kernel/00.00.01.law/0310.inventory/02.inventory.py"
WORK_ITEM = "00.kernel/00.00.10.work/0504.app-entry/05.01.md"
RECORD = "00.kernel/00.00.10.work/0401.goal/06.01.md"
SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
PINNED = {
    "00.kernel/00.00.01.law/0302.run/02.run.001.py":
        "af207d4d4f68ddcc2c22b7b1dced081b29dcbbfa6675d152ff7efa37871dcb8c",
    "00.kernel/00.00.01.law/0302.run/02.run.002.py":
        "4a962d3a6edd26428b75e27ad82113708e510a1e770522d34b9e8bb11ec2b0f4",
    "00.kernel/00.00.01.law/0302.run/02.md":
        "95062ea60f8b923c3bda1cf603f394e54e56d961f42af13c9520031bf13bb95f",
    # Committed additive correction in b471a24. This batch does not edit the page.
    "00.kernel/00.00.10.work/0502.workflow-start/05.01.md":
        "7f43ea75f0fc6f01229e0171312bc1f42a067df7a27e9689eab602d5f1bcfe17",
    "00.kernel/00.00.10.work/0014.design/01.001.md":
        "a04962e94ae54bcb0fc2ae42dd36ff6fc33822427cb2a983211d069aeaf4b610",
    "00.kernel/00.00.10.work/0011.contents/01.002.md":
        "a4e31538a92f499173075ada8e13344a5a207ab3cdd738fb227f7ba92c768ab7",
    "labs/bootstrap-establish-pass01/render_live.py":
        "45c738cfaaa1cb26204e0400040aa51c11fe3bfe91c0a7116b4401cf84b57d09",
    "labs/bootstrap-git-bytes-pass01/gitbytes.py":
        "e1c3022ac3c5611938ea418368d8eaf9aba24be1e50cdbbf9db1ca5adf1ede31",
    "returns/pack-B-prime-report-2026-10-26.md":
        "824784cbc762569832e03e44929091dfd3486bc89e5a4f24e218394184e5ba37",
}
MUTABLE_GUARDS = (
    "00.kernel/00.00.10.work/0401.goal/06.01.md",
    "00.kernel/00.live.md",
    "00.kernel/00.00.01.law/0302.run/02.run.002.py",
    "00.kernel/00.00.01.law/0302.run/02.run.003.py",
    "app/development-workspace.json",
    "app/librarian.py",
    "app/context.py",
    "app/README.md",
    "README.md",
    "labs/bootstrap-establish-pass01/write_contents.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lf(text: str) -> bytes:
    return text.replace("\r\n", "\n").encode("utf-8")


class Suite:
    def __init__(self) -> None:
        self.passed = []
        self.refusals = []
        self.skipped = []
        self.failed = []
        self.log = []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        self.log.append(f"PASS {name}")
        print(f"PASS {name}")

    def refusal(self, name: str) -> None:
        self.refusals.append(name)
        self.log.append(f"REFUSAL {name}")
        print(f"REFUSAL {name}")

    def skip(self, name: str, detail: str) -> None:
        self.skipped.append(name)
        self.log.append(f"SKIP {name}: {detail}")
        print(f"SKIP {name}: {detail}")

    def fail(self, name: str, detail: str) -> None:
        self.failed.append(name)
        self.log.append(f"FAIL {name}: {detail}")
        print(f"FAIL {name}: {detail}")


SUITE = Suite()
FOREIGN = Path(tempfile.mkdtemp(prefix="librarian-0504-cwd-"))
(FOREIGN / "note.txt").write_bytes(b"do-not-read\n")


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [PY, "-B", str(LIBRARIAN), *args],
        cwd=str(cwd or FOREIGN),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    shown = " ".join(proc.args) if isinstance(proc.args, list) else str(proc.args)
    SUITE.log.append(f"$ {shown}")
    SUITE.log.append(f"cwd: {cwd or FOREIGN}")
    SUITE.log.append(f"exit: {proc.returncode}")
    SUITE.log.append("stdout:")
    SUITE.log.append(proc.stdout)
    SUITE.log.append("stderr:")
    SUITE.log.append(proc.stderr)
    return proc


def check(name: str, fn) -> None:
    try:
        fn()
    except Exception:
        SUITE.fail(name, traceback.format_exc())


def expect_stop(name: str, proc: subprocess.CompletedProcess[str], snippet: str) -> None:
    bad = []
    if proc.returncode != 2:
        bad.append(f"exit {proc.returncode}")
    if "Traceback" in proc.stderr or "Traceback" in proc.stdout:
        bad.append("traceback")
    if not proc.stderr.startswith("stop:"):
        bad.append("stderr did not start with stop:")
    if snippet not in proc.stderr:
        bad.append(f"missing {snippet!r}")
    if proc.stdout.strip():
        bad.append("stdout was not empty")
    if bad:
        raise AssertionError("; ".join(bad))
    SUITE.refusal(name)


def record_text(state: str, **overrides: str) -> bytes:
    fields = {
        "record": "current-assignment",
        "schema": SCHEMA,
        "desk": "00.kernel",
        "book": "00.00.10.work",
        "workflow_space": "0",
        "current_work": WORK_ITEM,
        "pack": WORK_ITEM,
        "assignment_state": state,
        "waits_on": "review",
        "next": "next step",
        "updated": "2026-10-26",
    }
    fields.update(overrides)
    order = [
        "record", "schema", "desk", "book", "workflow_space", "current_work",
        "pack", "assignment_state", "waits_on", "next", "updated",
    ]
    return lf("".join(f"{key}: {fields[key]}\n" for key in order))


def plant(root: Path, state: str = "released", **overrides: str) -> None:
    (root / "00.kernel/00.00.10.work/0401.goal").mkdir(parents=True, exist_ok=True)
    (root / "00.kernel/00.00.01.law").mkdir(parents=True, exist_ok=True)
    (root / RECORD).write_bytes(record_text(state, **overrides))
    (root / WORK_ITEM).parent.mkdir(parents=True, exist_ok=True)
    (root / WORK_ITEM).write_bytes(b"fixture work item\n")


def plant_runner(root: Path, config_text: str | None = None) -> None:
    text = CONFIG.read_bytes() if config_text is None else lf(config_text)
    config = json.loads(text.decode("utf-8"))
    rel = str(config["runner"]["path"]).replace("\\", "/")
    dest = root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((REPO / rel).read_bytes())
    legacy = root / "00.kernel/00.00.01.law/0302.run/02.run.002.py"
    if legacy.resolve() != dest.resolve():
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_bytes(RUNNER_002.read_bytes())
    (root / "app").mkdir(parents=True, exist_ok=True)
    (root / "app/development-workspace.json").write_bytes(text)


def make_fixture(root: Path, state: str = "released", **overrides: str) -> str:
    plant(root, state, **overrides)
    page = root / "00.kernel/00.00.01.law/0310.inventory"
    page.mkdir(parents=True, exist_ok=True)
    (page / "02.inventory.py").write_bytes(PAYLOAD.read_bytes())
    (page / "02.md").write_bytes(CARD.read_bytes())
    shutil.copytree(SAMPLE, root / "00.kernel/00.00.20.sample")
    digest = sha(PAYLOAD)
    fixture = {
        "schema": "librarian-fixture",
        "version": 1,
        "identity": "0504-inventory-pass01",
        "compute_page": "0310.inventory",
        "inventory_book": "00.00.20.sample",
        "output": "output/inventory.json",
        "required_face": "01.md",
        "payload_sha256": digest,
    }
    (root / "fixture.json").write_bytes(lf(json.dumps(fixture, indent=2) + "\n"))
    return digest


def snap(paths: tuple[str, ...]) -> dict[str, str]:
    return {rel: sha(REPO / rel) for rel in paths}


def test_pins() -> None:
    for rel, digest in PINNED.items():
        if sha(REPO / rel) != digest:
            raise AssertionError(rel)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    selected = config["runner"]["path"].replace("\\", "/")
    if selected != "00.kernel/00.00.01.law/0302.run/02.run.003.py":
        raise AssertionError("runner selection is not the explicit 003 path")
    if sha(REPO / selected) != config["runner"]["sha256"]:
        raise AssertionError("configured runner hash does not match 003")
    SUITE.ok("pinned sources still match the manifest")


def test_real_context() -> None:
    before = snap(MUTABLE_GUARDS)
    where = run(["where", "--root", str(REPO)])
    validate = run(["validate", "--root", str(REPO)])
    state = ""
    for line in (REPO / "00.kernel/00.00.10.work/0401.goal/06.01.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("assignment_state: "):
            state = line.split(": ", 1)[1]
    if where.returncode != 0 or f"assignment_state: {state}" not in where.stdout:
        raise AssertionError(where.stdout + where.stderr)
    if "result: pass" in where.stdout or "result: pass" in validate.stdout:
        raise AssertionError("context command executed a candidate")
    if validate.returncode != 0 or "validate: pass" not in validate.stdout:
        raise AssertionError(validate.stdout + validate.stderr)
    if "runtime_band: 0300-0399" not in where.stdout:
        raise AssertionError("band was not reported")
    if snap(MUTABLE_GUARDS) != before:
        raise AssertionError("where or validate wrote a guarded file")
    SUITE.ok("real workspace where and validate")


def test_operation() -> None:
    scratch = REPO / "app" / "scratch" / "fixture"
    if scratch.exists():
        shutil.rmtree(scratch)
    digest = make_fixture(scratch)
    before = snap(MUTABLE_GUARDS)
    proc = run([
        "test-run", "--root", str(scratch),
        "--candidate", CANDIDATE, "--sha256", digest,
    ])
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    output = scratch / "output" / "inventory.json"
    got = json.loads(output.read_bytes().decode("utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    if got != expected:
        raise AssertionError(json.dumps(got, indent=2))
    if got["pages"][1]["missing_required_face"] != "01.md":
        raise AssertionError("missing face was not reported")
    if "do-not-read" in proc.stdout or "do-not-read" in output.read_text(encoding="utf-8"):
        raise AssertionError("the command read the foreign cwd")
    if f"payload_sha256: {digest}" not in proc.stdout:
        raise AssertionError("payload hash was not reported")
    if "result: pass" not in proc.stdout:
        raise AssertionError("result was not reported")
    if snap(MUTABLE_GUARDS) != before:
        raise AssertionError("fixture operation wrote a guarded file")
    relocated = Path(tempfile.mkdtemp(prefix="librarian-0504-reloc-"))
    try:
        copied = relocated / "fixture"
        shutil.copytree(scratch, copied)
        kept_inventory = (copied / "output" / "inventory.json").read_bytes()
        moved = json.loads((copied / "fixture.json").read_text(encoding="utf-8"))
        moved["output"] = "output/inventory-relocated.json"
        (copied / "fixture.json").write_bytes(lf(json.dumps(moved, indent=2) + "\n"))
        for name in ("02.run.002.py", "02.run.003.py", "02.run.009.py"):
            junk = copied / "00.kernel/00.00.01.law/0302.run" / name
            junk.parent.mkdir(parents=True, exist_ok=True)
            junk.write_bytes(b"not-the-runner\n")
        other = Path(tempfile.mkdtemp(prefix="librarian-0504-other-"))
        try:
            proc = run([
                "test-run", "--root", str(copied),
                "--container", str(copied),
                "--candidate", CANDIDATE, "--sha256", digest,
            ], cwd=other)
            if proc.returncode != 0:
                raise AssertionError(proc.stderr)
            if str(RUNNER.resolve()) not in proc.stdout:
                raise AssertionError("runner was not the law candidate")
            if "not-the-runner" in proc.stdout:
                raise AssertionError("relocated junk runner was selected")
            second = json.loads((copied / "output" / "inventory-relocated.json").read_bytes().decode("utf-8"))
            if second != expected:
                raise AssertionError("relocated inventory differed")
            if (copied / "output" / "inventory.json").read_bytes() != kept_inventory:
                raise AssertionError("the prior inventory was erased")
        finally:
            shutil.rmtree(other, ignore_errors=True)
    finally:
        shutil.rmtree(relocated, ignore_errors=True)
    SUITE.ok("fixture inventory from a foreign cwd and a relocated root")


def test_live_roots() -> None:
    before = snap(MUTABLE_GUARDS)
    digest = "a" * 64
    for name, root in (
        ("test-run on the real workspace", REPO),
        ("test-run on the real work book", REPO / "00.kernel/00.00.10.work"),
    ):
        proc = run([
            "test-run", "--root", str(root), "--candidate", CANDIDATE,
            "--sha256", digest, "--test",
        ])
        expect_stop(name, proc, "fixture root is the live workspace")
    proc = run(["run", "--root", str(REPO), "--test"])
    expect_stop("normal run", proc, "normal run is not activated")
    for label, path in (("002", RUNNER_002), ("003", RUNNER)):
        direct = subprocess.run(
            [PY, "-B", str(path), "run"],
            cwd=str(FOREIGN),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        SUITE.log.append(f"$ {PY} -B {path} run")
        SUITE.log.append(direct.stderr)
        if direct.returncode != 2 or "normal run is not activated" not in direct.stderr:
            raise AssertionError(direct.stderr)
        SUITE.refusal(f"direct runner {label} refuses")
    if snap(MUTABLE_GUARDS) != before:
        raise AssertionError("a refused command wrote a guarded file")
    if list((REPO / "00.kernel/00.00.01.law/0302.run").rglob("__pycache__")):
        raise AssertionError("bytecode was written in the law page")
    SUITE.ok("refused commands left the guarded files unchanged")


def test_authorization() -> None:
    root = REPO / "app" / "scratch" / "accepted"
    if root.exists():
        shutil.rmtree(root)
    digest = make_fixture(root, "accepted")
    proc = run([
        "test-run", "--root", str(root), "--candidate", CANDIDATE, "--sha256", digest,
    ])
    expect_stop("accepted assignment is not a fresh release", proc,
                "assignment is not a fresh execution release")
    if (root / "output" / "inventory.json").exists():
        raise AssertionError("refused test-run wrote an inventory")
    released = REPO / "app" / "scratch" / "released-validate"
    if released.exists():
        shutil.rmtree(released)
    plant(released, "accepted")
    plant_runner(released)
    (released / "00.kernel/00.00.01.law/0302.run/02.run.009.py").write_bytes(b"higher-version\n")
    proc = run(["where", "--root", str(released)])
    if proc.returncode != 0 or "02.run.003.py" not in proc.stdout:
        raise AssertionError(proc.stdout + proc.stderr)
    if "02.run.002.py" in proc.stdout or "02.run.009.py" in proc.stdout or "higher-version" in proc.stdout:
        raise AssertionError("a runner was selected by version instead of the configured path")
    SUITE.ok("accepted context can be inspected and does not select a higher version")
    proc = run([
        "test-run", "--root", str(root), "--candidate", CANDIDATE, "--sha256", digest, "--test",
    ])
    expect_stop("accepted fixture with --test is not a fresh release", proc,
                "assignment is not a fresh execution release")


def test_boundaries() -> None:
    base = REPO / "app" / "scratch" / "boundary"
    if base.exists():
        shutil.rmtree(base)

    missing_book = base / "missing-book"
    missing_book.mkdir(parents=True)
    (missing_book / "app").mkdir()
    (missing_book / "app/development-workspace.json").write_bytes(CONFIG.read_bytes())
    (missing_book / "00.kernel").mkdir()
    expect_stop(
        "missing work book",
        run(["validate", "--root", str(missing_book)]),
        "work book is missing",
    )

    missing_item = base / "missing-item"
    plant(missing_item, "released", current_work="00.kernel/00.00.10.work/0504.app-entry/missing.md")
    plant_runner(missing_item)
    expect_stop(
        "missing work item",
        run(["validate", "--root", str(missing_item)]),
        "work item is missing:",
    )

    space = base / "space"
    plant(space, "released", workflow_space="99")
    plant_runner(space)
    expect_stop(
        "undeclared workflow space",
        run(["validate", "--root", str(space)]),
        "workflow space is not the declared space",
    )

    mapping = base / "mapping"
    plant(mapping, "released", book="00.00.01.law")
    plant_runner(mapping)
    expect_stop(
        "wrong job book",
        run(["validate", "--root", str(mapping)]),
        "record book is not the configured work book",
    )

    same = base / "same-book"
    text = CONFIG.read_text(encoding="utf-8").replace(
        '"runtime_book": "00.00.01.law"', '"runtime_book": "00.00.10.work"'
    )
    (same / "app").mkdir(parents=True)
    (same / "app/development-workspace.json").write_bytes(lf(text))
    expect_stop(
        "job book mapped onto the runtime book",
        run(["validate", "--root", str(same)]),
        "job book and runtime book must differ",
    )

    ambiguous = base / "ambiguous"
    plant(ambiguous, "running")
    plant_runner(ambiguous)
    (ambiguous / "00.kernel/00.00.01.law/0399.run").mkdir()
    expect_stop(
        "ambiguous compute title",
        run(["validate", "--root", str(ambiguous)]),
        "more than one compute page for run",
    )

    escaped = base / "escape"
    plant(escaped, "released", current_work="../00.00.01.law/0302.run/02.run.002.py")
    plant_runner(escaped)
    expect_stop(
        "path escape",
        run(["validate", "--root", str(escaped)]),
        "path escapes the root",
    )

    digest = sha(PAYLOAD)
    outside = base / "outside-payload"
    make_fixture(outside)
    shutil.copy2(PAYLOAD, outside / "00.kernel/00.00.20.sample/0101.present/02.inventory.py")
    expect_stop(
        "payload outside its compute page",
        run([
            "test-run", "--root", str(outside),
            "--candidate", "00.kernel/00.00.20.sample/0101.present/02.inventory.py",
            "--sha256", digest,
        ]),
        "payload is outside its compute page",
    )

    wrong_hash = base / "wrong-hash"
    make_fixture(wrong_hash)
    expect_stop(
        "wrong payload hash",
        run([
            "test-run", "--root", str(wrong_hash),
            "--candidate", CANDIDATE, "--sha256", "b" * 64,
        ]),
        "payload hash does not match the fixture",
    )

    tampered = base / "tampered-payload"
    make_fixture(tampered)
    target = tampered / CANDIDATE
    target.write_bytes(target.read_bytes() + b"# changed\n")
    fixture = json.loads((tampered / "fixture.json").read_text(encoding="utf-8"))
    fixture["payload_sha256"] = "c" * 64
    (tampered / "fixture.json").write_bytes(lf(json.dumps(fixture, indent=2) + "\n"))
    expect_stop(
        "payload bytes do not match the declared hash",
        run([
            "test-run", "--root", str(tampered),
            "--candidate", CANDIDATE, "--sha256", "c" * 64,
        ]),
        "payload hash does not match",
    )

    climb = base / "climb"
    make_fixture(climb)
    page = climb / "00.kernel/00.00.01.law/0310.inventory"
    shutil.move(str(page), str(climb / "00.kernel/00.00.01.law/0410.inventory"))
    expect_stop(
        "compute page outside the band is not climbed to",
        run([
            "test-run", "--root", str(climb),
            "--candidate", "00.kernel/00.00.01.law/0410.inventory/02.inventory.py",
            "--sha256", digest,
        ]),
        "no compute page for inventory",
    )

    duplicate = base / "duplicate-title"
    make_fixture(duplicate)
    extra = duplicate / "00.kernel/00.00.01.law/0391.inventory"
    shutil.copytree(duplicate / "00.kernel/00.00.01.law/0310.inventory", extra)
    expect_stop(
        "two compute pages for one keyword",
        run([
            "test-run", "--root", str(duplicate),
            "--candidate", CANDIDATE, "--sha256", digest,
        ]),
        "more than one compute page for inventory",
    )
    if (duplicate / "output" / "inventory.json").exists():
        raise AssertionError("ambiguous lookup wrote an inventory")


def test_reparse() -> None:
    outside = Path(tempfile.mkdtemp(prefix="librarian-0504-out-"))
    root = REPO / "app" / "scratch" / "reparse"
    link = root / "00.kernel/00.00.10.work/0401.goal/out"
    try:
        (outside / "note.md").write_bytes(b"outside\n")
        if root.exists():
            shutil.rmtree(root)
        plant(root, "released")
        plant_runner(root)
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if proc.returncode != 0 or not link.exists():
            SUITE.skip("reparse junction", (proc.stderr or proc.stdout or "mklink failed").strip())
            return
        rel = "00.kernel/00.00.10.work/0401.goal/out/note.md"
        (root / RECORD).write_bytes(record_text("released", current_work=rel, pack=WORK_ITEM))
        expect_stop(
            "reparse escape",
            run(["validate", "--root", str(root)]),
            "path escapes the root",
        )
    finally:
        if link.exists():
            os.rmdir(link)
        shutil.rmtree(outside, ignore_errors=True)


def test_config_and_record() -> None:
    base = REPO / "app" / "scratch" / "config"
    if base.exists():
        shutil.rmtree(base)
    empty = base / "empty"
    empty.mkdir(parents=True)
    expect_stop("missing config", run(["validate", "--root", str(empty)]), "missing config")

    bad = base / "bad-json"
    (bad / "app").mkdir(parents=True)
    (bad / "app/development-workspace.json").write_bytes(b"{")
    expect_stop("malformed config", run(["validate", "--root", str(bad)]), "config is not json")

    dup = base / "dup"
    (dup / "app").mkdir(parents=True)
    (dup / "app/development-workspace.json").write_bytes(
        b'{ "schema": "librarian-development-workspace", "schema": "other" }\n'
    )
    expect_stop("duplicate config key", run(["validate", "--root", str(dup)]), "repeats a key")

    typed = base / "type"
    text = CONFIG.read_text(encoding="utf-8").replace('"version": 1', '"version": "1"', 1)
    (typed / "app").mkdir(parents=True)
    (typed / "app/development-workspace.json").write_bytes(lf(text))
    expect_stop("config version type", run(["validate", "--root", str(typed)]), "wrong type: version")

    unknown = base / "unknown"
    text = CONFIG.read_text(encoding="utf-8").replace(
        '"runtime_space": "0"', '"runtime_space": "0", "extra": true'
    )
    (unknown / "app").mkdir(parents=True)
    (unknown / "app/development-workspace.json").write_bytes(lf(text))
    expect_stop("unknown config key", run(["validate", "--root", str(unknown)]), "unknown key")

    widened = base / "widened"
    widened_config = json.loads(CONFIG.read_text(encoding="utf-8"))
    widened_config["fixture_containers"] = list(widened_config["fixture_containers"]) + ["app"]
    (widened / "app").mkdir(parents=True)
    (widened / "app/development-workspace.json").write_bytes(
        lf(json.dumps(widened_config, indent=2) + "\n")
    )
    expect_stop(
        "config cannot widen fixture containers",
        run(["validate", "--root", str(widened)]),
        "fixture containers are not the designated pair",
    )

    record = base / "record"
    plant(record, "released")
    plant_runner(record)
    (record / RECORD).write_bytes(b"this is not a record\n")
    expect_stop(
        "malformed record",
        run(["validate", "--root", str(record)]),
        "record line 1 is not 'key: value'",
    )

    repeated = base / "repeated"
    plant(repeated, "released")
    plant_runner(repeated)
    (repeated / RECORD).write_bytes(record_text("released") + b"desk: 00.kernel\n")
    expect_stop("duplicate record key", run(["validate", "--root", str(repeated)]), "repeats a key")

    completed = base / "completed"
    plant(completed, "completed")
    plant_runner(completed)
    expect_stop(
        "invalid assignment state",
        run(["validate", "--root", str(completed)]),
        "assignment_state is not a known state",
    )

    cr = base / "cr"
    plant(cr, "released")
    plant_runner(cr)
    (cr / RECORD).write_bytes(record_text("released").replace(b"\n", b"\r\n"))
    expect_stop("record carriage return", run(["validate", "--root", str(cr)]), "record has CR")

    view = base / "view"
    plant(view, "waiting")
    plant_runner(view)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["assignment_record"] = "00.kernel/00.live.md"
    (view / "app/development-workspace.json").write_bytes(lf(json.dumps(config, indent=2) + "\n"))
    (view / "00.kernel/00.live.md").write_bytes(
        record_text("released", current_work=WORK_ITEM).replace(
            b"fixture work item\n", b""
        ) + b"\nTAMPER-OPERATION-NOT-THIS\n"
    )
    proc = run(["where", "--root", str(view)])
    expect_stop("assignment path is the derived view", proc, "assignment record is the derived view")
    if "TAMPER-OPERATION-NOT-THIS" in proc.stdout or "TAMPER-OPERATION-NOT-THIS" in proc.stderr:
        raise AssertionError("the derived view was used")

    tamper = base / "tampered-view"
    plant(tamper, "waiting")
    plant_runner(tamper)
    (tamper / "00.kernel/00.live.md").write_bytes(
        b"TAMPER-OPERATION-NOT-THIS\nstate: released\n"
    )
    proc = run(["where", "--root", str(tamper)])
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    if "TAMPER-OPERATION-NOT-THIS" in proc.stdout or "assignment_state: released" in proc.stdout:
        raise AssertionError("tampered 00.live changed the context")
    if "assignment_state: waiting" not in proc.stdout:
        raise AssertionError(proc.stdout)
    SUITE.ok("tampered 00.live does not change context")

    wrong_runner = base / "wrong-runner"
    plant(wrong_runner, "running")
    plant_runner(wrong_runner)
    config = json.loads((wrong_runner / "app/development-workspace.json").read_text(encoding="utf-8"))
    config["runner"]["sha256"] = "d" * 64
    (wrong_runner / "app/development-workspace.json").write_bytes(lf(json.dumps(config, indent=2) + "\n"))
    expect_stop(
        "wrong runner hash",
        run(["validate", "--root", str(wrong_runner)]),
        "runner hash does not match",
    )


def test_app01() -> None:
    readme = REPO / "app/README.md"
    before = readme.read_bytes()
    digest = sha(PAYLOAD)
    planted = REPO / "app/fixture.json"
    try:
        planted.write_bytes(lf(json.dumps({
            "schema": "librarian-fixture",
            "version": 1,
            "identity": "0504-inventory-pass01",
            "allowed_root": ".",
            "compute_page": "0310.inventory",
            "inventory_book": "00.00.20.sample",
            "output": "README.md",
            "required_face": "01.md",
            "payload_sha256": digest,
        }) + "\n"))
        proc = run([
            "test-run", "--root", str(REPO / "app"),
            "--candidate", CANDIDATE, "--sha256", digest,
        ])
        expect_stop(
            "source folder app is not a fixture container",
            proc,
            "fixture root is not a designated container",
        )
    finally:
        if planted.exists():
            planted.unlink()
    if readme.read_bytes() != before:
        readme.write_bytes(before)
        raise AssertionError("app/README.md changed")

    proc = run([
        "test-run", "--root", str(REPO / "00.kernel/00.00.10.work/0504.app-entry"),
        "--candidate", CANDIDATE, "--sha256", digest,
    ])
    expect_stop(
        "source page is not a fixture container",
        proc,
        "fixture root is the live workspace",
    )

    named = REPO / "app/scratch/app01-allowed"
    if named.exists():
        shutil.rmtree(named)
    make_fixture(named)
    raw = json.loads((named / "fixture.json").read_text(encoding="utf-8"))
    raw["allowed_root"] = "."
    raw["output"] = "README.md"
    (named / "fixture.json").write_bytes(lf(json.dumps(raw, indent=2) + "\n"))
    proc = run([
        "test-run", "--root", str(named),
        "--candidate", CANDIDATE, "--sha256", digest,
    ])
    expect_stop("fixture allowed_root is not authority", proc, "unknown key: allowed_root")
    if (named / "README.md").exists() or (named / "output/inventory.json").exists():
        raise AssertionError("rejected fixture metadata wrote an output")

    external = Path(tempfile.mkdtemp(prefix="librarian-0502-ext-"))
    try:
        proc = run([
            "test-run", "--root", str(external),
            "--candidate", CANDIDATE, "--sha256", digest,
        ])
        expect_stop(
            "external container was not named",
            proc,
            "external fixture container was not named",
        )
        proc = run([
            "test-run", "--root", str(external),
            "--container", str(REPO),
            "--candidate", CANDIDATE, "--sha256", digest,
        ])
        expect_stop(
            "external container overlaps the workspace",
            proc,
            "external container overlaps the workspace",
        )
        proc = run([
            "test-run", "--root", str(external),
            "--container", str(Path(REPO.anchor)),
            "--candidate", CANDIDATE, "--sha256", digest,
        ])
        expect_stop(
            "filesystem root is not a container",
            proc,
            "fixture container is a filesystem root",
        )
    finally:
        shutil.rmtree(external, ignore_errors=True)
    proc = run([
        "test-run", "--root", str(Path(REPO.anchor)),
        "--candidate", CANDIDATE, "--sha256", digest,
    ])
    expect_stop(
        "fixture root is a filesystem root",
        proc,
        "fixture container is a filesystem root",
    )

    link_parent = Path(tempfile.mkdtemp(prefix="librarian-0502-link-"))
    link = link_parent / "alias"
    try:
        made = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(REPO / "app")],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if made.returncode != 0 or not link.exists():
            SUITE.skip("container alias", (made.stderr or made.stdout or "mklink failed").strip())
        else:
            proc = run([
                "test-run", "--root", str(link),
                "--candidate", CANDIDATE, "--sha256", digest,
            ])
            expect_stop(
                "junction to app is not a container",
                proc,
                "fixture root is not a designated container",
            )
    finally:
        if link.exists():
            os.rmdir(link)
        shutil.rmtree(link_parent, ignore_errors=True)

    box = Path(tempfile.mkdtemp(prefix="librarian-0502-box-"))
    alias = box / "alias"
    try:
        make_fixture(box)
        data = json.loads((box / "fixture.json").read_text(encoding="utf-8"))
        data["output"] = "alias/README.md"
        (box / "fixture.json").write_bytes(lf(json.dumps(data, indent=2) + "\n"))
        made = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(alias), str(REPO / "app")],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if made.returncode != 0 or not alias.exists():
            SUITE.skip("output alias", (made.stderr or made.stdout or "mklink failed").strip())
        else:
            proc = run([
                "test-run", "--root", str(box),
                "--container", str(box),
                "--candidate", CANDIDATE, "--sha256", digest,
            ])
            expect_stop("junction output leaves the container", proc, "path escapes the root")
    finally:
        if alias.exists():
            os.rmdir(alias)
        shutil.rmtree(box, ignore_errors=True)

    probe = REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/probe-0502"
    originals = [
        REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/02.inventory.py",
        REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/02.md",
        REPO / "00.kernel/00.00.10.work/0504.app-entry/fixtures/expected-inventory.json",
    ]
    pinned = {path: path.read_bytes() for path in originals}
    try:
        if probe.exists():
            shutil.rmtree(probe)
        probe_digest = make_fixture(probe)
        proc = run([
            "test-run", "--root", str(probe),
            "--candidate", CANDIDATE, "--sha256", probe_digest,
        ])
        if proc.returncode != 0:
            raise AssertionError(proc.stderr)
        got = json.loads((probe / "output/inventory.json").read_text(encoding="utf-8"))
        expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
        if got != expected:
            raise AssertionError("page-fixtures inventory differed")
        SUITE.ok("designated page fixtures container")
    finally:
        if probe.exists():
            shutil.rmtree(probe)
    for path, data in pinned.items():
        if path.read_bytes() != data:
            path.write_bytes(data)
            raise AssertionError(f"{path.name} changed")
    if readme.read_bytes() != before:
        readme.write_bytes(before)
        raise AssertionError("app/README.md changed during APP-01 checks")
    SUITE.ok("protected source bytes stayed unchanged")


def _reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    attributes = getattr(info, "st_file_attributes", 0)
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def test_ar01() -> None:
    """Refuse an output name, or its temporary name, that is already present."""
    base = REPO / "app" / "scratch" / "ar01"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    digest = sha(PAYLOAD)
    readme = REPO / "app/README.md"
    readme_before = readme.read_bytes()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    def invoke(root: Path) -> subprocess.CompletedProcess[str]:
        return run([
            "test-run", "--root", str(root),
            "--candidate", CANDIDATE, "--sha256", digest,
        ])

    def fresh_root(name: str) -> Path:
        root = base / name
        if root.exists():
            shutil.rmtree(root)
        make_fixture(root)
        return root

    junction = base / "dangling-junction" / "output" / "inventory.json.tmp"
    symlink = base / "file-symlink" / "output" / "inventory.json"
    try:
        fresh = fresh_root("fresh")
        proc = invoke(fresh)
        if proc.returncode != 0:
            raise AssertionError(proc.stderr)
        got = json.loads((fresh / "output" / "inventory.json").read_bytes().decode("utf-8"))
        if got != expected:
            raise AssertionError("fresh inventory differed")
        if (fresh / "output" / "inventory.json.tmp").exists():
            raise AssertionError("fresh run left the temporary name")
        SUITE.ok("fresh inventory when the output names are absent")

        ordinary = fresh_root("ordinary-output")
        marker = b"ordinary-output-marker\n"
        target = ordinary / "output" / "inventory.json"
        target.parent.mkdir(parents=True)
        target.write_bytes(marker)
        proc = invoke(ordinary)
        expect_stop("existing ordinary output", proc, "output name is already present")
        if target.read_bytes() != marker:
            raise AssertionError("ordinary output bytes changed")
        if (ordinary / "output" / "inventory.json.tmp").exists():
            raise AssertionError("ordinary output refusal wrote a temporary")

        temporary = fresh_root("ordinary-tmp")
        marker_tmp = b"ordinary-tmp-marker\n"
        tmp = temporary / "output" / "inventory.json.tmp"
        tmp.parent.mkdir(parents=True)
        tmp.write_bytes(marker_tmp)
        proc = invoke(temporary)
        expect_stop("existing ordinary temporary", proc, "output temporary name is already present")
        if tmp.read_bytes() != marker_tmp:
            raise AssertionError("ordinary temporary bytes changed")
        if (temporary / "output" / "inventory.json").exists():
            raise AssertionError("ordinary temporary refusal wrote the output")

        linked_out = fresh_root("hardlink-output")
        victim_out = linked_out / "victim-output.txt"
        victim_out_bytes = b"hardlink-output-victim\n"
        victim_out.write_bytes(victim_out_bytes)
        link_out = linked_out / "output" / "inventory.json"
        link_out.parent.mkdir(parents=True)
        os.link(victim_out, link_out)
        if victim_out.stat().st_nlink != 2:
            raise AssertionError("output hard link was not created")
        proc = invoke(linked_out)
        expect_stop("direct output hard link", proc, "output name is already present")
        if victim_out.read_bytes() != victim_out_bytes or link_out.read_bytes() != victim_out_bytes:
            raise AssertionError("output hard link changed the victim")
        if victim_out.stat().st_nlink != 2 or not link_out.exists():
            raise AssertionError("output hard link was removed")

        linked_tmp = fresh_root("hardlink-tmp")
        victim_tmp = linked_tmp / "victim-tmp.txt"
        victim_tmp_bytes = b"hardlink-tmp-victim\n"
        victim_tmp.write_bytes(victim_tmp_bytes)
        link_tmp = linked_tmp / "output" / "inventory.json.tmp"
        link_tmp.parent.mkdir(parents=True)
        os.link(victim_tmp, link_tmp)
        if victim_tmp.stat().st_nlink != 2:
            raise AssertionError("temporary hard link was not created")
        proc = invoke(linked_tmp)
        expect_stop("temporary hard link", proc, "output temporary name is already present")
        if victim_tmp.read_bytes() != victim_tmp_bytes or link_tmp.read_bytes() != victim_tmp_bytes:
            raise AssertionError("temporary hard link changed the victim")
        if victim_tmp.stat().st_nlink != 2 or not link_tmp.exists():
            raise AssertionError("temporary hard link was removed")
        if (linked_tmp / "output" / "inventory.json").exists():
            raise AssertionError("temporary hard link refusal wrote the output")

        junction_root = fresh_root("dangling-junction")
        missing = junction_root / "absent-dir"
        junction.parent.mkdir(parents=True, exist_ok=True)
        made = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(junction), str(missing)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if made.returncode != 0 or not _reparse(junction):
            SUITE.skip(
                "dangling temporary junction",
                (made.stderr or made.stdout or "mklink failed").strip(),
            )
        else:
            if junction.exists():
                raise AssertionError("dangling junction exists() was true")
            proc = invoke(junction_root)
            expect_stop(
                "dangling temporary junction",
                proc,
                "output temporary name is already present",
            )
            if missing.exists():
                raise AssertionError("dangling junction target was created")
            if not _reparse(junction):
                raise AssertionError("dangling junction was removed")
            if junction.exists():
                raise AssertionError("dangling junction became an existing path")
            if (junction_root / "output" / "inventory.json").exists():
                raise AssertionError("dangling junction refusal wrote the output")

        symlink_root = fresh_root("file-symlink")
        symlink_missing = symlink_root / "absent-file"
        symlink.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(str(symlink_missing), symlink)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                SUITE.skip(
                    "dangling file symlink",
                    "WinError 1314: a required privilege is not held by the client",
                )
            else:
                raise
        else:
            if symlink.exists():
                raise AssertionError("dangling file symlink exists() was true")
            proc = invoke(symlink_root)
            expect_stop("dangling file symlink", proc, "output name is already present")
            if symlink_missing.exists():
                raise AssertionError("dangling file symlink target was created")
            if not symlink.is_symlink():
                raise AssertionError("dangling file symlink was removed")

        if readme.read_bytes() != readme_before:
            readme.write_bytes(readme_before)
            raise AssertionError("app/README.md changed during AR-01 checks")
        SUITE.ok("occupied output names stayed unchanged")
    finally:
        if _reparse(junction):
            os.rmdir(junction)
        if symlink.is_symlink():
            symlink.unlink()
        shutil.rmtree(base, ignore_errors=True)


def main() -> None:
    scratch = REPO / "app" / "scratch"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    before = snap(tuple(PINNED) + MUTABLE_GUARDS)
    for name, fn in (
        ("pins", test_pins),
        ("real context", test_real_context),
        ("operation", test_operation),
        ("live roots", test_live_roots),
        ("authorization", test_authorization),
        ("boundaries", test_boundaries),
        ("app-01", test_app01),
        ("ar-01", test_ar01),
        ("reparse", test_reparse),
        ("config and record", test_config_and_record),
    ):
        check(name, fn)
    after = snap(tuple(PINNED) + MUTABLE_GUARDS)
    if before != after:
        changed = [key for key in before if before[key] != after[key]]
        SUITE.fail("guarded bytes changed during the suite", ", ".join(changed))
    else:
        SUITE.ok("guarded bytes were unchanged by the suite")
    pyc = list((REPO / "00.kernel").rglob("__pycache__"))
    pyc += [p for p in (REPO / "app").rglob("__pycache__") if "scratch" not in p.parts]
    if pyc:
        SUITE.fail("bytecode in a book or app", "\n".join(str(p) for p in pyc))
    else:
        SUITE.ok("no bytecode was written into the books or app")
    print(
        f"summary pass {len(SUITE.passed)} "
        f"expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} "
        f"fail {len(SUITE.failed)}"
    )
    log = scratch / "test-log.txt"
    log.write_text("\n".join(SUITE.log) + "\n", encoding="utf-8", newline="\n")
    shutil.rmtree(FOREIGN, ignore_errors=True)
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
