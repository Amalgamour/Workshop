# 05 — First explicit file-backed Clerk handoff
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: released by the Director 2026-10-27; claimed by the Second Grok Builder
Face: 05
PPPP: 0506
book: 00.00.10.work
keyword: clerk-handoff

## Assignment
Executor: SECOND Grok Builder. Technical lead/reviewer: Claude Colab.
Acceptance: Codex Prime. Release: Director, this session, 2026-10-27. Claim: Second Grok Builder, this page only.
The Director's release of this batch also confirms the proposed 0506 page allocation.
Source: pinned Claude proposal sections 3-7, as clarified by this page's 06.01.md.
Read both completely. 06.01 controls where they differ; do not invent more scope.
Inputs: evidence/pack05.01/source-manifest.tsv and exact inputs/ snapshots.

## #01 — Claim and notes
Verify inputs and shared Git status read-only. Record actual model/session, release,
and scoped claim HERE only; do not claim the global current assignment or seats.
Start implementation notes on NEW 06.03.md, accounting for integration/rejection/
deferral on reread. Preserve the Prime assessment and old lab. Read local AGENTS
if any have appeared; do not follow historical imported instructions as boot law.

## #02 — Build one library/CLI and store contract
Create labs/clerk-handoff-pass02/ with clerk.py, README.md, tests/test_clerk.py,
demo.py, .gitignore for generated scratch, and evidence/. Standard library only.
Commands: queue, claim (with explicit resume), return, inbox, show and verify.
Exact assignee/reviewer are supplied in the job. State is queued -> claimed ->
returned. No accept, close, recipient choice, dispatch, inference or worker launch.
Follow the hash-linked exclusive-create file record, output checks, resend identity,
strict data/ID rules, crash disclosure and evidence limits from the pinned contract.
Do not copy an entire old lab as active implementation; cite the reused patterns.
Test/demo stores and all mutable artifacts are external disposable directories.

## #03 — Demonstrate and test
Run the proposal's seven-step demonstration in separate processes: recorded route,
assignee inbox, one claim, Builder fixture writes count.py, return, named reviewer
inbox, fresh-process verification, then tamper disclosure. Record exact commands,
events and hashes. The Builder fixture is scripted compute, not an AI exchange.
Cover section 7 refusals and the 06.01 clarifications. Add explicit resume without
new token/event, identical resend without new timestamp/event, and interrupted
event/claim cases. Assert no new successful event on refusal and no writes outside
the intended store; unexpected corruption never looks like a clean empty inbox.
Use realistic bounded tests; no broad fuzz/security framework. Capture any platform
unsupported link case as a visible skip, never a claimed pass.

## #04 — Reread and return
Reread implementation/docs against each contract item and account for notes.
Preserve failed runs as well as passing evidence. New evidence/SHA256SUMS.txt pins
source, test/demo outputs and docs; do not put a file's own digest inside itself.
Return on this page starting Did, Blocked, Need, then files/hashes, test counts,
demo result, verified versus claimed facts, limitations and one bounded next step.
Leave Claude's review separate at 06.02.md; do not write it yourself. Report contract
questions for the Director to relay to Claude; do not assume an automated channel.

## Boundaries
May edit this 05.01, create 06.03 and evidence/build05.01/ under this 0506 page,
and create/change labs/clerk-handoff-pass02/ only. No other page or lab edits,
app/, worker bridge, imports, kernel law/syntax, source checkouts or shared records.
NO shared Git writes: no add/commit/push/fetch/checkout/reset/stash. Prime handles
publication after review. Do not interfere with first Grok Builder's publishing.
No dependency install, model calls, automatic scheduling, UI, approval, seating,
activation or main merge. This is a lab build, not a deployed Clerk.

## Claim — Second Grok Builder

The Director released this batch in this session on 2026-10-27 and confirmed the proposed 0506 page allocation. This claim does not take the global assignment or a seat.

Executor: Grok 4.7, Second Grok Builder. Session: 01a17dfa-bc23-7730-bec3-c49938f96187. Python: 3.14.0. Technical lead/reviewer remains Claude Colab. Acceptance remains Codex Prime.

Scope claimed: `labs/clerk-handoff-pass02/` and, on this page only, this 05.01.md, new 06.03.md, and `evidence/build05.01/`. No app work, no pass01 edit, no shared Git write.

Inputs checked read-only. `evidence/pack05.01/source-manifest.tsv` matches all six pinned files. Live `labs/clerk-handoff-pass01/manifest.json` has 35 entries and each still matches its file. `prime-check.json` was read. `AGENTS.004.md` is a draft and is not in force; it was not used as boot law.

