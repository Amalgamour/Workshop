//! Address grammar from seqAddr.md section 8.
//!
//! A short group is rejected. It is not padded out to the width of an axis.

use std::fmt;

/// Where a short address takes its missing ancestors, and which page a leading dot names.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Context {
    pub book: Option<BookId>,
    /// Page numbers in `book`. A leading dot needs exactly one.
    pub active_pages: Vec<u16>,
}

impl Context {
    pub fn empty() -> Self {
        Self {
            book: None,
            active_pages: Vec::new(),
        }
    }

    pub fn new(book: Option<BookId>, active_pages: Vec<u16>) -> Self {
        Self { book, active_pages }
    }
}

/// Desk, shelf, and book. Each axis is two digits.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct BookId {
    pub desk: u8,
    pub shelf: u8,
    pub book: u8,
}

impl BookId {
    pub fn canonical(self) -> String {
        format!("{:02}.{:02}.{:02}", self.desk, self.shelf, self.book)
    }
}

/// A tail word. `closed` is the bare counter, so it is not a tail.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Tail {
    Draft,
    Pack,
    Open,
    Return,
    Review,
    Retired,
}

impl Tail {
    pub fn as_str(self) -> &'static str {
        match self {
            Tail::Draft => "draft",
            Tail::Pack => "pack",
            Tail::Open => "open",
            Tail::Return => "return",
            Tail::Review => "review",
            Tail::Retired => "retired",
        }
    }

    pub fn parse(word: &str) -> Option<Self> {
        Some(match word {
            "draft" => Tail::Draft,
            "pack" => Tail::Pack,
            "open" => Tail::Open,
            "return" => Tail::Return,
            "review" => Tail::Review,
            "retired" => Tail::Retired,
            _ => return None,
        })
    }

    pub(crate) fn is_page_or_face(self) -> bool {
        matches!(self, Tail::Draft | Tail::Retired)
    }

    pub(crate) fn is_counter(self) -> bool {
        matches!(
            self,
            Tail::Draft | Tail::Pack | Tail::Open | Tail::Return | Tail::Review
        )
    }
}

impl fmt::Display for Tail {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Address {
    Desk {
        desk: u8,
        title: Option<String>,
    },
    Shelf {
        desk: u8,
        shelf: u8,
        title: Option<String>,
    },
    Book {
        id: BookId,
        title: Option<String>,
    },
    Page(PageAddr),
}

/// A page address. A title is a label. The face, when present, is the anchor under the page.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PageAddr {
    pub id: BookId,
    pub page: u16,
    pub title: Option<String>,
    pub face: Option<u8>,
    pub counter: Option<u8>,
    pub tail: Option<Tail>,
    pub card: Option<String>,
    pub brand: Option<u16>,
}

impl PageAddr {
    /// Identity of a face or counter. Title, tail, card, and brand are not part of it.
    pub fn storage_key(&self) -> Option<String> {
        let face = self.face?;
        let mut key = format!("{}.{:04}.{:02}", self.id.canonical(), self.page, face);
        if let Some(counter) = self.counter {
            key.push_str(&format!(".{counter:02}"));
        }
        Some(key)
    }

    pub fn canonical(&self) -> String {
        let mut out = format!("{}.{:04}", self.id.canonical(), self.page);
        if let Some(face) = self.face {
            out.push_str(&format!(".{face:02}"));
            if let Some(counter) = self.counter {
                out.push_str(&format!(".{counter:02}"));
            }
            if let Some(tail) = self.tail {
                out.push('.');
                out.push_str(tail.as_str());
            }
            if let Some(card) = &self.card {
                out.push('.');
                out.push_str(card);
                if let Some(brand) = self.brand {
                    out.push_str(&format!(".{brand:03}"));
                }
            }
        } else if let Some(title) = &self.title {
            out.push('.');
            out.push_str(title);
            if let Some(tail) = self.tail {
                out.push('.');
                out.push_str(tail.as_str());
            }
        } else if let Some(tail) = self.tail {
            out.push('.');
            out.push_str(tail.as_str());
        }
        out
    }
}

impl Address {
    pub fn canonical(&self) -> String {
        match self {
            Address::Desk { desk, title } => with_title(format!("{desk:02}"), title),
            Address::Shelf {
                desk,
                shelf,
                title,
            } => with_title(format!("{desk:02}.{shelf:02}"), title),
            Address::Book { id, title } => with_title(id.canonical(), title),
            Address::Page(page) => page.canonical(),
        }
    }
}

