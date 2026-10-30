# Submission — claude-0515-0502 (0515.prime-cycle 05.02)
who: claude-opus-5-5 (Anthropic), executor named Claude Builder · 2026-10-30 · branch workshop at d19241074e8db09723ddf44e0900c839a62bc526

## Did
- Verified pack05.02: 11 of 11 snapshots match their pins, and live equals all 11. Read Prime's 05.01 review, its probes and 0415/06.03. Wrote 06.02 first, then CONTRACT.md (a delta over 05.01), then the code.
- **Reproduced both findings** on the unchanged 05.01 code, then fixed them:
  - **PC-01:** a stale review showed finished and completed as current;
  - **PC-02:** an old decision recorded with exit 0 under a changed agreement.scope.
- **PC-01 fix.** A review's declarations are current only while its page, custody and direction binding hold, its record is `/2`, and no altered review is left unrecovered. Otherwise:
  - the terminals read `unknown`, and the old values move to `historical`, with the reason;
  - the next action becomes historical;
  - the summary and the day view's "current" count nothing as finished or completed.

  Holds keep blocking. Goal-change behaviour is unchanged. Nothing is erased. A fresh successor restores current status.
- **PC-02 fix.** `prime-cycle-decision/2` binds the direction: the agreement, field by field, plus the review location and book. record refuses a changed direction and names the field (`direction changed since read: agreement.scope`). It also refuses a `/1` template. Identical replay and successor lineage are kept.
  - **Excluded from the binding, by contract:** output_root, bounds, other works, the registration bytes, and clock-bearing reader fields.
  - **Legacy:** `/1` records are read but never current.
- **Journal.** `--journal-root` on read, record, inspect and packet writes `<root>/<date>/<op_id>/` with start, input snapshots, stdout and end. All files are exclusive-create, and machine facts are kept apart from supplied caller and note text.
  - **Failure rules:** start fails → exit 4, nothing ran; end fails → exit 5, and stderr names the committed or partial review; unexpected error → 6; an interrupt leaves the operation incomplete.
  - **`day` view:** attempts, refusals, partials and incomplete operations; unique reviews re-verified now; declared counts, once per work pass and goal; current status from a fresh read; no time totals and no productivity.
- **Tests:** 14 existing and 12 new, all OK on the final bytes in dev and default mode.
  - The first new-test run failed 1 (test_23, a test error). It is kept and was fixed.
  - 10 targeted mutations were all caught.
  - The Colab self-test, the demo and a bounded journalled sample cycle passed. The sample's day view was read in a new process.
- **Real preview:** repeated read-only at d192410 with the journal in external temp. The result is awaiting-review with legacy-review-unmapped. Nothing was written to the repository, and 0169 was not adopted.
- **Docs:**
  - PRIME-USE.md, which replaces the 05.01 guide;
  - REAL-USE.md;
  - DAILY-LOG.md;
  - COLD-PRIME-COLAB.md (05.02 interfaces), plus the updated Colab builder, evaluator and self-test.

  build05.01, 06.01 and capture 0170 are unchanged.
- The journal view, the review views (current and historical), the rendered completion review and the guide were read back in full.

## Blocked
Nothing blocks this batch.

## Need
**Prime:**
- Review PC-01, PC-02 and the journal.
- Confirm the journal root outside the repository; the proposal is `D:/prime-cycle-out/journal`.
- Supply the goal, the agreement and your judgment for a first real use.

**Director:** a Colab launch or N7NN allocation needs its own release. AR-01 stays held.

**Smallest next actual-use action for Prime:** follow PRIME-USE §1-4 for 0508.return-capture/05.20 with member 0169, with `--journal-root` on every command. That is: one logged `read --templates`, fill your judgment adopting your 05.20 prose review, one logged `record`, one logged `read`, then `day --registration`. Confirm the view shows `reviewed` with current terminals, and that the day view shows one unique review.

## Limits
- Synthetic checks: not a model benchmark, not a live dispatcher, not a fresh-Prime boot.
- Labels are not authentication; custody is not acceptance.
- The journal covers this tool only. There is no transaction across files, no OS sandbox, and no same-user race safety. The link check is not exercised by a test on this host.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0515.prime-cycle/06.02.md` e5605fef33d829efa290e121822e980922e5cde393822b9258b1edfbbce5d720
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/CONTRACT.md` aaecad52bd6d3a2049e5be85d928cc206058a7c7fa83ef206814891c78827b98
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/verification.json` 33a05ed82646cd8c131f7a8c4e747332b3aba198cbfbea8cca545eb57fefabd8
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/artifact-manifest.json` e8fddbe24d5c4c3474dfa4a6f9c7d3d1f0e5f0e56cc36fb79191f3c6cf37fd18
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/PRIME-USE.md` e81cfcdf02226d11ddae7ac1afb82df68626e21dc709e0dde311e4769397f20d
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/REAL-USE.md` 6eb37596ef845e536f849c8796c1822781796315145b4d955fa606f823c9134e
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/DAILY-LOG.md` 183930753eea40e59a2a04874211e4ce0632a65e8e970a3dab50b556c37e0935
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.02/sample-cycle.json` c17b7bad1eb760aabcb51b7cb51d83470cbf8dab0f41ca0c58790762016216e0

The artifact manifest binds the code, tests, fixture, demo, the Colab materials, notes and evidence (18 files), including COLD-PRIME-COLAB.md.
