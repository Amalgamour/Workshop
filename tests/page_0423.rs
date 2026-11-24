//! Page 90.50.10.0423. One worker: lockout, try-out, release, and a prefix push.
//! Built without Env::ready or Env::open, which face-write before any lockout.

mod common;

use common::{Env, PG};
use std::fs;
use std::process::Command;

const BOOK: &str = "10.10.10.0000";
const WHEN: u64 = 1_795_456_800;
const WHEN_ISO: &str = "2026-11-23T18:00:00Z";

fn start(name: &str) -> Env {
    let e = Env::new(name);
    e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
    e
}

fn lock(e: &Env, face: &str, who: &str, reason: &str) {
    let out = e.ok(&["lockout", PG, face, "--reason", reason, "--as", who]);
    assert!(out.contains("Next: wf try-out"), "{out}");
}

fn unlock(e: &Env, who: &str) {
    let out = e.ok(&["release", PG, "--as", who]);
    assert!(out.contains("no holder"), "{out}");
}

/// Faces, a draft and a pack, then the lock released. Pass 1 sits at pack.
fn packed(name: &str, branch: Option<&str>) -> Env {
    let e = start(name);
    let (ok, out) = e.wf_at(&["lockout", PG, "01", "--reason", "scope", "--as", "pri"], Some(WHEN));
    assert!(ok, "{out}");
    assert!(out.contains("Next: wf try-out"), "{out}");
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass.", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass. Kept.", "--as", "pri"]);
    let see = e.ok(&["try-out", PG, "--as", "pri"]);
    assert!(see.contains("lock holds on face 01"), "{see}");
    assert!(see.contains(&format!("since: {WHEN_ISO}")), "{see}");
    unlock(&e, "pri");
    lock(&e, "04", "pri", "plan");
    e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04", "--as", "pri"]);
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/a.rs\nchecks: cargo --version\nstop if: b must change\n").unwrap();
    e.ok(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"]);
    unlock(&e, "pri");
    lock(&e, "05", "pri", "pack");
    match branch {
        Some(b) => e.ok(&["pack", PG, "1", "--branch", b, "--as", "pri"]),
        None => e.ok(&["pack", PG, "1", "--as", "pri"]),
    };
    unlock(&e, "pri");
    e
}

fn publish_returns(e: &Env) {
    let origin = e.root.join("origin.git");
    let o = Command::new("git").args(["init", "--bare", "-q", origin.to_str().unwrap()]).output().unwrap();
    assert!(o.status.success(), "bare: {}", String::from_utf8_lossy(&o.stderr));
    e.git(&["config", "core.autocrlf", "false"]);
    e.git(&["remote", "add", "origin", origin.to_str().unwrap()]);
    e.git(&["push", "-q", "origin", "main:returns"]);
}

fn commit_published(e: &Env, bytes: &[u8]) {
    let rel = format!(".workshop/logs/{PG}/log.jsonl");
    e.git(&["checkout", "-q", "-B", "returns", "origin/returns"]);
    let path = e.root.join("game").join(&rel);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, bytes).unwrap();
    e.git(&["add", "--", &rel]);
    e.git(&["commit", "-q", "-m", "published log"]);
    e.git(&["push", "-q", "origin", "HEAD:returns"]);
    e.git(&["checkout", "-q", "main"]);
}

fn origin_log(e: &Env) -> Vec<u8> {
    let spec = format!("returns:.workshop/logs/{PG}/log.jsonl");
    let o = Command::new("git").arg("-C").arg(e.root.join("origin.git")).args(["show", &spec]).output().unwrap();
    assert!(o.status.success(), "show: {}", String::from_utf8_lossy(&o.stderr));
    o.stdout
}

fn book(e: &Env) {
    // 0000 is reserved. The test uses the existing system init. release does not.
    e.ok(&["init-page", BOOK, "--title", "book", "--person", "mat", "--prime", "old", "--grant", "src/", "--grant-ref", "tb", "--system", "--system-ref", "tbook", "--as", "mat"]);
    e.ok(&["set-prime", BOOK, "lead", "--ref", "tlead", "--as", "mat"]);
}

