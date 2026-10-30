# Submission — claude-0515-0503 (0515.prime-cycle 05.03)
who: claude-opus-5-5 (Anthropic), executor named Claude Builder · 2026-10-30 · branch workshop at b876c7a9e8a27df58c0a5a0815a53f653d929332

## Did
- Verified pack05.03: 19 of 19 snapshots match their pins, and live equals all 19. Read 0703 06.03.review C-03/C-04, REPORT §Repair work, and Codex's 05.01 return.
- Wrote 06.03 first, then CONTRACT.md (a delta over 05.01 and 05.02), then the code.
- **Reproduced first,** on the unchanged 05.02 code, on disposable fixtures:
  - with `clerk_adapter.py` missing, both a captured work and a page with no return read `no-return` with only "reader exit 2", because the reader's stderr was dropped;
  - a completed review whose observation then fails read `review-stale` ("binds a different page, receipt…");
  - record refused with no cause.
- **Failed observation is now its own state.**
  - Each work has `observation` (`observed`, or `failed` with part `source` or `custody`), a kind (`reader-exit-N`, `reader-report-invalid`, `reader-output-over-bound`, `no-source-identity`, `page-over-bound`, `member-observation-failed`), and a bounded diagnostic: the reader exit, stdout and stderr sha and bytes, an excerpt of at most 2000 characters, and one text line of at most 240 characters with control characters escaped.
  - With `--journal-root`, the full child stdout and stderr are kept exclusive-create in the operation's journal folder, and the view and refusal give their path.
- **`no-return` is reserved for observed absence.** Custody is `present`, `absent`, `unresolved` or `unknown`. The new `custody-unresolved` covers incomplete or refused custody, an ambiguous primary, and a registered member the page does not name.
- **Under a failed observation** a head review's declarations are historical (reason `observation-failed`), never stale or current. The counts stay at zero, holds still block, and the same review is current again once observation works.
- **Invalid bindings never become reviews.** record refuses a template made from a failed read ("no observed source identity"), and refuses on a failed fresh observation, with the cause and the retained path. Freshness, fingerprint and direction rules are unchanged.
- **Packet coverage is exposed:**
  - the sources requested and gathered, with status, bytes and sha;
  - the artifact checks requested;
  - whether the page was included;
  - the member's captured payloads not gathered.

  It appears in the text output and in the journal `result.coverage`. The request, the default gathering and the packet folder are unchanged.
- **Schemas:** the view is now `prime-cycle-view/3`. Decision `/2`, record `/2`, registration `/1`, the journal schemas and all dependency pins are unchanged.
- **Tests:** a new test_observation.py with 6 tests (missing adapter with retained diagnostics; invalid, over-bound, no-identity and noisy reader results with bounds; observed absent, present and unresolved custody; failed custody observation; a completed review and a hold under failure; packet coverage).
  - The existing test_prime_cycle (14) and test_binding_log (12) pass unchanged.
  - **Final bytes:** 32 tests OK in dev and default mode, 0 skips, no warnings.
  - **First runs failed** 2 of 6 and then 1 of 6, all test errors (kept, described in verification.json).
  - 7 targeted mutations were all caught. The Colab self-test and the demo are unchanged.
- **Docs:** README, PRIME-USE.md (a delta guide), and sample-cycle.json (a journalled cycle with the missing-adapter failure, retained stderr, refusal, record, coverage and the day view, plus the before and after reproductions). The views, the refusal and the guide were read back.

## Blocked
Nothing blocks this batch.

## Need
- **Prime:** review, then accept and pin the new prime_cycle.py identity before 0516 packages any bundle. It is not substituted into the first replay.
- **Prime and 0516:** decide any default packet change. Coverage is now visible; gathering is unchanged.

## Limits (tests, skips, what is not proven)
- **Skips:** no test skips. Not exercised: a real symlink or junction journal root (needs privilege here), and reserved-only custody (mapped to `absent` by contract; the fixture helper cannot reserve without capturing).
- **The custody-part diagnostic** has only the inspector's exit and attention codes, because the reader passes no inspector stderr. More detail would need a reader change, which is out of scope.
- **Synthetic fixtures only:** no model run, no performance claim, no OS sandbox, no same-user race safety.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0515.prime-cycle/06.03.md` cf45fd84513077de3359b043f68d6408160e64e6584fb8f363957798c7e64aec
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.03/CONTRACT.md` df71f915e3c4726d0b0dff9202235d5bad859ad7ffb140d5872d66e0c3b0cccf
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.03/verification.json` 9a35ca2898ccec8c97f77d65220192448a3ea4350ba29095a9f0dd63e5a5f3f2
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.03/artifact-manifest.json` 42efdc9f2c54629136832c98b9a0a4a94f8179b62bcc57ef378d3233671133a9
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.03/PRIME-USE.md` 7e62147456826712f5e9ba29b6c990dacc2acc0cd17feaa63f7de856110a977e
- `00.kernel/00.00.10.work/0515.prime-cycle/evidence/build05.03/sample-cycle.json` 63f0dc26e53eca4db45ebd207045a71e7116eb5c0dcad0a70ec336bc7f522f2a

The artifact manifest binds changed and new code, tests and docs (prime_cycle.py 19ede9c212530759…, README, test_observation.py) and the evidence, with the unchanged tests, fixture and demo for context.
