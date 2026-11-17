WORKSHOP PACK 10.20.30.1201.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1201 (steering)
prime:       prima
predecessor: none
repo:        driving-game
start:       3dcfc7160ad5849b5179f2f0111df90ef85340e2
branch:      pass/10.20.30.1201.05.01
return file: .workshop/returns/10.20.30.1201.05.01.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs (t300u)
axioms:      2,8,9
outcome:     arrow keys turn the car; max 30 degrees
overview:    first feel of the game; see 04
jobs:
  w01: steer left and right at rate 2
  w02: clamp the angle at 30 degrees
may touch:   src/steer.rs, tests/steer.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q "rate = 2" src/steer.rs; grep -q clamp src/steer.rs   (one command each, split by ;)
stop if:     the turn needs a physics change
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 4, hash 84b8d0a49c61
  face 06:        entry 8, hash 317ed8efc366
  last closed 05: none
sources:
  face 01:        v1 entry 5 hash 3785de471b80
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
