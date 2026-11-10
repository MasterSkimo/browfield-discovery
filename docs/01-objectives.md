# Goals, responsibilities, exclusions

## Mission

An evidence-led reconnaissance pass prepares a brownfield codebase **and creates its dedicated E2E Docker foundation** for autonomous development agents. The first downstream task is creation of a complete, reproducible E2E characterization baseline.

Success means the next agent can determine what exists, where to look, what it needs to run, what must be stubbed, how to obtain test data, and how to prove its work, **without repeating a general repository survey**.

## Depth of discovery

1. Map the repository globally: modules, entry points, build manifests, runtime components, critical integrations, deployment hints.
2. Identify feature surfaces: UI routes, public/internal APIs, asynchronous consumers/producers, scheduled processes, role-specific entry points.
3. Investigate code paths **deeply enough** to reconstruct environment prerequisites and representative end-to-end flows (UI -> API -> state/event). This may require following several layers, but not every class.
4. Stop before line-by-line or class-by-class exhaustive analysis; downstream agents investigate task-specific details.
5. Derive plausible conclusions from independent code, configuration, tests, migrations and CI/deployment clues; reserve unresolved for absent/contradictory evidence after the full investigation protocol.
6. Produce direct, actionable AGENTS.md instructions as specified by https://agents.md/, including exact project commands, not just pointers.

## Discovery owns

- An agent instruction entrypoint and discoverable, compact references.
- Runtime/dependency inventory and boundary classification, a Compose-first environment blueprint, and **real dedicated `.e2e/` Compose/Dockerfiles/config scaffolding** for downstream agents.
- E2E inventory: journeys, endpoints, async triggers and observable effects, known roles/identities, relevant data, and follow-up tasks.
- Required engineering evidence format and completion rules.
- Transparent unknowns, conflicting evidence, and source revision/freshness.

## Discovery does not own

- Build fixes, refactors, application source or developer/production infrastructure changes. New **isolated E2E Docker infrastructure files** are in scope.
- Starting or mutating running DBs, brokers or application services; the E2E agent validates startup/runtime. Discovery may run a **non-mutating Compose configuration check**, but must record whether it actually ran.
- Implementing external service stubs or data seed scripts.
- Writing Playwright/Newman suites or promising E2E coverage.
- Inventing business requirements or producing exhaustive functional specifications.

## Non-negotiables

- No application source or developer/prod configuration modifications. Discovery may create/update owned `.e2e/` files and non-conflicting agent context.
- No secrets in generated files or captured evidence; report secret *names* only.
- No destructive or environment-mutating commands as part of discovery.
- Never state a tool or execution was successful if not observed.
- Never discard a behavior because it seems difficult to test. Record prerequisite work.
- Preserve existing target instructions; conflicts require a recorded recommendation, not silent replacement.

## Discovery process

Execute phases D0–D6 in [the proposed workflow](09-discovery-workflow.md), recording progress and source-backed phase gates. Complete an [environment blueprint](10-compose-first-handoff.md) before the E2E handoff. This process **requires** discovery to create a dedicated `.e2e/compose.yaml` and required Dockerfiles/E2E configuration (without modifying developer configuration). The E2E agent completes stubs, data, runnable integration and tests.
