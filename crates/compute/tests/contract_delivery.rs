//! Pins CONTRACT.md delivery-id status codes to the compute source (pass 05.04 w04).
//! Fails if the addendum's 400 / 409 / 200-replay codes drift from store.rs.

use std::path::PathBuf;

fn root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..")
}

fn heading_section(text: &str, heading: &str) -> String {
    let start = text.find(heading).unwrap_or_else(|| panic!("CONTRACT.md is missing heading: {heading}"));
    let after = &text[start + heading.len()..];
    let end = after.find("\n## ").unwrap_or(after.len());
    text[start..start + heading.len() + end].to_string()
}

fn fn_src(src: &str, name: &str) -> String {
    let needle = format!("fn {name}");
    let start = src.find(&needle).unwrap_or_else(|| panic!("store.rs is missing fn {name}"));
    let after = &src[start..];
    let mut end = after.len();
    for (i, _) in after.match_indices('\n') {
        let rest = &after[i..];
        if rest.starts_with("\nfn ")
            || rest.starts_with("\npub fn ")
            || rest.starts_with("\n    fn ")
            || rest.starts_with("\n    pub fn ")
        {
            end = i;
            break;
        }
    }
    after[..end].to_string()
}

/// Three-digit numbers written as `(NNN,`.
fn paren_codes(s: &str) -> Vec<u16> {
    let b = s.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    while i + 4 < b.len() {
        if b[i] == b'(' && b[i + 1].is_ascii_digit() && b[i + 2].is_ascii_digit() && b[i + 3].is_ascii_digit() && b[i + 4] == b',' {
            out.push(std::str::from_utf8(&b[i + 1..i + 4]).unwrap().parse().unwrap());
        }
        i += 1;
    }
    out
}

fn only_code(s: &str, label: &str) -> u16 {
    let mut codes = paren_codes(s);
    codes.dedup();
    assert_eq!(codes.len(), 1, "{label} should use one status code, found {codes:?}");
    codes[0]
}

fn pinned_codes(addendum: &str) -> (u16, u16, u16) {
    const PREFIX: &str = "Pinned status codes: ";
    let line = addendum.lines().find(|l| l.starts_with(PREFIX)).unwrap_or_else(|| {
        panic!("CONTRACT addendum must contain a line starting with `{PREFIX}`")
    });
    let rest = &line[PREFIX.len()..];
    let bad = take_before(rest, " for a bad or mixed delivery id; ");
    let rest = after(rest, " for a bad or mixed delivery id; ");
    let conflict = take_before(rest, " for the same id with other content; ");
    let rest = after(rest, " for the same id with other content; ");
    let replay = take_before(rest, " for a replay of the same content.");
    assert!(rest.ends_with(" for a replay of the same content."), "pinned line ending drifted: {line}");
    (parse_code(bad, "bad-id"), parse_code(conflict, "other-content"), parse_code(replay, "replay"))
}

fn take_before<'a>(s: &'a str, sep: &str) -> &'a str {
    s.split_once(sep).unwrap_or_else(|| panic!("pinned line is missing `{sep}` in: {s}")).0
}

fn after<'a>(s: &'a str, sep: &str) -> &'a str {
    s.split_once(sep).unwrap_or_else(|| panic!("pinned line is missing `{sep}` in: {s}")).1
}

fn parse_code(s: &str, label: &str) -> u16 {
    s.parse().unwrap_or_else(|_| panic!("{label} status code is not a number: {s:?}"))
}

fn group_replay_code(group_fn: &str) -> u16 {
    let needle = "code: ";
    let i = group_fn.find(needle).unwrap_or_else(|| panic!("delivery_group must set hit.code"));
    let rest = group_fn[i + needle.len()..].trim_start();
    let digits: String = rest.chars().take_while(|c| c.is_ascii_digit()).collect();
    digits.parse().unwrap_or_else(|_| panic!("delivery_group code is not a number: {rest}"))
}

#[test]
fn contract_delivery_status_codes_match_the_code() {
    let contract = std::fs::read_to_string(root().join("docs/CONTRACT.md")).expect("docs/CONTRACT.md");
    let store = std::fs::read_to_string(root().join("crates/compute/src/store.rs")).expect("store.rs");

    let addendum = heading_section(&contract, "## Addendum (COMPUTE lane, 2026-11-18): delivery ids on POST /propose");
    let (doc_bad, doc_conflict, doc_replay) = pinned_codes(&addendum);

    let err_fn = fn_src(&store, "delivery_request_error");
    let replay_fn = fn_src(&store, "delivery_replay");
    let group_fn = fn_src(&store, "delivery_group");

    let code_bad = only_code(&err_fn, "delivery_request_error");
    let code_conflict = only_code(&replay_fn, "delivery_replay");
    let code_replay = group_replay_code(&group_fn);

    assert_eq!(
        (doc_bad, doc_conflict, doc_replay),
        (code_bad, code_conflict, code_replay),
        "CONTRACT.md delivery-id status codes drifted from crates/compute/src/store.rs (bad id, other content, replay)"
    );
}
