=== WORKSHOP JOB 10.20.30.1211.05.03 ===
Pack hash: 53ecc79bd914981f0c11c6c7ed501a3e3b93576f0820380a142283646e9857f3 (log entry 24, 2026-11-23T17:07:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 03 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.03   Start: 9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
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
