=== WORKSHOP JOB 90.50.10.0701.05.02 ===
Pack hash: 0fe67d63e293f6102674cf21a06ba8a9c6be07c310e499ff07bc9ca74783023c (log entry 18, 2026-11-23T15:29:33Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0701 02 --as <your-name>
Repo: work   Branch: returns   Start: a823ee284574be3d9f6247925b9088137a27a539
Read first: pages/90.50.10.0701/05.02/AGENTS.md (sha256 b71d13ba443c), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: lab trial for 90.50.10.0404. Builder: Grok-1. Lab page 90.50.10.0701.
Done when: cargo test --lib passes on the box; the lab's trial tests/lab_0404.rs passes on the box (a v4 return with no line is refused naming t416u and recorded; one with the line is accepted); cargo test --test wf still passes; a pass packed on template 1, 2 or 3 (such as 0403.05.01) prints and checks exactly as before.

Jobs:
  w01: Add tests/lab_0404.rs. It starts with mod common; and holds only 0404's cases. From outside, not from the builder's tests: a return on template 4 with no design review line is refused, the refusal names t416u, and it is recorded; a template 4 return with the line filled is accepted; a return for a pack on template 1, 2, or 3 is accepted without that line. cargo test --lib and cargo test --test wf still pass. Do not copy tests/common.
May touch: tests/lab_0404.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --test lab_0404
Done when (face 01): Done when: cargo test --lib passes on the box; the lab's trial tests/lab_0404.rs passes on the box (a v4 return with no line is refused naming t416u and recorded; one with the line is accepted); cargo test --test wf still passes; a pass packed on template 1, 2 or 3 (such as 0403.05.01) prints and checks exactly as before.
Stop if: another file must change, including src/ or tests/common/mod.rs or tests/wf.rs. The trial copies the harness. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0701/05.02/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0701.05.02.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0701 02 --branch returns --commit <sha> --file .workshop/returns/90.50.10.0701.05.02.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
