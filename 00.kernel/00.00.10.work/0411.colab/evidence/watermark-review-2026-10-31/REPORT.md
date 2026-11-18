# REPORT — Could provider text watermarking materially affect the Workshop?

Date: 2026-10-31. Independent Colab review by claude-opus-5-5 (Anthropic). Research and assessment only. Working notes, source versions and access failures are in `NOTES.md` beside this file. Reread once in full; the corrections from that reread are integrated (listed at the end).

**Conflict of interest.** I am a Claude model, and the subject is my own provider's watermark. I cannot observe the deployed sampler, the watermark key or its parameters, or whether any response, mine included, was marked. My statements about my own outputs are not evidence of marking.

## Did, Blocked, Need

**Did:**
- Read S1 (Anthropic announcement, 2026-08-14, updated 2026-09-01), S2 (Claude support article, undated "updated this week"), S3 and S4 (SynthID-Text README and `docs/tournament.md`, repo HEAD `9c055d932e042b75197e337371448a120bbc65bb`, tournament doc byline 2026-10-09) and S6 (xAI watermarking docs, undated, default-on from 2026-11-07).
- Used the partial Anthropic email the Director supplied (S7).
- Checked the sampling-parameter documentation (S8, S9).
- Wrote NOTES.md, then this report.
- Changed nothing: no code, settings, build artifacts or Git.

**Blocked:**
- The Nature paper's full text. The Nature page sends me to a login, PMC shows a CAPTCHA, and a mirror returns 403. Its identity (DOI 10.1038/s41586-024-08025-4; Nature 634, 818–823; online 2024-10-23) and the ~20 M-response live experiment are confirmed only by bibliographic records and search snippets. Paper details below are marked *recalled, not re-verified*.
- The "see below" part of Anthropic's email (S7), which explains its sentence about "non-default sampling settings".
- Anthropic's primary statement of current sampling-parameter support per model. Its API reference is too large to read whole, and the secondary sources conflict.

**Need:**
- The rest of the Anthropic email, or the page it links, before deciding anything that depends on sampling settings.
- A Director decision on the recommendation and on the optional experiment (§6). The experiment has a time window: before 2026-11-03.

## 1. Claim / evidence / qualification

