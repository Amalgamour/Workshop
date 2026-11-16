use std::fs;
use std::path::{Path, PathBuf};

use seqbook::{resolve, Address, Book, BookId, Context, Tail, Writer};

const AT: &str = "2026-11-11T19:13:00Z";
const BY: &str = "cursor";

fn book_10_11_21() -> BookId {
    BookId {
        desk: 10,
        shelf: 11,
        book: 21,
    }
}

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("seqbook-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

#[test]
fn full_address_parses_and_short_form_expands() {
    let bare = Context::empty();
    let full = resolve("10.11.21.1001.04", &bare).unwrap();
    assert_eq!(full.canonical(), "10.11.21.1001.04");

    let ctx = Context::new(Some(book_10_11_21()), Vec::new());
    assert_eq!(
        resolve("4442.01", &ctx).unwrap().canonical(),
        "10.11.21.4442.01"
    );
    assert_eq!(
        resolve("12.2523.04", &ctx).unwrap().canonical(),
        "10.11.12.2523.04"
    );
    assert_eq!(
        resolve("30.12.2523", &ctx).unwrap().canonical(),
        "10.30.12.2523"
    );
    assert!(matches!(
        resolve("10.11.21", &bare).unwrap(),
        Address::Book { id, title: None } if id == book_10_11_21()
    ));
}

#[test]
fn bad_width_is_rejected_not_padded() {
    let bare = Context::empty();
    assert!(resolve("1", &bare).is_err());
    assert!(resolve("01", &bare).is_ok());
    assert!(resolve("10.11.21.1001.4", &bare).is_err());
    assert!(resolve("10.11.21.1001.04", &bare).is_ok());
    assert!(resolve("10.11.21.001", &bare).is_err());
}

#[test]
fn leading_dot_needs_exactly_one_active_page() {
    let book = book_10_11_21();
    let one = Context::new(Some(book), vec![1001]);
    assert_eq!(resolve(".04", &one).unwrap().canonical(), "10.11.21.1001.04");
    assert_eq!(
        resolve(".05.03", &one).unwrap().canonical(),
        "10.11.21.1001.05.03"
    );

    let none = Context::new(Some(book), Vec::new());
    assert!(resolve(".04", &none).is_err());

    let two = Context::new(Some(book), vec![1001, 1002]);
    let err = resolve(".04", &two).unwrap_err();
    assert!(err.to_string().contains("refused"));
}

#[test]
fn put_creates_tail_moves_from_current_and_torn_line_drops() {
    let path = scratch("log");
    let mut writer = Writer::create(&path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.05.01", "task", Some(Tail::Draft))
        .unwrap();
    let again = writer.put(AT, BY, "1001.05.01", "other", Some(Tail::Draft));
    assert!(again.unwrap_err().to_string().contains("already exists"));

    writer
        .tail(AT, BY, "10.11.21.1001.05.01", "draft", "pack")
        .unwrap();
    let skip = writer.tail(AT, BY, "10.11.21.1001.05.01", "draft", "open");
    assert!(skip.unwrap_err().to_string().contains("current tail"));
    let jump = writer.tail(AT, BY, "10.11.21.1001.05.01", "pack", "return");
    assert!(jump.unwrap_err().to_string().contains("does not move"));

    let mut file = fs::OpenOptions::new().append(true).open(&path).unwrap();
    use std::io::Write;
    file.write_all(b"{\"n\":3,\"op\":\"put\"").unwrap();
    drop(file);

    let book = Book::load(&path).unwrap();
    assert!(book.dropped_last_line());
    assert_eq!(book.len(), 2);
    let face = book.face("10.11.21.1001.05.01").unwrap().unwrap();
    assert_eq!(face.tail, Some(Tail::Pack));
    assert_eq!(face.body, "task");
}

#[test]
fn fixture_timer_why_is_readable_in_the_file() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("fixtures/10.11.21.book");
    let _ = fs::remove_file(&path);
    write_timer(&path);

    let text = fs::read_to_string(&path).unwrap();
    assert!(text.contains("title: timer"));
    assert!(text.contains("why: The first fixture has to show a why in the file itself"));
    assert!(text.contains("## purpose"));

    let book = Book::load(&path).unwrap();
    assert_eq!(book.address(), book_10_11_21());
    assert!(!book.dropped_last_line());
    let why = book.face("10.11.21.1001.04").unwrap().unwrap();
    assert!(why.body.contains("why:"));
    assert!(why.body.contains("purpose"));
    let law = book.face("1001.01").unwrap().unwrap();
    assert!(law.body.contains("## purpose"));
    let stamp = book.face("1001.00").unwrap().unwrap();
    assert!(stamp.body.contains("title: timer"));
}

fn write_timer(path: &Path) {
    let mut writer = Writer::create(path, "10.11.21").unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.0000.00",
            "title: tools\nstate: draft\ntype: system\naxioms: 4\n",
            None,
        )
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.0000.01",
            "## book\ntype: rule\naxioms: 4\n\nThis book holds the timer page.\n",
            None,
        )
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
        .put(
            AT,
            BY,
            "10.11.21.1001.00",
            "address: 1001\ntitle: timer\nstate: draft\ntype: general\naxioms: 4\n",
            None,
        )
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.1001.01",
            "## purpose\ntype: rule\naxioms: 4\n\nA timer page is the first fixture.\n",
            None,
        )
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
fn workbook_replays() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("../cursor/temp.book");
    let book = Book::load(&path).unwrap();
    assert_eq!(
        book.address(),
        BookId {
            desk: 10,
            shelf: 10,
            book: 10,
        }
    );
    assert!(!book.dropped_last_line());
    let plan = book.face("10.10.10.0401.01").unwrap().unwrap();
    assert!(plan.body.contains("Show the plan"));
}
