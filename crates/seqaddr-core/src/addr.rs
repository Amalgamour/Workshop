//! Address grammar (seqAddr.md sections 1-4 and 8; decisions A1, A2, A4, C8.2).
//!
//! ```text
//! address    = container / page-addr / active-rel
//! container  = desk [ "." shelf [ "." book ] ] [ "." title ]
//! page-addr  = [ ancestors "." ] page [ "." page-end ]
//! page-end   = face-part / title [ "." page-tail ] / page-tail
//! active-rel = "." face-part
//! face-part  = face [ "." counter ] [ "." tail ] [ "." card [ "." brand ] ]
//! ```

use crate::error::{Result, SeqError};
use serde::{Deserialize, Serialize};
use std::fmt;

/// The six tail words (seqAddr 4, A2.5). They are reserved and never titles or card keys.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Tail {
    Draft,
    Retired,
    Pack,
    Open,
    Return,
    Review,
}

impl Tail {
    pub const ALL: [Tail; 6] = [Tail::Draft, Tail::Retired, Tail::Pack, Tail::Open, Tail::Return, Tail::Review];

    pub fn as_str(self) -> &'static str {
        match self {
            Tail::Draft => "draft",
            Tail::Retired => "retired",
            Tail::Pack => "pack",
            Tail::Open => "open",
            Tail::Return => "return",
            Tail::Review => "review",
        }
    }

    pub fn from_word(w: &str) -> Option<Tail> {
        Tail::ALL.iter().copied().find(|t| t.as_str() == w)
    }

    /// Page-level tails: `draft`, `retired` (A2.5).
    pub fn allowed_on_page(self) -> bool {
        matches!(self, Tail::Draft | Tail::Retired)
    }
    /// Seated-face tails: `draft`, `retired` (A2.5).
    pub fn allowed_on_face(self) -> bool {
        matches!(self, Tail::Draft | Tail::Retired)
    }
    /// Counter tails: `draft`, `pack`, `open`, `return`, `review` (A2.5). Bare = closed.
    pub fn allowed_on_counter(self) -> bool {
        !matches!(self, Tail::Retired)
    }
}

impl fmt::Display for Tail {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// True for a reserved tail word (A2.5).
pub fn is_tail_word(w: &str) -> bool {
    Tail::from_word(w).is_some()
}

/// Title / card-key characters: lowercase letters, digits, hyphens; starts with a letter (A2.3).
pub fn is_word(w: &str) -> bool {
    let mut ch = w.chars();
    match ch.next() {
        Some(c) if c.is_ascii_lowercase() => {}
        _ => return false,
    }
    ch.all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-')
}

/// Check a title (A2.3, A2.5): word characters and not a tail word.
pub fn check_title(w: &str) -> Result<()> {
    if !is_word(w) {
        return Err(SeqError::invalid("A2.3", format!("`{w}` is not a title: lowercase letters, digits, hyphens, starting with a letter")));
    }
    if is_tail_word(w) {
        return Err(SeqError::invalid("A2.5", format!("`{w}` is a tail word and can never be a title")));
    }
    Ok(())
}

/// A book's identity: desk, shelf, book (format 1.3: one file per book).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct BookId {
    pub desk: u8,
    pub shelf: u8,
    pub book: u8,
}

impl BookId {
    pub const KERNEL: BookId = BookId { desk: 0, shelf: 0, book: 0 };

    pub fn new(desk: u8, shelf: u8, book: u8) -> Self {
        BookId { desk, shelf, book }
    }

    /// Parse `DD.SS.BB` exactly (no title).
    pub fn parse(s: &str) -> Result<BookId> {
        match Address::parse(s)? {
            Address::Container(c) if c.shelf.is_some() && c.book.is_some() && c.title.is_none() => {
                Ok(BookId::new(c.desk, c.shelf.unwrap(), c.book.unwrap()))
            }
            _ => Err(SeqError::invalid("A1.3", format!("`{s}` is not a book address DD.SS.BB"))),
        }
    }

