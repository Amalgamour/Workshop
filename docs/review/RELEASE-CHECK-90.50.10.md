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

## Addendum 1 (2026-11-19, 1:27 PM EST, Designer): re-check after the fixes

Date fix: the date line at the top says "about 1:25 PM EST"; v1 was written at 1:20 PM EST.
v1 above is not changed (Axioms.md:23).

Compared (build HEAD 803cbcd): checklist RELEASE-CHECK.md @ c0e5b22; Axioms.md @ 3291593;
seqAddr.md @ 3291593; DESIGN.md @ c438459; addr.rs @ 79f12ed; AXIOM-CITE-GRAMMAR-review.md
@ af51f3e; DIRECTOR-WORDS t416u @ be04bb2, t420 @ 803cbcd; SELF-CHECK-90.50.10.0403-b21.md
@ 184abb3. wf-run-gh: origin/returns fetched at 1:25 PM EST = 60dd7e254df0.
Artifacts (untracked, sha256 prefix): 0400/log.jsonl 6168b2253b6c, 0400/01.md ae7931e81ea5;
0401/log.jsonl 97e6f0009dae; 0402/log.jsonl 9da134cffcbd; 0403/log.jsonl 3ee93090df27,
0403/05.01/PACK.md b2de54ce03fd, PROMPT.md 0d2cc64d401d, AGENTS.md 7f2ffaaeefb1.
Log chains: every entry's `prev` is the sha256 of the line before, on all four pages. The
first lines of 0400 (1-3), 0401 (1-6) and 0402 (1-6) hash to the v1 values above
(1cc4d90aefae, 440b1e70f2cf, cff83ac99adf), so nothing earlier was rewritten.

