# Sample page: car steering (EXAMPLE)

For Matthew. By Designer. EXAMPLE ONLY. Nothing here is real work, and nothing is decided.
created: Tue 17 Nov 2026, 12:20 PM EST. Version 2: Tue 17 Nov 2026, 12:45 PM EST.

## Change note, v2 (2026-11-17, 12:45 PM EST, Designer)

Folds two reviews relayed by Matthew: Codex (t252u) and Claude (t253u), in docs/review/SAMPLE-PAGE-CODEX-REVIEW-t252u.md and SAMPLE-PAGE-CLAUDE-REVIEW-t253u.md. They are not Matthew's approval. Also his t254u (who Prime is) and t255u (lead on face 00). Lines were changed in place; v1 is commit 068bd51. Each change carries a "v1 had ..." line where it sits. In short:
- New: the "Now" strip; close records; a "cards" column; face 01 history and pins; face 09 history; per-check trial results.
- Changed: Prime labels (t254u:7); lead fields on face 00 (t255u:7); Prime's read after the checker; prompt box and AGENTS.md built from the released pack; cost figures from records; "modify" not "created"; links by name and commit; face 01 holds no scope; branch per pass (proposed).
- The full point-by-point table is in ONE-PAGE-WORK.md, "SAMPLE-PAGE v2 reviews". Harder paths: SAMPLE-PAGE-PATHS.md.

## Change note, v2.1 (2026-11-17, 12:55 PM EST, Designer)

Folds your t263, t264u and t266u (docs/review/DIRECTOR-WORDS-t263-T6.md). Nothing renamed.
- Checker C is the lead's assistant: the compute hands it each return, it checks with tools, Prime signs (WORKFLOW-TOOLS.md, step 3).
- The observer is a separate role that watches Prime for drift, loops and stalls. Added as "Observer (EXAMPLE)" below (WORKFLOW-TOOLS.md, step 7).

## Now (a view the compute builds from the log, never stored; W11; not built yet)

```
live page revision: 41 (EXAMPLE)    live commit: e2f9b40 (EXAMPLE, main)
active pass:  05.03   tail: open    holder: model A
blocker:      none (05.02's w02 blocker was solved by a wider frame)
next:         model A returns 05.03 to the return file (P6)
                                                    [compute fills]
```

## How to read this

- This is one page of the driving game, filled in as it would really look.
- Every address, name, hash, SHA and time is MADE UP and marked EXAMPLE.
- Tags: [compute fills], [prime writes] (Prime = team lead, here Prima), [worker], [checker], [you].
- "(not built yet)" marks anything that needs spec or code work first.
- Plain words first. Side labels (like WL:166) say where a rule comes from.
- Harder paths (a failed review, a refused return, a blocker sent to you): SAMPLE-PAGE-PATHS.md.

## His words

- "Yes we need a sample as done up.  I want to see it laid out because I think we are close." (DIRECTOR-WORDS-t249u.md:7)
- "What I want is the designer to layout a sample for me.  So I can check it before we build it." (t249u:11)
- "I want to see 3 passes. because we need to make sure that is configured correctly." (DIRECTOR-WORDS-t250u.md:5)
- "2. Prime signs off the compute closes it." (t249u:6)
- "We need to establish the MVP goals in the 04 face, with it being stripped down in the 01 for the agent." (DIRECTOR-WORDS-t245u.md:12)
- "Yes it should link to the exact files and locations." (t245u:13)
- "Sorry I ment you.  It's actually the team lead, I have called that position prime.  It seemed to work well with models." (DIRECTOR-WORDS-t254u.md:7)

## Readings (Designer, 7)

- (v1, superseded by t254u:7) "Prime" is Prima.
- The current lead and previous leads sit on face 00 (t255u:7). Field names `prime` and `previous-primes` are proposed; `lead` is taken (lead letters, WL:107; face00.md:205). See ONE-PAGE-WORK.md S1.
- Now: Prime is the team lead role, and on this work Prima holds it (t254u:7). Prime signs off; the compute closes (t249u:6).
- The return order is still open (P1). This sample uses order B (job items first, a one-line summary on top). Labelled, not chosen.
- Names used: builder = "model A" (EXAMPLE). Checker = "checker C" (EXAMPLE). Lab model = "model B" (EXAMPLE).
- (v2.1, t266u) Checker C is Prime's assistant, never the builder (state.rs:578-583). Observer = "observer O" (EXAMPLE), a separate role that watches Prime.

