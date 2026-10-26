# 05 — First app entry and context-safe fixture execution
version: 001
Authorization: draft — 2026-10-26
who: Codex, Prime
state: returned
Face: 05
PPPP: 0504
book: 00.00.10.work
keyword: app-entry

## Assignment
Build a development CLI that reads explicit context, validates it, and executes one
useful fixture-only compute operation through a pinned new runner candidate.
Intended Builder: Grok. Reviewer: Codex Prime; separate Colab review after return.
Release: released by the Director, 2026-10-26.
Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-26, HEAD a5853b7ecdd076a77b4b106b057cea568e205bfb.
Reviewed base: a5853b7ecdd076a77b4b106b057cea568e205bfb, branch workshop.
Inputs: source-manifest.tsv. Some are intentionally modified/uncommitted Prime
review records; their pinned working bytes, not only their old HEAD bytes, matter.

Director, verbatim:

> Read and execute:
> D:\Git\lib-build\00.kernel\00.00.10.work\0504.app-entry\05.01.md
>
> I release this batch. Follow its scope and return on that page
> for Codex Prime review. Preserve Claude's independent work.

## Bounded finish line
These development commands work from a foreign current directory and relocated
fixture root (exact syntax below is the target interface, not an existing feature):

```text
python <workspace>/app/librarian.py where --root <workspace>
python <workspace>/app/librarian.py validate --root <workspace>
python <workspace>/app/librarian.py test-run --root <fixture> --candidate <fixture-relative-path> --sha256 <payload-hash>
```

where reports the desk, work book/space, current work, assignment state, runtime
book/space and selected dev runner. validate resolves their references and refuses
bad context. Neither executes a candidate. test-run works only on designated
fixtures, never the live work book. Normal run refuses; nothing is seated/activated.

## Scope
May create/change:
- app/: the entry, context module, explicit development configuration, tests and docs;
- law 0302.run: NEW 02.run.002.py candidate and 06.01.md adaptation notes only;
  preserve 02.run.001.py and 02.md byte-exact. No other law/syntax files;
- this 0504.app-entry page and evidence;
- work 0401.goal/01.md and 06.01.md, 0408.seats/01.md, 0409.decisions/01.md,
  0500.band.packs/01.md and 0611.findings/01.md: this release/assignment/status;
- work 0014.design: next versioned candidate documenting the local app configuration;
- work 0011.contents: next versioned candidate, keep predecessors;
- work book 00.md: update its provisional contents pointer to that exact new candidate;
- root README.md and app/README.md: actual entry/limits/next work;
- root .gitignore: exact app-test scratch exclusion only, retain existing rules;
- 00.kernel/00.live.md: regenerate/check from the record;
- 0502/05.01.md and its prime-review evidence: preserve/stage the existing Prime
  acceptance bytes as found; no rewriting the earlier return or acceptance.

No writes/capture in Claude's 0503 or lab, other runtime pages, old checkouts,
imports, original packs/returns or baseline labs. No model calls, APIs, UI,
Observer, Clerk dispatcher, job.py rewrite, dependency installs, seating/lock/main
merge or new permissions framework. Only workshop branch commits/push, no force.

This pack explicitly authorizes bounded CODE BODY changes in the new runner for
context/selection/path handling. It is not a stamp-only relocation. Original and
derived hashes and differences must be recorded. Do not silently activate a newer
candidate, add fallback search or run old candidate suites against old paths.

## #01 — Claim and establish one explicit development-context contract
Read the current entry/assignment, 0502 Prime Review, local notes and pinned sources.
Verify hashes and review current status/HEAD. Preserve the known Prime review
changes to 0502, its accepted assignment and derived view; no reset or stash.
List unrelated concurrent files and exclude them from staging. If an input changed
outside those known cases, reconcile with Prime before replacing it.

Use app/development-workspace.json as this slice's versioned, file-based LOCAL
development configuration. It explicitly names the assignment-record path, allowed
desk/book/workflow declarations, runtime book/space mapping and the exact loader
candidate path/hash. Document its small schema and validate it strictly. It is
application configuration for this release, not new universal kernel grammar or a
grant to execute arbitrary code. No index/database becomes a second truth source.

The actual operation context is work book 00.00.10.work, space 0. Its explicit
runtime context is law book 00.00.01.law, space 0 (N3NN -> 0300–0399). Never search
the work book for runtime just because it holds the job. The current work book
does not yet have a machine-readable space declaration; this configuration makes
that provisional declaration explicit rather than pretending prose was parsed.
Document its source/authority and future ownership on the versioned 0014 draft.

