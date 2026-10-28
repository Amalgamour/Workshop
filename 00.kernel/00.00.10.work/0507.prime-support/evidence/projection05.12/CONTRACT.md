# CONTRACT — state-projection-pass01 (0507.prime-support 05.12)

Author: claude-opus-5-5. Date: 2026-10-27.
This is a fixture-only lab contract. It is not a seated schema, a workflow, or a canonical-assignment migration. It carries SP-01 to SP-04 (prime-review05.11), and they override the 05.11 proposal wherever the two differ. Standard library only.

## 1. Command and exits

```text
python -B state_projection.py project --input OBS.json [--inspect] [--json]
```

| exit | meaning |
|---|---|
| 0 | projected, no attention items |
| 1 | projected, with one or more attention items |
| 2 | refused: the input is invalid or a pin mismatched; nothing is projected |

- The tool writes only to stdout. It never writes a file, a store, a registry or the book.
- `--inspect` launches the pinned inspector for each named member. Without it, custody is `not-observed`.

## 2. Input `state-observations/1` (strict JSON, exact keys, no duplicate keys, no NaN)

```text
{schema: "state-observations/1",
 scope: {book: LABEL, lanes: [LANE, ...]},          declared fixture scope; nothing outside it is read or derived
 members_book: ABS-PATH | null,                      required, and absolute, when --inspect and any member is named
 batches: [OBS, ...]}

OBS = {id: "<lane>/<NN.NN>", lane: LANE, batch: "05.NN",
       provenance: {kind: "supplied-commit" | "supplied-live", commit: HEX40 | null, page_sha256: HEX64 | null},
       document:   {header_state: STR | null},
       release:    {status: "recorded" | "pending" | "absent", text: STR | null},
       claim:      {status: "recorded" | "pending" | "absent", actor: STR | null},
       return:     {pointer: "present" | "pending" | "absent" | "ambiguous", members: [MEMBER, ...], candidate: MEMBER | null},
       review:     {status: "absent" | "pending" | "text" | "bound", text: STR | null,
                    binding: null | {member: MEMBER, receipt_sha256: HEX64,
                                     disposition: "accepted" | "held" | "correction-required",
                                     terminal: "completed" | null, reviewer: LABEL, followup: STR | null}},
       publication: {status: "unknown" | "at-ref", ref: STR | null, commit: HEX40 | null}}
```

**Validation rules.**
- `id` must equal `lane + "/" + batch` and be unique. `lane` must be in `scope.lanes`.
- `provenance.commit` is required exactly when the kind is `supplied-commit`.
- `binding` is required exactly when the review status is `bound`.
- `candidate`, when it is not null, must be one of `members`.
- Every field is type-checked before any iteration, membership test or comparison.
- An unknown schema or a wrong shape is refused with exit 2, before any projection or inspector launch.

**What the values mean.** Every value is a *supplied declaration*, labelled with its provenance. The tool reads no Git blob and no page, and it never claims to have verified one.

## 3. Custody, through the accepted inspector only

- **Pins.** `return_inspect.py` 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b is used, together with its sibling `return_capture.py` 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, the files next to this lab's `../return-capture-pass01/`. Both are hash-checked before every launch, and a mismatch refuses with exit 2 and no launch.
- **Launch.** `[sys.executable, "-I", "-B", inspector, "inspect", "--book", members_book, "--member", M, "--json"]`, with no shell.
- **Interface checks.** Strict JSON, schema `return-capture-inspection/1`, a known status, the exit matching that status, and the member equal to the requested name. A report that fails them is `observation-failed`. No receipt or package validation is re-implemented.
- **Inspection records.** Each launch is kept as `{member, observed_at (UTC), basis: "live", exit, status, origin, receipt_sha256, retrospective}`.
- **Candidates.** A member is a matching candidate when its status is `complete` and its origin `{book, page, batch}` equals `{scope.book, lane, batch}`. All three must match (SP-04).
  - `candidate` given and matching: it is primary.
  - `candidate` given and not matching: `conflict: explicit candidate does not match origin`.
  - No candidate, and exactly one match: that match is primary.
  - No candidate, and no match: `none`.
  - No candidate, and more than one match: `ambiguous`. There is no fallback to the first pointer or the newest.
  - Complete members with another origin are listed as `secondary`, with their origin.
