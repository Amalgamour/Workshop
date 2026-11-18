//! End-to-end tests: each one runs the wf binary against a temp folder and a temp git repo.

use std::fs;
use std::os::unix::fs::{self as unix_fs, MetadataExt, PermissionsExt};
use std::path::PathBuf;
use std::process::Command;

const PG: &str = "1.2.3.4";

struct Env {
    root: PathBuf,
}

impl Env {
    fn new(name: &str) -> Env {
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
    fn git(&self, args: &[&str]) -> String {
        let o = Command::new("git").current_dir(self.root.join("game")).args(["-c", "user.name=t", "-c", "user.email=t@t"]).args(args).output().unwrap();
        assert!(o.status.success(), "git {args:?}: {}", String::from_utf8_lossy(&o.stderr));
        String::from_utf8_lossy(&o.stdout).trim().to_string()
    }
    /// Run wf; returns (ok, stdout + stderr).
    fn wf(&self, args: &[&str]) -> (bool, String) {
        self.wf_at(args, None)
    }
    fn wf_at(&self, args: &[&str], now: Option<u64>) -> (bool, String) {
        let mut c = Command::new(env!("CARGO_BIN_EXE_wf"));
        c.env("WF_ROOT", &self.root).args(args);
        if let Some(n) = now {
            c.env("WF_NOW", n.to_string());
        }
        let o = c.output().unwrap();
        (o.status.success(), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)))
    }
    fn ok(&self, args: &[&str]) -> String {
        let (ok, out) = self.wf(args);
        assert!(ok, "wf {args:?} failed: {out}");
        out
    }
    fn no(&self, args: &[&str], want: &str) {
        let (ok, out) = self.wf(args);
        assert!(!ok, "wf {args:?} should be refused: {out}");
        assert!(out.contains(want), "wf {args:?}: expected '{want}' in: {out}");
    }
    fn page(&self) -> PathBuf {
        self.root.join("pages").join(PG)
    }
    fn log(&self) -> String {
        fs::read_to_string(self.page().join("log.jsonl")).unwrap()
    }
    /// A page with person mat, prime pri, goals, a 01 card and a 06 note.
    fn ready(name: &str) -> Env {
        let e = Env::new(name);
        e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
        e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
        e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: checks pass.", "--as", "pri"]);
        e.ok(&["face-write", PG, "06", "--text", "read 04", "--as", "pri"]);
        e
    }
    fn draft(&self, may: &str, checks: &str) {
        self.draft_jobs(may, checks, "w01: set a to 2");
    }
    fn draft_jobs(&self, may: &str, checks: &str, jobs: &str) {
        let f = self.root.join("pack.txt");
        fs::write(&f, format!("repo: game\nstart: main\noutcome: a = 2\n{jobs}\nmay touch: {may}\nchecks: {checks}\nstop if: b must change\n")).unwrap();
        self.ok(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"]);
    }
    /// Draft, pack, claim pass 1 as bob.
    fn open(&self, may: &str, checks: &str) {
        self.draft(may, checks);
        self.ok(&["pack", PG, "1", "--as", "pri"]);
        self.ok(&["claim", PG, "1", "--as", "bob"]);
    }
    /// The builder's work: branch, edit files, return file, commit. Returns the SHA.
    fn work(&self, nn: u32, edits: &[(&str, &str)], jobs: &str) -> String {
        let name = format!("{PG}.05.{nn:02}");
        let prompt = fs::read_to_string(self.page().join(format!("05.{nn:02}/PROMPT.md"))).unwrap();
        let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
        self.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
        for (f, t) in edits {
            fs::write(self.root.join("game").join(f), t).unwrap();
        }
        fs::create_dir_all(self.root.join("game/.workshop/returns")).unwrap();
        let ret = format!("pack: {hash}\ndone: set a\nchanged: modify src/a.rs\nnoticed: none\n{jobs}\nproof: tests\nnot done: none\nunprompted: none\noverflow: none\n");
        fs::write(self.root.join(format!("game/.workshop/returns/{name}.md")), ret).unwrap();
        self.git(&["add", "-A"]);
        self.git(&["commit", "-q", "-m", "work"]);
        let sha = self.git(&["rev-parse", "HEAD"]);
        self.git(&["checkout", "-q", "main"]);
        sha
    }
    fn ret(&self, nn: u32, sha: &str, who: &str) -> (bool, String) {
        let name = format!("{PG}.05.{nn:02}");
        self.wf(&["return", PG, &nn.to_string(), "--branch", &format!("pass/{name}"), "--commit", sha, "--file", &format!(".workshop/returns/{name}.md"), "--as", who])
    }
    /// Run wf with a git config env override (this box sets core.quotePath=false via GIT_CONFIG_*).
    fn wf_git(&self, args: &[&str], key: &str, val: &str) -> (bool, String) {
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
    fn close_one(&self, nn: u32) {
        let n = nn.to_string();
        self.ok(&["face-write", PG, "06", "--text", "read 04 and the last close", "--as", "pri"]);
        self.draft("src/a.rs", "true");
        self.ok(&["pack", PG, &n, "--as", "pri"]);
        self.ok(&["claim", PG, &n, "--as", "bob"]);
        let sha = self.work(nn, &[("src/a.rs", &format!("a = {nn}\n"))], "w01: done - a");
        assert!(self.ret(nn, &sha, "bob").0);
        self.ok(&["check", PG, &n, "--as", "cat"]);
        self.ok(&["signoff", PG, &n, "--outcome", "passed", "--as", "pri"]);
        self.ok(&["close", PG, &n, "--as", "pri"]);
    }
    /// A full pass up to a passing check.
    fn checked(name: &str) -> Env {
        let e = Env::ready(name);
        e.open("src/a.rs", "grep -q 2 src/a.rs");
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
fn seed_closed_passes(e: &Env, count: u32) {
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    for i in 1..=count {
        for (actor, role, kind, data) in closed_chain(i, "passed") {
            p.add(actor, role, kind, data).unwrap();
        }
    }
    wf::render::write(&p).unwrap();
}

/// Every entry of one pass from draft to close, in the order the log rules need.
fn closed_chain(nn: u32, outcome: &str) -> Vec<(&'static str, &'static str, &'static str, serde_json::Value)> {
    vec![
        ("pri", "prime", "draft", serde_json::json!({"pass": nn, "fields": {}, "pins": {}})),
        ("pri", "prime", "pack", seed_pack(nn)),
        ("bob", "builder", "claim", serde_json::json!({"pass": nn})),
        ("bob", "builder", "return", serde_json::json!({"pass": nn, "commit": "c", "file": "f", "jobs": {}})),
        ("cat", "checker", "check", serde_json::json!({"pass": nn, "commit": "c", "verdict": "pass", "report": ""})),
        ("pri", "prime", "signoff", serde_json::json!({"pass": nn, "outcome": outcome, "cards": {}})),
        ("pri", "tool", "close", serde_json::json!({"pass": nn, "outcome": outcome})),
    ]
}

#[test]
fn full_pass_closes_with_a_record() {
    let e = Env::checked("full");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    let rec = e.ok(&["close", PG, "1", "--as", "pri"]);
    assert!(rec.contains("signed off: pri, face 00 prime at entry"));
    assert!(rec.contains("cards:      w01 accepted"));
    let st = e.ok(&["status", PG]);
    assert!(st.contains("05.01  closed   passed"), "{st}");
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
    let face05 = fs::read_to_string(e.page().join("05.md")).unwrap();
    assert!(face05.contains("close record 1.2.3.4.05.01"));
}

#[test]
fn pack_prints_prompt_and_pins_axioms_and_design() {
    let e = Env::ready("pack");
    e.draft("src/a.rs", "true");
    let out = e.ok(&["pack", PG, "1", "--as", "pri"]);
    assert!(out.contains("=== WORKSHOP JOB 1.2.3.4.05.01 ===") && out.contains("May touch: src/a.rs"));
    let agents = fs::read_to_string(e.page().join("05.01/AGENTS.md")).unwrap();
    assert!(agents.contains("docs/AXIOMS.md") && agents.contains("docs/DESIGN.md") && agents.contains("hash "), "{agents}");
    assert!(agents.contains("Goal: a."));
    assert!(agents.contains("Done when (face 01): Done when: checks pass."), "{agents}");
    assert!(!agents.contains("cold set") && !agents.contains("Axioms named by this pack"), "{agents}");
    let pack = fs::read_to_string(e.page().join("05.01/PACK.md")).unwrap();
    assert!(pack.contains("face 04:        entry 2") && pack.contains("last closed 05: none"));
    assert!(pack.contains("done when:   Done when: checks pass."), "{pack}");
    assert!(out.contains("Done when (face 01): Done when: checks pass."), "{out}");
}

#[test]
fn draft_needs_a_06_note_after_the_last_close() {
    let e = Env::new("note");
    e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
    let f = e.root.join("p.txt");
    fs::write(&f, "w01: x\n").unwrap();
    e.no(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"], "write a 06 note");
}

#[test]
fn stale_pin_is_refused_until_redrafted() {
    let e = Env::ready("stale");
    e.draft("src/a.rs", "true");
    e.ok(&["face-write", PG, "04", "--section", "responses", "--text", "too slow", "--as", "mat"]);
    e.no(&["pack", PG, "1", "--as", "pri"], "stale pin 04");
    e.no(&["pack", PG, "1", "--as", "pri"], "Write a new 06 note and redraft");
    e.ok(&["draft", PG, "--pass", "1", "--file", e.root.join("pack.txt").to_str().unwrap(), "--as", "pri"]);
    e.ok(&["pack", PG, "1", "--as", "pri"]);
}

#[test]
fn may_touch_outside_grant_is_refused() {
    let e = Env::ready("grant");
    e.draft("docs/x.md", "true");
    e.no(&["pack", PG, "1", "--as", "pri"], "outside the grant");
}

#[test]
fn draft_waits_while_a_pass_is_open_so_files_cannot_overlap() {
    // w03: a second pass cannot be drafted while 05.01 is open, so two passes never hold the same files.
    let e = Env::ready("ov-ref");
    e.open("src/a.rs", "true");
    let before = e.log();
    let f = e.root.join("pack.txt");
    e.no(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"], "refused: 05.01 is at 'open' and not closed");
    assert_eq!(e.log(), before, "a refused draft must not append");
}

#[test]
fn pack_allows_overlap_after_other_closes() {
    let e = Env::checked("ov-close");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["close", PG, "1", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04 and closed 05.01", "--as", "pri"]);
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "2", "--as", "pri"]);
}

#[test]
fn overlap_ok_refuses_a_pass_that_is_not_open() {
    let e = Env::ready("ov-bad");
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "1", "--overlap-ok", "9", "--why", "none yet (t275u)", "--as", "pri"], "--overlap-ok 05.09 is not open (no such pass)");
    let e = Env::checked("ov-closed");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["close", PG, "1", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04 and closed 05.01", "--as", "pri"]);
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--why", "none yet (t275u)", "--as", "pri"], "--overlap-ok 05.01 is not open (tail is closed)");
}

#[test]
fn pin_text_in_pack_is_05_01() {
    let e = Env::checked("pin-pad");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["close", PG, "1", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04 and closed 05.01", "--as", "pri"]);
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "2", "--as", "pri"]);
    let pack = fs::read_to_string(e.page().join("05.02/PACK.md")).unwrap();
    assert!(pack.contains("last closed 05: 05.01 closed at entry"), "{pack}");
}

#[test]
fn check_dry_run_prints_full_output_and_writes_nothing() {
    let e = Env::ready("dry");
    e.open("src/a.rs", "printf '%s\\n' 'running 2 tests' 'test result: ok. 2 passed' 'running 23 tests' 'test result: ok. 23 passed'");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    let before = e.log();
    let out = e.ok(&["check", PG, "1", "--dry-run", "--as", "cat"]);
    assert!(out.contains("running 2 tests") && out.contains("running 23 tests"), "{out}");
    assert!(out.contains("test result: ok. 2 passed") && out.contains("test result: ok. 23 passed"), "{out}");
    assert!(out.contains("dry-run: nothing written"), "{out}");
    assert_eq!(e.log(), before);
    assert!(!before.contains("\"kind\":\"check\""));
    let filed = e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(filed.contains("running 2 tests") && filed.contains("running 23 tests"), "{filed}");
    assert!(e.log().contains("\"kind\":\"check\""));
}

#[test]
fn help_lists_overlap_ok_and_check_flags() {
    let e = Env::new("help");
    let out = e.ok(&["help"]);
    assert!(out.contains("pack <page> <NN> [--overlap-ok NN --why T]"), "{out}");
    assert!(out.contains("set-prime <page> <name> --ref tNNNu"), "{out}");
    assert!(out.contains("check <page> <NN> [--note T] [--fail T] [--dry-run]"), "{out}");
}

#[test]
fn only_prime_drafts_and_packs() {
    let e = Env::ready("roles");
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "1", "--as", "bob"], "only the prime");
}

#[test]
fn first_claim_wins_and_only_holder_returns() {
    let e = Env::ready("claim");
    e.open("src/a.rs", "true");
    e.no(&["claim", PG, "1", "--as", "eve"], "already claimed by bob");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    let (ok, out) = e.ret(1, &sha, "eve");
    assert!(!ok && out.contains("only the claim holder"), "{out}");
}

#[test]
fn out_of_frame_return_is_refused_and_recorded() {
    let e = Env::ready("frame");
    e.open("src/a.rs", "true");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n"), ("src/b.rs", "b = 2\n")], "w01: done - a");
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(!ok && out.contains("src/b.rs outside may touch"), "{out}");
    assert!(e.log().contains("\"kind\":\"return-refused\""));
    assert!(e.ok(&["status", PG]).contains("05.01  open"));
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
}

