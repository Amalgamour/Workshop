=== WORKSHOP JOB 90.50.10.0407.05.01 ===
Pack hash: 7ac8e94417e60349fb1c5d2cda794ab6aa5f4db8d07ea71a26dd52109787f387 (log entry 6, 2026-11-23T16:30:14Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0407 01 --as <your-name>
Repo: work   Branch: returns   Start: a823ee284574be3d9f6247925b9088137a27a539
Read first: pages/90.50.10.0407/05.01/AGENTS.md (sha256 78526c7f73b8), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: a page ending in 00 shows type: band on face 00, and a contents list of the band's pages, built by wf from the pages folder, not written by hand. Band door: 90.50.10.0400.
Builder: Grok-1 (Matthew's PC, D:\Git\grok1).
Lab: 90.50.10.0701 (wf loop lab). The lab trial is tests/lab_0407.rs, written by another view after this return. This page's own test file is tests/page_0407.rs.
Done when: a band door lists each page in its band with its state.
Done when: a dropped page shows as dropped.
Done when: a non-door page shows no list.
Done when: cargo test --test page_0407 passes on the box.
Done when: the lab trial tests/lab_0407.rs passes in lab 0701.

Jobs:
  w01: In src/render.rs face00 (line 355 at a823ee28), when this page is a band head (page_kind BandHead, src/addr.rs:73), print a line type: band and a contents list. Build the list by reading the other page folders of the same band under the run folder's pages directory. Do not hand-write the list. Each line names the page address and the state that page's log already has. A page that is not a band head gets no type: band line and no contents list.
  w02: Add tests/page_0407.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Show a band door listing each page in its band with its state, and a non-door page with no list. Do not add a dropped state. If a test cannot show dropped from the log as it is, stop and say so.
May touch: src/render.rs, tests/page_0407.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0407
Done when (face 01): Done when: a band door lists each page in its band with its state.
Done when: a dropped page shows as dropped.
Done when: a non-door page shows no list.
Done when: cargo test --test page_0407 passes on the box.
Done when: the lab trial tests/lab_0407.rs passes in lab 0701.
Stop if: another file must change, including src/addr.rs, src/cmd.rs, src/lib.rs, src/page.rs, or a hand edit of pages under the door. The only way to show dropped is to invent a state the log does not have. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0407/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0407.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0407 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0407.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
