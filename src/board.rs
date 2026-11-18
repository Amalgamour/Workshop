//! `wf board`: a read-only work-order board built only from the log (docs/design/WF-BOARD.md).
//! It never writes: no log entry, no view reprint, no lock file, and it runs no git.
//! Every string that came from the log goes through `escape_line` before it prints,
//! and each output line is passed through it once more as a guard (a no-op on clean text).

use crate::chars::escape_line;
use crate::log::{iso, now, short, Res};
use crate::page::{s, Page, Pass};
use crate::render::{self, git_changed_text, ViewDiff};
use crate::status::{drift, how_to_resume, observe, pass_next};
use crate::Args;
use std::path::Path;

/// The default page board is at most this many lines, except that person questions
/// and a halt are never cut (WF-BOARD.md section 2 and rules 1-2).
pub const CAP: usize = 40;
/// Closed cards shown by default; the footer counts the rest.
const CLOSED_SHOWN: usize = 3;
/// Long log text is cut to this many characters, after escaping.
const WIDTH: usize = 90;

/// (tail, column, body-shop side label, who owes the next move).
/// Build stage, pending Director answer (WF-BOARD.md Q1): tool words are the columns,
/// the body-shop words are side labels only.
pub const COLUMNS: [(&str, &str, &str, &str); 6] = [
    ("draft", "Draft", "estimate", "Prime: wf pack"),
    ("pack", "Ready", "ready for a bay", "any builder: wf claim"),
    ("open", "Working", "in the bay", "the builder who claimed it"),
    ("return", "Waiting check", "waiting QC", "a checker who is not the builder"),
    ("review", "Checked", "QC done", "Prime: wf signoff, then wf close"),
    ("closed", "Closed", "delivered", "nobody"),
];

/// Build stage, pending Director answer (WF-BOARD.md Q2): an open pass is STALE after
/// 24 hours with no log entry, the observer's default; `--stall-hours` changes it.
pub const STALL_HOURS: u64 = 24;

/// Build stage, pending Director answer (WF-BOARD.md Q3): the board reads only the log
/// and prints the git commands that open the evidence. It does not run git.
const NOT_CHECKED: &str = "links printed, not checked: the board runs no git (build stage, pending Director answer, WF-BOARD.md Q3)";

const UNKNOWN: &str = "unknown (not in the log)";

pub struct Opts {
    pub all: bool,
    pub stall_hours: u64,
}

/// `wf board [<page>] [--all] [--card NN] [--stall-hours H]`. Reads only.
pub fn run(root: &Path, a: &Args) -> Res<()> {
    let stall_hours = match a.flag("stall-hours") {
        None => STALL_HOURS,
        Some(h) => h.parse().map_err(|_| format!("--stall-hours must be a whole number of hours, not '{}'", escape_line(h)))?,
    };
    let Some(addr) = a.pos.first() else {
        print!("{}", book(root, stall_hours, now()));
        return Ok(());
    };
    crate::page::check_addr(addr)?;
    let dir = root.join("pages").join(addr);
    if !dir.join("log.jsonl").exists() {
        return Err(format!("no page {addr} under {}", escape_line(&dir.display().to_string())));
    }
    let p = Page::load(&dir)?;
    let edited = render::edited(&p);
    let out = match a.flag("card") {
        Some(c) => {
            let n: u32 = c.trim_start_matches('0').parse().map_err(|_| format!("--card needs a pass number like 1 or 01, not '{}'", escape_line(c)))?;
            card(&p, p.pass(n)?, stall_hours, now())
        }
        None => page_board(&p, &edited, &Opts { all: a.flag("all").is_some(), stall_hours }, now()),
    };
    print!("{out}");
    Ok(())
}

