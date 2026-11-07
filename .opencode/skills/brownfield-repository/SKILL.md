---
name: brownfield-repository
description: Discover a brownfield repository's main modules, execution entry points, architecture, commands and existing agent guidance without exhaustive class analysis.
---

## Procedure

1. Inspect Git root/revision and existing `AGENTS.md`, `.opencode`, `.agents`, `.claude`, manifests and README files.
2. Detect module roots, languages, frameworks, build tools, package managers, frontends, backends and executables.
3. Identify candidate start/build/check commands **from sources**; never claim a command succeeds unless it was actually observed.
4. Locate architectural seams: inbound HTTP/UI entry points, outbound adapters, background jobs, persistence and messaging.
5. Record global structure first; trace deeper only when needed for E2E setup or handoff.
6. Optionally use Graphify to locate candidate relationships. If the developer authorizes a historical search, query MemPalace for only relevant past decisions, verifying each claim against the current checkout. Keep durable troubleshooting insights in Basic Memory only with explicit permission; do not store secrets or unrelated conversations.
7. Emit source-backed notes for `.agent-context/architecture.md` and `execution.md`.

## Done when

Another agent can identify the relevant modules, configuration files and likely execution entry points without scanning the repository from scratch. Do not copy full README files, dependency lists, or code into the context package.
