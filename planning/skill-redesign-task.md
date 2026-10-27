# TASK-SKILL-REDESIGN-01：动态基线与工作流纠偏实施

## 当前状态

- 阶段：已完成并发布到 `main`。当前 `main` 为 `4b2a5065037acb9c92e17d72f44a226663b3d145`；GitHub Actions run `40027043521` 在该精确 SHA 上成功，原 feature branch 同 SHA 的 run `40025624097` 也成功。此前 run `40019503239` 的 Ubuntu partial 和“新 CI 待跑”均为历史状态；效率收益仍未验证。
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
| B5 | complete | Conditional Windows-only registration is included in `4b2a506`; exact-SHA GitHub Actions runs 40027043521 (`main`) and 40025624097 (feature branch) both succeeded. Earlier run 40019503239 remains historical failure evidence. |

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
4. Hosted verification：run 40008142044 曾在 Windows 失败；run 40019503239 的 Windows 通过，Ubuntu 的 checker 通过但诊断 assertion 发现 TEST=partial（Windows-only cases 被 skipUnless 报成跳过）。后续改为仅 Windows 条件注册；该修正随 SHA `4b2a5065037acb9c92e17d72f44a226663b3d145` 通过 main run 40027043521 和 feature run 40025624097。
5. 最新本地验证报告 `work/TASK-SKILL-REDESIGN-01-baseline-zero-skip-final2.json` 记录 TEST 286/162.946s、COMPILE 0.309s、GUIDANCE-COMPILE 0.296s；focused workflow_state 42 与 skill validator 通过。托管 run 对当前精确 SHA 的结果以上述 Actions 记录为准。
6. 用户已授权文档更新及本仓库发布，并明确审阅通过受保护变更。Commit de74171 及条件注册修正均已进入 `main`；当前 `4b2a506` 的 main 与 feature hosted run 均成功。此前“跟进尚未 push / main 未更新 / 新 CI pending”的文字是阶段历史，不再代表当前状态。效率收益仍未验证。

## 2026-10-28 交付事实校正

GitHub API 核实 `main` 当前 SHA 为 `4b2a5065037acb9c92e17d72f44a226663b3d145`；该 SHA 的 Actions run 40027043521（main）与 40025624097（codex/dynamic-baseline-workflow）均为 completed/success。旧的 40019503239 Ubuntu partial 保留作历史缺陷证据，不再作为当前待办。原实施与发布授权范围没有扩大；本记录仅校正交付状态。
