"use client";
import type { ProposeResult } from "@/lib/rules";
import { authHeader, learnName } from "@/lib/auth";

export type Op = Record<string, unknown> & { op: string; addr: string };

/** POSTs to one compute route through the app's pass-through, with the person's token. The compute decides. */
export async function post(route: "propose" | "ask/link" | "close" | "check.seq", body: string, contentType = "application/json"): Promise<ProposeResult> {
  try {
    const res = await fetch(`/api/post/${route}`, { method: "POST", headers: { "content-type": contentType, ...authHeader() }, body });
    const data = (await res.json().catch(() => ({}))) as ProposeResult;
    const out: ProposeResult = { ...data, http: res.status, status: data.status ?? (res.ok ? "approved" : "rejected") };
    if (out.queue_id) learnName(out.queue_id);
    return out;
  } catch (err) {
    return { status: "rejected", error: "down", detail: `The app could not reach the compute: ${String(err)}`, http: 0 };
  }
}

/** Sends one proposal. `by` is not sent: the compute takes the name from the token. */
export const propose = (ops: Op[]) => post("propose", JSON.stringify({ ops }));

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
