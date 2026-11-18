#!/usr/bin/env python3
"""Convergence workbook successor (0522/05.19, note 06.41).

Loads the frozen pass02 workbook from its canonical pin. The code root is
this file's candidate root when the relative path is
labs/review-loop-convergence-pass03/workbook.py. A loose copy refuses.
Predecessor pins are checked before a command. build_intake is the same
preparation path as the CLI and resets source-kind context first.
There is no live-root fallback.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

LIVE = Path(r"D:\Git\lib-build")
PASS02_REL = "labs/review-loop-convergence-pass02/workbook.py"
PASS02_SHA = "a013e4466c79794eb62c7f697d222e693d8453af91571a404fedb0b4dcc4ef3f"
PASS02_BYTES = 6613
PIN_KEYS = ("form", "return_access", "review_loop", "construct", "prime_cycle", "prime_review")


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def _sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def candidate_root() -> Path:
    here = Path(__file__).resolve()
    if (
        here.name != "workbook.py"
        or here.parent.name != "review-loop-convergence-pass03"
        or here.parent.parent.name != "labs"
    ):
        refuse_boot("workbook is not at labs/review-loop-convergence-pass03/workbook.py")
    return here.parents[2]


ROOT = candidate_root()


def load_pass02():
    path = LIVE / PASS02_REL
    if path.is_symlink() or not path.is_file():
        refuse_boot("pass02 workbook pin is missing")
    data = path.read_bytes()
    if len(data) != PASS02_BYTES or _sha(data) != PASS02_SHA:
        refuse_boot("pass02 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_loop_convergence_pass02", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass02 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_pass02()
prior = base.base


def _bind_repo(module) -> None:
    current = getattr(module, "REPO", None)
    if isinstance(current, Path) and os.path.normcase(str(current)) == os.path.normcase(str(LIVE)):
        module.REPO = ROOT


for _module in (base, prior, prior.inst, prior.p5, prior.p4, prior.p3, prior.p2, prior.wb):
    _bind_repo(_module)
prior.wb.REPO = ROOT

classify_pack = base.classify_pack
pointer_block = base.pointer_block
_base_locate = prior.locate_declared


def locate_declared(book, rel, page=None):
    """Use the candidate root first. A path absent there is read from the live checkout.

    A file present in the candidate root stays on that root, so a different
    dispatcher remains visible. This function does not replace a present file
    with the live copy.
    """
    located, how = _base_locate(book, rel, page)
    if how != "missing":
        return located, how
    current = prior.wb.REPO
    if os.path.normcase(str(current)) == os.path.normcase(str(LIVE)):
        return located, how
    prior.wb.REPO = LIVE
    try:
        return _base_locate(book, rel, page)
    finally:
        prior.wb.REPO = current


prior.locate_declared = locate_declared
prior.p3.locate_declared = locate_declared
prior.p2.locate_declared = locate_declared
prior.wb.locate_declared = locate_declared


def _pins() -> None:
    for key in PIN_KEYS:
        prior.wb.pin_file(key)


def _reset() -> None:
    prior.inst.HOLD.set(None)
    prior.COMPARE.set(None)
    prior.N7_RENDER.set(False)


def build_intake(book, page, pass_id):
    """Same preparation path as CLI prepare, with source-kind context reset first."""
    _pins()
    _reset()
    return prior.build_intake(book, page, pass_id)


def main(argv: list[str] | None = None) -> int:
    try:
        _pins()
    except prior.wb.Refusal as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2
    return base.main(argv)


if __name__ == "__main__":
    sys.exit(main())
