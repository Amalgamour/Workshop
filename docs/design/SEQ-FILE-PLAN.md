# The .seq book file: a design plan

state: draft plan, `7` (open). Not a ruling. Nothing here is law.
made: Mon 16 Nov 2026, Designer (design partner for Prima). Director: Matthew, the only approver.
why: Matthew asked today (16 Nov 2026, 11:04 AM EST, passed on by Prima) for a design plan for the book file. He said a book is a .seq file, it is basically a self-contained database file, and it should work like a pyramid.
status of every idea below: Matthew's ideas from today are marked "Matthew's idea, 16 Nov 2026". They are his leading ideas, not rulings. Anything not found in a Workshop source is marked "New (not in any source)". Rulings R1-R25 are quoted only where they already exist.
does not: edit DESIGN.md, the kernel, the core, or any spec file; close any QD question; write a 00.counter; seat anything.

---

## Plain-words summary

A book is one file on the disk. Today it is a list of changes, one per line, oldest first. To read a page, the computer reads the whole list from the top. That is fine while books are small. It gets slow when books grow.

Matthew wants the book file to work like a pyramid. The top is small and loads fast. It tells you where everything else is. You only open the deeper parts you need. But you can still get to any part quickly.

This plan keeps the list of changes exactly as it is. Nothing old is ever changed or removed. That keeps the past safe (axiom 6).

What it adds is a set of signposts. A signpost (the *map*) says "page 1001 starts at this spot in the file". The computer writes a new signpost at the end of the file after each change. The newest signpost is always the last one.

To open a book, the computer reads the first line and the last signpost. That is the top of the pyramid. Then it jumps straight to the page it needs.

A page has one signpost of its own (the *page index*). It says where each face of the page sits. Faces are only read when someone asks for them.

Face 00 still says what kind of page it is: a system page, a general page, or a kind not invented yet. The plan keeps the "where things sit" list out of face 00 itself. If it went inside face 00, face 00 would change every time any face changed.

Matthew's idea is that face 09 becomes the page's log. This plan tests it. It works best if face 09 is written only by the computer, and is a list of what happened to this page, pointing at the real changes. It should not be a second copy of them. That is a choice for Matthew.

Everything stays plain text (printable ASCII). A person can open the file in any editor and read it. That keeps Matthew's ruling R4. A binary file would be faster, but it would break R4, so it is listed as a choice, not a plan.

The signposts can always be rebuilt from the list of changes. So if a signpost is lost or damaged, nothing real is lost.

The real thing should be written in Rust, like the core and the compute today. The person still checks it in plain words, not in code.

There are open choices that only Matthew can make. They are listed near the end. The top three are marked.

---

## How to read this

- Each numbered step has three checks, always under the same three labels:
  - **Axioms:** does this step fit the nine axioms? Each answer cites the line in `docs/spec/Axioms.md`.
  - **Better:** is this better than what we have now, or than the obvious other way? Where do we still fall short?
  - **Three leads:** what the person, the model and the compute each need from this step.
- A cite like `[seqAddr.md:24]` is line 24 of `docs/spec/seqAddr.md`. Spec files are in `docs/spec/`. `[DESIGN.md:157]` is `docs/design/DESIGN.md`. `[BUILD-LOG:53]` is `docs/BUILD-LOG.md`. `[DECISIONS-LOG:410]` is a row in `docs/design/DECISIONS-LOG.md`. `[AGENTS.md:45]` is `docs/spec/AGENTS.md`.
- `[R4]` is a ruling in `docs/spec/DIRECTOR-RULINGS.md`. A ruling wins over older wording [DIRECTOR-RULINGS.md:1].
- A D number marked "working path" (for example D414) is a recommended option from Tester, not a ruling. It stays `7` until Matthew rules [DESIGN.md:17].
- `7` means missing or open. `9` means not yet trialled [Axioms.md:25] [Axioms.md:29]. This whole plan is `9`: it has not faced a hostile trial.
- The three axiom lines used most: axiom 1, authority is granted [Axioms.md:13]; axiom 6, the past is not rewritten [Axioms.md:23]; axiom 7, unknown stays unknown [Axioms.md:25].

---

## What exists today (the starting point, not a step)

- The book is the real stored copy. A `.seq` file today is a view of one page, exported from a book and imported back [R3] [DIRECTOR-RULINGS.md:12] [seqpage.md:11] [seqpage.md:13].
- A book is one file [format.md:21]. Book files are named like `10.11.21.book` [format.md:25].
- A book is an append-only log of approved writes. Nothing is edited in place. The current state comes from replaying every entry in order [format.md:61].
- Each entry is one JSON line [format.md:70]. Line 1 is the header: format name, version and book address [format.md:79]. An example header in the repo is `{"seqbook":1,"address":"10.11.21"}` (books/10.11.21.book line 1).
- A `snapshot` entry lets replay start late; older entries stay [format.md:88] [format.md:105]. Working path D414, not a ruling: a snapshot is never trusted over the log and is checked on every open [DESIGN.md:165].
- One compute owns every book; only it writes to disk [format.md:15] [format.md:18]. It runs one queue with one writer and appends with fsync [BUILD-LOG:53]. A cut-off last line is dropped on load [BUILD-LOG:54]. A cut-off multi-op proposal is dropped whole [BUILD-LOG:38].
- Stored files are printable ASCII 0x20-0x7E plus newline [R4] [DIRECTOR-RULINGS.md:16].
- Face 00 is the registry: the stamp, the page type and the per-type registry [R10] [R12] [R19] [DIRECTOR-RULINGS.md:41] [DIRECTOR-RULINGS.md:76].
- Face 09 is unassigned [decisions.md:182] [review.md:53] [seqAddr.md:158].
- Size today: the four book files in `books/` hold 71 lines and about 233 KB in total (measured with `wc` on 16 Nov 2026). The kernel book is the largest, about 205 KB in 51 lines.

---

