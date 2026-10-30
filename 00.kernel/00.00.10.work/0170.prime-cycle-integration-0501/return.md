# Submission — claude-0515-0501 (0515.prime-cycle 05.01)
who: claude-opus-5-5 (Anthropic), executor named Claude Builder · 2026-10-30 · branch workshop at 4d8bc1c7d6f0f960179deb87f1ebc81d18ab366a

## Did
- Read 0415.prime-cycle completely. Verified pack05.01: 25 of 25 snapshots match their pins, and live equals all 25.
- Wrote notes 06.01 first, then CONTRACT.md, then the code.
- **Built `labs/prime-cycle-pass01/prime_cycle.py`** (standard library only). Commands:
  - `read`: the view, plus templates with the mechanical fields pre-filled;
  - `record`: one work-local review, written as record.json, then REVIEW.md, then COMMITTED.json last;
  - `inspect`: the review phases and the recovery rule;
  - `packet`: the accepted review packet.
- **Reused modules**, pinned and hash-checked before every launch: batch_observe (with return_inspect and return_capture), prime_review (report and check-next) and review_packet. Not reused: prime_brief, state_projection and desk_state; CONTRACT §9 gives the reasons. No existing module was changed.
- **Pass and goal are kept separate.** A review states its disposition, its pass terminal and its goal terminal separately. Goal completion binds to the goal id and the statement's sha256, needs evidence and prime_review complete-as-supplied, and is never inherited by a new goal.
- **Tests:** 14, covering the batch's cases 1-9 plus a full read-fill-record-read transcript.
  - The first run failed 2 tests (test_05 check order, test_07 expectation). Both failures are kept; both were fixed.
  - Then OK in dev mode, default mode, a disposable copy, and on the final bytes.
  - Five targeted mutations were all caught.
- **Demo:** four works (new, held, finished with goal open, completed goal as a successor).
- **Read-only real preview** of 05.20 and member 0169 at 4d8bc1c:
  - result: awaiting-review, with legacy-review-unmapped attention;
  - nothing was written to the repository.
- **PRIME-USE.md**, for current Prime.
- **REAL-USE.md:** the facts that need Prime's input, the legacy mapping limit and the field counts (14, 18 and 15).
- **COLD-PRIME-COLAB.md** (the candidate entry), and separately `labs/prime-cycle-pass01/colab/` (the builder, the evaluator and a self-test, marked Prime/Director only and kept out of the candidate's reading order). The self-test passed.
- The guide, the rendered REVIEW.md (both accept and complete) and the return were read back in full.

## Blocked
Nothing blocks this batch.

## Need
**Prime:**
- Review the build.
- Decide the live review location; the proposal is `<lane>/evidence/prime-cycle-reviews/<pass>/`.
- Supply the goal statement, the agreement and the judgment for a first real use.

**Director:** any later Colab launch or N7NN allocation is a separate release.

**Smallest next actual-use action for Prime:** register 0508.return-capture/05.20 with member 0169 (PRIME-USE §1). Run `read --templates`, fill your judgment adopting your 05.20 prose review, `record`, and read again. Then confirm that the view shows `reviewed` with your disposition, pass terminal and goal terminal.

## Limits
- Synthetic checks: not a model benchmark, not a live dispatcher, not a fresh-Prime boot.
- A label is not authentication; custody is not acceptance.
- There is no transaction across files, and no OS sandbox. The local user is trusted.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0515.prime-cycle/06.01.md` 76fb86e7984fd9204584bf30d4e25cd73a6b0e274e906ffa4da3a99a93ee5092
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/CONTRACT.md` e296e3bb5ba3254ff388d33b46cfc3e9268c254f3cb757da7db200b0ecebf764
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/verification.json` 5d78c79a1452198e2ddefbd7394a247836e6b5a702958a4d5348d8ca90c1d97f
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/artifact-manifest.json` e99ffbebeaf5b1e4294db0f9ae8827d6c9cc1772a4bf0a30b69e8702bbd15581
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/REAL-USE.md` 3efa27817ba2c4b5b1ecaa9c64630255dfea4d2ad7902704958596923994253b
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/PRIME-USE.md` d1f19180de0e742ca63368bf3b0d09561aaff77dc22ffa706ba33adac59a8501
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/COLD-PRIME-COLAB.md` 4a72884a65ee6948f83510f72cbdca5398f4ceb3e1cf544481a70b67d5419304
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.01/sample-cycle.json` 442d23decfbaddde69977464f9827e3bbba7e21d30fd2c7ca03b78a67c91cc68

The artifact manifest binds the code, tests, fixtures, the Colab materials and the evidence (16 files).
