//! TRIAL-C (1, 3, 5): write rules, tails and finding judged against the spec text.
//! Each failing check is #[ignore = "finding N"]; see docs/trial/core-trial.md.
mod common;
use common::*;
use seqaddr_core::log::Op;
use seqaddr_core::resolve::{Found, Origin};

const W04: &str = "## Job\nwhy: because\n\nThe full explanation.";

fn page(w: &mut World2, addr_page: &str, title: &str) {
    seed(&mut w.0, "compute", vec![put(&format!("{addr_page}.00"), &format!("title: {title}")), put(&format!("{addr_page}.04"), W04)]);
}
struct World2(seqaddr_core::World);

fn pack_world() -> seqaddr_core::World {
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", W04)]);
    seed(&mut w, "lead", vec![put_t("10.11.21.1523.05.01", "pack", "## w01\ntype: work\n")]);
    seed(&mut w, "agent-7", vec![mv("10.11.21.1523.05.01", "pack", "open")]);
    seed(&mut w, "agent-7", vec![mv("10.11.21.1523.05.01", "open", "return")]);
    seed(&mut w, "reviewer", vec![mv("10.11.21.1523.05.01", "return", "review")]);
    w
}

// ---------------- sentinels, desks, pointers ----------------

#[test]
fn desk_book_dd_00_bb_is_a_book_owned_by_the_desk() {
    // seqAddr.md:49; lookup skips the shelf (decisions.md:171 uses real books)
    let mut w = world();
    door(&mut w, "10.00.21");
    let mut w2 = World2(w);
    page(&mut w2, "10.00.00.0030", "x");
    let r = w2.0.resolve(&pa("10.00.21.0030.04")).unwrap();
    assert_eq!((r.origin, r.source.as_deref()), (Origin::Desk, Some("10.00.00.0030.04")));
}

#[test]
#[ignore = "finding 9"]
fn pointer_99_is_never_content() {
    // decisions.md:214 "At every level, 99 is a pointer, never content. ... Its face 08 (map) records each target".
    // A law/why face on 9999 is content.
    let mut w = world();
    let out = propose(&w, "user", vec![put("10.11.21.9999.00", "type: pointer"), put("10.11.21.9999.01", "## Job\nRoute."), put("10.11.21.9999.04", W04)]);
    assert!(!out.approved(), "content faces accepted on the 9999 pointer");
    let _ = &mut w;
}

#[test]
#[ignore = "finding 9"]
fn desk_99_is_a_reserved_pointer_not_a_user_desk() {
    // seqAddr.md:39 `99` "reserved pointer"; decisions.md:260 user environments are 10-98.
    let mut w = world();
    let out = try_seed(&mut w, "user", vec![put("99.10.10.0000.00", "title: d"), put("99.10.10.0000.04", W04)]);
    assert!(!out.approved(), "a book with law/why content was created on desk 99");
}

#[test]
#[ignore = "finding 20"]
fn a_01_card_may_use_the_inherited_04_card() {
    // seqAddr.md:104 / decisions.md:128 books follow the kernel live; axiom 2 "Inherit what is agreed; write only the
    // difference. Do not copy the parent". C3.2 (seqAddr.md:175) asks that the 04 card exist - the core demands a
    // local copy, so overriding one kernel 01 card forces copying the kernel's 04 text into the book.
    let mut w = world();
    seed(&mut w, "compute", vec![put("00.00.00.0030.00", "title: k"), put("00.00.00.0030.01", "## Job\nKernel rule."), put("00.00.00.0030.04", W04)]);
    let out = propose(&w, "u", vec![put("10.11.21.0030.00", "title: b"), put("10.11.21.0030.01", "## Job\nLocal rule.")]);
    assert!(out.approved(), "{:?}", out.reasons);
}

#[test]
fn counters_01_98_then_99_after_98() {
    // seqAddr.md:24, decisions.md:201
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", W04)]);
    assert!(!propose(&w, "u", vec![put("10.11.21.1523.06.00", "x")]).approved(), "00 is the board");
    assert!(!propose(&w, "u", vec![put("10.11.21.1523.06.99", "x")]).approved(), "99 before 98");
    seed(&mut w, "u", vec![put("10.11.21.1523.06.01", "n")]);
    seed(&mut w, "u", vec![put("10.11.21.1523.06.98", "n")]);
    assert!(propose(&w, "u", vec![put("10.11.21.1523.06.99", "-> 10.11.21.1524")]).approved());
}

// ---------------- tails on every face type ----------------

