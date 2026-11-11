//! The page file in memory: a page id, ordered sections, blocks, history.

use seqaddr_core::addr::{Address, BookId};
use seqaddr_core::face::face_job;
use seqaddr_core::log::{BookLog, Entry};
use seqaddr_core::validate::OpRequest;
use std::collections::BTreeSet;
use std::fmt;

/// One page: `DD.SS.BB.PPPP`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct PageId {
    pub book: BookId,
    pub page: u16,
}

impl PageId {
    pub fn new(book: BookId, page: u16) -> Self {
        PageId { book, page }
    }
    /// Parse a full page address (`DD.SS.BB.PPPP`, an optional title is allowed and ignored here).
    pub fn parse(s: &str) -> Result<PageId, String> {
        let p = Address::parse_full_page(s).map_err(|e| e.to_string())?;
        if p.face.is_some() {
            return Err(format!("`{s}` names a face; a page address is DD.SS.BB.PPPP"));
        }
        let book = p.book_id().ok_or_else(|| format!("`{s}` is not a full address"))?;
        Ok(PageId { book, page: p.page })
    }
    /// The address of one section of this page.
    pub fn section_addr(&self, key: SectionKey) -> String {
        match key.counter {
            None => format!("{self}.{:02}", key.face),
            Some(nn) => format!("{self}.{:02}.{nn:02}", key.face),
        }
    }
}

impl fmt::Display for PageId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{:04}", self.book, self.page)
    }
}

/// Where a block sits: face 00 (the door; also page-level entries), a face's
/// own slot, or one counter `FF.NN`. Ordered door, 01, 05, 05.01, 05.02, 06 ...
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SectionKey {
    pub face: u8,
    pub counter: Option<u8>,
}

impl SectionKey {
    pub const DOOR: SectionKey = SectionKey { face: 0, counter: None };
    pub fn face(face: u8) -> Self {
        SectionKey { face, counter: None }
    }
    pub fn counter(face: u8, nn: u8) -> Self {
        SectionKey { face, counter: Some(nn) }
    }
    pub fn is_door(&self) -> bool {
        *self == Self::DOOR
    }
    /// The face's name in a section header (`law`, `notes`, ...; R1 `door`).
    pub fn name(&self) -> &'static str {
        face_job(self.face).name()
    }
}

/// The page and section an entry address belongs to. `None` when the address
/// is not a full page address (book-level entries such as snapshots).
pub fn slot_of(addr: &str) -> Option<(PageId, SectionKey)> {
    let p = Address::parse_full_page(addr).ok()?;
    let book = p.book_id()?;
    let key = match &p.face {
        None => SectionKey::DOOR,
        Some(fp) => match fp.counter {
            None => SectionKey::face(fp.face),
            Some(nn) => SectionKey::counter(fp.face, nn),
        },
    };
    Some((PageId::new(book, p.page), key))
}

/// Every page that has at least one entry in the book, in page order.
pub fn pages_in(log: &BookLog) -> Vec<PageId> {
    let set: BTreeSet<PageId> = log.entries.iter().filter_map(|e| slot_of(&e.addr)).map(|(p, _)| p).collect();
    set.into_iter().collect()
}

/// The entries of one page, in book order.
pub fn page_entries(log: &BookLog, page: PageId) -> Vec<Entry> {
    log.entries.iter().filter(|e| slot_of(&e.addr).map(|(p, _)| p == page).unwrap_or(false)).cloned().collect()
}

/// A derived line `key := value`: computed on export, checked on read, never imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Derived {
    pub line: usize,
    pub key: String,
    pub value: String,
}

#[derive(Debug, Clone, PartialEq)]
pub enum BlockKind {
    /// `--- @n ...`: an entry already in the book. Read-only history.
    Booked(Entry),
    /// `--- new ...`: a write the reader proposes. Becomes one proposal op.
    New(OpRequest),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Block {
    pub line: usize,
    pub kind: BlockKind,
    pub derived: Vec<Derived>,
}

impl Block {
    pub fn addr(&self) -> &str {
        match &self.kind {
            BlockKind::Booked(e) => &e.addr,
            BlockKind::New(o) => &o.addr,
        }
    }
    pub fn body(&self) -> Option<&str> {
        match &self.kind {
            BlockKind::Booked(e) => e.body.as_deref(),
            BlockKind::New(o) => o.body.as_deref(),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Section {
    pub key: SectionKey,
    pub line: usize,
    /// Name as written in the header (`law`), checked against the face number.
    pub name: Option<String>,
    /// Address as written in the header.
    pub addr: String,
    pub derived: Vec<Derived>,
    pub blocks: Vec<Block>,
}

/// One history line `@n op addr`.
#[derive(Debug, Clone, PartialEq)]
pub struct HistLine {
    pub line: usize,
    pub n: u64,
    pub op: String,
    pub addr: String,
}

/// A parsed `.seq` file.
#[derive(Debug, Clone, PartialEq)]
pub struct SeqPage {
    pub page: PageId,
    pub sections: Vec<Section>,
    pub history: Vec<HistLine>,
}

impl SeqPage {
    /// The booked entries, in book order (by `n`). This is the lossless part.
    pub fn booked(&self) -> Vec<Entry> {
        let mut v: Vec<Entry> = self
            .sections
            .iter()
            .flat_map(|s| s.blocks.iter())
            .filter_map(|b| match &b.kind {
                BlockKind::Booked(e) => Some(e.clone()),
                _ => None,
            })
            .collect();
        v.sort_by_key(|e| e.n);
        v
    }
    /// The proposed writes, in file order.
    pub fn proposed(&self) -> Vec<OpRequest> {
        self.sections
            .iter()
            .flat_map(|s| s.blocks.iter())
            .filter_map(|b| match &b.kind {
                BlockKind::New(o) => Some(o.clone()),
                _ => None,
            })
            .collect()
    }
}
