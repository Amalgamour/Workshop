# Decisions index

state: draft. made: 2026-11-11, lane DESIGN.
why: each decision appears here once, with every place it is written, so repeats fold into one line.

**Status words**
- **spec**: settled by the spec. The spec's own "settled" marks, and S01-S12 as approved directions [decisions.md:621].
- **ruling**: settled by a Director ruling, R1-R4 [DIRECTOR-RULINGS.md].
- **open**: not settled. This covers proposed items, items the spec marks open, and settled items that are now in a clash or conflict. The O-number is the question in `OPEN.md`.

`rv#` is the number in Prima's 58-decision list [prima-review:24-97]. Citation keys are the same as in `DESIGN.md`.

## Rulings

| # | Decision | Sources | Status |
|---|---|---|---|
| D01 | The full-zero sequence on any axis (`00`, `0000`) is the door. Older words (owner, identity, sentinel, board) mean the same spot. | [R1]; replaces seqAddr.md:29,44,64, decisions.md:160,175; K01 | ruling |
| D02 | At this build stage, a face may be seated without the Director's eyes after a hostile trial from another view, recorded as `approved-by: build-stage (R2)`. Open questions stay with him. | [R2] | ruling (who counts as another view: O1) |
| D03 | The book is the real copy. A `.seq` file holds one page as a view, exported and imported, and import goes through the queue. The round trip loses nothing. | [R3] | ruling (layout: O22) |
| D04 | Stored files use printable ASCII plus newline only. Anything else is rejected on write, and a book holding it is reported damaged. | [R4]; answers core-trial 1 | ruling |

## Address

| # | Decision | Sources | Status |
|---|---|---|---|
| D05 | Seqaddr is a new file type: one page with many faces. | v2:5-7, seqAddr.md:7, format.md:12, AGENTS.md:33-34 | spec |
| D06 | Five axes, `2.2.2.4.2`: desk, shelf, book, page, face. Highest on the left. | v2:12-19, seqAddr.md:14-22; rv1 | spec |
| D07 | Widths are exact, never padded. | seqAddr.md:14, decisions.md:39; rv5 | spec |
| D08 | A counter `NN` follows a face only, runs 01-98, and is not an axis. | v2:33,37,40, seqAddr.md:24, decisions.md:36; rv4 | spec |
| D09 | The 4-digit page is the anchor, and groups read by position. Missing ancestors come from the active book. | seqAddr.md:71-86, decisions.md:14-30; rv2 | spec |
| D10 | No 4-digit group means a container address read from the desk. A sibling book is written `21.0000`. | seqAddr.md:89, decisions.md:33; rv3 | spec |
| D11 | A leading dot means the active page. If several pages are active, it goes to the user. | seqAddr.md:92, decisions.md:41-48; rv6 | spec |
| D12 | Users may use short form. Models write the full address and say it back, with where it was found. | seqAddr.md:95, decisions.md:51; rv7 | spec |
| D13 | One address space per repository, and each repository holds its own kernel. | seqAddr.md:41, decisions.md:253,265, format.md:15; rv32 | spec |
| D14 | Desk 00 is the kernel, 01-09 are kernel branches, 10-98 are users, and 99 is a pointer. | seqAddr.md:36-39, decisions.md:256-260; rv33 | spec |
| D15 | 01-09 (and 0001-0099) are reserved on every axis. | seqAddr.md:30 | open (O32; v2 clash 7 [prima-review:136]) |
| D16 | The address grammar. | seqAddr.md:264-291 | spec (title placement: O34) |
| D17 | A one-digit mark is an axiom, never an address part. | seqAddr.md:293, decisions.md:561, Axioms.md:5 | spec |

## Titles

| # | Decision | Sources | Status |
|---|---|---|---|
| D18 | A title starts at the first dot group that isn't strictly digits. | v2:22-29, seqAddr.md:110, decisions.md:69 | open (O34, held) |
| D19 | Title characters are lowercase letters, digits and hyphens, starting with a letter. | seqAddr.md:112, decisions.md:75; rv10 | spec |
| D20 | A title is a label, not identity, and pages may share one. | seqAddr.md:114, decisions.md:78; rv11 | spec |
| D21 | The stamp's title is the truth. A title in an address is checked against it, and a mismatch goes to the user. (Folds A2.4, A2.8 and A3.2.) | seqAddr.md:116, decisions.md:133,152; rv15 | open (O34, held: v2 clash 1) |
| D22 | Pages 1000 and up must have a title, 0001-0999 may, and 0000 has none. | seqAddr.md:115, decisions.md:131-132, v2:104; rv14 | open (K17 folded into O34; the 9999 exemption is O28) |
| D23 | Tail words are reserved and never titles or card keys. | seqAddr.md:113, decisions.md:88, seqAddr.md:280 | spec |

