# wf commands for Prima: page 90.50.10.0405 pass 1

made: 2026-11-23, 10:30 AM EST, by Cursor-C (Design).
Job from Prima, Nov 23 10:22 AM EST.
The block below is for the real pages only after Matthew grants the page.
There is no words file for this page yet. Replace GRANTREF with the id he names.
Do not invent one. If he does not grant it, stop.

Binary: build wf from returns a823ee28. Flags are from src/lib.rs HELP at that commit.
3646e344-era help still matches init-page, face-write, draft and pack (src/lib.rs:23-28
at a823ee28). 0404 did not change those lines.

Pack file sha256: 0893a08f98b7778bd4a47111fec5ba766038bb96d12ed8401b74e67c2ce358c3

Until 0411 and 0412 land, wf lets only the person start a page (--as must match
--person, src/cmd.rs:190 at 0e7708d3). The init line is marked PERSON. Prima types it
with --as matthew and says so in face 06.

```bash
export WF_ROOT=/path/to/wf-run
WF=/path/to/wf
D=/path/to/build-repo/docs/design/drafts/90.50.10.0405
sha256sum $D/FINAL-PACK-0405-05.01.txt
# expect 0893a08f98b7778bd4a47111fec5ba766038bb96d12ed8401b74e67c2ce358c3

# PERSON. Grant is the one file this pass may change.
$WF init-page 90.50.10.0405 --title "tests build and run on Windows" --person matthew --prime prima --grant "tests/wf.rs" --grant-ref GRANTREF --as matthew
$WF face-write 90.50.10.0405 01 --file $D/FINAL-0405-face01.txt --as prima
$WF face-write 90.50.10.0405 04 --section goals --file $D/FINAL-0405-face04-goals.txt --as prima
$WF face-write 90.50.10.0405 08 --file $D/FINAL-0405-face08.txt --as prima
$WF face-write 90.50.10.0405 06 --file $D/FINAL-0405-face06-note.txt --as prima
$WF draft 90.50.10.0405 --file $D/FINAL-PACK-0405-05.01.txt --as prima
$WF pack 90.50.10.0405 1 --branch returns --as prima
$WF verify 90.50.10.0405
```

The check wf will run, under cmd /C on Windows (src/git.rs:111): cargo test --test wf
The proof is that command's output on Windows, written on the return proof line.
A Linux run of the same command is not the proof. The checker judges the proof line.

The door 0400 and the lab 0701 get this page on their faces when those faces are next
written. This folder does not replace them. 0701's live serves list is a replace of the
whole face. Do not write it from here.

After review, Prima's call. Never forced. Commits pages/90.50.10.0405 by path:
# $WF publish-pack 90.50.10.0405 1
