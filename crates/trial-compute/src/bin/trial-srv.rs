//! A copy of compute's main (lib path only) that binds 127.0.0.1:0 and prints
//! its port, so a test can kill -9 a real separate process mid-write.
//! Usage: trial-srv DIR
use compute::{Config, Store};

#[tokio::main]
async fn main() {
    let dir = std::env::args().nth(1).expect("trial-srv DIR");
    let store = Store::boot(Config::for_dirs(vec![dir.into()])).unwrap_or_else(|e| {
        eprintln!("{e}");
        std::process::exit(3)
    });
    let l = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    println!("PORT {}", l.local_addr().unwrap().port());
    use std::io::Write;
    std::io::stdout().flush().unwrap();
    compute::serve(store, l).await.unwrap();
}
