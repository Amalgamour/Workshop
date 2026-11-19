# Release check, 90.50.10.0415 (pass 1 draft)

checked by: Cursor-C (Design)
date: 2026-11-19, 3:25 PM EST
checklist: docs/design/RELEASE-CHECK.md @ 8e96151d (blob ef4c77486bcfddbdf8a013c6ff5651bb3df11aea)
compared: Axioms.md @ 8e96151d (blob b3d891b202b231c828a091f0f0422eb22f8d6f29); seqAddr.md @ 8e96151d (blob 692f0b18ad40a42ad34e66b9002736f2dcc2543f); DIRECTOR-RULINGS.md, DIRECTOR-WORDS, STAGE-PLAN-90.50.10.md at 8e96151d
code compared: origin/returns 3646e344 (src/log.rs identical to e30050dc; that commit adds only the 0701 log)
artifact: docs/design/drafts/90.50.10.0415/ at this commit
pack sha256: de57bdab5850ad99af189b671e934fd2ed22c5f8e740eb38a47e857e497eee7a

Not published. Nothing written under the real pages. Scratch dry run only (FINAL-RELEASE-CHECK section 6).

## 1. Address

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| A1-A4, A7 | t413u.md:7, :9; seqAddr.md:14 | 90.50.10.0415: desk 90, shelf 50, book 10, page 0415 | PASS |
| A5, A6 | t413u.md:9; seqAddr.md section 10 rule 4 | job page in band 0400, not the door | PASS |
| A8 | seqAddr.md:228; DIRECTOR-RULINGS.md:84 | not in 0001-0099 | PASS |
| A9 | seqAddr.md:242, :325 | not PP99, not 99, not 9999 | PASS |
| H1 slot | t415u.md:5; DIRECTOR-RULINGS.md:129-130 | 0415 is the next slot after 0414. 0405, 0410 and 0497 stay unused because they were titled and then parked (STAGE-PLAN 11.4, 12.5, 13.4). An address once titled is never reused. 0415 was never titled in book 90.50.10. The only 0415 in docs/ is an old library page in another book (docs/reference/LIB-BUILD-SURVEY.md:101) | PASS |
| ASCII | DIRECTOR-RULINGS.md:16 | every draft file in this folder is bytes 0x20-0x7E plus newline | PASS |

## 2. Faces 01, 08 and 06

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| Done when lines | src/page.rs:99-110 at e30050dc | four lines, each starting "Done when:". They include "the wf e2e suite passes on Windows" and "Linux still fsyncs the directory" | PASS |
| Lab link both ways | t422.md:8; t425u.md:3; seqAddr.md:251 | face 01 and face 08 name lab 0701 and tests/lab_0415.rs. The lab's replacement faces name 0415 back | PASS (texts exist; not written on the real lab yet) |
| Needs | t422.md:8 | needs 0701 pass 1, which is closed at 3646e344. Needed by 0498, written when 0498 is made | PASS |
| Face 06 before draft | src/cmd.rs:297-298 | FINAL-0415-face06-note.txt. It does not invent a grant ref | PASS |
| Plain words | DIRECTOR-RULINGS.md:16 | face 01 says fsync as a side label | PASS |

## 3. Pack

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| Required fields | src/cmd.rs:16, :365-367 | outcome, repo, start, may touch, checks, stop if, and jobs w01 and w02 | PASS (scratch pack accepted) |
| may touch inside grant | src/cmd.rs:369-371 | may touch src/log.rs; grant src/log.rs | PASS |
| Start resolves | src/cmd.rs:380; src/git.rs:18-19 | 3646e3448985d1cf40da82b262cfd8852ae59234 | PASS (scratch rev-parse) |
| Checks under cmd /C | src/git.rs:111; src/cmd.rs:748 | stored checks are "cargo test --lib; cargo test --test wf". Two commands, no shell tool. On Windows each runs as cmd /C | PASS |
| Pack template note | templates/pack.txt:19 | printed PACK.md adds "(one command each, split by ;)" after the checks. That note is not a third command | PASS |
| Unix fsync kept | src/log.rs:122-127; tests/wf.rs:789-798 | w01 keeps File::open plus sync_all on Unix, and keeps the call inside append so the source test still matches. A new unit test locks that, and it runs on Windows under cargo test --lib | PASS |
| Windows path stays in one file | stage plan 12.5 | OpenOptionsExt::custom_flags is in std. No new crate. Stop if Cargo.toml or tests/wf.rs must change | PASS |
| Do not skip a failed sync | Axioms.md:25 | stop if says quote the error. Do not return Ok and skip | PASS |
| Design review line by hand | t416u.md:7; t424.md:10 | overview tells the builder to add it in noticed. This pass is template 3 | PASS |
| Predecessor | 0701 return | 90.50.10.0701.05.01, the blocked w02 | PASS |
| Axioms chain | Axioms.md:5, :9 | 1.7.8,2.6.9 parses: dot order, comma split, no 3 modifier | PASS |

