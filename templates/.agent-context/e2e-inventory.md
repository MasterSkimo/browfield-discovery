# E2E behavior inventory — discovery template

This is an **inventory for future tests**, not a statement that these tests exist.

| ID | Surface | Entry point | Actor/role | Preconditions/data | Observable current effect | Source | Scenario state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E2E-1 | <UI/API/async> | <route/endpoint/message> | <role> | <fixture need> | <visible/API/state/event assertion> | <path:lines> | <to-implement/needs-investigation> |

## Priority flows
- <Main user journeys, API-only flows, async entry points>

## Test boundary and environment tasks
- Run application components, dockerize DB/brokers, stub all outside-app services: <dependency IDs>
- Authentication and data setup requirements: <action IDs>
- Deterministic reset and observation points: <action IDs>

Do not omit known behavior because preparation is unfinished. Record the required work.
