# CONTRACT — prime-review-pass01

Schema of this file's subject: prime-review support for 0512.prime-review/05.01.
The module is labs/prime-review-pass01/prime_review.py. Standard library only.
This file is the builder contract for that draft. It does not seat law.

## Trusted caller

The process that writes the JSON is the trusted caller. The module reads that JSON and, when a source says bind, the named file bytes.
Actor labels, roles, and dispositions are claims inside the JSON. The module does not see a person, a login, or a signature.
It can check a supplied hash against supplied text or a bound file. It cannot prove who wrote a reply.
A model name, a user name, or the word yes is not authenticated authority.

## What it does not do

It does not reserve a member, write a receipt, project a lifecycle, or brief a lane.
It does not import or launch prime_support.py, prime_brief.py, state_projection.py, return_capture.py, or return_inspect.py.
It does not call a model, Git, a network, a queue, or the app.
It does not write a live page. The draft command writes only a new file outside the repository it is given.
It does not decide that an explanation is good, that a repair is routine, or that two designs conflict.
It does not treat an 80% continue rate as a target. A continue_rate field is an unknown key and is refused.
closes_work is always false. releases_action is always false. authenticates_actor is always false.
Exit 0 is not a release, an acceptance, or a grant.

## Identities cited, not reimplemented

- page-bytes/1: path plus content and transport hashes.
- prime-support-return/1: revision_id, and finding identity `path#ID`. When bytes_are_revision is true, revision_id must equal the content sha256. This module does not recompute the pre-Review heading cut.
- return-capture/1: member, submission_id, origin book/page/batch, receipt_sha256 or null. Null receipt means unrecorded. A receipt is not approval.
- batch-observation/1: batch_id, source_sha256 equal to the content sha256, label SYNTHETIC, SUPPLIED, or DERIVED-FROM-RETAINED-SUMMARY.
- prime-brief-input/1: brief_sha256 equal to the content sha256.
- supplied-text/1: the same three labels. No lifecycle.

state-projection/1 closure rules are not applied.

## Commands

Paths on the command line are absolute, local, and not UNC. The input file must be a regular file with link count one, not a symlink or junction.

```text
python -B labs/prime-review-pass01/prime_review.py report --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py guard --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py check-next --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py draft --input ABS --dest ABS --repo ABS --expect-sha256 HEX [--root ABS]
```

check-next is the same read-only guard as guard.
--root is required when any source has bind true. A bound file is read only after the path stays inside that root and fails the link checks. The file sha256 must equal transport_sha256, and the length must equal transport_bytes.

## Exits

- 0: a shaped continue, develop, or complete-as-supplied report with an empty attention list, or a guard result independent-of-holds. Still not a release.
- 1: a shaped hold, a not-closed complete account, missing judgment, or any other attention. The JSON or markdown is still the result.
- 2: refused input, unsafe path, digest mismatch, or an argparse error. A refusal does not guess an outcome.

A director-input report is exit 1 because the work it names is held, not because the JSON was invalid.

## Records

prime-review-record/1 keys, exactly: schema, attribution, sources, agreement, judgment, holds, answers, review_passes, gaps.

attribution keys: actor_label, role, evidence. role is prime, director, builder, model, or unknown.

sources is a list of one or more bindings. Keys exactly: kind, logical_path, content_sha256, content_bytes, transport_sha256, transport_bytes, prior_content_sha256, prior_transport_sha256, record, bind, identity.
logical_path is relative, uses forward slashes, and has no empty, `.`, or `..` segment. Drive paths and UNC paths are refused.
record is null or the substantive text. When present, its UTF-8 sha256 and byte length must equal content_sha256 and content_bytes.
prior hashes are both null or both lowercase sha256. Both null means change unspecified. Equal priors mean unchanged. Same content and different transport means transport. Different content means substantive. One null prior is refused.
bind is a boolean. transport_sha256 equals content_sha256 only when the byte lengths also match.

