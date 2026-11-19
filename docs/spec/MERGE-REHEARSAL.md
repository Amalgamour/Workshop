# Merge rehearsal: board-dev + harden-dev into workflow

Build stage. Rehearsal only, on local branch `merge-rehearsal`. Nothing is merged into `workflow` and nothing is pushed. The real merge waits for the Director's answers to questions 13-16 (docs/review/QUESTIONS-2026-11-19.md on prima/build).

## What was merged
- Base: `workflow` at a00bc53.
- Merge 1: board-dev at 193da07 (`wf board`, log order check on load). Merge commit 2a91b92.
- Merge 2: harden-dev at 1f32ecb (order check before each write, refusals instead of panics, escapes). Merge commit 6bd4b17.
- Both merges use `--no-ff`, so `workflow` history shows where each branch came in.

## Result
- No conflicts. Both branches start from a00bc53 and harden-dev already holds 193da07, so git joined them without help.
- The merged tree is the same as harden-dev 1f32ecb, byte for byte (`git diff 1f32ecb 6bd4b17` is empty).
- Build: `cargo build --release` with `CARGO_TARGET_DIR=/workspace/workshop-build/target-builder`, clean.
- Tests: 43 unit + 110 e2e (tests/wf.rs), 153 passed, 0 failed.
- Real pages, copied to `scratch/rehearsal-pages/pages`, verify ok with the merged build:
  - 90.10.00.0001: 85 entries, head 219741ed8c3c
  - 90.20.00.0001: 49 entries, head 75421f543de4
  - 90.30.00.0001: 37 entries, head 9cb6b7f55d73
- The pinned `wf-bin/wf` (a00bc53) gives the same three results on the copies. `status` and `board` also load all three copies (exit 0), so the new order check passes on every real page.
- Real pages, `wf-bin/wf` and the `workflow` branch were not changed (a sha256 of every real page file matched before and after).

## Open before the real merge
- Q13 / ax1: the AGENTS.md and README lines for `wf board` and the order rules are marked "build stage". Tester asked that those lines not go into workflow's AGENTS.md without a ruling (question 8). The merge brings them in as they are.
- Q14: if the Director picks the proposed answer (a page with an old out-of-order entry still loads, shows "out of rule at entry N", and allows only resume or a Prime note), that is new code. The merge would then wait for it, or take it as a follow-up.
- Q17: 1f32ecb (one-line observe escape) has its own test but no Tester check yet.
- README and AGENTS.md name `docs/design/WF-BOARD.md`. That file is on prima/build, not in this tree. Copy it in with the merge or the link points nowhere.
