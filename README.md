# lib-build: the Workshop development desk

**State:** provisional entry, written by Pack B (`lib-build-bootstrap-pass01`, with addendum 001) on 2026-10-26.
**Status:** the desk is established. Runtime is NOT active. Nothing here is approved, seated or locked.
**Branch:** `workshop` of `github.com/Amalgamour/Librarian`. `main` holds the accepted record, and only the Director merges into it.

## Start here

1. **The current assignment** is the canonical record [`00.kernel/00.00.10.work/0401.goal/06.01.md`](00.kernel/00.00.10.work/0401.goal/06.01.md). It names the desk, the book, the workflow space, the current work, what it waits on, and the assignment state.
2. **The goal** is [`00.kernel/00.00.10.work/0401.goal/01.md`](00.kernel/00.00.10.work/0401.goal/01.md): this workspace's finish line, then runtime adaptation, then activation and a real cold-model test.
3. **Who sits where:** [`0408.seats`](00.kernel/00.00.10.work/0408.seats/01.md). **What the Director decided:** [`0409.decisions`](00.kernel/00.00.10.work/0409.decisions/01.md).
4. **What was imported, and its status:** [`0410.imports`](00.kernel/00.00.10.work/0410.imports/01.md). **Open findings:** [`0611.findings`](00.kernel/00.00.10.work/0611.findings/01.md).
5. **The bootstrap record**, with the packs, their outcomes and the evidence: [`0501.bootstrap`](00.kernel/00.00.10.work/0501.bootstrap/01.md).

**New jobs** in this line are page-local batches in the work book `00.kernel/00.00.10.work/`. Read the batch, its `01.md` and its `06.01.md`. The current batch is [`0502.workflow-start/05.01.md`](00.kernel/00.00.10.work/0502.workflow-start/05.01.md). Its return and the Prime review stay on that file. Root [`packs/`](packs) and [`returns/`](returns) keep the bootstrap history. They are not a second copy of a new job.

`00.kernel/00.live.md` is a derived view of the record, rebuilt by a development renderer. If it disagrees with `06.01.md`, the record wins, and the view should be regenerated.

## The desk and its books

| Address | Folder | Holds |
|---|---|---|
| desk `00` (owner address `00.00.00.kernel`) | `00.kernel/` | desk files `00.md`, `00.start.md`, `00.readme.md`, the derived `00.live.md` |
| `00.00.00` syntax | `00.kernel/00.00.00.syntax/` | orientation candidate `00.001.md`; imported reference faces (`01.md`), not locally approved |
| `00.00.01` law | `00.kernel/00.00.01.law/` | orientation candidate `00.001.md`; imported reference faces; new drafts `0041`, `0062`–`0065`; amendment drafts for `0018`, `0050`, `0057`; runtime band `0300` with inactive candidates |
| `00.00.10` work | `00.kernel/00.00.10.work/` | designs, assignments, decisions, imports, packs, returns, findings |

Beside the desk:

| Folder | What it is |
|---|---|
| `imports/` | Byte-exact snapshots from pinned Git objects (`source-tree/`), the Director's decision files (`director-decisions/`), and Claude's pass 02 manifests (`claude-pass02/`). Reference only, outside any executable lookup. |
| `packs/` | The packs as delivered, kept byte-exact. |
| `returns/` | Builder returns and Prime reviews. |
| `labs/` | Experiments and the development tooling these packs used, with their evidence. |
| `notes/` | Temporary working notes from before the desk existed. |
| `app/` | Reserved for the application. Nothing is implemented there yet. |

## Imported instructions are reference, not boot

Old boot files (`00.start.md`, `00.readme.md`, `AGENTS.md` and others under `imports/`) and the imported reference faces may still name old paths such as `D:\Git\Librarian-rebuild` or `00.00.00.kernel.draft`. They are historical sources for new drafts. Don't follow them as instructions. `AGENTS.004.md` at the root is a **draft** for the Director's review. It is not in force.

## What is missing

- No seated loader, and no active `02.<name>.py` on any runtime page. The candidates are named `02.<name>.VVV.py`, and the cards say they can't be executed yet.
- Clerk routing (inboxes, handoffs between seats) is not integrated. Seats hand work over through files in `packs/` and `returns/`.
- Lock and release are not implemented. No orientation face is seated.
- The renderer for `00.live.md` is development tooling in `labs/bootstrap-establish-pass01/`, not a runtime module.

## Byte custody

`.gitattributes` keeps `/imports`, `/labs`, `/notes`, `/packs`, `/returns` and `/00.kernel` byte-exact (`-text`). New app and control text is LF. `.gitignore` excludes only generated scratch repositories. See `0410.imports`, and addendum 001 #B-A03, for how every Git boundary was checked.