#[test]
fn return_with_missing_parts_is_refused() {
    let e = Env::ready("parts");
    e.open("src/a.rs", "true");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: finished");
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(!ok && out.contains("must start with done, need or blocked"), "{out}");
}

#[test]
fn need_item_goes_up_to_prime_and_prime_answers() {
    let e = Env::ready("need");
    e.open("src/a.rs", "true");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: need - b must change");
    assert!(e.ret(1, &sha, "bob").0);
    let st = e.ok(&["status", PG]);
    assert!(st.contains("-> prime: w01 need - b must change"), "{st}");
    let seq = e.log().lines().position(|l| l.contains("\"kind\":\"elevate\"")).unwrap() + 1;
    e.no(&["answer", PG, &seq.to_string(), "--text", "no", "--as", "bob"], "only the prime");
    e.no(&["elevate", PG, "1", "--to", "person", "--item", "x", "--as", "bob"], "only Prime sends it up");
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "may b change?", "--as", "pri"]);
    let up = e.log().lines().count();
    e.ok(&["answer", PG, &seq.to_string(), "--text", "sent up", "--as", "pri"]);
    e.ok(&["grant", PG, "--paths", "lib/", "--ref", "t2", "--answers", &up.to_string(), "--as", "mat"]);
    let st = e.ok(&["status", PG]);
    assert!(st.contains("waiting: nothing"), "{st}");
    assert!(fs::read_to_string(e.page().join("00.md")).unwrap().contains("src/, lib/ (from t1, t2)"));
}

#[test]
fn builder_cannot_check_own_work() {
    let e = Env::ready("own");
    e.open("src/a.rs", "true");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    e.no(&["check", PG, "1", "--as", "bob"], "may not check its own work");
}

#[test]
fn failed_check_twice_goes_up_and_blocks_passed_signoff() {
    let e = Env::ready("fail");
    e.open("src/a.rs", "grep -q 3 src/a.rs");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    assert!(e.ok(&["check", PG, "1", "--as", "cat"]).contains("check FAIL: grep -q 3 src/a.rs"));
    e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(e.ok(&["status", PG]).contains("second failed check"));
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "check failed");
    e.ok(&["signoff", PG, "1", "--outcome", "failed", "--as", "pri"]);
    assert!(e.ok(&["close", PG, "1", "--as", "pri"]).contains("w01 discarded"));
}

#[test]
fn non_prime_cannot_sign_off_and_close_needs_signoff() {
    let e = Env::checked("sign");
    e.no(&["close", PG, "1", "--as", "pri"], "has not signed off");
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "mat"], "only the prime");
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "cat"], "only the prime");
}

#[test]
fn prime_change_is_kept_and_old_prime_cannot_sign() {
    let e = Env::checked("handover");
    e.ok(&["set-prime", PG, "neo", "--ref", "t275u", "--as", "mat"]);
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "only the prime (neo)");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "neo"]);
    e.ok(&["close", PG, "1", "--as", "neo"]);
    let f00 = fs::read_to_string(e.page().join("00.md")).unwrap();
    assert!(f00.contains("prime:   neo") && f00.contains("  - pri: entries 1-"), "{f00}");
}

#[test]
fn face_writes_follow_roles() {
    let e = Env::ready("faces");
    e.no(&["face-write", PG, "04", "--section", "responses", "--text", "x", "--as", "pri"], "only the person");
    e.no(&["face-write", PG, "01", "--text", "x", "--as", "mat"], "only the prime");
    e.no(&["face-write", PG, "03", "--text", "x", "--as", "pri"], "printed by wf");
    e.no(&["face-write", PG, "05", "--text", "x", "--as", "pri"], "printed by wf");
    e.ok(&["face-write", PG, "04", "--section", "responses", "--text", "ok", "--as", "mat"]);
}

#[test]
fn hand_edited_face_is_refused_then_reprinted() {
    let e = Env::ready("edit");
    let f = e.page().join("01.md");
    fs::write(&f, "Goal: something else\n").unwrap();
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "view files differ from the log (hand edit or a failed reprint): 01.md");
    e.no(&["verify", PG], "view files differ from the log (hand edit or a failed reprint): 01.md");
    e.ok(&["verify", PG, "--fix"]);
    assert!(fs::read_to_string(&f).unwrap().contains("Goal: a."));
    e.ok(&["face-write", PG, "06", "--text", "x", "--as", "pri"]);
}

#[test]
fn log_tamper_is_detected() {
    let e = Env::ready("tamper");
    let log = e.page().join("log.jsonl");
    let t = e.log().replacen("\"prime\":\"pri\"", "\"prime\":\"eve\"", 1);
    fs::write(&log, t).unwrap();
    e.no(&["status", PG], "log chain broken at line 2");
    e.no(&["verify", PG], "log chain broken");
}

#[test]
fn last_line_tamper_shows_in_the_stamp() {
    let e = Env::ready("tail");
    let log = e.page().join("log.jsonl");
    let t = e.log().replace("read 04", "read nothing");
    fs::write(&log, t).unwrap();
    e.no(&["verify", PG], "view files differ from the log (hand edit or a failed reprint)");
}

#[test]
fn observer_reports_and_files_but_prime_cannot() {
    let e = Env::ready("obs");
    e.open("src/a.rs", "true");
    let later = e.wf_at(&["observe", PG, "--as", "olly"], Some(4_000_000_000)).1;
    assert!(later.contains("stalled: nothing has moved"), "{later}");
    e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "b works too", "--as", "pri"]);
    assert!(e.ok(&["observe", PG]).contains("drift: 05.01 was packed against face 04"));
    e.no(&["observe", PG, "--record", "x", "--as", "pri"], "Prime cannot file observer findings");
    e.ok(&["observe", PG, "--record", "goals moved under an open pass", "--as", "olly"]);
    assert!(e.ok(&["status", PG]).contains("observer findings: 1"));
}

#[test]
fn page_needs_its_person_to_start_it() {
    let e = Env::new("init");
    e.no(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "pri"], "the person starts");
    e.no(&["init-page", "../x", "--as", "mat"], "bad page address");
    e.no(&["status", PG], "no page");
}

/// The value of the first JSON string field `"key":"..."` in a log line, with escapes undone.
fn json_str(line: &str, key: &str) -> String {
    let pat = format!("\"{key}\":\"");
    let start = line.find(&pat).unwrap_or_else(|| panic!("no {key} in {line}")) + pat.len();
    let mut out = String::new();
    let mut chars = line[start..].chars();
    while let Some(c) = chars.next() {
        if c == '\\' {
            match chars.next() {
                Some('n') => out.push('\n'),
                Some('t') => out.push('\t'),
                Some(n) => out.push(n),
                None => break,
            }
        } else if c == '"' {
            break;
        } else {
            out.push(c);
        }
    }
    out
}

const REAL_FACE_01: &str = "Goal: the workflow kit (wf) any model can pull and run. MVP: every step of a pass runs through wf; refusals hold; README and AGENTS.md are enough for a fresh model. Done when: cargo test passes and the new behaviour has a test. Source: t267u, t268u, t270u.";
const REAL_DONE_WHEN: &str = "Done when: cargo test passes and the new behaviour has a test. Source: t267u, t268u, t270u.";

#[test]
fn pack_reads_inline_done_when_from_real_face_01() {
    let e = Env::new("dw-inline");
    e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
    e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", REAL_FACE_01, "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04", "--as", "pri"]);
    e.draft("src/a.rs", "true");
    let out = e.ok(&["pack", PG, "1", "--as", "pri"]);
    assert!(out.contains(&format!("Done when (face 01): {REAL_DONE_WHEN}")), "{out}");
    let pack = fs::read_to_string(e.page().join("05.01/PACK.md")).unwrap();
    assert!(pack.contains(&format!("done when:   {REAL_DONE_WHEN}")), "{pack}");
    let agents = fs::read_to_string(e.page().join("05.01/AGENTS.md")).unwrap();
    assert!(agents.contains(&format!("Done when (face 01): {REAL_DONE_WHEN}")), "{agents}");
}

#[test]
fn pack_warns_on_stderr_when_face_01_has_no_done_when() {
    let e = Env::new("dw-none");
    e.ok(&["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
    e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "a works", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a works.", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04", "--as", "pri"]);
    e.draft("src/a.rs", "true");
    let mut c = Command::new(env!("CARGO_BIN_EXE_wf"));
    c.env("WF_ROOT", &e.root).args(["pack", PG, "1", "--as", "pri"]);
    let o = c.output().unwrap();
    let stdout = String::from_utf8_lossy(&o.stdout);
    let stderr = String::from_utf8_lossy(&o.stderr);
    assert!(o.status.success(), "pack failed: {stdout}{stderr}");
    assert!(stderr.contains("warning: face 01 has no done-when"), "stderr={stderr}");
    assert!(!stdout.contains("warning: face 01 has no done-when"), "warning leaked to stdout: {stdout}");
    assert!(stdout.contains("=== WORKSHOP JOB"), "{stdout}");
    let pack = fs::read_to_string(e.page().join("05.01/PACK.md")).unwrap();
    assert!(pack.contains("done when:   none"), "{pack}");
}

#[test]
fn check_stores_at_most_last_40_lines_of_output() {
    let e = Env::ready("clip40");
    e.open("src/a.rs", "seq -f L%03g 1 50");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    let filed = e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(filed.contains("L001") && filed.contains("L050"), "printed report should keep full output: {filed}");
    let line = e.log().lines().find(|l| l.contains("\"kind\":\"check\"")).expect("check event").to_string();
    let stored = json_str(&line, "out");
    assert!(stored.starts_with("(10 lines cut)\nL011\n"), "{stored}");
    assert!(stored.ends_with("L050"), "{stored}");
    assert!(!stored.contains("L001") && !stored.contains("L010"), "{stored}");
    assert_eq!(stored.lines().count(), 41);
}


fn spawn_wf(root: &PathBuf, args: &[&str]) -> std::process::Child {
    Command::new(env!("CARGO_BIN_EXE_wf"))
        .env("WF_ROOT", root)
        .args(args)
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .spawn()
        .unwrap()
}

fn wait_out(child: std::process::Child) -> (bool, String) {
    let o = child.wait_with_output().unwrap();
    (o.status.success(), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)))
}

#[test]
fn eight_init_page_runs_leave_one_init() {
    let e = Env::new("init8");
    let args = ["init-page", PG, "--title", "t", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"];
    let kids: Vec<_> = (0..8).map(|_| spawn_wf(&e.root, &args)).collect();
    let results: Vec<_> = kids.into_iter().map(wait_out).collect();
    let wins = results.iter().filter(|(ok, _)| *ok).count();
    assert_eq!(wins, 1, "{results:?}");
    for (ok, out) in &results {
        if !*ok {
            assert!(out.contains("already exists") || out.contains("another wf command is writing"), "{out}");
        }
    }
    let log = e.log();
    assert_eq!(log.lines().filter(|l| l.contains("\"kind\":\"init\"")).count(), 1, "{log}");
    assert_eq!(log.lines().count(), 1, "{log}");
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
    assert!(!e.page().join(".wf-lock").exists());
}

#[test]
fn eight_claim_runs_leave_one_claim() {
    let e = Env::ready("claim8");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    let names: Vec<String> = (0..8).map(|i| format!("b{i}")).collect();
    let kids: Vec<_> = names.iter().map(|n| spawn_wf(&e.root, &["claim", PG, "1", "--as", n])).collect();
    let results: Vec<_> = kids.into_iter().map(wait_out).collect();
    let wins = results.iter().filter(|(ok, _)| *ok).count();
    assert_eq!(wins, 1, "{results:?}");
    for (ok, out) in &results {
        if !*ok {
            assert!(out.contains("already claimed") || out.contains("another wf command is writing"), "{out}");
        }
    }
    let log = e.log();
    assert_eq!(log.lines().filter(|l| l.contains("\"kind\":\"claim\"")).count(), 1, "{log}");
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
    assert!(!e.page().join(".wf-lock").exists());
}

#[test]
fn read_only_commands_run_while_a_lock_file_exists() {
    let e = Env::ready("nolock");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    fs::write(e.page().join(".wf-lock"), "").unwrap();
    assert!(e.ok(&["status", PG]).contains("05.01"));
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
    let (ok, out) = e.wf(&["observe", PG]);
    assert!(ok, "{out}");
    fs::remove_file(e.page().join(".wf-lock")).unwrap();
    e.ok(&["claim", PG, "1", "--as", "bob"]);
}

#[test]
fn check_reads_done_when_from_the_pack_and_notes_drift() {
    let e = Env::ready("dwpack");
    e.open("src/a.rs", "true");
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: a is 3 and b is 9.", "--as", "pri"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    assert!(e.ret(1, &sha, "bob").0);
    let out = e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(out.contains("done when (01): Done when: checks pass. -> checks ok; the checker judges the rest"), "{out}");
    assert!(!out.contains("Done when: a is 3 and b is 9."), "{out}");
    assert!(out.contains("drift: face 01 changed since pack (now v2 entry "), "{out}");
    let obs = e.ok(&["observe", PG]);
    assert!(obs.contains("packed against an older face 01 (now v2 entry "), "{obs}");
}

#[test]
fn check_lists_jobs_not_done_apart_from_checks_ok() {
    let e = Env::ready("notdone");
    e.draft_jobs("src/a.rs", "true", "w01: set a to 2\nw02: leave b alone");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2\nw02: blocked - b is outside may touch");
    assert!(e.ret(1, &sha, "bob").0);
    let out = e.ok(&["check", PG, "1", "--as", "cat"]);
    assert!(out.contains("check 05.01: pass"), "{out}");
    assert!(out.contains("job w01: done - a is 2"), "{out}");
    assert!(out.contains("job w02: blocked - b is outside may touch"), "{out}");
    assert!(out.contains("jobs not done: w02"), "{out}");
}

#[test]
fn signoff_passed_refuses_unfinished_jobs_until_named() {
    let e = Env::ready("so-jobs");
    e.draft_jobs("src/a.rs", "true", "w01: set a to 2\nw02: leave b alone");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2\nw02: blocked - b is outside may touch");
    assert!(e.ret(1, &sha, "bob").0);
    e.ok(&["check", PG, "1", "--as", "cat"]);
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "jobs not done: w02");
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w02=carried", "--as", "pri"], "--note needs a reason and a (ref)");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w02=carried", "--note", "carry b (t275u)", "--as", "pri"]);
    let rec = e.ok(&["close", PG, "1", "--as", "pri"]);
    assert!(rec.contains("w01 accepted") && rec.contains("w02 carried"), "{rec}");
}