## Step 1. Names and levels: book, page, face

Matthew's idea, 16 Nov 2026: "A book is a .seq file." A book holds pages. A page is a small multi-dimensional book broken into pieces, one piece (a *face*) for each lead. Face 00 is the page's registry face. It says what kind of page it is.

The levels match the existing design: books contain pages, pages contain faces, faces contain cards [AGENTS.md:41]. A page is one object with several faces, each a view for a different reader [format.md:12] [seqAddr.md:7].

The "one face for each lead" idea already has a footing in the face table. Face 01 is for agents (the model) [seqAddr.md:150]. Face 03 is for the compute [seqAddr.md:152]. Face 04 is for users (the person) [seqAddr.md:153].

**The name clash.** R3 says the `.seq` file is a page view and the book is the real copy [DIRECTOR-RULINGS.md:12]. Matthew's words today call the book itself a `.seq` file. Both cannot use the same name without confusion. This plan does not decide it. It uses "the book file" for the stored file and "the .seq page view" for today's export. The choice is listed for Matthew (choice C1).

New (not in any source): a plain reading that fits both. The book file could take the `.seq` extension, and the page view could keep its layout but take another name. Or the book could keep `.book`, and Matthew's sentence is read as "a book is the real seq file". Only Matthew can say which he meant.

**Axioms:** Fits axiom 2: the same shape at every scale; a page is "a small book" inside a book [Axioms.md:15]. Fits axiom 3: one face per lead [Axioms.md:17]. Changing the meaning of `.seq` would touch R3; only Matthew can do that, so it stays open [Axioms.md:13].

**Better:** Naming the levels the same way at every scale is better than inventing a new word for "the stored file". It falls short in one place: the word `.seq` is now used for two things (R3's view, and today's idea of the book). Until Matthew chooses, every document must say which one it means.

**Three leads:** The person needs one name per thing, so they can tell a book from a page view. The model needs the same, so it never writes a page view thinking it is the book. The compute needs the file name rule to be exact, because it checks that the header address matches the file name [BUILD-LOG:54].

---

## Step 2. The pyramid: the levels in one picture

Matthew's idea, 16 Nov 2026: the top loads quickly; deeper information is reached later; only what is needed is loaded, but getting to any point is quick.

This fits the brief: "Return only the context needed, with its source and governing rules" [AGENTS.md:44].

New (not in any source): the pyramid, top to bottom.

```
level 0  header line (line 1)          what this file is, its version, its book address
level 1  book map (the last map line)  one row per band of 100 pages: where its band map is
level 2  band map                      one row per page: kind, title, where its page index is
level 3  page index                    one row per face: state, where its current block is
level 4  face block                    the face itself: an ordinary entry, Markdown body
level 5  page history (face 09 idea)   the page's earlier blocks, reached by walking back
```

To read one face, the compute reads level 0, then the last book map, then one band map, then one page index, then one block. That is five short reads, however large the book is.

The bands follow the existing page layout. Every band is exactly 100 pages, `PP00-PP99` [seqAddr.md:240]. So a band map never holds more than 100 rows. The book map never holds more than 100 rows (pages 0000-9999).

Prima's first sketch had a header, one book map, and face 00 per page. This plan adds the band level and moves "where each face sits" out of face 00 into a compute-only page index (see Step 6). The reasons are given in those steps.

**Axioms:** Fits axiom 2: the same shape at every scale; a book map lists bands, a band map lists pages, a page index lists faces [Axioms.md:15]. Fits axiom 8: each level points down; "a pointer points; the source governs" [Axioms.md:27]. The maps are pointers only; the entries stay the source.

**Better:** Better than today for large books: today every open replays every entry [format.md:61]. Better than a single flat map: a flat map of up to 10,000 pages would be rewritten whole after every change; a band map is at most 100 rows. Where we fall short: books today are small (about 233 KB in total), so the gain is not felt yet, and five levels is more machinery than a small book needs. The plan pays complexity now for speed later.

**Three leads:** The person needs to see the same pyramid when they inspect a file, top line first, so they can follow it by hand. The model needs to be handed only the face it asked for, with its address and source, not the whole book [AGENTS.md:44]. The compute needs a fixed, short path to any face, and a way to rebuild every level from the entries if a level is damaged.

---

## Step 3. Plain text, not binary (keeps R4)

R4: stored files use printable ASCII 0x20-0x7E plus newline; any other byte is rejected on write, and a book holding one is damaged on read [DIRECTOR-RULINGS.md:16]. Matthew's words were "We want a simple storage design for now" [DIRECTOR-RULINGS.md:15]. The brief also says the store "must be checkable by a person" [AGENTS.md:10] and weighs "human inspection" [AGENTS.md:45].

This plan keeps every level as plain text: each level is one JSON line, like every entry today [format.md:70]. Offsets and lengths are written as plain decimal numbers. Nothing in this plan needs a byte outside R4.

Options, for the record:

- Option T1 (this plan): plain ASCII JSON lines at every level. Keeps R4. Readable in any editor. Slower to parse than binary, and a little larger.
- Option T2: a binary layout (fixed-size blocks, raw numbers). Faster and smaller. **It conflicts with R4** [DIRECTOR-RULINGS.md:16] and with the person-checkable goal [AGENTS.md:10] [AGENTS.md:45]. It cannot be built unless Matthew chooses it. This plan does not reopen or narrow R4.
- Option T3: SQLite. Already weighed in format.md: one file and real transactions, but binary, not mergeable in git, and its transactions duplicate the compute's queue; it remains the fallback if the log proves too slow [format.md:54]. It also conflicts with R4.

Matthew called a book "basically a self-contained database file". T1 gives the database parts (fast lookup by address, history, crash safety) without leaving plain text. The choice is listed for Matthew (choice C3).

**Axioms:** Fits axiom 1: R4 is Matthew's ruling; this plan works inside it and does not widen it [Axioms.md:13]. Fits axiom 4: the why of plain text is recorded (person-checkable, simple for now) [Axioms.md:19].

