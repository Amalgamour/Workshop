# Release check, 90.50.10.0417 (pass 1 draft)

checked by: Cursor-C (Design)
date: 2026-11-23, 10:45 AM EST
checklist: docs/design/RELEASE-CHECK.md @ prima/build 78101fe6 (blob ef4c77486bcfddbdf8a013c6ff5651bb3df11aea)
code: origin/returns a823ee28
pack sha256: bf70059db131de638c523b0fe334807a6df74001966f561dd6bb1dd4857d166f

| Item | Source | Seen | Result |
|---|---|---|---|
| A1-A9 | t413u.md:7, :9; seqAddr.md:242 | 90.50.10.0417, next free after 0416, not 00 or 99 | PASS |
| H1 new page | one job; t249u.md:9 is a draft | the push is not the work-order view and not the temp name | PASS (the one-job rule is still only in a draft) |
| Why not 0413 | section 15.4 wave 6; src/cmd.rs:584-585 | 0413 is src/render.rs beside 0409. This needs the return command | PASS |
| Why not 0414 | Prima, 10:32 AM EST | 0414 is the temp-worker name | PASS |
| No force, no branch switch | the ruling; publish-pack never forces | w01 says never force, never switch the builder's checkout | PASS |
| Needs 0413 | the file that changes in 05.NN | face 08 names 0413 both ways in the drafts | PASS |
| Wave | 0414 stays 14 | this page is wave 16, trial 17; 0498 moves to 18 and 19 | PASS |
| t492 file | looked at 78101fe6 | words file absent; job text quoted and marked | TENSION |
| Check and close too | the ruling names return | the pack also updates after check, signoff, and close | TENSION (asked) |
| Axiom 9 | Axioms.md:29 | no hostile pass of this draft | TENSION |

Scratch dry run: init through verify passed. May touch src/cmd.rs, src/git.rs is inside the grant. No secret in the output.

Verdict: no FAIL. Do not pack it until 0413 has closed, and do not init it until he grants it.
