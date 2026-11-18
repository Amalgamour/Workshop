# CONTRACT — 0705 pass02 independent desk-check lab
date: 2026-11-01
who: claude-opus-5-5 (Claude)
state: lab-local contract, written before the lab code. It is not a product output schema and does not prescribe 0524's interface.

## 1. Parts and files (colab/labs/0705.prime-desk-check/pass02/)
| File | Role |
|---|---|
| `cases.json` | pass02 case matrix, traceable to pass01 (`from_pass01`, `corrections`), with `mode` executable / manual / declarative |
| `expected.json` | expected-results manifest: assertions per executable case, written before any evaluation; its sha256 is a required checker argument |
| `manual-checklist.json` | manual items with the questions to answer; results are supplied separately with attribution |
| `build_fixture.py` | builds case fixtures from pack05.02 snapshot bytes plus declarative ops into a new external directory |
| `check.py` | consumes saved observation files, the expected manifest, the fixture manifests and optional manual results; prints a report |
| `harness.py` | two-process run of build plus check (harness restart only) |
| `tests/test_lab.py` | checker self-tests with labelled synthetic observations |
| `rehearsal/0521-05.03/` | first-use package: catalog, expected facts, steps |

## 2. Fixture builder
`python -I -B build_fixture.py --cases ABS --manifest ABS(pack05.02 source-manifest.json) --out ABS(new) [--case ID|all]`
- `--out` must not exist. Its parent must exist. It must resolve outside this checkout. The builder creates it, never removes or reuses it, and refuses occupied output.
- **Bytes come only from snapshots** named by the manifest, after their sha256 and length are checked. Never from live files. No search, no download.
- **Each case** gets `<out>/<case>/instance-A/…` (and `instance-B` for C03), plus `fixture-manifest.json`:
  - `{schema: desk-fixture/1, case, built_from: {manifest_sha256}, instances: {name: {root, files: {rel: sha256}}}, generated: [rel], ops: [...], derived: {...}}`.
  - `generated` lists every file not copied from a snapshot.
  - `derived` holds values the expected manifest refers to, such as a quote's byte hash.
- **Ops (declarative only):** `replace-line`, `duplicate-line`, `append-line`, `append-section`, `omit` (the file is deliberately not copied), `construct` (a generated file with given text), `second-instance`.

## 3. Normalized observation `desk-observation/1` (lab-local)
An adapter writes one JSON file per case, `<case>.json` (C14 also `C14.second.json`), with these exact top-level keys:
- `schema`
- `case_id`
- `producer` {kind, adapter: {id, sha256, status}, raw_outputs: [{path, sha256}], unmapped: [path]}
  - `kind`: `candidate` | `synthetic-self-test`
  - adapter `status`: `connected` | `not-connected`
- `instance` {selected}
- `selected` {work_ref, basis, source: {path, sha256}}
- `parallel` [{work_ref, basis, source}]
- `works` [{work_ref, claim: {state, basis}, return: {state, basis, source_path}, custody: {state, basis}, review: {state, basis}, disposition: {value, attributed_to, basis}, director_approval: {state}, blocked, tails: [{name, present}]}]
- `attention` {total, shown, overflow_route, items: [{kind, ref}]}
- `holds` [{id, work_ref, visible}]
- `coverage` [{area, status, reason}]
- `sources` [{path, instance, expected_sha256, observed_sha256, status}]
- `quotes` [{kind, attributed_to, source_path, quote_sha256}]
- `workers` [{name, state, basis}]
- `refusals` [{rule_ref, target_path, target_instance}]
- `identity_fingerprint`

**Vocabularies:**
- **basis:** observed / supplied / derived / unknown.
- **custody.state:** complete / pending / unknown / incomplete.
- **review.state:** pending / review-complete / unknown.
- **return.state:** not-returned / returned / unknown.
- **claim.state:** pending / claimed / unknown.
- **director_approval.state:** none-recorded / recorded.
- **source status:** ok / changed / absent / outside-instance.
- **coverage status:** covered / not-covered / unsupported.
- **attention kinds:** hold, director-question, awaiting-review, conflict, missing-evidence, stale-source, interrupted, coverage-gap, overflow.
- **work_ref:** `<page>/<pass>`, for example `0522.review-construction/05.04`.

## 4. Adapter boundary
- An adapter maps the candidate's raw output files (kept, with hashes in `producer.raw_outputs`) into this form. It records its own id and sha256.
- It may **not** invent a fact, fill a default, or upgrade a basis (supplied → observed).
- A fact it cannot map goes into `producer.unmapped` as a path prefix. Assertions under an unmapped prefix report `unsupported`, never `pass`.
- **In this pass the candidate adapter is NOT CONNECTED.** No adapter for 0524 exists. Its output interface is not frozen and was not read.

## 5. Assertions and statuses
An assertion is `{id, case, path, op, value, mandatory}`. `path` is a JSON array of keys and `{field: value}` list selectors.

**Ops:**
- `eq`, `ne`, `in`, `ge` (number at least);
- `contains`: the list has an item whose fields equal the given subset;
- `present`, `null`;
- `overflow-consistent`: `total - shown == count of overflow items`, and a route is present when anything was hidden;
- `one-of`: any sub-assertion passes;
- `same-as-second`: equal value in the C14 second observation.

A value may be `{"fixture_file": [instance, path]}` (that file's sha256 in the fixture manifest) or `{"fixture_derived": name}` (a derived value), resolved from the case's fixture manifest at check time. These refs may also sit inside a `contains` subset.

**Statuses:**
| Status | When |
|---|---|
| `pass` | the value matches |
| `wrong` | a value is present and does not match, or the observation file is malformed |
| `missing` | the path does not resolve |
| `unsupported` | the path is under `producer.unmapped` |
| `needs-human-assessment` | a manual item with no attributed answer |
| `not-run` | the case's observation file is absent |
| `checker-error` | the expected manifest hash mismatches, a fixture manifest is unreadable, or the checker has an internal fault |

## 6. Verdicts (never collapsed)
- **`checker_self_test`:** reported only when every observation is `synthetic-self-test`. It says what the checker detected. It is never desk evidence.
- **`desk_verdict`:**
  - `pass` only if all of: every observation has producer `candidate`; the adapter status is `connected`; every executable case was observed; every mandatory assertion is `pass`; every manual item is answered `yes` with `by` and `date`.
  - Otherwise `not-passed`, with `blocking: [...]` listing each reason (adapter-not-connected, synthetic-only, not-run case ids, assertion ids per status, manual pending).
  - Synthetic-only runs report `desk_verdict: not-applicable (synthetic self-test)`.
- **Counts reported separately:**
  - cases: defined / executable / observed / manual / declarative;
  - assertions: defined / evaluated / per status.

  The defined counts come from the hash-pinned expected manifest, so they cannot shrink silently.

## 7. Manual results (optional input)
`desk-manual-results/1`: `{items: [{id, answer: yes|no|partial, by, date, note}]}`.
- An item without `by` and `date` stays `needs-human-assessment`.
- `no` or `partial` counts as `wrong`.
- Reading time is recorded as an observation in `note`, never as a timed measurement.

## 8. Limits
- No product code. No import or execution of 0524 or 0522 work. No network. No live-book writes.
- Synthetic observations in the tests are built by the lab, labelled `synthetic-self-test`, and prove only checker behaviour.
- Word presence is never used to prove the absence of a forbidden inference. Those checks are manual.