**Better:** Better than binary for Workshop's goals: a person can check it [AGENTS.md:10], and git shows clean added lines [format.md:66]. Where we fall short: text is slower to read than binary, and a JSON line must be parsed to find its fields. For books in the tens of megabytes this is still fast; for much larger books it may not be, and then Matthew would need to weigh T2 or T3.

**Three leads:** The person needs to open any book in a text editor and read it top to bottom. The model needs text it can read directly, which JSON lines already are [format.md:70]. The compute needs to refuse any non-ASCII byte on write and report it on read, as it does today under R4.

---

## Step 4. The header (level 0, line 1)

Today line 1 is the header: format name and version, and the book's address [format.md:79]. The compute already checks that the version is 1 and that the address matches the file name, and refuses to start if the kernel fails [BUILD-LOG:54].

Prima's sketch put "where the map is" in the header. This plan does not, and here is why. The header is line 1. If it had to say where the newest map is, line 1 would change after every write. That is an edit in place, and format.md says "Nothing is ever edited in place" [format.md:61].

New (not in any source): the header is written once and never changes. It holds the format name, the version, and the book address, as today. A new version number (for example `"seqbook":2`) tells an older reader to refuse the file cleanly instead of misreading it. The newest map is found from the end of the file instead (Step 5).

Example (new, for illustration only):

```
{"seqbook":2,"address":"10.11.21"}
```

**Axioms:** Fits axiom 6: line 1 is never rewritten [Axioms.md:23]. Fits axiom 7: a reader that does not know version 2 refuses rather than guesses [Axioms.md:25].

**Better:** Better than Prima's sketch, because a header that points to the map would have to be rewritten after every change. Better than today only in that it gives the new layout a clean version line. Where we fall short: bumping the version means every book must be moved to the new layout once (Step 15), and old tools stop reading new books.

**Three leads:** The person needs line 1 to say plainly what the file is and which book it holds. The model needs nothing more than that, and should never write line 1. The compute needs line 1 to be fixed, so it can check the version and address on every open [BUILD-LOG:54].

---

## Step 5. The book map, found from the end (level 1)

New (not in any source): after each approved proposal, the compute appends a fresh **book map** line at the end of the file. The newest book map is always the last map line in the file. Older map lines stay where they are.

To open a book, the compute reads line 1, then reads backward from the end of the file to the last map line. Normally that is the very last line.

The book map has one row per band that has pages: the band (`PP`), where that band's newest band map sits (byte offset and length), and that band map's fingerprint (Step 10). Each map line also names the offset of the map before it, so older maps can be walked back.

A map line is a book-level entry written only by the compute, like a `snapshot` [format.md:88]. Book-level entries belong to no page and stay in the book on export [seqpage.md:206]. So the `.seq` page view does not change, and the R3 round trip stays lossless [DIRECTOR-RULINGS.md:12].

Example (new, for illustration only):

```
{"n":42,"at":"2026-11-16T16:30:00Z","by":"compute","op":"map","level":"book","prev":20480,"bands":[["00",18800,412,"fp:..."],["10",22010,388,"fp:..."]]}
```

A map is derived from the entries. It is never written by a person or a model, and never proposed. Boards, contents lists and path lists are already "derived from the log and never written as entries" [format.md:102]. The map is the same kind of thing, written down only so the compute can find it fast. Whether writing a derived line into the book is allowed at all is the same question as for snapshots (QD46, working path D414); this plan names it, and does not close it.

**Axioms:** Fits axiom 6: new maps are added after the old ones; nothing earlier is touched [Axioms.md:23]. Fits axiom 8: the map is a pointer; the entries govern [Axioms.md:27]. Fits axiom 1 if only the compute writes maps [Axioms.md:13] [format.md:18].

**Better:** Better than a header pointer: no edit in place. Better than today: opening a book reads two lines, not every line. This is the same trick other single-file formats use to stay append-only (new, not in any source). Where we fall short: every write now adds at least one extra line (a map), so the file grows faster. Tidying (Step 12) is the answer, and it is a choice for Matthew.

**Three leads:** The person needs to find the newest map by looking at the last lines of the file, with no special tool. The model needs nothing from the map directly; it asks the compute by address. The compute needs the map to be cheap to write after every proposal, and to be refused if anyone but the compute tries to write one.

---

## Step 6. Band maps and the page index (levels 2 and 3)

**Band map (level 2).** New (not in any source): one line per band, at most 100 rows. Each row is one page: page number, title, page kind (the `type` from face 00), page state, where that page's newest page index sits, its length, and its fingerprint.

The page kind is copied into the row so the compute can route a request (system page, general page, a kind not yet invented) without opening the page. The `type` stays defined in face 00 [decisions.md:285] [R19]. The row is a derived copy for speed, never the source.

**Page index (level 3).** New (not in any source): one line per page, written by the compute after any write to that page. It lists each face the page has: face number, its state (draft, seated, counted, retired), where its current block sits, its length, and its fingerprint. For a counted face it lists each counter and its tail. It also points to the page index before it (`prev`), so the page's past can be walked back (Step 8).

**Why not put this inside face 00.** Prima's sketch put "where each face sits" in face 00. This plan keeps it out, for a reason Matthew already gave. In R25 he said the 00 counter list "must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint" [DIRECTOR-RULINGS.md:101]. The same is true here. If face 00 held face locations, face 00 would change every time any face changed. Face 00 would then have no stable fingerprint, and every write would look like a change to the registry.

What face 00 keeps is what the rulings give it: the stamp, the type, and the per-type registry [R19] [DIRECTOR-RULINGS.md:76]. The face00.md draft already proposes that the compute writes the `faces:` list and nobody writes it by hand [face00.md:179], because a contents list is derived, never hand-written [face00.md:177]. Which wins on a mismatch is still `7` there (F2). In the `.seq` page view, the registry section can still show `faces :=` as a derived line, as it does today [seqpage.md:84]. So a person reading face 00 still sees "what kind of page, and which faces", which is what Matthew described. Only the byte positions live in the page index.

