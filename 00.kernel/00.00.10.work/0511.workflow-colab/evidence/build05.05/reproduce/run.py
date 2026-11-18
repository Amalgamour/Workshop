"""Reproduce WF01 on frozen pass03. A runner exit of 0 means the defect was reproduced.

pass03 is not edited. The injection is a partial os.write after truncation has begun,
then OSError. It is not a process crash and not a power-loss trial.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Git\lib-build")
PASS03 = ROOT / "labs/colab-workflow-pass03/colab_workflow.py"
OUT_ROOT = ROOT / "00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.05/reproduce/runs"


def load_pass03():
    spec = importlib.util.spec_from_file_location("pass03_workflow", PASS03)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    cw = load_pass03()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_ROOT / stamp
    out.mkdir(parents=True)
    page_name = "0797.wf01"
    with tempfile.TemporaryDirectory(prefix="0511-0505-wf01-") as tmp:
        root = Path(tmp)
        note = b"# Notes\n"
        sources = root / "sources"
        dest = sources / "subj" / "note.md"
        dest.parent.mkdir(parents=True)
        dest.write_bytes(note)
        digest = cw.sha256(note)
        request = {
            "book": "00.00.10.work",
            "page": page_name,
            "pass": "05.01",
            "schema": "colab-exchange-open/1",
            "targets": [
                {
                    "book": "00.00.10.work",
                    "file": "note.md",
                    "id": "T01",
                    "page": "0411.colab",
                    "section": None,
                    "source": {
                        "commit": "6896224510fe0bcebac291fce7ed311a2cd085cb",
                        "path": "subj/note.md",
                        "repository": "workshop",
                        "sha256": digest,
                    },
                }
            ],
            "title": "Exchange question",
        }
        request_path = root / "open.json"
        request_path.write_bytes(cw.canonical(request))
        book = root / "book"
        book.mkdir()
        code, stdout, _err = cw.execute(
            ["open", "--book", str(book), "--request", str(request_path), "--sources", str(sources)]
        )
        if code != 0:
            raise SystemExit(stdout.decode("utf-8", "replace"))
        folder = book / page_name
        record = cw.require_loaded(folder)
        inv = folder / "investigation.json"
        seal = folder / "seal.json"
        before = inv.read_bytes()
        old_seal = seal.read_bytes()
        real_open = cw.os.open
        real_write = cw.os.write
        state = {"fd": None, "calls": 0, "done": False}

        def op(path, *args, **kwargs):
            fd = real_open(path, *args, **kwargs)
            if str(path) == str(inv):
                state["fd"] = fd
            return fd

        def wr(fd, data):
            if fd == state["fd"] and not state["done"]:
                state["calls"] += 1
                if state["calls"] == 1:
                    return real_write(fd, data[: max(1, len(data) // 2)])
                state["done"] = True
                raise OSError("SYNTHETIC mid-write failure after partial record write")
            return real_write(fd, data)

        cw.os.open = op
        cw.os.write = wr
        try:
            try:
                cw.commit(folder, record)
                outcome = "completed"
            except Exception as exc:
                outcome = type(exc).__name__ + ": " + str(exc)
        finally:
            cw.os.open = real_open
            cw.os.write = real_write
        after = inv.read_bytes()
        summary = {
            "schema": "colab-workflow-wf01-reproduction/1",
            "module": "labs/colab-workflow-pass03/colab_workflow.py",
            "module_sha256": __import__("hashlib").sha256(PASS03.read_bytes()).hexdigest(),
            "outcome": outcome,
            "before_bytes": len(before),
            "after_bytes": len(after),
            "prior_record_intact": after == before,
            "old_seal_intact": seal.read_bytes() == old_seal,
            "partial_marker": (folder / "partial.json").exists(),
            "checkpoint_dir": (folder / "checkpoints").exists(),
            "calls": state["calls"],
            "kind": "controlled partial-write injection, not process crash",
        }
        (out / "prior-investigation.json").write_bytes(before)
        (out / "torn-investigation.json").write_bytes(after)
        (out / "seal.json").write_bytes(old_seal)
        (out / "summary.json").write_bytes((json.dumps(summary, indent=2) + "\n").encode("utf-8"))
        print(json.dumps(summary, indent=2))
        print(out)
    reproduced = (
        summary["prior_record_intact"] is False
        and summary["old_seal_intact"] is True
        and summary["partial_marker"] is True
        and summary["checkpoint_dir"] is False
        and summary["outcome"].startswith("Refuse")
    )
    return 0 if reproduced else 1


if __name__ == "__main__":
    sys.exit(main())
