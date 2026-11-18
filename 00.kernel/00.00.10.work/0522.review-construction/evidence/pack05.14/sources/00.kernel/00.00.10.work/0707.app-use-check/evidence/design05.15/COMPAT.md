# Compatibility with the frozen core helper `measured_agreement` (0707/05.15)
who: claude-opus-5-5 · state: **observed behavior plus proposed handling.** The helper is not edited.

**Source:** `labs/workbook-review-pass01/workbook.py` (sha256 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a, 79131 bytes). The parts used are `IDENT`, `sha256_bytes`, `section_between`, `first_paragraph`, `finish_items` and `measured_agreement`. The core decodes with `decode("utf-8", "replace")` (line 734). Adapter: `labs/task-agreement-reference-pass02/core_compat.py` (AST extraction; pin-checked; a wrong pin is refused, case C-helper-pin).

| # | Input | Observed (frozen helper) | Case | Proposed handling for a builder |
|---|---|---|---|---|
| 1 | LF page with all six sections | goal, scope, prime_discretion and director_required are the **first paragraph**; finish_criteria is `[{id, text}]` from `- id: text` bullets; recorded_decisions is `[{id: "director-verbatim", text, source_sha256 = sha256(body.strip("\n"))}]` | C-lf-six | keep as the legacy observation; **do not reinterpret it as a decision pairing** |
| 2 | **The same page with CRLF** | **all six None.** `section_between` splits on `\n`, so `"## Goal\r" != "## Goal"` | C-crlf | **an existing helper defect.** Report it; do not silently normalize in the profile. A fix belongs to the core's own reviewed successor (Prime) |
| 3 | an empty `## Goal` section | `None`, **the same as an absent section** | C-absent-empty | paragraph fields cannot tell empty from absent; report "absent-or-empty" in any projection |
| 4 | `## Finish` present without valid bullets | `[]`; when absent, `None` | C-absent-empty | **keep** the explicit-empty versus absent distinction |
| 5 | a Finish bullet whose id has a space (`- bad id: x`) | **silently dropped** (`IDENT` fails) | C-lf-six | report dropped bullets as a finding; do not invent ids |
| 6 | `## Director - verbatim` (hyphen) | observed like the em-dash variant; the hyphen form is tried first | C-hyphen | keep both |
| 7 | a fenced `## Goal` before the real one | **the helper takes the fenced text** (the first exact line wins; no fence rules) | C-fenced-goal | an existing helper ambiguity. The block mode selects the real heading (J1). The builder must not claim parity here, but report the difference |
| 8 | only `## Director` sections | the `source_sha256` hashes the stripped body only, not the record | C-lf-six | bind the whole record identity separately in the block mode (R5) |

**What this means:**
- **The new block mode and the legacy observation are different evidence.** A page can have both.
- **The host must show the legacy observation as legacy**, with its own defects (2, 3, 5, 7) visible, and must never upgrade it to a cited, block-mode agreement.
