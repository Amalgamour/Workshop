//! A page: its state is folded from the log. Nothing here is stored except the log.

use crate::log::{self, sha, Event, Res};
use serde_json::{Map, Value};
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

pub const FACES: [&str; 9] = ["00", "01", "02", "03", "04", "05", "06", "07", "08"];

#[derive(Default, Clone)]
pub struct Face {
    pub version: u64,
    pub seq: u64,
    pub text: String,
}
impl Face {
    pub fn hash(&self) -> String {
        sha(&self.text)
    }
}

#[derive(Default, Clone)]
pub struct Pass {
    pub nn: u32,
    pub tail: String,
    pub fields: Map<String, Value>,
    pub pins: Value,
    pub pack: Option<Value>,
    pub claim: Option<String>,
    pub ret: Option<Value>,
    pub refusals: Vec<(u64, String)>,
    pub check: Option<(String, Value)>,
    pub signoff: Option<(String, u64, Value)>,
    pub close: Option<Value>,
    pub last_seq: u64,
}

#[derive(Clone)]
pub struct Elev {
    pub seq: u64,
    pub pass: u32,
    pub to: String,
    pub by: String,
    pub item: String,
    pub answer: Option<String>,
}

#[derive(Default)]
pub struct Page {
    pub dir: PathBuf,
    pub events: Vec<Event>,
    pub head: String,
    pub addr: String,
    pub title: String,
    pub person: String,
    pub prime: String,
    /// (name, from seq, to seq)
    pub primes: Vec<(String, u64, u64)>,
    pub grant: Vec<String>,
    pub grant_refs: Vec<String>,
    pub faces: BTreeMap<String, Face>,
    pub passes: BTreeMap<u32, Pass>,
    pub elevs: Vec<Elev>,
    pub findings: Vec<(u64, String, String)>,
    /// Set by a halt entry, cleared by resume: (who, time, note, entry).
    pub halt: Option<(String, u64, String, u64)>,
}

pub fn s(v: &Value, k: &str) -> String {
    v[k].as_str().unwrap_or("").to_string()
}

pub fn list(v: &Value) -> Vec<String> {
    v.as_array().map(|a| a.iter().filter_map(|x| x.as_str().map(String::from)).collect()).unwrap_or_default()
}

pub fn split_list(s: &str) -> Vec<String> {
    s.split([',', ';']).map(|x| x.trim().to_string()).filter(|x| !x.is_empty()).collect()
}

/// `path` is inside `scope` if it equals an entry, or sits under an entry that ends in `/`.
pub fn inside(path: &str, scope: &[String]) -> bool {
    scope.iter().any(|g| g == path || (g.ends_with('/') && path.starts_with(g.as_str())))
}

/// Same file, or one is a folder prefix of the other (`src/` vs `src/a.rs`).
pub fn paths_overlap(a: &str, b: &str) -> bool {
    let a = a.trim_end_matches('/');
    let b = b.trim_end_matches('/');
    a == b || a.starts_with(&format!("{b}/")) || b.starts_with(&format!("{a}/"))
}

pub fn check_addr(a: &str) -> Res<()> {
    let ok = !a.is_empty() && !a.contains("..") && a.chars().all(|c| c.is_ascii_alphanumeric() || ".-_".contains(c));
    if ok { Ok(()) } else { Err(format!("bad page address '{}': use letters, digits, dots, - or _", crate::chars::escape_line(a))) }
}

/// Text from "done when:" (any case) to the end of each line that has it, joined; or "none".
pub fn done_when_lines(text: &str) -> String {
    const NEEDLE: &str = "done when:";
    let mut found = Vec::new();
    for line in text.lines() {
        let lower = line.to_lowercase();
        if let Some(pos) = lower.find(NEEDLE) {
            let start = lower[..pos].chars().count();
            let byte = line.char_indices().nth(start).map(|(i, _)| i).unwrap_or(line.len());
            found.push(&line[byte..]);
        }
    }
    if found.is_empty() { "none".into() } else { found.join("\n") }
}

/// If face 01 no longer matches the pack's pinned source, `Some("vN entry E")`.
pub fn face01_drift(p: &Page, pack: &Value) -> Option<String> {
    let now = p.faces.get("01").map(|g| format!("v{} entry {}", g.version, g.seq)).unwrap_or_default();
    if now.is_empty() || s(&pack["sources"], "01").starts_with(&now) {
        None
    } else {
        Some(now)
    }
}

