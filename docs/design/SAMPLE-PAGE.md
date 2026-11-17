# Sample page: car steering (EXAMPLE)

For Matthew. By Designer. EXAMPLE ONLY. Nothing here is real work, and nothing is decided.
created: Tue 17 Nov 2026, 12:20 PM EST

## How to read this

- This is one page of the driving game, filled in as it would really look.
- Every address, name, hash, SHA and time is MADE UP and marked EXAMPLE.
- Tags: [compute fills], [prime writes], [worker], [checker], [you].
- "(not built yet)" marks anything that needs spec or code work first.
- Plain words first. Side labels (like WL:166) say where a rule comes from.

## His words

- "Yes we need a sample as done up.  I want to see it laid out because I think we are close." (DIRECTOR-WORDS-t249u.md:7)
- "What I want is the designer to layout a sample for me.  So I can check it before we build it." (t249u:11)
- "I want to see 3 passes. because we need to make sure that is configured correctly." (DIRECTOR-WORDS-t250u.md:5)
- "2. Prime signs off the compute closes it." (t249u:6)
- "We need to establish the MVP goals in the 04 face, with it being stripped down in the 01 for the agent." (DIRECTOR-WORDS-t245u.md:12)
- "Yes it should link to the exact files and locations." (t245u:13)

## Readings (Designer, 7)

- "Prime" is Prima. She signs off. The compute does the close.
- The return order is still open (P1). This sample uses order B (job items first, a one-line summary on top). Labelled, not chosen.
- Names used: builder = "model A" (EXAMPLE). Checker = "checker C" (EXAMPLE). Lab model = "model B" (EXAMPLE).

## The page at a glance

- Address: 10.20.30.1201 (EXAMPLE). Title: steering.
- One page holds the whole piece: faces 00 to 08 (ONE-PAGE-WORK.md, O1).
- Three passes on face 05: 05.01 closed and passed, 05.02 closed and blocked, 05.03 in progress.

## Face 00: stamp

```
address:  10.20.30.1201                 (EXAMPLE)   [compute fills]
title:    steering                                   [compute fills, locked]
type:     workflow   (open: W8 type part, E5)        [compute fills, locked]
state:    live                                       [compute fills]
axioms:   1, 2, 3, 6, 8, 9                           [prime writes]
lineage:  10.20.30.1200 (band head)    (EXAMPLE)     [compute fills]
faces:    01 seated, 02 seated, 03 menu, 04 seated,
          05 counted, 06 counted, 07 counted, 08 seated   [compute fills]
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
Do not touch: physics, rendering, books/.         [prime writes, from 04]
```

## Face 02: light pseudo code

```
on each frame:
  key = read arrow key (smoothed)       -- 05.03 adds smoothing
  if key held less than 50 ms: ignore   -- dead zone
  angle = angle + rate * key            -- rate = 3
  angle = clamp(angle, -30, 30)
                                                    [prime writes]
```

- Drift check: each return says where this no longer matches the code (O9, still open).

## Face 03: the menu (not built yet: the O4 face 03 fix)

```
01 steering card .......... v3
02 pseudo code ............ 5 lines
04 MVP goals / responses / decisions
05 passes: 05.01 closed, 05.02 closed, 05.03 open
06 prime notes: 2
07 labs: 07.01
08 links: 4 files
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

**Prima's decisions, following you** [prime writes]
- D-a, after 05.01: rate 2 to 3. Links: 05.01, your response.
- D-b, after 05.02: add a dead zone and input smoothing; frame widened to src/input.rs (inside your grant). Links: 05.02, 06.02.

## Face 05: the work

### The board (05.00), as it reads now

```
counter  tail     outcome   claim     reviewer
05.01    closed   passed    model A   checker C
05.02    closed   blocked   model A   checker C
05.03    open     -         model A   -
```

- Today the board shows tails only (state.rs:296-300). The other columns are pack 1's job (not built yet).
- You watch this, and the tail feed, as the work goes (not built yet: feed, E3).
- Plain 05 is not seated with a best pass (O6, still open).

### Who acts at each step (every pass)

| Step | Who acts | What is recorded | Goes up if |
|---|---|---|---|
| draft | Prima writes the pack | pack fields [prime writes]; address, by, time [compute fills] | - |
| pack | compute checks the template, takes the pack hash | check result; hash | refused: back to Prima with the why |
| open | worker claims | claim owner; start commit; one-job pass code | - |
| return | worker hands back; Prima reads | return text once; return hash; commit check | `need` or `blocked`: to Prima |
| review | checker runs its tools; a 07 trial if risk calls for it | each check result, with its commit | failed check twice: to Prima |
| closed | Prima signs off; the compute closes (not built yet) | sign-off; outcome | a conflict at any step: halt, raise |

- Prima goes up to you only if she can't solve it with a better frame or authority (t245u:8).

### 05.01: full pack

```
address:     10.20.30.1201.05.01  (EXAMPLE)           [compute fills]
tail:        closed                                    [compute fills]
by:          prima                                     [compute fills]
made at:     Tue 17 Nov 2026 09:00 EST (EXAMPLE)       [compute fills]
pack hash:   a41c...07 (EXAMPLE, made up)              [compute fills]
claim:       model A                                   [compute fills]
baseline:    Amalgamour/driving-game, main,
             start 3b9d2e1 (EXAMPLE, made up)          [compute fills]
