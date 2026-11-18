//! Delivery ids, pass 05.01: a write sent twice with one id is booked once
//! (R37 item 2, K4). Same id with other content is refused in 05.02.
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
