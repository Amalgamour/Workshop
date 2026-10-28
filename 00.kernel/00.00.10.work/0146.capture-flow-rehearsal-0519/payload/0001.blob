"""Disposable end-to-end rehearsal of the accepted Clerk seam and handoff.

This module is not an app command and not a new lifecycle. It materializes
a hash-checked source-view from the 05.19 pack, runs the allowlisted protocol
test worker on disposable fixtures, and treats result.json as a synthetic
report. A verified receipt is custody, not acceptance.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(__file__).resolve().parents[2]
PACK = REPO / "00.kernel/00.00.10.work/0504.app-entry/evidence/pack05.19"
MANIFEST_SHA = "5c492c54e15a47a5bdf6f9231d619de428335ba470899e09e1b077d098613ef0"
MANIFEST_BYTES = 7167
PROVENANCE_SHA = "b6b255dcafd42696525dd2600b2049c1fbfea6eb943fcdd27389bfc07d1c7909"
PROVENANCE_BYTES = 5499
RUNNER_REL = "00.kernel/00.00.01.law/0302.run/02.run.003.py"
RUNNER_SHA = "bbca135691ba4e873e27b9322b1ad6d79deeb59107eb7d377f7d20014067d50c"
RUNNER_BYTES = 10143
LIBRARIAN_REL = "app/librarian.py"
LIBRARIAN_SNAPSHOT = "a320f270dd87508d4fa9d3d5e78904108605fa308abb3ebd86513ae9c3c01fab"
TASK_REL = "00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/router/instructions/task.md"
JOB_REL = "00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/fixture/bridge/job.json"
CLERK_JOB_REL = "00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples/router/clerk-job.json"
TASK_SHA = "6c913091d80948e3be49fa384b023ee3c43762599f3f61b47db885b4f846fe66"
JOB_SHA = "4d57cdb9ea210bfaedf4bdf6974c723735abcf431cb16b3ec946222fab05e1cf"
CLERK_JOB_SHA = "c4c9ddd38d3da0f72570404be23eb4c267d78653ff0ac23f0741ad8433bb1f5f"
RESULT_SHA = "0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6"
WORK_REF = "00.kernel/00.00.10.work/0504.app-entry/05.01.md"
RECORD_REL = "00.kernel/00.00.10.work/0401.goal/06.01.md"
RECORD_SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
CLOSURE = (
    "app/context.py",
    "app/clerk_seam.py",
    "app/clerk-seam.json",
    "app/worker_bridge.py",
    "app/worker-bridge.json",
    "app/development-workspace.json",
    "labs/clerk-handoff-pass02/clerk.py",
    "labs/return-capture-pass01/return_capture.py",
    "labs/return-capture-pass01/return_inspect.py",
    "labs/capture-handoff-pass01/handoff.py",
    "labs/worker-bridge-pass01/bridge/__init__.py",
    "labs/worker-bridge-pass01/bridge/adapter.py",
    "labs/worker-bridge-pass01/bridge/canon.py",
    "labs/worker-bridge-pass01/bridge/envelope.py",
    "labs/worker-bridge-pass01/bridge/ids.py",
    "labs/worker-bridge-pass01/bridge/verify.py",
    "labs/worker-bridge-pass01/fixtures/worker_fixture.py",
    "labs/worker-bridge-pass01/profiles.json",
)
LIVE_GUARDS = CLOSURE + (
    LIBRARIAN_REL,
    RUNNER_REL,
    "00.kernel/00.00.10.work/0504.app-entry/05.19.md",
    "00.kernel/00.00.10.work/0504.app-entry/05.18.md",
    "00.kernel/00.00.10.work/0146.capture-flow-rehearsal-0519/reservation.json",
    "00.kernel/00.00.10.work/0146.capture-flow-rehearsal-0519/01.md",
    "labs/capture-handoff-pass01/README.md",
    "labs/capture-handoff-pass01/tests/test_handoff.py",
    "labs/capture-handoff-pass01/demo.py",
    "labs/worker-bridge-pass01/bridge/cli.py",
    "00.kernel/00.00.10.work/0504.app-entry/06.19.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/flow05.19/CONTRACT.md",
    "labs/capture-flow-rehearsal-pass01/rehearse.py",
    "labs/capture-flow-rehearsal-pass01/README.md",
    "labs/capture-flow-rehearsal-pass01/demo.py",
    "labs/capture-flow-rehearsal-pass01/tests/test_rehearse.py",
)
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
PY = sys.executable


class PinError(Exception):
    pass


class ProofError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return digest(path.read_bytes())


def canonical(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def outside_git(path: Path) -> None:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            raise ProofError(f"path is inside a Git working tree: {path}")
        if current.parent == current:
            return
        current = current.parent


def _inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(str(child))
    parent_s = os.path.normcase(str(parent))
    if child_s == parent_s:
        return False
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def assert_owned(root: Path) -> Path:
    """Refuse every cleanup target that is not this process's own temp root."""
    if not root.is_absolute():
        raise ProofError("temporary root is not absolute")
    resolved = root.resolve()
    temp = Path(tempfile.gettempdir()).resolve()
    repo = REPO.resolve()
    if resolved == temp or resolved == repo or _inside(resolved, repo) or not _inside(resolved, temp):
        raise ProofError(f"refuse to remove {resolved}")
    outside_git(resolved)
    return resolved