## 4. Where it sits in the waves

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| Shared changed file | STAGE-PLAN 11.7, 13.5, 14.1, 15.1; src at e30050dc | no planned page names src/log.rs. sync_dir is called only from append in that file | PASS |
| Independence | t422.md:7-8 | 0415 needs only 0701, which is closed. It shares no changed file with 0404. Wave 2 can be 0404 and 0415 together. Trial file tests/lab_0415.rs is not tests/lab_0404.rs, so wave 3 can hold both trials | PASS |
| Holds the file | t432.md:12 | src/log.rs stays held until tests/lab_0415.rs passes. Nothing else in the plan needs that file, so the hold blocks no one | PASS |
| Bucket | t402u.md:3 | automate. The loop already exists. This makes the existing tests finish on the machine the builders use. It is the leftover of parked page 0405, and 0405 is not reused | PASS |
| Wave count | STAGE-PLAN 15.4 | no wave added. Still 17. Section 16 of the stage plan records it | PASS |

## 5. Axioms of this draft

| Axiom | Source | Result |
|---|---|---|
| 1 Authority | Axioms.md:13 | PASS. Matthew is named as the only grantor. The draft does not say he has granted it. The commands are on hold |
| 2 Fractal | Axioms.md:15 | PASS. Unix sync stays. Only the Windows open is new |
| 4 Why | Axioms.md:19 | PASS. The why is the 0701 return's blocked w02, quoted from that file |
| 5 Frame | Axioms.md:21 | PASS. Aim, file, stop, and done-when are in the pack and on face 01 |
| 6 Lineage | Axioms.md:23 | PASS. New page. The stage plan gains a section. Old sections are not rewritten |
| 7 Missing | Axioms.md:25 | PASS. The unproven Windows flush is a stop, not a made-up success. Asked as Q15 |
| 8 Connection | Axioms.md:27 | PASS. Links are written both ways in the draft files. TENSION until Prima writes them on the real pages |
| 9 Trial | Axioms.md:29 | TENSION. This draft has not had a hostile pass from another view. The page's own trial is tests/lab_0415.rs, written after the return |

## 6. Scratch dry run

Linux box. wf built from 3646e344 (cargo build --release, finished). Scratch root, no git remote, so no remote URL was printed. grant-ref on the scratch page was the word DRYRUN, not a real grant.

| Step | Result |
|---|---|
| init-page 90.50.10.0415, grant src/log.rs | accepted. On this Linux box the current sync_dir opened the new page folder. That is the Unix path this page must keep |
| face-write 01, 08, 06 | accepted |
| draft of FINAL-PACK-0415-05.01.txt | accepted, 05.01 |
| pack 1 --branch returns | accepted. start resolved to 3646e3448985d1cf40da82b262cfd8852ae59234. branch returns. return file .workshop/returns/90.50.10.0415.05.01.md |
| verify 0415 | ok: 6 entries; views match; AGENTS.md hash 48c8d63a9d38; links 4 hold |
| face-write of the two 0701 replacement files, on a scratch 0701 | accepted. verify ok: 3 entries |
| publish-pack | not run |

Could not look: a Windows run of the open with FILE_FLAG_BACKUP_SEMANTICS. This box is Linux. The 123 failures are from the 0701 return, not re-run here.

## 7. Verdict

No FAIL. Prima can review it. Do not init the real page until Matthew grants it.

Tensions: no hostile pass of this draft yet; the Windows flush is not proven on a Windows machine (Q15); the lab back-link and the door line are texts, not yet written on the real pages.

Question for Matthew (one):

Q15. If Windows still refuses to flush the folder, what should wf do?
- Default, already in the pack: stop. Quote the error. Do not pretend the folder was synced.
- Other option: on Windows, skip the folder sync and say so in the return, so the tests pass. Linux still fsyncs the folder.
- Why: File::open on a folder is refused (os error 5). The pack tells the builder to open the folder with the Windows backup-semantics flag and then sync it. Nobody has run that flag here. Some programs skip folder sync on Windows because Windows has no exact match for a Linux folder fsync. Who gets hurt: Matthew, if a crash on Windows loses a new page log and the tests had said pass.
- Axioms: 7 (Axioms.md:25) pass for the default, the hole stays visible. 9 (Axioms.md:29) tension for the skip, the tests would go green without the crash promise. 4 (Axioms.md:19) pass either way if the return says which one happened.
