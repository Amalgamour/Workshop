=== WORKSHOP JOB 90.50.10.0701.05.04 ===
Pack hash: 6c5192505588597d9969e4030dadaac2a9549613bf5433c2813d2ef7d20b8141 (log entry 37, 2026-11-24T20:08:39Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0701 04 --as <your-name>
Repo: work   Branch: returns   Start: 14467f3e79e859b45d8cc5a6789ec00616db4480
Read first: pages/90.50.10.0701/05.04/AGENTS.md (sha256 27551cdb4084), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: Independently trial 0423 one-worker behavior on the released binary through temporary pages and local remotes.
Builder: Grok-1. Checker: Grok-Check.
Done when: A held page allows reads, refuses a second writer on any face and leaves another page free to progress.
Done when: A fresh checker sees the published builder release and can take its own turn.
Done when: A divergent return push leaves the remote log byte-identical and a valid extension is accepted.
Done when: The old override remains readable after succession, current authority controls the next override, and the failed 05.01 build gives the expected negative result.
Done when: cargo test --test lab_0423 passes on Windows. The trial uses the binary and only changes tests/lab_0423.rs plus its standard return.

Jobs:
  w01: In tests/lab_0423.rs, exercise one writer per page with face 05 named, including try-out, a second writer refused even on another face, read-only status or try-out available to that worker with no appended event, and the same worker progressing on a second page while the first stays held. Inspect the generated records. Assert that a refused command leaves the log unchanged.
  w02: Use isolated local remotes and two independent run roots. Exercise the builder return while the builder still holds face 05. Assert the checker is refused until the release. Publish a valid generated suffix through the release. Since wf release is local, the test may place the return work commit on its local fixture branch first, let wf file return without --push and release, verify the exact prefix, and publish the unchanged generated log by path in the fixture. In a fresh checker root intake the log, acquire the checker lock and record the check. Assert the accepted order and actor changes. Report the local publication step as evidence of the current handoff behavior.
  w03: Use a local bare remote for a divergent-log trial. Keep the already published bytes fixed, run the binary's return push path with a conflicting history, and check the prefix refusal plus unchanged remote bytes. Include a valid extension control and distinguish a prefix refusal from a generic non-fast-forward error. Never force push.
  w04: With a synthetic book, record a valid override, rotate the book Prime, and check via the binary that status and verify keep the old log readable and byte-identical. On a fresh lock, show the former Prime is refused and current authority is accepted. Exercise the person-only fallback if the book stamp is absent. Demonstrate a negative control in a disposable checkout of the failed 0423.05.01 build 1b0d2c1 where the same succession scenario fails. Run the positive trial on the returned commit. Record precise commands, results and the refusal messages.
May touch: tests/lab_0423.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --test lab_0423
Done when (face 01): Done when: A held page allows reads, refuses a second writer on any face and leaves another page free to progress.
Done when: A fresh checker sees the published builder release and can take its own turn.
Done when: A divergent return push leaves the remote log byte-identical and a valid extension is accepted.
Done when: The old override remains readable after succession, current authority controls the next override, and the failed 05.01 build gives the expected negative result.
Done when: cargo test --test lab_0423 passes on Windows. The trial uses the binary and only changes tests/lab_0423.rs plus its standard return.
Stop if: the test needs src/, tests/common/mod.rs, a helper file, a real book page, or a shared remote; the 0423 passing build is not in the start; a historical log would need hand editing; a fixture can only pass by dropping live enforcement; or the current return/check handoff differs from the expected evidence. Record the first failing case and what should take it next. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0701/05.04/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0701.05.04.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0701 04 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0701.05.04.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
