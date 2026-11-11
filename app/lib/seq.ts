// Small display helpers. They only label what the compute returned; they never decide rules.
export const FACE_NAMES: Record<string, { name: string; plain: string }> = {
  "00": { name: "Stamp", plain: "identity: the page's address, title and state" },
  "01": { name: "Law", plain: "for models: what the page means, in short cards" },
  "02": { name: "Schema", plain: "templates, formats and exact steps" },
  "03": { name: "Operate", plain: "for the compute: operations and the card menu" },
  "04": { name: "Why", plain: "for you: the reason behind each card, in full" },
  "05": { name: "Tasks", plain: "passes of work, counted 01, 02, 03..." },
  "06": { name: "Notes", plain: "notes models leave, one per session" },
  "08": { name: "Map", plain: "links: where it came from and what depends on it" },
};
export const TAB_FACES = ["01", "02", "03", "04", "05", "06", "08"];

export const TAIL_PLAIN: Record<string, string> = {
  seated: "live: this is the one in force",
  draft: "being written, not active yet",
  retired: "was live, now retired before removal",
  pack: "ready to run",
  open: "a worker is running it now",
  return: "done: what was done is written",
  review: "under review",
  closed: "finished and closed",
};

export const SOURCE_PLAIN: Record<string, string> = {
  local: "written in this book",
  shelf: "inherited from the shelf",
  desk: "inherited from the desk",
  kernel: "inherited from the kernel",
  missing: "missing: not written anywhere",
};

export function frontMatter(body: string | undefined): Record<string, string> {
  const m = /^---\n([\s\S]*?)\n---/.exec(body ?? "");
  const out: Record<string, string> = {};
  if (m) for (const l of m[1].split("\n")) { const i = l.indexOf(":"); if (i > 0) out[l.slice(0, i).trim()] = l.slice(i + 1).trim(); }
  return out;
}

export type Card = { title: string; key: string; fields: [string, string][]; body: string };
export const keyOf = (t: string) => t.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

// Cards are ## headings, then field lines, then a blank line, then the body (seqAddr.md 5.3).
export function parseCards(body: string): { intro: string; cards: Card[] } {
  const cards: Card[] = [];
  let intro = "";
  let cur: Card | null = null;
  let inFields = false;
  for (const l of (body ?? "").split("\n")) {
    const h = /^##\s+(.+)$/.exec(l);
    if (h) { cur = { title: h[1].trim(), key: keyOf(h[1]), fields: [], body: "" }; cards.push(cur); inFields = true; continue; }
    if (!cur) { intro += (intro ? "\n" : "") + l; continue; }
    if (inFields) {
      const f = /^([a-z][a-z0-9_.-]*):\s?(.*)$/i.exec(l);
      if (f && l.trim()) { cur.fields.push([f[1], f[2]]); continue; }
      inFields = false;
      if (!l.trim()) continue;
    }
    cur.body += (cur.body ? "\n" : "") + l;
  }
  return { intro: intro.trim(), cards };
}

export const AXES = ["desk", "shelf", "book", "page", "face", "counter"];

export function torontoTime(iso: string) {
  try {
    return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Toronto", dateStyle: "medium", timeStyle: "short" }).format(new Date(iso)) + " Toronto";
  } catch { return iso; }
}

export function opPlain(e: { op: string; from?: string; to?: string; tail?: string }) {
  switch (e.op) {
    case "put": return e.tail ? `wrote it (as ${e.tail})` : "wrote it";
    case "tail": return `moved its state: ${e.from ?? "?"} → ${e.to ?? "?"}`;
    case "copy": return "copied the live face into a draft";
    case "note": return "added a note to a draft";
    case "merge": return "applied a note to a draft";
    case "promote": return "promoted the draft to live";
    case "snapshot": return "saved a full snapshot";
    case "use": return "recorded a word lookup";
    default: return e.op;
  }
}