fn with_title(mut base: String, title: &Option<String>) -> String {
    if let Some(title) = title {
        base.push('.');
        base.push_str(title);
    }
    base
}

#[derive(Debug)]
pub enum Error {
    Empty,
    BadWidth {
        segment: String,
        what: &'static str,
    },
    BadShape {
        detail: String,
    },
    NeedsBook,
    NoActivePage,
    AmbiguousActive {
        count: usize,
    },
    NotAFace,
    CardOnWrite,
    TailOnWrite,
    CountedFaceNeedsCounter {
        face: u8,
    },
    OutsideBook {
        addr: String,
        book: String,
    },
    Exists {
        key: String,
    },
    Missing {
        key: String,
    },
    TailFrom {
        current: String,
        from: String,
    },
    TailStep {
        current: String,
        to: String,
    },
    BadTailOnCreate {
        tail: String,
    },
    Corrupt {
        line: usize,
        detail: String,
    },
    BadHeader(String),
    Io(String),
    FileExists,
    TornFile,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Empty => write!(f, "address is empty"),
            Error::BadWidth { segment, what } => write!(
                f,
                "segment '{segment}' is not a {what}; a short group is rejected, not padded"
            ),
            Error::BadShape { detail } => write!(f, "{detail}"),
            Error::NeedsBook => write!(f, "short address needs an active book"),
            Error::NoActivePage => write!(f, "leading dot needs one active page"),
            Error::AmbiguousActive { count } => write!(
                f,
                "leading dot is refused: {count} pages are active"
            ),
            Error::NotAFace => write!(f, "a write names a face or a counter"),
            Error::CardOnWrite => {
                write!(f, "a write address names the face or the counter; the card stays in the body")
            }
            Error::TailOnWrite => write!(f, "the tail is a field on the write, not part of the address"),
            Error::CountedFaceNeedsCounter { face } => write!(
                f,
                "face {face:02} is always counted, so the write names a counter"
            ),
            Error::OutsideBook { addr, book } => {
                write!(f, "address {addr} is outside book {book}")
            }
            Error::Exists { key } => write!(f, "put creates; {key} already exists"),
            Error::Missing { key } => write!(f, "no face at {key}"),
            Error::TailFrom { current, from } => write!(
                f,
                "tail moves only from the current tail {current}, not from {from}"
            ),
            Error::TailStep { current, to } => {
                write!(f, "tail on {current} does not move to {to}")
            }
            Error::BadTailOnCreate { tail } => {
                write!(f, "tail {tail} is not a legal tail for this create")
            }
            Error::Corrupt { line, detail } => write!(f, "line {line} is not a book entry: {detail}"),
            Error::BadHeader(detail) => write!(f, "book header: {detail}"),
            Error::Io(detail) => write!(f, "{detail}"),
            Error::FileExists => write!(f, "book file already exists"),
            Error::TornFile => write!(f, "the book ends in a torn line and was not opened for append"),
        }
    }
}

impl std::error::Error for Error {}

/// Parse `input`. Missing ancestors come from `ctx`. A leading dot uses the one active page.
pub fn resolve(input: &str, ctx: &Context) -> Result<Address, Error> {
    if input.is_empty() {
        return Err(Error::Empty);
    }
    if input.chars().any(char::is_whitespace) {
        return Err(Error::BadShape {
            detail: "an address has no spaces".into(),
        });
    }
    if let Some(rest) = input.strip_prefix('.') {
        return resolve_active(rest, ctx);
    }
    if input.ends_with('.') || input.contains("..") {
        return Err(Error::BadShape {
            detail: "an address does not have an empty group".into(),
        });
    }
    let segs: Vec<&str> = input.split('.').collect();
    let pages: Vec<usize> = segs
        .iter()
        .enumerate()
        .filter(|(_, seg)| is_fixed_digits(seg, 4))
        .map(|(i, _)| i)
        .collect();
    if pages.len() > 1 {
        return Err(Error::BadShape {
            detail: "an address has one page".into(),
        });
    }
    if pages.is_empty() {
        return resolve_container(&segs);
    }
    resolve_page(&segs, pages[0], ctx)
}

