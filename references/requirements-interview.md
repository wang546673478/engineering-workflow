# Requirements Interview

## Before asking

Apply the takeover stages in [SKILL.md](../SKILL.md) before starting the detailed interview. On first takeover of existing code without a complete, valid baseline, establish the global baseline and obtain the user's review confirmation first. Before that, ask only basic goal questions necessary to orient discovery; after the answer, resume discovery rather than continuing into feature lists, release scope, or detailed design. A local page scan is not a global baseline. Record the current stage and transition evidence in the authoritative Task. Reuse a verified current baseline and applicable prior confirmation; small fixes retain their minimal workflow, and a project with no existing code records the baseline as not applicable.

Search the repository and read project instructions, existing requirements, issue context, UI/API contracts, schemas, and tests. Ask only about product intent, policy, or tradeoffs that the repository cannot answer. Never ask the user to identify a file or symbol that can be discovered by inspection.

## Explain plainly

在请用户做决定前，先用通俗语言说清楚：已经查到什么、为什么这个决定重要、需要用户选择什么，以及每个选项会带来什么结果。不要只贴技术名词、路径、日志或检查器输出；技术细节只能作为补充。每次只问一个影响最大的决定，并给出简短、互斥的选项和推荐项。用户说看不懂时，用更简单的例子或生活化说法重新解释，再继续提问。

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
