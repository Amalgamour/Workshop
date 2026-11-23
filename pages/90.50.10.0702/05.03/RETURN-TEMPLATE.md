# Return 90.50.10.0702.05.03
pack: 841660920ba0a469641307b96ac3ab8d4644d72f931bbef56808a36d86f7dee4
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - Define the text production used at lab :231-232 (why-draft-v and stamp-v). Write it from the code that prints those values. Do not leave text undefined.
w02: <done | need | blocked> - Add counters := to the registry (face 00) row at lab :205, for face 00 counter history. derive.rs:247-249 keeps that value when rendering face 00, for losslessness, even though the core does not treat it as legal.
w03: <done | need | blocked> - Narrow the open-conflict table. O2 must separate the v1 ASCII page view from the proposed whole-book format, which explicitly frames binary faces (SEQ-FILE-PLAN.md:315-327). O6 must acknowledge the settled 0700-0799 allocation (seqAddr.md:345-351). O9 is parked by R21 (DIRECTOR-RULINGS.md:82-84); do not treat it as a live conflict.
w04: <done | need | blocked> - Q2 already states R9's general rule. Mark that general rule answered, and carry the R16 dictionary 03.00 exception as open (DIRECTOR-RULINGS.md:65-66, face00.md:470).
w05: <done | need | blocked> - Tighten two implementation claims. Q6's fallback is the first nonblank trimmed note line (derive.rs:137-138). Lab :343 calls Bob's booked body imported; import checks booked bodies when a book is supplied and sends only new blocks as proposals (import.rs:45-51, 64-87). Fix the wording.
w06: <done | need | blocked> - Tighten lessons 3, 4, 6 and 7 as Codex said. Lesson 3: carry the R16 exception. Lesson 4: distinguish current implementation from an open design decision. Lesson 6: cite a dry-run transcript for the actual error, and note that avoiding spaces alone leaves the Windows caret issue. Lesson 7: the builder prompt supports the sequencing rule, but the cited material does not independently establish the reported intake incident. Keep lessons 1, 2, 5 and 8.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