#[test]
fn help_names_lockout_try_out_and_release() {
    let e = start("help");
    let help = e.ok(&["help"]);
    assert!(help.contains("lockout <page> <01|04|05> --reason T"), "{help}");
    assert!(help.contains("try-out <page>"), "{help}");
    assert!(help.contains("release <page> [--override --reason T]"), "{help}");
    assert!(help.contains("withdraw <page> <NN>"), "{help}");
    e.no(&["lockout", PG, "02", "--reason", "no", "--as", "pri"], "cannot be locked");
    e.no(&["lockout", PG, "01", "--reason", "   ", "--as", "pri"], "non-blank");
    assert!(!e.log().contains("\"kind\":\"lockout\""));
}

#[test]
fn lockout_on_01_lasts_across_two_face_writes_until_release() {
    let e = start("hold01");
    let (ok, out) = e.wf_at(&["lockout", PG, "01", "--reason", "scope", "--as", "pri"], Some(WHEN));
    assert!(ok, "{out}");
    assert!(out.contains("Next: wf try-out 10.10.10.0401 before work."), "{out}");
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass.", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass. Second.", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "note while 01 is held", "--as", "pri"]);
    let mid = e.log();
    assert_eq!(mid.matches("\"kind\":\"lockout\"").count(), 1, "{mid}");
    let see = e.ok(&["try-out", PG, "--as", "pri"]);
    assert!(see.contains("lock holds on face 01"), "{see}");
    assert!(see.contains("other workers are refused"), "{see}");
    assert!(see.contains("worker: pri"), "{see}");
    assert!(see.contains("reason: scope"), "{see}");
    assert!(see.contains(&format!("since: {WHEN_ISO}")), "{see}");
    assert_eq!(e.log(), mid, "try-out wrote");
    let other = e.ok(&["try-out", PG, "--as", "bob"]);
    assert!(other.contains("you would be refused"), "{other}");
    assert!(other.contains("face 01 is locked by pri"), "{other}");
    assert_eq!(e.log(), mid, "try-out wrote");
    e.no(&["lockout", PG, "04", "--reason", "again", "--as", "pri"], "face 01 is locked by pri");
    e.no(&["lockout", PG, "01", "--reason", "again", "--as", "bob"], "face 01 is locked by pri");
    assert_eq!(e.log().matches("\"kind\":\"lockout\"").count(), 1);
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let err = p.add("bob", "worker", "lockout", serde_json::json!({"face": "05", "reason": "again"})).unwrap_err();
    assert!(err.contains("face 01 is locked by pri"), "{err}");
    unlock(&e, "pri");
    let gone = e.ok(&["try-out", PG, "--as", "bob"]);
    assert!(gone.contains("no lockout holds"), "{gone}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none());
    e.ok(&["lockout", PG, "05", "--reason", "after", "--as", "bob"]);
}

