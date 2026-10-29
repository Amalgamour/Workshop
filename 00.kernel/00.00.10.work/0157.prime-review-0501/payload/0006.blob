# Walkthrough — pinned 0507/05.17

One committed source. Report and guard drafts only. This is not a new acceptance of the trial, not a reopening, and not a succession recommendation.
The review sentences are a SUPPLIED EXAMPLE. They are hypothetical. They are not a Director reply and not Codex Prime's acceptance.

## Source

`00.kernel/00.00.10.work/0507.prime-support/05.17.md`
sha256 `7ad45e5bafd71d04a6d1a114c88faadcb2f2e49203a488fec0007d53a6983f38`, 1304 bytes.
The record binds that path under `D:\Git\lib-build`. The tool matched the file bytes to the declared hash and length.
The page names reserved member 0153. This draft does not verify that member.

Record: `labs/prime-review-pass01/examples/walkthrough-0517.json`
Guards: `guard-read-0517.json`, `guard-appoint-0517.json`, `guard-reopen-0517.json`

## Commands

From `D:\Git\lib-build`:

```text
python -B labs/prime-review-pass01/prime_review.py report --input D:\Git\lib-build\labs\prime-review-pass01\examples\walkthrough-0517.json --root D:\Git\lib-build
```

Exit 1. Effective `hold`. `closes_work` false. Stdout sha256 `0ee3a80298ace7764242dfcbe5626e99ec60c4e83e269ab7ad248d8f35e4aadb`, 2307 bytes.

```text
python -B labs/prime-review-pass01/prime_review.py guard --input D:\Git\lib-build\labs\prime-review-pass01\examples\guard-read-0517.json --root D:\Git\lib-build
```

Exit 0. Result `independent-of-holds`. Stdout sha256 `0a99d781543a9f43f057e02c21e8f973421b46d2bdb2990fd416a87d8c166227`.

```text
python -B labs/prime-review-pass01/prime_review.py guard --input D:\Git\lib-build\labs\prime-review-pass01\examples\guard-appoint-0517.json --root D:\Git\lib-build
```

Exit 1. Result `blocked`. Stdout sha256 `672ac7c47572ddabe93fc00311f15dcd184e5c06af9852edf0ba0900a34d3d2b`.

```text
python -B labs/prime-review-pass01/prime_review.py check-next --input D:\Git\lib-build\labs\prime-review-pass01\examples\guard-reopen-0517.json --root D:\Git\lib-build
```

Exit 1. Result `blocked`. Stdout sha256 `b0610f68a6d10ffd2d7c314448508c8f5ffb92e65b863e6282109998a8a27217`.

`authorized_in_grant` true on these three guards is part of the supplied example. It is not a Director grant. Exit 0 on the read check does not release the read.

## Raw report

```text
# Prime review draft
schema: prime-review-report/1
authority: none
closes_work: false
releases_action: false
authenticates_actor: false
permission: withheld
authorizes_task: false
tasks_added: none

Supplied outcome: complete
Effective: hold
Supplied semantic_conflict: False

## Attribution
actor_label: SUPPLIED EXAMPLE
role: prime
evidence: Hypothetical review for the 05.01 walkthrough. Not a Director decision, not Prime acceptance, and not an appointment.
This module does not prove that identity.

## Prime finding
The pinned page says "Judge:not-oriented; authority none." and "Candidate is not appointed Prime." This supplied example does not appoint anyone.

## Supplied next action
Prime reviews this draft. No succession step is proposed.
This line is not a release.

## Agreed outcome evidence
Mechanical O1–O6 checks ok. O1–O5 semantic pass; O6 content sound but protocol wrong:
candidate disclosed extra shell operations forbidden by fixed evaluator(f).
Judge:not-oriented; authority none. Outside memory note also disclosed; influence
on answers unknown, no evaluator read alleged.

## Limits
Authority none. The page says the exact initial chat text was not supplied. This draft does not verify member 0153 and does not reopen the trial.

## Tests
The page records mechanical checks and a not-oriented judge line. This draft does not use those checks as closure.

## Learning
A protocol miss stays in the record.

## Preservation
Keep the pinned page bytes. This draft adds no acceptance.

## Remaining choices
Should anyone be appointed Prime from this trial, or should the trial be reopened? This supplied example is not an answer.

## Findings account
- 00.kernel/00.00.10.work/0507.prime-support/05.17.md#O6 accepted

## Finish criteria
- recorded met

## Holds
- H-0517 director-judgment status unresolved question Q-0517 r1 7ad45e5bafd71d04a6d1a114c88faadcb2f2e49203a488fec0007d53a6983f38
  scope: appoint-candidate, reopen-trial

## Sources
- page `00.kernel/00.00.10.work/0507.prime-support/05.17.md` content 7ad45e5bafd71d04a6d1a114c88faadcb2f2e49203a488fec0007d53a6983f38 transport 7ad45e5bafd71d04a6d1a114c88faadcb2f2e49203a488fec0007d53a6983f38 change unspecified

## Known gaps
Exact initial chat text and the full transcript were not supplied. They are not invented here.
```

## Raw guards

```text
# Prime review guard
schema: prime-review-guard-result/1
authority: none
releases_action: false
closes_work: false
action: read-pinned-page
result: independent-of-holds
This check does not release the action.
supplied_outcome: complete
effective: hold
other_holds:
- H-0517 unresolved
```

```text
# Prime review guard
schema: prime-review-guard-result/1
authority: none
releases_action: false
closes_work: false
action: appoint-candidate
result: blocked
This check does not release the action.
supplied_outcome: complete
effective: hold
covering:
- H-0517 unresolved
```

```text
# Prime review guard
schema: prime-review-guard-result/1
authority: none
releases_action: false
closes_work: false
action: reopen-trial
result: blocked
This check does not release the action.
supplied_outcome: complete
effective: hold
covering:
- H-0517 unresolved
```

## Before and after

Before, for this one page, the mechanical copying was five steps: open the page, copy the judge sentences, compute the sha256 and length, write the account blocks, and decide by eye which of the three actions sit in the appointment question. The quoted "Good, the prime test is done." still had to be kept from becoming a new release.

After this run, those sentences and that hash sit in one JSON record. The tool matched the 1304 bytes, rendered the supplied account, and classified the three actions. The finding text and the outcome word `complete` were supplied by the example. The tool did not decide that the judge line was right. The open question Q-0517 kept the effective result at `hold`.

That is the whole reduction observed here: one hash check, one length check, the required complete-account fields, and three action classifications. No token total is claimed. No clock was run. The 30–60 second line remains a reader target for Prime's own wording.

## Judgment that remains

Prime still has to decide whether this account is the right one, whether Q-0517 should be asked, and what a real Director reply would be. Seating PAGE-AMENDMENTS.md is a later Director choice. No caller listed in ADOPTION.md runs this guard yet.
