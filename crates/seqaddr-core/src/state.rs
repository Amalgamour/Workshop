//! A book's current state, rebuilt by replaying its log (format 3.1, 3.3, 3.4),
//! with the tail, drafting and claim rules applied to every entry.

use crate::addr::{Address, BookId, PageAddr, Tail};
use crate::cards::{parse_stamp, Stamp};
use crate::error::{Result, SeqError};
use crate::face::{always_counted, is_content_face};
use crate::log::{check_timestamp, BookLog, Entry, Op};
use crate::tail::{check_counter_create, check_counter_move, CounterTail, FaceSlotState, PageTail};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Outcomes recorded when a counter closes (workflow-loop.003 6, approved S03).
pub const OUTCOMES: [&str; 5] = ["passed", "failed", "blocked", "needs-authority", "abandoned"];

/// Switches for rules the spec marks proposed, or choices made provisionally.
/// Every switch is listed in docs/BUILD-LOG.md.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Policy {
    /// Apply the proposed ops `copy`, `note`, `merge`, `promote`, `use` (format 3.3).
    pub allow_proposed_ops: bool,
    /// D0 (proposed mechanism): a full-body `put` never replaces an existing face.
    pub enforce_drafting: bool,
    /// The author name the compute writes under (`use`, system returns).
    pub compute_name: String,
    /// Faces counted besides 05/06, as (page, face). Default: the dictionary 0012.03 (C8.3).
    pub extra_counted: Vec<(u16, u8)>,
    /// Apply C1.1 (face 00 + a content face) to door pages 0000 too. R10: the door page
    /// holds only face 00, so this is off by default; turning it on makes every door page fail.
    pub c1_on_door_pages: bool,
    /// A `put` on an existing counter still in `draft` replaces its body (a pack being written).
    pub draft_counter_put_replaces: bool,
    /// workflow-loop.003 6: reviewer must differ from the builder (claim owner).
    pub reviewer_not_builder: bool,
    /// workflow-loop.003 6.3: closing (`review -> bare`) needs an outcome.
    pub close_needs_outcome: bool,
    /// workflow-loop.003 6 steps 2 and 7: only the compute lints (`draft -> pack`) and closes (`review -> bare`).
    pub compute_only_steps: bool,
    /// workflow-loop.003 6.4: the compute may return on another's claim only during authorized
    /// recovery. How the abandonment decision is recorded is `7`, so this is off until it is designed.
    pub compute_recovery_return: bool,
    /// Proposal rule (R2, E7, drafting.md:20): seating a face (`promote`, or a bare `put` that
    /// creates a seated face) needs an approval record: `approved_by: director`, or
    /// `approved_by: build-stage (R2)` with a `trial` reference.
    pub seat_needs_approval: bool,
}

impl Default for Policy {
    fn default() -> Self {
        Policy {
            allow_proposed_ops: true,
            enforce_drafting: true,
            compute_name: "compute".into(),
            extra_counted: vec![(12, 3)],
            c1_on_door_pages: false,
            draft_counter_put_replaces: false,
            reviewer_not_builder: true,
            close_needs_outcome: true,
            compute_only_steps: true,
            compute_recovery_return: false,
            seat_needs_approval: true,
        }
    }
}

