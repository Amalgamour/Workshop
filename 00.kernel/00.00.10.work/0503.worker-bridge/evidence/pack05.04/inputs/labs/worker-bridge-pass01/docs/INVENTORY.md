# Model connection inventory (batch `0503.worker-bridge/05.01` #01)

**who:** claude-opus-5-5, Colab · **date:** 2026-10-26 · **machine:** the Director's Windows desktop (`D:\Git\lib-build`)

**How this was found:** only executables on PATH (`command -v`, `where.exe`), each tool's `--version` and `--help` text, and Python's module lookup. **Not done:** no model task was run, and no API call, credential, token, config file or user history was read. Whether a tool is signed in, and what each sign-in permits, is therefore **unknown**. Raw outputs are in `evidence/inventory/`.

## What is on this machine

| Mechanism | Found | How known | Headless use (from `--help`) | Unknown |
|---|---|---|---|---|
| Claude Code CLI | `C:\Users\misg\.local\bin\claude.exe`, `2.1.275 (Claude Code)` | `claude --version`, `claude --help` | `-p/--print` (one response, then exit); `--output-format json` or `stream-json`; `--input-format stream-json`; `--json-schema`; `--no-session-persistence`; `--max-budget-usd`; `--permission-mode`; `--tools`, `--allowedTools`, `--disallowedTools`; `--add-dir`; `--restricted` (removes command- and code-running tools and WebFetch unless named, confines file tools to the working folders, refuses `bypassPermissions`); `--bare` (Anthropic auth strictly an API key or `apiKeyHelper`) | whether it is signed in non-interactively; whether a desktop/subscription sign-in covers `-p` use; cost |
| Grok CLI | `C:\Users\misg\.grok\bin\grok.exe`, `grok 1.0.70 (f50904eaee6c) [stable]` | `grok --version`, `grok --help` | `-p/--single <PROMPT>`, `--prompt-file`, `--prompt-json`; `--output-format json`, `streaming-json`; `--json-schema`; `--max-turns`; `--permission-mode`; `--sandbox <PROFILE>`; `--cwd`; `--disable-web-search`; `--no-subagents` | sign-in state; which sandbox profiles exist; whether a session is persisted by default |
| Codex | not on PATH (`where.exe codex`: not found) | `command -v`, `where.exe` | none found | how Codex is reached here (likely another app); not usable from this process |
| Python SDKs (`anthropic`, `openai`, `xai_sdk`; HTTP clients `httpx`, `requests`) | none installed | `importlib.util.find_spec` | n/a | API keys were not looked for, and no install was made |
| A manually relayed file | always possible | by construction | the Director copies a request file to a model and returns its result file | needs a person in the loop for every exchange |

A chat or desktop subscription is not evidence of API access, and none is assumed here.

## The smallest real exchange to test next

**Recommended: one Claude Code CLI round trip,** through this lab's adapter, as a new backend profile. Use the same envelope and verifier, and a separately released delivery.

- **Profile, exact argv:** `claude -p --restricted --output-format json --no-session-persistence --max-budget-usd <cap> --tools Read,Write`
  - The prompt is passed on stdin.
  - The working directory is a fresh, empty output root inside the lab. `--restricted` confines the file tools to the working folders; the input is copied into that root.
- **Task:** the same fixed job as the fixture: read `input.txt`, write `result.json` holding `{"count": N}`, and answer with a `worker-bridge/result@1` JSON object.
- **The adapter adds one parsing step:** the CLI's JSON wrapper holds the model's text. That text must parse as the result object, or the receipt says `malformed`.
- **What it would prove:** a real model process can take a recorded request through the adapter and return a correlated, hash-verified artifact. **What it would not prove:** a Clerk dispatch, a schedule, a cold boot, a sandbox, or that the answer is right; review is still another seat's act.

**Why this one:**
- It is already installed.
- It has a documented one-shot mode with JSON output.
- It has a documented confinement flag and a spend cap.
- No new dependency or service is needed.

Grok's CLI looks equivalent (`-p` and `--sandbox`) and is the natural second backend, so the adapter is shown not to depend on one vendor.

## What is missing before that exchange

1. **A named release of that connection** by the Director: which CLI, which account or sign-in, a spend cap, and how many exchanges. This batch did not authorize any real model call.
2. **Whether the CLI is signed in for non-interactive use on this machine.** This could only be learned by running it, which wasn't permitted here.
3. **Whether `--restricted` plus `--tools Read,Write` is the confinement the Director accepts,** or whether a sandbox profile or a separate OS account is wanted first.
