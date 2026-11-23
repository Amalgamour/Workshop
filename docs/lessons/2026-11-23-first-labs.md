# First labs, 23 Nov 2026

Lessons from the first closed passes of the day: 90.50.10.0404, 0702, and 0703.

## Windows quoted check commands

**What happened.** On Windows, wf splits a quoted check command at spaces. A pack check like `git grep -q -F "## 3. Results"` failed with `ambiguous argument 3.` The heading was in the file. The fail was a wf quoting bug, not a fault in the lab return.

**Why.** wf runs each check through `cmd /C` on Windows. The quotes around a multi-word pattern do not stay together.

**What to do next time.** Write pack checks with no spaces inside a pattern. Until a page fixes the quoting, use a form like `git grep -q -E "^##[[:space:]]3[.]" -- <file>`.

**Source.** `docs/design/drafts/WF-WINDOWS-QUOTING.md` on branch `cloud/design` at 35a3f18a. Close logs 90.50.10.0703 `bdcc8b72` and 90.50.10.0702 `86770ec2` (checker notes: Windows heading-check fails are a wf quoting bug). The failing check form is in the 0703 pack: `git grep -q -F "## 3. Results"`.

## A changed template version must update every test that pins the old version

**What happened.** Page 90.50.10.0404.05.01 moved new packs to template 4. Two tests in `tests/wf.rs` still expected template 3, so the check failed. `tests/wf.rs` was outside the grant, so the builder could not fix them in that pass.

**Why.** Those tests pin the current template number. Changing the version without updating them leaves the suite red.

**What to do next time.** When a pass changes the template version, the grant must include every test that pins the old version, or a follow-up pass must update them before the suite can pass.

**Source.** Close log 90.50.10.0404.05.01 `464170c7`. Failures at `tests/wf.rs:1332` (`new_pack_records_template_version_3`) and `tests/wf.rs:2840` (`stripped_hashes_with_a_rechained_log_stay_invalid_after_fix`) on return `858f2846`, where `TEMPLATE_VER` is `"4"` (`src/render.rs:31`).

## A lab's pick must be backed by tests that measure the property it relies on

**What happened.** The 0703 storage lab picked an append-only hash-chain log. Claude's cross-check said the pick was not supported. The stores were not compared fairly: write durability was unequal, each store used a different tamper attack or reference, and there was no update workload (`read_one` returns the oldest record).

**Why.** A pick that is not measured on the property it needs can look strong in the table and still be the wrong store.

**What to do next time.** For each reason behind a pick, include a test or measurement of that property, and use the same attack and the same workload on every store.

**Source.** Close log 90.50.10.0703.05.01 `bdcc8b72`, checker note from Claude's cross-check.

## Cross-checks between two builders found real majors that self-checks missed

**What happened.** Codex built 0703 and Claude built 0702. Each then checked the other's lab. The automated pack checks and the self-checks passed. The cross-checks found real majors in both labs. Both passes were closed failed and sent back for 05.02.

**Why.** The builder is close to their own work. A second builder, reading to attack the report, sees gaps the first pass missed.

**What to do next time.** Keep the t506u rule: the other builder cross-checks the lab before it is closed as passed.

**Source.** Close logs 90.50.10.0703 `bdcc8b72` and 90.50.10.0702 `86770ec2`.

## Pack with the same wf build the builder runs

**What happened.** A wf built from `c09fa60c` does not know template 4. `packed_templates` treats `"4"` as an unknown version and refuses the pack. The build that first accepts template 4 is `a823ee28` (the 0404 return on `returns`).

**Why.** If Prime packs with a different wf than the builder runs, the pack may be refused on one side and accepted on the other.

**What to do next time.** Pack with the same wf build the builder runs.

**Source.** `c09fa60c` `src/render.rs:38-51` (no `"4"` arm; `"4"` is refused at line 49). `a823ee28` `src/render.rs:51` (the `"4"` arm).
