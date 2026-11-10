---
name: brownfield-e2e-readiness
description: Prepare an inventory of UI, API and asynchronous behaviors, identity, fixtures and observable effects for Playwright/Newman characterization.
---

## Procedure

1. Inventory user-facing UI routes and key actions, API endpoint groups and API-only journeys, and message/async triggers.
2. Identify identity flows, roles/permissions, primary data entities, migrations, seed/reset assets and test configuration.
3. For each discovered behavior record: ID, entry, actor/role, preconditions, input, expected **observable current** effect, source references and downstream E2E scenario work.
4. Prefer main flows and risk-significant branches; avoid a per-class dump. Capture gaps without claiming completeness prematurely.
5. Separate observed behavior from implied/intended business requirements.
6. Categorize follow-up needs as `environment`, `stub`, `data`, `identity`, `test`, or `investigation`.
7. Write `.agent-context/e2e-inventory.md`, and connect missing facts to `unknowns.md`.

## Deep exploration requirements

Do not stop after listing routes: follow representative browser action -> API -> DB/message/external effect; API-only endpoint -> auth/data/response and async trigger -> consumer -> observed effect. Group by business journey without class-by-class enumeration. Infer fixtures and user roles from schemas, test builders, migrations and security config, marking assumptions. An undocumented scenario is not an untestable scenario.

## Rules

Do not generate Playwright/Newman tests, create containers, or seed data. Do not mark discovered behavior `untestable`. The next agent owns E2E implementation and assertions.

## Runtime assumptions to reject

Do not assume manual app boot via IDE, local Postgres/RabbitMQ or a developer's existing `.env`. The next agent should aim for one Compose project building actual apps, with separate E2E profiles/env overrides, deterministic data/reset and all out-of-boundary integrations stubbed. Reference the environment blueprint for each test candidate.

## Docker foundation created by discovery

Reference **actual** `.e2e/compose.yaml` service names and the created E2E profile/env files in each test candidate. The E2E agent will finish fixtures/stubs/tests and execute Compose; discovery must create the initial Docker resources, not merely describe them.
