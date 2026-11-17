=== WORKSHOP JOB 10.20.30.1211.05.02 ===
Pack hash: fb9a09b73d702d15888aeb8285b71b3bb6c771f6d9602e9ec5c3558dbe22c01e (log entry 16, 2026-11-23T16:59:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1211 02 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1211.05.02   Start: 9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
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