pull:        src/steer.rs, tests/steer.rs              [compute fills]
predecessor: none                                      [compute fills]
linked:      10.20.30.1200 band head (EXAMPLE)         [compute fills]
authorized:  t300u (EXAMPLE grant)                     [prime writes; compute checks]
lead:        prima                                     [prime writes]
axioms:      2, 8, 9                                   [prime writes]
outcome:     arrow keys turn the car; max 30 degrees   [prime writes]
overview:    first feel of the game; see 04            [prime writes]
may touch:   src/steer.rs, tests/steer.rs              [prime writes]
must not:    src/physics/, src/render/, books/         [prime writes]
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
w01 done:    steer at rate 2. Created: src/steer.rs.
             Proof: commit 7c41aa0 (EXAMPLE), test steer_turns ok.
             Deviation: none.                          [worker]
w02 done:    clamp at 30. Changed: src/steer.rs:14-18.
             Proof: commit 7c41aa0, test steer_clamps ok.  [worker]
noticed:     a 1-frame tap gives a 2-degree twitch.    [worker]
questions:   none. Permission asked: none.             [worker]
did not do:  smoothing (not asked).                    [worker]
notes:       rate 2 may feel slow; why: 15 frames to full turn.  [worker]
cost:        12 min, 2 tries, 40k tokens, $0.30 (EXAMPLE)  [worker]
02 drift:    none.                                     [worker]
unprompted:  a test for both keys held at once.        [worker]
overflow:    none, why: job was small.                 [worker]
return hash: 5d0e...c2 (EXAMPLE, made up)              [compute fills]
commit check: 7c41aa0 exists, touched only may-touch paths  [compute fills]
```

### 05.01: tail run

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prima writes | 09:00 | pack fields |
| pack | compute checks, hashes | 09:01 | check passed; a41c...07 |
| open | model A claims | 09:05 | claim; start 3b9d2e1 |
| return | model A hands back; Prima reads | 09:17 | return; 5d0e...c2 |
| review | checker C: tests, lint, hash, commit | 09:20 | 4 checks passed |
| closed | Prima signs off; compute closes | 09:22 | outcome `passed` |

### 05.02: what differs (built from what 05.01 taught)

```
address:     10.20.30.1201.05.02  (EXAMPLE)           [compute fills]
predecessor: 05.01                                     [compute fills]
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
- Goes to: Prima. The worker could not solve it inside its frame.
- Prima solves it with a better frame: src/input.rs is inside your grant, so no trip to you. Had it been outside, it would go to you (WL:249).
- Recorded: outcome `blocked` on 05.02 (WL:166); note 06.02; decision D-b on 04; the new frame in 05.03.

### 05.02: tail run

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prima writes | 10:00 | pack fields |
| pack | compute checks, hashes | 10:01 | check passed |
| open | model A claims | 10:04 | claim; start 7c41aa0 |
| return | model A hands back; Prima reads | 10:20 | w02 `blocked`: up to Prima |
| review | checker C checks w01; 07.01 trial on rate 3 | 10:25 | 4 checks passed; trial held |
| closed | Prima signs off; compute closes | 10:30 | outcome `blocked` |

