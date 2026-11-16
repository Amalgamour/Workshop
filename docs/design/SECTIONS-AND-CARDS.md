# Sections, cards, and a copy check: a design plan

state: draft plan, `7` (open), `9` (not trialled). Not a ruling.
made: Mon 16 Nov 2026, Designer (design partner for Prima). Director: Matthew, the only approver.
revised: Mon 16 Nov 2026, after Director ruling R35 (t197u, 12:20 PM EST, entered by Prima in 8f6e9a7). See "Changes since 3c7401f".
why: Matthew held "refuse copied text" (fix 2) for design time [DIRECTOR-RULINGS.md:161] [DIRECTOR-RULINGS.md:162]. This plan is that design.
labels: "New" marks anything not in a Workshop source. Rulings are quoted, never made. Every question for Matthew uses his four-part form (t189u).
does not: edit any other file, change the core or the compute, or number a ruling. R35 updates decisions.md:404 for the menu card; that spec update is pending and is not made here.

---

## Plain-words summary

A page is mostly face 04, the part a person reads.

Face 04 is split into **sections**. A section is one piece of work, with a heading. A long page, like part of a story, may have dozens of sections.

Some sections also have small **cards** on faces 01, 02 or 03, on the same page. Those cards are for the model and the computer.

A section and its card share one name (its key). That name is how they find each other on the page.

On normal pages, faces 01 and 02 hold only **key words**. A key word does not explain itself. It points to the one place where its meaning is written (the dictionary).

Any page may have a **menu** on face 03. Matthew approved this. The menu lists every section and card on the page. The computer writes it. Nobody types it.

The menu saves work. The model reads the menu first, then loads only the sections it needs, instead of eating the whole page.

A section does not reuse another page's card. If it needs something from another page, it links to that page. The computer then serves just the piece that is needed. Matthew asked why a section would ever reuse a card; Prima said it should not. That is waiting for his word.

Copying is the problem Matthew held back. Some copying is honest. Some is not.

Honest: linking to a page. Using the same key word as another page. Quoting someone, with a note saying where it came from.

Not honest: pasting the same words again and passing them off as new work. For example, a face 04 that just repeats face 01, or the same "why" pasted onto two cards.

Who decides, in order: first the computer, by its rules. If its rules cannot decide, the model. If the model is not highly sure, a person. Every step is written in the page's log (face 09).

The open questions that matter most: what counts as "highly sure" for the model, whether every copy-check step goes in the page log, and whether a section ever needs anything from another page beyond a link.

---

## Changes since 3c7401f

- R35 folded in (quoted below). Q1 (refuse or flag) and Q2 (a face 03 menu on any page) are settled by R35.
- The copy check is rewritten around elevation: compute by its code first, then the model, then a person. Each case says who decides and what face 09 records.
- Cross-page card reuse is dropped, as Prima proposed (R35 item 3, held 7). A section links to the page by address plus title (R32); the compute serves just the needed piece through the face 03 menu. The `source:` line now names only cards on the same page; it is no longer used to cite another page's card. The copy-check row "card reuse by pointing" and the menu example's card cite are rewritten.
- New questions Q7 ("highly certain") and Q8 (face 09 logging of copy-check steps). Old Q3 is now held, not open; Q4-Q6 are unchanged.

---

## What Matthew said

Quoted exactly from `docs/spec/DIRECTOR-RULINGS.md`.

**R33, t192u, 12:06 PM EST (commit 865b880):**

- **R33, 2 (held 7):** "So this is where sections and cards come in. A section is a piece of work in 04. cards exist in 01,02,03. So a menu from 03 can say what lives in small pieces on a page. Normally 01,02 aren't going to exist on normal pages othen then for key words. I think this might need some dev time." [DIRECTOR-RULINGS.md:161]. Read: "not yet approved. A section is a piece of work in face 04. Cards live in faces 01, 02, and 03, and a face 03 menu can say what small pieces live on a page. On normal pages, faces 01 and 02 usually hold only key words. The copy check needs design work against this before it is built. Held 7." [DIRECTOR-RULINGS.md:162]
- **R33, 1, 3, 4 (approved):** "Yes, books change through compute not by models. Models can be wrong and having them answer a question correctly 100% of the time can be an issue." [DIRECTOR-RULINGS.md:159]; "I agree" [DIRECTOR-RULINGS.md:163]; "I agree." [DIRECTOR-RULINGS.md:165]

