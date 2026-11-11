//! Integration tests over HTTP for every endpoint of docs/CONTRACT.md.
mod common;
use common::*;
use serde_json::{json, Value};

#[tokio::test]
async fn health_books_book() {
    let s = Srv::start(&kernel_dir("hb")).await;
    let (c, h) = s.get("/health").await;
    assert_eq!((c, h["ok"].clone(), h["books"].clone()), (200, json!(true), json!(1)));
    seed(&s).await;
    let (_, b) = s.get("/books").await;
    let addrs: Vec<&str> = b.as_array().unwrap().iter().map(|x| x["address"].as_str().unwrap()).collect();
    assert_eq!(addrs, ["00.00.00", "10.11.21"]);
    assert_eq!(b[1]["title"], "tools");
    assert_eq!(b[1]["pages"], 3);
    let (c, d) = s.get("/book/10.11.21").await;
    assert_eq!(c, 200);
    assert_eq!(d["pages"][2]["page"], "1523");
    assert_eq!(d["pages"][2]["faces"], json!(["00", "05"]));
    assert_eq!(d["pages"][2]["title"], "timer");
    // new book file was created by the compute in books dir
    assert_eq!(s.lines("10.11.21"), 7);
    s.stop().await;
}

#[tokio::test]
async fn page_inherits_live_faces_book_shelf_desk_kernel() {
    let s = Srv::start(&kernel_dir("pg")).await;
    seed(&s).await;
    let (c, p) = s.get("/page/10.11.21.0020").await;
    assert_eq!(c, 200, "{p}");
    assert_eq!(p["title"], "routing");
    assert_eq!(p["faces"]["04"]["resolved_from"], "local");
    assert_eq!(p["faces"]["04"]["source"], "10.11.21.0020.04");
    assert_eq!(p["faces"]["01"]["resolved_from"], "kernel");
    assert_eq!(p["faces"]["01"]["source"], "00.00.00.0020.01");
    assert_eq!(p["inherited"], json!(["00.00.00.0020.01"]));
    assert!(p["faces"]["04"]["n"].is_number() && p["faces"]["04"]["by"] == "user");
    // counters: board 05.00 derived, counter 05.03 with its tail
    let (_, t) = s.get("/page/10.11.21.1523").await;
    assert_eq!(t["faces"]["05.03"]["tail"], "pack");
    assert_eq!(t["faces"]["05.00"]["body"], "03: pack");
    s.stop().await;
}

#[tokio::test]
async fn face_and_resolve_trace() {
    let s = Srv::start(&kernel_dir("fr")).await;
    seed(&s).await;
    let (c, f) = s.get("/face/10.11.21.0020.01").await;
    assert_eq!(c, 200);
    assert_eq!((f["resolved_from"].as_str(), f["source"].as_str()), (Some("kernel"), Some("00.00.00.0020.01")));
    let (_, f) = s.get("/face/10.11.21.0020.04").await;
    assert_eq!(f["resolved_from"], "local");
    assert!(f["body"].as_str().unwrap().contains("local why"));
    let (_, f) = s.get("/face/10.11.21.0020.04.route").await;
    assert!(f["body"].as_str().unwrap().starts_with("## Route"));
    let (c, tr) = s.get("/resolve/10.11.21.0020.01").await;
    assert_eq!(c, 200);
    let levels: Vec<&str> = tr.as_array().unwrap().iter().map(|x| x["level"].as_str().unwrap()).collect();
    assert_eq!(levels, ["local", "shelf", "desk", "kernel"]);
    assert_eq!(tr[1]["book_exists"], false);
    assert_eq!(tr[3]["found"], true);
    // page address resolves its door face 00
    let (_, tr) = s.get("/resolve/10.11.21.0020").await;
    assert_eq!(tr[0]["checked"], "10.11.21.0020.00");
    assert_eq!(tr[0]["found"], true);
    let (_, f) = s.get("/face/10.11.21.1523.05.03").await;
    assert_eq!(f["tail"], "pack");
    let (c, e) = s.get("/face/not.an.address").await;
    assert_eq!((c, e["error"].as_str(), e["rule"].as_str()), (422, Some("invalid"), Some("A1.3")), "{e}");
    s.stop().await;
}

