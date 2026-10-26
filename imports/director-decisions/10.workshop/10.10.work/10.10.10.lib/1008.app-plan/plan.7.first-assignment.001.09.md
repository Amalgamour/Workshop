# plan.7 first assignment
version: 001

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: retired by version 002, 2026-10-15 (05.03 #03). Never governs. Kept as the record of what was held on 05.01 #13.
page: 1008.app-plan
why: The exact first job, ready to release once the decisions on 05.01 and 05.02 have replies.

## Release
This text is released by your reply on `05.01` `#13`. Until then it is a proposal. If your replies on `05.01` or `05.02` change anything below, the model writes a new version beside this file and asks again on the next batch.

## The job
```text
job: build
stage: 1, batch 1 of 2 to 3. See the work (read-only)
member: open 2006.batch-desk in band 2000 (face 01 per 2001.page.README, face 08 to 2000, a 05.01 batch listing this job's lines), as a draft
code: app/ at the repo root. Package librarian. Tests in app/tests.
may write: app/**, the new member 2006.batch-desk/**, .gitignore (add .venv/ and .librarian/ only), .venv/ (outside git)
may not write: anything else. Not either kernel. Not jobs.py, clerk.py, the solo-kernel code, lcheck.py, rules.toml, moves.toml, AGENTS.md
read first: 1008.app-plan plan.1, plan.3, plan.4; lib/code/jobs.py; lib/code/clerk.py; solo-kernel code/desk.py, face.py, nav.py, slot.py
modules: place, tree, and the fixture. face and batch reading are batch 2
solo: not granted. Every line waits for a reply
```

## What to build
1. **Setup.** A project virtual environment `.venv` at the repo root, with `pytest` pinned in `app/requirements-dev.txt`. A `README.md` in `app/` saying how to start Python on this machine (the path found on 2026-10-15) and how to run the tests.
2. **place.** Find the repo root from any folder inside it, by `00.md`, `00.live.md` and the folder `00.00.00.kernel.draft`. Read `00.live`. Hold the kernel names and the no-read and no-write lists in one place. No machine path in code. No default `who`.
3. **tree.** One address parser taken from `clerk.py`, `jobs.py` and solo `face.py`. It names the kind of every folder and file: desk, shelf, book, page, seat face, draft face (`FF.VVV.md`, and the older `FF.VVV.draft.md`), slice (`03.10.md`), retired (`.09`), batch (`05.NN.md`, and the older `05.NN.open.md`, `05.NN.replied.md`, `05.NN.closed.md`, `05.plan.md`), furniture, unknown. Plan files in this page (`plan.N.*.md`) are named as page documents, not faces. A walk from `00.md` down, skipping `00.00.00.kernel`, `.git`, `colab`, `Research`, `downloads`, and zip files.
4. **commands.** `librarian tree [path]` prints the tree with address, title and kind. `librarian where` prints the root, the kernel names and `00.live` fields.
5. **fixture.** A small hand-made desk under `app/tests/fixtures/desk/`: `00.md`, `00.live.md`, a two-page kernel.draft, one book with a page holding a seat, a draft of each form, a retired face, a batch of each name form, a batch with each `kind:`, a solo-granted batch, and a carry chain across two batches. Batch 2 uses the last three; this batch only names their files.

## Tests that must pass
- A table of at least 30 names and their expected kind, including every odd form found in plan.1.
- `where` finds the root from three different subfolders of the fixture.
- A missing `00.md` stops with a message that names the folder.
- A read-only run of `librarian tree` over the real repo: a hash of every file under the tree before and after is identical.
- Every page folder that `find` lists under kernel.draft and the lib book appears in the walk. Any name the parser calls unknown is listed in the report, not hidden.

## Report
On `2006.batch-desk` `05.01`, a `status:` under each line's reply, as AGENTS Report: files changed, which `#NN`, overflow, unsure. Show the test output. Show `git status`. Anything that stopped the work is a `kind: stop` line. Anything found on the way is a `kind: finding` line. Propose a commit message. Stop.

## Not in this batch
No batch reading, no reply, no write into the tree outside the new member, no screen. No change to an existing script. No new dependency other than `pytest`.
