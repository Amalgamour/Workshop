# UI-1: open questions for Matthew

Builder: Claude. 2026-11-25.
None of these is decided here. Each has a default. The design in README.md assumes the default until Matthew answers.

---

## Q1. Which option builds the front?

README.md, Options.

- **A ★, default: wf gives the board as JSON, and the front only draws it.**
  - Inherits the board that exists (src/board.rs:25-32). Fits axiom 2.
  - Needs a later wf page on `src/board.rs`.
- B: the compute crate learns to read wf pages. The board logic would live twice.
- C: the front splits the text of `wf board`. Cheapest now. Breaks when the text changes.

## Q2. The front reads only. What about the old app's writes?

- The brief says the front reads only (W:72).
- But the old app posts writes: `app/app/api/post/[...path]/route.ts` on prima/build.
- And the compute crate takes writes: `/propose`, `/ask`, `/close` (crates/compute/src/lib.rs:258-261).
- **A, default: the new front has no write button at all. The old app is left as it is, and not edited.**
- B: the new front keeps the old app's write screens, behind the compute crate's token check (crates/compute/src/lib.rs:95).

## Q3. On a card, which "holder" is shown?

- The board prints the claimant (src/board.rs:368).
- Since 0423, the lock holder is what counts (src/page.rs:38-46, :369-386).
- **A, default: show both, with labels: "claimed by" and "lock held by".**
- B: show only the lock holder, and wait for 0424 to change the board (WORK-PAGE-2026-11-25.md:66 @dcdab638).

## Q4. Which copy of a page log does the front read?

- The same page log can differ by branch. 0403 has 12 entries on packs and 9 on returns (labs/review-stage1-route/C1-REVIEW.md, R9).
- wf board reads `pages/` in its run folder (src/board.rs:467).
- **A, default: the packs branch `pages/`, the same as wf board.**
- B: the longer of the two copies, with a mark when they differ.
- C: returns `.workshop/logs/`.

## Q5. What does "desk" mean on this screen?

- The brief says a desk is "who holds what" (W:73).
- The old app already has a desk screen: `app/app/desk/[dd]/page.tsx` on prima/build. That is a desk of books, by its DD part.
- **A, default: the new screen is the workers' desk (holds and claims). The books desk stays a separate screen.**
- B: one desk screen with two tabs.

## Q6. A pass has no ruling id. What does the card show?

- The pack entry has no ref key (0423 log entry 27).
- `init` has `grant_ref` (0403 log entry 1). A `grant` has `ref` (0423 log entry 23).
- **A, default: show the page's grant refs, and mark the pass ruling id missing (`7`).**
- B: a later wf page adds a `ref` to each pack entry.

## Q7. On the book board, which column does a page card sit in?

- A page has many passes, each in its own column.
- The wf book board shows counts per column, not one column (src/board.rs:486-489).
- **A, default: no single column. A page card shows its six counts, as wf does.**
- B: a page sits in the column of its least-finished open pass.

## Q8. Where does the new front live?

- The old app is `app/` on prima/build. wf is on returns. The two branches hold different trees (`git ls-tree` of each: prima/build has `app/` and `crates/`; returns has `src/`).
- The brief says no file in `app/` is edited (W:82).
- **A, default: a new folder, named by Prima when the build is packed. `app/` stays untouched.**
- B: rebuild inside `app/`, after Matthew lifts the rule.

---

## Raised, not a question

- DESIGN.md line 14 says several models may work one page at once. The live rule is one holder (0423). The brief lists this already (W:23). The board design follows the one-holder rule.
