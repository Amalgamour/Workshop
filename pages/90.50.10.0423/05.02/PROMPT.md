=== WORKSHOP JOB 90.50.10.0423.05.02 ===
Pack hash: e8e5d3404b3977c26489fce3c30024106142dc6f3d1e81bcee1190887eb8327f (log entry 17, 2026-11-24T18:52:09Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0423 02 --as <your-name>
Repo: work   Branch: returns   Start: 1fdef9ad49c721a6b9dab5e44a24b1543c1c5dec
Read first: pages/90.50.10.0423/05.02/AGENTS.md (sha256 f174acc65161), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: Fix 0423.05.01 replay compatibility while preserving live lockout, authority and prefix protection.
Builder: Grok-2. Checker: Grok-Check.
Done when: Valid published pre-lockout logs, including 0408 and 0423, load and verify without changing any log bytes.
Done when: A new work event always needs the matching lock. Replay still validates the post-lockout lifecycle and rejects inconsistent history.
Done when: A recorded valid override still loads after a book-Prime change. New overrides enforce current book authority or the documented person-only fallback.
Done when: cargo test --lib and cargo test --test page_0423 pass with regression cases for legacy replay and authority succession. Existing lock and byte-prefix tests keep passing.
The separate 0701 follow-up trial is outside this pass.

Jobs:
  w01: Make replay of the historical prefix before the first lockout entry accept valid work records written by earlier wf. Keep chain, event shape and pass-order validation. Once lockout has appeared, replay checks the lockout lifecycle, release sequence, holder and face of later events even between sessions. New command and Page::add writes always enforce the live lock rule from their first work event, including on an otherwise wholly pre-lockout page. A missing lock can never be excused in a new append. Do not rewrite any published entry, backdate a lockout or use a wall-clock cutoff.
  w02: Check override authority against the live parent book identity when a release is appended, preserving the person-only fallback when authority is missing. Preserve the actor, role, reason, holder and matching lock reference in the release. Record the basis used for the live decision, including the parent book address and its authority revision when available, or the missing-book/Prime fallback. On replay use the evidence recorded with the release, preserving structural, actor-role and lock matching checks. A later authority change must not retroactively invalidate an earlier valid override. For releases in the old shape, preserve structural replay of the recorded override and role. That compatibility rule is for replay only and must not allow any current release without the live authority check. Do not infer historically correct authority from a later book's current Prime or from cross-page wall-clock comparisons.
  w03: Extend tests/page_0423.rs with fixtures for a completed pre-lockout work order, a legacy page that acquires its first lock, a rejected new work event without a lock on that same legacy page, and valid and invalid post-lockout lifecycle events. Exercise status and verify against exact copies of published 0408 and 0423 log histories out of tree or include equivalent byte-preserving fixture evidence in the return. Prove the candidate can read both histories without changing their log bytes. Keep the existing tests for one holder, open claim exclusion, wrong-face refusal and byte-prefix pushes.
  w04: Test book-Prime succession after a valid override and prove the historical page still loads, including an old-shape override fixture. On a fresh lock, show that the former Prime and a distinct work-page Prime are refused, while the current book Prime or the person can override with a reason. Cover the person-only fallback. Report the existing page_0408 and wf fixture results separately from the packed tests. If fixtures still omit locks on new commands, identify them and bring the path/scope to the lead. Preserve live enforcement and keep those fixture files untouched.
May touch: src/cmd.rs, src/lib.rs, src/page.rs, tests/page_0423.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0423
Done when (face 01): Done when: Valid published pre-lockout logs, including 0408 and 0423, load and verify without changing any log bytes.
Done when: A new work event always needs the matching lock. Replay still validates the post-lockout lifecycle and rejects inconsistent history.
Done when: A recorded valid override still loads after a book-Prime change. New overrides enforce current book authority or the documented person-only fallback.
Done when: cargo test --lib and cargo test --test page_0423 pass with regression cases for legacy replay and authority succession. Existing lock and byte-prefix tests keep passing.
Stop if: the fix needs paths outside the grant; a published page record would need changing; you cannot distinguish a new append from replay in the code path; historical authority rules need a policy decision beyond these jobs; or any existing guard in 05.01 would be weakened. Name the finding and the evidence. Do not seed a real book identity or work around a refused live authority check. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0423/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0423.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0423 02 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0423.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
