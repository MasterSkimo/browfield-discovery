# Graphify as an optional discovery accelerator

Graphify is a candidate structural graph source, not the author of the project context or the sole proof of any finding.

Use it, **if it is installed and accessible**, to locate modules, call/import relationships, central nodes, likely change propagation, and starting points for tracing UI/API/async flows.

Guardrails:

- The agent works without Graphify, using manifests, repository search, and code evidence.
- Do not assume any CLI/MCP integration is installed; discover available tools first.
- Keep the code revision or indexing timestamp associated with graph-derived findings.
- Verify graph hints against files, framework wiring/configuration, and runtime contracts when relevant.
- Dynamic DI, reflection, event-driven paths and integrations may be missing or inferred; never promote these graph hints to proven behavior without evidence.
- Do not commit Graphify indexes, generated graphs, or credentials into the target repository unless explicitly requested.

No Graphify installation or MCP dependency is introduced by this PR.
