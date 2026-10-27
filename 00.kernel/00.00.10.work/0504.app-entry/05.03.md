# 05 — Independent review of designated-fixture repair
version: 001
Authorization: draft — 2026-10-26
who: Codex Prime
state: draft; awaiting Director release
Face: 05
PPPP: 0504
book: 00.00.10.work
keyword: app-entry

## Assignment
Executor: Claude Colab. Reviewer: Codex Prime. Release: PENDING. Claim: PENDING.
Independently review Grok's APP-01 repair before app-to-worker integration. Do not
implement integration or edit the app. Prime accepted the bounded repair; your
judgment must come from the code, contract and independently exercised behavior.
Inputs: evidence/pack05.03/source-manifest.tsv and exact inputs/ snapshots.

## #01 — Inspect and test in isolation
Review context.py, entry, new runner 003 and tests against 05.02's contract and
the original Prime source-overwrite finding. Verify source hashes, derive a copy
of the pinned published app and required book files in disposable scratch OUTSIDE
the shared workspace, and run the existing app suite there. Repeat the original
app/README.md source-folder fixture probe; prove refusal and unchanged bytes.
Review local designated containers, explicit external container, alias containment,
refusal before payload import, predecessor preservation, and relocation success.
Use judgment for a few meaningful boundary cases, not an open-ended security audit.
Same-user Python remains explicitly outside an OS sandbox. No external model calls.

## #02 — Integration readiness
Read 0503/05.04 design and Prime's clarifications from their pinned copies.
State exactly which repaired context functions/arguments the future glue should
reuse. Check that status inspection can use execute=False while new delivery
requires a release. Identify any material contradiction that blocks fixture-only
integration; separate it from deferred production concerns and ordinary improvements.
Do not fix a blocking issue yourself; return reproducible evidence for Prime.

## #03 — Return
Return here starting Did, Blocked, Need, then verified facts vs claims, findings
with file/line references, bounded recommendation and reviewed source identities.
No material findings is a valid result. May create 06.03.md and evidence/colab05.03/
on this page, and edit only this batch. No shared source, app/fixtures, other work
pages, labs, assignment/view/queue, dependencies or Git writes. All test writes
stay in disposable copies; retain evidence before any cleanup. Preserve Prime's
and Grok's records. No worker integration, activation, approval or model calls.

## Return — Claude
Release: the Director, chat 2026-10-26: "I release these two batches. Run them in this order and return separately on each page: 1. Independent review of Grok's fixture-boundary repair: D:\Git\lib-build\00.kernel\00.00.10.work\0504.app-entry\05.03.md 2. Repair the orientation checker's false-clean finding OR-01: D:\Git\lib-build\00.kernel\00.00.10.work\0502.workflow-start\05.03.md Follow each batch's scope. Do not edit the app during its review. Preserve Grok's work and the Observer's reserved review page. No shared Git writes, integration, activation or model calls. Return both for Codex Prime review."
Claim: claude-opus-5-5 (Anthropic), Colab, claimed 2026-10-26T18:23-05:00.
Execution: RETURNED for Codex Prime review, 2026-10-26. The app was not edited. No shared Git write, integration, activation, worker or model call. Grok's files and 06.01/06.02 were not touched. Written: 06.03.md (sha256 ec2c3004…) and evidence/colab05.03/ (manifest SHA256SUMS.txt, sha256 a11a75b4f8be5b55c8356ee693021856babeb9b87c43242208b2f6f878bb5845).

Did:
- Verified pack05.03: 9 of 9 snapshots match their pins, and the live files equal them. The app files equal HEAD d3bcdabd431bd0ca2bd5250da46f69b79879de89.
- Ran Grok's suite unchanged in a disposable `git archive` copy outside the workspace: exit 0, pass 10, expected-refusal 41, skip 0, fail 0, no bytecode (app-suite.txt). The copy is in another directory, so this also shows relocation succeeds.
- Ran 25 independent probes in that copy, using the suite's own fixture builders (probes.py, probes.txt). 23 pass, 1 FAIL (AR-01), 1 OBSERVE (AR-02).
- Probed status authorization per state (status_probe.py, status-probe.txt).
Blocked: nothing.
Need: a Prime decision on AR-01, below: whether it must be repaired before fixture-only integration. My recommendation is yes.

Verified facts (run here):
- The original APP-01 shape is refused before any fixture read, even with a complete fixture tree planted in app/ (record, payload, card, sample book; output README.md; allowed_root "."): "fixture root is not a designated container", and README stays 64a7953d…. Grok's test plants only fixture.json there; the full tree gives the same refusal.
- Designated containers: app/scratch and 0504.app-entry/fixtures succeed. The other page's fixtures folder and the sibling prefix fixtures-x are refused. A case-varied root succeeds from a foreign cwd. An explicit --container naming the other designated container is refused; naming the right one is accepted.
- An external container succeeds with --container. These are refused: a root outside the named container; an external root that is a junction to app/; a named container that is a junction to the workspace ("overlaps the workspace"); an output junction to app/ ("path escapes the root").
- Refusal before import: a payload that writes a marker on import was not imported at a refused root, with a broken stamp, or with mismatched CLI and fixture hashes.
- Predecessors: 02.run.001, 02.run.002 and 0302.run/02.md are unchanged, and 003 is selected by path and hash.
- Status: with runner_root set to the code root, validate_context(execute=False) passes for all six states. execute=True passes only for released; the others stop "assignment is not a fresh execution release".
Claims not independently verified: Grok's before-repair transcript (05.02.md:41). I did not rebuild the pre-repair tree; P9 below reproduces its after-hash by another route. Junction behaviour was tested only on this NTFS volume.

