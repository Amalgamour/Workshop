# Decisions log

state: draft. made: 2026-11-11, lane DECISIONS (Prima build), under Director ruling R22.
copied from: docs/design/DECISIONS-INDEX.md (D01-D129, lane DESIGN), then extended with every choice made in the build (D130 on).
why: R22 "make every design choice recorded" (DIRECTOR-RULINGS.md:86-88). One row per choice, with where it came from, so any summary can be checked against its source.

## How to read this

- **ID**: D01-D129 keep their numbers from DECISIONS-INDEX.md. D130 and up are new.
- **Choice**: the choice in one plain sentence.
- **Status** words:
  - `settled-by-ruling Rn`: a Director ruling settles it (DIRECTOR-RULINGS.md).
  - `settled-by-spec file:line`: the spec in docs/spec settles it.
  - `provisional 7 (LANE)`: the spec is silent; that build lane chose it so work could go on. It stays switchable until the Director rules.
  - `superseded by X`: replaced. Kept here, never deleted, so the history can be checked.
  - `open - QDnn`: not decided. QDnn is the question in docs/design/QUESTIONS-FOR-DIRECTOR.md.
  - `held - H1`: the Director dismissed this question card. Do not re-ask (OPEN.md O34).
- **Source**: file:line (paths under docs/spec/ unless shown), `BUILD-LOG:N` = docs/BUILD-LOG.md line N, a commit hash, or `chat tNNu` for a Director chat message. Rows copied from the index also carry `[DECISIONS-INDEX.md]`; their citation keys (v2, rv#) are the ones in docs/design/DESIGN.md.
- **Affects**: the pages, crates or app parts that follow the choice.
- Plain ASCII only (R4).

## 1. Addressing (axes, titles, doors, layout, bands, finding)

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D01 | The full-zero sequence on any axis (`00`, `0000`) is the door. Older words (owner, identity, sentinel, board) mean the same spot. | settled-by-ruling R1 (narrowed by R9: faces have no door) | [R1]; replaces seqAddr.md:29,44,64, decisions.md:160,175; K01 [DECISIONS-INDEX.md] | crates/seqaddr-core (Sentinel::Door, door_page); kernel 0051; app labels |
| D05 | Seqaddr is a new file type: one page with many faces. | settled-by-spec v2:5 | v2:5-7, seqAddr.md:7, format.md:12, AGENTS.md:33-34 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D06 | Five axes, `2.2.2.4.2`: desk, shelf, book, page, face. Highest on the left. | settled-by-spec v2:12 | v2:12-19, seqAddr.md:14-22; rv1 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D07 | Widths are exact, never padded. | settled-by-spec seqAddr.md:14 | seqAddr.md:14, decisions.md:39; rv5 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D08 | A counter `NN` follows a face only, runs 01-98, and is not an axis. | settled-by-spec v2:33 | v2:33,37,40, seqAddr.md:24, decisions.md:36; rv4 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D09 | The 4-digit page is the anchor, and groups read by position. Missing ancestors come from the active book. | settled-by-spec seqAddr.md:71-86 | seqAddr.md:71-86, decisions.md:14-30; rv2 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D10 | No 4-digit group means a container address read from the desk. A sibling book is written `21.0000`. | settled-by-spec seqAddr.md:89 | seqAddr.md:89, decisions.md:33; rv3 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D11 | A leading dot means the active page. If several pages are active, it goes to the user. | settled-by-spec seqAddr.md:92 | seqAddr.md:92, decisions.md:41-48; rv6 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D12 | Users may use short form. Models write the full address and say it back, with where it was found. | settled-by-spec seqAddr.md:95 | seqAddr.md:95, decisions.md:51; rv7 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D13 | One address space per repository, and each repository holds its own kernel. | settled-by-spec seqAddr.md:41 | seqAddr.md:41, decisions.md:253,265, format.md:15; rv32 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D14 | Desk 00 is the kernel, 01-09 are kernel branches, 10-98 are users, and 99 is a pointer. | settled-by-spec seqAddr.md:36-39 | seqAddr.md:36-39, decisions.md:256-260; rv33 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D15 | 01-09 (and 0001-0099) are reserved on every axis. | open - QD48 (O32) | seqAddr.md:30 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D16 | The address grammar. | settled-by-spec seqAddr.md:264-291; title placement held - H1 (O34) | seqAddr.md:264-291 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D17 | A one-digit mark is an axiom, never an address part. | settled-by-spec seqAddr.md:293 | seqAddr.md:293, decisions.md:561, Axioms.md:5 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; kernel 0051 |
| D18 | A title starts at the first dot group that isn't strictly digits. | held - H1 (O34, do not re-ask) | v2:22-29, seqAddr.md:110, decisions.md:69 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D19 | Title characters are lowercase letters, digits and hyphens, starting with a letter. | settled-by-spec seqAddr.md:112 | seqAddr.md:112, decisions.md:75; rv10 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D20 | A title is a label, not identity, and pages may share one. | settled-by-spec seqAddr.md:114 | seqAddr.md:114, decisions.md:78; rv11 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D21 | The stamp's title is the truth. A title in an address is checked against it, and a mismatch goes to the user. (Folds A2.4, A2.8 and A3.2.) | held - H1 (O34, do not re-ask) | seqAddr.md:116, decisions.md:133,152; rv15 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D22 | Pages 1000 and up must have a title, 0001-0999 may, and 0000 has none. | 0000 title held - H1; 9999 needs a title, enforced by CORE (A2.8, core-trial.md:172) | seqAddr.md:115, decisions.md:131-132, v2:104; rv14 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D23 | Tail words are reserved and never titles or card keys. | settled-by-spec seqAddr.md:113 | seqAddr.md:113, decisions.md:88, seqAddr.md:280 [DECISIONS-INDEX.md] | crates/seqaddr-core addr; face 00 stamp; kernel 0051 |
| D48 | Every axis has two sentinels, all-0 and all-9, which are special spots and never normal pages. | settled-by-ruling R1, narrowed by R9 (sentinels only on desk, shelf, book and page axes) | v2:97-101, seqAddr.md:26-31 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D49 | Page 0000 must exist for a book to be legal. | settled-by-spec v2:102 | v2:102, seqAddr.md:290, decisions.md:143; rv21 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D50 | Desk door `DD.00` and shelf door `DD.SS.00`, written as nested pages `DD.00.00.0000` and `DD.SS.00.0000`. | open - QD41 (O14) | v2:105,108, seqAddr.md:58-62, decisions.md:145-149; rv21-22 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D51 | `DD.00.BB` is a desk book with no shelf. | settled-by-spec v2:27 | v2:27, seqAddr.md:49, decisions.md:166 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D52 | A face is counted only if `FF.00` exists. 05 and 06 are always counted, and others by page type. | superseded by R9 (no FF.00); counted set provisional 7 CORE - QD11 | seqAddr.md:197-200, decisions.md:196-199; rv25 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D53 | A counted face is never seated, and plain `FF` means `FF.00`. | 'plain FF means FF.00' superseded by R9; 'never seated' superseded for face 05 by R22, R23, R24 (climb 05.CC, then seat 05); leftover (notes and dictionary) - QD01 | seqAddr.md:199, decisions.md:198; rv26 [DECISIONS-INDEX.md]; R22-R24 | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D54 | `99` at every level is a pointer, never content. It lists every path onward in face 08, and many targets are allowed. | settled-by-spec v2:106 | v2:106,109, seqAddr.md:249-250, decisions.md:213-227; rv28 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D55 | Every target links back, and a one-way link is invalid. | settled-by-spec v2:106 | v2:106, seqAddr.md:251, decisions.md:230; rv28 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D56 | Direct links are the truth. Ancestor lists are derived and never hand-edited. | settled-by-spec seqAddr.md:252 | seqAddr.md:252, decisions.md:237; rv29 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D57 | Missing is a valid state. | settled-by-spec seqAddr.md:254 | seqAddr.md:254, decisions.md:205; rv27 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D58 | Overflow: `FF.99` goes to the next free page in the band, and `PP99` goes to the next free hundred. Bands never grow in place. | FF.99 face overflow superseded by R9 (QD16); PP99 band overflow settled-by-spec seqAddr.md:258 | seqAddr.md:257-258, decisions.md:246-250; rv30-31 [DECISIONS-INDEX.md] | crates/seqaddr-core addr/state; kernel 0051, 0052 |
| D59 | The kernel is the template for 0000-0999. 0100-0999 are standard bands, 1000-9998 are user space, and 9999 is continuation. | settled-by-spec seqAddr.md:215-226 | seqAddr.md:215-226, decisions.md:115-125; rv19 [DECISIONS-INDEX.md] | crates/seqaddr-core PageKind; kernel 0051, 0057 |
| D60 | Below 0100: one reserved range or four. | settled-by-ruling R17 (four sections); exact split open - QD13 | decisions.md:120 vs seqAddr.md:220-223 [DECISIONS-INDEX.md] | crates/seqaddr-core PageKind; kernel 0051, 0057 |
| D61 | A page in 0001-0099 is a local override. | superseded by R7 (overrides only in 0001-0009) and R17; on hold by R21 | seqAddr.md:228, decisions.md:120 [DECISIONS-INDEX.md] | crates/seqaddr-core PageKind; kernel 0051, 0057 |
| D62 | Page numbers read `NDNN`, where D is the band. Bands are 100 pages, and each `xx00` at 0100 and up is a band head. | settled-by-spec seqAddr.md:233-242 | seqAddr.md:233-242, decisions.md:102-111; rv16-17 [DECISIONS-INDEX.md] | crates/seqaddr-core PageKind; kernel 0051, 0057 |
| D63 | Pages across bands form a set by matching numbers. | superseded by R18 (match by CC + title); elevation open - QD24 | seqAddr.md:243, decisions.md:112; rv18 [DECISIONS-INDEX.md] | crates/seqaddr-core PageKind; kernel 0051, 0057 |
| D64 | The dictionary is page 0012, face 03, counted, and it is only an index. | settled-by-spec seqAddr.md:230; 03.00 open - QD10 (R16 vs R9) | seqAddr.md:230, decisions.md:424-432, brands.md:15; rv47 [DECISIONS-INDEX.md] | 10.11.21.0012.03; kernel 0055; compute /brands |
| D94 | Find looks up book, shelf, desk, then kernel. The first match wins, and books follow the kernel live. (Folds A1.8 and A2.9.) | settled-by-spec seqAddr.md:97-104; drafts settled by R5; overrides R7/R21; retired pages QD18 | seqAddr.md:97-104, decisions.md:55,128; rv8, rv20 [DECISIONS-INDEX.md] | crates/seqaddr-core resolver; compute /resolve, /face |
| D95 | A difference that contradicts the parent needs a named, approved override. | settled-by-ruling R7 (override page); on hold by R21; approver deferred by R21 | Axioms.md:15, decisions.md:398 [DECISIONS-INDEX.md] | crates/seqaddr-core resolver; compute /resolve, /face |
| D96 | Authority runs desk, shelf, book, and a grant reaches only down. | settled-by-spec decisions.md:390 | decisions.md:390 [DECISIONS-INDEX.md] | crates/seqaddr-core resolver; compute /resolve, /face |
| D97 | User levels 00 (admin, kernel), 01 (power), and 04 (basic). | settled-by-spec decisions.md:378-387 for 00, 01, 04; others open - QD06 | decisions.md:378-387 [DECISIONS-INDEX.md] | crates/seqaddr-core resolver; compute /resolve, /face |
| D130 | Under R9, sentinels (all-0 and all-9) exist only on the desk, shelf, book and page axes. Faces have none. | settled-by-ruling R9 | DIRECTOR-RULINGS.md:37-38; core BUILD-LOG:95 | crates/seqaddr-core addr (sentinel() widths 2 and 4 only); kernel 0051, 0052 |
| D131 | Band heads (xx00 at 0100 and up) are called bands, because a band binds a set of pages into a work space. 'Door' is only the all-zero spot. | settled-by-ruling R13 | DIRECTOR-RULINGS.md:56-57; CONFLICTS.md K16 | kernel 0051.01, 0057.01 (quotes appended) |
| D132 | Below page 0100 the book has four sections: 0000-0019 static, 0020-0099 working pages (0020-0049 behavior, 0050-0099 structure). | settled-by-ruling R17 (exact split open - QD13) | DIRECTOR-RULINGS.md:68-69; ed908d5 | kernel 0051.01; core PageKind (unchanged) |
| D133 | Pages in different bands are one set when their CC (last two digits) and their title both match, e.g. N403.IDE-design and N503.IDE-design. | settled-by-ruling R18 | DIRECTOR-RULINGS.md:71-72 | core addr::same_set, BookState::set_of; kernel 0051.01, 0057.01 |
| D134 | R18 set titles are compared exactly. A title with capitals (the ruling's own example IDE-design) is refused by the title rule A2.3. | provisional 7 (CORE) - QD25 | BUILD-LOG:124; CONFLICTS.md D11 | crates/seqaddr-core addr |
| D135 | The kernel's Bands law drops the old 'title mismatch is elevated to the user' clause after R18. | provisional 7 (KERNEL) - QD24 | BUILD-LOG:151; kernel/QUESTIONS.md:191-194; CONFLICTS.md D16 | kernel 0051.01/04 |
| D136 | Lookup order is book -> shelf -> desk -> kernel (spec), not the contract's 'local, else kernel'. | settled-by-spec seqAddr.md:97-104; supersedes CONTRACT.md:16 | BUILD-LOG:9, 68 | crates/seqaddr-core resolver; compute /resolve, /face; app mock |
| D137 | The address grammar allows a title only at the end, so a word after DD, SS or BB (10.tools.21.4442) is invalid. | provisional 7 (CORE); title placement held - H1 | BUILD-LOG:43; OPEN.md O34 | crates/seqaddr-core addr |
| D138 | Card keys are made into title form: anything not a letter or digit becomes one hyphen; a key starts with a letter and is never a tail word. | provisional 7 (CORE) | BUILD-LOG:42 | crates/seqaddr-core cards |
| D139 | Page 9999 needs a title like any page 1000 and up. | settled-by-spec seqAddr.md:115 (A2.8) | core-trial.md:172; BUILD-LOG:102 | crates/seqaddr-core validate |
| D140 | 99 pointer pages take only faces 00 and 08, and a desk, shelf or book 99 is a pointer, never a user container. | settled-by-spec seqAddr.md:249-250 (A5.1) | core-trial.md:168; BUILD-LOG:102 | crates/seqaddr-core validate |
| D141 | The resolver skips a retired page (and every page of a book retired at its door) and walks on to the parent. | provisional 7 (CORE) - QD18 | BUILD-LOG:102, 104; kernel/QUESTIONS.md Q16 | crates/seqaddr-core resolver |
| D142 | A 9999 pointer that targets a book's door finds its back-link as a target: line in the door's face 00. | provisional 7 (CORE) - QD23 | BUILD-LOG:98; kernel/QUESTIONS.md Q26 | crates/seqaddr-core validate |
| D143 | A pointer's back-link is rechecked when the target face 08 changes or retires; a draft back-link counts (R5). | settled-by-spec seqAddr.md:251 (A5.3); draft part provisional 7 (CORE) - QD19 | core-trial.md:171; BUILD-LOG:102 | crates/seqaddr-core validate |
| D144 | The axioms are not a page in a book; they sit at desk level as 00.axioms. Working address 00.00.axioms. | settled-by-ruling R6 (exact address open - QD09) | DIRECTOR-RULINGS.md:25-26; BUILD-LOG:114 | kernel/00.00.axioms; books/00.00.axioms.jsonl; core (not modelled, BUILD-LOG:101) |
| D145 | The axioms were first put on kernel page 0050, the first structural page. | superseded by R6 | BUILD-LOG:18, 114 | kernel (old page 0050) |
| D146 | Kernel pages are numbered 0000, 0051 seqaddr, 0052 faces, 0053 tails, 0054 types, 0055 brands, 0056 drafting, 0057 workflow-loop; order inside 0050-0099 follows the brief. | provisional 7 (KERNEL) | BUILD-LOG:16, 18; kernel/MAP.md | kernel/00.00.00; books/00.00.00.book |
| D147 | The common questions list lives on page 0013, beside the dictionary on 0012. | provisional 7 (COMPUTE, KERNEL, APP) - QD27 | BUILD-LOG:128, 139, 161 | 10.11.21.0013; crates/ask; app /ask |
| D148 | The kernel builder refuses pages in 0001-0009 while the app is built. | settled-by-ruling R21 | CONFLICTS.md D15; fae009a | kernel/build.mjs |
| D149 | Pages are in a set across bands only by CC + title; F.2's 'reciprocal face 08 links' line is struck from the kernel's Bound Bands card. | settled-by-ruling R18 (CONFLICTS D10 kept for checking) | kernel-trial-2.md:276; CONFLICTS.md D10 | kernel 0057.01 |

## 2. Faces and cards (face jobs, face 00 registry, counted faces)

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D24 | The face jobs: 01 law, 02 schema, 03 operate, 04 user why, 05 tasks, 06 notes, 07 reserved, 08 map. | settled-by-spec v2:66 | v2:66-94, seqAddr.md:147-160, kernel-design.md:96-103; rv58 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D25 | Face ranges: 09 is unassigned, 10-98 are for later, and 99 is reserved. | settled-by-spec seqAddr.md:158-160 | seqAddr.md:158-160, decisions.md:182-184; rv24 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D26 | Face 00 holds the page stamp (address, title, state), and faces carry no stamp of their own. | settled-by-ruling R12 (stamp only in face 00; CONFLICTS D8) | seqAddr.md:64, decisions.md:176; rv23 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D27 | A page needs face 00 plus one of 01-06 or 08. Face 07 doesn't count. | settled-by-spec seqAddr.md:163; door pages settled by R10 (0000 holds only face 00) | seqAddr.md:163, decisions.md:274; rv34 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D28 | Draft faces count, and a new page may start with only drafts. | settled-by-spec seqAddr.md:164 | seqAddr.md:164, decisions.md:277; rv35 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D29 | Retiring the last content face retires the page, and derived paths update. | settled-by-spec seqAddr.md:165 | seqAddr.md:165, decisions.md:280; rv36 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D30 | A card is a `##` heading. Its key is the heading in title form, the same key on two faces is the same card, and a face's contents are derived. | settled-by-spec v2:60 | v2:60-61, seqAddr.md:168-170, decisions.md:298-301; rv38 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D31 | Field lines come first, then a blank line, then the body. | settled-by-spec seqAddr.md:169 | seqAddr.md:169, decisions.md:508 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D32 | Every 01 or 02 card has a 04 card with `why:` and a body (hard). A 04 that copies 01, or is missing its keywords, is a finding. | settled-by-spec seqAddr.md:175-185; brand cards exempt by R15; inherited 04 used (provisional 7 CORE) | v2:75-76, seqAddr.md:175-185, decisions.md:339-357; rv39 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D33 | When a 01 card and its 04 card disagree, it goes to the user, and neither governs. | settled-by-spec decisions.md:357 | decisions.md:357, decisions.md:575 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D34 | User pages are mostly 04, which may hold user ideas with no 01 or 02. | settled-by-spec v2:75 | v2:75-77, seqAddr.md:186, decisions.md:405 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D35 | Face 03 is allowed in the kernel and desk books anywhere, and in normal books only on 0001-0099. | settled-by-spec v2:71 | v2:71, seqAddr.md:189, decisions.md:404; rv43 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D36 | Card types: each face has a default, and the types are defined in the kernel as kernel-only. | settled-by-spec decisions.md:505-522; brand row settled by R15; question type - QD26 | seqAddr.md:171, decisions.md:505-522; rv52 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D37 | Page types live in the stamp and are defined in the kernel. The default is stamp, then band head, then `general`. | settled-by-spec seqAddr.md:192-194; type list open - QD02 | seqAddr.md:192-194, decisions.md:282-290; rv37 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D38 | Any card, and the stamp, may carry `axioms:`, and a cite permits nothing. | settled-by-spec seqAddr.md:172 | seqAddr.md:172, decisions.md:552-554, Axioms.md:5 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D39 | Face 06 holds one note counter per session, recording the model, what it refers to, and why. | settled-by-spec seqAddr.md:155; note fields open - QD51 | v2:83-87, seqAddr.md:155 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D40 | Face 08 holds the links: authority, dependencies, and what is needed to find and use the page. | open - QD50 (O36) | v2:91-94, seqAddr.md:157, decisions.md:368; rv41 [DECISIONS-INDEX.md] | crates/seqaddr-core cards/validate; kernel 0052; every page |
| D150 | Face 00 is the registry location on every page, not a sentinel. Page 0000 holds only face 00 and needs no content face. | settled-by-ruling R10 | DIRECTOR-RULINGS.md:40-41; BUILD-LOG:97 | core FaceJob::Registry, validate rule R10; seqpage; kernel every 00 |
| D151 | The stamp (address, title, type, state) lives in face 00. A page's state is kept in that stamp. | settled-by-ruling R12 | DIRECTOR-RULINGS.md:53-54; BUILD-LOG:121 | core (stamp read from 00); seqpage face00.rs; kernel every 00 |
| D152 | Face 00 holds the stamp portion, a type field, and a registry whose fields depend on the page type. | settled-by-ruling R19 (field sets are a draft) | DIRECTOR-RULINGS.md:74-76 | docs/spec/face00.md; crates/seqpage face00.rs; kernel every 00 |
| D153 | A brand card on face 01 needs no 04 card. | settled-by-ruling R15 | DIRECTOR-RULINGS.md:62-63; BUILD-LOG:123, 130 | core card table needs_04=false; kernel builder; sample 1001.04 removed |
| D154 | A stamp state: that is not live/draft/retired, or disagrees with what the faces give, is a finding, not a rejection. | provisional 7 (CORE) - QD08 | BUILD-LOG:121 | crates/seqaddr-core validate |
| D155 | Stamp fields: address, title, type, state, axioms (from the spec) plus two proposed: why-draft and lineage. | provisional 7 (SEQPAGE, face00.md PROPOSED) | face00.md:53-65 | face00.md; crates/seqpage face00.rs |
| D156 | Per-type registry fields: system owner, code repo, workflow role/set/approval, band role/default type/lead/contents/continues, pointer kind/index/layout, door level/parent/continues, override four statements + authorized-by. | provisional 7 (SEQPAGE, face00.md PROPOSED) - QD02 | face00.md:191-254 | face00.md; crates/seqpage face00.rs; kernel 0054 |
| D157 | A per-face draft reason is a why-NN line in face 00 (why-04: ...). | provisional 7 (SEQPAGE, face00.md PROPOSED) - QD38 | face00.md:171 | face00.md; kernel registry lines |
| D158 | The faces: list in face 00 is written by the compute and checked against the faces present; a mismatch is a finding. | provisional 7 (SEQPAGE) - QD03 | face00.md:173-181; seqpage-QUESTIONS.md:34-35 | face00.md; crates/seqpage |
| D159 | The core does not check face 00's list against the faces present. | provisional 7 (CORE) - QD03 | BUILD-LOG:98; kernel/QUESTIONS.md Q27 | crates/seqaddr-core |
| D160 | The kernel writes face 00 as front-matter stamp plus a ## Registry card listing the faces, and the builder checks it against the files. | provisional 7 (KERNEL) - QD03, QD29 | BUILD-LOG:116; face00.md:42-47 | kernel/build.mjs; every kernel 00 |
| D161 | Every face 00 check is a finding, never a block. An unknown type is a finding. | provisional 7 (SEQPAGE) - QD28 | BUILD-LOG:133; face00.md:439-459 | crates/seqpage face00.rs |
| D162 | In face 00, the value 7 means 'not known yet' and is never a mismatch. | provisional 7 (SEQPAGE) | face00.md:189 | crates/seqpage face00.rs |
| D163 | Page 0000's stamp title is the container's title, and it never appears in the address. | held - H1 (do not re-ask); provisional 7 (SEQPAGE F1) | face00.md:81-93, 465; CONFLICTS.md K17, D6 | face00.md; kernel door stamps |
| D164 | Faces carry no stamp of their own (the brief asked for one on every face; the spec was followed). | settled-by-spec decisions.md:176; confirmed by R12 | BUILD-LOG:22; CONFLICTS.md D8 | kernel every face |
| D165 | Missing whys are written as why: 4.7 and missing person-facing 04 bodies as a 7 hole, never filled in. | provisional 7 (KERNEL) | BUILD-LOG:21 | kernel 04 faces |
| D166 | A card stamp is --- front matter or leading field lines. | provisional 7 (CORE) | BUILD-LOG:42 | crates/seqaddr-core cards |
| D167 | C3.2 checks the newest view (draft if any, else seated) of 01/02 against 04; rule/schema cards need a 04 card; unknown card types are findings; bad axioms: chains are hard. | provisional 7 (CORE) | BUILD-LOG:41 | crates/seqaddr-core validate |
| D168 | C3.2 may use the inherited 04 face when the page has none of its own. | provisional 7 (CORE) | core-trial.md:179; BUILD-LOG:102 | crates/seqaddr-core validate; app card matching (BUILD-LOG:15) |
| D169 | C3.2 is skipped on counted 01/02 faces (counters are entries, not cards). | provisional 7 (CORE) - QD20 | BUILD-LOG:104; kernel/QUESTIONS.md Q20 | crates/seqaddr-core validate |
| D170 | The kernel builder checks C3.2 across the lookup and refuses in-place replacement of an inherited face. | provisional 7 (KERNEL) | kernel-trial-2.md:280; BUILD-LOG:150 | kernel/build.mjs, build.test.mjs |
| D171 | owner: kernel-only cards cannot be redefined in a book. | settled-by-spec decisions.md:287 (C1.4) | core-trial.md:167; BUILD-LOG:102 | crates/seqaddr-core validate |
| D172 | Counted faces are 05, 06 and Policy.extra_counted (default 0012.03). This replaced 'counted only if FF.00 exists'. | provisional 7 (CORE) - QD11 | BUILD-LOG:31, 95 | crates/seqaddr-core Policy |
| D173 | Plain FF on a counted face reads a derived counter listing (Found::Board, state board). | provisional 7 (CORE) | BUILD-LOG:95 | crates/seqaddr-core resolver |
| D174 | A counted face holds counters 01-98; counter 99 is refused and a full face takes no more. | provisional 7 (CORE) - QD16 | BUILD-LOG:96 | crates/seqaddr-core |
| D175 | Faces 07, 09 and 10-99 are refused as reserved. Face 03 outside kernel and desk books only on 0001-0099 is a hard rule. | settled-by-spec seqAddr.md:158-160, 189 (A4.3, C6) | BUILD-LOG:40; core-trial.md:137 | crates/seqaddr-core validate |
| D176 | FF.00 and FF.99 take no tail (written before R9). | superseded by R9 (FF.00 and FF.99 do not exist) | BUILD-LOG:32, 95 | crates/seqaddr-core |
| D177 | Boards: faces 05/06 always counted, the board derived, put to FF.00 refused. | superseded by R9 (no boards; counters listed under 'boards' as a view) | BUILD-LOG:31, 95; CONFLICTS.md K02 | crates/seqaddr-core; compute /page |
| D178 | Kernel door page 0000 carried a 04 card copied from kernel-design.md. | superseded by R10 (0000.04 removed) | BUILD-LOG:97, 116; CONFLICTS.md K10 | kernel 0000; books/00.00.00.book |
| D179 | The kernel base dictionary has no listed words, so page 0012 is not seated in the kernel. | provisional 7 (KERNEL) - QD64 | BUILD-LOG:20 | kernel 0012 |
| D180 | A question card is type: question with forms: and answer: (or 7 plus hole:); the builder accepts the question type. | provisional 7 (COMPUTE, KERNEL) - QD26 | BUILD-LOG:128, 139; CONFLICTS.md D14 | crates/ask QuestionCard; kernel/build.mjs; 10.11.21.0013 |
| D181 | The dictionary's 03.00 is a door (R16). This clashes with R9, so the kernel keeps the copied 03.00 menu text and builds nothing on it. | open - QD10 (R16 vs R9 held 7) | DIRECTOR-RULINGS.md:65-66; BUILD-LOG:131; CONFLICTS.md K03, D12 | kernel 0055.01/02/04; 10.11.21.0012.03 |
| D182 | Dictionary 0012.03.00 is treated as derived (format.md:102), not as written menu content. | provisional 7 (CORE) - QD10 | BUILD-LOG:44 | crates/seqaddr-core |
| D183 | Each page gets a face 05 that says what was learned and holds the work pack to reach that page's MVP, linking back to docs/design. That 05 is seated. | settled-by-ruling R22, R23, R24 (notes and dictionary leftover - QD01) | DIRECTOR-RULINGS.md:86-97; seqAddr.md:199 | every page; kernel; core counted-face rules |

## 3. Drafts, state and seating

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D02 | At this build stage, a face may be seated without the Director's eyes after a hostile trial from another view, recorded as `approved-by: build-stage (R2)`. Open questions stay with him. | settled-by-ruling R2; 'different view' settled by R20 | [R2] [DECISIONS-INDEX.md] | core + compute R2 gate; every seated face |
| D41 | Counter tails: draft, pack, open, return, review. Bare means closed. | settled-by-spec v2:44 | v2:44-51, seqAddr.md:128, decisions.md:96; rv12 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D42 | Face tails: `FF.draft` is unseated, and `FF.retired` waits for removal. | settled-by-spec seqAddr.md:127; draft address form settled by R8 | v2:52-54, seqAddr.md:127, seqAddr.md:201; rv12 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D43 | A seated face is bare `DD.SS.BB.PPPP.FF`, with no tail or counter. | settled-by-spec seqAddr.md:201; counted-face part changed by R9 (no FF.00) | v2:38-39, seqAddr.md:201, decisions.md:198 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D44 | Page tails are `draft` and `retired`. Containers take state from their door page. | partly superseded by R12 (page state in the face 00 stamp); stamp vs tail open - QD08 | seqAddr.md:126,129, decisions.md:99,172; rv13 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D45 | Workflow state lives only on counters. | settled-by-spec seqAddr.md:140 | seqAddr.md:140, decisions.md:99; rv13 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D46 | `draft` means "not active". | superseded by R5 (drafts are found and count; seated wins) | seqAddr.md:133 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D47 | `retired` refuses `pack`, `open`, `return` and `review` without a counter. | settled-by-spec seqAddr.md:287 | seqAddr.md:287 [DECISIONS-INDEX.md] | crates/seqaddr-core state; kernel 0053 |
| D75 | Never rewrite a face from memory. The 8 steps run copy, notes, merges, read again, then hand back for review. | settled-by-spec drafting.md:7-18 | drafting.md:7-18, decisions.md:309-318; rv53 [DECISIONS-INDEX.md] | kernel 0056; crates/seqaddr-core validate (D0); app draft screens |
| D76 | A brand-new face starts as an empty draft and still goes through notes. | settled-by-spec drafting.md:20 | drafting.md:20 [DECISIONS-INDEX.md] | kernel 0056; crates/seqaddr-core validate (D0); app draft screens |
| D77 | The compute enforces drafting with the ops copy, note, merge and promote. `put` only creates. | open - QD42 (O20); built as provisional 7 CORE (Policy.enforce_drafting) | drafting.md:22-35, decisions.md:320-330, format.md:86-97 [DECISIONS-INDEX.md] | kernel 0056; crates/seqaddr-core validate (D0); app draft screens |
| D78 | Derived content is never drafted. | settled-by-spec drafting.md:40 | drafting.md:40, format.md:102 [DECISIONS-INDEX.md] | kernel 0056; crates/seqaddr-core validate (D0); app draft screens |
| D79 | How review is recorded, and what happens on a reject. | who reviews settled by R2 + R20; what a reject does open - QD54 | drafting.md:45 [DECISIONS-INDEX.md] | kernel 0056; crates/seqaddr-core validate (D0); app draft screens |
| D184 | When the only copy of a face is a draft, lookup finds it and shows it as a draft. A seated face at the same spot wins. Drafts inherit book > shelf > desk > kernel. | settled-by-ruling R5 | DIRECTOR-RULINGS.md:18-20; BUILD-LOG:92 | core resolver (Found::Draft); compute /page, /face; app |
| D185 | A lookup shows why a face is a draft, not just that it is one. | settled-by-ruling R5 follow-up | DIRECTOR-RULINGS.md:28-29 | core why_draft; seqpage why-draft :=; app DraftState box |
| D186 | FF.draft exists only while a face is drafted, and is addressed ...PPPP.FF.draft. | settled-by-ruling R8 | DIRECTOR-RULINGS.md:34-35; BUILD-LOG:100 | core; seqpage (tail: draft refused); kernel book entries |
| D187 | A face may be seated while its page's door is still a draft. | settled-by-ruling R14 (which door - QD14) | DIRECTOR-RULINGS.md:59-60; BUILD-LOG:122 | crates/seqaddr-core door_first |
| D188 | A fresh session (a new subagent that did not build the face) is a different view for an R2 trial, even on the same model. A builder never trials its own work. | settled-by-ruling R20 | DIRECTOR-RULINGS.md:78-80 | all trials; R2 seats |
| D189 | Drafts were first booked as addr PPPP.FF plus a tail: draft field. | superseded by R8 | BUILD-LOG:50, 115 | kernel book entries |
| D190 | The kernel builder first read seqAddr.md:133 literally: drafts are not found. | superseded by R5 | BUILD-LOG:51; CONFLICTS.md K18 | kernel/build.mjs |
| D191 | /page first inherited only live faces, not drafts. | superseded by R5 (TRIAL-X finding 7 fixed: /page includes inherited drafts) | BUILD-LOG:57, 142 | crates/compute /page |
| D192 | Every new kernel face starts as FF.draft; nothing is seated without approval. | settled-by-spec drafting.md:20 | BUILD-LOG:17 | kernel/00.00.00 |
| D193 | Every door face is written as 00.draft. | provisional 7 (KERNEL) | BUILD-LOG:49 | kernel every 0000.00 and PPPP.00 |
| D194 | Face 00 was first a bare 00 file with state: draft inside. | superseded by 'every door face is 00.draft' (KERNEL pass 2) | BUILD-LOG:19, 49 | kernel |
| D195 | A new page from the app writes its door 00 as a draft too (00 + FF in one proposal). | provisional 7 (APP) | BUILD-LOG:82 | app draft screen |
| D196 | Drafting (D0) is enforced by default: a seated face changes only by copy, note, merge, promote; merge cites its note; promote needs every note struck. | provisional 7 (CORE) - QD42 | BUILD-LOG:36 | crates/seqaddr-core Policy.enforce_drafting |
| D197 | Promote had no review gate. | superseded by R2 gate (core-trial findings 2, 3 fixed) | BUILD-LOG:36, 93; core-trial.md:161-162 | crates/seqaddr-core |
| D198 | Seating (promote, a bare put of a non-counter face, or tail draft->bare) needs approved_by: director, or build-stage (R2) plus a trial reference. | settled-by-ruling R2; field names provisional 7 (CORE, COMPUTE) | BUILD-LOG:93, 141; CONTRACT.md:42 | core OpRequest.approved_by/trial; compute gate |
| D199 | The R2 gate runs in the compute ahead of the core (403, axiom 1) on every seating path. | provisional 7 (COMPUTE) | BUILD-LOG:141; CONTRACT.md:42 | crates/compute |
| D200 | An R2 trial reference must be docs/trial/NAME.md[#x], exist, and its author line must differ from the face's maker. | provisional 7 (COMPUTE) | BUILD-LOG:141; CONTRACT.md:42 | crates/compute |
| D201 | The compute's own bare puts (doors, derived pages) are exempt from seat approval; promote never is. | provisional 7 (CORE) - QD21 | BUILD-LOG:94 | crates/seqaddr-core validate |
| D202 | The app's seat screen asks the person to tick that the trial came from a different view. | provisional 7 (APP) | BUILD-LOG:80 | app /seat |
| D203 | An R2 seat is recorded as a seat-NN: line in face 00 (approved-by, trial, blob) and also on the book entry. | settled-by-ruling R25 (also on the book entry is provisional 7 KERNEL) | DIRECTOR-RULINGS.md:99-101; BUILD-LOG:149; kernel/QUESTIONS.md Q34, Q51 | kernel registry; books; 00.counter |
| D204 | First seats: 00.00.00.0056.01 (blob 112c169c) and 10.11.21.1001.01 (blob 5415cef2), under R2 + R20 after TRIAL-K2. | settled-by-ruling R2, R20 | 42ffbc9; BUILD-LOG:149; kernel-trial-2.md:24-28 | kernel 0056.01; 10.11.21.1001.01 |
| D205 | The kernel builder checks a seated face's git blob and refuses to build if a seated face changes. | provisional 7 (KERNEL) | 42ffbc9; BUILD-LOG:149 | kernel/build.mjs |
| D206 | Draft reason: an optional reason field on the request, stored on the entry; read only from the entry that opens a draft (copy or put FF.draft). | provisional 7 (CORE) | BUILD-LOG:118 | core OpRequest.reason, Entry.reason, why_draft.reason |
| D207 | In a .seq file, a draft's reason is the reason field, else the first note line, else 7 plus a finding. | provisional 7 (SEQPAGE) - QD38 | seqpage-QUESTIONS.md:30-32; BUILD-LOG:111 | crates/seqpage |
| D208 | Every kernel draft gives its reason on its registry line and in the reason field of its book entry. | provisional 7 (KERNEL) | BUILD-LOG:113, 132 | kernel; books |
| D209 | why_draft shape is {opened_by_entry, has_seated, open_notes, merged_notes, reason}. | provisional 7 (CORE) | BUILD-LOG:92, 118 | crates/seqaddr-core Resolution |
| D210 | A counter in draft is not live, so a page whose content is only drafts is a draft page (C1.2). | settled-by-spec seqAddr.md:164 (C1.2) | BUILD-LOG:76, 103 | crates/seqaddr-core PageState |
| D211 | A counter is created bare, draft or pack; put never replaces a draft counter (default). | provisional 7 (CORE) - QD15 | BUILD-LOG:33, 102; core-trial.md:177 | crates/seqaddr-core Policy.draft_counter_put_replaces=false |
| D212 | put on a counter still in draft replaced its body. | superseded by core-trial finding 18 fix (default false) | BUILD-LOG:33, 102 | crates/seqaddr-core |
| D213 | Faces retire only from seated; a retired face blocks a new put; page draft state is derived, not a tail op. | provisional 7 (CORE) | BUILD-LOG:35 | crates/seqaddr-core |
| D214 | No draft on a retired face and no promote that re-seats it. | provisional 7 (CORE) | core-trial.md:169; BUILD-LOG:100, 102 | crates/seqaddr-core |
| D215 | The tail op names the slot without a tail; bare is empty in from/to (no 'closed' word). | settled-by-spec format.md:76 (core-trial says the spec agrees) | BUILD-LOG:34; core-trial.md:131 | crates/seqaddr-core |
| D216 | Claims: id claim-{n}; owner is the author of pack->open; only the owner returns; the reviewer must differ from the builder; review->bare needs an outcome. | provisional 7 (CORE); S10, S11, S03 settled-by-spec | BUILD-LOG:37 | crates/seqaddr-core state; compute; app /work |
| D217 | The reviewer is the author of the return->review tail op. | provisional 7 (CORE) | BUILD-LOG:45 | crates/seqaddr-core |
| D218 | Only the compute lints draft->pack and closes review->closed. | settled-by-spec workflow-loop.003.md section 6 | core-trial.md:163; BUILD-LOG:102 | core Policy.compute_only_steps |
| D219 | The compute may not return someone else's open claim unless Policy.compute_recovery_return is on (off by default). | provisional 7 (CORE) - QD22 | core-trial.md:170; BUILD-LOG:102 | crates/seqaddr-core |
| D220 | POST /close lets a counter's reviewer ask the compute to close a review. | provisional 7 (COMPUTE) | BUILD-LOG:144; CONTRACT.md:49 | crates/compute; app /work |
| D221 | Closing a review was posted by the person writing. | superseded by compute-only close + POST /close | BUILD-LOG:84, 144 | app /work |
| D222 | The section 8 workflow lint template is not built; draft->pack is offered with a note saying so. | provisional 7 (CORE, APP) | core-trial.md:163; BUILD-LOG:83 | core; app /work |
| D223 | A new job number is the highest existing 05.NN + 1; the compute validates. | provisional 7 (APP) | BUILD-LOG:83 | app /work |
| D224 | Counters and boards of counted faces inherit down the chain like any face (current core). | provisional 7 (CORE) - QD17 | core-trial.md:165; kernel/QUESTIONS.md Q15 | crates/seqaddr-core resolver |
| D225 | A counted face (05, 06, dictionary sections) is not seated by R2 while 'a counted face is never seated' stands; R22 asks for a seated 05. | settled-by-ruling R22, R23, R24 (leftover notes 06 and dictionary open - QD01) | kernel/QUESTIONS.md Q35; DIRECTOR-RULINGS.md:86-97 | kernel 0053.06.01, 0054.06.01, 0056.06.01, 0012.03.14/16; every 05 |

## 4. Storage and the .seq page file

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D03 | The book is the real copy. A `.seq` file holds one page as a view, exported and imported, and import goes through the queue. The round trip loses nothing. | settled-by-ruling R3; layout provisional 7 (SEQPAGE, seqpage.md) - QD34 | [R3] [DECISIONS-INDEX.md] | crates/seqpage; compute /page.seq; app export/import |
| D04 | Stored files use printable ASCII plus newline only. Anything else is rejected on write, and a book holding it is reported damaged. | settled-by-ruling R4 (may widen later - QD63) | [R4]; answers core-trial 1 [DECISIONS-INDEX.md] | all crates; kernel; books; app |
| D80 | A book is one file. Every container is a book file, and exporting is copying the file. | settled-by-spec format.md:20-30 | format.md:20-30; rv54 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D81 | A book is an add-only log, and state is a replay. | settled-by-spec format.md:60-67 | format.md:60-67, Design.md:26; rv56 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D82 | One JSON line per entry, line 1 is the header, and face bodies are Markdown. | settled-by-spec format.md:69-81; draft entry shape settled by R8 | format.md:69-81 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D83 | Boards, contents and ancestor lists are derived, never written. | settled-by-ruling R9 (no boards to write); contents lists open - QD03 | format.md:102 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D84 | Snapshots let replay start late. | open - QD46 (O30); built provisional 7 CORE (snapshots verified) | format.md:87,104-105 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D87 | Write lifecycle and validation checks. | open (format.md:109 marks it proposed); built provisional 7 CORE | format.md:109-125 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D88 | Proposals can hold several ops, all or nothing. | open - QD42 (O20); built provisional 7 CORE (proposal/of) | format.md:100 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D226 | Plain ASCII is enforced everywhere: write refused (rule R4), a book holding a bad byte (raw or JSON-escaped) is damaged, and repair will not cut it away. | settled-by-ruling R4 | BUILD-LOG:90, 71; core-trial.md:160 | core validate/log; seqpage parser; kernel builder; compute 422 |
| D227 | Kernel and sample text was changed to ASCII; each page's 06.01 note gives the count. | settled-by-ruling R4 | CONFLICTS.md D7; BUILD-LOG:113 | kernel; books |
| D228 | Frozen example sources were cleaned with a fixed map: section sign -> 'section ', em dash -> '--', en dash -> '-', curly quotes -> straight quotes. | provisional 7 (SEQPAGE) | seqpage.md:255 | docs/spec/examples/sources |
| D229 | A multi-op proposal's entries carry proposal and of; a trailing proposal cut short is dropped whole on read. | provisional 7 (CORE) (proposal id settled-by-spec format.md:100) | BUILD-LOG:38; core-trial.md:135 | crates/seqaddr-core log |
| D230 | A snapshot carries full state; replay checks every snapshot against the log and never trusts a snapshot over it. | settled-by-spec format.md 3.4 (snapshot use open - QD46) | core-trial.md:164; BUILD-LOG:38, 102 | crates/seqaddr-core replay |
| D231 | Door first: nothing is written in a book until DD.SS.BB.0000.00 exists. | settled-by-spec format.md 4.1 | BUILD-LOG:39 | crates/seqaddr-core validate |
| D232 | C1.1 (a page needs a content face) applied to page 0000. | superseded by R10 (Policy.c1_on_door_pages default false) | BUILD-LOG:39, 97, 106 | crates/seqaddr-core Policy |
| D233 | A proposal writes one book only (cross-book transactions open). | provisional 7 (CORE) - QD61 | BUILD-LOG:40 | crates/seqaddr-core validate |
| D234 | A cut header is repaired to empty; timestamps are checked as real times. | provisional 7 (CORE) | core-trial.md:174-175; BUILD-LOG:102 | crates/seqaddr-core log |
| D235 | The kernel seed timestamp is fixed at 2026-11-11T19:30:00Z, one proposal id per page, so builds are byte-for-byte repeatable. | provisional 7 (KERNEL) | BUILD-LOG:24, 28 | kernel/build.mjs |
| D236 | The core is not yet built as WebAssembly (no wasm32 std on the box); the app does no validation of its own. | provisional 7 (CORE, COMPUTE, APP) | BUILD-LOG:7, 46, 66 | crates/seqaddr-core; app |
| D237 | Import never writes: new blocks become a normal proposal; booked blocks must equal the book's entries (axiom 6) or point at real ones (7.8). | settled-by-ruling R3 | BUILD-LOG:70; seqpage.md:210-214 | crates/seqpage; compute POST /propose text/x-seqpage |
| D238 | Derived lines (key := value) may change in place between exports, are checked on read, and are never imported; every other line only grows. | provisional 7 (SEQPAGE) - QD34 | BUILD-LOG:72; seqpage-QUESTIONS.md:5-8 | crates/seqpage |
| D239 | Derived state comes from replaying only the page's entries through the core after a stand-in door; on failure the values show 7. | provisional 7 (SEQPAGE) | BUILD-LOG:73 | crates/seqpage |
| D240 | The .seq field codec is generic over the entry, so fields the core adds later round-trip unchanged. | provisional 7 (SEQPAGE) | BUILD-LOG:74 | crates/seqpage |
| D241 | A .seq holds only the page's own entries in its own book; inherited faces and face 08 links are not included; lineage := is the address chain. | provisional 7 (SEQPAGE) - QD35, QD30 | BUILD-LOG:75; seqpage-QUESTIONS.md:10-16 | crates/seqpage |
| D242 | A .seq file starts with the registry section (face 00). The old '= 00 door' header is refused. | settled-by-ruling R10 | seqpage.md:64-82; BUILD-LOG:108 | crates/seqpage |
| D243 | In .seq: page 0000 holds only face 00; counter sections at 00 or 99 are refused; 'board :=' is renamed 'counters :='; tail: draft on a seated address is refused; 0001-0009 pages are marked kind := override (R7). | settled-by-ruling R8, R9, R10, R7 | BUILD-LOG:108 | crates/seqpage src/rulings.rs |
| D244 | File name is DD.SS.BB.PPPP.title.seq (or without title); a name whose title disagrees with face 00 is elevated. | provisional 7 (SEQPAGE) (title part held - H1) | seqpage.md:18-27 | crates/seqpage |
| D245 | Trailing spaces in a body line are kept as they are. | provisional 7 (SEQPAGE) - QD36 | seqpage-QUESTIONS.md:18-20 | crates/seqpage |
| D246 | A hand-written .seq for a page not yet in the book imports as a proposal to create it. | provisional 7 (SEQPAGE) - QD37 | seqpage-QUESTIONS.md:22-24 | crates/seqpage |
| D247 | Example sources were frozen and put in ruling form by SEQPAGE so golden tests do not move. | provisional 7 (SEQPAGE) | BUILD-LOG:109; seqpage.md:254 | docs/spec/examples/sources |
| D248 | .seq routes: GET /page.seq (text/plain us-ascii), POST /propose with text/x-seqpage, POST /check.seq; import findings return as seq_findings. | provisional 7 (SEQPAGE addendum, COMPUTE) | CONTRACT.md:31-36, 50 | crates/compute; app /export, page view |

## 5. Compute and identity

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D85 | One compute per repository owns every book. Reads are open, writes are proposals, and only the compute writes. | settled-by-spec format.md:14-18 | format.md:14-18, Design.md:47, AGENTS.md:39-42; rv55 [DECISIONS-INDEX.md] | crates/compute |
| D86 | First claim wins, because the queue approves one at a time. | settled-by-spec format.md:42 | format.md:42 [DECISIONS-INDEX.md] | crates/compute queue |
| D89 | Whatever the compute can't resolve goes to the user, never guessed. (Folds A1.6, A1.8, A2.8 and A3.2.) | settled-by-spec format.md:131 | format.md:131, seqAddr.md:104, decisions.md:56 [DECISIONS-INDEX.md] | compute; app; crates/ask probe |
| D90 | The core and compute are in Rust, and the app is TypeScript with Next.js, using the core as WebAssembly. | settled-by-spec format.md:137-149; WebAssembly not built yet (provisional 7) | format.md:137-149, Design.md:44-49, AGENTS.md:53; rv57 [DECISIONS-INDEX.md] | crates/seqaddr-core; crates/compute; app (no wasm yet) |
| D91 | The compute boots from a small fixed contract before the kernel loads. | open - QD47 (O31); built provisional 7 COMPUTE (BUILD-LOG:54) | kernel-design.md:109-122, decisions.md:613 [DECISIONS-INDEX.md] | crates/compute boot |
| D92 | The kernel defines agreements, the compute enforces them, the model reasons, and the person governs. | settled-by-spec kernel-design.md:35; note: kernel-design itself is proposed, :4 | kernel-design.md:35, AGENTS.md:42, Axioms.md:13 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D93 | Client transport, fork merging, hardware. | open - QD56, QD57, QD60 | format.md:155-157, Design.md:96-97 [DECISIONS-INDEX.md] | crates/seqaddr-core log; crates/compute |
| D249 | One compute process owns every book; every POST /propose goes into one queue drained by a single writer; validated, appended with fsync, then adopted. | settled-by-spec format.md 1.2, 2 | BUILD-LOG:53 | crates/compute |
| D250 | Boot follows kernel-design 7: find the kernel book, check header and address, replay, require the door; refuse to start on failure (exit 3); write nothing during boot. | settled-by-spec kernel-design.md 7 (kernel-design itself is proposed - QD47) | BUILD-LOG:54 | crates/compute |
| D251 | A damaged non-kernel book is refused and listed in /health; the compute still starts. | provisional 7 (COMPUTE) | BUILD-LOG:55 | crates/compute |
| D252 | Book folders are scanned books/ then kernel/; first file wins; a new book file goes in books/. | provisional 7 (COMPUTE) | BUILD-LOG:56 | crates/compute; app mock |
| D253 | HTTP codes followed SeqError::http_status (elevate 300, rule 422). | superseded by TRIAL-X fix codes | BUILD-LOG:58, 142 | crates/compute |
| D254 | HTTP codes: malformed address 400 everywhere; core rule 422; conflict and elevate 409; missing 404; no or unknown token 401; wrong media 415. | provisional 7 (COMPUTE) | BUILD-LOG:142; CONTRACT.md:41-42 | crates/compute; app error titles |
| D255 | Identity: books/.identities holds NAME TOKEN lines; every write carries a Bearer token; by comes from the token; only the director token may record approved_by director; the name compute is refused from clients. | provisional 7 (COMPUTE) - QD06 (Director to confirm) | BUILD-LOG:140; CONTRACT.md:38-40; compute-trial.md:22 | crates/compute; app sign in; scripts/dev.sh |
| D256 | Identity was a typed 'Writing as' name sent as by; anyone could be director or compute. | superseded by the token identity (TRIAL-X #1 fixed) | BUILD-LOG:81, 140 | app; crates/compute |
| D257 | No CORS headers; writes need application/json or text/x-seqpage; a non-loopback --listen is refused unless --allow-remote. | provisional 7 (COMPUTE) | CONTRACT.md:41; BUILD-LOG:142 | crates/compute |
| D258 | The compute appends at its known end of file with one write + fsync; a longer file is cut first, a shorter one refused. | provisional 7 (COMPUTE) | BUILD-LOG:143 | crates/compute |
| D259 | Queue ids persist across restarts in books/.queue. | provisional 7 (COMPUTE) | BUILD-LOG:143; CONTRACT.md:43 | crates/compute |
| D260 | /page shows every local face in every state; boards are listed under 'boards', never as FF.00; draft faces carry state and why_draft. | provisional 7 (COMPUTE) | BUILD-LOG:57, 142; CONTRACT.md:44 | crates/compute; app page view |
| D261 | /links: forward = page addresses in face 08; back = pages whose 08 names this one; missing and one_way listed; a retired 08 is not a link. | provisional 7 (COMPUTE) - QD50 | BUILD-LOG:61, 142 | crates/compute; app links |
| D262 | /face with a card key returns that card only; /resolve of a page resolves its face 00; /history parses its address and ignores titles. | provisional 7 (COMPUTE) | BUILD-LOG:62, 142 | crates/compute |
| D263 | /brands and /ask with no book read the --book chain, else the kernel only (not every book). | provisional 7 (COMPUTE) | BUILD-LOG:142; compute-trial.md:35 | crates/compute |
| D264 | Clients talk to the compute over HTTP only for now. | provisional 7 (COMPUTE) - QD56 | OPEN.md O42; BUILD-LOG:53 | crates/compute; app |
| D265 | Compute tests use a small built-in HTTP client instead of reqwest (box rustc 1.85.1). | provisional 7 (COMPUTE) | BUILD-LOG:67 | crates/compute tests |
| D266 | Anyone with a token may propose a write to the kernel book, with Director or R2 approval; only kernel-only cards are protected. | provisional 7 (CORE) - QD07 | kernel/QUESTIONS.md Q17; core-trial.md:167 | crates/seqaddr-core; crates/compute |

## 6. Ask, words and brands

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D65 | A brand is one meaning of a word, `word.NNN` running 001-998, with a brand card. | settled-by-spec brands.md:13-14 | brands.md:13-14, decisions.md:418,443; rv45 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D66 | A word after a face is a card key, and a 3-digit group after it is a brand. | open - QD39 (O12) | seqAddr.md:111, decisions.md:421, brands.md:47; rv46 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D67 | Brand cards hold forms (case-sensitive), meaning and meters. Only the compute writes meters, and they are exempt from drafting. | settled-by-spec decisions.md:435-440,484 | decisions.md:435-440,484, brands.md:51-61, drafting.md:39; rv48 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D68 | Each book keeps its own dictionary, and the kernel gives a small base. | settled-by-spec decisions.md:443 | decisions.md:443, brands.md:78; rv49 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D69 | The fixed dictionary layout `03.10-03.61` by letter share. Boundaries are estimates until checked. | settled-by-spec decisions.md:446-481 | decisions.md:446-481, brands.md:82-92; rv50 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D70 | Resolving a word: meters, then the last used, then the default, then the ordinary meaning, and the assumption is stated back. | settled-by-spec decisions.md:496-501 | decisions.md:496-501, brands.md:65-70; rv51 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D71 | A new meaning is asked for, then drafted by the compute, and the user's yes is its review. | settled-by-spec decisions.md:503 | decisions.md:503, brands.md:74, drafting.md:41 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D72 | Keywords on cards are brands. | settled-by-spec decisions.md:360 | decisions.md:360; rv40 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D73 | Failures count only against an assumed brand. | open - QD52 (O38) | decisions.md:493 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D74 | Where a new brand card goes. | open - QD53 (O39) | decisions.md:525 [DECISIONS-INDEX.md] | kernel 0055; dictionary 0012; compute /brands; crates/ask |
| D267 | A common-questions list works like brands: key words (what + my + name) link a phrasing to its answer; the compute hands the model 1-3 pieces, or probes the person. | settled-by-ruling R11 | DIRECTOR-RULINGS.md:43-50 | crates/ask; compute /ask; app /ask; 10.11.21.0013 |
| D268 | Words are split into key words, linking words, prepositions and question words, lowercased, ASCII only; folds like whats -> what is. | provisional 7 (COMPUTE) - QD65 | BUILD-LOG:137 | crates/ask src/lib.rs |
| D269 | Score is a weighted Dice match (key 2, link 1, question 1), best phrasing per question; brand card 1.0 exact form, 0.4 lowercase only. | provisional 7 (COMPUTE) - QD65 | BUILD-LOG:138 | crates/ask Config |
| D270 | Threshold 0.5; at most 3 pieces, one per target; holes are never pieces; below the threshold the compute asks a clarifying question. | provisional 7 (COMPUTE) | BUILD-LOG:138 | crates/ask; compute /ask |
| D271 | Seed questions: what is my name (and four forms) -> bob; what do i like -> cats; three holes. Kept as a draft proposal for KERNEL to absorb. | provisional 7 (COMPUTE) | BUILD-LOG:139 | crates/ask/seed/common-questions.proposal.json |
| D272 | POST /ask/link adds a phrasing through the queue as copy + note + merge on the question's draft. | provisional 7 (COMPUTE) | CONTRACT.md:48 | crates/compute; app /ask |
| D273 | /brands reads dictionary 0012.03 (all sections, drafts flagged dictionary_tail: draft); meters and session steps of brands.md are not built. | provisional 7 (COMPUTE) | BUILD-LOG:60 | crates/compute |
| D274 | /brands returns brand_id, is_default, forms, exact_form, dictionary; the word box states back the brand whose forms hold the exact form, else the default. | provisional 7 (APP) | BUILD-LOG:12 | app words box; mock |
| D275 | Dictionary entries use dotted names (bob.001:) that the core field grammar does not accept as fields; the core keeps them in the body. | provisional 7 (COMPUTE finding) | BUILD-LOG:60, 68 | crates/compute; core cards |

## 7. App

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D276 | The reader is Next.js 15 App Router + TypeScript with plain CSS (no Tailwind). | settled-by-spec AGENTS.md, Design.md (App = TypeScript, Next.js) | BUILD-LOG:5 | app |
| D277 | The app reads only through the compute; the browser goes through pass-throughs (GET, and later POST /api/propose); the app writes no files. | settled-by-spec format.md 1.2 | BUILD-LOG:6, 78 | app lib/compute.ts, app/api |
| D278 | A read-only mock compute replays books for development; POST /propose always rejects. | provisional 7 (APP) | BUILD-LOG:8 | app/mock/server.mjs |
| D279 | /page face keys are face part only (01, 01.draft, 05.01) so drafts and counters show. | provisional 7 (APP) | BUILD-LOG:10 | app mock pageView |
| D280 | Times show in Toronto time with the raw UTC beside them. | provisional 7 (APP) | BUILD-LOG:13 | app |
| D281 | A missing face shows as a dashed hole with a 7 and a link to the resolve trace. | settled-by-spec Axioms.md (axiom 7) | BUILD-LOG:14 | app |
| D282 | Drafting screens follow D0: new face = put with tail draft; live face = copy, note, merge, promote; notes read from /history. | provisional 7 (APP) (follows CORE) | BUILD-LOG:79 | app /draft, /seat |
| D283 | Ruling labels: door (R1), counters as a derived view (R9), face 00 as Registry (R10), a non-ASCII warning before send (R4). | settled-by-ruling R1, R4, R9, R10 | BUILD-LOG:85, 158 | app |
| D284 | The draft screen offers an override page in 0001 when an inherited face is changed. | provisional 7 (APP); on hold by R21 | BUILD-LOG:85 | app /draft |
| D285 | Ask screen shows the heard words, 1-3 pieces with matched words, score, why and a Draft badge, or the probe question. | settled-by-ruling R11 (layout provisional 7 APP) | BUILD-LOG:154 | app /ask |
| D286 | Sign in is a sidebar token box (localStorage, sent as Bearer). No whoami route yet, so the name is read from /queue after the first write. | provisional 7 (APP) - QD06 | BUILD-LOG:155 | app sidebar |
| D287 | .seq Export and Import are on the page view (check via /check.seq, import via /propose text/x-seqpage); the earlier 7 placeholder is removed. | settled-by-ruling R3 | BUILD-LOG:86, 156 | app page view, /export |
| D288 | A DraftState box shows why a face is a draft, its open and merged notes and the opening entry; the app reads the reason from /history. | settled-by-ruling R5 (layout provisional 7 APP) | BUILD-LOG:157 | app |
| D289 | Face 00 shows as a Registry (stamp, type, registry card), following the face00.md draft. | provisional 7 (APP) - QD29 | BUILD-LOG:158 | app page view, desk door |
| D290 | The common questions page is READER_BOOK.0013 (default 10.11.21); the phrasing list is the question cards on its face 01. | provisional 7 (APP) - QD27 | BUILD-LOG:161 | app /ask |
| D291 | Screenshots run on temp copies with demo tokens; nothing demo is kept in the repo. | provisional 7 (APP) | BUILD-LOG:163, 78 | app/screenshots |

## 8. Process, workflow and axioms

| ID | Choice | Status | Source | Affects |
|---|---|---|---|---|
| D98 | `.003` as a whole. | open - QD12 (O7) | workflow-loop.003.md:3 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D99 | S01: bind every grant to an approval ID and an exact N4 revision. | settled-by-spec decisions.md:627 | decisions.md:627, workflow-loop.003.md:88 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D100 | S02: evidence in proportion to risk. | settled-by-spec decisions.md:628 | decisions.md:628, workflow-loop.003.md:75,144 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D101 | S03: close at the bare counter, and record the outcome (passed, failed, blocked, needs-authority, abandoned). | settled-by-spec decisions.md:629 | decisions.md:629, workflow-loop.003.md:166 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D102 | S04: pack accepted, MVP done, and promotion are three separate things. | settled-by-spec decisions.md:630 | decisions.md:630, workflow-loop.003.md:89,219 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D103 | S05: band counterparts are not continuations. | settled-by-spec decisions.md:631 | decisions.md:631 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D104 | S06: a derived, read-only handoff manifest. | settled-by-spec decisions.md:632 | decisions.md:632, workflow-loop.003.md:220 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D105 | S07: work-card keys are `w01`, `w02` and onward. | settled-by-spec decisions.md:633 | decisions.md:633, workflow-loop.003.md:126 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D106 | S08: check targets by intent (depend, modify, create). | settled-by-spec decisions.md:634 | decisions.md:634 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D107 | S09: count passes per frame, and track repeated blockers. | settled-by-spec decisions.md:635 | decisions.md:635, workflow-loop.003.md:260 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D108 | S10: independent review, with a mandatory N7 trial for governing changes. | settled-by-spec decisions.md:636 | decisions.md:636, workflow-loop.003.md:199-200 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D109 | S11: one valid claim, its owner, and recovery terms. | settled-by-spec decisions.md:637; details open - QD22, QD61 | decisions.md:637, workflow-loop.003.md:206 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D110 | S12: N4 questions and N5 packs are on separate boards, linked explicitly. | settled-by-spec decisions.md:638 | decisions.md:638, workflow-loop.003.md:92 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D111 | Code lives in the repo, not in the book. | settled-by-ruling (Director, workflow-loop.003.md:70) | workflow-loop.003.md:70 [DECISIONS-INDEX.md] | repo layout; kernel 0057 |
| D112 | The loop: draft, pack, open, return, review, closed. Lint and close are the compute's. | open - QD12 (O7, O19) | workflow-loop.003.md:163-177 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D113 | Gravity: 1-3 passes is normal, pass 4 asks the why questions, and pass 6 halts. | open - QD12, QD62 (O7, O48) | workflow-loop.003.md:258-267 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D114 | The workflow band map: 0300 build, 0400 dev, 0500 jobs, 0700 colab (F.2). | open - QD40 (O13) | decisions.md:640-648, workflow-loop.003.md:40-49 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D115 | A return lives on its counter. | open - QD44 (O26) | decisions.md:612, workflow-loop.003.md:181 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D116 | What written permission is. | open - QD43 (O25) | decisions.md:594 [DECISIONS-INDEX.md] | kernel 0057; crates/seqaddr-core claims/tails; app /work |
| D117 | The nine axioms, with their numbers and order. | settled-by-spec Axioms.md:13-29 | Axioms.md:13-29, decisions.md:533-548 [DECISIONS-INDEX.md] | 00.00.axioms |
| D118 | Cite grammar: a dot orders, a comma splits, and only 3 takes M, P or C. `7.8` is not `8.7`. | settled-by-spec Axioms.md:5-7 | Axioms.md:5-7, decisions.md:558-566 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D119 | The cold set before a write is `1.7.8`. | settled-by-spec Axioms.md:9 | Axioms.md:9, decisions.md:564 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D120 | Every piece of work has a lead. | settled-by-spec Axioms.md:17 | Axioms.md:17, decisions.md:568-570 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D121 | A 01 card is the packed form of its 04 card. | settled-by-spec decisions.md:575 | decisions.md:575 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D122 | Lineage is kept with the page, on faces 00 and 08, by the compute. | settled-by-spec decisions.md:577-582 | decisions.md:577-582, seqAddr.md:157 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D123 | Nothing is promoted without a hostile pass from another view. | settled-by-spec Axioms.md:29; 'another view' settled by R20 | Axioms.md:29, decisions.md:586-590 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D124 | The axioms' page number and face names. | page number superseded by R6 (00.axioms on the desk; address QD09); face names QD45 | decisions.md:598, Axioms.md:3 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D125 | The axioms are the shape, and seqaddr is the geometry. | settled-by-spec AGENTS.md:27 | AGENTS.md:27, Design.md:53, kernel-design.md:15 [DECISIONS-INDEX.md] | 00.00.axioms; crates/seqaddr-core axioms |
| D126 | A concordance (word to page). | open (decisions.md:606 proposal; nothing built waits on it) | decisions.md:606 [DECISIONS-INDEX.md] | kernel (not built) |
| D127 | Face 05 task and ticket split, and patch and strike. | open - QD58, QD59 (O44, O45) | decisions.md:604-605 [DECISIONS-INDEX.md] | kernel (not built) |
| D128 | Link kinds, owner class, note fields. | open - QD50, QD06, QD51 (O36, O8, O37) | decisions.md:609-611 [DECISIONS-INDEX.md] | kernel (not built) |
| D129 | Does the kernel steer routing, or only hold agreements? | open - QD47 (O31) | kernel-design.md:153-162 [DECISIONS-INDEX.md] | kernel (not built) |
| D292 | The spec in docs/spec governs the lane contract; a disagreement is logged in BUILD-LOG as a finding. | settled-by-spec CONTRACT.md:3 | CONTRACT.md:3 | all lanes |
| D293 | Director rulings govern over older spec wording, and each keeps his exact words next to the reading. | settled-by-spec DIRECTOR-RULINGS.md:1 | DIRECTOR-RULINGS.md:1 | all lanes |
| D294 | A choice the spec does not settle is marked 7 in BUILD-LOG ('spec silent; chose X because Y'), kept isolated and switchable, and raised, never invented. | settled-by-spec CONTRACT.md:29 | CONTRACT.md:29; BUILD-LOG:3 | all lanes; core state::Policy |
| D295 | Every commit ends with the trailer 'Model: Grok Bot (Prima)'. | settled-by-spec CONTRACT.md:26 | CONTRACT.md:26 | all commits |
| D296 | Work is committed on local branch build; lanes never push. Prima alone pushes to the prima/build branch on GitHub, with no merges and nothing on claude. | settled-by-spec CONTRACT.md:28; push to prima/build allowed by the Director in chat (t72u) | CONTRACT.md:28; chat t72u | repo; GitHub Amalgamour/Workshop prima/build |
| D297 | Lanes touch only their own folders plus append-only BUILD-LOG lines with their lane tag. | settled-by-spec CONTRACT.md:27 | CONTRACT.md:27 | all lanes |
| D298 | Commits are path-limited (git commit -- paths), after 87eb383 swept another lane's staged files. | provisional 7 (COMPUTE, then all lanes) | BUILD-LOG:145 | all lanes |
| D299 | Build output target/ is not tracked; Cargo.lock is left to the lane that owns it. | provisional 7 (Prima, lanes) | 010e899, 538cfc6; BUILD-LOG:52, 77 | repo |
| D300 | Kernel text is copied from docs/spec with line sources in kernel/MAP.md, never rewritten from memory. | settled-by-spec drafting.md:7-18 | BUILD-LOG:16 | kernel |
| D301 | Every change to copied kernel text is a merge line in the page's 06.01 note. | settled-by-spec drafting.md (notes, merges) | BUILD-LOG:48, 116, 129 | kernel 06.01 notes |
| D302 | A ruling's quoted words are appended to the affected kernel cards; nothing is rewritten. | provisional 7 (KERNEL) | BUILD-LOG:129 | kernel 0051, 0057 |
| D303 | Hostile trials (axiom 9) report findings only and never edit what they test; each finding becomes an ignored test that is un-ignored when fixed. | settled-by-spec Axioms.md:29 (method provisional 7) | BUILD-LOG:27, 52, 119 | docs/trial; crates/trial-core, trial-compute |
| D304 | Four trials ran: TRIAL-K (kernel), TRIAL-C (core), TRIAL-X (compute over HTTP), TRIAL-K2 (kernel second pass). | settled-by-ruling R2, R20 | 5af2a64, 2069da1, e6e92cc, ed82086 | docs/trial |
| D305 | R2 does not let anyone answer an open Director question; those stay 7. | settled-by-ruling R2 | DIRECTOR-RULINGS.md:9 | all lanes |
| D306 | Questions go to the Director one at a time; v2 clash 1 (where a title lives) is not re-asked. | settled-by-spec OPEN.md:3, 15 | OPEN.md:3, 15 | Prima |
| D307 | Every design choice is recorded with its source; builders keep moving and save questions instead of stopping. | settled-by-ruling R22 | DIRECTOR-RULINGS.md:86-88 | all lanes; this file; QUESTIONS-FOR-DIRECTOR.md |
| D308 | No override pages while the Workshop app itself is built: changes go straight into pages, kernel or app. Override pages stay in the design for child desks. | settled-by-ruling R21 | DIRECTOR-RULINGS.md:82-84 | kernel/parked; core R7 code (kept, not exercised); app |
| D309 | An override is its own page in 0001-0009 stating what it changes, why it is there, why it is needed and what it should achieve; it may target a face, a behavior (0020-0049) or a structure (0050-0099). | settled-by-ruling R7; on hold by R21 | DIRECTOR-RULINGS.md:31-32 | core validate::override_pages (finding only); seqpage kind := override |
| D310 | An in-place face over an inherited face with no override page naming it is an R7 finding, not a rejection. | provisional 7 (CORE); on hold by R21 | BUILD-LOG:99 | crates/seqaddr-core |
| D311 | The sample override page 10.11.21.0001 (fields changing/there/needed/achieve) is parked; the in-place 0056.04 override was removed. | settled-by-ruling R21 | BUILD-LOG:115, 150; kernel-trial-2.md:251 | kernel/parked; books/10.11.21.book |
| D312 | The seated 05 is the best version of that page's pack. During a pass the pack may change to cover fixes; when the page is done, we seat the pack that already solves issues models run into. | settled-by-ruling R23 | DIRECTOR-RULINGS.md:90-92; chat t79u | every page face 05 |
| D313 | We climb the 05 counter (05.CC). The first stretch is 05.01 through 05.06; when that work is finished, we seat 05. If the page's scope or MVP then grows, we start 05.07 from that seated pack plus the new changes, and later reseat an update. The older seated 05 stays in the line. The past is not rewritten (axiom 6). The "05.01-06" and "3 more passes" are the shape of the climb, not a fixed count. | settled-by-ruling R24 | DIRECTOR-RULINGS.md:94-97; chat t80u, t81u; Axioms.md:23 | every page face 05 |
| D314 | Face 00 is the registry root, so it is not seated in the same manner as other faces. Changes are still recorded onto 00. | settled-by-ruling R25 | DIRECTOR-RULINGS.md:99-101; chat t82u | every face 00; kernel builder; core |
| D315 | Seat records may still be written onto face 00. The line of 00 itself is kept on a 00.counter face (00.CC), which lists 00's fingerprint as it was just before each change. This answers Q51 and QD05. | settled-by-ruling R25 | DIRECTOR-RULINGS.md:99-101; kernel/QUESTIONS.md Q51 | every face 00; seat records; 00.counter |
| D316 | The 00.counter steps are: snapshot 00's fingerprint first, then make the change, then count and compare (the old fingerprint, the change, and what 00 is now). The list must be its own face, not lines inside 00. | settled-by-ruling R25 | DIRECTOR-RULINGS.md:99-101; Axioms.md:23 | every face 00; 00.counter |
| D317 | PROPOSED: the 00.counter list climbs as 00.01, then 00.02, and so on. Each 00.CC face is write-once (fingerprint-before, the coming change, and a prior link). The "after" fingerprint is the next 00.CC's fingerprint-before. This matches R24 and axiom 6. | provisional 7 (DESIGN, Designer draft) - QD67 | docs/design/00-counter.md; R25 held 7; R24 | 00.counter; kernel builder (not built) |
| D318 | PROPOSED: 00.counter faces are not seated the normal way. They are write-once evidence. Seating them would write a seat record back onto face 00, which is another change and would cascade. | provisional 7 (DESIGN, Designer draft) - QD66 | docs/design/00-counter.md; R25 held 7 | 00.counter; kernel builder (not built) |
| D319 | WORKING PATH (Tester), not a ruling: add a page type only when the page lives under different laws; otherwise use a registry field (`kind`). Add `door`, `override`, and `axioms`. Keep the common questions page as `system` with `kind: questions`. Continuation pages use `pointer` with `kind: continuation`. Pending Director review. | working-path (Tester), pending Director review — not a ruling - QD02 | docs/design/WORKING-PATH-QD02.md; Tester 2026-11-11 evening | face 00 types; face 00 checker; held face 00s |

## Totals

Counted from the tables above by the first words of each Status cell. A row whose status has a settled part and an open part is counted by its first words; the open part is asked in QUESTIONS-FOR-DIRECTOR.md.

- **settled-by-ruling:** 53
- **settled-by-spec:** 113
- **provisional 7:** 103
- **working-path (pending Director review):** 1
- **superseded (in whole or part):** 22
- **open:** 23
- **held (do not re-ask):** 4
- **all:** 319

By area: addressing 61, faces 51, drafts 55, storage 32, compute 25, ask 19, app 16, process 59.

## Sources mined

DIRECTOR-RULINGS.md R1-R22; docs/BUILD-LOG.md (every `7` and every choice, lines 1-164); docs/CONTRACT.md and its two addenda; crates/seqaddr-core/API.md; docs/spec/face00.md; docs/spec/seqpage.md; docs/spec/seqpage-QUESTIONS.md; docs/spec/SEQ-GUIDE.md; kernel/QUESTIONS.md; kernel/CONFLICTS.md; docs/trial/kernel-trial.md, kernel-trial-2.md, core-trial.md, compute-trial.md; docs/design/DECISIONS-INDEX.md and OPEN.md; git log of branch build (3291593 to 8b2e909).

Updated 2026-11-11 evening (Designer): DIRECTOR-RULINGS.md R23-R25; docs/design/00-counter.md (draft proposal, not law); QUESTIONS-FOR-DIRECTOR.md QD66, QD67 (QD05 answered by R25). D312-D318 added. D53, D183, D203, D225 status updated from those rulings. Kernel QUESTIONS.md was not edited (KERNEL lane).
Updated 2026-11-11 7:15 PM EST (Prima): D319 added — Tester working path for QD02, not a ruling. See docs/design/WORKING-PATH-QD02.md.