#[test]
fn signoff_passed_refuses_unanswered_person_elevation_and_drift() {
    let e = Env::ready("so-elev");
    e.open("src/a.rs", "true");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    assert!(e.ret(1, &sha, "bob").0);
    e.ok(&["check", PG, "1", "--as", "cat"]);
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "may we accept this?", "--as", "pri"]);
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "to person has no answer");
    let seq = e.log().lines().enumerate().find(|(_, l)| l.contains("\"to\":\"person\"")).map(|(i, _)| i + 1).unwrap();
    e.ok(&["answer", PG, &seq.to_string(), "--text", "yes", "--as", "mat"]);
    // face 01 drift still blocks a passed signoff without a note
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: something new.", "--as", "pri"]);
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "face 01 has changed since pack");
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--note", "no ref here", "--as", "pri"], "--note needs a reason and a (ref)");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--note", "same goal (t275u)", "--as", "pri"]);
}

#[test]
fn overlap_ok_needs_why_and_set_prime_needs_ref() {
    let e = Env::ready("whyref");
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "1", "--overlap-ok", "1", "--as", "pri"], "missing --why");
    e.no(&["pack", PG, "1", "--overlap-ok", "1", "--why", "no ref", "--as", "pri"], "--why needs a reason and a (ref)");
    e.no(&["pack", PG, "1", "--overlap-ok", "1", "--why", "ok ( )", "--as", "pri"], "--why needs a reason and a (ref)");
    e.no(&["pack", PG, "1", "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri"], "--overlap-ok 05.01 is not open (tail is draft)");
    let e = Env::checked("setref");
    e.no(&["set-prime", PG, "neo", "--as", "mat"], "missing --ref");
    e.no(&["set-prime", PG, "neo", "--ref", " ", "--as", "mat"], "--ref must have non-blank text");
    e.ok(&["set-prime", PG, "neo", "--ref", "t275u", "--as", "mat"]);
    // changing a default card on a fully done passed pass needs --note
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w01=carried", "--as", "neo"], "--note needs a reason and a (ref)");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w01=carried", "--note", "hold for later (t275u)", "--as", "neo"]);
}

#[test]
fn check_commands_run_without_holding_the_page_lock() {
    let e = Env::ready("ckunlock");
    e.open("src/a.rs", "sleep 2");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    let slow = spawn_wf(&e.root, &["check", PG, "1", "--as", "cat"]);
    std::thread::sleep(std::time::Duration::from_millis(200));
    assert!(!e.page().join(".wf-lock").exists(), "check held .wf-lock while its command was running");
    let start = std::time::Instant::now();
    assert!(e.ok(&["status", PG]).contains("05.01"));
    e.ok(&["face-write", PG, "06", "--text", "note during check", "--as", "pri"]);
    assert!(
        start.elapsed() < std::time::Duration::from_millis(800),
        "a writer took {:?} during a check; expected well under 1s",
        start.elapsed()
    );
    let (ok, out) = wait_out(slow);
    assert!(ok, "{out}");
    assert!(out.contains("check 05.01: pass"), "{out}");
    assert!(e.log().contains("\"kind\":\"check\""));
}

#[test]
fn answer_text_must_be_nonblank() {
    let e = Env::checked("ansblank");
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "may we accept this?", "--as", "pri"]);
    let seq = e.log().lines().enumerate().find(|(_, l)| l.contains("\"to\":\"person\"")).map(|(i, _)| i + 1).unwrap();
    e.no(&["answer", PG, &seq.to_string(), "--text", " ", "--as", "mat"], "--text must have non-blank text");
    e.no(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"], "to person has no answer");
    e.ok(&["answer", PG, &seq.to_string(), "--text", "yes", "--as", "mat"]);
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
}

#[test]
fn close_passed_reruns_signoff_refusals() {
    let e = Env::checked("close-re");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "a late question", "--as", "pri"]);
    e.no(&["close", PG, "1", "--as", "pri"], "to person has no answer");
    let seq = e.log().lines().enumerate().find(|(_, l)| l.contains("\"to\":\"person\"")).map(|(i, _)| i + 1).unwrap();
    e.ok(&["answer", PG, &seq.to_string(), "--text", "yes", "--as", "mat"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: something new.", "--as", "pri"]);
    e.no(&["close", PG, "1", "--as", "pri"], "face 01 has changed since pack");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--note", "same goal (t275u)", "--as", "pri"]);
    let rec = e.ok(&["close", PG, "1", "--as", "pri"]);
    assert!(rec.contains("cards:      w01 accepted"), "{rec}");
}

#[test]
fn check_report_includes_drift_that_happens_during_the_check() {
    let e = Env::ready("ckdrift");
    e.open("src/a.rs", "sleep 2");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    let slow = spawn_wf(&e.root, &["check", PG, "1", "--as", "cat"]);
    std::thread::sleep(std::time::Duration::from_millis(200));
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: something new.", "--as", "pri"]);
    let (ok, out) = wait_out(slow);
    assert!(ok, "{out}");
    assert!(out.contains("drift: face 01 changed since pack (now v2 entry "), "{out}");
    assert!(e.log().contains("drift: face 01 changed since pack (now v2 entry "), "{}", e.log());
}

#[test]
fn check_refuses_if_another_check_is_filed_first() {
    let e = Env::ready("ckrace");
    e.open("src/a.rs", "sleep 1");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0);
    let a = spawn_wf(&e.root, &["check", PG, "1", "--as", "cat"]);
    let b = spawn_wf(&e.root, &["check", PG, "1", "--as", "kit"]);
    let results = vec![wait_out(a), wait_out(b)];
    let wins = results.iter().filter(|(ok, _)| *ok).count();
    assert_eq!(wins, 1, "{results:?}");
    for (ok, out) in &results {
        if !*ok {
            assert!(out.contains("no longer in return with the same pack and return") || out.contains("already passed its check"), "{out}");
        }
    }
    let log = e.log();
    assert_eq!(log.lines().filter(|l| l.contains("\"kind\":\"check\"")).count(), 1, "{log}");
}

#[test]
fn verify_reports_missing_unreadable_and_changed_views() {
    let e = Env::ready("views");
    let page = e.page();
    fs::remove_file(page.join("01.md")).unwrap();
    fs::write(page.join("06.md"), "hand edited\n").unwrap();
    let un = page.join("04.md");
    let mut perms = fs::metadata(&un).unwrap().permissions();
    perms.set_mode(0o000);
    fs::set_permissions(&un, perms).unwrap();

    let (ok, out) = e.wf(&["verify", PG]);
    assert!(!ok, "{out}");
    assert!(out.contains("missing view files: 01.md"), "{out}");
    assert!(out.contains("unreadable view files: 04.md"), "{out}");
    assert!(out.contains("view files differ from the log (hand edit or a failed reprint): 06.md"), "{out}");

    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "missing view files: 01.md");
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "unreadable view files: 04.md");
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "view files differ from the log (hand edit or a failed reprint): 06.md");

    let (ok, out) = e.wf(&["verify", PG, "--fix"]);
    assert!(!ok, "{out}");
    assert!(out.contains("reprinted from the log: 01.md, 06.md"), "{out}");
    assert!(out.contains("unreadable view files: 04.md"), "{out}");
    assert!(page.join("01.md").is_file());
    assert!(fs::read_to_string(page.join("06.md")).unwrap().contains("read 04"));

    let mut perms = fs::metadata(&un).unwrap().permissions();
    perms.set_mode(0o644);
    fs::set_permissions(&un, perms).unwrap();
    let out = e.ok(&["verify", PG]);
    assert!(out.contains("every view matches the log"), "{out}");
}

#[test]
fn return_refuses_a_rename_out_of_scope() {
    let e = Env::ready("ren");
    e.open("src/a.rs,src/c.rs", "true");
    let name = format!("{PG}.05.01");
    let prompt = fs::read_to_string(e.page().join("05.01/PROMPT.md")).unwrap();
    let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
    e.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
    e.git(&["mv", "src/b.rs", "src/c.rs"]);
    fs::write(e.root.join("game/src/a.rs"), "a = 2\n").unwrap();
    fs::create_dir_all(e.root.join("game/.workshop/returns")).unwrap();
    let ret = format!("pack: {hash}\ndone: renamed b to c\nchanged: create src/c.rs, modify src/a.rs\nnoticed: none\nw01: done - a is 2\nproof: tests\nnot done: none\nunprompted: none\noverflow: none\n");
    fs::write(e.root.join(format!("game/.workshop/returns/{name}.md")), ret).unwrap();
    e.git(&["add", "-A"]);
    e.git(&["commit", "-q", "-m", "work"]);
    let sha = e.git(&["rev-parse", "HEAD"]);
    e.git(&["checkout", "-q", "main"]);
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(!ok && out.contains("src/b.rs outside may touch"), "{out}");
    assert!(e.log().contains("\"kind\":\"return-refused\""));
}

#[test]
fn return_keeps_git_letters_and_prints_them_as_evidence() {
    let e = Env::checked("gitlist");
    let face05 = fs::read_to_string(e.page().join("05.md")).unwrap();
    assert!(face05.contains("git: A .workshop/returns/1.2.3.4.05.01.md, M src/a.rs"), "{face05}");
    assert!(face05.contains("changed: modify src/a.rs"), "{face05}");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    let rec = e.ok(&["close", PG, "1", "--as", "pri"]);
    assert!(rec.contains("git: A .workshop/returns/1.2.3.4.05.01.md, M src/a.rs"), "{rec}");
}

#[test]
fn torn_last_log_line_is_named_and_left_alone() {
    let e = Env::ready("torn");
    let log = e.page().join("log.jsonl");
    let before = e.log();
    let n = before.lines().count();
    let cut = before.rfind(',').expect("comma in last line");
    let torn = format!("{}\n", &before[..cut]).into_bytes();
    fs::write(&log, &torn).unwrap();
    let msg = format!("last line is half written: entry {n}; nothing was changed");
    e.no(&["verify", PG], &msg);
    e.no(&["verify", PG, "--fix"], &msg);
    e.no(&["status", PG], &msg);
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], &msg);
    assert_eq!(fs::read(&log).unwrap(), torn);
}

#[test]
fn close_passed_refuses_face_01_change_after_signoff_even_with_a_stored_note() {
    let e = Env::checked("close-after");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w01=carried", "--note", "hold for later (t275u)", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a.\nDone when: something new.", "--as", "pri"]);
    e.no(&["close", PG, "1", "--as", "pri"], "face 01 changed after the signoff entry");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--cards", "w01=carried", "--note", "same goal (t275u)", "--as", "pri"]);
    let rec = e.ok(&["close", PG, "1", "--as", "pri"]);
    assert!(rec.contains("w01 carried"), "{rec}");
}

#[test]
fn grant_ref_must_be_nonblank() {
    let e = Env::ready("grantref");
    e.no(&["grant", PG, "--paths", "lib/", "--ref", " ", "--as", "mat"], "--ref must have non-blank text");
    e.ok(&["grant", PG, "--paths", "lib/", "--ref", "t275u", "--as", "mat"]);
    assert!(e.log().contains("\"ref\":\"t275u\""));
}

#[test]
fn log_without_trailing_newline_is_named_and_left_alone() {
    let e = Env::ready("nonewline");
    let log = e.page().join("log.jsonl");
    let before = e.log();
    let n = before.lines().count();
    assert!(before.ends_with('\n'), "{before:?}");
    let stripped = before.trim_end_matches('\n');
    fs::write(&log, stripped).unwrap();
    let msg = format!("last line has no newline: entry {n}; nothing was changed");
    e.no(&["verify", PG], &msg);
    e.no(&["verify", PG, "--fix"], &msg);
    e.no(&["status", PG], &msg);
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], &msg);
    assert_eq!(fs::read_to_string(&log).unwrap(), stripped);
}

#[test]
fn log_append_source_writes_one_record_and_syncs_new_dir() {
    let src = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/log.rs"));
    let append = src.split("pub fn append").nth(1).and_then(|s| s.split("fn write_record").next()).unwrap_or("");
    assert!(!src.contains("writeln!(f"), "append must not use writeln! (it writes the line and the newline separately)");
    assert!(append.contains("write_record") && src.contains("write_all"), "append should write the JSON line and its newline in one write");
    assert!(append.contains("sync_all"), "append should sync the log file");
    assert!(
        append.contains("sync_dir") || append.contains("parent()"),
        "when append creates log.jsonl it should sync the page folder"
    );
}

