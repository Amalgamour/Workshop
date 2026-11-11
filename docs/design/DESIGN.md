# Workshop design, as built (condensed)

state: draft, for the Director to read. Nothing here is new law.
made: 2026-11-11, lane DESIGN (Prima build).
why: the Director asked that "The decisions are to update into a more concise design." This is that, one short page per idea.

## How to read this

- Each page holds one idea, and each paragraph says one thing.
- Each sentence ends with its source in square brackets.
- `[seqAddr.md:14]` is line 14 of `docs/spec/seqAddr.md`. All spec files are in `docs/spec/`.
- `[R1]` to `[R4]` are the Director's rulings in `docs/spec/DIRECTOR-RULINGS.md`. A ruling wins over older wording [DIRECTOR-RULINGS.md:1].
- `[v2:22]` is line 22 of the Director's own seqaddr page, `/workspace/prima/kernel-fresh/01.seqaddr/seqaddr.director.2026-11-09.v2.md`.
- `[BUILD-LOG:31]` is `docs/BUILD-LOG.md`. A BUILD-LOG line tells you what was built, not what the law is.
- `[Q2]` is a question in `kernel/QUESTIONS.md`. `[O2]` is a question in `docs/design/OPEN.md`.
- The mark `7` means missing, and `9` means not yet trialled [Axioms.md:25] [Axioms.md:29].

## The pages

1. Address
2. Faces and cards
3. Tails (state)
4. The door and the sentinels
5. Books are logs
6. The .seq page (a view)
7. The compute and its queue
8. Finding (resolution order)
9. The workflow loop
10. Axioms

---

## 1. Address

**What it is.** Sequence Address is "new design for a file type" [v2:5]. A page "contains multiple faces instead of being 2d with one face" [v2:6].

**The axes.** The "Chosen sequence" is `2.2.2.4.2` [v2:14]. That is desk `DD`, shelf `SS`, book `BB`, page `PPPP`, face `FF` [v2:15-19] [seqAddr.md:16-22].

**Widths are exact.** "`4442.1` is invalid" [seqAddr.md:14]. Every axis is at least 2 digits [v2:12].

**Counters.** A counter `NN` can follow a face, and it is "a climbing number" [v2:37]. Counters run "01-98" [v2:40]. A counter is not an axis [seqAddr.md:24].

**The page is the anchor.** The page is the only 4-digit group, so an address reads by position [seqAddr.md:71]. "Missing ancestors are taken from the active book" [seqAddr.md:79].

**Short form is for people.** Users may write short form. Models always write the full address and state it back [seqAddr.md:95].

**A leading dot means this page.** `.04` is face 04 of the active page [seqAddr.md:92].

**Titles.** A title begins at the first dot group that is not strictly digits [v2:22]. A title stored in the stamp is the truth, and a title written in an address is checked against it [seqAddr.md:116]. *Open: where the title really lives is v2 clash 1, held and not re-asked [O34].*

**A word after a face.** The spec reads a word after a face as a card key, such as `...1014.01.ham` [seqAddr.md:111]. *Open: v2 clash 5 [O12].*

**One space per repository.** "Each repository is its own namespace and contains its own kernel" [seqAddr.md:41].

**Desks.** Desk `00` is the kernel, `01-09` are kernel branches, and `10-98` are user desks [seqAddr.md:36-38].

**As built.** The Rust core parses this grammar [BUILD-LOG:29]. The trial ran 20,000 generated addresses and 200,000 junk strings, and they all held [core-trial:11]. Plain ASCII only, for now [R4].

---

## 2. Faces and cards

**One page, many faces.** "Each face contains a different bit of information" [v2:7]. Each face is for a different reader: agents, compute or users [seqAddr.md:7].

**The faces.**
- 01 law: "agents understanding of the meaning of the page" [v2:66].
- 02 schema: "where templates live" [v2:67].
- 03 operate: "Designed for the compute" [v2:71]. It holds the card menu [v2:72] and states "where authority comes from" [v2:73].
- 04 user: "for the user to see the why of the page" [v2:75].
- 05 tasks: "a working place for working agents" [v2:79].
- 06 notes: "one notes per session" [v2:83]. A note includes "which model created the notes" [v2:85] and "why the note exists" [v2:87].
- 07: "reserved not active" [v2:89].
- 08 map: "where all the links for a page goes" [v2:91].
- 00: the door [R1]. The spec puts the page stamp here (address, title, state) [seqAddr.md:64]. *Open: v2 asks for a stamp header on every face [v2:58] [O2].*

