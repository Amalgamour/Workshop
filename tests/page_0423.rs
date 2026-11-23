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
    assert!(e.log().contains("\"override\":true"));
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
