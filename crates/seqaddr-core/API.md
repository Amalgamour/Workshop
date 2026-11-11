# seqaddr-core API (for lane COMPUTE and the app)

Rust library, `crates/seqaddr-core`. Deps: serde, serde_json, thiserror. Feature `fs` (default) adds file I/O, the clock and the `seqaddr` CLI; build with `--no-default-features` for wasm32.
Director ruling R1: the full-zero sequence (`00`, `0000`) is the **door**. The API uses that word; older names (`identity_page`, `has_identity`) remain as aliases. R9 narrows R1: sentinels exist only on the desk, shelf, book and page axes; faces and counters have none. R10: face 00 is the registry (`FaceJob::Registry`) and the door page 0000 holds only face 00.

## Errors — `error::SeqError`
Variants: `Invalid`, `Missing` (axiom 7, HTTP 404), `Conflict` (axiom 1, HTTP 409), `Elevate`, `Rejected`, `Corrupt{line}`, `Io`.
Methods: `code()` ("invalid","missing","conflict","elevate","rejected","corrupt","io"), `rule()` (spec id, e.g. "A1.5", "format 4.1", "S11"), `axiom()`, `detail()`, `http_status()`.
Contract body: `{"error": e.code(), "axiom": e.axiom(), "rule": e.rule(), "detail": e.detail()}`.

## Addresses — `addr`
- `Address::parse(&str) -> Result<Address>`: reading only (A1.8). `Address::{Container, Page, ActiveRel}`. `Display` writes it back.
- `Address::expand(&Active) -> Result<Address>`: short form and leading dot (A1.2, A1.6). `Active { book: BookId, pages: Vec<u16> }`.
- `Address::parse_full_page(&str) -> Result<PageAddr>`: requires `DD.SS.BB.PPPP...` (what models and proposals write, A1.7).
- `PageAddr { desk, shelf, book: Option<u8>, page: u16, title, page_tail, face: Option<FacePart> }`; `form()`, `is_full()`, `book_id()`, `expand(BookId)`, `to_form(Form)`, `page_only()`, `slot()` (drops tail/card/title), `tail()`.
- `FacePart { face, counter, tail, card, brand }`. `Tail::{Draft, Retired, Pack, Open, Return, Review}`.
- `ContainerAddr { desk, shelf, book, title }`: `own_book()`, `door_page()`, `level()`.
- `BookId { desk, shelf, book }`: `parse`, `KERNEL`, `lookup_chain()` (book -> shelf -> desk -> kernel), `door_page()`, `file_name()` (`DD.SS.BB.book`), `is_desk_book()`, `is_kernel_or_desk_book()`.
- Classifiers: `sentinel(value, width) -> Option<Sentinel::{Door, Pointer}>`, `is_door`, `axis_role` (`Door/Reserved/Normal/Pointer`), `desk_kind`, `page_kind` (`Door`, `BandHead`, `BandContinuation`, ...), `band_of`, `band_head`, `set_key`, `counter_role` (`Door/Item/Continuation`), `check_title`, `is_tail_word`.

## Faces, cards, axioms
- `face::face_job(ff)` (`Door, Law, Schema, Operate, User, Tasks, Notes, ...`), `is_content_face`, `always_counted`, `default_card_type`, `card_type(name)`, `is_page_type`.
- `cards::parse_face(body) -> FaceDoc { preamble, cards: Vec<Card{heading,key,fields,body}> }`; `FaceDoc::contents()`; `Card::field`, `Card::card_type(face)`; `title_form(heading)`; `parse_stamp(body) -> Stamp` (`title()`, `page_type()`, `get()`).
- `axioms::AxiomChain::parse("1.7.8,3MC")`, `describe()`, `COLD_SET`.

## Book file — `log`
- `BookLog::parse(text)`: header + entries; drops a cut-off last line and a cut-off trailing proposal (`dropped_partial`); damage earlier is `Corrupt`. `to_text()`, `next_n()`, `latest_snapshot()`, `history(addr)`.
- `Entry { n, at, by, op, addr, tail?, from?, to?, body?, proposal?, cites?, outcome?, of?, state?, extra }` — `cites`, `outcome`, `of`, `state` are provisional fields (BUILD-LOG `7`). Unknown fields round-trip in `extra`.
- `Op::{Put, Tail, Snapshot, Copy, Note, Merge, Promote, Use}`; `is_proposed()`.
- `log::file::{read, create, append, repair_tail}` (feature `fs`): `append` repairs a partial tail, writes whole lines, fsyncs. `log::now_utc()`, `format_utc(secs)`, `check_timestamp`.