| # | claim | evidence (source) | qualification |
|---|---|---|---|
| 1a | Raw model predictions (logits) are unchanged; watermarking changes sampling. | SynthID: "Watermarking is the last step before sampling". It truncates to top-k, renormalises, reweights per layer by `(1 + g − g_mass)`, then samples (S4). The reference defaults are top-k 40, depth 15 and a context of 4 tokens. Anthropic: the watermark changes how a choice is made among candidates, using a key and preceding words (S1). | **Established for SynthID-Text** as published. Logits are untouched; the **processed probabilities** for a given key and context **are changed**, and so is the **final token**. For deployed Claude, Anthropic says "a version of" SynthID-Text (S1), with its parameters unpublished, so the exact pipeline is **not established**. |
| 1b | Text meaning, format and size are unchanged. | "Nothing is added to the text and there are no hidden characters"; no extra tokens or cost (S1). Grok: no characters or markup are added (S6). | Established as provider statements. "No added characters" is true by construction. "Meaning unchanged" is a quality claim; see 4. |
| 2 | "Distortion-free" means unchanged probabilities. | "if you sample `key` at random, then the distribution of the sampled tokens is the same as without watermarking" (S4). Exact "only … for records shorter than roughly `context_history_size` tokens" (1024 contexts). Repeated-context masking is "essential for ensuring the watermarking procedure remains non-distortionary" (S4). | **False as stated.** The guarantee is an expectation **over a randomly drawn key**, per record. A deployed system uses **one fixed key**. For a fixed key, the per-context distribution *is* reweighted, and with many layers sampling is "close to deterministic for a fixed key" (S4). In the reference implementation, masking skips contexts already seen inside the record, so one response cannot compound a bias; it does nothing **across** records. The deployed masking window is unpublished. The guarantee does not cover records longer than the history window, and says nothing about the population of all users sharing the fixed key. |
| 3 | Watermarking creates recurring "slop keywords". | The mechanism (S4): with a fixed key and a 4-token context window, the same context systematically favours the same candidate continuations among the model's top-k. Anthropic: it does not push Claude toward words it wouldn't otherwise consider (S1). | **Not established, but not excluded.** The mechanism does not imply global keywords: the preferences are **conditioned on the preceding tokens** and limited to tokens the model already ranks highly. A fixed key *can*, in principle, make choices **more consistent across separate responses that share contexts**, which a reader could experience as a recurring phrasing. Ordinary model style (training-derived habits) existed before watermarking and is a separate cause. Telling them apart needs a controlled on/off comparison (§6). No source I read measured cross-response repetition under a fixed key. |
| 4a | Watermarking cannot affect quality or diversity: the mathematical guarantee. | The random-key, per-record distribution equality (S4). | **Narrow.** It averages over keys, not the fixed deployed key. It concerns distribution, not "quality". Cross-response diversity under one key is not covered. |
| 4b | Provider evaluations. | Anthropic: "Watermarking does not impact the quality of Claude's output"; internal testing found "no impact … on the content, level of creativity, or readability" (S1). DeepMind: a live experiment on ~20 M Gemini responses found no statistically significant change in user feedback (S1 citing S5; snippets of S5). | **Provider claims.** Anthropic's methods and metrics are not published. The DeepMind result is for Gemini with its own configuration (*details recalled, not re-verified*). Thumbs ratings are a coarse quality signal, and do not measure diversity, voice stability or exact-copy fidelity. |
| 4c | Independent evidence. | None found or read this session for the deployed Claude system. | **Absent here.** |
| 4d | Established for the deployed Claude system. | — | **Not established** independently: parameters, key handling, masking window, and behaviour under non-default sampling (S7 hints these matter for compliance) are all unpublished. |
| 5a | Detection identifies model involvement. | Detection indicates Claude was "likely involved"; it does not work well on small samples (S1). "A detected mark provides a signal that content was processed by Claude, but is not fully conclusive"; absence proves nothing (S2). Frequentist detector: a p-value against "not watermarked" (S3). | A **statistical signal of Claude involvement** in a passage. It is weaker on short or low-entropy text, partly survives light edits, and carries into translation (S1). A fixed key can inflate false positives for shared n-grams unless the detector is calibrated (S4). |
| 5b | What detection cannot establish. | "carries no identifying information and can't be traced to a specific person, organization, or chat" (S1); it does not confirm human authorship (S1). | It cannot establish **who** (account or organization), **how much** human contribution there was, **authorship**, or whether a passage was **generated or edited**: Claude proofreading human text leaves few marks, and humans editing Claude's text leave some (S1). Access is a private-preview API for eligible organizations (S1, S2). The Workshop cannot run it. |

## 2. Practical consequences for the Workshop

**Runnable code, JSON and tool arguments.**
- **Anthropic:** "Where an exact output is required… the watermark isn't applied". Code is watermarked less, and comments can be watermarked (S1). This is a provider statement: when an output counts as "exact output required" is not specified, and JSON and tool arguments are not mentioned.
- **xAI:** says the opposite for its own system. Grok watermarks "structured outputs, and tool call arguments" (S6).
- **Mechanistically:** syntax-forced positions are low-entropy and carry almost no signal. Where several valid choices exist (names, ordering, wording in comments), the watermark changes *which* valid choice is made, as ordinary sampling already does.
- **Assessment:** no new failure class. Correctness is still established by our tests, validators, strict JSON parsing and pins, never by trusting generation. The Grok difference matters if Grok tool arguments ever carry exact identifiers. They should be validated, as ours already are.

**Copying exact Director wording and preserving source bytes.**
- Copying is usually low-entropy, so watermark influence is small. It is not zero wherever the model is uncertain, and that is equally true of unwatermarked sampling.
- The Workshop already avoids model retyping for bytes: snapshots, captures and sha256.
- **One real gap, independent of watermarking:** return-pointer "Release" lines and Director quotes are *typed by the executing model* from the chat prompt, with no on-disk source to hash against. A misquote there would not be caught.

