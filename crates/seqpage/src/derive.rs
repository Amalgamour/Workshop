//! Derived lines (seqpage.md 7). They are computed from the page's booked
//! entries alone, so export and check always agree and no book is needed.
//!
//! The page's state is found by replaying its entries through the core's own
//! rules (`BookState::apply`, default `Policy`) in a scratch book. A page
//! other than the door page 0000 gets a stand-in door `DD.SS.BB.0000.00`
//! first, because the core writes nothing in a book before its door
//! (format 4.1). The stand-in never appears in the file.

use crate::model::{slot_of, PageId, SectionKey};
use seqaddr_core::cards::parse_face;
use seqaddr_core::log::{Entry, Op};
use seqaddr_core::state::{BookState, PageState, Policy};
use seqaddr_core::tail::{FaceSlotState, PageTail};
use std::collections::BTreeMap;

/// Value written when a derived value cannot be computed (axiom 7: unknown stays unknown).
pub const UNKNOWN: &str = "7";
/// Value written when a stamp field is absent.
pub const NONE: &str = "-";

pub struct Derivation {
    /// Section key -> derived lines in their written order.
    pub sections: BTreeMap<SectionKey, Vec<(&'static str, String)>>,
    /// Why the page's own replay failed, if it did (reported as a finding).
    pub replay_error: Option<String>,
}

/// Replay the page's entries alone. Returns the page state, or the core's reason.
pub fn local_replay(page: PageId, entries: &[Entry]) -> Result<Option<PageState>, String> {
    let policy = Policy::default();
    let mut st = BookState::new(page.book);
    let mut next = 1u64;
    if page.page != 0 {
        let mut door = Entry::new(next, "2000-01-01T00:00:00Z", "seqpage-stand-in", Op::Put, format!("{}.0000.00", page.book));
        door.body = Some("---\ntitle: stand-in\n---".into());
        st.apply(&door, &policy).map_err(|e| format!("stand-in door: {e}"))?;
        next += 1;
    }
    let mut renum: BTreeMap<u64, u64> = BTreeMap::new();
    for e in entries {
        let mut e2 = e.clone();
        renum.insert(e.n, next);
        e2.n = next;
        if let Some(c) = e.cites {
            e2.cites = Some(*renum.get(&c).ok_or_else(|| format!("@{} cites @{c}, which is not on this page", e.n))?);
        }
        st.apply(&e2, &policy).map_err(|err| format!("@{}: {err}", e.n))?;
        next += 1;
    }
    Ok(st.page(page.page).cloned())
}

fn slot_word(s: FaceSlotState) -> &'static str {
    match s {
        FaceSlotState::Absent => "absent",
        FaceSlotState::DraftOnly => "draft",
        FaceSlotState::Seated => "seated",
        FaceSlotState::SeatedWithDraft => "seated+draft",
        FaceSlotState::Retired => "retired",
    }
}

fn page_word(t: PageTail) -> &'static str {
    match t {
        PageTail::Live => "live",
        PageTail::Draft => "draft",
        PageTail::Retired => "retired",
    }
}

/// `cards := a, b` for a face body: the card keys in order (seqAddr 5.3).
/// `None` when the body has no cards or is the door stamp.
pub fn cards_value(key: SectionKey, body: Option<&str>) -> Option<String> {
    if key.face == 0 {
        return None;
    }
    let body = body?;
    match parse_face(body) {
        Ok(doc) if doc.cards.is_empty() => None,
        Ok(doc) => Some(doc.contents().join(", ")),
        Err(_) => Some(UNKNOWN.to_string()),
    }
}

