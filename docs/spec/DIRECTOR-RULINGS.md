# Director rulings (given in chat; these govern over older spec wording)

## R1 — 2026-11-11 2:38 PM EST — the zero sequence is the door
Director's words: "a 00seq is the door 00 and 0000 are the same as a full zero sequence."
Meaning: on any axis, the full-zero sentinel (`00` for a 2-digit axis, `0000` for the page axis) is the **door**. Older spec wording that calls it owner, identity, or board refers to this same location; use the word "door".

## R2 — 2026-11-11 2:44 PM EST — build-stage approval
Director's words: "Approval without my eyes is fine for this stage of the work."
Meaning: during this build stage, a face may be seated without the Director's review once it has passed a hostile trial (axiom 9) from a different view than its maker. Record it as `approved-by: build-stage (R2)` with the trial reference, so every such seat can be found and re-reviewed later. This does not let anyone answer an open Director question (those stay 7 in QUESTIONS.md).

## R3 — 2026-11-11 2:46 PM EST — the page file type (.seq)
Director asked for a new file type that holds one multifaceted page. Ruling: the **book is the real stored copy**; the `.seq` page file is a **view** you export from a book and import back (import goes through the normal proposal queue). Round trip book -> .seq -> book must be lossless.

## R4 — 2026-11-11 2:54 PM EST — plain characters only
Director's words: "Remove accented letters from being used. We want a simple storage design for now. So limited characters is fine."
Meaning: stored files (books, .seq pages, addresses, titles, card text) use plain ASCII only: printable characters 0x20-0x7E plus newline. Any other byte (accented letters, emoji, tabs, CR) is rejected on write with a clear error, and a book holding one is reported as damaged on read. This is a simplicity choice for now and may widen later.

## R5 — 2026-11-11 2:55 PM EST — drafts are found (answers kernel Q2)
Director's answer to Q2: "Yes. Draft faces count and lookups find them."
Meaning: when the only copy of a face is a draft, resolution finds it (seqAddr.md:164 "Draft faces count"; books follow the kernel live, decisions.md:128). The result must still show the face's state as draft so a reader can tell it is unseated. Where a seated face and a draft both exist at the same spot, the seated face wins.

## R6 to R10 — 2026-11-11 3:03 PM EST — answers to kernel Q1-Q6
Director's words (t64u), quoted then read:

**R6 (Q1)** "Axioms exist outside of the book as a 00.axioms on the desk."
Read: the axioms are not a page inside a book (so not page 0050). They sit at desk level in the desk's 00 spot, titled axioms. Working address: `00.00.axioms` on the kernel desk (7 until the Director confirms the exact address).

**R5 follow-up (Q2)** "Yes it can be looked up but also why is it a draft?"
Read: a draft is found (R5), and the lookup should show why it is a draft (its reason/notes), not just that it is one.

**R7 (Q3)** "When a local override happens it exists in the reserved face pages of 0001-0009. Then it states what its changing, why it's there, why it's needed, what it should achieve. It might not change any faces but some structure or behavior. Those are 0020-0049 for behavior and 0050-0099 for structural."
Read: an override is written as its own page in the book's reserved range 0001-0009. It states: what it changes, why it is there, why it is needed, what it should achieve. Its target may be a face, a behavior (0020-0049) or a structure (0050-0099). An override does not silently replace a face in place.

**R8 (Q4)** "Only if its a draft. See the drafting.md to understand why we have the draft so we don't replace an existing work from memory."
Read: `FF.draft` exists only while a face is being drafted. It is the copy drafting.md step 1 makes so seated work is never replaced from memory. A draft is addressed as `...PPPP.FF.draft`.

**R9 (Q5)** "Faces do not have sentinels. Only pages, books, shelves and desks."
Read: no `FF.00` and no `FF.99`. Counted faces have no door; counters run 01-98 only. Sentinels (00/99 and 0000/9999) apply only to the desk, shelf, book and page axes. Narrows R1 to those axes.

**R10 (Q6)** "Page 0000.00 is the only location that exists. 00 is a registry location on a page, because it's multi faceted."
Read: on a book's door page 0000, face 00 is the only face. On any page, face 00 is the registry: the place that lists the page's faces (it is not a sentinel, per R9). So a door page needs no content face.