fn resolve_active(rest: &str, ctx: &Context) -> Result<Address, Error> {
    if rest.is_empty() || rest.ends_with('.') || rest.contains("..") {
        return Err(Error::BadShape {
            detail: "a leading dot names a face".into(),
        });
    }
    let segs: Vec<&str> = rest.split('.').collect();
    let face = parse_face(&segs)?;
    let id = ctx.book.ok_or(Error::NeedsBook)?;
    let page = match ctx.active_pages.as_slice() {
        [one] => *one,
        [] => return Err(Error::NoActivePage),
        many => {
            return Err(Error::AmbiguousActive {
                count: many.len(),
            })
        }
    };
    if page > 9999 {
        return Err(Error::BadWidth {
            segment: page.to_string(),
            what: "page",
        });
    }
    Ok(Address::Page(PageAddr {
        id,
        page,
        title: None,
        face: Some(face.face),
        counter: face.counter,
        tail: face.tail,
        card: face.card,
        brand: face.brand,
    }))
}

fn resolve_container(segs: &[&str]) -> Result<Address, Error> {
    let (nums, title) = split_title(segs)?;
    if nums.is_empty() || nums.len() > 3 {
        return Err(Error::BadShape {
            detail: "a container is a desk, a shelf, or a book".into(),
        });
    }
    let mut axes = Vec::with_capacity(nums.len());
    for seg in nums {
        axes.push(parse_fixed(seg, 2, "desk, shelf, or book")? as u8);
    }
    Ok(match axes.as_slice() {
        [desk] => Address::Desk {
            desk: *desk,
            title,
        },
        [desk, shelf] => Address::Shelf {
            desk: *desk,
            shelf: *shelf,
            title,
        },
        [desk, shelf, book] => Address::Book {
            id: BookId {
                desk: *desk,
                shelf: *shelf,
                book: *book,
            },
            title,
        },
        _ => {
            return Err(Error::BadShape {
                detail: "a container is a desk, a shelf, or a book".into(),
            })
        }
    })
}

fn resolve_page(segs: &[&str], page_at: usize, ctx: &Context) -> Result<Address, Error> {
    let mut ancestors = Vec::with_capacity(page_at);
    for seg in &segs[..page_at] {
        ancestors.push(parse_fixed(seg, 2, "desk, shelf, or book")? as u8);
    }
    let page = parse_fixed(segs[page_at], 4, "page")? as u16;
    let id = fill_book(&ancestors, ctx)?;
    let end = parse_page_end(&segs[page_at + 1..])?;
    Ok(Address::Page(PageAddr {
        id,
        page,
        title: end.title,
        face: end.face,
        counter: end.counter,
        tail: end.tail,
        card: end.card,
        brand: end.brand,
    }))
}

fn fill_book(ancestors: &[u8], ctx: &Context) -> Result<BookId, Error> {
    let active = ctx.book;
    Ok(match ancestors {
        [] => active.ok_or(Error::NeedsBook)?,
        [book] => {
            let active = active.ok_or(Error::NeedsBook)?;
            BookId {
                desk: active.desk,
                shelf: active.shelf,
                book: *book,
            }
        }
        [shelf, book] => {
            let active = active.ok_or(Error::NeedsBook)?;
            BookId {
                desk: active.desk,
                shelf: *shelf,
                book: *book,
            }
        }
        [desk, shelf, book] => BookId {
            desk: *desk,
            shelf: *shelf,
            book: *book,
        },
        _ => {
            return Err(Error::BadShape {
                detail: "too many ancestors in front of the page".into(),
            })
        }
    })
}

struct PageEnd {
    title: Option<String>,
    face: Option<u8>,
    counter: Option<u8>,
    tail: Option<Tail>,
    card: Option<String>,
    brand: Option<u16>,
}

fn parse_page_end(segs: &[&str]) -> Result<PageEnd, Error> {
    if segs.is_empty() {
        return Ok(PageEnd {
            title: None,
            face: None,
            counter: None,
            tail: None,
            card: None,
            brand: None,
        });
    }
    if Tail::parse(segs[0]).is_some() {
        let tail = page_tail(segs[0])?;
        if segs.len() != 1 {
            return Err(Error::BadShape {
                detail: "a page tail ends the address".into(),
            });
        }
        return Ok(PageEnd {
            title: None,
            face: None,
            counter: None,
            tail: Some(tail),
            card: None,
            brand: None,
        });
    }
    if is_label(segs[0]) {
        let title = Some(segs[0].to_string());
        let tail = if segs.len() == 1 {
            None
        } else if segs.len() == 2 {
            Some(page_tail(segs[1])?)
        } else {
            return Err(Error::BadShape {
                detail: "a title is not followed by a face; the face address omits the title".into(),
            });
        };
        return Ok(PageEnd {
            title,
            face: None,
            counter: None,
            tail,
            card: None,
            brand: None,
        });
    }
    let face = parse_face(segs)?;
    Ok(PageEnd {
        title: None,
        face: Some(face.face),
        counter: face.counter,
        tail: face.tail,
        card: face.card,
        brand: face.brand,
    })
}

