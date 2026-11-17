# Workflow design: the core (for every model)

Short form of the agreed design. Read it with AXIOMS.md before any work.
Sources are on Amalgamour/Workshop, branch prima/build. Cites read
`file:lines @commit`. Commit 9ac8d58 is the design as built here
(steps 1-7, T7, T8). Files under docs/design/ and docs/review/.
"Working path" means proposed and used by wf v0, not a ruling.

## 1. One page per piece of work
- Each piece of work gets one page (DIRECTOR-WORDS-t239u.md:11 @9ac8d58).
- The page holds the tool ("compute"). People and models sit outside.
  They reach a face only through the tool (DIRECTOR-WORDS-t262u.md:5-7;
  WORKFLOW-TOOLS.md:30-33 @9ac8d58).
- Several models may work one page at once (t262u, same lines).

## 2. The faces (DIRECTOR-WORDS-t243u.md; ONE-PAGE-WORK.md:151-165 @9ac8d58)
| Face | Holds | Written by (through wf) |
|---|---|---|
| 00 stamp | address, title, person, current Prime, previous Primes, grant | wf, from the log (t255u:7) |
| 01 agents card | the MVP, stripped down for the agent | Prime (t245u:12) |
| 02 pseudo code | light design of the code | Prime |
| 03 menu | what is on the page | wf only (ONE-PAGE-WORK.md:160) |
| 04 dev space | MVP goals, the person's responses, Prime's decisions | Prime (goals, decisions); person (responses) |
| 05 work | passes 05.01, 05.02 ... each pack, return, check, close | wf, from the pass commands (t239u:11) |
| 06 prime notes | Prime's notes, one before each draft | Prime |
| 07 labs | trials (not built in wf v0) | - |
| 08 connections | links to exact files and commits (t245u:13) | Prime |

## 3. Rule: no direct writes
- The log (`log.jsonl`) is the only truth. Every face file is a view the
  tool prints from it. A hand-edited view is refused
  (WORKFLOW-TOOLS.md:215-239 @9ac8d58).
- Packs, prompts and AGENTS cards are printed from fixed templates with
  pinned versions. Nobody writes them by hand (DIRECTOR-WORDS-t227u.md; S4).
- Status is always built fresh from the log, never stored (W11;
  WORKFLOW-TOOLS.md:175-184 @9ac8d58; t259u:11).

## 4. Roles
- **Person** (Matthew): holds authority; grants scope; answers big issues (axiom 1).
- **Prime**: the team lead (DIRECTOR-WORDS-t254u.md:7). Drafts passes and signs off (t249u:6, t259u:10).
- **Builder**: a model that claims a pass and does the work on its own branch.
- **Checker**: the lead's assistant. The tool hands it each return. It checks
  with tools and reports (DIRECTOR-WORDS-t263-T6.md:7, :25; t245u:10). Never the builder.
- **Observer**: watches Prime for drift from the goals and MVP, and for loops
  and stalls (DIRECTOR-WORDS-t263-T6.md:26; WORKFLOW-TOOLS.md:194-213 @9ac8d58).
  Separate from the checker (t264u). Never the Prime it watches.

## 5. A pass: draft > pack > open > return > review > closed
1. **Before drafting**, Prime reads face 04, face 06 and the last closed
   05, then writes a 06 note (t259u:7; WORKFLOW-TOOLS.md:96-110 @9ac8d58).
2. **Draft.** The tool pins 04, 06 and the last closed 05 (entry + hash).
3. **Pack.** The tool checks every field, that may-touch sits inside the
   grant, and that no pin is stale. Then it prints the pack, prompt box
   and AGENTS card (WORKFLOW-TOOLS.md:83-95).
4. **Open.** A builder claims it. First claim wins.
5. **Return.** The builder works on `pass/<page>.05.<NN>`, writes one return
   file, commits, pushes, then pings the tool (t259u:12). The tool checks the
   commit, the file, and that every changed file is inside may-touch
   (WORKFLOW-TOOLS.md:122-140). A failure records only the refusal (SAMPLE-PAGE-PATHS.md, Path 2).
6. **Review.** The checker runs the pack's checks and reports per check,
   per job and per "done when" line, plus anything out of frame.
   Working path T7: if all pass, Prime signs from the report; otherwise
   Prime reads the full return (WORKFLOW-TOOLS.md:324-328 @9ac8d58).
7. **Closed.** Prime signs off. The tool checks the signer was Prime on face 00
   at that log entry, then writes the close record: pack hash, return hash,
   commit, check evidence, outcome, and what happened to each job card
   (accepted, carried, discarded, candidate) (WORKFLOW-TOOLS.md:162-173).
   Outcomes: passed, failed, blocked, needs-authority.

## 6. The return (order used by wf v0)
`pack:` (the pack hash), `done:`, `changed:` (create/modify each file),
`noticed:`, one line per job `wNN: done|need|blocked - ...`, `proof:`,
`not done:`, then `unprompted:` and `overflow:` at the end.

## 7. Going up (DIRECTOR-WORDS-t245u.md:8; ONE-PAGE-WORK.md:105-120 @9ac8d58)
- Worker can't solve it: end the job `need` or `blocked`. The tool sends it to Prime.
- Prime can't solve it with a better frame or more authority inside the
  grant: Prime sends it to the person. Only big issues reach the person.
- Only that pass waits. Other pages keep moving.
- Observer findings (working path T8): one finding with its evidence, filed
  by the tool. It stops nothing (WORKFLOW-TOOLS.md:330-334 @9ac8d58).
