# TASK-ISSUE23-RECORD-INTEGRITY-01：权威工程记录完整性事故后续

## 当前状态

- 日期：2026-10-22（Asia/Shanghai）。源基点：Issue #23 原实现 1.8.0 / `a3129db61b7b1d5d1410efd2836b17ba03fbd91e`；当前本地已有用户修改。此次方案经用户确认后，新增本地 archive CLI/tests/流程说明及链接状态；不改变原实现的 1.8 流程合同。
- 触发：GitHub Issue #23 新评论报告 1.8.0 会话中文档误覆盖；用户明确补充：“这是个bug看看要怎么修复,这是实际运用中出现的问题,讨论下应该怎么修复”，并纠正目标为“从全局来看问题应该怎么修复,而不是打补丁的做法”。
- 当前阶段：用户确认按全局方案范围实施，并明确只要原有流程不变；本地 archive CLI 与回归已实现。1.8 审核流程保持。宿主级写入拦截不可用，明确标 unsupported；外部项目迁移/远端备份/提交发布均未执行。
- 关联会话：Issue 评论所指的“联通中转站”最新会话 `01a15a6d-3a4a-7713-94c6-4b2e757294f6`，工作区 `E:\liantongzhongzhuanzhan`，当时 HEAD `6cf0d90b5ff27f901697dddd61e0c28aba8efefc`。目标工作区未被本任务修改。
- 证据边界：Issue 评论和当前 Task 明确记录旧 Task 被误覆盖、重建及部分独有历史不可恢复。旧 Task 为未跟踪文件，不能从当前 Git 历史恢复。当前审计工具无法访问目标设备的编辑器/系统历史，也没有确认原始 shell 写入项；因此旧原文完整性与具体触发命令仍未验证。

## 工件链

`BASELINE-ISSUE23-02` → [SPEC-ISSUE23-RI-01](issue-23-record-integrity-spec.md)（本地恢复范围已确认，RI-06 host enforcement unsupported）→ [PLAN-ISSUE23-RI-01](issue-23-record-integrity-plan.md)（本地 archive slice）→ 本 Task → [archive tests](../scripts/tests/test_task_archive.py)。此前 `SPEC-ISSUE23-01` / `PLAN-ISSUE23-01 r1` 与 1.8.0 保持已完成、流程范围冻结。

## Skill review

来源：当前会话 Skills catalog，检查时间 2026-10-22；用户后续明确授权本地记录恢复实现，不改变审批和验证流程。

| 候选 | 来源/版本 | 决定与理由 |
| --- | --- | --- |
| engineering-workflow | `SKILL.md` / 当前本机 Skill；1.8.0，源 `a3129db` | 采用；用户明确授权本地记录恢复能力，保留既有阶段与检查合同 |
| skill-creator | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`；未提供版本 | 采用；候选涉及 Skill 行为与宿主职责，避免把单次失败固化成脆弱规则 |
| triage-issue | `C:/Users/54667/.agents/skills/triage-issue/SKILL.md`；未提供版本 | 采用诊断/root-cause/TDD plan 方法；不创建重复 GitHub issue，当前要求是架构讨论 |
| tdd | `C:/Users/54667/.agents/skills/tdd/SKILL.md`；未提供版本 | 采用；对可观察 CLI 行为逐项做红绿回归，覆盖整篇误覆盖、保存、冲突、恢复及失败保护 |
| planning-with-files | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`；未提供版本 | 不采用；使用工程清单已链接的 Spec/Plan/Task 与 traceability，不另建台账 |

## 当前结论

根因不是单条写文件命令，而是权威状态缺少独立历史与强制保存边界：当前 Task 同时承担 current state 和独有历史；项目文档可从 unrestricted shell 直接覆盖；未跟踪文件不受 Git 版本恢复保护；检查器不管理文档写入/版本；事故发生后重建损失只能诚实标注。原 Issue23 的批准摘要 digest 绑定“批准的内容”，不保存内容本身。

候选全局方向：由 agent 宿主提供版本化工程状态 owner，使用不可变 revision/event、事务 head 更新、compare-and-swap、历史恢复为新 revision，并把现有 Markdown/JSON 作为可恢复视图；批准绑定不可变 revision；宿主通过只读工作区/专用 writer 控制绕过路径。Skill、脚本、watcher 或 Git hook 不能在 unrestricted shell 下承诺禁止直接覆盖。无 Git 项目也须能恢复。现有项目采取显式预览迁移，当前字节成为迁移起点，已丢历史不伪造。