    pub fn is_kernel(&self) -> bool {
        *self == BookId::KERNEL
    }
    /// `DD.00.00`: the desk's own book (A4.1).
    pub fn is_desk_own(&self) -> bool {
        self.shelf == 0 && self.book == 0
    }
    /// `DD.00.BB` with BB != 00: a desk book, owned by the desk, no shelf (A4.1).
    pub fn is_desk_book(&self) -> bool {
        self.shelf == 0 && self.book != 0
    }
    /// `DD.SS.00` with SS != 00: the shelf's own book (A4.1).
    pub fn is_shelf_own(&self) -> bool {
        self.shelf != 0 && self.book == 0
    }
    /// Kernel or a desk's book (desk own book or desk book). Face 03 may be used anywhere here (C6).
    pub fn is_kernel_or_desk_book(&self) -> bool {
        self.is_kernel() || self.shelf == 0
    }

    /// The finding order (A1.8, A4.1): book -> shelf -> desk -> kernel, without repeats.
    pub fn lookup_chain(&self) -> Vec<BookId> {
        let mut out = vec![*self];
        let mut push = |b: BookId| {
            if !out.contains(&b) {
                out.push(b)
            }
        };
        push(BookId::new(self.desk, self.shelf, 0));
        push(BookId::new(self.desk, 0, 0));
        push(BookId::KERNEL);
        out
    }

    /// The identity page address of this container, `DD.SS.BB.0000` (A3.1).
    pub fn identity_page(&self) -> PageAddr {
        PageAddr::full(*self, 0)
    }

    /// File name in `books/` (lane contract): `DD.SS.BB.book`.
    pub fn file_name(&self) -> String {
        format!("{self}.book")
    }
}

impl fmt::Display for BookId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:02}.{:02}.{:02}", self.desk, self.shelf, self.book)
    }
}

/// What a desk number is for (seqAddr 1.3, A6.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DeskKind {
    Kernel,
    KernelBranch,
    User,
    Pointer,
}

pub fn desk_kind(d: u8) -> DeskKind {
    match d {
        0 => DeskKind::Kernel,
        1..=9 => DeskKind::KernelBranch,
        10..=98 => DeskKind::User,
        _ => DeskKind::Pointer,
    }
}

/// Role of a value on a two-digit container axis (seqAddr 1.2).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum AxisRole {
    /// `00`: the owner of the level above, itself (A4.1).
    Owner,
    /// `01-09`: reserved.
    Reserved,
    Normal,
    /// `99`: pointer, look for the next location (A5.1).
    Pointer,
}

pub fn axis_role(v: u8) -> AxisRole {
    match v {
        0 => AxisRole::Owner,
        1..=9 => AxisRole::Reserved,
        99 => AxisRole::Pointer,
        _ => AxisRole::Normal,
    }
}

/// What a page number is (seqAddr 6, 6.1, A2.6, A2.7).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum PageKind {
    /// `0000`: book identity (sentinel).
    Identity,
    /// `0001-0009`: special reserved.
    SpecialReserved,
    /// `0010-0019`: contents, dictionary, concordance.
    Required,
    /// `0020-0049`: localized behaviour.
    Localized,
    /// `0050-0099`: structural.
    Structural,
    /// `PP00` at or above 0100.
    BandHead,
    /// `PP99` below 9999: band continuation.
    BandContinuation,
    /// Item in a kernel-modelled band (0100-0999).
    StandardBand,
    /// Item in user space (1000-9998).
    User,
    /// `9999`: book continuation (sentinel).
    BookContinuation,
}

pub fn page_kind(p: u16) -> PageKind {
    match p {
        0 => PageKind::Identity,
        1..=9 => PageKind::SpecialReserved,
        10..=19 => PageKind::Required,
        20..=49 => PageKind::Localized,
        50..=99 => PageKind::Structural,
        9999 => PageKind::BookContinuation,
        _ if p % 100 == 0 => PageKind::BandHead,
        _ if p % 100 == 99 => PageKind::BandContinuation,
        100..=999 => PageKind::StandardBand,
        _ => PageKind::User,
    }
}

/// The band digit `D` of `NDNN` (A2.6). `None` below 0100 (no band).
pub fn band_of(p: u16) -> Option<u8> {
    if p < 100 || p > 9999 {
        None
    } else {
        Some(((p / 100) % 10) as u8)
    }
}

/// The band head `PP00` of a page at or above 0100 (A2.6).
pub fn band_head(p: u16) -> Option<u16> {
    if p < 100 {
        None
    } else {
        Some(p - p % 100)
    }
}

