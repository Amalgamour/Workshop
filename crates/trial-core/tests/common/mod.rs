//! Shared helpers for TRIAL-C. Worlds are built through `validate` (the real
//! write path) so every seeded page passed the core's own checks.
#![allow(dead_code)]
use seqaddr_core::log::{Entry, Op};
use seqaddr_core::validate::{validate, OpRequest, Outcome, Proposal};
use seqaddr_core::{Address, BookId, BookLog, BookState, Policy, World};

pub const AT: &str = "2026-11-11T19:45:00Z";

/// Small deterministic PRNG (xorshift64*), so fuzz runs are repeatable without deps.
pub struct Rng(pub u64);
impl Rng {
    pub fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545F4914F6CDD1D)
    }
    pub fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }
    pub fn pick<'a, T>(&mut self, xs: &'a [T]) -> &'a T {
        &xs[self.below(xs.len())]
    }
}

pub fn op(o: Op, addr: &str) -> OpRequest {
    OpRequest { op: Some(o), addr: addr.into(), ..Default::default() }
}
pub fn put(addr: &str, body: &str) -> OpRequest {
    OpRequest { op: Some(Op::Put), addr: addr.into(), body: Some(body.into()), ..Default::default() }
}
pub fn put_t(addr: &str, tail: &str, body: &str) -> OpRequest {
    OpRequest { op: Some(Op::Put), addr: addr.into(), tail: Some(tail.into()), body: Some(body.into()), ..Default::default() }
}
pub fn mv(addr: &str, from: &str, to: &str) -> OpRequest {
    OpRequest { op: Some(Op::Tail), addr: addr.into(), from: Some(from.into()), to: Some(to.into()), ..Default::default() }
}
pub fn close(addr: &str, outcome: &str) -> OpRequest {
    OpRequest { op: Some(Op::Tail), addr: addr.into(), from: Some("review".into()), to: None, outcome: Some(outcome.into()), ..Default::default() }
}

pub fn propose(w: &World, by: &str, ops: Vec<OpRequest>) -> Outcome {
    validate(w, &Proposal { by: by.into(), ops }, AT)
}

/// R2 (fix pass): seating a face needs an approval record. Seeding is setup, not the
/// thing under test, so seeds carry the Director's approval on every put; promotes are
/// left alone so the review rule stays visible.
pub fn approve(ops: Vec<OpRequest>) -> Vec<OpRequest> {
    ops.into_iter()
        .map(|mut r| {
            if r.op == Some(Op::Put) && r.approved_by.is_none() {
                r.approved_by = Some("director".into());
            }
            r
        })
        .collect()
}

/// Apply a proposal and store the new state; panics with the reasons if rejected.
pub fn seed(w: &mut World, by: &str, ops: Vec<OpRequest>) {
    let out = propose(w, by, approve(ops));
    assert!(out.approved(), "seed rejected: {:?}", out.reasons);
    w.insert(out.state.unwrap());
}
/// Apply if approved; return the outcome either way.
pub fn try_seed(w: &mut World, by: &str, ops: Vec<OpRequest>) -> Outcome {
    let out = propose(w, by, approve(ops));
    if let Some(st) = out.state.clone() {
        w.insert(st);
    }
    out
}

/// A book with its door page. R10 (fix pass): the door page 0000 holds only face 00.
pub fn door(w: &mut World, book: &str) {
    seed(w, "compute", vec![put(&format!("{book}.0000.00"), "---\ntitle: tools\n---")]);
}

/// Kernel 00.00.00, shelf 10.11.00, desk 10.00.00 and book 10.11.21, each with a door.
pub fn world() -> World {
    let mut w = World::new(Policy::default());
    for b in ["00.00.00", "10.00.00", "10.11.00", "10.11.21"] {
        door(&mut w, b);
    }
    w
}

pub fn pa(s: &str) -> seqaddr_core::PageAddr {
    Address::parse_full_page(s).unwrap()
}
pub fn bid(s: &str) -> BookId {
    BookId::parse(s).unwrap()
}

/// Every entry of a world's book as a log, rebuilt by re-running the same proposals.
pub struct LogBuilder {
    pub w: World,
    pub log: BookLog,
}
impl LogBuilder {
    pub fn new(book: &str) -> Self {
        // Log tests are about the file format, not seating (R2): seats need no approval record here.
        LogBuilder { w: World::new(Policy { seat_needs_approval: false, ..Policy::default() }), log: BookLog::new(bid(book)) }
    }
    pub fn add(&mut self, by: &str, ops: Vec<OpRequest>) {
        let out = propose(&self.w, by, ops);
        assert!(out.approved(), "{:?}", out.reasons);
        self.log.entries.extend(out.entries.iter().cloned());
        self.w.insert(out.state.unwrap());
    }
    pub fn add_entry(&mut self, e: Entry) {
        self.log.entries.push(e);
    }
    pub fn state(&self) -> &BookState {
        self.w.get(self.log.book().unwrap()).unwrap()
    }
    pub fn text(&self) -> String {
        self.log.to_text()
    }
}

pub fn entry(n: u64, by: &str, o: Op, addr: &str) -> Entry {
    Entry::new(n, AT, by, o, addr)
}
