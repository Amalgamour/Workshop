# wf commands for Prima: page 90.50.10.0414 pass 1

made: 2026-11-23, 10:45 AM EST, by Cursor-C (Design).
Do not run on the real pages until Matthew grants the page.
t492-t493u is quoted from Prima's statement. The words file is not in the repo yet.

Pack sha256: 4f2851d93c75216ed16660ffc27ab01cca43f934d63d7b8c6e1e683abe3499a9

Scratch dry run passed. grant-ref on that scratch was the word DRYRUN. publish-pack was not run.
This page waits for wave 14 (src/cmd.rs). 0404 is already closed.

```bash
export WF_ROOT=/path/to/wf-run
WF=/path/to/wf
D=/path/to/build-repo/docs/design/drafts/90.50.10.0414
sha256sum $D/FINAL-PACK-0414-05.01.txt
# expect 4f2851d93c75216ed16660ffc27ab01cca43f934d63d7b8c6e1e683abe3499a9

$WF init-page 90.50.10.0414 --title "the work order names its builder; claim raises a different one" --person matthew --prime prima --grant "src/cmd.rs,src/render.rs,templates/v5/prompt.txt,templates/v5/builder.txt" --grant-ref GRANTREF --as matthew
$WF face-write 90.50.10.0414 01 --file $D/FINAL-0414-face01.txt --as prima
$WF face-write 90.50.10.0414 04 --section goals --file $D/FINAL-0414-face04-goals.txt --as prima
$WF face-write 90.50.10.0414 08 --file $D/FINAL-0414-face08.txt --as prima
$WF face-write 90.50.10.0414 06 --file $D/FINAL-0414-face06-note.txt --as prima
$WF draft 90.50.10.0414 --file $D/FINAL-PACK-0414-05.01.txt --as prima
$WF pack 90.50.10.0414 1 --branch returns --as prima
$WF verify 90.50.10.0414
```

Checks, each under cmd /C on Windows: cargo test --lib ; cargo test --test wf
Wave 14. Needs 0404. Files: src/cmd.rs, src/render.rs, templates/v5/prompt.txt, templates/v5/builder.txt.