/// The set key `(N, NN)` shared by pages of one set across bands (A2.6).
pub fn set_key(p: u16) -> Option<(u8, u8)> {
    if p < 100 {
        None
    } else {
        Some(((p / 1000) as u8, (p % 100) as u8))
    }
}

/// True if the page number is a sentinel on the page axis (all 0s or all 9s).
pub fn is_page_sentinel(p: u16) -> bool {
    p == 0 || p == 9999
}
/// True if a two-digit axis value is a sentinel (00 or 99).
pub fn is_axis_sentinel(v: u8) -> bool {
    v == 0 || v == 99
}

/// A face, its counter, tail, card and brand (`face-part`).
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct FacePart {
    pub face: u8,
    pub counter: Option<u8>,
    pub tail: Option<Tail>,
    pub card: Option<String>,
    pub brand: Option<u16>,
}

impl FacePart {
    pub fn face(face: u8) -> Self {
        FacePart { face, counter: None, tail: None, card: None, brand: None }
    }
    pub fn counter(face: u8, counter: u8) -> Self {
        FacePart { face, counter: Some(counter), tail: None, card: None, brand: None }
    }
}

impl fmt::Display for FacePart {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:02}", self.face)?;
        if let Some(c) = self.counter {
            write!(f, ".{c:02}")?;
        }
        if let Some(t) = self.tail {
            write!(f, ".{t}")?;
        }
        if let Some(c) = &self.card {
            write!(f, ".{c}")?;
        }
        if let Some(b) = self.brand {
            write!(f, ".{b:03}")?;
        }
        Ok(())
    }
}

/// A container address: desk, shelf or book, with an optional title (A1.3).
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ContainerAddr {
    pub desk: u8,
    pub shelf: Option<u8>,
    pub book: Option<u8>,
    pub title: Option<String>,
}

impl ContainerAddr {
    /// The book file that holds this container's own pages (A4.1, format 1.3):
    /// desk `10` -> `10.00.00`, shelf `10.11` -> `10.11.00`, book -> itself.
    pub fn own_book(&self) -> BookId {
        BookId::new(self.desk, self.shelf.unwrap_or(0), self.book.unwrap_or(0))
    }
    /// The identity page (A3.1): book `10.11.21` -> `10.11.21.0000`, shelf `10.11` -> `10.11.00.0000`.
    pub fn identity_page(&self) -> PageAddr {
        PageAddr::full(self.own_book(), 0)
    }
    pub fn level(&self) -> ContainerLevel {
        match (self.shelf, self.book) {
            (None, _) => ContainerLevel::Desk,
            (Some(_), None) => ContainerLevel::Shelf,
            _ => ContainerLevel::Book,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ContainerLevel {
    Desk,
    Shelf,
    Book,
}

impl fmt::Display for ContainerAddr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:02}", self.desk)?;
        if let Some(s) = self.shelf {
            write!(f, ".{s:02}")?;
        }
        if let Some(b) = self.book {
            write!(f, ".{b:02}")?;
        }
        if let Some(t) = &self.title {
            write!(f, ".{t}")?;
        }
        Ok(())
    }
}

/// A page address, possibly short (ancestors left out) and possibly with a face part.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PageAddr {
    pub desk: Option<u8>,
    pub shelf: Option<u8>,
    pub book: Option<u8>,
    pub page: u16,
    /// Title after the page (only without a face part).
    pub title: Option<String>,
    /// Page tail `draft` / `retired` (only without a face part).
    pub page_tail: Option<Tail>,
    pub face: Option<FacePart>,
}

/// How many ancestors are written (seqAddr 2.1).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Form {
    /// `PPPP...`
    Short,
    /// `BB.PPPP...`
    Book,
    /// `SS.BB.PPPP...`
    Shelf,
    /// `DD.SS.BB.PPPP...`
    Full,
}

