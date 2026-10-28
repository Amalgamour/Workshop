# Diagnosis — return-shape corpus for the state design

Date: 2026-10-27. Recorder: Grok Builder 2. This is a recommendation for the next design slice. It is not a parser change and it is not an acceptance.

Corpus: `evidence/corpus05.12/corpus.json`, schema `return-shape-corpus/1`, SHA-256 `591721b62f2bedafc2255e1638c64fa6642585b822defaf5c65253ea376e0b53`, 441202 bytes. Source commit `4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5`. Parser `labs/prime-support-pass01/prime_support.py` SHA-256 `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70`. The stored observations come from `parse_source(data, "page-return")` on the commit bytes.

## Observed parser behavior

Fourteen of the sixteen pages are `unsupported` with reason `ambiguous heading` at the first return-family title outside the closed set. Two pages are `ok` with `execution` `unknown`. None of the sixteen is `no-return`.

The closed titles are `Return`, `Return — …`, `Review`, and `Review — …`, at heading level 2, outside fences. These observed titles are outside that set:

- `Return pointer` on ten pages. `0508.return-capture/05.11` puts two members under that singular heading. The count of members is in the body, which this failure never reads.
- `Return pointers` on `0508.return-capture/05.09` and `05.10`.
- `Return archive pointer — 2026-10-27` after a recognized `Return — …` section on `0507.prime-support/05.01` and `0504.app-entry/05.06`. The earlier recognized section does not survive. The call stops at the later heading and stores no revision id.

On the two `ok` pages the first return line is `Execution: RETURNED` or `Execution state: RETURNED`. That is not the token `execution:` plus `claimed`, `running`, `returned`, or `stopped`. The parser records `unknown`. It does not case-fold the prose. That matches the rule that status does not parse prose.

Fenced return text is skipped. The sixteen real pages have no fenced return or review heading. Synthetic S1 puts `## Return` and `execution: returned` in a fence and `## Return pointer` outside it. The observation is the outside ambiguous heading. The fenced token is not the result.

## Verified custody facts

Every live page equals its commit blob. Nineteen members named by those pages were read with the pinned inspector. All nineteen are live status `complete`. Each member's `receipt.json` blob at the corpus commit equals the live receipt. That is package presence at this commit. It is not a claim that the capture's own `source_commit` field equals `4cca1d2e`. Several manifests name an earlier checkpoint: `e6d6eb755387` for `0102` and `0101`, and `75ae515d8264` for the historical captures from the return-capture jobs.

Roles, from reservation origin plus the retrospective flag:

- Primary current submission, origin is this page and retrospective is false: `0107`, `0111`, `0123`, `0126`, `0131`, `0117`, `0127`, `0120`, `0121`, `0125`, `0129`, `0133`.
- Retrospective custody of this same page: `0102.prime-support-0501`, `0101.app-entry-0506`.
- Secondary historical capture, different origin, retrospective true: `0124`, `0128`, `0132`.
- Named in the assignment and absent from the return heading: `0118` and `0119` on `0508.return-capture/05.07`. The pointer names only `0120`. The review prose mentions the historical pages and the separate report. Those are different texts.
- `0504.app-entry/05.01` mentions `0101.present` and `0199.gap` as book inventory faces. They are not capture pointers and were not inspected as members.
- `0502.workflow-start/05.01` names no 0101–0199 capture.

`0504.app-entry/05.01` is `ok`. Its review line `Reviewed return SHA-256: 8ac327e236f10315b27646a4328d9322d39f463720f37bc3c53cbbba055f269b` is stored as `legacy_whole`. That value equals neither the current whole file nor the current revision id. `0502.workflow-start/05.01` contains `2cf4fd147bc4bcacb77585d11311ae6c57a4e031b40ede4d0f19a353af1e3816` in a different sentence, so the parser does not extract it. It also equals neither current whole nor current revision id. Which earlier bytes those hashes name was not searched. The binding stays unknown.

Review sentences such as `Accepted within scope` are source text. On an unsupported parse there is no review object. A receipt hash is custody identity. It is not a review and it is not approval.

## Synthetic controls

These are labelled examples. They are not desk history.

- S1. Fenced `## Return` is ignored. The outside `## Return pointer` is ambiguous heading line 6.
- S2. Two `## Return — primary` headings with different receipts: `duplicate heading`. The parser does not keep the first block.
- S3. One recognized heading whose body names two receipts: status `ok`, execution `unknown`. The conflict is invisible to `parse_source`.
- S4. `execution: returned` plus a member that was not created. Parser status `ok`. Inspector on the real book: status `missing`, exit 1.
- S5. A disposable book outside the desk, with `return.md` and no reservation or receipt. Inspector status `incomplete`, exit 2, problem `missing reservation.json`.
- S6. Receipt hash, `Reviewed return SHA-256`, and revision id are three different values. The disposition line is a recorded sentence, not an acceptance.

## One next slice

Design a read-only projection in `0507.prime-support/05.11`. Do not change `prime_support.py`. Do not rewrite these sixteen pages. Do not treat this diagnosis as the implementation.

The projection has two channels:

1. Observation. Recompute `parse_source` with the pinned file and keep its status, reason, revision id, execution, and review object exactly.
2. Pointer reading. Outside fences, inventory the three heading forms this corpus actually contains, plus the recognized `Return — …` form. For `Return pointer`, `Return pointers`, and `Return archive pointer — date`, list every `Member` and `Receipt` block in order. Do not require those headings to pass the current grammar before they can be listed.

Role rule, applied only to members named by that reading or by an assignment sentence of the form `NNNN.name captures`:

- Origin book, page, and batch equal this page, and retrospective is false: primary current submission.
- Origin matches and retrospective is true: retrospective custody of this same page.
- Origin differs and retrospective is true: secondary historical capture produced by the job.
- Named only in the assignment: not part of the pointer list.
- Inspector `missing` or `incomplete` stays that status. Do not allocate a substitute.

Review rule: copy the parser review object when the observation is `ok`. Otherwise keep the review section as text. Do not promote `Accepted`, `Disposition`, or a receipt into a bound judgement. Compare a `Reviewed return SHA-256` value to the current whole and the current revision id. A mismatch stays unbound unless a later slice verifies the bytes it names.

Input contract for that design page:

- Read this corpus and this diagnosis. Reproduce each stored observation before proposing behavior.
- Expectations in the corpus are proposals. They are not current tool results.
- Worked examples are C01, C07, C11, C13, C15, C16, and S1 through S6.
- The design may specify the projection. It may not patch the parser or the pages in that same pass.
- A returned receipt remains custody, not approval, acceptance, seating, or publication.

## Unresolved

Whether pages should grow the `execution:` token, or the reader should learn the pointer headings, remains the rehearsal's D4 choice. This corpus does not choose it.

Whether a later archive pointer should preserve the revision id of the earlier recognized return is a proposed rule. Current behavior discards it.

Whether `05.07`'s pointer should also name `0118` and `0119` is a page-form question. Today the pointer names `0120` only.

The two unbound review hashes are not resolved to an older blob in this pass.

This corpus covers the sixteen named pages and six synthetic controls. It does not say that every other return in the repository has been classified.
