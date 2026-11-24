//! Independent trial of the released 0423 binary.
//! The binary is the one cargo builds for this checkout (`CARGO_BIN_EXE_wf`),
//! not the workflow install. Every command is a process. Temporary pages and
//! local bare remotes only.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

const PAGE: &str = "10.20.30.0401";
const OTHER: &str = "10.20.30.0402";
const BOOK: &str = "10.20.30.0000";
const FAILED_BUILD: &str = "1b0d2c123f7fc8537dcac1e6819f2456a781890f";
const PREFIX_REFUSAL: &str = "refused: the published log is not a prefix of this page's log. Intake the published log and return again so new events append.";
/// `wf release` writes only the local log. This is the step that puts that log where a fresh root can intake it.
const PUBLICATION_STEP: &str = "commit the unchanged generated log by path on the fixture returns branch and push that branch";

struct Root {
    root: PathBuf,
}

impl Drop for Root {
    fn drop(&mut self) {
        if self.root.exists() {
        let _ = Command::new("cmd").args(["/C", "rmdir", "/S", "/Q"]).arg(&self.root).status();
    }
    }
}

struct Ev {
    actor: String,
    kind: String,
}

fn temp_root(name: &str) -> PathBuf {
    let n = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    std::env::temp_dir().join(format!("lab0423-{}-{name}-{n}", std::process::id()))
}

fn git(dir: &Path, args: &[&str]) -> String {
    let o = Command::new("git")
        .current_dir(dir)
        .args(["-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"])
        .args(args)
        .output()
        .unwrap();
    assert!(
        o.status.success(),
        "git {args:?} in {}: {}\n{}",
        dir.display(),
        String::from_utf8_lossy(&o.stderr),
        String::from_utf8_lossy(&o.stdout)
    );
    String::from_utf8_lossy(&o.stdout).trim().to_string()
}

fn git_out(dir: &Path, args: &[&str]) -> (bool, String) {
    let o = Command::new("git")
        .current_dir(dir)
        .args(["-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false"])
        .args(args)
        .output()
        .unwrap();
    (
        o.status.success(),
        format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)),
    )
}

fn run_bin(bin: &Path, root: &Path, args: &[&str]) -> (bool, String) {
    let o = Command::new(bin)
        .env("WF_ROOT", root)
        .env_remove("WF_AS")
        .env_remove("WF_NOW")
        .args(args)
        .output()
        .unwrap();
    (
        o.status.success(),
        format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)),
    )
}

fn wf(root: &Path, args: &[&str]) -> (bool, String) {
    run_bin(Path::new(env!("CARGO_BIN_EXE_wf")), root, args)
}

fn must(root: &Path, args: &[&str]) -> String {
    let (ok, out) = wf(root, args);
    assert!(ok, "wf {args:?} failed: {out}");
    out
}

fn must_bin(bin: &Path, root: &Path, args: &[&str]) -> String {
    let (ok, out) = run_bin(bin, root, args);
    assert!(ok, "{bin:?} {args:?} failed: {out}");
    out
}

fn refuse(root: &Path, args: &[&str], want: &str) {
    let (ok, out) = wf(root, args);
    assert!(!ok, "wf {args:?} should be refused: {out}");
    assert!(out.contains(want), "wf {args:?}: expected '{want}' in: {out}");
}

fn new_root(name: &str) -> Root {
    let root = temp_root(name);
    fs::create_dir_all(root.join("work/src")).unwrap();
    let work = root.join("work");
    git(&work, &["init", "-q", "-b", "main"]);
    git(&work, &["config", "core.autocrlf", "false"]);
    fs::write(work.join("src/a.rs"), "a = 1\n").unwrap();
    fs::write(work.join("src/b.rs"), "b = 1\n").unwrap();
    git(&work, &["add", "--", "src/a.rs", "src/b.rs"]);
    git(&work, &["commit", "-q", "-m", "start"]);
    Root { root }
}

