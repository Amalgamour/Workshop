# Pack A — preserve before establishing the workspace

State: PACKED / NOT RELEASED
Owner: Prime; executor: explicitly assigned Builder or Prime after release
Predecessor: none. Successor: Pack B, separately released after accepted return.
Authority: Director approved design and packing; execution awaits release.

## Goal and boundaries

Capture every row of preservation-manifest.tsv on independently verifiable archive
branches, without writing into either old checkout. Keep their files, refs, HEAD,
stashes and worktree registrations intact. Capture existing lib-build lab/notes and
Claude's source return too. Do not archive deleted files as deletions. The opaque
10.workshop.zip remains held as documented in inputs/claude-pass02/preservation-held.tsv; report
its custody, do not discard it. No main/rebuild branch push or force push.

All listed scripts in inputs are reviewed drafts, not trusted compute. Do not run
their copy modes. This pack includes building and testing the bounded copy helper
needed to make preservation safe; it does not delegate safety back to the model.

## #01 Capture and preflight

Read the package and verify every package hash, every source row and the workspace
baseline before writes. Set GIT_OPTIONAL_LOCKS=0 for reads of old repositories.
Capture HEAD, status --porcelain=v1 -uall, for-each-ref, stash list and worktree list
for both old checkouts. Record captured file hashes too: status alone cannot detect
a second edit to an already modified file. No fetch or maintenance in old repos.
Concurrent work is possible: a changed source is a reconciliation finding, never
permission to overwrite it or regenerate this approved manifest silently.

Use new isolated directories under D:\Git\lib-build\labs\bootstrap-preservation-pass01
for helper tests and temporary independent clones. Record absolute paths. Refuse
an existing nonempty clone destination. No local shared-object clone or worktree.

## #02 Implement the preservation helper and prove its refusals

Build a small tool plus tests in that lab. Inputs: explicit manifest subset, source
roots, destination repo, full expected HEAD and exact allowed replacement paths.
The tool must preflight the WHOLE batch before the first destination write:
- source bytes match pinned SHA-256 and length;
- destination is the expected independent Git repo at the expected HEAD;
- all paths are relative, unique ignoring Windows case, inside the resolved root;
  reject traversal, absolute/drive paths, alternate streams, reserved/ambiguous
  Windows names, symlink/junction/reparse escapes and unexpected file types;
- destination is absent, already the exact requested bytes, or a specifically
  allowed clean tracked file matching HEAD and index. A dirty/untracked conflict
  refuses. A committed file is not blanket permission to overwrite any path;
- index/worktree contain no unrelated changes; source and destination cannot alias.

Stage source bytes in isolation after verification; recheck destination conditions
before install. Write a recovery journal first and mark each installed file. Verify
final bytes. A copy is not complete if interrupted. Resume only using that journal
and the same pinned manifest; otherwise refuse and report recovery instructions.
Do not promise all-files atomicity. No automatic cleanup of evidence or unrelated
files. Stage only explicit manifest/tool/evidence paths, never git add -A/add ./ -a.

Meaningful isolated tests: new file; identical retry; explicitly allowed clean-base
replacement; dirty tracked conflict; conflicting untracked file; staged conflict;
wrong HEAD; changed source; duplicate/case-colliding destination; path and reparse
escape; source/destination alias; invalid late row leaves ALL earlier destinations
unchanged; simulated interruption leaves recoverable journal and cannot report
success. Include a successful recovery. Record skipped platform tests as skipped,
not passing. Run on Windows; use an independent scratch repo, not source checkouts.

## #03 Archive only the pinned rows

Clone https://github.com/Amalgamour/Librarian.git independently. Verify these full
objects exist and have the expected identities before branching:
- main baseline: 14676ca3c01833cc1b472198e62e3451ef706ec3
- rebuild baseline: de3b8ebc3df3e1da28c4d675963699644b78afab

Branches (no clobbering an existing divergent ref):
- archive/librarian-worktree-2026-10-26 from main baseline: P1–P6.
- archive/rebuild-worktree-2026-10-26 from rebuild baseline: P7.
- archive/lib-build-bootstrap-2026-10-26 from main baseline: P8 and P9.
Use separate clones or clean explicit switches. Only copy destinations listed for
that branch. An existing branch is resumable only after exact manifest/commit
verification; otherwise report the collision. Add preservation manifest and tested
helper/evidence under a distinct archive-evidence/ directory on each branch and
record their hashes. Never stage inherited files merely because they exist.

Tag baseline objects archive/main-14676ca and archive/rebuild-de3b8eb. Refuse a
same-name/different-object tag. Commit with Model: attribution. Record full commit
hashes, paths, counts and copied bytes. Push ONLY the three named archive branches
and two named tags. Release of this pack includes these publications; never main,
rebuild, wildcard refs, force pushes or a merge. Failed publication is pending,
not successful preservation.

## #04 Independent verification and return

In a second fresh remote clone, verify every archived row by destination, length
and SHA-256, and verify the remote refs/tags. Confirm archive-evidence hashes too.
Recheck old-checkout fingerprints and captured source bytes. Confirm baseline
labs/notes remain byte-exact. Distinguish concurrent source drift from a tool write;
either blocks declaring an unchanged-source pass until reconciled by Prime.

Write return to D:\Git\lib-build\notes\returns\pack-A-preserve-return.md with:
each #NN result, test command/output and failure cases, all archive refs by full
hash, verification counts, old-workspace before/after checks, journal status,
held zip location, new lab/evidence paths, and any unresolved finding. Preserve
stdout/stderr evidence separately. No work is approved/seated by this return.
Prime must accept the preservation result before Pack B begins.
