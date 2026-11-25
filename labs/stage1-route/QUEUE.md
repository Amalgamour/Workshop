# Next week's packs

Proposed order for November 30 to December 4, 2026.

This is a queue for Prima. The 0409 conflict pauses the affected booking at Q1.

Each group lists paths a builder could write. Check the exact grants against live holders at pack time.

Wait for the relevant close and trial before reusing a held path. [W 29–33](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L29-L33) · [W 245–256](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L245-L256) · [G 112–116](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L112-L116)

One worker per page. One active pass per page.

Grok-Check checks one return at a time and never checks its own build.

0701 runs one trial at a time, even when trial files differ.

The return and log paths are per pass or per page. They do not add a shared file within a group. [T 5–15](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/review/DIRECTOR-WORDS-t533.md#L5-L15) · [V 160–174](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/MVP-GOAL-PROPOSAL.md#L160-L174) · [W 37–46](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L37-L46)

## Before group 1 · finish the current review

1. Prima closed 0701.05.04 passed at entry 42. That clears the tests/ hold for the helper pack.

2. Grok-Check passed 0419.05.02 at entry 20. Prima closed it passed at entry 22. Grok-Check next checks 0407.05.01 on its sealed return.

3. Prima records the dispositions. Judge the 0407 dropped-page elevation against the packed stop. Its later proof requires 0409 behavior if that case still stands. See Q1.

These are existing passes. [0701 entries 40–42](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0701/log.jsonl#L40-L42) · [0419 entries 20–22](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0419/log.jsonl#L20-L22) · [0407 entries 8–9](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0407/log.jsonl#L8-L9) · [W 37–46](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L37-L46) · [W 124–125](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L124-L125)

## Group 1 · restore the tests

| Pack | Files | Opens when |
| --- | --- | --- |
| 0423.05.03 · Grok-2 | tests/common/mod.rs, tests/wf.rs, tests/page_0408.rs, tests/lab_0404.rs | Matthew records the four-file grant. 0701.05.04 is closed passed. |

Keep this group alone. Its helper is read by older tests.

Use the live lock in the fixtures. Preserve the tests and the lock rule.

Get the full suite results and an independent check.

If Grok-2 needs tests/page_0407.rs or any fifth file, the pack stops. [W 42–46](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L42-L46) · [W 69–75](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L69-L75) · [W 145–160](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L145-L160)

## Group 2 · three new starts in free files

After group 1 closes, re-pack the work of the three unclaimed 05.01 passes below.

Refresh the start from the current head of each work branch at release time.

Use the post-helper returns head for wf and the current prima/build head for the core.

The reviewed prima/build pin is dcdab638. The future returns start will include 0423.05.03.

Confirm a supported disposition of each old pack first. Use the next legal counter and preserve the published record. See Q5. [W 59–67](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L59-L67) · [W 247–255](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L247-L255)

| Replacement work | Branch for build | Exact files in the proposed lane | Entry or rule |
| --- | --- | --- | --- |
| 0426.05.01 · golden proof | returns | tests/page_0426.rs | P0426 e8. Record the live lock steps. Matthew settles the Prime change before Prima releases it (W:65). K:7–9. |
| 0424.05.01 · book board | returns | src/board.rs, tests/page_0424.rs | P0424 e7. Show the actual lock holder, step and next. Check Grok-3's availability after the 0419 close (G:108 and W:66). |
| 0418.05.01 · core seat | prima/build | crates/seqaddr-core/src/state.rs, crates/seqaddr-core/src/resolve.rs, crates/seqaddr-core/src/validate.rs, crates/seqaddr-core/src/face.rs, crates/seqaddr-core/tests/page_0418.rs | P0418 e1,6. Re-pin and check line anchors. Retain grant ref t523 (G:102 and W:67). |

The three lanes share no listed file.

The 0418 old start c1750c32 is an ancestor of the inspected prima/build head.

The core crate diff between those tips is empty. W:67's four-file drift is unconfirmed at this pin. The re-pin still stands.

Give the 0408 trial its own slot after group 1 and before the source move.

Its only test file is tests/lab_0408.rs. Keep other test writers clear while 0701 holds the wider tests/ grant.

Run the later 0418 and other 0701 trials one at a time as their builds return.

The closed 0419.05.02 trial used tests/lab_0419.rs.

[P0408 entry 11](https://github.com/Amalgamour/Workshop/blob/a72be090d97bd51c038a919283db3f79c5f621ac/pages/90.50.10.0408/log.jsonl#L11) · [R0419 entry 17](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0419/log.jsonl#L17) · [K 89–105](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0426-plan/README.md#L89-L105) · [G 112–116](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L112-L116)

The 0404 and 0416 proof follow-ups share tests/wf.rs. Book them one at a time after group 1.

Start with evidence at the right commit. 0404 needs the independent Linux rerun and a disposition of its accepted lab.

0416 needs the Linux rerun and the Windows 99th-pass timing proof.

Only book edits if the evidence calls for a named grant. Reuse the 0423.05.03 suite evidence when the sealed criteria allow it.

[P0404 entry 22](https://github.com/Amalgamour/Workshop/blob/a72be090d97bd51c038a919283db3f79c5f621ac/pages/90.50.10.0404/log.jsonl#L22) · [P0416 entry 12](https://github.com/Amalgamour/Workshop/blob/a72be090d97bd51c038a919283db3f79c5f621ac/pages/90.50.10.0416/log.jsonl#L12) · [R0701 entry 30](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0701/log.jsonl#L30) · [G 69–71](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L69-L71)

## Group 3 · move the kernel after the golden

| Pack | Files | Opens when |
| --- | --- | --- |
| 0426 · source move | src/lib.rs, src/cmd.rs, src/cmd/, src/page.rs, src/page/, tests/page_0426.rs | The replacement golden closes. The 0408 and 0423 trials are done. The test baseline is ready. |

Refresh the golden at the move's start in its own commit.

The move keeps help, commands, exit behavior, logs and views the same.

Wait for the independent move trial on 0701, tests/lab_0426.rs.

Keep the command and page trees free. The render or book-board paths only stay available if the move still needs no edits there.

[Cited move grant and checks](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0426-plan/PACK-0426-05.02.txt#L11-L16) · [K 67–105](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0426-plan/README.md#L67-L105)

## Group 4 · book Prime and report module

| Pack | Files | Opens when |
| --- | --- | --- |
| 0425 · book Prime | tests/page_0425.rs, src/cmd/start.rs and src/page/rules/start.rs only if needed | 0426 move and trial close. Prima checks the actual module names and free grant. |
| 0422.05.01 · report module | src/report.rs, src/lib.rs, tests/page_0422_01.rs | 0705 passed. The 0408, 0423 and 0426 trials are done. Matthew records the relocated grant. |

The proposed file lists do not cross. Put 0425 first if its final grant overlaps a 0422 pass.

An open 0422 pass finishes before 0425 takes a shared file.

Keep synthetic book fixtures for 0425. Keep the manual reports for 0498. [D25 7–14](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/mvp-plan/PACK-0425-05.01.txt#L7-L14) · [A 18–27](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/review/ANSWERS-0422-PLAN.md#L18-L27) · [R22 27–33](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0422-plan/README.md#L27-L33) · [R22 157–165](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0422-plan/README.md#L157-L165) · [V 208–213](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/MVP-GOAL-PROPOSAL.md#L208-L213)

## Later groups · release only as proof lands

Use one pack and its trial for each line on the command lane.

The post-split file names below that come from the old queue are candidates. Match them to the real files and grant before booking.

The report priorities below follow R1 and R2. Q1 lists the conflicting 0409 scope statements. [G 139–165](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L139-L165) · [A 11–26](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/review/ANSWERS-0422-PLAN.md#L11-L26)

| Group | Proposed packs in that group | Files and gate |
| --- | --- | --- |
| 5a | 0422.05.02 | src/page.rs, src/page/rules/mod.rs, src/page/rules/report.rs, tests/page_0422_02.rs. After .05.01 and its trial. |
| 5b | 0422.05.03 | src/cmd/build.rs, src/cmd/check.rs, src/cmd/sync.rs, tests/page_0422_03.rs. After .05.02 and its trial. Its own trial releases the R1 hold. |
| 6 | 0409 and 0413, only if both are free | 0409 command, router and rule paths, tests/page_0409.rs. 0413 src/render.rs. 0409 needs Q1 and R1 cleared. 0413 needs 0407's render hold released. If its dropped-page proof still waits for 0409, run 0409 first. |
| 7a | 0406 | Command, router and page rules, src/render.rs, tests/page_0406.rs. After the R1 hold, the 0409 disposition and any 0413 render hold. |
| 7b | 0411 | Runner command and router paths, tests/page_0411.rs. After 0406 close and trial. |
| 7c | 0412 | Grant command and router paths, tests/page_0412.rs. After 0411 close and trial. |
| 8a | 0414 | Builder command path, src/render.rs and the confirmed prompt templates. After 0412 trial and 0404 template proof. Q4 must be settled. |
| 8b | 0417 | Return command path and src/git.rs. After 0413 passes. Wait for any quoting grant on src/git.rs. The 0419.05.02 trial uses only its lab test. |
| 9 | 0498 | README.md, docs/WALKTHROUGH.md, tests/page_0498.rs. Last, after all required proof and scope decisions. Its 0701 trial follows on tests/lab_0498.rs. |

0422 files and trials come from R22:27–33, 75–78 and 157–165.

0409 through 0412 files and order come from G:97–100 and 139–165.

0413 and 0414 come from S:1103–1174 and G:94–95, 151 and 171.

0417 and 0498 come from G:96–103 and 176–182, plus S:989 and 1223–1224.

### Work with a separate gate

- 0422.05.04 needs src/render.rs, src/status.rs and tests/page_0422_04.rs. Book it after the active render proof frees the file. Its dependent .05.05 uses docs/REPORTS.md and tests/page_0422_05.rs. These two can follow the MVP schedule if they need a shared path. [R22 27–33](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/labs/0422-plan/README.md#L27-L33) · [A 71–74](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/review/ANSWERS-0422-PLAN.md#L71-L74)
- 0420 and 0421 depend on Matthew's scope decision. If included, 0420 follows 0412 and takes the confirmed lock path. 0421 follows 0418 and takes the confirmed render and command paths. Put either in its own group until its grant proves it can share. [G 104–105](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L104-L105) · [G 167–180](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L167-L180)
- 0405 and 0410 have no pack in this queue. Their unused disposition is recorded. [S 974–989](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/design/STAGE-PLAN-90.50.10.md#L974-L989) · [G 112](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L112)
- The second-field trial follows the 0498 run. Matthew picks the field. [V 176–181](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/MVP-GOAL-PROPOSAL.md#L176-L181)
