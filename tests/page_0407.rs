//! Page 90.50.10.0407. A band door's face 00 lists the band from the pages folder.
//! The log has no dropped state (retire is page 0409). This file does not invent one.

use serde_json::json;
use std::fs;
use std::path::{Path, PathBuf};
use wf::page::Page;
use wf::render;

fn work_dir(name: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("wf-page-0407-{}-{name}", std::process::id()));
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(dir.join("pages")).unwrap();
    dir
}

fn init(pages: &Path, addr: &str, title: &str) -> Page {
    let dir = pages.join(addr);
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("log.jsonl"), "").unwrap();
    let mut p = Page::load(&dir).unwrap();
    p.add("mat", "person", "init", json!({
        "address": addr,
        "title": title,
        "person": "mat",
        "prime": "pri",
        "grant": ["src/"],
        "grant_ref": "t1"
    })).unwrap();
    p
}

fn stamp(p: &Page) -> String {
    render::write(p).unwrap();
    fs::read_to_string(p.dir.join("00.md")).unwrap()
}

#[test]
fn a_band_door_lists_each_page_with_its_log_state_and_a_non_door_has_no_list() {
    let root = work_dir("band");
    let pages = root.join("pages");
    let door = init(&pages, "10.10.10.0400", "door");

    let mut open = init(&pages, "10.10.10.0401", "open page");
    open.add("pri", "prime", "draft", json!({"pass": 1, "fields": {}, "pins": {}})).unwrap();
    open.add("pri", "prime", "pack", json!({
        "pass": 1, "pack_text": "p\n", "pack_hash": "ab", "branch": "b",
        "return_file": "f", "start": "0", "templates": "1", "sources": {}
    })).unwrap();
    open.add("bob", "builder", "claim", json!({"pass": 1})).unwrap();

    let mut closed = init(&pages, "10.10.10.0402", "closed page");
    let commit = "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12";
    closed.add("pri", "prime", "draft", json!({"pass": 1, "fields": {}, "pins": {}})).unwrap();
    closed.add("pri", "prime", "pack", json!({
        "pass": 1, "pack_text": "p\n", "pack_hash": format!("{:064}", 1), "branch": "b",
        "return_file": "f", "start": "0", "templates": "1", "sources": {}
    })).unwrap();
    closed.add("bob", "builder", "claim", json!({"pass": 1})).unwrap();
    closed.add("bob", "builder", "return", json!({"pass": 1, "commit": commit, "file": "f", "jobs": {}})).unwrap();
    closed.add("cat", "checker", "check", json!({"pass": 1, "commit": commit, "verdict": "pass", "report": ""})).unwrap();
    closed.add("pri", "prime", "signoff", json!({"pass": 1, "outcome": "passed", "cards": {}})).unwrap();
    closed.add("pri", "tool", "close", json!({"pass": 1, "outcome": "passed"})).unwrap();

    let mut halted = init(&pages, "10.10.10.0403", "halted page");
    halted.add("pri", "prime", "halt", json!({"note": "wait (t1)"})).unwrap();

    fs::create_dir_all(pages.join("10.10.10.0404")).unwrap();
    let other = init(&pages, "10.10.10.0501", "other band");
    fs::create_dir_all(pages.join("notes")).unwrap();

    let door = Page::load(&door.dir).unwrap();
    let text = stamp(&door);
    assert!(text.contains("type: band\n"), "{text}");
    for line in [
        "  10.10.10.0400  init\n",
        "  10.10.10.0401  open\n",
        "  10.10.10.0402  closed\n",
        "  10.10.10.0403  halted\n",
        "  10.10.10.0404  unreadable: no log.jsonl\n",
    ] {
        assert!(text.contains(line), "missing {line} in {text}");
    }
    assert!(!text.contains("10.10.10.0501"), "{text}");
    assert!(!text.contains("notes"), "{text}");
    assert!(!text.contains("dropped"), "{text}");

    let item = stamp(&open);
    assert!(item.contains("title:   open page\n"), "{item}");
    assert!(!item.contains("type: band"), "{item}");
    assert!(!item.contains("contents:"), "{item}");

    let elsewhere = stamp(&other);
    assert!(!elsewhere.contains("type: band"), "{elsewhere}");
    assert!(!elsewhere.contains("contents:"), "{elsewhere}");

    let _ = fs::remove_dir_all(&root);
}
