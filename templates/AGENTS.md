# AGENTS.md — {{PROJECT_NAME}}

<!-- Brownfield agent: replace every {{...}} placeholder with inspected, project-specific facts. Remove this comment after generation. -->

## Project overview
Explain what each application does, which code is in scope, the main runtime and the repository revision inspected. Include evidence references here or in the linked context package.

## Repository map
Give actual module paths, their responsibilities and entry points. Include the module/application ownership boundary and which modules collaborate. Make the map actionable, not a generic list of file types.

## Setup commands
Provide exact **working directories**, prerequisite runtime/tool versions and commands **from the repository** to install or prepare dependencies. Label each command "declared, not executed" or "observed" accurately. If none exists, state the targeted sources inspected and the setup investigation to do next.

## Build and run
Provide per-application commands, environment profiles, ports, launch ordering and health checks. Show exact invocations in fenced shell blocks when known. Identify DB/broker and external-stub prerequisites, and include the **generated `.e2e/compose.yaml` command and E2E env file** where present; distinguish scaffold/config-validation status from runtime proof. State known limitations honestly.

## Tests and quality checks
Provide exact commands for unit, integration and any existing E2E tests, the directory in which each runs and locations of relevant test configurations. Show lint/typecheck/CI gates from actual source files. Indicate declared versus executed status.

## Architecture and code conventions
Specify naming conventions, organization, DI/security/transaction patterns, error handling, message conventions and canonical local examples actually seen. Do not prescribe imaginary patterns. Place genuinely module-specific rules in nested AGENTS.md files only where different from the root.

## Security and data handling
List where credentials are referenced (only **names**, not values), how local profiles/identities are selected and safe fixture/test-data requirements. Never paste secrets or personal data.

## First autonomous mission: E2E characterization
Do **not** assume the future agent will start services as a human developer through an IDE. Prefer a single reproducible **Docker Compose** project that builds and runs all real application backends, frontends, workers and consumers, alongside Docker DB/brokers and stubs for every external boundary. Detail existing build definitions and profiles; explicitly permit separate E2E application configuration files and environment-variable overrides instead of modifying developer profiles. Use Compose profiles for optional tooling, not as a substitute for application runtime profiles. Provide known service DNS, ports, health, seeds/reset, identity and fixtures. Describe Playwright UI, Newman API-only, and async assertions. Link to the source-backed environment blueprint and behavior inventory. Discovery **must actually create `.e2e/compose.yaml`**, Dockerfiles/E2E configs as needed, a safe env example and ignore rules. Explain their paths, source-based configuration and what the E2E agent must finish. A scaffold or passing Compose config check does not prove containers or tests run.

## Evidence and delivery
For each downstream request, connect acceptance criterion -> implementation path -> automated check/assertions -> command + environment + artifact -> result (pass/fail/not_run). Separate pre-existing failures and regressions. Do not report unexecuted tests as passing. Follow the verification contract.

## Detailed reference material
Link only to source-backed context files (architecture, execution, dependencies, environment blueprint, discovery progress, E2E inventory, unknowns, verification contract). The core work instructions above must stand on their own.
