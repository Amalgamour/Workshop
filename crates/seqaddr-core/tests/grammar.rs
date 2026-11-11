//! Address grammar tests. Each test is named after the spec rule it proves.
use seqaddr_core::addr::*;
use seqaddr_core::face::*;
use seqaddr_core::{Address, SeqError};

fn ok(s: &str) -> Address {
    Address::parse(s).unwrap_or_else(|e| panic!("{s} should parse: {e}"))
}
fn bad(s: &str) -> SeqError {
    Address::parse(s).expect_err(&format!("{s} should be invalid"))
}
fn page(s: &str) -> PageAddr {
    match ok(s) {
        Address::Page(p) => p,
        other => panic!("{s} is not a page: {other:?}"),
    }
}
const ACTIVE: BookId = BookId { desk: 10, shelf: 11, book: 21 };

#[test]
fn s1_1_five_axes_full_face_address() {
    let p = page("10.11.21.4442.01");
    assert_eq!((p.desk, p.shelf, p.book, p.page), (Some(10), Some(11), Some(21), 4442));
    assert_eq!(p.face.unwrap().face, 1);
}
#[test]
fn a1_5_exact_widths_rejects_4442_1() {
    assert_eq!(bad("4442.1").rule(), "E3");
    assert_eq!(bad("4442.001.x").rule(), "A1.5");
}
#[test]
fn a1_5_five_digit_group_invalid() {
    assert_eq!(bad("10.11.21.44420").rule(), "A1.5");
}
#[test]
fn a1_5_three_digit_ancestor_invalid() {
    assert!(Address::parse("100.4442").is_err());
}
#[test]
fn a1_5_three_digit_counter_invalid() {
    assert!(Address::parse("4442.05.001").is_err());
}
#[test]
fn a1_2_short_page_infers_desk_shelf_book() {
    assert_eq!(page("4442.01").expand(ACTIVE).to_string(), "10.11.21.4442.01");
}
#[test]
fn a1_2_book_page_infers_desk_shelf() {
    assert_eq!(page("12.2523.04").expand(ACTIVE).to_string(), "10.11.12.2523.04");
}
#[test]
fn a1_2_shelf_book_page_infers_desk() {
    assert_eq!(page("30.12.2523").expand(ACTIVE).to_string(), "10.30.12.2523");
}
#[test]
fn a1_2_full_address_infers_nothing() {
    assert_eq!(page("20.30.40.2523").expand(ACTIVE).to_string(), "20.30.40.2523");
}
#[test]
fn a1_2_forms_are_reported() {
    assert_eq!(page("4442").form(), Form::Short);
    assert_eq!(page("12.4442").form(), Form::Book);
    assert_eq!(page("11.12.4442").form(), Form::Shelf);
    assert_eq!(page("10.11.12.4442").form(), Form::Full);
}
#[test]
fn a1_2_to_form_writes_short_and_full() {
    let p = page("10.11.21.4442.05.03");
    assert_eq!(p.to_form(Form::Short), "4442.05.03");
    assert_eq!(p.to_form(Form::Book), "21.4442.05.03");
    assert_eq!(p.to_form(Form::Shelf), "11.21.4442.05.03");
    assert_eq!(p.to_form(Form::Full), "10.11.21.4442.05.03");
}
#[test]
fn a1_2_one_group_right_of_page_is_face_two_are_counter() {
    let f = page("4442.05").face.unwrap();
    assert_eq!((f.face, f.counter), (5, None));
    let f = page("4442.05.03").face.unwrap();
    assert_eq!((f.face, f.counter), (5, Some(3)));
}
#[test]
fn a1_2_more_than_three_ancestors_invalid() {
    assert!(Address::parse("01.10.11.21.4442").is_err());
}
#[test]
fn a1_2_two_page_groups_invalid() {
    assert_eq!(bad("4442.4443").rule(), "A1.2");
}
#[test]
fn a1_3_no_page_is_desk() {
    match ok("21") {
        Address::Container(c) => assert_eq!(c.level(), ContainerLevel::Desk),
        _ => panic!(),
    }
}
#[test]
fn a1_3_two_groups_is_shelf_three_is_book() {
    match ok("10.11") {
        Address::Container(c) => assert_eq!(c.level(), ContainerLevel::Shelf),
        _ => panic!(),
    }
    match ok("10.11.21") {
        Address::Container(c) => assert_eq!(c.level(), ContainerLevel::Book),
        _ => panic!(),
    }
}
#[test]
fn a1_3_four_two_digit_groups_without_page_invalid() {
    assert_eq!(bad("10.11.21.04").rule(), "A1.3");
}
#[test]
fn a1_3_sibling_book_through_identity_page() {
    assert_eq!(page("21.0000").expand(ACTIVE).to_string(), "10.11.21.0000");
}
#[test]
fn a1_4_counter_attaches_only_to_face() {
    assert!(Address::parse("4442.05.03.04").is_err());
}
#[test]
fn a1_4_counters_have_no_reserved_range_first_is_01() {
    assert_eq!(counter_role(1), CounterRole::Item);
    assert_eq!(page("4442.05.01").face.unwrap().counter, Some(1));
}
#[test]
fn a1_6_leading_dot_is_active_page_face() {
    let a = ok(".04");
    let act = Active { book: ACTIVE, pages: vec![1523] };
    assert_eq!(a.expand(&act).unwrap().to_string(), "10.11.21.1523.04");
}
#[test]
fn a1_6_leading_dot_task() {
    let act = Active { book: ACTIVE, pages: vec![1523] };
    assert_eq!(ok(".05.03").expand(&act).unwrap().to_string(), "10.11.21.1523.05.03");
}
#[test]
fn a1_6_several_active_pages_elevated() {
    let act = Active { book: ACTIVE, pages: vec![1, 2] };
    assert_eq!(ok(".04").expand(&act).unwrap_err().code(), "elevate");
}
#[test]
fn a1_6_no_active_page_is_missing_axiom_7() {
    let act = Active { book: ACTIVE, pages: vec![] };
    let e = ok(".04").expand(&act).unwrap_err();
    assert_eq!((e.code(), e.axiom()), ("missing", Some("7")));
}
#[test]
fn a1_6_bare_04_is_a_desk_not_a_face() {
    assert!(matches!(ok("04"), Address::Container(_)));
}
#[test]
fn a1_6_leading_dot_needs_face_part_only() {
    assert!(Address::parse(".4442").is_err());
    assert!(Address::parse(".timer").is_err());
}
#[test]
fn a1_7_models_write_full_short_rejected_where_full_required() {
    assert_eq!(Address::parse_full_page("4442.01").unwrap_err().rule(), "A1.7");
    assert!(Address::parse_full_page("10.11.21.4442.01").is_ok());
}
#[test]
fn a2_1_word_after_page_is_title() {
    assert_eq!(page("4442.timer").title.as_deref(), Some("timer"));
}
#[test]
fn a2_1_word_after_container_is_title() {
    match ok("10.11.21.tools") {
        Address::Container(c) => assert_eq!(c.title.as_deref(), Some("tools")),
        _ => panic!(),
    }
}
#[test]
fn c8_2_word_after_face_is_card_key() {
    let f = page("10.10.11.1014.01.ham").face.unwrap();
    assert_eq!(f.card.as_deref(), Some("ham"));
}
#[test]
fn c8_2_three_digit_after_card_is_brand() {
    let f = page("1014.01.ham.002").face.unwrap();
    assert_eq!((f.card.as_deref(), f.brand), (Some("ham"), Some(2)));
}
#[test]
fn c8_2_brand_needs_card() {
    assert_eq!(bad("1014.01.002").rule(), "C8.2");
}
#[test]
fn c8_5_brand_sentinels_000_999_reserved() {
    assert_eq!(bad("1014.01.ham.000").rule(), "C8.5");
    assert_eq!(bad("1014.01.ham.999").rule(), "C8.5");
}
#[test]
fn a2_2_faces_never_have_titles() {
    assert_eq!(bad("4442.timer.01").rule(), "A2.2");
}
#[test]
fn a2_3_title_characters() {
    assert!(Address::parse("4442.big-timer2").is_ok());
    assert!(Address::parse("4442.Timer").is_err());
    assert!(Address::parse("4442.2timer").is_err());
    assert!(Address::parse("4442.ti_mer").is_err());
}
#[test]
fn a2_3_no_spaces() {
    assert!(Address::parse("4442.big timer").is_err());
}
#[test]
fn a2_4_title_is_a_label_same_page() {
    assert_eq!(page("4442").page_only(), page("4442.timer").page_only());
}
#[test]
fn a2_5_tail_words_never_titles() {
    for w in ["draft", "retired", "pack", "open", "return", "review"] {
        assert!(check_title(w).is_err(), "{w}");
    }
}
#[test]
fn a2_5_page_tail_after_title() {
    let p = page("4442.plan.draft");
    assert_eq!((p.title.as_deref(), p.page_tail), (Some("plan"), Some(Tail::Draft)));
}
#[test]
fn a2_5_page_tail_without_title() {
    assert_eq!(page("4442.draft").page_tail, Some(Tail::Draft));
    assert_eq!(page("4442.retired").page_tail, Some(Tail::Retired));
}
#[test]
fn a2_5_page_takes_no_counter_tail() {
    assert_eq!(bad("4442.pack").rule(), "A2.5");
    assert_eq!(bad("4442.plan.open").rule(), "A2.5");
}
#[test]
fn a2_5_only_a_tail_follows_a_title() {
    assert_eq!(bad("4442.plan.other").rule(), "A2.5");
}
#[test]
fn a2_5_face_tails_draft_retired() {
    assert_eq!(page("4442.04.draft").face.unwrap().tail, Some(Tail::Draft));
    assert_eq!(page("4442.04.retired").face.unwrap().tail, Some(Tail::Retired));
}
#[test]
fn a2_5_workflow_tails_only_on_counters() {
    for t in ["pack", "open", "return", "review"] {
        assert_eq!(bad(&format!("4442.04.{t}")).rule(), "A2.5", "{t}");
        assert!(Address::parse(&format!("4442.05.03.{t}")).is_ok(), "{t}");
    }
}
#[test]
fn a2_5_retired_never_on_counter() {
    assert_eq!(bad("4442.05.03.retired").rule(), "A2.5");
}
#[test]
fn a2_5_counter_draft_allowed() {
    assert_eq!(page("4442.05.03.draft").face.unwrap().tail, Some(Tail::Draft));
}
#[test]
fn a2_5_containers_take_no_tail() {
    assert_eq!(bad("10.11.21.retired").rule(), "A2.5");
    assert!(Address::parse("10.11.21.0000.retired").is_ok());
}
#[test]
fn a2_5_one_tail_then_card() {
    let f = page("4442.05.03.pack.w01").face.unwrap();
    assert_eq!((f.tail, f.card.as_deref()), (Some(Tail::Pack), Some("w01")));
    assert!(Address::parse("4442.05.03.pack.open").is_err());
}
#[test]
fn a2_8_page_0000_has_no_title() {
    assert_eq!(bad("10.11.21.0000.tools").rule(), "A2.8");
}
#[test]
fn s8_ancestors_carry_no_titles() {
    assert!(Address::parse("10.tools.21.4442").is_err());
}
#[test]
fn s8_empty_groups_invalid() {
    assert!(Address::parse("10..21").is_err());
    assert!(Address::parse("4442.").is_err());
    assert!(Address::parse("").is_err());
}
#[test]
fn e3_one_digit_mark_is_axiom_never_address() {
    assert_eq!(bad("7.8").rule(), "E3");
}
#[test]
fn r9_faces_have_no_sentinels_ff00_and_ff99_do_not_exist() {
    for a in ["1523.05.00", "1523.05.00.open", "1523.05.99", "1523.05.99.pack", "10.11.21.1523.06.00", "10.11.21.0012.03.99"] {
        assert_eq!(bad(a).rule(), "R9", "{a}");
    }
    assert!(Address::parse("1523.05.01").is_ok() && Address::parse("1523.05.98").is_ok());
}
#[test]
fn r9_counter_roles_01_to_98_only() {
    assert_eq!(counter_role(0), CounterRole::NotACounter);
    assert_eq!(counter_role(1), CounterRole::Item);
    assert_eq!(counter_role(98), CounterRole::Item);
    assert_eq!(counter_role(99), CounterRole::NotACounter);
}
#[test]
fn s8_round_trip_display() {
    for s in ["10.11.21.4442.05.03.pack.w01", "10.11.21.4442.plan.draft", "10", "10.11.tools", "4442.01.ham.002", ".05.03", "21.0000"] {
        assert_eq!(ok(s).to_string(), s);
    }
}
#[test]
fn s1_2_axis_roles_00_01_09_99() {
    assert_eq!(axis_role(0), AxisRole::Door);
    assert_eq!(axis_role(5), AxisRole::Reserved);
    assert_eq!(axis_role(42), AxisRole::Normal);
    assert_eq!(axis_role(99), AxisRole::Pointer);
}
#[test]
fn s1_2_sentinels_all_zero_all_nine() {
    assert!(is_page_sentinel(0) && is_page_sentinel(9999) && !is_page_sentinel(1000));
    assert!(is_axis_sentinel(0) && is_axis_sentinel(99) && !is_axis_sentinel(10));
}
#[test]
fn a6_3_desk_kinds() {
    assert_eq!(desk_kind(0), DeskKind::Kernel);
    assert_eq!(desk_kind(1), DeskKind::KernelBranch);
    assert_eq!(desk_kind(9), DeskKind::KernelBranch);
    assert_eq!(desk_kind(10), DeskKind::User);
    assert_eq!(desk_kind(98), DeskKind::User);
    assert_eq!(desk_kind(99), DeskKind::Pointer);
}
#[test]
fn a4_1_owner_rule_books() {
    assert!(BookId::new(10, 0, 0).is_desk_own());
    assert!(BookId::new(10, 0, 5).is_desk_book());
    assert!(BookId::new(10, 11, 0).is_shelf_own());
    assert!(BookId::KERNEL.is_kernel());
    assert!(!BookId::new(10, 11, 21).is_kernel_or_desk_book());
}
#[test]
fn a3_1_identity_pages_of_containers() {
    let ids: Vec<String> = ["10.11.21", "10.11", "10"]
        .iter()
        .map(|s| match ok(s) {
            Address::Container(c) => c.identity_page().to_string(),
            _ => panic!(),
        })
        .collect();
    assert_eq!(ids, ["10.11.21.0000", "10.11.00.0000", "10.00.00.0000"]);
}
#[test]
fn a5_1_child_desk_pointer_identity() {
    match ok("10.99") {
        Address::Container(c) => assert_eq!(c.identity_page().to_string(), "10.99.00.0000"),
        _ => panic!(),
    }
}
#[test]
fn a1_8_lookup_chain_book_shelf_desk_kernel() {
    let chain: Vec<String> = BookId::new(10, 11, 21).lookup_chain().iter().map(|b| b.to_string()).collect();
    assert_eq!(chain, ["10.11.21", "10.11.00", "10.00.00", "00.00.00"]);
}
#[test]
fn a4_1_desk_book_lookup_skips_shelf() {
    let chain: Vec<String> = BookId::new(10, 0, 5).lookup_chain().iter().map(|b| b.to_string()).collect();
    assert_eq!(chain, ["10.00.05", "10.00.00", "00.00.00"]);
}
#[test]
fn a6_3_kernel_lookup_ends_at_itself() {
    assert_eq!(BookId::KERNEL.lookup_chain(), vec![BookId::KERNEL]);
}
#[test]
fn s6_page_layout_ranges() {
    assert_eq!(page_kind(0), PageKind::Door);
    assert_eq!(page_kind(5), PageKind::SpecialReserved);
    assert_eq!(page_kind(12), PageKind::Required);
    assert_eq!(page_kind(30), PageKind::Localized);
    assert_eq!(page_kind(55), PageKind::Structural);
    assert_eq!(page_kind(423), PageKind::StandardBand);
    assert_eq!(page_kind(1001), PageKind::User);
    assert_eq!(page_kind(9999), PageKind::BookContinuation);
}
#[test]
fn a2_6_band_digit_is_second_digit() {
    assert_eq!(band_of(423), Some(4));
    assert_eq!(band_of(1523), Some(5));
    assert_eq!(band_of(99), None);
}
#[test]
fn a2_6_band_heads_end_in_00_from_0100() {
    assert_eq!(page_kind(100), PageKind::BandHead);
    assert_eq!(page_kind(1000), PageKind::BandHead);
    assert_eq!(band_head(1523), Some(1500));
}
#[test]
fn a2_6_pp99_is_band_continuation() {
    assert_eq!(page_kind(1099), PageKind::BandContinuation);
    assert_eq!(page_kind(499), PageKind::BandContinuation);
}
#[test]
fn a2_6_sets_share_n_and_nn() {
    assert_eq!(set_key(423), set_key(523));
    assert_ne!(set_key(423), set_key(1423));
}
#[test]
fn a4_3_face_jobs() {
    assert_eq!(face_job(0), FaceJob::Registry);
    assert_eq!(face_job(1), FaceJob::Law);
    assert_eq!(face_job(2), FaceJob::Schema);
    assert_eq!(face_job(3), FaceJob::Operate);
    assert_eq!(face_job(4), FaceJob::User);
    assert_eq!(face_job(5), FaceJob::Tasks);
    assert_eq!(face_job(6), FaceJob::Notes);
    assert_eq!(face_job(7), FaceJob::Reserved07);
    assert_eq!(face_job(8), FaceJob::Map);
    assert_eq!(face_job(9), FaceJob::Unassigned09);
    assert_eq!(face_job(42), FaceJob::Custom);
    assert_eq!(face_job(99), FaceJob::Reserved99);
}
#[test]
fn c1_1_content_faces_exclude_00_and_07() {
    for f in [1, 2, 3, 4, 5, 6, 8] {
        assert!(is_content_face(f));
    }
    for f in [0, 7, 9, 10, 99] {
        assert!(!is_content_face(f));
    }
}
#[test]
fn a4_4_faces_05_06_always_counted() {
    assert!(always_counted(5) && always_counted(6) && !always_counted(4));
}
#[test]
fn c8_9_default_card_types() {
    let want = [(1, "rule"), (2, "schema"), (3, "menu"), (4, "why"), (5, "task"), (6, "note"), (8, "link")];
    for (f, t) in want {
        assert_eq!(default_card_type(f), Some(t));
    }
    assert!(card_type("rule").unwrap().needs_04 && card_type("schema").unwrap().needs_04);
    assert!(!card_type("brand").unwrap().needs_04);
}
#[test]
fn c1_4_page_types() {
    for t in ["system", "general", "code", "workflow", "band", "pointer"] {
        assert!(is_page_type(t));
    }
    assert!(!is_page_type("misc"));
}
#[test]
fn errors_cite_rule_and_axiom() {
    let e = SeqError::missing("A1.8", "x");
    assert_eq!((e.axiom(), e.http_status()), (Some("7"), 404));
    let e = SeqError::conflict("format 2", "x");
    assert_eq!((e.axiom(), e.http_status()), (Some("1"), 409));
}
#[test]
fn format_1_3_book_file_name() {
    assert_eq!(BookId::new(10, 11, 21).file_name(), "10.11.21.book");
    assert_eq!(BookId::parse("00.00.00").unwrap(), BookId::KERNEL);
    assert!(BookId::parse("10.11").is_err());
}