## Faces and cards

| # | Decision | Sources | Status |
|---|---|---|---|
| D24 | The face jobs: 01 law, 02 schema, 03 operate, 04 user why, 05 tasks, 06 notes, 07 reserved, 08 map. | v2:66-94, seqAddr.md:147-160, kernel-design.md:96-103; rv58 | spec |
| D25 | Face ranges: 09 is unassigned, 10-98 are for later, and 99 is reserved. | seqAddr.md:158-160, decisions.md:182-184; rv24 | spec |
| D26 | Face 00 holds the page stamp (address, title, state), and faces carry no stamp of their own. | seqAddr.md:64, decisions.md:176; rv23 | open (O2: v2:58 puts a stamp on every face) |
| D27 | A page needs face 00 plus one of 01-06 or 08. Face 07 doesn't count. | seqAddr.md:163, decisions.md:274; rv34 | open for door pages (O9) |
| D28 | Draft faces count, and a new page may start with only drafts. | seqAddr.md:164, decisions.md:277; rv35 | spec |
| D29 | Retiring the last content face retires the page, and derived paths update. | seqAddr.md:165, decisions.md:280; rv36 | spec |
| D30 | A card is a `##` heading. Its key is the heading in title form, the same key on two faces is the same card, and a face's contents are derived. | v2:60-61, seqAddr.md:168-170, decisions.md:298-301; rv38 | spec |
| D31 | Field lines come first, then a blank line, then the body. | seqAddr.md:169, decisions.md:508 | spec |
| D32 | Every 01 or 02 card has a 04 card with `why:` and a body (hard). A 04 that copies 01, or is missing its keywords, is a finding. | v2:75-76, seqAddr.md:175-185, decisions.md:339-357; rv39 | spec (across inheritance: O8) |
| D33 | When a 01 card and its 04 card disagree, it goes to the user, and neither governs. | decisions.md:357, decisions.md:575 | spec |
| D34 | User pages are mostly 04, which may hold user ideas with no 01 or 02. | v2:75-77, seqAddr.md:186, decisions.md:405 | spec |
| D35 | Face 03 is allowed in the kernel and desk books anywhere, and in normal books only on 0001-0099. | v2:71, seqAddr.md:189, decisions.md:404; rv43 | spec |
| D36 | Card types: each face has a default, and the types are defined in the kernel as kernel-only. | seqAddr.md:171, decisions.md:505-522; rv52 | spec (brand row: O17) |
| D37 | Page types live in the stamp and are defined in the kernel. The default is stamp, then band head, then `general`. | seqAddr.md:192-194, decisions.md:282-290; rv37 | spec (pointer split: O35) |
| D38 | Any card, and the stamp, may carry `axioms:`, and a cite permits nothing. | seqAddr.md:172, decisions.md:552-554, Axioms.md:5 | spec |
| D39 | Face 06 holds one note counter per session, recording the model, what it refers to, and why. | v2:83-87, seqAddr.md:155 | spec (fields: O37) |
| D40 | Face 08 holds the links: authority, dependencies, and what is needed to find and use the page. | v2:91-94, seqAddr.md:157, decisions.md:368; rv41 | open (how they are held: O36) |

## Tails and state

| # | Decision | Sources | Status |
|---|---|---|---|
| D41 | Counter tails: draft, pack, open, return, review. Bare means closed. | v2:44-51, seqAddr.md:128, decisions.md:96; rv12 | spec |
| D42 | Face tails: `FF.draft` is unseated, and `FF.retired` waits for removal. | v2:52-54, seqAddr.md:127, seqAddr.md:201; rv12 | spec |
| D43 | A seated face is bare `DD.SS.BB.PPPP.FF`, with no tail or counter. | v2:38-39, seqAddr.md:201, decisions.md:198 | spec (counted faces: O6) |
| D44 | Page tails are `draft` and `retired`. Containers take state from their door page. | seqAddr.md:126,129, decisions.md:99,172; rv13 | open (O5: stamp or tail) |
| D45 | Workflow state lives only on counters. | seqAddr.md:140, decisions.md:99; rv13 | spec |
| D46 | `draft` means "not active". | seqAddr.md:133 | open (O3: is a draft found?) |
| D47 | `retired` refuses `pack`, `open`, `return` and `review` without a counter. | seqAddr.md:287 | spec |

