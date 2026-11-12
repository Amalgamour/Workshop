# Recording note (Prima)

This is a copy of Tester's results file, recorded into the repo on
2026-11-11 at about 7:30 PM EST so it is on the branch for the Director
to review. The original is at `/workspace/workshop-build/scratch/r23-r25-six-tests.md`.
Tester's words below were not edited. This is **not a ruling**.

The working-path picks taken from these results are in
[WORKING-PATH-SIX-TESTS.md](WORKING-PATH-SIX-TESTS.md) (D344–D348).

---

# R23-R25 lineage: the six scratch-clone tests (results)

Lane: TESTER. Results only. Not law, not a trial verdict, nothing seated.
Made: 2026-11-11, about 7:25 PM EST (America/Toronto).
Source of the tests: docs/design/R23-R25-lineage.md, "Recommended next tests".

Where it ran: throwaway clones under /tmp only (git clone --no-local of the shared repo; fresh clones of publish and GitHub for test 5). The shared repo /workspace/workshop-build/repo was only read (git show, ls-tree, cat-file, merge-base). No edit, commit, seat, un-seat, push or merge was made in any real repo. This file is outside the git repo.

Repo heads seen (the shared repo moved while the tests ran; other lanes were committing):
- start: 6c57f86 (baseline --check: exit 0, "seats 26", "48 findings, 0 errors").
- KERNEL pass 12 (84d6bd9, Q67-Q69 builder change) landed during the run. Tests 1, 2, 3 were first run on pre-pass-12 heads (1012df5, 2a7cd48, 51298eb), then all three were RE-RUN at 37d5e18 (includes pass 12). Results were the same. The numbers below for tests 1-3 are from the 37d5e18 re-run unless marked.
- Test 4 ran at 25a7a6f (includes pass 12). Test 6 ran at 01b5672 (includes pass 12); its --check: exit 0, seats 26, 48 findings, 0 errors.
- crates/ had no change from 6c57f86 to 37d5e18 (git diff --stat empty), so the seqaddr binary built from the clone (/tmp/sqtarget/debug/seqaddr) is the current core.
- Publish clone (/tmp/pub, branch build): 2d6562e3. GitHub: origin of the publish folder is https://github.com/Amalgamour/Workshop.git; branch prima/build cloned fine (/tmp/gh): 4792ffdd. Neither clone is shallow.

---

## Short version (plain words)

| # | Test | Result | Original finding |
|---|------|--------|------------------|
| 1 | In-place counter re-seat (F1) | Clean build, exit 0, seats 26, no unseat line. The old blob is gone from face 00 and from the book. | CONFIRMED (also after pass 12) |
| 2 | Two seated packs (F4) | 05.03 seats clean (seats 27). Replay and resolve show 05.01, 05.02, 05.03 all "closed". Nothing says which is current. | CONFIRMED |
| 3 | 00.CC dry run (F7, F8) | Bare 00.01 refused ("a 00 counter may not be seated"). 00.01.draft builds CLEAN once face 00 lists it. But the core then refuses the whole 00.00.00 book, and every resolve fails. | CONFIRMED and SHARPENED: new hole (builder writes a book the core cannot read) |
| 4 | Fingerprint drift (F9) | A 00.01.draft naming the wrong prior blob, and then an all-zero blob, both build clean. No code anywhere reads "fingerprint". | CONFIRMED: R25's compare has no implementation |
| 5 | Lineage open test (F3) | 5 distinct commit ids, 50 cites in 19 of 22 seated 05 files. Every one fails in publish AND GitHub ("Not a valid object name", exit 128). All pass locally. | CONFIRMED and WIDENED (not only fae009a) |
| 6 | Stale-pack sweep (F2) | 11 seated 05.02 packs. 6 cards already done (5 of them done BEFORE the packs were seated), 5 with broken numbers or paths, 1 card that tells you to edit a seated face, several blocks narrowed by R23/R25. | CONFIRMED and SHARPENED: packs were seated already stale |

