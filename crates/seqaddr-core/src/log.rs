//! The book file: JSON Lines, an append-only log of approved writes (format 3).
//!
//! Line 1 is the header `{"seqbook":1,"address":"DD.SS.BB"}`. Every later line
//! is one approved write. A partly written last line is detected and dropped.

use crate::addr::BookId;
use crate::error::{Result, SeqError};
use serde::{Deserialize, Serialize};

pub const FORMAT_VERSION: u32 = 1;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Header {
    pub seqbook: u32,
    pub address: String,
}

impl Header {
    pub fn new(book: BookId) -> Self {
        Header { seqbook: FORMAT_VERSION, address: book.to_string() }
    }
}

/// Operations (format 3.3). `put`, `tail`, `snapshot` are decided; the rest
/// are proposed and only applied when `Policy::allow_proposed_ops` is on.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Op {
    Put,
    Tail,
    Snapshot,
    /// proposed (D0)
    Copy,
    /// proposed (D0)
    Note,
    /// proposed (D0)
    Merge,
    /// proposed (D0)
    Promote,
    /// proposed (C8.7): compute-only word resolution record
    Use,
}

impl Op {
    pub fn is_proposed(self) -> bool {
        !matches!(self, Op::Put | Op::Tail | Op::Snapshot)
    }
    pub fn as_str(self) -> &'static str {
        match self {
            Op::Put => "put",
            Op::Tail => "tail",
            Op::Snapshot => "snapshot",
            Op::Copy => "copy",
            Op::Note => "note",
            Op::Merge => "merge",
            Op::Promote => "promote",
            Op::Use => "use",
        }
    }
}

/// One approved write: one line of the book (format 3.2, lane contract).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Entry {
    pub n: u64,
    pub at: String,
    pub by: String,
    pub op: Op,
    pub addr: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tail: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub from: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub to: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub body: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proposal: Option<String>,
    /// Provisional: the note entry `n` a `merge` cites (D0).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cites: Option<u64>,
    /// Provisional: closing outcome on `review -> closed` (S03).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub outcome: Option<String>,
    /// Provisional: number of entries in this entry's proposal, written on every
    /// entry of a multi-op proposal so a cut-off proposal can be dropped whole.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub of: Option<u32>,
    /// Provisional: the full state carried by a `snapshot` entry.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub state: Option<serde_json::Value>,
    /// Unknown fields are kept so a newer writer's lines round-trip.
    #[serde(flatten)]
    pub extra: serde_json::Map<String, serde_json::Value>,
}

impl Entry {
    pub fn new(n: u64, at: impl Into<String>, by: impl Into<String>, op: Op, addr: impl Into<String>) -> Entry {
        Entry {
            n,
            at: at.into(),
            by: by.into(),
            op,
            addr: addr.into(),
            tail: None,
            from: None,
            to: None,
            body: None,
            proposal: None,
            cites: None,
            outcome: None,
            of: None,
            state: None,
            extra: Default::default(),
        }
    }
    pub fn to_line(&self) -> String {
        serde_json::to_string(self).expect("entry serializes")
    }
}

/// A book file read into memory.
#[derive(Debug, Clone, PartialEq)]
pub struct BookLog {
    pub header: Header,
    pub entries: Vec<Entry>,
    /// True if a partly written last line (or a cut-off proposal) was found and dropped (format 3.1).
    pub dropped_partial: bool,
    /// Byte length of the valid prefix of the text that was parsed.
    pub valid_len: usize,
}

/// Director ruling R4: stored text is plain ASCII, printable 0x20-0x7E plus newline.
pub fn is_plain_char(c: char) -> bool {
    c == '\n' || (' '..='~').contains(&c)
}

/// Check one stored string under R4. `what` names the field for the error.
pub fn check_plain(what: &str, s: &str) -> Result<()> {
    match s.char_indices().find(|(_, c)| !is_plain_char(*c)) {
        None => Ok(()),
        Some((i, c)) => Err(SeqError::rejected(
            "R4",
            format!("{what} holds {} at character {i}; storage is plain ASCII only (printable characters and newline; no accents, emoji, tabs or CR)", describe_char(c)),
        )),
    }
}

fn describe_char(c: char) -> String {
    match c {
        '\t' => "a tab".into(),
        '\r' => "a carriage return (CR)".into(),
        _ if c.is_control() => format!("control character U+{:04X}", c as u32),
        _ => format!("`{c}` (U+{:04X})", c as u32),
    }
}