impl Policy {
    pub fn is_counted(&self, page: u16, face: u8) -> bool {
        always_counted(face) || self.extra_counted.contains(&(page, face))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Note {
    pub n: u64,
    pub by: String,
    pub text: String,
    pub struck: bool,
    /// The merge entry that struck it.
    pub struck_by: Option<u64>,
}

/// `FF.draft`: one per face (seqAddr 5.7), with its notes (D0).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Draft {
    pub body: String,
    /// Why the draft was opened: field `reason` of the opening entry (R5 follow-up; optional).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reason: Option<String>,
    pub notes: Vec<Note>,
    /// Entry that created the draft (`put` or `copy`).
    pub n: u64,
}

impl Draft {
    pub fn open_notes(&self) -> usize {
        self.notes.iter().filter(|n| !n.struck).count()
    }
}

/// A claim on a pack (workflow-loop.003 6 step 3, S11): first valid claim wins.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Claim {
    pub id: String,
    pub owner: String,
    pub start: String,
    pub n: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CounterState {
    pub tail: CounterTail,
    /// Bodies in order: the pack, then the return appended to the same counter (6.1).
    pub bodies: Vec<String>,
    pub claim: Option<Claim>,
    pub reviewer: Option<String>,
    /// Who moved `open -> return`.
    pub returned_by: Option<String>,
    pub outcome: Option<String>,
    pub created_n: u64,
    /// Entry numbers that touched this counter.
    pub entries: Vec<u64>,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FaceState {
    /// The seated face, bare `FF`.
    pub seated: Option<String>,
    pub draft: Option<Draft>,
    /// `FF.retired`: the last seated body, awaiting removal.
    pub retired: Option<String>,
    pub counters: BTreeMap<u8, CounterState>,
}

impl FaceState {
    pub fn slot_state(&self) -> FaceSlotState {
        match (&self.seated, &self.draft, &self.retired) {
            (_, _, Some(_)) if self.seated.is_none() => FaceSlotState::Retired,
            (Some(_), Some(_), _) => FaceSlotState::SeatedWithDraft,
            (Some(_), None, _) => FaceSlotState::Seated,
            (None, Some(_), _) => FaceSlotState::DraftOnly,
            _ => FaceSlotState::Absent,
        }
    }
    /// Present and not retired: seated, a draft, or counters (C1.1, C1.2).
    pub fn is_present(&self) -> bool {
        self.seated.is_some() || self.draft.is_some() || !self.counters.is_empty()
    }
    /// Live content: seated, or a counter past `draft` (drafts are not active, seqAddr 4;
    /// C1.2 a page with only drafts is draft, draft counters included).
    pub fn is_live(&self) -> bool {
        self.seated.is_some() || self.counters.values().any(|c| c.tail != crate::tail::CounterTail::Draft)
    }
    /// The newest text: the draft if there is one, else the seated body.
    pub fn view(&self) -> Option<&str> {
        self.draft.as_ref().map(|d| d.body.as_str()).or(self.seated.as_deref())
    }
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct PageState {
    pub faces: BTreeMap<u8, FaceState>,
    /// Set by a `tail` move on the page itself (`PPPP.retired`).
    pub retired_explicit: bool,
}

impl PageState {
    pub fn face(&self, f: u8) -> Option<&FaceState> {
        self.faces.get(&f)
    }
    /// Page state (A2.5, C1.2, C1.3).
    pub fn tail(&self) -> PageTail {
        if self.retired_explicit {
            return PageTail::Retired;
        }
        let content: Vec<&FaceState> = self.faces.iter().filter(|(f, _)| is_content_face(**f)).map(|(_, s)| s).collect();
        let had_content = content.iter().any(|f| f.is_present() || f.retired.is_some());
        if had_content && !content.iter().any(|f| f.is_present()) {
            return PageTail::Retired; // C1.3: retiring the last content face retires the page
        }
        if had_content && !content.iter().any(|f| f.is_live()) {
            return PageTail::Draft; // C1.2: a page with only drafts
        }
        PageTail::Live
    }
    /// Face 00 stamp (seated, else draft).
    pub fn stamp(&self) -> Option<Stamp> {
        self.faces.get(&0).and_then(|f| f.view()).map(parse_stamp)
    }
    pub fn title(&self) -> Option<String> {
        self.stamp().and_then(|s| s.title().map(|t| t.to_string()))
    }
    /// C1.1: face 00 and at least one of 01-06 or 08 (drafts count; 07 does not).
    pub fn check_c1(&self, page: u16) -> Result<()> {
        if self.tail() == PageTail::Retired {
            return Ok(());
        }
        if !self.faces.get(&0).map(|f| f.is_present()).unwrap_or(false) {
            return Err(SeqError::rejected("C1.1", format!("page {page:04} has no face 00 (its registry, R10)")));
        }
        if !self.faces.iter().any(|(f, s)| is_content_face(*f) && s.is_present()) {
            return Err(SeqError::rejected("C1.1", format!("page {page:04} needs at least one of faces 01-06 or 08; a page with only its door has no reason to exist")));
        }
        Ok(())
    }
}

/// A word resolution recorded by the compute (C8.7, proposed `use`).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UseRecord {
    pub n: u64,
    pub addr: String,
    pub body: Option<String>,
    pub outcome: Option<String>,
}

/// The replayed state of one book.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BookState {
    pub book: BookId,
    pub pages: BTreeMap<u16, PageState>,
    pub last_n: u64,
    pub uses: Vec<UseRecord>,
}

/// One line of a counted face's derived listing: counter and its current tail.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BoardLine {
    pub counter: u8,
    pub tail: CounterTail,
}

