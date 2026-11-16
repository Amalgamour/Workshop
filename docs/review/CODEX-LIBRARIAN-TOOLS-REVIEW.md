# How Codex Prime built, used, and tested Librarian's tools

Advisory review by Prima (Grok Bot), for Matthew (Director). Not a ruling.
Asked in t202u. Steering in t203u: "All tools should be pushed to codex's librarian branch."
Written 2026-11-16, 12:30 to 12:55 PM EST. Every rerun was done on this date, between 12:31 and 12:46 PM EST.

Source repo: `Amalgamour/Librarian`. It was cloned read only into `/workspace/librarian-review/repo`.
Each pin got its own detached worktree. Every rerun used a throwaway copy made with `git archive <pin>`.
Nothing was pushed to the Librarian repo, and nothing in it was edited.

Short commit names used below:

| Short | Full SHA | Commit time (EST) | Used for |
|---|---|---|---|
| 960d20c | 960d20c5290656095df8457b1740d2d5e586b111 | 2026-10-31 1:15 PM | clerk lab, published app (`origin/workshop` head) |
| 7e60567 | 7e60567b242aeccf992fbf54d7ceb95a12863c89 | 2026-10-30 1:42 PM | prime-cycle first actual use |
| 627c424 | 627c424da9216504dac93eeb86869f1291a4cdf0 | 2026-10-30 3:22 PM | prime-cycle tool, tests, review 05.03 |
| 19fc336 | 19fc3369ae1862c25689b16bc6b02a2cf507e4b9 | 2026-10-30 2:55 PM | manual vs assisted replay |
| bdcc894 | bdcc894b6cd38b48bd2e96684034c6999412049e | 2026-11-01 12:19 PM | desk-core review (`origin/prime/grok-core-review-pass03` head) |
| dd4cd00 | dd4cd00a7c4e75b66e3a0716d564a19e5beca59f | (reviewed commit) | desk-core source that Codex reviewed |
| d5bc892 | d5bc89286fc4d31a1335bec56f16f2bc04dd538b | 2026-11-06 11:54 AM | Cursor Brand Clerk (`origin/cursor/brand-clerk-v0-43b3` head) |

A note on names. In git, every author on these pins except d5bc892 is "Mathias", which is Matthew's own account.
So git alone cannot say which model wrote the code. Below, who built and who ran each piece comes from the records inside the repo, and each one is cited.

---

## Did / Blocked / Need

**Did**
- Read all five pinned sources and the published app at 960d20c.
- Reran five checks in throwaway copies. Each one answers a named question (see "Reruns").
  - Clerk lab: reproduced. 20 tests pass, 8 processes, 14 events, same route.
  - Prime cycle: 32 of 32 tests pass. That needs the whole repo and a Python path that is not a symlink.
  - Desk core: reproduced the CC-07 hidden pending revision on Linux. The 22-test suite passes 22 of 22 while that defect is present.
  - Brand Clerk DEMO: output matches DEMO.md. The receipt holds no content hash.
  - Published app tests: all 11 files fail on Linux, because they call Windows-only commands.
- Checked the hashes the records claim: tool sha, read/packet stdout sha, the replay measurements against the return table, and the desk-core reviewed source against dd4cd00.
- Measured what the tool filled in versus what Prime typed on the first actual use: 57 of 78 decision fields came from the tool's template, and Prime wrote 21.
- Searched every remote branch for Codex's branch and the later files (t203u).

**Blocked**
- No branch has "codex" in its name. `git ls-remote --heads origin | grep -i codex` returned nothing. All 16 branches are listed in "Codex branch search" below.
- The later local files (`D:/Git/lib-build`) are not on any branch: `app/review_loop_tools_v9.py`, `app/authoring_tools_v2.py`, 0525 06.06, 0526 06.04, 0522 06.40 with prime-review05.18, and Brand Clerk 0701 05.10. So the later claims about them could not be checked. Exact list is under "Need".
- The Codex replay runs (experiment 3) were model work done on Windows, at `D:/` and `C:/Users/misg/...` paths. Their files can be read, but the runs can't be repeated.