impl PageAddr {
    pub fn full(book: BookId, page: u16) -> Self {
        PageAddr {
            desk: Some(book.desk),
            shelf: Some(book.shelf),
            book: Some(book.book),
            page,
            title: None,
            page_tail: None,
            face: None,
        }
    }
    pub fn with_face(mut self, fp: FacePart) -> Self {
        self.face = Some(fp);
        self
    }
    pub fn form(&self) -> Form {
        match (self.desk, self.shelf, self.book) {
            (Some(_), Some(_), Some(_)) => Form::Full,
            (None, Some(_), Some(_)) => Form::Shelf,
            (None, None, Some(_)) => Form::Book,
            _ => Form::Short,
        }
    }
    pub fn is_full(&self) -> bool {
        self.form() == Form::Full
    }
    /// The book, if the address is full.
    pub fn book_id(&self) -> Option<BookId> {
        match (self.desk, self.shelf, self.book) {
            (Some(d), Some(s), Some(b)) => Some(BookId::new(d, s, b)),
            _ => None,
        }
    }
    /// Fill missing ancestors from the active book (A1.2).
    pub fn expand(&self, active: BookId) -> PageAddr {
        let mut out = self.clone();
        out.book = Some(self.book.unwrap_or(active.book));
        out.shelf = Some(self.shelf.unwrap_or(active.shelf));
        out.desk = Some(self.desk.unwrap_or(active.desk));
        out
    }
    /// Write the address in a given form. Ancestors that are not known are left out.
    pub fn to_form(&self, form: Form) -> String {
        let mut parts: Vec<String> = Vec::new();
        if form >= Form::Full {
            if let Some(d) = self.desk {
                parts.push(format!("{d:02}"));
            }
        }
        if form >= Form::Shelf {
            if let Some(s) = self.shelf {
                parts.push(format!("{s:02}"));
            }
        }
        if form >= Form::Book {
            if let Some(b) = self.book {
                parts.push(format!("{b:02}"));
            }
        }
        parts.push(format!("{:04}", self.page));
        if let Some(fp) = &self.face {
            parts.push(fp.to_string());
        } else {
            if let Some(t) = &self.title {
                parts.push(t.clone());
            }
            if let Some(t) = self.page_tail {
                parts.push(t.to_string());
            }
        }
        parts.join(".")
    }
    /// The page itself, without title, tail or face.
    pub fn page_only(&self) -> PageAddr {
        PageAddr { title: None, page_tail: None, face: None, ..self.clone() }
    }
    /// The slot: page and face (and counter), dropping tail, card, brand and title.
    pub fn slot(&self) -> PageAddr {
        let face = self.face.as_ref().map(|f| FacePart { face: f.face, counter: f.counter, tail: None, card: None, brand: None });
        PageAddr { title: None, page_tail: None, face, ..self.clone() }
    }
    /// The tail written on this address, at whichever level.
    pub fn tail(&self) -> Option<Tail> {
        match &self.face {
            Some(f) => f.tail,
            None => self.page_tail,
        }
    }
}

impl fmt::Display for PageAddr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.to_form(Form::Full))
    }
}

/// Any address (seqAddr 8).
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Address {
    Container(ContainerAddr),
    Page(PageAddr),
    /// Leading dot: relative to the active page (A1.6).
    ActiveRel(FacePart),
}

impl fmt::Display for Address {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Address::Container(c) => c.fmt(f),
            Address::Page(p) => p.fmt(f),
            Address::ActiveRel(fp) => write!(f, ".{fp}"),
        }
    }
}

/// The session context used to expand short and leading-dot addresses (A1.2, A1.6).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Active {
    pub book: BookId,
    /// Active pages. One for `.04`; more than one makes `.04` ambiguous.
    pub pages: Vec<u16>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum Seg<'a> {
    Digits(&'a str),
    Word(&'a str),
}

fn classify<'a>(seg: &'a str, input: &str) -> Result<Seg<'a>> {
    if seg.is_empty() {
        return Err(SeqError::invalid("seqAddr 8", format!("`{input}` has an empty group (two dots or a trailing dot)")));
    }
    if seg.chars().all(|c| c.is_ascii_digit()) {
        return match seg.len() {
            1 => Err(SeqError::invalid("E3", format!("`{seg}` in `{input}`: a one-digit mark is an axiom, never an address part"))),
            2 | 3 | 4 => Ok(Seg::Digits(seg)),
            _ => Err(SeqError::invalid("A1.5", format!("`{seg}` in `{input}`: widths are exact (2, 3 or 4 digits)"))),
        };
    }
    if seg.chars().next().map(|c| c.is_ascii_digit()).unwrap_or(false) && seg.chars().all(|c| c.is_ascii_alphanumeric()) {
        // e.g. `4442a` - not a number and not a word
        return Err(SeqError::invalid("A2.3", format!("`{seg}` in `{input}` is neither a number group nor a word")));
    }
    if !is_word(seg) {
        return Err(SeqError::invalid("A2.3", format!("`{seg}` in `{input}`: words are lowercase letters, digits, hyphens, starting with a letter")));
    }
    Ok(Seg::Word(seg))
}

