# Hostile cases against draft law 0002 v004
date: 2026-11-02 · who: claude-opus-5-5 (Claude), 0710/05.01

This is analysis. No case was run. The "compute" column is the behaviour the draft requires, not a measured result.

| # | Case | Expected compute behaviour | Intelligence judgment | Draft clause |
|---|---|---|---|---|
| H1 | **Typed-field error** (0707/05.09 attempt 1: prose in `tests_passed`, a boolean) | **Refuse at that field.** Name the expected shape (boolean) and the observed one (text). Keep the input and give the correction route. With a template, compute asks for the boolean itself, so the model never writes the typed document | what the true value is, from the evidence | Fields; Construction |
| H2 | **Encoding fault** (attempt 2: a hand script re-read JSON in the platform encoding and changed the source text) | Read and write only in the declared encoding. **Compute serializes,** so no hand script exists. A byte mismatch on a bound source is refused, with both hashes | none. This is structure | Construction ("never in a platform default"); Sources (exact bytes) |
| H3 | **Missing dependency** | The resolver reports `missing`, with the declared reference. The build may preview but is not ready; nothing is invented | whether the dependency is really needed, or the declaration is wrong | Sources |
| H4 | **The governing source changed** (face 01, or the N4NN source, edited after review) | The bound bytes differ, so **the review is stale.** A ready build is refused, and the changed source is named | whether the change alters meaning; the form or the draft may need revision | Sources; Construction |
| H5 | **A copied, stale template** (for example `0423/templates/…` against its 02 home) | The copy names its form and version, and the form's bytes differ, so the copy is not used. **A copy that names no form is refused as having an unknown kind/source** | which form is the right one; whether the copy held intended changes, which then become a form revision | Sources |
| H6 | **Optional absence** | An absent optional field is not prompted beyond the listing. It is not filled with "N/A", and it stays distinct from "declared not applicable" and from an empty value | whether to declare "not applicable" explicitly | Fields |
| H7 | **Ambiguous form kind** (an 02 with no `kind`, or the loader card `0302/02.md` used as a template) | **Refuse to build.** Report that the form has no kind, or the wrong one. Do not infer from the file name or the headings | which kind it was meant to be; the owner revises the form | Job; Sources |
| H8 | **A template adds a new condition** (for example, a required field `risk ≤ 2 before release`) | **Mechanically:** every required field must state its ground; a `condition` ground must cite a 01 sentence. **A missing or unresolvable citation is a finding,** and compute does not enforce that field as law. Compute **cannot** tell whether a cited sentence really supports it | whether the requirement is structure or condition; if a condition, send it to face 01 under Admission | Requirements; Agreement |
| H9 | **A model-supplied path, pass, `#NN` or hash** | Not accepted from the semantic input. It is either rejected as an unexpected field or ignored with notice, per the form. **Compute derives these** | none | Fields |
| H10 | **A non-pack form inherits pack habits** (`#NN` on person aliases) | No repeating identity scheme is declared, so none is assigned. **An input `#NN` for aliases is an unexpected field** | none | Fields (repeating block only where declared) |
| H11 | **Review of a partial view** (only the changed item) | The review binds the whole draft's bytes. A review bound to a fragment does not bind the artifact | whether the whole reads correctly | Construction |
| H12 | **A form claims approval** ("schema-valid = accepted") | Valid shape reports structure only. **No approve, seat, lock or release state is written** | approval stays with the lifecycle owner | Construction; 0001 Validation |

**What the draft does not do:**
- **H8 stays judgment.** No checker decides meaning. The draft only makes the ground explicit, so that a reviewer can see an unsupported condition.
- **H1 and H2 disappear only if the tool supplies the form-driven prompt and serialization.** Law alone does not stop a hand-written document.
