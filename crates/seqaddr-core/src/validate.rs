//! Proposal validation (format 4.1). A proposal is a list of ops applied all
//! or nothing (format 3.3, proposed). Hard failures reject it with reasons;
//! findings are recorded for review and do not reject.

use crate::addr::{Address, BookId, PageAddr};
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
    /// Approval record for seating a face (R2): `director`, or `build-stage (R2)` with `trial`.
    #[serde(default, alias = "approved-by", skip_serializing_if = "Option::is_none")]
    pub approved_by: Option<String>,
    /// The hostile-trial reference that backs a `build-stage (R2)` approval.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub trial: Option<String>,
    /// Why a draft is opened (R5 follow-up): read on the entry that opens a draft (`copy`,
    /// or `put FF.draft` of a new face); stored as entry field `reason`.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reason: Option<String>,
}

/// Approval values accepted for seating a face.
pub const APPROVED_BY_DIRECTOR: &str = "director";
pub const APPROVED_BY_BUILD_STAGE: &str = "build-stage (R2)";

/// Does this request seat a face? `promote`, or a bare `put` creating a seated face (not a counter).
pub fn seats_a_face(r: &OpRequest) -> bool {
    match r.op {
        Some(Op::Promote) => true,
        Some(Op::Put) => {
            let tail_field = r.tail.as_deref().filter(|t| !t.is_empty());
            match Address::parse_full_page(&r.addr) {
                Ok(p) => p.face.as_ref().map(|f| f.counter.is_none() && f.tail.is_none() && tail_field.is_none()).unwrap_or(false),
                Err(_) => false,
            }
        }
        _ => false,
    }
}

