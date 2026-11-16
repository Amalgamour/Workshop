# The .seq book file: a design plan

state: draft plan, `7` (open). Not a ruling. Nothing here is law.
made: Mon 16 Nov 2026, Designer (design partner for Prima). Director: Matthew, the only approver.
revised: Mon 16 Nov 2026, after Director answers t171u (11:16 AM EST) and t172u (11:17 AM EST), Tester's stress test (50fdfac), Director rulings t175u (11:24 AM EST), and Tester's stress test 2 (e99665e), Director ruling R31 (t184u, 11:47 AM EST, entered by Prima in f2c8459), Tester's prototype results (SEQ-PROTO-RESULTS.md, 7697815), Director ruling R32 (t191u, 12:02 PM EST, entered by Prima in ff60c28, time fixed in 7289c45), Director ruling R33 items 1, 3 and 4 (t192u, 12:06 PM EST, entered by Prima in 865b880), Director ruling R34 (t195u, 12:16 PM EST, entered by Prima in a8e8dd3), Director ruling R35 (t197u, 12:20 PM EST, entered by Prima in 8f6e9a7) with its note (t198u, 12:23 PM EST, 9717698), and Director ruling R36 (t200u, 12:25 PM EST, entered by Prima in 71e45ee), all relayed by Prima. See "Changes since 29ec433".
why: Matthew asked today (16 Nov 2026, 11:04 AM EST, passed on by Prima) for a design plan for the book file. He said a book is a .seq file, it is basically a self-contained database file, and it should work like a pyramid.
status of every idea below: Matthew's first ideas from today are marked "Matthew's idea, 16 Nov 2026". His later answers are marked "Director answer, t171u (relayed by Prima)" or "t172u". His rulings of 11:24 AM EST are marked "Director ruling, t175u (relayed by Prima)". His answers of 11:47 AM EST are marked "R31, n" and those of 12:02 PM EST "R32, n" (item n of Prima's entry). Every question for Matthew follows his standing rule (t189u): the question, a proposed answer, the why, and the axiom lines checked, each marked pass or tension. Prima entered them in DIRECTOR-RULINGS.md as R26-R30 (commit e1a60aa) R31 (commit f2c8459), R32 (commits ff60c28, 7289c45), R33 (commit 865b880) and R34 (commit a8e8dd3); this plan cites those entries and does not number or edit rulings. Anything not found in a Workshop source is marked "New (not in any source)". Rulings R1-R25 are quoted only where they already exist.
does not: edit DESIGN.md, DIRECTOR-RULINGS.md, the kernel, the core, or any spec file; close any QD question; write a 00.counter; seat anything.

---

## Plain-words summary

Matthew has now ruled on the last three top choices (R32, 12:02 PM EST, t191u). This summary says where the plan stands.

The real copy is kept in small files: one folder per page, and one file per face inside it. Face 00 holds the page's type and its list of faces. Like a registry, face 00 has locked fields that never change (address, title, page type) and open fields that may change, such as the face list and the page's state. Where each face's file sits is kept in the page signpost (Prima's "page index"), so face 00 does not change on every write. A whole book as one `.seq` file is something you export.

The pyramid is the shape of that exported file. The computer keeps the same signposts over the small files, so finding any page is quick. Signposts are never the real copy; they can always be rebuilt.

Each page's log and each signpost carries a check number (the *chain*), starting from the page's own address, so a copied page cannot pass as another. Until the start-up check is done, answers are marked "not yet checked" (`9`) and writes are refused. Only the computer may write the stored files. Tester's throwaway prototype is fast (one lookup in a book of 100,000 writes took 49 microseconds warm) and found five things to fix, now in the plan.

**A link points to the page, not to a version.** A link is the page's address and title. Following it always gives the page as it is now. Matthew's example: a page about "Jim" changes over time, and a link to it should let the computer find out about Jim, not some old wording. Old versions stay in the page's log.

**What never changes:** a page's address and title, once paired, and the fact that the page exists. The same title may appear at other addresses (R34): titles can be reused, so the address is what tells pages apart. A retired page drops out of search and does not hold on to its title. **Face 00's locked fields lock once it is done**; its open fields and the other faces may still change, each change a new step with the old value kept. A page that exists and is linked to can never be deleted, only retired: it stays on record but drops out of active searches.

**General pages stay editable** the Google Docs way: every edit is a small change, with a full copy every so often, and old versions never change. **System pages** lock their main faces (00 to 04) once linked (R31, confirmed by R34): they are back end, built for control, not for users; the computer may still add work packs, notes, back-links and log lines. To improve a locked page, a developer makes and promotes a new copy at a new address, linked both ways. Pages may hold office kinds, such as a spreadsheet or a word document.

Face 04 is the person's face and stays plain text. Other faces may be compact computer code. Addresses are back end only; people see titles. A book is a working journal, retired to the shelf when its work is done, possibly partly complete. Face 09 is the page's log; face 00 keeps no log.

Any page may have a menu on face 03, written by the computer, listing its sections. The model reads the menu first and loads only the sections it needs (R35). Copied text is checked in order: the computer first, by its rules; then the model; then a person if the model is not highly sure. The details are in `docs/design/SECTIONS-AND-CARDS.md`.

Matthew asked that every question come with a proposed answer, the reason, and the axioms it was checked against. The open choices are written that way. The top three: which face 00 fields are locked and which are open, beyond the address, title and type Matthew named? When an address lookup reaches a retired page, does it stop there or fall through to the shelf's page with the same number? And when several pages share a title, how does a title search avoid picking the wrong one?

---

## Changes since 29ec433

29ec433 was the first version of this plan. f6296ba added Step 17 (face 04, t172u). d034948 added Matthew's t171u answers. c077d0c folded in Tester's stress test. e41300d added his t175u rulings. 6dbe53c folded in Tester's stress test 2. f8ac4d9 folded in Director ruling R31 (t184u), and cad88d0 Tester's prototype. a199955 folded in Director ruling R32 (t191u). db17f8a folded in Director ruling R33 items 1, 3 and 4 (t192u). This version folds in Director ruling R34 (t195u). Old commits are not changed; this is a new step on top (axiom 6) [Axioms.md:23].

- **A1 (t171u), faces as code.** New in Step 3, Step 7, Step 11 and Step 14. Face 04 stays readable; other faces may be compact code. At d034948 this was a pending narrowing of R4; it is now settled by t175u, 2 (see below). C3 is updated.
- **A2 (t171u), small files stored, books exported.** Steps 1, 2, 4, 5, 6, 9, 10 and 15 are reframed: the pyramid and book signpost are now the export format, and possibly a derived signpost over the small files. The stored form is the small files. C1 is updated, and the git-blob fingerprint flag in Step 10 is updated.
- **A3 (t171u), face 09 is the log.** Step 8 is rewritten: face 09 is the page log (his answer). The short log in face 00 is judged: no, with the reason. C2 is updated; whether refused or halted attempts are logged stays open.
- **A4 (t172u), face 04 history.** Step 17 (added in f6296ba) is kept. "Go with Google's approach" settles it. The Google Docs against Word comparison is kept only as the reason. C9 ("So they can't be changed") is kept, still open.
- **A5 (t171u), links name pages, not faces.** Step 13 is rewritten and checked against seqAddr.md.
- **Open choices.** C1, C3, C6, C7 and C8 are marked "updated by t171u". C2 is updated by t171u (A3). The top 3 are recomputed. A "Still open" list is added.
- **Summary.** Rewritten above.
- **Tester's stress test folded in** (docs/design/SEQ-FILE-PLAN-TEST.md, commit 50fdfac; Tester's file not edited). Fix 1: a running chain hash on every signpost line, checked once at compute start; answers `7` until then (corrected to `9` in this revision, Step 10); a mismatch halts (D324); D414 kept (Steps 5, 10, C4). Fix 2: signpost lines hold only changed rows, with a full line every K writes (Steps 5, 9). Fix 3: the compute checks a hash of earlier bytes before each append, and the builder writes elsewhere or appends instead of rewriting whole files (Steps 11, 15). Cite notes: the builder's whole-file write is now cited at `kernel/build.mjs:846`; D326 is cited in Step 6; the example signpost line now has the book `addr`.
- **Director rulings t175u (11:24 AM EST) folded in.** R3 and R4 are updated by t175u (entered by Prima as R26 and R27). C1 and C3 are settled. The lock ruling (t175u, 3) rewrites Step 13 with a rename rule, squares Step 17 with it, and marks C9 likely answered, pending Prima's confirmation. New choices C11 (what locks a page), C12 (face 04 on a locked page) and C13 (grammar stays ASCII). Top 3 recomputed. Summary rewritten again.
- **Tester's stress test 2 folded in** (SEQ-FILE-PLAN-TEST-2.md, commit e99665e; Tester's file not edited). Lock scope: the title and seated 00-04 text freeze; new 05/06 counters, 08 back-links and 09 log lines go on, compute-only (working path, Tester); the R24 against R30 clash is named (Step 13, new C14). Chain defined: hash(previous chain + new bytes), checked before each write against the copy in memory; reads `9` and writes refused until the start-up check ends (corrects the earlier `7`, with the reason). store.rs:941 described correctly (refuses shorter files, cuts longer ones at every append today; Tester's fix: refuse at runtime, cut only at start-up repair). OS file lock added; builder output moved out of `books/` (Step 11). K = 64 per band, with Tester's measured numbers (Step 5). Tester's picks recorded for C11, C12, C1a and C13 (working paths, still open). Stale wording fixed in Steps 8, 15 and 17. format.md cites fixed (:60 for the append-only heading; :18 for "only the compute writes"). Face 09 build gap listed. Sources rebuilt from every cite in the file. Top 3 recomputed (C11, C14, C12).
- **Director ruling R31 (t184u, 11:47 AM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:127]-[DIRECTOR-RULINGS.md:148], commit f2c8459; not edited). C11, C12, C14, C1a and C13 are marked settled by R31, each with what it now is. C9 is closed (R31, 10). Step 1 now has the per-page folder with one file per face, face 00's type that holds and orders them, and books as working journals. Step 3 adds office kinds. Step 8 records R31, 9 (no log in 00; the last-change note held 7). Step 13 is rebuilt: titles fixed for every page, system pages lock, general pages stay editable, developer-only promotion. Step 17 is squared with general pages. Tensions R31 creates with earlier rulings and with Tester's findings are listed in Step 13 and as new choices C15-C20; none is resolved here. Places where Prima's relayed summary differs from her R31 entry are listed under the R31 block. The summary, still-open list and top 3 are recomputed (C16, C15, C17).
- **Tester's prototype results folded in** (SEQ-PROTO-RESULTS.md, commit 7697815; Tester's file not edited). Working paths (Tester), not rulings: the book line is the commit point, and band lines after the last book line are dropped at start-up (Steps 9, 11); face 04's current view is written after its face 09 line (Steps 9, 17); each page's face 09 chain is seeded with the page address plus a book birth id, and all signposts missing is a halt that asks a person (Step 10); the check-then-write gap (2 of 20 tries) and what closes it (Step 11). Plan gaps filled: the chain across many small files (Step 10); C7 split into the chain hash and the file fingerprint (Step 10, C7); face 04's current-view file, its write order, the small-change format and the full-copy cadence (Step 17); how a hand edit is booked and who made it (Step 17). Measured numbers quoted exactly in Step 16, with what was not measured.
- **Director ruling R32 (t191u, 12:02 PM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:150]-[DIRECTOR-RULINGS.md:156], commits ff60c28 and 7289c45; not edited). C15, C16 and C17 are closed, each with what it now is. R32, 1 narrows R30 and R31, 1: a link gives the current page; what is fixed forever is the address-title pairing and the page's existence. Every place that assumed a link freezes a version is fixed or flagged (Steps 1, 6, 10, 13, 16, 17; C10, C11, C14; Still open; the list is under the R32 block). New tensions are named (C21-C23). The open choices are rewritten in Matthew's four-part form (t189u). Summary, still-open list and top 3 recomputed (C21, C22, C23).
- **Director ruling R33, items 1, 3 and 4 (t192u, 12:06 PM EST) folded in as approved** (entered by Prima at [DIRECTOR-RULINGS.md:158]-[DIRECTOR-RULINGS.md:166], commit 865b880; not edited; Prima confirmed, and Tester is building them in code). Item 1 approves Tester's fix to move the builder's output out of `books/` (Step 11, Step 15, Still open). Item 3 approves refusing a line dated earlier than the line above (Step 10). Item 4 approves refusing requests with the wrong Host header (Step 11, noted; it is a server check, not a file rule). Item 2 (refuse copied text) is held 7 and designed separately in `docs/design/SECTIONS-AND-CARDS.md` (commit 3c7401f). C21-C23 are not touched.
- **Director ruling R34 (t195u, 12:16 PM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:168]-[DIRECTOR-RULINGS.md:174], commit a8e8dd3; not edited). C21 closed (system pages freeze 00-04 once linked). C23 closed: this plan's proposal is rejected; titles may be reused and a retired page does not block its title. C22 is held 7 and unchanged. Every place that assumed titles are unique is fixed or flagged (list under the R34 block). New questions C25-C27 in the four-part form. Summary, still-open list and top 3 recomputed (C22, C25, C26).
- **Director ruling R35 (t197u, 12:20 PM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:176]-[DIRECTOR-RULINGS.md:182], commit 8f6e9a7; not edited). It answers SECTIONS-AND-CARDS.md Q1-Q3, not this plan's open choices. Places touched: the summary; Step 7 (the face 03 menu and loading sections one at a time); Step 8 (copy-check steps in the face 09 log, a tension with C2); Step 13's limit on face 03 noted; C2 and C10 notes; the still-open list. The decisions.md:404 update for the menu card is pending in the spec; this plan does not edit decisions.md. C25-C27 are unchanged (Prima is holding them). Top 3 unchanged (C22, C25, C26).
- **R35 note (t198u, 12:23 PM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:184]-[DIRECTOR-RULINGS.md:186], commit 9717698; not edited): for a general query the compute hands the model menus, not data. Step 7 updated.
- **Director ruling R36 (t200u, 12:25 PM EST) folded in** (entered by Prima at [DIRECTOR-RULINGS.md:188]-[DIRECTOR-RULINGS.md:190], commit 71e45ee; not edited). C22 is closed. Face 00 is redone as locked fields and open fields (Step 1), with a proposed placement of every existing field. Everything that moved records off face 00 because it was locked is rewritten (list under the R36 block). Tests 12 and 31 fixed; tests 34-36 added. New questions C28 and C29. Summary, still-open list and top 3 recomputed (C25, C26, C28). C25-C27 unchanged.
- **Rename: "map" is now "signpost".** "Map" is face 08's name [seqAddr.md:157] and "index" is used for the dictionary [seqAddr.md:230], so the plan's book map, band map and page index are now the book, band and page signposts.

---

## Director answers and rulings today

Matthew's words are quoted exactly as recorded by Prima in `docs/spec/DIRECTOR-RULINGS.md` (R26-R30 in commit e1a60aa; R31 in commit f2c8459; R32 in commits ff60c28 and 7289c45). This plan does not number or edit rulings; it cites Prima's entries. Where Prima's entry says "Held 7", this plan keeps it held.

**Director ruling R36, t200u (relayed by Prima), 12:25 PM EST** [DIRECTOR-RULINGS.md:188]. It answers C22 (after Prima's t198s761). Quoted exactly from the file:

- **R36, C22:** "Ok so on face 00 think of it like windows registry. We have fields that nevere change and lock, like it's address, it's title, it's page type. Others could change. We can have a split on this." [DIRECTOR-RULINGS.md:189]. Read: "face 00 is split into two kinds of fields. Locked fields (address, title, page type, and any others named later) are set once and never change. Open fields may change, so R25's records on 00 can continue. "Once the 00 is done it's locked" (R32) applies to the locked fields. Which fields fall in which group beyond the three named is open. C22 is closed." [DIRECTOR-RULINGS.md:190]

**Where Prima's relayed summary differs from her R36 entry** (checked line by line; R36 governs):

- Prima's summary lists the locked fields as "address, title, page type", as if complete. His words say "like" those three, which are examples; the Read says "and any others named later" and "Which fields fall in which group beyond the three named is open" [DIRECTOR-RULINGS.md:190]. That gap is C28.
- Prima's summary says R25's records "continue in the open fields". His words do not mention R25; they say only "Others could change. We can have a split on this." [DIRECTOR-RULINGS.md:189]. The tie to R25 is the Read's [DIRECTOR-RULINGS.md:190]. "We can have a split" is also softer than a settled design.
- The summary leaves out the Read's line that "Once the 00 is done it's locked" (R32) now applies to the locked fields [DIRECTOR-RULINGS.md:190], and that C22 is closed.
- The Windows registry comparison matches.

**Places changed by R36, and why:**

- Summary: face 00 described as locked and open fields; the "never changes" paragraph narrowed to locked fields; top 3 now C25, C26, C28.
- Step 1: the C22 tension replaced by the locked/open design, the field placement, how an open field changes (00 counter, then face 09; old values kept), why face 00 still stays small (R25), new faces, and the system-page tension (C29). Step 1's Better and Three leads updated.
- Step 6: the stale "this plan follows D326" (no `faces:` list in face 00) rewritten: `faces:` is an open field the compute writes.
- Step 7: the C22 tension note on the face 03 menu rewritten: adding a menu is an open-field change.
- Step 8: open fields are current values, not a log; face 09 stays the log.
- Step 13: "face 00 locks" narrowed to its locked fields; the two C22 tensions marked settled; Axioms, Better and Three leads updated.
- Step 16: tests 12 and 31 rewritten for the split; tests 34-36 added.
- C22 moved to settled, its proposal (seat records and new faces off face 00) withdrawn. C15, C17, C11 and C24 notes updated. New C28 (TOP) and C29. C25-C27 not touched.

**R35 note, t198u (relayed by Prima), 12:23 PM EST** [DIRECTOR-RULINGS.md:184]. Quoted exactly: "Yes the menu is how the compute handles giving information to a model. If a model has a general query about "Jim" for example. The compute might have "jim" as a key word in 4 pages. instead of handing the model all the data in those pages it hands it the menu. So the model can decide what it should request first." [DIRECTOR-RULINGS.md:185]. Read: "for a general query, the compute finds the pages holding the key word and hands the model their face 03 menus, not their data. The model then asks for the sections it needs first." [DIRECTOR-RULINGS.md:186]. Prima's summary ("the model picks which sections to request") drops his "first" and narrows to sections; his words say the model decides "what it should request first", and say "the menu", singular, while the Read and the summary say menus, plural, and "face 03" (the Read's word). Folded into Step 7.

**Director ruling R35, t197u (relayed by Prima), 12:20 PM EST** [DIRECTOR-RULINGS.md:176]. It answers SECTIONS-AND-CARDS.md Q1-Q3 (Prima answered item 3 in t197s757). Quoted exactly from the file:

- **R35, 1, refuse or flag copies:** "Yes this is where the elevate comes in. If the comp can't solve according to it's code, it gives it to the model, if the model can't solve to a high degree of certainty. then it goes to the person." [DIRECTOR-RULINGS.md:177]. Read: "the proposal stands (refuse exact and unmarked copies, flag partial overlap, allow links, key words, and cited quotes), and anything uncertain is elevated: compute first by its code, then the model, then a person if the model is not highly certain." [DIRECTOR-RULINGS.md:178]
- **R35, 2, a face 03 menu on every page:** "Yes of course, a page might contain the piece of a story. As such it might be broken into a number of sections perhaps dozens or more. So instead of the model eating everything it only gets what it needs." [DIRECTOR-RULINGS.md:179]. Read: "approved. Any page may have a compute-written face 03 menu of its sections, so a model loads only the sections it needs. This updates the pages 0001-0099 limit in decisions.md:404 for the menu card." [DIRECTOR-RULINGS.md:180]
- **R35, 3, a section reusing another page's card:** "Why would a section reuse a card?" [DIRECTOR-RULINGS.md:181]. Read: "not ruled; he questioned the premise. Prima answered (t197s757) that it shouldn't: a section links to the page (R32), and the compute serves only the needed piece. Held 7." [DIRECTOR-RULINGS.md:182]