fn want_body(e: &Entry, rule: &'static str) -> Result<String> {
    e.body.clone().ok_or_else(|| SeqError::rejected(rule, format!("`{}` on {} needs a body", e.op.as_str(), e.addr)))
}

impl BookState {
    pub fn new(book: BookId) -> Self {
        BookState { book, pages: BTreeMap::new(), last_n: 0, uses: Vec::new() }
    }

    /// Replay a whole log (format 3.1). Every snapshot met on the way is checked
    /// against the state the log gives at that point; a snapshot that disagrees
    /// is refused (axiom 6: the past is not rewritten). A log whose early entries
    /// were archived (first entry n > 1) starts at its first snapshot.
    pub fn replay(log: &BookLog, policy: &Policy) -> Result<BookState> {
        Self::replay_entries(log, &log.entries, policy)
    }

    /// Fast replay that trusts the latest snapshot and skips what comes before it (format 3.4).
    /// Use only on books whose snapshots were checked (by `replay`) when opened.
    pub fn replay_from_latest_snapshot(log: &BookLog, policy: &Policy) -> Result<BookState> {
        let start = log.latest_snapshot().unwrap_or(0);
        Self::replay_entries(log, &log.entries[start..], policy)
    }

    /// Replay only up to entry `n` (rewind, format 3.1), checking snapshots the same way.
    pub fn replay_until(log: &BookLog, n: u64, policy: &Policy) -> Result<BookState> {
        let upto: Vec<Entry> = log.entries.iter().take_while(|e| e.n <= n).cloned().collect();
        Self::replay_entries(log, &upto, policy)
    }

    fn replay_entries(log: &BookLog, entries: &[Entry], policy: &Policy) -> Result<BookState> {
        let book = log.book()?;
        let mut st = BookState::new(book);
        let start = match entries.first() {
            Some(e) if e.n != 1 && e.op != Op::Snapshot => entries
                .iter()
                .position(|e| e.op == Op::Snapshot)
                .ok_or_else(|| SeqError::Corrupt { line: 2, detail: format!("log starts at n={} with no snapshot to start from", e.n) })?,
            _ => 0,
        };
        for e in &entries[start..] {
            st.apply(e, policy)?;
        }
        Ok(st)
    }

    /// Build a snapshot entry carrying this full state (format 3.4).
    pub fn snapshot_entry(&self, at: &str, by: &str) -> Entry {
        let mut e = Entry::new(self.last_n + 1, at, by, Op::Snapshot, self.book.to_string());
        let mut copy = self.clone();
        copy.last_n += 1;
        e.state = Some(serde_json::to_value(&copy).expect("state serializes"));
        e
    }