def owned_temp(prefix: str) -> Path:
    parent = Path(tempfile.gettempdir()).resolve()
    outside_git(parent)
    made = Path(tempfile.mkdtemp(prefix=prefix, dir=str(parent)))
    return assert_owned(made)


def remove_owned(root: Path) -> None:
    resolved = assert_owned(root)
    if not resolved.exists():
        return
    for dirpath, dirnames, filenames in os.walk(resolved, topdown=True):
        kept = []
        for name in dirnames:
            path = Path(dirpath) / name
            if is_reparse(path):
                os.rmdir(path)
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            path = Path(dirpath) / name
            if is_reparse(path):
                os.remove(path)

    def _onerror(func, path, _exc):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(resolved, onerror=_onerror)


def live_hashes() -> dict[str, str]:
    return {rel: file_digest(REPO / rel) for rel in LIVE_GUARDS}


def _load_json_bytes(data: bytes, label: str) -> dict:
    if data.startswith(b"\xef\xbb\xbf"):
        raise PinError(f"{label} has a BOM")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PinError(f"{label} is not utf-8 json") from exc
    if not isinstance(value, dict):
        raise PinError(f"{label} is not an object")
    return value


def check_pack() -> dict[str, dict]:
    """Hash the pack documents and every snapshot. Stop before a source-view exists."""
    manifest_path = PACK / "source-manifest.json"
    provenance_path = PACK / "source-provenance.json"
    manifest_raw = manifest_path.read_bytes()
    provenance_raw = provenance_path.read_bytes()
    if digest(manifest_raw) != MANIFEST_SHA or len(manifest_raw) != MANIFEST_BYTES:
        raise PinError("source-manifest pin does not match")
    if digest(provenance_raw) != PROVENANCE_SHA or len(provenance_raw) != PROVENANCE_BYTES:
        raise PinError("source-provenance pin does not match")
    manifest = _load_json_bytes(manifest_raw, "source-manifest")
    provenance = _load_json_bytes(provenance_raw, "source-provenance")
    if manifest.get("schema") != "prime-pack-sources/1":
        raise PinError("source-manifest schema is not prime-pack-sources/1")
    sources = manifest.get("sources")
    rows = provenance.get("sources")
    if not isinstance(sources, list) or not isinstance(rows, list):
        raise PinError("pack sources are not lists")
    found = {}
    for item in sources:
        path = item.get("path")
        snapshot = item.get("snapshot")
        sha = item.get("sha256")
        size = item.get("bytes")
        if not isinstance(path, str) or path in found:
            raise PinError("pack source path is not usable")
        blob = PACK / snapshot
        data = blob.read_bytes()
        if digest(data) != sha or len(data) != size:
            raise PinError(f"snapshot does not match: {path}")
        found[path] = {"sha256": sha, "bytes": size, "snapshot": snapshot, "data": data}
    baseline = "d017f9f7e8271db6de3b72d31a82077c5ef588c4"
    prov_paths = []
    for item in rows:
        path = item.get("path")
        source = item.get("source")
        commit = item.get("source_commit")
        if not isinstance(path, str) or path not in found:
            raise PinError(f"provenance does not match the manifest: {path}")
        if source == "git-blob":
            if commit != baseline:
                raise PinError(f"provenance commit is not the baseline: {path}")
        elif source == "reviewed-working-bytes":
            if commit is not None:
                raise PinError(f"reviewed working bytes name a commit: {path}")
        else:
            raise PinError(f"provenance source is not usable: {path}")
        prov_paths.append(path)
    if prov_paths != list(found):
        raise PinError("provenance paths do not match the manifest")
    if found[LIBRARIAN_REL]["sha256"] != LIBRARIAN_SNAPSHOT:
        raise PinError("librarian snapshot pin moved")
    for rel in CLOSURE + (TASK_REL, JOB_REL, CLERK_JOB_REL):
        if rel not in found:
            raise PinError(f"required snapshot is missing: {rel}")
    runner = REPO / RUNNER_REL
    runner_data = runner.read_bytes()
    if digest(runner_data) != RUNNER_SHA or len(runner_data) != RUNNER_BYTES:
        raise PinError(
            "runner pin does not match "
            f"{RUNNER_REL}; expected {RUNNER_SHA} ({RUNNER_BYTES} bytes)"
        )
    found[RUNNER_REL] = {
        "sha256": RUNNER_SHA,
        "bytes": RUNNER_BYTES,
        "snapshot": None,
        "data": runner_data,
        "role": "declared-config-pin",
    }
    return found


