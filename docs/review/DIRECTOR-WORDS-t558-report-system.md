# Director words: t558 report-system plan (2026-11-23)

Claude, lead for page 90.50.10.0422 (report-system), raised R1-R7 in its plan (labs/0422-plan/README.md, returns b5cb8a47). Matthew relayed it at 2:48 PM EST (t558u). Prima answered R1, R2, R5 and C2-C6 in docs/review/ANSWERS-0422-PLAN.md (prima/build 3c6d509) and raised two questions, M1 and M2, each with a default. Matthew answered both at 2:53 PM EST (t558s2225). His choices, as relayed by Prima, are below. Readings follow. Nothing was packed.

## t558s2225  -  M1: a run folder with no report config (2:53 PM EST)

Asked: before every worker is set up, what should wf do when a run folder has no `.wf/config.json`?

> warn and carry on, and block later

Reading: this is the default. In 0422.05.03, a missing config does not refuse. The command runs as it does at a823ee28, writes no report entry, queues nothing, and ends with lines naming the file, docs/plan/REPORTS.md (push the stopgap report) and `wf setup`. A config that is present but invalid still refuses. No flag is added. "Block later": a later small pass (0422.05.06 or a later 04NN page) brings the refusal back, packed only once every active worker has a setup report on its N6 page. The pinned wf may move to a build with 05.03 after 05.03's trial passes. This changes lab 0705's "no opt-out" refusal (LESSONS.md lesson 9) for the rollout only.

## t558s2225  -  M2: an offline return (FAILURES.md section 2(a)) (2:53 PM EST)

Asked: if the network is down at return time, should a later wf pass record the return locally and send it later?

> not now, use the manual return

Reading: this is the default. wf keeps today's rule: an offline `return --push` fails at the fetch and records nothing. The builder follows docs/plan/MANUAL-RETURN.md (triggers 1 and 7). A return counts when it lands on `returns` (t557s2212 Q3). C6 in the 0422 plan stands. An offline `check` still records its entry and report and queues the push (C6). Recording an offline return locally is not queued.
