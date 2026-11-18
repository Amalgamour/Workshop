//! Delivery ids: a write sent twice with one id is booked once (R37 item 2, K4).
//! Pass 05.02: the receipt survives a restart; same id with other content is refused in 05.03.
mod common;
use common::*;
use serde_json::{json, Value};

fn note(addr: &str, body: &str, delivery_id: Option<&str>) -> Value {
    let mut op = json!({"op": "note", "addr": addr, "body": body});
    if let Some(id) = delivery_id {
        op["delivery_id"] = json!(id);
    }
    op
}

async fn open_draft(s: &Srv) {
    let (c, v) = s.post("user", json!([put_t("10.11.21.0020.01", "draft", "## Route\nLocal draft route.")])).await;
    assert_eq!(c, 200, "{v}");
}

/// One write sent twice with one id grows the book by one change and both replies
/// match; a write with no id still books each send (as today). The booked line
/// carries `delivery_id`.
#[tokio::test]
async fn delivery_id_retry_writes_once_and_no_id_behaves_as_today() {
    let s = Srv::start(&kernel_dir("did-01")).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";

    let before_plain = s.lines("10.11.21");
    let (c1, v1) = s.post("user", json!([note(addr, "plain thought", None)])).await;
    let (c2, v2) = s.post("user", json!([note(addr, "plain thought", None)])).await;
    assert_eq!(c1, 200, "{v1}");
    assert_eq!(c2, 200, "{v2}");
    assert_ne!(v1, v2, "two no-id writes must be two answers, as today");
    assert_eq!(s.lines("10.11.21"), before_plain + 2, "no id: each send is booked");

    let before = s.lines("10.11.21");
    let op = note(addr, "first thought", Some("d-1"));
    let (c3, v3) = s.post("user", json!([op.clone()])).await;
    assert_eq!(c3, 200, "{v3}");
    assert_eq!(s.lines("10.11.21"), before + 1, "{v3}");
    let (c4, v4) = s.post("user", json!([op])).await;
    assert_eq!((c4, &v4), (c3, &v3), "retry must return the first answer");
    assert_eq!(s.lines("10.11.21"), before + 1, "retry must write nothing new");

    let book = std::fs::read_to_string(s.dir.join("10.11.21.book")).unwrap();
    let hit = book.lines().filter(|l| l.contains("first thought")).collect::<Vec<_>>();
    assert_eq!(hit.len(), 1, "{book}");
    assert!(hit[0].contains("\"delivery_id\":\"d-1\""), "id stored on the book entry: {}", hit[0]);
    s.stop().await;
}


/// Lost-reply path (Codex t292u): commit a write with an id, drop the reply,
/// restart the compute on the same write dir, resend. The book has one new edit
/// and the retry's book, status and entries match the first answer.
#[tokio::test]
async fn lost_reply_survives_restart() {
    let dir = kernel_dir("did-lr");
    let s = Srv::start(&dir).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";
    let before = s.lines("10.11.21");
    let op = note(addr, "kept thought", Some("d-restart"));
    let (c1, v1) = s.post("user", json!([op.clone()])).await;
    assert_eq!(c1, 200, "{v1}");
    assert_eq!(s.lines("10.11.21"), before + 1, "{v1}");
    let book = v1["book"].clone();
    let status = v1["status"].clone();
    let entries = v1["entries"].clone();
    s.stop().await;

    let s = Srv::start(&dir).await;
    let (c2, v2) = s.post("user", json!([op])).await;
    assert_eq!(c2, 200, "{v2}");
    assert_eq!(v2["book"], book, "{v2}");
    assert_eq!(v2["status"], status, "{v2}");
    assert_eq!(v2["entries"], entries, "{v2}");
    assert_eq!(s.lines("10.11.21"), before + 1, "retry after restart must write nothing new");
    s.stop().await;
}

/// If the book already holds two lines with the same writer and id, the first
/// booked entry wins after a restart.
#[tokio::test]
async fn first_entry_wins_after_restart_when_book_holds_duplicates() {
    let dir = kernel_dir("did-dup");
    let s = Srv::start(&dir).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";
    let op = note(addr, "first wins", Some("d-dup"));
    let (c1, v1) = s.post("user", json!([op.clone()])).await;
    assert_eq!(c1, 200, "{v1}");
    let first_entries = v1["entries"].clone();
    let n = first_entries[0].as_u64().expect("entry n");
    s.stop().await;

    let f = dir.join("10.11.21.book");
    let mut t = std::fs::read_to_string(&f).unwrap();
    let last = t.lines().last().unwrap();
    let mut e: Value = serde_json::from_str(last).unwrap();
    e["n"] = json!(n + 1);
    e["body"] = json!("second should lose");
    t.push_str(&format!("{e}\n"));
    std::fs::write(&f, t).unwrap();
    let before = std::fs::read_to_string(dir.join("10.11.21.book")).unwrap().lines().count();

    let s = Srv::start(&dir).await;
    let (c2, v2) = s.post("user", json!([op])).await;
    assert_eq!(c2, 200, "{v2}");
    assert_eq!(v2["entries"], first_entries, "first booked entry wins: {v2}");
    assert_eq!(v2["status"], "approved", "{v2}");
    assert_eq!(s.lines("10.11.21"), before, "retry must not book a third line");
    s.stop().await;
}

