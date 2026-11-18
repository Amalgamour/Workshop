# CONTRACT delta — truthful basis and digest-only pins (0525.app-dependencies 05.02)

Written before the successor reader and before the versioned app records. The 0517 build05.01 contract and the build05.02 delta stay in force for module-declaration/1. This page adds module-declaration/2 and module-declaration-set/2. It does not change module-change/1 or module-dependency-result/1. It seats nothing and accepts nothing.

The reader is a new file, labs/module-dependencies-pass02/depdecl.py. labs/module-dependencies-pass01/depdecl.py stays the accepted predecessor and is not edited. The new file answers the same commands. It does not import, execute, or follow a declaration name. It does not launch Git, a network tool, or a named module.

## 1. Which schema applies

- A module-declaration-set/1 contains only module-declaration/1 records. A /2 record in that set is a refusal.
- A module-declaration-set/2 may contain /1 and /2 records. Each record is checked by its own schema.
- An unsupported schema or an unsupported basis kind is a refusal. It is not stored as git-blob and it is not dropped.
- /1 command output stays the predecessor output. Fields that name a /2 pin form or a /2 basis are omitted for /1 records.

## 2. Source basis (D-04)

module-declaration/1 basis stays exactly kind, repository, commit, path, and kind must be git-blob. That rule is unchanged, including the records that already use it.

module-declaration/2 basis is one of these two shapes.

git-blob, keys kind, repository, commit, path, verification:

- verification must be the string supplied-unverified.
- commit is a supplied reference. This reader does not fetch Git, does not compare the commit with a blob, and refuses verification values such as verified.
- A hash of the implementation bytes does not authenticate authorship, a commit, or environment readiness.

observed-file, keys kind, repository, path, form, context_head:

- form is working-tree or frozen-file.
- context_head is null or a 40-digit hex commit. It is observation context. It is not a claim that the commit identifies the bytes.
- A commit key on this kind is a refusal. The reader will not coerce the record into git-blob.

implementation.sha256 and implementation.bytes remain the measured file identity. The reader does not treat them as a Git check.

## 3. Pins (D-05)

A /1 pin is null, or {sha256, bytes} with bytes a non-negative integer. bytes null is a refusal on /1.

A /2 pin is one of three relationships:

- null, and pin_required false: genuinely unpinned. Resolution stays selected or single-unpinned.
- {sha256, bytes null}, and pin_required true: digest-only. The caller enforces the digest and does not enforce a length.
- {sha256, bytes integer}, and pin_required true: digest-plus-length, the existing pair.

On /2, pin_required is true exactly when a pin object is present.

Digest-only resolution compares implementation.sha256 only. One clean match is resolved. No match is pin-differs. Several matches are identity-conflict. The declared length is not read, so a missing enforcement length cannot become identity-pair-mismatch and cannot become a size match. The digest check stays on.

Pair resolution is the predecessor rule: sha256 and bytes, then identity-pair-mismatch or pin-differs.

impacted pin_vs_declarations:

- unpinned when the pin is null
- digest-matches or digest-differs for a digest-only pin
- matches-declared, pair-mismatch, or undeclared-bytes for a pair pin

digest-differs and pair-mismatch are findings. digest-matches, matches-declared, and unpinned are not. --implementation stays sha256 only. A digest-only pin with that sha is pin-matches. A missing pin length does not skip the digest comparison.

identity still measures fixture copies against implementation.sha256 and implementation.bytes. On a set that contains a /2 record, each fixture row also lists incoming pin forms. A digest-only pin that shares the fixture sha is digest-matches. It is not reported as a pair match. Fixture length remains the implementation measurement, separate from the pin.

delta keeps module-change/1. A /2 record may be a creation or a revision. A pin that changes from null to digest-only is a changed pin.

## 4. What stays limited

Address targets stay address-unresolved. The reader does not open them. Face tokens with an extra segment stay outside the address form. A stored JSON hash that the file does not check stays an unpinned document edge. A path named in source and not loaded stays a provenance link when that is how the /1 record stated it. Environment rows stay unverified. complete_claim stays false. complete-for-declared-coverage is not closure, readiness, or acceptance.

## 5. The corrected app set

labs/app-dependencies-pass02 is a new selected set, review-loop-entry-2, schema module-declaration-set/2. Each record is module-declaration/2 version 2 and supersedes the version 1 id in the preserved /1 set. Edges, conditions, and pair pins are the /1 edges except the two representation repairs.

The three paths whose working-tree git object equals HEAD use git-blob with verification supplied-unverified. The nine paths that do not use observed-file, form working-tree, and context_head set to the observed HEAD. The reader does not re-check that classification.

return-inspect-pass01 requirement return-capture becomes digest-only: sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac and bytes null. Source: labs/return-capture-pass01/return_inspect.py pin_bytes, lines 49-71, compares HELPER_SHA256 and does not compare length. The observed length 45767 stays on the helper's implementation row.

Exit 0 is an answer about declarations. It is not Prime review and not production classification.