fn init_page(root: &Path, addr: &str, prime: &str) {
    must(root, &[
        "init-page", addr, "--title", "t", "--person", "mat", "--prime", prime, "--grant", "src/",
        "--grant-ref", "t1", "--as", "mat",
    ]);
}

fn init_page_bin(bin: &Path, root: &Path, addr: &str, prime: &str) {
    must_bin(bin, root, &[
        "init-page", addr, "--title", "t", "--person", "mat", "--prime", prime, "--grant", "src/",
        "--grant-ref", "t1", "--as", "mat",
    ]);
}

fn log_path(root: &Path, addr: &str) -> PathBuf {
    root.join("pages").join(addr).join("log.jsonl")
}

fn read_log(root: &Path, addr: &str) -> Vec<u8> {
    fs::read(log_path(root, addr)).unwrap()
}

fn field(line: &str, key: &str) -> String {
    let pat = format!("\"{key}\":\"");
    let i = line.find(&pat).unwrap_or_else(|| panic!("no {key} in {line}"));
    let rest = &line[i + pat.len()..];
    rest[..rest.find('"').unwrap()].to_string()
}

fn events(bytes: &[u8]) -> Vec<Ev> {
    String::from_utf8(bytes.to_vec())
        .unwrap()
        .lines()
        .filter(|l| !l.is_empty())
        .map(|l| Ev { actor: field(l, "actor"), kind: field(l, "kind") })
        .collect()
}

fn copy_dir(src: &Path, dst: &Path) {
    fs::create_dir_all(dst).unwrap();
    for ent in fs::read_dir(src).unwrap() {
        let ent = ent.unwrap();
        if ent.file_name() == ".wf-lock" {
            continue;
        }
        let to = dst.join(ent.file_name());
        if ent.file_type().unwrap().is_dir() {
            copy_dir(&ent.path(), &to);
        } else {
            fs::copy(ent.path(), &to).unwrap();
        }
    }
}

fn attach_bare(r: &Root) -> PathBuf {
    let origin = r.root.join("origin.git");
    let made = Command::new("git").args(["init", "--bare", "-q"]).arg(&origin).output().unwrap();
    assert!(made.status.success(), "bare: {}", String::from_utf8_lossy(&made.stderr));
    let work = r.root.join("work");
    git(&work, &["remote", "add", "origin", origin.to_str().unwrap()]);
    git(&work, &["push", "-q", "origin", "main:refs/heads/returns"]);
    git(&work, &["fetch", "-q", "origin", "returns"]);
    origin
}

fn origin_log(bare: &Path, addr: &str) -> Vec<u8> {
    let spec = format!("returns:.workshop/logs/{addr}/log.jsonl");
    let o = Command::new("git").arg("-C").arg(bare).args(["show", &spec]).output().unwrap();
    assert!(o.status.success(), "show {spec}: {}", String::from_utf8_lossy(&o.stderr));
    o.stdout
}

fn commit_published(r: &Root, addr: &str, bytes: &[u8]) {
    let work = r.root.join("work");
    git(&work, &["checkout", "-q", "-B", "returns", "origin/returns"]);
    let rel = format!(".workshop/logs/{addr}/log.jsonl");
    let path = work.join(&rel);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, bytes).unwrap();
    git(&work, &["add", "--", &rel]);
    git(&work, &["commit", "-q", "-m", "published log", "--", &rel]);
    git(&work, &["push", "-q", "origin", "HEAD:refs/heads/returns"]);
    git(&work, &["checkout", "-q", "main"]);
}

