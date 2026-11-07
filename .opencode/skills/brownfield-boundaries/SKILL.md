---
name: brownfield-boundaries
description: Classify application boundaries, databases, message brokers, auth, and external systems requiring stubs for autonomous E2E setup.
---

## Procedure

1. Find database clients/configuration and schema/migration sources; record engines, version hints, database names and safe config **keys**.
2. Find broker clients, messaging topology declarations, subscribers, producers, and retry/dead-letter hints.
3. Identify *application-owned* components versus services outside the application test boundary. Do not mock application behavior.
4. For every external boundary identify protocol, URLs/configuration keys, auth type, contracts/schemas and success/error semantics if evidenced.
5. Map environment variables, profiles, ports, health endpoints and credential **names** without recording values.
6. Flag dynamic wiring and unconfirmed Graphify relationships as inferred, not verified.
7. Write `.agent-context/dependencies.md` and unresolved seams in `unknowns.md`.

## Classification

Use `application`, `docker-db`, `docker-messaging`, `external-stub` or `unresolved`. Missing contracts/data/auth do not make a dependency impossible to test; create targeted follow-up work.
