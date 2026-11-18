# Submission - 0526.dev-authoring/05.03

date: 2026-11-02
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0126.dev-authoring unfiled; slot occupied by 0126.boot-members-0509
readiness: blocked

This is the builder return for the named invocation of 05.03. It is not acceptance, not a live review, and not a Prime authoring pilot. Notes in 06.03.md were reread at close and integrated below. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.03 return pointer after the manifest exists.

## Did

Built `labs/pack-authoring-pass02` as the successor of pass01. Pass01 is loaded under a private name and its file is unchanged. The form declaration `labs/pack-authoring-pass02/forms/build-pack-v1.json` is the only field list. `authoring form` returns that list and writes nothing. Validation walks the same fields. There is no second hard-coded field list.

Named forms are intent, item, note, disposition, and review. A source-only request with no session returns intent. After intent is complete the next form is item, then disposition while a note is unresolved, then review, then none.

Review compares `--draft-sha256` to the candidate before the judgment is stored. The stored review keeps that candidate and a separate `final_sha256` computed from the render that includes the judgment. Freeze checks the final hash, the recomputed candidate, the form declaration, the readable template, the source digest, and the dependency set. Changed meaning, source, form, or set does not silently re-approve.

Ordinary derived-face replacement is `draft.md.history-<operation>` with `derived_conflict` false. A face that does not match the previous canonical render is `draft.md.divergence-<operation>` with `derived_conflict` true. Existing `draft.md.conflict-*` files stay.

`app/librarian.py` loads `app/authoring_tools_v2.py` as `librarian_authoring_tools_v2` for `authoring` only. `app/README.md` authoring section cites that door. `app/authoring_tools.py` and `app/authoring.json` stay. Review-loop v4 and its nine pins stay. The assembler is not called. `complete_claim` stays false. Approval and release stay false.

The retained final document is `evidence/build05.03/runs/20261102T183436Z/05.01.md`, equal to that run's `draft.md`, sha256 `dbdcc43ad9b1e0e225d27e704bc119b53b18fe4b1b41eb4b4d5c49be47c076b5`, 3425 bytes. The candidate Prime would copy from the pre-review inspect is `689bda49a3454d7010da28d38994835b836f2133c57500d90586462065d261e6`. No current-book authoring preview was written. `evidence/authoring05.02` is unchanged.

## Blocked

`0126.dev-authoring` is unfiled. Directory `0126.boot-members-0509` occupies slot 0126. This slice does not free it, file a return, allocate 0184, or invent a receipt. Readiness stays blocked.

Freeze on `D:\Git\lib-build` is refused with `freeze on the live checkout is outside this slice` and writes nothing.

File-symlink creation in the suite is a skip: `WinError 1314`. Junction refusal was executed before the module launched.

This builder does not commit.

## Need

Codex Prime review of this return. Stop here. Do not start the Prime authoring pilot in this build. Runnable commands begin with `authoring form` in `evidence/build05.03/PRIME-USE.md`.

## API and typed forms

Schemas: `authoring-delta-contract/1`, `authoring-pins/2` version 2, `authoring-forms/1`, `authoring-form/1`, `authoring-record/1`, `authoring-result/2`, `authoring-entry-run/1`, `authoring-verification/1`. An outside-book freeze still emits `prime-pack-sources/1` through the pinned checker.

```text
authoring form --book ABS --profile ID [--kind intent|item|note|disposition|review] [--json]
authoring start --book ABS --profile ID --operation ID [--input ABS] [--json]
authoring add-note --book ABS --profile ID --operation ID --input ABS [--json]
authoring add-item --book ABS --profile ID --operation ID --input ABS [--json]
authoring revise --book ABS --profile ID --operation ID --target intent|item|disposition --input ABS [--item NN] [--note ID] [--json]
authoring inspect --book ABS --profile ID [--json]
authoring review --book ABS --profile ID --operation ID --input ABS --draft-sha256 CANDIDATE [--json]
authoring freeze --book ABS --profile ID --operation ID --draft-sha256 FINAL [--json]
```

The caller cannot pass an executable, a template path, or a dependency-set path. Exit 0 is a committed result or an idempotent replay. Exit 2 is `stop:` on stderr and empty stdout. Exit 4 is `partial:` after a failed replace; the previous record stays. The same operation id and the same raw bytes replay. Different bytes under that id conflict and preserve the record. A typed refusal is not stored.

A required string refuses absent, null, empty, and a wrong JSON type. An optional object accepts null as not-applicable and refuses an empty object. An extra key is state extra. Disposition values are integrated, deferred, and rejected. `unresolved` is the compute starting state and is not a submitted value. Integrated requires an existing item and leaves `why` absent. Deferred and rejected require `why` and leave `item` absent. Review JSON does not contain either hash.

Before review, inspect returns `candidate_sha256` equal to `draft_sha256` and `final_sha256` null. After review, `candidate_sha256` stays the pre-judgment document, and `draft_sha256` equals `final_sha256`. The render text does not contain either digest.