/// Faces, a draft and a pack on `branch`, then the lock released. Pass 1 sits at pack.
fn packed(name: &str, addr: &str) -> Root {
    let r = new_root(name);
    attach_bare(&r);
    init_page(&r.root, addr, "pri");
    must(&r.root, &["lockout", addr, "01", "--reason", "scope", "--as", "pri"]);
    must(&r.root, &["face-write", addr, "01", "--text", "Goal: a.\nDone when: checks pass.", "--as", "pri"]);
    must(&r.root, &["release", addr, "--as", "pri"]);
    must(&r.root, &["lockout", addr, "04", "--reason", "plan", "--as", "pri"]);
    must(&r.root, &["face-write", addr, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
    must(&r.root, &["face-write", addr, "06", "--text", "read 04", "--as", "pri"]);
    let pack = r.root.join("pack.txt");
    fs::write(
        &pack,
        "repo: work\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/a.rs\nchecks: cargo --version\nstop if: b must change\n",
    )
    .unwrap();
    must(&r.root, &["draft", addr, "--file", pack.to_str().unwrap(), "--as", "pri"]);
    must(&r.root, &["release", addr, "--as", "pri"]);
    must(&r.root, &["lockout", addr, "05", "--reason", "pack", "--as", "pri"]);
    must(&r.root, &["pack", addr, "1", "--branch", "returns", "--as", "pri"]);
    must(&r.root, &["release", addr, "--as", "pri"]);
    r
}

fn pack_hash(root: &Path, addr: &str) -> String {
    let text = fs::read_to_string(root.join("pages").join(addr).join("05.01/PROMPT.md")).unwrap();
    text.lines()
        .find_map(|l| l.strip_prefix("Pack hash: "))
        .unwrap()
        .split_whitespace()
        .next()
        .unwrap()
        .to_string()
}

fn work_commit(r: &Root, addr: &str, hash: &str) -> String {
    let work = r.root.join("work");
    git(&work, &["checkout", "-q", "-B", "returns", "main"]);
    fs::write(work.join("src/a.rs"), "a = 2\n").unwrap();
    let rel = format!(".workshop/returns/{addr}.05.01.md");
    fs::create_dir_all(work.join(".workshop/returns")).unwrap();
    let text = format!(
        "pack: {hash}\ndone: set a to 2\nchanged: modify src/a.rs\nnoticed: none\nw01: done - a is 2\nproof: cargo --version\ndesign review: fixture compared the kit rules\nnot done: none\nunprompted: none\noverflow: none\n"
    );
    fs::write(work.join(&rel), text).unwrap();
    git(&work, &["add", "--", "src/a.rs", &rel]);
    git(&work, &["commit", "-q", "-m", "work"]);
    git(&work, &["rev-parse", "HEAD"])
}

fn return_args<'a>(addr: &'a str, sha: &'a str, file: &'a str, push: bool) -> Vec<&'a str> {
    let mut v = vec!["return", addr, "1", "--branch", "returns", "--commit", sha, "--file", file, "--as", "bob"];
    if push {
        v.push("--push");
    }
    v
}

/// Merge the work commit, then commit `bytes` by path and push. No force.
fn publish_generated(r: &Root, addr: &str, work_sha: &str, bytes: &[u8]) {
    let work = r.root.join("work");
    git(&work, &["checkout", "-q", "-B", "returns", "origin/returns"]);
    let (ok, out) = git_out(&work, &["merge", "-q", "--no-edit", work_sha]);
    assert!(ok, "merge {work_sha}: {out}");
    let rel = format!(".workshop/logs/{addr}/log.jsonl");
    let path = work.join(&rel);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, bytes).unwrap();
    git(&work, &["add", "--", &rel]);
    let quiet = Command::new("git")
        .current_dir(&work)
        .args(["diff", "--cached", "--quiet", "--", &rel])
        .status()
        .unwrap();
    match quiet.code() {
        Some(0) => {}
        Some(1) => {
            git(&work, &["commit", "-q", "-m", "publish generated log", "--", &rel]);
        }
        _ => panic!("git diff --cached failed"),
    }
    git(&work, &["push", "-q", "origin", "HEAD:refs/heads/returns"]);
}

