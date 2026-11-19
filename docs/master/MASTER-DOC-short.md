# Workshop master document (short draft)
For Matthew, the Director. Same facts as the long draft at `/workspace/workshop-build/scratch/MASTER-DOC-draft.md`. Date: Thu 19 Nov 2026, morning, America/Toronto (Eastern Time).
This is a draft. It is not a ruling. It is not a commit. If two sources disagree, both sides are at the end. I did not pick a winner.

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
## Branches
`workflow`, `board-dev`, and `harden-dev` are branches of `/workspace/workshop-build/repo`. `prima/build` and `reference/lib-build` are not; they live in other copies. This repo has no remotes set.
`workflow` — source of the wf tool and the line meant to be the next published wf kit; same tip as `wf-next`; last commit restores a return step so old records can stay (axiom 6); not the core or books tree. Path: branch of `/workspace/workshop-build/repo`, tip `a00bc53`; also `/workspace/workshop-build/workflow`.
`board-dev` — a wf branch that adds the read-only work board (`wf board`); Tester's fixes are in (no panic on a missing pass, card lines name their source, escapes, flags); not merged into `workflow` yet (open question 13); so you can see what needs someone, what is moving, and what passed, in under a minute. Path: tip `193da07`, worktree `/workspace/workshop-build/scratch/board-dev`.
`harden-dev` — a wf branch that checks log order and escapes hostile text in observer output; last commit escapes close-outcome words in the observe loop line; Tester has not yet checked that last commit (open question 17); not merged yet (open questions 14 and 16); so a messy or hostile log cannot break the record or the display. Path: tip `1f32ecb`, worktree `/workspace/workshop-build/scratch/harden-dev`.
`build` — the main Workshop build: the Rust core, the books, the kernel, the reader app, and the docs in `docs/`; last commit is a review note on the harden-dev end state and a close-outcome option, for Nov 19. Path: current branch of `/workspace/workshop-build/repo`, tip `488d2ba`.
`prima/build` — the GitHub publish name for the clean `build` line, not a branch of the repo; a local copy's branch `build` tracks `origin/prima/build` (tip `0f7616d`); it shares a commit message with repo `build` `488d2ba`, but not the same hash (disagreement 2); kernel trial docs say publish history is filtered, and a push goes only to `prima/build`. Path: `/workspace/workshop-build/publish`.
`reference/lib-build` — the branch of the old-lib copy, not a branch of the repo; `packed-refs` and `HEAD` name it at `cce5d257` (also packed as `origin/clean`); the README and the git config disagree on the GitHub name (disagreement 1); empty folders `.git/refs/heads` and `.git/refs/tags` were added so git can run; no fetch, reset, delete, overwrite, or checkout was done; a pinned copy of the old lib build, for reference and mining. Path: `/workspace/workshop-build/lib-ref`.
217 files are missing from the lib-ref copy on disk, mostly old evidence and output (`git status` shows them as deleted, probably from the Nov 18 snapshot restore); we are leaving them as they are, because the copy is only a reference and `git show cce5d257:path` still reads every one.
`wf-next` — the same commit as `workflow`; a worktree used to develop wf. Path: tip `a00bc53`, worktree `/workspace/workshop-build/wf-run/wfdev`.
`bench` — a wf branch that adds a small bench crate and a baseline on page `90.10.00.0001`, so speed can be measured against a known page. Path: tip `5cc2a93`, worktree `/workspace/workshop-build/bench`.
`core-wf` — the core "write once" line; same tip as `pass/90.20.00.0001.05.05`; the tree matches `build` (crates, books, kernel, app). Path: tip `2f66bda`, worktree `/workspace/workshop-build/wf-run/core`.
`merge-rehearsal` — a practice merge of `harden-dev` (`1f32ecb`) after `board-dev`, dated 19 Nov 2026; not the live `workflow` branch. Path: tip `6bd4b17`, worktree `/workspace/workshop-build/scratch/merge-rehearsal`.
`pass/90.20.00.0001.05.01` (`f363e28`) through `.05.05` (`2f66bda`) — frozen builder-return branches for the "write once" page (delivery ids, restart, first-write-wins, records, then the fix-up), so each pass can be opened again later (axiom 6). Path: branches of `/workspace/workshop-build/repo`.
`pass/90.30.00.0001.05.01` (`2a6aa0a`) through `.05.04` (`84cecd4`) — frozen builder-return branches for the "wf ready for next week" page (halt and resume, a return-file note, pack templates, and the category table and escapes), so each pass can be opened again later. Path: branches of `/workspace/workshop-build/repo`.
No other local branch names were present. Leftover detached worktrees under `scratch/` (old tester copies) are not branches.
## The wf tool and commands
`wf` — a small command-line tool that runs one work page and keeps the record; people and models ask it and do not edit page files by hand; the log `pages/<page>/log.jsonl` is the truth, and page files are copies printed from it; a hand edit makes wf refuse to go on; so the compute, not a model, keeps the rules and the record. Source: branch `workflow` (`workflow:README.md` and `workflow:src/`, including `src/lib.rs`, `src/cmd.rs`, `src/page.rs`). Pinned binary: `/workspace/workshop-build/wf-bin/wf`, built from `a00bc53`. Older binary: `/workspace/workshop-build/wf-bin/wf-8eb1fdb` (open question 15 asks to rename it so no one writes with it by accident). Every command that writes needs `--as <name>` (or `WF_AS`). Root folder: the current folder, or `WF_ROOT`. Commands below are in the pinned binary and on `workflow` (source: `wf --help`, `workflow:README.md`, and help text in `workflow:src/lib.rs`).
`init-page` — start a page: title, person, prime, and the grant (which files may be touched), with a grant ref.
`set-prime` — change who the Prime is, with a ref.
`grant` — widen the grant (more paths), with a ref; optional `--answers` ties it to an answer entry.
`face-write` — write text onto a face (01, 02, 04, 06, or 08); face 04 needs a section: goals, decisions, or responses; text may come from `--text` or `--file`.
`draft` — Prime writes the plan for a pass; wf pins what Prime read (faces 04 and 06, and the last closed 05); `--pass` can redraft a pass that is not packed yet; `--overlap-ok` lets a new draft start while another packed pass is still open, with a why and a ref.
`pack` — Prime releases the plan; wf checks it, then prints the job box for the builder.
`claim` — a builder takes the job; first claim wins, so two builders cannot take the same job.
`return` — the builder pings wf with the branch, the commit, and the return file; wf checks the files against the grant.
`check` — the checker (never the builder) runs the pack's tests; `--dry-run` prints the result and writes nothing; `--note` or `--fail` can be added.
`signoff` — Prime records the outcome: passed, failed, blocked, or needs-authority; cards can be named (`w01=accepted`, and so on); a note with a ref is needed for some hard cases.
`close` — write the close record after signoff; the same refusals as a passed signoff are run again, so a close is checked twice.
`elevate` — send a stuck item up to Prime or to the person, instead of forcing it through.
`answer` — answer an elevated item, by entry number, so the answer is tied to the item that went up.
`halt` — Prime or the person stops the page (refused while a pass is open); after a halt, draft, pack, and claim refuse.
`resume` — Prime or the person lets draft, pack, and claim go on again, with a record.
`status` — read only; show where the page stands, built fresh from the log.
`observe` — observer signals (stall hours, loops); `--record` files a finding; read-mostly, `--record` writes.
`verify` — check the log chain and every view file; `--fix` reprints missing or changed views from the log.
`board` — extra command, not in the pinned binary: a read-only work-order board (no log write, no view write, no lock, and it does not run git); `wf board` lists every page in one line; `wf board <page>` shows attention first, then columns; `--card NN` shows one pass, with each line naming its source; `--all` shows lines past the usual 40-line cap; `--stall-hours` defaults to 24; marked "build stage, pending Director answer" (open questions 8 and 13). Path: only on `board-dev` (and in the `merge-rehearsal` merge). Source: `board-dev:README.md` and `docs/design/WF-BOARD.md`.
## Pages 90.x0.00.0001
I found no single definition table for the `90.x0` pattern in `docs/spec`. The wf README says v0 page ids are temporary labels, not checked as SeqAddr (`workflow:README.md`, around line 135). A Codex triage notes that these ids already look like SeqAddr (`docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md:291`). Both are recorded (disagreement 3). Live pages sit under `/workspace/workshop-build/wf-run/pages/` (not inside the `build` tree). Title and grant come from each page's `00.md` view, which wf printed from the log.
`90.10.00.0001` — title "workflow kit"; the first real wf page (also called the dogfood page); 85 log entries; person Matthew, Prime Prima; grant: src, tests, templates, docs, examples, README, AGENTS, Cargo.toml (from t267u); to run and prove the wf kit on a real page, and the baseline for board tests and the core-via-wf plan. Path: `/workspace/workshop-build/wf-run/pages/90.10.00.0001/`. Also in `docs/design/PLAN-2026-11-18-core-via-wf.md:6` and `docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md`.
`90.20.00.0001` — title "core: write once"; the page that added delivery ids and write-once rules to the core; 49 log entries; grant: `crates/compute/`, `crates/seqaddr-core/`, `docs/CONTRACT.md`, `docs/BUILD-LOG.md` (from t285u); so a write is kept once, and a replay is safe. Path: `/workspace/workshop-build/wf-run/pages/90.20.00.0001/`. Spec: `docs/spec/WRITE-ONCE.md`. Journal: `docs/journal/2026-11-18-write-once.md`.
`90.30.00.0001` — title "wf: ready for next week"; the page that made wf ready for the next stretch (halt, resume, templates, escapes); 37 log entries; grant: src, tests, templates, README, AGENTS, examples (from t267u). Path: `/workspace/workshop-build/wf-run/pages/90.30.00.0001/`. Spec: `docs/spec/WF-90.30.md`. Journal: `docs/journal/2026-11-18-wf-90.30.md`.
`90.40.00.0001` — case A, "Sound successor" (control); the pack restates the goal and links the earlier failed pass; the clean case, to compare with the others. These four `90.40` pages are planned only (no `90.40*` folder under `wf-run/pages/`); a handoff trial in `docs/design/HANDOFF-TRIAL-01.md`, not live work pages. Planned in `docs/design/HANDOFF-TRIAL-01.md:28`.
`90.40.00.0002` — case B, "Lost context"; the pack says only "fix the clamp"; the real reason lives only in the earlier pass; to see what happens when the new pack hides the why. Planned in `docs/design/HANDOFF-TRIAL-01.md`.
`90.40.00.0003` — case C, "Deliberate deletion"; a later pass drops a job on purpose, with a recorded reason. Planned in `docs/design/HANDOFF-TRIAL-01.md`.
`90.40.00.0004` — case D, "Planted bad line"; same as A, but a bad line is planted in AGENTS.md to see if a worker follows it. Planned in `docs/design/HANDOFF-TRIAL-01.md`.
I found no live or planned `90.00`, `90.50`, or higher in the repo docs or under `wf-run/pages/`.
## Files in docs/spec
Path root: `/workspace/workshop-build/repo/docs/spec/`. These are the governing specs. Where a contract and a spec disagree, the spec wins (`docs/CONTRACT.md`).
`AGENTS.md` — early Workshop instruction notes (business wants and a few technical rules, such as keep the why); not the wf kit `AGENTS.md` on the `workflow` branch. `Axioms.md` — the nine axioms in short form. `DIRECTOR-RULINGS.md` — your rulings given in chat; these outrank older spec wording. `Design.md` — the system overview; it points to the other specs, and says each rule lives in exactly one of them. Path: `docs/spec/`.
Address and page shape, all in `docs/spec/`: `seqAddr.md` (the geometry: addresses, faces, cards, page layout, and grammar), `seqpage.md` (the `.seq` page file itself), `SEQ-GUIDE.md` (a reader's guide to the `.seq` file, written for you), `seqpage-QUESTIONS.md` (open questions about the `.seq` file), `format.md` (how a book is stored), `face00.md` (Face 00: the stamp, the page type, and the registry), `drafting.md` (how a face is changed; the principle is settled, enforcement is still proposed), `brands.md` (how brands fit together; rules live in `decisions.md`), `decisions.md` (working record of seqAddr decisions and their reasons).
Work from recent pages, all in `docs/spec/`: `WF-90.30.md` (the wf tool on `workflow` at `a00bc53`, from page `90.30.00.0001`), `WF-BOARD-AND-LOG-ORDER.md` (the board work and the log-order check, on two builder branches not yet merged into `workflow`), `WRITE-ONCE.md` (write-once and delivery ids in the core, from page `90.20.00.0001`; draft choices in it wait for you as K4; it describes code on `build` / `core-wf`).
`workflow-loop.md` (291 lines) and `workflow-loop.003.md` (317 lines) are two versions of the workflow-loop spec (how a pass moves from plan to close); I list both and did not pick which is current (disagreement 5). `workflow-loop.002-notes.md` keeps drafting notes and a read-back for loop version .002. Path: `docs/spec/`.
`kernel-design.md` — design draft for the kernel (the first book and how it is built). `review.md` — a condensation review of the older `claude` branch, kept as background. Path: `docs/spec/`.
Examples in `/workspace/workshop-build/repo/docs/spec/examples/`, so the format can be seen and checked: sample pages seqaddr (`00.00.00.0051`), bob (`10.11.21.1001`), timer (`10.11.30.1501`); face00 samples workshop, dictionary, dev, ide-design, and cats; proposal cuts of bob and a short "cats"; a real bob page exported from a book (`examples/real/README.md` says the "real" `.seq` files were exported by the seqpage tool from `books/`); source books `00.00.00`, `10.11.21`, `10.11.30`, and `10.11.40`.
## Files in docs/journal
Path root: `/workspace/workshop-build/repo/docs/journal/`. These tell the story of how a page was built, in plain order, so the team can see what happened and why.
`2026-11-18-write-once.md` — the story of page `90.20.00.0001` (core write once), including the five passes and what Tester found. Path: `docs/journal/2026-11-18-write-once.md`.
`2026-11-18-wf-90.30.md` — the story of page `90.30.00.0001` (wf ready for next week), including halt, templates, and the escape work. Path: `docs/journal/2026-11-18-wf-90.30.md`.
`2026-11-18-wf-board-and-log-order.md` — the story of the board branch and the log-order check on `harden-dev`, including Tester's rounds. Path: `docs/journal/2026-11-18-wf-board-and-log-order.md`.
## Files in docs/review
Path root: `/workspace/workshop-build/repo/docs/review/`. These are checks, outside reviews, and your exact words, kept so the team can cite them later.
Codex reviews, all under `docs/review/`: `CODEX-LIB-BUILD-REPORT-t323u.md` (old lib build, t323u), `CODEX-LIBRARIAN-TOOLS-REVIEW.md` (how Codex Prime built, used, and tested Librarian's tools), `CODEX-MANAGER-DRAFT-t304u.md` ("Workshop Manager and the First Desk Trial", word for word), `CODEX-PLAN-REVIEW-t292u.md` (core-via-wf plan, t292u), `CODEX-WF-REVIEW-t275u.md` (wf kit review, t275u), and `CODEX-WF-REVIEW-t275u-TRIAGE.md` (Prima's triage: what to fix, what to park).
Tester checks, advice only, not rulings, all under `docs/review/`: `CORE-SPEC-HOSTILE-PASS.md`, `DEV-WORK-LAB-PAGES-CHECK.md`, `FACE-05-D6-CHECK.md`, `PACK-TEMPLATE-CHECK.md`, `WORK-BOOK-AXIOM-CHECK.md`, `WORK-BOOK-CONCEPT-CHECK.md`, and `WORK-BOOK-HOSTILE-PASS.md`.
Other reviews, all under `docs/review/`: `CORE-SPEC-REVIEWS-t210u.md` (outside reviews of the core-and-tools spec, t210u), `CURSOR-BUILD-REVIEW.md` (Cursor's Workshop build, branch `cursor/build`), `OUR-CODE-VS-CURSOR-LESSONS.md` (our code compared with lessons from that build), `SAMPLE-PAGE-CLAUDE-REVIEW-t253u.md` and `SAMPLE-PAGE-CODEX-REVIEW-t252u.md`, `PRIMA-REVIEW-MANAGER-DRAFT-t304u.md` (Prima's review of the Codex manager draft), `DIRECTOR-AGENTS-DRAFT-t332u.md` (your AGENTS.md draft, word for word), `WORK-BOOK-RESEARCH.md` (how AGENTS.md is used in Cursor and in Grok Build), and `QUESTIONS-2026-11-19.md` (open questions 1-17; see below).
Your exact words, one file per chat, under `docs/review/DIRECTOR-WORDS-*.md`, so the team does not rely on memory: t212u, t223u, t226u, t227u, t239u (what each face of a work page holds), t240u-t241u, t243u, t245u, t246u, t249u, t250u, t254u, t255u, t259u, t261u, t262u (several models at one page), t263-T6 (checker and observer as roles), t267u, t268u, t285u, t301u, t303u, t305u, t306u, t306s1163, t307u, t309u (guard the compute, so an observer can check), t310u, t311u, t312u, t316u (t314u and t316u; the mining-authorized note used for Researcher task M2), t326u, t327u, t328u, t329u, t333u (AGENTS manager design), t335u (Designer may work with Researcher on a task Prima approves; Researcher is Prima's assistant first), and t335s1296 (the three safety rules, already answered).
Drawings, not text, in `docs/review/`: `DIRECTOR-DRAWING-t261u.png` and `DIRECTOR-DRAWING-t262u.png` — your drawings of the page and the compute.
Scripts in `docs/review/t275u-repro/`, so a finding from the t275u Codex wf review can be shown again: `lib.sh` (shared setup), `chain.sh` (hash-chain limits), `p1-init.sh` (two inits at once), `p1-loop.sh` (two plain claims together), `p1-race.sh` (two claims, one paused mid-load), `p2-signoff.sh` (passed signoff while blocked with an open elevation), `p3-donewhen.sh` (face 01 changes after pack), `p4-views.sh` (missing or unreadable views), `p5-changed.sh` (the return's free-text `changed:` line), `seqaddr.sh` (any label as a page id, and pass numbers past 98), `why-spots.sh` (choices that should need a why, but do not yet).
## Teammate bots and roles
I only state a role when a repo doc supports it. Page roles in the wf tool (person, Prime, builder, checker, observer) are not the same thing as teammate bot names. One doc warns that the page role "observer" is not the Observer bot that watches this build, and that nothing in your words joins them (`docs/design/WORKFLOW-TOOLS.md:38`). See disagreement 4.
Prima — repo docs call Prima the Prime (team lead) of the wf pages (`workflow:README.md`; each live page's `00.md` lists `prime: prima`); Prima authors many build commits and writes the specs and journals; the words "chief engineer" were not found in repo docs; an older lib note says that in the first Prima pilot, Prima was Codex's assistant, not the Prime (`docs/reference/LIB-BUILD-SURVEY.md:140`); that is old-lib history, not today's wf role; both are recorded. Role written in `workflow:README.md`, live page `00.md` files, and many docs under `docs/`.
Prima Worker A and Prima Worker B — role not in repo docs (no hits for "Worker A", "Prima Worker", or "Worker B").
Observer — the wf page role watches Prime for drift, loops, and stalls (`workflow:README.md`; `docs/design/WORKFLOW-TOOLS.md:15`); the Observer bot that watches this build is named as a distinct thing in `WORKFLOW-TOOLS.md:38`; I found no fuller bot-role file.
Tester — checks work and designs, often with a hostile pass; never the builder; often signed "Tester (Grok Bot)"; a different view must check the work. Role written in `docs/review/*CHECK*`, the journals, and `docs/design/HANDOFF-TRIAL-01.md` (Tester as scorer).
Designer — "design partner for Prima"; writes design docs; you are the only approver. Role written in `docs/design/SEQ-FILE-PLAN.md:4`, `docs/design/SECTIONS-AND-CARDS.md:4`, `docs/design/CORE-AND-TOOLS-SPEC.md:4`, and many other `docs/design/` pages.
Researcher — Prima's assistant first; may work with Designer directly only on a task Prima approves (`docs/review/DIRECTOR-WORDS-t335u.md:7-9`); also named as the author of the lib-mine notes (`docs/reference/LIB-MINE-M2.md:4`). Role written in those two files.
Rando Bot and Buildabot — role not in repo docs (no hits).
SM-Bot and Gameatron — only in the old-lib survey; no today's-team role is stated. SM-Bot: an idea that Observer would hand work to "the SM-bot for posts"; the posting idea is not in the roadmap (`docs/reference/LIB-BUILD-SURVEY.md:173`). Gameatron: a handoff file in the first Prima pilot (`docs/reference/LIB-BUILD-SURVEY.md:73,140`).
## Open questions 1-17 (source: `docs/review/QUESTIONS-2026-11-19.md`; saved by Prima while you were away, t337u; ask one at a time, each in four parts in its source doc, most important first)
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
Already answered, do not re-ask: Researcher's M2 Q3 (the three safety rules), approved t335s1296 (`QUESTIONS-2026-11-19.md:18`). Other question lists also exist (`docs/design/OPEN.md`, `docs/design/QUESTIONS-FOR-DIRECTOR.md`, `docs/design/DECISIONS-WAITING.md`); those are older or wider lists, not the numbered 1-17 set.
## Five disagreements (both sides kept; I did not pick a winner)
1. What the old-lib copy is called, and where it comes from — Side A: the lib-ref README says the branch is `workshop` of `Amalgamour/Librarian`, and calls the desk "lib-build: the Workshop development desk". Side B: the clone's git config and `packed-refs` say `reference/lib-build` of `Amalgamour/Workshop` at `cce5d257`.
2. The `build` tip and the publish tip do not share a hash — Side A: repo `build` in `/workspace/workshop-build/repo` ends at `488d2ba`. Side B: publish `origin/prima/build` in `/workspace/workshop-build/publish` ends at `0f7616d`; they share a commit message, but not a hash; kernel trial docs say publish history is filtered (`docs/trial/kernel-trial-8.md` and neighbours).
3. Are the `90.x0.00.0001` page ids temporary labels, or already SeqAddr? — Side A: the wf README says v0 page ids are temporary labels, not checked as SeqAddr (`workflow:README.md`, around line 135). Side B: a Codex triage notes that these ids already look like SeqAddr (`docs/review/CODEX-WF-REVIEW-t275u-TRIAGE.md:291`). I found no single spec table that defines the `90.x0` numbering itself.
4. Observer the page role, and Observer the teammate bot — Side A: the wf page role "observer" watches Prime for drift, loops, and stalls (`workflow:README.md`; `docs/design/WORKFLOW-TOOLS.md:15`). Side B: `docs/design/WORKFLOW-TOOLS.md:38` says the page role "observer" is not the Observer bot that watches this build, and that nothing in your words joins them.
5. Two workflow-loop spec files sit side by side — Side A: `docs/spec/workflow-loop.md` (291 lines) is one version. Side B: `docs/spec/workflow-loop.003.md` (317 lines) is another version; drafting notes for version .002 also sit beside them (`docs/spec/workflow-loop.002-notes.md`). I did not pick which file is current.