Findings:
- AR-01, material: the original overwrite recurs through a hard link. The approved payload is unchanged, its hash is the reviewed dd6a78b5…, the fixture sits in app/scratch, and there is no allowed_root. With output/inventory.json.tmp pre-planted as a hard link to app/README.md, test-run exits 0 with "result: pass", and the copy's README becomes 1b465c3517a5b4575a3ff5b2cdbeeb37220d83b262afb5f69864b292093e13c0. That is the same after-hash as the original failure. Cause: fixtures/02.inventory.py:94-95 writes its temporary file with write_bytes, through any existing link. The checks at context.py:94-104 and 553-564 and 02.run.003.py:260-264 and 281-282 compare resolved paths, and a hard link resolves inside the container. Write access to the container is the same precondition as planting fixture.json, so fixture data again decides where bytes land. To reproduce: run probes.py, step P9. The copy was restored and its tree check passed.
- AR-02, claim versus fact: README.md:21 says "This slice runs the one reviewed fixture payload". Nothing pins dd6a78b5…: librarian.py:79 takes the hash from the caller, and 02.run.003.py:240-243 compares it to the fixture's. In P8, a different, stamped, carded payload carrying its own hash ran inside app/scratch. This is not a boundary escape; README.md:21 already disclaims sandboxing. The sentence overstates what is enforced.
- AR-03, minor: validate_context defaults runner_root to the fixture root (context.py:383-384). Called without it, as where and validate do on a fixture, every state stops "runner is missing". The glue must pass runner_root=code_root.

Integration readiness (#02):
- The glue should reuse these, in librarian.py:85-100 order, before reading any job file: context.load_config(code_root/app/development-workspace.json); is_filesystem_root(root); overlaps_live(root, code_root, config); select_container(root, code_root, explicit), with explicit from --container only; guard_workspace_path(root, code_root); resolve_under(root, rel) and guard_workspace_path(..., code_root) for every job, input and output path. Then validate_context(root, config, execute=True, runner_root=code_root) for bridge-test, and execute=False, runner_root=code_root for bridge-status. load_fixture and check_allowed_root are fixture-only and are not glue inputs. The glue's job loader needs its own exact-key schema, with no container or root field.
- Status with execute=False and delivery requiring released: confirmed above. Per the Prime's clarification 2, bridge-status must also check the stored receipt's context, not only the current record. execute=False checks only the current record.
- Blocking contradiction: none in the design itself. DESIGN.md row 37 ("not accepted") and row 61 ("<APP-01 container metadata>") are stale: the accepted interface has no container metadata file, so the glue must neither read nor write one. AR-01 is the one blocking defect for fixture-only integration, in my view. The bridge's worker output_root (<container>/bridge/output) is reached by the same pre-planted-link class whenever it is reused. The bridge store itself is safe: its delivery folder is created fresh, and canon.py:50-59 writes inside it.
- Deferred production concerns: races between the guards and the write; 8.3 names and network paths (not tested); same-user Python not being a sandbox (already stated).
- Ordinary improvements: AR-02 wording; AR-03 default; the validate_context runner pin coupling for bridge commands.

Recommendation (bounded): one Grok repair slice before the integration pack.
1. In runner 003, or in a context helper it calls, refuse a fixture whose output or output.tmp already exists, or exists with a link count above 1. Or have the runner create the output folder fresh. Add P9 as a regression test.
2. Correct README.md:21, or pin the reviewed payload hash in the configuration.
3. Have the integration design create the worker's input and output roots fresh for each delivery.
Then pack the fixture bridge integration as the Prime planned.

Reviewed source identities (evidence/colab05.03/reviewed-sources.tsv):
- librarian.py 3d9aa20a…
- context.py ebb9d2e8…
- development-workspace.json b6f4e13b…
- test_entry.py f66f8af3…
- README.md 64a7953d…
- 02.run.003.py bbca1356…
- fixtures/02.inventory.py dd6a78b5…
- bridge/canon.py 6c1a761d…
All at HEAD d3bcdab or the live lab.
Shared checkout: HEAD and .git/index (e2f6591e…) are unchanged by this batch. Its only writes are 06.03.md, evidence/colab05.03/ and this return.
Overflow: TOCTOU, 8.3 names and network paths, parked untested. One thing I would have done differently: I would have run P9 against the pre-repair tree too, to show whether that route predates the repair.

## Review — Codex Prime
Date: 2026-10-27. Reviewed return SHA-256: `aa4bdb053d83bd5c3fab22f6be5848f17af3515388dc19f3600f745e7387ca3c`.
Disposition: Colab findings AR-01 and AR-02 accepted; integration remains blocked.
Prime independently reproduced AR-01 on a disposable copy of committed d3bcdab:
the standard, unchanged inventory payload ran in a designated fixture; its .tmp
output name was a pre-planted hard link (link count 2) to that copy's app README.
Exit 0; README changed from 64a7953d726e764c81208c16eaf294aa2d76ee87cdb2b7101a5e1693547037d9
to 1b465c3517a5b4575a3ff5b2cdbeeb37220d83b262afb5f69864b292093e13c0.
The real shared app was not executed or changed. Source containment does not
identify hard links. APP-01's original route stays fixed, but AR-01 is a new route
requiring repair before integration. AR-02 is also supported by inspection: the
caller and fixture supply the payload hash; docs must not claim a fixed payload
allowlist. No new authority framework is required to correct that wording.
AR-03 is an integration call requirement: use runner_root=code_root explicitly.
Next bounded repair is 05.04.md, draft pending Director release. Prime reviewed
the full Colab return and its six evidence-manifest files; did not repeat all 25
probes or claim their execution as Prime evidence. No model calls or Git writes
in this verification. The prior Prime acceptance of 05.02 was scoped to its tested
source-folder route and did not establish hard-link safety.
Evidence: evidence/prime-review05.03-2026-10-27/.
