//! Tail state machine, drafting and claims (seqAddr 4, 5.7; format 3.3, 4.1;
//! drafting.md / D0; workflow-loop.003 section 6).
mod common;
use common::*;
use seqaddr_core::log::Op;
use seqaddr_core::tail::{check_counter_move, CounterTail::*, FaceSlotState};

const PK: &str = "10.11.21.1523.05.03";

fn with_pack() -> Bk {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1523.00", None, "title: timer").unwrap();
    b.put(PK, Some("pack"), "## w01\ntype: work\n").unwrap();
    b
}
fn to_review(b: &mut Bk) {
    b.tail("builder", PK, Some("pack"), Some("open")).unwrap();
    b.tail("builder", PK, Some("open"), Some("return")).unwrap();
    b.tail("reviewer", PK, Some("return"), Some("review")).unwrap();
}

#[test]
fn wl003_6_tails_move_one_step() {
    for (a, z) in [(Draft, Pack), (Pack, Open), (Open, Return), (Return, Review), (Review, Closed)] {
        assert!(check_counter_move(a, z).is_ok());
    }
}
#[test]
fn format_4_1_pack_to_return_never() {
    assert_eq!(check_counter_move(Pack, Return).unwrap_err().rule(), "format 4.1");
}
#[test]
fn wl003_6_no_skips_no_backwards() {
    for (a, z) in [(Draft, Open), (Open, Pack), (Review, Open), (Closed, Draft), (Open, Closed), (Return, Closed)] {
        assert!(check_counter_move(a, z).is_err(), "{a}->{z}");
    }
}
#[test]
fn a2_5_bare_counter_is_closed_no_closed_tail() {
    let mut b = with_pack();
    to_review(&mut b);
    let mut e = b.e("compute", Op::Tail, PK);
    e.from = Some("review".into());
    e.to = Some("closed".into());
    e.outcome = Some("passed".into());
    assert!(b.apply(e).is_err());
}
#[test]
fn format_3_3_put_creates_counter_with_tail() {
    let b = with_pack();
    assert_eq!(b.st.counter(1523, 5, 3).unwrap().tail, Pack);
}
#[test]
fn format_3_3_tail_rejected_if_from_not_current() {
    let mut b = with_pack();
    let e = b.tail("x", PK, Some("draft"), Some("pack")).unwrap_err();
    assert_eq!(e.rule(), "format 3.3");
}
#[test]
fn format_2_first_claim_on_pack_wins_second_conflicts_axiom_1() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    let e = b.tail("agent-8", PK, Some("pack"), Some("open")).unwrap_err();
    assert_eq!((e.code(), e.axiom()), ("conflict", Some("1")));
    assert_eq!(b.st.counter(1523, 5, 3).unwrap().claim.as_ref().unwrap().owner, "agent-7");
}
#[test]
fn s11_claim_records_id_owner_start() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    let c = b.st.counter(1523, 5, 3).unwrap().claim.clone().unwrap();
    assert_eq!((c.owner.as_str(), c.start.as_str(), c.n), ("agent-7", AT, 4));
    assert_eq!(c.id, "claim-4");
}
#[test]
fn s11_only_claim_owner_returns() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    let e = b.tail("agent-8", PK, Some("open"), Some("return")).unwrap_err();
    assert_eq!(e.code(), "conflict");
}
#[test]
fn s11_compute_returns_on_a_foreign_claim_only_in_authorized_recovery() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    assert_eq!(b.tail("compute", PK, Some("open"), Some("return")).unwrap_err().rule(), "S11");
    // provisional 7: the recovery switch stands in for the unrecorded abandonment decision
    b.pol.compute_recovery_return = true;
    assert!(b.tail("compute", PK, Some("open"), Some("return")).is_ok());
}
#[test]
fn wl003_6_1_return_appended_to_same_counter() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    let mut e = b.e("agent-7", Op::Tail, PK);
    e.from = Some("open".into());
    e.to = Some("return".into());
    e.body = Some("## w01\nresult: done\n".into());
    b.apply(e).unwrap();
    let c = b.st.counter(1523, 5, 3).unwrap();
    assert_eq!(c.bodies.len(), 2, "pack text stays, return appended");
}
#[test]
fn s10_builder_cannot_review_own_return() {
    let mut b = with_pack();
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    b.tail("agent-7", PK, Some("open"), Some("return")).unwrap();
    assert_eq!(b.tail("agent-7", PK, Some("return"), Some("review")).unwrap_err().rule(), "S10");
    assert!(b.tail("reviewer", PK, Some("return"), Some("review")).is_ok());
    assert_eq!(b.st.counter(1523, 5, 3).unwrap().reviewer.as_deref(), Some("reviewer"));
}
#[test]
fn s03_close_records_outcome() {
    let mut b = with_pack();
    to_review(&mut b);
    b.close("compute", PK, Some("passed")).unwrap();
    let c = b.st.counter(1523, 5, 3).unwrap();
    assert_eq!((c.tail, c.outcome.as_deref()), (Closed, Some("passed")));
}
#[test]
fn s03_close_needs_outcome() {
    let mut b = with_pack();
    to_review(&mut b);
    assert_eq!(b.close("compute", PK, None).unwrap_err().rule(), "S03");
}
#[test]
fn s03_outcome_must_be_known() {
    let mut b = with_pack();
    to_review(&mut b);
    assert_eq!(b.close("compute", PK, Some("great")).unwrap_err().rule(), "S03");
    for o in ["failed", "blocked", "needs-authority"] {
        let mut b = with_pack();
        to_review(&mut b);
        assert!(b.close("compute", PK, Some(o)).is_ok(), "{o}");
    }
}
#[test]
fn s11_abandoned_needs_system_return() {
    let mut b = with_pack();
    to_review(&mut b);
    assert_eq!(b.close("compute", PK, Some("abandoned")).unwrap_err().rule(), "S11");
    let mut b = with_pack();
    b.pol.compute_recovery_return = true;
    b.tail("agent-7", PK, Some("pack"), Some("open")).unwrap();
    b.tail("compute", PK, Some("open"), Some("return")).unwrap();
    b.tail("reviewer", PK, Some("return"), Some("review")).unwrap();
    assert!(b.close("compute", PK, Some("abandoned")).is_ok());
}
#[test]
fn wl003_6_3_closed_counter_never_reopens() {
    let mut b = with_pack();
    to_review(&mut b);
    b.close("compute", PK, Some("failed")).unwrap();
    assert!(b.tail("x", PK, None, Some("open")).is_err());
    assert!(b.tail("x", PK, None, Some("draft")).is_err());
}
#[test]
fn format_3_3_counter_cannot_be_created_open() {
    let mut b = with_pack();
    assert!(b.put("10.11.21.1523.05.04", Some("open"), "x").is_err());
    assert!(b.put("10.11.21.1523.05.05", Some("review"), "x").is_err());
}
#[test]
fn format_3_3_counter_created_bare_or_draft() {
    let mut b = with_pack();
    b.put("10.11.21.1523.06.01", None, "a note").unwrap();
    assert_eq!(b.st.counter(1523, 6, 1).unwrap().tail, Closed);
    b.put("10.11.21.1523.05.04", Some("draft"), "w").unwrap();
    assert_eq!(b.st.counter(1523, 5, 4).unwrap().tail, Draft);
}
#[test]
fn format_3_3_put_never_replaces_counter() {
    let mut b = with_pack();
    assert!(b.put(PK, Some("pack"), "again").is_err());
}
#[test]
fn d0_put_never_replaces_a_draft_counter() {
    let mut b = with_pack();
    b.put("10.11.21.1523.05.04", Some("draft"), "v1").unwrap();
    assert!(b.put("10.11.21.1523.05.04", Some("draft"), "v2").is_err());
    // provisional switch kept for callers that relied on it
    b.pol.draft_counter_put_replaces = true;
    b.put("10.11.21.1523.05.04", Some("draft"), "v2").unwrap();
    assert_eq!(b.st.counter(1523, 5, 4).unwrap().bodies, vec!["v2".to_string()]);
}
#[test]
fn wl003_6_only_compute_lints_draft_to_pack() {
    let mut b = with_pack();
    b.put("10.11.21.1523.05.04", Some("draft"), "w").unwrap();
    assert_eq!(b.tail("lead", "10.11.21.1523.05.04", Some("draft"), Some("pack")).unwrap_err().rule(), "workflow-loop.003 6");
    assert!(b.tail("compute", "10.11.21.1523.05.04", Some("draft"), Some("pack")).is_ok());
}
#[test]
fn wl003_6_only_compute_closes() {
    let mut b = with_pack();
    to_review(&mut b);
    assert_eq!(b.close("builder", PK, Some("passed")).unwrap_err().rule(), "workflow-loop.003 6");
    assert!(b.close("compute", PK, Some("passed")).is_ok());
}
#[test]
fn s5_7_a_retired_face_is_not_drafted_or_promoted_back() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.op("m", Op::Copy, "10.11.21.1001.04", None, None).unwrap();
    b.tail("u", "10.11.21.1001.04", None, Some("retired")).unwrap();
    assert!(b.op("compute", Op::Promote, "10.11.21.1001.04.draft", None, None).is_err(), "old draft does not re-seat");
    let mut c = Bk::with_identity(B);
    c.put("10.11.21.1001.04", None, "v1").unwrap();
    c.tail("u", "10.11.21.1001.04", None, Some("retired")).unwrap();
    assert!(c.put("10.11.21.1001.04", Some("draft"), "v2").is_err());
}
#[test]
fn r9_counted_face_has_no_door_and_holds_only_counters() {
    let mut b = with_pack();
    assert_eq!(b.put("10.11.21.1523.05.00", None, "x").unwrap_err().rule(), "R9");
    assert_eq!(b.put("10.11.21.1523.05", None, "x").unwrap_err().rule(), "A4.4");
}
#[test]
fn a4_4_board_lists_counters_and_tails() {
    let mut b = with_pack();
    b.put("10.11.21.1523.05.01", None, "done").unwrap();
    b.put("10.11.21.1523.05.02", Some("draft"), "w").unwrap();
    let lines: Vec<(u8, &str)> = b.st.board(1523, 5).iter().map(|l| (l.counter, l.tail.board_word())).collect();
    assert_eq!(lines, [(1, "closed"), (2, "draft"), (3, "pack")]);
}
#[test]
fn a4_4_counters_only_on_counted_faces() {
    let mut b = with_pack();
    assert_eq!(b.put("10.11.21.1523.04.01", None, "x").unwrap_err().rule(), "A4.4");
}
#[test]
fn c8_3_dictionary_0012_03_is_counted() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.0012.00", None, "title: dictionary").unwrap();
    assert!(b.put("10.11.21.0012.03.10", None, "ham.001 -> 10.10.11.1014.01.ham").is_ok());
}
#[test]
fn r9_counters_run_01_to_98_and_ff99_does_not_exist() {
    let mut b = with_pack();
    b.put("10.11.21.1523.05.98", None, "x").unwrap();
    assert_eq!(b.put("10.11.21.1523.05.99", None, "-> 1524").unwrap_err().rule(), "R9");
    assert!(b.st.board(1523, 5).iter().all(|l| (1..=98).contains(&l.counter)));
}
#[test]
fn prov7_door_and_pointer_take_no_tail_move() {
    let mut b = with_pack();
    assert!(b.tail("x", "10.11.21.1523.05.00", None, Some("open")).is_err());
}
#[test]
fn format_3_3_tail_op_names_slot_without_tail() {
    let mut b = with_pack();
    assert!(b.tail("x", "10.11.21.1523.05.03.pack", Some("pack"), Some("open")).is_err());
}
#[test]
fn format_4_1_tail_on_missing_counter_is_missing_axiom_7() {
    let mut b = with_pack();
    let e = b.tail("x", "10.11.21.1523.05.09", Some("pack"), Some("open")).unwrap_err();
    assert_eq!(e.axiom(), Some("7"));
}
#[test]
fn s5_7_seated_face_bare_ff() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "why").unwrap();
    assert_eq!(b.st.face(1001, 4).unwrap().slot_state(), FaceSlotState::Seated);
}
#[test]
fn d0_put_never_replaces_seated_face() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert_eq!(b.put("10.11.21.1001.04", None, "v2").unwrap_err().rule(), "D0");
}
#[test]
fn d0_switch_off_allows_replace() {
    let mut b = Bk::with_identity(B);
    b.pol.enforce_drafting = false;
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert!(b.put("10.11.21.1001.04", None, "v2").is_ok());
}
#[test]
fn drafting_new_face_starts_as_draft() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", Some("draft"), "").unwrap();
    assert_eq!(b.st.face(1001, 4).unwrap().slot_state(), FaceSlotState::DraftOnly);
}
#[test]
fn s5_7_one_draft_per_face() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04.draft", None, "a").unwrap();
    let e = b.put("10.11.21.1001.04", Some("draft"), "b").unwrap_err();
    assert_eq!(e.rule(), "seqAddr 5.7");
}
#[test]
fn a2_5_address_tail_and_field_must_agree() {
    let mut b = Bk::with_identity(B);
    assert!(b.put("10.11.21.1001.04.draft", Some("retired"), "a").is_err());
}
#[test]
fn d0_seated_face_is_drafted_by_copy_not_put() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert_eq!(b.put("10.11.21.1001.04", Some("draft"), "mine").unwrap_err().rule(), "D0");
    b.op("model", Op::Copy, "10.11.21.1001.04", None, None).unwrap();
    let f = b.st.face(1001, 4).unwrap();
    assert_eq!(f.draft.as_ref().unwrap().body, "v1");
    assert_eq!(f.slot_state(), FaceSlotState::SeatedWithDraft);
}
#[test]
fn d0_copy_carries_no_body() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert!(b.op("model", Op::Copy, "10.11.21.1001.04", Some("x"), None).is_err());
}
#[test]
fn d0_copy_needs_seated_face_and_no_draft() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04.draft", None, "a").unwrap();
    assert!(b.op("model", Op::Copy, "10.11.21.1001.04", None, None).is_err());
}
#[test]
fn d0_full_cycle_copy_note_merge_promote() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.op("model", Op::Copy, "10.11.21.1001.04", None, None).unwrap();
    b.op("model", Op::Note, "10.11.21.1001.04.draft", Some("add the why"), None).unwrap();
    let note_n = b.st.last_n;
    b.op("model", Op::Merge, "10.11.21.1001.04.draft", Some("v2"), Some(note_n)).unwrap();
    b.op("compute", Op::Promote, "10.11.21.1001.04.draft", None, None).unwrap();
    let f = b.st.face(1001, 4).unwrap();
    assert_eq!((f.seated.as_deref(), f.draft.is_none()), (Some("v2"), true));
}
#[test]
fn d0_promote_needs_every_note_struck() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.op("model", Op::Copy, "10.11.21.1001.04", None, None).unwrap();
    b.op("model", Op::Note, "10.11.21.1001.04.draft", Some("n"), None).unwrap();
    assert_eq!(b.op("compute", Op::Promote, "10.11.21.1001.04.draft", None, None).unwrap_err().rule(), "D0");
}
#[test]
fn d0_merge_cites_an_open_note() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.op("model", Op::Copy, "10.11.21.1001.04", None, None).unwrap();
    assert!(b.op("model", Op::Merge, "10.11.21.1001.04.draft", Some("v2"), None).is_err());
    assert!(b.op("model", Op::Merge, "10.11.21.1001.04.draft", Some("v2"), Some(99)).is_err());
    b.op("model", Op::Note, "10.11.21.1001.04.draft", Some("n"), None).unwrap();
    let n = b.st.last_n;
    b.op("model", Op::Merge, "10.11.21.1001.04.draft", Some("v2"), Some(n)).unwrap();
    assert!(b.op("model", Op::Merge, "10.11.21.1001.04.draft", Some("v3"), Some(n)).is_err(), "already struck");
}
#[test]
fn d0_note_needs_a_draft() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert_eq!(b.op("m", Op::Note, "10.11.21.1001.04.draft", Some("n"), None).unwrap_err().axiom(), Some("7"));
}
#[test]
fn drafting_new_face_promotes_after_notes() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04.draft", None, "").unwrap();
    b.op("m", Op::Note, "10.11.21.1001.04.draft", Some("write it"), None).unwrap();
    let n = b.st.last_n;
    b.op("m", Op::Merge, "10.11.21.1001.04.draft", Some("text"), Some(n)).unwrap();
    b.op("compute", Op::Promote, "10.11.21.1001.04.draft", None, None).unwrap();
    assert_eq!(b.st.face(1001, 4).unwrap().seated.as_deref(), Some("text"));
}
#[test]
fn s5_7_retire_seated_face() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.tail("u", "10.11.21.1001.04", None, Some("retired")).unwrap();
    assert_eq!(b.st.face(1001, 4).unwrap().slot_state(), FaceSlotState::Retired);
    assert!(b.put("10.11.21.1001.04", None, "v2").is_err(), "retired awaits removal");
}
#[test]
fn s5_7_only_seated_faces_retire() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04.draft", None, "a").unwrap();
    assert!(b.tail("u", "10.11.21.1001.04", None, Some("retired")).is_err());
}
#[test]
fn c1_3_retiring_last_content_face_retires_page() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.00", None, "title: x").unwrap();
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    assert_eq!(b.st.page(1001).unwrap().tail(), seqaddr_core::tail::PageTail::Live);
    b.tail("u", "10.11.21.1001.04", None, Some("retired")).unwrap();
    assert_eq!(b.st.page(1001).unwrap().tail(), seqaddr_core::tail::PageTail::Retired);
}
#[test]
fn c1_2_page_with_only_drafts_is_draft() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.00", None, "title: x").unwrap();
    b.put("10.11.21.1001.04.draft", None, "v1").unwrap();
    assert_eq!(b.st.page(1001).unwrap().tail(), seqaddr_core::tail::PageTail::Draft);
}
#[test]
fn a2_5_page_retired_by_tail_move() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.00", None, "title: x").unwrap();
    b.put("10.11.21.1001.04", None, "v1").unwrap();
    b.tail("u", "10.11.21.1001", None, Some("retired")).unwrap();
    assert_eq!(b.st.page(1001).unwrap().tail(), seqaddr_core::tail::PageTail::Retired);
    assert!(b.tail("u", "10.11.21.1001", None, Some("retired")).is_err());
}
#[test]
fn a4_1_container_retired_through_door_page() {
    let mut b = Bk::with_identity(B);
    b.tail("u", "10.11.21.0000", None, Some("retired")).unwrap();
    assert_eq!(b.st.page(0).unwrap().tail(), seqaddr_core::tail::PageTail::Retired);
}
#[test]
fn format_4_1_identity_page_first() {
    let mut b = Bk::new(B);
    let e = b.put("10.11.21.1001.00", None, "title: x").unwrap_err();
    assert_eq!((e.code(), e.axiom()), ("missing", Some("7")));
    assert!(b.put("10.11.21.0000.00", None, "title: tools").is_ok());
}
#[test]
fn c8_7_use_written_only_by_compute() {
    let mut b = Bk::with_identity(B);
    assert_eq!(b.op("model", Op::Use, "10.11.21.0012.03.ham", Some("ham.001"), None).unwrap_err().rule(), "C8.7");
    b.op("compute", Op::Use, "10.11.21.0012.03.ham", Some("ham.001"), None).unwrap();
    assert_eq!(b.st.uses.len(), 1);
}
#[test]
fn format_3_3_put_needs_a_face() {
    let mut b = Bk::with_identity(B);
    assert!(b.put("10.11.21.1001", None, "x").is_err());
    assert!(b.put("10.11.21.1001.04.ham", None, "x").is_err(), "not a single card");
}

#[test]
fn c1_2_a_page_with_only_draft_counters_is_draft() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.0051.00", Some("draft"), "x").unwrap();
    b.put("10.11.21.0051.06.01", Some("draft"), "a note").unwrap();
    assert_eq!(b.st.page(51).unwrap().tail(), seqaddr_core::tail::PageTail::Draft);
    b.tail("compute", "10.11.21.0051.06.01", Some("draft"), Some("pack")).unwrap();
    assert_eq!(b.st.page(51).unwrap().tail(), seqaddr_core::tail::PageTail::Live);
}
