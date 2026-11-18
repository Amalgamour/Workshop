# CONTRACT — colab-support-pass02, exchange layout v2 (0510.colab-tools/05.03)
State: written after notes 06.03 and before code. Lab contract only. It implements `0411.colab/evidence/exchange-layout-v2/CONTRACT.md` for the producer side and changes nothing in v1, the helpers, 0411 or 0700.

## Commands
```text
python -B colab_support.py preview --request ABS --config ABS --json
python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
python -B colab_support.py verify  --output ABS --config ABS --json
python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug
       --return-file ABS --source-root ABS --artifact REL|LOGICAL [...] --json
python -B handoff_check.py check --output ABS --json
python -B handoff_check.py copy  --output ABS --to ABS --json
```
Exits follow v1: 0 is a positive result, 1 a recorded negative (partial, mismatch or attention), 2 a refusal.

## Versions
| item | v2 label |
|---|---|
| request | `colab-request/2` |
| config | `colab-config/2` |
| layout | `colab-exchange-layout/2` |
| digest domain | `colab-package-digest/2` |
| OUT verification | `colab-package-verification/2` |
| handoff | `colab-handoff/2` |
| intake output | `colab-intake-provenance/2` |
| placement proposal | `colab-placement-proposal/2` |

Any other schema value, including a v1 label, refuses with code `version`. Nothing is migrated or relabelled. A v1 OUT given to v2 verify refuses.

## Config `colab-config/2`
The v1 keys (`repositories`, `python`, `assembler`, `checker`, `helper`, `inspector`) plus `producer_v1`, the absolute path of accepted v1 `colab_support.py`, pinned at 33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c (67781 bytes). v1 is loaded only after its hash matches.

## Request `colab-request/2`
Exactly the v1 request keys, with `schema` = `colab-request/2`, plus `preparation_notes`: a list of 0–64 text items under v1's text rules. Validation builds an in-memory v1-shaped copy (schema `colab-request/1`, `preparation_notes` removed) and runs v1 `validate_request`. Binding, targets, sections, N7NN origin, scoring, evaluator, zip-only and limit rules are therefore v1's. The packaged `colab-request.json` is the exact v2 bytes.

## Package (`OUT/package/`, zipped)
| path | role |
|---|---|
| `ENTRY.md` | orientation; names the one primary instruction source and the pass |
| `05.NN.pack.md` | **primary instruction source** for pass 05.NN |
| `06.NN.notes.md` | supplied preparation notes, context, gaps and exact Director replies; not a review |
| `templates/05.NN.return.TEMPLATE.md` | return template; TEMPLATE banner |
| `templates/06.NN.review.TEMPLATE.md` | review template; TEMPLATE banner |
| `binding.json` | canonical `colab-binding/1` |
| `colab-request.json` | exact request bytes |
| `source-manifest.json`, `snapshots/NNNN.blob` | the accepted assembler's manifest and blobs (source closure) |
| `support/SUPPORT.md` | declares support/ as transport support, not instructions |
| `support/assembler/05.NN.md`, `request.snapshot`, `completion-receipt.json` | byte copies of the assembler's own outputs |

No file named `05.NN.return.md` or `06.NN.review.md` (or any `*.return.md` / `*.review.md`) exists in OUT at preparation.

## OUT (exact set)
`package/…`, `prepared-colab.zip`, `evaluator/…` (blind scoring only), `assembler-request.json`, `assembler-run.json` (raw helper output, not recomputed), `assembler-output/…` (the assembler's own directory), `handoff.json`, and `verification.json` (written last). Any other path is a pack defect.

## Digest `colab-package-digest/2`
Each part is an 8-byte big-endian length followed by its bytes. The parts are, in order:
1. `colab-package-digest/2`
2. `colab-exchange-layout/2`
3. the request bytes
4. the canonical binding
5. the assembler digest
6. path, sha256 and decimal length for each of: `ENTRY.md`, `05.NN.pack.md`, `06.NN.notes.md`, the two templates, `binding.json`, `colab-request.json`, `support/SUPPORT.md`, then the evaluator files
7. for each support copy, in fixed order: its support path, then its assembler name
8. the ZIP's sha256 and decimal length

`handoff.json` lists the same preimage as data.

## Prepare
1. Validate, plan, compare the digest, and check that OUT is fresh. This reuses v1's output rules: outside every repository, outside any `00.kernel` ancestor, not linked, and absent or empty.
2. If OUT is occupied by an intact package at the same digest, the result is `already-prepared` and nothing is written. Anything else is a `collision`, with the retained paths listed.
3. Write `assembler-request.json`. Run the pinned assembler CLI into `assembler-output/`. Its bytes must equal the plan, otherwise the result is `partial`.
4. Write the package files exclusively, then the evaluator files, the ZIP, `handoff.json`, and `verification.json`.

Private hooks: `before-assembler`, `after-assembler`, `before-zip` and `before-verification`.

## Verify
1. Read the OUT tree; a linked entry is a defect.
2. Require `verification.json` with schema `/2`; a missing file gives `partial`.
3. Re-plan from the packaged request and snapshots.
4. Compare the exact OUT file set and every byte, except `assembler-run.json`, which is checked to be valid JSON with exit 0.
5. Compare the ZIP members with package/.
6. Run the pinned assembler verify on a temporary projection.
7. Confirm no pre-created return or review exists.

Findings carry a kind: `pack-defect`, `input-defect` or `tool-limitation`.

## Handoff `colab-handoff/2`
Keys: `schema`, `layout`, `digest`, `digest_domain`, `digest_preimage[]`, `investigation`, `binding`, `binding_sha256`, `exchange{pass,nn,pack,notes,return_name,review_name,return_template,review_template,primary_instruction}`, `not_created[]`, `envelope[]{path,role,sha256,bytes}`, `source_map[]{source_path,snapshot,sha256,bytes,targets[],role}`, `support_projection[]{support_path,assembler_name,sha256,bytes}`, `zip{path,sha256,bytes,members[]}`, `evaluator[]`, `verify{argv,config_schema,config_keys,pins}`, `statements[]`.

`handoff_check.py` uses only the standard library. It recomputes every envelope hash, the ZIP members, the not-created names and the digest from the preimage. `copy` writes an exclusive byte copy of package/ and re-checks it.

## Intake
1. v2 verify must be intact.
2. Run the inspector. Status must be `reserved` or `complete`, and the origin must equal the investigation `{book,page,batch=pass}`; otherwise the result is `wrong-origin`, exit 2, and nothing is captured.
3. Run the pinned helper `capture`, then `verify`, then the inspector again. Keep every raw run.
4. Output `colab-intake-provenance/2` with a separate `placement` object of schema `colab-placement-proposal/2`:
```text
{schema, action:"proposed; not written", destination:{book,page,file:"05.NN.return.md"},
 source:{member,file:"return.md",sha256,bytes,receipt_sha256,manifest_sha256},
 rule:"exact bytes from the verified capture; provenance stays in this record, not in the text"}
```
The return bytes are never edited. Nothing is written to a live book. No review file is produced.

## Not
No edit to v1, the helpers, 0411, 0700, law, the app or Grok outputs. No section-id syntax, multi-commit support, model call, live placement, automatic next pack or closure, and no claim of workflow integration.
