# Workshop master document (draft)

For Matthew, the Director.
Written by Researcher for Prima, from the inventory and the repo docs.
Date: Thu 19 Nov 2026, morning, America/Toronto (Eastern Time).
This is a draft. It is not a ruling. It is not a commit.

How this was made:
I used the inventory at `/workspace/workshop-build/scratch/MASTER-INVENTORY-draft.md`.
I also used files in `docs/spec`, `docs/design`, and `docs/review` in `/workspace/workshop-build/repo`.
I cite a path for each key claim.
I did not invent a purpose or a plan that is not in those sources.
I did not `git add` or commit this file.
I did not change the repo.

If two sources disagree, both sides are at the end.
I did not pick a winner.

---

## What the Workshop is

The Workshop is a place to keep reasons, not only finished plans.

A "why" is the reason to do something.
A finished spec is a recipe, and recipes can rot.
With the why, a rebuild is possible. (`docs/spec/AGENTS.md`; `docs/spec/Design.md`)

It must be checkable by a person.
Models can forget (the docs say "intelligence bleeds").
So the record has to be reliable. (`docs/spec/AGENTS.md`)

People authorize.
Models reason and propose.
The compute checks and writes.
Models do not write the real records themselves. (`docs/spec/AGENTS.md`; `docs/spec/Design.md`)

Your words from t226u say the design is for this work to be automated.
The compute keeps status and prompts models to work.
Prompts between model and compute run the work.
This stage comes before that full system. (`docs/review/DIRECTOR-WORDS-t226u.md`)

Books hold pages.
Pages hold faces.
Faces hold cards.
Each piece has an address (SeqAddr). (`docs/spec/AGENTS.md`; `docs/spec/seqAddr.md`; `docs/spec/Design.md`)

The compute is the only writer of books.
People and models stay outside the page.
They reach a face only through the compute.
Several models may work one page at once. (Your drawing t262u, as read in `docs/design/WORKFLOW-TOOLS.md`)

The parts that exist today (`docs/spec/Design.md`; repo `README.md`):
- Core, in Rust: addresses, book logs, and rules.
- Compute, in Rust: one process that owns the books. Reads are open. Writes go through a queue.
- A reader app, in Next.js: shows faces and how they link.
- Books: logs that only add lines (JSON Lines).
- wf: a command-line tool that runs one work page and keeps the record. The log is the truth. Page files are copies printed from it. A hand edit makes wf stop. (Inventory, from the wf README on branch `workflow`)

The nine axioms are the shape of the reasoning.
Sequence Address is the geometry. (`docs/spec/Axioms.md`; `docs/spec/Design.md`)
You are the Director.
Only you approve. (`docs/design/WORK-BOOK-BRIEF.md`; `docs/design/WORKFLOW-TOOLS.md`)

The rest of this draft lists each piece: what it is, why it exists, and where it lives.

---

## Branches

`workflow`, `board-dev`, and `harden-dev` are branches of `/workspace/workshop-build/repo`.
`prima/build` and `reference/lib-build` are not branches of that repo.
They live in other copies, noted below.
This repo has no remotes set.
(Inventory)

### `workflow`

What it is: the source of the wf tool.
This is the line meant to be the next published wf kit.
Same tip as `wf-next`.
Last commit: restore a return step that an earlier pass had removed, so old records can stay (axiom 6).
Tree: `src/`, `tests/`, `templates/`, `docs/`, `AGENTS.md`, `README.md`.
Not the core or books tree.
Why it exists: so the wf tool has one source line to build and ship from.
Where it lives: branch of `/workspace/workshop-build/repo`, tip `a00bc53`.
Also checked out at `/workspace/workshop-build/workflow`.

### `board-dev`

What it is: a wf branch that adds the read-only work board (`wf board`).
Last commit: Tester's fixes (no panic on a missing pass, card lines name their source, escapes, flags).
Not merged into `workflow` yet (open question 13).
Why it exists: so you can see what needs someone, what is moving, and what passed, in under a minute.
Where it lives: branch of `/workspace/workshop-build/repo`, tip `193da07`.
Worktree: `/workspace/workshop-build/scratch/board-dev`.

### `harden-dev`

What it is: a wf branch that checks log order and escapes hostile text in observer output.
Last commit: escape close-outcome words in the observe loop line.
Tester has not yet checked this last commit (open question 17).
Not merged into `workflow` yet (open questions 14 and 16).
Why it exists: so a messy or hostile log cannot break the record or the display.
Where it lives: branch of `/workspace/workshop-build/repo`, tip `1f32ecb`.
Worktree: `/workspace/workshop-build/scratch/harden-dev`.

### `build`

What it is: the main Workshop build.
It holds the Rust core, the books, the kernel, the reader app, and the docs in `docs/`.
Last commit: a review note on the harden-dev end state and a close-outcome option, for Nov 19.
Why it exists: this is the tree for the core product and its specs, journals, and reviews.
Where it lives: current branch of `/workspace/workshop-build/repo`, tip `488d2ba`.

### `prima/build`

What it is: the GitHub publish name for the clean `build` line.
It is not a branch of `/workspace/workshop-build/repo`.
A local copy is `/workspace/workshop-build/publish`.
That copy's branch `build` tracks `origin/prima/build` (tip `0f7616d`).
It shares a commit message with repo `build` `488d2ba`, but not the same hash.
Kernel trial docs say publish history is filtered, and a push goes only to `prima/build`.
Why it exists: a clean line to publish, with history filtered.
Where it lives: `/workspace/workshop-build/publish`, tracking `origin/prima/build`.
See also disagreement 2, at the end.

### `reference/lib-build`