## Face 00: stamp

```
address:  10.20.30.1201                 (EXAMPLE)   [compute fills]
title:    steering                                   [compute fills, locked]
type:     workflow   (open: W8 type part, E5)        [compute fills, locked]
state:    live                                       [compute fills]
axioms:   1,2,3,6,8,9  (six separate pieces, E3)    [prime writes]
lineage:  10.20.30.1200 (band head)    (EXAMPLE)     [compute fills]

## Registry
prime:    prima  (since log entry 180, 09:40)  (EXAMPLE)   [compute fills; who sets it: S14]
previous-primes:                                           [compute fills, from the log]
  - designer   entries 12-179  (EXAMPLE)
  - codex      entries 1-11    (EXAMPLE)
faces:    01 seated, 02 seated, 03 menu, 04 seated,
          05 counted, 06 counted, 07 counted, 08 seated,
          09 log (not built yet)                    [compute fills]
```

## Face 01: the agents card (MVP stripped down for the agent)

```
## Steering
version: 3   (EXAMPLE)                              [compute fills]
hash:    1f2e...9a  (EXAMPLE, made up)              [compute fills]

Goal: the car turns left and right with the arrow keys.
Max turn: 30 degrees. Turn rate: 3 degrees per frame.
Small key taps under 50 ms do nothing (dead zone).
Done when: tests in tests/steer.rs pass, and the car
  never turns past 30 degrees.
                                                  [prime writes, from 04]
```

- v1 had "Do not touch" here. Removed: scope lives in the pack, not 01 (proposed scope rule, S9, open).
- Version history (EXAMPLE) [compute fills]. Who may approve a change to 01 is open (S8):
  - v1: rate 2, max 30. Used by 05.01.
  - v2: rate 3 (decision D-a). Used by 05.02. "Done when" unchanged.
  - v3: dead zone 50 ms (decision D-b). Used by 05.03. "Done when" unchanged.

## Face 02: light pseudo code

```
on each frame:
  key = read arrow key (smoothed)       -- 05.03 adds smoothing
  if key held less than 50 ms: ignore   -- dead zone
  angle = angle + rate * key            -- rate = 3
  angle = clamp(angle, -30, 30)
                                                    [prime writes]
```

- Face 02 is the design, so it can run ahead of the code: "05.03 adds smoothing" is not built yet (proposed, S11, open).
- Drift check: each return says what the code does that 02 does not say, and what 02 says that the code does not do yet (O9, S3).

## Face 03: the menu (not built yet: the O4 face 03 fix)

```
01 steering card .......... v3
02 pseudo code ............ 5 lines
04 MVP goals / responses / decisions
05 passes: 05.01 closed, 05.02 closed, 05.03 open
06 prime notes: 4
07 labs: 07.01
08 links: 4 files
09 log: 31 events (not built yet)
                                                    [compute fills]
```

- The compute writes it. Nobody types it (R35). The states are a view, not a stored copy (W11).

## Face 04: the dev space

**MVP goals, in full** [prime writes, you approve]
- The car steers with the left and right arrow keys.
- It never turns past 30 degrees, either way.
- It feels smooth: no jerk on a tap, no stiffness on a hold.
- Why: steering is the first thing a player feels. If it feels wrong, nothing else matters.

**Your responses** [you] (EXAMPLE words, not yours)
- After 05.01: "feels too stiff."
- After 05.02: "tapping still twitches."

**Prime's decisions (here Prima), following you** [prime writes]
- D-a, after 05.01: rate 2 to 3. Links: 05.01, your response.
- D-b, after 05.02: add a dead zone and input smoothing; frame widened to src/input.rs (inside your grant). Links: 05.02, 06.02.

## Face 05: the work

### The board (05.00), as it reads now

```
counter  tail     outcome   claim     reviewer   cards
05.01    closed   passed    model A   checker C  w01 accepted, w02 accepted
05.02    closed   blocked   model A   checker C  w01 accepted, w02 carried to 05.03
05.03    open     -         model A   -          w01, w02 open
```

- v2 adds the "cards" column, so 05.02's accepted w01 is not lost under `blocked` (Claude A1). The word list (accepted, candidate, discarded, carried) is open (S7).