/// First byte that breaks R4 in raw file bytes: (line, byte).
pub fn first_non_plain_byte(bytes: &[u8]) -> Option<(usize, u8)> {
    let mut line = 1;
    for &b in bytes {
        if b == b'\n' {
            line += 1;
        } else if !(0x20..=0x7E).contains(&b) {
            return Some((line, b));
        }
    }
    None
}

impl Entry {
    /// Optional `reason` field: why the entry opens a draft (R5 follow-up).
    pub fn reason(&self) -> Option<&str> {
        self.extra.get("reason").and_then(|v| v.as_str())
    }
    /// R4: every stored string of the entry is plain ASCII.
    pub fn check_plain(&self) -> Result<()> {
        check_plain("by", &self.by)?;
        check_plain("addr", &self.addr)?;
        for (k, v) in [("tail", &self.tail), ("from", &self.from), ("to", &self.to), ("body", &self.body), ("proposal", &self.proposal), ("outcome", &self.outcome)] {
            if let Some(v) = v {
                check_plain(k, v)?;
            }
        }
        let line = self.to_line();
        check_plain("entry line", &line)
    }
}

fn is_leap(y: u32) -> bool {
    (y % 4 == 0 && y % 100 != 0) || y % 400 == 0
}

/// Check an ISO 8601 UTC timestamp `YYYY-MM-DDTHH:MM:SS[.frac]Z`, and that it is a real time.
pub fn check_timestamp(s: &str) -> Result<()> {
    let b = s.as_bytes();
    let ok = b.len() >= 20
        && b[4] == b'-'
        && b[7] == b'-'
        && b[10] == b'T'
        && b[13] == b':'
        && b[16] == b':'
        && *b.last().unwrap() == b'Z'
        && [0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18].iter().all(|&i| b[i].is_ascii_digit())
        && (b.len() == 20 || (b[19] == b'.' && b.len() > 21 && b[20..b.len() - 1].iter().all(|c| c.is_ascii_digit())));
    let real = ok && {
        let n = |a: usize, b: usize| s[a..b].parse::<u32>().unwrap_or(99);
        let (y, mo, d, h, mi, se) = (n(0, 4), n(5, 7), n(8, 10), n(11, 13), n(14, 16), n(17, 19));
        let dim = match mo {
            1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
            4 | 6 | 9 | 11 => 30,
            2 if is_leap(y) => 29,
            2 => 28,
            _ => 0,
        };
        d >= 1 && d <= dim && h < 24 && mi < 60 && se < 60
    };
    if real {
        Ok(())
    } else {
        Err(SeqError::invalid("format 3.2", format!("`{s}` is not an ISO 8601 UTC time (YYYY-MM-DDTHH:MM:SSZ)")))
    }
}

/// Format seconds since the Unix epoch as ISO 8601 UTC.
pub fn format_utc(secs: i64) -> String {
    let days = secs.div_euclid(86_400);
    let rem = secs.rem_euclid(86_400);
    // civil from days (Howard Hinnant)
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z - era * 146_097;
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = if m <= 2 { y + 1 } else { y };
    format!("{:04}-{:02}-{:02}T{:02}:{:02}:{:02}Z", y, m, d, rem / 3600, (rem % 3600) / 60, rem % 60)
}

/// Now, as ISO 8601 UTC (feature `fs`; not available on wasm32-unknown).
#[cfg(feature = "fs")]
pub fn now_utc() -> String {
    let secs = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_secs() as i64).unwrap_or(0);
    format_utc(secs)
}

impl BookLog {
    pub fn new(book: BookId) -> Self {
        BookLog { header: Header::new(book), entries: Vec::new(), dropped_partial: false, valid_len: 0 }
    }

    pub fn book(&self) -> Result<BookId> {
        BookId::parse(&self.header.address)
    }

