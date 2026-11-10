# Dependency and test-boundary inventory — discovery template

| ID | Component | Classification | Protocol / purpose | Configuration/contract location | Safe notes / next action |
| --- | --- | --- | --- | --- | --- |
| DEP-1 | <name> | <application/docker-db/docker-messaging/external-stub/unresolved> | <protocol> | <path:lines> | <next action> |

## Persistence
- Engines, version hints, migrations, schemas and seed/reset references: <evidence>

## Messaging
- Brokers, exchanges/queues/topics, publishers/consumers, failure/retry behavior: <evidence>

## External services to stub
- For each outside-app dependency: endpoint/configuration key, request/response contracts, authentication **type**, observed error responses: <evidence>

## Identity and security boundaries
- Roles, login flows and token/header names only; never store values: <evidence>

## Unknowns
- <links to unknowns.md items>

## Intended autonomous runtime

Identify whether each **real** application component can be built/run in a full-stack Compose project. List database/broker containers, external stubs and dependencies, including profile/config keys and source evidence. Do not assume developer-hosted infrastructure or IDE processes. See `environment-blueprint.md` for the Compose-first handoff.
