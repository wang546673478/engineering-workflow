# TASK-SKILL-REDESIGN-01：动态基线与工作流纠偏实施

## 当前状态

- 阶段：implementation / final local baseline passes TEST 285, COMPILE, and GUIDANCE-COMPILE; focused workflow_state suite passes 42. Skill validator passes with isolated PyYAML 6.0.3. Staged tree f24a3b3eb709928536f781313def8e8d9cc92204 retains feature scale and all documentation_impact groups. Exact-commit gate cannot proceed because this batch changes protected manifest/checker files and needs the external approval signal required by the repository. Prior remote commit 7612033 is on the feature branch, not main; its hosted Windows job failed with generic annotations and inaccessible artifact. No new push or merge has occurred.
- 当前工件链：[Baseline](baseline-review.md) → [Spec](skill-redesign-spec.md) → [Plan](skill-redesign-implementation-plan.md) → 本 Task → 代码/测试证据。manifest active pointers now select this task, Spec and Plan; Issue #24 remains unchanged.
- 实施基点：工作树包含此前本任务方案/评估两个未跟踪文件，以及原有 Issue #24 在途工作；动手前尚未修改代码。本 Task 记录开始后的 git 基点和差异。
- 决策：首批以可验证 SQL 元数据和静态依赖按需切片为主；route/契约/权限能力按现有适配器证据决定，不支持的视图明确标示。
- 保持门槛：TEST、COMPILE、GUIDANCE-COMPILE 命令/覆盖/timeout 原样。

## Skill review

检查时间：2026-10-23 Asia/Shanghai。来源：当前会话 Skills catalog、仓库 `SKILL.md` 和适用 references。

| Skill | 来源/版本 | 决定 | 理由 |
| --- | --- | --- | --- |
| engineering-workflow | 本仓库 `SKILL.md`；版本 1.10.0 | adopted | 本需求明确改造对象；按本仓库当前任务链、基线与检查规则执行 |
| skill-creator | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`；可见版本未提供 | adopted | 收敛 skill 主入口与 references，并运行 validator 和行为验证 |
| tdd | `C:/Users/54667/.agents/skills/tdd/SKILL.md`；可见版本未提供 | adopted for checker/tool behavior | checker 与 query 工具存在明确可观测合同，使用针对行为的回归验证 |
| planning-with-files | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`；可见版本未提供 | not-adopted | 本项目已有权威 Spec/Plan/Task/manifest 体系，不建第二套记录 |

范围变化或 adapter 技术方案显著变化时重新做 skill review。

## 需求/验收进度

| ID | 内容 | 状态 |
| --- | --- | --- |
| SR-01 | 动态全局基线与三层权威 | complete for first batch; stable-ID facts query supported SQLite/module/source-reference boundaries |
| SR-02 | 上下文复用和按需新鲜度纠偏 | complete for first batch; every query recomputes current source fingerprints and exposes freshness limits |
| SR-03 | 实施中修正 Baseline，不改写 Spec 目标 | complete as workflow guidance; downstream projects will exercise the rule with their real evidence during implementation |
| SR-04 | 单一 change set 与唯一权威视图 | complete for first batch; section writes require Task, exact authority and linked artifact; mismatch regression passes |
| SR-05 | 稳定 ID / 精确事实查询 | complete for first batch; SQLite table/field, declared module and optional source relation IDs supported with explicit limits |
| SR-06 | Actionable delta 与少数硬阻塞 | complete for first batch; actionable path/inventory findings and manual pass boundary tests pass |
| SR-07 | 规模、适用门槛、依赖和变更范围 | complete for first batch; after, scale/applies_to, artifact path, read-only lifecycle and temporary scope tests pass; commit scope remains staged-only |
| SR-08 | required 可达、旧 manifest 兼容、checker 治理 | complete for first batch; legacy manifests keep inferred scale/old dependencies; manual inventory pass requires real evidence path and listed mapping |
| SR-09 | Greenfield partial/complete 事实基线 | complete as guidance; existing greenfield lifecycle is retained and clarified, no external project is migrated |
| AT-SR-01..10 | Spec 所有验证与交付验收 | implementation regression, original checks and synthetic schema/change-set pilot pass (6 CLI invocations); read-only real-session inventory query pass (4 tables, 2 fixed routes); legacy paired efficiency percentage remains unverified |

