//! Inheritance (A1.8, A2.9, A4.1), proposals (format 3.3, 4.1), cards (C2, C3, C8.9), axioms (E3).
mod common;
use common::*;
use seqaddr_core::cards::{parse_face, parse_stamp, title_form};
use seqaddr_core::log::Op;
use seqaddr_core::resolve::{Found, Origin};
use seqaddr_core::validate::{validate, OpRequest, Proposal};
use seqaddr_core::{Active, Address, AxiomChain, Policy, World};

fn book(addr: &str, puts: &[(&str, &str)]) -> seqaddr_core::BookState {
    let mut b = Bk::with_identity(addr);
    for (a, body) in puts {
        b.put(&format!("{addr}.{a}"), None, body).unwrap();
    }
    b.st
}
fn world() -> World {
    let mut w = World::new(Policy::default());
    w.insert(book("00.00.00", &[("0020.00", "title: k"), ("0020.01", "kernel law"), ("0021.00", "x"), ("0021.04", "kernel why")]));
    w.insert(book("10.00.00", &[("0021.00", "x"), ("0021.04", "desk why")]));
    w.insert(book("10.11.00", &[]));
    w.insert(book("10.11.21", &[("0020.00", "t"), ("0020.04", "local why"), ("1001.00", "title: timer"), ("1001.04", "w")]));
    w
}
fn p(s: &str) -> seqaddr_core::PageAddr {
    Address::parse_full_page(s).unwrap()
}
/// Requests in these tests carry the Director's approval, so seating rules (R2) stay out of the way;
/// `bare_req` carries none.
fn req(op: Op, addr: &str, body: Option<&str>) -> OpRequest {
    OpRequest { approved_by: Some("director".into()), ..bare_req(op, addr, body) }
}
fn bare_req(op: Op, addr: &str, body: Option<&str>) -> OpRequest {
    OpRequest { op: Some(op), addr: addr.into(), body: body.map(|s| s.into()), ..Default::default() }
}
fn prop(by: &str, ops: Vec<OpRequest>) -> Proposal {
    Proposal { by: by.into(), ops }
}

