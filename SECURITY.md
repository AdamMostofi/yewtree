# Security notes

## What is stored, and where

Each project's memory lives in `<project>/.agent-memory/`. Its own `.gitignore` (`*`) keeps it out of git. It
holds:
- the full history the plugins capture: prompts, tool calls and their output, assistant messages;
- every version of every file the reconciler sees.

That is everything an agent saw and did in the project, so treat the folder like the project's source and
secrets together. **Don't sync or share it:** the engine warns when a store is in a synced folder (OneDrive,
Dropbox, iCloud, Syncthing and others), because sync clients copy half-written databases and keep copies the
engine can't purge.

## Encryption

- **Archived content:** encrypted with AES-256-GCM, under a random 32-byte data key, with a fresh nonce per
  object. Each object's id is bound in as associated data, so a changed or swapped object fails authentication.
- **Object ids:** keyed hashes (HMAC-SHA256), so an id can't confirm a guessed value.
- **The store's keys** are themselves wrapped with a key-encryption key. It comes from one of three sources,
  chosen when a store is created (`AMEM_KEY_SOURCE`):
  - `key-file` (the default): a random key in `$XDG_CONFIG_HOME/agent-memory/keys/`, outside the store, with
    mode 0600. A copied store can't be read without it.
  - `passphrase`: derived with scrypt from `AMEM_PASSPHRASE`, and cached for 12 hours in the per-user runtime
    folder (`AMEM_PASSPHRASE_CACHE=0` turns that off).
  - `keychain`: the OS keychain, through the optional `keyring` package.
- **What isn't encrypted:** the event log (SQLite) and its indexes. Each event's summary fields are stored in
  plain text there, and summaries include the first 500 characters of each prompt and assistant message, tool
  names, commands and file paths, after secret redaction. Only full payloads and file contents are encrypted
  (checked: a summary written to a store is readable in its files; a payload isn't). Protect the folder with
  file permissions, as you would the project.

## Secrets

- **Redaction:** every payload and summary field is scanned before it is written. A match is replaced with
  `[SECRET:<rule>:<fingerprint>]`, and the value itself is never stored. The rules follow common
  [Gitleaks](https://github.com/gitleaks/gitleaks) patterns (MIT), plus an entropy check.
- **It's best effort:** a secret in a format no rule knows can get through.
- **`amem purge`** removes a leaked value, an object or a whole session for good, and can rotate the data key.
  Only you can run it; it isn't an agent tool.

## What runs

- **Hooks** (Claude Code, Codex, Gemini CLI, Cursor) run `amem` as a local command with the agent's own
  permissions. The OpenCode and Pi plugins run inside those agents. The engine makes no network calls.
- **The session server** that hooks hand their data to listens only on 127.0.0.1.
  - It accepts a connection only with a random token from `<store>/run/server`, a 0600 file.
  - It checks the server id first, so a hook never sends data to an unrelated program that reused the port.
- **Memory never blocks or approves an agent's actions:**
  - every hook exits 0;
  - a broken store becomes a recorded gap, not an error;
  - no permission hook is installed (Cursor's would block on invalid output).
- **Text from memory** goes to the model marked as recorded data, not instructions. That is a convention, not a
  guarantee: a model can still be influenced by text it is shown.

## Reporting

Report a vulnerability privately through GitHub's
[security advisories](https://github.com/AdamMostofi/yewtree/security/advisories/new), not a
public issue.
