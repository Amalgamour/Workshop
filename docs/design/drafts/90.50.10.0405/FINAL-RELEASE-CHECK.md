# Release check, 90.50.10.0405 (pass 1 draft)

checked by: Cursor-C (Design)
date: 2026-11-23, 10:30 AM EST
checklist: docs/design/RELEASE-CHECK.md @ prima/build 78101fe6 (blob ef4c77486bcfddbdf8a013c6ff5651bb3df11aea)
compared: docs/spec/Axioms.md @ 78101fe6 (blob b3d891b202b231c828a091f0f0422eb22f8d6f29); docs/spec/seqAddr.md @ 78101fe6 (blob 692f0b18ad40a42ad34e66b9002736f2dcc2543f); STAGE-PLAN-90.50.10.md section 4 and section 15.4 at 78101fe6; DIRECTOR-RULINGS.md at 78101fe6
code compared: origin/returns 0e7708d3 (the 0415 return) and a823ee28 (returns head). tests/wf.rs is the same file in both.
kit compared: /tmp build of a823ee28, docs/AXIOMS.md and src/chars.rs
artifact: docs/design/drafts/90.50.10.0405/
pack sha256: 0893a08f98b7778bd4a47111fec5ba766038bb96d12ed8401b74e67c2ce358c3

Not published. Scratch dry run only. grant-ref on the scratch page was the word DRYRUN. That is not a grant.

## 1. Address

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| A1-A4, A7 | t413u.md:7, :9; seqAddr.md:14 | 90.50.10.0405: desk 90, shelf 50, book 10, page 0405 | PASS |
| A5, A6 | t413u.md:9; seqAddr.md section 10 rule 4 | job page in band 0400, not the door | PASS |
| A8, A9 | seqAddr.md:228, :242 | not 0001-0099, not PP99 | PASS |
| H1 slot | t415u.md:5; STAGE-PLAN :72; DIRECTOR-RULINGS.md:129-130 | The title is the section 4 title, "tests build and run on Windows". The address was titled in section 4, then sections 12.5 and 15.3 say "not used" so a different job would not land there. This draft is that same job, narrowed to the five failures the 0415 return left. The title is not changed | TENSION (see question 1). Not a FAIL: the title matches the first title |
| ASCII | DIRECTOR-RULINGS.md:16 | every file in this folder is bytes 0x20-0x7E plus newline. The e-acute file is named as U+00E9, not pasted | PASS |

## 2. Faces and the plan

| Item | Source file:line | Seen | Result |
|---|---|---|---|
| Done when | src/page.rs:99-110 at 0e7708d3 | three lines. They require a Windows run, the Linux meaning of the five tests, and a named branch rather than a skip | PASS |
| Face 04 goals | t245u.md:12; src/cmd.rs face 04 needs --section | FINAL-0405-face04-goals.txt, section goals. Scratch face-write accepted it | PASS |
| Lab both ways | t422.md:8; t425u.md:3; seqAddr.md:251 | face 01 and face 08 name 0701 and tests/lab_0405.rs. The lab's own faces are not replaced by this folder | TENSION until Prima writes the back-link |
| Face 06 before draft | src/cmd.rs:297-298 | FINAL-0405-face06-note.txt. It does not invent a grant ref | PASS |
| Required pack fields | src/cmd.rs:16, :365-367 | outcome, repo, start, may touch, checks, stop if, jobs w01 w02 w03 | PASS |
| may touch inside grant | src/cmd.rs:369-371 | tests/wf.rs, grant tests/wf.rs. Section 4 says tests/wf.rs only | PASS |
| Start | src/git.rs:18 | a823ee284574be3d9f6247925b9088137a27a539. Scratch resolved it | PASS |
| One check, cmd /C | src/git.rs:111; src/cmd.rs:748 | stored checks are "cargo test --test wf". No sh, seq, grep, or true in the check field | PASS |
| Template note | templates/pack.txt:19 | printed PACK.md adds "(one command each, split by ;)". The stored field is one command | PASS |
| Evidence lines | return 0e7708d3 proof; tests/wf.rs at that commit | :379 seq, :410 sh, :847 tab, :1436 ESC name, :1646 same name. File unchanged at a823ee28 | PASS |
| Linux meaning kept | the five tests | w01 keeps the seq string on Linux and the clip numbers. w02 keeps sh and the script bytes on Linux. w03 keeps tab, newline, ESC, U+202E and U+2028 on Linux. Windows is a branch, not a skip | PASS |
| Windows names | src/chars.rs:3-7; os error 123 | Tab, newline, ESC and U+2028 are not written on Windows. U+202E (Cf) and U+3164 (Hangul filler) are the replacement, because wf escapes them. If that write still returns os error 123, the pack says stop | PASS |
| Design review | t416u.md:7; t424.md:10 | start is after 0404 closed. Scratch pack recorded templates 4. The return needs the line. The pack names spec lines and kit lines | PASS |
| Axiom chain | Axioms.md:5 | 1.7.8,2.5.9 parses | PASS |

