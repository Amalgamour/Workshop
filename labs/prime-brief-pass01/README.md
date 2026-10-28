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

When this lab was built (05.13), Grok-2's reader was held for repair, and the adapter was built against its contract only. The reader has since been accepted at 0508/05.15 (published 6d18d18). The adapter itself still never launches, imports or changes it; only the 05.14 rehearsal harness and tests run the pinned reader, and they pass its JSON in unchanged.

## How it maps

- **Release and claim** come only from coordination. A reader's raw `Release:` or `Claim:` line is kept as evidence and never used. This is why a fenced example line can't authorise anything (BO-01).
- **Members** come only from reader pointer sections. The reader's own custody snapshot is shown as an earlier, separate observation. It is never used as the candidate.
- **A review decision** comes only from coordination, and is labelled as a supplied fixture decision. The reader's unauthenticated `typed_declaration` never binds.
- **Provenance.** A `git-blob` source maps to `supplied-commit`, marked supplied and not verified here, and a live custody result can't make it complete. A `live-file` source maps to `supplied-live` (05.14; the 05.13 fixtures used a synthetic `live` tag).
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

## 05.14: strict consumer, real producer tags, a real-page rehearsal

The contract amendment is `00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/CONTRACT.md` §A.

- **PB-08.** Every consumed key must be present and typed (or explicitly null) before any lookup, hash or membership test. Labels are type-checked first. A malformed input refuses before the projection loads and before any subprocess.
- **PB-09.** The accepted reader emits `source.kind` `git-blob`, `live-file` or `supplied-text`.
  - `live-file` maps to `supplied-live`, and its observation times are kept as mapping evidence.
  - `supplied-text` stays unprojected.
  - The old synthetic tag `live` is no longer accepted, and the fixtures now use the real producer shape.
- **PB-10.** A pointer is ambiguous only on named reader codes: the ambiguity `unknown-return-heading`, or the attention codes `conflicting-stated-receipts`, `unparsed-member-line` or `unpaired-receipt`. `assignment-mention-not-pointer` is not one of them.
- **Member form.** A pointer member outside the projection's member form makes that batch unprojected; the input is not refused.
- **Reader codes on items.** Each brief item shows its reader codes. They are shown, and they do not change the exit code.

**Fixture versus actual source.** The tests use SYNTHETIC fixtures, plus real reader reports from disposable Git repositories. The 05.14 rehearsal (`evidence/realbrief05.14/rehearse.py`) ran the pinned reader on five real workbook pages at commit 6d18d18. Its reports are labelled SUPPLIED at this boundary, and the coordination records are Prime's supplied interpretation, not authentication.

**Live custody versus commit facts.** A `git-blob` report projects as commit basis. Custody at that commit is `not-verifiable-here`, and the live inspection is shown separately as `live_custody`.

**Remaining unknowns.**
- Pages whose release or claim is unknown stay unprojected.
- Real pages carry legacy codes (`legacy-ambiguous-heading`, `legacy-revision-withheld`), so revision ids stay null.
- A terminal decision is never inferred, so no real item completes.
