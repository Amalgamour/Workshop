# Notes — provider text watermarking review (Colab, research only)
Date: 2026-10-31. Reviewer: claude-opus-5-5 (Anthropic), acting as an independent Colab reviewer, in a long continuing workshop session.
State: written before REPORT.md. Research and assessment only; no runtime code, settings or build artifacts were changed.

## Disclosure and limits of this reviewer
- I am a Claude model, and the subject is my own provider's watermark. That is a conflict of interest; I state evidence and its source, and mark provider claims as provider claims.
- I cannot see the deployed sampler, the watermark key or parameters, or whether any of my historical responses were marked. Nothing I say about my own outputs is evidence of their marking. Introspection gives no access to this.
- I recalled some facts about the 2024 Nature paper from training. Where I could not re-read them this session they are marked "recalled, not re-verified".

## Checkpoint
- The previous build (0518.colab-review 05.01) was already complete before this request: captured in 0179, freshly verified, pointer appended.
- Nothing was in flight, and nothing was resumed or changed.
- Workshop HEAD at review: 960d20c5290656095df8457b1740d2d5e586b111.

## Sources read (2026-10-31, through the web fetch tool; the text is as rendered by that tool)

| # | source | what was obtained | version |
|---|---|---|---|
| S1 | https://www.anthropic.com/news/claude-text-watermark | full article | published 2026-08-14, updated 2026-09-01 (detection API) |
| S2 | https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content | full article | "Updated this week" (no date shown) |
| S3 | https://github.com/google-deepmind/synthid-text | README | repo HEAD `9c055d932e042b75197e337371448a120bbc65bb` (`git ls-remote`, 2026-10-31); 43 commits shown |
| S4 | https://github.com/google-deepmind/synthid-text/blob/main/docs/tournament.md | full document | byline date 2026-10-09; at HEAD above |
| S5 | https://www.nature.com/articles/s41586-024-08025-4 | **blocked** | Nature redirected to a login; the PMC copy showed a CAPTCHA; a reader mirror returned 403 |
| S5b | bibliographic records found by search (Nature Index, RePEc) | title, DOI, venue | Nature 634, 818–823, online 2024-10-23. Dathathri is listed first in RePEc; another listing differs on author order (unresolved) |
| S6 | https://docs.x.ai/developers/advanced-api-usage/watermarking | full page | no date shown; states default-on from 2026-11-07 |
| S7 | the user-supplied screenshot of Anthropic's email "Text watermarking is coming to more Claude models" | top portion only | a November 3, 2026 rollout to Mythos 5, Opus 4.7, Opus 4.6 and Sonnet 4.6; Bedrock may lag. "You don't need to change anything unless you rely on the watermark for your own compliance and use non-default sampling settings (see below)." **The "below" part was not supplied.** |
| S8 | platform.claude.com Messages API reference | partial | the page is 1.3 M characters; the first 100 k characters show no watermark and no sampling parameters; the rest not read |
| S9 | secondary sources on sampling parameters (OpenRouter migration guide, DEV posts, Bedrock model card snippet) | snippets | they conflict: on Opus 4.7+, temperature, top_p and top_k are "ignored" (OpenRouter) or "a 400 error" (DEV post). Not Anthropic primary text. |

Not done:
- no paid calls, installs, model launches or detection requests;
- no watermark-removal tools;
- the Nature full text was not read (blocked);
- the email's "see below" section was not seen.

## Working observations
O1. **The mechanism (S4).**
- g-values come from hashing the secret key with the last `context_len` tokens (default 4) plus the candidate.
- The next-token distribution is truncated to top-k (default 40) and renormalised, then reweighted per layer (depth default 15).
- The token is sampled from the result.
- "Watermarking is the last step before sampling." The raw logits are untouched; the processed distribution and the final choice are changed.
O2. **Non-distortion (S4).** It holds "if you sample `key` at random". It is exact only for records shorter than about `context_history_size` (1024) contexts. Repeated-context masking is "essential". With many layers the output is "close to deterministic for a fixed key". A fixed key can inflate false positives through shared n-grams.
O3. **Anthropic (S1).**
- "a version of the SynthID-Text approach"; the parameters are not published.
- Exact outputs are not watermarked; code is watermarked less, and comments can be.
- Factual passages are sparse.
- Detection says Claude was "likely involved"; it is weak on short text; light editing leaves the mark partly; translation carries it.
- No opt-out is mentioned.
O4. **Grok (S6).**
- On by default from 2026-11-07 for the listed models.
- Team-admin opt-out per model, some locked on; an `x-watermark` header reports it.
- It covers structured outputs and tool-call arguments.
O5. **Claude controls.**
- No opt-out is documented in S1 or S2.
- S7 links compliance reliance to non-default sampling settings without the detail.
- I must not infer that sampling changes disable or weaken the watermark.
O6. **Workshop practice relevant here.**
- Exact bytes are carried by files, snapshots, captures and sha256, never by a model retyping them.
- **One gap:** the Director's chat wording is typed into return-pointer "Release" lines by the executing model, from the prompt, with no on-disk source to hash against. That is a transcription risk with or without a watermark.
