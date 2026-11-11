//! kill -9 a real compute process (trial-srv = compute lib, own process) in the
//! middle of a stream of multi-op appends, then restart: every acknowledged
//! proposal is there whole, nothing half-written survives, writes continue.
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::sync::{Arc, Mutex};
use trial_compute::*;

fn spawn(dir: &std::path::Path) -> (std::process::Child, String) {
    let mut ch = Command::new(env!("CARGO_BIN_EXE_trial-srv")).arg(dir).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
    let mut l = String::new();
    BufReader::new(ch.stdout.take().unwrap()).read_line(&mut l).unwrap();
    let port = l.trim().strip_prefix("PORT ").expect("port line").to_string();
    (ch, format!("127.0.0.1:{port}"))
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn held_kill9_mid_append_keeps_every_acknowledged_proposal_whole() {
    let d = kernel_dir("kill9");
    let acked: Arc<Mutex<BTreeSet<String>>> = Arc::default();
    let filler = "x".repeat(400_000);
    let mut killed_mid = 0;
    {
        let s = Srv::start(&d).await;
        door(&s, "10.11.21", "tools").await;
        s.stop().await;
    }
    for round in 0..6u32 {
        let (mut ch, host) = spawn(&d);
        let mut hs = vec![];
        for w in 0..4u32 {
            let (host, acked, filler) = (host.clone(), acked.clone(), filler.clone());
            hs.push(tokio::spawn(async move {
                for k in 0..100u32 {
                    let pg = format!("{}{w}{k:02}", round + 1);
                    let ops = json!([put(&format!("10.11.21.{pg}.00"), "---\ntitle: p\n---"), put(&format!("10.11.21.{pg}.04"), &format!("## P\nwhy: crash.\n\n{filler}"))]);
                    let body = json!({"by": "user", "ops": ops}).to_string();
                    let r = tokio::time::timeout(std::time::Duration::from_secs(5), req(&host, "POST", "/propose", &[("content-type", "application/json")], body.as_bytes())).await;
                    match r {
                        Ok(r) if r.code == 200 => {
                            acked.lock().unwrap().insert(format!("10.11.21.{pg}"));
                        }
                        _ => return,
                    }
                }
            }));
        }
        // even rounds: kill the moment the file shows a line still being written;
        // odd rounds: kill at a fixed moment
        let f = d.join("10.11.21.book");
        let t0 = std::time::Instant::now();
        if round % 2 == 0 {
            while t0.elapsed() < std::time::Duration::from_secs(4) {
                if let Ok(b) = std::fs::read(&f) {
                    if b.last().is_some_and(|c| *c != b'\n') {
                        break;
                    }
                }
                tokio::time::sleep(std::time::Duration::from_micros(200)).await;
            }
        } else {
            tokio::time::sleep(std::time::Duration::from_millis(150 + 70 * round as u64)).await;
        }
        ch.kill().unwrap(); // SIGKILL
        ch.wait().unwrap();
        for h in hs {
            let _ = h.await;
        }
        if !read(&d, "10.11.21").ends_with('\n') {
            killed_mid += 1;
        }
        // restart in process and check
        let s = Srv::start(&d).await;
        let (_, h) = s.get("/health").await;
        assert_eq!(h["refused"], json!([]), "round {round}: book refused after kill -9: {h}");
        let (_, b) = s.get("/book/10.11.21").await;
        let pages: Vec<Value> = b["pages"].as_array().unwrap().clone();
        for p in pages.iter().filter(|p| p["page"] != "0000") {
            let f: Vec<&str> = p["faces"].as_array().unwrap().iter().map(|x| x.as_str().unwrap()).collect();
            assert_eq!(f, ["00", "04"], "round {round}: half a proposal survived on page {}", p["page"]);
        }
        let have: BTreeSet<String> = pages.iter().map(|p| format!("10.11.21.{}", p["page"].as_str().unwrap())).collect();
        let lost: Vec<String> = acked.lock().unwrap().iter().filter(|a| !have.contains(*a)).cloned().collect();
        assert!(lost.is_empty(), "round {round}: acknowledged but lost: {lost:?}");
        let (c, v) = s.post("user", page("10.11.21", &format!("{}998", round + 1), "after")).await;
        assert_eq!(c, 200, "round {round}: write after restart: {v}");
        acked.lock().unwrap().insert(format!("10.11.21.{}998", round + 1));
        assert!(read(&d, "10.11.21").ends_with('\n'));
        s.stop().await;
    }
    assert!(acked.lock().unwrap().len() > 10, "the storm wrote something");
    eprintln!("kill -9 rounds that left a cut line: {killed_mid}/6 (one write() per proposal: SIGKILL does not cut it; see the cut sweep); acked {}", acked.lock().unwrap().len());
}

/// kill -9 cannot cut a single write() in practice, so a cut line (power loss,
/// full disk) is simulated: cut the book at every byte inside its last
/// multi-op proposal and boot. The book is never refused, the proposal is
/// there whole or not at all, and the next write lands on a clean line.
#[tokio::test]
async fn held_cut_at_every_byte_of_the_last_proposal() {
    let d = kernel_dir("cut");
    let s = Srv::start(&d).await;
    seed(&s).await;
    let before = read(&d, "10.11.21");
    let (c, _) = s.post("user", page("10.11.21", "1002", "cut")).await;
    assert_eq!(c, 200);
    s.stop().await;
    let full = read(&d, "10.11.21");
    for cut in before.len()..full.len() {
        let dd = kernel_dir("cutx");
        std::fs::write(dd.join("10.11.21.book"), &full[..cut]).unwrap();
        let st = compute::Store::boot(compute::Config::for_dirs(vec![dd.clone()])).expect("kernel ok");
        assert!(st.refused.is_empty(), "cut at {cut}: refused {:?}", st.refused);
        let s = Srv::start(&dd).await;
        let (c, p) = s.get("/page/10.11.21.1002").await;
        let whole = c == 200 && p["faces"].get("00").is_some() && p["faces"].get("04").is_some();
        assert!(c == 404 || whole, "cut at {cut}: half a proposal: {c} {p}");
        let (c, v) = s.post("user", page("10.11.21", "1003", "after")).await;
        assert_eq!(c, 200, "cut at {cut}: {v}");
        let t = read(&dd, "10.11.21");
        assert!(t.lines().all(|l| serde_json::from_str::<Value>(l).is_ok()) && t.ends_with('\n'), "cut at {cut}: file not whole lines");
        s.stop().await;
        let _ = std::fs::remove_dir_all(&dd);
    }
}
