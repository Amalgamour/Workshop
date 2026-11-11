//! Bootstrap (kernel-design 7) and crash safety (format 3.1): restart replays to the same state.
mod common;
use common::*;
use compute::{Config, Store};
use serde_json::{json, Value};

async fn state(s: &Srv) -> Vec<Value> {
    let mut book = s.get("/book/10.11.21").await.1;
    book["warnings"] = json!("(load notes compared separately)");
    let mut out = vec![s.get("/books").await.1, book];
    for p in ["/page/10.11.21.0020", "/page/10.11.21.1523", &format!("/face/{PK}"), "/history/10.11.21", "/links/10.11.21.0020", "/resolve/10.11.21.0020.01"] {
        out.push(s.get(p).await.1);
    }
    out
}

#[tokio::test]
async fn restart_replays_to_same_state() {
    let dir = kernel_dir("rs");
    let s = Srv::start(&dir).await;
    seed(&s).await;
    s.post("agent-7", json!([tail(PK, "pack", "open")])).await;
    let a = state(&s).await;
    s.stop().await;
    let s = Srv::start(&dir).await;
    assert_eq!(a, state(&s).await);
    s.stop().await;
}

#[tokio::test]
async fn partial_last_line_dropped_on_load_then_writes_continue() {
    let dir = kernel_dir("pl");
    let s = Srv::start(&dir).await;
    seed(&s).await;
    let a = state(&s).await;
    s.stop().await;
    // a crash mid-write leaves part of a line
    let f = dir.join("10.11.21.book");
    let mut t = std::fs::read_to_string(&f).unwrap();
    t.push_str(r#"{"n":6,"at":"2026-11-11T20:00:00Z","by":"agent-7","op":"tail","addr":"10.11"#);
    std::fs::write(&f, &t).unwrap();
    let s = Srv::start(&dir).await;
    assert_eq!(a, state(&s).await, "the partial line is ignored");
    let (_, b) = s.get("/book/10.11.21").await;
    assert!(b["warnings"][0].as_str().unwrap().contains("partly written"), "{b}");
    let (c, v) = s.post("agent-7", json!([tail(PK, "pack", "open")])).await;
    assert_eq!(c, 200, "{v}");
    assert_eq!(v["entries"], json!([6]));
    let text = std::fs::read_to_string(&f).unwrap();
    assert!(text.lines().all(|l| serde_json::from_str::<Value>(l).is_ok()), "file is whole lines again");
    s.stop().await;
    let s = Srv::start(&dir).await;
    assert_eq!(s.get(&format!("/face/{PK}")).await.1["tail"], "open");
    s.stop().await;
}

#[test]
fn boot_refuses_without_kernel() {
    let d = tmp("nok");
    let e = Store::boot(Config::for_dirs(vec![d])).err().expect("refused");
    assert_eq!(e.step, "7.1 locate kernel");
}

#[test]
fn boot_refuses_unknown_format_version() {
    let d = tmp("ver");
    std::fs::write(d.join("00.00.00.book"), KERNEL.replacen("\"seqbook\":1", "\"seqbook\":2", 1)).unwrap();
    let e = Store::boot(Config::for_dirs(vec![d.clone()])).err().expect("refused");
    assert_eq!(e.step, "7.2 version");
    assert_eq!(std::fs::read_to_string(d.join("00.00.00.book")).unwrap(), KERNEL.replacen("\"seqbook\":1", "\"seqbook\":2", 1), "nothing rewritten");
}

#[test]
fn boot_refuses_damaged_kernel_but_not_for_a_damaged_book() {
    let d = tmp("dmg");
    let mut lines: Vec<&str> = KERNEL.lines().collect();
    lines.insert(2, "{not json");
    std::fs::write(d.join("00.00.00.book"), lines.join("\n") + "\n").unwrap();
    assert!(Store::boot(Config::for_dirs(vec![d.clone()])).is_err());
    std::fs::write(d.join("00.00.00.book"), KERNEL).unwrap();
    std::fs::write(d.join("10.11.21.book"), "{\"seqbook\":1,\"address\":\"10.11.22\"}\n").unwrap();
    let s = Store::boot(Config::for_dirs(vec![d])).expect("kernel ok, bad book refused");
    assert_eq!(s.refused.len(), 1);
    assert_eq!(s.refused[0]["step"], "7.3 address");
    assert_eq!(s.world.books.len(), 1);
}

#[test]
fn boot_loads_the_real_books() {
    let s = Store::boot(Config::for_dirs(vec![repo_books()])).expect("real books boot");
    assert!(s.refused.is_empty(), "{:?}", s.refused);
    assert!(s.world.books.len() >= 4);
}
