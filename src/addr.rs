//! Work-page address rules, copied from seqaddr-core `addr.rs`
//! (`axis_role`, `desk_kind`, `page_kind`, `band_head`).
//! The wf branch cannot depend on that crate. Commit 79f12ed is not in this
//! clone; these four functions match origin/prima/build at 7c1c0bf1.

use crate::log::Res;

/// What a desk number is for (seqAddr 1.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
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
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AxisRole {
    /// `00`: the door.
    Door,
    /// `01-09`: reserved.
    Reserved,
    Normal,
    /// `99`: pointer, look for the next location.
    Pointer,
}

pub fn axis_role(v: u8) -> AxisRole {
    match v {
        0 => AxisRole::Door,
        1..=9 => AxisRole::Reserved,
        99 => AxisRole::Pointer,
        _ => AxisRole::Normal,
    }
}

/// What a page number is (seqAddr 6, 6.1).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PageKind {
    /// `0000`: the book's door.
    Door,
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
    /// `9999`: book continuation.
    BookContinuation,
}

/// `9999` is matched before `% 100 == 99`, so the book continuation is not a band continuation.
pub fn page_kind(p: u16) -> PageKind {
    match p {
        0 => PageKind::Door,
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

/// The band head `PP00` of a page at or above 0100. `None` below 0100.
pub fn band_head(p: u16) -> Option<u16> {
    if p < 100 {
        None
    } else {
        Some(p - p % 100)
    }
}

const MSG_00_09: &str = "00-09 are system-reserved on every axis; work starts at 10 (t413u)";
const MSG_BOOK_00: &str = "DD.SS.00 is the shelf's authority book; only the system writes there (t413u)";
const MSG_99: &str = "99 is a pointer to the next location, not work (seqAddr.md:31, :249)";
const MSG_LOW: &str = "pages 0000-0099 are reserved (t413u)";
const MSG_9999: &str = "9999 is the book continuation, not work (seqAddr.md:226)";
const MSG_NN00: &str = "NN00 is the band head, the band's door; work goes on NN01-NN98 (t413u, seqAddr.md:241)";
const MSG_NN99: &str = "NN99 is the band's continuation, not work (seqAddr.md:242)";
const MSG_SHAPE: &str = "not a work address DD.SS.BB.PPPP";

/// A work address is `DD.SS.BB.PPPP`. Book `00` has its own message; every other
/// `00-09` on desk, shelf or book shares one. Checked after `check_addr`.
pub fn check_work(addr: &str) -> Res<()> {
    let (desk, shelf, book, page) = parse_work(addr).ok_or(MSG_SHAPE)?;
    if let Some(msg) = desk_block(desk) {
        return Err(msg.into());
    }
    if let Some(msg) = axis_block(shelf, false) {
        return Err(msg.into());
    }
    if let Some(msg) = axis_block(book, true) {
        return Err(msg.into());
    }
    if let Some(msg) = page_block(page) {
        return Err(msg.into());
    }
    Ok(())
}

fn parse_work(addr: &str) -> Option<(u8, u8, u8, u16)> {
    let mut parts = addr.split('.');
    let desk = two(parts.next()?)?;
    let shelf = two(parts.next()?)?;
    let book = two(parts.next()?)?;
    let page = four(parts.next()?)?;
    if parts.next().is_some() {
        return None;
    }
    Some((desk, shelf, book, page))
}

fn two(s: &str) -> Option<u8> {
    if s.len() == 2 && s.bytes().all(|b| b.is_ascii_digit()) {
        s.parse().ok()
    } else {
        None
    }
}

fn four(s: &str) -> Option<u16> {
    if s.len() == 4 && s.bytes().all(|b| b.is_ascii_digit()) {
        s.parse().ok()
    } else {
        None
    }
}

fn desk_block(d: u8) -> Option<&'static str> {
    match desk_kind(d) {
        DeskKind::Pointer => Some(MSG_99),
        DeskKind::Kernel | DeskKind::KernelBranch => Some(MSG_00_09),
        DeskKind::User => None,
    }
}

/// Book `00` is the shelf's authority book. Shelf `00`, and book `01-09`, stay on the 00-09 rule.
fn axis_block(v: u8, book: bool) -> Option<&'static str> {
    match axis_role(v) {
        AxisRole::Pointer => Some(MSG_99),
        AxisRole::Door if book => Some(MSG_BOOK_00),
        AxisRole::Door | AxisRole::Reserved => Some(MSG_00_09),
        AxisRole::Normal => None,
    }
}