- Today the board shows tails only (state.rs:296-300). The other columns are pack 1's job (not built yet).
- You watch this, and the tail feed, as the work goes (not built yet: feed, E3).
- Plain 05 is not seated with a best pass (O6, still open).

### Who acts at each step (every pass)

| Step | Who acts | What is recorded | Goes up if |
|---|---|---|---|
| draft | Prime writes the pack | pack fields [prime writes]; address, by, time, face 01 pin [compute fills] | - |
| pack | compute checks the template, takes the pack hash | check result; hash | refused: back to Prime with the why |
| open | worker claims | claim owner; start commit; branch; one-job pass code | - |
| return | worker hands back; the compute records it and routes any `need` or `blocked` item to Prime | return text once; return hash; commit and frame check | `need` or `blocked`: to Prime |
| review | checker runs its tools, starting from the pack and the commit; a 07 trial if risk calls for it; then Prime reads | each check result, with its commit | failed check twice: to Prime |
| closed | Prime signs off; the compute checks the signer was face 00 `prime` at that log entry, then closes (not built yet) | the close record (below) | a conflict at any step: halt, raise |

- Prime goes up to you only if it can't solve it with a better frame or authority (t245u:8).
- v1 had Prima reading before the checker. Moved after, so the checker starts from the pack and the commit, not the builder's story (Claude B15; S13, open).

### 05.01: full pack

```
address:     10.20.30.1201.05.01  (EXAMPLE)           [compute fills]
tail:        closed                                    [compute fills]
by:          prima                                     [compute fills]
made at:     Tue 17 Nov 2026 09:00 EST (EXAMPLE)       [compute fills]
pack hash:   a41c...07 (EXAMPLE, made up)              [compute fills]
claim:       model A                                   [compute fills]
baseline:    Amalgamour/driving-game, branch pass/1201.05.01
             (proposed, S12), start 3b9d2e1 (EXAMPLE)  [compute fills]
face 01:     v1, hash 0c7d...e1 (EXAMPLE, pinned)      [compute fills]
pull:        src/steer.rs, tests/steer.rs              [compute fills]
predecessor: none                                      [compute fills]
linked:      10.20.30.1200 band head (EXAMPLE)         [compute fills]
authorized:  t300u (EXAMPLE grant)                     [prime writes; compute checks]
lead:        3MC (lead letters, WL:107; EXAMPLE)       [prime writes]
axioms:      2,8,9                                     [prime writes]
outcome:     arrow keys turn the car; max 30 degrees   [prime writes]
overview:    first feel of the game; see 04            [prime writes]
may touch:   src/steer.rs, tests/steer.rs              [prime writes]
must not:    everything outside may touch (derived; proposed, S9)  [compute fills]
stop if:     the turn needs a physics change           [prime writes]
grant:       code edits in src/steer.rs, src/input.rs,
             tests/steer.rs; no book writes            [prime writes; compute checks]
risk:        proposed low; floor low; effective low    [prime writes; compute fills]
w01:         steer left and right at rate 2            [prime writes]
w02:         clamp the angle at 30 degrees             [prime writes]
checks:      cargo test steer; no test removed         [prime writes]
read first:  01 card; 04 MVP goals                     [prime writes]
hand back:   return by the return template             [compute fills]
```

### 05.01: return (order B, labelled; P1 still open)

```
summary:     2 of 2 done                               [compute fills]
w01 done:    steer at rate 2. Changed (modify): src/steer.rs.
             Proof: commit 7c41aa0 (EXAMPLE), test steer_turns ok.
             Deviation: none.                          [worker]
w02 done:    clamp at 30. Changed (modify): src/steer.rs,
             fn clamp_angle.
             Proof: commit 7c41aa0, test steer_clamps ok.  [worker]
noticed:     a 1-frame tap gives a 2-degree twitch.    [worker]
questions:   none. Permission asked: none.             [worker]
did not do:  smoothing (not asked).                    [worker]
notes:       rate 2 may feel slow; why: 15 frames to full turn.  [worker]
cost:        12 min, 2 tries (from the log); tokens and
             dollars: not available (no API record yet)  [compute fills]
cost note:   most time went on the clamp test.          [worker]
02 drift:    none.                                     [worker]
unprompted:  a test for both keys held at once.        [worker]
overflow:    none, why: job was small.                 [worker]
return hash: 5d0e...c2 (EXAMPLE, made up)              [compute fills]
commit check: 7c41aa0 exists, touched only may-touch paths,
             "modify" matches files that existed      [compute fills]
```

