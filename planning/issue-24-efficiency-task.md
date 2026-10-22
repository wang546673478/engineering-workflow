# TASK-ISSUE24-EFFICIENCY-01：工程状态目录与批量读写工具

## 当前状态

- 阶段：verification / delivery；Windows Actions 路径别名缺陷已修复并有回归。实现改为仅对含 `~N` 8.3 片段的路径调用 Win32 API 后，最终正式 checker 已通过；complete commit-scope 门禁也通过。精确 committed-tree 门禁待提交后运行；推送待其通过后进行。基点 `d225cb49d25cec51abfcbaca11470ca8b71ff7af`，分支 main。
- 工件链：BASELINE-ISSUE23-02 + Actions run `39787233509` 的平台缺陷证据 → SPEC-ISSUE24-EFFICIENCY-01 r1（timeout 执行政策修订见文内） → PLAN-ISSUE24-EFFICIENCY-01 r1（TEST 240s 用户修订 + Windows follow-up） → 本 Task → work/issue24-windows-path-final4.json。
- 批准：2026-10-22 05:55:38 +08:00 用户说“批准方案”；06:06:57 +08:00 用户说“一次性根据spec/plan/task把engineering workflow 全部改完吧,然后上传github”；首次实施指令 05:50:41 +08:00 为“开始实施吧”。原话与时间取自当前 thread session log。授权本仓库本地实施、运行原有门槛并在提交检查通过后上传；不含 GitHub Release、外部项目/会话改动、OS 权限或 host API 修改。
- 保持边界：原 1.8 stages、审核节点、审批含义/复用、strict/diagnostic 默认、required checks、测试命令与覆盖不变；唯一门槛例外是经用户批准将当前仓库 TEST timeout 从 120 秒改为 240 秒。COMPILE 与 GUIDANCE-COMPILE 仍为 30 秒；新 CLI 可选且不加 required gate。Windows follow-up 只纠正安全路径比较的 alias 规范化，不改这些流程/门槛。

## 实施范围

新增 scripts/workflow_state.py，提供 index、snapshot、apply-batch：

- index 从 manifest/Task 输出 JSON 或 Markdown；列出 manifest 文档、Task 及 planning 下未登记 Markdown。未登记/无证据状态显示 unknown/unverified，不从年龄或非当前推断 obsolete；active 与显式 lifecycle 冲突显示 conflict。approval、Task 状态、requirement 与 implementation 状态分开显示。
- snapshot 按唯一 document ID 读全文或唯一 Markdown 标题章节，返回 source SHA-256、semantic revision 与 active Task/Spec/Plan/deferred 摘要；不保留跨调用缓存。标题扫描忽略 fenced code。
- apply-batch 要求严格 JSON（拒绝重复键）、operation ID、archive head 和每个目标文件 expected hash；默认只输出完整 diff。只准唯一标题正文替换或 manifest document lifecycle JSON Pointer。保护 workflow/approval/stage/task/check/timeout 字段；拒绝 request 文件作为被改目标。
- 写入前检查 archive drift 与 CAS；成功批次作为既有 task_archive 中的一条不可变 revision，并逐文件同目录原子替换。相同 operation ID + request 幂等；陈旧 hash/head 整批拒绝。普通 I/O 错误尝试回滚；多文件不具跨文件原子可见性，强制中断/回滚失败仍可能留下 partial projection，由 archive check/restore --project-head 检出和恢复。
- cwd 进程启动前失败无法由此 CLI 捕获；进程收到无效 root 时一次报告 unsupported。没有声称存在 host file API，也不宣称修复 host cwd 问题。

## Skill review

检查时间 2026-10-22 Asia/Shanghai；来源为当前会话 Skills catalog 与直接读取的 skill 文件。

| Skill | 来源 / 版本 | 决定 | 理由 |
| --- | --- | --- | --- |
| engineering-workflow | 本仓库 SKILL.md；1.9.0 / e1abcac | adopted | 权威工件、影响链、既有门槛与发布规则 |
| tdd | C:/Users/54667/.agents/skills/tdd/SKILL.md；版本未提供；另读 tests.md / interface-design.md | adopted | 逐步验证 public CLI 行为 |
| skill-creator | C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md；版本未提供；另读 references/openai_yaml.md | adopted | 新可选功能保持精简、逐层披露并执行结构验证 |
| openai-docs | 当前会话 catalog；版本未提供 | not adopted for code | 未实现 host API 或 Codex 产品集成 |
| planning-with-files | C:/Users/54667/.agents/skills/planning-with-files/SKILL.md；版本未提供 | not adopted | 复用已有 Baseline/Spec/Plan/Task，不建第二套任务账本 |

## 影响、版本与范围边界

- 模块：instructions、workflow-state、tests、governance；复用 checker 的 safe path/strict JSON、task_archive 的 revision/CAS。无产品 API、应用数据库或迁移。
- 同步：manifest、Baseline、module map、contracts、business flow、impact、Issue24 Spec/Plan/Task/traceability、SKILL、README、checker reference 与版本记录。原 Issue #23 1.9 archive Task 保持其原审批/结果；该文件中早期 Issue24 候选现由本 Task 承接，不作为第二验收源。
- 版本：1.9.0 → 1.10.0 / Unreleased，向后兼容的新可选能力（MINOR）；VERSION、SKILL、README、agents/openai.yaml、CHANGELOG 已同步。无 Release。
- 效率 pilot：未使用活跃的外部中转站会话做修改或测量；生产配对 pilot 未完成，所以实际节省比例保持 unverified。

## 验收状态

