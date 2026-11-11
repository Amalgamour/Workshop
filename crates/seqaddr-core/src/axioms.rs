//! Axiom chains (Axioms.md; decision E3). A chain is never an address.
//!
//! `1.7.8` orders axioms in one piece; `1,3` splits pieces; only axiom 3 takes
//! a modifier of one to three distinct letters from M, P, C (`3MPC`).

use crate::error::{Result, SeqError};
use serde::Serialize;

/// One cited axiom, with the lead letters if it is axiom 3.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AxiomRef {
    pub n: u8,
    /// Lead letters for axiom 3, in order (`M`, `P`, `C`).
    pub leads: Vec<char>,
}

/// A parsed chain: pieces (split by comma), each an ordered list (split by dot).
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AxiomChain {
    pub pieces: Vec<Vec<AxiomRef>>,
}

pub const AXIOM_NAMES: [&str; 9] = ["Authority", "Fractal", "Leads", "Why", "Frame", "Lineage", "Missing", "Connection", "Trial"];

pub fn axiom_name(n: u8) -> Option<&'static str> {
    if (1..=9).contains(&n) {
        Some(AXIOM_NAMES[(n - 1) as usize])
    } else {
        None
    }
}

/// The cold set before a write (E3): `1.7.8`.
pub const COLD_SET: &str = "1.7.8";

impl AxiomChain {
    pub fn parse(s: &str) -> Result<AxiomChain> {
        let s = s.trim();
        if s.is_empty() {
            return Err(SeqError::invalid("E3", "empty axiom chain"));
        }
        let mut pieces = Vec::new();
        for piece in s.split(',') {
            let piece = piece.trim();
            if piece.is_empty() {
                return Err(SeqError::invalid("E3", format!("`{s}`: empty piece between commas")));
            }
            let mut refs = Vec::new();
            for part in piece.split('.') {
                let mut ch = part.chars();
                let d = ch.next().ok_or_else(|| SeqError::invalid("E3", format!("`{s}`: empty step between dots")))?;
                let n = d
                    .to_digit(10)
                    .filter(|n| (1..=9).contains(n))
                    .ok_or_else(|| SeqError::invalid("E3", format!("`{part}` in `{s}`: an axiom is one digit 1-9")))? as u8;
                let leads: Vec<char> = ch.collect();
                if !leads.is_empty() {
                    if n != 3 {
                        return Err(SeqError::invalid("E3", format!("`{part}` in `{s}`: only axiom 3 takes a modifier")));
                    }
                    if leads.len() > 3 || leads.iter().any(|c| !matches!(c, 'M' | 'P' | 'C')) {
                        return Err(SeqError::invalid("E3", format!("`{part}` in `{s}`: lead letters are one to three of M, P, C")));
                    }
                    let mut seen = leads.clone();
                    seen.sort();
                    seen.dedup();
                    if seen.len() != leads.len() {
                        return Err(SeqError::invalid("E3", format!("`{part}` in `{s}`: lead letters must be distinct")));
                    }
                }
                refs.push(AxiomRef { n, leads });
            }
            pieces.push(refs);
        }
        Ok(AxiomChain { pieces })
    }

    /// Plain words for a chain, e.g. `7.8` -> "Missing > Connection".
    pub fn describe(&self) -> String {
        self.pieces
            .iter()
            .map(|p| {
                p.iter()
                    .map(|r| {
                        let name = axiom_name(r.n).unwrap_or("?");
                        if r.leads.is_empty() {
                            name.to_string()
                        } else {
                            format!("{name}({})", r.leads.iter().collect::<String>())
                        }
                    })
                    .collect::<Vec<_>>()
                    .join(" > ")
            })
            .collect::<Vec<_>>()
            .join(", ")
    }
}

impl std::fmt::Display for AxiomChain {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = self
            .pieces
            .iter()
            .map(|p| p.iter().map(|r| format!("{}{}", r.n, r.leads.iter().collect::<String>())).collect::<Vec<_>>().join("."))
            .collect::<Vec<_>>()
            .join(",");
        f.write_str(&s)
    }
}
