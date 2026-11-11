# TRIAL-X: hostile pass on crates/compute (axiom 9)

Lane TRIAL-X, 2026-11-11 (about 3:10 PM EST). A different view from the compute's maker. Judged against docs/spec, docs/CONTRACT.md and Director rulings R1-R11.
Method: every attack goes over real HTTP, to a compute on 127.0.0.1:0 over temp copies of the books, or to a separate process that gets kill -9. crates/compute was not edited.

Tests are in `crates/trial-compute`:
- `cargo test -p trial-compute` runs the 18 held tests, and they pass.
- `cargo test -p trial-compute -- --ignored` runs the 16 findings. Each is a `#[ignore = "finding N"]` test, and each fails today.

**What was under test.** The compute at commit 2bf48d1, which is unchanged since then. It was linked against the **working tree** of `seqaddr-core`, which the CORE fix pass was still changing during this trial (R4, R5, R9, R10 and a seat gate all came in mid-run).
- Two problems I first logged as compute findings were fixed by that core work, so they are now held tests with a note:
  - an R4 refusal came back as HTTP 500;
  - `/face/...FF.draft` gave a 404.
- The seeds try the R10 door first (door page has only face 00). If that fails, they fall back to the C1.1 door (face 00 plus a content face). So the suite runs on either core.

**Counts: 1 blocker, 7 major, 8 minor.**

## Findings

