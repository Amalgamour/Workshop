# 05 - Build a runnable desk core for model handoffs
version: 001
date: 2026-10-31
who: Codex Prime
state: prepared; Director invocation releases this bounded prototype build
Face: 05
PPPP: 0523
book: 00.00.10.work

## Assignment
Executor: grok.com GitHub-connected builder. Reviewer: Codex Prime.
Repository: Amalgamour/Librarian. Branch: builder/grok-core-pass01 only.
Do not edit main/workshop or merge your branch into them. Standard-library Python
3.12+; no dependencies to install. Verify evidence/pack05.01/source-manifest.json.
Record invocation, branch, preparation commit and your actual model/host label.

## Goal
Produce a working local CLI core that takes work between Director/Prime and workers
through durable work-book files. It must run end-to-end on a disposable book.
Models supply content, judgment and proposed actions. Compute constructs records,
retrieves exact assignments/returns, verifies identities and persists transitions.
No automatic model launch, UI, service, subscription integration or migration is
required. A CLI with actual input/output commands is the first app core.

## Governing rules
- Source work N5NN maps to matching return N1NN, retaining NN and subject name.
  Passes stay inside that line. Never allocate a new page per capture/pass.
- N7NN Colab keeps 05.NN.pack.md, 05.NN.return.md and 06.NN.review.md on its page;
  it does not allocate N1NN. Implement this route or refuse it as unsupported;
  the first complete demonstrated loop must support N5NN correctly.
- Full readable Prime review belongs on N5NN/05.NN, not only an evidence pointer.
- Preserve source text, evidence and Director wording. No silent section loss.
- A receipt, a passing check and a review are different. None fabricates release,
  Director approval, seating, migration completion or permission to launch a model.
- Current-assignment records remain records. Views derive state and report conflict;
  they must not silently replace authority with newest-file selection.
- Review binding must survive mechanical pointer/review rendering, but task,
  relevant dependency/evidence or agreement changes must stale it.
- Concurrency and same-user permission limits are real. Never claim OS isolation,
  authenticated roles or race freedom from prompts, hashes or compare/rename alone.

## #01 - inspect, notes and minimal contracts
Write 06.01.md notes before code. Read the Prime review on 0519/05.01 and corrected
rule 0417/06.01 BEFORE treating original DESIGN/BUILD-PLAN as requirements. Their
old sequential members, evidence-only review home, successor-band proposal and
selector demotion are superseded. Grok-2's reviewed 0520 lab shows existing behavior.
Inspect current code and choose explicit reusable interfaces, not a wholesale
rewrite. Preserve existing modules byte-identical. In evidence/build05.01/CONTRACT.md
declare the prototype's schemas, layout, commands and exact compatibility boundary.
If existing custody tools cannot write matching lines, implement the minimum new
versioned prototype adapter inside your own module. Do not patch legacy receipts
or pretend /1 tools already support new placement. No historical live migration.

## #02 - implementation ownership
All new executable app code and its meaningful tests/docs belong in app/desk_core/.
Provide one documented invocation, for example python -m app.desk_core, using only
the standard library. Do not modify app/librarian.py or other existing modules.
The separate entry permits later reviewed integration without conflicting with
local builders. Read-only reuse of pinned dependencies is allowed; declare all
direct/transitive runtime dependencies and check supported source identities.
This core must be able to operate on an explicit fixture/work-book root. Tests
write only to disposable external roots. No tool automatically chooses the live
repository book or imports old assignment authority. Do not scan for highest version.

## #03 - actual vertical loop
Provide runnable commands, with structured JSON input/output where useful, to:
1. Initialize a disposable desk/work book and record a bounded task from a supplied
   specification. Compute builds its page/face and declared pass, not just a todo.
2. Register the supplied release and worker claim, bound to task/source identity;
   show the exact task, expected outputs, scope and current state to a new process.
3. Submit a worker return and artifacts; compute verifies/captures them under the
   matching return line/pass, then constructs the source batch's return pointer.
4. Retrieve the captured return and evidence for Prime, plus unresolved questions.
5. Accept a supplied typed Prime judgment, preserve findings/dissent/Director text,
   construct the FULL readable review on its source batch and record next action.
6. Restart and recover the actual pending state/next actor/action from records alone.
Also provide a small read-only pending-work view. Do not require whole-history scans
for exact page/pass retrieval. No new independent job ledger beside the work book.

