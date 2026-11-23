WORKSHOP PACK 90.50.10.0407.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0407 (the door prints its own type and contents)
prime:       prima
predecessor: none
repo:        work
start:       a823ee284574be3d9f6247925b9088137a27a539
branch:      returns
return file: .workshop/returns/90.50.10.0407.05.01.md
grant:       src/render.rs, tests/page_0407.rs (t461u)
axioms:      1.7.8
outcome:     face 00 of a band door shows type: band and a contents list built from the pages folder; a non-door page has no list
overview:    Builder: Grok-1 (Matthew's PC, D:\Git\grok1). Checker: Grok-Check (wf check --as Grok-Check). Wave 4 of the stage plan (section 15.4) and wave 1 of the Grok builder queue: this page is the render.rs side, beside 0408 which is the cmd.rs side. They share no file. Start is returns a823ee284574be3d9f6247925b9088137a27a539. 0403 is closed. This pack is template 4, so the return must fill the design review line. Lab is 90.50.10.0701. The lab trial tests/lab_0407.rs is not this page's file. This page writes tests/page_0407.rs (section 11.7). Code re-read at a823ee28: face 00 is printed by face00 in src/render.rs:355. It lists title, person, prime, grant and the log head. It does not print type: band or a contents list. page_kind is src/addr.rs:73. BandHead is PP00 at or above 0100. Do not change src/addr.rs. The plan's done-when says a dropped page shows as dropped. wf has no dropped state in the log (retire is page 0409, later). Do not invent one.
jobs:
  w01: In src/render.rs face00 (line 355 at a823ee28), when this page is a band head (page_kind BandHead, src/addr.rs:73), print a line type: band and a contents list. Build the list by reading the other page folders of the same band under the run folder's pages directory. Do not hand-write the list. Each line names the page address and the state that page's log already has. A page that is not a band head gets no type: band line and no contents list.
  w02: Add tests/page_0407.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Show a band door listing each page in its band with its state, and a non-door page with no list. Do not add a dropped state. If a test cannot show dropped from the log as it is, stop and say so.
may touch:   src/render.rs, tests/page_0407.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0407   (one command each, split by ;)
done when:   Done when: a band door lists each page in its band with its state.
Done when: a dropped page shows as dropped.
Done when: a non-door page shows no list.
Done when: cargo test --test page_0407 passes on the box.
Done when: the lab trial tests/lab_0407.rs passes in lab 0701.
stop if:     another file must change, including src/addr.rs, src/cmd.rs, src/lib.rs, src/page.rs, or a hand edit of pages under the door. The only way to show dropped is to invent a state the log does not have. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash ae25cf3d2705
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash 556630a7d2d0
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
