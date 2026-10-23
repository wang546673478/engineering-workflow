# PLAN-SKILL-REDESIGN-01：分批实施与验证

状态：已由用户审核完整方案并授权实施；当前按 B0–B5 执行。依据 [SPEC-SKILL-REDESIGN-01](skill-redesign-spec.md)、用户审核的 [完整方案](skill-redesign-plan.md) 和当前 [基线审查](baseline-review.md)。本 Plan 是实现路径，可随代码/测试证据调整，但不得改变 Spec 的目标、硬边界或验收。

## 实现边界和当前基线

- 源码基点：任务启动时工作树 `HEAD` 与当前未提交改动另记在 Task；保留既有 Issue #24 工作树内容，不替换或回滚。
- 首批派生查询仅交付能够由现有本地 adapter 与 fixture 可靠验证的 SQLite/SQL 元数据和静态依赖视图。固定 Gin 路由源码回执可在 receipt/source hashes 有效时查询静态字段/记录的权限说明；动态路由、handler runtime 和生产授权仍 unsupported。无 request/response receipt adapter 时不宣称其受支持。
- 动态“同批可见”落实为：相关源变化后，在下一次依赖该切片前执行按需 query，核验来源指纹并重算；不承诺后台 watcher，不要求 Agent 每个微操作重复读取。
- 继续遵守当前 manifest 中 required `TEST`、`COMPILE`、`GUIDANCE-COMPILE` 的原命令、覆盖和 timeout；本任务不改门槛以求通过。
- 本仓库 checker 可自改，但每次控制面改动需先通过原保护及独立回归；不得以待修改版使自身变绿。

## B0–B5 执行项

| 批次 | 实施内容 | 主要验证 | 状态 |
| --- | --- | --- | --- |
| B0 | 登记新需求 Spec/Plan/Task、影响、skill review、追踪和独立用户授权；冻结兼容和 finding 合同 | Manifest 自检及原 checker；保留 Issue24 历史授权原样 | complete |
| B1 | 在现有 `workflow_state.py` 中增加受支持 adapter 的只读按需切片查询、稳定 ID、来源指纹和覆盖声明 | SQLite/source fixture，变化后 query 刷新、无变化复用、unsupported 边界 | complete：SQLite table/field、manifest module 和可选 source-context relation query 已接入；adapter partial/unsupported 明示 |
| B2 | 将 checker 差异收敛为结构化 actionable findings；修复 manual inventory 可达路径，不添加结果状态 | checker 回归、required inventory 通过与差异 fixture | complete：manual pass 必须有可定位 evidence/scope，mapping 与所列条目匹配；path/inventory actionable finding 已验证 |
| B3 | 按 Task 实际规模和动作实现适用门槛；拆解技术 depends_on 与非阻塞 after；临时项显式报告并与 blocking scope 分开；保留 commit staged scope | scale/gate/依赖/scope 回归，保留安全与 required checks | complete：policy_version/scale、applies_to、after、artifact_path depends_on、read-only Task 授权和临时路径识别已通过聚焦/完整 checker regression；commit scope 继续只看 staged |
| B4 | 实现单一 change set 精确分发、唯一权威视图、冲突拒绝与必要引用；同步 skill/reference/模板/README/追踪与版本记录 | 批处理 dry-run/apply、hash conflict、approval 不可提升、旧 manifest fixture | complete：section operation 要求 task_id/authority 并校验精确链接；文档、模板、manifest、版本元数据已同步 |
| B5 | 跑完整原门槛、skill validator、场景验收和适用平台测试；检查准确支持范围与交付基线 | 完整 TEST 280/156.219s，COMPILE/GUIDANCE-COMPILE 和 quick_validate 通过；baseline current 报告 required_checks_satisfied=true；效率 pilot 无可信配对日志故 unverified；staged/commit gates 未运行，因为本地未暂存 | complete for local verification |

## 语义实施规则

- Baseline 负责当前代码/行为事实；Spec 是需求正文唯一权威；Plan 是技术路径唯一权威；Task 是进度/阻塞/下一步唯一权威。Baseline 可维护到这些视图的索引/链接，不复制任务状态正文。
- hotfix/minor 不要求重建全局基线，但证实受影响切片事实错误时仍须即时纠正；完整 Baseline 表示声明范围每个适用视图均有来源、状态、边界、影响说明，允许明确 unsupported/unknown，不等于全支持。
- 代码描述事实可由 Agent 依据证据修正；新业务规则、权限选择、用户目标或验收改变按现有决策/Spec 审核规则确认。测试失败允许在授权范围继续诊断修复；阻止依赖该验证结果的提交/交付。
- `baseline.fact_correction` 包括派生事实重算和判断层已确认描述错误的更正；它不得更改 Spec 的需求目标。
- 单一 change set 是机械写入入口，不增加用户审核点；只更新操作实际影响的唯一权威和必要引用。单视图变化也经此入口但不改无关文档。
- 报告固定键为 task/session/mode；同槽 current 覆盖，跨会话历史文件不自动删除，只清理由本次运行创建的临时文件。
- `task.scale`、`policy_version`、`applies_to` 和依赖字段必须各自回答触发时纠正何种偏差：scale 防止小任务走无关全局门槛；policy_version 明确新旧解释以免兼容规则猜测；applies_to 防止不适用 gate 阻塞；depends_on/after 防止资料顺序被误判为技术前置。

## 当前影响范围

预计改动 `SKILL.md`、`scripts/check_project.py`、`scripts/workflow_state.py`、相关测试、checker/baseline/implementation references、manifest 与模板、README、基线/模块图/契约/业务流、traceability/change-impact、VERSION、CHANGELOG。准确文件按证据确认并持续更新 Task。无外部项目迁移、产品 API 或业务数据库变更。

## 不确定与延后

- route/OpenAPI/request-response adapters 是否及何时加入：依现有依赖、覆盖和成本调查结论决定；没有实现前不计相关验收为通过。
- 宿主是否提供受信任的工具调用日志、文件只读挂载或 report lifecycle API：目前不假设存在；无法验证时标 unsupported/unverified。
- 真实 feature 工具调用下降 ≥50%：仅有同类配对样本与完整日志才可测；没有就保持未验证。
