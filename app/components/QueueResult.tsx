import { get } from "@/lib/compute";
import { Outcome } from "@/components/Outcome";
import type { ProposeResult, Reason } from "@/lib/rules";

type QP = { id: string; status: "approved" | "rejected"; book?: string; entries?: number[]; reasons?: Reason[]; findings?: Reason[]; http?: number };

/** Shows the result of a proposal as the compute's own queue records it (after the page reloads). */
export async function QueueResult({ id }: { id?: string }) {
  if (!id) return null;
  const r = await get<{ proposals: QP[] }>("/queue");
  const p = r.kind === "ok" ? r.data.proposals.find((x) => x.id === id) : undefined;
  if (!p) return <p className="note">Result {id} is no longer in the compute&apos;s queue memory.</p>;
  const res: ProposeResult = { status: p.status, book: p.book, entries: p.entries, reasons: p.reasons, findings: p.findings, queue_id: p.id, http: p.http };
  return <Outcome res={res} />;
}
