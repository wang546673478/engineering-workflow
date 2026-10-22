# ISSUE24-ASSESSMENT-01：需求访谈记录效率与工具替换的全局评估

状态（历史）：Issue #24 全局诊断完成并形成候选方案时，本 assessment 只授权评估，不含实现。用户随后另行批准 SPEC/PLAN r1 的实施；当前授权与实现状态以 [TASK-ISSUE24-EFFICIENCY-01](issue-24-efficiency-task.md) 为准。

来源：GitHub Issue #24（链接见本 Task 记录）；目标会话“梳理当前用户体系”（会话 ID 01a15d44-a667-7952-89da-04ff9179fd6d），工作区 E:\liantongzhongzhuanzhan。会话目前仍 active，Spec 1.3-draft 尚待模块完整性审核，未授权产品实施。

## 调查结果与证据范围

截至 2026-10-22 本次只读快照，会话约 35 个 turn、1,595 个 shell 命令调用，其中约 1,287 条读取/搜索类与 127 条写入类。数字随活动会话继续变化；可读快照实际累计值到约1,595条命令，会话后续仍继续增长。平台日志没有逐调用耗时，故 Issue 的“700+/小时”“约2/3时间在文档”本轮不可独立验证。

活动 Spec 收敛轮快照约 495 条 shell 调用：396 条读取、121 条搜索、10 条写入类。反复检查 enterprise-sales-requirements、core-review-task、pricing Spec/Plan 摘要及 manifest，最后这些权威文件有 fileChange 事件。大量失败 shell 返回“Failed to create unified exec process: 目录名称无效”；不少命令随后以相同工作目录重试。这属于宿主 workspace/command 启动问题，Skill 内更换文本编辑工具不能修复。

成本至少来自四个不同因素：重复读取/搜索；多文件同步及机械验证；写入锚点不匹配或非幂等操作造成返工；宿主工作目录错误导致命令根本没启动。Issue 提出的“70%时间在文档”和“5–10倍写入放大”来自单次审计估算，现有快照不含真实墙钟耗时或统一分类，不能当成本轮测量事实。

## 推荐方向：结构化批量状态接口，不只是换编辑器

建议采用两个衔接部件：**状态目录索引**帮助定位权威目录/文件及其状态；可选 `workflow_state` 读写接口帮助批量读写这些文件。它直接操作 manifest 声明的 Task、Spec、Plan 和决定记录，继续让原工件作为唯一权威源，不建立第二套业务状态库。目录索引回答“在哪里、职责是什么、当前状态/版本是什么”，不复制长段需求正文或形成另一份含义不清的当前状态。

索引字段建议如下：

| 字段 | 用途 | 来源与更新规则 |
| --- | --- | --- |
| `document_id` | 稳定标识 | 直接对应 `manifest.documents.id` |
| `path` | 精确路径/链接 | 直接对应项目相对路径 `manifest.documents.path` |
| `kind` / owner | 文档职责与维护方 | `manifest.kind` 和项目规则，不复制正文 |
| `state` | `current`、`draft`、`approved`、`historical`、`superseded`、`unverified` | 从 active pointers、Task workflow 状态及正文 revision 用显式规则映射；事实冲突时标 `conflict`，不能凭印象选择 |
| `revision` / `based_on` | 当前内容和依据版本 | 从 active revisions 与 Spec/Plan/Task 头部读取；不一致则提示冲突 |
| `last_changed` / `sha256` | 缓存新鲜度与外部改动检测 | 文件事实元数据；hash 不能表示语义已审核或批准 |
| `related_documents` | 一次加载上下游文档 | 由 `artifact_links` / manifest 映射生成，不重复存长正文 |
| `review_status` / `implementation_status` | 分开显示是否已确认与是否已实施 | 从 Task 对应字段读取，禁止互相推断 |

索引必须是可以随时由 manifest + Task 重建的导航视图，而不是新的权威台账。可先由 CLI `index` 子命令输出 JSON/表格；仅当用户确实需要持久导航页时再物化 Markdown 视图，避免新增一个需要人工同步的副本。

1. **read snapshot**：一次返回 active Task、当前 Spec/Plan 摘要、待决项及按请求指定的章节；每个文件附内容摘要和 revision。内容未变时可在同轮复用快照；摘要变化后刷新，不能复用陈旧内容。
2. **apply batch**：一个 JSON 请求携带 operation ID、预期 manifest/文件摘要及精确的 document/section/key 操作；一次更新已确认需要同步的多个文件。按 manifest 对象 ID 更新结构化 JSON，按唯一标题/具名区块或明确范围更新 Markdown，按事件 ID 幂等追加决定/进度。相同 operation 重放不产生第二次修改。
3. 写之前核对全部目标、唯一锚点、前置摘要、需求/验收 ID 和 manifest 引用；任一冲突就整批拒绝，返回一次完整 diff 与冲突原因。不允许静默跳过锚点再换全局字符串替换。工具不判断正文是否业务正确、用户是否批准。
4. 一次批量更新只生成一个机械保存 revision，记录父 revision、affected paths、旧/新摘要和来源；它不增加 Task 语义版本、Spec 冻结或用户审核轮次。沿用现有 task_archive 作为可选恢复库，先原子登记 snapshot，再提交文件视图；失败保留旧 head 并允许恢复。
5. 一次返回机读验证报告：实际读取/写入路径、diff、revision、幂等重放状态、JSON/manifest/引用校验、未完成检查和限制。Agent 只需读回受影响章节，而不是每次重读同一文件开头。