## R11 — 2026-11-11 3:07 PM EST — common questions, solved by key words (answers kernel Q7)
Director's words (t65u): "The what is my name will become part of a common questions people ask list. When we see a version of this, it becomes linked as a sentence; it works like brands do. This is how we let the compute solve. So when it sees prepositions, paired with key words like 'what' + 'name' + 'my' we can use those to solve and give the best guess. Most people only have a few important words when they write or say something. We use this as how we solve. Then compute should be complex enough to parse the words and find what it should hand to the model. It should list 1-3 pieces from that the model can use its intelligence to solve, or ask the model about another option. Otherwise it should ask the person what they are saying, probing them for more detail until the compute and model can solve and resolve their prompt."
Read:
- There is a **common questions list**. Each entry is a sentence pattern that works like a brand card: a set of key words (e.g. what + my + name) linked to what answers it (e.g. the user's name -> the `bob` card).
- The compute pulls the few important words out of a prompt (key words plus the small linking words), matches them to the list and to brand cards, and ranks the best guesses.
- It hands the model **1 to 3 pieces**. The model uses its own judgment to solve from them, or asks the compute for another option.
- If nothing fits well enough, the compute asks the person what they mean, probing for more detail until it can be resolved.
- New phrasings of a known question get linked to that question, the way new forms are added to a brand.

## R12 to R18 — 2026-11-11 3:11 PM EST — answers to kernel Q8-Q14 (t66u, numbered 1-7 = Q8-Q14)
**R12 (Q8, also seqpage S9)** "The stamp should go in the .00 as the reg location."
Read: the stamp (address, title, type, state) lives in face 00, the page's registry location. A page's state is kept in the stamp in face 00.

**R13 (Q9)** "I like bands, it's a band because it binding together a set of pages into a work space."
Read: a band head (N?00) keeps the word "band". A band binds a set of pages into a work space. "Door" is only the all-zero sentinel (R1, narrowed by R9).

**R14 (Q10)** "Yes."
Read: a face may be seated while its page's door is still a draft.

**R15 (Q11)** "No."
Read: a brand card on face 01 does not need a 04 card (decisions.md:521 card-type table wins over :353 for brands).

**R16 (Q12)** "door"
Read: the dictionary's 03.00 is a door. TENSION with R9 ("Faces do not have sentinels"): held as 7 and asked back to the Director. Builders do not resolve it.

**R17 (Q13)** "Its broken into 4 sections. Each one has it's own important. 0000-0019 are static 0020-0099 aren't just locations."
Read: below 0100 the book is split into four sections, not one reserved range (Q13 option B). 0000-0019 are static; 0020-0099 are working pages, not just locations (0020-0049 behavior, 0050-0099 structure). The exact four-way split is 7: seqAddr.md lists 0000, 0001-0009, 0010-0019, 0020-0049, 0050-0099 (five rows); asked back to the Director.

**R18 (Q14)** "The matching would be in the hundreds range as in workflow. So N4CC, CC is a counter space, so if you have a workflow from N3-N7 then N403.IDE-design would match N503.IDE-design. They are matched by the CC and the title."
Read: pages in different bands belong together when their last two digits (CC, the counter space inside the band) AND their title match. Example: N403.IDE-design and N503.IDE-design are one set across bands N3-N7.

## R19 — 2026-11-11 3:12 PM EST — what face 00 holds (answers seqpage S8/S9)
Director's words (t67u): "It's a registry location, it can hold a stamp, a registry, it's type. Each page type can have a different set of registry fields to use. But we have the stamp portion, a types field, that sort of thing. Fill out what is missing but that is what I am thinking."
Read: face 00 is the registry location. It holds (a) the stamp portion (address, title, state, axioms, lineage), (b) the page's type, and (c) a registry whose fields depend on the page type: each type defines its own set of registry fields. Builders are to draft the missing detail (the common fields and the per-type field sets) as a draft for the Director to see, never as settled law.

## R20 — 2026-11-11 3:14 PM EST — what counts as a "different view" for an R2 trial (answers design O1)
Director's answer (widget on t68s322): "Yes, a fresh session of the same model counts as a different view."
Read: a hostile trial run by a fresh session (a new subagent that did not build the face) satisfies R2's "different view", even on the same model. The builder's own session never trials its own work.

## R21 — 2026-11-11 3:25 PM EST — no override pages during this build
Director's answer (widget t68s326, "Who approves an override page?"): "No overrides for now. we build them in. But because we are working children desks can have override we are working on the app it's self right now."
Read: while we build the Workshop app itself, nothing is changed by an override page. Changes are built straight into the pages, the kernel or the app. Override pages (R7, 0001-0009) stay in the design for child desks later. The approver question is deferred until then. The sample override page 10.11.21.0001 is parked (not used), and R7 code stays but is not exercised.

## R22 — 2026-11-11 3:50 PM EST — every design choice recorded; seated 05 per page is its MVP work pack
Director's words (t77u): "I want you to make every design choice recorded. As the seated 05 for each page should explain what you learned and become the seated pack of work to achieve the MVP for each page that links back to the overall design. Keep moving forward save questions."
Read: (1) every design choice made in the build is written down with its source. (2) Each page gets a face 05 that says what was learned building that page and holds the work pack to reach that page's MVP, linking back to the overall design (docs/design). That 05 is seated (under R2 after a fresh-session trial, R20). (3) Builders keep moving and save questions instead of stopping.

## R23 — 2026-11-11 6:41 PM EST — the seated 05 is the best version of the pack (t79u)
Director's words (t79u): "So the seated 05 is for the best version of the pack. So a pass might need 3-5 fixes, the 05.02 might solve those issues. But when a page is done, we build the best version of the pack so it solves the issues models run into before they run it. Does that make sense?"
Read: This confirms R22: face 05 is seated. What is seated is the best version of that page's pack. During a pass, the pack (05.02) may change to cover the 3-5 fixes that come up. When the page is finished, we build and seat the best pack, so it already solves issues models run into, before the next model runs it. Earlier seated packs stay as the best so far; a better version is seated (after a fresh trial, R2 and R20) when the page is done. Held 7: whether an older seated 05 is un-seated when the new best version is seated, or both remain and the newer one wins.

## R24 — 2026-11-11 6:45 PM EST — climb 05.CC, then reseat an update; this aligns with axiom 6 (t80u, t81u)
Director's words (t80u): "Also we keep climbing the 05.CC so the best pack might change so we finish the original work it's 05.01-06 Then we seat 05. It needs an update we expanded the scope of that page or it MVP. So we run 05.07 built from the seat and the changes. AFter 3 more passes. The page is complete again and we reseat an update to 05."
Director's words (t81u): "this is to make it align with axiom 6. lineage matters."
Read: We climb the 05 counter (05.CC) as work proceeds. The first stretch is 05.01 through 05.06; when that original work is finished, we seat 05 (the best pack, R23). If the page's scope or its MVP then grows, we do not rewrite the seated pack. We start 05.07, built from that seated pack plus the new changes. After further passes, when the page is complete again, we reseat an update to 05. This is so it aligns with axiom 6 (Lineage): every piece descends from something; a change is a new step in the line, made visible; the past is not rewritten, because rewriting a step breaks the line — add the new step after it. The "05.01-06" and "3 more passes" are the shape of the climb, not a fixed count that every page must hit. This also settles the R23 hold 7: the older seated 05 stays in the line (it is not rewritten); the new best pack is seated as an update, after a fresh trial (R2 and R20).

## R25 — 2026-11-11 6:49 PM EST — face 00 is the registry root; a 00.counter lists prior fingerprints (t82u, answers Q51)
Director's words (t82u): "So I can see we have an exception for 00 it's special by being this registry root concept. That we don't seat 00 in the same manner. We record the changes onto 00 but we might need a 2nd 00.counter  Where its a list of the previous fingerprint before the changes  are made.  We count and compare the change.  Does that work?"
Read: Yes. Face 00 is special because it is the registry root, so it is not seated in the same manner as other faces. Changes are still recorded onto 00. A second face, a 00 counter (00.CC), holds a list of 00's fingerprint as it was just before each change. We snapshot that fingerprint first, then make the change, then count and compare: the old fingerprint, the change, and what 00 is now. This keeps the line (axiom 6) without needing face 00's own fingerprint to stay frozen. The list must be its own face, not lines inside 00, or writing the list would again change 00's fingerprint. This answers Q51 / QD05 (where the seat record lives): seat records may still be written onto 00; the line of 00 itself is kept on the 00.counter face. Held 7: whether those 00.counter faces are themselves seated in the normal way, and how the list climbs (00.01, 00.02, ...) when a new fingerprint is added.

## R26 — 2026-11-16 11:24 AM EST — R3 updated: small files are stored; whole books are an export (t171u, t175u)
Director's words (t171u, answer 2): "Yes we can keep small files then have the ability to export books later."
Director's words (t175u, 1): "yes change R3"
Read: this updates R3 (above, not rewritten, axiom 6). The stored form is today's small files. A whole-book .seq file is an export made from them, not the stored copy.

## R27 — 2026-11-16 11:24 AM EST — R4 updated: only face 04 must be human-readable (t171u, t175u)
Director's words (t171u, answer 1): "Our systems design needs to be understandable by our tech documentation But we want it fast for models and compute to work. Hench the multi faced design. So no it doesn't need to be. It can just be code. for every face other then 04."
Director's words (t175u, 2): "Update R4."
Read: this updates R4. Face 04, the person's face, stays plain readable text. Every other face may be stored as compact computer code (binary), for model and compute speed.

## R28 — 2026-11-16 11:16 AM EST — face 09 is the page's log (t171u)
Director's words (t171u, answer 3): "agreed 09 is log, we keep a short log in 00 if you think that is a superiour design."
Read: face 09 is the page's log. A short log in 00 is allowed only if shown to be better. Prima's view: it is not better, because 00 must stay small and rarely rewritten (R25). Held 7 until the Director sees the plan's answer.

## R29 — 2026-11-16 11:17 AM EST — people edit face 04 the Google Docs way (t171u, t172u)
Director's words (t171u, answer 4): "A user should be able to modify and change their documents in 04."
Director's words (t172u): "go with Google's approach."
Read: edits to face 04 are kept as a log of small changes plus full snapshots now and then. The current view is the latest, and old versions are never changed (axiom 6). Held 7: the t171u words "So they can't be changed" were asked back to the Director.

## R30 — 2026-11-16 11:24 AM EST — links use the page address and title; registered pages lock (t171u, t175u)
Director's words (t171u, answer 5): "We use the seqaddr system. our 2.2.2.4.title we don't include the face its a sub group of the page."
Director's words (t175u, 3): "Once a book is complete, changing pages shouldn't be possible anymore. A new copy can be made and reworked. But the original work shouldn't changed. Once a page is linked to and registered with the book it shouldn't change."
Read: a link points to a page's address plus its title (for example 2.2.2.4.title), never to a face. Once a page is registered and linked in a book, or the book is complete, that page is locked: no rename, no change. Rework goes into a new copy. So links never break. Held 7: how this fits face 04 edits (R29). Prima's reading: edits happen while a page is a draft, and registration locks it.

## R31 — 2026-11-16 11:47 AM EST — answers to the .seq lock and page questions (t184u, answering Prima's t183s712)
Each answer below replies to Prima's proposed answer with a why (t183s712). His words are quoted, and the reading follows.
1. Lock: "I agree, once it's linked it can't be used for anything else it's done. Even if the page is retired. It never is rewritten. OUr design is made so you can point to a new page to keep the chain going or write a new one. Once a address is given a title it exists and doesn't change anymore. it would break too much to allow it to be open"
Read: once an address is given a title, that pairing is fixed forever. Once a page is linked, it is done, even if it is later retired. To continue the work, point to a new page or write a new one.
2. What a lock freezes: "See above I think it answers it for you."
Read: Prima's answer stands. The title and the finished faces 00-04 freeze, and additions written only by the compute (05, 06, 08, 09) may continue. This also settles R24 against R30.
3. "So locked pages are for system pages, a normal page can be edited think our google document page. Our page design is to basically allow us to hold a full office suite inside of it as pages. So we could have pages that are cel based file system, a word file."
Read: locking applies to system pages. General pages stay editable in the Google Docs way (R29). Pages may hold office kinds, such as a cell-based sheet or a word document.
4. "No that is correct, we update and promote when its time to improve our work. This is dev only ability."
Read: a lock is never undone. Improvement happens by updating and promoting a new copy, and only developers can do that.
5. "Correct"
Read: a rework copy gets a new address, with links both ways.
6. "This of a book kind of like a working journal. In time each one is retired and put on a shelf as a refernce but once that piec of work is complete it's done. It could be used in the future or might only sit partly complete."
Read: a book is a working journal. When it's done it's retired to the shelf as a reference, and it may stay partly complete.
7. "Well yes, but we should have a type type that contains and orders this. With our reader able to open and see what data is there."
Read: one folder per page and one file per face, plus a type, written in face 00, that holds and orders the face files. The reader can open a page and show what data is there.
8. "Titles do, we keep addresses hidden from users it's back end only."
Read: titles stay plain text. Addresses are back end only and never shown to users.
9. "I agree, where do we place those short logs?"
Read: no log in face 00. Prima's answer (t184s714): a "last change" note in the page index, which only the compute writes. Held 7 until he confirms.
10. "I agree"
Read: R29's "So they can't be changed" means old versions can't be changed. The R29 hold is closed.

## R32 — 2026-11-16 12:02 PM EST — links point to the page, not a version; face 00 locks; linked pages only retire (t191u, answering Prima's C16, C15, C17 in t188s728)
1. Links (C16): "Lets say we have a book about relationships... So say page 1024 is about "Jim" That might be changed and updated. We don't want to link to exact wordings of a page face. But be linked so the compute can find out about Jim. So I think your answer is wrong, if you disagree tell me why."
Read: Prima's proposal (a link locks the version it points to) is rejected, and Prima agrees. A link points to the page (address plus title), and following it gives the current page. Old versions stay in the log (R29). This narrows R30 and R31 item 1: what is fixed forever is the address-title pairing and the page's existence, not the wording of a general page's faces.
2. System pages and lock (C15): "Yes, when a page is created, it gets its properties is assigned a title and seqaddr. Once the 00 is done it's locked the info might change on the faces but once a page exists and is linked it can only be retired, so the record is there, and not be in active searches."
Read: at creation a page gets its properties, title, and address. Once face 00 is done, face 00 is locked; the other faces may still change. Once a page exists and is linked, it can't be deleted, only retired. A retired page stays on record but leaves active searches.
3. Face list (C17): "I agree"
Read: face 00 holds the page type and its face list. Where each face sits is kept in the page index, so face 00 doesn't change on every write.

## R33 — 2026-11-16 12:06 PM EST — Tester's four fixes from the code-vs-lessons check (t192u, answering Prima's t190s736; review at 7e67b97)
1. Builder: "Yes, books change through compute not by models. Models can be wrong and having them answer a question correctly 100% of the time can be an issue."
Read: approved. The book builder stops writing into books/ and makes an export instead (R26). Books change only through the compute's gate.
2. Copied text: "So this is where sections and cards come in. A section is a piece of work in 04. cards exist in 01,02,03. So a menu from 03 can say what lives in small pieces on a page. Normally 01,02 aren't going to exist on normal pages othen then for key words. I think this might need some dev time."
Read: not yet approved. A section is a piece of work in face 04. Cards live in faces 01, 02, and 03, and a face 03 menu can say what small pieces live on a page. On normal pages, faces 01 and 02 usually hold only key words. The copy check needs design work against this before it is built. Held 7.
3. Clocks: "I agree"
Read: approved. Refuse a line dated earlier than the line above it.
4. Host check: "I agree."
Read: approved. Refuse requests that arrive with the wrong Host header.

## R34 — 2026-11-16 12:16 PM EST — system pages freeze; titles may be reused (t195u, answering Designer's C21 and C23 via Prima's t193s748)
1. C21: "yes I think we freeze system pages. They are backend and designed for control not for user to access."
Read: system pages freeze once linked (faces 00-04). They are back end, built for control, and not for users to access.
2. C22: "I need more explaination on this one."
Read: not ruled. Prima explained in t195s752. Held 7.
3. C23: "So we don't lock words in books. if you look at workflow you already know that titles can be reused."
Read: Designer's proposal is rejected. A retired page does not block its title. Titles may be reused, as the existing workflow already allows. Note: R31 item 1 fixes the address-title pairing, not the title alone.

## R35 — 2026-11-16 12:20 PM EST — copy check uses elevation; every page may have a face 03 menu (t197u, answering Designer's sections-and-cards Q1-Q3 via Prima's t194s750; design at 3c7401f)
1. Refuse or flag copies: "Yes this is where the elevate comes in. If the comp can't solve according to it's code, it gives it to the model, if the model can't solve to a high degree of certainty. then it goes to the person."
Read: the proposal stands (refuse exact and unmarked copies, flag partial overlap, allow links, key words, and cited quotes), and anything uncertain is elevated: compute first by its code, then the model, then a person if the model is not highly certain.
2. Face 03 menu on every page: "Yes of course, a page might contain the piece of a story. As such it might be broken into a number of sections perhaps dozens or more. So instead of the model eating everything it only gets what it needs."
Read: approved. Any page may have a compute-written face 03 menu of its sections, so a model loads only the sections it needs. This updates the pages 0001-0099 limit in decisions.md:404 for the menu card.
3. Section reusing another page's card: "Why would a section reuse a card?"
Read: not ruled; he questioned the premise. Prima answered (t197s757) that it shouldn't: a section links to the page (R32), and the compute serves only the needed piece. Held 7.

## R35 note — 2026-11-16 12:23 PM EST — how the face 03 menu is used (t198u)
Director's words: "Yes the menu is how the compute handles giving information to a model. If a model has a general query about "Jim" for example. The compute might have "jim" as a key word in 4 pages. instead of handing the model all the data in those pages it hands it the menu. So the model can decide what it should request first."
Read: for a general query, the compute finds the pages holding the key word and hands the model their face 03 menus, not their data. The model then asks for the sections it needs first.

## R36 — 2026-11-16 12:25 PM EST — face 00 is like a registry: locked fields and open fields (t200u, answering C22 after Prima's t198s761)
Director's words: "Ok so on face 00 think of it like windows registry. We have fields that nevere change and lock, like it's address, it's title, it's page type. Others could change. We can have a split on this."
Read: face 00 is split into two kinds of fields. Locked fields (address, title, page type, and any others named later) are set once and never change. Open fields may change, so R25's records on 00 can continue. "Once the 00 is done it's locked" (R32) applies to the locked fields. Which fields fall in which group beyond the three named is open. C22 is closed.

## R37 — 2026-11-16 12:56 PM EST — what we carry forward from the Codex Librarian tools (t204u, answering Prima's ranked list in t203s778; review at 65cac98)
Director's words: "1. I agree 2. I agree 3. I agree 4. Yes, that is good 5. I agree 6. It's good 7. good 8. good 9. Design with a min and a max, so we can shift the amount of logging we do up or down, we don't really know how much information we should be capturing in a log yet. 10. That is good."
Read: all ten are adopted:
1. One append-only log is the only source of truth, so a fresh process can rebuild from it.
2. A return and its next step are saved together, and a delivery id can't change its content.
3. The compute fills templates, bindings, and hashes, and the model writes only the judgment.
4. A review is tied to the exact version it read and goes stale when the page changes. A review is a record, not a link (R32).
5. Selected, pending, and accepted are separate states.
6. "Couldn't look" is kept separate from "isn't there".
7. A check before each run confirms every needed file and the expected state.
8. Refuse with a handback, and stop rather than invent a meaning.
9. An operation journal, designed with a minimum and maximum level so the amount of logging can be turned up or down. Where it lives (face 09 or a system log) is still open.
10. Every packet says what it gathered and what it didn't.