fn fresh_checker(bare: &Path, page_src: &Path, addr: &str) -> Root {
    let root = temp_root("checker");
    fs::create_dir_all(root.join("pages")).unwrap();
    copy_dir(page_src, &root.join("pages").join(addr));
    let work = root.join("work");
    fs::create_dir_all(&work).unwrap();
    git(&work, &["init", "-q", "-b", "main"]);
    git(&work, &["config", "core.autocrlf", "false"]);
    git(&work, &["remote", "add", "origin", bare.to_str().unwrap()]);
    git(&work, &["fetch", "-q", "origin", "returns"]);
    git(&work, &["checkout", "-q", "-B", "returns", "origin/returns"]);
    Root { root }
}

fn failed_build_bin() -> PathBuf {
    let dir = std::env::temp_dir().join("lab0423-failed-1b0d2c1");
    let bin = dir.join("target").join("debug").join("wf.exe");
    let stamp = dir.join("built-from.txt");
    if bin.is_file() && fs::read_to_string(&stamp).ok().as_deref() == Some(FAILED_BUILD) {
        return bin;
    }
    if dir.exists() {
        let _ = Command::new("cmd").args(["/C", "rmdir", "/S", "/Q"]).arg(&dir).status();
    }
    let src = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let cloned = Command::new("git")
        .args(["clone", "--shared", "-q", "-c", "core.autocrlf=false"])
        .arg(&src)
        .arg(&dir)
        .output()
        .unwrap();
    assert!(cloned.status.success(), "clone 1b0d2c1: {}", String::from_utf8_lossy(&cloned.stderr));
    let switched = Command::new("git")
        .args(["-C"])
        .arg(&dir)
        .args(["checkout", "-q", "--detach", FAILED_BUILD])
        .output()
        .unwrap();
    assert!(switched.status.success(), "checkout 1b0d2c1: {}", String::from_utf8_lossy(&switched.stderr));
    let built = Command::new("cargo").current_dir(&dir).args(["build", "--bin", "wf"]).output().unwrap();
    assert!(
        built.status.success(),
        "cargo build {FAILED_BUILD}: {}",
        String::from_utf8_lossy(&built.stderr)
    );
    fs::write(&stamp, FAILED_BUILD).unwrap();
    bin
}