**Need**
- Push the local `D:/Git/lib-build` work to a named branch, as Matthew said in t203u. Or upload these exact files with a `git rev-parse HEAD` and `git status` of that tree:
  1. `app/librarian.py` (the later version), `app/review_loop_tools_v9.py`, `app/authoring_tools_v2.py`
  2. `00.kernel/00.00.10.work/0525.app-dependencies/06.06.md` and every file in `0525.app-dependencies/evidence/prime-review05.03/`
  3. `00.kernel/00.00.10.work/0526.dev-authoring/06.04.md` and every file in `0526.dev-authoring/evidence/prime-review05.03/`
  4. `00.kernel/00.00.10.work/0522.review-construction/06.40.md` and every file in `0522.review-construction/evidence/prime-review05.18/`. On GitHub, `0522` holds only `evidence/build05.05/CONTRACT.md`, on `prima/returns` and `prima/assignments`.
  5. `10.workshop/10.10.work/10.10.13.brand-clerk/0701.brand-clerk/05.10.return` (exact file name unknown; probably `05.10.return.md`), plus the review it compares and the receipt it names.
  6. For each tool run: the Python version and the full command line.
- A decision on which proof to build first (see Question 4).

---

## Codex branch search (t203u)

Command: `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`, then `git for-each-ref refs/remotes/origin`. Run 12:36 PM EST.
No branch name has "codex" in it. These are the 16 branches, with their head commits:

```
main 14676ca                              rebuild de3b8eb
archive/librarian-worktree-2026-10-26 e8b1a99
archive/rebuild-worktree-2026-10-26 586cfa4
archive/lib-build-bootstrap-2026-10-26 fe42b01
observer/pilot-0502-2026-10-26 1a60557    observer/reviews 754b9fc
workshop 960d20c                          builder/grok-core-pass01 05aa369
prime/grok-core-review-pass01 5e0040e     prime/grok-core-review-pass02 42563e6
prime/grok-core-review-pass03 bdcc894     prima/assignments 1244554
prima/returns 6d61a27                     cursor/brand-clerk-v0-43b3 d5bc892
(origin HEAD -> main)
```

`workshop` (960d20c) is the latest branch that holds Codex Prime's lab work. The later files were searched for on every branch with `git ls-tree -r`. None of the Need items 1 to 5 were found.
One near miss: `0504.app-entry/evidence/prime-review05.18/` is on several branches, but it belongs to work item 0504, not 0522. The only tool-version file found was `app/review_loop_tools_v2.py`, on the prima branches, not v9.

---

## Reruns (question, command, input, result, limits)

All were run on Linux with Python 3.13.5, between 12:31 and 12:46 PM EST.

**R-1. Clerk lab.** Question: does the pinned source reproduce the claimed 20 tests, 8 processes and 14 events off Windows?
- Input: 960d20c `labs/clerk-handoff-pass01`. sha256: `clerk_lab.py` ef9f7c2f…122de3, `test_lab.py` 1051d19f…5dea48, `run_lab.py` e8533cb5…2fa4fa.
- Command: `python3 run_lab.py --output /tmp/clerk-rerun-<pid>`
- Result: exit 0. Tests "Ran 20 tests … OK". 8 processes, 14 events. Route: build-1 built, review-1 changes, build-2 built, review-2 accepted.
- Limits: Linux, not Windows. So it can't show the Windows file-handle fix.

**R-2. Prime-cycle tests.** Question: do the 32 tests that Codex ran on its own pass for a second reviewer?
- Input: 627c424, full `git archive`, committed into a scratch git repo. `prime_cycle.py` sha256 19ede9c2…e17861d. That matches "Accepted tool identity" in REVIEW.md:43.
- Command: `python3 -B -X dev labs/prime-cycle-pass01/tests/<file>.py` for test_prime_cycle, test_binding_log and test_observation.
- Result:
  - With `/usr/bin/python3`, which is a symlink: 30 pass, 2 fail (test_11 and test_30). The packet tool refuses because "python ancestor is link".
  - With `/usr/bin/python3.13`, the real file: 14 + 12 + 6 = 32 pass, 0 fail. `demo.py` exits 0.
