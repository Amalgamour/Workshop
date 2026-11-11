//! Face 00: the page's registry location (R10, R12, R19). DRAFT.
//!
//! Mirrors docs/spec/face00.md. Face 00 holds:
//! - the **stamp** portion (front matter): address, title, type, state,
//!   why-draft, axioms, lineage;
//! - a **registry** (`## Registry` card): the faces list plus fields that
//!   depend on the page type.
//!
//! Every check here is a **finding**, never an error: which ones become hard
//! rejections is for the Director (face00.md "Open", F7). An unknown type is a finding.

use crate::error::PageError;
use crate::model::PageId;
use seqaddr_core::cards::{parse_face, parse_stamp};

/// Where a field's rule comes from.
#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Status {
    /// The spec or a ruling gives both the idea and the field.
    Sourced,
    /// Drafted by the builders to fill a gap (R19). Not law.
    Proposed,
}

#[derive(Debug, Clone, Copy, serde::Serialize)]
pub struct FieldSpec {
    pub name: &'static str,
    pub meaning: &'static str,
    pub source: &'static str,
    pub status: Status,
    /// Written only by the compute (derived); a written value must match.
    pub compute_only: bool,
}

const fn f(name: &'static str, meaning: &'static str, source: &'static str, status: Status, compute_only: bool) -> FieldSpec {
    FieldSpec { name, meaning, source, status, compute_only }
}
use Status::{Proposed, Sourced};

/// The stamp portion every face 00 has (face00.md section 1).
pub const STAMP: &[FieldSpec] = &[
    f("address", "the page's full address DD.SS.BB.PPPP", "decisions.md:176 (A4.2); R12", Sourced, false),
    f("title", "the page's title; on page 0000 the container's title", "decisions.md:131-132 (A2.8), :143 (A3.1); R12", Sourced, false),
    f("type", "the page type (section 2)", "decisions.md:285 (C1.4); R12; R19", Sourced, false),
    f("state", "page state: live, draft or retired", "decisions.md:176 (A4.2); R12; seqAddr.md section 4", Sourced, false),
    f("why-draft", "why the page is a draft; present when state is draft", "R5 follow-up (field name PROPOSED)", Proposed, false),
    f("axioms", "axiom chain cited on the page", "decisions.md:553 (E2)", Sourced, false),
    f("lineage", "the line back to what governs the page; kept by the compute", "decisions.md:577-582 (E6); R19 (form PROPOSED)", Proposed, true),
];

/// Registry fields every page type has (face00.md section 3.1).
pub const COMMON_REGISTRY: &[FieldSpec] = &[
    f("faces", "the page's faces and their state, e.g. `01 seated, 04 draft, 05 counted`", "R10; derived per decisions.md:301 (tension, F2)", Sourced, true),
    // `why-NN` (why face NN is a draft) is matched by pattern in `registry_field`.
];

/// The `why-NN` pattern: why face NN is a draft (R5). PROPOSED name.
pub const WHY_FACE: FieldSpec = f("why-NN", "why face NN is a draft", "R5 follow-up (field name PROPOSED)", Proposed, false);

#[derive(Debug, Clone, Copy, serde::Serialize)]
pub struct TypeSpec {
    pub name: &'static str,
    pub meaning: &'static str,
    pub source: &'static str,
    pub fields: &'static [FieldSpec],
}