    pub fn page(&self, p: u16) -> Option<&PageState> {
        self.pages.get(&p)
    }
    pub fn face(&self, p: u16, f: u8) -> Option<&FaceState> {
        self.pages.get(&p).and_then(|pg| pg.faces.get(&f))
    }
    pub fn counter(&self, p: u16, f: u8, nn: u8) -> Option<&CounterState> {
        self.face(p, f).and_then(|fs| fs.counters.get(&nn))
    }
    /// A derived listing of a counted face's counters (R9: there is no `FF.00`; never written as an entry).
    pub fn board(&self, p: u16, f: u8) -> Vec<BoardLine> {
        self.face(p, f)
            .map(|fs| fs.counters.iter().filter(|(nn, _)| **nn != 99).map(|(nn, c)| BoardLine { counter: *nn, tail: c.tail }).collect())
            .unwrap_or_default()
    }
    /// The book's title, from its door page stamp (0000.00) (A3.1).
    pub fn title(&self) -> Option<String> {
        self.page(0).and_then(|p| p.title())
    }
    /// Older name for [`BookState::has_door`].
    pub fn has_identity(&self) -> bool {
        self.has_door()
    }
    /// Does the door exist (face 00 on 0000)? Containers need it to be legal (seqAddr 8).
    /// R18: the pages of this book in the same cross-band set as `p` (same N and CC,
    /// other bands, same title), `p` included when it has a title. Sorted.
    pub fn set_of(&self, p: u16) -> Vec<u16> {
        let Some(t) = self.page(p).and_then(|pg| pg.title()) else { return vec![] };
        let mut out: Vec<u16> = self.pages.iter().filter(|(q, pg)| **q == p || crate::addr::same_set(p, Some(&t), **q, pg.title().as_deref())).map(|(q, _)| *q).collect();
        out.sort();
        out
    }
    pub fn has_door(&self) -> bool {
        self.face(0, 0).map(|f| f.is_present()).unwrap_or(false)
    }

    fn parse_own(&self, addr: &str) -> Result<PageAddr> {
        let p = Address::parse_full_page(addr)?;
        if p.book_id() != Some(self.book) {
            return Err(SeqError::rejected("format 1.3", format!("{addr} is not in book {}", self.book)));
        }
        Ok(p)
    }

    /// Apply one approved entry. Used by replay and by proposal validation.
    pub fn apply(&mut self, e: &Entry, policy: &Policy) -> Result<()> {
        // A snapshot may start a replay (format 3.4): then earlier entries are skipped.
        let starts_replay = e.op == Op::Snapshot && self.last_n == 0 && self.pages.is_empty();
        if e.n != self.last_n + 1 && !starts_replay {
            return Err(SeqError::rejected("format 3.2", format!("entry n={} out of sequence; expected {}", e.n, self.last_n + 1)));
        }
        check_timestamp(&e.at)?;
        if e.by.trim().is_empty() {
            return Err(SeqError::rejected("format 3.2", "every entry names its author (`by`)"));
        }
        if e.op.is_proposed() && !policy.allow_proposed_ops {
            return Err(SeqError::rejected("format 3.3", format!("op `{}` is proposed and switched off", e.op.as_str())));
        }
        match e.op {
            Op::Snapshot => self.apply_snapshot(e)?,
            Op::Put => self.apply_put(e, policy)?,
            Op::Tail => self.apply_tail(e, policy)?,
            Op::Copy => self.apply_copy(e)?,
            Op::Note => self.apply_note(e)?,
            Op::Merge => self.apply_merge(e)?,
            Op::Promote => self.apply_promote(e)?,
            Op::Use => self.apply_use(e, policy)?,
        }
        self.last_n = e.n;
        Ok(())
    }

    fn apply_snapshot(&mut self, e: &Entry) -> Result<()> {
        let v = e.state.clone().ok_or_else(|| SeqError::rejected("format 3.4", "a snapshot carries the full state"))?;
        let st: BookState = serde_json::from_value(v).map_err(|err| SeqError::rejected("format 3.4", format!("bad snapshot: {err}")))?;
        if st.book != self.book {
            return Err(SeqError::rejected("format 3.4", "snapshot is for another book"));
        }
        if st.last_n != e.n {
            return Err(SeqError::rejected("format 3.4", format!("snapshot at n={} records last_n={}", e.n, st.last_n)));
        }
        let starts_replay = self.last_n == 0 && self.pages.is_empty() && self.uses.is_empty();
        if !starts_replay {
            let mut here = self.clone();
            here.last_n = e.n;
            if here != st {
                return Err(SeqError::rejected("format 3.4", format!("snapshot n={} disagrees with the log before it; refused (axiom 6: the past is not rewritten)", e.n)));
            }
        }
        *self = st;
        self.last_n = e.n - 1; // apply() sets last_n = e.n
        Ok(())
    }

