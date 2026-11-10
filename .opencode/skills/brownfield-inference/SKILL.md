---
name: brownfield-inference
description: Resolve apparent brownfield unknowns through independent evidence, code-to-config tracing, and explicit bounded inference before escalating.
---

# Resolve evidence before escalating

Load this skill after the high-level inventory and again immediately before handoff. Read the investigation protocol under .agents/brownfield-discovery/docs/08-investigation-protocol.md if installed, otherwise follow this procedure.

1. Gather the list of all unknown or "requires developer" statements from your draft inventory.
2. For each, inspect the immediate producer or configuration and at least one independent evidence channel (tests, CI/CD, docs, migrations, client call sites, manifests, generated contracts or Git history).
3. For a UI/API/event flow, follow one representative trace from entry point through handler, state mutation/emission and externally visible outcome; record relevant role/fixture assumptions.
4. Compare competing hypotheses and inspect counterexamples. Capture the reasoning and evidence even when no runtime is available.
5. Promote plausible deductions to **inferred**, not **unresolved**, when grounded in source and supported by a specific reasoning chain. Never imply runtime verification.
6. Only escalate after the evidence ladder is exhausted or access/business authority is genuinely needed; record searched sources, best hypothesis, reason it cannot be settled, and a targeted next action. Do not label anything "untestable".
7. Repeat until no unexplained unknowns remain. Depth is measured by E2E-relevant flows, not by classes read.

Examples:
- Postgres driver + migration scripts + repository mapping => PostgreSQL Docker dependency, without needing to run it.
- RabbitMQ listener + publisher + exchange declarations => infer required broker/topology and observable message effect.
- Browser route + HTTP client + backend endpoint => candidate UI E2E flow; use tests/authorization config to infer preconditions.

The skill does not modify application files, start infrastructure, create test data or write Playwright/Newman suites.

## Docker-oriented deduction

If README tells developers to manually start apps or services, cross-check CI/build/containers to deduce how a downstream agent can build them as images. Infer E2E profile names/variable overrides only with configuration evidence; propose dedicated test configuration when existing profiles are unsuitable. A missing existing Compose file is not an unknown runtime architecture.

## Docker artifacts as evidence

The absence of an existing compose file should trigger **creation** of the isolated `.e2e/compose.yaml` and required app Dockerfiles, not escalation as an unknown. Ground images, build contexts and app configuration names in actual source/build/deploy evidence, and record incomplete stub/data/test work for the next agent.
