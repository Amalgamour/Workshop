# LAB 0702: the seq grammar lab

Page: 90.50.10.0702, pass 05.01. Builder: Claude. Checker: Codex, by hand.
Made: 2026-11-23. Status: `9`. Nobody has run a hostile trial on it yet (Axioms.md:29@8e96151d).
Why: t451u, quoted on face 01. Matthew: "We have a lot to learn about axioms, designing and building our grammar out of seqaddr. How a .seq file should work."

How to read the cites. A cite written `path:line@8e96151d` means that line of that file at build commit 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a (origin/prima/build). I read each source with `git show 8e96151d:<path>`. Short paths are used below:
- `seqpage.md` stands for docs/spec/seqpage.md.
- `seqAddr.md`, `face00.md`, `SEQ-GUIDE.md`, `seqpage-QUESTIONS.md`, `KERNEL-FILE-TITLES.md` and `Axioms.md` are all under docs/spec/.
- `PLAN`, `TEST`, `TEST-2`, `PROTO` and `CITE-DRAFT` are docs/design/SEQ-FILE-PLAN.md, SEQ-FILE-PLAN-TEST.md, SEQ-FILE-PLAN-TEST-2.md, SEQ-PROTO-RESULTS.md and AXIOM-CITE-GRAMMAR-draft-t383u.md.
- Example files are named by their path under docs/spec/examples/.

The report says "@8e96151d" once at the top of each section, not on every cite. Every cite in this file is at 8e96151d unless it says otherwise.

Who said what:
- A line marked **Claude proposal** is my own reading or idea. It is not a source and not a ruling.
- Matthew's words appear only where a source quotes them, with the source's cite.
- Matthew did not talk the design through with me in this pass (2026-11-23), so this report records none of his words directly.

---

## 0. Sources read

Commit: 8e96151dbe9ff03a55e6838168033ba6bf5f4a4a. I fetched it from origin/prima/build on 2026-11-23, and `git cat-file -t` reports it as a commit. The branch tip has since moved to 78101fe6. I read nothing at the tip.

| Source | At 8e96151d | Lines | Read |
|---|---|---|---|
| docs/spec/Axioms.md | present | 29 | read in full. Its body is byte-identical to the kit's docs/AXIOMS.md under that file's 2-line header. |
| docs/spec/seqpage.md | present | 263 | read in full |
| docs/spec/seqpage-QUESTIONS.md | present | 48 | read in full |
| docs/spec/SEQ-GUIDE.md | present | 609 | read in full |
| docs/spec/face00.md | present | 478 | read in full |
| docs/spec/KERNEL-FILE-TITLES.md | present | 62 | read in full |
| docs/spec/seqAddr.md | present | 364 | read in full. The pack names sections 1, 4, 8, 10 and 11, and I used sections 2, 3, 5, 6 and 7 too. |
| docs/design/SEQ-FILE-PLAN.md | present | 1138 | read in part: lines 1-120, 209-488, 630-706 and 942-1112 (summary, rulings, Steps 1-8 and 13, open choices, still open). Steps 9-12 and 14-17 were not read line by line. |
| docs/design/SEQ-FILE-PLAN-TEST.md | present | 332 | read in part: headings, verdict, sections e (114-134) and "New holes" (291-312) |
| docs/design/SEQ-FILE-PLAN-TEST-2.md | present | 267 | read in part: headings, verdict, section 4 (122-144) and Face 09 (191-200) |
| docs/design/SEQ-PROTO-RESULTS.md | present | 169 | read in part: 1-28 and 144-169 |
| docs/design/AXIOM-CITE-GRAMMAR-draft-t383u.md | present | 82 | read in full |
| docs/spec/examples/face00/10.11.40.1001.cats.seq | present | 48 | read line by line (example A) |
| docs/spec/examples/10.11.30.1501.timer.seq | present | 168 | read line by line (example B) |
| docs/spec/examples/proposals/10.11.21.1001.bob.seq | present | 83 | read line by line (example C) |
| docs/spec/examples/00.00.00.0051.seqaddr.seq | present | 584 | listed only. I did not read it line by line in this pass. |
| docs/spec/examples/10.11.21.1001.bob.seq | present | 72 | listed only |
| docs/spec/examples/face00/10.11.40.0000.seq | present | 28 | listed only. face00.md:412-437 quotes its face 00 section. |
| docs/spec/examples/face00/10.11.40.0012.dictionary.seq | present | 47 | listed only. face00.md:306-333 quotes its face 00 section. |
| docs/spec/examples/face00/10.11.40.0400.dev.seq | present | 46 | listed only. face00.md:341-369 quotes its face 00 section. |
| docs/spec/examples/face00/10.11.40.0403.ide-design.seq | present | 63 | listed only. face00.md:377-406 quotes its face 00 section. |
| docs/spec/examples/proposals/10.11.21.1002.seq | present | 18 | listed only |
| docs/spec/examples/real/10.11.21.1001.bob.seq | present | 154 | listed only |

No named source is missing. docs/spec/examples/ holds the 11 `.seq` files the pack expects. It also holds real/README.md and four books under sources/. Those are not `.seq` files, and I did not read them.

