// Plain words for the rule ids the compute returns. Labels only: the compute decides.
export const RULE_PLAIN: Record<string, string> = {
  R2: "Seating a face needs an approval: the Director, or build-stage (R2) with a trial reference",
  S10: "The builder cannot review their own work",
  S11: "Only the one holding the claim can hand in the return",
  S03: "Closing needs an outcome: passed, failed, blocked, needs-authority or abandoned",
  D0: "Drafting rules: change a live face by copy, note, merge, then seat",
  "format 2": "First claim wins: someone else already took this job",
  "format 3.3": "The state has moved on: 'from' is not the current state",
  "format 3.4": "Snapshots are written only by the compute",
  "format 3.2": "An entry is missing a field it needs",
  "format 4.1": "Write things in order: the door first, then what is inside",
  "format 1.3": "Book file rule",
  "C1.1": "A page needs its door (face 00) and at least one content face",
  "C1.4": "Page type rule",
  "C2": "Card rule",
  "C3.2": "Every 01 or 02 card needs a 04 card with a why",
  "C6": "Face 03 is only allowed on certain pages",
  "C8.2": "Card key rule",
  "C8.5": "Dictionary rule",
  "C8.7": "Word-use records are written only by the compute",
  "A1.2": "Address reading rule",
  "A1.3": "Address shape rule",
  "A1.5": "Each part of an address has an exact width",
  "A1.6": "Leading-dot addresses need one active page",
  "A1.7": "Proposals must use the full address",
  "A1.8": "Finding rule",
  "A2.2": "Faces never have titles",
  "A2.3": "Titles: lowercase letters, digits, hyphens",
  "A2.5": "Tail words: which tails are allowed where",
  "A2.8": "Title rule (pages 1000 and up need a title)",
  "A4.3": "Face numbers: some faces are reserved",
  "A4.4": "The door FF.00 and pointer FF.99 carry no tail",
  "A4.5": "Counter rule",
  "A5.1": "Pointer rule",
  "A5.3": "A link needs its back-link",
  E3: "Axiom chain rule",
  "seqAddr 5.7": "Counted and seated faces rule",
  "seqAddr 8": "Address grammar",
  CONTRACT: "The request was not in the shape the compute expects",
  R4: "Plain characters only: letters, digits and simple punctuation (no accents, emoji or tabs)",
  R9: "Faces have no door: counters run 01-98",
  "C8.9": "Card type rule",
};

export const AXIOM_PLAIN: Record<string, string> = {
  "1": "Authority: granted, never claimed",
  "2": "Fractal: inherit, write only the difference",
  "3": "Leads: who leads each part",
  "4": "Why: keep the reason with the choice",
  "5": "Frame: the aim and its edges",
  "6": "Lineage: the line back and forward",
  "7": "Missing: marked, never invented",
  "8": "Connection: only written links count",
  "9": "Trial: a hostile pass before promotion",
};

export type Reason = { code?: string; rule?: string; axiom?: string | null; detail?: string; op?: number };
export type ProposeResult = {
  status?: "approved" | "rejected";
  reasons?: Reason[];
  findings?: Reason[];
  entries?: number[];
  queue_id?: string;
  book?: string;
  error?: string;
  axiom?: string | null;
  detail?: string;
  http?: number;
  seq_findings?: Reason[];
  linked?: { draft?: string; note?: string; phrasing?: string; question?: string };
  errors?: (Reason & { line?: number })[];
  ok?: boolean;
};

// workflow-loop.003 section 6: the loop on a face 05 counter.
export const LOOP = [
  { tail: "draft", step: "1 Write", who: "lead", plain: "The lead writes the job (the pack) and its work cards." },
  { tail: "pack", step: "2 Lint", who: "compute", plain: "Checked against its template. Ready to run. A pack that fails stays a draft." },
  { tail: "open", step: "3 Claim · 4 Work", who: "builder", plain: "A builder claims it. The first claim wins. The builder does the work cards." },
  { tail: "return", step: "5 Return", who: "builder", plain: "Only the claim holder hands in the return: what was done, with evidence." },
  { tail: "review", step: "6 Review", who: "reviewer", plain: "Someone other than the builder checks the evidence." },
  { tail: "closed", step: "7 Close", who: "compute", plain: "Closed with an outcome. The card keeps the history of every stage." },
] as const;

export const NEXT: Record<string, { to: string; label: string; needs?: "body" | "outcome"; who: string; rule: string }> = {
  draft: { to: "pack", label: "Mark ready to run (pack)", who: "lead", rule: "draft → pack. The spec has compute lint here (section 8); the lint is not built yet, so it is shown, not run." },
  pack: { to: "open", label: "Claim it (open)", who: "builder", rule: "pack → open. The first claim wins; a second claim gets 'conflict' (axiom 1)." },
  open: { to: "return", label: "Hand in the return", needs: "body", who: "builder", rule: "open → return. Only the claim holder can do this (S11). Write what was done per work card: result: done | blocked | need." },
  return: { to: "review", label: "Start review", who: "reviewer", rule: "return → review. The reviewer must not be the builder (S10)." },
  review: { to: "", label: "Close with an outcome", needs: "outcome", who: "the reviewer asks; the compute writes", rule: "review → closed. Only the reviewer can ask, and the compute writes the close (POST /close). An outcome must be recorded (S03). 'abandoned' is not offered: it needs the compute's recovery return (S11)." },
};
export const OUTCOMES = ["passed", "failed", "blocked", "needs-authority"];
