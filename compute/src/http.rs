//! A small local HTTP server so a browser can ask the compute.
//! This is a trial for one machine. It does not settle HTTP, MCP, or both.

use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::path::Path;
use std::time::Duration;

use seqbook::Book;

use crate::{catalog, page_title, propose_sentence, read_face, Proposal, Verdict};

pub struct Reply {
    pub status: u16,
    pub body: String,
}

pub fn reply(book: &Path, method: &str, target: &str, body: &str) -> Reply {
    if method == "OPTIONS" {
        return Reply {
            status: 204,
            body: String::new(),
        };
    }
    let (path, query) = target.split_once('?').unwrap_or((target, ""));
    match (method, path) {
        ("GET", "/health") => Reply {
            status: 200,
            body: "ok\n".to_string(),
        },
        ("GET", "/seq") => seq_view(book, query),
        ("GET", "/book") => match Book::load(book) {
            Ok(loaded) => Reply {
                status: 200,
                body: catalog(&loaded),
            },
            Err(err) => Reply {
                status: 400,
                body: format!("decision: refuse\n{err}\n"),
            },
        },
        ("GET", "/face") => face(book, query),
        ("POST", "/propose") => propose(book, body),
        ("GET", _) | ("POST", _) => Reply {
            status: 404,
            body: "decision: refuse\nreason: unknown path\n".to_string(),
        },
        _ => Reply {
            status: 405,
            body: "decision: refuse\nreason: this trial serves GET and POST\n".to_string(),
        },
    }
}

pub fn proposal_text(proposal: &Proposal) -> String {
    let title = proposal
        .title
        .as_deref()
        .map(|title| format!("title: {title}\n"))
        .unwrap_or_default();
    let mut out = format!(
        "proposer: {}\nThis proposer is local. It is not a remote model.\naddr: {}\n{title}{}\n",
        proposal.proposer, proposal.addr, proposal.body
    );
    match &proposal.verdict {
        Verdict::Accept { len } => {
            out.push_str(&format!("decision: accept\nlen: {len}\n"));
        }
        Verdict::Refuse { reasons } => {
            out.push_str("decision: refuse\n");
            for reason in reasons {
                out.push_str(&format!("reason: {reason}\n"));
            }
        }
        Verdict::Read { .. } => {
            out.push_str("decision: refuse\nreason: a proposal returned a read\n");
        }
    }
    out
}

pub fn serve(book: &Path, port: u16) -> std::io::Result<()> {
    let listener = TcpListener::bind(("127.0.0.1", port))?;
    eprintln!("compute listening on {}", listener.local_addr()?);
    serve_listener(book, listener)
}

pub fn serve_listener(book: &Path, listener: TcpListener) -> std::io::Result<()> {
    for stream in listener.incoming() {
        match stream {
            Ok(mut stream) => {
                let _ = stream.set_read_timeout(Some(Duration::from_secs(2)));
                let _ = handle(&mut stream, book);
            }
            Err(err) => eprintln!("{err}"),
        }
    }
    Ok(())
}

fn seq_view(book: &Path, query: &str) -> Reply {
    let Some(page) = query_value(query, "page") else {
        return Reply {
            status: 400,
            body: "decision: refuse\nreason: page is required\n".to_string(),
        };
    };
    match seqpage::export(book, &page) {
        Ok(text) => Reply {
            status: 200,
            body: text,
        },
        Err(err) => Reply {
            status: 400,
            body: format!("decision: refuse\n{err}\n"),
        },
    }
}

fn propose(book: &Path, sentence: &str) -> Reply {
    match propose_sentence(book, sentence) {
        Ok(proposal) => {
            let status = if matches!(proposal.verdict, Verdict::Accept { .. }) {
                200
            } else {
                409
            };
            Reply {
                status,
                body: proposal_text(&proposal),
            }
        }
        Err(err) => Reply {
            status: 400,
            body: format!("decision: refuse\n{err}\n"),
        },
    }
}

fn face(book: &Path, query: &str) -> Reply {
    let Some(addr) = query_value(query, "addr") else {
        return Reply {
            status: 400,
            body: "decision: refuse\nreason: addr is required\n".to_string(),
        };
    };
    let heading = title_line(book, &addr);
    match read_face(book, &addr) {
        Ok(Verdict::Read { body }) => Reply {
            status: 200,
            body: format!("decision: read\n{heading}{body}"),
        },
        Ok(Verdict::Refuse { reasons }) => Reply {
            status: 404,
            body: format!("decision: refuse\n{heading}{}", reasons.join("\n")),
        },
        Ok(Verdict::Accept { .. }) => Reply {
            status: 500,
            body: "decision: refuse\nreason: a read returned a write\n".to_string(),
        },
        Err(err) => Reply {
            status: 400,
            body: format!("decision: refuse\n{err}\n"),
        },
    }
}

fn title_line(book: &Path, addr: &str) -> String {
    let Ok(loaded) = Book::load(book) else {
        return String::new();
    };
    match page_title(&loaded, addr) {
        Ok(Some(title)) => format!("title: {title}\n"),
        _ => String::new(),
    }
}

fn query_value(query: &str, key: &str) -> Option<String> {
    for pair in query.split('&') {
        let (name, value) = pair.split_once('=').unwrap_or((pair, ""));
        if decode(name) == key {
            return Some(decode(value));
        }
    }
    None
}

fn decode(input: &str) -> String {
    let bytes = input.as_bytes();
    let mut out = Vec::with_capacity(bytes.len());
    let mut index = 0;
    while index < bytes.len() {
        if bytes[index] == b'%' && index + 2 < bytes.len() {
            let hex = std::str::from_utf8(&bytes[index + 1..index + 3]).unwrap_or("");
            if let Ok(value) = u8::from_str_radix(hex, 16) {
                out.push(value);
                index += 3;
                continue;
            }
        }
        if bytes[index] == b'+' {
            out.push(b' ');
        } else {
            out.push(bytes[index]);
        }
        index += 1;
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn handle(stream: &mut TcpStream, book: &Path) -> std::io::Result<()> {
    let mut buf = [0u8; 8192];
    let read = stream.read(&mut buf)?;
    let text = String::from_utf8_lossy(&buf[..read]);
    let (head, payload) = text.split_once("\r\n\r\n").unwrap_or((text.as_ref(), ""));
    let line = head.lines().next().unwrap_or("");
    let mut parts = line.split_whitespace();
    let method = parts.next().unwrap_or("");
    let target = parts.next().unwrap_or("/");
    let reply = reply(book, method, target, payload);
    write_reply(stream, &reply)
}

fn write_reply(stream: &mut TcpStream, reply: &Reply) -> std::io::Result<()> {
    let reason = match reply.status {
        200 => "OK",
        204 => "No Content",
        400 => "Bad Request",
        404 => "Not Found",
        405 => "Method Not Allowed",
        409 => "Conflict",
        _ => "Error",
    };
    let head = format!(
        "HTTP/1.1 {} {}\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: {}\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type\r\nConnection: close\r\n\r\n",
        reply.status,
        reason,
        reply.body.len()
    );
    stream.write_all(head.as_bytes())?;
    stream.write_all(reply.body.as_bytes())?;
    stream.flush()
}
