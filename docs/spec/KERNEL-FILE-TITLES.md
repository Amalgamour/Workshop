# Kernel file titles: the spec

state: describes kernel/build.mjs on branch build at 9cf70d7. One builder choice is marked 7 (the axioms, section 4).
made: Thu 19 Nov 2026, by Prima builder-b22, because Matthew asked.
Director's words: docs/review/DIRECTOR-WORDS-t375u-t377u.md. t375u: "I need you to see this.  Notice you have no titles on these pages." t377u: "Yes rename the kernel files".
rule source: docs/spec/seqpage.md section 2 (lines 18-27) and docs/spec/seqAddr.md section 3 (lines 108-116, A2.8, A3.2).
the story: docs/journal/2026-11-19-kernel-file-titles.md.

## 1. The rule

A kernel source file holds one face of one page. Its name is:

```
DD.SS.BB.PPPP.title.FF[.NN][.tail].md     00.00.00.0051.seqaddr.01.draft.md
DD.SS.BB.PPPP.FF[.NN][.tail].md           00.00.00.0000.00.draft.md   (page 0000 has no title, A2.8)
```

- The title is the `title:` line of the page's face 00 stamp. The stamp is the truth; the name copies it (seqAddr.md:116).
- Page 0000 (a door) never has a title in its name, even when its stamp has one (A2.8).
- A page whose stamp has no title has no title in its name (seqpage.md section 2).
- The title sits right after the address, before the face. A word after the face would be a card key (seqAddr.md:111), so it cannot go there.

Why: a file list of bare numbers tells a reader nothing until each file is opened (t375u). The spec already put the title in the name (seqpage.md section 2); the kernel files had never used it.

## 2. A title is a label, not identity

The face's address does not change. `kernel/00.00.00/00.00.00.0051.seqaddr.01.draft.md` is still the face `00.00.00.0051.01.draft`. Books, seats, trial PASS lists, registries and cites by address are all unchanged (A2.4: `4442` and `4442.timer` are the same page). The exported books are byte-identical before and after the rename.

## 3. A mismatch is elevated, never fixed

`node kernel/build.mjs` checks every name on a page against its face 00 stamp. Each of these stops the build with "elevate to Director; the stamp title is the truth and a name is never fixed silently":

- a name with no title when the stamp has one (the old name form);
- a name whose title is not the stamp title;
- a name with a title when the stamp has none;
- a page 0000 name with a title;
- a stamp title that is not a legal title word (seqAddr.md:281: lowercase letters, digits and hyphens, a letter first, not a tail word);
- an axioms stamp title other than `axioms` (section 4).

The builder never renames a file. Which side is wrong, the name or the stamp, is the Director's call (A2.8, A3.2).

## 4. The axioms (7, builder choice)

The axioms live at the working address `00.00.axioms` (R6), whose last word already is their title. Their files keep the names `00.00.axioms.FF[.NN][.tail].md`; a second `axioms` would only repeat it. The build checks that the axioms stamp says `title: axioms`. If Matthew wants the names to follow the page form exactly, this is the one place to change.

## 5. Old names in history

Trials and seats made before the rename name the old files. The builder still reads them:

- the seat-history walk (`FACE00`) reads face 00 files under either name form;
- the trial-tree check (`inTrialTree`) takes the title out of a name before it compares, so an old trial commit still matches.

So every seat made under the old names still verifies (seats 26, 0 errors).

## 6. What was renamed

65 files: all faces of pages 00.00.00.0051 to 0057 (seqaddr, faces, tails, types, brands, drafting, workflow-loop), samples 10.11.21.0012 (dictionary), 0013 (common-questions) and 1001 (bob), and the parked override 10.11.21.0001 (override-drafting). Not renamed: every page 0000 (kernel, samples and the parked doors), and the axioms (section 4).

## 7. What was not changed, and why

- Seated faces, including every seated 05.02 work pack, keep their old path text in grant:, path: and done: lines. A seated face is pinned by its git blob (R2); editing a path would unseat it and need a new trial. Glob lines such as `kernel/00.00.00/00.00.00.0051.*.draft.md` still match the new names. Exact lines such as `kernel/00.00.00/00.00.00.0051.04.draft.md` now name a file that is gone; read them by address. This is raised for the Director.
- Records of the past keep the names they had: docs/trial/, docs/BUILD-LOG.md, docs/design/DECISIONS-LOG.md, test and evaluation notes tied to a commit, docs/review/DIRECTOR-WORDS-*, books/, export/ and the exported example docs/spec/examples/real/10.11.21.1001.bob.seq.