## State — `state`
- `BookState::replay(&BookLog, &Policy)`, `replay_until(log, n, policy)` (rewind), `apply(&Entry, &Policy)` (all op rules), `snapshot_entry(at, by)`.
- Reads: `page(p)`, `face(p, f)`, `counter(p, f, nn)`, `board(p, f)` (derived listing of a counted face; R9: no `FF.00`), `title()`, `has_door()`.
- `PageState::tail()` (`Live/Draft/Retired`, C1.2/C1.3), `stamp()`, `title()`, `check_c1(page)`.
- `FaceState { seated, draft: Option<Draft{body, notes, n}>, retired, counters }`, `slot_state()`, `view()`.
- `CounterState { tail: CounterTail, bodies, claim: Option<Claim{id, owner, start, n}>, reviewer, returned_by, outcome, ... }`.
- `Policy` (all switches for proposed/provisional rules): `allow_proposed_ops`, `enforce_drafting`, `compute_name` ("compute"), `extra_counted` ([(12,3)]), `c1_on_door_pages`, `draft_counter_put_replaces` (default now **false**), `reviewer_not_builder`, `close_needs_outcome`, `compute_only_steps` (true), `compute_recovery_return` (false), `seat_needs_approval` (true). Build `Policy` with `..Policy::default()`.

## Tails — `tail`
`CounterTail::{Draft, Pack, Open, Return, Review, Closed}` (Closed = bare), `check_counter_move(from, to)`, `check_counter_create`, `PageTail`, `FaceSlotState`.
Counter rules applied in `apply`: first `pack -> open` claims (second gets `Conflict`); `open -> return` only by claim owner or `compute` (body appended to the counter); `return -> review` reviewer != builder (S10); `review -> bare` needs `outcome` in passed/failed/blocked/needs-authority/abandoned; `abandoned` needs a compute system return (S11).

## Finding — `resolve`
- `World { books: BTreeMap<BookId, BookState>, policy }`; `insert`, `get`.
- `World::resolve(&PageAddr) -> Result<Resolution>`; `resolve_str(input, Option<&Active>)`; `resolve_page(&PageAddr) -> BTreeMap<u8, Resolution>`; `check_title(&PageAddr)` (A2.8: mismatch is `Elevate`).
- `Resolution { address, source, origin: Origin::{Local, Shelf, Desk, Kernel, Missing}, found: Option<Found>, trace: Vec<Step{step, checked, found, note}> }`; `state: Option<String>` ("seated", "draft", "retired", "counter", "door"; `Found::state()`); `into_result()` turns Missing into a 404 error. **R5:** at each spot a seated face wins, else a draft is returned as `Found::Draft` (state "draft"), and drafts are inherited book > shelf > desk > kernel. Retired faces are skipped (note "retired"); a retired page, or any page of a book whose door 0000 is retired, is skipped (note "retired page").

## Proposals — `validate`
- `validate(&World, &Proposal, at) -> Outcome`. `Proposal { by, ops: Vec<OpRequest{op, addr, tail?, from?, to?, body?, cites?, outcome?}> }`.
- `Outcome { status: Approved|Rejected, reasons: Vec<Reason{code, rule, axiom?, detail, op?}>, findings, entries, entry_numbers, state }`. Serializes as `{"status","reasons","findings","entries":[n...]}`.
- On approval the compute appends `outcome.entries` with `log::file::append` and replaces the book's state with `outcome.state`. The world is never changed by `validate`. Queue proposals one at a time per book.

## CLI
`seqaddr parse|validate <addr> [--active DD.SS.BB[:PPPP,..]]`, `axioms <chain>`, `replay <file> [--until N]`, `history <file> <addr>`, `resolve <addr> --books <dir> [--active ..]`, `propose <proposal.json> --books <dir>` (dry run). JSON out; exit 1 on error.

## Fix pass (TRIAL-C findings, R2, R4, R5) - what changed for callers

