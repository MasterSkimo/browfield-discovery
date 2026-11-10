# Discovery output contract (v0.1)

The agent writes discovery knowledge **and a dedicated, source-backed Docker Compose foundation** into the target repository, using the following structure. Existing files must be preserved and updated additively or represented as a proposed merge if an automatic merge is not safe.

```text
AGENTS.md                            # operational instructions, commands and agent rules
.agent-context/
  manifest.json                     # source SHA, state, artifact links, high-value findings
  architecture.md                   # modules, entry points, important interactions
  execution.md                      # known build/start/config commands (not executed unless observed)
  dependencies.md                   # local infra vs outside-app systems, configs and stubbing clues
  environment-blueprint.md          # actual created Docker files, status, remaining E2E tasks
  discovery-progress.json           # D0-D7 workflow gates, evidence and blockers
  clarifications.md                 # sanitized user Q&A status, answers and validation
  e2e-inventory.md                  # UI/API/async behaviors, roles, data, expected observations
  unknowns.md                       # unresolved facts and recommended targeted investigations
  verification-contract.md          # task -> change -> test -> execution evidence rules
.e2e/
  compose.yaml                       # actual real-app/DB/broker service foundation
  .env.e2e.example                   # safe, source-backed environment keys/defaults
  .gitignore                         # excludes local E2E secrets/config
  docker/                            # required application Dockerfiles
  config/                            # optional dedicated E2E app profiles
```

See [templates](../templates) and [schemas](../schemas). Prefer links over duplicating content; add module-specific instructions only if they carry a real constraint.

## AGENTS.md is an operational guide

Must give developers and agents actionable facts **in the file itself**: overview; module responsibilities and entry points; exact working directories plus installation/build/start/test commands (with declared/executed status); versions/profiles; concrete code and security conventions; E2E setup responsibilities; verification and PR expectations; pointers to deeper context. Merely linking to context files is insufficient. Declare facts derived from CI/build files as declared, not as executed. Nested AGENTS.md may be used for genuine module-specific rules.

## Source provenance

Each high-impact fact needs a traceable reference: relative file path plus line(s) or a named manifest/setting, at the source revision recorded in the manifest. Mark confidence:

- **verified**: directly confirmed from an inspected source or observed command result;
- **inferred**: derived from code structure but not yet runtime-validated;
- **unresolved**: unclear, contradictory, or missing.

A graph edge alone is not proof of runtime behavior. A grounded static inference is still useful and should be published as **inferred** with its reasoning chain; it should not automatically be demoted to an unknown.

Before any unknown is recorded, follow [the investigation protocol](08-investigation-protocol.md), record inspected sources, best hypothesis, counterevidence and precise reason it cannot be resolved.

## Status semantics

- **ready_for_e2e_setup**: all D0–D7 discovery gates completed with evidence, including the **actual dedicated Compose file and environment example** covering real application builds, database/broker containers, external stubbing routes and safe E2E profiles. Remaining fixtures, stubs and tests are tracked downstream. Unknowns may remain as explicit, investigated downstream tasks.
- **awaiting_user_clarification**: D0–D6 created the initial handoff, and an evidence-backed user question has been asked; D7 is `awaiting_user` and the question is persisted.
- **needs_investigation**: critical entry points, boundaries, access assumptions, or configuration locations are still unlocated, or critical blockers remain after the user's responses.

Neither value means the application boots nor that E2E tests pass.

## Conflict and freshness rules

- Do not overwrite existing application code, developer/production configs, infrastructure or agent resources. Only create/reconcile dedicated `.e2e/` files and agent-context output, preserving conflicting existing files.
- Where `AGENTS.md` exists, make only additive non-conflicting edits; for conflicts, write a proposed resolution in `unknowns.md` and leave original content intact.
- Record the analyzed Git revision and warn when the current HEAD differs.
- Sensitive values must never enter the context package. Use environment variable names or secret reference identifiers.
- Generated files are project-specific outputs, not generic claims copied from the templates. Run the read-only gate scripts/validate_discovery.py against the target output before declaring the discovery complete; repair any reported defects.

## Workflow and runtime blueprint requirements

The process is defined in [phases D0–D7](09-discovery-workflow.md) and recorded in `.agent-context/discovery-progress.json`. The [Compose-first contract](10-compose-first-handoff.md) is represented by `.agent-context/environment-blueprint.md`: application-owned services must be built/run as real code, alongside isolated DB/brokers and outside-boundary stubs, with dedicated E2E profiles and environment variable mappings where appropriate. Do not assume that a developer's manual run instructions are the correct autonomous setup. Discovery creates the concrete **Docker foundation** and supporting plan; it does **not start containers or implement full E2E tests/stub behavior**.

## Compose validation record

Manifest outputs must point to `.e2e/compose.yaml` and `.e2e/.env.e2e.example`. The manifest also records `docker_validation`: `pass`, `fail` or `not_run`, exact command and a reason when not passing. A `pass` means only Compose configuration was validated; it never proves builds, startup, application health or E2E results. A real failure blocks `ready_for_e2e_setup`. The output quality gate requires valid scaffolding, a real source-build service, safe local-value exclusions and a recorded validation status.

## Interactive clarification record

The agent must open a real chat with the developer **after** D6 when investigated unknowns remain, not just provide a list. Save the current question, developer answer summaries, provenance, corroboration and unresolved next actions to `.agent-context/clarifications.md`; never save raw conversations or secrets. A human answer can inform an inference or decision but is not automatically verified runtime behavior. Reopen D2/D5/D6 and rerun checks if answers alter Docker or AGENTS instructions. D7 can be `awaiting_user` between sessions; use `/brownfield-clarify` to resume without rerunning D0–D6. See [the protocol](11-interactive-clarification.md).
