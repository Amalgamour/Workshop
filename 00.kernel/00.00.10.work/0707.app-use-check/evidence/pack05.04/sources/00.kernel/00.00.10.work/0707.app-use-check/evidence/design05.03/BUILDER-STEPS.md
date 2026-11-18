# BUILDER-STEPS — slice L1 (isolated loop successor)
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · for a Grok builder once Prime releases a pack; Claude writes no production code

1. **Verify the pack inputs** by compute. Record the pins of loop pass02 (8082750f…, 47189), cycle pass03 (496b4d72…, 76045), construct pass02 (b82413ff…, 36188) and construct pass04 (6d541d42…, 42582). Write the notes and contract first.
2. **Copy** `labs/review-loop-pass02/review_loop.py` → NEW `labs/review-loop-pass03/review_loop.py`. Do not edit pass02.
3. **Change, in pass03 only:**
   - a. `CONSTRUCT` path and pins → construct pass04.
   - b. `build_envelope`: emit /2 with `supplied_review_state` from `decision["judgment"]` (DELTA D1). `record` passes the decision.
   - c. Add `verify_committed` (D1, checks 1–6). Call it in `render_committed` before the existing write-token check and before `apply`. Map failures to `Refusal(code: …)`.
   - d. `prepare`: after the cycle read, run `construct.py inspect --fixture-root <root> --target <reg target> --binding <template task_binding_sha256>`; attach `target`.
   - e. `wrap`: add `mechanical` (D2 table), `supplied_next_action`, and `committed_check` where computed. Set `next` = `mechanical.text`. Keep `current.*` as is.
   - f. Update `pin_set` and the module docstring. Keep `reproduce` behaviour explicit.
4. **Write tests** for ACCEPTANCE L1–L18 under `labs/review-loop-pass03/tests/`, using copied fixtures, new run directories and an aggregate nonzero exit on any failure.
5. **Run only the new suite.** Preserve the first failures and skips. Do not run the v2 app test as `__main__`. Do not touch `app/`.
6. **Return** on the 0522 or N5NN page Prime names: pins before and after; the pass02 to pass03 diff; raw outputs. **Stop** for Prime before L2 (door, librarian, pilot data, 0525 records).

**Manual cost that stays for Prime after L1:**
- filling the judgment words, guided by the 05.02 operator guide;
- interpreting `render-blocked` and `rendered-marker-missing`, which have no automatic route by design.
