"use client";
import { useEffect, useState } from "react";

const KEY = "workshop.by";
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

/** The name written as `by` on every proposal. There is no login yet (BUILD-LOG 7). */
export function WhoAmI() {
  const [who, setWho] = useWho();
  return (
    <div className="who">
      <label htmlFor="who">Writing as <small>(the "by" name)</small></label>
      <input id="who" value={who} onChange={(e) => setWho(e.target.value.trim())} spellCheck={false} />
      <small className="note">No sign-in yet. The compute records this name.</small>
    </div>
  );
}
