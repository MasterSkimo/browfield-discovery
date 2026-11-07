# Mandatory verification contract for future agents

For each task, provide a machine-readable evidence record containing:

1. Task ID, request, source/implementation revision and test environment.
2. Each acceptance criterion (AC ID), its implementation paths, related test IDs and `pass`/`fail`/`not_run` outcome.
3. Each test ID, executable command, actual result, assertions and artifact locations.
4. Known baseline failures and any new regressions.
5. Overall status (`verified`, `not_verified`, `incomplete`) and remaining limitations.

The JSON format is specified by `schemas/task-evidence.schema.json` in the brownfield-discovery package; export a copy into your testing/QA area when needed.

- Never claim `pass` for a check that was not executed.
- Preserve Playwright traces/screenshots and Newman reports as execution evidence, not as substitutes for behavioral assertions.
- Characterization E2E captures existing behavior; changes to desired business behavior require an explicit request.
- Do not hide unsupported or pending coverage: list prerequisites and follow-up tasks.
- Redact secrets and personal data. Keep artifacts tied to the tested commit, fixtures and configuration.