#[test]
fn tails_on_every_face_type() {
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.0012.00", "title: dictionary"), put("10.11.21.0012.04", W04)]);
    // seated faces 01,02,04,08 take draft (new) and retire from seated
    for f in ["01", "02", "04", "08"] {
        let pg = format!("10.11.21.10{f}");
        let body = if f == "01" || f == "02" { "## Job\nx" } else { "## Job\nwhy: y\n\nz" };
        let mut ops = vec![put(&format!("{pg}.00"), "title: t"), put_t(&format!("{pg}.{f}"), "draft", body)];
        if f == "01" || f == "02" {
            ops.push(put(&format!("{pg}.04"), W04));
        }
        let out = try_seed(&mut w, "u", ops);
        assert!(out.approved(), "{f}: {:?}", out.reasons);
        // workflow tails never on a face
        for t in ["pack", "open", "return", "review"] {
            assert!(!propose(&w, "u", vec![put_t(&format!("{pg}.{f}"), t, "x")]).approved(), "{f}.{t}");
        }
    }
    // counted faces 05/06 and 0012.03: no seated face, no FF.draft, no FF.retired
    for a in ["10.11.21.1523.05", "10.11.21.1523.06", "10.11.21.0012.03"] {
        assert!(!propose(&w, "u", vec![put_t(a, "draft", "x")]).approved(), "{a}.draft");
        assert!(!propose(&w, "u", vec![put(a, "x")]).approved(), "{a} seated");
    }
    // counters: retired never (seqAddr.md:287)
    assert!(!propose(&w, "u", vec![put_t("10.11.21.0012.03.10", "retired", "x")]).approved());
}

#[test]
#[ignore = "finding 2"]
fn a_new_face_is_not_seated_without_draft_and_review() {
    // drafting.md:180 "A brand-new face ... starts as an empty draft and still goes through notes and merges";
    // seqAddr.md:201 FF.draft is the unseated face; axiom 9 / decisions.md:588 "Nothing is promoted until it has
    // faced a hostile pass". A bare `put` seats (promotes) a new face in one step.
    let w = world();
    let out = propose(&w, "model", vec![put("10.11.21.1600.00", "title: t"), put("10.11.21.1600.04", W04)]);
    assert!(!out.approved(), "new face 04 seated directly by a model with no draft or review");
}

#[test]
#[ignore = "finding 3"]
fn promote_needs_a_review_by_someone_other_than_the_drafter() {
    // format.md:97 / drafting.md:191 "promote: after review"; decisions.md:588 (E7, settled):
    // "Nothing is promoted until it has faced a hostile pass from a view other than its maker's."
    let mut w = world();
    seed(&mut w, "model", vec![put("10.11.21.1600.00", "title: t"), put_t("10.11.21.1600.04", "draft", W04)]);
    let out = propose(&w, "model", vec![op(Op::Promote, "10.11.21.1600.04.draft")]);
    assert!(!out.approved(), "the drafter promoted its own draft with no review recorded");
}

#[test]
#[ignore = "finding 10"]
fn a_retired_face_is_not_reseated_through_a_draft() {
    // seqAddr.md:201 `FF.retired` is "a previously seated face awaiting removal"; the core already refuses a bare put
    // on it (state.rs:421). A put of FF.draft and a promote re-seat it anyway and wipe the retired body from state.
    let mut w = world();
    seed(&mut w, "u", vec![put("10.11.21.1600.00", "title: t"), put("10.11.21.1600.04", W04), put("10.11.21.1600.08", "## l\ntarget: 10.11.21.0000\n")]);
    seed(&mut w, "u", vec![mv("10.11.21.1600.04", "", "retired")]);
    let out = try_seed(&mut w, "u", vec![put_t("10.11.21.1600.04", "draft", W04)]);
    if out.approved() {
        let out = propose(&w, "u", vec![op(Op::Promote, "10.11.21.1600.04.draft")]);
        assert!(!out.approved(), "retired face re-seated by draft + promote");
    }
}

// ---------------- workflow loop (wl.003 section 6) ----------------

#[test]
#[ignore = "finding 4"]
fn only_compute_closes_and_not_the_builder() {
    // workflow-loop.003.md:174 step 7 Close "Who: Compute"; :175 step 6 review by a valid reviewer;
    // S10 "The builder is ineligible to review its own return" (wl.003 6.3).
    let w = pack_world();
    let out = propose(&w, "agent-7", vec![close("10.11.21.1523.05.01", "passed")]);
    assert!(!out.approved(), "the builder closed its own reviewed work as passed");
}

#[test]
#[ignore = "finding 4"]
fn only_compute_lints_draft_to_pack() {
    // workflow-loop.003.md:170 step 2 Lint `draft -> pack` "Who: compute ... A pack that fails stays draft".
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", W04)]);
    seed(&mut w, "lead", vec![put_t("10.11.21.1523.05.02", "draft", "anything at all")]);
    let out = propose(&w, "lead", vec![mv("10.11.21.1523.05.02", "draft", "pack")]);
    assert!(!out.approved(), "the lead moved its own pack past lint with no template check");
}

