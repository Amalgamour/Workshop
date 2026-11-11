"use client";
// Token sign-in (CONTRACT addendum, COMPUTE: identity is provisional, BUILD-LOG 7).
// The token stays in this browser (localStorage) and is sent only to the app's own pass-through, which forwards it to the compute.
// The compute has no "who am I" route, so the name shown is the one the compute recorded on your latest write (from /queue).
const TOKEN = "workshop.token";
const NAME = "workshop.name";
const EVT = "workshop-auth";

export type AuthState = { token: string; name: string | null; check: "unknown" | "ok" | "bad" | "down" };

export function readAuth(): AuthState {
  if (typeof window === "undefined") return { token: "", name: null, check: "unknown" };
  return { token: localStorage.getItem(TOKEN) ?? "", name: localStorage.getItem(NAME), check: (localStorage.getItem(TOKEN + ".check") as AuthState["check"]) ?? "unknown" };
}
function emit() { window.dispatchEvent(new Event(EVT)); }
export function onAuth(f: () => void) { window.addEventListener(EVT, f); return () => window.removeEventListener(EVT, f); }

export function authHeader(): Record<string, string> {
  const t = typeof window === "undefined" ? "" : localStorage.getItem(TOKEN) ?? "";
  return t ? { authorization: `Bearer ${t}` } : {};
}

export function setToken(t: string) {
  localStorage.setItem(TOKEN, t.trim());
  localStorage.removeItem(NAME);
  localStorage.setItem(TOKEN + ".check", "unknown");
  emit();
}
export function signOut() { localStorage.removeItem(TOKEN); localStorage.removeItem(NAME); localStorage.removeItem(TOKEN + ".check"); emit(); }

/** Asks the compute whether the token is known, without writing anything: an empty proposal body is refused
 *  before it reaches the queue, with 401 for an unknown token and 400 for a known one. */
export async function checkToken(): Promise<AuthState["check"]> {
  let c: AuthState["check"] = "down";
  try {
    const r = await fetch("/api/post/propose", { method: "POST", headers: { "content-type": "application/json", ...authHeader() }, body: "" });
    c = r.status === 401 || r.status === 403 ? "bad" : r.status === 400 ? "ok" : "down";
  } catch { c = "down"; }
  localStorage.setItem(TOKEN + ".check", c);
  emit();
  return c;
}

/** After a write, read the name the compute recorded for it. */
export async function learnName(queueId: string) {
  try {
    const q = await (await fetch("/api/compute/queue")).json();
    const p = (q.proposals ?? []).find((x: { id: string }) => x.id === queueId);
    if (p?.by && p.http !== 401) { localStorage.setItem(NAME, p.by); localStorage.setItem(TOKEN + ".check", "ok"); emit(); }
  } catch { /* keep the old name */ }
}
