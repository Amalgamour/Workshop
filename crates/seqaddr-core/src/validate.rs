//! Proposal validation (format 4.1). A proposal is a list of ops applied all
//! or nothing (format 3.3, proposed). Hard failures reject it with reasons;
//! findings are recorded for review and do not reject.

use crate::addr::{Address, BookId, PageAddr, Tail};
use crate::axioms::AxiomChain;
use crate::cards::{parse_face, parse_stamp};
use crate::error::SeqError;
use crate::face::{card_type, is_active_face, is_page_type};
use crate::log::{Entry, Op};
use crate::resolve::World;
use crate::state::BookState;
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

/// One requested op: an entry without `n`, `at`, `by` (lane contract `POST /propose`).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct OpRequest {
    pub op: Option<Op>,
    pub addr: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tail: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub from: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub to: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub body: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cites: Option<u64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub outcome: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Proposal {
    pub by: String,
    pub ops: Vec<OpRequest>,
}

/// Why a proposal was rejected, or a finding on it.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Reason {
    pub code: String,
    pub rule: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub axiom: Option<String>,
    pub detail: String,
    /// Index of the op it concerns, if one.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub op: Option<usize>,
}

impl Reason {
    pub fn from_error(e: &SeqError, op: Option<usize>) -> Self {
        Reason { code: e.code().into(), rule: e.rule().into(), axiom: e.axiom().map(|s| s.into()), detail: e.detail(), op }
    }
    fn finding(rule: &str, detail: impl Into<String>) -> Self {
        Reason { code: "finding".into(), rule: rule.into(), axiom: None, detail: detail.into(), op: None }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Status {
    Approved,
    Rejected,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Outcome {
    pub status: Status,
    pub reasons: Vec<Reason>,
    pub findings: Vec<Reason>,
    /// The entries to append (empty when rejected).
    #[serde(skip)]
    pub entries: Vec<Entry>,
    /// Entry numbers that would be appended.
    #[serde(rename = "entries")]
    pub entry_numbers: Vec<u64>,
    /// The state after applying, when approved.
    #[serde(skip)]
    pub state: Option<BookState>,
}

impl Outcome {
    pub fn approved(&self) -> bool {
        self.status == Status::Approved
    }
    pub fn first_error_code(&self) -> Option<&str> {
        self.reasons.first().map(|r| r.code.as_str())
    }
}

fn reject(reasons: Vec<Reason>, findings: Vec<Reason>) -> Outcome {
    Outcome { status: Status::Rejected, reasons, findings, entries: vec![], entry_numbers: vec![], state: None }
}

/// The book a request writes to: the book of its address (full form required, A1.7).
pub fn target_book(req: &OpRequest) -> Result<BookId, SeqError> {
    let p = Address::parse_full_page(&req.addr)?;
    Ok(p.book_id().unwrap())
}

/// Validate a proposal against `world` (all ops must target the same book).
/// `at` is the time stamped on every entry. Nothing in `world` is changed:
/// on approval the caller appends `outcome.entries` and stores `outcome.state`.
pub fn validate(world: &World, proposal: &Proposal, at: &str) -> Outcome {
    let policy = &world.policy;
    let mut reasons = Vec::new();
    let mut findings = Vec::new();
    if proposal.ops.is_empty() {
        return reject(vec![Reason::from_error(&SeqError::rejected("format 3.3", "a proposal holds at least one op"), None)], findings);
    }
    if proposal.by.trim().is_empty() {
        return reject(vec![Reason::from_error(&SeqError::rejected("format 3.2", "a proposal names its author (`by`)"), None)], findings);
    }
    // 1. addresses are well formed, full, and in one book
    let mut book: Option<BookId> = None;
    for (i, r) in proposal.ops.iter().enumerate() {
        match target_book(r) {
            Ok(b) => match book {
                None => book = Some(b),
                Some(x) if x != b => reasons.push(Reason::from_error(
                    &SeqError::rejected("workflow-loop.003 10", format!("op {i} writes {b} but the proposal writes {x}; cross-book proposals are not designed (7)")),
                    Some(i),
                )),
                _ => {}
            },
            Err(e) => reasons.push(Reason::from_error(&e, Some(i))),
        }
        if r.op.is_none() {
            reasons.push(Reason::from_error(&SeqError::invalid("format 3.3", "op is missing"), Some(i)));
        }
        if r.op == Some(Op::Snapshot) {
            reasons.push(Reason::from_error(&SeqError::rejected("format 3.4", "snapshots are written by the compute, not proposed"), Some(i)));
        }
    }
    if !reasons.is_empty() {
        return reject(reasons, findings);
    }
    let book = book.unwrap();
    let mut st = world.get(book).cloned().unwrap_or_else(|| BookState::new(book));
    let first_n = st.last_n + 1;
    let pid = format!("p{first_n}");
    let multi = proposal.ops.len() > 1;
    let mut entries = Vec::new();
    let mut touched: BTreeSet<u16> = BTreeSet::new();
    for (i, r) in proposal.ops.iter().enumerate() {
        let mut e = Entry::new(st.last_n + 1, at, proposal.by.clone(), r.op.unwrap(), r.addr.clone());
        e.tail = r.tail.clone();
        e.from = r.from.clone();
        e.to = r.to.clone();
        e.body = r.body.clone();
        e.cites = r.cites.clone();
        e.outcome = r.outcome.clone();
        if multi {
            e.proposal = Some(pid.clone());
            e.of = Some(proposal.ops.len() as u32);
        }
        // reserved faces (A4.3)
        if let Ok(p) = Address::parse_full_page(&r.addr) {
            if let Some(fp) = &p.face {
                if !is_active_face(fp.face) {
                    reasons.push(Reason::from_error(&SeqError::rejected("A4.3", format!("face {:02} is reserved and not active", fp.face)), Some(i)));
                    continue;
                }
                // compute-only fields (C8.7, C8.9)
                if let Some(b) = &r.body {
                    if proposal.by != policy.compute_name {
                        if let Ok(doc) = parse_face(b) {
                            for c in &doc.cards {
                                let ty = c.card_type(fp.face).unwrap_or_default();
                                if let Some(ct) = card_type(&ty) {
                                    for f in ct.compute_fields {
                                        if c.field(f).is_some() {
                                            reasons.push(Reason::from_error(&SeqError::rejected("C8.7", format!("card `{}`: `{f}` is written only by the compute", c.key)), Some(i)));
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            touched.insert(p.page);
        }
        match st.apply(&e, policy) {
            Ok(()) => entries.push(e),
            Err(err) => reasons.push(Reason::from_error(&err, Some(i))),
        }
    }
    if !reasons.is_empty() {
        return reject(reasons, findings);
    }
    // 2. page-level checks on every touched page
    for &pg in &touched {
        check_page(world, &st, pg, &mut reasons, &mut findings);
    }
    if !reasons.is_empty() {
        return reject(reasons, findings);
    }
    let nums = entries.iter().map(|e| e.n).collect();
    Outcome { status: Status::Approved, reasons, findings, entries, entry_numbers: nums, state: Some(st) }
}

fn hard(reasons: &mut Vec<Reason>, e: SeqError) {
    reasons.push(Reason::from_error(&e, None));
}

fn check_page(world: &World, st: &BookState, pg: u16, reasons: &mut Vec<Reason>, findings: &mut Vec<Reason>) {
    let policy = &world.policy;
    let Some(page) = st.page(pg) else { return };
    // C1.1
    if pg != 0 || policy.c1_on_identity_pages {
        if let Err(e) = page.check_c1(pg) {
            hard(reasons, e);
        }
    }
    // stamp: page type (C1.4), title rules (A2.3, A2.8)
    if let Some(f0) = page.face(0).and_then(|f| f.view()) {
        let stamp = parse_stamp(f0);
        if let Some(t) = stamp.page_type() {
            if !is_page_type(t) {
                hard(reasons, SeqError::rejected("C1.4", format!("page {pg:04}: unknown page type `{t}` (system, general, code, workflow, band, pointer)")));
            }
        }
        if let Some(t) = stamp.title() {
            if let Err(e) = crate::addr::check_title(t) {
                hard(reasons, e);
            }
        }
        if pg >= 1000 && pg != 9999 && stamp.title().is_none() && page.tail() != crate::tail::PageTail::Retired {
            hard(reasons, SeqError::rejected("A2.8", format!("page {pg:04}: pages 1000 and up must have a title in the stamp")));
        }
        if let Some(ax) = stamp.get("axioms") {
            if let Err(e) = AxiomChain::parse(ax) {
                hard(reasons, e);
            }
        }
    }
    // C6: face 03 in normal books only on reserved pages 0001-0099
    if page.face(3).map(|f| f.is_present()).unwrap_or(false) && !st.book.is_kernel_or_desk_book() && !(1..=99).contains(&pg) {
        hard(reasons, SeqError::rejected("C6", format!("page {pg:04}: face 03 is allowed in a normal book only on pages 0001-0099")));
    }
    // cards on every content face view: keys (C2), types (C8.9), axioms (E2, E3)
    let mut docs = std::collections::BTreeMap::new();
    for (f, fs) in &page.faces {
        if *f == 0 {
            continue;
        }
        let mut texts: Vec<&str> = fs.view().into_iter().collect();
        for c in fs.counters.values() {
            texts.extend(c.bodies.iter().map(|s| s.as_str()));
        }
        for (k, t) in texts.iter().enumerate() {
            match parse_face(t) {
                Ok(doc) => {
                    for c in &doc.cards {
                        if let Some(ty) = c.card_type(*f) {
                            if card_type(&ty).is_none() {
                                findings.push(Reason::finding("C8.9", format!("page {pg:04} face {f:02}: card `{}` has unknown type `{ty}`", c.key)));
                            }
                        }
                        if let Some(ax) = c.field("axioms") {
                            if let Err(e) = AxiomChain::parse(ax) {
                                hard(reasons, e);
                            }
                        }
                    }
                    if k == 0 {
                        docs.insert(*f, doc);
                    }
                }
                Err(e) => hard(reasons, e),
            }
        }
    }
    // C3.2: every 01/02 card that needs it has a 04 card with `why:` and a body
    let empty = crate::cards::FaceDoc { preamble: String::new(), cards: vec![] };
    let f04 = docs.get(&4).unwrap_or(&empty);
    for f in [1u8, 2u8] {
        if page.face(f).map(|x| !x.counters.is_empty()).unwrap_or(false) {
            continue;
        }
        let Some(doc) = docs.get(&f) else { continue };
        for c in &doc.cards {
            let ty = c.card_type(f).unwrap_or_default();
            let needs = card_type(&ty).map(|t| t.needs_04).unwrap_or(false);
            if !needs {
                continue;
            }
            match f04.card(&c.key) {
                None => hard(reasons, SeqError::rejected("C3.2", format!("page {pg:04}: card `{}` on face {f:02} has no 04 card with the same key", c.key))),
                Some(w) => {
                    if w.field("why").map(|s| s.trim().is_empty()).unwrap_or(true) {
                        hard(reasons, SeqError::rejected("C3.2", format!("page {pg:04}: 04 card `{}` needs a `why:` line", c.key)));
                    }
                    if w.body.trim().is_empty() {
                        hard(reasons, SeqError::rejected("C3.2", format!("page {pg:04}: 04 card `{}` needs a body", c.key)));
                    }
                    if f == 1 && !w.body.trim().is_empty() && w.body.trim() == c.body.trim() {
                        findings.push(Reason::finding("C3.2", format!("page {pg:04}: 04 card `{}` copies the 01 body", c.key)));
                    }
                }
            }
        }
    }
    // A5.3: a pointer page's face 08 links need back-links on the target
    let is_pointer = pg == 9999 || (pg >= 100 && pg % 100 == 99) || st.book.desk == 99 || st.book.shelf == 99 || st.book.book == 99;
    if is_pointer {
        if let Some(doc) = docs.get(&8) {
            let me = PageAddr::full(st.book, pg);
            for c in &doc.cards {
                let Some(target) = c.field("target") else { continue };
                let tp = match Address::parse_full_page(target) {
                    Ok(p) => p.page_only(),
                    Err(e) => {
                        hard(reasons, e);
                        continue;
                    }
                };
                let tb = tp.book_id().unwrap();
                let tstate = if tb == st.book { Some(st) } else { world.get(tb) };
                // The target's identity page links back (A5.3): page 0000 for a book target,
                // or the target page itself for a page target (provisional).
                let back = tstate.and_then(|s| s.face(tp.page, 8)).and_then(|f| f.view()).and_then(|b| parse_face(b).ok());
                let ok = back
                    .map(|d| d.cards.iter().any(|bc| bc.field("target").and_then(|t| Address::parse_full_page(t).ok()).map(|p| p.page_only() == me).unwrap_or(false)))
                    .unwrap_or(false);
                if !ok {
                    hard(reasons, SeqError::missing("A5.3", format!("{me}.08 links to {tp} but {tp}.08 has no back-link; a one-way link is invalid (7.8)")));
                }
            }
        }
    }
    let _ = Tail::Draft;
}
