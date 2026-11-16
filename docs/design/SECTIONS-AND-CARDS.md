# Sections, cards, and a copy check: a design plan

state: draft plan, `7` (open), `9` (not trialled). Not a ruling.
made: Mon 16 Nov 2026, Designer (design partner for Prima). Director: Matthew, the only approver.
why: Matthew held "refuse copied text" (fix 2) for design time [DIRECTOR-RULINGS.md:161] [DIRECTOR-RULINGS.md:162]. This plan is that design.
labels: "New" marks anything not in a Workshop source. Rulings are quoted, never made. Every question for Matthew uses his four-part form (t189u).
does not: edit any other file, change the core or the compute, or number a ruling.

---

## Plain-words summary

A page is mostly face 04, the part a person reads.

Face 04 is split into **sections**. A section is one piece of work, with a heading.

Some sections also have small **cards** on faces 01, 02 or 03. Those cards are for the model and the computer.

A section and its card share one name (its key). That name is how they find each other.

On normal pages, faces 01 and 02 hold only **key words**. A key word does not explain itself. It points to the one place where its meaning is written (the dictionary).

Face 03 can hold a **menu**. The menu lists every small piece on the page: each section, each card, and what it is. The computer writes the menu. Nobody types it.

Copying is the problem Matthew held back. Some copying is honest. Some is not.

Honest: pointing to a card instead of repeating it. Using the same key word as another page. Quoting someone, with a note saying where it came from.

Not honest: pasting the same words again and passing them off as new work. For example, a face 04 that just repeats face 01, or the same "why" pasted onto two cards.

The plan: the computer **refuses** a dishonest copy, **flags** a copy that is only partly the same, and **allows** links, shared key words and quotes with a source.

Three questions matter most. Should copies be refused or only flagged? May every page have a face 03 menu? And how does a section reuse another page's card, when links may only name pages?

---

## What Matthew said (R33, t192u, 12:06 PM EST)

