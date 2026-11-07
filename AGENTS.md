# Instructions for contributors to browfield-discovery

This is the **agent-package repository**, not a target application's generated `AGENTS.md`.

- Protect the functional boundary: discovery provides information; downstream agents build environments, fixtures, stubs, and tests.
- Do not implement application-specific integrations here.
- Keep the target-project `AGENTS.md` concise; store source-backed details outside it.
- Never invent repository facts, execution results, secrets, or coverage.
- Every factual discovery output must reference source files, configs, manifests, or commands actually inspected.
- Treat unknowns as follow-up work, never silently exempt behavior from E2E coverage.
- Preserve pre-existing agent instructions and avoid overwriting project files.
- Update the output contract, templates, and tests together when a field changes.
