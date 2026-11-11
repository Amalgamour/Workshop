//! Book file tests (format.md section 3).
mod common;
use common::*;
use seqaddr_core::log::{check_timestamp, format_utc, Entry, Op};
use seqaddr_core::{BookLog, BookState, Policy};

const EXAMPLE: &str = r###"{"seqbook":1,"address":"10.11.21"}
{"n":1,"at":"2026-11-09T14:02:11Z","by":"user","op":"put","addr":"10.11.21.0000.00","body":"---\ntitle: tools\n---"}
{"n":2,"at":"2026-11-09T14:05:40Z","by":"claude-opus-5-5","op":"put","addr":"10.11.21.1523.05.03","tail":"pack","body":"## Build timer\n..."}
{"n":3,"at":"2026-11-09T14:06:02Z","by":"agent-7","op":"tail","addr":"10.11.21.1523.05.03","from":"pack","to":"open"}
"###;

#[test]
fn format_3_2_spec_example_parses_and_replays() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    assert_eq!(log.entries.len(), 3);
    let st = BookState::replay(&log, &Policy::default()).unwrap();
    let c = st.counter(1523, 5, 3).unwrap();
    assert_eq!(c.tail.board_word(), "open");
    assert_eq!(c.claim.as_ref().unwrap().owner, "agent-7");
    assert_eq!(st.title().as_deref(), Some("tools"));
}
#[test]
fn format_3_2_header_is_line_one() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    assert_eq!(log.header.seqbook, 1);
    assert_eq!(log.header.address, "10.11.21");
}
#[test]
fn format_3_2_bad_header_is_corrupt() {
    assert_eq!(BookLog::parse("{\"x\":1}\n").unwrap_err().code(), "corrupt");
    assert_eq!(BookLog::parse("{\"seqbook\":2,\"address\":\"10.11.21\"}\n").unwrap_err().code(), "corrupt");
    assert_eq!(BookLog::parse("{\"seqbook\":1,\"address\":\"10.11\"}\n").unwrap_err().code(), "corrupt");
}
#[test]
fn format_3_2_round_trip_text() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    assert_eq!(log.to_text(), BookLog::parse(&log.to_text()).unwrap().to_text());
    assert_eq!(BookLog::parse(&log.to_text()).unwrap(), log);
}
#[test]
fn format_3_2_unknown_fields_are_kept() {
    let t = EXAMPLE.replace("\"by\":\"user\"", "\"by\":\"user\",\"future\":7");
    let log = BookLog::parse(&t).unwrap();
    assert!(log.to_text().contains("\"future\":7"));
}
#[test]
fn format_3_2_entries_numbered_in_order() {
    let t = EXAMPLE.replace("\"n\":2", "\"n\":5");
    assert_eq!(BookLog::parse(&t).unwrap_err().code(), "corrupt");
}
#[test]
fn format_3_2_timestamps_are_iso_utc() {
    assert!(check_timestamp("2026-11-09T14:02:11Z").is_ok());
    assert!(check_timestamp("2026-11-09T14:02:11.123Z").is_ok());
    assert!(check_timestamp("2026-11-09 14:02:11").is_err());
    assert!(check_timestamp("2026-11-09T14:02:11-05:00").is_err());
    let t = EXAMPLE.replace("2026-11-09T14:06:02Z", "yesterday");
    assert_eq!(BookLog::parse(&t).unwrap_err().code(), "corrupt");
}
#[test]
fn format_utc_formats_epoch_seconds() {
    assert_eq!(format_utc(0), "1970-01-01T00:00:00Z");
    assert_eq!(format_utc(1794355200), "2026-11-11T00:00:00Z");
}
#[test]
fn format_3_1_partial_last_line_dropped() {
    let cut = &EXAMPLE[..EXAMPLE.len() - 20];
    let log = BookLog::parse(cut).unwrap();
    assert!(log.dropped_partial);
    assert_eq!(log.entries.len(), 2);
}
#[test]
fn format_3_1_complete_last_line_without_newline_kept() {
    let t = EXAMPLE.trim_end();
    let log = BookLog::parse(t).unwrap();
    assert!(!log.dropped_partial);
    assert_eq!(log.entries.len(), 3);
}
#[test]
fn format_3_1_damage_before_last_line_is_corrupt() {
    let t = EXAMPLE.replace("\"op\":\"put\",\"addr\":\"10.11.21.1523", "\"op\":\"put\",\"addr\":10.11.21.1523");
    let e = BookLog::parse(&t).unwrap_err();
    assert_eq!(e.code(), "corrupt");
}
#[test]
fn format_3_1_cut_off_proposal_dropped_whole() {
    let mut b = Bk::with_identity(B);
    let mut e1 = b.e("user", Op::Put, "10.11.21.1001.00");
    e1.body = Some("title: one".into());
    e1.proposal = Some("p2".into());
    e1.of = Some(2);
    b.apply(e1).unwrap();
    let text = b.text();
    let log = BookLog::parse(&text).unwrap();
    assert!(log.dropped_partial, "a proposal of 2 with only 1 line is dropped");
    assert_eq!(log.entries.len(), 1);
}
#[test]
fn format_3_1_rewind_replays_up_to_n() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    let st = BookState::replay_until(&log, 2, &Policy::default()).unwrap();
    assert_eq!(st.counter(1523, 5, 3).unwrap().tail.board_word(), "pack");
}
#[test]
fn format_3_1_history_per_address() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    let h: Vec<u64> = log.history("10.11.21.1523.05.03").unwrap().iter().map(|e| e.n).collect();
    assert_eq!(h, [2, 3]);
    let h: Vec<u64> = log.history("10.11.21.1523").unwrap().iter().map(|e| e.n).collect();
    assert_eq!(h, [2, 3]);
    let h: Vec<u64> = log.history("10.11.21.0000").unwrap().iter().map(|e| e.n).collect();
    assert_eq!(h, [1]);
}
#[test]
fn format_3_1_history_ignores_title_and_tail() {
    let log = BookLog::parse(EXAMPLE).unwrap();
    assert_eq!(log.history("10.11.21.1523.05.03.open").unwrap().len(), 2);
}
#[test]
fn format_3_4_snapshot_then_replay_from_it() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.00", None, "title: one").unwrap();
    b.put("10.11.21.1001.04", None, "hello").unwrap();
    let snap = b.st.snapshot_entry(AT, "compute");
    b.apply(snap).unwrap();
    b.put("10.11.21.1002.00", None, "title: two").unwrap();
    let log = BookLog::parse(&b.text()).unwrap();
    assert_eq!(log.latest_snapshot(), Some(3));
    let st = BookState::replay(&log, &Policy::default()).unwrap();
    assert_eq!(st, b.st);
    assert_eq!(st.last_n, 5);
}
#[test]
fn format_3_4_snapshot_needs_state() {
    let mut b = Bk::with_identity(B);
    let e = b.e("compute", Op::Snapshot, B);
    assert!(b.apply(e).is_err());
}
#[test]
fn format_3_4_snapshot_for_other_book_rejected() {
    let mut b = Bk::with_identity(B);
    let other = Bk::with_identity("10.11.22");
    let mut e = other.st.snapshot_entry(AT, "compute");
    e.n = 2;
    assert!(b.apply(e).is_err());
}
#[test]
fn format_3_3_proposed_ops_switch_off() {
    let mut b = Bk::with_identity(B);
    b.put("10.11.21.1001.04", None, "x").unwrap();
    b.pol.allow_proposed_ops = false;
    let e = b.op("user", Op::Copy, "10.11.21.1001.04", None, None).unwrap_err();
    assert_eq!(e.rule(), "format 3.3");
}
#[test]
fn format_3_3_op_names_serialize_lowercase() {
    let e = Entry::new(1, AT, "u", Op::Promote, "10.11.21.0001.01");
    assert!(e.to_line().contains("\"op\":\"promote\""));
    for op in [Op::Copy, Op::Note, Op::Merge, Op::Promote, Op::Use] {
        assert!(op.is_proposed());
    }
    for op in [Op::Put, Op::Tail, Op::Snapshot] {
        assert!(!op.is_proposed());
    }
}
#[test]
fn format_1_3_entry_must_be_in_its_book() {
    let mut b = Bk::with_identity(B);
    assert_eq!(b.put("10.11.22.1001.00", None, "title: x").unwrap_err().rule(), "format 1.3");
}
#[test]
fn format_3_2_entry_sequence_enforced_in_apply() {
    let mut b = Bk::with_identity(B);
    let mut e = b.e("user", Op::Put, "10.11.21.1001.00");
    e.n = 9;
    e.body = Some("x".into());
    assert!(b.apply(e).is_err());
}
#[test]
fn format_3_2_author_required() {
    let mut b = Bk::with_identity(B);
    let mut e = b.e(" ", Op::Put, "10.11.21.1001.00");
    e.body = Some("x".into());
    assert!(b.apply(e).is_err());
}

