//! TRIAL-X helpers: a raw HTTP/1.1 client (custom headers, raw bytes), an
//! in-process compute on 127.0.0.1:0 over a temp copy of books, and seeds.
//! Written from the trial's side; it does not reuse compute's test helpers.
use compute::{Config, Store};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

static N: AtomicUsize = AtomicUsize::new(0);

pub fn tmp(name: &str) -> PathBuf {
    let d = std::env::temp_dir().join(format!("trialx-{}-{}-{}", std::process::id(), name, N.fetch_add(1, Ordering::SeqCst)));
    let _ = std::fs::remove_dir_all(&d);
    std::fs::create_dir_all(&d).unwrap();
    d
}

pub fn repo() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
}

/// Copy every `.book` of the repo's books/ into a fresh temp dir.
pub fn real_books(name: &str) -> PathBuf {
    let d = tmp(name);
    identities(&d);
    for e in std::fs::read_dir(repo().join("books")).unwrap() {
        let e = e.unwrap();
        if e.file_name().to_string_lossy().ends_with(".book") {
            std::fs::copy(e.path(), d.join(e.file_name())).unwrap();
        }
    }
    d
}

/// A minimal ASCII kernel: door, page 0020 seated 01 + 04.
pub const KERNEL: &str = concat!(
    r###"{"seqbook":1,"address":"00.00.00"}"###, "\n",
    r###"{"n":1,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0000.00","body":"---\ntitle: kernel\n---"}"###, "\n",
    r###"{"n":2,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0000.04","body":"## Kernel\nwhy: base.\n\nThe kernel."}"###, "\n",
    r###"{"n":3,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.00","body":"---\ntitle: routing\n---"}"###, "\n",
    r###"{"n":4,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.01","body":"## Route\nkernel route."}"###, "\n",
    r###"{"n":5,"at":"2026-11-11T19:30:00Z","by":"user","op":"put","addr":"00.00.00.0020.04","body":"## Route\nwhy: kernel why.\n\nKernel reason."}"###, "\n",
);

pub fn kernel_dir(name: &str) -> PathBuf {
    let d = tmp(name);
    identities(&d);
    std::fs::write(d.join("00.00.00.book"), KERNEL).unwrap();
    d
}

/// Writers the trial servers know (compute fix pass: every write carries a token).
/// `compute` is listed so a client presenting its token can be shown refused.
pub const WRITERS: &[&str] = &["director", "agent-7", "agent-8", "agent-9", "reviewer", "trial-x", "compute"];

/// The token for a writer name. "user" (the round-2 trials) writes as the Director.
/// Any other name gets a token no server knows (so `agent-7 ` is refused 401).
pub fn token(by: &str) -> String {
    let n = if by == "user" { "director" } else { by };
    format!("tok-{n}-0123456789")
}

/// Write `<dir>/.identities` (NAME TOKEN per line) if it is missing.
pub fn identities(dir: &Path) {
    let p = dir.join(".identities");
    if !p.exists() {
        let mut t: String = WRITERS.iter().map(|w| format!("{w} {}\n", token(w))).collect();
        for i in 0..64 {
            if !WRITERS.contains(&format!("agent-{i}").as_str()) {
                t.push_str(&format!("agent-{i} {}\n", token(&format!("agent-{i}"))));
            }
        }
        std::fs::write(p, t).unwrap();
    }
}

/// The book files of a dir: compute state files (`.identities`, `.queue`) are dotfiles.
pub fn listing(dir: &Path) -> Vec<String> {
    let mut v: Vec<String> = std::fs::read_dir(dir).unwrap().map(|e| e.unwrap().file_name().to_string_lossy().to_string()).filter(|n| !n.starts_with('.')).collect();
    v.sort();
    v
}

pub fn read(dir: &Path, book: &str) -> String {
    std::fs::read_to_string(dir.join(format!("{book}.book"))).unwrap_or_default()
}

pub struct Resp {
    pub code: u16,
    pub head: String,
    pub body: Vec<u8>,
}
impl Resp {
    pub fn json(&self) -> Value {
        serde_json::from_slice(&self.body).unwrap_or(Value::Null)
    }
    pub fn header(&self, name: &str) -> Option<String> {
        let n = format!("{}:", name.to_ascii_lowercase());
        self.head.lines().find(|l| l.to_ascii_lowercase().starts_with(&n)).map(|l| l[n.len()..].trim().to_string())
    }
}

/// Send raw bytes as one HTTP/1.1 request and read the whole answer.
pub async fn raw(host: &str, bytes: &[u8]) -> Resp {
    let mut s = tokio::net::TcpStream::connect(host).await.expect("connect");
    let _ = s.write_all(bytes).await;
    let mut buf = Vec::new();
    let _ = s.read_to_end(&mut buf).await;
    let split = buf.windows(4).position(|w| w == b"\r\n\r\n").unwrap_or(buf.len());
    let head = String::from_utf8_lossy(&buf[..split]).to_string();
    let code = head.split_whitespace().nth(1).and_then(|c| c.parse().ok()).unwrap_or(0);
    let mut body = if split + 4 <= buf.len() { buf[split + 4..].to_vec() } else { vec![] };
    if head.to_ascii_lowercase().contains("transfer-encoding: chunked") {
        let mut out = Vec::new();
        let mut i = 0;
        while let Some(e) = body[i..].windows(2).position(|w| w == b"\r\n").map(|p| p + i) {
            let n = usize::from_str_radix(String::from_utf8_lossy(&body[i..e]).trim(), 16).unwrap_or(0);
            if n == 0 {
                break;
            }
            out.extend_from_slice(&body[e + 2..e + 2 + n]);
            i = e + 4 + n;
        }
        body = out;
    }
    Resp { code, head, body }
}

