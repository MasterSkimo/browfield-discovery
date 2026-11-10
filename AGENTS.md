# Instructions for contributors to browfield-discovery

This is the **agent-package repository**, not a target application's generated `AGENTS.md`.

- Protect the functional boundary: discovery provides source-backed information **and a dedicated Docker Compose foundation**; downstream agents finish stubs, fixtures, tests and runtime validation.
- Do not implement application-specific integrations here.
- Keep target-project `AGENTS.md` operational and source-backed: setup/build/run/test commands and conventions directly in the file, with links for details.
- Never invent repository facts, execution results, secrets, or coverage.
- Every factual discovery output must reference source files, configs, manifests, or commands actually inspected.
- Treat unknowns as investigated follow-up work. After D6, **start D7 by asking the developer one targeted clarification question** when possible, then persist and verify responses.
- Preserve pre-existing agent instructions, app code and developer/prod configuration. Discovery may create/reconcile `.e2e/` files (Compose, Dockerfiles, E2E profiles and safe env examples).
- Update the output contract, templates, and tests together when a field changes.
