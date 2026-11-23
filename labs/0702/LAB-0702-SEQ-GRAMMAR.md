# LAB 0702: the seq grammar lab

Page: 90.50.10.0702. Builder: Claude. Checker: Codex, by hand.
Status: `9`. Nobody has run a hostile trial on this version yet (Axioms.md:29@8e96151d).
Why: t451u, quoted on face 01. Matthew: "We have a lot to learn about axioms, designing and building our grammar out of seqaddr. How a .seq file should work."

**Versions.** This file has three versions so far. Each is a new step; older text stays in git history (Axioms.md:23).
- Pass 05.01 (commit 56f89178): the first version. It closed failed on Codex's cross-check (page 0702 face 05, signoff entry 10).
- Pass 05.02 (commit ba9a5b71): it closed failed on Codex's manual check, 4 met and 3 not met (page 0702 face 05, check entry 18, signoff entry 19).
- Pass 05.03 (this version, 2026-11-23): made from that check. Line cites in the 05.03 pack (lab :205, :231-232, :343) are lines of ba9a5b71.

What changed in pass 05.03:
1. The text productions behind `why-draft-v` and `stamp-v` are defined from the code (2.4).
2. The registry row lists `counters :=` for face 00 counter history (2.4; derive.rs:247-249).
3. The stamp-against-replay note no longer calls the booked body imported (3.4; import.rs:45-51, :64-87).
4. Open conflicts O2 and O6 are narrowed. O9 moves to a new "parked" table (5.3, P1). The R16 dictionary exception is a new open conflict (O11).
5. Q2 is split: R9's general rule is answered, and the R16 exception stays open.
6. Q6 gives the exact note fallback (derive.rs:137-138).
7. LESSONS.md lessons 3, 4, 6 and 7 are tightened. The evidence for lessons 6 and 7 is saved in labs/0702/EVIDENCE-0703-p1-session.txt.

What changed in pass 05.02, and still holds:
1. The entry-number rule is restated (2.3, item 2).
2. The claim about body checks is fixed (2.3, item 5).
3. Derived values now have a value grammar (2.4).
4. New coverage: escaped keys and decoded ASCII checks (2.5), and stamp against replay (3.4).
5. Section 5 is split into superseded text and real open conflicts.
6. Q2, Q4, Q5, Q6 and Q7 are marked answered.
7. LESSONS.md is new, beside this file.

How to read the cites:
- A cite written `path:line` means that line at build commit 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a (origin/prima/build), read with `git show 8e96151d:<path>`.
- In pass 05.02 I checked that docs/spec, crates/seqpage and crates/seqaddr-core are unchanged between 8e96151d and the branch tip 78101fe6. `git diff --stat` printed nothing. So the cites hold at both.
- `seqpage.md`, `seqAddr.md`, `face00.md`, `SEQ-GUIDE.md`, `seqpage-QUESTIONS.md`, `KERNEL-FILE-TITLES.md`, `Axioms.md` and `DIRECTOR-RULINGS.md` are under docs/spec/.
- `PLAN`, `TEST`, `TEST-2`, `PROTO` and `CITE-DRAFT` are docs/design/SEQ-FILE-PLAN.md, SEQ-FILE-PLAN-TEST.md, SEQ-FILE-PLAN-TEST-2.md, SEQ-PROTO-RESULTS.md and AXIOM-CITE-GRAMMAR-draft-t383u.md.
- Code is cited by file name: `parse.rs`, `derive.rs` and `text.rs` are under crates/seqpage/src/; `state.rs`, `tail.rs`, `addr.rs`, `face.rs` and `validate.rs` are under crates/seqaddr-core/src/.
- Example files are named by their path under docs/spec/examples/.

Who said what:
- A line marked **Claude proposal** is my own reading. It is not a source and not a ruling.
- Codex's cross-check is cited from its checker note in page 0702 face 05 (signoff entry 10) and from the pass 05.02 pack.
- Matthew did not talk the design through with me in either pass, so this report records none of his words directly.

---

## 0. Sources read

Commit: 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a. Fetched from origin/prima/build. The tip is 78101fe6, and the paths cited here are unchanged there.

| Source | At 8e96151d | Lines | Read |
|---|---|---|---|
| docs/spec/Axioms.md | present | 29 | read in full. Its body matches the kit's docs/AXIOMS.md. |
| docs/spec/seqpage.md | present | 263 | read in full |
| docs/spec/seqpage-QUESTIONS.md | present | 48 | read in full |
| docs/spec/SEQ-GUIDE.md | present | 609 | read in full |
| docs/spec/face00.md | present | 478 | read in full |
| docs/spec/KERNEL-FILE-TITLES.md | present | 62 | read in full |
| docs/spec/seqAddr.md | present | 364 | read in full |
| docs/spec/DIRECTOR-RULINGS.md | present | 204 | pass 05.02: read lines 1-45, 74-92, 100-126 and 176-192 (R1-R12, R19, R21-R23, R25-R30, R35, R36, R37 heading) |
| crates/seqpage/src/parse.rs | present | 461 | pass 05.02: read lines 34-35, 78-92, 255-280 and 360-372 |
| crates/seqpage/src/derive.rs | present | 259 | pass 05.02: read lines 18-20, 54-145 and 155-259 |
| crates/seqpage/src/text.rs | present | - | pass 05.02: read lines 60-152 |
| crates/seqaddr-core/src/state.rs | present | 686 | pass 05.02: read lines 600-635 |
| crates/seqaddr-core/src/tail.rs | present | - | pass 05.02: read lines 54-66 |
| crates/seqaddr-core/src/addr.rs | present | - | pass 05.02: read lines 136-156 |
| crates/seqpage/src/import.rs | present | - | pass 05.03: read lines 40-90 |
| crates/seqaddr-core/src/cards.rs | present | - | pass 05.03: read lines 77-87 and 157-181 |
| src/git.rs (the wf kit, at a823ee28) | present | - | pass 05.03: read lines 100-130, for lesson 6 |
| crates/seqaddr-core/src/face.rs, validate.rs | present | - | pass 05.02: one grep each (face.rs:101, :103; validate.rs:40-42) |
| docs/design/SEQ-FILE-PLAN.md | present | 1138 | read in part: lines 1-120, 209-488, 630-706 and 942-1112 |
| docs/design/SEQ-FILE-PLAN-TEST.md | present | 332 | read in part: headings, verdict, 114-134 and 291-312 |
| docs/design/SEQ-FILE-PLAN-TEST-2.md | present | 267 | read in part: headings, verdict, 122-144 and 191-200 |
| docs/design/SEQ-PROTO-RESULTS.md | present | 169 | read in part: 1-28 and 144-169 |
| docs/design/AXIOM-CITE-GRAMMAR-draft-t383u.md | present | 82 | read in full |
| examples/face00/10.11.40.1001.cats.seq | present | 48 | read line by line (example A) |
| examples/10.11.30.1501.timer.seq | present | 168 | read line by line (example B) |
| examples/proposals/10.11.21.1001.bob.seq | present | 83 | read line by line (example C) |
| examples/real/10.11.21.1001.bob.seq | present | 154 | pass 05.02: read lines 1-40 and 75-100 (section 3.4) |
| examples/real/README.md | present | 35 | pass 05.02: read in full |
| the other 7 example `.seq` files | present | - | listed only, not read line by line |

