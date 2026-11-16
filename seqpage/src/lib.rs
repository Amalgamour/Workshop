//! A `.seq` file is a view of one page. The book stays the real copy.
//! This follows SEQ-GUIDE.md. The spec it names is not in this repo.

use std::collections::BTreeMap;
use std::path::Path;

use seqbook::{read_writes, Book, LogWrite};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Fault {
    pub line: usize,
    pub detail: String,
}

pub fn export(book: &Path, page: &str) -> Result<String, seqbook::Error> {
    let loaded = Book::load(book)?;
    let writes = read_writes(book)?;
    let page_writes: Vec<&LogWrite> = writes
        .iter()
        .filter(|write| write.addr.starts_with(&format!("{page}.")))
        .collect();
    let mut by_face: BTreeMap<String, Vec<&LogWrite>> = BTreeMap::new();
    for write in page_writes {
        by_face.entry(write.addr.clone()).or_default().push(write);
    }
    let stamp_key = format!("{page}.00");
    let stamp = loaded.face(&stamp_key)?.map(|face| face.body);
    let mut out = String::from("seqpage 1\n");
    if by_face.is_empty() {
        out.push_str("~ history\n~ end\n");
        return Ok(out);
    }
    let book_id = loaded.address().canonical();
    for (addr, face_writes) in &by_face {
        let role = face_role(addr);
        out.push_str(&format!("= {role} {addr}\n"));
        if addr == &stamp_key {
            if let Some(body) = &stamp {
                derived(&mut out, page, body, &book_id, face_writes, &by_face);
            }
        } else if let Some(first) = face_writes.iter().find(|write| write.op == "put") {
            out.push_str(&format!("source := book {book_id} @{}\n", first.n));
        }
        out.push('\n');
        for write in face_writes {
            block(&mut out, write);
            out.push('\n');
        }
    }
    out.push_str("~ history\n");
    let mut flat: Vec<&LogWrite> = by_face.values().flatten().copied().collect();
    flat.sort_by_key(|write| write.n);
    for write in flat {
        out.push_str(&format!("@{} {} {}\n", write.n, write.op, write.addr));
    }
    out.push_str("~ end\n");
    Ok(out)
}

pub fn file_name(page: &str, title: Option<&str>) -> String {
    match title {
        Some(title) if !title.is_empty() => format!("{page}.{title}.seq"),
        _ => format!("{page}.seq"),
    }
}

