//! Read a wf page log and compute benchmark measures 1-4 and 6-9.
//! Measures 5, 10 and 11 are marked manual.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Write as _;
use std::fs;
use std::path::Path;

use serde_json::Value;

#[derive(Debug, Clone)]
pub struct Entry {
    pub kind: String,
    pub seq: u64,
    pub time_s: i64,
    pub data: Value,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Measures {
    pub entries: usize,
    /// Fresh goals that passed, and fresh-goal count.
    pub first_try_passed: usize,
    pub fresh_goals: usize,
    pub signoffs: usize,
    /// Longest run of signoffs from a failed fresh goal through its last fix-up.
    pub longest_chain: usize,
    pub longest_from: Option<u64>,
    pub longest_to: Option<u64>,
    pub cards_carried: usize,
    pub cards_total: usize,
    pub carried_twice: bool,
    pub fails_by_commands: usize,
    pub fails_by_checker: usize,
    pub check_count: usize,
    pub merges_in_06: usize,
    pub pin_actions_in_06: usize,
    pub judgement_calls: Vec<String>,
    pub elevate: usize,
    pub questions_outside: BTreeSet<String>,
    pub observe: usize,
    pub observer_in_06: Vec<u64>,
    pub loops: usize,
    /// Pack→close, claim→return, return→check, in minutes (only complete pairs).
    pub pack_close: Vec<f64>,
    pub builder: Vec<f64>,
    pub checker: Vec<f64>,
    pub audit_notes: usize,
}

impl Default for Measures {
    fn default() -> Self {
        Self {
            entries: 0,
            first_try_passed: 0,
            fresh_goals: 0,
            signoffs: 0,
            longest_chain: 0,
            longest_from: None,
            longest_to: None,
            cards_carried: 0,
            cards_total: 0,
            carried_twice: false,
            fails_by_commands: 0,
            fails_by_checker: 0,
            check_count: 0,
            merges_in_06: 0,
            pin_actions_in_06: 0,
            judgement_calls: Vec::new(),
            elevate: 0,
            questions_outside: BTreeSet::new(),
            observe: 0,
            observer_in_06: Vec::new(),
            loops: 0,
            pack_close: Vec::new(),
            builder: Vec::new(),
            checker: Vec::new(),
            audit_notes: 0,
        }
    }
}

pub fn load_log(path: &Path) -> Result<Vec<Entry>, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("reading {}: {e}", path.display()))?;
    let mut out = Vec::new();
    for (i, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        let v: Value = serde_json::from_str(line)
            .map_err(|e| format!("{}:{}: {e}", path.display(), i + 1))?;
        out.push(Entry {
            kind: v
                .get("kind")
                .and_then(Value::as_str)
                .unwrap_or("")
                .to_string(),
            seq: v.get("seq").and_then(Value::as_u64).unwrap_or(0),
            time_s: v.get("time_s").and_then(Value::as_i64).unwrap_or(0),
            data: v.get("data").cloned().unwrap_or(Value::Null),
        });
    }
    Ok(out)
}

fn pass_of(e: &Entry) -> Option<u64> {
    if let Some(p) = e.data.get("pass").and_then(Value::as_u64) {
        return Some(p);
    }
    if e.kind == "pack" {
        if let Some(branch) = e.data.get("branch").and_then(Value::as_str) {
            // pass/<page>.05.NN
            return branch
                .rsplit('.')
                .next()
                .and_then(|s| s.parse::<u64>().ok());
        }
    }
    None
}

fn outcome(data: &Value) -> &str {
    data.get("outcome").and_then(Value::as_str).unwrap_or("")
}

fn face_of(data: &Value) -> String {
    match data.get("face") {
        Some(Value::String(s)) => s.clone(),
        Some(Value::Number(n)) => format!("{n}"),
        _ => String::new(),
    }
}

fn is_06(data: &Value) -> bool {
    matches!(face_of(data).as_str(), "6" | "06")
}

/// A completed merge reported in a 06 note, not a plan to merge later.
fn mentions_completed_merge(text: &str) -> bool {
    let t = text.to_ascii_lowercase();
    t.contains("merged by prime")
        || t.contains("merged and pushed")
        || t.contains("merged (")
}

