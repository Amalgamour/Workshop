WORKSHOP PACK 10.20.30.1211.05.04
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1211 (steering hard paths)
prime:       prima
predecessor: 05.03
repo:        driving-game
start:       9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
branch:      pass/10.20.30.1211.05.04
return file: .workshop/returns/10.20.30.1211.05.04.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs, src/physics/grip.rs (t300u, t301u)
axioms:      
outcome:     no skid on fast turns
overview:    
jobs:
  w01: turns stay smooth at speed
may touch:   src/steer.rs, src/physics/grip.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q "clamp(-30, 30)" src/steer.rs   (one command each, split by ;)
stop if:     the turn needs a physics change
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 36, hash b0077a174f71
  last closed 05: 05.3 closed at entry 33
sources:
  face 01:        v1 entry 2 hash dabe1860431f
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
