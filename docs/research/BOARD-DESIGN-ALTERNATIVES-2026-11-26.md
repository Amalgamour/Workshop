# Board front: design alternatives (stage 1 kanban)

Made: Thu Nov 26 2026, by Grok Bot (fire-sale research worker for Prima).
State: survey only. Not a ruling. Nothing packed. Nothing in the repo changed.
For: Prima first, then Matthew.

## Pins (what I read)

- Local repo: /workspace/workshop-build/repo, branch `build`, tip `3cbd972`.
- GitHub `returns` tip `ec78461d` (wf source `src/`, UI-1 and UI-2 lab returns).
- GitHub `packs` tip `c697e035` (the wf `pages/` and each `log.jsonl`).
- GitHub `prima/build` tip `5201b243` (the EOW work page).
- Short cite forms:
  - `R:src/board.rs:25` = returns@ec78461d.
  - `P:pages/...` = packs@c697e035.
  - A bare path = local repo, branch build @3cbd972.

## Read this first: three things that shape the whole answer

1. **The MVP board is the wf command, not a web page.**
   - Matthew, G5: "wf board with holder, step and next" (docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md:31).
   - Matthew, G6: the GUI manager is the long-term goal.
   - Prima's reading: the GUI "is not part of the MVP scope" (docs/review/DIRECTOR-WORDS-t541-mvp-gaps.md:39).
   - So the web front must not block 0498 (docs/plan/MVP-GOAL-PROPOSAL.md:87).
2. **Writes from a screen wait for stage 7.**
   - Stage 1 adds a read-only `wf board` (docs/design/ROADMAP-2026-11-18.md:302).
   - Assign and move come in stage 7, after the locked door (stage 2) (docs/design/ROADMAP-2026-11-18.md:303-304).
   - "A drag that only changes the screen is not allowed" (docs/design/ROADMAP-2026-11-18.md:303).
3. **The front is already being designed, as a read-only lab.**
   - Matthew picked it on Nov 25 (t593u, card t593s2418) (docs/plan/WORK-PAGE-2026-11-25-EOW.md:5).
   - The brief: "a Next.js kanban that reads only. The Rust compute core owns every write" (docs/plan/WORK-PAGE-2026-11-25-EOW.md:72).
   - Claude returned UI-1 (design). Codex returned UI-2 (evidence). Both are on `returns` (commits listed in section 1.5).
   - Claude's design must be checked by another view before use (docs/plan/WORK-PAGE-2026-11-25-EOW.md:46; t580u).
   - This survey is that other view. My checks of Claude's claims are in section 1.6.

---

## 1. What exists now

### 1.1 The old reader app (`app/`)

- A Next.js 15 / React 19 app (app/package.json).
- Last changed Nov 11, commit `9514d97` (`git log -- app`). That is before wf, packs and returns (docs/plan/WORK-PAGE-2026-11-25-EOW.md:21).
- It reads only the **compute crate** HTTP API, not wf (app/lib/compute.ts:1-2, default port 7700).
- The compute crate reads `books/*.book`, not wf `pages/` (docs/CONTRACT.md:5-8).
- Screens that work (with the mock or real compute) (app/README.md:20-30):
  - Library, Page (faces as tabs), Cards, Links, History, Words, Resolve.
  - Each screen has "Check it yourself": the raw answer and its URL (app/README.md:30).
- Board-like screens that already exist:
  - **Desk board**: every 05 counter on a desk, in the six loop columns (app/app/desk/[dd]/page.tsx:26-29, :65-75).
  - **Work loop board**: one page's 05 jobs as columns, plus a job panel (app/components/WorkBoard.tsx:48-63).
  - The columns are the loop tails draft, pack, open, return, review, closed (app/lib/rules.ts:77-84).
  - It says the board is "a view the compute derives from the log; never written" (app/components/WorkBoard.tsx:49).
- **It writes.** Not read-only:
  - WorkBoard has move and "Write the job as a draft" buttons (app/components/WorkBoard.tsx:36-43, :84, :98).
  - A POST pass-through forwards propose, ask, ask/link, close and check.seq with the user's token (app/app/api/post/[...path]/route.ts:5-14).
- A GET-only pass-through exists, with an allow-list (app/app/api/compute/[...path]/route.ts:4-8).
- A read-only mock compute and sample books exist (app/mock/server.mjs; app/README.md:15-16).

### 1.2 The compute crate (Rust, `crates/compute`)