**R35, t197u, 12:20 PM EST (commit 8f6e9a7)** [DIRECTOR-RULINGS.md:176], answering this plan's Q1-Q3:

- **R35, 1, refuse or flag copies:** "Yes this is where the elevate comes in. If the comp can't solve according to it's code, it gives it to the model, if the model can't solve to a high degree of certainty. then it goes to the person." [DIRECTOR-RULINGS.md:177]. Read: "the proposal stands (refuse exact and unmarked copies, flag partial overlap, allow links, key words, and cited quotes), and anything uncertain is elevated: compute first by its code, then the model, then a person if the model is not highly certain." [DIRECTOR-RULINGS.md:178]
- **R35, 2, face 03 menu on every page:** "Yes of course, a page might contain the piece of a story. As such it might be broken into a number of sections perhaps dozens or more. So instead of the model eating everything it only gets what it needs." [DIRECTOR-RULINGS.md:179]. Read: "approved. Any page may have a compute-written face 03 menu of its sections, so a model loads only the sections it needs. This updates the pages 0001-0099 limit in decisions.md:404 for the menu card." [DIRECTOR-RULINGS.md:180]
- **R35, 3, a section reusing another page's card:** "Why would a section reuse a card?" [DIRECTOR-RULINGS.md:181]. Read: "not ruled; he questioned the premise. Prima answered (t197s757) that it shouldn't: a section links to the page (R32), and the compute serves only the needed piece. Held 7." [DIRECTOR-RULINGS.md:182]

**Where Prima's short versions differ from the file.**

- R33: her version (and the Read [DIRECTOR-RULINGS.md:162]) says faces 01 and 02 "usually hold only key words". Matthew's words are stronger: they "aren't going to exist on normal pages" other than for key words [DIRECTOR-RULINGS.md:161]. Her version also left out "I think this might need some dev time" and that the item was held 7.
- R35, 1: her summary gives only the elevation order. The Read also says "the proposal stands": refuse exact and unmarked copies, flag partial overlap, allow links, key words and cited quotes [DIRECTOR-RULINGS.md:178]. And in Matthew's words elevation starts only when the compute "can't solve according to it's code" [DIRECTOR-RULINGS.md:177]; her summary says the compute "decides first", which matches.
- R35, 2: her summary says this "updates decisions.md:404". The Read limits it: it updates that limit "for the menu card" [DIRECTOR-RULINGS.md:180]; other face 03 cards keep the 0001-0099 rule. Her summary also leaves out his reason, a page holding "the piece of a story" in "dozens or more" sections [DIRECTOR-RULINGS.md:179].
- R35, 3: matches. Matthew's words are only the question [DIRECTOR-RULINGS.md:181]; "it shouldn't" is Prima's answer, held 7 [DIRECTOR-RULINGS.md:182].

---

## What exists today

- A card is a `##` heading. Its key is the heading in title form. "Keys are unique within a face. Cards with the same key on different faces are the same card." [decisions.md:298] [decisions.md:299] [decisions.md:300]
- A face's contents list is derived from its cards, never written by hand [decisions.md:301].
- Every 01 or 02 card has a 04 card with the same key, a `source:` line and a `why:` line [decisions.md:353] [decisions.md:354] [seqAddr.md:184].
- "The 04 body is not identical to the 01 body" is only a finding [decisions.md:355] [seqAddr.md:185].
- Key words are brands. The compute stores each in the dictionary, and reuses a matching meaning [decisions.md:360].
- The dictionary (page 0012, face 03) maps a word to its brand cards "and nothing more" [decisions.md:424]. A brand card lives on face 01 of the page that explains it [decisions.md:435].
- Face 03 is "the card menu" [seqAddr.md:152]. The `menu` card type has "entries derived by the compute" [decisions.md:516].
- Face 03 is allowed in normal books only on reserved pages 0001-0099 [decisions.md:404]. R35, 2 updates this for the menu card [DIRECTOR-RULINGS.md:180]; the spec text is not yet changed.
- "A 04 section may have a 01 card: a brief of how a model should understand it." [decisions.md:405] [seqAddr.md:186]. So the sources already call a 04 card a "section".
- Face 00 is "the registry, the place that lists the page's faces" [seqpage.md:81]; its `type` field names the page type [face00.md:61].
- Borrowed content is shown from its source as a derived line, never copied in (working path D403, not a ruling) [DESIGN.md:189].
- R31 layout: one folder per page, one file per face [DIRECTOR-RULINGS.md:142]. Face 00 holds the face list; the page index holds where each face sits [DIRECTOR-RULINGS.md:156].
- Links name a page (address plus title), never a face, and give the current page [DIRECTOR-RULINGS.md:123] [DIRECTOR-RULINGS.md:152]. Every link has a back-link [seqAddr.md:251]. Titles may repeat at other addresses; the address tells pages apart [DIRECTOR-RULINGS.md:174].
- Tester (L4): the copy check is "a finding (a note), not a refusal", exact match only, face 01 only; nothing "compares one why with another" (docs/review/OUR-CODE-VS-CURSOR-LESSONS.md:86-88). A copied 04 and a reused why were approved and then seated by the Director token (same file, :103-118). The check is `crates/seqaddr-core/src/validate.rs:440-441`.

