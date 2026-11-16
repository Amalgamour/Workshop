# The .seq book file: a design plan

state: draft plan, `7` (open). Not a ruling. Nothing here is law.
made: Mon 16 Nov 2026, Designer (design partner for Prima). Director: Matthew, the only approver.
revised: Mon 16 Nov 2026, after Director answers t171u (11:16 AM EST) and t172u (11:17 AM EST), both relayed by Prima. See "Changes since 29ec433".
why: Matthew asked today (16 Nov 2026, 11:04 AM EST, passed on by Prima) for a design plan for the book file. He said a book is a .seq file, it is basically a self-contained database file, and it should work like a pyramid.
status of every idea below: Matthew's first ideas from today are marked "Matthew's idea, 16 Nov 2026". His later answers are marked "Director answer, t171u (relayed by Prima), not yet a numbered ruling" or "Director answer, t172u (relayed by Prima), not yet a numbered ruling". None of them is a numbered ruling yet. Anything not found in a Workshop source is marked "New (not in any source)". Rulings R1-R25 are quoted only where they already exist.
does not: edit DESIGN.md, the kernel, the core, or any spec file; close any QD question; write a 00.counter; seat anything.

---

## Plain-words summary

Matthew has now answered most of the first questions. This summary says where the plan stands after his answers.

The real copy stays in small files. Matthew said: "we can keep small files then have the ability to export books later." So the stored copy is a set of small files, as today. A whole book as one `.seq` file is something you export, for example to send or back up.

The pyramid is now the shape of that exported file. The top loads fast and tells you where everything is. You open only the deeper parts you need. The computer may also keep the same signposts over the small files, so finding any page is quick. The signposts are never the real copy. They can always be rebuilt.

Face 04 is the person's face. It stays plain text a person can read. Matthew said every other face "can just be code": a compact form for the computer. That would narrow his ruling R4 to face 04 only. Until he makes that a numbered ruling, R4 stands for every face, so every face stays plain ASCII for now.

Addresses, titles and card keys stay plain ASCII in every case. They are how people and computers find things.

Face 04 keeps its history the way Google Docs does. Matthew said "go with Google's approach". Each edit is stored as a small change, with a full copy every so often. The current view is the latest version. Every old version is kept.

He also said "So they can't be changed". What he meant is still unclear, and Prima has asked him. For now this plan reads it as "old versions can't be changed". That reading is provisional.

Face 09 is the page's log. Matthew agreed. The log says what happened to the page, who did it, and when.

Matthew asked whether a short log in face 00 would be better. This plan says no. Face 00 should stay small and change rarely (ruling R25). A short log there would change face 00 on every write, and it would be a second copy of face 09. The computer can keep a "last change" signpost outside face 00 instead, which is just as fast.

Links point to a page, never to a face. Matthew said: "our 2.2.2.4.title we don't include the face its a sub group of the page." So a link names the page address and its title. Once you reach the page, you open the face you need.

The real thing should be written in Rust, like the core and the compute today. The person still checks it in plain words, not in code.

Three choices matter most now. What exactly are the small files? Does "code" mean raw computer bytes, or a compact form that is still plain text? Should face 09 also record attempts that were refused or stopped? They are at the top of the open choices list.

---

## Changes since 29ec433

29ec433 was the first version of this plan. f6296ba added Step 17 (face 04, t172u). This version adds Matthew's t171u answers. Old commits are not changed; this is a new step on top (axiom 6) [Axioms.md:23].

- **A1 (t171u), faces as code.** New in Step 3, Step 7, Step 11 and Step 14. Face 04 stays readable; other faces may be compact code. This is a pending narrowing of R4 to face 04 and needs a numbered ruling. Until then R4 stands. C3 is updated.
- **A2 (t171u), small files stored, books exported.** Steps 1, 2, 4, 5, 6, 9, 10 and 15 are reframed: the pyramid and book signpost are now the export format, and possibly a derived signpost over the small files. The stored form is the small files. C1 is updated, and the git-blob fingerprint flag in Step 10 is updated.
- **A3 (t171u), face 09 is the log.** Step 8 is rewritten: face 09 is the page log (his answer). The short log in face 00 is judged: no, with the reason. C2 is updated; whether refused or halted attempts are logged stays open.
- **A4 (t172u), face 04 history.** Step 17 (added in f6296ba) is kept. "Go with Google's approach" settles it. The Google Docs against Word comparison is kept only as the reason. C9 ("So they can't be changed") is kept, still open.
- **A5 (t171u), links name pages, not faces.** Step 13 is rewritten and checked against seqAddr.md.
- **Open choices.** C1, C3, C6, C7 and C8 are marked "updated by t171u". C2 is updated by t171u (A3). The top 3 are recomputed. A "Still open" list is added.
- **Summary.** Rewritten above.
- **Tester's stress test folded in** (docs/design/SEQ-FILE-PLAN-TEST.md, commit 50fdfac; Tester's file not edited). Fix 1: a running chain hash on every signpost line, checked once at compute start; answers `7` until then; a mismatch halts (D324); D414 kept (Steps 5, 10, C4). Fix 2: signpost lines hold only changed rows, with a full line every K writes (Steps 5, 9). Fix 3: the compute checks a hash of earlier bytes before each append, and the builder writes elsewhere or appends instead of rewriting whole files (Steps 11, 15). Cite notes: the builder's whole-file write is now cited at `kernel/build.mjs:846`; D326 is cited in Step 6; the example signpost line now has the book `addr`.
- **Rename: "map" is now "signpost".** "Map" is face 08's name [seqAddr.md:157] and "index" is used for the dictionary [seqAddr.md:230], so the plan's book map, band map and page index are now the book, band and page signposts.

---

## Director answers today (not yet numbered rulings)

Each of these is quoted as relayed by Prima. None is a numbered ruling in DIRECTOR-RULINGS.md yet. Where one would change a ruling, this plan says so and keeps the ruling as written until Matthew numbers the change.

- **A1. Director answer, t171u (relayed by Prima), not yet a numbered ruling.** "It can just be code. for every face other then 04." Read: face 04 stays human-readable; the other faces may be compact computer code. If confirmed as a ruling, this narrows R4 [DIRECTOR-RULINGS.md:16] to face 04 for face content. Until then, R4 as written stands.
- **A2. Director answer, t171u (relayed by Prima), not yet a numbered ruling.** "we can keep small files then have the ability to export books later." Read: small files stay the stored form; the whole-book `.seq` file is an export.
- **A3. Director answer, t171u (relayed by Prima), not yet a numbered ruling.** "agreed 09 is log, we keep a short log in 00 if you think that is a superiour design." Read: face 09 is the page log. The short log in 00 is left to the design's judgment (Step 8: no).
- **A4. Director answer, t172u (relayed by Prima), not yet a numbered ruling.** "go with Google's approach." Read: face 04 edits are stored as a log of small changes plus a full copy every so often (Step 17). His phrase "So they can't be changed" is still unclear (C9).
- **A5. Director answer, t171u (relayed by Prima), not yet a numbered ruling.** "We use the seqaddr system. our 2.2.2.4.title we don't include the face its a sub group of the page." Read: links point to a page address plus its title, never to a face (Step 13).

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
- **Signpost** (new name): what the first two versions of this plan called a "map" (book map, band map) and a "page index". Renamed because "map" is already the name of face 08 [seqAddr.md:157], and "index" is already used for the dictionary, "an index from each word to its brand cards" [seqAddr.md:230]. "Signpost" is used nowhere else in the sources.
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
- Face 09 is unassigned in the spec [decisions.md:182] [review.md:53] [seqAddr.md:158].
- The kernel keeps its sources as small files, one Markdown file per face (for example `kernel/00.00.00/00.00.00.0051.01.draft.md`), and builds them into the kernel book; seats are pinned to the git blob of those files [R23-R25-lineage.md:94].
- Size today: the four book files in `books/` hold 71 lines and about 233 KB in total (measured with `wc` on 16 Nov 2026). The kernel book is the largest, about 205 KB in 51 lines.

---

## Step 1. Names and levels: small files stored, whole books exported

Matthew's idea, 16 Nov 2026: "A book is a .seq file." A book holds pages. A page is a small multi-dimensional book broken into pieces, one piece (a *face*) for each lead. Face 00 is the page's registry face. It says what kind of page it is.

**Updated by A2 (Director answer, t171u (relayed by Prima), not yet a numbered ruling):** "we can keep small files then have the ability to export books later." So there are two forms:

