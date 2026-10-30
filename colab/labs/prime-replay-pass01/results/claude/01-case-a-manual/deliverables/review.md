# Review — case A (0513.bench-build 05.01, member 0163), MANUAL condition

Reviewer: claude-opus-5-5, Colab run 01-case-a-manual. Prime-replay lab output: not a live review, and authorizes nothing.

**Disclosure.** I am the original Builder of this return: it names claude-opus-5-5 as submitter, so this is self-review, with author bias. I do not recall that session beyond its return. The same session later built the frozen assistance adapter. No assistance bundle was invoked in this run.

## Did, Blocked, Need
- **Did:**
  - read the projected assignment (05.01.002), the captured return 0163, the harness CONTRACT, RUN-GUIDE and keys, and the supplied method context (0414.bench 01.002, 0701 return and review);
  - verified custody by hand;
  - inspected the code paths for collect and compare;
  - attempted the historical test suite and `validate` in the disposable copy.
- **Blocked:** the historical tests cannot run in this frozen input. `setUpModule` needs `labs/prime-review-pass01/prime_review.py`, which is absent (exit 5). `validate` reports drift for all 5 support pins (exit 1).
- **Need:** one bounded correction pack that implements the accepted method controls the build lacks (next-pack.md). Nothing for the Director at this step.

## Verified versus claimed

| claim (return 0163) | status in this run | how |
|---|---|---|
| Receipt `7efb07af…` is the page pointer's | **verified** | sha256 of receipt.json equals the pointer |
| Manifest, reservation and 6 payloads bind the declared outputs | **verified** | receipt.manifest_sha256 equals the manifest; reservation sha matches; 6 blobs equal their manifest rows and the repository files byte for byte; submission.md == return.md (742beefb…) |
| 9 declared output hashes, including prime_bench.py 258727ee…, the tests 5c125c3b… and bench.json f00c6f29… | **verified** | recomputed |
| artifact-manifest binds 69 files | **verified** | 69 of 69 rows match, none missing |
| bench.json seals 59 case files and conditions.json | **verified, by the subject's own validator** | `validate --json`: the only drift is the 5 absent support files; no case file drifted |
| 32 tests, 0 failures, 0 skips; 3 mutation probes caught; 16 end-to-end runs | **claimed only: not reproducible here** | the dependency is absent, so the tests error before running (exit 5). Unknown, not false. |
| "Task and sources byte-identical across conditions; PROMPT.md differs only in its Tools paragraph" | **partly verified** | static: prepare builds both conditions from the same case files, and conditions.json differs only in `tools` and `support`. Not exercised. |
| Changed key or rubric refuses | **verified by code reading** | prepare pins them; assess raises `key-changed` |

## Assessment against the accepted method (0414.bench 01.002 and the 0701 review dispositions)

The method update landed after the Builder's claim (the return says so: 80f7025). Gaps against it are integration findings for now, not disobedience of the original grant. That is the 0701 review's own next action: "Review Claude's independently built harness against these accepted requirements."

- **F01, byte parity:** partly met. Structurally, prepare builds both conditions from the same bytes and stores per-run `candidate_files` pins. But no command compares the baseline and assisted pins for a case, and the allowed difference (the Tools paragraph plus support/) is not sealed as an explicit diff list. **Gap: there is no pair-level parity check.**
- **F02, commitment scoring:** **contradicted by the current key design.** For example, `design-fork-a/evaluator/key.json` scores `must_quote` on the exact Director sentence plus `must_mention` "exit 0" and "exit 2". That is the wording test the method rejects: a paraphrase that keeps the fork's commitments fails deterministically, and a quote alongside a contradicting action can pass the string checks. Semantic judgment exists only as a reviewer rubric score (R1–R5), not as present, contradicted or absent per commitment on the proposed action. The complete family (no-change outcome) does exist.
- **F03, seal before answers; no input revision after:** partly met.
  - **Met:** bench, key, rubric and task are pinned at prepare, and a changed key refuses.
  - **Missing:** `collect` and `compare` never re-hash the candidate folder against `run.json` `candidate_files` (grep: `candidate_files` occurs only at prepare, 669/707, and in load_run's key check, 727). A coordinator could edit an assisted candidate package after seeing the baseline answer, and compare would still mark the pair clean.
  - **Not recorded:** order and publication evidence beyond `prepared_at`.
- **F04, costs:** partly met.
  - **Met:** failed and abandoned runs are kept; corrections and interventions are events; usage is "as supplied"; reviewer_minutes and director_attention_events are per review; missing values are `unavailable`.
  - **Missing:** a preparation owner, time and repairs field; a declared operation unit; and start/stop event definitions (times are coordinator-supplied).
- **F05, AR-01:** respected. Nothing held was run.

## Defects and meaningful unknowns
1. **(control gap, F03)** There is no candidate-package re-verification at collect or compare.
2. **(control gap, F02)** Deterministic keys reward exact wording, and no commitment scoring exists.
3. **(control gap, F01)** There is no pair-level parity comparison, and no sealed allowed-difference list.
4. **(control gap, F04)** There is no preparation and repair cost record.
5. **(unknown)** Test and mutation results cannot be re-run from the frozen input.
6. **(observation)** `validate`'s support check makes the bench unusable in any copy without the support files. That is correct as a pin, but it means a portable copy needs them.

No invented defect: I found nothing against the original 05.01.002 grant itself. Its own items #02–#05 appear implemented as described, as far as reading can show.

## Disposition
- **Pass:** finished, accepted as a bounded first instrument. Custody is intact, the declared artifacts are bound, and the scope was respected (no model calls, no Git, no live pages). That holds with test reproduction unknown here.
- **Goal** ("a trustworthy bounded instrument… preserving inputs, judgments and unknown measurements"): **open.** The instrument is not yet trustworthy against the accepted method: the F01–F04 controls are partly missing, and F02 is contradicted.
- **Correction is required before any live trial,** and it is within Prime's discretion: these are corrections inside the declared design, and the method revision already requires them.
- **Director:** not needed for this correction. It is needed later for models, effort, run count, spending and the session surface (RUN-GUIDE §1, 0414 "remaining choices").

## Preservation
The return, the receipt, the original 05.01.002 page and the bench version f00c6f29 stay as they are. A correction must produce a new bench.json version and keep f00c6f29 runs distinguishable, not rewrite the old cases.

## One bounded next action
Pack one implementation correction to `labs/prime-bench-pass01` that adds:
- pair parity verification;
- candidate re-hash at collect and compare;
- a commitment-scored key format;
- preparation and repair cost fields;

each with regression cases, under a new bench version. Details are in next-pack.md.

## Factfind
- `prime_bench.py:785-860`: collect reads run.json and the response files only, and never the candidate folder.
- `prime_bench.py:1088-1160`: compare's clean reasons cover status, capabilities, isolation, shared session, intervention, leakage and identity. There is no parity or package-integrity reason.
- `cases/design-fork-a/evaluator/key.json`: `must_quote` holds the exact Director sentence.

## Hostile
The path that should break: an assisted package edited after the baseline answer, then compared. Current code calls it clean. The face I was tempted to obey as live was my own return's "32 tests, 0 failures": I could not reproduce it, and I am its author.

## Overflow
- Whether `must_quote` should stay as a separate "preservation" obligation (the method says to preserve wording separately) or be dropped is a design detail for the correction pack. It is not decided here.
- The RUN-GUIDE "balance the order" step is advice only; compare does not check order balance.

## Unprompted
- The support-pin drift makes every frozen or portable copy of the bench fail `validate`. Any Colab that freezes the bench should include its support files, or declare the drift.
