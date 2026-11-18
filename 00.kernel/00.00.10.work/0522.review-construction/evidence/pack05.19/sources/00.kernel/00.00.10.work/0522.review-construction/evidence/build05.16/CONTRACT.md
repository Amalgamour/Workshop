# Contract — N5 current applicability

The identity rule was written in `00.kernel/00.00.10.work/0522.review-construction/06.34.md` before `labs/review-instance-binding-pass01/workbook.py`. The rule section was not revised after that write. The Result section was appended after the suite exited 0.

A stored N5 review is current only when the stored book resolves, by the existing `book_dir` rules, to the live book string, the live intake book equals that string, and the stored `instance_id` equals sha256 of canonical `{"book": that string, "pass": live pass, "source": live page}`.

Otherwise current applicability is held. Reasons are `different-root`, `identifier-disagreement`, `relocation-or-clone`, and `unbound`. The stored judgment stays readable. The successor does not rebind, does not add a registry, and does not treat equal row hashes as the same current instance.

Same-instance N5 checks and every non-N5 check stay on the predecessor `source_changed`. N7 strict parsing stays pass05. This layer does not add `n1-not-applicable`.

form does not carry `instance_applicability`. prepare, inspect, read, recover, publish, and the record repin guard do.
