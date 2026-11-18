# Contract — stable cycle binding and full review construction

Date: 2026-10-31. Author: Grok-2. This contract is written before the 05.03 successor code. It binds `labs/prime-cycle-pass02`, `labs/prime-review-pass02`, and `labs/review-loop-pass01`. The sealed constructor contract in `evidence/build05.02/CONTRACT.md` stays the constructor's record. A rendered review is not approval, acceptance, release, closure, seating, or custody.

## Base and delta

`labs/prime-review-pass02/prime_review.py` is a copy of `labs/prime-review-pass01/prime_review.py` at `805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0`, 58324 bytes. The only behavioral delta is `MEMBER`, from `^01[0-9]{2}\.[a-z0-9][a-z0-9.-]*$` to `^[0-9]1[0-9]{2}\.[a-z0-9][a-z0-9.-]*$`. A header names the base hash. `01NN` still matches. `00NN` and `05NN` do not. Origin checks stay exact. The tool does not judge meaning.

`labs/prime-cycle-pass02/prime_cycle.py` is a focused successor of `labs/prime-cycle-pass01/prime_cycle.py` at `19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d`, 77846 bytes. It copies the pass01 judgment terminal rules and these pass states: `awaiting-review`, `reviewed`, `review-stale`, `review-unusable`, `observation-failed`. It adds `missing`, `reserved`, `incomplete`, `conflict`, `render-pending`, and `render-conflict` as distinct states. It does not copy `packet`, `day`, or live `observe`, and it does not import pass01. It does not call `return_capture.py` or `return_inspect.py`.

`labs/review-construction-pass01/construct.py` stays `8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a`, 35956 bytes. It remains pinned to pass01 `prime_review.py`. This pack does not edit it and does not point it at pass02.

## Commands

From `D:\Git\lib-build`:

```text
python -B labs/prime-cycle-pass02/prime_cycle.py read --fixture-root ABS --registration REL
python -B labs/prime-cycle-pass02/prime_cycle.py record --fixture-root ABS --registration REL --decision REL --envelope REL
python -B labs/prime-cycle-pass02/prime_cycle.py inspect --fixture-root ABS --registration REL
python -B labs/review-loop-pass01/review_loop.py prepare --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py record --fixture-root ABS --request REL --decision REL
python -B labs/review-loop-pass01/review_loop.py render --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py read --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py recover --fixture-root ABS --request REL
python -B labs/review-loop-pass01/review_loop.py run --fixture-root ABS --request REL --decision REL
```

The fixture root is an absolute directory outside `D:\Git\lib-build` and must not contain that checkout. Logical paths use forward slashes and stay inside the fixture. Exit 0 completes a mechanical step. Exit 1 means the judgment was kept and the step is not full success, including a pass02 report exit 1 and a render that is still pending. Exit 2 refuses, with stderr starting `refused:`. Stdout is one JSON object for both success and refusal. No command writes the live work book.

`run` reads, records, and renders in that order. A record refusal does not render. `full_success` is true only when the requested mechanical step finished. It is not acceptance. Every result sets `custody` to `not-established`, `allocated` to false, and `closes_work`, `releases_action`, and `authenticates_actor` to false.

## Registration and descriptor

Registration schema `prime-cycle-registration/2` has exact keys `schema`, `book`, `work_id`, `source_kind`, `page_id`, `pass`, `kernel_page`, `target`, `descriptor_path`, `agreement`, `task_id`, `assignment_path`, `evidence`, `submission_id`, `receipt_label`, `review_identity`, `review_location`, `goal`, `bounds`. `book` is `00.00.10.work`. `source_kind` is `N5NN` or `N7NN`. `pass` is `05.` plus two digits. `goal` has exact keys `goal_id`, `statement`, `terminal`, `evidence`. The goal digest is the SHA-256 of the UTF-8 goal statement. `bounds.max_output_bytes` is a positive integer. `agreement` uses the constructor agreement keys. Evidence rows use `label` and `logical_path`.

The request schema `review-loop-request/1` has exact keys `schema` and `registration_path`.

Descriptor schema `return-line-descriptor/1` has the seam's exact keys: `schema`, `origin`, `route`, `target_page`, `return_path`, `custody_path`, `receipt_path`, `manifest_path`, `submission_id`, `custody_format`, `receipt_sha256`, `return_sha256`, `return_bytes`, `state`, `verification`. `origin` has exact `book`, `page`, `batch`. `verification` has exact `tool_path`, `tool_sha256`, `result`, `evidence_path`. `route` is `matched-workflow-return-line` or `page-local-colab`. `state` is `complete`, `reserved`, `incomplete`, or `conflict`. `custody_format` is `return-line-capture/1` or `legacy-relocated/1`.