---

## 1. Sections and cards in the page folder

**Sections (face 04).** A section is a `##` heading in the face 04 file, with its body under it. This is today's 04 card shape [decisions.md:298] [seqAddr.md:186]. New: this plan uses "section" for a 04 card, and "card" for a card on 01, 02 or 03, to match Matthew's words.

**Cards (faces 01-03).** Each card is a `##` heading in its face's file on the same page: 01 for meaning, 02 for exact processes, 03 for operations and the menu [seqAddr.md:152].

**How they are linked, on one page.** A section and its cards share one key. Same key on different faces is the same card [decisions.md:300]. So `1024.04.jim` (section) and `1024.01.jim` (card) are one piece seen two ways. The section's `source:` line names its cards on this page, for example `source: [01 / jim]` [seqAddr.md:184]. That written line is the connection; matching keys alone would be "agreement", not connection [Axioms.md:27]. New: a `source:` line names only cards on the same page. It never names a card on another page.

**Across pages: a link, not a reused card (held 7, R35, 3).** New, as Prima proposed [DIRECTOR-RULINGS.md:182]: a section never reuses another page's card. When a section needs something another page explains, the page's face 08 links that page by address plus title, with a back-link (R32 [DIRECTOR-RULINGS.md:152]; [seqAddr.md:251]). When the model follows the link, the compute opens that page's face 03 menu and serves only the section or card that is needed. Nothing from the other page is copied in (axiom 2; D403 [DESIGN.md:189]). Held 7 until Matthew confirms.

**Where they sit (R31, R32).** All sections live in the one face 04 file, all 01 cards in the one face 01 file, and so on. New: the page index (page signpost) records where each card or section starts in its face file, so the compute opens one section without reading the whole face [DIRECTOR-RULINGS.md:156]. Face 04 history is kept the Google Docs way, as small changes [DIRECTOR-RULINGS.md:119].

**Office kinds (R31).** A sheet or document page is also face 04 [DIRECTOR-RULINGS.md:134]. New: a sheet's sections are its named tables; a document's sections are its headings. Where office content lives is open in SEQ-FILE-PLAN.md (C18).

**Axioms:** Fits axiom 2: one card rule for every face and page, and no copy of another page's card [Axioms.md:15]. Fits axiom 8: the `source:` line and the face 08 link are written connections, not matches [Axioms.md:27]. Fits axiom 3: one face per lead (person 04, model 01, compute 03) [Axioms.md:17].

**Better:** Better than reusing cards across pages, which would tie one page's words to another's and blur which page governs. Better than a new storage shape: it is the existing card rule, inside the R31 folder. Where we fall short: one file per face means a big face 04 holds many sections; the page index must point inside it, which is new and untested.

**Three leads:** The person reads sections in face 04 as plain headings, and follows links to other pages. The model reads a section's 01 card (or key words) first, follows links instead of copying, and loads other pages' pieces through their menus. The compute keeps keys unique per face, checks every 01/02 key has a section, refuses a `source:` line that names another page, and serves only the asked-for piece.

---

## 2. The face 03 menu (settled by R35, 2)

**Matthew's ruling.** "Yes of course, a page might contain the piece of a story. As such it might be broken into a number of sections perhaps dozens or more. So instead of the model eating everything it only gets what it needs." [DIRECTOR-RULINGS.md:179]. Read: any page may have a compute-written face 03 menu of its sections, "so a model loads only the sections it needs" [DIRECTOR-RULINGS.md:180].

**What it lists.** New: one `menu` card on face 03, with one line per piece: key, face, card type, a short label, its size, and whether it points elsewhere (a link or a cited quote). For example:

```
## Menu
type: menu

jim       04 why    the section about Jim          1.2 KB
jim       01 rule   key words: friend.003, work.001
chapter-3 04 why    the walk home                  4.8 KB  quotes page 10.11.21.0077.tea
```