| Change | Migration |
|---|---|
| **R4** plain ASCII: `log::check_plain`, `Entry::check_plain`; `validate` rejects (rule `R4`) any by/addr/tail/from/to/body/outcome/approved_by/trial holding a byte outside 0x20-0x7E + newline; `file::append` refuses; `BookLog::parse`/`file::read` return `Corrupt` ("damaged ... R4") for such a byte or a JSON escape that decodes to one; `repair_tail` refuses to cut it away. | Replace non-ASCII in books (e.g. em dash -> `--`, section sign -> `sec.`). A boot that loads a damaged book must refuse it or report it. |
| **R2** seating needs approval: `OpRequest.approved_by` (serde also `approved-by`) and `OpRequest.trial`. A `promote`, or a bare `put` of a non-counter face, by anyone but `compute_name`, needs `approved_by: "director"`, or `"build-stage (R2)"` plus `trial`. Else rule `E7` (none) / `R2` (bad record). Both are copied into `entry.extra`. Consts `APPROVED_BY_DIRECTOR`, `APPROVED_BY_BUILD_STAGE`. | Pass the record through, or set `Policy.seat_needs_approval = false`. OpRequest literals need `..Default::default()`. |
| `draft -> pack` and `review -> closed` only by `compute_name` (rule `workflow-loop.003 6`). | Have the compute do lint and close, or `compute_only_steps = false`. |
| Compute `open -> return` on another's claim is refused (S11) unless `compute_recovery_return = true`. | Set the flag only in an authorized recovery. |
| `put` on a draft counter is refused (D0 / decisions.md:329). | Use note/merge, or `draft_counter_put_replaces = true`. |
| `replay` checks every snapshot against the replayed state (rule `format 3.4`); a log whose first n > 1 starts at its first snapshot. `replay_from_latest_snapshot` keeps the old fast path. | None for honest logs. |
| R5 resolver (above); trace note "draft only" is gone. | Read `Resolution.state`; treat `Found::Draft` as found. |
| Validation: page 9999 needs a title (A2.8); pointer pages (9999, PP99 >= 0100, books with 99 on an axis) take only faces 00 and 08 (A5.1); a book may not redefine a kernel `owner: kernel-only` card (C1.4); C3.2 may use the inherited 04 face; retiring or changing a back-link is checked against pointers that target it (A5.3). | None. |
| `addr::sentinel(value, width)` handles widths 2, 3, 4 (99/999/9999); other widths -> None. | None. |
| `log::check_timestamp` checks real ranges (month, day incl. leap years, hour, minute, second). | None. |
| `file::repair_tail` empties a file that holds only a cut header; new `file::write_header(path, book)`. | Call `write_header` when the repaired file is empty. |
| `FaceState::is_live` counts a counter only past `draft`, so a page whose content is only drafts (draft counters included) is `PageTail::Draft` (C1.2). | None. |
| Policy field `c1_on_identity_pages` renamed `c1_on_door_pages` (R1). | Rename. |

### Rulings R6-R10 (folded into the fix pass)

| Change | Migration |
|---|---|
| **R9** faces have no sentinels: `FF.00` and `FF.99` fail to parse (rule `R9`); counters run 01-98. `CounterRole` is now `{Item, NotACounter}` (was `{Door, Item, Continuation}`). `sentinel(v, 3)` returns None (brands are not an axis). A counted face is still 05, 06 and `Policy.extra_counted`; nothing depends on an `FF.00`. Plain `FF` on a counted face still resolves to the derived `Found::Board` listing (state `"board"`, was `"door"`; provisional 7). | Drop any `FF.00`/`FF.99` addresses; match `CounterRole::NotACounter`. |
| **R10** face 00 is the registry: `FaceJob::Door` -> `FaceJob::Registry` (name `"registry"`). `validate` rejects any face but 00 on page 0000 (rule `R10`). `Policy.c1_on_door_pages` defaults to false. A pointer that targets a door page finds its back-link as a `target:` line in the door's face 00 (provisional 7). | Write doors as `0000.00` only; retire existing `0000.NN` faces. |
| **R7** overrides: a face written over an inherited face, outside 0001-0009, with no override page in 0001-0009 naming it on a `target:` line, gives an `R7` finding (not a rejection; format 7). New `validate::override_pages(&BookState, target) -> Vec<u16>`. | Write overrides as reserved pages that name their target. |
| **R5 follow-up / R8** `Resolution.why_draft: Option<DraftWhy { opened_by_entry, has_seated, open_notes: Vec<DraftNote{n, by, text}>, merged_notes }>` when a draft is found. Drafts are addressed `...PPPP.FF.draft` and end on promote (R8; unchanged). | Read `why_draft` to show why a face is a draft. |
| **R6** axioms at `00.00.axioms` on the kernel desk: not modelled (address form 7, kernel Q28). | None. |
| **R5 follow-up `reason`** `OpRequest.reason: Option<String>` (optional, R4-checked) is stored as entry field `reason` (`Entry::reason()`); the entry that opens a draft (`copy`, or `put FF.draft` of a new face) puts it in `Draft.reason` (serde default, so old snapshots load) and `DraftWhy.reason`. | Optional: send `reason` when opening a draft. |

### Rulings R12-R18

- **R12** `validate` reports finding `R12` when a face-00 stamp `state:` is not live/draft/retired or disagrees with the derived page state.
- **R14** seating under a draft door is allowed (no change). **R15** brand cards need no 04 (no change).
- **R18** `addr::same_set(a, title_a, b, title_b) -> bool` and `BookState::set_of(p) -> Vec<u16>`: cross-band sets match by CC and title. `set_key` is unchanged (number only).
- **R16** held 7 (conflicts with R9); not modelled.
