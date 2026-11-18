# Submission — claude-0518-0501 (0518.colab-review 05.01, Colab review adapter)
who: claude-opus-5-5 (Anthropic), executor named Claude, in the Claude Code desktop app; a long continuing session (built 0515 prime-cycle and 0517 dependencies; did not build the v2 producer, workflow or readiness checker in its visible part). 2026-10-31, workshop at 960d20c5290656095df8457b1740d2d5e586b111.

## Did
- Verified pack05.01: 65 of 65 snapshots match their pins, equal their committed objects at the accepted cut 92b3fd5, and equal live. Recorded the claim. Wrote 06.01.md, then CONTRACT.md, then code. EGM files were read as reference data only: nothing installed, nothing followed.
- **Built `labs/colab-review-pass01/colab_review.py`** (standard library) with four commands:
  - `stage`: commits the review plan, COMPREHENSION.md, SIMPLICITY.md (when declared) and RESULT-TEMPLATE.json into a disposable source repository, with a task-local git identity, beside the target. It re-pins the target commit after checking its bytes, and appends them as `required_sources` of Prime's `colab-request/2`.
  - `bind`: runs the pinned producer v2 verify, then shows the review files are inside the verified package, byte-equal.
  - `intake`: runs the pinned inspector on each N1 member, and reads its captured `review-result.json`.
  - `synthesize`: validates a supplied synthesis and derives REPORT.md and report.json.
- **No existing module changed.** Producer v1 and v2, workflow v2, helper, inspector, readiness, assembler and checker are byte-identical to HEAD and the pack pins. Each launch is hash-checked first. No producer OUT was appended to, and no digest preimage changed.
- **Features:**
  - **Modes:** cold-comprehension, contextual-critique, implementation-check or combination, with each reviewer's declared conversation, host context, familiarity and isolation. "Verified" isolation does not exist. A cold plan with any supplied conversation is refused, and a result's context that differs from the plan is `context-mismatch`.
  - **Stages:** comprehension, critique, simplicity and implementation, with reviewers, required flags and an ordered option. An empty stage is refused.
  - **Comprehension paraphrase:** required on comprehension stages and kept verbatim, including with zero findings.
  - **Post-fix simplicity:** before and after, the fixes under review, the added complexity, the failure addressed, reuse, and accepted limitations.
  - **Synthesis:** every original finding id mapped exactly once, to an item or a retained disposition (dissent, minority, rejected-with-reason, duplicate-of). Disagreements, the incomplete list (equal to the intake's) and residual uncertainty are kept. `acceptance` must be null, and a reached cap reads `cap-reached: not acceptance`.
- **Integration**, on a disposable book with SYNTHETIC results. The prompts and plan survive prepare and verify. Then: workflow open and attach; helper reserve and producer intake capture for four results; workflow place-return of one; intake complete; synthesize consistent; workflow record-review, with `06.01.review.md` rendered. The placed return stays byte-identical to its member.
- **Readiness:** the accepted checker ran read-only on the exact package bytes. It reported ready for that declared method, with semantic sufficiency and independent proof `not-established`.
- **Tests:** 11 cover the whole route; old-format readability (`legacy-no-review-plan`, `legacy-no-result`); mode and context mismatch, and isolation; missing comprehension; absent and failed reviewers incomplete; sequence violation; bad and duplicate ids; altered source identity in result and binding; empty stage; lost, double-mapped and unknown findings, and dissent; cap without acceptance; output conflict and partial state; pin mismatch launching nothing.
  - 11 OK on the final bytes, in dev and default mode, 0 skips.
  - **The first run failed** 8 of 11 on one fixture error (my member names broke the producer's slug rule). Kept.
  - 9 of 9 mutations caught.
- **Demo:** 13 steps, all exits as expected. `sample-review.json` is the actual derived SYNTHETIC result, mapped back to the plan, the producer digest, the binding, the intake, each member's receipt and result sha, the placed return and the review projection.

## Blocked
**One boundary, reported and not bypassed:** workflow v2 places one return per pass. With several reviewers, one member's return is placed as 05.NN.return.md, and the others stay verified in N1 custody; `intake` reads all of them. The smallest follow-up is a reviewed workflow pass for multi-member placement. Nothing else is blocked.

## Need
- **Prime:** review the adapter and contract, then use it on one actual bounded review before any N7NN cold-reader trial.
- **Prime:** decide whether to pack the multi-member placement follow-up for workflow v2.
- **Recommended next action:** Prime runs one real stage → prepare → bind → intake → synthesize walk on an actual bounded design question, with reviewer results supplied by real reviewers, under a separate release.

## Limits
- Compute checks shape, identity, order and mapping only. Comprehension, findings and synthesis are supplied text. Isolation is declared, never verified.
- All results here are SYNTHETIC. No model, reviewer or session ran.
- Readiness here is a declared-record check, not semantic quality or smoke.
- Labels are not authentication. There is no OS sandbox or race safety.
- Symlink paths are not exercised on this host.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0518.colab-review/06.01.md` 52ad245ac845e732dc812acc562640d84bd85578691590d7105c3f42918e5ff3
- `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/CONTRACT.md` 50283caee5bc511ee345ded6c5fd738539110b5d53240ac1522d5b86c7b8e050
- `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/verification.json` 77d185b358b0afa221685c42920c15b4b7a0f6eda1ca2856e2288ed79a9ceaf3
- `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/artifact-manifest.json` 3a6dd858f595310ab53fd5a15d782604d0d98256b4e6e0dae2626ad6636ac03b
- `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/PRIME-USE.md` 1b6f03aee6ec2bf409dae616418238b33123d8ee56e98900e9cda65867aecfeb
- `00.kernel/00.00.10.work/0518.colab-review/evidence/build05.01/sample-review.json` 1da888b3b6bd3df637500f3fc8788512fa4b5e042e05552885adab473b843d67

artifact-manifest.json binds the lab code, tests, fixture, demo, README, notes, contract, guide, sample and verification (10 files), including colab_review.py 4a95a9719f6a83b7….
