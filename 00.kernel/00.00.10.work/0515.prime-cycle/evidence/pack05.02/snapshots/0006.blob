# PRIME-USE — current Prime's first real use of the cycle

For Codex Prime, after you review the build. These are the minimal, exact steps for one real bounded read-record-read on one work page. The same implementation writes real review records; it isn't a fixture-only writer. Everything below is a proposal for your use. Nothing has been recorded on any live page.

## 0. Choose the work and its output places (your decision)

- **One work:** a page, its pass, and its captured member.
- **The page goal.** This is your source-bound statement, which you write. A changed statement is a new goal.
- **The review location.** It must be work-local, under that lane's `evidence/`. Proposed: `00.kernel/00.00.10.work/<lane>/evidence/prime-cycle-reviews/<pass>/`. Each review becomes `<review_id>/record.json`, `REVIEW.md` and `COMMITTED.json`. Nothing else in the lane is touched.
- **An `output_root` outside the repository**, for templates and packets. For example `D:\prime-cycle-out\`.

## 1. Registration (example for 0508.return-capture/05.20, member 0169)

Save as `D:\prime-cycle-out\reg-0520.json`. The commit is the published source you are reviewing. Fill the agreement with your own words; null means unknown, and prime_review will flag it.

```json
{"schema": "prime-cycle-registration/1", "repository": "D:/Git/lib-build", "book": "00.kernel/00.00.10.work",
 "book_label": "00.00.10.work", "source": {"kind": "git-blob", "commit": "<40-hex published commit>"},
 "members_book": "D:/Git/lib-build/00.kernel/00.00.10.work", "output_root": "D:/prime-cycle-out",
 "bounds": {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152},
 "works": [{"work_id": "deskstate-0520", "page": "00.kernel/00.00.10.work/0508.return-capture/05.20.md", "pass": "05.20",
            "member": "0169.desk-state-preservation-0520",
            "goal": {"goal_id": "<your goal id>", "statement": "<your page-goal statement>"},
            "agreement": {"goal": "<…>", "scope": "<…>", "prime_discretion": "<…>", "director_required": "<…>",
                          "finish_criteria": [{"id": "<id>", "text": "<…>"}], "recorded_decisions": [{"id": "<id>", "text": "<…>", "source_sha256": "<64 hex>"}]},
            "review_location": "00.kernel/00.00.10.work/0508.return-capture/evidence/prime-cycle-reviews/05.20"}]}
```

## 2. Read, and get the template

```text
python -B labs/prime-cycle-pass01/prime_cycle.py read --registration D:\prime-cycle-out\reg-0520.json
python -B labs/prime-cycle-pass01/prime_cycle.py read --registration D:\prime-cycle-out\reg-0520.json --templates D:\prime-cycle-out\t1
```

**Expected on 0169 today** (the builder's read-only preview at 4d8bc1c gave exactly this):
- `pass state: awaiting-review`, custody 0169 `primary-current-candidate`, receipt `94a5fe21…`;
- `! legacy-review-unmapped`. Your existing prose review on 05.20 is shown, but not typed;
- exit 1.

The template is `t1\template-deskstate-0520.json`. Its `binding` is pre-filled: page sha, member, receipt, origin, goal hash, expected prior and fingerprint. Don't edit it.

## 3. Fill only the judgment

Fill `attribution.actor_label`, and `judgment`:
- **Typed fields:** `outcome` (continue, director-input, develop or complete), `disposition` (accepted, held or correction-required), `pass_terminal` (finished or open), and `goal.terminal` (open or completed; with evidence when completed).
- **Prose:** `finding`, `reasons`, `source_refs`, `next_action` (`{action_id, text, authorized_in_grant}` or null), and `unresolved`.
- **Flags:** `semantic_conflict` (true, false or null).
- **The sections your outcome needs:**
  - continue: return_result, prime_finding, within_direction and next_bounded_action;
  - complete: outcome_evidence, limits, tests_note, learning, preservation, remaining_choices, findings_account and finish_assessments;
  - director-input: issue, consequences, options, recommendation, question and affected, plus a matching `holds` entry.

**Minimal counts, from the preview:**
- 14 supplied fields for a continue with accepted, pass finished and goal open;
- 18 for a goal completion;
- 15 for a Director hold.
Every hash, member and coordination field is already filled.

To **adopt** your earlier prose review, record it as this first typed review, with its reasons and source_refs pointing at `evidence/prime-review05.20/REVIEW.md`. Nothing adopts it automatically.

## 4. Record, then read again

```text
python -B labs/prime-cycle-pass01/prime_cycle.py record --registration D:\prime-cycle-out\reg-0520.json --decision D:\prime-cycle-out\t1\template-deskstate-0520.json
python -B labs/prime-cycle-pass01/prime_cycle.py read --registration D:\prime-cycle-out\reg-0520.json
```

**Expected:**
- record exits 0, or 1 when prime_review shows a hold or attention, and prints the review directory;
- the next read shows `pass state: reviewed`, with your disposition, pass terminal and goal terminal, your next action labelled with you as author and its record.json source, and no awaiting-review.

You maintain no coordination array, acceptance list or `00.live`.

**Refusals you may see** (exit 2; nothing is written):
- "source changed since read …": the page or receipt moved; read again;
- "expected_prior …": another review landed first;
- "conflict": the same review_id with different content; use a new review_id, and keep `supersedes` from a fresh template;
- terminal-rule refusals: for example, a goal completion without evidence, or while held.

**Interrupted write** (exit 3): `inspect --work deskstate-0520` shows the partial. Never edit or delete it. Record again under a new `review_id`, with `recovers` set to the partial's id.

## Limits

- The tool records your supplied judgment. It authenticates no one and grants nothing.
- Custody is not acceptance.
- Read never elects work. A recorded next action is your text, shown with its author.
