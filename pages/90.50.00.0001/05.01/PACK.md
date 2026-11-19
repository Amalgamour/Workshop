WORKSHOP PACK 90.50.00.0001.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.00.0001 (wf: builder prompt says wf.exe)
prime:       prima
predecessor: none
repo:        work
start:       3daaa4861346ebf7829a5f3eace6a99387be4d1c
branch:      returns
return file: .workshop/returns/90.50.00.0001.05.01.md
grant:       src/, tests/, templates/ (t407u)
axioms:      
outcome:     every wf command in BUILDER-PROMPT.md reads wf.exe
overview:    
jobs:
  w01: in templates/v3/builder.txt, write wf.exe wherever the builder is told to run wf (the claim line, the return line, and the two "wf return ... --push" mentions). Leave "cargo install ... wf" as is: there wf names the crate.
  w02: in tests/wf.rs, update t401u_pack_on_the_shared_branch_prints_one_builder_prompt to expect "wf.exe claim 1.2.3.4 01" and "wf.exe return 1.2.3.4 01"
may touch:   templates/v3/builder.txt, tests/wf.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --test wf builder_prompt   (one command each, split by ;)
done when:   Done when: every wf command line in a printed BUILDER-PROMPT.md starts with wf.exe, and cargo test --test wf builder_prompt passes on the box.
stop if:     another file must change. On Windows tests/wf.rs does not compile yet (unix-only imports, known): run cargo build instead, say so on the proof line, and go on; the checker runs the test on the box
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 2, hash d1c8ebcb73a3
  face 06:        entry 4, hash a3bb33a794a9
  last closed 05: none
sources:
  face 01:        v1 entry 3 hash ca5a7d494f5b
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
