# Review: Cursor's own Workshop build (branch `cursor/build`)

For: Matthew (the Director). Written by Prima, 16 Nov 2026, EST.
Status: a review. It changes nothing in our design. Nothing here is a ruling.
What was read: `https://github.com/Amalgamour/Workshop/tree/cursor/build`, cloned read-only to a scratch folder at commit `709b973`. Nothing was pushed, merged, or edited on GitHub.
How to read the cites: `cursor:` means a file on Cursor's branch. A cite with no prefix is our repo (`/workspace/workshop-build/repo`, branch `build`).

---

## 1. Plain-words summary

1. Cursor built a small, working version of the Workshop on 11 Nov, from about 2:02 PM to 4:12 PM EST. (cursor:cursor/temp.book lines 2 and 149; times there are in UTC, 19:02Z to 21:12Z.)
2. It was put on GitHub today, 16 Nov at 11:11 AM EST, as one single commit. (`709b973`, dated 10:11:59 -0600.) The other 53 commits on that branch are the older `claude` branch history. (cursor: `git log`, parent `bcaaee8`.)
3. It has three Rust parts, a small web page, and 34 tests. All 34 pass. (I ran `cargo test` on the scratch copy: 5+6+4+1+6+7+5 passed.)
4. Its book is one text file per book. Each line is one write. Nothing is ever changed in place. (cursor:core/src/book.rs:1, :43-45.)
5. The big difference from us: **in Cursor's build a face can never be changed or promoted after it is written.** It only ever grows new faces. (cursor:core/src/book.rs:142, :246, :439-440.)
6. Cursor worked without your rulings R1-R25. Its code even says the spec "is not in this repo". (cursor:seqpage/src/lib.rs:2.)
7. It is honest. When it broke a rule, it wrote that down in the book. That is worth copying. (cursor:cursor/temp.book line 4.)

---

## 2. What is on the branch (the map)

**Size.** One Cursor commit adds 95 files and 11,821 lines. (cursor: `git show --stat 709b973`.)

**Shared design files.** Most design files are the same as ours. They differ only in line endings (Windows style). I checked: `Axioms.md`, `seqAddr.md`, `format.md`, `AGENTS.md`, `drafting.md`, `brands.md`, `decisions.md`, `Design.md`, `kernel-design.md`, `review.md`, `SEQ-GUIDE.md` all match our `docs/spec/` copies when line endings are ignored. (`diff --strip-trailing-cr` against `docs/spec/`.)
- `SEQ-GUIDE.md` is a copy of **our** guide (our commit `688b9df`). It points to files Cursor did not have, like `docs/spec/seqpage.md` and `crates/seqpage`. (cursor:SEQ-GUIDE.md:5, :604-609.)
- Cursor is **missing** `DIRECTOR-RULINGS.md`, `seqpage.md`, `face00.md`, and `seqpage-QUESTIONS.md`. We have all four in `docs/spec/`. (cursor: file list; our `docs/spec/`.)
- Its `workflow-loop.md` is the newer `.003` version. (cursor:workflow-loop.md equals cursor:workflow-loop.003.md.)

**Code (Rust, plus a Next.js page).**
| Part | What it does | Cite |
|---|---|---|
| `core/` (crate `seqbook`) | reads addresses, reads and appends the book, checks whys | cursor:core/src/lib.rs:1-12 |
| `compute/` | the gatekeeper: read a face, propose a write, small web server | cursor:compute/src/lib.rs:1-2, cursor:compute/src/main.rs:96-99 |
| `seqpage/` | turns one page into a `.seq` text view, and back into a request | cursor:seqpage/src/lib.rs:1-2, :15, :202 |
| `app/` | web page: pick a band, a page, a face; send a sentence | cursor:app/app/page.tsx:5, :24-28 |

**Tests.** 34 tests, all pass (my run). Ours have 359 `#[test]` marks across `crates/` (grep count; not run in this review).

**Books.** `cursor/temp.book` (149 lines) is Cursor's own work record, written as a book. `core/fixtures/10.11.21.book` is a small test book with one "timer" page. (cursor:cursor/temp.book; cursor:core/fixtures/10.11.21.book.)

