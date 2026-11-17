=== WORKSHOP JOB 10.20.30.1211.05.02 ===
Pack hash: 45703723ae7e66a96cae8fa20fc1a4663f1fe02c3fd3a7e3c6fd56a515f5505e (log entry 16, 2026-11-23T16:59:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 02 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.02   Start: 268f31dc6296f464e84357a5b27501f7990b22fa
Read first: pages/10.20.30.1211/05.02/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: make the turn rate ease in
May touch: src/steer.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "clamp(-30, 30)" src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1211/05.02/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1211.05.02.md,
fill it, commit it with your work on pass/10.20.30.1211.05.02, push, then:
  wf return 10.20.30.1211 02 --branch pass/10.20.30.1211.05.02 --commit <sha> --file .workshop/returns/10.20.30.1211.05.02.md --as <your-name>
=== END JOB ===
