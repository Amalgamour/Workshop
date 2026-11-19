# Axiom Cite Grammar: draft relayed by Matthew (t383u, 2026-11-19, 11:24 AM EST)

Matthew's words, verbatim: "This is for designer to work on.  our grammar for axioms.  If now isn't the right time.  Park as additional work for later in our dev cycle."

The draft below is kept verbatim. Status: proposal for review. Designer is the owner. It is not a ruling.

---

# Axiom Cite Grammar — Draft for Prima’s Review

Prima,

Matthew asked me to turn our discussion of axiom chains into a grammar a fresh model can use accurately. The aim is to preserve how the reasoning pieces relate, in a form short enough to put on a work order. This is a proposal for review.

The strongest example is `7.8` versus `8.7`. Both use Missing and Connection, but each directs the worker’s attention differently. If the worker reads both as “something about a missing link,” the numbers survived and the reasoning was lost.

## 1. What each piece asks

These questions are aids for reading the governing axiom text. Keep the full axioms as the source.

| Piece | Reading question |
|---|---|
| `1` Authority | Who can authorize this action, and what record establishes that authority? |
| `2` Fractal | What is inherited, and what is different here? |
| `3` Leads | Who leads each part, and in what order? |
| `4` Why | What reason was recorded, and does it still apply? |
| `5` Frame | What are we trying to accomplish, and where does the work stop? |
| `6` Lineage | What came before, what changed, and what depends on it? |
| `7` Missing | What is absent, incomplete, or still unknown? |
| `8` Connection | What is linked, and what does the link establish? |
| `9` Trial | What has another view actually tested? |

## 2. How to write a cite

Use the `axioms:` field.

    cite       = chain ("," chain)*
    chain      = piece ("." piece)*
    piece      = "1" | "2" | "3" [lead_order] | "4" | "5" | "6" | "7" | "8" | "9"
    lead_order = 1 to 3 distinct letters drawn from M, P, C

Only `3` takes letters. `M`, `P`, and `C` name model, person, and compute. A one-digit axiom mark is distinct from a SeqAddr address. The distinct-letter rule is proposed for the draft.

## 3. How to read a cite

1. **Name the subject.** Read the chain against the action, finding, or record it is attached to. Ask what it refers to if that is unclear.
2. **Start with the first piece.** It sets what the reading is about. Read left to right. Each dot brings a new axiom to bear on the reading so far. Keep the earlier focus as the chain grows.
3. **Start a separate reading at a comma.** Both chains apply to the named subject unless the record assigns them different subjects. The second chain does not become a step in the first.
4. **Keep the lead order attached to `3`.** `3MPC` says the model leads, then the person, then compute. It names the lead order. The workflow defines any handoffs, and the grant defines what each participant may do.
5. **Say it back in plain language.** Give the reading in one sentence, point to the relevant evidence or gap, and explain what follows for the affected action.

**Why.** Compute can check the syntax. A person or model has to interpret the chain against the actual work. A short readback exposes the difference between repeating the numbers and understanding what they mean together.

## 4. A cite can guide a check or label a finding

In a pack, `1.7.8` can tell a worker what to examine before a write. The cite alone does not assert that anything is missing. In a return, the same cite can label a specific gap that prevented the worker from establishing authority. The surrounding record tells the reader which use is intended. A cite runs nothing and permits nothing.

| Cite | Example readback |
|---|---|
| `7.8` | “The required connection to the predecessor is missing or could not be established.” Say whether no link was recorded or an existing pointer could not be resolved. |
| `8.7` | “The connection is established, and I can tell which part of it is incomplete. It identifies the predecessor page but omits the revision required for this review.” |
| `4.7` | “The decision is recorded. Its why is missing.” |
| `1.7.8` | “Before this write, check who authorizes it and whether a missing or unresolved connection prevents us from establishing that authority.” |
| `1,3MPC` | “One reading concerns who can authorize the work. The other concerns the lead order: model, then person, then compute.” |

The important edge case is a pointer the reader cannot open. The worker can report that the pointer exists and its target could not be verified. It should preserve the observed reason if known, such as denied access or a reader failure. The failed read does not establish that the target is absent.

## 5. First cold trial

Give a fresh worker the grammar card and three unfamiliar work order records. Keep the expected readings with the reviewer.

1. A predecessor connection is required and no link is recorded.
2. A link resolves to the predecessor page, but the required revision is unspecified.
3. A pointer names a page and revision, but the reader cannot open the target.

For each case, ask the worker for a cite, a one-sentence readback, the evidence behind it, and what should happen next. Also give it a routine `1.7.8` pre-write check where the authority and connection are complete. See whether it can perform the check without inventing a finding.

Judge the action as well as the notation. A worker can write `7.8` correctly and still make the wrong move by assuming the target is absent, substituting a similarly named predecessor, or proceeding with a write whose grant it could not verify. Record those outcomes separately.

## Question for Prima

Check the draft against the existing decisions and the Lab 02 and Lab 03 records. In particular, does **“read left to right, keeping the earlier focus as each later piece refines it”** hold beyond the examples we’ve already taught? Please try it on one unfamiliar chain. If two careful readers arrive at different meanings, bring back the smallest example that exposes the ambiguity before we add more rules.
