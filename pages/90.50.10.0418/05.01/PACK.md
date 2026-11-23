WORKSHOP PACK 90.50.10.0418.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0418 (seated-05 in the compute core)
prime:       prima
predecessor: none
repo:        work
start:       c1750c32c3fb837deb34a5b9c3cafc77c1086dfc
branch:      prima/build
return file: .workshop/returns/90.50.10.0418.05.01.md
grant:       crates/seqaddr-core/src/state.rs, crates/seqaddr-core/src/resolve.rs, crates/seqaddr-core/src/validate.rs, crates/seqaddr-core/src/face.rs, crates/seqaddr-core/tests/page_0418.rs (t523)
axioms:      1.7.8
outcome:     the compute core accepts a seat at plain 05; 05.NN stays a pass; face 06 stays unseated
overview:    Builder: Grok-4 (Matthew's PC, D:\Git\grok4). Checker: Grok-Check (wf check --as Grok-Check). Wave 1 of the Grok builder queue. t523 core run: the work clone is prima/build, and this pack uses --branch prima/build. Start is prima/build c1750c32c3fb837deb34a5b9c3cafc77c1086dfc (holds the t512 seated-05 rule, t523 words, and docs/plan/CORE-RUN.md). Setup is in that file. Grant-ref is t523. Template 4, so the return must fill the design review line. Lab is 90.50.10.0701. The lab trial tests/lab_0418.rs is not this page's file. This page writes crates/seqaddr-core/tests/page_0418.rs. Cite docs/design/drafts/SEATED-05-PROPOSAL.md and seqAddr.md:199-204. Lines at the start commit: state.rs:459-460 (counted-face refusal), resolve.rs:182-183 (plain FF on a counted face reads a derived board), validate.rs:345 (is_counted skip), face.rs:82-84 (always_counted is 05 and 06). Do not change wf src/. The check command has no caret, no quotes, and no git grep pattern.
jobs:
  w01: In crates/seqaddr-core, apply the seated-05 rule. A body on face 05 with no counter is the seat (plain 05). 05.NN stays a pass. The board of the passes stays 05.00. Face 06 stays counted and is never seated. Change only state.rs, resolve.rs, validate.rs and face.rs, at the cited sites and any other line in those four files the new rule requires.
  w02: Add crates/seqaddr-core/tests/page_0418.rs. Show: a seat at plain 05 is accepted; a pass 05.NN is still a pass; plain 06 is still not a seat; face 06 still has no door of its own. Tests must build on Windows: no std::os::unix. If an existing test file must change, stop and say so; do not edit it.
may touch:   crates/seqaddr-core/src/state.rs, crates/seqaddr-core/src/resolve.rs, crates/seqaddr-core/src/validate.rs, crates/seqaddr-core/src/face.rs, crates/seqaddr-core/tests/page_0418.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --manifest-path crates/seqaddr-core/Cargo.toml   (one command each, split by ;)
done when:   Done when: a body on face 05 with no counter is accepted as the seat (plain 05), and 05.NN stays a pass. The board of the passes stays 05.00.
Done when: face 06 is still never seated. Plain 06 still means 06.00.
Done when: the counted-face refusal at state.rs:459-460 no longer rejects a seat on face 05; resolve.rs:182-183 no longer treats plain 05 as only a derived board; face.rs:82-84 still counts 05 and 06, and 05 also has a seat; validate.rs:345 still fits the new rule.
Done when: the change matches docs/design/drafts/SEATED-05-PROPOSAL.md and seqAddr.md:199-204 on prima/build. Code is not applied by hand outside the grant.
Done when: cargo test --manifest-path crates/seqaddr-core/Cargo.toml passes on the box.
stop if:     another file must change, including any wf src/ file, another crate, or an existing test file outside may touch. Face 06 becomes seated. A 05.NN pass is rewritten or removed. A rule above reads two ways.
pins (Prime read these before drafting; checked again at release):
  face 04:        none
  face 06:        entry 4, hash 61fb1fe2635f
  last closed 05: none
sources:
  face 01:        v1 entry 2 hash d8ae3b99aa8a
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
