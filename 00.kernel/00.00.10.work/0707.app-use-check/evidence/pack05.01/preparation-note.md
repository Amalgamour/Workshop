# Pack dependency correction before release
2026-11-01, Codex Prime. First preparation incorrectly required a live
return-line-layout.json. That file is absent; pilot.py only checks whether it exists
before/after. Removed the nonexistent input requirement before release. No fixture
layout was fabricated, and no live file or captured record changed. First preparation
failure remains in the Codex tool transcript. Supplied sources are frozen below
sources/ and bound by source-manifest.json. This is an unreleased pack correction.