/// The page types the spec names (decisions.md:286 C1.4), with their registry fields.
pub const TYPES: &[TypeSpec] = &[
    TypeSpec { name: "general", meaning: "an ordinary page; the default type", source: "decisions.md:286, :289 (C1.4)", fields: &[] },
    TypeSpec {
        name: "system",
        meaning: "a page of the system's own rules (kernel and desk law)",
        source: "decisions.md:286 (C1.4)",
        fields: &[f("owner", "who may change it: kernel-only, desk-local or book-local", "decisions.md:287 (C1.4 'owner: kernel-only'); E9 owner class (decisions.md:610)", Proposed, false)],
    },
    TypeSpec {
        name: "code",
        meaning: "a page about code; the code itself lives in the repo",
        source: "decisions.md:286 (C1.4); workflow-loop.003.md section 3.1",
        fields: &[f("repo", "the repository its face 08 file links point into", "workflow-loop.003.md:68-77 (section 3.1)", Proposed, false)],
    },
    TypeSpec {
        name: "workflow",
        meaning: "a page in a workflow band (N3 build, N4 dev, N5 jobs, N7 colab)",
        source: "decisions.md:286 (C1.4); workflow-loop.003.md section 2",
        fields: &[
            f("role", "the band's workflow role: build, dev, jobs or colab", "workflow-loop.003.md:38-50 (section 2)", Sourced, true),
            f("set", "the cross-band set key CC.title (N403.ide-design matches N503.ide-design)", "R18", Sourced, true),
            f("approval", "the approval record of the current N4 revision (dev pages)", "workflow-loop.003.md:86 (S01); a record, not a flag", Proposed, true),
        ],
    },
    TypeSpec {
        name: "band",
        meaning: "a band head N?00: binds a set of pages into a work space",
        source: "decisions.md:286 (C1.4); R13; seqAddr.md:241",
        fields: &[
            f("role", "the workflow role this band adopts by name", "workflow-loop.003.md:38", Sourced, false),
            f("default-type", "page type for pages in the band whose stamp has none", "decisions.md:289 (C1.4)", Sourced, false),
            f("lead", "default lead letters for work in the band", "Axioms.md:17 (axiom 3); workflow-loop.003.md:107", Sourced, false),
            f("contents", "the band's pages; derived", "seqAddr.md:241; decisions.md:301", Sourced, true),
            f("continues", "the band's continuation PP99, if any; derived", "seqAddr.md section 7.1; decisions.md A5.1", Sourced, true),
        ],
    },
    TypeSpec {
        name: "pointer",
        meaning: "contents, dictionary and concordance pages (continuations: open)",
        source: "decisions.md:286, :292 (C1.4)",
        fields: &[
            f("kind", "which pointer page: contents, dictionary, concordance or continuation", "decisions.md:292 (C1.4 open)", Proposed, false),
            f("index", "the face that holds the index (dictionary: 03)", "brands.md:15; decisions.md:424 (C8.3)", Sourced, false),
            f("layout", "the fixed section layout it follows (dictionary: kernel)", "brands.md:82", Sourced, false),
        ],
    },
];

/// Registry fields for pages the spec places but gives no type (face00.md section 3.3).
pub const DOOR_PAGE_FIELDS: &[FieldSpec] = &[
    f("level", "which container this is: kernel, desk, shelf or book; derived from the address", "seqAddr.md section 1.4-1.5", Sourced, true),
    f("parent", "back-link to the pointer that names this container (face 08 is not allowed on 0000)", "decisions.md:230 (A5.3); R10", Proposed, false),
    f("continues", "the book's continuation 9999, if any; derived", "decisions.md A4.6, A5.1", Sourced, true),
];

pub const OVERRIDE_PAGE_FIELDS: &[FieldSpec] = &[
    f("changes", "what it changes: a face, a behavior (0020-0049) or a structure (0050-0099)", "R7", Proposed, false),
    f("why-here", "why it is there", "R7", Proposed, false),
    f("why-needed", "why it is needed", "R7", Proposed, false),
    f("achieves", "what it should achieve", "R7", Proposed, false),
    f("authorized-by", "who authorized the override", "decisions.md:582 (E6)", Proposed, false),
];

pub fn type_spec(name: &str) -> Option<&'static TypeSpec> {
    TYPES.iter().find(|t| t.name == name)
}

/// Face 00 read into its parts.
#[derive(Debug, Clone, Default, PartialEq, serde::Serialize)]
pub struct Face00 {
    pub stamp: Vec<(String, String)>,
    pub has_registry: bool,
    pub registry: Vec<(String, String)>,
}

impl Face00 {
    pub fn stamp(&self, k: &str) -> Option<&str> {
        self.stamp.iter().find(|(a, _)| a == k).map(|(_, v)| v.as_str())
    }
    pub fn registry(&self, k: &str) -> Option<&str> {
        self.registry.iter().find(|(a, _)| a == k).map(|(_, v)| v.as_str())
    }
}

pub fn parse_face00(body: &str) -> Face00 {
    let stamp = parse_stamp(body).fields;
    let (has_registry, registry) = match parse_face(body) {
        Ok(doc) => match doc.card("registry") {
            Some(c) => (true, c.fields.clone()),
            None => (false, vec![]),
        },
        Err(_) => (false, vec![]),
    };
    Face00 { stamp, has_registry, registry }
}

/// The registry field spec for `key` on a page, if the key is allowed there.
pub fn registry_field(page: u16, ty: Option<&str>, key: &str) -> Option<FieldSpec> {
    if let Some(s) = COMMON_REGISTRY.iter().find(|s| s.name == key) {
        return Some(*s);
    }
    if key.len() == 6 && key.starts_with("why-") && key[4..].bytes().all(|b| b.is_ascii_digit()) {
        return Some(WHY_FACE);
    }
    let extra: &[FieldSpec] = match page {
        0 => DOOR_PAGE_FIELDS,
        1..=9 => OVERRIDE_PAGE_FIELDS,
        _ => &[],
    };
    if let Some(s) = extra.iter().find(|s| s.name == key) {
        return Some(*s);
    }
    ty.and_then(type_spec).and_then(|t| t.fields.iter().find(|s| s.name == key).copied())
}

