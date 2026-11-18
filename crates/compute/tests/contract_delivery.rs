//! Pins CONTRACT.md delivery-id status codes to live compute behaviour (pass 05.05 w04).
//! Reads the pinned line from the newest addendum and fails if two pinned lines disagree.

mod common;
use common::*;
use serde_json::{json, Value};
use std::path::PathBuf;

fn contract_text() -> String {
    std::fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../docs/CONTRACT.md")).expect("docs/CONTRACT.md")
}

fn parse_pinned(line: &str) -> (u16, u16, u16) {
    const PREFIX: &str = "Pinned status codes: ";
    assert!(line.starts_with(PREFIX), "not a pinned line: {line}");
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

/// Pinned 400/409/200 codes from the newest addendum. Fails if two pinned lines disagree.
fn newest_pinned(text: &str) -> (u16, u16, u16) {
    let lines: Vec<&str> = text.lines().filter(|l| l.starts_with("Pinned status codes: ")).collect();
    assert!(!lines.is_empty(), "CONTRACT.md has no pinned status-codes line");
    let parsed: Vec<(u16, u16, u16)> = lines.iter().copied().map(parse_pinned).collect();
    for (i, p) in parsed.iter().enumerate().skip(1) {
        assert_eq!(
            &parsed[0], p,
            "pinned status-code lines disagree: {:?} vs {:?} ({:?} vs {:?})",
            parsed[0], p, lines[0], lines[i]
        );
    }
    parsed[parsed.len() - 1]
}

/// "a missing or unknown token is NNN" codes in the delivery-id addenda; they must agree.
fn missing_token_codes(text: &str) -> Vec<u16> {
    let start = text.find("## Addendum (COMPUTE lane, 2026-11-18): delivery ids").expect("delivery-id addendum");
    let key = "token is ";
    let mut out = Vec::new();
    let mut s = &text[start..];
    while let Some(i) = s.find(key) {
        let rest = &s[i + key.len()..];
        let digits: String = rest.chars().take_while(|c| c.is_ascii_digit()).collect();
        if !digits.is_empty() {
            out.push(digits.parse().expect("token status code"));
        }
        s = &s[i + key.len()..];
    }
    out
}

fn note(addr: &str, body: &str, delivery_id: Option<&str>) -> Value {
    let mut op = json!({"op": "note", "addr": addr, "body": body});
    if let Some(id) = delivery_id {
        op["delivery_id"] = json!(id);
    }
    op
}

#[tokio::test]
async fn contract_delivery_status_codes_match_the_code() {
    let text = contract_text();
    let (bad, conflict, replay) = newest_pinned(&text);
    let token_codes = missing_token_codes(&text);
    assert!(!token_codes.is_empty(), "delivery-id addenda must say what a missing token returns");
    assert!(
        token_codes.windows(2).all(|w| w[0] == w[1]),
        "missing-token codes in the doc disagree: {token_codes:?}"
    );
    let doc_auth = *token_codes.last().unwrap();

    let s = Srv::start(&kernel_dir("did-contract")).await;
    seed(&s).await;
    let (c, v) = s.post("user", json!([put_t("10.11.21.0020.01", "draft", "## Route\nLocal draft route.")])).await;
    assert_eq!(c, 200, "{v}");
    let addr = "10.11.21.0020.01.draft";

    let body = json!({"ops": [note(addr, "x", Some("d-auth"))]}).to_string().into_bytes();
    let (c_auth, b_auth) = Http.req_h(&s.base, "POST", "/propose", Some(body), &[("content-type", "application/json")]).await;
    let v_auth: Value = serde_json::from_slice(&b_auth).unwrap_or(Value::Null);
    assert_eq!(c_auth, doc_auth, "missing token: doc {doc_auth}, compute {c_auth}, {v_auth}");

    let (c128, v128) = s.post("user", json!([note(addr, "capped", Some(&"b".repeat(128)))])).await;
    assert_eq!(c128, 200, "128-char id must be accepted: {v128}");

    let (c129, v129) = s.post("user", json!([note(addr, "x", Some(&"a".repeat(129)))])).await;
    assert_eq!(c129, bad, "129-char id: doc {bad}, compute {c129}, {v129}");

    let op = note(addr, "first thought", Some("d-1"));
    let (c1, v1) = s.post("user", json!([op.clone()])).await;
    assert_eq!(c1, 200, "{v1}");
    let before = s.lines("10.11.21");
    let (c2, v2) = s.post("user", json!([op])).await;
    assert_eq!(c2, replay, "replay: doc {replay}, compute {c2}, {v2}");
    assert_eq!(&v2, &v1, "replay must return the first answer");
    assert_eq!(s.lines("10.11.21"), before, "replay must write nothing");

    let (c3, v3) = s.post("user", json!([note(addr, "other body", Some("d-1"))])).await;
    assert_eq!(c3, conflict, "other content: doc {conflict}, compute {c3}, {v3}");
    assert_eq!(s.lines("10.11.21"), before, "other content must write nothing");

    s.stop().await;
}