### 05.01: tail run

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prime writes | 09:00 | pack fields |
| pack | compute checks, hashes | 09:01 | check passed; a41c...07 |
| open | model A claims | 09:05 | claim; start 3b9d2e1 |
| return | model A hands back; compute records | 09:17 | return; 5d0e...c2 |
| review | checker C: tests, lint, hash, commit; then Prime reads | 09:20 | 4 checks passed |
| closed | Prime signs off; compute checks signer, closes | 09:22 | outcome `passed`; close record |

### 05.01: close record (not built yet; S6)

```
pack:        05.01 at hash a41c...07                   [compute fills]
return:      hash 5d0e...c2                            [compute fills]
commit:      7c41aa0 (merged to main; proposed, S12)   [compute fills]
review:      checker C, 4 checks at 7c41aa0: tests ok, lint ok,
             hash ok, commit ok                        [compute fills]
signed off:  prima, face 00 prime at entry 201         [compute fills]
cards:       w01 accepted; w02 accepted                [compute fills]
unresolved:  "tap twitch" (noticed) -> carried to 04   [prime writes]
```

### 05.02: what differs (built from what 05.01 taught)

```
address:     10.20.30.1201.05.02  (EXAMPLE)           [compute fills]
predecessor: 05.01                                     [compute fills]
face 01:     v2, hash 4b88...30 (EXAMPLE, pinned)      [compute fills]
baseline:    branch pass/1201.05.02, start 7c41aa0     [compute fills]
overview:    you said "feels too stiff" (04)           [prime writes]
w01:         rate 2 to 3 (decision D-a)                [prime writes]
w02:         ignore taps under 50 ms (dead zone)       [prime writes]
may touch:   src/steer.rs, tests/steer.rs              [prime writes]
```

Return, what differs:

```
summary:     1 done, 1 blocked                         [compute fills]
w01 done:    rate 3. Proof: commit e2f9b40 (EXAMPLE).  [worker]
w02 blocked: tap length comes from src/input.rs, which
             is outside may-touch. Needs: src/input.rs
             in the frame.                             [worker]
did not do:  w02.                                      [worker]
```

**The elevation in 05.02** (ONE-PAGE-WORK.md, Elevation)
- Signal: a return item ends `blocked` (WL:191).
- Goes to: Prime (here Prima). The worker could not solve it inside its frame.
- Prime solves it with a better frame: src/input.rs is inside your grant, so no trip to you. Had it been outside, it would go to you (WL:249).
- Recorded: outcome `blocked` on 05.02 (WL:166); note 06.02; decision D-b on 04; the new frame in 05.03.

### 05.02: tail run

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prime writes | 10:00 | pack fields |
| pack | compute checks, hashes | 10:01 | check passed |
| open | model A claims | 10:04 | claim; start 7c41aa0 |
| return | model A hands back; compute routes w02 `blocked` to Prime | 10:20 | return; w02 up to Prime |
| review | checker C checks w01; 07.01 trial on rate 3; then Prime reads | 10:25 | 4 checks passed; trial held |
| closed | Prime signs off; compute checks signer, closes | 10:30 | outcome `blocked`; close record |

### 05.02: close record, and what happened to the partial work (not built yet; S6, S7)

```
pack:        05.02 at hash 61f0...2a                   [compute fills]
return:      hash 9b3a...11                            [compute fills]
commit:      e2f9b40                                   [compute fills]
review:      checker C, 4 checks on w01 at e2f9b40; 07.01 held  [compute fills]
signed off:  prima, face 00 prime at entry 233         [compute fills]
cards:       w01 accepted: e2f9b40 merged to main, now live
             w02 carried: not done, goes to 05.03 with a wider frame
             (nothing discarded)                       [compute fills]
live commit: e2f9b40 (main)                            [compute fills]
```

- v1 started 05.03 from 05.02's commit with no word on its fate. Now w01 is accepted at close, so 05.03 starts from live main (Codex 1; Claude B14).

### 05.03: what differs (in progress)

