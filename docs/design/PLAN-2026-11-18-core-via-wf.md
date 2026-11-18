# Plan for today: build a piece of the core with WF, and measure WF

state: plan for Matthew to review. Not a ruling. Nothing starts until he says yes.
made: Wed 18 Nov 2026, 12:30 PM EST, by Prima.
asked for (t284u): "design a project lead task, to assess our project goals ... build the core of the workshop using the WF system we made. While doing it be testing and reviewing it's effectiveness. A benchmark should be designed for use."
sources: build repo at f3ed48d; WF kit at 8eb1fdb; the dogfood page log `wf-run/pages/90.10.00.0001/log.jsonl` (85 entries).
labels: **LOG** = counted from the log or git. **EST** = an estimate. Nothing else is a number.

---

## 1. Where we are now

**The core has a working first version.** It is in Rust. One program (the compute) owns the books and takes every change through one gate (`/propose`). It checks the rules, the writer's token, plain characters (R4) and approvals (R2). It keeps each book as one append-only log file, and it survives a crash in the middle of a write (crates/trial-compute/tests/crash.rs). There is a reader app and a `.seq` page file.

**The core still has known holes.** The design spec lists them (docs/design/CORE-AND-TOOLS-SPEC.md, Part D). The worst is marked "fails today": if the reply to a write is lost, the tool sends it again and the change is written twice (B6; crates/compute/src/lib.rs:66). There is also no page history view (face 09, R28), no review tied to a version, and no lock against other programs writing the book files. The order to build these is open question K8. Its proposed order is: close the direct-write door, then the "first proof" (Part F), then crash tests, then the move to small files.

**WF works, and was built with itself.** WF is our workflow tool (the `wf` kit). It ran 10 passes on its own page yesterday (Tue 17 Nov). 6 passed and 4 failed, and every fail was fixed in the next pass (LOG). It has 82 tests (LOG: 22 unit + 60 end-to-end at 05.10). Three gaps showed up while using it:
- It has no "halted" state. After we stopped, `wf status` still says "next: draft".
- Merging and rebuilding the pinned tool are done by hand (6 times yesterday).
- Observer findings and questions to Matthew happened in chat, so they are not in the page log.

## 2. The goal for today

**Main pick: "write once" (the side label is delivery ids).** It means a change that is sent twice is only written once.
- Each write may carry an id.
- The same id with the same content gives back the first answer and writes nothing new.
- The same id with different content is refused, and the first content's fingerprint is handed back.
- An id belongs to one writer's name.
- Ids still work after the compute restarts, because they are rebuilt from the book log.

**Why this piece comes next:**
1. **You already ruled it.** R37 item 2 says "a delivery id can't change its content" (DIRECTOR-RULINGS.md:196). The detailed shape is proposal K4 (CORE-AND-TOOLS-SPEC.md:949). So the authority is there (axiom 1).
2. **It fixes the one hole marked "fails today".** A lost reply writes a change twice.
3. **The first proof needs it.** Part F (one edit, one review, one restart) lists delivery ids as needed first, and its test 9 is this exact case.
4. **It is small and easy to test.** It touches the gate (crates/compute) and the request shape (crates/seqaddr-core/src/validate.rs:16-43). The restart tests already exist to copy.
5. **The bigger first step can't be done today.** K8 step 1 (closing the direct-write door) needs an OS account choice on the machine, and that is yours to make.

**Alternative: the face 09 history view.** This shows a page's history from today's log, without changing storage (R28; S5 proposes "a view"; K8 step 2). It is lower risk because it only reads. But it fixes no bug, and the "view or stored" choice (S5) is still open.

## 3. How we use WF to build it

**Setup.** This is small and adds no WF code.
- A work folder: `git worktree add ../wf-run/core -b core-wf build`. It is about 22 MB (LOG: tracked files). The page's `repo:` is `core`.
- Builders and Tester build into the existing `repo/target` folder, one at a time. This adds no new 26 GB build folder, and the disk is 89% full. The pinned `wf` tool stays separate in `wf-bin`, so no builder can overwrite the judge.
- Page id: **90.20.00.0001**, title "core: write once". Page ids are temporary labels (ruling Q-SA). Passes run 01-98 (R9).
- Start the page with your grant (question 2), recorded as `--as matthew --grant-ref t284u`.
- Use the WF commands we already have, so everything lands in the log:
  - the Observer files findings with `wf observe --record`;
  - any question for you goes through `wf elevate --to person`.

**Roles.**
- **Prima** is Prime. She writes the 06 note, drafts, packs and signs off.
- **Executor builders** (b11, b12, ...) do one pass each, on `pass/90.20.00.0001.05.NN`.
- **Tester** is the checker and runs the pinned `wf check`. Tester never builds.
- **Observer** watches Prima for drift from face 01 and 04, for loops and for stalls. It runs `wf observe` after each close.
- **Designer** is not used unless a real design question comes up. The refusal shape in pass 05.02 is the only likely one.