- Book reads, a serialized proposal queue, and an approval gate (commit `cf31c93`).
- Every write needs `Authorization: Bearer TOKEN`; the body's `by` is not trusted (crates/compute/src/lib.rs:95).
- No CORS headers. Only same-machine clients talk to it (crates/compute/src/lib.rs:9-10).
- A Host check allows only the listener's own address (crates/compute/src/lib.rs:267-276).
- It has **no board route** and does not read wf pages (UI-2 GAPS row "Typed board endpoint: Missing").

### 1.3 wf board (Rust, on `returns`)

- `wf board <page>` = page board. `wf board` = book board (R:src/board.rs:49-50).
- It never writes: "no log entry, no view reprint, no lock file, and it runs no git" (R:src/board.rs:2).
- wf itself marks `board` and `status` as non-writing, so no lock is taken (R:src/lib.rs:117-120, :158).
- Every log string is escaped before it prints (R:src/board.rs:3-4).
- Six columns, tool words first, body-shop side labels, and who owes the next move (R:src/board.rs:25-32).
- Column names are still "build stage, pending Director answer" (R:src/board.rs:22-24; docs/design/WF-BOARD.md:132-136).
- Page board: header, ATTENTION first, columns, footer (R:src/board.rs:280-300).
- Default cap 40 lines; person questions and a halt are never cut (R:src/board.rs:14-16).
- STALE after 24 hours with no entry (R:src/board.rs:34-36).
- Short card "held by" = the **claim**, not the lock holder (R:src/board.rs:272-273).
- Full card `--card NN` names the entry behind every line (R:src/board.rs:347-375).
- Book board: one line per page, counts per column, attention count, HALTED (R:src/board.rs:466-497).
- **Output is text only.** Flags are only `--all`, `--card NN`, `--stall-hours H` (R:src/board.rs:51-52). There is no JSON form.

### 1.4 Page 0424 (book-board): holder, step and next

- Init by Matthew, grant `src/board.rs` and `tests/page_0424.rs`, grant ref t541u (P:pages/90.50.10.0424/log.jsonl:1).
- Goal: each book-board line shows holder, step and next (P:pages/90.50.10.0424/01.md:5).
- Holder there = the pass's claim, "or the word none" (P:pages/90.50.10.0424/04.md, goals, "How the three fields are chosen").
- 05.01 is packed, not claimed (P:pages/90.50.10.0424/05.md:4).
- 0498 needs 0424 (docs/plan/GROK-BUILDER-QUEUE.md:101).
- **So `src/board.rs` is held by 0424 now.** Any board JSON work must wait for 0424 to close.

### 1.5 The two lab returns (Nov 25)

- UI-1, Claude: `labs/ui-scaffold/` README, CONTRACT, QUESTIONS (returns commit "lab: UI-1 kanban front design", before `6fca9e2f`).
- UI-2, Codex: `labs/ui-evidence/` EXISTS, GAPS, PATTERNS (returns `6fca9e2f`).
- Claude's options: A ★ wf gives JSON, front draws; B compute crate reads wf pages; C front splits wf text (labs/ui-scaffold/README.md:57-93).
- Claude's 8 questions (labs/ui-scaffold/QUESTIONS.md:8-67).
- Codex's gap table: most rows "partial"; "Ruling ID on a card" and "Typed board endpoint" are "missing" (labs/ui-evidence/GAPS.md, table).

### 1.6 Independent check of Claude's UI-1 claims (t580u)

I opened the cited source myself. Results:

| Claude's claim | Check | Where I looked |
|---|---|---|
| Six columns at board.rs:25-32 | true | R:src/board.rs:25-32 |
| "read only, built from the log" at :285 | true | R:src/board.rs:285 |
| 40-line cap at :16 | true | R:src/board.rs:16 |
| No JSON form; text only | true (flag refusal lists 3 flags only) | R:src/board.rs:51-52 |
| Book board prints counts only | true | R:src/board.rs:486-489 |
| Board holder is the claimant | true (short card :272; full card :367-370) | R:src/board.rs:272, :367-370 |
| Lock holder is a separate `Hold` | true | R:src/page.rs:38-46, :77-78 |
| App calls compute on 7700 | true | app/lib/compute.ts:2 |
| App last changed in commit `9f5500f3` | **not confirmed**: local build branch shows `9514d97` for app/. May be a prima/build hash. | `git log -- app` |

- No poisoned or false claim found in the lines I checked.
- I did not check every CONTRACT.md row.

### 1.7 What does not exist

- No web screen reads wf pages.
- No machine-readable board (JSON) anywhere.
- No desk-wide "who holds what" source across pages (labs/ui-scaffold/README.md:51; UI-2 GAPS row "Desk").
- No ruling id on a pass; only `init` (`grant_ref`) and `grant` carry a ref (labs/ui-scaffold/QUESTIONS.md:48-53; P:pages/90.50.10.0424/log.jsonl:1).
- No page 0498 folder yet (packs `pages/` list ends at 0426 and 0700-0705).

