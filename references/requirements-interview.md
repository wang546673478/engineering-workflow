# Requirements Interview

## Before asking

Search the repository and read project instructions, existing requirements, issue context, UI/API contracts, schemas, and tests. Ask only about product intent, policy, or tradeoffs that the repository cannot answer. Never ask the user to identify a file or symbol that can be discovered by inspection.

## One-question loop

Ask exactly one material question per turn. Offer concrete, mutually exclusive choices when possible and identify the recommended default. After each answer:

1. Record the decision, source, date, and affected requirement IDs.
2. Re-evaluate the remaining unknowns and remove questions answered by the new decision.
3. Ask the next highest-impact question, or stop when the confidence threshold is met.

For new projects and major changes, cover: goal and users, in/out of scope, workflows, permissions, data ownership, integrations, failure/retry behavior, compatibility, rollout, and acceptance evidence. For small changes, ask only missing information that could alter the fix.

## 95% readiness

The proposal is ready when goal, audience, scope, constraints, authoritative owners, cross-layer data flow, edge behavior, and acceptance tests are explicit. Do not continue questioning for cosmetic preferences. Preserve unresolved low-impact choices as documented engineering defaults.

Readiness review: for each dimension write confirmed, repository fact, explicit default, not applicable (with reason), or unresolved. A high-impact unresolved item keeps the interview open; a default must not masquerade as a user decision. Keep the next question tied to the last answer and the highest-impact remaining choice. Use [the decision-log template](../assets/templates/decision-log.md) if no project log exists.

## Record

Keep an interview log in the project's planning artifacts. Do not put credentials, secrets, or private user data in it. When a material answer changes scope, update Spec, Plan, and Tasks before implementation.