## Door, sentinels, counted faces, links

| # | Decision | Sources | Status |
|---|---|---|---|
| D48 | Every axis has two sentinels, all-0 and all-9, which are special spots and never normal pages. | v2:97-101, seqAddr.md:26-31 | spec + ruling (D01) |
| D49 | Page 0000 must exist for a book to be legal. | v2:102, seqAddr.md:290, decisions.md:143; rv21 | spec |
| D50 | Desk door `DD.00` and shelf door `DD.SS.00`, written as nested pages `DD.00.00.0000` and `DD.SS.00.0000`. | v2:105,108, seqAddr.md:58-62, decisions.md:145-149; rv21-22 | open (O14: v2 clash 4) |
| D51 | `DD.00.BB` is a desk book with no shelf. | v2:27, seqAddr.md:49, decisions.md:166 | spec |
| D52 | A face is counted only if `FF.00` exists. 05 and 06 are always counted, and others by page type. | seqAddr.md:197-200, decisions.md:196-199; rv25 | open (O6, O29) |
| D53 | A counted face is never seated, and plain `FF` means `FF.00`. | seqAddr.md:199, decisions.md:198; rv26 | open (O6: v2 clash 3) |
| D54 | `99` at every level is a pointer, never content. It lists every path onward in face 08, and many targets are allowed. | v2:106,109, seqAddr.md:249-250, decisions.md:213-227; rv28 | spec |
| D55 | Every target links back, and a one-way link is invalid. | v2:106, seqAddr.md:251, decisions.md:230; rv28 | spec |
| D56 | Direct links are the truth. Ancestor lists are derived and never hand-edited. | seqAddr.md:252, decisions.md:237; rv29 | spec |
| D57 | Missing is a valid state. | seqAddr.md:254, decisions.md:205; rv27 | spec |
| D58 | Overflow: `FF.99` goes to the next free page in the band, and `PP99` goes to the next free hundred. Bands never grow in place. | seqAddr.md:257-258, decisions.md:246-250; rv30-31 | spec (exact allocation: O47) |

## Book layout and bands

| # | Decision | Sources | Status |
|---|---|---|---|
| D59 | The kernel is the template for 0000-0999. 0100-0999 are standard bands, 1000-9998 are user space, and 9999 is continuation. | seqAddr.md:215-226, decisions.md:115-125; rv19 | spec |
| D60 | Below 0100: one reserved range or four. | decisions.md:120 vs seqAddr.md:220-223 | open (O24) |
| D61 | A page in 0001-0099 is a local override. | seqAddr.md:228, decisions.md:120 | spec |
| D62 | Page numbers read `NDNN`, where D is the band. Bands are 100 pages, and each `xx00` at 0100 and up is a band head. | seqAddr.md:233-242, decisions.md:102-111; rv16-17 | spec |
| D63 | Pages across bands form a set by matching numbers. | seqAddr.md:243, decisions.md:112; rv18 | open (O13: F.2 wants links both ways) |
| D64 | The dictionary is page 0012, face 03, counted, and it is only an index. | seqAddr.md:230, decisions.md:424-432, brands.md:15; rv47 | spec (03.00: O16) |

## Brands

| # | Decision | Sources | Status |
|---|---|---|---|
| D65 | A brand is one meaning of a word, `word.NNN` running 001-998, with a brand card. | brands.md:13-14, decisions.md:418,443; rv45 | spec |
| D66 | A word after a face is a card key, and a 3-digit group after it is a brand. | seqAddr.md:111, decisions.md:421, brands.md:47; rv46 | open (O12: v2 clash 5) |
| D67 | Brand cards hold forms (case-sensitive), meaning and meters. Only the compute writes meters, and they are exempt from drafting. | decisions.md:435-440,484, brands.md:51-61, drafting.md:39; rv48 | spec |
| D68 | Each book keeps its own dictionary, and the kernel gives a small base. | decisions.md:443, brands.md:78; rv49 | spec |
| D69 | The fixed dictionary layout `03.10-03.61` by letter share. Boundaries are estimates until checked. | decisions.md:446-481, brands.md:82-92; rv50 | spec |
| D70 | Resolving a word: meters, then the last used, then the default, then the ordinary meaning, and the assumption is stated back. | decisions.md:496-501, brands.md:65-70; rv51 | spec |
| D71 | A new meaning is asked for, then drafted by the compute, and the user's yes is its review. | decisions.md:503, brands.md:74, drafting.md:41 | spec |
| D72 | Keywords on cards are brands. | decisions.md:360; rv40 | spec |
| D73 | Failures count only against an assumed brand. | decisions.md:493 | open (O38) |
| D74 | Where a new brand card goes. | decisions.md:525 | open (O39) |

