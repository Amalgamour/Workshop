use std::fs;
use std::path::PathBuf;

use seqpage::{check, check_name, export, file_name, import_request};

const AT: &str = "2026-11-11T20:55:00Z";
const BY: &str = "cursor";

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("seqpage-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

fn book(path: &std::path::Path) {
    let mut writer = seqbook::Writer::create(path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", "title: timer\nstate: draft\ntype: general\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.04",
            "## purpose\ntype: why\nwhy: A person can read this.\n\nThe why is in the file.\n",
            None,
        )
        .unwrap();
}

#[test]
fn export_matches_the_book_and_does_not_write_it() {
    let path = scratch("round");
    book(&path);
    let before = fs::read(&path).unwrap();
    let text = export(&path, "10.11.21.1001").unwrap();
    assert!(text.starts_with("seqpage 1\n"));
    assert!(text.contains("= 00 registry 10.11.21.1001.00\n"));
    assert!(text.contains("title := timer\n"));
    assert!(text.contains("| why: A person can read this.\n"));
    assert!(text.ends_with("~ end\n"));
    assert!(check(&text, &path).unwrap().is_empty());
    assert_eq!(fs::read(&path).unwrap(), before);
    assert_eq!(file_name("10.11.21.1001", Some("timer")), "10.11.21.1001.timer.seq");
}

#[test]
fn a_changed_booked_line_is_refused() {
    let path = scratch("past");
    book(&path);
    let before = fs::read(&path).unwrap();
    let text = export(&path, "10.11.21.1001").unwrap().replace("can read this", "can edit this");
    let faults = check(&text, &path).unwrap();
    assert!(faults.iter().any(|fault| fault.detail.contains("past is not rewritten")));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_title_in_the_name_that_differs_is_reported() {
    let path = scratch("name");
    book(&path);
    let text = export(&path, "10.11.21.1001").unwrap();
    let faults = check_name("10.11.21.1001.cats.seq", &text);
    assert!(faults.iter().any(|fault| fault.detail.contains("cats") && fault.detail.contains("timer")));
}

#[test]
fn a_new_block_is_a_request_and_the_book_is_not_written() {
    let path = scratch("import");
    book(&path);
    let before = fs::read(&path).unwrap();
    let text = export(&path, "10.11.21.1001").unwrap();
    let (ops, faults) = import_request(&text);
    assert!(ops.is_empty());
    assert!(faults.iter().any(|fault| fault.detail.contains("nothing to propose")));
    let proposed = text.replacen(
        "~ history",
        "--- new put 10.11.21.1001.06.01\n| ## note\n| hello\n\n~ history",
        1,
    );
    let (ops, faults) = import_request(&proposed);
    assert!(faults.iter().all(|fault| !fault.detail.contains("after the booked")));
    assert_eq!(ops.len(), 1);
    assert_eq!(ops[0].addr, "10.11.21.1001.06.01");
    assert!(ops[0].body.contains("hello"));
    let early = format!("seqpage 1\n--- new put 10.11.21.1001.06.01\n| hi\n\n{text}");
    let (_, early_faults) = import_request(&early);
    assert!(early_faults.iter().any(|fault| fault.detail.contains("after the booked")));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_mark_outside_plain_ascii_is_reported() {
    let path = scratch("ascii");
    book(&path);
    let text = export(&path, "10.11.21.1001").unwrap().replace("timer", "timér");
    let faults = check(&text, &path).unwrap();
    assert!(faults.iter().any(|fault| fault.detail.contains("plain ASCII")));
}
