# Dev journal: the first WF loop over GitHub (rehearsal)

date: Thu 19 Nov 2026, about 12:40-1:00 PM EST. written by: Prima builder-b21.
spec: docs/spec/WF-GITHUB-LOOP.md. Status: build stage.

Why: t400u/t401u, Matthew wants to hand builders work over GitHub now; t402u, the minimum loop first,
glitchy is fine. One end-to-end run on the box, with a local bare repo standing in for GitHub, one clone
as Prima and one as the builder. Nothing was pushed to GitHub.

Script: the steps below, run by bash. Transcript (exact output):

```

## GitHub stand-in: bare repo with a returns branch (code) and a packs branch (pages)

## Prima's run folder (box): packs checkout, with work/ = returns checkout

## Builder's run folder (stands in for Matthew's Windows machine)

## Prima: page, faces, draft, pack on the shared returns branch, publish
$ /workspace/workshop-build/target-wf-functional/debug/wf init-page 10.20.30.1301 --title steer rehearsal --person mat --prime prima --grant src/ --grant-ref t401u --as mat
page 10.20.30.1301 started. Next: Prime writes 01 and 04 goals.
$ /workspace/workshop-build/target-wf-functional/debug/wf face-write 10.20.30.1301 04 --section goals --text steering rate doubles --as prima
$ /workspace/workshop-build/target-wf-functional/debug/wf face-write 10.20.30.1301 01 --text Goal: steering rate is 2.
Done when: src/steer.rs says rate = 2. --as prima
$ /workspace/workshop-build/target-wf-functional/debug/wf face-write 10.20.30.1301 06 --text first loop over GitHub (t401u) --as prima
$ /workspace/workshop-build/target-wf-functional/debug/wf draft 10.20.30.1301 --file /tmp/wfr/pack.txt --as prima
drafted 05.01. Next: wf pack 10.20.30.1301 1 --as prima
(job box printed; BUILDER-PROMPT.md written)
$ /workspace/workshop-build/target-wf-functional/debug/wf publish-pack 10.20.30.1301 1
published 10.20.30.1301.05.01 to packs (a169ce1)

## Builder: follows BUILDER-PROMPT.md
$ git checkout -- pages
$ git pull -q --ff-only origin packs
$ git -C work fetch -q origin
$ /workspace/workshop-build/target-wf-functional/debug/wf claim 10.20.30.1301 1
claimed 05.01. Read pages/10.20.30.1301/05.01/PROMPT.md and pages/10.20.30.1301/05.01/AGENTS.md
$ git -C work switch -q -c work/10.20.30.1301.05.01 5cad9654e1a0706ba6ac9abe5628438610785ead
$ git -C work add -- .workshop/returns/10.20.30.1301.05.01.md src/steer.rs
$ git -C work commit -qm 10.20.30.1301.05.01: rate 2
$ /workspace/workshop-build/target-wf-functional/debug/wf return 10.20.30.1301 1 --branch returns --commit cc346fef92936fa01c1b4dd70b2470e3e334d97d --file .workshop/returns/10.20.30.1301.05.01.md --push
return filed on 05.01. Next: a checker runs wf check 10.20.30.1301 1 --as <checker>
pushed returns: your commit, the return file and the page log. Prima picks it up with wf intake.

## Prima: intake, check (Tester's seat), signoff, close, publish
$ /workspace/workshop-build/target-wf-functional/debug/wf intake
10.20.30.1301: took 2 new log entries
ready to check:
  10.20.30.1301 05.01: wf check 10.20.30.1301 1 --as <checker>
$ /workspace/workshop-build/target-wf-functional/debug/wf check 10.20.30.1301 1 --as cat
check 05.01: pass
  check ok: grep -q "rate = 2" src/steer.rs
  frame ok: changed A .workshop/returns/10.20.30.1301.05.01.md, M src/steer.rs
  job w01: done - rate is 2
  done when (01): Done when: src/steer.rs says rate = 2. -> checks ok; the checker judges the rest
$ /workspace/workshop-build/target-wf-functional/debug/wf signoff 10.20.30.1301 1 --outcome passed --as prima
signed off 05.01 passed. Next: wf close 10.20.30.1301 1
cards:      w01 accepted
note:       none
git: A .workshop/returns/10.20.30.1301.05.01.md, M src/steer.rs
$ /workspace/workshop-build/target-wf-functional/debug/wf publish-pack 10.20.30.1301 1
published 10.20.30.1301.05.01 to packs (0855df8)
$ /workspace/workshop-build/target-wf-functional/debug/wf verify 10.20.30.1301
ok: log chain holds (11 entries, head c66df7ad54b3); every view matches the log
  05.01: AGENTS.md hash f8db4e60a887 holds; PROMPT.md hash 03df0d614db9 holds; links 4 hold

## Builder: next pull of packs is clean
$ git checkout -- pages
$ git pull -q --ff-only origin packs
$ /workspace/workshop-build/target-wf-functional/debug/wf verify 10.20.30.1301
ok: log chain holds (11 entries, head c66df7ad54b3); every view matches the log
  05.01: AGENTS.md hash f8db4e60a887 holds; PROMPT.md hash 03df0d614db9 holds; links 4 hold

## GitHub stand-in: branch logs
$ git -C /tmp/wfr/origin.git log --oneline returns
7b0767e wf: return 10.20.30.1301.05.01 (log)
cc346fe 10.20.30.1301.05.01: rate 2
5cad965 code: steer
$ git -C /tmp/wfr/origin.git log --oneline packs
0855df8 wf: publish 10.20.30.1301.05.01
a169ce1 wf: publish 10.20.30.1301.05.01
7eec702 packs: start
```

What it showed: pack, publish-pack, claim, work, return --push, intake, check, signoff, close and publish all ran in one go, and both run folders verify the same 11-entry log. The builder's next `git checkout -- pages` + `git pull --ff-only origin packs` was clean.

Not tried: a lost push race (two builders at once), a merge conflict, Windows itself.