// ---------- inheritance ----------
#[test]
fn a1_8_local_wins() {
    let r = world().resolve(&p("10.11.21.0020.04")).unwrap();
    assert_eq!(r.origin, Origin::Local);
    assert_eq!(r.found, Some(Found::Face { body: "local why".into() }));
}
#[test]
fn a2_9_unoverridden_face_found_in_kernel() {
    let r = world().resolve(&p("10.11.21.0020.01")).unwrap();
    assert_eq!(r.origin, Origin::Kernel);
    assert_eq!(r.source.as_deref(), Some("00.00.00.0020.01"));
}
#[test]
fn a1_8_desk_before_kernel() {
    let r = world().resolve(&p("10.11.21.0021.04")).unwrap();
    assert_eq!((r.origin, r.source.as_deref()), (Origin::Desk, Some("10.00.00.0021.04")));
}
#[test]
fn a1_8_trace_lists_each_step() {
    let r = world().resolve(&p("10.11.21.0020.01")).unwrap();
    let steps: Vec<(&str, bool)> = r.trace.iter().map(|s| (s.checked.as_str(), s.found)).collect();
    assert_eq!(steps, [("10.11.21.0020.01", false), ("10.11.00.0020.01", false), ("10.00.00.0020.01", false), ("00.00.00.0020.01", true)]);
}
#[test]
fn a1_8_not_found_is_elevated_never_guessed_axiom_7() {
    let r = world().resolve(&p("10.11.21.0030.01")).unwrap();
    assert_eq!((r.origin, r.found.is_none()), (Origin::Missing, true));
    assert_eq!(r.trace.len(), 4);
    let e = r.into_result().unwrap_err();
    assert_eq!(e.axiom(), Some("7"));
}
#[test]
fn a1_8_missing_book_in_chain_is_a_step_not_an_error() {
    let mut w = world();
    w.books.remove(&seqaddr_core::BookId::parse("10.11.00").unwrap());
    let r = w.resolve(&p("10.11.21.0020.01")).unwrap();
    assert_eq!(r.trace[1].note.as_deref(), Some("no book"));
    assert_eq!(r.origin, Origin::Kernel);
}
#[test]
fn r5_a_draft_alone_is_found_and_inherited_as_a_draft() {
    let mut w = world();
    let mut k = Bk::with_identity("00.00.00");
    k.put("00.00.00.0050.00", None, "x").unwrap();
    k.put("00.00.00.0050.01.draft", None, "draft law").unwrap();
    w.insert(k.st);
    let r = w.resolve(&p("10.11.21.0050.01")).unwrap();
    assert_eq!((r.origin, r.state.as_deref()), (Origin::Kernel, Some("draft")));
    assert_eq!(r.found, Some(Found::Draft { body: "draft law".into() }));
    let r = w.resolve(&p("00.00.00.0050.01.draft")).unwrap();
    assert_eq!(r.found, Some(Found::Draft { body: "draft law".into() }));
}
#[test]
fn r5_seated_beats_draft_at_the_same_spot() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    b.put("10.11.22.1001.04", None, "seated").unwrap();
    b.op("m", Op::Copy, "10.11.22.1001.04", None, None).unwrap();
    w.insert(b.st);
    let r = w.resolve(&p("10.11.22.1001.04")).unwrap();
    assert_eq!((r.found, r.state.as_deref()), (Some(Found::Face { body: "seated".into() }), Some("seated")));
}
#[test]
fn r5_a_local_draft_is_found_before_an_inherited_seated_face() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.0021.00", None, "x").unwrap();
    b.put("10.11.22.0021.04.draft", None, "local draft").unwrap();
    w.insert(b.st);
    let r = w.resolve(&p("10.11.22.0021.04")).unwrap();
    assert_eq!((r.origin, r.state.as_deref()), (Origin::Local, Some("draft")));
}
#[test]
fn axiom_1_a_retired_page_is_skipped_and_the_walk_goes_on() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.0021.00", None, "x").unwrap();
    b.put("10.11.22.0021.04", None, "local").unwrap();
    b.tail("u", "10.11.22.0021", None, Some("retired")).unwrap();
    w.insert(b.st);
    let r = w.resolve(&p("10.11.22.0021.04")).unwrap();
    assert_eq!(r.origin, Origin::Desk);
    assert_eq!(r.trace[0].note.as_deref(), Some("retired page"));
}
#[test]
fn a4_1_a_book_retired_at_its_door_is_not_live() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.0021.00", None, "x").unwrap();
    b.put("10.11.22.0021.04", None, "local").unwrap();
    b.tail("u", "10.11.22.0000", None, Some("retired")).unwrap();
    w.insert(b.st);
    assert_eq!(w.resolve(&p("10.11.22.0021.04")).unwrap().origin, Origin::Desk);
}
#[test]
fn r9_plain_ff_on_counted_face_reads_the_derived_listing() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1523.00", None, "title: t").unwrap();
    b.put("10.11.22.1523.05.01", Some("pack"), "w").unwrap();
    w.insert(b.st);
    match w.resolve(&p("10.11.22.1523.05")).unwrap().found {
        Some(Found::Board { lines }) => assert_eq!(lines.len(), 1),
        other => panic!("{other:?}"),
    }
    assert_eq!(seqaddr_core::Address::parse("10.11.22.1523.05.00").unwrap_err().rule(), "R9");
    assert!(matches!(w.resolve(&p("10.11.22.1523.05.01")).unwrap().found, Some(Found::Counter { .. })));
}
#[test]
fn a1_2_resolve_short_form_against_active_book() {
    let act = Active { book: seqaddr_core::BookId::parse("10.11.21").unwrap(), pages: vec![20] };
    let r = world().resolve_str("0020.01", Some(&act)).unwrap();
    assert_eq!(r.address, "10.11.21.0020.01");
    let r = world().resolve_str(".04", Some(&act)).unwrap();
    assert_eq!(r.origin, Origin::Local);
}
#[test]
fn a1_7_resolve_short_without_active_is_invalid() {
    assert!(world().resolve_str("0020.01", None).is_err());
}
#[test]
fn a1_8_resolve_page_merges_local_and_inherited() {
    let m = world().resolve_page(&p("10.11.21.0020")).unwrap();
    assert_eq!(m.get(&4).unwrap().origin, Origin::Local);
    assert_eq!(m.get(&1).unwrap().origin, Origin::Kernel);
}
#[test]
fn a2_8_title_in_address_checked_against_stamp() {
    let w = world();
    assert!(w.check_title(&p("10.11.21.1001.timer")).is_ok());
    assert_eq!(w.check_title(&p("10.11.21.1001.clock")).unwrap_err().code(), "elevate");
    assert!(w.check_title(&p("10.11.21.1001")).is_ok());
}