fn two(seg: &str) -> u8 {
    seg.parse().expect("checked digits")
}

impl Address {
    /// Read an address (A1.8 "reading"): well formed or not. Needs no context.
    pub fn parse(input: &str) -> Result<Address> {
        if input.is_empty() {
            return Err(SeqError::invalid("seqAddr 8", "empty address"));
        }
        if input.trim() != input || input.contains(char::is_whitespace) {
            return Err(SeqError::invalid("A2.3", format!("`{input}` contains spaces")));
        }
        if let Some(rest) = input.strip_prefix('.') {
            let segs = rest.split('.').map(|s| classify(s, input)).collect::<Result<Vec<_>>>()?;
            let (fp, used) = parse_face_part(&segs, 0, input)?;
            if used != segs.len() {
                return Err(SeqError::invalid("A1.6", format!("`{input}`: a leading dot is followed only by a face part")));
            }
            let fp = fp.ok_or_else(|| SeqError::invalid("A1.6", format!("`{input}`: a leading dot needs a face")))?;
            check_face_rules(&fp, input)?;
            return Ok(Address::ActiveRel(fp));
        }
        let segs = input.split('.').map(|s| classify(s, input)).collect::<Result<Vec<_>>>()?;
        let page_positions: Vec<usize> = segs
            .iter()
            .enumerate()
            .filter(|(_, s)| matches!(s, Seg::Digits(d) if d.len() == 4))
            .map(|(i, _)| i)
            .collect();
        if page_positions.len() > 1 {
            return Err(SeqError::invalid("A1.2", format!("`{input}` has more than one 4-digit page group")));
        }
        if let Some(&pi) = page_positions.first() {
            parse_page_addr(&segs, pi, input).map(Address::Page)
        } else {
            parse_container(&segs, input).map(Address::Container)
        }
    }

    /// Expand to a full address using the session context (A1.1, A1.2, A1.6).
    /// Containers are already full (A1.3). A leading dot with no active page is
    /// missing (7); with several active pages it is elevated (A1.6).
    pub fn expand(&self, active: &Active) -> Result<Address> {
        match self {
            Address::Container(_) => Ok(self.clone()),
            Address::Page(p) => Ok(Address::Page(p.expand(active.book))),
            Address::ActiveRel(fp) => match active.pages.as_slice() {
                [] => Err(SeqError::missing("A1.6", format!("`{self}`: no active page"))),
                [p] => Ok(Address::Page(PageAddr::full(active.book, *p).with_face(fp.clone()))),
                _ => Err(SeqError::elevate("A1.6", format!("`{self}`: several pages are active; ask the user which one"))),
            },
        }
    }

    /// Parse and require a full page or face address (what models write, A1.7).
    pub fn parse_full_page(input: &str) -> Result<PageAddr> {
        match Address::parse(input)? {
            Address::Page(p) if p.is_full() => Ok(p),
            Address::Page(_) => Err(SeqError::invalid("A1.7", format!("`{input}` is short form; the full address DD.SS.BB.PPPP is required here"))),
            _ => Err(SeqError::invalid("A1.2", format!("`{input}` is not a page or face address"))),
        }
    }

    pub fn as_page(&self) -> Option<&PageAddr> {
        match self {
            Address::Page(p) => Some(p),
            _ => None,
        }
    }
}

impl std::str::FromStr for Address {
    type Err = SeqError;
    fn from_str(s: &str) -> Result<Self> {
        Address::parse(s)
    }
}

