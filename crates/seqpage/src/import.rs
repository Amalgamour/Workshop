//! Import (seqpage.md 10): a `.seq` file becomes a **proposal**. Nothing is
//! written. Booked blocks are history and must match the book exactly
//! (axiom 6: the past is not rewritten); `new` blocks become the proposal's
//! ops, which the compute validates and books like any other write (R3).

use crate::error::{PageError, Report};
use crate::model::{page_entries, PageId, SeqPage};
use crate::parse::{check, parse};
use seqaddr_core::log::{BookLog, Entry};
use seqaddr_core::validate::Proposal;
use serde::Serialize;
use std::collections::BTreeMap;

#[derive(Debug, Clone, Serialize)]
pub struct Imported {
    pub page: String,
    /// Entry numbers of the booked blocks (already in the book).
    pub booked: Vec<u64>,
    /// The proposal for `POST /propose` (lane contract): `{"by","ops"}`.
    pub proposal: Proposal,
    pub findings: Vec<PageError>,
    #[serde(skip)]
    pub page_id: Option<PageId>,
    #[serde(skip)]
    pub entries: Vec<Entry>,
}

/// Compare the file's booked blocks with the book (errors, findings).
pub fn compare_with_book(sp: &SeqPage, log: &BookLog) -> (Vec<PageError>, Vec<PageError>) {
    let mut errors = Vec::new();
    let mut findings = Vec::new();
    if log.header.address != sp.page.book.to_string() {
        errors.push(PageError::connection(0, "seqpage 10", format!("page {} is not in book {}", sp.page, log.header.address)));
        return (errors, findings);
    }
    let book: BTreeMap<u64, &Entry> = log.entries.iter().map(|e| (e.n, e)).collect();
    let mut line_of: BTreeMap<u64, usize> = BTreeMap::new();
    for s in &sp.sections {
        for b in &s.blocks {
            if let crate::model::BlockKind::Booked(e) = &b.kind {
                line_of.insert(e.n, b.line);
            }
        }
    }
    let file = sp.booked();
    for e in &file {
        let line = line_of.get(&e.n).copied().unwrap_or(0);
        match book.get(&e.n) {
            None => errors.push(PageError::missing_link(line, "seqpage 10", format!("@{} is not in book {}; a booked block must point at a real entry", e.n, log.header.address))),
            Some(b) if *b != e => errors.push(PageError::lineage(line, "seqpage 10", format!("@{} differs from the book's entry; the past is not rewritten (change it with a `new` block)", e.n))),
            _ => {}
        }
    }
    let have: std::collections::BTreeSet<u64> = file.iter().map(|e| e.n).collect();
    let behind: Vec<String> = page_entries(log, sp.page).iter().filter(|e| !have.contains(&e.n)).map(|e| format!("@{}", e.n)).collect();
    if !behind.is_empty() {
        findings.push(PageError::missing(0, "seqpage 10", format!("the book has newer entries for this page not in the file ({}); the file is behind - export again", behind.join(" "))));
    }
    (errors, findings)
}

/// Turn a `.seq` file into a proposal. With `book`, booked blocks are checked
/// against it. `by` is the proposer (the compute stamps `at`, `n`, `proposal`).
pub fn import(text: &str, book: Option<&BookLog>, by: &str) -> Result<Imported, Report> {
    let sp = parse(text).map_err(|e| Report::new(vec![e], vec![]))?;
    let mut r = check(&sp);
    if let Some(log) = book {
        let (e, f) = compare_with_book(&sp, log);
        r.errors.extend(e);
        r.findings.extend(f);
    }
    if by.trim().is_empty() {
        r.errors.push(PageError::missing(0, "seqpage 10", "a proposal names its author (`by`)"));
    }
    if !r.errors.is_empty() {
        r.ok = false;
        return Err(r);
    }
    let ops = sp.proposed();
    if ops.is_empty() {
        r.findings.push(PageError::invalid(0, "seqpage 10", "no `new` blocks: nothing to propose"));
    }
    let entries = sp.booked();
    Ok(Imported {
        page: sp.page.to_string(),
        booked: entries.iter().map(|e| e.n).collect(),
        proposal: Proposal { by: by.to_string(), ops },
        findings: r.findings,
        page_id: Some(sp.page),
        entries,
    })
}
