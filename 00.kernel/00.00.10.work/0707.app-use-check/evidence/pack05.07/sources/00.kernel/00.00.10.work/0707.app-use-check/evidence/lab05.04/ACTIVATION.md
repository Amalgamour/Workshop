# ACTIVATION checklist — after Grok-1 returns 0522/05.08 and Prime reviews it
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

**The harness does not run the candidate until all of these are true:**

1. **A later named Director invocation** releases a real candidate run. This assignment does not.
2. **Prime supplies the candidate pin** from the reviewed return: `labs/review-loop-pass03/review_loop.py` sha256 = `<PRIME SUPPLIES>`, bytes = `<PRIME SUPPLIES>`.
3. **Prime confirms or replaces the dependency pins** in `candidate.config.json`. They are the reviewed values now: construct pass04 6d541d42…/42582, construct pass02 b82413ff…/36188, cycle pass03 496b4d72…/76045, prime_review p01 805995a1…/58324 and p02 80836a13…/58560, return_lines 863968c5…/100897, return_placement db96f702…/66097, return_inspect 947915fe…/11402, return_capture 8f3da5c6…/45767. Add any new dependency the candidate's reviewed `pin_set` names.
4. **Prime supplies `field_map` entries** wherever the candidate's reviewed contract names a matrix field differently: `target.state`, `mechanical.{state,route,text}`, `supplied_next_action.text`, `committed_check.supplied_state`, `record.result`, `render.result`, `render.apply_called`, `next`.
5. **Prime confirms R02 wording.** Cases A11, A18, A22 and A23 use wording heuristics (`retained`, `not established`, `not recorded`, and no "committed judgment" claim). Adjust the patterns in a NEW case-file version if the reviewed candidate uses other exact phrases. Never loosen them to pass.
6. **Inspect A24 by hand:** the candidate `pin_set` names construct pass04 and refuses on a mismatch.
7. **Write the filled config to a NEW file.** Keep `candidate.config.json` with nulls. Then run `harness.py preflight`, then `harness.py run --matrix real`, in a new evidence directory. Do not edit earlier runs.
8. **The aggregate is execution status.** INCOMPLETE is the best possible result while A24 is MANUAL. Prime judges the result; a PASS here is not acceptance.