Validate: schema, required/duplicate fields and types, declared spaces, actual desk
and book folders, current work and pack references, path containment and ambiguity.
Reject missing, escaped, incompatible or undeclared context. Context validity and
assignment authorization are distinct: accepted/completed jobs may be inspected,
but are not a fresh execution release. 00.live is never the input authority.
result: pass. `app/development-workspace.json` is schema
`librarian-development-workspace`, version 1. It names the assignment
record, desk `00.kernel`, work book `00.00.10.work`, workflow space `0`,
runtime book `00.00.01.law`, runtime space `0`, and `02.run.002.py` by path
and sha256 `4a962d3a6edd26428b75e27ad82113708e510a1e770522d34b9e8bb11ec2b0f4`.
`where` and `validate` resolve that context and do not import the runner.
A record path ending in `00.live.md` is refused. Source and future ownership
are on `0014.design/01.002.md`. `01.001.md` is unchanged.

## #02 — Build the app entry and adapt the canonical runner candidate
Keep app/librarian.py thin; context validation has ONE implementation shared with
the runner by an explicit interface. Do not create a second competing loader in
app/. Adapt 0302.run/02.run.001.py into NEW 02.run.002.py: correct current stamps,
remove implicit cwd/book assumptions, and support only the declared development
selection needed here. Preserve useful existing card/stamp checks and record any
changed/retired behavior with reasons in 0302.run/06.01.md.

New runner selection is explicit path + SHA-256 + designated fixture scope. Match
the configured runner before importing it. Lookup is within the exact declared
book and N3NN band; zero/multiple matches refuse. Never pick highest version or
climb to another book/space. Selected payload must also be inside the permitted
fixture compute page and match its hash. A label claiming approval is not authority.
The normal run path refuses until a later reviewed activation contract exists.

Use explicit root parameters, avoid global os.chdir and permanent sys.path changes,
and keep generated bytecode out of the books. Preserve .VVV candidates, with source
and derived hashes. No original candidate or active-name file is overwritten.
Update app docs to describe actual commands, configuration and refusal behavior.
result: pass. `app/librarian.py` loads `app/context.py` from its own directory,
and `02.run.002.py` calls that same module. Source `02.run.001.py` is sha256
`af207d4d4f68ddcc2c22b7b1dced081b29dcbbfa6675d152ff7efa37871dcb8c`, 13805 bytes.
Derived `02.run.002.py` is sha256
`4a962d3a6edd26428b75e27ad82113708e510a1e770522d34b9e8bb11ec2b0f4`, 9470 bytes.
`02.md` is sha256 `95062ea60f8b923c3bda1cf603f394e54e56d961f42af13c9520031bf13bb95f`,
746 bytes, and still names `02.run.py`. No active-name file was written.
Normal run refuses. The adaptation record is `0302.run/06.01.md`.

## #03 — Execute one useful operation on a synthetic book
Create a declared test workspace and a small fixture compute page/payload. Through
the new entry and runner, inspect a fixture book and produce a JSON inventory of
its pages and files at a declared fixture output path. Compare the inventory to
explicit expected data, including an intentionally missing required fixture face
that the operation reports. This is fixture compute, not a fake external model.
Run the resulting operation through the entry, not by directly calling a helper
and claiming the loader path worked.

All mutable inputs, outputs and temporary candidates stay in app test scratch or
this page's fixtures. Require explicit fixture identity/allowed root and refuse
the real work book as a test-run root, even if a caller supplies a test flag.
Test scope and path validation are not OS sandboxing; state that same-user Python
code is not confined by these checks. Execute only the known reviewed test payload
in this slice. Do not advertise safety for arbitrary untrusted programs.

Record command, resolved context, selected runner/payload hashes, output artifact
hash and result. Explain what the real operation proves and what it does not.
result: pass. Fixture `0504-inventory-pass01` was inventoried from a foreign
current directory. Payload `fixtures/02.inventory.py` is sha256
`dd6a78b5a3781fe840e68950805b9838e569095d15dac3c678f00782341ed69b`, 2988 bytes.
Output sha256 `1b465c3517a5b4575a3ff5b2cdbeeb37220d83b262afb5f69864b292093e13c0`,
363 bytes, schema `librarian-book-inventory` version 1. `0101.present` has
`01.md` and `08.md`. `0199.gap` has `08.md` and `missing_required_face` `01.md`.
`fixtures/expected-inventory.json` and `evidence/inventory.json` are those bytes.
The live workspace root and the live work-book path both stop with
`fixture root is the live workspace` before a fixture is read. `--test` is ignored.
These checks are not an operating-system sandbox.

