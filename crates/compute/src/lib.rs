//! # compute
//!
//! The one process that owns every book (format.md 1.2). Reads are open;
//! writes are proposals sent to one serialized queue, validated by
//! seqaddr-core, and appended to the book file when approved. HTTP API per
//! docs/CONTRACT.md, shaped to match what app/ consumes.
//!
//! Every write names its writer by a token (identity.rs, provisional 7); the
//! body's `by` is ignored. No CORS headers: only same-machine clients and the
//! app's server-side pass-through talk to the compute.

pub mod askq;
pub mod identity;
pub mod store;

pub use identity::Identities;
pub use store::{ApprovalGate, BootError, Config, Store};

use axum::extract::{Path, Query, State};
use axum::http::{HeaderMap, HeaderValue, StatusCode};
use axum::response::{IntoResponse, Response};
use axum::routing::{get, post};
use axum::{Json, Router};
use serde_json::{json, Value};
use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, RwLock};
use tokio::sync::{mpsc, oneshot};

/// One write, in queue order. Only the writer task touches book files.
pub enum Write {
    Propose(Value),
    Seq(String),
    AskLink(Value),
    Close(Value),
}

type Job = (Write, String, oneshot::Sender<store::Answer>);

#[derive(Clone)]
pub struct App {
    pub store: Arc<RwLock<Store>>,
    tx: mpsc::Sender<Job>,
    pending: Arc<AtomicUsize>,
}

impl App {
    /// Start the single writer: every write goes through this one queue, in order (format 2).
    pub fn new(store: Store) -> App {
        let store = Arc::new(RwLock::new(store));
        let (tx, mut rx) = mpsc::channel::<Job>(1024);
        let pending = Arc::new(AtomicUsize::new(0));
        let (s2, p2) = (store.clone(), pending.clone());
        tokio::spawn(async move {
            while let Some((w, by, reply)) = rx.recv().await {
                let ans = {
                    let mut s = s2.write().unwrap_or_else(|e| e.into_inner());
                    match w {
                        Write::Propose(v) => s.propose(v, &by),
                        Write::Seq(t) => s.propose_seq(&t, &by),
                        Write::AskLink(v) => s.ask_link(&v, &by),
                        Write::Close(v) => s.close(&v, &by),
                    }
                };
                p2.fetch_sub(1, Ordering::SeqCst);
                let _ = reply.send(ans);
            }
        });
        App { store, tx, pending }
    }
    fn read<T>(&self, f: impl FnOnce(&Store) -> T) -> T {
        f(&self.store.read().unwrap_or_else(|e| e.into_inner()))
    }
    async fn write(&self, w: Write, by: String) -> Response {
        let (tx, rx) = oneshot::channel();
        self.pending.fetch_add(1, Ordering::SeqCst);
        if self.tx.send((w, by, tx)).await.is_err() {
            return reply((503, json!({"error": "queue", "detail": "the write queue is closed"})));
        }
        match rx.await {
            Ok(ans) => reply(ans),
            Err(_) => reply((500, json!({"error": "queue", "detail": "the writer stopped"}))),
        }
    }
    /// Who is writing: the name for the request's token (identity.rs).
    fn who(&self, h: &HeaderMap) -> Result<String, Response> {
        let tok = h
            .get("authorization")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.strip_prefix("Bearer "))
            .or_else(|| h.get("x-seq-token").and_then(|v| v.to_str().ok()))
            .map(|s| s.to_string());
        let Some(tok) = tok else {
            return Err(reply((401, json!({"status": "rejected", "error": "identity", "detail": "every write carries `Authorization: Bearer TOKEN` (books/.identities); the body's `by` is not trusted"}))));
        };
        self.read(|s| s.ids.who(&tok)).map_err(|(c, e, d)| reply((c, json!({"status": "rejected", "error": e, "axiom": "1", "detail": d}))))
    }
}

fn reply((code, body): store::Answer) -> Response {
    (StatusCode::from_u16(code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR), Json(body)).into_response()
}

/// The request's media type, lowercased, without parameters.
fn media(h: &HeaderMap) -> String {
    h.get("content-type").and_then(|v| v.to_str().ok()).unwrap_or("").split(';').next().unwrap_or("").trim().to_ascii_lowercase()
}

fn unsupported(allowed: &str) -> Response {
    reply((415, json!({"status": "rejected", "error": "media", "detail": format!("send Content-Type {allowed} (a cross-site form or text/plain post is refused)")})))
}

fn json_body(body: &[u8]) -> Result<Value, Response> {
    serde_json::from_slice(body).map_err(|e| reply((400, json!({"status": "rejected", "error": "invalid", "detail": format!("body is not JSON: {e}"), "reasons": [], "entries": []}))))
}