#[cfg(feature = "fs")]
mod files {
    use super::*;
    use seqaddr_core::log::file;
    use seqaddr_core::BookId;

    fn tmp(name: &str) -> std::path::PathBuf {
        let d = std::env::temp_dir().join(format!("seqaddr-test-{}-{name}", std::process::id()));
        let _ = std::fs::remove_file(&d);
        d
    }
    #[test]
    fn format_3_1_append_then_read() {
        let p = tmp("append");
        file::create(&p, BookId::parse(B).unwrap()).unwrap();
        let mut e = Entry::new(1, AT, "user", Op::Put, "10.11.21.0000.00");
        e.body = Some("title: tools".into());
        file::append(&p, &[e]).unwrap();
        let log = file::read(&p).unwrap();
        assert_eq!(log.entries.len(), 1);
        assert!(file::create(&p, BookId::parse(B).unwrap()).is_err(), "create never overwrites");
    }
    #[test]
    fn format_3_1_crash_safe_append_repairs_partial_line() {
        let p = tmp("crash");
        std::fs::write(&p, &EXAMPLE[..EXAMPLE.len() - 15]).unwrap();
        assert!(file::repair_tail(&p).unwrap());
        let log = file::read(&p).unwrap();
        assert_eq!(log.entries.len(), 2);
        let mut e = Entry::new(3, AT, "agent-7", Op::Tail, "10.11.21.1523.05.03");
        e.from = Some("pack".into());
        e.to = Some("open".into());
        file::append(&p, &[e]).unwrap();
        let log = file::read(&p).unwrap();
        assert_eq!(log.entries.len(), 3);
        assert!(!log.dropped_partial);
    }
    #[test]
    fn format_3_1_append_after_unterminated_complete_line() {
        let p = tmp("noeol");
        std::fs::write(&p, EXAMPLE.trim_end()).unwrap();
        let e = Entry::new(4, AT, "agent-7", Op::Tail, "10.11.21.1523.05.03");
        file::append(&p, &[e]).unwrap();
        assert_eq!(file::read(&p).unwrap().entries.len(), 4);
    }
}
