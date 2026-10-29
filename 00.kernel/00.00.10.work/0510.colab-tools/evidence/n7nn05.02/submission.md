# Return — claude-0510-0502 (0510.colab-tools 05.02, N7NN-bound Colab preparation, verification and intake)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-29. Workshop at claim: c406b2a9a3d8d9cc1c67c2c79a8e336989cc0eb1 (unchanged at return).

## Did
- **Pack and claim.** pack05.02: 32 of 32 snapshots match their pins, and live equals all 32. I recorded the Director's chat release and my claim on 05.02. 05.01 was never begun, and 0154 stays a reservation only.
- **Order.** Notes FIRST (06.02.md), then evidence/n7nn05.02/CONTRACT.md, then code.
- **Module** `labs/colab-support-pass01/colab_support.py`, standard library only, with `preview`, `prepare`, `verify` and `intake`.
  - Strict `colab-request/1` carries the exact shared `colab-binding/1`.
  - The investigation origin must be N7NN (0701–0799). N5NN batches, the 0700 door and a target naming the investigation page all refuse.
  - Targets are read as Git blobs at their commit and must match their sha256. A stale hash reports the actual hash as a fact and never retargets. Sections are exact heading lines outside fences, with an explicit occurrence for duplicates. `kind: id` refuses; v1 has no id syntax.
  - The accepted pack assembler is reused through pins. An adapter maps the request onto `pack-assembly-request/1`. The assembler is loaded in-process to plan and run by its CLI to assemble, with raw output kept.
  - The package has the shared file set plus the assembler's request.snapshot, completion-receipt.json and the exact colab-request.json. The ZIP is deterministic, and there is no `.colab` tail.
  - The `colab-package-digest/1` digest binds the request, binding, assembler digest, colab files and the planned ZIP.
  - Verify recomputes every file from the packaged request and snapshots. It runs the pinned assembler verify on a byte-identical projection of the assembler's file set, because that verify's exact-set rule would otherwise fail on the colab files.
  - Intake verifies the package and requires the reservation origin to equal the binding's investigation. It then runs the pinned helper's capture and verify and the inspector, keeps every raw output and exit, and prints `colab-intake-provenance/1` with a pointer line. It edits no page.
- **Tests.** 50 tests on disposable repositories, books and outputs with the real pinned assembler, checker, helper and inspector. Three recorded full runs all passed: 49, then 50, then 50 tests, with 0 skips. They cover:
  - strict malformed, type, duplicate, nonfinite and limit inputs;
  - N5NN origin refusal, the door, and a valid N7NN origin;
  - multi-target, whole-file and section binding;
  - duplicate-heading ambiguity, and a stale source or section;
  - unsafe and linked paths, a digest mismatch, partials at all four hooks, collisions and replay;
  - blind evaluator overlap by path and by bytes, unscored and open-scored modes;
  - exact replies, Overflow and template retention, ZIP-only closure and local-path refusal;
  - a missing image body versus a committed image that travels;
  - tamper and extra-file detection, and a bad pin before launch;
  - intake capture, replay, changed-bytes attention, wrong target-page origin and implementation-batch origin;
  - CLI exits with no traceback.

  Each test class asserts that the source repository is unchanged.
- **One real-source package.** It targets `0411.colab/01.md` `## Compute module — proposed operations` at c406b2a9, with a declared FIXTURE binding 0701.colab-compute-ops/05.01. No model was called. Digest **a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4**, verify intact, assembler verify exit 0, replay `already-prepared`. prepared-colab.zip and binding.json are byte copies.
- **Labelled synthetic intake** in a disposable book, origin 0701/05.01: `captured`, receipt a83056a2…. The replay gave `already-captured`. A reservation whose origin was the target page 0411.colab was refused as `wrong-origin` before capture.
- **Friction and contract changes during the build**, all recorded in 06.02, CONTRACT and REAL-USE:
  - A blind rubric now lives only in evaluator sources, because the request travels in the ZIP. I found that leak while writing limits.
  - The assembler's writable scope comes from `environment.write`.
  - A stale hash reports the actual hash.

## Blocked
Nothing.

## Need
- Prime's review of this return and of the interface gaps G01–G07 in 06.02. The main ones:
  - section-id syntax;
  - one commit per package;
  - where a ZIP-only recipient sees the digest;
  - who reserves the investigation return member;
  - confirmation that N7NN means 0701–0799.
- Prime should use the tool on a current design piece before a fresh Colab probes it, as 0411 asks. REAL-USE gives the invocation, the manual inputs that remain, and the integration contract for Grok-1's adapter after both returns are reviewed.
- Note that the reserved capture list names the evidence files only. The lab code (`labs/colab-support-pass01/`) is not a captured artifact. Its hashes are below and in verification.json.

## Limits and notes
- Labels are not authentication. The 0701 investigation is a fixture; no page was created. Neither the package nor the receipt is a release, review or acceptance.
- I did not read, run or integrate any 0511 or `labs/colab-workflow-pass01` file.
- Mutation testing was not done. Unchanged dependency suites were not rerun.
- A tool's hash is checked immediately before each launch. No sandbox is claimed against a same-user race between that check and the launch.
- A superseded smoke package (digest d8f5846d…, before two adapter edits) stays in session temp and was not captured.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0510.colab-tools/06.02.md: 27ec455fc99754f3a00f4291db54c1873f45951fdca4559aa94a86a47b21bb6a, 11631
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/CONTRACT.md: 323043016f72f8ec200d8e5fe99df1fff24b5716130b8e54852ed0f13abfe364, 10242
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/request-example.json: 460e8ef45e5095e1af91133a475524a727d4aa21a4d3d1d84801bc0d5e2a3e25, 6426
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/binding.json: e1311900743bde2274e9ceb729150673fb815d9d47320602d4de71ada1136a21, 691
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/REAL-USE.md: f844b9d47ad21d15da8bd8443d76ed9cb5d6d63bfaa7cacf63a7d148e445cf13, 10015
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/verification.json: 100f7f049643b68e4be5632d49f68e1eb3e74b3f24d7a23ebe68faa4bed004d9, 43501
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/prepared-colab.zip: f44c4bf1985ba893a4e09d80593438ac011cb1fe35d695a378c811ec41f44c60, 52146
- labs/colab-support-pass01/colab_support.py (not captured): 33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c, 67781
- labs/colab-support-pass01/README.md (not captured): 8b04686131fb00f35987754c10a3b540a02f13b736d99761f033c156b2b12d8e, 5270
- labs/colab-support-pass01/tests/test_colab_support.py (not captured): f6be57f6bccf9a9aada4e32e0fc2681964cd2ead7bcb4e1f5ff6dc5983212ff8, 33110