    fn door_first(&self, page: u16, face: u8) -> Result<()> {
        if page == 0 && face == 0 {
            return Ok(());
        }
        if !self.has_door() {
            return Err(SeqError::missing(
                "format 4.1",
                format!("book {} has no door {}.0000.00 yet; the door is written first", self.book, self.book),
            ));
        }
        // A page's own face 00 may arrive later in the same proposal; C1.1 checks the result.
        Ok(())
    }

    fn entry_tail(e: &Entry, p: &PageAddr) -> Result<Option<Tail>> {
        let from_addr = p.tail();
        let from_field = match e.tail.as_deref() {
            None | Some("") => None,
            Some(w) => Some(Tail::from_word(w).ok_or_else(|| SeqError::invalid("A2.5", format!("`{w}` is not a tail word")))?),
        };
        match (from_addr, from_field) {
            (Some(a), Some(b)) if a != b => Err(SeqError::invalid("A2.5", format!("address tail `{a}` and `tail` field `{b}` disagree"))),
            (a, b) => Ok(a.or(b)),
        }
    }

    fn apply_put(&mut self, e: &Entry, policy: &Policy) -> Result<()> {
        let p = self.parse_own(&e.addr)?;
        let fp = p.face.clone().ok_or_else(|| SeqError::rejected("format 3.3", format!("`put` creates a face or counter; {} names no face", e.addr)))?;
        if fp.card.is_some() {
            return Err(SeqError::rejected("format 3.3", "`put` writes a whole face or counter, not a single card"));
        }
        let tail = Self::entry_tail(e, &p)?;
        self.door_first(p.page, fp.face)?;
        let counted = policy.is_counted(p.page, fp.face);
        match fp.counter {
            Some(nn) if !(1..=98).contains(&nn) => Err(SeqError::rejected("R9", format!("counter {nn:02}: faces have no sentinels; counters run 01-98 (Director ruling R9)"))),
            Some(nn) => {
                if !counted {
                    return Err(SeqError::rejected("A4.4", format!("face {:02} on page {:04} is not a counted face; counters live on counted faces only (05, 06 and Policy.extra_counted)", fp.face, p.page)));
                }
                if let Some(Tail::Retired) = tail {
                    return Err(SeqError::invalid("A2.5", "`retired` is used only without a counter"));
                }
                let ct = CounterTail::from_tail(tail)?;
                if nn == 99 {
                    if self.counter(p.page, fp.face, 98).is_none() {
                        return Err(SeqError::rejected("A4.5", "`FF.99` is written only once `FF.98` exists"));
                    }
                    if ct != CounterTail::Closed {
                        return Err(SeqError::invalid("A5.1", "`FF.99` is a pointer and takes no tail"));
                    }
                }
                let n = e.n;
                let body = e.body.clone();
                let page = self.pages.entry(p.page).or_default();
                let face = page.faces.entry(fp.face).or_default();
                match face.counters.get_mut(&nn) {
                    Some(c) => {
                        if policy.draft_counter_put_replaces && c.tail == CounterTail::Draft && ct == CounterTail::Draft {
                            c.bodies = body.into_iter().collect();
                            c.entries.push(n);
                            Ok(())
                        } else {
                            Err(SeqError::rejected("format 3.3", format!("counter {:02}.{nn:02} already exists; `put` only creates (D0)", fp.face)))
                        }
                    }
                    None => {
                        check_counter_create(ct)?;
                        face.counters.insert(
                            nn,
                            CounterState { tail: ct, bodies: body.into_iter().collect(), claim: None, reviewer: None, returned_by: None, outcome: None, created_n: n, entries: vec![n] },
                        );
                        Ok(())
                    }
                }
            }
            None => {
                if counted {
                    return Err(SeqError::rejected("A4.4", format!("face {:02} is counted: it holds counters only, so write a counter `FF.NN` (01-98); it has no door of its own (R9)", fp.face)));
                }
                let body = want_body(e, "format 3.3")?;
                let n = e.n;
                let page = self.pages.entry(p.page).or_default();
                let face = page.faces.entry(fp.face).or_default();
                match tail {
                    None => {
                        if face.retired.is_some() && face.seated.is_none() {
                            return Err(SeqError::rejected("seqAddr 5.7", "this face is retired and awaiting removal; it cannot be re-seated by `put`"));
                        }
                        if face.draft.is_some() {
                            return Err(SeqError::rejected("seqAddr 5.7", "this face has a draft; seat it with `promote`, not `put`"));
                        }
                        if face.seated.is_some() && policy.enforce_drafting {
                            return Err(SeqError::rejected("D0", "a full-body `put` never replaces an existing face; use copy, note, merge, promote"));
                        }
                        face.seated = Some(body);
                        Ok(())
                    }
                    Some(Tail::Draft) => {
                        if face.retired.is_some() && face.seated.is_none() {
                            return Err(SeqError::rejected("seqAddr 5.7", "this face is retired and awaiting removal; it is not drafted again"));
                        }
                        if face.draft.is_some() {
                            return Err(SeqError::conflict("seqAddr 5.7", "this face already has its one draft `FF.draft`"));
                        }
                        if face.seated.is_some() && policy.enforce_drafting {
                            return Err(SeqError::rejected("D0", "a seated face is drafted with `copy` (the compute copies it); the writer sends no body"));
                        }
                        face.draft = Some(Draft { body, reason: e.reason().map(str::to_string), notes: Vec::new(), n });
                        Ok(())
                    }
                    Some(t) => Err(SeqError::rejected("A2.5", format!("a face is not created as `{t}`"))),
                }
            }
        }
    }

