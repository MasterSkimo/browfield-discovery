# Brownfield Discovery

Prepare an **existing** software project so autonomous development agents can work on it without repeating a repository-wide investigation.

This repository contains a **proposal (v0.2)** for a discovery agent that investigates the application and **creates the dedicated E2E Docker foundation** (Compose, application build definitions and isolated configuration). It never rewrites the real application or developer profiles and does not implement complete stubs, seed data or tests.

## Target outcome

The first downstream mission is to build a reproducible E2E characterization baseline:

- run the actual application components;
- use Docker for detected databases and message brokers;
- stub everything outside the application boundary;
- prepare reproducible data and identities (with developer guidance where needed);
- exercise UI journeys with Playwright and API-only journeys with Newman;
- link observed behaviors, acceptance criteria, test executions, and evidence.

The discovery agent gathers the information **and creates the Docker starting point** for that mission. The E2E agent finishes the stubs, data and verification. The E2E-bootstrap agent is not expected to behave like a developer with IDE-launched components: its preferred target is a self-contained Docker Compose project that **builds and runs the real applications**, databases, brokers, external stubs and test runners as needed, with dedicated application profiles/config and environment overrides.

## What this proposal includes

- [Objectives and boundaries](docs/01-objectives.md)
- [Discovery output contract](docs/02-output-contract.md)
- [E2E handoff requirements](docs/03-e2e-handoff.md)
- [Evidence and reliability rules](docs/04-reliability.md)
- [Acceptance criteria](docs/05-acceptance.md)
- [Optional Graphify integration](docs/06-graphify.md)
- [Investigation and inference protocol](docs/08-investigation-protocol.md)
- [Proposed phased discovery workflow](docs/09-discovery-workflow.md)
- [Interactive developer clarification](docs/11-interactive-clarification.md)
- [Compose-first E2E runtime contract](docs/10-compose-first-handoff.md)
- OpenCode v2 agent: [.opencode/agents/brownfield-discovery.md](.opencode/agents/brownfield-discovery.md)
- On-demand skills under [.opencode/skills](.opencode/skills)
- Target-project output examples under [templates](templates)

## Run a complete discovery

After installing the agent and commands in the **target** project or globally:

~~~text
# From T3 Code with OpenCode provider or OpenCode itself (start a new thread)
/brownfield-discover

# From Cursor's Agent input
/brownfield-discover
~~~

The command follows phases D0–D7 from [the workflow](docs/09-discovery-workflow.md), records progress, **creates .e2e/compose.yaml, Dockerfiles and E2E profiles/env example when required**, documents their status, and invokes source-backed inference. It must generate a working AGENTS.md that follows https://agents.md/ (real setup/build/run/test instructions, module boundaries, conventions and delivery rules), not a list of links.

For noninteractive OpenCode runs from the target repository root:

~~~sh
opencode run --agent brownfield-discovery "Run the complete brownfield discovery for this repository, including cross-source inference, operational AGENTS.md and the quality gate."
~~~

In T3, commands must **start** the message. If the provider does not display the new slash command yet, refresh provider status and restart the agent session. If a particular T3 build does not expose the command, send the same explicit prompt to the brownfield-discovery agent; this avoids silently running a normal chat response. The structural quality gate is:

~~~sh
python3 .agents/brownfield-discovery/scripts/validate_discovery.py --project .
~~~

After D6, if justified unknowns remain, the agent **asks the user the first clarifying question in the chat** (with source evidence and hypothesis) and persists `awaiting_user`. Reply in the same conversation, or resume in T3/OpenCode or Cursor using `/brownfield-clarify`. An answer is cross-checked against the repo before changing the Docker foundation and `AGENTS.md`. If no meaningful developer questions exist, D7 completes without an interview.

Use the globally installed copy from ~/.agents/brownfield-discovery/scripts when working with global agent configuration.

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

The package detects existing CLIs, skips upgrades, and uses an available uv or pipx for missing packages. The installer also deploys both provider slash commands, shared inference skill, templates, and validation script. Cursor and OpenCode receive client-specific agents with shared skills under `.agents/skills`. No memory import, transcript mining, graph indexing, or Git hook installation occurs automatically. Selecting Context7 authorizes registering its hosted MCP endpoint for the selected clients, preserving existing entries. Local memory MCP connections still require `--connect-mcp`.

If you previously installed the earlier version, a default reinstall preserves existing files and reports conflicts. To explicitly replace old brownfield agent, command and skill files **with per-file backups**, add --upgrade-agent-files:

~~~sh
python3 scripts/setup.py --clients cursor,opencode --tools '' --upgrade-agent-files --yes
~~~

See [optional tooling setup](docs/07-optional-tooling.md).

**Proposal status:** this is an initial contract and agent prompt, not a proven autonomous discovery implementation. It must be exercised on representative brownfield repositories before being promoted to stable.

## Concrete Docker handoff

Discovery produces `.e2e/compose.yaml`, `.e2e/.env.e2e.example`, `.e2e/.gitignore` and project-specific Dockerfiles/configuration under `.e2e/` where necessary. It also writes `.agent-context/environment-blueprint.md` with actual created paths, service boundaries and remaining downstream work. If Docker Compose is available it attempts `docker compose -f .e2e/compose.yaml --env-file .e2e/.env.e2e.example config --quiet`, recording the actual result. **This is not a passing application build or E2E run.** The next agent completes test data, stubs, Playwright/Newman and execution evidence. See [the workflow](docs/09-discovery-workflow.md) and [Docker contract](docs/10-compose-first-handoff.md).
