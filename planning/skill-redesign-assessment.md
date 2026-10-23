# Engineering Workflow Skill 改造需求评估

状态：历史评估记录。该文档在实施前描述为 `assessment / implementation_not_authorized`；后续用户于 2026-10-23 审核方案并授权实施，当前状态见 `planning/skill-redesign-task.md` 与 `engineering-manifest.json`。

## 来源与范围

- 来源：用户提供的需求附件（原始附件位置为本机私有路径，不作为仓库发布内容）。
- 需求主题：改造 `engineering-workflow` skill，使基线分为派生事实、判断、状态三层；把完整性门槛改为代码与基线的 delta 纠偏；增加稳定锚点、任务规模分级、技术依赖与顺序依赖拆分，并降低临时文件、手工 inventory 和同步仪式造成的阻塞。
- 明确保留：Baseline / Spec / Plan / Task 纠偏链、必要护栏、业务正确性与程序检查的区分。
- 当时未授权范围：修改本仓库代码、修改 checker/模板/manifest 规则、迁移外部项目、把旧 Issue24 的批准扩展到新需求。后续实施及发布授权见当前 Task。

## 当前基线

- 工作树基点：评估开始前无未提交改动；评估记录最初是唯一新增文件。形成审阅方案后，当前两份新增未跟踪文件为本评估和 `planning/skill-redesign-plan.md`；未改动实现文件。记录时 HEAD 为 `6de2cbbc90b53a23a401a395780e9e676d51012d`（2026-10-23）。
- 当前 manifest 活动任务：`TASK-ISSUE24-EFFICIENCY-01`。其批准只覆盖旧的可选 `workflow_state.py` 目录/快照/批量更新工具、Windows 路径修复和已记录的 TEST 超时政策，不覆盖本附件提出的 workflow 语义改造。
- 当前已有 `scripts/workflow_state.py`：提供 `index`、`snapshot`、`apply-batch`，可从 manifest 重建导航视图，按 hash/锚点做批量更新并保留未知生命周期状态。它是旧 Issue24 的实现，不是本附件要求的派生事实生成器或 delta gate。
- 当前已有 `scripts/check_project.py`：校验 manifest 引用、模块路径、任务依赖、inventory、审批记录、实现范围、文档影响和声明的 required checks；输出 `pass/fail/partial/unsupported` 及部分 gaps。

## 已验证证据

| 检查 | 结果 | 含义 / 限制 |
| --- | --- | --- |
| `python -m unittest scripts.tests.test_workflow_state -q` | 30 pass | 旧状态工具的 focused 行为通过。 |
| `python -m unittest scripts.tests.test_checker -q` | 30 pass | checker 核心 fixture 通过。 |
| `python -m unittest discover -s scripts/tests -q` | 246 tests，2 errors | `test_checker_lifecycle` 的 Windows 进程族回归在本次运行中出现 pidfile 尚未完成写入；JS/TS 关系测试报告 pinned TypeScript runtime 不可用。该结果不能证明全量回归通过。 |
| 现有 baseline checker（唯一新报告路径） | 结构性检查通过；required `TEST` fail，`COMPILE`/`GUIDANCE-COMPILE` pass | TEST 约 148 秒返回 1，原因对应上述两个环境/回归错误；报告未被解释为新需求的失败。 |
| `git status --short --branch` | clean | 本评估前没有代码或文档改动。 |

## 附件需求与当前实现的差异

### 1. 基线三层

- **已有**：手写的 Baseline、模块图、数据库字典、契约和业务流；SQLite/MySQL/PostgreSQL/Redis 元数据提取器；可选 source-context 静态关系图。
- **缺口**：没有统一的“从代码生成派生事实”契约；没有声明哪些文件是生成物、生成命令、输入范围、源 hash、生成版本和失败/不支持边界；当前 `docs/module-map.md`、`docs/database.md`、`docs/contracts.md` 仍可手写。
- **影响**：不能承诺“改代码即在同一批次自动重生成”，也不能安全地禁止手写第一层。语言、框架、路由、ORM、模块注册方式各异，需要先定义适配器与覆盖边界。

### 2. Delta 门槛

- **已有**：`change_check` 按路径覆盖和 `documentation_impact` 报告文档缺口；inventory 会比较源清单与映射字段。
- **缺口**：checker 没有“代码事实 A、基线事实 B、需要补 X”的统一 delta 模型；不能把自动可修、需要语义判断、真正硬阻塞分开；`manual` inventory 明确保持 `partial`，并会在必需时阻塞。
- **影响**：需要重新定义报告结构和 required 判定，且必须证明安全项（密钥入库、必测未跑、越权）仍是硬阻塞，其他缺口只进入待补证据清单。

### 3. 稳定锚点

- **已有**：manifest 文档、模块、需求、验收和任务 ID；`workflow_state` 支持按文档 ID/Markdown 标题读取。
- **缺口**：表、字段、路由、接口和模块上下游没有统一稳定 ID 与切片索引；现有 ID 主要服务于治理记录，不能一次读取代码派生的具体事实。

