=== WORKSHOP JOB 90.50.10.0419.05.02 ===
Pack hash: b1882a4544faf8fa7865d570c351f2633df21cd4e049528bf9eb073a8c1e43f6 (log entry 17, 2026-11-23T18:19:31Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0419 02 --as <your-name>
Repo: work   Branch: pass/90.50.10.0419.05.02   Start: 4dc2e0f076326657a7f4ac232bf8edd6733464c2
Read first: pages/90.50.10.0419/05.02/AGENTS.md (sha256 96f611bac36e), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: the lab trial tests/lab_0419.rs proves the Windows-safe git grep form, from outside this page's own tests. The 05.01 work in src/git.rs and tests/page_0419.rs stays. Band door: 90.50.10.0400.
Builder: Grok-3 (Matthew's PC, D:\Git\grok3).
Lab: 90.50.10.0701 (wf loop lab). This pass writes the lab trial tests/lab_0419.rs. tests/page_0419.rs was written in 05.01 and is not this pass's file.
Why: 05.01 closed failed. Grok-Check entry 9 failed because tests/lab_0419.rs was not in the return. Face 01 had said another view would write it after that return, and the 05.01 grant did not include it. The safe git grep form, the bare-form note, and tests/page_0419.rs met their Done when lines. Jobs w01 and w02 were accepted. This pass grants the trial file and names Grok-3, who claimed and returned 05.01.
Done when: cargo test --test lab_0419 passes on the box.
Done when: the lab trial fails on start commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on this return (and on the 05.01 return 710485918b0f7ef90638d8ab57c363ba1f2d0a71).
Done when: what 05.01 already met stays true: the safe form git grep -q -E [#][#][[:space:]]0[.] -- <file> is documented and tested, and the bare ## form is documented as a sh -c comment (exit 128, no pattern given).

Jobs:
  w01: Add tests/lab_0419.rs. It starts with mod common; and holds only 0419's cases. From outside, not from tests/page_0419.rs: the form git grep -q -E [#][#][[:space:]]0[.] -- <file> matches a heading under sh -c (exit 0), the pattern token has no caret, no quotes, no spaces, and does not start with #, and the bare form git grep -q -E ##[[:space:]]0[.] -- <file> exits 128 under sh -c with no pattern given. src/git.rs still documents both forms in the run comment (the [#][#] form, the bare ## form, exit 128, and no pattern given). The test fails on commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on 710485918b0f7ef90638d8ab57c363ba1f2d0a71 and on this return. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test. Do not copy tests/common. cargo test --lib and cargo test --test page_0419 still pass.
May touch: tests/lab_0419.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0419; cargo test --test lab_0419
Done when (face 01): Done when: cargo test --test lab_0419 passes on the box.
Done when: the lab trial fails on start commit a823ee284574be3d9f6247925b9088137a27a539, which has no tests/page_0419.rs, and passes on this return (and on the 05.01 return 710485918b0f7ef90638d8ab57c363ba1f2d0a71).
Done when: what 05.01 already met stays true: the safe form git grep -q -E [#][#][[:space:]]0[.] -- <file> is documented and tested, and the bare ## form is documented as a sh -c comment (exit 128, no pattern given).
Stop if: another file must change, including src/git.rs, tests/page_0419.rs, src/cmd.rs (held by 0408), or tests/common/mod.rs. The 05.01 safe form or bare-form note is weakened. A check command has a caret, quotes, or a space inside a git grep pattern. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0419/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0419.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0419 02 --branch pass/90.50.10.0419.05.02 --commit <sha> --file .workshop/returns/90.50.10.0419.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
