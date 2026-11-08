# Brownfield Discovery

Prepare an **existing** software project so autonomous development agents can work on it without repeating a repository-wide investigation.

This repository contains a **proposal (v0.1)** for an information-only discovery agent. The agent prepares instructions and targeted knowledge; it does **not** provision infrastructure, repair application code, create stubs, seed data, or implement tests.

## Target outcome

The first downstream mission is to build a reproducible E2E characterization baseline:

- run the actual application components;
- use Docker for detected databases and message brokers;
- stub everything outside the application boundary;
- prepare reproducible data and identities (with developer guidance where needed);
- exercise UI journeys with Playwright and API-only journeys with Newman;
- link observed behaviors, acceptance criteria, test executions, and evidence.

The discovery agent gathers the information that makes that mission possible. It does not carry out the mission.

## What this proposal includes

- [Objectives and boundaries](docs/01-objectives.md)
- [Discovery output contract](docs/02-output-contract.md)
- [E2E handoff requirements](docs/03-e2e-handoff.md)
- [Evidence and reliability rules](docs/04-reliability.md)
- [Acceptance criteria](docs/05-acceptance.md)
- [Optional Graphify integration](docs/06-graphify.md)
- OpenCode v2 agent: [.opencode/agents/brownfield-discovery.md](.opencode/agents/brownfield-discovery.md)
- On-demand skills under [.opencode/skills](.opencode/skills)
- Target-project output examples under [templates](templates)

## Optional bootstrap for Cursor and OpenCode

A single cross-platform installer offers Basic Memory, MemPalace, Graphify and Context7, while detecting installed tools and preserving existing agent configuration.

```bash
# Linux/macOS: show detected tools without changing anything
python3 scripts/setup.py --check

# Windows PowerShell: same check
py -3 scripts/setup.py --check

# Interactive selection of tools and clients (all changes require confirmation)
python3 scripts/setup.py

# Explicit, non-interactive workstation bootstrap
python3 scripts/setup.py --clients cursor,opencode --tools basic-memory,mempalace,graphify,context7 --yes

# Install client agents and shared skills into an existing project without optional tools
python3 scripts/setup.py --scope project --target /path/to/project --clients cursor,opencode --tools '' --yes
```

The package detects existing CLIs, skips upgrades, and uses an available uv or pipx for missing packages. Cursor and OpenCode receive client-specific agents with shared skills under `.agents/skills`. No memory import, transcript mining, graph indexing, or Git hook installation occurs automatically. Selecting Context7 authorizes registering its hosted MCP endpoint for the selected clients, preserving existing entries. Local memory MCP connections still require `--connect-mcp`.

See [optional tooling setup](docs/07-optional-tooling.md).

**Proposal status:** this is an initial contract and agent prompt, not a proven autonomous discovery implementation. It must be exercised on representative brownfield repositories before being promoted to stable.
