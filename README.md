<p align="center">
  <img src="assets/banner.svg" alt="Yewtree: lossless, tree-structured memory for coding agents" width="100%">
</p>

<p align="center">
  <a href="https://github.com/AdamMostofi/yewtree/releases"><img alt="Release" src="https://img.shields.io/github/v/release/AdamMostofi/yewtree?color=2f6b45&label=release"></a>
  <a href="https://github.com/AdamMostofi/yewtree/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/AdamMostofi/yewtree/actions/workflows/tests.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2f6b45"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-2f6b45">
  <img alt="No network calls" src="https://img.shields.io/badge/network-none-2f6b45">
  <img alt="Encrypted at rest" src="https://img.shields.io/badge/archive-encrypted-2f6b45">
</p>

[![M8ven Score](https://m8ven.ai/badge/mcp/adammostofi-yewtree-nzqgjc?v=6ca62c90f779c7b20953ce7163f53562)](https://m8ven.ai/mcp/adammostofi-yewtree-nzqgjc?s=readme)

<p align="center">
  <b>Your coding agent forgets. Yewtree keeps everything, and shows the agent only what it needs.</b>
</p>

---

## Why

Long agent sessions lose things:
- **Compaction** summarises the past and throws away the detail.
- **A new session** starts from nothing.
- **A notes file** goes stale the moment a file changes behind it.

Yewtree records every prompt, tool call, reply, file version, test run and decision, losslessly, in the project
itself. It keeps that record honest: it checks files against what the agent says it did, and records the gaps.
Then it hands the agent a small, budgeted slice at the moments that matter:
- when a session starts;
- on each prompt;
- right after a compaction.

The rest stays one tool call away.

## How it works

<p align="center"><img src="assets/how-it-works.svg" alt="The agent's hooks hand every event to the amem engine, which records it in the project's memory; memory flows back as an overview, prompt offers, a restore after compaction, and tools." width="100%"></p>

- **Capture never gets in the way.** Every hook exits 0. A broken store becomes a recorded gap, never an error
  in the agent. A session server keeps the store open, so a hook takes tens of milliseconds.
- **Nothing is trusted blindly.** Every file change is checked against what the agent reported, and labelled:
  - `agent_tool`: an agent's edit;
  - `agent_bash`: an agent's command;
  - `git_operation`;
  - `external`;
  - an honest `unattributed`.

  Test results are marked verified, stale or unknown, and say why.
- **Context is a budget, not a dump.** A context manager tracks what the agent has loaded. It offloads finished
  work to one-line references, and restores any reference exactly.

## Four trees, one store

<p align="center"><img src="assets/four-trees.svg" alt="History, Artifacts, Knowledge and State are four navigable trees over one append-only, encrypted store." width="100%"></p>

Each tree answers one question and has its own navigator, and links between trees are explicit. Every record
says how it is known:
- **observed** by the engine;
- **declared** by an agent or by you;
- **inferred** by a named rule.

## Features

**Capture and storage**
- **Event log:** append-only, with a hash chain per writer, so tampering or loss shows up in `amem verify`.
- **Archive:** compressed, encrypted (AES-256-GCM) and content-addressed. Old content is packed losslessly with
  lzma.
- **Secrets:** redacted before anything is written. `amem purge` removes a leaked value for good, and can
  rotate the key.
- **Where it lives:** inside the project, in `.agent-memory/`, which ignores itself in git.

**Understanding the project**
- **Artifacts:**
  - every file version, with rename and revert detection;
  - Python and TypeScript symbols and imports;
  - Markdown and reStructuredText sections and links;
  - full-text search.
- **Knowledge:** decisions, approaches, requirements, constraints, bugs and their fixes, under a topic
  hierarchy, with supersession chains.
- **State:** objectives, tasks, blockers, priorities, focus and next actions, with staleness and token-budgeted
  levels.
- **Verification:** test runs recorded with the files and environment they covered.

**Working with agents**
- **10 memory tools over MCP:** one per tree, plus links, load and get, context (offload, restore, pin),
  storage, and declare.
- **Protected items** (constraints, objectives, open conflicts, the current task) are never evicted silently.
  When they overflow, they are ranked, referenced or counted.
- **Several agents in one project:** a session started in Claude Code continues in OpenCode, and every change
  names the agent and session that made it.
- **Pi's session tree:** forks and `/tree` branches become memory branches.

## What it does, and what it doesn't

| Yewtree does | Yewtree doesn't |
|---|---|
| Keep the full history of a project's agent sessions, losslessly | Send anything over the network: no cloud, no telemetry, no API keys |
| Tell you who changed a file, or say plainly that it doesn't know | Guess: an unexplained change is `unattributed` |
| Give the agent a small overview and point to the rest | Fill the context window with everything it has |
| Work with any agent that has hooks, MCP or just a shell | Block, approve or slow down an agent's actions |
| Prove the record is intact (`amem verify`) | Prove nothing happened before capture started |
| Redact secrets it recognises | Catch every secret format (purge exists for the rest) |
| Encrypt file contents and full messages | Encrypt the event log's short summaries ([SECURITY.md](SECURITY.md)) |

## Agents

<p align="center"><img src="assets/tiers.svg" alt="Three tiers: hooks, MCP only, CLI only." width="100%"></p>

| Agent | Tier | Connect it | Tested |
|---|---|---|---|
| **Claude Code** | Hooks | `claude plugin marketplace add AdamMostofi/yewtree`, then `claude plugin install yewtree@yewtree` | Replayed real sessions |
| **OpenCode** | Hooks | Add `".../plugins/opencode/index.js"` to `plugin` in `opencode.json` | Live, OpenCode 1.18.35 |
| **Pi** | Hooks | `pi install git:github.com/AdamMostofi/yewtree@v0.3.0` | Real runtime, Pi 1.4.0 |
| **Codex** | Hooks | `codex plugin marketplace add AdamMostofi/yewtree`, install from `/plugins`, then trust its hooks in `/hooks` | Built from its docs |
| **Gemini CLI** | Hooks | `gemini extensions install ./plugins/gemini` (from a clone) | Built from its docs |
| **Cursor** | Hooks | `amem setup cursor` | Built from its docs |
| **Windsurf, Cline** | MCP only | `amem setup windsurf` or `amem setup cline` | Built from their docs |
| **Aider** | CLI only | `amem setup aider` | Built from its docs |

"Built from its docs" means the adapter follows the agent's official documentation (read 2026-11-20) and passes
the shared adapter suite. It has not been run against a real install yet. [docs/agents.md](docs/agents.md) has
the details.

## Install

```bash
uv tool install git+https://github.com/AdamMostofi/yewtree@v0.3.0
```

Then connect your agent (the table above), and work as usual. To look at what was recorded:

```bash
amem verify               # integrity, capture completeness, known gaps, uncertain attribution
amem state overview       # what matters now
amem knowledge topics     # decisions, bugs, constraints, by topic
amem history sessions     # every session, by every agent
amem brief                # the memory overview as a file, for agents that only read files
```

The key that encrypts the memory lives outside the project by default. A passphrase or the OS keychain works
too: set `AMEM_KEY_SOURCE` (`key-file`, `passphrase` or `keychain`).

## Records: the engine as a program's store

A program can keep its own data in the engine as records (0.3.0). The engine stores, versions, indexes and
links them; the program decides what they mean. [ADAM](https://github.com/AdamMostofi/ADAM) keeps its facts and
derivations this way.

```python
from agent_memory import Store

store = Store("facts.engine", project_id="myapp", profiles=["generic"])
store.put_record("myapp.fact", "socrates|is|man", {"subject": "socrates", "object": "man"},
                 "session-1", "myapp", index=["subject"])
store.find_records("myapp.fact", subject="socrates")      # current versions whose indexed field matches
store.record_history(Store.record_id("myapp.fact", "socrates|is|man"))   # every version, oldest first
```

`put_records` stores many records and the links between them in one transaction, all or none.

## Measured so far

These come from the test suite and from replays of real sessions, not from a benchmark:

| What | Result |
|---|---|
| Hook latency through the session server (replayed Claude Code sessions) | p50 36–39 ms, p95 103–150 ms |
| Per event in OpenCode and Pi | 8–46 ms and 10–75 ms |
| Recall on prompts that share no words with what they need (test fixture) | 20% before, 80% after task- and link-aware retrieval |
| Memory overview at session start | about 390 tokens |
| Tool definitions | about 1,224 estimated tokens |

**The benchmark against plain compaction and against notes with git and grep is designed but not run.**
[benchmark/RESULTS.md](benchmark/RESULTS.md) says why. Until it runs, there is no evidence that Yewtree reduces
stale-state errors. That is the claim it exists to test.

## FAQ

**Does it need an API key, a model or an account?** No. The engine runs locally with no model and no network.

**Where is my data?** In `<project>/.agent-memory/`, encrypted, with the key outside the project.
[SECURITY.md](SECURITY.md) lists exactly what is encrypted and what isn't.

**Will it slow my agent down?** Hooks hand their data to a session server, in tens of milliseconds. If anything
fails, the agent carries on and the failure becomes a recorded gap.

**Can I use it with two agents at once?** Yes. Each change names the agent and session that made it. When two
agents' commands could both explain a change, both are listed and neither is picked.

**Why "Yewtree"?** Yews live for thousands of years and keep growing around their own past. Its logo's four
branches are the four trees, growing from one root: the archive.

## Development

```bash
git clone https://github.com/AdamMostofi/yewtree && cd yewtree
uv sync --locked --extra dev
uv run pytest -q
```

**Names:** the command is `amem`, and the Python package is `agent_memory`. Yewtree was built inside
[ADAM](https://github.com/AdamMostofi/ADAM) under the working name `agent-memory`, and moved here with its
history. The design documents are there:
- [architecture revision 3](https://github.com/AdamMostofi/ADAM/blob/master/docs/design/2026-11-13-memory-architecture-rev3.md);
- the [original design](https://github.com/AdamMostofi/ADAM/blob/master/docs/design/2026-11-06-agent-memory-engine.md).

## License

[MIT](LICENSE). Third-party licenses are in [THIRD_PARTY.md](THIRD_PARTY.md).
