#!/usr/bin/env python3
"""N7 return-pointer intake compatibility (0707/05.16). NONPRODUCTION lab prototype.

Loads the PINNED selected workbook pass03 (which loads pass02 and pass01 from the live checkout,
read-only, under their own pins) and, with --patch, installs one pointer parser into the three module
namespaces where pass03 itself installs its parser (pass03 lines 493 and 498: p2.parse_pointer and
wb.parse_pointer; an earlier lab hypothesis that p2 was missed was refuted by test D2, run01). The parser
keeps every existing N5 form and adds exactly two observed N7 forms:
  Returned: PATH (ATTRIBUTION), sha256 HASH, N bytes.
  Artifact manifest: PATH, sha256 HASH, N bytes.
A path ending in , ; : ) is refused (never stripped). Attribution text is descriptive only.
--repo-root DIR points the code root at a disposable copy with the production layout (lab only;
pins are still verified against the copied bytes). No production file is changed.

usage: n7compat.py [--patch] [--repo-root DIR] <workbook command and flags>
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
V7_JSON = LIVE / "app/review-loop-v7.json"   # verified against its pack05.16 pin in load_pass03
PATH =r"([A-Za-z0-9][A-Za-z0-9._/-]*)"
RETURNED_RE = re.compile(r"^Returned: " + PATH + r" \(([^()]{1,160})\), sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
N7_MANIFEST_RE = re.compile(r"^Artifact manifest: " + PATH + r", sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
TRAILING = (",", ";", ":", ")")
SHA_ANY = re.compile(r"[0-9a-f]{64}")
LABEL_WORDS = ("Submission:", "Artifact manifest:", "Verification:", "Returned:")


def pin_of(rel: str) -> dict:
    m = json.loads((LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.16/source-manifest.json").read_text(encoding="utf-8"))
    return next(f for f in m["files"] if f["path"] == rel)


def load_pass03():
    v7 = V7_JSON.read_bytes()
    want = pin_of("app/review-loop-v7.json")
    if hashlib.sha256(v7).hexdigest() != want["sha256"]:
        raise SystemExit("refused: review-loop-v7.json differs from its pack05.16 pin")
    item = json.loads(v7)["tools"]["workbook"]
    path = LIVE / item["path"]
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != item["sha256"] or len(data) != item["bytes"]:
        raise SystemExit("refused: workbook pass03 differs from its v7 pin")
    spec = importlib.util.spec_from_file_location("workbook_review_pass03", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_parser(p3):
    p2 = p3.p2

    def parse_pointer(body):
        findings = []
        parsed = {"findings": findings, "manifest": None, "state": "absent", "submission": None, "verification": None}
        if body is None:
            findings.append({"code": "return-pointer-absent", "path": None})
            return parsed
        stripped = body.strip()
        if stripped == "":
            findings.append({"code": "return-pointer-empty", "path": None})
            parsed["state"] = "empty"
            return parsed
        if stripped == "PENDING.":
            findings.append({"code": "return-pending", "path": None})
            parsed["state"] = "pending"
            return parsed
        fields = {"Submission": None, "Artifact manifest": None, "Verification": None}
        ambiguous = set()
        for raw_line in body.split("\n"):
            line = raw_line.strip()
            if line == "" or line.startswith("Invocation/claim:"):
                continue
            # --- N7 forms (new) ---
            ret = RETURNED_RE.fullmatch(line)
            if ret:
                attribution = ret.group(2)
                if SHA_ANY.search(attribution) or any(w in attribution for w in LABEL_WORDS):
                    findings.append({"code": "attribution-not-descriptive", "path": None, "text": line[:180]})
                    continue
                p3.accept_field(fields, ambiguous, findings, "Submission", {
                    "attribution_text": attribution, "bytes": int(ret.group(4)), "declared_form": "n7-returned",
                    "path": ret.group(1), "sha256": ret.group(3)})
                continue
            man = N7_MANIFEST_RE.fullmatch(line)
            if man:
                p3.accept_field(fields, ambiguous, findings, "Artifact manifest", {
                    "bytes": int(man.group(3)), "declared_form": "n7-manifest", "path": man.group(1), "sha256": man.group(2)})
                continue
            # --- existing N5 forms (unchanged), with trailing-punctuation refusal ---
            counted = p3.COUNT_RE.fullmatch(line)
            if counted and counted.group(6) in p3.COUNT_TAILS:
                if counted.group(2).endswith(TRAILING):
                    findings.append({"code": "unrecognized-path-punctuation", "path": None, "text": line[:180]})
                    continue
                p3.accept_field(fields, ambiguous, findings, counted.group(1), {
                    "bytes": int(counted.group(4)), "file_count": int(counted.group(5)), "path": counted.group(2), "sha256": counted.group(3)})
                continue
            match = p3.FIELD_RE.fullmatch(line)
            if match and p2.suffix_ok(match.group(5)):
                if match.group(2).endswith(TRAILING):
                    findings.append({"code": "unrecognized-path-punctuation", "path": None, "text": line[:180]})
                    continue
                p3.accept_field(fields, ambiguous, findings, match.group(1), {
                    "bytes": int(match.group(4)), "path": match.group(2), "sha256": match.group(3)})
                continue
            findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
        parsed["submission"] = fields["Submission"]
        parsed["manifest"] = fields["Artifact manifest"]
        parsed["verification"] = fields["Verification"]
        parsed["state"] = "ambiguous" if ambiguous else "parsed"
        if parsed["submission"] is None and "Submission" not in ambiguous:
            findings.append({"code": "submission-not-declared", "path": None})
        return parsed

    return parse_pointer


def install(p3, patch: bool, repo_root: str | None):
    if repo_root:
        root = Path(repo_root).resolve()
        p3.wb.REPO = root
        p3.p2.REPO = root
        p3.REPO = root
    if patch:
        fn = make_parser(p3)
        p3.parse_pointer = fn
        p3.p2.parse_pointer = fn
        p3.wb.parse_pointer = fn
    return p3


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    patch = "--patch" in args
    args = [x for x in args if x != "--patch"]
    root = None
    if "--repo-root" in args:
        i = args.index("--repo-root")
        root = args[i + 1]
        del args[i:i + 2]
    p3 = install(load_pass03(), patch, root)
    return p3.main(args)


if __name__ == "__main__":
    sys.exit(main())
