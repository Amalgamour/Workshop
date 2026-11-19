# Local builder flow (t399u, t400u): Prima's design choices

Source: docs/review/DIRECTOR-WORDS-t399u-t400u.md. Matthew reviews these choices and 👍 or changes them (t387u, t390u). Each choice is checked: Better? Stronger? Aligns?

## The flow in one breath
Matthew talks. Prima writes the vision and the page (goal, MVP, done-when), packs a pass with wf, and pushes it to GitHub. Prima hands Matthew **one prompt** to paste into Cursor (or a Grok builder in PowerShell). The builder works 30-50 minutes, runs wf to make the return, and wf pushes it. Every 4 hours a cheap check looks for new returns. When there is one, Prima and Tester review it, then Prima and Matthew talk and move forward.

## Choice 1: where things live on GitHub (Amalgamour/Workshop)
- `prima/build`: docs, words and specs, as now.
- `packs`: only Prima writes here. It holds each page's log and the packed pass (PROMPT.md, AGENTS.md). This is the plan side.
- `returns/<page>.05.NN`: **one branch per pass**, not one shared returns branch. The builder's code commits, the return file, and wf's claim and return log lines all go on it.
- Why one branch per pass: two builders running at once would fight over a single shared branch (push conflicts). With one branch per pass they can't collide, and a pass's work and its return stay together.
- Better: yes. Stronger: yes, and here's a bonus. Prima's `packs` head is a record outside the builder's copy, so wf can check that a return's log *continues* exactly from the packed log. That closes most of Tester's full-rewrite hole for free (axiom 6). Aligns: axiom 1 (only Prima writes packs, builders only their own pass branch), axiom 8 (the return links back to its pack).

## Choice 2: what Matthew does
- Pastes one prompt per pass. Nothing else, and no wf commands by hand (t399u).
- The prompt tells the builder: pull `packs`, read the pass's PROMPT.md and AGENTS.md, claim, work, then run the wf return line, which pushes.
- Builders push only to their own `returns/<page>.05.NN` branch. Never main, never packs, never force push (t335s1296 rules).

## Choice 3: the cheap 4-hour check
- A routine at 8 AM, 12 PM, 4 PM and 8 PM EST on weekdays (Matthew runs builders about 8 hours a day, 5 days a week).
- Each run does one small thing: list the `returns/*` branches on GitHub and compare them with the last list it saw. If nothing changed, it ends silently and does no other work. Only a new or moved return wakes Prima to review.
- Why not a GitHub trigger: the trigger list has no "branch pushed" event. Opening a pull request per return would work, but it adds a step on Matthew's machine. Park that as a later upgrade.
- Better: yes. Stronger: same. Aligns: t349u and t400u (no wasted usage).

## Choice 4: tracking the whole build like a house
- The [roadmap](ROADMAP-2026-11-18.md) stages become a build plan: each stage is a set of pages, each page has its goal, MVP and done-when on face 01, and the WF board (docs/design/WF-BOARD.md) shows every page's state.
- Plan every step first, then execute, and learn on the shop floor: what a pass teaches goes into the page's face 06 note and the next pack.

## What has to be built first (by box builders, on wf)
1. `wf return --push` to the pass branch, plus a `--pull` that fetches the pack. The return check confirms the log continues from the `packs` head.
2. Make the tests run on Windows: 43 tests use `true` as a check, and line-ending rules need settling (`.gitattributes`).
3. A builder prompt template: the one paste, printed by wf with the pack.
4. The 4-hour routine.
5. A first practice pass end to end: Matthew pastes one prompt, and the return comes back through GitHub.
