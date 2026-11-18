//! Read-only views built fresh from the log: status (now strip, board, feed) and observe.

use crate::chars::escape_line;
use crate::log::{iso, now, short};
use crate::page::{face01_drift, s, Page};
use crate::render::cards_text;

/// Who may resume a halted page, and how. Used by status and by refusals.
pub fn how_to_resume(p: &Page) -> String {
    format!("Prime ({}) or the person ({}) resumes it: wf resume {} --note \"why (ref)\"", p.prime, p.person, p.addr)
}

fn next_step(p: &Page) -> String {
    if p.halt.is_some() {
        return format!("halted. {}", how_to_resume(p));
    }
    match p.passes.values().filter(|x| x.tail != "closed").max_by_key(|x| x.nn) {
        None => format!("Prime writes a 06 note, then wf draft {}", p.addr),
        Some(x) => pass_next(p, x),
    }
}

/// The next step for one pass that is not closed.
pub fn pass_next(p: &Page, x: &crate::page::Pass) -> String {
    let n = x.nn;
    match x.tail.as_str() {
        "draft" => format!("Prime releases it: wf pack {} {n}", p.addr),
        "pack" => format!("a builder claims it: wf claim {} {n}", p.addr),
        "open" => format!("{} pushes the work, then wf return {} {n}", x.claim.as_deref().unwrap_or("?"), p.addr),
        "return" => format!("a checker (not the builder) runs wf check {} {n}", p.addr),
        _ if x.signoff.is_some() => format!("wf close {} {n}", p.addr),
        _ => format!("Prime ({}) reads the check report, then wf signoff {} {n}", p.prime, p.addr),
    }
}

pub fn status(p: &Page) -> String {
    let mut o = format!("NOW  page {} ({})  prime: {}  person: {}\n", p.addr, p.title, p.prime, p.person);
    let open: Vec<String> = p.passes.values().filter(|x| x.tail != "closed")
        .map(|x| format!("05.{:02} {} {}", x.nn, x.tail, x.claim.as_deref().map(|c| format!("(held by {c})")).unwrap_or_default())).collect();
    o += &format!("  active:  {}\n", if open.is_empty() { "none".into() } else { open.join("; ") });
    let waiting: Vec<String> = p.elevs.iter().filter(|e| e.answer.is_none()).map(|e| format!("entry {} 05.{:02} {} -> {}: {}", e.seq, e.pass, e.by, e.to, escape_line(&e.item))).collect();
    o += &format!("  waiting: {}\n", if waiting.is_empty() { "nothing".into() } else { waiting.join("\n           ") });
    if let Some((who, t, note, seq)) = &p.halt {
        o += &format!("  halted:  by {who} at {} (entry {seq}): {note}\n", iso(*t));
    }
    o += &format!("  next:    {}\n", next_step(p));
    o += &format!("  log:     {} entries, last {}, head {}\n", p.events.len(), p.events.last().map(|e| iso(e.time)).unwrap_or_default(), short(&p.head));
    if !p.findings.is_empty() {
        o += &format!("  observer findings: {} (latest: {})\n", p.findings.len(), p.findings.last().unwrap().2);
    }
    o += "\nBOARD\n  pass   tail     outcome          claim        checker      cards\n";
    for x in p.passes.values() {
        let outcome = x.close.as_ref().map(|c| s(c, "outcome")).unwrap_or("-".into());
        let cards = x.close.as_ref().map(|c| cards_text(&c["cards"])).unwrap_or("-".into());
        let checker = x.check.as_ref().map(|c| c.0.clone()).unwrap_or("-".into());
        o += &format!("  05.{:02}  {:<8} {:<16} {:<12} {:<12} {}\n", x.nn, x.tail, outcome, x.claim.as_deref().unwrap_or("-"), checker, cards);
    }
    o += "\nFEED (newest first)\n";
    for e in p.events.iter().rev().take(10) {
        let pass = e.data["pass"].as_u64().map(|n| format!(" 05.{n:02}")).unwrap_or_default();
        o += &format!("  {:>3} {} {:<14}{} by {} ({})\n", e.seq, iso(e.time), e.kind, pass, e.actor, e.role);
    }
    o
}