/// Escape log text for one line, then cut it on a character boundary, never inside `\u{...}`.
pub fn clip(text: &str, max: usize) -> String {
    let t = escape_line(text);
    if t.chars().count() <= max {
        return t;
    }
    let mut cut: String = t.chars().take(max.saturating_sub(3)).collect();
    if let Some(i) = cut.rfind('\\') {
        let rest = &cut[i..];
        if !rest.contains('}') && ("\\u{".starts_with(rest) || rest.starts_with("\\u{")) {
            cut.truncate(i);
        }
    }
    cut + "..."
}

fn e(text: &str) -> String {
    escape_line(text)
}

fn column_of(tail: &str) -> usize {
    COLUMNS.iter().position(|c| c.0 == tail).unwrap_or(0)
}

fn time_of(p: &Page, seq: u64) -> u64 {
    p.events.get((seq as usize).wrapping_sub(1)).map(|ev| ev.time).unwrap_or(0)
}

/// Entry numbers of every `kind` event on pass `nn`, oldest first.
fn entries(p: &Page, nn: u32, kind: &str) -> Vec<u64> {
    p.events.iter().filter(|ev| ev.kind == kind && ev.data["pass"].as_u64() == Some(nn as u64)).map(|ev| ev.seq).collect()
}

fn last_entry(p: &Page, nn: u32, kind: &str) -> String {
    entries(p, nn, kind).last().map(|n| n.to_string()).unwrap_or_else(|| UNKNOWN.into())
}

fn age(secs: u64) -> String {
    if secs < 3600 { format!("{}m", secs / 60) } else { format!("{}h", secs / 3600) }
}

fn failed_checks(p: &Page, nn: u32) -> usize {
    p.events.iter().filter(|ev| ev.kind == "check" && ev.data["pass"].as_u64() == Some(nn as u64) && s(&ev.data, "verdict") == "fail").count()
}

fn open_questions(p: &Page, nn: u32) -> usize {
    p.elevs.iter().filter(|q| q.pass == nn && q.answer.is_none()).count()
}

/// Why a pass is stale (WF-BOARD.md section 5). Empty when it is not. Closed passes are never stale.
pub fn stale(p: &Page, x: &Pass, stall_hours: u64, t: u64) -> Vec<String> {
    let mut why = vec![];
    if x.tail == "closed" {
        return why;
    }
    let h = t.saturating_sub(time_of(p, x.last_seq)) / 3600;
    if x.is_open_tail() && h >= stall_hours {
        why.push(format!("wait: no log entry for {h}h (last entry {}; limit {stall_hours}h)", x.last_seq));
    }
    for d in drift(p, x) {
        let (was, now) = if d.face == "04" { (format!("entry {}", d.was), format!("entry {}", d.now)) } else { (d.was, d.now) };
        why.push(format!("drift: packed against face {} {}; face {} is now {}", d.face, e(&was), d.face, e(&now)));
    }
    if let (Some(r), Some((_, c))) = (&x.ret, &x.check) {
        if s(r, "commit") != s(c, "commit") {
            why.push(format!(
                "old check: check entry {} was on commit {}; the latest return (entry {}) is commit {}",
                last_entry(p, x.nn, "check"), short(&e(&s(c, "commit"))), last_entry(p, x.nn, "return"), short(&e(&s(r, "commit")))
            ));
        }
    }
    if let Some((_, seq, _)) = &x.signoff {
        let f01 = p.faces.get("01").map(|f| f.seq).unwrap_or(0);
        if f01 > *seq {
            why.push(format!("old signoff: face 01 changed at entry {f01}, after the signoff entry {seq}"));
        }
    }
    why
}

