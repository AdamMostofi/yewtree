# Changelog

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
