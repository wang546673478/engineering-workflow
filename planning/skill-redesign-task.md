# TASK-SKILL-REDESIGN-01：动态基线与工作流纠偏实施

## 当前状态

- 阶段：implementation / delivery validation passed locally; staged and exact-commit publication gates pending. On 2026-10-24, the full required baseline run passed 283 tests, COMPILE and GUIDANCE-COMPILE; this supersedes the earlier same-day 4-failure run as the current verification while retaining it as history below. README summarizes the real-session baseline query pilot, with full scope/measurement limits in [pilot report](real-session-efficiency-pilot.md). User's 2026-10-24 request, “更新readme这样的文档,然后上传github”, extends the prior local-only authorization to update this repository's linked documentation and upload the reviewed delivery batch to its existing GitHub repository. The earlier no-upload scope is retained as historical evidence. Upload remains contingent on staged/exact-commit gates and repository control-plane review; no external project was edited.
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
| B5 | complete | Fresh full suite exposed four regressions: unsupported route queries returned `unknown`; source-derived receipts did not recheck source-file hashes; the GORM fixture omitted the model mapping required by the receipt contract. Fixed route classification and live receipt source hash checking, corrected the fixture, and reran the required baseline and staged commit checks: TEST 283 pass, COMPILE pass, GUIDANCE-COMPILE pass; exact staged commit-scope check passes.

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
4. 历史验证：280 项 TEST 曾通过；2026-10-24 后续 283 项 TEST 曾失败 4 项（unsupported/unknown 预期差异、source-derived receipt 边界）。保留该失败证据，不以它覆盖后续新运行。
5. 最新验证：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --task TASK-SKILL-REDESIGN-01 --run-checks` 于 2026-10-24 通过，`required_checks_satisfied=true`，TEST 283 项通过（173.675s），COMPILE 通过（0.301s），GUIDANCE-COMPILE 通过（0.297s）；报告 `work/TASK-SKILL-REDESIGN-01-baseline-docs.json`。`git diff --check` 与 JSON 解析也通过。
6. 2026-10-24 用户补充交付授权：“更新readme这样的文档,然后上传github”。已更新 README 并建立[真实会话试点报告](real-session-efficiency-pilot.md)；staged `commit` 门禁于同日通过，`verified_tree=0ee94e8ac1166309f9b2b88d632524e957e54414`，提交 SHA 与提交后门禁待记录。当前 efficiency paired percentage 仍 unverified。
