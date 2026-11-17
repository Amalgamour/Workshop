//! End-to-end tests: each one runs the wf binary against a temp folder and a temp git repo.

use std::fs;
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
        let f = self.root.join("pack.txt");
        fs::write(&f, format!("repo: game\nstart: main\noutcome: a = 2\nw01: set a to 2\nmay touch: {may}\nchecks: {checks}\nstop if: b must change\n")).unwrap();
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
    let pack = fs::read_to_string(e.page().join("05.01/PACK.md")).unwrap();
    assert!(pack.contains("face 04:        entry 2") && pack.contains("last closed 05: none"));
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
    e.ok(&["pack", PG, "2", "--overlap-ok", "1", "--as", "pri"]);
    assert!(e.log().contains("\"overlap_ok\":1"), "{}", e.log());
    e.draft("src/a.rs", "true");
    e.no(&["pack", PG, "3", "--overlap-ok", "1", "--as", "pri"], "overlaps open pass 05.02");
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
    e.ok(&["set-prime", PG, "neo", "--as", "mat"]);
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
    e.no(&["face-write", PG, "06", "--text", "x", "--as", "pri"], "hand-edited page files: 01.md");
    e.no(&["verify", PG], "hand-edited view files: 01.md");
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
    e.no(&["verify", PG], "hand-edited view files");
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
