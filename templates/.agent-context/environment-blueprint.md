# Full-stack E2E environment blueprint — PROJECT_NAME

The discovery agent **creates the dedicated E2E Docker foundation**. The downstream agent completes stub behavior, fixtures, E2E tests and runtime validation.

## Scope and evidence
- Git revision: REVISION
- Application components to run as real code: APP_MODULES_WITH_PATHS
- Outside-application dependencies to stub: EXTERNAL_BOUNDARIES_WITH_PATHS

## Proposed Compose topology

| Component | Category | Source/build context or image/version hint | Port/service DNS | Startup/health dependency | Source/confidence |
| --- | --- | --- | --- | --- | --- |
| SERVICE_NAME | application / database / broker / stub / test-runner | REPOSITORY_REFERENCE | PORT_AND_DNS | HEALTH_AND_DEPENDENCIES | SOURCE_AND_REASONING |

Include every real application backend/frontend/worker and its infrastructure. Do not assume developers will manually start the applications.

## Docker builds and application profiles

| App | Existing build/launch definition | Docker build approach | Separate E2E runtime profile/config | Source/confidence |
| --- | --- | --- | --- | --- |
| APP_NAME | BUILD_SOURCE | COMPOSE_BUILD_OR_DOCKERFILE_PLAN | E2E_CONFIG_PLAN | SOURCE_AND_REASONING |

- Explain any reason a component cannot currently be built inside Docker, with a specific next action.
- Compose profiles select optional services. App profiles configure the application; never conflate them.
- Do not modify developer configs. **Discovery owns** separate `.e2e/config` files and `.e2e/docker` Dockerfiles where needed; name created paths and their source evidence.

## Variables and environment isolation

| Service | Environment variable or profile key | Current source/default | Proposed E2E override | Source/confidence |
| --- | --- | --- | --- | --- |
| SERVICE | VARIABLE_NAME | SOURCE_KEY | COMPOSE_OVERRIDE_OR_ENV_FILE | SOURCE_AND_REASONING |

- Specify container DNS for DB, broker and stubs rather than localhost.
- Distinguish Compose --env-file interpolation, env_file container variables and environment service overrides.
- Create safe `.e2e/.env.e2e.example` and `.e2e/.gitignore` entries excluding local values; never write `.env.e2e.local` credentials. Never store secret values.

## Data and messaging
- Database engine/version/migration hints: EVIDENCE_AND_ACTIONS
- Existing seeds and deterministic reset needs: EVIDENCE_AND_ACTIONS
- Broker topology, retry and DLQ expectations: EVIDENCE_AND_ACTIONS

## External boundaries and identities
- Each stubbed endpoint, protocol, client source, URL override, auth and error behavior: EVIDENCE_AND_ACTIONS
- Test users, permissions, identity provider boundary and callbacks: EVIDENCE_AND_ACTIONS

## E2E invocation and observability
- Playwright UI entry points, roles and fixtures: EVIDENCE_AND_ACTIONS
- Newman endpoint groups, auth and assertions: EVIDENCE_AND_ACTIONS
- Async observations, logs, report paths, teardown: EVIDENCE_AND_ACTIONS

## Planned downstream verification
1. Reuse and complete the **already generated Compose, dedicated app profiles/Dockerfiles and safe example config**, without changing developer defaults.
2. Complete missing stubs/fixtures, then build and start DB/broker/stubs and actual applications with readiness checks.
3. Load/reset deterministic state, block unintended real external calls, run UI/API/async characterization.
4. Save command, commit, environment, assertions, traces/reports and failure evidence.
5. Tear down without affecting developer environments.

## Assumptions and next actions
SOURCE_BACKED_ASSUMPTIONS_BLOCKERS_AND_PRIORITIZED_TASKS

## Created E2E Docker artifacts and static validation

- Compose: .e2e/compose.yaml — created / preserved conflict / incomplete (record exact result)
- Env example: .e2e/.env.e2e.example — keys only, no real values
- Local-value ignore: .e2e/.gitignore — includes .env.e2e.local
- Dockerfiles and app profiles: list **actual paths** and source references
- Compose config validation: PASS / FAIL / NOT_RUN, exact command and captured reason (do not invent results)
- Components/routing still to implement in E2E phase: actual next actions