/// Establishing or rebuilding the pinned tool, as written in a 06 note.
fn mentions_pin_action(text: &str) -> bool {
    let t = text.to_ascii_lowercase();
    t.contains("pin rebuilt") || t.contains("pin wf-bin rebuilt") || t.contains("pinned binary")
}

fn judgement_label(e: &Entry, text: &str) -> Option<String> {
    let t = text.to_ascii_lowercase();
    let kind = if t.contains("prime decision") {
        "prime decision"
    } else if t.contains("safer reading") {
        "safer reading"
    } else if t.contains("kept as is") {
        "kept as is"
    } else {
        return None;
    };
    if e.kind == "signoff" {
        if let Some(p) = pass_of(e) {
            return Some(format!("{kind} (signoff 05.{p:02})"));
        }
    }
    Some(format!("{kind} (06 entry {})", e.seq))
}

fn question_ids(text: &str) -> BTreeSet<String> {
    // Q-SA, Q63, Q-SA2, etc. Recorded in notes when asked outside wf.
    let mut out = BTreeSet::new();
    let bytes = text.as_bytes();
    let mut i = 0;
    while i + 2 < bytes.len() {
        if bytes[i] == b'Q' && bytes[i + 1] == b'-' {
            let start = i;
            i += 2;
            while i < bytes.len() && bytes[i].is_ascii_alphanumeric() {
                i += 1;
            }
            if i > start + 2 {
                out.insert(text[start..i].to_string());
            }
        } else {
            i += 1;
        }
    }
    out
}

fn commands_failed(data: &Value) -> bool {
    match data.get("results") {
        Some(Value::Array(rs)) => rs.iter().any(|r| r.get("ok") != Some(&Value::Bool(true))),
        _ => false,
    }
}

/// One-decimal rounding (half away from zero). For minutes, pass seconds/60.
pub fn round1(x: f64) -> f64 {
    (x * 10.0).round() / 10.0
}

fn median(xs: &[f64]) -> Option<f64> {
    if xs.is_empty() {
        return None;
    }
    let mut v = xs.to_vec();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = v.len();
    if n % 2 == 1 {
        Some(v[n / 2])
    } else {
        Some((v[n / 2 - 1] + v[n / 2]) / 2.0)
    }
}