**Where Prima's relayed summary differs from her R35 entry** (checked line by line; R35 governs):

- Item 1: the summary gives only the order (compute, model, person). The Read also says "the proposal stands": refuse exact and unmarked copies, flag partial overlap, allow links, key words and cited quotes [DIRECTOR-RULINGS.md:178]. In Matthew's words the model is used only when the compute "can't solve according to it's code" [DIRECTOR-RULINGS.md:177].
- Item 2: the summary says it "updates decisions.md:404". The Read limits that to "the menu card" [DIRECTOR-RULINGS.md:180]; other face 03 cards keep the 0001-0099 rule. The summary also leaves out his reason: a page may hold part of a story in "dozens or more" sections [DIRECTOR-RULINGS.md:179].
- Item 3: matches (held 7). Matthew asked a question [DIRECTOR-RULINGS.md:181]; "it shouldn't" is Prima's answer, not his [DIRECTOR-RULINGS.md:182].

**Places changed by R35, and why:**

- Summary: one paragraph on the menu and the copy check (both now approved in outline).
- Step 7: the page signpost also points at each section inside face 04, and the compute serves sections one at a time through the face 03 menu (R35, 2).
- Step 8: copy-check refusals and elevation steps are proposed as face 09 lines (SECTIONS-AND-CARDS.md Q8); this rubs against C2's "plain refusals no".
- Step 7 also notes that the face 03 limit of pages 0001-0099 [decisions.md:404] no longer applies to the menu card; the spec update is pending. It named a tension with C22 (a locked face list without face 03); R36 has since closed C22 and the note is rewritten (see R36).
- C2: a note on the copy-check tension. C10: cross-page card cites are dropped in the sections design (held 7), so cards on another page are reached by a link, not a cite.
- Still open: the R33, 2 bullet now says the outline is approved by R35 and Q3 is held 7.

**Director ruling R34, t195u (relayed by Prima), 12:16 PM EST** [DIRECTOR-RULINGS.md:168]. It answers this plan's C21 and C23 (via Prima's t193s748). Quoted exactly from the file:

- **R34, 1, C21:** "yes I think we freeze system pages. They are backend and designed for control not for user to access." [DIRECTOR-RULINGS.md:169]. Read: "system pages freeze once linked (faces 00-04). They are back end, built for control, and not for users to access." [DIRECTOR-RULINGS.md:170]
- **R34, 2, C22:** "I need more explaination on this one." [DIRECTOR-RULINGS.md:171]. Read: "not ruled. Prima explained in t195s752. Held 7." [DIRECTOR-RULINGS.md:172]
- **R34, 3, C23:** "So we don't lock words in books. if you look at workflow you already know that titles can be reused." [DIRECTOR-RULINGS.md:173]. Read: "Designer's proposal is rejected. A retired page does not block its title. Titles may be reused, as the existing workflow already allows. Note: R31 item 1 fixes the address-title pairing, not the title alone." [DIRECTOR-RULINGS.md:174]

**Where Prima's relayed summary differs from her R34 entry** (checked line by line; R34 governs):

- C21: the summary says "system pages freeze". The Read says when and what: "once linked (faces 00-04)" [DIRECTOR-RULINGS.md:170]. The summary says "not for users"; the file says "not for user to access" [DIRECTOR-RULINGS.md:169], which is stronger: users do not access them at all. Neither says what makes a page a system page (C27).
- C23: the summary leaves out Matthew's first sentence, "So we don't lock words in books." [DIRECTOR-RULINGS.md:173], and the Read's note: "R31 item 1 fixes the address-title pairing, not the title alone." [DIRECTOR-RULINGS.md:174]. "A retired page does not block its title" is in the Read, not in his words.
- C22: matches ("Held 7"). The file adds that Prima explained it in t195s752 [DIRECTOR-RULINGS.md:172].

**Places changed because they assumed titles are unique (R34, 3), and why:**

- Summary: "a page's address and title, once paired" could read as the title being reserved. Now says the same title may appear at other addresses, and the address tells them apart.
- Step 13, "Titles are fixed for every page": said the pairing is "never given to anything else". Now: the address is never given another title and never reused; the title may be reused at other addresses (seqAddr.md:114 already said "several pages may share a title").
- Step 13, retire bullet: "Its address and title are never reused". Now: the address is never reused; the title may be.
- Step 13, new paragraph "Titles may repeat": how a link and a lookup stay safe.
- Step 13, rename rule 2: a new page may take any title, including one another page already has.
- Step 13, tensions: "Same-titled pages must be told apart without showing addresses" kept and sharpened (C13a); "title lookup would quietly find the shelf's page of the same name" replaced (lookup is by address; C25, C26).
- Step 16, test 30 rewritten; test 33 added.
- C13a: the same-title part now rests on R34, 3; the proposed answer shows context, never the address.
- C23: closed; its proposal (a retired page blocks title fall-through) is rejected.
- Still open, fork note: two pages with the same title at different addresses are not a fork; only two files claiming one address are.

**Director ruling R33, t192u (relayed by Prima), 12:06 PM EST** [DIRECTOR-RULINGS.md:158]. Tester's four fixes from the code-vs-lessons check. Items 1, 3 and 4 are approved; item 2 is held 7. Quoted exactly from the file:

- **R33, 1, Builder (approved):** "Yes, books change through compute not by models. Models can be wrong and having them answer a question correctly 100% of the time can be an issue." [DIRECTOR-RULINGS.md:159]. Read: "approved. The book builder stops writing into books/ and makes an export instead (R26). Books change only through the compute's gate." [DIRECTOR-RULINGS.md:160]
- **R33, 2, Copied text (held 7):** see `docs/design/SECTIONS-AND-CARDS.md`. Read: "not yet approved. A section is a piece of work in face 04. Cards live in faces 01, 02, and 03, and a face 03 menu can say what small pieces live on a page. On normal pages, faces 01 and 02 usually hold only key words. The copy check needs design work against this before it is built. Held 7." [DIRECTOR-RULINGS.md:162]
- **R33, 3, Clocks (approved):** "I agree" [DIRECTOR-RULINGS.md:163]. Read: "approved. Refuse a line dated earlier than the line above it." [DIRECTOR-RULINGS.md:164]
- **R33, 4, Host check (approved):** "I agree." [DIRECTOR-RULINGS.md:165]. Read: "approved. Refuse requests that arrive with the wrong Host header." [DIRECTOR-RULINGS.md:166]

**Director ruling R32, t191u (relayed by Prima), 12:02 PM EST** [DIRECTOR-RULINGS.md:150]. It answers Prima's C16, C15 and C17 in t188s728 (the same labels as this plan's choices). His words and Prima's Read are quoted exactly from the file.

- **R32, 1, Links (C16):** "Lets say we have a book about relationships... So say page 1024 is about "Jim" That might be changed and updated. We don't want to link to exact wordings of a page face. But be linked so the compute can find out about Jim. So I think your answer is wrong, if you disagree tell me why." [DIRECTOR-RULINGS.md:151]. Read: "Prima's proposal (a link locks the version it points to) is rejected, and Prima agrees. A link points to the page (address plus title), and following it gives the current page. Old versions stay in the log (R29). This narrows R30 and R31 item 1: what is fixed forever is the address-title pairing and the page's existence, not the wording of a general page's faces." [DIRECTOR-RULINGS.md:152]
- **R32, 2, System pages and lock (C15):** "Yes, when a page is created, it gets its properties is assigned a title and seqaddr. Once the 00 is done it's locked the info might change on the faces but once a page exists and is linked it can only be retired, so the record is there, and not be in active searches." [DIRECTOR-RULINGS.md:153]. Read: "at creation a page gets its properties, title, and address. Once face 00 is done, face 00 is locked; the other faces may still change. Once a page exists and is linked, it can't be deleted, only retired. A retired page stays on record but leaves active searches." [DIRECTOR-RULINGS.md:154]
- **R32, 3, Face list (C17):** "I agree" [DIRECTOR-RULINGS.md:155]. Read: "face 00 holds the page type and its face list. Where each face sits is kept in the page index, so face 00 doesn't change on every write." [DIRECTOR-RULINGS.md:156]