#[test]
#[ignore = "finding 11"]
fn compute_returns_only_during_authorized_recovery() {
    // workflow-loop.003.md:173 step 5 "Compute during authorized recovery"; 6.4: "Silence alone leaves the claim
    // unresolved. After the required authority records an abandonment decision, Compute fences the old claim".
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", W04)]);
    seed(&mut w, "lead", vec![put_t("10.11.21.1523.05.01", "pack", "w")]);
    seed(&mut w, "agent-7", vec![mv("10.11.21.1523.05.01", "pack", "open")]);
    let out = propose(&w, "compute", vec![mv("10.11.21.1523.05.01", "open", "return")]);
    assert!(!out.approved(), "compute took over a live claim with no abandonment decision recorded");
}

#[test]
fn claim_rules_hold() {
    let mut w = world();
    seed(&mut w, "compute", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", W04)]);
    seed(&mut w, "lead", vec![put_t("10.11.21.1523.05.01", "pack", "w")]);
    seed(&mut w, "agent-7", vec![mv("10.11.21.1523.05.01", "pack", "open")]);
    let o = propose(&w, "agent-8", vec![mv("10.11.21.1523.05.01", "pack", "open")]);
    assert_eq!(o.reasons[0].code, "conflict");
    assert!(!propose(&w, "agent-8", vec![mv("10.11.21.1523.05.01", "open", "return")]).approved(), "foreign return");
    assert!(!propose(&w, "agent-7", vec![mv("10.11.21.1523.05.01", "open", "review")]).approved(), "skip");
    // one proposal cannot make the builder its own reviewer either
    assert!(!propose(&w, "agent-7", vec![mv("10.11.21.1523.05.01", "open", "return"), mv("10.11.21.1523.05.01", "return", "review")]).approved());
}

// ---------------- finding (resolution) ----------------

#[test]
fn resolution_order_book_shelf_desk_kernel() {
    // seqAddr.md:101 book -> shelf -> desk -> kernel, first match wins
    let mut w = World2(world());
    page(&mut w, "00.00.00.0030", "k");
    let r = w.0.resolve(&pa("10.11.21.0030.04")).unwrap();
    assert_eq!(r.origin, Origin::Kernel);
    page(&mut w, "10.00.00.0030", "d");
    assert_eq!(w.0.resolve(&pa("10.11.21.0030.04")).unwrap().origin, Origin::Desk);
    page(&mut w, "10.11.00.0030", "s");
    assert_eq!(w.0.resolve(&pa("10.11.21.0030.04")).unwrap().origin, Origin::Shelf);
    page(&mut w, "10.11.21.0030", "b");
    assert_eq!(w.0.resolve(&pa("10.11.21.0030.04")).unwrap().origin, Origin::Local);
    let steps: Vec<String> = w.0.resolve(&pa("10.11.21.0031.04")).unwrap().trace.iter().map(|s| s.checked.clone()).collect();
    assert_eq!(steps, ["10.11.21.0031.04", "10.11.00.0031.04", "10.00.00.0031.04", "00.00.00.0031.04"]);
}

#[test]
fn a_local_draft_does_not_shadow_and_a_kernel_draft_is_not_inherited() {
    // seqAddr.md:133 draft "being written; not active"; seqAddr.md:104 first match wins (live)
    let mut w = world();
    seed(&mut w, "compute", vec![put("00.00.00.0030.00", "title: k"), put_t("00.00.00.0030.04", "draft", W04), put("00.00.00.0030.08", "## l\ntarget: 00.00.00.0000\n")]);
    let r = w.resolve(&pa("10.11.21.0030.04")).unwrap();
    assert_eq!(r.origin, Origin::Missing);
    seed(&mut w, "compute", vec![put("10.00.00.0030.00", "title: d"), put("10.00.00.0030.04", W04)]);
    seed(&mut w, "u", vec![put("10.11.21.0030.00", "title: b"), put_t("10.11.21.0030.04", "draft", W04)]);
    let r = w.resolve(&pa("10.11.21.0030.04")).unwrap();
    assert_eq!(r.origin, Origin::Desk, "local draft is not live, the desk's seated face is found");
}

#[test]
#[ignore = "finding 6"]
fn a_kernel_draft_counter_is_not_inherited() {
    // API.md:122 "Drafts and retired faces are never inherited"; decisions.md:277 counts `05.01.draft` as a draft face.
    // A bare counter address walks the chain and returns the kernel's counter whatever its tail.
    let mut w = world();
    seed(&mut w, "compute", vec![put("00.00.00.0057.00", "title: wl"), put("00.00.00.0057.04", W04)]);
    seed(&mut w, "compute", vec![put_t("00.00.00.0057.05.01", "draft", "kernel pack being written")]);
    let r = w.resolve(&pa("10.11.21.0057.05.01")).unwrap();
    assert!(!matches!(r.found, Some(Found::Counter { .. })), "book inherits the kernel's draft task: {:?} from {:?}", r.found, r.source);
    let r = w.resolve(&pa("10.11.21.0057.05")).unwrap();
    assert!(r.found.is_none(), "book shows the kernel's task board as its own: {:?}", r.source);
}

#[test]
#[ignore = "finding 7"]
fn a_retired_page_is_not_live() {
    // seqAddr.md:138 retired "previously seated, retired before removal"; axiom 1: "location, state, and a lawful
    // connection decide what is live". A page retired by `PPPP.retired` still answers as live and shadows the kernel.
    let mut w = World2(world());
    page(&mut w, "00.00.00.0030", "k");
    page(&mut w, "10.11.21.0030", "b");
    seed(&mut w.0, "u", vec![mv("10.11.21.0030", "", "retired")]);
    let r = w.0.resolve(&pa("10.11.21.0030.04")).unwrap();
    assert_ne!(r.origin, Origin::Local, "retired page still served as the live local face");
}

#[test]
#[ignore = "finding 8"]
fn kernel_only_cards_cannot_be_redefined_by_a_book() {
    // decisions.md:287 types are cards "marked `owner: kernel-only`, so no book can redefine it"; seqAddr.md:193.
    let mut w = world();
    seed(&mut w, "compute", vec![put("00.00.00.0054.00", "title: types"), put("00.00.00.0054.01", "## General\nowner: kernel-only\n\nThe general type."), put("00.00.00.0054.04", "## General\nwhy: w\n\nlong")]);
    let out = propose(&w, "model", vec![put("10.11.21.0054.00", "title: types"), put("10.11.21.0054.01", "## General\nowner: book\n\nMy own general type."), put("10.11.21.0054.04", "## General\nwhy: w\n\nlong")]);
    assert!(!out.approved(), "a book redefined a kernel-only card");
}

#[test]
#[ignore = "finding 12"]
fn back_link_must_be_live_not_a_draft() {
    // decisions.md:230 / axiom 8: a connection is lawful only when written; seqAddr.md:133 a draft is not active.
    let mut w = world();
    seed(&mut w, "u", vec![put("10.11.22.0000.00", "title: next"), put_t("10.11.22.0000.08", "draft", "## back\ntarget: 10.11.21.9999\nkind: continuation")]);
    let out = propose(&w, "u", vec![put("10.11.21.9999.00", "type: pointer"), put("10.11.21.9999.08", "## next\ntarget: 10.11.22.0000\nkind: continuation")]);
    assert!(!out.approved(), "a draft back-link satisfied A5.3");
}

#[test]
#[ignore = "finding 12"]
fn retiring_a_back_link_does_not_leave_a_one_way_link() {
    // decisions.md:230 "A link that only goes one way is a validation error."
    let mut w = world();
    seed(&mut w, "u", vec![put("10.11.22.0000.00", "title: next"), put("10.11.22.0000.04", W04), put("10.11.22.0000.08", "## back\ntarget: 10.11.21.9999\nkind: continuation")]);
    seed(&mut w, "u", vec![put("10.11.21.9999.00", "type: pointer"), put("10.11.21.9999.08", "## next\ntarget: 10.11.22.0000\nkind: continuation")]);
    let out = propose(&w, "u", vec![mv("10.11.22.0000.08", "", "retired")]);
    assert!(!out.approved(), "back-link retired; 10.11.21.9999 now links one way");
}

#[test]
#[ignore = "finding 13"]
fn pages_1000_and_up_need_a_title_including_9999() {
    // seqAddr.md:115 / decisions.md:131 "Pages 1000 and up must have a title" - no exception for 9999 is written;
    // validate.rs:233 exempts 9999 without a BUILD-LOG `7`.
    let mut w = world();
    seed(&mut w, "u", vec![put("10.11.22.0000.00", "title: next"), put("10.11.22.0000.04", W04), put("10.11.22.0000.08", "## back\ntarget: 10.11.21.9999\nkind: continuation")]);
    let out = propose(&w, "u", vec![put("10.11.21.9999.00", "type: pointer"), put("10.11.21.9999.08", "## next\ntarget: 10.11.22.0000\nkind: continuation")]);
    assert!(!out.approved(), "9999 accepted with no title and no 7 recorded");
}

#[test]
fn c3_2_and_c1_1_hold_on_counters_and_drafts() {
    let w = world();
    // 01 card with no 04 card: rejected even as drafts
    let out = propose(&w, "u", vec![put("10.11.21.1600.00", "title: t"), put_t("10.11.21.1600.01", "draft", "## Job\nRoute.")]);
    assert!(!out.approved());
    // door + only face 07: no content face
    assert!(!propose(&w, "u", vec![put("10.11.21.1600.00", "title: t"), put("10.11.21.1600.07", "x")]).approved());
}
