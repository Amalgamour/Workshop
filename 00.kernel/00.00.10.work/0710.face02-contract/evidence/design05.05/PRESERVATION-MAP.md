# Source-section preservation map — seats → selected candidates (0710/05.05)
who: claude-opus-5-5 (author of both candidates; **not a cold review**) · state: prepared for Prime.

**This map starts from the SEATS, not from earlier candidate maps:**
- 0001 seat v004 (6288 bytes) → candidate v005 (f46ae1cd…);
- 0002 seat v003 (1521 bytes) → candidate v004 (d16f05b2…).

Sentence coverage was measured by compute: every seat sentence was searched verbatim in the candidate. Only the rows marked *changed* below were not found verbatim. **Coverage is mechanical; whether meaning is preserved is my judgment, for review.**

## 0001.law/01 — seat v004 → candidate v005
| Seat section | Disposition | Candidate destination | Change and reason | Authority | Affected links |
|---|---|---|---|---|---|
| stamp | changed | stamp | version 004→005; Authorization and state → draft; `who` added (a draft convention) | 0024 Number; 0060 | — |
| Authority | **retained verbatim** | Authority | — | — | — |
| Use | **changed** (1 sentence) | Use | "face 02 supplies its compact form" → "face 02 supplies its working forms" | 06.02 #01 | 0003 |
| Stamp | retained verbatim | Stamp | — | — | — |
| Sections | retained verbatim | Sections | — | — | 0002 Coverage relies on it (02 heading = 01 heading) |
| Construction | **changed** (1 sentence) | Construction | "compact forms on face 02" → "working forms on face 02" | 06.02 #01 | — |
| Admission | retained verbatim | Admission | — | — | 0002 Requirements uses its test |
| Scope | retained verbatim | Scope | — | — | — |
| Inheritance | retained verbatim | Inheritance | — | — | — |
| Correspondence | **changed** (1 sentence → 5) | Correspondence | "Face 02 is present where a compact form is shorter than the rule." → present where a declared working form serves a job; card shorter than its rule; template and schema complete for their job, not held to shortness; a form never amends its rule; **a form-rule conflict goes to the Director and the affected act waits.** "A disagreement is recorded for authority review…" is kept | 06.02 #01, #02 | 0002 Job, Coverage, Agreement; **finding F-1** |
| Validation | retained verbatim | Validation | — | — | 0002 Construction |
| Overrides | retained verbatim | Overrides | — | — | — |
| patch lines (3), last change (2) | retained verbatim | footer | history kept | 0021 Order | — |
| — | **new** | footer | `last change: 2026-11-02 draft 005…` and `### notes` | 0021 Order | — |

**0001:** 75 of 81 seat lines or sentences are verbatim. The other 6 are 3 stamp lines and the 3 intended changes. **Nothing is unplaced.**

