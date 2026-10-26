"""Pack B #05: write the runtime door 0300.band.compute and the five card drafts. Hand form, run once.

Each card holds only runs/uses/args (card rule B, Director 2026-10-26). It names the intended ACTIVE file
`02.<name>.py`, which does not exist, so the card cannot be executed: the candidate on the page is
`02.<name>.VVV.*` and is never selected implicitly. Nothing here is a supported loader interface.
Refuses to overwrite any existing file.
"""
from pathlib import Path

LAW = Path(r"D:\Git\lib-build\00.kernel\00.00.01.law")
CARDS = {
    "0302.run": ("run", ["runs: 02.run.py"], "02.run.001.py", "the loader"),
    "0303.jobs": ("jobs", ["runs: 02.jobs.py"], "02.jobs.010.py", "batches and their lifecycle"),
    "0304.check": ("check", ["runs: 02.lcheck.py", "uses: 02.sentinel.py as sentinel", "args: --config 02.rules.toml --moves 02.moves.toml"],
                   "02.lcheck.001.py, 02.sentinel.001.py, 02.rules.001.toml, 02.moves.001.toml", "the checker"),
    "0305.clerk": ("clerk", ["runs: 02.clerk.py"], "02.clerk.009.py", "faces: drop, draft, revise, live, lint"),
    "0307.face": ("face", ["runs: 02.face.py"], "02.face.001.py", "a new face with its stamp"),
}

DOOR = """# 01

version: 001
Authorization: draft — 2026-10-26
who: claude-opus-5-5
state: draft. Ordinary development door, hand form (Pack B #05). Not approved.
Face: 01
PPPP: 0300
book: 00.00.01.law
keyword: band.compute
why: The runtime band of workflow space 0 in the law book (N3NN with N = 0).

## Authority
This door holds the permission for the band. A member points. It does not repeat it.

```text
who: the Director seats a module; the Prime proposes; compute runs only what is seated
may: hold one page per runtime module, with its card 02.md and its code faces
may not: run a candidate 02.<name>.VVV.* in normal operation, or pick the highest version
halt: a card that names a file that is not active
```

## Members
`0302.run` (the loader), `0303.jobs`, `0304.check`, `0305.clerk`, `0307.face`. Each holds an inactive candidate imported byte-exact (`00.00.10.work/0410.imports`) and a card draft. `0306` is not allocated (slot is deferred; the title `slot` is taken by law 0034).

## State
No module is active. No loader is seated. The cards name `02.<name>.py`, which does not exist on any page, so no card can be executed. Activation is a separate Director decision, after a pack adapts the explicit loader and context against fixtures.

## Not
Not the universal runtime location: another declared workflow space would use its own N300 band. Not a seat.

### notes
born: 2026-10-26
source: Pack B #05; law 0057 amendment draft 01.003 (Space). The address 0300 also holds a template `0300.band` in Grok's unapproved candidate kernel (imports L3); that is another book, recorded on 0611.findings.
"""


def card(page, name, lines, cand, what):
    return f"""# 02

version: 001
Authorization: draft — 2026-10-26
who: claude-opus-5-5
state: draft. Card draft, hand form (Pack B #05). Cannot be executed: it names an active file that does not exist.
Face: 02
PPPP: {page[:4]}
book: 00.00.01.law
keyword: {name}
why: The intended card for {what}.

## Card
```text
{chr(10).join(lines)}
```

## State
Candidate(s) on this page: `{cand}`, imported byte-exact and inactive. The card names `{lines[0].split(': ')[1]}`, the active file, which does not exist until the Director seats a module. Nothing selects a candidate by its version number.

## Not
Not executable. Not a supported loader interface. Old stamps inside the candidate name their rebuild addresses; their needed adaptation is listed on `00.00.10.work/0410.imports`.
"""


def main():
    door = LAW / "0300.band.compute" / "01.md"
    out = [(door, DOOR)] + [(LAW / p / "02.md", card(p, *v)) for p, v in CARDS.items()]
    for path, _ in out:
        if path.exists():
            raise SystemExit(f"stop: exists: {path}")
    for path, text in out:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        print(path)


if __name__ == "__main__":
    main()