```
address:     10.20.30.1201.05.03  (EXAMPLE)           [compute fills]
tail:        open                                      [compute fills]
claim:       model A, 11:05 (EXAMPLE)                  [compute fills]
predecessor: 05.02                                     [compute fills]
face 01:     v3, hash 1f2e...9a (EXAMPLE, pinned)      [compute fills]
baseline:    branch pass/1201.05.03, start e2f9b40 (live main)  [compute fills]
overview:    05.02 w02 blocked; frame widened (D-b)    [prime writes]
w01:         smooth the key input in src/input.rs      [prime writes]
w02:         ignore taps under 50 ms                   [prime writes]
may touch:   src/steer.rs, src/input.rs, tests/steer.rs  [prime writes]
```

### 05.03: tail run so far

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prime writes | 11:00 | pack fields |
| pack | compute checks, hashes | 11:01 | check passed |
| open | model A claims | 11:05 | claim; start e2f9b40 |
| return | (waiting) | - | - |
| review | (waiting) | - | - |
| closed | (waiting) | - | - |

## Face 06: prime notes

```
06.01  after 05.01: rate 2 works but slow; you said stiff.
       Decision D-a on 04. Links: 05.01.             [prime writes]
06.02  after 05.02: w02 blocked by frame, not by skill.
       Widened to src/input.rs, inside grant t300u.
       Decision D-b on 04. Links: 05.02.             [prime writes]
06.03  spot check: re-ran checker C's tests on 05.01. Same result.
       Picked by rule: first pass on a new page (E4). [prime writes]
06.04  face 01 v2 and v3 follow D-a and D-b. "Done when" unchanged.
       Approval for 01 changes: open (S8).           [prime writes]
```

## Face 07: labs (not built yet: face 07 spec and code steps)

```
07.01  trial of 05.02 w01 (return hash 9b3a...11, EXAMPLE)
       by: model B (not model A, the builder)        [compute fills]
       try: hold right key 10 s; tap 1 ms x 100      [prime writes]
       check 1, clamp: hold right 10 s -> max 30.0 degrees: pass
       check 2, taps: 1 ms x 100 -> twitch 2 degrees: fail,
                known (05.01 noticed), carried to 05.03  [worker: model B]
       outcome: held                                 [checker]
```

- "held" means: the property this trial was for (the clamp) held. It does not mean every check passed. A failed check is carried forward by name, never dropped (Codex 4; Claude A4).

- Face 07 needs seqAddr.md 5.1, 5.2, 5.7, decisions.md A4.3, face.rs:72-85 first. Today validate.rs:229-234 refuses it.

## Face 08: links to exact files and lines (EXAMPLE paths)

- Every link carries its commit. Names first, line numbers as a hint (Claude B13).

```
src/steer.rs           fn steer      at e2f9b40 (lines 1-40)   [compute fills]
src/steer.rs           fn clamp_angle at e2f9b40 (lines 14-18) [compute fills]
src/input.rs           fn read_key   at e2f9b40 (05.03 will change)  [compute fills]
tests/steer.rs         test steer_clamps at e2f9b40           [compute fills]
10.20.30.1200          band head (EXAMPLE)            [compute fills]
```

## Face 09: history (not built yet; S5)

- Today face 09 is "unassigned" (seqAddr.md:158) and the code refuses writes to it (face.rs:72-75; validate.rs:229-234). Your R28 calls 09 the page's log (DIRECTOR-RULINGS.md:113-115). The proposal here: 09 is a view of the book's log for this page, not a second copy (S5).
- One recorded event (EXAMPLE), in the shape of a real log entry today (crates/seqaddr-core/src/log.rs:64-96):

```
{"n":233, "at":"2026-11-17T15:30:02Z", "by":"compute",
 "op":"tail", "addr":"10.20.30.1201.05.02",
 "from":"review", "to":"closed", "outcome":"blocked",
 "for":"prima", "pack":"61f0...2a", "return":"9b3a...11",
 "commit":"e2f9b40", "review":[228,229,230,231]}
                        [compute fills; EXAMPLE values]
```

- n, at, by, op, addr, from, to and outcome exist today. "for" is sent with the close request (store.rs:995). "pack", "return", "commit" and "review" are new (S6).
- The board: for each counter, the compute takes the last tail event. That is how the tail board works today (state.rs:296-300).
- The tail feed: the same events, newest first, one line each. The "Now" strip: the newest open counter, its claim, and any `need` or `blocked` item not yet answered.
- A change of Prime is one more event on face 00. `previous-primes` is built from those events.

## The printed AGENTS.md (S4: proposed this way, Codex t252u; open)