Biggest new things:
1. Test 3: the builder's --check passes a book that the core's replay rejects (A4.4). The whole 00.00.00 book becomes unreadable to the core, so resolve fails for every address in every book (even 10.11.21.1001.01). Only the core's repo_books test catches it; --check does not.
2. Test 3: F7 is real in numbers. The snapshot names face 00 blob 0430347c..., but the face 00 committed with it is 14ce04b8.... The snapshot never matches any face 00 that lived beside it.
3. Test 6: the TRIAL-K3 fix list (w01) was finished by 7b08cbf, which is an ancestor of the commit that seated the packs (679d49e). The packs were trialed and seated with w01 already done.
4. Test 6: 0052.05.02 w02 tells the next agent to fill holes in 0052.04.draft.md. That file does not exist. 0052.04 was seated (8ba452d) after the pack was seated. Following the card would edit a seated face.

---

## Test 1. In-place counter re-seat (F1)

What I ran (clone /tmp/r1 at 37d5e18; first run /tmp/t1 at 1012df5 gave the same result):
1. Appended a forged card w99 to the seated kernel/samples/10.11.21/10.11.21.0013.05.02.md. Committed.
   - old blob 24a27e08bfb78ff75b1f7a2b91e82e2956a1163f (the real seat, trial docs/trial/kernel-trial-7.md)
   - new blob d995fa38d4ec9590b53a6b7ecada6c5fc478df09
2. Wrote docs/trial/forged-r1.md with a PASS list line "- `10.11.21.0013.05.02` (blob `d995fa38...`)". Committed alone (the builder requires the adding commit to touch only docs/trial/ and kernel/QUESTIONS.md, trialOrigin). Trial blob 7d7aea62afb35cc9646fa7b07c68b1fe6104b787 (first run: 452cf72683a2a6239c535eeb3328829b7d2415db).
3. Replaced the seat-05.02 line on 10.11.21.0013.00.draft.md with the forged trial and the new blob, staged it, ran node kernel/build.mjs (write), committed face 00 + books.
4. node kernel/build.mjs --check.

Note: in the first run the write failed until face 00 was staged: "face 00 ... is blob 00172ac1... in git (index), not the bytes on disk 057304f9...; face 00 carries seat records, so it must be committed or staged exactly as read". That is the Q62 rule, not a refusal of the re-seat.

Result:
- write_exit=0, check_exit=0, "seats 26", "48 findings, 0 errors". Findings identical to the baseline (diff of finding lines empty).
- unseat lines on face 00: 0. No error asked for one.
- Old blob 24a27e08... in face 00: 0 lines. In books/10.11.21.book: 0 lines. The book line now reads: "trial":"docs/trial/forged-r1.md blob ...; face blob d995fa38...".
- Where the old blob still appears (working tree): kernel/build.test.mjs (REAL_0502 constant), docs/BUILD-LOG.md, docs/trial/kernel-trial-7.md (its PASS list), kernel-trial-8/9/10.md. And in git history (git cat-file -t 24a27e08... = blob).

Verdict: CONFIRMED. The builder lets a seated counter be replaced at the same address with no record. Why: unseatChecks skips any address that is still seated, `if (now) continue;` (kernel/build.mjs:578 at 37d5e18), and never compares the current seat blob with past seat blobs. Pass 12 did not change this.

Hole: after the swap, kernel-trial-7.md still says 0013.05.02 passed at 24a27e08..., but nothing in face 00 or the book says that seat ended. A reader of the live registry cannot find the earlier seat (R2 "every such seat can be found and re-reviewed"); only a git walk can.

## Test 2. Two seated packs (F4)

What I ran (clone /tmp/r2 at 37d5e18; first run /tmp/t2 at 2a7cd48):
1. Added kernel/00.00.00/00.00.00.0051.05.03.md: a copy of 05.02 with `predecessor: 00.00.00.0051.05.02 (forged test 2)` and a w99 card. Blob f5c7ccb420cf8c784ec72efb672cca9891ce1f6f (first run b785ceb4d652f7e7485fb6f05c486e304a15c9ca).
2. Forged trial docs/trial/forged-r2.md (blob 796895e8b17fef1f901a44cdf9f2b66c73a3a3bd), own commit.
3. Face 00: `faces: ..., 05.03 seated` and `seat-05.03: approved-by: build-stage (R2); trial: docs/trial/forged-r2.md blob 796895e8...; blob: f5c7ccb4...`. Write, commit, --check.
4. seqaddr replay books/00.00.00.book; seqaddr resolve on ...0051.05, ...0051.05.02, ...0051.05.03 (--books books).

