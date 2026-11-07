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

## AGENTS.md is intentionally short

Must state: scope/boundaries, how to navigate the context package, code conventions evidenced by sources, how to locate and run relevant checks, and minimum proof required to declare future work complete. It must not claim unverified commands work.

## Source provenance

Each high-impact fact needs a traceable reference: relative file path plus line(s) or a named manifest/setting, at the source revision recorded in the manifest. Mark confidence:

- **verified**: directly confirmed from an inspected source or observed command result;
- **inferred**: derived from code structure but not yet runtime-validated;
- **unresolved**: unclear, contradictory, or missing.

A graph edge alone is not proof of runtime behavior.

## Status semantics

- **ready_for_e2e_setup**: enough information is available for another agent to start provisioning and E2E implementation; unknowns may remain as explicit work items.
- **needs_investigation**: critical entry points, boundaries, access assumptions, or configuration locations are still unlocated.

Neither value means the application boots nor that E2E tests pass.

## Conflict and freshness rules

- Do not overwrite existing instructions, scripts, infrastructure, or agent resources.
- Where `AGENTS.md` exists, make only additive non-conflicting edits; for conflicts, write a proposed resolution in `unknowns.md` and leave original content intact.
- Record the analyzed Git revision and warn when the current HEAD differs.
- Sensitive values must never enter the context package. Use environment variable names or secret reference identifiers.
- Generated files are project-specific outputs, not generic claims copied from the templates.
