// Face 00 is the registry location (R10, R19; docs/spec/face00.md is a DRAFT): stamp + type + per-type registry.
// Display only: the stamp is front matter, the registry is a `## Registry` card. Layout is 7 until KERNEL settles it.
import { frontMatter, parseCards, type Card } from "@/lib/seq";

export const STAMP_FIELDS: [string, string][] = [
  ["address", "the page's full address"],
  ["title", "the page's title (on page 0000: the container's title)"],
  ["state", "live, draft or retired"],
  ["why-draft", "why the page is a draft (R5; name PROPOSED)"],
  ["axioms", "the axioms the page cites"],
  ["lineage", "the line back to what governs it (PROPOSED form)"],
];

export type Face00 = { stamp: Record<string, string>; type: string | null; registry: Card | null; other: Card[]; prose: string };

export function readFace00(body: string | undefined): Face00 {
  const stamp = frontMatter(body);
  const rest = (body ?? "").replace(/^---\n[\s\S]*?\n---\n?/, "");
  const { intro, cards } = parseCards(rest);
  const registry = cards.find((c) => c.key === "registry") ?? null;
  const type = stamp.type ?? null;
  const { type: _t, ...s } = stamp; void _t;
  return { stamp: s, type, registry, other: cards.filter((c) => c !== registry), prose: intro };
}