**Per-page run sheets.** `cursor/pages/10.10.10.0501/AGENTS.md` (and 0502-0504) tell a worker exactly which commands to run for a pack, and where to stop. (cursor:cursor/pages/10.10.10.0501/AGENTS.md:9-31.)

---

## 3. How it handles each part of the design

**Addresses (seqAddr).**
- Uses the same `desk.shelf.book.page.face` shape. A short group is refused, never padded. (cursor:core/src/addr.rs:1-3.)
- A title comes right after the page. A title can never be followed by a face. (cursor:core/src/addr.rs:501.) This matches your answer A5 today: links are page plus title, never a face.
- A face's identity leaves out title and tail. So `.draft` and the plain face are the **same slot**. (cursor:core/src/addr.rs:127-135.) This is why a draft can never be seated (see below).

**Faces 00-09.**
- Face 00 is a short "stamp": title, state, type, axioms. (cursor:cursor/temp.book line 2; cursor:core/fixtures/10.11.21.book line 5.) It is **not** a registry, and has no fingerprint list. Compare our R19 and R25. (DIRECTOR-RULINGS.md:74, :99.)
- Faces 05 and 06 must have a counter (`05.01`, `06.01`...). (cursor:core/src/book.rs:355.)
- Face 06 counters are used as a running notes log for each page. (cursor:cursor/temp.book lines 128-149.)
- Face 09: nothing. A request for `.09` is just "missing". (cursor:cursor/temp.book line 138.) Ours is also unassigned in code today. (crates/seqaddr-core/src/face.rs:28.)

**Tails (states).**
- Counter faces climb: draft, pack, open, return, review, closed. (cursor:core/src/book.rs:426-434.)
- Plain faces can only go seated to retired, or draft to retired. (cursor:core/src/book.rs:437-443.)
- There is **no** draft to seated step. Cursor says so itself: "These faces cannot be rewritten. There is no promote." (cursor:cursor/temp.book line 105.)

**The book file and storage.**
- One JSON line per write; line 1 is a header. (cursor:core/src/book.rs:85-99.) Same as our base format. (docs/spec/format.md:70.)
- Every read loads and replays the **whole** book from the top. (cursor:core/src/book.rs:43-45; cursor:compute/src/lib.rs:177, :194.) No index, no pyramid, no snapshots. Snapshots were left out on purpose. (cursor:cursor/temp.book line 116.)
- After each write it calls `flush`, not `fsync`. (cursor:core/src/book.rs:298.) Ours calls `sync_all` (fsync). (crates/seqaddr-core/src/log.rs:399, :411, :437.)
- A torn last line is dropped on read, and blocks the next write until a person looks. (cursor:core/src/book.rs:60, :221-224.)

**The `.seq` file.**
- A `.seq` file is a view of one page. The book stays the real copy. (cursor:seqpage/src/lib.rs:1.) Same as our R3. (DIRECTOR-RULINGS.md:11-12.)
- It checks plain ASCII on `.seq` files. (cursor:seqpage/src/lib.rs:93-96.) But the **book writer does not** check ASCII. (no ASCII check in cursor:core/src/book.rs; grep.) Their book holds long dashes (non-ASCII) in entry 20. (cursor:cursor/temp.book line 21.) That entry was written at 2:02 PM EST, before R4 at 2:54 PM EST, so it was not a break at the time. (DIRECTOR-RULINGS.md:14.)
- Import turns a new block into **one** request. It cannot create a new page, because a page needs a stamp and a content face, which is two writes. Cursor stopped there and asked. (cursor:cursor/temp.book line 149.)

**Logs.** The whole book is the log. There is no per-page log. Per-page history is shown by filtering the book (cursor:seqpage/src/lib.rs:15-24, :51-56).

**The axioms.** Same nine. (cursor:Axioms.md, equal to docs/spec/Axioms.md.) Every write carries an `axioms:` cite. (cursor:cursor/temp.book, e.g. line 3.)