What it is: the branch of the old-lib copy.
It is not a branch of `/workspace/workshop-build/repo`.
`packed-refs` and `HEAD` name `reference/lib-build` at `cce5d257` (also packed as `origin/clean`).
The working-tree README calls it "lib-build: the Workshop development desk".
The README also says the branch is `workshop` of `github.com/Amalgamour/Librarian`.
The clone's git config points at `github.com/Amalgamour/Workshop` on `reference/lib-build`.
Both wordings are recorded. I did not pick a side (disagreement 1).
The empty folders `.git/refs/heads` and `.git/refs/tags` were added so git can run.
`git log -1 reference/lib-build` now works and shows tip `cce5d257`.
217 files are missing from the copy on disk, mostly old evidence and output files (`git status` shows them as deleted). They were probably lost in the Nov 18 snapshot restore. We are leaving them as they are, because the copy is only a reference and `git show cce5d257:path` still reads every one.
No fetch, reset, delete, overwrite, or checkout was done.
Why it exists: a pinned copy of the old lib build, for reference and mining.
Where it lives: `/workspace/workshop-build/lib-ref`, branch `reference/lib-build`, tip `cce5d257`.

### Other branches in `/workspace/workshop-build/repo`

`wf-next`
What it is: the same commit as `workflow`.
Why it exists: a worktree used to develop wf.
Where it lives: tip `a00bc53`, worktree `/workspace/workshop-build/wf-run/wfdev`.

`bench`
What it is: a wf branch that adds a small bench crate and a baseline on page `90.10.00.0001`.
Why it exists: so speed can be measured against a known page.
Where it lives: tip `5cc2a93`, worktree `/workspace/workshop-build/bench`.

`core-wf`
What it is: the core "write once" line.
Same tip as `pass/90.20.00.0001.05.05`.
The tree matches `build` (crates, books, kernel, app).
Why it exists: the line that carried the write-once work.
Where it lives: tip `2f66bda`, worktree `/workspace/workshop-build/wf-run/core`.

`merge-rehearsal`
What it is: a practice merge of `harden-dev` (`1f32ecb`) after `board-dev`.
Dated 19 Nov 2026.
Not the live `workflow` branch.
Why it exists: to practice the merge before it is real.
Where it lives: tip `6bd4b17`, worktree `/workspace/workshop-build/scratch/merge-rehearsal`.

`pass/90.20.00.0001.05.01` (`f363e28`) through `.05.05` (`2f66bda`)
What they are: frozen builder-return branches for the "write once" page.
Each holds one pass of the core work (delivery ids, restart, first-write-wins, records, then the fix-up).
Why they exist: so each pass can be opened again later (axiom 6).
Where they live: branches of `/workspace/workshop-build/repo`.

`pass/90.30.00.0001.05.01` (`2a6aa0a`) through `.05.04` (`84cecd4`)
What they are: frozen builder-return branches for the "wf ready for next week" page.
The passes cover halt and resume, a return-file note, pack templates, and the category table and escapes.
Why they exist: so each of those passes can be opened again later.
Where they live: branches of `/workspace/workshop-build/repo`.

No other local branch names were present.
There are also leftover detached worktrees under `scratch/` (old tester copies).
Those are not branches.

---

## The wf tool

What it is: a small command-line tool that runs one work page and keeps the record.
People and models ask it.
They do not edit the page files by hand.
The log `pages/<page>/log.jsonl` is the truth.
The page files are copies printed from it.
If someone edits a page file by hand, wf refuses to go on.
Why it exists: so the compute, not a model, keeps the rules and the record.
Where it lives: source on branch `workflow` (`workflow:README.md` and `workflow:src/`, including `src/lib.rs`, `src/cmd.rs`, `src/page.rs`).
Pinned binary in use: `/workspace/workshop-build/wf-bin/wf`, built from `a00bc53` (same as `workflow`).
An older binary sits beside it: `/workspace/workshop-build/wf-bin/wf-8eb1fdb`.
Open question 15 asks to rename that older binary so no one writes with it by accident.
I name the path only.

Every command that writes needs `--as <name>` (or `WF_AS`).
Root folder: the current folder, or `WF_ROOT`.

### Commands in the pinned binary (and on `workflow`)

Source: `wf --help`, `workflow:README.md`, and help text in `workflow:src/lib.rs`.

`init-page`
What it is: start a page: title, person, prime, and the grant (which files may be touched), with a grant ref.
Why it exists: so a page begins with a clear owner and a clear grant.
Where it lives: pinned `wf` and branch `workflow`.

`set-prime`
What it is: change who the Prime is, with a ref.
Why it exists: so the lead can change, and the change is recorded.
Where it lives: pinned `wf` and branch `workflow`.

`grant`
What it is: widen the grant (more paths), with a ref.
Optional `--answers` ties it to an answer entry.
Why it exists: so more files can be touched only with a recorded yes.
Where it lives: pinned `wf` and branch `workflow`.

`face-write`
What it is: write text onto a face (01, 02, 04, 06, or 08).
Face 04 needs a section: goals, decisions, or responses.
Text may come from `--text` or `--file`.
Why it exists: so face text goes through wf, not a hand edit.
Where it lives: pinned `wf` and branch `workflow`.

`draft`
What it is: Prime writes the plan for a pass.
wf pins what Prime read (faces 04 and 06, and the last closed 05).
`--pass` can redraft a pass that is not packed yet.
`--overlap-ok` lets a new draft start while another packed pass is still open, with a why and a ref.
Why it exists: so the plan is pinned to what Prime actually read.
Where it lives: pinned `wf` and branch `workflow`.

`pack`
What it is: Prime releases the plan.
wf checks it, then prints the job box for the builder.
Why it exists: so a job is only issued after the plan passes the checks.
Where it lives: pinned `wf` and branch `workflow`.

`claim`
What it is: a builder takes the job.
First claim wins.
Why it exists: so two builders cannot take the same job.
Where it lives: pinned `wf` and branch `workflow`.

