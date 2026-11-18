# Section-preservation and impact map — law 0002/01 v003 → draft v004
date: 2026-11-02 · who: claude-opus-5-5 (Claude), 0710/05.01

**Source:** `00.kernel/00.00.01.law/0002.schema/01.md`, v003, 1521 bytes, sha256 per `evidence/pack05.01/source-manifest.json`.
**Target:** `evidence/design05.01/0002.schema.01.004.draft.md`.

## Every part of v003
| v003 part | Disposition | Destination | Why |
|---|---|---|---|
| Header `# 01` | retained | same | the face header |
| `version: 003` | changed → `004` | stamp | a new draft version (law 0001 Stamp) |
| `Authorization: approved — 2026-10-10` / `state: approved` | changed → `draft — 2026-11-02` / `draft…` | stamp | a draft is never stamped approved |
| — | **new** `who:` | stamp | the draft names its drafter. This is the convention on existing draft faces (0302/02.md, `02.run.003.py`) and AGENTS v003; it is not listed in 0001 Stamp |
| `Face`, `PPPP`, `book`, `keyword: schema`, `cite: 2.8` | retained | stamp | identity unchanged. **`schema` is kept** because syntax 0002 points at "law page `0002.schema`" |
| `why: The job of face 02. A compact form adds no conditions.` | changed | stamp | "working form", plus "serves a declared job" |
| **Job:** "supplies a compact form of a named subject section" | changed | Job | "working form". The kinds become card / template / schema / compute form, with each job named. The compute-form kind is **contingent on D1** (return) |
| **Job:** "a card, template, or schema appropriate to that subject" | merged | Job | now the kind list, with "names its kind" |
| **Job:** "It does not add normative conditions absent from face 01." | retained verbatim, with "A form" as the subject | Job | the core limit |
| **Job:** "named separately rather than treating every box as interchangeable" | retained in meaning | Job | "The kinds are not interchangeable: a card is not a template, and a schema is not permission." |
| **Coverage:** "Create … when a compact representation serves the job." | changed | Coverage | "working form" |
| **Coverage:** "Its source section is explicit." | retained, then made concrete | Coverage | the 02 heading equals the exact 01 heading; the form's internal labels are content. This uses the existing heading key (0001 Sections), **with no new address axis** |
| **Coverage:** card shorter stays / read-the-source-only card comes off | retained verbatim | Coverage | — |
| — | **new sentence:** a template or schema may be longer than the rule | Coverage | **The core change.** Without it, 0001 Correspondence ("shorter than the rule") excludes construction forms. See 0001 below |
| **Coverage:** "If no compact form is needed, its face is absent and the menu omits it." | retained ("form") | Coverage | consistent with 0003 Integrity |
| **Agreement** (all sentences) | **retained verbatim** | Agreement | — |
| — | **new sentence:** "A template, schema, or compute form is held to the same test." | Agreement | extends the limit to the longer kinds |
| `patch: 2026-10-11. 05.04 #02 …` | retained | footer | history |
| `last change: 2026-10-10 approved …`, `last change: 2026-10-11 patch.` | retained | footer | history |
| — | **new** `last change: 2026-11-02 draft 004 …` | footer | the draft records its change |
| — | **new section Requirements** | — | **the authority test (structure versus condition).** It reuses the 0001 Admission test, with no new authority |
| — | **new section Fields** | — | the field declaration and the three suppliers; absent / empty / not applicable; examples are not decisions; repeating blocks only if declared |
| — | **new section Sources** | — | identity, exact-byte binding, retrieval by address, stale copies, declared dependencies; relationships stay on 08 |
| — | **new section Construction** | — | the whole-artifact build and review, an explicit encoding, the failure content, staleness, and lifecycle by reference only |

**Nothing in v003 is removed.**

**Deliberately not in the draft:**
- pack, `#NN`, freeze or authoring commands;
- JSON, Python, file extensions, module names;
- any lifecycle states.

These stay on their owning subject or module pages, such as 0423, 0526 and the module's own 02.

## Minimal related changes (only actual inconsistencies)
| Page / section | Current text | Proposed | Why |
|---|---|---|---|
| **0001/01 Correspondence** | "Face 02 is present where a compact form is shorter than the rule." | "Face 02 is present where a working form serves a declared job; a card is present only where it is shorter than the rule." | **Required.** The current sentence forbids a template that is longer than its rule. This is a semantic amendment of 0001, so it needs Director approval |
| **0001/01 Use** | "face 02 supplies its compact form" | "face 02 supplies its working form" | terminology; otherwise a template reads as unlawful |
| **0001/01 Construction** | "compact forms on face 02" | "working forms on face 02" | the same |
| 0001/01 Sections | "Matching sections keep the exact same heading across faces 01, 02, and 04." | **unchanged** | the 0002 draft complies by making the 02 heading the 01 heading |
| 0001/01 Validation | — | **unchanged** | it already separates structural failures from unresolved meaning |
| 0003/01 Selection | "a compact use may need 02" | **unchanged** | still true of a card; it does not exclude a template |
| 0004/01 Job | "rule and card sections" | **unchanged** (optional later: "rule and form sections") | not inconsistent: face 04 explains, and "card" there reads as a plain word |
| 0008/01 | — | **unchanged** | the draft sends page relationships to 08 |
| syntax 0001.rules, 0002.schema | pointers to "law page `0002.schema`" | **unchanged** | the address and keyword are kept |
| law 0010.about/01 line 20 (outside the pack; found by `reference-search.txt`) | "Face 02 is the compact form and the template." | **unchanged** | already names the template; optional later wording only |
| syntax 0010.about/01 line 20 (outside the pack) | "That short name is the compact form." (a page's short name) | **unchanged** | a different meaning of the same words, unrelated to face 02 |

## Existing face-02 uses checked against the draft (findings, not fixes)
| Artifact | Kind | Under the draft |
|---|---|---|
| `0302.run/02.md`, `0304.check/02.md`, `0307.face/02.md` (draft cards) | card for a loader | **Do not comply.** The headings `Card`/`State`/`Not` match no 01 heading, and no kind is named. They are draft, so this is a finding for their next draft, not a defect in seated law |
| `0302.run/02.run.003.py` (draft code, stamp in comments) | compute form | **Admitted only if D1 is yes.** The stamp exists in the comments; it does not name its source section |
| `0411.colab/02.md`, `0413.assistants/02.md` (design drafts) | schema / record groups | **Comply in spirit:** they say they are not seated schemas. **They lack** the per-field supplier and the 01 heading |
| `0423/templates/build-pack-v1.draft.md` | template | **Not on a face.** It needs a 02 home on the page whose 01 governs pack shape. That owner is not identified in the inputs (Need) |
