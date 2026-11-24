WORKSHOP PACK 90.50.10.0423.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0423 (one-worker)
prime:       prima
predecessor: 05.01
repo:        work
start:       1fdef9ad49c721a6b9dab5e44a24b1543c1c5dec
branch:      returns
return file: .workshop/returns/90.50.10.0423.05.02.md
grant:       src/cmd.rs, src/page.rs, src/lib.rs, tests/page_0423.rs (t562u)
axioms:      1.4.5.6.7.8.9
outcome:     Published pre-lockout page logs remain readable. A book-Prime override valid when written stays readable after succession. New writes require the same matching session lock and live authority as 05.01. Existing log bytes and sealed packs are preserved.
overview:    Builder: Grok-2. Checker: Grok-Check. 90.50.10.0423.05.02 repairs the two blocking findings on 05.01. Lead record: typed by Codex for Prima, t562u. Start includes the 05.01 implementation and failed close. Read the checker report on returns at f5125ea, reports/90.50.10.0423/05.01/Grok-Check-check-20261123-1644.md. Use t533u and t541u for the live one-worker and authority rules, and Axiom 6 for replay. Keep the existing commands, face-lock scope, first-claim rule and byte-prefix push guard. Reuse Page::load, Page::order and Page::add as far as the distinction between replay and a new append allows. Build the candidate in a separate target directory. Use the pinned a823ee28 wf.exe for the work order. The separate 0701 trial follows close. Fill the template-4 design review. If wf fails, follow docs/plan/MANUAL-RETURN.md.
jobs:
  w01: Make replay of the historical prefix before the first lockout entry accept valid work records written by earlier wf. Keep chain, event shape and pass-order validation. Once lockout has appeared, replay checks the lockout lifecycle, release sequence, holder and face of later events even between sessions. New command and Page::add writes always enforce the live lock rule from their first work event, including on an otherwise wholly pre-lockout page. A missing lock can never be excused in a new append. Do not rewrite any published entry, backdate a lockout or use a wall-clock cutoff.
  w02: Check override authority against the live parent book identity when a release is appended, preserving the person-only fallback when authority is missing. Preserve the actor, role, reason, holder and matching lock reference in the release. Record the basis used for the live decision, including the parent book address and its authority revision when available, or the missing-book/Prime fallback. On replay use the evidence recorded with the release, preserving structural, actor-role and lock matching checks. A later authority change must not retroactively invalidate an earlier valid override. For releases in the old shape, preserve structural replay of the recorded override and role. That compatibility rule is for replay only and must not allow any current release without the live authority check. Do not infer historically correct authority from a later book's current Prime or from cross-page wall-clock comparisons.
  w03: Extend tests/page_0423.rs with fixtures for a completed pre-lockout work order, a legacy page that acquires its first lock, a rejected new work event without a lock on that same legacy page, and valid and invalid post-lockout lifecycle events. Exercise status and verify against exact copies of published 0408 and 0423 log histories out of tree or include equivalent byte-preserving fixture evidence in the return. Prove the candidate can read both histories without changing their log bytes. Keep the existing tests for one holder, open claim exclusion, wrong-face refusal and byte-prefix pushes.
  w04: Test book-Prime succession after a valid override and prove the historical page still loads, including an old-shape override fixture. On a fresh lock, show that the former Prime and a distinct work-page Prime are refused, while the current book Prime or the person can override with a reason. Cover the person-only fallback. Report the existing page_0408 and wf fixture results separately from the packed tests. If fixtures still omit locks on new commands, identify them and bring the path/scope to the lead. Preserve live enforcement and keep those fixture files untouched.
may touch:   src/cmd.rs, src/lib.rs, src/page.rs, tests/page_0423.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0423   (one command each, split by ;)
done when:   Done when: Valid published pre-lockout logs, including 0408 and 0423, load and verify without changing any log bytes.
Done when: A new work event always needs the matching lock. Replay still validates the post-lockout lifecycle and rejects inconsistent history.
Done when: A recorded valid override still loads after a book-Prime change. New overrides enforce current book authority or the documented person-only fallback.
Done when: cargo test --lib and cargo test --test page_0423 pass with regression cases for legacy replay and authority succession. Existing lock and byte-prefix tests keep passing.
stop if:     the fix needs paths outside the grant; a published page record would need changing; you cannot distinguish a new append from replay in the code path; historical authority rules need a policy decision beyond these jobs; or any existing guard in 05.01 would be weakened. Name the finding and the evidence. Do not seed a real book identity or work around a refused live authority check.
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 14, hash 6d65da52f668
  face 06:        entry 15, hash 797130b13a81
  last closed 05: 05.01 closed at entry 12
sources:
  face 01:        v2 entry 13 hash e946b029cf51
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
