=== WORKSHOP JOB 90.50.10.0403.05.01 ===
Pack hash: b2de54ce03fd3280e81acadfbef4c1f366105918625956a832c5923663ce45a9 (log entry 6, 2026-11-19T18:22:49Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0403 01 --as <your-name>
Repo: work   Branch: returns   Start: 60dd7e254df032a6fa02510667eb408acf4a41ee
Read first: pages/90.50.10.0403/05.01/AGENTS.md (sha256 7f2ffaaeefb1), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: wf init-page refuses invalid work addresses with the rule it broke, and lets system pages through only with --system and a ref. Band door: 90.50.10.0400.
Done when: cargo test --lib addr and cargo test --test wf init_page_address pass on the box, and every old test passes with the test page moved to 10.10.10.0401.
Jobs:
  w01: new src/addr.rs with the address rules, copied from seqaddr-core (crates/seqaddr-core/src/addr.rs @ 79f12ed: axis_role, desk_kind, page_kind, band_head), because the wf repo cannot depend on that crate (it is not on this branch). A work address is DD.SS.BB.PPPP (two, two, two and four digits). Refuse, each with its own plain message naming the rule and its source: any desk, shelf or book axis 00-09 ("00-09 are system-reserved on every axis; work starts at 10 (t413u)"); book 00 says "DD.SS.00 is the shelf's authority book; only the system writes there (t413u)"; 99 on any axis ("99 is a pointer to the next location, not work (seqAddr.md:31, :249)"); page 0000-0099 ("pages 0000-0099 are reserved (t413u)"); page 9999 ("9999 is the book continuation, not work (seqAddr.md:226)"); a page ending in 00 ("NN00 is the band head, the band's door; work goes on NN01-NN98 (t413u, seqAddr.md:241)"); a page ending in 99 ("NN99 is the band's continuation, not work (seqAddr.md:242)"). Check 9999 before NN99 so it gets its own message. Any other shape is refused as "not a work address DD.SS.BB.PPPP". Unit tests in src/addr.rs for each rule, and for 90.50.10.0401, 90.50.10.0498 and 10.10.10.0401 passing.
  w02: in src/cmd.rs init_page, call the new check after check_addr. Add --system --system-ref tNNNu: with both, the rules are skipped and the init entry records system_ref; --system without a ref is refused. Only init-page checks; every other command still opens existing pages at any address (90.10.00.0001 and the rest keep working). Add the two flags to the usage text in src/lib.rs.
  w03: in tests/wf.rs, change the test page PG from 1.2.3.4 to 10.10.10.0401 everywhere (and the strings built from it), then add e2e tests named init_page_address_*: refused, each with its message, for 90.50.00.0401, 90.05.10.0401, 99.50.10.0401, 90.99.10.0401, 90.50.99.0401, 90.50.10.0050, 90.50.10.0400, 90.50.10.0499, 90.50.10.9999 and 1.2.3.4; accepted for 90.50.10.0401; accepted for 90.50.00.0001 with --system --system-ref t413u and the ref is in the log; refused with --system and no ref; an existing page at 90.50.00.0001 (made with --system) still verifies and shows status.
May touch: src/addr.rs, src/cmd.rs, src/lib.rs, tests/wf.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib addr; cargo test --test wf init_page_address
Done when (face 01): Done when: cargo test --lib addr and cargo test --test wf init_page_address pass on the box, and every old test passes with the test page moved to 10.10.10.0401.
Stop if: another file must change, or a rule above reads two ways. On Windows tests/wf.rs does not compile yet (unix-only imports, known): run cargo build and cargo test --lib addr (or only cargo build if that does not compile), say so on the proof line, and go on; the checker runs the e2e tests on the box (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0403/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0403.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0403 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0403.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
