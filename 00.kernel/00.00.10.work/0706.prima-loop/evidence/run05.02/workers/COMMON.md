# prima-0706-0502 worker rules (shared by Worker A and Worker B)

Assignment: prima-0706-0502 (Codex Prime pack 05.02, sha256 ba68603544018780eb91f6372754085f7da1f85d3bf5b2ab00dd4c923b441b54), dispatched by Prima for the Director (Matthew).

## Inputs
- Frozen source room, read-only: /workspace/prima/run0502/source-room. It holds 87 files, all verified against the pack's bundle hashes.
- Never edit, move or add files there. To probe anything, copy it into your own folder first.

## Your folder
- Write everything under /workspace/prima/run0502/workers/<A or B>/. Nothing outside it.

## Time and usage limits
- This unit has a 25-minute maximum from when you receive this brief. At 25 minutes, write up what you have and stop.
- If you find a finding or hit a blocker, write it to findings.md straight away as a checkpoint, then continue.
- Stop immediately if Prima or the Director tells you to stop. Your partial findings count.

## Allowed methods
- Read the code.
- Write bounded Python stdlib AST/static checks.
- Run isolated pure-function probes on synthetic data in your own folder.

## Not allowed
- Running a production CLI.
- Building a fake D: tree, or doing imports that have side effects.
- Patching source to make it run, or changing expected results after a failure.
- Installing packages.
- Spawning subagents, cloud agents or other bots, or automatic retries.
- git, or publishing anything.
- Contacting anyone except replying to Prima.
- Treating a Windows or fixed-root portability limit as a reason to retry. Record it as evidence instead.

## Deliverables (in your folder)
1. **findings.md**: one entry per finding, in this format:
   - **id:** A-01, B-01 and so on.
   - **fact:** what you found.
   - **evidence:** path, sha256 and line numbers.
   - **method:** read, static check or probe, and exactly which original functions actually ran.
   - **severity and impact**
   - **recommendation**
   - **label:** verified (you ran or checked it yourself) or inferred.
   Honest unknowns and questions you couldn't settle are valid entries.
2. **findings.json**: the same entries as JSON.
3. **probes/**: any probe or extraction code you wrote, plus exact commands with their exit codes and first failures.
4. **SESSION.md**: start and end time with UTC offset, your bot name and agent id, your model identity if you know it ("unknown" if not), the files you read, and checks you skipped and why.

You may challenge this brief if part of it is wrong or impossible; write that in findings.md.

## When done
Reply to Prima in one or two short lines (done, partial or blocked, plus the number of findings). Prima reads your files directly, so don't paste them into the reply.
