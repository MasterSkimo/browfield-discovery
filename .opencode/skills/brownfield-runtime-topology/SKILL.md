---
name: brownfield-runtime-topology
description: Create a source-backed Docker Compose foundation, app Dockerfiles and isolated E2E profiles/environment files without modifying existing developer configuration.
---

# Autonomous runtime topology discovery

The next agent will not act as a human developer with manually launched IDE processes. Default target: a **single reproducible Docker Compose project** that builds all real application backends/frontends/workers and runs databases, brokers and stubs for out-of-boundary systems.

Discovery **creates** the isolated Docker foundation, including `.e2e/compose.yaml`, source-build Dockerfiles where needed, E2E-specific app profiles/config and a safe `.env.e2e.example`. The E2E agent completes stubs, seeds, tests and runtime verification.

## Procedure

1. Inspect source manifests, CI build targets, existing Dockerfiles/Compose files, deployment manifests, runtime entrypoints and frontend build tools.
2. Enumerate all application-owned executables and build contexts. Derive likely Docker multi-stage build steps and launch commands, noting unsupported platforms instead of assuming the developer's host.
3. Detect database and messaging engine/version/topology, migrations, schema, broker topology, health and startup sequencing from config and code.
4. Identify all outside-application connections and infer URL overrides, auth scheme, request/response/error paths and candidate stub names. Keep real app modules real.
5. Trace configuration precedence, env variable names and app profiles; **create dedicated `.e2e/config/` profile files when needed**, wired to actual supported configuration loading. Do not reuse real credentials.
6. Create `.e2e/compose.yaml` with actual in-scope application source builds, DB/broker services, safe container DNS and health wiring; add Dockerfiles under `.e2e/docker/` only where needed. Provide controlled external stub wiring (or explicit blockers), plus planned fixture/reset and test-runner tasks.
7. Separate Compose profiles (optional services) from app profiles; keep required services default. Create `.e2e/.env.e2e.example` and `.e2e/.gitignore` excluding `.env.e2e.local`, with non-secret values. Do not overwrite developer configs or introduce real credentials.
8. Mark each claim OBSERVED/INFERRED/UNRESOLVED with paths/reasoning. For any missing fact, follow brownfield-inference before escalating.
9. Attempt non-mutating `docker compose -f .e2e/compose.yaml --env-file .e2e/.env.e2e.example config --quiet` if available; record actual result, never claim a build/start/test. Write .agent-context/environment-blueprint.md including created artifacts, source evidence, outstanding E2E tasks and validation status. Feed the core strategy and known commands into AGENTS.md.
10. Close phase D2 in discovery-progress.json only when the actual Compose file/env example, per-app source build wiring and required E2E config exist, and all app/infrastructure/external boundaries have a disposition. Block readiness for known Compose config errors.

## Quality gate

The output must **deliver the actual initial Compose stack**, not just answer questions. Has the discovery agent created the source-backed Docker foundation that the E2E agent can continue without starting an IDE? What real modules are built? Which DB/brokers and versions? Which external calls are stubbed? Which E2E profiles/env overrides are needed? What seed/reset and health checks? What remains a documented investigation?

Never claim a Docker build, startup, Compose config validation or E2E test ran when it did not. Preserve existing files and avoid destructive provisioning.