**Who writes it.** Only the compute, derived from the cards, never by hand [decisions.md:301] [decisions.md:516]. It is rebuilt after each write to the page. It points; it never becomes what it points to [Axioms.md:27]. The page index says where each piece sits; the menu says what each piece is [DIRECTOR-RULINGS.md:156].

**How a model loads a page (lazy loading).** New: the model asks for the page; the compute returns the menu; the model asks for the sections it needs by key; the compute returns only those. A page with dozens of sections costs the model one menu plus a few sections, not the whole face.

**Spec update pending.** R35, 2 updates the 0001-0099 limit in decisions.md:404 for the menu card only [DIRECTOR-RULINGS.md:180]. Other face 03 cards keep today's rule. This plan does not edit decisions.md.

**Axioms:** Fits axiom 8: "a menu, a copy or a link never becomes what it points to" [Axioms.md:27]. Fits axiom 1: Matthew approved it; the compute writes it [Axioms.md:13]. Fits axiom 5: the model works inside a frame of only the pieces it needs [Axioms.md:21].

**Better:** Better than a hand-kept table of contents, which drifts. Better than giving the model the whole page. Where we fall short: a menu on every page is one more piece per page (Tester measured 3 to 7 times disk use for small files, SEQ-PROTO-RESULTS.md), and the size column must be kept honest by the compute.

**Three leads:** The person sees what is on a page at a glance. The model reads the menu first and opens only the pieces it needs. The compute derives the menu, refuses any hand edit to it, and serves pieces by key.

---

## 3. Key words point to their meanings

**What Matthew said.** On normal pages, 01 and 02 exist only "for key words" [DIRECTOR-RULINGS.md:161].

**How a key word points (existing rule).** A key word is a brand, `word.NNN` [decisions.md:360]. The dictionary maps it to its brand card [decisions.md:424]. The brand card holds the meaning, on face 01 of the page that explains it [decisions.md:435]. So a key word never carries its meaning with it; it points to one place. This is not card reuse: the dictionary is the one lawful index for meanings.

**On a normal page (new).** Each section may have one 01 card with the same key. That card holds only key words, each written as its brand, for example `friend.003, work.001`. No body text. The section keeps the full explanation in face 04.

**On system and kernel pages (new).** Faces 01 and 02 keep full cards (rules and schemas), as today [decisions.md:514].

**Tension.** Today a 01 card may be "a brief of how a model should understand it" [decisions.md:405]. Matthew's words narrow that on normal pages to key words only. Not settled until R33, 2 is approved (Q4).

**Axioms:** Fits axiom 2: a meaning is written once and reused, never copied [Axioms.md:15]. Fits axiom 8: each key word points to its brand card [Axioms.md:27]. Fits axiom 7: an unknown meaning is asked for, not guessed [Axioms.md:25] [decisions.md:440].

**Better:** Better than a 01 brief that repeats face 04 in short form, which is exactly the copy Tester found (L4). Where we fall short: the model loses its short brief on normal pages and must read face 04 or the key words' brand cards.

**Three leads:** The person writes face 04 only. The model proposes key words; it does not write meanings on normal pages. The compute stores each key word as a brand and links it to its brand card.

---

## 4. The copy check, by elevation (settled by R35, 1)

**Matthew's ruling.** "Yes this is where the elevate comes in. If the comp can't solve according to it's code, it gives it to the model, if the model can't solve to a high degree of certainty. then it goes to the person." [DIRECTOR-RULINGS.md:177]. Read: the proposal stands, "and anything uncertain is elevated: compute first by its code, then the model, then a person if the model is not highly certain." [DIRECTOR-RULINGS.md:178]

**Text is compared after a plain clean-up** (new): lower case, spaces collapsed, punctuation dropped.

**Step 1: the compute, by its code.** It decides every case its rules can settle:

