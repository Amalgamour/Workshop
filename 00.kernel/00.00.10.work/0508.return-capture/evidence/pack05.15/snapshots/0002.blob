# Prime review — 0508/05.14
Date: 2026-10-28. Reviewer: Codex Prime.

HELD for BO-05. The14-test suite passes independently in a disposable checkout.
The repaired code now controls the previously reproduced declaration crashes,
retains duplicate field evidence, records live times, and tests reservation state
in a disposable book. Fresh0140 capture verify is complete, not acceptance.

BO-05: collect_fields() starts in header mode but treats the opening level-one
page title as an unrelated section. Actual workbook pages start with '# 05 — …',
followed by stamp/header fields, so their state is now silently lost. Independent
probe of the actual05.14 finds state: draft in source, but fields.state is empty.
A minimal normally shaped title/header/Assignment/Return fixture reproduces it.

Preserve initial title plus header scanning until the real body boundary. Do not
reopen header mode for a later quoted/example/body title. Keep fence, blockquote,
duplicate and source-kind guards. Test actual corpus header values, not just small
title-free snippets. No new interpretation of release prose or automatic closure.

The raw Release-and-claim pointer guidance and the actual Release line both remain
visible as duplicate eligible evidence on this page. That conservative ambiguity
is not authority and is not to be silently resolved in this narrow repair.

Next action: a focused initial-title/header repair and regression tests before
integration. No state projection/app/dependency changes. Other workers untouched.
