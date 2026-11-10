# E2E baseline: downstream handoff requirements

The *discovery* agent reconstructs actionable, source-backed information; the *next* agent creates the environment and E2E tests. The test boundary is the application under test, not a collection of mocked application components.

## Target environment

| Component | Downstream treatment | Discovery information to locate |
| --- | --- | --- |
| Application frontends and backends | Build/run real components through a single Compose project where feasible | build contexts, Dockerfile needs, runtime profiles, ports, config, healthchecks |
| Databases | Docker Compose services | engines/versions, schemas, migrations, schemas/collections, initial data |
| Messaging | Docker Compose services | brokers, topology, queues/topics, producers/consumers, failure/retry handling |
| Outside-application services | Stub at the boundary | endpoints, protocols, auth, contracts, typical success/error responses |
| Identity provider | Real or simulated identity boundary suitable for the test | auth flows, roles, tokens, local fixtures and callback configuration |
| Data | Deterministic fixtures/seed/reset | migration/seed assets, invariants, records and dependencies |
| Browser-accessible journeys | Playwright | routes, roles, actions, expected visible outcomes |
| API-only journeys | Newman/Postman | endpoints, methods, auth, sequences, assertions, side effects |
| Async/other background flows | Observable E2E scenarios | triggers, queues, eventual effects and verification points |

## Coverage definition

Coverage is assessed against an **inventory of discovered behaviors**, not class count or endpoints alone. List at least: entry point, identity/role, starting conditions, input, expected observation, source references, and scenario status. UI and API coverage may overlap; avoid double-counting the same business behavior while retaining both interfaces where materially different.

Each inventory item must eventually be marked as tested with executable evidence or tracked as an unimplemented E2E scenario with prerequisite work. **No behavior is labeled 'untestable'**. Missing data, access, external contracts, or deterministic controls become actionable follow-ups.

## Characterization vs specification

The baseline captures **current observable behavior**, including existing defects and inconsistent responses. A test verifying current behavior is not automatically evidence of intended business correctness. Preserve that distinction in test names and evidence.

## Developer input

Developers may help clarify business semantics, data invariants, and fixture design if existing scripts do not suffice. Record which questions require their help; do not block the entire discovery waiting for perfect answers.

## Handoff boundaries

The discovery agent must not create a Docker Compose environment, write seed scripts, deploy stubs, or generate test suites. It prepares the dependency map, E2E inventory, and required verification contract for the agents that will.

## Deeper investigation expectation

The discovery agent must trace representative frontend routes through API calls, server behavior and state/event observations, and APIs through auth, data and external contracts. It should infer environment requirements from source, tests, config, CI and migrations even where no Docker or E2E configuration exists. Reserve 'unknown' for evidence gaps after investigation, and preserve the reasoning chain in the manifest and unknowns ledger.

## Autonomous runtime strategy

The future E2E agent should not follow a human developer setup by default (IDE, individually launched apps, manually provisioned DB or broker). Prefer a single Docker Compose project that builds all in-scope app images from the source checkout and runs supporting DB/broker/stub services; optional profiles select test runners or debug tools. Application-specific E2E profiles/files may be created separately from developer configuration and wired with Compose environment variables and env_file as necessary. The discovery agent identifies exact candidates, sources and constraints in `.agent-context/environment-blueprint.md` but does not implement them. See [the runtime contract](10-compose-first-handoff.md).
