#!/usr/bin/env python3
"""Controlled interleavings for shared bridge parents.

These checks call the real helper. They do not sleep and they do not edit the lab.
"""

from __future__ import annotations

import importlib.util
import os
import stat
import subprocess
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


class Suite:
    def __init__(self) -> None:
        self.passed, self.refusals, self.failed = [], [], []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        print(f"PASS {name}", flush=True)

    def refusal(self, name: str) -> None:
        self.refusals.append(name)
        print(f"REFUSAL {name}", flush=True)

    def fail(self, name: str, detail: str) -> None:
        self.failed.append(name)
        print(f"FAIL {name}: {detail}", flush=True)


SUITE = Suite()


class Stop(Exception):
    pass


class Ctx:
    def stop(self, message: str) -> None:
        raise Stop(message)


def load():
    path = REPO / "app" / "worker_bridge.py"
    spec = importlib.util.spec_from_file_location("bridge_dirs_under_test", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def cleanup(home: Path) -> None:
    if not os.path.lexists(home):
        return
    for dirpath, dirnames, _filenames in os.walk(home):
        kept = []
        for name in dirnames:
            path = Path(dirpath) / name
            if is_reparse(path):
                os.rmdir(path)
            else:
                kept.append(name)
        dirnames[:] = kept
    subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(home)], check=False)


def race(path: Path, plant) -> None:
    real = os.mkdir
    fired = {"n": 0}

    def hooked(name, mode=0o777, *args, **kwargs):
        if Path(name) == path and fired["n"] == 0:
            fired["n"] = 1
            plant(real)
        return real(name, mode, *args, **kwargs)

    os.mkdir = hooked
    try:
        yield_ran = True
        return fired
    finally:
        os.mkdir = real
        del yield_ran


class Race:
    def __init__(self, path: Path, plant) -> None:
        self.path = path
        self.plant = plant
        self.real = os.mkdir
        self.fired = 0

    def __enter__(self):
        path = self.path
        plant = self.plant
        real = self.real
        holder = self

        def hooked(name, mode=0o777, *args, **kwargs):
            if Path(name) == path and holder.fired == 0:
                holder.fired = 1
                plant(real)
            return real(name, mode, *args, **kwargs)

        os.mkdir = hooked
        return self

    def __exit__(self, exc_type, exc, tb):
        os.mkdir = self.real
        return False


def check(name: str, fn) -> None:
    home = Path(tempfile.mkdtemp(prefix="bridge0512-"))
    try:
        fn(home)
    except Exception:
        SUITE.fail(name, traceback.format_exc())
    finally:
        cleanup(home)


def test_plain_parent_race(home: Path) -> None:
    bridge = load()
    path = home / "shared-parent"

    def plant(real) -> None:
        real(path)

    with Race(path, plant) as raced:
        bridge._ensure_plain_dir(Ctx(), path, "shared parent")
    if raced.fired != 1 or not path.is_dir() or is_reparse(path):
        raise AssertionError("plain parent was not revalidated")
    bridge._ensure_plain_dir(Ctx(), path, "shared parent")
    SUITE.ok("raced ordinary parent is a plain directory")


def test_file_parent_race(home: Path) -> None:
    bridge = load()
    path = home / "shared-parent"
    payload = b"kept-bytes\n"

    def plant(real) -> None:
        del real
        path.write_bytes(payload)

    with Race(path, plant):
        try:
            bridge._ensure_plain_dir(Ctx(), path, "shared parent")
        except Stop as exc:
            if "not a plain directory" not in str(exc):
                raise
        else:
            raise AssertionError("file parent was accepted")
    if path.read_bytes() != payload or path.is_dir():
        raise AssertionError("raced file was replaced")
    SUITE.refusal("raced file parent is refused and retained")


def test_junction_parent_race(home: Path) -> None:
    bridge = load()
    path = home / "shared-parent"
    target = home / "junction-target"
    target.mkdir()
    (target / "keep.txt").write_bytes(b"keep\n")

    def plant(real) -> None:
        del real
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(path), str(target)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise AssertionError(proc.stdout + proc.stderr)

    with Race(path, plant):
        try:
            bridge._ensure_plain_dir(Ctx(), path, "bridge delivery")
        except Stop as exc:
            if "not a plain directory" not in str(exc):
                raise
        else:
            raise AssertionError("junction parent was accepted")
    if (target / "keep.txt").read_bytes() != b"keep\n" or not is_reparse(path):
        raise AssertionError("junction target changed")
    SUITE.refusal("raced junction parent is refused and retained")


def test_exclusive_occupied(home: Path) -> None:
    bridge = load()
    path = home / "bridge-0001"
    path.mkdir()
    (path / "marker.txt").write_bytes(b"occupied\n")
    try:
        bridge._exclusive_dir(Ctx(), path, "per-delivery directory")
    except Stop as exc:
        if "already present" not in str(exc):
            raise
    else:
        raise AssertionError("occupied delivery was accepted")
    if (path / "marker.txt").read_bytes() != b"occupied\n":
        raise AssertionError("occupied delivery was overwritten")
    SUITE.refusal("occupied per-delivery directory is refused")


def test_exclusive_race(home: Path) -> None:
    bridge = load()
    path = home / "bridge-0001"

    def plant(real) -> None:
        real(path)
        (path / "marker.txt").write_bytes(b"occupied\n")

    with Race(path, plant) as raced:
        try:
            bridge._exclusive_dir(Ctx(), path, "per-delivery directory")
        except Stop as exc:
            if "already present" not in str(exc):
                raise
        else:
            raise AssertionError("raced delivery was accepted")
    if raced.fired != 1 or (path / "marker.txt").read_bytes() != b"occupied\n":
        raise AssertionError("raced delivery was overwritten")
    other = home / "bridge-0002"
    bridge._exclusive_dir(Ctx(), other, "per-delivery directory")
    if not other.is_dir() or path.resolve() == other.resolve():
        raise AssertionError("a different delivery directory was not exclusive")
    try:
        bridge._exclusive_dir(Ctx(), other, "per-delivery directory")
    except Stop as exc:
        if "already present" not in str(exc):
            raise
    else:
        raise AssertionError("second exclusive create was accepted")
    SUITE.refusal("raced per-delivery directory stays exclusive")
    SUITE.ok("a different delivery directory is created once")


def main() -> None:
    for name, fn in (
        ("plain", test_plain_parent_race),
        ("file", test_file_parent_race),
        ("junction", test_junction_parent_race),
        ("occupied", test_exclusive_occupied),
        ("exclusive-race", test_exclusive_race),
    ):
        check(name, fn)
    print(
        f"summary pass {len(SUITE.passed)} "
        f"expected-refusal {len(SUITE.refusals)} "
        f"skip 0 "
        f"fail {len(SUITE.failed)}"
    )
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
