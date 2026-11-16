//! Append-only book file. Replay rebuilds the faces. Only [`Writer`] appends.

use std::collections::BTreeMap;
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

use crate::addr::{resolve, Address, BookId, Context, Error, Tail};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FaceView {
    pub body: String,
    pub tail: Option<Tail>,
}

/// One stored face or counter, in address order.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FaceAt {
    pub key: String,
    pub body: String,
    pub tail: Option<Tail>,
}

#[derive(Clone, Debug)]
struct Face {
    body: String,
    tail: Option<Tail>,
    counter: bool,
}

/// A book rebuilt from its log.
#[derive(Clone, Debug)]
pub struct Book {
    id: BookId,
    faces: BTreeMap<String, Face>,
    len: usize,
    dropped_last_line: bool,
}

impl Book {
    pub fn load(path: &Path) -> Result<Self, Error> {
        let text = fs::read_to_string(path).map_err(|err| Error::Io(err.to_string()))?;
        Self::replay(&text)
    }

    pub fn address(&self) -> BookId {
        self.id
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn dropped_last_line(&self) -> bool {
        self.dropped_last_line
    }

    /// The approved writes, in book order. A torn last line is dropped. A bad middle line is corrupt.
    pub fn writes(path: &Path) -> Result<Vec<LogWrite>, Error> {
        read_writes(path)
    }

    /// Resolve `addr` in this book and return the face, if a put created it.
    pub fn faces(&self) -> Vec<FaceAt> {
        self.faces
            .iter()
            .map(|(key, face)| FaceAt {
                key: key.clone(),
                body: face.body.clone(),
                tail: face.tail,
            })
            .collect()
    }

    pub fn face(&self, addr: &str) -> Result<Option<FaceView>, Error> {
        let key = write_target(self.id, addr)?.0;
        Ok(self.faces.get(&key).map(|face| FaceView {
            body: face.body.clone(),
            tail: face.tail,
        }))
    }

    fn replay(text: &str) -> Result<Self, Error> {
        let lines = split_log(text);
        if lines.is_empty() {
            return Err(Error::BadHeader("the file has no header".into()));
        }
        let header: Header = serde_json::from_str(lines[0]).map_err(|err| {
            Error::BadHeader(err.to_string())
        })?;
        if header.seqbook != 1 {
            return Err(Error::BadHeader(format!(
                "seqbook {} is not 1",
                header.seqbook
            )));
        }
        let id = header_book(&header.address)?;
        let mut book = Book {
            id,
            faces: BTreeMap::new(),
            len: 0,
            dropped_last_line: false,
        };
        let mut dropped = false;
        let last = lines.len() - 1;
        for (index, line) in lines.iter().enumerate().skip(1) {
            let line_no = index + 1;
            let entry: Entry = match serde_json::from_str(line) {
                Ok(entry) => entry,
                Err(err) => {
                    if index == last {
                        dropped = true;
                        break;
                    }
                    return Err(Error::Corrupt {
                        line: line_no,
                        detail: err.to_string(),
                    });
                }
            };
            let expected = book.len as u64 + 1;
            if entry.n != expected {
                return Err(Error::Corrupt {
                    line: line_no,
                    detail: format!("n is {}, expected {expected}", entry.n),
                });
            }
            book.apply(&entry)?;
            book.len += 1;
        }
        book.dropped_last_line = dropped;
        Ok(book)
    }

    fn apply(&mut self, entry: &Entry) -> Result<(), Error> {
        match entry.op.as_str() {
            "put" => {
                let (key, counter) = write_target(self.id, &entry.addr)?;
                if self.faces.contains_key(&key) {
                    return Err(Error::Exists { key });
                }
                let body = entry.body.clone().ok_or_else(|| Error::Corrupt {
                    line: entry.n as usize,
                    detail: "put needs a body".into(),
                })?;
                let tail = match &entry.tail {
                    None => None,
                    Some(word) => Some(tail_on_create(word, counter)?),
                };
                self.faces.insert(
                    key,
                    Face {
                        body,
                        tail,
                        counter,
                    },
                );
                Ok(())
            }
            "tail" => {
                let (key, counter) = write_target(self.id, &entry.addr)?;
                let face = self.faces.get_mut(&key).ok_or_else(|| Error::Missing {
                    key: key.clone(),
                })?;
                let from = entry.from.clone().unwrap_or_default();
                let to = entry.to.clone().unwrap_or_default();
                face.tail = move_tail(face.tail, face.counter || counter, &from, &to)?;
                Ok(())
            }
            other => Err(Error::Corrupt {
                line: entry.n as usize,
                detail: format!("op '{other}' is not put or tail"),
            }),
        }
    }
}

/// The only append path. A put creates. A tail moves from the current tail.
pub struct Writer {
    path: PathBuf,
    book: Book,
}

impl Writer {
    pub fn create(path: &Path, address: &str) -> Result<Self, Error> {
        if path.exists() {
            return Err(Error::FileExists);
        }
        if let Some(parent) = path.parent() {
            if !parent.as_os_str().is_empty() {
                fs::create_dir_all(parent).map_err(|err| Error::Io(err.to_string()))?;
            }
        }
        let id = header_book(address)?;
        let header = Header {
            seqbook: 1,
            address: id.canonical(),
            title: None,
            state: None,
        };
        let line = serde_json::to_string(&header).map_err(|err| Error::Io(err.to_string()))?;
        let mut file = File::create(path).map_err(|err| Error::Io(err.to_string()))?;
        file.write_all(line.as_bytes())
            .and_then(|_| file.write_all(b"\n"))
            .and_then(|_| file.flush())
            .map_err(|err| Error::Io(err.to_string()))?;
        Ok(Writer {
            path: path.to_path_buf(),
            book: Book {
                id,
                faces: BTreeMap::new(),
                len: 0,
                dropped_last_line: false,
            },
        })
    }