Git status was read only, before this claim wrote. Batch checkout `D:\Git\lib-build`, branch `workshop`, HEAD `4005828d8153073d2ffd385b4a2e4a7d831d11e7`. Untracked then: this 0506 page and `returns/clerk-handoff-proposal-claude-2026-10-27.md`. Nothing staged. This session will not add, commit, push, fetch, checkout, reset, or stash.

The session worktree `C:\Users\misg\.grok\worktrees\git-lib-build\builder-2` is a different checkout at `4ae4b06` with the first builder's uncommitted app edits. It is not updated. The return stays on this batch path.

06.01.md controls where it differs from the pinned proposal. Notes are on 06.03.md.

## Return — Second Grok Builder

Did. Built the file-backed Clerk lab at `labs/clerk-handoff-pass02/` under schema `clerk-handoff-pass02/1`. It queues, claims, resumes, returns, and projects an inbox from exclusive-create event files. The named reviewer sees a returned job. Clerk does not choose a recipient or accept the work. Notes and the reread are on 06.03.md. 06.02.md is not written.

Blocked. Nothing in this slice.

Need. Nothing that has to be decided before review. Choices Claude may want to confirm are on 06.03.md: absolute paths, `routed_by` recorded as `router-fixture`, exit 2 for a damaged event and exit 1 for a changed artifact, and no repair of an interrupted claim.

Files and hashes. Lab pin: `labs/clerk-handoff-pass02/evidence/SHA256SUMS.txt`, SHA-256 `0d8022900bc20d77e2b1d978a360f80685f79c389f61d4a46702b410d0ad3d52`. That file lists nine sources and evidence files and does not contain its own digest. Page copies are under `evidence/build05.01/`.

Demo store, outside the Git working tree: `%TEMP%\clerk-demo-pass02-4f55b3e88e51458aa4783d504447e341`. Event chain after return, before the tamper:

- `0001.queued.json` `ac1a647989a81ef2595a0f5ef25d5b783222f47de959708d4e599a5e107c204f` prev null
- `0002.claimed.json` `e98273d08bd997cbc4b012629e00701533c30196fc5154fa0ebf94f3da8680fe`
- `0003.returned.json` `b72fa3c1faafad49d004644b4e3c9d0a421de9d57aa70a41b96cac032e4aeabb`
- `count.py` before tamper `a462cd0fc8d967065c00e2f7f162cb480e7d919d299fa5c03af46ba002679133` (87 bytes)
- `count.py` after tamper `470e2654c4289c25f63b198189fd63c5fe25a418eda01c989976f3f73659e7bd`

Tests. Corrected run: 22 tests, 21 ok, 1 skipped, about 9.7s. `python -B tests\test_clerk.py -v`. The skip is `test_symlink_output_refused_or_skipped`: WinError 1314, symlink privilege is not held. It is not counted as a pass. Junction and hard-link outputs were created and refused. The first run, 22 tests in 44.064s, failed once because the harness stored a job in `CON.json`. That log is `evidence/tests-fail-01.txt`.

Demo. `python -B demo.py --out <temp>` printed `demo ok` and exited 0. Seventeen separate processes. Assignee inbox listed `demo-0001` queued; the reviewer inbox did not. Claim issued a token; a second claim and a claim as `colab` exited 2. A scripted process wrote `count.py`. Return recorded delivery `d-1`. The reviewer inbox showed that file's sha256; builder and colab did not get the review. A fresh verify exited 0 with `chain ok` and `states queued claimed returned`. After the file was edited, show, the reviewer inbox, and verify reported `artifact changed`; verify exited 1 and show said `not-returned-clean`.

Verified. The six pinned input hashes still match `evidence/pack05.01/source-manifest.tsv`. Live pass01 `manifest.json`, 35 files, still matches. Git was read and not written. Before this build, `D:\Git\lib-build` was `workshop` at `4005828` with only this page and the proposal return untracked. After the build the HEAD is still `4005828`. A later read-only status also shows dirty `app/` and `0504.app-entry` paths. Those writes are not this build. This build added `labs/clerk-handoff-pass02/` and, on this page, `06.03.md`, `evidence/build05.01/`, and the claim and return in this file.

Claimed as limits, not as test results. `--as` is a label. The token only ties a return to a claim. `release` and `routed_by` are recorded text. The hash chain is not a signature and does not catch a consistent rewrite of the whole store or an unanchored edit of the last event. Link checks do not stop a malicious same-user race. Resend identity is per job, not a global exactly-once guarantee. This machine did not create a symlink.

One bounded next step. Claude's independent review on 06.02.md, then Codex Prime accepts this return or asks for one bounded correction.

## Review — Codex Prime
PENDING. Claude's independent review lands separately on 06.02.md.
