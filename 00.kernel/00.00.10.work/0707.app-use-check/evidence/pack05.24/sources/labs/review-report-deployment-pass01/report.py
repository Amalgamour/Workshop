#!/usr/bin/env python3
"""Deployment runtime for one selected read-only review report.

Contract review-report-deployment/1. This module checks the candidate
dispatcher and the historical dependency cut, then calls the accepted
pass03 observation. It does not call pass01.check_pins and it does not
launch pass03 main. Exit 0 is not a release.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

CONTRACT = "review-report-deployment/1"
HELPER_ROOT = Path(r"D:\Git\lib-build")
HELPER_MODULE = "labs/workbook-review-pass03/workbook.py"
REPARSE = 0x400
PINS = {
    "app/librarian.py": (12805, "d37dd14ccb921f92ff1a05c00890d57ee0f3d9f27d766bd86d81861abdd80a52"),
    "app/review-loop-v4.json": (2519, "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723"),
    "app/review-loop-v5.json": (1964, "eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3"),
    "app/review-loop-v6.json": (2743, "c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa"),
    "app/review-loop-v7.json": (3515, "bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8"),
    "app/review_loop_tools_v4.py": (13381, "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296"),
    "app/review_loop_tools_v5.py": (7875, "b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9"),
    "app/review_loop_tools_v6.py": (9175, "e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94"),
    "app/review_loop_tools_v7.py": (10291, "93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d"),
    "labs/prime-cycle-pass03/prime_cycle.py": (76045, "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c"),
    "labs/prime-review-pass02/prime_review.py": (58560, "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"),
    "labs/return-access-pass01/return_access.py": (26561, "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5"),
    "labs/review-construction-pass04/construct.py": (42582, "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"),
    "labs/review-loop-pass03/review_loop.py": (55474, "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b"),
    "labs/review-report-pass01/report.py": (42127, "72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc"),
    "labs/review-report-pass02/report.py": (38323, "d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e"),
    "labs/review-report-pass03/report.py": (8091, "70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade"),
    "labs/workbook-review-pass01/forms/workbook-review-v1.json": (4532, "152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f"),
    "labs/workbook-review-pass01/workbook.py": (79131, "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"),
    "labs/workbook-review-pass02/forms/workbook-review-v1.json": (4532, "66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645"),
    "labs/workbook-review-pass02/workbook.py": (52574, "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a"),
    "labs/workbook-review-pass03/forms/workbook-review-v1.json": (4532, "4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b"),
    "labs/workbook-review-pass03/workbook.py": (19533, "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c"),
}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def _load(rel: str, name: str):
    path = Path(__file__).resolve().parents[1] / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p3 = _load("review-report-pass03/report.py", "review_report_pass03_for_deployment_v1")
_PATCHED = p3.finish.__globals__
base_report = _PATCHED["base_report"]
emit = _PATCHED["emit"]
parse_args = _PATCHED["p1"].parse_args
ArgRefuse = _PATCHED["p1"].Refuse


def _linked(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def check_pins(code_root: Path) -> None:
    root = Path(code_root)
    for rel in PINS:
        want_bytes, want_sha = PINS[rel]
        if "\\" in rel or rel.startswith("/") or any(part in {"", ".", ".."} for part in rel.split("/")):
            raise Refuse("pin path escapes")
        cursor = root
        for part in rel.split("/"):
            cursor = cursor / part
            if _linked(cursor):
                raise Refuse(f"dependency conflict {rel} is linked and was not followed")
        if not cursor.is_file():
            raise Refuse(
                f"dependency conflict {rel} got missing want {want_bytes} bytes sha256 {want_sha}"
            )
        data = cursor.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if len(data) != want_bytes or got != want_sha:
            raise Refuse(
                f"dependency conflict {rel} got {len(data)} bytes sha256 {got} "
                f"want {want_bytes} bytes sha256 {want_sha}"
            )


def main(argv: list[str] | None = None) -> int:
    blank = {"book": None, "code_root": None, "pass": None, "source": None}
    try:
        options = parse_args(argv)
    except ArgRefuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(p3.finish(base_report(blank, "refused", 2)))
        return 2
    try:
        check_pins(options["code_root"])
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(p3.finish(base_report(options, "refused", 2)))
        return 2
    report = p3.finish(p3.observe(options))
    if report["exit"] == 2:
        print("refused: core stdout is not one workbook-review-result/1 object", file=sys.stderr)
    emit(report)
    return int(report["exit"])


if __name__ == "__main__":
    sys.exit(main())
