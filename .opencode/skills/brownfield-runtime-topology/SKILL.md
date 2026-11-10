---
name: brownfield-runtime-topology
description: Reconstruct an E2E-ready full-application Docker Compose topology from source evidence, without implementing or running containers.
---

# Autonomous runtime topology discovery

The next agent will not act as a human developer with manually launched IDE processes. Default target: a **single reproducible Docker Compose project** that builds all real application backends/frontends/workers and runs databases, brokers and stubs for out-of-boundary systems.

Discovery **does not** create Dockerfiles, Compose, application profiles or test env files; it supplies the information needed for that downstream implementation.

## Procedure

1. Inspect source manifests, CI build targets, existing Dockerfiles/Compose files, deployment manifests, runtime entrypoints and frontend build tools.
2. Enumerate all application-owned executables and build contexts. Derive likely Docker multi-stage build steps and launch commands, noting unsupported platforms instead of assuming the developer's host.
3. Detect database and messaging engine/version/topology, migrations, schema, broker topology, health and startup sequencing from config and code.
4. Identify all outside-application connections and infer URL overrides, auth scheme, request/response/error paths and candidate stub names. Keep real app modules real.
5. Trace configuration precedence, env variable names, existing application profiles and which **dedicated E2E profile/config files** the next agent should create if developer configs are unsuitable. Do not reuse real credentials.
6. Propose container service DNS, ports, network dependencies, healthchecks, deterministic seed/reset, logs/observability and optional Playwright/Newman test runners.
7. Separate Compose profiles (optional service selection) from application runtime profiles (application behavior). Do not profile mandatory core services by default.
8. Mark each claim OBSERVED/INFERRED/UNRESOLVED with paths/reasoning. For any missing fact, follow brownfield-inference before escalating.
9. Write .agent-context/environment-blueprint.md, with actual source evidence and downstream actionable tasks. Feed the core strategy and known commands into AGENTS.md.
10. Close phase D2 in discovery-progress.json only when every identified in-scope app and infrastructure/external boundary has a disposition.

## Quality gate

The output must answer: Can the E2E agent derive a runnable Compose stack without asking a developer how to start an IDE? What real modules are built? Which DB/brokers and versions? Which external calls are stubbed? Which E2E profiles/env overrides are needed? What seed/reset and health checks? What remains a documented investigation?

Never claim a build, Compose config or E2E test ran when it did not.