/// `faces := 01 draft, 04 seated, 05 counted`: what the registry lists (R10),
/// derived from the page's own entries.
fn faces_value(by_key: &BTreeMap<SectionKey, Vec<&Entry>>, state: Option<&PageState>, ok: bool) -> String {
    let faces: std::collections::BTreeSet<u8> = by_key.keys().map(|k| k.face).filter(|f| *f != 0).collect();
    if faces.is_empty() {
        return NONE.into();
    }
    faces
        .into_iter()
        .map(|f| {
            let fs = state.and_then(|p| p.face(f));
            let word = if !ok {
                UNKNOWN.to_string()
            } else if by_key.keys().any(|k| k.face == f && k.counter.is_some()) {
                "counted".to_string()
            } else {
                slot_word(fs.map(|x| x.slot_state()).unwrap_or(FaceSlotState::Absent)).to_string()
            };
            format!("{f:02} {word}")
        })
        .collect::<Vec<_>>()
        .join(", ")
}

/// R10 / R7: what the page number says the page is, where a ruling names it.
pub fn kind_value(page: u16) -> Option<&'static str> {
    match page {
        0 => Some("book door (R10: face 00 only)"),
        1..=9 => Some("override (R7)"),
        _ => None,
    }
}

/// R5: why a face is a draft. The `reason` field of the entry that opened the
/// current draft (a `put` with tail draft, or a `copy`), else the first line of
/// the first `note` on it, else none (shown as `7`). Provisional (QUESTIONS S7).
pub fn draft_reason(own: &[&Entry]) -> Option<String> {
    let mut reason: Option<String> = None;
    let mut open = false;
    for e in own {
        let addr_draft = e.addr.ends_with(".draft");
        let tail_draft = e.tail.as_deref() == Some("draft");
        match e.op {
            Op::Put if addr_draft || tail_draft => {
                open = true;
                reason = e.extra.get("reason").and_then(|v| v.as_str()).map(String::from);
            }
            Op::Copy => {
                open = true;
                reason = e.extra.get("reason").and_then(|v| v.as_str()).map(String::from);
            }
            Op::Note if open && reason.is_none() => {
                reason = e.body.as_deref().and_then(|b| b.lines().map(str::trim).find(|l| !l.is_empty())).map(String::from);
            }
            Op::Promote => {
                open = false;
                reason = None;
            }
            _ => {}
        }
    }
    if open {
        reason
    } else {
        None
    }
}

/// The newest face 00 body (draft if any, else seated), by the page's own replay.
pub fn registry_view(page: PageId, entries: &[Entry]) -> Option<String> {
    local_replay(page, entries).ok().flatten().and_then(|p| p.face(0).and_then(|f| f.view()).map(String::from))
}

/// The lineage line: the page, then the A1.8 lookup chain it inherits through.
pub fn lineage_value(page: PageId) -> String {
    let mut parts = vec![page.to_string()];
    for b in page.book.lookup_chain() {
        parts.push(b.to_string());
    }
    parts.join(" < ")
}

fn refs(entries: &[&Entry]) -> String {
    entries.iter().map(|e| format!("@{}", e.n)).collect::<Vec<_>>().join(" ")
}

