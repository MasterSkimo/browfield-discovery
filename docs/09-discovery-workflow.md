# Brownfield discovery workflow — proposed v0.2

Discovery produces a usable Docker foundation, not just plans. The downstream E2E agent adds complete stub behavior, data, automated scenarios and runtime validation. Never assume human IDE/manual startup is the right execution model.

| Phase | Discovery work | Exit condition |
| --- | --- | --- |
| D0 — Reconnaissance | Inspect Git revision, existing instructions and manifests, CI/build/deploy | Source inventory and revision recorded |
| D1 — Application map | Identify real app modules, entry points, UI/API/async paths and owners | All executable components and boundaries mapped |
| D2 — Docker foundation | Create .e2e/compose.yaml, required Dockerfiles and isolated E2E profiles/env example | Real app services, DB/brokers and external stubbing routes represented; scaffold exists and gaps recorded |
| D3 — Behavior tracing | Explore representative UI -> API -> state/message, API-only and async paths | Candidate E2E cases with inputs, roles and assertions |
| D4 — Data and integrations | Map fixtures/migrations/reset, auth and external contracts | Concrete work items for the E2E agent |
| D5 — Independent inference | Revisit all unknowns and update Docker files using corroborated source evidence | Only justified unknowns remain and D2 stays consistent |
| D6 — Handoff and quality gate | Generate operational AGENTS.md, sources, progress and checks | Docker scaffold and metadata validated; existing app/dev config unchanged |

Maintain .agent-context/discovery-progress.json with evidence and blockers for every phase. Proceed sequentially, reopening a previous phase if findings invalidate it. A phase cannot be done merely because a Markdown file exists.

## D2 rules

- Discovery is permitted to create and edit **dedicated .e2e/** Compose, Dockerfiles and application E2E config, a nonsecret env example, plus additive .gitignore rules. It must **not modify application source, normal developer/prod configs, existing developer Compose/Dockerfiles, or migrations**.
- Each in-scope frontend, backend, worker, consumer or scheduler requiring its own process is represented as a **real** service with a source build context. Do not replace application code with stubs.
- Include detected DB and broker services, container DNS, environment mappings and health/readiness dependencies. Select source-grounded image versions.
- Route every external call to a test-controlled boundary or explicitly record a blocking wiring gap. Full stub behavior is downstream.
- Create separate E2E application profiles/configuration if needed and wire them into Compose through supported environment variables, env_file or mounted config. Do not assume developer settings can safely be reused.
- Distinguish Compose service-selection profiles from app runtime profiles. Keep required services in the default Compose set.
- Create .e2e/.env.e2e.example with safe defaults/names; ignore .e2e/.env.e2e.local and never write real credentials.
- If Docker Compose is available, run its **non-mutating config validation** and record pass/fail, command and evidence. Do not execute up, down -v, migrations or tests in discovery.
- Unimplemented stubs, fixture loading and E2E tests remain explicit follow-up tasks. Do not fabricate readiness or a passing build.

## Readiness

ready_for_e2e_setup requires D0–D6 done with evidence and a concrete Docker foundation that passes the structural gate. If a Compose config check was possible and failed, the failure blocks readiness. If Docker was unavailable, record not_run and the reason; the E2E agent must perform runtime checks later.

needs_investigation means a required component, scaffold or handoff rule could not be established without further investigation.

## Review decisions

The present boundary is: discovery creates Docker scaffolding and isolated E2E configurations; the E2E agent completes stubs, fixtures, Playwright/Newman and runtime verification. Build/start/health validation can be expanded later.