// ---------- proposals ----------
#[test]
fn format_4_1_proposal_approved_returns_entries() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: clock")), req(Op::Put, "10.11.21.1002.04", Some("why"))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
    assert_eq!(out.entry_numbers.len(), 2);
    assert_eq!(out.entries[0].proposal, out.entries[1].proposal);
    assert_eq!(out.entries[1].of, Some(2));
}
#[test]
fn format_3_3_all_or_nothing() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: clock")), req(Op::Put, "10.11.21.1001.04", Some("replace"))]), AT);
    assert!(!out.approved());
    assert!(out.entries.is_empty() && out.state.is_none());
    assert_eq!(out.reasons[0].op, Some(1));
}
#[test]
fn c1_1_page_needs_door_and_content_face() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: clock"))]), AT);
    assert_eq!(out.reasons[0].rule, "C1.1");
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.04", Some("why"))]), AT);
    assert_eq!(out.reasons[0].rule, "C1.1");
}
#[test]
fn c1_1_face_07_does_not_count() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.07", Some("x"))]), AT);
    assert!(!out.approved());
}
#[test]
fn a4_3_reserved_faces_rejected() {
    let w = world();
    for f in ["07", "09", "10", "99"] {
        let out = validate(&w, &prop("user", vec![req(Op::Put, &format!("10.11.21.1001.{f}"), Some("x"))]), AT);
        assert_eq!(out.reasons[0].rule, "A4.3", "{f}");
    }
}
#[test]
fn c1_2_draft_faces_count() {
    let w = world();
    let mut r = req(Op::Put, "10.11.21.1002.04", Some(""));
    r.tail = Some("draft".into());
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), r]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn a2_8_pages_1000_up_need_title_in_stamp() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("type: general")), req(Op::Put, "10.11.21.1002.04", Some("w"))]), AT);
    assert_eq!(out.reasons[0].rule, "A2.8");
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.0030.00", Some("type: general")), req(Op::Put, "10.11.21.0030.04", Some("w"))]), AT);
    assert!(out.approved(), "0001-0999 may have no title: {:?}", out.reasons);
}
#[test]
fn a2_3_stamp_title_characters() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: Big Clock")), req(Op::Put, "10.11.21.1002.04", Some("w"))]), AT);
    assert_eq!(out.reasons[0].rule, "A2.3");
}
#[test]
fn c1_4_unknown_page_type_rejected() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c\ntype: fancy")), req(Op::Put, "10.11.21.1002.04", Some("w"))]), AT);
    assert_eq!(out.reasons[0].rule, "C1.4");
}
#[test]
fn c3_2_01_card_needs_04_card() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.01", Some("## Job\nRoute."))]), AT);
    assert_eq!(out.reasons[0].rule, "C3.2");
}
#[test]
fn c3_2_04_card_needs_why_and_body() {
    let w = world();
    let ops = |w04: &str| prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.01", Some("## Job\nRoute.")), req(Op::Put, "10.11.21.1002.04", Some(w04))]);
    assert_eq!(validate(&w, &ops("## Job\nsource: [01 / Job]\n\nlong text"), AT).reasons[0].rule, "C3.2");
    assert_eq!(validate(&w, &ops("## Job\nwhy: because\n"), AT).reasons[0].rule, "C3.2");
    let ok = validate(&w, &ops("## Job\nsource: [01 / Job]\nwhy: Routing should reduce reading.\n\nThe full explanation."), AT);
    assert!(ok.approved(), "{:?}", ok.reasons);
}
#[test]
fn c3_2_04_copying_01_is_a_finding_not_rejection() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.01", Some("## Job\nRoute.")), req(Op::Put, "10.11.21.1002.04", Some("## Job\nwhy: x\n\nRoute."))]), AT);
    assert!(out.approved());
    assert_eq!(out.findings[0].rule, "C3.2");
}
#[test]
fn c8_9_brand_cards_need_no_04() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.01", Some("## ham\ntype: brand\nbrand: ham.001\nmeans: friend"))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn c8_9_unknown_card_type_is_finding() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.04", Some("## Odd\ntype: gizmo\n\nx"))]), AT);
    assert!(out.approved());
    assert_eq!(out.findings[0].rule, "C8.9");
}
#[test]
fn c8_7_meters_written_only_by_compute() {
    let w = world();
    let out = validate(&w, &prop("model", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.01", Some("## ham\ntype: brand\nmeters: sandwich 100%"))]), AT);
    assert_eq!(out.reasons[0].rule, "C8.7");
}
#[test]
fn e2_axioms_field_must_parse() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c\naxioms: 1.7.8")), req(Op::Put, "10.11.21.1002.04", Some("## A\naxioms: 3X\n\nx"))]), AT);
    assert_eq!(out.reasons[0].rule, "E3");
}
#[test]
fn c2_duplicate_card_keys_rejected() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.04", Some("## Retry Policy\nx\n## retry policy\ny"))]), AT);
    assert_eq!(out.reasons[0].rule, "C2");
}
#[test]
fn c6_face_03_only_on_reserved_pages_in_normal_books() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.03", Some("menu"))]), AT);
    assert_eq!(out.reasons[0].rule, "C6");
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.0030.00", Some("t: x")), req(Op::Put, "10.11.21.0030.03", Some("menu"))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn c6_face_03_anywhere_in_kernel_and_desk_books() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.00.00.1002.00", Some("title: c")), req(Op::Put, "10.00.00.1002.03", Some("menu"))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn a1_7_proposals_use_full_addresses() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "1002.04", Some("w"))]), AT);
    assert_eq!(out.reasons[0].rule, "A1.7");
}
#[test]
fn format_3_4_snapshot_not_proposable() {
    let w = world();
    let out = validate(&w, &prop("compute", vec![req(Op::Snapshot, "10.11.21.0000.00", None)]), AT);
    assert!(!out.approved());
}
#[test]
fn format_3_3_one_book_per_proposal() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.04", Some("w")), req(Op::Put, "10.00.00.1002.04", Some("w"))]), AT);
    assert!(!out.approved());
}
#[test]
fn format_4_1_new_book_starts_with_door() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.30.0000.00", Some("title: new"))]), AT);
    assert!(out.approved(), "R10: a door page needs only face 00: {:?}", out.reasons);
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.31.1001.00", Some("title: x"))]), AT);
    assert_eq!(out.reasons[0].axiom.as_deref(), Some("7"));
}
#[test]
fn format_2_second_claim_in_queue_is_conflict_409() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1523.00", None, "title: t").unwrap();
    b.put("10.11.22.1523.05.01", Some("pack"), "w").unwrap();
    w.insert(b.st);
    let claim = || {
        let mut r = req(Op::Tail, "10.11.22.1523.05.01", None);
        r.from = Some("pack".into());
        r.to = Some("open".into());
        r
    };
    let first = validate(&w, &prop("agent-7", vec![claim()]), AT);
    assert!(first.approved());
    w.insert(first.state.unwrap());
    let second = validate(&w, &prop("agent-8", vec![claim()]), AT);
    assert_eq!(second.reasons[0].code, "conflict");
    assert_eq!(second.reasons[0].axiom.as_deref(), Some("1"));
}
#[test]
fn a5_3_pointer_needs_back_link() {
    let w = world();
    let link = "## next\ntype: link\ntarget: 10.11.22.0000\nkind: continuation";
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.9999.00", Some("title: next\ntype: pointer")), req(Op::Put, "10.11.21.9999.08", Some(link))]), AT);
    assert_eq!(out.reasons[0].rule, "A5.3");
    let mut w = world();
    // R10: the door page holds only face 00, so a door's back-link is a `target:` line in its registry (7).
    let mut t = Bk::new("10.11.22");
    t.put("10.11.22.0000.00", None, "---\ntitle: tools\ntarget: 10.11.21.9999\n---").unwrap();
    w.insert(t.st);
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.9999.00", Some("title: next\ntype: pointer")), req(Op::Put, "10.11.21.9999.08", Some(link))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn a5_3_band_continuation_pp99_is_a_pointer_too() {
    let w = world();
    let link = "## next\ntarget: 10.11.21.2100\nkind: continuation";
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1099.00", Some("title: more")), req(Op::Put, "10.11.21.1099.08", Some(link))]), AT);
    assert_eq!(out.reasons[0].rule, "A5.3");
}
#[test]
fn format_4_1_reasons_carry_rule_and_op_index() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1001.04", Some("again"))]), AT);
    let r = &out.reasons[0];
    assert_eq!((r.rule.as_str(), r.op, r.code.as_str()), ("D0", Some(0), "rejected"));
    let j = serde_json::to_value(&out).unwrap();
    assert_eq!(j["status"], "rejected");
}
#[test]
fn format_4_1_empty_proposal_rejected() {
    assert!(!validate(&world(), &prop("user", vec![]), AT).approved());
    assert!(!validate(&world(), &prop("", vec![req(Op::Put, "10.11.21.1002.04", Some("w"))]), AT).approved());
}
#[test]
fn format_4_1_validation_does_not_change_world() {
    let w = world();
    let before = w.get(seqaddr_core::BookId::parse("10.11.21").unwrap()).unwrap().clone();
    let _ = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.04", Some("w"))]), AT);
    assert_eq!(w.get(before.book).unwrap(), &before);
}

