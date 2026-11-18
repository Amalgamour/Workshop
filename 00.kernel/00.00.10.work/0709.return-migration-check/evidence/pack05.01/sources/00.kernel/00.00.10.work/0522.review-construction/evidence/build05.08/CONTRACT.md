# CONTRACT — review-loop pass03 (isolated L1)
date: 2026-11-01
who: Grok-1
state: implementation contract for 0522.review-construction/05.08, written before the pass03 code change
reviewer: Codex Prime

This is the delta from frozen labs/review-loop-pass02/review_loop.py. It follows 0707 evidence/design05.03/DELTA-CONTRACT.md as corrected by 0707/06.03.review.md. It does not restate an app design and it does not select L2.

accepted is false. authority is none. custody is not-established. This builder does not commit.

## Pins this loop launches
- inspect, apply, show, and the pre-apply bind: labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes.
- record and read: labs/prime-cycle-pass03/prime_cycle.py sha256 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c, 76045 bytes. That cycle still calls constructor pass02 for its own bind. This loop does not edit that call.
- describe-legacy: the pinned return_inspect, return_placement, and return_lines modules, unchanged.
- reproduce: delegated to labs/review-loop-pass02/review_loop.py sha256 8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7, 47189 bytes. Outside L1. This command is how pass02 behaviour stays explicit. Pass03 does not reimplement it and does not send it through pass04.

A wrong pinned byte refuses in pin_set before any tool launch. ROOT stays D:\Git\lib-build. Fixture roots stay outside that checkout.

## API delta
Commands stay prepare, record, render, read, recover, run, plus the existing describe-legacy and the delegated reproduce. No new command and no new gate.

Result schema review-loop-result/2 adds:
- target on prepare, and on later commands that inspect so mechanical state can be named;
- mechanical on every result: state, blocker, route, text, target;
- supplied_next_action on every result: the supplied action_id, text, and authorized_in_grant, or null;
- committed_check on render, recover, and read.

current.next_action keeps the cycle value and its position. current.next_action_label is "supplied". Top-level next is mechanical.text. It is never supplied prose.

Refusals stay review-loop-refusal/1. D1 and R01 codes appear in rule. Stderr for a refusal starts with "refused:". A render-conflict result exits 2 and does not print "refused:".

Exits: 0 complete, 1 attention, 2 refusal or render-conflict. Flags stay accepted false, authority none, custody not-established, and the release, close, allocation, and authentication flags false.

## Record
build_envelope emits schema review-construction/2. supplied_review_state is supplied-review-state/1 with source "cycle decision judgment" and disposition, pass_terminal, goal.terminal, and outcome copied from the decision being validated.

The loop writes that object to scratch/envelope.json and passes it to the cycle. The cycle stores those bytes. scratch/envelope.json remains the same-fixture witness of what this loop asked the cycle to store. It is not an authenticated seal. The unchanged cycle also writes scratch/bind-input.json on read; that file is not the witness.

Record still hashes the target before the cycle call. An absent target refuses before the cycle runs. The decision file is left unchanged and the refusal says the cycle did not commit it. Record does not gain a veto from substantive, unsupported, or constructed review content.

## Committed checks
Before every apply, and before an already-rendered shortcut reports verified or rendered state, verify_committed reads the cycle directory named by the current cycle read. Render, recover, and read all run it. Missing or malformed record.json, COMMITTED.json, or envelope.json is a coded refusal, exit 2, with no traceback and no verified claim.

Checks, each exit 2 and no page, support, partial, or rendered-marker write:

1. record-hash. sha256(record.json) equals COMMITTED.json.record_sha256 and latest_review.record_sha256.
2. review-identity. envelope.review_identity equals the registration. record.review_id, decision.review_id, and latest_review.review_id equal `<pass>-<review_identity>`.
3. binding. decision.binding.task_binding_sha256 equals latest_review.task_binding_sha256 and, when the cycle view has one, the current view task_binding_sha256.
4. envelope-record. envelope.record equals decision.supplied_record.
5. envelope-target. envelope.target and envelope.pass equal the registration.
6. supplied-state, or the legacy result below.

