# Return — claude-0510-0503 (0510.colab-tools 05.03, versioned N7NN exchange-layout preparer)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-29. Workshop at claim: 6896224510fe0bcebac291fce7ed311a2cd085cb (unchanged at return).

## Timing and boundary
- **Grok-1** is still repairing v1 workflow integration on 0511/05.02 against frozen v1 33bbe41c….
- **Grok-2** is still building Prime reporting on 0512/05.01.
- I did not read or change any of their pages, claims, evidence or labs (`colab-workflow-pass01`, `prime-review-pass01`). Their outputs are not dependencies here.
- No v2 workflow integration is claimed.

v1 (code, README, tests) and the four helpers are byte-identical before and after this batch.

## Did
- **Pack and claim.** pack05.03: 16 of 16 snapshots match their pins, and live equals all 16. I recorded the Director's release and my claim on 05.03.
- **Order.** Notes FIRST (06.03.md), then evidence/exchange05.03/CONTRACT.md, then code.
- **New lab `labs/colab-support-pass02`**, standard library only:
  - `colab_support.py`: preview, prepare, verify and intake;
  - `handoff_check.py`: a standalone consumer check and copy;
  - README, tests, and a config example and real request example.
- **Reuse of v1.** v1 is loaded by pin and its validation, section resolution, pinned tool loading and launch, ZIP and output rules are reused. No custody engine is copied.
- **Versions** fail closed: `colab-request/2`, `colab-config/2`, `colab-package-digest/2`, `colab-package-verification/2`, `colab-handoff/2`, `colab-intake-provenance/2` and `colab-placement-proposal/2`. A v1 request, config or OUT is refused; nothing is migrated.
- **Layout.** The package holds:
  - ENTRY, naming ONE instruction source;
  - `05.NN.pack.md`;
  - `06.NN.notes.md`, which is supplied notes plus exact Director replies, not a review;
  - `templates/05.NN.return.TEMPLATE.md` and `templates/06.NN.review.TEMPLATE.md`, each with a TEMPLATE banner;
  - the binding, the request and the source closure;
  - `support/`, which holds the accepted assembler's legacy draft, request and receipt, labelled as transport support and verified byte-for-byte against the assembler's own output and by the pinned assembler verify on a projection.

  No real `05.NN.return.md` or `06.NN.review.md` is created. Verify flags one anywhere in OUT as `fabricated-exchange`.
- **Handoff.** `handoff.json` gives:
  - the digest preimage, the binding and the exchange names (including the not-created return and review);
  - the envelope roles and hashes, and the source-to-snapshot map;
  - the support projection, the ZIP, and the verify invocation and config contract.

  `handoff_check.py` validated and copied the real package without importing either producer or any Grok code.
- **Intake.** It enforces the origin `investigation book/page/05.NN`, runs the pinned capture, verify and inspect, and keeps the exact bytes. It emits a separate placement proposal mapping the member, receipt and return hash to `<page>/05.NN.return.md`, `proposed; not written`. Nothing is injected into the return or written to a live book.
- **Tests.** 24 tests, 0 skips.
  - The first run stopped on a test-helper name clash (`run` shadowed `TestCase.run`). After renaming it, two full runs passed.
  - The suite covers:
    - names and pass binding;
    - missing, misnamed and extra files;
    - no return or review before receipt, and fabricated ones detected;
    - exact notes and quotes;
    - template versus review;
    - support declared not instruction;
    - wrong request, config and OUT versions in both directions;
    - a wrong producer pin and inherited v1 rules;
    - wrong origin and digest mismatch;
    - byte mutations of the pack, support, snapshot, handoff, assembler-output, template and ZIP;
    - linked output and linked entry;
    - partials at all four hooks, collision and replay;
    - blind evaluator absence;
    - the standalone check and copy;
    - synthetic intake with placement, replay, conflict and wrong target origin;
    - CLI with no traceback.
  - The module asserts the seven frozen dependency hashes before and after.
  - v1's unchanged 50-test suite also passes as a regression check.
- **Real-source package.** It targets the committed 0411 exchange-layout-v2/CONTRACT.md (whole file) at 6896224, with the fixture investigation 0701.colab-exchange-layout/05.01. No model was called.
  - Digest **42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184**, verify intact, assembler projection verify exit 0, replay `already-prepared`.
  - handoff check `valid`, copy `copied`.
  - Labelled synthetic intake `captured`, replay `already-captured`, wrong target origin refused with exit 2.
- **Write-ups.** REAL-USE gives the exact invocation and the inputs Prime still supplies. ADOPTION names Grok-1's future layout update and Grok-2's review mapping without changing their work. The artifact manifest binds code, tests, templates, handoff and outputs.

## Blocked
Nothing. No consequential design fork arose. Three questions are recorded for Prime instead of being decided (06.03 X01–X03):
- whether notes stay a snapshot;
- how a second return for the same NN is versioned;
- support/ visibility.

## Need
- Prime's review of this return and of X01–X03.
- Before any v2 end-to-end claim: a reviewed and released workflow pass that consumes `handoff.json`, and a review-output mapping onto `06.NN.review.md` (see ADOPTION).
- The reserved capture list names the evidence only. Lab code is bound by hash in artifact-manifest.json and below.

## Limits and notes
- Labels are not authentication. The 0701 investigation is a fixture.
- Neither a package nor a receipt is a release, review or acceptance.
- There was no code mutation testing, and no measured time or token claims are made.
- The hash of a pinned tool is checked immediately before each launch. No sandbox is claimed against a same-user race.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0510.colab-tools/06.03.md: f0c45a282cd782a157ef79cdce10a0dda71216787c77caa15ecb1f8d3a22af2a, 10677
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/CONTRACT.md: d6da4eec4fef1f7ac53cbb3a68455f1876b3db88fb76cb61d8e8e47b9dfd2811, 7361
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/verification.json: 0e8139e0acf3457f71e6c2e75d973a05983963f0b4697f0355201f8151b04ac1, 64260
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/REAL-USE.md: 2f4a321e50a09f62bd175c6ae5511580e5feab99f01ee6d761d52be706e626f1, 7245
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/ADOPTION.md: 0728703ae705eb309a20d03b7f6efc932500c947b5430084d012b76006581b1b, 2685
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/artifact-manifest.json: 5f53965a0146fe49dd9bce5233fd35d3147193a07e115f5c152e762191a5dc1f, 4779
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/prepared-colab.zip: 5f77b08318a40b9329f51a9178e274637271d1cf06d4aa3e9e1ea3c354862cfe, 43099
- labs/colab-support-pass02/colab_support.py (not captured): 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b, 53892
- labs/colab-support-pass02/handoff_check.py (not captured): db921e1cc84483b74da0a475fa40dcee8d66bddea6ee778abe948e71336261ce, 6228
- labs/colab-support-pass02/README.md (not captured): 1b410759e85f8527bd2b27d5d1b5986f8a1928230de276179bf5e9e36ad5146b, 4842
- labs/colab-support-pass02/tests/test_colab_support_v2.py (not captured): 13eaa1178bdfb432210bbd1535126b40ae75c4e1c3ce12addeb8ccc0cea3d1a5, 26748
- labs/colab-support-pass02/examples/config.example.json (not captured): a95440a63e4c96d639f5a5296d257de1b8e8b5eeb82b1cfa21d6d505c3c88278, 517
- labs/colab-support-pass02/examples/request-exchange-layout.json (not captured): 5778b69507ff4eadd67e0b3eb2bdb3aa7d22440110d1ddb16e09b5e5e7c0b1fa, 6270