**The three leads (person, model, compute).**
- Compute: refuses or accepts each write; a refusal leaves the file alone. (cursor:compute/src/main.rs:1; cursor:compute/src/lib.rs:186-215.)
- Model: there is **no real model**. The "proposer" is a tiny local rule (`law:` prefix or a note). (cursor:compute/src/lib.rs:30-72.) No model key was set. (cursor:cursor/temp.book line 138.)
- Person: reads faces in the web page; the page talks to the compute, never the file. (cursor:cursor/temp.book line 138; cursor:app/app/page.tsx:5, :28.)

**Editing user documents (face 04).** Not possible. A face 04 can be written once. To correct it, Cursor writes a new "current" note on face 06 that says the old text is out of date. (cursor:cursor/temp.book lines 105-114.) Cursor lists this as its own top gap: "no way to revise a seated face". (cursor:cursor/temp.book line 118.)

---

## 4. Insights (what we learned)

**I1. Cursor proves our "Google approach" choice was needed.** Without a way to change face 04, its book filled with "this is out of date" notes. Ten of them in one session. (cursor:cursor/temp.book lines 105-114.) Your t172u answer (small changes, plus full copies, old versions kept) fixes exactly this. (docs/design/SEQ-FILE-PLAN.md:457-489.)

**I2. "Draft and seated are the same slot" blocks promotion.** Because the tail is not part of a face's identity (cursor:core/src/addr.rs:127-135), and a slot can be filled only once (cursor:core/src/book.rs:246), a draft can never become seated. Our R24 climb-and-reseat (DIRECTOR-RULINGS.md:94-97) needs the opposite. Lesson: identity rules decide what editing is even possible. Decide them together.

**I3. Working without your rulings cost them.** Cursor did not have R1-R25 (cursor:seqpage/src/lib.rs:2; cursor:cursor/temp.book line 144). So: no registry in face 00 (R19, R25), no ASCII check in the book (R4), no reseat (R24). Lesson: the rulings file is the most valuable thing to hand any new team first.

**I4. "Closer / Not closer" is a strong habit.** Every pass ends with: what was checked (real command, real output), what got closer, and what did not. (cursor:cursor/temp.book lines 129, 138, 145, 149.) It answers your check 2 ("is it better, and where do we fall short") in two lines.

**I5. They put their own work in a book.** Plans, answers, runs and checks all live in `cursor/temp.book` as pages and faces. (cursor:cursor/temp.book lines 2-149.) It tests the design by using it. But the times in it are typed in by hand, not read from the clock (cursor:core/examples/record_seq_design.rs:8; cursor:compute/src/lib.rs:19). So one entry is dated before the one above it (cursor:cursor/temp.book lines 143-144: 21:05Z then 20:55Z). A recorded time that is made up breaks axiom 6's "a change that is not recorded did not happen" in spirit. (docs/spec/Axioms.md:23.)

**I6. They tried each write on a copy first, then only refused NEW problems.** The compute copies the book, tries the write, and compares problems before and after. Old gaps do not block a new write; only new gaps do. (cursor:compute/src/lib.rs:186-215, :204-207.) This fits axiom 7: an old gap stays visible, but you may not add a new one. I could not confirm whether our compute compares before and after this way (not verified).

**I7. They spotted the "new page needs two writes at once" problem.** A page needs face 00 and a content face together, or neither. (cursor:cursor/temp.book line 149.) Any face 04 editing and import design must allow a group of writes that land together or not at all.

**I8. Their single-file book is simple but will not scale.** Every read replays the whole book (cursor:core/src/book.rs:43-45). Fine at 149 lines. Your pyramid and small-files answers (docs/design/SEQ-FILE-PLAN.md:42-100) are the fix.

**I9. Address rule A5 is already in their code.** "A title is not followed by a face" (cursor:core/src/addr.rs:501). Independent agreement is a good sign your A5 is natural.

**I10. Honest about breaking rules.** The first batch of writes (37 entries, all stamped 19:02Z) went straight into the file, without the compute. Cursor wrote that down in face 04 and kept the book as draft. (cursor:cursor/temp.book line 4.) That is axiom 6 done right.

---

## 5. Ideas worth taking

