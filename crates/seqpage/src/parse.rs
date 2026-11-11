//! Reading and checking a `.seq` file (seqpage.md 3-8, 11).
//!
//! `parse` reads the structure and stops at the first malformed line.
//! `check` then collects every rule broken by a well-formed file.

use crate::derive::{cards_value, derive};
use crate::error::{PageError, Report};
use crate::model::{slot_of, Block, BlockKind, Derived, HistLine, PageId, Section, SectionKey, SeqPage};
use crate::text::{body_line, decode_value};
use crate::write::file_name;
use crate::MAGIC;
use seqaddr_core::addr::Address;
use seqaddr_core::log::{BookLog, Entry, Op};
use seqaddr_core::validate::OpRequest;
use std::collections::{BTreeMap, BTreeSet};

const ENTRY_KEYS: [&str; 14] = ["n", "at", "by", "op", "addr", "tail", "from", "to", "body", "proposal", "cites", "outcome", "of", "state"];

struct OpenBlock {
    line: usize,
    n: Option<u64>,
    op: Op,
    addr: String,
    fields: BTreeMap<String, (usize, String)>,
    extra: serde_json::Map<String, serde_json::Value>,
    derived: Vec<Derived>,
    body: Option<Vec<String>>,
}

fn parse_op(word: &str, line: usize) -> Result<Op, PageError> {
    serde_json::from_value::<Op>(serde_json::Value::String(word.to_string()))
        .map_err(|_| PageError::invalid(line, "seqpage 6.1", format!("`{word}` is not an op (put, tail, snapshot, copy, note, merge, promote, use)")))
}

