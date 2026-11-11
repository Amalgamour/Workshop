#![allow(dead_code)]
use seqaddr_core::log::BookLog;
use std::path::PathBuf;

pub fn repo() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..")
}

pub fn books_in(dir: &str) -> Vec<(String, String, BookLog)> {
    let d = repo().join(dir);
    let mut out = Vec::new();
    let mut paths: Vec<_> = std::fs::read_dir(&d).unwrap().flatten().map(|e| e.path()).filter(|p| p.extension().and_then(|x| x.to_str()) == Some("book")).collect();
    paths.sort();
    for p in paths {
        let text = std::fs::read_to_string(&p).unwrap();
        let log = BookLog::parse(&text).unwrap_or_else(|e| panic!("{}: {e}", p.display()));
        out.push((p.display().to_string(), text, log));
    }
    out
}

pub fn read(rel: &str) -> String {
    std::fs::read_to_string(repo().join(rel)).unwrap_or_else(|e| panic!("{rel}: {e}"))
}

/// Tiny deterministic PRNG (xorshift64*), so fuzz runs are repeatable without extra crates.
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
        (self.next() % n.max(1) as u64) as usize
    }
}
