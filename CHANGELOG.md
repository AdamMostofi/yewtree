# Changelog

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