struct FacePart {
    face: u8,
    counter: Option<u8>,
    tail: Option<Tail>,
    card: Option<String>,
    brand: Option<u16>,
}

fn parse_face(segs: &[&str]) -> Result<FacePart, Error> {
    if segs.is_empty() {
        return Err(Error::BadShape {
            detail: "a face is required".into(),
        });
    }
    let face = parse_fixed(segs[0], 2, "face")? as u8;
    let mut index = 1;
    let mut counter = None;
    if index < segs.len() && is_fixed_digits(segs[index], 2) {
        counter = Some(parse_fixed(segs[index], 2, "counter")? as u8);
        index += 1;
    }
    let mut tail = None;
    if index < segs.len() {
        if let Some(parsed) = Tail::parse(segs[index]) {
            if counter.is_some() {
                if !parsed.is_counter() {
                    return Err(Error::BadShape {
                        detail: format!("tail {} is not used on a counter", parsed.as_str()),
                    });
                }
            } else if !parsed.is_page_or_face() {
                return Err(Error::BadShape {
                    detail: format!(
                        "tail {} belongs on a counter, and this address has none",
                        parsed.as_str()
                    ),
                });
            }
            tail = Some(parsed);
            index += 1;
        }
    }
    let mut card = None;
    if index < segs.len() && is_label(segs[index]) {
        card = Some(segs[index].to_string());
        index += 1;
    }
    let mut brand = None;
    if index < segs.len() && is_fixed_digits(segs[index], 3) {
        if card.is_none() {
            return Err(Error::BadShape {
                detail: "a brand number follows a card".into(),
            });
        }
        let number = parse_fixed(segs[index], 3, "brand")?;
        if !(1..=998).contains(&number) {
            return Err(Error::BadWidth {
                segment: segs[index].to_string(),
                what: "brand 001-998",
            });
        }
        brand = Some(number);
        index += 1;
    }
    if index != segs.len() {
        return Err(Error::BadWidth {
            segment: segs[index].to_string(),
            what: "face, counter, tail, card, or brand",
        });
    }
    Ok(FacePart {
        face,
        counter,
        tail,
        card,
        brand,
    })
}

fn page_tail(word: &str) -> Result<Tail, Error> {
    match Tail::parse(word) {
        Some(tail) if tail.is_page_or_face() => Ok(tail),
        Some(tail) => Err(Error::BadShape {
            detail: format!("tail {} belongs on a counter", tail.as_str()),
        }),
        None => Err(Error::BadShape {
            detail: format!("'{word}' is not a page tail"),
        }),
    }
}

fn split_title<'a>(segs: &'a [&str]) -> Result<(&'a [&'a str], Option<String>), Error> {
    let Some(last) = segs.last() else {
        return Ok((segs, None));
    };
    if is_fixed_digits(last, 2) {
        return Ok((segs, None));
    }
    if is_label(last) {
        return Ok((&segs[..segs.len() - 1], Some((*last).to_string())));
    }
    if last.chars().all(|c| c.is_ascii_digit()) {
        return Err(Error::BadWidth {
            segment: (*last).to_string(),
            what: "desk, shelf, or book",
        });
    }
    Err(Error::BadShape {
        detail: format!("'{last}' is not a title"),
    })
}

fn is_label(seg: &str) -> bool {
    let mut chars = seg.chars();
    let Some(first) = chars.next() else {
        return false;
    };
    if !first.is_ascii_lowercase() {
        return false;
    }
    if Tail::parse(seg).is_some() {
        return false;
    }
    chars.all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-')
}

fn is_fixed_digits(seg: &str, width: usize) -> bool {
    seg.len() == width && seg.bytes().all(|b| b.is_ascii_digit())
}

fn parse_fixed(seg: &str, width: usize, what: &'static str) -> Result<u16, Error> {
    if !is_fixed_digits(seg, width) {
        return Err(Error::BadWidth {
            segment: seg.to_string(),
            what,
        });
    }
    seg.parse::<u16>()
        .map_err(|_| Error::BadWidth {
            segment: seg.to_string(),
            what,
        })
}