**Hashes, immutable returns and reproducibility.**
- A watermark acts at generation. Once bytes exist, hashes, receipts and captures bind them exactly. Nothing is invalidated.
- Byte-reproducible regeneration was never available under sampling. A fixed key may make repeated generations for identical contexts *more* alike, not less.
- The Workshop's reproducibility rests on stored bytes, not regeneration, so this is **not material**.

**Specifications.**
- Normative terms are low-entropy; choices among synonyms are where a watermark acts.
- Meaning is protected only by review, as it already is. No new risk is identified beyond ordinary sampling variation.

**Narrative voice and long RPG sessions.**
- This is the **most exposed area**. Creative text is high-entropy, so it carries the strongest mark and the most watermark-steered choices.
- Long sessions are many records. In the reference implementation, masking protects within one response, but not across turns that share 4-token contexts, so fixed-key preferences could surface as recurring phrasing across a campaign. **Unmeasured** (claim 3).
- **Disclosure consequence:** published creative writing that Claude drafted or substantially wrote may later test as "Claude likely involved" with an eligible detector, after light editing and in translation. It is not traced to the account.

## 3. Documented controls, by surface

| surface | is the watermark applied? | documented control | notes |
|---|---|---|---|
| Claude apps (subscription) | yes, for supported models (S2) | **none documented** | file outputs also get C2PA metadata (S1, S2) |
| Claude Code | yes; listed among surfaces (S2) | **none documented** | no user sampling parameters found in the sources read; **not verified** |
| Claude API (first party) | yes (S1, S2); the older models listed in S7 from 2026-11-03 | **none documented** | S7: "You don't need to change anything unless you rely on the watermark for your own compliance and use non-default sampling settings (see below)". The detail was not seen, so **no inference** that sampling disables or weakens it. Secondary sources conflict on whether Opus 4.7+ ignore or reject `temperature`, `top_p` and `top_k` (S9) |
| Claude via AWS, Google Cloud, Microsoft Foundry | yes, per S2's partner list; Bedrock rollout may lag (S7) | none documented | |
| Grok API | yes, default-on from 2026-11-07 for listed models (S6) | **team-admin opt-out per model in the console; some models locked on**; an `x-watermark: true` response header | covers structured outputs and tool-call arguments; no request parameter |

## 4. Independent assessment, and where I disagree with the framing

1. **The watermark changes outputs.** "Raw predictions unchanged" is accurate but not reassuring on its own: what the Workshop receives is the final token, and that does change. The honest summary is: the same model, the same candidates, a different (keyed) choice among them.
2. **"Distortion-free" is narrower than the framing suggests.** It is an average over keys, per record. The deployed fixed key is exactly the case the guarantee does not describe. That is the strongest technical reason for caution, and the reason claims 3 and 4 remain open rather than settled.
3. **"Slop keywords" conflates two things.** Model style is trained. A keyed signature is context-conditioned and statistical. The mechanism permits cross-response consistency, but nothing I read shows global recurring keywords. Treat it as a testable hypothesis, not a finding.
4. **For coding, specifications, hashes and immutable returns,** I find **no material effect**. The Workshop never relies on generation alone for correctness or exactness: code is tested and validated, and bytes are carried by files and hashes. The real exact-text weakness here, model-typed Director quotes, exists with or without watermarking.
5. **The material consequences are two.**
   - **Disclosure:** creative and other published prose that Claude wrote can test as Claude-involved, unless it is heavily rewritten (S1: light editing "probably won't remove the watermark completely").
   - **Possible voice effects** in long creative sessions: unmeasured.

   Neither is about code quality. The first is a policy question for the Director, not a technical defect.
6. **Disagreement with the framing:** the concern raised before this request was that Claude might not be usable at all. The evidence does not support that for the Workshop's engineering. It does support a clear-eyed authorship and disclosure decision for creative work, and an inexpensive measurement if voice matters.

## 5. Recommendation: **add provenance and testing**

Continue using the tools. There is nothing to configure: no Claude opt-out is documented, and changing sampling is not a documented control. Add the following.

