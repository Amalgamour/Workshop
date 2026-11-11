//! Errors and findings. Every one cites the `seqpage.md` section it enforces
//! and, where one applies, the axiom it stands on (docs/spec/Axioms.md).

use serde::Serialize;

/// One error or finding. `line` is 1-based; 0 means the whole file.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PageError {
    pub line: usize,
    /// `invalid`, `missing`, `conflict`, `lineage`, `connection`, `authority`, `elevate`.
    pub code: &'static str,
    /// Axiom chain cited: `7` missing, `1` authority/conflict, `6` lineage, `8` connection, `7.8` a connection that is missing.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub axiom: Option<&'static str>,
    pub rule: &'static str,
    pub detail: String,
}

impl PageError {
    fn mk(line: usize, code: &'static str, axiom: Option<&'static str>, rule: &'static str, detail: impl Into<String>) -> Self {
        PageError { line, code, axiom, rule, detail: detail.into() }
    }
    /// Not well formed. No axiom: grammar.
    pub fn invalid(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "invalid", None, rule, d)
    }
    /// Something required is not there (axiom 7). Never guessed.
    pub fn missing(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "missing", Some("7"), rule, d)
    }
    /// A connection that cannot be opened (axiom chain 7.8).
    pub fn missing_link(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "missing", Some("7.8"), rule, d)
    }
    /// Two claims on one place (axiom 1).
    pub fn conflict(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "conflict", Some("1"), rule, d)
    }
    /// The past rewritten or reordered (axiom 6).
    pub fn lineage(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "lineage", Some("6"), rule, d)
    }
    /// A piece not where its address says, or a copy that disagrees with its source (axiom 8).
    pub fn connection(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "connection", Some("8"), rule, d)
    }
    /// A writer claiming what only the compute stamps (axiom 1).
    pub fn authority(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "authority", Some("1"), rule, d)
    }
    /// Goes to the user, never guessed (A2.8 title mismatch).
    pub fn elevate(line: usize, rule: &'static str, d: impl Into<String>) -> Self {
        Self::mk(line, "elevate", None, rule, d)
    }
}

impl std::fmt::Display for PageError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.line > 0 {
            write!(f, "line {}: ", self.line)?;
        }
        write!(f, "{} ({}", self.code, self.rule)?;
        if let Some(a) = self.axiom {
            write!(f, ", axiom {a}")?;
        }
        write!(f, "): {}", self.detail)
    }
}

impl std::error::Error for PageError {}

/// Result of a check: errors stop an import; findings are reported only.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize)]
pub struct Report {
    pub ok: bool,
    pub errors: Vec<PageError>,
    pub findings: Vec<PageError>,
}

impl Report {
    pub fn new(errors: Vec<PageError>, findings: Vec<PageError>) -> Self {
        Report { ok: errors.is_empty(), errors, findings }
    }
}
