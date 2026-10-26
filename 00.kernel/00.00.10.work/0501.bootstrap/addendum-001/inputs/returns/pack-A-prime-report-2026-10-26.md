# Prime report — Pack A preservation

Date: 2026-10-26
Reviewer: Codex, Prime
Source return: D:\Git\lib-build\returns\pack-A-preserve-return.md
Disposition: ACCEPT preservation result. Pack B not started or released by this report.

## Verified outcome

Prime independently queried GitHub refs and checked the final objects in the
builder's fresh verification clone, using a separately written review script.
All 167 preservation rows match pinned length and SHA-256: 90 main-worktree,
28 rebuild-worktree, 49 bootstrap. All 36 evidence payloads match their per-branch
manifests; each branch also contains its HASHES.tsv. Both baseline tags match.
No branch changes paths beyond its declared rows and archive evidence. Main and
rebuild remote refs remain at their captured baselines.

Final archive commits:
- main-worktree: e8b1a994da07000fa576fd771e455a94718ed431
- rebuild-worktree: 586cfa4ae055c29a98c1106bb70143901c57cc11
- bootstrap: fe42b017b5e8c288f70878d696cb227b09ab5a8e

All 167 current sources, all 39 original lab/notes baseline files and package hashes
still match. Prime compared the current old-checkout HEAD/status/refs/stashes/worktree
registrations and hashed status files with the before capture: unchanged. All six
copy journals are complete. These checks establish the bounded preservation result;
they do not certify the copy helper as general production runtime.

Builder's test evidence records 20 tests: 19 passed, one source-symlink test skipped
because Windows denied symlink creation. Junction refusal was tested. Prime read
the helper, verifier and test output, but did not rerun the mutation test suite.

## Important learning

The initial archive verification failed because Git normalized CRLF bytes. Exact
working files are not proof of exact archived blobs. The builder kept that failed
result, corrected the archives with additional fast-forward commits, and verified
again from another clone. Prime independently confirmed the corrected final blobs.

This is useful evidence that the independent verification boundary caught an error
the copy checks missed. It is not evidence that the helper now prevents that error:
the archived helper is still the earlier implementation. Its successful copy
journal covers installed files, not the later Git storage boundary.

## Conditions to incorporate before releasing Pack B

1. Return destination is returns/ beside packs/. The Director's current instruction
   supersedes notes/returns/ in the immutable original packs. Preserve the original
   pack and record this override in a versioned addendum, rather than altering it.
2. Pin Pack A's three final archive commits above as setup dependencies.
3. Add staged-blob and committed-blob length/SHA checks for every byte-exact file.
   Include CRLF and LF fixtures. Do not rely on a clean Git diff or worktree hash.
4. Define a TRACKED .gitattributes policy for preserved/imported byte-exact files,
   including pre-existing lab/notes baseline material. Prefer explicit -text rules
   for that custody scope. Local .git/info/attributes alone cannot carry the policy
   to a new clone. Test a fresh clone under core.autocrlf=true and verify bytes.
5. Ignore generated clones and nested test repositories before staging workspace
   files. Keep their manifests, test evidence and remote archive references. Leave
   the scratch directories in place; no deletion is necessary for setup.
6. Include this return, Prime review, final verifier and verification evidence in
   the refreshed baseline and later work-book record. Do not claim the original
   archive branches contain the final verifier: it currently exists in the lab.

## Alignment and next action

This pass secured the source material and exposed a real storage-boundary defect
without starting the desk migration. It followed the bounded assignment and stopped
at the review boundary. There is still no .git or desk in lib-build; that remains
Pack B's job. Clerk routing, runtime activation and Observer are not built here.

Next: prepare the small Pack B addendum above, then release the workspace-establishment
pass through the Director's normal decision. No new architecture or role expansion
is needed to finish the desk. Observer remains a separate proposal.

Evidence: pack-A-prime-verification-2026-10-26.json and
pack-A-prime-review-checks-2026-10-26.py beside this report. The review script performs
read-only Git/source checks and writes its JSON under D:\librarian\temp; it makes
no archive changes or activation decisions.
