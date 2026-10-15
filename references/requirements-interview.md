# Requirements Interview

## Before asking

Apply the takeover stages in [SKILL.md](../SKILL.md) before starting the detailed interview. On first takeover of existing code without a complete, valid baseline, establish the global baseline and obtain the user's review confirmation first. Before that, ask only basic goal questions necessary to orient discovery; after the answer, resume discovery rather than continuing into feature lists, release scope, or detailed design. A local page scan is not a global baseline. Record the current stage and transition evidence in the authoritative Task. Reuse a verified current baseline and applicable prior confirmation; small fixes retain their minimal workflow, and a project with no existing code records the baseline as not applicable.

Search the repository and read project instructions, existing requirements, issue context, UI/API contracts, schemas, and tests. Ask only about product intent, policy, or tradeoffs that the repository cannot answer. Never ask the user to identify a file or symbol that can be discovered by inspection.

## Continuous discussion records

In an enabled project, follow-up answers and short confirmations continue the active task without another explicit skill invocation. Any discussion of adding, changing or removing a functional module, or changing its behavior, permissions, billing or data relationships, belongs in the requirements record before implementation starts. Update the existing authoritative requirements/decision record and current task state as new information arrives, before the next question or ending the turn; do not wait until the module review. These may share one file. Reuse the same entries and links for repeated information. A factual answer with no new change information does not need a duplicate requirement or artificial document edit.

Distinguish repository facts (with source evidence), candidates (not yet agreed), confirmed decisions (with the user's statement, date and scope), and deferred discussion. Recording a candidate does not confirm it. For a deferred item, retain its module, conclusions already reached, remaining questions, effects/dependencies and the condition for resuming discussion; do not invent a date or treat deferral as cancellation. Revisit it before dependent design or implementation. A deferred high-impact dependency remains unresolved for the affected work.

Track requirement state separately from implementation state using the project's vocabulary. A confirmed requirement may still be unimplemented; requirement confirmation or a module review does not itself authorize implementation. Keep the current summary, open items and next action up to date when decisions change, and mark superseded statements as history instead of leaving conflicting current instructions. If saving fails, report the failure and what remains unsaved; do not claim the record was updated.

## Explain plainly

在请用户做决定前，先用通俗语言说清楚：已经查到什么、为什么这个决定重要、需要用户选择什么，以及每个选项会带来什么结果。不要只贴技术名词、路径、日志或检查器输出；技术细节只能作为补充。每次只问一个影响最大的决定，并给出简短、互斥的选项和推荐项。用户说看不懂时，用更简单的例子或生活化说法重新解释，再继续提问。

## One-question loop

Ask exactly one material question per turn. Offer concrete, mutually exclusive choices when possible and identify the recommended default. After each answer:

1. Save new information and decisions to the existing records above, with sources/dates and affected requirement IDs as applicable.
2. Re-evaluate the remaining unknowns and remove questions answered by the new decision.
3. Ask the next highest-impact question, or stop when the confidence threshold is met.

For new projects and major changes, cover: goal and users, in/out of scope, workflows, permissions, data ownership, integrations, failure/retry behavior, compatibility, rollout, and acceptance evidence. For small changes, ask only missing information that could alter the fix.

## 95% readiness

The proposal is ready when goal, audience, scope, constraints, authoritative owners, cross-layer data flow, edge behavior, and acceptance tests are explicit. Do not continue questioning for cosmetic preferences. Preserve unresolved low-impact choices as documented engineering defaults.

Readiness review: for each dimension write confirmed, repository fact, explicit default, not applicable (with reason), or unresolved. A high-impact unresolved item keeps the interview open; a default must not masquerade as a user decision. Keep the next question tied to the last answer and the highest-impact remaining choice. Use [the decision-log template](../assets/templates/decision-log.md) if no project log exists.

## Module review

For this review, a module is the cohesive functional topic being discussed with the user; source-directory boundaries do not define a separate review unit. When that discussion concludes, combine the completeness check with the user's module review. Compare the discussion with the current requirements, changes, open/deferred items and related effects, then present that one reviewable summary in plain language. Let the user check understanding, scope and omissions; record their statement, date, reviewed scope and document version. If changes are needed, update that module and its affected links. Do not add a separate concentrated check or approval after every answer; continuous saving during discussion still applies.

Keep the whole-system baseline review and the complete implementation proposal approval required by SKILL.md. Module reviews do not replace either gate. Reuse valid prior confirmations; after later changes, recheck and obtain review for the affected parts rather than restarting unrelated discussions.

## Record

Keep the current requirements and interview log in the project's existing planning artifacts, linking one authoritative location for each fact or decision. Do not put credentials, secrets, or private user data in them. When an answer changes scope, carry it into the affected Spec, Plan and Tasks before dependent implementation; keep target requirements separate from the current-system baseline.