New Director words since v1:
- t416u.md:4 records the fix-plan approval ("1-3 is good, remove the old WF pages, or mark
  them as retired"). t416u.md:7 records the gate: "Novel work requires additional reviews
  against design documents for alignement. Must be confirmed before the return is
  complete. We can't force it but we can force it to confirm it did this via our WF"
  (spaces shortened).
- t420.md:4, :6, :10 answer v1 questions: the band head is the band's door; a pack lives on
  the job page's own face 05; 0020-0099 are system only. t420.md:8 approves a versioned
  seqAddr.md note. Question 2 (who starts a page) is not answered (t420.md:12, :16).

| Item | Source file:line | Seen in artifact | Result |
|---|---|---|---|
| 0400 face 01 v2 appended, v1 kept | Axioms.md:23 | 0400/log.jsonl:4 (new entry, 18:22:07Z); v1 still at log.jsonl:2; 01.md:2 "v2 (entry 4)" | PASS |
| 0400 says temporary, why, what replaces it | Axioms.md:23, :25 | 0400/01.md:5 (job not packed yet; says it will be named) | PASS |
| 0400 0401 dropped, 0402 superseded, 0403 live | Axioms.md:27 | 0400/01.md:7, :8, :9 | PASS |
| 0400 band range stops at 0498 | seqAddr.md:242 | 0400/01.md:4 "0401-0498" | PASS |
| 0400 "door" wording | t420.md:4 | 0400/01.md:4 | PASS (C1 answered) |
| 0400 docs/ grant | Axioms.md:13 | 0400/01.md:10 notes it as a tension; still `docs/` (00.md:8) | TENSION (only Matthew can narrow) |
| 0401 drop note on face 06, kept, not published | Axioms.md:23; DIRECTOR-RULINGS.md:129-130, :153-154 | 0401/06.md:5 (log.jsonl:7); 05.md still `pack`, folder untracked in wf-run-gh | PASS |
| 0402 drop note on face 06, kept, not published | same | 0402/06.md:5 (log.jsonl:7); 05.md still `pack`; folder untracked | PASS |
| A1-A4, A7, A8 for 0403 | t413u.md:7, :9; seqAddr.md:14, :30 | 0403/00.md:1 90.50.10.0403 | PASS |
| A5, A6, A9 for 0403: inside band 0400, not NN00, not PP99, not 9999 | t413u.md:9; seqAddr.md:241-242 | 0403 in 0401-0498 | PASS |
| Pack lives on the job page's own 05 | t420.md:6 | 0403/05.md:4 | PASS (C2 answered) |
| Pack hash matches log | t373u.md:3 | sha256 PACK.md b2de54ce03fd = log.jsonl:6 pack_hash; AGENTS.md 7f2ffaaeefb1 = PROMPT.md:6 | PASS |
| Start is the tip of origin/returns | 0403/06.md:4 | PACK.md:8 60dd7e25 = `git rev-parse origin/returns` after fetch | PASS |
| w01 refuses 99 on desk, shelf, book | seqAddr.md:31, :39, :249; addr.rs:186-187, :208 | PACK.md:16 "99 on any axis" | PASS |
| w01 refuses PP99 and 9999 (9999 first) | seqAddr.md:226, :242; addr.rs:246, :248 | PACK.md:16 | PASS |
| w03 tests each 99 case | RELEASE-CHECK.md v2 A9 | PACK.md:18: 99.50.10.0401, 90.99.10.0401, 90.50.99.0401, 90.50.10.0499, 90.50.10.9999 | PASS |
| w03 tests the 00-09 cases on every axis | t413u.md:7 | PACK.md:18 has shelf 05 and book 00, but no desk 00-09 and no book 01-09 e2e case; w01 asks unit tests "for each rule" (PACK.md:16) | TENSION (small; unit tests should cover it) |
| `axioms: 1.7.8` | Axioms.md:5 ("`1.7.8`: authority, then missing, then connection"), :9 (cold set before a write), :27 | PACK.md:12 | PASS as the cold set. It is one ordered chain, not a list of three (a list would be `1,7,8`, Axioms.md:5) |
| `1.7.8` misread risk | AXIOM-CITE-GRAMMAR-review.md:13 (three-number chains split readers), :133-140 (G1 open); Axioms.md:7 (`7.8` alone = "a connection that is missing") | PACK.md:12 | TENSION (no file makes it a rule; Axioms.md:5 glosses this exact chain, so risk is low) |
| Back-link to door 0400 | seqAddr.md:251; Axioms.md:27 | 0403/01.md:4 and PACK.md:14 name the door; door lists 0403 (0400/01.md:9). Both ways, in text; 0403/08.md empty | PASS (text both ways); face 08 empty is a TENSION (wf has no link op) |
| Grant authority | Axioms.md:13; t311u.md:8 | PACK.md:11 grant_ref still `t413u`; the approval is now recorded at t416u.md:4 | TENSION (name t416u.md:4 next time) |
| Rules copied, not shared | Axioms.md:15 | PACK.md:16; 0403/06.md:4 says tension | TENSION |
| Stamp type and state | DIRECTOR-RULINGS.md:54 | 0403/00.md:4-9 none | TENSION (wf v0; t401u.md:7) |
| Person who started the page | Axioms.md:13 | 0403/log.jsonl:1 actor `matthew`, same second as Prima's entries | TENSION (still open, t420.md:12) |
| T1, t416u gate | t416u.md:7 | RETURN-TEMPLATE.md:1-12 has no design-review line | TENSION. The gate acts when the return completes, not at release. Until wf lint has it, Prima must get the builder's stated design review (files compared) before sign-off |

What t416u and t420 change in RELEASE-CHECK.md (noted here; that file not edited now):
- T1 now has recorded words (t416u.md:7). It should become a hard check at return time:
  for novel work, the return states the design review and the files compared; no
  statement, no completion.
- Gate placement: unchanged, a separate job. t416u.md:7 says WF forces the confirmation,
  which is a tool check, not 0403's address guard. The "first wf lint check" idea is
  Prima's (t416u.md:11), not his words.
- C1, C2, C4 are answered (t420.md:4, :6, :10). C3 is to be closed by a seqAddr.md
  versioned note (t420.md:8). Question 2 stays open.

b21 self-check (SELF-CHECK-90.50.10.0403-b21.md) against this re-check:
- Agrees: all fixes PASS (:17-27); A1-A9 PASS (:32-35); same tensions: grant authority,
  copy vs share, no trial, stamp, text-only links, page starter, `--system` ref, T1 (:37-49).
- Misses: its date says "about 1:40 PM EST" and origin/returns "fetched 1:35 PM EST"
  (:4, :27). Both are later than now; the logs show 18:22Z = 1:22 PM EST. The time is wrong.
- Misses: :37 says the "1-3 is good" approval is "not a DIRECTOR-WORDS file yet", and :49
  says T1 is "not recorded". Both were recorded at be04bb2, before the self-check (184abb3).
- Misses: `1.7.8` is marked "filled" (:25), with no check of what it means.
- Misses: no desk 00-09 / book 01-09 e2e case; no check of the log chain.
- Narrow: it compared seqAddr, DESIGN, addr.rs and t413u-t415u only (:6), not
  DIRECTOR-RULINGS, face00 or workflow-loop.
- Unverified by me: :50 says src/ has no unix-only code.

Verdict, addendum 1:
- 0400: PASS as a temporary door. Tension: the docs/ grant, until Matthew narrows it.
- 0403: PASS, release. No FAIL found. Tensions carry: grant_ref names t413u not t416u.md:4;
  rules copied; no face 08 link; stamp type and state; page starter; `1.7.8` reading;
  desk 00-09 e2e case. At sign-off, Prima confirms the builder's design review (t416u.md:7).
- 0401, 0402: N/A, dropped. Keep them unpublished; their passes are still claimable.