    /// Append to a book that already replays. A torn last line is left for a person.
    pub fn open(path: &Path) -> Result<Self, Error> {
        let book = Book::load(path)?;
        if book.dropped_last_line {
            return Err(Error::TornFile);
        }
        Ok(Writer {
            path: path.to_path_buf(),
            book,
        })
    }

    pub fn book(&self) -> &Book {
        &self.book
    }

    pub fn put(
        &mut self,
        at: &str,
        by: &str,
        addr: &str,
        body: &str,
        tail: Option<Tail>,
    ) -> Result<(), Error> {
        let (key, counter) = write_target(self.book.id, addr)?;
        if self.book.faces.contains_key(&key) {
            return Err(Error::Exists { key });
        }
        if let Some(tail) = tail {
            tail_on_create(tail.as_str(), counter)?;
        }
        self.append(OutEntry {
            n: self.book.len as u64 + 1,
            at: at.to_string(),
            by: by.to_string(),
            op: "put",
            addr: addr.to_string(),
            body: Some(body.to_string()),
            tail: tail.map(|tail| tail.as_str().to_string()),
            from: None,
            to: None,
        })
    }

    pub fn tail(
        &mut self,
        at: &str,
        by: &str,
        addr: &str,
        from: &str,
        to: &str,
    ) -> Result<(), Error> {
        let (key, counter) = write_target(self.book.id, addr)?;
        let face = self.book.faces.get(&key).ok_or_else(|| Error::Missing {
            key: key.clone(),
        })?;
        move_tail(face.tail, face.counter || counter, from, to)?;
        self.append(OutEntry {
            n: self.book.len as u64 + 1,
            at: at.to_string(),
            by: by.to_string(),
            op: "tail",
            addr: addr.to_string(),
            body: None,
            tail: None,
            from: Some(from.to_string()),
            to: Some(to.to_string()),
        })
    }

