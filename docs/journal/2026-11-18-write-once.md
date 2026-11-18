# Dev journal: write once (page 90.20.00.0001)

date: Wed 18 Nov 2026. All times are EST.
written by: Prima, because Matthew asked (t303u): "Make sure you are writing the spec documentation to go with the work. So I can understand what we did and have the why's in there. It's almost a dev journal so I or a future model have access."
what it covers: the five passes that built "write once", 05.01 to 05.05, in order, with the why for each step.
the spec (what the code does now): docs/spec/WRITE-ONCE.md.

How to read the labels:
- A **pass** is one round of work: Prima writes the job, a builder does it, Tester checks it, Prima signs it off. (Side label: a 05.NN card on the page.)
- A **job** is one line of a pass, w01 to w04. At sign-off each job is *accepted* or *carried* (moved to the next pass).
- **WF** is our workflow tool (the `wf` kit). It keeps the page log and refuses steps out of order.
- **7** means "not complete yet" (axiom 7). Here it marks a choice that waits for Matthew.
- A line in square brackets is a side label for engineers.

---

## The short version

- **What we built:** a write sent twice is saved once, even if the compute restarts in between.
- **How:** 5 passes. 4 passed. 1 failed (05.04), and 1 fix-up pass (05.05) fixed it.
- **Tests:** 291 pass.
- **Time:** the page ran from 12:24 PM to 1:38 PM EST, about 74 minutes.
- **Usage:** about 4 points, from about 54.7% to 58% of the weekly limit. (Prima's reading of the usage meter. It is not in the page log.)
- **Where it is:** merged into the local `build` branch as 2166b46. Not pushed. Pushing needs Matthew's OK.
- **Waiting on Matthew:** the draft choices for his K4 ruling (spec section 6), and the risk notes (spec section 5).

---

## Before the passes: why write once came first

**Matthew asked for it (t284u).** He asked for a project-lead task: build the core of Workshop using WF, test how well WF works while doing it, and design a benchmark.

**Prima's plan** (docs/design/PLAN-2026-11-18-core-via-wf.md, committed 12:13 PM EST as 957d348) picked write once. The plan's reasons:
1. Matthew already ruled it. R37 item 2: "a delivery id can't change its content."
2. It fixes the one hole in the core marked "fails today": a lost reply makes the tool resend, and the change is written twice (B6).
3. The "first proof" of the core needs it (Part F, test 9 is this exact case).
4. It is small and easy to test.
5. The bigger first step (closing the direct-write door) needs a choice about computer accounts, and that choice is Matthew's.

The alternative was a read-only history view (face 09). It was lower risk but fixes no bug.

**Matthew said yes (t285u, about 12:20 PM EST).** His words, kept in full in docs/review/DIRECTOR-WORDS-t285u.md. The parts that set this work:
- Q1, write once first: "yes, I agree".
- Q2, the grant: "Yes I agree". The builders may change only `crates/compute/`, `crates/seqaddr-core/`, `docs/CONTRACT.md` and `docs/BUILD-LOG.md`, on a branch called `core-wf`. Prima merges into `build`. Nothing is pushed without his OK.
- Q3, use WF as it is and write down its gaps: "Yes, this is about getting WF ready for next week with the usage we have."

**The page was opened at 12:24 PM EST.** Prima entered Matthew's Q2 yes as the grant, on his behalf. He did not type it into WF himself. [page log entries 1-4]

**Codex reviewed the plan (t292u, pasted 12:36 PM EST).** This came in while pass 05.01 was already being built. Recorded word for word in docs/review/CODEX-PLAN-REVIEW-t292u.md. What we took from it:
- **A higher bar for "done":** the feature is done only when a committed write whose reply was lost can be resent after a restart without a second edit.
- **The order:** check the token first, then that writer's receipt, then the normal rules.
- **The receipt goes with the edit:** a crash must not leave a saved change without its receipt.
- **Real tests:** each new test must fail on the old code, for the expected reason. Tests that guard old behaviour may pass on both.
- **Independent audits:** Prima writes her own verdict before she reads Tester's.
- **A written approval record** of what Matthew allowed. Prima added it as a page note at 12:36 PM EST. [entry 9]

Because of Codex, the restart work moved forward from pass 05.03 to 05.02. The plan's 05.02 job (refuse other content) moved to 05.03.

**Preflight of WF (Codex asked for it).** Prima checked the pinned WF tool before using it. The lock is taken before reading page state. WF refuses "passed" when the check failed. A job marked "need" or "blocked" could still be signed off as passed with a note. So Prima set a rule for herself: never sign off a pass as passed while any job is "need" or "blocked". [entry 9]

---

## Pass 05.01: the id, and resend in one session

**Time:** 12:24 to 12:39 PM EST. **Builder:** b11. **Result:** passed. [commit f363e28]

**What it asked:** `/propose` takes an optional id on each op. The id is saved on the book line. The same id, writer and content gives back the first answer and saves nothing new. Each new test fails on the old code (f3ed48d). [pack: /tmp/core-p01.txt]

**Why this first:** it is the smallest useful step. It proves the idea in one session before restarts make it harder.

**What the builder did:**
- Added the `delivery_id` field to the request and to the book line.
- Kept an in-memory list of writer plus id, pointing to the first answer.
- Wrote a test. It sends one write twice with one id: the book grows by one line, and both replies match. A write with no id still saves every time, as before.
- On the old code, that test failed as expected: the resend saved a second line (entries 9 and 10).
- 279 tests passed.

**Prima's audit (12:40 PM EST, before reading Tester):** pass. Four notes for later: mixed ids were silently treated as no id; only 200 answers were remembered; the receipt sits on the book line, so it is saved with the edit; the token is checked first. [scratch/prima-audit/05.01.txt]

**What Tester found:** pass. Hostile tries: 16 copies sent at once saved once; trimmed ids and the `delivery-id` spelling match; case matters; a 200,000-character id was accepted (no cap yet). Known gaps, as planned: other content was still saved again, and a restart forgot every id. [entry 10]

**Carried forward:** the restart proof, the token-first order, an id length cap, mixed ids, and the exact "not a ruling" wording in BUILD-LOG.

---

## Pass 05.02: survive a restart

**Time:** 12:39 to 12:56 PM EST. **Builder:** b12. **Result:** passed. [commit 800ea5e]

**What it asked:** at start-up, rebuild the id list from the book lines. Then the lost-reply test: save a write, drop the reply, restart the compute, resend. The book must hold one edit, and the resend must get the original answer. Also: check the token first, keep ids per writer, refuse ids over 128 characters or with control characters (400), refuse mixed ids (400). [pack: /tmp/core-p02.txt]

**Why:** this is Codex's bar for "done". Without it, write once only works until the next restart, which is exactly when a reply is most likely lost.

**What the builder did:**
- Rebuilt the list at start-up from the ids already on the book lines. No new file and no format change.
- If a book already held the same id twice, the first line wins.
- Added the lost-reply test and 5 others.
- On the old code, 5 of the 6 new tests failed for the expected reason. The token test passed on old code, because the token was already checked first. It guards existing behaviour, and Codex allows that.
- Named two fields that a restart cannot rebuild: `queue_id` and `findings`. Marked 7.
- 284 tests passed.

**Prima's audit:** none this pass (the plan was 1 pass in 3).

**What Tester found:** pass. The lost reply survives a restart. A torn last line is dropped at start-up and the resend saves once. 16 copies at once after a restart: saved once. 50,000 ids added 0.19 seconds to start-up. Follow-ups:
1. **A real bug for later:** if the same writer and id were in two books, the rebuild picked the lower book id, not the one written first. The first sender's resend then got 422 instead of its own 200.
2. An id on some ops and none on others was accepted, and this choice was not written down.
3. `queue_id` could be rebuilt after all, from `.queue`.
4. Face 01's wording said "each test fails on f3ed48d"; it should say "each regression test", since guard tests are allowed. [entry 19]

---

## Pass 05.03: other content is refused, and the first write really wins

**Time:** 12:56 to 1:10 PM EST. **Builder:** b13. **Result:** passed. [commit a398778]

**What it asked:** the same writer and id with other content is refused (409) and names the first write's fingerprint and book. Fix Tester's bug: across books, the first written wins. Decide and write down two choices: mixed id/no-id writes, and whether refusals use up the id. Rebuild `queue_id` from `.queue` if that needs no new file. [pack: /tmp/core-p03.txt]

**Why:** Matthew's ruling says an id can't change its content. Until this pass, a second content under the same id was simply saved again.

**What the builder did:**
- 409 with `first_fingerprint` (a SHA-256 hash of the first content) and `first_book`.
- Wrote SHA-256 inside the compute (62 lines) instead of adding a library, because a new library changes Cargo.lock, which is outside the grant.
- The rebuild now keeps the earlier line in a book, the earlier time across books, and the lower book id on a tie.
- Partial ids get 400. Refused answers leave the id free. Both marked 7 in BUILD-LOG with their why.
- `queue_id` comes back after a restart from `.queue`. `findings` stays empty, because findings are not saved anywhere.
- On the old code (800ea5e), 4 of the 5 new tests failed for the expected reason. One is a guard test.
- 290 tests passed.

**Prima's audit:** none this pass.

**What Tester found:** pass. 19 different op shapes, resent before and after a restart: no false 409. 16 different bodies with one id at once: 1 saved, 15 refused with 409, all naming the same first fingerprint. Tester checked the fingerprint by hand with `sha256sum` and it matched. The cross-book bug is fixed. [entry 27]

Two more things Tester found:
- **A new forward risk** (from reading the code): a line saved under 05.01 with an id over 128 characters, or with a new line, now gets 400 when resent, because the id check runs before the replay.
- **The stale-binary trap was confirmed.** See "What we learned about WF" below.

**Face 01 wording** was fixed after this pass: each regression test fails on the start commit of its own pass, and guard tests are named. [entry 30]

---

## Pass 05.04: the records (failed)

**Time:** 1:10 to 1:28 PM EST. **Builder:** b14. **Result:** failed on one job, w03. [commit 280ff80]

**What it asked:** no code change. Write the records:
- w01: a CONTRACT.md section so a client author can use ids from the doc alone;
- w02: check that seqaddr-core API.md matches the code;
- w03: BUILD-LOG lines for the forward risk, the stale-binary trap, and **a list of every draft choice on this page**;
- w04: a small test that fails if the codes in CONTRACT.md drift from the code. [pack: /tmp/core-p04.txt]

**Why:** the plan said a pass is not done until the docs match the code. And Matthew must be able to see every choice that was made without his ruling (axiom 7). Otherwise a draft choice hardens into a rule nobody approved.

**What the builder did:** wrote the CONTRACT section, fixed stale lines in API.md, wrote the BUILD-LOG section with a list of draft choices, and wrote a drift test. 291 tests passed.

**Prima's audit (1:20 PM EST, before reading Tester):** pass, with one follow-up. The drift test read the code's source text, not its behaviour, so it could break easily. [scratch/prima-audit/05.04.txt]

**What Tester found:** **fail on w03.** The list of draft choices was not complete. Missing from it, or not marked 7: the 409 code and body; the fingerprint method; the first-write rule across books; `queue_id` from `.queue`; ids per writer; trimming; the plain-character 422; case sensitivity. [entry 36]

The other three jobs passed. Tester also listed:
- client gaps in CONTRACT.md (the 422, trimming, case, no `queue_id` on 400 or 409, the 400 body, what to do on 409);
- three cites off by one line;
- what the drift test misses (many changes it would not catch);
- three risks for Matthew: a hand-edited book line is trusted; a lost or forged `.queue`; about 6 KB of memory per id with no cap.

**Why this matters.** Prima had checked this pass herself and passed it. She missed the incomplete list. Tester caught it. This is exactly what the second reader is for. Axiom 9: work is not right because you made it; its maker is the easiest one to convince. Here the "maker" was Prima, who wrote the job. [entry 37]

---

## Pass 05.05: the fix-up

**Time:** 1:28 to 1:38 PM EST. **Builder:** b14 again. **Result:** passed. [commit 2f66bda]

**What it asked:** fix-up 1 for the records goal. Start from 05.04's branch, so the accepted work is kept. [pack: /tmp/core-p05.txt]
- w01: one complete list of every draft choice, all marked 7;
- w02: Tester's three risks written down as 7 notes, no code change;
- w03: a "05.05 corrections" section in CONTRACT.md for the client gaps and the three cites;
- w04: replace the drift test with one that starts a real compute and checks what it does.

**Why:** fix the fail, and fix Prima's own follow-up at the same time. A test that reads code text breaks on a harmless rewrite and misses real changes.

**What the builder did:** all four. Old sections were not rewritten: BUILD-LOG and CONTRACT only get new sections. The new drift test was shown failing once on a wrong doc line, then the line was put back. No code under `src` changed. 291 tests passed.

**What Tester found:** pass. Every claim in the new CONTRACT section is true on a running compute. The new drift test catches the codes it pins. It still misses bullet-level changes and some behaviours (trimming, the alias, mixed-id 400, control characters). Two small nits. [entry 46]

**The page halted at 1:38 PM EST.** No more passes until Matthew rules on the draft choices. [entry 49]

**Merged** into local `build` as 2166b46, by hand. Not pushed.

---

## What we learned about WF itself

These are gaps and wins in the workflow tool, found by using it. They are data for the benchmark and for next week's WF work.

1. **WF refused a stale pin. (The guard worked.)** Prima drafted 05.05 before 05.04 was signed off. WF allowed the draft but refused to pack it, because it was pinned to the page as it was before the close. Prima redrafted it after the close. [entries 39, 41]
2. **WF allowed a draft before sign-off. (A gap.)** Prima's first try at signing off 05.04 used a wrong card word and did not go through. In between, she drafted 05.05. Only the pack step caught it. A draft for the next pass should probably wait for the sign-off. [entry 39]
3. **The shared build folder reuses old programs. (A trap.)** Builders and Tester build into one shared folder to save disk (89% full). When old code and new code are built in turn, cargo can reuse the old test program, because the two copies look the same to it. A checker then sees old results. The fix: clean the two packages and touch the source files between builds. Builders b11, b12, b13 and Tester all hit it. [BUILD-LOG.md:477; returns 05.01-05.03]
   - A related cost: `cargo clean` also removes the compute program, so it must be rebuilt after.
   - The pinned `wf check` makes and removes its own temporary copy under /tmp on each run, and a package clean was needed after each one (Tester).
4. **The docs path in kit/AGENTS.md is wrong from wf-run.** It tells builders to read `docs/AXIOMS.md` and `docs/DESIGN.md`. From `wf-run`, they are at `kit/docs/`. Builders b11, b12 and b13 each reported it. The hashes matched, so no harm was done. [kit/AGENTS.md:4-5]
5. **WF has no "halted" state.** After the HALT note, `wf status` still says "next: Prime writes a 06 note, then wf draft". A new model reading it would think work should go on. (Checked again today after the halt.)
6. **Merges are done by hand.** Prima moved `core-wf` forward after each pass and merged into `build` by hand (2166b46). WF does not do this.
7. **Questions and findings stayed outside the log.** The page log has no `observe` and no `elevate` entries. Observer's notes and the usage-limit questions to Matthew happened in chat.
8. **The box clock is an hour behind Toronto.** It shows CST. BUILD-LOG times were written in EST by hand (builder 05.04, Tester 05.03).

---

## The why-questions

**Why did it work?**
- The goal was small and already ruled (R37 item 2). Nobody had to guess what Matthew wanted.
- Each pass had a short "done when" list, and each new test had to fail on the old code. So a test could not pass just by doing nothing.
- Tester tried to break each pass with hostile tries, far beyond the pack (19 op shapes, 16 at once, torn lines, 50,000 ids). Most of the real follow-ups came from there.
- Codex's review raised the bar early. The restart proof landed in pass 2, not pass 3.
- Draft choices were marked 7 as they were made, so none was hidden.

**Why did 05.04 fail?**
- The job asked for "a short list of every draft choice". The builder listed the lines already marked 7, but not the choices made inside other lines (like the 409 code, or the fingerprint method). Those were written as facts, not as choices.
- Prima's audit checked that the docs were clear and the tests worked. It did not check the list item by item against the code. Tester did.
- In short: the list was built from labels, not from the behaviour. A choice nobody labelled was missed.

**What would we do differently?**
- Mark a choice 7 at the moment the builder makes it, in the same line. Then the list is just a search.
- Ask for the draft-choice list in every code pass, not only in a records pass at the end.
- When Prima audits, check lists against the code, item by item.
- Write the drift test against behaviour from the start (05.05's version).
- Fix the WF gaps above before next week: a halted state, the docs path, a guard on drafting before sign-off, and a safe build step for old-versus-new checks.
- Keep the second reader. It caught the one fail.

---

## The numbers

All from the page log and git unless marked.

| Measure | This page | Baseline (WF building WF, Tue 17 Nov) |
|---|---|---|
| Passes | 5 | 10 |
| Passed / failed | 4 / 1 | 6 / 4 |
| First-try pass rate (passes not after a fail) | 3 of 4 (75%) | 3 of 6 (50%) |
| Fix-ups | 1 (05.05) | 4 (10 passes for 6 fresh goals; longest chain 3) |
| Jobs carried | 1 of 20 (5%) | 5 of 48 (10%) |
| Fails caught by the test commands | 0 | 0 |
| Fails caught by the checker reading | 1 | 4 |
| Prima audits | 2 (05.01 agreed; 05.04 disagreed, Tester was right) | none recorded |
| Time per pass, pack to close (median) | 15.1 min (9.7 to 18.0) | 10.8 min |
| Builder time, claim to return | 4.4 to 7.9 min | 6.2 min (median) |
| Checker time, return to check | 4.1 to 9.2 min | 2.7 min (median) |
| Tests at the end | 291 (279, 284, 290, 291, 291 by pass) | 82 (WF's own) |
| Usage (Prima's reading, not in the log) | about 4 points, about 54.7% to 58% | about 9.3 points for 10 passes |

The baseline column is copied from the plan, section 4. The plan's 1-in-3 audit rate was met: 2 audits in 5 passes.

---

## For a future model

Where everything lives. Paths are on the box under `/workspace/workshop-build/` unless they start with `docs/` or `crates/` (those are in the repo, `repo/`, branch `build`).

- **The spec (what the code does, and why):** `docs/spec/WRITE-ONCE.md`.
- **The technical contract:** `docs/CONTRACT.md:54-79` (two delivery-id sections, dated 2026-11-18).
- **The build notes and every draft choice:** `docs/BUILD-LOG.md:452-486`. The one complete list is line 483. Risk notes are line 484.
- **The code:** `crates/compute/src/store.rs` (search for `delivery_`), `crates/compute/src/sha256.rs`, `crates/compute/src/lib.rs:190-193` (token check), `crates/seqaddr-core/src/validate.rs` and `log.rs` (the field).
- **The tests:** `crates/compute/tests/delivery.rs` (11 tests) and `crates/compute/tests/contract_delivery.rs` (the drift test).
- **Run them:** `CARGO_TARGET_DIR=/workspace/workshop-build/repo/target cargo test -q -p compute -p seqaddr-core`. Clean the two packages and touch the sources first if another copy of the code was built in the same folder.
- **Git:** passes on branch `core-wf`: f363e28 (05.01), 800ea5e (05.02), a398778 (05.03), 280ff80 (05.04), 2f66bda (05.05). Merged into `build` as 2166b46. Start commit was f3ed48d. Not pushed.
- **The page:** `wf-run/pages/90.20.00.0001/`. `log.jsonl` is the record (49 entries); `00.md` to `08.md` are views printed from it; `05.0N/` holds each pass's PACK, PROMPT and AGENTS files. Do not edit the views.
- **The builders' returns:** `wf-run/core/.workshop/returns/90.20.00.0001.05.0N.md` (also in the repo under `.workshop/returns/`).
- **The packs as sent:** `/tmp/core-p0N.txt` and `/tmp/core-p0N-prompt.txt`. /tmp may be wiped; the same pack text is in each `pack` entry of `log.jsonl`.
- **Prima's audits:** `scratch/prima-audit/05.01.txt` and `05.04.txt`.
- **Tester's full findings:** the `report` field of each `check` entry in `log.jsonl` (entries 10, 19, 27, 36, 46). Tester's work folders are `scratch/tester-0502/` to `scratch/tester-0505/`.
- **Why it was built:** `docs/design/PLAN-2026-11-18-core-via-wf.md`, `docs/review/CODEX-PLAN-REVIEW-t292u.md`, `docs/review/DIRECTOR-WORDS-t285u.md`.
- **Matthew's rulings behind it:** R37 item 2 in `docs/spec/DIRECTOR-RULINGS.md:196`; the open question K4 in `docs/design/CORE-AND-TOOLS-SPEC.md:949`.
- **Matthew's words on this journal:** `docs/review/DIRECTOR-WORDS-t303u.md`.

What is still open: Matthew's K4 ruling on the draft choices (spec section 6), and the risk notes (spec section 5). Do not change the behaviour of a draft choice without his ruling.