1. **Director-quote provenance.** Release and quote lines should be copied from a stored source:
   - the Director's message saved to a file by the harness, or pasted into the page by the Director, with its sha256 recorded and the model's quote checked against it byte for byte;
   - until then, mark model-typed quotes as transcribed.

   This closes the one exact-text gap, whatever the watermark does.
2. **Authorship records.** Keep the existing `who:` and disclosure lines as the Workshop's provenance. Do not use watermark detection as evidence of who wrote what. Decide a disclosure policy for any published creative writing.
3. **Evidence before belief on creative voice.** Run the experiment in §6 if the Director cares about it.
4. **Grok.** If Grok output ever carries exact tool arguments, validate them, as already done. Record whether the team opt-out is used, as an account decision, not a model setting.

## 6. Smallest meaningful experiment (proposal only; not run; paid calls need Director approval)

**A natural on/off window may exist until 2026-11-03.** S7 says Opus 4.6 and Sonnet 4.6 begin carrying the watermark then. However, S2's model table already lists Sonnet 4.6 with first-party text watermarking, which may describe the scheduled state. **The premise that a model is unwatermarked today is not verified.** Confirm it with Anthropic before spending, and prefer Opus 4.6 only if confirmed.

1. **Exact copy.** Ask Opus 4.6 to reproduce one ~3 KB Workshop text exactly, 10 times before and 10 times after 2026-11-03, at default sampling. Hash each output and count byte mismatches.
2. **Voice.** Ask for 20 continuations of one fixed RPG scene prompt, before and after. Measure distinct-n and repeated 4-gram rates, and have the Director rate blind, unlabelled pairs.
3. **Controls:**
   - record the model id, date and settings;
   - do not vary sampling parameters (that would confound, and must not be read as disabling anything);
   - keep every output as captured bytes;
   - report "no difference detected at this size", never "no effect".

The cost is about 60 calls. A Grok-only alternative uses the team opt-out for a same-day on/off pair. It needs no deadline, but tells us about xAI's watermark, not Claude's.

## Sources

- S1 Anthropic, "Claude text watermark", https://www.anthropic.com/news/claude-text-watermark (2026-08-14; updated 2026-09-01).
- S2 Claude Help Center, "How Claude marks AI-generated content", https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content (undated: "updated this week").
- S3 google-deepmind/synthid-text, https://github.com/google-deepmind/synthid-text (HEAD `9c055d932e042b75197e337371448a120bbc65bb`, read 2026-10-31).
- S4 `docs/tournament.md`, https://github.com/google-deepmind/synthid-text/blob/main/docs/tournament.md (byline 2026-10-09, at the HEAD above).
- S5 Dathathri et al., "Scalable watermarking for identifying large language model outputs", Nature 634, 818–823 (2024), https://www.nature.com/articles/s41586-024-08025-4. **Full text not accessible to this review.**
- S6 xAI, "Watermarking", https://docs.x.ai/developers/advanced-api-usage/watermarking (undated; default-on from 2026-11-07).
- S7 Anthropic email "Text watermarking is coming to more Claude models", partial screenshot supplied by the Director.
- S8 Claude Messages API reference, https://platform.claude.com/docs/en/api/messages (partial read).
- S9 Secondary sampling-parameter sources: the OpenRouter Claude 4.7 migration guide, https://openrouter.ai/docs/guides/evaluate-and-optimize/model-migrations/claude-4-7, and DEV Community posts. **Conflicting; not primary.**

## Corrections integrated on reread (2026-10-31)

- **§6:** the "unwatermarked until 2026-11-03" premise was stated as fact. S2's table lists Sonnet 4.6 as text-watermarked, so it is now marked unverified, with a confirm-first step.
- **§4 item 4:** "never relies on generation" was overstated. It now reads "generation alone", with the reason.
- **§4 item 5:** the disclosure sentence was reworded to match S1's editing statement.
- **§4 item 6:** the framing disagreement now attributes the concern to the earlier message, not to this request.
- **Claims 1a and 2, §2:** reference-implementation defaults and masking are marked as such; the deployed values are unpublished.
- **§2 code:** the scope of Anthropic's exact-output exemption is marked as unspecified.
