# Lab report · X6

Builder: Codex.

Pack: X6. [Nov 30 brief 103–116](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L103-L116)

## What I did

- Read the released 0418 pack and its six-entry log on packs. Checked the start's ancestry, the five granted paths and the four cited source anchors. [Packed start c1750c32](https://github.com/Amalgamour/Workshop/commit/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc) · [Compared prima/build tip 5d26b448](https://github.com/Amalgamour/Workshop/commit/5d26b4484067c776dfcf2e58f8255847d2385755) · [0418 pack 7–18](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L7-L18) · [0418 log 1–6](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/log.jsonl#L1-L6)
- Found that the 05.00 requirement conflicts with R9 and that the crate's existing tail test expects a plain 05 refusal. The pack stays held as written. [SeqAddr fix proposal 61–81](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L61-L81) · [addr.rs 834–839](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/addr.rs#L834-L839) · [tails.rs 212–217](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/tests/tails.rs#L212-L217)
- Checked the written acceptance lines against w02. A missing new test file can slip through the literal acceptance lines even though the job requires it. [0418 pack 16–26](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L16-L26) · [Done-when review 44–47](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L44-L47) · [Done-when review 60–63](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L60-L63)
- Recorded DW10. Builder evidence comes from Windows. The checker runs on the box, and the box run decides. [Done-when review 84–87](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L84-L87) · [Nov 30 brief 116](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L116)

## Files touched

- [X6 note](../../../labs/stage1-route/packs/X6-0418-NOTE.md)
- reports/lab/stage1-route/Codex-X6.md, this report.

## Questions for Matthew

- Where does the 05 pass board read from once plain 05 is the seat? May the 06 wording describe the derived notes without 06.00?
- Which existing tests or parser paths may be granted if a later pack needs them?
- How should the held pack and cited spec be handled in order?

[Questions and evidence](../../../labs/stage1-route/packs/X6-0418-NOTE.md#questions-for-matthew)

## Stop rule

The H3 rule conflict stops release and build work on 0418. The existing-test conflict also reaches outside the current grant. I stopped at the evidence note and left both decisions open. This was a static review. [Nov 30 brief 55–71](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L55-L71) · [0418 pack 17–26](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L17-L26) · [SeqAddr fix proposal 69–81](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L69-L81)

## Sources cited

Evidence pins are [packs c697e035](https://github.com/Amalgamour/Workshop/commit/c697e0353c34e41a46ebf029f7b417479e5485fa), [Compared prima/build tip 5d26b448](https://github.com/Amalgamour/Workshop/commit/5d26b4484067c776dfcf2e58f8255847d2385755), [Packed start c1750c32](https://github.com/Amalgamour/Workshop/commit/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc), and [returns bc38979b](https://github.com/Amalgamour/Workshop/commit/bc38979b92cb81ba3d2eaf1e6df1c138a4520663).

- [0418 pack 16–26](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L16-L26)
- [SeqAddr fix proposal 61–81](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L61-L81)
- [tails.rs 212–217](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/tests/tails.rs#L212-L217)
- [0418 log 1–6](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/log.jsonl#L1-L6)
- [0418 pack 7–14](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L7-L14)
- [Core run 3–12](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/docs/plan/CORE-RUN.md#L3-L12)
- [Nov 30 brief 26–30](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L26-L30)
- [0418 pack 14–18](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L14-L18)
- [state.rs 458–462](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/state.rs#L458-L462)
- [resolve.rs 179–199](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/resolve.rs#L179-L199)
- [validate.rs 340–354](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/validate.rs#L340-L354)
- [face.rs 82–85](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/face.rs#L82-L85)
- [0418 pack 16–23](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L16-L23)
- [0418 face 01 6–10](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/01.md#L6-L10)
- [addr.rs 834–839](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/addr.rs#L834-L839)
- [resolve_validate.rs 136–148](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/tests/resolve_validate.rs#L136-L148)
- [0418 pack 21–24](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L21-L24)
- [SeqAddr fix proposal 34–49](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L34-L49)
- [resolve.rs 179–188](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/src/resolve.rs#L179-L188)
- [grammar.rs 283–288](https://github.com/Amalgamour/Workshop/blob/c1750c32c3fb837deb34a5b9c3cafc77c1086dfc/crates/seqaddr-core/tests/grammar.rs#L283-L288)
- [Done-when review 44–47](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L44-L47)
- [0418 pack 17–25](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L17-L25)
- [Done-when review 60–63](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L60-L63)
- [SeqAddr spec 196–206](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/spec/seqAddr.md#L196-L206)
- [Seated 05 draft 50–60](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/design/drafts/SEATED-05-PROPOSAL.md#L50-L60)
- [SeqAddr fix proposal 69–81](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L69-L81)
- [0418 pack 20–25](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L20-L25)
- [Done-when review 84–87](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-DONE-WHEN.md#L84-L87)
- [Nov 30 brief 116](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L116)
- [0418 pack 17–26](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L17-L26)
- [SeqAddr fix proposal 8–11](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/FIRE-SALE-2026-11-26-SEQADDR-SPEC-FIX-PROPOSAL.md#L8-L11)
- [Pending rules 1–9](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/review/PENDING-RULES.md#L1-L9)
- [Nov 30 brief 165](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L165)
- [Nov 30 brief 103–116](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L103-L116)
- [0418 pack 7–18](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0418/05.01/PACK.md#L7-L18)
- [Nov 30 brief 55–71](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L55-L71)
