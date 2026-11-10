# AGENTS.md — {{PROJECT_NAME}}

<!-- Brownfield agent: replace every {{...}} placeholder with inspected, project-specific facts. Remove this comment after generation. -->

## Project overview
Explain what each application does, which code is in scope, the main runtime and the repository revision inspected. Include evidence references here or in the linked context package.

## Repository map
Give actual module paths, their responsibilities and entry points. Include the module/application ownership boundary and which modules collaborate. Make the map actionable, not a generic list of file types.

## Setup commands
Provide exact **working directories**, prerequisite runtime/tool versions and commands **from the repository** to install or prepare dependencies. Label each command "declared, not executed" or "observed" accurately. If none exists, state the targeted sources inspected and the setup investigation to do next.

## Build and run
Provide per-application commands, environment profiles, ports, launch ordering and health checks. Show exact invocations in fenced shell blocks when known. Identify DB/broker and external-stub prerequisites without implementing them. State known limitations honestly.

## Tests and quality checks
Provide exact commands for unit, integration and any existing E2E tests, the directory in which each runs and locations of relevant test configurations. Show lint/typecheck/CI gates from actual source files. Indicate declared versus executed status.

## Architecture and code conventions
Specify naming conventions, organization, DI/security/transaction patterns, error handling, message conventions and canonical local examples actually seen. Do not prescribe imaginary patterns. Place genuinely module-specific rules in nested AGENTS.md files only where different from the root.

## Security and data handling
List where credentials are referenced (only **names**, not values), how local profiles/identities are selected and safe fixture/test-data requirements. Never paste secrets or personal data.

## First autonomous mission: E2E characterization
Describe the scope of the existing application's **real** UI/backend modules; Docker DB/brokers; external services to stub; identity/fixture needs; Playwright for UI, Newman for API-only, and assertions on async outcomes. The baseline must capture observed current behavior without conflating it with intended requirements. Link to the inventory for scenario details.

## Evidence and delivery
For each downstream request, connect acceptance criterion -> implementation path -> automated check/assertions -> command + environment + artifact -> result (pass/fail/not_run). Separate pre-existing failures and regressions. Do not report unexecuted tests as passing. Follow the verification contract.

## Detailed reference material
Link only to source-backed context files (architecture, execution, dependencies, E2E inventory, unknowns, verification contract). The core work instructions above must stand on their own.
