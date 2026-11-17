=== WORKSHOP JOB 10.20.30.1211.05.01 ===
Pack hash: aefed1072d7fb089ca7bf62051255aeb926d95c1b907a8ff5c9187d0724555b5 (log entry 5, 2026-11-23T16:49:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 01 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.01   Start: 268f31dc6296f464e84357a5b27501f7990b22fa
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
