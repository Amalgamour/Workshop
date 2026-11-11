//! The Bob test over HTTP (R11): session 1 makes the brand bob = the user's name;
//! session 2 (a fresh compute on the same books) asks for it three ways.
mod common;
use common::*;
use serde_json::{json, Value};

const SEED: &str = include_str!("../../ask/seed/common-questions.proposal.json");

/// Session 1: the reader's book, its brand page and the common-questions seed.
async fn session_one(s: &Srv) {
    seed(s).await;
    let brand = "## bob\ntype: brand\nbrand: bob.001\nforms: Bob\nmeans: the user's name\n\n## cats\ntype: brand\nbrand: cats.001\nforms: cats\nmeans: animals the user likes";
    let (c, v) = s.post("alice", json!([put_t("10.11.21.1001.00", "draft", "---\ntitle: bob\n---"), put_t("10.11.21.1001.01", "draft", brand)])).await;
    assert_eq!(c, 200, "{v}");
    let seed_ops: Value = serde_json::from_str(SEED).unwrap();
    let (c, v) = s.post_as("alice", "/propose", json!({"ops": seed_ops["ops"]})).await;
    assert_eq!(c, 200, "the seed applies as drafts: {v}");
}

fn top3(v: &Value) -> Vec<String> {
    v["pieces"].as_array().map(|a| a.iter().map(|p| p["address"].as_str().unwrap().to_string()).collect()).unwrap_or_default()
}

#[tokio::test]
async fn bob_test_end_to_end() {
    let dir = kernel_dir("bob");
    let s = Srv::start(&dir).await;
    session_one(&s).await;
    s.stop().await;

    // session 2: a new compute process on the same books
    let s = Srv::start(&dir).await;
    for prompt in ["what is my name", "whats my name?", "who am I"] {
        let (c, v) = s.ask(prompt).await;
        assert_eq!(c, 200, "{v}");
        let top = top3(&v);
        assert!(top.len() <= 3 && top.iter().any(|a| a == "10.11.21.1001.01.bob"), "{prompt}: {v}");
        let p = &v["pieces"][0];
        assert_eq!(p["card"]["title"], "bob", "{v}");
        assert_eq!(p["card"]["fields"]["means"], "the user's name");
        assert_eq!(p["card"]["state"], "draft", "R5: a draft is found and says so: {v}");
        assert!(p["matched"].as_array().unwrap().len() >= 1 && p["score"].as_f64().unwrap() >= v["threshold"].as_f64().unwrap());
    }
    // the brand word itself
    let (_, v) = s.ask("Bob").await;
    assert_eq!(top3(&v)[0], "10.11.21.1001.01.bob", "{v}");
    // nonsense: a probe with a clarifying question, no pieces
    let (c, v) = s.ask("purple monkey dishwasher").await;
    assert_eq!(c, 200);
    assert!(v.get("pieces").is_none() && v["probe"]["question"].as_str().unwrap().ends_with('?'), "{v}");
    // a hole is never an answer
    let (_, v) = s.ask("what time is it").await;
    assert!(v.get("pieces").is_none(), "holes are never pieces: {v}");
    // non-ASCII is refused (R4)
    let (c, v) = s.ask("what is my n\u{e4}me").await;
    assert_eq!((c, v["rule"].as_str()), (422, Some("R4")), "{v}");
    s.stop().await;
}

#[tokio::test]
async fn ask_link_adds_a_phrasing_through_the_queue() {
    let s = Srv::start(&kernel_dir("asklink")).await;
    session_one(&s).await;
    let (_, v) = s.ask("tell me my name").await;
    let before = top3(&v);
    let q = "10.11.21.0013.01.what-is-my-name";
    // a write: a token is needed
    let (c, _) = Http.req(&s.base, "POST", "/ask/link", Some(json!({"question": q, "phrasing": "tell me my name"}).to_string().into_bytes())).await;
    assert_eq!(c, 401);
    let (c, v) = s.post_as("bob", "/ask/link", json!({"question": q, "phrasing": "tell me my name"})).await;
    assert_eq!(c, 200, "{v}");
    assert!(v["queue_id"].is_string());
    let (_, v) = s.ask("tell me my name").await;
    let p = &v["pieces"][0];
    assert_eq!(p["address"], "10.11.21.1001.01.bob", "before {before:?}: {v}");
    assert_eq!(p["score"], 1.0, "{v}");
    let (c, v) = s.post_as("bob", "/ask/link", json!({"question": q, "phrasing": "tell me my name"})).await;
    assert_eq!(c, 409, "{v}");
    let (c, _) = s.post_as("bob", "/ask/link", json!({"question": "10.11.21.0013.01.nope", "phrasing": "x y"})).await;
    assert_eq!(c, 404);
    let (_, h) = s.get("/history/10.11.21.0013.01").await;
    let ops: Vec<&str> = h.as_array().unwrap().iter().map(|e| e["op"].as_str().unwrap()).collect();
    assert!(ops.ends_with(&["note", "merge"]), "{ops:?}");
    assert_eq!(h.as_array().unwrap().last().unwrap()["by"], "bob");
    s.stop().await;
}

#[tokio::test]
async fn seq_routes() {
    let s = Srv::start(&kernel_dir("seq")).await;
    seed(&s).await;
    let (c, b) = Http.req(&s.base, "GET", "/page.seq?addr=10.11.21.0020", None).await;
    let text = String::from_utf8(b).unwrap();
    assert_eq!(c, 200, "{text}");
    assert!(text.contains("Local reason."), "{text}");
    let (c, b) = Http.req_h(&s.base, "POST", "/check.seq", Some(text.clone().into_bytes()), &[("content-type", "text/x-seqpage")]).await;
    let rep: Value = serde_json::from_slice(&b).unwrap();
    assert_eq!(c, 200, "{rep}");
    assert!(rep["ok"].is_boolean(), "{rep}");
    // propose a .seq: no token -> 401; wrong media -> 415
    let (c, _) = Http.req_h(&s.base, "POST", "/propose", Some(text.clone().into_bytes()), &[("content-type", "text/x-seqpage")]).await;
    assert_eq!(c, 401);
    let (c, _) = Http.req_h(&s.base, "POST", "/check.seq", Some(text.clone().into_bytes()), &[("content-type", "text/plain")]).await;
    assert_eq!(c, 415);
    let edited = text.replace("Local reason.", "Local reason, edited.");
    let auth = format!("Bearer {}", token("alice"));
    let (c, b) = Http.req_h(&s.base, "POST", "/propose", Some(edited.into_bytes()), &[("content-type", "text/x-seqpage"), ("authorization", &auth)]).await;
    let v: Value = serde_json::from_slice(&b).unwrap_or(Value::Null);
    assert!(c == 200 || c == 403 || c == 422, "{c} {v}");
    let (c, _) = Http.req(&s.base, "GET", "/page.seq?addr=10.11.21.9999", None).await;
    assert_eq!(c, 404);
    s.stop().await;
}