| # | Sev | What breaks | Evidence | Spec |
|---|---|---|---|---|
| 1 | blocker | **Anyone can forge the Director's approval.** `by` is whatever the client types. `by:"user"` with `approved_by:"director"` seats a face, and the entry records it as Director-approved. | store.rs:669-676 (`Some("director") => director_names.contains(proposal.by)`); test findings.rs:21 | Axioms.md:13 "Authority is granted, never claimed. A person holds it... Compute enforces it." R2: approvals must be findable for re-review, and a forged `director` is not findable. |
| 2 | major | **The compute's approval gate checks only `promote`.** A bare `put` that seats a new face skips it. On the committed core it needs nothing. On the CORE-pass core it needs only the words `approved_by: director`, which the core takes from any author (an agent here). | store.rs:664-666 (`if r.op != Some(Op::Promote) { continue }`); test findings.rs:40 | drafting.md:20 "A brand-new face... starts as an empty draft"; R2 "seated... once it has passed a hostile trial" |
| 3 | major | **Any web page can write.** Every reply sends `access-control-allow-origin: *`, and `/propose` ignores the content type. Any web page open in the Director's browser can send a `text/plain` POST (no CORS preflight) and seat faces. Together with #1, it can do that as the Director. | lib.rs:56 (ACAO *), lib.rs:104-108 (raw bytes, no content-type check); test findings.rs:55 | Axioms.md:13 "Compute enforces it"; format.md:17 "Writes are proposals" (from writers, not from any site) |
| 4 | major | **Any client can act as the compute.** It writes `by:"compute"` and gets compute-only powers: `use` records, meters, the `abandoned` outcome. | store.rs:656 (`by` passed through as written); core validate.rs:170 and state.rs:610 trust it; test findings.rs:70 | format.md:98 "`use`... Written only by the compute"; drafting.md:39 "Meters... written only by the compute" |
| 5 | major | **The R2 trial reference is never checked.** Any non-empty string passes, including the maker's own name (`trial:"agent-7"` from agent-7) and a file that does not exist. | store.rs:670,675; test findings.rs:85 | R2 "passed a hostile trial (axiom 9) from a different view than its maker"; Axioms.md:29 "its maker is the easiest one to convince" |
| 6 | major | **A builder can review its own return.** S10 compares names exactly, so `agent-7 ` (with a trailing space) reviews agent-7's return. Case changes are not folded either. | store.rs:656 (no normalizing); core state.rs:514; test findings.rs:100 | workflow-loop.003.md:29 "Reviewer: a view other than the builder (approved S10)... must not review its own work" |
| 7 | major | **`/page` drops inherited drafts, against R5.** The compute's own filter `!it.live` removes them. `/face` (core resolver) now finds the same face. Every real kernel face is a draft, so `/page` of a book inherits nothing, and the two endpoints disagree. | store.rs:341; test findings.rs:117 | R5 "Draft faces count and lookups find them... must still show the face's state as draft" |
| 15 | major | **Every write re-reads the whole book while holding the store's write lock.** One small write takes 1 ms on a small book and 4.4 s on a 38 MB book (debug build). All reads and writes wait during that time, so one client posting about 20 large bodies stalls the compute. Over a book's life, write cost grows as O(n²). | store.rs:725 -> core log.rs:337-341 (`repair_tail` parse + `fs::read`), lib.rs:41 (write lock held); test findings.rs:232 | format.md:105 "A long log replays slowly..." (snapshots); format.md:54 SQLite "remains the fallback if the log proves too slow" |
| 8 | minor | **`elevate` comes back as HTTP 300**, a redirect code with no `Location` header. The contract has no 300. | store.rs:697, core error.rs:93; test findings.rs:136 | CONTRACT.md:23 "Errors: {"error":code,"detail"}" |
| 9 | minor | **One mistake gets two different codes.** A malformed address is 400 on `/book` but 422 on `/page`, `/face`, `/links` and `/resolve`. | store.rs:87,291 vs err_json; test findings.rs:149 | CONTRACT.md:23 (one error shape) |
| 10 | minor | **`/history` never parses its address.** Garbage gets 200 `[]`. A page's titled address (`1523.timer`) finds 0 entries, against 2 for `1523`, even though the core's `history()` ignores titles. | store.rs:463-468; test findings.rs:165 | CONTRACT.md:17 "[log entries touching it]"; Axioms.md:23 lineage |
| 11 | minor | **Queue ids repeat after a restart.** They start again at `q1`, and `/queue` is not kept, so a `queue_id` already handed to a writer becomes ambiguous. | store.rs:268,636-637; test findings.rs:179 | CONTRACT.md:22 "recent proposals with status and reasons"; Axioms.md:23 "A change that is not recorded did not happen" |
| 12 | minor | **A retired face 08 still counts as a link,** both forward and back. | store.rs:478 and 511 (all states via `face_items`); test findings.rs:196 | seqAddr.md:201 "`FF.retired`... awaiting removal"; Axioms.md:27 "A connection is lawful only when it is written" |
| 13 | minor | **`/brands` without `book=` reads every book's dictionary,** so a word defined only on desk 20 answers a reader on desk 10. | store.rs:541; test findings.rs:213 | Design.md:92 "found through each book's dictionary"; seqAddr 2.5 lookup chain |
| 14 | minor | **`--listen 0.0.0.0` and `COMPUTE_LISTEN` are accepted with no warning.** Unauthenticated writes (#1, #4) are then open to the network. The default is loopback, and that holds. | main.rs:9,17; test binary.rs:55 | CONTRACT.md:10 "default http://127.0.0.1:7700". The spec does not say whether non-loopback is allowed (7). |
| 16 | minor | **The compute still builds and lists `FF.00` boards, against R9.** `/page` shows key `05.00`. The core now rejects `/face/...05.00` with 422, so the endpoints disagree. | store.rs:149-150, 427; test findings.rs:262 | R9 "Faces do not have sentinels... no `FF.00`" |

### Top 5
1. **#1** Forged Director approval.
2. **#3** Any web page can write (and, with #1, write as the Director).
3. **#2** A seating `put` skips the compute's gate.
4. **#4** and **#6** Identity is self-declared (acting as the compute, self-review by alias).
5. **#15** Write cost grows with book size and stalls everything.

These share one root: **the compute has no idea who is writing.** Fixing #1, #3, #4, #5 and #6 needs an identity or authentication design. The spec does not have one (7, raise to the Director). Possible pieces include a local token for the Director, an Origin/content-type check, and reserving the names `compute` and `user`/`director`.

## What held up (18 passing tests)

**Concurrency** (held.rs:20). 48 proposals at once: 16 claims on one pack, 16 creators of the same page, and 16 independent pages.
- Exactly one claim won and exactly one creator won.
- All 16 independent pages landed, with no extra entries.
- `n` stayed contiguous, and a restart replayed to the same book.

**kill -9** (crash.rs:20). Five SIGKILL rounds against a separate process during a storm of 400 KB two-op proposals.
- No book was refused afterwards.
- Every acknowledged proposal was there whole, and no half proposal survived.
- Writes carried on after each restart.
- SIGKILL never cut a line. Each proposal is one `write()` followed by fsync, so a cut line can only come from power loss.

**Byte-cut sweep** (crash.rs:102). The book was cut at every byte inside its last multi-op proposal.
- The book always booted, and the proposal was there whole or not at all.
- The next write landed on a clean line.

**R4** (held.rs:62, 89). Tested with é, tab, CRLF, CR, NUL, ESC, DEL, emoji, U+2028 and a byte-order mark, placed in the body, the author, the title and the tail.
- Every case was refused with a 4xx and `status: rejected`.
- The book stayed byte-for-byte unchanged, and numbering stayed contiguous.
- A kernel holding é refuses boot. A book holding a tab is listed in `refused`, and neither file is rewritten.

**Damaged books** (held.rs:106). A refused book is never overwritten by a later write.

**Malformed and huge bodies** (held.rs:122).
- A 3 MB body gets 413.
- Each of these gets a 4xx, and the server keeps serving: 200,000 nested `[`, invalid UTF-8, an empty body, `null`, `[]`, a wrong `ops` type, a numeric `by`, an unknown op, and an op without an address.
- A `content-length` shorter than the body is cut, not over-read. A garbage request line gets 400.

**Path traversal** (held.rs:146). Tried `..`, `%2F`, `%00` and `%0A` in `/face`, `/book`, `/page`, `/links`, `/resolve`, `/brands?book=`, and in proposal addresses.
- All were refused.
- No file was read outside `books/`, and none was created there.

**R2 gate basics** (held.rs:173).
- Refused with 403: a missing approval, `Director` with a capital D, R2 without a trial, R2 with a blank trial, and `director` from a non-Director.
- A non-string `approved_by` gets 400.
- `approved-by` and `trial` survive a restart in `/history`.

**S10 with the exact name** (held.rs:202). The exact builder name cannot review. A stranger cannot return someone else's claim (409). A replayed stale claim is refused.

**Resolution order book > shelf > desk > kernel** (held.rs:222). The trace walks in that order and stops where the face is found. A local face wins, and `/page` sources match.

**R5 on `/face`** (held.rs:250). A draft is found both at `FF.draft` and through lookup, marked `tail: draft`.

**Links** (held.rs:263).
- One-way links and missing 7.8 targets are reported across books.
- Self-links, digit runs and addresses glued to a word are ignored.

**Brands and cards** (held.rs:280).
- Word lookup ignores case, while forms match exact case.
- A brand line pointing at a card that isn't there is marked `missing`, not guessed.
- Empty, blank, punctuation-only, non-ASCII, 10k-character, dotted-id and address queries return 200 `[]`.
- `book=` limits the lookup to that chain.
- `/cards` skips face 00.

**Restart consistency** (held.rs:311). Nine read endpoints give identical answers after mixed traffic: approved, conflicting, rejected, draft and note.

**A stalled client doesn't block the queue** (held.rs:335). A half-sent body does not block other proposals.

**Default listen is loopback** (binary.rs:45).

## Notes for the fix pass
- The core is still changing. If CORE adds identity checks (for example on `by: compute`), #4 may close from the core side. The compute should still reserve the name at the HTTP edge.
- The real `books/00.00.00.book` has 11 non-ASCII lines. Under R4 the core now refuses it, so the compute will not boot on the real books until the kernel is rebuilt in ASCII. That is correct R4 behavior, but it is a cross-lane blocker for the live app. It belongs to the KERNEL lane, not the compute.
