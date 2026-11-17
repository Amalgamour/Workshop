=== WORKSHOP JOB 10.20.30.1211.05.03 ===
Pack hash: c7f88bcf414861cf02c93a4b27b72c6e8091b124f5e6f324e97095e91c4afd58 (log entry 24, 2026-11-23T17:07:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 03 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.03   Start: 268f31dc6296f464e84357a5b27501f7990b22fa
Read first: pages/10.20.30.1211/05.03/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: turns stay smooth at speed
May touch: src/steer.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "clamp(-30, 30)" src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1211/05.03/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1211.05.03.md,
fill it, commit it with your work on pass/10.20.30.1211.05.03, push, then:
  wf return 10.20.30.1211 03 --branch pass/10.20.30.1211.05.03 --commit <sha> --file .workshop/returns/10.20.30.1211.05.03.md --as <your-name>
=== END JOB ===
