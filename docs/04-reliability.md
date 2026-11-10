# Reliability and proof contract for downstream work

The agent package must instruct later agents to demonstrate alignment between **request -> acceptance criteria -> implementation -> automated checks -> observed results**.

For every future task:

1. Record the request and explicit acceptance criteria (AC IDs).
2. Link each AC to code/configuration changes or to a justified no-change outcome.
3. Link every AC to executable verification, including meaningful assertions and data setup.
4. Record the command, environment, input/fixture revision, execution time, result and artifacts.
5. Report baseline failures separately from regressions; an unknown or unexecuted check is not a passing check.
6. Assign one result per AC: `pass`, `fail`, or `not_run`, with rationale for non-passing cases.
7. Name remaining risks and caveats. Completion cannot be claimed solely from a code diff.

Schema: [task-evidence.schema.json](../schemas/task-evidence.schema.json). A concrete illustrative evidence record lives in [task-evidence.example.json](../examples/task-evidence.example.json).

## Evidence examples

- Playwright trace, JUnit/HTML report, screenshots **with asserting test steps**, relevant logs, and result summary.
- Newman JSON/JUnit report, sanitized request/response evidence, status assertions and side-effect checks.
- For messaging: produced event/correlation ID and observed downstream state or queue effect.
- For infrastructure: running health checks and deterministic reset validation, not just a created Compose file.

Artifacts must be reproducible, scoped, appropriately redacted, and tied to a particular commit and environment. A screenshot alone or a passing HTTP status without behavioral assertions is insufficient.

The discovery itself must also cite provenance for its key findings, but it does not fabricate test execution evidence.
