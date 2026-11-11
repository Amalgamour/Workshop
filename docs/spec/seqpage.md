# The page file (.seq)

Status: **draft, `9`** (not yet through a hostile trial). Built by the SEQPAGE lane, 2026-11-11.
Governs: Director rulings R3 (this file type), R4 (plain ASCII), R5 (a draft shows why), R7 (override pages), R8 (draft address), R9 (no face sentinels), R10 (face 00 is the registry; page 0000 has only face 00). R1's door now names only the zero sequence on the desk, shelf, book and page axes (R9).
Implementation: `crates/seqpage` (library and the `seqpage` command). Open choices are marked `7` here and listed in `seqpage-QUESTIONS.md`.

---

## 1. What it is

A `.seq` file holds **one page** with all its faces, as plain text a person can read top to bottom.

- **The book is the real copy (R3).** A `.seq` file is a view: exported from a book, imported back.
- **Import is a proposal.** Importing never writes a book. New writes in the file become one proposal for the compute's queue (format.md 1.2, 4.1).
- **Lossless.** book -> `.seq` -> book gives back every entry of the page exactly: every field, every body, every entry number.
- **Append-friendly.** When the book gains entries, a fresh export only **adds** lines. The only lines that may change in place are derived lines (`key := value`, section 7), which are never imported.

## 2. File name

```
DD.SS.BB.PPPP.title.seq        10.11.21.1001.bob.seq
DD.SS.BB.PPPP.seq              00.00.00.0000.seq    (page 0000 has no title, A2.8)
```

- The address is the full page address. The title is the title field in face 00 (the registry), when it is a legal title word (seqAddr 3).
- A page without a title in its stamp has no title in its name.
- A name whose title disagrees with face 00's title is **elevated** to the user (A2.8), never fixed silently. A name whose address is not the page's address is an error (axiom 8).

## 3. Characters and lines

**R4: plain ASCII only.** Every character of a `.seq` file is printable ASCII `0x20`-`0x7E` or newline `0x0A`. Nothing else:

| Refused | Example | Write instead |
|---|---|---|
| tab | `U+0009` | spaces |
| carriage return | `U+000D` (Windows line ends) | newline only |
| accented letters | `e` with an accent, `U+00E9` | plain letters |
| em / en dash | `U+2014`, `U+2013` | `--` or `-` |
| curly quotes | `U+201C` `U+201D` `U+2018` `U+2019` | `"` and `'` |
| section sign | `U+00A7` | `section` |
| any other byte | emoji, control characters, bytes that are not UTF-8 | |

- The reader refuses the file at the **first** such character and names its line, column and code point (rule `R4`).
- A JSON escape cannot smuggle one in: a quoted value or JSON field whose decoded text holds a refused character is refused too (`"caf\u00e9"`, `"a\tb"`).
- Export refuses a book entry holding one, naming the entry (`@13 body holds U+00A7 ...`). Such a book is damaged under R4 and must be fixed in the book first.

The file is a sequence of lines, each ending in a newline. Line kinds, by how the line starts:

| Starts with | Kind |
|---|---|
| `seqpage 1` | magic line (line 1 only) |
| `= ` | face section header |
| `== ` | counter section header |
| `--- ` | block header |
| `key: ` | field (inside a block) |
| `key := ` | derived line (under a section header or block header) |
| `\|` | body line (inside a block) |
| `~ history` / `~ end` | history start / file end |
| `@` | history line (between `~ history` and `~ end`) |
| (empty) | separator |

Any other line is refused (`seqpage 3`).

## 4. The registry comes first (R10)

What face 00 holds (stamp, type, registry fields per type) is drafted in `face00.md` (DRAFT, R12, R19). The checker reports face 00 problems as findings, never errors (face00.md section 5). A draft face 00 also shows `why-draft :=` in the registry section.

```
seqpage 1
= 00 registry 10.11.21.1001.00
title := bob
state := draft
registry := draft
faces := 01 draft, 04 draft
type := general
axioms := -
lineage := 10.11.21.1001 < 10.11.21 < 10.11.00 < 10.00.00 < 00.00.00
source := book 10.11.21 @7
```

