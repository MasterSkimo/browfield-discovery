# D7 — Interactive developer clarification

D7 begins **after D0–D6**: initial discovery, Docker foundation, AGENTS.md and first structural validation are complete. It is a real dialogue with the user who launched discovery, not only a list of unresolved facts.

## Starting the conversation

1. Read the discovered unknowns, manifest unresolved findings and developer-question actions, and any prior clarification record.
2. Re-run the evidence ladder from brownfield-inference. Never ask the user something that can be derived from implementation, configuration, tests, CI, deployments or source-backed reasoning.
3. Prioritize questions that materially affect Docker startup, external stubs, auth, data preparation or the future E2E baseline.
4. **Ask one question per message**, with unknown ID, observed source facts, best hypothesis, why evidence is insufficient and the exact decision impacted. Explicitly wait for the answer. Do not end with a generic summary if questions remain.
5. No meaningful questions? Record "No developer clarification required" and mark D7 done without asking a fabricated question.

## Processing a response

- Accept a direct answer, partial answer, correction, "I don't know", skip or stop.
- Save a **minimal sanitized summary**, not raw dialogue, in .agent-context/clarifications.md. Record unknown ID, status, source revision, provenance (developer statement), evidence, remaining assumptions and affected files.
- Verify the response against source/configuration/tests where possible. User testimony is NOT automatically a verified code fact. When it defines a business/operational decision, identify it as a developer decision, not a confirmed runtime behavior.
- Update unknowns, manifest findings/actions, Docker Compose/profiles, AGENTS.md and blueprint only as needed. Reopen affected gates D2/D5/D6 and rerun the quality check; when appropriate rerun non-mutating Compose config validation. Do not fabricate tests or runtime success.
- Continue with the next prioritized question, one at a time.

## Persisted interview lifecycle

- When the first question is posed, record D7 = awaiting_user and manifest.status = awaiting_user_clarification. Keep the question ID and its exact context in clarifications.md.
- An answer moves the relevant row to answered/resolved after validation, or leaves it unresolved with an evidence-based reason.
- "Don't know" and skip are tracked as deferred, not as resolved; if the user says stop, preserve all outstanding work.
- D7 = done when all useful questions were answered, deferred or declined, or when no questions existed. If critical unknowns remain, status still requires investigation.
- In noninteractive execution, **finish the tool's response with the actual question** and persist awaiting_user; another session can resume using /brownfield-clarify.
- Only claim ready_for_e2e_setup after D7 has closed and D0–D6 gates remain valid.

## Privacy

Never store raw chats, developer identity, credentials, client/customer information or unrelated memory. MemPalace/Basic Memory archives require separate explicit permission. Do not ask the developer to inspect code the agent can inspect.

## Example phrasing (illustrative only)

UNK-3 — Identity: I found an OIDC issuer setting in config and middleware requiring JWT, but no test IdP configuration. My hypothesis is that the E2E environment must simulate the external issuer. Can the app accept locally issued tokens, or is a specific external login flow mandatory?
