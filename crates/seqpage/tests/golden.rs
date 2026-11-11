//! Golden files: the examples in docs/spec/examples are exactly what export writes
//! from the frozen source books beside them.
mod common;
use common::*;
use seqpage::{check_text, export, import, PageId};

fn golden(book: &str, page: &str, file: &str) {
    let log = seqaddr_core::log::BookLog::parse(&read(book)).unwrap();
    let got = export(&log, PageId::parse(page).unwrap()).unwrap();
    let want = read(file);
    assert_eq!(got, want, "{file} differs from export of {book} {page}; regenerate with `seqpage export` if the format changed on purpose");
    let rep = check_text(&want, Some(file), Some(&log));
    assert!(rep.ok, "{file}: {:?}", rep.errors);
}

#[test]
fn kernel_seqaddr_page() {
    golden("docs/spec/examples/sources/00.00.00.r4.book", "00.00.00.0051", "docs/spec/examples/00.00.00.0051.seqaddr.seq");
}

#[test]
fn bob_cats_page() {
    golden("docs/spec/examples/sources/10.11.21.book", "10.11.21.1001", "docs/spec/examples/10.11.21.1001.bob.seq");
}

#[test]
fn timer_workflow_page() {
    golden("docs/spec/examples/sources/10.11.30.book", "10.11.30.1501", "docs/spec/examples/10.11.30.1501.timer.seq");
    let t = read("docs/spec/examples/10.11.30.1501.timer.seq");
    for want in ["== 05.01 10.11.30.1501.05.01", "--- @7 tail 10.11.30.1501.05.01", "to: \"\"", "outcome: passed", "--- @13 merge 10.11.30.1501.01", "cites: 12", "board := 01 closed", "axioms := 1.7.8"] {
        assert!(t.contains(want), "missing `{want}`");
    }
}

#[test]
fn bob_session_two_proposal() {
    let file = "docs/spec/examples/proposals/10.11.21.1001.bob.seq";
    let text = read(file);
    let log = seqaddr_core::log::BookLog::parse(&read("docs/spec/examples/sources/10.11.21.book")).unwrap();
    let rep = check_text(&text, Some(file), Some(&log));
    assert!(rep.ok, "{:?}", rep.errors);
    let imp = import(&text, Some(&log), "grok-bot").unwrap();
    assert_eq!(imp.booked, vec![7, 8, 9]);
    assert_eq!(imp.proposal.by, "grok-bot");
    assert_eq!(imp.proposal.ops.len(), 1);
    let op = &imp.proposal.ops[0];
    assert_eq!(op.addr, "10.11.21.1001.06.01");
    assert!(op.body.as_deref().unwrap().contains("what is my name"));
    // The core accepts it as a proposal against the sample world (dry run, nothing written).
    let mut w = seqaddr_core::World::new(seqaddr_core::Policy::default());
    w.insert(seqaddr_core::BookState::replay(&log, &w.policy).unwrap());
    let out = seqaddr_core::validate(&w, &imp.proposal, "2026-11-11T20:00:00Z");
    assert_eq!(out.status, seqaddr_core::Status::Approved, "{:?}", out.reasons);
}

#[test]
fn examples_are_plain_ascii() {
    for f in ["00.00.00.0051.seqaddr.seq", "10.11.21.1001.bob.seq", "10.11.30.1501.timer.seq", "proposals/10.11.21.1001.bob.seq", "sources/00.00.00.r4.book", "sources/10.11.21.book", "sources/10.11.30.book"] {
        let t = read(&format!("docs/spec/examples/{f}"));
        assert!(t.bytes().all(|b| b == b'\n' || (0x20..=0x7e).contains(&b)), "{f} breaks R4");
    }
}

#[test]
fn hand_written_new_page_proposes_its_creation() {
    let text = read("docs/spec/examples/proposals/10.11.21.1002.seq");
    let log = seqaddr_core::log::BookLog::parse(&read("docs/spec/examples/sources/10.11.21.book")).unwrap();
    let imp = import(&text, Some(&log), "me").unwrap();
    assert!(imp.booked.is_empty());
    assert_eq!(imp.proposal.ops.len(), 2);
    let mut w = seqaddr_core::World::new(seqaddr_core::Policy::default());
    w.insert(seqaddr_core::BookState::replay(&log, &w.policy).unwrap());
    let out = seqaddr_core::validate(&w, &imp.proposal, "2026-11-11T20:00:00Z");
    assert_eq!(out.status, seqaddr_core::Status::Approved, "{:?}", out.reasons);
}