// ---------- cards and stamps ----------
#[test]
fn c2_key_is_heading_in_title_form() {
    assert_eq!(title_form("Retry Policy").unwrap(), "retry-policy");
    assert_eq!(title_form("w01").unwrap(), "w01");
    assert!(title_form("1. Intro").is_err());
    assert!(title_form("Draft").is_err(), "tail words are not card keys");
}
#[test]
fn s5_3_fields_then_blank_then_body() {
    let d = parse_face("intro\n## Job\nsource: [01 / Job]\nwhy: Routing.\n\nFull text\nmore: not a field\n## Next\nbody").unwrap();
    assert_eq!(d.contents(), ["job", "next"]);
    let c = d.card("job").unwrap();
    assert_eq!(c.field("why"), Some("Routing."));
    assert_eq!(c.body, "Full text\nmore: not a field");
    assert_eq!(d.preamble, "intro\n");
}
#[test]
fn c8_9_card_type_from_field_or_face_default() {
    let d = parse_face("## A\ntype: brand\n\nx\n## B\nx").unwrap();
    assert_eq!(d.card("a").unwrap().card_type(1).as_deref(), Some("brand"));
    assert_eq!(d.card("b").unwrap().card_type(1).as_deref(), Some("rule"));
}
#[test]
fn c2_headings_in_code_fences_are_not_cards() {
    let d = parse_face("## A\n```\n## not a card\n```\n").unwrap();
    assert_eq!(d.contents(), ["a"]);
}
#[test]
fn wl003_5_1_field_names_may_have_spaces() {
    let d = parse_face("## w01\ntype: work\nstop if: tests fail\n").unwrap();
    assert_eq!(d.card("w01").unwrap().field("stop if"), Some("tests fail"));
}
#[test]
fn a4_2_stamp_front_matter_or_fields() {
    assert_eq!(parse_stamp("---\ntitle: tools\n---").title(), Some("tools"));
    let s = parse_stamp("title: clock\ntype: code\n\nbody");
    assert_eq!((s.title(), s.page_type()), (Some("clock"), Some("code")));
}