A kind not invented yet: a `type` not in the kernel's list is a finding, not an error, and the page is still read [face00.md:146]. The band map copies the unknown type exactly as written. It never guesses a nearer type.

**Axioms:** Fits axiom 7: an unknown kind stays unknown and is shown as written [Axioms.md:25]. Fits axiom 8: the band map's copy of `type` is a pointer; face 00 governs; if they disagree, the compute raises it [Axioms.md:27]. Fits axiom 2: the band map and page index have the same shape as the book map [Axioms.md:15].

**Better:** Better than Prima's sketch: face 00 does not churn, which keeps R25's fingerprint idea workable. Better than today: the compute can tell what kind a page is without replaying the book. Where we fall short: the page kind now appears in two places (face 00 and the band map row). That is a copy, and copies can drift [Axioms.md:15]. The plan answers this by making the row derived only and checked against face 00, but the risk is real.

**Three leads:** The person needs face 00 to stay the one place that says what kind of page this is. The model needs to read face 00 and the faces it is given, and never write a band map or page index. The compute needs the band map and page index to route requests fast, and to rebuild them from the entries whenever asked.

---

## Step 7. Face blocks, read only on demand (level 4)

A face block is simply the entry that wrote the face's current text: an ordinary `put` (or `promote`, `merge`, and so on) line, as today [format.md:74] [format.md:86]. Face content stays Markdown in `body` [format.md:81]. Cards are its `##` headings [seqAddr.md:168].

New (not in any source): the page index points straight at that entry's byte offset. The compute reads that one line and nothing else. A face nobody asks for is never read.

Block size: this plan uses no fixed block size. A block is one entry line, as long as it needs to be. The offset and length in the page index are enough to read it in one go. A fixed size (for example 4096 bytes, padded) would help a binary layout, but in plain text it wastes space and padding would be bytes nobody wrote. This is a builder choice, recorded with its why [AGENTS.md:45]; it is not a choice for Matthew unless he wants one.

Seated, draft and counted faces work as today. A draft is found by lookup and shows that it is a draft and why [R5] [DIRECTOR-RULINGS.md:20] [DIRECTOR-RULINGS.md:29]. A counted face has counters 01-98 only; faces have no sentinels [R9] [DIRECTOR-RULINGS.md:38]. A new counter is never a silent in-place replace (working path D320, D344 [DECISIONS-LOG:380] [DECISIONS-LOG:407]). The page index just points at whichever entries those rules say are current.

**Axioms:** Fits axiom 6: blocks are never edited; a change is a new block [Axioms.md:23]. Fits axiom 5 in spirit: the model is handed only the framed piece it needs [Axioms.md:21].

**Better:** Better than today: today the whole book is replayed to serve one face [format.md:61]. Better than fixed-size blocks in a text file: no padding, no wasted space. Where we fall short: one very large face is still read whole; there is no way to read half a card. Nothing in the sources asks for that yet.

**Three leads:** The person needs a face to look the same as today when they read it: Markdown with `##` cards. The model needs to be given exactly the face (or card) it asked for, with its address and source [AGENTS.md:44]. The compute needs one seek and one read per face.

---

## Step 8. Face 09 as the page's log (Matthew's idea, tested)

Matthew's idea, 16 Nov 2026: the log needs its own space; make face 09 the page's log.

**Where face 09 stands today.** Face 09 is unassigned: "01-09 system faces (01-08 defined, 07 reserved, 09 unassigned)" [decisions.md:182]; the review list says the same [review.md:53]; the face table says "reserved, unassigned" [seqAddr.md:158]. Retiring is done with the tail word `retired` [seqAddr.md:127] [seqAddr.md:138]. So face 09 is free, and it sits in the system face range, which suits a face the compute keeps. (The brief says an older ".09 retired" tail existed and is gone; this plan found no source line that still uses it, so that history is not verified here.)

**What "the log" already is today.** There are four things that could be called a log, and face 09 must not be confused with them:

- The book itself is the log of approved writes [format.md:61]. That is the source of truth.
- The `.seq` page view already has a `~ history` section: one line per booked entry for the page, in book order, across all faces; "it only grows" [seqpage.md:199]. It is derived on export.
- BUILD-LOG is a document of build choices and their whys for the whole repo [BUILD-LOG:3]. It is not a page and not a face.
- Face 06 holds notes: one counter per session, left by models [seqAddr.md:155]. Notes say why and what was found; a log says what happened.

**The test.** Three ways face 09 could work:

- Option L1 (recommended by this plan): face 09 is the page's history, written only by the compute, as a chain of pointers. Each page index line (Step 6) already points to the page index before it. Walking that chain lists every write to the page: entry number, time, who, operation, address, and the reason field where there is one. Face 09 holds **no copies** of bodies. It is shown as face 09 in the `.seq` page view, where the `~ history` section is today. Nobody proposes to face 09, and it is never imported.
- Option L2: face 09 is real stored entries (for example a `put` to `PPPP.09.NN`) that the compute writes after every write. This makes a second copy of what the book already holds. A busy page would pass counter 98 quickly, and what happens after 98 is open (QD16); R9 forbids a `09.99` [DIRECTOR-RULINGS.md:38]. It also doubles the writes.
- Option L3: no face 09. Keep the history as a derived section, as today [seqpage.md:199].

**Honest results of the test.**

