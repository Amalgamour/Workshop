# Release check: what Designer compares before a design or pack goes out

state: v1, 2026-11-19, Designer. Checklist; it adds no new law.
authority: Matthew, t414u (docs/review/DIRECTOR-WORDS-t414u.md:3).
axioms: 1.7.8, 9

## 1. What this is, and why

Plain words: before Designer says a design or a pack is ready, Designer checks it
against the axioms, the address rules (seqAddr) and the design files. The check is
written down. Any FAIL stops the release.

Matthew's words (DIRECTOR-WORDS-t414u.md:3): "You must check design work against our
axioms and the seqadrr and our design. This wasn't done well. This should be part of
the designer's job. We have design files it should be comparing against before it
releases a design. This is a major flaw in designer right now."
(Spaces between sentences shortened.)

Why now: a WF job was packed at 90.50.00.0001. Book 00 is a shelf's own book, and
page 0001 is reserved. Matthew named this drift (DIRECTOR-WORDS-t413u.md:7-9). The
same mistake sits in 90.10.00.0001, 90.20.00.0001 and 90.30.00.0001
(DIRECTOR-WORDS-t413u.md:16, Prima's plain-words list). A check against seqAddr.md
section 1.2 and 6 would have caught it.

Related: t415u (DIRECTOR-WORDS-t415u.md:5): "Additional checking is required to verify
we aren't drifting very carefully planned out design work."

Axioms check of this checklist (Axioms.md lines):
- 1 Authority (Axioms.md:13): PASS. Matthew grants it (t414u); the check enforces
  existing rules and grants nothing new.
- 2 Fractal (Axioms.md:15): PASS. It inherits the rules where they live and points to
  them; it copies no rule text except short quotes with cites.
- 4 Why (Axioms.md:19): PASS. Each check names its source line; the why is there.
- 6 Lineage (Axioms.md:23): PASS. Re-checks are new files; old checks stay (section 2).
- 7 Missing (Axioms.md:25): PASS. Gaps and conflicts are listed, not filled (section 6).
- 8 Connection (Axioms.md:27): PASS. Every row links to file:line; matching is not proof.
- 9 Trial (Axioms.md:29): TENSION. This list was written by Designer and has not had a
  hostile pass from another view yet. Mark it 9 until it does.

## 2. When it runs

- Before any design doc or pack is reported as ready (to Prima, or anyone).
- Again on every new version of that design or pack. Each re-check is a new check
  file. Old check files are never edited (Axioms.md:23: "The past is not rewritten").
- Also when a ruling lands that touches an item already released: re-check, as a new file.

## 3. Hard address checks first (t413u)

Source: DIRECTOR-WORDS-t413u.md:7 and :9. Run these on every address in the artifact
(stamps, pack paths, folder names, links). Any miss is FAIL.

| # | Check | Source |
|---|---|---|
| A1 | Desk is 10 or higher (00-09 are system only) | t413u.md:7; seqAddr.md:30, :36-38 |
| A2 | Shelf is 10 or higher | t413u.md:7; seqAddr.md:30 |
| A3 | Book is 10 or higher; book is not 00 (DD.SS.00 is the shelf's own book) | t413u.md:7; seqAddr.md:29, :50 |
| A4 | Page is 0100 or higher (0000-0099 are reserved) | t413u.md:9; seqAddr.md:219-223 |
| A5 | Work sits in band 0400 (0400-0499) unless a ruling says otherwise | t413u.md:9; workflow-loop.003.md:45 |
| A6 | The band door ends in 00 (0400); job pages start at 0401 | t413u.md:9; seqAddr.md:241; workflow-loop.003.md:51 |
| A7 | Widths exact: DD.SS.BB.PPPP, each axis 2 digits, page 4 | seqAddr.md:14, :273-278 |
| A8 | Nothing sits in 0001-0099 as an override during this build | seqAddr.md:228; DIRECTOR-RULINGS.md:84 |

What seqAddr.md says on the same points (see section 6 for the gaps):
- Agrees: 01-09 reserved on every axis (seqAddr.md:30); 00 is the owner of the level
  above (seqAddr.md:29, :44); DD.SS.00 is the shelf's own book (seqAddr.md:50).
- Agrees: 0000-0099 are identity, reserved, contents, behavior, structure, not work
  (seqAddr.md:219-223).
- Names 0400 a "band head", not a "door" (seqAddr.md:241). Silent on "start in 0400".

## 4. Files to compare against

Use the version at the HEAD you check, and write its hash in the check file.

### 4.1 docs/spec/Axioms.md (the shape)
- X1 Every `axioms:` chain parses: dot orders, comma splits, only 3 takes M/P/C (:5).
- X2 Before a write, authority, missing, connection are answered (`1.7.8`) (:9, :27).
- X3 Authority is named and traced to a person; nothing claimed (:13).
- X4 No copy of a parent and no reinvention; a contradicting change has a named override (:15).
- X5 Every piece of work has a lead, named or by band default (:17).
- X6 Every rule has its why; no invented reasons (:19).
- X7 The frame says aim, where, what to do, where to stop, what done looks like (:21).
- X8 Changes are new steps; nothing earlier rewritten (:23).
- X9 Unknowns are marked 7, not filled (:25).
- X10 Links are written both ways or inherited; no link by matching (:27).
- X11 Not promoted without a hostile pass from another view (:29).

### 4.2 docs/spec/seqAddr.md (the geometry)
- S1 Address grammar holds (:264-284) and the extra rules (:286-291).
- S2 Reserved values: 00 owner, 01-09 reserved, 99 pointer (:27-31).
- S3 Desks 10-98 for user work (:38).
- S4 Page ranges and bands (:217-226, :240-243): bands are 100 pages; PP00 head; PP99 continuation.
- S5 Titles: lowercase, digits, hyphens; pages 1000+ need one; stamp title wins (:112-116).
- S6 Tails only where allowed; workflow state only on counters (:124-140, :287).
- S7 A page has face 00 plus one of 01-06 or 08 (:163).
- S8 Every 01/02 card has a 04 card with `why:` (:175-185).
- S9 One-way links are invalid (:251).

### 4.3 docs/spec/DIRECTOR-RULINGS.md (answered questions; governs older wording, :1)
- D1 Plain ASCII only in stored files (:16); face 04 must stay readable (:111).
- D2 Faces have no sentinels; counters run 01-98 (:37-38).
- D3 Stamp in face 00; face 00 is the registry (:54, :77).
- D4 Band head N?00 binds a band (:56-57). See conflict C1.
- D5 Below 0100 is four sections, not work space (:68-69).
- D6 Sets across bands match by last two digits AND title (:71-72).
- D7 No override pages during this build (:82-84).
- D8 Every design choice recorded; seated 05 links back to the design (:86-88).
- D9 05 climbs; reseat as an update, never rewrite (:94-97).
- D10 Links point to page address plus title, never a face (:123-125, :151-152).
- D11 Return and next step saved together; "couldn't look" kept apart from "isn't there" (:196, :200).

### 4.4 docs/spec/Design.md (system overview)
- G1 Each rule is defined in exactly one document; cite that one (:3-17).
- G2 Writers never touch book files; the compute validates and appends (:32-49, :84-88).
- G3 Anything the compute cannot resolve is elevated, never guessed (:88).

### 4.5 docs/spec/drafting.md (how a face changes)
- F1 No face rewritten from memory (:7).
- F2 Change by copy, note, merge, read again (:11-18); full `put` only for a new face (:33).
- F3 Derived content (boards, contents, menus) is not hand-written (:40).

### 4.6 docs/spec/workflow-loop.003.md (current draft) and workflow-loop.md (.002)
Both are drafts, "Director review required; not live" (.003:3; .002:3). .003 is the newer
copy of .002 (.003:4). Check against .003; note where .002 differs.
- W1 Roles: lead, builder, reviewer, compute; reviewer is not the builder (.003:22-32).
- W2 Band map: N3 build, N4 dev, N5 jobs, N7 colab (.003:38-51). See conflict C2.
- W3 Pack header fields and lint checks (.003:99-110, :234-250).
- W4 A pack links to its approval record and N4 revision (.003:88-90).
- W5 .002 calls N?00 the band "door" (workflow-loop.md:52); .003 says "band head" (.003:51).

### 4.7 docs/spec/face00.md (DRAFT, :3)
- P1 Stamp has address, title, type, state (:57-62); stamp address matches the real one (:71).
- P2 Type is one of general, system, code, workflow, band, pointer (:135-142).
- P3 A band head page has `type: band` (:141, example :337-368); job pages `type: workflow` (:140).
- P4 Registry fields allowed for the type (:195-210).

### 4.8 docs/design/DESIGN.md (condensed design, draft, :3)
- N1 Every sentence carries its source (:10).
- N2 Working paths are not rulings; they stay 7 (:17).
- N3 Desks 00 kernel, 01-09 branches, 10-98 user (:62).
- N4 Open: "Is a band head (0400) also a door [O23]?" (:149). See conflict C1.
- N5 Workflow loop state and roles (:253-265).

### 4.9 Director words files that are rulings
How picked: I read every docs/review/DIRECTOR-WORDS-*.md at this HEAD. A file is in if
Matthew answers a design question or sets a standing rule for pages, packs, addresses,
roles, instruction files or checks. Out: requests and asks for opinion (t212u, t240u-t241u,
t250u), budget and usage (t267u, t268u budget part, t285u, t301u), branches, hosting and
team setup (t316u, t335u, t399u-t400u, t401u), one-off folds (t305u), order of work
(t402u). Prima's "mapping" or "reading" lines are not his words; check his quote.

| File:line | One-line check |
|---|---|
| t223u.md:8 | A pack goes in the page's next open 05.NN counter |
| t226u.md:11 | A return states done, created, noticed, unprompted, overflow |
| t227u.md:5 | Jobs are handed to the compute (its template), not hand-built |
| t239u.md:10 | 05 counter tracks passes and what was learned |
| t243u.md:5-14, t249u.md:9 | One page per piece, faces 01-08 (one-page work) |
| t245u.md:5, :10, :12, :13 | 07 labs; checker uses tools; MVP on 04, stripped on 01; 08 links exact files |
| t249u.md:6, t254u.md:7 | The lead ("Prime") signs off; the compute closes |
| t255u.md:7 | Face 00 holds current lead and previous leads |
| t259u.md:7-12 | Lead checks 04, 06 and the last closed 05; finish pings the compute |
| t262u.md:5-7 | The page holds the compute; people and models outside |
| t263-T6.md:15, :25-26 | Checker (lead's assistant) and observer (drift, loops) are separate |
| t268u.md:5, t333u.md:7 | Rust for the compute core; NextJS allowed for the workshop front |
| t303u.md:3 | Spec and dev journal with whys go with the work |
| t306u.md:5, t306s1163.md:16 | Inherit kernel > desk > shelf > book; other books' choices are changeable defaults |
| t307u.md:8 | A book's 0000-0009 is for local changes |
| t309u.md:8, t310u.md:8, t311u.md:8, t312u.md:8 | Every instruction: axioms, why, authority |
| t326u.md:7, t327u.md:7 | AGENTS.md built from approved section templates |
| t328u.md:7, t329u.md:7 | Compute protects the book; build-stage allowances are temporary |
| t335s1296.md:6-8, :12 | Stage by path; push only granted branch; never print secrets |
| t373u.md:3, t378u.md:3 | Released AGENTS.md is hashed and locked; new one per pass only if needed |
| t375u-t377u.md:3, :6 | Kernel file names carry the page title |
| t379u.md:4, t380u.md:4 | AGENTS.md narrow; links only to valid hashed work |
| t381u.md:8, :17, :25 | Design and rule files never change mid pass |
| t384u.md:5 | In questions, mark the fractal option "(default)" |
| t387u-t391u.md:7 | Rulings can change; weigh new facts against old choices |
| t413u.md:7, :9 | Address checks A1-A6 |
| t414u.md:3 | This check, before release |
| t415u.md:5 | Check against the design, not model habits |

## 5. Output: the check file

Write docs/review/RELEASE-CHECK-<address>.md (one per artifact or band, new file each time).

```
# Release check, <address> (<artifact>)
checked by: Designer   date: <Toronto time>   checklist: RELEASE-CHECK.md @ <hash>
compared (path @ git hash): Axioms.md @ ..., seqAddr.md @ ..., ...
artifact (path @ hash or sha256): ...

| Item | Source file:line | Seen in artifact (path:line) | Result |
|---|---|---|---|
| A3 book not 00 | t413u.md:7 | pages/.../00.md:3 "address: 90.50.10.0400" | PASS |

verdict: RELEASE / BLOCKED (list each FAIL) ; tensions raised: ...
```

- Result is one of PASS, FAIL, TENSION, N/A. N/A needs a short why.
- Any FAIL blocks release. A TENSION goes to Prima as a question; it does not block
  unless it touches A1-A8.
- "Couldn't look" is written as such, never as PASS (DIRECTOR-RULINGS.md:200).

## 6. Conflicts found (open; not resolved here)

- C1 Is a band head a door? t413u.md:9 says "0400 being the door as it ends in 00".
  seqAddr.md:241 calls it a "band head". DIRECTOR-RULINGS.md:57 reads "'Door' is only
  the all-zero sentinel" (a reading under his "I like bands" answer, :56), and :5 says
  the door is the full zero. DESIGN.md:149 lists it as open (O23). workflow-loop.md:52
  (.002) says door; .003:51 says band head.
- C2 Where does a job pack live? t413u.md:9 says start work in 0400; t223u.md:8 says the
  page's own 05.NN; t249u.md:9 likes one-page work. workflow-loop.003.md:46 and :99 put
  packs on an N5 page (0501.05.NN). .003 is a draft, not live (:3).
- C3 seqAddr.md is silent on two t413u points: "work starts at 10" as a stated rule
  (it only reserves 01-09, :30), and "start work in 0400" (it says 0100-0999 are kernel
  standard bands, :224, and 1000-9998 user space, :225).
- C4 What "work" means below 0100. t413u.md:9: "work shouldn't exist there".
  DIRECTOR-RULINGS.md:69 reads 0020-0099 as "working pages, not just locations"
  (behavior and structure). Likely both hold (system pages yes, job work no), but unconfirmed.

## 7. Honest limits

- Rulings newer than this file are not in it. At each use, list DIRECTOR-WORDS files
  newer than the checklist hash and read them first (t388u: rulings can change).
- Several checks need judgement (X4 drift, X7 frame, X11 trial, F1 memory). Write what
  was seen, not just PASS.
- face00.md, DESIGN.md and both workflow-loop files are drafts. A FAIL against a draft
  alone is a TENSION, unless a ruling or seqAddr.md backs it.
- This list is Designer's own work and has not faced a hostile pass (axiom 9).
- Line numbers are for the hashes in the check file; they drift when files change.

## v2 note (2026-11-19, 1:18 PM EST, Designer): model habits, and work at 99

This note adds to v1 above. v1 is not rewritten (Axioms.md:23).

Authority: Matthew, t415u (docs/review/DIRECTOR-WORDS-t415u.md:3 and :5, on b11b48f).
His words (:5): "Work done here is often very novel. As such be very careful about
assuming the averages from the LLM model's weights. Additional checking is required to
verify we aren't drifting very carefully planned out design work."
(Spaces between sentences shortened.) He gave it as "An addition for our agents.md
manager" (:3). Using it here too is Prima's ask; the plain-words line at :7 is Prima's
reading, not his words.

Why: 90.50.00.0001 looked "normal" (first book, first page) and was wrong
(DIRECTOR-WORDS-t413u.md:7-9). A habit felt like a rule.

New hard checks (run with A1-A8; any miss is FAIL):

| # | Check | Source |
|---|---|---|
| H1 | Any choice that looks normal or habitual (page 0001, book 00, a "usual" default, a first free slot, a common file layout) is traced to a design file:line. No trace: FAIL. Write the trace in the check row. | t415u.md:5; t413u.md:7-9; Axioms.md:15, :25 |
| A9 | No work at 99 on any axis, at PP99 (band continuation) or at 9999 (book continuation). These are pointers, not work. | seqAddr.md:31, :39, :226, :242, :249; DESIGN.md:137; crates/seqaddr-core/src/addr.rs:186-187, :200-208, :246-248 |

A9 is settled from the files, which agree: seqAddr.md calls 99 and 9999 a pointer to
the next location (:31, :249), PP99 the band's continuation (:242), desk 99 a reserved
pointer (:39). DESIGN.md:137 quotes the Director's own seqaddr page: "Those addresses with
a seq00 or seq99 are special locations and cannot be normal pages". t413u does not mention
99; it does not conflict.

t416u (design-alignment review before a return completes): there is no
docs/review/DIRECTOR-WORDS-t416u.md at this HEAD. It is relayed by Prima only and has no
recorded words yet. Until it is recorded, run it as check T1, result TENSION at most:
"for novel work, a design-alignment review is confirmed before the return completes."
Do not quote it as his words.

Axioms check of this note (t311u):
- 1 Authority (Axioms.md:13): PASS for H1 (t415u). TENSION for T1 (no record yet).
- 2 Fractal (Axioms.md:15): PASS. A9 applies the same sentinel shape at the 99 end
  that A1-A4 apply at the 00 end.
- 4 Why (Axioms.md:19): PASS. Each check names its source.
- 6 Lineage (Axioms.md:23): PASS. Added as a new step.
- 7 Missing (Axioms.md:25): PASS. t416u is marked missing, not filled in.
- 9 Trial (Axioms.md:29): TENSION. Still no hostile pass on this list.