**R32 narrows earlier rulings (their text is not rewritten, axiom 6 [Axioms.md:23]).** R30's Read said a registered, linked page is locked, "no rename, no change" [DIRECTOR-RULINGS.md:125]. R31, 1's Read said "Once a page is linked, it is done" [DIRECTOR-RULINGS.md:130]. R32, 1's Read: "This narrows R30 and R31 item 1: what is fixed forever is the address-title pairing and the page's existence, not the wording of a general page's faces." [DIRECTOR-RULINGS.md:152]. R32, 2 adds that face 00 locks once done for every page [DIRECTOR-RULINGS.md:154], which R25's "We record the changes onto 00" [DIRECTOR-RULINGS.md:100] did not foresee (C22, since settled by R36: the lock applies to face 00's locked fields [DIRECTOR-RULINGS.md:190]).

**Where Prima's relayed summary differs from her R32 entry** (checked line by line; R32 governs):

- Item 1: the summary says a link gives the current page and "This narrows R30 and R31 item 1". The Read adds "not the wording of a general page's faces" (the word "general" matters here) [DIRECTOR-RULINGS.md:152]: the narrowing is stated for general pages; system pages are not mentioned (C21). The summary also leaves out that Prima agrees, and Matthew's own "if you disagree tell me why" [DIRECTOR-RULINGS.md:151].
- Item 1: the rejected proposal is described as "a link locks the version it points to" [DIRECTOR-RULINGS.md:152]. That was Prima's proposal in t188s728. This plan's C16 proposed answer (Option A, f8ac4d9) was already that a linked general page stays editable and a link may reach changed words, which is what R32 rules; this plan's Option C was the version-pinning one.
- Item 2: labelled C15 (what is a system page). Neither Matthew's words nor the Read [DIRECTOR-RULINGS.md:153] [DIRECTOR-RULINGS.md:154] define a system page. The summary presents C15 as answered; only the lock part is. The summary also leaves out his first sentence, that at creation a page "gets its properties is assigned a title and seqaddr" [DIRECTOR-RULINGS.md:153].
- Item 3: matches. The Read adds the reason, "so face 00 doesn't change on every write" [DIRECTOR-RULINGS.md:156].
- "Old versions stay in the log (R29)" is in the Read [DIRECTOR-RULINGS.md:152], not in Matthew's words.

**Places changed because they assumed a link freezes a version (R32, 1), and why:**

- Summary: "Once a system page is linked to, it is done" read as if linking froze the page. Now: a link gives the current page; linking makes a page undeletable (retire only); system pages lock 00-04 under R31, not because a link pins them.
- Step 1, face 00's role: said the face list is derived and not written in face 00. R32, 3 puts the face list in face 00 and the places in the page signpost. Rewritten.
- Step 6, page signpost: now named as Prima's "page index" that holds where each face sits (R32, 3).
- Step 10, Three leads: "cite a version by address plus fingerprint" kept for cites (D348), but marked as a cite, not a link; links carry no fingerprint (R32, 1; C10).
- Step 13: "A system page locks once it is linked to" and "Once a page is linked, it is done" now carry R32's narrowing; the R31, 1 against R31, 3 tension and the "links may reach changed words" tension are marked settled by R32, 1; "live and as linked may differ (C16)" now says a link always follows the current page; the rework copy's lineage fingerprint is marked as a record of where the copy started, not a link; Better and Three leads updated.
- Step 16: tests 28-32 added (a link follows edits; delete refused, retire allowed; retired pages leave search; face 00 refused once done; a link never carries a fingerprint).
- Step 17: "Whether a linked general page is still editable is C16" replaced by R32, 1.
- C11 and C14: C11 now records R32's narrowing; C14 stands for system pages, with C21 asking whether R32, 2 changes it. C10 sharpened: links never pin a version; cites may.
- Still open: the fork note "links to them stay true" now says links give each copy's current page, which is why the fork rule must halt.
- Checked and left as is: Step 12's K2 file generation names the old file by fingerprint; that is a pointer to a frozen old file, not a page link. Test 11 (title mismatch raised) still holds.

**Director ruling R31, t184u (relayed by Prima), 11:47 AM EST** [DIRECTOR-RULINGS.md:127]. Each item is Matthew's reply to Prima's proposed answer (t183s712) [DIRECTOR-RULINGS.md:128]. His words and Prima's Read are quoted exactly from the file.

- **R31, 1:** "I agree, once it's linked it can't be used for anything else it's done. Even if the page is retired. It never is rewritten. OUr design is made so you can point to a new page to keep the chain going or write a new one. Once a address is given a title it exists and doesn't change anymore. it would break too much to allow it to be open" [DIRECTOR-RULINGS.md:129]. Read: "once an address is given a title, that pairing is fixed forever. Once a page is linked, it is done, even if it is later retired. To continue the work, point to a new page or write a new one." [DIRECTOR-RULINGS.md:130]
- **R31, 2:** "See above I think it answers it for you." [DIRECTOR-RULINGS.md:131]. Read: "Prima's answer stands. The title and the finished faces 00-04 freeze, and additions written only by the compute (05, 06, 08, 09) may continue. This also settles R24 against R30." [DIRECTOR-RULINGS.md:132]
- **R31, 3:** "So locked pages are for system pages, a normal page can be edited think our google document page. Our page design is to basically allow us to hold a full office suite inside of it as pages. So we could have pages that are cel based file system, a word file." [DIRECTOR-RULINGS.md:133]. Read: "locking applies to system pages. General pages stay editable in the Google Docs way (R29). Pages may hold office kinds, such as a cell-based sheet or a word document." [DIRECTOR-RULINGS.md:134]
- **R31, 4:** "No that is correct, we update and promote when its time to improve our work. This is dev only ability." [DIRECTOR-RULINGS.md:135]. Read: "a lock is never undone. Improvement happens by updating and promoting a new copy, and only developers can do that." [DIRECTOR-RULINGS.md:136]
- **R31, 5:** "Correct" [DIRECTOR-RULINGS.md:137]. Read: "a rework copy gets a new address, with links both ways." [DIRECTOR-RULINGS.md:138]
- **R31, 6:** "This of a book kind of like a working journal. In time each one is retired and put on a shelf as a refernce but once that piec of work is complete it's done. It could be used in the future or might only sit partly complete." [DIRECTOR-RULINGS.md:139]. Read: "a book is a working journal. When it's done it's retired to the shelf as a reference, and it may stay partly complete." [DIRECTOR-RULINGS.md:140]
- **R31, 7:** "Well yes, but we should have a type type that contains and orders this. With our reader able to open and see what data is there." [DIRECTOR-RULINGS.md:141]. Read: "one folder per page and one file per face, plus a type, written in face 00, that holds and orders the face files. The reader can open a page and show what data is there." [DIRECTOR-RULINGS.md:142]
- **R31, 8:** "Titles do, we keep addresses hidden from users it's back end only." [DIRECTOR-RULINGS.md:143]. Read: "titles stay plain text. Addresses are back end only and never shown to users." [DIRECTOR-RULINGS.md:144]
- **R31, 9:** "I agree, where do we place those short logs?" [DIRECTOR-RULINGS.md:145]. Read: "no log in face 00. Prima's answer (t184s714): a "last change" note in the page index, which only the compute writes. Held 7 until he confirms." [DIRECTOR-RULINGS.md:146]
- **R31, 10:** "I agree" [DIRECTOR-RULINGS.md:147]. Read: "R29's "So they can't be changed" means old versions can't be changed. The R29 hold is closed." [DIRECTOR-RULINGS.md:148]

**Where Prima's relayed summary differs from her R31 entry** (checked line by line; R31 governs):

- Summary: "a face 00 type that holds them". Matthew's words say only "a type type that contains and orders this" [DIRECTOR-RULINGS.md:141]; "written in face 00" is in Prima's Read [DIRECTOR-RULINGS.md:142], not in his words.
- Summary: "titles stay plain text (C13)". Matthew's words are "Titles do" [DIRECTOR-RULINGS.md:143]; "plain text" is the Read [DIRECTOR-RULINGS.md:144]. Neither says ASCII, and neither mentions card keys. So C13 is settled only in part (see C13).
- Summary: "A book is a working journal, retired to the shelf when it is done." R31 also says a book "might only sit partly complete" [DIRECTOR-RULINGS.md:139] [DIRECTOR-RULINGS.md:140]. Left out of the summary.
- Summary leaves out R31, 5: a rework copy gets a new address, with links both ways [DIRECTOR-RULINGS.md:138]; and R31, 4's Read that a lock is never undone [DIRECTOR-RULINGS.md:136].
- Summary: "Locks are for SYSTEM pages" and "A page that is linked to is never rewritten". Both are in R31 ([DIRECTOR-RULINGS.md:133] [DIRECTOR-RULINGS.md:129]), but R31 does not say how they fit together: item 1 is not limited to system pages in his words. Named as a tension (Step 13, C16).
- Summary: "a last-change note in the page index, held at 7". Matches the Read [DIRECTOR-RULINGS.md:146]. Matthew's own words are "I agree, where do we place those short logs?" [DIRECTOR-RULINGS.md:145]: he asked where; Prima's answer (t184s714) is not yet confirmed by him.
- Summary: "faces 00-04 freeze". The Read says "the finished faces 00-04" [DIRECTOR-RULINGS.md:132]. Same meaning as this plan's "seated text"; noted only for exactness.

**Director rulings, t175u (relayed by Prima), 11:24 AM EST:**

- **t175u, 1: "yes change R3"** [DIRECTOR-RULINGS.md:105]. With t171u answer 2: "Yes we can keep small files then have the ability to export books later." [DIRECTOR-RULINGS.md:104]. Read: small files are the stored form; whole books are an export. **R3 is updated by t175u** (Prima has entered it as R26, [DIRECTOR-RULINGS.md:103] [DIRECTOR-RULINGS.md:106]). R3's own text is not rewritten (axiom 6). C1 is settled by this ruling.
- **t175u, 2: "Update R4."** [DIRECTOR-RULINGS.md:110]. With t171u answer 1: "Our systems design needs to be understandable by our tech documentation But we want it fast for models and compute to work. Hench the multi faced design. So no it doesn't need to be. It can just be code. for every face other then 04." [DIRECTOR-RULINGS.md:109]. Read: faces other than 04 may be true compact code (binary); face 04 stays human-readable. **R4 is updated by t175u** (Prima has entered it as R27, [DIRECTOR-RULINGS.md:108] [DIRECTOR-RULINGS.md:111]). C3 is settled by this ruling. Whether addresses, titles and card keys stay ASCII is not in his words; this plan keeps them ASCII and lists it as a detail to confirm (C13).
- **t175u, 3:** "Once a book is complete, changing pages shouldn't be possible anymore. A new copy can be made and reworked. But the original work shouldn't changed. Once a page is linked to and registered with the book it shouldn't change." [DIRECTOR-RULINGS.md:124]. Read: a page that is registered and linked to, or in a completed book, is locked; changes go into a new copy; links never break (Step 13). Prima's entry holds 7 how this fits face 04 edits [DIRECTOR-RULINGS.md:125].

**Director answers (relayed by Prima), recorded by Prima, still partly held 7:**

- **t171u, answer 3:** "agreed 09 is log, we keep a short log in 00 if you think that is a superiour design." [DIRECTOR-RULINGS.md:114]. Face 09 is the page log (Prima's R28). The short log in 00 is held 7 until Matthew sees this plan's answer [DIRECTOR-RULINGS.md:115]; this plan's answer is no (Step 8). R31, 9 agrees: no log in face 00 [DIRECTOR-RULINGS.md:146]; where the short log goes is held 7.
- **t171u, answer 4:** "A user should be able to modify and change their documents in 04." [DIRECTOR-RULINGS.md:118]. **t172u:** "go with Google's approach." [DIRECTOR-RULINGS.md:119]. Face 04 edits are small changes plus full copies now and then (Prima's R29, Step 17). "So they can't be changed" was held 7 [DIRECTOR-RULINGS.md:120]; R31, 10 closes it: old versions can't be changed [DIRECTOR-RULINGS.md:148] (C9 closed).
- **t171u, answer 5:** "We use the seqaddr system. our 2.2.2.4.title we don't include the face its a sub group of the page." [DIRECTOR-RULINGS.md:123]. Links name a page address plus title, never a face (Prima's R30, Step 13). R31, 3 appears to answer R30's hold (how the lock fits face 04 edits) [DIRECTOR-RULINGS.md:134]; Prima has not marked R30's hold closed, so this plan does not either.

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

- Until 16 Nov 2026 the book was the real stored copy, and a `.seq` file a view of one page, exported from a book and imported back [R3] [DIRECTOR-RULINGS.md:12] [seqpage.md:11] [seqpage.md:13]. **R3 is updated by t175u**: small files are stored, whole books are an export [DIRECTOR-RULINGS.md:105] [DIRECTOR-RULINGS.md:106].
- A book is one file [format.md:21]. Book files are named like `10.11.21.book` [format.md:25].
- A book is an append-only log of approved writes. Nothing is edited in place. The current state comes from replaying every entry in order [format.md:60] [format.md:61].
- Each entry is one JSON line [format.md:70]. Line 1 is the header: format name, version and book address [format.md:79]. An example header in the repo is `{"seqbook":1,"address":"10.11.21"}` (books/10.11.21.book line 1).
- A `snapshot` entry lets replay start late; older entries stay [format.md:88] [format.md:105]. Working path D414, not a ruling: a snapshot is never trusted over the log and is checked on every open [DESIGN.md:165].
- One compute owns every book; only it writes to disk [format.md:15] [format.md:18]. It runs one queue with one writer and appends with fsync [BUILD-LOG:53]. A cut-off last line is dropped on load [BUILD-LOG:54]. A cut-off multi-op proposal is dropped whole [BUILD-LOG:38].
- Stored files were printable ASCII 0x20-0x7E plus newline [R4] [DIRECTOR-RULINGS.md:16]. **R4 is updated by t175u**: face 04 stays readable; other faces may be compact code [DIRECTOR-RULINGS.md:110] [DIRECTOR-RULINGS.md:111].
- Face 00 is the registry: the stamp, the page type and the per-type registry [R10] [R12] [R19] [DIRECTOR-RULINGS.md:41] [DIRECTOR-RULINGS.md:76].
- Face 09 is unassigned in the spec [decisions.md:182] [review.md:53] [seqAddr.md:158].
- The kernel keeps its sources as small files, one Markdown file per face (for example `kernel/00.00.00/00.00.00.0051.01.draft.md`), and builds them into the kernel book; seats are pinned to the git blob of those files [R23-R25-lineage.md:94].
- Size today: the four book files in `books/` hold 71 lines and about 233 KB in total (measured with `wc` on 16 Nov 2026). The kernel book is the largest, about 205 KB in 51 lines.

---

## Step 1. Names and levels: a folder per page, a file per face; books are working journals; whole books exported

Matthew's idea, 16 Nov 2026: "A book is a .seq file." A book holds pages. A page is a small multi-dimensional book broken into pieces, one piece (a *face*) for each lead. Face 00 is the page's registry face. It says what kind of page it is.

**Settled by Director ruling, t175u, 1 (relayed by Prima): "yes change R3"** [DIRECTOR-RULINGS.md:105], with t171u, answer 2: "Yes we can keep small files then have the ability to export books later." [DIRECTOR-RULINGS.md:104]. **R3 is updated by t175u** (Prima's entry R26 [DIRECTOR-RULINGS.md:106]); R3's own text is not rewritten. So there are two forms:

- **The stored form: small files.** This is the real copy, the one the compute writes.
- **The export: one whole-book `.seq` file.** It is made from the small files when someone wants the book as one file. It is read back only through the normal proposal queue, as page views are today [DIRECTOR-RULINGS.md:12] [seqpage.md:14].

The levels match the existing design: books contain pages, pages contain faces, faces contain cards [AGENTS.md:41]. A page is one object with several faces, each a view for a different reader [format.md:12] [seqAddr.md:7]. The "one face for each lead" idea has a footing in the face table: face 01 is for agents (the model) [seqAddr.md:150], face 03 for the compute [seqAddr.md:152], face 04 for users (the person) [seqAddr.md:153].

**Which small files: settled by R31, 7 (C1a).** Matthew: "Well yes, but we should have a type type that contains and orders this. With our reader able to open and see what data is there." [DIRECTOR-RULINGS.md:141]. Prima's Read: "one folder per page and one file per face, plus a type, written in face 00, that holds and orders the face files. The reader can open a page and show what data is there." [DIRECTOR-RULINGS.md:142]. So the stored form is option S3, the plan's lean and Tester's pick: one folder per page, one file per face (and per counter) inside it. The other options are kept only as the record of what was weighed: S1 one log file per book, as today [format.md:25]; S2 one file per page. The kernel already keeps its sources one file per face, for example `kernel/00.00.00/00.00.00.0051.01.draft.md`, and seats are pinned to the git blob of those files [R23-R25-lineage.md:94]. The old reasons against "a folder of files per page", "No single file to export" and "'Rename is a claim' only works on one disk" [format.md:50], are answered by the export (R26) and by the compute's queue [format.md:41] [format.md:42].

**What a page folder holds (plan, new, not a ruling).** One file per face that exists: compact code files for faces other than 04 (R27), face 04 as plain text with its small-change log and full copies (Step 17), and face 09 as the page's log file (Step 8). Which faces exist on a page comes from its type (below). A write that touches several files or pages still needs to be all or nothing; Tester's pick is a compute-only book journal, like the compute's `.queue` file (`crates/compute/src/store.rs:307`). R31, 7 does not mention it, so it stays open (Still open).

**Face 00's role: the type and the face list; the page signpost holds the places (R31, 7; settled by R32, 3, was C17).** Face 00 already holds the stamp, the page's type and a per-type registry [R19] [DIRECTOR-RULINGS.md:76], and the starting types include `system` and `general` [decisions.md:286]. A type can carry rules such as required or forbidden faces and who may write it [decisions.md:288]. R32, 3: Matthew: "I agree" [DIRECTOR-RULINGS.md:155]; Read: "face 00 holds the page type and its face list. Where each face sits is kept in the page index, so face 00 doesn't change on every write." [DIRECTOR-RULINGS.md:156]. So (plan detail, new, not a ruling): face 00's face list names which faces the page has, in the order the reader shows them (for example 00, 01, 02, 04, 05, 06, 08, 09). It names faces, not files: a new 05 counter, a new 04 full copy or a new 09 line is a new file or line inside a listed face and does not touch face 00. Prima's "page index" is this plan's page signpost (Step 6): it holds where each face's current file and pieces sit, and it changes on every write. R25's churn worry [DIRECTOR-RULINGS.md:101] is met. The face list is an open field (R36, below), so a page that later needs a new face adds it as a logged step.

**Face 00: locked fields and open fields (R36; closes C22).** Matthew: "Ok so on face 00 think of it like windows registry. We have fields that nevere change and lock, like it's address, it's title, it's page type. Others could change. We can have a split on this." [DIRECTOR-RULINGS.md:189]. Read: face 00 is split into locked fields, "set once and never change", and open fields that "may change, so R25's records on 00 can continue" [DIRECTOR-RULINGS.md:190]. "Once the 00 is done it's locked" (R32) now applies to the locked fields [DIRECTOR-RULINGS.md:190].

Proposed split of the fields that already exist (none invented; sources: the stamp [face00.md:59]-[face00.md:65], the common registry [face00.md:170]-[face00.md:171], per-type fields [face00.md:198]-[face00.md:210], page 0000 [face00.md:236]-[face00.md:238], override pages [face00.md:248]-[face00.md:252], and R25's seat records [DIRECTOR-RULINGS.md:101]). Beyond address, title and type, every placement is a proposal, put to Matthew in C28:

- **Locked (set at creation, never changed):** `address`, `title`, `type` (named by Matthew); `level` (worked out from the address); `parent` (page 0000's back-link to the pointer that names its container); pointer `kind`; workflow and band `role`; and, on a book's identity page only, the birth id this plan adds in Step 10 (plan detail, not a spec field).
- **Open (may change, each change a logged step):** `state`, `why-draft`, `faces` (the face list and each face's state, which is where R25's seat records sit), `why-NN`, `axioms`, `lineage`; per-type `owner`, `repo`, `set`, `approval`, `default-type`, `lead`, `index`, `layout`; the compute-only `contents` and `continues`; and the override fields `changes`, `why-here`, `why-needed`, `achieves`, `authorized-by`.

**How an open field changes without breaking axiom 6** (plan, new where not cited). Only the compute writes face 00. For each change it (1) writes face 00's fingerprint as it is now onto the 00 counter, as R25 says [DIRECTOR-RULINGS.md:101]; (2) writes the new face 00; (3) appends a face 09 line naming the field, the old value and the new value. The old face 00 is never edited in place; each change is a new step after the last [Axioms.md:23], and every old value stays findable through face 09 and the 00 counter. A write that touches a locked field is refused.

**Face 00 stays small and rarely rewritten (R25).** R25 wants face 00 not to churn; its own past is kept on the 00 counter, "not lines inside 00" [DIRECTOR-RULINGS.md:101]. So open fields hold only the current value, never a list of past values, and they change only on events: a page is seated or retired, a face is added, a type rule changes a per-type field. Ordinary writes (a new 04 change, a 05 counter, a 09 line) never touch face 00: where each face sits stays in the page signpost [DIRECTOR-RULINGS.md:156]. Face 09 stays the page log (R29, R31 [DIRECTOR-RULINGS.md:146] [DIRECTOR-RULINGS.md:148]); an open field is a current value, not a log.

**A new face** is an open-field change: the compute adds it to `faces` (for example a face 03 menu added under R35, 2 [DIRECTOR-RULINGS.md:180]). **A wrong locked field** (a mistyped title, the wrong type) cannot be fixed in place; the work continues on a new page that links back (R31, 5 [DIRECTOR-RULINGS.md:138]).

**Tension (named, not resolved): system pages.** R34, 1 freezes a system page's faces 00-04 once linked [DIRECTOR-RULINGS.md:170], and R31, 2 lets only compute additions to 05, 06, 08 and 09 continue [DIRECTOR-RULINGS.md:132]. R36 says open fields may change. Whether a linked system page's open fields (for example `state` when it is retired) may still change is C29.

**A book is a working journal (R31, 6).** Matthew: "This of a book kind of like a working journal. In time each one is retired and put on a shelf as a refernce but once that piec of work is complete it's done. It could be used in the future or might only sit partly complete." [DIRECTOR-RULINGS.md:139]. Read: "a book is a working journal. When it's done it's retired to the shelf as a reference, and it may stay partly complete." [DIRECTOR-RULINGS.md:140]. What this means for the file: a book is opened, written to for a piece of work, then retired. Retiring is a new step (a face 09 line on the book's identity page, written by the compute), never a rewrite [Axioms.md:23]; the files stay where they are and stay readable. "Retired" already exists as a tail word for pages [seqAddr.md:127]. **Open, not resolved here:** R30 says that once a book is complete, changing its pages "shouldn't be possible anymore" [DIRECTOR-RULINGS.md:124]; R31, 6 says a retired book may be only partly complete. Whether retiring a book locks all its pages, or only its system pages, and what marks a book "complete" or "retired", are C20. "Put on a shelf" may be a figure of speech or may mean a shelf address (DD.SS) [seqAddr.md:14]; the sources do not say.

**Names.** R3 called the `.seq` file a one-page view [DIRECTOR-RULINGS.md:12]. Matthew now calls the exported whole book a `.seq` file. Under S3 (R31, 7) each page folder and face file needs a name pattern built from its address. These names are back end only: Matthew said "we keep addresses hidden from users it's back end only" [DIRECTOR-RULINGS.md:143], so the reader shows titles, not file names. Either way the one-page view needs either a new name or a clear note that `.seq` now has two shapes (one page, or a whole book). This is part of C1.

**Axioms:** Fits axiom 2: the same shape at every scale; a page is "a small book", and the export is the same book in one file [Axioms.md:15]. Fits axiom 3: one face per lead [Axioms.md:17]. Fits axiom 8: the export is a copy, and "a copy ... never becomes what it points to" [Axioms.md:27]; the small files govern. R3 is changed by Matthew's own ruling (t175u), not by the builders [Axioms.md:13].

**Better:** Better than making the big file the stored copy: small files are quick to write, each change touches only the file it changes, and git shows exactly which piece changed. The export still gives Matthew his "self-contained database file" when he wants one. Where we fall short: a page of six or so files costs more disk than its bytes (Tester measured 3 to 7 times, SEQ-PROTO-RESULTS.md); which face 00 fields beyond address, title and type are locked is open (C28); and what retires or completes a book is open (C20).

**Three leads:** The person needs one title per thing and a reader that opens a page and shows what data is there [DIRECTOR-RULINGS.md:142], never raw addresses or file names; in face 00 they see which fields are fixed and which may still change. The model needs to write only proposals, never an export and never a small file directly [AGENTS.md:42]. The compute needs one stored form it alone writes [format.md:18], and an export it can build from it on request.

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

## Step 3. Face 04 plain text; other faces compact code (R4 updated by t175u)

**What R4 said.** Stored files use printable ASCII 0x20-0x7E plus newline; any other byte is rejected on write, and a book holding one is damaged on read [DIRECTOR-RULINGS.md:16]. Matthew's words were "We want a simple storage design for now" [DIRECTOR-RULINGS.md:15].

**R4 is updated by t175u.** Director ruling, t175u, 2 (relayed by Prima): "Update R4." [DIRECTOR-RULINGS.md:110], building on t171u, answer 1: "... It can just be code. for every face other then 04." [DIRECTOR-RULINGS.md:109]. Prima's entry (R27) reads: face 04 stays plain readable text; every other face may be stored as compact computer code (binary), for model and compute speed [DIRECTOR-RULINGS.md:111]. R4's own text is not rewritten (axiom 6). C3 is settled.

**What this plan now does.** Face 04 stays plain text (printable ASCII plus newline, as R4 said). Faces other than 04 may be true compact code: raw bytes, in a strict format the core defines. The brief's "must be checkable by a person" [AGENTS.md:10] is met through face 04 and through a decoded view (below).

**Titles and addresses: settled in part by R31, 8 (C13).** Matthew: "Titles do, we keep addresses hidden from users it's back end only." [DIRECTOR-RULINGS.md:143]. Read: "titles stay plain text. Addresses are back end only and never shown to users." [DIRECTOR-RULINGS.md:144]. So titles stay plain text, and addresses are never shown to users. Not said: whether "plain text" means ASCII, and nothing about card keys. This plan keeps addresses, titles and card keys plain ASCII, because the grammar only allows lowercase letters, digits and hyphens [seqAddr.md:112] [seqAddr.md:280] [seqAddr.md:281], file names are built from addresses, R30 links carry the title and must match byte for byte, and working path D432 says the same [DECISIONS-LOG:560]. That leftover is C13a, a lesser detail. Inside a code face, a card key is still stored as its plain ASCII key, so a card can be found by key without decoding the whole face.

**Office kinds (R31, 3).** Matthew: "Our page design is to basically allow us to hold a full office suite inside of it as pages. So we could have pages that are cel based file system, a word file." [DIRECTOR-RULINGS.md:133]. Read: "Pages may hold office kinds, such as a cell-based sheet or a word document." [DIRECTOR-RULINGS.md:134]. What this plan does: each office kind is a page type (face 00 type, [decisions.md:286]), so its rules (which faces, who writes) are kernel cards like any type [decisions.md:287] [decisions.md:288]. The person-facing content of a sheet or word document lives in face 04 and follows Step 17. **Tension, not resolved here:** R27 says face 04 "stays plain readable text" [DIRECTOR-RULINGS.md:111]. A cell-based sheet can be held as plain text (rows of cells), but a word document with layout, or a sheet with formulas, may not fit plain text well. Whether office kinds keep face 04 plain text, or hold their content in a code face with face 04 as a readable view, is C18.

**Why small files make binary safe.** Under the stored small files (Step 1), each code face is its own file. Raw bytes in one file cannot break the lines of another file. So face 04 files and the face 09 log stay line-based text, and only code face files are binary. In a whole-book export, code faces are written with their length and fingerprint before the bytes, so the reader never looks for a newline inside them (new, not in any source; see Step 11).

**The why must stay readable.** Every 01 or 02 card already needs a 04 card with a `why:` line and a body [seqAddr.md:175] [seqAddr.md:184]. So even with 01 and 02 as code, the person reads every why in face 04.

**Before binary faces are trusted.** Working path D432 lists hostile trials before any widening, starting with a crash cut inside a character [DECISIONS-LOG:560], and a new format version so old readers refuse cleanly. The same is needed here: a crash cut at every byte of a code face, a version bump, and a decoder that refuses anything it does not know (Step 16).

**Options considered (C3 settled by t175u):** T1 all plain text (R4 as first written) is replaced. T1c compact plain text for non-04 faces stays allowed, for faces where text is easier. T2 binary for non-04 faces is now allowed. T3 SQLite stays set aside: it would make face 04 binary too [format.md:54].

**Axioms:** Fits axiom 1: this follows Matthew's ruling and does not go beyond it; where his words are silent (grammar), it asks [Axioms.md:13]. Fits axiom 4: the why is recorded: readable for the person in 04, fast for models and compute elsewhere [Axioms.md:19]. Fits axiom 7: the grammar detail is not guessed into a ruling [Axioms.md:25].

**Better:** Better than all plain text for speed and size on faces people do not read directly. Better than all binary because the person's face and every why stay readable. Tester measured that plain text costs little for finding a spot by offset; binary mainly speeds up the full read and full check (SEQ-FILE-PLAN-TEST.md section a). Where we fall short: a person cannot read a code face without a tool, so the decoded view becomes something people must trust; and binary needs new crash tests that do not exist yet.

**Three leads:** The person needs face 04, with every why, to stay plain text they can read in any editor, and a decoded view of any other face. The model needs code faces turned into text before it drafts; face 01 is meant to be "model-efficient" [seqAddr.md:150], and Tester advises keeping 01 as text (SEQ-FILE-PLAN-TEST.md, Step 3). The compute needs one strict decoder per code face kind, and to refuse any face 04 byte outside printable ASCII.

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

A signpost line is a book-level entry written only by the compute, like a `snapshot` [format.md:88]. Book-level entries belong to no page and stay in the book on export [seqpage.md:206]. So the `.seq` page view does not change. R3's round-trip rule [DIRECTOR-RULINGS.md:12] still stands after R26: R26 changes which copy is stored, not the rule that an export and its import must be lossless [DIRECTOR-RULINGS.md:106]; the round trip is now small files to export to small files.

Example (new, for illustration only):

```
{"n":42,"at":"2026-11-16T16:30:00Z","by":"compute","op":"signpost","addr":"10.11.21","level":"book","chain":"sha256:...","prev":20480,"bands":[["00",18800,412,"fp:..."],["10",22010,388,"fp:..."]]}
```

**Tester fix 2 (signpost growth), folded in from SEQ-FILE-PLAN-TEST.md:** a book or band signpost line holds **only the rows that changed**, plus `prev`, the offset of the signpost line before it. **Defined by Tester's test 2 (working path, not a ruling): each band gets its own full signpost line every K = 64 of its own writes**, and the book signpost gets a full line every 64 book writes. K is written in the header, so a reader knows the bound. Tester's simulation (20,000 writes; a full line on every write is about 20 KB) gave, quoted from SEQ-FILE-PLAN-TEST-2.md section 2: "64 | bands touched | 8,331" bytes per write with 71 worst reads; "64 | each band, own count | 1,075" bytes per write with 129 worst reads; K = 16 for all 100 bands cost 63,883 bytes per write; K = 256 per band cost 832 bytes with 490 worst reads. "Worst case reads: K book lines back, plus up to K band lines, plus page signpost and face. About 2K + 3." "Warm cache, 129 reads is about 1.3 ms. Cold disk not measured." So per band, K = 64: about 1.1 KB of signposts per write, worst case about 129 short reads. Tester measured that full lines on a full book would add about 20 KB per write and about 200 MB per 10,000 writes; changed-rows-only lines remove that (SEQ-FILE-PLAN-TEST.md section b). K = 64 is a builder setting, recorded with its why [AGENTS.md:45]; it can change with a version bump.

**Tester fix 1 (the open check), folded in, defined by test 2:** every signpost line carries a **chain**: chain = hash(previous chain + the new bytes since the previous signpost line) (`chain` in the example). So any signpost can be checked from the one before it, and the chain covers every byte of the file. See Step 10.

A signpost is derived from the entries. It is never written by a person or a model, and never proposed. Boards, contents lists and path lists are already "derived from the log and never written as entries" [format.md:102]. The signpost is the same kind of thing, written down only so the compute can find it fast. Whether writing a derived line into the book is allowed at all is the same question as for snapshots (QD46, working path D414); this plan names it, and does not close it.

**Axioms:** Fits axiom 6: new signposts are added after the old ones; nothing earlier is touched [Axioms.md:23]. Fits axiom 8: the signpost is a pointer; the entries govern [Axioms.md:27]. Fits axiom 1 if only the compute writes signposts [Axioms.md:13] [format.md:18].

**Better:** Better than a header pointer: no edit in place. Better than today: opening a book reads two lines, not every line. This is the same trick other single-file formats use to stay append-only (new, not in any source). Where we fall short: every write now adds at least one extra line (a signpost), so the file grows faster. Tidying (Step 12) is the answer, and it is a choice for Matthew.

**Three leads:** The person needs to find the newest signpost by looking at the last lines of the file, with no special tool. The model needs nothing from the signpost directly; it asks the compute by address. The compute needs the signpost to be cheap to write after every proposal, and to be refused if anyone but the compute tries to write one.

---

## Step 6. Band signposts and the page signpost (levels 2 and 3)

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

**Band signpost (level 2).** New (not in any source): one line per band, at most 100 rows. Each row is one page: page number, title, page kind (the `type` from face 00), page state, where that page's newest page signpost sits, its length, and its fingerprint.

The page kind is copied into the row so the compute can route a request (system page, general page, a kind not yet invented) without opening the page. The `type` stays defined in face 00 [decisions.md:285] [R19]. The row is a derived copy for speed, never the source.

**Page signpost (level 3); Prima's "page index" (R32, 3).** It holds where each face sits, so face 00 does not change on every write [DIRECTOR-RULINGS.md:156]. New (not in any source): one line per page, written by the compute after any write to that page. It lists each face the page has: face number, its state (draft, seated, counted, retired), where its current block sits, its length, and its fingerprint. For a counted face it lists each counter and its tail. It also points to the page signpost before it (`prev`), so the page's past can be walked back (Step 8).

**Why not put this inside face 00.** Prima's sketch put "where each face sits" in face 00. This plan keeps it out, for a reason Matthew already gave. In R25 he said the 00 counter list "must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint" [DIRECTOR-RULINGS.md:101]. The same is true here. If face 00 held face locations, face 00 would change every time any face changed. Face 00 would then have no stable fingerprint, and every write would look like a change to the registry.

What face 00 keeps is what the rulings give it: the stamp, the type, and the per-type registry [R19] [DIRECTOR-RULINGS.md:76]. The face00.md draft already proposes that the compute writes the `faces:` list and nobody writes it by hand [face00.md:179], because a contents list is derived, never hand-written [face00.md:177]. Working path D326 went further: nobody writes a `faces:` list into face 00 at all; the computer works it out [DECISIONS-LOG:386]. R32, 3 puts the face list in face 00 [DIRECTOR-RULINGS.md:156], and R36 makes it an open field [DIRECTOR-RULINGS.md:190], so this plan now has the compute write `faces:` (as face00.md proposes) and change it only when a face is added or changes state; face positions stay here, so face 00 does not churn. Which wins on a mismatch is still `7` there (F2). In the `.seq` page view, the registry section can still show `faces :=` as a derived line, as it does today [seqpage.md:84]. So a person reading face 00 still sees "what kind of page, and which faces", which is what Matthew described. Only the byte positions live in the page signpost.

A kind not invented yet: a `type` not in the kernel's list is a finding, not an error, and the page is still read [face00.md:146]. The band signpost copies the unknown type exactly as written. It never guesses a nearer type.

**Axioms:** Fits axiom 7: an unknown kind stays unknown and is shown as written [Axioms.md:25]. Fits axiom 8: the band signpost's copy of `type` is a pointer; face 00 governs; if they disagree, the compute raises it [Axioms.md:27]. Fits axiom 2: the band signpost and page signpost have the same shape as the book signpost [Axioms.md:15].

**Better:** Better than Prima's sketch: face 00 does not churn, which keeps R25's fingerprint idea workable. Better than today: the compute can tell what kind a page is without replaying the book. Where we fall short: the page kind now appears in two places (face 00 and the band signpost row). That is a copy, and copies can drift [Axioms.md:15]. The plan answers this by making the row derived only and checked against face 00, but the risk is real.

**Three leads:** The person needs face 00 to stay the one place that says what kind of page this is. The model needs to read face 00 and the faces it is given, and never write a band signpost or page signpost. The compute needs the band signpost and page signpost to route requests fast, and to rebuild them from the entries whenever asked.

---

## Step 7. Face blocks, read only on demand (level 4)

Today a face's current text is the entry that wrote it: an ordinary `put` (or `promote`, `merge`, and so on) line [format.md:74] [format.md:86]. Face content is Markdown in `body` [format.md:81]. Cards are its `##` headings [seqAddr.md:168].

New (not in any source): the page signpost points straight at the face's current block. Under A2 that is a small file (or, under S1, a byte offset in the book file); in the export it is a byte offset. The compute reads that one piece and nothing else. A face nobody asks for is never read.

**Updated by A1 (t171u):** face 04 blocks stay Markdown text. Blocks of other faces may be compact code (Step 3), as compact plain text or as raw bytes (R4 updated by t175u, 2). Whatever the form, the card keys inside a block stay plain ASCII [DECISIONS-LOG:560], so a card can still be found by its key.

Block size: no fixed block size. A block is as long as it needs to be. The page signpost gives where it is and how long. A fixed size (padded) would help only a raw-bytes layout; padding is bytes nobody wrote. This is a builder choice, recorded with its why [AGENTS.md:45].

Seated, draft and counted faces work as today. A draft is found by lookup and shows that it is a draft and why [R5] [DIRECTOR-RULINGS.md:20] [DIRECTOR-RULINGS.md:29]. A counted face has counters 01-98 only; faces have no sentinels [R9] [DIRECTOR-RULINGS.md:38]. A new counter is never a silent in-place replace (working path D320, D344 [DECISIONS-LOG:380] [DECISIONS-LOG:407]). The page signpost points at whichever pieces those rules say are current.

**Sections loaded one at a time (R35, 2).** Matthew: "So instead of the model eating everything it only gets what it needs." [DIRECTOR-RULINGS.md:179]. Any page may have a compute-written face 03 menu of its sections [DIRECTOR-RULINGS.md:180]. New (not in any source): the page signpost also records where each `##` section starts inside the face 04 block, and how long it is. The model asks for the page and gets the menu; it then asks for sections by key, and the compute reads only those byte ranges. The menu is derived (never typed), rebuilt after each write, and is not the real copy [decisions.md:301] [decisions.md:516]. Full design: `docs/design/SECTIONS-AND-CARDS.md`, Part 2. R35, 2 updates the face 03 limit of reserved pages 0001-0099 [decisions.md:404] for the menu card only [DIRECTOR-RULINGS.md:180]; that spec update is pending, and this plan does not edit decisions.md. Adding a menu to an existing page adds face 03 to face 00's open `faces` field, a logged step (R36 [DIRECTOR-RULINGS.md:190]; Step 1).

**General queries get menus, not data (R35 note).** Matthew: "instead of handing the model all the data in those pages it hands it the menu. So the model can decide what it should request first." [DIRECTOR-RULINGS.md:185]. Read: the compute "finds the pages holding the key word and hands the model their face 03 menus, not their data" [DIRECTOR-RULINGS.md:186]. So (plan): a query on a key word goes to the compute; it finds the pages whose 01 cards carry that key word (a derived brand-to-pages list, SECTIONS-AND-CARDS.md Q9; not in any source); it returns each page's menu with its address plus title; the model picks what to ask for first; the compute then reads only those sections through the page signpost. This answers "one very large face is still read whole" for face 04; other large faces are still read whole.

**Axioms:** Fits axiom 6: blocks are never edited; a change is a new block [Axioms.md:23]. Fits axiom 5 in spirit: the model is handed only the framed piece it needs, and on a general query it chooses its own first step from the menus [Axioms.md:21].

**Better:** Better than today: today the whole book is replayed to serve one face [format.md:61]. Better than one big file being rewritten: each piece is its own block. Where we fall short: a very large face other than 04 is still read whole; section offsets in the signpost are one more thing to rebuild and check; and a code face must be decoded before a person or model can read it.

**Three leads:** The person needs face 04 to look the same as today: Markdown with `##` cards. The model needs exactly the face (or card) it asked for, as text, with its address and source [AGENTS.md:44]; on a long page it reads the face 03 menu first and asks only for the sections it needs (R35, 2); on a general query it gets the menus of the pages holding the key word, not their data, and decides what to request first (R35 note). The compute needs one lookup and one read per face or section, plus a decoder for code faces; it writes the menu, keeps the key-word-to-pages list, and answers a general query with menus only.

---

## Step 8. Face 09 is the page's log; no short log in face 00

**Director answer, t171u (relayed by Prima), recorded by Prima as R28; the short-log part is held 7 until Matthew sees this plan's answer [DIRECTOR-RULINGS.md:115] (A3):** "agreed 09 is log, we keep a short log in 00 if you think that is a superiour design."

**Where face 09 stood.** Face 09 was unassigned: "01-09 system faces (01-08 defined, 07 reserved, 09 unassigned)" [decisions.md:182]; the review list says the same [review.md:53]; the face table says "reserved, unassigned" [seqAddr.md:158]. Retiring is done with the tail word `retired` [seqAddr.md:127] [seqAddr.md:138]. (The brief says an older ".09 retired" tail existed and is gone; no source line still uses it, so that history is not verified here.) A3 gives face 09 its job. A3 is now entered by Prima as R28 [DIRECTOR-RULINGS.md:113]. The spec's face table still says "unassigned" [seqAddr.md:158], and the core still refuses writes to face 09: it allows only faces 00-06 and 08 (`crates/seqaddr-core/src/face.rs:72`; the refusal is at `crates/seqaddr-core/src/validate.rs:232-233`). Changing them is build work, listed as an open gap; this plan does not edit them.

**What the face 09 log holds (plan, new).** One line per approved write to the page: entry number, time, who, operation, address, proposal, and the reason where there is one. It is written only by the compute. Nobody proposes to face 09. Writing face 09 never creates another face 09 line, so the log does not log itself (the same trap R25 avoids for face 00 [DIRECTOR-RULINGS.md:101]).

**How it fits A2 (small files).** Under S3, now settled by R31, 7, face 09 is the page's own log file, the one record of that page's history; the compute appends one line per write. Under S1, the book file is still the log [format.md:61], and face 09 is the page's list of pointers into it. Either way there is one source, not two. In the export, face 09 sits at level 5 of the pyramid, reached from the page signpost. In the one-page `.seq` view, face 09 takes the place of today's derived `~ history` section, which already lists "the page's line of writes across all faces" and "only grows" [seqpage.md:199].

**Other logs, kept apart.** BUILD-LOG is the repo's record of build choices [BUILD-LOG:3]; it is not a page. Face 06 holds model notes, one counter per session [seqAddr.md:155]; notes say why and what was found, while face 09 says what happened. Face 09 does not replace R25's 00 counter (00.CC), which keeps face 00's fingerprints [DIRECTOR-RULINGS.md:101]; QD66 and QD67 stay open.

**Should face 00 keep a short log too? No.** In plain words:

1. Face 00 should stay small and change rarely. R25 says face 00 is the registry root, its past is kept as a list of its fingerprints, and that list "must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint" [DIRECTOR-RULINGS.md:101]. A short log inside 00 would change face 00 on every write to any face. Each of those changes would then need its own 00 counter entry. That is the cascade R25 was written to avoid.
2. It would be a copy. The short log would repeat what face 09 already holds. Two copies can drift apart, and "agreement is not connection" [Axioms.md:27]. Axiom 2 says do not copy [Axioms.md:15].
3. It would not be faster. What a reader wants from "a short log in 00" is the latest change, fast. The compute can keep a derived **last change** pointer outside face 00 (in the page signpost, Step 6). It is one hop, the same as reading face 00. In the `.seq` view it can be shown as a worked-out line in the registry section, like `faces :=` today [seqpage.md:84]. It is never stored in face 00 and never imported.

So: face 09 holds the log. Face 00 holds no log. R36's open fields do not change this: an open field holds one current value (for example `faces: 01 seated`), and its past lives in face 09 and the 00 counter, not in face 00. The compute keeps a "last change" pointer outside face 00. This agrees with Prima's lean.

**R31, 9.** Matthew: "I agree, where do we place those short logs?" [DIRECTOR-RULINGS.md:145]. Read: "no log in face 00. Prima's answer (t184s714): a "last change" note in the page index, which only the compute writes. Held 7 until he confirms." [DIRECTOR-RULINGS.md:146]. Prima's "page index" is what this plan calls the page signpost (renamed because "index" is the dictionary's word [seqAddr.md:230]). So the plan's answer above is Prima's answer. It stays held 7 until Matthew confirms.

**Still open (C2):** should face 09 also record attempts that were refused or halted? Today a refused proposal writes nothing ("Rejected = reasons, nothing written") [BUILD-LOG:53]. Under S2 or S3, face 09 is a stored file, so it could hold them; under S1 it could not without a new kind of book entry. Only Matthew can say whether he wants them logged.

**Copy-check steps (R35, 1).** The copy check now elevates: compute by its code, then the model, then a person if the model is not highly certain [DIRECTOR-RULINGS.md:178]. New (not in any source), from SECTIONS-AND-CARDS.md Part 4 and Q8: each refusal and each elevation step gets a face 09 line (who decided: compute, model or person; the rule; the reason). Tension (named, not resolved): C2 proposes that plain refusals are not logged. Both cannot stand as written; Matthew's answer to Q8 or C2 decides. While a case is elevated, the write waits as a draft (R5 [DIRECTOR-RULINGS.md:29]).

**Disagreement halts.** If face 09, the page signpost or the "last change" pointer ever disagrees with the pieces it describes, the compute does not pick one. It halts and raises it, following working path D324, "neither silently wins; halt and raise it (axiom 1)" [DECISIONS-LOG:384], and working path D367, which halts on a fingerprint mismatch [DECISIONS-LOG:440].

**Axioms:** Fits axiom 6: the log only grows; the line back is kept with the page [Axioms.md:23]. Fits axiom 8 and axiom 2: one log, no copy in face 00; the pointer points and the source governs [Axioms.md:27] [Axioms.md:15]. Fits axiom 1: only the compute writes the log, A3 is Matthew's answer, and a disagreement is raised, not chosen [Axioms.md:13].

**Better:** Better than today's derived `~ history` section, because the page's past is reachable in a few reads without a full replay. Better than a short log in face 00, because face 00 stays small and stable (R25) and nothing is copied, with the same speed. Where we fall short: whether refused or halted attempts belong in the log is undecided, and the face table in the spec still says 09 is unassigned until A3 is numbered.

**Three leads:** The person needs one place to see what happened to this page, in time order, in plain words. The model needs to read that log before drafting, so it builds on the real past and not on memory [drafting.md:7]. The compute needs to append the log once per write, keep the "last change" pointer outside face 00, and halt if anything disagrees.

---

## Step 9. Appending a change and writing new signposts

**Updated by A2 (t171u):** this level belongs to the exported whole-book `.seq` file. The same rows may also serve as the compute's derived signpost over the stored small files (Step 2). It is never the stored copy.

New (not in any source), building on what exists: one approved proposal is written in this order, all at the end of the file.

0. Hold the OS file lock on the stored folder; check the file's length and last chain against the copy held in memory; if anything changed outside the compute, refuse and raise (Step 11). Refuse all writes until the start-up check has ended (Step 10).
1. The proposal's entries, as today: one or more JSON lines, all or nothing [format.md:100] [BUILD-LOG:38].
2. A new page signpost line for each page the proposal touched.
3. A new band signpost line for each band the proposal touched, holding only the changed rows (a full line every 64 of that band's own writes).
4. One new book signpost line, changed rows only (full every 64 book writes), carrying the chain: hash(previous chain + the new bytes).
5. One fsync, as today [BUILD-LOG:53].

**Under small files (R31, 7), the write order (working path, Tester, not a ruling).** The prototype wrote: "memory. Write order: face piece, 09 line, page, band, book." [SEQ-PROTO-RESULTS.md:27]. With Tester's fixes:

0. Hold the OS lock; check each file's length and last chain against memory (Step 11).
1. The face piece, in its face file, fsynced. Its length and fingerprint are known.
2. The face 09 line that books it (naming the piece, its length and fingerprint), fsynced.
3. Face 04 only: the current-view file, written **after** the 09 line (fix 3, [SEQ-PROTO-RESULTS.md:134] [SEQ-PROTO-RESULTS.md:135]; Step 17).
4. The page signpost, then the band line, then the book line. **The book line is the commit point** (fix 2, [SEQ-PROTO-RESULTS.md:130]): a write is booked when its book line is down and fsynced.

Nothing earlier in the file is changed. Old blocks and old page, band and book signposts all stay. This is Prima's sketch ("changes appended at the end and a new signpost written, with old blocks kept"), with the two extra levels.

The cost of one write is the entries plus three small derived lines (one page signpost, one band signpost of at most 100 rows, one book signpost of at most 100 rows).

A reseat follows the existing rules: the R24 climb uses a new counter, built from the seat plus the changes [DIRECTOR-RULINGS.md:97]; the newer seated pack carries a write-once `supersedes:` naming the older one (working path D321, D345 [DECISIONS-LOG:381] [DECISIONS-LOG:408]). The signposts only point at the result; they decide nothing.

Two copies of a book changed apart are never merged by mixing lines (working path D427 [DECISIONS-LOG:550] [DESIGN.md:167]). The signposts help here without deciding QD57: two copies whose book signposts have the same fingerprint are the same state, and where they differ, comparing band signposts shows which bands changed (new, not in any source).

**Axioms:** Fits axiom 6: "add the new step after it" [Axioms.md:23]. Fits axiom 1: only the compute appends, one proposal at a time, through the queue; only the compute writes to disk [Axioms.md:13] [format.md:18]. Fits axiom 8: every new signpost points at real entries [Axioms.md:27].

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

**Two hashes, kept apart (fixes the C7 mismatch Tester found).** The plan said the fingerprint is the git blob (C7), while its example signpost says `"chain":"sha256:..."`; Tester notes the mismatch and used "SHA-256 of the bytes" [SEQ-PROTO-RESULTS.md:149] [SEQ-PROTO-RESULTS.md:150]. They are two different things (working path, building on Tester; new, not a ruling):

- **The chain hash** is always SHA-256 over raw bytes: chain = SHA-256(previous chain + new bytes). This is what the `sha256:` in the example means. It is not a choice.
- **The file fingerprint** of a stored face file is its git blob id, so a person can check it with git [AGENTS.md:10]. Which form of git blob (SHA-1, git's default, or git's SHA-256 form) stays the lesser choice C7.

**When to check (Tester fix 1, folded in).** Working path D414 says a snapshot is never trusted over the log, is checked on every open, and only the compute takes one [DESIGN.md:165] [DECISIONS-LOG:524]. Signposts are the same kind of thing. Per-line fingerprints alone cannot prove that nothing was cut out between lines; a running chain hash can (SEQ-FILE-PLAN-TEST.md section c). So, new (not in any source):

- Every signpost line carries a chain: chain = hash(previous chain + the new bytes since the previous signpost line). Defined by Tester's test 2 (SEQ-FILE-PLAN-TEST-2.md section 1).
- "Open" means compute start, once per process, not every request. Today the compute already reads every book at start and serves from memory (`crates/compute/src/store.rs:1009-1023`).
- At start the compute checks the chain in one pass over the file, runs the R4 byte check on face 04 text (and the strict decoder check on code faces) in the same pass, and then replays the entries to rebuild the signposts and compare them. A forged signpost with a right-looking chain but wrong rows passes the chain check; only the replay-compare catches it (SEQ-FILE-PLAN-TEST-2.md section 1). Tester measured replay at 1.3 s for 183 MB (release build).
- **Until that check ends, every read is marked `9`, and every write is refused.** Why `9`, not `7`: `7` "marks what is not complete", a hole [Axioms.md:25]; `9` "marks what has not yet faced its trial: do not trust it as it stands" [Axioms.md:29]. An answer read before the check is not missing; it is there but not yet checked, so `9` fits. Earlier versions of this plan said `7` (following Prima's wording); this corrects it, as Tester suggested (SEQ-FILE-PLAN-TEST-2.md, "What the revision fixed").
- **Time order (approved by R33, 3).** Matthew: "I agree" [DIRECTOR-RULINGS.md:163]; Read: "Refuse a line dated earlier than the line above it." [DIRECTOR-RULINGS.md:164]. So every log line and signpost line carries its time from the system clock, and the compute refuses a line dated earlier than the line above it, at write and at the start-up check. In the small-file layout this applies within each chained file (each page's face 09 log, the signpost log, the book journal). Tester found nothing refused this today (OUR-CODE-VS-CURSOR-LESSONS.md, L3).
- The compute keeps the last chain and the file length in memory. Before each write it checks the file against that memory copy, not against the file's own last line (a rewritten file would carry its own good last line) (SEQ-FILE-PLAN-TEST-2.md section 3).
- If a crash cut the last signpost, its `prev` is lost with it. The compute scans back for the signpost before (at most one proposal back), then replays after it.
- Any mismatch halts and is raised; neither side silently wins (working path D324 [DECISIONS-LOG:384]; D367 [DECISIONS-LOG:440]). A full replay can then rebuild the signposts, with the person's approval.
- The chain has no secret. Anyone who rewrites the file can write new, matching chains. So it catches damage and accidents, not a forger; the OS file lock and the memory check (Step 11) are what stop other writers.
- Under small files (S3), a per-file fingerprint does not show a whole file that was deleted. So the page's face 09 log lists each piece with its fingerprint, and the face 09 log has its own chain.

**The chain across many small files (R31, 7; new, building on Tester; not a ruling).** Tester: "Chain: defined for one file. With small files there are many files. I chained signposts.log and each 09.log apart. A chain over the whole book is not defined." [SEQ-PROTO-RESULTS.md:146] [SEQ-PROTO-RESULTS.md:147] [SEQ-PROTO-RESULTS.md:148]. Defined here:

1. **Book birth id.** When a book is made, the compute writes a random 128-bit birth id once, in the stamp on face 00 of the book's identity page (page 0000 holds only face 00 [DIRECTOR-RULINGS.md:41]). It is written once and never changes, so it adds no face 00 churn (R25). It is back end only (R31, 8).
2. **Page chain.** Each page's face 09 log starts from seed = SHA-256("page" + birth id + page address) (fix 4, [SEQ-PROTO-RESULTS.md:137] [SEQ-PROTO-RESULTS.md:138]). Each 09 line: chain = SHA-256(previous chain + line bytes). Each 09 line names the face piece it books, with its length and fingerprint, so every face file is covered by its page's chain.
3. **Book chain.** The signpost log (band and book lines) starts from seed = SHA-256("book" + birth id + book address). Each band row carries its page's latest 09 chain head; each book line carries the chain of each band line it points to. So the last book line covers every page's 09 head, and through them every face file.
4. **Book journal** (writes across pages, Still open) is chained the same way, from its own seed.

What this catches: a page folder copied to a new page number (Tester saw "ACCEPTED as page 0950. No file inside a page names its address." [SEQ-PROTO-RESULTS.md:111]) now fails its seed and halts; a book copied to a new address fails too. What it does not catch: a byte-exact copy of a whole book at the same address. Tester: "Copy the whole book, write to both: both boot fine. Nothing tells them apart." [SEQ-PROTO-RESULTS.md:108] [SEQ-PROTO-RESULTS.md:109]. The two copies are told apart only once both reach the same compute, where the fork rule halts (Still open, forks).

**All signposts missing is a halt (fix 4).** Tester emptied the signposts after a forge, and the result was "ACCEPTED": boot rebuilt every signpost and reported 250 quiet crash findings [SEQ-PROTO-RESULTS.md:103] [SEQ-PROTO-RESULTS.md:104]. So: if every signpost (all band and book lines and every page signpost) is missing, the compute halts and asks a person; it does not quietly rebuild [SEQ-PROTO-RESULTS.md:139]. A missing tail after a crash is still repaired at start-up, as before.

This keeps D414 ("checked on every open", "never trusted over the log") [DECISIONS-LOG:524], and still serves the top fast, marked `9` until checked. Tester measured one hash pass at about 0.4 s per 500 MB in Python. For stored small files, the same rule applies per file: each file's fingerprint is checked at start. This touches QD46 and does not close it (C4).

**Axioms:** Fits axiom 8: a pointer whose fingerprint does not match is missing (`7.8`) and is not repaired from memory [Axioms.md:27]. Fits axiom 9: check before trusting [Axioms.md:29]. Fits axiom 1: a mismatch halts and is raised [Axioms.md:13]. Fits axiom 2: one kind of fingerprint (the git blob) where the existing design already uses it [Axioms.md:15].

**Better:** Better than today: today nothing inside a book says "this line is intact" except that it parses. Better than a new kind of fingerprint: under S2 or S3 the git blob is already used for seats. Where we fall short: a fingerprint shows damage; it cannot repair it. And git's default hash is SHA-1, which is old.

**Three leads:** The person needs to check a fingerprint with a common tool (git), not trust the compute blindly [AGENTS.md:10]. The model needs to cite a version by address plus fingerprint, never by commit id, as working path D348 already does for packs [DECISIONS-LOG:411]. That is a cite, which may pin a version; a link never does: a link names address and title and gives the current page (R32, 1 [DIRECTOR-RULINGS.md:152]; C10). The compute needs fingerprints that are cheap on write and on read.

---

## Step 11. Crash safety

What exists: a partly written last line is dropped on load and cut off before the next append [BUILD-LOG:54]; a cut-off multi-op proposal is dropped whole [BUILD-LOG:38]; the compute appends with fsync [BUILD-LOG:53]. Working path D431 (not a ruling) records the hardware as one ordinary computer with a local disk that honours fsync [DECISIONS-LOG:558].

New (not in any source): with the write order in Step 9, a crash can only leave one of these:

- A cut-off entry, or a cut-off page, band or book signpost, at the very end. The existing rule drops it [BUILD-LOG:54].
- Whole entries with no new signpost after them (the crash came before step 4). The compute finds the last good book signpost, then replays only the entries after it, and writes a fresh signpost. Nothing is lost, because the entries are complete and the signposts are derived.
- A signpost whose fingerprints do not match. It is not used; the compute walks back to the signpost before it (`prev`), and raises it.

**The book line is the commit point (fix 2, working path, Tester, not a ruling).** Tester's prototype: "Crash after the band line, before the book line: boot PASSED, but the next read raised a false alarm" [SEQ-PROTO-RESULTS.md:86] [SEQ-PROTO-RESULTS.md:87]; "A crash between band and book lines leaves a stale path that boot does not see." [SEQ-PROTO-RESULTS.md:130] [SEQ-PROTO-RESULTS.md:131]. So a write is booked only when its book line is down. At start-up, any band lines (and page signposts) written after the last book line are an unfinished tail: they are dropped, like a cut-off last line, and the compute rebuilds them from the face 09 lines, which are complete. Dropping happens only in the start-up repair, never at runtime.

**Face 04's current view after its 09 line (fix 3).** Tester: "Crash after 04.md, before the 09 line: boot called it a HAND EDIT and parked the text as 04.pending. A false alarm." [SEQ-PROTO-RESULTS.md:89] [SEQ-PROTO-RESULTS.md:90]. With the order in Step 9, a current view newer than the log can only come from outside the compute; a current view older than the log (crash before the view was written) is rewritten from the log at start-up, not called a hand edit (Step 17).

The worst case is always: ignore every signpost and replay the whole book, exactly as today. So the new layout can never be less safe than today's. The one exception is new: if **every** signpost is missing, the compute halts and asks a person (Step 10), because that is what a forger who re-chains a page and deletes the signposts leaves behind.

**Updated by A1 and A2 (t171u), new:** with small files, each write puts the new piece in a new file (or new lines), fsyncs it, and only then appends the face 09 log line; a piece with no log line is ignored as unfinished. Old pieces are never overwritten. Today's safety leans on whole lines: a cut-off last line is dropped [BUILD-LOG:54]. A raw-bytes face (allowed by t175u, 2) has no lines to lean on, so its log line must carry its length and fingerprint, and a piece that fails either is treated as not written. The one storage failure seen so far was a crash cutting inside an accented letter, and R4 fixed it by refusal, not by repair code [DESIGN.md:173]; working path D432 asks for a hostile crash test before any widening [DECISIONS-LOG:560]. The same is needed before raw-bytes faces.

**Outside writers (Tester fix 3, defined by test 2); plan text only, no code changed.** What the code does today, corrected: in the compute's append (`crates/compute/src/store.rs:917`), a file **shorter** than the compute last wrote is refused as "changed outside the compute" (`store.rs:937-939`); a file **longer** than that has the extra bytes cut as a "partial tail" (`store.rs:940-941`). That cut runs at every append, not only at start-up, and nothing checks that the earlier bytes are unchanged. The first Tester fold-in (c077d0c) said the compute "cuts any bytes past the length it last wrote" without a check; that was right for longer files but missed the refusal for shorter ones. (Prima's brief said "store.rs:941 refuses at runtime and only cuts during boot repair"; the code at HEAD does not do that yet. It is Tester's fix, below.) The compute's write folder is `books/` (`store.rs:59`), and the kernel builder writes its output to the same folder (`kernel/build.mjs:29`, the whole-file write at `kernel/build.mjs:846`). So a rebuild while the compute runs could mix two files, and every signpost offset would point at the wrong bytes.

The fix in this plan (working path from Tester's test 2, not a ruling):

- **Refuse at runtime, cut only at start-up repair.** At runtime, any length change the compute did not make is refused and raised (D324). Cutting a partial tail happens only during the start-up repair, after a crash.
- **Check against memory.** Before each write, the compute checks the file's length and last chain against the copy it holds in memory (Step 10).
- **OS file lock.** The compute holds an operating-system file lock on its stored folder while it runs. Any other tool that would write there, including the builder, refuses to run while the lock is held. Tester's prototype: "Second writer while the compute runs: REFUSED (folder lock)." [SEQ-PROTO-RESULTS.md:114].
- **The lock alone does not close the check-then-write gap (fix 5).** Tester measured it: "Race between check and write: in 2 of 20 tries the compute's line went in after an outside line. The write was reported OK. It was caught only at the next write or boot. The OS lock is advisory: a tool that ignores it is not stopped." [SEQ-PROTO-RESULTS.md:117] [SEQ-PROTO-RESULTS.md:118] [SEQ-PROTO-RESULTS.md:119] [SEQ-PROTO-RESULTS.md:120]. What closes it (new, building on Tester; not a ruling; **not yet measured**):
  1. **Only the compute's own OS account may write the stored folder.** Other tools and people get read-only access. File permissions are enforced by the operating system, unlike the advisory lock, so a tool that ignores the lock still cannot write. This is what closes the gap; the lock stays as a polite signal for tools that cooperate.
  2. **Write at the expected place, then confirm before saying OK.** The compute writes each piece at the byte offset it expects (the length it holds in memory), not "at the end, wherever that is"; after the fsync it re-reads the length and the last chain. Only if both match does it report the write as booked; otherwise it reports "not booked", halts that page and raises it (D324). This turns a silent mix into a refusal at once, instead of at the next write or boot. On its own it narrows the gap but cannot close it (an outside write could land after the re-read), which is why point 1 is needed.
  3. The memory check before each write and the full check at start-up stay as they are.
- **Move the builder's output out of `books/` (approved by R33, 1).** Matthew: "Yes, books change through compute not by models. Models can be wrong and having them answer a question correctly 100% of the time can be an issue." [DIRECTOR-RULINGS.md:159]. Read: "approved. The book builder stops writing into books/ and makes an export instead (R26). Books change only through the compute's gate." [DIRECTOR-RULINGS.md:160]. So the builder writes its exports to their own folder, never the compute's stored folder, and books change only through the compute's gate. Tester is building this in code.
- **Host check (approved by R33, 4).** Read: "approved. Refuse requests that arrive with the wrong Host header." [DIRECTOR-RULINGS.md:166]. This is a check on the compute's server, not on the book files; it closes the read-side gap Tester found (OUR-CODE-VS-CURSOR-LESSONS.md, L6). Noted here because it guards the same stored books.

**Axioms:** Fits axiom 6: recovery only adds; it never rewrites an earlier line [Axioms.md:23]. Fits axiom 7: a damaged signpost is treated as missing, not guessed [Axioms.md:25]. Fits axiom 1: a damaged signpost is raised, not silently replaced [Axioms.md:13].

**Better:** As safe as today, and faster to recover after the common case (a crash after the entries but before the signpost). Better than an edit-in-place signpost, which can be half-written in the middle of the file. Where we fall short: it still needs a disk that honours fsync (D431); Tester's crash tests used kill -9, which "is not a power cut" [SEQ-PROTO-RESULTS.md:82], so power loss is untested. On a disk that lies about fsync, no file layout is safe, and this plan does not fix that.

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

## Step 13. Links give the current page; titles are fixed; face 00's locked fields lock; linked pages only retire; system pages lock; developers promote copies

**Director answer, t171u, answer 5 (relayed by Prima), recorded by Prima as R30:** "We use the seqaddr system. our 2.2.2.4.title we don't include the face its a sub group of the page." [DIRECTOR-RULINGS.md:123]. **Director rulings R32, 1-3 (t191u) and R31, 1-5 (t184u), below.** **Director ruling, t175u, 3 (relayed by Prima):** "Once a book is complete, changing pages shouldn't be possible anymore. A new copy can be made and reworked. But the original work shouldn't changed. Once a page is linked to and registered with the book it shouldn't change." [DIRECTOR-RULINGS.md:124].

**Links name a page, checked against seqAddr.md.** "2.2.2.4" is the four address widths: desk, shelf and book are 2 digits, the page is 4 [seqAddr.md:14] [seqAddr.md:18] [seqAddr.md:19] [seqAddr.md:20] [seqAddr.md:21]. A word after the page is a title, and "Faces never have titles: a face is `PPPP.FF` or `PPPP.FF.NN`" [seqAddr.md:110]. The grammar allows a title right after the page [seqAddr.md:269]. Link targets are already page-level: "Every target's identity page links back" [seqAddr.md:251]. So a link reads like `10.11.21.1001.bob`. Points from seqAddr.md a link must respect:

- A title is a label, not identity: `4442` and `4442.timer` are the same page [seqAddr.md:114]. The address is what the link follows; the title is a check.
- A title written in an address is checked against the stamp in face 00, and a mismatch is raised to the person [seqAddr.md:116].
- Pages 1000 and up must have a title; pages 0001-0999 may; page 0000 has none [seqAddr.md:115]. A link to an untitled page is the address alone. A link to a whole book uses its address or identity page, for example `21.0000` [seqAddr.md:89].
- Face numbers stay legal in addresses [seqAddr.md:271] [seqAddr.md:111]; links just do not use them. Whether cites may still name a face or counter is C10.

**Titles are fixed for every page (R31, 1).** Matthew: "Once a address is given a title it exists and doesn't change anymore. it would break too much to allow it to be open" [DIRECTOR-RULINGS.md:129]. Read: "once an address is given a title, that pairing is fixed forever." [DIRECTOR-RULINGS.md:130]. This holds for every page, system or general: an address, once given its title, never gets another title, and the address is never reused, even after the page is retired ("Even if the page is retired. It never is rewritten." [DIRECTOR-RULINGS.md:129]). seqAddr.md already says a title is a label and the address is identity [seqAddr.md:114]; R31, 1 adds that the label, once given to an address, is permanent for that address. **Titles are not unique (R34, 3).** Matthew: "So we don't lock words in books. if you look at workflow you already know that titles can be reused." [DIRECTOR-RULINGS.md:173]. Read: "Titles may be reused, as the existing workflow already allows. Note: R31 item 1 fixes the address-title pairing, not the title alone." [DIRECTOR-RULINGS.md:174]. seqAddr.md already says "several pages may share a title" [seqAddr.md:114], and the workflow makes sets of pages in different bands with matching titles, such as `0423.timer` and `0523.timer` [seqAddr.md:243]. So the same title may sit at many addresses; **the address is what tells them apart.** Pages 0001-0999 may have no title [seqAddr.md:115]; giving one later is the one time a title is set.

**A link gives the current page, not a version (R32, 1; settled, was C16).** Matthew: "So say page 1024 is about "Jim" That might be changed and updated. We don't want to link to exact wordings of a page face. But be linked so the compute can find out about Jim." [DIRECTOR-RULINGS.md:151]. Read: "A link points to the page (address plus title), and following it gives the current page. Old versions stay in the log (R29)." [DIRECTOR-RULINGS.md:152]. So a link stores the target's address and title, nothing else: no fingerprint, no version number, no face. Following it always opens the page as it is now. Anyone who needs an old wording reads the page's face 09 log and face 04 history (Step 17). **This narrows R30 and R31, 1** (Prima's Read, [DIRECTOR-RULINGS.md:152]): what is fixed forever is the address-title pairing and the page's existence, not the wording of a general page's faces. R30's and R31's text is not rewritten [Axioms.md:23].

**Face 00's locked fields lock once done (R32, 2, narrowed by R36); a linked page can only be retired (settled, was C15 in part).** Matthew: "Yes, when a page is created, it gets its properties is assigned a title and seqaddr. Once the 00 is done it's locked the info might change on the faces but once a page exists and is linked it can only be retired, so the record is there, and not be in active searches." [DIRECTOR-RULINGS.md:153]. Read: "at creation a page gets its properties, title, and address. Once face 00 is done, face 00 is locked; the other faces may still change. Once a page exists and is linked, it can't be deleted, only retired. A retired page stays on record but leaves active searches." [DIRECTOR-RULINGS.md:154]. So, for every page:

- At creation the page gets its type and properties, its title and its address.
- Once face 00 is done, its locked fields are locked; its open fields may still change, each change a logged step (R36 [DIRECTOR-RULINGS.md:190]; Step 1). Locked fields are set at creation (R32, 2 [DIRECTOR-RULINGS.md:154]); which fields are locked beyond address, title and type is C28.
- Once the page is linked to, it can never be deleted, only retired. Retiring is a face 09 line and the tail word `retired` [seqAddr.md:127]; the page and all its history stay; it leaves active searches. Its address is never reused and never gets another title (R31, 1 [DIRECTOR-RULINGS.md:129]). Its title is not reserved: another page at another address may use it (R34, 3 [DIRECTOR-RULINGS.md:174]). Whether an address lookup stops at a retired page or falls through to the shelf is C25.

**System pages lock faces 00-04 (R31, 3), and what is still open.** Matthew (R31, 3): "So locked pages are for system pages, a normal page can be edited think our google document page." [DIRECTOR-RULINGS.md:133]. Read: "locking applies to system pages. General pages stay editable in the Google Docs way (R29)." [DIRECTOR-RULINGS.md:134]. Under R31, a system page's title and faces 00-04 freeze once it is linked. R32 narrows only what a link fixes and "the wording of a general page's faces" [DIRECTOR-RULINGS.md:152]; it does not mention system pages. R34, 1 settles that it does not: system pages freeze 00-04 once linked [DIRECTOR-RULINGS.md:170] (was C21). What a system page is remains undefined in R31 and R32; this plan keeps the candidate reading, face 00 type `system`, "a kernel or structural page" [face00.md:138] [decisions.md:286], with the lock as a rule of that type [decisions.md:288] (new, not a ruling; C27). `general` is "an ordinary page; the default" [face00.md:137].

- A **general page**: face 00's locked fields lock once done, its open fields stay changeable through the compute (R36); faces 01-09 stay editable, every version kept (Step 17, R29); links to it always give the current page.
- A **system page**: as a general page, and once linked its title and faces 00-04 also freeze, with compute-only additions (R31, 2), confirmed by R34, 1: "system pages freeze once linked (faces 00-04). They are back end, built for control, and not for users to access." [DIRECTOR-RULINGS.md:170]. A link to it also gives the current page, which for frozen faces is the same words.

**What a lock freezes: settled by R31, 2 (was C14).** Matthew: "See above I think it answers it for you." [DIRECTOR-RULINGS.md:131]. Read: "Prima's answer stands. The title and the finished faces 00-04 freeze, and additions written only by the compute (05, 06, 08, 09) may continue. This also settles R24 against R30." [DIRECTOR-RULINGS.md:132]. So on a locked page: frozen are the title and the finished text of faces 00, 01, 02, 03 and 04. Still added, **only by the compute**, never changing anything written: new face 05 counters (the R24 climb [DIRECTOR-RULINGS.md:97]), face 06 notes [seqAddr.md:155], back-link lines on face 08, and log lines on face 09. The R24 against R30 clash named in 6dbe53c is settled by this. R34, 1 confirms it for system pages [DIRECTOR-RULINGS.md:170].

**No undo; developers promote a new copy (R31, 4 and 5).** Matthew: "No that is correct, we update and promote when its time to improve our work. This is dev only ability." [DIRECTOR-RULINGS.md:135]. Read: "a lock is never undone. Improvement happens by updating and promoting a new copy, and only developers can do that." [DIRECTOR-RULINGS.md:136]. And R31, 5: "Correct" [DIRECTOR-RULINGS.md:137]; Read: "a rework copy gets a new address, with links both ways." [DIRECTOR-RULINGS.md:138]. So:

1. A lock is never undone.
2. To improve a locked page, a developer makes a new copy at a new address, works on it, and promotes it. Its face 08 links back to the original, and the compute adds the matching back-link to the original's face 08 (an addition allowed by R31, 2), so the line is written both ways [seqAddr.md:251] [Axioms.md:23]. The copy's face 00 lineage names the original by address, title and fingerprint (working path, Tester). That fingerprint is a record of where the copy started (history, axiom 6), not a link: it pins nothing, and the face 08 links both ways carry address and title only (R32, 1). Old links still reach the original, and give its current page.
3. Locking and promoting are face 09 lines, written by the compute: who, when, why.
4. Promotion is still a proposal the compute writes; only the compute writes to disk [format.md:18].

Not said, and not resolved here: who is a "developer". The sources have a `dev` band role (N4, "the design") [workflow-loop.003.md:38] [face00.md:214], and authority is granted, not taken [Axioms.md:13]; during this build a face may be seated without the Director's review only after a hostile trial [DIRECTOR-RULINGS.md:9]. Whether "dev only" means people in a developer role, the dev band, or builders with Matthew's approval, is C19.

**Titles may repeat: how links and lookups stay safe (R34, 3; new detail, not a ruling).**

- **A link** stores the target's address and title (R30, R32 [DIRECTOR-RULINGS.md:152]). The compute follows the **address**; the title is only a check against the target's face 00 [seqAddr.md:116]. Because one address has one title forever (R31, 1), the check never fails on a healthy page, and another page with the same title can never capture the link.
- **An address lookup** walks book, shelf, desk, kernel; the first match wins [seqAddr.md:101] [seqAddr.md:104]. It is by page number, not by title, so repeated titles do not affect it. What a retired page does to this walk is C25.
- **A title search** (a person or model looking for "timer") may find several pages. The compute never picks one silently: it returns every live match, each with its book's title, its kind and its last change, and the reader shows that context, never the address (R31, 8). If one must be chosen, the person or model chooses (C26). A link is never made from a title alone; it is made from the chosen page's address.
- **A retired page** drops out of title search and does not reserve its title (R34, 3 [DIRECTOR-RULINGS.md:174]); a new page elsewhere may use it. Links to the retired page still open it by its address, marked retired (R32, 2 [DIRECTOR-RULINGS.md:154]).

**The rename rule (rebuilt on R31, 1).**

1. **No page is ever renamed.** The compute refuses any title change on any page that has a title, locked or not, and says why (R31, 1).
2. **A new title means a new page.** For a general page, the person makes a new page with the new title and links it to the old one; the old page keeps its title. The new title may be one other pages already use (R34, 3). For a locked system page, this is the developer's new copy above.
3. **A link whose title does not match** the target's face 00 is raised to the person, never followed silently and never fixed by guessing [seqAddr.md:116]. Under rules 1-2 this happens only through damage or a write outside the compute.

**Tensions from R31, and what R32 did to them.**

- **R31, 1 against R31, 3: settled by R32, 1.** "It's done" means the address-title pairing and the page's existence are done; a general page's wording stays editable [DIRECTOR-RULINGS.md:152].
- **Editable general pages against links: settled by R32, 1.** A link reaching changed words is what Matthew wants: "We don't want to link to exact wordings of a page face." [DIRECTOR-RULINGS.md:151].
- **Against Tester's C11 pick.** Tester picked "seated AND linked" so nobody could freeze someone else's draft by linking to it (SEQ-FILE-PLAN-TEST-2.md, C11). Under R32 a link to a general page freezes no wording; it only makes the page undeletable. For system pages R34, 1 confirms the freeze once linked [DIRECTOR-RULINGS.md:170], so the draft-freezing risk Tester named remains for them.
- **Against R30's book rule.** R30: once a book is complete, its pages should not change [DIRECTOR-RULINGS.md:124]. R31, 3 and R32, 1 keep general pages editable. Open in C20.
- **Addresses hidden (R31, 8) against links that name an address.** The person picks a title; the stored link carries the address. Titles repeat (R34, 3), so same-titled pages must be told apart without showing addresses. C13a, C26.
- **Developer-only promotion against granted authority.** C19.

**New tensions from R32 (named, not resolved).**

- **Face 00 locked (R32, 2) against R25: settled by R36.** Locked fields never change; R25's records continue in the open fields [DIRECTOR-RULINGS.md:190]. The face list is an open field, so a new face can be added.
- **Open fields (R36) against the system-page freeze of 00-04 (R34, 1).** C29.
- **R32, 2's "the info might change on the faces" against R31, 2's system-page freeze of 00-04: settled by R34, 1** [DIRECTOR-RULINGS.md:170].
- **Retired pages leave active searches against address fall-through.** An address lookup walks book, shelf, desk, kernel; the first match wins [seqAddr.md:101] [seqAddr.md:104]. If a retired book page dropped out of that walk, a lookup of its address would quietly reach the shelf's page with the same number. R34 frees the retired page's title, not its address. C25.
- **"Not for user to access" (R34, 1) against "checkable by a person"** [AGENTS.md:10]. If users cannot open system pages, a person cannot check the rules that govern their pages. C27.
- **Links follow the current page against axiom 8's "a copy never becomes what it points to"** [Axioms.md:27]: no tension found; a link is a pointer, and the current page is the source.

**Across books and files.** A book points to another book by address, never by byte offset or file position; offsets belong to one file and change if it is tidied or exported again (Step 12). Addresses are "ranked so it is stable to store" [Axioms.md:23]. Finding still looks up book, then shelf, then desk, then kernel; the first match wins [seqAddr.md:101] [seqAddr.md:104]. Books follow the kernel live [decisions.md:128]. Links live on face 08 and need a back-link [seqAddr.md:157] [seqAddr.md:251]. A link always follows the current page (R32, 1). For a locked system page the frozen faces read the same as when the link was made; for a general page they may not, and that is intended. Old wordings are in the log. A borrowed face is shown from its source, at most as a derived line (working path D403 [DESIGN.md:189]); copying the parent is what axiom 2 forbids [Axioms.md:15].

**Axioms:** Fits axiom 6: the original is never rewritten; rework is a new copy, a new step after it, linked back [Axioms.md:23]. Fits axiom 8: links are written both ways and name their target page; a mismatch is raised [Axioms.md:27]. Fits axiom 1: the lock, its scope and developer-only promotion are Matthew's rulings (R31); the compute enforces them and refuses, it does not choose [Axioms.md:13]. Fits axiom 7: what a system page is, which face 00 fields lock, how retired pages leave search, and who a developer is are not invented; they are asked (C27, C28, C25, C26, C19); titles may repeat, so a link follows the address and the title is only a check (R34, 3) [Axioms.md:25]. Fits axiom 6: retire, never delete; the record stays (R32, 2) [Axioms.md:23].

**Better:** Better than letting titles change under links, which breaks them, and better than links to faces, which break when a page reorganises. Better than fixing links after a rename, because nothing has to be fixed. Better than locking every page, which would stop people working in their documents (R29). Better than links that pin a version, which would leave every link pointing at stale words about "Jim" (R32, 1). Where we fall short: until "system page", the locked face 00 fields and "developer" are defined, the compute cannot enforce the locks (C27, C28, C19); with repeated titles a person must be shown context to pick the right page (C26); a reader who needs the words as they were when a link was made must open the page's history; and a new copy means two pages about the same thing, so readers must be shown which is newer (the back-links do that, but only if people follow them).

**Three leads:** The person needs to see titles only, follow a link to the page as it is now, retire (never delete) a linked page, and keep editing general pages freely. The model needs to read the current page through a link, read the log when it needs an old wording, propose edits only where faces are unlocked, never a rename, and leave rework of locked pages to a developer's new copy. The compute needs to store links as address plus title only, refuse any change to a locked face 00 field, write each open-field change as a new step (00 counter, then face 09), refuse deleting a linked page, keep retired pages out of active searches, refuse changes to frozen faces on locked system pages, and write a copy's links both ways.

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
- Under S3 (one file per face, settled by R31, 7; S2 kept for the record): each book is split into small files, one entry history per piece, copied byte for byte. The old book file is kept, frozen, as history, and the new files name it by fingerprint. R3 is already changed by t175u (R26 [DIRECTOR-RULINGS.md:106]); which small files is C1a.

Before any move, two things must be true: the round trip book to `.seq` to book still gives back the same entries [DIRECTOR-RULINGS.md:12] [seqpage.md:208]; and the kernel builder's output moves out of `books/` into its own export folder (Tester fix 3, Step 11) (approved by R33, 1 [DIRECTOR-RULINGS.md:160]), or the kernel's history keeps being lost [R23-R25-lineage.md:94] (the whole-file write is now at `kernel/build.mjs:846`; the lineage note cites `build.mjs:818`, which has since moved). Neither is done. This plan does not do them; they are build work after Matthew approves.

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
12. Face 00 must not change when only other faces change (no log in face 00); it changes only when an open field's value changes (R36).

Added from Tester's stress test (SEQ-FILE-PLAN-TEST.md, Step 16):

13. A rebuild of a book file while the compute runs must be refused at the next append (prefix hash).
14. A line cut out of the middle of a file must be caught by the chain hash at start.
15. A fork with the same address must be told apart, or raised.
16. A hand edit to face 04 outside the compute must be found and taken in as a new step, never halted forever.

**Measured by Tester's throwaway prototype (SEQ-PROTO-RESULTS.md, commit 7697815; working path, Tester, not a ruling).** "Code: /workspace/seq-proto (not in the repo). 316 lines of Rust." [SEQ-PROTO-RESULTS.md:5]. Quoted exactly [SEQ-PROTO-RESULTS.md:37]-[SEQ-PROTO-RESULTS.md:76]:

```
Book sizes used:

| book | writes  | pages | files  | real size | on disk |
|------|---------|-------|--------|-----------|---------|
| 1k   | 1,000   | 250   | 1,502  | 1.1 MB    | 7.2 MB  |
| 10k  | 10,000  | 2,500 | 15,002 | 11 MB     | 72 MB   |
| 100k | 100,000 | 9,000 | 54,173 | 89 MB     | 284 MB  |

Boot (full chain check, every file read), seconds:

| book | warm (3 runs)       | cold (3 runs)       |
|------|---------------------|---------------------|
| 1k   | 0.015, 0.014, 0.012 | 0.077, 0.066, 0.137 |
| 10k  | 0.182, 0.130, 0.149 | 0.637, 0.619, 0.592 |
| 100k | 1.046, 1.058, 1.007 | 2.455, 2.483, 2.452 |

One lookup (book -> band -> page -> face), microseconds:

| book | warm p50/p99 | cold first 200 | cold single x40 | reads |
|      | (20,000)     | p50 / p99      | p50 / max       | max   |
|------|--------------|----------------|-----------------|-------|
| 1k   | 21 / 36      | 92 / 329       | 325 / 468       | 24    |
| 10k  | 31 / 63      | 100 / 573      | 622 / 5,071     | 82    |
| 100k | 49 / 90      | 215 / 1,047    | 251 / 641       | 99    |

- "Cold single": caches dropped before each one lookup.
- Most reads seen: 99. The plan's bound is 2K + 3 = 131. Holds.

Append (one face write plus log and signposts), microseconds:

| book | no fsync p50/p99 | fsync p50/p99 | after cold boot |
|      | (3,000 writes)   | (300 writes)  | no fsync p50/p99|
|------|------------------|---------------|-----------------|
| 1k   | 55 / 108         | 422 / 818     | 54 / 94         |
| 10k  | 61 / 163         | 449 / 3,055   | 65 / 102        |
| 100k | 74 / 154         | 479 / 2,081   | 80 / 150        |

- A cold append does not exist here: the boot check reads every
  file first, so the first append is already warm.
- Signposts cost about 380 bytes per write (38 MB per 100k).
```

Machine and method, quoted exactly [SEQ-PROTO-RESULTS.md:31]-[SEQ-PROTO-RESULTS.md:35]:

```
Machine: 8 vCPU "Intel Xeon Processor" (virtual machine).
Disk: virtio /dev/vdb, ext4, 128 GB; disk type not known.
Cold = guest page cache dropped (sync; drop_caches, with sudo).
The host may still cache; that cannot be seen from inside.
Release build. Times are best of a few runs, or p50/p99 as named.
```

Most reads seen, 99, against this plan's bound of 2K + 3 = 131: "Holds." [SEQ-PROTO-RESULTS.md:63]. Tester's summary: "1. Speed is fine. 100k writes, 9,000 pages: lookup 49 us warm, under 1.1 ms cold (p99); append 74 us, or 479 us with fsync; boot 1.0 s warm, 2.5 s cold." [SEQ-PROTO-RESULTS.md:127] [SEQ-PROTO-RESULTS.md:128] [SEQ-PROTO-RESULTS.md:129].

**Not measured (Tester's list, quoted exactly)** [SEQ-PROTO-RESULTS.md:162]-[SEQ-PROTO-RESULTS.md:169]:

```
- Power loss. kill -9 is not a power cut; fsync order is not
  tested by it.
- Real cold disk: the host's cache could not be dropped.
- Disk type: virtio reports "rotational", which says nothing.
- Books over 100k writes or 10,000 pages.
- Many readers at once; the export file; git blob hashing.
```

Also not measured: the race fix in Step 11, the full-copy cadence in Step 17, locks, exports, links and C11-C14, which the prototype did not build [SEQ-PROTO-RESULTS.md:160].

Added from Tester's prototype (to run on the real build):

22. Crash between the band line and the book line: start-up must drop the band lines after the last book line, and the next read must raise no false alarm.
23. Crash after a face 04 09 line but before the current view: start-up must rewrite the view from the log, not call it a hand edit.
24. Copy a page folder to a new page number, and a whole book to a new address: both must halt (seed mismatch).
25. Re-chain a page and empty every signpost: must halt and ask a person, not rebuild quietly.
26. Repeat Tester's race test (20 tries, outside writer appending during writes) with the folder writable only by the compute's account and the confirm-before-OK step: 0 writes may be reported OK on a touched file.
27. Power loss (not kill -9) during writes, on the real disk.

Added from R32:

28. Link to a general page, then edit its face 04: following the link must give the new text; the old text must be readable from the log.
29. Delete a linked page: refused. Retire it: allowed, logged in face 09, and the page still opens by address.
30. A retired page must not appear in title search; a new page at another address may take its title (R34, 3); a link to the retired page must still open it by address, marked retired; and an address lookup must follow the C25 answer.
33. Two live pages with the same title at different addresses: a link to each must reach its own page; a title search must list both with their book and kind, never pick one silently (C26); a link whose stored title does not match its target's face 00 must still be raised.
31. Change a locked face 00 field (address, title, type, and any C28 adds) at any time after creation: refused (R32, 2; R36). Change an open field (for example `state`, or add a face to `faces`): accepted, written by the compute only, with face 00's old fingerprint on the 00 counter first and a face 09 line naming the old and new value; the old value must be findable afterwards.
32. A stored link must hold only address and title: a link carrying a fingerprint or version is refused (R32, 1).

Added from R36:

34. Add face 03 (a menu) to a page whose face 00 is done: accepted as an open-field change; a hand edit to `faces` is refused.
35. Write a 04 change, a 05 counter and a 09 line: face 00's fingerprint must stay the same.
36. On a linked system page, change an open field: must follow the C29 answer.

Added from Tester's stress test 2:

17. A file rewritten with its own matching chains must still be refused at the next write (memory check), and its signposts caught by the start-up replay-compare.
18. A write sent before the start-up check ends must be refused; reads in that window must show `9`.
19. A second process writing the stored folder while the compute holds its OS lock must be refused.
20. On a locked page, a title change and a face 01 change must be refused; a new 05 counter, a 06 note, an 08 back-link and a 09 log line written by the compute must be accepted (R31, 2). A title change on an unlocked general page must be refused too (R31, 1).
21. With K = 64 per band, no lookup may take more than 2K + 3 reads.

**Axioms:** Fits axiom 9: a hostile pass from another view before promotion [Axioms.md:29]. Fits axiom 1: Matthew approves. R2's build-stage approval lets a face be seated after a trial [DIRECTOR-RULINGS.md:9]; it does not speak of changing the file format, so this plan reads that change as Matthew's to approve [Axioms.md:13].

**Better:** Better than building first and testing after. Where we fall short: these tests are a list, not code; none of them exist yet.

**Three leads:** The person needs the trial results in plain words before deciding. The model (as Tester, a fresh session per R20) needs the plan and the sources, read-only. The compute needs the tests to run on real book files, not only on samples.

---

## Step 17. Face 04 edits: small changes plus a full copy every so often

**Director answer, t172u (relayed by Prima), 16 Nov 2026, 11:17 AM EST; recorded by Prima as R29 [DIRECTOR-RULINGS.md:119], with t171u, answer 4: "A user should be able to modify and change their documents in 04." [DIRECTOR-RULINGS.md:118].** Matthew said: "go with Google's approach." This is built in here as his answer, not as a choice.

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
- Face 04 stays printable ASCII: R4 [DIRECTOR-RULINGS.md:16], as updated by t175u, keeps face 04 plain readable text [DIRECTOR-RULINGS.md:111]. A small change is written as plain text lines.
- Where it is stored under small files (working path, Tester's test 2 section 5, not a ruling): under S3, the page's folder holds face 04's change files and full copies, all plain text, written only by the compute.
- A face 04 full copy is a snapshot of the face. So D414's rule applies: the change log is the source; a full copy is checked against it and never wins; a mismatch halts (D324) [DECISIONS-LOG:524] [DECISIONS-LOG:384].

New (not in any source), for the builders: how often a full copy is stored (for example every so many changes, or when the run of changes grows past a size) is a builder setting, recorded with its why [AGENTS.md:45]. The face 04 full copy is not a book `snapshot` entry, but it is checked by the same rule (above); working path D414 [DESIGN.md:165] is followed, not changed or closed. Whether the same "small changes plus full copy" way should later apply to other faces is not decided here; Matthew's answer was about face 04.

**"So they can't be changed": closed by R31, 10 (was C9).** Matthew: "I agree" [DIRECTOR-RULINGS.md:147]. Read: "R29's "So they can't be changed" means old versions can't be changed. The R29 hold is closed." [DIRECTOR-RULINGS.md:148]. A stored small change or full copy is never edited; a correction is a new change after it [Axioms.md:23].

**The files and the write order (working path, Tester, plus new detail; not a ruling).** Tester's prototype kept face 04 as three files: "04.chg: a log of small changes (replace lines a..b)." [SEQ-PROTO-RESULTS.md:13], "04.snap: a full copy every 16 changes." [SEQ-PROTO-RESULTS.md:14], and "04.md: the current view, for people to read." [SEQ-PROTO-RESULTS.md:15]. This plan takes that shape:

- **The change log** (Tester's `04.chg`): append-only, written only by the compute.
- **Full copies** (Tester's `04.snap`): append-only, each with its fingerprint.
- **The current view** (Tester's `04.md`): plain text, the latest version, for people to read in any editor. It is derived: rebuilt from the last full copy plus the changes after it. Written only by the compute, and always **after** the face 09 line that books the change (Step 9, fix 3). The 09 line carries the fingerprint the view must have. At start-up and before a read, the compute compares the view's fingerprint with the one the last 09 line names. Tester flagged the view file as "not in the plan" and its write order as "not defined" [SEQ-PROTO-RESULTS.md:151] [SEQ-PROTO-RESULTS.md:152]; this defines both.

**The small-change format (new, building on Tester; not a ruling).** Tester used "a line range" [SEQ-PROTO-RESULTS.md:154]: "replace lines a..b" [SEQ-PROTO-RESULTS.md:13]. This plan takes that as the format for plain text: one change says "in the version with fingerprint F, replace lines a to b with these lines" (an insert is an empty range; a delete has no new lines). Naming the base fingerprint means a change can never be applied to the wrong version. It is plain text, so it survives the R3 round trip to the page view [DIRECTOR-RULINGS.md:12]. Office kinds (a sheet's cells) may need a cell-based change instead (C18).

**How often a full copy is taken (new, building on Tester; not a ruling).** Tester used "a builder setting; I used 16" [SEQ-PROTO-RESULTS.md:155]: a full copy every 16 changes [SEQ-PROTO-RESULTS.md:14]. This plan uses 16 as the starting builder setting, plus a full copy whenever a system page locks and when a developer's new copy starts, so each of those starts from one clean text. Reading the current view is then at most one full copy plus 15 changes. The effect of 16 against other values on rebuild time was **not measured**.

**How a hand edit is booked, and who made it (new, building on Tester; not a ruling).** Tester: "Hand edit to 04.md: found at boot, and at read time. The logged version stays live; the edit is kept as 04.pending (a draft). Not booked: who made it is unknown." [SEQ-PROTO-RESULTS.md:95] [SEQ-PROTO-RESULTS.md:96] [SEQ-PROTO-RESULTS.md:97]; "Taking in a hand edit: who made it has no source. Parked only." [SEQ-PROTO-RESULTS.md:158]. So:

1. The compute never books a hand edit by itself. The logged version stays live; the edit is kept as a draft (R5), shown in the reader beside the live text.
2. A person who can edit the page opens the reader and either **takes it in** or **discards** it. Taking it in makes a normal proposal in that person's name, through the queue; it is booked as one small change, and its face 09 line says: taken in by that person, typed outside the compute, typist not known. Discarding is a face 09 line too. Nothing is guessed: who typed it stays unknown unless someone says so (axiom 7 [Axioms.md:25]).
3. On a locked system page, taking it in is not allowed; a developer may carry it into a new copy (R31, 4).
4. Until someone acts, the draft stays a draft, never live.

**Squaring face 04 edits with the lock (R31, 3; R32, 1).** General pages: face 04 is edited the Google Docs way for as long as the page lives, every small change kept [DIRECTOR-RULINGS.md:134]. System pages: face 04 is edited the same way until the page is linked to; then it is frozen with faces 00-03 [DIRECTOR-RULINGS.md:132], and improvement is a developer's new copy whose face 04 starts from the original's latest version [DIRECTOR-RULINGS.md:136]. This settles C12. Office kinds (a sheet, a word document) keep the same rule; how their small changes are written down depends on C18. A linked general page stays editable, and links to it give its current version (R32, 1 [DIRECTOR-RULINGS.md:152]).

**Axioms:** Fits axiom 6: every old version is kept, and a change is a new step after the old one [Axioms.md:23]. Fits axiom 1: this is Matthew's answer, recorded as his, not invented by the builders [Axioms.md:13]. Fits axiom 4: the why (the Google Docs against Word comparison) is recorded with the choice [Axioms.md:19]. Fits axiom 7: the phrase was held until Matthew answered it (R31, 10); what office kinds need is asked, not guessed (C18) [Axioms.md:25].

**Better:** Better than storing a whole new face 04 on every edit: much smaller, and the difference between two versions is visible directly. Better than keeping only the latest version, which would lose the past. Where we fall short: rebuilding an old version means applying a run of changes, so a bad change or a bug in applying changes could give a wrong old version; the fingerprint on each full copy is the check against that. Office kinds may need a change format other than lines (C18). The line-range format above is new and untested against real documents.

**Three leads:** The person needs to read the current face 04 as one clean text, and to open any earlier version and see what changed and when. The model needs to propose small changes against the latest version, never a rewrite from memory [drafting.md:7]. The compute needs to store each change and the full copies, rebuild any version on request, check fingerprints, and refuse any attempt to edit a stored version.

---

## Open choices only Matthew can decide

Matthew's standing rule (t189u): every question comes as (1) the question in plain words, (2) a proposed answer, (3) the why, tied to a real reason (an axiom, a link, or who gets hurt), and (4) the Axioms.md lines it was checked against, each marked pass or tension. The top three are marked **TOP**. Proposed answers are this plan's or Tester's working paths, never rulings. Settled choices are listed after the open ones, each with what it now is.

**C28 (TOP). New, from R36. Which face 00 fields are locked, and which are open?**
1. **Question.** You named address, title and page type as locked; others may change [DIRECTOR-RULINGS.md:189]. Face 00 has more fields than these. Which group does each go in?
2. **Proposed answer.** Locked, set at creation: address, title, type, plus `level` (worked out from the address), page 0000's `parent`, a pointer page's `kind`, a workflow or band page's `role`, and a book's birth id (Step 10). Open, changed only by the compute as a logged step: everything else that exists today: `state`, `why-draft`, `faces` (with R25's seat records), `why-NN`, `axioms`, `lineage`, and the other per-type and override fields (full list in Step 1).
3. **Why.** Locked fields are the ones that say what and where the page is; links and lookups rely on them, so changing one would quietly change what every link finds (who gets hurt: every page that links to it). Open fields describe the page's current state and rules, which really do change (a page is seated, retired, or gains a face). `kind` and `role` are locked because they act like the type: a dictionary page that became a contents page would be a different page.
4. **Axioms checked.** Axiom 1 [Axioms.md:13]: pass for the three named; tension for the rest (each placement needs his word). Axiom 6 [Axioms.md:23]: pass (open changes are new steps, old values kept). Axiom 8 [Axioms.md:27]: pass (links rely only on locked fields). Axiom 7 [Axioms.md:25]: pass (unnamed placements are asked, not assumed). Axiom 2 [Axioms.md:15]: tension (`lineage` and `axioms` open means the line back can change; the old line is kept in face 09, but a reader must look there).

**C29. New, from R36 and R34, 1. May a linked system page's open face 00 fields still change?**
1. **Question.** System pages freeze faces 00-04 once linked [DIRECTOR-RULINGS.md:170]; only compute additions to 05, 06, 08 and 09 continue [DIRECTOR-RULINGS.md:132]. R36 says face 00's open fields may change [DIRECTOR-RULINGS.md:190]. On a linked system page, can an open field (for example `state` when it is retired, or a new face) still change?
2. **Proposed answer.** Yes, but only by the compute, and only for `state`, `why-draft` and `faces`; the other open fields freeze with the page. Any real change of rules is a developer's new copy (R31, 4 [DIRECTOR-RULINGS.md:136]).
3. **Why.** A frozen system page must still be retirable, and the compute must be able to record a seat or a new compute-written face (such as a menu). Letting a person change its rules would undo the freeze Matthew asked for (who gets hurt: every page governed by it).
4. **Axioms checked.** Axiom 1 [Axioms.md:13]: tension (R34, 1 says faces 00-04 freeze; this reads R36 as a narrow exception). Axiom 6 [Axioms.md:23]: pass. Axiom 2 [Axioms.md:15]: pass (one rule for open fields, narrowed by type).

**C25 (TOP). New, from R32, 2 and R34, 3. When an address lookup reaches a retired page, does it stop there?**
1. **Question.** A retired page "leaves active searches" [DIRECTOR-RULINGS.md:154] and does not block its title [DIRECTOR-RULINGS.md:174]. Finding by address walks book, shelf, desk, kernel, and the first match wins [seqAddr.md:101] [seqAddr.md:104]. When the book's page at that number is retired, should a lookup of that address stop at the retired page, or go on to the shelf's page with the same number?
2. **Proposed answer.** Stop there. An address lookup that reaches a retired page returns it, marked retired, with any successor named on its face 08. It does not fall through. Title search skips it, and its title is free (R34, 3).
3. **Why.** R34 frees the title, not the address: "R31 item 1 fixes the address-title pairing" [DIRECTOR-RULINGS.md:174], and a linked page "can only be retired, so the record is there" [DIRECTOR-RULINGS.md:153]. If the lookup fell through, a link or a cite to that address would quietly open a different page with different rules. Who gets hurt: everyone who linked to it, and the model drafting from the wrong page.
4. **Axioms checked.** Axiom 8 [Axioms.md:27]: pass (a pointer reaches its own source, not a look-alike). Axiom 6 [Axioms.md:23]: pass (the record stays). Axiom 2 [Axioms.md:15]: tension (books follow the parent live, and stopping at a retired page hides the parent's page at that number until the book writes a new one).

**C26 (TOP). New, from R34, 3 and R31, 8. When several pages share a title, what does a title search do?**
1. **Question.** Titles may be reused [DIRECTOR-RULINGS.md:174], and people see titles, not addresses [DIRECTOR-RULINGS.md:144]. When a person or the model searches for a title that several live pages share, what should the computer do?
2. **Proposed answer.** List every live match, nearest first (book, shelf, desk, kernel), each with its book's title, its kind and its last change; never pick one silently. The person or model picks; a link is then made from the picked page's address. Retired pages are left out.
3. **Why.** A silent pick would hand someone the wrong page under the right name. Who gets hurt: the person who links or edits the wrong page, and the model, which would read the wrong source. Showing context keeps addresses hidden (R31, 8) but makes the choice visible.
4. **Axioms checked.** Axiom 8 [Axioms.md:27]: pass ("Agreement is not connection": a matching title is not a link). Axiom 7 [Axioms.md:25]: pass (which page is meant is asked, not guessed). Axiom 3 [Axioms.md:17]: pass (the person picks; the compute lists; the model does not guess). Axiom 1 [Axioms.md:13]: pass.

**C27. New, from R34, 1. What is a system page, and may a person still read one?**
1. **Question.** R34, 1 says system pages "are backend and designed for control not for user to access" [DIRECTOR-RULINGS.md:169], but neither R31 nor R34 says what makes a page a system page. And the brief says the work "must be checkable by a person" [AGENTS.md:10]. Which pages are system pages, and may a person read them?
2. **Proposed answer.** A system page is a page whose face 00 type is `system`, "a kernel or structural page" [face00.md:138]. Users do not edit it and it does not appear in their normal search, but a person can still open it read-only in the reader to check the rules that govern their own pages.
3. **Why.** The type already exists and already carries "who may write it" [decisions.md:288], so no new mechanism is needed. Reading is not editing: a person who cannot see the rule governing their page cannot check it. Who gets hurt otherwise: the person told "no" by a rule they are not allowed to read.
4. **Axioms checked.** Axiom 1 [Axioms.md:13]: pass (control stays with the granted authority; reading grants nothing). Axiom 4 [Axioms.md:19]: pass (a rule's why stays readable). Axiom 7 [Axioms.md:25]: tension ("system page" as type `system` is still a reading, not his word). Axiom 3 [Axioms.md:17]: pass.

**C20. From R31, 6 and R30. What retires or completes a book, and does it freeze its general pages?**
1. **Question.** R30 says once a book is complete "changing pages shouldn't be possible anymore" [DIRECTOR-RULINGS.md:124]. R31, 6 says a book is a working journal, retired to the shelf, maybe partly complete [DIRECTOR-RULINGS.md:140]. R32 keeps general pages editable [DIRECTOR-RULINGS.md:152]. What marks a book retired, and does retiring stop edits to its general pages?
2. **Proposed answer.** A compute-written entry on the book's identity page, approved by you, marks it retired. From then on all its pages are read-only in that book, general pages included; the book stays on record and leaves active searches like a retired page (C23). Work that continues goes into a new book that links back.
3. **Why.** R30's book rule was not narrowed by R32, which speaks of links and pages [DIRECTOR-RULINGS.md:152]. A retired journal that keeps changing is not a reference; who gets hurt: anyone who relies on the shelf copy as it was when the work ended. A new book keeps the chain going, as R31, 1 says: "point to a new page to keep the chain going or write a new one" [DIRECTOR-RULINGS.md:129].
4. **Axioms checked.** Axiom 6 [Axioms.md:23]: pass. Axiom 1 [Axioms.md:13]: pass (retiring needs your approval). Axiom 7 [Axioms.md:25]: pass (partly complete stays marked as such). Axiom 2 [Axioms.md:15]: tension (a general page edited in the new book is a second place for the same subject, joined only by links).

**C18. From R31, 3. Where do office kinds keep their content?**
1. **Question.** Pages may hold office kinds, such as a cell-based sheet or a word document [DIRECTOR-RULINGS.md:134]. R27 keeps face 04 plain readable text [DIRECTOR-RULINGS.md:111]. Does a sheet or document live in face 04 as plain text, or in a code face?
2. **Proposed answer.** In face 04 as plain text: a sheet as rows of cells (one row per line), a document as marked-up text. Each office kind is a face 00 type with its own rules. Formulas and layout are stored as text too.
3. **Why.** Keeps R27 and keeps every person's content readable in any editor and checkable without a tool [AGENTS.md:10]. Small changes stay line ranges (Step 17), so history and the R3 round trip work unchanged. Who gets hurt otherwise: a person who cannot read their own sheet without the app.
4. **Axioms checked.** Axiom 3 [Axioms.md:17]: pass (person reads face 04; model and compute read code faces). Axiom 4 [Axioms.md:19]: pass (the why stays readable). Axiom 2 [Axioms.md:15]: pass (one copy of the content). Axiom 9 [Axioms.md:29]: tension (plain-text sheets are untried; they need a trial before being trusted).

**C19. From R31, 4. Who is a "developer" for updating and promoting a new copy?**
1. **Question.** Promotion is "dev only ability" [DIRECTOR-RULINGS.md:135]. The sources have a `dev` band role (N4) [workflow-loop.003.md:38], and builders who are agents. Who may promote?
2. **Proposed answer.** People you name as developers, each promotion approved by you; the builders may prepare the new copy as a proposal; the compute writes it.
3. **Why.** Authority is granted, not taken: a promotion replaces what every link to the old page leads people to via the back-link, so it needs a named, approved person (who gets hurt: everyone using the old page). The `dev` band is a place for design work, not a permission. Only the compute writes to disk [format.md:18].
4. **Axioms checked.** Axiom 1 [Axioms.md:13]: pass. Axiom 6 [Axioms.md:23]: pass (promotion is a new copy, the old stays). Axiom 9 [Axioms.md:29]: pass if each promotion passes a hostile trial first, as seats do [DIRECTOR-RULINGS.md:9].

**C13a. From R31, 8 and R34, 3. Is "plain text" ASCII, and how are same-titled pages told apart with addresses hidden?**
1. **Question.** R31, 8 says titles stay plain text and addresses are back end only [DIRECTOR-RULINGS.md:144]. Must titles (and card keys) be ASCII? And with addresses hidden, how does a person tell two pages with the same title apart?
2. **Proposed answer.** Yes, titles, addresses and card keys stay ASCII. Titles may repeat (R34, 3 [DIRECTOR-RULINGS.md:174]), so where two pages share a title, the reader shows the title with its book's title and the page's kind beside it, never the address (see C26).
3. **Why.** The grammar allows only lowercase letters, digits and hyphens [seqAddr.md:112] [seqAddr.md:280] [seqAddr.md:281]; links carry the title and must match byte for byte (R30, R32, 1); D432 says the same [DECISIONS-LOG:560]. Who gets hurt otherwise: a link that breaks because two spellings of one letter look alike.
4. **Axioms checked.** Axiom 8 [Axioms.md:27]: pass (exact match). Axiom 7 [Axioms.md:25]: pass. Axiom 3 [Axioms.md:17]: tension (people who write in other alphabets cannot title pages in them).

**C24. From R31, 9 (held 7 by Prima). Where does the "last change" note go?**
1. **Question.** Matthew asked "where do we place those short logs?" [DIRECTOR-RULINGS.md:145]. Prima's answer is a last-change note in the page index, written only by the compute, held 7 [DIRECTOR-RULINGS.md:146]. Is that right?
2. **Proposed answer.** Yes: the page signpost (Prima's page index) carries a last-change line for each page, derived from face 09 and written only by the compute. Face 00 holds no log.
3. **Why.** Face 00's open fields change only on events (R36) and face 00 should not churn (R25 [DIRECTOR-RULINGS.md:101]); the page signpost already changes on every write (R32, 3 [DIRECTOR-RULINGS.md:156]), so the note costs nothing extra and is one hop, as fast as face 00.
4. **Axioms checked.** Axiom 2 [Axioms.md:15]: pass (derived, not a second log). Axiom 8 [Axioms.md:27]: pass (points to face 09, the source). Axiom 6 [Axioms.md:23]: pass.

**C2. From t171u (A3). Should face 09 also record attempts that were refused or halted?**
1. **Question.** Today a refused proposal writes nothing [BUILD-LOG:53]. Should a page's face 09 log also list refused and halted attempts, with reasons?
2. **Proposed answer.** Halted attempts yes (a halt is a fact about the page's safety); plain refusals no, they stay in the compute's reply to the proposer.
3. **Why.** A halt means something disagreed on this page, and the next reader needs to know (who gets hurt: a person trusting a page that once failed its check). Refusals are many and say more about the proposal than the page.
4. **Axioms checked.** Axiom 7 [Axioms.md:25]: pass (a halt is a known gap, kept visible). Axiom 6 [Axioms.md:23]: pass. Axiom 2 [Axioms.md:15]: pass.

*R35 note.* The copy check now elevates through compute, model and person [DIRECTOR-RULINGS.md:178]. SECTIONS-AND-CARDS.md Q8 proposes logging copy-check refusals and every elevation step on face 09, which goes against this answer's "plain refusals no". Tension named, not resolved; the two questions should be answered together.

**C4. Related to QD46 (D414). How much should the compute trust the signposts when it opens a book?**
1. **Question.** Should the compute fully check every chain at start-up, check each piece only when read, or replay everything on every open?
2. **Proposed answer.** Check every chain once at start-up, then replay-compare; until then answers are marked `9` and writes are refused; any mismatch halts (D324). This is Tester fix 1 and keeps D414.
3. **Why.** Damage in a part nobody has read yet is found at start, not months later (who gets hurt: the person reading that part). Tester measured start-up at 1.0 s warm and 2.5 s cold for 100k writes [SEQ-PROTO-RESULTS.md:129].
4. **Axioms checked.** Axiom 9 [Axioms.md:29]: pass (nothing trusted before its check). Axiom 1 [Axioms.md:13]: pass (mismatch halts, not chosen). Axiom 8 [Axioms.md:27]: pass.

**C5. May old lines ever be tidied away?**
1. **Question.** May the compute ever cut old lines, or start a new file generation with the old one frozen?
2. **Proposed answer.** Never, for now (K1). Revisit only if a real book grows too slow, then use K2 (new generation, old file frozen and linked) with your approval.
3. **Why.** Tester measured that speed is fine at 100k writes (SEQ-PROTO-RESULTS.md, Step 16). Cutting history would break the line back for everyone who cites an old version.
4. **Axioms checked.** Axiom 6 [Axioms.md:23]: pass for K1 and K2; K3 (cutting) fails. Axiom 8 [Axioms.md:27]: pass for K2 only if linked both ways.

**C6. From t171u (A2). Is a band level wanted in the export and the signposts?**
1. **Question.** Should signposts have a band level of up to 100 pages, or one flat list of pages?
2. **Proposed answer.** Band signposts of up to 100 pages [seqAddr.md:240], changed rows only, each band full every 64 of its own writes, as a builder setting recorded with its why.
3. **Why.** Tester measured at most 99 reads against a bound of 131 [SEQ-PROTO-RESULTS.md:63]; a flat list would rewrite thousands of rows per write.
4. **Axioms checked.** Axiom 2 [Axioms.md:15]: pass (same shape at every scale). Axiom 4 [Axioms.md:19]: pass (why recorded).

**C7. From t171u (A2) and Tester's prototype. Which form of git blob for file fingerprints? (lesser)**
1. **Question.** The chain is always SHA-256 over raw bytes. Should file fingerprints use git's default blob hash (SHA-1) or git's SHA-256 form?
2. **Proposed answer.** Git's SHA-256 form.
3. **Why.** SHA-1 is old and has known collisions; a fingerprint that can be forged protects nobody. The SHA-256 form can still be checked with git.
4. **Axioms checked.** Axiom 9 [Axioms.md:29]: pass. Axiom 2 [Axioms.md:15]: tension (the kernel builder's existing seat pins use the repo's current blob form; two forms would live side by side until moved).

**C8. From t171u (A2, A5). Should an exported book carry what it inherits?**
1. **Question.** When a book is exported as one file, should it also bundle the inherited pages it relies on?
2. **Proposed answer.** As an option, yes, marked as a view of the inherited pages, never as the book's own pages (Tester's pick).
3. **Why.** A reader on another machine cannot follow links into a kernel they do not have (who gets hurt: the person opening the export). Marking them as a view keeps the copy from becoming what it points to.
4. **Axioms checked.** Axiom 8 [Axioms.md:27]: pass (marked as a copy). Axiom 2 [Axioms.md:15]: tension (a bundled copy is a second copy, even if marked).

**C10. From t171u (A5), sharpened by R32, 1. Do references other than links also name only pages?**
1. **Question.** Links name only a page and give the current page [DIRECTOR-RULINGS.md:152]. May cites and work-card references still name a face or counter and pin a version, for example a seated pack `05.02` with its blob?
2. **Proposed answer.** Yes. Links name pages and follow the current page; cites name exactly what was relied on, version included (working path D348 [DECISIONS-LOG:411]).
3. **Why.** A cite records what a decision rested on; if it followed the current page, the reason for an old decision would silently change (who gets hurt: anyone checking why a choice was made). A link is for finding; a cite is for proof. R35, 3 (held 7 [DIRECTOR-RULINGS.md:182]): in the sections design, a section no longer cites another page's card; it links the page, and the compute serves the needed piece. So a card-level reference across pages is only ever a cite of what was relied on, never a reuse.
4. **Axioms checked.** Axiom 6 [Axioms.md:23]: pass (the past a decision rested on stays visible). Axiom 4 [Axioms.md:19]: pass (the why keeps its evidence). Axiom 8 [Axioms.md:27]: pass.

**C1, leftover. Names (lesser).**
1. **Question.** The exported whole book is a `.seq` file. What are the one-page view and the stored small files called?
2. **Proposed answer.** The one-page view stays `.seq` with a `page` marker in its header; the stored files are named by face number inside the page folder (back end only, R31, 8).
3. **Why.** People never see the stored names (addresses are back end only), so only the two `.seq` shapes need telling apart, which the header does.
4. **Axioms checked.** Axiom 2 [Axioms.md:15]: pass. Axiom 8 [Axioms.md:27]: pass (the header says what the file is).

**Settled choices, and what each now is:**

- **C21. Settled by R34, 1.** System pages freeze faces 00-04 once linked; they are back end, built for control, not for users to access [DIRECTOR-RULINGS.md:170]. Left over: what a system page is, and whether a person may read one (C27).
- **C22. Settled by R36.** Face 00 is split like a registry: locked fields (address, title, page type, and any others named later) never change; open fields may change, so R25's records on 00 continue; R32's lock applies to the locked fields [DIRECTOR-RULINGS.md:190]. Left over: which other fields lock (C28) and system pages (C29). Its proposal (seat records and new faces move to face 09 or a new page) is withdrawn.
- **C23. Settled by R34, 3.** This plan's proposal was rejected. Titles may be reused; a retired page does not block its title; R31, 1 fixes the address-title pairing, not the title alone [DIRECTOR-RULINGS.md:174]. Left over: whether an address lookup stops at a retired page (C25), and what a title search does with repeats (C26).

- **C16. Settled by R32, 1.** A link names a page (address plus title) and gives the current page; old versions stay in the log [DIRECTOR-RULINGS.md:152]. This plan's proposed answer (Option A) matched.
- **C15. Settled in part by R32, 2.** Face 00 locks once done, for every page (R36: its locked fields); a linked page can only be retired, never deleted; a retired page stays on record and leaves active searches [DIRECTOR-RULINGS.md:154]. Not answered: what a system page is (C21).
- **C17. Settled by R32, 3.** Face 00 holds the page type and its face list; the page index (this plan's page signpost) holds where each face sits [DIRECTOR-RULINGS.md:156]. The face list is an open field (R36 [DIRECTOR-RULINGS.md:190]).
- **C11. Settled by R31, 1 and 3; narrowed by R32, 1 and 2.** Locks are for system pages [DIRECTOR-RULINGS.md:134]. What a link fixes for every page is the address-title pairing and existence [DIRECTOR-RULINGS.md:152]; face 00's locked fields lock once done [DIRECTOR-RULINGS.md:154] [DIRECTOR-RULINGS.md:190]. System pages freeze 00-04 once linked (R34, 1 [DIRECTOR-RULINGS.md:170]). Left over: C27.
- **C14. Settled by R31, 2.** On a locked system page the title and finished faces 00-04 freeze; compute-only additions continue [DIRECTOR-RULINGS.md:132]. Confirmed for system pages by R34, 1 [DIRECTOR-RULINGS.md:170].
- **C12. Settled by R31, 3 and 4.** A locked system page's face 04 changes only through a developer's new copy [DIRECTOR-RULINGS.md:136]; general pages stay editable [DIRECTOR-RULINGS.md:134].
- **C1a. Settled by R31, 7.** One folder per page, one file per face [DIRECTOR-RULINGS.md:142].
- **C1. Settled by t175u, 1.** Small files stored; whole books exported. Names leftover above.
- **C3. Settled by t175u, 2.** Face 04 plain text; other faces may be compact code.
- **C13. Settled in part by R31, 8.** Titles plain text; addresses back end only [DIRECTOR-RULINGS.md:144]. Leftover: C13a.
- **C9. Closed by R31, 10.** Old versions can't be changed [DIRECTOR-RULINGS.md:148].
- How face 04 edits are stored: R29 ("go with Google's approach"); Step 17.

---

## Still open

- C25, C26 and C28 (the top three), then C27, C29, C20, C18, C19, C13a, C24, C2, C4-C8, C10, and the C1 naming leftover. All are in Matthew's four-part form.
- Settled by R36: C22. Settled by R34: C21, C23. Settled by R32: C16, C17, and C15 in part. Settled by R31: C11 (narrowed by R32), C12, C14 (confirmed by R34, 1), C1a, C13 in part. C9 closed.
- Prima's entry R28 (short log in 00) is still held 7: R31, 9 says no log in face 00; Prima's answer is held 7 until Matthew confirms [DIRECTOR-RULINGS.md:146] (C24). R29's hold is closed [DIRECTOR-RULINGS.md:148]. R30's hold [DIRECTOR-RULINGS.md:125] appears answered by R31, 3 and R32, 1 [DIRECTOR-RULINGS.md:134] [DIRECTOR-RULINGS.md:152], but Prima has not marked it closed; this plan does not close it.
- New tensions from R32 (Step 13): face 00 locked against R25's records onto 00 and a fixed face list against a later-needed face (both settled by R36); "the info might change on the faces" against the system-page freeze (settled by R34, 1); retired pages leaving search against address fall-through (C25).
- New tensions from R34: repeated titles with hidden addresses (C26, C13a); "not for user to access" against "checkable by a person" (C27).
- Tensions still open from R31: link-alone locking of system pages against Tester's "seated AND linked" (R34, 1 confirms the freeze once linked; Tester's draft-freezing risk remains for system pages); a retired book against editable general pages (C20); office kinds against R27 (C18); developer-only promotion (C19); hidden addresses and same titles (C13a).
- **Build gap, face 09.** The spec's face table still says face 09 is unassigned [seqAddr.md:158], and the core refuses writes to face 09 (`crates/seqaddr-core/src/validate.rs:232-233`; only faces 00-06 and 08 are active, `crates/seqaddr-core/src/face.rs:72`). R28 needs both changed. This plan does not edit them; it is build work.
- **Build gap, outside writers.** At HEAD, store.rs still cuts a longer file at every append (`crates/compute/src/store.rs:940-941`), there is no OS file lock, and the builder still writes to `books/` (`kernel/build.mjs:29`, `:846`). Moving the builder's output is now approved by R33, 1 [DIRECTOR-RULINGS.md:160], and Tester is building it, along with the time-order check (R33, 3 [DIRECTOR-RULINGS.md:164]) and the Host check (R33, 4 [DIRECTOR-RULINGS.md:166]). The cut-at-append fix and the OS lock are still Tester's working paths, not approved. No code is changed by this plan.
- R33, 2 (refuse copied text) was held 7 [DIRECTOR-RULINGS.md:162]. R35, 1 approves the outline with elevation (compute, model, person) [DIRECTOR-RULINGS.md:178] and R35, 2 approves a face 03 menu on any page [DIRECTOR-RULINGS.md:180]. Still open in `docs/design/SECTIONS-AND-CARDS.md`: what "highly certain" means (Q7), face 09 logging of copy-check steps (Q8, against C2), and cross-page card reuse (Q3, held 7 by R35, 3 [DIRECTOR-RULINGS.md:182]). The decisions.md:404 update for the menu card is pending in the spec.
- New tensions from R35: copy-check logging against C2.
- New from R36: which face 00 fields lock beyond the three named (C28); open fields on a linked system page (C29).
- How a write that spans several pages is made all or nothing under small files. Page 0000 may hold only face 00 [DIRECTOR-RULINGS.md:41], so a book-wide log cannot sit on the door page. Tester's pick: a compute-only book journal, like the `.queue` file (C1a).
- The kernel builder's whole-file rewrite [R23-R25-lineage.md:94] (the whole-file write is now at `kernel/build.mjs:846`; the lineage note cites `build.mjs:818`, which has since moved).
- Two copies of one book with the same address (a fork, D427). The page and book seeds (Step 10) now catch a copy moved to a new address, but not a byte-exact copy at the same address [SEQ-PROTO-RESULTS.md:108]. Tester's pick (working path, not a ruling): the compute halts if two files claim one address (axiom 1 [Axioms.md:13]); a copy that changed apart gets a new address before it comes back. Locked pages are the same in both copies (SEQ-FILE-PLAN-TEST-2.md section 7a); but a link gives each copy's current page (R32, 1), so links to general pages would read differently in each, which is why the fork rule must halt. Two pages with the same title at different addresses are not a fork (R34, 3); only two files claiming one address are.
- Hand edits to a face 04 file made outside the compute. Now designed in Step 17 (taken in by a named person, typist not known). Earlier, Tester's pick (working path, not a ruling): the compute keeps a current-view 04 file and compares its fingerprint at start or before a read; if changed, the logged 04 stays live, the edit shows as a draft (R5), and it is booked as a small change once who made it is known, else the person is asked; on a locked page the edit goes to a rework copy (SEQ-FILE-PLAN-TEST-2.md section 7b). Only the compute writes [format.md:18].
- Face 04's small-change format (line ranges, Step 17) is designed for plain text only; office kinds wait on C18.
- Not measured by the prototype: power loss, a real cold disk, books over 100k writes or 10,000 pages, many readers at once, the export file, git blob hashing [SEQ-PROTO-RESULTS.md:162]-[SEQ-PROTO-RESULTS.md:169]; and the race fix (Step 11).
- QD65 stays with Matthew.

---

## Related open questions (named, not closed)

- QD34: is the `.seq` file layout OK [QUESTIONS-FOR-DIRECTOR.md:298]. This plan does not answer it.
- QD46: snapshot trust (C4 above) [QUESTIONS-FOR-DIRECTOR.md:360].
- QD16: what happens after counter 98 (would matter if face 09 were ever a counted face) [QUESTIONS-FOR-DIRECTOR.md:180].
- QD57 / D427: two copies changed apart [QUESTIONS-FOR-DIRECTOR.md:414].
- QD60 / D431: hardware; a local disk that honours fsync [QUESTIONS-FOR-DIRECTOR.md:430].
- QD63 / D432: accented letters [QUESTIONS-FOR-DIRECTOR.md:446]. R4 is now updated by t175u for non-04 faces; whether accented letters return to face 04 is not touched here.
- QD66, QD67: how 00 counter faces are seated and climb; face 09 does not replace them [QUESTIONS-FOR-DIRECTOR.md:66] [QUESTIONS-FOR-DIRECTOR.md:76].
- QD65 stays with Matthew; this plan does not touch it.

---

## Sources

Every bracket cite in this file, by file and line (296 distinct; 16 new in this revision against 544555e). Each was checked against the file at the time of writing.

- `docs/spec/Axioms.md` (the nine axioms): lines 13, 15, 17, 19, 21, 23, 25, 27, 29.
- `docs/spec/DIRECTOR-RULINGS.md` (rulings R1-R36; R26-R30 entered by Prima in e1a60aa, R31 in f2c8459, R32 in ff60c28 and 7289c45, R33 in 865b880, R34 in a8e8dd3, R35 in 8f6e9a7, R35 note in 9717698, R36 in 71e45ee): lines 1, 9, 12, 15, 16, 20, 29, 38, 41, 76, 97, 100, 101, 103, 104, 105, 106, 108, 109, 110, 111, 113, 114, 115, 118, 119, 120, 123, 124, 125, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 150, 151, 152, 153, 154, 155, 156, 158, 159, 160, 162, 163, 164, 165, 166, 168, 169, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 182, 184, 185, 186, 188, 189, 190.
- `docs/spec/AGENTS.md` (the brief): lines 10, 41, 42, 44, 45.
- `docs/spec/format.md` (book format): lines 12, 15, 18, 21, 25, 41, 42, 50, 51, 54, 60, 61, 66, 70, 74, 79, 81, 86, 88, 94, 95, 96, 97, 100, 102, 105, 139, 140, 141, 145, 146, 147, 149, 157.
- `docs/spec/seqAddr.md` (addresses): lines 7, 14, 18, 19, 20, 21, 24, 89, 101, 104, 110, 111, 112, 114, 115, 116, 127, 138, 150, 152, 153, 155, 157, 158, 168, 175, 184, 230, 240, 243, 251, 269, 271, 280, 281.
- `docs/spec/seqpage.md` (the page view): lines 11, 13, 14, 84, 199, 206, 208.
- `docs/spec/face00.md` (face 00 draft): lines 59, 65, 137, 138, 146, 170, 171, 177, 179, 198, 210, 214, 236, 238, 248, 252.
- `docs/spec/decisions.md`: lines 128, 182, 285, 286, 287, 288, 301, 404, 516.
- `docs/spec/review.md`: lines 53.
- `docs/spec/drafting.md`: lines 7, 12, 14.
- `docs/spec/workflow-loop.003.md`: lines 38.
- `docs/design/DESIGN.md`: lines 17, 157, 165, 167, 173, 189.
- `docs/design/DECISIONS-LOG.md` (working paths, not rulings): lines 380, 381, 383, 384, 386, 407, 408, 410, 411, 415, 427, 440, 524, 548, 550, 558, 560.
- `docs/design/R23-R25-lineage.md`: lines 94.
- `docs/design/QUESTIONS-FOR-DIRECTOR.md`: lines 66, 76, 180, 298, 360, 414, 430, 446.
- `docs/BUILD-LOG.md`: lines 3, 6, 38, 53, 54, 66.
- `docs/design/SEQ-PROTO-RESULTS.md` (Tester prototype, commit 7697815; working paths, not rulings): lines 5, 13, 14, 15, 27, 31, 35, 37, 63, 76, 82, 86, 87, 89, 90, 95, 96, 97, 103, 104, 108, 109, 111, 114, 117, 118, 119, 120, 127, 128, 129, 130, 131, 134, 135, 137, 138, 139, 146, 147, 148, 149, 150, 151, 152, 154, 155, 158, 160, 162, 169.
- Code read, not changed: `crates/compute/src/store.rs:1009-1023`, `crates/compute/src/store.rs:307`, `crates/compute/src/store.rs:917`, `crates/compute/src/store.rs:940-941`, `crates/seqaddr-core/src/face.rs:72`, `crates/seqaddr-core/src/validate.rs:232-233`, `kernel/build.mjs:29`, `kernel/build.mjs:846`.
- `docs/design/SEQ-FILE-PLAN-TEST.md` (Tester's stress test, commit 50fdfac), `docs/design/SEQ-FILE-PLAN-TEST-2.md` (Tester's stress test 2, commit e99665e), `docs/review/OUR-CODE-VS-CURSOR-LESSONS.md` (Tester's code review, commit 7e67b97) and `docs/design/SECTIONS-AND-CARDS.md` (Designer plan, commit 3c7401f, revised for R35 in b12dc00 and for the R35 note and R36 in ab19e04). Working paths, not rulings.
- Matthew's words, 16 Nov 2026 (passed on by Prima): first ideas, not rulings.
- Director answers t171u (11:16 AM EST) and t172u (11:17 AM EST), Director rulings t175u (11:24 AM EST), and Director ruling t184u (11:47 AM EST), relayed by Prima; entered by Prima as R26-R30 (commit e1a60aa) and R31 (commit f2c8459) in `docs/spec/DIRECTOR-RULINGS.md`. This plan quotes them and does not number or edit them.
- `docs/design/QUESTIONS-FOR-DIRECTOR.md` headings cited: QD16, QD34, QD46, QD57, QD60, QD63, QD66, QD67.
