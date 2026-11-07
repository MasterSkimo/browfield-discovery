# Acceptance criteria for the initial discovery proposal

## Contract/agent package

- [ ] OpenCode v2 loads the agent and on-demand skills from the documented paths.
- [ ] The agent can operate from a target project root and produce the seven listed outputs plus `AGENTS.md`.
- [ ] No application source, infrastructure file, or pre-existing agent instruction is overwritten.
- [ ] Source revision is recorded; findings are source-backed and labeled verified/inferred/unresolved.
- [ ] The output is scoped to high-level architecture and E2E-relevant paths, without a class-by-class code dump.
- [ ] All detected databases and brokers have configuration locations recorded.
- [ ] All discovered outside-application boundaries have stubbing pointers or explicit unknowns.
- [ ] UI/API/async behavior inventories include identification of roles, data, and observable effects.
- [ ] Each unknown becomes a targeted investigation or developer question; no 'untestable' exemption.
- [ ] Next-agent instructions include Playwright/Newman requirements and the reliability/evidence contract.
- [ ] No credentials, token values, or sensitive test records appear in the generated artifacts.
- [ ] Re-running discovery after a code change updates impacted findings and flags stale evidence.

## Validation fixtures (future acceptance runs)

Evaluate on (a) one backend/API repo, (b) one UI + backend repo, (c) one multi-service repo with DB and messaging. Compare a fresh E2E-bootstrap agent operating with and without the discovery outputs. Record exploration repetition, ability to identify services/stubs/data, and ungrounded assertions.

This PR proposes these criteria; real brownfield acceptance runs are **not** claimed here.
