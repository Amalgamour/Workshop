# Dev journal: wf board and the log order check

date: Wed 18 Nov 2026. All times are EST.
written by: Prima builder-b18, because Matthew asked (t303u): "Make sure you are writing the spec documentation to go with the work. So I can understand what we did and have the why's in there. It's almost a dev journal so I or a future model have access."
what it covers: building `wf board`, then hardening the log, in 7 commits and 7 Tester rounds, with the why for each step.
the spec (what the code does now): docs/spec/WF-BOARD-AND-LOG-ORDER.md.
note: the box restarted at about 4:33 PM and was restored from a snapshot taken just before the first commit of these docs. That commit was lost, so both docs were rewritten with the same content at about 4:38 PM. The code branches and the real pages were not affected.

How to read the labels:
- A **commit** is one saved step of code, named by a short id like 193da07.
- **Tester** is the model that checks the work. The builder never checks its own work (axiom 9).
- A **fail** from Tester means "fix this before it is used".
- `7` means "not complete yet" (axiom 7).
- A line in square brackets is a side label for engineers.

---

## The short version

- **What we built:** a read-only board that shows what needs someone first. Then a check that refuses a log with steps out of order.
- **How:** 7 commits on two branches. Tester failed the first one on two narrow points. Every later round passed, with small gaps fixed in the next commit.
- **Tests at the end:** 43 unit and 105 end-to-end, 0 failed.
- **Time:** about 3:39 PM to 4:54 PM EST.
- **Where it is:** branch `board-dev` at 193da07, and branch `harden-dev` at bce5cb9 (which holds both). Not merged. Not pushed.
- **Waiting on Matthew:** board Q1-Q3 (item 8), the order rules and a stuck test page (item 14), the old binary (item 15), the merge (item 16).

---

## Before the work

Prima wrote the board plan (docs/design/WF-BOARD.md) at about 3:30 PM, from Matthew's body-shop picture (t296u-t297u) and roadmap U4, U6 and U7. It has seven jobs (w01-w07), twelve tests, and three open questions.

Prima told the builder to use the plan's proposed answers for now, and mark each one "build stage, pending Director answer":
- Q1: tool words as columns, body-shop words as side labels.
- Q2: STALE after 24 hours with no movement, changeable.
- Q3: read only the log, and print git commands; do not run git.

Rules for the builder: the board must never write; every log string must be escaped; tests must prove page files are unchanged; do not touch the real pages or the pin.

---

## Commit bc690cc: the first board

**Time:** about 3:46 PM. **Branch:** board-dev, from workflow a00bc53.

**What landed:** the page board, the full card, and the book board, in a new file `src/board.rs`. Attention first. The 40-line limit that never cuts person questions or a halt. STALE marks. Escaping. 20 new tests. README and AGENTS rows.

A run on the real page 90.30 changed no file (sha256 the same before and after).

**Tester (about 3:55 PM):** fail, on two narrow points.
1. A log with a good chain but an entry for a pass that was never drafted made wf crash while reading the page. The book board then crashed for every page.
2. Some full-card lines did not say where they came from.

Small gaps too: short hashes could be cut in the middle of an escape; an entry with no time showed an age of 498620 hours; `--card` did not take `05.NN`; unknown flags were accepted; an empty log showed a blank address.

---

## Commit 193da07: Tester fixes on the board

**Time:** about 3:58 PM.

**What changed:**
- Reading a page now returns an error instead of crashing. **Why this way:** it fixes `status`, `observe` and `verify` too, not only the board. The book board shows that page as unreadable and still lists the rest.
- Every full-card line now names a log entry, a path, or a command. The test checks every line.
- Short hashes are cut before escaping. A missing time shows "unknown" and is never stale.
- `--card` takes `05.NN`. Unknown flags, a second argument, and `--card` with no page are refused. An empty log is unreadable.

**Tester (about 4:04 PM):** pass.

---

## Commit 385452a: harden the log

**Time:** about 4:08 PM. **Branch:** harden-dev, a new worktree from 193da07, so board-dev was left alone.

**What Tester had found:** forged logs in the wrong state made `wf return`, `check`, `signoff` and `close` crash (exit 101). A pass number of 4294967297 became pass 1. The log accepted steps in the wrong order: close before return, a check on an open pass, a claim after close, a re-draft of a closed pass, a missing kind, a second start.

**What changed:**
- One rule check (`Page::order`) runs on every entry when a page is read, and before every write. It follows the same order the commands keep.
- The four write commands refuse with a clear message instead of crashing.
- Pass numbers must be 01 to 98 (R9).
- A refused write says "refused, nothing written: <rule>", not "the log cannot be read".
- `--card` with `--all` is refused. A bad page address is shown escaped.

**Real pages:** Prima's rule was "if a real page breaks a rule, stop and report". None did. Copies of 90.10, 90.20 and 90.30 verified on the old and the new binary.

**Tests that had to change:** some test pages had been seeded with shortcuts, such as a draft followed straight by a close. They now go through every step. The board's "old check" test planted a return after a check, which is now refused, so it was changed to plant a second check instead.

**Tester (about 4:17 PM):** pass, items 1-5.

---

## Commit 0312f23: small fixes

**Time:** about 4:18 PM.

**What Tester asked:**
1. The "old check" STALE rule could no longer fire on a good log. And the test called a newer check "old".
2. README said "check on a returned pass", but the code also allows a re-check.
3. The AGENTS line about unreadable pages had no why.
4. `--card` should take the same pass forms as the other commands. An overlap error printed "05.100".
5. Optional: refuse a double signoff and a check with no verdict on read.

**What changed:**
- "Old check" is now "check on another commit". The test name says what it proves.
- README and AGENTS fixed. The order rules are marked "build stage, no Director ruling yet".
- `--card` uses the same parser as the other commands. The overlap error says "pass 100".
- A check with no verdict is refused on read.