agreement keys: goal, scope, prime_discretion, director_required, finish_criteria, recorded_decisions.
Text fields are null or non-blank. Null means unknown and becomes attention. It is not an empty grant.
finish_criteria is null or a list of {id, text}. recorded_decisions is null or a list of {id, text, source_sha256}.

judgment keys: outcome, finding, reasons, semantic_conflict, design_fork, next_action, sections.
outcome is continue, director-input, develop, complete, or null.
semantic_conflict is true, false, or null. Null stays unknown. The module never sets it.
design_fork is null or {id, text}.
reasons is null or a list of strings.

sections keys, all required, unused values null: return_result, prime_finding, within_direction, next_bounded_action, for_model, issue, consequences, options, recommendation, question, affected, proposed_plan, exploration, assumptions, open_questions, outcome_evidence, limits, tests_note, tests_passed, learning, preservation, remaining_choices, findings_account, finish_assessments.
for_model is null or {model, prompt}.
question is null or {id, revision, content_sha256, text}.
affected is null or a list of {action_id, dependency}.
proposed_plan is null or {label, text} with label exactly proposed-plan.
tests_passed is true, false, or null.
findings_account items are {finding_id, status}. status is open, accepted, discarded, or unresolved.
finish_assessments items are {criterion_id, assessment}. assessment is met, unmet, or unknown.
finding_id matches `path#ID`.

holds items: hold_id, finding_id, kind, question_id, question_revision, question_sha256, dependent_scope.
kind is director-judgment, design-conflict, or design-fork.
dependent_scope is a list of action ids. An empty list blocks nothing. There is no status field on input. Resolution is derived from answers.

answers items: answer_id, question_id, question_revision, question_sha256, reply, provenance, disposition.
reply is kept exactly, including the word yes.
provenance uses the attribution shape.
disposition is null, brief-approval, new-detail, or unresolved.
Null disposition does not approve, including when the reply is yes.

review_passes items: pass_id, finding_id, review_record_sha256, result, prior_pass_id, tool_retry.
result is unresolved or resolved. review_record_sha256 is a sha256 or null. prior_pass_id is an id or null. tool_retry is a boolean.

gaps is a list of strings and may be empty.

Duplicate keys, unknown keys, blank prose, nonfinite numbers, bools where a count is required, lists over 24 items, text over 12000 characters, and documents over 262144 bytes are refused.

## Change of source

A substantive change is a different content hash. A transport change is the same content hash and a different transport hash.
The module does not strip whitespace to invent a content hash.
An answer can bind only to the current question id, revision, and content hash.
If that hash equals the prior content hash of a source whose change is substantive, the hold is reconciliation-required even when the reply matches the old hash.
A transport-only change does not by itself unbind a reply that matches the current content hash.

## Reports

Output schema prime-review-report/1. Default stdout is the markdown as UTF-8 with LF newlines. --json is the same record, also UTF-8 LF, and includes that markdown and its sha256. markdown_sha256 is the digest of those markdown bytes. Neither contains a clock.
Rendering copies supplied text. It does not summarize a model and it does not fill a short section with invented prose.
The 30–60 second line in the Director agreement is a reader target for Prime's own wording. This module has no word-count gate.

continue, when the agreement is known, semantic_conflict is false, the four blocks are present (return/result, Prime finding, within-direction, next bounded action), reasons and finding and next_action are present, and no unresolved hold or elevation overrides it:
the markdown ends with `## For {model}` and the supplied prompt when for_model is present. Effective is continue. Exit 0. permission is recorded-only.

director-input requires issue, consequences, at least one option, recommendation, the question, affected work, and a hold with the same question id, revision, and hash. An affected action that no hold lists is attention. Effective is hold. Exit 1.
No executable For [model] prompt is emitted. A supplied prompt is withheld and is not copied into the output. A proposed_plan is shown with its label and the line `This block is not executable.`