`return-line-capture/1` in this lane means the file at `receipt_path` is caller-supplied bytes. The lane records the SHA-256 and the length. It does not parse those bytes as a live return-capture receipt and it does not allocate a member directory. The typed identity inside a supplied record remains schema `return-capture/1` with keys `schema`, `member`, `submission_id`, `receipt_sha256`, and `origin`. That name is the existing report identity. It is not a relabel of sealed capture metadata.

`legacy-relocated/1` keeps the stated `target_page`, requires `verification.evidence_path` to be a regular file, and moves nothing.

Derived address, from `page_id` `{N}5{NN}.{subject}` or `{N}7{NN}.{subject}`:

- N5NN member is `{N}1{NN}.{subject}`. Route must be `matched-workflow-return-line`. Destination is `{page_id}/{pass}.md`.
- N7NN member is null. Route must be `page-local-colab`. Destination is `{page_id}/06.{tail}.review.md`.

`origin.book`, `origin.page`, and `origin.batch` must equal `00.00.10.work`, the registration page id, and the pass. `target_page` must equal the derived destination. The registration `target` must equal that same destination. A wrong registration target refuses with `target is not the derived review destination` before a review directory is created. A descriptor that is readable but has the wrong origin, route, or `target_page` is `conflict`, with the reason kept. It is not `observation-failed`.

A stated `complete` is rechecked. Receipt, return, manifest, custody, and verification-evidence paths must be regular files. `receipt_sha256` must equal the receipt bytes. `return_sha256` and `return_bytes` must equal the return file. A disagreement is `conflict`. The stated `complete` is not authority. `verification.result` is an observed check, not authentication.

`missing` means the descriptor path is declared and the file is absent. Hashes and lengths are null. `reserved` means state `reserved`. It is not a no-return. Absent reserved bytes stay null. `incomplete` means state `incomplete`. `observation-failed` means the descriptor is unreadable, torn JSON, or not a regular file. It is never a no-return. These states do not collapse into one custody state.

## Binding, write token, and old records

The task digest is the constructor `bind` result. Schema of the preimage stays `review-task-binding/2`. This cycle does not reimplement that hash. `bind` is used because it does not call `prime_review` and does not read the review home.

Decision schema `prime-cycle-decision/3` has exact keys `schema`, `review_id`, `supersedes`, `recovers`, `binding`, `attribution`, `judgment`, `supplied_record`. The read template sets `supplied_record` to null and leaves the judgment shell empty. Prime supplies both the judgment and the `prime-review-record/1` record. Compute does not invent a disposition from the report.

Binding schema `prime-cycle-binding/3` stores `task_binding_sha256`, origin, member, receipt and return and manifest identities, agreement digest, goal, direction, `expected_prior`, and a separate `write_token`. The fingerprint is the SHA-256 of the canonical binding with `write_token` and `fingerprint` removed. Direction schema stays `prime-cycle-direction/1` and uses the pass01 direction fields. The write token is schema `review-write-token/1`: the review-home path, its SHA-256, and its length. It is not inside the fingerprint.

A `/3` review is current when the fresh fingerprint matches and observation is complete. Rendering changes the write token and leaves the fingerprint unchanged, so the review stays `reviewed` after a finished render. Changing the task, the assignment path, the assignment bytes, an evidence file, the agreement, the receipt, the return, the manifest, the source page, or the pass changes the fingerprint. The old review becomes `review-stale` and historical. It is not rebound to the new work. A later record that still carries the old fingerprint refuses with `task binding changed since read` when that digest differs, `direction changed since read` when only the direction differs, `goal changed since read` when the goal digest differs, and `source changed since read` for the other fingerprint fields. A write token that differs from the template refuses with `write token changed since read` and does not discard the committed review.

Record schema `prime-cycle-review/3` is the committed object. `/1` and `/2` remain readable. A `/1` head is `review-unusable` with reason `legacy-binding`, historical, and never current. A `/2` head uses the historical whole-page rule: current only when its stored page hash equals the current write token and its stored member, receipt, submission, origin, and direction still match. It is not upgraded and it is not rehashed as `review-task-binding/2`. A page-hash change makes that `/2` review `review-stale` and historical.