pub fn compute(log: &[Entry]) -> Measures {
    let mut m = Measures {
        entries: log.len(),
        ..Measures::default()
    };

    let signoffs: Vec<&Entry> = log.iter().filter(|e| e.kind == "signoff").collect();
    m.signoffs = signoffs.len();

    // Fresh goal: first signoff, or the previous signoff passed.
    let mut fresh_idx = Vec::new();
    for (i, e) in signoffs.iter().enumerate() {
        let fresh = i == 0 || outcome(&signoffs[i - 1].data) == "passed";
        if fresh {
            fresh_idx.push(i);
            m.fresh_goals += 1;
            if outcome(&e.data) == "passed" {
                m.first_try_passed += 1;
            }
        }
    }

    // Longest chain: from a fresh failed (or incomplete) goal through the
    // signoff that ends it (a pass, or the last signoff if still open).
    for (k, &start) in fresh_idx.iter().enumerate() {
        let end = fresh_idx.get(k + 1).copied().unwrap_or(signoffs.len()) - 1;
        let len = end - start + 1;
        if len > m.longest_chain {
            m.longest_chain = len;
            m.longest_from = pass_of(signoffs[start]);
            m.longest_to = pass_of(signoffs[end]);
        }
    }

    let mut last_carried: BTreeSet<String> = BTreeSet::new();
    for e in &signoffs {
        let Some(cards) = e.data.get("cards").and_then(Value::as_object) else {
            last_carried.clear();
            continue;
        };
        let mut now = BTreeSet::new();
        for (k, v) in cards {
            m.cards_total += 1;
            if v.as_str() == Some("carried") {
                m.cards_carried += 1;
                now.insert(k.clone());
                if last_carried.contains(k) {
                    m.carried_twice = true;
                    m.loops += 1;
                }
            }
        }
        last_carried = now;
    }

    for e in log {
        match e.kind.as_str() {
            "check" => {
                m.check_count += 1;
                if e.data.get("verdict").and_then(Value::as_str) == Some("fail") {
                    if commands_failed(&e.data) {
                        m.fails_by_commands += 1;
                    } else {
                        m.fails_by_checker += 1;
                    }
                }
            }
            "elevate" => m.elevate += 1,
            "observe" => m.observe += 1,
            "signoff" => {
                if let Some(note) = e.data.get("note").and_then(Value::as_str) {
                    if note.to_ascii_lowercase().contains("(audit)") {
                        m.audit_notes += 1;
                    }
                    if let Some(j) = judgement_label(e, note) {
                        m.judgement_calls.push(j);
                    }
                }
            }
            "face" if is_06(&e.data) => {
                let text = e.data.get("text").and_then(Value::as_str).unwrap_or("");
                if mentions_completed_merge(text) {
                    m.merges_in_06 += 1;
                }
                if mentions_pin_action(text) {
                    m.pin_actions_in_06 += 1;
                }
                if let Some(j) = judgement_label(e, text) {
                    m.judgement_calls.push(j);
                }
                // File a finding ("Observer (…):", "Observer:", "wf observe"),
                // not a later back-reference ("per Observer's halt advice").
                let tl = text.to_ascii_lowercase();
                if tl.contains("wf observe")
                    || tl.contains("observer:")
                    || tl.contains("observer (")
                {
                    m.observer_in_06.push(e.seq);
                }
                m.questions_outside.extend(question_ids(text));
            }
            _ => {}
        }
    }

    let mut times: BTreeMap<u64, BTreeMap<String, i64>> = BTreeMap::new();
    for e in log {
        if let Some(p) = pass_of(e) {
            times.entry(p).or_default().insert(e.kind.clone(), e.time_s);
        }
    }
    for t in times.values() {
        if let (Some(&pack), Some(&close)) = (t.get("pack"), t.get("close")) {
            m.pack_close.push((close - pack) as f64 / 60.0);
        }
        if let (Some(&claim), Some(&ret)) = (t.get("claim"), t.get("return")) {
            m.builder.push((ret - claim) as f64 / 60.0);
        }
        if let (Some(&ret), Some(&check)) = (t.get("return"), t.get("check")) {
            m.checker.push((check - ret) as f64 / 60.0);
        }
    }
    m
}

fn fmt_pct(n: usize, d: usize) -> String {
    if d == 0 {
        return "n/a".into();
    }
    format!("{}%", ((n as f64 / d as f64) * 100.0).round() as i64)
}

fn fmt_ratio(n: usize, d: usize) -> String {
    if d == 0 {
        return "n/a".into();
    }
    format!("{n} / {d} = {:.1}", round1(n as f64 / d as f64))
}

fn fmt_mins(xs: &[f64]) -> String {
    match median(xs) {
        None => "n/a".into(),
        Some(med) => {
            let mut v = xs.to_vec();
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            format!(
                "median {:.1} ({:.1} to {:.1})",
                round1(med),
                round1(v[0]),
                round1(*v.last().unwrap())
            )
        }
    }
}

fn fmt_med(xs: &[f64]) -> String {
    match median(xs) {
        None => "n/a".into(),
        Some(m) => format!("{:.1}", round1(m)),
    }
}

