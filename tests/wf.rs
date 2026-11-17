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
    assert!(agents.contains("docs/AXIOMS.md: hash ") && agents.contains("docs/DESIGN.md: hash "));
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
fn pack_refuses_overlapping_may_touch() {
    let e = Env::ready("ov-ref");
    e.open("src/a.rs", "true");
    e.draft("src/", "true");
    let (ok, out) = e.wf(&["pack", PG, "2", "--as", "pri"]);
    assert!(!ok, "{out}");
    assert!(out.contains("overlaps open pass 05.01") && out.contains("src/") && out.contains("src/a.rs"), "{out}");
}

#[test]
fn pack_allows_overlap_with_flag() {
    let e = Env::ready("ov-ok");
    e.open("src/a.rs", "true");
    e.draft("src/a.rs", "true");
    e.ok(&["pack", PG, "2", "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri"]);
    assert!(e.log().contains("\"overlap_ok\":1") && e.log().contains("shared files (t275u)"), "{}", e.log());
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "3", "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri"], "overlaps open pass 05.02");
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
    e.open("src/a.rs", "true");
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--as", "pri"], "missing --why");
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--why", "no ref", "--as", "pri"], "--why needs a reason and a (ref)");
    e.no(&["pack", PG, "2", "--overlap-ok", "1", "--why", "ok ( )", "--as", "pri"], "--why needs a reason and a (ref)");
    e.ok(&["pack", PG, "2", "--overlap-ok", "1", "--why", "shared files (t275u)", "--as", "pri"]);
    assert!(e.log().contains("\"overlap_why\":\"shared files (t275u)\""), "{}", e.log());
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
