WORKSHOP PACK 90.50.10.0419.05.02
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0419 (pack checks are safe on Windows)
prime:       prima
predecessor: 05.01
repo:        work
start:       4dc2e0f076326657a7f4ac232bf8edd6733464c2
branch:      pass/90.50.10.0419.05.02
return file: .workshop/returns/90.50.10.0419.05.02.md
grant:       src/git.rs, tests/page_0419.rs, tests/lab_0419.rs (t461u, t461u)
axioms:      1.7.8,9
outcome:     the lab trial tests/lab_0419.rs proves the Windows-safe git grep form from outside this page's own tests
overview:    Builder: Grok-3 (Matthew's PC, D:\Git\grok3). Checker: Grok-Check (wf check --as Grok-Check). Pass 05.02. 05.01 closed failed (Grok-Check entry 9, signoff 10, close 11; close log 7f3cdadf; packs 0c94febb). The safe git grep form, the bare-form note, and tests/page_0419.rs met their Done when lines. Jobs w01 and w02 were accepted. The major was that tests/lab_0419.rs was not in the return; the 05.01 grant did not include it. This pass grants that file and names Grok-3, who claimed and returned 05.01. The published 05.01 pack still says Grok-5; do not republish it to change the name. Start is returns 4dc2e0f076326657a7f4ac232bf8edd6733464c2, which already contains the 05.01 return 710485918b0f7ef90638d8ab57c363ba1f2d0a71. Template 4, so the return must fill the design review line. Lab is 90.50.10.0701. This pass writes only tests/lab_0419.rs. Do not change src/git.rs or tests/page_0419.rs. Do not copy the harness. 0701.05.02 may-touch is tests/lab_0404.rs; 0701.05.03 may-touch is tests/lab_0415.rs; this pass does not touch those files. 0407, 0408, 0418 and 0705.05.02 hold no tests/lab_0419.rs.
jobs:
  w01: Add tests/lab_0419.rs. It starts with mod common; and holds only 0419's cases. From outside, not from tests/page_0419.rs: the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c (exit 0), the pattern token has no caret, no quotes, no spaces, and does not start with #, and the bare form git grep -q -E ##[[:space:]]0[.] -- <file> exits 128 under sh -c with no pattern given. src/git.rs still documents both forms in the run comment (the [#][#] form, the bare ## form, exit 128, and no pattern given). The test fails on commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on 710485918b0f7ef90638d8ab57c363ba1f2d0a71 and on this return. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test. Do not copy tests/common. cargo test --lib and cargo test --test page_0419 still pass.
may touch:   tests/lab_0419.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0419; cargo test --test lab_0419   (one command each, split by ;)
done when:   Done when: cargo test --test lab_0419 passes on the box.
Done when: the lab trial fails on start commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on this return (and on the 05.01 return 710485918b0f7ef90638d8ab57c363ba1f2d0a71).
Done when: what 05.01 already met stays true: the safe form git grep -q -E [#][#][[:space:]]0[.] -- <file> is documented and tested, and the bare ## form is documented as a sh -c comment (exit 128, no pattern given).
stop if:     another file must change, including src/git.rs, tests/page_0419.rs, src/cmd.rs (held by 0408), or tests/common/mod.rs. The 05.01 safe form or bare-form note is weakened. A check command has a caret, quotes, or a space inside a git grep pattern. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 15, hash ed6a99cc6ebf
  last closed 05: 05.01 closed at entry 11
sources:
  face 01:        v2 entry 13 hash 8c21ee105930
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
