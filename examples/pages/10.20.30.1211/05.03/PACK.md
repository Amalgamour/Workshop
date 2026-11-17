WORKSHOP PACK 10.20.30.1211.05.03
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1211 (steering hard paths)
prime:       prima
predecessor: 05.02
repo:        driving-game
start:       268f31dc6296f464e84357a5b27501f7990b22fa
branch:      pass/10.20.30.1211.05.03
return file: .workshop/returns/10.20.30.1211.05.03.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs (t300u)
axioms:      
outcome:     no skid on fast turns
overview:    
jobs:
  w01: turns stay smooth at speed
may touch:   src/steer.rs, tests/steer.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q "clamp(-30, 30)" src/steer.rs   (one command each, split by ;)
stop if:     the turn needs a physics change
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 22, hash 98ceb9ceb1fe
  last closed 05: 05.2 closed at entry 21
sources:
  face 01:        v1 entry 2 hash dabe1860431f
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
