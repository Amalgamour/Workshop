# N7 return-pointer intake — contract and grammar (0707/05.16)
who: claude-opus-5-5 · state: **PROPOSAL.** It is backed by `labs/n7-intake-compat-pass01` (lab) and `proposal/workbook-review-pass04.workbook.py.proposal` (unapplied).

## Where the N7 return is lost today (measured, not inferred)
Path: `app/librarian.py review-loop` → `app/review_loop_tools_v7.py` → `labs/workbook-review-pass03/workbook.py` (pin 9e66d7e4…) → pass02 → pass01.

pass03's `parse_pointer` is installed into all three module namespaces (pass03 lines 493 and 498). Its grammar is:
- `^(Submission|Artifact manifest|Verification): (\S+) sha256 HASH, N bytes\.(.*)$`
- the counted form `… N bytes, K files.`

For the real 05.15 pointer:
1. **`Returned: 05.15.return.md (claude-opus-5-5, 2026-11-03), sha256 …, 7929 bytes.`** matches no label. It becomes `unparsed-return-line` and then `submission-not-declared`.
2. **`Artifact manifest: evidence/design05.15/artifact-manifest.json, sha256 …, 5322 bytes.`** matches the N5 form, with `(\S+)` = `…artifact-manifest.json,`. **The comma becomes part of the path**, giving `declared-file-missing`.
3. **`Notes: …`** becomes `unparsed-return-line`. It is informational, and stays so.

**Result:** `measurement: incomplete`. The 26 manifest artifacts are never measured (baselines A and B, `runs01`).

## Proposed grammar (bounded; the two observed N7 forms plus the unchanged N5 forms)
```text
PATH        = [A-Za-z0-9][A-Za-z0-9._/-]*                      (no comma, space, parenthesis, leading '.' or '/')
N7 return   = "Returned: " PATH " (" ATTRIBUTION "), sha256 " HEX64 ", " DIGITS " bytes."
N7 manifest = "Artifact manifest: " PATH ", sha256 " HEX64 ", " DIGITS " bytes."
N5 forms    = unchanged (pass03 FIELD_RE and COUNT_RE), except that a path ending in , ; : ) is REFUSED
ATTRIBUTION = 1-160 characters without parentheses; it must not contain a 64-hex run or a label word
```
- **`Returned:` binds the Submission field** (`declared_form: n7-returned`), page-relative. It is measured by the existing `measure_declared` and `locate_declared`, with the existing `logical()` path guard and the hash and length check.
- **Attribution is kept as `attribution_text`.** It is descriptive only, never authority or identity.
- **Duplicates or conflicts are `ambiguous-*`** (the existing `accept_field`): two Returned lines; Returned plus Submission; N7 plus N5 manifests.
- **Anything else is `unparsed-return-line` or `unrecognized-path-punctuation`.** Nothing is ever stripped or searched for.

## Examples
| Line | Result |
|---|---|
| `Returned: 05.15.return.md (claude-opus-5-5, 2026-11-03), sha256 bcee…, 7929 bytes.` | Submission `05.15.return.md` (n7-returned) |
| `Artifact manifest: evidence/design05.15/artifact-manifest.json, sha256 …, 5322 bytes.` | Manifest `evidence/design05.15/artifact-manifest.json` (n7-manifest) |
| `Submission: x.md sha256 …, 9 bytes.` / `Artifact manifest: m.json sha256 …, 9 bytes, 3 files.` | **unchanged N5 behavior** (G1: identical parse dicts) |
| `Returned: a.md; (x, y), sha256 …` | refused: `unparsed-return-line` |
| `Artifact manifest: m.json,, sha256 …` | refused: `unrecognized-path-punctuation` |
| `Submission: s.md, sha256 …` | refused: `unrecognized-path-punctuation` (**a behavior change for N5;** it previously "parsed" the path `s.md,`) |
| `Returned: ../x.md (…)` or `/x.md` | no match |
| `Returned: a/../../x.md (…)` | matches, then **`malformed-declared-path`** (the existing `logical()` guard, I5) |
| `Returned: a.md (sha256 <hex64>)` / `(Submission: b.md)` | refused: `attribution-not-descriptive` (H1) |

## What does not change
- custody (still `missing` for N7), authority, release, the agreement fields and the publish rules;
- **manual-review protection:** publish with an existing `06.15.review.md` stays held, with `correction: manual-review`;
- every N5 path that does not end in punctuation.
