# wf board and the log order check (the spec)

state: describes the wf tool on two builder branches. Neither branch is merged into `workflow` yet. Nothing is pushed.
- `board-dev` at 193da07: the board.
- `harden-dev` at bce5cb9: the board, plus the log order check (commits 385452a, 0312f23, 4494a2e, cbda5e0, bce5cb9). harden-dev starts from 193da07, so it holds both.
made: Wed 18 Nov 2026, by Prima builder-b18, because Matthew asked (t303u): every piece of work gets a spec and a dev journal, with the whys.
the story of how it was built: docs/journal/2026-11-18-wf-board-and-log-order.md.
the plan the board came from: docs/design/WF-BOARD.md.
code: `/workspace/workshop-build/scratch/harden-dev` (line numbers are from cbda5e0; bce5cb9 moved a few).

How to read the labels:
- A line in square brackets is a side label for engineers. It names the code (file:line) or a test.
- `7` means "not complete yet" (axiom 7). Here it marks a gap or a question for Matthew.
- "Build stage" means: we use a proposed answer now, and it can change. Matthew has not ruled on it yet.
- File paths are short: `board.rs` is `src/board.rs`.

---

## 1. What this work is

Two pieces.

1. **`wf board`** shows the work on a page like work orders on a board in a body shop. It shows what needs someone first. It only reads. It never writes.
2. **The log order check.** When wf reads a page, it now checks that every step in the log came in the right order. A log with steps out of order is refused. So a forged or hand-written log cannot steer the tool.

Why both now: Matthew wants to see what needs him in under a minute (t296u-t297u, roadmap U6 step 1). And the board reads the log, so the log must be one the tool can trust.

---

## 2. The board

### 2.1 What it shows

- `wf board <page>` prints the **page board**:
  1. A header: page, title, person, Prime, how many log entries, the last entry time, the head hash.
  2. **ATTENTION**: what needs someone, most urgent first (2.3).
  3. **COLUMNS**: one card per pass (2.2).
  4. A footer: what was cut off, and the command to see it.
- `wf board <page> --card NN` prints one **full card**: every field of one pass (2.6).
- `wf board` with no page prints the **book board**: one line per page under `pages/` (2.7).
- Times are shown as they are in the log, in UTC (they end in Z).

**Why:** see what needs you, what is moving, and what passed, in under a minute. [plan WF-BOARD.md section 1]

### 2.2 The columns

The columns use the tool's own words. The body-shop word is a side label only.

| Column | Side label | Who owes the next move |
|---|---|---|
| Draft | estimate | Prime: `wf pack` |
| Ready | ready for a bay | any builder: `wf claim` |
| Working | in the bay | the builder who claimed it |
| Waiting check | waiting QC | a checker who is not the builder |
| Checked | QC done | Prime: `wf signoff`, then `wf close` |
| Closed | delivered | nobody |

- The Closed column counts passed, failed, blocked and needs-authority.
- By default only the last 3 closed cards show. The footer counts the rest.
- The "next move" text comes from the same code as `wf status`, so the two never disagree.

**Why tool words:** the tools, docs and logs already use them. Two sets of names would drift apart (axiom 8: one name points to one thing). The side label keeps Matthew's body-shop picture.

**Build stage, no Director ruling yet:** the column names (plan Q1; questions file item 8).

[code: board.rs:25 (COLUMNS); status.rs `pass_next`]

### 2.3 Attention, most urgent first

One line each. Each line names its log entry.

1. Questions to the person with no answer.
2. The page is halted: who, why, and how to resume.
3. A page file differs from the log. The board still prints from the log, and says "the log wins; run wf verify <page> --fix".
4. Returns waiting for a check.
5. Checked passes waiting for signoff or close.
6. Questions to Prime with no answer.
7. Observer signals.
8. Stale items (2.4).

- If nothing needs anyone, it prints "attention: none found in the log". It never says "all clear". **Why:** if nothing is written down, that does not prove nothing is wrong (axiom 7).
- Items 1 and 2 are never cut off (2.5).

[code: board.rs:220 (`attention`)]

### 2.4 Stale is shown as stale

A card gets the word `STALE` and the reason when:

- **Waiting too long:** an open pass has had no log entry for 24 hours. `--stall-hours H` changes the limit. An entry with no time is never stale on time; its age shows as "unknown".
- **Drift:** the pass was packed against an older face 01 or 04. Both entry numbers are shown.
- **Check on another commit:** the latest check names a commit that the latest return does not name. Full commits are shown. If one is a prefix of the other, it says so, so two short forms are not read as the same commit.
- **Old signoff:** face 01 changed after the signoff.