/// One request. A POST with a JSON body naming `by` and no `authorization`
/// header gets that writer's token added (the compute ignores the body's `by`).
pub async fn req(host: &str, method: &str, path: &str, headers: &[(&str, &str)], body: &[u8]) -> Resp {
    let mut h = format!("{method} {path} HTTP/1.1\r\nhost: {host}\r\nconnection: close\r\ncontent-length: {}\r\n", body.len());
    for (k, v) in headers {
        h.push_str(&format!("{k}: {v}\r\n"));
    }
    if method == "POST" && !headers.iter().any(|(k, _)| k.eq_ignore_ascii_case("authorization")) {
        if let Some(by) = serde_json::from_slice::<Value>(body).ok().and_then(|v| v.get("by").and_then(|b| b.as_str()).map(|b| b.to_string())) {
            h.push_str(&format!("authorization: Bearer {}\r\n", token(&by)));
        }
    }
    h.push_str("\r\n");
    let mut b = h.into_bytes();
    b.extend_from_slice(body);
    raw(host, &b).await
}

pub struct Srv {
    pub host: String,
    pub dir: PathBuf,
    task: tokio::task::JoinHandle<()>,
}

impl Srv {
    /// The reader's book is 10.11.21 (as scripts/dev.sh passes `--book`), so a
    /// request naming no book reads that chain only (fix pass, finding 13).
    pub async fn start(dir: &Path) -> Srv {
        let mut cfg = Config::for_dirs(vec![dir.to_path_buf()]);
        cfg.default_book = seqaddr_core::BookId::parse("10.11.21").ok();
        Self::start_cfg(cfg, dir).await
    }
    pub async fn start_cfg(cfg: Config, dir: &Path) -> Srv {
        identities(dir);
        let store = Store::boot(cfg).expect("boot");
        let l = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let host = l.local_addr().unwrap().to_string();
        let task = tokio::spawn(async move {
            let _ = compute::serve(store, l).await;
        });
        Srv { host, dir: dir.to_path_buf(), task }
    }
    pub async fn stop(self) {
        self.task.abort();
        let _ = self.task.await;
    }
    pub async fn get(&self, path: &str) -> (u16, Value) {
        let r = req(&self.host, "GET", path, &[], b"").await;
        (r.code, r.json())
    }
    pub async fn post(&self, by: &str, ops: Value) -> (u16, Value) {
        self.post_bytes(json!({"by": by, "ops": ops}).to_string().as_bytes()).await
    }
    pub async fn post_bytes(&self, body: &[u8]) -> (u16, Value) {
        let r = req(&self.host, "POST", "/propose", &[("content-type", "application/json")], body).await;
        (r.code, r.json())
    }
    pub fn book(&self, b: &str) -> String {
        read(&self.dir, b)
    }
}

/// A bare (seating) put. It carries `approved_by: director` so seeds written
/// "by user" pass a core that gates seating puts (CORE fix pass, R2/E7); a
/// core without that gate ignores the extra field.
pub fn put(addr: &str, body: &str) -> Value {
    json!({"op": "put", "addr": addr, "body": body, "approved_by": "director"})
}
/// A bare put with no approval field at all.
pub fn put_plain(addr: &str, body: &str) -> Value {
    json!({"op": "put", "addr": addr, "body": body})
}
pub fn put_t(addr: &str, tail: &str, body: &str) -> Value {
    json!({"op": "put", "addr": addr, "tail": tail, "body": body})
}
pub fn tail(addr: &str, from: &str, to: &str) -> Value {
    json!({"op": "tail", "addr": addr, "from": from, "to": to})
}
/// A new page: door + a why face (C1.1).
pub fn page(book: &str, pg: &str, title: &str) -> Value {
    json!([put(&format!("{book}.{pg}.00"), &format!("---\ntitle: {title}\n---")), put(&format!("{book}.{pg}.04"), &format!("## {title}\nwhy: trial page.\n\n{title}."))])
}

pub const PK: &str = "10.11.21.1523.05.03";

/// Open a book with its door. R10 says the door page 0000 holds only face 00;
/// the committed core (C1.1) still wants a content face with it. Try the R10
/// form first and fall back, so the trial runs on either core.
pub async fn door(s: &Srv, book: &str, title: &str) {
    let (c, v) = s.post("user", json!([put(&format!("{book}.0000.00"), &format!("---\ntitle: {title}\n---"))])).await;
    if c == 200 {
        return;
    }
    let (c2, v2) = s.post("user", page(book, "0000", title)).await;
    assert_eq!(c2, 200, "door {book}: R10 form -> {c} {v}; C1.1 form -> {v2}");
}

/// Book 10.11.21 door, page 1523 with a pack on 05.03.
pub async fn seed(s: &Srv) {
    door(s, "10.11.21", "tools").await;
    let (c, v) = s.post("user", json!([put("10.11.21.1523.00", "---\ntitle: timer\n---"), put_t(PK, "pack", "## w01\ntype: work\n\nBuild the timer.")])).await;
    assert_eq!(c, 200, "{v}");
}
