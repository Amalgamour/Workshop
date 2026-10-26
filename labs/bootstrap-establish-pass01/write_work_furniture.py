"""Pack B #04: write the work book's furniture and doors, and 0501.bootstrap 01.md and 05.01.md (the Pack A
record). Hand form; refuses to overwrite. The contents page (0011) is generated separately, last.
"""
from pathlib import Path

W = Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")


def head(face, pppp, keyword, why, state="draft. Work book furniture, hand form (Pack B #04). Not approved kernel law."):
    return (f"# {face}\n\nversion: 001\nAuthorization: draft — 2026-10-26\nwho: claude-opus-5-5\nstate: {state}\n"
            f"Face: {face}\nPPPP: {pppp}\nbook: 00.00.10.work\nkeyword: {keyword}\nwhy: {why}\n\n")


def door(pppp, keyword, what, members, who):
    return head("01", pppp, keyword, f"The door of the {what} band.") + (
        f"## Authority\nThis door holds the permission for the band. A member points. It does not repeat it.\n\n"
        f"```text\n{who}\n```\n\n## Members\n{members}\n\n## Not\nNot law. Not a seat.\n")


FILES = {
    "00.md": ("00.00.10.work: the work book of desk 00.kernel. Provisional (Pack B, 2026-10-26); contents in 0011.contents/01.001.md.\n"),
    "0010.about/01.001.md": head("01", "0010", "about", "What this book is and how to read it.") + (
        "## Book\nThe work book holds designs, assignments, decisions, packs, returns and findings for this desk. It references runtime modules in the law book; it holds no runtime itself.\n\n"
        "## Read\nStart at `0401.goal/06.01.md`, the canonical current assignment. Then `0401.goal/01.md`, the goal; `0408.seats`; `0409.decisions`; `0410.imports`; `0611.findings`. The contents are `0011.contents/01.001.md`.\n\n"
        "## Workflow space\nThis book uses workflow space 0 only (`0000`–`0999`). It has no runtime band: modules live in law, `00.00.01.law/0300`–`0399`.\n\n"
        "## Not\nNot the syntax or law book. Not an approval of anything it records.\n"),
    "0014.design/01.001.md": head("01", "0014", "design", "Where this book's designs and pages sit.") + (
        "## Bands\n| Band | Door | Holds |\n|---|---|---|\n| 0100–0199 | `0100.band.returns` | records of returns (the returns themselves are in `returns/`) |\n"
        "| 0400–0499 | `0400.band.dev` | designs, goal, seats, decisions, imports |\n| 0500–0599 | `0500.band.packs` | records of packs and their executions |\n"
        "| 0600–0699 | `0600.band.notes` | findings and carried threads |\n\n"
        "## Pages\nOne number, one name, inside this book. The function pages avoid the module numbers 02–07, so a later design page for a module (for example `0405.clerk`) keeps the same number as its law page (`0305.clerk`).\n\n"
        "## Records\nA page's batch records are `05.NN.md`. The canonical assignment record is `0401.goal/06.01.md`; its schema is on `0410.imports`.\n\n"
        "## Not\nNot a schema approved by the Director: this is the provisional hand form.\n"),
    "0100.band.returns/01.md": door("0100", "band.returns", "returns",
        "None yet. Returns are files in `returns/` beside `packs/` (the Director, 2026-10-26). A member page here would record one.",
        "who: a Builder or Colab returns; the Prime reviews\nmay: one member per return record, linked to its pack\nmay not: accept its own result"),
    "0400.band.dev/01.md": door("0400", "band.dev", "dev",
        "`0401.goal`, `0408.seats`, `0409.decisions`, `0410.imports`.",
        "who: the Prime designs here; the Director decides here\nmay: design one slice per member\nmay not: build or run here"),
    "0500.band.packs/01.md": door("0500", "band.packs", "packs",
        "`0501.bootstrap`: the bootstrap packs (A, B and addendum 001), their releases and outcomes.",
        "who: the Prime records packs; a Builder executes a released pack\nmay: one member per pack line of work\nmay not: run a pack without the Director's release"),
    "0600.band.notes/01.md": door("0600", "band.notes", "notes",
        "`0611.findings`.",
        "who: any seat records a finding\nmay: findings with their source and landing\nmay not: declare a finding fixed without its test"),
    "0501.bootstrap/01.md": head("01", "0501", "bootstrap", "The record of the bootstrap packs: what was packed, released and done, with the evidence.",
                                 "draft. Work page, hand form (Pack B #04).") + (
        "## Packs\n| Batch | Pack | Release | State |\n|---|---|---|---|\n"
        "| `05.01.md` | Pack A, preserve (`pack/PACK-A-preserve.md`) | the Director, chat 2026-10-26 (`>run.pack`) | done, accepted by Prime |\n"
        "| `05.02.md` | Pack B, establish (`pack/PACK-B-establish.md`) with addendum 001 (`addendum-001/ADDENDUM-001.md`) | the Director, chat 2026-10-26 (\"Run addendum-B first then Pack B\") | returned for Prime review |\n\n"
        "## Copies\n`pack/` is the whole Pack A and B package, and `addendum-001/` the addendum package, each byte-exact from the baseline commit `d0bdd53a` (rows K001–K032 of `labs/bootstrap-establish-pass01/evidence/step04/import-copies.tsv`). The originals stay in `packs/`, unchanged.\n\n"
        "## Returns\nThe returns are in `returns/`: `pack-A-preserve-return.md`, the Prime's review of it, and `pack-B-establish-return.md`. They are linked from here, not copied, so there is one authoritative return.\n\n"
        "## Tools and evidence\n- Pack A: `labs/bootstrap-preservation-pass01/` (copy helper, tests, verifier, evidence).\n"
        "- Addendum gate: `labs/bootstrap-git-bytes-pass01/` (`gitbytes.py`, `test_gitbytes.py`, evidence).\n"
        "- Pack B: `labs/bootstrap-establish-pass01/` (inventory, import helper and tests, renderer and tests, writers, checks, evidence).\n"),
    "0501.bootstrap/05.01.md": head("05", "0501", "bootstrap", "Batch. The record of Pack A, preserve before establishing the workspace.",
                                    "ran. Record written after the fact by the executor; the Prime accepted the result.") + (
        "pack: `pack/PACK-A-preserve.md` (sha256 in `pack/manifest.sha256.tsv`)\n"
        "release: the Director, chat 2026-10-26: \"Next pack is back.  Now we have moved \\n\\nwithin lib-build/  we have returns/ packs/  you go here now for them until we finish standing the desk.  >run.pack\"\n"
        "executor: claude-opus-5-5\nreturn: `returns/pack-A-preserve-return.md`\nreview: `returns/pack-A-prime-report-2026-10-26.md` (Codex, Prime): ACCEPT\n\n"
        "#01 >run capture and preflight\nresult: pass. 18 package files, 167 sources, 39 baseline files matched; old checkouts fingerprinted with GIT_OPTIONAL_LOCKS=0.\n\n"
        "#02 >build the preservation helper and prove its refusals\nresult: built (`labs/bootstrap-preservation-pass01/preserve_copy.py`); 20 tests: 19 pass, 1 skipped (symlink creation not permitted).\n\n"
        "#03 >run archive only the pinned rows\nresult: three archive branches and two tags pushed. Final commits e8b1a994da07000fa576fd771e455a94718ed431 (90 rows), 586cfa4ae055c29a98c1106bb70143901c57cc11 (28), fe42b017b5e8c288f70878d696cb227b09ab5a8e (49).\n\n"
        "#04 >run independent verification and return\nresult: first verification FAILED (Git line endings on 29 files; kept as evidence); fixed forward; second verification from a fresh clone PASS, 167/167. Old checkouts unchanged.\n\n"
        "reply: none on this record. The Director's release is quoted above; the Prime's acceptance is in its report.\n"),
}


def main():
    for rel, text in FILES.items():
        p = W / rel
        if p.exists():
            raise SystemExit(f"stop: exists: {p}")
    for rel, text in FILES.items():
        p = W / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
        print(p)


if __name__ == "__main__":
    main()
