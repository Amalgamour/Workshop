#!/usr/bin/env python3
"""0707 pass01: recover the supplied judgment in a new process and compare.

usage: compare.py <run>
Reads only: the run's evidence (raw app stdout, the decision written) and the
disposable books. The recovery route is the one an operator has: the app's
`read` output names latest_review.directory and record_sha256; the record file
is opened there and checked against that hash. Nothing is written except
<run>/recovery-comparison.json.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402

PAGE_REL = "0519.desk-app/05.01.md"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def calls(out: Path) -> list[dict]:
    return [json.loads(line) for line in (out / "calls.jsonl").read_bytes().splitlines()]


def stdout_of(out: Path, case: str, label: str) -> dict:
    row = [r for r in calls(out) if r["case"] == case and r["label"] == label][-1]
    return json.loads((out / row["stdout"]).read_bytes().decode("utf-8"))


def recover_case(out: Path, book: Path, case: str, read_label: str) -> dict:
    read = stdout_of(out, case, read_label)
    latest = read["current"]["latest_review"]
    record_raw = (book / latest["directory"] / "record.json").read_bytes()
    committed = json.loads((book / latest["directory"] / "COMMITTED.json").read_bytes())
    record = json.loads(record_raw)
    page = (book / PAGE_REL).read_bytes().decode("utf-8")
    page_record = re.search(r"^record_sha256: ([0-9a-f]{64})$", page, re.M)
    support_rel = re.search(r"^support: (\S+)$", page, re.M)
    support_raw = (book / support_rel.group(1)).read_bytes() if support_rel else None
    return {
        "read": read,
        "latest": latest,
        "record_raw": record_raw,
        "record": record,
        "committed": committed,
        "page": page,
        "page_record_sha256": page_record.group(1) if page_record else None,
        "support_rel": support_rel.group(1) if support_rel else None,
        "support_raw": support_raw,
    }


def check(rows: list, name: str, ok: bool, left=None, right=None) -> None:
    rows.append({"check": name, "ok": bool(ok), "left": left, "right": right})


def main() -> int:
    name = sys.argv[1]
    out = H.EVIDENCE / "runs" / name
    books = H.BOOKS / name
    words = json.loads((H.LAB / "supplied-judgment.json").read_text(encoding="utf-8"))
    rows: list = []

    decision_raw = (out / "A-decision.json").read_bytes()
    decision = json.loads(decision_raw)
    check(rows, "A book decision.json bytes == evidence A-decision.json", (books / "A" / "decision.json").read_bytes() == decision_raw,
          sha((books / "A" / "decision.json").read_bytes()), sha(decision_raw))

    a = recover_case(out, books / "A", "A", "read")
    check(rows, "A record.json sha == read latest_review.record_sha256", sha(a["record_raw"]) == a["latest"]["record_sha256"],
          sha(a["record_raw"]), a["latest"]["record_sha256"])
    check(rows, "A COMMITTED.json names the same record", a["committed"]["record_sha256"] == a["latest"]["record_sha256"])
    rec = a["record"]["decision"]
    for key in ("attribution", "judgment", "supplied_record", "binding", "review_id"):
        check(rows, f"A recovered decision.{key} == recorded decision.{key} (canonical)", canon(rec.get(key)) == canon(decision.get(key)),
              canon(rec.get(key)), canon(decision.get(key)))
    check(rows, "A recovered attribution == supplied attribution", rec["attribution"] == words["attribution"])
    rj = words["record_judgment"]
    jj = rec["judgment"]
    for field in ("outcome", "disposition", "finding", "reasons", "semantic_conflict", "design_fork"):
        check(rows, f"A recovered judgment.{field} == supplied", jj[field] == rj[field], jj[field], rj[field])
    check(rows, "A recovered next_action.text == supplied", jj["next_action"]["text"] == rj["next_action"])
    for key, text in rj["sections_text"].items():
        check(rows, f"A recovered section {key} == supplied", jj["sections"][key] == text)
    check(rows, "A read stdout supplied_judgment is null (judgment not carried by read)", a["read"]["supplied_judgment"] is None)
    check(rows, "A page support record sha == page record_sha256", a["support_raw"] is not None and sha(a["support_raw"]) == a["page_record_sha256"],
          sha(a["support_raw"]) if a["support_raw"] else None, a["page_record_sha256"])
    check(rows, "A page support record == recorded supplied_record (canonical)",
          a["support_raw"] is not None and canon(json.loads(a["support_raw"])) == canon(decision["supplied_record"]))
    page = a["page"]
    check(rows, "A page shows supplied finding verbatim", rj["finding"] in page)
    check(rows, "A page shows every supplied reason verbatim", all(r in page for r in rj["reasons"]))
    check(rows, "A page shows every supplied section verbatim", all(t in page for t in rj["sections_text"].values()))
    check(rows, "A page shows attribution actor_label", words["attribution"]["actor_label"] in page)
    check(rows, "A page in-section states disposition (expected by an operator; observed?)", re.search(r"^disposition: ", page, re.M) is not None)
    check(rows, "A page in-section states pass_terminal (observed?)", "pass_terminal" in page)
    check(rows, "A page keeps OUTSIDE and TAIL tokens", "OUTSIDE-0707-TOKEN" in page and "TAIL-0707-TOKEN" in page)

    # source identity
    pins = H.manifest()
    m = f"00.kernel/00.00.10.work/{H.MEMBER}/"
    ret_pin, rcp_pin = pins[m + "return.md"]["sha256"], pins[m + "receipt.json"]["sha256"]
    binding = rec["binding"]
    descriptor = json.loads((books / "A" / "descriptor.json").read_bytes())
    check(rows, "binding.return_sha256 == pack pin of 0182 return.md", binding["return_sha256"] == ret_pin, binding["return_sha256"], ret_pin)
    check(rows, "binding.receipt_sha256 == pack pin of 0182 receipt.json", binding["receipt_sha256"] == rcp_pin, binding["receipt_sha256"], rcp_pin)
    check(rows, "binding.member is the derived line 0119.desk-app", binding["member"] == "0119.desk-app", binding["member"])
    check(rows, "binding.submission_id == descriptor submission_id", binding["submission_id"] == descriptor["submission_id"] == "claude-0519-0501")
    check(rows, "binding.origin == descriptor origin", binding["origin"] == descriptor["origin"], binding["origin"], descriptor["origin"])
    cap = [s for s in rec["supplied_record"]["sources"] if s["kind"] == "capture"][0]
    check(rows, "capture source content_sha256 == pack pin", cap["content_sha256"] == ret_pin)
    check(rows, "capture identity member/submission/receipt/origin", cap["identity"] == {
        "schema": "return-capture/1", "member": "0119.desk-app", "submission_id": "claude-0519-0501",
        "receipt_sha256": rcp_pin, "origin": descriptor["origin"]})
    obs = a["read"]["observation"]
    check(rows, "read observation custody_verified true (capture integrity)", obs.get("custody_verified") is True, obs.get("custody_verified"))
    check(rows, "read observation task_association not-established (separate fact)", obs.get("task_association") == "not-established", obs.get("task_association"))
    check(rows, "read flags accepted false / custody not-established / authority none",
          a["read"]["accepted"] is False and a["read"]["custody"] == "not-established" and a["read"]["authority"] == "none")
    check(rows, "copied member in book still equals pack pins after all calls", H.tree(books / "A" / H.MEMBER) == {
        k[len(m):]: v["sha256"] for k, v in pins.items() if k.startswith(m)})

    # B: interrupted render, then recover, equals A
    b = recover_case(out, books / "B", "B", "read-after-recover")
    check(rows, "B recovered decision.judgment == A recovered (canonical)", canon(b["record"]["decision"]["judgment"]) == canon(jj))
    check(rows, "B task binding == A task binding", b["latest"]["task_binding_sha256"] == a["latest"]["task_binding_sha256"])
    sec = lambda p: p.split("## Review - Codex Prime\n", 1)[1].split("## Notes\n", 1)[0]  # noqa: E731
    check(rows, "B rendered section bytes == A rendered section bytes", sec(b["page"]) == sec(a["page"]),
          sha(sec(b["page"]).encode()), sha(sec(a["page"]).encode()))

    # E: conflict; the partial holds the same section the success case rendered
    partial = sorted((books / "E" / "partial").glob("*.md"))
    check(rows, "E exactly one partial", len(partial) == 1, [p.name for p in partial])
    conflict = json.loads((books / "E" / "cycle" / "05.01-r1" / "render-conflict.json").read_bytes())
    check(rows, "E render-conflict.json names the partial", conflict.get("partial") is not None, conflict.get("partial"))
    if partial:
        ptext = partial[0].read_bytes().decode("utf-8")
        check(rows, "E partial contains the supplied finding", rj["finding"] in ptext)

    body = {
        "schema": "0707-recovery-comparison/1",
        "run": name,
        "all_ok_excluding_observation_checks": all(r["ok"] for r in rows if "(observed?)" not in r["check"] and "expected by" not in r["check"]),
        "supplied_judgment_canonical_sha256": canon(words),
        "recorded_decision_sha256": sha(decision_raw),
        "recovered_record_sha256": sha(a["record_raw"]),
        "recovered_judgment_canonical_sha256": canon(jj),
        "recorded_judgment_canonical_sha256": canon(decision["judgment"]),
        "checks": rows,
    }
    (out / "recovery-comparison.json").write_bytes(H.dump(body))
    for r in rows:
        print("OK  " if r["ok"] else "NO  ", r["check"])
    print("all_ok_excluding_observation_checks:", body["all_ok_excluding_observation_checks"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
