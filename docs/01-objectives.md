# Goals, responsibilities, exclusions

## Mission

An information-only reconnaissance pass prepares a brownfield codebase for autonomous development agents. The first downstream task is creation of a complete, reproducible E2E characterization baseline.

Success means the next agent can determine what exists, where to look, what it needs to run, what must be stubbed, how to obtain test data, and how to prove its work, **without repeating a general repository survey**.

## Depth of discovery

1. Map the repository globally: modules, entry points, build manifests, runtime components, critical integrations, deployment hints.
2. Identify feature surfaces: UI routes, public/internal APIs, asynchronous consumers/producers, scheduled processes, role-specific entry points.
3. Investigate **only** code paths needed to identify environment dependencies, test boundaries, data, and probable end-to-end flows.
4. Stop before line-by-line or class-by-class exhaustive analysis; downstream agents investigate task-specific details.
5. Prefer existing documentation, manifests, and code references; distinguish observed, inferred, and unresolved conclusions.

## Discovery owns

- An agent instruction entrypoint and discoverable, compact references.
- Runtime/dependency inventory and boundary classification.
- E2E inventory: journeys, endpoints, async triggers and observable effects, known roles/identities, relevant data, and follow-up tasks.
- Required engineering evidence format and completion rules.
- Transparent unknowns, conflicting evidence, and source revision/freshness.

## Discovery does not own

- Build fixes, refactors, application code or infra changes.
- Running or provisioning the entire stack, Docker, brokers or databases.
- Implementing external service stubs or data seed scripts.
- Writing Playwright/Newman suites or promising E2E coverage.
- Inventing business requirements or producing exhaustive functional specifications.

## Non-negotiables

- No application source modifications.
- No secrets in generated files or captured evidence; report secret *names* only.
- No destructive or environment-mutating commands as part of discovery.
- Never state a tool or execution was successful if not observed.
- Never discard a behavior because it seems difficult to test. Record prerequisite work.
- Preserve existing target instructions; conflicts require a recorded recommendation, not silent replacement.