`return`
What it is: the builder pings wf with the branch, the commit, and the return file.
wf checks the files against the grant.
Why it exists: so the compute files what was done, and checks the grant.
Where it lives: pinned `wf` and branch `workflow`.

`check`
What it is: the checker (never the builder) runs the pack's tests.
`--dry-run` prints the result and writes nothing.
`--note` or `--fail` can be added.
Why it exists: so a different view tests the work.
Where it lives: pinned `wf` and branch `workflow`.

`signoff`
What it is: Prime records the outcome: passed, failed, blocked, or needs-authority.
Cards can be named (`w01=accepted`, and so on).
A note with a ref is needed for some hard cases.
Why it exists: so the lead, not the builder, records the outcome.
Where it lives: pinned `wf` and branch `workflow`.

`close`
What it is: write the close record after signoff.
The same refusals as a passed signoff are run again.
Why it exists: so a close is checked twice, then written into the log.
Where it lives: pinned `wf` and branch `workflow`.

`elevate`
What it is: send a stuck item up to Prime or to the person.
Why it exists: so a hard case goes up, instead of being forced through.
Where it lives: pinned `wf` and branch `workflow`.

`answer`
What it is: answer an elevated item, by entry number.
Why it exists: so the answer is tied to the item that went up.
Where it lives: pinned `wf` and branch `workflow`.

`halt`
What it is: Prime or the person stops the page (refused while a pass is open).
After a halt, draft, pack, and claim refuse.
Why it exists: so work can be stopped on purpose, and recorded.
Where it lives: pinned `wf` and branch `workflow`.

`resume`
What it is: Prime or the person lets draft, pack, and claim go on again.
Why it exists: so a halted page can start again, with a record.
Where it lives: pinned `wf` and branch `workflow`.

`status`
What it is: read only.
Show where the page stands, built fresh from the log.
Why it exists: so anyone can see the state without writing.
Where it lives: pinned `wf` and branch `workflow`.

`observe`
What it is: observer signals (stall hours, loops).
`--record` files a finding.
Read-mostly; `--record` writes.
Why it exists: so drift, loops, and stalls can be seen and filed.
Where it lives: pinned `wf` and branch `workflow`.

`verify`
What it is: check the log chain and every view file.
`--fix` reprints missing or changed views from the log.
Why it exists: so the printed files can be checked against the log, and repaired from it.
Where it lives: pinned `wf` and branch `workflow`.

### Extra command, not in the pinned binary

`board`
What it is: a read-only work-order board.
No log write, no view write, no lock, and it does not run git.
`wf board` lists every page in one line.
`wf board <page>` shows attention first, then columns.
`--card NN` shows one pass, with each line naming its source.
`--all` shows lines past the usual 40-line cap.
`--stall-hours` defaults to 24.
Marked "build stage, pending Director answer" (open questions 8 and 13).
Why it exists: so you can see what needs someone, what is moving, and what passed, in under a minute.
Where it lives: only on `board-dev` (and in the `merge-rehearsal` merge), not in the pinned `workflow` binary.
Source and words: `board-dev:README.md` and `docs/design/WF-BOARD.md`.

---

## Page addresses of the form 90.x0.00.0001

I found no single definition table for the `90.x0` pattern in `docs/spec`.
The wf README says v0 page ids are temporary labels, not checked as SeqAddr (`workflow:README.md`, around line 135).
A Codex triage notes that these ids already look like SeqAddr (`docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md:291`).
Both are recorded (disagreement 3).

What exists today is usage.
This build's wf work pages use `90.10`, `90.20`, `90.30`, and a planned `90.40` set.
Live pages sit under `/workspace/workshop-build/wf-run/pages/` (not inside the `build` tree).
Title and grant below come from each page's `00.md` view, which wf printed from the log.

### Live pages

`90.10.00.0001`
What it is: title "workflow kit".
The first real wf page (also called the dogfood page).
85 log entries.
Person Matthew, Prime Prima.
Grant: src, tests, templates, docs, examples, README, AGENTS, Cargo.toml (from t267u).
Why it exists: to run and prove the wf kit on a real page.
It is also the baseline for board tests and the core-via-wf plan.
Where it lives: `/workspace/workshop-build/wf-run/pages/90.10.00.0001/`.
Mentioned in `docs/design/PLAN-2026-11-18-core-via-wf.md:6` and `docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md`.

`90.20.00.0001`
What it is: title "core: write once".
The page that added delivery ids and write-once rules to the core.
49 log entries.
Grant: `crates/compute/`, `crates/seqaddr-core/`, `docs/CONTRACT.md`, `docs/BUILD-LOG.md` (from t285u).
Why it exists: so a write is kept once, and a replay is safe.
Where it lives: `/workspace/workshop-build/wf-run/pages/90.20.00.0001/`.
Spec: `docs/spec/WRITE-ONCE.md`.
Journal: `docs/journal/2026-11-18-write-once.md`.

`90.30.00.0001`
What it is: title "wf: ready for next week".
The page that made wf ready for the next stretch (halt, resume, templates, escapes).
37 log entries.
Grant: src, tests, templates, README, AGENTS, examples (from t267u).
Why it exists: so wf can be halted, resumed, and used more safely in the next stretch of work.
Where it lives: `/workspace/workshop-build/wf-run/pages/90.30.00.0001/`.
Spec: `docs/spec/WF-90.30.md`.
Journal: `docs/journal/2026-11-18-wf-90.30.md`.

### Planned, not on disk

I found no `90.40*` folder under `wf-run/pages/`.
These four are planned in `docs/design/HANDOFF-TRIAL-01.md`.
They are a handoff trial, not live work pages.

`90.40.00.0001`
What it is: case A, "Sound successor" (control).
The pack restates the goal and links the earlier failed pass.
Why it exists: the clean case, to compare with the others.
Where it lives: planned only, in `docs/design/HANDOFF-TRIAL-01.md:28`.

