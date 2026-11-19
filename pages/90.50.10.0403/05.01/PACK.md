WORKSHOP PACK 90.50.10.0403.05.01
Printed by wf from templates/pack.txt. Do not edit.

page:        90.50.10.0403 (wf: init-page refuses invalid work addresses)
prime:       prima
predecessor: none
repo:        work
start:       60dd7e254df032a6fa02510667eb408acf4a41ee
branch:      returns
return file: .workshop/returns/90.50.10.0403.05.01.md
grant:       src/, tests/ (t413u)
axioms:      1.7.8
outcome:     wf init-page refuses a work page at a system address (00-09 or 99 on any axis, page 0000-0099, NN00, NN99, 9999), naming the rule it broke; --system with a ref lets system pages through
overview:    Band 90.50.10.04xx, door 90.50.10.0400 (its face 01 lists this job). Why: wf never used the seqAddr rules, so its first pages sat at book 00, page 0001 (t413u). Rules: t413u (00-09 reserved, DD.SS.00 shelf authority book, 0000-0099 reserved, NN00 band door); seqAddr.md:31, :39, :226, :242, :249 and DESIGN.md:137 (99 and 9999 are pointers or continuations, never normal pages); crates/seqaddr-core/src/addr.rs @ 79f12ed (axis_role, desk_kind, page_kind, band_head). Replaces 0402 (dropped, no 99 rules; RELEASE-CHECK-90.50.10). Job 1 (wf.exe prompt) closed passed on 90.50.00.0001.05.01.
jobs:
  w01: new src/addr.rs with the address rules, copied from seqaddr-core (crates/seqaddr-core/src/addr.rs @ 79f12ed: axis_role, desk_kind, page_kind, band_head), because the wf repo cannot depend on that crate (it is not on this branch). A work address is DD.SS.BB.PPPP (two, two, two and four digits). Refuse, each with its own plain message naming the rule and its source: any desk, shelf or book axis 00-09 ("00-09 are system-reserved on every axis; work starts at 10 (t413u)"); book 00 says "DD.SS.00 is the shelf's authority book; only the system writes there (t413u)"; 99 on any axis ("99 is a pointer to the next location, not work (seqAddr.md:31, :249)"); page 0000-0099 ("pages 0000-0099 are reserved (t413u)"); page 9999 ("9999 is the book continuation, not work (seqAddr.md:226)"); a page ending in 00 ("NN00 is the band head, the band's door; work goes on NN01-NN98 (t413u, seqAddr.md:241)"); a page ending in 99 ("NN99 is the band's continuation, not work (seqAddr.md:242)"). Check 9999 before NN99 so it gets its own message. Any other shape is refused as "not a work address DD.SS.BB.PPPP". Unit tests in src/addr.rs for each rule, and for 90.50.10.0401, 90.50.10.0498 and 10.10.10.0401 passing.
  w02: in src/cmd.rs init_page, call the new check after check_addr. Add --system --system-ref tNNNu: with both, the rules are skipped and the init entry records system_ref; --system without a ref is refused. Only init-page checks; every other command still opens existing pages at any address (90.10.00.0001 and the rest keep working). Add the two flags to the usage text in src/lib.rs.
  w03: in tests/wf.rs, change the test page PG from 1.2.3.4 to 10.10.10.0401 everywhere (and the strings built from it), then add e2e tests named init_page_address_*: refused, each with its message, for 90.50.00.0401, 90.05.10.0401, 99.50.10.0401, 90.99.10.0401, 90.50.99.0401, 90.50.10.0050, 90.50.10.0400, 90.50.10.0499, 90.50.10.9999 and 1.2.3.4; accepted for 90.50.10.0401; accepted for 90.50.00.0001 with --system --system-ref t413u and the ref is in the log; refused with --system and no ref; an existing page at 90.50.00.0001 (made with --system) still verifies and shows status.
may touch:   src/addr.rs, src/cmd.rs, src/lib.rs, tests/wf.rs
must not:    anything outside may touch (the return check refuses it)
checks:      cargo test --lib addr; cargo test --test wf init_page_address   (one command each, split by ;)
done when:   Done when: cargo test --lib addr and cargo test --test wf init_page_address pass on the box, and every old test passes with the test page moved to 10.10.10.0401.
stop if:     another file must change, or a rule above reads two ways. On Windows tests/wf.rs does not compile yet (unix-only imports, known): run cargo build and cargo test --lib addr (or only cargo build if that does not compile), say so on the proof line, and go on; the checker runs the e2e tests on the box
pins (Prime read these before drafting; checked again at release):
  face 04:        entry 2, hash 4269aae974cf
  face 06:        entry 4, hash d4316b5440c1
  last closed 05: none
sources:
  face 01:        v1 entry 3 hash cdfea45843e1
  docs/AXIOMS.md (in the kit folder, the folder with src/ and AGENTS.md; not beside pages/): hash 552014964d27
  docs/DESIGN.md (in the kit folder, same as AXIOMS.md; not beside pages/): hash 46be27fa22a7