#[test]
fn verify_reports_a_view_symlink_and_fix_replaces_it_without_writing_through() {
    let e = Env::ready("symlink");
    let page = e.page();
    let outside = e.root.join("outside-01.md");
    let original = fs::read_to_string(page.join("01.md")).unwrap();
    fs::write(&outside, &original).unwrap();
    fs::remove_file(page.join("01.md")).unwrap();
    unix_fs::symlink(&outside, page.join("01.md")).unwrap();
    assert!(page.join("01.md").is_symlink());

    let dangling_target = e.root.join("missing-06.md");
    fs::remove_file(page.join("06.md")).unwrap();
    unix_fs::symlink(&dangling_target, page.join("06.md")).unwrap();
    assert!(!dangling_target.exists());

    let (ok, out) = e.wf(&["verify", PG]);
    assert!(!ok, "{out}");
    assert!(out.contains("view files differ from the log (hand edit or a failed reprint): 01.md"), "{out}");
    assert!(out.contains("06.md"), "{out}");

    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "view files differ from the log (hand edit or a failed reprint): 01.md");

    let out = e.ok(&["verify", PG, "--fix"]);
    assert!(out.contains("reprinted from the log: 01.md"), "{out}");
    assert!(out.contains("06.md"), "{out}");
    assert!(page.join("01.md").is_file() && !page.join("01.md").is_symlink(), "01.md should be a regular file");
    assert!(page.join("06.md").is_file() && !page.join("06.md").is_symlink(), "06.md should be a regular file");
    assert_eq!(fs::read_to_string(&outside).unwrap(), original, "must not write through the symlink");
    assert!(!dangling_target.exists(), "must not create a file at the dangling target");
    assert!(e.ok(&["verify", PG]).contains("every view matches the log"));
}

#[test]
fn return_accepts_git_paths_with_spaces_tabs_newlines_and_non_ascii() {
    let e = Env::ready("qpath");
    e.git(&["config", "core.quotepath", "true"]);
    e.open("src/", "true");
    let name = format!("{PG}.05.01");
    let prompt = fs::read_to_string(e.page().join("05.01/PROMPT.md")).unwrap();
    let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
    e.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
    let game = e.root.join("game");
    fs::write(game.join("src/a space.rs"), "space\n").unwrap();
    fs::write(game.join("src/a\tb.rs"), "tab\n").unwrap();
    fs::write(game.join("src/a\nb.rs"), "newline\n").unwrap();
    fs::write(game.join("src/é.rs"), "eacute\n").unwrap();
    fs::create_dir_all(game.join(".workshop/returns")).unwrap();
    let ret = format!("pack: {hash}\ndone: unusual names\nchanged: create src/a space.rs\nnoticed: none\nw01: done - names\nproof: tests\nnot done: none\nunprompted: none\noverflow: none\n");
    fs::write(game.join(format!(".workshop/returns/{name}.md")), ret).unwrap();
    e.git(&["add", "-A"]);
    e.git(&["commit", "-q", "-m", "work"]);
    let sha = e.git(&["rev-parse", "HEAD"]);
    e.git(&["checkout", "-q", "main"]);
    let name_ret = format!("{PG}.05.01");
    let (ok, out) = e.wf_git(
        &["return", PG, "1", "--branch", &format!("pass/{name_ret}"), "--commit", &sha, "--file", &format!(".workshop/returns/{name_ret}.md"), "--as", "bob"],
        "core.quotePath",
        "true",
    );
    assert!(ok, "{out}");
    let log = e.log();
    assert!(log.contains("src/a space.rs"), "{log}");
    assert!(log.contains("src/a\\tb.rs"), "{log}");
    assert!(log.contains("src/a\\nb.rs"), "{log}");
    assert!(log.contains("src/é.rs"), "{log}");
}

#[test]
fn verify_reports_a_symlinked_pass_folder_and_fix_refuses_without_writing_through() {
    let e = Env::ready("symdir");
    e.open("src/a.rs", "true");
    let page = e.page();
    let outside = e.root.join("ext-0501");
    fs::rename(page.join("05.01"), &outside).unwrap();
    unix_fs::symlink(&outside, page.join("05.01")).unwrap();
    assert!(page.join("05.01").is_symlink());

    let pack = outside.join("PACK.md");
    let original = fs::read_to_string(&pack).unwrap();

    let (ok, out) = e.wf(&["verify", PG]);
    assert!(!ok, "{out}");
    assert!(out.contains("view files differ from the log (hand edit or a failed reprint):"), "{out}");
    assert!(out.contains("05.01/PACK.md"), "{out}");
    assert!(out.contains("05.01/AGENTS.md"), "{out}");

    let (ok, out) = e.wf(&["verify", PG, "--fix"]);
    assert!(!ok, "{out}");
    assert!(out.contains("linked folder: 05.01"), "{out}");
    assert!(out.contains("nothing was changed"), "{out}");
    assert_eq!(fs::read_to_string(&pack).unwrap(), original, "must not write through the linked folder");
    assert!(page.join("05.01").is_symlink(), "must not replace the linked folder");

    e.no(
        &["face-write", PG, "06", "--text", "x", "--as", "pri"],
        "view files differ from the log (hand edit or a failed reprint):",
    );
    assert_eq!(fs::read_to_string(&pack).unwrap(), original, "a write must not touch the outside folder");
    assert_eq!(fs::read_to_string(outside.join("PACK.md")).unwrap(), original);
}

#[test]
fn reprint_replaces_a_hardlinked_view_without_writing_through() {
    let e = Env::ready("hardlink");
    let page = e.page();
    let view = page.join("06.md");
    let outside = e.root.join("hard-06.md");
    let original = fs::read_to_string(&view).unwrap();
    fs::hard_link(&view, &outside).unwrap();
    assert_eq!(fs::metadata(&view).unwrap().nlink(), 2);

    e.ok(&["face-write", PG, "06", "--text", "new note", "--as", "pri"]);

    assert_eq!(fs::read_to_string(&outside).unwrap(), original, "must not write through the hard link");
    assert!(view.is_file() && !view.is_symlink(), "06.md should stay a regular file");
    assert_eq!(fs::metadata(&view).unwrap().nlink(), 1, "the hard link should be replaced");
    assert!(fs::read_to_string(&view).unwrap().contains("new note"), "the view should have the new text");
    assert!(!fs::read_to_string(&outside).unwrap().contains("new note"));
}

#[test]
fn draft_refuses_pass_0() {
    let e = Env::ready("pass0");
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/a.rs\nchecks: true\nstop if: b must change\n").unwrap();
    let file = f.to_str().unwrap();
    e.no(&["draft", PG, "--pass", "0", "--file", file, "--as", "pri"], "refused: pass 0 is not allowed (R9)");
    e.no(&["draft", PG, "--pass", "00", "--file", file, "--as", "pri"], "refused: pass 0 is not allowed (R9)");
    e.no(&["draft", PG, "--pass", "05.00", "--file", file, "--as", "pri"], "refused: pass 0 is not allowed (R9)");
    assert!(!e.log().contains("\"kind\":\"draft\""), "pass 0 must not be logged");
}

#[test]
fn draft_refuses_a_99th_pass() {
    let start = std::time::Instant::now();
    let e = Env::ready("pass98");
    seed_closed_passes(&e, 98);
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/a.rs\nchecks: true\nstop if: b must change\n").unwrap();
    let file = f.to_str().unwrap();
    let st = e.ok(&["status", PG]);
    assert!(st.contains("05.98  closed"), "{st}");
    let before = e.log();
    e.no(
        &["draft", PG, "--file", file, "--as", "pri"],
        "counter 98 reached: after 98 is open (QD16); ask Prime",
    );
    assert_eq!(e.log(), before, "a refused 99th draft must not append");
    e.no(
        &["draft", PG, "--pass", "99", "--file", file, "--as", "pri"],
        "counter 98 reached: after 98 is open (QD16); ask Prime",
    );
    e.no(
        &["draft", PG, "--pass", "05.99", "--file", file, "--as", "pri"],
        "counter 98 reached: after 98 is open (QD16); ask Prime",
    );
    let elapsed = start.elapsed();
    assert!(
        elapsed < std::time::Duration::from_secs(10),
        "99-pass test took {elapsed:?}, want under 10 s"
    );
}

#[test]
fn reprint_failure_after_append_says_logged_as() {
    let e = Env::ready("loggedas");
    e.draft("src/a.rs", "true");
    let page = e.page();
    let outside = e.root.join("ext-0501");
    fs::create_dir_all(&outside).unwrap();
    unix_fs::symlink(&outside, page.join("05.01")).unwrap();
    let n = e.log().lines().count() + 1;
    let (ok, out) = e.wf(&["pack", PG, "1", "--as", "pri"]);
    assert!(!ok, "{out}");
    assert!(
        out.contains(&format!("logged as entry {n}; views not reprinted ("))
            && out.contains("linked folder: 05.01")
            && out.contains(&format!("run wf verify {PG} --fix")),
        "{out}"
    );
    assert_eq!(e.log().lines().count(), n, "the pack must have been logged");
    assert!(e.log().contains("\"kind\":\"pack\""), "{}", e.log());
    assert!(page.join("05.01").is_symlink(), "must not replace the pre-made link");
    assert!(fs::read_dir(&outside).unwrap().next().is_none(), "must not write through the linked folder");
}

#[test]
fn reprint_failure_when_temp_path_is_a_directory_says_logged_as() {
    let e = Env::ready("tmptmp");
    fs::create_dir(e.page().join(".06.md.wf-tmp")).unwrap();
    let n = e.log().lines().count() + 1;
    let (ok, out) = e.wf(&["face-write", PG, "06", "--text", "x", "--as", "pri"]);
    assert!(!ok, "{out}");
    assert!(
        out.contains(&format!("logged as entry {n}; views not reprinted ("))
            && out.contains("cannot write")
            && out.contains(&format!("run wf verify {PG} --fix")),
        "{out}"
    );
    assert!(!out.contains("nothing was changed"), "{out}");
    assert_eq!(e.log().lines().count(), n, "the face write must have been logged");
}

#[test]
fn write_atomic_source_opens_temp_with_create_new() {
    let src = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/render.rs"));
    let body = src.split("fn write_atomic").nth(1).and_then(|s| s.split("pub fn edited").next()).unwrap_or("");
    assert!(body.contains("create_new(true)"), "write_atomic should open the temp file with create_new");
    assert!(!body.contains("File::create"), "write_atomic must not use File::create (it follows a symlink at the temp path)");
}

#[test]
fn halt_and_resume_need_prime_or_person_and_a_note_with_ref() {
    let e = Env::ready("halt");
    e.no(&["halt", PG, "--note", "stop (t1)", "--as", "bob"], "only Prime (pri) or the person (mat)");
    e.no(&["halt", PG, "--as", "pri"], "--note needs a reason and a (ref)");
    e.no(&["halt", PG, "--note", "stop", "--as", "pri"], "--note needs a reason and a (ref)");
    e.no(&["halt", PG, "--note", "  (t1)", "--as", "pri"], "--note needs a reason and a (ref)");
    e.ok(&["halt", PG, "--note", "wait for Matthew (t301u)", "--as", "mat"]);
    assert!(e.log().contains("\"kind\":\"halt\"") && e.log().contains("wait for Matthew (t301u)"), "{}", e.log());
    e.no(&["halt", PG, "--note", "again (t1)", "--as", "pri"], "already halted");
    e.no(&["resume", PG, "--note", "go", "--as", "pri"], "--note needs a reason and a (ref)");
    e.no(&["resume", PG, "--note", "go (t1)", "--as", "bob"], "only Prime (pri) or the person (mat)");
    e.ok(&["resume", PG, "--note", "answered (t302u)", "--as", "pri"]);
    assert!(e.log().contains("\"kind\":\"resume\"") && e.log().contains("answered (t302u)"), "{}", e.log());
    e.no(&["resume", PG, "--note", "again (t1)", "--as", "pri"], "is not halted");
    assert!(e.ok(&["help"]).contains("halt <page> --note"));
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
}

#[test]
fn halt_is_refused_while_a_pass_is_open() {
    let e = Env::ready("halt-open");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    e.no(&["halt", PG, "--note", "stop (t1)", "--as", "pri"], "refused: 05.01 is at 'pack'; halt only when no pass is open");
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    e.no(&["halt", PG, "--note", "stop (t1)", "--as", "mat"], "refused: 05.01 is at 'open'");
    let e = Env::checked("halt-review");
    let before = e.log();
    e.no(&["halt", PG, "--note", "stop (t1)", "--as", "pri"], "refused: 05.01 is at 'review'");
    assert_eq!(e.log(), before, "a refused halt must not append");
}

#[test]
fn halted_page_shows_in_status_and_stops_draft_pack_claim() {
    let e = Env::ready("halted");
    e.draft("src/a.rs", "true");
    e.ok(&["halt", PG, "--note", "wait for Matthew (t301u)", "--as", "pri"]);
    let st = e.ok(&["status", PG]);
    assert!(st.contains("halted:  by pri at ") && st.contains("wait for Matthew (t301u)"), "{st}");
    assert!(st.contains("next:    halted. Prime (pri) or the person (mat) resumes it: wf resume 1.2.3.4 --note"), "{st}");
    let f = e.root.join("pack.txt");
    let before = e.log();
    for args in [vec!["draft", PG, "--pass", "1", "--file", f.to_str().unwrap(), "--as", "pri"], vec!["pack", PG, "1", "--as", "pri"], vec!["claim", PG, "1", "--as", "bob"]] {
        e.no(&args, "refused: page 1.2.3.4 is halted (by pri, entry ");
        e.no(&args, "Prime (pri) or the person (mat) resumes it: wf resume 1.2.3.4");
    }
    assert_eq!(e.log(), before, "refusals on a halted page must not append");
    let later = e.wf_at(&["observe", PG], Some(4_000_000_000)).1;
    assert!(!later.contains("stalled"), "{later}");
    e.ok(&["resume", PG, "--note", "answered (t302u)", "--as", "mat"]);
    assert!(!e.ok(&["status", PG]).contains("halted"));
    assert!(e.wf_at(&["observe", PG], Some(4_000_000_000)).1.contains("stalled"));
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    e.ok(&["claim", PG, "1", "--as", "bob"]);
}