`90.40.00.0002`
What it is: case B, "Lost context".
The pack says only "fix the clamp"; the real reason lives only in the earlier pass.
Why it exists: to see what happens when the new pack hides the why.
Where it lives: planned only, in `docs/design/HANDOFF-TRIAL-01.md`.

`90.40.00.0003`
What it is: case C, "Deliberate deletion".
A later pass drops a job on purpose, with a recorded reason.
Why it exists: to see a planned drop, with the reason on record.
Where it lives: planned only, in `docs/design/HANDOFF-TRIAL-01.md`.

`90.40.00.0004`
What it is: case D, "Planted bad line".
Same as A, but a bad line is planted in AGENTS.md to see if a worker follows it.
Why it exists: to test whether a worker follows a planted bad instruction.
Where it lives: planned only, in `docs/design/HANDOFF-TRIAL-01.md`.

I found no live or planned `90.00`, `90.50`, or higher in the repo docs or under `wf-run/pages/`.

---

## Files in docs/spec

Path root: `/workspace/workshop-build/repo/docs/spec/`.
These are the governing specs.
Where a contract and a spec disagree, the spec wins (`docs/CONTRACT.md`).

### Main specs

`AGENTS.md` (53 lines)
What it is: early Workshop instruction notes (business wants and a few technical rules, such as keep the why).
Why it exists: a short agents file for this project.
It is not the wf kit `AGENTS.md` on the `workflow` branch.
Where it lives: `docs/spec/AGENTS.md`.

`Axioms.md` (29 lines)
What it is: the nine axioms in short form, so a model can carry a large idea in a small cite.
Why it exists: the shape of the reasoning.
Where it lives: `docs/spec/Axioms.md`.

`DIRECTOR-RULINGS.md` (204 lines)
What it is: your rulings given in chat.
These outrank older spec wording.
Why it exists: one place for what you have already decided.
Where it lives: `docs/spec/DIRECTOR-RULINGS.md`.

`Design.md` (99 lines)
What it is: the system overview.
It points to the other specs, and says each rule lives in exactly one of them.
Why it exists: to tie the other documents together.
Where it lives: `docs/spec/Design.md`.

`SEQ-GUIDE.md` (609 lines)
What it is: a reader's guide to the `.seq` page file, written for you.
Why it exists: so the page file can be read in plain words.
Where it lives: `docs/spec/SEQ-GUIDE.md`.

`WF-90.30.md` (123 lines)
What it is: the spec for the wf tool on `workflow` at `a00bc53`, from page `90.30.00.0001`.
Why it exists: to state what "ready for next week" means in the tool.
Where it lives: `docs/spec/WF-90.30.md`.

`WF-BOARD-AND-LOG-ORDER.md` (230 lines)
What it is: the spec for the board work and the log-order check, on two builder branches that are not yet merged into `workflow`.
Why it exists: to state those two branches before they merge.
Where it lives: `docs/spec/WF-BOARD-AND-LOG-ORDER.md`.

`WRITE-ONCE.md` (312 lines)
What it is: the spec for write-once and delivery ids in the core, from page `90.20.00.0001`.
Draft choices in it wait for you (K4).
It describes code on `build` / `core-wf`.
Why it exists: to state the write-once rules for the core.
Where it lives: `docs/spec/WRITE-ONCE.md`.

`brands.md` (97 lines)
What it is: how brands (kinds of marks) fit together.
Rules live in `decisions.md`.
Why it exists: to show how those marks relate.
Where it lives: `docs/spec/brands.md`.

`decisions.md` (648 lines)
What it is: working record of seqAddr decisions and their reasons.
Why it exists: so each decision keeps its why.
Where it lives: `docs/spec/decisions.md`.

`drafting.md` (46 lines)
What it is: how drafting is meant to work.
The principle is settled; enforcement is still proposed.
Why it exists: to state how a face is changed.
Where it lives: `docs/spec/drafting.md`.

`face00.md` (478 lines)
What it is: Face 00: the stamp, the page type, and the registry.
Why it exists: to define the page's stamp face.
Where it lives: `docs/spec/face00.md`.

`format.md` (160 lines)
What it is: the book file format (how a book is stored).
Why it exists: so the book file has one written shape.
Where it lives: `docs/spec/format.md`.

`kernel-design.md` (168 lines)
What it is: design draft for the kernel (the first book and how it is built).
Why it exists: to describe the kernel's role and bootstrap.
Where it lives: `docs/spec/kernel-design.md`.

`review.md` (180 lines)
What it is: a condensation review of the older `claude` branch, kept as background.
Why it exists: so that older review is still at hand.
Where it lives: `docs/spec/review.md`.

`seqAddr.md` (307 lines)
What it is: the address system: addresses, faces, cards, page layout, and grammar.
Why it exists: this is the geometry of the store.
Where it lives: `docs/spec/seqAddr.md`.

`seqpage-QUESTIONS.md` (48 lines)
What it is: open questions about the `.seq` page file.
Why it exists: to keep those questions in one place.
Where it lives: `docs/spec/seqpage-QUESTIONS.md`.

`seqpage.md` (263 lines)
What it is: the spec for the `.seq` page file itself.
Why it exists: to define the page-file view of a book page.
Where it lives: `docs/spec/seqpage.md`.

`workflow-loop.md` (291 lines) and `workflow-loop.003.md` (317 lines)
What they are: two versions of the workflow-loop spec (how a pass moves from plan to close).
I list both.
I did not pick which is current (disagreement 5).
Why they exist: to describe the pass from plan to close.
Where they live: `docs/spec/workflow-loop.md` and `docs/spec/workflow-loop.003.md`.

