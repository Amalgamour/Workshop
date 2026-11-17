WORKSHOP PACK 10.20.30.1201.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1201 (steering)
prime:       prima
predecessor: 05.01
repo:        driving-game
start:       089ad979a4f89727471abefdc7d4d692fb2ce5a0
branch:      pass/10.20.30.1201.05.02
return file: .workshop/returns/10.20.30.1201.05.02.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs (t300u)
axioms:      2,8,9
outcome:     steering feels less stiff; taps under 50 ms do nothing
overview:    you said "feels too stiff" (04)
jobs:
  w01: rate 2 to 3 (decision D-a)
  w02: ignore taps under 50 ms (dead zone)
may touch:   src/steer.rs, tests/steer.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q "rate = 3" src/steer.rs   (one command each, split by ;)
stop if:     the tap length lives outside may touch
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 21, hash 80585fb4b9f5
  face 06:        entry 22, hash f2078044888a
  last closed 05: 05.1 closed at entry 15
sources:
  face 01:        v2 entry 18 hash 3f7d2c60c999
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
