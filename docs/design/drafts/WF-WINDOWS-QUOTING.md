How wf runs a check. Source: src/cmd.rs:752 and src/git.rs:110-112, in the wf build from a823ee28.

The checks field is split only on semicolons. wf does not split a command on spaces. Each piece is one string. On Linux, wf runs sh -c with that string. On Windows, wf runs cmd /C with that string as the single argument after /C. cmd.exe then parses the string. ^ is cmd's escape character. A quoted pattern that contains ^ is not kept as written, because cmd treats ^ as special when it handles quotes after /C. git grep -q exits 1 and prints nothing when the pattern misses, so the check fails with an empty diagnostic.

Safe form, run on Linux against labs/0702/LAB-0702-SEQ-GRAMMAR.md (headings "## 0." through "## 7." all matched):
git grep -q -E ##[[:space:]]0[.] -- labs/0702/LAB-0702-SEQ-GRAMMAR.md

No caret, no quotes, and no space inside the pattern. That pattern is one token. cmd's special characters are & < > ( ) @ ^ | and this token has none of them. Do not use git grep -q -F -e ##.0. Fixed-string search is literal, and the heading is "## 0." with a space, so that pattern does not match.

The published 0702 05.02 checks use the caret form and fail on Windows. The published 0703 05.02 checks are cargo test --manifest-path labs/0703/Cargo.toml and two git ls-files lines. They have no caret and no quotes, so they do not have this bug. Those packs are unchanged.
