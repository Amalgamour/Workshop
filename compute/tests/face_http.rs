use std::fs;
use std::path::PathBuf;

use compute::http::reply;

const AT: &str = "2026-11-11T20:50:00Z";
const BY: &str = "compute";

fn book(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!(
        "compute-http-{}-{name}.book",
        std::process::id()
    ));
    let _ = fs::remove_file(&path);
    let mut writer = seqbook::Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", "address: 1001\ntitle: timer\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.04",
            "## purpose\ntype: why\nwhy: A person can read this line.\n\nThe why is in the file.\n",
            None,
        )
        .unwrap();
    path
}

#[test]
fn a_face_request_returns_the_why_and_does_not_write() {
    let path = book("read");
    let before = fs::read(&path).unwrap();
    let reply = reply(&path, "GET", "/face?addr=10.11.21.1001.04", "");
    assert_eq!(reply.status, 200, "{}", reply.body);
    assert!(reply.body.contains("decision: read"));
    assert!(reply.body.contains("title: timer"));
    assert!(reply.body.contains("A person can read this line."));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_missing_face_is_a_refusal() {
    let path = book("missing");
    let reply = reply(&path, "GET", "/face?addr=10.11.21.1001.09", "");
    assert_eq!(reply.status, 404);
    assert!(reply.body.contains("decision: refuse"));
    assert!(reply.body.contains("title: timer"));
}

#[test]
fn a_sentence_is_accepted_onto_a_note() {
    let path = book("note");
    let reply = reply(&path, "POST", "/propose", "The timer still needs a person.");
    assert_eq!(reply.status, 200, "{}", reply.body);
    assert!(reply.body.contains("proposer: local"));
    assert!(reply.body.contains("not a remote model"));
    assert!(reply.body.contains("decision: accept"));
    assert!(reply.body.contains("title: timer"));
    let text = fs::read_to_string(&path).unwrap();
    assert!(text.contains("The timer still needs a person."));
}

#[test]
fn a_law_sentence_is_refused_and_the_file_stays() {
    let path = book("law");
    let before = fs::read(&path).unwrap();
    let reply = reply(&path, "POST", "/propose", "law: A rule with no why.");
    assert_eq!(reply.status, 409, "{}", reply.body);
    assert!(reply.body.contains("decision: refuse"));
    assert!(reply.body.contains("demo"));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_seq_view_is_served_and_the_book_is_not_written() {
    let path = book("seq");
    let before = fs::read(&path).unwrap();
    let reply = reply(&path, "GET", "/seq?page=10.11.21.1001", "");
    assert_eq!(reply.status, 200, "{}", reply.body);
    assert!(reply.body.starts_with("seqpage 1\n"));
    assert!(reply.body.contains("title := timer"));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn the_catalog_lists_every_band_and_the_page_title() {
    let path = book("catalog");
    let before = fs::read(&path).unwrap();
    let loaded = seqbook::Book::load(&path).unwrap();
    let text = compute::catalog(&loaded);
    assert!(text.contains("band: 0400-0499 dev"));
    assert!(text.contains("band: 0100-0299 unassigned"));
    assert!(text.contains("page: 10.11.21.1001 title: timer"));
    assert!(text.contains("face: 10.11.21.1001.04"));
    assert_eq!(fs::read(&path).unwrap(), before);
}