## 0002.schema/01 — seat v003 → candidate v004
| Seat section | Disposition | Candidate destination | Change and reason | Authority | Affected links |
|---|---|---|---|---|---|
| stamp | changed | stamp | version 003→004; draft; `who`; why "A compact form adds no conditions." → "Named working forms, selected by name, adding no conditions." | 0024; 0060 | — |
| Job: "Face 02 supplies a compact form of a named subject section: a card, template, or schema appropriate to that subject." | **changed** | Job | "working forms"; each kind's job named (card read, template builds, schema checks); face 02 also controls attached payloads | 06.02 #01, #03; 06.03 #02, #05 | Payload; 0001 Use/Correspondence (**F-1**) |
| Job: "It does not add normative conditions absent from face 01." | **retained in meaning** (subject "A form") | Job (last sentence) | the subject is generalized to every form | — | Agreement |
| Job: "These forms are named separately rather than treating every box as interchangeable." | **changed and merged** | Job ("These are not interchangeable: a card is not a template, and a schema is not permission.") + **Forms** (each form declares its name and kind) | the naming rule becomes the explicit Forms section | 06.02 #03 | 0003 menu |
| Coverage: "Create a face 02 section when a compact representation serves the job." | changed | Coverage | "working form" | 06.02 #01 | — |
| Coverage: "Its source section is explicit." | **changed and merged** | Coverage ("The face 02 section heading is the exact face 01 heading it represents.") + Forms ("governing source section") | made concrete using the existing heading key; no new axis | 06.01 review; 0001 Sections | 0001 Sections |
| Coverage: card shorter stays / read-the-source-only card comes off | retained verbatim | Coverage | — | — | — |
| Coverage: "If no compact form is needed, its face is absent and the menu omits it." | changed | Coverage | "If no form is needed…" | 06.02 #01 | 0003 Integrity |
| Agreement (8 sentences) | **retained verbatim** | Agreement | + "Every form kind is held to the same test." + the Director conflict route ("…goes to the Director… does not choose which source to follow… The act that depends on the form waits…") | 06.02 #02 | 0001 Correspondence |
| patch (1), last change (2) | retained verbatim | footer | history kept | 0021 | — |
| — | **new section Forms** | Forms | named forms per section; name is a label, not a heading or axis; face 03 lists them; selection by name; **profile lawful if its mapping names section, form and revision**; no-match or multi-match refused | 06.02 #03; 06.02 review N4 | 0003 |
| — | **new section Requirements** | Requirements | a meaning part (ground: a 01 section or a recorded task grant) and a representation part (ground: the form); no narrowing, gates or unsupported meaning; compute checks, intelligence judges | proposed (06.01 review R01 direction); **not a Director decision** | 0001 Admission |
| — | **new section Fields** | Fields | templates and schemas; answers: not supplied / null / empty / value / not applicable, **each field declaring only those it needs**; empty keeps its shape; intelligence chooses references, compute resolves and generates | 06.02 #06; 06.03 #03 | Grok-1 form (comparison only) |
| — | **new section Binding** | Binding | bind the selected revision; a newer draft does not supersede; **a version is not superiority**; dev-phase Director review of changed binding or replacement | 06.02 #04 | 0022, 0024 |
| — | **new section Construction** | Construction | templates only; whole artifact shown; declared encoding; raw versus declared serialization; **candidate and final identity separate**; not sign/approve/seat/lock/release | 06.02 #06, #07; 0526/06.02 A1 | 0001 Validation |
| — | **new section Payload** | Payload | `02.NAME.VVV.TYPE` tag; attached to its controlling face 02 by metadata kept with that face; no companion file per payload; interpretation follows the attachment; **no permission to run**; a later store keeps the attachment | 06.03 #02, #05 and the next message | 0018 Coordinate (no amendment) |
| — | new footer | footer | the draft `last change` line and `### notes` | 0021 | — |

**0002:** 19 of 27 measured lines are verbatim. The rest are 4 stamp lines plus the Job and Coverage changes above. **Nothing is unplaced.**

## Unplaced meaning and contradictions (shown plainly)
- **Unplaced seat meaning:** none found. Every seat sentence is retained, retained in meaning, or changed with a named destination.
- **F-1 (candidate finding: 0001 v005 Correspondence, Use).**
  - **What:** 0001 v005 says face 02 is present "where a declared working form serves a job", and Use says face 02 "supplies its working forms". The 0002 v004 Payload model (selected in 05.03, *after* the 0001 candidate was written in 05.02) lets a face 02 control attached payloads. **A face 02 whose only job is payload attachment has no stated presence condition in 0001.**
  - **Impact:** a reader could call such a face unlawful.
  - **Proposal:** a successor 0001 adds "or controls attached payloads". **Not edited here.**
- **F-2 (wording; not a block).** 0002 Agreement keeps the seat's "in the compact form" while it now governs every kind. Harmless, because the next added sentence says "Every form kind is held to the same test." A successor may say "in the form".
- **D-1 (discrepancy for Prime).** Syntax `00.axioms` (v008, approved) says "The card is face `02`" (Shelf) and "Face `02` is the snippet" (Twin). Both rows are shelf-local ("That limit is local"; "This row is not every page's layout"), so I read **no conflict**. Prime should confirm. **No axiom change is proposed.**
- **Contradictory conditions between the candidates:** none besides F-1.