**What a page needs.** It needs face 00 and at least one of 01-06 or 08 [seqAddr.md:163]. Draft faces count [seqAddr.md:164].

**Cards.** Cards "are like kamban cards" [v2:60]. "Cards titles are to be matched across faces" [v2:61]. In the spec, a card is a `##` heading, and "The same key on two faces is the same card" [seqAddr.md:168].

**Face 04 holds the why.** "The cards of face 01 and 02 must have a representation on face 04" [v2:75]. The compute rejects a write if the 04 card, its `why:` line or its body is missing [seqAddr.md:184].

**Card types.** Each face has a default card type, defined in the kernel [seqAddr.md:171].

**As built.** The core checks the 04 rule [BUILD-LOG:41]. The app shows an inherited 04 card instead of a false hole [BUILD-LOG:15]. The core still demands a local 04 card, which the trial flagged [core-trial:117-120]. *Open: [O8].*

---

## 3. Tails (state)

**What a tail is.** "A tail follows a title or a face" [seqAddr.md:122]. It gives the state [seqAddr.md:131-138].

**Counter tails.** These are the workflow states:
- `FF.NN.draft`: "the pack being written" [v2:46].
- `FF.NN.pack`: "ready to run" [v2:47].
- `FF.NN.open`: "Being run by a worker" [v2:48].
- `FF.NN.return`: "what was done" [v2:49].
- `FF.NN.review`: "the review" [v2:50].
- bare `05.MM`: "closed" [v2:51].

**Face tails, with no counter.**
- `FF.draft`: "Draft of a face not seated so not to be used as active" [v2:53].
- `FF.retired`: "A previously seated face turned into retired before it can be removed" [v2:54].

**Seated.** "Seated face exists only as FF no tail or counter" [v2:38]. "Seated face only legal formate DD.SS.BB.PPPP.FF" [v2:39].

**Where state lives.** "Workflow state lives only on counters" [seqAddr.md:140]. A page can also be `draft` or `retired` [seqAddr.md:126]. A desk, shelf or book takes its state from its door page [seqAddr.md:129] [R1].

**As built.** The core refuses workflow tails on faces that are not counted, and it refuses `retired` on counters [core-trial:16]. Every kernel face is a draft, and none is seated [BUILD-LOG:49]. *Open: is a draft found by a lookup [O3]? Where does a page keep its state [O5]? How is a draft written in the book [O11]?*

---

## 4. The door and the sentinels

**The door.** "a 00seq is the door 00 and 0000 are the same as a full zero sequence" [R1]. Old words for the same spot (owner, identity, board) now all mean "door" [R1].

**Two sentinels on every axis.** "Its a full sequence of 0 and of 9" [v2:98]. "Those addresses with a seq00 or seq99 are special locations and cannot be normal pages" [v2:100]. "it's the alpha and omega for the axis" [v2:101].

**Page 0000.** "Page 0000 must exist for a book to be a legal space" [v2:102].

**Page 9999.** "Page 9999 must exist if the book is refenencing a sequence of a continuation of a book" [v2:103].

**Desks and shelves.** "A desk must also have it's sentinal as DD.00" [v2:105]. "A shelf must also have a .00 as DD.SS.00" [v2:108]. *Open: the spec writes these as nested pages `DD.00.00.0000` and `DD.SS.00.0000` [seqAddr.md:61-62], which is v2 clash 4 [O14].*

**99 points onward.** "if a DD.99 exists it means it's linking to a child desk" [v2:106]. The child "must have it's .00 linking back" [v2:106]. In the spec, "A one-way link is invalid" [seqAddr.md:251].

**Missing is valid.** No `FF.99`, `PP99` or `9999` just means no continuation [seqAddr.md:254].