- **The stored form: small files.** This is the real copy, the one the compute writes.
- **The export: one whole-book `.seq` file.** It is made from the small files when someone wants the book as one file. It is read back only through the normal proposal queue, as page views are today [DIRECTOR-RULINGS.md:12] [seqpage.md:14].

The levels match the existing design: books contain pages, pages contain faces, faces contain cards [AGENTS.md:41]. A page is one object with several faces, each a view for a different reader [format.md:12] [seqAddr.md:7]. The "one face for each lead" idea has a footing in the face table: face 01 is for agents (the model) [seqAddr.md:150], face 03 for the compute [seqAddr.md:152], face 04 for users (the person) [seqAddr.md:153].

**What "small files" means is not settled.** Three readings fit his words (new framing, not in any source):

- Option S1: one small log file per book, as today (`books/10.11.21.book` and the others) [format.md:25]. R3 is unchanged: the book file is the real copy [DIRECTOR-RULINGS.md:12]. The export is a new, faster-to-read shape of the same book.
- Option S2: one small file per page. Today's one-page `.seq` view would become the stored form. That reverses R3's "the book is the real stored copy" and needs a numbered ruling.
- Option S3: one small file per face (and per counter). The kernel already keeps its sources this way: one Markdown file per face, for example `kernel/00.00.00/00.00.00.0051.01.draft.md`, built into the kernel book by the builder. Seats are already pinned to the git blob of those files [R23-R25-lineage.md:94]. This also changes R3 and needs a numbered ruling.

**Plan's lean (new, not a ruling):** S3 fits Matthew's other answers best. Face 04 can stay a readable Markdown file with its own history (Step 17). The other faces can be compact files (A1, Step 3). Face 09 can be the page's own log file (A3, Step 8). Each file has a git blob fingerprint that git and the kernel builder already use (Step 10). The old reason against "a folder of files per page" was "No single file to export" and "'Rename is a claim' only works on one disk" [format.md:50]. A2's export answers the first; the compute's queue already handles claims [format.md:41] [format.md:42], which answers the second. S1 is the safe fallback: it changes the least. Only Matthew can choose (choice C1).

**Names.** R3 calls the `.seq` file a one-page view [DIRECTOR-RULINGS.md:12]. Matthew now calls the exported whole book a `.seq` file. Under S1 the stored book file can keep `.book`. Under S2 or S3, each small file needs a name pattern built from its address. Either way the one-page view needs either a new name or a clear note that `.seq` now has two shapes (one page, or a whole book). This is part of C1.

**Axioms:** Fits axiom 2: the same shape at every scale; a page is "a small book", and the export is the same book in one file [Axioms.md:15]. Fits axiom 3: one face per lead [Axioms.md:17]. Fits axiom 8: the export is a copy, and "a copy ... never becomes what it points to" [Axioms.md:27]; the small files govern. S2 and S3 would change R3, which only Matthew can do [Axioms.md:13].

**Better:** Better than making the big file the stored copy: small files are quick to write, each change touches only the file it changes, and git shows exactly which piece changed. The export still gives Matthew his "self-contained database file" when he wants one. Where we fall short: "small files" has three readings, and two of them change R3. Until Matthew picks one, the stored form is not fixed.

**Three leads:** The person needs one name per thing, so they can tell the stored small files from an exported book. The model needs to write only proposals, never an export and never a small file directly [AGENTS.md:42]. The compute needs one stored form it alone writes [format.md:18], and an export it can build from it on request.

---

## Step 2. The pyramid: the export shape, and a signpost over the small files

Matthew's idea, 16 Nov 2026: the top loads quickly; deeper information is reached later; only what is needed is loaded, but getting to any point is quick. This fits the brief: "Return only the context needed, with its source and governing rules" [AGENTS.md:44].

**Updated by A2 (t171u):** the pyramid is now the shape of the **exported** whole-book `.seq` file. The same rows can also serve as the compute's **signposts** over the stored small files. In both uses it is derived. It is never the real copy.

New (not in any source): the pyramid, top to bottom.

```
level 0  header line (line 1)          what this file is, its version, its book address
level 1  book signpost (the last signpost line)  one row per band of 100 pages: where its band signpost is
level 2  band signpost                      one row per page: kind, title, where its page signpost is
level 3  page signpost                    one row per face: state, where its current block is
level 4  face block                    the face itself
level 5  page history (face 09)        the page's log, reached from the page signpost
```

In the export, "where" means a byte offset in the one file. In the signpost over small files, "where" means a file name built from the address. The rows are the same.

To read one face, the compute reads the top, then one band row, then one page signpost, then the face. That is a fixed, short path, however large the book is.

The bands follow the existing page layout. Every band is exactly 100 pages, `PP00-PP99` [seqAddr.md:240]. So a band signpost never holds more than 100 rows, and the book signpost never holds more than 100 rows.

**Axioms:** Fits axiom 2: the same shape at every scale; a book signpost lists bands, a band signpost lists pages, a page signpost lists faces [Axioms.md:15]. Fits axiom 8: each level points down, and "a pointer points; the source governs" [Axioms.md:27]. The small files are the source.