fn page_block(p: u16) -> Option<&'static str> {
    // 9999 before NN99: page_kind names the book continuation ahead of a band continuation.
    if page_kind(p) == PageKind::BookContinuation {
        return Some(MSG_9999);
    }
    // PP00 at or above 0100 is the page that is its own band head.
    if band_head(p) == Some(p) {
        return Some(MSG_NN00);
    }
    match page_kind(p) {
        PageKind::Door | PageKind::SpecialReserved | PageKind::Required | PageKind::Localized | PageKind::Structural => Some(MSG_LOW),
        PageKind::BandContinuation => Some(MSG_NN99),
        PageKind::BandHead => Some(MSG_NN00),
        PageKind::BookContinuation => Some(MSG_9999),
        PageKind::StandardBand | PageKind::User => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn refused(addr: &str, msg: &str) {
        assert_eq!(check_work(addr).unwrap_err(), msg, "{addr}");
    }

    #[test]
    fn classifiers_match_seqaddr_core() {
        assert_eq!(desk_kind(0), DeskKind::Kernel);
        assert_eq!(desk_kind(5), DeskKind::KernelBranch);
        assert_eq!(desk_kind(90), DeskKind::User);
        assert_eq!(desk_kind(99), DeskKind::Pointer);
        assert_eq!(axis_role(0), AxisRole::Door);
        assert_eq!(axis_role(5), AxisRole::Reserved);
        assert_eq!(axis_role(50), AxisRole::Normal);
        assert_eq!(axis_role(99), AxisRole::Pointer);
        assert_eq!(page_kind(0), PageKind::Door);
        assert_eq!(page_kind(50), PageKind::Structural);
        assert_eq!(page_kind(400), PageKind::BandHead);
        assert_eq!(page_kind(401), PageKind::StandardBand);
        assert_eq!(page_kind(499), PageKind::BandContinuation);
        assert_eq!(page_kind(1498), PageKind::User);
        assert_eq!(page_kind(9999), PageKind::BookContinuation);
        assert_eq!(band_head(50), None);
        assert_eq!(band_head(401), Some(400));
        assert_eq!(band_head(9999), Some(9900));
    }

    #[test]
    fn each_rule_has_its_own_message() {
        refused("90.05.10.0401", MSG_00_09);
        refused("05.50.10.0401", MSG_00_09);
        refused("90.00.10.0401", MSG_00_09);
        refused("90.50.05.0401", MSG_00_09);
        refused("90.50.00.0401", MSG_BOOK_00);
        refused("99.50.10.0401", MSG_99);
        refused("90.99.10.0401", MSG_99);
        refused("90.50.99.0401", MSG_99);
        refused("90.50.10.0050", MSG_LOW);
        refused("90.50.10.0000", MSG_LOW);
        refused("90.50.10.0099", MSG_LOW);
        refused("90.50.10.9999", MSG_9999);
        refused("90.50.10.0400", MSG_NN00);
        refused("90.50.10.0100", MSG_NN00);
        refused("90.50.10.0499", MSG_NN99);
        refused("1.2.3.4", MSG_SHAPE);
        refused("10.10.10.401", MSG_SHAPE);
    }

    #[test]
    fn work_pages_pass() {
        for addr in ["90.50.10.0401", "90.50.10.0498", "10.10.10.0401"] {
            assert!(check_work(addr).is_ok(), "{addr}");
        }
    }
}