- L1 fits Matthew's idea that the log has its own space, and it puts the page's past one hop away from the page. It adds no second copy.
- One thing only L2 can do: hold what is not in the book. Today a refused proposal writes nothing ("Rejected = reasons, nothing written") [BUILD-LOG:53]. If Matthew wants the page log to also record refused attempts, halts, or raised disagreements, then L1 is not enough, because those are not entries. That is a real choice for Matthew (choice C2).
- The log must not log itself. Writing face 09 must not create a new face 09 entry, or it never ends. This is the same trap R25 avoids for face 00 [DIRECTOR-RULINGS.md:101]. Under L1 it cannot happen, because face 09 is never a write of its own.
- Face 09 does not replace the 00 counter of R25. R25 is a ruling; its 00 counter (00.CC) keeps face 00's fingerprints before each change [DIRECTOR-RULINGS.md:101]. Whether 00.CC faces are seated and how they climb are still open (QD66, QD67). This plan leaves them alone.

**Disagreement halts.** If face 09 (or any page index) ever disagrees with the entries it points at, the compute does not pick one. It halts and raises it. This follows working path D324, "neither silently wins; halt and raise it (axiom 1)" [DECISIONS-LOG:384], and working path D367, which halts on a fingerprint mismatch [DECISIONS-LOG:440]. The entries are the source [Axioms.md:27]; a person may then approve rebuilding the derived chain from them.

**Axioms:** Fits axiom 6: the history only grows; the line back is kept with the page [Axioms.md:23]. Fits axiom 8: under L1 face 09 points, and the entries govern; agreement is not connection [Axioms.md:27]. Fits axiom 2 under L1 (no copy of the parent or of the log) [Axioms.md:15]; L2 risks drift. Fits axiom 1: only the compute writes it, and a disagreement is raised, not chosen [Axioms.md:13].

**Better:** L1 is better than today's derived `~ history` section, because the page's past is reachable from the stored file in a few reads, without a full replay. It is better than L2, because there is no second copy to drift and no counter limit. Where we fall short: L1 cannot hold refused or halted attempts, because they are not in the book. And giving face 09 a fixed job means changing the face table, which is Matthew's decision, not this plan's.

**Three leads:** The person needs to open one place and see what happened to this page, in time order, in plain words. The model needs to read that history before drafting, so it builds on the real past and not on memory [drafting.md:7]. The compute needs to keep the history chain short to walk, never write it twice, and halt if it ever disagrees with the entries.

---

## Step 9. Appending a change and writing new maps

New (not in any source), building on what exists: one approved proposal is written in this order, all at the end of the file.

1. The proposal's entries, as today: one or more JSON lines, all or nothing [format.md:100] [BUILD-LOG:38].
2. A new page index line for each page the proposal touched.
3. A new band map line for each band the proposal touched.
4. One new book map line.
5. One fsync, as today [BUILD-LOG:53].

Nothing earlier in the file is changed. Old blocks, old page indexes and old maps all stay. This is Prima's sketch ("changes appended at the end and a new map written, with old blocks kept"), with the two extra levels.

The cost of one write is the entries plus three small derived lines (one page index, one band map of at most 100 rows, one book map of at most 100 rows).

A reseat follows the existing rules: the R24 climb uses a new counter, built from the seat plus the changes [DIRECTOR-RULINGS.md:97]; the newer seated pack carries a write-once `supersedes:` naming the older one (working path D321, D345 [DECISIONS-LOG:381] [DECISIONS-LOG:408]). The maps only point at the result; they decide nothing.

Two copies of a book changed apart are never merged by mixing lines (working path D427 [DECISIONS-LOG:550] [DESIGN.md:167]). The maps help here without deciding QD57: two copies whose book maps have the same fingerprint are the same state, and where they differ, comparing band maps shows which bands changed (new, not in any source).

**Axioms:** Fits axiom 6: "add the new step after it" [Axioms.md:23]. Fits axiom 1: only the compute appends, one proposal at a time, through the queue [Axioms.md:13] [format.md:42]. Fits axiom 8: every new map points at real entries [Axioms.md:27].

**Better:** Better than today because the next reader does not replay; better than rewriting the file, which format.md set aside ("Every write rewrites the file. Does not scale") [format.md:51]. Where we fall short: the file grows by three derived lines per write. A book with many small writes gets a lot of map lines. Writing maps only every so many writes would save space, but then a reader must replay the entries since the last map; that is a builder setting, not a ruling.

**Three leads:** The person needs each change to show up as new lines at the end, so a git diff is a clean addition [format.md:66]. The model needs its proposal to be booked whole or not at all, and to be told which. The compute needs a fixed write order it can recover from after a crash (Step 11).

---

## Step 10. Fingerprints and checks

New (not in any source): every pointer carries the fingerprint of what it points to. The book map carries each band map's fingerprint; each band map row carries its page index's fingerprint; each page index row carries its block's fingerprint. A fingerprint here is a hash of the exact bytes of that line.

This makes a chain. The book map's own fingerprint stands for the whole book state at that moment. To check one face, the compute checks only the lines on the path down to it, not the whole book.

**Not the same as R25's fingerprint.** R25 speaks of face 00's fingerprint before each change, kept on a 00 counter [DIRECTOR-RULINGS.md:101]. Working path D347, filled in by Designer proposal D350 and Tester working path D358 (none of them rulings), defines that fingerprint as face 00's git blob at the parent of the commit that adds the 00.CC, stored as the blob and never as a commit id [DECISIONS-LOG:410] [DECISIONS-LOG:415] [DECISIONS-LOG:427]. That is a git fingerprint of a Markdown source file. The block fingerprints in this plan are hashes of lines inside the book file. They hash different bytes and answer a different question. This plan does not change D347 and does not merge the two.

Which hash: this plan suggests SHA-256 written as plain hex (ASCII). Using git's own blob hash form would let a person check a block with standard git tools, but git's default hash is the older SHA-1. This is a lesser choice; it is listed (choice C7).

**When to check.** Working path D414 says a snapshot is never trusted over the log and is checked on every open [DESIGN.md:165]. If every map had to be fully checked on every open, the compute would read the whole file on open, and the pyramid would lose its fast top. New (not in any source): two ways to meet D414's spirit:

