#!/usr/bin/env python3
"""Workbook review pass05: malformed recognized N7 declarations block the intake (0522/05.15).

A thin successor of the pinned pass04. Pass04, pass03, pass02, and pass01 stay byte-identical.
- The pointer grammar is chosen by the source kind intake already measures, held for build_intake and reset afterwards.
- N5NN, or no kind context: the pass03 parser object captured by pass04, unchanged.
- N7NN: the accepted pass04 forms. A recognized label that is not one of those forms blocks the whole pointer.
- An Artifact manifest line that uses the N7 delimiter ", sha256 " is accepted only as the exact N7 manifest form.
- A block clears every field from that pointer and, after the inner intake, sets measurement incomplete.
Installed into the same namespaces where pass04 installs parse_pointer and build_intake.
This file refuses to run from any root other than D:\\Git\\lib-build.
"""

from __future__ import annotations

import contextvars
import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
HERE_ROOT = Path(__file__).resolve().parents[2]
PASS04_REL = "labs/workbook-review-pass04/workbook.py"
PASS04_SHA = "b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2"
PASS04_BYTES = 6508

LABEL_WORDS = ("Submission:", "Artifact manifest:", "Verification:", "Returned:")
KIND = contextvars.ContextVar("pass05_source_kind", default=None)
BLOCKED = contextvars.ContextVar("pass05_n7_blocked", default=False)


def load_pass04():
    if os.path.normcase(str(HERE_ROOT)) != os.path.normcase(str(REPO)):
        print("refused: workbook pass05 is not at its canonical root", file=sys.stderr)
        raise SystemExit(2)
    path = REPO / PASS04_REL
    data = path.read_bytes()
    if len(data) != PASS04_BYTES or hashlib.sha256(data).hexdigest() != PASS04_SHA:
        print("refused: pass04 workbook pin mismatch", file=sys.stderr)
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location("workbook_review_pass04", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p4 = load_pass04()
p3 = p4.p3
PASS03_PARSE = p4.PASS03_PARSE
PASS04_BUILD = p4.build_intake


def _malformed(findings, line, prior):
    if prior is not None:
        findings.append(prior)
    findings.append({"code": "malformed-n7-declaration", "path": None, "text": line[:180]})


def _unparsed(line):
    return {"code": "unparsed-return-line", "path": None, "text": line[:180]}


def parse_n7(body):
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
    blocked = False
    for raw_line in body.split("\n"):
        line = raw_line.strip()
        if line == "" or line.startswith("Invocation/claim:"):
            continue
        ret = p4.RETURNED_RE.fullmatch(line)
        if ret:
            attribution = ret.group(2)
            if p4.SHA_ANY.search(attribution) or any(word in attribution for word in LABEL_WORDS):
                _malformed(findings, line, {"code": "attribution-not-descriptive", "path": None, "text": line[:180]})
                blocked = True
                continue
            p3.accept_field(fields, ambiguous, findings, "Submission", {
                "attribution_text": attribution, "bytes": int(ret.group(4)), "declared_form": "n7-returned",
                "path": ret.group(1), "sha256": ret.group(3)})
            continue
        man = p4.N7_MANIFEST_RE.fullmatch(line)
        if man:
            p3.accept_field(fields, ambiguous, findings, "Artifact manifest", {
                "bytes": int(man.group(3)), "declared_form": "n7-manifest", "path": man.group(1), "sha256": man.group(2)})
            continue
        recognized = line.startswith(LABEL_WORDS)
        if line.startswith("Artifact manifest:") and ", sha256 " in line:
            _malformed(findings, line, _unparsed(line))
            blocked = True
            continue
        counted = p3.COUNT_RE.fullmatch(line)
        if counted and counted.group(6) in p3.COUNT_TAILS:
            p3.accept_field(fields, ambiguous, findings, counted.group(1), {
                "bytes": int(counted.group(4)), "file_count": int(counted.group(5)), "path": counted.group(2), "sha256": counted.group(3)})
            continue
        match = p3.FIELD_RE.fullmatch(line)
        if match and p3.p2.suffix_ok(match.group(5)):
            p3.accept_field(fields, ambiguous, findings, match.group(1), {
                "bytes": int(match.group(4)), "path": match.group(2), "sha256": match.group(3)})
            continue
        if recognized:
            _malformed(findings, line, _unparsed(line))
            blocked = True
            continue
        findings.append(_unparsed(line))
    if blocked:
        fields["Submission"] = None
        fields["Artifact manifest"] = None
        fields["Verification"] = None
    parsed["submission"] = fields["Submission"]
    parsed["manifest"] = fields["Artifact manifest"]
    parsed["verification"] = fields["Verification"]
    if blocked:
        parsed["state"] = "blocked"
    else:
        parsed["state"] = "ambiguous" if ambiguous else "parsed"
        if parsed["submission"] is None and "Submission" not in ambiguous:
            findings.append({"code": "submission-not-declared", "path": None})
    return parsed


def parse_pointer(body):
    return parse_n7(body) if KIND.get() == "N7NN" else PASS03_PARSE(body)


def build_intake(book, source, pass_id):
    kind = p3.wb.address_of(source, pass_id).get("kind")
    token = KIND.set(kind)
    blocked_token = BLOCKED.set(False)
    try:
        intake = PASS04_BUILD(book, source, pass_id)
        blocked = kind == "N7NN" and any(
            isinstance(item, dict) and item.get("code") == "malformed-n7-declaration"
            for item in intake.get("findings") or []
        )
        if blocked:
            BLOCKED.set(True)
            intake["measurement"] = "incomplete"
            p3.rehash(intake)
        return intake
    finally:
        KIND.reset(token)
        BLOCKED.reset(blocked_token)


for _ns in (p4, p3, p3.p2, p3.wb):
    _ns.parse_pointer = parse_pointer
    _ns.build_intake = build_intake


def main(argv=None) -> int:
    return p4.main(argv)


if __name__ == "__main__":
    sys.exit(main())