`workflow-loop.002-notes.md` (69 lines)
What it is: drafting notes and a read-back for loop version .002.
Why it exists: to keep the notes from that draft.
Where it lives: `docs/spec/workflow-loop.002-notes.md`.

### Examples in docs/spec/examples

Why they exist: so the format can be seen and checked, not only described.
Where they live: `/workspace/workshop-build/repo/docs/spec/examples/`.

`examples/00.00.00.0051.seqaddr.seq` — sample page "seqaddr" at `00.00.00.0051`.
`examples/10.11.21.1001.bob.seq` — sample page "bob" at `10.11.21.1001`.
`examples/10.11.30.1501.timer.seq` — sample page "timer" at `10.11.30.1501`.
`examples/face00/10.11.40.0000.seq` — sample "workshop" stamp page at `10.11.40.0000`.
`examples/face00/10.11.40.0012.dictionary.seq` — sample "dictionary" at `10.11.40.0012`.
`examples/face00/10.11.40.0400.dev.seq` — sample "dev" at `10.11.40.0400`.
`examples/face00/10.11.40.0403.ide-design.seq` — sample "ide-design" at `10.11.40.0403`.
`examples/face00/10.11.40.1001.cats.seq` — sample "cats" at `10.11.40.1001`.
`examples/proposals/10.11.21.1001.bob.seq` — a proposal cut of the bob page.
`examples/proposals/10.11.21.1002.seq` — a short proposal sample titled "cats".
`examples/real/10.11.21.1001.bob.seq` — bob page exported from a real book, not written by hand.
`examples/real/README.md` — says the "real" `.seq` files were exported by the seqpage tool from `books/`.
`examples/sources/00.00.00.ruled.book` — source book `00.00.00` used to build some examples.
`examples/sources/10.11.21.book` — source book `10.11.21`.
`examples/sources/10.11.30.book` — source book `10.11.30`.
`examples/sources/10.11.40.book` — source book `10.11.40`.

---

## Files in docs/journal

Path root: `/workspace/workshop-build/repo/docs/journal/`.
These tell the story of how a page was built, in plain order, so the team can see what happened and why.

`2026-11-18-write-once.md` (276 lines)
What it is: the story of page `90.20.00.0001` (core write once), including the five passes and what Tester found.
Why it exists: so that page's work can be read in order.
Where it lives: `docs/journal/2026-11-18-write-once.md`.

`2026-11-18-wf-90.30.md` (142 lines)
What it is: the story of page `90.30.00.0001` (wf ready for next week), including halt, templates, and the escape work.
Why it exists: so that page's work can be read in order.
Where it lives: `docs/journal/2026-11-18-wf-90.30.md`.

`2026-11-18-wf-board-and-log-order.md` (192 lines)
What it is: the story of the board branch and the log-order check on `harden-dev`, including Tester's rounds.
Why it exists: so that branch work can be read in order.
Where it lives: `docs/journal/2026-11-18-wf-board-and-log-order.md`.

---

## Files in docs/review

Path root: `/workspace/workshop-build/repo/docs/review/`.
These are checks, outside reviews, and your exact words, kept so the team can cite them later.

### Reviews and checks

`CODEX-LIB-BUILD-REPORT-t323u.md` (54 lines) — Codex's report on the old lib build, relayed as t323u. Why: so that report can be cited. Path: `docs/review/CODEX-LIB-BUILD-REPORT-t323u.md`.

`CODEX-LIBRARIAN-TOOLS-REVIEW.md` (416 lines) — how Codex Prime built, used, and tested Librarian's tools. Why: a record of those tools. Path: `docs/review/CODEX-LIBRARIAN-TOOLS-REVIEW.md`.

`CODEX-MANAGER-DRAFT-t304u.md` (80 lines) — Codex's draft "Workshop Manager and the First Desk Trial", kept word for word. Why: so the draft is not retold from memory. Path: `docs/review/CODEX-MANAGER-DRAFT-t304u.md`.

`CODEX-PLAN-REVIEW-t292u.md` (28 lines) — Codex's review of the core-via-wf plan, word for word (t292u). Why: so that review can be cited. Path: `docs/review/CODEX-PLAN-REVIEW-t292u.md`.

`CODEX-WF-REVIEW-t275u.md` (139 lines) — Codex's review of the wf kit, relayed by you (t275u). Why: so that review can be cited. Path: `docs/review/CODEX-WF-REVIEW-t275u.md`.

`CODEX-WF-REVIEW-t275u-TRIAGE.md` (297 lines) — Prima's triage of that Codex wf review: what to fix, what to park. Why: so the triage is on record. Path: `docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md`.

`CORE-SPEC-HOSTILE-PASS.md` (369 lines) — Tester's hostile check of the core-and-tools spec. Not a ruling. Why: a hard check, kept as advice. Path: `docs/review/CORE-SPEC-HOSTILE-PASS.md`.

`CORE-SPEC-REVIEWS-t210u.md` (78 lines) — outside reviews of the core-and-tools spec, relayed word for word (t210u). Why: so those reviews can be cited. Path: `docs/review/CORE-SPEC-REVIEWS-t210u.md`.

`CURSOR-BUILD-REVIEW.md` (188 lines) — a review of Cursor's own Workshop build (branch `cursor/build`). Why: to compare with that other build. Path: `docs/review/CURSOR-BUILD-REVIEW.md`.

`DEV-WORK-LAB-PAGES-CHECK.md` (156 lines) — Tester's hostile check of the dev / work / lab page design. Advice only. Why: a hard check, kept as advice. Path: `docs/review/DEV-WORK-LAB-PAGES-CHECK.md`.

`DIRECTOR-AGENTS-DRAFT-t332u.md` (61 lines) — your AGENTS.md draft, saved as t332u. Why: so your draft is kept word for word. Path: `docs/review/DIRECTOR-AGENTS-DRAFT-t332u.md`.