#[test]
fn draft_is_refused_while_an_earlier_pass_is_not_closed() {
    let e = Env::ready("draft-open");
    let f = e.root.join("pack.txt");
    let file = f.to_str().unwrap().to_string();
    let refused = |tail: &str, next: &str| {
        let before = e.log();
        e.no(&["draft", PG, "--file", &file, "--as", "pri"], &format!("refused: 05.01 is at '{tail}' and not closed"));
        e.no(&["draft", PG, "--file", &file, "--as", "pri"], next);
        assert_eq!(e.log(), before, "a refused draft must not append");
    };
    e.draft("src/a.rs", "true");
    refused("draft", "Next for 05.01: Prime releases it: wf pack 1.2.3.4 1, or redraft it: wf draft 1.2.3.4 --pass 1");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    refused("pack", "Next for 05.01: a builder claims it: wf claim 1.2.3.4 1");
    e.ok(&["claim", PG, "1", "--as", "bob"]);
    refused("open", "Next for 05.01: bob pushes the work, then wf return 1.2.3.4 1");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a is 2");
    assert!(e.ret(1, &sha, "bob").0);
    refused("return", "Next for 05.01: a checker (not the builder) runs wf check 1.2.3.4 1");
    e.ok(&["check", PG, "1", "--as", "cat"]);
    refused("review", "Next for 05.01: Prime (pri) reads the check report, then wf signoff 1.2.3.4 1");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    refused("review", "Next for 05.01: wf close 1.2.3.4 1");
    e.ok(&["close", PG, "1", "--as", "pri"]);
    e.ok(&["face-write", PG, "06", "--text", "read 04 and closed 05.01", "--as", "pri"]);
    assert!(e.ok(&["draft", PG, "--file", &file, "--as", "pri"]).contains("drafted 05.02"));
}

#[test]
fn draft_overlap_ok_lets_prime_draft_while_a_pass_is_open() {
    let e = Env::ready("draft-ov");
    e.open("src/a.rs", "true");
    let f = e.root.join("p2.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/b.rs\nchecks: true\nstop if: b must change\n").unwrap();
    let file = f.to_str().unwrap();
    let before = e.log();
    e.no(&["draft", PG, "--file", file, "--as", "pri"], "refused: 05.01 is at 'open' and not closed");
    assert_eq!(e.log(), before, "a refused draft must not append");
    let out = e.ok(&[
        "draft", PG, "--file", file, "--overlap-ok", "1", "--why", "several models can work one page (t262u)", "--as", "pri",
    ]);
    assert!(out.contains("drafted 05.02"), "{out}");
    assert!(e.log().contains("\"overlap_ok\":1") && e.log().contains("several models can work one page (t262u)"), "{}", e.log());
    // a pass still at draft cannot be overlapped
    let f3 = e.root.join("p3.txt");
    fs::write(&f3, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/b.rs\nchecks: true\nstop if: b must change\n").unwrap();
    e.no(
        &["draft", PG, "--file", f3.to_str().unwrap(), "--overlap-ok", "1", "--why", "again (t262u)", "--as", "pri"],
        "refused: 05.02 is at 'draft' and not closed",
    );
    e.no(
        &["draft", PG, "--file", f3.to_str().unwrap(), "--overlap-ok", "2", "--why", "again (t262u)", "--as", "pri"],
        "--overlap-ok 05.02 is not open (tail is draft)",
    );

    let plan = "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/b.rs\nchecks: true\nstop if: b must change\n";
    let e = Env::ready("draft-ov-pack");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    let f = e.root.join("p2.txt");
    fs::write(&f, plan).unwrap();
    assert!(e.ok(&[
        "draft", PG, "--file", f.to_str().unwrap(), "--overlap-ok", "1", "--why", "several models can work one page (t262u)", "--as", "pri",
    ]).contains("drafted 05.02"));

    let e = Env::checked("draft-ov-rev");
    let f = e.root.join("p2.txt");
    fs::write(&f, plan).unwrap();
    assert!(e.ok(&[
        "draft", PG, "--file", f.to_str().unwrap(), "--overlap-ok", "1", "--why", "several models can work one page (t262u)", "--as", "pri",
    ]).contains("drafted 05.02"));
}

#[test]
fn pack_refuses_overlapping_may_touch() {
    let e = Env::ready("ov-ref");
    e.open("src/a.rs", "true");
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/\nchecks: true\nstop if: b must change\n").unwrap();
    e.ok(&[
        "draft", PG, "--file", f.to_str().unwrap(), "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri",
    ]);
    let (ok, out) = e.wf(&["pack", PG, "2", "--as", "pri"]);
    assert!(!ok, "{out}");
    assert!(out.contains("overlaps open pass 05.01") && out.contains("src/") && out.contains("src/a.rs"), "{out}");
}

#[test]
fn pack_allows_overlap_with_flag() {
    let e = Env::ready("ov-ok");
    e.open("src/a.rs", "true");
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: src/a.rs\nchecks: true\nstop if: b must change\n").unwrap();
    e.ok(&[
        "draft", PG, "--file", f.to_str().unwrap(), "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri",
    ]);
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--as", "pri"], "missing --why");
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--why", "no ref", "--as", "pri"], "--why needs a reason and a (ref)");
    e.ok(&["pack", PG, "2", "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri"]);
    assert!(e.log().contains("\"overlap_ok\":1") && e.log().contains("shared files (t275u)"), "{}", e.log());
}

#[test]
fn plus_one_is_not_read_as_pass_1() {
    let e = Env::ready("plus1");
    e.draft("src/a.rs", "true");
    let f = e.root.join("pack.txt");
    let file = f.to_str().unwrap();
    let before = e.log();
    e.no(&["draft", PG, "--pass", "+1", "--file", file, "--as", "pri"], "bad --pass");
    e.no(&["pack", PG, "+1", "--as", "pri"], "give the pass number, like 3 or 05.03");
    assert_eq!(e.log(), before, "+1 must not be accepted as pass 1");
    // a real pack of pass 1 still works, so the earlier +1 did not consume it
    e.ok(&["pack", PG, "1", "--as", "pri"]);
}

#[test]
fn pass_100_is_not_printed_as_05_100() {
    let e = Env::ready("p100");
    let (ok, out) = e.wf(&["pack", PG, "100", "--as", "pri"]);
    assert!(!ok, "{out}");
    assert!(out.contains("no pass 100 on this page"), "{out}");
    assert!(!out.contains("05.100"), "{out}");
}

#[test]
fn halt_note_refuses_a_newline() {
    let e = Env::ready("halt-nl");
    let before = e.log();
    e.no(
        &["halt", PG, "--note", "wait for Matthew (t301u)\nnext: draft", "--as", "pri"],
        "--note cannot contain control characters",
    );
    e.no(&["halt", PG, "--note", "wait\there (t1)", "--as", "pri"], "--note cannot contain control characters");
    e.no(&["halt", PG, "--note", "wait\rhere (t1)", "--as", "pri"], "--note cannot contain control characters");
    assert_eq!(e.log(), before, "a refused halt must not append");
    let st = e.ok(&["status", PG]);
    assert!(!st.lines().any(|l| l.trim() == "next: draft"), "{st}");
    assert!(!st.contains("halted:"), "{st}");
    e.ok(&["halt", PG, "--note", "wait for Matthew (t301u)", "--as", "pri"]);
    e.no(&["resume", PG, "--note", "go\non (t1)", "--as", "pri"], "--note cannot contain control characters");
    let log = e.log();
    assert!(log.contains("\"kind\":\"halt\""), "{log}");
    assert!(!log.contains("\"kind\":\"resume\""), "{log}");
}

#[test]
fn job_box_names_axioms_in_the_kit_folder() {
    let e = Env::ready("kitpath");
    e.draft("src/a.rs", "true");
    let out = e.ok(&["pack", PG, "1", "--as", "pri"]);
    assert!(out.contains("kit folder") && out.contains("docs/AXIOMS.md") && out.contains("not the run folder that holds pages/"), "{out}");
    let agents = fs::read_to_string(e.page().join("05.01/AGENTS.md")).unwrap();
    assert!(agents.contains("in the kit folder") && agents.contains("docs/AXIOMS.md") && agents.contains("not beside pages/"), "{agents}");
    let pack = fs::read_to_string(e.page().join("05.01/PACK.md")).unwrap();
    assert!(pack.contains("in the kit folder") && pack.contains("docs/DESIGN.md"), "{pack}");
}


fn real_pages_dir() -> Option<PathBuf> {
    if let Ok(p) = std::env::var("WF_TEST_PAGES") {
        let p = PathBuf::from(p);
        if p.join("90.10.00.0001/log.jsonl").is_file() {
            return Some(p);
        }
    }
    for c in [
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../pages"),
        PathBuf::from("/workspace/workshop-build/wf-run/pages"),
    ] {
        if c.join("90.10.00.0001/log.jsonl").is_file() {
            return Some(c);
        }
    }
    None
}

fn copy_dir(src: &PathBuf, dst: &PathBuf) {
    fs::create_dir_all(dst).unwrap();
    for ent in fs::read_dir(src).unwrap() {
        let ent = ent.unwrap();
        let name = ent.file_name();
        if name == ".wf-lock" {
            continue;
        }
        let from = ent.path();
        let to = dst.join(&name);
        let meta = fs::symlink_metadata(&from).unwrap();
        if meta.is_dir() {
            copy_dir(&from, &to);
        } else if meta.file_type().is_file() {
            fs::copy(&from, &to).unwrap();
        }
    }
}

fn file_bytes(dir: &PathBuf) -> std::collections::BTreeMap<String, Vec<u8>> {
    let mut out = std::collections::BTreeMap::new();
    fn walk(base: &PathBuf, cur: &PathBuf, out: &mut std::collections::BTreeMap<String, Vec<u8>>) {
        for ent in fs::read_dir(cur).unwrap() {
            let ent = ent.unwrap();
            let p = ent.path();
            if p.is_dir() {
                walk(base, &p, out);
            } else if p.is_file() {
                let rel = p.strip_prefix(base).unwrap().to_string_lossy().to_string();
                out.insert(rel, fs::read(&p).unwrap());
            }
        }
    }
    walk(dir, dir, &mut out);
    out
}

/// w01: copies of the three real pages still verify with the current templates.
/// Past packs have no template version, so they must reprint from the v1 (8eb1fdb) text.
#[test]
fn past_packed_pages_still_verify() {
    let Some(src) = real_pages_dir() else {
        eprintln!("skipping past_packed_pages_still_verify: real pages not found at ../pages or /workspace/workshop-build/wf-run/pages");
        return;
    };
    let root = std::env::temp_dir().join(format!("wf-test-{}-realpages", std::process::id()));
    let _ = fs::remove_dir_all(&root);
    fs::create_dir_all(root.join("pages")).unwrap();
    let addrs = ["90.10.00.0001", "90.20.00.0001", "90.30.00.0001"];
    for addr in addrs {
        copy_dir(&src.join(addr), &root.join("pages").join(addr));
    }
    let bin = env!("CARGO_BIN_EXE_wf");
    for addr in addrs {
        let before = file_bytes(&root.join("pages").join(addr));
        let v = Command::new(bin).env("WF_ROOT", &root).args(["verify", addr]).output().unwrap();
        let out = format!("{}{}", String::from_utf8_lossy(&v.stdout), String::from_utf8_lossy(&v.stderr));
        assert!(v.status.success(), "verify {addr} failed: {out}");
        assert!(out.contains("ok: log chain holds"), "verify {addr}: {out}");
        let fix = Command::new(bin).env("WF_ROOT", &root).args(["verify", addr, "--fix"]).output().unwrap();
        let fout = format!("{}{}", String::from_utf8_lossy(&fix.stdout), String::from_utf8_lossy(&fix.stderr));
        assert!(fix.status.success(), "verify --fix {addr} failed: {fout}");
        assert!(fout.contains("ok: log chain holds"), "verify --fix {addr} should be a no-op: {fout}");
        assert!(!fout.contains("reprinted"), "verify --fix {addr} must change no file: {fout}");
        let after = file_bytes(&root.join("pages").join(addr));
        assert_eq!(before, after, "verify --fix changed a file on {addr}");
    }
    let _ = fs::remove_dir_all(&root);
}

#[test]
fn new_pack_records_template_version_2() {
    let e = Env::ready("tmpl-ver");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "1", "--as", "pri"]);
    let log = e.log();
    assert!(log.contains("\"templates\":\"2\""), "{log}");
    let agents = fs::read_to_string(e.page().join("05.01/AGENTS.md")).unwrap();
    assert!(agents.contains("kit folder") && agents.contains("cargo clean -p wf"), "{agents}");
}

