# A Linux packed suite will auto-fail a Windows check

**What happened.** 90.50.10.0404.05.02 packed `cargo test --test wf`. The Done when allows the five named Windows failures, and asks the suite to pass on Linux. Grok-Check ran the packed command on Windows. It failed, so wf marked the check fail, even though the checker's own judgments said both Done when lines were met.

**Why.** wf fails the check when any packed command exits non-zero. It does not apply an allowed-failure list.

**What to do next time.** A "pass on Linux" check must be run on Linux. Do not pack `cargo test --test wf` for a Windows checker until 0416 fixes those five fails.

**Source.** Grok-Check report `reports/90.50.10.0404/05.02/Grok-Check-check-20261123-1150.md` on returns `c48ec491`; close `411a014e`.
