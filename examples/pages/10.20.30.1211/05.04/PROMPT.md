=== WORKSHOP JOB 10.20.30.1211.05.04 ===
Pack hash: 94e6c10c3124a13bc883e0b106e10dec8c9358adea7dd6cce6b604ccd8cfd39b (log entry 38, 2026-11-23T17:19:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 04 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.04   Start: 9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
Read first: pages/10.20.30.1211/05.04/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: turns stay smooth at speed
May touch: src/steer.rs, src/physics/grip.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "clamp(-30, 30)" src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1211/05.04/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1211.05.04.md,
fill it, commit it with your work on pass/10.20.30.1211.05.04, push, then:
  wf return 10.20.30.1211 04 --branch pass/10.20.30.1211.05.04 --commit <sha> --file .workshop/returns/10.20.30.1211.05.04.md --as <your-name>
=== END JOB ===
