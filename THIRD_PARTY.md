# Third-party notices

Checked 2026-11-20 for v0.1.0.

**Runtime dependencies** (installed separately, not bundled):

| Package | Version checked | License |
|---|---|---|
| cryptography | 50.0.2 | Apache-2.0 OR BSD-3-Clause |
| tree-sitter | 0.26.1 | MIT |
| tree-sitter-python | 0.25.0 | MIT |
| tree-sitter-typescript | 0.23.2 | MIT |
| cffi (through cryptography) | 2.1.1 | MIT-0 |
| pycparser (through cffi) | 3.12 | BSD-3-Clause |

**Adapted, not copied:** the secret-detection rules in `src/agent_memory/secrets.py` follow common patterns from
[Gitleaks](https://github.com/gitleaks/gitleaks), licensed MIT (Copyright (c) 2019 Zachary Rice).

**Agent plugins:** the plugins call each agent's documented plugin, hook and MCP interfaces. They bundle no code
from those agents. Pi's own packages are a peer dependency, supplied by Pi.
