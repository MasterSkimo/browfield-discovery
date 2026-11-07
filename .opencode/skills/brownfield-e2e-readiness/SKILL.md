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

## Rules

Do not generate Playwright/Newman tests, create containers, or seed data. Do not mark discovered behavior `untestable`. The next agent owns E2E implementation and assertions.
