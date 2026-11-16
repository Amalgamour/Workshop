use std::fs;
use std::path::PathBuf;
use std::process::Command;

use seqbook::{page_gaps, why_gaps, Book, BookId, Writer};

const AT: &str = "2026-11-11T19:41:00Z";
const BY: &str = "cursor";

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("seqbook-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

fn book() -> BookId {
    BookId {
        desk: 10,
        shelf: 11,
        book: 21,
    }
}

fn stamp(page: &str, title: &str) -> String {
    format!("address: {page}\ntitle: {title}\nstate: draft\ntype: general\naxioms: 4\n")
}

fn write_timer(path: &std::path::Path) {
    let mut writer = Writer::create(path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.00", "title: tools\nstate: draft\ntype: system\naxioms: 4\n", None)
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.01", "## book\ntype: rule\naxioms: 4\n\nThis book holds the timer page.\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.0000.04",
            "## book\ntype: why\nsource: [01 / book]\naxioms: 4\nwhy: The identity page needs a why a person can read, or the book is only a stamp.\n\nThe book is the timer fixture. Page 1001 is the page under test.\n",
            None,
        )
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", &stamp("1001", "timer"), None)
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.01", "## purpose\ntype: rule\naxioms: 4\n\nA timer page is the first fixture.\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.04",
            "## purpose\ntype: why\nsource: [01 / purpose]\naxioms: 4\nwhy: The first fixture has to show a why in the file itself, so a person can check the record without a reader program.\n\nThis page is the timer example. The why is the line above. The law card on face 01 is only the brief.\n",
            None,
        )
        .unwrap();
}

#[test]
fn open_appends_to_an_existing_book() {
    let path = scratch("open");
    let mut writer = Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", &stamp("1001", "timer"), None)
        .unwrap();
    drop(writer);
    let mut writer = Writer::open(&path).unwrap();
    writer
        .put(AT, BY, "1001.04", "second", None)
        .unwrap();
    let loaded = Book::load(&path).unwrap();
    assert_eq!(loaded.len(), 2);
    assert_eq!(loaded.address(), book());
    assert_eq!(
        loaded.face("10.11.21.1001.04").unwrap().unwrap().body,
        "second"
    );
}

#[test]
fn read_prints_the_timer_why() {
    let bin = env!("CARGO_BIN_EXE_seqbook");
    let fixture = scratch("read-timer");
    write_timer(&fixture);
    let ok = Command::new(bin)
        .args(["read", fixture.to_str().unwrap(), "10.11.21.1001.04"])
        .output()
        .unwrap();
    assert!(ok.status.success());
    let text = String::from_utf8(ok.stdout).unwrap();
    assert!(text.contains("why: The first fixture has to show a why in the file itself"));
    assert!(!text.contains("\"op\""));

    let missing = Command::new(bin)
        .args(["read", fixture.to_str().unwrap(), "10.11.21.1001.09"])
        .output()
        .unwrap();
    assert!(!missing.status.success());
    assert!(String::from_utf8(missing.stderr).unwrap().contains("missing"));
}

#[test]
fn timer_fixture_passes_both_checks() {
    let path = scratch("timer-check");
    write_timer(&path);
    let book = Book::load(&path).unwrap();
    let why = why_gaps(&book);
    assert!(why.hard.is_empty(), "{:?}", why.hard);
    assert!(why.findings.is_empty(), "{:?}", why.findings);
    assert!(page_gaps(&book).is_empty());
}

#[test]
fn missing_why_is_a_hard_gap() {
    let path = scratch("why");
    let mut writer = Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "1001.00", &stamp("1001", "timer"), None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "1001.01",
            "## purpose\ntype: rule\naxioms: 4\n\nThe law card.\n",
            None,
        )
        .unwrap();
    let book = writer.book();
    let why = why_gaps(book);
    assert!(
        why.hard.iter().any(|gap| gap.contains("purpose") && gap.contains("no face 04")),
        "{:?}",
        why.hard
    );

    writer
        .put(
            AT,
            BY,
            "1001.04",
            "## purpose\ntype: why\naxioms: 4\nwhy:\n\nA blank why is not a reason.\n",
            None,
        )
        .unwrap();
    let why = why_gaps(writer.book());
    assert!(
        why.hard.iter().any(|gap| gap.contains("no why")),
        "{:?}",
        why.hard
    );
}

#[test]
fn copied_why_is_a_finding() {
    let path = scratch("copy");
    let mut writer = Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "1001.00", &stamp("1001", "timer"), None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "1001.01",
            "## purpose\ntype: rule\n\nSame words.\n",
            None,
        )
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "1001.04",
            "## purpose\ntype: why\nwhy: The line is here so the hard rule passes.\n\nSame words.\n",
            None,
        )
        .unwrap();
    let why = why_gaps(writer.book());
    assert!(why.hard.is_empty(), "{:?}", why.hard);
    assert!(why.findings.iter().any(|gap| gap.contains("copies")));
}

#[test]
fn page_shape_rejects_a_stamp_with_only_face_07() {
    let path = scratch("shape");
    let mut writer = Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "1001.00", &stamp("1001", "timer"), None)
        .unwrap();
    writer.put(AT, BY, "1001.07", "reserved", None).unwrap();
    writer
        .put(AT, BY, "1002.01", "## alone\ntype: rule\n\nNo stamp.\n", None)
        .unwrap();
    let gaps = page_gaps(writer.book());
    assert!(gaps.iter().any(|gap| gap.contains("1001") && gap.contains("no content")));
    assert!(gaps.iter().any(|gap| gap.contains("1002") && gap.contains("no face 00")));
}

#[test]
fn planned_pages_pass_their_own_checks() {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../cursor/temp.book");
    let book = Book::load(&path).unwrap();
    for page in ["0402", "0403", "0404", "0302", "0303", "0304"] {
        let face = book.face(&format!("10.10.10.{page}.04")).unwrap();
        assert!(face.is_some(), "{page} has no face 04");
        assert!(face.unwrap().body.contains("why:"));
    }
    let why = why_gaps(&book);
    let own: Vec<_> = why
        .hard
        .iter()
        .filter(|gap| {
            ["0402", "0403", "0404", "0302", "0303", "0304", "0502", "0503", "0504"]
                .iter()
                .any(|page| gap.contains(page))
        })
        .cloned()
        .collect();
    assert!(own.is_empty(), "{own:?}");
    let shape: Vec<_> = page_gaps(&book)
        .into_iter()
        .filter(|gap| gap.contains(".0402") || gap.contains(".0403") || gap.contains(".0404"))
        .collect();
    assert!(shape.is_empty(), "{shape:?}");
}