// ---------- axiom chains ----------
#[test]
fn e3_dot_orders_comma_splits() {
    let c = AxiomChain::parse("1.7.8,3").unwrap();
    assert_eq!(c.pieces.len(), 2);
    assert_eq!(c.pieces[0].iter().map(|r| r.n).collect::<Vec<_>>(), [1, 7, 8]);
    assert_eq!(c.to_string(), "1.7.8,3");
}
#[test]
fn e3_only_axiom_3_takes_lead_letters() {
    assert_eq!(AxiomChain::parse("3MPC").unwrap().pieces[0][0].leads, ['M', 'P', 'C']);
    assert!(AxiomChain::parse("4M").is_err());
    assert!(AxiomChain::parse("3MM").is_err());
    assert!(AxiomChain::parse("3X").is_err());
    assert!(AxiomChain::parse("3MPCM").is_err());
}
#[test]
fn e3_axioms_are_one_digit_1_to_9() {
    assert!(AxiomChain::parse("0").is_err());
    assert!(AxiomChain::parse("10").is_err());
    assert!(AxiomChain::parse("1..7").is_err());
    assert!(AxiomChain::parse("").is_err());
}
#[test]
fn e3_order_is_meaning_7_8_vs_8_7() {
    assert_eq!(AxiomChain::parse("7.8").unwrap().describe(), "Missing > Connection");
    assert_eq!(AxiomChain::parse("8.7").unwrap().describe(), "Connection > Missing");
    assert_eq!(AxiomChain::parse(seqaddr_core::axioms::COLD_SET).unwrap().describe(), "Authority > Missing > Connection");
}

