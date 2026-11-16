# Workshop `claude` branch — condensation review

Read-only. Nothing written to GitHub.
Old review kept as `review.v1.bak.md`.

## Frame

This branch is the **Director's own rework**, started before the kernel is made.
`claude/decisions.md` holds **his** decisions.
The job is to condense them into a shorter design.
The v2 seqaddr page
(`/workspace/prima/kernel-fresh/01.seqaddr/seqaddr.director.2026-11-09.v2.md`)
is his later short write of the address itself.
Where the two differ, list the clash; do not pick a winner here.

Sources under `/workspace/prima/workshop-claude/src/`.
24 commits on `claude`, 2026-11-09 about 2:07 PM–5:58 PM EST, under Mathias / Amalgamour.

---

## A. Core decisions (one line each)

### Address and short form
1. Every page/face has a full address `DD.SS.BB.PPPP[.FF[.NN]]`; short form only leaves ancestors unstated. [A1.1]
2. The 4-digit page is the anchor; read groups by position left and right of it. [A1.2]
3. No page digits means a container address read from the desk (`21` = desk 21). [A1.3]
4. Counters attach only after a face; they are not an axis. [A1.4]
5. Exact widths; never pad (`4442.1` is invalid). [A1.5]
6. A leading dot means "relative to the active page" (`.04` = face 04 there). [A1.6]
7. Users may write short form; models always echo the full address. [A1.7]
8. Finding looks up book → shelf → desk → kernel; first match wins; never guess — elevate to the user. [A1.8]

### Titles and tails
9. A word after DD/SS/BB/PPPP is a title; a word after FF/NN is a tail; faces have no titles. [A2.1–A2.2]
10. Title characters: lowercase, digits, hyphens; start with a letter; no dots or spaces. [A2.3]
11. A title is a label, not identity; several pages may share one. [A2.4]
12. Page tails: `draft`, `retired`. Face tails: `draft`, `retired`. Counter tails: `draft`, `pack`, `open`, `return`, `review` (bare = closed). [A2.5]
13. Workflow state lives only on counters; a container's state comes from its sentinel page. [A2.5]
14. Pages 1000+ must have a title in the stamp; 0001–0999 may; 0000 has none. [A2.8]
15. A title written in an address is checked against the stamp; mismatch elevates to the user. [A2.8, A3.2]

### Bands and book layout
16. A page number reads as `NDNN`; the second digit `D` is the band. [A2.6]
17. Every band is exactly 100 pages; every `xx00` at or above 0100 is a band head; `PP99` continues the band. [A2.6]
18. Same `N`+`NN` across bands form one set (e.g. `0423` with `0523`); titles should match. [A2.6]
19. Book layout: `0000` identity; `0001–0099` reserved/overrides; `0100–0999` kernel bands; `1000–9998` user space; `9999` continuation. [A2.7]
20. Books inherit the kernel live; they do not copy it at creation. [A2.9]

### Containers, 00, and 99
21. Every desk, shelf and book is identified by a page 0000 whose stamp holds its title. [A3.1]
22. `00` means "the owner of the level above, itself" (`DD.00.00` desk book, `DD.00.BB` desk book, `DD.SS.00` shelf book). [A4.1]
23. Face `00` holds the page stamp (address, title, state); other faces carry no stamp. [A4.2]
24. Face ranges: `00` identity; `01–09` system (07 reserved, 09 unassigned); `10–98` later; `99` reserved. [A4.3]
25. `FF.00` is the board of a counted face; a face is counted iff the board exists; 05 and 06 are always counted. [A4.4]
26. A counted face is never seated; plain `FF` on a counted face means `FF.00`. [A4.4]
27. Missing is a valid state (no board, no continuation, no 9999). [A4.6]
28. `99` at every level is a pointer (never content); face 08 records targets; many targets allowed; back-links required. [A5.1–A5.3]
29. Direct links are truth; ancestor path lists are derived by walking, never hand-edited. [A5.4]

### Capacity and kernel
30. Counter overflow: after `FF.98`, `FF.99` points to the same face on the next free page in the band. [A6.1]
31. Band overflow: `PP99` points to the next free hundred; bands never grow in place. [A6.1]
32. One address namespace per repository. [A6.2]
33. Desk `00` = kernel; `01–09` = kernel branches; `10–98` = user; each repo holds its own kernel. [A6.3–A6.4]

