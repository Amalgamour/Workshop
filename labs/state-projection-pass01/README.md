# state-projection-pass01

A fixture-only state projection with explicit closure (0507.prime-support/05.12). Standard library only. It proves proposed mechanics. It is not a seated workflow, a schema or a canonical-assignment migration.

The contract is `00.kernel/00.00.10.work/0507.prime-support/evidence/projection05.12/CONTRACT.md`. It carries Prime's SP-01 to SP-04 from prime-review05.11.

```
python -B state_projection.py project --input OBS.json [--inspect] [--json]
python -B -X dev tests/test_state_projection.py -v
python -B demo.py
```

**Exits:** 0 means projected with no attention items; 1 means projected with attention items; 2 means refused, and nothing was projected.

## Input and output

**Input** is one strict `state-observations/1` document. It has a declared fixture scope (a book and its lanes), an optional absolute member book, and a list of typed batch observations, each with exactly these facets:
- document;
- release;
- claim;
- return (pointer, members, optional explicit candidate);
- review (absent, pending, text, or bound with a typed binding);
- publication.

Each observation is a *supplied declaration* with provenance `supplied-commit` or `supplied-live`. The tool reads no page and no Git blob.

Input is refused before any projection when it has:
- wrong shapes, unknown keys or versions, or duplicate keys or ids;
- lanes outside the declared scope;
- a candidate that isn't one of the named members.

**Output** is a `state-projection/1` JSON (`--json`) or a readable view, on stdout only. It keeps the six facets separate, with provenance, live inspections, attention and follow-up. Each lane lists its open, awaiting-release, completed and conflict items in input order. It never selects "the current work", and it is not a v1 assignment record.

## Custody

`--inspect` launches the accepted `../return-capture-pass01/return_inspect.py` (947915fe…) for each named member. The inspector and its sibling `return_capture.py` (8f3da5c6…) are hash-checked first, and a mismatch launches nothing.

The tool uses only what the inspector reports: status, origin and receipt. It does not re-validate custody.
- **Primary match.** A member is primary only when it is `complete` and its origin book, page and batch all match.
- **Ambiguity.** More than one match is ambiguous unless an explicit `candidate` selects one.
- **Secondary members.** Retrospective captures, and members whose origin is another book or batch, are listed as secondary, whatever their pointer order.
- **Live versus commit.** Inspections are live and timestamped. For a `supplied-commit` observation they are shown beside the commit facets and never set them.

## Closure

A batch is `completed` only when all of these hold:
- the release is recorded;
- the primary is resolved;
- a bound review names that member and receipt;
- the review is `accepted` with `terminal: completed`;
- the observation's provenance is live.

Everything else stays open, or is a conflict:
- **Review text alone:** `open-review-unresolved`. The word "Accepted" alone closes nothing.
- **Held or correction-required review:** `open-held` or `open-correction-required`, with the follow-up kept.
- **Review bound to a different member or receipt:** `open-re-review-required`.
- **Accepted with no terminal declaration:** `open-accepted-not-terminal`.
- **More than one complete match:** `open-candidate-ambiguous`.
- **Missing release despite activity:** `conflict-missing-release`. No release is inferred.
- **A held review that declares a terminal:** `conflict-contradictory-review`.
- **Publication** is a separate fact. A published held item stays held.

## Limits

- Fixture mechanics only. Observations are supplied, not parsed from pages.
- No parser or corpus integration, no app wiring, no registry, no writes.
- Reviewer and actor labels are recorded text, not authentication or grants.
- Two inspector reads are two observations.
- The projection grants no release, acceptance, seat or work.

## SP-05 repair (05.13)

The contract amendment is `00.kernel/00.00.10.work/0507.prime-support/evidence/brief05.13/CONTRACT.md` §A.

- **Boolean flag.** A complete inspector report must carry `capture.retrospective` as a real boolean. Anything else is a failed observation.
- **Retrospective captures are historical.** A same-origin capture with `retrospective: true` is listed under `secondary` with `historical: same-origin retrospective`. It is never a candidate, never counts toward ambiguity, and can never complete the current batch.
- **Explicit historical candidate.** An explicit candidate that is a retrospective capture gives custody `candidate-historical`, and the lifecycle `conflict-candidate`.
- **Unchanged.** The 17 original tests and the demo are unchanged. Tests 18-21 add the countercases, using real `--retrospective` captures.