The judgment object uses the pass01 `JUDGMENT_KEYS`. Outcome `complete` if and only if `goal.terminal` is `completed`. `held` and `correction-required` keep the pass and the goal open. `director-input` requires disposition `held`. The goal must name the registration's current `goal_id` and goal digest. The supplied record's outcome, finding, reasons, sections, semantic conflict, and next-action text must equal the decision judgment. A mismatch refuses with `supplied record does not match the judgment` before a review directory is created. Source hashes inside the supplied record must equal the measured files. A mismatch refuses with `supplied record does not match the measured bytes` before commit. That refusal is not `render-pending`.

Record calls pass02 `prime_review.py report`. Exit 0 or 1 commits. Exit 2 refuses and writes nothing. Exit 1 remains a recorded report, not approval. The same decision bytes are an idempotent replay. The same `review_id` with different bytes is a conflict: the first record stays, and the rule is `conflict: a different review is already committed under this review_id`. A partial directory is never read as a review. Recovery of a partial uses a new `review_id` with `recovers`. Nothing deletes a partial.

Commit order inside `{review_location}/{review_id}/` is `record.json`, `REVIEW.md`, `envelope.json`, then `COMMITTED.json`. The marker hashes `record.json` and `REVIEW.md` only. `envelope.json` is the constructor input and does not affect the marker. `rendered.json` is absent until the loop finishes a render.

## Render and recovery

The loop renders by calling the unchanged constructor `apply`. The 0-space destination is the N5NN review home. N7NN renders on its own `06.NN.review.md`. The constructor preserves bytes outside the review section and preserves a substantive section that differs.

`rendered.json` uses schema `review-loop-rendered/1` and is written only after `apply` exits 0 and a reread of the review home matches the constructor's reported hash. The loop then checks `show`. The section's `task_binding` line must equal the committed digest.

If commit succeeds and render does not, the result is `render-pending` or `render-conflict`, `full_success` is false, and the judgment stays. A nonzero N5NN is the explicit compatibility limit: pass02 accepts the derived member, the constructor still refuses `bad member` because it pins pass01, nothing is written on the page, and the next correction says a constructor successor must pin `labs/prime-review-pass02/prime_review.py` before a nonzero page can render. Recovery retries that render and still refuses. This pack does not retarget the constructor.

Recovery is idempotent:

- A `rendered.json` whose target hash matches the review home, and whose `show` binding matches, is `already-rendered`. `apply` is not called again.
- A committed review, no `rendered.json`, a pending section, and a review home that still equals the stored write token retries `apply` with the current expect hash.
- A committed review whose section is already substantive conflicts. The constructor saves one partial and does not overwrite the section. The loop records `render-conflict.json`. A second recovery returns that conflict and does not call `apply` again.
- A review home that matches neither the stored write token nor `rendered.json` refuses with `write token changed since read` and keeps the record.

A new process is a new Python process. Its `read` returns the supplied next-action text and the supplied questions. Questions come from `judgment.unresolved` and from `sections.question.text` when that section is present. Director replies come from the supplied answers and remain in the rendered section. Source wording is not rewritten.

## Trace, app pin, and evidence

Each loop command appends one `review-loop-trace/1` object to `{fixture}/trace/trace.jsonl` and writes the same object under `{fixture}/trace/`. A refusal uses schema `review-loop-refusal/1` and names `rule`, `contract`, `request_sha256`, `observation`, `supplied_judgment`, `current`, `historical`, `preserved`, and `next`. A completed step uses schema `review-loop-result/1` and names the request, the measured pins, this contract, the observation, the supplied judgment, current versus historical state, and the next step. Input and partial files stay. A format failure is not reported as a semantic disagreement.

`app/review-loop.json` is a new declaration, schema `review-loop-pins/1`. It is not `librarian-prime-review` and it is not loaded by `librarian.py`. `app/review_loop_tools.py` checks that declaration, refuses a linked path, a drifted pin, a caller tool override, and draft, dest, capture, or reserve flags. The declaration is not seating and not adoption. `integration-patch.md` names the later single-owner registration and is not applied.

The suite writes only under `evidence/build05.03/`. It publishes one synthetic `return-line-descriptor/1` fixture and the raw command evidence. The 0-space loop is the success demonstration. Nonzero coverage is the compatibility limit above, plus a direct pass02 report that accepts `1199` and a direct pass01 report that still refuses it. Historical `/1` and `/2` records are planted in their own fixtures.

AR-01 stays held. No old allocator, no `0184`, and no invented receipt.
