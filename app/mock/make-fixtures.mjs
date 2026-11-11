// Writes sample books into mock/fixtures as JSON Lines (spec/format.md section 3).
// Run: node mock/make-fixtures.mjs   (only used when the repo has no books/ yet)
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, "fixtures");
mkdirSync(out, { recursive: true });

let clock = Date.parse("2026-11-09T14:00:00Z");
const tick = () => new Date((clock += 97_000)).toISOString().replace(/\.\d+Z$/, "Z");

function book(address, entries) {
  let n = 0;
  const lines = [JSON.stringify({ seqbook: 1, address })];
  for (const e of entries) {
    n += 1;
    const { addr, ...rest } = e;
    if (rest.cites === "prev") rest.cites = n - 1;
    lines.push(JSON.stringify({ n, at: tick(), by: e.by ?? "user", op: e.op ?? "put", addr: `${address}.${addr}`, ...rest, ...(e.by ? {} : {}) }));
  }
  writeFileSync(join(out, `${address}.book`), lines.join("\n") + "\n");
}
const stamp = (title, type = "general", extra = "") =>
  `---\ntitle: ${title}\ntype: ${type}\nstate: seated${extra}\n---`;

// ---------- kernel ----------
book("00.00.00", [
  { addr: "0000.00", body: stamp("kernel", "system"), by: "compute" },
  { addr: "0012.00", body: stamp("dictionary", "system"), by: "compute" },
  // The dictionary face 03 is counted: one counter per letter section (brands.md layout; R9: no 03.00 door).
  { addr: "0012.03.25", body: "## face\ntype: index\ndefault: face.001\nface.001: 00.00.00.0050.01.face", by: "compute" },
  { addr: "0012.03.49", body: "## seqaddr\ntype: index\ndefault: seqaddr.001\nseqaddr.001: 00.00.00.0050.01.seqaddr", by: "compute" },
  { addr: "0020.00", body: stamp("retry-policy", "system"), by: "user" },
  { addr: "0020.01", body: "## Retry Policy\ntype: rule\naxioms: 1.7.8\n\nA failed write is never retried automatically. Report it and wait.", by: "claude-opus" },
  { addr: "0020.04", body: "## Retry Policy\nsource: [01 / Retry Policy]\nwhy: Retrying hides failures and burns usage.\n\nIf a write fails, the person needs to see it. Silent retries make it look like work went well when it did not. So the kernel says: stop, report, wait for the Director.", by: "user" },
  { addr: "0021.00", body: stamp("naming", "system"), by: "user" },
  { addr: "0021.01", body: "## Titles\ntype: rule\n\nTitles are lowercase letters, digits and hyphens. A title is a label, not identity.", by: "claude-opus" },
  { addr: "0021.04", body: "## Titles\nsource: [01 / Titles]\nwhy: Renaming must never break an address.\n\nThe number is the identity. The word after it helps a person read it. Two pages can share a title.", by: "user" },
  { addr: "0050.00", body: stamp("faces", "system"), by: "user" },
  { addr: "0050.01", body: "## Seqaddr\ntype: brand\nbrand: seqaddr.001\nforms: seqaddr, seqAddr\nmeans: the sequence address: desk.shelf.book.page.face\n\nAn address reads by position. The page is the anchor.\n\n## Face\ntype: brand\nbrand: face.001\nforms: face, faces\nmeans: one view of a page, for one kind of reader\n\nA page has several faces. Each face is numbered 00 to 08.", by: "claude-opus" },
  { addr: "0050.02", body: "## Seqaddr\ntype: schema\n\n```\n[DD.][SS.][BB.] PPPP [.FF][.NN] [.title][.tail]\n```", by: "claude-opus" },
  { addr: "0050.04", body: "## Seqaddr\nsource: [01 / Seqaddr], [02 / Seqaddr]\nwhy: One address must find one thing, always.\n\nThe address is the line written down. Each part comes from the one before it, so it stays stable to store.\n\n## Face\nsource: [01 / Face]\nwhy: Different readers need different views of the same page.\n\nA model needs short law. A person needs the long why. The compute needs exact steps. Faces keep them together without mixing them.", by: "user" },
]);

// ---------- desk 10 and shelf 10.11 ----------
book("10.00.00", [
  { addr: "0000.00", body: stamp("matthew", "system") },
]);
book("10.11.00", [
  { addr: "0000.00", body: stamp("workshop", "system") },
  { addr: "0021.00", body: stamp("naming", "system") },
  { addr: "0021.06.01", body: "## Shelf naming note\ntype: note\n\nOn this shelf, book titles name the tool, not the person.", by: "claude-opus" },
]);

