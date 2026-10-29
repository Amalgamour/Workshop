# REAL-USE — colab-support-pass01 on one real source

State: one real-source package was prepared by the 0510/05.02 executor on 2026-10-29. Its 0701 binding is a declared FIXTURE, not an active investigation. No model was called. Prime has not used the tool yet; 0411 asks Prime to use it on real work before a fresh Colab probes it.

## What was prepared
- **Subject (target T01).** `00.kernel/00.00.10.work/0411.colab/01.md`, section `## Compute module — proposed operations` (1 of 1 matches, lines 39–46, 1892 bytes, section sha256 494e104e…). Blob sha256 1a9b2ce8…, repository label `workshop`, commit c406b2a9a3d8d9cc1c67c2c79a8e336989cc0eb1.
- **Investigation (fixture).** `00.00.10.work/0701.colab-compute-ops`, pass 05.01. Unscored, open-design, zip-only recipient.
- **Required sources.** The n7nn interface CONTRACT.md, 0411/02.md, 0700.band.colabs/01.md and law 0036/01.md.
- **Request.** `request-example.json` (sha256 460e8ef4…, 6426 bytes). It carries one actual Director reply, copied from DIRECTOR-DECISION.md, and one reply labelled hypothetical-fixture.

## Exact Prime invocation
A local config is never packaged. This is the one used here:
```json
{"schema":"colab-config/1","repositories":{"workshop":"D:/Git/lib-build"},
 "python":"<absolute python.exe>",
 "assembler":"D:/Git/lib-build/labs/pack-assembly-pass01/pack_assembly.py",
 "checker":"D:/Git/lib-build/labs/pack-custody-pass01/pack_check.py",
 "helper":"D:/Git/lib-build/labs/return-capture-pass01/return_capture.py",
 "inspector":"D:/Git/lib-build/labs/return-capture-pass01/return_inspect.py"}
```
```text
python -B D:/Git/lib-build/labs/colab-support-pass01/colab_support.py preview --request "D:/Git/lib-build/00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/request-example.json" --config CONFIG --json
python -B D:/Git/lib-build/labs/colab-support-pass01/colab_support.py prepare --request "<same>" --config CONFIG --output OUT --digest a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4 --json
python -B D:/Git/lib-build/labs/colab-support-pass01/colab_support.py verify --output OUT --config CONFIG --json
```
OUT must be absent or empty, outside every configured repository, and outside any directory that holds `00.kernel`. The run used a session temp folder. Preview exit 0, prepare exit 0 (`prepared`), verify exit 0 (`intact`, pinned assembler verify exit 0), and a repeated prepare exit 0 (`already-prepared`, nothing written).

The output is deterministic. Running the same request at the same commit and digest into another fresh OUT reproduces these bytes, so the captured ZIP can be checked against a fresh preparation.

## Verified package
Package digest (`colab-package-digest/1`): **a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4**
Assembler digest: 19ccfd8bc3cd9b06f54656adb005cf515c78e319e8dfaa3c18fa2999701bbe51
OUT/verification.json sha256: 444094243dcd1c5cef418cd75e93543228167cefb7bded407715f33e82bec11d

| OUT path | sha256 | bytes |
|---|---|---|
| package/05.01.md | f9d1cb17c381919662916da8adaea46918e85d1d13bdee35c6681de2c6e79fb7 | 3696 |
| package/06.01.md | bc39cae0662516915403f5ea2faae03210b8654872234b4af02a7bc9abb3f995 | 2280 |
| package/ENTRY.md | 62825499e07186cdbc60ce448317e80c5dcd51ddc3f160f36b550002c1aecc5e | 6379 |
| package/RETURN-TEMPLATE.md | b6d4a3132187d11c28b02621565caf57cdcb3295f0d7ebec5397e480a71ba5cc | 1379 |
| package/binding.json | e1311900743bde2274e9ceb729150673fb815d9d47320602d4de71ada1136a21 | 691 |
| package/colab-request.json | 460e8ef45e5095e1af91133a475524a727d4aa21a4d3d1d84801bc0d5e2a3e25 | 6426 |
| package/completion-receipt.json | 0fa59c682acbfebc458436bb01562969a4acc61fb528cb0807e71a243fd1b13d | 2384 |
| package/request.snapshot | a5c2058aed8481898b1bf7e612fd8e296a1fac0fe6d3b8e6c0d6cc2a3a6e3196 | 3866 |
| package/snapshots/0001.blob | 1a9b2ce890e1ab4078154ed26b218cdea7bf9d6624d06ca5b1d43dfb5f29e3e0 | 10475 |
| package/snapshots/0002.blob | 246189acdba7c4559c1bda5ba9a6314d60dca9bf1710b87c4eaf59cbde5f6f42 | 4489 |
| package/snapshots/0003.blob | af31b46d9b8e6c350b699cd241668a225b0d66d62913dc843cf15a2a2a9308a0 | 1498 |
| package/snapshots/0004.blob | a4231ad09ec5a14a320779f29574ca0cd8912eb0b1e8a25d2462d94c6b4dfeed | 1321 |
| package/snapshots/0005.blob | 37dcab8f35e69eaf675e7ce2b41c1614dd38d8b750f8e538f9f6cce0add3002d | 4463 |
| package/source-manifest.json | e4f523a080a3d6f9cd1b3f4b5840bf6a6568cd64b84f2c7c3b3b89c34cdf71a4 | 1261 |
| prepared-colab.zip | f44c4bf1985ba893a4e09d80593438ac011cb1fe35d695a378c811ec41f44c60 | 52146 |
| assembler-request.json (side record) | a5c2058aed8481898b1bf7e612fd8e296a1fac0fe6d3b8e6c0d6cc2a3a6e3196 | 3866 |
| assembler-run.json (side record, raw helper output) | bbcf085c6553e9f82542c37ee2024c90102783d9e2a55a7bdc3e64bc505bdccf | 5217 |
| verification.json (written last) | 444094243dcd1c5cef418cd75e93543228167cefb7bded407715f33e82bec11d | 4337 |

