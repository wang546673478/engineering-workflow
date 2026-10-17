# TASK-LINKED-ARTIFACTS-01：基线与 Spec / Plan / Task 联动模型

## 当前状态

- 阶段：本地实现、验证与文档整理完成，`complete`（2026-10-18）；1.5.0 主提交已通过提交/实际提交门禁并上传 GitHub；正在补发布回执。
- 当前工件：Baseline `BASELINE-LINKED-02`；Spec `SPEC-LINKED-02`；Plan `PLAN-LINKED-02`；Task `TASK-LINKED-ARTIFACTS-01`。路径由 [manifest](../engineering-manifest.json) 和 [traceability](traceability.md) 定位。
- 来源：本仓库 SKILL.md，发布基点 1.4.4 / `9df5662`，当前 1.5.0 工作树，发布前保持 Unreleased；恢复时核对实际 diff。
- 范围：指令、引用、持久化入口、模板、初始化器、checker、测试及本仓库当前文档。不修改联通中转站或其他项目。
- 需求/方案：本地实现已完成；用户在看到完成摘要后授权提交上传本批 1.5.0，包括已说明的新项目临时基线和检查器规则。审批依据是本轮原话，不沿用历史批准。

## 授权与依据

2026-10-18 用户原话：“那就开始完整的更改吧,现在是更改了提示词对吧?全面修改完了之后,看看既有文档是否符合更改后的内容,不符合是不是需要整理,按照新的内容来?”。实施范围包含前一轮已说明的新项目生命周期、初始化/检查器配套和现有文档整理。

[Spec](../docs/spec.md) 记录需求/验收；[Plan](../docs/plan.md) 记录 PL-01..05。需求确认、本地实施授权、保护规则提交批准和发布分别记录；此前未授权提交发布；现由下述新指令授权。

## 可执行步骤

| 步骤 | Plan / 需求验收 | 依赖 | 状态与负责人 | 产物和证据 |
| --- | --- | --- | --- | --- |
| TW-01 核对规则、工作树和有效工件 | PL-01/03；LINKED-01/03 | 无 | complete；当前 agent | 已读规则、manifest、正文、引用及当前文档；保留原有未提交评估任务 |
| TW-02 补齐新项目/整理规则和模板 | PL-01/04/05；LINKED-01/04/05 | TW-01 | complete；当前 agent | SKILL、联动引用、接入段、模板及公开说明 |
| TW-03 实现初始化和临时基线校验 | PL-02/04；LINKED-02/04 | TW-01 | complete；当前 agent | 显式 greenfield 入口、作用域、状态/完成限制、链接存在性及实际 CLI 回归 |
| TW-04 核对整理当前文档 | PL-03/05；LINKED-03/05 | TW-02/03 | complete；当前 agent | 下方整理表；保留旧审阅和外部项目 |
| TW-05 必需检查并记录限制 | PL-05；AT-LINKED-01..05 | TW-04 | complete；当前 agent | 105 tests、编译、变更范围和技能验证通过；未提交发布 |

LINKED-n 对应 REQ-LINKED-n / AT-LINKED-n；完整映射见追踪索引。

## Skill review

- 来源：当前会话 Skills catalog、根 AGENTS.md 和 manifest；范围扩大后 2026-10-18 重新检查。
- engineering-workflow：adopted；来源本仓库 SKILL.md，1.4.4 发布基点/1.5.0 候选；已读正文、requirements-interview、project-documentation、implementation-workflow、checker、project-agents-clauses、baseline-linked-artifacts。
- skill-creator：adopted；C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md，版本未提供；已读正文及 openai_yaml，用于结构、渐进披露、实际验证和能力边界。
- planning-with-files：not-adopted；宿主清单 C:/Users/54667/.agents/skills/planning-with-files/SKILL.md，版本未提供；已有工件承担唯一状态，不新增台账。
- tdd：not-adopted；宿主清单 C:/Users/54667/.agents/skills/tdd/SKILL.md，版本未提供；以实际 CLI 状态转换和兼容回归验证本批脚本。
- Recheck：2026-10-18 发布范围复核，重新读取正文、implementation-workflow、checker、AGENTS、manifest 与当前工件；采用 engineering-workflow 1.5.0，沿用 skill-creator 的版本和格式验证。发布只使用现有 Git/项目门禁，不新增产品代码、自动迁移或宿主设置。