No named source is missing. In this version I did not run `seqpage check` or any other code. Where a rule is cited to code, it is my reading of that code.

---

## 1. What a .seq file is

**What it holds.** A `.seq` file holds one page with all its faces, as plain text a person can read top to bottom (seqpage.md:11; SEQ-GUIDE.md:14-16). It holds only the page's own entries from its own book. Inherited faces are not in it (seqpage-QUESTIONS.md:11-12, S2, provisional).

**It is a view.** R3 made the book the real copy and the `.seq` file a view you export and import back (DIRECTOR-RULINGS.md:12; seqpage.md:13).
- Import is only a proposal: "Importing never writes a book" (seqpage.md:14, :215).
- The round trip is lossless (seqpage.md:15).
- A re-export only adds lines, except derived lines (seqpage.md:16).
- R26 later updated R3: "The stored form is today's small files. A whole-book .seq file is an export made from them" (DIRECTOR-RULINGS.md:103-106). So the store is now the small files, not one book file. A page `.seq` is still a view, now of that store.
- seqpage.md:13 still has the R3 wording. That is stale text (section 5.1, S1), not an open conflict.

**One page per file, or not.** The spec's page file holds one page (seqpage.md:11). R26 adds a second shape: the whole-book `.seq` export (DIRECTOR-RULINGS.md:106; PLAN:247). The kernel keeps its sources as one face of one page per `.md` file (KERNEL-FILE-TITLES.md:11-15). How the two `.seq` shapes are named and told apart is open (section 5.2, O1).

**How it is named.**
- The form is `DD.SS.BB.PPPP.title.seq`, or `DD.SS.BB.PPPP.seq` with no title (seqpage.md:21-22). The title comes from face 00 (seqpage.md:25).
- If the title in the name differs from the stamp, the mismatch is elevated. If the address is wrong, that is an error (seqpage.md:27).
- Page 0000 never has a title in its name (KERNEL-FILE-TITLES.md:19).

**Who writes it.**
- The compute writes it on export, including every `:=` line (seqpage.md:177, :206, :237-238).
- A person may write `new` blocks by hand and leave out derived lines (seqpage.md:178).
- A person may hand-write a file for a page that does not exist yet (seqpage-QUESTIONS.md:23, S5).
- A `new` block cannot carry `at`, `by` or the other compute stamps. The proposer is named at import (seqpage.md:148, :239).

**Plain characters.** The file is printable ASCII 0x20-0x7E plus newline (seqpage.md:31, R4). The reader refuses the first other character (parse.rs:86-88). Section 2.5 covers values that hide a character inside a JSON escape. R27 lets stored faces other than 04 be binary (DIRECTOR-RULINGS.md:108-111). Whether that reaches the `.seq` view is open (section 5.2, O2).

---

## 2. Grammar

### 2.1 The address form

The axes, from highest to lowest (seqAddr.md:14-22):

| Part | Width | Rule |
|---|---|---|
| desk `DD` | 2 digits | seqAddr.md:18 |
| shelf `SS` | 2 | seqAddr.md:19 |
| book `BB` | 2 | seqAddr.md:20 |
| page `PPPP` | 4 | the only 4-digit axis, so it anchors reading (seqAddr.md:21, :71) |
| face `FF` | 2 | seqAddr.md:22 |
| counter `NN` | 2, 01-98 | not an axis; it attaches to a face (seqAddr.md:24). There is no `FF.00` or `FF.99` (R9, DIRECTOR-RULINGS.md:37-38). |
| tail | word | page and face: `draft`, `retired`. Counter: `draft`, `pack`, `open`, `return`, `review`; a bare counter means closed (seqAddr.md:126-128). |

The formal grammar is at seqAddr.md:265-283:
- `page-end = face-part / title [ "." page-tail ] / page-tail` (:269)
- `face-part = face [ "." counter ] [ "." tail ] [ "." card [ "." brand ] ]` (:271)
- `active-rel = "." face-part` (:270)

The rules it does not express are at :287-291. The rule that "A counter requires its face's `00` board" (:288) is superseded by R9 (section 5.1, S2).

Other address rules:
- Axiom chains are never addresses (:293).
- Work starts at 10 on desk, shelf and book (:320).
- Pages 0000-0099 are reserved (:322).
- Labs sit on 0701-0798 (:351).

Inside a `.seq` file every address is full form. Block headers and section headers carry full addresses (seqpage.md:106, :121, :130-131), and models always write full addresses (seqAddr.md:95).

### 2.2 The line kinds

The first characters of a line decide its kind (seqpage.md:47-60):

