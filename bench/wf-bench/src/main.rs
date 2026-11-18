use std::{env, process};

fn main() {
    let mut args = env::args().skip(1);
    let pages = match args.next() {
        Some(p) => p,
        None => {
            eprintln!("usage: wf-bench <pages-dir> <page>");
            process::exit(2);
        }
    };
    let page = match args.next() {
        Some(p) => p,
        None => {
            eprintln!("usage: wf-bench <pages-dir> <page>");
            process::exit(2);
        }
    };
    match wf_bench::run(&pages, &page) {
        Ok(text) => print!("{text}"),
        Err(e) => {
            eprintln!("wf-bench: {e}");
            process::exit(1);
        }
    }
}