#[test]
fn held_page_stays_readable_and_excludes_a_second_writer() {
    let r = new_root("hold");
    init_page(&r.root, PAGE, "pri");
    init_page(&r.root, OTHER, "ada");
    let out = must(&r.root, &["lockout", PAGE, "05", "--reason", "named face", "--as", "ada"]);
    assert!(out.contains("locked face 05"), "{out}");
    assert!(out.contains(&format!("Next: wf try-out {PAGE} before work.")), "{out}");

    let see = must(&r.root, &["try-out", PAGE, "--as", "ada"]);
    assert!(see.contains("lock holds on face 05"), "{see}");
    assert!(see.contains("worker: ada"), "{see}");
    assert!(see.contains("reason: named face"), "{see}");
    assert!(see.contains("other workers are refused"), "{see}");
    let held = read_log(&r.root, PAGE);
    let ev = events(&held);
    let locks: Vec<_> = ev.iter().filter(|e| e.kind == "lockout").collect();
    assert_eq!(locks.len(), 1);
    assert_eq!(locks[0].actor, "ada");
    assert!(String::from_utf8(held.clone()).unwrap().contains("\"face\":\"05\""));

    let other = must(&r.root, &["try-out", PAGE, "--as", "bob"]);
    assert!(other.contains("you would be refused"), "{other}");
    assert!(other.contains("face 05 is locked by ada"), "{other}");
    assert_eq!(read_log(&r.root, PAGE), held, "try-out appended");

    let status = must(&r.root, &["status", PAGE]);
    assert!(status.contains(&format!("NOW  page {PAGE}")), "{status}");
    assert!(status.contains("entries"), "{status}");
    let board = must(&r.root, &["board", PAGE]);
    assert!(board.contains(PAGE), "{board}");
    let verify = must(&r.root, &["verify", PAGE]);
    assert!(verify.contains("log chain holds"), "{verify}");
    assert_eq!(read_log(&r.root, PAGE), held, "a read appended");

    refuse(&r.root, &["lockout", PAGE, "01", "--reason", "other face", "--as", "bob"], "face 05 is locked by ada");
    refuse(&r.root, &["lockout", PAGE, "04", "--reason", "other face", "--as", "bob"], "face 05 is locked by ada");
    refuse(&r.root, &["face-write", PAGE, "01", "--text", "no", "--as", "bob"], "face 05 is locked by ada");
    refuse(&r.root, &["release", PAGE, "--as", "bob"], "face 05 is locked by ada");
    assert_eq!(read_log(&r.root, PAGE), held, "a refused command appended");

    let other_before = read_log(&r.root, OTHER);
    let moved = must(&r.root, &["lockout", OTHER, "05", "--reason", "second page", "--as", "ada"]);
    assert!(moved.contains("locked face 05"), "{moved}");
    must(&r.root, &["face-write", OTHER, "02", "--text", "sketch moves", "--as", "ada"]);
    let other_after = read_log(&r.root, OTHER);
    assert!(other_after.len() > other_before.len());
    let oe = events(&other_after);
    assert_eq!(oe[oe.len() - 2].kind, "lockout");
    assert_eq!(oe[oe.len() - 2].actor, "ada");
    assert_eq!(oe[oe.len() - 1].kind, "face");
    assert!(String::from_utf8(other_after).unwrap().contains("sketch moves"));
    let still = must(&r.root, &["try-out", PAGE, "--as", "ada"]);
    assert!(still.contains("lock holds on face 05"), "{still}");
    assert_eq!(read_log(&r.root, PAGE), held, "the second page rewrote the held page");
}

