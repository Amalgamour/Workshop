//! The local compute. It reads a book through the core, and it appends a put
//! only after the why rule and the page shape still hold.

pub mod http;

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

use seqbook::{page_gaps, why_gaps, Book, Writer};

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Verdict {
    Read { body: String },
    Accept { len: usize },
    Refuse { reasons: Vec<String> },
}

const PROPOSE_AT: &str = "2026-11-11T21:10:00Z";

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Proposal {
    pub proposer: &'static str,
    pub addr: String,
    pub title: Option<String>,
    pub body: String,
    pub verdict: Verdict,
}

/// A local proposer. It is not a remote model. `law:` proposes a 01 card with no why.
pub fn propose_sentence(book: &Path, sentence: &str) -> Result<Proposal, seqbook::Error> {
    let sentence = sentence.trim();
    if sentence.is_empty() {
        return Ok(local_proposal(
            String::new(),
            None,
            String::new(),
            Verdict::Refuse {
                reasons: vec!["the sentence is empty".to_string()],
            },
        ));
    }
    let loaded = Book::load(book)?;
    let book_id = loaded.address().canonical();
    if let Some(rest) = sentence.strip_prefix("law:") {
        let addr = format!("{book_id}.1002.01");
        let body = format!("## demo\ntype: rule\n\n{}\n", rest.trim());
        let verdict = propose_put(book, PROPOSE_AT, "local-proposer", &addr, &body)?;
        return Ok(local_proposal(
            addr.clone(),
            page_title(&loaded, &addr).ok().flatten(),
            body,
            verdict,
        ));
    }
    let stamp = format!("{book_id}.1001.00");
    if !loaded.faces().iter().any(|face| face.key == stamp) {
        return Ok(local_proposal(
            stamp,
            None,
            String::new(),
            Verdict::Refuse {
                reasons: vec!["page 1001 has no stamp, so a note cannot land".to_string()],
            },
        ));
    }
    let addr = next_note(&loaded, &book_id);
    let body = format!("## note\ntype: note\naxioms: 5\nproposer: local\n\n{sentence}\n");
    let verdict = propose_put(book, PROPOSE_AT, "local-proposer", &addr, &body)?;
    let title = page_title(&loaded, &addr).ok().flatten();
    Ok(local_proposal(addr, title, body, verdict))
}

fn local_proposal(addr: String, title: Option<String>, body: String, verdict: Verdict) -> Proposal {
    Proposal {
        proposer: "local",
        addr,
        title,
        body,
        verdict,
    }
}

/// The page title is the `title` field on face 00. A face has no title of its own.
pub fn page_title(book: &Book, addr: &str) -> Result<Option<String>, seqbook::Error> {
    let ctx = seqbook::Context::new(Some(book.address()), Vec::new());
    let seqbook::Address::Page(page) = seqbook::resolve(addr, &ctx)? else {
        return Ok(None);
    };
    let stamp = format!("{}.{:04}.00", page.id.canonical(), page.page);
    let Some(face) = book.face(&stamp)? else {
        return Ok(None);
    };
    Ok(stamp_title(&face.body))
}

fn stamp_title(body: &str) -> Option<String> {
    for line in body.lines() {
        if line.trim().is_empty() {
            break;
        }
        if let Some(value) = line.trim().strip_prefix("title:") {
            let value = value.trim();
            if !value.is_empty() {
                return Some(value.to_string());
            }
        }
    }
    None
}

const BANDS: &[(u16, u16, &str, &str)] = &[
    (0, 99, "0000-0099", "kernel"),
    (100, 299, "0100-0299", "unassigned"),
    (300, 399, "0300-0399", "build"),
    (400, 499, "0400-0499", "dev"),
    (500, 599, "0500-0599", "jobs"),
    (600, 699, "0600-0699", "unassigned"),
    (700, 799, "0700-0799", "colab"),
    (800, 999, "0800-0999", "unassigned"),
    (1000, 9999, "1000-9998", "user"),
];

