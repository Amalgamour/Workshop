"use client";
import type { ProposeResult } from "@/lib/rules";
import { getToken } from "@/components/WhoAmI";

export type Op = Record<string, unknown> & { op: string; addr: string };

/** Sends one proposal to the compute through the app's pass-through. The compute decides. */
export async function propose(by: string, ops: Op[]): Promise<ProposeResult> {
  try {
    const res = await fetch("/api/propose", { method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${getToken()}` }, body: JSON.stringify({ by, ops }) });
    const body = (await res.json().catch(() => ({}))) as ProposeResult;
    return { ...body, http: res.status, status: body.status ?? (res.ok ? "approved" : "rejected") };
  } catch (err) {
    return { status: "rejected", error: "down", detail: `The compute is not answering: ${String(err)}`, http: 0 };
  }
}

/** After an approved write: reload the screen with ?done=<queue id>, so the result shown comes from the compute's queue. */
export function showDone(router: { replace: (u: string) => void; refresh: () => void }, id?: string) {
  const u = new URL(window.location.href);
  if (id) u.searchParams.set("done", id);
  router.replace(u.pathname + u.search);
  router.refresh();
}

/** After a refused write: drop an older ?done= result so the screen shows only this refusal. */
export function clearDone(router: { replace: (u: string) => void }) {
  const u = new URL(window.location.href);
  if (!u.searchParams.has("done")) return;
  u.searchParams.delete("done");
  router.replace(u.pathname + u.search);
}
