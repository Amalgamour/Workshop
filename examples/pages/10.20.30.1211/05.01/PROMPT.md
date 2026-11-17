=== WORKSHOP JOB 10.20.30.1211.05.01 ===
Pack hash: 9bdfa9c5f4309709b395c9eb4111f0ceae5ff42ac97b7723a0d8048c20e8e790 (log entry 5, 2026-11-23T16:49:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 01 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.01   Start: 9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
Read first: pages/10.20.30.1211/05.01/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: make the turn rate ease in
May touch: src/steer.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "clamp(-30, 30)" src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1211/05.01/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1211.05.01.md,
fill it, commit it with your work on pass/10.20.30.1211.05.01, push, then:
  wf return 10.20.30.1211 01 --branch pass/10.20.30.1211.05.01 --commit <sha> --file .workshop/returns/10.20.30.1211.05.01.md --as <your-name>
=== END JOB ===
