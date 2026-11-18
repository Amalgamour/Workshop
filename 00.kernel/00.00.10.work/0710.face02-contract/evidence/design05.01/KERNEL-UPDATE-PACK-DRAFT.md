# 05.NN DRAFT — kernel update: law 0002/01 v004 and three 0001/01 sentences
date: 2026-11-02 · drafted by: claude-opus-5-5 (Claude), 0710/05.01 · for: Codex Prime to adapt; the Director to release
state: **DRAFT. Not released.** This file makes no kernel write.

## Goal
Seat the face-02 working-form contract with the smallest kernel change:
- one 0002/01 revision;
- three sentences in 0001/01.

No other law or syntax page changes.

## Preconditions
- Prime and the Director have reviewed 0710/05.01.
- **D1 is answered** (whether compute forms are a lawful face-02 kind). If no, remove the compute-form clauses from the draft before staging: the Job kind list, and the `compute form` phrase in Agreement.
- Grok-1's 0526/05.01 return has been reviewed, and the alignment test below has been run against it. **Differences are recorded, not silently resolved.**

## Exact paths (book `00.kernel/00.00.01.law`)
| Act | Source | Target |
|---|---|---|
| Stage the 0002 draft beside the seat | `00.kernel/00.00.10.work/0710.face02-contract/evidence/design05.01/0002.schema.01.004.draft.md` (as reviewed; record its sha256) | `0002.schema/01.004.md` (NEW; `FF.VVV` draft beside the seat) |
| Stage the 0001 draft beside the seat | `0001.law/01.md` v004 with exactly the three sentence edits in `SECTION-MAP.md` (Use, Construction, Correspondence), plus a `last change` draft line | `0001.law/01.005.md` (NEW) |
| Seat (**Director act**) | the approved `01.004.md` / `01.005.md` | `0002.schema/01.md` / `0001.law/01.md` |
| Retire the predecessor (**at seating**) | the current seats, v003 and v004 | **name per the existing version law (0018, `FF.VVV.09`):** `0002.schema/01.003.09.md` and `0001.law/01.004.09.md`. Law 0018 is not in this pack's inputs; confirm before execution |

**Unchanged:**
- 0003, 0004 and 0008;
- syntax 0001.rules and 0002.schema (the keyword `schema` and the address are kept);
- every existing 02 file. The draft cards 0302/0304/0307 and the design drafts 0411/0413 are reported for their own next drafts, not edited here.

## Validation (before seating)
1. **Bytes.** The staged drafts equal the reviewed sha256. The seats are byte-unchanged until the Director seats.
2. **Checker.** Run the current seated checker per the boot instructions, read-only, against the book. **Record the before and after finding counts.** A new finding on a changed page is fixed in the draft or reported; **a rule is never weakened.**
3. **Correspondence.** Every section heading of 0002 v004 is unique, and every old v003 sentence is accounted for per `SECTION-MAP.md`.
4. **Reference check:**
   - search the kernel for "compact form" and list each hit: changed (the three in 0001) or kept, with the reason;
   - search for "shorter than the rule";
   - search for `0002.schema` pointers (they must be unchanged).
5. **Example check.** The two example forms (pack, person) are read against v004 by Prime: each field states a supplier and a ground, the pack `#NN` is declared, and the person form has no repeating identity.

## Alignment test, once Grok-1 returns (0526/05.01)
**Compare, do not edit,** Grok-1's machine template and authoring record against v004:
- the form declares kind, version, source section and encoding;
- each field states its supplier (intelligence / compute / source), its presence, and absent versus not-applicable;
- the `#NN` identity is declared as a repeating block that compute assigns;
- each required field's ground is stated, and condition grounds cite a sentence;
- a template, source or dependency change makes the review stale;
- a refusal names the field and the expected and observed shape, and keeps the input;
- UTF-8 is explicit;
- the model's input contains no path, pass, `#NN` or hash.

Each gap is a finding for the next authoring pass, or a reason to revise this draft. **Neither side is changed silently.**

## Rollback
- **Before seating:** retire the staged `01.004.md` / `01.005.md` as `.09`. The seats were never touched.
- **After seating:** the Director re-seats the retired `.09` predecessors by the same lifecycle. **History lines are kept,** and nothing is deleted.

## Out of scope
- Any template home for packs (F4: the owner page must be identified first);
- face-02 conversions of existing cards;
- tools, modules, the app, `00.live`, migration, Git publication.
