//! Finding (A1.8, A2.9, A4.1): a face is looked up in its book, then the
//! shelf's own book, then the desk's own book, then the kernel `00.00.00`, at
//! the same page and face. The first match wins. Missing stays missing (axiom 7).

use crate::addr::{Address, Active, BookId, PageAddr};
use crate::error::{Result, SeqError};
use crate::state::{BoardLine, BookState, Policy};
use crate::tail::CounterTail;
use serde::Serialize;
use std::collections::{BTreeMap, BTreeSet};

/// Every open book, keyed by address (format 4.2).
#[derive(Debug, Clone, Default)]
pub struct World {
    pub books: BTreeMap<BookId, BookState>,
    pub policy: Policy,
}

/// Where a face was found, relative to the asked book.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Origin {
    Local,
    Shelf,
    Desk,
    Kernel,
    Missing,
}

impl Origin {
    pub fn as_str(self) -> &'static str {
        match self {
            Origin::Local => "local",
            Origin::Shelf => "shelf",
            Origin::Desk => "desk",
            Origin::Kernel => "kernel",
            Origin::Missing => "missing",
        }
    }
}

/// One step of the lookup trace (lane contract `/resolve`).
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Step {
    pub step: usize,
    pub checked: String,
    pub found: bool,
    /// Why it was not found: `no book`, `no page`, `no face`, `draft only`, `retired`.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub note: Option<String>,
}

/// What was found.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Found {
    /// A seated face.
    Face { body: String },
    /// A counter with its tail and bodies.
    Counter { tail: CounterTail, bodies: Vec<String> },
    /// A derived listing of a counted face's counters, read by plain `FF` (R9: there is no `FF.00`; 7).
    Board { lines: Vec<BoardLine> },
    /// A draft: asked for as `FF.draft`, or the only copy at a spot (Director ruling R5).
    Draft { body: String },
    /// A retired face, only when asked for `FF.retired`.
    Retired { body: String },
}

