# Requirements Interview

## Before asking

Apply the takeover stages in [SKILL.md](../SKILL.md) before starting the detailed interview. On first takeover of existing code without a complete, valid baseline, establish the global baseline and obtain the user's review confirmation first. Before that, ask only basic goal questions necessary to orient discovery; after the answer, resume discovery rather than continuing into feature lists, release scope, or detailed design. A local page scan is not a global baseline. Record the current stage and transition evidence in the authoritative Task. Reuse a verified current baseline and applicable prior confirmation; small fixes retain their minimal workflow, and a project with no existing code records the baseline as not applicable.

For a no-implementation project, record the empty starting state and constraints before interviewing; no review of a nonexistent system is required. Follow [the greenfield lifecycle](baseline-linked-artifacts.md#新项目从零建立基线). Baseline not-applicable is temporary: target architecture belongs in Plan, implementation produces partial factual views, and delivery requires a complete factual baseline. Existing code lacking documents still requires discovery.

Search the repository and read project instructions, existing requirements, issue context, UI/API contracts, schemas, and tests. Ask only about product intent, policy, or tradeoffs that the repository cannot answer. Never ask the user to identify a file or symbol that can be discovered by inspection.

## Continuous discussion records

In an enabled project, follow-up answers and short confirmations continue the active task without another explicit skill invocation. Any discussion of adding, changing or removing a functional module, or changing its behavior, permissions, billing or data relationships, belongs in the requirements record before implementation starts. Update the existing authoritative requirements/decision record and current task state as new information arrives, before the next question or ending the turn; do not wait until the module review. These may share one file. Reuse the same entries and links for repeated information. A factual answer with no new change information does not need a duplicate requirement or artificial document edit.

Distinguish repository facts (with source evidence), candidates (not yet agreed), confirmed decisions (with the user's statement, date and scope), and deferred discussion. Recording a candidate does not confirm it. For a deferred item, retain its module, conclusions already reached, remaining questions, effects/dependencies and the condition for resuming discussion; do not invent a date or treat deferral as cancellation. Revisit it before dependent design or implementation. A deferred high-impact dependency remains unresolved for the affected work.

Track requirement state separately from implementation state using the project's vocabulary. A confirmed requirement may still be unimplemented; requirement confirmation or a module review does not itself authorize implementation. Keep the current summary, open items and next action up to date when decisions change, and mark superseded statements as history instead of leaving conflicting current instructions. If saving fails, report the failure and what remains unsaved; do not claim the record was updated.

## Explain plainly

在请用户做决定前，先用通俗语言说清楚：已经查到什么、为什么这个决定重要、需要用户选择什么，以及每个选项会带来什么结果。不要只贴技术名词、路径、日志或检查器输出；技术细节只能作为补充。每次只问一个影响最大的决定，并给出简短、互斥的选项和推荐项。用户说看不懂时，用更简单的例子或生活化说法重新解释，再继续提问。

## One-question loop

When a material product decision or unavailable access input is actually missing, ask at most one question at a time. Investigation that can proceed independently needs no question. Offer concrete, mutually exclusive choices when possible and identify the recommended default. After each answer:

1. Save new information and decisions to the existing records above, with sources/dates and affected requirement IDs as applicable.
2. Re-evaluate the remaining unknowns and remove questions answered by the new decision.
3. Ask the next highest-impact question, or stop when the confidence threshold is met.

For new projects and major changes, cover: goal and users, in/out of scope, workflows, permissions, data ownership, integrations, failure/retry behavior, compatibility, rollout, and acceptance evidence. For small changes, ask only missing information that could alter the fix.

## 95% readiness

The proposal is ready when goal, audience, scope, constraints, authoritative owners, cross-layer data flow, edge behavior, and acceptance tests are explicit. Do not continue questioning for cosmetic preferences. Preserve unresolved low-impact choices as documented engineering defaults.

Readiness review: for each dimension write confirmed, repository fact, explicit default, not applicable (with reason), or unresolved. A high-impact unresolved item keeps the interview open; a default must not masquerade as a user decision. Keep the next question tied to the last answer and the highest-impact remaining choice. Use [the decision-log template](../assets/templates/decision-log.md) if no project log exists.

## Module review

If a new choice conflicts with an earlier user principle or approved requirement, preserve both sources and explain which behavior changes, which remains, and whether an exception is intended. Ask only about an unresolved material boundary; an explicit instruction replacing the old rule can be recorded directly. Do not rewrite the old statement merely to make the documents appear consistent. Apply factual corrections to Baseline autonomously, keeping goal changes in a new Spec revision.

A user's goal or answer to a requirement question confirms only its actual scope. It does not approve a complete implementation Plan that has not been presented. Show the converged module scope and complete proposal together when appropriate; one explicit reply covering both may serve both records without another approval round. Reuse valid earlier approvals within their scope. Record new work outside that scope as pending while independent authorized investigation continues.

For this review, a module is the cohesive functional topic being discussed with the user; source-directory boundaries do not define a separate review unit. When that discussion concludes, combine the completeness check with the user's module review. Compare the discussion with the current requirements, changes, open/deferred items and related effects, then present that one reviewable summary in plain language. Let the user check understanding, scope and omissions; record their statement, date, reviewed scope and document version. If changes are needed, update that module and its affected links. Do not add a separate concentrated check or approval after every answer; continuous saving during discussion still applies.

Keep the whole-system baseline review and the complete implementation proposal approval required by SKILL.md. Module reviews do not replace either gate. Reuse valid prior confirmations; after later changes, recheck and obtain review for the affected parts rather than restarting unrelated discussions.

Baseline review accepts the source/worktree version, scope, main findings and stated limits. The agent owns technical and semantic investigation; do not ask the user to guarantee field-level facts or production correctness. The baseline stays current after acceptance: evidence-based factual corrections proceed autonomously, while invalidated product decisions or implementation premises reopen only the affected review under [project-documentation.md](project-documentation.md#continuous-correction).

## Optional requirement and acceptance examples

EARS can help make a requirement's conditions and observable response explicit. Use it when it improves an entry, or keep the project's existing prose, Chinese, tables and other formats. Historical requirements need no conversion, and English keywords such as SHALL are not required. These synthetic examples explain notation only; their product rules are candidates until actually confirmed for the project:

| EARS type | Chinese equivalent and example |
| --- | --- |
| Ubiquitous / 始终型 | 系统应当……；例如：系统应以 UTF-8 编码保存文本记录。 |
| Event-driven / 事件型 | 当……发生时，系统应当……；例如：当用户提交空输入时，系统应显示校验提示。 |
| State-driven / 状态型 | 在……状态期间，系统应当……；例如：在只读状态期间，系统应禁用保存操作。 |
| Unwanted behavior / 异常型 | 如果……异常发生，那么系统应当……；例如：如果保存时网络中断，那么系统应保留当前输入并提示重试。 |
| Optional feature / 可选型 | 在启用……能力的情况下，系统应当……；例如：在启用导出能力的情况下，系统应提供导出入口。 |
| Combined / 组合型 | 明确组合的条件与响应；例如：在启用批量导入能力且处于编辑状态期间，当用户提交空文件时，系统应显示校验提示。 |

The ubiquitous form legitimately has no separate trigger. A well-formed sentence does not prove that a rule is complete, correct or approved. Retain the entry's source, candidate/confirmed/deferred state and the existing review/implementation distinction.

Given–When–Then can describe acceptance as a precondition, action and observable result. For a project-confirmed empty-input rule, an illustrative entry using that project's own requirement/acceptance IDs could read:

> Given / 已知：当前输入为空，且尚未保存记录。
>
> When / 当：用户提交输入。
>
> Then / 那么：显示校验提示，不新增无效记录。

Link the acceptance entry to its existing requirement ID; keep the original IDs, status and traceability. The example's “do not save” rule must also have a confirmed basis before adoption. This notation is readable acceptance, not an installed runner, executable test or passing result. It introduces no parser, lint gate, testing framework or mandatory record structure.

## Record

Keep the current requirements and interview log in the project's existing planning artifacts, linking one authoritative location for each fact or decision. Do not put credentials, secrets, or private user data in them. When an answer changes scope, carry it into the affected Spec, Plan and Tasks before dependent implementation; keep target requirements separate from the current-system baseline.
