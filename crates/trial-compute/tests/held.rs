//! TRIAL-X: what held up. Each test is an attack the compute survived.
use serde_json::{json, Value};
use std::collections::BTreeSet;
use trial_compute::*;

fn check_log(text: &str) -> usize {
    let mut n = 0u64;
    for (i, l) in text.lines().enumerate() {
        let v: Value = serde_json::from_str(l).unwrap_or_else(|e| panic!("line {} not JSON: {e}", i + 1));
        if i > 0 {
            n += 1;
            assert_eq!(v["n"].as_u64(), Some(n), "n out of order at line {}", i + 1);
        }
    }
    assert!(text.is_empty() || text.ends_with('\n'));
    n as usize
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn held_concurrent_mixed_storm_is_serialized() {
    let d = kernel_dir("storm");
    let s = Srv::start(&d).await;
    seed(&s).await;
    let mut hs = Vec::new();
    for i in 0..48u32 {
        let host = s.host.clone();
        hs.push(tokio::spawn(async move {
            let (kind, body) = match i % 3 {
                0 => ("claim", json!({"by": format!("agent-{i}"), "ops": [tail(PK, "pack", "open")]})),
                1 => ("same", json!({"by": "user", "ops": page("10.11.21", "1600", "same")})),
                _ => ("own", json!({"by": "user", "ops": page("10.11.21", &format!("17{i:02}"), "own")})),
            };
            let r = req(&host, "POST", "/propose", &[("content-type", "application/json")], body.to_string().as_bytes()).await;
            (kind, r.code)
        }));
    }
    let mut wins = std::collections::BTreeMap::new();
    for h in hs {
        let (k, c) = h.await.unwrap();
        assert!([200, 409, 422].contains(&c), "{k}: unexpected {c}");
        if c == 200 {
            *wins.entry(k).or_insert(0) += 1;
        }
    }
    assert_eq!(wins.get("claim"), Some(&1), "exactly one claim wins");
    assert_eq!(wins.get("same"), Some(&1), "exactly one creator of 1600 wins");
    assert_eq!(wins.get("own"), Some(&16), "every independent write lands");
    let seeded = check_log(&s.book("10.11.21")) - (1 + 2 + 32);
    assert!(seeded == 3 || seeded == 4, "seed + claim 1 + same 2 + own 32 entries, nothing else (seed {seeded})");
    let (_, b1) = s.get("/book/10.11.21").await;
    s.stop().await;
    let s = Srv::start(&d).await;
    assert_eq!(s.get("/book/10.11.21").await.1, b1, "restart replays to the same book");
    s.stop().await;
}

/// R4 (Director ruling): non-ASCII, tab, CR, control bytes are refused with a
/// 4xx and the book is left byte for byte unchanged. (Against committed core
/// 2069da1 these were accepted or answered 500; holds with the CORE fix pass's
/// working tree, which checks R4 during validation.)
#[tokio::test]
async fn held_r4_refusals_are_4xx_and_leave_the_book_unchanged() {
    let s = Srv::start(&kernel_dir("r4")).await;
    seed(&s).await;
    let before = s.book("10.11.21");
    let bads = ["caf\u{e9}", "a\tb", "a\r\nb", "a\rb", "a\u{0}b", "\u{1b}[31m", "\u{7f}", "\u{1F600}", "\u{2028}", "\u{feff}"];
    for (i, bad) in bads.iter().enumerate() {
        let pg = format!("11{i:02}");
        let (c, v) = s.post("user", json!([put(&format!("10.11.21.{pg}.00"), "---\ntitle: x\n---"), put(&format!("10.11.21.{pg}.04"), &format!("## X\nwhy: {bad}.\n\nX."))])).await;
        assert!((400..500).contains(&c) && v["status"] == "rejected", "body {bad:?}: {c} {v}");
        let (c, _) = s.post(&format!("agent{bad}"), page("10.11.21", &pg, "x")).await;
        assert!((400..500).contains(&c), "by {bad:?}: {c}");
        let (c, _) = s.post("user", json!([put(&format!("10.11.21.{pg}.00"), &format!("---\ntitle: x{bad}\n---")), put(&format!("10.11.21.{pg}.04"), "## X\nwhy: x.\n\nX.")])).await;
        assert!((400..500).contains(&c), "title {bad:?}: {c}");
        let (c, _) = s.post("user", json!([put_t(PK, &format!("pack{bad}"), "x")])).await;
        assert!((400..500).contains(&c), "tail {bad:?}: {c}");
        assert_eq!(s.book("10.11.21"), before, "book changed after {bad:?}");
    }
    let n0 = before.lines().count() as u64; // header + entries: next n is n0
    let (c, v) = s.post("user", page("10.11.21", "1198", "plain")).await;
    assert_eq!(c, 200, "{v}");
    assert_eq!(v["entries"], json!([n0, n0 + 1]), "numbering stays contiguous after refusals");
    let (_, q) = s.get("/queue").await;
    // (fix pass: a bad `by` is now a bad token, refused 401 at the door before the queue: 30 queued refusals, not 40)
    assert!(q["proposals"].as_array().unwrap().iter().skip(1).take(30).all(|p| p["status"] == "rejected"));
    s.stop().await;
}

#[test]
fn held_r4_damaged_books_reported_on_read_and_never_rewritten() {
    let d = tmp("r4k");
    let k = KERNEL.replace("The kernel.", "The k\u{e9}rnel.");
    std::fs::write(d.join("00.00.00.book"), &k).unwrap();
    let e = compute::Store::boot(compute::Config::for_dirs(vec![d.clone()])).err().expect("kernel with non-ASCII refused");
    assert!(e.detail.contains("ASCII"), "{e}");
    assert_eq!(std::fs::read_to_string(d.join("00.00.00.book")).unwrap(), k, "nothing rewritten");
    let d = kernel_dir("r4b");
    let bad = "{\"seqbook\":1,\"address\":\"10.11.21\"}\n{\"n\":1,\"at\":\"2026-11-11T19:30:00Z\",\"by\":\"user\",\"op\":\"put\",\"addr\":\"10.11.21.0000.00\",\"body\":\"a\tb\"}\n";
    std::fs::write(d.join("10.11.21.book"), bad).unwrap();
    let st = compute::Store::boot(compute::Config::for_dirs(vec![d.clone()])).expect("kernel ok");
    assert_eq!(st.refused.len(), 1, "{:?}", st.refused);
    assert!(st.refused[0]["detail"].as_str().unwrap().contains("ASCII"));
    assert_eq!(read(&d, "10.11.21"), bad);
}

#[tokio::test]
async fn held_damaged_book_is_not_overwritten_by_a_write() {
    let d = kernel_dir("dmgw");
    let bad = "{\"seqbook\":1,\"address\":\"10.11.21\"}\n{not json\n{\"n\":2}\n";
    std::fs::write(d.join("10.11.21.book"), bad).unwrap();
    let s = Srv::start(&d).await;
    let (_, h) = s.get("/health").await;
    assert_eq!(h["refused"].as_array().unwrap().len(), 1);
    let (c, _) = s.post("user", json!([put("10.11.21.0000.00", "---\ntitle: tools\n---")])).await;
    assert_ne!(c, 200);
    let (c, _) = s.post("user", page("10.11.21", "0000", "tools")).await;
    assert_ne!(c, 200);
    assert_eq!(s.book("10.11.21"), bad, "a refused book is never rewritten");
    s.stop().await;
}

#[tokio::test]
async fn held_malformed_and_huge_bodies() {
    let s = Srv::start(&kernel_dir("body")).await;
    seed(&s).await;
    let before = s.book("10.11.21");
    let big = "a".repeat(3_000_000);
    let (c, _) = s.post("user", json!([put("10.11.21.1400.00", "---\ntitle: big\n---"), put("10.11.21.1400.04", &format!("## B\nwhy: b.\n\n{big}"))])).await;
    assert_eq!(c, 413, "over the body limit");
    let deep = b"[".repeat(200_000);
    let cases: Vec<&[u8]> = vec![&deep, b"\xff\xfe{", b"", b"null", b"[]", br#"{"by":"user","ops":{}}"#, br#"{"by":7,"ops":[]}"#, br#"{"by":"user","ops":[{"op":"explode","addr":"10.11.21.1400.04"}]}"#, br#"{"by":"user","ops":[{"op":"put"}]}"#];
    for b in cases {
        let (c, v) = s.post_bytes(b).await;
        assert!((400..500).contains(&c), "{:?} -> {c} {v}", String::from_utf8_lossy(&b[..b.len().min(30)]));
    }
    assert_eq!(req(&s.host, "GET", "/propose", &[], b"").await.code, 405);
    // (fix pass: a write now carries its media type and a token; the point here is the short length)
    let r = raw(&s.host, format!("POST /propose HTTP/1.1\r\nhost: x\r\ncontent-type: application/json\r\nauthorization: Bearer {}\r\ncontent-length: 5\r\nconnection: close\r\n\r\n{{\"by\":\"user\",\"ops\":[]}}", token("user")).as_bytes()).await;
    assert_eq!(r.code, 400, "short content-length is cut, not over-read");
    let r = raw(&s.host, b"\x00\x01GARBAGE\r\n\r\n").await;
    assert!(r.code == 400 || r.code == 0);
    assert_eq!(s.book("10.11.21"), before);
    assert_eq!(s.get("/health").await.0, 200, "still serving");
    s.stop().await;
}

#[tokio::test]
async fn held_path_traversal_in_addr_and_book_params() {
    let root = tmp("trav");
    let d = root.join("books");
    std::fs::create_dir_all(&d).unwrap();
    std::fs::write(d.join("00.00.00.book"), KERNEL).unwrap();
    std::fs::write(root.join("secret.book"), "TOPSECRET\n").unwrap();
    let s = Srv::start(&d).await;
    seed(&s).await;
    for p in ["/face/..%2F..%2Fetc%2Fpasswd", "/face/../secret", "/book/..%2Fsecret", "/book/../secret", "/page/10.11.21.1523%00", "/page/10.11.21.1523%2F..%2F..", "/links/..%2F..", "/resolve/%2Fetc%2Fpasswd", "/brands?q=bob&book=../secret", "/brands?q=bob&book=%2Fetc", "/face/10.11.21.1523.00%0A", "/face/10.11.21.1523.00.%2E%2E"] {
        let r = req(&s.host, "GET", p, &[], b"").await;
        assert_ne!(r.code, 200, "{p}");
        assert!(!String::from_utf8_lossy(&r.body).contains("TOPSECRET"), "{p}");
    }
    for a in ["../../secret.04", "..%2F..%2Fsecret.04", "10.11.21.1002.04/../../../secret", "/tmp/x.book", "10.11.21/../../x.0000.00", "10.11.21.1002.04\u{0}"] {
        let (c, v) = s.post("user", json!([put(a, "x")])).await;
        assert!((400..500).contains(&c), "{a}: {c} {v}");
    }
    let mut files: Vec<String> = std::fs::read_dir(&root).unwrap().map(|e| e.unwrap().file_name().to_string_lossy().to_string()).collect();
    files.sort();
    assert_eq!(files, ["books", "secret.book"], "nothing written outside books/");
    // (fix pass: the compute's own dotfiles .identities and .queue live beside the books)
    assert_eq!(listing(&d), ["00.00.00.book", "10.11.21.book"]);
    s.stop().await;
}

#[tokio::test]
async fn held_r2_gate_basics_and_record_survives_restart() {
    let d = kernel_dir("r2");
    let s = Srv::start(&d).await;
    seed(&s).await;
    let (c, v) = s.post("agent-7", json!([put_t("10.11.21.1002.00", "draft", "---\ntitle: clock\n---"), put_t("10.11.21.1002.04", "draft", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert_eq!(c, 200, "{v}");
    let pr = |x: Value| {
        let mut op = json!({"op": "promote", "addr": "10.11.21.1002.04.draft"});
        op.as_object_mut().unwrap().extend(x.as_object().unwrap().clone());
        json!([op])
    };
    for bad in [json!({}), json!({"approved_by": "Director"}), json!({"approved_by": "build-stage (R2)"}), json!({"approved_by": "build-stage (R2)", "trial": "   "}), json!({"approved_by": "director"})] {
        let (c, v) = s.post("agent-7", pr(bad.clone())).await;
        assert_eq!(c, 403, "{bad} -> {v}");
    }
    assert_eq!(s.post("agent-7", pr(json!({"approved_by": 1}))).await.0, 400);
    let (c, v) = s.post("agent-9", pr(json!({"approved_by": "build-stage (R2)", "trial": "docs/trial/compute-trial.md"}))).await;
    assert_eq!(c, 200, "{v}");
    let (_, h1) = s.get("/history/10.11.21.1002.04").await;
    s.stop().await;
    let s = Srv::start(&d).await;
    let (_, h2) = s.get("/history/10.11.21.1002.04").await;
    assert_eq!(h1, h2);
    let last = h2.as_array().unwrap().last().unwrap();
    assert_eq!((last["approved-by"].as_str(), last["trial"].as_str()), (Some("build-stage (R2)"), Some("docs/trial/compute-trial.md")));
    s.stop().await;
}

#[tokio::test]
async fn held_builder_exact_name_cannot_review_own_return() {
    let s = Srv::start(&kernel_dir("s10")).await;
    seed(&s).await;
    assert_eq!(s.post("agent-7", json!([tail(PK, "pack", "open")])).await.0, 200);
    let (c, _) = s.post("agent-8", json!([{"op": "tail", "addr": PK, "from": "open", "to": "return", "body": "## w01\nresult: stolen"}])).await;
    assert_eq!(c, 409, "a stranger cannot return someone else's claim");
    assert_eq!(s.post("agent-7", json!([{"op": "tail", "addr": PK, "from": "open", "to": "return", "body": "## w01\nresult: done"}])).await.0, 200);
    let (c, v) = s.post("agent-7", json!([tail(PK, "return", "review")])).await;
    assert_ne!(c, 200, "{v}");
    let (c, _) = s.post("agent-9", json!([tail(PK, "pack", "open")])).await;
    assert_ne!(c, 200, "a replayed claim is refused once the counter moved on");
    s.stop().await;
}

async fn face01(s: &Srv, b: &str, who: &str) {
    let (c, v) = s.post("user", json!([put(&format!("{b}.0020.00"), "---\ntitle: routing\n---"), put(&format!("{b}.0020.01"), &format!("## Route\n{who} route.")), put(&format!("{b}.0020.04"), &format!("## Route\nwhy: {who} why.\n\n{who}."))])).await;
    assert_eq!(c, 200, "{b}: {v}");
}

#[tokio::test]
async fn held_resolution_order_book_shelf_desk_kernel() {
    let s = Srv::start(&kernel_dir("ord")).await;
    for (b, t) in [("10.00.00", "desk"), ("10.11.00", "shelf"), ("10.11.21", "book"), ("10.12.21", "book2"), ("20.11.21", "book3")] {
        door(&s, b, t).await;
    }
    face01(&s, "10.00.00", "desk").await;
    face01(&s, "10.11.00", "shelf").await;
    for (b, lvl, src) in [("10.11.21", "shelf", "10.11.00.0020.01"), ("10.12.21", "desk", "10.00.00.0020.01"), ("20.11.21", "kernel", "00.00.00.0020.01")] {
        let (c, f) = s.get(&format!("/face/{b}.0020.01")).await;
        assert_eq!((c, f["resolved_from"].as_str(), f["source"].as_str()), (200, Some(lvl), Some(src)), "{b}: {f}");
        let (_, tr) = s.get(&format!("/resolve/{b}.0020.01")).await;
        let lv: Vec<&str> = tr.as_array().unwrap().iter().map(|x| x["level"].as_str().unwrap()).collect();
        let full = ["local", "shelf", "desk", "kernel"];
        let k = full.iter().position(|x| *x == lvl).unwrap();
        assert_eq!(lv, full[..=k].to_vec(), "trace walks in order and stops where found");
    }
    face01(&s, "10.11.21", "book").await;
    let (_, f) = s.get("/face/10.11.21.0020.01").await;
    assert_eq!(f["resolved_from"], "local");
    let (_, p) = s.get("/page/10.12.21.0020").await;
    assert_eq!(p["faces"]["01"]["source"], "10.00.00.0020.01");
    s.stop().await;
}

/// R5 on /face: a draft is readable at its own `FF.draft` address and through
/// lookup, and still shows as a draft. (Failed against committed core 2069da1;
/// holds with the CORE fix pass's working tree.)
#[tokio::test]
async fn held_r5_face_finds_drafts_and_marks_them() {
    let s = Srv::start(&kernel_dir("r5")).await;
    seed(&s).await;
    let (c, v) = s.post("agent-7", json!([put_t("10.11.21.1002.00", "draft", "---\ntitle: clock\n---"), put_t("10.11.21.1002.04", "draft", "## Clock\nwhy: time.\n\nClock.")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, f) = s.get("/face/10.11.21.1002.04.draft").await;
    assert_eq!((c, f["tail"].as_str()), (200, Some("draft")), "{f}");
    let (c, f) = s.get("/face/10.11.21.1002.04").await;
    assert_eq!((c, f["tail"].as_str()), (200, Some("draft")), "{f}");
    s.stop().await;
}

#[tokio::test]
async fn held_links_one_way_missing_and_cross_book() {
    let s = Srv::start(&kernel_dir("lnk")).await;
    seed(&s).await;
    door(&s, "20.11.21", "other").await;
    let mk = |b: &str, p: &str, l: &str| json!([put(&format!("{b}.{p}.00"), "---\ntitle: l\n---"), put(&format!("{b}.{p}.08"), l)]);
    assert_eq!(s.post("user", mk("10.11.21", "1001", "to 20.11.21.1001 and 10.11.21.1999 and me 10.11.21.1001 and 10.11.21.10011 and x10.11.21.1523")).await.0, 200);
    assert_eq!(s.post("user", mk("20.11.21", "1001", "nothing")).await.0, 200);
    let (_, l) = s.get("/links/10.11.21.1001").await;
    assert_eq!(l["forward"], json!(["20.11.21.1001", "10.11.21.1999"]), "self link and digit-run/word-glued forms ignored");
    assert_eq!(l["missing"], json!(["10.11.21.1999"]));
    assert_eq!(l["one_way"], json!(["20.11.21.1001"]));
    let (_, b) = s.get("/links/20.11.21.1001").await;
    assert_eq!(b["back"], json!(["10.11.21.1001"]));
    s.stop().await;
}

#[tokio::test]
async fn held_brand_and_card_lookup_edges() {
    let s = Srv::start(&kernel_dir("brand")).await;
    seed(&s).await;
    let (c, v) = s.post("user", json!([put("10.11.21.0012.00", "---\ntitle: dictionary\n---"), put("10.11.21.0012.03.14", "## bob\ntype: index\ndefault: bob.001\nbob.001: 10.11.21.1001.01.bob\nbob.002: 10.11.21.1001.01.robert")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, v) = s.post("user", json!([put("10.11.21.1001.00", "---\ntitle: people\n---"), put("10.11.21.1001.01", "## Bob\nforms: Bob\nmeans: the user's name\n\nBob."), put("10.11.21.1001.04", "## Bob\nwhy: the Bob test.\n\nName.")])).await;
    assert_eq!(c, 200, "{v}");
    let (_, b) = s.get("/brands?q=BOB").await;
    let ids: BTreeSet<&str> = b.as_array().unwrap().iter().map(|x| x["brand_id"].as_str().unwrap()).collect();
    assert_eq!(ids, ["bob.001", "bob.002"].into_iter().collect());
    let b1 = b.as_array().unwrap().iter().find(|x| x["brand_id"] == "bob.001").unwrap();
    assert_eq!((b1["is_default"].as_bool(), b1["exact_form"].as_bool(), b1["why"].as_str()), (Some(true), Some(false), Some("the user's name")));
    let b2 = b.as_array().unwrap().iter().find(|x| x["brand_id"] == "bob.002").unwrap();
    assert_eq!(b2["missing"], true, "a brand line to a card that is not there is marked missing, not guessed");
    let long = "b".repeat(10_000);
    for q in ["", "%20%20%20", "!!!", "%C3%A9", "bob.001", long.as_str(), "10.11.21.1001.01.bob"] {
        let (c, v) = s.get(&format!("/brands?q={q}")).await;
        assert_eq!((c, v.clone()), (200, json!([])), "{q:.20}");
    }
    assert_eq!(s.get("/brands?q=bob&book=zz").await.0, 400, "fix pass #9: a malformed address is 400 everywhere");
    assert_eq!(s.get("/brands?q=bob&book=20.11.21").await.1, json!([]), "book= limits to that lookup chain");
    let (_, cards) = s.get("/cards?title=Bob").await;
    let faces: BTreeSet<&str> = cards.as_array().unwrap().iter().map(|x| x["face_no"].as_str().unwrap()).collect();
    assert!(faces.contains("01") && faces.contains("04") && !faces.contains("00"), "{faces:?}");
    for t in ["", "!!!", "%C3%A9"] {
        assert_eq!(s.get(&format!("/cards?title={t}")).await, (200, json!([])));
    }
    s.stop().await;
}

#[tokio::test]
async fn held_restart_consistency_after_mixed_traffic() {
    let d = kernel_dir("rst");
    let s = Srv::start(&d).await;
    seed(&s).await;
    s.post("agent-7", json!([tail(PK, "pack", "open")])).await;
    s.post("agent-8", json!([tail(PK, "pack", "open")])).await;
    s.post("user", json!([put("10.11.21.1002.00", "---\ntitle: x\n---"), put("10.11.21.1002.07", "x")])).await;
    s.post("agent-7", json!([put_t("10.11.21.1003.00", "draft", "---\ntitle: y\n---"), put_t("10.11.21.1003.04", "draft", "## Y\nwhy: y.\n\nY.")])).await;
    s.post("agent-7", json!([{"op": "note", "addr": "10.11.21.1003.04.draft", "body": "add a line"}])).await;
    let paths = ["/books", "/book/10.11.21", "/page/10.11.21.1523", "/page/10.11.21.1003", "/history/10.11.21", "/face/10.11.21.1003.04.draft", "/links/10.11.21.1523", "/resolve/10.11.21.1003.04", "/cards?title=y"];
    let mut a = vec![];
    for p in paths {
        a.push(s.get(p).await);
    }
    s.stop().await;
    let s = Srv::start(&d).await;
    for (i, p) in paths.iter().enumerate() {
        assert_eq!(s.get(p).await, a[i], "{p} differs after restart");
    }
    check_log(&s.book("10.11.21"));
    s.stop().await;
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn held_stalled_client_does_not_block_the_queue() {
    use tokio::io::AsyncWriteExt;
    let s = Srv::start(&kernel_dir("stall")).await;
    seed(&s).await;
    let mut hang = tokio::net::TcpStream::connect(&s.host).await.unwrap();
    hang.write_all(b"POST /propose HTTP/1.1\r\nhost: x\r\ncontent-length: 100000\r\n\r\n{\"by\":").await.unwrap();
    let t = tokio::time::timeout(std::time::Duration::from_secs(5), s.post("user", page("10.11.21", "1002", "a"))).await;
    assert_eq!(t.expect("queue stalled").0, 200);
    drop(hang);
    s.stop().await;
}