/// What needs someone, most urgent first: (rule 1-8, line). Rules 1 and 2 are never cut.
pub fn attention(p: &Page, edited: &Res<ViewDiff>, stall_hours: u64, t: u64) -> Vec<(u8, String)> {
    let mut out = vec![];
    let ask = |to: &str, who: &str, q: &crate::page::Elev| {
        format!("QUESTION for {to} ({}): entry {} on 05.{:02} from {}: {}. Answer: wf answer {} {} --text \"...\"",
            e(who), q.seq, q.pass, e(&q.by), clip(&q.item, WIDTH), e(&p.addr), q.seq)
    };
    for q in p.elevs.iter().filter(|q| q.answer.is_none() && q.to == "person") {
        out.push((1, ask("the person", &p.person, q)));
    }
    if let Some((who, at, note, seq)) = &p.halt {
        out.push((2, format!("HALTED by {} at {} (entry {seq}): {}. {}", e(who), iso(*at), clip(note, WIDTH), e(&how_to_resume(p)))));
    }
    match edited {
        Ok(d) if !d.is_empty() => out.push((3, format!("VIEWS DIFFER from the log: {}. The board prints from the log; the log wins; run wf verify {} --fix", e(&d.report()), e(&p.addr)))),
        Err(why) => out.push((3, format!("VIEWS NOT COMPARED: {}. The board prints from the log; run wf verify {}", clip(why, WIDTH), e(&p.addr)))),
        _ => {}
    }
    for x in p.passes.values().filter(|x| x.tail == "return") {
        out.push((4, format!("WAITING CHECK 05.{:02}: returned by {} at entry {}. Next: {}", x.nn, e(x.claim.as_deref().unwrap_or(UNKNOWN)), last_entry(p, x.nn, "return"), e(&pass_next(p, x)))));
    }
    for x in p.passes.values().filter(|x| x.tail == "review") {
        let (who, c) = x.check.clone().unwrap_or_default();
        let signed = x.signoff.as_ref().map(|(_, n, _)| format!(", signed off at entry {n}")).unwrap_or_default();
        out.push((5, format!("CHECKED 05.{:02}: verdict {} by {} (entry {}){signed}. Next: {}", x.nn, e(&s(&c, "verdict")), e(&who), last_entry(p, x.nn, "check"), e(&pass_next(p, x)))));
    }
    for q in p.elevs.iter().filter(|q| q.answer.is_none() && q.to != "person") {
        out.push((6, ask("Prime", &p.prime, q)));
    }
    // Unanswered questions and drift already have their own lines (rules 1, 6 and 8).
    let last = p.events.last().map(|ev| ev.seq).unwrap_or(0);
    for f in observe(p, stall_hours).into_iter().filter(|f| !f.starts_with("unanswered:") && !f.starts_with("drift:")) {
        let at = if f.contains("entry") { String::new() } else { format!(" (as of entry {last})") };
        out.push((7, format!("OBSERVER: {}{at}", e(&f))));
    }
    for x in p.passes.values() {
        let why = stale(p, x, stall_hours, t);
        if !why.is_empty() {
            out.push((8, format!("STALE 05.{:02}: {}", x.nn, why.join("; "))));
        }
    }
    out
}

fn short_card(p: &Page, x: &Pass, stall_hours: u64, t: u64) -> Vec<String> {
    let outcome = clip(x.fields.get("outcome").and_then(|v| v.as_str()).unwrap_or(UNKNOWN), WIDTH - 30);
    if x.tail == "closed" {
        let how = x.close.as_ref().map(|c| s(c, "outcome")).unwrap_or_default();
        return vec![format!("    05.{:02}  {:<15} {outcome}  (closed at entry {})", x.nn, e(&how), last_entry(p, x.nn, "close"))];
    }
    let mark = if stale(p, x, stall_hours, t).is_empty() { "" } else { "  STALE" };
    vec![
        format!("    05.{:02}  {outcome}  ({}){mark}", x.nn, e(&x.tail)),
        format!("           held by {} | next: {} | age {} | open questions {}, refused returns {}, failed checks {}",
            e(x.claim.as_deref().unwrap_or("nobody")), e(&pass_next(p, x)), age(t.saturating_sub(time_of(p, x.last_seq))),
            open_questions(p, x.nn), x.refusals.len(), failed_checks(p, x.nn)),
    ]
}

