# Return — claude-0510-0504 (0510.colab-tools 05.04, standalone handoff checker repair)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor. Reviewer: Codex Prime. Date: 2026-10-29. Workshop at claim: e66248378657977d304cf4ed1b7ecbeb1209b27d (unchanged at return).

## Did
- **Pack and claim.** pack05.04: 14 of 14 snapshots match their pins, and live equals all 14. I recorded the Director's release and my claim.
- **Order.** Notes FIRST (06.04.md), then evidence/checker05.04/CONTRACT.md, then code.
- **HC01 reproduced exactly** on a copy of the real 05.03 package. With only `handoff.investigation.page` changed to `0799.wrong-investigation`:
  - held checker db921e1c… exit 0, `valid`, reporting the wrong page;
  - frozen producer verify exit 1, `mismatch`.
- **Repair** (labs/colab-support-pass02/handoff_check.py, db921e1c… to 7d62dde4…).
  - The expected digest is the only trust anchor.
  - The checker now derives from digest-bound bytes, by fixed v2 rules, the investigation, binding, exchange names and roles, the source-to-snapshot map, the support projection, ZIP membership, evaluator separation and the full preimage.
  - It recomputes the assembler digest independently under `pack-assembly-digest/1`; this matched the producer's recorded ef610184…. It also recomputes the package digest.
  - Every handoff field a consumer relies on must equal the derivation. Identity is output only under `trusted`, and only when the result is `valid`.
  - Safe reading: strict JSON (duplicate keys, non-finite numbers, types, limits, exact keys), every path validated, and links, junctions, hard links, unknown extras, duplicate ZIP entries and fabricated return or review files refused.
  - Copy needs a fresh destination and writes exclusively. A replay is a read-only refusal (`already-copied` or `occupied`). A failed copy stays `partial`, with no deletion and no resume. The source is re-checked after the copy.
  - Its bounded capability is stated in every output (`not_verified`): it does not re-render prose, compute section line ranges, check the assembler receipt's checker result, or check pins.
- **After repair.** HC01 gives exit 1, `mismatch`, with no identity. A three-way comparison on the real package found that the held checker also accepted a changed source_map role and an emptied not_created list. The repaired checker now matches the frozen producer verify on all 9 cases. The clean package checks `valid`, copies 16 files exactly, and a replay refuses read-only.
- **Tests.** The new tests/test_handoff_check.py has 31 tests and 0 skips; it passed on its first run and on the final run.
  - It covers:
    - HC01;
    - one tamper at a time across investigation, binding, binding hash, exchange, not_created, envelope roles and hashes, source_map, support projection, ZIP members, layout, digest domain, digest, the preimage (order, extra part, kind change, unsupported kind) and evaluator;
    - a handoff version change, extra or missing keys, and a wrong informational type;
    - byte tampers, including a consistent relabel of the request and binding;
    - a non-canonical binding;
    - missing, extra and fabricated return or review files;
    - a duplicate ZIP entry;
    - the manifest commit and the assembler request origin;
    - a wrong or malformed expected digest;
    - evaluator tampers;
    - strict JSON and limits, and unsafe paths;
    - a junction inside the package, a junction ancestor and a hard link;
    - an exact copy and read-only replay, an occupied or overlapping destination, an injected partial copy, and CLI exits.
  - Every bad case asserts no `trusted` output and no copy destination. For each handoff tamper, the frozen producer verify is also required to fail.
  - The accepted v2 suite (24 tests, unchanged) still passes.
  - Three in-process mutation probes were each caught.
  - Frozen hashes are asserted before and after.
- **Unchanged.** The frozen producer 2b720434…, v1 33bbe41c…, the four helpers, the v2 tests and examples, workflow, Grok-2 and shared contracts. Changed: only the checker, its new test file and the v2 README.

## Blocked
Nothing.

## Need
- Prime's review of the repaired checker.
- Smallest next action: Prime decides whether a workflow pass may rely on the standalone check, within its stated bounded capability, or keeps the pinned full producer verify, as the 05.03 review currently requires. I have not changed that instruction.
- The reserved capture list names only the evidence. Lab files are bound by hash in artifact-manifest.json and below.

## Limits and notes
- **Copy replay.** An identical replay is a read-only refusal (exit 2), not exit 0. That keeps the accepted v2 suite's "never overwrites" assertion; CONTRACT records it.
- **Not run.** v1's unchanged suite was not run, per the pack, and no model was called.
- **Races.** No sandbox is claimed against same-user races between check and use.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0510.colab-tools/06.04.md: 1e3aefc84cd81786cd26cc253bcf1753f29356e6313d362ee6b53fb75c4b0208, 8640
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/checker05.04/CONTRACT.md: a4ff9364aef4631b47e61edd46b96fed071503549a52c28c24dbde47a8dde863, 7202
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/checker05.04/verification.json: fea82db348ed8fee3c053c5ae55af3a8777690a883975c36a9091008260fb2a2, 121072
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/checker05.04/REAL-USE.md: d3856ca851e5c35429983fc31bd8d4e611f4f626cd7f8d2cca65eeb4c6aeffb4, 3314
- 00.kernel/00.00.10.work/0510.colab-tools/evidence/checker05.04/artifact-manifest.json: 15e925acaee6fb4c28df21e34ee48043d4786ffd109ab9e7518d47991d6ef549, 3073
- labs/colab-support-pass02/handoff_check.py (not captured): 7d62dde48165c5ac80f7f92a2a91f73a66b40c1e8dd2383f0269027038c6a268, 27722
- labs/colab-support-pass02/tests/test_handoff_check.py (not captured): 6e5a056f95f628b60fa301a125a4a10d3ee6eea67e6e15fd1709c50d26b7219d, 21579
- labs/colab-support-pass02/README.md (not captured): 36cb2f668212e93b3aaa9ff82f4267d94c8d04686ee90d83bb22cc4371dd8b88, 5885
