# Conflicts in the spec

Places where spec files disagree, quoted with file and line (paths under `docs/spec/`). **None are resolved by the kernel.** Director rulings settle some (marked SETTLED or RESOLVED, with the ruling quoted). Each needs the Director (axiom 1: "Two live claims with no lawful connection: halt, and raise it to whoever holds more. Do not choose.").

Section A: spec file against spec file. Section B: workflow-loop `.002` against `.003` (the kernel page 0057 uses `.003`). Section C: where a Director ruling meets older text.

## A. Between spec files

### K01. What `00` / `0000` is called: owner, identity, sentinel, board - RESOLVED by R1
**Resolved:** `DIRECTOR-RULINGS.md:4-5` (R1, 2026-11-11): "a 00seq is the door 00 and 0000 are the same as a full zero sequence." ... "Older spec wording that calls it owner, identity, or board refers to this same location; use the word "door"." Kernel faces now say "door" (each change is a recorded merge in the page's 06.01 note). R9 later removed face sentinels altogether (no `FF.00`), and R10 made face 00 the registry. Quotes kept as history:
- `seqAddr.md:29` - "`00` / `0000` | the owner of the level above, itself [A4.1]"
- `seqAddr.md:64` - "A page is identified by its face 00, which holds the page stamp (address, title, state)."
- `decisions.md:119` - "`0000` | book identity (sentinel) |"
- `decisions.md:33` - "To refer to a sibling book in short form, use its sentinel page: `21.0000` is book 21 on the active shelf."
- `seqAddr.md:89` - "A sibling book in short form is written through its identity page: `21.0000`."
- `decisions.md:99` - "A container takes its state from its sentinel page" vs `seqAddr.md:129` - "state comes from the identity page"
- `seqAddr.md:53` - "`FF.00` | a counted face's board" (here `00` is a board, not an owner or identity)
- `review.md:132` - the Director's v2 page: "Faces listed 01-08 only; stamp is "header" on a face, not a separate face 00" (v2 page itself is not in docs/spec)

### K02. Boards must exist, but are never written - SETTLED
**Settled:** R9 (DIRECTOR-RULINGS.md:37) "Faces do not have sentinels. Only pages, books, shelves and desks." There is no `FF.00` to write or derive.
- `decisions.md:196` - "A face is counted **if and only if `FF.00` exists**. The board's presence is the check."
- `seqAddr.md:198` - "A counter without a board is invalid."
- `format.md:102` - "Boards (`FF.00`), contents lists and ancestor path lists are derived from the log and never written as entries (A4.4, A5.4)."
- `format.md:123` (same file) - "the target exists, or the write creates it legally (identity page first, board before counters)"
- Effect here: kernel 06 counters and the sample dictionary counters have no written board (build finding on each).

### K03. `03.00` on the dictionary: menu or board - HELD 7 (R16 vs R9)
**Held:** R16 (`DIRECTOR-RULINGS.md:65`) says "door"; R9 (`:37`) says faces have no sentinels. The pass-2 R9 strike of the `03.00` rows was undone in pass 3; the copied text stands (QUESTIONS Q29).
- `decisions.md:432` - "`0012.03.00` is the menu of sections." and `decisions.md:450` - "| `03.00` | menu |"
- `decisions.md:187` - "A counted face's `00` lists every counter and its current tail, like a kanban board"

### K04. Brand cards on face 01: 04 card required or not - SETTLED by R15
**Settled:** R15 (`DIRECTOR-RULINGS.md:62`) "No.": `:521` wins for brands. The builder skips C3.2 for `type: brand`; the sample's bob/cats 04 face was removed. No kernel 04 hole was a brand card, so the `4.7` count is unchanged (59).
- `decisions.md:353` - "| Every 01/02 card key has a 04 card | hard: the compute rejects the write |"
- `decisions.md:521` - "| `brand` | 01 | `brand`, `forms`, `means`, `meters` (compute) | no |" (column: "Needs a 04 card")

### K05. Reserved `01-09` on every axis vs counters and dictionary sections
- `seqAddr.md:30` - "| `01-09` / `0001-0099` | reserved |" (table title `seqAddr.md:26`: "Reserved values on every axis")
- `seqAddr.md:37` - "| `01-09` | kernel branches, downloaded into the repository as needed |"
- `decisions.md:36` - "Counters are not an axis, so the reserved 01-09 range does not apply to them."
- `decisions.md:451` - "| `03.01-03.09` | reserved: words starting with digits or symbols |"
- `decisions.md:481` - "This layout reserves `03.01-03.09` by its own definition. A1.4 (the reserved range does not apply to climbing counters) still stands."

### K06. Book layout below 0100: one range or four - SETTLED by R17 (split held 7)
**Settled:** R17 (`DIRECTOR-RULINGS.md:68`): four sections; 0000-0019 static, 0020-0099 working. The exact split is `7` (QUESTIONS Q30); quote appended to 0051.01 Book Layout.
- `decisions.md:120` - "| `0001-0099` | reserved; a page here is a local override of the inherited environment |"
- `seqAddr.md:220-223` - "`0001-0009` | special reserved pages", "`0010-0019` | contents, dictionary, concordance and other required pages", "`0020-0049` | localized behaviour", "`0050-0099` | structural pages, mostly in the kernel or templates"
- `review.md:116` already flags it: "pick one layout when condensing."

### K07. Band sets by number vs axiom 8 - SETTLED by R18 (see D10)
**Settled:** R18 (`DIRECTOR-RULINGS.md:71`): matched by CC plus title. Quote appended to 0051.01 Bands and 0057.01 Bound Bands.
- `decisions.md:112` - "**Sets across bands are linked by number.**"
- `decisions.md:250` - "This keeps A2.6 intact: fixed 100-page bands, every `xx00` a head, and sets linked by number."
- `seqAddr.md:243` - "Pages with the same `N` and `NN` in different bands form a set"
- `Axioms.md:27` - "Agreement is not connection: two pieces that match are not connected by matching"
- `decisions.md:644` (F.2, proposed) - "Membership requires explicit reciprocal Face 08 links."
- `workflow-loop.003.md:60` - "Under proposed F.2, membership requires reciprocal Face 08 links (axiom 8). This amends A2.6's current membership by number."

### K08. Which band digit is "build"
- `decisions.md:112` and `seqAddr.md:243` - "`0423.timer` (dev) and `0523.timer` (build)"
- `workflow-loop.003.md:44` - "| `0300-0399` (N3) | build |" and `:46` - "| `0500-0599` (N5) | jobs |"
- `decisions.md:645` (F.2, proposed) - "`0300` build, `0400` dev, `0500` jobs, and `0700` colab"

### K09. The axioms' faces - SETTLED
**Settled:** in part, by R6 (DIRECTOR-RULINGS.md:25): the axioms sit outside any book at `00.axioms` (working address `00.00.axioms`, `7`). Which faces they carry (Axioms.md:3 vs decisions.md:531) is still open.
- `Axioms.md:3` - "open `axioms/` for the faces: 01 agent form, 02 cite card, 03 menu, 04 full explanation, 06 notes."
- `decisions.md:531` - "`axioms/` (faces 00-04, notes 06.01)"
- `seqAddr.md:150-152` - "`01` | law", "`02` | schema", "`03` | operate" (general face jobs; "agent form" and "cite card" are not these names)
- `kernel-design.md:15` - "The Axioms (`Axioms.md`, decisions E1-E7)" while `decisions.md` E8 and E9 also belong to section E.

### K10. Identity pages must exist, but a page with only an identity has no reason to exist - SETTLED
**Settled:** R10 (DIRECTOR-RULINGS.md:40) "Page 0000.00 is the only location that exists." A door page has only face 00 and needs no content face.
- `decisions.md:143` - "Each desk, shelf and book has an identity page. Its stamp holds the container's title."
- `seqAddr.md:290` - "Containers need their identity page to be legal."
- `decisions.md:274` - "A page is valid when it has face 00 and at least one of faces 01-06 or 08. ... A page with only an identity has no reason to exist."
- No file names the content face of a page 0000. Effect here: sample identity pages are face 00 only (build finding); kernel 0000 got a 04 card copied from `kernel-design.md`.

### K11. The written address shape
- `decisions.md:18` - "`[DD.][SS.][BB.] PPPP [.FF][.NN] [.tail]`"
- `seqAddr.md:74` - "`[DD.][SS.][BB.] PPPP [.FF][.NN] [.title][.tail]`"
- `seqAddr.md:271` - "`face-part  = face [ "." counter ] [ "." tail ] [ "." card [ "." brand ] ]`" (card keys appear only in the grammar)

### K12. Where a return lives: settled or proposed
- `workflow-loop.md:170` (.002) - "This settles where a return lives."
- `decisions.md:612` (E9, "Proposals awaiting the Director") - "Where a return lives: on its counter"
- `workflow-loop.003.md:181` - "`7`: seat the E9 placement"

### K13. Pack-lint predecessor sits in a band the workflow does not use
- `workflow-loop.003.md:232` - "Consult the predecessor `0117.pack-lint`."
- `workflow-loop.003.md:43` - "| `0100-0299` | unassigned by this workflow |" (`.002`, `workflow-loop.md:43`: "| N1NN | not in use | |")

### K14. Written permission: decided in `.002`, open in decisions
- `workflow-loop.md:88` (.002) - "This revision-bound approval is written permission to act within the agreed frame"
- `decisions.md:594` (E8, open) - "\"Written permission\" (axiom 7): a recorded grant, or a direct instruction?"
- `workflow-loop.003.md:91` - "`7`: the general E8 definition of written permission remains open."

### K15. `.003` cites decision codes that are not recorded
- `workflow-loop.003.md:53,79,150,199,206,224,260` cite F02-F10 ("**F08.**", "**F06-F07.**", "**F10.**" ...).
- `decisions.md` section F has only F.1 (`:619`) and F.2 (`:640`). F02-F10 have no record (`7.8`). `workflow-loop.003-notes.md`, linked at `workflow-loop.003.md:16`, is not in docs/spec.

### K16. "door" in `.002` means a band head, not the zero sequence - SETTLED by R13
**Settled:** R13 (`DIRECTOR-RULINGS.md:56`): band heads are "band". Kernel faces copy `.003`, which already says "band head"; quote appended to 0051.01 Bands and 0057.01 Band Design.
- `workflow-loop.md:52` (.002) - "`N?00` is the door of each hundred-page band (for example `0400` or `1500`)"
- `workflow-loop.md:42` (.002) - "not a universal doors band"
- `DIRECTOR-RULINGS.md:5` (R1) - "on any axis, the full-zero sentinel (`00` for a 2-digit axis, `0000` for the page axis) is the **door**." `0400` is not all zeros. `.003:51` says "band head" instead. Raised in pass 2 (QUESTIONS.md Q9); answered by R13.

### K17. Does page 0000 have a title?
- `seqAddr.md:115` - "Page 0000 has none."
- `seqAddr.md:56` - "Every container is identified by a page 0000, whose stamp holds its title."
- `decisions.md:132` - "Page 0000 has none (it holds the book's title in its stamp)." The kernel door stamp carries `title: kernel` under this reading.

### K18. Are drafts live? - SETTLED
**Settled:** R5 (DIRECTOR-RULINGS.md:19) "Yes. Draft faces count and lookups find them." A seated face at the same spot wins.
- `seqAddr.md:133` - "| `draft` | being written; not active |"
- `seqAddr.md:164` - "Draft faces count and are allowed on any page. A new page may start with only drafts."
- `decisions.md:128` - "Anything a book does not override is found through the A1.8 lookup (book -> shelf -> desk -> kernel), so a kernel change reaches every book that has not overridden it."
- The builder reads `seqAddr.md:133` literally: a draft is not found by the lookup (QUESTIONS.md Q2).

## B. workflow-loop `.002` (`workflow-loop.md`) vs `.003` (`workflow-loop.003.md`)

`.003` line 4: "copy of: [root `.002` draft](workflow-loop.md)". Both are `state: draft`. Kernel page 0057 copies `.003`; `.002` stays as lineage.

| # | Topic | `.002` | `.003` |
|---|---|---|---|
| W01 | Authority line | `:6` "Director approved S01-S12 and four design choices" | `:6` "Director authorized drafting `.003`. ... Review and trial of `.003` remain due (`9`)." |
| W02 | Band map | `:38` "`N4` means `N400-N499` in any thousands band." `:42` "N0NN \| reserved / existing kernel allocation" (clashes with `decisions.md:125` "`1000` is the head of the first user band") | `:38` "The workflow map defaults within the standard range `0100-0999`" ... "A user band in `1000-9998` adopts a workflow role by name"; `:42` "`0000-0099` \| existing kernel allocation" |
| W03 | Set membership | `:64` "Matching subject digits establish a possible *set*, not continuation." | `:60` "membership requires reciprocal Face 08 links" (proposed F.2) |
| W04 | Compute role | `:30` "enforces grants, creates handoffs" | `:30` "enforces grants on its own writes, verifies external changes"; new F08 block `:79-81` |
| W05 | Written permission | `:88` "This revision-bound approval is written permission to act" | `:91` "`7`: the general E8 definition of written permission remains open." |
| W06 | Lead default | `:104` "if they differ from the band default (`3MC`)" | `:107` "`7`: no `3MC` workflow default is seated." |
| W07 | Risk | `:111` "risk/impact rating used to select evidence" | `:114` "lead's proposed risk. Compute records its floor"; new section 5.3 `:150-154`; new field "repository baseline" `:116` |
| W08 | Work-card example reason | `:132` "From a recorded, resolvable predecessor card ..." | `:135` "A person needs one place to inspect what the builder completed ..." |
| W09 | Review step | `:164` "\| 6 Review \| `return -> review` \| independent reviewer \|" | `:175` "\| 6 Review \| `return -> review` \| Compute on a valid reviewer claim \|"; review classes R1-R3 proposed `:200` |
| W10 | Return placement | `:170` "This settles where a return lives." | `:181` "uses the E9 proposal ... `7`: seat the E9 placement" |
| W11 | Abandoned claim | `:193` "closes it `abandoned` only after the recovery rule is met" | `:206` "Compute fences the old claim and records a system return on the same counter ... proceeds through `review` before closing" |
| W12 | Promotion manifest | none | new section 7.1 `:222-226` (F10) |
| W13 | Lint templates | `:211` "The template lives in the kernel as card types (decision C8.9)" | `:232` "This draft proposes kernel-owned card types under C8.9 ... `7`: seat the workflow card types" |
| W14 | Gravity | `:244-245` pass 4 why questions, pass 6 halt | `:262-269` adds pass 5 check, halt-reply allowance; `:260` counting event "each successful `draft -> pack` release consumes one pass" (proposed) |
| W15 | Open list | `:262-269` eight `7` items | `:286-295` ten `7` items plus "`9` **Trial**" |

## C. Where a ruling meets older text (rulings govern; listed so they can be checked)

Rulings govern over older spec wording (`DIRECTOR-RULINGS.md:1`). These are not reopened, only shown.

| # | Ruling | Older text |
|---|---|---|
| D1 | R9 `DIRECTOR-RULINGS.md:37` "Faces do not have sentinels. Only pages, books, shelves and desks." | Director's v2 page (`/workspace/prima/kernel-fresh/01.seqaddr/seqaddr.director.2026-11-09.v2.md:98,100`, not in docs/spec): "The sentinels exist in every axis of the design." ... "Two sentinels exist for every axis." Faces are axis 5 (v2:19). Also `decisions.md:196`, `:202`, `:246` (board, `FF.99`, counter overflow). `7`: what follows counter 98. |
| D2 | R5 `:19` "Draft faces count and lookups find them." | v2:53 "`FF.draft` Draft of a face not seated so not to be used as active."; `seqAddr.md:133` "being written; not active". |
| D3 | R6 `:25` "Axioms exist outside of the book as a 00.axioms on the desk." | v2:24 "DD.title after dot doesn't == next axis so it's a desk title", so `00.axioms` reads as desk 00 titled "axioms"; `seqAddr.md:36` "`00` | kernel. Its own book is `00.00.00`." The working address `00.00.axioms` reads as shelf `00.00` titled axioms, and "Shelf 00 and book 00 are never ordinary shelves or books" (`decisions.md:173`). Exact address `7`. |
| D4 | R7 `:31` "it exists in the reserved face pages of 0001-0009" | `seqAddr.md:228` "A page in `0001-0099` that exists in a book is a local override of the inherited environment."; Axioms.md:15 "A difference that contradicts the parent needs a named override, approved by the authority above it." R7 does not say who approves an override (`7`). |
| D5 | R10 `:40` "00 is a registry location on a page" (lists the page's faces) | `decisions.md:301` "A face's contents list is derived from its cards, never written by hand."; `format.md:102` "contents lists ... are derived from the log and never written as entries". The kernel writes the registry, and the builder checks it against the files. Whether the registry is written or derived is `7`. |
| D6 | R10 page 0000 has only face 00 | v2:104 "DD.SS.BB.0000 No title allowed." The kernel door stamps still carry `title:` (K17, open). |
| D7 | R4 `:16` plain ASCII only | The spec files themselves hold em dashes, section signs and arrows. Copied text was changed to ASCII (each page's 06.01 note gives the count). |
| D8 | R12 `:53` "The stamp should go in the .00 as the reg location." | v2:58 "Must have a stamp the as the header explaining the context and what face." (under "Face format", read as a stamp on every face). The kernel puts the stamp only in face 00 (R12); other faces carry no front matter. |
| D9 | R15 `:62` "No." (brand cards need no 04 card) | v2:75 "The cards of face 01 and 02 must have a representation on face 04."; `decisions.md:353` "Every 01/02 card key has a 04 card". |
| D10 | R18 `:71` "They are matched by the CC and the title." | `Axioms.md:27` "Agreement is not connection: two pieces that match are not connected by matching"; `decisions.md:644` (F.2, proposed) "Membership requires explicit reciprocal Face 08 links." Matching by CC plus title is a match, not a written link. |
| D11 | R18 example `N403.IDE-design` | `seqAddr.md:112` "Characters: lowercase letters, digits, hyphens." (A2.3). `IDE` is upper case; the kernel copies the quote as said. |
| D12 | R16 `:65` "door" (dictionary `03.00`) | R9 `:37` "Faces do not have sentinels." Held `7` (Q29). |
| D13 | R17 `:68` "Its broken into 4 sections." | `seqAddr.md:219-223` lists five rows (`0000`, `0001-0009`, `0010-0019`, `0020-0049`, `0050-0099`); `decisions.md:120` one row `0001-0099`. Split `7` (Q30). |
| D14 | R11 `:44` common questions "works like brands do" | `decisions.md` C8.9 card-type table has no `question` type. The sample uses `type: question` from crates/ask (COMPUTE); `7`. |
| D15 | R21 `:82-84` "No overrides for now. we build them in." | R7 `:31` overrides are pages in 0001-0009; `seqAddr.md:228`. The kernel keeps R7 text and code, adds "none while the Workshop app is built (R21)" to the 0051 law, refuses 0001-0009 pages in the builder, and parks sample `10.11.21.0001`. R7's approver question (D4) is deferred by R21. |
| D16 | R18 `:71` (title is part of the match) | `decisions.md:112` "Titles should match; a mismatch is elevated to the user (A2.8)." The pass-4 law drops the elevation clause; whether a same-CC, different-title pair is still elevated is QUESTIONS Q37. |
