"use client";
import { useEffect, useState } from "react";

const KEY = "workshop.by";
const TOKEN_KEY = "workshop.token";

/** The writer's secret token (books/.identities). The compute names the writer from it, not from `by`. */
export function getToken(): string {
  return typeof window === "undefined" ? "" : localStorage.getItem(TOKEN_KEY) ?? "";
}
export function useWho(): [string, (v: string) => void] {
  const [who, setWho] = useState("user");
  useEffect(() => { const v = localStorage.getItem(KEY); if (v) setWho(v); }, []);
  useEffect(() => {
    const h = () => setWho(localStorage.getItem(KEY) ?? "user");
    window.addEventListener("workshop-who", h);
    return () => window.removeEventListener("workshop-who", h);
  }, []);
  return [who, (v: string) => { localStorage.setItem(KEY, v); setWho(v); window.dispatchEvent(new Event("workshop-who")); }];
}

/** The writer's name and token. The compute records the name its token maps to (BUILD-LOG 7: provisional identity). */
export function WhoAmI() {
  const [who, setWho] = useWho();
  const [tok, setTok] = useState("");
  useEffect(() => setTok(getToken()), []);
  return (
    <div className="who">
      <label htmlFor="who">Writing as <small>(your name in books/.identities)</small></label>
      <input id="who" value={who} onChange={(e) => setWho(e.target.value.trim())} spellCheck={false} />
      <label htmlFor="tok">Token <small>(from books/.identities)</small></label>
      <input id="tok" type="password" value={tok} autoComplete="off" spellCheck={false}
        onChange={(e) => { const v = e.target.value.trim(); setTok(v); localStorage.setItem(TOKEN_KEY, v); }} />
      <small className="note">Every write carries this token. The compute ignores the typed name and records the token&apos;s name.</small>
    </div>
  );
}
