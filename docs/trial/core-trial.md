# TRIAL-C: hostile pass on the Rust core (axiom 9)

Lane TRIAL-C, 2026-11-11 (Toronto time, EST). Target: `crates/seqaddr-core` at commit `20e8b6c` (branch `build`).
Judged against `docs/spec/` with `DIRECTOR-RULINGS.md` (R1) governing, plus `docs/BUILD-LOG.md` and `crates/seqaddr-core/API.md`.
The core was **not edited**. Tests are in `crates/trial-core` (`cargo test -p trial-core`). Every test that shows a real
violation is `#[ignore = "finding N"]`, so the suite stays green. `cargo test -p trial-core -- --ignored` shows them all failing.

**Totals: 1 blocker, 8 major, 11 minor (20 findings).**

What held up under attack (no finding):
- **Address grammar.** 80 table cases covering every form, sentinel and tail position all match the spec. 20,000 grammar-generated addresses parse and round-trip. 200,000 junk strings (including Arabic-Indic and full-width digits) never panic, and nothing non-ASCII is accepted.
- **Book reader.** 30,000 junk or mutated logs never panic. Cutting a log at every byte (ASCII) or every character boundary (non-ASCII) keeps exactly the complete prefix and drops only the partial last line. A cut-short multi-op proposal is dropped whole.
- **Replay and snapshots.** Replay is deterministic, and `to_text` round-trips. A snapshot taken after any entry replays to the same state, and `replay_until` matches.
- **Finding order.** It is book -> shelf -> desk -> kernel (seqAddr.md:101), and a desk book `DD.00.BB` skips the shelf. A local draft does not shadow, and a kernel draft *face* is not inherited.
- **Claims and close rules.** The first claim wins (409, axiom 1). A foreign return is rejected, there are no skipped steps, the builder cannot review, and closing needs an outcome.
- **Counters and faces.** Counters 00/99/98 follow A4.4/A4.5. Workflow tails are refused on every non-counted face, and `retired` is refused on counters.

---

## Findings

### 1. BLOCKER: a crash that cuts a non-ASCII line makes the book unreadable and unwritable
- **Evidence:** `log.rs:307` (`file::read`) and `log.rs:323` (`repair_tail`, called first by `append`) use `fs::read_to_string`. `serde_json` writes non-ASCII raw, so a crash cut inside a multi-byte character (for example `café`, `—`, `名前` in a body) gives `Io { "stream did not contain valid UTF-8" }`. Read fails, repair fails, and every later append fails.
- **Test:** `log_hostile::crash_cut_inside_utf8_char_is_dropped_by_file_read_and_append`.
- **Spec:** format.md:67 "Crash safety. A partly written last line is detected and dropped. Nothing earlier can be damaged." format.md:140 "must never corrupt a book."
- **Note:** `BookLog::parse(&str)` can't even be given these bytes. The cut has to be handled on bytes, or JSON has to be written ASCII-escaped.