```
# AGENTS.md  (generated by the compute; do not edit)
for:      10.20.30.1201.05.03, pack hash 88e1...4d   (EXAMPLE)
sources:  face 01 steering card v3, hash 1f2e...9a
          pack 05.03 as released, hash 88e1...4d
          kernel rules for workers, rev 12, hash 77aa...03
generated: Tue 17 Nov 2026 11:05 EST                (EXAMPLE)

Goal (01): the car turns left and right with the arrow keys.
Max turn 30 degrees. Turn rate 3 degrees per frame.
Taps under 50 ms do nothing.
Done when (01): tests in tests/steer.rs pass, and the car
  never turns past 30 degrees.
Your job (pack): w01 smooth key input; w02 dead zone 50 ms.
You may touch (pack): src/steer.rs, src/input.rs, tests/steer.rs.
Nothing else.
Rules (kernel): one return; no book writes; do not edit this file.
```

- v1 printed only the 01 card. Now: face 01 gives the short goal; the pack gives the job and its edges; the kernel gives the standing rules. Each source has its version, so an old job can be rebuilt (Codex, t252u:12, :16).

## The prompt box Prime hands you (for 05.03)

```
=== WORKSHOP JOB 10.20.30.1201.05.03 === (EXAMPLE)
Sheet: made 11:05 EST from log line 212. Pack hash 88e1...4d.
Door: open (K8 step 1 not done). Records are not proof.
You are: model A. Claim: model A.
Repo: Amalgamour/driving-game  Branch: pass/1201.05.03
Start: e2f9b40 (live main)
Read first: AGENTS.md (face 01 v3; pack 88e1...4d)
Jobs: w01 smooth key input; w02 dead zone 50 ms
May touch: src/steer.rs, src/input.rs, tests/steer.rs
Must not: anything else (the commit check refuses it)
Checks: cargo test steer; no test removed
Stop if: the turn needs a physics change
Earlier returns: 05.01 passed; 05.02 blocked (w02 carried here)
Not available: tokens and dollars (no API record yet)
Hand back: one return, in the return template order, in
.workshop/returns/1201.05.03.md in your pushed commit (P6).
=== END JOB ===
                       [compute fills all of it, from the released pack]
```

- v1 left out may touch, the checks and the return path, so the worker could not know it may edit src/input.rs (Claude A3).

## Observer (EXAMPLE; not built yet; WORKFLOW-TOOLS.md step 7)

```
watching:     Prime (Prima) on 10.20.30.1201 (EXAMPLE)
passes:       3 on this page (no frame count yet; pass 4 asks the why questions, WL:258-267)
same blocker: none twice (05.02's w02 blocker solved by a wider frame)
goals:        04 pin current; 05.03 works on smoothing, a 04 goal
finding:      none                                  [observer]
```

- Where a finding goes is open (WORKFLOW-TOOLS.md, T8). Whether it reads 06 is open (T5).

## Not built yet (what this sample depends on)

- Face 03 menu off pages 0001-0099: seqAddr.md:189, validate.rs:352-354 (O4).
- Face 07 labs: seqAddr.md 5.1, 5.2, 5.7; decisions.md A4.3; face.rs:72-85; validate.rs:229-234.
- Face 09 history: seqAddr.md:158; face.rs:72-75; validate.rs:229-234 (S5).
- Prime signs off, the compute closes: store.rs:991-992; the signer checked against face 00 `prime` (E2, S1).
- The close record fields (S6), the cards column (S7), branch per pass (S12).
- Face 00 `prime` and `previous-primes`: a new step in face00.md 3.1 (S1).
- The "Now" strip, the tail feed, and board columns beyond the tail (E3, pack 1).
- Templates, the check step, hashes, AGENTS.md generation, the return file road (PACK-TEMPLATE.md section 6).

## What the sample showed that doesn't fit

All in ONE-PAGE-WORK.md as four-part questions:
- S1 answered (t255u:7); the sign-off detail is S14, S15.
- S2 (face 00 role and set), S3 (02 drift in the return), S4 (AGENTS.md, proposed this way by Codex).
- S5 face 09; S6 close record; S7 card words; S8 face 01 approval; S9 scope rule; S10 cost figures; S11 face 02 design or description; S12 branch per pass; S13 Prime's read after the checker.
- (v2.1) T7 what checker C hands Prime; T8 where the observer reports: WORKFLOW-TOOLS.md.

Harder paths: SAMPLE-PAGE-PATHS.md.
