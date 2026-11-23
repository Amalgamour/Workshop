# wf commands for Prima: page 90.50.10.0413 pass 1

made: 2026-11-23, 10:45 AM EST, by Cursor-C (Design).
Do not run on the real pages until Matthew grants the page. t461u is on file. t492-t493u is not.
Replace GRANTREF with the words-file id he names.

Pack sha256: b10dc873a88d9bcf234e8c210214d5ca5f635b3d2338e56c865596785fc5323c

Scratch dry run passed (init, faces 01, 04, 08, 06, draft, pack, verify). grant-ref on that scratch was the word DRYRUN. publish-pack was not run.

```bash
export WF_ROOT=/path/to/wf-run
WF=/path/to/wf
D=/path/to/build-repo/docs/design/drafts/90.50.10.0413
sha256sum $D/FINAL-PACK-0413-05.01.txt
# expect b10dc873a88d9bcf234e8c210214d5ca5f635b3d2338e56c865596785fc5323c

$WF init-page 90.50.10.0413 --title "work order view: 05.NN reads as one record" --person matthew --prime prima --grant "src/render.rs" --grant-ref GRANTREF --as matthew
$WF face-write 90.50.10.0413 01 --file $D/FINAL-0413-face01.txt --as prima
$WF face-write 90.50.10.0413 04 --section goals --file $D/FINAL-0413-face04-goals.txt --as prima
$WF face-write 90.50.10.0413 08 --file $D/FINAL-0413-face08.txt --as prima
$WF face-write 90.50.10.0413 06 --file $D/FINAL-0413-face06-note.txt --as prima
$WF draft 90.50.10.0413 --file $D/FINAL-PACK-0413-05.01.txt --as prima
$WF pack 90.50.10.0413 1 --branch returns --as prima
$WF verify 90.50.10.0413
```

Checks, each under cmd /C on Windows: cargo test --lib ; cargo test --test wf
Wave 6, beside 0409. May touch src/render.rs only.
The packs push on return is page 0417, not this one.
