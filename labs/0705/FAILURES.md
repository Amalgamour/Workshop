# Lab 0705: when a report cannot land

Page 90.50.10.0705, pass 05.01. Builder: Claude. Status: `9`.
Each section says what happens today (wf a823ee28), what the report path should do (**Claude proposal**), and what wf must tell the worker.

The common rule for every case (axiom 7, Axioms.md:25@8e96151d): a report that did not land is reported as not landed. It is never claimed as pushed, and never silently dropped.

## 1. Push rejected

**Today.**
- `push_log` tries 3 times.
- On each rejection it pulls with a merge (`pull --no-rebase`) and pushes again, and it never forces.
- On the third failure it prints "return recorded locally but the push failed 3 times (...). Nothing was forced. Run: git -C <work> push origin HEAD:<branch>" (src/cmd.rs:565-578).
- The stopgap snippet rebases instead of merging (docs/plan/REPORTS.md:68-72).

**Report path.**
1. Keep wf's merge, not a rebase.
   - A merge keeps the worker's commit SHA, which the `return` entry already recorded (src/cmd.rs:542-544, :524).
   - A rebase would make the recorded commit disappear from the branch.
   - Never force (kit AGENTS.md; docs/plan/REPORTS.md:26).
2. Before pushing, sync the page log from packs (SPEC.md section 2, step 2). A rejection is then almost always just another worker's commit on the same branch, and the merge is clean.
   - The two only conflict if both changed the same page log. That cannot happen while one page has one open pass and one holder.
3. If the merge conflicts:
   - abort it, as `merge_into_shared` does (src/cmd.rs:549-552);
   - leave the report committed locally;
   - queue it (section 2);
   - print: `report <seq> recorded locally; not pushed: merge conflict on <branch> in <paths>. Nothing was forced. Tell Prima.`
4. After 3 failed tries, print the same line, with the last git error in place of "merge conflict". Then exit with a failure code, so a script that runs wf can see it.

**What the worker must be told** (the last line, never hidden):
- whether the report is in the local log (yes, always, once step 3 of SPEC.md section 2 ran);
- whether it reached GitHub;
- the one command to try again: `wf report --retry`.

## 2. Offline

**Today.** `return --push` without a network fails during `merge_into_shared`'s `git fetch`, before any entry is written (src/cmd.rs:496-499). So an offline return records nothing. `check` never pushes, so offline makes no difference to it today.

**Report path.**
- **Recorded locally, always:** the `return` or `check` entry, the `report` entry, the reprinted views, and a local commit on `report.branch` holding the log and the report copy. Nothing about the work is lost by being offline.
- **Queued:** wf appends one line to `<WF_ROOT>/.wf/outbox`:

  ```json
  {"page":"...","pass":N,"seq":S,"commit":"<local commit>","branch":"..."}
  ```

  The outbox lives beside the config, outside `pages/`, and is never pushed.
- **Retried:**
  - `wf report --retry` pushes each queued commit in order, with the same merge-and-retry rule as section 1, and removes the lines that landed.
  - Every later reporting command also tries the outbox first, so a worker that is back online clears the queue without being asked.
- **Order kept:** a later report on the same page is not pushed ahead of an earlier queued one. The branch's copy of the log must stay a prefix chain for intake to take it (src/cmd.rs:629).
- **A return that needs the network.** A builder's code commit must be on the branch for the check to run (src/cmd.rs:505-506). So `return --push` offline records the return and the report locally, and the check waits until `--retry` lands both.

  This is a change from today, where an offline return records nothing. It is a proposal, raised for Matthew because it changes when a return "counts".

  (a) Proposed default: the return counts when it lands on the branch. That is when `wf intake` on Prima's side shows it.

## 3. Codex no-network

The case: the Codex CLI may run in a sandbox with no git network. It can still write files and run wf in its run folder, but `git fetch` and `git push` fail.

