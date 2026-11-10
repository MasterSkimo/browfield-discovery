---
name: brownfield-clarification
description: Interview the developer after discovery about evidence-backed unknowns, persist sanitized decisions and update Docker E2E handoff.
---

# D7 — Clarification loop

After the first D0–D6 investigation and **attempted** quality check (even when D6 is blocked by a genuine user-answerable unknown), or via /brownfield-clarify, read docs/11-interactive-clarification.md from the installed package.

1. Read manifest, progress, unknowns and existing clarifications; never restart a whole-codebase exploration when resuming.
2. Complete autonomous evidence investigation first. List only developer-answerable questions not settled by code, tests, config, CI or evidence-based inference.
3. Ask the highest-impact question **in the chat**, ONE per turn, with its unknown ID, source facts, likely interpretation and why a human answer matters. Do not merely print a TODO summary.
4. Before asking, persist an awaiting_user D7 state and the question in .agent-context/clarifications.md and set manifest.status to awaiting_user_clarification.
5. On the reply, record a minimal sanitized answer, verify claims against current sources when possible, and update relevant unknowns, findings, AGENTS.md, Docker foundation/profiles and E2E blueprint. Never treat developer testimony as automatically verified implementation behavior.
6. Reopen/re-run affected D2, D5 and D6 quality gates before presenting another question.
7. If the user cannot answer, skips or stops, preserve unresolved items and precise downstream actions. D7 becomes done only after all useful questions are resolved/deferred/declined or there are no questions; readiness must still reflect critical unresolved issues.
8. In one-shot sessions, end with the question and leave saved state for /brownfield-clarify; never falsely claim dialogue completion.

No secrets, raw transcripts, unrelated personal memory or developer names in artifacts.