/// w02: plant each refused class through --as, --title and a note.
#[test]
fn printed_fields_refuse_every_unsafe_char_class() {
    let e = Env::ready("safe-txt");
    let classes: &[(&str, char)] = &[
        ("C0 ESC", '\u{001B}'),
        ("DEL", '\u{007F}'),
        ("C1 NEL", '\u{0085}'),
        ("U+2028", '\u{2028}'),
        ("U+2029", '\u{2029}'),
        ("bidi RLO", '\u{202E}'),
        ("zero-width space", '\u{200B}'),
        ("LTR mark", '\u{200E}'),
        ("RTL mark", '\u{200F}'),
        ("ALM", '\u{061C}'),
        ("soft hyphen", '\u{00AD}'),
        ("function application", '\u{2061}'),
        ("language tag", '\u{E0001}'),
        ("Hangul filler", '\u{3164}'),
        ("choseong filler", '\u{115F}'),
        ("jungseong filler", '\u{1160}'),
    ];
    let before = e.log();
    for (name, ch) in classes {
        let planted = format!("x{ch}y");
        e.no(&["halt", PG, "--note", "wait (t1)", "--as", &planted], "--as cannot contain control characters");
        e.no(
            &["init-page", "9.9.9.9", "--title", &planted, "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"],
            "--title cannot contain control characters",
        );
        e.no(&["halt", PG, "--note", &format!("wait{ch} (t1)"), "--as", "pri"], "--note cannot contain control characters");
        let _ = name;
    }
    assert_eq!(e.log(), before, "a refused command must not append");
    // Face text from --file keeps newlines but refuses the rest.
    let f = e.root.join("face01.txt");
    fs::write(&f, "Goal: a.\nDone when: checks pass.\n").unwrap();
    e.ok(&["face-write", PG, "01", "--file", f.to_str().unwrap(), "--as", "pri"]);
    fs::write(&f, "Goal: a.\u{001B}hidden\nDone when: checks pass.\n").unwrap();
    e.no(&["face-write", PG, "01", "--file", f.to_str().unwrap(), "--as", "pri"], "--file cannot contain control characters");
    fs::write(&f, "Goal: a.\r\nDone when: checks pass.\n").unwrap();
    e.no(&["face-write", PG, "01", "--file", f.to_str().unwrap(), "--as", "pri"], "--file cannot contain control characters");
    e.no(&["halt", PG, "--note", "\u{0301}\u{0301} (t1)", "--as", "pri"], "--note cannot be only combining marks");
    e.no(&["halt", PG, "--note", "wait (t1)", "--as", "\u{0301}\u{0301}"], "--as cannot be only combining marks");
}

#[test]
fn agents_overlap_line_cites_t262u() {
    let t = include_str!("../AGENTS.md");
    let line = t.lines().find(|l| l.contains("overlap-ok")).expect("overlap line");
    assert!(line.contains("t262u"), "{line}");
    assert!(line.contains("sometimes multiple models can sit at this"), "{line}");
    assert!(!t.contains("(t285u)"), "{t}");
}

#[test]
fn job_agents_template_has_clean_and_touch() {
    let t = include_str!("../templates/agents.txt");
    assert!(t.contains("cargo clean -p wf") && t.contains("touch the sources"), "{t}");
}


/// A hostile return job line is logged as evidence, but status, observe and 05.md show it escaped.
#[test]
fn planted_return_job_line_is_escaped_on_status_observe_and_views() {
    let e = Env::ready("esc-job");
    e.open("src/", "true");
    let hostile = "w01: need - x\u{1b}[2K\r  next: draft";
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], hostile);
    assert!(e.ret(1, &sha, "bob").0, "a hostile return must still be logged");
    let st = e.ok(&["status", PG]);
    assert!(!st.contains('\u{1b}'), "status must not show raw ESC: {st}");
    assert!(!st.contains('\r'), "status must not show raw CR: {st}");
    assert!(!st.lines().any(|l| l.trim() == "next: draft"), "status must not show a fake next line: {st}");
    assert!(st.contains("\\u{1b}") && st.contains("\\u{d}"), "status should show escaped ESC and CR: {st}");
    let ob = e.ok(&["observe", PG]);
    assert!(!ob.contains('\u{1b}') && !ob.contains('\r'), "observe must not show raw ESC/CR: {ob}");
    assert!(ob.contains("\\u{1b}") || st.contains("\\u{1b}"), "{ob}");
    let face = fs::read_to_string(e.page().join("05.md")).unwrap();
    assert!(!face.contains('\u{1b}'), "05.md must not show raw ESC: {face}");
    assert!(!face.contains('\r'), "05.md must not show raw CR: {face}");
    assert!(face.contains("\\u{1b}") && face.contains("\\u{d}"), "05.md should show escaped ESC and CR: {face}");
    assert!(e.log().contains("\\u001b") || e.log().contains("\u{1b}"), "{}", e.log());
}

/// Changed file names with ESC, bidi and U+2028 are escaped in 05.md.
#[test]
fn planted_file_names_are_escaped_in_views() {
    let e = Env::ready("esc-name");
    e.open("src/", "true");
    let name = format!("{PG}.05.01");
    let prompt = fs::read_to_string(e.page().join("05.01/PROMPT.md")).unwrap();
    let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
    e.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
    let game = e.root.join("game");
    let fname = "src/x\u{1b}y\u{202e}z\u{2028}w.rs";
    fs::write(game.join("src/a.rs"), "a = 2\n").unwrap();
    fs::write(game.join(fname), "plant\n").unwrap();
    fs::create_dir_all(game.join(".workshop/returns")).unwrap();
    let ret = format!("pack: {hash}\ndone: plant a name\nchanged: modify src/a.rs, create a planted name\nnoticed: none\nw01: done - names\nproof: tests\nnot done: none\nunprompted: none\noverflow: none\n");
    fs::write(game.join(format!(".workshop/returns/{name}.md")), ret).unwrap();
    e.git(&["add", "-A"]);
    e.git(&["commit", "-q", "-m", "work"]);
    let sha = e.git(&["rev-parse", "HEAD"]);
    e.git(&["checkout", "-q", "main"]);
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(ok, "{out}");
    let face = fs::read_to_string(e.page().join("05.md")).unwrap();
    assert!(!face.contains('\u{1b}'), "05.md raw ESC: {face}");
    assert!(!face.contains('\u{202e}'), "05.md raw bidi: {face}");
    assert!(!face.contains('\u{2028}'), "05.md raw U+2028: {face}");
    assert!(face.contains("\\u{1b}") && face.contains("\\u{202e}") && face.contains("\\u{2028}"), "{face}");
}

#[test]
fn draft_field_keys_are_checked() {
    let e = Env::ready("dkey");
    let f = e.root.join("pack.txt");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a\nmay touch: src/a.rs\nchecks: true\nstop if: none\nw0\u{1b}1: hidden\n").unwrap();
    e.no(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"], "--field cannot contain control characters");
    // CR in a pack field value is refused; newline is kept.
    fs::write(&f, "repo: game\nstart: main\noutcome: a =\r2\nw01: set a\nmay touch: src/a.rs\nchecks: true\nstop if: none\n").unwrap();
    e.no(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"], "--outcome cannot contain control characters");
    fs::write(&f, "repo: game\nstart: main\noutcome: a = 2\nw01: set a\n  still one job\nmay touch: src/a.rs\nchecks: true\nstop if: none\n").unwrap();
    e.ok(&["draft", PG, "--file", f.to_str().unwrap(), "--as", "pri"]);
}

// ---- wf board (docs/design/WF-BOARD.md): read only, built from the log ----

/// sha256 of every file under `dir` (relative path -> hex).
fn sha_map(dir: &PathBuf) -> std::collections::BTreeMap<String, String> {
    use sha2::{Digest, Sha256};
    file_bytes(dir).into_iter().map(|(k, v)| (k, Sha256::digest(&v).iter().map(|b| format!("{b:02x}")).collect())).collect()
}

/// Log entries written through the tool's own append (Page::add), then views reprinted.
/// Stands in for old log entries and for states the commands cannot reach today.
fn seed(e: &Env, page: &str, evs: &[(&str, &str, &str, serde_json::Value)]) {
    let mut p = wf::page::Page::load(&e.root.join("pages").join(page)).unwrap();
    for (actor, role, kind, data) in evs {
        p.add(actor, role, kind, data.clone()).unwrap();
    }
    wf::render::write(&p).unwrap();
}

fn seed_pack(nn: u32) -> serde_json::Value {
    serde_json::json!({"pass": nn, "pack_text": format!("pack {nn}\n"), "pack_hash": format!("{nn:064}"), "branch": format!("pass/{PG}.05.{nn:02}"),
        "return_file": format!(".workshop/returns/{PG}.05.{nn:02}.md"), "start": "0", "templates": "2", "sources": {}})
}

fn seed_draft(nn: u32) -> serde_json::Value {
    serde_json::json!({"pass": nn, "fields": {"outcome": format!("outcome {nn}"), "repo": "game", "start": "main", "w01": "x", "may touch": "src/b.rs", "checks": "true", "stop if": "none"}, "pins": {}})
}

/// Lines between "ATTENTION" and "COLUMNS".
fn attention_lines(b: &str) -> Vec<String> {
    b.lines().skip_while(|l| !l.starts_with("ATTENTION")).skip(1).take_while(|l| !l.starts_with("COLUMNS")).map(String::from).collect()
}

#[test]
fn board_writes_nothing() {
    let e = Env::checked("board-ro");
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "may we widen", "--as", "pri"]);
    let before = sha_map(&e.page());
    let log = e.log();
    for args in [vec!["board", PG], vec!["board", PG, "--all"], vec!["board", PG, "--card", "1"], vec!["board", PG, "--stall-hours", "0"], vec!["board"]] {
        let out = e.ok(&args);
        assert!(!out.is_empty(), "{args:?}");
        assert!(!e.page().join(".wf-lock").exists(), "{args:?} made a lock file");
    }
    assert_eq!(sha_map(&e.page()), before, "the board changed a page file");
    assert_eq!(e.log(), log);
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
    e.no(&["board", PG, "--stall-hours", "x"], "--stall-hours must be a whole number");
    e.no(&["board", PG, "--card", "7"], "no pass 05.07");
    assert!(e.ok(&["help"]).contains("board [<page>]"));
}

#[test]
fn board_puts_each_tail_in_its_column() {
    let e = Env::checked("board-cols"); // 05.01 at review
    let mut evs = closed_chain(2, "failed");
    evs[0].3 = seed_draft(2);
    seed(&e, PG, &evs);
    seed(&e, PG, &[
        ("pri", "prime", "draft", seed_draft(3)), ("pri", "prime", "pack", seed_pack(3)), ("bob", "builder", "claim", serde_json::json!({"pass": 3})),
        ("bob", "builder", "return", serde_json::json!({"pass": 3, "commit": "c3", "file": "f", "jobs": {"w01": "done - x"}})),
        ("pri", "prime", "draft", seed_draft(4)), ("pri", "prime", "pack", seed_pack(4)), ("ann", "builder", "claim", serde_json::json!({"pass": 4})),
        ("pri", "prime", "draft", seed_draft(5)), ("pri", "prime", "pack", seed_pack(5)),
        ("pri", "prime", "draft", seed_draft(6)),
    ]);
    let b = e.ok(&["board", PG]);
    let lines: Vec<&str> = b.lines().collect();
    for (col, nn) in [("Draft [estimate]: 1", 6), ("Ready [ready for a bay]: 1", 5), ("Working [in the bay]: 1", 4),
                      ("Waiting check [waiting QC]: 1", 3), ("Checked [QC done]: 1", 1), ("Closed [delivered]: 1 (passed 0, failed 1", 2)] {
        let i = lines.iter().position(|l| l.starts_with(&format!("  {col}"))).unwrap_or_else(|| panic!("{col}: {b}"));
        assert!(lines[i + 1].starts_with(&format!("    05.{nn:02}")), "{col}: {b}");
    }
    assert!(b.contains("held by ann | next: ann pushes the work"), "{b}");
    assert!(b.contains("WAITING CHECK 05.03") && b.contains("CHECKED 05.01: verdict pass by cat"), "{b}");
}

#[test]
fn board_attention_puts_person_questions_first_and_the_halt_second() {
    let e = Env::ready("board-order");
    e.close_one(1);
    e.ok(&["elevate", PG, "1", "--to", "prime", "--item", "which path", "--as", "bob"]);
    e.ok(&["elevate", PG, "1", "--to", "person", "--item", "may we widen", "--as", "pri"]);
    e.ok(&["halt", PG, "--note", "wait for Matthew (t301u)", "--as", "pri"]);
    let a = attention_lines(&e.ok(&["board", PG]));
    assert!(a[0].starts_with("  QUESTION for the person (mat): entry") && a[0].contains("may we widen"), "{a:?}");
    assert!(a[1].starts_with("  HALTED by pri") && a[1].contains("wf resume"), "{a:?}");
    assert!(a[2].starts_with("  QUESTION for Prime (pri)") && a[2].contains("which path"), "{a:?}");
}

#[test]
fn board_cap_never_cuts_person_questions_or_the_halt() {
    let e = Env::ready("board-cap");
    seed_closed_passes(&e, 20);
    let mut evs = vec![];
    for i in 0..5 {
        evs.push(("pri", "prime", "elevate", serde_json::json!({"pass": 20, "to": "person", "item": format!("person q {i}")})));
    }
    for i in 0..40 {
        evs.push(("bob", "builder", "elevate", serde_json::json!({"pass": 20, "to": "prime", "item": format!("prime q {i}")})));
    }
    seed(&e, PG, &evs);
    e.ok(&["halt", PG, "--note", "wait for Matthew (t301u)", "--as", "pri"]);
    let b = e.ok(&["board", PG]);
    assert!(b.lines().count() <= 40, "{} lines: {b}", b.lines().count());
    assert_eq!(b.matches("QUESTION for the person").count(), 5, "{b}");
    assert!(b.contains("HALTED by pri"), "{b}");
    let all = e.ok(&["board", PG, "--all"]);
    let optional = attention_lines(&all).len() - 6;
    let shown = attention_lines(&b).len() - 6;
    assert!(b.contains(&format!("not shown: {} attention lines, 3 cards, 17 older closed cards", optional - shown)), "{b}");
    assert_eq!(all.matches("(closed at entry").count(), 20);
    assert!(all.contains("footer: nothing cut"), "{all}");
}