**As built.** The core names the zero sentinel `Door` in its types and errors [BUILD-LOG:30]. A book takes no writes until its door `0000.00` exists [BUILD-LOG:39]. *Open: is the door of a counted face (`FF.00`) written or worked out [O6]? Does a door page need a content face [O9]? Is a band head (`0400`) also a door [O23]?*

---

## 5. Books are logs

**A book is one file.** "A book exports as a single file" [format.md:21]. Desks, shelves and the kernel are book files too [format.md:21-28].

**Add-only.** "Each approved write is appended to the end of the book as one entry. Nothing is ever edited in place" [format.md:61]. The current state comes from replaying the entries in order [format.md:61].

**What that gives.** It gives history, rewind and fork, clean git diffs, and crash safety [format.md:64-67].

**Plain text.** Each entry is one JSON line, "readable in any editor" [format.md:70]. Face content stays Markdown [format.md:81].

**Derived, never written.** "Boards (`FF.00`), contents lists and ancestor path lists are derived from the log and never written as entries" [format.md:102]. *Open: this clashes with "board before counters" [format.md:123] [O6].*

**Snapshots.** A snapshot lets replay start late, and older entries stay [format.md:105].

**Plain characters.** Stored files use printable ASCII plus newline, and anything else is rejected on write [R4].

**As built.** The core reads and writes the log, and a cut-off last line is dropped [BUILD-LOG:29] [core-trial:12]. The trial found a forged snapshot could rewrite history, and that a crash in the middle of an accented letter broke the book [core-trial:22] [core-trial:43]. R4 removes accented letters from storage [R4].

---

## 6. The .seq page (a view)

**Why.** The Director asked for "a new file type that holds one multifaceted page" [R3]. The spec already calls seqaddr a file type [seqAddr.md:7] [AGENTS.md:33].

**The book stays the real copy.** "the book is the real stored copy" [R3].

**A .seq page is a view.** It is "a view you export from a book and import back" [R3].

**Import is a proposal.** "import goes through the normal proposal queue" [R3].

**Nothing lost.** "Round trip book -> .seq -> book must be lossless" [R3].

**As built.** A builder lane is writing the reader, writer and round-trip tests in `crates/seqpage`, and nothing there is committed yet (git status, 2026-11-11 2:56 PM EST). *Open: what the file looks like inside [O22].*

---

## 7. The compute and its queue

**One compute per repository.** "There is one compute per repository, and it owns every book in it" [format.md:15].

**Reads are open.** "Anyone may read any face" [format.md:16].

**Writes are proposals.** "Writers submit a write to the compute's queue" [format.md:17].

**Only the compute writes.** "Agents, users and the app never touch book files" [format.md:18].

**First claim wins.** "proposals are approved one at a time, so the first claim on a `pack` wins" [format.md:42].

**Never guess.** "Anything the compute cannot resolve goes to the user and is never guessed" [format.md:131].

**The split of jobs.** "People authorize, models reason and propose, compute validates and executes" [AGENTS.md:42].

**A small fixed start.** The compute needs "a minimal, stable bootstrap contract that works before the kernel has loaded" [kernel-design.md:111]. *That file calls itself proposed [kernel-design.md:4].*

**Language.** The core and compute are in Rust, and the app is in TypeScript with Next.js [format.md:139-141].

**As built.** The Rust compute runs one queue with one writer, validates every proposal with the core, and appends with fsync [BUILD-LOG:53]. It follows the bootstrap steps and refuses to start if the kernel is damaged [BUILD-LOG:54]. Promoting needs an `approved_by` value, and R2 counts only with a trial reference [BUILD-LOG:59]. The app reads only through the compute [BUILD-LOG:6]. The core is not yet built for the browser (WebAssembly), a `7` [BUILD-LOG:66]. *Open: who counts as "a different view" for R2 [O1]? Who is allowed to do what [O15]?*

---

## 8. Finding (resolution order)

**Reading versus finding.** You only need the address rules to read an address [seqAddr.md:98].

**The order.** Finding looks up `book -> shelf -> desk -> kernel` [seqAddr.md:101].

**First match wins.** "The first match wins" [seqAddr.md:104].