**Report path.**
- Codex's run folder is set up with `report.push: false` (`wf setup --no-push`, WORKER-SETUP.md section 1).
- Every report is then recorded and committed locally, and queued in the outbox (section 2). wf prints: `report <seq> recorded locally; push is off for this run folder. A networked shell must run: wf report --retry (in <WF_ROOT>)`.
- Matthew, or a networked shell he opens on the same machine and folder, runs `wf report --retry`. Nothing about the report changes. The retry pushes the commit Codex already made, so the report is still Codex's (actor and commit author).
- If Codex cannot reach the run folder's disk from any networked shell either, the report cannot land on GitHub. The lab says so plainly:
  - the report exists only in that run folder's log;
  - Prima cannot see it;
  - the pass must not be checked until it lands, because the check needs the commit on the branch (src/cmd.rs:505-506, :753).
- **What is not allowed:** pasting the report into chat as a substitute for the push. A pasted report is not in the chain (DESIGN.md section 1). A prompt box may say that a report is waiting, but not carry it (WORKER-SETUP.md section 3).

The source does not say what network the Codex CLI on Matthew's PC actually has. Codex's checks on 2026-11-23 were filed as "Codex (Matthew's PC)" in page logs. Whether Codex pushed them itself is not recorded (`7`).

## 4. Dead lock

**Today.**
- A write command takes `<page>/.wf-lock` with `create_new`, and waits up to 5 s (src/lib.rs:85-104). The lock is removed when the command ends (src/lib.rs:106-110).
- If the process is killed, the file stays.
- Every later write then refuses with: "another wf command is writing this page (... exists). If none is running, remove that file." (src/lib.rs:97-100).
- `verify --fix` also takes the lock (src/lib.rs:117), so it cannot repair a page that has a dead lock.
- This happened on 2026-11-23. A filtered pipe ended `wf check` on 0703 after its log append but before its view reprint, leaving the lock, a `.03.md.wf-tmp` file and stale views (labs/0702/LESSONS.md, lesson 7).
- Page 0420 is the later fix (docs/plan/GROK-BUILDER-QUEUE.md:86).

**Report path, until 0420:**
1. **Hold the lock for as short a time as possible.** The report path holds the lock only for append and reprint (SPEC.md section 2, step 3), never for fetch, merge or push.
   - Today `return --push` holds it through the whole push, because `run` takes the lock for the whole command (src/lib.rs:154) and `ret` pushes inside it (src/cmd.rs:533-536).
   - After the build, a killed or hung push cannot leave a lock.
2. **Save the report before taking the lock.** wf writes the report text to `<WF_ROOT>/.wf/pending-<page>-<pass>-<kind>.md` before it takes the lock. If the lock is dead, nothing the worker wrote is lost. wf prints the existing lock message and adds: `report text saved at <path>; nothing was appended.`
3. **Never remove a lock.** wf never removes a lock it did not create, and never on its own judgement (axiom 1, Axioms.md:13@8e96151d). The worker stops and tells Matthew in a prompt box.
4. **The manual repair, as done on 2026-11-23 with Matthew's approval:**
   1. Confirm no wf process is running (`Get-Process wf`).
   2. Remove only the lock and any `.wf-tmp` files in that page folder.
   3. Run `wf verify <page> --fix`.
   4. Run `wf verify <page>` and confirm it says ok.
   5. Re-run the report command. The one-report-per-`of` rule (SPEC.md section 4) refuses a double entry if the append had already happened, and wf then only pushes.
5. **After 0420.** When `verify --fix` can take over a dead lock (for example, a lock older than the last log entry, docs/plan/GROK-BUILDER-QUEUE.md:86), step 4's hand removal goes away. The report path does not change.

**Never pipe or filter wf output** (`Select-Object -First N` and similar). A closed pipe can end wf mid-write. That is how the 2026-11-23 dead lock happened (labs/0702/LESSONS.md, lesson 7). Worker prompts already say so. This lab adds that wf's own last lines must be short enough that nobody needs to filter them (SPEC.md section 2, step 7).