/// Auth runs first: a resend with a known id but a missing or wrong token is an
/// auth refusal, not a replay, and writes nothing.
#[tokio::test]
async fn resend_with_wrong_or_missing_token_is_auth_refusal_not_replay() {
    let s = Srv::start(&kernel_dir("did-auth")).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";
    let op = note(addr, "secret thought", Some("d-auth"));
    let (c1, v1) = s.post("user", json!([op.clone()])).await;
    assert_eq!(c1, 200, "{v1}");
    let before = s.lines("10.11.21");
    let body = json!({"by": "user", "ops": [op]}).to_string().into_bytes();

    let (c2, b2) = Http.req_h(&s.base, "POST", "/propose", Some(body.clone()), &[("content-type", "application/json")]).await;
    let v2: Value = serde_json::from_slice(&b2).unwrap_or(Value::Null);
    assert_eq!(c2, 401, "missing token must be auth, not a replay: {v2}");
    assert_eq!(v2["error"], "identity", "{v2}");
    assert_ne!(v2.get("entries"), v1.get("entries"), "must not replay the first answer: {v2}");

    let (c3, b3) = Http.req_h(&s.base, "POST", "/propose", Some(body), &[("content-type", "application/json"), ("authorization", "Bearer tok-nope-0123456789")]).await;
    let v3: Value = serde_json::from_slice(&b3).unwrap_or(Value::Null);
    assert_eq!(c3, 401, "wrong token must be auth, not a replay: {v3}");
    assert_eq!(v3["error"], "identity", "{v3}");
    assert_eq!(s.lines("10.11.21"), before, "auth refusal must write nothing");
    s.stop().await;
}

/// Ids are per writer: another writer sending the same id is a new write, not a replay.
#[tokio::test]
async fn another_writers_same_id_is_not_a_replay() {
    let s = Srv::start(&kernel_dir("did-writer")).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";
    let op = note(addr, "shared id body", Some("d-share"));
    let (c1, v1) = s.post("alice", json!([op.clone()])).await;
    assert_eq!(c1, 200, "{v1}");
    let after_alice = s.lines("10.11.21");
    let (c2, v2) = s.post("bob", json!([op.clone()])).await;
    assert_eq!(c2, 200, "{v2}");
    assert_ne!(&v2, &v1, "bob's same id is a new write, not alice's answer");
    assert_eq!(s.lines("10.11.21"), after_alice + 1, "{v2}");
    let (c3, v3) = s.post("bob", json!([op])).await;
    assert_eq!((c3, &v3), (c2, &v2), "bob's retry is his own first answer");
    assert_eq!(s.lines("10.11.21"), after_alice + 1, "bob's retry must write nothing new");
    s.stop().await;
}

/// Tester 05.01 follow-ups: overlong or control-bearing ids, and mixed ids in one
/// proposal, are refused with 400 and write nothing. 128 characters is accepted.
#[tokio::test]
async fn refuse_long_or_control_or_mixed_delivery_ids() {
    let s = Srv::start(&kernel_dir("did-cap")).await;
    seed(&s).await;
    open_draft(&s).await;
    let addr = "10.11.21.0020.01.draft";
    let before = s.lines("10.11.21");

    let long = "a".repeat(129);
    let (c, v) = s.post("user", json!([note(addr, "x", Some(&long))])).await;
    assert_eq!(c, 400, "129-char id: {v}");
    assert_eq!(s.lines("10.11.21"), before);

    let (c, v) = s.post("user", json!([note(addr, "x", Some("ok\nid"))])).await;
    assert_eq!(c, 400, "newline in id: {v}");
    let (c, v) = s.post("user", json!([note(addr, "x", Some("tab\there"))])).await;
    assert_eq!(c, 400, "tab in id: {v}");
    assert_eq!(s.lines("10.11.21"), before);

    let ok = "b".repeat(128);
    let (c, v) = s.post("user", json!([note(addr, "capped", Some(&ok))])).await;
    assert_eq!(c, 200, "128-char id must be accepted: {v}");
    assert_eq!(s.lines("10.11.21"), before + 1);

    let before = s.lines("10.11.21");
    let (c, v) = s.post("user", json!([note(addr, "one", Some("d-a")), note(addr, "two", Some("d-b"))])).await;
    assert_eq!(c, 400, "mixed ids: {v}");
    assert_eq!(s.lines("10.11.21"), before);
    s.stop().await;
}