fn parse_container(segs: &[Seg<'_>], input: &str) -> Result<ContainerAddr> {
    let mut nums = Vec::new();
    let mut i = 0;
    while i < segs.len() {
        match segs[i] {
            Seg::Digits(d) if d.len() == 2 => nums.push(two(d)),
            Seg::Digits(d) => {
                return Err(SeqError::invalid("A1.5", format!("`{d}` in `{input}`: container groups are exactly 2 digits")));
            }
            Seg::Word(_) => break,
        }
        i += 1;
    }
    if nums.is_empty() {
        return Err(SeqError::invalid("A1.3", format!("`{input}`: an address starts with a desk or a page")));
    }
    if nums.len() > 3 {
        return Err(SeqError::invalid("A1.3", format!("`{input}`: a container is at most desk.shelf.book; a page needs 4 digits")));
    }
    let mut title = None;
    if i < segs.len() {
        let w = match segs[i] {
            Seg::Word(w) => w,
            _ => unreachable!(),
        };
        if is_tail_word(w) {
            return Err(SeqError::invalid("A2.5", format!("`{input}`: desks, shelves and books take no tail; state comes from the identity page (`...0000.{w}`)")));
        }
        check_title(w)?;
        title = Some(w.to_string());
        i += 1;
    }
    if i < segs.len() {
        return Err(SeqError::invalid("A2.5", format!("`{input}`: nothing may follow a container title")));
    }
    Ok(ContainerAddr { desk: nums[0], shelf: nums.get(1).copied(), book: nums.get(2).copied(), title })
}

fn parse_page_addr(segs: &[Seg<'_>], pi: usize, input: &str) -> Result<PageAddr> {
    if pi > 3 {
        return Err(SeqError::invalid("A1.2", format!("`{input}`: at most desk.shelf.book may stand left of the page")));
    }
    let mut anc = Vec::new();
    for s in &segs[..pi] {
        match s {
            Seg::Digits(d) if d.len() == 2 => anc.push(two(d)),
            Seg::Digits(d) => return Err(SeqError::invalid("A1.5", format!("`{d}` in `{input}`: ancestors are exactly 2 digits"))),
            Seg::Word(w) => {
                return Err(SeqError::invalid("seqAddr 8", format!("`{w}` in `{input}`: a title goes only at the end of an address (ancestors carry no titles)")))
            }
        }
    }
    let page: u16 = match segs[pi] {
        Seg::Digits(d) => d.parse().unwrap(),
        _ => unreachable!(),
    };
    // Left of the page, read right to left: BB, SS, DD (A1.2).
    let (desk, shelf, book) = match anc.len() {
        0 => (None, None, None),
        1 => (None, None, Some(anc[0])),
        2 => (None, Some(anc[0]), Some(anc[1])),
        _ => (Some(anc[0]), Some(anc[1]), Some(anc[2])),
    };
    let mut out = PageAddr { desk, shelf, book, page, title: None, page_tail: None, face: None };
    let rest = &segs[pi + 1..];
    if rest.is_empty() {
        return Ok(out);
    }
    match rest[0] {
        Seg::Digits(_) => {
            let (fp, used) = parse_face_part(rest, 0, input)?;
            if used != rest.len() {
                return Err(trailing(rest, used, input));
            }
            let fp = fp.unwrap();
            check_face_rules(&fp, input)?;
            out.face = Some(fp);
        }
        Seg::Word(w) => {
            let mut j = 0;
            if let Some(t) = Tail::from_word(w) {
                if !t.allowed_on_page() {
                    return Err(SeqError::invalid("A2.5", format!("`{input}`: `{w}` is a counter tail; a page takes only `draft` or `retired`")));
                }
                out.page_tail = Some(t);
                j = 1;
            } else {
                check_title(w)?;
                out.title = Some(w.to_string());
                j += 1;
                if let Some(Seg::Word(w2)) = rest.get(1) {
                    match Tail::from_word(w2) {
                        Some(t) if t.allowed_on_page() => {
                            out.page_tail = Some(t);
                            j += 1;
                        }
                        Some(_) => {
                            return Err(SeqError::invalid("A2.5", format!("`{input}`: `{w2}` is a counter tail; a page takes only `draft` or `retired`")))
                        }
                        None => return Err(SeqError::invalid("A2.5", format!("`{input}`: only a tail may follow a title"))),
                    }
                }
            }
            if j < rest.len() {
                return Err(match rest[j] {
                    Seg::Digits(_) if out.title.is_some() => SeqError::invalid("A2.2", format!("`{input}`: a face follows the page directly; titles never sit between a page and its face")),
                    _ => trailing(rest, j, input),
                });
            }
            if out.title.is_some() && page == 0 {
                return Err(SeqError::invalid("A2.8", format!("`{input}`: page 0000 has no title (it holds the container's title in its stamp)")));
            }
        }
    }
    Ok(out)
}

fn trailing(rest: &[Seg<'_>], at: usize, input: &str) -> SeqError {
    let what = match rest[at] {
        Seg::Digits(d) | Seg::Word(d) => d,
    };
    SeqError::invalid("seqAddr 8", format!("`{input}`: unexpected `{what}`"))
}

/// Parse `face [ . counter ] [ . tail ] [ . card [ . brand ] ]` starting at `i`.
fn parse_face_part(segs: &[Seg<'_>], mut i: usize, input: &str) -> Result<(Option<FacePart>, usize)> {
    let face = match segs.get(i) {
        Some(Seg::Digits(d)) if d.len() == 2 => two(d),
        Some(Seg::Digits(d)) => return Err(SeqError::invalid("A1.5", format!("`{d}` in `{input}`: a face is exactly 2 digits"))),
        _ => return Ok((None, i)),
    };
    i += 1;
    let mut fp = FacePart::face(face);
    if let Some(Seg::Digits(d)) = segs.get(i) {
        if d.len() == 3 {
            return Err(SeqError::invalid("C8.2", format!("`{d}` in `{input}`: a 3-digit group is a brand and needs a card before it")));
        }
        if d.len() != 2 {
            return Err(SeqError::invalid("A1.5", format!("`{d}` in `{input}`: a counter is exactly 2 digits")));
        }
        fp.counter = Some(two(d));
        i += 1;
    }
    if let Some(Seg::Word(w)) = segs.get(i) {
        if let Some(t) = Tail::from_word(w) {
            fp.tail = Some(t);
            i += 1;
        }
    }
    if let Some(Seg::Word(w)) = segs.get(i) {
        if is_tail_word(w) {
            return Err(SeqError::invalid("A2.5", format!("`{input}`: only one tail, and it comes before any card key")));
        }
        fp.card = Some(w.to_string());
        i += 1;
        if let Some(Seg::Digits(d)) = segs.get(i) {
            if d.len() != 3 {
                return Err(SeqError::invalid("C8.2", format!("`{d}` in `{input}`: after a card only a 3-digit brand number may follow")));
            }
            fp.brand = Some(d.parse().unwrap());
            i += 1;
        }
    } else if let Some(Seg::Digits(d)) = segs.get(i) {
        if d.len() == 3 {
            return Err(SeqError::invalid("C8.2", format!("`{d}` in `{input}`: a 3-digit group is a brand and needs a card before it")));
        }
        if fp.counter.is_some() {
            return Err(SeqError::invalid("A1.4", format!("`{d}` in `{input}`: counters are not an axis; only one counter follows a face")));
        }
    }
    Ok((Some(fp), i))
}

/// Rules the grammar does not express (seqAddr 8, A2.5, A4.4, A4.5, C8.5).
fn check_face_rules(fp: &FacePart, input: &str) -> Result<()> {
    match (fp.counter, fp.tail) {
        (None, Some(t)) if !t.allowed_on_face() => {
            return Err(SeqError::invalid("A2.5", format!("`{input}`: `{t}` is a workflow tail and lives only on counters")));
        }
        (Some(_), Some(Tail::Retired)) => {
            return Err(SeqError::invalid("A2.5", format!("`{input}`: `retired` is used only without a counter")));
        }
        (Some(0), Some(t)) => {
            return Err(SeqError::invalid("A4.4", format!("`{input}`: `FF.00` is the board, derived by the compute; it takes no tail `{t}` (provisional, see BUILD-LOG)")));
        }
        (Some(99), Some(t)) => {
            return Err(SeqError::invalid("A5.1", format!("`{input}`: `FF.99` is a pointer, never content; it takes no tail `{t}` (provisional, see BUILD-LOG)")));
        }
        _ => {}
    }
    if let Some(b) = fp.brand {
        if b == 0 || b == 999 {
            return Err(SeqError::invalid("C8.5", format!("`{input}`: brand numbers 000 and 999 are reserved; brands run 001-998")));
        }
    }
    Ok(())
}

/// Counter role (seqAddr 8 grammar comment, A4.4, A4.5).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum CounterRole {
    Board,
    Item,
    Continuation,
}

pub fn counter_role(nn: u8) -> CounterRole {
    match nn {
        0 => CounterRole::Board,
        99 => CounterRole::Continuation,
        _ => CounterRole::Item,
    }
}