#[test]
fn fresh_checker_sees_the_published_release() {
    let r = packed("hand", PAGE);
    let bare = r.root.join("origin.git");
    let snap = r.root.join("baseline-page");
    copy_dir(&r.root.join("pages").join(PAGE), &snap);
    let baseline = read_log(&r.root, PAGE);
    commit_published(&r, PAGE, &baseline);
    assert_eq!(origin_log(&bare, PAGE), baseline);

    must(&r.root, &["lockout", PAGE, "05", "--reason", "handoff-hold", "--as", "bob"]);
    let see = must(&r.root, &["try-out", PAGE, "--as", "bob"]);
    assert!(see.contains("lock holds on face 05"), "{see}");
    must(&r.root, &["claim", PAGE, "1", "--as", "bob"]);
    let hash = pack_hash(&r.root, PAGE);
    let sha = work_commit(&r, PAGE, &hash);
    let file = format!(".workshop/returns/{PAGE}.05.01.md");
    let args = return_args(PAGE, &sha, &file, false);
    let (ok, out) = wf(&r.root, &args);
    assert!(ok, "{out}");
    assert!(out.contains("return filed on 05.01"), "{out}");

    let held = read_log(&r.root, PAGE);
    refuse(&r.root, &["check", PAGE, "1", "--as", "cat"], "face 05 is locked by bob");
    refuse(&r.root, &["lockout", PAGE, "05", "--reason", "too soon", "--as", "cat"], "face 05 is locked by bob");
    assert_eq!(read_log(&r.root, PAGE), held, "a refused checker command appended");

    let released = must(&r.root, &["release", PAGE, "--as", "bob"]);
    assert!(released.contains("released face 05"), "{released}");
    assert!(released.contains("no holder"), "{released}");
    let generated = read_log(&r.root, PAGE);
    let published = origin_log(&bare, PAGE);
    assert!(generated.starts_with(&published), "published log is not a prefix of the generated log");
    assert!(generated.len() > published.len());
    assert_eq!(published, baseline);
    assert!(!String::from_utf8_lossy(&published).contains("handoff-hold"));
    let mid = &events(&generated)[events(&baseline).len()..];
    assert_eq!(
        mid.iter().map(|e| e.kind.as_str()).collect::<Vec<_>>(),
        ["lockout", "claim", "return", "release"]
    );
    assert!(mid.iter().all(|e| e.actor == "bob"), "builder events changed actor");

    // The release is local until this path commit. Intake is what a fresh checker can see.
    publish_generated(&r, PAGE, &sha, &generated);
    let remote = origin_log(&bare, PAGE);
    assert_eq!(remote, generated, "publication step failed: {PUBLICATION_STEP}");
    assert!(String::from_utf8_lossy(&remote).contains("handoff-hold"));

    let checker = fresh_checker(&bare, &snap, PAGE);
    let (ok, intake) = wf(&checker.root, &["intake"]);
    assert!(ok, "{intake}");
    assert!(intake.contains("took"), "{intake}");
    assert_eq!(read_log(&checker.root, PAGE), generated, "intake did not take the generated log");
    let clear = must(&checker.root, &["try-out", PAGE, "--as", "cat"]);
    assert!(clear.contains("no lockout holds"), "{clear}");
    must(&checker.root, &["lockout", PAGE, "05", "--reason", "check", "--as", "cat"]);
    let checked = must(&checker.root, &["check", PAGE, "1", "--as", "cat"]);
    assert!(checked.contains("check 05.01: pass"), "{checked}");
    let final_log = read_log(&checker.root, PAGE);
    let tail = &events(&final_log)[events(&generated).len()..];
    assert_eq!(tail.len(), 2, "{}", String::from_utf8_lossy(&final_log));
    assert_eq!(tail[0].actor, "cat");
    assert_eq!(tail[0].kind, "lockout");
    assert_eq!(tail[1].actor, "cat");
    assert_eq!(tail[1].kind, "check");
    let text = String::from_utf8(final_log).unwrap();
    let suffix = &text[baseline.len()..];
    let ret = suffix.find("\"kind\":\"return\"").unwrap();
    let rel = suffix.find("\"kind\":\"release\"").unwrap();
    let chk = suffix.find("\"kind\":\"check\"").unwrap();
    assert!(ret < rel && rel < chk, "return, release, check are out of order in the published suffix");
}

