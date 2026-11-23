WORKSHOP PACK 90.50.10.0408.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0408 (withdraw a packed pass nobody has claimed)
prime:       prima
predecessor: none
repo:        work
start:       a823ee284574be3d9f6247925b9088137a27a539
branch:      returns
return file: .workshop/returns/90.50.10.0408.05.01.md
grant:       src/cmd.rs, src/lib.rs, src/page.rs, tests/page_0408.rs (t461u)
axioms:      1.7.8
outcome:     prime can withdraw a packed unclaimed pass; the pass stays in the log and a later claim is refused
overview:    Builder: Grok-2 (Matthew's PC, D:\Git\grok2). Checker: Grok-Check (wf check --as Grok-Check). Wave 4 of the stage plan (section 15.4) and wave 1 of the Grok builder queue: this page is the cmd.rs side, beside 0407 which is the render.rs side. They share no file. Start is returns a823ee284574be3d9f6247925b9088137a27a539. This pack is template 4, so the return must fill the design review line. Lab is 90.50.10.0701. The lab trial tests/lab_0408.rs is not this page's file. This page writes tests/page_0408.rs (section 11.7). Code re-read at a823ee28: claim accepts only tail pack and no existing claim (src/cmd.rs:435-442). is_open_tail is pack, open, return, review (src/page.rs:151). There is no withdraw command in src/lib.rs help. The plan uses the word withdraw and does not spell the command. This pack uses wf withdraw.
jobs:
  w01: Add wf withdraw <page> <NN>, prime only. It runs only when the pass tail is pack and there is no claim. Append a log entry and set the tail to withdrawn. The pass stays in the log. Refuse it when the tail is open, return, review, or closed. A later claim is refused. withdrawn is not an open tail, so the pass no longer holds its files (src/page.rs:151). Wire the command in src/lib.rs help and dispatch, and in src/cmd.rs.
  w02: Add tests/page_0408.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Cover withdraw at pack with no claim, a refusal at open or later, a refused later claim, and the pass still present in the log.
may touch:   src/cmd.rs, src/lib.rs, src/page.rs, tests/page_0408.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0408   (one command each, split by ;)
done when:   Done when: withdraw works at pack with no claim.
Done when: withdraw is refused at open or later.
Done when: a later claim is refused.
Done when: the log keeps the pass.
Done when: cargo test --test page_0408 passes on the box.
Done when: the lab trial tests/lab_0408.rs passes in lab 0701.
stop if:     another file must change, including src/render.rs or templates. The command spelling wf withdraw is wrong. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash 32d37380127d
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash 5eb81e646874
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