R01, still before apply, and before the already-rendered shortcut:
- envelope.task.task_id and assignment_path equal the registration (task-identity);
- envelope.agreement equals the registration (agreement);
- envelope.evidence equals the registration (evidence);
- envelope.receipt equals the receipt derived from the registration and descriptor (receipt);
- the pinned pass04 bind runs on the envelope path and on the render input actually passed to apply;
- the measured binding_sha256 must equal the hash-verified decision binding and the current cycle view (source-change when the declared fields still match and the measured bytes do not).

A copy of one stored string compared with another copy of the same string is not enough. The post-apply show binding check stays. A matching task binding is not body equality and is not permission to write.

These checks are a foundation. Rewriting every anchor, including the witness and the record hash together, is outside this integrity model. No authenticated identity or approval is created.

## /1 eligibility
A genuine /1 envelope stays renderable. The basis is all of the following:

- the envelope stored in the committed cycle directory has schema review-construction/1;
- that object has no supplied_review_state key;
- checks 1 through 5 pass;
- if scratch/envelope.json exists, it is also review-construction/1 and it has no supplied_review_state key.

The reported supplied_state is then `legacy-/1-envelope: no supplied state is rendered`. Pass04 renders a /1 envelope without the supplied-state lines. This slice does not edit the cycle. Pass02 still emits /1, so a review pass02 committed remains eligible when its stored envelope and witness agree.

A review this loop records is /2. Deleting supplied_review_state, or rewriting the stored envelope to schema /1, is a downgrade when the witness is still /2 or still carries supplied state. The code is `downgrade`. It is not reported as legacy. A /2 envelope whose supplied state does not match the hash-verified decision is `supplied-state`.

If the witness is absent, a stored /1 envelope that passes checks 1 through 5 stays eligible. That covers a historical /1 directory copied without scratch. Deleting the witness and rewriting the stored envelope together is outside the model above. No cycle edit is required for this basis.

## Mechanical wording
mechanical is a function of the cycle view, the read-only inspection, and a failed committed check. It does not read supplied prose.

- awaiting-review and target pending: route record. "Supply the typed judgment, then record."
- awaiting-review and target existing-review, unsupported, or constructed-same-binding: route record-then-blocked. "Recording preserves the judgment; rendering into this target will be refused."
- awaiting-review and target absent: route none-in-this-entry. "No judgment is recorded. The target is absent, so this entry does not commit one."
- render-interrupted: committed, tokens equal, target pending. Route recover.
- render-blocked: committed, tokens equal, target existing-review or unsupported. "The judgment is retained. Rendering into this target is refused."
- target-changed-since-record: tokens differ and the page is not this binding. "The judgment is retained. The target changed after record, so this entry does not write."
- rendered-marker-missing: tokens differ and inspect reports constructed-same-binding for the committed binding. "The judgment is retained. A matching task binding is not body equality and is not permission to write. This entry does not clear the missing marker." Recover still refuses. It does not delete or invent a marker.
- existing-review-conflict: render_state conflict. "The judgment is retained. The existing review was not overwritten."
- rendered: route read. "Read the rendered review."
- committed-record-mismatch: "The committed record is not established."
- unknown-state: "The mechanical state is not established."

Absent and unknown text does not say a judgment is kept. Only a hash-verified committed record that cannot be rendered may say the judgment is retained.

## Rendering and B8
Prepare calls pass04 inspect and attaches the review-target-inspection/1 object. Inspection writes nothing. Prepare still writes trace/ through the loop. The unchanged cycle may write scratch/bind-input.json during its read. Those are not one read-only step. A pending inspection does not authorize a later write. Final token, source, record, and show checks still run.

An existing, unsupported, or same-binding target can still be recorded. Render then refuses: render-conflict (exit 2, one partial, page unchanged) or the stale write-token refusal. Recover retries the same committed render into an unchanged target. It does not overwrite a review, repair an arbitrary conflict, or clear a missing marker.

No targetless recording and no supersession. Template supersedes and recovers are not operated.

## Tests
labs/review-loop-pass03/tests/test_review_loop.py drives this loop on new disposable roots outside the checkout. It covers L1–L18 plus task-id tamper, agreement, evidence, and receipt mismatch, measured source-change, legacy downgrade, truthful absent and unknown wording, and committed checks on read and on the already-rendered shortcut. Real return_lines capture and real pass04 inspect/apply/bind are separate from a pin refusal that uses a copied module with a wrong construct digest. The v2 app test, constructor suite, cycle suite, and pass02 evidence writers are not run.
