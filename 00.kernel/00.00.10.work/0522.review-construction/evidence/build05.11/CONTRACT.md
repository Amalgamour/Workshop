# CONTRACT - workbook review pass01
date: 2026-11-02
who: Grok-1
schema: workbook-review-contract/1
state: written before code; not revised after tests

This is the API, delta, failure, and ownership contract for 0522.review-construction/05.11. It is one operational integration. It is not a workflow engine and not a kernel rewrite.

## Reuse

Pinned and not edited:

- labs/return-access-pass01/return_access.py sha256 501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5, 26561 bytes. Commands used: lookup. Result schema return-access-result/1. accepted, approved, and published stay false. task_association stays not-established.
- labs/review-loop-pass03/review_loop.py sha256 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b, 55474 bytes. Used only for the filed cycle path below.
- labs/prime-cycle-pass03/prime_cycle.py sha256 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c, 76045 bytes. Reached only through that loop. Not called when observation cannot be complete.
- labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes. Reached only through that loop's render. Not called for a preliminary judgment.
- labs/prime-review-pass02/prime_review.py sha256 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e, 58560 bytes. report is the judgment check for a preliminary record. Exit 0 is not acceptance.
- app/review_loop_tools_v4.py and app/review-loop-v4.json stay the fixture-root door. v5 calls that module for the old commands. The fixture-root guard is not removed.
- Authoring-v2 and return-lines-v2 stay on their doors. The form declaration follows the authoring-forms field list (meaning, type, presence, owner, correction). pack_author.py is not imported and its parser is not copied.

Filed cycle path. All of these are true: return-access lookup returns a descriptor whose schema is return-line-descriptor/1 or return-line-descriptor/2, descriptor state is complete, receipt_sha256 is a hex digest, and that receipt path is an existing regular file inside the book. The workbook then writes the looked-up descriptor and a registration under the book and calls the pinned loop prepare, record, and, on publish, render. The cycle record is authoritative. The workbook journal stores its path and hashes and is not a second judgment.

Preliminary path. Any missing piece of the filed test above. The workbook does not write a receipt, a reservation, a descriptor that was not returned, or a capture identity. prime_review.report receives page-bytes/1 or supplied-text/1 sources only. The stored record says custody missing or cycle not called. operation complete is refused. closes_work, releases_action, and eligible completion stay false.

If lookup shows a complete descriptor but the loop or cycle refuses, the refusal is kept. The judgment may be stored only as operation other than complete, with cycle_committed false and publication through the constructor not attempted. A complete judgment is not kept in that case.

No parallel committed-review ledger. COMMITTED.json is written only by the cycle.

## API

Book is an absolute directory. Source is a page id, not a path. Pass is 05.NN. N5NN matches `^[0-9]5[0-9][0-9]\.[a-z0-9][a-z0-9-]*$`. N7NN matches the same with band digit 7. Any other band is exit 2 and missing contains route. No member number is accepted from the caller.

Logical paths use forward slashes and are relative to the book. N5NN assignment is `{page}/{pass}.md`. N5NN derived return is `{member}/{pass}.return.md`, member `{space}1{nn}.{subject}`. N5NN review target is the assignment page, section heading `## Review - Codex Prime` or `## Review — Codex Prime`. N7NN assignment is `{page}/{pass}.pack.md` if that file exists, otherwise `{page}/{pass}.md`. If both exist, the assignment is ambiguous and neither is chosen. N7NN return is `{page}/{pass}.return.md`. N7NN review file is `{page}/06.{tail}.review.md`. No 01NN allocation. Returns are not moved.

Instance identity is the sha256 of the canonical object `{book, source, pass}` using the absolute book path. Another directory is another instance.

Commands, all through `app/librarian.py review-loop` after v5 is selected:

- prepare --book --source --pass
- form --book --source --pass
- record --book --source --pass --intake --judgment [--successor]
- inspect --book --source --pass
- publish --book --source --pass --review
- read --book --source --pass
- recover --book --source --pass

prepare, form, and inspect are read-only. record, publish, read, and recover refuse when the book is inside D:\Git\lib-build or contains it. The current book is only prepared, formed, and inspected.

