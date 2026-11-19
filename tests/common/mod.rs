#![allow(dead_code)]

use std::fs;
use std::path::PathBuf;
use std::process::Command;

pub const PG: &str = "10.10.10.0401";

pub struct Env {
    pub root: PathBuf,
}

impl Env {
    pub fn new(name: &str) -> Env {
        let root = std::env::temp_dir().join(format!("wf-test-{}-{name}", std::process::id()));
        let _ = fs::remove_dir_all(&root);
        fs::create_dir_all(root.join("game/src")).unwrap();
        let e = Env { root };
        e.git(&["init", "-q", "-b", "main"]);
        fs::write(e.root.join("game/src/a.rs"), "a = 1\n").unwrap();
        fs::write(e.root.join("game/src/b.rs"), "b = 1\n").unwrap();
        e.git(&["add", "."]);
        e.git(&["commit", "-q", "-m", "start"]);
        e
    }
    pub fn git(&self, args: &[&str]) -> String {
        let o = Command::new("git").current_dir(self.root.join("game")).args(["-c", "user.name=t", "-c", "user.email=t@t"]).args(args).output().unwrap();
        assert!(o.status.success(), "git {args:?}: {}", String::from_utf8_lossy(&o.stderr));
        String::from_utf8_lossy(&o.stdout).trim().to_string()
    }
    /// Run wf; returns (ok, stdout + stderr).
    pub fn wf(&self, args: &[&str]) -> (bool, String) {
        self.wf_at(args, None)
    }
    pub fn wf_at(&self, args: &[&str], now: Option<u64>) -> (bool, String) {
        let mut c = Command::new(env!("CARGO_BIN_EXE_wf"));
        c.env("WF_ROOT", &self.root).args(args);
        if let Some(n) = now {
            c.env("WF_NOW", n.to_string());
        }
        let o = c.output().unwrap();
        (o.status.success(), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)))
    }
    pub fn ok(&self, args: &[&str]) -> String {
        let (ok, out) = self.wf(args);
        assert!(ok, "wf {args:?} failed: {out}");
        out
    }
    pub fn no(&self, args: &[&str], want: &str) {
        let (ok, out) = self.wf(args);
        assert!(!ok, "wf {args:?} should be refused: {out}");
        assert!(out.contains(want), "wf {args:?}: expected '{want}' in: {out}");
    }
    pub fn page(&self) -> PathBuf {
        self.root.join("pages").join(PG)
    }
    pub fn log(&self) -> String {
        fs::read_to_string(self.page().join("log.jsonl")).unwrap()
    }
    /// A page with person mat, prime pri, goals, a 01 card and a 06 note.
    pub fn ready(name: &str) -> Env {
        let e = Env::new(name);
        e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
        e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
        e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass.", "--as", "pri"]);
        e.ok(&["face-write", PG, "06", "--text", "read 04", "--as", "pri"]);
        e
    }
    pub fn draft(&self, may: &str, checks: &str) {
        self.draft_jobs(may, checks, "w01: set a to 2");
    }
    pub fn draft_jobs(&self, may: &str, checks: &str, jobs: &str) {
        let f = self.root.join("pack.txt");
        fs::write(&f, format!("repo: game\nstart: main\noutcome: a = 2\n{jobs}\nmay touch: {may}\nchecks: {checks}\nstop if: b must change\n")).unwrap();
        self.ok(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"]);
    }
    /// Draft, pack, claim pass 1 as bob.
    pub fn open(&self, may: &str, checks: &str) {
        self.draft(may, checks);
        self.ok(&["pack", PG, "1", "--as", "pri"]);
        self.ok(&["claim", PG, "1", "--as", "bob"]);
    }
    /// The builder's work: branch, edit files, return file, commit. Returns the SHA.
    pub fn work(&self, nn: u32, edits: &[(&str, &str)], jobs: &str) -> String {
        let name = format!("{PG}.05.{nn:02}");
        let prompt = fs::read_to_string(self.page().join(format!("05.{nn:02}/PROMPT.md"))).unwrap();
        let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
        self.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
        for (f, t) in edits {
            fs::write(self.root.join("game").join(f), t).unwrap();
        }
        fs::create_dir_all(self.root.join("game/.workshop/returns")).unwrap();
        let ret = format!("pack: {hash}\ndone: set a\nchanged: modify src/a.rs\nnoticed: none\n{jobs}\nproof: tests\ndesign review: kit docs compared (test)\nnot done: none\nunprompted: none\noverflow: none\n");
        fs::write(self.root.join(format!("game/.workshop/returns/{name}.md")), ret).unwrap();
        self.git(&["add", "-A"]);
        self.git(&["commit", "-q", "-m", "work"]);
        let sha = self.git(&["rev-parse", "HEAD"]);
        self.git(&["checkout", "-q", "main"]);
        sha
    }
    pub fn ret(&self, nn: u32, sha: &str, who: &str) -> (bool, String) {
        let name = format!("{PG}.05.{nn:02}");
        self.wf(&["return", PG, &nn.to_string(), "--branch", &format!("pass/{name}"), "--commit", sha, "--file", &format!(".workshop/returns/{name}.md"), "--as", who])
    }
    /// Run wf with a git config env override (this box sets core.quotePath=false via GIT_CONFIG_*).
    pub fn wf_git(&self, args: &[&str], key: &str, val: &str) -> (bool, String) {
        let mut c = Command::new(env!("CARGO_BIN_EXE_wf"));
        c.env("WF_ROOT", &self.root)
            .env("GIT_CONFIG_COUNT", "1")
            .env("GIT_CONFIG_KEY_0", key)
            .env("GIT_CONFIG_VALUE_0", val)
            .args(args);
        let o = c.output().unwrap();
        (o.status.success(), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)))
    }
    /// Pass `nn` from a 06 note to a passed close.
    #[allow(dead_code)]
    pub fn close_one(&self, nn: u32) {
        let n = nn.to_string();
        self.ok(&["face-write", PG, "06", "--text", "read 04 and the last close", "--as", "pri"]);
        self.draft("src/a.rs", "cargo --version");
        self.ok(&["pack", PG, &n, "--as", "pri"]);
        self.ok(&["claim", PG, &n, "--as", "bob"]);
        let sha = self.work(nn, &[("src/a.rs", &format!("a = {nn}\n"))], "w01: done - a");
        assert!(self.ret(nn, &sha, "bob").0);
        self.ok(&["check", PG, &n, "--as", "cat"]);
        self.ok(&["signoff", PG, &n, "--outcome", "passed", "--as", "pri"]);
        self.ok(&["close", PG, &n, "--as", "pri"]);
    }
    /// A full pass up to a passing check.
    pub fn checked(name: &str) -> Env {
        let e = Env::ready(name);
        e.open("src/a.rs", "cargo --version");
        let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
        assert!(e.ret(1, &sha, "bob").0);
        e.ok(&["check", PG, "1", "--as", "cat"]);
        e
    }
}

