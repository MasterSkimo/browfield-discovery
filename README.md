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

## Try the agent with OpenCode v2

Run from **this** repository to install global copies, then start OpenCode from the **target** project root:

```sh
# Copy only the agent and its discovery skills; do not replace unrelated global configuration.
mkdir -p "$HOME/.config/opencode/agents" "$HOME/.config/opencode/skills"
cp .opencode/agents/brownfield-discovery.md "$HOME/.config/opencode/agents/"
cp -R .opencode/skills/brownfield-* "$HOME/.config/opencode/skills/"

# In the target repository: ask the agent to perform an information-only discovery.
opencode
```

Select or invoke `brownfield-discovery` in OpenCode. Agent/skills are intentionally model-agnostic and do not enable Graphify or any MCP server by default. Existing global skill names may conflict; review before copying.

**Proposal status:** this is an initial contract and agent prompt, not a proven autonomous discovery implementation. It must be exercised on representative brownfield repositories before being promoted to stable.
