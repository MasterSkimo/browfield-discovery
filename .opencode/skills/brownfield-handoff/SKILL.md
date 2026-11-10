---
name: brownfield-handoff
description: Assemble concise AGENTS.md instructions, discovery manifest, evidence contract and actionable handoff to autonomous development agents.
---

## Procedure

1. Review discovered facts and make their sources and confidence inspectable.
2. Generate a substantive, directly actionable `AGENTS.md` with source-based working directories, actual setup/build/run/test commands, module boundaries, conventions, safe E2E Docker invocation and proof obligations; links are supplemental.
3. Store details under `.agent-context/`; use links instead of duplicating long inventories. Use templates/schemas from `.agents/brownfield-discovery/` when the package is installed by setup.py.
4. Provide `verification-contract.md` for AC -> changes -> automated assertions -> execution artifacts -> outcome.
5. Complete `manifest.json` with analyzed revision, actual artifact paths, findings and status; never leave template placeholders in completed output.
6. Capture unknowns, conflicts and developer questions in `unknowns.md` with next steps.
7. Review `git diff` or equivalent: **only** generated agent context, dedicated `.e2e/` Docker foundation and narrowly scoped ignore rules may change. No application/source/dev config edits or secrets.
8. Report actual Compose file, Dockerfiles, dedicated app profiles, environment example and non-mutating Compose config validation status. Do not assert running containers, built images or E2E coverage.

## Deep exploration requirements

AGENTS.md is a WORKING GUIDE, not a file index. It must directly include actual commands and working directories for installation, build, running and tests (with evidence and declared/executed status), project/module map, code and security conventions, E2E mission and proof requirements, and links for deeper details. Only create nested AGENTS.md for real module-specific constraints. Check every unresolved against brownfield-inference and run the structural quality validator. If the gate fails, revise outputs and re-run; never claim successful completion with only generic placeholders.

## Existing instructions

Preserve `AGENTS.md` and module-specific rules already present. Add non-conflicting pointers if safe; otherwise document a merge proposal and notify the caller. Never silently replace rules or claim precedence over the existing project policy.

## Workflow handoff

Before completion, require D0–D6 progression with evidence in `.agent-context/discovery-progress.json`. Verify **actual** `.e2e/compose.yaml`, `.e2e/.env.e2e.example`, Dockerfiles/profiles where needed and `.e2e/.gitignore` exist; `.agent-context/environment-blueprint.md` must describe their sources, all app/DB/broker services, external stub wiring, profile/env settings, config-check result, fixture/reset tasks and gaps. Include the runtime strategy directly in AGENTS.md, while linking to the detailed blueprint. Never claim provisioning or build success that did not occur.

## Post-handoff developer interview

D6 is not the end of the conversation. Always invoke brownfield-clarification as D7. If any investigated user-answerable unknown remains, **ask one specific question directly to the user**, save `awaiting_user` and wait for their response. On answers, update findings and affected Docker/AGENTS/context, revalidate and continue. Do not close the session with a list of unknowns; a separate `/brownfield-clarify` command resumes a pending interview.