## Drafting

| # | Decision | Sources | Status |
|---|---|---|---|
| D75 | Never rewrite a face from memory. The 8 steps run copy, notes, merges, read again, then hand back for review. | drafting.md:7-18, decisions.md:309-318; rv53 | spec |
| D76 | A brand-new face starts as an empty draft and still goes through notes. | drafting.md:20 | spec |
| D77 | The compute enforces drafting with the ops copy, note, merge and promote. `put` only creates. | drafting.md:22-35, decisions.md:320-330, format.md:86-97 | open (O20) |
| D78 | Derived content is never drafted. | drafting.md:40, format.md:102 | spec |
| D79 | How review is recorded, and what happens on a reject. | drafting.md:45 | open (O1, O40) |

## Books and compute

| # | Decision | Sources | Status |
|---|---|---|---|
| D80 | A book is one file. Every container is a book file, and exporting is copying the file. | format.md:20-30; rv54 | spec |
| D81 | A book is an add-only log, and state is a replay. | format.md:60-67, Design.md:26; rv56 | spec |
| D82 | One JSON line per entry, line 1 is the header, and face bodies are Markdown. | format.md:69-81 | spec (draft entry shape: O11) |
| D83 | Boards, contents and ancestor lists are derived, never written. | format.md:102 | open (O6: clashes with format.md:123) |
| D84 | Snapshots let replay start late. | format.md:87,104-105 | open (O30) |
| D85 | One compute per repository owns every book. Reads are open, writes are proposals, and only the compute writes. | format.md:14-18, Design.md:47, AGENTS.md:39-42; rv55 | spec |
| D86 | First claim wins, because the queue approves one at a time. | format.md:42 | spec |
| D87 | Write lifecycle and validation checks. | format.md:109-125 | open (the section is marked proposed, format.md:109) |
| D88 | Proposals can hold several ops, all or nothing. | format.md:100 | open (O20) |
| D89 | Whatever the compute can't resolve goes to the user, never guessed. (Folds A1.6, A1.8, A2.8 and A3.2.) | format.md:131, seqAddr.md:104, decisions.md:56 | spec |
| D90 | The core and compute are in Rust, and the app is TypeScript with Next.js, using the core as WebAssembly. | format.md:137-149, Design.md:44-49, AGENTS.md:53; rv57 | spec |
| D91 | The compute boots from a small fixed contract before the kernel loads. | kernel-design.md:109-122, decisions.md:613 | open (O31) |
| D92 | The kernel defines agreements, the compute enforces them, the model reasons, and the person governs. | kernel-design.md:35, AGENTS.md:42, Axioms.md:13 | spec (kernel-design itself is proposed, :4) |
| D93 | Client transport, fork merging, hardware. | format.md:155-157, Design.md:96-97 | open (O42, O43, O46) |

## Finding

| # | Decision | Sources | Status |
|---|---|---|---|
| D94 | Find looks up book, shelf, desk, then kernel. The first match wins, and books follow the kernel live. (Folds A1.8 and A2.9.) | seqAddr.md:97-104, decisions.md:55,128; rv8, rv20 | spec (drafts: O3, override: O8, retired: O21) |
| D95 | A difference that contradicts the parent needs a named, approved override. | Axioms.md:15, decisions.md:398 | open (O8) |
| D96 | Authority runs desk, shelf, book, and a grant reaches only down. | decisions.md:390 | spec |
| D97 | User levels 00 (admin, kernel), 01 (power), and 04 (basic). | decisions.md:378-387 | spec for 00, 01 and 04; open for 02, 03 and 05-09 (O15) |

## Workflow loop