## Authority

Compute owns the pass, the item numbers, both document identities, UTF-8, dependency lookup, and the return directory name. The model owns meaning and the semantic review, and copies the candidate inspect already returned. The model does not predict the final-document identity. The record remains authoritative. `draft.md` is derived.

## Source and dependency reuse

Frozen inputs: `evidence/pack05.03/source-manifest.json`, schema `prime-pack-inputs/1`, sha256 `d7cf4eeb27c1ffe06619d73100d6f7fe274a9aff3ac439191aa831cb2f872195`, 9384 bytes, 28 rows, bad 0, missing 0, live bytes 366497. Close recheck: missing 0, snapshot mismatches 0, live bytes 367442, not repinned. Live drift is only `app/librarian.py` and `app/README.md`.

Reused without editing them:

- predecessor `labs/pack-authoring-pass01/pack_author.py` sha256 `30908475162fe9b1a566018d217d26465151b1243bb3a8f391cb54254f3ba10c`, 67547 bytes
- profiles `0423-to-0526` and `fixture-authoring`
- reader `labs/module-dependencies-pass02/depdecl.py` sha256 `a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7`, 53693 bytes; commands `validate` and `requires` only
- set `labs/app-dependencies-pass02/set.json` sha256 `444dba1589c0d6a0204e7a3d6be334b3135d524e4b376e7e92eb8fb434e6f706`, 7054 bytes; label measured-file, form working-tree
- checker `labs/pack-custody-pass01/pack_check.py` sha256 `9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d`, 21563 bytes

The assembler is not called. Review-loop v4 was checked, not rerun. The pass01 suite was not rerun. Gaps: no N3NN address, no return filing, `complete_claim` false, and the hash-to-subprocess gap is not closed. 0710/06.02.decisions stays unseated direction. No template-versus-seated-law conflict was present in the allowed inputs, so no action was held.

## Pins

Successor module sha256 `345c2f79a325ace9e3c0c42847d9ba9ce626ada5be205dbdd26f195907dcf6c2`, 40491 bytes. Form declaration sha256 `b3d18c26699674d7aa0607e491210664b31e90a63dba13860befb5409b0416ab`, 19453 bytes. Door `app/authoring_tools_v2.py` sha256 `f191e43337ab9b6ac2c863b0c0f0eb91a0b55d00d2df99c2897a96a0965e1124`, 8049 bytes. Declaration `app/authoring-v2.json` sha256 `14965030b2344f77e196a1d6a29b8cb74400cc3cf237e4f5ecc44c2adf332d11`, 2106 bytes.

Before: `app/librarian.py` sha256 `dab9bba639da15ae264333f92503167da97a8608e46192092328ad1cc146e35d`, 11566 bytes; `app/README.md` sha256 `5f1ee92125b7613823ea3ceffdab052537380b41b60f01199ba4f5dceeec31dd`, 34696 bytes. Copies are under `evidence/build05.03/before/`.

After: `app/librarian.py` sha256 `3f9dbfec25f71b4b3e0845d367d1d08138854bc1862b3b5b150aa6ce9250bc22`, 11581 bytes; `app/README.md` sha256 `82f839d211e1e4471f89cbc53f04b427d2929b9e67f139f4edd228925415355c`, 35626 bytes.

## Tests

Command: `python -B app/tests/test_authoring_entry_v2.py`. Run `evidence/build05.03/runs/20261102T183436Z`. Schema `authoring-entry-run/1`. 89 cases, failed 0, first_failure null. Exit 0. No earlier failed run exists for this suite.

The run began with a source-only form, then a filled start, two items, a new process for inspect, note dispositions, review of the returned candidate, inspection of the final document, and an outside-book freeze whose page bytes equal the final hash. It also covered stale candidate, changed source, changed form, stale set, missing and stale dependency, explicit field states, retry and conflict, interrupted replace, and a divergent derived face. `where` without `--root` exits 2. Live freeze writes nothing. The synthetic preview hash was the same before and after.

## Factfind

Close recheck hashed the 28 frozen rows and their snapshots. Only the two edited app files differ from the freeze. The predecessor, the two profiles, the reader, the set, and the checker match their pins. `05.02.md` does not exist. HEAD `960d20c5290656095df8457b1740d2d5e586b111`, branch `workshop`, index empty.

## Hostile

A review digest that is not the inspected candidate is refused and is not stored. Freeze with the candidate hash, rather than the final hash, is refused and writes no page. Item text is not executed. A clean dependency answer is not closure. A frozen page is not release. Ordinary history is not labelled as tampering. A pass01 record is not rewritten into the new binding.

## Overflow

None.

## Unprompted

No kernel edit, no migration-lane edit, no memory edit, no model call, no write to `authoring05.02`, no Prime pilot, and no Git stage or commit.