| Case | Compute decides | Why |
|---|---|---|
| Key word written as its brand | allow | the dictionary exists for this [decisions.md:360] |
| Link to a page (face 08, address plus title, back-link) | allow | one source, connected [Axioms.md:27] |
| Quote, marked, whose cite names a page that exists | allow | the source is named [Axioms.md:23] |
| A why quoting its governing rule, with a cite | allow | the builder already requires this (OUR-CODE-VS-CURSOR-LESSONS.md:89) |
| Section body the same as its own 01 or 02 body | refuse | a copy, not an explanation [Axioms.md:15] |
| The same why on two cards | refuse the second | a why must be its own reason [Axioms.md:19] |
| Exact copy of another piece (this page, this book, inherited), unmarked | refuse: "link it or quote it" | matching is not connection [Axioms.md:27] |
| `source:` line naming a card on another page | refuse: "link the page" | cross-page card reuse is dropped (held 7) |
| Partial overlap, or a quote whose cite does not resolve | cannot decide: elevate | needs judgement |
| Sheet cells, code blocks | exempt (Q6) | a repeated number is not a copied reason |

**Step 2: the model.** It gets only what the compute could not settle, with both texts and the overlap. It answers allow, refuse, or "add a cite", with a reason naming the rule. If it is highly certain (Q7), that answer stands. If not, it elevates.

**Step 3: a person.** The page's owner, or whoever holds authority over the page (axiom 1), sees both texts, the compute's measure and the model's reason, and decides. Their answer stands.

**While a case is elevated,** the write waits as a draft, not live (R8 [DIRECTOR-RULINGS.md:35]), and the draft shows why it is waiting: "elevated, copy check" (R5 [DIRECTOR-RULINGS.md:29]).

**How each step is logged on face 09** (new): one line per step, written only by the compute.

```
copy-check  compute  refused    rule: same-why       with: 1024.04.kettle
copy-check  compute  elevated   overlap 62%          with: 0077.04.walk
copy-check  model    elevated   not highly certain   reason: may be a paraphrase of a quote
copy-check  person   allowed    by: matthew          reason: his own earlier text, cite added
```

Allowed writes the compute settles alone get no extra line beyond the normal write line. Refusals and every elevated step are logged, so the trail shows who decided and why. Whether refusals belong in face 09 is still open in the file plan (SEQ-FILE-PLAN.md C2); this design proposes yes for copy-check steps (Q8).

**On promote.** The compute re-runs step 1, so a promotion cannot seat a copy by accident, as the Director token did in Tester's run 3 (OUR-CODE-VS-CURSOR-LESSONS.md:113-116). Seating a copy on purpose needs a named override (axiom 2 [Axioms.md:15]; Q5).

**How far it looks.** Within the page always. Within the book through a compute-only list of section fingerprints. Inherited pages only for quotes and cites. New.

**What it cannot catch.** A reworded copy (same meaning, new words) passes step 1. The model may catch it at step 2 only if a write is elevated for another reason; otherwise review must.

**Axioms:** Fits axiom 1: the order is Matthew's; compute enforces, the model works within it, a person holds final authority [Axioms.md:13]. Fits axiom 2: "Do not copy the parent" [Axioms.md:15]. Fits axiom 4: a pasted why is an invented reason [Axioms.md:19]. Fits axiom 8: "Agreement is not connection" [Axioms.md:27]. Fits axiom 6: every decision is a logged step [Axioms.md:23]. Axiom 9: the overlap measure and "highly certain" are untried, marked `9` [Axioms.md:29].

**Better:** Better than today's note-only check, which let a copy be seated (L4). Better than sending every overlap to a person, which wastes their time; most cases end at step 1. Where we fall short: "highly certain" is not defined yet (Q7), and reworded copies slip through.

**Three leads:** The person decides only what the compute and model could not, and sees the full trail. The model judges overlaps, gives a reason, and says plainly when it is not sure. The compute settles clear cases by rule, elevates the rest, holds the write as a draft, and logs every step.

**Trials before it is built (new).** Tester's runs 1-3 must now be refused at step 1; a cited quote must pass; a shared key word must pass; a half-pasted section must reach step 2; a model that is not highly certain must reach step 3; a `source:` line naming another page must be refused; a Director promote of a copy must be refused without an override; every step must leave its face 09 line.

---

## Questions for Matthew

Each uses his four-part form. The top three are marked **TOP**.

**Settled by R35.** Q1 (refuse or flag): refuse exact and unmarked copies, flag partial overlap, allow links, key words and cited quotes, and elevate anything uncertain: compute, then model, then person [DIRECTOR-RULINGS.md:178]. Q2 (a face 03 menu on any page): approved, for the menu card [DIRECTOR-RULINGS.md:180].