1. **"Closer / Not closer" lines** at the end of every pass and every Tester eval. (cursor:cursor/temp.book lines 129, 138.)
2. **Try-on-a-copy, refuse only new gaps** as a compute check, if we do not already do it. (cursor:compute/src/lib.rs:186-215.)
3. **A "copies face 01" warning.** Their check flags a face 04 that only repeats face 01 instead of explaining why. (cursor:core/src/check.rs:50-57.) We have the hard why check (crates/seqaddr-core/src/validate.rs:403-435). I did not find the copy warning in our code (grep; not fully verified).
4. **A per-page run sheet** for each pack: exact commands, where to stop, what to return. (cursor:cursor/pages/10.10.10.0501/AGENTS.md:9-31.)
5. **Group writes** that land together or not at all, for new pages and for imports. (cursor:cursor/temp.book line 149.)
6. **Record our own build in a book**, but with real clock times only. (cursor:cursor/temp.book; contrast cursor:compute/src/lib.rs:19.)
7. **A web page that only talks to the compute,** never the file. (cursor:app/app/page.tsx:5, :28.)

---

## 6. Conflicts with our axioms or your rulings

| # | Cursor's choice | What it conflicts with | Cite |
|---|---|---|---|
| X1 | A face can be written once; no revise | Your t172u Google approach for face 04 | cursor:core/src/book.rs:246; docs/design/SEQ-FILE-PLAN.md:457 |
| X2 | Draft can only go to retired; no seat | R24 climb then reseat | cursor:core/src/book.rs:439-440; DIRECTOR-RULINGS.md:94 |
| X3 | Face 00 is a stamp only | R19, R25 (registry root, 00 counter) | cursor:cursor/temp.book line 2; DIRECTOR-RULINGS.md:74, :99 |
| X4 | No face 09; page history lives in face 06 notes | Your t171u answer: face 09 is the page log | cursor:cursor/temp.book line 138, lines 128-149; docs/design/SEQ-FILE-PLAN.md:234 |
| X5 | One big file, replayed from the top every read | Your pyramid and small-files answers | cursor:core/src/book.rs:43-45; docs/design/SEQ-FILE-PLAN.md:42, :71 |
| X6 | Book writer does not check ASCII | R4 (stored files are plain ASCII, refused on write) | cursor:core/src/book.rs (no check); DIRECTOR-RULINGS.md:14-16 |
| X7 | Times typed in by hand, one out of order | Axiom 6 (the record must be true) | cursor:compute/src/lib.rs:19; cursor:cursor/temp.book lines 143-144 |
| X8 | `flush` only, no `fsync` | Crash safety we already require | cursor:core/src/book.rs:298; crates/seqaddr-core/src/log.rs:399 |
| X9 | Check on a copy, then write later, with no lock | Two writers could slip in between (Cursor ruled out a second writer for now) | cursor:compute/src/lib.rs:196-212; cursor:cursor/temp.book line 116 |
| X10 | Local server allows any web page to call it (`Access-Control-Allow-Origin: *`) | Axiom 1: only granted callers may propose | cursor:compute/src/http.rs:235 |

Not a conflict: Cursor keeps every face as readable text. Your t171u answer says only face 04 must be readable; the rest **may** be code. Readable everywhere is allowed, just slower.

---

## 7. Questions you could ask Cursor

1. When you found you could not fix an out-of-date face, why did you choose "add a new note" instead of building a way to revise it? What would you build now?
2. Why is a draft the same slot as the seated face? Was that on purpose, and how would a draft ever become seated?
3. Why did you type the times in by hand instead of reading the clock? Would you change it?
4. Your compute refuses only new gaps, not old ones. Why that rule? Did you see any case where it let something bad through?
5. How would you make "a new page" land as one group: stamp and content together, or nothing?
6. You used face 06 notes as each page's history. If face 09 were the page log, what would move there, and what would stay in 06?
7. Your book replays from the top on every read. At what size did you expect that to become too slow, and what would you add first?
8. Which of your "Closer / Not closer" checks caught a real mistake? Can you show one?
9. You worked without our rulings file. Which of your choices would you change after reading R1-R25?
10. Why does the local server let any web page call it? Who should be allowed to propose a write?