## 影响分析与门槛变化

- instructions：补齐新项目状态与现状/目标分离、文档整理；新生成 full/lite 都要求链接视图存在，修正“可选但被引用”的不一致。
- checker：旧清单仍需 complete/approved；greenfield 临时状态允许继续工作，拒绝 handoff/选中任务 complete；声明实现位置出现文件时拒绝 not_applicable，不受排除项影响。
- initializer：显式 greenfield，仍为 planned；修正 root/无归属触发器；full 保守要求基线视图，lite 记录实际影响，项目按审阅后的边界细化。
- governance：不将历史 approved 沿用到新工作树；当前事实基线独立记录，保留原批准。补具体 revision、Plan 项和执行步骤；预先存在的任务不改写。
- 局限：仅核验声明范围/链接，不能证明 origin、语义或 revision 一致；仍需 agent 核验。必需测试、控制面保护和外部批准机制不降级。

## 既有文档整理

| 文档 | 不一致 | 处理 |
| --- | --- | --- |
| SKILL/README/元数据 | 正文版本 1.4.4；新项目仅一句例外；lite 说明不符 | 同步 1.5.0，补生命周期及整理入口 |
| Baseline/manifest | 历史批准覆盖了扩展后的工作树，来源模糊 | 新修订绑定具体基点/范围/证据，保留 2026-10-14 原审批 |
| Spec | 缺新项目与整理验收 | SPEC-LINKED-02 增 LINKED-04/05，保留既有要求和发布事实 |
| Plan | 无 revision/设计项，批准表述不准确 | PLAN-LINKED-02，PL-01..05，分清实施和提交批准、输入/输出基线 |
| Task/traceability | 只有概括性下一步 | TW-01..05，需求/验收/Plan/步骤/视图及验证映射 |
| Map/contracts/flow/templates | 未写临时状态及初始化边界 | 按实现刷新当前说明；原发布保留范围 |
| Database/inventories | 无业务数据库，适配器未改 | 复核后保持 metadata-only，manual 清单 partial/optional |
| 历史任务和原有评估 | 不能改写成新版批准或本轮成果 | 保留；当前入口由 manifest 选择，旧证据仅适用旧范围 |
| change-impact / skill-review 旧入口 | 顶部发布批准和技能结论仍像当前状态 | 增加当前任务入口并标明下方为 2026-10-14 历史记录 |

## 验证与证据

