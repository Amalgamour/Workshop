# Triage of the Codex wf review (t275u)

Written: Tue Nov 17 2026, by Prima. The review itself is in CODEX-WF-REVIEW-t275u.md (verbatim).
Tested against: `workflow` commit 693e608, built with CARGO_TARGET_DIR=target-builder.
Repro scripts: `docs/review/t275u-repro/` (each one makes its own temp folder; run with
`WF=<path to wf built from 693e608> ./<script>.sh`). Outputs below are copied from real runs.

This is Prima's reading. Nothing here is a ruling. One question for Matthew is at the end.

## Short answer

Codex was right on every concrete point. All five failures happened when I ran them.
I also found two more: a rename can hide a deleted file outside "may touch", and a failed reprint looks like a hand edit.

| # | Item | Verdict | Fix lands in |
|---|---|---|---|
| P1 | Lock taken after the page is read | Accepted (reproduced: log broke) | 05.04 |
| P1b | init-page has no lock at all | Accepted (13 of 50 runs broke a page) | 05.04 |
| P2 | Unfinished jobs signed off as accepted; open questions ignored | Accepted (reproduced) | 05.05 |
| P3 | Check reads today's face 01, not the packed done-when | Accepted (reproduced) | 05.05 |
| P4 | Missing or unreadable views are skipped by verify | Accepted (reproduced) | 05.06 |
| P4b | A failed reprint after an append is reported as "hand-edited" | Accepted (new, reproduced) | 05.06 |
| P5 | The return's `changed:` line is never matched to git | Accepted (reproduced) | 05.06 |
| P5b | A rename hides a deleted file outside may-touch | Accepted (new, major, reproduced) | 05.06 |
| W | A why is not required at big choices | Accepted in part; rest deferred | 05.05 |
| S | SeqAddr: any label is a page id; passes go past 98 | Accepted as fact; choice is Matthew's (Q-SA) | 05.07 after his answer |
| T1 | Hash chain only shows the log is consistent | Accepted (reproduced); docs fix now, protection later | 05.06 (docs); later (checkpoints) |
| T2 | Torn last line (interrupted append) | Accepted in part: name it and keep it; repair deferred | 05.06 |
| T3 | `--as` is trusted; no merge in v0 | Kept as is (Codex agrees) | none |

---

## P1. Lock taken after the page is read. Accepted.

**What the code does.**
- `main.rs:103` loads the whole page (`Page::load`, page.rs:123-131), and `main.rs:104` checks the view files.
- Only after that does `main.rs:144` take the lock (`main.rs:139` for `observe --record`).
- `Page::add` (page.rs:148-155) appends with the sequence number and head hash it read before the lock.
- `verify --fix` (main.rs:110-112) writes views with no lock.
- `init-page` (main.rs:90-93, cmd.rs:66-72) checks that the log does not exist, then appends, with no lock.

**Evidence 1: a forced race** (`p1-race.sh`). Process B is paused after it loads and before it locks: one view file is a FIFO, so `render::edited` waits on it. Then A claims, and B is let go.
```
-- A claims while B is paused:
claimed 05.01.  [exit 0]
-- B:
claimed 05.01.  B exit 0
{"seq":6,"actor":"pri","kind":"pack","prev":"cd9a7cfcb266"}
{"seq":7,"actor":"alice","kind":"claim","prev":"0efd5674e3f6"}
{"seq":7,"actor":"bob","kind":"claim","prev":"0efd5674e3f6"}
$ wf status 1.2.3.4
wf: log chain broken at line 8: it does not match the line before (tampered?)
```
Both claims "won". The log now has two entry 7s, and every command on the page fails, including `verify`.

**Evidence 2: no tricks** (`p1-loop.sh`, `p1-init.sh`).
```
100 runs: one claim won=100, BOTH claims 'won'=0, log left broken=0, lock refusals seen=73
50 runs: page log got two init lines=13, page left unreadable=13
```
Plain parallel claims did not hit the gap in 100 tries, because the gap is short. But it widens as a page grows, since the view check reads more files. Parallel `init-page` broke 13 pages out of 50. Also, 73 of 100 parallel claims got "another wf command is writing" rather than waiting.

