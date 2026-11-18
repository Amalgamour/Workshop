# CONTRACT — 0705 pass03 real-output adapter and failing baseline
date: 2026-11-01
who: claude-opus-5-5 (Claude)
state: lab contract, written before code. It extends the pass02 CONTRACT (snapshot 0032) and changes nothing in pass01 or pass02.

## 1. Pinned inputs (all from pack05.03 snapshots, copied into a disposable `pinned/` tree after hash checks)
| Role | Path in pinned tree | Snapshot | sha256 |
|---|---|---|---|
| candidate | `labs/prime-desk-pass01/prime_desk.py` | 0063 | from manifest |
| candidate reader | `app/context.py` | 0034 | 5b1a31d4… (equal to the candidate's READERS pin) |
| fixture builder | `pass02/build_fixture.py` | 0042 | from manifest |
| cases | `pass02/cases.json` | 0043 | dcb4cb27… |
| checker | `pass02/check.py` | 0044 | from manifest |
| expectations | `pass02/expected.json` | 0045 | d44d237a…8e09 |
| manual checklist | `pass02/manual-checklist.json` | 0047 | 18d8f1d1… |

The fixture source manifest is `0705/evidence/pack05.02/source-manifest.json`, the one the expectations were written against.

No other code is run. No live lab file is executed: the pinned tree is built from snapshot bytes only.

## 2. Run (`run_baseline.py --out NEW-ABS`)
1. Build the pinned tree and verify every sha256.
2. Build all fixtures with the pinned builder.
3. For each executable case, copy the fixture to `runs/<case>/book/`. Write the **request artifacts**, labelled SYNTHETIC REQUEST ARTIFACT:
   - `prime-desk-shadow-selector.json`;
   - `prime-desk-catalog.json`;
   - `request.json`.
4. Run the pinned candidate as a separate process: `python -I -B pinned/labs/prime-desk-pass01/prime_desk.py view --request ABS --json`. If its `selected.id` names a work, also run `packet --work-id <that id> --json`. For C14, run `view` a second time in a new process.
5. Keep for every run: the argv, the exit code, the raw stdout and stderr bytes (as files), their sha256, the request sha256, the candidate sha256 and the fixture-manifest sha256 → `runs/<case>/run-record.json`.
6. Adapt each case's raw output to `desk-observation/1` → `observations/<case>.json`. Write `mapping-trace/<case>.json` (the raw JSON pointer for every mapped fact) and `conflicts/<case>.json`.
7. Run the pinned pass02 checker with `--expected-sha256 d44d237a…8e09` and the manual checklist. No manual results are supplied, so all 24 items stay pending.

## 3. Request preparation (adapter `prepare_request`)
- **R1. The shadow selector names the work whose address equals `current_work` in the pinned pack05.02 snapshot of 0401/06.01.** That work is 0522.review-construction/05.04. The rule is identical for every case and never reads a case's edited canonical record or expected.json.
- **R2.** The canonical 0401/06.01 is a reference with role `assignment`. `tools_root` points to the pinned tree, so the candidate's own pinned reader parses it.
- **R3.** Work entries come from catalog `works`: id `w-<slug>`, address = work_ref, path, and sha256/bytes of the current fixture file. A catalog-declared pin replaces the current hash (C13).
- **R4.** Catalog roles map to references: decision record → `director`, goal → `goal`, previous selector → `other`, catalogued pin → (it is the work entry). Workers map to `{id: name, work_id: "unassigned", evidence: null}` plus `supplied {speaker: "catalog (supplied)", about: name, text: "<name> <state> (supplied label; source <path>)", limit}`. Cross-instance references map to `foreign`.
- **R5.** The candidate catalog file lists works and parallels: `{work_id, address, label: "supplied (catalog index)" or "work"}`.

## 4. Mapping (adapter `normalize`) — exact table in `pass03/mapping.json`
- Only values present in the candidate's raw JSON, plus these declared structural transformations:
  - an instance root path → its fixture instance label, by exact path equality;
  - `foreign[].read == false` with a different root → a `sources` row with status `outside-instance`;
  - a candidate source status `matched` → `ok`;
  - a candidate source status `stale` or `changed` → `changed`;
  - absent → `absent`.
- `basis` is copied verbatim. The adapter never upgrades it.
- Anything the candidate does not output goes in `producer.unmapped` and stays empty in the observation: works' claim, return, custody, review, disposition, approval, blocked and tails; holds; parallel; coverage; quotes of kind interpretation; worker state; refusals.
- **Conflicts:** each case's `conflicts.json` lists contradictions between candidate facts, for example `selected.address` against `record.assignment_reader[].fields.current_work`, or duplicate ids. They are reported and never resolved.
- `producer.kind = candidate` and `adapter.status = connected` are labels. They authenticate nothing.

## 5. Adapter self-tests (`tests/test_adapter.py`)
| Test | Expected outcome |
|---|---|
| raw stdout altered after recording | refused (hash mismatch) |
| wrong candidate sha256 in the run record | refused |
| a field missing in raw JSON | the observation's field missing or unmapped, never invented |
| candidate `basis: supplied` | stays `supplied` |
| duplicate or conflicting facts | listed in conflicts |
| `prepare_request` reading expected.json | impossible by construction; the test asserts that `prepare_request` has no expected argument and that the shadow selector is identical across cases |

## 6. Verdict reading
- The pinned checker's `desk_verdict` will be `not-passed`. The report separates:
  - **(a) defects:** `wrong` facts;
  - **(b) coverage gaps:** `unsupported` (unmapped) and `missing`;
  - **(c) pending human assessment:** 24 manual items.
- Only (a) is product evidence. (b) can be a product limit or an adapter limit, and is named per field.

## 7. Successor rerun boundary (documented, not executed)
`--candidate PATH --candidate-sha256 HEX --dependencies MANIFEST`:
- The path must be allowlisted (an existing view/packet CLI under `labs/prime-desk-pass*/prime_desk.py`).
- The hash must be supplied by Prime, and every dependency pinned.
- A new output schema needs an adapter revision with its own self-tests. Old expectations are never coerced to fit.