async fn health(State(a): State<App>) -> Response {
    let p = a.pending.load(Ordering::SeqCst);
    reply(a.read(|s| s.health(p)))
}
async fn books(State(a): State<App>) -> Response {
    reply(a.read(|s| s.books()))
}
async fn book(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.book(&x)))
}
async fn page(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.page(&x)))
}
async fn face(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.face(&x)))
}
async fn resolve(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.resolve(&x)))
}
async fn history(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.history(&x)))
}
async fn links(State(a): State<App>, Path(x): Path<String>) -> Response {
    reply(a.read(|s| s.links(&x)))
}
async fn brands(State(a): State<App>, Query(q): Query<HashMap<String, String>>) -> Response {
    let w = q.get("q").cloned().unwrap_or_default();
    let b = q.get("book").cloned();
    reply(a.read(|s| s.brands(&w, b.as_deref())))
}
async fn cards(State(a): State<App>, Query(q): Query<HashMap<String, String>>) -> Response {
    let t = q.get("title").cloned().unwrap_or_default();
    reply(a.read(|s| s.cards(&t)))
}
async fn queue(State(a): State<App>) -> Response {
    let p = a.pending.load(Ordering::SeqCst);
    reply(a.read(|s| s.queue_view(p)))
}
async fn page_seq(State(a): State<App>, Query(q): Query<HashMap<String, String>>) -> Response {
    let addr = q.get("addr").cloned().unwrap_or_default();
    match a.read(|s| s.page_seq(&addr)) {
        Ok((text, name)) => {
            let mut r = (StatusCode::OK, text).into_response();
            r.headers_mut().insert("content-type", HeaderValue::from_static("text/plain; charset=us-ascii"));
            if let Ok(v) = HeaderValue::from_str(&format!("attachment; filename=\"{name}\"")) {
                r.headers_mut().insert("content-disposition", v);
            }
            r
        }
        Err(ans) => reply(ans),
    }
}
async fn check_seq(State(a): State<App>, h: HeaderMap, body: axum::body::Bytes) -> Response {
    if media(&h) != "text/x-seqpage" {
        return unsupported("text/x-seqpage");
    }
    let text = String::from_utf8_lossy(&body).to_string();
    reply(a.read(|s| s.check_seq(&text)))
}
async fn propose(State(a): State<App>, h: HeaderMap, body: axum::body::Bytes) -> Response {
    let m = media(&h);
    if m != "application/json" && m != "text/x-seqpage" {
        return unsupported("application/json or text/x-seqpage");
    }
    let by = match a.who(&h) {
        Ok(n) => n,
        Err(r) => return r,
    };
    if m == "text/x-seqpage" {
        let Ok(text) = String::from_utf8(body.to_vec()) else { return reply((422, json!({"ok": false, "errors": [{"line": 0, "code": "invalid", "rule": "R4", "detail": "the .seq file is not plain ASCII"}]}))) };
        return a.write(Write::Seq(text), by).await;
    }
    match json_body(&body) {
        Ok(v) => a.write(Write::Propose(v), by).await,
        Err(r) => r,
    }
}
async fn ask(State(a): State<App>, h: HeaderMap, body: axum::body::Bytes) -> Response {
    if media(&h) != "application/json" {
        return unsupported("application/json");
    }
    match json_body(&body) {
        Ok(v) => reply(a.read(|s| s.ask(&v))),
        Err(r) => r,
    }
}
async fn ask_link(State(a): State<App>, h: HeaderMap, body: axum::body::Bytes) -> Response {
    if media(&h) != "application/json" {
        return unsupported("application/json");
    }
    let by = match a.who(&h) {
        Ok(n) => n,
        Err(r) => return r,
    };
    match json_body(&body) {
        Ok(v) => a.write(Write::AskLink(v), by).await,
        Err(r) => r,
    }
}
async fn close(State(a): State<App>, h: HeaderMap, body: axum::body::Bytes) -> Response {
    if media(&h) != "application/json" {
        return unsupported("application/json");
    }
    let by = match a.who(&h) {
        Ok(n) => n,
        Err(r) => return r,
    };
    match json_body(&body) {
        Ok(v) => a.write(Write::Close(v), by).await,
        Err(r) => r,
    }
}
async fn not_found(uri: axum::http::Uri) -> Response {
    reply((404, json!({"error": "route", "detail": uri.path()})))
}

pub fn router(app: App) -> Router {
    Router::new()
        .route("/health", get(health))
        .route("/books", get(books))
        .route("/book/:addr", get(book))
        .route("/page/:addr", get(page))
        .route("/face/:addr", get(face))
        .route("/resolve/:addr", get(resolve))
        .route("/history/:addr", get(history))
        .route("/links/:addr", get(links))
        .route("/brands", get(brands))
        .route("/cards", get(cards))
        .route("/queue", get(queue))
        .route("/page.seq", get(page_seq))
        .route("/check.seq", post(check_seq))
        .route("/propose", post(propose))
        .route("/ask", post(ask))
        .route("/ask/link", post(ask_link))
        .route("/close", post(close))
        .fallback(not_found)
        .with_state(app)
}

/// Serve on a bound listener until the future ends (used by main and the tests).
pub async fn serve(store: Store, listener: tokio::net::TcpListener) -> std::io::Result<()> {
    let app = App::new(store);
    axum::serve(listener, router(app)).await
}
