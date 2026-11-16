# Stress test of the .seq file plan

WORKING PATH by Tester, not a ruling.
Tests docs/design/SEQ-FILE-PLAN.md at 29ec433 (Designer's plan).
Folds in Director answers t171u, relayed by Prima (11:16 AM EST).
Those answers have no R-number yet. Nothing here closes a QD.

## Verdict

- The core idea holds: add-only file, signposts found from the end,
  rebuild by full replay when in doubt.
- Measured: the pyramid lookup is fast in plain text (under 0.1 ms).
- Three gaps must be fixed first: the open check (D414), map growth,
  and outside writers that rewrite whole files.
- Matthew's t171u answers change Steps 1, 3, 8, 13, 15 and C1-C3, C8.
  Answer 2 turns the plan around: small files are stored, the book
  is an export. That reverses R3, so R3 needs his restatement.

## Top 3 fixes

1. Open check: each map line carries a running hash of every byte
   before it (D414's own offer). Boot checks it in one pass.
2. Map growth: write only changed rows, plus a full map every K
   writes. Up to about 20 KB of map per write today, as designed.
3. Outside writers: the builder rewrites whole books (build.mjs:846)
   into books/, the compute's own write folder (store.rs:59). Fix
   before any byte offset is trusted.

## a. Plain text vs binary, and real speed

Measured on the box, warm cache, Python, synthetic books:

| book   | full parse | hash all | last map line | one seek |
|--------|------------|----------|---------------|----------|
| 10 MB  | 0.025 s    | 0.008 s  | 0.028 ms      | 0.007 ms |
| 100 MB | 0.236 s    | 0.076 s  | 0.027 ms      | 0.008 ms |
| 500 MB | 0.758 s    | 0.397 s  | 0.029 ms      | 0.010 ms |

Real core (seqaddr replay, release build, 18,001 entries):
- 20 MB: 0.19 s. 183 MB: 1.30 s. (Debug build, 20 MB: 2.7 s.)

What this shows:
- Finding a spot by offset in text is as fast as binary. The cost is
  the disk, not the text.
- Offsets in text are safe: JSON escapes newlines in bodies, so a raw
  newline always ends a line.
- Line length is no problem: longest kernel line is 18,662 bytes.
- Binary would only speed up the full read and full check.
- So R4 (plain characters) costs little speed. Step 3 holds.
- Today the compute reads all books at boot and serves from memory
  (store.rs:1009-1023). So the pyramid speeds up boot and memory,
  not each request. The plan does not say this.
- Not measured: cold disk reads (cache cannot be dropped here).
- t171u answer 1: faces other than 04 may be compact code. Compact
  ASCII keeps R4. Real binary bytes break R4 as ruled
  (DIRECTOR-RULINGS.md:16). That needs Matthew to restate R4.

## b. Does "last map line" stay fast as a book grows?

- Reading from the end is bounded: one short read (0.03 ms) at any
  size, as long as a map is written after each proposal.
- If maps are written only every K writes, the walk back is up to
  K entries. Bounded, but say K.
- Each write is NOT O(n): maps are capped at 100 rows a level.
- But each write is big when the book is full: book map about
  9.5 KB, band map about 10 KB, plus a page index.
- Entries today average 1.6 to 4 KB. So maps can be 5 to 10 times
  the size of the change.
- 10,000 writes on a full book add about 200 MB of maps.
- Fix: a map line holds only rows that changed, plus `prev`. Write a
  full map every K writes. Reader walks back at most K map lines.
- Small books (1-3 bands) cost under 1 KB per write. Fine.

## c. D414: snapshot checked on every open

- D414 (DECISIONS-LOG:524): a snapshot is never trusted over the
  log, is checked on every open, and only the compute takes one.
- Maps are the same kind of thing as snapshots (Step 5 says so).
- A full replay on every open erases the speed gain. The code does
  this today: replay checks every snapshot (state.rs:245); the fast
  path has no callers (state.rs:251).
- Also R4 says a book holding a bad byte is damaged on read
  (DIRECTOR-RULINGS.md:16). A lazy reader never sees unread bytes.
- Design that keeps both:
  - each map line carries a chain hash of all bytes before it;
  - "open" means compute boot, once per process, not each request;
  - boot checks the chain in one hash pass (0.4 s per 500 MB in
    Python) and the R4 byte scan in the same pass;
  - until the pass ends, answers are marked `9` (not yet checked);
  - any mismatch halts and is raised (D367); full replay rebuilds.
- This keeps "checked on every open" and "never trusted over the
  log", and still serves the top fast.

## d. The builder rewrites whole files

- R23-R25-lineage.md:94 (verified): the builder rewrites each
  books/*.book whole, numbers from 1, fixed time and author.
- That line cites build.mjs:818. At 29ec433 it is build.mjs:846.
- The compute writes to books/ by default (store.rs:59).
- store.rs:941 cuts any bytes past its known length as a "partial
  tail". It does not check that earlier bytes are unchanged.
- So a rebuild while the compute runs can mix two files silently.
  With maps, every offset would then point at the wrong bytes.
- The core's own append reads the whole file twice
  (log.rs:420, :449, :451). The compute's append does not.
- So the plan's "add-only" claim holds for the compute only, not
  for the kernel book (axiom 6, Axioms.md:23). Step 15 says so.
- Fix: the compute checks a prefix hash before each append; the
  builder writes elsewhere or appends.
- t171u answer 2 changes this: if small files are stored and books
  are export, the builder's whole rewrite becomes a normal export.
  Lineage then lives in the small files and git (D347 blobs).

## e. Cross-book links when a book moves

- Plan (Step 13): link by address only, never by byte offset. Good.
- t171u answer 5: links use page address plus title, never a face.
  So a link cannot target `PPPP.FF`. Step 13 allows face cites via
  D348 address plus blob; that must narrow to page level.
- Moved file, same address: links still work. Address is the key.
- Renamed file: the header address must match the file name
  (BUILD-LOG:54). A rename is refused at boot. Good: no silent drift.
- New address (re-shelved): every link breaks. The title check
  catches a wrong page at the old address. Back-links must be
  rewritten as new steps, both ways (seqAddr.md:251).
- Copy that changed apart is its own book (D427). Same address, two
  files: links cannot tell them apart. Needs a book fingerprint or
  the fork's new address in the link. Hole.
- Door return links sit on the door's face 00 (D368). Fine with
  answer 5: they point at a page.
- D391: a seated pointer needs a seated return link. Unchanged.
- How face 08 links are stored is QD50 (OPEN O36), Matthew's only.
  This test does not answer it.

## Steps 1-16 (each against the three checks)

Step 1. Names: book, page, face
- Axioms: 2 :15 fits; 1 :13 (R3 is Matthew's) fits.
- Better: yes. Falls short: "map" also names face 08 (seqAddr:157).
- Leads: person, model, compute all covered.
- t171u answer 2 settles the name clash only in part: books are the
  export, small files are stored. R3 must be restated.
- Result: holds with fix (rename the plan's "map").

Step 2. The pyramid
- Axioms: 2 :15, 8 :27 fit.
- Better: measured, yes at large size; no gain at 233 KB today.
- Falls short: the compute serves from memory, so the gain is boot.
- Leads: all three. Compute needs depth stated with deltas (b).
- Result: holds with fix.

Step 3. Plain text, not binary
- Axioms: 1 :13, 4 :19 fit.
- Better: yes; measured lookup is disk-bound, not text-bound.
- t171u answer 1 narrows it: only 04 must be human-readable.
  Compact ASCII for other faces keeps R4; binary needs R4 restated.
- Leads: model loses if 01 (agent face) turns to code. Keep 01 text.
- Result: holds; changed by answer 1.

Step 4. The header, written once
- Axioms: 6 :23, 7 :25 fit. Core refuses unknown version (log.rs:283).
- Better: yes. Falls short: every old tool stops reading v2.
- Leads: all three.
- Result: holds.

Step 5. Book map found from the end
- Axioms: 6 :23, 8 :27 fit; 1 :13 if compute-only.
- Better: yes. Falls short: map size per write (b); map lines need
  an entry number (log.rs:293) or a new line type; example has no
  addr, unlike seqpage.md:206 book-level entries.
- Leads: person can read the last line. Compute needs rule (c).
- Result: holds with fix (deltas, chain hash).

Step 6. Band maps and page index
- Axioms: 7 :25, 8 :27, 2 :15 fit.
- Better: keeps face 00 still. Falls short: face00.md:179 lets the
  compute write `faces:` into 00, which churns 00. D326 says nobody
  writes it. Plan should cite D326.
- Leads: all three.
- Result: holds with fix.

Step 7. Face blocks read on demand
- Axioms: 6 :23, 5 :21 fit.
- Better: yes (one seek, 0.01 ms). Falls short: under answer 4 a
  hand edit to 04 must never be in place inside a book (offsets).
- Leads: all three.
- Result: holds.

Step 8. Face 09 as the page log
- Axioms: 6 :23, 8 :27, 1 :13 fit under L1.
- t171u answer 3: face 09 is the page log. Now Director-answered.
- Still open: L1 (pointers) or L2 (stored lines, can hold refusals).
- Core refuses writes to 09 today (validate.rs:232-233; face.rs:72).
  seqAddr.md:158 says unassigned. Spec change needed (builders).
- Under answer 2 (small files) L1's pointer chain into one book
  file does not exist. 09 becomes its own compute-only file, one
  log, not counted (avoids R9's 98 cap and QD16).
- Leads: compute must never log its own log write (R25 trap).
- Result: holds with fix; changed by answers 2 and 3.

Step 9. Append order
- Axioms: 6 :23, 1 :13, 8 :27 fit.
- Better: no rewrite. Falls short: 20 KB per write when full.
- Leads: all three.
- Result: holds with fix (b).

Step 10. Fingerprints and checks
- Axioms: 8 :27, 9 :29, 1 :13 fit.
- Falls short: per-line hashes do not prove nothing was cut out
  between lines. A chain hash does. C4 needs the design in (c).
- Answer 4: a hand edit to 04 shows as a hash mismatch. It must be
  taken in, not halted forever (see holes).
- Result: holds with fix.

Step 11. Crash safety
- Axioms: 6 :23, 7 :25, 1 :13 fit.
- Better: same as today plus faster recovery.
- Falls short: store.rs:941 cuts extra bytes without a prefix check.
- Leads: all three.
- Result: holds with fix (prefix hash before append).

Step 12. Tidying (K1-K3)
- Axioms: K1, K2 fit 6 :23; K3 breaks it.
- Better: K1 is right now. K2 strains "one file" but fits answer 2.
- Leads: all three.
- Result: holds.

Step 13. Books pointing to books
- Axioms: 8 :27, 2 :15, 6 :23 fit.
- t171u answer 5: page address plus title, never a face. Changes
  the pinned-face part of this step.
- Falls short: forks with one address (e).
- Result: holds with fix; changed by answer 5.

Step 14. Rust
- Axioms: 2 :15, 4 :19, 3 :17 fit.
- Better: yes; measured release replay 7 to 14 times faster than
  debug. Falls short: no wasm build (BUILD-LOG:66).
- Leads: person gets a dump tool, not code. Good.
- Result: holds.

Step 15. Moving today's books
- Axioms: 6 :23, 9 :29 fit.
- Falls short: builder rewrite (d) is the blocker; plan says so.
- t171u answer 2 changes this: the stored form is small files, the
  book is an export. M1 becomes "export v2 from small files".
- Result: changed by answer 2; plan must be revised.

Step 16. How to trial
- Axioms: 9 :29, 1 :13 fit.
- Add tests: a hand edit to 04 is taken in; a rebuild while the
  compute runs is refused; a cut line in the middle is caught by
  the chain hash; a fork with the same address is told apart.
- Result: holds with fix.

## C1-C8 picks (working path, not a ruling)

C1. Which file is ".seq"? Director-answered in part (t171u, 2):
  small files are stored, the whole book is an export. Pick: the
  page file (.seq) is the stored unit; the book file is an export.
  Needs Matthew to restate R3. Considered: A (book is .seq), B.
C2. Face 09 as log? Director-answered (t171u, 3): yes. Pick: one
  compute-only, add-only log per page, not counted. Record refused
  attempts too only if Matthew says so. Considered: L1, L2, L3.
C3. Text or binary? Narrowed (t171u, 1). Pick: 04 plain text;
  other faces compact ASCII (keeps R4). Real binary only after R4
  is restated. Measured: binary gains little for lookup.
C4. Map trust on open. Pick: chain hash checked once at boot, `9`
  until done, halt on mismatch. Keeps D414. Considered: A, B.
C5. Tidying. Pick: K1 now; K2 later with Matthew's approval. K3 no.
C6. Band level. Pick: A (bands), with delta rows and a full map
  every K writes. Considered: flat map (rewrites 10,000 rows).
C7. Fingerprint. Pick: A, SHA-256 hex. Git's default is SHA-1.
C8. Book readable alone? Narrowed (t171u, 2): the book is an
  export. Pick: B, the export may bundle inherited faces as a
  marked view. Stored small files stay A (no copies).

## What Designer's revision may already fix

- f6296ba (Step 17, t172u, seen, not tested): face 04 edits kept as
  small changes plus a full copy now and then. Meets answer 4 in
  part: lineage of 04 is kept (axiom 6).
- It does not yet say how a free hand edit outside the compute is
  found and taken in.
- Answer 2 may fix (d): if books are exports, a whole rewrite is OK.
- Answer 5 may fix (e) for faces: no face-level links to break.
- Answer 3 fixes C2's main question.
- Still not fixed by any answer: (c) open check, (b) map size,
  store.rs:941 prefix check, forks with one address.

## New holes the t171u answers open

- R3 clash: answer 2 says small files are stored; R3 says the book
  is the real copy. Matthew must restate R3.
- R4 clash: binary non-04 faces break R4 as ruled. Compact ASCII
  does not. If he means binary, he must restate R4 (D432 says R4
  stands unless he narrows it).
- Free 04 edits: a hand edit is a write outside the compute
  (format.md:18). Path: the compute sees the hash change, keeps the
  last logged 04 as live, shows the edit as a draft (R5), and books
  it as a new step with who and when. Who made it must be known
  (axiom 1); if not, ask.
- D414 vs free edits: the log stays the source. The edited file is
  a proposal until taken in. A snapshot of 04 never outranks it.
- Offsets: a hand edit inside one book file shifts every later
  offset. Small files avoid this; in a book export, edits are
  never in place.
- Face 09 needs the face table (seqAddr.md:158) and the core's
  active-face list (face.rs:72) changed.
- Title in links: a page retitle breaks every link to it. Needs a
  rule: retitle is a new step and back-links are updated.

## Cite check

- Checked 117 file:line cites and 13 D-number rows. 6 notes:
1. L57 [format.md:61]: "append-only log" is the heading at :60.
2. L397, L404 [R23-R25-lineage.md:94]: right line, but it cites
   build.mjs:818; the write is at build.mjs:846.
3. L283 [format.md:42]: says claims are solved by the queue; "only
   the compute writes" is format.md:18.
4. L171 [seqpage.md:206]: book-level entries are "addressed to the
   book"; the map example at L176 has no addr.
5. L199 [face00.md:179]: correct, but D326 (DECISIONS-LOG:386) says
   nobody writes faces: into face 00. Not cited.
6. L358 [seqAddr.md:157]: correct; face 08's name there is "map",
   which clashes with the plan's "map".
- All D rows (D320-D431) and all Axioms.md and R-line cites match.

## What I did not do

- Did not edit the plan, DESIGN.md, the kernel, the core, or specs.
- No push, merge, or seat. Nothing here is a ruling.
