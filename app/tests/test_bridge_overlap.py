#!/usr/bin/env python3
"""Two distinct Clerk deliveries overlapping on shared bridge parents.

The workers are the allowlisted fixture. A barrier starts both calls. The
fixture-sleep hold makes the overlap observable. This is not an exactly-once claim.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
CLERK = REPO / "labs" / "clerk-handoff-pass02" / "clerk.py"
EXAMPLE = REPO / "00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples"
EXAMPLE_TASK = EXAMPLE / "router/instructions/task.md"
WORK_REF = "00.kernel/00.00.10.work/0504.app-entry/05.01.md"
RECORD = "00.kernel/00.00.10.work/0401.goal/06.01.md"
SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
TASK_SHA = "6c913091d80948e3be49fa384b023ee3c43762599f3f61b47db885b4f846fe66"
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
ACTOR = "fixture-worker"
TIMEOUT_S = 60
OBSERVE_S = 25
DELIVER_TIMEOUT_S = 120
GUARDS = (
    "app/worker_bridge.py",
    "app/clerk_seam.py",
    "app/context.py",
    "app/librarian.py",
    "app/README.md",
    "app/tests/test_clerk_seam.py",
    "labs/clerk-handoff-pass02/clerk.py",
    "labs/worker-bridge-pass01/fixtures/worker_fixture.py",
    "labs/worker-bridge-pass01/profiles.json",
)

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


class StopHere(Exception):
    pass


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def record_text() -> bytes:
    values = {
        "record": "current-assignment",
        "schema": SCHEMA,
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


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def ordinary_dir(path: Path) -> bool:
    if is_reparse(path) or not path.is_dir():
        return False
    try:
        return path.resolve().parent == path.parent.resolve()
    except OSError:
        return False


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2) + "\n").encode("utf-8"))


def fields(text: str) -> dict[str, str]:
    found = {}
    for line in text.splitlines():
        key, sep, value = line.partition(": ")
        if sep:
            found[key] = value
    return found


def run(args: list[str], cwd: Path, timeout: float) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def show(proc: subprocess.CompletedProcess[str]) -> str:
    return f"exit {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"


class Slot:
    def __init__(self, delivery: str, clerk_job: str, instruction_name: str, instruction: bytes) -> None:
        self.delivery = delivery
        self.clerk_job = clerk_job
        self.instruction_name = instruction_name
        self.instruction = instruction
        self.digest = sha_bytes(instruction)
        self.job_rel = f"bridge/job-{delivery}.json"
        self.link_rel = f"clerk-link/{delivery}.json"


class World:
    def __init__(self) -> None:
        self.home = Path(tempfile.mkdtemp(prefix="bridge0513-"))
        self.foreign = Path(tempfile.mkdtemp(prefix="librarian-0513-cwd-"))
        (self.foreign / "note.txt").write_bytes(b"do-not-read\n")
        self.container = self.home / "container"
        self.root = self.container / "fixture"
        self.store = self.container / "clerk-store"
        self.instructions = self.home / "router" / "instructions"
        self.outside = self.home / "outside.txt"
        self.outside_bytes = b"outside-sentinel\n"
        self.slots: dict[str, Slot] = {}

    def plant_tree(self) -> None:
        task = EXAMPLE_TASK.read_bytes()
        if sha_bytes(task) != TASK_SHA or len(task) != 175:
            raise AssertionError("design task.md hash drifted")
        self.instructions.mkdir(parents=True)
        (self.root / "00.kernel/00.00.10.work/0401.goal").mkdir(parents=True)
        (self.root / "00.kernel/00.00.01.law").mkdir(parents=True)
        (self.root / "00.kernel/00.00.10.work/0504.app-entry").mkdir(parents=True)
        (self.root / RECORD).write_bytes(record_text())
        (self.root / WORK_REF).write_bytes(b"fixture work item\n")
        (self.root / "bridge/declared").mkdir(parents=True)
        (self.root / "clerk-link").mkdir(parents=True)
        self.outside.write_bytes(self.outside_bytes)
        other = b"One counted line.\n"
        self.add_slot("bridge-0001", "clerk-0001", "task.md", task, "fixture-sleep")
        self.add_slot("bridge-0002", "clerk-0002", "task-b.md", other, "fixture-sleep")

    def add_slot(self, delivery: str, clerk_job: str, name: str, instruction: bytes, backend: str) -> Slot:
        slot = Slot(delivery, clerk_job, name, instruction)
        self.slots[delivery] = slot
        (self.instructions / name).write_bytes(instruction)
        (self.root / "bridge/declared" / name).write_bytes(instruction)
        job = {
            "schema": "librarian-bridge-job",
            "version": 1,
            "delivery_id": delivery,
            "job_id": clerk_job,
            "role": "builder",
            "work_ref": WORK_REF,
            "backend": backend,
            "inputs": [
                {
                    "name": "task",
                    "path": name,
                    "sha256": slot.digest,
                    "bytes": len(instruction),
                }
            ],
            "limits": {
                "timeout_s": TIMEOUT_S,
                "max_stdout_bytes": 1048576,
                "max_stderr_bytes": 1048576,
            },
        }
        job_path = self.root / slot.job_rel
        write_json(job_path, job)
        link = {
            "schema": "librarian-clerk-link",
            "version": 1,
            "delivery_id": delivery,
            "clerk_store": str(self.store.resolve()),
            "clerk_job_id": clerk_job,
            "bridge_job": slot.job_rel,
            "bridge_job_sha256": sha_path(job_path),
        }
        write_json(self.root / slot.link_rel, link)
        clerk_job_path = self.home / "router" / f"{clerk_job}.json"
        write_json(
            clerk_job_path,
            {
                "job_id": clerk_job,
                "assignee": ACTOR,
                "reviewer": "codex-prime",
                "instructions": {"path": name, "sha256": slot.digest},
                "release": "fixture release, overlap 05.13",
                "routed_by": "router-fixture",
                "expected_outputs": ["result.json"],
            },
        )
        slot.clerk_path = clerk_job_path
        return slot

    def clerk(self, *args: str) -> subprocess.CompletedProcess[str]:
        proc = run([PY, "-B", str(CLERK), *args], self.foreign, 60)
        if proc.returncode != 0:
            raise AssertionError(show(proc))
        return proc

    def prepare(self, delivery: str) -> None:
        slot = self.slots[delivery]
        self.clerk(
            "queue",
            "--store",
            str(self.store),
            "--job",
            str(slot.clerk_path),
            "--instructions-base",
            str(self.instructions),
        )
        self.clerk(
            "claim",
            "--store",
            str(self.store),
            "--job",
            slot.clerk_job,
            "--as",
            ACTOR,
            "--instructions-base",
            str(self.instructions),
        )

    def deliver(self, delivery: str) -> subprocess.CompletedProcess[str]:
        slot = self.slots[delivery]
        return run(
            [
                PY,
                "-B",
                str(LIBRARIAN),
                "clerk-deliver",
                "--root",
                str(self.root),
                "--container",
                str(self.container),
                "--link",
                slot.link_rel,
                "--as",
                ACTOR,
                "--instructions-base",
                str(self.instructions),
            ],
            self.foreign,
            DELIVER_TIMEOUT_S,
        )

    def output(self, delivery: str, name: str) -> Path:
        return self.root / "bridge" / "delivery" / delivery / "output" / name

    def outbox(self, delivery: str) -> Path:
        return self.store / "jobs" / self.slots[delivery].clerk_job / "outbox" / "result.json"

    def launches(self, delivery: str) -> list[str]:
        path = self.output(delivery, "launches.log")
        if not path.is_file():
            return []
        return path.read_text(encoding="utf-8").splitlines()

    def snapshot(self, delivery: str) -> dict[str, str]:
        slot = self.slots[delivery]
        roots = [
            self.store / "jobs" / slot.clerk_job,
            self.root / "bridge" / "delivery" / delivery,
            self.root / "bridge" / "store" / delivery,
        ]
        found = {}
        for base in roots:
            if not base.exists():
                continue
            for dirpath, dirnames, filenames in os.walk(base):
                kept = []
                for name in dirnames:
                    path = Path(dirpath) / name
                    if is_reparse(path):
                        found[str(path)] = "reparse-dir"
                    else:
                        kept.append(name)
                dirnames[:] = kept
                for name in filenames:
                    path = Path(dirpath) / name
                    found[str(path)] = "reparse" if is_reparse(path) else sha_path(path)
        prov = self.root / "bridge" / "provenance" / f"{delivery}.json"
        if prov.is_file():
            found[str(prov)] = sha_path(prov)
        return found

    def close(self) -> None:
        for path in (self.home, self.foreign):
            if not os.path.lexists(path):
                continue
            for dirpath, dirnames, _filenames in os.walk(path):
                kept = []
                for name in dirnames:
                    child = Path(dirpath) / name
                    if is_reparse(child):
                        os.rmdir(child)
                    else:
                        kept.append(name)
                dirnames[:] = kept
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(path)], check=False)


def expect_collected(world: World, delivery: str, proc: subprocess.CompletedProcess[str], clerk_line: str) -> str:
    slot = world.slots[delivery]
    if proc.returncode != 0 or "Traceback" in proc.stdout or "Traceback" in proc.stderr:
        raise AssertionError(show(proc))
    got = fields(proc.stdout)
    if got.get("clerk_job") != slot.clerk_job or got.get("delivery_id") != delivery:
        raise AssertionError(show(proc))
    if got.get("transport") != "delivered" or got.get("collection") != "collected":
        raise AssertionError(show(proc))
    if got.get("clerk") != clerk_line or "review: not performed" not in proc.stdout:
        raise AssertionError(show(proc))
    if "acceptance: not performed" not in proc.stdout:
        raise AssertionError(show(proc))
    artifact_line = got.get("artifact", "")
    if "result.json sha256 " not in artifact_line:
        raise AssertionError(show(proc))
    digest = artifact_line.split("sha256 ", 1)[1].split(" ", 1)[0]
    output = world.output(delivery, "result.json").read_bytes()
    outbox = world.outbox(delivery).read_bytes()
    if sha_bytes(output) != digest or output != outbox:
        raise AssertionError(f"{delivery} artifact bytes diverged: {digest}")
    expected = canonical({"count": sum(1 for line in slot.instruction.decode("utf-8").splitlines() if line.strip())})
    if output != expected:
        raise AssertionError(f"{delivery} count artifact is {output!r}")
    prov = json.loads((world.root / "bridge/provenance" / f"{delivery}.json").read_text(encoding="utf-8"))
    if prov.get("delivery_id") != delivery or prov.get("job_id") != slot.clerk_job:
        raise AssertionError(f"provenance identity {prov.get('delivery_id')} {prov.get('job_id')}")
    if prov.get("job_sha256") != sha_path(world.root / slot.job_rel):
        raise AssertionError("provenance job hash does not match the job file")
    receipt = json.loads((world.root / "bridge/store" / delivery / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("delivery_id") != delivery or receipt.get("job_id") != slot.clerk_job:
        raise AssertionError("receipt identity crossed")
    returned = json.loads((world.store / "jobs" / slot.clerk_job / "0003.returned.json").read_text(encoding="utf-8"))
    if returned.get("delivery") != delivery or returned.get("by") != ACTOR:
        raise AssertionError("return event identity crossed")
    if world.launches(delivery) != [f"{delivery} sleep"]:
        raise AssertionError(world.launches(delivery))
    return digest


def main() -> None:
    before = {rel: sha_path(REPO / rel) for rel in GUARDS}
    world = World()
    try:
        world.plant_tree()
        world.prepare("bridge-0001")
        world.prepare("bridge-0002")
        barrier = threading.Barrier(2)
        procs: dict[str, subprocess.CompletedProcess[str]] = {}
        errors: list[str] = []

        def go(delivery: str) -> None:
            try:
                barrier.wait(timeout=30)
                procs[delivery] = world.deliver(delivery)
            except Exception:
                errors.append(delivery + "\n" + traceback.format_exc())

        threads = [threading.Thread(target=go, args=(delivery,)) for delivery in ("bridge-0001", "bridge-0002")]
        for thread in threads:
            thread.start()
        deadline = time.monotonic() + OBSERVE_S
        observed = False
        while time.monotonic() < deadline:
            markers = [world.output(delivery, "started.marker").is_file() for delivery in ("bridge-0001", "bridge-0002")]
            results = [world.output(delivery, "result.json").exists() for delivery in ("bridge-0001", "bridge-0002")]
            if all(markers) and not any(results):
                observed = True
                print("OVERLAP both started.marker files exist and neither result.json exists", flush=True)
                print("OVERLAP launches", world.launches("bridge-0001"), world.launches("bridge-0002"), flush=True)
                break
            time.sleep(0.05)
        for thread in threads:
            thread.join(timeout=DELIVER_TIMEOUT_S + 5)
        if errors:
            raise AssertionError("\n".join(errors))
        if not observed:
            raise AssertionError("overlap was not observed within the bound")
        if any(thread.is_alive() for thread in threads):
            raise AssertionError("a delivery call did not finish")
        digests = {}
        for delivery in ("bridge-0001", "bridge-0002"):
            digests[delivery] = expect_collected(world, delivery, procs[delivery], "returned")
            print(
                f"IDENTITY {delivery} {world.slots[delivery].clerk_job} "
                f"artifact {digests[delivery]} launches {world.launches(delivery)}",
                flush=True,
            )
        if digests["bridge-0001"] == digests["bridge-0002"]:
            raise AssertionError("distinct jobs produced the same artifact")
        parents = [
            world.root / "bridge",
            world.root / "bridge" / "delivery",
            world.root / "bridge" / "store",
            world.root / "bridge" / "provenance",
        ]
        if not all(ordinary_dir(path) for path in parents):
            raise AssertionError("a shared parent is not an ordinary directory")
        if world.output("bridge-0001", "result.json").parent.parent.parent != world.root / "bridge" / "delivery":
            raise AssertionError("deliveries do not share bridge/delivery")
        print("PASS two overlapping deliveries collected separate artifacts", flush=True)

        frozen = {delivery: world.snapshot(delivery) for delivery in ("bridge-0001", "bridge-0002")}
        for delivery in ("bridge-0001", "bridge-0002"):
            replay = world.deliver(delivery)
            expect_collected(world, delivery, replay, "already-recorded")
            if "already in clerk outbox" not in replay.stdout:
                raise AssertionError(show(replay))
            if world.snapshot(delivery) != frozen[delivery]:
                raise AssertionError(f"{delivery} stored bytes changed on replay")
            if world.launches(delivery) != [f"{delivery} sleep"]:
                raise AssertionError(world.launches(delivery))
            print(f"REPLAY {delivery} already-recorded artifact {digests[delivery]}", flush=True)
        print("PASS identical replays are read-only", flush=True)

        occupied = world.root / "bridge" / "delivery" / "bridge-0003"
        marker = occupied / "marker.txt"
        payload = b"occupied-bytes\n"
        marker.parent.mkdir()
        marker.write_bytes(payload)
        world.add_slot("bridge-0003", "clerk-0003", "task.md", world.slots["bridge-0001"].instruction, "fixture-ok")
        world.prepare("bridge-0003")
        refused = world.deliver("bridge-0003")
        if refused.returncode != 2 or "Traceback" in refused.stdout or "Traceback" in refused.stderr:
            raise AssertionError(show(refused))
        if not refused.stderr.startswith("stop:") or "already present" not in refused.stderr:
            raise AssertionError(show(refused))
        if refused.stdout.strip():
            raise AssertionError(show(refused))
        if marker.read_bytes() != payload or world.launches("bridge-0003"):
            raise AssertionError("occupied delivery was replaced or launched")
        if world.snapshot("bridge-0001") != frozen["bridge-0001"] or world.snapshot("bridge-0002") != frozen["bridge-0002"]:
            raise AssertionError("occupied refusal changed an earlier delivery")
        print("REFUSAL occupied bridge-0003 is refused and its bytes stay", flush=True)
        if world.outside.read_bytes() != world.outside_bytes:
            raise AssertionError("outside sentinel changed")
        print("limit: not an exactly-once guarantee; same-job overlap remains the seam suite", flush=True)
    finally:
        world.close()
    after = {rel: sha_path(REPO / rel) for rel in GUARDS}
    if before != after:
        changed = [rel for rel in before if before[rel] != after.get(rel)]
        raise SystemExit("product bytes changed: " + ", ".join(changed))
    print("summary pass 2 expected-refusal 1 skip 0 fail 0", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        print("summary pass 0 expected-refusal 0 skip 0 fail 1", flush=True)
        raise SystemExit(1)