| Step | 需求 | 状态 / 证据 |
| --- | --- | --- |
| WFS-01 | E02/E03/E04：索引、历史保留、来源明确 | implemented；manifest/Task index、unknown planning Markdown、显式 lifecycle 与冲突覆盖于 focused tests |
| WFS-02 | E05：批量快照与源 hash | implemented；全文/章节读取、唯一标题、hash 与 active/open summary 覆盖于 focused tests |
| WFS-03 | E06/E07：精确批量更新、一致性、冲突和幂等 | implemented；duplicate JSON/ID/constant、受保护字段、CAS/stale head/hash、重放、archive drift、rollback、BOM/CRLF 覆盖于 focused tests |
| WFS-04 | E08：host cwd 故障边界 | script 能力已界定；host pre-start recovery unsupported |
| WFS-05 | E01/E09/E10：效率与兼容 | 原流程/检查保持；真实 paired efficiency pilot deferred，量化收益 unverified |
| WFS-06 | 文件/基线/版本/正式门槛 | 文档/manifest/版本已同步；checker 正式门槛见下方报告 |
| WFS-07 | 用户要求的 GitHub 上传 | 用户已授权；当前等候本地 commit/committed gates 与 push |

## 用户批准的验证超时更新（2026-10-22）

用户原话：“把 TEST 超时改为 240 秒，其余检查和流程保持不变，并据此更新方案后继续”。据此仅将 manifest 的 TEST timeout 由 120s 改为 240s；TEST command、测试覆盖/断言、required=true、COMPILE/GUIDANCE-COMPILE 30s、1.8 stages/审批语义/strict-default 均不变。该实现/验证政策调整记录在 manifest、Plan 和 impact，不更改产品功能目标 Spec。

## 验证结果

- focused：python -m unittest scripts.tests.test_workflow_state -q，29 tests pass（CPython 3.14）。
- Original 120s timeout reports remain historical. Pre-Windows-fix formal checker report `work/issue24-baseline-test240-final-docs.json` applies to the prior tree only. Current Windows fix verification is recorded below; latest formal checker is `work/issue24-windows-path-final4.json` on CPython 3.12.14 with pinned tree-sitter parsers through task-local `PYTHONPATH`, TEST 260 pass in 117.016s under 240s, COMPILE 0.172s and GUIDANCE-COMPILE 0.187s under their unchanged 30s limits; `required_checks_satisfied=true`, `errors=[]`. Full direct `unittest discover` after adding both regressions passes 262 tests in 140.102s.
- Skill Creator quick_validate 使用已有 PyYAML 6.0.3 路径及 PYTHONUTF8=1 后通过；git diff --check 和新增 Python 文件 py_compile 通过。原 database/contracts inventory 为非必需 partial，按既有状态保留。

## Windows reviewed Actions 缺陷修复（2026-10-23）

- 复现证据：GitHub Actions run `39787233509`，提交 `d225cb49d25cec51abfcbaca11470ca8b71ff7af`。`reviewed (ubuntu-latest)` 35s 通过；`reviewed (windows-latest)` 2m39s 失败。Windows checker TEST 70.563s 返回 1（非超时）；诊断全量测试 260 项在 59.142s 结束，1 failure / 9 errors。
- 根因：Windows 临时项目根/目标在 `runneradmin` 长路径与 `RUNNER~1` 8.3 短路径表示间不一致。原 `safe_path` 以词面 `Path.relative_to(root)` 比较，误把同一目录中的路径判为越界。`workflow_state.apply_batch` 把解析后的绝对文档路径再次交给该校验器，所以测试请求、manifest 文档与 archive batch 路径处理连续失败。
- 修复：公共路径边界 helper 在 Windows 上逐组件调用 Win32 `GetLongPathNameW`，只展开存在组件的 8.3 alias 后比较 project-root containment；原 candidate/component link 检查与最终 resolved-root 校验保持。没有用 `Path.resolve` 代替 link 防护；POSIX 词面行为不变。Path-like 参数和结构化错误路径保留原输入。
- 回归：新增 checker 层短路径接受/越界拒绝用例，以及 workflow-state 使用短路径 root 初始化 archive 并成功批量更新、同时拒绝指向项目外的 alias 文件的真实边界用例。Windows focused 回归通过；checker 子套件 119 项通过；完整正式 checker TEST 260 项通过（117.016s）；COMPILE 0.172s、GUIDANCE-COMPILE 0.187s 通过；报告 `work/issue24-windows-path-final3.json` 的 `required_checks_satisfied=true`。短路径专用测试还证明项目外 alias 仍被拒绝；完整 direct TEST 增加两项 Windows regression 后 262 项通过/126.394s。最后正式 checker 报告 `work/issue24-windows-path-final4.json` 的 required checks 全部通过。
- 影响：修复 `scripts/check_project.py` 路径验证边界，并覆盖其消费者 `workflow_state.py` / `task_archive.py`；不改变 manifest 命令、260 项覆盖、240s TEST / 30s compile limits、required checks、Windows/Ubuntu workflow matrix 或 1.8 stages/审批流程。
- GitHub：本修复尚未提交或推送；scope 检查前置步骤已通过。

## 上传前步骤

1. 最终检查本批与既有 Issue #23 文件的暂存范围；不混入 work 临时产物。
2. 已按用户批准 TEST 240s 跑当前 checker，TEST/COMPILE/GUIDANCE-COMPILE 全部通过（见上方最终报告）；该报告只证明清单声明的检查结果。
3. required checks 全部通过后，按原规则暂存批准范围并运行 commit/committed 门禁；control-plane 如需一次性批准，仅按本批批准和原 checker 规则处理，不放宽保护。
4. 两个提交门禁通过后按用户授权 push main 并核对远端 SHA；不创建 GitHub Release。