/// Compare a view to its book. A difference in a booked block is a fault. Nothing is written.
pub fn check(text: &str, book: &Path) -> Result<Vec<Fault>, seqbook::Error> {
    let writes = read_writes(book)?;
    let by_n: BTreeMap<u64, &LogWrite> = writes.iter().map(|write| (write.n, write)).collect();
    let mut faults = Vec::new();
    let lines: Vec<&str> = text.split('\n').collect();
    let last = lines.iter().rposition(|line| !line.is_empty()).unwrap_or(0);
    if !text.lines().any(|line| line.starts_with("= 00 ")) {
        faults.push(Fault {
            line: 1,
            detail: "face 00 comes first".into(),
        });
    }
    if lines.first().copied().unwrap_or("") != "seqpage 1" {
        faults.push(Fault {
            line: 1,
            detail: "line 1 must be seqpage 1".into(),
        });
    }
    if lines.get(last).copied().unwrap_or("") != "~ end" {
        faults.push(Fault {
            line: last + 1,
            detail: "the last line must be ~ end".into(),
        });
    }
    for (index, line) in lines.iter().enumerate().take(last + 1) {
        if let Some(column) = bad_char(line) {
            faults.push(Fault {
                line: index + 1,
                detail: format!("column {column}: a .seq file is plain ASCII 0x20-0x7E plus newline"),
            });
        }
    }
    let mut saw_face = false;
    let mut history = false;
    let mut blocks: Vec<(usize, u64, String, String, Vec<String>)> = Vec::new();
    let mut history_lines: Vec<(usize, String)> = Vec::new();
    let mut index = 0;
    while index < lines.len() {
        let line = lines[index];
        if line.starts_with("= ") {
            if !saw_face && !line.starts_with("= 00 ") {
                faults.push(Fault {
                    line: index + 1,
                    detail: "face 00 comes first".into(),
                });
            }
            saw_face = true;
            history = false;
        } else if let Some(rest) = line.strip_prefix("--- @") {
            let header = parse_block_header(rest);
            let start = index + 1;
            index += 1;
            let mut fields: Vec<&str> = Vec::new();
            let mut body: Vec<String> = Vec::new();
            while index < lines.len() {
                let row = lines[index];
                if row.starts_with("--- ") || row.starts_with("= ") || row.starts_with('~') {
                    break;
                }
                if let Some(text) = row.strip_prefix("| ") {
                    body.push(text.to_string());
                } else if row == "|" {
                    body.push(String::new());
                } else if !row.is_empty() && !row.contains(" := ") {
                    fields.push(row);
                }
                index += 1;
            }
            if let Some((n, op, addr)) = header {
                blocks.push((start, n, op, addr, body));
                let _ = fields;
            } else {
                faults.push(Fault {
                    line: start,
                    detail: "a block does not start with @n op address".into(),
                });
            }
            continue;
        } else if line == "~ history" {
            history = true;
        } else if history && line.starts_with('@') {
            history_lines.push((index + 1, line.to_string()));
        }
        index += 1;
    }
    for (line, n, op, addr, body) in &blocks {
        let Some(write) = by_n.get(n) else {
            faults.push(Fault {
                line: *line,
                detail: format!("@{n} is not in the book"),
            });
            continue;
        };
        if write.op != *op || write.addr != *addr {
            faults.push(Fault {
                line: *line,
                detail: format!("@{n} differs from the book's entry; the past is not rewritten"),
            });
            continue;
        }
        if write.op == "put" {
            let decoded = decode_body(body);
            if write.body.as_deref().unwrap_or("") != decoded {
                faults.push(Fault {
                    line: *line,
                    detail: format!("@{n} differs from the book's entry; the past is not rewritten"),
                });
            }
        }
    }
    let mut expected: Vec<(u64, String)> = blocks
        .iter()
        .map(|(_, n, op, addr, _)| (*n, format!("@{n} {op} {addr}")))
        .collect();
    expected.sort_by_key(|(n, _)| *n);
    let got: Vec<String> = history_lines.iter().map(|(_, line)| line.clone()).collect();
    let expected: Vec<String> = expected.into_iter().map(|(_, line)| line).collect();
    if expected != got {
        faults.push(Fault {
            line: history_lines.first().map(|(line, _)| *line).unwrap_or(1),
            detail: "the history does not match the booked blocks".into(),
        });
    }
    Ok(faults)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RequestOp {
    pub op: String,
    pub addr: String,
    pub body: String,
}

/// Read `new` blocks as a request. This does not write a book.
pub fn import_request(text: &str) -> (Vec<RequestOp>, Vec<Fault>) {
    let lines: Vec<&str> = text.split('\n').collect();
    let mut ops = Vec::new();
    let mut faults = Vec::new();
    let mut saw_new = false;
    let mut index = 0;
    while index < lines.len() {
        let line = lines[index];
        if let Some(rest) = line.strip_prefix("--- @") {
            if saw_new && parse_block_header(rest).is_some() {
                faults.push(Fault {
                    line: index + 1,
                    detail: "a new block comes after the booked blocks".into(),
                });
            }
        } else if let Some(rest) = line.strip_prefix("--- new ") {
            saw_new = true;
            let mut parts = rest.split_whitespace();
            let op = parts.next().unwrap_or("").to_string();
            let addr = parts.next().unwrap_or("").to_string();
            index += 1;
            let mut body = Vec::new();
            while index < lines.len() {
                let row = lines[index];
                if row.starts_with("--- ") || row.starts_with("= ") || row.starts_with('~') {
                    break;
                }
                if let Some(text) = row.strip_prefix("| ") {
                    body.push(text.to_string());
                } else if row == "|" {
                    body.push(String::new());
                }
                index += 1;
            }
            if op.is_empty() || addr.is_empty() {
                faults.push(Fault {
                    line: index,
                    detail: "a new block needs an operation and an address".into(),
                });
            } else {
                ops.push(RequestOp {
                    op,
                    addr,
                    body: decode_body(&body),
                });
            }
            continue;
        }
        index += 1;
    }
    if ops.is_empty() {
        faults.push(Fault {
            line: 0,
            detail: "no new blocks: nothing to propose".into(),
        });
    }
    (ops, faults)
}

pub fn check_name(name: &str, text: &str) -> Vec<Fault> {
    let stem = name.strip_suffix(".seq").unwrap_or(name);
    let title_in_name = stem.rsplit_once('.').and_then(|(head, tail)| {
        if tail.chars().all(|ch| ch.is_ascii_digit()) {
            None
        } else if head.rsplit_once('.').is_some() {
            Some(tail)
        } else {
            None
        }
    });
    let title_in_file = text.lines().find_map(|line| {
        line.strip_prefix("title := ")
            .map(str::trim)
            .filter(|title| !title.is_empty() && *title != "7")
    });
    match (title_in_name, title_in_file) {
        (Some(name_title), Some(file_title)) if name_title != file_title => vec![Fault {
            line: 1,
            detail: format!("the name says {name_title} and the stamp says {file_title}"),
        }],
        _ => Vec::new(),
    }
}

fn derived(
    out: &mut String,
    page: &str,
    stamp: &str,
    book_id: &str,
    writes: &[&LogWrite],
    faces: &BTreeMap<String, Vec<&LogWrite>>,
) {
    let title = field(stamp, "title").unwrap_or_else(|| "7".to_string());
    let state = field(stamp, "state").unwrap_or_else(|| "7".to_string());
    let kind = field(stamp, "type").unwrap_or_else(|| "7".to_string());
    let axioms = field(stamp, "axioms").unwrap_or_else(|| "-".to_string());
    out.push_str(&format!("title := {title}\n"));
    out.push_str(&format!("state := {state}\n"));
    out.push_str(&format!("type := {kind}\n"));
    out.push_str(&format!("axioms := {axioms}\n"));
    let prefix = format!("{page}.");
    let list = faces
        .keys()
        .filter_map(|addr| addr.strip_prefix(&prefix))
        .filter(|tail| *tail != "00")
        .collect::<Vec<_>>()
        .join(", ");
    if list.is_empty() {
        out.push_str("faces := -\n");
    } else {
        out.push_str(&format!("faces := {list}\n"));
    }
    if let Some(first) = writes.iter().find(|write| write.op == "put") {
        out.push_str(&format!("source := book {book_id} @{}\n", first.n));
    }
}

fn block(out: &mut String, write: &LogWrite) {
    out.push_str(&format!("--- @{} {} {}\n", write.n, write.op, write.addr));
    out.push_str(&format!("at: {}\n", write.at));
    out.push_str(&format!("by: {}\n", write.by));
    if let Some(tail) = &write.tail {
        out.push_str(&format!("tail: {tail}\n"));
    }
    if let Some(from) = &write.from {
        out.push_str(&format!("from: {from}\n"));
    }
    if let Some(to) = &write.to {
        out.push_str(&format!("to: {to}\n"));
    }
    if let Some(body) = &write.body {
        out.push_str(&encode_body(body));
    }
}

fn encode_body(body: &str) -> String {
    if body.is_empty() {
        return String::new();
    }
    let mut out = String::new();
    let parts: Vec<&str> = body.split('\n').collect();
    let end = if body.ends_with('\n') { parts.len() - 1 } else { parts.len() };
    for line in parts.iter().take(end) {
        if line.is_empty() {
            out.push_str("|\n");
        } else {
            out.push_str("| ");
            out.push_str(line);
            out.push('\n');
        }
    }
    out
}

fn decode_body(lines: &[String]) -> String {
    if lines.is_empty() {
        return String::new();
    }
    let mut out = lines.join("\n");
    out.push('\n');
    out
}

fn field(body: &str, key: &str) -> Option<String> {
    let prefix = format!("{key}:");
    for line in body.lines() {
        if line.trim().is_empty() {
            break;
        }
        if let Some(value) = line.trim().strip_prefix(&prefix) {
            let value = value.trim();
            if !value.is_empty() {
                return Some(value.to_string());
            }
        }
    }
    None
}

fn face_role(addr: &str) -> String {
    let face = addr.split('.').nth(4).unwrap_or("");
    let name = match face {
        "00" => "registry",
        "01" => "law",
        "02" => "schema",
        "03" => "operate",
        "04" => "why",
        "05" => "tasks",
        "06" => "notes",
        "07" => "reserved",
        "08" => "map",
        "09" => "unassigned",
        _ => "face",
    };
    format!("{face} {name}")
}

fn parse_block_header(rest: &str) -> Option<(u64, String, String)> {
    let mut parts = rest.split_whitespace();
    let n: u64 = parts.next()?.parse().ok()?;
    let op = parts.next()?.to_string();
    let addr = parts.next()?.to_string();
    Some((n, op, addr))
}

fn bad_char(line: &str) -> Option<usize> {
    for (index, ch) in line.chars().enumerate() {
        let ok = ch.is_ascii() && (ch == '\n' || (('\u{20}'..='\u{7e}').contains(&ch)));
        if !ok {
            return Some(index + 1);
        }
    }
    None
}
