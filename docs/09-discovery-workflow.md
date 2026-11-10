# Proposed Brownfield Discovery workflow

Discovery remains **information-only**. It prepares agents to build a reproducible E2E environment; it does not provision that environment. A developer's manual workflow is evidence to investigate, **not the assumed runtime model**.

Run each phase in order and record progress in .agent-context/discovery-progress.json. Revisit earlier phases when later evidence invalidates their conclusions.

| Phase | Activities | Exit gate |
| --- | --- | --- |
| D0 — Reconnaissance | Record Git revision, existing instructions, modules, CI/build/deploy/tests | Current revision, source inventory and protected preexisting instructions |
| D1 — Application map | Identify executable application components, UI, API, workers, messaging, ownership | Every important application component has a mapped entry point and owner |
| D2 — Runtime topology | Infer app build/start, DB/broker, external stub, Compose services, dedicated app profiles, env-key precedence, readiness | Source-backed **full-stack Compose-first** blueprint completed, with explicit gaps |
| D3 — Behavior tracing | Trace representative UI -> API -> state/event and API-only + async flows | E2E candidates have entry, role, fixture assumptions, observable effects |
| D4 — Data and boundaries | Map DB migration/seed/reset, brokers, external contracts, test identity and failure behavior | Next agent knows what to build/reuse and what needs developer input |
| D5 — Autonomous inference | Revisit every unknown via config, code, tests, migrations, CI, Graphify leads, counterevidence | Only justified unknowns remain, each with a search trail and next action |
| D6 — Operational handoff | Generate AGENTS.md, supporting context, verification rules and validate it | Quality gate passes; source files unchanged; status accurately reported |

## Phase discipline

1. Read checkpoint and verify current commit before starting any phase.
2. Explore the phase using source-backed evidence. Corroborated static deductions are INFERRED, not automatically UNKNOWN.
3. Record evidence paths and conclusions in the progress record; mark done only with adequate evidence, otherwise blocked or in_progress.
4. Do not advance to later phases with an incomplete earlier gate.
5. Reopen earlier phases if a later discovery contradicts them.
6. Run final quality checks and report blockers; do not claim an executable Docker environment or passing E2E tests.

The quality gate checks structure and declared progress, not whether Docker, brokers or application code ran.

## Tooling

Graphify may accelerate navigation, Context7 may explain public framework behavior, and developer-authorized memories may suggest previous decisions. Current checked-out code/configuration remains the source of truth. Never automatically mine private conversations.

## Completion semantics

- ready_for_e2e_setup means D0–D6 are done with supported evidence; next agents can build the stack without repeating general discovery. No claim is made that Docker or E2E tests ran.
- needs_investigation means a critical gate is incomplete/blocked or a source mapping is missing.

## Review topics

- D2 currently produces a **blueprint**, not an actual compose.yaml. Do we want discovery to create a draft Compose file later?
- D3 currently inventories all discovered entry surfaces and deeply traces representative flows, rather than every class.
- D6 currently uses a structural validator and later real-project acceptance tests; independent agent review can be added.
