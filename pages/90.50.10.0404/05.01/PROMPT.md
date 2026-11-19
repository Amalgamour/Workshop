=== WORKSHOP JOB 90.50.10.0404.05.01 ===
Pack hash: aa8de5e137a42f221472177de482bbb8c794ec620cffa5541a88bf43b659220c (log entry 6, 2026-11-19T20:27:28Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0404 01 --as <your-name>
Repo: work   Branch: returns   Start: 3646e3448985d1cf40da82b262cfd8852ae59234
Read first: pages/90.50.10.0404/05.01/AGENTS.md (sha256 8de8fc900e65), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: a return for a pass packed on template 4 must carry a filled design review line, naming the design files the builder compared its work against; wf refuses the return without it, naming t416u. Band door: 90.50.10.0400.
Lab: 90.50.10.0701 (wf loop lab, lab band 0700); trial file tests/lab_0404.rs.
Done when: cargo test --lib passes on the box; the lab's trial tests/lab_0404.rs passes on the box (a v4 return with no line is refused naming t416u and recorded; one with the line is accepted); cargo test --test wf still passes; a pass packed on template 1, 2 or 3 (such as 0403.05.01) prints and checks exactly as before.

Jobs:
  w01: new templates/v4/return.txt: the text of templates/return.txt with one line added after the proof line and before the not done line: "design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>". In src/render.rs add T_RETURN_V4 from that file, set TEMPLATE_VER to "4", and make packed_templates return (T_AGENTS_V3, T_PROMPT_V3, T_RETURN_V4) for "4". Leave "1", "2" and "3" exactly as they are. Update the render.rs unit tests that name the version.
  w02: in src/cmd.rs, when the pass's pack entry has templates "4", parse_return also requires a filled "design review" line (present, not empty, not starting with "<"). The refusal says: "the return has no 'design review:' line filled in. t416u: novel work is reviewed against the design documents before the return is complete". It is recorded as return-refused like the other refusals. Packs on templates 1, 2 or 3 do not need the line. Unit tests in src/cmd.rs's own test module: a v4 pass without the line is refused with that message; with it, passes; a v3 pass without it passes.
May touch: templates/v4/return.txt, src/render.rs, src/cmd.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test wf
Done when (face 01): Done when: cargo test --lib passes on the box; the lab's trial tests/lab_0404.rs passes on the box (a v4 return with no line is refused naming t416u and recorded; one with the line is accepted); cargo test --test wf still passes; a pass packed on template 1, 2 or 3 (such as 0403.05.01) prints and checks exactly as before.
Stop if: another file must change; a test file seems needed (the lab writes it; say what it should try in overflow); a pass packed before this change would print or check differently; a rule above reads two ways (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0404/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0404.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0404 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0404.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
