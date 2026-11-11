//! Writing a `.seq` file (seqpage.md 3-8). The writer is the canonical form:
//! `render(parse(text)) == text` for every file it wrote.

use crate::derive::{cards_value, derive};
use crate::error::PageError;
use crate::model::{page_entries, slot_of, PageId, SectionKey};
use crate::text::{body_lines, encode_value};
use crate::MAGIC;
use seqaddr_core::addr::check_title;
use seqaddr_core::log::{BookLog, Entry, Op};
use seqaddr_core::validate::OpRequest;
use std::collections::BTreeMap;

fn op_word(op: Op) -> &'static str {
    op.as_str()
}

/// Fields shown first, in this order; any other field follows in name order.
pub const FIELD_ORDER: [&str; 10] = ["at", "by", "tail", "from", "to", "proposal", "cites", "outcome", "of", "state"];
/// Keys carried by the block header or body, never as fields.
pub const HEADER_KEYS: [&str; 4] = ["n", "op", "addr", "body"];

/// Field lines for any serialized record (entry or proposed op). Generic, so a
/// field the core adds later still round-trips without a change here.
pub fn field_lines(map: &serde_json::Map<String, serde_json::Value>) -> Vec<String> {
    let mut keys: Vec<&String> = map.keys().filter(|k| !HEADER_KEYS.contains(&k.as_str())).collect();
    keys.sort_by_key(|k| (FIELD_ORDER.iter().position(|o| o == k).unwrap_or(FIELD_ORDER.len()), (*k).clone()));
    keys.into_iter()
        .map(|k| {
            let v = &map[k];
            if crate::text::is_field_key(k) {
                format!("{k}: {}", crate::text::encode_field(v))
            } else {
                let mut m = serde_json::Map::new();
                m.insert(k.clone(), v.clone());
                format!("x: {}", serde_json::Value::Object(m))
            }
        })
        .collect()
}

fn as_map<T: serde::Serialize>(t: &T) -> serde_json::Map<String, serde_json::Value> {
    match serde_json::to_value(t).expect("serializes") {
        serde_json::Value::Object(m) => m,
        _ => unreachable!(),
    }
}

fn booked_block(key: SectionKey, e: &Entry) -> Vec<String> {
    let mut out = vec![format!("--- @{} {} {}", e.n, op_word(e.op), encode_value(&e.addr))];
    out.extend(field_lines(&as_map(e)));
    if let Some(c) = cards_value(key, e.body.as_deref()) {
        out.push(format!("cards := {c}"));
    }
    if let Some(b) = &e.body {
        out.extend(body_lines(b));
    }
    out
}

fn new_block(key: SectionKey, o: &OpRequest) -> Vec<String> {
    let op = o.op.map(op_word).unwrap_or("put");
    let mut out = vec![format!("--- new {op} {}", encode_value(&o.addr))];
    out.extend(field_lines(&as_map(o)));
    if let Some(c) = cards_value(key, o.body.as_deref()) {
        out.push(format!("cards := {c}"));
    }
    if let Some(b) = &o.body {
        out.extend(body_lines(b));
    }
    out
}

fn section_header(page: PageId, key: SectionKey) -> String {
    let addr = page.section_addr(key);
    match key.counter {
        None => format!("= {:02} {} {addr}", key.face, key.name()),
        Some(nn) => format!("== {:02}.{nn:02} {addr}", key.face),
    }
}

