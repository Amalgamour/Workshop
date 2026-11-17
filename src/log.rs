//! The log: `log.jsonl`, one event per line, append only. The only source of truth.
//! Each line holds `prev`, the sha256 of the line before it ("0" for the first),
//! so any edit to an earlier line breaks the chain.

use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;

pub type Res<T> = Result<T, String>;

#[derive(Clone, Debug)]
pub struct Event {
    pub seq: u64,
    pub time: u64,
    pub actor: String,
    pub role: String,
    pub kind: String,
    pub data: Value,
}

pub fn sha(s: &str) -> String {
    let d = Sha256::digest(s.as_bytes());
    d.iter().map(|b| format!("{b:02x}")).collect()
}

pub fn short(h: &str) -> &str {
    &h[..h.len().min(12)]
}

/// Seconds since 1970. `WF_NOW` overrides it (tests and examples).
pub fn now() -> u64 {
    if let Ok(v) = std::env::var("WF_NOW") {
        if let Ok(n) = v.parse() {
            return n;
        }
    }
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0)
}

/// UTC time as `2026-11-17T17:55:00Z`.
pub fn iso(t: u64) -> String {
    let (days, s) = ((t / 86400) as i64, t % 86400);
    // civil-from-days (Howard Hinnant)
    let z = days + 719468;
    let era = z.div_euclid(146097);
    let doe = z - era * 146097;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = yoe + era * 400 + if m <= 2 { 1 } else { 0 };
    format!("{y:04}-{m:02}-{d:02}T{:02}:{:02}:{:02}Z", s / 3600, s / 60 % 60, s % 60)
}

/// Read and check the whole log. Refuses on a broken chain or a bad sequence.
pub fn read(path: &Path) -> Res<(Vec<Event>, String)> {
    let text = fs::read_to_string(path).map_err(|e| format!("cannot read {}: {e}", path.display()))?;
    if !text.is_empty() && !text.ends_with('\n') {
        let n = text.lines().count();
        return Err(format!("last line has no newline: entry {n}; nothing was changed"));
    }
    let mut prev = "0".to_string();
    let mut out = Vec::new();
    let lines: Vec<&str> = text.lines().collect();
    let last = lines.len();
    for (i, line) in lines.iter().enumerate() {
        let v: Value = match serde_json::from_str(line) {
            Ok(v) => v,
            Err(_) if i + 1 == last => {
                return Err(format!("last line is half written: entry {}; nothing was changed", i + 1));
            }
            Err(e) => return Err(format!("log line {} is not JSON: {e}", i + 1)),
        };
        let n = i as u64 + 1;
        if v["prev"].as_str() != Some(prev.as_str()) {
            return Err(format!("log chain broken at line {n}: it does not match the line before (tampered?)"));
        }
        if v["seq"].as_u64() != Some(n) {
            return Err(format!("log line {n} has seq {} (expected {n})", v["seq"]));
        }
        let s = |k: &str| v[k].as_str().unwrap_or("").to_string();
        out.push(Event { seq: n, time: v["time_s"].as_u64().unwrap_or(0), actor: s("actor"), role: s("role"), kind: s("kind"), data: v["data"].clone() });
        prev = sha(line);
    }
    Ok((out, prev))
}

/// Append one event. `head` is the hash of the last line (from `read`).
/// Returns the event and the new head hash.
pub fn append(path: &Path, head: &str, seq: u64, actor: &str, role: &str, kind: &str, data: Value) -> Res<(Event, String)> {
    let t = now();
    let line = json!({"seq": seq, "time": iso(t), "time_s": t, "actor": actor, "role": role,
                      "kind": kind, "data": data, "prev": head}).to_string();
    let created = !path.exists();
    let mut f = OpenOptions::new().create(true).append(true).open(path).map_err(|e| e.to_string())?;
    write_record(&mut f, &line).map_err(|e| e.to_string())?;
    f.sync_all().map_err(|e| e.to_string())?;
    if created {
        if let Some(dir) = path.parent() {
            if !dir.as_os_str().is_empty() {
                sync_dir(dir)?;
            }
        }
    }
    Ok((Event { seq, time: t, actor: actor.into(), role: role.into(), kind: kind.into(), data }, sha(&line)))
}

/// The JSON line and its trailing newline, as one buffer, so a short write cannot split them.
fn write_record(w: &mut impl Write, line: &str) -> std::io::Result<()> {
    let mut rec = String::with_capacity(line.len() + 1);
    rec.push_str(line);
    rec.push('\n');
    w.write_all(rec.as_bytes())
}