**Fix (05.04).** Take the lock first, then load, check, append and reprint. Lock `init-page` after the folder exists, and look for the log again under the lock. Put `verify --fix` and `observe --record` under the lock. Retry the lock for up to 5 seconds. Add tests that run 8 inits and 8 claims at once.

## P2. Unfinished jobs signed off as accepted. Accepted.

**Code.** `signoff` (cmd.rs:366-389) only checks that a "passed" signoff has a passing check (cmd.rs:374). With `passed`, every job becomes `accepted` (cmd.rs:378). Open elevations are never looked at. The note defaults to "none" (cmd.rs:386).

**Evidence** (`p2-signoff.sh`):
```
check 05.01: pass
  job w01: done - a is 2
  job w02: blocked - b is outside may touch
-- open elevations before signoff:
{"seq":9,"kind":"elevate","data":{"item":"w02 blocked - b is outside may touch","pass":1,"to":"prime"}}
$ wf signoff 1.2.3.4 1 --outcome passed --as pri      [exit 0]
cards:      w01 accepted, w02 accepted
{"cards":{"w01":"accepted","w02":"accepted"},"note":"none","outcome":"passed","pass":1}
  waiting: entry 9 05.01 wf -> prime: w02 blocked - b is outside may touch
```
The close record says the blocked job w02 was accepted, and the question it raised is still open.

**Fix (05.05).** The check report adds "jobs not done: ...". A "passed" signoff is refused while:
- (a) a job is `need` or `blocked` and `--cards` doesn't name it;
- (b) a question to the person on this pass has no answer;
- (c) face 01 changed since the pack.

Choosing a card for an unfinished job, or signing off over drift, also needs `--note "<why> (ref)"`. Questions that went to Prime only (made automatically from need/blocked jobs) are settled by the card choice. That keeps informational questions from blocking.

## P3. Check reads today's face 01. Accepted.

**Code.** `pack` stores `done_when` (cmd.rs:211, :224), and the printed job uses it (render.rs:63). But `check` reads the current face 01 (cmd.rs:338). The observer already notices face 01 drift (status.rs:93-96). The check doesn't.

**Evidence** (`p3-donewhen.sh`): packed "Done when: a is 2."; then face 01 was rewritten.
```
-- packed done_when:
Done when: a is 2.
check 05.01: pass
  done when (01): Done when: a is 3 and b is 9. -> checks ok; the checker judges the rest
```
**Fix (05.05).** The check uses the packed done-when. If face 01 changed, it adds one drift line, using a helper shared with status.rs. A "passed" signoff over drift needs a note (P2, rule c).

## P4. Missing and unreadable views are skipped. Accepted.

**Code.** `render::edited` (render.rs:181-191) skips any file it cannot read (`if let Ok(...)`). Then verify prints "every view matches" (main.rs:108-109).

**Evidence** (`p4-views.sh`): deleted 01.md and 05.01/PACK.md, and made 04.md unreadable:
```
$ wf verify 1.2.3.4
ok: log chain holds (6 entries, head 490c762930be); every view matches the log   [exit 0]
```
**P4b (new).** The next write command (`face-write 06`) appended its log entry, then failed while reprinting (`Permission denied`). The log now has 7 entries, but the views were printed from 6. So the following `verify` reports `hand-edited view files: 02.md, 06.md`, even though nobody edited them.

**Fix (05.06).** Report missing, unreadable and changed views separately. `--fix` reprints missing and changed views. An unreadable file stays an error that names the file. Write commands refuse on any of the three. The message changes to "differs from the log (hand edit or a failed reprint)".

## P5. The `changed:` line is never matched to git. Accepted.

**Code.**
- `parse_return` (cmd.rs:247-262) only needs `changed:` to be non-empty.
- The real list comes from `git diff --name-only` (git.rs:36-38, used at cmd.rs:281). It is stored in the return event, and `check` uses it for the frame (cmd.rs:324).
- AGENTS.md:43-44 says the return file "must be listed in changed", but the tool never checks this.

