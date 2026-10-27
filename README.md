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

**New jobs** in this line are page-local batches in the work book `00.kernel/00.00.10.work/`. Read the batch, its `01.md` and its `06.01.md`. The canonical record above selects the current batch; do not infer it from this historical overview. Each return and Prime review stays on its own batch file. `0502.workflow-start/05.01.md` is the accepted previous return. Root [`packs/`](packs) and [`returns/`](returns) keep the bootstrap history. They are not a second copy of a new job.

`00.kernel/00.live.md` is a derived view of the record, rebuilt by a development renderer. If it disagrees with `06.01.md`, the record wins, and the view should be regenerated.

## The desk and its books

| Address | Folder | Holds |
|---|---|---|
| desk `00` (owner address `00.00.00.kernel`) | `00.kernel/` | desk files `00.md`, `00.start.md`, `00.readme.md`, the derived `00.live.md` |
| `00.00.00` syntax | `00.kernel/00.00.00.syntax/` | orientation candidate `00.001.md`; imported reference faces (`01.md`), not locally approved |
| `00.00.01` law | `00.kernel/00.00.01.law/` | orientation candidate `00.001.md`; imported reference faces; new drafts `0041`, `0062`â€“`0065`; amendment drafts for `0018`, `0050`, `0057`; runtime band `0300` with inactive candidates |
| `00.00.10` work | `00.kernel/00.00.10.work/` | designs, assignments, decisions, imports, packs, returns, findings |

Beside the desk:

| Folder | What it is |
|---|---|
| `imports/` | Byte-exact snapshots from pinned Git objects (`source-tree/`), the Director's decision files (`director-decisions/`), and Claude's pass 02 manifests (`claude-pass02/`). Reference only, outside any executable lookup. |
| `packs/` | The packs as delivered, kept byte-exact. |
| `returns/` | Builder returns and Prime reviews. |
| `labs/` | Experiments and the development tooling these packs used, with their evidence. |
| `notes/` | Temporary working notes from before the desk existed. |
| `app/` | Development entry `app/librarian.py`. `where` and `validate` resolve context and run nothing. `test-run` runs one fixture inventory. `bridge-test`, `bridge-status`, and `bridge-recover` run one fixture protocol-test exchange through the pinned lab. `run` refuses. Nothing is seated. |

## Imported instructions are reference, not boot

Old boot files (`00.start.md`, `00.readme.md`, `AGENTS.md` and others under `imports/`) and the imported reference faces may still name old paths such as `D:\Git\Librarian-rebuild` or `00.00.00.kernel.draft`. They are historical sources for new drafts. Don't follow them as instructions. `AGENTS.004.md` at the root is a **draft** for the Director's review. It is not in force.

## What is missing

- No seated loader, and no active `02.<name>.py` on any runtime page. The development entry can hash-check `0302.run/02.run.003.py` and run one fixture payload. `run` refuses. The law card still names `02.run.py`, which does not exist.
- Clerk routing (inboxes, handoffs between seats) is not integrated. Seats currently hand work over manually through page-local `05.NN` batches and their returns; root `packs/` and `returns/` retain bootstrap history.
- Lock and release are not implemented. No orientation face is seated.
- The renderer for `00.live.md` is development tooling in `labs/bootstrap-establish-pass01/`, not a runtime module.

## Byte custody

`.gitattributes` keeps `/imports`, `/labs`, `/notes`, `/packs`, `/returns` and `/00.kernel` byte-exact (`-text`). New app and control text is LF. `.gitignore` excludes only generated scratch repositories. See `0410.imports`, and addendum 001 #B-A03, for how every Git boundary was checked.

## Development status â€” 2026-10-27
The development entry can hash-check `0302.run/02.run.003.py` and run one fixture inventory. It can also submit one fixture job to the accepted local process adapter, print a verified artifact and a durable receipt, read that receipt from a fresh process, and replay the same job without a second launch. The worker kind is `protocol test worker`. Collection is not approval. No model connection is active. The lab at `labs/worker-bridge-pass01` is unchanged. `run` refuses. AR-01's pre-existing output name is still refused before an inventory payload runs. The advisory book checker is accepted on 0502/05.03. The Observer's first manual review and Prime responses are 0502/06.02. No continuous Observer process exists. Nothing is seated or activated.

## Latest review disposition â€” app 05.05 / Clerk 05.01
The app now implements a fixture-only worker exchange, but acceptance is blocked
by stored-receipt correlation BRI-01 (0504/05.06). AR-01/AR-02 were repaired and
accepted on 0504/05.04. The separate file-backed Clerk loop works in its demo but
needs the reviewed corrections on 0506/05.02. No model connection is active.
The Observer independently publishes periodic advisory notes on observer/reviews;
Prime intake is manual during work sessions, not an automatic dispatcher.

## Latest corrected-component checkpoint — app 05.06 / Clerk 05.02
BRI-01's persisted-receipt mutation is now refused; the fixture-only correction
passed independent app and entry suites. Clerk schema 2 passes the relocated
suite and isolated-loss probes, with independent lead review still due before
integrated acceptance. The completed seam design needs read-only show --json
(0506/05.04) before implementation; it is not a deployed connection. Active
Prime-support work is separate and is not included by this checkpoint.
