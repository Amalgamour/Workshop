use std::env;
use std::path::Path;

use seqbook::{page_gaps, resolve, why_gaps, Address, Book, Context};

fn main() {
    let path = env::args().nth(1).expect("book");
    let book = Book::load(Path::new(&path)).expect("load");
    println!("book {} entries {}", book.address().canonical(), book.len());
    let mut page = String::new();
    for face in book.faces() {
        let Address::Page(parsed) = resolve(&face.key, &Context::empty()).expect("key") else {
            continue;
        };
        let page_key = format!("{}.{:04}", parsed.id.canonical(), parsed.page);
        if page_key != page {
            println!("\n{page_key}");
            page = page_key;
        }
        let head = face
            .body
            .lines()
            .find(|line| {
                line.starts_with("## ") || line.starts_with("title:") || line.starts_with("address:")
            })
            .unwrap_or("");
        let tail = face
            .tail
            .map(|t| t.to_string())
            .unwrap_or_else(|| "-".into());
        println!("  {} [{tail}] {head}", face.key);
    }
    let why = why_gaps(&book);
    println!("\nhard {}", why.hard.len());
    for gap in &why.hard {
        println!("  {gap}");
    }
    println!("findings {}", why.findings.len());
    for gap in &why.findings {
        println!("  {gap}");
    }
    let pages = page_gaps(&book);
    println!("shape {}", pages.len());
    for gap in &pages {
        println!("  {gap}");
    }
}
