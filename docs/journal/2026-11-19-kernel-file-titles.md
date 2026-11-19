# Dev journal: titles in kernel file names

date: Thu 19 Nov 2026. All times are EST.
written by: Prima builder-b22, for Matthew and future models.
the spec (what the code does now): docs/spec/KERNEL-FILE-TITLES.md.

## What happened

1. Matthew sent a screenshot of the kernel folder on GitHub (t375u): "I need you to see this.  Notice you have no titles on these pages." Every file was a bare address such as `00.00.00.0051.01.draft.md`.
2. Prima checked: seqpage.md section 2 already says a page's name carries its title (`10.11.21.1001.bob.seq`), and every page's face 00 stamp already had one. The kernel files had never used it. Prima proposed the rename; Matthew said "Yes rename the kernel files" (t377u).
3. builder-b22 renamed 65 files with git mv, so history follows them. Page 0000 and the axioms keep their names (spec sections 1 and 4).
4. The builder (kernel/build.mjs) learned the new name form and a check: a name whose title disagrees with its stamp stops the build and says "elevate to Director". Why stop and not fix it: A2.8 says a mismatch is elevated to the user, and axiom 8 says a copy does not outrank the record. The stamp is the record; the name is a copy.
5. Old names are still read in history, so seats and trials made before today still verify. Why: R2 pins a seat to a blob and a trial to the file it passed; renaming must not undo a seat.
6. Live docs that point at a kernel file were updated (SEQ-FILE-PLAN, WORK-BOOK-SPEC, page-types, kernel/parked/README.md). Records of the past were left as written (spec section 7).

## Results

- Tests: `node kernel/build.test.mjs` 82 pass (74 before, plus 8 title tests). `node kernel/build.mjs --check`: seats 26, 48 findings, 0 errors, same findings as before apart from the file names in them.
- export/ is byte-identical before and after. The books hold addresses, not file names.

## One slip

The 65 renames were staged in the shared repo index when another commit on build was made (5524c16, Director words t379u), so that commit carries them. The builder half came one commit later (9cf70d7). Between the two, `--check` at 5524c16 fails on the new names. Nothing was rewritten to hide this (no amend, no reset).

## Still open (for Matthew)

- The seated 05.02 packs name exact old paths in grant:/path:/done: lines. Changing them means a new draft and a new trial (R2). Until then, read those lines by address.
- The axioms names (spec section 4) are a builder choice, marked 7.