#[test]
fn board_marks_a_waiting_pass_and_drift_as_stale() {
    let e = Env::ready("board-stale");
    e.open("src/a.rs", "true");
    let now = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs();
    let (ok, b) = e.wf_at(&["board", PG], Some(now));
    assert!(ok && !b.contains("STALE"), "{b}");
    let (ok, b) = e.wf_at(&["board", PG], Some(now + 25 * 3600));
    assert!(ok && b.contains("(open)  STALE") && b.contains("STALE 05.01: wait: no log entry for 25h (last entry 7; limit 24h)"), "{b}");
    let (_, b) = e.wf_at(&["board", PG, "--stall-hours", "48"], Some(now + 25 * 3600));
    assert!(!b.contains("STALE"), "{b}");
    e.ok(&["face-write", PG, "04", "--section", "goals", "--text", "b works too", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a and b.\nDone when: checks pass.", "--as", "pri"]);
    let b = e.ok(&["board", PG, "--card", "1"]);
    assert!(b.contains("drift: packed against face 04 entry 2; face 04 is now entry 8"), "{b}");
    assert!(b.contains("drift: packed against face 01 v1 entry 3; face 01 is now v2 entry 9"), "{b}");
}

#[test]
fn board_marks_an_old_check_and_an_old_signoff() {
    let e = Env::checked("board-oldcheck");
    let c = e.ok(&["board", PG, "--card", "1"]);
    assert!(c.contains("stale:      none found in the log"), "{c}");
    // A later return on another commit: the commands cannot reach this today, so it is seeded.
    // A return after a check is refused by the log rules; a check whose commit is not the
    // return's is the disagreement the board must show (seeded).
    seed(&e, PG, &[("cat", "checker", "check", serde_json::json!({"pass": 1, "commit": "d".repeat(40), "verdict": "pass", "report": ""}))]);
    let b = e.ok(&["board", PG]);
    assert!(b.contains("old check: check entry 10 was on commit dddddddddddd; the latest return (entry 8) is commit"), "{b}");

    let e = Env::checked("board-oldsign");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["face-write", PG, "01", "--text", "Goal: a, new.\nDone when: checks pass.", "--as", "pri"]);
    let b = e.ok(&["board", PG]);
    assert!(b.contains("old signoff: face 01 changed at entry 11, after the signoff entry 10"), "{b}");
}

#[test]
fn board_prints_from_the_log_over_a_hand_edit() {
    let e = Env::checked("board-edit");
    let face = e.page().join("05.md");
    let mut t = fs::read_to_string(&face).unwrap();
    t.push_str("hand edit\n");
    fs::write(&face, &t).unwrap();
    let before = sha_map(&e.page());
    let b = e.ok(&["board", PG]);
    assert!(b.contains("VIEWS DIFFER from the log") && b.contains("05.md") && b.contains("the log wins; run wf verify 1.2.3.4 --fix"), "{b}");
    assert!(b.contains("Checked [QC done]: 1"), "{b}");
    assert_eq!(sha_map(&e.page()), before);
    assert_eq!(fs::read_to_string(&face).unwrap(), t);
}

#[test]
fn board_escapes_hostile_log_text_everywhere() {
    let e = Env::ready("board-esc");
    e.open("src/", "true");
    let name = format!("{PG}.05.01");
    let prompt = fs::read_to_string(e.page().join("05.01/PROMPT.md")).unwrap();
    let hash = prompt.lines().find_map(|l| l.strip_prefix("Pack hash: ")).unwrap().split(' ').next().unwrap().to_string();
    e.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
    let game = e.root.join("game");
    fs::write(game.join("src/a.rs"), "a = 2\n").unwrap();
    fs::write(game.join("src/x\u{1b}y\u{202e}z\u{2028}w.rs"), "plant\n").unwrap();
    fs::create_dir_all(game.join(".workshop/returns")).unwrap();
    let ret = format!("pack: {hash}\ndone: plant\nchanged: names\nnoticed: none\nw01: need - x\u{1b}[2K\r  next: draft\nproof: tests\nnot done: none\nunprompted: none\noverflow: none\n");
    fs::write(game.join(format!(".workshop/returns/{name}.md")), ret).unwrap();
    e.git(&["add", "-A"]);
    e.git(&["commit", "-q", "-m", "work"]);
    let sha = e.git(&["rev-parse", "HEAD"]);
    e.git(&["checkout", "-q", "main"]);
    // Old log entries written before the input check: hostile names and items.
    let bad = "q\u{85}r\u{e0001}s\u{3164}t\u{2028}u\u{202e}v";
    seed(&e, PG, &[("wf", "tool", "return-refused", serde_json::json!({"pass": 1, "by": bad, "commit": "c", "why": format!("bad file src/\u{1b}]0;title\u{7}.rs {bad}")}))]);
    assert!(e.ret(1, &sha, "bob").0);
    seed(&e, PG, &[(bad, "prime", "elevate", serde_json::json!({"pass": 1, "to": "person", "item": bad}))]);
    let out = [e.ok(&["board", PG]), e.ok(&["board", PG, "--all"]), e.ok(&["board", PG, "--card", "1"]), e.ok(&["board"])].concat();
    for c in ['\u{1b}', '\r', '\u{7}', '\u{2028}', '\u{85}', '\u{202e}', '\u{e0001}', '\u{3164}'] {
        assert!(!out.contains(c), "raw U+{:04X} in board output: {out}", c as u32);
    }
    for want in ["\\u{1b}[2K\\u{d}", "\\u{202e}", "\\u{2028}", "\\u{85}", "\\u{e0001}", "\\u{3164}", "\\u{1b}]0;title\\u{7}"] {
        assert!(out.contains(want), "missing {want}: {out}");
    }
    assert!(!out.lines().any(|l| l.trim() == "next: draft"), "{out}");
}

#[test]
fn board_card_names_evidence_paths_that_exist() {
    let e = Env::checked("board-card");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["close", PG, "1", "--as", "pri"]);
    let c = e.ok(&["board", PG, "--card", "01"]);
    let files: Vec<&str> = c.lines().filter_map(|l| l.trim().strip_prefix("file:")).map(|f| f.trim()).collect();
    assert_eq!(files.len(), 4, "{c}");
    assert!(files.iter().any(|f| f.ends_with("05.01/PACK.md")), "{c}");
    for f in files {
        assert!(e.root.join(f).is_file(), "{f} does not exist: {c}");
    }
    assert!(e.root.join("pages").join(PG).join("05.md").is_file());
    for want in ["report:   pages/1.2.3.4/05.md section \"## 05.01\"", "record:   pages/1.2.3.4/05.md section \"## 05.01\"",
                 "open:     git -C game show", ":.workshop/returns/1.2.3.4.05.01.md", "close:      entry", "signoff:    entry", "links printed, not checked"] {
        assert!(c.contains(want), "missing {want}: {c}");
    }
    let open = e.ok(&["board", PG, "--card", "05.01"]);
    assert_eq!(open, c, "--card 05.01 and --card 01 are the same card");
    for card in [c, Env::ready("board-card-draft").card_of_a_draft()] {
        for l in card.lines() {
            assert!(names_source(l), "card line names no path, command or log entry: {l}\n{card}");
        }
    }
}

/// A card line names a path (pages/...), a command (git -C, wf ...) or a log entry number.
fn names_source(l: &str) -> bool {
    let entry = ["entry ", "entries "].iter().any(|w| l.match_indices(w).any(|(i, _)| l[i + w.len()..].starts_with(|c: char| c.is_ascii_digit())));
    entry || l.contains("pages/") || l.contains("git -C ") || l.contains("wf ")
}

impl Env {
    fn card_of_a_draft(&self) -> String {
        self.draft_jobs("src/a.rs", "true", "w01: set a\nw02: set b");
        self.ok(&["board", PG, "--card", "1"])
    }
}

/// Write a log with a valid chain by hand (an old or foreign log the tool did not write).
/// `time` None leaves out time_s.
fn write_log(dir: &PathBuf, evs: &[(&str, serde_json::Value, Option<u64>)]) {
    use sha2::{Digest, Sha256};
    fs::create_dir_all(dir).unwrap();
    let (mut prev, mut text) = ("0".to_string(), String::new());
    for (i, (kind, data, time)) in evs.iter().enumerate() {
        let mut v = serde_json::json!({"seq": i + 1, "actor": "pri", "role": "prime", "kind": kind, "data": data, "prev": prev});
        if let Some(t) = time {
            v["time_s"] = serde_json::json!(t);
        }
        if kind.is_empty() {
            v.as_object_mut().unwrap().remove("kind");
        }
        let line = v.to_string();
        prev = Sha256::digest(line.as_bytes()).iter().map(|b| format!("{b:02x}")).collect();
        text += &line;
        text.push('\n');
    }
    fs::write(dir.join("log.jsonl"), text).unwrap();
}

fn init_data(addr: &str) -> serde_json::Value {
    serde_json::json!({"address": addr, "title": "foreign", "person": "mat", "prime": "pri", "grant": ["src/"], "grant_ref": "t1"})
}

/// Must-fix 1: an entry for a never-drafted pass is an error, not a panic, everywhere.
#[test]
fn entry_for_a_missing_pass_is_unreadable_not_a_panic() {
    let e = Env::ready("board-nopass");
    let bad = e.root.join("pages/1.2.3.8");
    write_log(&bad, &[("init", init_data("1.2.3.8"), Some(1)), ("claim", serde_json::json!({"pass": 3}), Some(2)),
                      ("close", serde_json::json!({"pass": 3, "outcome": "passed"}), Some(3))]);
    let bin = env!("CARGO_BIN_EXE_wf");
    for args in [vec!["board", "1.2.3.8"], vec!["board", "1.2.3.8", "--card", "3"], vec!["status", "1.2.3.8"], vec!["observe", "1.2.3.8"], vec!["verify", "1.2.3.8"]] {
        let o = Command::new(bin).env("WF_ROOT", &e.root).args(&args).output().unwrap();
        let err = String::from_utf8_lossy(&o.stderr);
        assert_eq!(o.status.code(), Some(1), "{args:?} must refuse, not panic: {err}");
        assert!(err.contains("log entry 2 is out of order: a claim for 05.03, which was never drafted; the page cannot be read"), "{args:?}: {err}");
        assert!(!err.contains("panicked"), "{args:?}: {err}");
    }
    let b = e.ok(&["board"]);
    assert!(b.contains("  1.2.3.8  unreadable: log entry 2 is out of order: a claim for 05.03, which was never drafted"), "{b}");
    assert!(b.contains("  1.2.3.4  t  entries 4"), "the other page still shows: {b}");
}

/// Also-fix 4 and 7: no time_s reads as unknown age and never stale; an empty log is unreadable.
#[test]
fn board_handles_a_log_without_times_and_an_empty_log() {
    let e = Env::ready("board-notime");
    let dir = e.root.join("pages/1.2.3.9");
    write_log(&dir, &[("init", init_data("1.2.3.9"), None), ("draft", serde_json::json!({"pass": 1, "fields": {"outcome": "o"}, "pins": {}}), None),
                      ("pack", serde_json::json!({"pass": 1, "pack_text": "p", "pack_hash": "h", "templates": "2", "sources": {}}), None),
                      ("claim", serde_json::json!({"pass": 1}), None)]);
    let far = 4_000_000_000u64;
    let (ok, b) = e.wf_at(&["board", "1.2.3.9", "--stall-hours", "0"], Some(far));
    assert!(ok, "{b}");
    assert!(b.contains("age unknown (no time in the log)") && b.contains("last entry unknown (no time in the log)"), "{b}");
    assert!(!b.contains("STALE") && !b.contains("stalled") && !b.contains("h |"), "{b}");
    let (ok, c) = e.wf_at(&["board", "1.2.3.9", "--card", "1"], Some(far));
    assert!(ok && c.contains("age:        unknown (no time in the log) since entry 4"), "{c}");
    let (_, ob) = e.wf_at(&["observe", "1.2.3.9", "--stall-hours", "0"], Some(far));
    assert!(!ob.contains("stalled"), "{ob}");
    let empty = e.root.join("pages/1.2.3.7");
    fs::create_dir_all(&empty).unwrap();
    fs::write(empty.join("log.jsonl"), "").unwrap();
    e.no(&["board", "1.2.3.7"], "page 1.2.3.7 is unreadable: the log is empty (no init entry)");
    let book = e.ok(&["board"]);
    assert!(book.contains("  1.2.3.7  unreadable: the log is empty (no init entry)"), "{book}");
    assert!(!book.lines().any(|l| l.starts_with("    ") || l.starts_with("   (")), "{book}");
}

/// Also-fix 6: unknown flags and extra arguments are refused; the book board refuses --card.
#[test]
fn board_refuses_unknown_flags_and_extra_arguments() {
    let e = Env::ready("board-flags");
    let before = sha_map(&e.page());
    e.no(&["board", PG, "--as", "pri"], "wf board takes only --all, --card NN and --stall-hours H, not --as");
    e.no(&["board", PG, "--cards", "1"], "not --cards");
    e.no(&["board", PG, "1"], "at most one page, got 2 arguments");
    e.no(&["board", "--card", "1"], "the book board has no cards");
    e.no(&["board", "--all", PG], "--all takes no value");
    e.no(&["board", PG, "--card", "05.x"], "--card needs a pass number like 4, 04 or 05.04");
    assert_eq!(sha_map(&e.page()), before);
}

