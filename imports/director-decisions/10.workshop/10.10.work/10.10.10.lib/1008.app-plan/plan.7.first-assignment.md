# plan.7 first assignment

version: 002
Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The exact first job, rewritten after 05.01, 05.02 and 05.03. Released by a reply on 05.03 #08.

## Release
This job is released by your reply on `05.03` #08. Until then it is a proposal. Version 001 is kept as `plan.7.first-assignment.001.09.md`.
Release it when the solo-kernel redraft has settled or been committed, so the build reads a stable `clerk` and solo code.

## The job
```text
job: build
stage: 1, batch 1 of 2 to 3. See the work (read-only)
branch: build/2006.batch-desk, made from main at release. Commit only there. Never on main. Never merge.
member: open 2006.batch-desk in band 2000 of 10.10.10.lib (face 01 per 2001.page.README, face 08 to 2000), and its batch 05.01 holding this job's lines
code: app/ at the repo root, beside the desk. Package librarian. Tests in app/tests.
may write: app/**, 10.workshop/10.10.work/10.10.10.lib/2006.batch-desk/**, .gitignore (add .venv/ and .librarian/ only), .venv/ (outside git)
may not write: anything else. Not either kernel. Not jobs.py, clerk.py, clerk.002.py, the solo-kernel code, lcheck.py, rules.toml, moves.toml, AGENTS.md, AGENTS.003.md
read first: 1008.app-plan plan.1, plan.3, plan.4, plan.8; lib/code/jobs.py; lib/code/clerk.py and clerk.002.py if present; solo-kernel code/desk.py, face.py, nav.py, slot.py
solo: not granted. Each line waits for its reply on 2006.batch-desk 05.01
modules: place, tree, and the fixture. face and batch reading are batch 2
```

## How the work is recorded
1. Make the branch `build/2006.batch-desk` from `main`.
2. Open `2006.batch-desk` with face `01` (what compute fills, what the model fills, the test, as `2001.page.README` asks) and face `08` (parent `2000.band.build.page`).
3. Open `2006.batch-desk/05.01.md` in the `1006` shape. One line per piece below, `#NN >build subject`, with `recommend`, `Ask: >build` and the reason, `path`, `scale`, blank `reply:`. Commands come from `plan.8`.
4. Wait for your replies. Work only the lines you released.
5. After each released line: `status:` under your reply with the files, the test output, and the commit. One commit per closed line, message `2006.batch-desk 05.01 #NN <subject>`, only the files that line names.
6. Anything that blocks: a `>stop` line saying where, what was planned, what is needed. Anything found on the way: a `>note` line. Nothing guessed.
7. Before the report: compare `git status` and the branch diff with the `path:` and `status:` lines. Any file no line names is batched as a `>note`.

## The pieces (one line each on 2006.batch-desk 05.01)
1. **Setup.** A project virtual environment `.venv` at the repo root, with `pytest` pinned in `app/requirements-dev.txt`. A `README.md` in `app/` saying how to start Python on this machine (the path found on 2026-10-15) and how to run the tests. `.gitignore` gains `.venv/` and `.librarian/`.
2. **place.** Find the repo root from any folder inside it, by `00.md`, `00.live.md` and the folder `00.00.00.kernel.draft`. Read `00.live`. Hold the kernel names, the no-read list and the no-write list in one place. Shape it for the lookup book, shelf, desk, kernel (`05.03` #05), holding only the desk level now. No machine path in code. No default `who`.
3. **tree.** One address parser taken from `clerk.py` (and `clerk.002.py` if it is there; say which was used), `jobs.py` and solo `face.py`. It names the kind of every folder and file: desk, shelf, book, page, seat face, draft face (`FF.VVV.md`, and the older `FF.VVV.draft.md`), slice (`03.10.md`), retired (`.09`), batch (`05.NN.md`, and the older `05.NN.open.md`, `05.NN.replied.md`, `05.NN.closed.md`, `05.plan.md`), page document (`plan.N.*.md`), furniture, unknown. A walk from `00.md` down, skipping `00.00.00.kernel`, `.git`, `.venv`, `.librarian`, `colab`, `Research`, `downloads`, and zip files.
4. **commands.** `librarian tree [path]` prints the tree with address, title and kind. `librarian where` prints the root, the kernel names and the `00.live` fields.
5. **fixture.** A small hand-made desk under `app/tests/fixtures/desk/`: `00.md`, `00.live.md`, a two-page kernel.draft, one book with a page holding a seat, a draft of each form, a retired face, a batch of each name form, lines using commands from `plan.8` plus one that is not on it, a `>stop` line, a line of solo work (blank reply with a status) under a grant, and a carry chain across two batches. Batch 2 reads the last five; this batch only names their files.

## Tests that must pass
- A table of at least 30 names and their expected kind, including every odd form named in plan.1 and above.
- `where` finds the root from three different subfolders of the fixture.
- A missing `00.md` stops with a message that names the folder.
- A read-only run of `librarian tree` over the real repo: a hash of every file under the tree before and after is identical.
- Every page folder that `find` lists under kernel.draft and the lib book appears in the walk. Any name the parser calls unknown is listed in a `>note` line, not hidden.

## Report
On `2006.batch-desk` `05.01`: a `status:` under each reply, as AGENTS Report: files changed, which `#NN`, overflow, unsure, the branch and the commits. Show the test output. Show `git status` and `git log main..build/2006.batch-desk`. Stop. You read the branch and merge it, or reply with corrections.

## Not in this batch
No batch reading, no reply, no write into the tree outside the new member, no screen. No change to an existing script. No new dependency other than `pytest`. No commit on `main`. No merge.

## Before release
- `AGENTS.md` (002) still says "Never commit". Until `AGENTS.003.md` is seated, this job's `branch:` line is the explicit grant of commit, on that branch only, as `AGENTS.003` itself requires.
- The command list (`plan.8`) is a draft. The build uses it to write its own `05.01` lines and the fixture. If you change the list first, the build follows your version.

### notes
born: 2026-10-15
version 002, from 05.03 #03. Changed from 001: a named branch and a commit per closed line (05.01 #07, 05.03 #07); the build's own 05.01 in the 1006 shape with commands from plan.8 (05.02 #01, #02); >stop and >note instead of guessing; the unseen-work self-check before reporting (05.02 #04); fixture covers commands, >stop, solo work under a grant and carry; place shaped for the rule lookup (05.03 #05); clerk.002.py read if present; member renamed 2006.batch-desk; skips .venv and .librarian. Unchanged: the read-only scope, the modules (place, tree), the tests.