**Evidence (a)** (`p5-changed.sh`):
```
{"git_changed":[".workshop/returns/1.2.3.4.05.01.md","src/a.rs"],"declared":"changed: create src/zzz.rs, delete src/b.rs"}
```
The return was accepted even though the builder's line describes files that were never touched.

**P5b (new, major).** `--name-only` uses git's rename detection, so a rename shows only its new path. When a builder renames `src/b.rs`, which is outside "may touch", to `src/c.rs`, which is inside, the return is accepted:
```
git diff --name-only (what wf uses, git.rs:37):    .workshop/returns/...  src/c.rs
git diff --name-status --no-renames (the truth):   A .workshop/returns/...  D src/b.rs  A src/c.rs
```
That deletes a file outside the frame, and the scope check never sees it.

**Fix (05.06).**
- Use `--name-status --no-renames`. Keep each path with its letter (A, M, D), and check every path against "may touch".
- Keep the builder's `changed:` line as the builder's own words. Print git's list as the evidence on face 05 and in the close record.
- Change AGENTS.md and the return template to say this.

The review asked for one of two options: check the builder's line against git, or label it as commentary. Labelling is the smaller one.

## W. A why at big choices. Accepted in part.

**Code and evidence** (`why-spots.sh`):
- `--overlap-ok` stores only the other pass number: `{"pass":2,"overlap_ok":1}` (cmd.rs:226-228).
- `set-prime` stores only a name: `{"name":"other"}` (cmd.rs:76-80).
- The signoff note defaults to "none" (cmd.rs:386).
- `grant` already needs `--ref` (cmd.rs:85).

**Accepted now (05.05):**
- `--overlap-ok` needs `--why "<reason> (ref)"`.
- `set-prime` needs `--ref`.
- Signoff needs `--note` when it settles unfinished work, signs over drift, or changes a default card.

**Deferred:** "superseding a task or criterion" and "closure decisions". Re-drafting already needs a fresh 06 note (cmd.rs:120-121, :201), and that note is the why. Adding more required fields now would be paperwork, and Codex warns against that too. We'll look again after the trial of 05.05.

## S. SeqAddr. Accepted as fact; the choice is Matthew's.

**What wf does.**
- `check_addr` (page.rs:91-94) takes any letters, digits, dots, - or _. Pass numbers count up with no cap (cmd.rs:128).

**Evidence** (`seqaddr.sh`):
```
hello            page hello started.
10.20.30.12345   page 10.20.30.12345 started.
99.99.99.9999    page 99.99.99.9999 started.
05.01  05.100  05.98  05.99
```
**The governing source:**
- `docs/spec/seqAddr.md:14`: "Widths are exact" (DD.SS.BB.PPPP.FF).
- `docs/spec/seqAddr.md:24`: counters are "2 digits, 01-98".
- `docs/spec/DIRECTOR-RULINGS.md:38` (R9): "counters run 01-98 only". It overrides the older grammar comment at `seqAddr.md:277` ("00 board, 01-98, 99 continuation").
- What happens after 98 is still an open question (QD16; working path D363, `docs/design/DESIGN.md:42`).
- `crates/seqaddr-core/src/addr.rs:835-837` already enforces R9.

**Proposed (see Q-SA):** wf v0 states plainly that its page ids are **temporary labels**, not SeqAddr. A SeqAddr check comes later through seqaddr-core.
- wf's pass numbers already are face-05 counters, so they follow R9 now: wf refuses past 98, and refuses 0, and the message points at QD16.
- This changes no shared rule. It only applies R9, which Matthew already made.
- Pass 05.07 waits for his answer.

## T. Trust and recovery.

**T1. The hash chain.** Accepted (`chain.sh`). I changed the face 04 goal at entry 2 to "REWRITTEN" and recomputed every `prev`:
```
$ wf verify 1.2.3.4
wf: hand-edited view files: 00.md, 04.md. ...
$ wf verify 1.2.3.4 --fix
reprinted from the log: 00.md, 04.md          [exit 0]
```
The chain still holds, and `--fix` then prints the forged history as the truth. README.md:72 calls verify "Check nothing was tampered", which claims too much.
- **Now (05.06):** reword it, and say the limit in "Not in v0".
- **Later (deferred):** a checkpoint that models cannot rewrite, for example the log head hash written into the git history of the kit repo at each close. That is a design choice, so it belongs with merging (T1 question) and stays out of these passes.