- Line 1 is `seqpage 1` (format and version). Line 2 opens the **registry section**: face 00, which on every page is the registry, the place that lists the page's faces (R10). It is not a sentinel (R9). It also holds the page's stamp (address, title, type, state, axioms, lineage) and its type field (R12, DIRECTOR-RULINGS.md:53-54; R19, :74-76; layout in face00.md, DRAFT). The page's address is read from this header.
- A file without a registry section first is refused (axiom 7). A second one is refused (axiom 1). The old header `= 00 door` is refused (axiom 8: wrong face name).
- Derived lines (section 7):
  - `faces :=` is what the registry lists: each face the page has, with its state (`counted` for a face with counters).
  - `registry :=` is the state of face 00 itself.
  - `title`, `type`, `axioms` are read from the stamp fields in face 00's body when present (`-` when not). Where they live is settled: S9 is closed by R12 ("The stamp should go in the .00 as the reg location", DIRECTOR-RULINGS.md:53-54) and R19 (face 00 holds the stamp, the type and a per-type registry, :74-76); see seqpage-QUESTIONS.md S9 and DECISIONS-LOG D151, D152. Still open: whether page state is the stamp `state:` or the page tail (DECISIONS-LOG D44, QUESTIONS-FOR-DIRECTOR QD08, kernel/QUESTIONS.md Q31), and the page 0000 title (face00.md F1). (Fixed by FOLLOWUPS, 2026-11-11; this line used to call S9 open.)
  - `state :=` is the page state from the core (`live`, `draft`, `retired`).
  - `lineage :=` is the address written down (axiom 6): the page, then the A1.8 lookup chain (book, shelf, desk, kernel). Face 08 links are not included (`7`, S3).
  - `kind :=` appears where a ruling names the page: `book door (R10: face 00 only)` on page 0000, `override (R7)` on pages 0001-0009.
- Then come the registry's blocks: every entry on face 00, and any entry on the page address itself (for example a page `tail` to `retired`).

### 4.1 Page 0000 has only face 00 (R10)
A book's door page `DD.SS.BB.0000` has face 00 and nothing else. A face section other than 00 in a 0000 file is refused (rule `R10`), and export refuses a book that has one (the book must be fixed first).

### 4.2 Override pages (R7)
A local override is its own page in 0001-0009. It states what it changes, why it is there, why it is needed and what it should achieve. The file marks such a page `kind := override (R7)`. Where those four statements sit (cards? fields?) is open (`7`, S10); the file does not check them yet.

## 5. Face sections

### 5.1 Faces
```
= 01 law 10.11.21.1001.01
state := draft
source := book 10.11.21 @8
```
- `= FF name DD.SS.BB.PPPP.FF`: the face number, its name from seqAddr 5.1 (`law`, `schema`, `operate`, `user`, `tasks`, `notes`, `map`, ...) and its seated address.
- Faces appear in number order, each once, and only when the page has entries on them. A missing face is simply absent: missing is a valid state (A4.6).
- `state :=` is the face slot's state from the core: `draft` (only `FF.draft`), `seated`, `seated+draft`, `retired`, `absent`.
- **Drafts (R8, R5).** A draft is addressed `DD.SS.BB.PPPP.FF.draft` and exists only while the face is being drafted (drafting.md: the copy that keeps seated work from being replaced from memory). Draft blocks sit in their face's section. A block that marks a face draft with a `tail: draft` field on the seated address is refused (rule `R8`). When the face is in draft, `why-draft :=` shows **why** (R5): the `reason` field of the entry that opened the draft (a `put` to `FF.draft` or a `copy`), else the first line of the first `note` on it, else `7` with a finding (rule `R5`). Where the reason is stored is provisional (S7).

### 5.2 Counters
```
= 05 tasks 10.11.30.1501.05
counters := 01 closed

== 05.01 10.11.30.1501.05.01
state := closed
source := book 10.11.30 @6 @7 @8 @9 @10
```
- **Faces have no sentinels (R9):** there is no `FF.00` and no `FF.99`. A counted face lists its counters and their tails in the derived line `counters :=`; that list is not an address.
- Each counter is a `== FF.NN address` section under its face header, in number order, with `NN` from 01 to 98. A counter section or block at `FF.00` or `FF.99` is refused (rule `R9`). Its blocks are every entry on that counter: the pack, the claim, the return, the review, the close.
- `state :=` on a counter is its tail word on the board (`draft`, `pack`, `open`, `return`, `review`, or `closed` for bare).

## 6. Blocks

A block is one write: either an entry already in the book, or a write you propose.

### 6.1 Block header
```
--- @8 put 10.11.21.1001.01        a booked entry: number, op, address
--- new put 10.11.21.1001.06.01    a proposed write: op, address
```
- `op` is one of the book ops: `put`, `tail`, `snapshot`, `copy`, `note`, `merge`, `promote`, `use`.
- The address must be on this page (axiom 8) and must belong to the section the block sits in (axiom 8).
- Booked blocks keep book order inside a section (axiom 6). An entry number appears once in the file (axiom 1).
- `new` blocks come **after** the booked blocks of their section: new work is added after the past, never in front of it (axiom 6).