#[test]
fn r1_full_zero_sequence_is_the_door_on_every_axis() {
    assert_eq!(sentinel(0, 2), Some(Sentinel::Door));
    assert_eq!(sentinel(0, 4), Some(Sentinel::Door));
    assert_eq!(sentinel(99, 2), Some(Sentinel::Pointer));
    assert_eq!(sentinel(9999, 4), Some(Sentinel::Pointer));
    assert_eq!(sentinel(99, 4), None);
    assert_eq!(sentinel(42, 2), None);
    assert!(is_door(0) && !is_door(1));
    assert_eq!(BookId::new(10, 11, 21).door_page().to_string(), "10.11.21.0000");
}
#[test]
fn r1_door_names_in_roles() {
    assert_eq!(axis_role(0), AxisRole::Door);
    assert_eq!(page_kind(0), PageKind::Door);
    assert_eq!(face_job(0).name(), "registry", "R10: face 00 is the registry, not a door");
}

#[test]
fn r9_sentinels_only_on_desk_shelf_book_and_page_widths() {
    assert_eq!(sentinel(999, 3), None, "brands have no sentinel (000/999 are only reserved, C8.5)");
    assert_eq!(sentinel(0, 3), None);
    assert_eq!(sentinel(0, 5), None);
    assert_eq!(sentinel(100, 2), None);
}
