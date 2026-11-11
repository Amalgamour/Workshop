#![allow(dead_code)]
use compute::{Config, Store};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicUsize, Ordering};

static N: AtomicUsize = AtomicUsize::new(0);

pub fn tmp(name: &str) -> PathBuf {
    let d = std::env::temp_dir().join(format!("compute-test-{}-{}-{}", std::process::id(), name, N.fetch_add(1, Ordering::SeqCst)));
    let _ = std::fs::remove_dir_all(&d);
    std::fs::create_dir_all(&d).unwrap();
    d
}

/// A small kernel: door 0000; page 0020 with a seated 01 (plus a working draft of it with one note) and 04;
/// page 0030 whose only 01 is a draft (R5).
pub const KERNEL: &str = concat!(
    r###"{"seqbook":1,"address":"00.00.00"}"###, "\n",
    r###"{"n":1,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0000.00","body":"---\ntitle: kernel\n---"}"###, "\n",
    r###"{"n":2,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.00","body":"---\ntitle: routing\n---"}"###, "\n",
    r###"{"n":3,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.01","body":"## Route\nRoute the work."}"###, "\n",
    r###"{"n":4,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.04","body":"## Route\nwhy: kernel why.\n\nKernel reason."}"###, "\n",
    r###"{"n":5,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0030.00","body":"---\ntitle: waiting\n---"}"###, "\n",
    r###"{"n":6,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0030.01","tail":"draft","body":"## Wait\nA draft rule."}"###, "\n",
    r###"{"n":7,"at":"2026-11-11T19:30:00Z","by":"user","op":"copy","addr":"00.00.00.0020.01"}"###, "\n",
    r###"{"n":8,"at":"2026-11-11T19:30:00Z","by":"user","op":"note","addr":"00.00.00.0020.01.draft","body":"say who routes"}"###, "\n",
);

pub fn kernel_dir(name: &str) -> PathBuf {
    let d = tmp(name);
    std::fs::write(d.join("00.00.00.book"), KERNEL).unwrap();
    d
}

pub fn repo_books() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../../books")
}

pub fn copy_dir(from: &Path, name: &str) -> PathBuf {
    let d = tmp(name);
    for e in std::fs::read_dir(from).unwrap() {
        let e = e.unwrap();
        if e.file_name().to_string_lossy().ends_with(".book") {
            std::fs::copy(e.path(), d.join(e.file_name())).unwrap();
        }
    }
    d
}

pub struct Srv {
    pub base: String,
    pub dir: PathBuf,
    pub task: tokio::task::JoinHandle<()>,
    pub http: Http,
}

impl Srv {
    pub async fn start(dir: &Path) -> Srv {
        write_identities(dir);
        let store = Store::boot(Config::for_dirs(vec![dir.to_path_buf()])).expect("boot");
        let l = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let base = format!("http://{}", l.local_addr().unwrap());
        let task = tokio::spawn(async move {
            let _ = compute::serve(store, l).await;
        });
        Srv { base, dir: dir.to_path_buf(), task, http: Http }
    }
    pub async fn stop(self) {
        self.task.abort();
        let _ = self.task.await;
    }
    pub async fn get(&self, path: &str) -> (u16, Value) {
        let (c, b) = Http.req(&self.base, "GET", path, None).await;
        (c, serde_json::from_slice(&b).unwrap_or(Value::Null))
    }
    pub async fn post(&self, by: &str, ops: Value) -> (u16, Value) {
        self.post_raw(json!({"by": by, "ops": ops})).await
    }
    /// POST /propose with the token of the body's `by` ("user" is the Director, as in round 2).
    pub async fn post_raw(&self, body: Value) -> (u16, Value) {
        let by = body["by"].as_str().unwrap_or("user").to_string();
        self.post_as(&by, "/propose", body).await
    }
    /// POST a JSON body to `path` as writer `by` (token `tok-NAME`).
    pub async fn post_as(&self, by: &str, path: &str, body: Value) -> (u16, Value) {
        let auth = format!("Bearer {}", token(by));
        let (c, b) = Http.req_h(&self.base, "POST", path, Some(body.to_string().into_bytes()), &[("content-type", "application/json"), ("authorization", &auth)]).await;
        (c, serde_json::from_slice(&b).unwrap_or(Value::Null))
    }
    /// POST /ask (a read: no token needed).
    pub async fn ask(&self, prompt: &str) -> (u16, Value) {
        let (c, b) = Http.req(&self.base, "POST", "/ask", Some(json!({"prompt": prompt, "book": "10.11.21"}).to_string().into_bytes())).await;
        (c, serde_json::from_slice(&b).unwrap_or(Value::Null))
    }
    pub fn lines(&self, book: &str) -> usize {
        std::fs::read_to_string(self.dir.join(format!("{book}.book"))).map(|t| t.lines().count()).unwrap_or(0)
    }
}

