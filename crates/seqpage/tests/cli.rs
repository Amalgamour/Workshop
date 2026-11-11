//! The `seqpage` command: export, check, import (never writes a book).
mod common;
use common::*;
use std::process::Command;

fn run(args: &[&str]) -> (bool, String) {
    let o = Command::new(env!("CARGO_BIN_EXE_seqpage")).args(args).current_dir(repo()).output().unwrap();
    (o.status.success(), String::from_utf8_lossy(&o.stdout).to_string())
}

#[test]
fn export_to_stdout_matches_golden() {
    let (ok, out) = run(&["export", "docs/spec/examples/sources/10.11.21.book", "10.11.21.1001"]);
    assert!(ok);
    assert_eq!(out, read("docs/spec/examples/10.11.21.1001.bob.seq"));
}

#[test]
fn check_ok_and_bad() {
    let (ok, out) = run(&["check", "docs/spec/examples/10.11.30.1501.timer.seq", "--book", "docs/spec/examples/sources/10.11.30.book"]);
    assert!(ok, "{out}");
    let dir = std::env::temp_dir().join(format!("seqpage-cli-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let bad = dir.join("10.11.21.1001.bob.seq");
    std::fs::write(&bad, read("docs/spec/examples/10.11.21.1001.bob.seq").replace("Bob likes", "Bob\tlikes")).unwrap();
    let (ok, out) = run(&["check", bad.to_str().unwrap()]);
    assert!(!ok && out.contains("R4"), "{out}");
    let raw = dir.join("raw.seq");
    std::fs::write(&raw, [b's', b'e', 0xff, b'\n']).unwrap();
    let (ok, out) = run(&["check", raw.to_str().unwrap()]);
    assert!(!ok && out.contains("R4"), "{out}");
}

#[test]
fn import_prints_a_proposal_and_writes_nothing() {
    let before = read("docs/spec/examples/sources/10.11.21.book");
    let (ok, out) = run(&["import", "docs/spec/examples/proposals/10.11.21.1001.bob.seq", "--book", "docs/spec/examples/sources/10.11.21.book", "--by", "grok-bot"]);
    assert!(ok, "{out}");
    let v: serde_json::Value = serde_json::from_str(&out).unwrap();
    assert_eq!(v["proposal"]["by"], "grok-bot");
    assert_eq!(v["proposal"]["ops"][0]["addr"], "10.11.21.1001.06.01");
    assert_eq!(read("docs/spec/examples/sources/10.11.21.book"), before);
}
