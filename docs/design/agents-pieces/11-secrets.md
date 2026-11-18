# piece agents.secrets

id: agents.secrets
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Secrets
axioms: 1, 7
why: a token in a file a model can read lets anyone who reads it act as its owner.
authority: `7` (missing): no recorded Director ruling found. Evidence only: CORE-AND-TOOLS-SPEC.md:234-236 (token file risk); INSTRUCTION-GUARD-t309u.md:116 (L3). Needs his ruling before approval.
slots: none
sha256: 3509ca2ca5ac6da531efc8d29f5e2195120368a7196d45fe846b4c793bccc992

wording:
Never print, copy or commit a token, password or key. If you find one, stop and tell Prime where, without its value.
end wording

authority update (Prima, 3:33 PM EST Nov 18): Director approved this rule text, docs/review/DIRECTOR-WORDS-t335s1296.md.