/// The writers every test server knows (`NAME tok-NAME`).
pub const WRITERS: &[&str] = &["director", "alice", "bob", "trial-x", "kernel", "app", "agent-7", "agent-8", "reviewer", "compute"];

/// The token for a writer name; "user" (round-2 tests) writes as the Director.
pub fn token(by: &str) -> String {
    let n = if by == "user" { "director" } else { by };
    format!("tok-{n}-0123456789")
}

pub fn write_identities(dir: &Path) {
    let p = dir.join(".identities");
    if !p.exists() {
        let mut t = String::from("# test identities\n");
        for w in WRITERS {
            t.push_str(&format!("{w} {}\n", token(w)));
        }
        std::fs::write(p, t).unwrap();
    }
}

/// A seated put, signed by the Director (R2/E7: seating needs an approval record).
pub fn put(addr: &str, body: &str) -> Value {
    json!({"op": "put", "addr": addr, "body": body, "approved_by": "director"})
}
pub fn put_t(addr: &str, tail: &str, body: &str) -> Value {
    json!({"op": "put", "addr": addr, "tail": tail, "body": body})
}
pub fn tail(addr: &str, from: &str, to: &str) -> Value {
    json!({"op": "tail", "addr": addr, "from": from, "to": to})
}

pub const PK: &str = "10.11.21.1523.05.03";

/// Book 10.11.21 with its door, page 0020 overriding the kernel's 04, and a pack on 1523.05.03.
pub async fn seed(s: &Srv) {
    let (c, v) = s.post("user", json!([put("10.11.21.0000.00", "---\ntitle: tools\n---")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, v) = s.post("user", json!([put("10.11.21.0020.00", "---\ntitle: routing\n---"), put("10.11.21.0020.04", "## Route\nwhy: local why.\n\nLocal reason.")])).await;
    assert_eq!(c, 200, "{v}");
    let (c, v) = s.post("user", json!([put("10.11.21.1523.00", "---\ntitle: timer\n---"), put_t(PK, "pack", "## w01\ntype: work\n\nBuild the timer.")])).await;
    assert_eq!(c, 200, "{v}");
}

/// A tiny HTTP/1.1 client (one request per connection), so the tests need no extra crates.
#[derive(Clone, Copy)]
pub struct Http;

impl Http {
    pub async fn req(&self, base: &str, method: &str, path: &str, body: Option<Vec<u8>>) -> (u16, Vec<u8>) {
        self.req_h(base, method, path, body, &[("content-type", "application/json")]).await
    }
    pub async fn req_h(&self, base: &str, method: &str, path: &str, body: Option<Vec<u8>>, headers: &[(&str, &str)]) -> (u16, Vec<u8>) {
        use tokio::io::{AsyncReadExt, AsyncWriteExt};
        let host = base.trim_start_matches("http://");
        let mut s = tokio::net::TcpStream::connect(host).await.unwrap();
        let body = body.unwrap_or_default();
        let head = format!("{method} {path} HTTP/1.1\r\nhost: {host}\r\nconnection: close\r\n{}content-length: {}\r\n\r\n", headers.iter().map(|(k, v)| format!("{k}: {v}\r\n")).collect::<String>(), body.len());
        s.write_all(head.as_bytes()).await.unwrap();
        s.write_all(&body).await.unwrap();
        let mut buf = Vec::new();
        s.read_to_end(&mut buf).await.unwrap();
        let split = buf.windows(4).position(|w| w == b"\r\n\r\n").expect("http head");
        let head = String::from_utf8_lossy(&buf[..split]).to_string();
        let code: u16 = head.split_whitespace().nth(1).unwrap().parse().unwrap();
        let mut rest = buf[split + 4..].to_vec();
        if head.to_ascii_lowercase().contains("transfer-encoding: chunked") {
            let mut out = Vec::new();
            let mut i = 0;
            loop {
                let e = rest[i..].windows(2).position(|w| w == b"\r\n").unwrap() + i;
                let n = usize::from_str_radix(String::from_utf8_lossy(&rest[i..e]).trim(), 16).unwrap();
                if n == 0 { break; }
                out.extend_from_slice(&rest[e + 2..e + 2 + n]);
                i = e + 4 + n;
            }
            rest = out;
        }
        (code, rest)
    }
}