| # | Decision | Sources | Status |
|---|---|---|---|
| D98 | `.003` as a whole. | workflow-loop.003.md:3 | open (O7) |
| D99 | S01: bind every grant to an approval ID and an exact N4 revision. | decisions.md:627, workflow-loop.003.md:88 | spec |
| D100 | S02: evidence in proportion to risk. | decisions.md:628, workflow-loop.003.md:75,144 | spec |
| D101 | S03: close at the bare counter, and record the outcome (passed, failed, blocked, needs-authority, abandoned). | decisions.md:629, workflow-loop.003.md:166 | spec |
| D102 | S04: pack accepted, MVP done, and promotion are three separate things. | decisions.md:630, workflow-loop.003.md:89,219 | spec |
| D103 | S05: band counterparts are not continuations. | decisions.md:631 | spec |
| D104 | S06: a derived, read-only handoff manifest. | decisions.md:632, workflow-loop.003.md:220 | spec |
| D105 | S07: work-card keys are `w01`, `w02` and onward. | decisions.md:633, workflow-loop.003.md:126 | spec |
| D106 | S08: check targets by intent (depend, modify, create). | decisions.md:634 | spec |
| D107 | S09: count passes per frame, and track repeated blockers. | decisions.md:635, workflow-loop.003.md:260 | spec |
| D108 | S10: independent review, with a mandatory N7 trial for governing changes. | decisions.md:636, workflow-loop.003.md:199-200 | spec |
| D109 | S11: one valid claim, its owner, and recovery terms. | decisions.md:637, workflow-loop.003.md:206 | spec (details: O47) |
| D110 | S12: N4 questions and N5 packs are on separate boards, linked explicitly. | decisions.md:638, workflow-loop.003.md:92 | spec |
| D111 | Code lives in the repo, not in the book. | workflow-loop.003.md:70 | spec (Director, 2026-11-11) |
| D112 | The loop: draft, pack, open, return, review, closed. Lint and close are the compute's. | workflow-loop.003.md:163-177 | open (O7, O19) |
| D113 | Gravity: 1-3 passes is normal, pass 4 asks the why questions, and pass 6 halts. | workflow-loop.003.md:258-267 | open (O7, O48) |
| D114 | The workflow band map: 0300 build, 0400 dev, 0500 jobs, 0700 colab (F.2). | decisions.md:640-648, workflow-loop.003.md:40-49 | open (O13) |
| D115 | A return lives on its counter. | decisions.md:612, workflow-loop.003.md:181 | open (O26) |
| D116 | What written permission is. | decisions.md:594 | open (O25) |

## Axioms

| # | Decision | Sources | Status |
|---|---|---|---|
| D117 | The nine axioms, with their numbers and order. | Axioms.md:13-29, decisions.md:533-548 | spec |
| D118 | Cite grammar: a dot orders, a comma splits, and only 3 takes M, P or C. `7.8` is not `8.7`. | Axioms.md:5-7, decisions.md:558-566 | spec |
| D119 | The cold set before a write is `1.7.8`. | Axioms.md:9, decisions.md:564 | spec |
| D120 | Every piece of work has a lead. | Axioms.md:17, decisions.md:568-570 | spec |
| D121 | A 01 card is the packed form of its 04 card. | decisions.md:575 | spec |
| D122 | Lineage is kept with the page, on faces 00 and 08, by the compute. | decisions.md:577-582, seqAddr.md:157 | spec |
| D123 | Nothing is promoted without a hostile pass from another view. | Axioms.md:29, decisions.md:586-590 | spec (identity of the view: O1) |
| D124 | The axioms' page number and face names. | decisions.md:598, Axioms.md:3 | open (O10, O27) |
| D125 | The axioms are the shape, and seqaddr is the geometry. | AGENTS.md:27, Design.md:53, kernel-design.md:15 | spec |

## Proposals still waiting (E9)

| # | Decision | Sources | Status |
|---|---|---|---|
| D126 | A concordance (word to page). | decisions.md:606 | open (O18) |
| D127 | Face 05 task and ticket split, and patch and strike. | decisions.md:604-605 | open (O44, O45) |
| D128 | Link kinds, owner class, note fields. | decisions.md:609-611 | open (O36, O8, O37) |
| D129 | Does the kernel steer routing, or only hold agreements? | kernel-design.md:153-162 | open (O31) |

## Totals

Counted from the tables above. "spec + ruling" (D48) counts as spec.

- **spec:** 88
- **ruling:** 4
- **open:** 37
- **all:** 129

A spec row with an open part in brackets counts as spec. That part is asked in OPEN.md.