#[test]
fn divergent_push_is_refused_and_a_valid_extension_is_accepted() {
    let bad = b"not-the-page-log\n";
    let diverge = packed("diverge", PAGE);
    let bare = diverge.root.join("origin.git");
    must(&diverge.root, &["lockout", PAGE, "05", "--reason", "push-hold", "--as", "bob"]);
    must(&diverge.root, &["try-out", PAGE, "--as", "bob"]);
    must(&diverge.root, &["claim", PAGE, "1", "--as", "bob"]);
    let hash = pack_hash(&diverge.root, PAGE);
    let sha = work_commit(&diverge, PAGE, &hash);
    commit_published(&diverge, PAGE, bad);
    assert_eq!(origin_log(&bare, PAGE), bad);
    let file = format!(".workshop/returns/{PAGE}.05.01.md");
    let args = return_args(PAGE, &sha, &file, true);
    let (ok, out) = wf(&diverge.root, &args);
    assert!(!ok, "{out}");
    assert!(out.contains(PREFIX_REFUSAL), "{out}");
    assert!(!out.contains("non-fast-forward"), "prefix refusal looked like a generic non-fast-forward: {out}");
    assert_eq!(origin_log(&bare, PAGE), bad, "a refused push changed the remote");

    let work = diverge.root.join("work");
    git(&work, &["checkout", "-q", "--orphan", "side"]);
    git(&work, &["commit", "-q", "--allow-empty", "-m", "side"]);
    let (pushed, push_out) = git_out(&work, &["push", "origin", "HEAD:refs/heads/returns"]);
    assert!(!pushed, "{push_out}");
    assert!(
        push_out.contains("non-fast-forward"),
        "the generic rejection should name non-fast-forward: {push_out}"
    );
    assert_ne!(push_out.trim(), PREFIX_REFUSAL);
    assert_eq!(origin_log(&bare, PAGE), bad, "the non-fast-forward push changed the remote");

    let extend = packed("extend", PAGE);
    let bare2 = extend.root.join("origin.git");
    must(&extend.root, &["lockout", PAGE, "05", "--reason", "push-hold", "--as", "bob"]);
    let see = must(&extend.root, &["try-out", PAGE, "--as", "bob"]);
    assert!(see.contains("lock holds on face 05"), "{see}");
    must(&extend.root, &["claim", PAGE, "1", "--as", "bob"]);
    let before = read_log(&extend.root, PAGE);
    commit_published(&extend, PAGE, &before);
    let hash2 = pack_hash(&extend.root, PAGE);
    let sha2 = work_commit(&extend, PAGE, &hash2);
    let file2 = format!(".workshop/returns/{PAGE}.05.01.md");
    let args2 = return_args(PAGE, &sha2, &file2, true);
    assert!(!args2.iter().any(|a| a.contains("force")));
    let (ok, out) = wf(&extend.root, &args2);
    assert!(ok, "{out}");
    assert!(out.contains("pushed returns"), "{out}");
    assert!(!out.contains(PREFIX_REFUSAL), "{out}");
    assert!(!out.contains("non-fast-forward"), "{out}");
    let local = read_log(&extend.root, PAGE);
    assert!(local.starts_with(&before));
    assert!(local.len() > before.len());
    assert_eq!(origin_log(&bare2, PAGE), local);
}

