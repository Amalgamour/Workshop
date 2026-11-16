//! `seqpage export` prints one page. `seqpage check` compares a view to its book.

use std::env;
use std::fs;
use std::path::Path;
use std::process::ExitCode;

fn main() -> ExitCode {
    let mut args = env::args().skip(1);
    match args.next().as_deref() {
        Some("export") => {
            let Some(book) = args.next() else { return usage() };
            let Some(page) = args.next() else { return usage() };
            match seqpage::export(Path::new(&book), &page) {
                Ok(text) => {
                    if let Some(out) = take(&mut args, "--out") {
                        if let Err(err) = fs::write(&out, text) {
                            eprintln!("{err}");
                            return ExitCode::from(1);
                        }
                        println!("{{\"ok\": true, \"file\": \"{out}\"}}");
                    } else {
                        print!("{text}");
                    }
                    ExitCode::SUCCESS
                }
                Err(err) => {
                    eprintln!("{err}");
                    ExitCode::from(1)
                }
            }
        }
        Some("check") => {
            let Some(file) = args.next() else { return usage() };
            let Some(book) = take(&mut args, "--book") else { return usage() };
            let text = match fs::read_to_string(&file) {
                Ok(text) => text,
                Err(err) => {
                    eprintln!("{err}");
                    return ExitCode::from(1);
                }
            };
            match seqpage::check(&text, Path::new(&book)) {
                Ok(faults) => {
                    let mut faults = faults;
                    faults.extend(seqpage::check_name(
                        Path::new(&file)
                            .file_name()
                            .and_then(|name| name.to_str())
                            .unwrap_or(&file),
                        &text,
                    ));
                    if faults.is_empty() {
                        println!("{{\"ok\": true}}");
                        ExitCode::SUCCESS
                    } else {
                        println!("{{\"ok\": false}}");
                        for fault in faults {
                            println!("line {}: {}", fault.line, fault.detail);
                        }
                        ExitCode::from(1)
                    }
                }
                Err(err) => {
                    eprintln!("{err}");
                    ExitCode::from(1)
                }
            }
        }
        _ => usage(),
    }
}

fn take(args: &mut impl Iterator<Item = String>, flag: &str) -> Option<String> {
    let next = args.next()?;
    if next == flag { args.next() } else { None }
}

fn usage() -> ExitCode {
    eprintln!("usage: seqpage export <book> <page> [--out <file>]");
    eprintln!("       seqpage check <file> --book <book>");
    ExitCode::from(2)
}
