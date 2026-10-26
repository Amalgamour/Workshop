# Pack B — addendum 001

State: PACKED / NOT RELEASED
Applies to: packs/lib-build-bootstrap-pass01-2026-10-26/PACK-B-establish.md
Owner: Codex, Prime. Executor: Director-assigned Builder or Prime upon release.
Reason: accepted Pack A found Git line-ending normalization after correct copying.
This is a correction to B, not another standalone build pass.

## #B-A01 — Dependency and return overrides

Before Pack B #01, verify this package's manifest, dependencies.sha256.tsv, the
original package manifest, and archive-dependencies.tsv. Use the final archive
commits listed there, not the earlier Pack A row/evidence commits:
- librarian-worktree: e8b1a994da07000fa576fd771e455a94718ed431 (90 rows)
- rebuild-worktree: 586cfa4ae055c29a98c1106bb70143901c57cc11 (28 rows)
- bootstrap: fe42b017b5e8c288f70878d696cb227b09ab5a8e (49 rows)
Verify these objects and row hashes after fetch in the NEW repository. Check the
remote archive refs still match. A moved ref is a finding; do not silently retarget.

Director correction: returns belong in D:\Git\lib-build\returns beside packs.
Override every Pack B reference to notes/returns with returns/. Read the existing
Pack A return from returns/pack-A-preserve-return.md. Write B's final return to
returns/pack-B-establish-return.md. Work page 0501 keeps linked/byte-exact copies
with provenance, not a second independently edited authoritative return.

The original pack, its ZIP and manifests remain unchanged. Record this addendum's
identity, execution release and outcomes on the bootstrap work page. The Director's
release must identify original B plus addendum 001. Do not rerun Pack A.

## #B-A02 — Early Git-byte fixture gate (before Pack B #02)

Run this gate in a NEW isolated scratch repository under
labs/bootstrap-git-bytes-pass01/scratch, before Git-in-place or importing book files.
Implement the small staged/committed-blob verifier required below as development
tooling on this lab/work page. The pre-F1 helper in inputs is not already fixed.
No staged blob may be accepted solely because the worktree file is correct.

Fixtures must include UTF-8 CRLF text, UTF-8 LF text and binary bytes (including NUL)
at representative custody paths, plus ordinary LF app code outside that scope.
Use explicit byte writes and pinned length/SHA manifests. Configure only the test
repository with core.autocrlf=true. Never change global/system Git configuration.

Tests and evidence required:
1. Demonstrate the original normalization failure under * text=auto eol=lf with a
   CRLF fixture. The mismatch must be detected at the INDEX blob, before commit.
2. With tracked -text custody rules, the same fixture and LF/binary files retain
   their exact bytes in worktree, index and commit. Record effective attributes.
3. Deliberately stage wrong bytes while the worktree contains expected bytes: the
   index check refuses. A clean diff alone cannot satisfy this check.
4. A deliberately mismatching committed fixture fails committed-blob verification.
5. Clone the fixture repo independently (no shared objects); enable core.autocrlf
   true BEFORE checkout (for example clone --no-checkout, configure, then checkout).
   No local .git/info/attributes workaround. Verify tracked policy and exact bytes
   in the new worktree and stored blobs. Local fresh-clone fixture is sufficient
   here; final workspace publication still needs B's remote-clone verification.

Capture commands/results and each expected refusal distinctly. Failure blocks B
#02 and later work; preserve evidence and return the finding. A failed gate is not
permission to create a new migration plan or alter the pinned source manifests.

## #B-A03 — Tracked attributes and checks at every Git boundary

Extend B #02 and #03: after the ancestry/empty-index commit, install and commit
the new workspace's .gitignore and .gitattributes BEFORE staging baseline payloads
or imports. This is new-branch setup; neither old checkout nor archive branch is
edited. Explain this insertion in the step log.

Track the following initial .gitattributes policy (root-anchored rules):

```gitattributes
* text=auto eol=lf
/imports/** -text
/labs/** -text
/notes/** -text
/packs/** -text
/returns/** -text
/00.kernel/** -text
```

Purpose: byte-exact custody for preserved baseline, evidence, snapshots, selected
references, candidates and work records; normal LF policy for new app/control text.
-text prevents Git text conversion; it does not require treating prose as opaque
to reviewers. Do not add binary/-diff attributes unless separately justified.
Maintain root control files with LF. Add their actual intended bytes to new-file
verification records as appropriate.

