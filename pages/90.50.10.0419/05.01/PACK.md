WORKSHOP PACK 90.50.10.0419.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0419 (pack checks are safe on Windows)
prime:       prima
predecessor: none
repo:        work
start:       a823ee284574be3d9f6247925b9088137a27a539
branch:      returns
return file: .workshop/returns/90.50.10.0419.05.01.md
grant:       src/git.rs, tests/page_0419.rs (t461u)
axioms:      1.7.8
outcome:     wf check commands that use git grep are safe on Windows and still run on Linux
overview:    Builder: Grok-5 (Matthew's PC, D:\Git\grok5). Checker: Grok-Check (wf check --as Grok-Check). Wave 1 of the Grok builder queue. Start is returns a823ee284574be3d9f6247925b9088137a27a539. This pack is template 4, so the return must fill the design review line. Lab is 90.50.10.0701. The lab trial tests/lab_0419.rs is not this page's file. This page writes tests/page_0419.rs. Source: docs/design/drafts/WF-WINDOWS-QUOTING.md on prima/build. Code re-read at a823ee28: wf runs each check as one string (src/cmd.rs:752; src/git.rs:110-112). On Linux that is sh -c; on Windows it is cmd /C. cmd's escape is caret, and a quoted pattern that contains caret is not kept as written. The quoting doc's example, git grep -q -E ##[[:space:]]0[.] -- file, has no caret, no quotes and no spaces, but under sh -c a token that starts with # is a comment, so git prints "fatal: no pattern given" and exits 128. The form that works on Linux and stays safe on Windows is git grep -q -E [#][#][[:space:]]0[.] -- file. 0417 will need src/git.rs later, so this page must finish first.
jobs:
  w01: In src/git.rs, make check commands safe on Windows and still correct on Linux. A git grep pattern in a check must have no caret, no quotes, and no spaces. Do not leave Linux broken: a bare ## pattern must not be the form packs rely on, because it is a comment under sh -c. If the right fix also needs a pack-time lint, stop and say so (src/cmd.rs is held by 0408).
  w02: Add tests/page_0419.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Prove that the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c, and that the bare ## form fails under sh -c with no pattern given. If a test needs Windows cmd /C and this box is Linux, still run the sh -c cases here and state what must be proven on Windows.
may touch:   src/git.rs, tests/page_0419.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib; cargo test --test page_0419   (one command each, split by ;)
done when:   Done when: a check that uses git grep -q -E [#][#][[:space:]]0[.] -- <file> passes under wf on Linux (sh -c) and is safe on Windows (cmd /C): no caret, no quotes, no spaces in the pattern, and no sh comment.
Done when: the bare form git grep -q -E ##[[:space:]]0[.] -- <file> is documented as a sh -c comment (it exits 128, "no pattern given") so packs do not use it.
Done when: cargo test --test page_0419 passes on the box.
Done when: the lab trial tests/lab_0419.rs passes in lab 0701.
stop if:     another file must change, including src/cmd.rs (held by 0408) or templates. The only way to pass is to skip checks on Windows, or to break Linux checks. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash c2ee7aa624e4
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash f85611ed9b47
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