    /// Parse book text. A last line that is cut off (no newline at the end and
    /// not valid JSON) is dropped (format 3.1). Damage anywhere earlier is an error.
    pub fn parse(text: &str) -> Result<BookLog> {
        if let Some((line, b)) = first_non_plain_byte(text.as_bytes()) {
            return Err(SeqError::Corrupt { line, detail: format!("damaged: byte 0x{b:02X} is not plain ASCII (Director ruling R4)") });
        }
        let ends_clean = text.ends_with('\n');
        let lines: Vec<&str> = text.split('\n').collect();
        // split leaves a trailing "" when the text ends with '\n'
        let mut lines: Vec<&str> = if ends_clean { lines[..lines.len() - 1].to_vec() } else { lines };
        let mut dropped_partial = false;
        if !ends_clean {
            if let Some(last) = lines.last().copied() {
                let parses = serde_json::from_str::<serde_json::Value>(last).is_ok();
                if !parses || last.is_empty() {
                    lines.pop();
                    dropped_partial = !last.is_empty();
                }
            }
        }
        let first = lines.first().ok_or(SeqError::Corrupt { line: 1, detail: "no header line".into() })?;
        let header: Header = serde_json::from_str(first).map_err(|e| SeqError::Corrupt { line: 1, detail: format!("bad header: {e}") })?;
        if header.seqbook != FORMAT_VERSION {
            return Err(SeqError::Corrupt { line: 1, detail: format!("unknown seqbook version {}", header.seqbook) });
        }
        BookId::parse(&header.address).map_err(|e| SeqError::Corrupt { line: 1, detail: e.to_string() })?;
        let mut entries = Vec::with_capacity(lines.len());
        for (i, line) in lines.iter().enumerate().skip(1) {
            if line.trim().is_empty() {
                return Err(SeqError::Corrupt { line: i + 1, detail: "blank line inside the log".into() });
            }
            let e: Entry = serde_json::from_str(line).map_err(|err| SeqError::Corrupt { line: i + 1, detail: err.to_string() })?;
            let expect = entries.len() as u64 + 1;
            if e.n != expect {
                return Err(SeqError::Corrupt { line: i + 1, detail: format!("entry n={} out of order; expected {expect}", e.n) });
            }
            check_timestamp(&e.at).map_err(|err| SeqError::Corrupt { line: i + 1, detail: err.to_string() })?;
            // R4 also covers JSON escapes (`\u00e9`, `\t`) that decode to a non-plain character.
            e.check_plain().map_err(|err| SeqError::Corrupt { line: i + 1, detail: format!("damaged: {} (Director ruling R4)", err.detail()) })?;
            entries.push(e);
        }
        // A proposal is all or nothing (format 3.3): drop a trailing group that is cut short.
        if let Some(last) = entries.last() {
            if let (Some(pid), Some(of)) = (last.proposal.clone(), last.of) {
                let have = entries.iter().rev().take_while(|e| e.proposal.as_deref() == Some(pid.as_str())).count();
                if have < of as usize {
                    entries.truncate(entries.len() - have);
                    dropped_partial = true;
                }
            }
        }
        let kept_lines = 1 + entries.len();
        let mut valid_len: usize = lines.iter().take(kept_lines).map(|l| l.len() + 1).sum();
        if valid_len > text.len() {
            valid_len = text.len(); // last kept line had no newline
        }
        Ok(BookLog { header, entries, dropped_partial, valid_len })
    }

    /// Serialize the whole log (header + entries), one per line, newline ended.
    pub fn to_text(&self) -> String {
        let mut s = serde_json::to_string(&self.header).unwrap();
        s.push('\n');
        for e in &self.entries {
            s.push_str(&e.to_line());
            s.push('\n');
        }
        s
    }

    pub fn next_n(&self) -> u64 {
        self.entries.len() as u64 + 1
    }

    /// Index of the latest snapshot entry, if any (format 3.4).
    pub fn latest_snapshot(&self) -> Option<usize> {
        self.entries.iter().rposition(|e| e.op == Op::Snapshot)
    }

    /// Entries touching an address (format 3.1 history): the address itself and
    /// anything below it (a page's faces, a face's counters). Tails, titles and
    /// card keys are ignored when matching.
    pub fn history(&self, addr: &str) -> Result<Vec<&Entry>> {
        let want = crate::addr::Address::parse(addr)?;
        let want_key = history_key(&want);
        Ok(self
            .entries
            .iter()
            .filter(|e| e.op != Op::Snapshot)
            .filter(|e| match crate::addr::Address::parse(&e.addr) {
                Ok(a) => {
                    let k = history_key(&a);
                    k == want_key || k.starts_with(&format!("{want_key}."))
                }
                Err(_) => false,
            })
            .collect())
    }
}