| Starts with | Kind | Rule |
|---|---|---|
| `seqpage 1` | magic line, line 1 only | seqpage.md:51 |
| `= ` | face section: `= FF name DD.SS.BB.PPPP.FF` | seqpage.md:52, :106 |
| `== ` | counter section: `== FF.NN address` | seqpage.md:53, :121 |
| `--- ` | block header: `--- @N op address` or `--- new op address` | seqpage.md:54, :130-131 |
| `key: ` | field | seqpage.md:55, :145 |
| `key := ` | derived line, under a section or block header | seqpage.md:56, :177 |
| `\|` | body line | seqpage.md:57, :166 |
| `~ history` / `~ end` | history start / file end | seqpage.md:58 |
| `@` | history line `@N op address` | seqpage.md:59, :199 |
| (empty) | separator | seqpage.md:60 |

Any other line is refused (seqpage.md:62).

The file order:
1. The magic line.
2. The registry section, first and only once (seqpage.md:81-82).
3. The other faces in number order, with counters in number order under their face (seqpage.md:107, :121).
4. Inside each section, booked blocks in book order, then `new` blocks (seqpage.md:135-136).
5. `~ history`, then `~ end`, with nothing after it (seqpage.md:202).

Fields:
- The ops are listed at seqpage.md:133.
- Field order is at seqpage.md:146.
- A booked block must have `at` and `by` (seqpage.md:147).
- Each value has one canonical form (seqpage.md:152-155; text.rs:111-146).

Body:
- Body lines carry the face's Markdown, and cards are its `##` headings (seqpage.md:167; seqAddr.md:168-169).
- Face 00's body is a front-matter stamp plus a `## Registry` card. This layout is a draft (face00.md:28-32, F9 at :475).

Where derived lines may appear is in section 2.4.

### 2.3 How a line refers to another page or line

1. **The block address.** A block's address must be on this page and in its own section (seqpage.md:134). A block cannot write to another page.
2. **Entry numbers** (restated in pass 05.02). Each booked entry `@N` has exactly one booked block (`--- @N op address`) and exactly one matching history line (`@N op address`). The two carry the same op and address. Blocks keep book order inside their section, and history lines are in book order across the page (seqpage.md:135, :199-201).
   Other lines may refer to the number without breaking that rule:
   - `source :=` lists the section's entry numbers (derive.rs:168-170, :216, :230, :255).
   - A `cites:` field may name an entry (timer.seq:51 `cites: 11`).
   - A `new` block has no number and no history line (seqpage.md:201).

   *Pass 05.01 said "An entry number appears once in the file". That was wrong: the number appears in a header, in a history line, and in any line that refers to it.*

   Open: may `cites:` name an entry on another page (Q10)?
3. **The lineage line.** `lineage :=` writes the page's lookup chain (seqpage.md:88; derive.rs:159-166; addr.rs:137-149). Section 2.4 gives its value form. Face 08 links are left out (S3, seqpage-QUESTIONS.md:16).
4. **Links between pages.** Links sit on face 08 and are written both ways (seqAddr.md:157, :251). How the compute holds them is not designed (seqAddr.md:302).
   R30 and R32 say a link names a page (address plus title), never a face, and gives the current page (DIRECTOR-RULINGS.md:123-125, :150; PLAN:643). The `.seq` grammar has no line kind for a link. A link is text in a face 08 body.
5. **The body, and references inside it** (fixed in pass 05.02).
   - Body text is not read as file structure. Every body line is prefixed, "so nothing in a body can be mistaken for structure" (seqpage.md:169).
   - The body is still checked:
     - a block's `cards :=` must match the body's `##` cards (seqpage.md:186; parse.rs:366-370);
     - the whole file, body included, passes R4 (parse.rs:86-88);
     - import compares a booked body with the book's entry (seqpage.md:214).
   - The core also knows `source` as a field of `schema` and `why` cards (face.rs:101, :103).
   - What I did not find is a check that resolves a reference written in a body, such as `source: [01 / Timer]` (timer.seq:73; seqAddr.md:179). I grepped crates/seqpage and crates/seqaddr-core for such a check and found none. That bracket form is not in the address grammar (seqAddr.md:265-283).

   *Pass 05.01 said "The file never checks body text". That was too broad.*

   Full card addresses in a body, such as `10.11.21.1001.01.bob` (proposals/bob.seq:77), are in the grammar (seqAddr.md:111, :271).
6. **Axiom cites.** An `axioms:` field holds a chain (Axioms.md:5; seqAddr.md:172). The proposed cite grammar (CITE-DRAFT:37-40) is a draft (CITE-DRAFT:5).
7. **Lines in other files.** No line kind points at a line in another file. Entry numbers are the only line-level references.

### 2.4 Derived lines and their value grammar (new in pass 05.02)

Where derived lines may appear (seqpage.md:183-186; derive.rs:195-256):

| Section | Lines, in the order derive.rs writes them |
|---|---|
| registry (face 00) | `title`, `state`, `registry`, `why-draft` (only while face 00 is in draft, derive.rs:204-207), `faces`, `type`, `axioms`, `lineage`, `kind` (pages 0000 and 0001-0009 only), `source`, then `counters` (only when face 00 has counter history; derive.rs:247-249 keeps it on face 00 "for losslessness" although the core does not treat face 00 counters as legal) |
| face | `state`, `why-draft` (only while in draft), `source`, `counters` (only when the face has counters) |
| counter | `state`, `source` |
| block | `cards` (any other key under a block is refused, parse.rs:366-368) |

The value grammar below is a **Claude proposal**. It is written from the code that prints each value, in the style of seqAddr.md:265-283. Where the code and seqpage.md agree, both are cited.