fn sync_dir(dir: &Path) -> Res<()> {
    #[cfg(test)]
    SYNC_DIR_COUNT.with(|n| n.set(n.get() + 1));
    let f = fs::File::open(dir).map_err(|e| format!("cannot sync {}: {e}", dir.display()))?;
    f.sync_all().map_err(|e| format!("cannot sync {}: {e}", dir.display()))
}

#[cfg(test)]
thread_local! {
    static SYNC_DIR_COUNT: std::cell::Cell<u32> = const { std::cell::Cell::new(0) };
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn iso_known_dates() {
        assert_eq!(iso(0), "1970-01-01T00:00:00Z");
        assert_eq!(iso(1_795_456_800), "2026-11-23T18:00:00Z");
    }

    #[test]
    fn read_names_a_torn_last_line_and_leaves_the_file() {
        let d = std::env::temp_dir().join(format!("wf-log-torn-{}", std::process::id()));
        let _ = fs::remove_dir_all(&d);
        fs::create_dir_all(&d).unwrap();
        let path = d.join("log.jsonl");
        let (e, head) = append(&path, "0", 1, "mat", "person", "init", serde_json::json!({"address": "p"})).unwrap();
        assert_eq!(e.seq, 1);
        let _ = append(&path, &head, 2, "pri", "prime", "face", serde_json::json!({"face": "01", "text": "Goal"})).unwrap();
        let before = fs::read(&path).unwrap();
        // cut the last line in half, the way an interrupted append looks
        let text = String::from_utf8(before.clone()).unwrap();
        let cut = text.rfind(',').unwrap();
        let torn = format!("{}\n", &text[..cut]);
        fs::write(&path, &torn).unwrap();
        let err = read(&path).unwrap_err();
        assert!(err.contains("last line is half written: entry 2; nothing was changed"), "{err}");
        assert_eq!(fs::read(&path).unwrap(), torn.as_bytes());
        let _ = fs::remove_dir_all(&d);
    }

    #[test]
    fn read_names_a_last_line_with_no_newline_and_leaves_the_file() {
        let d = std::env::temp_dir().join(format!("wf-log-nonewline-{}", std::process::id()));
        let _ = fs::remove_dir_all(&d);
        fs::create_dir_all(&d).unwrap();
        let path = d.join("log.jsonl");
        let (e, head) = append(&path, "0", 1, "mat", "person", "init", serde_json::json!({"address": "p"})).unwrap();
        assert_eq!(e.seq, 1);
        let _ = append(&path, &head, 2, "pri", "prime", "face", serde_json::json!({"face": "01", "text": "Goal"})).unwrap();
        let text = fs::read_to_string(&path).unwrap();
        assert!(text.ends_with('\n'), "{text:?}");
        let stripped = text.trim_end_matches('\n');
        fs::write(&path, stripped).unwrap();
        let err = read(&path).unwrap_err();
        assert!(err.contains("last line has no newline: entry 2; nothing was changed"), "{err}");
        assert_eq!(fs::read_to_string(&path).unwrap(), stripped);
        let _ = fs::remove_dir_all(&d);
    }

    #[test]
    fn write_record_sends_the_line_and_newline_in_one_write() {
        struct Count { buf: Vec<u8>, n: usize }
        impl Write for Count {
            fn write(&mut self, b: &[u8]) -> std::io::Result<usize> {
                self.n += 1;
                self.buf.extend_from_slice(b);
                Ok(b.len())
            }
            fn flush(&mut self) -> std::io::Result<()> { Ok(()) }
        }
        let mut c = Count { buf: vec![], n: 0 };
        write_record(&mut c, r#"{"seq":1}"#).unwrap();
        assert_eq!(c.n, 1);
        assert_eq!(c.buf, b"{\"seq\":1}\n");
    }

    #[test]
    fn append_syncs_the_page_folder_when_it_creates_the_log() {
        let d = std::env::temp_dir().join(format!("wf-log-dirsync-{}", std::process::id()));
        let _ = fs::remove_dir_all(&d);
        fs::create_dir_all(&d).unwrap();
        let path = d.join("log.jsonl");
        SYNC_DIR_COUNT.with(|n| n.set(0));
        let (_, head) = append(&path, "0", 1, "mat", "person", "init", serde_json::json!({"address": "p"})).unwrap();
        assert_eq!(SYNC_DIR_COUNT.with(|n| n.get()), 1);
        append(&path, &head, 2, "pri", "prime", "face", serde_json::json!({"face": "01", "text": "Goal"})).unwrap();
        assert_eq!(SYNC_DIR_COUNT.with(|n| n.get()), 1, "an existing log must not sync the folder again");
        let text = fs::read_to_string(&path).unwrap();
        assert!(text.ends_with('\n') && text.matches('\n').count() == 2, "{text:?}");
        let _ = fs::remove_dir_all(&d);
    }
}
