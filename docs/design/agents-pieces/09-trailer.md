# piece agents.commit-trailer

id: agents.commit-trailer
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Commit trailer
axioms: 6
why: every commit names which model made it, so lineage can be traced.
authority: trailer: docs/CONTRACT.md:26; DECISIONS-LOG.md D295. Staging line: older words AGENTS.004.md:22 (lib build, draft, never in force); `7`: no recorded Director words for it yet.
slots:
  - trailer: exact text `Model: Grok Bot (<seat>)`, seat from the seat list
sha256: 067058a346411353bc802d6642ad4ef3fc9602957b436de8cd4d8976f9ab7fd0

wording:
End every commit message with a blank line, then `{{trailer}}`.
Stage files by path only. Never `git add -A`, `git add .` or `commit -a`.
end wording

authority update (Prima, 3:33 PM EST Nov 18): Director approved this rule text, docs/review/DIRECTOR-WORDS-t335s1296.md.