```
none          = "-"                                  ; derive.rs:20, seqpage.md:188
unknown       = "7"                                  ; derive.rs:18, seqpage.md:188
book-addr     = desk "." shelf "." book              ; always full form (derive.rs:216 prints page.book)
page-addr     = book-addr "." page
entry-ref     = "@" 1*DIGIT

source-v      = "book" SP book-addr *( SP entry-ref )          ; derive.rs:168-170, :216, :230, :255
lineage-v     = page-addr 1*( " < " book-addr )                ; derive.rs:160-166
                ; the books are: own book, DD.SS.00, DD.00.00, 00.00.00, with repeats dropped (addr.rs:138-148)
page-state-v  = "live" / "draft" / "retired" / none / unknown   ; derive.rs:64-70, :198
slot-v        = "absent" / "draft" / "seated" / "seated+draft" / "retired" / unknown   ; derive.rs:54-62
faces-v       = none / face-state *( ", " face-state )          ; derive.rs:88-108
face-state    = face SP ( slot-v / "counted" )                  ; "counted" when the face has a counter (derive.rs:99-100)
counters-v    = unknown / counter-state *( ", " counter-state ) ; derive.rs:232-243
counter-state = counter SP ( board-word / unknown )
board-word    = "draft" / "pack" / "open" / "return" / "review" / "closed"   ; tail.rs:54-58, seqpage.md:122
cards-v       = unknown / card *( ", " card )                   ; derive.rs:72-84; card as seqAddr.md:280
kind-v        = "book door (R10: face 00 only)" / "override (R7)"   ; derive.rs:110-117
why-draft-v   = reason-text / note-line / unknown               ; derive.rs:119-145, seqpage.md:109
stamp-v       = stamp-text / none / unknown  ; title, type, axioms read from the stamp (derive.rs:189-194)

; text productions (added in pass 05.03)
r4-char       = %x20-7E                      ; printable ASCII; the file is R4 (parse.rs:86-88; text.rs:59-61)
text          = 1*r4-char                    ; one line, at least one character
stamp-text    = r4-char [ *r4-char r4-char ] ; text with no leading or trailing space:
                ; the value after the first ":" on a stamp field line, trimmed (cards.rs:77-86, parse_stamp cards.rs:160-181);
                ; an empty value is shown as none (derive.rs:193)
reason-text   = text                         ; the opening entry's `reason` string, used as stored, not trimmed (derive.rs:131, :135)
note-line     = stamp-text                   ; the first nonblank line of the first `note` body after the draft
                ; opened, trimmed (derive.rs:137-138)
```

Notes on the grammar:
- `source :=` always uses the full book address `DD.SS.BB`, for example `source := book 10.11.30 @5 @6` (timer.seq:93).
  *Pass 05.01 wrote it as `source := book BB @n @m`, which is not the form.*
- With no entries, the registry's `source` is just `book DD.SS.BB` (derive.rs:216).
- `-` means face 00 has no such field. `7` means it could not be computed, for example when the entries do not replay (seqpage.md:179, :188).
- `reason-text` is one line only if the stored reason is one line. A decoded JSON string may hold a newline and still pass R4, because newline is an R4 character (text.rs:59-61, :97-104). derive.rs:131 and :135 do not trim or split the reason. I found no code that refuses a multi-line reason before it reaches `why-draft :=`, and I did not test it. That case stays `7`.
- On face 00, `counters :=` uses `counters-v` like any other face (derive.rs:232-243, :249).

### 2.5 Escaped keys and decoded ASCII (new in pass 05.02)

**Escaped keys** (seqpage.md:156). A field key must be a lowercase word: a letter, then `a-z`, `0-9`, `-` or `_` (text.rs:148-152; parse.rs:34-35). Any other key is written as `x: {"Key":value}`. The reader holds it to four rules (parse.rs:263-276):
- the value is a JSON object;
- the object has exactly one key;
- every string in it, the key included, passes R4 after decoding (text.rs:97-104);
- `x:` is refused when the key could have been written as a plain field.

**Decoded ASCII** (seqpage.md:44). R4 is checked twice:
1. On the raw file: the first byte outside 0x20-0x7E and newline is refused, with its line and column (parse.rs:86-88; text.rs:63-78).
2. On decoded values: a quoted value or JSON value whose decoded text holds a refused character is refused (text.rs:121-139). So a quoted value written as a quote, `caf`, a backslash, `u00e9` and a quote (the JSON escape for an accented e) is refused, even though every raw byte in it is ASCII. seqpage.md:44 gives the same example.

Values also have one canonical form: plain text unquoted, JSON compact, no spare quotes (text.rs:113-146; seqpage.md:152-155).

---

## 3. Worked examples

All cites are @8e96151d.
- "Covered" means the line kind and its placement match section 2.
- **NOT COVERED** marks a point the docs or code do not settle.
- **ANSWERED** marks a point pass 05.01 left open that a ruling or the code now settles.

### Example A: face00/10.11.40.1001.cats.seq (48 lines, a draft general page)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1 | `seqpage 1` | magic | covered |
| 2 | `= 00 registry 10.11.40.1001.00` | face section | covered. The name `registry` is R10 (DIRECTOR-RULINGS.md:40-41). |
| 3-5 | `title := cats`, `state := draft`, `registry := draft` | derived | covered (2.4: stamp-v, page-state-v, slot-v) |
| 6 | `why-draft := a new page starts as a draft (drafting.md)` | derived | covered: derive.rs:204-207 writes it while face 00 is in draft, from the `reason:` on line 16 (derive.rs:119-136). See Q6. |
| 7 | `faces := 01 draft` | derived | covered (2.4: faces-v) |
| 8-9 | `type := general`, `axioms := -` | derived | covered |
| 10 | `lineage := 10.11.40.1001 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00` | derived | covered (2.4: lineage-v) |
| 11 | `source := book 10.11.40 @9` | derived | covered (2.4: source-v, full book address) |
| 13 | `--- @9 put 10.11.40.1001.00.draft` | block header | covered. The draft is addressed `FF.draft` (R8, DIRECTOR-RULINGS.md:34-35). |
| 14-16 | `at:`, `by:`, `reason:` | fields | covered (seqpage.md:146-147) |
| 17-27 | front-matter stamp, then `## Registry` | body | covered as body. Layout is a draft (face00.md:28-32). |
| 29-32 | `= 01 law ...` and its derived lines | face section | covered |
| 34-38 | `--- @10 put ...01.draft`, fields, `cards := cats` | block | covered. `cards :=` is checked against the body (parse.rs:369-370). |
| 39-43 | `\| ## cats` and its fields | body | covered |
| 45-48 | `~ history`, two lines, `~ end` | history | covered. Each history line matches one block (seqpage.md:200). |