// ---------- book 10.11.21 tools ----------
book("10.11.21", [
  { addr: "0000.00", body: stamp("tools", "system") },
  { addr: "0012.00", body: stamp("dictionary", "system") },
  { addr: "0012.03.16", body: "## colab\ntype: index\ndefault: colab.001\ncolab.001: 10.11.21.1014.01.colab", by: "compute" },
  { addr: "0012.03.29", body: "## ham\ntype: index\ndefault: ham.001\nham.001: 10.11.21.1014.01.ham\nham.002: 10.11.22.1001.01.ham", by: "compute" },
  { addr: "0020.00", body: stamp("retry-policy", "system") },
  { addr: "0020.01", body: "## Retry Policy\ntype: rule\naxioms: 1.7.8\n\nA failed write is retried once, only if the assignment allows it. Then report it.", by: "claude-opus" },
  { addr: "1014.00", body: stamp("colab", "general", "\naxioms: 4.6") },
  { addr: "1014.01", body: "## Colab\ntype: brand\nbrand: colab.001\nforms: colab, Colab\nmeans: the shared notebook where the Director runs experiments\nmeters: notebook 100%, run 80%, gpu 60%\n\nWhen the Director says colab, he means his notebook, not working together.\n\n## Ham\ntype: brand\nbrand: ham.001\nforms: ham\nmeans: the Director's favourite sandwich\n\nHam is lunch.\n\n## Retry Policy\ntype: rule\n\nColab runs are never retried without asking.", by: "claude-opus" },
  { addr: "1014.04", body: "## Colab\nsource: [01 / Colab]\nwhy: Models read colab as collaborate and drift.\n\nThe Director uses colab for one thing: his notebook. Writing it down stops the model guessing the average meaning.\n\n## Retry Policy\nsource: [01 / Retry Policy]\nwhy: A GPU run costs money each time.\n\nRetrying a run silently spends usage. Ask first.", by: "user" },
  { addr: "1014.05.01", tail: "pack", body: "## Build timer\ntype: task\nlead: 3MC\n\nBuild the timer page in the dev band.", by: "prima" },
  { addr: "1014.05.01", op: "tail", from: "pack", to: "open", by: "agent-7" },
  { addr: "1014.05.01", op: "tail", from: "open", to: "return", by: "agent-7" },
  { addr: "1014.05.02", tail: "pack", body: "## Link the notebook\ntype: task\n\nAdd the notebook link to face 08.", by: "prima" },
  { addr: "1014.06.01", body: "## Session 2026-11-09\ntype: note\n\nThe Director said colab three times today, always the notebook.", by: "claude-opus" },
  { addr: "1014.08", body: "## Timer\ntype: link\nkind: dependency\nto: 10.11.21.1523\n\n## Naming rule\ntype: link\nkind: authority\nto: 00.00.00.0021\n\n## Notebook export\ntype: link\nkind: dependency\nto: 10.11.21.1777\n\nNot written yet.", by: "claude-opus" },
  { addr: "1523.00", body: stamp("timer", "code") },
  { addr: "1523.01", body: "## Timer\ntype: rule\n\nA timer counts down and records when it ends.", by: "claude-opus" },
  { addr: "1523.04", body: "## Timer\nsource: [01 / Timer]\nwhy: Long runs need a clear end so work does not drift.\n\nThe timer is the first small tool to test the workbook idea.", by: "user" },
  { addr: "1523.08", body: "## Colab\ntype: link\nkind: back-link\nto: 10.11.21.1014", by: "compute" },
  { addr: "1523.01", op: "copy", tail: "draft", by: "compute" },
  { addr: "1523.01.draft", op: "note", body: "Say the timer can be paused.", by: "claude-opus" },
  { addr: "1523.01.draft", op: "merge", cites: "prev", body: "## Timer\ntype: rule\n\nA timer counts down, records when it ends, and can be paused.", by: "claude-opus", proposal: "p-0007" },
]);

// ---------- book 10.11.22 bob ----------
book("10.11.22", [
  { addr: "0000.00", body: stamp("personal-desk", "system") },
  { addr: "1001.00", body: stamp("bob", "general") },
  { addr: "1001.01", body: "## Name\ntype: rule\n\nThe user's name is Bob.\n\n## Ham\ntype: brand\nbrand: ham.002\nforms: Ham, Hammie\nmeans: a friend from work\n\nHam is a person here.", by: "claude-opus" },
  { addr: "1001.04", body: "## Name\nsource: [01 / Name]\nwhy: Session 1: \"My name is Bob and I like cats.\"\n\nSaved so session 2 can answer \"what is my name\" from the card, not from memory.\n\n## Cats\nwhy: Bob said he likes cats.\n\nKept with the name because it came in the same sentence.", by: "user" },
]);
console.log("fixtures written to", out);
