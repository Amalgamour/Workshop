# Section and impact map — 0710/05.03 (changes from the 05.02 candidates only)
date: 2026-11-02 · who: claude-opus-5-5

## 0001 v005
**Unchanged from 05.02:** `design05.02/candidates/0001.law.01.005.candidate.md`, sha256 f46ae1cd5c5cf6df…, 7832 bytes.

It keeps:
- the compactness fix (cards shorter; templates and schemas fit for their job);
- the Director conflict route.

No new file.

## 0002 v004 → `design05.03/candidates/0002.schema.01.004.candidate.md` (sha256 d16f05b2…, 8586 bytes, CRLF)
| Section | Change from 05.02 | Class | Answers |
|---|---|---|---|
| stamp | state names 05.03 | — | — |
| **Job** | **payload is no longer a form kind.** Face 02 "controls the payloads attached to it" | S | Director 06.03 #02, #05; review R1 |
| Coverage | unchanged | — | — |
| **Forms** | + "A profile or other selector is lawful when its declared mapping names the section, the form, and the revision." | S | review N4 |
| Agreement | unchanged (verbatim seat text + the conflict route) | — | — |
| Requirements | unchanged | — | — |
| **Fields** | + a field declares only the answers it needs; a required text may accept only a value; **an empty answer keeps its field's shape** | S | review R2, the Grok-1 correction; probe 1 |
| Binding | unchanged | — | — |
| Construction | unchanged (candidate and final identities kept) | — | — |
| **Payload** | **rewritten:** the name is `02.NAME.VVV.TYPE`, a search tag and not a face file; **attached** to its controlling face 02 by metadata kept with that face (owner, location, selected revision, bytes, state, served section and form, dependencies, invocation, outputs); one face may control many payloads; **no companion file per payload**; interpretation follows the attachment; equal names on two pages are found through their faces; a payload without an attachment, or with changed bytes, is a finding; **no permission to run** from the tag, type or invocation; a later store carries the same attachment | S | Director 06.03 #02, #05 and the next message ("preserve the naming conventions") |
| notes | sources: the 06.03 decisions and the 06.02 review | — | — |

**Removed from 05.02:** "A payload is a file beside its face … The face is the governing form; the payload file is not a face. The declaring face is the payload's source and its lifecycle." That rule set a separate non-face architecture that the Director had not chosen (R1). It is replaced by the attachment model the Director stated.

## Other law
| Page | 05.02 proposal | 05.03 |
|---|---|---|
| **0018** | add a payload-naming sentence; F2 fork | **withdrawn.** Under 0018 Coordinate ("For now it is a .md file"), a `02.*.py` is not a face file, so the face scan does not rank it. **No amendment and no new 0018 candidate** (review R5). The pending `01.011.md` is untouched. **Its 010 history is verified on disk; the commit is unverified** (notes V3) |
| 0003 | possible form-level target (N5) | **no change.** Route plus selector meets 0003, shown by the qualified menus and cases M1–M4 |
| **0009** | — | **gap, not conflict:** the warehouse layout is unspecified. The page-folder layout is proposed in `lifecycle/LIFECYCLE.md`, to be approved as part of the kernel update. It is not assumed |
| 0021, 0022, 0024, 0060, 0023 | — | unchanged; cited by the lifecycle template |

## Examples
| Example | Status |
|---|---|
| **Attachment** (`attach/`) | real fixture files; two `02.check.001.py` on different pages; lookups A1–A8 |
| **Forms** (`forms/`) | derived from 05.02 by `derive_forms.py`; stored revisions 001 and 002; qualified per-page menus; the pack subject proposal for 0423 (draft, not seated) |
| **Person subject** | stays synthetic |
