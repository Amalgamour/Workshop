# Final release check: 0700 face 01, 0701.05.01 pack, 0400 face 01 v3 (base c09fa60c)

made: 2026-11-19, 2:19 PM EST, by Designer. For Prima's review. Not published; nothing
written under wf-run-gh/pages. Every cite read at returns c09fa60c (code d9110934).
Command block: COMMANDS-FOR-PRIMA.md in this folder.

Final files (the face writes and the draft read these):
- 90.50.10.0700/FINAL-0700-face01.txt, FINAL-0700-face08.txt
- 90.50.10.0700/FINAL-0701-face01.txt, FINAL-0701-face08.txt, FINAL-0701-face06-note.txt
- 90.50.10.0700/FINAL-PACK-0701-05.01.txt (sha256 5a2da32f9179413bfcaca25f5c1e04546a8b09e468a0f8b75892c5247aafc18c)
- 90.50.10/FINAL-0400-face01-v3.txt

Dry run: I ran the whole command block with the box binary against a scratch copy of
wf-run-gh in /tmp (push URLs disabled; publish-pack not run). Every step passed; wf
verify passed on 0700 (3 entries), 0701 (6 entries) and 0400 (5 entries, face 01 v3).
0700 without --system was refused with the NN00 message, as expected. The real pack hash
will differ (it carries the time).

## 1. 0700 face 01 (and face 08)

| Check | Source | Result |
|---|---|---|
| Door made only with --system --system-ref | src/addr.rs:102, :177-178; src/cmd.rs:168-178, :184-187 | PASS (dry run refused, then made) |
| Band answered | t434.md:24 "Yes, the lab band is 0700-0799" | PASS |
| Quotes | t432.md:16 | PASS (verbatim) |
| Links two-way | face 08 lists 0701, 0701 face 08 names 0700; seqAddr.md:251 | PASS |
| Pass 1 line | 0403 closed passed (packs 3313938c entry 12) | PASS |
| ASCII, plain words, no R-numbers | file | PASS |
Tensions: --system-ref is only text-checked (src/cmd.rs:174); grant none/ is a
placeholder; links are by hand until 0406.
Verdict: PASS.

## 2. 0701.05.01 pack

| Check | Source | Result |
|---|---|---|
| REQUIRED fields filled | src/cmd.rs:16; pack check :365-367 | PASS (dry run packed) |
| may touch inside grant tests/ | src/cmd.rs:369-371 | PASS |
| Draft needs a new 06 note | src/cmd.rs:297-298 | PASS (face 06 note written first) |
| Harness range | tests/wf.rs:10-170 | PASS |
| Return strings | tests/wf.rs:94, :858, :994, :1575, :1789 | PASS (five; v3 said two, fixed) |
| Windows cites | tests/wf.rs:4, :820, :841, :954, :959, :1021, :1117 | PASS |
| parse_return | src/cmd.rs:467-482 | PASS |
| Axioms | Axioms.md:9, :15, :29 | PASS |
| Start | c09fa60c resolves in work (git::commit, src/cmd.rs:380) | PASS |
| Hold | 0403 closed passed | lifted |
| Independence (t422.md:7-8) | open passes on other pages | TENSION, see below |
Tensions: 90.50.10.0401.05.01 and 0402.05.01 are still at pack (wf cannot withdraw a
pack) and list tests/wf.rs. Both are dropped (face 06 entry 7), never published, and the
observer filed it (entry 8). No builder can claim them from the packs branch, so the
lab pass does not share files with live work. wf checks overlap only within one page
(refuse_overlap, src/cmd.rs:339-355). 0408 is the fix. Prima decides at review.
Also: the grant reads approval of the lab as approval of tests/ (t432u, Q8 t432.md:7);
no hostile pass yet. Within wf, src/addr.rs is now the one home for the address rules
(its only caller is src/cmd.rs:186), so the "rules copied, not shared" tension is
retired inside wf. A narrower one stays: addr.rs is a copy of seqaddr-core, matched
against 7c1c0bf1 because 79f12ed is not in that clone (src/addr.rs:1-4).
Verdict: PASS, releasable on Prima's review.

## 3. 0400 face 01 v3

| Check | Source | Result |
|---|---|---|
| Follows v2 | packs 3313938c pages/90.50.10.0400/01.md:2 (entry 4, 3aa6fa3921a7) | PASS |
| 0403 line | closed passed, packs 3313938c entry 12 | PASS |
| Lab band named | t432u, t434.md:24 | PASS |
| Goal line quote | t423u.md:7 (double spaces shortened, said in the v3 notes) | PASS |
| Dry run | face-write 01 printed v3 (entry 5) | PASS |
Verdict: PASS.

## 4. 0404 (not final)

PACK-0404-v3.md with its v4 note stays ON HOLD until 0701.05.01 closes passed; its start
is the commit where 0701 lands.
