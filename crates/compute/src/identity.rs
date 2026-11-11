//! Who is writing (TRIAL-X #1, #3, #4, #6). Provisional design, 7 until the
//! Director confirms it (BUILD-LOG `[COMPUTE]`):
//! - a local file `books/.identities` (gitignored, made by scripts/dev.sh if
//!   missing) maps secret tokens to names: `NAME TOKEN` per line, `#` comments;
//! - every write carries `Authorization: Bearer TOKEN` (or `X-Seq-Token`); the
//!   compute sets `by` from the token and ignores the body's `by`;
//! - only the `director` token may record `approved_by: director`;
//! - `compute` is internal only: a client presenting it is refused;
//! - names are exact: lowercase letters, digits and hyphens, no whitespace.

use std::collections::BTreeMap;
use std::path::Path;

pub const DIRECTOR: &str = "director";
pub const COMPUTE: &str = "compute";

#[derive(Debug, Clone, Default)]
pub struct Identities {
    by_token: BTreeMap<String, String>,
    pub source: Option<String>,
}

pub fn valid_name(n: &str) -> bool {
    !n.is_empty() && n.len() <= 64 && n.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-') && !n.starts_with('-')
}

fn valid_token(t: &str) -> bool {
    t.len() >= 8 && t.len() <= 256 && t.bytes().all(|b| (0x21..=0x7e).contains(&b))
}

impl Identities {
    pub fn parse(text: &str) -> Result<Identities, String> {
        let mut by_token = BTreeMap::new();
        for (i, raw) in text.lines().enumerate() {
            let l = raw.trim_end_matches('\r');
            if l.trim().is_empty() || l.trim_start().starts_with('#') {
                continue;
            }
            let mut parts = l.split(' ');
            let (Some(name), Some(token), None) = (parts.next(), parts.next(), parts.next()) else {
                return Err(format!("line {}: write `NAME TOKEN` separated by one space", i + 1));
            };
            if !valid_name(name) {
                return Err(format!("line {}: name `{name}` must be lowercase letters, digits and hyphens", i + 1));
            }
            if !valid_token(token) {
                return Err(format!("line {}: token for `{name}` must be 8-256 printable characters, no spaces", i + 1));
            }
            if by_token.insert(token.to_string(), name.to_string()).is_some() {
                return Err(format!("line {}: the same token is given twice", i + 1));
            }
        }
        Ok(Identities { by_token, source: None })
    }
    pub fn load(path: &Path) -> Result<Identities, String> {
        let text = std::fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
        let mut ids = Identities::parse(&text).map_err(|e| format!("{}: {e}", path.display()))?;
        ids.source = Some(path.display().to_string());
        Ok(ids)
    }
    pub fn from_pairs<'a>(pairs: impl IntoIterator<Item = (&'a str, &'a str)>) -> Identities {
        Identities { by_token: pairs.into_iter().map(|(n, t)| (t.to_string(), n.to_string())).collect(), source: Some("in memory".into()) }
    }
    pub fn is_empty(&self) -> bool {
        self.by_token.is_empty()
    }
    pub fn names(&self) -> Vec<String> {
        let mut v: Vec<String> = self.by_token.values().cloned().collect();
        v.sort();
        v
    }
    /// The name for a token presented by a client (never `compute`).
    pub fn who(&self, token: &str) -> Result<String, (u16, &'static str, String)> {
        match self.by_token.get(token) {
            None => Err((401, "identity", "unknown token: every write carries `Authorization: Bearer TOKEN` from books/.identities".into())),
            Some(n) if n == COMPUTE => Err((403, "authority", "`compute` is internal; no client may write as the compute (format.md 3.3, C8.7)".into())),
            Some(n) => Ok(n.clone()),
        }
    }
}
