# Premise check — is any Claude model unwatermarked before 2026-11-03?
Date: 2026-10-31. Reviewer: claude-opus-5-5 (Anthropic), acting as Colab reviewer. Research only.
Request: the Director's "Confirm premise first", the answer to REPORT.md §6.
State: a new file beside REPORT.md. REPORT.md and NOTES.md are unchanged.

## The premise under test
REPORT.md §6 proposes an on/off comparison. Its premise: until 2026-11-03, Opus 4.6 and/or Sonnet 4.6 produce **unwatermarked** text. The source is S7, the user's email screenshot: "Text watermarking is coming to more Claude models", rolling out on November 3, 2026 to Mythos 5, Opus 4.7, Opus 4.6 and Sonnet 4.6.

## What was checked (2026-10-31, web fetch and search only)
| # | source | finding on the premise |
|---|---|---|
| P1 | S2, support article 16266773, model table (refetched) | Opus 4.6 and Sonnet 4.6 each show a single "✅\*". The fetch tool could not say which column the mark sits in, and the page gives no dates. The page says Anthropic "is adding watermarks to outputs from models released before August 2, 2026". The table may show planned coverage. **It neither confirms nor refutes the current state.** |
| P2 | S1, anthropic.com/news/claude-text-watermark (refetched) | It names no model and no date. It says future models "will generate text that contains a watermark", and that models launched before 2026-08-02 have an EU transition period, with the rollout "over the coming months". The 2026-09-01 update concerns only the detection API. **Silent on the premise.** |
| P3 | search limited to anthropic.com, claude.com and Anthropic docs and support domains, for release notes, "November 3", Opus 4.6 and Sonnet 4.6 | No indexed page states the 2026-11-03 rollout, or the current watermark state of these models. Launch dates found: Opus 4.6 on 2026-02-05, Sonnet 4.6 on 2026-02-17. Both are before 2026-08-02, so both are transition-period models, consistent with S7. |
| P4 | S7, the email | This is the only source that dates the change. Its "(see below)" part, about non-default sampling settings, was not supplied. |

Not opened this pass: the Claude Platform release-notes page and the support release-notes page in full. Search returned their URLs, but no matching text.

## Result
**The premise is not verified.** The evidence fits it:
- the email dates the rollout as 2026-11-03;
- both models launched before 2026-08-02;
- S1 says the older models are still to come.

But no public Anthropic page states that these models are unwatermarked today. The ✅\* in S2 could mean either "now" or "scheduled". Inference from these sources is not confirmation, and a Claude model's own account of its outputs is no evidence either (NOTES.md, Disclosure).

## Recommendation
- **Do not run** the REPORT.md §6 experiment on this premise as it stands.
- The premise can be confirmed only by something Anthropic itself states, for example:
  1. the rest of the S7 email (the "see below" part), which the Director holds;
  2. a direct question to Anthropic support: "Before 2026-11-03, are outputs of claude-opus-4-6 and claude-sonnet-4-6 watermarked?";
  3. a documented API response field or header that reports watermark status. None was found: S8 was read only in part, and Claude has no documented counterpart to Grok's `x-watermark` header.
- If the answer comes after 2026-11-03, the natural window is gone. The rest of REPORT.md (provenance and testing controls) does not depend on this premise.

## Not done
- no paid calls, model launches, detection requests or installs;
- no watermark-removal tools;
- no edits to REPORT.md or NOTES.md;
- no Git stage, commit or push;
- the previous build was not resumed.