`FACE-05-D6-CHECK.md` (149 lines) — Tester's check of what face 05 should hold (D6). Advice only. Why: a check, not a ruling. Path: `docs/review/FACE-05-D6-CHECK.md`.

`OUR-CODE-VS-CURSOR-LESSONS.md` (250 lines) — our code compared with lessons from Cursor's build. Why: to keep those lessons. Path: `docs/review/OUR-CODE-VS-CURSOR-LESSONS.md`.

`PACK-TEMPLATE-CHECK.md` (192 lines) — Tester's hostile check of the pack template. Advice only. Why: a hard check, kept as advice. Path: `docs/review/PACK-TEMPLATE-CHECK.md`.

`PRIMA-REVIEW-MANAGER-DRAFT-t304u.md` (42 lines) — Prima's review of the Codex manager draft (t304u). Why: so Prima's review sits next to the draft. Path: `docs/review/PRIMA-REVIEW-MANAGER-DRAFT-t304u.md`.

`QUESTIONS-2026-11-19.md` (29 lines) — the open questions 1-17 for you, for after the usage reset. Why: one short list to ask from. Path: `docs/review/QUESTIONS-2026-11-19.md`. See the questions section below.

`SAMPLE-PAGE-CLAUDE-REVIEW-t253u.md` (48 lines) — Claude's review of the sample page, relayed by you (t253u). Why: so that review can be cited. Path: `docs/review/SAMPLE-PAGE-CLAUDE-REVIEW-t253u.md`.

`SAMPLE-PAGE-CODEX-REVIEW-t252u.md` (17 lines) — Codex's review of the sample page, relayed by you (t252u). Why: so that review can be cited. Path: `docs/review/SAMPLE-PAGE-CODEX-REVIEW-t252u.md`.

`WORK-BOOK-AXIOM-CHECK.md` (77 lines) — Tester's axiom check of the work-book idea. Not a ruling. Why: a check against the axioms. Path: `docs/review/WORK-BOOK-AXIOM-CHECK.md`.

`WORK-BOOK-CONCEPT-CHECK.md` (169 lines) — Tester's check of the work-book concept. Not a ruling. Why: a check of the concept. Path: `docs/review/WORK-BOOK-CONCEPT-CHECK.md`.

`WORK-BOOK-HOSTILE-PASS.md` (200 lines) — Tester's hostile pass on the work-book spec. Not a ruling. Why: a hard check, kept as advice. Path: `docs/review/WORK-BOOK-HOSTILE-PASS.md`.

`WORK-BOOK-RESEARCH.md` (236 lines) — research (by Tester) on how AGENTS.md is used in Cursor and in Grok Build. Why: evidence for later AGENTS.md design. Path: `docs/review/WORK-BOOK-RESEARCH.md`.

### Your words

Each file holds your exact words from that chat, saved by Prima so the team does not rely on memory.
Why they exist: so your words can be cited later, as written.
Where they live: `/workspace/workshop-build/repo/docs/review/`, one file per request or card.

`DIRECTOR-WORDS-t212u.md` — request t212u.
`DIRECTOR-WORDS-t223u.md` — answers t223u, to Prima's t212s804 list.
`DIRECTOR-WORDS-t226u.md` — answers t226u, to six proposed changes.
`DIRECTOR-WORDS-t227u.md` — t227u.
`DIRECTOR-WORDS-t239u.md` — t239u (includes words on what each face of a work page holds).
`DIRECTOR-WORDS-t240u-t241u.md` — t240u and t241u together.
`DIRECTOR-WORDS-t243u.md` — t243u.
`DIRECTOR-WORDS-t245u.md` — t245u.
`DIRECTOR-WORDS-t246u.md` — t246u.
`DIRECTOR-WORDS-t249u.md` — t249u.
`DIRECTOR-WORDS-t250u.md` — t250u.
`DIRECTOR-WORDS-t254u.md` — t254u.
`DIRECTOR-WORDS-t255u.md` — t255u.
`DIRECTOR-WORDS-t259u.md` — t259u.
`DIRECTOR-WORDS-t261u.md` — t261u (pairs with the drawing below).
`DIRECTOR-WORDS-t262u.md` — t262u (several models at one page; pairs with the other drawing).
`DIRECTOR-WORDS-t263-T6.md` — your answer to T6 (card t263s974): checker and observer as roles.
`DIRECTOR-WORDS-t267u.md` — t267u and card t267s994.
`DIRECTOR-WORDS-t268u.md` — t268u.
`DIRECTOR-WORDS-t285u.md` — t285u, about 12:20 PM Eastern Time, 18 Nov 2026.
`DIRECTOR-WORDS-t301u.md` — t301u, 1:34 PM Eastern Time, 18 Nov 2026.
`DIRECTOR-WORDS-t303u.md` — t303u, 1:40 PM Eastern Time, 18 Nov 2026.
`DIRECTOR-WORDS-t305u.md` — t305u, just after t304u at 1:56 PM Eastern Time, 18 Nov 2026.
`DIRECTOR-WORDS-t306u.md` — t306u, 1:58 PM Eastern Time, 18 Nov 2026.
`DIRECTOR-WORDS-t306s1163.md` — card t306s1163.
`DIRECTOR-WORDS-t307u.md` — t307u.
`DIRECTOR-WORDS-t309u.md` — t309u (guard the compute, so an observer can check).
`DIRECTOR-WORDS-t310u.md` — t310u.
`DIRECTOR-WORDS-t311u.md` — t311u.
`DIRECTOR-WORDS-t312u.md` — t312u.
`DIRECTOR-WORDS-t316u.md` — t314u and t316u (the mining-authorized note used for Researcher task M2).
`DIRECTOR-WORDS-t326u.md` — t326u.
`DIRECTOR-WORDS-t327u.md` — t327u.
`DIRECTOR-WORDS-t328u.md` — t328u.
`DIRECTOR-WORDS-t329u.md` — t329u.
`DIRECTOR-WORDS-t333u.md` — t333u (AGENTS manager design).
`DIRECTOR-WORDS-t335u.md` — t335u: Designer may work with Researcher on a task Prima approves; Researcher is Prima's assistant first.
`DIRECTOR-WORDS-t335s1296.md` — t335s1296: the three safety rules (already answered; see the question list).