- 本轮最终必需检查：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-LINKED-ARTIFACTS-01 --run-checks --report work/linked-greenfield-final-check.json`，exit 0，required_checks_satisfied=true。
- TEST：完整 105 项 unittest，通过，75.053 秒；包括 full/lite 从空目录到首批实现、临时状态完成限制、实际 Git change/handoff、审批仍生效、平铺项目初始化、旧 manifest 和保护规则回归。COMPILE、GUIDANCE-COMPILE 均 exit 0。
- 官方 skill-creator quick_validate.py：使用已有隔离 work/pyyaml，UTF-8 模式，结果 Skill is valid!。未新增全局依赖。
- change-scope、manifest 和 task-gate 通过，uncovered/documentation_gaps 为空；元数据 1.5.0 一致，git diff --check 通过。最后仅刷新文档/状态，再核对结构、链接、范围和证据新鲜度，不重复未受影响的全量测试。
- 源码证据：`work/linked-greenfield-source.json` 保存当前指令、模板、脚本/测试的 SHA-256；验证报告位于忽略的 work 目录。当前基线记录范围，不转移旧审批。
- 可选 database/contract 手工清单仍为 partial；没有因此降级必需项。checker 不证明业务语义、revision 一致、origin 真实性、宿主加载或外部项目已同步；本轮未运行远程 CI、提交/发布门禁或生产验证。

### 本批历史验证与更正

首批 97 tests、4 个 focused linkage/init tests、Python 编译和 `work/linked-artifact-model-baseline-v2.json` 曾通过；当时官方 validator 缺 PyYAML/网络不可用。这些结果保留为历史，不证明本轮源文件；本轮找到已有 work/pyyaml 后完成了官方验证。初始 Plan 的 approved-for-local-implementation 标签本身不构成审批证据，当前授权以本轮用户原话和具体范围为准。

本轮调试修正了测试场景未选中 active_task、flat-source CLI 未传必需 manifest 参数的问题；最终完整测试全部通过，断言和完成门槛保留。

## Release impact 与下一步

- VERSION 为权威，同一批 1.4.4 → 1.5.0 MINOR；兼容新增能力，历史版本保留。同步 SKILL、README、agents、CHANGELOG。
- 1.5.0 源码已于 2026-10-18 上传，CHANGELOG 填写实际日期。用户已批准具体完成范围，仅在对应一次检查的子进程环境传递批准信号，不写入永久设置。
- 下一步：将发布回执按同等门禁提交上传，核对最终远程 SHA；本地独立评估记录保留。

## 2026-10-18 发布授权与范围

用户在上一轮完成摘要（105 tests、greenfield 生命周期、现有文档整理、1.5.0 未发布）后原话：“已经升级完成了对吧?升级完成就上传github”。该指令批准提交并上传这批已经完成的 1.5.0 内容，包括前文说明的保护规则变更；无需再要求一次同范围确认。

发布在独立 checkout 中准备，基点 9df5662。排除原有 version-policy-task 本地补记及四份 assessment/pilot 文档和对应 manifest 注册；原目录文件保持原样。发布清单保留全部已发布历史任务，只增加本批联动任务、需求/验收、工件指针及基线当前状态。没有修改旧 required 检查、保护路径集合或批准变量。

本轮新增提交/发布证据不改变交付行为，继续使用 1.5.0，不再升版；GitHub 源码上传与 hosted CI 的结果分别核实。

发布前 commit 模式发现 AGENTS.md、VERSION、CHANGELOG.md 三个已归属 instructions 的变更尚未列入本任务文档触发器。change 模式不强制逐源文件触发覆盖，因而此前通过不能替代提交门禁。现补齐这三个既有作用域到 workflow-guidance，继续要求同组 Spec/Plan/Map/Contract/Flow/Task 更新；未放宽检查或排除路径。失败时测试按门禁跳过，待提交预检通过后执行。

### 1.5.0 源码上传回执

- 主提交：`46d57a6cefd5cc80ae62e47099b782d4cb381504`；2026-10-18T02:08:31+08:00 核对远程 origin/main 为同一 SHA，源码上传成功。
- 主提交暂存区门禁 `work/release-1.5.0-commit-v4.json` 与实际提交门禁 `work/release-1.5.0-committed.json` 均 exit 0，required_checks_satisfied=true。两次均包含 105 tests、COMPILE、GUIDANCE-COMPILE，以及 task/control-plane/提交范围检查；可选手工清单仍 partial。
- 本次仅补发布日期、状态和真实回执，不改变实现或已批准的检查政策，保持版本 1.5.0；收尾仍按同等提交/实际提交门禁验证，不将未执行检查写成通过。
- 尚未把 GitHub hosted CI 记为通过；上传成功和本地检查不是远程 CI 成功证据。最终回执 SHA 由本地 work/release-1.5.0-final-receipt.json 保存，避免自引用尚未存在的提交。
