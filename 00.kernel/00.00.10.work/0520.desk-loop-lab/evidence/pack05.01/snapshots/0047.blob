"""Repair demonstration. Read-only. Writes only under the system temp directory."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))

import batch_observe

PAGE = """# 05 — Header demonstration
version: 001
state: draft
```
state: fenced-draft
Release: false release from a fence
Claim: false claim from a fence
```
> Release: quoted false release

## Assignment
Executor: Grok Builder 2

## Return pointer
Release: actual release
Claim: actual claim
"""

DECLARATION = """{
  "schema": "batch-review-declaration/1",
  "reviewed_member": "0191.declared-0514",
  "reviewed_receipt_sha256": "abababababababababababababababababababababababababababababababab",
  "reviewed_disposition": ["accepted"],
  "reviewer": "Codex Prime"
}
"""


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="batch-observe-demo-") as tmp:
        root = Path(tmp)
        page = root / "page.md"
        page.write_text(PAGE, encoding="utf-8")
        code, payload, error = batch_observe.execute(
            [
                "observe",
                "--supplied",
                str(page),
                "--path",
                "label/00.00.10.work/0508.return-capture/05.15.md",
                "--json",
            ]
        )
        if error or not payload:
            sys.stderr.write(error + "\n")
            return 1
        body = json.loads(payload.decode("utf-8"))
        release = body["assignment"]["release_raw"]
        claim = body["assignment"]["claim_raw"]
        state = body["document"]["header_state_raw"]
        state_lines = body["document"]["lines"]
        texts = [item["text"] for item in body["assignment"]["release_lines"]]
        texts.extend(item["text"] for item in body["assignment"]["claim_lines"])
        texts.extend(item["text"] for item in state_lines)
        if state != "state: draft" or state_lines != [{"line": 3, "text": "state: draft"}]:
            sys.stderr.write("header state was not kept\n")
            return 1
        if release != "Release: actual release" or claim != "Claim: actual claim":
            sys.stderr.write("eligible fields were not kept\n")
            return 1
        if body["assignment"]["executor_raw"] != "Executor: Grok Builder 2":
            sys.stderr.write("assignment executor was not kept\n")
            return 1
        if any("false" in text or "fenced-draft" in text for text in texts):
            sys.stderr.write("fenced or quoted field was kept\n")
            return 1
        declaration = root / "declaration.json"
        declaration.write_text(DECLARATION, encoding="utf-8")
        refused, refused_payload, refused_error = batch_observe.execute(
            [
                "observe",
                "--supplied",
                str(page),
                "--path",
                "label/00.00.10.work/0508.return-capture/05.15.md",
                "--declaration",
                str(declaration),
                "--json",
            ]
        )
        if refused != 2 or refused_payload or "Traceback" in refused_error or not refused_error:
            sys.stderr.write(refused_error + "\n")
            return 1
        sys.stdout.write(
            "\n".join(
                [
                    "titled page",
                    "fenced field ignored",
                    f"header_state_raw: {state}",
                    f"header_state_line: {state_lines[0]['line']}",
                    f"executor_raw: {body['assignment']['executor_raw']}",
                    f"release_raw: {release}",
                    f"claim_raw: {claim}",
                    f"observation_exit: {code}",
                    f"declaration_refusal: {refused_error}",
                    f"declaration_exit: {refused}",
                    "",
                ]
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