/// Every derived line of every section, from the booked entries.
pub fn derive(page: PageId, entries: &[Entry]) -> Derivation {
    let (state, replay_error) = match local_replay(page, entries) {
        Ok(s) => (s, None),
        Err(e) => (None, Some(e)),
    };
    let ok = replay_error.is_none();
    let mut by_key: BTreeMap<SectionKey, Vec<&Entry>> = BTreeMap::new();
    for e in entries {
        if let Some((_, k)) = slot_of(&e.addr) {
            by_key.entry(k).or_default().push(e);
        }
    }
    let mut sections: BTreeMap<SectionKey, Vec<(&'static str, String)>> = BTreeMap::new();

    // Registry, face 00 (seqpage.md 4, R10).
    let stamp = state.as_ref().and_then(|p| p.stamp());
    let field = |k: &str| -> String {
        if !ok {
            return UNKNOWN.into();
        }
        stamp.as_ref().and_then(|s| s.get(k)).filter(|v| !v.is_empty()).map(|v| v.to_string()).unwrap_or_else(|| NONE.into())
    };
    let mut door = vec![("title", field("title"))];
    door.push((
        "state",
        if ok { state.as_ref().map(|p| page_word(p.tail()).to_string()).unwrap_or_else(|| NONE.into()) } else { UNKNOWN.into() },
    ));
    door.push((
        "registry",
        if ok { slot_word(state.as_ref().and_then(|p| p.face(0)).map(|f| f.slot_state()).unwrap_or(FaceSlotState::Absent)).to_string() } else { UNKNOWN.into() },
    ));
    if ok && matches!(state.as_ref().and_then(|p| p.face(0)).map(|f| f.slot_state()), Some(FaceSlotState::DraftOnly | FaceSlotState::SeatedWithDraft)) {
        let own: Vec<&Entry> = by_key.get(&SectionKey::DOOR).cloned().unwrap_or_default();
        door.push(("why-draft", draft_reason(&own).unwrap_or_else(|| UNKNOWN.into())));
    }
    door.push(("faces", faces_value(&by_key, state.as_ref(), ok)));
    door.push(("type", field("type")));
    door.push(("axioms", field("axioms")));
    door.push(("lineage", lineage_value(page)));
    if let Some(k) = kind_value(page.page) {
        door.push(("kind", k.to_string()));
    }
    let door_entries = by_key.get(&SectionKey::DOOR).cloned().unwrap_or_default();
    door.push(("source", if door_entries.is_empty() { format!("book {}", page.book) } else { format!("book {} {}", page.book, refs(&door_entries)) }));
    sections.insert(SectionKey::DOOR, door);

    // Faces and counters (seqpage.md 5).
    let faces: std::collections::BTreeSet<u8> = by_key.keys().filter(|k| k.face != 0 || k.counter.is_some()).map(|k| k.face).collect();
    for f in faces {
        let fs = state.as_ref().and_then(|p| p.face(f));
        let mut lines = Vec::new();
        if let Some(own) = by_key.get(&SectionKey::face(f)) {
            let slot = fs.map(|x| x.slot_state()).unwrap_or(FaceSlotState::Absent);
            lines.push(("state", if ok { slot_word(slot).to_string() } else { UNKNOWN.into() }));
            if ok && matches!(slot, FaceSlotState::DraftOnly | FaceSlotState::SeatedWithDraft) {
                lines.push(("why-draft", draft_reason(own).unwrap_or_else(|| UNKNOWN.into())));
            }
            lines.push(("source", format!("book {} {}", page.book, refs(own))));
        }
        let counters: Vec<u8> = by_key.keys().filter(|k| k.face == f).filter_map(|k| k.counter).collect();
        if !counters.is_empty() {
            let board = if ok {
                counters
                    .iter()
                    .map(|nn| format!("{nn:02} {}", fs.and_then(|x| x.counters.get(nn)).map(|c| c.tail.board_word()).unwrap_or(UNKNOWN)))
                    .collect::<Vec<_>>()
                    .join(", ")
            } else {
                UNKNOWN.into()
            };
            lines.push(("counters", board));
        }
        if f != 0 {
            sections.insert(SectionKey::face(f), lines);
        } else if !lines.is_empty() {
            // counters on face 00 (not legal in the core, kept for losslessness)
            sections.get_mut(&SectionKey::DOOR).unwrap().extend(lines.into_iter().filter(|(k, _)| *k == "counters"));
        }
        for nn in counters {
            let k = SectionKey::counter(f, nn);
            let es = by_key.get(&k).cloned().unwrap_or_default();
            let st = if ok { fs.and_then(|x| x.counters.get(&nn)).map(|c| c.tail.board_word().to_string()).unwrap_or_else(|| UNKNOWN.into()) } else { UNKNOWN.into() };
            sections.insert(k, vec![("state", st), ("source", format!("book {} {}", page.book, refs(&es)))]);
        }
    }
    Derivation { sections, replay_error }
}
