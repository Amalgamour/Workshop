WORKSHOP PACK 90.50.10.0404.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0404 (wf: returns state a design review (t416u))
prime:       prima
predecessor: 05.01
repo:        work
start:       464170c7561d3d39c6cc71ab12a332a2ffa3d8c0
branch:      returns
return file: .workshop/returns/90.50.10.0404.05.02.md
grant:       src/, templates/, tests/wf.rs (t461u, 0404 check entry 10)
axioms:      1.7.8
outcome:     the two e2e tests expect template 4, and cargo test --lib and cargo test --test wf pass on Linux
overview:    Builder: Cursor-1. Pass 05.01 closed failed. The check found tests/wf.rs still expects template 3, and that file was outside the grant. This pass adds tests/wf.rs and changes only those two tests. Leave src/board.rs:397 and the CRLF in templates/v4/return.txt alone. Start is returns head 464170c7561d3d39c6cc71ab12a332a2ffa3d8c0. Template 4. On Windows, the only failures allowed are the five named in the 0415 return (sh, seq, and three file names); page 0416 fixes those.
jobs:
  w01: In tests/wf.rs rename new_pack_records_template_version_3 (line 1327 at 464170c7) to new_pack_records_template_version_4. Change the assertion at line 1332 from templates "3" to templates "4". Change nothing else in that test.
  w02: In stripped_hashes_with_a_rechained_log_stay_invalid_after_fix (line 2802), a fresh pack is now template 4. Change the assertion at line 2840 from templates 3 to templates 4. Leave the loop that patches versions 3 and 2 as it is. Change nothing else.
may touch:   tests/wf.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test wf   (one command each, split by ;)
done when:   Done when: cargo test --lib and cargo test --test wf pass on Linux.
Done when: on Windows the only failures allowed are the five already named in the 0415 return (sh, seq, and three file names). Page 0416 fixes those.
stop if:     another file must change, including src/board.rs or templates/v4/return.txt. The wording at src/board.rs:397 is changed. The CRLF in templates/v4/return.txt is changed. A Linux test fails. A Windows failure is not one of the five named in the 0415 return. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 13, hash be133221dfb8
  last closed 05: 05.01 closed at entry 12
sources:
  face 01:        v2 entry 15 hash d318feb22cb4
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
