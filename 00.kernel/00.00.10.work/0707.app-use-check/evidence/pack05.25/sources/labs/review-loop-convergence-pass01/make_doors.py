#!/usr/bin/env python3
"""Write the convergence review-loop door and declaration from the frozen instance door.

The instance door and its declaration stay byte-identical. This file copies their
pin table, points the workbook pin at the convergence workbook, and adds the
instance, capacity, and N7-local reference pins. It does not import the N7 prototype.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LAB = REPO / "labs" / "review-loop-convergence-pass01"
INSTANCE_DOOR = REPO / "labs" / "review-instance-binding-pass01" / "review_loop_tools.py"
INSTANCE_JSON = REPO / "labs" / "review-instance-binding-pass01" / "review-loop.json"


def digest(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def main() -> int:
    wb_sha, wb_len = digest(LAB / "workbook.py")
    instance_sha, instance_len = digest(REPO / "labs" / "review-instance-binding-pass01" / "workbook.py")
    capacity_sha, capacity_len = digest(REPO / "labs" / "review-source-capacity-pass03" / "prime_review.py")
    local_sha, local_len = digest(REPO / "labs" / "n7-local-lifecycle-pass01" / "workbook.py")
    text = INSTANCE_DOOR.read_bytes().decode("utf-8")
    if "\r" in text:
        raise SystemExit("instance door has CR")
    replacements = (
        (
            '"""Unselected door for N5 book-instance applicability (0522/05.16, note 06.34).\n\n'
            "librarian.py does not load this module. The selected review-loop door stays v7.\n"
            "Workbook commands call labs/review-instance-binding-pass01/workbook.py.\n",
            '"""Unselected door for the convergence candidate (0522/05.17, note 06.36).\n\n'
            "librarian.py does not load this module. The selected review-loop door stays v7.\n"
            "Workbook commands call labs/review-loop-convergence-pass01/workbook.py.\n",
        ),
        (
            'CANONICAL_FILE = REPO / "labs" / "review-instance-binding-pass01" / "review_loop_tools.py"\n',
            'CANONICAL_FILE = REPO / "labs" / "review-loop-convergence-pass01" / "review_loop_tools.py"\n',
        ),
        ('SCHEMA = "review-loop-pins/8"\n', 'SCHEMA = "review-loop-pins/9"\n'),
        (
            'DECLARATION_REL = "labs/review-instance-binding-pass01/review-loop.json"\n',
            'DECLARATION_REL = "labs/review-loop-convergence-pass01/review-loop.json"\n',
        ),
        (
            'WB_SHA = "3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba"\nWB_BYTES = 5916\n',
            f'WB_SHA = "{wb_sha}"\nWB_BYTES = {wb_len}\n'
            f'INSTANCE_SHA = "{instance_sha}"\nINSTANCE_BYTES = {instance_len}\n'
            f'CAPACITY_SHA = "{capacity_sha}"\nCAPACITY_BYTES = {capacity_len}\n'
            f'N7_LOCAL_SHA = "{local_sha}"\nN7_LOCAL_BYTES = {local_len}\n',
        ),
        (
            '    "workbook_pass05",\n}',
            '    "workbook_pass05",\n    "workbook_instance",\n    "prime_review_capacity",\n    "workbook_n7_local",\n}',
        ),
        (
            '        refuse("review loop declaration schema is not review-loop-pins/8")\n',
            '        refuse("review loop declaration schema is not review-loop-pins/9")\n',
        ),
        (
            '    pin_named(code_root, "labs/review-instance-binding-pass01/workbook.py", WB_SHA, WB_BYTES, "review-instance")\n',
            '    pin_named(code_root, "labs/review-loop-convergence-pass01/workbook.py", WB_SHA, WB_BYTES, "convergence")\n'
            '    pin_named(code_root, "labs/review-instance-binding-pass01/workbook.py", INSTANCE_SHA, INSTANCE_BYTES, "review-instance")\n'
            '    pin_named(code_root, "labs/review-source-capacity-pass03/prime_review.py", CAPACITY_SHA, CAPACITY_BYTES, "capacity")\n'
            '    pin_named(code_root, "labs/n7-local-lifecycle-pass01/workbook.py", N7_LOCAL_SHA, N7_LOCAL_BYTES, "n7-local")\n',
        ),
        (
            '        print("refused: review-instance door is not at its canonical root", file=sys.stderr)\n',
            '        print("refused: convergence door is not at its canonical root", file=sys.stderr)\n',
        ),
    )
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit("door template match failed")
        text = text.replace(old, new, 1)
    if "review-loop-pins/8" in text or "review-instance-binding-pass01/review_loop_tools.py" in text:
        raise SystemExit("door template left an instance path in place")
    out = text.encode("utf-8")
    if b"\r" in out:
        raise SystemExit("convergence door gained CR")
    (LAB / "review_loop_tools.py").write_bytes(out)
    document = json.loads(INSTANCE_JSON.read_bytes())
    document["schema"] = "review-loop-pins/9"
    document["_note"] = (
        "Convergence candidate (0522/05.17, note 06.36). Workbook commands use "
        "labs/review-loop-convergence-pass01/workbook.py. The N7-local prototype is pinned "
        "and is not imported. Pass05, the instance workbook, the capacity successor, and "
        "v4 through v9 stay pinned. This declaration is unselected."
    )
    tools = document["tools"]
    tools["workbook"] = {
        "bytes": wb_len,
        "path": "labs/review-loop-convergence-pass01/workbook.py",
        "sha256": wb_sha,
    }
    tools["workbook_instance"] = {
        "bytes": instance_len,
        "path": "labs/review-instance-binding-pass01/workbook.py",
        "sha256": instance_sha,
    }
    tools["prime_review_capacity"] = {
        "bytes": capacity_len,
        "path": "labs/review-source-capacity-pass03/prime_review.py",
        "sha256": capacity_sha,
    }
    tools["workbook_n7_local"] = {
        "bytes": local_len,
        "path": "labs/n7-local-lifecycle-pass01/workbook.py",
        "sha256": local_sha,
    }
    payload = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (LAB / "review-loop.json").write_bytes(payload)
    print(f"door {hashlib.sha256(out).hexdigest()} {len(out)}")
    print(f"json {hashlib.sha256(payload).hexdigest()} {len(payload)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
