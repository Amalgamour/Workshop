# piece agents.axioms

id: agents.axioms
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Axioms pointer
axioms: 1, 5, 7, 9
why: the axioms are the shape every choice is checked against; a pointer keeps one source instead of copies (axiom 8).
authority: workflow/AGENTS.md:3-13 @a00bc53; templates/agents.txt:10-12 @a00bc53; docs/spec/Axioms.md
slots:
  - axioms_hash: sha256 of docs/AXIOMS.md, 12-char prefix
sha256: f802074a9e70410aa9564b70eef6f04d73f8e910ab520adb4fab20b3f0369fbe

wording:
Read docs/AXIOMS.md before you start. Its pinned hash is {{axioms_hash}}. If yours differs, stop and tell Prime.
Check every choice against axioms 1 (authority), 5 (frame), 7 (missing) and 9 (trial).
end wording
