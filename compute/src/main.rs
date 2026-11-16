//! `compute read` and `compute put`. A refusal leaves the book unchanged.

use std::env;
use std::path::Path;
use std::process::ExitCode;

use compute::Verdict;

fn main() -> ExitCode {
    let mut args = env::args().skip(1);
    let book = match take(&mut args, "--book") {
        Some(path) => path,
        None => return usage(),
    };
    match args.next().as_deref() {
        Some("read") => {
            let Some(addr) = args.next() else {
                return usage();
            };
            match compute::read_face(Path::new(&book), &addr) {
                Ok(Verdict::Read { body }) => {
                    println!("decision: read");
                    print!("{body}");
                    ExitCode::SUCCESS
                }
                Ok(Verdict::Refuse { reasons }) => refuse(&reasons),
                Ok(Verdict::Accept { .. }) => ExitCode::from(1),
                Err(err) => {
                    eprintln!("{err}");
                    ExitCode::from(1)
                }
            }
        }
        Some("serve") => {
            let port = take(&mut args, "--port")
                .and_then(|value| value.parse().ok())
                .unwrap_or(7040);
            match compute::http::serve(Path::new(&book), port) {
                Ok(()) => ExitCode::SUCCESS,
                Err(err) => {
                    eprintln!("{err}");
                    ExitCode::from(1)
                }
            }
        }
        Some("put") => {
            let Some(addr) = take(&mut args, "--addr") else {
                return usage();
            };
            let Some(at) = take(&mut args, "--at") else {
                return usage();
            };
            let Some(by) = take(&mut args, "--by") else {
                return usage();
            };
            let Some(body) = take(&mut args, "--body") else {
                return usage();
            };
            match compute::propose_put(Path::new(&book), &at, &by, &addr, &body) {
                Ok(Verdict::Accept { len }) => {
                    println!("decision: accept");
                    println!("len: {len}");
                    ExitCode::SUCCESS
                }
                Ok(Verdict::Refuse { reasons }) => refuse(&reasons),
                Ok(Verdict::Read { .. }) => ExitCode::from(1),
                Err(err) => {
                    eprintln!("{err}");
                    ExitCode::from(1)
                }
            }
        }
        _ => usage(),
    }
}

fn refuse(reasons: &[String]) -> ExitCode {
    println!("decision: refuse");
    for reason in reasons {
        println!("reason: {reason}");
    }
    ExitCode::from(1)
}

fn take(args: &mut impl Iterator<Item = String>, flag: &str) -> Option<String> {
    let next = args.next()?;
    if next == flag {
        args.next()
    } else if flag == "--book" {
        Some(next)
    } else {
        None
    }
}

fn usage() -> ExitCode {
    eprintln!("usage: compute --book <file> read <address>");
    eprintln!("       compute --book <file> put --addr <address> --at <time> --by <who> --body <text>");
    eprintln!("       compute --book <file> serve --port <port>");
    ExitCode::from(2)
}
