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
    if ok { Ok(()) } else { Err(format!("bad page address '{a}': use letters, digits, dots, - or _")) }
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
const NEEDS_PASS: [&str; 7] = ["pack", "claim", "return-refused", "return", "check", "signoff", "close"];

fn missing_pass(seq: u64, kind: &str, nn: u32) -> String {
    format!("log entry {seq} is a {kind} for pass {nn}, which was never drafted; the log cannot be read")
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
        let nn = data["pass"].as_u64().unwrap_or(0) as u32;
        if NEEDS_PASS.contains(&kind) && !self.passes.contains_key(&nn) {
            return Err(missing_pass(seq, kind, nn));
        }
        let (e, head) = log::append(&self.log_path(), &self.head, seq, actor, role, kind, data)?;
        self.apply(&e)?;
        self.events.push(e);
        self.head = head;
        Ok(())
    }

    /// Fold one entry in. An entry for a pass that was never drafted is an error, not a panic.
    fn apply(&mut self, e: &Event) -> Res<()> {
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