**T2. Interrupted append.** Accepted in part (`chain.sh` b). A half-written last line stops every command, `verify --fix` included:
```
wf: log line 5 is not JSON: EOF while parsing a string at line 1 column 26
```
Refusing is right, because the evidence is kept. But the message is unclear, and `log::append` (log.rs:84-91) never syncs to disk.
- **Now (05.06):** sync after each write, and name the torn line plainly.
- **Deferred:** a repair. It would mean wf cutting `log.jsonl`, and the past is not rewritten (axiom 6). That is Matthew's call, and nothing has needed it yet.

**T3.** `--as` is trusted, and merging is outside v0 (README.md:113-114). Both are kept.

---

## The passes (page 90.10.00.0001)

All four touch `src/cmd.rs` and `tests/`, so they run one at a time: pack refuses overlapping open passes. 05.04 starts at 693e608. The others say `start: workflow`, so each one starts from the merged tip at pack time. Each draft was packed once with the 693e608 tool on a test page, and all four were accepted.

### 05.04 Concurrency
```
predecessor: 05.03
repo: kit
start: 693e608
axioms: 6,9
outcome: two wf commands on one page can never write from stale state; the log chain cannot be broken by timing
overview: Codex review t275u P1 (triage CODEX-WF-REVIEW-t275u-TRIAGE.md). Repro: two claims both "won" and the log broke at line 8; 13 of 50 parallel init-page runs left a page unreadable.
w01: every command that writes takes the page lock BEFORE Page::load and the view check, and keeps it through append and reprint (main.rs:103-144); read-only commands (status, observe without --record, verify without --fix, check --dry-run) take no lock
w02: init-page creates the page folder, takes the lock, then checks log.jsonl does not exist (cmd.rs:66-72); verify --fix and observe --record run under the lock too
w03: Lock::take retries for up to 5 seconds before refusing, so two quick commands queue instead of failing
w04: tests: 8 init-page runs of one page at once leave a readable log with exactly one init; 8 claim runs of one pass at once leave a readable log with exactly one claim
may touch: src/main.rs, src/cmd.rs, tests/
checks: cargo test -q
stop if: the fix needs a new dependency, an OS-specific lock API, or a change to the log format
```

### 05.05 Acceptance and why
```
predecessor: 05.04
repo: kit
start: workflow
axioms: 1,4,7
outcome: a pass cannot be signed off "passed" while work is unfinished, an authority question is open, or the agreement changed, unless Prime says why
overview: Codex review t275u P2, P3 and the why items (triage CODEX-WF-REVIEW-t275u-TRIAGE.md). Repro: w02 blocked + checks ok -> signoff passed -> close says "w02 accepted"; check judged a face 01 written after the pack.
w01: check reads done-when from the pack (pk.done_when), not the current face 01 (cmd.rs:338); if face 01 changed after the pack, the report adds one line "drift: face 01 changed since pack (now vN entry E)"; share one drift helper with status.rs:93-96
w02: check report adds "jobs not done: wNN, ..." when any job is need or blocked, so "checks ok" and "work done" stay separate
w03: signoff --outcome passed is refused while (a) a job is need or blocked and --cards does not name it, (b) an elevation --to person on this pass has no answer, or (c) face 01 drifted; --cards for a not-done job, or drift, also needs --note "<why> (ref)"; default cards stay as now for done jobs
w04: --overlap-ok needs --why "<reason> (ref)", stored with the pack; set-prime needs --ref; signoff --cards that change a default needs --note
w05: tests for w01-w04, including a blocked job with passing checks and an unanswered person elevation; README and AGENTS.md command lines updated
may touch: src/cmd.rs, src/main.rs, src/page.rs, src/status.rs, tests/, README.md, AGENTS.md
checks: cargo test -q
stop if: this needs a new log event kind, a change to old log entries, or a rule about which elevations block that is not (a)-(c) above
```

