//! A .seq request reaches the compute. The compute decides. The request itself writes nothing.

use std::fs;
use std::path::PathBuf;

use compute::{propose_put, Verdict};
use seqpage::{export, import_request};

const AT: &str = "2026-11-11T21:10:00Z";
const BY: &str = "compute";

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("import-book-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

fn book(path: &std::path::Path) {
    let mut writer = seqbook::Writer::create(path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", "title: timer\nstate: draft\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.04",
            "## purpose\ntype: why\nwhy: The page already has a why.\n\nSo a note can land.\n",
            None,
        )
        .unwrap();
}

#[test]
fn a_request_is_refused_when_the_page_is_new_and_accepted_when_it_fits() {
    let path = scratch("gate");
    book(&path);
    let before = fs::read(&path).unwrap();
    let text = export(&path, "10.11.21.1001").unwrap();
    let bad = format!("--- new put 10.11.21.1003.01\n| ## demo\n| type: rule\n|\n| A law with no why.\n\n{text}");
    let (ops, _) = import_request(&bad);
    assert_eq!(ops.len(), 1);
    let refused = propose_put(&path, AT, BY, &ops[0].addr, &ops[0].body).unwrap();
    assert!(matches!(refused, Verdict::Refuse { .. }), "{refused:?}");
    assert_eq!(fs::read(&path).unwrap(), before);

    let good = text.replacen(
        "~ history",
        "--- new put 10.11.21.1001.06.01\n| ## note\n| The request landed.\n\n~ history",
        1,
    );
    let (ops, _) = import_request(&good);
    let accepted = propose_put(&path, AT, BY, &ops[0].addr, &ops[0].body).unwrap();
    assert!(matches!(accepted, Verdict::Accept { .. }), "{accepted:?}");
    let saved = fs::read_to_string(&path).unwrap();
    assert!(saved.contains("The request landed."));
}