- Check lazily: check each line's fingerprint when it is read, and run a full check in the background or on demand. A mismatch halts (working path D367 [DECISIONS-LOG:440]).
- Check fully on open, as D414 says for snapshots, and accept a slower open.

This touches QD46 (how far a snapshot is trusted). It is not closed here. It is listed for Matthew (choice C4).

**Axioms:** Fits axiom 8: a pointer that cannot be opened, or whose fingerprint does not match, is missing (`7.8`) and is not repaired from memory [Axioms.md:27]. Fits axiom 9: a check from another view before trusting [Axioms.md:29]. Fits axiom 1: a mismatch halts and is raised [Axioms.md:13].

**Better:** Better than today: today nothing inside the book says "this line is intact" except that it parses. Better than one checksum for the whole file: you can check one face without reading everything. Where we fall short: a fingerprint shows damage; it cannot repair it. Repair still means going back to the entries, or to another copy.

**Three leads:** The person needs to be able to check a fingerprint with a common tool, so they are not asked to trust the compute blindly [AGENTS.md:10]. The model needs to know that what it was handed is intact, and to cite it by address plus fingerprint, never by commit id, as working path D348 already does for packs [DECISIONS-LOG:411]. The compute needs fingerprints that are cheap to compute on write and to check on read.

---

## Step 11. Crash safety

What exists: a partly written last line is dropped on load and cut off before the next append [BUILD-LOG:54]; a cut-off multi-op proposal is dropped whole [BUILD-LOG:38]; the compute appends with fsync [BUILD-LOG:53]. Working path D431 (not a ruling) records the hardware as one ordinary computer with a local disk that honours fsync [DECISIONS-LOG:558].

New (not in any source): with the write order in Step 9, a crash can only leave one of these:

- A cut-off entry, page index or map at the very end. The existing rule drops it [BUILD-LOG:54].
- Whole entries with no new map after them (the crash came before step 4). The compute finds the last good book map, then replays only the entries after it, and writes a fresh map. Nothing is lost, because the entries are complete and the maps are derived.
- A map whose fingerprints do not match. It is not used; the compute walks back to the map before it (`prev`), and raises it.

The worst case is always: ignore every map and replay the whole book, exactly as today. So the new layout can never be less safe than today's.

**Axioms:** Fits axiom 6: recovery only adds; it never rewrites an earlier line [Axioms.md:23]. Fits axiom 7: a damaged map is treated as missing, not guessed [Axioms.md:25]. Fits axiom 1: a damaged map is raised, not silently replaced [Axioms.md:13].

**Better:** As safe as today, and faster to recover after the common case (a crash after the entries but before the map). Better than an edit-in-place index, which can be half-written in the middle of the file. Where we fall short: it still needs a disk that honours fsync (D431). On a disk that lies about fsync, no file layout is safe, and this plan does not fix that.

**Three leads:** The person needs to know that a crash cannot eat old work, and to be told plainly when a map was damaged. The model needs its proposal to be either fully booked or clearly not booked after a restart. The compute needs a recovery rule that is short, tested, and always falls back to full replay.

---

## Step 12. Tidying old blocks without losing history

Over time the file fills with old maps and old page indexes. format.md already says older entries "can be moved to an archive file if size becomes a problem" [format.md:105], and lists the archive policy as open [format.md:157]. Working path D414: no entries are archived until an archive can still be opened and is checked with the book [DESIGN.md:165].

Options (new framing, not in any source):

- Option K1 (this plan, for now): never tidy. Books are small today (about 233 KB in total). Nothing needs tidying yet.
- Option K2: a new generation. The compute writes a new book file that starts with the header, then the current state of every page, then fresh maps. The new file's first entry points back to the old file by name and fingerprint; the old file is frozen, kept, and checked with the book. Old maps are dropped from the new file only, never from the old one. History is one link away.
- Option K3: cut old lines out of the file. **Set aside**: it rewrites the past and breaks axiom 6 [Axioms.md:23].

Whether K2 may ever be done, and who approves it, is Matthew's choice (choice C5).

**Axioms:** K1 and K2 fit axiom 6: nothing old is rewritten; K2 adds a new step and links back [Axioms.md:23]. K2 fits axiom 8 only if the link is written both ways [Axioms.md:27]. K3 breaks axiom 6.

**Better:** K1 is the simplest and safest for now. K2 is better than K3 because the past stays whole and can be opened. Where we fall short: K2 makes a book two (or more) files, which strains "a book is one file" [format.md:21] and Matthew's "self-contained". That trade-off is his.

**Three leads:** The person needs to approve any tidy, and to be able to open the old file afterwards. The model needs to be able to cite an old version by address and fingerprint even after a tidy. The compute needs a tidy that is all or nothing, checked, and never touches the frozen file.

---

## Step 13. Books pointing to books

What exists: finding looks up book, then shelf, then desk, then kernel; the first match wins [seqAddr.md:101] [seqAddr.md:104]. Books follow the kernel live; they do not copy it [decisions.md:128]. Links live on face 08 [seqAddr.md:157]; every target links back, and a one-way link is invalid [seqAddr.md:251]. The kernel is a book file too [format.md:28].

New (not in any source): a book file points to another book **by address only**, never by byte offset into the other file. Offsets belong to one file and change if that file is tidied (Step 12). Addresses are "ranked so it is stable to store" [Axioms.md:23].

Where a link must name an exact version, it may add the target's fingerprint: address plus fingerprint, the same way working path D348 cites packs by address plus blob [DECISIONS-LOG:411]. A pinned link whose fingerprint no longer matches is shown as stale and raised, not followed silently.

"Self-contained" then means: a book file holds all of its own pages and their history. It does not hold copies of what it inherits. Copying the parent is what axiom 2 forbids [Axioms.md:15]. A borrowed face is shown from its source, at most as a derived line (working path D403 [DESIGN.md:189]).

