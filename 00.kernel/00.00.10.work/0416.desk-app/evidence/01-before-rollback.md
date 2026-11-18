# Desk application: immediate milestone
date: 2026-10-31
who: Codex Prime
state: Director-approved direction; implementation design pending Colab

## Director instruction
The Director approved a small local app as the front door to the desk, with every
session connecting to receive assignments and submit work. It must work for the
current Prime before broader rollout. The Director approved isolating Claude for
labs and proposed design, followed by design discussion and Colab before building.

Latest reply preserved verbatim:
> 1. Agreed made it happen
> 2. Ok, I need to remove build an isolated room for Claude to work in from now on.  Lets get that up next
> 3. agree, we need to spend some time on design and colab it.
> 4. I agree.
> 5. I agree, it works for you, before it works anywhere else.

## First supported path
Connect session -> orient -> receive bounded assignment -> submit proposal ->
compute constructs candidate and runs checks -> review exact differences ->
record Director approval -> compute applies approved bytes -> recover after restart.
The service owns controlled records and active artifacts. Models propose content
and changes. Unchanged sections are copied from their sources. Removed, moved or
merged sections require recorded dispositions and applicable authorization.

## Finish condition
In a disposable desk, a fresh session discovers its task without chat explanation,
submits a section change, receives refusal for an unexplained removal, corrects
the proposal, and the service applies only the approved candidate. A restarted
session recovers the durable state and pending work. Demonstrate the current
Prime using that same path before any broader migration.

## Scope and roles
Claude: bounded labs, integration evidence, proposed architecture and independent
reviews. No production implementation or edits to the live desk.
Codex Prime: reconcile design with Director intent, prepare implementation packs,
review returns and preserve learning. Grok Build: released implementation packs.
Compute: construct, preserve, check and enforce transitions; it does not judge
meaning. This direction is architectural, not a finding that watermarking caused
a defect, and applies regardless of model provider.

Prioritize this complete path over unrelated feature expansion. This does not
erase old tasks, close findings, approve unreviewed returns or activate runtime.
No automatic model launches, paid calls, remote bots or orchestration in slice 1.
AR-01 remains held until the hard-link race is addressed; no held fixtures or
broad tests exercising that path are authorized by this assignment.

## Claude room
Local room: D:\Git\lib-claude-lab. Source is a committed, pinned export with no
Git metadata, remotes, credentials or live links. It intentionally excludes local
uncommitted changes and Claude's unreviewed 0518 return. Missing work is missing,
not evidence that a proposed module does not exist. Request any additional source
through Prime. The source manifest identifies the scope and exact bytes.

A separate folder is not a security boundary. Current provisioning does NOT
restrict the Windows account or the Claude host. Before executing a Claude lab,
verify a host sandbox limited to this room, or an OS/container boundary with only
this room writable and no live workspace mounts or host credentials. Until then,
the assignment is prepared but execution is held. Do not test isolation by
attempting writes to actual live artifacts. Use designated disposable canaries.

## Next bounded action
Establish and verify Claude's host boundary, then release room assignment 0001.
Its output is an evidence-backed integration map and proposed minimal design,
not an app build. Prime and Director discuss it, then a separate cold Colab
reviews it before Grok implementation packs are released.

## Discovery
See 06.01.md for provisioning evidence. This page records the new development
priority; it does not silently rewrite the old current-assignment schema or
claim the historical boot selector already supports this new route.