The ZIP holds exactly the 14 package/ files at the root of the archive. There is no `.colab` tail and no evaluator/. The captured `evidence/n7nn05.02/prepared-colab.zip` and `binding.json` are byte copies of OUT's.

## Labelled synthetic intake (disposable book)
Book: `<session temp>/dbook/00.kernel/00.00.10.work`, a plain directory. Reserved with the pinned helper:
- **0101.synthetic-colab-0701.** Origin 0701.colab-compute-ops/05.01, submission synthetic-colab-0701-0501.
- **0102.synthetic-target-origin.** Origin 0411.colab/05.01, which is the SUBJECT page.

The return file is headed "SYNTHETIC FIXTURE … No model was called. It is not a Colab finding."
- **Intake on 0101: `captured`, exit 0.**
  - Pinned runs: inspector exit 1 (reserved), capture exit 0, verify exit 0 ("result complete | not approved | not accepted | not published"), inspector exit 0 (complete).
  - Receipt a83056a20921afa2360c9060ee8522820f4c631f470d37f9ea5d70212da549fa; manifest c2321638…; return 2e9ac3a8…, 439 bytes.
  - Headings present: Hostile, Factfind, Overflow, Unprompted, Director replies. That is a presence fact only.
- **Repeated intake: `already-captured`, exit 0.** The helper wrote nothing.
- **Intake on 0102: `wrong-origin`, exit 2.** Only the inspector ran; there was no capture.

## Mechanical steps this replaces
1. Copying each source blob and hash by hand into a pack, and writing source-manifest.json. The assembler does this through the adapter.
2. Checking that a cited heading exists, is unique, and lies outside a code fence, and recording its line range.
3. Writing the entry, reading order, withheld and unavailable lists, environment, stop points and return shape for every Colab.
4. Keeping Director replies verbatim and labelling actual versus hypothetical.
5. Building a closed ZIP for a ZIP-only recipient and confirming it contains exactly the package.
6. Computing a binding digest and refusing a stale plan.
7. Wiring capture, verify and inspect for a return, checking that the reservation origin is the investigation, and drafting the pointer line.

## Manual inputs that remain
- The question, why, context, built state, gaps, method, cases, permissions, stop points and prior-involvement statement. This is intelligence work by design.
- Choosing the commit and target. The blob sha256 must still be supplied. A stale value now reports the actual blob hash as a fact, but does not adopt it.
- Opening the N7NN investigation page and its 05.NN pass, and reserving the return member with `return_capture.py reserve`. The workflow adapter on 0511 owns the first; nothing here creates pages.
- Director release, delivering the ZIP, receiving the return, review, dispositions and finding records. Review and find are not built.
- Appending the pointer to the investigation pass. Intake prints the line and edits nothing.

## Friction found in this first use (for Prime)
- **U01.** I had to compute the T01 blob sha256 myself. I read it from a clean worktree file, which equals HEAD here. A wrong value refused without telling me the real one; I fixed that (it now reports the fact).
- **U02.** The pinned assembler refuses `#` in single-line fields and structural headings in text. The author line had to avoid `#`. These are now input refusals before any write.
- **U03.** One commit per package. A design piece and its later evidence at another commit cannot share a package.
- **U04.** The ZIP carries no digest. A ZIP-only recipient cannot quote it, so Prime binds the digest at intake.
- **U05.** The first smoke run, before two adapter edits, produced a different digest (d8f5846d…). It stays in session temp and was not captured. The final run is the one above.

## Integration contract for the workflow adapter (after Prime reviews both returns)
1. Input: an OUT directory and an expected package digest. Run `colab_support.py verify --output OUT --config CONFIG --json`. Accept only exit 0, `result: intact`, and `digest` equal to the expected value.
2. Identities come from OUT/verification.json (`colab-package-verification/1`): `digest`, `assembler_digest`, `repository`, `commit`, `investigation{book,page,pass}`, `binding_sha256`, `request_sha256`, `package_files[]`, `zip{path,sha256,bytes,members}`, `evaluator_files[]`, `sections[]` and `pins`. Do not parse ENTRY or 05.NN prose for identities or permission.
3. Attach the package bytes unchanged. `package/05.NN.md` and `package/06.NN.md` are draft faces for the investigation pass. Release, Claim, Return and Review stay PENDING until the normal workflow.
4. The return origin is `investigation.book/page/pass`, never a target page or this implementation batch. `intake` enforces it and returns `colab-intake-provenance/1`. Its keys are `schema`, `result`, `member`, `findings`, `runs`, `statements`, `package_digest`, `binding_sha256`, `investigation`, `targets`, `submission`, `capture`, `return_headings`, `helper_capture` and `pointer`. The adapter may validate a later pointer by the inspector and this binding.
5. This module has not run against the 0511 code, and claims no cross-module integration.