/// Values the compute would write for compute-only fields it can derive here.
pub fn derived_value(page: PageId, title: Option<&str>, key: &str, faces: &str, lineage: &str) -> Option<String> {
    match key {
        "faces" => Some(faces.to_string()),
        "lineage" => Some(lineage.to_string()),
        "set" if page.page >= 100 => title.map(|t| format!("{:02}.{t}", page.page % 100)),
        "role" => match page.page / 100 {
            3 => Some("build".into()),
            4 => Some("dev".into()),
            5 => Some("jobs".into()),
            7 => Some("colab".into()),
            _ => None,
        },
        "level" => Some(
            match (page.book.desk, page.book.shelf, page.book.book) {
                (0, 0, 0) => "kernel",
                (_, 0, 0) => "desk",
                (_, _, 0) => "shelf",
                _ => "book",
            }
            .into(),
        ),
        _ => None,
    }
}

/// Findings on a face 00 body (face00.md section 5). `page_state` and `faces`,
/// `lineage` are the derived values the .seq file shows.
pub fn check_face00(page: PageId, body: &str, page_state: &str, faces: &str, lineage: &str) -> Vec<PageError> {
    let f00 = parse_face00(body);
    let mut out = Vec::new();
    let r = "face00";
    // stamp
    match f00.stamp("address") {
        None => out.push(PageError::missing(0, r, "the stamp has no `address:` (A4.2, R12)")),
        Some(a) if a != page.to_string() => out.push(PageError::elevate(0, "A3.2", format!("stamp address `{a}` is not the page {page}; a mismatch goes to the user"))),
        _ => {}
    }
    let title = f00.stamp("title").filter(|t| !t.is_empty());
    if title.is_none() && (page.page == 0 || page.page >= 1000) {
        let why = if page.page == 0 { "page 0000's stamp holds the container's title (A3.1)" } else { "pages 1000 and up need a title in the stamp (A2.8)" };
        out.push(PageError::missing(0, r, format!("the stamp has no `title:`; {why}")));
    }
    let ty = f00.stamp("type").filter(|t| !t.is_empty());
    match ty {
        None => {} // legal: default is the band head's default, else general (C1.4)
        Some(t) if type_spec(t).is_none() => out.push(PageError::invalid(0, r, format!("type `{t}` is not a page type the spec names (C1.4: system, general, code, workflow, band, pointer); finding only"))),
        _ => {}
    }
    match f00.stamp("state") {
        None => out.push(PageError::missing(0, r, "the stamp has no `state:` (R12: a page's state is kept in the stamp)")),
        Some(s) if !["live", "draft", "retired"].contains(&s) => out.push(PageError::invalid(0, r, format!("state `{s}` is not live, draft or retired (seqAddr.md section 4)"))),
        Some(s) => {
            if page_state != crate::derive::UNKNOWN && page_state != crate::derive::NONE && s != page_state {
                out.push(PageError::connection(0, r, format!("stamp state `{s}` disagrees with the page's entries (`{page_state}`)")));
            }
            if s == "draft" && f00.stamp("why-draft").map(str::is_empty).unwrap_or(true) {
                out.push(PageError::missing(0, "R5", "the stamp says draft but gives no `why-draft:`"));
            }
        }
    }
    for (k, v) in &f00.stamp {
        if !STAMP.iter().any(|s| s.name == k) {
            out.push(PageError::invalid(0, r, format!("`{k}:` is not a stamp field (face00.md section 1)")));
        } else if k == "lineage" && v != lineage {
            out.push(PageError::connection(0, r, format!("stamp lineage `{v}` disagrees with the address chain `{lineage}` (E6: the compute keeps it)")));
        }
    }
    // registry
    if !f00.has_registry {
        out.push(PageError::missing(0, "R19", "face 00 has no `## Registry` card (R10, R19)"));
    }
    for (k, v) in &f00.registry {
        match registry_field(page.page, ty, k) {
            None => out.push(PageError::invalid(
                0,
                r,
                format!("`{k}:` is not a registry field for type `{}` (face00.md section 3)", ty.unwrap_or("general (default)")),
            )),
            Some(spec) if spec.compute_only && v != "7" => {
                if let Some(want) = derived_value(page, title, k, faces, lineage) {
                    if *v != want {
                        out.push(PageError::connection(0, r, format!("`{k}: {v}` disagrees with what the compute derives (`{want}`); compute-only fields are never hand-edited")));
                    }
                }
            }
            _ => {}
        }
    }
    out
}
