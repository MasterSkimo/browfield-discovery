---
description: Full evidence-led brownfield discovery and AGENTS.md preparation
agent: brownfield-discovery
subagent: false
---

Perform the COMPLETE brownfield discovery from this repository root, rather than answering with a plan. Optional focus/constraints: $ARGUMENTS

Follow the full D0–D7 evidence-gated workflow and update discovery-progress.json as each phase completes. Load all brownfield skills, including brownfield-runtime-topology and brownfield-inference. **Create the real `.e2e/compose.yaml` foundation** and required Dockerfiles, isolated E2E app config, env example and ignore rules during D2; document Compose config validation pass/fail/not_run. Continue through repository mapping, runtime/integration boundary reconstruction, representative UI/API/async tracing, cross-source inference, E2E readiness and AGENTS.md delivery.

Before declaring anything unknown, investigate its implementation, configuration, tests and CI/deploy evidence; write the strongest bounded inference when supported. Do not read every class or change application code/developer configs. E2E-specific Docker files ARE an expected output.

Write the complete project-specific AGENTS.md per agents.md: actual setup/build/run/test commands and directories, module map, conventions, security, E2E instructions and acceptance/evidence requirements. Write the .agent-context package, then run its structural quality validator if available. Repair failed checks; report remaining blockers with investigation trails.

After D6, start D7 **in this same chat**: if real developer-answerable unknowns remain, persist the active question and `awaiting_user` status, then ask the user ONE evidence-backed clarification question and wait. Never finish with only an unknowns list. If the user replies, incorporate and verify the answer, update Docker/AGENTS/context, rerun relevant checks and continue. For a later session use `/brownfield-clarify`. Finish only after the output passes the gate (or explain exactly why a validation cannot run). This command must execute the full discovery, not just outline the work.
