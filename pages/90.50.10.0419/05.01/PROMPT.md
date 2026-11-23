=== WORKSHOP JOB 90.50.10.0419.05.01 ===
Pack hash: 3ed7f6c93aad3e7d847f9029b1c77e36c94ca4e2fd9e8e7351665fad0f619e9c (log entry 6, 2026-11-23T16:31:12Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0419 01 --as <your-name>
Repo: work   Branch: returns   Start: a823ee284574be3d9f6247925b9088137a27a539
Read first: pages/90.50.10.0419/05.01/AGENTS.md (sha256 e404380168ef), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: pack check commands are safe on Windows and still work on Linux. A git grep pattern in a check has no caret, no quotes, and no spaces. Band door: 90.50.10.0400.
Builder: Grok-5 (Matthew's PC, D:\Git\grok5).
Lab: 90.50.10.0701 (wf loop lab). The lab trial is tests/lab_0419.rs, written by another view after this return. This page's own test file is tests/page_0419.rs.
Done when: a check that uses git grep -q -E [#][#][[:space:]]0[.] -- <file> passes under wf on Linux (sh -c) and is safe on Windows (cmd /C): no caret, no quotes, no spaces in the pattern, and no sh comment.
Done when: the bare form git grep -q -E ##[[:space:]]0[.] -- <file> is documented as a sh -c comment (it exits 128, "no pattern given") so packs do not use it.
Done when: cargo test --test page_0419 passes on the box.
Done when: the lab trial tests/lab_0419.rs passes in lab 0701.

Jobs:
  w01: In src/git.rs, make check commands safe on Windows and still correct on Linux. A git grep pattern in a check must have no caret, no quotes, and no spaces. Do not leave Linux broken: a bare ## pattern must not be the form packs rely on, because it is a comment under sh -c. If the right fix also needs a pack-time lint, stop and say so (src/cmd.rs is held by 0408).
  w02: Add tests/page_0419.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Prove that the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c, and that the bare ## form fails under sh -c with no pattern given. If a test needs Windows cmd /C and this box is Linux, still run the sh -c cases here and state what must be proven on Windows.
May touch: src/git.rs, tests/page_0419.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0419
Done when (face 01): Done when: a check that uses git grep -q -E [#][#][[:space:]]0[.] -- <file> passes under wf on Linux (sh -c) and is safe on Windows (cmd /C): no caret, no quotes, no spaces in the pattern, and no sh comment.
Done when: the bare form git grep -q -E ##[[:space:]]0[.] -- <file> is documented as a sh -c comment (it exits 128, "no pattern given") so packs do not use it.
Done when: cargo test --test page_0419 passes on the box.
Done when: the lab trial tests/lab_0419.rs passes in lab 0701.
Stop if: another file must change, including src/cmd.rs (held by 0408) or templates. The only way to pass is to skip checks on Windows, or to break Linux checks. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0419/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0419.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0419 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0419.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
