import type { LogEntry } from "@/lib/compute";

export type DraftNote = { n: number; by: string; at: string; body: string; struck: boolean; struckBy?: number };

/** Notes on the current draft of one face, read from its history (drafting.md: copy, note, merge, promote). Display only. */
export function draftNotes(history: LogEntry[], faceAddr: string): DraftNote[] {
  const draftAddr = `${faceAddr}.draft`;
  let notes: DraftNote[] = [];
  for (const e of history) {
    if (e.addr !== draftAddr && e.addr !== faceAddr) continue;
    if (e.op === "promote") notes = [];
    if (e.op === "note" && e.addr === draftAddr) notes.push({ n: e.n, by: e.by, at: e.at, body: e.body ?? "", struck: false });
    if (e.op === "merge" && e.addr === draftAddr && typeof e.cites === "number") {
      const t = notes.find((x) => x.n === e.cites);
      if (t) { t.struck = true; t.struckBy = e.n; }
    }
  }
  return notes;
}

export const FACE_TEMPLATE: Record<string, string> = {
  "01": "## Card Title\ntype: rule\naxioms: 1.7.8\n\nWhat a model must know, in a few lines.",
  "02": "## Card Title\ntype: schema\n\nThe exact template, format or steps.",
  "03": "## Card Title\ntype: menu\n\nOperations for the compute.",
  "04": "## Card Title\nsource: [01 / Card Title]\nwhy: The reason, in one line.\n\nThe full explanation, for a person.",
  "05": "## Job title\ntype: task\nlead: 3MC\n\nWhat the job is.",
  "06": "## Session note\ntype: note\n\nWhat I learned.",
  "08": "## Link name\ntype: link\nkind: dependency\nto: DD.SS.BB.PPPP",
};