fn history_key(a: &crate::addr::Address) -> String {
    match a {
        crate::addr::Address::Page(p) => p.slot().to_string(),
        crate::addr::Address::Container(c) => {
            let mut c = c.clone();
            c.title = None;
            c.to_string()
        }
        other => other.to_string(),
    }
}

#[cfg(feature = "fs")]
pub mod file {
    //! Crash-safe file access. Only the compute should call the writers (format 1.2).
    use super::*;
    use std::fs::{self, OpenOptions};
    use std::io::Write;
    use std::path::Path;

    fn io(e: std::io::Error) -> SeqError {
        SeqError::Io { detail: e.to_string() }
    }

    /// Read a book. A byte outside plain ASCII (R4) reports the book as damaged.
    pub fn read(path: &Path) -> Result<BookLog> {
        let bytes = fs::read(path).map_err(io)?;
        if let Some((line, b)) = first_non_plain_byte(&bytes) {
            return Err(SeqError::Corrupt { line, detail: format!("{}: damaged: byte 0x{b:02X} is not plain ASCII (Director ruling R4)", path.display()) });
        }
        BookLog::parse(std::str::from_utf8(&bytes).expect("ASCII is UTF-8"))
    }

    /// Create a new book file with only its header. Fails if it exists.
    pub fn create(path: &Path, book: BookId) -> Result<()> {
        let mut f = OpenOptions::new().write(true).create_new(true).open(path).map_err(io)?;
        let mut line = serde_json::to_string(&Header::new(book)).unwrap();
        line.push('\n');
        f.write_all(line.as_bytes()).map_err(io)?;
        f.sync_all().map_err(io)
    }

    /// Write the header into an empty file (after `repair_tail` emptied a cut header).
    pub fn write_header(path: &Path, book: BookId) -> Result<()> {
        let mut f = OpenOptions::new().write(true).open(path).map_err(io)?;
        if f.metadata().map_err(io)?.len() != 0 {
            return Err(SeqError::rejected("format 3.2", "the file already has content; the header is line 1"));
        }
        let mut line = serde_json::to_string(&Header::new(book)).unwrap();
        line.push('\n');
        f.write_all(line.as_bytes()).map_err(io)?;
        f.sync_all().map_err(io)
    }

    /// Cut a partly written last line off the file, so the next append starts
    /// on a clean line (format 3.1). Returns true if anything was cut.
    ///
    /// A file cut inside its header (a crash during `create`) holds no complete
    /// line; it is emptied, and the caller writes the header again (`write_header`).
    pub fn repair_tail(path: &Path) -> Result<bool> {
        let bytes = fs::read(path).map_err(io)?;
        if let Some((line, b)) = first_non_plain_byte(&bytes) {
            return Err(SeqError::Corrupt { line, detail: format!("damaged: byte 0x{b:02X} is not plain ASCII (Director ruling R4); not repaired") });
        }
        let text = String::from_utf8(bytes).expect("ASCII");
        if !text.is_empty() && !text.contains('\n') && serde_json::from_str::<Header>(&text).is_err() {
            let f = OpenOptions::new().write(true).open(path).map_err(io)?;
            f.set_len(0).map_err(io)?;
            f.sync_all().map_err(io)?;
            return Ok(true);
        }
        let log = BookLog::parse(&text)?;
        if log.valid_len >= text.len() {
            return Ok(false);
        }
        let f = OpenOptions::new().write(true).open(path).map_err(io)?;
        f.set_len(log.valid_len as u64).map_err(io)?;
        f.sync_all().map_err(io)?;
        Ok(true)
    }

    /// Append entries (one proposal) as whole lines, then fsync. Repairs a
    /// partial last line first. Each entry is written as one `write` of a
    /// complete line so a crash leaves at most one partial line at the end.
    /// Entries breaking R4 are refused before anything is written.
    pub fn append(path: &Path, entries: &[Entry]) -> Result<()> {
        for e in entries {
            e.check_plain()?;
        }
        repair_tail(path)?;
        let mut buf = String::new();
        let existing = fs::read(path).map_err(io)?;
        if !existing.is_empty() && !existing.ends_with(b"\n") {
            buf.push('\n');
        }
        for e in entries {
            buf.push_str(&e.to_line());
            buf.push('\n');
        }
        let mut f = OpenOptions::new().append(true).open(path).map_err(io)?;
        f.write_all(buf.as_bytes()).map_err(io)?;
        f.sync_all().map_err(io)
    }
}
