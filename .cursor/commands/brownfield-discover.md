# Full brownfield discovery

Run the brownfield-discovery subagent for the CURRENT repository and wait for its complete output. Follow D0–D6 discovery phases, recording evidence and status in discovery-progress.json. Use shared brownfield-repository, brownfield-boundaries, brownfield-runtime-topology, brownfield-e2e-readiness, brownfield-inference and brownfield-handoff skills, plus the templates and quality validator.

Do the investigation now, not merely propose a plan. Trace concrete app paths, runtime and dependency wiring, UI/API/async behaviors, data and tests. Resolve missing facts autonomously using independent evidence before marking them unknown; record evidence, inferences and precise unresolved items.

Generate a real AGENTS.md with direct project-specific setup, build, run, test commands, module map, conventions, security, E2E responsibilities and evidence rules. Produce the .agent-context files and run the quality gate if available. Correct deficient output and report status.

No application code, Docker, stubs, data scripts or E2E tests are to be created in this discovery mission.

Derive a full-stack Compose-first environment blueprint for future agents, including building actual apps, DB/broker containers, external stubs and dedicated E2E application profiles/environment overrides. The discovery agent must not implement those files.
