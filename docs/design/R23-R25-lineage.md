# R23, R24, R25 against axiom 6 (lineage)

**DRAFT.** Research notes from Tester. These are not law, not a design, and not a trial verdict on any face. Nothing was seated, pushed, or merged. Matthew is the only one who approves a ruling.

Lane: TESTER. Made: 2026-11-11, about 7:15 PM EST (America/Toronto).
Repo: `/workspace/workshop-build/repo`, branch `build`. The review was read at HEAD `9718fd0` (TRIAL-K10). By the time this note was filed, HEAD was `faf1454` (Designer's 00.counter draft, and Q51 marked answered by R25). Those later commits do not change the findings.

Key sources: `docs/spec/DIRECTOR-RULINGS.md` (R23-R25), `docs/spec/Axioms.md` (axiom 6), `docs/spec/seqAddr.md`, `docs/design/00-counter.md` (Designer DRAFT, not settled), kernel face 00 and seated 05 packs, `kernel/build.mjs`, `kernel/QUESTIONS.md`, recent trials (especially TRIAL-K10).

`--check` was run read-only: exit 0, 26 seats, 48 findings, 0 errors. No seated file and no kernel file was changed.

---

## Short version (plain words)

1. R24 says the past is not rewritten, and that a later update starts at 05.07. It does not say where the reseated pack is stored. The builder lets new words replace a seated face at the same address and leaves no trace on face 00. That second path rewrites the past, which axiom 6 forbids.
2. The seated packs are already out of date, and no 05.03 was ever started. The climb R23 and R24 describe has not been used.
3. The seated packs point back by git commit id. Those ids are not in the published history, so the line back cannot be opened there.
4. To the core and the compute, a seated pack is a finished task. It cannot be handed to a model to run, and nothing marks which seated pack is the current best.
5. R25 says face 00 is not seated the usual way. The builder still knows only two states for it: draft, or seated by trial. So every face 00, and every page stamp, stays draft, with a reason that no longer explains why.
6. Designer's 00.counter draft cannot be written as things stand. Writing a 00.counter changes face 00's face list, so every snapshot is itself a change to face 00. The builder, the grammar and the core all refuse or misread a write-once, not-seated 00.counter.
7. "Fingerprint" is not defined. The books are rebuilt from scratch on every build, so they do not keep face 00's past. Only git does. A 00.counter would be a second record of the same past, and nothing says which one wins if they disagree.

---

## Findings

Severity: blocker / major / minor / info. "Known" means it is already tracked. "New" means no existing entry was found.

### R23 and R24: the 05 climb

**F1. major, new (sharpens QD01).** R24 says we do not rewrite the seated pack: we start 05.07 from that pack, then reseat an update. Axiom 6: "The past is not rewritten ... add the new step after it." (`DIRECTOR-RULINGS.md:95-97`; `Axioms.md:23`)

Two readings exist. (a) The update is a new counter, for example 05.07, seated beside 05.02, and 05.02 is not touched. (b) "05" is one seated slot, and the update replaces it at the same address. Only (a) keeps the line.

The builder allows (b) and records nothing: `unseatChecks` (`kernel/build.mjs:556-557`) skips any address that is still seated (`if (now) continue;`) and does not compare blobs. Replacing a seated `05.02` with new bytes and a new `seat-05.02:` line builds clean. No `unseat-05.02:` is written. The old seat line on face 00 is simply overwritten. TRIAL-K10 did this in a test: it re-seated `0013.01` at a new blob (`docs/trial/kernel-trial-10.md:142`).

TRIAL-K10 and Q67 read R24 as "re-seats are normal." For counters, that reading points the other way from R24's "start 05.07."

seqAddr has a `retired` state, but only on faces without counters (`seqAddr.md:138,287`). A replaced pack cannot be marked replaced.

Under reading (b), or for any non-counted face (01, 04), the only record of the past is git history. R2's "every such seat can be found and re-reviewed later" then depends on the git walks that TRIAL-K10 finding 1 showed can be fooled.

**F2. major, new.** The seated packs describe work that is already done or has changed, and nobody started a new counter (05.03) while the work moved on. Axiom 6: "If the trail is stale, raise it."

On seated `00.00.00.0051.05.02` (one commit, never changed after seating):

- w01 is "fix TRIAL-K3 findings 5, 6, 9" - later passes already did that work.
- w02 is "fill the 20 `why: 4.7` holes" with done-test "28 cards on the face." Today `0051.04.draft.md` has 17 `why: 4.7` lines and 30 cards, after WHY-GAPS and WHY-FIX.
- w08 is `blocked-by: Q34` (where a seat record lives). R25 answers the closely related Q51 / QD05: seat records may still be written onto 00. Q34 itself (book entry, face 00, or both) is not fully closed. The pack's block may still be stale.

The 05.01 note still says "20 of the 28 cards on 0051.04 still hold `why: 4.7`." That is no longer true.

R23 says "during a pass, the pack (05.02) may change to cover the 3-5 fixes." Later work ran from WHY-GAPS, BUILD-LOG and QUESTIONS, not from a climbed 05.NN. No `05.03` file exists under `kernel/`. The R24 climb has never been used.

**F3. major, new.** The seated packs link to their past by commit id, and those commits are not in the published history. The line back cannot be opened there.

`0051.05.02` through `0055.05.02` say `predecessor: fae009a (kernel pass 4)`. The 05.01 notes cite the same kind of commit ids. In `/workspace/workshop-build/publish`, that work is commit `013db63f`. `git merge-base --is-ancestor fae009a build` is not an ancestor, and a fresh clone of publish or GitHub will not have `fae009a`.

The builder already moved trial cites from commit ids to blobs for this reason (Q53, `build.mjs:183-185`). The pack lineage fields were not moved. Axiom 8: "A connection that cannot be opened is missing (`7.8`)." Seated packs cannot be edited (axiom 6, R24), so a fix would have to be a new counter.

**F4. major, partly known (Q41, QD01; the run-time effect is new).** The machine reads a seated pack as a finished task. It cannot hand it to a model to run, and it cannot tell the best pack from an older one.

In the core, a bare counter is `Closed`. `Closed` has no next step. `seqaddr replay` reports every seated 05.01 and 05.02 as `closed`. `resolve 00.00.00.0051.05` returns a board of two closed lines. Compute claims start from the `pack` tail, so a seated pack can never be claimed. R23 seats the pack "so it solves the issues models run into before they run it."

After R24's climb, 05.02 and 05.07 would both be bare and closed. No field, tail or rule picks the current best. R24 says in words that the older seated 05 stays in the line; the machine has no way to follow that.

Also, 05.01 is a "What We Learned" note (`type: note`). R24 counts "05.01-06" as the pack's climb. With a note at 05.01, "which counter is the pack" is already unclear.

**F5. minor, sharpens Q40 / QD08.** Seating a work pack is what makes a page "live" to the core, even when none of its law is seated. Replay reports pages 0051, 0053, 0054, 0055 and 0057 as `live`, yet their only seated faces are 05.01/05.02, and their stamps say `state: draft`. Q40 already covers stamp-draft vs derived-live for 0056 and 1001. This is a further case: the R22 pack alone flips the page.

### R25: face 00 and the 00.counter

**F6. major, new.** The builder still offers face 00 only two states: a draft, or seated by trial. R25 says face 00 is not seated that way. So every face 00 stays a draft forever, and so does every page stamp.

`build.mjs:4` still says rulings applied are R1-R22. The `seat-00` path is still live (`:179-181`, `:592`, `:626-629`): every face with no tail needs a seat record. All 15 face 00 files are `.draft` with `state: draft`. Their `why-draft:` still says they need a new trial (axiom 9, R2). After R25 that reason no longer explains why they are drafts.

There is no state for "the live registry root, recorded on, not seated." R12 puts page state in the face 00 stamp. Together with F5, the written state (draft) and the derived state (live) can now never agree.

**F7. major, new (hostile check of Designer's 00-counter draft).** Writing a 00.counter is itself a change to face 00, because face 00 must list every face on the page.

The builder requires the registry `faces:` line to equal the files on the page (`build.mjs:615-617`). A new `...0051.00.01` file is parsed as face 00, counter 01, so face 00 must list it. The draft's steps are: snapshot face 00, write a 00.CC, then change face 00. Step 2 already changes face 00 through its registry. The snapshot is never "just before the change" (R25). Either it misses the registry edit, or that edit needs its own snapshot, and so on.

The draft covers the seating cascade (QD66). This listing cascade happens even if a 00.CC is never seated. It depends on QD03 and QD04 (is the face list written, and is face 00 in it).

**F8. major, new (hostile check of the same draft).** No address or state can hold a "write-once, not seated" 00.counter today.

A bare `00.NN` is treated as seated and needs `seat-00.NN:`, then is refused, because only face 05 counters may be seated (`SEATABLE_COUNTERS`, `build.mjs:49,628`). The only tails are workflow tails (`draft`, `pack`, `open`, `return`, `review`). So QD66 option A (not seated, write-once evidence) ends up as permanent drafts, which axiom 9 reads as untrusted.

The core refuses counters on face 00: "counters live on counted faces only (05, 06 and Policy.extra_counted)." `resolve ...0051.00.01` returns "no counter." seqAddr 5.7 says faces 05 and 06 are always counted. Face 00 as a counted face is a new case the spec does not list.

**F9. major, new.** "Fingerprint" is not defined, and the book does not keep face 00's past. Git does. A 00.counter would be a second record of something git already holds, and nothing says which wins.

Every seat is pinned to the git blob of the Markdown source (`blobOf`, `build.mjs:174-177`), not to anything in the book. R3: "the book is the real stored copy." `format.md:60`: "A book is an append-only log of approved writes." But the builder rewrites each `books/*.book` whole on every build (`writeFileSync`, `build.mjs:818`), with a fixed time and author, and entry numbers starting again from 1 (`:780`). Earlier face 00 versions are not in the book.

So the book is not append-only and is not the stored copy of the past; git history is. Face 00's line is already walked from git. A 00.CC `fingerprint-before` would be a second live claim about the same past. Axiom 1: "Two live claims with no lawful connection: halt."

**F10. minor, new.** Door pages have a face 00 that changes too, but R10 says 0000.00 is the only spot on a door page. The builder's door rule only forbids faces whose number is not 00 (`build.mjs:622`), so a `0000.00.01` would slip past it, yet R10's words forbid it. This is the R25 version of Q42 (where a door's 05 pack goes). The kernel has five doors: `00.00.00`, `10.00.00`, `10.11.00`, `10.11.21`, and the axioms' own face 00 (an address the core cannot parse: known as Q28 / QD09).

**F11. minor, sharpens QD16.** Face 00 changes far more often than a pack does. In about one day of this build, some face 00 files were touched 8 to 10 times. With one 00.CC per change, plus F7's extra listing change, a busy page could reach the 98-counter cap (R9) in days, not months. QD16 ("what happens after 98") is already open; this makes it urgent for face 00 first.

**F12. minor, new (hostile check of the 00-counter draft).** The draft writes the snapshot before the change, and says not to rewrite the 00.CC face. If the change is then refused, a write-once record of a change that never happened stays forever. Axiom 6 says "a change that is not recorded did not happen." The reverse case - recorded but not made - has no rule. It needs a way to void a snapshot that stays visible in the line.

**F13. info.** The Director's words lean toward one list ("a 2nd 00.counter Where its a list of the previous fingerprint"). The draft recommends many write-once faces and calls one list "not recommended." QD67 already frames both. This is only a lean, not an answer. Prima should keep QD67 neutral when it is shown to Matthew.

**F14. info.** The 00-counter draft gives 00.CC `address:` and `prior:` fields that could be read as a stamp, and only face 00 carries a stamp (R12; CONFLICTS D8). If these are meant as card fields, the draft should say so.

### Links to recent trials

**F15. info.** TRIAL-K10 finding 1's attack needs a face seated twice at the same address. Under reading (a) of F1, counters never do that, so for 05 the attack goes away. For 01 and 04 faces it stays. Q67 is already a builder-lane question.

**F16. info, known (K10 finding 4, Q69).** A builder test uses `R23` as a fake ruling. R23 is now real, so the suite is 66/67 at HEAD.

**F17. info.** The seqpage round-trip test no longer checks that the real books round-trip (it is loosened on purpose). Today all 14 pages in `books/*.book` do round-trip, so it could be tightened. The axioms book is not covered by that glob (R6 storage is still `7`).

---

## What still holds

- No seated face file has been edited after seating. Each of the 26 seated files has exactly one commit, the rename from `.draft`. As practised, axiom 6 holds for seated bytes.
- `--check` is clean at HEAD (26 seats, 0 errors).
- R9 is applied the same way in the builder and the core: counters 01-98, no `FF.00` or `FF.99`.
- The R3 round trip holds for all 14 pages in `books/*.book`.

---

## Questions for Prima to record (working recommendations, not rulings)

These are new or sharper. They are not answered. The picks below are a working path only, for Matthew to review.

1. **When a page's 05 is reseated as an update, does the new pack go on a new counter, or replace the same address?** (sharper QD01, from F1.) Working pick: a new counter (05.07 beside 05.02). Nothing at the old address is replaced. That is what R24's "start 05.07" and axiom 6 already say. The builder should not allow a silent in-place replace.

2. **When two seated packs sit on one page, how does a reader know which is the current best?** (new, from F4.) Working pick: a `supersedes:` (or `prior:`) field on the newer pack, pointing at the older one. That is write-once on the new face. It does not rewrite the old pack. A reader walks those links to the pack that nothing later supersedes. I would not mark the old pack `retired` until counters are allowed that state.

3. **What state does face 00 have once R25 says it is not seated the usual way?** (new, from F6.) Working pick: face 00 is the live registry. It is neither a draft that "needs a trial" nor a trial-seated face. The stamp `state:` stays the page's state (QD04's current path), and is separate from face 00's own standing. The `why-draft:` line that says "needs a new trial" should not be used for this.

4. **What is face 00's "fingerprint"?** (new, from F9.) Working pick: the git blob of the face 00 file. That is already what every seat record uses. Name it so. Do not pretend the book holds this today; it does not.

5. **If the 00.counter and git history disagree about face 00's past, which governs?** (new, from F9.) Working pick: neither silently wins. They must agree. A mismatch is a defect: halt and raise it (axiom 1).

6. **Where does a door page's 00.counter go, since R10 says 0000.00 is the only spot?** (new, from F10; cousin of Q42.) Working pick: allow `0000.00.CC` on the door page, as an exception to R10, the way R25 already makes face 00 special. The line has to live next to the face 00 it measures. Moving it to another page would break that. This does not also let a door hold a 05 pack (Q42 stays open).

F7, F8, F12 and F3 are builder or design-lane problems first. They become Director questions only if a lane cannot solve them without a choice of law. F7 is tied to QD03 (the face list in face 00), which is the next question in Prima's ordered list.

---

## Recommended next tests (scratch clones only; no seats)

1. **In-place counter re-seat (F1).** In a fresh clone, change a seated `05.02`, write a forged docs-only trial for the new blob, update `seat-05.02:`, and run `--check`. Expect a clean build with no `unseat-05.02:`, as K10 showed for `0013.01`. Then see whether anything on face 00 or in the book still names the old blob.
2. **Two seated packs (F4).** In a clone, add a seated `05.03` (forged trial) beside `05.02`. Run `seqaddr replay` / `resolve ...05` and see whether any output can tell which one is current.
3. **00.CC dry run (F7, F8).** In a clone, add `...0051.00.01.md` (bare) and `...0051.00.01.draft.md` in turn. Record the builder errors, the registry-mismatch error, and what the core does with `put ...0051.00.01`. Do not write a builder fix.
4. **Fingerprint drift (F9).** In a clone, make two face 00 commits and a hand-made 00.CC whose `fingerprint-before` names the wrong blob. Confirm that nothing detects it today.
5. **Lineage open test (F3).** For every `predecessor:` or commit cite on a seated 05 face, check `git merge-base --is-ancestor` in fresh clones of publish and GitHub, and list each one that fails.
6. **Stale-pack sweep (F2).** For each seated 05.02 work card, check its `done:` test against HEAD and list the ones already done, already broken, or whose `blocked-by` was answered by a ruling.

These tests were not run. They wait for a concrete assignment.
