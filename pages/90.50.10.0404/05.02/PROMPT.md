=== WORKSHOP JOB 90.50.10.0404.05.02 ===
Pack hash: fd3b5963141a2347680e13c3faf4a4d50d65070ce04e55b20db10047c45de46d (log entry 17, 2026-11-23T15:47:03Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0404 02 --as <your-name>
Repo: work   Branch: returns   Start: 464170c7561d3d39c6cc71ab12a332a2ffa3d8c0
Read first: pages/90.50.10.0404/05.02/AGENTS.md (sha256 c5a47e498058), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: a return for a pass packed on template 4 must carry a filled design review line, naming the design files the builder compared its work against; wf refuses the return without it, naming t416u. Band door: 90.50.10.0400.
Builder: Cursor-1.
Lab: 90.50.10.0701 (wf loop lab, lab band 0700); trial file tests/lab_0404.rs.
Done when: cargo test --lib and cargo test --test wf pass on Linux.
Done when: on Windows the only failures allowed are the five already named in the 0415 return (sh, seq, and three file names). Page 0416 fixes those.

Jobs:
  w01: In tests/wf.rs rename new_pack_records_template_version_3 (line 1327 at 464170c7) to new_pack_records_template_version_4. Change the assertion at line 1332 from templates "3" to templates "4". Change nothing else in that test.
  w02: In stripped_hashes_with_a_rechained_log_stay_invalid_after_fix (line 2802), a fresh pack is now template 4. Change the assertion at line 2840 from templates 3 to templates 4. Leave the loop that patches versions 3 and 2 as it is. Change nothing else.
May touch: tests/wf.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test wf
Done when (face 01): Done when: cargo test --lib and cargo test --test wf pass on Linux.
Done when: on Windows the only failures allowed are the five already named in the 0415 return (sh, seq, and three file names). Page 0416 fixes those.
Stop if: another file must change, including src/board.rs or templates/v4/return.txt. The wording at src/board.rs:397 is changed. The CRLF in templates/v4/return.txt is changed. A Linux test fails. A Windows failure is not one of the five named in the 0415 return. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0404/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0404.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0404 02 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0404.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
