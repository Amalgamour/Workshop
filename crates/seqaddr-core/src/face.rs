//! Face jobs and card types (seqAddr 5.1, 5.3; A4.3; C1.1; C8.9).

use serde::Serialize;

/// The job of a face number (seqAddr 5.1, A4.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum FaceJob {
    /// 00: the registry, holding the page stamp and listing the page's faces (R10;
    /// not a sentinel, R9). On the door page 0000 it is the only face.
    Registry,
    /// 01: agents, the meaning of the page in cards.
    Law,
    /// 02: templates, formats, exact processes.
    Schema,
    /// 03: compute operations, the card menu.
    Operate,
    /// 04: users, the why, long form.
    User,
    /// 05: passes, as counters.
    Tasks,
    /// 06: one counter per session.
    Notes,
    /// 07: reserved, not active.
    Reserved07,
    /// 08: links, lineage with face 00.
    Map,
    /// 09: unassigned.
    Unassigned09,
    /// 10-98: reserved for later customization.
    Custom,
    /// 99: reserved.
    Reserved99,
}

pub fn face_job(ff: u8) -> FaceJob {
    match ff {
        0 => FaceJob::Registry,
        1 => FaceJob::Law,
        2 => FaceJob::Schema,
        3 => FaceJob::Operate,
        4 => FaceJob::User,
        5 => FaceJob::Tasks,
        6 => FaceJob::Notes,
        7 => FaceJob::Reserved07,
        8 => FaceJob::Map,
        9 => FaceJob::Unassigned09,
        99 => FaceJob::Reserved99,
        _ => FaceJob::Custom,
    }
}

impl FaceJob {
    pub fn name(self) -> &'static str {
        match self {
            FaceJob::Registry => "registry",
            FaceJob::Law => "law",
            FaceJob::Schema => "schema",
            FaceJob::Operate => "operate",
            FaceJob::User => "user",
            FaceJob::Tasks => "tasks",
            FaceJob::Notes => "notes",
            FaceJob::Reserved07 => "reserved",
            FaceJob::Map => "map",
            FaceJob::Unassigned09 => "unassigned",
            FaceJob::Custom => "reserved-custom",
            FaceJob::Reserved99 => "reserved",
        }
    }
}

/// Faces 00-06 and 08 are the active system faces. 07, 09, 10-99 are reserved (A4.3).
pub fn is_active_face(ff: u8) -> bool {
    matches!(ff, 0..=6 | 8)
}

/// Content faces that satisfy C1.1: 01-06 or 08. Face 07 does not count.
pub fn is_content_face(ff: u8) -> bool {
    matches!(ff, 1..=6 | 8)
}

/// Faces that are always counted (A4.4): 05 tasks and 06 notes.
pub fn always_counted(ff: u8) -> bool {
    matches!(ff, 5 | 6)
}

/// A card type known to the core (C8.9; `work` from workflow-loop S07).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct CardType {
    pub name: &'static str,
    /// Fields named in C8.9 for this type.
    pub fields: &'static [&'static str],
    /// Whether a 04 card with the same key is required (C8.9, C3.2).
    pub needs_04: bool,
    /// Fields only the compute writes.
    pub compute_fields: &'static [&'static str],
}

pub const CARD_TYPES: &[CardType] = &[
    CardType { name: "rule", fields: &["owner"], needs_04: true, compute_fields: &[] },
    CardType { name: "schema", fields: &["source", "form"], needs_04: true, compute_fields: &[] },
    CardType { name: "menu", fields: &[], needs_04: false, compute_fields: &[] },
    CardType { name: "why", fields: &["source", "why"], needs_04: false, compute_fields: &[] },
    CardType { name: "task", fields: &[], needs_04: false, compute_fields: &[] },
    CardType { name: "note", fields: &[], needs_04: false, compute_fields: &[] },
    CardType { name: "link", fields: &["target", "kind"], needs_04: false, compute_fields: &[] },
    CardType { name: "brand", fields: &["brand", "forms", "means", "meters"], needs_04: false, compute_fields: &["meters"] },
    CardType { name: "index", fields: &["default"], needs_04: false, compute_fields: &[] },
    // workflow-loop 5.2 (approved S07): a work card is a seqAddr card with `type: work`.
    CardType { name: "work", fields: &["title", "reason", "ask"], needs_04: false, compute_fields: &[] },
];

pub fn card_type(name: &str) -> Option<&'static CardType> {
    CARD_TYPES.iter().find(|t| t.name == name)
}

/// The default card type of a face (seqAddr 5.3, C8.9).
pub fn default_card_type(ff: u8) -> Option<&'static str> {
    match ff {
        1 => Some("rule"),
        2 => Some("schema"),
        3 => Some("menu"),
        4 => Some("why"),
        5 => Some("task"),
        6 => Some("note"),
        8 => Some("link"),
        _ => None,
    }
}

/// Page types (seqAddr 5.6, C1.4).
pub const PAGE_TYPES: &[&str] = &["system", "general", "code", "workflow", "band", "pointer"];

pub fn is_page_type(t: &str) -> bool {
    PAGE_TYPES.contains(&t)
}
