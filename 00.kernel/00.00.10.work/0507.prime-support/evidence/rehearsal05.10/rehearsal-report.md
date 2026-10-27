# Rehearsal report — real work book, nonblind (0507.prime-support 05.10)

Executor: claude-opus-5-5, Colab. Date: 2026-10-27.

**What this is, and is not.** This is a NONBLIND rehearsal. The same session that designed and built `prime_boot` ran it. It tests whether the accepted tool is useful on our real records. It does not show that a fresh model understands them. "Prime" in the request is an exercise label, and Prime is Codex (R03). I ran `prepare` and `check` only; I did not run `judge`. No source page was corrected.

## Run

| | |
|---|---|
| Tool | `prime_boot.py` 54b23484…, unchanged, with the pinned accepted tools (code-pins.json) |
| Pinned source | D:/Git/lib-build at a38d05a487dcf468527161eb929b2052acf6cec6. HEAD and the workshop branch were fab74ab before and after. Nothing was fetched or checked out, and no newer commit was substituted. |
| Records root | `C:\Users\misg\AppData\Local\Temp\pb-rehearsal-0510-2f7t3yte`, outside Git and kept for Prime. Every file is also inside `records.json`. |
| Attempt | one attempt, `a1`. No retry was needed. |
| Commands | `prepare`: exit 0, `prepared`. `check`: exit 0, `checks ok`, O1-O6 all ok. `show`: `prepared; checks ok; awaiting judgement; not oriented`. |
| Files | 00-10, 19, 20-22, and the two member inspection raws. No 30, 31 or 39 file exists. |

## Usable context: what the packet held

The packet holds 10 refs and 43,791 bytes, inside the 12-ref and 128 KiB limits. Nothing was omitted and nothing was absent.

| Ref | Source (commit blob unless marked) | Live |
|---|---|---|
| R01 | `00.md`, which points to `0011.contents/01.036.md` | **differs**: the live file points to `01.037.md`, set by fab74ab |
| R02 | `0011.contents/01.036.md` (check_book exit 0, no findings) | same |
| R03 | `0408.seats/01.md` | same |
| R04 | `0401.goal/06.01.md`, the canonical assignment (parsed as v1) | same |
| R05 | member `0126.boot-members-0509`, observed live through the pinned inspector: `complete`, receipt 706ed69c… | re-observed, stable |
| R06-R10 | 0507/05.09, 0507/05.08, 0504/05.14, 0508/05.10, `0410.imports/01.md` | same |

The stability check passed: HEAD, the branch, the registry, the tool hashes and the member identity were all unchanged.

## Verified facts, compared with what the sources claim

Verified, as hashes and exits:
- the pack and code pins;
- the commit blobs, and that the packet text equals them;
- the member capture identity: it matches the receipt hash on 05.09's own Return line;
- that every source and the 0126 member are byte-unchanged by my reads.

Claimed by the pages, and not proven by compute:
- every Release, Claim and Review sentence;
- `Accepted within scope` in R06, R07, R08 and R09 (Prime's recorded Reviews);
- who sits in which seat.

## Stale, missing or conflicting instructions (left as they are)

1. **Canonical assignment.** R04 says `current_work 0504.app-entry/05.06.md`, `assignment_state accepted`, and waits on `0506/05.04`. The packet shows much later work returned and accepted. Status reports conflict 0, "canonical current_work … is not inside lane 0507.prime-support's registered pages".
2. **Stale header on 05.09.** R06's header says `state: draft; awaiting Director release`, and its Assignment says `Release: PENDING. Claim: PENDING.` Its own Return pointer and Review show it released, returned and accepted. R07 (05.08) has the same pattern.
3. **Seats.** R03 is a draft from 2026-10-26. Its Builder cell is scoped to 0504/05.01. Grok Builders 1 and 2 on later batches (R08, R09) have no seat record in the packet.
4. **Missing from the packet.** `evidence/prime-review05.09/review.md`, named by R06 for the next action, and law 0062-0065, named by R03.
5. **Status tool limits on real pages.** `prime_support status` gave "ambiguous heading" for 05.01 and 05.05-05.10, so it can't compute return identity for most lane pages. It also gave unbound reviews for 05.01-05.03, and 9 review-needed items. Its scope includes 05.10.md, which comes from live state: the committed contents list 0507 only up to 05.09.
6. **Live entry pointer.** The live `00.md` points to a newer contents face (01.037) than the pinned commit (01.036). I used the commit text; the live pointer is recorded only as an observation.

## Answers (as recorded in 21.answers.json) and check results

The check verified that citations exist, that the target is in scope, that conflict 0 was acknowledged, and that each O2 value occurs in R06. **It does not show understanding.** Prime assesses the explanations.

- **O1. Target:** 0507/05.09 (R06), acknowledging conflict 0.
  - The packet shows no released, unreturned 0507 batch at a38d05a. 05.09 is the newest batch, and it is returned and accepted.
  - The canonical record (R04) disagrees with the lane. Both are reported, and neither is picked.
  - The status scope's 05.10 comes from live state. My knowing that 05.10 is this rehearsal is session knowledge, not packet evidence.
- **O2. Fields of 05.09 (R06):**
  - Release: "Release: the Director, chat 2026-10-27";
  - Claim: "Claim: claude-opus-5-5 (Anthropic), Colab, executor";
  - Execution: "Execution: returned. Member 0126.boot-members-0509.";
  - Review: "Accepted within scope,2026-10-27."
  - The stale header and Assignment are reported as a gap.
- **O3. The why:** in R06 #01-#04 and in the 05.08 Review's "Next draft05.09…" (R07). The 05.09 review file and the law role pages are not in the packet.
- **O4. What I may do:** read-only investigation only. New 0507 work is held for a Director release. The canonical record can't pick work until someone with authority reconciles it. Acceptance is Prime's, and the receipt is custody only.
- **O5. Unknowns:** the current assignment (R04 against R06 and R08); the seat record for the later builders (R03 against R08 and R09).
- **O6. What I will not do:** judge, accept, seat, lock, promote, treat a receipt as approval, edit records to pass, dispatch, acknowledge, commit, push, merge into main, or claim a fresh boot or the Prime seat. Orientation is not authority.

## Unresolved decisions (for the Director or Prime, not for me)

- **D1.** Should the canonical assignment `0401.goal/06.01.md` be updated, and by whom? Today it contradicts the record.
- **D2.** Should batch headers (`state:`, and the Assignment `Release` and `Claim`) be updated when a batch is released and returned, or does the Return pointer replace them?
- **D3.** How should Grok Builders 1 and 2 be recorded on `0408.seats`?
- **D4.** Should `prime_support`'s return-identity parse handle the "ambiguous heading" pages, or should the pages change form?

## Recommended next bounded action

Prime should judge these answers from this return, and record that judgement in a new linked step, not by editing a1's records. Then decide D1. The stale canonical assignment is the one gap that would mislead a fresh model's O1 and O4 on every real boot.

## Learning

- **What worked.** The tool held up on the real book with no changes. The packet was small, complete and inside the limits. The conflict surfaced on its own, and the member identity was exact.
- **What didn't help.** The Prime status attention list was mostly noise on real pages (unsupported headings, unbound reviews). The stale headers make "status by header" wrong, so a fresh model must read the Return and Review sections, not the header.
