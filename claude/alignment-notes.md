# Alignment Notes (2026-11-09)

Working notes for aligning the claude/ documents after the C-section and brands discussion. Each change below is applied from these notes.

## New decisions from this round

1. **C8.6 approved:** dictionary layout of 52 fixed sections, `03.10-03.61`, 1-5 per letter by first-letter share (PlainSpell, Wiktionary). Within-letter boundaries are estimates, to be checked against a real word list before freezing.
2. **C8.7 signals:** only the compute updates meters. Success = the output runs and the user carries on. Failure = negative words, the user stopping the process, or **restatement** (the user repeating and over-explaining because the first attempt failed). The user's word was "overflow"; "restatement" is proposed as the more accurate term.
3. **C8.8 confirmed:** a word with no brand uses the LLM's ordinary meaning. When the user shows a different meaning, the compute pushes the model to ask, and hands the answer to the compute, which records the brand. Order: meter match, recent in session, marked default, ordinary meaning. Assumptions are stated back. The user confirming the meaning is the review for the new brand card (D0).
4. **C8.9 approved:** card types, with per-face defaults and kernel definitions.
5. **C3.3 now settled** (keywords are brands).
6. **C6 settled (late):** face 03 is allowed in normal books on reserved pages. User pages are mostly 04; a 04 section may have a 01 card (a brief of how a model should understand it), and a 02 card only when the section describes a task process.

## Still open (carry into every doc)

- C1.4: do continuation pages share the `pointer` type?
- C4: face 08 links. The user's direction: 08 is the links face; most pages have none, some have many; the compute holds all connections in memory so it can see and trace them. Design pending.
- C5: authority precedence. The user asked for an explanation; not yet given.
- C7: notes metadata. The user wants to discuss.
- C8.7: should a failure count only against an assumed brand?
- C8.10: where a new brand card goes (a page the user picks, or a default terms page per book).
- D0 mechanism (`copy`, `note`, `merge`, `promote`) is proposed.
- Proposals of several operations applied all-or-nothing (from the C3 proposal) are needed by C1 and C3 but not yet confirmed as a format change.
- Section D: task failure paths, claims, promotion.

## Inconsistencies found and how they are resolved

1. **Counters and the reserved range.** A1.4 says the reserved 01-09 range does not apply to counters. The dictionary layout reserves `03.01-03.09`. Resolution: A1.4 stands for climbing counters; the dictionary's sections are a fixed layout that reserves 01-09 by its own definition, not by the axis rule.
2. **Grammar lacks cards and brands.** A word after a face is now a card key (C8.2), and a 3-digit group is a brand. `seqAddr.md` section 8 must add `card` and `brand`.
3. **`put` replaces faces.** `format.md` lets `put` set any face. D0 restricts `put` to new faces. `format.md` must show this as proposed, with the drafting ops.
4. **Resolution events have no home.** C8.7 needs the compute to record word resolutions. Proposed: a `use` entry in the book whose dictionary resolved the word.
5. **seqAddr section 5.2 describes 04 as mirroring 01/02.** C3 replaced the mirror with a full explanation. Update.
6. **Stale lists elsewhere.** `agents.001.md` (root) lists what is settled; it is now out of date (C3.3, C6, C8.6, C8.8, C8.9). Not edited here; flag to the user.

## File plan

| File | Change |
|---|---|
| `decisions.md` | C3 status; C4-C7 entries; C8.6-C8.10 statuses and content |
| `seqAddr.md` | grammar (card, brand), faces and cards, page and card types, face rules, dictionary pointer, open list |
| `format.md` | proposal batches, drafting ops, `use` events, card field syntax |
| `brands.md` | new: aligned brand and dictionary design |
| `drafting.md` | new: aligned drafting process and its enforcement |
| `design.md` | new: the system overview tying the documents together |

Root `brands.md`, `drafting.md`, `Design.md` and `seqAddr.md` are the user's sources and stay unchanged.

## Root files check (`D:\Git\Workshop`)

These are the user's files. They are checked here and not edited. Aligned copies were made beside them: `seqAddr.002.md` (`.001` was already taken by the older draft), `brands.001.md`, `drafting.001.md`, `Design.001.md`, `agents.002.md`.