- **Live against commit.** For a `supplied-commit` observation, inspection results are shown as `live_custody` beside the commit facets. They never set the commit-time return facet. Custody basis at the commit is `not-verifiable-here`.

## 4. Facets (independent; SP-02)

Each batch reports these facets with their provenance:
- `document`: the header, verbatim;
- `release`, and `claim` with the actor verbatim;
- `return`: pointer, members, custody (`primary`, `ambiguous`, `none`, `not-observed`, `observation-failed`, `candidate-mismatch`, `not-verifiable-here`), plus the primary, secondary and ambiguous lists;
- `review`: status, binding check (`current`, `stale`, `unverifiable`), disposition and terminal;
- `publication`.

There is no "furthest facet" summary.

## 5. Lifecycle (SP-01): the first rule that matches wins

| # | lifecycle | when |
|---|---|---|
| 1 | `conflict-missing-release` | release is not recorded, while a claim, a return pointer or a review exists |
| 2 | `unreleased` | release is not recorded |
| 3 | `conflict-contradictory-review` | the binding is `terminal: completed` but the disposition is not `accepted` |
| 4 | `conflict-candidate` | the explicit candidate does not match origin |
| 5 | `open-re-review-required` | a bound review's member or receipt is not the current primary (stale) |
| 6 | `open-held` / `open-correction-required` | the binding is current and the disposition is held or correction-required. The follow-up is kept. |
| 7 | `completed` | the binding is current, the disposition is accepted, the terminal is completed, the custody is `primary`, and the provenance is `supplied-live` |
| 8 | `open-commit-custody-unverified` | rule 7 would hold except that the provenance is `supplied-commit` |
| 9 | `open-accepted-not-terminal` | the binding is current and accepted, but the terminal is null |
| 10 | `open-review-unresolved` | the review is text-only (no binding), or bound but unverifiable (no resolved primary) |
| 11 | `open-candidate-ambiguous` | custody is `ambiguous` |
| 12 | `returned-awaiting-review` | the return pointer is present and there is no review |
| 13 | `claimed` | the claim is recorded |
| 14 | `released` | otherwise |

Publication never changes the lifecycle. A published held item stays `open-held`. Every non-`completed` lifecycle except `unreleased` is **open**.

## 6. Output `state-projection/1`

`{schema, tool {path, sha256}, input_sha256, scope, projected_at, inspected (bool), batches [{id, lane, batch, provenance, facets, live_custody, inspections (the live records, or null), lifecycle, attention [...], followup}], lanes {LANE: {open [ids], awaiting_release [ids], completed [ids], conflicts [ids]}}, attention_count, authority, note}`

- `authority` is `none; a projection grants no release, acceptance, seat or work`.
- `note` is `not a v1 assignment record and not canonical`.
- Lane lists keep the declared input order. A lane with no open item lists `open: []`. Nothing is selected as "the current work".

## 7. Corrected expectations for the 05.11 worked cases (additive; 0134 is unchanged)

| case | 05.11 expectation | corrected here |
|---|---|---|
| W1 | lanes "idle" because the latest review text closed them | text-only reviews give `open-review-unresolved`. Every lane lists those items as open; nothing is closed by text. |
| W2 | open, running | `claimed` (unchanged in substance) |
| W3 | open, returned awaiting review | `returned-awaiting-review` (unchanged) |
| W4 | "closed" by `Accepted within scope` text | `open-review-unresolved`. The stale header is shown verbatim in `document` and does not affect the lifecycle. |
| W5 | custody-problem | custody `none` (the incomplete member is not a candidate), and the lifecycle follows the other facets |
| W6 | stale-candidate review needs re-review; primary chosen by origin | `open-re-review-required`. The secondary first pointer is listed as `secondary`, and the primary is chosen by origin {book, page, batch}. |
| W7 | lane idle | a lane with no open item lists `open: []`. 0506/05.06's text disposition is `open-review-unresolved`, not idle. |

## 8. Limits

- Fixture mechanics only. Input is supplied, and no page or Git is read.
- There is no parser or corpus integration, and no app wiring.
- Reviewer and actor labels are recorded text, not authentication or grants.
- Two inspector reads at different times are two observations.
