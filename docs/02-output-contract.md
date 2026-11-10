# Discovery output contract (v0.1)

The agent writes **only discovery information** into the target repository, using the following suggested structure. Existing files must be preserved and updated additively or represented as a proposed merge if an automatic merge is not safe.

```text
AGENTS.md                            # short, authoritative agent navigation and non-negotiable rules
.agent-context/
  manifest.json                     # source SHA, state, artifact links, high-value findings
  architecture.md                   # modules, entry points, important interactions
  execution.md                      # known build/start/config commands (not executed unless observed)
  dependencies.md                   # local infra vs outside-app systems, configs and stubbing clues
  e2e-inventory.md                  # UI/API/async behaviors, roles, data, expected observations
  unknowns.md                       # unresolved facts and recommended targeted investigations
  verification-contract.md          # task -> change -> test -> execution evidence rules
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

- **ready_for_e2e_setup**: enough information is available for another agent to start provisioning and E2E implementation; unknowns may remain as explicit work items.
- **needs_investigation**: critical entry points, boundaries, access assumptions, or configuration locations are still unlocated.

Neither value means the application boots nor that E2E tests pass.

## Conflict and freshness rules

- Do not overwrite existing instructions, scripts, infrastructure, or agent resources.
- Where `AGENTS.md` exists, make only additive non-conflicting edits; for conflicts, write a proposed resolution in `unknowns.md` and leave original content intact.
- Record the analyzed Git revision and warn when the current HEAD differs.
- Sensitive values must never enter the context package. Use environment variable names or secret reference identifiers.
- Generated files are project-specific outputs, not generic claims copied from the templates. Run the read-only gate scripts/validate_discovery.py against the target output before declaring the discovery complete; repair any reported defects.