    fn apply_tail(&mut self, e: &Entry, policy: &Policy) -> Result<()> {
        let p = self.parse_own(&e.addr)?;
        if p.tail().is_some() {
            return Err(SeqError::invalid("format 3.3", "a `tail` op names the slot without a tail and gives `from` / `to`"));
        }
        let Some(fp) = p.face.clone() else {
            // Page tail (A2.5): only bare -> retired is a move (provisional).
            let to = e.to.as_deref().unwrap_or("");
            let from = e.from.as_deref().unwrap_or("");
            let page = self.pages.get_mut(&p.page).ok_or_else(|| SeqError::missing("A2.5", format!("page {} does not exist", p)))?;
            if from.is_empty() && to == "retired" && !page.retired_explicit {
                page.retired_explicit = true;
                return Ok(());
            }
            return Err(SeqError::rejected("A2.5", format!("page tail move `{from}` -> `{to}` is not allowed; a page is retired from bare")));
        };
        if fp.card.is_some() {
            return Err(SeqError::invalid("format 3.3", "a tail moves on a face or counter, not on a card"));
        }
        match fp.counter {
            None => {
                let from = e.from.as_deref().unwrap_or("");
                let to = e.to.as_deref().unwrap_or("");
                let face = self.pages.get_mut(&p.page).and_then(|pg| pg.faces.get_mut(&fp.face)).ok_or_else(|| SeqError::missing("format 4.1", format!("{} does not exist", p)))?;
                if from.is_empty() && to == "retired" {
                    let body = face.seated.take().ok_or_else(|| SeqError::rejected("seqAddr 5.7", "only a seated face can be retired"))?;
                    face.retired = Some(body);
                    return Ok(());
                }
                Err(SeqError::rejected("seqAddr 5.7", format!("face tail move `{from}` -> `{to}` is not allowed; drafts are seated by `promote`")))
            }
            Some(0) | Some(99) => Err(SeqError::rejected("R9", "faces have no sentinels: `FF.00` and `FF.99` do not exist (Director ruling R9)")),
            Some(nn) => {
                let from = CounterTail::from_field(e.from.as_deref())?;
                let to = CounterTail::from_field(e.to.as_deref())?;
                let c = self
                    .pages
                    .get_mut(&p.page)
                    .and_then(|pg| pg.faces.get_mut(&fp.face))
                    .and_then(|f| f.counters.get_mut(&nn))
                    .ok_or_else(|| SeqError::missing("format 4.1", format!("counter {} does not exist", p)))?;
                if c.tail != from {
                    if from == CounterTail::Pack && to == CounterTail::Open && c.tail == CounterTail::Open {
                        let owner = c.claim.as_ref().map(|c| c.owner.clone()).unwrap_or_default();
                        return Err(SeqError::conflict("format 2", format!("{} is already claimed by `{owner}`; the first claim on a pack wins", p)));
                    }
                    return Err(SeqError::rejected("format 3.3", format!("{} is `{}`, not `{from}`; a tail move is rejected if `from` is not current", p, c.tail)));
                }
                check_counter_move(from, to)?;
                if policy.compute_only_steps && e.by != policy.compute_name {
                    match (from, to) {
                        (CounterTail::Draft, CounterTail::Pack) => {
                            return Err(SeqError::rejected("workflow-loop.003 6", "`draft -> pack` is the lint step; only the compute moves it, after checking the pack (section 8)"))
                        }
                        (CounterTail::Review, CounterTail::Closed) => {
                            return Err(SeqError::rejected("workflow-loop.003 6", "`review -> closed` is done by the compute once the review and outcome are recorded"))
                        }
                        _ => {}
                    }
                }
                match (from, to) {
                    (CounterTail::Pack, CounterTail::Open) => {
                        c.claim = Some(Claim { id: format!("claim-{}", e.n), owner: e.by.clone(), start: e.at.clone(), n: e.n });
                    }
                    (CounterTail::Open, CounterTail::Return) => {
                        let owner = c.claim.as_ref().map(|c| c.owner.as_str()).unwrap_or("");
                        if e.by != owner {
                            if e.by != policy.compute_name {
                                return Err(SeqError::conflict("S11", format!("`{}` does not hold the claim on {} (held by `{owner}`); a stale or foreign claim cannot write", e.by, p)));
                            }
                            if !policy.compute_recovery_return {
                                return Err(SeqError::rejected("S11", format!("the compute returns on `{owner}`'s claim only in authorized recovery, after an abandonment decision is recorded (workflow-loop.003 6.4); how it is recorded is not designed yet (7)")));
                            }
                        }
                        c.returned_by = Some(e.by.clone());
                        if let Some(b) = &e.body {
                            c.bodies.push(b.clone()); // 6.1: the return lives on the same counter
                        }
                    }
                    (CounterTail::Return, CounterTail::Review) => {
                        let owner = c.claim.as_ref().map(|c| c.owner.as_str()).unwrap_or("");
                        if policy.reviewer_not_builder && e.by == owner {
                            return Err(SeqError::rejected("S10", format!("`{}` built {} and cannot review its own return", e.by, p)));
                        }
                        c.reviewer = Some(e.by.clone());
                    }
                    (CounterTail::Review, CounterTail::Closed) => {
                        match e.outcome.as_deref() {
                            Some(o) if OUTCOMES.contains(&o) => {
                                if o == "abandoned" && c.returned_by.as_deref() != Some(policy.compute_name.as_str()) {
                                    return Err(SeqError::rejected("S11", "`abandoned` needs the compute's system return (recovery record) on this counter"));
                                }
                                c.outcome = Some(o.to_string());
                            }
                            Some(o) => return Err(SeqError::rejected("S03", format!("outcome `{o}` is not one of passed, failed, blocked, needs-authority, abandoned"))),
                            None if policy.close_needs_outcome => return Err(SeqError::rejected("S03", "record the outcome on the move to the bare counter")),
                            None => {}
                        }
                    }
                    _ => {}
                }
                c.tail = to;
                c.entries.push(e.n);
                Ok(())
            }
        }
    }