#[test]
fn work_refuses_with_no_lock_and_under_another_workers_lock() {
    let e = start("work");
    let file = e.root.join("pack.txt");
    fs::write(&file, "repo: game\n").unwrap();
    let path = file.to_str().unwrap();
    for args in [
        vec!["face-write", PG, "01", "--text", "x", "--as", "pri"],
        vec!["face-write", PG, "04", "--section", "goals", "--text", "x", "--as", "pri"],
        vec!["face-write", PG, "06", "--text", "x", "--as", "pri"],
        vec!["draft", PG, "--file", path, "--as", "pri"],
        vec!["pack", PG, "1", "--as", "pri"],
        vec!["claim", PG, "1", "--as", "bob"],
        vec!["check", PG, "1", "--as", "cat"],
        vec!["check", PG, "1", "--dry-run", "--as", "cat"],
        vec!["signoff", PG, "1", "--outcome", "failed", "--as", "pri"],
        vec!["close", PG, "1", "--as", "pri"],
    ] {
        e.no(&args, "lockout first");
    }
    assert!(!e.log().contains("\"kind\":\"face\""));
    lock(&e, "01", "pri", "scope");
    e.no(&["face-write", PG, "01", "--text", "x", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["face-write", PG, "04", "--section", "goals", "--text", "x", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["face-write", PG, "02", "--text", "x", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["face-write", PG, "08", "--text", "x", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["draft", PG, "--file", path, "--as", "pri"], "face 01 is locked by pri");
    e.no(&["pack", PG, "1", "--as", "pri"], "face 01 is locked by pri");
    e.no(&["claim", PG, "1", "--as", "bob"], "face 01 is locked by pri");
    e.no(&["check", PG, "1", "--dry-run", "--as", "cat"], "face 01 is locked by pri");
    e.ok(&["face-write", PG, "02", "--text", "sketch", "--as", "pri"]);
    e.ok(&["face-write", PG, "08", "--text", "link", "--as", "pri"]);
    let before = e.log();
    e.no(&["release", PG, "--as", "bob"], "face 01 is locked by pri");
    assert_eq!(e.log(), before);
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let seq = p.hold.as_ref().unwrap().seq;
    let err = p.add("bob", "worker", "release", serde_json::json!({"face": "01", "lockout": seq})).unwrap_err();
    assert!(err.contains("face 01 is locked by pri"), "{err}");
}

#[test]
fn session_05_returns_under_the_lock_and_checks_after_release() {
    let e = packed("sess", None);
    lock(&e, "05", "bob", "claim");
    let see = e.ok(&["try-out", PG, "--as", "bob"]);
    assert!(see.contains("lock holds on face 05"), "{see}");
    assert!(see.contains("other workers are refused"), "{see}");
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(ok, "{out}");
    let held = wf::page::Page::load(&e.page()).unwrap();
    assert_eq!(held.hold.as_ref().unwrap().worker, "bob");
    assert_eq!(held.hold.as_ref().unwrap().face, "05");
    assert_eq!(held.pass(1).unwrap().tail, "return");
    let before = e.log();
    e.no(&["check", PG, "1", "--as", "cat"], "face 05 is locked by bob");
    e.no(&["check", PG, "1", "--dry-run", "--as", "cat"], "face 05 is locked by bob");
    assert_eq!(e.log(), before, "a refused check wrote");
    unlock(&e, "bob");
    e.no(&["check", PG, "1", "--as", "cat"], "lockout first");
    lock(&e, "05", "cat", "check");
    e.no(&["check", PG, "1", "--as", "dog"], "face 05 is locked by cat");
    let checked = e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(checked.contains("check 05.01: pass"), "{checked}");
}

#[test]
fn second_claim_is_refused_while_one_claim_is_open() {
    let e = packed("two", None);
    lock(&e, "05", "bob", "claim 1");
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    unlock(&e, "bob");
    lock(&e, "04", "pri", "draft 2");
    let f = e.root.join("pack2.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: b = 2\nw01: set b to 2\nmay touch: src/b.rs\nchecks: cargo --version\nstop if: a must change\n").unwrap();
    e.ok(&["draft", PG, "--file", f.to_str().unwrap(), "--overlap-ok", "1", "--why", "pass 2 touches a different file (t0423)", "--as", "pri"]);
    unlock(&e, "pri");
    lock(&e, "05", "pri", "pack 2");
    e.ok(&["pack", PG, "2", "--as", "pri"]);
    unlock(&e, "pri");
    lock(&e, "05", "bob", "claim 2");
    e.no(&["claim", PG, "2", "--as", "bob"], "a second claim is refused");
    e.no(&["claim", PG, "1", "--as", "bob"], "first claim wins");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.pass(2).unwrap().claim.is_none());
    assert_eq!(p.pass(1).unwrap().tail, "open");
}

#[test]
fn withdraw_still_runs_without_a_lockout() {
    let e = packed("wd", None);
    let out = e.ok(&["withdraw", PG, "1", "--as", "pri"]);
    assert!(out.contains("withdrew 05.01"), "{out}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert_eq!(p.pass(1).unwrap().tail, "withdrawn");
    assert!(p.hold.is_none());
    assert!(!p.pass(1).unwrap().is_open_tail());
}

#[test]
fn override_accepts_the_book_prime_or_the_person() {
    let e = start("over");
    book(&e);
    lock(&e, "05", "bob", "left");
    let before = e.log();
    e.no(&["release", PG, "--override", "--reason", "holder left", "--as", "pri"], "only the book's Prime");
    e.no(&["release", PG, "--override", "--reason", "holder left", "--as", "old"], "only the book's Prime");
    e.no(&["release", PG, "--override", "--reason", "   ", "--as", "lead"], "non-blank");
    assert_eq!(e.log(), before);
    assert!(!e.log().contains("the book Prime is missing"));
    let out = e.ok(&["release", PG, "--override", "--reason", "holder left", "--as", "lead"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    let log = e.log();
    assert!(log.contains("\"override\":true"), "{log}");
    assert!(log.contains("\"holder\":\"bob\""), "{log}");
    assert!(log.contains("\"reason\":\"holder left\""), "{log}");
    assert!(log.contains("\"face\":\"05\""), "{log}");
    assert!(log.contains(&format!("\"book\":\"{BOOK}\"")), "{log}");
    assert!(log.contains("\"prime\":\"lead\""), "{log}");
    assert!(log.contains("\"revision\":2"), "{log}");
    assert!(log.contains("\"person\":\"mat\""), "{log}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none());
    lock(&e, "04", "bob", "again");
    let out = e.ok(&["release", PG, "--override", "--reason", "person clears it", "--as", "mat"]);
    assert!(out.contains("override released face 04 held by bob"), "{out}");
    assert!(e.log().contains("\"reason\":\"person clears it\""));
    e.ok(&["lockout", PG, "01", "--reason", "after override", "--as", "pri"]);
}

#[test]
fn missing_book_lets_only_the_person_override() {
    let e = start("miss");
    lock(&e, "05", "bob", "left");
    let before = e.log();
    e.no(&["release", PG, "--override", "--reason", "holder left", "--as", "pri"], "the book Prime is missing");
    assert_eq!(e.log(), before);
    let out = e.ok(&["release", PG, "--override", "--reason", "holder left", "--as", "mat"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    let log = e.log();
    let release = log.lines().find(|l| l.contains("\"kind\":\"release\"")).unwrap();
    assert!(release.contains("\"override\":true"), "{release}");
    assert!(release.contains("\"fallback\":\"missing-book\""), "{release}");
    assert!(release.contains(&format!("\"book\":\"{BOOK}\"")), "{release}");
    assert!(release.contains("\"person\":\"mat\""), "{release}");
    assert!(!release.contains("\"prime\""), "{release}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none());
}

#[test]
fn push_refuses_when_the_published_log_is_not_a_prefix() {
    let e = packed("push-no", Some("returns"));
    publish_returns(&e);
    lock(&e, "05", "bob", "claim");
    e.ok(&["try-out", PG, "--as", "bob"]);
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    let published = b"not-the-page-log\n";
    commit_published(&e, published);
    let name = format!(".workshop/returns/{PG}.05.01.md");
    let (ok, out) = e.wf(&["return", PG, "1", "--branch", "returns", "--commit", &sha, "--file", &name, "--push", "--as", "bob"]);
    assert!(!ok, "{out}");
    assert!(out.contains("the published log is not a prefix"), "{out}");
    assert!(out.contains("Intake the published log"), "{out}");
    assert_eq!(origin_log(&e), published);
}

#[test]
fn push_accepts_a_prefix_extension() {
    let e = packed("push-yes", Some("returns"));
    publish_returns(&e);
    lock(&e, "05", "bob", "claim");
    let see = e.ok(&["try-out", PG, "--as", "bob"]);
    assert!(see.contains("lock holds on face 05"), "{see}");
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    let before = fs::read(e.page().join("log.jsonl")).unwrap();
    commit_published(&e, &before);
    let name = format!(".workshop/returns/{PG}.05.01.md");
    let (ok, out) = e.wf(&["return", PG, "1", "--branch", "returns", "--commit", &sha, "--file", &name, "--push", "--as", "bob"]);
    assert!(ok, "{out}");
    assert!(out.contains("pushed returns"), "{out}");
    let local = fs::read(e.page().join("log.jsonl")).unwrap();
    assert!(local.starts_with(&before), "local log is not an extension of the published prefix");
    assert!(local.len() > before.len());
    assert_eq!(origin_log(&e), local);
    let held = wf::page::Page::load(&e.page()).unwrap();
    assert_eq!(held.hold.as_ref().map(|h| h.worker.as_str()), Some("bob"));
}

const FULL: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
/// Published logs at the start commit. Copied out of the repo before status and verify.
const PUBLISHED_0408: &[u8] = include_bytes!("../.workshop/logs/90.50.10.0408/log.jsonl");
const PUBLISHED_0423: &[u8] = include_bytes!("../.workshop/logs/90.50.10.0423/log.jsonl");

fn raw(dir: &std::path::Path, actor: &str, role: &str, kind: &str, data: serde_json::Value) {
    let path = dir.join("log.jsonl");
    let (n, head) = if path.is_file() {
        let (ev, head) = wf::log::read(&path).unwrap();
        (ev.len() as u64 + 1, head)
    } else {
        (1, "0".into())
    };
    wf::log::append(&path, &head, n, actor, role, kind, data).unwrap();
}

/// A finished pass written the way earlier wf wrote it: no lockout entry.
fn write_closed_without_lock(dir: &std::path::Path) {
    raw(dir, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri", "grant": ["src/"], "grant_ref": "t1"}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "04", "mode": "append", "section": "goals", "text": "a works"}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "01", "mode": "replace", "section": "", "text": "Goal: a.\nDone when: checks pass."}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "06", "mode": "append", "section": "note", "text": "read 04"}));
    raw(dir, "pri", "prime", "draft", serde_json::json!({"pass": 1, "fields": {"w01": "set a"}, "pins": {}}));
    raw(dir, "pri", "prime", "pack", serde_json::json!({"pass": 1}));
    raw(dir, "bob", "builder", "claim", serde_json::json!({"pass": 1}));
    raw(dir, "bob", "builder", "return", serde_json::json!({"pass": 1, "commit": FULL}));
    raw(dir, "cat", "checker", "check", serde_json::json!({"pass": 1, "verdict": "pass", "commit": FULL}));
    raw(dir, "pri", "prime", "signoff", serde_json::json!({"pass": 1, "outcome": "passed"}));
    raw(dir, "pri", "prime", "close", serde_json::json!({"pass": 1}));
}

fn write_legacy_faces(dir: &std::path::Path) {
    raw(dir, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri", "grant": ["src/"], "grant_ref": "t1"}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "04", "mode": "append", "section": "goals", "text": "a works"}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "01", "mode": "replace", "section": "", "text": "Goal: a.\nDone when: checks pass."}));
    raw(dir, "pri", "prime", "face", serde_json::json!({"face": "06", "mode": "append", "section": "note", "text": "read 04"}));
}

fn reprint(dir: &std::path::Path) {
    let p = wf::page::Page::load(dir).unwrap();
    wf::render::write(&p).unwrap();
}

fn load_err(dir: &std::path::Path, want: &str) {
    match wf::page::Page::load(dir) {
        Err(err) => {
            assert!(err.contains(want), "{err}");
            assert!(err.contains("cannot be read"), "{err}");
        }
        Ok(_) => panic!("page loaded: {want}"),
    }
}

/// Status, then verify. Reprint views from the log when the recorded hashes still match.
/// Either way the log bytes stay equal to `bytes`.
fn status_and_verify(e: &Env, addr: &str, bytes: &[u8]) {
    let dir = e.root.join("pages").join(addr);
    fs::create_dir_all(&dir).unwrap();
    let log = dir.join("log.jsonl");
    fs::write(&log, bytes).unwrap();
    let status = e.ok(&["status", addr]);
    assert!(status.contains(&format!("page {addr}")), "{status}");
    assert!(status.contains("entries"), "{status}");
    let page = wf::page::Page::load(&dir).unwrap();
    assert!(!page.events.is_empty());
    let reprinted = wf::render::write(&page);
    let (ok, verify) = e.wf(&["verify", addr]);
    assert_eq!(fs::read(&log).unwrap(), bytes, "status or verify changed the log");
    match reprinted {
        Ok(()) => {
            assert!(ok, "{verify}");
            assert!(verify.contains("log chain holds"), "{verify}");
        }
        Err(err) => {
            assert!(!err.contains("out of order") && !err.contains("lockout first"), "{err}");
            assert!(!ok, "{verify}");
            assert!(!verify.contains("out of order") && !verify.contains("lockout first"), "{verify}");
        }
    }
}

#[test]
fn pre_lockout_order_loads_and_a_new_write_still_needs_a_lock() {
    let e = Env::new("prelock");
    let dir = e.page();
    fs::create_dir_all(&dir).unwrap();
    write_closed_without_lock(&dir);
    let bytes = fs::read(dir.join("log.jsonl")).unwrap();
    let p = wf::page::Page::load(&dir).unwrap();
    assert_eq!(p.pass(1).unwrap().tail, "closed");
    assert!(p.hold.is_none());
    assert!(!p.seen_lockout);
    assert!(!std::str::from_utf8(&bytes).unwrap().contains("lockout"));
    let status = e.ok(&["status", PG]);
    assert!(status.contains("05.01"), "{status}");
    assert!(status.contains("closed"), "{status}");
    reprint(&dir);
    let file = e.root.join("pack.txt");
    fs::write(&file, "repo: game\n").unwrap();
    e.no(&["face-write", PG, "01", "--text", "Goal: later.", "--as", "pri"], "lockout first");
    e.no(&["draft", PG, "--file", file.to_str().unwrap(), "--as", "pri"], "lockout first");
    e.no(&["pack", PG, "1", "--as", "pri"], "lockout first");
    e.no(&["claim", PG, "1", "--as", "bob"], "lockout first");
    let mut p = wf::page::Page::load(&dir).unwrap();
    let err = p.add("pri", "prime", "face", serde_json::json!({"face": "01", "mode": "replace", "section": "", "text": "n"})).unwrap_err();
    assert!(err.contains("lockout first"), "{err}");
    assert!(err.contains("nothing written"), "{err}");
    assert_eq!(fs::read(dir.join("log.jsonl")).unwrap(), bytes);
}

#[test]
fn legacy_page_takes_its_first_lock_and_release_does_not_restore_the_exemption() {
    let e = Env::new("legacy");
    let dir = e.page();
    fs::create_dir_all(&dir).unwrap();
    write_legacy_faces(&dir);
    let prefix = fs::read(dir.join("log.jsonl")).unwrap();
    let p = wf::page::Page::load(&dir).unwrap();
    assert!(!p.seen_lockout);
    assert_eq!(p.faces.get("01").map(|f| f.version), Some(1));
    reprint(&dir);
    e.no(&["face-write", PG, "06", "--text", "new note", "--as", "pri"], "lockout first");
    assert_eq!(fs::read(dir.join("log.jsonl")).unwrap(), prefix);
    lock(&e, "01", "pri", "first lock on a legacy page");
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass. Kept.", "--as", "pri"]);
    unlock(&e, "pri");
    e.no(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: after.", "--as", "pri"], "lockout first");
    e.no(&["face-write", PG, "06", "--text", "after release", "--as", "pri"], "lockout first");
    let p = wf::page::Page::load(&dir).unwrap();
    assert!(p.seen_lockout);
    assert!(p.hold.is_none());
    let now = fs::read(dir.join("log.jsonl")).unwrap();
    assert!(now.starts_with(&prefix), "the legacy prefix was rewritten");
    assert!(now.len() > prefix.len());
}

#[test]
fn post_lockout_replay_checks_lifecycle() {
    let e = Env::new("life");
    let good = e.root.join("good");
    fs::create_dir_all(&good).unwrap();
    raw(&good, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&good, "pri", "worker", "lockout", serde_json::json!({"face": "01", "reason": "scope"}));
    raw(&good, "pri", "prime", "face", serde_json::json!({"face": "01", "mode": "replace", "section": "", "text": "Goal"}));
    raw(&good, "pri", "worker", "release", serde_json::json!({"face": "01", "lockout": 2}));
    raw(&good, "pri", "worker", "lockout", serde_json::json!({"face": "04", "reason": "plan"}));
    raw(&good, "pri", "prime", "face", serde_json::json!({"face": "06", "mode": "append", "section": "note", "text": "while 04 is held"}));
    let p = wf::page::Page::load(&good).unwrap();
    assert!(p.seen_lockout);
    assert_eq!(p.hold.as_ref().map(|h| h.face.as_str()), Some("04"));
    assert_eq!(p.hold.as_ref().map(|h| h.worker.as_str()), Some("pri"));

    let bare = e.root.join("release-first");
    fs::create_dir_all(&bare).unwrap();
    raw(&bare, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&bare, "pri", "worker", "release", serde_json::json!({"face": "01", "lockout": 1}));
    load_err(&bare, "no lockout holds");

    let twice = e.root.join("second-lock");
    fs::create_dir_all(&twice).unwrap();
    raw(&twice, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&twice, "pri", "worker", "lockout", serde_json::json!({"face": "01", "reason": "scope"}));
    raw(&twice, "pri", "worker", "lockout", serde_json::json!({"face": "04", "reason": "again"}));
    load_err(&twice, "face 01 is locked by pri");

    let wrong = e.root.join("wrong-holder");
    fs::create_dir_all(&wrong).unwrap();
    raw(&wrong, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&wrong, "pri", "worker", "lockout", serde_json::json!({"face": "01", "reason": "scope"}));
    raw(&wrong, "bob", "prime", "face", serde_json::json!({"face": "01", "mode": "replace", "section": "", "text": "no"}));
    load_err(&wrong, "face 01 is locked by pri");

    let after = e.root.join("after-release");
    fs::create_dir_all(&after).unwrap();
    raw(&after, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&after, "pri", "worker", "lockout", serde_json::json!({"face": "05", "reason": "session"}));
    raw(&after, "pri", "worker", "release", serde_json::json!({"face": "05", "lockout": 2}));
    raw(&after, "pri", "prime", "pack", serde_json::json!({"pass": 1}));
    load_err(&after, "lockout first");

    let other = e.root.join("other-release");
    fs::create_dir_all(&other).unwrap();
    raw(&other, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&other, "pri", "worker", "lockout", serde_json::json!({"face": "05", "reason": "session"}));
    raw(&other, "bob", "worker", "release", serde_json::json!({"face": "05", "lockout": 2}));
    load_err(&other, "face 05 is locked by pri");
}

#[test]
fn published_0408_and_0423_logs_load_without_changing_bytes() {
    let e = Env::new("published");
    assert!(PUBLISHED_0408.starts_with(b"{"), "0408 log");
    assert!(PUBLISHED_0423.starts_with(b"{"), "0423 log");
    status_and_verify(&e, "90.50.10.0408", PUBLISHED_0408);
    status_and_verify(&e, "90.50.10.0423", PUBLISHED_0423);
    let repo = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let spec = "origin/returns:.workshop/logs/90.50.10.0423/log.jsonl";
    let shown = Command::new("git").arg("-C").arg(&repo).args(["show", spec]).output().unwrap();
    if shown.status.success() && shown.stdout.starts_with(b"{") {
        assert_ne!(shown.stdout, PUBLISHED_0423, "origin/returns 0423 should be the later published log");
        status_and_verify(&e, "90.50.10.0423", &shown.stdout);
    }
}

#[test]
fn override_basis_survives_book_prime_succession() {
    let e = start("succ");
    book(&e);
    let book = wf::page::Page::load(&e.root.join("pages").join(BOOK)).unwrap();
    assert_eq!(book.primes.last().map(|(_, from, _)| *from), Some(2));
    lock(&e, "05", "bob", "left");
    let out = e.ok(&["release", PG, "--override", "--reason", "holder left", "--as", "lead"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    let recorded = e.log();
    assert!(recorded.contains("\"prime\":\"lead\""), "{recorded}");
    assert!(recorded.contains("\"revision\":2"), "{recorded}");
    e.ok(&["set-prime", BOOK, "bea", "--ref", "tbea", "--as", "mat"]);
    let book = wf::page::Page::load(&e.root.join("pages").join(BOOK)).unwrap();
    assert_eq!(book.prime, "bea");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none());
    assert!(p.seen_lockout);
    assert_eq!(e.log(), recorded, "succession rewrote the work page");
    lock(&e, "05", "bob", "fresh");
    let held = e.log();
    e.no(&["release", PG, "--override", "--reason", "former prime", "--as", "lead"], "only the book's Prime");
    e.no(&["release", PG, "--override", "--reason", "work prime", "--as", "pri"], "only the book's Prime");
    e.no(&["release", PG, "--override", "--reason", "first prime", "--as", "old"], "only the book's Prime");
    assert_eq!(e.log(), held);
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let seq = p.hold.as_ref().unwrap().seq;
    let stale = serde_json::json!({
        "face": "05", "lockout": seq, "holder": "bob", "override": true, "reason": "stale",
        "basis": {"book": BOOK, "person": "mat", "prime": "lead", "revision": 2}
    });
    let err = p.add("bea", "prime", "release", stale).unwrap_err();
    assert!(err.contains("live authority basis"), "{err}");
    let err = p.add("bea", "prime", "release", serde_json::json!({"face": "05", "lockout": seq, "holder": "bob", "override": true, "reason": "no basis"})).unwrap_err();
    assert!(err.contains("live authority basis"), "{err}");
    assert_eq!(e.log(), held);
    let out = e.ok(&["release", PG, "--override", "--reason", "current prime", "--as", "bea"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    assert!(e.log().contains("\"prime\":\"bea\""));
    lock(&e, "01", "bob", "person");
    let out = e.ok(&["release", PG, "--override", "--reason", "the person", "--as", "mat"]);
    assert!(out.contains("override released face 01 held by bob"), "{out}");
    assert!(e.log().contains("\"role\":\"person\""));
}

#[test]
fn old_shape_override_reloads_after_succession_and_a_new_one_needs_live_authority() {
    let e = start("oldshape");
    book(&e);
    e.ok(&["set-prime", BOOK, "bea", "--ref", "tbea", "--as", "mat"]);
    lock(&e, "05", "bob", "left");
    let hold = wf::page::Page::load(&e.page()).unwrap().hold.unwrap();
    raw(&e.page(), "lead", "prime", "release", serde_json::json!({
        "face": hold.face, "lockout": hold.seq, "holder": hold.worker, "override": true, "reason": "recorded while lead was Prime"
    }));
    let legacy = e.log();
    assert!(!legacy.contains("\"basis\""), "{legacy}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none(), "old-shape override did not release");
    assert_eq!(p.events.last().unwrap().role, "prime");
    e.ok(&["set-prime", BOOK, "cara", "--ref", "tcara", "--as", "mat"]);
    let p = wf::page::Page::load(&e.page()).unwrap();
    assert!(p.hold.is_none());
    assert_eq!(e.log(), legacy, "a later Prime rewrote the old override");
    reprint(&e.page());

    // The book Prime is cara. Replay must still refuse an actor the recorded basis does not name.
    let forged = e.root.join("pages").join("10.10.10.0402");
    fs::create_dir_all(&forged).unwrap();
    raw(&forged, "mat", "person", "init", serde_json::json!({"address": "10.10.10.0402", "title": "t", "person": "mat", "prime": "pri"}));
    raw(&forged, "bob", "worker", "lockout", serde_json::json!({"face": "05", "reason": "left"}));
    raw(&forged, "cara", "prime", "release", serde_json::json!({
        "face": "05", "lockout": 2, "holder": "bob", "override": true, "reason": "named the old prime",
        "basis": {"book": BOOK, "person": "mat", "prime": "lead", "revision": 2}
    }));
    load_err(&forged, "does not match the recorded authority");

    let worker = e.root.join("worker-role");
    fs::create_dir_all(&worker).unwrap();
    raw(&worker, "mat", "person", "init", serde_json::json!({"address": PG, "title": "t", "person": "mat", "prime": "pri"}));
    raw(&worker, "bob", "worker", "lockout", serde_json::json!({"face": "05", "reason": "left"}));
    raw(&worker, "lead", "worker", "release", serde_json::json!({
        "face": "05", "lockout": 2, "holder": "bob", "override": true, "reason": "wrong role"
    }));
    load_err(&worker, "not prime or person");

    lock(&e, "05", "bob", "fresh");
    let held = fs::read(e.page().join("log.jsonl")).unwrap();
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let seq = p.hold.as_ref().unwrap().seq;
    let err = p.add("cara", "prime", "release", serde_json::json!({"face": "05", "lockout": seq, "holder": "bob", "override": true, "reason": "old shape"})).unwrap_err();
    assert!(err.contains("live authority basis"), "{err}");
    assert_eq!(fs::read(e.page().join("log.jsonl")).unwrap(), held);
    let out = e.ok(&["release", PG, "--override", "--reason", "current prime", "--as", "cara"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    assert!(e.log().contains("\"basis\""));
    assert!(e.log().contains("\"prime\":\"cara\""));
}

#[test]
fn push_log_does_not_pull_merge() {
    let src = include_str!("../src/cmd.rs");
    let start = src.find("fn push_log(").expect("push_log");
    let body = &src[start..];
    let end = body.find("pub fn publish_pack").expect("publish_pack");
    let body = &body[..end];
    assert!(!body.contains("\"pull\""), "{body}");
    assert!(!body.contains("--force"), "{body}");
    assert!(body.contains("PREFIX_REFUSAL"), "{body}");
}
