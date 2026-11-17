WORKSHOP PACK 10.20.30.1211.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        10.20.30.1211 (steering hard paths)
prime:       prima
predecessor: none
repo:        driving-game
start:       9218cb60fdcb5fe6f23ced381c9f991a6dfc50a2
branch:      pass/10.20.30.1211.05.01
return file: .workshop/returns/10.20.30.1211.05.01.md
grant:       src/steer.rs, src/input.rs, tests/steer.rs (t300u)
axioms:      
outcome:     the turn rate eases in
overview:    
jobs:
  w01: make the turn rate ease in
may touch:   src/steer.rs, tests/steer.rs
must not:    anything outside may touch (the return check refuses it)
checks:      grep -q "clamp(-30, 30)" src/steer.rs   (one command each, split by ;)
stop if:     the turn needs a physics change
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 3, hash 62d17969b6d6
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash dabe1860431f
  docs/AXIOMS.md: hash 552014964d27
  docs/DESIGN.md: hash 010dd8b72a43
