# Return — claude-0513-0502 (0513.bench-build 05.02, benchmark method controls and delivered-input checks)

Submitter: claude-opus-5-5 (Anthropic), Builder. Reviewer: Codex Prime. Date: 2026-10-29. Claim at 749cfd9c670fe77fbedd232c2630f98b0529025d; HEAD at return a8825689ab3220396841b144f3a7ebe95c9c9a66 (see Limits).

## Did
- **Pack, review and claim.**
  - pack05.02: 10 of 10 snapshots match their pins, and live equals all 10.
  - I read the full Prime review (F01–F04), probes.json, 0414.bench/01.002.md, the 0701 review and the exact 0701 return.
  - I recorded the release and the claim. Notes (06.02.md) came FIRST, then CONTRACT.md, then code.
- **F01 fixed: input drift after preparation.** Prime's probe was reproduced exactly: a hint appended to the assisted design-fork-a `sources/consumer-note.md` after preparation.
  - `check-inputs` now exits 1 with `drift: changed: sources/consumer-note.md`.
  - Collect exits 0 and keeps the raw answer, but records the drift.
  - Compare lists the run as not clean, its pair as unreadable and the trial as INCOMPLETE.
  - The check covers changed, missing, extra and linked files (symlink, junction, hard link, or `work/` itself linked).
  - Notes under `work/` are declared candidate output and do not count as drift.
  - The check runs before launch, at collection, and again at compare.
- **F02 fixed: one seal over the whole trial before any answer.** `seal` replaces `prepare`. It prepares every planned pair in one step. seal.json binds:
  - the plan (runs, pairs, cases, conditions, order, labels, capabilities, allowed differences, preparation owner, setup, amortization);
  - the investigation;
  - the bench, harness, conditions, measures and support hashes;
  - each case's key, rubric and commitments hashes;
  - every run.json and delivery manifest;
  - pair parity and baseline reach;
  - the machine clock.

  Parity holds inside a pair, byte for byte, except the declared support copies and the PROMPT.md Tools paragraph. A withheld conflicting source (0701 C01) or an edited assisted source refuses the seal and writes nothing. Variants a and b are not compared byte for byte.
  - A corrected kit is a new late identity, made by `rerun`. The original's evidence stays byte-identical, and the late run is reported but never clean.
  - Compare takes the trial folder, so every planned run appears, including missing and uncollected ones.
  - These are flagged: a tampered run.json, a declared start before the seal, and a tampered plan (refused).
- **F03 fixed: action commitments.** Each case now has an `evaluator/commitments.json` at case revision 2, with kinds required-action, hold, prohibited and no-further-edit. Each complete case has a no-further-edit item.
  - `actions` binds a supplied assessor record: present, contradicted or absent for each commitment, with the evidence quoted exactly from the response. Code checks only the shape and bindings.
  - The tests distinguish the 0701 specimens:
    - B, a correct quote followed by a contradicting action: string checks pass, quote kept, actions contradicted;
    - C, a faithful paraphrase: quote check fails, commitments present;
    - an unneeded edit on a complete case: no-further-edit contradicted.
  - String checks keep their label and are never used as semantic success. There is no universal score.
- **F04 fixed: full cost record.**
  - measures.json is sealed. It holds the operation unit, the named session start and stop events, preparation timing, and the fields and units.
  - Each run has a declared `prime-bench-costs/1` record: launch order, tool operations, failed calls, repairs, corrections, Director attention and cache state. Unknown fields stay `unknown` and mark the record incomplete.
  - Preparation comes from the plan, plus the seal's mechanical clock, with the amortization share shown.
  - Every value is labelled mechanical, declared, or supplied judgment.
  - No ratio, saving, ranking or cost conversion is computed.
- **Versions.** Rules `prime-bench-rules/2`, bench and case revision 2, run and collection schema 2. A rules-1 run is refused as `legacy-run`.
- **Tests.** `python -B -X dev labs/prime-bench-pass01/tests/test_prime_bench.py -v`: 31 tests, 0 failures, 0 skips.
  - Four mutation probes were each caught: input recheck, pair parity, seal binding, cost completeness.
  - The 05.01 suite (32 tests) exercised the removed `prepare` command, so it was rewritten rather than run; its scenarios were carried over.
- **End-to-end disposable trial** through the CLI, outside the repository: 8 sealed pairs plus 1 late rerun, 62 calls. It covered:
  - sealing, check-inputs (15 intact, 1 drift), collection, string checks and supplied actions;
  - complete, incomplete and missing costs;
  - the drifted run kept, the late rerun, a failed run, a reviewer record, a correction event, a refused wrong identity;
  - compare and export.

  The output is `sample-report.md`, with wrong answers split two per condition.
- **Docs.** The 05.02 RUN-GUIDE and the lab README are updated. Notes dispositions are recorded.

## Blocked
Nothing. No new Director choice was needed for this correction.

## Need
- Prime's review of rules 2 against 0414.bench/01.002.md.
- **Smallest next action, after acceptance:** the Director chooses models, effort, pair count, spending and a session surface that can start fresh, confined sessions, before any ACTUAL trial is sealed.
- A reserved member for that coordinator return. Its expected outputs would be `comparison.md`, `comparison.json` and `seal.json`.

## Limits
- **Hashes are not chronology.** Code cannot prove when a session started, that the seal was published first, or that a session saw nothing else. The guide asks for the seal digest to go to Prime before launch.
- Isolation, confinement, times, tool events, usage and costs are declared. Rubric scores and action dispositions are supplied judgment.
- A late run can never be clean. A clean replacement needs a new sealed trial.
- Compare rechecks the candidate folders, so they must be kept until export, or those runs are reported as drift.
- The synthetic tests and sample demonstrate the instrument only. No model performance, productivity multiple or fresh-Prime claim.
- **Not run:** any model or session; AR-01 inventory and bridge fixtures; the broad app suite; race probes; any capture of a coordinator return.
- **HEAD moved during the build** (a882568). It touches no input, dependency or output of this batch.
- **Preserved unchanged:** member 0163, build05.01 evidence and 06.01.md.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0513.bench-build/06.02.md: 21c1a70ad2c9d5f39074c9093cbfa46225bd7c704ab80334b93c4776481362fb, 12553
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/CONTRACT.md: 522832502635a6e871c12a5aae3a9d8cb4e0c3da210d2cf59b5f68fdc253d7e0, 12061
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/verification.json: e177d00172ca868dc51584ef624664198ab12d1c915892e574bec914a4cbf77d, 153068
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/RUN-GUIDE.md: 6db7dddc98a22c20bf75036a74ec71e86234f7fb1ea10b9e4596a45274efaf1c, 6793
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/artifact-manifest.json: ac4a60c8e9be8940e417a6ef8ded1d226cecb3d5ca0d0041cab3e26252f03796, 15864
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.02/sample-report.md: eba2202c865020d159dfedb320ba57e0f6c4ff006947e23008e2380459279cdd, 11174
- labs/prime-bench-pass01/prime_bench.py (not captured; bound in artifact-manifest.json): a6dc98b8b6dbcaa8e080903a3ec537381e511b2b94206b259bb5c723c0696fe3, 106951
- labs/prime-bench-pass01/tests/test_prime_bench.py (not captured): 2616b2ce2f36eb759129071c12a817964aa04414b98489591ee29e5f42449345, 48650
- labs/prime-bench-pass01/bench.json (not captured): ba17e1218eb27316d209784d51ba8e236a80967bdd6faa29b64f7161d82146db
