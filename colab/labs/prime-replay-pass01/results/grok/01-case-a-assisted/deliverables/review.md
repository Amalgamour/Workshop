# Review — case-a assisted — Grok Colab

Model: Grok 4.7, Grok Build CLI, this session. Condition: assisted, first of four. The judgment is mine. The cycle did not store it.

## Did
- Read the projected assignment `0513.bench-build/05.01.md`, notes `06.01.md`, captured return, receipt, manifest, contract, sample report, bench README, `prime_bench.py`, the test module's setup, `0414.bench/01.002.md`, and the 0701 method return and Prime review.
- Journalled `read` with a template. It exited 1. Pass state `no-return`. Custody role none. Attention: `observation-failed: reader exit 2`.
- Ran `batch_observe` directly. Exit 2. stderr: `missing clerk_adapter.py`. The assistance tree has no `labs/prime-support-pass01/clerk_adapter.py`.
- `packet` for work `case-a` exited 0. Assembly complete. Helper verify exited 0, receipt `7efb07af0f08d3cbaf1b490e97889bb3caa601b932762fcf32820854e45f7e4f`, result complete, not approved, not accepted, not published. Artifact checks: none. Embedded sources are the return and the receipt, not the harness.
- Hashed the six captured outputs, `return.md`, `prime_bench.py`, `test_prime_bench.py`, and `bench.json`. All match the return and the capture manifest. Bench version `f00c6f29f35edd27465b2bbf5e4023323d8f028c4c6d8291ef1fe85db39fe9d1`, 12713 bytes.
- Hashed all 10 `pack05.01.002` snapshots against the pack manifest. All 10 match. None of those paths is a live file in this frozen repository, including `0414.bench/01.md`.
- `validate` exited 1. Drift is five missing support paths, including `labs/prime-review-pass01/prime_review.py`.
- `test_prime_bench.py -v` ran 0 tests. `setUpModule` raised `FileNotFoundError` for that same missing file. Process exit 5.
- Filled `out/decision-case-a.json` without editing the template binding. `record` exited 2: `observation failed: reader exit 2`. `inspect` shows no review directory contents. A later `read` repeated the same failure. `day` lists the journal and derives no finished pass.

## Blocked
- The cycle cannot record an accepted review from this registration. The reader never binds the receipt, and an accepted decision requires a bound receipt. I did not add `clerk_adapter.py` or copy support files into the repository.
- The historical "32 tests, 0 failures" claim is not reproduced here. The pinned support files are outside this frozen tree. Their pack snapshots that exist match the stated pins. The 0512 contract pin named by `SUPPORT` is not one of those 10 snapshots, so that byte is not in this tree at all.

## Need
- One later correction of the harness for the controls in `0414.bench/01.002.md` and `0701.bench-method/06.01.review.md`. That pack is not released and was not started.
- Director choices that stay open: models, effort, run count, spending, and a fresh confined session surface. AR-01 stays held.

## Verified versus claimed
- Verified by hash: notes, contract, verification.json, RUN-GUIDE, artifact manifest, sample report, return bytes `742beefbf856429ce3dfcf59e675a06f618c1b75b74f8f09b87c67dc6575198e` (6655), `prime_bench.py` `258727ee…` (68800), tests `5c125c3b…` (42700), bench.json `f00c6f29…`.
- Verified by packet helper, not by the cycle reader: member 0163 custody is complete and is not acceptance. The page's return pointer names the same receipt.
- Verified by reading code: `assess_run` is string checks (`must_mention`, `must_quote`, `must_not`, outcome label, canary). `compare_runs` refuses mixed versions and mixed investigations, keeps unclean, failed, and uncollected runs, and computes no ratio. Each comparison row includes `records` hashes. Isolation is a stored declaration.
- Claimed, not re-run: 32 tests, 3 mutation probes, 16-run CLI sample, assisted-kit smoke exit 0. The sample report text matches the return's description of balanced wrong answers (r0002 and r0010 assisted, r0005 and r0015 baseline) and identical scores on the two reviewed runs. I did not re-execute that CLI.
- Not a live file here: `0414.bench/01.md`. Snapshot `0006.blob` matches pin `d226c3b5…`, 3311 bytes. I did not open the blob. The builder said that page was the grant and that `01.002.md` was not read. I do not treat the later page as a rule the builder broke.