def materialize(dest: Path, packed: dict[str, dict]) -> list[dict]:
    if dest.exists():
        raise ProofError("source-view already exists")
    dest.mkdir(parents=True)
    written = []
    for rel in CLOSURE:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = packed[rel]["data"]
        target.write_bytes(data)
        written.append({
            "path": rel,
            "sha256": packed[rel]["sha256"],
            "bytes": packed[rel]["bytes"],
            "role": "pack-snapshot",
        })
    runner = dest / RUNNER_REL
    runner.parent.mkdir(parents=True, exist_ok=True)
    runner.write_bytes(packed[RUNNER_REL]["data"])
    written.append({
        "path": RUNNER_REL,
        "sha256": RUNNER_SHA,
        "bytes": RUNNER_BYTES,
        "role": "declared-config-pin",
        "pack_snapshot": False,
    })
    return written


def require_closure(dest: Path, packed: dict[str, dict]) -> None:
    """Re-hash the source-view. A mismatch returns before import and before launch."""
    if not dest.is_dir():
        raise PinError("source-view is missing")
    for rel in CLOSURE:
        path = dest / rel
        if not path.is_file() or is_reparse(path):
            raise PinError(f"closure file is missing: {rel}")
        data = path.read_bytes()
        if digest(data) != packed[rel]["sha256"] or len(data) != packed[rel]["bytes"]:
            raise PinError(f"closure hash does not match: {rel}")
    runner = dest / RUNNER_REL
    if not runner.is_file() or is_reparse(runner):
        raise PinError("runner pin is missing from the source-view")
    data = runner.read_bytes()
    if digest(data) != RUNNER_SHA or len(data) != RUNNER_BYTES:
        raise PinError("runner pin does not match")
    if (dest / LIBRARIAN_REL).exists():
        raise PinError("live librarian was copied into the source-view")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PinError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class View:
    def __init__(self, home: Path, root: Path, packed: dict, files: list[dict], context, seam, handoff) -> None:
        self.home = home
        self.root = root
        self.packed = packed
        self.files = files
        self.context = context
        self.seam = seam
        self.handoff = handoff


def open_view() -> View:
    packed = check_pack()
    home = owned_temp("flow0519-view-")
    root = home / "source-view"
    try:
        files = materialize(root, packed)
        require_closure(root, packed)
        context = _load_module(root / "app/context.py", "flow0519_context")
        seam = _load_module(root / "app/clerk_seam.py", "flow0519_seam")
        handoff = _load_module(root / "labs/capture-handoff-pass01/handoff.py", "flow0519_handoff")
        handoff_root = Path(handoff.__file__).resolve().parents[2]
        if os.path.normcase(str(handoff_root)) != os.path.normcase(str(root.resolve())):
            raise PinError("handoff ROOT is not the source-view")
    except Exception:
        remove_owned(home)
        raise
    return View(home, root, packed, files, context, seam, handoff)


def exclusion_record() -> dict:
    live = (REPO / LIBRARIAN_REL).read_bytes()
    return {
        "path": LIBRARIAN_REL,
        "role": "excluded",
        "reason": "not part of the tool closure; live bytes are not the accepted snapshot and are not copied",
        "snapshot_sha256": LIBRARIAN_SNAPSHOT,
        "live_sha256": digest(live),
        "live_bytes": len(live),
        "copied": False,
    }


def run_cli(script: Path, args: list[str]) -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(
        [PY, "-B", str(script), *args],
        cwd=str(script.parent),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        timeout=60,
        check=False,
    )
    return {
        "code": proc.returncode,
        "stdout": proc.stdout.replace(b"\r\n", b"\n").decode("utf-8", "replace"),
        "stderr": proc.stderr.replace(b"\r\n", b"\n").decode("utf-8", "replace"),
    }


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise ProofError(f"missing {prefix!r}\n{text}")


def _record_text() -> bytes:
    values = {
        "record": "current-assignment",
        "schema": RECORD_SCHEMA,
        "desk": "00.kernel",
        "book": "00.00.10.work",
        "workflow_space": "0",
        "current_work": WORK_REF,
        "pack": WORK_REF,
        "assignment_state": "released",
        "waits_on": "review",
        "next": "next step",
        "updated": "2026-10-26",
    }
    order = (
        "record", "schema", "desk", "book", "workflow_space", "current_work",
        "pack", "assignment_state", "waits_on", "next", "updated",
    )
    return "".join(f"{key}: {values[key]}\n" for key in order).encode("utf-8")


def _index(root: Path) -> dict[str, str]:
    found = {}
    if not root.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(root):
        kept = []
        for name in dirnames:
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix()
            if is_reparse(path):
                found[rel + "/"] = "reparse"
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix()
            found[rel] = "reparse" if is_reparse(path) else file_digest(path)
    return found


def _file_sha(path: Path) -> str | None:
    if path.is_file() and not is_reparse(path):
        return file_digest(path)
    return None