develop requires exploration, at least one assumption, and at least one open question. The header says authorizes_task: false. A supplied prompt is withheld. Prose in the exploration is preserved and is not turned into a job. Exit 0 when nothing else is held.

complete requires the outcome evidence, limits, tests note, learning, preservation, remaining choices, at least one finish criterion, and an account that covers every finding id used by a hold or a review pass.
complete-as-supplied also needs semantic_conflict false, every accounted finding accepted or discarded, every criterion met, and no unresolved hold. Exit 0.
Any unresolved or open finding, unmet or unknown criterion, or missing account is not-closed. Exit 1.
tests_passed true never closes work and never adds a task. tasks_added is always an empty list.
The header always says closes_work: false.

If semantic_conflict is true and no design-conflict or design-fork hold exists, the result is attention. The module does not invent the dependent scope.
If a hold exists, it overrides a continue label. The supplied outcome stays visible. The For [model] prompt is withheld.
Unknown agreement, outcome, finding, reasons, or semantic_conflict is attention. Permission stays withheld.

## Answers

A reply binds only when all of these hold: one answer matches the hold's question id, revision, and hash; the source check above does not require reconciliation; disposition is brief-approval; provenance.role is director; the reply is not empty.
The derived hold status is then reply-bound.
The bound reply does not expand the grant and does not release code. Guard result for that dependent action is not-released, exit 1.
new-detail stays open-new-detail. unresolved and null disposition stay open.
role model, prime, builder, or unknown cannot bind a Director question. The reply is kept and the hold stays open.
Two exact matches make the hold ambiguous and ask for clarification. All answers are listed.
A different hash on the same id and revision is reconciliation-required. A different revision on the same id is stale.
Changed question text is a new hash. The old reply does not follow it.

## Elevation

Countable passes for one finding are unresolved, tool_retry false, and have a review_record_sha256.
Two or more count only when the first has prior_pass_id null and each later countable pass lists the previous countable pass_id, in input order.
That sets elevate true. No page is allocated. A continue label is not left clean: the report exits 1 and withholds the prompt.
The guard does not freeze an action outside the declared hold scopes because of this flag. The flag is visible on the guard result.
Tool retries, missing review hashes, a different finding, and a broken or dangling prior are not two reviewed passes.
A broken link asks for clarification. Every pass is preserved in the attempts list.
Input order is the supplied order. The module does not sort by time or by filename.

## Guard

Input schema prime-review-guard/1 keys: schema, review, proposed_action.
proposed_action keys: action_id, label, grant_ref, authorized_in_grant.
authorized_in_grant true means the caller declares that this action is already inside a grant. The module does not read the grant text and does not re-authorize it.
null withholds permission. false is outside-declared-grant.
An action whose id is absent from every dependent_scope is independent-of-holds when authorized_in_grant is true. Other holds stay listed and do not freeze it. Exit 0. releases_action remains false.
An action inside an unresolved, stale, ambiguous, new-detail, reconciliation, or model-blocked hold is blocked. Exit 1.
An action inside a reply-bound hold is not-released. Exit 1.
A hold overrides an inconsistent continue label for the actions in its scope. Nothing in the guard starts work.

## Draft writer

draft renders the report markdown and writes those bytes only when their sha256 equals --expect-sha256.
The destination must be a new absolute file outside --repo. The parent must already exist and must not be a link.
The write is an exclusive create. A mismatch writes nothing.
If the destination already exists, including a partial file, the command refuses and leaves those bytes.
A write that fails after the exclusive create leaves the partial file. A retry refuses. The module does not delete it.
The destination cannot be a live page because it cannot sit inside the repository.

## Callers this slice does not gate

app/librarian.py commands, including prime-status, pack-check, batch-observe, capture-return, and the boot commands, do not call this module.
prime_support.py, prime_brief.py, and pack_check.py do not call it.
ADOPTION.md names the later tests. Unsupported callers are not described as already gated.
