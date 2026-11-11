//! `compute [--books DIR]... [--listen ADDR] [--book DD.SS.BB] [--no-r2] [--allow-remote]`
//! Writes need a token from `<first books dir>/.identities` (scripts/dev.sh makes one).
//! A non-loopback --listen is refused unless --allow-remote (TRIAL-X #12).
//! Defaults: books/ then kernel/ under WORKSHOP_ROOT (or the current folder); 127.0.0.1:7700.
use compute::{Config, Store};
use std::path::PathBuf;

#[tokio::main]
async fn main() {
    let mut dirs: Vec<PathBuf> = Vec::new();
    let mut listen = std::env::var("COMPUTE_LISTEN").unwrap_or_else(|_| "127.0.0.1:7700".into());
    let mut r2 = true;
    let mut remote = false;
    let mut book: Option<String> = None;
    let mut args = std::env::args().skip(1);
    while let Some(a) = args.next() {
        match a.as_str() {
            "--books" => dirs.push(args.next().expect("--books DIR").into()),
            "--listen" => listen = args.next().expect("--listen ADDR"),
            "--no-r2" => r2 = false,
            "--allow-remote" => remote = true,
            "--book" => book = Some(args.next().expect("--book DD.SS.BB")),
            "-h" | "--help" => {
                println!("compute [--books DIR]... [--listen 127.0.0.1:7700] [--book 10.11.21] [--no-r2] [--allow-remote]");
                return;
            }
            other => {
                eprintln!("unknown argument {other}");
                std::process::exit(2);
            }
        }
    }
    if dirs.is_empty() {
        let root = std::env::var("WORKSHOP_ROOT").map(PathBuf::from).unwrap_or_else(|_| PathBuf::from("."));
        dirs = vec![root.join("books"), root.join("kernel")];
    }
    let loopback = listen.parse::<std::net::SocketAddr>().map(|a| a.ip().is_loopback()).unwrap_or_else(|_| listen.starts_with("localhost:"));
    if !loopback && !remote {
        eprintln!("refusing to listen on {listen}: not a loopback address. The compute has no TLS; tokens would cross the network in the clear. Pass --allow-remote to accept that.");
        std::process::exit(2);
    }
    if !loopback {
        eprintln!("warning: listening on {listen} (--allow-remote): tokens travel unencrypted");
    }
    let mut cfg = Config::for_dirs(dirs);
    cfg.approval.allow_build_stage_r2 = r2;
    if let Some(b) = book {
        match seqaddr_core::BookId::parse(&b) {
            Ok(id) => cfg.default_book = Some(id),
            Err(e) => {
                eprintln!("--book {b}: {}", e.detail());
                std::process::exit(2);
            }
        }
    }
    let store = match Store::boot(cfg) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(3);
        }
    };
    for (b, w) in &store.warnings {
        for x in w {
            eprintln!("warning {b}: {x}");
        }
    }
    for r in &store.refused {
        eprintln!("refused: {r}");
    }
    let n = store.world.books.len();
    let listener = tokio::net::TcpListener::bind(&listen).await.unwrap_or_else(|e| {
        eprintln!("cannot listen on {listen}: {e}");
        std::process::exit(4)
    });
    println!("compute on http://{listen}  ({n} books)");
    let app = compute::App::new(store);
    let server = axum::serve(listener, compute::router(app)).with_graceful_shutdown(async {
        let _ = tokio::signal::ctrl_c().await;
    });
    if let Err(e) = server.await {
        eprintln!("server error: {e}");
    }
}