pub fn format_table(page: &str, m: &Measures) -> String {
    let mut s = String::new();
    let _ = writeln!(s, "page: {page}  ({} log entries)", m.entries);
    let _ = writeln!(s, "#  Measure                  Value");

    let _ = writeln!(
        s,
        "1  First-try pass rate      {} of {} ({})",
        m.first_try_passed,
        m.fresh_goals,
        fmt_pct(m.first_try_passed, m.fresh_goals)
    );

    let chain = if m.longest_chain == 0 {
        "none".into()
    } else if let (Some(a), Some(b)) = (m.longest_from, m.longest_to) {
        format!("longest {} (05.{a:02}-05.{b:02})", m.longest_chain)
    } else {
        format!("longest {}", m.longest_chain)
    };
    let _ = writeln!(
        s,
        "2  Passes per goal          {}; {chain}",
        fmt_ratio(m.signoffs, m.fresh_goals)
    );

    let twice = if m.carried_twice {
        "at least one card carried twice"
    } else {
        "none carried twice"
    };
    let _ = writeln!(
        s,
        "3  Cards carried            {} of {} ({}); {twice}",
        m.cards_carried,
        m.cards_total,
        fmt_pct(m.cards_carried, m.cards_total)
    );

    let _ = writeln!(
        s,
        "4  Who caught the fails     {} by commands, {} by the checker",
        m.fails_by_commands, m.fails_by_checker
    );

    let audit = if m.audit_notes == 0 {
        "manual: look for \"(audit) agree/disagree\" in signoff notes (none in this log; baseline not measured)".to_string()
    } else {
        format!(
            "manual: {} signoff note(s) contain \"(audit)\"; read them for agree/disagree",
            m.audit_notes
        )
    };
    let _ = writeln!(s, "5  Checker misses           {audit}");

    let judgements = if m.judgement_calls.is_empty() {
        "0 judgement calls in notes".into()
    } else {
        format!(
            "{} judgement call(s): {}",
            m.judgement_calls.len(),
            m.judgement_calls.join("; ")
        )
    };
    let _ = writeln!(
        s,
        "6  Prime hand steps         {} merges and {} pin actions in 06 notes; 1 after the last pass is not in the log (manual); {judgements}",
        m.merges_in_06, m.pin_actions_in_06
    );

    let outside = if m.questions_outside.is_empty() {
        "0 outside in 06 notes".into()
    } else {
        let ids: Vec<_> = m.questions_outside.iter().cloned().collect();
        format!(
            "{} outside in 06 notes ({})",
            ids.len(),
            ids.join(", ")
        )
    };
    let _ = writeln!(
        s,
        "7  Questions to you         {} in the log; {outside}",
        m.elevate
    );

    let obs06 = if m.observer_in_06.is_empty() {
        "0 written into a 06 note".into()
    } else {
        let ids: Vec<_> = m.observer_in_06.iter().map(|n| n.to_string()).collect();
        format!(
            "{} written into a 06 note (entry {})",
            m.observer_in_06.len(),
            ids.join(", ")
        )
    };
    let loop_s = if m.loops == 0 {
        "0 loops".into()
    } else {
        format!("{} loop(s)", m.loops)
    };
    let _ = writeln!(
        s,
        "8  Observer findings        {} filed with wf; {obs06}; {loop_s}",
        m.observe
    );

    let _ = writeln!(
        s,
        "9  Time per pass            {}; builder {}; checker {}",
        fmt_mins(&m.pack_close),
        fmt_med(&m.builder),
        fmt_med(&m.checker)
    );

    let _ = writeln!(
        s,
        "10 Usage per pass           manual: weekly usage % moved / passes, and / passed passes, from the usage report"
    );
    let _ = writeln!(
        s,
        "11 Fresh-model readiness    manual: give a new model only `wf status`, face 01 and AGENTS.md; score these 5 questions out of 5: goal? next pass? who acts next? what is open? is the page halted?"
    );
    s
}