Quoted exactly from `docs/spec/DIRECTOR-RULINGS.md` (Prima's entry, commit 865b880):

- **R33, 2 (held 7):** "So this is where sections and cards come in. A section is a piece of work in 04. cards exist in 01,02,03. So a menu from 03 can say what lives in small pieces on a page. Normally 01,02 aren't going to exist on normal pages othen then for key words. I think this might need some dev time." [DIRECTOR-RULINGS.md:161]. Read: "not yet approved. A section is a piece of work in face 04. Cards live in faces 01, 02, and 03, and a face 03 menu can say what small pieces live on a page. On normal pages, faces 01 and 02 usually hold only key words. The copy check needs design work against this before it is built. Held 7." [DIRECTOR-RULINGS.md:162]
- **R33, 1 (approved):** "Yes, books change through compute not by models. Models can be wrong and having them answer a question correctly 100% of the time can be an issue." [DIRECTOR-RULINGS.md:159]
- **R33, 3 and 4 (approved):** "I agree" [DIRECTOR-RULINGS.md:163]; "I agree." [DIRECTOR-RULINGS.md:165]

**Where Prima's short version differs from the file.** Her version says faces 01 and 02 "usually hold only key words". Matthew's words are stronger: 01 and 02 "aren't going to exist on normal pages" other than for key words [DIRECTOR-RULINGS.md:161]. The Read softens this to "usually" [DIRECTOR-RULINGS.md:162]. Her version also leaves out "I think this might need some dev time", and that the item is held 7 and "not yet approved".

---

## What exists today

- A card is a `##` heading. Its key is the heading in title form. "Keys are unique within a face. Cards with the same key on different faces are the same card." [decisions.md:298] [decisions.md:299] [decisions.md:300]
- A face's contents list is derived from its cards, never written by hand [decisions.md:301].
- Every 01 or 02 card has a 04 card with the same key, a `source:` line and a `why:` line [decisions.md:353] [decisions.md:354] [seqAddr.md:184].
- "The 04 body is not identical to the 01 body" is only a finding [decisions.md:355] [seqAddr.md:185].
- Key words are brands. The compute stores each in the dictionary, and reuses a matching meaning [decisions.md:360].
- The dictionary (page 0012, face 03) maps a word to its brand cards "and nothing more" [decisions.md:424]. A brand card lives on face 01 of the page that explains it [decisions.md:435].
- Face 03 is "the card menu" [seqAddr.md:152]. The `menu` card type has "entries derived by the compute" [decisions.md:516].
- Face 03 is allowed in normal books only on reserved pages 0001-0099 [decisions.md:404].
- "A 04 section may have a 01 card: a brief of how a model should understand it." [decisions.md:405] [seqAddr.md:186]. So the sources already call a 04 card a "section".
- Links name a page (address plus title), never a face, and give the current page [DIRECTOR-RULINGS.md:123] [DIRECTOR-RULINGS.md:152]. Every link has a back-link [seqAddr.md:251].
- Face 00 is "the registry, the place that lists the page's faces" [seqpage.md:81]; its `type` field names the page type [face00.md:61].
- Borrowed content is shown from its source as a derived line, never copied in (working path D403, not a ruling) [DESIGN.md:189].
- R31 layout: one folder per page, one file per face [DIRECTOR-RULINGS.md:142]. Face 00 holds the face list; the page index holds where each face sits [DIRECTOR-RULINGS.md:156].
- Tester (L4): the copy check is "a finding (a note), not a refusal", exact match only, face 01 only; nothing "compares one why with another" (docs/review/OUR-CODE-VS-CURSOR-LESSONS.md:86-88). A copied 04 and a reused why were approved and then seated by the Director token (same file, :103-118). The check is `crates/seqaddr-core/src/validate.rs:440-441`.

---

## 1. Sections and cards in the page folder

**Sections (face 04).** A section is a `##` heading in the face 04 file, with its body under it. This is today's 04 card shape [decisions.md:298] [seqAddr.md:186]. New: this plan uses "section" for a 04 card, and "card" for a card on 01, 02 or 03, to match Matthew's words.

**Cards (faces 01-03).** Each card is a `##` heading in its face's file: 01 for meaning, 02 for exact processes, 03 for operations and the menu [seqAddr.md:152].

**How they are linked.** A section and its cards share one key. Same key on different faces is the same card [decisions.md:300]. So `1024.04.jim` (section) and `1024.01.jim` (card) are one piece seen two ways. The section's `source:` line names its cards, for example `source: [01 / jim]` [seqAddr.md:184]. That written line is the connection; matching keys alone would be "agreement", not connection [Axioms.md:27].

**Where they sit (R31, R32).** In the page folder, all sections live in the one face 04 file, all 01 cards in the one face 01 file, and so on. New: the page index (page signpost) records, for each face file, where each card or section starts, so the compute opens one card without reading the whole face [DIRECTOR-RULINGS.md:156]. Face 04 history is kept the Google Docs way, as small changes [DIRECTOR-RULINGS.md:119].

**Office kinds (R31).** A sheet or document page is also face 04 [DIRECTOR-RULINGS.md:134]. New: a sheet's sections are its named tables; a document's sections are its headings. Where office content lives is an open question in SEQ-FILE-PLAN.md (C18).

**Axioms:** Fits axiom 2: one card rule for every face and every page [Axioms.md:15]. Fits axiom 8: the `source:` line is a written connection, not a match [Axioms.md:27]. Fits axiom 3: one face per lead (person 04, model 01, compute 03) [Axioms.md:17].

**Better:** Better than a new storage shape: it is the existing card rule, inside the R31 folder. Where we fall short: one file per face means a big face 04 holds many sections; the page index must point inside it, which is new and untested.

**Three leads:** The person reads sections in face 04 as plain headings. The model reads a section's 01 card (or key words) first, then the section only if needed. The compute keeps keys unique per face, checks every 01/02 key has a section, and records where each starts.

---

## 2. The face 03 menu

**What it lists.** Matthew: "a menu from 03 can say what lives in small pieces on a page" [DIRECTOR-RULINGS.md:161]. New: one `menu` card on face 03, with one line per piece: key, face, card type, a short label, and whether it points elsewhere (a link or a cite). For example:

```
## Menu
type: menu

jim       04 why    the section about Jim
jim       01 rule   key words: friend, work
kettle    04 why    how to boil water (quotes 10.11.21.0077.04.kettle)
```

**Who writes it.** Only the compute, derived from the cards, never by hand [decisions.md:301] [decisions.md:516]. It is rebuilt after each write to the page. It points; it never becomes what it points to [Axioms.md:27].

**Why it helps the copy check.** The menu shows, in one place, every piece that points elsewhere. A piece that repeats another without pointing is easy to spot.

**Where it is allowed (open).** Today face 03 is allowed in normal books only on pages 0001-0099 [decisions.md:404]. A menu on every page needs that rule widened for derived menus only (Question 2).

**Axioms:** Fits axiom 8: "a menu, a copy or a link never becomes what it points to" [Axioms.md:27]. Fits axiom 1: the compute writes it; nobody claims it [Axioms.md:13]. Tension with decisions.md:404 until Matthew answers Question 2 (axiom 1 [Axioms.md:13]).

**Better:** Better than a hand-kept table of contents, which drifts. Where we fall short: a menu on every page is one more file per page (Tester measured 3 to 7 times disk use for small files, SEQ-PROTO-RESULTS.md).

**Three leads:** The person sees what is on a page at a glance. The model reads the menu first and opens only the pieces it needs (the pyramid idea). The compute derives it, and refuses any hand edit to it.

---

## 3. Key words point to their meanings

**What Matthew said.** On normal pages, 01 and 02 exist only "for key words" [DIRECTOR-RULINGS.md:161].

**How a key word points (existing rule).** A key word is a brand, `word.NNN` [decisions.md:360]. The dictionary maps it to its brand card [decisions.md:424]. The brand card holds the meaning, on face 01 of the page that explains it [decisions.md:435]. So a key word never carries its meaning with it; it points to one place.

**On a normal page (new).** Each section may have one 01 card with the same key. That card holds only key words, each written as its brand, for example `friend.003, work.001`. No body text. The section keeps the full explanation in face 04.

**On system and kernel pages (new).** Faces 01 and 02 keep full cards (rules and schemas), as today [decisions.md:514].

**Tension.** Today a 01 card may be "a brief of how a model should understand it" [decisions.md:405]. Matthew's words narrow that on normal pages to key words only. This is not settled until R33, 2 is approved (Question 4).

**Axioms:** Fits axiom 2: a meaning is written once and reused, never copied [Axioms.md:15]. Fits axiom 8: each key word points to its brand card [Axioms.md:27]. Fits axiom 7: an unknown meaning is asked for, not guessed [Axioms.md:25] [decisions.md:440].

**Better:** Better than a 01 brief that repeats face 04 in short form, which is exactly the copy Tester found (L4). Where we fall short: the model loses its short brief on normal pages and must read face 04 or the key words' brand cards.

**Three leads:** The person writes face 04 only. The model proposes key words; it does not write meanings on normal pages. The compute stores each key word as a brand and links it to its brand card.

---

## 4. The copy check

**What counts as what (new).** Text is compared after a plain clean-up: lower case, spaces collapsed, punctuation dropped.

| Case | Example | Compute does | Why |
|---|---|---|---|
| Card reuse by pointing | a section's `source:` names another page's card; face 08 links that page | allow | one source, connected [Axioms.md:27] |
| Key word reuse | many pages use `friend.003` | allow | the dictionary exists for this [decisions.md:360] |
| Quote with a cite | text marked as a quote, with the source address | allow; listed in the menu | the source is named [Axioms.md:23] |
| A why quoting its governing rule, with a cite | a kernel why that is a cited spec line | allow | the builder already requires this (OUR-CODE-VS-CURSOR-LESSONS.md:89) |
| Section body the same as its own 01 or 02 body | Tester's run 1 | refuse | a copy, not an explanation [Axioms.md:15] |
| The same why on two cards | Tester's run 2 | refuse the second | a why must be its own reason [Axioms.md:19] |
| Unmarked copy of another piece (this page, this book, or inherited) | a pasted section with no cite | refuse: "link it or cite it" | a copy drifts; matching is not connection [Axioms.md:15] [Axioms.md:27] |
| Partial overlap (much shared, not the same) | half a section pasted | flag for review | may be honest; a person decides |
| Office kinds: sheet cells, code blocks | repeated numbers | exempt (not prose) | repeating a number is not a copied reason |

**Where it runs.** At the compute's one gate, on every merge into a draft and again on promote [DIRECTOR-RULINGS.md:160]. New: promote re-runs the check, so a Director promotion cannot seat a copy by accident, as it did in Tester's run 3 (OUR-CODE-VS-CURSOR-LESSONS.md:113-116). Seating a copy on purpose needs a named override (axiom 2 [Axioms.md:15]).

**How far it looks.** Within the page always. Within the book through a compute-only list of section fingerprints. Inherited pages only for quotes and cites. New.

**Thresholds.** Exact after clean-up: refuse. Partial overlap: flag. New: the partial measure (for example shared runs of eight words over half of the shorter text) is untested and must face a trial before it is trusted (axiom 9).

**Axioms:** Fits axiom 2: "Do not copy the parent" [Axioms.md:15]. Fits axiom 4: a pasted why is an invented reason [Axioms.md:19]. Fits axiom 8: "Agreement is not connection" [Axioms.md:27]. Fits axiom 1: the compute enforces; refusals give the reason [Axioms.md:13]. Axiom 9: the overlap rule is marked `9` until trialled [Axioms.md:29].

**Better:** Better than today's note-only check, which let a copy be seated (L4). Better than refusing every overlap, which would block honest quotes and shared key words. Where we fall short: a reworded copy (same meaning, new words) passes; only review catches it.

**Three leads:** The person gets a plain reason: "link it or cite it". The model must point or quote, never paste. The compute refuses exact copies, flags partial ones, and re-checks on promote.

**Trials before it is built (new).** Tester's runs 1-3 must now be refused; a quote with a cite must pass; a shared key word must pass; a half-pasted section must be flagged; a Director promote of a copy must be refused without an override.

---

## Questions for Matthew

Each uses his four-part form. The top three are marked **TOP**.

**Q1 (TOP). Should the computer refuse a copy, or only flag it?**
1. Question: When a section repeats its own face 01 text, or two cards share one why, should the computer refuse the write?
2. Proposed answer: Refuse exact copies (after clean-up) and unmarked copies of another piece. Flag partial overlaps for a person. Allow links, key words, and quotes with a cite.
3. Why: Tester showed a copied 04 and a reused why were approved and seated (OUR-CODE-VS-CURSOR-LESSONS.md:118). Who gets hurt: a reader who trusts a why that is really a paste. Refusing only clear cases keeps honest quoting.
4. Axioms checked: axiom 2 [Axioms.md:15] pass; axiom 4 [Axioms.md:19] pass; axiom 8 [Axioms.md:27] pass; axiom 9 [Axioms.md:29] tension (the partial-overlap rule is untried).

**Q2 (TOP). May every page have a face 03 menu?**
1. Question: Today face 03 is allowed in normal books only on pages 0001-0099. May every page have a face 03 menu, written only by the computer?
2. Proposed answer: Yes, for the derived `menu` card only. Other face 03 cards keep today's rule.
3. Why: You asked for "a menu from 03" on a page [DIRECTOR-RULINGS.md:161]. A derived menu adds no authored content, so it cannot drift.
4. Axioms checked: axiom 8 [Axioms.md:27] pass; axiom 1 [Axioms.md:13] tension (changes settled C6 [decisions.md:404]); axiom 2 [Axioms.md:15] pass.

**Q3 (TOP). How does a section reuse another page's card, when links name only pages?**
1. Question: Links name a page, never a face [DIRECTOR-RULINGS.md:123]. How does a section point to one card on another page?
2. Proposed answer: Face 08 links the page (address plus title, with a back-link). The section's `source:` line cites the card's address, for example `10.11.21.0077.01.kettle`, as a cite, not a link.
3. Why: R30 and R32 keep links at page level; a cite may name a card (SEQ-FILE-PLAN.md C10). Who gets hurt otherwise: readers who cannot find which card was reused.
4. Axioms checked: axiom 8 [Axioms.md:27] pass (link written both ways); axiom 6 [Axioms.md:23] pass; axiom 1 [Axioms.md:13] tension (depends on C10).

**Q4. On normal pages, are faces 01 and 02 key words only?**
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

- `docs/spec/DIRECTOR-RULINGS.md`: lines 119, 123, 134, 142, 152, 156, 159, 160, 161, 162, 163, 165.
- `docs/spec/decisions.md`: lines 298, 299, 300, 301, 353, 354, 355, 360, 404, 405, 424, 435, 440, 514, 516.
- `docs/spec/seqAddr.md`: lines 152, 184, 185, 186, 251.
- `docs/spec/seqpage.md`: line 81. `docs/spec/face00.md`: line 61. `docs/design/DESIGN.md`: line 189.
- `docs/spec/Axioms.md`: lines 13, 15, 17, 19, 23, 25, 27, 29.
- `docs/review/OUR-CODE-VS-CURSOR-LESSONS.md` (Tester, not a ruling): lines 86-89, 103-118.
- `crates/seqaddr-core/src/validate.rs:440-441` (read, not changed).
- `docs/design/SEQ-FILE-PLAN.md` (C10, C18) and `docs/design/SEQ-PROTO-RESULTS.md` (disk cost). Working paths, not rulings.
