# prime-brief-pass01

A fixture-only reader-to-projection adapter that produces a readable Prime brief (0507.prime-support/05.13). Standard library only. It proves the mapping. It is not app wiring, a seated schema or a live integration.

The contract is `00.kernel/00.00.10.work/0507.prime-support/evidence/brief05.13/CONTRACT.md` §B, and its expected-results table is §C.

```
python -B prime_brief.py brief --input IN.json [--inspect] [--json]
python -B -X dev tests/test_prime_brief.py -v
python -B demo.py
```

**Exits:** 0 means a brief with no attention items and nothing unprojected; 1 means a brief with attention items or unprojected batches; 2 means refused.

## What goes in

`prime-brief-input/1` holds three things:
- a declared scope and member book;
- **labelled** reader observations in Grok-2's `batch-observation/1` shape, each labelled SYNTHETIC, SUPPLIED or DERIVED-FROM-RETAINED-SUMMARY;
- **SUPPLIED** coordination records.

Each coordination record is bound to a batch id and the observation's `source.sha256`. It carries release, claim, an optional explicit candidate, an optional typed review decision, and publication.

Grok-2's reader is held for repair. This lab never launches, imports or changes it.

## How it maps

- **Release and claim** come only from coordination. A reader's raw `Release:` or `Claim:` line is kept as evidence and never used. This is why a fenced example line can't authorise anything (BO-01).
- **Members** come only from reader pointer sections. The reader's own custody snapshot is shown as an earlier, separate observation. It is never used as the candidate.
- **A review decision** comes only from coordination, and is labelled as a supplied fixture decision. The reader's unauthenticated `typed_declaration` never binds.
- **Provenance.** A `git-blob` source maps to `supplied-commit`, marked supplied and not verified here, and a live custody result can't make it complete. A `live` source maps to `supplied-live`.
- **Unprojected.** Anything `state-observations/1` can't express goes to a visible unprojected list, with its reason. It is never coerced. That covers:
  - no coordination record;
  - an `unknown` release or claim;
  - a decision bound to a different source sha;
  - an unidentified page;
  - another source kind.

## The projection and the brief

- **The projection** is `../state-projection-pass01/state_projection.py`, loaded only after its sha256 equals `PROJECTION_SHA256` (b349da5c…, the SP-05 repair). Lifecycle and custody are the projection's job. Fresh custody goes through its pinned inspector and helper, which are checked before any launch.
- **The brief lists** are:
  - awaiting review;
  - correction or held, with the follow-up;
  - completed FIXTURES, as a derived label, not approval;
  - conflicts;
  - other open;
  - unreleased;
  - unprojected.
- **Alongside the brief:** the full projection, the per-batch mapping decisions with the evidence kept, and the reader custody snapshots.
- **Authority:** none. Nothing is selected, released, accepted or dispatched, and no file is written.

## Limits

- Fixture data only. There are no full retained reader reports, so the one DERIVED fixture carries only the facts from the retained demo summary.
- Labels are not authentication.
- The `PENDING.` rule for review text is an exact literal.
