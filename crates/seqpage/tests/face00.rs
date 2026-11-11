//! Face 00: stamp + type + registry (docs/spec/face00.md, R12, R19). All findings.
mod common;
use common::*;
use seqaddr_core::log::BookLog;
use seqpage::face00::{self, Status};
use seqpage::{check_text, export, PageId};

const SRC: &str = "docs/spec/examples/sources/10.11.40.book";

fn book() -> BookLog {
    BookLog::parse(&read(SRC)).unwrap()
}

/// Replace face 00's body of `page` (the entry with addr starting `page.00`), export, check.
fn findings_with(page: &str, body: &str) -> (bool, Vec<String>) {
    let mut log = book();
    let e = log.entries.iter_mut().find(|e| e.addr.starts_with(&format!("{page}.00"))).unwrap();
    e.body = Some(body.to_string());
    let text = export(&log, PageId::parse(page).unwrap()).unwrap();
    let r = check_text(&text, None, Some(&log));
    (r.ok, r.findings.iter().map(|f| format!("{} {}", f.rule, f.detail)).collect())
}

#[test]
fn examples_are_golden_and_clean() {
    let log = book();
    for (page, file) in [
        ("10.11.40.0000", "10.11.40.0000.seq"),
        ("10.11.40.0012", "10.11.40.0012.dictionary.seq"),
        ("10.11.40.0400", "10.11.40.0400.dev.seq"),
        ("10.11.40.0403", "10.11.40.0403.ide-design.seq"),
        ("10.11.40.1001", "10.11.40.1001.cats.seq"),
    ] {
        let path = format!("docs/spec/examples/face00/{file}");
        let want = read(&path);
        assert_eq!(export(&log, PageId::parse(page).unwrap()).unwrap(), want, "{path}: regenerate with seqpage export");
        let r = check_text(&want, Some(&path), Some(&log));
        assert!(r.ok && r.findings.is_empty(), "{path}: {:?} {:?}", r.errors, r.findings);
    }
}

#[test]
fn code_table_mirrors_face00_md() {
    let doc = read("docs/spec/face00.md");
    for t in face00::TYPES {
        assert!(doc.contains(&format!("`{}`", t.name)), "type {} missing from face00.md", t.name);
        for f in t.fields {
            assert!(doc.contains(&format!("`{}`", f.name)), "field {} ({}) missing from face00.md", f.name, t.name);
        }
    }
    for f in face00::STAMP.iter().chain(face00::COMMON_REGISTRY).chain(face00::DOOR_PAGE_FIELDS).chain(face00::OVERRIDE_PAGE_FIELDS) {
        assert!(doc.contains(&format!("`{}`", f.name)), "field {} missing from face00.md", f.name);
        if f.status == Status::Proposed {
            assert!(!f.source.is_empty());
        }
    }
    assert!(doc.contains("DRAFT"));
    assert_eq!(face00::TYPES.iter().map(|t| t.name).collect::<Vec<_>>(), ["general", "system", "code", "workflow", "band", "pointer"], "C1.4 starting types only");
}

