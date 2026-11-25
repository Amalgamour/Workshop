# Questions for Matthew

Defaults are proposals. The affected packs wait for Matthew's answer.

Q1 is a rule conflict under the [work-page stop rule](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L223-L230).

## Q1. 0409 and the route to 0498

The stage plan lists 0409 as a 0498 prerequisite.

R1 says retire-a-page is outside the MVP, but still books 0422 ahead of 0409 and the shared command pages.

0407 also raised that its dropped-page test needs 0409.

The choice changes both the route and the 0407 proof.

[Stage plan lines 1003–1010](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/design/STAGE-PLAN-90.50.10.md#L1003-L1010) · [R1 lines 11–16](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/review/ANSWERS-0422-PLAN.md#L11-L16) · [0407 entry 9](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0407/log.jsonl#L9)

- **A · Default.** Keep 0409 on the route. Keep R1's file order. Prove dropped-page behavior before completing the 0407 trial.
- **B.** Move 0409 after 0498. Record which dropped-page proof 0407 and 0498 may defer. State whether R1 still holds 0406, 0411 and 0412.

## Q2. 0420 dead lock

The queue suggests a dead-lock recovery pass.

0423 already has a recorded override path. Its independent trial is closed passed.

[Queue lines 99–105](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L99-L105) · [0701 entries 40–42](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0701/log.jsonl#L40-L42)

- **A · Default.** Keep 0420 after 0498. Show the existing override in the walkthrough when it fits.
- **B.** Make 0420 a prerequisite. Name the dead-lock case the current override cannot handle. Name the lock and test paths after 0412.

## Q3. 0421 wf seat

The core seat is 0418. The suggested wf follow-up is 0421.

The answered MVP asks for one recorded seqaddr validate step.

[Queue lines 101–105](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L101-L105) · [MVP G1 and G2](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/MVP-GOAL-PROPOSAL.md#L143-L158)

- **A · Default.** Keep 0421 after 0498. Use the existing wf and the recorded core validation.
- **B.** Require 0421 before 0498. Name the wf view or face 01 behavior the walkthrough must prove. Schedule it after 0418.

## Q4. 0414 builder name rule

The stage plan names template v4 and refuses names outside its list.

The builder queue names v5 and gives an unfamiliar name a stable temporary worker.

Which behavior should a new pack enforce?

[Stage plan lines 1148–1164](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/design/STAGE-PLAN-90.50.10.md#L1148-L1164) · [Queue lines 93–96](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/GROK-BUILDER-QUEUE.md#L93-L96)

- **A · Default.** Use the v5 proposal for new packs. Prove that old packs still render the same. State the rule for a different claimant.
- **B.** Use the recorded allow-list rule. Name the template paths and prove the published pack bytes stay stable.

## Q5. replacing the three unclaimed packs

The work page calls for re-packing after 0423.05.03.

The pinned a823 build has no withdraw command. The returns source has it.

The old 0426 pack was released by Claude. The brief calls for Matthew's Prime decision before Prima releases its replacement.

[Work page lines 59–67](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/WORK-PAGE-2026-11-25.md#L59-L67) · [Withdraw source lines 459–469](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/src/cmd.rs#L459-L469) · [0426 entries 1–8](https://github.com/Amalgamour/Workshop/blob/a72be090d97bd51c038a919283db3f79c5f621ac/pages/90.50.10.0426/log.jsonl#L1-L8) · [Axiom 6](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/docs/AXIOMS.md#L25)

- **A · Default.** Approve a compatible pinned build and the 0426 Prime decision. Have the authorized Prime record each withdrawal and use the next legal counter.
- **B.** Keep the three passes held until an authorized path is approved. Keep the published pack bytes and counters as they stand.

## Q6. board column words

The MVP requires holder, step and next. The column words are a separate open design choice.

[MVP G5](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/plan/MVP-GOAL-PROPOSAL.md#L183-L191) · [Board design lines 132–136](https://github.com/Amalgamour/Workshop/blob/dcdab638529ea388d28e8222ba1dbcdd1cdda726/docs/design/WF-BOARD.md#L132-L136)

- **A · Default.** Keep the existing tool words in the columns. Use body-shop words as side labels.
- **B.** Choose a new column vocabulary. Decide it in a separate design change so the 0424 proof stays small.
