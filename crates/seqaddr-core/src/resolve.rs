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
    /// The derived board of a counted face (`FF` or `FF.00`).
    Board { lines: Vec<BoardLine> },
    /// A draft, only when asked for `FF.draft`.
    Draft { body: String },
    /// A retired face, only when asked for `FF.retired`.
    Retired { body: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Resolution {
    /// The full address asked for.
    pub address: String,
    /// The full address where it was found.
    pub source: Option<String>,
    pub origin: Origin,
    pub found: Option<Found>,
    pub trace: Vec<Step>,
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
        let Some(fp) = &p.face else { return (None, Some("no face")) };
        let counted = self.policy.is_counted(p.page, fp.face);
        let Some(face) = page.face(fp.face) else { return (None, Some("no face")) };
        match (fp.counter, fp.tail) {
            (Some(0), _) | (None, None) if counted => {
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
            (None, _) => match &face.seated {
                Some(b) => (Some(Found::Face { body: b.clone() }), None),
                None if face.draft.is_some() => (None, Some("draft only")),
                None if face.retired.is_some() => (None, Some("retired")),
                None => (None, Some("no face")),
            },
        }
    }

    /// Resolve a full face address through book -> shelf -> desk -> kernel.
    /// Drafts and retired faces are not live and are never inherited.
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
                        return Ok(Resolution { address: p.to_string(), source: Some(checked_s), origin: origin_for(asked, *b), found: Some(f), trace });
                    }
                }
            }
        }
        Ok(Resolution { address: p.to_string(), source: None, origin: Origin::Missing, found: None, trace })
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
            Some(Found::Face { body }) => body,
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
