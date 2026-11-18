# Section and impact map — 0710/05.02
date: 2026-11-02 · who: claude-opus-5-5 (Claude)

**Candidates:**
- `candidates/0001.law.01.005.candidate.md`
- `candidates/0002.schema.01.004.candidate.md`

Both use CRLF line endings, like their seats.

**Every change is classed** as **S** (substantive: it changes what is required, allowed or forbidden) or **W** (wording that follows from an S change). Per R08, the new 0002 sections are S: they are new obligations, to be reviewed as rules.

## 0001/01: seat v004 → candidate v005
| Section | Disposition | Class | Ground |
|---|---|---|---|
| stamp | version 005, draft, `who` | — | 0024, 0060 |
| Authority, Stamp, Sections, Admission, Scope, Inheritance, Validation, Overrides | **unchanged, word for word** (diff-verified) | — | — |
| Use | "its compact form" → "its working forms" | W | follows Correspondence |
| Construction | "compact forms" → "working forms" | W | the same |
| **Correspondence** | the compact-only limit is replaced. Cards stay shorter; templates and schemas are fit for building and checking; a form never amends its rule; **a form-rule conflict goes to the Director and the affected act waits.** The old sentence on authority review is kept | **S** | Director #01, #02; D01, D02 |
| history | the patch and last-change lines are kept; one draft line and notes are added | — | 0021 Order |

## 0002/01: seat v003 → candidate v004 (it succeeds my 05.01 draft, which stays as evidence)
| Section | Seat v003 | 05.01 draft | Candidate v004 | Class | Answers |
|---|---|---|---|---|---|
| stamp | v003, approved | v004 draft | v004 draft, a new `why` | — | — |
| Job | compact form; card/template/schema | 4 kinds incl. "compute form" | 4 kinds: card, template, schema, **payload** (declared and bound by the face) | **S** | D05, R04 |
| Coverage | compact; source explicit; card rules | + 02 heading = 01 heading; may be longer | the same, with "complete enough to build/check" in place of "may be longer" | **S** | D01 |
| **Forms** | — | — | **new:** several named forms per section, each with name, kind, purpose, source and revision; the name is a label, not a heading or an axis; face 03 lists them; selection is by name; no-match or multi-match is refused | **S** | Director #03, D03, R03 |
| Agreement | verbatim | verbatim + 1 sentence | verbatim + "every form kind" + **the Director conflict route; intelligence does not choose a source; the act waits** | **S** | #02, D02 |
| Requirements | — | structure-versus-condition test | **rewritten:** a meaning part (ground: a 01 section or a recorded task grant) and a representation part (ground: the form); prose-but-not-field versus absent-everywhere; no narrowing, gates or unsupported meaning; compute checks, intelligence judges | **S** | R01 |
| Fields | — | 3 answer states | **5 answers:** not supplied / null / empty / value / not applicable, each declared per field; model-chosen semantic references versus compute-generated locations, numbering and hashes; **scoped to templates and schemas** | **S** | R06, D06 |
| Binding | — | "Sources": "a changed form makes the copy stale" | **replaced:** bind the selected revision; a newer draft does not supersede it; versions are not superiority; stale only when bound bytes change; history stays valid evidence; Director review in the dev phase | **S** | #04, D04, R02 |
| Construction | — | all forms | **scoped to templates;** raw bytes versus declared serialization; **candidate and final identities** (the A1 gap); not sign/approve/seat/lock/release | **S** | R06, A1 |
| Payload | — | — | **new:** a declared file beside the face, not a face; the extension, runner or kind grants no permission to run; storage is representation | **S** | #05, D05, R04 |
| history | patch, last change ×2 | + draft line | kept, + a draft line and notes | — | — |

**Removed from my 05.01 draft:**
- the "compute form" name, replaced by payload;
- the absolute rule that a changed source makes a copy stale (R02);
- the "same meaning in another representation" test (R01);
- Construction obligations on every kind (R06).

## Other law: minimal, actual inconsistencies only
| Page | Text | Proposal | Class | State |
|---|---|---|---|---|
| **0018 Why and Envelope** | "Compute reads the rank, the version, and a 09 without opening the file." A payload `02.run.003.py` scans as a draft of face 02 at v003 | add to Envelope: "A payload a face declares carries the face, a title, its own revision, and its type. It is not a face and not a draft of one." | **S** | **Held:** 0018 already has a pending draft, `01.011.md`. A second draft would compete. **Director fork F2** |
| 0018 Coordinate | "For now it is a .md file. Later it is a row." | **unchanged.** It already states the Director's architecture (#05) | — | — |
| 0024 Number | "The draft is FF.VVV." | **unchanged** if F2 adds the payload sentence to 0018. Otherwise the same ambiguity stands here | — | depends on F2 |
| 0003 Job / Integrity | menu entries "link to the exact available face-section targets" | **unchanged.** A form entry links to its section and names the form. **Unverified:** whether "exact target" must address the form itself. If so, that is a 0003 change. Recorded as overflow, not drafted | — | overflow |
| 0004, 0005, 0008, 0009, 0021, 0022, 0023, 0060, syntax 0001/0002 | — | **unchanged** | — | — |
| law/syntax 0010.about | "compact form" | **unchanged** (05.01 reference search) | — | — |

## Existing artifacts under the candidate (status, not edits)
- **0302/0304/0307 `02.md` loader cards:** they would become forms of kind card with a payload declaration. Today their headings (`Card`/`State`/`Not`) are not 01 headings, and they name no form.
- **`02.run.003.py` and the other `02.*.py`/`.toml` files:** they would become payloads declared by their face. **Until F2, their names scan as drafts.**
- **0411/0413 `02.md` (design drafts):** no form names, no 01 headings, no per-field answers.
- **Grok-1's 0526 template:** see `GROK1-ALIGNMENT.md`.