**Face 01 (the MVP for the agent).**
"Goal: a write sent twice is booked once.
Done when: the delivery-id tests pass, and each fails on f3ed48d."

**Passes.** Each pass has a "done when" list, and each new test must fail on the old code.

| Pass | Work | Done when |
|---|---|---|
| 05.01 | `/propose` takes an optional delivery id, stored on the book entry. The same id, writer and content returns the first answer. | A test sends one write twice with one id: the book grows by one change, and both replies match. |
| 05.02 | The same id with different content is refused, and the first fingerprint is handed back. Ids are kept per writer name. The status code and field names are draft choices, marked `7` in BUILD-LOG. | A test shows the refusal and the fingerprint. A test shows two writers using the same id do not clash. |
| 05.03 | The id index is rebuilt from the book log at start-up. The id is checked before the rules (K4). | A test writes, restarts, resends: no second change. A lost-reply test (Part F test 9): the change is written, the reply is dropped, the retry gets the first answer. |
| 05.04 | Records. Add a CONTRACT.md addendum and update seqaddr-core API.md. Add BUILD-LOG lines with each draft choice marked `7`. Tester does a hostile pass (axiom 9). | The docs match the code. The hostile pass is filed in the check. No open `need` or `blocked`. |

**Limits.**
- A goal gets at most 2 fix-up passes. A third fail goes to you through `wf elevate`.
- After 05.04 passes, the page halts and I report to you.
- Nothing is pushed without your OK.

## 4. The benchmark: how well does WF work?

Every measure is read from the page log and git. "Fresh goal" means a pass that does not follow a failed pass.

| # | Measure | How to compute it | Baseline (05.01-05.10) |
|---|---|---|---|
| 1 | First-try pass rate | fresh goals that passed / fresh goals | 3 of 6 (50%) LOG |
| 2 | Passes per goal | all passes / fresh goals; also the longest fix-up chain | 10 / 6 = 1.7; longest 3 (05.07-05.09) LOG |
| 3 | Cards carried | cards marked `carried` at signoff / all cards | 5 of 48 (10%); none carried twice LOG |
| 4 | Who caught the fails | fails where the `checks` commands failed, versus fails found by the checker's own reading | 0 by commands, 4 by the checker; cargo test passed in all 10 LOG |
| 5 | Checker misses | Prima audits 1 pass in 3 in full and writes "(audit) agree/disagree" in the signoff note | no audits were recorded; baseline not measured |
| 6 | Prime hand steps | hand merges + pin rebuilds; Prime judgement calls in notes | 6 merges and 6 pin rebuilds (5 in 06 notes, 1 after the last pass); 3 judgement calls (05.01, 05.05, 05.09 halt plan) LOG |
| 7 | Questions to you | `elevate --to person` entries; plus questions asked outside wf | 0 in the log; 1 outside (Q-SA, recorded in 06 note entry 38) LOG |
| 8 | Observer findings | `observe` entries; loops = the same card carried twice | 0 filed with wf; 1 written into a 06 note (halt advice, entry 70); 0 loops LOG |
| 9 | Time per pass | pack to close, in minutes, median (also builder: claim to return; checker: return to check) | median 10.8 (5.6 to 13.1); builder 6.2; checker 2.7 LOG |
| 10 | Usage per pass | weekly usage % moved / passes, and / passed passes | about 0.9 per pass, 1.6 per passed pass EST (see 5) |
| 11 | Fresh-model readiness | a new model gets only `wf status`, face 01 and AGENTS.md, and answers 5 fixed questions: goal? next pass? who acts next? what is open? is the page halted? Score out of 5 | not measured. The "halted?" answer is known to be wrong today (status says "next: draft") |

**What the baseline already tells us.** Every fail was caught by the checker reading the work, not by the tests. So the checker is the part that matters most, and measure 5 (the audit) is the one we lack.

**How to compute it.** The appendix has a short script, used to make the baseline above. Later this can become a `wf bench <page>` command in Rust.

**A fixed reference task (BENCH-01).** This is a test we can run again on every new WF version.
- It uses the car-steering example repo in the kit (examples/car-steering.sh), so it needs no outside code.
- **Part a, a builder pass.** The plan file is fixed: "clamp the angle at -30 and +30, and test both edges".
- **Part b, a checker trap.** A ready-made bad return clamps only +30. Its check commands pass, but its "done when" fails. The checker must fail it.
- Record: passed first try (yes/no), trap caught (yes/no), minutes, log entries and usage points.
- Cost is about 1 point (EST). Build it today only if usage is under 60% after the core passes. Otherwise build it next week.