/// One face that changed under a packed pass that is not closed.
/// `was` and `now` name the face's entry ("7" for 04; "v1 entry 3" for 01).
pub struct Drift {
    pub face: &'static str,
    pub was: String,
    pub now: String,
}

/// Faces 04 and 01 that changed since the pass was packed. Shared by observe and board.
pub fn drift(p: &Page, x: &crate::page::Pass) -> Vec<Drift> {
    let Some(pk) = x.pack.as_ref().filter(|_| x.tail != "closed") else { return vec![] };
    let mut out = vec![];
    let now04 = p.faces.get("04").map(|g| g.seq).unwrap_or(0);
    let pinned = x.pins["04"]["entry"].as_u64().unwrap_or(0);
    if now04 != pinned {
        out.push(Drift { face: "04", was: pinned.to_string(), now: now04.to_string() });
    }
    if let Some(v01) = face01_drift(p, pk) {
        let src = s(&pk["sources"], "01");
        let was = src.split(" hash ").next().unwrap_or("").to_string();
        out.push(Drift { face: "01", was: if was.is_empty() { "unknown (not in the log)".into() } else { was }, now: v01 });
    }
    out
}

/// Signals that the lead may be drifting, looping or stalled. Read only.
pub fn observe(p: &Page, stall_hours: u64) -> Vec<String> {
    let mut f = vec![];
    let n = p.passes.len();
    if n >= 6 {
        f.push(format!("{n} passes on this page: halt advised before the next release (the observer stops nothing)"));
    } else if n >= 4 {
        f.push(format!("{n} passes on this page: ask the why questions"));
    }
    let mut seen: Vec<(String, u32)> = vec![];
    for x in p.passes.values() {
        for (k, v) in x.ret.as_ref().and_then(|r| r["jobs"].as_object().cloned()).unwrap_or_default() {
            let v = v.as_str().unwrap_or("").to_lowercase();
            if v.starts_with("done") {
                continue;
            }
            let item = v.splitn(2, ' ').nth(1).unwrap_or("").trim_start_matches(['-', ' ']).to_string();
            if let Some((_, first)) = seen.iter().find(|(i, _)| *i == item) {
                f.push(format!("same blocker again: 05.{first:02} and 05.{:02} {k}: {}", x.nn, escape_line(&item)));
            }
            seen.push((item, x.nn));
        }
    }
    let outs: Vec<String> = p.passes.values().filter_map(|x| x.close.as_ref().map(|c| s(c, "outcome"))).collect();
    if outs.len() >= 2 && outs[outs.len() - 2..].iter().all(|o| o != "passed") {
        f.push(format!("loop: the last two closed passes ended {} and {}", outs[outs.len() - 2], outs[outs.len() - 1]));
    }
    if let Some(last) = p.events.last() {
        let h = now().saturating_sub(last.time) / 3600;
        if last.time > 0 && h >= stall_hours && p.halt.is_none() && p.passes.values().any(|x| x.tail != "closed") {
            f.push(format!("stalled: nothing has moved for {h} hours (entry {})", last.seq));
        }
    }
    for x in p.passes.values() {
        for d in drift(p, x) {
            f.push(match d.face {
                "04" => format!("drift: 05.{:02} was packed against face 04 entry {}; face 04 is now entry {}", x.nn, d.was, d.now),
                _ => format!("drift: 05.{:02} was packed against an older face 01 (now {})", x.nn, d.now),
            });
        }
    }
    for e in p.elevs.iter().filter(|e| e.answer.is_none()) {
        f.push(format!("unanswered: entry {} to {}: {}", e.seq, e.to, escape_line(&e.item)));
    }
    f
}
