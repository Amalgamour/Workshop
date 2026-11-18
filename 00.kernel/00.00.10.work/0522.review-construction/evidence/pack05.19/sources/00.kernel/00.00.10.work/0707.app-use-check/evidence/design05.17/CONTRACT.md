# Contract — return-pointer grammar by source kind (0707/05.17)
who: claude-opus-5-5 · state: **PROPOSAL for Prime review.** It supersedes the 05.16 grammar section (K1). Lab: `labs/n7-intake-compat-pass02/`.

## The rule
The pointer grammar is selected by the **source kind that intake already measures**: pass01 `address_of(source, pass)["kind"]`, which is `N5NN` or `N7NN`.
- **Mechanism:** a `build_intake` wrapper sets the kind in a context variable before it delegates to pass03's `build_intake`, and resets it afterwards. pass03 already uses this pattern for `p2._resolve_page`.
- **`parse_pointer` reads the context value. It does not:**
  - look at filenames;
  - look at the filesystem;
  - try a second grammar after a first one fails.

| Context | Grammar |
|---|---|
| `N5NN` | **The pass03 parser object itself** (captured before replacement). Its meaning is unchanged, including filenames ending in `,` `;` `)`, repeated lines and conflicting lines. |
| none (any caller outside intake) | Same as N5NN: pass03 unchanged. |
| `N7NN` | The two observed N7 forms are tried first, then the pass03 counted and field forms, **unchanged and with no added refusal**, then `unparsed-return-line`. |

**The N7 forms** (each must match the whole line; `PATH` is `[A-Za-z0-9][A-Za-z0-9._/-]*`, so it contains no comma, space or parenthesis):
- `Returned: PATH (ATTRIBUTION), sha256 HASH, N bytes.` declares the Submission.
  - `ATTRIBUTION` is 1–160 characters with no parentheses. It is descriptive only.
  - An attribution containing a 64-hex run or a label word (`Submission:`, `Artifact manifest:`, `Verification:`, `Returned:`) gives `attribution-not-descriptive`, and nothing is bound.
- `Artifact manifest: PATH, sha256 HASH, N bytes.` declares the manifest (`declared_form: n7-manifest`).

## The one lexical collision, and how it is decided
`Artifact manifest: m.json, sha256 H, N bytes.`
- **In N5 context, or with no context:** it means the file `m.json,`. This is pass03's meaning, preserved.
- **In N7 context:** it means `m.json` with the N7 delimiter.
- **Nothing else collides.** Each of these keeps the pass03 meaning in **both** contexts, because none of them is an N7 form:
  - `Submission: return.md, sha256 …` means `return.md,` (and likewise `;` and `)`);
  - `Artifact manifest: m.json,, sha256 …` means `m.json,,`;
  - the counted form `Artifact manifest: m.json, sha256 H, N bytes, K files. Excludes itself.` means `m.json,`.
- **Consequence on N7 pages:** a manifest literally named `X,` can still be declared, through the counted form. A path outside the N7 `PATH` alphabet can still be declared through `Submission:`. Nothing becomes undeclarable.

## Why no Director question
- The source kind is already measured; selecting by it **is not a new convention.** Prime's 06.16 direction says "isolate grammar by the already measured source kind".
- **Read-only scan of the live work book** (06.17.notes):
  - 8 N7 pointers use the comma manifest form: 0707/05.10–05.16 and 0710/05.05, all my own returns.
  - **For all 8, no file with a comma name exists,** so pass03 already measured all 8 as missing.
  - **No currently resolving declaration changes meaning.**
- **N5 meaning is byte-for-byte pass03** (P1, I-N5-*, and the 0522/05.13 replay with an identical intake_id).

## Unchanged from 05.16
These are all unchanged:
- path guards;
- hash and length measurement;
- manifest coverage;
- ambiguity: a duplicate or cross-form line on one field leaves it unbound;
- the manual-review hold when `06.NN.review.md` exists;
- freshness;
- no stripping and no fuzzy lookup;
- custody stays `missing`.

**`attribution_text` and `declared_form`** are kept in the parsed pointer only. `measure_declared` keeps path, sha256 and bytes, so the stored record schema does not change.

## Platform note (no generalization)
- `,` `;` `)` are legal in Windows filenames. Prime made real ones.
- `:` is not legal in a Windows filename but is legal on POSIX.
- The contract does not depend on either fact: it never asks what the filesystem allows.