### Drawings

These are images, not text.
Why they exist: they are your drawings of the page and the compute.
Where they live: `docs/review/`.

`DIRECTOR-DRAWING-t261u.png` — your drawing from t261u.
`DIRECTOR-DRAWING-t262u.png` — your drawing from t262u.

### Scripts that try to reproduce findings

Folder `docs/review/t275u-repro/`.
Why they exist: so a finding from the t275u Codex wf review can be shown again, not only described.

`t275u-repro/lib.sh` — shared setup for those scripts.
`t275u-repro/chain.sh` — hash-chain limits (rewrite an old line).
`t275u-repro/p1-init.sh` — two inits of one page at the same time.
`t275u-repro/p1-loop.sh` — two plain claims started together.
`t275u-repro/p1-race.sh` — two claims of the same pass, with one paused mid-load.
`t275u-repro/p2-signoff.sh` — a passed signoff while a job is blocked and an elevation is open.
`t275u-repro/p3-donewhen.sh` — face 01 changes after pack; the check report should use the packed "done when".
`t275u-repro/p4-views.sh` — missing or unreadable view files, and whether verify notices.
`t275u-repro/p5-changed.sh` — the return's free-text `changed:` line, and a rename hiding a path.
`t275u-repro/seqaddr.sh` — wf accepting any label as a page id, and pass numbers past 98.
`t275u-repro/why-spots.sh` — choices that should need a why, but do not yet.

---

## Teammate bots and their roles

I only state a role when a repo doc supports it.
Page roles in the wf tool (person, Prime, builder, checker, observer) are not the same thing as teammate bot names.
One doc warns that the page role "observer" is not the Observer bot that watches this build, and that nothing in your words joins them (`docs/design/WORKFLOW-TOOLS.md:38`).
See disagreement 4.