Stdout is one JSON object, indent 2, trailing newline. Schema workbook-review-result/1. Refusals print `refused:` on stderr and exit 2. A publication block after a stored judgment exits 1 and does not say completed. Exit 0 is not approval, filing, or release.

The judgment file is the intelligence answer only. Extra keys are refused. Compute rejects hashes, registration, receipt, descriptor, and review-document fields in that file. The form declaration is labs/workbook-review-pass01/forms/workbook-review-v1.json. Validation reads that declaration. Null tests_passed stays null. Omitted semantic_conflict is a missing field, not false. A missing decision is not consent.

Intake id is the sha256 of the canonical measured intake. Prime passes that id back. record writes the intake only when no intake is stored and the id matches the live measurement. A later different measurement does not replace the stored intake. The old review bytes stay. Staleness is reported.

Review id is `w` plus 16 hex characters from the judgment bytes and the intake id. Prime does not choose it. The same judgment bytes return the same id and do not write a second record. A different judgment while a current review exists refuses unless --successor names that current id. The new id is distinct. The old record is not deleted.

Director text measured from a heading `## Director - verbatim` or `## Director — verbatim` is copied into the result and is not rewritten as the model finding. A successor answer is stored as supplied. It does not close a finding, release a pack, or set closes_work.

## Publication

Compute derives the target. The authorized page diff is the review section body. Prefix and suffix, including the heading line, stay. Vacant section text is empty or `PENDING.`. Other existing section text that does not carry this store's `workbook-review-id` is a manual predecessor: publish refuses and the bytes stay. A prior review from this store may be replaced only by an explicit publish of the latest review id. The predecessor record file stays.

Writes are per file: exclusive temp file, fsync, replace. The journal status moves recorded, then pointer-pending after the rendered body is stored, then published only after the target bytes verify. A failed target write leaves pointer-pending. published is not set. The judgment record is not deleted.

The declared pointer write is the review section or the N7NN review file. Recovery does not call the judgment stale only because that write matches the stored rendered body. Any other target change, or a rendered-body change, is stale. A done label is not trusted. Recovery rehashes the record, the rendered body, and the target.

Sealed captures, submission files, receipts, and original artifact manifests are not written.

## Failure

- Unknown command, missing flag, path argument, tool override, or book inside the checkout on a write: exit 2, no review write.
- Ambiguous assignment, ambiguous return pointer, or a pointer line that is not a known form: finding, no guessed path. prepare still exits 0 when the page id and pass are valid. The form shows the finding.
- Malformed judgment: exit 2, original bytes copied under the pass `failed` directory, correction text from the declaration, no review record.
- operation complete while the filed cycle path is not available: exit 2, failed input kept, no complete record.
- Same-byte record: exit 0, same review id, no second body.
- Conflicting record without --successor: exit 2, old record unchanged.
- Source drift after a stored intake: exit 2, stored intake and reviews unchanged.
- Publish when the judgment is absent: exit 2.
- Publish when the target changed outside the review area, the section is manual, or the target write fails: exit 1 when a judgment record exists, else exit 2. The record stays. completion is false.
- Loop or prime_review pin mismatch: exit 2 before the call.
- prime_review report exit 2: the judgment is not recorded. Exit 0 or 1 from prime_review can be stored. The effective value is copied. It is not turned into acceptance.

## Ownership

Intelligence supplies finding, reasons, operation, disposition, pass terminal, goal terminal, next action, semantic conflict, design fork, findings, sections, holds, answers, review passes, and gaps.

Compute supplies intake id, review id, instance id, source rows, byte counts, digests, custody mode, destination, legal unknowns, and the journal. Compute does not supply the finding.

The cycle owns COMMITTED.json and prime-cycle-review/3 when the filed path records. The workbook owns workbook-review-record/1 for every stored judgment and the publication journal. On the filed path the workbook record points at the cycle record and recover re-reads those bytes.

Matching 0122.review-construction stays pending. This contract does not file it, allocate 0184, seat law, or activate a model.

## Delta

New lab labs/workbook-review-pass01. New door app/review_loop_tools_v5.py and app/review-loop-v5.json. librarian.py loads v5 for the review-loop command only. README documents v5 and the retained v4 fixture commands. v4 bytes stay. No return-backend upgrade, no band migration, no allocator patch.
