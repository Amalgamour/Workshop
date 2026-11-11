# seqaddr-core API (for lane COMPUTE and the app)

Rust library, `crates/seqaddr-core`. Deps: serde, serde_json, thiserror. Feature `fs` (default) adds file I/O, the clock and the `seqaddr` CLI; build with `--no-default-features` for wasm32.
Director ruling R1: the full-zero sequence (`00`, `0000`) is the **door**. The API uses that word; older names (`identity_page`, `has_identity`) remain as aliases.

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
- Reads: `page(p)`, `face(p, f)`, `counter(p, f, nn)`, `board(p, f)` (the derived `FF.00` door), `title()`, `has_door()`.
- `PageState::tail()` (`Live/Draft/Retired`, C1.2/C1.3), `stamp()`, `title()`, `check_c1(page)`.
- `FaceState { seated, draft: Option<Draft{body, notes, n}>, retired, counters }`, `slot_state()`, `view()`.
- `CounterState { tail: CounterTail, bodies, claim: Option<Claim{id, owner, start, n}>, reviewer, returned_by, outcome, ... }`.
- `Policy` (all switches for proposed/provisional rules): `allow_proposed_ops`, `enforce_drafting`, `compute_name` ("compute"), `extra_counted` ([(12,3)]), `c1_on_door_pages`, `draft_counter_put_replaces`, `reviewer_not_builder`, `close_needs_outcome`.

## Tails — `tail`
`CounterTail::{Draft, Pack, Open, Return, Review, Closed}` (Closed = bare), `check_counter_move(from, to)`, `check_counter_create`, `PageTail`, `FaceSlotState`.
Counter rules applied in `apply`: first `pack -> open` claims (second gets `Conflict`); `open -> return` only by claim owner or `compute` (body appended to the counter); `return -> review` reviewer != builder (S10); `review -> bare` needs `outcome` in passed/failed/blocked/needs-authority/abandoned; `abandoned` needs a compute system return (S11).

## Finding — `resolve`
- `World { books: BTreeMap<BookId, BookState>, policy }`; `insert`, `get`.
- `World::resolve(&PageAddr) -> Result<Resolution>`; `resolve_str(input, Option<&Active>)`; `resolve_page(&PageAddr) -> BTreeMap<u8, Resolution>`; `check_title(&PageAddr)` (A2.8: mismatch is `Elevate`).
- `Resolution { address, source, origin: Origin::{Local, Shelf, Desk, Kernel, Missing}, found: Option<Found>, trace: Vec<Step{step, checked, found, note}> }`; `into_result()` turns Missing into a 404 error. Drafts and retired faces are never inherited.

## Proposals — `validate`
- `validate(&World, &Proposal, at) -> Outcome`. `Proposal { by, ops: Vec<OpRequest{op, addr, tail?, from?, to?, body?, cites?, outcome?}> }`.
- `Outcome { status: Approved|Rejected, reasons: Vec<Reason{code, rule, axiom?, detail, op?}>, findings, entries, entry_numbers, state }`. Serializes as `{"status","reasons","findings","entries":[n...]}`.
- On approval the compute appends `outcome.entries` with `log::file::append` and replaces the book's state with `outcome.state`. The world is never changed by `validate`. Queue proposals one at a time per book.

## CLI
`seqaddr parse|validate <addr> [--active DD.SS.BB[:PPPP,..]]`, `axioms <chain>`, `replay <file> [--until N]`, `history <file> <addr>`, `resolve <addr> --books <dir> [--active ..]`, `propose <proposal.json> --books <dir>` (dry run). JSON out; exit 1 on error.