已有 1.8 流程保持：一问一答、持续需求记录、事实/候选/确认/延后区分、模块完整性审核、完整 Plan 批准、实施授权、required checks 和 strict/diagnostic 语义不变。批量只是减少机械文件操作，不合并产品审核，也不把用户答复提升为批准。外部项目显式采用，不能自动迁移或转移旧批准。

宿主错误必须独立处理：当 cwd 无效时，writer 启动前验证 workspace handle；失败后停止在同一错误 cwd 下盲目重试，改用宿主提供的稳定 file API/会话 cwd，或明确阻塞并恢复后再继续。helper subprocess 如果依赖同一失效 cwd，也无法解决这一问题。当前 Codex 宿主的公开工具面未提供沙箱/目录解析配置接口，因此本轮只能确认这一根因并提出宿主侧要求，不能在 Skill 仓库伪装成已修复。

## 与现有 task archive 的关系

1.9.0 `task_archive.py` 只在项目显式运行时保存/检查/恢复 revision；不会自动跑，不减少搜索/读取调用，也不做多文档智能同步。批量接口可复用其快照/恢复能力，但不是 archive 现有功能。不要宣称 Issue #24 已由 1.9.0 解决。

## 建议验证

用同一代表性需求变更做旧方式和候选方式配对试验，记录成功调用数、读/写数、重复路径、写入失败、宿主启动失败/重试和实耗时间；确认输出文档、原审核节点、manifest 引用及必需检查完全一致。测试覆盖多文件单批更新、幂等重放、前置摘要过期整批拒绝、坏 JSON/缺失锚点不写入、事务中断保留旧版本、恢复为新 revision、旧项目未迁移时原行为不变。

这只是 candidate Plan 的验证设计，不宣称已取得效率提升。还需宿主定位“正确工作区却 cwd 无效”的触发条件。任何工具计数只按完整会话快照复核，不从单次会话外推总体效率。

## 与 Issue24 原建议的关系及结论

Windows CI follow-up (2026-10-23): Actions run 39802741018 exposed a POSIX skip-summary interaction after the Windows-only alias regression tests were added. The required TEST became partial because unittest reported those host-specific cases as skipped. The tests are now registered only on Windows; this validation correction does not measure or claim an efficiency improvement. The paired efficiency pilot remains unmeasured.

- 导航索引可减少“文件在哪里”的搜索，但应由 CLI 从 manifest/active task 生成；手写第二份索引会增加另一份需同步状态。索引只保存 document ID、路径、状态/版本、owner 和上下游关联，不复制整段 Spec/Task 正文。
- 批量状态接口能把一次已确认答复需要的若干确定更新压成一次可审核操作。单纯把 PowerShell 换为 Python，而不提供单次读取快照、明确目标、幂等 operation ID 和批次校验，无法系统性减少重复搜索/返工。
- 不建议当前把历史全部搬到 JSONL 或把 Task 缩成“当前状态+下一问”；那会改变现有权威记录方式和迁移边界。先用索引/摘要改善导航与读取，再经配对试点证明收益后评估格式演化。
- `task_archive.py`只提供可选快照/恢复；batch reader/writer 是独立职责，可复用其快照能力，不能说1.9.0已解决Issue24。
- 候选优先级：先确认/修复宿主失效cwd与失败重试的调用契约；再试点从现有manifest生成索引和原子apply-batch；最后用真实配对会话衡量调用数、重复读写、失败率和时间。所有产品审核节点/批准语义继续由1.8流程控制。

Implementation handoff (2026-10-22): the assessment-time candidate scope has been superseded by the separately approved [SPEC](issue-24-efficiency-spec.md) / [PLAN](issue-24-efficiency-plan.md) / [Task](issue-24-efficiency-task.md). Its original `not authorized` status describes the research boundary when assessed; the current implementation authorization and impact are owned by `TASK-ISSUE24-EFFICIENCY-01`. No session data in the external project is included in this implementation.

## Follow-up evidence: Windows Actions path alias (2026-10-23)

The first Issue #24 publication triggered Actions run `39787233509`: Ubuntu reviewed passed in 35s; Windows reviewed failed after its TEST command returned 1, with one failure and nine errors in 260 tests. The exact root cause and fix remain implementation evidence, not a new efficiency measurement: Windows temporary paths alternated between long and 8.3 spellings, and the shared checker rejected in-root paths as escapes. The optional tool efficiency pilot remains unmeasured.


Windows CI follow-up (2026-10-23): Actions run `39802741018` showed the Ubuntu reviewed leg failed because its required TEST summary included skipped Windows-only regression cases and was classified `partial`. The Windows reviewed leg was still waiting for protected-environment approval when inspected, so that run does not establish a Windows result. The collection correction is tracked in the active Task; the paired efficiency pilot remains unmeasured.