fn split_key(line: &str) -> Option<(&str, &str)> {
    let end = line.find(|c: char| !(c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-')).unwrap_or(line.len());
    if end == 0 || !line.as_bytes()[0].is_ascii_lowercase() {
        return None;
    }
    Some((&line[..end], &line[end..]))
}

fn val(raw: &str, line: usize, rule: &'static str) -> Result<String, PageError> {
    decode_value(raw).map_err(|e| PageError::invalid(line, rule, e))
}

impl OpenBlock {
    fn finish(self) -> Result<Block, PageError> {
        let line = self.line;
        let body = self.body.map(|v| v.join("\n"));
        let mut f = self.fields;
        let take = |f: &mut BTreeMap<String, (usize, String)>, k: &str| f.remove(k);
        let num = |v: Option<(usize, String)>| -> Result<Option<u64>, PageError> {
            match v {
                None => Ok(None),
                Some((l, s)) => s.parse::<u64>().map(Some).map_err(|_| PageError::invalid(l, "seqpage 6.3", format!("`{s}` is not a whole number"))),
            }
        };
        match self.n {
            Some(n) => {
                let at = take(&mut f, "at").ok_or_else(|| PageError::missing(line, "seqpage 6.2", format!("@{n} has no `at:` line; a booked entry keeps its time")))?.1;
                let by = take(&mut f, "by").ok_or_else(|| PageError::missing(line, "seqpage 6.2", format!("@{n} has no `by:` line; a booked entry keeps its author")))?.1;
                let mut e = Entry::new(n, at, by, self.op, self.addr);
                e.tail = take(&mut f, "tail").map(|x| x.1);
                e.from = take(&mut f, "from").map(|x| x.1);
                e.to = take(&mut f, "to").map(|x| x.1);
                e.proposal = take(&mut f, "proposal").map(|x| x.1);
                e.cites = num(take(&mut f, "cites"))?;
                e.outcome = take(&mut f, "outcome").map(|x| x.1);
                e.of = match num(take(&mut f, "of"))? {
                    Some(v) => Some(u32::try_from(v).map_err(|_| PageError::invalid(line, "seqpage 6.3", "`of` is too large"))?),
                    None => None,
                };
                if let Some((l, s)) = take(&mut f, "state") {
                    let v: serde_json::Value = serde_json::from_str(&s).map_err(|err| PageError::invalid(l, "seqpage 6.3", format!("`state:` is JSON: {err}")))?;
                    if let Some(ch) = crate::text::json_r4(&v) {
                        return Err(PageError::invalid(l, "R4", format!("`state:` holds {} through a JSON escape; stored text is plain ASCII only", crate::text::describe_char(ch))));
                    }
                    e.state = Some(v);
                }
                e.body = body;
                e.extra = self.extra;
                Ok(Block { line, kind: BlockKind::Booked(e), derived: self.derived })
            }
            None => {
                let o = OpRequest {
                    op: Some(self.op),
                    addr: self.addr,
                    tail: take(&mut f, "tail").map(|x| x.1),
                    from: take(&mut f, "from").map(|x| x.1),
                    to: take(&mut f, "to").map(|x| x.1),
                    body,
                    cites: num(take(&mut f, "cites"))?,
                    outcome: take(&mut f, "outcome").map(|x| x.1),
                };
                Ok(Block { line, kind: BlockKind::New(o), derived: self.derived })
            }
        }
    }
}

/// Read a `.seq` file. Stops at the first malformed line.
pub fn parse(text: &str) -> Result<SeqPage, PageError> {
    if let Some((l, c, ch)) = crate::text::first_non_r4(text) {
        return Err(PageError::invalid(l, "R4", format!("column {c}: {} is not allowed; a .seq file is plain ASCII 0x20-0x7E plus newline", crate::text::describe_char(ch))));
    }
    let body = text.strip_suffix('\n').unwrap_or(text);
    if body.is_empty() {
        return Err(PageError::missing(0, "seqpage 3", "empty file: no `seqpage 1` line and no door"));
    }
    let lines: Vec<&str> = body.split('\n').collect();
    if lines[0] != MAGIC {
        return Err(if lines[0].starts_with("seqpage ") {
            PageError::invalid(1, "seqpage 3", format!("`{}`: only `{MAGIC}` is known", lines[0]))
        } else {
            PageError::invalid(1, "seqpage 3", format!("the first line must be `{MAGIC}`"))
        });
    }
    let mut page: Option<PageId> = None;
    let mut sections: Vec<Section> = Vec::new();
    let mut history: Vec<HistLine> = Vec::new();
    let mut block: Option<OpenBlock> = None;
    let mut header_open = false;
    let mut in_history = false;
    let mut ended = false;

    fn close(block: &mut Option<OpenBlock>, sections: &mut [Section]) -> Result<(), PageError> {
        if let Some(b) = block.take() {
            let blk = b.finish()?;
            sections.last_mut().expect("block inside a section").blocks.push(blk);
        }
        Ok(())
    }

    for (idx, &l) in lines.iter().enumerate().skip(1) {
        let ln = idx + 1;
        if ended {
            return Err(PageError::invalid(ln, "seqpage 8", "nothing may follow `~ end`"));
        }
        if in_history {
            if l == "~ end" {
                ended = true;
                continue;
            }
            let rest = l.strip_prefix('@').ok_or_else(|| PageError::invalid(ln, "seqpage 8", "a history line is `@n op address`; the history ends with `~ end`"))?;
            let mut it = rest.splitn(3, ' ');
            let n = it.next().unwrap_or("");
            let n: u64 = n.parse().map_err(|_| PageError::invalid(ln, "seqpage 8", format!("`@{n}`: entry number must be a whole number")))?;
            let op = it.next().ok_or_else(|| PageError::invalid(ln, "seqpage 8", "history line has no op"))?;
            parse_op(op, ln)?;
            let addr = val(it.next().ok_or_else(|| PageError::invalid(ln, "seqpage 8", "history line has no address"))?, ln, "seqpage 8")?;
            history.push(HistLine { line: ln, n, op: op.to_string(), addr });
            continue;
        }
        if l.is_empty() {
            close(&mut block, &mut sections)?;
            header_open = false;
            continue;
        }
        if l == "~ history" {
            close(&mut block, &mut sections)?;
            if page.is_none() {
                return Err(PageError::missing(ln, "seqpage 4", "no door section `= 00 door DD.SS.BB.PPPP.00` before the history"));
            }
            in_history = true;
            continue;
        }
        if let Some(b) = body_line(l) {
            let text = b.map_err(|e| PageError::invalid(ln, "seqpage 6.4", e))?;
            let ob = block.as_mut().ok_or_else(|| PageError::invalid(ln, "seqpage 6.4", "a body line `|` must belong to a block (`--- ...`)"))?;
            ob.body.get_or_insert_with(Vec::new).push(text.to_string());
            continue;
        }
        if let Some(rest) = l.strip_prefix("= ") {
            close(&mut block, &mut sections)?;
            let mut it = rest.splitn(3, ' ');
            let (ff, name, addr) = (it.next().unwrap_or(""), it.next().unwrap_or(""), it.next().unwrap_or(""));
            if ff.len() != 2 || !ff.bytes().all(|c| c.is_ascii_digit()) || name.is_empty() || addr.is_empty() {
                return Err(PageError::invalid(ln, "seqpage 5", "a face header is `= FF name DD.SS.BB.PPPP.FF`"));
            }
            let face: u8 = ff.parse().unwrap();
            match page {
                None => {
                    if face != 0 {
                        return Err(PageError::missing(ln, "seqpage 4", "the file opens with the door: the first section must be `= 00 door DD.SS.BB.PPPP.00` (R1)"));
                    }
                    let p = Address::parse_full_page(addr).map_err(|e| PageError::invalid(ln, "seqpage 4", format!("door address: {e}")))?;
                    let fp = p.face.clone();
                    if fp.as_ref().map(|f| f.face != 0 || f.counter.is_some() || f.tail.is_some() || f.card.is_some()).unwrap_or(true) || p.title.is_some() {
                        return Err(PageError::invalid(ln, "seqpage 4", "the door header names the page's face 00: `DD.SS.BB.PPPP.00`"));
                    }
                    page = Some(PageId::new(p.book_id().unwrap(), p.page));
                }
                Some(_) => {
                    if face == 0 {
                        return Err(PageError::conflict(ln, "seqpage 4", "a second door section; a page has one door"));
                    }
                }
            }
            let key = SectionKey::face(face);
            if let Some(prev) = sections.last() {
                if key <= prev.key {
                    return Err(PageError::invalid(ln, "seqpage 5", format!("face {ff} is out of order or repeated; faces are written 00, 01, ... once each")));
                }
            }
            sections.push(Section { key, line: ln, name: Some(name.to_string()), addr: addr.to_string(), derived: vec![], blocks: vec![] });
            header_open = true;
            continue;
        }
        if let Some(rest) = l.strip_prefix("== ") {
            close(&mut block, &mut sections)?;
            let mut it = rest.splitn(2, ' ');
            let (fc, addr) = (it.next().unwrap_or(""), it.next().unwrap_or(""));
            let ok = fc.len() == 5 && fc.as_bytes()[2] == b'.' && fc.bytes().enumerate().all(|(i, c)| i == 2 || c.is_ascii_digit());
            if !ok || addr.is_empty() {
                return Err(PageError::invalid(ln, "seqpage 5.2", "a counter header is `== FF.NN DD.SS.BB.PPPP.FF.NN`"));
            }
            let face: u8 = fc[..2].parse().unwrap();
            let nn: u8 = fc[3..].parse().unwrap();
            let cur = sections.last().ok_or_else(|| PageError::missing(ln, "seqpage 4", "no door section before this counter"))?;
            if cur.key.face != face {
                return Err(PageError::missing(ln, "seqpage 5.2", format!("counter {fc} must sit under its face header `= {:02} ...`", face)));
            }
            let key = SectionKey::counter(face, nn);
            if key <= cur.key {
                return Err(PageError::invalid(ln, "seqpage 5.2", format!("counter {fc} is out of order or repeated")));
            }
            sections.push(Section { key, line: ln, name: None, addr: addr.to_string(), derived: vec![], blocks: vec![] });
            header_open = true;
            continue;
        }
        if let Some(rest) = l.strip_prefix("--- ") {
            close(&mut block, &mut sections)?;
            header_open = false;
            if sections.is_empty() {
                return Err(PageError::missing(ln, "seqpage 4", "a block before the door section"));
            }
            let mut it = rest.splitn(3, ' ');
            let (tag, op, addr) = (it.next().unwrap_or(""), it.next().unwrap_or(""), it.next().unwrap_or(""));
            if op.is_empty() || addr.is_empty() {
                return Err(PageError::invalid(ln, "seqpage 6.1", "a block header is `--- @n op address` or `--- new op address`"));
            }
            let n = if tag == "new" {
                None
            } else {
                let d = tag.strip_prefix('@').ok_or_else(|| PageError::invalid(ln, "seqpage 6.1", format!("`{tag}`: a block is `@n` (booked) or `new` (proposed)")))?;
                Some(d.parse::<u64>().map_err(|_| PageError::invalid(ln, "seqpage 6.1", format!("`{tag}`: entry number must be a whole number")))?)
            };
            let op = parse_op(op, ln)?;
            let addr = val(addr, ln, "seqpage 6.1")?;
            block = Some(OpenBlock { line: ln, n, op, addr, fields: BTreeMap::new(), extra: Default::default(), derived: vec![], body: None });
            continue;
        }
        if let Some((key, rest)) = split_key(l) {
            if let Some(v) = rest.strip_prefix(" := ") {
                let d = Derived { line: ln, key: key.to_string(), value: v.to_string() };
                if let Some(b) = block.as_mut() {
                    if b.body.is_some() {
                        return Err(PageError::invalid(ln, "seqpage 7", "a derived line comes before the body"));
                    }
                    b.derived.push(d);
                } else if header_open {
                    sections.last_mut().unwrap().derived.push(d);
                } else {
                    return Err(PageError::invalid(ln, "seqpage 7", "a derived line belongs right under a section header or a block header"));
                }
                continue;
            }
            if let Some(v) = rest.strip_prefix(": ") {
                let b = block.as_mut().ok_or_else(|| PageError::invalid(ln, "seqpage 6.2", format!("field `{key}:` outside a block")))?;
                if b.body.is_some() {
                    return Err(PageError::invalid(ln, "seqpage 6.2", "fields come before the body"));
                }
                let booked = b.n.is_some();
                let allowed_new = ["tail", "from", "to", "cites", "outcome"];
                let allowed_booked = ["at", "by", "tail", "from", "to", "proposal", "cites", "outcome", "of", "state", "x"];
                if !booked && !allowed_new.contains(&key) && allowed_booked.contains(&key) {
                    return Err(PageError::authority(ln, "seqpage 10", format!("`{key}:` is stamped by the compute when it books a write; a proposed block cannot carry it")));
                }
                if !(if booked { allowed_booked.contains(&key) } else { allowed_new.contains(&key) }) {
                    return Err(PageError::invalid(ln, "seqpage 6.2", format!("unknown field `{key}:`")));
                }
                if key == "x" {
                    let obj: serde_json::Map<String, serde_json::Value> =
                        serde_json::from_str(v).map_err(|e| PageError::invalid(ln, "seqpage 6.3", format!("`x:` is a JSON object with one key: {e}")))?;
                    if obj.len() != 1 {
                        return Err(PageError::invalid(ln, "seqpage 6.3", "`x:` holds exactly one extra field"));
                    }
                    let (k, xv) = obj.into_iter().next().unwrap();
                    if let Some(ch) = crate::text::json_r4(&serde_json::json!({ k.clone(): xv.clone() })) {
                        return Err(PageError::invalid(ln, "R4", format!("`x:` holds {} through a JSON escape; stored text is plain ASCII only", crate::text::describe_char(ch))));
                    }
                    if ENTRY_KEYS.contains(&k.as_str()) {
                        return Err(PageError::invalid(ln, "seqpage 6.3", format!("`x:` cannot carry the known field `{k}`")));
                    }
                    if b.extra.insert(k.clone(), xv).is_some() {
                        return Err(PageError::conflict(ln, "seqpage 6.3", format!("extra field `{k}` written twice")));
                    }
                    continue;
                }
                let value = if key == "state" { v.to_string() } else { val(v, ln, "seqpage 6.3")? };
                if b.fields.insert(key.to_string(), (ln, value)).is_some() {
                    return Err(PageError::conflict(ln, "seqpage 6.2", format!("field `{key}:` written twice in one block")));
                }
                continue;
            }
        }
        return Err(PageError::invalid(ln, "seqpage 3", format!("unrecognised line `{}`", l.chars().take(60).collect::<String>())));
    }
    if !ended {
        return Err(PageError::missing(lines.len(), "seqpage 8", "the file has no `~ end` line: it is cut off or unfinished"));
    }
    let page = page.ok_or_else(|| PageError::missing(0, "seqpage 4", "no door section"))?;
    Ok(SeqPage { page, sections, history })
}

/// Every rule a parsed file breaks (errors), plus findings.
pub fn check(sp: &SeqPage) -> Report {
    let mut errors = Vec::new();
    let mut findings = Vec::new();
    let page = sp.page;
    let booked = sp.booked();
    let d = derive(page, &booked);
    if let Some(r) = &d.replay_error {
        findings.push(PageError::invalid(0, "seqpage 7", format!("the page's own entries do not replay under the core's rules ({r}); derived state shows `7`")));
    }
    let mut seen: BTreeMap<u64, usize> = BTreeMap::new();
    for s in &sp.sections {
        // header address and name (8)
        let want = page.section_addr(s.key);
        if s.addr != want {
            errors.push(PageError::connection(s.line, "seqpage 5", format!("header address `{}` should be `{want}`", s.addr)));
        }
        if let Some(n) = &s.name {
            if n != s.key.name() {
                errors.push(PageError::connection(s.line, "seqpage 5", format!("face {:02} is `{}`, not `{n}`", s.key.face, s.key.name())));
            }
        }
        let expect: BTreeMap<&str, &String> = d.sections.get(&s.key).map(|v| v.iter().map(|(k, v)| (*k, v)).collect()).unwrap_or_default();
        for dl in &s.derived {
            match expect.get(dl.key.as_str()) {
                None => errors.push(PageError::invalid(dl.line, "seqpage 7", format!("`{} :=` is not a derived line of this section", dl.key))),
                Some(v) if **v != dl.value => errors.push(PageError::connection(
                    dl.line,
                    "seqpage 7",
                    format!("derived `{} := {}` disagrees with the entries (`{v}`); derived lines are never edited", dl.key, dl.value),
                )),
                _ => {}
            }
        }
        let mut last_n = 0u64;
        let mut seen_new = false;
        for b in &s.blocks {
            match slot_of(b.addr()) {
                None => errors.push(PageError::invalid(b.line, "seqpage 6.1", format!("`{}` is not a full face address DD.SS.BB.PPPP.FF", b.addr()))),
                Some((p, _)) if p != page => errors.push(PageError::connection(b.line, "seqpage 6.1", format!("`{}` is not on page {page}", b.addr()))),
                Some((_, k)) if k != s.key => errors.push(PageError::connection(
                    b.line,
                    "seqpage 5",
                    format!("`{}` belongs in section {}, not {}", b.addr(), page.section_addr(k), page.section_addr(s.key)),
                )),
                _ => {}
            }
            for dl in &b.derived {
                if dl.key != "cards" {
                    errors.push(PageError::invalid(dl.line, "seqpage 7", format!("`{} :=` is not a derived line of a block", dl.key)));
                } else if cards_value(s.key, b.body()).as_deref() != Some(dl.value.as_str()) {
                    errors.push(PageError::connection(dl.line, "seqpage 7", format!("`cards := {}` disagrees with the body's `##` cards", dl.value)));
                }
            }
            match &b.kind {
                BlockKind::Booked(e) => {
                    if seen_new {
                        errors.push(PageError::lineage(b.line, "seqpage 6.1", format!("@{} comes after a `new` block; booked history comes first, new writes are added after it", e.n)));
                    }
                    if let Some(first) = seen.insert(e.n, b.line) {
                        errors.push(PageError::conflict(b.line, "seqpage 6.1", format!("@{} is written twice (also line {first})", e.n)));
                    } else if e.n <= last_n {
                        errors.push(PageError::lineage(b.line, "seqpage 6.1", format!("@{} after @{last_n}: blocks keep book order; the past is not reordered", e.n)));
                    }
                    last_n = last_n.max(e.n);
                }
                BlockKind::New(_) => seen_new = true,
            }
        }
    }
    // history (8)
    let mut prev = 0u64;
    let mut hist: BTreeSet<u64> = BTreeSet::new();
    let by_n: BTreeMap<u64, &Entry> = booked.iter().map(|e| (e.n, e)).collect();
    for h in &sp.history {
        if h.n <= prev {
            errors.push(PageError::lineage(h.line, "seqpage 8", format!("history @{} after @{prev}: the history only grows, in book order", h.n)));
        }
        prev = prev.max(h.n);
        hist.insert(h.n);
        match by_n.get(&h.n) {
            None => errors.push(PageError::missing(h.line, "seqpage 8", format!("history names @{} but no block holds it", h.n))),
            Some(e) => {
                if e.op.as_str() != h.op || e.addr != h.addr {
                    errors.push(PageError::connection(h.line, "seqpage 8", format!("history line @{} says `{} {}`, the block says `{} {}`", h.n, h.op, h.addr, e.op.as_str(), e.addr)));
                }
            }
        }
    }
    for e in &booked {
        if !hist.contains(&e.n) {
            errors.push(PageError::missing(seen.get(&e.n).copied().unwrap_or(0), "seqpage 8", format!("@{} has no history line", e.n)));
        }
    }
    // the page's door (C1.1) - reported, not refused: the view shows the book as it is
    if !booked.iter().any(|e| slot_of(&e.addr).map(|(_, k)| k.is_door() && Address::parse_full_page(&e.addr).ok().and_then(|p| p.face).is_some()).unwrap_or(false))
        && !sp.proposed().iter().any(|o| slot_of(&o.addr).map(|(_, k)| k.is_door()).unwrap_or(false))
    {
        findings.push(PageError::missing(0, "seqpage 4", format!("page {page} has no face 00 (door) entry; C1.1 requires one")));
    }
    Report::new(errors, findings)
}

/// Check a file name against the page (seqpage.md 2).
pub fn check_file_name(name: &str, sp: &SeqPage) -> Option<PageError> {
    let base = name.rsplit('/').next().unwrap_or(name);
    let stem = match base.strip_suffix(".seq") {
        Some(s) => s,
        None => return Some(PageError::invalid(0, "seqpage 2", format!("`{base}` does not end in `.seq`"))),
    };
    let booked = sp.booked();
    let title = crate::write::derived_title(sp.page, &booked);
    let want = file_name(sp.page, title.as_deref());
    if base == want {
        return None;
    }
    let addr_part = sp.page.to_string();
    if !stem.starts_with(&addr_part) {
        return Some(PageError::connection(0, "seqpage 2", format!("file name `{base}` does not start with the page address {addr_part}")));
    }
    Some(PageError::elevate(0, "A2.8", format!("file name `{base}` does not match the door's title; expected `{want}`. A title in an address is checked against the stamp and a mismatch goes to the user")))
}

/// Parse and check text, optionally with its file name and the book it came from.
pub fn check_text(text: &str, name: Option<&str>, book: Option<&BookLog>) -> Report {
    let sp = match parse(text) {
        Ok(sp) => sp,
        Err(e) => return Report::new(vec![e], vec![]),
    };
    let mut r = check(&sp);
    if let Some(n) = name {
        if let Some(e) = check_file_name(n, &sp) {
            r.errors.push(e);
        }
    }
    if let Some(log) = book {
        let (e, f) = crate::import::compare_with_book(&sp, log);
        r.errors.extend(e);
        r.findings.extend(f);
    }
    r.ok = r.errors.is_empty();
    r
}