## #04 — Attack the boundary and repair orientation
Tests must cover the real command path:
- current real workspace: where and validate pass without executing anything;
- fixture operation succeeds from a foreign cwd and a relocated fixture root;
- missing book/work item, undeclared space, wrong job/runtime book mapping;
- ambiguous compute title, path escape and reparse escape where supported;
- wrong runner hash, wrong payload hash, payload outside its permitted page;
- missing/malformed config/record, duplicate keys and invalid assignment state;
- accepted/completed fixture assignment cannot be reused as a fresh release;
- normal run and test-run on the real workspace refuse without mutation;
- tampered 00.live cannot change context or the operation chosen.
Keep negative expected refusals separate from unexpected failures; retain failed
attempts. Hash protected source trees before/after to support the no-write claim.
Do not rerun unrelated suites merely to increase counts.

Address W-F1 within this named scope: create the next contents candidate preserving
predecessors, make the work book's provisional pointer name that exact candidate,
and document that the old contents generator is still legacy. Do not modify the
old lab writer; W-F2 stays open as a legacy-tool limitation. New app inventory may supply future generation data, but this pass
does not seat a new generator or silently make the old command safe.
Only mark context findings addressed to the extent tests demonstrate. Clerk lint
F01, routing, other module integration and cold-model/activation remain open.
result: pass. `app/tests/test_entry.py` printed
`summary pass 8 expected-refusal 30 skip 0 fail 0` and exited 0. A confirmation
run on 2026-10-26 printed the same summary. The saved log is the earlier
captured run, `evidence/test-log.txt`, sha256
`1b71ed03b4509012bd9ebf0d4d265ec0ec587e22d4e4e44824671c1f6c84b5ce`, 17275 bytes.
It holds eight PASS lines and thirty REFUSAL lines. Reparse escape was a refusal.
`00.md` names `0011.contents/01.003.md`. `01.001.md` and `01.002.md` stay.
`01.003.md` omits `0503.worker-bridge`. `write_contents.py` was not run.
W-F2 stays open. F01, F04, F05, Clerk routing, and activation stay open.

## #05 — Return in the book and publish the bounded change
Update release, scoped assignment and record running/returned explicitly; regenerate
the view. Keep current header state and Return execution state consistent; preserve the original packed state in a byte-exact packed snapshot, not as a contradictory current-state field. Preserve packed instructions if formatting changes are needed.
Use notes -> draft -> full reread -> integrated notes for the contract/adaptation.
Update relevant goal, door, findings and README pointers. Finish line 2 remains
PARTIAL: this slice does not integrate jobs/checker/clerk/face modules.

Stage exact authorized paths, including Prime's already-present 0502 review changes
and their evidence. Exclude 0503 and labs/worker-bridge-pass01, even if visible in
contents. Do not fix or commit another worker's files. Check staged/commit bytes
using existing custody tooling and explicit manifests. Publish workshop only after
checking the remote ancestor; no force. Keep final evidence/return publication
finite and report the final commit through the handoff.

Return here with exact commands, outcomes, counts/skips, code/record before-after
hashes, source/derived runner hashes, inventory output and known limitations.
The first decisive check for Prime: can the entry resolve real context and perform
the declared fixture operation without remembering a path from chat?
result: pass. The entry resolved the returned workspace and the fixture from
the files under `--root`. The selected runner was the hashed law candidate.
The inventory reported the missing face. The Return names the evidence commit.

