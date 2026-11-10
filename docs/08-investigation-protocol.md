# Evidence-led brownfield investigation protocol

The goal is autonomous **inference**, not a list of unknowns. The discovery agent is expected to reconstruct what future developers need to run and test the current application without analyzing each class.

## Required investigation passes

1. **Inventory:** inspect repository manifests, module roots, CI, Docker/Compose, Helm/Kubernetes, IaC, runbooks and existing agent instructions. Record all executable application components.
2. **Runtime wiring:** correlate ports, profiles, environment-key references, config precedence, build targets, service discovery, database clients, broker declarations, auth filters and scheduled jobs.
3. **User surfaces:** inspect frontend route and state declarations, backend route/controller/middleware annotations, API schemas, message consumers and scheduled triggers. Trace representative routes through application logic to persisted, emitted or visible outcomes.
4. **Dependency boundaries:** distinguish application-owned services from infrastructure (containerized DB/broker) and outside services (stubs). Resolve client URLs, auth, request/response shapes, retry/timeout paths from clients, configuration, tests and fixtures.
5. **Data/identity:** inspect schemas, migrations, entity mappings, fixture factories, tests, sample requests, auth/role config and seed scripts. Infer dataset prerequisites and what the next agent must implement.
6. **Conventions and procedures:** read *actual examples* and CI/test/build definitions to derive package-specific commands, project conventions, quality gates and anti-patterns.
7. **Adversarial review:** revisit every inconclusive statement; search for conflicting files, alternative runtime profiles and evidence that could falsify each hypothesis. Produce an actionable handoff.

Use Graphify if already available to find candidate connections, but inspect source and configuration before treating edges as facts. Memory/old chats are leads only, with developer approval. Context7 helps interpret public library documentation, not private app behavior.

## Evidence ladder before declaring an unknown

For every open question:

1. Search the closest configuration/code implementation.
2. Search *independent* evidence: tests and fixtures, CI/deploy files, schema/migrations, documentation, Git history (only if available), generated OpenAPI/clients.
3. Trace the producer **and** the consumer for API/message flows; look for defaults, fallbacks, profiles and environment-variable wiring.
4. Develop a concrete hypothesis and compare it with the observed code and counterevidence.
5. If corroborated, report the **most useful bounded inference**, with confidence and assumptions. Runtime verification is not necessary for a static inference to be useful.
6. Mark **unresolved** only if evidence conflicts, is absent after targeted searches, or requires unavailable credentials, real data, business authority or runtime behavior. Report exactly what you searched, why deduction failed, and the next specific action.

A single missing README or env.example entry never justifies an unknown when the code, tests or CI expose the answer. Do not ask developers questions answerable by a local repository inspection. Conversely, do not invent protocol payloads or business meaning.

## Findings format

For an important finding, include:
- statement and classification: OBSERVED (direct source evidence), INFERRED (evidence-based reasoning), or UNRESOLVED;
- source paths and specific locators;
- for INFERRED: reasoning chain and assumptions, including why the conclusion is likely;
- for UNRESOLVED: searched locations, strongest hypothesis, missing/contradictory evidence and precise investigation or developer input needed.

Examples of acceptable inference:
- An application has JDBC PostgreSQL configuration, a Flyway migrations directory and JDBC repositories. Infer **PostgreSQL is a local Docker prerequisite**, even if no docker-compose file exists.
- A service declares RabbitMQ exchange bindings and listeners in configuration and publisher code. Infer the **broker and topology needed for E2E** from those sources; do not mark the system unknown because no broker is running.
- A frontend route invokes an HTTP client for /orders while the backend defines POST /orders and persists an entity. Infer an **order-creation E2E candidate**; explicitly flag any unverified identity or external effects.

Bad outputs:
- "DB unknown, ask a developer" without inspecting data source configuration or migrations.
- "API requests need mocking" without identifying the external boundary, request contract and client.
- "Run the tests" without exact directory, command or test location.
- "See architecture.md" as the entire content of AGENTS.md.

## Stop condition and quality gate

Do not stop at the first apparently complete manifest. Verify all important modules have a disposition, all discovered infrastructure and external connections have a classification, and each primary UI/API/async surface has at least one testable observation or a targeted continuation. Run the **non-mutating** quality check from this package if available:

~~~sh
python3 /path/to/browfield-discovery/scripts/validate_discovery.py --project /path/to/target
~~~

A failed quality gate requires repair of the discovery output, not a "discovery complete" claim. The gate checks structure and provenance, not runtime correctness; report any still-unknown limits honestly.

## Runtime independence from developers

Investigate whether all application components can be built and run from source inside a single Compose project, including frontends/backends, workers and scheduled consumers. Do not assume IDE launch configs are the preferred downstream approach. Identify app-specific E2E profiles/files and environment variable wiring without editing the project during discovery. Record Docker build context, service dependencies/healthchecks, container DNS, DB/broker topology, stub endpoints and seed/reset plan in the environment blueprint. If an existing production/development profile cannot be reused safely, describe a separate E2E config for downstream agents.
