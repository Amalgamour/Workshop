//! The seqAddr core: one address parser, one book log, one writer.
//!
//! The compute and the app are not in this crate. Append goes through
//! [`Writer`]. [`Book::load`] only reads, and a torn last line is dropped.

mod addr;
mod book;
mod check;

pub use addr::{resolve, Address, BookId, Context, Error, PageAddr, Tail};
pub use book::{read_writes, Book, FaceAt, FaceView, LogWrite, Writer};
pub use check::{page_gaps, why_gaps, WhyReport};