- Limits:
  - A copy of only the lab folder fails all 32, because the tests need sibling labs (`../return-capture-pass01`).
  - The symlink refusal is the tool's own safety rule. It is not a bug, but the README does not tell a second reviewer about it.

**R-3. Desk-core CC-07 probe.** Question: does the hidden pending revision reproduce on the unchanged reviewed code?
- Input: dd4cd00, full archive. The probe is `probe-cloud-second-revision-nov01.py` from bdcc894, sha256 ade63402…0f7860. Only line 3 was changed, the `D:\` output folder, to point at a local folder.
- Command: `python3 -B probe.py`
- Result: same as the stored `second-revision-probes.json`.
  - At the after-prior-task stop: show says `selected`, body is "B selected wording", recover says `idempotent`. Meanwhile history/0002 holds C's intent.json and task.json. So pending C is hidden.
  - At the after-task-replacement stop: show says `conflict`, and recover says `restored-selected`.
- Limits: a process exit, not a power loss.

**R-4. Desk-core suite.** Question: does the 22-test suite pass when the full repo is present? Does it notice CC-07?
- Input: dd4cd00, full archive.
- Command: `python3 -B -m unittest app.desk_core.test_loop app.desk_core.test_repair app.desk_core.test_fault`
- Result: "Ran 22 tests … OK" in 13.4 s.
- What it means: the suite passes while CC-07 is present. So the suite does not cover a second revision.

**R-5. Brand Clerk DEMO.** Question: does the DEMO match its return? What does a receipt prove?
- Input: d5bc892. `code/clerk.py` sha256 1ae0fd48…5847e6, `code/scope.toml` e5a28d1b…7b1b.
- Command: the six DEMO commands, run with `python3 code/clerk.py`.
- Result: all six match DEMO.md:24-29. Unknown words get `stop:` and exit 2. A forbidden path gets `refuse: yes`, a handback, and exit 2.
- What a receipt proves: it holds day, pack, piece, path and "result: allow". It has no content hash, no actor and no command. `check` on a made-up path `code/clerk.py.tmp` also wrote an allow receipt. Nothing stops a write that never called `check`.
- Limits: DEMO's `..\..\..\..\00.00.00.kernel.draft` points one folder above the repo root. It was refused here because the path matched a forbidden name, not because it was found inside the repo.

**R-6. Published app tests.** Question: can a second reviewer run the published app's tests?
- Input: 960d20c `app/`, full archive in a scratch git repo.
- Command: `python3.13 -B app/tests/<file>.py` for all 11 files.
- Result: all 11 exit 1 on Linux. For example, test_entry.py says "pass 9 expected-refusal 42 fail 3", and its failures call `cmd /c mklink /J`. test_prime_tools.py: 2 failures, 2 errors.
- Limits: these tests are Windows-only. This is not proof that the app is broken on Windows.

---

## Findings

### F1. The clerk lab kept the route in recorded events, but its "correction" was scripted
- **Claim:** Clerk routed each step from a hash-chained event record. No work path was handed to a role by hand. But the launcher picked which role ran and when. The builder's "fix" was chosen by attempt number, not by reading the review.
- **Where:** 960d20c `labs/clerk-handoff-pass01/clerk_lab.py`:
  - :29-42 events with seq, prev and hash
  - :45-83 `project` rebuilds state and refuses a broken chain
  - :151-164 `next` picks the role's work from state
  - `actor`, around :255-262: the build body is picked by `work['attempt'] == 1`
  - `run_lab.py`:157-159: the fixed role schedule
  - REPORT.md:19-20: "The launcher did supply the workspace and role and did start each process in a fixed schedule."
- **Verified:**
  - R-1 reproduced the result.
  - transcript.json has 8 steps, all exit 0.
  - The review-1 artifact holds failing cases, but the builder never opens it.
  - The audit at step 8 is a fresh process that rebuilds closure from the ledger alone.
  - `initial-failure/tests.txt` shows all 20 tests "errors=20" with WinError 32 in tearDown, while its 8-step demo still exited 0 every step. So the first failure was a test-cleanup handle leak, fixed by closing connections (NOTES.md:95-106). It was not a routing fault.
- **Who did what:**
  - Built and tests written: Codex Prime. REPORT.md and NOTES.md are written in the first person, and Matthew says so in t202u. Git shows only "Mathias", d0bdd53.
  - Run: Codex's Windows runtime (`C:\Users\misg\.cache\codex-runtimes` in initial-failure/tests.txt). Rerun by Prima (R-1).
- **Design consequence:** take the ledger, the derived view, and "the summary file never decides routing" into the compute. Don't count this lab as proof that a model can act on a review. The next proof must have the builder read the review it got.

### F2. Prime cycle: the tool stamped every binding, but Prime still wrote the registration and the judgment
- **Claim:** On first actual use (read, then record, then read), the tool built the decision template and every hash binding. A new process rebuilt the day view from the journal. Prime wrote the registration by hand, supplied all judgment, and typed each command.
- **Where:**
  - 7e60567 `0515.prime-cycle/evidence/prime-review05.02/actual-use/README.md`:9-19. Line 17: "Prime still authored a registration and direction, supplied the judgment, and issued separate read/record/read/day commands."
  - `registration.json` (2,210 bytes, sha bf7a6ae6…57b30)
  - `templates/template-deskstate-0520.json`, `decision-deskstate-0520.json`
  - `day-view.json`
- **Verified:**
  - Prima compared template and decision field by field. 78 fields in all. 57 match the template: the binding block, hashes, goal and direction. The 21 that differ are all `attribution/*` or `judgment/*`: disposition, reasons, next action, unresolved, and so on.
  - The day view counts 1 read ok, 1 read ok-attention, 1 record, with per-operation times. It says it is "read-only; this view is not itself logged".
- **Who did what:**
  - Built: "Claude Builder" (claude-opus), per `evidence/build05.01..03/submission.md`, line 2 of each.
  - Tests: delivered in the builder's submissions. Who wrote each test is not recorded (unknown).
  - Used: Codex Prime.
- **Design consequence:** this is the right split for axiom 3. Compute fills bindings, the model writes only judgment, and a person sees the result. The registration is still hand-made. In our build, the compute should derive it from face 00 and the page index.

### F3. The 32 tests that Codex ran on its own, and what fixed the tool's identity
- **Claim:** In review 05.03, Codex reran 32 tests: 14 existing, 12 on binding and journal, 6 on observation. Then it used the accepted tool for a logged read and packet.
- **Where:**
  - 627c424 `0515.prime-cycle/evidence/prime-review05.03/REVIEW.md`:7-10 and :24-28
  - `independent-checks.json`: tool sha, argv, and stdout hashes
- **Verified:**
  - The tool's sha256 matches 19ede9c2… (R-2).
  - `read.stdout` and `packet.stdout` hash to the recorded 047eb4d2… and 37c82d4c….
  - The test counts per file are 14, 12 and 6.
  - R-2 reproduced 32 of 32 with a non-symlink Python.
  - Builder mutation results were "not rerun" (REVIEW.md:10). They remain builder claims.
- **Design consequence:** a pinned tool hash, saved argv, and hashed stdout are enough for a second reviewer. Keep that pattern. Also record the interpreter path and version, and say that the whole repo is needed.

### F4. The replay experiment found real delivery defects, not a speedup
- **Claim:** In both assisted runs, the tools could not read their sources, because `clerk_adapter.py` was not shipped, and the record step correctly refused. Case A also lacked its 5 pinned support files. Codex's own smoke check passed a broken kit, because it accepted exit 1 and never checked the state.
- **Where:**
  - 19fc336 `0172.prime-replay-codex-01/return.md`:23-35 (measurements), :73-89 (Blocked), :111-113 ("A clean day exit means the event journal is readable, not that the intended work succeeded.")
  - `colab/labs/prime-replay-pass01/results/codex/measurements.json`
- **Verified:**
  - `assistance/labs/batch-observation-pass01/batch_observe.py`:66 asks for `labs/prime-support-pass01/clerk_adapter.py`. That folder is missing from `assistance/labs/`, but it is in the repo at 19fc336.
  - Operation `02-case-a-assisted/operations/2d97501c…/stderr.txt` reads "missing clerk_adapter.py" (exit 2).
  - The record steps `e3cf3f74…` (case A) and `7070c7be…` (case B) exit 2.
  - measurements.json matches the return table: 6/10/9/3 commands, 0.485/1.876/4.780/3.203 s, and `tokens: null, cost: null`.
- **Who did what:** Codex designed and prepared the lab, ran the four conditions, and wrote the return (return.md:4-9). It "already knew the work" (:6-7).
  - Note: `0703.prime-replay/06.03.review.md` is Codex's review of **Claude's** replay return (0174), not of Codex's own. The review of Grok's return is 06.02. The three-model synthesis is `0703.prime-replay/REPORT.md`.
- **Design consequence:** before any run, check that the kit has every file it needs, all the way down, and that the expected state appears. Checking the exit code is not enough.

### F5. Desk core: Codex told a gap in its own review setup apart from a real product defect
- **Claim:**
  - Codex's first native run failed 1 of 22 tests, because its own export left out 33 pinned reference files. That was a review-setup gap, not a product bug.
  - Separately, Codex's own probe found CC-07: a valid selected revision B hides an unfinished revision C.
- **Where:**
  - bdcc894 `0523.desk-core/evidence/prime-review05.03/REVIEW.md`:17-27 (export) and :42-56 (CC-07)
  - `export-correction.json`
  - `tests.stderr`, line 25: the FAIL is `test_pins_and_live_book_and_undeclared`
  - `probe-cloud-second-revision-nov01.py`, `second-revision-probes.json`
- **Verified:**
  - The reviewed source in evidence matches dd4cd00 (spot-checked engine.py, test_fault.py and cli.py by sha).
  - R-3 reproduced CC-07 exactly.
  - R-4 passed 22 of 22 with the full repo. That confirms the first failure came from the export, and that the suite does not test second revisions.
  - REVIEW.md:39 also notes "One assertion compares a file read with itself and adds no evidence."
- **Who did what:**
  - Built: "grok.com builder" (`cloud-batch-original.md`:11).
  - Cloud Linux tests: builder-reported (REVIEW.md:12-13).
  - Native Windows run, export fix, and probe: Codex Prime. Rerun by Prima.
- **Design consequence:** our database must keep five things apart: the selected state, the pending operation, custody, review freshness, and acceptance (REVIEW.md:60-62). "Idempotent" must name what it covers.

### F6. Brand Clerk refuses well, but its receipt is a permission slip, not proof
- **Claim:** A small book with a dictionary, a concordance and a scope file let a model look up meanings, and it stopped instead of inventing. `check` refuses with a useful handback. But the allow receipt binds no content and no actor, and the gate only works if the model calls it.
- **Where:**
  - d5bc892 `10.10.13.brand-clerk/code/clerk.py`:109-125 (`write_receipt`) and :190-216 (`cmd_check`)
  - `code/scope.toml`
  - `0101.brand-clerk/05.02.return.md`:57: "clerk-mediated write so a model cannot bypass `check`" is listed as future work
- **Verified:** R-5.
- **Who did what:** Cursor agent built it (`0501.brand-clerk/05.02.md`:4). There are no tests. Director ran the DEMO (05.02.md:18). Prima reran it.
- **Design consequence:** keep the stop-instead-of-invent lookup, and keep the refuse-with-handback shape. In our build, writing goes through the compute gate (R33). The gate's receipt must include the content sha, the actor, and the pack, and it is written by the compute.

### F7. The published app is an earlier cut, and its tests only run on Windows
- **Claim:** `app/` at 960d20c has about 4,126 lines over 10 modules, and 11 test files. On Linux, every test file fails on Windows-only calls.
- **Where:** 960d20c `app/README.md` (the command list) and `app/tests/`.
- **Verified:** R-6.
- **Design consequence:** don't move this app over whole. Move its ideas, with failing cases attached, into our compute. Our tests must run on the box's Linux too.

---

## Matthew's four questions, in plain words

### 1. What could a fresh process recover? What did a person or model still carry?

**A fresh process got back on its own:**
- **Clerk lab:** the whole job state, from the event record. That covers who has what, what is waiting, and whether the job is closed. A wrong summary file did not fool it (test `test_stale_live_summary_does_not_control_routing`). A half-done claim showed up and needed an explicit "resume".
- **Prime cycle:** the day view, from the journal (`day-view.json`). It also rebuilt the review status from the git source and the review records, through `read`.
- **Desk core:** first-revision crashes, recovered in a new process, at nine stopping points (REVIEW.md:33-35). But it did **not** recover a hidden second revision (CC-07).

**Still carried by a person or model:**
- **Clerk lab:** the launcher picked the role and the order. The builder's fix was scripted.
- **Prime cycle:** Prime wrote the registration (2,210 bytes), wrote all 21 judgment fields, and ran read, record, read and day by hand (README.md:17-18).
- **Replay:** Codex picked paths and code ranges and wrote ad-hoc audit code (return.md:93-96). A broken read gave only "reader exit 2", so Codex had to call the inner tool by hand to find the missing file (:105-107).
- **Brand Clerk:** the model must choose to call `check`.

### 2. Which tests mattered?

**Found a real defect:**
- Clerk lab first run: the SQLite handle leak (NOTES.md:95-106).
- Desk-core CC-07 probe: the hidden pending revision. Reproduced (R-3).
- Replay: the missing `clerk_adapter.py` and the 5 missing case-A files. A setup defect.
- Claude's manual case-B pass (reviewed by Codex in 06.03.review.md:18-28): 19 nested evidence files missing from the delivery.
- Prime-cycle review 05.03: a diagnostic was 2,012 characters where the contract said 2,000. Small.

**Changed a decision:**
- The replay's "no-return beside observation-failed" confusion led to the reader repair. That repair was accepted in 05.03 (REVIEW.md:12-18).
- CC-07 led to "a CC-07-only follow-up" and no app adoption (REVIEW.md:67-68).
- The replay led to "verify the actual shipped bytes and their nested manifests" (06.03.review.md:64-68).

**Proved compute took over a manual step:**
- Prime cycle: 57 of 78 fields bound by the tool. The record step refused a null source identity, which caught the broken kit.
- Clerk lab: routing came from recorded state, with no hand-copied paths. But see F1: the launcher still scheduled the roles.

**Only exercised a fixture or a test mechanism:**
- All 20 clerk-lab tests use one synthetic job.
- The Director-decision test injects a fake decision (NOTES.md:120-122).
- The clerk checker shares code with Clerk (REPORT.md:47-48), so it is not a separate check.
- The prime-cycle `demo.py` uses "SUPPLIED FIXTURE" reviews.
- The desk-core self-compare assertion (REVIEW.md:39).
- The replay smoke check accepted exit 1 without checking the state (return.md:84-87).
- Brand Clerk has no tests, only a DEMO.

### 3. Where can a second reviewer repeat the result?

**Yes:**
- **Clerk lab:** the source and the run outputs are in the repo. R-1 matched.
- **Desk core:** the reviewed commit dd4cd00 is in the repo, and the probe script is kept. R-3 and R-4 matched. This is the best record of the five.

**Yes, with caveats:**
- **Prime-cycle tests:** you need the whole repo and a Python path that is not a symlink (R-2).
- **Actual-use outputs:** the stdout hashes match. But a full rerun of `read` needs the `D:/librarian/prime-cycle-out` and `D:/Git/lib-build` layout. Copies of the registration, decision and journal are kept, so you can read and check them, but you can't simply run them again.

**No (you can read and check them, but not repeat them):**
- **Replay runs:** they were model work on Windows paths. Token use and model time were never recorded.
- **Brand Clerk receipts:** they hold today's date and no content hash, so a later rerun can't match the one in the repo.
- **Published app tests:** Windows only.

### 4. What to carry forward, what to set aside, and one proof to watch

**Carry forward:**
- **Into the kernel / compute:** the event log with a hash chain, used as the only authority. Return and next route written in one transaction. A delivery ID can't change its content. Refuse with a handback.
- **Into the database:** the selected, pending, custody, freshness and acceptance states kept apart. "Observation failed" kept apart from "absent".
- **Into the desk IDE:** the compute fills the template and the model writes only the judgment. A day view built from the journal. Coverage shown on every packet.

**Set aside:**
- SQLite as a fixed choice. The lab itself says "not an approved architectural commitment" (REPORT.md:54-55), and R26 keeps small files.
- Windows-only test harnesses.
- Scripted-role demos offered as proof of model handoff.
- The default packet treated as a complete review.
- Brand Clerk receipts as proof.
- Moving the 960d20c `app/` over whole.
- Any speedup claim from the replay.

**Experiment 3: what it shows, and what a rerun needs.**
- **It can show:**
  - The assisted tools refuse to record without a source identity.
  - A full byte check is different from a complete working kit.
  - All three models reached the same main judgments (REPORT.md).
  - A manual second pass can catch omissions.
- **It can't show:**
  - Any speedup or cost ratio. The measurements are only subprocess seconds and stdout bytes, with tokens and cost null.
  - That the assisted path works, because both assisted cycles stayed partial.
  - Anything about a fresh model, because Codex already knew the work.
- **A rerun needs:**
  1. A kit with a preflight that proves every file it needs is present and that the expected state appears, including `clerk_adapter.py`.
  2. A model that has not seen the work.
  3. Tool calls and file reads logged by the harness, not self-reported.
  4. Provider token counts and model time, for each condition.
  5. Balanced order (manual and assisted swapped across cases) or separate model sessions.
  6. The same source range and frame given in every condition.
  7. A judgment rubric set before the runs, graded by someone who can't see which condition produced it.

**One proof Matthew can open and watch: "one edit, one review, one restart"**
- **Watch today, in about 1 second:** the clerk lab. Run `python3 run_lab.py --output /tmp/clerk-watch` in `/workspace/librarian-review/rerun1`. Then open `transcript.json` and `demo/00.live.md`. You can see 8 steps and the route closing.
- **Build next, on our compute (small, about one day):**
  1. A model sends one face 04 edit to `/propose`.
  2. The compute writes a face 09 line and makes a review template with the sha bound in.
  3. A second model reads the edit and fills in only the judgment, say "changes", with a reason.
  4. The first model reads that reason and sends a fix.
  5. The review is accepted, bound to the new sha.
  6. Stop the compute. Start it again, and rebuild the page view from the log alone.
  7. Then show two refusals. A hand-edited summary does not change the view. Editing the page after the review makes the review stale.
- **Pass if:** each step is a log line you can open. No path or hash was typed by a person or model. And step 4 really used the review text, unlike the clerk lab.

---

## What Prima recommends we use, and why (ranked)

Axioms are quoted from `docs/spec/Axioms.md`, by line. Rulings come from `docs/spec/DIRECTOR-RULINGS.md`. Leads: P = person, M = model, C = compute.

**1. One append-only, hash-chained log as the only authority. Views are built from it and never trusted over it.** (F1)
- **Why:** a fresh process rebuilt the state, and a fake summary couldn't steer it.
- **Axioms:**
  - 1 (:13) "The live record is where authority is kept … A draft, a copy, or a memory does not outrank it." Pass.
  - 6 (:23) "A change that is not recorded did not happen." Pass.
- **Rulings:** R28, face 09 is the log: pass. R33, books change only through the gate: pass. R26, small files are stored: pass, with the log kept as small files, not SQLite. R29: pass.
- **Leads:** C keeps it. P can open it. M gets the view.

**2. Return and next route in one transaction, and a delivery ID can't change its content.** (F1)
- **Why:** no lost or doubled work after a crash, which the tests showed.
- **Axioms:** 8 (:27) "A connection is lawful only when it is written." Pass. 6: pass.
- **Rulings:** R33: pass.
- **Leads:** C. P and M can't route around it.

**3. The compute fills the template and bindings. The model writes only the judgment.** (F2)
- **Why:** 57 of 78 fields came from the compute, so the model typed no hashes.
- **Axioms:** 3 (:17) "Each leads the part of the work it does best." Pass.
- **Rulings:** R35, elevation goes compute, then model, then person: pass. R36, open fields in face 00 are written only by the compute: pass.
- **Leads:** C binds, M judges, P approves.

**4. A review is bound to the exact revision it read. Any change makes it stale.** (F1, F3)
- **Why:** a review can't quietly move onto different work.
- **Axioms:** 9 (:29) "Work is not right because you made it." Pass. 6: pass.
- **Rulings:** R32 says a link points to the page, not a version. **Tension:** a review is a record, not a link, so it must name the sha it read. Links still follow the current page.
- **Leads:** C binds, M reviews, P sees what's stale.

**5. Keep the states separate: selected, pending, custody, review freshness, acceptance.** (F5)
- **Why:** CC-07 showed that merging them hides unfinished work.
- **Axioms:** 7 (:25) "Never invent it; unknown stays unknown." Pass.
- **Rulings:** R36, open fields in face 00: pass. R31, a lock is never undone: pass.
- **Leads:** C tracks it. P and M see what is pending.

**6. Keep "observation failed" separate from "absent", and show the real cause.** (F3, F4)
- **Why:** "no-return" next to a failed read misled the reviewers.
- **Axioms:** 7 (:25) "A required absence is a defect: report it, and raise it." Pass.
- **Rulings:** R35, elevate when unsure: pass.
- **Leads:** C reports it, M or P acts.

**7. A preflight that proves the kit has every file it needs and that the expected state appears, not just an allowed exit code.** (F4)
- **Why:** a byte-perfect kit still failed to run.
- **Axioms:**
  - 9 (:29) "it faces a hostile pass from another view." Pass.
  - 8 (:27) "A connection that cannot be opened is missing (`7.8`)." Pass.
- **Rulings:** R33: pass.
- **Leads:** C checks. P sees one pass or fail.

**8. Refuse with a handback (reason, what is allowed, what to do next), and stop instead of inventing a meaning.** (F6)
- **Why:** the model gets told what to do next instead of a dead end.
- **Axioms:**
  - 5 (:21) "At the edge of the frame, stop, state the issue, record it, and raise it." Pass.
  - 1: pass, but only if the gate is the compute and not optional.
- **Rulings:** R33: pass, once it is a real gate. R35 (elevate): pass.
- **Leads:** C refuses, M follows, P gets what was elevated.

**9. An operations journal: start and end for each operation, argv, input hashes, and time per operation. No productivity figures worked out from it.** (F2, F3)
- **Why:** this is what made F3 checkable.
- **Axioms:** 6: pass. 4 (:19) "Never invent a reason so the work feels finished." Pass.
- **Rulings:** R28: pass. **Tension:** face 09 is a page log, and this is a system-wide log. Where it lives needs a ruling.
- **Leads:** C writes it. P audits it.

**10. Show coverage on every packet: what was asked for, what was gathered, and what was not.** (F3)
- **Why:** it stops a model treating the default packet as the whole review.
- **Axioms:** 8 (:27) "a menu, a copy or a link never becomes what it points to." Pass.
- **Rulings:** R35 note, the menu first and then pieces on request: pass. It is the same idea.
- **Leads:** C gathers. M asks for more.

**Not recommended now:** SQLite as storage (R26 tension), the Brand Clerk receipt format, scripted-role demos as proof, the replay speed numbers, and the 960d20c `app/` code moved over whole.

**Three-lead check overall:**
- **Person:** can open the log, the day view, refusals and elevations (1, 6, 8, 9).
- **Model:** gets judgment work and menus, not bookkeeping (3, 8, 10).
- **Compute:** owns routing, binding, state and checks (1, 2, 4, 5, 7).
- **Gap:** none of the five sources shows a real model acting on another model's review through the compute. That is why the proof above asks for it.
