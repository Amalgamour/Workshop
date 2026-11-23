=== WORKSHOP JOB 90.50.10.0418.05.01 ===
Pack hash: 5f94dd5099e30e7363f9877baadab3e4fc1286be7788eeb7e247f90f46172163 (log entry 6, 2026-11-23T16:49:31Z)
You are: the builder. Claim first:
  wf claim 90.50.10.0418 01 --as <your-name>
Repo: work   Branch: prima/build   Start: c1750c32c3fb837deb34a5b9c3cafc77c1086dfc
Read first: pages/90.50.10.0418/05.01/AGENTS.md (sha256 cdd750638ab7), and in the kit folder (the folder with src/ and AGENTS.md, not the run folder that holds pages/): docs/AXIOMS.md, docs/DESIGN.md
Goal (face 01):
Goal: seated-05 in the compute core. A body on face 05 with no counter is the seat. 05.NN stays a pass. Face 06 stays counted and is never seated. Band door: 90.50.10.0400.
Builder: Grok-4 (Matthew's PC, D:\Git\grok4).
Lab: 90.50.10.0701 (wf loop lab). The lab trial is tests/lab_0418.rs, written by another view after this return. This page's test file is crates/seqaddr-core/tests/page_0418.rs.
Done when: a body on face 05 with no counter is accepted as the seat (plain 05), and 05.NN stays a pass. The board of the passes stays 05.00.
Done when: face 06 is still never seated. Plain 06 still means 06.00.
Done when: the counted-face refusal at state.rs:459-460 no longer rejects a seat on face 05; resolve.rs:182-183 no longer treats plain 05 as only a derived board; face.rs:82-84 still counts 05 and 06, and 05 also has a seat; validate.rs:345 still fits the new rule.
Done when: the change matches docs/design/drafts/SEATED-05-PROPOSAL.md and seqAddr.md:199-204 on prima/build. Code is not applied by hand outside the grant.
Done when: cargo test --manifest-path crates/seqaddr-core/Cargo.toml passes on the box.

Jobs:
  w01: In crates/seqaddr-core, apply the seated-05 rule. A body on face 05 with no counter is the seat (plain 05). 05.NN stays a pass. The board of the passes stays 05.00. Face 06 stays counted and is never seated. Change only state.rs, resolve.rs, validate.rs and face.rs, at the cited sites and any other line in those four files the new rule requires.
  w02: Add crates/seqaddr-core/tests/page_0418.rs. Show: a seat at plain 05 is accepted; a pass 05.NN is still a pass; plain 06 is still not a seat; face 06 still has no door of its own. Tests must build on Windows: no std::os::unix. If an existing test file must change, stop and say so; do not edit it.
May touch: crates/seqaddr-core/src/state.rs, crates/seqaddr-core/src/resolve.rs, crates/seqaddr-core/src/validate.rs, crates/seqaddr-core/src/face.rs, crates/seqaddr-core/tests/page_0418.rs
Must not: anything else (the return check refuses it)
The return file under .workshop/returns/ is always allowed and must be listed in changed.
Checks: cargo test --manifest-path crates/seqaddr-core/Cargo.toml
Done when (face 01): Done when: a body on face 05 with no counter is accepted as the seat (plain 05), and 05.NN stays a pass. The board of the passes stays 05.00.
Done when: face 06 is still never seated. Plain 06 still means 06.00.
Done when: the counted-face refusal at state.rs:459-460 no longer rejects a seat on face 05; resolve.rs:182-183 no longer treats plain 05 as only a derived board; face.rs:82-84 still counts 05 and 06, and 05 also has a seat; validate.rs:345 still fits the new rule.
Done when: the change matches docs/design/drafts/SEATED-05-PROPOSAL.md and seqAddr.md:199-204 on prima/build. Code is not applied by hand outside the grant.
Done when: cargo test --manifest-path crates/seqaddr-core/Cargo.toml passes on the box.
Stop if: another file must change, including any wf src/ file, another crate, or an existing test file outside may touch. Face 06 becomes seated. A 05.NN pass is rewritten or removed. A rule above reads two ways. (then end that job `need` or `blocked`, say why)
Hand back: copy pages/90.50.10.0418/05.01/RETURN-TEMPLATE.md to .workshop/returns/90.50.10.0418.05.01.md,
fill it, commit on your pass branch, created from the start commit; push only where your setup says, then:
  wf return 90.50.10.0418 01 --branch prima/build --commit <sha> --file .workshop/returns/90.50.10.0418.05.01.md --as <your-name>
Pass numbers may be written 1 or 01. Hashes are sha256 (12-char prefix).
=== END JOB ===