**Axioms:** Fits axiom 8: connection by written link, both ways; a pointer never becomes what it points to [Axioms.md:27]. Fits axiom 2: inherit, do not copy [Axioms.md:15]. Fits axiom 6: travel by written connections, not by what matches [Axioms.md:23].

**Better:** Better than pointing by offset, which breaks on tidy. Better than copying inherited pages in, which drifts. Where we fall short: a book is not fully self-contained for reading; a page that inherits faces needs its shelf, desk and kernel files present. That is by design, but it means "send one file" does not always send everything a reader sees.

**Three leads:** The person needs to see where a borrowed face came from. The model needs full addresses, stated back in full when the user wrote short form [seqAddr.md:95]. The compute needs to resolve across files by address, and elevate anything it cannot find, never guess [seqAddr.md:104].

---

## Step 14. Language choice

What exists: format.md marks Rust as decided for the core library and the compute, and TypeScript with Next.js for the app [format.md:139] [format.md:140] [format.md:141]. The core and the compute are already Rust crates in the repo (`crates/seqaddr-core`, `crates/compute`, `crates/seqpage`). Prima recommended Rust for the real book file.

This plan agrees: write the book file reader and writer in Rust, inside the core, so there is one implementation. format.md gives the why: "One parser everywhere", "The rules become types", "It suits a file format" [format.md:145] [format.md:146] [format.md:147].

Trade-offs, said plainly:

- Rust is slower to change than TypeScript or Python, and fewer people can read it.
- The app would need the core built for the browser (WebAssembly). That is not built yet [BUILD-LOG:66]. Until it is, the app reads through the compute [BUILD-LOG:6], which is fine.
- A quick prototype in another language would be a second implementation, and two parsers can disagree. format.md set aside "TypeScript for everything" for this reason [format.md:149].
- Matthew does not read code. So the person's check is not the Rust. It is this plan in plain words, the file itself in plain text, and a small read-only dump tool (new) that prints the pyramid for a book.

**Axioms:** Fits axiom 2: do not reinvent what already exists; the core is Rust [Axioms.md:15]. Fits axiom 4: the why is recorded [Axioms.md:19]. Fits axiom 3: compute work in the compute's own form [Axioms.md:17].

**Better:** Better than a second language for the same file. Where we fall short: the WebAssembly build is missing, and Rust raises the cost of quick experiments.

**Three leads:** The person needs a plain-words spec and a dump tool, not code. The model needs one API from the compute, over HTTP, as today (working path D426 [DECISIONS-LOG:548]). The compute needs one fast, typed implementation it can trust not to corrupt a book [format.md:140].

---

## Step 15. Moving today's books to the new layout

What exists: books are version 1 JSON-line logs [format.md:60] [BUILD-LOG:54]. The kernel builder rewrites each `books/*.book` whole on every build, renumbering from 1 [R23-R25-lineage.md:94]. So today the kernel book is not truly append-only.

New (not in any source):

- Option M1 (this plan): for each book, write a new version 2 file: the new header, then every version 1 entry copied **byte for byte**, with the same entry numbers, then the first maps. The old file is kept, frozen, as history, and the new file's first map names it by fingerprint. Nothing in any entry changes.
- Option M2: keep version 1 and just add `map` lines. Old readers would meet an unknown operation; a clean version bump is safer.

Before any move, two things must be true: the round trip book to `.seq` to book still gives back the same entries [DIRECTOR-RULINGS.md:12] [seqpage.md:208]; and the kernel builder appends instead of rewriting, or the maps are rebuilt on every build and the kernel's history is lost again [R23-R25-lineage.md:94]. Neither is done. This plan does not do them; they are build work after Matthew approves.

**Axioms:** Fits axiom 6: entries are copied unchanged; the old file is kept [Axioms.md:23]. Fits axiom 9: before replacing the old format, open it and test the new one against it [Axioms.md:29].

**Better:** Better than converting entries into a new shape, which would risk changing what they say. Where we fall short: the kernel builder's whole-file rewrite is a real gap today, and the new layout does not fix it by itself.

**Three leads:** The person needs to approve the move and to be able to compare old and new files line by line. The model needs no change: it still proposes by address. The compute needs to read both versions during the move, and refuse a version it does not know.

---

## Step 16. How this plan should be trialled

This plan is `9`: it has not faced a hostile trial [Axioms.md:29]. Before anything is built, a different view (Tester) should try to break it. New (not in any source), suggested tests:

1. Crash at every byte of a write (entries, page index, band map, book map). The book must reopen to the last good state every time.
2. Delete or damage every map. A full replay must rebuild the same maps, byte for byte.
3. Forge a map that points at the wrong entry with a matching-looking row. The fingerprint check must halt it.
4. Round trip: book to `.seq` page views to book must stay lossless with map lines present.
5. A page with a type nobody has defined: it must be stored, routed and shown as written, with a finding.
6. Face 09 (option L1) must list exactly the page's entries, in book order, and match today's `~ history` section.
7. A book of 10,000 pages: opening and reading one face must touch only the five levels.
8. Two copies changed apart: the book map fingerprints must show they differ, and nothing may merge them by mixing lines.

**Axioms:** Fits axiom 9: a hostile pass from another view before promotion [Axioms.md:29]. Fits axiom 1: Matthew approves. R2's build-stage approval lets a face be seated after a trial [DIRECTOR-RULINGS.md:9]; it does not speak of changing the file format, so this plan reads that change as Matthew's to approve [Axioms.md:13].

**Better:** Better than building first and testing after. Where we fall short: these tests are a list, not code; none of them exist yet.

**Three leads:** The person needs the trial results in plain words before deciding. The model (as Tester, a fresh session per R20) needs the plan and the sources, read-only. The compute needs the tests to run on real book files, not only on samples.

---

## Open choices only Matthew can decide

Each is a plain question, with the options and what each would mean. The top three are marked **TOP**. None of these is answered here.