## Return — Grok Builder
Execution: RETURNED
Implemented interface and actual commands: `python` is not on PATH. The interpreter
was `C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
Below, `<py>` is that interpreter and `<ws>` is `D:\Git\lib-build`.

```text
<py> -B <ws>/app/librarian.py where --root <ws>
<py> -B <ws>/app/librarian.py validate --root <ws>
<py> -B <ws>/app/librarian.py test-run --root <fixture> --candidate 00.kernel/00.00.01.law/0310.inventory/02.inventory.py --sha256 dd6a78b5a3781fe840e68950805b9838e569095d15dac3c678f00782341ed69b
```

`where` on the returned workspace printed desk `00.kernel`, work book
`00.00.10.work`, workflow space `0`, current work this file, pack this file,
assignment state `returned`, runtime book `00.00.01.law`, runtime space `0`,
runtime band `0300-0399`, runner `00.kernel/00.00.01.law/0302.run/02.run.002.py`,
and runner sha256 `4a962d3a6edd26428b75e27ad82113708e510a1e770522d34b9e8bb11ec2b0f4`.
`validate` printed those lines and `validate: pass`. Neither command imported
the runner. The fixture command printed `fixture: 0504-inventory-pass01`,
`result: pass`, and output sha256
`1b465c3517a5b4575a3ff5b2cdbeeb37220d83b262afb5f69864b292093e13c0`.
The same inventory was produced again from a relocated fixture root and a
different foreign current directory. `runner_resolved` was the law file
`02.run.002.py`.

Tests/evidence and fixture output: suite summary `pass 8 expected-refusal 30
skip 0 fail 0`, exit 0, confirmed again before publication. Log
`evidence/test-log.txt` sha256
`1b71ed03b4509012bd9ebf0d4d265ec0ec587e22d4e4e44824671c1f6c84b5ce`, 17275 bytes.
Inventory `evidence/inventory.json` sha256
`1b465c3517a5b4575a3ff5b2cdbeeb37220d83b262afb5f69864b292093e13c0`, 363 bytes.
`0101.present` lists `01.md` and `08.md`. `0199.gap` lists `08.md` and reports
missing `01.md`. `render_live.py check` is `evidence/render-check.txt`.
`write_contents.py --check` is `evidence/contents-check.txt` and exits 2.
The writer was not run, and `01.001.md` was not replaced.

Changed files and source/derived hashes: Accepted assignment
`evidence/assignment-before.md` sha256
`06380a35d72005b17aaa553e35b779107b7f439c14ae299787ab42cd90b4c73e`, 525 bytes.
Running `evidence/assignment-running.md` sha256
`f7ed0d88aaf63e42eb6583e8dd990edd6dfafc25f3fa78db75ecee0d4aa0cccd`, 546 bytes.
Returned record sha256
`d7f5c8f416641d8a3db113e6a09b8540e2bd802a1774e41f757ada4bd9aff9a6`, 633 bytes.
Views: before `evidence/live-before.md` sha256
`309f24b2fb79e504eb4672d6a8d8e117cba38f7e0347302f223ea0c6804f172c`, 1140 bytes;
running `evidence/live-running.md` sha256
`ef08714c5a3931ce602835d7bbc8238f98c0f4dfbfde372798d3ffc2959bc5e6`, 1161 bytes;
current `00.live.md` sha256
`02f183359e4e72a033dfb532b7f9a4687f0af5e515b9ee278e742fe125190f0f`, 1248 bytes.
Runner source `af207d4d4f68ddcc2c22b7b1dced081b29dcbbfa6675d152ff7efa37871dcb8c`
(13805 bytes) and derived
`4a962d3a6edd26428b75e27ad82113708e510a1e770522d34b9e8bb11ec2b0f4` (9470 bytes).
Card `02.md` sha256
`95062ea60f8b923c3bda1cf603f394e54e56d961f42af13c9520031bf13bb95f` (746 bytes).
Payload `dd6a78b5a3781fe840e68950805b9838e569095d15dac3c678f00782341ed69b`
(2988 bytes). Kernel paths in the evidence commit, other than `evidence/custody.tsv`
and the gitbytes transcripts, are in `evidence/custody.tsv`. `README.md`,
`.gitignore`, and the `app/` files are in `evidence/text-custody.tsv` and stay
out of the `-text` attribute check.

Failures/skips/remaining risks: This suite recorded no skip and no unexpected
failure. A fresh `autocrlf=true` clone was not repeated. Bytecode was kept out
of the books by `-B` and `PYTHONDONTWRITEBYTECODE`. The path checks do not confine
same-user Python, and they are not a claim about an arbitrary program. Finish
line 2 stays partial: jobs, checker, clerk, and face are not integrated. Normal
run stays refused. Nothing is seated or activated. `02.run.py` was not created.
W-F2 stays open. F01, F04, F05, Clerk routing, and cold activation stay open.
Visible at publication and not staged: `0503.worker-bridge/`,
`labs/worker-bridge-pass01/`, and `0505.observer-design/`. `01.003.md` lists
`0505.observer-design` and omits `0503.worker-bridge`, as this batch requires.
Prime's 0502 acceptance bytes are staged as found. Packed snapshots in
`evidence/packed/` stay byte-exact.

The entry can resolve this workspace and can perform the declared fixture
inventory without a path supplied only in chat. That is the check this slice
was built to answer.

Evidence commit: 70741312cb09c6413f9ea1b79902e050d884cce7. `gitbytes.py commit` passed 41 rows in `evidence/custody.tsv` and 7 rows in `evidence/text-custody.tsv` at that revision. The manifest, and the five transcripts left out of it, match that commit's blobs. This file does not embed the hash of the commit that contains this return.
Next work proposed, not released: integrate a real existing compute module against
fixtures, then review its activation; connect the independently reviewed worker bridge.

## Review — Codex Prime
Reviewed revision/hash: PENDING
Disposition, independently verified facts and remaining findings: PENDING
Colab review/Director activation if later required: PENDING
