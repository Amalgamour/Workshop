=== WORKSHOP JOB 90.50.10.0408.05.01 ===
Pack hash: d9021b979577182fdca33d58bd8cf077630e094ec1750b50ca2a131894d5166a (log entry 6, 2026-11-23T16:30:20Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0408 01 --as <your-name>
Repo: work   Branch: returns   Start: a823ee284574be3d9f6247925b9088137a27a539
Read first: pages/90.50.10.0408/05.01/AGENTS.md (sha256 1a5818c1bb20), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: Prime can withdraw a pass that is at pack and has no claim. The pass stays in the log as withdrawn, and a later claim is refused. Band door: 90.50.10.0400.
Builder: Grok-2 (Matthew's PC, D:\Git\grok2).
Lab: 90.50.10.0701 (wf loop lab). The lab trial is tests/lab_0408.rs, written by another view after this return. This page's own test file is tests/page_0408.rs.
Done when: withdraw works at pack with no claim.
Done when: withdraw is refused at open or later.
Done when: a later claim is refused.
Done when: the log keeps the pass.
Done when: cargo test --test page_0408 passes on the box.
Done when: the lab trial tests/lab_0408.rs passes in lab 0701.

Jobs:
  w01: Add wf withdraw <page> <NN>, prime only. It runs only when the pass tail is pack and there is no claim. Append a log entry and set the tail to withdrawn. The pass stays in the log. Refuse it when the tail is open, return, review, or closed. A later claim is refused. withdrawn is not an open tail, so the pass no longer holds its files (src/page.rs:151). Wire the command in src/lib.rs help and dispatch, and in src/cmd.rs.
  w02: Add tests/page_0408.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Cover withdraw at pack with no claim, a refusal at open or later, a refused later claim, and the pass still present in the log.
May touch: src/cmd.rs, src/lib.rs, src/page.rs, tests/page_0408.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --lib; cargo test --test page_0408
Done when (face 01): Done when: withdraw works at pack with no claim.
Done when: withdraw is refused at open or later.
Done when: a later claim is refused.
Done when: the log keeps the pass.
Done when: cargo test --test page_0408 passes on the box.
Done when: the lab trial tests/lab_0408.rs passes in lab 0701.
Stop if: another file must change, including src/render.rs or templates. The command spelling wf withdraw is wrong. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0408/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0408.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0408 01 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0408.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
