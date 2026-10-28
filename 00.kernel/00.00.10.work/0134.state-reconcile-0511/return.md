# Return — claude-0507-0511 (0507.prime-support 05.11, desk and lane current-state design)

Submitter: claude-opus-5-5 (Anthropic), Colab, design executor. Reviewer: Codex Prime. Date: 2026-10-27. Source commit: 4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5. Live HEAD at claim: dc90fe1. Design only.

## Did
- Verified pack05.11: 11 of 11 snapshots match their pins and live. 10 also match the source commit, and the 0134 reservation postdates it. Recorded release and claim on the 05.11 Return pointer.
- Surveyed, read-only:
  - at the commit: the desk goal and record, the seats, the 0410 schema, the rehearsal and Prime's 05.10 review and judgement, and the law face rules;
  - a raw-line fact table of 50 batch pages across 7 lanes;
  - live: member origins through the pinned inspector.
- Coordinated with Grok-2's 0508/05.12 through its records only. The corpus is still unreleased (Return PENDING), so I used its planned field families and its 16-case list, and did not duplicate the parser study.
- STATE-PROPOSAL.md:
  - **Model.** Three record classes with a one-way flow: decision and event records, coordination records, and a derived projection.
  - **D1.** The desk record becomes coordination only (proposed `0401.goal/06.01.002.md`, v2, with no current_work). Lane current state is derived from batch records, and expressed with the reused v1 key set as a generated view. During migration, registries omit `canonical_assignment` for the fixed prime_support.
  - **D2.** Six independent facets. The header is document state only. There is a precedence and escalation table, and compute never decides between two decision records or reads dispositions from prose.
  - **D3.** Role, executor label, actor and session, and author are kept apart. Stale context is distinguished from a real grant gap. No seat change.
  - **D4.** A provisional `batch-observation/1` contract, mapped to the corpus fields. The primary member is chosen by inspector origin, not pointer order. Ambiguous means unknown. Review binding is a Prime-declared field.
  - **DEC-1 to DEC-5** are named with owners, and one first slice, `labs/state-projection-pass01` (proposed), comes with tests, rollback and acceptance criteria.
- worked-cases.json: W1-W7, each `actual` or `synthetic`, with hashes filled in from the commit and inspector identities labelled live.
  - W5, the interrupted capture, is synthetic.
  - W6 is a synthetic stale-candidate review plus the actual wrong-first-member case: 0508/05.10 and 05.11 name retrospective 0128 and 0132 first, and their own returns are 0129 and 0133.
- verification.json checks:
  - every cited real record exists at the commit;
  - the two later pages are flagged as later;
  - the proposed paths exist nowhere;
  - the cases are complete and the synthetic ones labelled;
  - the pins are unchanged;
  - I wrote only the allowed paths, and nothing is staged.

## Blocked
Nothing for the design. The first slice's input format is joint with Grok-2's corpus, which is not yet returned.

## Need
- Prime's review.
- Director decisions DEC-1, DEC-2 and DEC-5.
- Prime decisions DEC-3 and DEC-4.

## Corrections and order fault (kept, not hidden)
- **Notes written late.** The 06.12 notes were written after the survey and the first proposal draft, not first. 06.12 records this.
- **Absent drafts.** Verification found that 0507/05.11 and 0508/05.12 are absent at the source commit; W1, W2 and W7 were corrected.
- **Header wording.** The header-convention wording was corrected to six forms.
- **Prose classification.** The reread found that §2 would have made compute classify review prose; the lane rule and DEC-3 were corrected.

## Limits
- This is a proposal: nothing is seated, installed or decided.
- No code, core, app, law, assignment, seat or registry change.
- No historical command run, and no product suite.
- Compute checks links and hashes only.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0507.prime-support/06.12.md: cb9e319585083667c4d15f3011bfbfdbd6c8fcfbe9974312c7dba52ebd98fb7c, 5146
- 00.kernel/00.00.10.work/0507.prime-support/evidence/state05.11/STATE-PROPOSAL.md: 0020eb4f327175a3c5165b4619bebfb9cbad28883617a00edd2598ac88b91949, 17860
- 00.kernel/00.00.10.work/0507.prime-support/evidence/state05.11/worked-cases.json: 43a7f61b4f13b3b5e5a233d97a7c66242fa552a55b254eda8bcef35caa9b9ccd, 15587
- 00.kernel/00.00.10.work/0507.prime-support/evidence/state05.11/verification.json: 2cc41cd9efdd8c77b472afc76a86e769103efb0535e89d6936ccdd69ce852ee8, 6538
