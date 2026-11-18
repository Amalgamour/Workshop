# Grok-1 0526/05.01 return against candidate 0002 v004 (comparison only; nothing edited)
date: 2026-11-02 · who: claude-opus-5-5 (Claude)

**Sources** (pack05.02 snapshots):
- `0526.dev-authoring/evidence/build05.01/CONTRACT.md`
- `0526.dev-authoring/evidence/build05.01/submission.md`
- `0526.dev-authoring/06.02.md` (Prime review A1–A4)
- `0423.dev-authoring/06.04.md`

I did not open Grok-1's module or app code.

| # | Candidate clause | Grok-1 pass01, as returned | Status |
|---|---|---|---|
| 1 | **Construction:** a review binds the candidate it judged; the candidate and the final artifact keep separate identities | review compares `--draft-sha256` with a render that **already includes the review** (A1, confirmed by Prime) | **Tested implementation gap.** Prime's run failed it, and validation case V8/N16 shows the intended binding. **The law is not bent to match:** the repair is Grok-1's (0526/05.03) |
| 2 | **Fields:** five answers, declared per field | intent values are strings; items have list fields; only `condition.state` has `applicable / inapplicable / unknown`; no null or not-applicable for fields | **Gap.** Prose for "nothing applies" and the empty list are not distinguished. The submission notes a first-run correction for "an empty-list render" |
| 3 | **Forms:** named forms, menu, selection by name | the caller selects a **profile id**; there is one implicit form per profile | **Gap (A2):** no menu of named forms, and no create/revise form split. `revise` is a command, not a form |
| 4 | **Forms / Fields:** the declared form governs validation | the template lists field names and ownership, but parsing is hard-coded (A2) | **Gap.** The 0526/05.03 repair is already directed at this |
| 5 | **Fields:** compute-owned keys refused from input | unknown keys refused (including `tests_passed`); the model never names a pass, `#NN` or hash | **Agrees** |
| 6 | **Construction:** declared encoding; raw bytes kept | UTF-8 required; invalid UTF-8 refused; a raw source is hashed and copied raw | **Agrees** |
| 7 | **Construction:** a failure names the field, the expected shape and the kept input | "Help … names the field, the expected shape, the retained input path" | **Agrees** |
| 8 | **Binding:** the selected revision; staleness only on changed bound bytes; history kept | review invalidated by changed meaning, template, source or set bytes; revisions kept in `review_history` | **Agrees** for its scope. It has no notion of a selected template revision while a newer draft exists, because there is one pinned template |
| 9 | **Requirements:** each required field names a meaning ground | no grounds are declared; the required fields are fixed in code | **Gap.** Not claimed by its pack; a future alignment point |
| 10 | **Agreement:** a template-law conflict goes to the Director | not in scope; 0423/06.04 states it ("Director review is required for a template/law conflict") | **Agrees in policy;** no mechanism |

**Disagreement preserved:**
- **(2):** Grok-1's "strings only" intent and the candidate's per-field answers are different designs. Neither is adjusted to the other here.
- **(3):** the profile id is a lawful selector for a tool. **Whether a profile counts as a form selection under Forms** is a review question for Prime, not something I assume.