    fn draft_slot(&mut self, e: &Entry) -> Result<(PageAddr, &mut FaceState)> {
        let p = self.parse_own(&e.addr)?;
        let fp = p.face.clone().ok_or_else(|| SeqError::rejected("D0", "drafting ops name a face"))?;
        if fp.counter.is_some() || fp.card.is_some() {
            return Err(SeqError::rejected("D0", "drafting ops work on a whole seated face `FF` or its `FF.draft`"));
        }
        if matches!(fp.tail, Some(t) if t != Tail::Draft) {
            return Err(SeqError::invalid("D0", "drafting ops name `FF` or `FF.draft`"));
        }
        let page = p.page;
        let face = self.pages.get_mut(&page).and_then(|pg| pg.faces.get_mut(&fp.face)).ok_or_else(|| SeqError::missing("D0", format!("{} does not exist", e.addr)))?;
        Ok((p, face))
    }

    fn apply_copy(&mut self, e: &Entry) -> Result<()> {
        if e.body.is_some() {
            return Err(SeqError::rejected("D0", "`copy`: the compute copies the face; the writer sends no body"));
        }
        let n = e.n;
        let (_, face) = self.draft_slot(e)?;
        let seated = face.seated.clone().ok_or_else(|| SeqError::missing("D0", "`copy` needs a seated face to copy"))?;
        if face.draft.is_some() {
            return Err(SeqError::conflict("seqAddr 5.7", "this face already has its one draft"));
        }
        face.draft = Some(Draft { body: seated, reason: e.reason().map(str::to_string), notes: Vec::new(), n });
        Ok(())
    }

