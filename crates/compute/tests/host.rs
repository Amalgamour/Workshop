//! R33 item 4: a request whose Host is not the compute's own address is
//! refused (421) before any route runs, so another site cannot read pages
//! through DNS rebinding. Its own address, localhost and [::1] work.
mod common;
use common::*;

async fn raw(base: &str, host: Option<&str>) -> (u16, String) {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    let addr = base.trim_start_matches("http://");
    let mut s = tokio::net::TcpStream::connect(addr).await.unwrap();
    let h = host.map(|h| format!("host: {h}\r\n")).unwrap_or_default();
    let req = format!("GET /health HTTP/1.1\r\n{h}connection: close\r\n\r\n");
    s.write_all(req.as_bytes()).await.unwrap();
    let mut buf = Vec::new();
    s.read_to_end(&mut buf).await.unwrap();
    let t = String::from_utf8_lossy(&buf).to_string();
    (t.split_whitespace().nth(1).unwrap().parse().unwrap(), t)
}

#[tokio::test]
async fn wrong_or_missing_host_is_refused() {
    let s = Srv::start(&kernel_dir("host")).await;
    let addr = s.base.trim_start_matches("http://").to_string();
    let port = addr.rsplit(':').next().unwrap().to_string();
    for good in [addr.clone(), format!("localhost:{port}"), format!("LOCALHOST:{port}"), format!("[::1]:{port}")] {
        let (c, t) = raw(&s.base, Some(&good)).await;
        assert_eq!(c, 200, "{good}: {t}");
    }
    for bad in [format!("evil.example:{port}"), "evil.example".to_string(), "127.0.0.1:1".to_string(), "localhost".to_string()] {
        let (c, t) = raw(&s.base, Some(&bad)).await;
        assert_eq!(c, 421, "{bad}: {t}");
        assert!(t.contains("\"error\":\"host\""), "{t}");
    }
    let (c, t) = raw(&s.base, None).await;
    assert_eq!(c, 421, "no Host: {t}");
    assert!(t.contains("no Host header"), "{t}");
    s.stop().await;
}

#[test]
fn allowed_hosts_for_loopback_and_remote() {
    let h = compute::allowed_hosts("127.0.0.1:7700".parse().unwrap(), &[]);
    assert_eq!(h, ["127.0.0.1:7700", "[::1]:7700", "localhost:7700"]);
    let h = compute::allowed_hosts("192.0.2.5:7700".parse().unwrap(), &["Workshop.lan:7700".into()]);
    assert_eq!(h, ["192.0.2.5:7700", "workshop.lan:7700"]);
}