Result:
- write_exit=0, check_exit=0, "seats 27", "48 findings, 0 errors".
- replay, page 0051, face 05: counters 01 "closed", 02 "closed", 03 "closed"; claim null on all; slot "absent". Page state "live".
- resolve 00.00.00.0051.05: {"kind":"board","lines":[{"counter":1,"tail":"closed"},{"counter":2,"tail":"closed"},{"counter":3,"tail":"closed"}]}.
- resolve ...05.02 and ...05.03: each {"kind":"counter","tail":"closed"} with its body. Same shape, no order or status field.
- The only link from 05.03 to 05.02 is the free-text `predecessor:` I wrote inside the body. Neither builder nor core reads it (grep for predecessor/supersed in kernel/build.mjs: none). The core has no "current pack" logic (grep for supersed/latest/newest in crates/seqaddr-core/src: only state.rs:153 "newest text: the draft if there is one, else the seated body", which is about a face's draft vs seat, not counters).
- 05.01 (a note) is on the same board, also "closed", so "the highest counter" would not even work as a rule if a note were the newest counter.

Verdict: CONFIRMED. No output can tell which seated pack is the current best.

## Test 3. 00.CC dry run (F7, F8)

Clean clone /tmp/r3 at 37d5e18 (first run /tmp/t3 at 51298eb, same results). Baseline --check at 51298eb: exit 0, seats 26.
The 00.01 file holds one card: `fingerprint-before: 0430347c0f8499652d4566dd7d30cee5a3cf2f21` (the HEAD blob of 00.00.00.0051.00.draft.md).

| Step | --check exit | Errors (exact) |
|------|--------------|----------------|
| 3a bare 0051.00.01.md, face 00 not changed | 1 | (1) "registry lists [00.draft,01.draft,02.draft,04.draft,05.01,05.02,06.01.draft] but the page has [00.01,00.draft,...] (R10)"; (2) "00.00.00.0051.00.01.md: a 00 counter may not be seated: R22 allows only face 05 counters, and seating others is open (QUESTIONS Q35; ...); write it as 00.01.draft"; (3) "seated face has no seat-00.01: on the face 00 registry (R2: approved-by, trial, blob); write it as FF.draft" |
| 3b bare, face 00 lists `00.01 seated`, committed | 1 | errors (2) and (3) above. (Uncommitted, a third error: "face 00 ... is blob 0430347c... in git (HEAD), not the bytes on disk ...; face 00 carries seat records, so it must be committed exactly as read".) |
| 3b' bare, listed with a made-up state word `00.01 written` | 1 | registry mismatch ("[00.01.written,...] but the page has [00.01,...]") plus (2), (3) |
| 3c1 0051.00.01.draft.md, face 00 not changed | 1 | "registry lists [...] but the page has [00.01.draft,00.draft,...] (R10)" |
| 3c2 draft, listed `00.01 draft`, no why-00.01, committed | 1 | "a draft must say why (R5): the registry has no why-00.01:" |
| 3c3 draft, listed, with why-00.01, books rebuilt and committed | 0 | none. "seats 26", "48 findings, 0 errors" |

No forged seat for a bare 00.01 was tried: the "may not be seated" error comes from SEATABLE_COUNTERS = { '05': 'R22' } (kernel/build.mjs:49, check at :651) before any seat record is looked at, so a seat line cannot clear it.

F7 in numbers (3c3): the snapshot says fingerprint-before 0430347c..., but the face 00 committed with it (with the new `00.01 draft` and why-00.01 lines) is 14ce04b8fe1c3fc145fe118a93da563e95ecd281. Writing the snapshot forced a face 00 change, and that change is not in any snapshot. Also, because 0051's face 00 carries seat records, the registry edit has to be committed before --check passes, so the snapshot and the face 00 change it causes always land together.

The core (seqaddr built from the clone):
- On the 3c3 books: `seqaddr replay books/00.00.00.book` exit 1: {"error":"rejected","rule":"A4.4","detail":"face 00 on page 0051 is not a counted face; counters live on counted faces only (05, 06 and Policy.extra_counted)"}. (crates/seqaddr-core/src/state.rs:420.)
- `seqaddr resolve 00.00.00.0051.00.01 --books books` and `...00.01.draft`: exit 1, {"error":"corrupt","rule":"format 3.1","detail":"books/00.00.00.book: rejected (A4.4): face 00 on page 0051 is not a counted face; ..."}.
- `seqaddr resolve 10.11.21.1001.01 --books books` (an unrelated address in another book): the same "corrupt" error, exit 1. load_world loads every book, so one bad book stops all lookups.
- `cargo test -p seqaddr-core --test repo_books` on the 3c3 tree: FAILED, panicked "books/00.00.00.book: rejected (A4.4): face 00 on page 0051 is not a counted face ...". So the core's test catches it; the builder's --check does not.
- `seqaddr validate 00.00.00.0051.00.01`: ok true, face 0, counter 1, job "registry". The grammar parses it; the state rules refuse it.
- `seqaddr propose` (dry run) on the clean HEAD books, one op {"op":"put","addr":"00.00.00.0051.00.01"} and again with addr "...00.01.draft": both {"status":"rejected","reasons":[{"code":"rejected","rule":"A4.4","detail":"face 00 on page 0051 is not a counted face; ..."}]} (CLI exit 0; the refusal is in the JSON).

Verdict: F8 CONFIRMED (no address/state holds a write-once, not-seated 00.CC: bare is refused, only `draft` builds). F7 CONFIRMED with blobs. NEW HOLE: the builder accepts `FF.NN.draft` on face 00 and writes a book that the core rejects on replay. --check exit 0 is not proof the books are readable.

## Test 4. Fingerprint drift (F9)

Clone /tmp/t4 at 25a7a6f (includes pass 12).
1. Two harmless face 00 commits on 00.00.00.0051.00.draft.md (an HTML comment line each):
   - B0 = 0430347c0f8499652d4566dd7d30cee5a3cf2f21 (before)
   - B1 = b521febd5b0251192f8c789bfcb37bd4608e51cd (commit 8263b87)
   - B2 = ba67cf142fbbd66dc3ba43368403c328321e87f7 (commit 6f307c5, the true prior face 00)
2. Added 0051.00.01.draft.md with `fingerprint-before: 0430347c...` (B0: a real blob git holds, an older face 00, but NOT the face 00 just before the change). Listed `00.01 draft` and why-00.01 on face 00, committed, rebuilt books, committed.
3. --check: exit 0, "seats 26", "48 findings, 0 errors". Finding lines identical to the 51298eb baseline.
4. Variant 4b: changed fingerprint-before to 0000000000000000000000000000000000000000 (a blob git does not hold). Rebuilt, committed. --check exit 0, seats 26, 0 errors.
5. Core: replay of that book fails with the A4.4 refusal (as in test 3), so the core never gets as far as reading the claim.
6. Search: grep -rliI "fingerprint" kernel/build.mjs kernel/build.test.mjs crates/ app/ scripts/ found no file (exit 1). The word appears only in docs (docs/design/00-counter.md, R25 text).

Verdict: CONFIRMED. Nothing detects a wrong or made-up fingerprint. The "count and compare" step R25 asks for has no implementation in the builder, the core, the app or the scripts.

## Test 5. Lineage open test (F3)

Method: every 7-40 hex token in every seated 05 file under kernel/ (05.01 and 05.02, parked/ excluded) at the shared repo HEAD 3f305629, read with git show. 22 files. Each token typed with git cat-file -t in each copy. For commits: git merge-base --is-ancestor <id> HEAD (local on build, publish clone on build, GitHub clone on prima/build). 57 tokens: 50 commit cites, 7 blob cites. Script: /tmp/t5.py, raw output /tmp/t5.json.

Results by distinct commit:

| Cited id | Local (build) | Publish clone | GitHub prima/build | Same work there (exact subject match) | Cited in |
|----------|---------------|---------------|--------------------|---------------------------------------|----------|
| fae009a (kernel pass 4) | ancestor, exit 0 | "fatal: Not a valid object name fae009a", exit 128 | same, exit 128 | 013db63f5340bf23eebc0fa2711566c4b5f08a97 (is-ancestor in publish: exit 0) | predecessor: 0051-0057.05.02, axioms.05.02, 0012.05.02; sources:/body of 0051, 0052, 0053, 0055, 0056, 0057 05.01 |
| 8c8f780 (kernel pass 3) | ancestor | missing | missing | 7a9795c9c15bcc493f85e07b57fc0e6d1f68133b | predecessor: 0012.05.02, 0013.05.02; sources/body: 0051.05.01, 0055.05.01, 0013.05.01 |
| d37e532 (TRIAL-K3 commit) | ancestor | missing | missing | d5a19b75484ff5ce47baaad018ac1d8569ba5c08 | reason: lines of 0051-0057.05.02 and axioms.05.02; body of 0051, 0052, 0056, 0057 05.01 |
| 42ffbc9 (seat of 0056.01, 1001.01) | ancestor | missing | missing | 6322281b0ba47572b631b2e1663743f0e9d11b7b | predecessor: 0056.05.02, 1001.05.02; sources/body/reason: 0056.05.01, 0056.05.02, 1001.05.01 |
| ef28051 (kernel pass 2) | ancestor | missing | missing | 076d783eb45d5c5c7c6f1cc56e1e7d20dfbbe18f | predecessor: axioms.05.02 |

- 50 of 50 commit cites fail in publish and in GitHub. 0 fail locally.
- 19 of 22 seated 05 files carry at least one commit cite. The 3 with none: 00.00.00.0054.05.01, 00.00.axioms.05.01, 10.11.21.0012.05.01.
- The 7 blob cites (112c169c x3, 5415cef2 x3, 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d x1) resolve as blobs in all three copies. Blob cites survive; commit cites do not.
- Per-line detail (file:line, field, id, result) is in /tmp/t5.json; summary lines were printed as e.g. "00.00.00.0051.05.02.md:12 [predecessor] fae009a local=('commit', True) pub=('missing', None) gh=('missing', None)".

Verdict: CONFIRMED and WIDENED. It is not only fae009a: all five cited commits are unreachable in the published copies, and the cites sit in predecessor:, sources:, reason: and body text.

## Test 6. Stale-pack sweep (F2)

Read-only against clone /tmp/t6 at 01b5672 (--check exit 0, seats 26). 11 seated 05.02 packs. Every work card was listed (title, blocked-by, done) and checked. Hole counts are `grep -c '^why: 4.7'`; card counts are `## ` headings.

Timeline that matters: 7b08cbf (KERNEL pass 5, TRIAL-K3 fixes and the seat-guard tests) is an ancestor of 679d49e (pass 6 step 2, the 15 packs seated, "renamed .draft.md to .md (blobs unchanged)"); commit times 15:06 and 15:26 (-0600, so 4:06 and 4:26 PM EST). 8ba452d (pass 7 step 2, seats 0052.01 and 0052.04) came after the packs were seated.

A. Already done (done-test passes now, or the work was finished):

| Card | Evidence |
|------|----------|
| 0051.05.02 w01, 0052.05.02 w01, 0057.05.02 w01 (fix TRIAL-K3 findings) | docs/BUILD-LOG.md:180: "w01 in the seated 05.02 packs of 0051, 0052, 0056, 0057 and 00.00.axioms (the TRIAL-K3 fix list) was done by 7b08cbf; its done test passes. ... Close these in each page's next 05 draft counter." Done BEFORE the seat (7b08cbf is an ancestor of 679d49e). No next counter was ever opened. |
| 0056.05.02 w01 (harden the seat guard; blocked-by Q34) | kernel/build.test.mjs has every test the done line names: :101 "a face 00 seated with no seat-00 record is refused (H1)", :131 "a seat citing a trial file that does not exist is refused (H2)", :134 "a real trial that did not pass the face", :141/:144 director seats without a valid ruling, :163 "retiring a seated face with no unseat record is refused (H7)". First added in 7b08cbf, before the seat. Done while still marked blocked by Q34. |
| 00.00.axioms.05.02 w01 (check C3.2 on the axioms) | kernel/build.test.mjs:152 "C3.2: an axioms 01 card with no 04 card is refused (H3)", first added in 7b08cbf, before the seat. |
| 0056.05.02 w02 (keep 0056.01 as trialed) | git hash-object 0056.01.md = 112c169ccd06d54c6d9ab607fee6c2d16004cc62 (starts 112c169c), --check exit 0. A standing guard; its test passes now. |
| 10.11.21.1001.05.02 w01 (keep 1001.01 as trialed) | git hash-object 1001.01.md = 5415cef2dd0a37f3c2ba4c9b6d2652262f0ef82d, --check exit 0. Same kind. |
| 0052.05.02 w06 / w07 (trial and seat 0052.01, .02, .04) | PARTLY done: 0052.01 and 0052.04 passed TRIAL-K5 and were seated in 8ba452d. 0052.02 is still draft. |

B. Already broken (numbers, paths or claims no longer match):

| Card | Says | HEAD |
|------|------|------|
| 0051.05.02 w02 | "fill the 20 `why: 4.7` holes", done "28 cards on the face" | 17 holes, 30 cards; 0 of the 17 remaining hole cards name a Q or O id, so the done-test fails either way |
| 0052.05.02 w02 | "fill the 13 holes on 00.00.00.0052.04", done greps kernel/00.00.00/00.00.00.0052.04.draft.md | That file does not exist. 0052.04 is seated as 0052.04.md (8ba452d, after the pack). The grep errors. Doing the work means editing a seated face, which needs FF.draft and a new trial (R2, axiom 9). (13 holes / 17 cards still match the seated face.) |
| 0054.05.02 w03 | "fill the 2 holes", 3 cards | 1 hole, 3 cards. Half done; the remaining hole names no question, so the done-test still fails |
| 0055.05.02 w03 | "fill the 10 holes", 12 cards | 7 holes, 12 cards. Partly done; title count stale |
| 0056.05.02 w04 | "fill the 2 holes", 4 cards | 1 hole, 4 cards. Partly done |
| 0057.05.02 w04 | "fill the 7 holes", "19 cards on the face" | 4 holes, 21 cards. Count broken |

Still accurate (for contrast): 0053.05.02 w03 (5 holes, 6 cards: matches). Not done and correctly described: 0012.05.02 w02 (the real-books test crates/compute/tests/http.rs brands_and_cards_on_real_books checks bob only, not cats), 0013.05.02 w02 and 1001.05.02 w03 (the "what is my name" test, crates/compute/tests/ask.rs bob_test_end_to_end, runs on the fixture kernel_dir, crates/compute/tests/common/mod.rs:30-33, not on a copy of books/).

C. Blocks touched by a ruling (precise):

| Block | Status | Cards |
|-------|--------|-------|
| Q51 / QD05 | ANSWERED by R25 (kernel/QUESTIONS.md marks it). No seated 05 card lists Q51 in blocked-by (grep). Only the parked door packs did (BUILD-LOG). | none seated |
| Q34 (where a seat record lives) | NOT closed. R25 says "Changes are still recorded onto 00", which keeps option B (face 00 registry) and rules out moving seats off 00, but does not say whether the book entry also carries it (option C). Narrowed, not answered. The block was also never real in practice: seats were written while Q34 was open (679d49e, 8ba452d), and 0056 w01 was completed while "blocked" by it. | 0051 w08, 0052 w03/w07, 0053 w05, 0054 w05, 0055 w06, 0056 w01/w07, 0057 w07, axioms w06, 0012 w05, 0013 w05, 1001 w02 |
| Q41 (is a counted 05 seated?) | Not marked answered. Its entry still says "Applied R22 (kernel pass 5), awaiting Director confirmation". R23 reads "This confirms R22: face 05 is seated" and R24 describes the 05.CC climb, so the core of Q41 looks answered; which of options A/B/C is still not said. | blocked-by on 0052 w05, 0057 w05; open: on 0053, 0057, 0012 |
| Q43 (where a pack lives) | Not marked answered. R22-R24 all put the pack on the page's face 05 (05.CC), which reads as Q43's first option. | 0057 w03 |
| Q30, Q28, Q33, Q29, Q35 | Have Tester working paths (Q30/QD13, QD09, QD02, QD10, Q35) recorded by Prima. Working paths are not rulings, so these cards stay blocked. | 0051 w03/w04, 0052 w03, 0054 w01, 0055 w01, axioms w02, 0012 w01/w05 |

Not measured: 0052 w03 and 1001 w02 (POST /check.seq output) and the O-item cards (O7, O16, O20, O25, O27, O38-O41); I did not run the compute server.

Verdict: CONFIRMED and SHARPENED. The packs were not only overtaken later: five w01-type cards were done before the packs were trialed and seated. R23 says the seated pack is "the best version", but no seated pack is current.

---

## What should change in the working path (recommendations only, not law)

1. F1 / test 1: keep the working pick "an update is a new counter; never replace a seated counter in place". Ask the builder lane to make --check refuse it: a seated counter whose seat blob differs from any earlier seat blob at the same address (from the face 00 and books/ history walk it already does) is an error unless a new counter is used. Today nothing stops it.
2. F4 / test 2: the `supersedes:` pick needs a reader. Today predecessor: is free text that no code reads. If supersedes: is adopted, both the builder (check it names a seated counter on the same page) and the core (expose "current" on resolve of ...05) must read it. Also keep notes (05.01) out of the "which pack is current" rule.
3. F7/F8 / test 3: before any 00.CC is written, someone must decide its address with the core in mind. As things stand, a 00.NN.draft passes the builder and breaks the whole book for the core. Two small guards (builder lane, not law): (a) --check should replay each written book with the core rules, or at least refuse a counter on a face the core does not count (00, 01-04, 08); (b) the repo_books core test should be part of the pre-commit set. The listing cascade (F7) is real: if the face list stays written (QD03 working path keeps it checked), a 00.CC must either be left out of `faces:` or its fingerprint must be defined to ignore that one line.
4. F9 / test 4: define "fingerprint" as the git blob of face 00 at the parent of the commit that adds the 00.CC, and make the compare a builder check: fingerprint-before must equal that blob. Then git and the 00.CC cannot silently disagree (working pick 5 in the lineage note: a mismatch halts).
5. F3 / test 5: seated packs cannot be edited, so the fix is the next counter (05.03 per page): cite lineage by address plus blob (or trial path plus blob), never by commit id, as Q53 already did for trials. Map for that counter: fae009a -> 013db63f, 8c8f780 -> 7a9795c9, d37e532 -> d5a19b75, 42ffbc9 -> 6322281b, ef28051 -> 076d783e (publish/GitHub ids today; they may change at the next filter-branch, which is why blobs are better).
6. F2 / test 6: the R24 climb should start now. Each page's next 05 counter closes the done w01 cards, fixes the broken counts, and re-points 0052 w02 at a 0052.04.draft re-trial. A trial of a pack should run its mechanical done-tests (hole and card counts, file paths) before the seat, so a pack is not seated already stale.
7. For Prima's question records: Q41 and Q43 look answered in substance by R23/R24 but are not marked; Q34 is narrowed by R25, not closed. These are for Matthew to confirm, not for us to mark.

Nothing here was seated, pushed, merged, or written into the shared repo. All forged trials and seat lines exist only in /tmp clones (t0-t4, t6, r1-r3, pub, gh), which can be deleted.