### 2. MAJOR: a brand-new face can be seated (approved) in one `put`, with no draft and no review
- **Evidence:** `state.rs:430` seats a new face on a bare `put`, by any author. For example, a `model` writes `10.11.21.1600.04` and it is live.
- **Test:** `rules_hostile::a_new_face_is_not_seated_without_draft_and_review`.
- **Spec:** drafting.md:20 "A brand-new face ... starts as an empty draft and still goes through notes and merges". seqAddr.md:201 says `FF.draft` is the unseated face. decisions.md:588 (E7, settled) "Nothing is promoted until it has faced a hostile pass". The spec also says drafting.md:33 "`put` ... allowed only to create a new face", so the spec is ambiguous about creating a face as *seated*. The core picked the reading that skips review, and logged no `7`. TRIAL-K raised the same thing as a blocker for the kernel seed (the doors were seated without the Director's yes). The core is what allows it.

### 3. MAJOR: `promote` has no review gate, and the drafter can promote its own draft
- **Evidence:** `state.rs:594-606` checks only that every note is struck. A draft with zero notes, promoted by its own author, is approved.
- **Test:** `rules_hostile::promote_needs_a_review_by_someone_other_than_the_drafter`.
- **Spec:** format.md:97 and drafting.md:31 "promote | after review". decisions.md:588 (settled) "from a view other than its maker's". BUILD-LOG:36 marks "no review gate" as `7`, but the spec is **not silent** here. Only the *recording* of review is open (drafting.md:45). The requirement itself, and "not the maker," are settled.

### 4. MAJOR: compute-only workflow steps are open to anyone, so the builder can close its own work as `passed`
- **Evidence:** `state.rs:497-533` restricts only `open->return` (owner) and `return->review` (not the owner). `draft->pack` (lint) and `review->bare` (close) accept any `by`. The builder `agent-7` closes `05.01` with `outcome: passed`. The lead moves an un-linted draft to `pack`.
- **Tests:** `rules_hostile::only_compute_closes_and_not_the_builder`, `only_compute_lints_draft_to_pack`.
- **Spec:** workflow-loop.003.md:171 step 2 "Lint | draft -> pack | compute | checks the pack against its template (section 8). A pack that fails stays draft". :176 step 7 "Close | review -> bare counter | Compute". 6.3 S10 "The builder is ineligible to review its own return". The pack lint (section 8) is not built at all, and BUILD-LOG has no `7` for it.

### 5. MAJOR: replay trusts a snapshot over the log; a forged or buggy snapshot silently rewrites history
- **Evidence:** `state.rs:320-332` replaces the whole state with `snapshot.state`, checking only the book and `last_n`. `replay` starts at the latest snapshot (`state.rs:228`). A snapshot that drops page 1523 (its pack, claim and return) replays without complaint. `history()` still lists the entries, so history and state disagree.
- **Test:** `log_hostile::forged_snapshot_is_not_trusted_over_the_log`.
- **Spec:** format.md:88 a snapshot is "the full current state". Axiom 6 "The past is not rewritten". format.md:140 "must never corrupt a book." The core needs at least a check mode that re-derives state from the log and compares, or a digest of the prefix.

### 6. MAJOR: draft (and any-state) counters and whole task boards are inherited from the kernel
- **Evidence:** `resolve.rs:119-137`. A bare `PPPP.05.NN` or `PPPP.05` walks book -> kernel and returns the kernel's counter whatever its tail. For example, `10.11.21.0057.05.01` returns the kernel's `draft` pack, with `origin: kernel`.
- **Test:** `rules_hostile::a_kernel_draft_counter_is_not_inherited`.
- **Spec:** API.md:47 "Drafts and retired faces are never inherited". decisions.md:277 counts `05.01.draft` as a draft face. seqAddr.md:133 "draft | being written; not active". wl.003 6 says counters are a page's own passes. A kernel task showing up as every book's task is not a lawful connection (axiom 8).

### 7. MAJOR: a retired page still resolves as the live local face and shadows the kernel
- **Evidence:** `resolve.rs:115` never looks at `PageState::tail()`. After `10.11.21.0030` is retired (page tail op), `10.11.21.0030.04` resolves `Local`, and the kernel's `0030.04` is hidden. The same holds for a book retired through `0000.retired`: its faces still resolve, and writes are still approved.
- **Test:** `rules_hostile::a_retired_page_is_not_live`.
- **Spec:** seqAddr.md:138 retired is "previously seated, retired before removal". Axiom 1 "location, state, and a lawful connection decide what is live". decisions.md:99 / :172 say `0000.retired` retires the book/desk. What a retired page answers is not written down, so at minimum this should be a `7`, not silent "live".

### 8. MAJOR: `owner: kernel-only` is not enforced; a book can redefine kernel-only cards (and anyone can write the kernel)
- **Evidence:** `validate.rs` has no owner or authority check. A `model` overrides `0054.01 ## General` (kernel `owner: kernel-only`) in book 10.11.21, and it is approved and resolves `Local`. Writes to `00.00.00` by any `by` are approved.
- **Test:** `rules_hostile::kernel_only_cards_cannot_be_redefined_by_a_book`.
- **Spec:** decisions.md:287 "marked `owner: kernel-only`, so no book can redefine it". seqAddr.md:193. C5.2 (decisions.md:380, levels settled) "`00` internal authorised admin | the kernel". BUILD-LOG has no `7` for leaving authority out.

### 9. MINOR: the 99 pointers take content; desk 99 takes a user book
- **Evidence:** A proposal writing `10.11.21.9999.01` (law) and `.04` is approved. A book `99.10.10` with law/why content is approved. `validate.rs:310` only adds a back-link check for pointers.
- **Tests:** `rules_hostile::pointer_99_is_never_content`, `desk_99_is_a_reserved_pointer_not_a_user_desk`.
- **Spec:** decisions.md:214 "At every level, 99 is a pointer, never content. ... Its face 08 (map) records each target". seqAddr.md:39 desk `99` "reserved pointer". decisions.md:260 user environments are 10-98.

### 10. MINOR: a retired face is re-seated through `put FF.draft` + `promote`
- **Evidence:** A bare `put` on a retired face is refused (`state.rs:421`), but `state.rs:433` allows a draft on it, and `state.rs:605` `promote` re-seats it and clears the retired body from state.
- **Test:** `rules_hostile::a_retired_face_is_not_reseated_through_a_draft`.
- **Spec:** seqAddr.md:201 "`FF.retired` is a previously seated face awaiting removal". The two paths disagree inside the core.

### 11. MINOR: compute can take over a live claim at any time (no recorded abandonment decision)
- **Evidence:** `state.rs:504` lets `compute` do `open->return` on any open counter. A later close as `abandoned` needs only that.
- **Test:** `rules_hostile::compute_returns_only_during_authorized_recovery`. Core test `tails.rs::wl003_6_compute_may_return_during_recovery` encodes the violation.
- **Spec:** wl.003:174 "Compute during **authorized** recovery". wl.003:206 "Silence alone leaves the claim unresolved. After the required authority records an abandonment decision, Compute fences the old claim". *Who* may confirm is `7` (wl.003:208). *That* a decision is recorded first is settled.

### 12. MINOR: back-links can be drafts, and removing a back-link is not checked
- **Evidence:** `validate.rs:327` reads the target's `view()` (draft if any), so a `0000.08.draft` back-link satisfies A5.3. Retiring the target's `08` is approved, which leaves `9999` linking one way. Back-links are checked only when the pointer page itself is written.
- **Tests:** `rules_hostile::back_link_must_be_live_not_a_draft`, `retiring_a_back_link_does_not_leave_a_one_way_link`.
- **Spec:** decisions.md:230 "A link that only goes one way is a validation error". Axiom 8 "lawful only when it is written". decisions.md:280 (C1.3) says the compute updates incoming links when something is retired.

### 13. MINOR: provisional choices made in code with no BUILD-LOG `7`
- `validate.rs:233` exempts page 9999 from "pages 1000 and up must have a title". seqAddr.md:115 and decisions.md:131 give no exception. Test: `rules_hostile::pages_1000_and_up_need_a_title_including_9999`.
- `validate.rs:283` skips C3.2 for a counted 01/02 face. The spec is silent, and no `7` was logged.
- These may be good choices, but the contract (CONTRACT.md "mark it `7` in BUILD-LOG") asks for them to be logged.

### 14. MINOR: `sentinel(value, width)` is wrong for 3-digit groups
- **Evidence:** `addr.rs:292`: any width other than 4 uses 99 as the all-nine value, so `sentinel(99, 3)` is `Pointer` and `sentinel(999, 3)` is `None`. Brands are 3 digits (seqAddr.md:279), and decisions.md:443 reserves `000`/`999`. R1 speaks of "a full zero sequence".
- **Test:** `grammar_hostile::r1_sentinel_on_a_three_digit_group`. Either reject widths other than 2/4, or compute 10^w-1.

### 15. MINOR: a crash during `create` (cut header) leaves a book that can't be read or repaired
- **Evidence:** `log.rs:204` returns `Corrupt "no header line"` after dropping the cut header. `repair_tail` fails the same way.
- **Test:** `log_hostile::crash_during_create_leaves_a_readable_empty_book`.
- **Spec:** format.md:67 (crash safety). This is low risk, because `create` writes one short line and fsyncs.

### 16. MINOR: timestamps are shape-checked only
- **Evidence:** `log.rs:135` accepts `2026-13-45T99:99:99Z`.
- **Test:** `log_hostile::timestamps_must_be_real_times`.
- **Spec:** format.md:80 "time". The contract says ISO 8601 UTC.

### 17. MINOR: core tests named after spec sections that test something else (task part 4)
- `resolve_validate.rs::a4_6_missing_stays_missing_axiom_7` asserts an **error** (404). A4.6 (decisions.md:205) says missing "is not an error". The behaviour is A1.8 elevation, so the name cites the wrong rule.
- `grammar.rs::a4_4_board_takes_no_tail`, `a5_1_counter_continuation_takes_no_tail` and `tails.rs::a4_4_board_and_pointer_take_no_tail_move` are named as A4.4/A5.1 rules, but they test the provisional `7` at BUILD-LOG:32.
- `tails.rs::wl003_6_draft_pack_may_be_rewritten_while_draft`: wl.003 6 says nothing about rewriting. It is BUILD-LOG:33's `7` (see 18).
- `tails.rs::wl003_6_compute_may_return_during_recovery` and `s11_abandoned_needs_system_return` model no "authorized" recovery (finding 11).
- Some tests are too weak for their name. `tails.rs::drafting_new_face_starts_as_draft` passes but never checks that a new face *must* (finding 2). `log_format.rs::format_3_1_partial_last_line_dropped` is ASCII and in-memory only (finding 1). `format_3_4_snapshot_then_replay_from_it` uses only an honest snapshot (finding 5). `resolve_validate.rs::s4_drafts_are_not_live_and_not_inherited` covers faces, not counters (finding 6). `c1_3_retiring_last_content_face_retires_page` skips C1.3's "updates ... incoming links" (finding 12).

### 18. MINOR: BUILD-LOG `7` at line 33 is where the spec speaks
- **"`put` on a counter still in `draft` replaces its body":** format.md:86 "`put` | create a new face or counter". decisions.md:329 "A full-body `put` is allowed only to create ... never to replace". The spec speaks, against it.
- **"Counter created ... `pack`":** this conflicts with wl.003:171 (only compute's lint moves `draft -> pack`), though format.md:75's example does it. The spec contradicts itself. This should be raised as a conflict, not as silence.

### 19. MINOR: "counted" is hard-wired to 05, 06 and `0012.03`
- **Evidence:** `state.rs:54` `Policy.extra_counted = [(12,3)]`.
- **Spec:** decisions.md:199 "Other faces may be counted on certain page types, for example 03 or 04 on a contents or dictionary page". A contents page 0010 can't count 03/04. BUILD-LOG:31's `7` covers the board conflict, not this.

### 20. MAJOR: overriding one kernel 01 card forces a local copy of the kernel's 04 card
- **Evidence:** `validate.rs:281-294` looks for the 04 card only on the local page. With kernel `0030.01`/`0030.04 ## Job`, a book that writes only its own `0030.01 ## Job` is rejected (C3.2).
- **Test:** `rules_hostile::a_01_card_may_use_the_inherited_04_card`.
- **Spec:** seqAddr.md:104 / decisions.md:128 books follow the kernel live. Axiom 2 "Inherit what is agreed; write only the difference. Do not copy the parent ... both create drift". C3.2 (seqAddr.md:175) asks that a 04 card *exist*, not that it be local. The app lane already resolves an inherited 04 (BUILD-LOG:15). The core and the app disagree.

---

## Part 3: BUILD-LOG `7` audit (is the spec really silent?)

| BUILD-LOG line | Choice | Verdict |
|---|---|---|
| 31 | boards derived, 05/06 + 0012.03 counted | Real conflict (decisions.md:196 vs format.md:102). OK, but see 19. |
| 32 | FF.00 / FF.99 take no tail | Silent. A5.1 "never content" supports it. OK, but tests are misnamed (17). |
| 33 | counter created bare/draft/pack; draft put replaces | **The spec speaks** (18). |
| 34 | tail op names the slot; bare = "" | The spec speaks *and agrees* (format.md:76 example). Not really a `7`. |
| 35 | retire only from seated; page draft derived | seqAddr.md:201 agrees. Re-seat path is inconsistent (10). |
| 36 | D0 on by default; promote with no review gate | Enforcing a *proposed* mechanism by default is logged and switchable, OK. **"No review gate" is wrong: the spec speaks** (3). |
| 37 | claims; compute may return; reviewer = tail author | Claim shape is OK as `7` (wl.003:208). **Compute return without a recorded decision: the spec speaks** (11). Reviewer = author is logged as a finding, OK. |
| 38 | `proposal`/`of`, snapshot `state`, `use` by compute | `proposal` id is spec (format.md:100). `of` and `state` are OK as `7`. Snapshot trust is not addressed (5). |
| 39 | door first; C1.1 on 0000 | Real conflict with the format.md:74 example, logged. OK. |
| 40 | one book per proposal; faces 07/09/10-99 rejected; C6 hard | wl.003:10 is `7`, OK. Face ranges are spec (A4.3), not `7`. |
| 41 | C3.2 newest view; unknown types are findings; back-links | OK as `7`, but local-only 04 (20) and draft back-links (12). |
| 42 | title form; stamp form | Silent beyond the C2 example. OK. |

## Part 5: resolution order and "drafts never inherited"
- **Order:** it matches seqAddr.md:101 exactly, including the trace and missing books (`no book`). Desk books skip the shelf, consistent with decisions.md:166.
- **Draft faces:** not inherited, and a local draft does not hide an inherited live face. This agrees with seqAddr.md:133.
- **Draft counters and boards:** inherited. This violates API.md:47's own promise (6).
- **Retired pages and books:** still live (7).
- **Observation, not a finding:** a *retired local face* falls through to the kernel's face. The spec doesn't say whether retiring an override should re-expose the parent. This should be raised as a question.

## How to run
```
cargo test -p trial-core               # green: 20 pass, 20 ignored (each names its finding)
cargo test -p trial-core -- --ignored  # the 20 ignored tests fail, one per documented violation
```
