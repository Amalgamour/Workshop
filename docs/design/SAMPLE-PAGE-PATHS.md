# Sample page: the harder paths (EXAMPLE)

For Matthew. By Designer. EXAMPLE ONLY. Goes with SAMPLE-PAGE.md (the car steering page).
created: Tue 17 Nov 2026, 12:45 PM EST

## Why this file

- Claude (relayed by Matthew, t253u) asked for the harder paths: a failed review, a refused return, a blocker sent to you (SAMPLE-PAGE-CLAUDE-REVIEW-t253u.md:39-43).
- You asked for three passes (DIRECTOR-WORDS-t250u.md:5). The main sample keeps three. These are extra.
- Every name, hash and time is MADE UP. "(not built yet)" marks unbuilt parts.
- Prime = the team lead role; here Prima (DIRECTOR-WORDS-t254u.md:7).

## Path 1: a review fails, and the rework is a new pass

Pass 05.04 (EXAMPLE): "make the turn rate ease in".

| Step | Who | What happens |
|---|---|---|
| draft, pack, open | Prime writes; compute checks; model A claims | as usual |
| return | model A hands back | w01 says done |
| review | checker C runs `cargo test steer` | test steer_clamps fails: the car reaches 31 degrees |
| review | checker C runs it again on the same commit | fails again: a second fail goes to Prime |
| closed | Prime signs off "failed"; compute closes | outcome `failed` (WL:166) |

Close record (not built yet):
```
cards:       w01 discarded: commit 5aa1c09 not merged
unresolved:  clamp broken by ease-in -> carried to 05.05
live commit: e2f9b40 (unchanged)
```

- The rework is a new pass, 05.05, with predecessor 05.04. The failed pass stays on record (axiom 6).
- Nothing reaches main from a failed pass (branch per pass, proposed, S12).

## Path 2: a return touches a file outside its frame

Pass 05.06 (EXAMPLE). May touch: src/steer.rs, tests/steer.rs.

- model A's commit also changes src/physics/grip.rs.
- The compute's commit check refuses the return (WL:244). Not built yet.
- The tail stays `open`. The return is not recorded.

What model A is told:
```
Return refused: src/physics/grip.rs is outside may touch.
Rule: frame check (pack 05.06, may touch).
Do: send a new commit without it, or end the job `need`
and say why you need it.
```

What Prime is told (feed line):
```
05.06 return refused: out-of-frame file src/physics/grip.rs
```

- If model A ends `need`, it goes up to Prime. If physics is outside your grant, Prime sends it up to you (Path 3).
- Whether a refused return is recorded at all, or only the refusal, is open (ONE-PAGE-WORK.md S6).

## Path 3: a blocker outside the grant goes to you

Pass 05.07 (EXAMPLE). The worker needs to change src/physics/grip.rs. Your grant t300u covers steering and input only.

- model A ends w01 `need`: "grip change needed for smooth turns".
- Prime can't solve it with a better frame: physics is outside the grant (WL:249).
- So it goes to you, as one entry in DECISIONS-WAITING, in four parts.
- 05.07 closes with outcome `needs-authority` (WL:166).

What you see (EXAMPLE):
```
Q: May steering work change src/physics/grip.rs?
Proposed: yes, one function, fn grip_at_speed, for 05.08 only.
Why: turns skid at speed; steering alone can't fix it.
Axioms: 1 pass (you grant it); 2 pass; 9 tension (untried).
Waiting: 05.08 only. Other pages keep moving.
```

- What waits: only the next pass on this page. Other pieces, like 1202.brakes, keep moving.
- Your yes is recorded as a new grant (a t-number). Prime then packs 05.08 with the wider frame.
