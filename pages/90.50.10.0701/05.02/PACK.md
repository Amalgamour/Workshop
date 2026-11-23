WORKSHOP PACK 90.50.10.0701.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0701 (wf loop lab: one harness, every wf trial)
prime:       prima
predecessor: 05.01
repo:        work
start:       a823ee284574be3d9f6247925b9088137a27a539
branch:      returns
return file: .workshop/returns/90.50.10.0701.05.02.md
grant:       tests/ (t432u)
axioms:      1.7.8
outcome:     an outside trial tests/lab_0404.rs passes the 0404 done-when without using the builder's own tests
overview:    Builder: Grok-1. Wave 3 trial for 90.50.10.0404, lab pass 05.02. One file only, so the 0415 trial can be open beside it (stage plan 12.3). Start of this lab pass is a823ee28, which already contains the 0404 return. The work page's own start was earlier; this trial is the outside view. Template 4. The return of this pass fills the design review line. Do not copy the harness. Do not change src/.
jobs:
  w01: Add tests/lab_0404.rs. It starts with mod common; and holds only 0404's cases. From outside, not from the builder's tests: a return on template 4 with no design review line is refused, the refusal names t416u, and it is recorded; a template 4 return with the line filled is accepted; a return for a pack on template 1, 2, or 3 is accepted without that line. cargo test --lib and cargo test --test wf still pass. Do not copy tests/common.
may touch:   tests/lab_0404.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --test lab_0404   (one command each, split by ;)
done when:   Done when: cargo test --lib passes on the box; the lab's trial tests/lab_0404.rs passes on the box (a v4 return with no line is refused naming t416u and recorded; one with the line is accepted); cargo test --test wf still passes; a pass packed on template 1, 2 or 3 (such as 0403.05.01) prints and checks exactly as before.
stop if:     another file must change, including src/ or tests/common/mod.rs or tests/wf.rs. The trial copies the harness. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 15, hash 3b1c1ca11cc0
  last closed 05: 05.01 closed at entry 12
sources:
  face 01:        v3 entry 16 hash 7fdd999bf5fb
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
