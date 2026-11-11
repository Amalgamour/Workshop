//! # compute
//!
//! The one process that owns every book (format.md 1.2). Reads are open;
//! writes are proposals sent to one serialized queue, validated by
//! seqaddr-core, and appended to the book file when approved. HTTP API per
//! docs/CONTRACT.md, shaped to match what app/ consumes.

pub mod store;

pub use store::{ApprovalGate, BootError, Config, Store};

use axum::extract::{Path, Query, State};
use axum::http::{HeaderValue, StatusCode};
use axum::response::{IntoResponse, Response};
use axum::routing::{get, post};
use axum::{Json, Router};
use serde_json::Value;
use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, RwLock};
use tokio::sync::{mpsc, oneshot};

type Job = (Value, oneshot::Sender<store::Answer>);

#[derive(Clone)]
pub struct App {
    pub store: Arc<RwLock<Store>>,
    tx: mpsc::Sender<Job>,
    pending: Arc<AtomicUsize>,
}

impl App {
    /// Start the single writer: every proposal goes through this one queue, in order (format 2).
    pub fn new(store: Store) -> App {
        let store = Arc::new(RwLock::new(store));
        let (tx, mut rx) = mpsc::channel::<Job>(1024);
        let pending = Arc::new(AtomicUsize::new(0));
        let (s2, p2) = (store.clone(), pending.clone());
        tokio::spawn(async move {
            while let Some((raw, reply)) = rx.recv().await {
                let ans = { s2.write().unwrap_or_else(|e| e.into_inner()).propose(raw) };
                p2.fetch_sub(1, Ordering::SeqCst);
                let _ = reply.send(ans);
            }
        });
        App { store, tx, pending }
    }
    fn read<T>(&self, f: impl FnOnce(&Store) -> T) -> T {
        f(&self.store.read().unwrap_or_else(|e| e.into_inner()))
    }
}

fn reply((code, body): store::Answer) -> Response {
    let mut r = (StatusCode::from_u16(code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR), Json(body)).into_response();
    r.headers_mut().insert("access-control-allow-origin", HeaderValue::from_static("*"));
    r
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
async fn propose(State(a): State<App>, body: axum::body::Bytes) -> Response {
    let raw: Value = match serde_json::from_slice(&body) {
        Ok(v) => v,
        Err(e) => return reply((400, serde_json::json!({"status": "rejected", "error": "invalid", "detail": format!("body is not JSON: {e}"), "reasons": [], "entries": []}))),
    };
    let (tx, rx) = oneshot::channel();
    a.pending.fetch_add(1, Ordering::SeqCst);
    if a.tx.send((raw, tx)).await.is_err() {
        return reply((503, serde_json::json!({"error": "queue", "detail": "the write queue is closed"})));
    }
    match rx.await {
        Ok(ans) => reply(ans),
        Err(_) => reply((500, serde_json::json!({"error": "queue", "detail": "the writer stopped"}))),
    }
}
async fn not_found(uri: axum::http::Uri) -> Response {
    reply((404, serde_json::json!({"error": "route", "detail": uri.path()})))
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
        .route("/propose", post(propose))
        .fallback(not_found)
        .with_state(app)
}

/// Serve on a bound listener until the future ends (used by main and the tests).
pub async fn serve(store: Store, listener: tokio::net::TcpListener) -> std::io::Result<()> {
    let app = App::new(store);
    axum::serve(listener, router(app)).await
}