Inspect nested .gitattributes and effective attributes BEFORE staging each payload:
text must be unset for byte-exact paths, and no clean/process filter, ident expansion
or working-tree-encoding transformation may affect them. Inspect local info attributes
and configured attributes files for overrides. Refuse or reconcile a conflicting
effective transformation; do not assume the root policy necessarily wins. Do not
add an untracked * -text workaround or silently disable global settings.

For every declared byte-exact path, using literal path arguments:
- verify worktree bytes against the pinned custody manifest;
- after exact staging and BEFORE commit, read the INDEX blob through Git and
  compare length/SHA against that same manifest; reject missing/unmerged entries;
- after commit, read COMMIT:path blobs and repeat those checks;
- after publication, verify remote commit identity and all covered committed blobs
  from B's independent clone, then verify checked-out bytes under autocrlf=true.

The custody set includes the original 39 baseline files, all 890 snapshots, all
81 selected copies (73 references + 8 runtime candidates), 22 archive-sourced P1
decision files, immutable packs and input evidence, and newly captured immutable
return/review/tool evidence. Maintain explicit path/hash manifests, deduplicating
identical paths and refusing conflicting rows. Do not conflate these categories or
claim the sum is a unique-file count. New drafts/control records have their own
declared candidate hashes; no fabricated original-source hash.

If a stage or commit check fails, keep recovery evidence and stop publication.
An unpushed correction or an explicit fix-forward commit is acceptable; do not
rewrite shared history or normalize pinned source bytes to make a check pass.

## #B-A04 — Scratch exclusion and additive baseline

Extend B #01/#02: inventory the new labs, packs, returns and evidence added since
the original 39-file baseline. Exclude only generated scratch repositories/cache
from staging, with explicit tracked ignore rules, initially:

```gitignore
/labs/bootstrap-preservation-pass01/clones/
/labs/bootstrap-preservation-pass01/tests-tmp/
/labs/bootstrap-git-bytes-pass01/scratch/
```

Inspect for any other nested .git files/directories without traversing their object
stores. Classify them in the baseline/exclusion record; add exact exclusions only
for generated scratch. No blanket labs/ ignore, broad staging or accidental gitlinks.
Leave existing clones and test repositories in place. Keep helper sources, tests,
verifiers, stdout/stderr, journals, manifests and meaningful failed-run evidence.
Record hashes/remote refs needed to identify excluded clones; do not inventory
their internal Git object files as app payload. Git ls-files --stage must show no
mode 160000 entries. Check every intended source/evidence file is actually tracked.

The original 39-file manifest remains immutable. A new additive custody manifest
records subsequent material. Exclude its own bytes from itself; manifests, journals
and the final return must use a defined capture/finalization boundary rather than
recursively hashing a file that is still being written.

## #B-A05 — Evidence landing and final acceptance

Extend B #04/#07: retain the Pack A builder return, Prime report, Prime JSON/check
script and final verify_remote.py (all copied in this addendum's inputs) with source
identity. Preserve original helper/tests as evidence; the new verifier/fix must have
its own source/hash and tests. Record this on 0410.imports and 0501.bootstrap.
Do not claim the original archive-evidence helper already implements the new check.

The final return at returns/pack-B-establish-return.md must explicitly report:
- B #01–#07 AND #B-A01–#B-A05 outcomes, including actual fixture refusals;
- archive commits used, original/additive baseline counts and exact exclusions;
- effective byte-custody policy, staged/committed/fresh-clone checks and counts;
- successful imported/selected/P1 rows, candidate allocation and actual desk tree;
- zero tracked nested repositories, unchanged old-workspace fingerprints;
- location of the original pack, this addendum and all evidence in the work book;
- remaining runtime/activation work, skipped checks and unresolved findings.

Keep return publication finite: commit finalized evidence, write the return naming
that commit, then commit/push the return and verify its own bytes from another read.
The return need not contain the hash of the commit that contains itself. Report
that final return commit through the handoff; do not edit the return indefinitely.

All original B checks remain unless explicitly superseded here. The byte-fixture
gate is mandatory, not deferred. An incomplete orientation renderer is reported
INCOMPLETE as original B specifies. Nothing here authorizes runtime seating, lock,
Observer implementation, pending old packs, branch rewrites or a main merge.
