# Lab report · X2

Builder: Codex.

Pack: X2. [Work page line 112](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L112)

## What I did

- Rated all 15 proposed tests. Two are useful, six are weak and seven are missing a case. [X2 review](../../../labs/review-draft-page/X2-REVIEW.md)
- Reviewed all eight open questions and the note about the older pinned binary. [Questions for Matthew](../../../labs/review-draft-page/X2-REVIEW.md#questions-for-matthew)
- Read the sources and traced the failure paths. This was a static review.

## Files touched

- [X2 review](../../../labs/review-draft-page/X2-REVIEW.md)
- reports/lab/review-draft-page/Codex-X2.md, this report.

## Questions for Matthew

- Q1 and Q6. What identifies a draft and keeps a dropped attempt reachable?
- Q2 and the pin gate. Which build can run a live trial and what proves that it is live?
- Q3. Who approves the exact checked candidate, and who can stop or recover the switch?
- Q4 and Q7. Does the lane rule allow overlapping files on separate branches, and who owns the freeze?
- Q5. Which branch publishes the page log and the release?
- Q8. Which commit defines a stale start, and what happens to held packs?

Full wording and evidence are in the [questions section](../../../labs/review-draft-page/X2-REVIEW.md#questions-for-matthew).

## Stop rules

The same-file test assumes a branch exception that the current lane rule does not grant. I left that exception and the log-home choice with Matthew. [Q4 and Q5](../../../labs/review-draft-page/X2-REVIEW.md#questions-for-matthew) · [Work page stop rules](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L55-L62)

The review is complete. The affected trial remains at the decision boundary.

## Sources cited in the review

The review used [returns ec78461d](https://github.com/Amalgamour/Workshop/commit/ec78461d00a9d4e0f74a188e6056043f91943eb4) and [prima/build 5d26b448](https://github.com/Amalgamour/Workshop/commit/5d26b4484067c776dfcf2e58f8255847d2385755).

- [Nov 30 brief 34–46](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L34-L46)
- [Nov 30 brief 55–73](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L55-L73)
- [Nov 30 brief 103–112](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L103-L112)
- [X1 review 1–20](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/labs/review-draft-page/X1-README-REVIEW.md#L1-L20)
- [Test plan 3–16](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L3-L16)
- [Test plan 28–38](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L28-L38)
- [Commands 385–414](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L385-L414)
- [Commands 725–736](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L725-L736)
- [Test plan 40–50](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L40-L50)
- [Commands 771–797](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L771-L797)
- [Test plan 52–61](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L52-L61)
- [Commands 362–368](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L362-L368)
- [Session rule 44–55](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/PENDING-RULES.md#L44-L55)
- [Nov 25 brief 29–33](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-25.md#L29-L33)
- [Test plan 63–73](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L63-L73)
- [Run folder 149–159](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/lib.rs#L149-L159)
- [Commands 575–584](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L575-L584)
- [Commands 771–794](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L771-L794)
- [0423 trial source 419–446](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/tests/lab_0423.rs#L419-L446)
- [Test plan 75–84](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L75-L84)
- [Pinned binary rule 22–26](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/AGENTS.md#L22-L26)
- [Nov 30 brief 26–32](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L26-L32)
- [Test plan 86–95](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L86-L95)
- [Commands 608–627](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L608-L627)
- [Commands 706–719](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L706-L719)
- [Commands 830–858](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L830-L858)
- [Test plan 40–61](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L40-L61)
- [Test plan 101–111](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L101-L111)
- [Test plan 218–222](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L218-L222)
- [Git source 22–24](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/git.rs#L22-L24)
- [Test plan 113–124](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L113-L124)
- [Split recipe 1–13](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/labs/0426-plan/tools/split_cmd.py#L1-L13)
- [Split recipe 88–96](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/labs/0426-plan/tools/split_cmd.py#L88-L96)
- [0426 move draft 8–12](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/labs/0426-plan/PACK-0426-05.02.txt#L8-L12)
- [Test plan 126–135](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L126-L135)
- [Commands 971–982](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L971-L982)
- [Draft design 138–169](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/README.md#L138-L169)
- [Test plan 137–147](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L137-L147)
- [Commands 277–299](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L277-L299)
- [Commands 329–338](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L329-L338)
- [Pass state 223–229](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/page.rs#L223-L229)
- [Pass state 533–536](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/page.rs#L533-L536)
- [Nov 30 brief 165](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L165)
- [Nov 25 brief 63–66](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-25.md#L63-L66)
- [Test plan 149–159](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L149-L159)
- [Pass state 101–105](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/page.rs#L101-L105)
- [Commands 344–359](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L344-L359)
- [Commands 1069–1076](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L1069-L1076)
- [Draft design 138–142](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/README.md#L138-L142)
- [Test plan 161–169](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L161-L169)
- [Commands 830–877](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L830-L877)
- [Log source 68–99](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/log.rs#L68-L99)
- [Test plan 175–186](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L175-L186)
- [Commands 949–960](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L949-L960)
- [Commands 1069–1095](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L1069-L1095)
- [Manual return 67–81](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/MANUAL-RETURN.md#L67-L81)
- [Test plan 188–198](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L188-L198)
- [Commands 441–468](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L441-L468)
- [Session rule 48–55](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/PENDING-RULES.md#L48-L55)
- [Test plan 204–214](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L204-L214)
- [0426 move draft 8–16](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/labs/0426-plan/PACK-0426-05.02.txt#L8-L16)
- [Nov 30 brief 114](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L114)
- [Done-when review 49–57](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L49-L57)
- [Test plan 9–16](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L9-L16)
- [0423 check report 24–29](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/reports/90.50.10.0701/05.04/Grok-Check-check-20261125-1157.md#L24-L29)
- [Done-when review 49–53](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L49-L53)
- [Claude questions 10–25](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L10-L25)
- [Draft design 198–202](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/README.md#L198-L202)
- [Claude questions 29–42](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L29-L42)
- [Nov 30 brief 145–148](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L145-L148)
- [Catch log 36](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/quality/CATCH-LOG.md#L36)
- [Test plan 218–221](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/TEST-PLAN.md#L218-L221)
- [Claude questions 46–57](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L46-L57)
- [Draft design 158–169](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/README.md#L158-L169)
- [Claude questions 61–69](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L61-L69)
- [Nov 30 brief 152–155](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L152-L155)
- [Claude questions 73–85](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L73-L85)
- [Nov 30 brief 150–155](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L150-L155)
- [Claude questions 89–98](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L89-L98)
- [Draft design 194–205](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/README.md#L194-L205)
- [Commands 242–255](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L242-L255)
- [Claude questions 102–109](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L102-L109)
- [Claude questions 113–119](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L113-L119)
- [Commands 375–391](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/src/cmd.rs#L375-L391)
- [Claude questions 123–127](https://github.com/Amalgamour/Workshop/blob/314784b815a39eece12de8c42415543ad9a4f5b2/labs/draft-page/QUESTIONS.md#L123-L127)
