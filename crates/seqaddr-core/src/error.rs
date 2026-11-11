//! Typed errors. Every error names the spec rule it enforces and, where the
//! spec gives one, the axiom (`7` missing, `1` conflict).

use serde::Serialize;
use thiserror::Error;

/// One error from the core. `rule` is the spec section or decision id
/// (for example `A1.5` or `format 3.1`).
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize)]
#[serde(tag = "error", rename_all = "snake_case")]
pub enum SeqError {
    /// The text is not a well formed address or value.
    #[error("invalid ({rule}): {detail}")]
    Invalid { rule: &'static str, detail: String },
    /// Something required is not there. Axiom 7: never guessed.
    #[error("missing ({rule}, axiom 7): {detail}")]
    Missing { rule: &'static str, detail: String },
    /// Two live claims with no lawful connection. Axiom 1: halt.
    #[error("conflict ({rule}, axiom 1): {detail}")]
    Conflict { rule: &'static str, detail: String },
    /// The compute cannot decide; goes to the user, never guessed.
    #[error("elevate ({rule}): {detail}")]
    Elevate { rule: &'static str, detail: String },
    /// A write breaks a rule (proposal validation, tail move, drafting).
    #[error("rejected ({rule}): {detail}")]
    Rejected { rule: &'static str, detail: String },
    /// A book file is damaged before its last line (format 3.1).
    #[error("corrupt book at line {line}: {detail}")]
    Corrupt { line: usize, detail: String },
    /// File system error (feature `fs`).
    #[error("io: {detail}")]
    Io { detail: String },
}

impl SeqError {
    pub fn invalid(rule: &'static str, detail: impl Into<String>) -> Self {
        SeqError::Invalid { rule, detail: detail.into() }
    }
    pub fn missing(rule: &'static str, detail: impl Into<String>) -> Self {
        SeqError::Missing { rule, detail: detail.into() }
    }
    pub fn conflict(rule: &'static str, detail: impl Into<String>) -> Self {
        SeqError::Conflict { rule, detail: detail.into() }
    }
    pub fn elevate(rule: &'static str, detail: impl Into<String>) -> Self {
        SeqError::Elevate { rule, detail: detail.into() }
    }
    pub fn rejected(rule: &'static str, detail: impl Into<String>) -> Self {
        SeqError::Rejected { rule, detail: detail.into() }
    }

    /// Short machine code, matching the lane contract error codes.
    pub fn code(&self) -> &'static str {
        match self {
            SeqError::Invalid { .. } => "invalid",
            SeqError::Missing { .. } => "missing",
            SeqError::Conflict { .. } => "conflict",
            SeqError::Elevate { .. } => "elevate",
            SeqError::Rejected { .. } => "rejected",
            SeqError::Corrupt { .. } => "corrupt",
            SeqError::Io { .. } => "io",
        }
    }

    /// The axiom this error stands on, if any.
    pub fn axiom(&self) -> Option<&'static str> {
        match self {
            SeqError::Missing { .. } => Some("7"),
            SeqError::Conflict { .. } => Some("1"),
            _ => None,
        }
    }

    /// The spec rule cited.
    pub fn rule(&self) -> &'static str {
        match self {
            SeqError::Invalid { rule, .. }
            | SeqError::Missing { rule, .. }
            | SeqError::Conflict { rule, .. }
            | SeqError::Elevate { rule, .. }
            | SeqError::Rejected { rule, .. } => rule,
            SeqError::Corrupt { .. } => "format 3.1",
            SeqError::Io { .. } => "io",
        }
    }

    /// Suggested HTTP status for the compute (lane contract).
    pub fn http_status(&self) -> u16 {
        match self {
            SeqError::Missing { .. } => 404,
            SeqError::Conflict { .. } => 409,
            SeqError::Invalid { .. } | SeqError::Rejected { .. } => 422,
            SeqError::Elevate { .. } => 300,
            SeqError::Corrupt { .. } | SeqError::Io { .. } => 500,
        }
    }

    pub fn detail(&self) -> String {
        match self {
            SeqError::Invalid { detail, .. }
            | SeqError::Missing { detail, .. }
            | SeqError::Conflict { detail, .. }
            | SeqError::Elevate { detail, .. }
            | SeqError::Rejected { detail, .. }
            | SeqError::Corrupt { detail, .. }
            | SeqError::Io { detail } => detail.clone(),
        }
    }
}

pub type Result<T> = std::result::Result<T, SeqError>;
