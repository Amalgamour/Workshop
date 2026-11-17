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
    let mut prev = "0".to_string();
    let mut out = Vec::new();
    for (i, line) in text.lines().enumerate() {
        let v: Value = serde_json::from_str(line).map_err(|e| format!("log line {} is not JSON: {e}", i + 1))?;
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
    let mut f = OpenOptions::new().create(true).append(true).open(path).map_err(|e| e.to_string())?;
    writeln!(f, "{line}").map_err(|e| e.to_string())?;
    Ok((Event { seq, time: t, actor: actor.into(), role: role.into(), kind: kind.into(), data }, sha(&line)))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn iso_known_dates() {
        assert_eq!(iso(0), "1970-01-01T00:00:00Z");
        assert_eq!(iso(1_795_456_800), "2026-11-23T18:00:00Z");
    }
}