#[test]
fn book_board_lists_pages_and_shows_an_unreadable_one() {
    let e = Env::ready("board-book");
    e.ok(&["init-page", "1.2.3.5", "--title", "second", "--person", "mat", "--prime", "pri", "--grant", "src/", "--grant-ref", "t1", "--as", "mat"]);
    fs::create_dir_all(e.root.join("pages/1.2.3.6")).unwrap();
    fs::write(e.root.join("pages/1.2.3.6/log.jsonl"), "not json\n{}\n").unwrap();
    fs::create_dir_all(e.root.join("pages/1.2.3.7")).unwrap();
    let (ok, b) = e.wf(&["board"]);
    assert!(ok, "{b}");
    assert!(b.contains("BOOK BOARD  4 pages under"), "{b}");
    assert!(b.contains("  1.2.3.4  t  entries 4"), "{b}");
    assert!(b.contains("  1.2.3.5  second  entries 1"), "{b}");
    assert!(b.contains("  1.2.3.6  unreadable: log line 1 is not JSON"), "{b}");
    assert!(b.contains("  1.2.3.7  unreadable: no log.jsonl"), "{b}");
}

/// Tests 11 and 12: copies of the three real pages print, every hash stays the same,
/// and the default 90.10 board is 40 lines or fewer.
#[test]
fn board_on_real_pages_is_read_only_and_short() {
    let Some(src) = real_pages_dir() else {
        eprintln!("skipping board_on_real_pages_is_read_only_and_short: real pages not found at ../pages or /workspace/workshop-build/wf-run/pages");
        return;
    };
    let root = std::env::temp_dir().join(format!("wf-test-{}-board-real", std::process::id()));
    let _ = fs::remove_dir_all(&root);
    let addrs = ["90.10.00.0001", "90.20.00.0001", "90.30.00.0001"];
    for addr in addrs {
        copy_dir(&src.join(addr), &root.join("pages").join(addr));
    }
    let before = sha_map(&root.join("pages"));
    let bin = env!("CARGO_BIN_EXE_wf");
    let run = |args: &[&str]| {
        let o = Command::new(bin).env("WF_ROOT", &root).args(args).output().unwrap();
        let out = format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr));
        assert!(o.status.success(), "{args:?}: {out}");
        out
    };
    for addr in addrs {
        let b = run(&["board", addr]);
        assert!(b.starts_with(&format!("BOARD  page {addr}")), "{b}");
        assert!(!b.contains("VIEWS"), "{addr}: {b}");
        run(&["board", addr, "--all"]);
        let card = run(&["board", addr, "--card", "05.01"]);
        assert!(card.lines().all(names_source), "{addr}: {card}");
    }
    let short = run(&["board", "90.10.00.0001"]);
    assert!(short.lines().count() <= 40, "{} lines: {short}", short.lines().count());
    assert!(run(&["board"]).contains("BOOK BOARD  3 pages"));
    assert_eq!(sha_map(&root.join("pages")), before, "the board changed a real page file");
    let _ = fs::remove_dir_all(&root);
}

// ---- log hardening: forged or wrong-order entries ----

/// One pass's entries for a hand-written log, by kind: (kind, data, time).
fn ev(kind: &'static str, nn: u64) -> (&'static str, serde_json::Value, Option<u64>) {
    let d = match kind {
        "draft" => serde_json::json!({"pass": nn, "fields": {"outcome": "o", "repo": "game", "start": "main", "w01": "x", "may touch": "src/a.rs", "checks": "true", "stop if": "none"}, "pins": {}}),
        "pack" => serde_json::json!({"pass": nn, "pack_text": "p", "pack_hash": "h", "branch": "b", "return_file": "f", "start": "0", "templates": "2", "sources": {}}),
        "return" => serde_json::json!({"pass": nn, "commit": "c", "file": "f", "hash": "h", "jobs": {"w01": "done - x"}}),
        "check" => serde_json::json!({"pass": nn, "commit": "c", "verdict": "pass", "report": ""}),
        "signoff" => serde_json::json!({"pass": nn, "outcome": "passed", "cards": {}, "note": "none"}),
        "close" => serde_json::json!({"pass": nn, "outcome": "passed"}),
        "halt" | "resume" => serde_json::json!({"note": "why (t1)"}),
        _ => serde_json::json!({"pass": nn}),
    };
    (kind, d, Some(1_795_456_800))
}

fn forged(e: &Env, addr: &str, kinds: &[(&'static str, u64)]) -> PathBuf {
    let dir = e.root.join("pages").join(addr);
    let mut evs = vec![("init", init_data(addr), Some(1_795_456_800))];
    evs.extend(kinds.iter().map(|(k, n)| ev(k, *n)));
    write_log(&dir, &evs);
    dir
}

fn run_code(e: &Env, args: &[&str]) -> (Option<i32>, String) {
    let o = Command::new(env!("CARGO_BIN_EXE_wf")).env("WF_ROOT", &e.root).args(args).output().unwrap();
    (o.status.code(), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)))
}

/// Item 1: write commands on forged wrong-state logs refuse with exit 1, leave the log as it was and no lock.
#[test]
fn write_commands_on_forged_logs_refuse_without_a_panic() {
    let e = Env::ready("forged-writes");
    let cases: [(&str, &[(&'static str, u64)], Vec<&str>); 4] = [
        ("9.0.0.1", &[("draft", 1), ("claim", 1)], vec!["return", "9.0.0.1", "1", "--branch", "b", "--commit", "c", "--file", "f", "--as", "pri"]),
        ("9.0.0.2", &[("draft", 1), ("claim", 1), ("return", 1)], vec!["check", "9.0.0.2", "1", "--as", "cat"]),
        ("9.0.0.3", &[("draft", 1), ("check", 1)], vec!["signoff", "9.0.0.3", "1", "--outcome", "failed", "--as", "pri"]),
        ("9.0.0.4", &[("draft", 1), ("signoff", 1), ("close", 1)], vec!["close", "9.0.0.4", "1", "--as", "pri"]),
    ];
    for (addr, kinds, args) in cases {
        let dir = forged(&e, addr, kinds);
        let before = fs::read(dir.join("log.jsonl")).unwrap();
        let (code, out) = run_code(&e, &args);
        assert_eq!(code, Some(1), "{args:?}: {out}");
        assert!(out.contains("is out of order") && out.contains("the page cannot be read") && !out.contains("panicked"), "{args:?}: {out}");
        assert_eq!(fs::read(dir.join("log.jsonl")).unwrap(), before, "{args:?} changed the log");
        assert!(!dir.join(".wf-lock").exists(), "{args:?} left a lock");
    }
}

/// Item 2: wrong-order entries make the page unreadable, with the entry and the reason.
#[test]
fn wrong_order_entries_make_the_page_unreadable() {
    let e = Env::ready("order");
    let full: &[(&'static str, u64)] = &[("draft", 1), ("pack", 1), ("claim", 1), ("return", 1), ("check", 1), ("signoff", 1), ("close", 1)];
    let mut after_close = full.to_vec();
    after_close.push(("claim", 1));
    let mut redraft = full.to_vec();
    redraft.push(("draft", 1));
    let cases: Vec<(&str, Vec<(&'static str, u64)>, &str)> = vec![
        ("8.0.0.1", vec![("draft", 1), ("pack", 1), ("claim", 1), ("close", 1)], "log entry 5 is out of order: a close for 05.01, which is at 'open'; a close needs review"),
        ("8.0.0.2", vec![("draft", 1), ("pack", 1), ("claim", 1), ("check", 1)], "log entry 5 is out of order: a check for 05.01, which is at 'open'; a check needs return or review"),
        ("8.0.0.3", after_close, "log entry 9 is out of order: a claim for 05.01, which is at 'closed'; a claim needs pack"),
        ("8.0.0.4", redraft, "log entry 9 is out of order: a re-draft for 05.01, which is at 'closed'; a draft needs draft"),
        ("8.0.0.5", vec![("draft", 1), ("", 1)], "log entry 3 is out of order: the entry has no kind"),
        ("8.0.0.6", vec![("draft", 1), ("teleport", 1)], "log entry 3 is out of order: 'teleport' is not a wf entry kind"),
        ("8.0.0.7", vec![("init", 1)], "log entry 2 is out of order: a second init: only entry 1 starts the page"),
        ("8.0.0.8", vec![("draft", 1), ("pack", 1), ("claim", 1), ("return", 1), ("check", 1), ("close", 1)], "log entry 7 is out of order: a close for 05.01 with no signoff"),
        ("8.0.0.9", vec![("halt", 0), ("halt", 0)], "log entry 3 is out of order: a halt while the page is already halted"),
        ("8.0.1.0", vec![("resume", 0)], "log entry 2 is out of order: a resume while the page is not halted"),
        ("8.0.1.1", vec![("halt", 0), ("draft", 1)], "log entry 3 is out of order: a draft for 05.01 while the page is halted"),
    ];
    for (addr, kinds, want) in &cases {
        let mut evs = vec![("init", init_data(addr), Some(1_795_456_800))];
        evs.extend(kinds.iter().map(|(k, n)| if *k == "init" { ("init", init_data(addr), Some(1)) } else { ev(k, *n) }));
        write_log(&e.root.join("pages").join(addr), &evs);
        for cmd in ["verify", "status", "board"] {
            let (code, out) = run_code(&e, &[cmd, addr]);
            assert_eq!(code, Some(1), "{cmd} {addr}: {out}");
            assert!(out.contains(want), "{cmd} {addr}: want '{want}' in {out}");
        }
    }
    // A log whose first entry is not the init.
    let dir = e.root.join("pages/8.0.2.0");
    write_log(&dir, &[ev("draft", 1)]);
    let (code, out) = run_code(&e, &["verify", "8.0.2.0"]);
    assert!(code == Some(1) && out.contains("log entry 1 is out of order: the first entry is a draft, not the init"), "{out}");
    let book = e.ok(&["board"]);
    assert!(book.contains("  8.0.0.1  unreadable: log entry 5 is out of order") && book.contains("  1.2.3.4  t  entries 4"), "{book}");
    // The full chain itself loads.
    forged(&e, "8.1.0.0", full);
    let (code, out) = run_code(&e, &["status", "8.1.0.0"]);
    assert_eq!(code, Some(0), "{out}");
}

/// Item 3: pass numbers outside 01-98 are refused, never wrapped (4294967297 is not pass 1).
#[test]
fn pass_numbers_outside_01_98_are_refused_not_wrapped() {
    let e = Env::ready("wrap");
    for (addr, n) in [("7.0.0.1", 4_294_967_297u64), ("7.0.0.2", 0), ("7.0.0.3", 99)] {
        forged(&e, addr, &[("draft", n)]);
        let (code, out) = run_code(&e, &["status", addr]);
        assert_eq!(code, Some(1), "{out}");
        assert!(out.contains(&format!("log entry 2 is out of order: a draft for pass {n}, outside 01-98 (R9)")), "{out}");
    }
    let dir = forged(&e, "7.0.0.4", &[("draft", 1)]);
    let mut evs = vec![("init", init_data("7.0.0.4"), Some(1)), ev("draft", 1), ev("pack", 4_294_967_297)];
    evs[2].1["pass"] = serde_json::json!(4_294_967_297u64);
    write_log(&dir, &evs);
    let (code, out) = run_code(&e, &["board", "7.0.0.4"]);
    assert!(code == Some(1) && out.contains("a pack for pass 4294967297, outside 01-98 (R9)"), "{out}");
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let before = e.log();
    let err = p.add("pri", "prime", "draft", serde_json::json!({"pass": 4_294_967_297u64, "fields": {}, "pins": {}})).unwrap_err();
    assert!(err.contains("outside 01-98 (R9)"), "{err}");
    assert_eq!(e.log(), before);
    e.no(&["claim", PG, "4294967297", "--as", "bob"], "give the pass number");
}

/// Item 4: a refused write through the tool's append says the write is refused and why.
#[test]
fn refused_append_says_nothing_was_written_and_why() {
    let e = Env::ready("append-guard");
    let before = e.log();
    let mut p = wf::page::Page::load(&e.page()).unwrap();
    let err = p.add("bob", "builder", "claim", serde_json::json!({"pass": 5})).unwrap_err();
    assert_eq!(err, "refused, nothing written: a claim for 05.05, which was never drafted");
    let err = p.add("mat", "person", "init", serde_json::json!({"address": PG})).unwrap_err();
    assert_eq!(err, "refused, nothing written: a second init: only entry 1 starts the page");
    assert_eq!(e.log(), before);
    assert!(!err.contains("cannot be read"));
    assert!(e.ok(&["verify", PG]).contains("ok: log chain holds"));
}

/// Item 5: --card with --all is refused; a bad typed address is shown escaped.
#[test]
fn board_card_with_all_is_refused_and_bad_addresses_are_escaped() {
    let e = Env::checked("item5");
    e.no(&["board", PG, "--card", "1", "--all"], "give one of them");
    e.no(&["board", PG, "--all", "--card", "1"], "give one of them");
    for cmd in ["status", "board", "verify"] {
        let (ok, out) = e.wf(&[cmd, "a\u{1b}[2Kb\u{202e}"]);
        assert!(!ok, "{out}");
        assert!(!out.contains('\u{1b}') && !out.contains('\u{202e}'), "{cmd}: raw char in {out}");
        assert!(out.contains("bad page address 'a\\u{1b}[2Kb\\u{202e}'"), "{cmd}: {out}");
    }
}