---

## 2. How faces and passes show as cards (shared by all three options)

One board shape at every level: a level, an address, columns, cards (labs/ui-scaffold/README.md:29-43; axiom 2, docs/plan/WORK-PAGE-2026-11-25-EOW.md:15).

**Book board** (one card per page; docs/design/ROADMAP-2026-11-18.md:277)
- Card: address, title, holder, step, next (0424), six counts, attention count, HALTED.
- No single column per page. Show the six counts, as wf does (R:src/board.rs:486-489).

**Page board** (one card per 05.NN; docs/design/ROADMAP-2026-11-18.md:278)
- Top strip: nine small face cards, 00 stamp to 08 connections.
  - Face names from the views: 00 stamp, 01 agents card, 02 pseudo code, 03 menu, 04 dev space, 05 work, 06 prime notes, 07 labs, 08 connections (first line of each P:pages/90.50.10.0424/NN.md).
  - Each face card shows version, entry and hash, from the log, not from the file (views say "Do not edit", P:pages/90.50.10.0424/01.md:2).
  - A locked face (01, 04 or 05) shows a lock tag: worker, reason, time (R:src/page.rs:38-46; LOTO, DIRECTOR-WORDS-t541-mvp-gaps.md:63-65).
- Then ATTENTION, first, never hidden (docs/design/WF-BOARD.md:41-52).
- Then six columns of pass cards.
  - Pass card: `05.NN`, outcome line, tail, "claimed by", "lock held by", next, age, STALE, counts.
  - A tail that is not one of the six (for example withdrawn) goes in its own "other" lane. Today wf drops it into column 1 (R:src/board.rs:136-137; UI-2 GAPS row "Pass step").

**Pass board** (later)
- Cards are jobs w01, w02 ...; columns pending, accepted, discarded (labs/ui-scaffold/README.md:38).

**Every card**
- Opens its evidence: pack, return, check, close paths and entry numbers (docs/design/WF-BOARD.md:73-84).
- Unknown stays "unknown (not in the log)", never a dash (R:src/board.rs:42; axiom 7).
- Times: the log is UTC (Z). Show EST and UTC side by side, like the old History screen (app/README.md:26).
- React prints text, never raw HTML. No `dangerouslySetInnerHTML`. Hostile text stays text (docs/design/WF-BOARD.md:86-90, test 8 at :100).

---

## 3. Three design alternatives

All three: read-only first. No write button. No token in the front.

### Option A (default): wf makes the board data, the front only draws it

Data flow:
1. A later wf page adds `wf board --json` and `wf board <page> --json`.
2. It uses the same code that builds the text board. Same columns, cards, attention, stale.
3. The Next.js **server** runs that one read-only command on a read-only copy of `pages/` (a packs checkout).
4. The browser gets drawn HTML. It never talks to wf.
5. Words (titles, brands) can still come from the compute crate GET routes later (app/lib/compute.ts:10-21).

Pros:
- Inherits the board that exists. Rules stay in Rust (R:src/board.rs:25-32, :174-218).
- One source, so the text board and the screen cannot disagree (axiom 2; docs/design/WF-BOARD.md:38).
- `board` is already a non-writing command in wf (R:src/lib.rs:117-120).
- Matches Claude ★ and fits Matthew's "wf board" ruling (G5).

Cons:
- Needs one wf page on `src/board.rs`. That file is held by 0424 now (section 1.4).
- A web server that starts a program is a new surface. It must be locked down (below).
- Nothing live to draw until the JSON page closes. Saved JSON samples fill the gap.

Risk to "compute is the fortress" (t328u, docs/review/DIRECTOR-WORDS-t328u.md:7):
- Low. The front reaches only one read-only command.
- Guards to write into the pack:
  - Allow-list: the server may run only `wf board` with fixed flags. No shell. No user text in the command line except a checked page address.
  - It runs on a read-only checkout, never Matthew's working `pages/`.
  - Next.js binds 127.0.0.1 only.
  - The new app has no POST route at all.
  - A test hashes every page file before and after (as WF-BOARD.md test 1, docs/design/WF-BOARD.md:93).

Smallest first slice Matthew can review and test (t585u):
- **A1: one screen, the book board.**
- After 0424 closes, one small wf page adds `--json` to the **book board only**.
- One Next.js page draws it: one card per page, six counts, holder, step, next.
- Matthew test: run `wf board` and open the screen on the same folder. The numbers match.
- Done when: same page list, same counts, same holder/step/next; page hashes unchanged; no POST route in the new folder.

