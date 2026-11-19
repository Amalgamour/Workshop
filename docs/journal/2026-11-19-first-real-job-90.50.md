# Dev journal: the first real job over GitHub (page 90.50.00.0001)

date: Thu 19 Nov 2026, about 1:00-1:15 PM EST. written by: Prima builder-b21.
Why: t400u-t402u (WF over GitHub, minimum loop first); t407u (Matthew's PC is set up; `wf` opens Windows Fax there, `wf.exe` works).

## Run folder on the box
- /workspace/workshop-build/wf-run-gh: clone of `packs` (Amalgamour/Workshop), with work/ = clone of `returns`. Identity Prima <prima@local> in both, as in the publish repo; credentials through the box's gh credential helper (no token in any URL).
- wf binary: /workspace/workshop-build/wf-bin/wf-3daaa48, built from wf-functional 3daaa48 (sha256 d110772b85d2c698...). The pinned wf-bin/wf is untouched.

## The page address: 90.50.00.0001
- The wf tool's own work pages use the 90 band, one desk per step of wf: 90.10 (write once), 90.20, 90.30 (wf ready for next week).
- 90.40.00.0001-0004 are reserved for the handoff trial (docs/design/HANDOFF-TRIAL-01.md), planned only.
- So the next free desk is 90.50, page 0001: "wf: builder prompt says wf.exe", the first job run over GitHub.
- Grant: src/, tests/, templates/ (t407u).

## The job (05.01)
- Start: origin/wf-functional (3daaa486), the only code with BUILDER-PROMPT. The return merges wf-functional into returns.
- w01: templates/v3/builder.txt says wf.exe on every wf command line (not `cargo install ... wf`, which names the crate).
- w02: tests/wf.rs test t401u_pack_on_the_shared_branch_prints_one_builder_prompt expects wf.exe.
- may touch: templates/v3/builder.txt, tests/wf.rs. checks: `cargo test --test wf builder_prompt` (run by the checker on the box).
- Why that check: tests/wf.rs does not compile on Windows yet (it imports std::os::unix for symlink tests), so no `cargo test --test wf` filter runs there. The builder runs `cargo build` on Windows and says so; the checker runs the test on the box. Making tests/wf.rs compile on Windows is a follow-up.

## What happened
1. A first pack was made, then set aside before publishing (moved, not deleted, to scratch/wf-run-gh-set-aside/90.50.00.0001-pack1-unpublished): its stop-if would have stopped the builder on Windows, because the check cannot compile there. The page was started again with the Windows note in face 06 and the job.
2. Packed with `--branch returns`, verified (AGENTS.md, PROMPT.md and 4 links hold), and published: packs cf449512.
3. Found before publishing: returns (82ac4e7) and wf-functional (3daaa48) both added .gitattributes with different text, so merging the builder's commit into returns is an add/add conflict, and `wf return --push` would stop with "does not merge cleanly". Fix (prepared, not pushed; only Prima's packs push is allowed here): one commit on returns giving .gitattributes the same text as wf-functional. A merge test of that commit with wf-functional is clean.