/// The page board: header, attention, columns, footer. At most CAP lines unless `all`,
/// but person questions and a halt are always printed.
pub fn page_board(p: &Page, edited: &Res<ViewDiff>, o: &Opts, t: u64) -> String {
    // (lines, must keep, is a card)
    let mut units: Vec<(Vec<String>, bool, bool)> = vec![];
    let must = |u: &mut Vec<(Vec<String>, bool, bool)>, l: String| u.push((vec![l], true, false));
    must(&mut units, format!("BOARD  page {} ({})  person: {}  prime: {}", e(&p.addr), e(&p.title), e(&p.person), e(&p.prime)));
    must(&mut units, format!("  log: {} entries, last entry {}, head {}; board time {}; read only, built from the log",
        p.events.len(), p.events.last().map(|ev| iso(ev.time)).unwrap_or_else(|| UNKNOWN.into()), short(&p.head), iso(t)));
    must(&mut units, "ATTENTION (most urgent first)".into());
    let attn = attention(p, edited, o.stall_hours, t);
    if attn.is_empty() {
        must(&mut units, "  attention: none found in the log".into());
    }
    for (rule, line) in attn {
        units.push((vec![format!("  {line}")], rule <= 2, false));
    }
    must(&mut units, "COLUMNS (tool word [side label]: count; who owes the next move)".into());
    let mut older_closed = 0;
    for (i, (_, name, label, owner)) in COLUMNS.iter().enumerate() {
        let mut xs: Vec<&Pass> = p.passes.values().filter(|x| column_of(&x.tail) == i).collect();
        let count = xs.len();
        let mut head = format!("  {name} [{label}]: {count}; next move: {owner}");
        if i == 5 {
            let n = |w: &str| xs.iter().filter(|x| x.close.as_ref().map(|c| s(c, "outcome")).as_deref() == Some(w)).count();
            let known = n("passed") + n("failed") + n("blocked") + n("needs-authority");
            head = format!("  {name} [{label}]: {count} (passed {}, failed {}, blocked {}, needs-authority {}{}); next move: {owner}",
                n("passed"), n("failed"), n("blocked"), n("needs-authority"), if count > known { format!(", other {}", count - known) } else { String::new() });
            if !o.all && xs.len() > CLOSED_SHOWN {
                xs.sort_by_key(|x| x.last_seq);
                older_closed = xs.len() - CLOSED_SHOWN;
                xs.drain(..older_closed);
                xs.sort_by_key(|x| x.nn);
            }
        }
        must(&mut units, head);
        for x in xs {
            units.push((short_card(p, x, o.stall_hours, t), false, true));
        }
    }
    let must_lines: usize = units.iter().filter(|u| u.1).map(|u| u.0.len()).sum::<usize>() + 1;
    let mut budget = if o.all { usize::MAX } else { CAP.saturating_sub(must_lines) };
    let (mut cut_attn, mut cut_cards, mut full) = (0, 0, false);
    let mut out = String::new();
    for (lines, keep, is_card) in units {
        if !keep {
            if full || lines.len() > budget {
                full = true;
                if is_card { cut_cards += 1 } else { cut_attn += 1 }
                continue;
            }
            budget -= lines.len();
        }
        for l in lines {
            out += &escape_line(&l);
            out.push('\n');
        }
    }
    let addr = e(&p.addr);
    out += &if cut_attn + cut_cards + older_closed == 0 {
        format!("  footer: nothing cut. Full card: wf board {addr} --card NN\n")
    } else {
        format!("  footer: not shown: {cut_attn} attention lines, {cut_cards} cards, {older_closed} older closed cards. See all: wf board {addr} --all; full card: wf board {addr} --card NN\n")
    };
    out
}