## #04 - meaningful failures and evidence
Prove these with actual subprocess commands on disposable books:
- worker says done but no captured return is present: not complete;
- unchanged retry is idempotent; changed bytes under the same identity are refused;
- wrong return line/pass or source hash is refused;
- stale/conflicting assignment or receipt is visible and does not become accepted;
- review construction preserves bytes outside the allowed section and retains the
  complete supplied assessment, including zero findings and unresolved questions;
- adding a mechanical pointer/review does not invalidate task binding;
- changing task, bound evidence or agreement does invalidate it;
- after an interrupted write, state is partial/pending, never silently complete;
- after restart, return, review and pending next action are recoverable;
- two different passes of a source page remain within the same N1NN subject line.
Do not reproduce the held AR-01 hard-link race or run inventory/bridge fixtures.
Expected negative tests are successes when the specified refusal occurs. Label
synthetic tasks/judgments honestly. No claim of a real fresh model/session test.

## #05 - stop/checkpoint protocol
At each coherent completed stage, save notes/evidence and a scoped commit. If you
hit an UNEXPECTED failure, missing requirement, incompatible interface or design
choice not covered above: STOP affected build work, preserve files and raw errors,
and write evidence/build05.01/stops/STOP-NNN.json plus a readable STOP-NNN.md.
Do not guess approval or repeatedly retry the same failure. Expected refusals in
declared negative tests do not trigger this stop. Each stop must contain:
id; category; current stage; what worked; exact command/exit/error; relevant file
and source identity; impact; recommended smallest fix; alternative if any; exact
decision/input needed; current commit; resume checkpoint. Categories:
SOURCE, DEPENDENCY, CONTRACT, AUTHORITY, TEST, WRITE, RECOVERY, ENVIRONMENT.
Commit the checkpoint on this branch, update this batch's return pointer, and
reply with code, branch/commit, paths and the one thing you need. The Director
relays it to Prime. Wait for a recorded response before resolving that stop.
Use a later checkpoint/response record; never erase or rewrite earlier stops.
If Git publication itself is blocked, retain files and report that exact failure.

## #06 - finish and reproducibility
Write evidence/build05.01/submission.md (Did, Blocked, Need), CONTRACT.md, PRIME-USE.md,
verification.json and artifact-manifest.json. Include raw commands/results, actual
test counts/skips, a reproducible demo, all runtime dependencies, known limitations
and a precise proposal for integration into the existing app. Reread all output
and integrate notes before completion. Do not call the core production-ready.
Record the return pointer and full deliverable on this work page. Correct custody
home is 0123.desk-core after reviewed migration; its old occupant must not be
overwritten. Until then the durable page-local submission is explicitly pending
matching-line custody. Do not reserve 0184 or move any live captures.

## Allowed writes and Git
Only app/desk_core/, 0523/06.01.md, evidence/build05.01 and this batch's claim/return
pointer. Disposable fixture roots outside tracked source are allowed. No other
page, existing app/module, kernel/law, live data or capture changes. No source
deletions, renumbering, global config/credential changes, paid calls, new agents or
installs. Stage only explicit allowed paths; no git add -A, add . or commit -a.
Commits include Model: <actual model label>. Push only builder/grok-core-pass01,
never force-push, merge or touch main/workshop. The Prime reviews before integration.

## Return pointer
Claim: Grok Build (xAI), grok.com GitHub-connected builder, 2026-10-31.
Host: Linux sandbox. python3.11 is Python 3.11.2. python3 is Python 3.10.22.
Python 3.12 is not on this host. No runtime was installed. Tests and the demo used python3.11 -B.
Branch: builder/grok-core-pass01.
Preparation commit: 17ad02453edde4a2f65f6a0d78686004bf4e5fe1.
Notes checkpoint: 2c8a72b93b4782915ea0cbbcede4fadf4a33b3c5.
Implementation checkpoint: 6024a4245a87471a68cb85230172b333cc8c1549.
Submission commit: eaca9bd8dbcc2e5642d136a62f28c03161eeff4c.
Submission: evidence/build05.01/submission.md (Did, Blocked, Need).
Also on that page: CONTRACT.md, PRIME-USE.md, verification.json, artifact-manifest.json,
unittest.txt, demo-transcript.txt, and notes 06.01.md.
Prototype entry: python3.11 -B -m app.desk_core.
Tests: 9 run, 0 failed, 0 skipped. Pins: 33 of 33. Runtime dependency: Python standard library only.
Matching-line custody for this live batch remains pending reviewed migration.
Live occupant 0123.boot-validation-0508 was not overwritten. 0184 was not reserved.
No runtime acceptance. No model launch. Not production-ready.

## Review - Codex Prime
PENDING.
