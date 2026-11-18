# CONTRACT — handoff_check.py repair (0510.colab-tools/05.04)
State: written after notes 06.04 and before code. This lab contract changes only `labs/colab-support-pass02/handoff_check.py`, its new test file and the v2 README. The producer (2b720434…), its handoff format `colab-handoff/2` and digest `colab-package-digest/2` are unchanged, and no new format is introduced.

## Commands
```text
python -B handoff_check.py check --output ABS --expected-digest HEX --json
python -B handoff_check.py copy  --output ABS --expected-digest HEX --to ABS --json
```
Output is one JSON object, schema `colab-handoff-check/2`. Its keys are `result`, `problems[]` (each with `code` and `detail`), `trusted` (present only when `result` is `valid` or `copied`), `unbound_informational` (check only), `not_verified`, `capability`, and for copy `written[]` and `retained[]`.

Exit 0: `valid` or `copied`.
Exit 1: `mismatch` (a bound claim, byte or digest disagrees) or `partial` (copy).
Exit 2: `refused` (malformed or unsafe input, unsupported part or version, or an existing destination). There is never a traceback.

## Trust rule
The expected digest from the launch is the only trust anchor. Every claim in `trusted` is DERIVED from bytes that this digest binds, using fixed v2 rules. handoff.json is never a source of truth. Each consumer-relied handoff field is compared with the derivation, and any difference is `mismatch` with no identity output. Those fields are `schema`, `layout`, `digest`, `digest_domain`, `digest_preimage`, `investigation`, `binding`, `binding_sha256`, `exchange`, `not_created`, `envelope`, `source_map`, `support_projection`, `zip` and `evaluator`.

The informational fields `verify`, `statements` and `digest_rule` are type-checked and returned under `unbound_informational`. They are never trusted.

## Derivation (fixed v2 rules)
1. **Paths and files.** Validate every candidate relative path: NFC, no backslash, absolute, drive, UNC, `.`, `..` or empty segment, and no trailing space or dot. Reject any symlink, junction or reparse point on OUT, its ancestors or any file or directory under it, and any regular file with link count > 1. A `*.return.md` or `*.review.md` anywhere under OUT is `mismatch` (fabricated exchange).
2. **Request and binding.**
   - `package/colab-request.json` is strict UTF-8 JSON (no BOM, duplicate keys or non-finite numbers, ≤ 262144 bytes), schema `colab-request/2`.
   - `package/binding.json` must equal `json.dumps(request.binding, ensure_ascii=False, indent=2, sort_keys=True) + "\n"` byte-for-byte, with schema `colab-binding/1`.
   - The investigation is `binding.investigation`. The page matches `^07(0[1-9]|[1-9][0-9])\.[a-z][a-z0-9-]*$` and the pass matches `^05\.(0[1-9]|[1-9][0-9])$`.
3. **Names.** For pass `05.NN` they are `05.NN.pack.md`, `06.NN.notes.md`, `05.NN.return.md`, `06.NN.review.md`, `templates/05.NN.return.TEMPLATE.md`, `templates/06.NN.review.TEMPLATE.md` and `support/assembler/05.NN.md`. `not_created` is [return, review]. The primary instruction is the pack.
4. **Sources.**
   - `package/source-manifest.json` is `prime-pack-sources/1` with `commit`, `repository` and `sources[]`.
   - Its paths must equal the unique target paths in target order, followed by the `required_sources` paths.
   - Snapshots are `snapshots/NNNN.blob` in order, and each snapshot's bytes must match its row.
   - Each target's `source.sha256` must equal its snapshot, its commit must equal the manifest commit, and its repository label must equal the manifest's.
5. **Assembler request** (`support/assembler/request.snapshot`). It must be strict JSON with `origin` = {book, page, batch=pass}, `identity` = {book, pppp=page[:4], keyword=page[5:], batch=pass}, `revision` = the commit and `paths` = the manifest paths.
6. **Assembler digest**, recomputed under the accepted `pack-assembly-digest/1` rule. The parts are `pack-assembly-digest/1`, `pack-assembly-draft/1`, the request.snapshot bytes and the commit. Then come each source's path, sha256 and length. Then come the planned `05.NN.md`, `request.snapshot`, `source-manifest.json` and snapshots in order, each as name, sha256 and length.
7. **Package set.** It must equal exactly: the fixed colab files, source-manifest.json, the snapshots, and the three support/assembler files.
8. **ZIP.** No duplicate entry names; the member set equals the package set; every member's bytes equal its package file.
9. **Evaluator** (only when `request.scoring` is scored and blind). OUT/evaluator holds `source-manifest.json` with paths equal to `evaluator_sources` in order, plus `snapshots/NNNN.blob`. No evaluator snapshot shares bytes with a candidate snapshot. Otherwise no evaluator/ may exist.
10. **Preimage.** It is rebuilt in the producer's order: domain, layout, file `package/colab-request.json`, file `package/binding.json`, the assembler digest; path, sha256 and length for each colab file in fixed order; the same for evaluator files; then the support path and assembler name for each support file; then the ZIP sha256 and length. The digest is sha256 over parts, each an 8-byte big-endian length followed by its bytes. It must equal the expected digest. A handoff preimage that differs in order, kind or value is `mismatch`; an unsupported part kind is `refused`.
11. **Roles and envelope.** Fixed roles are entry, pack-primary-instruction, notes, template-return, template-review, binding, request, source-manifest, support-declaration, snapshot and support-assembler. The envelope is sorted by path, with the sha256 and bytes of the actual files.
12. **Source map.** For each manifest row: the snapshot path, sha256, bytes, the target ids for that path, and the role `target`, `required` or `other`.

## Not verified (bounded capability)
The checker reports these in `not_verified`; use the pinned full producer verify for them:
- whether ENTRY, the pack, notes, templates, SUPPORT.md and the assembler draft text were correctly rendered from the request (their bytes are bound, not re-rendered);
- heading-section line ranges;
- the content of the assembler receipt and the custody checker's result;
- tool pins;
- the v1 request validation rules beyond schema and binding shape.

## Copy
1. Run the full check; any non-valid result stops the copy before any write.
2. The destination must be absolute, its parent a real non-linked directory, and it must not be inside OUT or contain OUT.
3. A copy needs a fresh destination. If the destination exists, the copy is a read-only replay: `refused`, exit 2, nothing written, with `retained` listed. The problem code is `already-copied` when it is an identical copy and `occupied` otherwise. (This keeps the accepted v2 suite's "never overwrites" exit-2 assertion; that suite is not edited.) Nothing is deleted or overwritten.
4. Otherwise create it, write each file exclusively, then re-hash the copy and re-run the check on the source. A failure mid-copy gives `partial`, with `written` listed. Nothing is deleted and nothing resumes automatically.

## Limits
Size limits: handoff.json ≤ 4 MiB, ≤ 4096 package files, and each JSON file ≤ 4 MiB. Same-user races between check and use are not claimed to be prevented.
