# pack-authoring-pass02

Successor of `labs/pack-authoring-pass01` for usable typed forms and review binding. Pass01 stays byte-stable. This module loads it under a private name and replaces the form, review, and derived-face seams.

The field list is `forms/build-pack-v1.json`, schema `authoring-forms/1`. The form command and the validator both read that file. Named forms are intent, item, note, disposition, and review.

Review compares `--draft-sha256` to the candidate Prime inspected, then stores a separate final-document hash. Freeze checks both. Ordinary face replacement is `draft.md.history-<operation>`. A face that does not match the previous canonical render is `draft.md.divergence-<operation>`.

The app door is `app/authoring_tools_v2.py`. Help is `PRIME-USE.md`. This lab is not approval, release, or the Prime pilot.