Prima
What it is: repo docs call Prima the Prime (team lead) of the wf pages (`workflow:README.md`; each live page's `00.md` lists `prime: prima`).
Prima authors many build commits and writes the specs and journals.
The words "chief engineer" were not found in repo docs.
An older lib note says that in the first Prima pilot, Prima was Codex's assistant, not the Prime (`docs/reference/LIB-BUILD-SURVEY.md:140`).
That is old-lib history, not today's wf role.
Both are recorded.
Why it exists: to lead the build and the wf pages, as Prime.
Where the role is written: `workflow:README.md`, live page `00.md` files, and many docs under `docs/`.

Prima Worker A
Role not in repo docs (no hits for "Worker A" or "Prima Worker").

Prima Worker B
Role not in repo docs (no hits for "Worker B").

Observer
What it is: the wf page role watches Prime for drift, loops, and stalls (`workflow:README.md`; `docs/design/WORKFLOW-TOOLS.md:15`).
The Observer bot that watches this build is named as a distinct thing in `WORKFLOW-TOOLS.md:38`.
I found no fuller bot-role file.
Why it exists (page role): to watch the lead for drift, loops, and stalls.
Where the role is written: `workflow:README.md` and `docs/design/WORKFLOW-TOOLS.md`.

Tester
What it is: checks work and designs, often with a hostile pass; never the builder (`docs/review/` check files and the journals; `docs/design/HANDOFF-TRIAL-01.md` names Tester as scorer).
Often signed "Tester (Grok Bot)".
Why it exists: a different view must check the work.
Where the role is written: `docs/review/*CHECK*`, the journals, and `docs/design/HANDOFF-TRIAL-01.md`.

Designer
What it is: "design partner for Prima" (`docs/design/SEQ-FILE-PLAN.md:4`, `docs/design/SECTIONS-AND-CARDS.md:4`, and the same line in `docs/design/CORE-AND-TOOLS-SPEC.md:4`).
Writes design docs.
You are the only approver.
Why it exists: to draft design for Prima, for you to approve.
Where the role is written: those design files, and many other `docs/design/` pages.

Researcher
What it is: Prima's assistant first; may work with Designer directly only on a task Prima approves (`docs/review/DIRECTOR-WORDS-t335u.md:7-9`).
Also named as the author of the lib-mine notes (`docs/reference/LIB-MINE-M2.md:4`).
Why it exists: to research and write reference notes for Prima.
Where the role is written: `docs/review/DIRECTOR-WORDS-t335u.md` and `docs/reference/LIB-MINE-M2.md`.

Rando Bot
Role not in repo docs (no hits).

SM-Bot
Only in the old-lib survey: an idea that Observer would hand work to "the SM-bot for posts"; the posting idea is not in the roadmap (`docs/reference/LIB-BUILD-SURVEY.md:173`).
No today's-team role is stated.

Gameatron
Only in the old-lib survey: a handoff file in the first Prima pilot (`docs/reference/LIB-BUILD-SURVEY.md:73,140`).
No today's-team role is stated.

Buildabot
Role not in repo docs (no hits).

---

## Open questions 1-17

Source: `/workspace/workshop-build/repo/docs/review/QUESTIONS-2026-11-19.md`.
Title: "Questions for Matthew, Thu Nov 19, 2026 (after the usage reset)".
Saved by Prima while you were away (t337u).
The file says to ask them one at a time, each in four parts in its source doc, most important first.
Why this list exists: so the open asks wait in one short file until you can answer.
Where it lives: `docs/review/QUESTIONS-2026-11-19.md`.

1. Who approves an AGENTS.md option? (AGENTS-MANAGER-t333u.md M1.) Proposed: you, on the exact text, after Tester's hostile check. (`QUESTIONS-2026-11-19.md:5`)
2. Which sections are locked in the kernel? (M2.) Proposed: Axioms, Three tests, Evidence, Disagreement, Records, No self-check, Secrets. (`:6`)
3. Build the manager first as `wf agents build|verify`? (M3.) Proposed: yes, move it into the compute core later. (`:7`)
4. Version numbers: the compute gives the next number; a model never picks it; stop and ask if it differs from your words. (LIB-MINE-M2.md Q1.) Proposed: yes. (`:8`)
5. May a model type up your words as the source for an option? (LIB-MINE-M2.md Q2.) Proposed: only after you confirm the typed text; the compute stamps "confirmed by". (`:9`)
6. Can a rule be locked (C9), and the 0000-0009 layout (C10)? (LIB-MINE-M1.md Q1, roadmap section 8.) (`:10`)
7. Joining characters (ZWJ/ZWNJ): wf refuses them, so some emoji combos and some Hindi/Persian words are refused. (WF-90.30.md section 9.) Proposed: keep refusing in names and addresses; decide later for free notes. (`:11`)
8. Board: tool words as columns with body-shop side labels; STALE after 24 hours; log-only first. (WF-BOARD.md Q1-Q3.) (`:12`)
9. Handoff trial: run it (8 runs), the planted line, the answer key, Tester as scorer, read-only workers. (HANDOFF-TRIAL-01.md section 9.) (`:13`)
10. t262u reading: several models working one page at the same time (unanswered card t318s1214). (`:14`)
11. Roadmap conflicts C1-C12 and guard G1-G7 (roadmap sections 8 and 9), as time allows. (`:15`)
12. Disk was 89% full; may Tester's old scratch folders (tester-3003 and others) be deleted? (`:16`)
13. (Added 3:56 PM Eastern Time.) `wf board` is on `board-dev`. Tester flagged that AGENTS.md/README lines which assume the answers to question 8 should not merge into `workflow` until you answer. Proposed: answer question 8, then Prima merges `board-dev` into `workflow`. (`:21`)
14. (Added 4:16 PM Eastern Time.) Log-order check on `harden-dev`: a test page made with two wf versions can get stuck, including resume. No real page has this. Proposed: new writes must follow the order; an already out-of-order page still loads, shows the problem, and allows only resume or a Prime note. No Director ruling yet. (`:24`)
15. The old wf binary `wf-bin/wf-8eb1fdb` can still write and does not know about halt. Proposed: rename it (not delete it) so no one runs it by accident. (`:25`)
16. Merge `harden-dev` into `workflow` together with `board-dev`, after question 14. (`:26`)
17. (Added 5:08 PM Eastern Time.) `harden-dev` ends at `1f32ecb`. Tester passed every round up to `a7f9700` and called the series ready, but has not yet checked this last one-line display fix. A later option: refuse a close whose outcome differs from its signoff. Proposed: yes, after question 14. (`:29`)

Already answered, do not re-ask: Researcher's M2 Q3 (the three safety rules), approved t335s1296 (`QUESTIONS-2026-11-19.md:18`).

Other question lists also exist (`docs/design/OPEN.md`, `docs/design/QUESTIONS-FOR-DIRECTOR.md`, `docs/design/DECISIONS-WAITING.md`).
Those are older or wider lists, not the numbered 1-17 set.

---

## Five disagreements (both sides kept)

I did not pick a winner.

### 1. What the old-lib copy is called, and where it comes from

Side A: the working-tree README in `/workspace/workshop-build/lib-ref` says the branch is `workshop` of `Amalgamour/Librarian`.
It also calls the desk "lib-build: the Workshop development desk".

Side B: the clone's git config and `packed-refs` say `reference/lib-build` of `Amalgamour/Workshop` at `cce5d257`.

Source: inventory, from the lib-ref README, git config, and `packed-refs`.

### 2. The `build` tip and the publish tip do not share a hash

Side A: repo `build` in `/workspace/workshop-build/repo` ends at `488d2ba`.

Side B: publish `origin/prima/build` in `/workspace/workshop-build/publish` ends at `0f7616d`.
The two share a commit message, but not a hash.
Kernel trial docs say publish history is filtered (`docs/trial/kernel-trial-8.md` and neighbours, as cited in the inventory).

Source: inventory, from those two copies and the kernel trial docs.

### 3. Are the `90.x0.00.0001` page ids temporary labels, or already SeqAddr?

Side A: the wf README says v0 page ids are temporary labels, not checked as SeqAddr (`workflow:README.md`, around line 135).

Side B: a Codex triage notes that these ids already look like SeqAddr (`docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md:291`).

Source: those two files, as recorded in the inventory.
I found no single spec table that defines the `90.x0` numbering itself.

### 4. Observer the page role, and Observer the teammate bot

Side A: the wf page role "observer" watches Prime for drift, loops, and stalls (`workflow:README.md`; `docs/design/WORKFLOW-TOOLS.md:15`).

Side B: `docs/design/WORKFLOW-TOOLS.md:38` says the page role "observer" is not the Observer bot that watches this build, and that nothing in your words joins them.

Source: `docs/design/WORKFLOW-TOOLS.md:38`, and the inventory.

### 5. Two workflow-loop spec files sit side by side

Side A: `docs/spec/workflow-loop.md` (291 lines) is one version of the workflow-loop spec.

Side B: `docs/spec/workflow-loop.003.md` (317 lines) is another version.
Drafting notes for version .002 also sit beside them (`docs/spec/workflow-loop.002-notes.md`).

Source: the files in `docs/spec/`, as listed in the inventory.
I did not pick which file is current.