impl Drop for Env {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}

/// Closed passes written through the tool's own log append (Page::add), not 98 process runs.
pub fn seed_closed_passes(e: &Env, count: u32) {
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    for i in 1..=count {
        for (actor, role, kind, data) in closed_chain(i, "passed") {
            p.add(actor, role, kind, data).unwrap();
        }
    }
    wf::render::write(&p).unwrap();
}

/// Every entry of one pass from draft to close, in the order the log rules need.
pub fn closed_chain(nn: u32, outcome: &str) -> Vec<(&'static str, &'static str, &'static str, serde_json::Value)> {
    vec![
        ("pri", "prime", "draft", serde_json::json!({"pass": nn, "fields": {}, "pins": {}})),
        ("pri", "prime", "pack", seed_pack(nn)),
        ("bob", "builder", "claim", serde_json::json!({"pass": nn})),
        ("bob", "builder", "return", serde_json::json!({"pass": nn, "commit": "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12", "file": "f", "jobs": {}})),
        ("cat", "checker", "check", serde_json::json!({"pass": nn, "commit": "ab12cd34ef56ab12cd34ef56ab12cd34ef56ab12", "verdict": "pass", "report": ""})),
        ("pri", "prime", "signoff", serde_json::json!({"pass": nn, "outcome": outcome, "cards": {}})),
        ("pri", "tool", "close", serde_json::json!({"pass": nn, "outcome": outcome})),
    ]
}

/// Pack entry for a seeded pass. Lives with closed_chain, which is the only harness caller.
pub fn seed_pack(nn: u32) -> serde_json::Value {
    serde_json::json!({"pass": nn, "pack_text": format!("pack {nn}\n"), "pack_hash": format!("{nn:064}"), "branch": format!("pass/{PG}.05.{nn:02}"),
        "return_file": format!(".workshop/returns/{PG}.05.{nn:02}.md"), "start": "0", "templates": "1", "sources": {}})
}
