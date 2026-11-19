# 2026-11-19 merge rehearsal (builder-b19)

Why a rehearsal: the merge of board-dev and harden-dev into workflow waits for the Director (questions 13-16). Doing it once now, on a throwaway branch, means the real merge is a known step when he answers: no surprise conflicts, test counts known, real pages known to load.

Why a new worktree and branch: the rules say never touch `workflow`, the pinned binary or the real pages. A new worktree (`scratch/merge-rehearsal`, branch `merge-rehearsal` from a00bc53) keeps all of that apart.

Why board-dev first, then harden-dev: that is the order they were built in (harden-dev starts on 193da07). Merging in that order mirrors the review history.

Why `--no-ff`: both merges would fast-forward. A merge commit for each keeps a mark in workflow's history of when each reviewed branch came in, so the past stays readable (axiom 6).

What happened: no conflicts. The result equals harden-dev 1f32ecb. 153 tests passed. All three real pages, as copies, verify ok with 85, 49 and 37 entries under both the merged build and the pinned binary.

Why copies: verify is read-only, but `--fix`, `status` and `board` all run on a root folder; copying the pages keeps any mistake away from the real log.

What I found that the Director or Prima should know:
1. The merge brings in "build stage" AGENTS.md lines (Q13, ax1).
2. A Q14 "still loads, out of rule" answer needs new code before or after the merge.
3. 1f32ecb is not yet Tester-checked (Q17).
4. `docs/design/WF-BOARD.md` is named in README and AGENTS.md but is not on these branches.
