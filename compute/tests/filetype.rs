//! What the file type does today, tried on scratch books.

use std::fs;
use std::io::Write;
use std::path::PathBuf;

use compute::{page_title, propose_put, Verdict};

const AT: &str = "2026-11-11T21:40:00Z";
const BY: &str = "compute";

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("filetype-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

fn base(path: &std::path::Path) {
    let mut writer = seqbook::Writer::create(path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.00", "title: tools\nstate: draft\n", None)
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.01", "## book\ntype: rule\n\nThe book.\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.0000.04",
            "## book\ntype: why\nwhy: The book needs a why.\n\nSo the file is a book.\n",
            None,
        )
        .unwrap();
}

#[test]
fn a_torn_last_line_drops_and_a_middle_break_is_corrupt() {
    let path = scratch("torn");
    base(&path);
    let mut file = fs::OpenOptions::new().append(true).open(&path).unwrap();
    writeln!(file, "{{\"n\":4,\"op\":\"put\"").unwrap();
    let loaded = seqbook::Book::load(&path).unwrap();
    assert!(loaded.dropped_last_line());
    assert!(loaded.face("10.11.21.0000.04").unwrap().is_some());
    assert!(seqbook::Writer::open(&path).is_err());

    let broken = scratch("middle");
    base(&broken);
    let text = fs::read_to_string(&broken).unwrap();
    let mut lines: Vec<&str> = text.lines().collect();
    lines.insert(2, "this is not json");
    fs::write(&broken, lines.join("\n") + "\n").unwrap();
    let err = seqbook::Book::load(&broken).unwrap_err();
    assert!(err.to_string().contains("corrupt") || err.to_string().contains("line"));
}

#[test]
fn one_put_cannot_stand_a_new_page() {
    let path = scratch("newpage");
    base(&path);
    let before = fs::read(&path).unwrap();
    let stamp = propose_put(&path, AT, BY, "10.11.21.1003.00", "title: fresh\n").unwrap();
    assert!(matches!(stamp, Verdict::Refuse { .. }), "{stamp:?}");
    let law = propose_put(
        &path,
        AT,
        BY,
        "10.11.21.1003.01",
        "## demo\ntype: rule\n\nA first face.\n",
    )
    .unwrap();
    assert!(matches!(law, Verdict::Refuse { .. }), "{law:?}");
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_title_on_the_address_is_not_checked_against_the_stamp() {
    let path = scratch("title");
    base(&path);
    let mut writer = seqbook::Writer::open(&path).unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", "title: timer\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.04",
            "## purpose\ntype: why\nwhy: A why.\n\nThe body.\n",
            None,
        )
        .unwrap();
    let loaded = seqbook::Book::load(&path).unwrap();
    let titled = page_title(&loaded, "10.11.21.1001.other").unwrap();
    assert_eq!(titled.as_deref(), Some("timer"));
    let read = seqbook::Book::load(&path)
        .unwrap()
        .face("10.11.21.1001.other");
    assert!(read.is_err(), "a title is not a face, and the mismatch is not reported");
}

#[test]
fn an_unknown_operation_is_corrupt() {
    let path = scratch("snap");
    base(&path);
    let text = fs::read_to_string(&path).unwrap();
    let extra = format!(
        "{text}{{\"n\":4,\"at\":\"{AT}\",\"by\":\"{BY}\",\"op\":\"snapshot\",\"addr\":\"10.11.21\"}}\n"
    );
    fs::write(&path, extra).unwrap();
    let err = seqbook::Book::load(&path).unwrap_err();
    let message = err.to_string();
    assert!(message.contains("snapshot") || message.contains("corrupt"), "{message}");
}
