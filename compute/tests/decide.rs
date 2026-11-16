use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use compute::{propose_put, read_face, Verdict};

const AT: &str = "2026-11-11T20:27:00Z";
const BY: &str = "compute";

fn scratch(name: &str) -> PathBuf {
    let path = std::env::temp_dir().join(format!("compute-{}-{name}.book", std::process::id()));
    let _ = fs::remove_file(&path);
    path
}

fn bin() -> PathBuf {
    PathBuf::from(env!("CARGO_BIN_EXE_compute"))
}

fn write_base(path: &Path) {
    let mut writer = seqbook::Writer::create(path, "10.11.21").unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.00", "title: tools\nstate: draft\n", None)
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.0000.01", "## book\ntype: rule\n\nThe fixture book.\n", None)
        .unwrap();
    writer
        .put(
            AT,
            BY,
            "10.11.21.0000.04",
            "## book\ntype: why\nwhy: The book needs a why of its own.\n\nIt holds the timer page.\n",
            None,
        )
        .unwrap();
    writer
        .put(AT, BY, "10.11.21.1001.00", "address: 1001\ntitle: timer\n", None)
        .unwrap();
}

#[test]
fn read_returns_the_face_and_does_not_grow_the_book() {
    let path = scratch("read");
    write_base(&path);
    let before = fs::read(&path).unwrap();
    let verdict = read_face(&path, "10.11.21.1001.00").unwrap();
    assert!(matches!(verdict, Verdict::Read { .. }));
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_missing_why_is_refused_and_the_file_is_unchanged() {
    let path = scratch("why");
    write_base(&path);
    let before = fs::read(&path).unwrap();
    let verdict = propose_put(
        &path,
        AT,
        BY,
        "10.11.21.1001.01",
        "## purpose\ntype: rule\n\nA law card with no twin.\n",
    )
    .unwrap();
    match verdict {
        Verdict::Refuse { reasons } => {
            assert!(reasons.iter().any(|reason| reason.contains("purpose") && reason.contains("04")));
        }
        other => panic!("{other:?}"),
    }
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_face_07_page_is_refused() {
    let path = scratch("shape");
    write_base(&path);
    let before = fs::read(&path).unwrap();
    let verdict = propose_put(&path, AT, BY, "10.11.21.1002.07", "reserved\n").unwrap();
    match verdict {
        Verdict::Refuse { reasons } => {
            assert!(reasons.iter().any(|reason| reason.contains("1002") && reason.contains("content")));
        }
        other => panic!("{other:?}"),
    }
    assert_eq!(fs::read(&path).unwrap(), before);
}

#[test]
fn a_paired_why_is_accepted_and_the_book_grows() {
    let path = scratch("accept");
    write_base(&path);
    let law = propose_put(
        &path,
        AT,
        BY,
        "10.11.21.1001.04",
        "## purpose\ntype: why\nwhy: The timer needs a reason before the law card lands.\n\nThis is the why a person reads.\n",
    )
    .unwrap();
    assert!(matches!(law, Verdict::Accept { .. }));
    let paired = propose_put(
        &path,
        AT,
        BY,
        "10.11.21.1001.01",
        "## purpose\ntype: rule\n\nA timer page the compute accepted.\n",
    )
    .unwrap();
    assert!(matches!(paired, Verdict::Accept { .. }));
    let text = fs::read_to_string(&path).unwrap();
    assert!(text.contains("The timer needs a reason"));
}

#[test]
fn the_command_prints_a_refusal() {
    let path = scratch("cli");
    write_base(&path);
    let output = Command::new(bin())
        .args([
            "--book",
            path.to_str().unwrap(),
            "put",
            "--addr",
            "10.11.21.1002.07",
            "--at",
            AT,
            "--by",
            BY,
            "--body",
            "reserved",
        ])
        .output()
        .unwrap();
    let text = String::from_utf8(output.stdout).unwrap();
    assert!(text.contains("decision: refuse"), "{text}");
    assert!(!output.status.success());
}