**Why:** a summary can disagree with its records. The board shows the disagreement. It never picks one, and never quietly re-points (axiom 6).

**Build stage, no Director ruling yet:** the 24-hour limit (plan Q2; questions file item 8). It is the same default as `wf observe`, so the two agree.

Defensive only: a check that names an *earlier* return's commit cannot happen in a log wf will read now, because a second return after a check is refused (section 3). The wording stays in the code in case it is ever reached. [unit test `check_on_another_commit_names_which_commit`]

[code: board.rs:174 (`stale`), status.rs:75 (`drift`, shared with observe)]

### 2.5 The 40-line limit

- The page board is at most 40 lines.
- Questions to the person, and a halt, are **never cut**, even if that makes it longer.
- The footer counts the cut attention lines, cut cards, and older closed cards.
- `--all` shows everything.

**Why:** under a minute to read. But no limit may hide something that needs the person.

[code: board.rs:16 (CAP), :280 (`page_board`)]

### 2.6 The full card

- `--card NN` takes `4`, `04`, `004` or `05.04`, the same forms as every other command.
- Every line names where it came from: a log entry number, a `pages/` path, or a command (`git -C <repo> show <commit>:<file>`, `wf ...`).
- A field the log does not hold says "unknown (not in the log)", and names the entries it searched.

**Why:** each card must open its own proof (axiom 8). Unknown stays unknown (axiom 7).

**Build stage, no Director ruling yet:** the board prints git commands. It does not run git. So a printed link is not proof that it opens (plan Q3; questions file item 8).

[code: board.rs:347 (`card`), :91 (`card_nn` uses the same parser as the other commands)]

### 2.7 The book board

- One line per page: title, entries, the last time, a count per column, how many attention items, and HALTED if halted.
- A page that cannot be read shows "unreadable: <reason>". The other pages still print.
- An empty log, or a log whose first entry is not the start of the page, is unreadable.

[code: board.rs:450 (`book`), :97 (`load`)]

### 2.8 It never writes, and it escapes

- No log entry, no page file, no lock file. It runs no git.
- Every bit of text that came from the log is escaped, for example `\u{1b}`, before it prints. Names too. Long text is cut after escaping, and never in the middle of an escape. Short hashes are cut before escaping.
- Clean text looks the same.

**Why it only reads:** moving cards comes later, after the locked door (roadmap U7). A board that wrote now would write around the compute (axiom 1). **Why escape:** old log entries were written before input was checked. A hostile line must never print raw on a screen people trust.

[code: lib.rs:127 (board runs before any lock); board.rs:117 (`clip`). Test: `board_writes_nothing` compares the sha256 of every page file before and after.]

### 2.9 What the board refuses

- Any flag other than `--all`, `--card` and `--stall-hours` (including `--as`: the board writes nothing, so it needs no name).
- A second argument.
- `--all` with a value. Put the page first: `wf board <page> --all`.
- `--card` together with `--all`.
- `--card` or `--all` with no page.
- `--stall-hours` that is not a whole number.
- A bad page address. The address is shown escaped.

---

## 3. The log order check

### 3.1 What it does

Every time wf reads a page, it checks each log entry against the order the commands keep. It checks again before it writes a new entry.

- **On read:** a log that breaks a rule is unreadable. Every command says "log entry N is out of order: <rule>; the page cannot be read", exits with code 1, and writes nothing. The book board shows that page as unreadable and lists the rest.
- **On write:** an entry that would break a rule is refused before it is written: "refused, nothing written: <rule>".

**Why:** a forged or hand-written log must not steer what the tool does next (axiom 1: authority). Before this, some forged logs made write commands crash (exit 101), and one made pass 4294967297 turn into pass 1.

[code: page.rs:195 (`order`), :269 (`apply` calls it on read), `Page::add` calls it before writing]

### 3.2 The rules

1. Entry 1 is the start of the page (init). It is the only one. A second one is refused.
2. Every entry has a known kind. A missing kind or an unknown kind is refused.
3. A pass number is 01 to 98 (R9). Anything else is refused. It is never wrapped around.
4. A pass goes in this order:
   - draft (a new pass, or a re-draft while it is still a draft; never after it is closed),
   - pack (after a draft),
   - claim (after a pack),
   - return, or a refused return (on a claimed pass),
   - check (on a returned pass; a re-check only after a failed check, and never after a signoff),
   - signoff (on a checked pass),
   - close (on a checked pass, and only after a signoff).