**Live inheritance.** "Books follow the kernel live: anything not overridden locally is found in the kernel" [seqAddr.md:104].

**Never guess.** "If nothing is found, the address is elevated to the user, never guessed" [seqAddr.md:104].

**A local override.** A page in `0001-0099` in a book is "a local override of the inherited environment" [seqAddr.md:228]. Axiom 2 says a contradicting difference "needs a named override, approved by the authority above it" [Axioms.md:15].

**As built.** The core, compute and app all walk the four levels [BUILD-LOG:9] [core-trial:142]. Drafts are not inherited, so today the books inherit nothing from the kernel [BUILD-LOG:57]. *Open: are drafts found [O3]? Does an override replace a whole face or only its cards [O8]? What does a retired page answer [O21]?*

---

## 9. The workflow loop

**Its state.** The `.003` loop is "draft — Director review required; not live" [workflow-loop.003.md:3]. What the Director did approve is the S01-S12 directions [decisions.md:621]. *Open: [O7].*

**Why it exists.** It is "how work loops from a design to a build and back, so a model can run passes without history and a person can check every step" [workflow-loop.003.md:8].

**The loop.** `draft -> pack -> open -> return -> review -> closed` [workflow-loop.003.md:163]. "`closed` is the board label for the bare `05.NN` counter" [workflow-loop.003.md:166].

**How it ends.** The outcome is recorded apart from the tail: passed, failed, blocked, needs-authority or abandoned [decisions.md:629].

**Roles.** A person approves, a lead writes packs, a builder claims and builds, a reviewer from another view checks, and the compute records [workflow-loop.003.md:26-30]. "A lead is not authority" [workflow-loop.003.md:32].

**Approval is pinned.** The person approves "one identified N4 revision" [workflow-loop.003.md:88].

**Evidence.** A return cites the changed paths and the commit, with proof in proportion to risk [decisions.md:628].

**Code lives in the repo.** "code lives in the repo, not in the book" [workflow-loop.003.md:70].

**Limits on loops.** "1-3 passes is normal" [workflow-loop.003.md:258]. Pass 6 halts and goes to the authority [workflow-loop.003.md:267].

**As built.** The core has claims, and the first claim wins (HTTP 409) [BUILD-LOG:37] [BUILD-LOG:64]. A builder cannot review its own return [BUILD-LOG:64]. The trial found that anyone can do the compute-only steps, lint and close [core-trial:38-41]. That is a fix, because the spec is clear [workflow-loop.003.md:171] [workflow-loop.003.md:176].

---

## 10. Axioms

**What they are.** "The axioms give a model a different awareness: a large concept in a very small package" [Axioms.md:3]. "Axioms is the shape, seqaddr is the geometry" [AGENTS.md:27].

**The nine.**
1. Authority: "Authority is granted, never claimed" [Axioms.md:13].
2. Fractal: "Inherit what is agreed; write only the difference" [Axioms.md:15].
3. Leads: "Every piece of work has a lead" [Axioms.md:17].
4. Why: "A law without its why is incomplete" [Axioms.md:19].
5. Frame: "Know what the work aims at, and why, before doing it" [Axioms.md:21].
6. Lineage: "The past is not rewritten" [Axioms.md:23].
7. Missing: "Never invent it; unknown stays unknown" [Axioms.md:25].
8. Connection: "Agreement is not connection" [Axioms.md:27].
9. Trial: "Work is not right because you made it" [Axioms.md:29].

**How to cite them.** "A dot orders axioms in one piece" and "A comma splits pieces" [Axioms.md:5]. "A cite runs nothing and permits nothing" [Axioms.md:5].

**Before a write.** The cold set is `1.7.8`: authority, missing, connection [Axioms.md:9].

**At this stage.** "Approval without my eyes is fine for this stage of the work" [R2]. A face may be seated after a hostile trial from a different view, recorded as `approved-by: build-stage (R2)` [R2].

**As built.** Every kernel why cites its spec line, and missing whys are written `why: 4.7`, not made up [kernel-trial:136] [BUILD-LOG:21]. *Open: the axioms page number [O10], and whether a fresh sitting of the same model counts as a different view [O1].*