### 4. Spec / Plan / Task 同步

- **已有**：三者分开保存并通过 manifest/artifact links 关联；`workflow_state.apply-batch` 可做精确多文件机械更新。
- **缺口**：没有共享变更入口、三视图自动一致的语义模型；日常变更仍可能要求多处人工改写和 revision 指针同步。现有 batch 工具只保证机械 JSON/区段更新，不判断三个工件的业务语义一致性。

### 5. 任务规模与门禁分级

- **已有**：所有任务使用相同的字段校验和 required checks；实现授权由全局 `workflow.stage` 与所选 task 的 `implementation_authorization` 共同控制。
- **缺口**：manifest/task 没有 `scale`；门禁没有 `applies_to`；调查任务在进入 implementation/verification 阶段时可能被全局实现授权语义影响；没有按 `hotfix / minor / feature / takeover` 减少无关门槛的规则。

### 6. 依赖语义

- **已有**：`task.depends_on` 不完整时在 `change/handoff/commit/committed` 的 task gate 中阻塞；模块依赖还会做允许边界和环检测。
- **缺口**：没有 `after` 或“只影响完成、不影响开工”的顺序语义；资料整理类父任务可以阻塞编码子任务。

### 7. checker 治理与变更范围

- **已有**：受保护控制面路径、外部批准环境变量和 commit/committed 模式；`staged_git_paths` 只读暂存区，change 模式的 `git_paths` 仍包含 untracked。
- **缺口**：没有独立、只读挂载 checker 的机制；“禁止就地改 checker”目前只有流程/控制面约束，没有可验证的发布边界。change-scope 也没有按附件要求默认忽略临时/备份 untracked 文件的策略。

### 8. 成本自查

- **已有**：旧 Issue24 有候选效率 pilot 记录，但未完成真实配对测量。
- **缺口**：没有任务结束时统计实际产出、命令/轮次、重复读写和失败重试的工具或报告字段；不能把旧会话估算当作普遍效率收益。

## 需求中需要在新 Spec/Plan 明确的技术边界

1. 派生事实的首批适配范围：仅 SQLite/数据库元数据，还是同时覆盖路由、请求/响应类型和模块依赖；没有通用 extractor 时哪些视图保持 `unsupported`。
2. 生成物写入方式：仓库存储生成 JSON/Markdown，还是只在检查/读取时生成；是否允许人工修改生成物，如何检测漂移。
3. delta 的报告合同：代码事实、基线事实、证据路径、自动修复动作、需要判断的结论、阻塞级别和待补证据字段。
4. `task.scale` 的默认值、迁移兼容和每个 gate 的 `applies_to`；旧 manifest 是否继续按 legacy 规则运行。
5. `depends_on` 与 `after` 的完成/开工语义，以及如何处理未知依赖、环和跨任务文档依赖。
6. change-scope 的 staged/untracked 政策是否只影响新 manifest，还是要改变当前仓库的既有门禁；临时/备份文件的可验证识别规则。
7. checker 独立发布/只读挂载如何在本仓库可验证；若宿主无法提供，只能记录为 unsupported，不能伪造解决。
8. 成本自查是诊断报告还是 required gate；如何避免为统计本身增加新的同步仪式。

## 当前判断

这不是旧 `workflow_state` 的补丁，而是对 skill、checker、manifest schema、模板、文档和测试的跨层改造。附件的验收标准 1、3、4、5、6、7 可以形成可测试的工具/规则合同；标准 2（典型 feature 工具调用数下降一半以上）必须通过匿名化配对 pilot 测量，不能由单元测试或静态检查宣称达成。

本附件是独立新需求。完整方案已审核并于 2026-10-23 授权开始实施。本地首批改造已完成，当前实现与验证状态以新任务 TASK-SKILL-REDESIGN-01、Spec/Plan 和 manifest 活动指针为准。本需求不沿用 Issue24 批准，不含外部项目迁移或远程发布。

2026-10-24：用户另外授权更新文档并上传本仓库；该决定与上文记录的初始“本轮不含发布”范围不同，当前有效状态以 TASK-SKILL-REDESIGN-01 与 manifest 为准。新 CI follow-up 的 Ubuntu 诊断失败源于 skipUnless 测试注册造成 partial TEST；条件注册后本地 TEST 286 与 baseline 通过。

## 下一步

2026-10-23 已根据该评估和用户附件形成 [完整改造方案审阅稿](skill-redesign-plan.md)；用户随后审核了方案方向并补充了上下文复用与实施中纠偏原则。方案自检已完成，后续用户批准已触发本仓库本地实施。新 Spec/Plan/Task 和活动指针已建立；首批代码与指导改造完成，原 required checks 与 validator 通过，当前报告见 [TASK-SKILL-REDESIGN-01](skill-redesign-task.md) 和固定 current 报告。未完成项是效率配对 pilot（缺可信日志）与 route/permission adapters（本批明确 unsupported）。不把授权扩展到 Issue24 旧范围或外部项目迁移。
