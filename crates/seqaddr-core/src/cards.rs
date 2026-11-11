//! Cards inside a face's Markdown (seqAddr 5.3; C2; C8.9) and the page stamp (A4.2).
//!
//! A card is a `##` heading. Field lines (`name: value`) follow the heading,
//! then a blank line, then the body. The key is the heading in title form.

use crate::addr::{is_tail_word, is_word};
use crate::error::{Result, SeqError};
use serde::Serialize;

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Card {
    /// The heading as written (`Retry Policy`).
    pub heading: String,
    /// The key in title form (`retry-policy`).
    pub key: String,
    /// Field lines in order.
    pub fields: Vec<(String, String)>,
    /// The body after the fields.
    pub body: String,
}

impl Card {
    pub fn field(&self, name: &str) -> Option<&str> {
        self.fields.iter().find(|(k, _)| k == name).map(|(_, v)| v.as_str())
    }
    /// The card's type: its `type:` field, else the face default (C8.9).
    pub fn card_type(&self, face: u8) -> Option<String> {
        self.field("type").map(|s| s.to_string()).or_else(|| crate::face::default_card_type(face).map(|s| s.to_string()))
    }
}

/// A face body split into cards.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct FaceDoc {
    /// Text before the first card.
    pub preamble: String,
    pub cards: Vec<Card>,
}

impl FaceDoc {
    pub fn card(&self, key: &str) -> Option<&Card> {
        self.cards.iter().find(|c| c.key == key)
    }
    /// The derived contents list: card keys in order (C2).
    pub fn contents(&self) -> Vec<String> {
        self.cards.iter().map(|c| c.key.clone()).collect()
    }
}

/// Heading -> key in title form (C2: `Retry Policy` -> `retry-policy`).
///
/// Provisional (BUILD-LOG `7`): characters other than letters and digits
/// become one hyphen; leading and trailing hyphens are dropped.
pub fn title_form(heading: &str) -> Result<String> {
    let mut out = String::new();
    let mut dash = false;
    for c in heading.trim().chars() {
        if c.is_ascii_alphanumeric() {
            if dash && !out.is_empty() {
                out.push('-');
            }
            dash = false;
            out.push(c.to_ascii_lowercase());
        } else {
            dash = true;
        }
    }
    if !is_word(&out) {
        return Err(SeqError::invalid("C2", format!("heading `{heading}` has no title-form key (must start with a letter)")));
    }
    if is_tail_word(&out) {
        return Err(SeqError::invalid("A2.5", format!("heading `{heading}`: `{out}` is a tail word and cannot be a card key")));
    }
    Ok(out)
}

fn parse_field(line: &str) -> Option<(String, String)> {
    let (k, v) = line.split_once(':')?;
    let k = k.trim_end();
    if k.is_empty() || !k.chars().next().unwrap().is_ascii_lowercase() {
        return None;
    }
    if !k.chars().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-' || c == '_' || c == ' ') {
        return None;
    }
    Some((k.to_string(), v.trim().to_string()))
}

/// Split a face body into cards. Duplicate keys in one face are rejected (C2).
pub fn parse_face(body: &str) -> Result<FaceDoc> {
    let mut preamble = String::new();
    let mut cards: Vec<Card> = Vec::new();
    let mut in_fence = false;
    // state for the current card
    let mut in_fields = false;
    for line in body.lines() {
        let trimmed = line.trim_start();
        if trimmed.starts_with("```") || trimmed.starts_with("~~~") {
            in_fence = !in_fence;
        }
        if !in_fence && line.starts_with("## ") {
            let heading = line[3..].trim().to_string();
            let key = title_form(&heading)?;
            if cards.iter().any(|c| c.key == key) {
                return Err(SeqError::rejected("C2", format!("card key `{key}` appears twice in one face")));
            }
            cards.push(Card { heading, key, fields: Vec::new(), body: String::new() });
            in_fields = true;
            continue;
        }
        match cards.last_mut() {
            None => {
                preamble.push_str(line);
                preamble.push('\n');
            }
            Some(card) => {
                if in_fields {
                    if line.trim().is_empty() {
                        in_fields = false;
                        continue;
                    }
                    if let Some(f) = parse_field(line) {
                        card.fields.push(f);
                        continue;
                    }
                    in_fields = false;
                }
                card.body.push_str(line);
                card.body.push('\n');
            }
        }
    }
    for c in &mut cards {
        let t = c.body.trim_end().to_string();
        c.body = t;
    }
    Ok(FaceDoc { preamble, cards })
}

/// The page stamp held on face 00 (A4.2): address, title, state, type, axioms.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize)]
pub struct Stamp {
    pub fields: Vec<(String, String)>,
}

impl Stamp {
    pub fn get(&self, k: &str) -> Option<&str> {
        self.fields.iter().find(|(a, _)| a == k).map(|(_, v)| v.as_str())
    }
    pub fn title(&self) -> Option<&str> {
        self.get("title").filter(|s| !s.is_empty())
    }
    pub fn page_type(&self) -> Option<&str> {
        self.get("type")
    }
}

/// Read a stamp: either a `---` front-matter block (format 3.2 example) or
/// leading field lines up to the first blank line (provisional, BUILD-LOG).
pub fn parse_stamp(body: &str) -> Stamp {
    let mut fields = Vec::new();
    let mut lines = body.lines().peekable();
    let fenced = matches!(lines.peek(), Some(l) if l.trim() == "---");
    if fenced {
        lines.next();
    }
    for line in lines {
        if fenced && line.trim() == "---" {
            break;
        }
        if !fenced && line.trim().is_empty() {
            break;
        }
        if let Some(f) = parse_field(line) {
            fields.push(f);
        } else if !fenced {
            break;
        }
    }
    Stamp { fields }
}