候选核心验证：完整错误覆盖仍可恢复、崩溃各保存阶段只留下完整revision、并发写冲突可见、旧版本恢复不转移批准、非Git项目可用、直接绕过在宿主边界真实拒绝（否则标 unsupported）、旧项目迁移逐字保留起始内容。详见Spec与Plan。

## 当前 Skill 流程影响 / 候选结论

- 不改变既有 Baseline → Spec → Plan → Task → Evidence 顺序、需求/模块审核/方案批准/实施授权的意义，也不新增“每次保存/每个问题都要审核”的轮次。
- 保存系统 revision 与 Spec/Plan/审批语义 revision 分开；存档或恢复本身不表示用户同意，不转移旧批准。
- 旧项目未迁移前继续使用原 Markdown/JSON、manifest、stage 例外和声明检查；迁移需显式预览和启用，不自动 strict 化、不新增必需检查。
- 迁移并启用 writer 的项目会改变编辑方法；并发冲突需显式处理。若宿主权限无法阻止绕过写入，则能力只能标为检测/恢复或 unsupported，不能说流程受到强制保护。
- 上述是候选设计影响，未在当前宿主验证；宿主权限与旧项目迁移机制是方案批准前的技术调查项。

## 实施进度 / 2026-10-22

- `scripts/task_archive.py` 提供本地 SQLite 归档；必须显式指定工作区外的 `--store` 和稳定 `--project-id`。`init` 快照当前 manifest 声明的文件；`check` 检测视图与保存 head 的漂移；`check --save --expected-head REV` 由调用者确认当前工作区修改后，创建带父 revision 的检查点；`history` 列版本；`restore REV` 先确认工作区等于 head、再记录 restore revision，并原子重建各文件。
- 6项真实子进程 CLI 回归通过：初始快照、整篇误覆盖检测、历史保存、旧版本恢复为新 revision、旧/未知 revision 拒绝、未保存改动时拒绝恢复、过期 CAS 拒绝，以及 SQLite 中断式 insert-abort 后事务回滚保持旧 head。工具不改 Git index/worktree 状态。
- 当前实现保护的是“可检测与可恢复”，不是宿主级强制写权限；shell/editor 直接写入仍可发生。SQLite 事务对归档版本/ head 保证原子；若恢复投影过程中崩溃，archive head 先记 restore intent，工作区可能处于 partial，须运行 `restore --project-head` 重建。
- 用户于 2026-10-22 明确授权：“那就按照这样进行更改,只要原有流程不变就可以,1.8的流程已经很不错了”。范围为新增可选本地记录恢复能力、更新指导/合同和 linked artifacts；不改变原流程阶段、审批、命令、超时、strict/default 或 commit gate。不自动迁移外部项目、不配置 OS 权限、不启用远端同步、不提交或发布。

## 影响范围与发布

- 候选模块：宿主文件/状态写入权限边界、instructions、checker、adoption/governance。当前仓库没有宿主级 write sandbox、通用状态 store 或文档 writer；宿主 API、存储、权限、保留和重装行为尚未调查。
- 存储：候选需要双故障域副本；位置、加密、留存、清除与跨设备同步均待宿主调查。无业务数据库影响；不能预设新增SQLite即解决问题。
- 兼容：1.8.0已发布源范围与原批准保持；候选应兼容项目自有Markdown/JSON及无Git项目，迁移需显式。审批与测试原合同保留。
- 验证：本地 CLI 6项行为回归通过；任务隔离 venv 使用锁定 tree-sitter==0.25.2 / tree-sitter-rust==0.24.2 后，原始 TEST 命令完整运行 231 项并通过（133.853s 诊断环境）。正式 change/commit gate 原命令/120s 不变：TEST 在 120.011s（commit rerun with task Python 3.11-unavailable fallback）及 120.000s（task Python 3.12.14）超时；COMPILE/GUIDANCE-COMPILE 均通过，task-gate/control-plane 亦通过，因此 required_checks_satisfied=false。隔离诊断环境 231 项 133.853s 不能替代正式 TEST；未提高超时、缩减测试或提交/推送。Skill quick_validate 在 PYTHONUTF8=1 下通过。宿主 write sandbox 不可用，RI-06 hard enforcement 保持 unsupported。
- 发布：兼容的新可选本地能力按 MINOR 候选 `1.9.0 / Unreleased`；五处元数据适用性与 Release Impact 待同步核验。当前无 commit/push/Release；正式 TEST 超时，故未创建 commit 或推送 GitHub。

## 下一步

宿主级写入强制隔离因能力缺失保持 unsupported；本地 archive 为可选使用。原 1.8 工作流审核语义保持。