**Better:** Better than today for large books: today every open replays every entry [format.md:61]. Better than a single flat signpost: a band signpost is at most 100 rows. Better than making the pyramid the stored form: the stored small files stay simple, and the pyramid can be rebuilt at any time. Where we fall short: books today are small (about 233 KB in total), so the gain is not felt yet. Today the compute reads every book at start and serves from memory (`crates/compute/src/store.rs:1009-1023`), so the pyramid mainly speeds up start-up and memory use, not each request (Tester's finding). And keeping signposts means one more thing that must agree with the files.

**Three leads:** The person needs to see the same pyramid when they open an exported book, top line first, so they can follow it by hand. The model needs to be handed only the face it asked for, with its address and source [AGENTS.md:44]. The compute needs a short path to any face, and to rebuild the signpost or the export from the small files whenever asked.

---

## Step 3. Plain text and "code" faces (R4, and A1 pending)

**What R4 says today.** Stored files use printable ASCII 0x20-0x7E plus newline; any other byte is rejected on write, and a book holding one is damaged on read [DIRECTOR-RULINGS.md:16]. Matthew's words were "We want a simple storage design for now" [DIRECTOR-RULINGS.md:15]. The brief says the store "must be checkable by a person" [AGENTS.md:10] and weighs "human inspection" [AGENTS.md:45].

**Updated by A1 (Director answer, t171u (relayed by Prima), not yet a numbered ruling):** "It can just be code. for every face other then 04." Read: face 04 stays human-readable; the other faces may be compact computer code.

**What this does to R4.** If Matthew confirms A1 as a numbered ruling, it narrows R4 for face content to face 04 only. **Until then, R4 as written stands for every face and every stored file.** This plan does not narrow R4 on its own. It is a pending change that needs a numbered ruling.

**What stays ASCII in every case.** Addresses, titles, card keys, tail words, identities and tokens stay plain ASCII always. Working path D432 says so for any widening [DECISIONS-LOG:560], and the address grammar only allows digits, lowercase letters and hyphens [seqAddr.md:112] [seqAddr.md:280] [seqAddr.md:281]. File names are built from addresses, so they stay ASCII too. A1 would touch face content only, never how things are found.

**What "code" could mean.** His words do not say. Two readings (new framing, not in any source):

- Reading A: compact text. A short, strict machine form, written only in printable ASCII (for example terse JSON). This is allowed **today** under R4. It needs no ruling. It loses easy reading for people, but keeps every R4 check.
- Reading B: raw bytes (binary). Smallest and fastest. This **needs** A1 as a numbered ruling, because R4 refuses any byte outside 0x20-0x7E plus newline.

A third path, writing raw bytes as ASCII letters (for example base64), keeps R4's bytes rule. But it gives neither easy reading nor small size, and it is close to the "ASCII escapes" offer that the Read of R4 refuses today for text [DECISIONS-LOG:560]. This plan does not recommend it.

**Plan's pick for now (new):** Reading A (compact plain text) for faces other than 04, because it needs no ruling and keeps every check working. Reading B only after A1 is a numbered ruling and the trials in Step 16 pass.

**The why must stay readable.** Every 01 or 02 card already needs a 04 card with a `why:` line and a body [seqAddr.md:175] [seqAddr.md:184]. So even if 01 and 02 become code, the person still reads every why in face 04. That is what keeps the store checkable by a person under A1.

**Options for C3 (updated by t171u):**

- Option T1: plain ASCII text for every face (R4 as written; today).
- Option T1c: face 04 plain text; other faces compact plain text (Reading A). Allowed now. Plan's pick for now.
- Option T2: face 04 plain text; other faces raw bytes (Reading B). Needs A1 as a numbered ruling narrowing R4.
- Option T3: SQLite [format.md:54]. Binary for everything, including face 04, so it conflicts with R4 and with A1's "04 stays readable". Set aside.

**Axioms:** Fits axiom 1: R4 is Matthew's ruling and A1 is his answer; this plan keeps R4 until he numbers the change [Axioms.md:13]. Fits axiom 4: the why of keeping face 04 readable is recorded (person-checkable) [Axioms.md:19]. Fits axiom 7: what "code" means is unknown, so it stays an open question, not a guess [Axioms.md:25].

**Better:** A1 is better than "all plain text" for speed and size on faces people do not read directly, and better than "all binary" because the person's face and every why stay readable. Where we fall short: a person cannot read a code face without a tool, so the compute must show a decoded view, and that view becomes something people trust. And until A1 is numbered, the plan cannot use raw bytes at all.

**Three leads:** The person needs face 04, with every why, to stay plain text they can read in any editor. The model needs code faces turned into text it can read before it drafts; face 01 is meant to be "model-efficient" [seqAddr.md:150], which is not the same as compact for the compute. The compute needs one strict decoder per face kind, and to refuse any byte R4 refuses until a numbered ruling says otherwise.

---

## Step 4. The header (level 0, line 1)

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

Today line 1 is the header: format name and version, and the book's address [format.md:79]. The compute already checks that the version is 1 and that the address matches the file name, and refuses to start if the kernel fails [BUILD-LOG:54].

Prima's sketch put "where the signpost is" in the header. This plan does not, and here is why. The header is line 1. If it had to say where the newest signpost is, line 1 would change after every write. That is an edit in place, and format.md says "Nothing is ever edited in place" [format.md:61].

New (not in any source): the header is written once and never changes. It holds the format name, the version, and the book address, as today. A new version number (for example `"seqbook":2`) tells an older reader to refuse the file cleanly instead of misreading it. The newest signpost is found from the end of the file instead (Step 5).

Example (new, for illustration only):

```
{"seqbook":2,"address":"10.11.21"}
```

**Axioms:** Fits axiom 6: line 1 is never rewritten [Axioms.md:23]. Fits axiom 7: a reader that does not know version 2 refuses rather than guesses [Axioms.md:25].

**Better:** Better than Prima's sketch, because a header that points to the signpost would have to be rewritten after every change. Better than today only in that it gives the new layout a clean version line. Where we fall short: bumping the version means every book must be moved to the new layout once (Step 15), and old tools stop reading new books.

**Three leads:** The person needs line 1 to say plainly what the file is and which book it holds. The model needs nothing more than that, and should never write line 1. The compute needs line 1 to be fixed, so it can check the version and address on every open [BUILD-LOG:54].

---

## Step 5. The book signpost, found from the end (level 1)

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

New (not in any source): after each approved proposal, the compute appends a fresh **book signpost** line at the end of the file. The newest book signpost is always the last signpost line in the file. Older signpost lines stay where they are.

To open a book, the compute reads line 1, then reads backward from the end of the file to the last signpost line. Normally that is the very last line.

The book signpost has one row per band that has pages: the band (`PP`), where that band's newest band signpost sits (byte offset and length), and that band signpost's fingerprint (Step 10). Each signpost line also names the offset of the signpost before it, so older signposts can be walked back.

A signpost line is a book-level entry written only by the compute, like a `snapshot` [format.md:88]. Book-level entries belong to no page and stay in the book on export [seqpage.md:206]. So the `.seq` page view does not change, and the R3 round trip stays lossless [DIRECTOR-RULINGS.md:12].

Example (new, for illustration only):

```
{"n":42,"at":"2026-11-16T16:30:00Z","by":"compute","op":"signpost","addr":"10.11.21","level":"book","chain":"sha256:...","prev":20480,"bands":[["00",18800,412,"fp:..."],["10",22010,388,"fp:..."]]}
```

**Tester fix 2 (signpost growth), folded in from SEQ-FILE-PLAN-TEST.md:** a book or band signpost line holds **only the rows that changed**, plus `prev`, the offset of the signpost line before it. Every K writes the compute writes a **full** signpost line with every row. A reader walks back at most K signpost lines to put the full picture together. Tester measured that full lines on a full book would add about 20 KB per write and about 200 MB per 10,000 writes; changed-rows-only lines remove that (SEQ-FILE-PLAN-TEST.md section b). K is a builder setting, recorded with its why [AGENTS.md:45].

**Tester fix 1 (the open check), folded in:** every signpost line carries a **running chain hash** of every byte of the file before it (`chain` in the example). See Step 10.

A signpost is derived from the entries. It is never written by a person or a model, and never proposed. Boards, contents lists and path lists are already "derived from the log and never written as entries" [format.md:102]. The signpost is the same kind of thing, written down only so the compute can find it fast. Whether writing a derived line into the book is allowed at all is the same question as for snapshots (QD46, working path D414); this plan names it, and does not close it.

**Axioms:** Fits axiom 6: new signposts are added after the old ones; nothing earlier is touched [Axioms.md:23]. Fits axiom 8: the signpost is a pointer; the entries govern [Axioms.md:27]. Fits axiom 1 if only the compute writes signposts [Axioms.md:13] [format.md:18].

**Better:** Better than a header pointer: no edit in place. Better than today: opening a book reads two lines, not every line. This is the same trick other single-file formats use to stay append-only (new, not in any source). Where we fall short: every write now adds at least one extra line (a signpost), so the file grows faster. Tidying (Step 12) is the answer, and it is a choice for Matthew.

**Three leads:** The person needs to find the newest signpost by looking at the last lines of the file, with no special tool. The model needs nothing from the signpost directly; it asks the compute by address. The compute needs the signpost to be cheap to write after every proposal, and to be refused if anyone but the compute tries to write one.

---

## Step 6. Band signposts and the page signpost (levels 2 and 3)

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

**Band signpost (level 2).** New (not in any source): one line per band, at most 100 rows. Each row is one page: page number, title, page kind (the `type` from face 00), page state, where that page's newest page signpost sits, its length, and its fingerprint.

The page kind is copied into the row so the compute can route a request (system page, general page, a kind not yet invented) without opening the page. The `type` stays defined in face 00 [decisions.md:285] [R19]. The row is a derived copy for speed, never the source.

**Page signpost (level 3).** New (not in any source): one line per page, written by the compute after any write to that page. It lists each face the page has: face number, its state (draft, seated, counted, retired), where its current block sits, its length, and its fingerprint. For a counted face it lists each counter and its tail. It also points to the page signpost before it (`prev`), so the page's past can be walked back (Step 8).

**Why not put this inside face 00.** Prima's sketch put "where each face sits" in face 00. This plan keeps it out, for a reason Matthew already gave. In R25 he said the 00 counter list "must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint" [DIRECTOR-RULINGS.md:101]. The same is true here. If face 00 held face locations, face 00 would change every time any face changed. Face 00 would then have no stable fingerprint, and every write would look like a change to the registry.

What face 00 keeps is what the rulings give it: the stamp, the type, and the per-type registry [R19] [DIRECTOR-RULINGS.md:76]. The face00.md draft already proposes that the compute writes the `faces:` list and nobody writes it by hand [face00.md:179], because a contents list is derived, never hand-written [face00.md:177]. Working path D326 goes further: nobody writes a `faces:` list into face 00 at all; the computer works it out [DECISIONS-LOG:386]. This plan follows D326, so face 00 does not churn. Which wins on a mismatch is still `7` there (F2). In the `.seq` page view, the registry section can still show `faces :=` as a derived line, as it does today [seqpage.md:84]. So a person reading face 00 still sees "what kind of page, and which faces", which is what Matthew described. Only the byte positions live in the page signpost.

A kind not invented yet: a `type` not in the kernel's list is a finding, not an error, and the page is still read [face00.md:146]. The band signpost copies the unknown type exactly as written. It never guesses a nearer type.

**Axioms:** Fits axiom 7: an unknown kind stays unknown and is shown as written [Axioms.md:25]. Fits axiom 8: the band signpost's copy of `type` is a pointer; face 00 governs; if they disagree, the compute raises it [Axioms.md:27]. Fits axiom 2: the band signpost and page signpost have the same shape as the book signpost [Axioms.md:15].

**Better:** Better than Prima's sketch: face 00 does not churn, which keeps R25's fingerprint idea workable. Better than today: the compute can tell what kind a page is without replaying the book. Where we fall short: the page kind now appears in two places (face 00 and the band signpost row). That is a copy, and copies can drift [Axioms.md:15]. The plan answers this by making the row derived only and checked against face 00, but the risk is real.

**Three leads:** The person needs face 00 to stay the one place that says what kind of page this is. The model needs to read face 00 and the faces it is given, and never write a band signpost or page signpost. The compute needs the band signpost and page signpost to route requests fast, and to rebuild them from the entries whenever asked.

---

## Step 7. Face blocks, read only on demand (level 4)

Today a face's current text is the entry that wrote it: an ordinary `put` (or `promote`, `merge`, and so on) line [format.md:74] [format.md:86]. Face content is Markdown in `body` [format.md:81]. Cards are its `##` headings [seqAddr.md:168].

New (not in any source): the page signpost points straight at the face's current block. Under A2 that is a small file (or, under S1, a byte offset in the book file); in the export it is a byte offset. The compute reads that one piece and nothing else. A face nobody asks for is never read.

**Updated by A1 (t171u):** face 04 blocks stay Markdown text. Blocks of other faces may be compact code (Step 3), as compact plain text now, or raw bytes only after a numbered ruling. Whatever the form, the card keys inside a block stay plain ASCII [DECISIONS-LOG:560], so a card can still be found by its key.

Block size: no fixed block size. A block is as long as it needs to be. The page signpost gives where it is and how long. A fixed size (padded) would help only a raw-bytes layout; padding is bytes nobody wrote. This is a builder choice, recorded with its why [AGENTS.md:45].

Seated, draft and counted faces work as today. A draft is found by lookup and shows that it is a draft and why [R5] [DIRECTOR-RULINGS.md:20] [DIRECTOR-RULINGS.md:29]. A counted face has counters 01-98 only; faces have no sentinels [R9] [DIRECTOR-RULINGS.md:38]. A new counter is never a silent in-place replace (working path D320, D344 [DECISIONS-LOG:380] [DECISIONS-LOG:407]). The page signpost points at whichever pieces those rules say are current.

**Axioms:** Fits axiom 6: blocks are never edited; a change is a new block [Axioms.md:23]. Fits axiom 5 in spirit: the model is handed only the framed piece it needs [Axioms.md:21].

**Better:** Better than today: today the whole book is replayed to serve one face [format.md:61]. Better than one big file being rewritten: each piece is its own block. Where we fall short: one very large face is still read whole, and a code face must be decoded before a person or model can read it.

**Three leads:** The person needs face 04 to look the same as today: Markdown with `##` cards. The model needs exactly the face (or card) it asked for, as text, with its address and source [AGENTS.md:44]. The compute needs one lookup and one read per face, plus a decoder for code faces.

---

## Step 8. Face 09 is the page's log; no short log in face 00

**Director answer, t171u (relayed by Prima), not yet a numbered ruling (A3):** "agreed 09 is log, we keep a short log in 00 if you think that is a superiour design."

**Where face 09 stood.** Face 09 was unassigned: "01-09 system faces (01-08 defined, 07 reserved, 09 unassigned)" [decisions.md:182]; the review list says the same [review.md:53]; the face table says "reserved, unassigned" [seqAddr.md:158]. Retiring is done with the tail word `retired` [seqAddr.md:127] [seqAddr.md:138]. (The brief says an older ".09 retired" tail existed and is gone; no source line still uses it, so that history is not verified here.) A3 gives face 09 its job. The face table still says "unassigned" until A3 is a numbered ruling and the spec is changed by whoever is allowed to change it.

**What the face 09 log holds (plan, new).** One line per approved write to the page: entry number, time, who, operation, address, proposal, and the reason where there is one. It is written only by the compute. Nobody proposes to face 09. Writing face 09 never creates another face 09 line, so the log does not log itself (the same trap R25 avoids for face 00 [DIRECTOR-RULINGS.md:101]).

**How it fits A2 (small files).** Under S2 or S3, face 09 is the page's own log file, the one record of that page's history; the compute appends one line per write. Under S1, the book file is still the log [format.md:61], and face 09 is the page's list of pointers into it. Either way there is one source, not two. In the export, face 09 sits at level 5 of the pyramid, reached from the page signpost. In the one-page `.seq` view, face 09 takes the place of today's derived `~ history` section, which already lists "the page's line of writes across all faces" and "only grows" [seqpage.md:199].

**Other logs, kept apart.** BUILD-LOG is the repo's record of build choices [BUILD-LOG:3]; it is not a page. Face 06 holds model notes, one counter per session [seqAddr.md:155]; notes say why and what was found, while face 09 says what happened. Face 09 does not replace R25's 00 counter (00.CC), which keeps face 00's fingerprints [DIRECTOR-RULINGS.md:101]; QD66 and QD67 stay open.

**Should face 00 keep a short log too? No.** In plain words:

1. Face 00 should stay small and change rarely. R25 says face 00 is the registry root, its past is kept as a list of its fingerprints, and that list "must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint" [DIRECTOR-RULINGS.md:101]. A short log inside 00 would change face 00 on every write to any face. Each of those changes would then need its own 00 counter entry. That is the cascade R25 was written to avoid.
2. It would be a copy. The short log would repeat what face 09 already holds. Two copies can drift apart, and "agreement is not connection" [Axioms.md:27]. Axiom 2 says do not copy [Axioms.md:15].
3. It would not be faster. What a reader wants from "a short log in 00" is the latest change, fast. The compute can keep a derived **last change** pointer outside face 00 (in the page signpost, Step 6). It is one hop, the same as reading face 00. In the `.seq` view it can be shown as a worked-out line in the registry section, like `faces :=` today [seqpage.md:84]. It is never stored in face 00 and never imported.

So: face 09 holds the log. Face 00 holds no log. The compute keeps a "last change" pointer outside face 00. This agrees with Prima's lean.

**Still open (C2):** should face 09 also record attempts that were refused or halted? Today a refused proposal writes nothing ("Rejected = reasons, nothing written") [BUILD-LOG:53]. Under S2 or S3, face 09 is a stored file, so it could hold them; under S1 it could not without a new kind of book entry. Only Matthew can say whether he wants them logged.

**Disagreement halts.** If face 09, the page signpost or the "last change" pointer ever disagrees with the pieces it describes, the compute does not pick one. It halts and raises it, following working path D324, "neither silently wins; halt and raise it (axiom 1)" [DECISIONS-LOG:384], and working path D367, which halts on a fingerprint mismatch [DECISIONS-LOG:440].

**Axioms:** Fits axiom 6: the log only grows; the line back is kept with the page [Axioms.md:23]. Fits axiom 8 and axiom 2: one log, no copy in face 00; the pointer points and the source governs [Axioms.md:27] [Axioms.md:15]. Fits axiom 1: only the compute writes the log, A3 is Matthew's answer, and a disagreement is raised, not chosen [Axioms.md:13].

**Better:** Better than today's derived `~ history` section, because the page's past is reachable in a few reads without a full replay. Better than a short log in face 00, because face 00 stays small and stable (R25) and nothing is copied, with the same speed. Where we fall short: whether refused or halted attempts belong in the log is undecided, and the face table in the spec still says 09 is unassigned until A3 is numbered.

**Three leads:** The person needs one place to see what happened to this page, in time order, in plain words. The model needs to read that log before drafting, so it builds on the real past and not on memory [drafting.md:7]. The compute needs to append the log once per write, keep the "last change" pointer outside face 00, and halt if anything disagrees.

---

## Step 9. Appending a change and writing new signposts

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

New (not in any source), building on what exists: one approved proposal is written in this order, all at the end of the file.

0. Check the hash of the earlier bytes; if they changed outside the compute, refuse and raise (Tester fix 3, Step 11).
1. The proposal's entries, as today: one or more JSON lines, all or nothing [format.md:100] [BUILD-LOG:38].
2. A new page signpost line for each page the proposal touched.
3. A new band signpost line for each band the proposal touched, holding only the changed rows (a full line every K writes; Tester fix 2).
4. One new book signpost line, changed rows only (full every K writes), carrying the running chain hash (Tester fix 1).
5. One fsync, as today [BUILD-LOG:53].

Nothing earlier in the file is changed. Old blocks and old page, band and book signposts all stay. This is Prima's sketch ("changes appended at the end and a new signpost written, with old blocks kept"), with the two extra levels.

The cost of one write is the entries plus three small derived lines (one page signpost, one band signpost of at most 100 rows, one book signpost of at most 100 rows).

A reseat follows the existing rules: the R24 climb uses a new counter, built from the seat plus the changes [DIRECTOR-RULINGS.md:97]; the newer seated pack carries a write-once `supersedes:` naming the older one (working path D321, D345 [DECISIONS-LOG:381] [DECISIONS-LOG:408]). The signposts only point at the result; they decide nothing.

Two copies of a book changed apart are never merged by mixing lines (working path D427 [DECISIONS-LOG:550] [DESIGN.md:167]). The signposts help here without deciding QD57: two copies whose book signposts have the same fingerprint are the same state, and where they differ, comparing band signposts shows which bands changed (new, not in any source).

**Axioms:** Fits axiom 6: "add the new step after it" [Axioms.md:23]. Fits axiom 1: only the compute appends, one proposal at a time, through the queue [Axioms.md:13] [format.md:42]. Fits axiom 8: every new signpost points at real entries [Axioms.md:27].

**Better:** Better than today because the next reader does not replay; better than rewriting the file, which format.md set aside ("Every write rewrites the file. Does not scale") [format.md:51]. Where we fall short: the file grows by three derived lines per write. A book with many small writes gets a lot of signpost lines. Writing signposts only every so many writes would save space, but then a reader must replay the entries since the last signpost; that is a builder setting, not a ruling.

**Three leads:** The person needs each change to show up as new lines at the end, so a git diff is a clean addition [format.md:66]. The model needs its proposal to be booked whole or not at all, and to be told which. The compute needs a fixed write order it can recover from after a crash (Step 11).

---

## Step 10. Fingerprints and checks

New (not in any source): every pointer carries the fingerprint of what it points to. The book signpost carries each band signpost's fingerprint; each band signpost row carries its page signpost's fingerprint; each page signpost row carries its face's fingerprint. This makes a chain. The book signpost's own fingerprint stands for the whole book state at that moment. To check one face, the compute checks only the path down to it.

**Updated by A2 (t171u): the git-blob flag.** The first version of this plan kept its fingerprints apart from git blobs, because a line inside one big file is not a git file. With small files as the stored form, that changes:

- Under S2 or S3, each stored small file **is** a file in git, so its git blob is its natural fingerprint. That is the same kind of fingerprint the kernel builder already pins seats to [R23-R25-lineage.md:94], and the kind working path D323 names for face 00 [DECISIONS-LOG:383].
- R25's fingerprint is a different, narrower thing: face 00's fingerprint before each change, kept on a 00 counter [DIRECTOR-RULINGS.md:101]. Working path D347, filled in by Designer proposal D350 and Tester working path D358 (none of them rulings), defines it as face 00's git blob at the parent of the commit that adds the 00.CC, stored as the blob and never as a commit id [DECISIONS-LOG:410] [DECISIONS-LOG:415] [DECISIONS-LOG:427]. Small files make that rule easier to check, because face 00 would be its own file. This plan does not change D347.
- In the export, each row can carry the same git blob id of the small file it was built from. Then a person can check an exported piece against the stored file with standard git tools.
- Under S1 (one log file per book), the git blob covers the whole book file only, so the export rows still need hashes of their own lines.

Which hash (C7, updated by t171u): git's blob hash for stored small files and for export rows that copy them. Git's default hash is the older SHA-1; git also has a SHA-256 form. Which one is a lesser choice.

**When to check (Tester fix 1, folded in).** Working path D414 says a snapshot is never trusted over the log, is checked on every open, and only the compute takes one [DESIGN.md:165] [DECISIONS-LOG:524]. Signposts are the same kind of thing. Per-line fingerprints alone cannot prove that nothing was cut out between lines; a running chain hash can (SEQ-FILE-PLAN-TEST.md section c). So, new (not in any source):

- Every signpost line carries a running chain hash of every byte of the file before it.
- "Open" means compute start, once per process, not every request. Today the compute already reads every book at start and serves from memory (`crates/compute/src/store.rs:1009-1023`).
- At start the compute checks the chain in one pass over the file, and runs the R4 byte check (or, for code faces, the strict decoder check) in the same pass.
- Until that pass ends, every answer is marked `7` (not yet checked). Tester's file uses `9` for the same state; this plan follows Prima's wording, `7`.
- Any mismatch halts and is raised; neither side silently wins (working path D324 [DECISIONS-LOG:384]; D367 [DECISIONS-LOG:440]). A full replay can then rebuild the signposts, with the person's approval.

This keeps D414 ("checked on every open", "never trusted over the log") and still serves the top fast. Tester measured one hash pass at about 0.4 s per 500 MB in Python. For stored small files, the same rule applies per file: each file's fingerprint is checked at start. This touches QD46 and does not close it (C4).

**Axioms:** Fits axiom 8: a pointer whose fingerprint does not match is missing (`7.8`) and is not repaired from memory [Axioms.md:27]. Fits axiom 9: check before trusting [Axioms.md:29]. Fits axiom 1: a mismatch halts and is raised [Axioms.md:13]. Fits axiom 2: one kind of fingerprint (the git blob) where the existing design already uses it [Axioms.md:15].

**Better:** Better than today: today nothing inside a book says "this line is intact" except that it parses. Better than a new kind of fingerprint: under S2 or S3 the git blob is already used for seats. Where we fall short: a fingerprint shows damage; it cannot repair it. And git's default hash is SHA-1, which is old.

**Three leads:** The person needs to check a fingerprint with a common tool (git), not trust the compute blindly [AGENTS.md:10]. The model needs to cite a version by address plus fingerprint, never by commit id, as working path D348 already does for packs [DECISIONS-LOG:411]. The compute needs fingerprints that are cheap on write and on read.

---

## Step 11. Crash safety

What exists: a partly written last line is dropped on load and cut off before the next append [BUILD-LOG:54]; a cut-off multi-op proposal is dropped whole [BUILD-LOG:38]; the compute appends with fsync [BUILD-LOG:53]. Working path D431 (not a ruling) records the hardware as one ordinary computer with a local disk that honours fsync [DECISIONS-LOG:558].

New (not in any source): with the write order in Step 9, a crash can only leave one of these:

- A cut-off entry, or a cut-off page, band or book signpost, at the very end. The existing rule drops it [BUILD-LOG:54].
- Whole entries with no new signpost after them (the crash came before step 4). The compute finds the last good book signpost, then replays only the entries after it, and writes a fresh signpost. Nothing is lost, because the entries are complete and the signposts are derived.
- A signpost whose fingerprints do not match. It is not used; the compute walks back to the signpost before it (`prev`), and raises it.

The worst case is always: ignore every signpost and replay the whole book, exactly as today. So the new layout can never be less safe than today's.

**Updated by A1 and A2 (t171u), new:** with small files, each write puts the new piece in a new file (or new lines), fsyncs it, and only then appends the face 09 log line; a piece with no log line is ignored as unfinished. Old pieces are never overwritten. Today's safety leans on whole lines: a cut-off last line is dropped [BUILD-LOG:54]. A raw-bytes face (only after A1 is a numbered ruling) has no lines to lean on, so its log line must carry its length and fingerprint, and a piece that fails either is treated as not written. The one storage failure seen so far was a crash cutting inside an accented letter, and R4 fixed it by refusal, not by repair code [DESIGN.md:173]; working path D432 asks for a hostile crash test before any widening [DECISIONS-LOG:560]. The same is needed before raw-bytes faces.

**Tester fix 3 (outside writers), folded in; plan text only, no code changed:** today the compute, before it appends, cuts any bytes past the length it last wrote as a "partial tail" (`crates/compute/src/store.rs:941`), but it does not check that the earlier bytes are unchanged. Its write folder is `books/` (`store.rs:59`), the same folder the kernel builder rewrites whole (`kernel/build.mjs:846`). So a rebuild while the compute runs could mix two files silently, and every signpost offset would then point at the wrong bytes. The fix in this plan:

- Before each append, the compute checks a hash of the earlier bytes (the chain hash on the last signpost line, Step 10). If they changed, it refuses to write, halts and raises it (D324).
- The builder writes somewhere else, or appends through the same rules, instead of rewriting whole files in the compute's folder.

**Axioms:** Fits axiom 6: recovery only adds; it never rewrites an earlier line [Axioms.md:23]. Fits axiom 7: a damaged signpost is treated as missing, not guessed [Axioms.md:25]. Fits axiom 1: a damaged signpost is raised, not silently replaced [Axioms.md:13].

**Better:** As safe as today, and faster to recover after the common case (a crash after the entries but before the signpost). Better than an edit-in-place signpost, which can be half-written in the middle of the file. Where we fall short: it still needs a disk that honours fsync (D431). On a disk that lies about fsync, no file layout is safe, and this plan does not fix that.

**Three leads:** The person needs to know that a crash cannot eat old work, and to be told plainly when a signpost was damaged. The model needs its proposal to be either fully booked or clearly not booked after a restart. The compute needs a recovery rule that is short, tested, and always falls back to full replay.

---

## Step 12. Tidying old blocks without losing history

Over time the file fills with old signposts and old page signposts. format.md already says older entries "can be moved to an archive file if size becomes a problem" [format.md:105], and lists the archive policy as open [format.md:157]. Working path D414: no entries are archived until an archive can still be opened and is checked with the book [DESIGN.md:165].

Options (new framing, not in any source):

- Option K1 (this plan, for now): never tidy. Books are small today (about 233 KB in total). Nothing needs tidying yet.
- Option K2: a new generation. The compute writes a new book file that starts with the header, then the current state of every page, then fresh signposts. The new file's first entry points back to the old file by name and fingerprint; the old file is frozen, kept, and checked with the book. Old signposts are dropped from the new file only, never from the old one. History is one link away.
- Option K3: cut old lines out of the file. **Set aside**: it rewrites the past and breaks axiom 6 [Axioms.md:23].

Whether K2 may ever be done, and who approves it, is Matthew's choice (choice C5).

**Axioms:** K1 and K2 fit axiom 6: nothing old is rewritten; K2 adds a new step and links back [Axioms.md:23]. K2 fits axiom 8 only if the link is written both ways [Axioms.md:27]. K3 breaks axiom 6.

**Better:** K1 is the simplest and safest for now. K2 is better than K3 because the past stays whole and can be opened. Where we fall short: K2 makes a book two (or more) files, which strains "a book is one file" [format.md:21] and Matthew's "self-contained". That trade-off is his.

**Three leads:** The person needs to approve any tidy, and to be able to open the old file afterwards. The model needs to be able to cite an old version by address and fingerprint even after a tidy. The compute needs a tidy that is all or nothing, checked, and never touches the frozen file.

---

## Step 13. Links: books and pages point to pages, never to faces

**Director answer, t171u (relayed by Prima), not yet a numbered ruling (A5):** "We use the seqaddr system. our 2.2.2.4.title we don't include the face its a sub group of the page." Read: a link points to a page address plus its title, never to a face.

**Checked against seqAddr.md.** "2.2.2.4" is the four address widths: desk, shelf and book are 2 digits, the page is 4 [seqAddr.md:14] [seqAddr.md:18] [seqAddr.md:19] [seqAddr.md:20] [seqAddr.md:21]. A word after the page is a title, and "Faces never have titles: a face is `PPPP.FF` or `PPPP.FF.NN`" [seqAddr.md:110]. The grammar allows a title right after the page [seqAddr.md:269]. Link targets are already page-level: "Every target's identity page links back" [seqAddr.md:251]. So A5 fits seqAddr.md. A link reads like `10.11.21.1001.bob`.

Three points from seqAddr.md that a link must respect:

- A title is a label, not identity: `4442` and `4442.timer` are the same page [seqAddr.md:114]. The address is what the link follows; the title is a check.
- A title written in an address is checked against the stamp in face 00, and a mismatch is raised to the person [seqAddr.md:116].
- Not every page has a title. Pages 1000 and up must; pages 0001-0999 may; page 0000 has none [seqAddr.md:115]. So a link to an untitled page is the page address alone. A link to a whole book uses the book's address or its identity page, for example `21.0000` [seqAddr.md:89].

**What A5 changes.** Face numbers stay legal in addresses: the grammar still has a face part [seqAddr.md:271], and a card can be named on a face, like `10.10.11.1014.01.ham` [seqAddr.md:111]. A5 says links do not use them. Once a link reaches the page, the face is opened inside the page. Whether A5 also covers cites and work-card references that name a face or counter today (for example a seated pack `05.02`, cited by address plus blob under working path D348 [DECISIONS-LOG:411]) is not clear. That is a new question for Matthew (C10).

**Across books and files.** A book points to another book by address, never by byte offset or file position. Offsets belong to one file and change if it is tidied or exported again (Step 12). Addresses are "ranked so it is stable to store" [Axioms.md:23]. Finding still looks up book, then shelf, then desk, then kernel; the first match wins [seqAddr.md:101] [seqAddr.md:104]. Books follow the kernel live; they do not copy it [decisions.md:128]. Links live on face 08 and need a back-link [seqAddr.md:157] [seqAddr.md:251].

**Pinning a version.** The first version of this plan let a link pin a face's fingerprint. Under A5 a link does not name a face, so that is dropped. A link follows the live page. If an exact past version is ever needed, it is a cite, not a link (C10).

"Self-contained" means: a book holds all of its own pages and their history. It does not hold copies of what it inherits; copying the parent is what axiom 2 forbids [Axioms.md:15]. A borrowed face is shown from its source, at most as a derived line (working path D403 [DESIGN.md:189]).

**Axioms:** Fits axiom 8: a connection is lawful only when written, and a link names its target page and is linked back [Axioms.md:27]. Fits axiom 6: the address is the line written down; travel by written connections, not by what matches [Axioms.md:23]. Fits axiom 2: inherit, do not copy [Axioms.md:15].

**Better:** Better than links to faces: a page can reorganise its faces without breaking links to it, and there is one kind of link target. Better than links by offset, which break on tidy or export. Where we fall short: a link can no longer say which face it means, so the reader must know or be told inside the page; and whether face-level cites survive is open (C10).

**Three leads:** The person needs links they can read: a page address and a title they recognise. The model needs full addresses, stated back in full when the user wrote short form [seqAddr.md:95], and must never write a face into a link. The compute needs to check the title against face 00, raise a mismatch, follow the address, and refuse a one-way link [seqAddr.md:251].

---

## Step 14. Language choice

What exists: format.md marks Rust as decided for the core library and the compute, and TypeScript with Next.js for the app [format.md:139] [format.md:140] [format.md:141]. The core and the compute are already Rust crates in the repo (`crates/seqaddr-core`, `crates/compute`, `crates/seqpage`). Prima recommended Rust for the real book file.

This plan agrees: write the book file reader and writer in Rust, inside the core, so there is one implementation. format.md gives the why: "One parser everywhere", "The rules become types", "It suits a file format" [format.md:145] [format.md:146] [format.md:147].

Trade-offs, said plainly:

- Rust is slower to change than TypeScript or Python, and fewer people can read it.
- The app would need the core built for the browser (WebAssembly). That is not built yet [BUILD-LOG:66]. Until it is, the app reads through the compute [BUILD-LOG:6], which is fine.
- A quick prototype in another language would be a second implementation, and two parsers can disagree. format.md set aside "TypeScript for everything" for this reason [format.md:149].
- Matthew does not read code. So the person's check is not the Rust. It is this plan in plain words, the file itself in plain text, and a small read-only dump tool (new) that prints the pyramid for a book.

**Updated by A1 (t171u), the parser:** the core would need two readers behind one interface: a Markdown reader for face 04, and a strict decoder for each code face kind. Both stay in the one Rust core, so the app, the compute and the dump tool can never disagree [format.md:145]. The grammar for addresses, titles and card keys does not change [seqAddr.md:280] [seqAddr.md:281]. The dump tool must also print code faces as readable text, because that is how a person checks them.

**Axioms:** Fits axiom 2: do not reinvent what already exists; the core is Rust [Axioms.md:15]. Fits axiom 4: the why is recorded [Axioms.md:19]. Fits axiom 3: compute work in the compute's own form [Axioms.md:17].

**Better:** Better than a second language for the same file. Where we fall short: the WebAssembly build is missing, and Rust raises the cost of quick experiments.

**Three leads:** The person needs a plain-words spec and a dump tool, not code. The model needs one API from the compute, over HTTP, as today (working path D426 [DECISIONS-LOG:548]). The compute needs one fast, typed implementation it can trust not to corrupt a book [format.md:140].

---

## Step 15. From today's books to small files and exports

What exists: books are version 1 JSON-line logs [format.md:60] [BUILD-LOG:54]. The kernel keeps one Markdown file per face as its source (for example `kernel/00.00.00/00.00.00.0051.01.draft.md`), and the builder rewrites each `books/*.book` whole on every build, renumbering from 1 [R23-R25-lineage.md:94] (the whole-file write is now at `kernel/build.mjs:846`; the lineage note cites `build.mjs:818`, which has since moved). So today the kernel book is not truly append-only.

**Updated by A2 (t171u):** the move depends on what "small files" means (C1).

- Under S1 (one log file per book): nothing about the stored form moves. The only new things are the signpost and the export. The export is a new version 2 file: a new header, then every version 1 entry copied **byte for byte**, with the same entry numbers, then the signposts. The stored book file is not touched.
- Under S2 or S3 (one file per page, or per face): each book is split into small files, one entry history per piece, copied byte for byte. The old book file is kept, frozen, as history, and the new files name it by fingerprint. This changes R3 and waits for a numbered ruling.

Before any move, two things must be true: the round trip book to `.seq` to book still gives back the same entries [DIRECTOR-RULINGS.md:12] [seqpage.md:208]; and the kernel builder stops rewriting whole files in the compute's folder: it writes somewhere else, or appends (Tester fix 3, Step 11), or the kernel's history keeps being lost [R23-R25-lineage.md:94] (the whole-file write is now at `kernel/build.mjs:846`; the lineage note cites `build.mjs:818`, which has since moved). Neither is done. This plan does not do them; they are build work after Matthew approves.

**Axioms:** Fits axiom 6: entries are copied unchanged; the old file is kept [Axioms.md:23]. Fits axiom 9: before replacing the old form, open it and test the new one against it [Axioms.md:29]. Fits axiom 1: S2 and S3 wait for Matthew [Axioms.md:13].

**Better:** Under S1 the move is almost free. Under S2 or S3 the move is bigger, but it follows how the kernel sources are already kept. Where we fall short: the kernel builder's whole-file rewrite is a real gap today, and no layout fixes it by itself.

**Three leads:** The person needs to approve the move and compare old and new files line by line. The model needs no change: it still proposes by address. The compute needs to read the old and new forms during the move, and refuse a version it does not know.

---

## Step 16. How this plan should be trialled

This plan is `9`: it has not faced a hostile trial [Axioms.md:29]. Before anything is built, a different view (Tester) should try to break it. New (not in any source), suggested tests:

1. Crash at every byte of a write (entries, page signpost, band signpost, book signpost). The book must reopen to the last good state every time.
2. Delete or damage every signpost. A full replay must rebuild the same signposts, byte for byte.
3. Forge a signpost that points at the wrong entry with a matching-looking row. The fingerprint check must halt it.
4. Round trip: book to `.seq` page views to book must stay lossless with signpost lines present.
5. A page with a type nobody has defined: it must be stored, routed and shown as written, with a finding.
6. Face 09 must list exactly the page's approved writes, in book order, and match today's `~ history` section.
7. A book of 10,000 pages: opening and reading one face must touch only the five levels.
8. Two copies changed apart: the book signpost fingerprints must show they differ, and nothing may merge them by mixing lines.

Added after t171u (new):

9. Face 04 history (Step 17): rebuild every old version from its full copy plus changes, and compare fingerprints.
10. A code face cut off at every byte: it must be ignored as unfinished, never read as a shorter face.
11. A link with a title that does not match face 00: it must be raised, not followed silently.
12. Face 00 must not change when only other faces change (no log in face 00).

Added from Tester's stress test (SEQ-FILE-PLAN-TEST.md, Step 16):

13. A rebuild of a book file while the compute runs must be refused at the next append (prefix hash).
14. A line cut out of the middle of a file must be caught by the chain hash at start.
15. A fork with the same address must be told apart, or raised.
16. A hand edit to face 04 outside the compute must be found and taken in as a new step, never halted forever.

**Axioms:** Fits axiom 9: a hostile pass from another view before promotion [Axioms.md:29]. Fits axiom 1: Matthew approves. R2's build-stage approval lets a face be seated after a trial [DIRECTOR-RULINGS.md:9]; it does not speak of changing the file format, so this plan reads that change as Matthew's to approve [Axioms.md:13].

**Better:** Better than building first and testing after. Where we fall short: these tests are a list, not code; none of them exist yet.

**Three leads:** The person needs the trial results in plain words before deciding. The model (as Tester, a fresh session per R20) needs the plan and the sources, read-only. The compute needs the tests to run on real book files, not only on samples.

---

## Step 17. Face 04 edits: small changes plus a full copy every so often

**Director answer, t172u (relayed by Prima), 16 Nov 2026, 11:17 AM EST; not yet a numbered ruling.** Matthew said: "go with Google's approach." This is built in here as his answer, not as a choice.

What it means for the book file:

- Face 04 edits are stored as a log of small changes (each change says what was changed in the face, not the whole face again).
- Every so often the compute also stores a full copy of face 04 (a *snapshot* of that face).
- The current view of face 04 is the latest version: the last full copy plus the small changes after it.
- Every old version is kept. Any old version can be rebuilt from the full copy before it plus the small changes up to it.

**The reason, not a choice.** The comparison behind this answer is Google Docs against Word. In the Google Docs way, a document keeps a history of small edits and you can open any earlier version. In the Word way, each save is a whole new file, and what came before is only kept if someone keeps the old file. Matthew chose the Google way. The comparison is kept here only as the reason; it is no longer an open choice.

**How it fits what already exists.**

- Face 04 is the person's face: "the why of the page, long form, for inspection" [seqAddr.md:153].
- The book already only grows, and already has full-state snapshots that let replay start late [format.md:61] [format.md:88] [format.md:105]. Step 17 applies the same idea at the size of one face.
- Drafting already works in small steps: copy the face to a draft, add notes, merge one change at a time, then promote [format.md:94] [format.md:95] [format.md:96] [format.md:97] [drafting.md:12] [drafting.md:14]. A merge "applies one change to a draft" [format.md:96]. Small stored changes fit that shape.
- In the pyramid (Step 2), the page signpost points at face 04's latest full copy and the small changes after it. Reading the current view is one full copy plus a short run of changes. Reading an old version walks back through the page's history (Step 8).
- Each full copy and each small change carries a fingerprint (Step 10). A rebuilt version can be checked against the full copy that follows it.
- Everything stays printable ASCII under R4 [DIRECTOR-RULINGS.md:16]. A small change is written as plain text lines.

New (not in any source), for the builders: how often a full copy is stored (for example every so many changes, or when the run of changes grows past a size) is a builder setting, recorded with its why [AGENTS.md:45]. The face 04 full copy is not the same thing as a book `snapshot` entry; working path D414 on book snapshots [DESIGN.md:165] is not changed or closed by this step. Whether the same "small changes plus full copy" way should later apply to other faces is not decided here; Matthew's answer was about face 04.

**"So they can't be changed" (provisional reading).** Matthew also said "So they can't be changed". What he meant is still unclear, and Prima has asked him. **Provisional reading, until he says otherwise: old versions can't be changed.** A stored small change or full copy is never edited; a correction is a new change after it. This reading fits axiom 6, "The past is not rewritten" [Axioms.md:23]. It is listed as an open question (C9). If he meant something else (for example that the current face 04 may not be changed by a model, or may not be changed without his approval), this step must be revisited.

**Axioms:** Fits axiom 6: every old version is kept, and a change is a new step after the old one [Axioms.md:23]. Fits axiom 1: this is Matthew's answer, recorded as his, not invented by the builders [Axioms.md:13]. Fits axiom 4: the why (the Google Docs against Word comparison) is recorded with the choice [Axioms.md:19]. Fits axiom 7: the unclear phrase stays open, with a reading marked provisional, not a guess presented as fact [Axioms.md:25].

**Better:** Better than storing a whole new face 04 on every edit: much smaller, and the difference between two versions is visible directly. Better than keeping only the latest version, which would lose the past. Where we fall short: rebuilding an old version means applying a run of changes, so a bad change or a bug in applying changes could give a wrong old version; the fingerprint on each full copy is the check against that. How a small change is written down (by line, by card, or by character) is not designed yet, and it must survive the R3 round trip to the `.seq` page view without loss [DIRECTOR-RULINGS.md:12].

**Three leads:** The person needs to read the current face 04 as one clean text, and to open any earlier version and see what changed and when. The model needs to propose small changes against the latest version, never a rewrite from memory [drafting.md:7]. The compute needs to store each change and the full copies, rebuild any version on request, check fingerprints, and refuse any attempt to edit a stored version.

---

## Open choices only Matthew can decide

Each is a plain question, with the options and what each would mean. The top three are marked **TOP**. None of these is answered here. "Updated by t171u" marks a choice his t171u answers changed.

**C1 (TOP). Updated by t171u (A2). What exactly are the "small files", and does R3 change?**
You said small files stay the stored form and whole books are exported. R3 says the book is the real copy [DIRECTOR-RULINGS.md:12]. R3 stays as written until you rule.
- Option S1: one small log file per book, as today. R3 is unchanged. The export is a new one-file shape of the book.
- Option S2: one file per page. Today's one-page `.seq` view becomes the stored form. Changes R3.
- Option S3 (plan's lean): one file per face, the way kernel sources are kept today. Fits your answers on faces as code, face 09 and face 04 best. Changes R3.
- Also part of C1: names. The exported whole book is a `.seq` file; what is the one-page view called, and what are the small files called?

**C2 (TOP). Updated by t171u (A3). Should face 09 also record attempts that were refused or halted?**
Settled by your answer: face 09 is the page log, and face 00 keeps no short log (Step 8).
- Option A: approved writes only. Simple; matches the book log today.
- Option B: also refused and halted attempts, with their reasons. Fuller history; possible only if face 09 is a stored file (S2 or S3), or with a new kind of entry under S1.

**C3 (TOP). Updated by t171u (A1). Will you make "every face other than 04 can be code" a numbered ruling, and what does "code" mean?**
Until you number it, R4 stands for every face [DIRECTOR-RULINGS.md:16].
- Option T1: everything plain text (R4 as written).
- Option T1c (plan's pick for now): face 04 plain text; other faces compact plain text. Allowed today, no ruling needed.
- Option T2: face 04 plain text; other faces raw bytes. Needs a numbered ruling narrowing R4 to face 04.
- Option T3: SQLite. Set aside: it makes face 04 binary too.
- In every option, addresses, titles, card keys, tails, identities and tokens stay plain ASCII.

**C4. How much should the compute trust the signposts when it opens a book?**
Related to QD46 (working path D414). Under A2 the signpost can be rebuilt from the small files on start, which makes this smaller.
- Plan's pick now (Tester fix 1): a running chain hash on every signpost line, checked once at compute start in one pass; answers marked `7` until the pass ends; any mismatch halts (D324). This keeps D414.
- Option A: full replay on every open (slow for big books).
- Option B: check each piece only as it is read (fast, but damage in unread parts is found late, and R4's damaged-on-read rule is not met).

**C5. May old lines ever be tidied away?**
- Option K1 (plan's pick for now): never.
- Option K2: a new file generation, with the old file frozen and linked. Then say who approves it.
- Option K3 (set aside, breaks axiom 6): cut old lines out.

**C6. Updated by t171u (A2). Is a band level wanted in the export and the signposts?**
Now about the export file and the signposts only, not the stored form. This plan suggests it becomes a builder choice, recorded with its why, unless you want to decide it.
- Option A (plan's pick): book signpost, then band signposts of up to 100 pages each [seqAddr.md:240].
- Option B: one flat signpost with a row per page.

**C7. Updated by t171u (A2). Which fingerprint?** (lesser)
Now: the git blob of each stored small file (under S2 or S3), the same kind the kernel builder already uses for seats.
- Option A: git's default blob hash (SHA-1, older).
- Option B: git's SHA-256 form.

**C8. Updated by t171u (A2, A5). Should an exported book carry what it inherits?**
A book holds its own pages; inherited faces come from the shelf, desk and kernel [decisions.md:128]. Links name pages only (A5).
- Option A (as designed): the export holds the book's own pages only.
- Option B: an export option that also bundles the inherited pages, as a view, so one file shows everything a reader sees.

**C9. What did "So they can't be changed" mean?** (still open; Prima has asked Matthew)
- Provisional reading used in Step 17, until he says otherwise: old versions of face 04 can't be changed.
- If he meant something else, Step 17 is revisited.

**C10. New. Do links-name-pages-only (A5) also cover cites and work-card references?**
- Option A: only links (face 08 and cross-book links). Cites may still name a face or counter, for example a seated pack `05.02` with its blob.
- Option B: every reference names a page only; faces are found inside the page.

Settled, not a choice: how face 04 edits are stored. Matthew answered "go with Google's approach" (Director answer, t172u, relayed by Prima; not yet a numbered ruling). See Step 17.

---

## Still open

- C1, C2 and C3 (the top three), and C4-C10 above.
- Whether A1-A5 become numbered rulings. Until then, R3 and R4 stay as written, and the spec's face table still says face 09 is unassigned [seqAddr.md:158].
- What "So they can't be changed" meant (C9).
- How a write that spans several pages is made all or nothing under S2 or S3. Page 0000 may hold only face 00 [DIRECTOR-RULINGS.md:41], so a book-wide log cannot sit on the door page. This is build detail, raised here so it is not lost.
- The kernel builder's whole-file rewrite [R23-R25-lineage.md:94] (the whole-file write is now at `kernel/build.mjs:846`; the lineage note cites `build.mjs:818`, which has since moved).
- Two copies of one book with the same address (a fork, D427) cannot be told apart by a link; a book fingerprint or a new address is needed (SEQ-FILE-PLAN-TEST.md section e).
- How a hand edit to a face 04 file made outside the compute is found and taken in as a new step (SEQ-FILE-PLAN-TEST.md, new holes). Only the compute writes [format.md:18].
- QD65 stays with Matthew.

---

## Related open questions (named, not closed)

- QD34: is the `.seq` file layout OK [QUESTIONS-FOR-DIRECTOR.md:298]. This plan does not answer it.
- QD46: snapshot trust (C4 above) [QUESTIONS-FOR-DIRECTOR.md:360].
- QD16: what happens after counter 98 (would matter if face 09 were ever a counted face) [QUESTIONS-FOR-DIRECTOR.md:180].
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
- `docs/spec/format.md` (book format): lines 12, 15, 18, 21, 25, 28, 42, 51, 54, 60, 61, 66, 70, 74, 79, 81, 86, 88, 94-97, 100, 102, 105, 139-149, 157.
- `docs/spec/seqAddr.md` (addresses): lines 7, 95, 101, 104, 127, 138, 150, 152, 153, 155, 157, 158, 168, 240, 251.
- `docs/spec/seqpage.md` (the page view): lines 11, 13, 84, 199, 206, 208.
- `docs/spec/face00.md` (face 00 draft): lines 146, 177, 179.
- `docs/spec/decisions.md`: lines 128, 182, 285.
- `docs/spec/review.md`: line 53.
- `docs/spec/drafting.md`: lines 7, 12, 14.
- `docs/design/DESIGN.md`: lines 17, 165, 167, 189.
- `docs/design/DECISIONS-LOG.md` (working paths, not rulings): D320 (:380), D321 (:381), D324 (:384), D344 (:407), D345 (:408), D347 (:410), D348 (:411), D350 (:415), D358 (:427), D367 (:440), D426 (:548), D427 (:550), D431 (:558).
- `docs/design/R23-R25-lineage.md`: line 94.
- `docs/design/QUESTIONS-FOR-DIRECTOR.md`: QD16, QD34, QD46, QD57, QD60, QD63, QD66, QD67.
- `docs/BUILD-LOG.md`: lines 3, 6, 38, 53, 54, 66.
- Matthew's words, 16 Nov 2026 (passed on by Prima): ideas, not rulings.
- Director answers t171u (11:16 AM EST, A1, A2, A3, A5), relayed by Prima, 16 Nov 2026. Not yet numbered rulings.
- Director answer, t172u (relayed by Prima), 16 Nov 2026, 11:17 AM EST: "go with Google's approach" for face 04 edits. Not yet a numbered ruling. The phrase "So they can't be changed" is still open (C9).

---