impl Found {
    /// The state of what was found: `seated`, `draft`, `retired`, `counter`, `door` (board).
    pub fn state(&self) -> &'static str {
        match self {
            Found::Face { .. } => "seated",
            Found::Draft { .. } => "draft",
            Found::Retired { .. } => "retired",
            Found::Counter { .. } => "counter",
            Found::Board { .. } => "board",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Resolution {
    /// The full address asked for.
    pub address: String,
    /// The full address where it was found.
    pub source: Option<String>,
    pub origin: Origin,
    pub found: Option<Found>,
    /// `found.state()`: `seated`, `draft` (R5: a draft found is still a draft), `retired`, `counter`, `board`.
    pub state: Option<String>,
    /// R5 follow-up: when a draft is found, why it is a draft (its drafting record and notes).
    #[serde(skip_serializing_if = "Option::is_none")]
    pub why_draft: Option<DraftWhy>,
    pub trace: Vec<Step>,
}

/// Why a found face is a draft (R5 follow-up, R8: a draft exists only while a face is being drafted).
/// The shape is provisional (7, see BUILD-LOG).
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DraftWhy {
    /// Entry that opened the draft (`copy` of the seated face, or `put FF.draft` of a new face).
    pub opened_by_entry: u64,
    /// The `reason` recorded on the opening entry, if any.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reason: Option<String>,
    /// True when a seated face exists at the spot (the draft is a working copy of it, drafting.md step 1).
    pub has_seated: bool,
    /// Notes not yet merged: `(entry, by, text)`.
    pub open_notes: Vec<DraftNote>,
    /// Notes already merged (struck).
    pub merged_notes: usize,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DraftNote {
    pub n: u64,
    pub by: String,
    pub text: String,
}

fn draft_why(st: &BookState, p: &PageAddr) -> Option<DraftWhy> {
    let fp = p.face.as_ref()?;
    let face = st.page(p.page)?.face(fp.face)?;
    let d = face.draft.as_ref()?;
    Some(DraftWhy {
        opened_by_entry: d.n,
        reason: d.reason.clone(),
        has_seated: face.seated.is_some(),
        open_notes: d.notes.iter().filter(|n| !n.struck).map(|n| DraftNote { n: n.n, by: n.by.clone(), text: n.text.clone() }).collect(),
        merged_notes: d.notes.iter().filter(|n| n.struck).count(),
    })
}

impl Resolution {
    pub fn into_result(self) -> Result<Resolution> {
        if self.found.is_some() {
            Ok(self)
        } else {
            Err(SeqError::missing("A1.8", format!("{} was not found in book, shelf, desk or kernel; elevate to the user, never guess", self.address)))
        }
    }
}

fn origin_for(asked: BookId, at: BookId) -> Origin {
    if asked == at {
        Origin::Local
    } else if at.is_kernel() {
        Origin::Kernel
    } else if at.shelf == 0 {
        Origin::Desk
    } else {
        Origin::Shelf
    }
}

impl World {
    pub fn new(policy: Policy) -> Self {
        World { books: BTreeMap::new(), policy }
    }
    pub fn insert(&mut self, st: BookState) {
        self.books.insert(st.book, st);
    }
    pub fn get(&self, b: BookId) -> Option<&BookState> {
        self.books.get(&b)
    }

    /// Look in one book for the slot named by `p` (ancestors ignored).
    fn find_in(&self, st: &BookState, p: &PageAddr) -> (Option<Found>, Option<&'static str>) {
        let Some(page) = st.page(p.page) else { return (None, Some("no page")) };
        // A retired page, or any page of a book retired through its door, is not live
        // (axiom 1; seqAddr 4). Asking for `.retired` still reads it.
        let asks_retired = p.face.as_ref().and_then(|f| f.tail) == Some(crate::addr::Tail::Retired);
        let book_retired = p.page != 0 && st.page(0).map(|d| d.tail() == crate::tail::PageTail::Retired).unwrap_or(false);
        if !asks_retired && (page.tail() == crate::tail::PageTail::Retired || book_retired) {
            return (None, Some("retired page"));
        }
        let Some(fp) = &p.face else { return (None, Some("no face")) };
        let counted = self.policy.is_counted(p.page, fp.face);
        let Some(face) = page.face(fp.face) else { return (None, Some("no face")) };
        match (fp.counter, fp.tail) {
            // R9: a counted face has no door/board slot; plain `FF` reads a derived listing (7).
            (None, None) if counted => {
                if face.counters.is_empty() {
                    (None, Some("no counters"))
                } else {
                    (Some(Found::Board { lines: st.board(p.page, fp.face) }), None)
                }
            }
            (Some(nn), _) => match face.counters.get(&nn) {
                Some(c) => {
                    if let Some(t) = fp.tail {
                        if c.tail.as_tail() != Some(t) {
                            return (None, Some("tail differs"));
                        }
                    }
                    (Some(Found::Counter { tail: c.tail, bodies: c.bodies.clone() }), None)
                }
                None => (None, Some("no counter")),
            },
            (None, Some(crate::addr::Tail::Draft)) => match &face.draft {
                Some(d) => (Some(Found::Draft { body: d.body.clone() }), None),
                None => (None, Some("no draft")),
            },
            (None, Some(crate::addr::Tail::Retired)) => match &face.retired {
                Some(b) => (Some(Found::Retired { body: b.clone() }), None),
                None => (None, Some("not retired")),
            },
            // R5: a seated face beats a draft at the same spot; a draft alone is found, as a draft.
            (None, _) => match (&face.seated, &face.draft) {
                (Some(b), _) => (Some(Found::Face { body: b.clone() }), None),
                (None, Some(d)) => (Some(Found::Draft { body: d.body.clone() }), None),
                (None, None) if face.retired.is_some() => (None, Some("retired")),
                _ => (None, Some("no face")),
            },
        }
    }

    /// Resolve a full face address through book -> shelf -> desk -> kernel.
    /// R5: at each spot a seated face wins; if the only copy there is a draft, the
    /// draft is found (state `draft`) and inherited like a seated face. Retired
    /// faces and retired pages are skipped and the walk goes on (A2.9; 7, see BUILD-LOG).
    pub fn resolve(&self, p: &PageAddr) -> Result<Resolution> {
        let asked = p.book_id().ok_or_else(|| SeqError::invalid("A1.7", format!("{} is short form; expand it first", p.to_form(crate::addr::Form::Short))))?;
        if p.face.is_none() {
            return Err(SeqError::invalid("A1.8", "resolve names a face; use resolve_page for a whole page"));
        }
        let mut trace = Vec::new();
        // Asking for a draft, a retired face or a specific tail is local only.
        let chain = match p.face.as_ref().and_then(|f| f.tail) {
            Some(_) => vec![asked],
            None => asked.lookup_chain(),
        };
        for (i, b) in chain.iter().enumerate() {
            let checked = PageAddr { desk: Some(b.desk), shelf: Some(b.shelf), book: Some(b.book), ..p.slot() };
            let mut checked_s = checked.to_string();
            if let Some(t) = p.face.as_ref().and_then(|f| f.tail) {
                checked_s = format!("{checked_s}.{t}");
            }
            match self.books.get(b) {
                None => trace.push(Step { step: i + 1, checked: checked_s, found: false, note: Some("no book".into()) }),
                Some(st) => {
                    let (found, why) = self.find_in(st, p);
                    let hit = found.is_some();
                    trace.push(Step { step: i + 1, checked: checked_s.clone(), found: hit, note: why.map(|s| s.to_string()) });
                    if let Some(f) = found {
                        let state = Some(f.state().to_string());
                        let why_draft = if matches!(f, Found::Draft { .. }) { draft_why(st, p) } else { None };
                        return Ok(Resolution { address: p.to_string(), source: Some(checked_s), origin: origin_for(asked, *b), found: Some(f), state, why_draft, trace });
                    }
                }
            }
        }
        Ok(Resolution { address: p.to_string(), source: None, origin: Origin::Missing, found: None, state: None, why_draft: None, trace })
    }

    /// Parse, expand against the session, and resolve (A1.2, A1.6, A1.8).
    pub fn resolve_str(&self, input: &str, active: Option<&Active>) -> Result<Resolution> {
        let a = Address::parse(input)?;
        let a = match active {
            Some(act) => a.expand(act)?,
            None => a,
        };
        match a {
            Address::Page(p) if p.is_full() => self.resolve(&p),
            Address::Page(_) => Err(SeqError::invalid("A1.2", format!("`{input}` is short form and no active book was given"))),
            _ => Err(SeqError::invalid("A1.8", format!("`{input}` is not a face address"))),
        }
    }

    /// Resolve every face of a page that exists anywhere along the chain.
    pub fn resolve_page(&self, p: &PageAddr) -> Result<BTreeMap<u8, Resolution>> {
        let asked = p.book_id().ok_or_else(|| SeqError::invalid("A1.7", "expand the page address first"))?;
        let mut faces = BTreeSet::new();
        for b in asked.lookup_chain() {
            if let Some(pg) = self.books.get(&b).and_then(|st| st.page(p.page)) {
                faces.extend(pg.faces.keys().copied());
            }
        }
        let mut out = BTreeMap::new();
        for f in faces {
            let fa = p.page_only().with_face(crate::addr::FacePart::face(f));
            let r = self.resolve(&fa)?;
            if r.found.is_some() {
                out.insert(f, r);
            }
        }
        Ok(out)
    }

    /// Check a title written in an address against the stamp (A2.8, A3.2).
    /// No title written: Ok. Mismatch: elevated. No stamp: missing.
    pub fn check_title(&self, p: &PageAddr) -> Result<()> {
        let Some(want) = &p.title else { return Ok(()) };
        let stamp_addr = p.page_only().with_face(crate::addr::FacePart::face(0));
        let r = self.resolve(&stamp_addr)?;
        let body = match r.found {
            Some(Found::Face { body }) | Some(Found::Draft { body }) => body,
            _ => return Err(SeqError::missing("A2.8", format!("{} has no stamp to check the title `{want}` against", p.page_only()))),
        };
        let stamp = crate::cards::parse_stamp(&body);
        match stamp.title() {
            Some(t) if t == want => Ok(()),
            Some(t) => Err(SeqError::elevate("A2.8", format!("address says `{want}` but the stamp says `{t}`"))),
            None => Err(SeqError::elevate("A2.8", format!("address says `{want}` but the stamp has no title"))),
        }
    }
}
