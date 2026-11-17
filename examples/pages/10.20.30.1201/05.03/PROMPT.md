=== WORKSHOP JOB 10.20.30.1201.05.03 ===
Pack hash: bdfde313c9ebfdb5d8bd33cfece39dbd0afa25acb1cb3975b63e3015e365cc83 (log entry 36, 2026-11-23T16:41:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1201 03 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1201.05.03   Start: 9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
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