### Faces and cards
34. A page needs face 00 plus at least one of 01–06 or 08; face 07 does not count. [C1.1]
35. Draft faces count; a new page may start with only drafts. [C1.2]
36. Retiring the last content face retires the page; derived paths update. [C1.3]
37. Page types (`system`, `general`, `code`, `workflow`, `band`, `pointer`) live in the stamp; kernel-defined. [C1.4 — partly open]
38. A card is a `##` heading; same key across faces is the same card; contents lists are derived. [C2]
39. Face 04 is a full explanation with a `why:`, not a mirror of 01/02. [C3]
40. Keywords on cards are brands. [C3.3]
41. Face 08 is the links face; design of how the compute holds them is still open. [C4 — open]
42. Authority precedence between levels is still open. [C5 — open]
43. Face 03 is allowed on reserved pages in normal books; anywhere in kernel/desk books. [C6]
44. Notes metadata is still open. [C7 — open]

### Brands and drafting
45. A brand is one meaning of a word (`word.NNN`), held on a brand card. [C8.1]
46. A word after a face is a card key; a 3-digit group after it is a brand number. [C8.2]
47. The dictionary (page 0012, face 03) is only an index from word to brand cards. [C8.3]
48. Brand cards hold forms, meaning, and compute-only meters. [C8.4]
49. Each book has its own dictionary; kernel supplies a small base; brands run 001–998. [C8.5]
50. Fixed dictionary section layout `03.10–03.61` by letter share. [C8.6]
51. Resolve order: meter match → recent in session → default → ordinary LLM meaning; state assumptions back. [C8.8]
52. Card types with per-face defaults, defined in the kernel. [C8.9]
53. Never rewrite a face from memory: copy → note → merge → promote (mechanism proposed). [D0]

### Storage and compute (format / design pages)
54. A book is one file; every container is a book file. [format]
55. One compute per repository owns every book; reads open; writes are proposals. [format]
56. Encoding is an append-only JSON Lines log of approved writes. [format]
57. Core and compute in Rust; reader app in TypeScript/Next.js using the core as WebAssembly. [format / design]

### Face jobs (from the reworked seqAddr, matching the Director's face rewrite)
58. 01 law · 02 schema · 03 operate · 04 user-why · 05 tasks · 06 notes · 07 reserved · 08 map.

---

## B. Repeats, supersessions, and conflicts

### Repeats (say once in the condensed design)
- **Elevate, never guess** appears in A1.8, A1.6, A2.8, A2.6, A3.2 — one axiom.
- **Missing is valid** (A4.6) restated for boards, continuations, dictionary sections — one axiom.
- **Live inheritance** (A2.9) and the A1.8 lookup are the same path — one rule.
- **Title is a label checked against the stamp** (A2.4, A2.8, A3.2) — one rule.
- **Back-links required / derived ancestors** (A5.3, A5.4, C1.3) — one rule family.
- Face jobs are written in both `seqAddr.md` and the Director's v2 page — keep one faces page.

### Later supersessions inside the branch
- Root `seqAddr.md` (title = first non-digit; face 04 mirrors 01/02; no face 00; no boards) is **superseded** by `claude/seqAddr.md` + decisions. [alignment-notes]
- Root `brands.md` (reference word as a **tail**) is **superseded** by C8.2 (word after face = **card key**). [alignment-notes]
- Face 04 "mirror" wording in early seqAddr drafts is **superseded** by C3 (full explanation + `why:`).
- `format.md` early `put` that can replace any face is **restricted** by D0 (`put` only for new faces; replace via promote). [alignment-notes]
- A2.7's coarse `0001–0099 reserved` is later **subdivided** in `seqAddr.md` §6 (0001–0009 / 0010–0019 / 0020–0049 / 0050–0099) — pick one layout when condensing.

### Conflicts inside the decisions themselves
- **A1.4 vs dictionary layout:** A1.4 says reserved 01–09 does not apply to counters; C8.6 reserves `03.01–03.09` as sections. Alignment notes resolve: layout's own rule, not the axis rule — keep that note beside both.
- **A2.5 page/face `draft` vs counter `draft`:** same word, two jobs (unseated face vs pass being written). Position decides; say so once in the tails page.
- **A4.4 "counted face never seated" vs seated-address rule:** seated form is bare `DD.SS.BB.PPPP.FF`, but counted faces treat bare `FF` as the board. Needs one clear sentence when condensed.
- **C1.4 open pointer type** vs A5 treating all 99s the same — still open.
- **D0 mechanism** and proposal batches are **proposed**, not settled — do not mark them settled in the short design.