/// Entry kinds that only make sense for a pass that was drafted first.
/// Every entry kind wf writes. Anything else in a log is refused.
const KINDS: [&str; 17] = ["init", "prime", "grant", "face", "draft", "pack", "claim", "return-refused", "return",
    "check", "signoff", "close", "elevate", "answer", "finding", "halt", "resume"];

/// Kinds that belong to one pass (data.pass, 01-98).
const PASS_KINDS: [&str; 9] = ["draft", "pack", "claim", "return-refused", "return", "check", "signoff", "close", "elevate"];

/// A full git commit hash as wf writes it: 40 (SHA-1 repo) or 64 (SHA-256 repo)
/// lowercase hex characters. One rule for return and check entries.
pub fn is_full_hash(c: &str) -> bool {
    (c.len() == 40 || c.len() == 64) && c.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

fn commit_rule(kind: &str, nn: u32, d: &Value) -> Res<()> {
    if d["commit"].as_str().is_some_and(is_full_hash) {
        Ok(())
    } else {
        Err(format!("a {kind} for 05.{nn:02} whose commit is not a 40- or 64-character lowercase hex hash"))
    }
}

fn missing_pass(seq: u64, kind: &str, nn: u32) -> String {
    format!("log entry {seq} is a {kind} for 05.{nn:02}, which was never drafted")
}

impl Pass {
    /// Pack, open (claimed), return, and review all hold the pack's files.
    pub fn is_open_tail(&self) -> bool {
        matches!(self.tail.as_str(), "pack" | "open" | "return" | "review")
    }
}

impl Page {
    pub fn log_path(&self) -> PathBuf {
        self.dir.join("log.jsonl")
    }

    pub fn load(dir: &Path) -> Res<Page> {
        let (events, head) = log::read(&dir.join("log.jsonl"))?;
        let mut p = Page { dir: dir.to_path_buf(), head, ..Default::default() };
        for e in &events {
            p.apply(e)?;
        }
        p.events = events;
        Ok(p)
    }

    pub fn pass(&self, nn: u32) -> Res<&Pass> {
        self.passes.get(&nn).ok_or_else(|| {
            if (1..=98).contains(&nn) {
                format!("no pass 05.{nn:02} on this page")
            } else {
                format!("no pass {nn} on this page")
            }
        })
    }

    /// The newest closed pass, if any.
    pub fn last_closed(&self) -> Option<&Pass> {
        self.passes.values().filter(|p| p.tail == "closed").max_by_key(|p| p.last_seq)
    }

    /// Who was Prime just after log entry `seq`.
    pub fn prime_at(&self, seq: u64) -> String {
        self.primes.iter().find(|(_, a, b)| *a <= seq && seq <= *b).map(|x| x.0.clone()).unwrap_or_default()
    }

    /// Append one event to the log and fold it in.
    pub fn add(&mut self, actor: &str, role: &str, kind: &str, data: Value) -> Res<()> {
        let seq = self.events.len() as u64 + 1;
        self.order(seq, kind, &data).map_err(|why| format!("refused, nothing written: {why}"))?;
        let (e, head) = log::append(&self.log_path(), &self.head, seq, actor, role, kind, data)?;
        self.apply(&e)?;
        self.events.push(e);
        self.head = head;
        Ok(())
    }

    /// Why an entry of `kind` with `d` cannot come next on this page, or Ok.
    /// The same state order the commands keep: draft, pack, claim, return, check, signoff, close.
    pub fn order(&self, seq: u64, kind: &str, d: &Value) -> Res<()> {
        if !KINDS.contains(&kind) {
            return Err(if kind.is_empty() { "the entry has no kind".into() } else { format!("'{}' is not a wf entry kind", crate::chars::escape_line(kind)) });
        }
        if kind == "init" && seq != 1 {
            return Err("a second init: only entry 1 starts the page".into());
        }
        if kind != "init" && seq == 1 {
            return Err(format!("the first entry is a {kind}, not the init"));
        }
        match kind {
            "halt" if self.halt.is_some() => return Err("a halt while the page is already halted".into()),
            "halt" => {
                if let Some(x) = self.passes.values().find(|x| x.is_open_tail()) {
                    return Err(format!("a halt while 05.{:02} is at '{}'", x.nn, x.tail));
                }
            }
            "resume" if self.halt.is_none() => return Err("a resume while the page is not halted".into()),
            _ => {}
        }
        if !PASS_KINDS.contains(&kind) {
            return Ok(());
        }
        let nn = match d["pass"].as_u64() {
            Some(n) if (1..=98).contains(&n) => n as u32,
            Some(n) => return Err(format!("a {kind} for pass {n}, outside 01-98 (R9)")),
            None => return Err(format!("a {kind} with no pass number")),
        };
        if matches!(kind, "draft" | "pack" | "claim") && self.halt.is_some() {
            return Err(format!("a {kind} for 05.{nn:02} while the page is halted"));
        }
        let Some(x) = self.passes.get(&nn) else {
            return if kind == "draft" { Ok(()) } else { Err(format!("a {kind} for 05.{nn:02}, which was never drafted")) };
        };
        let want: &[&str] = match kind {
            "draft" | "pack" => &["draft"],
            "claim" => &["pack"],
            "return-refused" | "return" => &["open"],
            "check" => &["return", "review"],
            "signoff" | "close" => &["review"],
            _ => return Ok(()), // elevate: any drafted pass
        };
        if !want.contains(&x.tail.as_str()) {
            let what = if kind == "draft" && x.tail == "closed" { "a re-draft".to_string() } else { format!("a {kind}") };
            return Err(format!("{what} for 05.{nn:02}, which is at '{}'; a {kind} needs {}", x.tail, want.join(" or ")));
        }
        if kind == "check" {
            match d.get("verdict") {
                None | Some(Value::Null) => return Err(format!("a check for 05.{nn:02} with no verdict")),
                Some(v) if !matches!(v.as_str(), Some("pass" | "fail")) => {
                    return Err(format!("a check for 05.{nn:02} with a verdict that is not pass or fail"))
                }
                _ => {}
            }
            commit_rule(kind, nn, d)?;
            // Same as wf check: a re-check only after a failed check, and never after a signoff.
            if let Some((_, c)) = &x.check {
                if s(c, "verdict") != "fail" {
                    return Err(format!("a re-check of 05.{nn:02}, whose last check passed"));
                }
            }
            if x.signoff.is_some() {
                return Err(format!("a check of 05.{nn:02} after its signoff"));
            }
        }
        // A refused return keeps the raw attempt as evidence (axiom 6), so its commit is not checked.
        if kind == "return" {
            commit_rule(kind, nn, d)?;
        }
        if kind == "signoff" && !d["outcome"].as_str().is_some_and(|o| crate::cmd::OUTCOMES.contains(&o)) {
            return Err(format!("a signoff for 05.{nn:02} whose outcome is not {}", crate::cmd::OUTCOMES.join(", ")));
        }
        if kind == "close" && x.signoff.is_none() {
            return Err(format!("a close for 05.{nn:02} with no signoff"));
        }
        Ok(())
    }

    /// Fold one entry in. An entry for a pass that was never drafted is an error, not a panic.
    fn apply(&mut self, e: &Event) -> Res<()> {
        self.order(e.seq, &e.kind, &e.data).map_err(|why| format!("log entry {} is out of order: {why}; the page cannot be read", e.seq))?;
        let d = &e.data;
        let nn = d["pass"].as_u64().unwrap_or(0) as u32;
        let missing = || missing_pass(e.seq, &e.kind, nn);
        match e.kind.as_str() {
            "init" => {
                self.addr = s(d, "address");
                self.title = s(d, "title");
                self.person = s(d, "person");
                self.grant = list(&d["grant"]);
                self.grant_refs.push(s(d, "grant_ref"));
                self.set_prime(&s(d, "prime"), e.seq);
            }
            "prime" => self.set_prime(&s(d, "name"), e.seq),
            "grant" => {
                for g in list(&d["paths"]) {
                    if !self.grant.contains(&g) {
                        self.grant.push(g);
                    }
                }
                self.grant_refs.push(s(d, "ref"));
            }
            "face" => {
                let f = self.faces.entry(s(d, "face")).or_default();
                f.version += 1;
                f.seq = e.seq;
                if s(d, "mode") == "append" {
                    f.text.push_str(&format!("- [{}] {} ({}, entry {})\n", s(d, "section"), s(d, "text").trim(), e.actor, e.seq));
                } else {
                    f.text = s(d, "text");
                }
            }
            "draft" => {
                let p = self.passes.entry(nn).or_default();
                p.nn = nn;
                p.tail = "draft".into();
                p.fields = d["fields"].as_object().cloned().unwrap_or_default();
                p.pins = d["pins"].clone();
            }
            "pack" => {
                let p = self.passes.get_mut(&nn).ok_or_else(missing)?;
                p.tail = "pack".into();
                p.pack = Some(d.clone());
            }
            "claim" => {
                let p = self.passes.get_mut(&nn).ok_or_else(missing)?;
                p.tail = "open".into();
                p.claim = Some(e.actor.clone());
            }
            "return-refused" => self.passes.get_mut(&nn).ok_or_else(missing)?.refusals.push((e.seq, s(d, "why"))),
            "return" => {
                let p = self.passes.get_mut(&nn).ok_or_else(missing)?;
                p.tail = "return".into();
                p.ret = Some(d.clone());
            }
            "check" => {
                let p = self.passes.get_mut(&nn).ok_or_else(missing)?;
                p.tail = "review".into();
                p.check = Some((e.actor.clone(), d.clone()));
            }
            "signoff" => self.passes.get_mut(&nn).ok_or_else(missing)?.signoff = Some((e.actor.clone(), e.seq, d.clone())),
            "close" => {
                let p = self.passes.get_mut(&nn).ok_or_else(missing)?;
                p.tail = "closed".into();
                p.close = Some(d.clone());
            }
            "elevate" => self.elevs.push(Elev { seq: e.seq, pass: nn, to: s(d, "to"), by: e.actor.clone(), item: s(d, "item"), answer: None }),
            "answer" => {
                let at = d["elevation"].as_u64().unwrap_or(0);
                if let Some(x) = self.elevs.iter_mut().find(|x| x.seq == at) {
                    x.answer = Some(format!("{} (by {}, entry {})", s(d, "text"), e.actor, e.seq));
                }
            }
            "finding" => self.findings.push((e.seq, e.actor.clone(), s(d, "text"))),
            "halt" => self.halt = Some((e.actor.clone(), e.time, s(d, "note"), e.seq)),
            "resume" => self.halt = None,
            _ => {}
        }
        if let Some(p) = self.passes.get_mut(&nn) {
            if nn > 0 {
                p.last_seq = e.seq;
            }
        }
        if let Some(last) = self.primes.last_mut() {
            last.2 = e.seq;
        }
        Ok(())
    }

    fn set_prime(&mut self, name: &str, seq: u64) {
        if let Some(last) = self.primes.last_mut() {
            last.2 = seq - 1;
        }
        self.primes.push((name.to_string(), seq, seq));
        self.prime = name.to_string();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn inside_scope() {
        let g = vec!["src/".to_string(), "tests/steer.rs".to_string()];
        assert!(inside("src/a/b.rs", &g) && inside("tests/steer.rs", &g));
        assert!(!inside("tests/other.rs", &g) && !inside("srcx/a.rs", &g));
    }

    #[test]
    fn paths_overlap_file_and_folder() {
        assert!(paths_overlap("src/a.rs", "src/a.rs"));
        assert!(paths_overlap("src/", "src/a.rs") && paths_overlap("src/a.rs", "src/"));
        assert!(paths_overlap("src", "src/a.rs"));
        assert!(!paths_overlap("src/foo", "src/foobar"));
        assert!(!paths_overlap("src/a.rs", "src/b.rs") && !paths_overlap("src/", "tests/"));
    }

    #[test]
    fn open_tails_hold_files() {
        for (tail, hold) in [("pack", true), ("open", true), ("return", true), ("review", true), ("draft", false), ("closed", false)] {
            let x = Pass { tail: tail.into(), ..Default::default() };
            assert_eq!(x.is_open_tail(), hold, "{tail}");
        }
    }

    #[test]
    fn done_when_lines_reads_face_01() {
        assert_eq!(done_when_lines("Goal: a.\nDone when: checks pass.\n"), "Done when: checks pass.");
        assert_eq!(done_when_lines("Goal: a.\n"), "none");
        // This page's real one-line face 01: "Done when:" sits mid-line, not at the start.
        let real = "Goal: the workflow kit (wf) any model can pull and run. MVP: every step of a pass runs through wf; refusals hold; README and AGENTS.md are enough for a fresh model. Done when: cargo test passes and the new behaviour has a test. Source: t267u, t268u, t270u.";
        assert_eq!(
            done_when_lines(real),
            "Done when: cargo test passes and the new behaviour has a test. Source: t267u, t268u, t270u."
        );
        assert_eq!(done_when_lines("GOAL and then DONE WHEN: Yes."), "DONE WHEN: Yes.");
    }

    #[test]
    fn face01_drift_compares_pack_source_to_current_face() {
        let mut p = Page::default();
        p.faces.insert("01".into(), Face { version: 2, seq: 9, text: "Goal: a.".into() });
        let same = serde_json::json!({"sources": {"01": "v2 entry 9 hash abc"}});
        let older = serde_json::json!({"sources": {"01": "v1 entry 3 hash def"}});
        assert_eq!(face01_drift(&p, &same), None);
        assert_eq!(face01_drift(&p, &older).as_deref(), Some("v2 entry 9"));
    }
}