// ---------- seating (R2, E7, drafting.md:20) ----------
#[test]
fn drafting_20_a_new_face_is_not_seated_by_a_bare_put_without_approval() {
    let w = world();
    let out = validate(&w, &prop("model", vec![bare_req(Op::Put, "10.11.21.1002.00", Some("title: c")), bare_req(Op::Put, "10.11.21.1002.04", Some("why"))]), AT);
    assert_eq!(out.reasons[0].rule, "E7");
    let mut d = bare_req(Op::Put, "10.11.21.1002.04", Some("why"));
    d.tail = Some("draft".into());
    let mut s00 = bare_req(Op::Put, "10.11.21.1002.00", Some("title: c"));
    s00.tail = Some("draft".into());
    assert!(validate(&w, &prop("model", vec![s00, d]), AT).approved(), "drafts need no approval");
}
#[test]
fn e7_promote_needs_review_record() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    b.put("10.11.22.1001.04.draft", None, "d").unwrap();
    w.insert(b.st);
    let pr = |a: Option<&str>, t: Option<&str>| {
        let mut r = bare_req(Op::Promote, "10.11.22.1001.04.draft", None);
        r.approved_by = a.map(|s| s.into());
        r.trial = t.map(|s| s.into());
        validate(&w, &prop("model", vec![r]), AT)
    };
    assert_eq!(pr(None, None).reasons[0].rule, "E7");
    assert_eq!(pr(Some("build-stage (R2)"), None).reasons[0].rule, "R2");
    assert_eq!(pr(Some("me"), None).reasons[0].rule, "R2");
    let ok = pr(Some("build-stage (R2)"), Some("docs/trial/core-trial.md#3"));
    assert!(ok.approved(), "{:?}", ok.reasons);
    assert_eq!(ok.entries[0].extra.get("approved-by").and_then(|v| v.as_str()), Some("build-stage (R2)"));
    assert!(pr(Some("director"), None).approved());
}
#[test]
fn r2_approval_field_accepts_dash_spelling() {
    let r: OpRequest = serde_json::from_str(r#"{"op":"promote","addr":"10.11.21.1001.04.draft","approved-by":"director"}"#).unwrap();
    assert_eq!(r.approved_by.as_deref(), Some("director"));
}
#[test]
fn r4_non_ascii_is_rejected_on_write() {
    let w = world();
    for body in ["caf\u{e9}", "a\tb", "a\r\nb", "em \u{2014} dash"] {
        let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.00", Some("title: c")), req(Op::Put, "10.11.21.1002.04", Some(body))]), AT);
        assert_eq!(out.reasons[0].rule, "R4", "{body:?}");
    }
    let out = validate(&w, &prop("us\u{e9}r", vec![req(Op::Put, "10.11.21.1002.04", Some("x"))]), AT);
    assert_eq!(out.reasons[0].rule, "R4");
}
#[test]
fn a5_1_pointer_99_is_never_content() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.9999.00", Some("title: next")), req(Op::Put, "10.11.21.9999.04", Some("x"))]), AT);
    assert_eq!(out.reasons[0].rule, "A5.1");
    let out = validate(&w, &prop("user", vec![req(Op::Put, "99.10.10.0000.00", Some("title: d")), req(Op::Put, "99.10.10.1001.00", Some("title: p")), req(Op::Put, "99.10.10.1001.04", Some("x"))]), AT);
    assert_eq!(out.reasons[0].rule, "A5.1");
}
#[test]
fn a2_8_page_9999_needs_a_title_too() {
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.9999.00", Some("type: pointer")), req(Op::Put, "10.11.21.9999.08", Some("## n\ntarget: 10.11.21.0000\n"))]), AT);
    assert!(out.reasons.iter().any(|r| r.rule == "A2.8"));
}
#[test]
fn c1_4_kernel_only_card_not_redefined_by_a_book() {
    let mut w = world();
    let mut k = Bk::with_identity("00.00.00");
    k.put("00.00.00.0054.00", None, "title: types").unwrap();
    k.put("00.00.00.0054.01", None, "## General\nowner: kernel-only\n\nThe general type.").unwrap();
    w.insert(k.st);
    let out = validate(&w, &prop("model", vec![req(Op::Put, "10.11.21.0054.00", Some("title: types")), req(Op::Put, "10.11.21.0054.01", Some("## General\nowner: book\n\nmine")), req(Op::Put, "10.11.21.0054.04", Some("## General\nwhy: w\n\nlong"))]), AT);
    assert_eq!(out.reasons[0].rule, "C1.4");
}
#[test]
fn c3_2_the_04_card_may_be_inherited() {
    let mut w = world();
    let mut k = Bk::with_identity("00.00.00");
    k.put("00.00.00.0030.00", None, "title: k").unwrap();
    k.put("00.00.00.0030.01", None, "## Job\nKernel rule.").unwrap();
    k.put("00.00.00.0030.04", None, "## Job\nwhy: w\n\nlong").unwrap();
    w.insert(k.st);
    let out = validate(&w, &prop("u", vec![req(Op::Put, "10.11.21.0030.00", Some("title: b")), req(Op::Put, "10.11.21.0030.01", Some("## Job\nLocal rule."))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
}
#[test]
fn a5_3_retiring_a_back_link_is_refused() {
    let mut w = world();
    let mut t = Bk::with_identity("10.11.22");
    t.put("10.11.22.0010.00", None, "x").unwrap();
    t.put("10.11.22.0010.08", None, "## back\ntarget: 10.11.21.9999\nkind: continuation").unwrap();
    w.insert(t.st);
    let mut b = Bk::with_identity("10.11.21");
    for (a, body) in [("0020.00", "t"), ("0020.04", "local why"), ("1001.00", "title: timer"), ("1001.04", "w"), ("9999.00", "title: next"), ("9999.08", "## next\ntarget: 10.11.22.0010\nkind: continuation")] {
        b.put(&format!("10.11.21.{a}"), None, body).unwrap();
    }
    w.insert(b.st);
    let mut r = req(Op::Tail, "10.11.22.0010.08", None);
    r.to = Some("retired".into());
    let out = validate(&w, &prop("u", vec![r]), AT);
    assert_eq!(out.reasons[0].rule, "A5.3");
}

// ---------- Director rulings R7-R10 ----------
#[test]
fn r10_door_page_holds_only_face_00() {
    let w = world();
    for f in ["01", "04", "08"] {
        let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.30.0000.00", Some("title: new")), req(Op::Put, &format!("10.11.30.0000.{f}"), Some("## A\nwhy: w\n\nabout"))]), AT);
        assert_eq!(out.reasons[0].rule, "R10", "{f}");
    }
}
#[test]
fn r10_face_00_is_the_registry_and_c1_1_still_needs_it() {
    assert_eq!(seqaddr_core::face::face_job(0).name(), "registry");
    let w = world();
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.1002.04", Some("## A\nwhy: w\n\nx"))]), AT);
    assert!(out.reasons.iter().any(|r| r.rule == "C1.1" || r.rule == "format 4.1"), "{:?}", out.reasons);
}
#[test]
fn r7_in_place_override_of_an_inherited_face_is_reported() {
    let w = world();
    // kernel 0020.01 exists; the book writes its own 0020.01 with no override page
    let out = validate(&w, &prop("user", vec![req(Op::Put, "10.11.21.0021.00", Some("x")), req(Op::Put, "10.11.21.0021.04", Some("## A\nwhy: w\n\nbook why"))]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
    assert!(out.findings.iter().any(|f| f.rule == "R7"), "{:?}", out.findings);
    // with an override page in 0001-0009 that names the target, no finding
    let out = validate(&w, &prop("user", vec![
        req(Op::Put, "10.11.21.0001.00", Some("title: override-desk-why")),
        req(Op::Put, "10.11.21.0001.04", Some("## Override\nwhy: the desk text is wrong for tools\ntarget: 10.11.21.0021.04\n\nChanges the why; needed for tools; should give the local reason.")),
        req(Op::Put, "10.11.21.0021.00", Some("x")),
        req(Op::Put, "10.11.21.0021.04", Some("## A\nwhy: w\n\nbook why")),
    ]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
    assert!(!out.findings.iter().any(|f| f.rule == "R7"), "{:?}", out.findings);
}
#[test]
fn r5_followup_a_found_draft_says_why_it_is_a_draft() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    b.put("10.11.22.1001.04.draft", None, "new text").unwrap();
    b.op("m", Op::Note, "10.11.22.1001.04.draft", Some("add the reason"), None).unwrap();
    w.insert(b.st);
    let r = w.resolve(&p("10.11.22.1001.04")).unwrap();
    assert_eq!(r.state.as_deref(), Some("draft"));
    let why = r.why_draft.expect("why_draft");
    assert!(!why.has_seated);
    assert_eq!(why.open_notes.len(), 1);
    assert_eq!(why.open_notes[0].text, "add the reason");
    assert!(w.resolve(&p("10.11.21.1001.04")).unwrap().why_draft.is_none(), "seated face: no why_draft");
}
#[test]
fn r8_a_draft_exists_only_while_drafting() {
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    b.put("10.11.22.1001.04", None, "v1").unwrap();
    b.op("m", Op::Copy, "10.11.22.1001.04", None, None).unwrap();
    assert!(b.st.page(1001).unwrap().face(4).unwrap().draft.is_some());
    b.op("compute", Op::Promote, "10.11.22.1001.04.draft", None, None).unwrap();
    assert!(b.st.page(1001).unwrap().face(4).unwrap().draft.is_none(), "promote ends the draft");
}

#[test]
fn r5_followup_reason_on_the_entry_that_opens_a_draft() {
    let mut w = world();
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    w.insert(b.st);
    let mut r = req(Op::Put, "10.11.22.1001.04.draft", Some("## A\nwhy: w\n\nnew"));
    r.reason = Some("tools need a local why".into());
    let out = validate(&w, &prop("model", vec![r]), AT);
    assert!(out.approved(), "{:?}", out.reasons);
    assert_eq!(out.entries[0].reason(), Some("tools need a local why"));
    let line = out.entries[0].to_line();
    assert!(line.contains("\"reason\":\"tools need a local why\""), "{line}");
    w.insert(out.state.unwrap());
    let why = w.resolve(&p("10.11.22.1001.04")).unwrap().why_draft.unwrap();
    assert_eq!(why.reason.as_deref(), Some("tools need a local why"));
    let mut r = req(Op::Put, "10.11.22.1001.01.draft", Some("x"));
    r.reason = Some("caf\u{e9}".into());
    assert_eq!(validate(&w, &prop("model", vec![r]), AT).reasons[0].rule, "R4");
}
#[test]
fn r5_followup_reason_survives_replay_and_copy() {
    let mut b = Bk::with_identity("10.11.22");
    b.put("10.11.22.1001.00", None, "title: t").unwrap();
    b.put("10.11.22.1001.04", None, "v1").unwrap();
    let mut e = b.e("m", Op::Copy, "10.11.22.1001.04");
    e.extra.insert("reason".into(), serde_json::Value::String("fix the why".into()));
    b.apply(e).unwrap();
    let log = seqaddr_core::BookLog::parse(&b.text()).unwrap();
    let st = seqaddr_core::BookState::replay(&log, &seqaddr_core::Policy::default()).unwrap();
    assert_eq!(st.page(1001).unwrap().face(4).unwrap().draft.as_ref().unwrap().reason.as_deref(), Some("fix the why"));
}
