//! R33 item 3: a line dated earlier than the line above it is refused,
//! on boot (the book is listed as refused) and on a write through the gate.
mod common;
use common::*;
use compute::{Config, Store};
use serde_json::json;

const DOOR: &str = r###"{"n":1,"at":"2099-01-01T00:00:00Z","by":"director","op":"put","addr":"10.11.21.0000.00","approved-by":"director","body":"---\ntitle: tools\n---"}"###;

#[tokio::test]
async fn write_dated_before_the_line_above_is_refused() {
    // The last line is dated 2099, as if the clock went backwards since it was written.
    let d = kernel_dir("clock-w");
    let book = format!("{}\n{DOOR}\n", r###"{"seqbook":1,"address":"10.11.21"}"###);
    std::fs::write(d.join("10.11.21.book"), &book).unwrap();
    let s = Srv::start(&d).await;
    let (c, v) = s.post("user", json!([put("10.11.21.0020.00", "---\ntitle: routing\n---"), put("10.11.21.0020.04", "## Route\nwhy: local why.\n\nLocal reason.")])).await;
    assert_eq!(c, 409, "{v}");
    assert_eq!(v["error"], "clock", "{v}");
    assert!(v["detail"].as_str().unwrap().contains("earlier than the line above"), "{v}");
    assert_eq!(std::fs::read_to_string(d.join("10.11.21.book")).unwrap(), book, "nothing written");
    s.stop().await;
}

#[test]
fn boot_refuses_a_book_whose_times_run_backwards() {
    let d = kernel_dir("clock-b");
    let back = DOOR.replace("2099-01-01T00:00:00Z", "2026-11-11T19:30:00Z");
    let line2 = r###"{"n":2,"at":"2020-01-01T00:00:00Z","by":"director","op":"put","addr":"10.11.21.0020.00","approved-by":"director","body":"---\ntitle: routing\n---"}"###;
    std::fs::write(d.join("10.11.21.book"), format!("{}\n{back}\n{line2}\n", r###"{"seqbook":1,"address":"10.11.21"}"###)).unwrap();
    write_identities(&d);
    let s = Store::boot(Config::for_dirs(vec![d])).expect("kernel ok, the backward book refused");
    assert_eq!(s.refused.len(), 1, "{:?}", s.refused);
    assert!(s.refused[0]["detail"].as_str().unwrap().contains("earlier than the line above"), "{:?}", s.refused);
}
