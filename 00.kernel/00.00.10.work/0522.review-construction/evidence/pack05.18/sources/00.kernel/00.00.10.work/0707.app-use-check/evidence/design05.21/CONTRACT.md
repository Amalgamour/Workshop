# Harness contract (0707/05.21)
who: claude-opus-5-5 · state: **executable test equipment (lab). Not an app, not a repair, not a readiness claim.**

## Invocation
```bash
python -B labs/loop-convergence-harness-pass01/harness.py --candidate ROOT --inputs INPUTS.json --rooms NEW-DIR --out RESULT.json [--suite all|GROUP,…]
```

| Exit | Meaning |
|---|---|
| 0 | **READY.** Only when `verdict.aggregate` returns ready. |
| 1 | NOT READY |
| 2 | inputs or candidate refused before any case executed |
| 3 | harness crash |

**A runner exiting 0 is never itself evidence of anything.**

## Before execution (refusal, exit 2)
- **Inputs schema** `harness-inputs/1`. Dependency status is one of `accepted` / `pending` / `rejected`.
- **A `pending` row must have `files: "PENDING"`.** A guessed pin is refused (HX-3).
- **An `accepted` row:** every file matches the live bytes exactly, by sha256 and length (HX-4).
- **The frozen fixture source** (`evidence/pack05.21/source-manifest.json`) and each retained judgment match their declared hashes.
- **The candidate:** `CANDIDATE.json` matches the declared identity hash, and every declared candidate file matches (HX-2).
- **Every per-case copy is re-checked** against the candidate file list.
- **No discovery, ever:** no newest-file selection, no hidden live glob, no repin, no install.

## Execution
- **Each case:** a NEW copy of the candidate root, plus fixtures copied from **pack05.21 snapshots** (or a manifest row verified by its own declared hash).
- **Commands** run through the candidate's own `app/librarian.py review-loop` in new processes.
- **The baseline comparator** is the faithful pinned pass03 (`labs/n7-intake-compat-pass02/n7compat2.py --repo-root`).
- **A declared artifact at a candidate-owned path is never overwritten.** It is recorded as a collision, and the case expects the measurement to show it changed (for example 0522/05.13 `app/librarian.py`).
- **Expected values** come from fixture facts and frozen Prime evidence computed by the harness:
  - manifest row counts;
  - the independent emitted-source count;
  - the retained judgments;
  - Director states.
  - **Never from the candidate's own functions.**
- **A missing or wrong candidate field is a `fail`,** never a default success.

## Records (one per case)
`id, group, requirement, required, needs, candidate {candidate_json_sha256, kind}, expected, observed, verdict, evidence, provenance`

**Verdicts:**
- `pass`, `fail`;
- `blocked` (a needed dependency is not `accepted`; the case is not executed);
- `not-run`;
- `error` (crash, with traceback);
- `known-failure-reproduced` / `known-failure-not-reproduced` (non-required baseline demonstrations).

## Readiness (verdict.py; unit-tested 16/16)
**READY iff all of these hold:**
- the required ids are declared and non-empty;
- every required record exists, is well-formed, is marked required, and is exactly `pass`;
- no record is `error`;
- no undeclared required record and no duplicate ids;
- **every required dependency is `accepted`.**

**Known failures never count. A partial suite cannot be READY** while any dependency is pending (HX-6).

## The automated inspection checkpoint
- **Before each publish,** the harness loads the full `inspect` stdout, requires non-empty `rendered` text, and stores `{inspect_stdout_sha256, rendered_sha256}` in `<rooms>/<case>-inspect-checkpoint.json`.
- **This is NOT a claim that a human or model read it.** Prime keeps a separate actual-read gate before any real publication.

## Transport versus semantics
- **The judgment is compared canonically** (equal parsed JSON).
- **Raw judgment-file bytes are not claimed;** the retained files are kept as frozen inputs.
