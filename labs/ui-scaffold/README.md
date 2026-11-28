# UI-1: the workshop front, a kanban design

Builder: Claude. 2026-11-25. Status: `9` (not yet tried by another view).
Brief: docs/plan/WORK-PAGE-2026-11-25-EOW.md:66-84 @ prima/build 5201b243.
This is design only. No file in `app/` is edited.

## Pins

- returns 755d046e: the wf tool. `src/board.rs` is here.
- prima/build 5201b243: the Next.js reader `app/` and the Rust crates `crates/`.
- packs 88be5702: the page files `pages/<addr>/` and each `log.jsonl`.
- "W" means docs/plan/WORK-PAGE-2026-11-25-EOW.md @5201b243.

## What really exists (axiom 9)

- **wf already has a board.** `wf board <page>` prints a page board. `wf board` with no page prints a book board (src/lib.rs:49-50).
- **It reads only, and builds from the log.** "read only, built from the log" (src/board.rs:285).
- **It already has the kanban columns.** Six of them, one per pass tail: Draft, Ready, Working, Waiting check, Checked, Closed (src/board.rs:25-32).
- **Each column names who owes the next move.** For example Ready: "any builder: wf claim" (src/board.rs:27).
- **It already has a card.** `wf board <page> --card NN` prints one pass (src/board.rs:347-400).
- **But it prints text only.** Every line is a `format!` string (src/board.rs:284-305, :357-372). There is no JSON form.
- **The reader app is old.** app/ was last changed Nov 11 (commit 9f5500f3). That is before wf (W:21).
- **The app reads a different store.** It calls the compute crate at `COMPUTE_URL`, port 7700 (app/lib/compute.ts:2). The compute crate reads `books/`, not wf `pages/` (crates/compute/src/lib.rs:130-131, :246-261).
- **wf checks the form of a work address, DD.SS.BB.PPPP, at init.** It uses rules copied from seqaddr-core (src/addr.rs:1-4, :108-123), called at src/cmd.rs:187. It does not look the address up in a compute book.

So the front must join two stores: wf pages (the work) and compute books (the words).
Today nothing joins them.

## One board shape at every level (axiom 2)

The board has one shape: **a level, an address, columns, and cards.**
Each level inherits that shape. It writes only its difference.

| Level | The board is | Its cards are | Its columns are |
|---|---|---|---|
| Book | a book, for example 90.50.10 | its pages | the six pass tails, as counts per page (src/board.rs:486-489) |
| Page | one page, for example 90.50.10.0423 | faces 00-08, plus each 05 pass | faces: one "Faces" lane; passes: the six tails (src/board.rs:25-32) |
| Pass | one pass, for example 05.03 | its jobs w01, w02 ... | the wf card words: accepted, carried, discarded, candidate (src/cmd.rs:14; signoff and close `cards`, 0404 log entry 12 and 22) |

- The card shape is the same at every level: address, holder, step, next, why, ruling id.
- A card at one level opens the board one level down. A page card opens the page board. A pass card opens the pass board.
- This is axiom 2: same shape, and each child writes only its difference.
- It is also axiom 8: each card links up to its parent and down to its children by address.

### The desk

- The desk answers "who holds what, right now".
- Its cards are workers. Each worker card lists the faces it holds and the passes it has claimed.
- A hold is a lockout: page, face, worker, reason, time (src/page.rs:38-46).
- A claim is the claim entry on a pass (src/board.rs:368).
- **Nothing lists holds across pages today.** The book board prints counts only (src/board.rs:486-489). See CONTRACT.md, the desk fields.

## Options

Each option keeps the rule: the Next.js front reads only. The Rust core owns every write (W:72).

### Option A ★ (default): wf gives the board as data, and the front only draws it

- Add a JSON form of `wf board` in a later wf page, for example `wf board <page> --json`.
- It prints the same columns, cards and attention lines that the text board prints today.
- The Next.js front calls it on the server, and draws the one board shape.
- For words (titles, brands, resolve), the front still calls the compute crate, as app/ does today (app/lib/compute.ts:10-13).

Why ★:
- It inherits the board that exists. The columns, the owners and the stale rules stay in Rust (src/board.rs:25-32, :174-218).
- The front writes only the difference: layout and links.
- Nothing is computed twice, so the two cannot drift (axiom 2: "do not reinvent what already exists").

Cost:
- One wf page for `--json`. That touches `src/board.rs`, a busy file. It needs a grant and a free lane.
- A Next.js shell: three screens and one board component.
- Until `--json` lands, the front has nothing live to draw. It can use saved JSON examples.

### Option B: the compute crate learns to read wf pages

- The compute crate gets new routes, for example `/wf/board/:addr`.
- It reads `pages/<addr>/log.jsonl` and builds the board itself.
- The front calls only the compute crate, as the app does today.

Cost:
- The board logic would exist twice: once in wf (src/board.rs) and once in the compute crate. They will drift.
- The compute crate is on prima/build, and wf is on returns. Two branches to change.
- It is one front door, which is simpler for the front.

### Option C: the front reads the text of `wf board` and splits it

- The server runs `wf board` and splits the lines into cards.
- No Rust change at all.

Cost:
- It is the cheapest today.
- It breaks whenever the text changes. The text is made for people, with cuts and caps (src/board.rs:16, :338-340).
- Cut lines would be lost cards. The cap is 40 lines (src/board.rs:16).

## What the screens show

- The fields, and where each one comes from, are in CONTRACT.md.
- Fields with no source today are marked **missing** there.
- The biggest gaps:
  1. The holder on the board is the **claimant**, not the **lock holder** (src/board.rs:368; src/page.rs:38-46). Since 0423, the lock holder is what counts.
  2. No pass carries its own **ruling id**. The pack entry has no ref field (0423 log entry 27, keys). Only `init` and `grant` entries carry one.
  3. **The desk** has no source across pages.
  4. **Faces 00-08** are not on the board. They are files: `pages/<addr>/00.md` to `08.md` (packs 88be5702).

## Not decided here

- Which option. See QUESTIONS.md Q1.
- Where the new front lives. See Q8.
- Every other open choice is in QUESTIONS.md.
