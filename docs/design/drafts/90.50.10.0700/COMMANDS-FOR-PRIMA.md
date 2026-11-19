# wf commands for Prima: 0700 door, 0701 lab pass 1, 0400 face 01 v3

made: 2026-11-19, 2:19 PM EST, by Designer. Not run against wf-run-gh by Designer; dry run
only, on a scratch copy (FINAL-RELEASE-CHECK.md). Every flag is from src/lib.rs HELP
(:21-47) and src/cmd.rs at returns c09fa60c.

Binary: /workspace/workshop-build/wf-bin/wf-d9110934 (sha256 8df6ebe93b56...). It is
built from code commit d9110934; c09fa60c adds only .workshop/logs/90.50.10.0403/log.jsonl
(git diff --name-only d9110934 c09fa60c), and its help text matches a fresh build at
c09fa60c. To build it yourself: git worktree add /tmp/wf-c09 c09fa60c in wf-run-gh/work,
then cargo build --release there; the binary is target/release/wf.

Rule until 0411 and 0412 land (t424.md:6 Q1; t432.md:7 Q8 "The real runner records my
grant and cites my words file"): wf v0 lets only the person start a page (--as must
match --person, src/cmd.rs:190) and only the person grant (must_be person,
src/cmd.rs:221). So the lines marked PERSON log actor matthew. Either Matthew runs them,
or Prima, as the real runner, types them with --as matthew and the words file in
--grant-ref, and says so in face 06 (the 0701 note does). The log cannot show who typed.
No separate wf grant is needed: init-page --grant records the grant (src/cmd.rs:195-199).

```bash
export WF_ROOT=/workspace/workshop-build/wf-run-gh
WF=/workspace/workshop-build/wf-bin/wf-d9110934
D7=/workspace/workshop-build/repo/docs/design/drafts/90.50.10.0700
D4=/workspace/workshop-build/repo/docs/design/drafts/90.50.10
sha256sum $D7/FINAL-PACK-0701-05.01.txt   # expect 5a2da32f9179413bfcaca25f5c1e04546a8b09e468a0f8b75892c5247aafc18c

# 0700, lab band door (no pass, ever)
# PERSON (src/cmd.rs:190). Without --system it is refused: NN00 (src/addr.rs:102)
$WF init-page 90.50.10.0700 --title "lab band door 90.50.10.07xx: labs reusable by every stage" --person matthew --prime prima --grant "none/" --grant-ref t434 --system --system-ref t432u --as matthew
$WF face-write 90.50.10.0700 01 --file $D7/FINAL-0700-face01.txt --as prima
$WF face-write 90.50.10.0700 08 --file $D7/FINAL-0700-face08.txt --as prima

# 0701, wf loop lab, pass 1
# PERSON (src/cmd.rs:190); grant tests/ is set here
$WF init-page 90.50.10.0701 --title "wf loop lab: one harness, every wf trial" --person matthew --prime prima --grant "tests/" --grant-ref t432u --as matthew
$WF face-write 90.50.10.0701 01 --file $D7/FINAL-0701-face01.txt --as prima
$WF face-write 90.50.10.0701 08 --file $D7/FINAL-0701-face08.txt --as prima
$WF face-write 90.50.10.0701 06 --file $D7/FINAL-0701-face06-note.txt --as prima   # draft needs a new 06 note (src/cmd.rs:297-298)
$WF draft 90.50.10.0701 --file $D7/FINAL-PACK-0701-05.01.txt --as prima
$WF pack 90.50.10.0701 1 --branch returns --as prima

# 0400, band door face 01 v3 (after v2, entry 4)
$WF face-write 90.50.10.0400 01 --file $D4/FINAL-0400-face01-v3.txt --as prima

$WF verify 90.50.10.0700; $WF verify 90.50.10.0701; $WF verify 90.50.10.0400

# Prima's call after review (pushes to packs; never forced, commits pages/<page> by path):
# $WF publish-pack 90.50.10.0700; $WF publish-pack 90.50.10.0701 1; $WF publish-pack 90.50.10.0400
```

Before running: wf-run-gh has changes not made by Designer (pages/90.50.00.0001/00.md and
log.jsonl modified; pages/90.50.10.0401/ and 0402/ untracked). publish-pack commits by
path, so they stay out, but Prima should know they are there.
