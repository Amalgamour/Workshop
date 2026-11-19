# Release check, band 90.50.10.04xx (door 0400, job 0401, job 0402)

checked by: Designer   date: 2026-11-19, about 1:25 PM EST
checklist: docs/design/RELEASE-CHECK.md @ c0e5b22 (v1 + v2 note)
authority: t414u (docs/review/DIRECTOR-WORDS-t414u.md:3)

Plain words: two packs were checked against the design. Both are blocked for now. Each
needs a small fix, listed at the end. Job 0401 is dropped and is not checked.

## What was compared (path @ last-change commit on build)

- docs/spec/Axioms.md @ 3291593; docs/spec/seqAddr.md @ 3291593
- docs/spec/DIRECTOR-RULINGS.md @ 26a17be; docs/spec/Design.md @ 3291593
- docs/spec/drafting.md @ 3291593; docs/spec/workflow-loop.003.md @ 420fc98
- docs/spec/face00.md @ 1cd06de; docs/design/DESIGN.md @ c438459
- crates/seqaddr-core/src/addr.rs @ 79f12ed
- DIRECTOR-WORDS t413u @ bf2c566, t414u @ d840bac, t415u @ b11b48f
- Builder context: docs/spec/ADDRESS-DRIFT-t413u.md and
  docs/journal/2026-11-19-address-drift-t413u.md @ 8701a04
- t416u: no recorded file. Relayed by Prima only (RELEASE-CHECK.md v2 note).

Artifacts (read-only; folders are untracked in wf-run-gh, so sha256 prefixes are given):
- pages/90.50.10.0400/: log.jsonl 1cc4d90aefae, 00.md 829de8a26c1c, 01.md 7ad61e588c84
- pages/90.50.10.0401/: log.jsonl 440b1e70f2cf
- pages/90.50.10.0402/: log.jsonl cff83ac99adf, 05.01/PACK.md 2cf1de306014,
  05.01/PROMPT.md 58633e924cd9, 05.01/AGENTS.md cce889f088b9
Paths below are short: `0400/01.md:4` means pages/90.50.10.0400/01.md line 4.

## 90.50.10.0400, the band door

