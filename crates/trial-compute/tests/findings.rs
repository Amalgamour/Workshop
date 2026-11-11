//! TRIAL-X findings on crates/compute. Each test states what the spec (or a
//! Director ruling) requires and FAILS today. Run: cargo test -p trial-compute -- --ignored
//! Numbers match docs/trial/compute-trial.md.
use serde_json::{json, Value};
use trial_compute::*;

async fn draft_page(s: &Srv, pg: &str, by: &str) {
    let (c, v) = s.post(by, json!([put_t(&format!("10.11.21.{pg}.00"), "draft", "---\ntitle: clock\n---"), put_t(&format!("10.11.21.{pg}.04"), "draft", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert_eq!(c, 200, "{v}");
}
fn promote(addr: &str, extra: Value) -> Value {
    let mut op = json!({"op": "promote", "addr": addr});
    op.as_object_mut().unwrap().extend(extra.as_object().unwrap().clone());
    json!([op])
}

/// Finding 1 (blocker): any HTTP client can sign as the Director. `by` is
/// self-declared, so `by: "user"` + `approved_by: "director"` seats a face.
#[tokio::test]
#[ignore = "finding 1"]
async fn f01_director_approval_is_forgeable() {
    let s = Srv::start(&kernel_dir("f01")).await;
    seed(&s).await;
    draft_page(&s, "1002", "agent-7").await;
    let before = s.book("10.11.21");
    // an agent (not the Director) simply types the Director's name
    let (c, v) = s.post("user", promote("10.11.21.1002.04.draft", json!({"approved_by": "director"}))).await;
    assert_ne!(c, 200, "Director approval was accepted from an unauthenticated client: {v}");
    assert_eq!(s.book("10.11.21"), before);
    s.stop().await;
}

/// Finding 2 (major): the compute's approval gate (store.rs:664-686) looks
/// only at `promote`. A bare `put` that seats a brand-new face is never gated
/// by the compute: with the committed core it needs no approval at all; with
/// the CORE fix pass's gate it needs only the words `approved_by: director`,
/// which the core accepts from any author. Either way an agent seats a face.
#[tokio::test]
#[ignore = "finding 2"]
async fn f02_seating_put_skips_compute_gate() {
    let s = Srv::start(&kernel_dir("f02")).await;
    seed(&s).await;
    let door = |pg: &str| put_t(&format!("10.11.21.{pg}.00"), "draft", "---\ntitle: clock\n---");
    let (c1, v1) = s.post("agent-7", json!([door("1002"), put_plain("10.11.21.1002.04", "## Clock\nwhy: time.\n\nClock.")])).await;
    let (c2, v2) = s.post("agent-7", json!([door("1003"), put("10.11.21.1003.04", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert!(c1 != 200 && c2 != 200, "agent seated a face by put: no approval -> {c1} {}; self-typed director -> {c2} {}", v1["status"], v2["status"]);
    s.stop().await;
}

/// Finding 3 (major): `access-control-allow-origin: *` on every answer and
/// /propose ignores content-type, so any web page open in the Director's
/// browser can POST a `text/plain` "simple request" (no CORS preflight) and write.
#[tokio::test]
#[ignore = "finding 3"]
async fn f03_cross_site_simple_post_writes() {
    let s = Srv::start(&kernel_dir("f03")).await;
    seed(&s).await;
    let before = s.book("10.11.21");
    let body = json!({"by": "user", "ops": page("10.11.21", "1300", "evil")}).to_string();
    let r = req(&s.host, "POST", "/propose", &[("content-type", "text/plain"), ("origin", "http://evil.example")], body.as_bytes()).await;
    assert_ne!(r.code, 200, "cross-origin text/plain POST was approved (acao={:?})", r.header("access-control-allow-origin"));
    assert_eq!(s.book("10.11.21"), before);
    s.stop().await;
}

/// Finding 4 (major): any client may write as `compute` and so gets the
/// compute-only powers (C8.7 `use` records, meters, `abandoned`).
#[tokio::test]
#[ignore = "finding 4"]
async fn f04_clients_can_impersonate_the_compute() {
    let s = Srv::start(&kernel_dir("f04")).await;
    seed(&s).await;
    let before = s.book("10.11.21");
    let (c, v) = s.post("compute", json!([{"op": "use", "addr": "10.11.21.0012.03", "body": "word: bob\nbrand: bob.001\noutcome: hit"}])).await;
    assert_ne!(c, 200, "an HTTP client wrote a compute-only `use` record: {v}");
    assert_eq!(s.book("10.11.21"), before);
    s.stop().await;
}

/// Finding 5 (major): R2 needs a hostile trial "from a different view than its
/// maker". The gate takes any non-empty string as `trial`, including the
/// maker's own name and references to nothing.
#[tokio::test]
#[ignore = "finding 5"]
async fn f05_r2_trial_reference_is_not_checked() {
    let s = Srv::start(&kernel_dir("f05")).await;
    seed(&s).await;
    draft_page(&s, "1002", "agent-7").await;
    draft_page(&s, "1003", "agent-7").await;
    let (c1, v1) = s.post("agent-7", promote("10.11.21.1002.04.draft", json!({"approved_by": "build-stage (R2)", "trial": "agent-7"}))).await;
    let (c2, v2) = s.post("agent-7", promote("10.11.21.1003.04.draft", json!({"approved_by": "build-stage (R2)", "trial": "docs/trial/does-not-exist.md#nothing"}))).await;
    assert!(c1 != 200 && c2 != 200, "maker==trial -> {c1} {v1}; fake trial ref -> {c2} {v2}");
    s.stop().await;
}

/// Finding 6 (major): S10 "builder cannot review its own return" compares raw
/// strings, so the builder passes by adding a space (or changing case).
#[tokio::test]
#[ignore = "finding 6"]
async fn f06_self_review_by_alias() {
    let s = Srv::start(&kernel_dir("f06")).await;
    seed(&s).await;
    assert_eq!(s.post("agent-7", json!([tail(PK, "pack", "open")])).await.0, 200);
    assert_eq!(s.post("agent-7", json!([{"op": "tail", "addr": PK, "from": "open", "to": "return", "body": "## w01\nresult: done"}])).await.0, 200);
    let (c, v) = s.post("agent-7 ", json!([tail(PK, "return", "review")])).await;
    assert_ne!(c, 200, "builder reviewed its own return as `agent-7 `: {v}");
    s.stop().await;
}

/// Finding 7 (major): ruling R5 "Draft faces count and lookups find them" is
/// not applied on /page: the compute's own filter (store.rs:341 `!it.live`)
/// drops an inherited draft, while /face (core resolver, CORE fix pass) now
/// finds it. Every real kernel face is a draft, so /page of a book inherits nothing
/// and the two endpoints disagree about the same face.
#[tokio::test]
#[ignore = "finding 7"]
async fn f07_r5_inherited_drafts_not_found() {
    let d = kernel_dir("f07");
    let mut k = KERNEL.to_string();
    k.push_str(r###"{"n":6,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.02","tail":"draft","body":"## Shape\nkernel draft schema."}"###);
    k.push('\n');
    std::fs::write(d.join("00.00.00.book"), k).unwrap();
    let s = Srv::start(&d).await;
    seed(&s).await;
    let (c, f) = s.get("/face/10.11.21.0020.02").await;
    let (_, p) = s.get("/page/10.11.21.0020").await;
    let in_page = p["faces"].as_object().map(|m| m.keys().any(|k| k.starts_with("02"))).unwrap_or(false);
    assert!(in_page, "R5: /face -> {c} tail {}; /page faces {:?}", f["tail"], p["faces"].as_object().map(|m| m.keys().cloned().collect::<Vec<_>>()));
    s.stop().await;
}

/// Finding 8 (minor): `elevate` is answered HTTP 300 Multiple Choices, a
/// redirect class with no Location; the contract defines no 300.
#[tokio::test]
#[ignore = "finding 8"]
async fn f08_elevate_is_http_300() {
    let s = Srv::start(&kernel_dir("f09")).await;
    seed(&s).await;
    let (c, v) = s.get("/page/10.11.21.1523.wrong").await;
    assert_eq!(v["error"], "elevate");
    assert!(!(300..400).contains(&c), "elevate came back as redirect-class {c}");
    s.stop().await;
}

/// Finding 9 (minor): the same mistake (a malformed address) gets 400 on
/// /book but 422 on /page, /face, /links, /resolve.
#[tokio::test]
#[ignore = "finding 9"]
async fn f09_bad_address_codes_disagree() {
    let s = Srv::start(&kernel_dir("f10")).await;
    let mut codes = vec![];
    for p in ["/book/zz", "/page/zz", "/face/zz", "/links/zz", "/resolve/zz"] {
        codes.push(s.get(p).await.0);
    }
    codes.dedup();
    assert_eq!(codes.len(), 1, "one malformed address, several codes: {codes:?}");
    s.stop().await;
}

/// Finding 10 (minor): /history never parses its address: garbage is 200 [],
/// and the titled form of a real page (`PPPP.title`) finds nothing although
/// the core's own history ignores titles (log.rs `history_key`).
#[tokio::test]
#[ignore = "finding 10"]
async fn f10_history_unvalidated_and_title_blind() {
    let s = Srv::start(&kernel_dir("f11")).await;
    seed(&s).await;
    let (cg, _) = s.get("/history/..%2F..%2Fetc").await;
    let (_, plain) = s.get("/history/10.11.21.1523").await;
    let (_, titled) = s.get("/history/10.11.21.1523.timer").await;
    assert!(cg != 200 && plain == titled, "garbage -> {cg}; titled history {} vs plain {}", titled.as_array().map(|a| a.len()).unwrap_or(0), plain.as_array().map(|a| a.len()).unwrap_or(0));
    s.stop().await;
}

/// Finding 11 (minor): /queue ids restart at q1 after a restart and the queue
/// is not kept, so a `queue_id` handed to a writer is ambiguous and lost.
#[tokio::test]
#[ignore = "finding 11"]
async fn f11_queue_ids_reused_after_restart() {
    let d = kernel_dir("f13");
    let s = Srv::start(&d).await;
    seed(&s).await;
    let (_, v1) = s.post("user", page("10.11.21", "1002", "a")).await;
    s.stop().await;
    let s = Srv::start(&d).await;
    let (_, v2) = s.post("user", page("10.11.21", "1003", "b")).await;
    let (_, q) = s.get("/queue").await;
    assert!(v1["queue_id"] != v2["queue_id"] && q["proposals"].as_array().unwrap().len() > 1, "queue ids {} then {} after restart; queue {}", v1["queue_id"], v2["queue_id"], q);
    s.stop().await;
}

/// Finding 12 (minor): a retired face 08 still counts as a link, forward and
/// back. Retired is "awaiting removal", not a lawful written connection.
#[tokio::test]
#[ignore = "finding 12"]
async fn f12_retired_links_still_count() {
    let s = Srv::start(&kernel_dir("f14")).await;
    seed(&s).await;
    let (c, v) = s.post("user", json!([put("10.11.21.1200.00", "---\ntitle: l\n---"), put("10.11.21.1200.08", "links 10.11.21.1523")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, v) = s.post("user", json!([{"op": "tail", "addr": "10.11.21.1200.08", "from": "", "to": "retired"}])).await;
    assert_eq!(c, 200, "{v}");
    let (_, fwd) = s.get("/links/10.11.21.1200").await;
    let (_, back) = s.get("/links/10.11.21.1523").await;
    assert!(fwd["forward"] == json!([]) && back["back"] == json!([]), "retired 08 still links: forward {} back {}", fwd["forward"], back["back"]);
    s.stop().await;
}

/// Finding 13 (minor): /brands without `book=` reads every book's dictionary,
/// so a word defined only in desk 20 answers a reader on desk 10.
#[tokio::test]
#[ignore = "finding 13"]
async fn f13_brands_cross_desk_leak() {
    let s = Srv::start(&kernel_dir("f15")).await;
    seed(&s).await;
    door(&s, "20.11.21", "other").await;
    let (c, v) = s.post("user", json!([put("20.11.21.0012.00", "---\ntitle: dictionary\n---"), put("20.11.21.0012.03.14", "## secret\ntype: index\ndefault: secret.001\nsecret.001: 20.11.21.1001.01.secret")])).await;
    assert_eq!(c, 200, "{v}");
    let (_, b) = s.get("/brands?q=secret").await;
    assert_eq!(b, json!([]), "desk-20 word answered with no book context");
    s.stop().await;
}

/// Finding 15 (minor): every approved write re-reads and re-parses the whole
/// book file (store.rs:725 -> log::file::append -> repair_tail + fs::read), and
/// the writer holds the store's write lock meanwhile, so a small write and every
/// read wait on the book's size: cost per write grows with the book (O(n^2) over
/// a book's life). format.md 3.4 expects a long log and plans snapshots for
/// replay, not for every write.
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
#[ignore = "finding 15"]
async fn f15_write_cost_grows_with_book_size() {
    let s = Srv::start(&kernel_dir("f15")).await;
    seed(&s).await;
    let t = |s: &Srv, pg: String| {
        let host = s.host.clone();
        async move {
            let t0 = std::time::Instant::now();
            let r = req(&host, "POST", "/propose", &[("content-type", "application/json")], json!({"by": "user", "ops": page("10.11.21", &pg, "t")}).to_string().as_bytes()).await;
            assert_eq!(r.code, 200);
            t0.elapsed()
        }
    };
    let small = t(&s, "1001".into()).await;
    let big = "y".repeat(1_900_000);
    for i in 0..20 {
        let (c, _) = s.post("user", json!([put(&format!("10.11.21.12{i:02}.00"), "---\ntitle: b\n---"), put(&format!("10.11.21.12{i:02}.04"), &format!("## B\nwhy: b.\n\n{big}"))])).await;
        assert_eq!(c, 200);
    }
    let large = t(&s, "1002".into()).await;
    eprintln!("small-book write {small:?}, 38 MB book write {large:?}");
    assert!(large < small * 20 + std::time::Duration::from_millis(50), "one tiny write: {small:?} on a small book, {large:?} on a 38 MB book");
    s.stop().await;
}

/// Finding 16 (minor): ruling R9 "Faces do not have sentinels" (no `FF.00`,
/// no `FF.99`), but the compute itself derives and serves a board at `FF.00`
/// (store.rs:149-150 `face_items`, store.rs:427 `Found::Board`): /page lists
/// `05.00` and /face answers `...05.00` with 200.
#[tokio::test]
#[ignore = "finding 16"]
async fn f16_r9_compute_serves_face_sentinel_00() {
    let s = Srv::start(&kernel_dir("f16")).await;
    seed(&s).await;
    let (_, p) = s.get("/page/10.11.21.1523").await;
    let keys: Vec<String> = p["faces"].as_object().unwrap().keys().cloned().collect();
    let (c, f) = s.get("/face/10.11.21.1523.05.00").await;
    assert!(!keys.iter().any(|k| k == "05.00") && c != 200, "R9: /page keys {keys:?}; /face 05.00 -> {c} {}", f["body"]);
    s.stop().await;
}