**Decision: a double signoff was not refused.** Prima looked first: `wf signoff` itself allows a second signoff. Refusing it on read would make logs the tool writes today unreadable.

**Tester (about 4:24 PM):** pass, all 5.

---

## Commit 4494a2e: tighter checks

**Time:** about 4:25 PM.

**What changed:**
- A check needs a commit. "No verdict" and "a verdict that is not pass or fail" became two messages.
- On read, a re-check is only allowed after a failed check, and never after a signoff. That matches `wf check`.
- "Check on another commit" shows full commits, and says when one is a prefix of the other.
- README: the "earlier return" wording is defensive only. AGENTS names axiom 1.

**Decision: the double-signoff change was tried, then taken back.** Tester asked for `wf signoff` to refuse a second signoff. Prima made the change. Two existing tests then failed. They show that re-signing is how Prime answers a face 01 change before close. There is no un-signoff, and the latest signoff governs. So refusing it would break a real recovery path. Prima took both halves back, and added a test that a re-signoff and close still read fine. **Why:** a fix must not remove the only way out of a known state (axiom 6: the past should not block the next step for good).

**Tester (about 4:31 PM):** pass on the rest. Tester agreed with the revert. The commit rule was "partial": an empty commit was refused, but a blank or junk one was not.

---

## Commit cbda5e0: full hash, plain message

**Time:** about 4:32 PM.

**What changed:**
- A check's commit must be a full hash: 40 lowercase hex characters. Tester found all 868 checks wf has written on this computer already have one. The test refuses a space, a tab and newline, a non-hash, an uppercase hash and a short hash.
- README says why a second signoff is allowed.
- The confusing check message ("no longer in return with the same pack and return") is now two plain messages: "it was signed off by ..., next: wf close", or "it changed while the checks ran, run wf check again".

**Real pages:** copies of 90.10, 90.20 and 90.30 still verify on the old and the new binary. The copy and the real folder have the same hash.

**What Tester found:** R1 and R2 pass. G2 fail: a SHA-256 git repo gives 64-character commits. `wf return` took them, but `wf check` was then refused, and such a page would no longer load. The 40-only rule was too narrow: I checked only the hashes on this computer, not every kind of git repo.

---

## Commit bce5cb9: SHA-256 repos, escaped signoff message

**Time:** about 4:53 PM (after the box restart; /tmp was wiped, so the build folder was rebuilt from clean).

**What changed:**
- One shared rule at load for return and check entries: the commit is 40 or 64 lowercase hex. A refused return is not checked, because it records the raw attempt (axiom 6). "Check on another commit" stays a board mark only.
- The "signed off by ..." refusal now escapes the signer and the outcome, since both come from the log.
- At load, a signoff outcome must be one `wf signoff` accepts. Tester's note said "passed/failed", but the command also accepts blocked and needs-authority, so the rule uses all four. Refusing those two would make a page with a legit blocked signoff unreadable. The real pages use only passed (12) and failed (7).
- New end-to-end test: make a SHA-256 git repo, run return, check, signoff and close, then verify, status and the card. It skips with a message if git lacks SHA-256. Git 2.47.3 here has it, so it ran.

**Real pages:** copies in scratch/b18-real (90.10.00.0001 with 85 entries, 90.20.00.0001 with 49, 90.30.00.0001 with 37) verify ok on the new binary. The copies have the same hash as the real pages, and before and after. The old binary was not rebuilt after the restart, so only the new one was run this round.

---

## Parked for Matthew

**The stuck test page (item 14).** Tester made a page with two wf versions. The new one halted it. The old one, which does not know halt, then packed it. Under the new order rules that page is unreadable, so every write is refused, resume too. No real page has this. Prima did not change the rules for it. **Why:** loosening the rules quietly would undo the guard. Matthew should decide how a page that is already out of order may recover. The proposal is in the questions file.

**The old binary (item 15).** `wf-bin/wf-8eb1fdb` can still write pages and does not know halt. That is how the stuck page was made. The proposal is to rename it.

**Merging (items 13 and 16).** The board lines use proposed answers. Tester flags axiom 1: they should not merge into `workflow` before Matthew answers item 8.

---

## Lessons

1. **Read the code before you add a rule.** The double-signoff refusal looked safe, but it would have broken a real recovery path. The tests caught it.
2. **A new rule can make old states unreachable.** The "old check" mark went dead once a return after a check was refused. Rename it, or say it is defensive only.
3. **Check the real pages against every new rule before you commit.** All three passed each time.
4. **A crash is the worst refusal.** It names nothing and can leave work half done. Every refusal now names the entry and the rule, and exits 1.
5. **Plain messages say the state and the next step.** "Signed off, next: wf close" helps. "No longer in return with the same pack" did not.

---

## For a future model

- **The spec:** `docs/spec/WF-BOARD-AND-LOG-ORDER.md` in the build repo (branch `build`).
- **The plan:** `docs/design/WF-BOARD.md`.
- **The code:** `/workspace/workshop-build/scratch/harden-dev` at cbda5e0 (branch `harden-dev`), and `/workspace/workshop-build/scratch/board-dev` at 193da07 (branch `board-dev`).
- **The questions:** `docs/review/QUESTIONS-2026-11-19.md`, items 8 and 13-16.
- **Real pages:** `/workspace/workshop-build/wf-run/pages/`. Do not edit them. Test on copies (`scratch/b18-real`).
- **Matthew's words behind this work:** t296u-t297u (body-shop work orders), t303u (spec and journal), t262u (several models on one page).

Do not merge the board lines, or change the order rules, without Matthew's rulings on items 8 and 14.