**Held 7 (R35, 3).** Q3 (a section reusing another page's card): Matthew asked "Why would a section reuse a card?" [DIRECTOR-RULINGS.md:181]. Prima answered that it shouldn't; this plan is written that way (Part 1) and waits for his confirmation [DIRECTOR-RULINGS.md:182].

**Q7 (TOP). What does "highly certain" mean for the model?**
1. Question: The model passes a copy case to a person when it is not highly certain. How do we tell when it is?
2. Proposed answer: The model is highly certain only when it can name the exact rule and the exact source text behind its answer, and a second model pass from another view (a hostile check) gives the same answer. If either fails, it goes to a person. A number the model gives about its own confidence is not used.
3. Why: A model's own sense of certainty is easy to fool; its maker is "the easiest one to convince". Two views that agree, each with a named reason, are a real check. Who gets hurt otherwise: a person whose honest quote is refused, or a reader who trusts a copy.
4. Axioms checked: axiom 9 [Axioms.md:29] pass (a hostile pass from another view); axiom 4 [Axioms.md:19] pass (a named reason); axiom 1 [Axioms.md:13] pass (the person keeps the last word); axiom 3 [Axioms.md:17] tension (a second model pass costs time and money on every elevated case).

**Q8 (TOP). Should every copy-check step be written in the page's log (face 09)?**
1. Question: Should face 09 record each copy-check refusal and each elevation step (compute, model, person), even though a refused write changes nothing?
2. Proposed answer: Yes for copy-check steps: one line per step, written only by the compute. Allowed writes the compute settles alone need no extra line.
3. Why: Elevation hands a decision from one lead to another; without a written trail nobody can see who decided or why. Who gets hurt otherwise: the person asked to decide without seeing what the model said.
4. Axioms checked: axiom 6 [Axioms.md:23] pass ("A change that is not recorded did not happen"); axiom 1 [Axioms.md:13] pass; axiom 2 [Axioms.md:15] tension (the file plan's C2 proposal logs only halts, so this would be a second rule for one log until C2 is answered).

**Q4 (TOP). On normal pages, are faces 01 and 02 key words only?**
1. Question: Today a 01 card may be a short brief. You said 01 and 02 "aren't going to exist on normal pages" other than for key words. Is that the rule?
2. Proposed answer: Yes on general pages: a 01 card holds only key words (brands). System and kernel pages keep full 01 and 02 cards.
3. Why: A short brief is a second copy of face 04 and drifts. Key words point to one meaning.
4. Axioms checked: axiom 2 [Axioms.md:15] pass; axiom 3 [Axioms.md:17] tension (the model loses its brief); axiom 8 [Axioms.md:27] pass.

**Q5. May a promotion seat a copy?**
1. Question: In Tester's run 3 the Director token seated a copied section. Should promotion re-run the copy check?
2. Proposed answer: Yes. A copy can be seated only with a named override written on the section.
3. Why: Seating makes the copy law for everyone downstream. A named override keeps the choice visible.
4. Axioms checked: axiom 1 [Axioms.md:13] pass; axiom 2 [Axioms.md:15] pass (named override); axiom 6 [Axioms.md:23] pass.

**Q6. Are sheet cells and code blocks exempt from the copy check?**
1. Question: Office pages repeat numbers and code often. Should the copy check skip them?
2. Proposed answer: Yes, skip cells and code blocks; check prose and whys only.
3. Why: A repeated number is not a copied reason. Refusing it would block normal sheets.
4. Axioms checked: axiom 4 [Axioms.md:19] pass; axiom 9 [Axioms.md:29] tension (untried on real sheets).

---

## Sources

- `docs/spec/DIRECTOR-RULINGS.md`: lines 29, 35, 119, 123, 134, 142, 152, 156, 159, 161, 162, 163, 165, 174, 176, 177, 178, 179, 180, 181, 182.
- `docs/spec/decisions.md`: lines 298, 299, 300, 301, 353, 354, 355, 360, 404, 405, 424, 435, 440, 514, 516.
- `docs/spec/seqAddr.md`: lines 152, 184, 185, 186, 251.
- `docs/spec/seqpage.md`: line 81. `docs/spec/face00.md`: line 61. `docs/design/DESIGN.md`: line 189.
- `docs/spec/Axioms.md`: lines 13, 15, 17, 19, 21, 23, 25, 27, 29.
- `docs/review/OUR-CODE-VS-CURSOR-LESSONS.md` (Tester, not a ruling): lines 86-89, 103-118.
- `crates/seqaddr-core/src/validate.rs:440-441` (read, not changed).
- `docs/design/SEQ-FILE-PLAN.md` (C2, C18) and `docs/design/SEQ-PROTO-RESULTS.md` (disk cost). Working paths, not rulings.
