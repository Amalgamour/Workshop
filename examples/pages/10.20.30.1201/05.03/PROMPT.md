=== WORKSHOP JOB 10.20.30.1201.05.03 ===
Pack hash: 343e49adfe56162cea7d3b85c10ace1c01917967b163d3ded393969fab64926e (log entry 36, 2026-11-23T16:41:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1201 03 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1201.05.03   Start: 268f31dc6296f464e84357a5b27501f7990b22fa
Read first: pages/10.20.30.1201/05.03/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: smooth the key input in src/input.rs
  w02: ignore taps under 50 ms
May touch: src/steer.rs, src/input.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q smooth src/input.rs; grep -q "rate = 3" src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1201/05.03/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1201.05.03.md,
fill it, commit it with your work on pass/10.20.30.1201.05.03, push, then:
  wf return 10.20.30.1201 03 --branch pass/10.20.30.1201.05.03 --commit <sha> --file .workshop/returns/10.20.30.1201.05.03.md --as <your-name>
=== END JOB ===
