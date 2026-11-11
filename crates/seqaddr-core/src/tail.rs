//! Tail state machines (seqAddr 4, 5.7; A2.5; format 4.1; workflow-loop 6).

use crate::addr::Tail;
use crate::error::{Result, SeqError};
use serde::{Deserialize, Serialize};
use std::fmt;

/// The state of a counter. `Closed` is the bare counter: no `.closed` tail (A2.5, S03).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum CounterTail {
    Draft,
    Pack,
    Open,
    Return,
    Review,
    Closed,
}

impl CounterTail {
    /// From an optional written tail: `None` is bare, closed.
    pub fn from_tail(t: Option<Tail>) -> Result<CounterTail> {
        Ok(match t {
            None => CounterTail::Closed,
            Some(Tail::Draft) => CounterTail::Draft,
            Some(Tail::Pack) => CounterTail::Pack,
            Some(Tail::Open) => CounterTail::Open,
            Some(Tail::Return) => CounterTail::Return,
            Some(Tail::Review) => CounterTail::Review,
            Some(Tail::Retired) => return Err(SeqError::invalid("A2.5", "`retired` is used only without a counter")),
        })
    }
    /// From the text of a `from` / `to` field. Empty or absent is bare.
    pub fn from_field(s: Option<&str>) -> Result<CounterTail> {
        match s {
            None | Some("") => Ok(CounterTail::Closed),
            Some(w) => {
                let t = Tail::from_word(w).ok_or_else(|| SeqError::invalid("A2.5", format!("`{w}` is not a tail word (bare = closed; there is no `.closed` tail)")))?;
                CounterTail::from_tail(Some(t))
            }
        }
    }
    pub fn as_tail(self) -> Option<Tail> {
        match self {
            CounterTail::Draft => Some(Tail::Draft),
            CounterTail::Pack => Some(Tail::Pack),
            CounterTail::Open => Some(Tail::Open),
            CounterTail::Return => Some(Tail::Return),
            CounterTail::Review => Some(Tail::Review),
            CounterTail::Closed => None,
        }
    }
    /// Board text: the tail word, or `closed` for bare (A4.4 board example).
    pub fn board_word(self) -> &'static str {
        match self.as_tail() {
            Some(t) => t.as_str(),
            None => "closed",
        }
    }
    /// The one next state (workflow-loop 6: tails move one step at a time).
    pub fn next(self) -> Option<CounterTail> {
        match self {
            CounterTail::Draft => Some(CounterTail::Pack),
            CounterTail::Pack => Some(CounterTail::Open),
            CounterTail::Open => Some(CounterTail::Return),
            CounterTail::Return => Some(CounterTail::Review),
            CounterTail::Review => Some(CounterTail::Closed),
            CounterTail::Closed => None,
        }
    }
}

impl fmt::Display for CounterTail {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.board_word())
    }
}

/// Is a counter tail move allowed? One step at a time:
/// `draft -> pack -> open -> return -> review -> closed` (workflow-loop 6; format 4.1:
/// `pack -> open` yes, `pack -> return` never).
pub fn check_counter_move(from: CounterTail, to: CounterTail) -> Result<()> {
    if from.next() == Some(to) {
        Ok(())
    } else {
        Err(SeqError::rejected(
            "format 4.1",
            format!("tail move `{}` -> `{}` is not allowed; tails move one step: draft -> pack -> open -> return -> review -> closed", from, to),
        ))
    }
}

/// Tails a counter may be created with by `put` (format 3.3: "optionally with its tail").
/// Provisional (BUILD-LOG `7`): bare (closed, e.g. a note), `draft` or `pack`.
pub fn check_counter_create(t: CounterTail) -> Result<()> {
    match t {
        CounterTail::Closed | CounterTail::Draft | CounterTail::Pack => Ok(()),
        _ => Err(SeqError::rejected("format 3.3", format!("a counter cannot be created as `{t}`; it must be claimed and moved there one step at a time"))),
    }
}

/// The state of a page (A2.5, C1.2, C1.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum PageTail {
    Live,
    Draft,
    Retired,
}

impl PageTail {
    pub fn as_tail(self) -> Option<Tail> {
        match self {
            PageTail::Live => None,
            PageTail::Draft => Some(Tail::Draft),
            PageTail::Retired => Some(Tail::Retired),
        }
    }
}

/// State of one non-counted face slot (seqAddr 5.7).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum FaceSlotState {
    Absent,
    /// Only `FF.draft` exists (a brand-new face, drafting.md).
    DraftOnly,
    /// Seated `FF`, no draft.
    Seated,
    /// Seated `FF` and its one `FF.draft`.
    SeatedWithDraft,
    /// `FF.retired`: previously seated, awaiting removal.
    Retired,
}