fn record_override(bin: &Path, root: &Path, addr: &str) -> Vec<u8> {
    must_bin(bin, root, &["lockout", addr, "05", "--reason", "left", "--as", "bob"]);
    let out = must_bin(bin, root, &["release", addr, "--override", "--reason", "holder left", "--as", "lead"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    read_log(root, addr)
}

#[test]
fn old_override_survives_succession_and_failed_build_does_not() {
    let bin = Path::new(env!("CARGO_BIN_EXE_wf"));
    let r = new_root("succ");
    must_bin(bin, &r.root, &[
        "init-page", BOOK, "--title", "book", "--person", "mat", "--prime", "old", "--grant", "src/",
        "--grant-ref", "tb", "--system", "--system-ref", "tbook", "--as", "mat",
    ]);
    must_bin(bin, &r.root, &["set-prime", BOOK, "lead", "--ref", "tlead", "--as", "mat"]);
    init_page_bin(bin, &r.root, PAGE, "pri");
    let recorded = record_override(bin, &r.root, PAGE);
    let text = String::from_utf8(recorded.clone()).unwrap();
    assert!(text.contains("\"prime\":\"lead\""), "{text}");
    assert!(text.contains("\"revision\":2"), "{text}");
    assert!(text.contains(&format!("\"book\":\"{BOOK}\"")), "{text}");
    must_bin(bin, &r.root, &["set-prime", BOOK, "bea", "--ref", "tbea", "--as", "mat"]);
    let status = must_bin(bin, &r.root, &["status", PAGE]);
    assert!(status.contains(&format!("NOW  page {PAGE}")), "{status}");
    assert!(status.contains("entries"), "{status}");
    let verify = must_bin(bin, &r.root, &["verify", PAGE]);
    assert!(verify.contains("log chain holds"), "{verify}");
    assert_eq!(read_log(&r.root, PAGE), recorded, "succession rewrote the work log");
    must_bin(bin, &r.root, &["lockout", PAGE, "05", "--reason", "fresh", "--as", "bob"]);
    let held = read_log(&r.root, PAGE);
    let (ok, former) = run_bin(bin, &r.root, &["release", PAGE, "--override", "--reason", "former prime", "--as", "lead"]);
    assert!(!ok, "{former}");
    assert!(former.contains("only the book's Prime"), "{former}");
    let (ok, work_prime) = run_bin(bin, &r.root, &["release", PAGE, "--override", "--reason", "work prime", "--as", "pri"]);
    assert!(!ok && work_prime.contains("only the book's Prime"), "{work_prime}");
    let (ok, first) = run_bin(bin, &r.root, &["release", PAGE, "--override", "--reason", "first prime", "--as", "old"]);
    assert!(!ok && first.contains("only the book's Prime"), "{first}");
    assert_eq!(read_log(&r.root, PAGE), held, "a refused override appended");
    let current = must_bin(bin, &r.root, &["release", PAGE, "--override", "--reason", "current prime", "--as", "bea"]);
    assert!(current.contains("override released face 05 held by bob"), "{current}");
    assert!(String::from_utf8(read_log(&r.root, PAGE)).unwrap().contains("\"prime\":\"bea\""));

    let missing = new_root("missing-book");
    init_page(&missing.root, PAGE, "pri");
    must(&missing.root, &["lockout", PAGE, "05", "--reason", "left", "--as", "bob"]);
    let before = read_log(&missing.root, PAGE);
    refuse(&missing.root, &["release", PAGE, "--override", "--reason", "holder left", "--as", "pri"], "the book Prime is missing");
    assert_eq!(read_log(&missing.root, PAGE), before);
    let out = must(&missing.root, &["release", PAGE, "--override", "--reason", "holder left", "--as", "mat"]);
    assert!(out.contains("override released face 05 held by bob"), "{out}");
    let release = String::from_utf8(read_log(&missing.root, PAGE)).unwrap();
    let line = release.lines().find(|l| l.contains("\"kind\":\"release\"")).unwrap();
    assert!(line.contains("\"fallback\":\"missing-book\""), "{line}");
    assert!(line.contains(&format!("\"book\":\"{BOOK}\"")), "{line}");
    assert!(line.contains("\"person\":\"mat\""), "{line}");
    assert!(!line.contains("\"prime\""), "{line}");

    let old = failed_build_bin();
    let neg = new_root("neg");
    must_bin(&old, &neg.root, &[
        "init-page", BOOK, "--title", "book", "--person", "mat", "--prime", "old", "--grant", "src/",
        "--grant-ref", "tb", "--system", "--system-ref", "tbook", "--as", "mat",
    ]);
    must_bin(&old, &neg.root, &["set-prime", BOOK, "lead", "--ref", "tlead", "--as", "mat"]);
    init_page_bin(&old, &neg.root, PAGE, "pri");
    let recorded = record_override(&old, &neg.root, PAGE);
    must_bin(&old, &neg.root, &["set-prime", BOOK, "bea", "--ref", "tbea", "--as", "mat"]);
    assert_eq!(read_log(&neg.root, PAGE), recorded, "the failed build rewrote the log during set-prime");
    let (ok, status) = run_bin(&old, &neg.root, &["status", PAGE]);
    assert!(!ok, "1b0d2c1 status should fail after succession: {status}");
    assert!(status.contains("log entry 3 is out of order"), "{status}");
    assert!(status.contains("only the book's Prime (bea) or the person (mat) may override"), "{status}");
    assert!(status.contains("the page cannot be read"), "{status}");
    let (vok, verify) = run_bin(&old, &neg.root, &["verify", PAGE]);
    assert!(!vok, "{verify}");
    assert!(verify.contains("the page cannot be read"), "{verify}");
    assert_eq!(read_log(&neg.root, PAGE), recorded, "the failed read rewrote the log");
    let (ook, again) = run_bin(&old, &neg.root, &["release", PAGE, "--override", "--reason", "former prime", "--as", "lead"]);
    assert!(!ook, "{again}");
    assert!(again.contains("the page cannot be read"), "{again}");
    assert_eq!(read_log(&neg.root, PAGE), recorded);
}
