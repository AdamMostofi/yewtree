# Changelog

## 0.3.0 (2026-11-24)

**Generic records**, so a program can keep its own data in the engine. Built for
[ADAM](https://github.com/AdamMostofi/ADAM), which now keeps its facts, derivations, sources, passages, skills and
traces here (ADAM Stage 4.1).

- **Records:** a caller-defined type (such as `adam.fact`), a key, fields, an optional body and a list of fields
  to index. The engine stores, versions, indexes and links them, and never interprets them.
  - `put_record`, `put_records` (many puts and their links in one transaction), `retire_record`, `get_record`,
    `record_body`, `record_history`, `find_records(type, **equals)`, `records(type)` and `record_edges`.
  - Every put is a new version, and nothing is overwritten. A put that changes nothing stores nothing; a
    caller that tracks its own changes can pass `check_unchanged=False` to skip that lookup.
  - A body is archived like any payload: compressed and encrypted. Fields are in the event summary, so they
    are searchable and redacted, not encrypted.
  - Records are nodes of the knowledge tree, under the topic `records/<type>`, and rebuild from the log.
- **Links:** a new basis, `recorded` (the caller states the link as a fact of its data), and attributes on a
  link (`relate(..., attrs=...)`), such as a premise's position.
- **Fixed:** opening a store with the profiles it already has no longer writes to it.

## 0.2.0 (2026-11-20)

**Renamed to Yewtree** (the owner's choice). The repository is now
[AdamMostofi/yewtree](https://github.com/AdamMostofi/yewtree); GitHub redirects the old URL.

- **New names:** the package is `yewtree`, and so are the Claude Code, Codex and Gemini CLI plugins. The OpenCode
  and Pi plugins are `opencode-yewtree` and `pi-yewtree`.
- **Unchanged:** the `amem` command, the `agent_memory` Python package, the `agent-memory` MCP server and the
  `.agent-memory/` store folder. Existing stores keep working.
- **Claude Code:** if you installed the 0.1.0 plugin, reinstall from the new marketplace:
  `claude plugin marketplace add AdamMostofi/yewtree`, then `claude plugin install yewtree@yewtree`.
- **New:** a landing README, a logo, a banner and diagrams (`assets/`).

## 0.1.0 (2026-11-20)

The first release, extracted from the [ADAM](https://github.com/AdamMostofi/ADAM) repository with its history.
It was built there under the working name `agent-memory`.

- **The engine:**
  - lossless capture into an append-only, hash-chained event log and an encrypted, content-addressed archive;
  - four navigable trees: history, artifacts, knowledge and active state;
  - file reconciliation with honest attribution;
  - verification records, a context manager with offload and restore, and 10 MCP tools.
- **Agents:**
  - **Claude Code:** plugin and marketplace.
  - **OpenCode:** plugin.
  - **Pi:** package.
  - **Codex and Gemini CLI:** packaging, built from their docs and untested.
  - **Cursor, Windsurf, Cline and Aider:** `amem setup`, built from their docs and untested.

  [docs/agents.md](docs/agents.md) says what each gets, and how far each was tested.
- **Not included:** PyPI and npm packages. Everything installs from this repository.
