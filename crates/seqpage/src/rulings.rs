//! Director rulings that shape where a write may sit on a page (R8, R9, R10).
//! Checked on every block read and on every entry exported.

use crate::error::PageError;
use crate::model::{slot_of, PageId, SectionKey};

/// R9 / R10 for a section of a page.
pub fn check_section(page: PageId, key: SectionKey, line: usize) -> Option<PageError> {
    if let Some(nn) = key.counter {
        if nn == 0 || nn == 99 {
            return Some(PageError::invalid(line, "R9", format!("counter {:02}.{nn:02}: faces have no sentinels, so there is no FF.00 or FF.99; counters run 01-98", key.face)));
        }
    }
    if page.page == 0 && key.face != 0 {
        return Some(PageError::invalid(line, "R10", format!("page {page} is a book door page: face 00 (the registry) is its only face, so face {:02} cannot be on it", key.face)));
    }
    None
}

/// R8 / R9 / R10 for one write (booked or proposed) at `addr` with `tail` field.
pub fn check_write(page: PageId, addr: &str, tail: Option<&str>, line: usize, what: &str) -> Option<PageError> {
    let (_, key) = slot_of(addr)?;
    if let Some(e) = check_section(page, key, line) {
        return Some(PageError::invalid(e.line, e.rule, format!("{what}: {}", e.detail)));
    }
    if key.counter.is_none() && tail == Some("draft") && !addr.ends_with(".draft") {
        return Some(PageError::invalid(line, "R8", format!("{what}: a draft face is addressed `{addr}.draft` (R8), not by a `tail: draft` field on the seated address")));
    }
    None
}