    fn apply_note(&mut self, e: &Entry) -> Result<()> {
        let text = want_body(e, "D0")?;
        let (n, by) = (e.n, e.by.clone());
        let (_, face) = self.draft_slot(e)?;
        let d = face.draft.as_mut().ok_or_else(|| SeqError::missing("D0", "`note` adds to a draft; there is no `FF.draft`"))?;
        d.notes.push(Note { n, by, text, struck: false, struck_by: None });
        Ok(())
    }

    fn apply_merge(&mut self, e: &Entry) -> Result<()> {
        let body = want_body(e, "D0")?;
        let cites = e.cites.ok_or_else(|| SeqError::rejected("D0", "`merge` cites the note it comes from (`cites`)"))?;
        let n = e.n;
        let (_, face) = self.draft_slot(e)?;
        let d = face.draft.as_mut().ok_or_else(|| SeqError::missing("D0", "`merge` needs a draft"))?;
        let note = d.notes.iter_mut().find(|x| x.n == cites).ok_or_else(|| SeqError::missing("D0", format!("note {cites} is not on this draft")))?;
        if note.struck {
            return Err(SeqError::rejected("D0", format!("note {cites} is already struck")));
        }
        note.struck = true;
        note.struck_by = Some(n);
        d.body = body;
        Ok(())
    }

    fn apply_promote(&mut self, e: &Entry) -> Result<()> {
        if e.body.is_some() {
            return Err(SeqError::rejected("D0", "`promote` seats the draft as it is; it carries no body"));
        }
        let (_, face) = self.draft_slot(e)?;
        let d = face.draft.as_ref().ok_or_else(|| SeqError::missing("D0", "`promote` needs a draft"))?;
        if face.retired.is_some() && face.seated.is_none() {
            return Err(SeqError::rejected("seqAddr 5.7", "this face is retired and awaiting removal; a draft does not re-seat it"));
        }
        if d.open_notes() > 0 {
            return Err(SeqError::rejected("D0", format!("{} note(s) are not struck; review checks every note is struck before promote", d.open_notes())));
        }
        let d = face.draft.take().unwrap();
        face.seated = Some(d.body);
        face.retired = None;
        Ok(())
    }

    fn apply_use(&mut self, e: &Entry, policy: &Policy) -> Result<()> {
        if e.by != policy.compute_name {
            return Err(SeqError::rejected("C8.7", "`use` is written only by the compute"));
        }
        Address::parse(&e.addr)?;
        self.uses.push(UseRecord { n: e.n, addr: e.addr.clone(), body: e.body.clone(), outcome: e.outcome.clone() });
        Ok(())
    }
}
