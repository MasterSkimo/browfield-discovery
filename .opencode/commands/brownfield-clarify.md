---
description: Resume interactive brownfield clarification and reconcile Docker E2E instructions
agent: brownfield-discovery
subagent: false
---

Resume D7 from this project's saved .agent-context/manifest.json, discovery-progress.json, unknowns.md and clarifications.md. Optional new answer: $ARGUMENTS

Use brownfield-clarification and brownfield-inference. Do not repeat completed D0–D6 phases or previously answered questions.

If the user has supplied an answer, save a sanitized summary, verify against code/config as far as possible, update impacted Docker foundation/AGENTS/context, and revalidate. Then ask the next developer-answerable question, ONE per turn, with evidence and current hypothesis. If no answer was supplied, ask the highest-priority outstanding question.

Respect "I don't know", skip and stop. If all questions are answered/deferred or none existed, close D7 and report actual outstanding E2E work.
