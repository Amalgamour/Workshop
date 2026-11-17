=== WORKSHOP JOB 10.20.30.1201.05.01 ===
Pack hash: 8f7767f29573203adc3eda16cf564f4752c85b3cf0abd0ef5b47352ef806b441 (log entry 10, 2026-11-23T16:11:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1201 01 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1201.05.01   Start: 3dcfc7160ad5849b5179f2f0111df90ef85340e2
Read first: pages/10.20.30.1201/05.01/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: steer left and right at rate 2
  w02: clamp the angle at 30 degrees
May touch: src/steer.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "rate = 2" src/steer.rs; grep -q clamp src/steer.rs
Stop if: the turn needs a physics change (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1201/05.01/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1201.05.01.md,
fill it, commit it with your work on pass/10.20.30.1201.05.01, push, then:
  wf return 10.20.30.1201 01 --branch pass/10.20.30.1201.05.01 --commit <sha> --file .workshop/returns/10.20.30.1201.05.01.md --as <your-name>
=== END JOB ===