### Option B: board snapshot files, no live link (air gap)

Data flow:
1. At each `wf publish-pack` (or a separate read step), wf writes `wf board --json` into a file in git, for example `boards/90.50.10.json` on packs.
2. The front is a static site. It reads only those files (local checkout or GitHub).
3. The front never runs wf and never calls the compute.

Pros:
- Strongest air gap. The front cannot reach the compute at all.
- Works with GitHub, which Matthew says is enough for search now (G6, DIRECTOR-WORDS-t541-mvp-gaps.md:37).
- Matthew can open it anywhere, even with no wf on the machine.
- Same "view printed by wf, do not edit" pattern the face files already use (P:pages/90.50.10.0424/01.md:2).

Cons:
- Stale by design. Each screen must say "as of entry N, head hash H".
- Adds a stored board file. The old app says the board is "never written" and "not a stored face" (app/components/WorkBoard.tsx:49).
- The WF-BOARD plan says stop if the board needs a write (docs/design/WF-BOARD.md:120). A snapshot is a write by publish, a new view kind.
- Touches publish code too, a second busy area.

Risk to the fortress:
- Lowest live risk. But a snapshot file can be hand-edited in git.
- Guard: the screen re-checks the snapshot's head hash against the page log head, and shows "differs, the log wins" (docs/design/WF-BOARD.md:45, rule 3).

Smallest first slice:
- **B1: one JSON snapshot of 90.50.10, made by hand on the box with the A1 command, plus a static page that draws it.**
- Matthew test: open the static page from a file. Compare with `wf board`.
- Needs Option A's `--json` anyway. So B is really "A, plus publish the output".

### Option C: reuse the old reader; the web side reads the logs itself

Data flow (two variants):
- C1: the Next.js server reads `pages/*/log.jsonl` and rebuilds the columns in TypeScript.
- C2: the compute crate learns new routes, for example `/wf/board/:addr` (labs/ui-scaffold/README.md:74-83).
- Either way, reuse `app/` desk and work boards (app/app/desk/[dd]/page.tsx:65-75; app/components/WorkBoard.tsx:48-63).

Pros:
- Fastest to a picture. The board UI and styles exist.
- No wait on `src/board.rs` (C1).
- One front door for the browser, as today (C2).