### Conflicts with the Director's v2 seqaddr page
(v2 is the short address page written the same day. List only; do not resolve.)

| # | Topic | decisions.md / claude seqAddr | v2 seqaddr page |
|---|---|---|---|
| 1 | Where the title lives | Stamp on identity page 0000; title in address is a checked label | Title is written in the address (`DD.title`, `DD.SS.title`, …) |
| 2 | Seated form on disk | Faces live as entries inside one `.book` log (format page) | "Seated face only legal formate `DD.SS.BB.PPPP.FF` That is the seated address." |
| 3 | Face 00 | Required identity / stamp face | Faces listed 01–08 only; stamp is "header" on a face, not a separate face 00 |
| 4 | `FF.00` board | Board required for counted faces; 05/06 always counted | Counters exist; no board rule |
| 5 | Counted vs seated | Counted face never seated; plain FF means board | Seated = bare FF (no tail, no counter) for a face |
| 6 | Desk/shelf identity | Nested `DD.00.00.0000` / `DD.SS.00.0000` | Desk `DD` + sentinel `DD.00`; shelf `DD.SS` + sentinel `DD.SS.00` |
| 7 | 01–09 on every axis | Reserved on axes; desks 01–09 = kernel branches | v2 does not reserve 01–09 on every axis; desks point to kernel as parent |
| 8 | Card key in the address | Word after face = card key (`…01.ham`) | Cards live inside faces; faces have no titles; no card segment in the address |
| 9 | Bands | Full `NDNN` / `xx00` head / `PP99` model | Not on the v2 page (bands live in earlier Nov-7 notes) |
| 10 | Bare closed counter | Generalized to bare `FF.NN` | Still writes "bare `05.MM`" (same idea, older letters) |

Open on purpose in both places, or only in decisions: C4 (08 design), C5 (authority), C7 (notes meta), C8.7 assumed-only failures, C8.10 new brand home, section D task failure/claims.

---

## C. Suggested condensed shape

Goal: fewer pages, each with one job.
Pull from decisions; leave open items as questions, not answers.

| Page (kernel / design) | Holds these decisions | Leave out / later |
|---|---|---|
| **1. seqaddr (axis)** | 1–5, 9–11, 14–15, 21–22, 27–28 (sentinels 00/99), 32–33, 58 (pointer only to faces page) | Short-form sugar (6–8) can be a short appendix; storage (54–57) stays off this page |
| **2. faces** | 12–13 (tails), 23–26, 34–36, 38–40, 43, 58 (full face jobs), stamp + cards | Page/card *type catalogs* (37, 52) → structural page; C4/C5/C7 stay as open questions |
| **3. bands / book layout** | 16–20, 30–31 | Dictionary section map (50) → brands page |
| **4. tails / passes** | 12–13 in full, D0 principle (53), closed = bare | Compute ops `copy/note/merge/promote` → drafting page; task failure paths → still open |
| **5. brands / dictionary** | 45–51, open C8.7 and C8.10 as questions | Fixed letter table can be an appendix once frozen |
| **6. drafting** | 53 principle + steps; exceptions (meters, derived content) | Enforcement ops stay proposed until seated |
| **7. format / compute** (later, not kernel page 1) | 54–57, proposal queue, log encoding | Language choice and app stack can wait until ideas are seated |
| **axioms (one-liners)** | Elevate never guess; Missing is valid; Live inheritance; Title is a label; Never rewrite from memory; Direct links are truth | — |

### Condensation tips
- Merge A1.8 + A2.9 into one "find" rule.
- Merge A2.4 + A2.8 + A3.2 into one "title" rule.
- Keep one tails table (page / face / counter).
- Mark D0 mechanism, proposal batches, C1.4 pointer split, C4, C5, C7, C8.7, C8.10 as **open**, not settled.
- When folding into page 1, reconcile the ten clashes in section B with the v2 page first so the short design speaks with one voice.

---

## Still open (carry forward)

- C1.4: do continuation pages share the `pointer` type?
- C4: how face 08 links are held and traced.
- C5: authority precedence.
- C7: notes metadata.
- C8.7: failure only against assumed brands?
- C8.10: where a new brand card goes.
- D0 mechanism and proposal batches (proposed).
- Section D: task failure paths, claims, review reject.