## Defects
- Against `01.002`, the code does not compare the bytes the two conditions actually received. Task and sources are copied from one sealed case, and `PROMPT.md` differs by the Tools paragraph. An extra or missing file after `prepare` is not a pair-level parity failure.
- Against `01.002`, a quote and an outcome label can pass while the proposed action contradicts the fork. `assess_run` does not score present, contradicted, or absent.
- Against `01.002`, nothing stops the same coordinator from preparing the second condition after seeing the first answer. Hash equality of a pin does not record that the package was sealed before any answer.
- These are missing controls named by the later method. They are not a false completion inside the original grant. The return already asks for that reconciliation.

## Unknowns
- Whether the 32 tests pass in a tree that contains the pinned support files. This tree does not.
- Tokens, provider cost, and cache. Unknown.
- I read `verification.json` through the recorded test log and the start of the CLI transcript, not every later CLI row. The file hash matches the claim, so the unread tail is the captured file.

## Disposition
Accepted. Pass finished. Goal open.

The 05.01 pass delivered the instrument its own contract describes, with custody and matching hashes. The goal "a trustworthy bounded instrument for later Prime comparisons" is not complete. `01.002` says not to claim these controls are already in the code, and this review finds they are not.

`semantic_conflict` is false. The return does not claim the later controls. It asks for them.

## Pass-finished versus goal-complete
Pass finished means this build return can be accepted as that pass. Goal complete would mean the comparison instrument already enforces the accepted method controls and this review re-ran its tests. Neither of those is true.

## Director needs
No model trial, no spending, no live-book edit, and no release of the correction from this lab. Choose the session surface only after the correction exists.

## Preservation
Keep the reader failure, the record refusal, validate drift, the 0-test error, and the packet line "not accepted". The decision file remains at `out/decision-case-a.json`. No `prime-cycle-reviews` record was written. I did not change the harness or the assistance.

## One bounded next action
One lab-only correction inside `labs/prime-bench-pass01` for delivered-byte parity, action commitments scored apart from quotes, and a seal that keeps the original run when inputs change after the first answer. See `next-pack.md`. Do not execute it here.

## Factfind
F01. `prime_bench.py` `assess_run` sets `deterministic_pass` from string checks only. A response can quote the Director sentence and still propose the change the sentence forbids, and the quote check can pass. `01.002` requires the action to be scored present, contradicted, or absent.
F02. `compare_runs` never opens the two candidate directories. `01.002` requires a manifest of the bytes delivered, with only a pre-listed interface difference allowed.
F03. `validate` in this repository exits 1 before any case logic, because `REPO / support path` is missing. The historical verification.json claim of `result: valid` was not reproduced in this fixture.

## Hostile
The failing reading is the cycle view. It says `no-return` and receipt none. The return file is on disk, its hash matches the manifest, and packet verify exited 0. Using the cycle line as proof that member 0163 is absent would be false. Using packet "assembly complete" as acceptance would also be false. The packet says not accepted.

## Overflow
The replay assistance bundle cannot `read` this registration until `clerk_adapter.py` is present. That is a limit of this lab's assistance copy. It is not a defect of the 0513 harness, and I did not repair it.

The frozen repository also drops the live support files the bench pins. A later full-tree run can still validate. This run cannot.

## Unprompted
`SUPPORT` includes `00.kernel/00.00.10.work/0512.prime-review/evidence/build05.01/CONTRACT.md`. That path is not in the 10-file pack manifest I hashed. Its bytes are not in this tree. The other four support pins are among the pack snapshots and match, but the live paths are still absent, so validate still drifts.