| File | State | Out of line with |
|---|---|---|
| `AGENTS.md` | current brief: design only | Aligned. "A multi-faced file that can be stored in a database" matches the book log. "A reader to view the faces" is the app. |
| `agents.001.md` | proposed brief | Its settled list is out of date: C3.3, C6, C8.6, C8.8, C8.9 are now settled, and C4, C5, C7, C8.10 are new open items. It also says root `brands.md` and `drafting.md` are sources to leave unchanged. |
| `seqAddr.md` | original design | Superseded in many places by `claude/seqAddr.md`: the title rule (first non-digit ends the address) now depends on position; "first open page 1001" is now band head `1000`; every face has its own stamp -> page stamp on face 00 only; face 04 mirrors 01/02 -> full explanation; no face 00, no counted-face boards, no page or card types, no card keys after a face; typo `0020-049`. |
| `seqAddr.001.md` | older draft | Historical. |
| `brands.md` | source for C8 | Says the reference word is a **tail** after `01.cardtitle`. Decided: it is a **card key** (tails are reserved). Missing: forms, `means`, `default`, compute-only meters, success and failure signals, resolution order, dictionary layout. |
| `drafting.md` | source for D0 | Aligned in substance. Step 3 is numbered twice. Missing: the compute's enforcement (proposed) and the exceptions (meters, derived content, brand cards). |
| `Design.md` | empty | `claude/design.md` is the proposed content. |
| `Axioms.md` | empty | Candidate axioms are in `decisions.md`, for example A4.6 "missing is a valid state". |

## Root update, 2026-11-11 (notes before the edits)

Asked by the user: bring the root files up to the axiom work. Root only, not subfolders.

| File | Change | Why |
|---|---|---|
| `decisions.md` | add section E: the nine, the `axioms:` field, chain grammar, default lead, lineage on 00/08, trial, open items, proposals awaiting the Director | none of the axiom decisions were recorded there |
| `seqAddr.md` | `axioms:` field in 5.3 and the stamp; chains are not addresses (section 8); lineage on faces 00/08 (5.1); section 9 list | seqAddr never mentioned chains or the field |
| `Design.md` | Axioms.md as the shape; new documents in the table; read path proposed in "How work flows"; not-yet-decided list | it predates the axioms |
| `agents.003.md` | sources list, settled and open lists, conduct: AGENTS.md no longer says "design only"; until the user confirms, no code | stale since AGENTS.md was edited directly |
| `Kernel-Architecture-Design.md` | "Clerk" read as the compute; link to Axioms.md | Workshop dropped the clerk (axiom 3 notes) |

Not changed: `format.md`, `brands.md`, `drafting.md` (they change only when the Director decides Fable's proposals), `Axioms.md` (current), `AGENTS.md` (the user's).

Left for later, in subfolders (the user said root only): `axioms/04.md` says "the kernel's gravity page (`0012.gravity`)"; it should say the old kernel draft's, so it is not read as Workshop page 0012. `claude/readpath.md` says the default lead comes from the band head; axiom 3 now says band or pack.

Note: the user renamed `Kernel-Architecture-Design.md` to `kernel-design.md` during the update; references in the root files point to the new name.

## Workflow draft, 2026-11-11

`workflow-loop.001.md` (root) is a copy of the Director's `workflow-loop.md`, which is unchanged. It adds axiom citations to every section and fills missing details, each marked "(filled)". Director answers carried in: the lead reads N4 01 and 04 every pass and elevates changes to them for approval; a model lead may design packs and run loops once the N4 page is approved; pass count is an aim with hard move-on points, and the compute forces why questions after several passes without the person.

Main fills: roles (with a reviewer), the N4 approval as axiom 7's written permission, pack header fields, the work card term `W01`, the return on the same counter (no copy), the review step and failed review as a new `continues-from` counter, pack lint checks, the why questions at pass 4 and a halt at pass 6.
Open: where code lives, N4 05 mirroring, `scale`, `W01`, stale `open` time, when labs are required, correcting A2.6.
- Decided (Director, 2026-11-11): code lives in the repo, linked. N3 face 02 describes the files; face 08 links each by repo path. Recorded in `workflow-loop.001.md` section 3.1.
