# Release check, 90.50.10.0413 (pass 1 draft, after t492-t493u)

checked by: Cursor-C (Design)
date: 2026-11-23, 10:45 AM EST
checklist: docs/design/RELEASE-CHECK.md @ prima/build 78101fe6 (blob ef4c77486bcfddbdf8a013c6ff5651bb3df11aea)
code: origin/returns a823ee28
trial: docs/trial/TRIAL-WORK-ORDER-1.md at cloud/test b11becea
pack sha256: b10dc873a88d9bcf234e8c210214d5ca5f635b3d2338e56c865596785fc5323c

| Item | Source | Seen | Result |
|---|---|---|---|
| A1-A9 | t413u.md:7, :9; seqAddr.md:14, :242 | 90.50.10.0413 | PASS |
| No pasted quote | t461u.md:5; trial major 1 | no words: field; words stay on faces 01 and 04 | PASS |
| Seal told honestly | trial major 4; src/log.rs:2 | last entry not sealed; next entry seals | PASS |
| Prime and grant | trial major 3; src/cmd.rs:213, :220 | shown at pack time, later entries listed | PASS |
| Notes not by prefix | trial major 6; Axioms.md:27 | by entry number from the draft pin | PASS |
| Hashed files | src/render.rs:408 | pack text, AGENTS.md, PROMPT.md. The other two reprint | PASS |
| Old page exempt | trial note 4; src/render.rs:642 | a missing WORK-ORDER.md does not block | PASS |
| Folder push is not this page | Prima's statement of t492-t493u | page 0417; this may touch is src/render.rs | PASS |
| Wave 6 | section 15.4; section 13.5 | beside 0409; files do not overlap | PASS |
| t492 file | looked at 78101fe6 | words file absent; job text quoted and marked | TENSION |
| Axiom 9 | Axioms.md:29 | no hostile pass of this draft | TENSION |

Scratch dry run: init through verify passed. 7 entries. No secret in the output. publish-pack not run.

Verdict: no FAIL. Do not init the real page until he grants it.