5. A check has a verdict of pass or fail. "No verdict" and "a verdict that is not pass or fail" are told apart.
6. A return and a check name their commit as a full hash: 40 or 64 lowercase hex characters (0-9, a-f). 40 is a normal (SHA-1) git repo, 64 is a SHA-256 repo (`git init --object-format=sha256`). It is one shared rule for both kinds. A refused return is not checked: it keeps the raw attempt as evidence (axiom 6), and the board shows it escaped. "Check on another commit" stays a board mark (STALE), not a load rule.
7. A signoff has an outcome that `wf signoff` accepts: passed, failed, blocked or needs-authority. The real pages use only passed and failed.
8. No draft, pack or claim while the page is halted. No second halt. No resume unless halted. No halt while a pass is open.
9. A question sent up must belong to a pass that exists.

The three real pages (90.10 with 85 entries, 90.20 with 49, 90.30 with 37) follow every rule. Copies verify on the old and the new binary. Tester also found all 868 checks wf has written on this computer already use a full hash. On the real pages, all 19 returns and 19 checks use a 40-character hash, and the 19 signoffs are 12 passed and 7 failed.

**Build stage, no Director ruling yet:** all of these rules (questions file item 14).

### 3.3 Write commands refuse, they do not crash

`wf return`, `wf check`, `wf signoff` and `wf close` used to crash (exit 101) when a forged log was missing a pack, a return or a check. Now they say "refused: 05.NN has no <part> in the log; nothing was written". The order check stops these logs first. This is a second guard behind it.

`wf check` on a signed-off pass now says, in plain words, that it was signed off (by whom, at which entry, with which outcome; the signer and outcome come from the log, so they are shown escaped), that nothing was written, and that the next step is `wf close`. If the pass changed while the checks ran, it says what state the pass is in now, and to run `wf check` again.

[code: cmd.rs:101 (`no_part`), :551 and :588 (signed off), :591 (changed while the checks ran)]

### 3.4 Small fixes that came with it

- An overlap error for pass 100 says "pass 100", never "05.100". [cmd.rs:119 `pass_label`]
- A bad page address is shown escaped in every error. [page.rs:93]
- `wf observe` no longer says "stalled" because an entry has no time. Its other output is unchanged. [status.rs:120]

---

## 4. Out of scope (on purpose)

1. **A second signoff is allowed.** It is how Prime answers a face 01 change before close. There is no un-signoff, and the latest signoff governs. Two existing tests use this path. [tests `close_passed_reruns_signoff_refusals`, `close_passed_refuses_face_01_change_after_signoff_even_with_a_stored_note`]
2. **Roles are not checked on read.** The order check does not ask who wrote each entry. The commands check roles when they run. Names are still not proven (README, known gaps).
3. **A return's commit is not checked on read.** Only git checks it, when `wf return` runs.
4. **The order check does not prove who wrote the log.** Anyone who can write `log.jsonl` can still rewrite it and its chain.

---

## 5. Waiting on Matthew (`7`)

1. **Board columns, the 24-hour stale limit, and printing git commands instead of running git** (plan Q1-Q3). The code and docs mark them "build stage, pending Director answer". Questions file item 8. Tester flags axiom 1: those lines should not merge into the workflow branch until answered (item 13). `7`
2. **The order rules, and one stuck test page** (item 14). A test page was made with two wf versions: halted by the new one, then packed by the old one, which does not know halt. It is now unreadable, so every write is refused, resume too. No real page has this. Axiom 6 says the past should not block the next step for good. The proposed fix waits for Matthew: new writes always follow the order; a page that already has an out-of-order entry still loads, shows "out of rule at entry N", and allows only resume or a Prime note. We did not change this. `7`
3. **The old binary** `wf-bin/wf-8eb1fdb` can still write pages and does not know halt (item 15). Proposed: rename it so nobody runs it by accident (a rename, not a delete). `7`
4. **Merging** board-dev and harden-dev into `workflow` waits on items 8 and 14 (item 16). `7`

---

## 6. Tests

At bce5cb9: 43 unit tests and 105 end-to-end tests, 0 failed. `sha256_repo_runs_a_full_pass_and_loads` makes a SHA-256 git repo and runs return, check, signoff and close on it; it skips with a message if git has no SHA-256 support (git 2.47.3 here has it, so it ran). The real-pages tests ran and did not skip. They copy 90.10, 90.20 and 90.30, run the board and verify, and check that every file's sha256 is the same after. The default 90.10 board is 40 lines or fewer.

Builds used `CARGO_TARGET_DIR=/workspace/workshop-build/target-builder`, never the pin's folder. `cargo clean -p wf` ran, and the sources were touched, before each final test run.
