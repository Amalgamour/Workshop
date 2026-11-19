# Builder self-check, band 90.50.10.04xx after the RELEASE-CHECK-90.50.10 fixes

checked by: Prima builder-b21 (not Designer; this is not the release check)
date: 2026-11-19, about 1:40 PM EST
checklist: docs/design/RELEASE-CHECK.md @ 55d87c8 (v1 + v2 note); review: docs/review/RELEASE-CHECK-90.50.10.md @ 55d87c8
compared: docs/spec/seqAddr.md, docs/design/DESIGN.md @ c438459, crates/seqaddr-core/src/addr.rs @ 79f12ed, DIRECTOR-WORDS t413u-t415u
artifacts (wf-run-gh/pages, untracked, unpublished; sha256 prefix):
- 90.50.10.0400/log.jsonl 6168b2253b6c, 01.md ae7931e81ea5 (face 01 v2, entry 4)
- 90.50.10.0401/log.jsonl 97e6f0009dae (drop note, entry 7)
- 90.50.10.0402/log.jsonl 9da134cffcbd (drop note, entry 7)
- 90.50.10.0403/log.jsonl 3ee93090df27; 05.01/PACK.md b2de54ce03fd (= pack hash); PROMPT.md 0d2cc64d401d; AGENTS.md 7f2ffaaeefb1
I ran wf verify on each page (ok). I did not run the 0403 job.

## Fixes asked for
| Item | Seen | Result |
|---|---|---|
| 0400 face 01 v2: says temporary, why (no face 00 registry in wf v0), replaced by `type: band` + compute contents | 0400/01.md:5 | PASS (the replacing wf job is not packed; the note says so) |
| 0400: 0401 dropped, why | 0400/01.md:7 | PASS |
| 0400: live job named | 0400/01.md:9 (0403; 0402 marked superseded :8) | PASS |
| 0400: docs/ grant noted as tension | 0400/01.md:10 | PASS (still a tension, not narrowed; only Matthew can, `grant` is person-only) |
| 0401 face 06 drop note, with "moved from; job 1 closed there" | 0401/06.md entry 7 | PASS; pack not published; folder kept |
| 0402 face 06 drop note "superseded by 0403 ..." | 0402/06.md entry 7 | PASS; pack not published; folder kept |
| 0403 adds 99 on any axis, PP99, 9999, with messages and tests | PACK.md w01, w03 (99.50.10.0401, 90.99.10.0401, 90.50.99.0401, 90.50.10.0499, 90.50.10.9999) | PASS |
| 0403 cites seqAddr.md:31, :39, :226, :242, :249; DESIGN.md:137; addr.rs | PACK.md overview and w01; 06.md; 04.md | PASS (line contents re-read at HEAD be04bb2) |
| 0403 axioms filled | PACK.md:12 `1.7.8` | PASS |
| 0403 overview filled, back-link to door 0400 | PACK.md:14; 01.md | PASS (link in text only; wf has no face 08 link op, so 08.md is empty: TENSION, S9/X10) |
| 0403 starts from current origin/returns | PACK.md:8 60dd7e25 = origin/returns (fetched 1:35 PM EST) | PASS |

## Checklist on 0403
| # | Result | Note |
|---|---|---|
| A1-A4, A7 | PASS | 90 / 50 / 10 / 0403, widths 2.2.2.4 |
| A5, A6 | PASS | band 0400; door 0400; job at 0403 |
| A8 | PASS | nothing in 0001-0099 |
| A9 | PASS | not 99, PP99, 9999 |
| H1 habits traced | PASS | address: next free in band after 0401/0402, which are fixed to their titles (DIRECTOR-RULINGS.md:129-130 via the review); test page 10.10.10.0401 is the first valid work address (t413u.md:7, :9); start = origin/returns because job 1 landed there |
| X3 authority | TENSION | grant_ref t413u; the "1-3 is good" approval is not a DIRECTOR-WORDS file yet |
| X4 copy vs share | TENSION | rules copied into src/addr.rs, crate not on the wf branch (Axioms.md:15) |
| X6 why | PASS | 06.md and overview give the why |
| X7 frame | PASS | outcome, may touch, checks, stop if, done when |
| X8 lineage | PASS | 0401/0402 kept, notes appended; 0400 face 01 v1 kept in the log |
| X9 missing | PASS | replacing wf registry job marked as not packed |
| X11 trial | TENSION | no hostile pass |
| S7 / P1-P4 stamp type, state, registry | TENSION | wf v0 has none (t401u.md:7) |
| D10 / S9 links both ways | TENSION | door lists 0403 and 0403 names the door, by text only |
| Person who started the page | TENSION | log actor `matthew`, run by Prima (review question 2) |
| "band door" vs "band head" (C1) | TENSION | message says both: "NN00 is the band head, the band's door" |
| `--system` ref not checked against a recorded ruling | TENSION | as in 0402 |
| T1 (t416u) | TENSION | not recorded; not judged |
| Windows check | PASS | `cargo test --lib addr` should compile there (src/ has no unix-only code); e2e left to the checker |

verdict (builder's view): no FAIL found; the tensions above carry over from the review.