Cons:
- Board logic lives twice. They will drift (axiom 2; labs/ui-scaffold/README.md:81).
- C1 skips wf's log order check. A forged or out-of-order log could look fine on screen (docs/spec/WF-BOARD-AND-LOG-ORDER.md:24).
- C1 skips wf's escaping (R:src/board.rs:3-4).
- The old app writes. Its buttons and POST route must be cut first (app/app/api/post/[...path]/route.ts:5).
- The brief says no file in `app/` is edited (docs/plan/WORK-PAGE-2026-11-25-EOW.md:82).
- C2 changes two branches: compute on prima/build, wf on returns (labs/ui-scaffold/README.md:82).
- Text-splitting the wf output (Claude's C) is worse still: the 40-line cap loses cards (R:src/board.rs:16).

Risk to the fortress:
- Highest. The web side becomes a second, weaker reader of the truth.
- Leaving the old write route in place keeps a write path from a screen before the locked door (stage 2) (docs/design/ROADMAP-2026-11-18.md:304).

Smallest first slice:
- **C-1: copy the desk board into a new folder and point it at one page log.**
- Matthew test: compare with `wf board`. Expect mismatches on stale and attention, since those rules are not ported.

### Side by side

| | A (default) | B | C |
|---|---|---|---|
| Who builds the board | wf (Rust) | wf (Rust) | TypeScript or compute crate |
| Live or snapshot | live, read-only | snapshot | live |
| Rust change | 1 wf page (`--json`) | `--json` + publish | none (C1) or compute (C2) |
| Can drift from `wf board` | no | no (but can go stale) | yes |
| Fortress risk | low | lowest | highest |
| Blocks on 0424 | yes | yes | no |
| First slice | book board screen | static file page | copied desk board |

---

## 4. The design-following option: **Option A (default)**

Why it follows the design:
- Matthew's board is `wf board` (G5, DIRECTOR-WORDS-t541-mvp-gaps.md:31). A draws exactly that.
- Inherit, do not rebuild: one board, one rule set, in Rust (axiom 2; R:src/board.rs:25-32).
- Rust only for the compute core; Next.js for the kanban front (t333u, docs/review/DIRECTOR-WORDS-t333u.md:7). A keeps that split clean.
- Read-only until stage 7 (docs/design/ROADMAP-2026-11-18.md:302-304).
- Claude's UI-1 also marks A ★ (labs/ui-scaffold/README.md:57). I checked its basis (section 1.6).

Order of work (proposal):
1. 0424 closes (holder, step, next on the book board).
2. 0498 stays first. The front does not block it (G6).
3. A small wf page: `wf board --json`, book board only. Grant `src/board.rs` plus its own test.
4. A lab or 04NN page for the front: one screen, new folder, no POST route.
5. Then the page board, then face cards, then pass boards.

---

## 5. Open questions for Matthew

Format: Question / Why it matters / Options with default / What if no answer.
The default is the option that follows the existing design.

**Q1. Which data flow builds the front?**
- Why it matters: it decides where the board rules live, and the fortress risk.
- Options: **A, default: wf makes the board as JSON; the front only draws it.** B: wf writes snapshot files; the front is static. C: the web side reads logs itself.
- If no answer: plan A. Build nothing until 0424 closes.

**Q2. Is the web front part of stage 1, or a side lab until after 0498?**
- Why it matters: G6 says the GUI is not MVP scope. Stage 1 work should not slow 0498.
- Options: **A, default: side lab now (design and samples only); a real 04NN page after the 0498 run.** B: a 04NN page now, in parallel. C: wait for stage 7.
- If no answer: side lab only. No front page is packed before 0498.

**Q3. Where does the new front live?**
- Why it matters: `app/` is old, writes, and the brief says do not edit it.
- Options: **A, default: a new folder, named by Prima at pack time; `app/` untouched.** B: rebuild inside `app/` after the write screens are removed.
- If no answer: new folder. `app/` stays as a record.

**Q4. Any write buttons on the new front?**
- Why it matters: writes from a screen need the locked door (stage 2) and the message log (stage 5).
- Options: **A, default: none until stage 7. Not even disabled buttons.** B: keep the old app's token-gated writes.
- If no answer: none.

**Q5. Who is the "holder" on a card?**
- Why it matters: since 0423 the lock holder counts, but the board prints the claimant.
- Options: **A, default: show both, labelled "claimed by" and "lock held by"; "none" when empty.** B: only the lock holder, after a wf change.
- If no answer: both labels.

**Q6. Column names?**
- Why it matters: still "build stage" in the code (R:src/board.rs:22-24). The screen will fix the words in Matthew's eyes.
- Options: **A, default: tool words (Draft, Ready, Working, Waiting check, Checked, Closed), body-shop words as small side labels.** B: body-shop words first.
- If no answer: tool words, same as `wf board`.

**Q7. Which copy of the page logs does the front read?**
- Why it matters: logs differ by branch (0403: 12 entries on packs, 9 on returns; labs/ui-scaffold/QUESTIONS.md:35).
- Options: **A, default: a read-only packs checkout, the same root `wf board` reads (R:src/board.rs:467).** B: the longer copy, with a mark when they differ.
- If no answer: packs, with the head hash shown on every screen.

**Q8. Who may open the front, and from where?**
- Why it matters: t328u, no one reaches the compute without strong safety. Sign-in comes later (t585u).
- Options: **A, default: 127.0.0.1 only, on the box or Matthew's PC, no sign-in, read-only.** B: a shared network address.
- If no answer: local only.

**Q9. What does a card show for "ruling id"?**
- Why it matters: every card should carry its why and ruling (docs/plan/WORK-PAGE-2026-11-25-EOW.md:16). Passes have no ref field.
- Options: **A, default: show the page's `grant_ref`; mark the pass ruling missing (`7`).** B: a later wf page adds `ref` to each pack.
- If no answer: grant ref plus a visible "missing".

**Q10. Do faces 00-08 show on the page board?**
- Why it matters: t423u names faces as part of the boards. Today only 05 passes are on the board.
- Options: **A, default: a strip of nine face cards from the log (version, entry, lock tag), above the pass columns.** B: passes only for the first slice.
- If no answer: passes only in slice 1; face strip in slice 2.

**Q11. Who builds the JSON page and the front?**
- Why it matters: t580u: Claude gets narrow lanes and no data authority; Grok bots do control tasks only (t572u).
- Options: **A, default: a Grok worker or Cursor-1 builds both; Claude stays design-only; Codex gathers evidence.** B: Claude builds the front code under an independent check.
- If no answer: Grok worker or Cursor-1, after Prima packs it.

Question count: 11.

---

## 6. Things I did not do

- No wf command run. No commit, push or edit in the repo.
- Did not run the old app or the compute.
- Did not check every row of UI-1 CONTRACT.md or UI-2 EXISTS.md.
- Read remote branches through GitHub, at the pinned commits above.