/// Render a page from its booked entries (book order) plus proposed writes.
pub fn render(page: PageId, entries: &[Entry], proposed: &[OpRequest]) -> String {
    let d = derive(page, entries);
    let mut booked: BTreeMap<SectionKey, Vec<&Entry>> = BTreeMap::new();
    for e in entries {
        let k = slot_of(&e.addr).map(|(_, k)| k).unwrap_or(SectionKey::DOOR);
        booked.entry(k).or_default().push(e);
    }
    let mut new: BTreeMap<SectionKey, Vec<&OpRequest>> = BTreeMap::new();
    for o in proposed {
        let k = match slot_of(&o.addr) {
            Some((p, k)) if p == page => k,
            _ => SectionKey::DOOR,
        };
        new.entry(k).or_default().push(o);
    }
    // Every section that has entries, plus the face header for any counter.
    let mut keys: std::collections::BTreeSet<SectionKey> = booked.keys().chain(new.keys()).copied().collect();
    keys.insert(SectionKey::DOOR);
    for k in keys.clone() {
        if k.counter.is_some() && k.face != 0 {
            keys.insert(SectionKey::face(k.face));
        }
    }
    let mut out: Vec<String> = vec![MAGIC.to_string()];
    for k in keys {
        out.push(section_header(page, k));
        let mut dl = d.sections.get(&k).cloned().unwrap_or_default();
        if k.is_door() {
            // door-level board for counters on face 00 is already merged in derive()
        } else if !d.sections.contains_key(&k) {
            dl.clear();
        }
        for (dk, dv) in dl {
            out.push(format!("{dk} := {dv}"));
        }
        for e in booked.get(&k).into_iter().flatten() {
            out.push(String::new());
            out.extend(booked_block(k, e));
        }
        for o in new.get(&k).into_iter().flatten() {
            out.push(String::new());
            out.extend(new_block(k, o));
        }
        out.push(String::new());
    }
    out.push("~ history".to_string());
    let mut sorted: Vec<&Entry> = entries.iter().collect();
    sorted.sort_by_key(|e| e.n);
    for e in sorted {
        out.push(format!("@{} {} {}", e.n, op_word(e.op), encode_value(&e.addr)));
    }
    out.push("~ end".to_string());
    let mut s = out.join("\n");
    s.push('\n');
    s
}

/// Export one page of a book as `.seq` text (seqpage.md 9).
pub fn export(log: &BookLog, page: PageId) -> Result<String, PageError> {
    let entries = page_entries(log, page);
    if entries.is_empty() {
        return Err(PageError::missing(0, "seqpage 9", format!("book {} has no entries for page {page}", log.header.address)));
    }
    for e in &entries {
        check_entry_r4(e)?;
        if let Some(err) = crate::rulings::check_write(page, &e.addr, e.tail.as_deref(), 0, &format!("@{}", e.n)) {
            return Err(PageError::invalid(0, err.rule, format!("{}; this book entry breaks the ruling and cannot be exported until the book is fixed", err.detail)));
        }
    }
    Ok(render(page, &entries, &[]))
}

/// R4: every stored string of an entry is plain ASCII (0x20-0x7E plus newline).
/// A book entry that breaks it cannot be exported; the book is reported damaged.
pub fn check_entry_r4(e: &Entry) -> Result<(), PageError> {
    use crate::text::{describe_char, first_non_r4, json_r4};
    let strings: [(&str, Option<&str>); 9] = [
        ("at", Some(&e.at)),
        ("by", Some(&e.by)),
        ("addr", Some(&e.addr)),
        ("tail", e.tail.as_deref()),
        ("from", e.from.as_deref()),
        ("to", e.to.as_deref()),
        ("proposal", e.proposal.as_deref()),
        ("outcome", e.outcome.as_deref()),
        ("body", e.body.as_deref()),
    ];
    for (k, v) in strings {
        if let Some((l, c, ch)) = v.and_then(first_non_r4) {
            let at = if k == "body" { format!(" (body line {l}, column {c})") } else { String::new() };
            return Err(PageError::invalid(0, "R4", format!("@{} `{k}` holds {}{at}; stored text is plain ASCII only, so this book entry is damaged under R4 and cannot be exported", e.n, describe_char(ch))));
        }
    }
    let mut extra = serde_json::Map::new();
    extra.extend(e.extra.clone());
    if let Some(s) = &e.state {
        extra.insert("state".into(), s.clone());
    }
    if let Some(ch) = json_r4(&serde_json::Value::Object(extra)) {
        return Err(PageError::invalid(0, "R4", format!("@{} has an extra/state field holding {}; stored text is plain ASCII only", e.n, describe_char(ch))));
    }
    Ok(())
}

/// The file name: full page address, then the stamp title if it is a legal
/// title word, then `.seq` (seqpage.md 2). Page 0000 has no title (A2.8).
pub fn file_name(page: PageId, title: Option<&str>) -> String {
    match title {
        Some(t) if page.page != 0 && t != crate::derive::NONE && t != crate::derive::UNKNOWN && check_title(t).is_ok() => format!("{page}.{t}.seq"),
        _ => format!("{page}.seq"),
    }
}

/// The title the door shows for these entries (derived), if any.
pub fn derived_title(page: PageId, entries: &[Entry]) -> Option<String> {
    derive(page, entries).sections.get(&SectionKey::DOOR)?.iter().find(|(k, _)| *k == "title").map(|(_, v)| v.clone())
}
