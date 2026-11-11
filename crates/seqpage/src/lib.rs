//! # seqpage — the `.seq` page file
//!
//! One plain-text file holds one multifaceted page (Director ruling R3).
//! The book (JSON Lines log, docs/spec/format.md) is the real stored copy;
//! a `.seq` file is a **view**: exported from a book, imported back as a
//! **proposal** that goes through the compute's queue. Nothing here writes
//! a book.
//!
//! Layout and grammar: docs/spec/seqpage.md. Section numbers in error
//! rules (`seqpage 6.2`) point there.

pub mod derive;
pub mod error;
pub mod face00;
pub mod import;
pub mod model;
pub mod parse;
pub mod rulings;
pub mod text;
pub mod write;

pub use error::{PageError, Report};
pub use import::{import, Imported};
pub use model::{page_entries, pages_in, slot_of, Block, BlockKind, Derived, HistLine, PageId, Section, SectionKey, SeqPage};
pub use parse::{check_text, parse};
pub use write::{export, file_name, render};

/// First line of every `.seq` file.
pub const MAGIC: &str = "seqpage 1";
/// File extension.
pub const EXT: &str = "seq";
