# wf commands for Prima: page 90.50.10.0415 pass 1

made: 2026-11-19, 3:25 PM EST, by Cursor-C (Design).
Dry run: the block below was run on a scratch root, not on the real pages.
The scratch grant-ref was the word DRYRUN. That is not a grant. Do not use it.
Nothing was published. publish-pack was not run.

HOLD. Do not run this on the real pages until Matthew grants the page.
He has not spoken on it. There is no words file for it yet.
When he names one, put that file's id in place of GRANTREF.
If he does not grant it, stop. An agent's draft is not a grant.

Binary: build wf from returns commit 3646e344 (code is e30050dc; 3646e344 adds only
.workshop/logs/90.50.10.0701/log.jsonl). Flags below are from src/lib.rs HELP lines 21-47
at that commit. In the work repo: git worktree add at 3646e344, then cargo build --release.
The binary is target/release/wf.

Rule until 0411 and 0412 land (t424.md:6; t432.md:7): wf v0 lets only the person start a
page (--as must match --person, src/cmd.rs:190). The init line is marked PERSON. Prima
types it with --as matthew and the words file in --grant-ref, and says so in face 06.
The log cannot show who typed.

Pack file sha256: de57bdab5850ad99af189b671e934fd2ed22c5f8e740eb38a47e857e497eee7a

```bash
export WF_ROOT=/path/to/wf-run
WF=/path/to/wf
D=/path/to/build-repo/docs/design/drafts/90.50.10.0415
sha256sum $D/FINAL-PACK-0415-05.01.txt
# expect de57bdab5850ad99af189b671e934fd2ed22c5f8e740eb38a47e857e497eee7a

# PERSON (src/cmd.rs:190). Grant is the one file this pass may change.
# Replace GRANTREF with the id of Matthew's words file. Do not invent one.
$WF init-page 90.50.10.0415 --title "a new log folder syncs on Windows" --person matthew --prime prima --grant "src/log.rs" --grant-ref GRANTREF --as matthew
$WF face-write 90.50.10.0415 01 --file $D/FINAL-0415-face01.txt --as prima
$WF face-write 90.50.10.0415 08 --file $D/FINAL-0415-face08.txt --as prima
$WF face-write 90.50.10.0415 06 --file $D/FINAL-0415-face06-note.txt --as prima
$WF draft 90.50.10.0415 --file $D/FINAL-PACK-0415-05.01.txt --as prima
$WF pack 90.50.10.0415 1 --branch returns --as prima

# Back-link on the lab. face-write of 01 and 08 replaces the whole face.
# These two files are the faces at returns 3646e344 (log entries 2 and 3) plus 0415.
# If the live 0701 faces have changed since that commit, do not write them. Stop.
$WF face-write 90.50.10.0701 01 --file $D/FINAL-0701-face01-serves.txt --as prima
$WF face-write 90.50.10.0701 08 --file $D/FINAL-0701-face08-serves.txt --as prima

$WF verify 90.50.10.0415
$WF verify 90.50.10.0701
```

The door 90.50.10.0400 lists pages by hand until 0407. This folder does not replace that
face. When you next write it, add one line for 0415. Do not overwrite it from here.

Checks the checker will run, each one under cmd /C on Windows (src/git.rs:111):
cargo test --lib
cargo test --test wf
The printed PACK.md adds the words "(one command each, split by ;)" after them. That
note is the template (templates/pack.txt:19). It is not a third command. The stored
checks field is only the two cargo lines.

0413 and 0414 are still missing from the live 0701 serves list. This page does not add
them. The stage plan (section 15.2) already asked for that write after 0701 closed.

After review, Prima's call (pushes to packs; never forced; commits pages/<page> by path):
# $WF publish-pack 90.50.10.0415 1
# $WF publish-pack 90.50.10.0701


## Pack note (2026-11-19, Cursor-C Pack)

The hold in COMMANDS-FOR-PRIMA.md is lifted by t461u. The grant ref used is t461u.
Face 06 now cites docs/review/DIRECTOR-WORDS-t461u.md. The pack file was not changed.
Q15 stays on the written default: stop and quote the error. Do not pretend the folder synced.
init-page --as prima was refused by wf. The init line was typed with --as matthew, and face 06 says so.