/// The full card for one pass: every field, with where it came from.
pub fn card(p: &Page, x: &Pass, stall_hours: u64, t: u64) -> String {
    let n = x.nn;
    let (addr, dir) = (e(&p.addr), format!("pages/{}/05.{n:02}", e(&p.addr)));
    let (_, col, label, owner) = COLUMNS[column_of(&x.tail)];
    let field = |k: &str| x.fields.get(k).and_then(|v| v.as_str()).map(e).unwrap_or_else(|| UNKNOWN.into());
    let mut l = vec![
        format!("CARD 05.{n:02}  page {addr} ({})  read only, built from the log", e(&p.title)),
        format!("  column:     {col} [{label}]; tail {}; next move owed by {owner}", e(&x.tail)),
        format!("  outcome:    {} (draft entry {})", field("outcome"), last_entry(p, n, "draft")),
    ];
    for (k, v) in render::jobs(&x.fields) {
        l.push(format!("  job {}:    {}", e(&k), e(&v)));
    }
    l.push(format!("  may touch:  {}", field("may touch")));
    l.push(format!("  checks:     {}", field("checks")));
    l.push(format!("  repo:       {}; start {}", field("repo"), field("start")));
    l.push(format!("  held by:    {} (claim entry {})", e(x.claim.as_deref().unwrap_or(UNKNOWN)), last_entry(p, n, "claim")));
    l.push(format!("  next:       {}", if x.tail == "closed" { "nobody".into() } else { e(&pass_next(p, x)) }));
    l.push(format!("  age:        {} since entry {}", age(t.saturating_sub(time_of(p, x.last_seq))), x.last_seq));
    let st = stale(p, x, stall_hours, t);
    l.push(format!("  stale:      {}", if st.is_empty() { "none found in the log".into() } else { format!("STALE {}", st.join("; ")) }));
    match &x.pack {
        Some(pk) => {
            l.push(format!("  pack:       entry {}; hash {}; template version {}", last_entry(p, n, "pack"), short(&e(&s(pk, "pack_hash"))),
                pk.get("templates").map(|v| e(&v.to_string())).unwrap_or_else(|| "1 (none stored)".into())));
            for f in ["PACK.md", "PROMPT.md", "AGENTS.md", "RETURN-TEMPLATE.md"] {
                l.push(format!("    file:     {dir}/{f}"));
            }
        }
        None => l.push(format!("  pack:       {UNKNOWN}")),
    }
    match &x.ret {
        Some(r) => {
            l.push(format!("  return:     entry {}; commit {}; branch {}; hash {}", last_entry(p, n, "return"), e(&s(r, "commit")), e(&s(r, "branch")), short(&e(&s(r, "hash")))));
            l.push(format!("    open:     git -C {} show {}:{}", field("repo"), e(&s(r, "commit")), e(&s(r, "file"))));
            l.push(format!("    changed:  {}", { let g = git_changed_text(r); if g.is_empty() { UNKNOWN.into() } else { g } }));
            for (k, v) in r["jobs"].as_object().cloned().unwrap_or_default() {
                l.push(format!("    {}:      {}", e(&k), clip(v.as_str().unwrap_or(""), WIDTH)));
            }
        }
        None => l.push(format!("  return:     {UNKNOWN}")),
    }
    if x.refusals.is_empty() {
        l.push("  refused returns: none found in the log".into());
    }
    for (seq, why) in &x.refusals {
        l.push(format!("  refused return: entry {seq}: {}", clip(why, WIDTH)));
    }
    match &x.check {
        Some((who, c)) => {
            l.push(format!("  check:      entry {}; checker {}; verdict {}; commit {}; failed checks {}", last_entry(p, n, "check"), e(who), e(&s(c, "verdict")), short(&e(&s(c, "commit"))), failed_checks(p, n)));
            l.push(format!("    report:   pages/{addr}/05.md section \"## 05.{n:02}\""));
        }
        None => l.push(format!("  check:      {UNKNOWN}")),
    }
    match &x.signoff {
        Some((who, seq, d)) => l.push(format!("  signoff:    entry {seq}; by {}; outcome {}; cards {}", e(who), e(&s(d, "outcome")), e(&render::cards_text(&d["cards"])))),
        None => l.push(format!("  signoff:    {UNKNOWN}")),
    }
    match &x.close {
        Some(c) => {
            l.push(format!("  close:      entry {}; outcome {}; record_hash {}", last_entry(p, n, "close"), e(&s(c, "outcome")), short(&e(&s(c, "record_hash")))));
            l.push(format!("    record:   pages/{addr}/05.md section \"## 05.{n:02}\""));
        }
        None => l.push(format!("  close:      {UNKNOWN}")),
    }
    for q in p.elevs.iter().filter(|q| q.pass == n) {
        let ans = q.answer.as_deref().map(clip_w).unwrap_or_else(|| "no answer".into());
        l.push(format!("  question:   entry {} to {} from {}: {} ({ans})", q.seq, e(&q.to), e(&q.by), clip(&q.item, WIDTH)));
    }
    l.push(format!("  evidence:   {NOT_CHECKED}"));
    l.iter().map(|x| escape_line(x) + "\n").collect()
}

