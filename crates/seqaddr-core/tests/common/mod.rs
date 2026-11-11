#![allow(dead_code)]
use seqaddr_core::log::{Entry, Op};
use seqaddr_core::{BookId, BookState, Policy, SeqError};

pub const AT: &str = "2026-11-11T19:30:00Z";
pub const B: &str = "10.11.21";

/// Applies entries to a book state with automatic numbering.
pub struct Bk {
    pub st: BookState,
    pub pol: Policy,
    pub log: Vec<Entry>,
}

impl Bk {
    pub fn new(book: &str) -> Bk {
        Bk { st: BookState::new(BookId::parse(book).unwrap()), pol: Policy::default(), log: vec![] }
    }
    /// A book with its identity page already written.
    pub fn with_identity(book: &str) -> Bk {
        let mut b = Bk::new(book);
        b.put(&format!("{book}.0000.00"), None, "---\ntitle: tools\n---").unwrap();
        b
    }
    pub fn e(&self, by: &str, op: Op, addr: &str) -> Entry {
        Entry::new(self.st.last_n + 1, AT, by, op, addr)
    }
    pub fn apply(&mut self, e: Entry) -> Result<(), SeqError> {
        self.st.apply(&e, &self.pol)?;
        self.log.push(e);
        Ok(())
    }
    pub fn put(&mut self, addr: &str, tail: Option<&str>, body: &str) -> Result<(), SeqError> {
        let mut e = self.e("user", Op::Put, addr);
        e.tail = tail.map(|s| s.to_string());
        e.body = Some(body.to_string());
        self.apply(e)
    }
    pub fn tail(&mut self, by: &str, addr: &str, from: Option<&str>, to: Option<&str>) -> Result<(), SeqError> {
        let mut e = self.e(by, Op::Tail, addr);
        e.from = from.map(|s| s.to_string());
        e.to = to.map(|s| s.to_string());
        self.apply(e)
    }
    pub fn close(&mut self, by: &str, addr: &str, outcome: Option<&str>) -> Result<(), SeqError> {
        let mut e = self.e(by, Op::Tail, addr);
        e.from = Some("review".into());
        e.outcome = outcome.map(|s| s.to_string());
        self.apply(e)
    }
    pub fn op(&mut self, by: &str, op: Op, addr: &str, body: Option<&str>, cites: Option<u64>) -> Result<(), SeqError> {
        let mut e = self.e(by, op, addr);
        e.body = body.map(|s| s.to_string());
        e.cites = cites;
        self.apply(e)
    }
    pub fn text(&self) -> String {
        let mut log = seqaddr_core::BookLog::new(self.st.book);
        log.entries = self.log.clone();
        log.to_text()
    }
}