### 05.03: what differs (in progress)

```
address:     10.20.30.1201.05.03  (EXAMPLE)           [compute fills]
tail:        open                                      [compute fills]
claim:       model A, 11:05 (EXAMPLE)                  [compute fills]
predecessor: 05.02                                     [compute fills]
overview:    05.02 w02 blocked; frame widened (D-b)    [prime writes]
w01:         smooth the key input in src/input.rs      [prime writes]
w02:         ignore taps under 50 ms                   [prime writes]
may touch:   src/steer.rs, src/input.rs, tests/steer.rs  [prime writes]
```

### 05.03: tail run so far

| Step | Who | When (EXAMPLE) | Recorded |
|---|---|---|---|
| draft | Prima writes | 11:00 | pack fields |
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
```

## Face 07: labs (not built yet: face 07 spec and code steps)

```
07.01  trial of 05.02 w01 (return hash 9b3a...11, EXAMPLE)
       by: model B (not model A, the builder)        [compute fills]
       try: hold right key 10 s; tap 1 ms x 100      [prime writes]
       result: never past 30 degrees. Taps twitch 2 degrees
               (known; 05.03 fixes)                  [worker: model B]
       outcome: held                                 [checker]
```

- Face 07 needs seqAddr.md 5.1, 5.2, 5.7, decisions.md A4.3, face.rs:72-85 first. Today validate.rs:229-234 refuses it.

## Face 08: links to exact files and lines (EXAMPLE paths)

```
src/steer.rs:1-40      steering, checked at e2f9b40   [compute fills]
src/steer.rs:14-18     the 30-degree clamp            [compute fills]
src/input.rs:1-25      key input (05.03 will change)  [compute fills]
tests/steer.rs:1-60    steer tests                    [compute fills]
10.20.30.1200          band head (EXAMPLE)            [compute fills]
```

## The printed AGENTS.md (made from the 01 card, O5)

```
# AGENTS.md  (printed by the compute; do not edit)
from:    10.20.30.1201.01  steering card, version 3
hash:    1f2e...9a  (EXAMPLE, made up)
printed: Tue 17 Nov 2026 11:05 EST for 05.03 (EXAMPLE)

Goal: the car turns left and right with the arrow keys.
Max turn: 30 degrees. Turn rate: 3 degrees per frame.
Small key taps under 50 ms do nothing (dead zone).
Done when: tests in tests/steer.rs pass, and the car
  never turns past 30 degrees.
Do not touch: physics, rendering, books/.
```

## The prompt box Prima hands you (for 05.03)

```
=== WORKSHOP JOB 10.20.30.1201.05.03 === (EXAMPLE)
Sheet: made 11:05 EST from log line 212. Pack hash 88e1...4d.
Door: open (K8 step 1 not done). Records are not proof.
You are: model A. Claim: model A.
Repo: Amalgamour/driving-game  Branch: main  Start: e2f9b40
Read first: AGENTS.md (version 3, hash 1f2e...9a)
Pack: 10.20.30.1201.05.03  Tail: open
Linked: 10.20.30.1200 band head (linked)
Earlier returns: 05.01 passed; 05.02 blocked (w02)
Jobs: w01 smooth key input; w02 dead zone 50 ms
Stop if: the turn needs a physics change
Not available: none
Hand back: one return, in the return template order,
in the return file in your pushed commit (P6). Do not edit AGENTS.md.
=== END JOB ===
                       [compute fills all of it; values EXAMPLE]
```

## Not built yet (what this sample depends on)

- Face 03 menu off pages 0001-0099: seqAddr.md:189, validate.rs:352-354 (O4).
- Face 07 labs: seqAddr.md 5.1, 5.2, 5.7; decisions.md A4.3; face.rs:72-85; validate.rs:229-234.
- Prima signs off, the compute closes: store.rs:991-992 (E2).
- The tail feed, and board columns beyond the tail (E3, pack 1).
- Templates, the check step, hashes, the AGENTS.md print, the return file road (PACK-TEMPLATE.md section 6).

## What the sample showed that doesn't fit

Raised as four-part questions in ONE-PAGE-WORK.md: S1 (who may sign off), S2 (face 00 role and set), S3 (where 02 drift sits in the return), S4 (AGENTS.md: the card or the pack).
