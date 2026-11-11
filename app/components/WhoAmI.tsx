"use client";
import { useEffect, useState } from "react";
import { checkToken, onAuth, readAuth, setToken, signOut, type AuthState } from "@/lib/auth";

export function useAuth(): AuthState {
  const [a, setA] = useState<AuthState>({ token: "", name: null, check: "unknown" });
  useEffect(() => { setA(readAuth()); return onAuth(() => setA(readAuth())); }, []);
  return a;
}

/** Sidebar sign-in: paste a token from books/.identities. */
export function WhoAmI() {
  const a = useAuth();
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  async function save() { setBusy(true); setToken(draft); setDraft(""); await checkToken(); setBusy(false); }
  return (
    <div className="who">
      <div className="who-title">Signed in</div>
      {a.token ? (
        <>
          <div className={`who-state ${a.check}`}>
            {a.check === "ok" ? <>✓ Token accepted{a.name ? <> as <b>{a.name}</b></> : null}</> : a.check === "bad" ? <>✗ The compute does not know this token</> : a.check === "down" ? <>? The compute is not answering</> : <>Token saved, not checked yet</>}
          </div>
          {a.check === "ok" && !a.name ? <small className="note">Your name shows here after your first write. (This compute has no &quot;who am I&quot; route.)</small> : null}
          <div className="row" style={{ gap: 6, marginTop: 6 }}>
            <button className="quiet small" onClick={async () => { setBusy(true); await checkToken(); setBusy(false); }} disabled={busy}>Check again</button>
            <button className="quiet small" onClick={signOut}>Sign out</button>
          </div>
        </>
      ) : <div className="who-state unknown">Not signed in. You can read everything; to write, paste your token.</div>}
      <label htmlFor="tok" className="note" style={{ display: "block", marginTop: 10 }}>Token <small>(your line in books/.identities)</small></label>
      <input id="tok" type="password" value={draft} onChange={(e) => setDraft(e.target.value)} placeholder={a.token ? "paste a different token" : "paste your token"} autoComplete="off" spellCheck={false} />
      <button className="go small" disabled={!draft.trim() || busy} onClick={save}>Sign in</button>
    </div>
  );
}
