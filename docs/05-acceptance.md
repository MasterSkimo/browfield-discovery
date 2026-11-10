# Acceptance criteria for the initial discovery proposal

## Contract/agent package

- [ ] OpenCode v2 loads the agent and on-demand skills from the documented paths.
- [ ] The agent can operate from a target project root and produce the seven listed outputs plus `AGENTS.md`.
- [ ] No application source, infrastructure file, or pre-existing agent instruction is overwritten.
- [ ] Source revision is recorded; findings are source-backed and labeled verified/inferred/unresolved.
- [ ] The output is scoped to module-level architecture and representative UI/API/async pathways with enough depth for test setup, without a class-by-class dump.
- [ ] Important unknowns are first investigated through implementation, configuration, tests, migrations and CI/deploy, with documented hypotheses and search trails.
- [ ] Root AGENTS.md directly gives module map, actual working directories and exact setup/build/run/test commands, source-based conventions, security, E2E and delivery rules; links alone do not pass.
- [ ] Discovery quality gate passes, or concrete failure is declared (never silently treated as complete).
- [ ] /brownfield-discover is installed for both OpenCode and Cursor, with a T3/OpenCode invocation documented.
- [ ] All detected databases and brokers have configuration locations recorded.
- [ ] All discovered outside-application boundaries have stubbing pointers or explicit unknowns.
- [ ] UI/API/async behavior inventories include identification of roles, data, and observable effects.
- [ ] Each unknown becomes a targeted investigation or developer question; no 'untestable' exemption.
- [ ] Next-agent instructions include Playwright/Newman requirements and the reliability/evidence contract.
- [ ] No credentials, token values, or sensitive test records appear in the generated artifacts.
- [ ] Re-running discovery after a code change updates impacted findings and flags stale evidence.

## Validation fixtures (future acceptance runs)

Evaluate on (a) one backend/API repo, (b) one UI + backend repo, (c) one multi-service repo with DB and messaging. Compare a fresh E2E-bootstrap agent operating with and without the discovery outputs. Record exploration repetition, ability to identify services/stubs/data, and ungrounded assertions.

This PR proposes these criteria; real brownfield acceptance runs are **not** claimed here.

## Full-stack discovery handoff and phased workflow

- [ ] D0–D6 phases have a recorded status and evidence; readiness is not claimed while phase gates are missing.
- [ ] A Compose-first environment blueprint specifies all real application builds, DB/brokers, outside-boundary stubs, service DNS, health, E2E test runners, data/reset and isolation.
- [ ] Distinguishes Compose service-selection profiles from application runtime profiles and documents separate E2E configurations / environment-variable overrides.
- [ ] Does not assume a developer's IDE and manually started applications are the E2E execution strategy.
- [ ] Discovery **creates Compose, E2E Dockerfiles and E2E-only application profiles/environment files** while preserving developer/prod configuration; full stubs/fixtures/tests belong downstream.
- [ ] Phase gates are reviewed after deeper discoveries; evidence and source revision are consistent.

## Concrete Docker artifacts

- [ ] The generated target includes `.e2e/compose.yaml` with **real** app services built from project sources and DB/broker services detected from code/config.
- [ ] Project-specific Dockerfiles under `.e2e/docker/` exist where existing build definitions are insufficient, and app startup wiring uses dedicated E2E config when appropriate.
- [ ] `.e2e/.env.e2e.example` includes safe non-secret keys/defaults; `.e2e/.gitignore` excludes `.env.e2e.local` and local credentials.
- [ ] External integration endpoints have explicit E2E-safe stubbing routes or a documented wiring blocker; no accidental real endpoint use is assumed.
- [ ] The agent attempted a non-mutating `docker compose config --quiet` when available and recorded status/command/reason; it does not claim unexecuted builds/tests pass.
- [ ] The quality gate checks actual Docker artifacts, not only `environment-blueprint.md`.
- [ ] E2E agent ownership remains: final stubs/fixtures/seed-reset, Playwright/Newman, health/start/runtime and test execution.

## Interactive developer clarification (D7)

- [ ] After D6, the agent reviews only investigated unknowns for developer-answerable gaps and begins an **interactive conversation** rather than ending with a list.
- [ ] Each question includes source evidence, a bounded hypothesis and why the answer affects Docker/E2E; only one question is posed per turn.
- [ ] The active question and status are persisted in `.agent-context/clarifications.md` and D7 = `awaiting_user` while the answer is pending.
- [ ] Answers are sanitized, source-checked and used to revise affected Docker/AGENTS/context outputs and verification; testimony is not silently promoted to verified behavior.
- [ ] "Don't know", skip and stop preserve unknowns and next actions rather than inventing resolutions.
- [ ] `/brownfield-clarify` resumes the interview on OpenCode/T3 and Cursor without restarting a full discovery or repeating answered questions.
- [ ] D7 is completed when no relevant questions exist or all are answered/deferred/declined; `ready_for_e2e_setup` cannot be claimed while the user reply is pending.