| Item | Source file:line | Seen in artifact | Result |
|---|---|---|---|
| A1-A3 desk 90, shelf 50, book 10 | t413u.md:7; seqAddr.md:30 | 0400/00.md:1 | PASS |
| A4 page 0400 is 0100 or more | t413u.md:9; seqAddr.md:219-224 | 0400/00.md:1 | PASS |
| A5, A6 band 0400; door ends in 00 | t413u.md:9; seqAddr.md:241 | 0400/01.md:4 | PASS |
| A9 not 99, PP99 or 9999 | RELEASE-CHECK.md v2 A9 | 0400/00.md:1 | PASS |
| Door does no work | t413u.md:9 ("That is how you enter, find the work") | 0400/01.md:4 "No work is done on this page and it drafts no passes" | PASS |
| Name: "door" vs "band head" | t413u.md:9 vs seqAddr.md:241, DIRECTOR-RULINGS.md:57; DESIGN.md:149 | 0400/01.md:4 "band door" | TENSION (open, question 1) |
| Registry points to live work | Axioms.md:27 ("A pointer points; the source governs"); t413u.md:9 ("find the work") | 0400/01.md:6 lists 0401 as job 1; 0401 is dropped and job 1 closed on 90.50.00.0001 (90.50.00.0001/log.jsonl:12-13). 0400/01.md:7 says "after job 1 lands"; it landed at 60dd7e25 | FAIL |
| Registry written by hand in face 01 | seqAddr.md:241 (head holds the band's contents); face00.md:206 (contents is compute-only); drafting.md:40 (derived content is not hand-written) | 0400/01.md:5-7; reason in 0400/06.md:4 | TENSION (temporary only; see below) |
| The page says it is temporary | Axioms.md:23 ("what changed, why, and what now governs"); Axioms.md:25 ("A required absence is a defect: report it") | Only 0400/06.md:4 says "glitch". 01.md does not say temporary or name what replaces it | FAIL |
| Stamp has type and state | DIRECTOR-RULINGS.md:54; face00.md:141 (band head is `type: band`), :203-207 | 0400/00.md:4-9: no type, no state, no registry. All wf v0 pages lack them | TENSION (t401u.md:7 allows glitchy first loop) |
| Grant fits a no-work page | Axioms.md:13; 0400/01.md:4 | 0400/00.md:8 `grant: docs/ (from t413u)`; log.jsonl:1 grant_ref t413u. t413u grants no paths; it gives the why | TENSION |
| Person who started the page | Axioms.md:13 ("granted, never claimed"); wf src/cmd.rs:171 @ 60dd7e25 ("the person starts their own page") | log.jsonl:1 actor `matthew`, same second as Prima's entries 2-3 (18:11:09Z) | TENSION (question 2) |
| H1 habits traced | RELEASE-CHECK.md v2 H1 | Address traced to t413u (0400/01.md:4) | PASS |

Is it acceptable as a temporary door? Yes, but only after a new face 01 version (v2,
appended; v1 stays) that says:
1. "Temporary: this registry is written by hand because wf v0 has no face 00 type or
   registry. It is replaced when wf writes `type: band` and a compute-made contents list
   on face 00" (name that job once it is packed).
2. 0401 is dropped: it repeats job 1, which closed on 90.50.00.0001.05.01 (passed).
3. 0402 is the live job, starting from origin/returns 60dd7e25 (or the job that replaces it).
4. The `docs/` grant is a placeholder and no pass may be drafted here. Better: Matthew
   narrows it with a new grant entry to a path nothing writes (wf `grant` is person-only,
   src/cmd.rs:199-204 @ 60dd7e25), with grant_ref naming the recorded approval.
Item 4's narrowing is advice; items 1-3 are needed for release.

Verdict 0400: BLOCK. Must change: face 01 v2 with items 1-3. Prime can write face 01.

## 90.50.10.0401, job 1 again: N/A, dropped

| Item | Source file:line | Seen in artifact | Result |
|---|---|---|---|
| All checks | Prima's drop; journal:14 ("It duplicates the work that already landed") | 0401/01.md:4 is the same goal as 90.50.00.0001; that pass closed passed (90.50.00.0001/log.jsonl:12-13, commit 439a4eb2) | N/A, dropped |

Keep the folder as history; do not delete it.
- Axioms.md:23: "A change that is not recorded did not happen. The past is not
  rewritten". Deleting it erases a step.
- DIRECTOR-RULINGS.md:153-154: once a page exists and is linked, it can only be retired.
  0400/01.md:6 links to it.
- DIRECTOR-RULINGS.md:129-130: once an address has a title, the pairing is fixed. So
  0401 is never reused; new work takes 0403 and up.
- Record the drop as a face 06 note on 0401 (append). Do not publish its 05.01: the pass
  is at `pack` (0401/05.md) and wf cannot withdraw it (ADDRESS-DRIFT-t413u.md:28), so a
  published copy could still be claimed.
- Small fix in the same note: 0401/06.md:4 calls 90.50.00.0001 "retired", but its pass
  closed passed. Say "moved from; job 1 closed there".

## 90.50.10.0402, job 2: the address guard for `wf init-page`

| Item | Source file:line | Seen in artifact | Result |
|---|---|---|---|
| A1-A6, A9 page address | t413u.md:7, :9; seqAddr.md:30, :241 | 0402/00.md:1 | PASS |
| Start commit is real | ADDRESS-DRIFT-t413u.md:15; 0402/06.md:4 | PACK.md:8 `60dd7e25...`. git in wf-run-gh: it is the tip of origin/returns, "wf: return 90.50.00.0001.05.01 (log)"; parent chain holds job 1's 439a4eb2 | PASS |
| Pack, prompt and AGENTS hashes match the log | t373u.md:3 | sha256 PACK.md 2cf1de306014 = log.jsonl:6 pack_hash; AGENTS.md cce889f088b9 = PROMPT.md:6 | PASS |
| Rules traced, not habit (H1) | RELEASE-CHECK.md v2 H1; t415u.md:5 | PACK.md:16 cites crates/seqaddr-core/src/addr.rs (axis_role, page_kind, band_head @ d840bac). Test page 10.10.10.0401 (PACK.md:18) = first valid desk/shelf/book and first work page (t413u.md:7, :9) | PASS |
| Refuses 00-09 on desk, shelf, book; book 00; pages 0000-0099; NN00 | t413u.md:7, :9; addr.rs:204-210, :239-248 | PACK.md:16 | PASS |
| Refuses work at 99 on an axis, PP99, 9999 (A9) | seqAddr.md:31, :39, :226, :242, :249; DESIGN.md:137; addr.rs:186-187, :208, :246, :248 | PACK.md:16 has no 99 rule; PACK.md:18 has no 99 test. 90.50.10.0499 or 99.50.10.0401 would pass as work. PACK.md:13 outcome says it refuses "a work page at a system address" | FAIL |
| Message word "band door" | t413u.md:9 vs seqAddr.md:241 | PACK.md:16 "NN00 is the band door" | TENSION (question 1) |
| Rules copied into wf, not shared | Axioms.md:15 ("Do not copy the parent ... both create drift") | PACK.md:16 copies; why in ADDRESS-DRIFT-t413u.md:15 (crate not on the wf branch) | TENSION (fine for now if a later job shares the crate or a test pins the same cases) |
| `--system` needs a ref | t413u.md:7 ("without it being system level"); Axioms.md:13 | PACK.md:17: any `tNNNu` text is accepted; nothing checks the ref is a recorded ruling | TENSION |
| Grant authority | Axioms.md:13; t311u.md:8 ("Where is the authority for this action.") | PACK.md:11 `grant: src/, tests/ (t413u)`. t413u asks "How do we fix it?" (t413u.md:9) but grants no paths. The fix approval "1-3 is good..." is quoted only in journal:4, not in a DIRECTOR-WORDS file | TENSION |
| Pack header complete | workflow-loop.003.md:238 (overview; draft, not live), :250 (no axioms: finding) | PACK.md:12 `axioms:` empty; PACK.md:14 `overview:` empty | TENSION |
| Return holds noticed, unprompted, overflow | t226u.md:11 | RETURN-TEMPLATE.md:5, :11-12 | PASS |
| Back-link to the band door | seqAddr.md:251; t245u.md:13 | 0402/08.md empty. The band tie is by address only (Axioms.md:27 allows "inherited through the address") | TENSION |
| Stamp type and state | DIRECTOR-RULINGS.md:54; face00.md:140 | 0402/00.md:4-9 none (wf v0) | TENSION (t401u.md:7) |
| Person who started the page | Axioms.md:13; src/cmd.rs:171 @ 60dd7e25 | log.jsonl:1 actor `matthew`, same second as entries 2-6 (18:13:10Z) | TENSION (question 2) |
| Design-alignment review before the return completes (T1, t416u) | no recorded words | RETURN-TEMPLATE.md has no such line | TENSION (not recorded; not judged) |

Verdict 0402: BLOCK. Must change: w01 also refuses 99 on the desk, shelf and book axes,
PP99 and 9999, each with its own message naming seqAddr.md:31/:242/:226; w03 adds
refused tests (for example 99.50.10.0401, 90.99.10.0401, 90.50.99.0401, 90.50.10.0499,
90.50.10.9999). `--system` with a ref still lets system pages through.
Should fix (not blocking): fill `axioms:` (suggest `1.7.8`) and `overview:`; add the
recorded approval to grant_ref once it is filed.
How to change it without rewriting: 05.01 is packed, not claimed, not published. Keep it
in the log as history. Pack the fixed version as the next pass on 0402 if wf allows a
second pack; if not, use 0403 and drop 0402 the same way as 0401. Prima picks (wf limit,
ADDRESS-DRIFT-t413u.md:28).

## Answers Prima asked for

99, PP99, 9999: yes, refuse them for work pages. The files are not silent and do not
conflict. seqAddr.md:31 ("99 / 9999 | pointer: look for the next location"), :39 (desk
99 reserved pointer), :226 (9999 book continuation), :242 ("PP99 is the band's
continuation"), :249 ("99 at any level is a pointer"); DESIGN.md:137 quoting the
Director's own seqaddr page: "Those addresses with a seq00 or seq99 are special
locations and cannot be normal pages"; addr.rs:186-187, :208, :246, :248 mark them
pointer and continuation. t413u.md:7-9 speaks only of 00-09; it does not allow 99.
DIRECTOR-RULINGS.md:38 keeps sentinels on these four axes. No Director question needed.

t416u gate: a separate later job, not 0402. Reasons:
- No recorded words yet (no DIRECTOR-WORDS-t416u.md); a pack built on it has no
  traceable authority (Axioms.md:13, :25; t311u.md:8).
- Different outcome, different frame: 0402 is the address guard (PACK.md:13); the gate is
  a return check. Axioms.md:21: the frame says where to stop and what done looks like.
- One page, one job: docs/design/WORK-BOOK-SPEC.md:79 "One work page is one job." This is
  Designer's draft, not a ruling (WORK-BOOK-SPEC.md:3). I found no recorded ruling that
  says "one job per pack" in those words; the nearest are t249u.md:9 (one-page work) and
  t223u.md:8 (a pack is a jobs list on the page's own 05).
- Design does not change on a packed pass (t381u.md:8, :17).
So: record t416u first, then pack it as its own job (Prima's "first wf lint check" fits
workflow-loop.003.md:234-250, the lint table).

## Open questions for Matthew (four parts each; "(default)" = follows the existing shape)

1. Is a band head (0400) also the band's door?
   - Proposed: (default) yes. The 00 end of the band is its door, as 00 is the door of
     desk, shelf, book and page. Add a new note after DIRECTOR-RULINGS.md:57; do not
     rewrite it. Other option: keep "door" for full zeros only and call 0400 "band head".
   - Why: t413u.md:9 says "0400 being the door"; seqAddr.md:241 and the reading at
     DIRECTOR-RULINGS.md:57 say otherwise; wf messages already say "band door".
     Who gets hurt: builders who read two words for one place.
   - Axioms: 2 (Axioms.md:15) pass; 6 (:23) pass, a new note; 8 (:27) pass; 1 (:13) pass,
     he decides.
2. Who starts a wf page?
   - Context: wf records the starter as the person ("--as must match --person",
     src/cmd.rs:171), so these pages show actor `matthew` in the same second as Prima's
     entries.
   - Proposed: (default) the log names who really ran it. The person is named as the one
     who granted it, with a grant_ref to a recorded file. Other option: build-stage
     allowance, Prima acts as him, marked build-stage so it can be found later.
   - Why: Axioms.md:13 "Authority is granted, never claimed"; t329u.md:7 says build-stage
     allowances are temporary. Who gets hurt: an observer who reads the log and cannot
     tell who acted.
   - Axioms: 1 (:13) pass for default, tension for the other; 6 (:23) pass; 8 (:27) pass.

## Overall verdict

- 0400: BLOCK until face 01 v2 (temporary marker and replacing step, 0401 dropped,
  0402 current).
- 0401: N/A, dropped. Keep the folder, unpublished, with a drop note.
- 0402: BLOCK until the guard also refuses 99 on an axis, PP99 and 9999, with tests.
- For Prima, not Matthew: file the "1-3 is good" approval (journal:4) and t416u as
  DIRECTOR-WORDS files, so grants and the later gate have recorded authority.

Limits: I did not run wf or any tests. Line cites in wf src are at 60dd7e25. Judgement
items: the temporary-door wording and the copy-vs-share tension.
