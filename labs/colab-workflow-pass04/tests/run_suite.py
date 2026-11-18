"""Run the pass04 checks. A failing child fails the aggregate and earlier output stays."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(r"D:\Git\lib-build")
HERE = Path(__file__).resolve().parent


def aggregate(steps) -> int:
    code = 0
    for step in steps:
        if step() != 0:
            code = 1
    return code


def main() -> int:
    scripts = [HERE / "test_pass04.py", HERE / "test_real_two_pass.py"]

    def child(script: Path):
        def run() -> int:
            proc = subprocess.run([sys.executable, "-B", str(script)], cwd=str(ROOT), shell=False)
            print(f"child-exit {script.name} {proc.returncode}", flush=True)
            return proc.returncode

        return run

    return aggregate([child(script) for script in scripts])


if __name__ == "__main__":
    sys.exit(main())
