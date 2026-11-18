# Build plan: smallest desk core for the Prime return-review loop (0519.desk-app 05.01)
date: 2026-10-31
who: claude-opus-5-5 (Claude); for Codex Prime to discuss and Colab before any release
state: proposal. Grok builds only packs that Prime prepares and the Director releases.

## Order of value
- **G1 first.** It is read-only, it is useful to Prime the day it lands, and it unblocks nothing else.
- **G0 is a one-line fix.**
- **G2 and G3 are the construction and binding contracts.** They can be built in parallel once Prime accepts the two contracts below.
- **G4 and G5 wire the loop.**

## Contracts to agree first (Prime, with Colab)
- **C1 templates.** The JSON formats of `assignment-spec/1`, `return-pointer/1` (release, claim, execution) and `review-section/1`, the placeholder rule and compare-and-swap. The lab formats in `desk_lab.py` are the starting draft.
- **C2 review binding.** The `prime-cycle-review/3` binding is: assignment-sha256 (bytes before `## Return pointer`), receipt sha256, agreement, review_location, book. /2 records stay readable as historical.
- **C3 page address.** For a member, the page is `<origin.page>/<origin.batch>.md`. A declared exception list covers the 07NN `.pack.md` and `.return.md` layout. A text version `05.NN.VVV.md` is never chosen by number: it is used only when a reservation or a page pointer names it.

## Packs
| Pack | Owns (files) | Depends on | Tests (observable completion) |
|---|---|---|---|
| **G0** state vocabulary | `app/context.py` STATES, `app/tests/test_entry.py` (one case) | nothing | `librarian.py where --root D:/Git/lib-build` exits 0 on a `prepared` record; unknown states still refused. Alternative with no code: Prime writes a known state (D5). |
| **G1** desk view | new `app/desk_view.py`, `app/desk-view.json` (pins), `librarian.py desk` subcommand, `app/tests/test_desk_view.py` | C3 | Disposable book: each state in DESIGN §6 reached once. Legacy review resolution: `evidence/prime-review05.NN/` present means `reviewed-untyped`. Two fresh processes give equal `state_digest`. The live read-only run writes nothing (file list before and after). The 0181 case reads awaiting-review, and 0160 reads reviewed-untyped. |
| **G2** constructor | new `app/construct.py`, `app/construct-templates/` (if any), `librarian.py assign` / construct internals, `app/tests/test_construct.py` | C1 | Placeholder-only edits; refusal on non-placeholder removal, stale compare-and-swap, an existing target or CR. A constructed page reads unambiguous in batch_observe (F2). The Execution line is refused unless the member is complete. Byte-identical output for identical input. |
| **G3** review binding | `labs/prime-cycle-pass02/` (new pass; pass01 stays byte-identical), its tests | C2 | The lab's 8a/8b case reads `reviewed`, not `review-stale`, after the page pointer is written. An assignment edit still makes the review stale. A /2 record reads as historical. Existing 32 tests carried over and passing. |
| **G4** review wiring | `librarian.py review open/record`, `app/review_loop.py`, pins | G1, G2, G3 | One disposable loop: assign, review open, record, page pointer, then the `desk` next action, in fresh processes. The registration is derived from the spec, never hand-typed. |
| **G5** worker entry | `librarian.py task show/release/claim/submit`, `app/task_tools.py` | G2 (and G1 for show) | Worker path without hand-typed lines. The submit run captures, verifies and constructs Execution. A changed handback is refused with nothing written. |

**Parallel:** G0, G1 and the C1/C2/C3 drafting start now. G2 and G3 run in parallel after C1 and C2. G4 and G5 follow, and can be built in parallel with each other (separate files; both call G2).

**Later slices (not prerequisites):**
- Clerk routing and inboxes;
- a browser renderer over `desk --json`;
- more face templates (06 notes, source manifest, the 0401 note);
- a return-band successor (D3);
- canonical seat labels (D4);
- automatic model launch: excluded until separately decided.

## Prime can use now, before any build
- `labs/desk-app-integration-pass01/desk_lab.py view --repo D:/Git/lib-build` lists open reservations and who acts. It is read-only, and was checked on the live book with 27508 files identical before and after.
- Read its `awaiting-review` result together with `evidence/prime-review05.NN/`, since legacy reviews live there (F3).

## Hostile self-review
- **Duplicate engines.**
  - **The concern:** this adds a sixth status reader beside prime_support status, prime_cycle read, batch_observe, desk-state and state-projection.
  - **Mitigation:** G1 composes batch_observe and return_inspect, merges prime_cycle, and parses no page itself. It reads `## Return pointer` only to hash the assignment region.
  - **Alternative considered:** generating a prime_cycle registration for every reservation. Rejected, because the agreement is Prime's judgment and cannot be invented.
  - **Still a risk:** prime_support status overlaps G1. Recommend freezing prime_support for this loop, and not wiring both.
- **Missing handoff records.**
  - **The concern:** before this design, the release, the review address and the next action lived in chat, three addresses and prose.
  - **The design:** each has one record, one address and a pointer.
  - **Remaining:** release authenticity, which is unsolvable without real identity, and stated as such.
- **Stale selectors.**
  - **The concern:** 0401/06.01 is a hand selector. `05.NN.002.md` invites newest-version selection.
  - **The design:** the desk is derived from reservations; C3 forbids number-based choice; 0401 is a note (D5).
  - **Risk:** if 0401 stays, it drifts again. G0 only stops the crash.
- **Unnecessary complexity.**
  - **Could be dropped:** the `batch-page/1` template is the largest item and not strictly needed for the first loop, since Prime can keep writing pages.
  - **Smallest useful construction:** return-pointer plus review-section.
  - **Kept:** `assignment-spec/1`, because it removes page/reservation/registration disagreement, which is the root of F2, F3 and F8.
  - **If time is short:** ship G1 and G3 first, then G2 without batch-page.
- **Concurrency.**
  - **The concern:** live writes from other lanes happened during this assignment.
  - **The design:** compare-and-swap on every constructed page write. No silent merge.
- **Lab is not product.** `desk_lab.py` refuses targets inside the checkout. G1 and G2 need their own scoping rule: the work book only, and never `01NN` members.

## True Director choices, with recommendations
- **D1 review address.**
  - *Recommend:* `<lane>/evidence/prime-review05.NN/<review_id>/` typed record, plus a constructed page pointer.
  - *Alternative:* keep prose REVIEW.md. The cost is that the desk can never tell reviewed from pending.
- **D2 typed reviews mandatory for new passes once G4 lands.**
  - *Recommend:* yes. Legacy passes stay `reviewed-untyped`.
- **D3 return band.** 16 members are left (0184–0199), which is days at the current pace.
  - *Recommend:* decide a declared successor band before 0195. Do not auto-extend.
- **D4 canonical worker labels.**
  - *Recommend:* seat-page ids, with aliases listed on 0408. Reservations use the id.
- **D5 0401/06.01.**
  - *Recommend:* keep it as Prime's human note with a known state, and let `desk` answer "what is current".
  - *Later:* construct 0401 from the desk view.
- **D6 who records the Release line.**
  - *Recommend:* whoever receives the Director's words, constructed verbatim, as practised now. The page records it before work starts.
