# Execution and configuration — discovery template

## Source revision
<SHA>

## Candidate commands
| Purpose | Directory | Command | Source | Observation |
| --- | --- | --- | --- | --- |
| <build/start/check> | <module> | <command> | <path:lines> | <declared/observed success/observed failure> |

## Runtime components and ports
| Component | Profile | Config keys | Port | Health indicator | Source |
| --- | --- | --- | --- | --- | --- |
| <component> | <profile> | <non-secret names> | <port> | <path> | <path:lines> |

## Local requirements
- Runtime versions and tooling: <references>
- Profiles and feature flags: <references>
- Build/start uncertainties: <action IDs>

Do not treat commands discovered in README files as successfully executed.

## Autonomous environment design (implemented as Docker scaffold by discovery)

Create actual `.e2e/compose.yaml` and required Dockerfiles/profile files/overrides, using source-grounded build contexts and environmental wiring. Keep developer configuration untouched and record source evidence. Distinguish declared commands from observed execution. Cross-reference `environment-blueprint.md`.

## Discovery-created E2E runtime

Record the actual `.e2e/compose.yaml`, dedicated Dockerfiles and profile files, safe env example, supported `docker compose ... config` command, and validation result. Full application build/start and tests remain downstream.