## Batches

| Batch | 状态 | 记录 |
| --- | --- | --- |
| B0 | complete | 创建新 Spec/Plan/Task、批准证据、manifest 活动指针、影响和 traceability；Issue24 记录保持独立 |
| B1 | complete for first batch | SQLite table/field and declared module queries; optional bounded JS/TS/Rust source references via query --relations; workflow_state tests 35 pass; no-source modules return unsupported |
| B2 | complete | manual inventory locatable-boundary pass/fail and actionable finding tests pass; checker suite 129 pass; final full suite 280 pass | 结构化 delta、manual inventory pass reachability |
| B3 | complete for first batch | policy_version/scale/applies_to, nonblocking after, structured artifact dependency, read-only Task lifecycle, temporary handling and legacy compatibility covered; staged commit scope policy unchanged |
| B4 | complete | apply-batch authority routing and guidance/template/docs/version synchronization; focused changeset and skill validator pass |
| B5 | local checks pass; hosted Windows follow-up open | Prior query/receipt regressions were corrected. Current local full TEST 285, COMPILE, GUIDANCE-COMPILE and focused workflow_state 42 all pass. GitHub run 40008142044 for commit 7612033 failed in reviewed Windows; detailed logs are unavailable. A narrow extended-path normalization fix and Windows-only regression test are prepared. Retain feature scale and all original documentation gates. |

## 影响分析

- Modules：instructions、checker、workflow-state、adapters/source-context、tests、governance。
- API/DB：没有产品 API 或业务数据库影响；工具合同影响在 Plan/spec 中定义。
- 文档：SKILL、checker/reference/baseline/implementation guidance、manifest/template、README、module-map、contracts、business-flow、baseline-review、traceability/change-impact、新 Spec/Plan/Task、VERSION/CHANGELOG。
- 门禁：本任务不修改 required 命令、测试覆盖、timeout 或控制面审批约束。
- 风险：checker 自身变化必须保留旧行为回归与控制面路径；unsupported adapter 不得伪装完整；多文件 change-set 只能在冲突前全部拒绝或给出可恢复行为。

## 进度与下一步

1. complete：登记 Spec/Plan/Task 与活动指针；Issue24 approval unchanged.
2. complete：确认 SQLite main schema extractor 支持 checkpointed DB；静态 JS/TS/Rust source-context adapter 已接入 query 的可选 `--relations`，结果保留 partial/unsupported 与证据限制；checker 原行为基线已复核。
3. B1-B4 首批能力与权威 guidance/模板已更新；synthetic schema round-trip pilot pass。route/permission adapters 不在首批支持范围；真实效率配对指标仍 unverified。发现事实冲突先修 Baseline/Plan/Task。
4. 历史验证：280 项 TEST 曾通过；2026-10-24 一次中间全量运行中 283 项有 4 项失败，修正后本地 283 项通过。GitHub Actions 对精确提交 7612033 的 Windows reviewed job 失败，见 run 40008142044；公开注释只显示通用退出码，日志 artifact 无法下载，故具体失败项未知。
5. 最新验证：独立全量 `python -m unittest discover -s scripts/tests -q` 于 2026-10-24 通过，285 项 / 159.116s；`workflow_state` 聚焦套件 42 项通过，COMPILE 与 GUIDANCE-COMPILE 通过。更新后的 baseline checker 报告 `work/TASK-SKILL-REDESIGN-01-baseline-windows-fix.json` 也通过，包含 TEST 285、COMPILE、GUIDANCE-COMPILE。当前扩展路径 follow-up 还需以未降级的 feature documentation_impact 通过 staged/exact-commit，再由 GitHub Windows CI 验证。
6. 2026-10-24 用户授权更新相关文档并上传本仓库。README 与[去标识试点报告](real-session-efficiency-pilot.md)已准备。本地 required 与 exact-commit 检查通过；GitHub Actions 在 reviewed Windows job 失败，运行 `40008142044`，页面注释只有进程退出码，artifact 下载不可用。新发现的 extended-path 根路径差异需要通过 Windows-only regression 和完整 TEST/commit/committed 检查验证。发布仍需保留 `feature` 规模和原有 documentation_impact，当前分支未合并 main。整体效率比例仍未验证。
