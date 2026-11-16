//! Read one face, or run the page and why checks.

use std::env;
use std::path::Path;
use std::process::ExitCode;

use seqbook::{page_gaps, why_gaps, Book};

fn main() -> ExitCode {
    let mut args = env::args().skip(1);
    match args.next().as_deref() {
        Some("read") => read(args.next(), args.next()),
        Some("check") => check(args.next()),
        _ => {
            eprintln!("usage: seqbook read <file> <address>");
            eprintln!("       seqbook check <file>");
            ExitCode::from(2)
        }
    }
}

fn read(file: Option<String>, addr: Option<String>) -> ExitCode {
    let (Some(file), Some(addr)) = (file, addr) else {
        eprintln!("usage: seqbook read <file> <address>");
        return ExitCode::from(2);
    };
    let book = match Book::load(Path::new(&file)) {
        Ok(book) => book,
        Err(err) => {
            eprintln!("{err}");
            return ExitCode::from(1);
        }
    };
    match book.face(&addr) {
        Ok(Some(face)) => {
            print!("{}", face.body);
            ExitCode::SUCCESS
        }
        Ok(None) => {
            eprintln!("missing {addr}");
            ExitCode::from(1)
        }
        Err(err) => {
            eprintln!("{err}");
            ExitCode::from(1)
        }
    }
}

fn check(file: Option<String>) -> ExitCode {
    let Some(file) = file else {
        eprintln!("usage: seqbook check <file>");
        return ExitCode::from(2);
    };
    let book = match Book::load(Path::new(&file)) {
        Ok(book) => book,
        Err(err) => {
            eprintln!("{err}");
            return ExitCode::from(1);
        }
    };
    let why = why_gaps(&book);
    let pages = page_gaps(&book);
    for gap in pages.iter().chain(why.hard.iter()) {
        eprintln!("hard: {gap}");
    }
    for finding in &why.findings {
        println!("finding: {finding}");
    }
    if pages.is_empty() && why.hard.is_empty() {
        println!("ok");
        ExitCode::SUCCESS
    } else {
        ExitCode::from(1)
    }
}