class Fixture:
    """One disposable desk, store, and book. Setup may queue and claim. Handoff does not."""

    def __init__(self, view: View, label: str, backend: str) -> None:
        self.view = view
        self.label = label
        self.backend = backend
        self.home = owned_temp(f"flow0519-{label}-")
        self.container = self.home / "container"
        self.root = self.container / "fixture"
        self.store = self.container / "clerk-store"
        self.instructions = self.home / "instructions"
        self.book = self.home / "book"
        self.source = self.home / "report-source"
        self.record = self.home / "handoff-record"
        self.failure_log = self.home / "failure.log"
        self.binding_path = self.home / "binding.json"
        self.job_id = "clerk-0001"
        self.delivery = "bridge-0001"
        self.member = ""
        self.submission = "fixture-" + label
        self.event_sha = ""
        self.report = b""
        self.setup: dict[str, dict] = {}
        try:
            self._stand()
        except Exception:
            self.close()
            raise

    def close(self) -> None:
        remove_owned(self.home)

    def clerk(self) -> Path:
        return self.view.root / "labs/clerk-handoff-pass02/clerk.py"

    def capture_tool(self) -> Path:
        return self.view.root / "labs/return-capture-pass01/return_capture.py"

    def launches(self) -> list[str]:
        path = self.root / "bridge/delivery" / self.delivery / "output/launches.log"
        if not path.is_file():
            return []
        return path.read_text(encoding="utf-8").splitlines()

    def returned_event(self) -> Path:
        return self.store / "jobs" / self.job_id / "0003.returned.json"

    def outbox_result(self) -> Path:
        return self.store / "jobs" / self.job_id / "outbox/result.json"

    def _stand(self) -> None:
        outside_git(self.home)
        self.container.mkdir()
        self.instructions.mkdir()
        self.book.mkdir()
        self.source.mkdir()
        (self.root / "00.kernel/00.00.10.work/0401.goal").mkdir(parents=True)
        (self.root / "00.kernel/00.00.01.law").mkdir(parents=True)
        (self.root / "00.kernel/00.00.10.work/0504.app-entry").mkdir(parents=True)
        (self.root / RECORD_REL).write_bytes(_record_text())
        (self.root / WORK_REF).write_bytes(b"fixture work item\n")
        task = self.view.packed[TASK_REL]["data"]
        job = self.view.packed[JOB_REL]["data"]
        clerk_job = self.view.packed[CLERK_JOB_REL]["data"]
        if digest(task) != TASK_SHA or digest(job) != JOB_SHA or digest(clerk_job) != CLERK_JOB_SHA:
            raise PinError("design fixture bytes do not match the pack")
        (self.instructions / "task.md").write_bytes(task)
        declared = self.root / "bridge/declared"
        declared.mkdir(parents=True)
        (declared / "task.md").write_bytes(task)
        if self.backend != "fixture-ok":
            value = json.loads(job.decode("utf-8"))
            value["backend"] = self.backend
            job = (json.dumps(value, indent=2) + "\n").encode("utf-8")
        (self.root / "bridge/job.json").write_bytes(job)
        link = {
            "schema": "librarian-clerk-link",
            "version": 1,
            "delivery_id": self.delivery,
            "clerk_store": str(self.store.resolve()),
            "clerk_job_id": self.job_id,
            "bridge_job": "bridge/job.json",
            "bridge_job_sha256": digest(job),
        }
        link_dir = self.root / "clerk-link"
        link_dir.mkdir()
        (link_dir / "bridge-0001.json").write_bytes((json.dumps(link, indent=2) + "\n").encode("utf-8"))
        job_path = self.home / "clerk-job.json"
        job_path.write_bytes(clerk_job)
        queued = run_cli(self.clerk(), [
            "queue", "--store", str(self.store), "--job", str(job_path),
            "--instructions-base", str(self.instructions),
        ])
        self.setup["queue"] = queued
        if queued["code"] != 0:
            raise ProofError(f"queue failed\n{queued['stdout']}{queued['stderr']}")
        claimed = run_cli(self.clerk(), [
            "claim", "--store", str(self.store), "--job", self.job_id,
            "--as", "fixture-worker", "--instructions-base", str(self.instructions),
        ])
        self.setup["claim"] = claimed
        if claimed["code"] != 0:
            raise ProofError(f"claim failed\n{claimed['stdout']}{claimed['stderr']}")

    def deliver(self) -> dict:
        try:
            result = self.view.seam.perform(
                self.view.context,
                self.view.root,
                self.root,
                link_rel="clerk-link/bridge-0001.json",
                actor="fixture-worker",
                instructions_base=str(self.instructions),
                explicit=str(self.container),
            )
        except self.view.context.Stop as exc:
            return {"kind": "stop", "code": 2, "text": str(exc), "stderr": ""}
        return {"kind": "result", "code": result.code, "text": result.text, "stderr": ""}

    def show(self) -> dict:
        shown = run_cli(self.clerk(), [
            "show", "--store", str(self.store), "--job", self.job_id,
            "--instructions-base", str(self.instructions), "--json",
        ])
        document = None
        if shown["code"] == 0 and shown["stdout"].strip():
            document = json.loads(shown["stdout"])
        shown["document"] = document
        return shown

    def bind(self) -> str:
        self.report = self.outbox_result().read_bytes()
        (self.source / "result.json").write_bytes(self.report)
        event = self.returned_event().read_bytes()
        self.event_sha = digest(event)
        reserved = run_cli(self.capture_tool(), [
            "reserve", "--book", str(self.book), "--submission", self.submission,
            "--name", "flow", "--origin-book", "00.00.10.work",
            "--origin-page", "0504.app-entry", "--origin-batch", "05.19",
            "--submitter", "Fixture Submitter", "--reviewer", "Fixture Reviewer",
            "--release", "fixture reservation; not a release",
            "--expected-output", "result.json",
        ])
        self.setup["reserve"] = reserved
        if reserved["code"] != 0:
            raise ProofError(f"reserve failed\n{reserved['stdout']}{reserved['stderr']}")
        self.member = field(reserved["stdout"], "member ")
        body = {
            "artifact_base": str(self.outbox_result().parent.resolve()),
            "artifacts": [{
                "bytes": len(self.report),
                "clerk_path": "result.json",
                "logical": "result.json",
                "sha256": digest(self.report),
                "source": "result.json",
            }],
            "assignee": "fixture-worker",
            "book": str(self.book.resolve()),
            "clerk_store": str(self.store.resolve()),
            "failure_log": str(self.failure_log.resolve()),
            "instructions_base": str(self.instructions.resolve()),
            "job_id": self.job_id,
            "member": self.member,
            "origin": {"batch": "05.19", "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str(self.record.resolve()),
            "report": {
                "bytes": len(self.report),
                "clerk_path": "result.json",
                "sha256": digest(self.report),
                "source": "result.json",
            },
            "returned_event_sha256": self.event_sha,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(self.source.resolve()),
            "submission_id": self.submission,
            "work_ref": WORK_REF,
        }
        self.binding_path.write_bytes(canonical(body))
        return str(self.binding_path.resolve())

    def perform(self, path: str | None = None, **kwargs) -> dict:
        buf = io.StringIO()
        with _redirect(buf):
            code = self.view.handoff.perform(path or str(self.binding_path.resolve()), **kwargs)
        text = buf.getvalue()
        return {"code": code, "text": text}

    def durable(self) -> dict[str, dict[str, str]]:
        member = self.book / self.member if self.member else self.book / "missing-member"
        return {
            "source": _index(self.source),
            "job": _index(self.store / "jobs" / self.job_id),
            "member": _index(member) if member.exists() else {},
            "record": _index(self.record) if self.record.exists() else {},
            "launch_sha256": _file_sha(self.root / "bridge/delivery" / self.delivery / "output/launches.log"),
            "returned_event_sha256": _file_sha(self.returned_event()),
            "result_sha256": _file_sha(self.outbox_result()),
        }

    def identities(self) -> dict:
        report_sha = digest(self.report) if self.report else None
        member = self.book / self.member if self.member else None
        return_bytes = None
        payload = {}
        receipt_sha = None
        if member is not None and member.is_dir():
            return_path = member / "return.md"
            if return_path.is_file():
                return_bytes = return_path.read_bytes()
            payload_dir = member / "payload"
            if payload_dir.is_dir():
                for name in sorted(os.listdir(payload_dir)):
                    path = payload_dir / name
                    if path.is_file():
                        payload[name] = digest(path.read_bytes())
            receipt = member / "receipt.json"
            if receipt.is_file():
                receipt_sha = file_digest(receipt)
        return {
            "label": "fixture",
            "backend": self.backend,
            "work_ref": WORK_REF,
            "work_ref_role": "declared-label",
            "delivery_id": self.delivery,
            "job_id": self.job_id,
            "submission_id": self.submission,
            "member": self.member,
            "returned_event_sha256": self.event_sha or None,
            "report_sha256": report_sha,
            "report_bytes": len(self.report) if self.report else None,
            "report_text": self.report.decode("utf-8") if self.report else None,
            "return_md_sha256": digest(return_bytes) if return_bytes is not None else None,
            "return_md_equals_report": return_bytes == self.report if return_bytes is not None else None,
            "payload": payload,
            "receipt_sha256": receipt_sha,
            "launches": self.launches(),
            "returned_event_present": self.returned_event().is_file(),
        }


class _redirect:
    def __init__(self, buf: io.StringIO) -> None:
        self.buf = buf
        self._old = None

    def __enter__(self):
        self._old = sys.stdout
        sys.stdout = self.buf
        return self.buf

    def __exit__(self, *_args):
        sys.stdout = self._old
        return False


def _call_handoff(view: View, path: str, **kwargs) -> dict:
    buf = io.StringIO()
    with _redirect(buf):
        code = view.handoff.perform(path, **kwargs)
    return {"code": code, "text": buf.getvalue()}


def prove_closure(view: View) -> dict:
    require_closure(view.root, view.packed)
    excluded = exclusion_record()
    if excluded["copied"] or (view.root / LIBRARIAN_REL).exists():
        raise ProofError("librarian was copied")
    if excluded["live_sha256"] == excluded["snapshot_sha256"]:
        raise ProofError("expected the recorded live librarian difference")
    return {
        "expected": "pass",
        "files": view.files,
        "excluded": excluded,
        "manifest_sha256": MANIFEST_SHA,
        "provenance_sha256": PROVENANCE_SHA,
        "bad": 0,
        "runner": {"path": RUNNER_REL, "sha256": RUNNER_SHA, "bytes": RUNNER_BYTES, "pack_snapshot": False},
    }


def prove_malformed(view: View) -> dict:
    result = _call_handoff(view, "binding.json")
    if result["code"] != 2 or "binding path must be absolute" not in result["text"]:
        raise ProofError(result["text"])
    if "Traceback" in result["text"] or "result refused" not in result["text"]:
        raise ProofError(result["text"])
    return {"expected": "refusal", "code": result["code"], "text": result["text"], "launches": []}


def prove_unsafe(view: View) -> dict:
    home = owned_temp("flow0519-unsafe-")
    try:
        binding = {
            "artifact_base": str((home / "outbox").resolve()),
            "artifacts": [{
                "bytes": 1,
                "clerk_path": "result.json",
                "logical": "result.json",
                "sha256": "0" * 64,
                "source": "result.json",
            }],
            "assignee": "fixture-worker",
            "book": str(home.resolve()),
            "clerk_store": str(home.resolve()),
            "failure_log": str((home / "failure.log").resolve()),
            "instructions_base": str(home.resolve()),
            "job_id": "clerk-0001",
            "member": "0101.flow",
            "origin": {"batch": "05.19", "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str((home / "record").resolve()),
            "report": {
                "bytes": 1,
                "clerk_path": "result.json",
                "sha256": "0" * 64,
                "source": "../secret",
            },
            "returned_event_sha256": "1" * 64,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(home.resolve()),
            "submission_id": "fixture-unsafe",
            "work_ref": WORK_REF,
        }
        path = home / "binding.json"
        path.write_bytes(canonical(binding))
        refused = _call_handoff(view, str(path.resolve()))
        if refused["code"] != 2 or "report source is not a simple filename" not in refused["text"]:
            raise ProofError(refused["text"])
        if "Traceback" in refused["text"]:
            raise ProofError(refused["text"])
        try:
            view.seam.perform(
                view.context,
                view.root,
                view.root,
                link_rel="clerk-link/bridge-0001.json",
                actor="fixture-worker",
                instructions_base=str(view.root),
            )
        except view.context.Stop as exc:
            message = str(exc)
        else:
            raise ProofError("seam accepted a fixture root that is the source-view")
        if message != "fixture root is the live workspace":
            raise ProofError(message)
        if (view.root / "bridge/delivery").exists():
            raise ProofError("unsafe seam launched a delivery")
        return {
            "expected": "refusal",
            "binding": refused,
            "seam_stop": message,
            "launches": [],
        }
    finally:
        remove_owned(home)


def prove_bad_pin(view: View) -> dict:
    home = owned_temp("flow0519-badpin-")
    fixture = None
    try:
        tampered = home / "source-view"
        shutil.copytree(view.root, tampered)
        clerk = tampered / "labs/clerk-handoff-pass02/clerk.py"
        data = clerk.read_bytes()
        mid = len(data) // 2
        clerk.write_bytes(data[:mid] + bytes([data[mid] ^ 0x01]) + data[mid + 1:])
        try:
            require_closure(tampered, view.packed)
        except PinError as exc:
            pin_message = str(exc)
        else:
            raise ProofError("tampered closure was accepted")
        if "closure hash does not match" not in pin_message:
            raise ProofError(pin_message)
        fixture = Fixture(view, "badpin", "fixture-ok")
        try:
            view.seam.perform(
                view.context,
                tampered,
                fixture.root,
                link_rel="clerk-link/bridge-0001.json",
                actor="fixture-worker",
                instructions_base=str(fixture.instructions),
                explicit=str(fixture.container),
            )
        except view.context.Stop as exc:
            seam_message = str(exc)
        else:
            raise ProofError("tampered clerk pin was accepted")
        if seam_message != "clerk pin does not match":
            raise ProofError(seam_message)
        if fixture.launches():
            raise ProofError(f"worker launched on a bad pin: {fixture.launches()}")
        if fixture.returned_event().exists() or fixture.outbox_result().exists():
            raise ProofError("bad pin wrote a return")
        return {
            "expected": "refusal",
            "closure": pin_message,
            "seam_stop": seam_message,
            "queue": fixture.setup["queue"],
            "claim": fixture.setup["claim"],
            "launches": fixture.launches(),
        }
    finally:
        if fixture is not None:
            fixture.close()
        remove_owned(home)


def _payload_matches(fixture: Fixture) -> bool:
    member = fixture.book / fixture.member / "payload"
    if not member.is_dir():
        return False
    blobs = [path.read_bytes() for path in member.iterdir() if path.is_file()]
    return any(blob == fixture.report for blob in blobs)


def _success_checks(fixture: Fixture, seam: dict, handoff: dict) -> None:
    if seam["code"] != 0 or "Traceback" in seam["text"]:
        raise ProofError(seam["text"])
    for phrase in ("transport: delivered", "collection: collected", "review: not performed", "acceptance: not performed"):
        if phrase not in seam["text"]:
            raise ProofError(seam["text"])
    if "approval" in seam["text"] or "clerk: returned" not in seam["text"]:
        raise ProofError(seam["text"])
    if fixture.launches() != ["bridge-0001 ok"]:
        raise ProofError(f"launches {fixture.launches()}")
    if digest(fixture.report) != RESULT_SHA:
        raise ProofError(f"synthetic report {digest(fixture.report)}")
    if not fixture.identities()["return_md_equals_report"] or not _payload_matches(fixture):
        raise ProofError("report bytes were not preserved")
    if handoff["code"] != 0 or "result ok" not in handoff["text"] or "writes none" in handoff["text"]:
        raise ProofError(handoff["text"])
    for phrase in ("result complete", "not approved", "not accepted", "not published", "work-ref-role declared-label"):
        if phrase not in handoff["text"]:
            raise ProofError(handoff["text"])
    if "completed.json" not in fixture.durable()["record"] or "intent.json" not in fixture.durable()["record"]:
        raise ProofError("handoff record is incomplete")


def prove_success(view: View) -> dict:
    fixture = Fixture(view, "complete", "fixture-ok")
    try:
        seam = fixture.deliver()
        if seam["code"] != 0:
            raise ProofError(json.dumps(seam))
        fixture.bind()
        handoff = fixture.perform()
        _success_checks(fixture, seam, handoff)
        shown = fixture.show()
        evidence = ""
        if shown["document"] and isinstance(shown["document"].get("returned"), dict):
            evidence = str(shown["document"]["returned"].get("evidence", ""))
        if not evidence or evidence.encode("utf-8") == fixture.report:
            raise ProofError("transport evidence is not distinct from the synthetic report")
        before = fixture.durable()
        replay = fixture.deliver()
        again = fixture.perform()
        after = fixture.durable()
        if replay["code"] != 0 or fixture.launches() != ["bridge-0001 ok"]:
            raise ProofError(f"repetition launched again\n{replay['text']}\n{fixture.launches()}")
        if again["code"] != 0 or "writes none" not in again["text"]:
            raise ProofError(again["text"])
        if before != after:
            raise ProofError("repetition changed durable bytes")
        if after["returned_event_sha256"] != fixture.event_sha:
            raise ProofError("returned event changed")
        member_before = before["member"]
        changed = dict(json.loads(fixture.binding_path.read_text(encoding="utf-8")))
        flip = "0" if fixture.event_sha[-1] != "0" else "1"
        changed["returned_event_sha256"] = fixture.event_sha[:-1] + flip
        changed_path = fixture.home / "binding-changed.json"
        changed_path.write_bytes(canonical(changed))
        changed_result = fixture.perform(str(changed_path.resolve()))
        if changed_result["code"] != 2 or "returned event does not match the binding" not in changed_result["text"]:
            raise ProofError(changed_result["text"])
        if fixture.durable()["member"] != member_before or fixture.launches() != ["bridge-0001 ok"]:
            raise ProofError("changed binding replaced the capture or launched a worker")
        source = fixture.source / "result.json"
        source.write_bytes(fixture.report + b"\n")
        payload_result = fixture.perform()
        if payload_result["code"] != 2 or "source bytes are not the outbox bytes" not in payload_result["text"]:
            raise ProofError(payload_result["text"])
        if fixture.durable()["member"] != member_before or fixture.launches() != ["bridge-0001 ok"]:
            raise ProofError("changed payload replaced the capture or launched a worker")
        return {
            "complete": {
                "expected": "pass",
                "seam": seam,
                "handoff": handoff,
                "show": shown,
                "setup": fixture.setup,
                "identities": fixture.identities(),
                "transport_evidence": evidence,
                "transport_distinct": True,
                "tree": before,
            },
            "repetition": {
                "expected": "pass",
                "seam": replay,
                "handoff": again,
                "before": before,
                "after": after,
                "unchanged": True,
                "launches": fixture.launches(),
            },
            "changed-binding": {
                "expected": "refusal",
                "handoff": changed_result,
                "member_unchanged": True,
                "launches": fixture.launches(),
            },
            "changed-payload": {
                "expected": "refusal",
                "handoff": payload_result,
                "member_unchanged": True,
                "launches": fixture.launches(),
            },
        }
    finally:
        fixture.close()


def prove_failed(view: View) -> dict:
    fixture = Fixture(view, "crash", "fixture-crash")
    try:
        seam = fixture.deliver()
        if seam["code"] == 0 or "Traceback" in seam["text"] or "Traceback" in seam.get("stderr", ""):
            raise ProofError(json.dumps(seam))
        if fixture.launches() != ["bridge-0001 crash"]:
            raise ProofError(f"launches {fixture.launches()}")
        if fixture.returned_event().exists() or fixture.outbox_result().exists():
            raise ProofError("failed delivery wrote a collected return")
        if list(fixture.book.iterdir()) or fixture.record.exists() or fixture.failure_log.exists():
            raise ProofError("failed delivery reserved or captured")
        return {
            "expected": "refusal",
            "seam": seam,
            "setup": fixture.setup,
            "launches": fixture.launches(),
            "returned_event_present": False,
            "capture": "not called",
        }
    finally:
        fixture.close()


def prove_stop(view: View) -> dict:
    fixture = Fixture(view, "stop", "fixture-ok")
    try:
        seam = fixture.deliver()
        if seam["code"] != 0:
            raise ProofError(json.dumps(seam))
        fixture.bind()
        report = fixture.report

        def hook(point: str):
            if point == "after-capture":
                return "stop"
            return None

        stopped = fixture.perform(hook=hook)
        text = stopped["text"]
        if stopped["code"] != 2 or not text.startswith("attention: stopped after-capture"):
            raise ProofError(text)
        if not text.rstrip().endswith("result attention"):
            raise ProofError(text)
        for phrase in (
            "member-written observed",
            "custody complete",
            "observed-record intent.json",
            "record-absent completed.json",
            "handoff-complete no",
        ):
            if phrase not in text:
                raise ProofError(text)
        member = fixture.book / fixture.member
        return_bytes = (member / "return.md").read_bytes()
        if return_bytes != report:
            raise ProofError("retained return.md is not the synthetic report")
        for name in ("return.md", "manifest.json", "receipt.json"):
            if not (member / name).is_file():
                raise ProofError(f"retained file missing: {name}")
        if (fixture.record / "completed.json").exists():
            raise ProofError("stop wrote completed.json")
        failure = fixture.failure_log.read_text(encoding="utf-8")
        reserved_mark = '"status":"reserved"' in failure or '"status": "reserved"' in failure
        if "result captured" not in failure or not reserved_mark:
            raise ProofError(failure)
        receipt_before = (member / "receipt.json").read_bytes()
        member_before = _index(member)
        retry = fixture.perform()
        if retry["code"] != 2 or "complete capture has no completed handoff record" not in retry["text"]:
            raise ProofError(retry["text"])
        if (fixture.record / "completed.json").exists():
            raise ProofError("retry resumed the handoff")
        if (member / "receipt.json").read_bytes() != receipt_before or _index(member) != member_before:
            raise ProofError("retry replaced the retained capture")
        if fixture.launches() != ["bridge-0001 ok"]:
            raise ProofError(f"stop retry launched a worker: {fixture.launches()}")
        return {
            "stop-after-capture": {
                "expected": "refusal",
                "seam": seam,
                "handoff": stopped,
                "failure_log": failure,
                "identities": fixture.identities(),
                "launches": fixture.launches(),
            },
            "stop-retry": {
                "expected": "refusal",
                "handoff": retry,
                "completed_absent": True,
                "receipt_unchanged": True,
                "launches": fixture.launches(),
            },
        }
    finally:
        fixture.close()


def build_evidence() -> dict:
    before = live_hashes()
    view = open_view()
    try:
        closure = prove_closure(view)
        malformed = prove_malformed(view)
        unsafe = prove_unsafe(view)
        bad_pin = prove_bad_pin(view)
        success = prove_success(view)
        failed = prove_failed(view)
        stopped = prove_stop(view)
        after = live_hashes()
        if before != after:
            raise ProofError("live bytes changed during the rehearsal")
        return {
            "schema": "flow05.19-results",
            "date": "2026-10-28",
            "label": "fixture",
            "model": False,
            "live_job": False,
            "app_wired": False,
            "pack": {
                "manifest_sha256": MANIFEST_SHA,
                "manifest_bytes": MANIFEST_BYTES,
                "provenance_sha256": PROVENANCE_SHA,
                "provenance_bytes": PROVENANCE_BYTES,
                "bad": 0,
                "baseline_commit": "d017f9f7e8271db6de3b72d31a82077c5ef588c4",
            },
            "source_view": {
                "files": closure["files"],
                "runner": closure["runner"],
                "excluded": closure["excluded"],
            },
            "cases": {
                "closure": closure,
                "malformed-binding": malformed,
                "unsafe-path": unsafe,
                "failed-pin": bad_pin,
                "complete": success["complete"],
                "repetition": success["repetition"],
                "changed-binding": success["changed-binding"],
                "changed-payload": success["changed-payload"],
                "failed-delivery": failed,
                "stop-after-capture": stopped["stop-after-capture"],
                "stop-retry": stopped["stop-retry"],
            },
            "live_hashes_unchanged": True,
            "unknowns": [
                "same-user gap between a hash read and a later write remains open",
                "this rehearsal is not an operating-system sandbox",
                "the single-launch observation is not a general exactly-once guarantee",
                "an unknown pin, timeout, or inspection outcome stays unknown",
                "recovery and a new submission are outside this rehearsal",
                "file-symlink creation was not re-tested; WinError 1314 remains a platform limit",
            ],
        }
    finally:
        remove_owned(view.home)


def write_evidence(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