### 6.2 Fields
```
at: 2026-11-11T19:30:00Z
by: prima-kernel-seed
tail: draft
proposal: prima-kernel-seed:10.11.21.1001
```
- One `key: value` line per field of the entry, after the header and before the body.
- Order: `at`, `by`, `tail`, `from`, `to`, `proposal`, `cites`, `outcome`, `of`, `state`, then any other field in name order. Fields the core adds later (for example R2's `approved_by` and `trial`) are written the same way with no change to this format.
- A booked block must have `at` and `by` (axiom 7).
- A `new` block **cannot** carry `at`, `by`, `n`, `proposal`, `of` or `state`: the compute stamps those when it books the write (axiom 1). The proposer is named once, at import.
- A field written twice is refused (axiom 1). A field that would not survive into the book entry (null, wrong type, unknown on a proposal) is refused.

### 6.3 Values
- A text value is written **raw** when it is plain: not empty, no leading or trailing space, does not start with `"`, and would not read as JSON (`12`, `true`, `null`, `[...]`, `{...}`).
- Otherwise it is written as a **JSON string**: `to: ""` (bare, closed), `count: "12"`.
- A number, true/false, list or object is written as **compact JSON**: `cites: 12`.
- Only this one form is accepted for each value, so a file has exactly one canonical text.
- A field whose key is not a lowercase word (`a-z`, `0-9`, `-`, `_`) is written `x: {"Key":value}`.

### 6.4 Body
```
| ## bob
| type: brand
| brand: bob.001
|
| ## cats
```
- Every body line starts with `| ` (bar, space). An empty body line is a lone `|`.
- The body is the face's Markdown exactly as in the book. **Cards are its `##` headings** (seqAddr 5.3): a card is a named block inside the face, with its field lines, a blank line, then its text.
- A block with no `|` lines has no body. A block with one lone `|` has an empty body.
- Because every body line is prefixed, nothing in a body can be mistaken for structure.

## 7. Derived lines

```
title := bob
cards := bob, cats
```
- `key := value` lines are **computed** on export and **checked** on read. They are never imported.
- They are optional when reading (a person writing a `new` block need not add any), but one that is present must match what the entries give, or the file is refused (axiom 8: a copy never becomes what it points to).
- The page's state is found by replaying the page's own entries through the core's rules (`BookState::apply`, default `Policy`). A page other than 0000 is replayed after a stand-in book door registry `DD.SS.BB.0000.00` that never appears in the file. If the entries do not replay, every state value shows `7` and the check reports it as a finding.

| Where | Lines |
|---|---|
| registry section | `title`, `state` (page: `live`, `draft`, `retired`), `registry` (face 00 slot), `faces`, `type`, `axioms`, `lineage`, `kind` (0000 and 0001-0009 only), `source` |
| face section | `state`, `why-draft` (when in draft), `source` (when the face has its own entries); `counters` (when it has counters) |
| counter section | `state`, `source` |
| block | `cards` (card keys in order; `7` if the body's cards do not parse) |

`-` means face 00 has no such field. `7` means it could not be computed.

## 8. History and end

```
~ history
@7 put 10.11.21.1001.00
@8 put 10.11.21.1001.01
@9 put 10.11.21.1001.04
~ end
```
- One line per booked entry, in book order: number, op, address. It is the page's line of writes across all faces, and it only grows (axiom 6).
- Every booked block has a history line and every history line has a block (axiom 7). They must agree on op and address (axiom 8).
- `new` blocks are not in the history: they are not booked yet.
- `~ end` is the last line. A file without it is cut off (axiom 7). Nothing may follow it.

## 9. Export

`export(book, page)` refuses a page whose book entries break R4, R8, R9 or R10, naming the entry; the book must be fixed first. Otherwise it takes every entry of the book whose address is on the page, in book order, and writes the layout above. Book-level entries (a `snapshot`, addressed to the book) belong to no page and stay in the book.

Reassembling a book from all its pages' files plus its book-level entries gives back the same entries, byte for byte (tested on every book in `books/` and `docs/spec/examples/sources/`).

## 10. Import

`import(file, book?, by)`:
1. Parse and check the file (sections 3-8).
2. With the book: every booked block must equal the book's entry with that number. An edited past entry is refused (axiom 6: change it with a `new` block). A booked number the book does not have is refused (axiom 7.8). A file from another book is refused (axiom 8). Book entries for the page that the file lacks are a finding: the file is behind; export again.
3. The `new` blocks, in file order, become the proposal `{"by", "ops": [...]}` of the lane contract (`POST /propose`). Nothing is written. The compute validates it like any other proposal and books it all or nothing.

## 11. Errors

Every error names its line, a code, the rule (`seqpage N` or `R4`, `A2.8`) and, where one applies, the axiom.

| Code | Axiom | When |
|---|---|---|
| `invalid` | - | malformed line or value; any character outside R4 (rule `R4`); a draft not addressed `FF.draft` (`R8`); `FF.00` or `FF.99` (`R9`); a face other than 00 on page 0000 (`R10`) |
| `missing` | 7 | no registry section, no `~ end`, no `at`/`by`, history and blocks do not match |
| `missing` | 7.8 | a booked block points at an entry the book does not have |
| `conflict` | 1 | second registry section, an entry or field written twice |
| `authority` | 1 | a `new` block carrying a compute stamp (`at`, `by`, `proposal`, ...) |
| `lineage` | 6 | blocks or history out of book order; `new` before booked; a booked entry that differs from the book |
| `connection` | 8 | a block on another page or in the wrong section; a derived line that disagrees; a header address or face name that is wrong; a file from another book |
| `elevate` | - | file name title differs from face 00's title (A2.8) |

Findings (reported, never blocking): a draft with no recorded reason (R5, axiom 7); the page has no face 00 entry (C1.1); the page's entries do not replay under the core; the file is behind its book; nothing to propose.

## 12. The command

```
seqpage export <book-file> <DD.SS.BB.PPPP> [--out FILE | --dir DIR]
seqpage export <book-file> --all --dir DIR
seqpage import <file.seq> [--book BOOK-FILE] [--by NAME] [--books DIR]
seqpage check  <file.seq> [--book BOOK-FILE]
```
JSON out; exit 1 on any error. `import --books DIR` also runs the core's `validate` as a dry run and prints its verdict; it still writes nothing.

## 13. Examples

| File | Shows |
|---|---|
| `examples/00.00.00.0051.seqaddr.seq` | the kernel page 0051 seqaddr, exported from `examples/sources/00.00.00.ruled.book`; every face is a draft with no recorded reason, so each shows `why-draft := 7` |
| `examples/10.11.21.1001.bob.seq` | the Bob test page: brand cards `bob` and `cats` on 01 with their 04 whys, as drafts |
| `examples/10.11.30.1501.timer.seq` | a workflow page: seated faces, a finished drafting cycle on 01 (`copy`, `note`, `merge` citing its note, `promote`), an open draft on 04 that shows its reason (R5), a task counter through `pack -> open -> return -> review -> closed`, a session note |
| `examples/proposals/10.11.21.1001.bob.seq` | the Bob page with one `new` block: session 2's note answering "what is my name" from the card. Imports to a one-op proposal that the core approves in a dry run. |
| `examples/proposals/10.11.21.1002.seq` | a hand-written file for a page not yet in the book: registry and 04 as `new` drafts (`.00.draft`, `.04.draft`) only. Imports to a proposal that creates the page. |

`examples/sources/` holds frozen copies of the books the examples come from, so the golden tests do not move while other lanes edit `books/`. They are put in the rulings' form by the SEQPAGE lane, provisionally, until KERNEL lands the same rulings in `books/`:
- `00.00.00.ruled.book`: the kernel book of 2026-11-11 with non-ASCII characters replaced (R4: `U+00A7` -> `section `, `U+2014` -> `--`, `U+2013` -> `-`, curly double quotes -> `"`), the entry `0000.04` dropped (R10), drafts readdressed `FF.draft` with no `tail` field (R8), entries renumbered. No text changed otherwise.
- `10.11.21.book`: the sample desk book, drafts readdressed (R8).
- `10.11.30.book`: hand-written for this document (`0000.04` dropped under R10).

**Regenerate after KERNEL and CORE land R5-R10:** the golden files depend on the core's replay (states) and on these frozen copies. When `books/` follows the rulings, re-copy the sources from `books/` and rerun `seqpage export` for each example; the golden tests show any difference.

## 14. Open (`7`)

See `seqpage-QUESTIONS.md`. Settled by rulings: S6 (R8). Open: S1-S5, and new S7-S10 (where a draft's reason lives; what face 00's body holds as the registry; where title and type live; the shape of an override page).