Result: every line is covered. The stamp's own `why-draft:` (line 22) differs in text from the derived line (line 6). The view shows the entry's reason. The stamp field is a PROPOSED name (face00.md:113). See Q6.

### Example B: 10.11.30.1501.timer.seq (168 lines, a workflow page with counted faces)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1-10 | registry section, `faces := 01 seated, 04 seated+draft, 05 counted, 06 counted` | as in A | covered |
| 12-23 | `--- @2 put ...00` with `proposal: p3` and `of: 3`, stamp body with no `## Registry` | block | covered. The missing registry card is a finding (face00.md:457). |
| 25-27 | `= 01 law ...`, `source := book 10.11.30 @3 @10 @11 @12 @13` | face section | covered (source-v) |
| 29-37 | `--- @3 put ...01`, `cards := timer`, body `## Timer` | block | covered (card key in title form, seqAddr.md:168) |
| 39-41 | `--- @10 copy 10.11.30.1501.01` with no body | block | **ANSWERED** (was not covered). Drafting ops name the seated `FF` or `FF.draft` (state.rs:607-615). A `copy` sends no body and needs a seated face. The compute then makes the one draft from the seated text (state.rs:621-631). So a `copy` addressed to the seated face is the built form. See Q5. |
| 43-59 | `note`, `merge` with `cites: 11`, `promote` | blocks | covered. `cites: 11` refers to entry 11 (2.3, item 2). |
| 61-64 | `= 04 user ...`, `state := seated+draft`, `why-draft := ...` | face section | covered. `why-draft` comes from the `copy`'s `reason:` (line 81; derive.rs:133-135). |
| 66-76 | `--- @4 put ...04`, card with `\| source: [01 / Timer]` | block | covered as body. **NOT COVERED**: nothing resolves the bracket reference (2.3, item 5). |
| 78-86 | `--- @15 copy ...04` with `reason:`, `--- @16 note ...04` | blocks | covered (same rule as line 39) |
| 88-89 | `= 05 tasks ...`, `counters := 01 closed` | face section | **ANSWERED** (was not covered): faces have no `FF.00` board (R9, DIRECTOR-RULINGS.md:37-38). The board is the derived `counters :=` (2.4). |
| 91-93 | `== 05.01 ...`, `state := closed`, `source := ...` | counter section | covered |
| 95-104 | `--- @5 put ...05.01`, `tail: pack`, body with `lead: 3MC` | block | covered as a field. **NOT COVERED**: the counter's tail is a field and a `tail` op, while seqAddr.md:128 writes counter tails in the address. Open (section 5.2, O3; Q3). |
| 106-133 | four `tail` blocks; the last has `to: ""` and `outcome: passed` | blocks | covered. `""` is the JSON string for "bare = closed" (seqpage.md:153). |
| 135-150 | `= 06 notes ...`, `== 06.01 ...`, one `put` | face, counter, block | covered. No `06.00` board, per R9. |
| 152-168 | `~ history` with 15 lines, then `~ end` | history | covered. History is in book order; blocks are in book order inside each section (seqpage.md:135, :199). |