#[test]
fn unknown_type_is_a_finding_not_an_error() {
    let (ok, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: gizmo\nstate: live\n---\n\n## Registry\nfaces: 04 seated");
    assert!(ok, "never an error");
    assert!(f.iter().any(|x| x.contains("type `gizmo` is not a page type")), "{f:?}");
}

#[test]
fn registry_fields_follow_the_type() {
    // `role` is a band/workflow field, not a general one
    let (ok, f) = findings_with("10.11.40.1001", "---\naddress: 10.11.40.1001\ntitle: cats\ntype: general\nstate: draft\nwhy-draft: new\n---\n\n## Registry\nfaces: 01 draft\nrole: dev\nwhy-01: new");
    assert!(ok);
    assert!(f.iter().any(|x| x.contains("`role:` is not a registry field for type `general`")), "{f:?}");
    // the same field is fine on a band head
    let (_, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: band\nstate: live\n---\n\n## Registry\nfaces: 04 seated\nrole: dev\nlead: 3MP");
    assert!(f.is_empty(), "{f:?}");
}

#[test]
fn compute_only_fields_must_match_what_the_compute_derives() {
    let base = "---\naddress: 10.11.40.0403\ntitle: ide-design\ntype: workflow\nstate: live\n---\n\n## Registry\n";
    for (field, bad) in [("faces", "faces: 04 seated"), ("set", "set: 04.ide-design"), ("role", "role: jobs")] {
        let (ok, f) = findings_with("10.11.40.0403", &format!("{base}faces: 04 seated, 05 counted\n{bad}"));
        assert!(ok);
        assert!(f.iter().any(|x| x.contains(&format!("`{field}:")) && x.contains("derives")), "{field}: {f:?}");
    }
    let (_, f) = findings_with("10.11.40.0403", &format!("{base}faces: 04 seated, 05 counted\napproval: 7"));
    assert!(f.is_empty(), "`7` marks a missing compute value, not a mismatch: {f:?}");
}

#[test]
fn stamp_checks() {
    // address mismatch is elevated
    let (_, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0401\ntitle: dev\ntype: band\nstate: live\n---\n\n## Registry\nfaces: 04 seated");
    assert!(f.iter().any(|x| x.starts_with("A3.2")), "{f:?}");
    // state missing, then state disagreeing with the entries
    let (_, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: band\n---\n\n## Registry\nfaces: 04 seated");
    assert!(f.iter().any(|x| x.contains("no `state:`")), "{f:?}");
    let (_, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: band\nstate: retired\n---\n\n## Registry\nfaces: 04 seated");
    assert!(f.iter().any(|x| x.contains("disagrees with the page's entries")), "{f:?}");
    // a draft page must say why (R5)
    let (_, f) = findings_with("10.11.40.1001", "---\naddress: 10.11.40.1001\ntitle: cats\ntype: general\nstate: draft\n---\n\n## Registry\nfaces: 01 draft");
    assert!(f.iter().any(|x| x.starts_with("R5") && x.contains("why-draft")), "{f:?}");
    // unknown stamp field
    let (_, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: band\nstate: live\ncolour: red\n---\n\n## Registry\nfaces: 04 seated");
    assert!(f.iter().any(|x| x.contains("`colour:` is not a stamp field")), "{f:?}");
}

#[test]
fn door_page_title_is_the_containers_and_required() {
    let (_, f) = findings_with("10.11.40.0000", "---\naddress: 10.11.40.0000\nstate: live\n---\n\n## Registry\nfaces: -\nlevel: book");
    assert!(f.iter().any(|x| x.contains("container's title")), "{f:?}");
    let (_, f) = findings_with("10.11.40.0000", "---\naddress: 10.11.40.0000\ntitle: workshop\nstate: live\n---\n\n## Registry\nfaces: -\nlevel: shelf");
    assert!(f.iter().any(|x| x.contains("`level:")), "{f:?}");
    // the file name never carries the 0000 title
    assert_eq!(seqpage::file_name(PageId::parse("10.11.40.0000").unwrap(), Some("workshop")), "10.11.40.0000.seq");
}

#[test]
fn override_pages_take_r7_fields() {
    assert!(face00::registry_field(3, None, "why-needed").is_some());
    assert!(face00::registry_field(1003, None, "why-needed").is_none());
    assert!(face00::registry_field(0, None, "parent").is_some());
    assert!(face00::registry_field(1003, Some("general"), "why-04").is_some());
}

#[test]
fn missing_registry_card_is_reported() {
    let (ok, f) = findings_with("10.11.40.0400", "---\naddress: 10.11.40.0400\ntitle: dev\ntype: band\nstate: live\n---");
    assert!(ok);
    assert!(f.iter().any(|x| x.starts_with("R19")), "{f:?}");
}
