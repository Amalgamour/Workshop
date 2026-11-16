# Stress test 2 of the .seq file plan

WORKING PATH by Tester, not a ruling.
Tests docs/design/SEQ-FILE-PLAN.md at e41300d (Designer's revision).
Rulings used: R26-R30 (DIRECTOR-RULINGS.md:103-125), with their
own held-7 parts kept held. Nothing here closes a QD.

## Verdict

- Holds with fixes. The revision took in all three test-1 fixes and
  the new rulings, honestly and in plain words.
- But three of the fixes are named, not defined: how the chain hash
  is built, what K is, and what the append check really checks.
- One new clash is missed: the lock (R30) against the 05 climb
  (R24) and against back-links on face 08.
- Two old holes stay open: forks with one address, and hand edits
  to face 04 made outside the compute.

## Top 3 fixes

1. Lock scope: say what a lock freezes. Pick: title and seated text
   of faces 00-04. Not frozen: new 05/06 counters (R24) and
   compute-only lines on 08 (back-links) and 09 (log).
2. Define the chain: chain = hash(previous chain + the new bytes).
   Check it against the compute's own memory before each write.
   Writes wait until the boot check ends; reads are marked `9`.
3. Define K per band: each band gets a full line every K of its own
   writes (K=64 suggested). Measured: about 1.1 KB per write, worst
   case about 129 short reads. A bad K policy is 3x worse.

## What the revision fixed from test 1

- Chain hash on signposts, checked once at start (D414 kept). Yes,
  but the build of the chain is not defined (item 1).
- Changed rows only, full every K. Yes, but K is not defined
  (item 2).
- Outside writers: append check and "builder writes elsewhere".
  Named only; the builder still writes books/ (item 3).
- Cite notes: 4 of 6 fixed (build.mjs:846, D326, addr in the
  example, "map" renamed "signpost").
- Not fixed: format.md:61 for "append-only log" (L98; heading is
  :60). format.md:42 for "only the compute appends" (L349; :18).
- Kept as Prima's wording: answers marked `7` until checked. Axiom
  9 (Axioms.md:29) is the mark for "not yet checked"; `7` means
  missing (Axioms.md:25). Suggest `9`.

## 1. Signpost chain hash

- Axioms: 6 (:23) nothing earlier is touched; 9 (:29) check first.
- What it covers: every byte before the signpost line. Good: it
  catches a line cut from the middle, which per-line hashes miss.
- Hole: the build is not said. If it means "hash of the whole file
  so far", every restart must rehash everything. Fix: chain =
  hash(previous chain + bytes since the previous signpost). Then
  any signpost can be checked from the one before it.
- Hole: the hash has no secret. Anyone who rewrites the file can
  write new, matching chains. So the chain catches damage and
  accidents, not a forger.
- Hole: a forged signpost with the right chain but wrong rows passes
  the boot pass. Only a replay that rebuilds the signposts and
  compares catches it. Replay is affordable: 1.3 s for 183 MB
  (release build, test 1).
- Can the check be skipped? The plan serves answers before the pass
  ends, marked. Writes before the pass ends are not covered. Fix:
  refuse writes until the pass and a background replay-compare end.
- After a cut tail: if the cut hits the last signpost, its `prev`
  is lost with it. The compute must scan back for the signpost
  before (at most one proposal back), then replay after it.
- Small files (S3): per-file fingerprints do not show a whole file
  that was deleted. The face 09 log must list each piece with its
  fingerprint, and the 09 log needs its own chain.
- D414 (DECISIONS-LOG:524): kept, if boot means chain pass plus
  replay-compare, and the log stays the source.
- Leads: person sees `9` until checked; model must not trust an
  unchecked answer; compute holds the last chain in memory.
- Result: holds with fix.

## 2. Changed rows only, full every K

- Axioms: 2 (:15) same shape; 6 (:23) add only.
- Lookup is bounded only if K is defined and full lines are planned
  per band. The plan says "full every K writes" for both levels.
- Simulated (20,000 writes; full lines every write = about 20 KB):

| K   | full lines for       | bytes/write | worst reads |
|-----|----------------------|-------------|-------------|
| 16  | all 100 bands        | 63,883      | 22          |
| 64  | bands touched        | 8,331       | 71          |
| 64  | each band, own count | 1,075       | 129         |
| 256 | each band, own count | 832         | 490         |

- Worst case reads: K book lines back, plus up to K band lines,
  plus page signpost and face. About 2K + 3.
- Warm cache, 129 reads is about 1.3 ms. Cold disk not measured.
- Pick: per band, K=64, recorded with its why (AGENTS.md:45).
- Leads: person can still read the last full line by hand; compute
  needs K in the header so readers know the bound.
- Result: holds with fix.

## 3. The append check (store.rs:941, build.mjs:846)

- Axioms: 6 (:23) the past is not rewritten; 1 (:13) halt, raise.
- The plan checks "the chain hash on the last signpost line". Read
  from the file, that only checks the file against itself. A
  rewritten file has its own good last line. Not closed.
- A true prefix rehash per write costs O(size): 0.4 s per 500 MB.
- Cheap fix: the compute remembers file length and last chain in
  memory. At runtime, any length change it did not make is refused.
  store.rs:941 must refuse, not cut. Cut only at boot repair.
- Builder: not moved. build.mjs:29 still writes books/, the
  compute's folder (store.rs:59). The plan leaves "elsewhere or
  append" open.
- R26 helps: the whole book is now an export. Pick: the builder
  writes exports to their own folder, never the stored folder.
- Race (check then write): yes. Another process can write between
  the two. Fix: the compute holds an OS file lock on its folder;
  the builder refuses to run while it is held.
- Leads: person told plainly why a write was refused; compute owns
  one folder alone (format.md:18).
- Result: breaks as written; holds with fix.

## 4. Locked pages and rework copies (Step 13, R30)

- Axioms: 6 (:23) rework is a new step; 8 (:27) links both ways;
  1 (:13) the lock is Matthew's.
- What locks a page: not defined (C11). The plan asks honestly.
- Clash missed: R24 (DIRECTOR-RULINGS.md:97) climbs face 05 after
  the seat and reseats updates. Face 06 notes keep coming
  (seqAddr.md:155). A locked page cannot do either as worded.
- Clash missed: rule 2 writes a back-link on the locked original's
  face 08. That is a change to a locked page.
- Can a lock be undone? Not said. R30 says "shouldn't change", and
  R21 says no override pages during this build. Pick: no undo; a
  new copy is the only way.
- Rework copy: a new page at a new address, new or same title. Its
  face 00 lineage names the original by address, title and
  fingerprint. If the book is complete, the copy may need another
  book. Not said in the plan.
- Links: old links still reach the original. Yes, by address.
- The lock event itself must be a face 09 line (who, when, why).
- Leads: person must see a page is locked before editing; model
  must propose a copy, not a write; compute refuses and explains.
- Result: holds with fix (lock scope, back-link rule).

## 5. Step 17, face 04 edits (R29)

- Axioms: 6 (:23) old versions kept; 4 (:19) why recorded.
- Where stored: not said for small files. Step 17 still talks of
  "the book file". Pick: under S3, a page folder holds 04 change
  files and full copies; plain text (R27, :111).
- Who writes: the compute only (Step 17 leads). Good.
- D414: the plan says D414 is not touched. But a 04 full copy is a
  snapshot of the face. Say it plainly: the change log is the
  source; a full copy is checked against it and never wins; a
  mismatch halts (D324).
- How a change is written (line, card, letter) is not designed.
- Leads: person reads one clean 04; model proposes small changes;
  compute rebuilds any version.
- Result: holds with fix.

## 6. Locked pages and face 04 edits together

- R29 (:118) lets people change their 04. R30 (:124) says a
  registered, linked page does not change. Both are rulings.
- It is a clash only if a lock comes early. If a lock comes late
  (seated and linked), working documents stay free.
- Pick (C12 A, Prima's reading): edit 04 freely before the lock;
  after it, edit a rework copy whose 04 starts from the original's
  latest version.
- R30 holds this part 7 (:125). Matthew must confirm.
- Result: holds with fix, if C11 picks a late lock.

## 7. The two open holes

(a) Two copies with one address (QD57, D427):
- Not closed. The plan lists it as still open.
- Lock helps: locked pages are the same in both copies, so links to
  them stay true. Only unlocked pages can differ.
- Pick: the compute halts if two files claim one address (axiom 1,
  :13). A copy that changed apart is given a new address before it
  comes back (D427: it is its own book).

(b) Hand edits to face 04 outside the compute:
- Not closed. Listed as open, and test 16 added.
- Pick: the compute keeps a current-view 04 file. At boot or before
  a read it compares the fingerprint. If changed: the logged 04
  stays live; the edit shows as a draft (R5); it is booked as a
  small change once who made it is known (axiom 1); if unknown, ask.
- On a locked page the hand edit goes to a rework copy, never in.

## Face 09 and R28

- Face 09 is the page log: fits R28 (:113-115). Good.
- R28's "short log in 00": handled. Step 8 says no, with three
  reasons (R25 churn, a copy, no faster). Held 7 for Matthew.
- Build gap: the core still refuses writes to 09 (validate.rs:
  232-233; face.rs:72), and seqAddr.md:158 says "unassigned".
- Stale: Step 8 (L300) says "until A3 is a numbered ruling". R28
  is now numbered.

## Choice picks (working path, not a ruling)

C11. What locks a page?
- Pick: seated (registered as live) AND the target of a seated,
  written face 08 link from another page; OR the book is marked
  complete by a compute-written entry approved by Matthew.
- Why: keeps R29 free edits before the lock; stops anyone freezing
  a draft by linking to it; "complete" needs a written act.
- Lock freezes title and seated 00-04 text. Not 05/06 new counters
  (R24) or compute lines on 08 and 09. Matthew must confirm.
- Other options: having face 00 at birth locks (blocks all edits);
  any link locks; either one alone locks.

C12. Can face 04 change on a locked page?
- Pick: A. No; edit a rework copy.
- Why: R30 "shouldn't change"; links stay true; R29 still met
  before the lock.
- Other option: B, 04 stays editable with versions kept (bends
  R30).

C1a. Which small files?
- Pick: S3 inside a folder per page (one file per face, plus 04
  change files and the 09 log), with a compute-only book journal
  for writes that touch several files.
- Why: fits R27 (code faces), R28 (09 log file), R29 (04 history);
  matches the kernel's sources. The journal has a precedent: the
  compute's `.queue` file (store.rs:307). It is not a page.
- Other options: S1 one file per book (least change); S2 one file
  per page (my test-1 pick, now weaker after R27-R29).

C13. Do addresses, titles and card keys stay ASCII?
- Pick: A. Yes, always.
- Why: the grammar (seqAddr.md:112, :280-281); file names come from
  addresses under S3; R30 links carry the title, so it must match
  byte for byte; D432 (DECISIONS-LOG:560) says so.
- Other option: B, widen them (touches grammar and every lookup).

## Cite check

- Checked 167 distinct cites; 52 are new since 29ec433.
- All 52 new cites point at the right line. No line mismatches.
- The 115 carried cites: lines unchanged at e41300d.
- Code cites (store.rs:59, :941, :1009-1023; build.mjs:846) match.
- Stale wording, not line errors:
  - L300 (Step 8): "until A3 is a numbered ruling" (R28 exists).
  - L504 (Step 15): "waits for a numbered ruling" (R26 exists).
  - L571 (Step 17): cites R4 :16 for ASCII; add R27 :111.
  - L230 (Step 5): R3 round trip; say if it stands after R26.
  - Sources list (L685-707) misses all 52 new cites.
  - Test-1 notes 1 and 3 still stand (L98, L349).

## Still open for Matthew

- C11: what locks a page, and what a lock freezes (R30 held 7).
- R24 against R30: may face 05 still climb on a locked page?
- C12: face 04 on a locked page (R30 held 7, :125).
- C1a: which small files.
- C13: ASCII for addresses, titles, card keys.
- R28: no short log in 00 (held 7 until he sees Step 8).
- R29: "So they can't be changed" (held 7, :120; C9).
- C2: should face 09 log refused or halted attempts?
- What makes a book "complete", and who says so.

## What I did not do

- Did not edit the plan, DESIGN.md, rulings, kernel, core, specs.
- No commit, push, merge, or seat. Nothing here is a ruling.