    fn append(&mut self, entry: OutEntry) -> Result<(), Error> {
        let line = serde_json::to_string(&entry).map_err(|err| Error::Io(err.to_string()))?;
        let mut file = OpenOptions::new()
            .append(true)
            .open(&self.path)
            .map_err(|err| Error::Io(err.to_string()))?;
        file.write_all(line.as_bytes())
            .and_then(|_| file.write_all(b"\n"))
            .and_then(|_| file.flush())
            .map_err(|err| Error::Io(err.to_string()))?;
        let stored = Entry {
            n: entry.n,
            at: entry.at,
            by: entry.by,
            op: entry.op.to_string(),
            addr: entry.addr,
            body: entry.body,
            tail: entry.tail,
            from: entry.from,
            to: entry.to,
        };
        self.book.apply(&stored)?;
        self.book.len += 1;
        Ok(())
    }
}

fn header_book(address: &str) -> Result<BookId, Error> {
    match resolve(address, &Context::empty())? {
        Address::Book { id, title: None } => Ok(id),
        Address::Book { title: Some(_), .. } => Err(Error::BadHeader(
            "the header address is the book, without a title".into(),
        )),
        other => Err(Error::BadHeader(format!(
            "{} is not a book address",
            other.canonical()
        ))),
    }
}

fn write_target(book: BookId, addr: &str) -> Result<(String, bool), Error> {
    let ctx = Context::new(Some(book), Vec::new());
    let page = match resolve(addr, &ctx)? {
        Address::Page(page) => page,
        other => {
            return Err(Error::BadShape {
                detail: format!("{} is not a face", other.canonical()),
            })
        }
    };
    if page.id != book {
        return Err(Error::OutsideBook {
            addr: page.canonical(),
            book: book.canonical(),
        });
    }
    if page.card.is_some() || page.brand.is_some() {
        return Err(Error::CardOnWrite);
    }
    if page.tail.is_some() {
        return Err(Error::TailOnWrite);
    }
    let Some(face) = page.face else {
        return Err(Error::NotAFace);
    };
    if matches!(face, 5 | 6) && page.counter.is_none() {
        return Err(Error::CountedFaceNeedsCounter { face });
    }
    let key = page.storage_key().ok_or(Error::NotAFace)?;
    Ok((key, page.counter.is_some()))
}

fn tail_on_create(word: &str, counter: bool) -> Result<Tail, Error> {
    let Some(tail) = Tail::parse(word) else {
        return Err(Error::BadTailOnCreate {
            tail: word.to_string(),
        });
    };
    let legal = if counter {
        tail.is_counter()
    } else {
        tail.is_page_or_face()
    };
    if !legal {
        return Err(Error::BadTailOnCreate {
            tail: word.to_string(),
        });
    }
    Ok(tail)
}

fn move_tail(
    current: Option<Tail>,
    counter: bool,
    from: &str,
    to: &str,
) -> Result<Option<Tail>, Error> {
    let current_word = current_name(current, counter);
    if from != current_word {
        return Err(Error::TailFrom {
            current: current_word,
            from: from.to_string(),
        });
    }
    let next = match if counter {
        next_counter(current)
    } else {
        next_face(current)
    } {
        Next::Illegal => {
            return Err(Error::TailStep {
                current: current_word,
                to: to.to_string(),
            })
        }
        Next::Stay(tail) => tail,
    };
    let next_word = match next {
        Some(tail) => tail.as_str(),
        None if counter => "closed",
        None => "seated",
    };
    if to != next_word {
        return Err(Error::TailStep {
            current: current_word,
            to: to.to_string(),
        });
    }
    Ok(next)
}

enum Next {
    Stay(Option<Tail>),
    Illegal,
}

fn next_counter(current: Option<Tail>) -> Next {
    match current {
        Some(Tail::Draft) => Next::Stay(Some(Tail::Pack)),
        Some(Tail::Pack) => Next::Stay(Some(Tail::Open)),
        Some(Tail::Open) => Next::Stay(Some(Tail::Return)),
        Some(Tail::Return) => Next::Stay(Some(Tail::Review)),
        Some(Tail::Review) => Next::Stay(None),
        _ => Next::Illegal,
    }
}

fn next_face(current: Option<Tail>) -> Next {
    match current {
        None => Next::Stay(Some(Tail::Retired)),
        Some(Tail::Draft) => Next::Stay(Some(Tail::Retired)),
        _ => Next::Illegal,
    }
}

fn current_name(current: Option<Tail>, counter: bool) -> String {
    match current {
        Some(tail) => tail.as_str().to_string(),
        None if counter => "closed".to_string(),
        None => "seated".to_string(),
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct LogWrite {
    pub n: u64,
    pub at: String,
    pub by: String,
    pub op: String,
    pub addr: String,
    pub body: Option<String>,
    pub tail: Option<String>,
    pub from: Option<String>,
    pub to: Option<String>,
}

pub fn read_writes(path: &Path) -> Result<Vec<LogWrite>, Error> {
    let text = fs::read_to_string(path).map_err(|err| Error::Io(err.to_string()))?;
    let lines = split_log(&text);
    if lines.is_empty() {
        return Err(Error::BadHeader("the file has no header".into()));
    }
    let mut writes = Vec::new();
    let last = lines.len() - 1;
    for (index, line) in lines.iter().enumerate().skip(1) {
        let entry: Entry = match serde_json::from_str(line) {
            Ok(entry) => entry,
            Err(err) => {
                if index == last {
                    break;
                }
                return Err(Error::Corrupt {
                    line: index + 1,
                    detail: err.to_string(),
                });
            }
        };
        let expected = writes.len() as u64 + 1;
        if entry.n != expected {
            return Err(Error::Corrupt {
                line: index + 1,
                detail: format!("n is {}, expected {expected}", entry.n),
            });
        }
        writes.push(LogWrite {
            n: entry.n,
            at: entry.at,
            by: entry.by,
            op: entry.op,
            addr: entry.addr,
            body: entry.body,
            tail: entry.tail,
            from: entry.from,
            to: entry.to,
        });
    }
    Ok(writes)
}

fn split_log(text: &str) -> Vec<&str> {
    text.split('\n')
        .map(|line| line.strip_suffix('\r').unwrap_or(line))
        .filter(|line| !line.is_empty())
        .collect()
}

#[derive(Debug, Serialize, Deserialize)]
struct Header {
    seqbook: u32,
    address: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    title: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    state: Option<String>,
}

#[derive(Debug, Deserialize)]
struct Entry {
    n: u64,
    #[allow(dead_code)]
    at: String,
    #[allow(dead_code)]
    by: String,
    op: String,
    addr: String,
    #[serde(default)]
    body: Option<String>,
    #[serde(default)]
    tail: Option<String>,
    #[serde(default)]
    from: Option<String>,
    #[serde(default)]
    to: Option<String>,
}

#[derive(Serialize)]
struct OutEntry {
    n: u64,
    at: String,
    by: String,
    op: &'static str,
    addr: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    body: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    tail: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    to: Option<String>,
}

