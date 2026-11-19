# Dev journal: address drift fix (t413u, t414u)

date: Thu 19 Nov 2026, about 1:10-1:35 PM EST. written by: Prima builder-b21.
Why: t413u. Matthew approved "1-3 is good, remove the old WF pages, or mark them as retired". t414u then held all publishing until Designer checks. Spec: docs/spec/ADDRESS-DRIFT-t413u.md.

## Found on the way
- Job 1 had already run. Cursor-1 claimed 90.50.00.0001.05.01 at 1:03 PM EST and returned it at 1:05 PM EST, before t413u. The commit is 439a4eb2, merged into returns (402475d1, log 60dd7e25). Matthew had also pushed the .gitattributes fix (3917464e), so the merge was clean. The builder ran `cargo build` on Windows and elevated w02 (the test can't run there). A check dry-run on the box passes (`cargo test --test wf builder_prompt`: 1 passed).
- My first local retire note on 90.50.00.0001 was written before intake, so it forked the log at entry 7: my note against the builder's claim. I copied that page folder to scratch/wf-run-gh-set-aside/90.50.00.0001-forked-local-entry7, restored the published copy (cf449512) with `git checkout -- pages/90.50.00.0001`, ran intake (+3 entries), then wrote the note again (entry 10). Nothing forked was ever published. Lesson: intake before writing to a page that a builder may hold.

## What was done (all local; nothing published, t414u)
- wf-run (pinned wf, a00bc53): `halt --note "retired: ..."` on 90.10/90.20/90.30.00.0001. Entries 85->86, 49->50, 37->38; verify ok with both binaries. A copy of the pages from before is in scratch/wf-run-backup-t413u.
- wf-run-gh 90.50.00.0001: face 06 retire note (10 entries). Its pass 05.01 is still at return: check, signoff and close stay with Prima.
- 90.50.10.0400: door, registry in face 01 (3 entries).
- 90.50.10.0401: job 1 packed again (start 3daaa48). It duplicates the work that already landed, so Designer should withdraw it or leave it unpublished.
- 90.50.10.0402: job 2 packed, start origin/returns = 60dd7e25 (job 1 landed).
- Earlier: the first unpublished 90.50.00.0001 pack is in scratch/wf-run-gh-set-aside/90.50.00.0001-pack1-unpublished.
