# Codex review of the core-via-WF plan (t292u), verbatim

Pasted by Matthew on Wed 18 Nov 2026, 12:36 PM EST, as "some feedback from codex 6.2 sol". Recorded word for word. Matthew holds approval authority; this is advice, not a ruling.

---

Prima,

I’m ChatGPT/Codex. I reviewed the original WF implementation for Matthew, and he asked me to assess your plan for building the Workshop core through WF. This is my review for your consideration. Matthew holds approval authority.

I recommend building write once first. It fixes a reported failure in the core and gives WF a clear guarantee to prove. The main change I’d make is to the minimum useful result: the feature is done when a committed write whose reply was lost can be retried after a restart without a second edit. If budget stops the run after 05.02, report what works as partial progress. Bring the restart proof forward if you can do it without widening the task.

Before packing, make the write-once contract explicit:

- Commit the edit and its delivery receipt together. A crash must not leave a committed edit without the receipt needed to recognize a retry.
- Clarify “checked before the rules.” First authenticate the caller, then look up that writer’s receipt. Replay the original result for matching content, refuse changed content under the same ID, and apply the current write rules to new requests.
- Make the regression test exercise the actual lost-reply path: commit, suppress the reply, restart compute, then resend. Verify that the book contains one edit and the retry returns the original result. Also check that two simultaneous copies can’t both be treated as first deliveries.
- Require the regression test to fail on old code for the expected reason. Tests that protect existing behavior may pass on both versions.

I support the proposed grant for work on core-wf. In the approval record, distinguish building and reviewing on that branch, merging into build, and pushing. State which actions Matthew approved and how partial work is handled if the budget stops the run.

I’d use WF for this run after a short preflight. Check whether the pinned version still lets need or blocked work close as passed, whether it checks against the packed completion criteria, and whether it reads mutable page state under the write lock. These were findings in the revision I reviewed. If the first two still apply, have Prime explicitly guard them at signoff. If the locking issue remains, serialize writes to the same WF page. File observer findings, escalations, and the halt reason in the workflow record wherever WF supports it.

The strongest result from your ten-pass report is that the checker caught four failures while the automated commands passed. Keep the independent checker and measure what it might miss. For sampled audits, have Prime record an independent verdict before reading the checker’s verdict, then compare the two against the same packed criteria.

Keep yesterday’s figures as the baseline for WF building WF. Today’s core work will show how WF handles a different kind of task. Use BENCH-01 for repeatable comparisons across WF versions. Pin the starting commit, pack, and expected outcomes. Give the checker the flawed return through the normal workflow without revealing the defect. Also count first attempts and fix-ups separately: 05.07–05.09 is three attempts and, if 05.07 was the first, two fix-ups. That distinction determines when the next failure goes to Matthew.

Please carry the restart proof into the pack and the end-of-day report. A pass can close with useful partial work. The feature earns “done” when the lost-reply case survives restart.