#[tokio::test]
async fn missing_is_404_axiom_7() {
    let s = Srv::start(&kernel_dir("ms")).await;
    seed(&s).await;
    for path in ["/face/10.11.21.1777.04", "/page/10.11.21.1777", "/book/10.11.99", "/face/10.11.21.0020.04.nokey"] {
        let (c, v) = s.get(path).await;
        assert_eq!((c, v["error"].as_str(), v["axiom"].as_str()), (404, Some("missing"), Some("7")), "{path}: {v}");
    }
    let (_, v) = s.get("/face/10.11.21.1777.04").await;
    assert_eq!(v["resolved_from"], "missing");
    assert_eq!(v["trace"].as_array().unwrap().len(), 4);
    // a tail move on a counter that does not exist
    let (c, v) = s.post("agent-7", json!([tail("10.11.21.1523.05.09", "pack", "open")])).await;
    assert_ne!(c, 200, "{v}");
    assert_eq!(v["status"], "rejected");
    s.stop().await;
}

#[tokio::test]
async fn two_concurrent_claims_exactly_one_wins_409_axiom_1() {
    let s = Srv::start(&kernel_dir("cc")).await;
    seed(&s).await;
    let before = s.lines("10.11.21");
    let a = s.post("agent-7", json!([tail(PK, "pack", "open")]));
    let b = s.post("agent-8", json!([tail(PK, "pack", "open")]));
    let ((ca, va), (cb, vb)) = tokio::join!(a, b);
    let mut codes = [ca, cb];
    codes.sort();
    assert_eq!(codes, [200, 409], "{va} {vb}");
    let loser = if ca == 409 { &va } else { &vb };
    assert_eq!((loser["error"].as_str(), loser["axiom"].as_str()), (Some("conflict"), Some("1")));
    assert_eq!(s.lines("10.11.21"), before + 1, "exactly one entry appended");
    let (_, q) = s.get("/queue").await;
    assert_eq!(q["serialized"], true);
    let st: Vec<&str> = q["proposals"].as_array().unwrap().iter().take(2).map(|x| x["status"].as_str().unwrap()).collect();
    assert!(st.contains(&"approved") && st.contains(&"rejected"));
    s.stop().await;
}

#[tokio::test]
async fn many_concurrent_claims_one_winner() {
    let s = Srv::start(&kernel_dir("cc8")).await;
    seed(&s).await;
    let mut hs = Vec::new();
    for i in 0..8 {
        let base = s.base.clone();
        hs.push(tokio::spawn(async move { Http.req(&base, "POST", "/propose", Some(json!({"by": format!("agent-{i}"), "ops": [tail(PK, "pack", "open")]}).to_string().into_bytes())).await.0 }));
    }
    let mut wins = 0;
    for h in hs {
        match h.await.unwrap() {
            200 => wins += 1,
            409 => {}
            c => panic!("unexpected {c}"),
        }
    }
    assert_eq!(wins, 1);
    s.stop().await;
}

