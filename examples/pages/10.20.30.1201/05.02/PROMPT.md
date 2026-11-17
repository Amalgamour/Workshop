=== WORKSHOP JOB 10.20.30.1201.05.02 ===
Pack hash: 28bfccc75a4ee17d5d93f586d3f5a3ce2df86ec139774f3e4d8338ae3bfd57d8 (log entry 24, 2026-11-23T16:29:00Z)
You are: the builder. Claim first:
  wf claim 10.20.30.1201 02 --as <your-name>
Repo: driving-game   Branch: pass/10.20.30.1201.05.02   Start: 089ad979a4f89727471abefdc7d4d692fb2ce5a0
Read first: pages/10.20.30.1201/05.02/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md
Jobs:
  w01: rate 2 to 3 (decision D-a)
  w02: ignore taps under 50 ms (dead zone)
May touch: src/steer.rs, tests/steer.rs
Must not: anything else (the return check refuses it)
Checks: grep -q "rate = 3" src/steer.rs
Stop if: the tap length lives outside may touch (then end that job `need` or `blocked`, say why)
Hand back: copy pages/10.20.30.1201/05.02/RETURN-TEMPLATE.md to .workshop/returns/10.20.30.1201.05.02.md,
fill it, commit it with your work on pass/10.20.30.1201.05.02, push, then:
  wf return 10.20.30.1201 02 --branch pass/10.20.30.1201.05.02 --commit <sha> --file .workshop/returns/10.20.30.1201.05.02.md --as <your-name>
=== END JOB ===
