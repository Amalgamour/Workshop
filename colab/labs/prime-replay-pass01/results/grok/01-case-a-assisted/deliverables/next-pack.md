# LAB ONLY — NOT RELEASED

Next pack for the case-a finding. This file is not a work release. Do not execute it from the replay lab. Do not stage, commit, or push.

## Problem
`labs/prime-bench-pass01` records a bounded comparison, and it does not enforce three controls that `0414.bench/01.002.md` and `0701.bench-method/06.01.review.md` already accepted. The 05.01 builder was not required to implement those pages. The instrument is still not ready for a model trial.

## Scope
One correction inside `labs/prime-bench-pass01` and its tests. No new custody engine. No model call. No session launcher. No live page write. No change to `0414.bench/01.002.md`.

## Exact sources
- `labs/prime-bench-pass01/prime_bench.py` sha256 `258727eef76693583ab0b88813c1b5afbded0009561f43c9bb61797b9d4dd650`, 68800 bytes, in this frozen tree.
- `labs/prime-bench-pass01/tests/test_prime_bench.py` sha256 `5c125c3b4cc8ff5a72838fd83f0f7d88e55903f34b558f5deece187d4ca09ec9`, 42700 bytes.
- `00.kernel/00.00.10.work/0414.bench/01.002.md` in this tree.
- `00.kernel/00.00.10.work/0701.bench-method/06.01.review.md`, findings F01, F02, F03, and F04.
- `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/CONTRACT.md`.

## Steps
1. Delivered-byte parity. At `prepare`, store the sha256 and length of every candidate file. At `compare`, for each matched case, allow only the pre-listed assisted support files and the Tools paragraph of `PROMPT.md` to differ. Any other hash or length difference marks that pair unusable for a benefit reading and keeps both runs in the report.
2. Action commitments. Extend the key with commitments about the proposed next action, each scored present, contradicted, or absent. A passing `must_quote` must not flip a contradicted commitment to pass. On a `complete` case, an unrequested change is not a better score.
3. Seal before answers. Record the seal time on the investigation. If a key, rubric, task, or candidate manifest changes after the first collection in that investigation, refuse to replace the original run. Keep the original and require a new run id.
4. Cost fields. Keep preparation owner, correction loops, Director-attention count, and cache or order when supplied. Missing values stay unavailable. Do not add a ratio.
5. Add regression cases for a withheld conflicting file, a quote that contradicts the action, a package edited after the first answer, and a blank cost field that must not become zero.

## Exclusions
- Do not run a model or spend.
- Do not execute AR-01 inventory or bridge fixtures.
- Do not copy this replay's missing `clerk_adapter.py` into the harness. That failure belongs to the replay assistance tree.
- Do not treat a green `validate` inside this frozen repository as possible until the pinned support files are actually in the tree under review. This pack does not vendor them by silently editing pins.

## Verification
- The new tests fail on the current `prime_bench.py` and pass after the correction.
- `compare` still prints no ratio, no ranking, and no token saving.
- A SYNTHETIC label still appears when any run is SYNTHETIC.
- Custody tools stay unpinned-as-modified. Their hashes stay the recorded pins.

## Return expectations
Did, Blocked, Need. Name the tests run and any test that could not run. Leave model choice, effort, run count, spending, and the session surface for the Director. No performance multiple.