### 05.06 Integrity and the change list
```
predecessor: 05.05
repo: kit
start: workflow
axioms: 6,7,8
outcome: verify tells missing, unreadable and changed views apart; the changed-file list is git's full truth, renames and deletes included; a torn log line is named, not hidden
overview: Codex review t275u P4, P5 and trust limits (triage CODEX-WF-REVIEW-t275u-TRIAGE.md). Repro: deleted 01.md and PACK.md -> verify "every view matches"; git mv of a file outside may touch was accepted because diff --name-only hid the old path.
w01: render::edited returns missing, unreadable and changed views separately (render.rs:181-191); verify reports each kind; --fix reprints missing and changed; unreadable stays an error naming the file; write commands refuse on any of the three
w02: the "hand-edited" message becomes "differs from the log (hand edit or a failed reprint)", since a failed reprint after an append leaves the same state
w03: git::changed uses git diff --name-status --no-renames (git.rs:36-38), so a rename lists both the deleted and the added path; the return event keeps each path with its letter (A, M, D); every path is checked against may touch
w04: the builder's "changed:" line is kept as the builder's words; face 05 and the close record print the git list as the evidence; AGENTS.md:43-44 and templates/return.txt say the tool takes the list from git and the line is the builder's summary (create, modify, delete)
w05: log::append syncs the file after writing; log::read names a torn last line ("last line is half written: entry N; nothing was changed") and every command, verify --fix included, refuses and leaves the log as it is
w06: README: "Check nothing was tampered" (README.md:72) becomes "check the log chain and views"; Not-in-v0 says the chain shows the log is consistent, not that it was never rewritten: anyone who can write log.jsonl can rewrite and rehash it
w07: tests for w01, w03 (rename out of scope is refused), w05
may touch: src/render.rs, src/git.rs, src/log.rs, src/cmd.rs, src/main.rs, templates/return.txt, tests/, README.md, AGENTS.md
checks: cargo test -q
stop if: repairing a torn line needs wf to rewrite or cut log.jsonl (that is Matthew's call, axiom 6)
```

### 05.07 SeqAddr honesty (only after Matthew answers Q-SA)
```
predecessor: 05.06
repo: kit
start: workflow
axioms: 6,8
outcome: wf says plainly what its page ids are, and its pass numbers obey R9 (01-98)
overview: Codex review t275u SeqAddr item. Run ONLY after Matthew answers the SeqAddr question in CODEX-WF-REVIEW-t275u-TRIAGE.md; if he picks another option, redraft.
w01: draft refuses a new pass number above 98 with "counter 98 reached: after 98 is open (QD16); ask Prime"; refuses pass 0 (R9, DIRECTOR-RULINGS.md:38)
w02: README Not-in-v0 and docs/DESIGN.md: wf v0 page ids are temporary labels, not checked as SeqAddr; a SeqAddr check comes later through seqaddr-core
w03: test: drafting a 99th pass is refused
may touch: src/cmd.rs, tests/, README.md, docs/DESIGN.md
checks: cargo test -q
stop if: the work needs seqaddr-core as a dependency, or any change to SeqAddr docs or rulings
```

---

## Question for Matthew

**Q-SA. What should wf v0 say about page addresses?**
- **The question:** wf takes any label as a page id ("hello" works). Should wf v0 (a) say plainly that its page ids are temporary labels, with a real SeqAddr check added later, or (b) check full SeqAddr addresses now?
- **Proposed answer:** (a). Separately, wf obeys your rule R9 now for its pass numbers: 01 to 98 only.
- **Why:**
  - (b) would tie the tool to the SeqAddr code (seqaddr-core) before the workflow is proven.
  - The page ids wf uses today (`90.10.00.0001`) already look like SeqAddr, so nothing has to be renamed later.
  - R9 is already your ruling, so following it adds no new rule.
- **Axioms check:**
  - 1 (authority): you decide shared design, so this question comes to you.
  - 6 (lineage): no SeqAddr rule is changed or rewritten.
  - 7 (missing): the gap is written down, not hidden.
  - 8 (connection): the later check links to seqaddr-core instead of copying it.