/// R2 / E7 / drafting.md:20: the approval a seating op must carry.
pub fn check_seat_approval(r: &OpRequest) -> Result<(), SeqError> {
    match (r.approved_by.as_deref().map(str::trim), r.trial.as_deref().map(str::trim).filter(|t| !t.is_empty())) {
        (Some(APPROVED_BY_DIRECTOR), _) => Ok(()),
        (Some(APPROVED_BY_BUILD_STAGE), Some(_)) => Ok(()),
        (Some(APPROVED_BY_BUILD_STAGE), None) => Err(SeqError::rejected("R2", "`build-stage (R2)` approval needs the hostile trial reference (`trial`)")),
        (Some(other), _) => Err(SeqError::rejected("R2", format!("approval `{other}` is not known; use `director` or `build-stage (R2)` with a `trial` reference"))),
        (None, _) => Err(SeqError::rejected(
            "E7",
            "seating a face needs a review first: a new face starts as `FF.draft` (drafting.md:20) and is promoted only after a hostile pass from another view (decisions.md:588); record `approved_by` (R2)",
        )),
    }
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
        // R4: plain ASCII only.
        let fields = [("by", Some(&proposal.by)), ("addr", Some(&r.addr)), ("tail", r.tail.as_ref()), ("from", r.from.as_ref()), ("to", r.to.as_ref()), ("body", r.body.as_ref()), ("outcome", r.outcome.as_ref()), ("approved_by", r.approved_by.as_ref()), ("trial", r.trial.as_ref()), ("reason", r.reason.as_ref())];
        for (k, v) in fields {
            if let Some(v) = v {
                if let Err(e) = crate::log::check_plain(k, v) {
                    reasons.push(Reason::from_error(&e, Some(i)));
                }
            }
        }
        // Seating needs an approval record (R2, E7). Provisional 7: a bare `put` by the
        // compute itself (derived and system records) is exempt; `promote` never is.
        if policy.seat_needs_approval && seats_a_face(r) && (r.op == Some(Op::Promote) || proposal.by != policy.compute_name) {
            if let Err(e) = check_seat_approval(r) {
                reasons.push(Reason::from_error(&e, Some(i)));
            }
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
        if let Some(a) = &r.approved_by {
            e.extra.insert("approved-by".into(), serde_json::Value::String(a.clone()));
        }
        if let Some(t) = &r.trial {
            e.extra.insert("trial".into(), serde_json::Value::String(t.clone()));
        }
        if let Some(t) = &r.reason {
            e.extra.insert("reason".into(), serde_json::Value::String(t.clone()));
        }
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
    if pg != 0 || policy.c1_on_door_pages {
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
        if pg >= 1000 && stamp.title().is_none() && page.tail() != crate::tail::PageTail::Retired {
            hard(reasons, SeqError::rejected("A2.8", format!("page {pg:04}: pages 1000 and up must have a title in the stamp")));
        }
        // R12: the stamp, page state included, lives in face 00. A written `state:` that is not a
        // page state, or disagrees with the state the faces give, is reported (finding, 7).
        if let Some(sv) = stamp.get("state") {
            let derived = match page.tail() {
                crate::tail::PageTail::Live => "live",
                crate::tail::PageTail::Draft => "draft",
                crate::tail::PageTail::Retired => "retired",
            };
            let sv = sv.trim();
            if !["live", "draft", "retired"].contains(&sv) {
                findings.push(Reason::finding("R12", format!("page {pg:04}: stamp `state: {sv}` is not a page state (live, draft, retired)")));
            } else if sv != derived {
                findings.push(Reason::finding("R12", format!("page {pg:04}: stamp says `state: {sv}` but its faces make it {derived}")));
            }
        }
        if let Some(ax) = stamp.get("axioms") {
            if let Err(e) = AxiomChain::parse(ax) {
                hard(reasons, e);
            }
        }
    }
    // R10: the door page 0000 holds only face 00 (the registry); face 00 is not a sentinel (R9).
    if pg == 0 {
        for (f, fs) in &page.faces {
            if *f != 0 && (fs.is_present()) {
                hard(reasons, SeqError::rejected("R10", format!("{}.0000.{f:02}: the door page 0000 holds only face 00 (Director ruling R10)", st.book)));
            }
        }
    }
    // R7: a local override is its own page in the reserved range 0001-0009 that names its target.
    // A face written over an inherited one with no such page is reported (finding, not rejection:
    // how an override page names its target is 7 - read here as a `target:` line).
    if !st.book.is_kernel() && !(1..=9).contains(&pg) {
        for (f, fs) in &page.faces {
            if *f == 0 || !fs.is_present() || world.policy.is_counted(pg, *f) {
                continue;
            }
            let inherited = st.book.lookup_chain().into_iter().skip(1).find(|b| {
                world.get(*b).and_then(|s| s.page(pg)).and_then(|p| p.face(*f)).map(|x| x.seated.is_some() || x.draft.is_some()).unwrap_or(false)
            });
            if let Some(from) = inherited {
                let target = format!("{}.{pg:04}.{f:02}", st.book);
                if override_pages(st, &target).is_empty() {
                    findings.push(Reason::finding("R7", format!("{target} replaces the face inherited from {from}.{pg:04}.{f:02} in place; an override is written as its own page in 0001-0009 that names its target and says what it changes, why, why it is needed and what it should achieve (Director ruling R7)")));
                }
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
    // decisions.md:287 (C1.4, C8.9): a kernel card marked `owner: kernel-only` is never redefined by a book.
    if !st.book.is_kernel() {
        if let Some(kpage) = world.get(BookId::KERNEL).and_then(|k| k.page(pg)) {
            for (f, doc) in &docs {
                let kdoc = kpage.face(*f).and_then(|x| x.view()).and_then(|b| parse_face(b).ok());
                let Some(kdoc) = kdoc else { continue };
                for c in &doc.cards {
                    if kdoc.card(&c.key).and_then(|k| k.field("owner")) == Some("kernel-only") {
                        hard(reasons, SeqError::rejected("C1.4", format!("{}.{pg:04}.{f:02}: card `{}` is `owner: kernel-only` in the kernel; no book can redefine it", st.book, c.key)));
                    }
                }
            }
        }
    }
    // C3.2: every 01/02 card that needs it has a 04 card with `why:` and a body
    // The 04 card may be inherited (A2.9, axiom 2): if this page has no 04 face of its own,
    // the 04 face found up the chain (book -> shelf -> desk -> kernel) is used.
    let empty = crate::cards::FaceDoc { preamble: String::new(), cards: vec![] };
    let inherited04 = if docs.contains_key(&4) {
        None
    } else {
        let mut w2 = World { books: world.books.clone(), policy: world.policy.clone() };
        w2.insert(st.clone());
        w2.resolve(&PageAddr::full(st.book, pg).with_face(crate::addr::FacePart::face(4)))
            .ok()
            .and_then(|r| match r.found {
                Some(crate::resolve::Found::Face { body }) | Some(crate::resolve::Found::Draft { body }) => parse_face(&body).ok(),
                _ => None,
            })
    };
    let f04 = docs.get(&4).or(inherited04.as_ref()).unwrap_or(&empty);
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
    // A5.1: 99 is a pointer, never content: only the registry (00) and the map (08).
    if is_pointer_page(st.book, pg) {
        for (f, fs) in &page.faces {
            if *f != 0 && *f != 8 && fs.is_present() {
                hard(reasons, SeqError::rejected("A5.1", format!("{}.{pg:04}.{f:02}: a 99 pointer is never content; it holds only its registry 00 and its map 08", st.book)));
            }
        }
        check_pointer_links(world, st, pg, reasons);
    }
    // A5.3 also when a target changes: a pointer anywhere that names this page must still have its back-link.
    let me = PageAddr::full(st.book, pg);
    let mut pointers: Vec<(BookId, u16)> = Vec::new();
    let books = world.books.keys().copied().chain(std::iter::once(st.book)).collect::<BTreeSet<_>>();
    for b in books {
        let bs = if b == st.book { st } else { world.get(b).unwrap() };
        for (ppg, ppage) in &bs.pages {
            if !(is_pointer_page(b, *ppg)) || (b == st.book && *ppg == pg) {
                continue;
            }
            if link_targets(ppage, *ppg).iter().any(|t| *t == me) {
                pointers.push((b, *ppg));
            }
        }
    }
    for (b, ppg) in pointers {
        if b == st.book {
            check_pointer_links(world, st, ppg, reasons);
        } else if let Some(bs) = world.get(b) {
            check_pointer_links_in(world, st, bs, ppg, reasons);
        }
    }
}

/// A page that is a 99 pointer (A5.1): page 9999, a band continuation PP99, or any page of a
/// book with 99 on its desk, shelf or book axis (desk 99 is a reserved pointer, seqAddr 1.3).
pub fn is_pointer_page(book: BookId, pg: u16) -> bool {
    pg == 9999 || (pg >= 100 && pg % 100 == 99) || book.desk == 99 || book.shelf == 99 || book.book == 99
}

/// `target:` page addresses of a page's links (newest view): the link cards on face 08, or,
/// on a door page 0000 (which holds only face 00, R10), `target:` lines in its registry face 00
/// (provisional 7: where a door keeps its back-link is not specified).
fn link_targets(page: &crate::state::PageState, pg: u16) -> Vec<PageAddr> {
    if pg == 0 {
        return page.face(0).and_then(|f| f.view()).map(target_lines).unwrap_or_default();
    }
    page.face(8)
        .and_then(|f| f.view())
        .and_then(|b| parse_face(b).ok())
        .map(|d| d.cards.iter().filter_map(|c| c.field("target")).filter_map(|t| Address::parse_full_page(t).ok()).map(|p| p.page_only()).collect())
        .unwrap_or_default()
}

/// Every `target: <full page address>` line in a text.
fn target_lines(text: &str) -> Vec<PageAddr> {
    text.lines()
        .filter_map(|l| l.trim().strip_prefix("target:"))
        .filter_map(|t| Address::parse_full_page(t.trim()).ok())
        .map(|p| p.page_only())
        .collect()
}

/// R7: the override pages (reserved 0001-0009) of a book whose text names `target`
/// (a full page or face address) on a `target:` line. Provisional 7: the field name.
pub fn override_pages(st: &BookState, target: &str) -> Vec<u16> {
    let page_of = target.split('.').take(4).collect::<Vec<_>>().join(".");
    (1..=9u16)
        .filter(|p| {
            st.page(*p)
                .map(|page| {
                    page.faces.values().filter_map(|f| f.view()).any(|t| {
                        t.lines().filter_map(|l| l.trim().strip_prefix("target:")).map(|v| v.trim()).any(|v| v == target || v == page_of)
                    })
                })
                .unwrap_or(false)
        })
        .collect()
}

fn check_pointer_links(world: &World, st: &BookState, pg: u16, reasons: &mut Vec<Reason>) {
    check_pointer_links_in(world, st, st, pg, reasons)
}

/// A5.3: each target of pointer page `pg` in book `ps` names `pg` back on its face 08.
/// `st` is the proposal's book after the ops (it replaces the world's copy).
fn check_pointer_links_in(world: &World, st: &BookState, ps: &BookState, pg: u16, reasons: &mut Vec<Reason>) {
    let Some(page) = ps.page(pg) else { return };
    let me = PageAddr::full(ps.book, pg);
    if let Some(doc) = page.face(8).and_then(|f| f.view()).and_then(|b| parse_face(b).ok()) {
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
            let ok = tstate.and_then(|s| s.page(tp.page)).map(|tpage| link_targets(tpage, tp.page).iter().any(|t| *t == me)).unwrap_or(false);
            if !ok {
                let back = if tp.page == 0 { "00 (door page, R10)" } else { "08" };
                hard(reasons, SeqError::missing("A5.3", format!("{me}.08 links to {tp} but {tp}.{back} has no back-link; a one-way link is invalid (7.8)")));
            }
        }
    }
}