Result: every line has a kind. Two points pass 05.01 marked are now answered (the `copy` address and the boardless counted face). One stays open (where a counter's tail lives).

### Example C: proposals/10.11.21.1001.bob.seq (83 lines, one `new` block)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1-11 | registry section with `why-draft := 7` | as in A | covered. `7` means no reason was recorded, a finding (seqpage.md:232; derive.rs:206). |
| 13-22 | `--- @7 put ...00.draft`, `proposal: prima-kernel-seed:10.11.21.1001`, stamp body | block | covered. A raw value may contain `:` (text.rs:141-142). |
| 24-66 | faces 01 and 04, one draft block each, two cards each | face, block | covered. `[01 / bob]` in the 04 bodies is the same unresolved form as B:73. |
| 68-70 | `= 06 notes ...`, `== 06.01 ...` with no derived lines | face, counter | covered. Derived lines are optional when reading (seqpage.md:178), and no board is needed (R9). |
| 72-77 | `--- new put 10.11.21.1001.06.01`, body only | `new` block | covered: after the booked blocks, and no stamp fields (seqpage.md:136, :148) |
| 79-83 | `~ history`, three lines, `~ end` | history | covered. The `new` block has no history line (seqpage.md:201). |

Result: every line is covered except the bracket references in the face 04 bodies.

### 3.4 Stamp against replay: real/10.11.21.1001.bob.seq (new in pass 05.02)

This file is exported by the seqpage CLI from a real book, not written by hand (real/README.md:3, :8). The same file shows the page's state in two places, and they disagree:

| Where | Line | Says | Source of the value |
|---|---|---|---|
| derived registry line | 4 | `state := live` | replay of the page's entries (derive.rs:174-178, :198) |
| stamp, in the face 00 body | 23 | `\| state: draft` | written by a person in the stamp |
| derived registry line | 7 | `faces := 01 seated, 05 counted` | derived from entries (derive.rs:88-108) |
| registry card, in the body | 28 | `\| faces: 01 seated, 05.01 seated, 05.02 seated` | written in the stamp's registry |
| face 05.01 body | 85-88 | the page's own 05.01 card reports that `seqpage check` "disagrees with the kernel face 00" on stamp state, and that TRIAL-K3 raised the same clash | written by prima-packs |

How the grammar handles it:
- The file is still valid. The disagreement is a finding, not an error (face00.md:105, :453; seqpage.md:232).
- real/README.md:25-29 records "0 errors, 3 findings": stamp state against entries, `faces:` written against derived, and `seat-01:` not a registry field for type `general`.
- README.md:21 says why `05 counted` differs from the seat records: seqpage derives counter state from tails, not seat records.

What stays open:
- Which state is the page's state: the stamp `state:` or the replayed page tail? seqpage.md:86 calls this "Still open".
- Which wins between a written and a derived `faces:` (face00.md F2, :468).
- These are O4 and O5 in section 5.2.

**Claude proposal.** This is the clearest real case for Q6 and O4. The derived line shows one truth, and the stamp in the booked body shows another.

Neither is sent as a write on import (fixed in pass 05.03):
- Derived lines are never imported (seqpage.md:177).
- The stamp sits in booked block @12. When a book is supplied, import only compares each booked block with the book's entry of that number, refusing a missing or different entry (import.rs:45-51, :64-71).
- Only `new` blocks become the proposal (import.rs:79-87).

*Pass 05.02 called the booked body "imported". That was wrong.* The grammar reports the gap but does not choose, which keeps axiom 1: "Do not choose" (Axioms.md:13).

---

## 4. How each axiom is kept

All cites are @8e96151d. The axiom text is Axioms.md:13-29.

| # | Axiom (Axioms.md line) | Where the grammar keeps it | Gap |
|---|---|---|---|
| 1 | Authority (:13) | Import is only a proposal (seqpage.md:215). A `new` block cannot carry compute stamps (seqpage.md:148; parse.rs:256-258). A second registry, or a field or entry written twice, is a conflict (seqpage.md:82, :226). Stamp against replay is reported, not chosen (3.4). | The file never checks a grant. The proposer is named only at import (seqpage.md:239). |
| 2 | Fractal (:15) | The address inherits its ancestors (seqAddr.md:79, :101-104). `lineage :=` writes the chain (2.4). Face, counter and registry sections share the same `state :=` and `source :=` shape (seqpage.md:183-185). The board is a derived list one level down, like `faces :=` on face 00 (R9; derive.rs:232-243). | Inherited faces are not shown (S2). The whole-book export (R26) has no written grammar yet, so whether it reuses the page grammar is open (O1). |
| 3 | Leads (:17) | Faces map to readers (seqAddr.md:150-153). Cards may carry `lead:` (timer.seq:101). A band page has a `lead` registry field (face00.md:205). | No lead field at block or section level. `lead:` lives only in body text. |
| 4 | Why (:19) | `why-draft :=` shows why a face is a draft, from the opening entry's `reason:` (derive.rs:119-145; seqpage.md:109). A `why:` line is required on 04 cards (seqAddr.md:184). The core request carries `reason` (validate.rs:40-42). | A missing why is only a finding (`why-draft := 7`). derive.rs:121 still calls the source of the why provisional (S7). |
| 5 | Frame (:21) | A face 05 counter holds a pass's pack, claim, return, review and close (seqpage.md:121). | No structure for goal, stop or done-when. A pack is free text in a card body (timer.seq:100-104). |
| 6 | Lineage (:23) | Booked blocks in book order, `new` after the past, and one block plus one history line per entry (seqpage.md:135-136, :199-201). An edited past entry is refused (seqpage.md:214; SEQ-GUIDE.md:516-534). | Derived lines change in place (S1, seqpage-QUESTIONS.md:7-8), an agreed exception. R28 makes face 09 the page log (DIRECTOR-RULINGS.md:113-115), but the view still writes `~ history`, and the core refuses face 09 (TEST-2:196-197). |
| 7 | Missing (:25) | `7` (could not be computed) is distinct from `-` (none written) (derive.rs:18-20; seqpage.md:188). A missing face is absent (seqpage.md:107). A missing registry, `~ end`, `at` or `by` is an error (seqpage.md:224). | Derived lines are optional when reading (seqpage.md:178), so leaving one out raises nothing. |
| 8 | Connection (:27) | A block must be on its page and in its section (seqpage.md:134). A derived line that disagrees is refused, `cards :=` included (seqpage.md:178; parse.rs:366-370). A wrong file name or header address is an error (seqpage.md:27, :229). | Face 08 links are not designed (seqAddr.md:302). `lineage :=` leaves them out (S3). Body references such as `[01 / Timer]` are not resolved (2.3, item 5). |
| 9 | Trial (:29) | The spec marks itself `9` (seqpage.md:3). R2's `approved-by` and `trial` fields appear on real seated entries (real/bob.seq:98-99). | No line kind marks a block `9`. The trial record is a free field, not part of the grammar. |

---

## 5. Conflicts in the docs

All cites are @8e96151d. In pass 05.02, section 5 is split in two.

### 5.1 Superseded or stale text (a later ruling or fix settles it)

The older line is not rewritten. It stays as written, and the later step governs (Axioms.md:23). The "was" column gives each item's number in pass 05.01.

| # | Was | Older text | Later step that governs |
|---|---|---|---|
| S1 | K2 | seqpage.md:13 "The book is the real copy (R3)"; SEQ-GUIDE.md:22 | R26: "The stored form is today's small files. A whole-book .seq file is an export" (DIRECTOR-RULINGS.md:103-106) |
| S2 | K4 | seqAddr.md:197-198 "A face is counted if and only if `FF.00` exists"; :44, :53, :277, :288 | R9: "no `FF.00` and no `FF.99`. Counted faces have no door" (DIRECTOR-RULINGS.md:37-38); seqpage.md:120. R9 settles the general rule only. The R16 dictionary 03.00 "door" (DIRECTOR-RULINGS.md:65-66) is held 7, and is open conflict O11. |
| S3 | K5 | seqAddr.md:149 names face `00` "identity"; R1 calls the zero sequence "door" (DIRECTOR-RULINGS.md:5) | R10: "On any page, face 00 is the registry" (DIRECTOR-RULINGS.md:40-41); seqpage.md:81-82 |
| S4 | K7 | seqAddr.md:158 face 09 "reserved, unassigned" | R28: "face 09 is the page's log" (DIRECTOR-RULINGS.md:113-115). Only the short-log-in-00 part is held 7 (:115). The build gap stays: the core refuses face 09 (TEST-2:196-197). |
| S5 | K9 | seqAddr.md:189 face 03 allowed only on reserved pages | R35, 2: "Any page may have a compute-written face 03 menu", for the menu card (DIRECTOR-RULINGS.md:179-180) |
| S6 | K10 | face00.md:478 F12 "The core OpRequest has no `reason` field"; seqpage-QUESTIONS.md:32 | Fixed in code: `reason` is on the request (validate.rs:40-42). SEQ-GUIDE.md:598 records F12 closed. face00.md:478 is stale. |
| S7 | K11 | seqpage.md:263 lists S7-S10 as open, including "where title and type live" | seqpage.md:86 and seqpage-QUESTIONS.md:40 say S9 is settled by R12 and R19. Line 263 is stale. |

### 5.2 Real open conflicts (not resolved here)

| # | Was | One side | Other side | What clashes |
|---|---|---|---|---|
| O1 | K1 | seqpage.md:11 "A `.seq` file holds one page" | R26: a whole-book .seq is an export (DIRECTOR-RULINGS.md:106); PLAN:242, :274 | two `.seq` shapes under one extension. R26 says the book shape exists but not how the two are named or told apart (PLAN:1050-1053, C1). |
| O2 | K3 | the v1 page view: `seqpage 1` files are plain ASCII on every line (seqpage.md:31, :44; parse.rs:86-88) | the proposed stored form and whole-book format: R27 lets faces other than 04 be compact code (DIRECTOR-RULINGS.md:108-111). SEQ-FILE-PLAN Step 3 frames that binary for stored face files and the whole-book export, with length and fingerprint before the bytes (PLAN:315-327, esp. :321, :327). | Narrowed in pass 05.03. The v1 page view stays ASCII, and nothing in R27 or PLAN:315-327 changes `seqpage 1`. What stays open is only how a code face appears in a page view: PLAN:321 says "a decoded view", but no format or version for it is written. |
| O3 | K6 | seqAddr.md:128 counter tail in the address, `PPPP.FF.NN.tail` | seqpage.md:122 and timer.seq:98 counter tail as a `tail:` field and `tail` ops; R8 puts the face draft in the address (DIRECTOR-RULINGS.md:34-35) | where a tail lives |
| O4 | new | the stamp `state:` (face00.md:62, :103) | the replayed page tail (derive.rs:198); seqpage.md:86 "Still open" | which is the page's state. The real case is real/bob.seq:4 against :23 (section 3.4). |
| O5 | new | a written `faces:` in the registry card (real/bob.seq:28) | the derived `faces :=` (real/bob.seq:7; derive.rs:88-108) | written against derived; face00.md F2 (:468) |
| O6 | K12 | face00.md:214 workflow `role` from the band digit: `N7` is "colab" | the lab band allocation `DD.SS.BB.0700-0799` is settled by t432u and t434 (seqAddr.md:345-351) | Narrowed in pass 05.03. The allocation is not in conflict: 0700-0799 is the lab band. What stays open is only face00.md's draft role table, which still maps `N7` to `colab` for workflow pages. Whether that table drops `N7`, or keeps colab for bands other than 0700, is not written. |
| O7 | K13 | seqAddr.md:157 face 08 with face 00 keeps lineage | seqpage.md:88 `lineage :=` is the address chain only (S3) | what lineage holds; face00.md F5 (:471) |
| O8 | K14 | seqAddr.md:149-158 faces 01 law, 03 operate, 06 notes, 07 reserved | kit docs/DESIGN.md:22, :24, :27, :28 @c09fa60c: 01 agents card, 03 menu, 06 prime notes, 07 labs | face names on wf pages. DESIGN.md is a kit file, not a listed source. |
| O10 | K8 (part) | face00.md:111 a draft page carries a stamp `why-draft:` | the view's `why-draft :=` comes from the entry's `reason:` (derive.rs:119-145, :204-206) | two whys for one draft. The view's rule is answered (Q6), but whether the stamp field should exist is open (face00.md:113, PROPOSED). |
| O11 | new in 05.03 | R9: "no `FF.00` and no `FF.99`" (DIRECTOR-RULINGS.md:37-38) | R16: "the dictionary's 03.00 is a door", held 7 with the tension named (DIRECTOR-RULINGS.md:65-66); face00.md:470 (F4) | Whether the dictionary's face 03 is an exception to R9. Builders do not resolve it (DIRECTOR-RULINGS.md:66). |

### 5.3 Parked by a ruling (not a live conflict)

| # | Was | Text | Ruling that parks it |
|---|---|---|---|
| P1 | K15, then O9 | seqpage.md:96 override pages in 0001-0009 (R7); seqpage.md:263 lists S10 open | R21: no override pages "while we build the Workshop app itself"; they "stay in the design for child desks later" (DIRECTOR-RULINGS.md:82-84). Parked until child desks; not answered and not live. Moved here in pass 05.03. |


---

## 6. Open questions

The option marked **(default)** is the fractal one, under axiom 2: "The same shape at every scale. Inherit what is agreed; write only the difference" (Axioms.md:15), per t384u.md:5 as the pack cites it. Defaults are **Claude proposals**, never decisions (Axioms.md:13).

Questions marked **ANSWERED** in pass 05.02 keep their number, so links from pass 05.01 still hold.

**Q1. One page or a whole book (O1).** Open.
- (a) The page file only, with the book export under another name.
- (b) One extension, two shapes, told apart by a header marker (PLAN:1052).
- (c) **(default)** One grammar at every scale: a book file is the book's door page (`DD.SS.BB.0000`, face 00 only) as its registry section, then each page in the page shape of section 2. A book is identified by page 0000 (seqAddr.md:56), as a page is by face 00 (seqAddr.md:64).

**Q2. The board of a counted face. General rule ANSWERED; one exception open.**
- Answered: R9's general rule, "no `FF.00` and no `FF.99`. Counted faces have no door; counters run 01-98 only" (DIRECTOR-RULINGS.md:37-38).
- The board is the derived `counters :=` (derive.rs:232-243), and seqAddr's `FF.00` lines are superseded (5.1, S2).
- Open (O11): R16 calls the dictionary's `03.00` "a door". That ruling is held 7, its tension with R9 is named, and "Builders do not resolve it" (DIRECTOR-RULINGS.md:65-66; face00.md:470, F4).
  - (a) The dictionary's 03.00 is a named exception to R9.
  - (b) R9 governs, and the dictionary's index board is derived, like every other board.
  - (b) is the **(default)**: one board form at every face (Axioms.md:15). An exception would need a named override (Axioms.md:15).

**Q3. Where a tail lives (O3).** Open.
- (a) In the address at every level, as R8 does for face drafts.
- (b) In a field or op at every level.
- (c) Mixed, as built.

(a) is the **(default)**: one form at page, face and counter (seqAddr.md:126-128).

**Q4. The name of face 00. ANSWERED.**
- R10: "On any page, face 00 is the registry" (DIRECTOR-RULINGS.md:40-41).
- The header `= 00 registry` is what the reader accepts, and `= 00 door` is refused (seqpage.md:81-82).
- seqAddr's "identity" is superseded (5.1, S3).

**Q5. A copy that opens a draft. ANSWERED** (by code).
- Drafting ops name the seated `FF` or `FF.draft` (state.rs:607-615).
- A `copy` sends no body, needs a seated face, and the compute makes the face's one draft from it (state.rs:621-631).
- So `--- @10 copy ...01` on the seated address is the built form (timer.seq:39).

**Q6. Which why governs a draft in the view. ANSWERED** (by code).
- The view's `why-draft :=` comes from the `reason` of the entry that opened the current draft. That entry is a `put` to `FF.draft` (or with tail draft) or a `copy`. If there is no reason, it comes from the first nonblank line of the first `note` after the draft opened, trimmed of spaces (derive.rs:137-138). Otherwise it is `7` (derive.rs:119-145).
- The same rule applies to face 00 (derive.rs:204-206).
- Still open: whether the stamp keeps its own `why-draft:` field at all (5.2, O10). derive.rs:121 also marks the rule provisional (S7).

**Q7. The page log: `~ history` or face 09. ANSWERED** (by ruling).
- R28: "face 09 is the page's log" (DIRECTOR-RULINGS.md:113-115).
- Still open: how the `.seq` view shows face 09 once the core allows it (TEST-2:196-197). Today's `~ history` section stays as built until then.
- Option: face 09 as a face section `= 09 ...` like every other face (fractal), or `~ history` kept as its derived view. **(default)**: the face section.

**Q8. Inherited faces (S2).** Open.
- (a) Leave them out, as today.
- (b) Copy them in.
- (c) **(default)** A derived `inherits :=` line naming where each missing face resolves (seqpage-QUESTIONS.md:12).

**Q9. Value forms of derived lines.** Partly answered in pass 05.02. Section 2.4 now writes the grammar from the code.
- Still open: whether seqpage.md should carry that grammar as spec. Today only the code and examples give it.
- **(default)**: write it into the spec in the address grammar's style (seqAddr.md:265-283), so one grammar covers every value.

**Q10. References inside the file and its bodies.** Open.
- (a) Keep `[01 / Timer]` as the card reference in 04 bodies (seqAddr.md:179).
- (b) **(default)** Use the active-relative form `.01.timer` (seqAddr.md:270-271).

Also open: may `cites:` name an entry on another page (PLAN:1044-1047, C10)?

**Q11. Leads and frame in the grammar.** Open.
- (a) Keep them as body text.
- (b) **(default)** Allow `lead:` the way `axioms:` is allowed on any card and the stamp (seqAddr.md:172).

**Q12. Face names on wf pages (O8).** Open, and outside this lab's grant.
- (a) Keep DESIGN.md's names.
- (b) **(default)** Use seqAddr's numbers and names, with any difference as a named override (Axioms.md:15).

**Q13. What lineage holds (O7).** Open.
- (a) The address chain only.
- (b) The authorization trail only.
- (c) **(default)** Both, each as its own derived line.

**Q14. Stamp against replay (O4, O5). New in pass 05.02.** Open.
- (a) The stamp governs, and replay is a check.
- (b) Replay governs, and the stamp's `state:` and `faces:` become derived only.
- (c) Keep both, and report a finding, as built.

**(default)** (b). It is the same rule `:=` lines already follow: a derived value is computed, never typed, and a copy never becomes what it points to (seqpage.md:177-178; Axioms.md:27). It also matches face00.md:179, which proposes that "the compute writes `faces:`, nobody writes it by hand". But R12's Read says "A page's state is kept in the stamp in face 00" (DIRECTOR-RULINGS.md:53-54), which points toward (a). So the fractal default and R12's Read pull opposite ways. That is why this stays open and is Matthew's call.

---

## 7. Notes for the checker

- Every section is `9`.
- I did not run `seqpage check` or any other code in either pass. Every "covered" and "ANSWERED" verdict cites a line of spec, ruling or code that I read. None is tool output.
- Pass 05.03 checks use the form `[#][#][[:space:]]N[.]`, with no caret, no quotes and no space (pages/90.50.10.0702/05.03/PACK.md, checks line). On Windows, wf runs each check through `cmd /C` (src/git.rs:111 @a823ee28), where `^` and `"` have meanings of their own.
- In pass 05.03 I ran the pack's checks by hand in PowerShell, not through `wf check`. Only the checker's run shows how wf runs them.
- Line numbers in this version differ from ba9a5b71. The pack's lab:N cites refer to ba9a5b71.
- LESSONS.md, beside this file, lists what went wrong in passes 05.01 and 05.02, and why.
