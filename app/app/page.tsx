"use client";

import { FormEvent, useEffect, useState } from "react";

const COMPUTE = "http://127.0.0.1:7040";

type FaceItem = { addr: string; tail: string };
type PageItem = { addr: string; title: string; faces: FaceItem[] };
type BandItem = { id: string; name: string; pages: PageItem[] };
type Catalog = { book: string; len: string; bands: BandItem[] };

export default function Home() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [bandId, setBandId] = useState("");
  const [pageAddr, setPageAddr] = useState("");
  const [addr, setAddr] = useState("");
  const [pageTitle, setPageTitle] = useState("");
  const [text, setText] = useState("Open a band, then a page, then a face.");
  const [sentence, setSentence] = useState("");
  const [proposal, setProposal] = useState("");
  const [busy, setBusy] = useState<"read" | "propose" | "book" | null>("book");
  const [error, setError] = useState("");

  async function loadBook() {
    setBusy("book");
    setError("");
    try {
      const response = await fetch(`${COMPUTE}/book`);
      const body = await response.text();
      if (!response.ok) {
        setError(body);
        return;
      }
      setCatalog(parseCatalog(body));
    } catch (err) {
      setError(err instanceof Error ? err.message : "The compute did not answer.");
    } finally {
      setBusy(null);
    }
  }

  useEffect(() => {
    void loadBook();
  }, []);

  const band = catalog?.bands.find((item) => item.id === bandId) ?? null;
  const page = band?.pages.find((item) => item.addr === pageAddr) ?? null;

  function openBand(next: BandItem) {
    setBandId(next.id === bandId ? "" : next.id);
  }

  async function openPage(next: PageItem) {
    setPageAddr(next.addr);
    setPageTitle(next.title);
    setAddr(next.addr);
    setBusy("read");
    try {
      const response = await fetch(
        `${COMPUTE}/seq?page=${encodeURIComponent(next.addr)}`,
      );
      setText(await response.text());
    } catch (err) {
      setText(err instanceof Error ? err.message : "The compute did not answer.");
    } finally {
      setBusy(null);
    }
  }

  async function openFace(face: string) {
    setAddr(face);
    setBusy("read");
    try {
      const response = await fetch(
        `${COMPUTE}/face?addr=${encodeURIComponent(face)}`,
      );
      const body = await response.text();
      setText(body);
      const title = lineValue(body, "title");
      if (title) setPageTitle(title);
    } catch (err) {
      setText(err instanceof Error ? err.message : "The compute did not answer.");
    } finally {
      setBusy(null);
    }
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    await openFace(addr);
  }

  async function onPropose(event: FormEvent) {
    event.preventDefault();
    setBusy("propose");
    try {
      const response = await fetch(`${COMPUTE}/propose`, {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: sentence,
      });
      setProposal(await response.text());
      await loadBook();
    } catch (err) {
      setProposal(err instanceof Error ? err.message : "The compute did not answer.");
    } finally {
      setBusy(null);
    }
  }

  return (
    <main>
      <h1>Book</h1>
      <p className="lead">
        Dev mode. Every band, page, and face the compute is serving is listed
        here. This page does not open the book file.
      </p>
      <p className="book-line">
        {catalog
          ? `${catalog.book} · ${catalog.len} lines`
          : busy === "book"
            ? "Asking the compute for the book."
            : "The book is not loaded."}
      </p>
      {error ? <p className="error">{error}</p> : null}
      <div className="browser">
        <nav className="menu" aria-label="Book">
          {catalog?.bands.map((item) => (
            <div key={item.id}>
              <button
                type="button"
                className="choice"
                aria-expanded={item.id === bandId}
                onClick={() => openBand(item)}
              >
                {item.name}
                <span>
                  {item.id} {item.pages.length}
                </span>
              </button>
              {item.id === bandId
                ? item.pages.map((pageItem) => (
                    <div key={pageItem.addr} className="nest">
                      <button
                        type="button"
                        className="choice"
                        aria-pressed={pageItem.addr === pageAddr}
                        onClick={() => openPage(pageItem)}
                      >
                        {pageItem.addr.slice(pageItem.addr.length - 4)}
                        <span>{pageItem.title}</span>
                      </button>
                      {pageItem.addr === pageAddr
                        ? pageItem.faces.map((face) => (
                            <button
                              key={face.addr}
                              type="button"
                              className="choice face"
                              aria-pressed={face.addr === addr}
                              onClick={() => void openFace(face.addr)}
                            >
                              {face.addr.slice(pageItem.addr.length)}
                              {face.tail ? <span>{face.tail}</span> : null}
                            </button>
                          ))
                        : null}
                    </div>
                  ))
                : null}
              {item.id === bandId && item.pages.length === 0 ? (
                <p className="empty">No pages.</p>
              ) : null}
            </div>
          ))}
        </nav>
        <section className="file">
          <p className="page-title">Title:({pageTitle})</p>
          <form onSubmit={onSubmit}>
            <label>
              Address
              <input
                value={addr}
                onChange={(event) => setAddr(event.target.value)}
                aria-label="Address"
              />
            </label>
            <button type="submit" disabled={busy !== null}>
              {busy === "read" ? "Reading" : "Read"}
            </button>
          </form>
          <pre className="file-body">{text}</pre>
        </section>
      </div>
      <h2>Propose</h2>
      <p className="lead">
        The proposer here is local. It is not a remote model. An accepted
        sentence is appended by the compute to the book it is serving.
      </p>
      <form onSubmit={onPropose}>
        <label>
          Sentence
          <textarea
            value={sentence}
            onChange={(event) => setSentence(event.target.value)}
            aria-label="Sentence"
            rows={3}
          />
        </label>
        <button type="submit" disabled={busy !== null}>
          {busy === "propose" ? "Proposing" : "Propose"}
        </button>
      </form>
      {proposal ? <pre>{proposal}</pre> : null}
    </main>
  );
}

function parseCatalog(text: string): Catalog {
  const bands: BandItem[] = [];
  let book = "";
  let len = "";
  let band: BandItem | null = null;
  let page: PageItem | null = null;
  for (const line of text.split("\n")) {
    if (line.startsWith("book: ")) book = line.slice(6).trim();
    else if (line.startsWith("len: ")) len = line.slice(5).trim();
    else if (line.startsWith("band: ")) {
      const rest = line.slice(6).trim();
      const space = rest.indexOf(" ");
      band = {
        id: space === -1 ? rest : rest.slice(0, space),
        name: space === -1 ? "" : rest.slice(space + 1),
        pages: [],
      };
      bands.push(band);
      page = null;
    } else if (line.startsWith("page: ") && band) {
      const rest = line.slice(6);
      const mark = rest.indexOf(" title: ");
      page = {
        addr: (mark === -1 ? rest : rest.slice(0, mark)).trim(),
        title: mark === -1 ? "" : rest.slice(mark + 8).trim(),
        faces: [],
      };
      band.pages.push(page);
    } else if (line.startsWith("face: ") && page) {
      const rest = line.slice(6);
      const mark = rest.indexOf(" tail: ");
      page.faces.push({
        addr: (mark === -1 ? rest : rest.slice(0, mark)).trim(),
        tail: mark === -1 ? "" : rest.slice(mark + 7).trim(),
      });
    }
  }
  return { book, len, bands };
}

function lineValue(text: string, key: string): string {
  const prefix = `${key}:`;
  const line = text.split("\n").find((item) => item.startsWith(prefix));
  return line ? line.slice(prefix.length).trim() : "";
}