/// Every page and face, grouped by the workflow bands. Empty bands stay in the list.
pub fn catalog(book: &Book) -> String {
    let faces = book.faces();
    let mut pages: BTreeMap<u16, Vec<&seqbook::FaceAt>> = BTreeMap::new();
    for face in &faces {
        if let Some(page) = page_number(&face.key) {
            pages.entry(page).or_default().push(face);
        }
    }
    let book_id = book.address().canonical();
    let mut out = format!("book: {book_id}\nlen: {}\n", book.len());
    for (start, end, id, name) in BANDS {
        out.push_str(&format!("band: {id} {name}\n"));
        for (page, page_faces) in pages.range(start..=end) {
            let page_addr = format!("{book_id}.{page:04}");
            let title = page_faces
                .iter()
                .find(|face| face.key == format!("{page_addr}.00"))
                .and_then(|face| stamp_title(&face.body));
            match title {
                Some(title) => out.push_str(&format!("page: {page_addr} title: {title}\n")),
                None => out.push_str(&format!("page: {page_addr}\n")),
            }
            for face in page_faces {
                match face.tail {
                    Some(tail) => {
                        out.push_str(&format!("face: {} tail: {}\n", face.key, tail.as_str()));
                    }
                    None => out.push_str(&format!("face: {}\n", face.key)),
                }
            }
        }
    }
    out
}

fn page_number(key: &str) -> Option<u16> {
    key.split('.').nth(3)?.parse().ok()
}

fn next_note(book: &Book, book_id: &str) -> String {
    let prefix = format!("{book_id}.1001.06.");
    let keys: BTreeSet<String> = book.faces().into_iter().map(|face| face.key).collect();
    for counter in 1..99 {
        let addr = format!("{prefix}{counter:02}");
        if !keys.contains(&addr) {
            return addr;
        }
    }
    format!("{prefix}98")
}

pub fn read_face(book: &Path, addr: &str) -> Result<Verdict, seqbook::Error> {
    let loaded = Book::load(book)?;
    match loaded.face(addr)? {
        Some(face) => Ok(Verdict::Read { body: face.body }),
        None => Ok(Verdict::Refuse {
            reasons: vec![format!("missing {addr}")],
        }),
    }
}

/// Try a put on a copy. The real book gains a line only when no new hard gap appears.
pub fn propose_put(
    book: &Path,
    at: &str,
    by: &str,
    addr: &str,
    body: &str,
) -> Result<Verdict, seqbook::Error> {
    let before = Book::load(book)?;
    let before_gaps = hard_gaps(&before);
    let scratch = scratch_copy(book)?;
    if let Err(err) = put_on(&scratch, at, by, addr, body) {
        let _ = fs::remove_file(&scratch);
        return Ok(Verdict::Refuse {
            reasons: vec![err.to_string()],
        });
    }
    let after = Book::load(&scratch)?;
    let introduced: Vec<String> = hard_gaps(&after)
        .difference(&before_gaps)
        .cloned()
        .collect();
    let _ = fs::remove_file(&scratch);
    if !introduced.is_empty() {
        return Ok(Verdict::Refuse { reasons: introduced });
    }
    put_on(book, at, by, addr, body)?;
    let loaded = Book::load(book)?;
    Ok(Verdict::Accept { len: loaded.len() })
}

fn put_on(book: &Path, at: &str, by: &str, addr: &str, body: &str) -> Result<(), seqbook::Error> {
    let mut writer = Writer::open(book)?;
    writer.put(at, by, addr, body, None)
}

fn hard_gaps(book: &Book) -> BTreeSet<String> {
    let why = why_gaps(book);
    why.hard.into_iter().chain(page_gaps(book)).collect()
}

fn scratch_copy(book: &Path) -> Result<PathBuf, seqbook::Error> {
    let name = format!(
        "compute-{}-{}.book",
        std::process::id(),
        book.file_name().and_then(|n| n.to_str()).unwrap_or("book")
    );
    let path = std::env::temp_dir().join(name);
    fs::copy(book, &path).map_err(|err| seqbook::Error::Io(err.to_string()))?;
    Ok(path)
}