**C1 (TOP). Which file is "the .seq file"?**
R3 says the book is the real copy and a `.seq` file is a view of one page [DIRECTOR-RULINGS.md:12]. Today you said a book is a .seq file.
- Option A: the book file takes the `.seq` name. Then today's one-page view needs a new name. R3's meaning (book is the real copy, page view round-trips) stays; only names change.
- Option B: books keep `.book`, and `.seq` stays the one-page view. Your sentence is read as "a book is the real seq file", and nothing is renamed.
- Option C: something else you have in mind.

**C2 (TOP). Should face 09 be the page's log, and what goes in it?**
Face 09 is unassigned today [decisions.md:182].
- Option L1 (this plan's pick): face 09 is the page's history, written only by the compute, as pointers to the real changes. No copies. It can only show approved writes.
- Option L2: face 09 holds stored log lines of its own. It could also record refused attempts, halts and raised disagreements, which are not in the book today. But it is a second copy, and it hits the counter-98 limit (QD16).
- Option L3: leave face 09 unassigned and keep history as a worked-out section, as today.
- Also: should the log record refused or halted attempts at all? If yes, only L2 can do it.

**C3 (TOP). Plain text or binary for the book file?**
R4 says stored files are plain ASCII plus newline [DIRECTOR-RULINGS.md:16]. This plan keeps R4.
- Option T1 (this plan's pick): plain text at every level. You can read it in any editor. A bit slower and larger.
- Option T2: binary. Faster and smaller, but it conflicts with R4 and with "must be checkable by a person" [AGENTS.md:10]. It needs your ruling to change R4, which this plan does not ask for.
- Option T3: SQLite, already named as the fallback if the log is too slow [format.md:54]. Also binary, also conflicts with R4.

**C4. How much should the compute trust a map when it opens a book?**
Related to QD46 (working path D414 says a snapshot is checked on every open).
- Option A: check fully on every open. Safest; opening a big book is slow.
- Option B: check each piece as it is read, and run a full check in the background or on demand. Fast; damage in an unread part is found later. A mismatch always halts.

**C5. May old lines ever be tidied away?**
- Option K1 (this plan's pick for now): never.
- Option K2: the compute may start a new file generation, with the old file frozen and linked. Then say who approves it, and when.
- Option K3 (set aside, breaks axiom 6): cut old lines out.

**C6. Is a band level wanted, or one flat map?**
- Option A (this plan's pick): book map, then band maps of up to 100 pages each [seqAddr.md:240]. More levels, small writes.
- Option B: one flat map with a row per page. Simpler, but the whole map is rewritten after each change.

**C7. Which fingerprint?** (lesser; builders could choose and record why)
- Option A: SHA-256 as plain hex.
- Option B: git's blob hash form, so a person can check with git tools.

**C8. Must a book be readable alone?**
- Option A (as designed): a book holds its own pages only; inherited faces come from the shelf, desk and kernel files [decisions.md:128].
- Option B: an export option that bundles the inherited faces, as a view, for sending one file to someone.

---

## Related open questions (named, not closed)

- QD34: is the `.seq` file layout OK [QUESTIONS-FOR-DIRECTOR.md:298]. This plan does not answer it.
- QD46: snapshot trust (C4 above) [QUESTIONS-FOR-DIRECTOR.md:360].
- QD16: what happens after counter 98 (affects option L2) [QUESTIONS-FOR-DIRECTOR.md:180].
- QD57 / D427: two copies changed apart [QUESTIONS-FOR-DIRECTOR.md:414].
- QD60 / D431: hardware; a local disk that honours fsync [QUESTIONS-FOR-DIRECTOR.md:430].
- QD63 / D432: accented letters; R4 stands [QUESTIONS-FOR-DIRECTOR.md:446].
- QD66, QD67: how 00 counter faces are seated and climb; face 09 does not replace them [QUESTIONS-FOR-DIRECTOR.md:66] [QUESTIONS-FOR-DIRECTOR.md:76].
- QD65 stays with Matthew; this plan does not touch it.

---

## Sources

- `docs/spec/Axioms.md` (the nine axioms): lines 13, 15, 17, 19, 21, 23, 25, 27, 29.
- `docs/spec/DIRECTOR-RULINGS.md`: R3 (:12), R4 (:15-16), R5 (:20, :29), R9 (:38), R10 (:41), R19 (:76), R2 (:9), R24 (:97), R25 (:101).
- `docs/spec/AGENTS.md` (the brief): lines 10, 41, 44, 45.
- `docs/spec/format.md` (book format): lines 12, 15, 18, 21, 25, 28, 42, 51, 54, 60, 61, 66, 70, 74, 79, 81, 86, 88, 100, 102, 105, 139-149, 157.
- `docs/spec/seqAddr.md` (addresses): lines 7, 95, 101, 104, 127, 138, 150, 152, 153, 155, 157, 158, 168, 240, 251.
- `docs/spec/seqpage.md` (the page view): lines 11, 13, 84, 199, 206, 208.
- `docs/spec/face00.md` (face 00 draft): lines 146, 177, 179.
- `docs/spec/decisions.md`: lines 128, 182, 285.
- `docs/spec/review.md`: line 53.
- `docs/spec/drafting.md`: line 7.
- `docs/design/DESIGN.md`: lines 17, 165, 167, 189.
- `docs/design/DECISIONS-LOG.md` (working paths, not rulings): D320 (:380), D321 (:381), D324 (:384), D344 (:407), D345 (:408), D347 (:410), D348 (:411), D350 (:415), D358 (:427), D367 (:440), D426 (:548), D427 (:550), D431 (:558).
- `docs/design/R23-R25-lineage.md`: line 94.
- `docs/design/QUESTIONS-FOR-DIRECTOR.md`: QD16, QD34, QD46, QD57, QD60, QD63, QD66, QD67.
- `docs/BUILD-LOG.md`: lines 3, 6, 38, 53, 54, 66.
- Matthew's words, 16 Nov 2026 (passed on by Prima): ideas, not rulings.