## 5. The budget

- **Cost per pass (EST).** Usage went from about 39.7% to 49% on the dogfood day. That is about 9.3 points for 10 passes, or about 0.9 points a pass. It also paid for the Codex review triage, so it is an upper guess for that kind of pass. Core passes build a bigger crate, so I plan on about 1 to 1.5 points a pass.
- **Today's plan (EST).** Setup 0.5, plus 4 passes and up to 2 fix-ups (6 to 9), plus BENCH-01 (1), plus reports (1). That is about 8.5 to 11.5 points, ending near 59-62%.
- **Stop lines:**
  - **58%:** no second fix-up on any goal.
  - **60%:** no new pass is packed, and BENCH-01 waits.
  - **62%:** finish only the pass in flight, halt the page, write the report.
  - **66%:** hard stop. All bots wind down. 68% is never reached.
- **If we run low,** we stop at the last passed pass. The smallest useful result is 05.01 + 05.02 passed (write once, in one run). The restart part waits for next week.
- Usage resets Thu 19 Nov at 10:42 AM EST.

## 6. Risks and your decisions

**Risks.**
- **Disk is 89% full.** Mitigation: one small worktree and the shared build folder. Nothing is deleted without your yes.
- **The checker is the one safety net (measure 4).** Mitigation: Prima's 1-in-3 audit.
- **Draft choices could harden into rules.** Each one is marked `7` in BUILD-LOG until you rule on K4.

**Q1. Is "write once" the right first core piece?**
- **Proposed answer:** Yes. The face 09 view is the alternative.
- **Why:** You already ruled it (R37 item 2). It fixes the one "fails today" hole. It is small. The first proof needs it.
- **Axioms check:** 1 pass (your ruling). 6 pass (a retry never adds a false step to the history). 7 pass (field names and the refusal code stay marked `7`). 9 pass (each pass faces Tester).

**Q2. May the page's grant be `crates/compute/`, `crates/seqaddr-core/`, `docs/CONTRACT.md` and `docs/BUILD-LOG.md`?**
- Work happens on a new branch `core-wf` (folder `wf-run/core`), merged into `build` by Prima. Nothing is pushed without your OK.
- **Proposed answer:** Yes.
- **Why:** WF refuses any change outside the grant, and only you can grant. This is the smallest grant the four passes need.
- **Axioms check:** 1 pass (granted, not claimed). 5 pass (a clear frame). 2 pass (no new folders).

**Q3. Do we fix WF's gaps first, or just use it and record them?**
- The gaps are: no halted state, hand merges and pin rebuilds, and findings that happen outside the log.
- **Proposed answer:** Use it as it is today. Record each gap as benchmark data (measures 6 to 8). Fix them next week as one WF pass.
- **Why:** None of them blocks the run. It keeps today's points for the core. It also matches your words: "We should get it setup. But for now. YOu can use it with the bots today."
- **Axioms check:** 5 pass (stays in frame). 7 pass (the gaps are recorded, not quietly filled). 9 pass (WF itself is on trial today).

## 7. End-of-day report (the format)

```
CORE: write once - page 90.20.00.0001 - halted at 05.NN
Done:      what now works, in one line each
Not done:  what waits, and why
Benchmark: the measure table, today against the baseline
WF gaps:   new friction found (one line each)
Usage:     start % -> end %, points per passed pass
For you:   questions (four-part form), push OK needed (y/n)
```

---

## Appendix: how the baseline was computed

Run from `wf-run/pages/90.10.00.0001` (read-only):

```python
import json, statistics as st
L=[json.loads(l) for l in open('log.jsonl')]
so=[e['data'] for e in L if e['kind']=='signoff']
fresh=[d for i,d in enumerate(so) if i==0 or so[i-1]['outcome']=='passed']
print('first-try', sum(d['outcome']=='passed' for d in fresh), '/', len(fresh))
cards=[v for d in so for v in d['cards'].values()]
print('carried', cards.count('carried'), '/', len(cards))
ck=[e['data'] for e in L if e['kind']=='check']
print('fails', sum(c['verdict']=='fail' for c in ck), 'commands failed', sum(not all(r['ok'] for r in c['results']) for c in ck))
print('elevate', sum(e['kind']=='elevate' for e in L), 'observe', sum(e['kind']=='observe' for e in L))
t={}
for e in L:
    p=e['data'].get('pass') or (int(e['data']['branch'][-2:]) if e['kind']=='pack' else None)
    if p: t.setdefault(p,{})[e['kind']]=e['time_s']
print('median pack->close min', st.median((v['close']-v['pack'])/60 for v in t.values()))
```
