//! Page shape (C1) and the why rule (C3.2).
//!
//! Hard gaps are refusals. A 04 body that copies face 01 is a finding.

use std::collections::BTreeMap;

use crate::addr::{resolve, Address, Context};
use crate::book::Book;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct WhyReport {
    pub hard: Vec<String>,
    pub findings: Vec<String>,
}

struct Card {
    key: String,
    why: Option<String>,
    body: String,
}

/// Faces 01 and 02 need a 04 card with the same key, a why line, and a body.
pub fn why_gaps(book: &Book) -> WhyReport {
    let mut hard = Vec::new();
    let mut findings = Vec::new();
    for (page, faces) in pages(book) {
        let law = cards_on(&faces, 1);
        let schema = cards_on(&faces, 2);
        let user = cards_on(&faces, 4);
        for card in law.iter().chain(schema.iter()) {
            let Some(twin) = user.iter().find(|item| item.key == card.key) else {
                hard.push(format!(
                    "{page} card {} has no face 04 card",
                    card.key
                ));
                continue;
            };
            match &twin.why {
                Some(why) if !why.is_empty() => {}
                _ => hard.push(format!(
                    "{page} card {} has no why on face 04",
                    card.key
                )),
            }
            if twin.body.is_empty() {
                hard.push(format!(
                    "{page} card {} has no body on face 04",
                    card.key
                ));
            } else if law
                .iter()
                .any(|item| std::ptr::eq(item, card) && item.body == twin.body)
            {
                findings.push(format!(
                    "{page} card {} copies its face 01 body onto face 04",
                    card.key
                ));
            }
        }
    }
    WhyReport { hard, findings }
}

/// A page that has any face needs face 00 and one content face. Face 07 does not count.
pub fn page_gaps(book: &Book) -> Vec<String> {
    let mut gaps = Vec::new();
    for (page, faces) in pages(book) {
        if !faces_has(&faces, 0) {
            gaps.push(format!("{page} has no face 00"));
        }
        let content = faces.iter().any(|(face, _)| {
            (1..=6).contains(face) || *face == 8
        });
        if !content {
            gaps.push(format!("{page} has no content face"));
        }
    }
    gaps
}

fn pages(book: &Book) -> BTreeMap<String, Vec<(u8, String)>> {
    let mut pages: BTreeMap<String, Vec<(u8, String)>> = BTreeMap::new();
    for stored in book.faces() {
        let Ok(Address::Page(page)) = resolve(&stored.key, &Context::empty()) else {
            continue;
        };
        let Some(face) = page.face else {
            continue;
        };
        let id = format!("{}.{:04}", page.id.canonical(), page.page);
        pages.entry(id).or_default().push((face, stored.body));
    }
    pages
}

fn cards_on(faces: &[(u8, String)], face: u8) -> Vec<Card> {
    faces
        .iter()
        .filter(|(number, _)| *number == face)
        .flat_map(|(_, body)| parse_cards(body))
        .collect()
}

fn faces_has(faces: &[(u8, String)], face: u8) -> bool {
    faces.iter().any(|(number, _)| *number == face)
}

fn parse_cards(body: &str) -> Vec<Card> {
    let lines: Vec<&str> = body
        .split('\n')
        .map(|line| line.strip_suffix('\r').unwrap_or(line))
        .collect();
    let mut cards = Vec::new();
    let mut index = 0;
    while index < lines.len() {
        let Some(heading) = lines[index].strip_prefix("## ") else {
            index += 1;
            continue;
        };
        index += 1;
        let mut why = None;
        while index < lines.len()
            && !lines[index].is_empty()
            && !lines[index].starts_with("## ")
        {
            if let Some((name, value)) = field(lines[index]) {
                if name == "why" {
                    why = Some(value);
                }
                index += 1;
            } else {
                break;
            }
        }
        let mut body_lines = Vec::new();
        if index < lines.len() && lines[index].is_empty() {
            index += 1;
            while index < lines.len() && !lines[index].starts_with("## ") {
                body_lines.push(lines[index]);
                index += 1;
            }
        }
        cards.push(Card {
            key: title_key(heading),
            why,
            body: body_lines.join("\n").trim().to_string(),
        });
    }
    cards
}

fn field(line: &str) -> Option<(String, String)> {
    let (name, value) = line.split_once(':')?;
    if name.is_empty() || !name.chars().next()?.is_ascii_alphabetic() {
        return None;
    }
    if !name
        .chars()
        .all(|ch| ch.is_ascii_alphanumeric() || ch == '-')
    {
        return None;
    }
    Some((name.to_ascii_lowercase(), value.trim().to_string()))
}

fn title_key(heading: &str) -> String {
    let mut key = String::new();
    let mut hyphen = false;
    for ch in heading.trim().chars() {
        if ch.is_ascii_alphanumeric() {
            key.push(ch.to_ascii_lowercase());
            hyphen = false;
        } else if !hyphen && !key.is_empty() {
            key.push('-');
            hyphen = true;
        }
    }
    while key.ends_with('-') {
        key.pop();
    }
    key
}
