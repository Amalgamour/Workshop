WORKSHOP PACK 90.50.10.0701.05.04
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0701 (wf loop lab: one harness, every wf trial)
prime:       prima
predecessor: 05.03
repo:        work
start:       14467f3e79e859b45d8cc5a6789ec00616db4480
branch:      returns
return file: .workshop/returns/90.50.10.0701.05.04.md
grant:       tests/ (t432u)
axioms:      1.4.5.6.7.8.9
outcome:     An independent black-box trial shows the released 0423 binary enforces one active writer per page with a named face, supports a handoff a fresh run folder can follow, and preserves history across divergent pushes and book-Prime succession.
overview:    Builder: Grok-1. Checker: Grok-Check. Page 90.50.10.0701, pass 05.04, trial of 90.50.10.0423. 0423.05.02 closed passed at returns 314bcd2, build bf520780. The lab recovery is 3f8cbd1 and both older dispositions are in the packed start. Use the scenarios in the Grok-1 prep report at 7f5f7b9. Typed by Codex for Prima, t562u. Use pinned a823ee28 for the live work order and the binary built from the trial checkout for the tests. Work on isolated roots and local test remotes. Use the existing test harness where it fits. Its higher level helpers currently assume unlocked writes, so use the lower level command runner and stage each required lock explicitly. Do not copy the harness, change fixtures outside this grant, import internal wf modules into the trial, or use production pages or remotes. This pass uses a single trial file. Report existing suite failures separately. Fill template-4 design review. If wf fails, follow docs/plan/MANUAL-RETURN.md.
jobs:
  w01: In tests/lab_0423.rs, exercise one writer per page with face 05 named, including try-out, a second writer refused even on another face, read-only status or try-out available to that worker with no appended event, and the same worker progressing on a second page while the first stays held. Inspect the generated records. Assert that a refused command leaves the log unchanged.
  w02: Use isolated local remotes and two independent run roots. Exercise the builder return while the builder still holds face 05. Assert the checker is refused until the release. Publish a valid generated suffix through the release. Since wf release is local, the test may place the return work commit on its local fixture branch first, let wf file return without --push and release, verify the exact prefix, and publish the unchanged generated log by path in the fixture. In a fresh checker root intake the log, acquire the checker lock and record the check. Assert the accepted order and actor changes. Report the local publication step as evidence of the current handoff behavior.
  w03: Use a local bare remote for a divergent-log trial. Keep the already published bytes fixed, run the binary's return push path with a conflicting history, and check the prefix refusal plus unchanged remote bytes. Include a valid extension control and distinguish a prefix refusal from a generic non-fast-forward error. Never force push.
  w04: With a synthetic book, record a valid override, rotate the book Prime, and check via the binary that status and verify keep the old log readable and byte-identical. On a fresh lock, show the former Prime is refused and current authority is accepted. Exercise the person-only fallback if the book stamp is absent. Demonstrate a negative control in a disposable checkout of the failed 0423.05.01 build 1b0d2c1 where the same succession scenario fails. Run the positive trial on the returned commit. Record precise commands, results and the refusal messages.
may touch:   tests/lab_0423.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --test lab_0423   (one command each, split by ;)
done when:   Done when: A held page allows reads, refuses a second writer on any face and leaves another page free to progress.
Done when: A fresh checker sees the published builder release and can take its own turn.
Done when: A divergent return push leaves the remote log byte-identical and a valid extension is accepted.
Done when: The old override remains readable after succession, current authority controls the next override, and the failed 05.01 build gives the expected negative result.
Done when: cargo test --test lab_0423 passes on Windows. The trial uses the binary and only changes tests/lab_0423.rs plus its standard return.
stop if:     the test needs src/, tests/common/mod.rs, a helper file, a real book page, or a shared remote; the 0423 passing build is not in the start; a historical log would need hand editing; a fixture can only pass by dropping live enforcement; or the current return/check handoff differs from the expected evidence. Record the first failing case and what should take it next.
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 34, hash 3097491e86cf
  face 06:        entry 35, hash 95adc8de8f94
  last closed 05: 05.03 closed at entry 32
sources:
  face 01:        v6 entry 33 hash 0e94d5e33926
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
