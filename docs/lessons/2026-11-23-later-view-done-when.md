# Don't put a later-view trial on this pass's Done when

**What happened.** 90.50.10.0419.05.01 had a Done when that the lab trial `tests/lab_0419.rs` passes in lab 0701. Face 01 said another view writes that file after this return, and the grant did not include it. Grok-Check failed the check for that reason, even though the git grep work itself met its Done when lines.

**Why.** A check can only judge files in the return. A later-view file cannot be in this return.

**What to do next time.** Keep the later-view lab trial off this pass's Done when. The trial is its own later pass.

**Source.** Grok-Check report `reports/90.50.10.0419/05.01/Grok-Check-check-20261123-1144.md` on returns `f4b812ac`; close `7f3cdadf`.