---

## 8. What I could not verify

- Whether our compute already compares problems before and after a write, like Cursor's (I6). Not checked in our code.
- Whether our code has a "face 04 copies face 01" warning. A grep found none; not a full read.
- Our test count (359) is a grep of `#[test]`; I did not run our tests in this review.
- Who answered Cursor's four questions on 11 Nov. Its book says "the person". (cursor:cursor/temp.book line 40.) I did not confirm it was you.

## Cursor's answers to our 10 questions (relayed by Matthew, t186u, 2026-11-16 11:50 AM EST)

These are summarized from Cursor's reply. Its file:line cites point into cursor/build and were not re-checked here.

1. Stale faces: a seated face can be created only once (core/src/book.rs:245). The revise steps in format.md (~:94) were still marked proposed, so Cursor didn't build them, and new truth went into face 06 notes (cursor/temp.book:105). What it would build now: re-seating for 05, a change log plus snapshots for 04, and locked linked pages with rework done as a new copy. That matches R24, R29, R30, and R31.
2. Draft and final slot: one address holds one body, and the tail is a field on the face (book.rs:148). Work counters walk draft, pack, open, return, review, closed (book.rs:426). Content faces can only go to retired (book.rs:437). A draft could never become the seated body, because promote was never built.
3. Times: they were typed-in constants (core/examples/record_pass2.rs:8, record_seq_design.rs:8), chosen so the notes would read in pass order, which made n 143 earlier than n 142. Cursor would have the writer read the clock and refuse a time earlier than the line above, leave the old lines, and add a note that n 143's clock is wrong.
4. Gate: writes are tried on a copy, and the file changes only if no NEW hard gap appears (compute/src/lib.rs:186, :222; core/src/check.rs:32). The hard gaps are a missing why, an empty why, or a bad page shape. Findings such as a copied why (check.rs:54) are ignored, so a face 04 that repeats 01 would pass. The record programs wrote through Writer and skipped the gate entirely.
5. A new page all at once: one proposal carries the stamp, the first content face, and the 04 why. It's applied on a copy, and either all of it is appended or none (format.md:100). Under R26, the small page file appears whole or not at all.
6. Face 09: it's unassigned in seqpage/src/lib.rs:393, so history went into 06. Pass reports and stale notes would move to 09, while a person's working notes stay in 06.
7. Every read reloads and replays the whole file (book.rs:43). That would get slow somewhere past a few tens of thousands of lines (Cursor's estimate). Cursor's first fix: keep the book in memory, plus a snapshot line (format.md:104).
8. A real catch: a page saved from PowerShell gained a carriage return on every line, and the seq check refused it (temp.book:145). The tool was then fixed to write plain newlines.
9. What Cursor would change after reading our rulings: face 00 becomes a registry, 05 gets re-seated, faces other than 04 become compact, small page files become the stored form, history moves to 09, 04 gets a change log and snapshots, links name the page plus title (Cursor's point at faces, temp.book:119), and registered, linked pages lock.
10. Server: it sends Access-Control-Allow-Origin: * (compute/src/http.rs:235) but listens only on 127.0.0.1 (:83), so any page in this machine's browser can call it. Cursor's view: the person (through the Workshop page) and models may propose, the compute decides, and other sites are refused.

### Lessons for our build (Prima, 2026-11-16)
- L1. Unbuilt "proposed" steps turn into stale data. Every rule a face relies on (revise, promote, reseat) must be built before that face is seated.
- L2. Every write goes through one gate. Cursor's record programs skipped its gate, so check that our kernel builder and any tools also go through the compute.
- L3. Clocks come from the system, and a time earlier than the line above is refused. Never type times in by hand (honesty, t180u).
- L4. The gate should also refuse a copied why, such as a face 04 that repeats 01, not just note it.
- L5. Line-ending and encoding checks catch real mistakes. Keep the carriage-return refusal.
- L6. Our compute server must refuse calls from other sites. Check whether ours allows any origin.
- L7. Moving notes into face 09 means splitting person notes (06) from system history (09). Our plan should say which is which.