Some sources cite files that are not on the source list, such as DIRECTOR-RULINGS.md, decisions.md and format.md. I did not open those files. Where this report needs one of them, it cites the listed source that quotes it.

---

## 1. What a .seq file is

All cites in this section are @8e96151d.

**What it holds.** A `.seq` file holds one page with all its faces, as plain text a person can read from top to bottom (seqpage.md:11; SEQ-GUIDE.md:14-16). It holds only the page's own entries from its own book. Faces that the page inherits through a lookup are not in the file (seqpage-QUESTIONS.md:11-12, S2, provisional).

**It is a view, not the store.** "The book is the real copy" (seqpage.md:13, R3). The file is exported from a book and imported back. An import is only a proposal: "Importing never writes a book" (seqpage.md:14; also :215). The round trip is lossless (seqpage.md:15). The file only grows when re-exported, and only derived lines may change in place (seqpage.md:16).

Later design moved the store. PLAN:226 says R3 "is updated by t175u: small files are stored, whole books are an export". PLAN:246-247 says the stored form is small files and the export is one whole-book `.seq`. seqpage.md was not updated to match. See section 5, conflicts K1 and K2.

**One page per file, or not.**
- In the spec, a file is one page (seqpage.md:11).
- In the design plan, the name `.seq` also covers a whole book: "A book is a .seq file" (PLAN:242, Matthew's idea of 16 Nov 2026 as the plan quotes it). PLAN:274 says the one-page view "needs either a new name or a clear note that `.seq` now has two shapes". This is open as C1 (PLAN:1050-1053).
- The kernel keeps a third form for its sources: one face of one page per `.md` file (KERNEL-FILE-TITLES.md:11-15).
- The prototype keeps one folder per page and one file per face (PROTO:10-18).

**How it is named.**
- `DD.SS.BB.PPPP.title.seq`, or `DD.SS.BB.PPPP.seq` when the page has no title (seqpage.md:21-22).
- The address is the full page address. The title is the `title` field on face 00 (seqpage.md:25).
- If the title in the name differs from face 00, the mismatch is elevated, never fixed silently. If the address in the name is wrong, that is an error (seqpage.md:27).
- Page 0000 never has a title in its name (seqpage.md:22; KERNEL-FILE-TITLES.md:19).
- A title is a label, not identity (seqAddr.md:114).

**Who writes it.**
- The compute writes it through `export`. Derived `:=` lines are "computed on export" (seqpage.md:177, :206). The command is `seqpage export` (seqpage.md:237-238).
- A person may write `new` blocks by hand, and may leave out derived lines (seqpage.md:178; SEQ-GUIDE.md:183).
- A person may hand-write a whole file for a page that does not exist yet (seqpage-QUESTIONS.md:23, S5, provisional).
- The proposer is named once, at import (`--by NAME`). A `new` block cannot carry `at`, `by` or the other stamp fields (seqpage.md:148, :239).
- Only the compute writes the book (seqpage.md:215).

**Plain characters.** Every character is printable ASCII 0x20-0x7E or newline. The reader refuses the file at the first other character (seqpage.md:31, :43, R4). PLAN:319 says R4 was later narrowed for stored faces. See conflict K3.

---

## 2. Grammar

All cites in this section are @8e96151d. Each rule is cited. Where the docs do not settle a point, this section says so and points to section 5 or 6.

### 2.1 The address form

The axes, from highest to lowest (seqAddr.md:14-22):

| Part | Width | Rule |
|---|---|---|
| desk `DD` | 2 digits | highest controlling environment (seqAddr.md:18) |
| shelf `SS` | 2 | themed work space (:19) |
| book `BB` | 2 | localized environment (:20) |
| page `PPPP` | 4 | the work inside a book. This is the only 4-digit axis, so it anchors reading (:21, :71) |
| face `FF` | 2 | one view of a page (:22) |
| counter `NN` | 2, 01-98 | not an axis. It attaches only to a face (:24) |
| tail | word | `draft` or `retired` on a page or face. `draft`, `pack`, `open`, `return` or `review` on a counter. A bare counter means closed (:126-128) |

Reading order is `[DD.][SS.][BB.] PPPP [.FF][.NN] [.title][.tail]` (seqAddr.md:74). The formal grammar is at seqAddr.md:265-283. Its main rules:
- `page-end = face-part / title [ "." page-tail ] / page-tail` (:269)
- `face-part = face [ "." counter ] [ "." tail ] [ "." card [ "." brand ] ]` (:271)
- `active-rel = "." face-part` (:270)

It has these rules besides:
- Widths are exact (:14).
- `00` means "the owner of the level above, itself" (:29, :44).
- `01-09` and `0001-0099` are reserved (:30). `99` and `9999` are pointers (:31).
- A word after a face is a card key, not a title. Three digits after a card are a brand (:111).
- Rules the grammar does not express are listed at :287-291. For example, `retired` comes only without a counter, and a counter needs its face's `00` board. The board rule clashes with R9 (conflict K4).
- An axiom chain is never an address (:293).
- Work addresses: desk, shelf and book 00-09 are system only, and work starts at 10 (seqAddr.md:320). Pages 0000-0099 are reserved (:322). Band heads are doors (:323). Labs sit on `0701-0798` (:351).

In a `.seq` file the grammar uses only the full address. Each block header carries a full address (seqpage.md:130-131), and section headers carry the seated address (seqpage.md:106, :121). Short form is for users only, and "Models always write the full address" (seqAddr.md:95). In the three examples, every address is in full form.

### 2.2 The line kinds

The first characters of a line decide its kind (seqpage.md:47-60):

| Starts with | Kind | Rule |
|---|---|---|
| `seqpage 1` | magic line, line 1 only | seqpage.md:51 |
| `= ` | face section: `= FF name DD.SS.BB.PPPP.FF` | seqpage.md:52, :106 |
| `== ` | counter section: `== FF.NN address` | seqpage.md:53, :121 |
| `--- ` | block header: `--- @N op address` or `--- new op address` | seqpage.md:54, :130-131 |
| `key: ` | field, inside a block, after the header and before the body | seqpage.md:55, :145 |
| `key := ` | derived line, under a section header or a block header | seqpage.md:56, :177 |
| `\|` | body line: `\| ` plus text, or a lone `\|` | seqpage.md:57, :166 |
| `~ history` / `~ end` | history start / file end | seqpage.md:58 |
| `@` | history line `@N op address`, between `~ history` and `~ end` | seqpage.md:59, :199 |
| (empty) | separator | seqpage.md:60 |

Any other line is refused (seqpage.md:62).

The file has this order:
1. The magic line.
2. The registry section `= 00 registry ...`. It must come first and appear only once (seqpage.md:81-82).
3. The other faces, in number order (seqpage.md:107). Counters are in number order under their face (seqpage.md:121).
4. Within a section, booked blocks in book order, then `new` blocks (seqpage.md:135-136).
5. `~ history`, then `~ end`. Nothing may follow `~ end` (seqpage.md:202).

Block ops are `put`, `tail`, `snapshot`, `copy`, `note`, `merge`, `promote` and `use` (seqpage.md:133).

Fields come in a fixed order: `at`, `by`, `tail`, `from`, `to`, `proposal`, `cites`, `outcome`, `of`, `state`, then any other field in name order (seqpage.md:146). A booked block must have `at` and `by` (seqpage.md:147).

A value is written in one form only (seqpage.md:152-155):
- raw text when it is plain;
- a JSON string otherwise;
- compact JSON for numbers, true/false, lists and objects.

Body lines carry the face's Markdown exactly. Cards are its `##` headings (seqpage.md:167; seqAddr.md:168-169). Inside the body, face 00 has its own form: a front-matter stamp between `---` lines, then a `## Registry` card (face00.md:28-32). The exact layout is `7` (F9, face00.md:475).

Derived lines are allowed in these places (seqpage.md:183-186):
- **Registry section:** `title`, `state`, `registry`, `faces`, `type`, `axioms`, `lineage`, `kind` and `source`. `why-draft` too, by seqpage.md:66.
- **Face section:** `state`, `why-draft`, `source` and `counters`.
- **Counter section:** `state` and `source`.
- **Block:** `cards`.

`-` means face 00 has no such field. `7` means the value could not be computed (seqpage.md:188).

The value forms of some derived lines are not given as grammar. These are the `lineage` chain with `<`, `source := book BB @n @m`, `faces := 01 seated, 04 draft` and `counters := 01 closed`. They are shown only by example (seqpage.md:77-78, :114, :118). That is a gap: see Q9.

### 2.3 How a line refers to another page or line

1. **The block address.** The header of a block names the address it writes to, and that address must be on this page and in this section (seqpage.md:134). A block cannot write to another page.
2. **Entry numbers.** `@N` names entry N of the page's book. It appears in block headers, in `source :=` lines and in history lines (seqpage.md:130, :118, :199). An entry number appears once in the file (seqpage.md:135).
   The `cites:` field refers to another entry by its number. timer.seq:51 has `cites: 11`, and the field order lists `cites` (seqpage.md:146). The spec gives no rule that the cited entry must be on the same page. See Q10.
3. **The lineage line.** `lineage :=` writes the page's lookup chain: page < book < shelf < desk < kernel (seqpage.md:88; seqAddr.md:101). It uses container addresses (seqAddr.md:89). It leaves out face 08 links (S3, seqpage-QUESTIONS.md:16).
4. **Links between pages.** Links are meant to sit on face 08, written both ways (seqAddr.md:157, :251). How the compute holds them is "not yet designed" (seqAddr.md:302, C4). The design plan says a link names a page (address plus title), never a face, and gives the current page (PLAN:634, :643; TEST:117-119). The `.seq` grammar has no line kind for links. A link exists only as text in the body of face 08.
5. **References inside a body.**
   - A face 04 card refers to its 01 card as `source: [01 / Timer]` (timer.seq:73). seqAddr.md:179 shows the same form. That bracket form is not in the address grammar (seqAddr.md:265-283).
   - Bodies may also hold full addresses with a card, such as `10.11.21.1001.01.bob` (proposals/bob.seq:77). That form is in the grammar (seqAddr.md:111, :271).
   - The file never checks body text (seqpage.md:169).
6. **Axiom cites.** An `axioms:` field holds a chain (Axioms.md:5; seqAddr.md:172). Its proposed grammar is `cite = chain ("," chain)*` (CITE-DRAFT:37-40), which is a draft and not a ruling (CITE-DRAFT:5). In a `.seq` file, `axioms` appears as a stamp field in the body and as the derived `axioms :=` line (seqpage.md:86).
7. **Lines in other files.** No line kind refers to a line in another file. Entry numbers are the only line-level references.

---

## 3. Worked examples

All cites in this section are @8e96151d. I picked three files that together use every line kind, both block kinds (booked and `new`), a counted face and drafts. A line marked **NOT COVERED** is one the grammar of section 2 does not fully settle. "Covered" means the line kind and its placement match the rules cited.

### Example A: face00/10.11.40.1001.cats.seq (48 lines, a draft general page)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1 | `seqpage 1` | magic | covered (seqpage.md:51) |
| 2 | `= 00 registry 10.11.40.1001.00` | face section | covered (seqpage.md:81). See K5 for the face name. |
| 3-5 | `title := cats`, `state := draft`, `registry := draft` | derived | covered (seqpage.md:183) |
| 6 | `why-draft := a new page starts as a draft (drafting.md)` | derived | covered by seqpage.md:66. **NOT COVERED** by the registry row of the table at seqpage.md:183, which does not list `why-draft`. The value comes from the `reason:` on line 16, not from the stamp's `why-draft:` on line 22, and the two texts differ (see K8). |
| 7 | `faces := 01 draft` | derived | covered. The value form is shown only by example (Q9). |
| 8-9 | `type := general`, `axioms := -` | derived | covered (`-` means no such field, seqpage.md:188) |
| 10 | `lineage := 10.11.40.1001 < 10.11.40 < ...` | derived | covered (seqpage.md:88). The `<` form is not in seqAddr's grammar (Q9). |
| 11 | `source := book 10.11.40 @9` | derived | covered. The form is shown only by example. |
| 12 | (empty) | separator | covered |
| 13 | `--- @9 put 10.11.40.1001.00.draft` | block header | covered. The draft address `FF.draft` follows R8 (seqpage.md:109) and seqAddr.md:271. |
| 14-15 | `at:`, `by: user` | fields | covered (seqpage.md:147) |
| 16 | `reason: a new page starts as a draft (drafting.md)` | field | covered as "any other field" (seqpage.md:146). It is the R5 source (seqpage.md:109). |
| 17-23 | `\| ---` ... `\| ---` | body: front-matter stamp | covered as body (seqpage.md:166). The stamp form is a draft (face00.md:30, F9). |
| 24 | `\|` | empty body line | covered (seqpage.md:166) |
| 25-27 | `\| ## Registry`, `\| faces: 01 draft`, `\| why-01: ...` | body: registry card | covered as body. `why-NN` is a PROPOSED name (face00.md:171). |
| 28 | (empty) | separator | covered |
| 29 | `= 01 law 10.11.40.1001.01` | face section | covered (seqpage.md:106; the name is from seqAddr.md:150) |
| 30-32 | `state := draft`, `why-draft := ...`, `source := ...` | derived | covered (seqpage.md:184) |
| 34 | `--- @10 put 10.11.40.1001.01.draft` | block header | covered |
| 35-37 | `at:`, `by:`, `reason:` | fields | covered |
| 38 | `cards := cats` | derived under a block | covered (seqpage.md:186) |
| 39-43 | `\| ## cats` ... `\| means: ...` | body: a card with fields | covered (seqAddr.md:168-169). The card has no blank line between its fields and its body, because it has no body text. seqAddr.md:169 does not say whether that blank line is required. |
| 45-47 | `~ history`, `@9 put ...00.draft`, `@10 put ...01.draft` | history | covered. Each history line matches a block (seqpage.md:200). |
| 48 | `~ end` | end | covered (seqpage.md:202) |

Result: every line has a line kind. One placement (line 6) is not in the table that should list it, and one meaning (line 6 against line 22) is unsettled.

### Example B: 10.11.30.1501.timer.seq (168 lines, a workflow page with a counted face)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1-10 | magic, `= 00 registry ...`, derived lines | as in A | covered. Line 6 is `faces := 01 seated, 04 seated+draft, 05 counted, 06 counted`. |
| 12-16 | `--- @2 put 10.11.30.1501.00`, `at`, `by`, `proposal: p3`, `of: 3` | block, fields | covered. The field order `proposal` before `of` follows seqpage.md:146. |
| 17-23 | front-matter stamp in the body | body | covered. There is no `## Registry` card; face00.md:457 makes that a finding, not an error. |
| 25-27 | `= 01 law ...`, `state := seated`, `source := book 10.11.30 @3 @10 @11 @12 @13` | face section | covered. `source` lists several entries; the form is shown only by example. |
| 29-37 | `--- @3 put ...01`, fields, `cards := timer`, body `## Timer` | block | covered. The card key `timer` comes from the heading `Timer` in title form (seqAddr.md:168). |
| 39-41 | `--- @10 copy 10.11.30.1501.01` with no body | block | covered (seqpage.md:168: a block with no `\|` lines has no body). **NOT COVERED**: a `copy` opens a draft (seqpage.md:109), yet it is addressed to the seated face `...01`, not to `...01.draft`. R8 says a draft is addressed `FF.draft` (seqpage.md:109). The spec does not say whether a `copy` to the seated address is the R8 form or an exception. See Q5. |
| 43-46 | `--- @11 note ...01`, body one line | block | covered |
| 48-55 | `--- @12 merge ...01`, `cites: 11`, `cards := timer`, body | block | covered. `cites: 11` is compact JSON (seqpage.md:154) and refers to entry 11 (section 2.3, item 2). |
| 57-59 | `--- @13 promote ...01` | block | covered |
| 61-64 | `= 04 user ...`, `state := seated+draft`, `why-draft := ...`, `source := ...` | face section | covered (seqpage.md:108 lists `seated+draft`) |
| 66-76 | `--- @4 put ...04`, card `## Timer` with `\| source: [01 / Timer]` and `\| why: ...` | block | covered as body. **NOT COVERED** by the address grammar: `[01 / Timer]` is a reference form found only in seqAddr.md:179 (see 2.3, item 5). |
| 78-81 | `--- @15 copy ...04` with `reason:` | block | covered. This `reason:` feeds the `why-draft :=` on line 63 (seqpage.md:109). Like line 39, it is a copy to the seated address. |
| 83-86 | `--- @16 note ...04` | block | covered |
| 88-89 | `= 05 tasks 10.11.30.1501.05`, `counters := 01 closed` | face section | covered by R9 (seqpage.md:120). **NOT COVERED** by seqAddr.md:197-198, which says "A face is counted if and only if `FF.00` exists" and "A counter without a board is invalid". This file has no `05.00` and is still valid. See K4. |
| 91-93 | `== 05.01 10.11.30.1501.05.01`, `state := closed`, `source := ...` | counter section | covered (seqpage.md:121-122) |
| 95-104 | `--- @5 put ...05.01`, `tail: pack`, `cards := build-timer`, body with `lead: 3MC` and `axioms: 5` | block | covered as fields and body. **NOT COVERED**: the counter's tail is a field (`tail: pack`), while seqAddr.md:128 writes counter tails in the address (`PPPP.FF.NN.tail`). seqpage.md:109 refuses a `tail: draft` field on a seated face, so the two levels treat tails in opposite ways. See K6 and Q3. |
| 106-133 | four `--- @N tail ...05.01` blocks with `from:` and `to:`; the last has `to: ""` and `outcome: passed` | blocks | covered. `""` is the JSON string for "bare = closed" (seqpage.md:153; seqAddr.md:128). |
| 135-150 | `= 06 notes ...`, `counters := 01 closed`, `== 06.01 ...`, one put with card `## Session 2026-11-11` | face, counter, block | covered. The card key is `session-2026-11-11`. As with face 05, there is no `06.00` board. |
| 152-168 | `~ history` with 15 lines, then `~ end` | history | covered. History is in book order (@2 to @16). Blocks are grouped by section and kept in book order inside each section (seqpage.md:135), so the two orders differ, as designed. |

Result: every line has a line kind. Three points are not settled by the docs: the address of a `copy` that opens a draft, a counted face with no board, and where a counter's tail lives.

### Example C: proposals/10.11.21.1001.bob.seq (83 lines, a booked page plus one `new` block)

| Line(s) | Text, shortened | Kind | Against section 2 |
|---|---|---|---|
| 1-11 | magic, registry section, `why-draft := 7` | as in A | covered. `7` means the value could not be computed (seqpage.md:188). No reason was recorded, so this is a finding (seqpage.md:232). |
| 13-22 | `--- @7 put ...00.draft`, `proposal: prima-kernel-seed:10.11.21.1001`, stamp in the body | block | covered. The proposal value contains `:` and is still raw (seqpage.md:152 does not ban colons). There is no `## Registry` card and no `why-draft:` line, both findings (SEQ-GUIDE.md:491-492). |
| 24-44 | `= 01 law ...` with `why-draft := 7`; one draft block with cards `bob, cats` | face, block | covered. Lines 34-38 and 40-44 are two cards separated by a lone `\|` (line 39). |
| 46-66 | `= 04 user ...`; one draft block; the cards have `source: [01 / bob] ...` and `why: ...` | face, block | covered as body. `[01 / bob]` is the same uncovered reference form as B:73. Line 60 includes a `7` in its prose, which the grammar does not read (body text is never parsed, seqpage.md:169). |
| 68 | `= 06 notes 10.11.21.1001.06` | face section | covered. It has no derived lines; they are optional (seqpage.md:178). |
| 70 | `== 06.01 10.11.21.1001.06.01` | counter section | covered. **NOT COVERED** by seqAddr.md:198 (no `06.00` board), as in B. |
| 72-77 | `--- new put 10.11.21.1001.06.01`, body with no fields | `new` block | covered. It comes after the booked blocks (seqpage.md:136; there are none in this section). It carries no stamp fields (seqpage.md:148). The body address `10.11.21.1001.01.bob` (line 77) is a card address the grammar covers (seqAddr.md:271). |
| 79-83 | `~ history`, three lines, `~ end` | history | covered. The `new` block is not in the history (seqpage.md:201). |

Result: every line has a line kind. The derived `faces := 01 draft, 04 draft` (line 7) leaves out face 06, because the `new` block is not booked. That matches seqpage.md:84, since `faces` lists faces "the page has". The `[01 / bob]` reference and the boardless counter are not covered.

**Claude proposal.** In all three files, the line-kind grammar (section 2.2) covered every line. Every gap was in the meaning layer: addresses, tails, boards, references and value forms. The surface syntax looks settled. The open work is in what the lines mean.

---

## 4. How each axiom is kept

All cites in this section are @8e96151d. The axiom text is Axioms.md:13-29.

| # | Axiom (Axioms.md line) | Where the grammar keeps it | Gap |
|---|---|---|---|
| 1 | Authority (:13) | Import is only a proposal; "Nothing is written" (seqpage.md:215). A `new` block cannot carry compute stamps (seqpage.md:148; error `authority`, :227). A second registry section, or a field or entry written twice, is a `conflict` (seqpage.md:82, :226). | The file never checks a grant: who may propose to this page is left to the compute's later validation (seqpage.md:215). The proposer is named only at import (seqpage.md:239). The file cannot carry an axiom 1 halt between two live claims. |
| 2 | Fractal (:15) | The address inherits its ancestors (seqAddr.md:79), and finding walks book, shelf, desk, kernel (seqAddr.md:101-104). The file carries the chain as `lineage :=` (seqpage.md:88). The section shape repeats: a face section holds blocks, a counter section holds blocks, and both take `state :=` and `source :=` lines (seqpage.md:183-185). | Inherited faces are not shown (S2, seqpage-QUESTIONS.md:11-12). A reader cannot see "write only the difference" against the parent. The whole-book `.seq` of the design plan (PLAN:242, :288-298) does not reuse the page file's grammar, so the shape changes with scale (K1, Q1). |
| 3 | Leads (:17) | Faces map to readers: 01 agents, 02 model or compute, 03 compute, 04 users (seqAddr.md:150-153). Cards may carry `lead:`, as in timer.seq:101 `lead: 3MC`. A band page has a `lead` registry field (face00.md:205). | The `.seq` grammar has no lead field at block or section level. `lead:` lives only in body text, which the file does not read (seqpage.md:169). The default lead from the band or pack (Axioms.md:17) is not derived into the file. |
| 4 | Why (:19) | `why-draft :=` shows why a face is a draft (seqpage.md:109, R5). A 04 card needs a `why:` line (seqAddr.md:184). The `reason:` field records why on the entry (seqpage.md:109). | The place for the why is provisional (S7, seqpage-QUESTIONS.md:32). A missing why is only a finding (`why-draft := 7`, proposals/bob.seq:6). There are two whys for one draft (stamp against entry, K8). |
| 5 | Frame (:21) | A face 05 counter holds a pass's pack, claim, return, review and close (seqpage.md:121). The tails trace the pass (seqAddr.md:128). | The file has no structure for goal, why, stop or done-when. A pack is free text in a card body (timer.seq:100-104), so the grammar cannot check that a frame exists. |
| 6 | Lineage (:23) | Booked blocks keep book order. `new` blocks come after the past (seqpage.md:135-136). History only grows (seqpage.md:199). An edited past entry is refused with error `lineage` (seqpage.md:214, :228; SEQ-GUIDE.md:516-534). | Derived lines change in place (S1, seqpage-QUESTIONS.md:7-8), an agreed exception. Under the design plan, `~ history` would be replaced by face 09 (PLAN:455), and the core refuses face 09 today (TEST-2:196-197). |
| 7 | Missing (:25) | `7` is a value meaning "could not be computed", distinct from `-` (none written) (seqpage.md:188). A missing face is simply absent (seqpage.md:107). A missing registry, `~ end`, `at` or `by` is error `missing` (seqpage.md:224). A booked entry the book lacks is `missing 7.8` (seqpage.md:225). | Derived lines are optional when reading (seqpage.md:178), so a hand-written file that leaves one out raises nothing. That is fine for `:=` lines. Nothing marks a required body field as missing; that is left to face00.md's findings (face00.md:449-459). |
| 8 | Connection (:27) | A block must be on this page and in its section. A derived line that disagrees is refused, "a copy never becomes what it points to" (seqpage.md:134, :178). A file from another book, or a wrong header address, is error `connection` (seqpage.md:229). A file name with the wrong address is an error (seqpage.md:27). | Face 08 links are not designed (seqAddr.md:302). `lineage :=` leaves them out (S3). Nothing in the file checks a back-link (seqAddr.md:251). Body references such as `[01 / Timer]` are never checked (2.3, item 5). |
| 9 | Trial (:29) | The spec marks itself `9` (seqpage.md:3). R2 `trial` fields would be written like any other field with no format change (seqpage.md:146). | No line kind or field marks a block or face as `9`. Promotion (`promote`, timer.seq:57) carries no record of which hostile pass it survived. |

---

## 5. Conflicts in the docs

All cites in this section are @8e96151d unless marked otherwise. This section lists each conflict and does not resolve it.

| # | One side | Other side | What clashes |
|---|---|---|---|
| K1 | seqpage.md:11 "A `.seq` file holds one page" | PLAN:242 "A book is a .seq file", and PLAN:247 "one whole-book `.seq` file" | one page, or a whole book, under one extension |
| K2 | seqpage.md:13 "The book is the real copy (R3)"; SEQ-GUIDE.md:22 | PLAN:226 "R3 is updated by t175u: small files are stored"; PLAN:246 | what the store is, and so what the file is a view of |
| K3 | seqpage.md:31 "R4: plain ASCII only"; SEQ-GUIDE.md:343 | PLAN:319 "every other face may be stored as compact computer code (binary)"; PLAN:232 | whether non-04 faces stay ASCII. The plan applies its rule to stored faces; the spec applies R4 to the file. |
| K4 | seqAddr.md:197-198 "A face is counted if and only if `FF.00` exists", "A counter without a board is invalid"; seqAddr.md:44, :53, :277, :288 | seqpage.md:120 "Faces have no sentinels (R9): there is no `FF.00`"; SEQ-GUIDE.md:284 | the board at `FF.00` |
| K5 | seqAddr.md:149 face `00` name "identity" | seqpage.md:81-82 face 00 "is the registry"; the header `= 00 door` is refused | the name of face 00 |
| K6 | seqAddr.md:128 counter tail written in the address, `PPPP.FF.NN.tail` | seqpage.md:122 and timer.seq:98 counter state from a `tail: pack` field and `tail` op blocks, while seqpage.md:109 refuses a `tail: draft` field on a seated face | where a tail lives: in the address or in a field |
| K7 | seqAddr.md:158 face `09` "reserved, unassigned"; seqpage.md:199 `~ history` is the page's log | PLAN:449-455 "Face 09 is the page's log", taking "the place of today's derived `~ history` section" | the page log |
| K8 | face00.md:111 a draft page "carries `why-draft:`" in its stamp (cats.seq:22) | seqpage.md:109 `why-draft :=` comes from the `reason` field of the opening entry (cats.seq:6, :16) | two whys for one draft, with different text in the same file. face00.md:115 names both but does not say which governs. |
| K9 | seqAddr.md:189 face 03 "In a normal book it is allowed on the reserved pages (0001-0099)" | PLAN:435 "Any page may have a compute-written face 03 menu" (R35, 2) | where face 03 is allowed |
| K10 | face00.md:478 F12 "The core OpRequest has no `reason` field" (open); seqpage-QUESTIONS.md:32 "OpRequest has no `reason` field yet" | SEQ-GUIDE.md:598 "F12 closed: the core's request now has a `reason` field" | whether F12 is open |
| K11 | seqpage.md:86 says S9 is closed by R12 and R19 | seqpage.md:263 "Open: S1-S5, and new S7-S10 (... where title and type live ...)" | the same file says S9 is both closed and open. seqpage-QUESTIONS.md:40 says S9 is settled. |
| K12 | face00.md:214 band role "`N7` colab" | seqAddr.md:351 "Labs have their own band, `DD.SS.BB.0700-0799`" | what band digit 7 means |
| K13 | seqAddr.md:157 face 08 together with face 00 is "where the page's lineage is kept" | seqpage.md:88 `lineage :=` is only the address chain; face 08 links are not included (S3) | what lineage contains. face00.md:471 (F5) leaves it open. |
| K14 | seqAddr.md:149-158 faces 01 law, 03 operate, 06 notes, 07 reserved | kit docs/DESIGN.md:22, :24, :27, :28 @c09fa60c faces 01 agents card, 03 menu, 06 prime notes, 07 labs | The face names on wf pages, including this page (90.50.10.0702), are not seqAddr's names. DESIGN.md is a kit file, not a listed source. seqAddr.md:360 says face 07 stays reserved and lab links are on face 08. |
| K15 | seqpage.md:96 override pages in 0001-0009 (R7), S10 open (seqpage.md:263) | SEQ-GUIDE.md:562 "No override pages while we build the app. (R21)"; SEQ-GUIDE.md:597 S10 "parked by R21" | whether override pages exist now |

---

## 6. Open questions

Each question lists options. The option marked **(default)** is the fractal one, under axiom 2: "The same shape at every scale. Inherit what is agreed; write only the difference" (Axioms.md:15), per t384u.md:5 as the pack cites it. I have not opened t384u.md; it is not a listed source. Defaults are **Claude proposals**, not decisions. A default marks which option is fractal. It does not choose for Matthew (Axioms.md:13).

**Q1. One page or a whole book (K1, PLAN:1050-1053).**
- (a) `.seq` stays one page only, and a whole book gets another name or extension.
- (b) One extension with two shapes, told apart by a header marker (PLAN:1052).
- (c) **(default)** One grammar at every scale. A book file is the same line kinds, with the book's own door page (`DD.SS.BB.0000`, face 00 only, seqpage.md:93) as its registry section, then each page in address order, each in the page shape of section 2.

Why (c) is fractal: a book is identified by its page 0000 (seqAddr.md:56), just as a page is identified by its face 00 (seqAddr.md:64). It is the same shape one level up. Option (c) does not cover the plan's signpost lines (PLAN:288-298). They would stay derived, like `:=` lines.

**Q2. The board of a counted face (K4).**
- (a) The board is `FF.00`, as in seqAddr.md:197.
- (b) **(default)** There is no `FF.00`. The board is the derived line `counters :=` on the face section (seqpage.md:120).

Why (b) is fractal: it is the same form as `faces :=` on the registry section, a derived list one level up. It is also the later ruling (R9).

**Q3. Where a tail lives (K6).**
- (a) In the address at every level: `PPPP.FF.draft` and also `PPPP.FF.NN.pack`.
- (b) In a field or op at every level.
- (c) Mixed, as today: the address for drafts (R8), a field or op for counters.

**(default)** is (a). The tail is written the same way at page, face and counter level (seqAddr.md:126-128), and R8 already chose the address for faces (seqpage.md:109). Under (a), a counter's `tail` op would still record the move from one tail to the next, but the counter's tail would be read from the address.

**Q4. The name of face 00 (K5).**
- (a) `identity` (seqAddr.md:149).
- (b) **(default)** `registry` (R10, seqpage.md:81).

Why (b) is fractal: page 0000 is the book's registry, and face 00 is the page's registry. It is one word for the same role at each level, and it is the later ruling.

**Q5. A copy that opens a draft (example B, lines 39 and 78).**
- (a) A `copy` is addressed to the seated face, and opens `FF.draft` by its op.
- (b) **(default)** A `copy` is addressed to `FF.draft`, like every other write that opens a draft (R8).

Why (b) is fractal: one address form for every draft write.

**Q6. Which why governs a draft (K8).**
- (a) The stamp's `why-draft:` field.
- (b) **(default)** The `reason:` of the entry that opened the draft, at page and face level alike (seqpage.md:109). The stamp then holds no second copy.

Why (b) is fractal: axiom 2 says do not copy, and a second copy drifts. This is shown by cats.seq:6 against cats.seq:22.

**Q7. Page log: `~ history` or face 09 (K7).**
- (a) Keep `~ history` as a derived section.
- (b) **(default)** Face 09 is a face section `= 09 ...`, shaped like every other face, once the core allows face 09 (TEST-2:196-197).

Why (b) is fractal: the log becomes one more face instead of a special section. Until then, (a) stays as built.

**Q8. Inherited faces (S2, seqpage-QUESTIONS.md:11-12).**
- (a) Leave them out, as today.
- (b) Copy them in.
- (c) **(default)** A derived `inherits :=` line naming where each missing face resolves (seqpage-QUESTIONS.md:12).

Why (c) is fractal: the file inherits, writes only the difference, and points to the parent without copying it.

**Q9. Value forms of derived lines (2.2).**
- (a) Leave them as shown by example.
- (b) **(default)** Write each one in the address grammar where it names addresses: `lineage` as a list of container addresses (seqAddr.md:266), and `source` as a book address plus entry numbers. Then one grammar parses every address in the file.

**Q10. References inside the file and its bodies (2.3).**
- (a) Keep `[01 / Timer]` as the card reference in 04 bodies.
- (b) **(default)** Use the address grammar's active-relative form, `.01.timer` (seqAddr.md:270-271), for every card reference.

Also open: may `cites:` name an entry on another page or in another book? PLAN:1045-1047 (C10) proposes that cites name exactly what was relied on. The fractal default is the same rule as links: a full address for anything off the page.

**Q11. Leads and frame in the grammar (section 4, axioms 3 and 5).**
- (a) Keep them as body text.
- (b) **(default)** Allow `lead:` the same way `axioms:` is allowed on any card and on the stamp (seqAddr.md:172).

Why (b) is fractal: the same field at every level, with the default inherited from the band (face00.md:205).

**Q12. Face names on wf pages (K14).**
- (a) wf pages keep DESIGN.md's names.
- (b) **(default)** wf pages use seqAddr's face numbers and names, and write only the difference as a named override (Axioms.md:15).

This needs authority above the builder, and is raised here only.

**Q13. Whether lineage includes face 08 links (K13, F5).**
- (a) Only the address chain.
- (b) Only the authorization trail.
- (c) **(default)** Both, each as its own derived line, so neither copies the other.

---

## 7. Notes for the checker

- Every section, every claim and every cite is `9`.
- I did not run `seqpage check` or any code from 8e96151d. Every "covered" verdict in section 3 is my reading of the spec, not a tool result.
- I read four design files only in part. Section 0 gives the line ranges. A claim about those files cites only lines I read.