#[tokio::test]
async fn builder_cannot_review_own_return() {
    let s = Srv::start(&kernel_dir("rv")).await;
    seed(&s).await;
    assert_eq!(s.post("agent-7", json!([tail(PK, "pack", "open")])).await.0, 200);
    let ret = json!([{"op": "tail", "addr": PK, "from": "open", "to": "return", "body": "## w01\nresult: done"}]);
    assert_eq!(s.post("agent-7", ret).await.0, 200);
    let (c, v) = s.post("agent-7", json!([tail(PK, "return", "review")])).await;
    assert_ne!(c, 200);
    assert_eq!(v["reasons"][0]["rule"], "S10", "{v}");
    let (c, v) = s.post("reviewer", json!([tail(PK, "return", "review")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, v) = s.post("compute", json!([{"op": "tail", "addr": PK, "from": "review", "outcome": "passed"}])).await;
    assert_eq!(c, 200, "{v}");
    let (_, f) = s.get(&format!("/face/{PK}")).await;
    assert!(f.get("tail").is_none(), "closed counter is bare: {f}");
    assert!(f["body"].as_str().unwrap().contains("result: done"));
    s.stop().await;
}

#[tokio::test]
async fn proposal_is_all_or_nothing() {
    let s = Srv::start(&kernel_dir("aon")).await;
    seed(&s).await;
    let before = s.lines("10.11.21");
    // second op writes reserved face 07: the whole proposal is rejected
    let (c, v) = s.post("user", json!([put("10.11.21.1002.00", "---\ntitle: clock\n---"), put("10.11.21.1002.04", "## Clock\nwhy: time.\n\nClock."), put("10.11.21.1002.07", "x")])).await;
    assert_eq!(c, 422, "{v}");
    assert_eq!(v["status"], "rejected");
    assert_eq!(v["entries"], json!([]));
    assert_eq!(s.lines("10.11.21"), before);
    assert_eq!(s.get("/page/10.11.21.1002").await.0, 404);
    // a page with only its door fails C1.1: nothing written
    let (c, _) = s.post("user", json!([put("10.11.21.1003.00", "---\ntitle: lone\n---")])).await;
    assert_eq!(c, 422);
    assert_eq!(s.lines("10.11.21"), before);
    // the same page with a content face is approved as consecutive entries sharing a proposal id
    let (c, v) = s.post("user", json!([put("10.11.21.1002.00", "---\ntitle: clock\n---"), put("10.11.21.1002.04", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert_eq!(c, 200, "{v}");
    let n: Vec<u64> = v["entries"].as_array().unwrap().iter().map(|x| x.as_u64().unwrap()).collect();
    assert_eq!(n.len(), 2);
    assert_eq!(n[1], n[0] + 1);
    let (_, h) = s.get("/history/10.11.21.1002").await;
    assert_eq!(h.as_array().unwrap().len(), 2);
    assert_eq!(h[0]["proposal"], h[1]["proposal"]);
    s.stop().await;
}

#[tokio::test]
async fn bad_proposals() {
    let s = Srv::start(&kernel_dir("bad")).await;
    let (c, _) = Http.req(&s.base, "POST", "/propose", Some(b"not json".to_vec())).await;
    assert_eq!(c, 400);
    let (c, _) = s.post_raw(json!({"ops": []})).await;
    assert_eq!(c, 400);
    let (c, v) = s.post("user", json!([])).await;
    assert_eq!(c, 422, "{v}");
    // no write before the door (format 4.1: identity page first)
    let (c, v) = s.post("user", json!([put("10.11.21.1002.00", "---\ntitle: clock\n---"), put("10.11.21.1002.04", "## C\nwhy: x.\n\nC.")])).await;
    assert_ne!(c, 200, "{v}");
    assert!(!s.dir.join("10.11.21.book").exists() || s.lines("10.11.21") == 1);
    // only the compute writes snapshots
    let (c, _) = s.post("user", json!([{"op": "snapshot", "addr": "00.00.00.0000.00"}])).await;
    assert_ne!(c, 200);
    s.stop().await;
}

#[tokio::test]
async fn history_lists_every_entry_for_an_address() {
    let s = Srv::start(&kernel_dir("hi")).await;
    seed(&s).await;
    s.post("agent-7", json!([tail(PK, "pack", "open")])).await;
    let (c, h) = s.get(&format!("/history/{PK}")).await;
    assert_eq!(c, 200);
    let ops: Vec<&str> = h.as_array().unwrap().iter().map(|e| e["op"].as_str().unwrap()).collect();
    assert_eq!(ops, ["put", "tail"]);
    assert_eq!(h[1]["by"], "agent-7");
    assert_eq!(h[1]["book"], "10.11.21");
    let (_, h) = s.get("/history/10.11.21").await;
    assert_eq!(h.as_array().unwrap().len(), 7);
    let (_, h) = s.get("/history/10.11.21.9000").await;
    assert_eq!(h, json!([]));
    s.stop().await;
}

#[tokio::test]
async fn links_forward_back_missing_one_way() {
    let s = Srv::start(&kernel_dir("ln")).await;
    seed(&s).await;
    let mk = |p: &str, t: &str, l: &str| json!([put(&format!("10.11.21.{p}.00"), &format!("---\ntitle: {t}\n---")), put(&format!("10.11.21.{p}.08"), l)]);
    assert_eq!(s.post("user", mk("1001", "a", "Links: 10.11.21.1002 and 10.11.21.1003 and 10.11.21.1777.")).await.0, 200);
    assert_eq!(s.post("user", mk("1002", "b", "Back to 10.11.21.1001.")).await.0, 200);
    assert_eq!(s.post("user", mk("1003", "c", "Nothing back.")).await.0, 200);
    let (c, l) = s.get("/links/10.11.21.1001").await;
    assert_eq!(c, 200);
    assert_eq!(l["forward"], json!(["10.11.21.1002", "10.11.21.1003", "10.11.21.1777"]));
    assert_eq!(l["back"], json!(["10.11.21.1002"]));
    assert_eq!(l["missing"], json!(["10.11.21.1777"]));
    assert_eq!(l["missing_axiom"], "7.8");
    assert_eq!(l["one_way"], json!(["10.11.21.1003"]));
    let (_, l) = s.get("/links/10.11.21.1003").await;
    assert_eq!(l["back"], json!(["10.11.21.1001"]));
    s.stop().await;
}

#[tokio::test]
async fn brands_and_cards_on_real_books() {
    let s = Srv::start(&copy_dir(&repo_books(), "real")).await;
    let (c, b) = s.get("/brands?q=Bob").await;
    assert_eq!(c, 200);
    let bob = b.as_array().unwrap().iter().find(|x| x["brand_id"] == "bob.001").expect("bob.001 in the Bob test dictionary");
    assert_eq!(bob["why"], "the user's name");
    assert_eq!(bob["is_default"], true);
    assert_eq!(bob["exact_form"], true);
    assert_eq!(bob["brand"], "10.11.21.1001.01.bob");
    let (_, b) = s.get("/brands?q=bob&book=10.11.21").await;
    assert_eq!(b[0]["exact_form"], false, "forms are case-sensitive (brands.md)");
    // Bob test session 2: "what is my name" has no dictionary word
    for w in ["what", "is", "my", "name"] {
        assert_eq!(s.get(&format!("/brands?q={w}")).await.1, json!([]), "{w}");
    }
    let (_, b) = s.get("/brands?q=").await;
    assert_eq!(b, json!([]));
    let (c, cards) = s.get("/cards?title=bob").await;
    assert_eq!(c, 200);
    let faces: Vec<&str> = cards.as_array().unwrap().iter().map(|x| x["face_no"].as_str().unwrap()).collect();
    assert!(faces.contains(&"01") && faces.contains(&"04"), "{faces:?}");
    let (_, k) = s.get("/books").await;
    assert!(k.as_array().unwrap().iter().any(|b| b["address"] == "00.00.00"));
    s.stop().await;
}

#[tokio::test]
async fn r2_build_stage_approval_gate_on_promote() {
    let s = Srv::start(&kernel_dir("r2")).await;
    seed(&s).await;
    let (c, v) = s.post("user", json!([put("10.11.21.1002.00", "---\ntitle: clock\n---"), put_t("10.11.21.1002.04", "draft", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert_eq!(c, 200, "{v}");
    let promote = |extra: Value| {
        let mut op = json!({"op": "promote", "addr": "10.11.21.1002.04.draft"});
        op.as_object_mut().unwrap().extend(extra.as_object().unwrap().clone());
        json!([op])
    };
    assert_eq!(s.post("agent-7", promote(json!({}))).await.0, 403);
    assert_eq!(s.post("agent-7", promote(json!({"approved_by": "build-stage (R2)"}))).await.0, 403, "R2 needs a trial reference");
    assert_eq!(s.post("agent-7", promote(json!({"approved_by": "director"}))).await.0, 403, "only the Director signs as director");
    let (c, v) = s.post("agent-7", promote(json!({"approved_by": "build-stage (R2)", "trial": "docs/trial/kernel-trial.md#1002"}))).await;
    assert_eq!(c, 200, "{v}");
    let (_, f) = s.get("/face/10.11.21.1002.04").await;
    assert_eq!(f["resolved_from"], "local", "seated now");
    let (_, h) = s.get("/history/10.11.21.1002.04.draft").await;
    let last = h.as_array().unwrap().last().unwrap().clone();
    assert_eq!((last["op"].as_str(), last["approved-by"].as_str()), (Some("promote"), Some("build-stage (R2)")));
    assert_eq!(last["trial"], "docs/trial/kernel-trial.md#1002");
    s.stop().await;
}

#[tokio::test]
async fn unknown_route_is_json_404() {
    let s = Srv::start(&kernel_dir("rt")).await;
    let (c, v) = s.get("/nope").await;
    assert_eq!((c, v["error"].as_str()), (404, Some("route")));
    s.stop().await;
}
