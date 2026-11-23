# wf commands for Prima: page 90.50.10.0417 pass 1

made: 2026-11-23, 10:45 AM EST, by Cursor-C (Design).
Do not run on the real pages until Matthew grants the page, and do not pack it until 0413 has closed.
t492-t493u is quoted from Prima's statement. The words file is not in the repo yet.

Pack sha256: bf70059db131de638c523b0fe334807a6df74001966f561dd6bb1dd4857d166f

Scratch dry run passed. grant-ref on that scratch was the word DRYRUN. publish-pack was not run.

```bash
export WF_ROOT=/path/to/wf-run
WF=/path/to/wf
D=/path/to/build-repo/docs/design/drafts/90.50.10.0417
sha256sum $D/FINAL-PACK-0417-05.01.txt
# expect bf70059db131de638c523b0fe334807a6df74001966f561dd6bb1dd4857d166f

$WF init-page 90.50.10.0417 --title "the packs folder updates on every return" --person matthew --prime prima --grant "src/cmd.rs,src/git.rs" --grant-ref GRANTREF --as matthew
$WF face-write 90.50.10.0417 01 --file $D/FINAL-0417-face01.txt --as prima
$WF face-write 90.50.10.0417 04 --section goals --file $D/FINAL-0417-face04-goals.txt --as prima
$WF face-write 90.50.10.0417 08 --file $D/FINAL-0417-face08.txt --as prima
$WF face-write 90.50.10.0417 06 --file $D/FINAL-0417-face06-note.txt --as prima
$WF draft 90.50.10.0417 --file $D/FINAL-PACK-0417-05.01.txt --as prima
$WF pack 90.50.10.0417 1 --branch returns --as prima
$WF verify 90.50.10.0417
```

Checks, each under cmd /C on Windows: cargo test --lib ; cargo test --test wf
Wave 16, after trial 0414. 0414 stays at wave 14. Files: src/cmd.rs, src/git.rs.
Needs 0413 closed.