fn clip_w(s: &str) -> String {
    clip(s, WIDTH)
}

/// The book board: one line per page under `pages/`. An unreadable page is shown, not fatal.
pub fn book(root: &Path, stall_hours: u64, t: u64) -> String {
    let pages = root.join("pages");
    let mut names: Vec<String> = match std::fs::read_dir(&pages) {
        Ok(rd) => rd.filter_map(|d| d.ok()).filter(|d| d.path().is_dir()).map(|d| d.file_name().to_string_lossy().to_string()).collect(),
        Err(_) => vec![],
    };
    names.sort();
    let mut o = format!("BOOK BOARD  {} pages under {} (read only, built from each log)\n", names.len(), e(&pages.display().to_string()));
    if names.is_empty() {
        o += "  pages: none found under pages/\n";
    }
    for name in names {
        let dir = pages.join(&name);
        let line = if !dir.join("log.jsonl").is_file() {
            format!("  {}  unreadable: no log.jsonl", e(&name))
        } else {
            match Page::load(&dir) {
                Err(why) => format!("  {}  unreadable: {}", e(&name), clip(&why, WIDTH)),
                Ok(p) => {
                    let c = |tail: &str| p.passes.values().filter(|x| x.tail == tail).count();
                    let attn = attention(&p, &render::edited(&p), stall_hours, t).len();
                    format!("  {}  {}  entries {}, last {} | draft {}, ready {}, working {}, waiting check {}, checked {}, closed {} | attention {}{}",
                        e(&name), clip(&p.title, 30), p.events.len(), p.events.last().map(|ev| iso(ev.time)).unwrap_or_else(|| UNKNOWN.into()),
                        c("draft"), c("pack"), c("open"), c("return"), c("review"), c("closed"), attn, if p.halt.is_some() { ", HALTED" } else { "" })
                }
            }
        };
        o += &escape_line(&line);
        o.push('\n');
    }
    o += "  page board: wf board <page>\n";
    o
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::log::Event;
    use crate::page::Elev;
    use serde_json::json;

    const T0: u64 = 1_795_456_800;

    fn page() -> Page {
        Page { addr: "1.2.3.4".into(), title: "t".into(), person: "mat".into(), prime: "pri".into(), head: "ab".repeat(32), ..Default::default() }
    }

    fn ev(p: &mut Page, kind: &str, time: u64, data: serde_json::Value) -> u64 {
        let seq = p.events.len() as u64 + 1;
        p.events.push(Event { seq, time, actor: "pri".into(), role: "prime".into(), kind: kind.into(), data });
        seq
    }

    fn pass(p: &mut Page, nn: u32, tail: &str) {
        let seq = ev(p, tail, T0, json!({"pass": nn}));
        let mut x = Pass { nn, tail: tail.into(), last_seq: seq, ..Default::default() };
        x.fields.insert("outcome".into(), json!(format!("outcome {nn}")));
        if tail == "closed" {
            x.close = Some(json!({"outcome": "passed"}));
        }
        p.passes.insert(nn, x);
    }

    fn ask(p: &mut Page, to: &str, item: &str) {
        let seq = ev(p, "elevate", T0, json!({"pass": 1, "to": to, "item": item}));
        p.elevs.push(Elev { seq, pass: 1, to: to.into(), by: "bob".into(), item: item.into(), answer: None });
    }

    fn board(p: &Page, all: bool, t: u64) -> String {
        page_board(p, &Ok(ViewDiff::default()), &Opts { all, stall_hours: STALL_HOURS }, t)
    }

    #[test]
    fn clip_cuts_after_escape_and_never_inside_an_escape() {
        assert_eq!(clip("short", 10), "short");
        let c = clip("abcdef\u{1b}ghijkl", 10);
        assert_eq!(c, "abcdef...");
        assert!(!c.contains('\u{1b}'));
        let c = clip("ab\u{1b}cdefghijklmnop", 12);
        assert_eq!(c, "ab\\u{1b}c...");
        assert_eq!(clip("abcde\u{1b}fghijk", 10), "abcde...");
        assert_eq!(clip("éééééééééé", 6), "ééé...");
    }

    #[test]
    fn each_tail_shows_in_its_column() {
        let mut p = page();
        for (i, (tail, ..)) in COLUMNS.iter().enumerate() {
            pass(&mut p, i as u32 + 1, tail);
        }
        let b = board(&p, false, T0);
        let lines: Vec<&str> = b.lines().collect();
        for (i, (_, name, label, _)) in COLUMNS.iter().enumerate() {
            let head = lines.iter().position(|l| l.starts_with(&format!("  {name} [{label}]: 1"))).unwrap_or_else(|| panic!("{name}: {b}"));
            assert!(lines[head + 1].starts_with(&format!("    05.{:02}", i + 1)), "{name}: {b}");
        }
    }

    #[test]
    fn attention_order_and_none_found() {
        let mut p = page();
        assert!(board(&p, false, T0).contains("  attention: none found in the log\n"));
        assert!(!board(&p, false, T0).contains("all clear"));
        pass(&mut p, 1, "return");
        pass(&mut p, 2, "review");
        ask(&mut p, "prime", "need a path");
        ask(&mut p, "person", "may we widen");
        p.halt = Some(("pri".into(), T0, "wait (t1)".into(), 9));
        let a = attention(&p, &Err("x".into()), STALL_HOURS, T0);
        let rules: Vec<u8> = a.iter().map(|r| r.0).collect();
        let mut sorted = rules.clone();
        sorted.sort();
        assert_eq!(rules, sorted, "{a:?}");
        assert!(a[0].1.starts_with("QUESTION for the person (mat): entry"), "{a:?}");
        assert!(a[1].1.starts_with("HALTED by pri"), "{a:?}");
        assert!(rules.contains(&3) && rules.contains(&4) && rules.contains(&5) && rules.contains(&6), "{a:?}");
    }

    #[test]
    fn cap_never_cuts_person_questions_or_the_halt() {
        let mut p = page();
        for nn in 1..=20 {
            pass(&mut p, nn, "closed");
        }
        for i in 0..50 {
            ask(&mut p, "person", &format!("person q {i}"));
        }
        for i in 0..30 {
            ask(&mut p, "prime", &format!("prime q {i}"));
        }
        p.halt = Some(("pri".into(), T0, "wait (t1)".into(), 9));
        let b = board(&p, false, T0);
        assert_eq!(b.matches("QUESTION for the person").count(), 50, "{b}");
        assert!(b.contains("HALTED by pri"), "{b}");
        let shown = b.matches("QUESTION for Prime").count();
        assert!(b.contains(&format!("not shown: {} attention lines", 30 + 1 - shown)), "{b}");
        assert!(b.contains("17 older closed cards"), "{b}");
        let all = board(&p, true, T0);
        assert_eq!(all.matches("QUESTION for Prime").count(), 30);
        assert_eq!(all.matches("(closed at entry").count(), 20);
        assert!(all.contains("footer: nothing cut"), "{all}");
    }

    #[test]
    fn small_cap_cuts_cards_but_stays_within_40_lines() {
        let mut p = page();
        for nn in 1..=25 {
            pass(&mut p, nn, "pack");
        }
        ask(&mut p, "person", "q");
        let b = board(&p, false, T0);
        assert!(b.lines().count() <= CAP, "{} lines: {b}", b.lines().count());
        assert!(b.contains("QUESTION for the person"));
        let cut: usize = b.split("attention lines, ").nth(1).unwrap().split(' ').next().unwrap().parse().unwrap();
        assert_eq!(cut + b.matches("    05.").count(), 25, "{b}");
    }

    #[test]
    fn open_pass_is_stale_after_the_stall_hours() {
        let mut p = page();
        pass(&mut p, 1, "open");
        p.passes.get_mut(&1).unwrap().claim = Some("bob".into());
        assert!(stale(&p, &p.passes[&1], 24, T0 + 23 * 3600).is_empty());
        let why = stale(&p, &p.passes[&1], 24, T0 + 25 * 3600);
        assert_eq!(why, vec!["wait: no log entry for 25h (last entry 1; limit 24h)".to_string()]);
        assert!(stale(&p, &p.passes[&1], 48, T0 + 25 * 3600).is_empty());
        let b = page_board(&p, &Ok(ViewDiff::default()), &Opts { all: false, stall_hours: 24 }, T0 + 25 * 3600);
        assert!(b.contains("(open)  STALE") && b.contains("STALE 05.01: wait"), "{b}");
        pass(&mut p, 2, "closed");
        assert!(stale(&p, &p.passes[&2], 0, T0 + 99 * 3600).is_empty(), "closed is never stale");
    }

    #[test]
    fn hostile_log_text_is_escaped_on_board_and_card() {
        let bad = "x\u{1b}[2K\r next:\u{2028}\u{85}\u{202e}\u{e0001}\u{3164}y";
        let mut p = page();
        p.title = bad.into();
        p.person = bad.into();
        pass(&mut p, 1, "return");
        let x = p.passes.get_mut(&1).unwrap();
        x.claim = Some(bad.into());
        x.fields.insert("outcome".into(), json!(bad));
        x.refusals.push((1, bad.into()));
        x.ret = Some(json!({"commit": bad, "branch": bad, "file": bad, "jobs": {"w01": bad}, "changed": [{"letter": "A", "path": bad}]}));
        ask(&mut p, "person", bad);
        p.halt = Some((bad.into(), T0, bad.into(), 2));
        let out = board(&p, true, T0) + &card(&p, &p.passes[&1], 24, T0);
        for c in ['\u{1b}', '\r', '\u{2028}', '\u{85}', '\u{202e}', '\u{e0001}', '\u{3164}'] {
            assert!(!out.contains(c), "raw U+{:04X} in: {out}", c as u32);
        }
        assert!(out.contains("\\u{1b}") && out.contains("\\u{3164}") && out.contains("\\u{e0001}"), "{out}");
        assert!(!out.lines().any(|l| l.trim() == "next:"), "{out}");
    }

    #[test]
    fn card_says_unknown_for_fields_not_in_the_log() {
        let mut p = page();
        pass(&mut p, 1, "draft");
        let c = card(&p, &p.passes[&1], 24, T0);
        for k in ["pack:", "return:", "check:", "signoff:", "close:"] {
            assert!(c.contains(&format!("  {k}")) && c.lines().any(|l| l.contains(k) && l.ends_with("unknown (not in the log)")), "{k}: {c}");
        }
        assert!(!c.lines().any(|l| l.trim_end().ends_with(" -")), "{c}");
    }
}
