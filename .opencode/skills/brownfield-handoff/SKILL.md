---
name: brownfield-handoff
description: Assemble concise AGENTS.md instructions, discovery manifest, evidence contract and actionable handoff to autonomous development agents.
---

## Procedure

1. Review discovered facts and make their sources and confidence inspectable.
2. Generate a minimal `AGENTS.md`: repository orientation, module boundaries, conventions, links, safe execution hints and proof obligations.
3. Store details under `.agent-context/`; use links instead of duplicating long inventories.
4. Provide `verification-contract.md` for AC -> changes -> automated assertions -> execution artifacts -> outcome.
5. Complete `manifest.json` with analyzed revision, actual artifact paths, findings and status; never leave template placeholders in completed output.
6. Capture unknowns, conflicts and developer questions in `unknowns.md` with next steps.
7. Review `git diff` or equivalent: **only** agent instructions and discovery outputs may change. No secrets.
8. Report handoff readiness without asserting a running environment or E2E coverage.

## Existing instructions

Preserve `AGENTS.md` and module-specific rules already present. Add non-conflicting pointers if safe; otherwise document a merge proposal and notify the caller. Never silently replace rules or claim precedence over the existing project policy.