pub fn run(pages_dir: &str, page: &str) -> Result<String, String> {
    let path = Path::new(pages_dir).join(page).join("log.jsonl");
    if !path.is_file() {
        return Err(format!("no log at {}", path.display()));
    }
    let log = load_log(&path)?;
    Ok(format_table(page, &compute(&log)))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn e(kind: &str, seq: u64, time_s: i64, data: Value) -> Entry {
        Entry {
            kind: kind.into(),
            seq,
            time_s,
            data,
        }
    }

    fn so(seq: u64, pass: u64, outcome: &str, cards: Value, note: &str) -> Entry {
        e(
            "signoff",
            seq,
            1000 + seq as i64 * 100,
            json!({"pass": pass, "outcome": outcome, "cards": cards, "note": note}),
        )
    }

    #[test]
    fn first_try_chains_and_who_caught() {
        // P, F, P  →  one first-try pass of two fresh goals; longest chain 2 (05.02-05.03).
        let log = vec![
            so(1, 1, "passed", json!({"w01": "accepted"}), ""),
            so(
                2,
                2,
                "failed",
                json!({"w01": "accepted", "w02": "carried"}),
                "",
            ),
            so(3, 3, "passed", json!({"w02": "accepted"}), ""),
            e(
                "check",
                10,
                1,
                json!({"pass": 1, "verdict": "pass", "results": [{"ok": true}]}),
            ),
            e(
                "check",
                11,
                2,
                json!({"pass": 2, "verdict": "fail", "results": [{"ok": true}]}),
            ),
            e(
                "check",
                12,
                3,
                json!({"pass": 3, "verdict": "pass", "results": [{"ok": true}]}),
            ),
            e(
                "check",
                13,
                4,
                json!({"pass": 4, "verdict": "fail", "results": [{"ok": false}]}),
            ),
            e("pack", 20, 0, json!({"branch": "pass/x.05.01"})),
            e("close", 21, 600, json!({"pass": 1})), // 10.0 min
        ];
        let m = compute(&log);
        assert_eq!(m.first_try_passed, 1);
        assert_eq!(m.fresh_goals, 2);
        assert_eq!(m.signoffs, 3);
        assert_eq!(m.longest_chain, 2);
        assert_eq!(m.longest_from, Some(2));
        assert_eq!(m.longest_to, Some(3));
        assert_eq!(m.cards_carried, 1);
        assert_eq!(m.cards_total, 4);
        assert!(!m.carried_twice);
        assert_eq!(m.fails_by_checker, 1);
        assert_eq!(m.fails_by_commands, 1);
        assert_eq!(m.pack_close, vec![10.0]);
        assert_eq!(round1(10.775), 10.8);
        assert_eq!(round1(13.05), 13.1);
    }

    #[test]
    fn notes_elevate_observe_and_loops() {
        let log = vec![
            e(
                "face",
                12,
                1,
                json!({
                    "face": "06",
                    "text": "05.01 closed passed; merged by Prime as fast-forward. Tool is now the pinned binary ../wf-bin/wf. Matthew ruled Q-SA."
                }),
            ),
            e(
                "face",
                46,
                2,
                json!({
                    "face": 6,
                    "text": "Hole 5 kept as is. Not merged until 05.06 passes."
                }),
            ),
            e(
                "face",
                70,
                3,
                json!({
                    "face": "06",
                    "text": "Observer: halt advice. Prime decision: one narrow fix-up 05.09."
                }),
            ),
            so(
                4,
                1,
                "failed",
                json!({"w02": "carried"}),
                "Review counted as open: accepted, safer reading.",
            ),
            so(5, 2, "failed", json!({"w02": "carried"}), ""),
            e("elevate", 6, 4, json!({"to": "person"})),
            e("observe", 7, 5, json!({})),
            so(8, 3, "passed", json!({"w02": "accepted"}), "(audit) agree"),
        ];
        let m = compute(&log);
        assert_eq!(m.merges_in_06, 1);
        assert_eq!(m.pin_actions_in_06, 1);
        assert_eq!(m.questions_outside.iter().collect::<Vec<_>>(), vec!["Q-SA"]);
        assert_eq!(m.elevate, 1);
        assert_eq!(m.observe, 1);
        assert_eq!(m.observer_in_06, vec![70]);
        assert!(m.carried_twice);
        assert_eq!(m.loops, 1);
        assert_eq!(m.audit_notes, 1);
        assert_eq!(m.judgement_calls.len(), 3);
        let text = format_table("demo", &m);
        assert!(text.contains("1 of 1 (100%)") || text.contains("First-try"));
        assert!(text.contains("Q-SA"));
        assert!(text.contains("manual:"));
        // three fresh? first failed is fresh, second is fix-up, third is... previous failed so not fresh. 0 first-try of 1 fresh? Wait last is after failed so not fresh. first_try 0 of 1.
        assert_eq!(m.fresh_goals, 1);
        assert_eq!(m.first_try_passed, 0);
    }
}
