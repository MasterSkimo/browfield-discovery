# Optional tooling setup (Cursor and OpenCode)

One entrypoint runs on Linux, macOS and Windows using Python 3.10+ (stdlib only): scripts/setup.py.

## Usage

- Status only: python3 scripts/setup.py --check (Windows: py -3 scripts\setup.py --check)
- Interactive: python3 scripts/setup.py
- Explicit workstation installation: python3 scripts/setup.py --tools basic-memory,mempalace,graphify,context7 --clients cursor,opencode --yes
- Project-scoped clients (no tools): python3 scripts/setup.py --scope project --target /path/to/repo --tools '' --clients cursor,opencode --yes
- Preview only: append --dry-run
- Optional local MCP registration: append --connect-mcp and specify clients and tools

No tools or clients are selected by default. Interactive selection is individual, with a final confirmation defaulting to no. Noninteractive changes require --yes and explicit selections. Existing tools are never upgraded or reinstalled.

## Official tools

| Tool | PATH detection | Package with uv/pipx | Purpose |
| --- | --- | --- | --- |
| Basic Memory | basic-memory | basic-memory | Long-lived knowledge not suitable for AGENTS.md |
| MemPalace | mempalace | mempalace | Developer's past conversations, only with explicit consent |
| Graphify | graphify | graphifyy | Source graph to guide discovery |
| Context7 | Existing `context7` MCP server entry | No local package (hosted MCP) | Current library and framework documentation |

Context7 is configured through its remote MCP endpoint `https://mcp.context7.com/mcp` in the selected clients, with no npm or Node.js requirement. Selecting Context7 explicitly authorizes adding that endpoint to selected client configurations; the clients handle OAuth when needed. Existing `context7` entries are never replaced. For the vendor CLI + Skills mode, use `npx ctx7 setup` separately (Node.js 22.13+).

The installer requires uv or pipx already installed to add missing **local Python packages**. It does not download package managers. For Basic Memory, uv uses --prerelease=allow in accordance with its current package requirements.

The script does not initialize repositories, run database migrations, record or mine discussions, scan the current repository with Graphify, or install Graphify hooks/skills. Restart your shell/client when PATH or agent discovery needs refresh.

## Cursor and OpenCode

Cursor receives its custom subagent in .cursor/agents and slash command in .cursor/commands; OpenCode v2 receives its agent in .opencode/agents and slash command in .opencode/commands. Both reuse the *same* SKILL.md files in .agents/skills; the discovery templates, schema, investigation protocol and non-mutating quality checker are copied to .agents/brownfield-discovery.

Scope global installs under the appropriate home directory. Scope project requires an explicit --target and writes only to that repository's agent/skill directories. It never replaces existing files: identical copies are ignored and customized copies become reported conflicts. The target's AGENTS.md is not created or changed during installation.

Cursor user-level skills in ~/.agents/skills are available to local sessions. For Cursor Cloud Agents and remote workers, install project-scoped skills into the repository (or follow Cursor's explicit skill sync mechanism).

## Running full discovery

Run /brownfield-discover in the target repository from the Cursor or OpenCode agent interface. In T3 Code, choose the OpenCode provider and put /brownfield-discover at the very start of the message. Reload provider configuration / restart the agent session after first installation if needed. OpenCode also supports a direct noninteractive invocation with opencode run --agent brownfield-discovery followed by the full-discovery prompt.

The discovery quality gate is .agents/brownfield-discovery/scripts/validate_discovery.py --project . (invoke with Python 3.10+). A gate failure is an incomplete discovery, not a successful handoff.

## MCP integration

--connect-mcp explicitly opts in to adding missing server definitions. Supported local entrypoints: basic-memory mcp and mempalace-mcp if present on PATH. Context7 uses a remote MCP connection and is explicitly registered when selected, even without --connect-mcp. The script adds missing entries to Cursor's mcpServers JSON and OpenCode v2's mcp.servers JSON; existing server definitions are preserved. JSONC is not rewritten; merge manually if one exists. Graphify stays CLI-only in this bootstrap because using its MCP needs project graph context and separate registration.

For a MemPalace installation without mempalace-mcp, run mempalace mcp for version-specific instructions. Neither memory tool mines or syncs history as part of setup.

Context7 queries a hosted documentation service; do not send private source code, customer data, secrets, or internal architecture to its search tools. Consult it for public library documentation and validate details against the application's pinned dependency versions.

## Privacy and trust

Historic MemPalace conversations may contain unrelated personal or client information. The discovery agent must obtain explicit developer permission before searching historical conversations; restrict searches to the project and validate conclusions against the current checkout. Do not export raw transcripts into AGENTS.md or shared files.

Basic Memory is intended for durable decisions and troubleshooting insights that do not belong in generated instructions. It must not become a secret store. Code/configuration at the analyzed Git revision remains the source of truth for project behavior, not memory or inferred graph edges.

## Official references

- https://docs.basicmemory.com/local/local-install
- https://github.com/basicmachines-co/basic-memory
- https://github.com/MemPalace/mempalace
- https://mempalaceofficial.com/guide/mcp-integration
- https://github.com/Graphify-Labs/graphify
- https://github.com/upstash/context7
- https://context7.com/docs/resources/all-clients
- https://cursor.com/docs/subagents
- https://cursor.com/docs/skills
- https://opencode.ai/docs/agents
- https://opencode.ai/docs/skills
- https://opencode.ai/docs/mcp-servers
