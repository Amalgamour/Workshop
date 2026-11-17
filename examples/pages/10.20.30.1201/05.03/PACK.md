WORKSHOP PACK 10.20.30.1201.05.03
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1201 (steering)
prime:       prima
predecessor: 05.02
repo:        driving-game
start:       268f31dc6296f464e84357a5b27501f7990b22fa
branch:      pass/10.20.30.1201.05.03
return file: .workshop/returns/10.20.30.1201.05.03.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs (t300u)
axioms:      2,8,9
outcome:     taps under 50 ms do nothing; holds feel smooth
overview:    05.02 w02 blocked; frame widened (D-b)
jobs:
  w01: smooth the key input in src/input.rs
  w02: ignore taps under 50 ms
may touch:   src/steer.rs, src/input.rs, tests/steer.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q smooth src/input.rs; grep -q "rate = 3" src/steer.rs   (one command each, split by ;)
stop if:     the turn needs a physics change
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 32, hash 046c5a5a81cf
  face 06:        entry 34, hash 1fb6ca49cf72
  last closed 05: 05.2 closed at entry 30
sources:
  face 01:        v3 entry 33 hash 5a1d60190942
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
