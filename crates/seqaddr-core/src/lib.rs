//! # seqaddr-core
//!
//! The core of the Workshop design (docs/spec): the seqAddr address grammar,
//! the book file (JSON Lines append-only log), tail rules, the inheritance
//! resolver and proposal validation. One implementation, shared by the
//! compute and (as WebAssembly) the app (format 5).
//!
//! The spec governs. Choices the spec does not settle are marked `7` in
//! docs/BUILD-LOG.md and are switchable through [`state::Policy`].
//! See `API.md` for the public API.

pub mod addr;
pub mod axioms;
pub mod cards;
pub mod error;
pub mod face;
pub mod log;
pub mod resolve;
pub mod state;
pub mod tail;
pub mod validate;

pub use addr::{Active, Address, BookId, ContainerAddr, FacePart, Form, PageAddr, Tail};
pub use axioms::AxiomChain;
pub use error::{Result, SeqError};
pub use log::{BookLog, Entry, Header, Op};
pub use resolve::{Origin, Resolution, World};
pub use state::{BookState, Policy};
pub use tail::CounterTail;
pub use validate::{validate, OpRequest, Outcome, Proposal, Reason, Status};