## 3. Wave in section 15.4

Section 15.4 at 78101fe6, wave 4, is 0407 and 0408. 0407 may change src/render.rs (13.5). 0408 may change src/cmd.rs, src/lib.rs, src/page.rs (13.5). This page may change tests/wf.rs only.

| Later row in 15.4 | May change | Shares tests/wf.rs |
|---|---|---|
| wave 6, 0409 and 0413 | cmd.rs, lib.rs, page.rs; render.rs | no |
| wave 8, 0406 | cmd.rs, lib.rs, page.rs, render.rs | no |
| wave 10, 0411 | cmd.rs, lib.rs | no |
| wave 12, 0412 | cmd.rs, lib.rs | no |
| wave 14, 0414 | cmd.rs, render.rs, templates | no |
| wave 16, 0498 | README.md, a walk-through | no |
| 0701 later trials | tests/lab_PPPP.rs | no |

Proposed slot: wave 4, beside 0407 and 0408. The trial tests/lab_0405.rs is wave 5, beside the 0407 and 0408 trials. No new wave. Still 17. 0404 has already closed (a823ee28) and did not change tests/wf.rs, so the file is free. Independence test: t422.md:8, neither needs the other, they change no shared files.

## 4. Axioms of this draft

| Axiom | Source | Result |
|---|---|---|
| 1 Authority | Axioms.md:13 | PASS. The draft does not say Matthew has granted it. Commands wait for his words file |
| 2 Fractal | Axioms.md:15 | PASS. Linux commands and names stay. Windows is the difference |
| 5 Frame | Axioms.md:21 | PASS. Five tests, one file, stop line, done-when |
| 6 Lineage | Axioms.md:23 | PASS. New draft. The stage plan is not edited. Sections 12.5 and 15.3 stay as written |
| 7 Missing | Axioms.md:25 | PASS. The unproven Windows names and PowerShell are a stop, not a made-up pass |
| 8 Connection | Axioms.md:27 | TENSION. Both sides are named. The lab face is not written by this folder |
| 9 Trial | Axioms.md:29 | TENSION. No hostile pass of this draft. The page's proof is a Windows run of the suite, by the builder, then the lab trial |

## 5. Scratch dry run

wf built from a823ee28 (cargo build --release, finished). Scratch root, no git remote.

| Step | Result |
|---|---|
| init-page, grant tests/wf.rs, title from section 4 | accepted |
| face-write 01, 04 goals, 08, 06 | accepted |
| draft and pack 1 --branch returns | accepted. start a823ee28. templates 4. return file .workshop/returns/90.50.10.0405.05.01.md |
| verify | ok: 7 entries; views match; AGENTS.md hash eb825a494c32; links 4 hold |
| publish-pack | not run |

Could not look: a Windows run. This box is Linux. The five failures are taken from the 0415 return, not re-run here.

## 6. Verdict

No FAIL. Prima can review the draft. Do not init the real page until Matthew grants it.

Tensions: sections 12.5 and 15.3 still say 0405 is not used; the lab back-link is not written on the real lab; no hostile pass of this draft; the Windows replacement name and PowerShell were not run here.

Questions for Prima:

1. Sections 12.5 and 15.3 park 0405 so a different job cannot reuse it. This draft uses the section 4 title for the five failures that remained. Do you want a new plan section that puts 0405 into wave 4, or should this draft stay in the folder until you say so? I did not edit the stage plan.

2. The checker may be on Linux. cargo test --test wf then passes there even if Windows would fail. The pack says the proof line must show the Windows run, and the checker judges that line. Is that the proof you want, or do you want the Windows output stored some other way?

3. The Windows commands use PowerShell, because sh and seq are not on that PATH. If cmd /C cannot find powershell, the builder stops. Is PowerShell the right host?
