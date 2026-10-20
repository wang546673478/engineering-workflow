# TASK-ISSUE-22-REVIEW：全局对照下的三项增强

## 当前状态

- 本批结果：三项增强已实施并完成本地验证，版本 **1.7.2 / Unreleased**。完成时间：2026-10-20T17:27:04.644555+08:00。
- 实际完成范围：原实施指引的缺陷证据、原交付收敛的差异分类与回流、原访谈指引的可选EARS/Given–When–Then示例，以及两个原模板、短入口和B/M/C/F/追踪/版本同步。
- 授权原话：“那就按照这个增强的文档去实施”。结合此前“不要全部读完了，先看看哪些可以借鉴”，全量上游审读继续暂缓，不再作为本批依赖；它没有被标为完成。原更早的“先审后改”顺序保留为历史。
- 当前链路：输入BASELINE-ISSUE22-01 / source868e496 → 冻结SPEC-ISSUE22-ENHANCEMENT-01 r1 → PLAN-ISSUE22-ENHANCEMENT-01 r2 → T22-01及T22-08..16 → 当前BASELINE-ISSUE22-02。
- 当前下一步：向用户交付本次GitHub源提交回执；源码已上传main，托管CI独立记录，完整审读及全局安装继续暂缓。

## 实现与验收

| 完成内容 | Plan / Task | 实际文件与证据 |
| --- | --- | --- |
| 缺陷的症状、复现、原因证据/假设、保持行为、前后结果及相称验证 | P22-03 / T22-08 | references/implementation-workflow.md；S22-02..04 |
| 本批缺失、部分、矛盾、无归属实现、过期/未验证证据及权威回流 | P22-04 / T22-09 | references/baseline-linked-artifacts.md原交付段；S22-05/06 |
| EARS五型及组合中文示例、Given–When–Then验收 | P22-05 / T22-10 | references/requirements-interview.md；S22-07/08 |
| 短路由、可选模板、全局视图、真实版本与验证闭环 | P22-06..08 / T22-11..16 | SKILL/README、spec-plan-task/impact模板、B/M/C/F及元数据；S22-01/09/10和原检查 |

REQ-ISSUE22-E01..E10 / AT-ISSUE22-E01..E10的逐项关系见[traceability](traceability.md)，需求/验收语义仍是原Spec r1；原审核文本及SHA256已存档，当前仅清理Markdown尾空格（fmt1）。旧记录和格式仍可用，没有必填BUG报告、阶段、审批轮次、schema/状态机、CLI或依赖变化。

## 全局影响和保持性

- instructions负责三个原引用，SKILL/README只路由，原两个模板只提供可选提示；governance维护权威记录。依赖方向、checker/adoption/collector/adapter运行代码、AGENTS/原接入模板/旧manifest示例/decision模板及CI/hooks未变。
- 同步BASELINE、module-map、contracts、business-flow及追踪，当前事实基线02不沿用旧批准到新内容。数据库/API/权限/计费/事件或任务无新增：本仓库无业务数据库，docs/database.md及原适配器边界复核后保持，不伪造库存或迁移。
- 当前任务documentation_impact补实际指令/模板/版本路径的原文档同步门槛；checks、120/30/30秒、schema、modules、exclude和control_plane对照HEAD完全不变。未设置提交控制面的外部批准变量。
- 独立兼容指引澄清批次按PATCH到1.7.2，VERSION/SKILL/README/openai.yaml/CHANGELOG同步；1.7.1 / Unreleased旧条目保留。没有实际发布日期或外部项目迁移声明。

## 实际验证与失败历史

- 原正式命令及变更范围门槛最终通过：enhancement-change-ready.json，errors=[]、required_checks_satisfied=true；TEST、COMPILE、GUIDANCE-COMPILE均pass。TEST仍为原unittest discover命令及120秒，编译仍为原命令及30秒。
- 前两次正式TEST失败、后一次触及120秒的报告全部保留。直接诊断206项通过未替代失败门槛。查明Windows中声明的裸python解析到任务专用基础Python3.11.15，而锁定解析器原只在venv；受控runner下Rust fixture明确复现缺解析器，补入相同依赖后focused测试通过。其后计时诊断206项在102.382秒完成，最终仍独立运行原正式quiet命令并通过，没有修改断言、跳过测试或放宽时限。早先超时保留为环境/运行耗时限制，未凭诊断消除。
- Skill-creator quick_validate通过；版本/源哈希/策略/链接核验通过，git diff --check通过。最终记录更新后再做只读范围/链接核对，不重复未受影响的运行回归。
- S22-01..10已在ignored局部合成输入上应用原指引并检查实际输出，其中S22-02保留Issue/Task文件，S22-08保留带原REQ/AT的Spec。仅为同一agent的手工语义练习，不是独立agent验证、上游产品执行或未来宿主遵循保证。
- 原机器结果、命令摘要、内容哈希、场景输入/实际记录及失败/修正证据统一在[issue-22-evidence.json](issue-22-evidence.json)的enhancement_implementation和validation_environment_correction。正式报告在work/issue-22-review/，完整结果摘要保存在可追踪JSON中。

## Skill review与环境

- 本会话catalog及AGENTS为来源；本轮重读本仓库/用户指定engineering-workflow输入1.7.1、适用implementation/linked-artifacts/interview/project-documentation/checker及system skill-creator（无版本）。采用前两者；无运行代码变更，不采用TDD、重复planning体系或子agent。manifest保存来源/时间/理由。
- 任务局部CPython3.11.15，原锁定tree-sitter0.25.2、tree-sitter-rust0.24.2，PyYAML6.0.3，Node24.21.0/TypeScript6.0.3。运行时、venv和复核产物保留在ignored工作目录，未改系统默认Python/全局skill。

## 延后事项与完成边界

- REQ-ISSUE22-SOURCE / AT-ISSUE22-SOURCE及T22-02..07完整五仓库审读与全量合并仍未完成：366份已读、3177份未读。账本保留，执行由当前task的deferred字段引用；本次完成状态仅覆盖用户最新指定的三项增强。
- 当前结论只采用已读证据支持的记录纪律、差异分类和可选表达，没有移植上游源码/引擎/hooks。后续用户明确恢复完整审读时从pending账本继续，不重读已完成文件。
- 未验证其他平台/宿主未来行为、托管CI和全局安装；这些不冒充本地结果。先前实施指令未包含提交；后续“提交到githb”已明确授权提交/推送本批内容，安装与Release等仍不包含。

## 先前任务记录（历史，不代表当前实现状态）

以下为调查、方案准备和实施启动时的原记录。原话、当时覆盖、批准与限制保留；当前完成范围、验证和延后状态以上文为准。

### 历史任务记录：全局能力审查

日期：2026-10-20（Asia/Shanghai）

## 当前状态

- 阶段：三项增强正文、短入口、可选模板、B/M/C/F和1.7.2 Unreleased版本已写入，当前执行S22场景和原正式检查。Spec r1冻结；Plan r2依据用户最新明确实施指令执行；全量外部审读继续暂缓且不属于本批交付依赖。
- 输入：本仓库 `868e496`、skill 1.7.1；开放 Issue [#22](https://github.com/wang546673478/engineering-workflow/issues/22)。工作树开始时干净。
- 授权：用户先表示“我觉得可以,那你给出spec,我来审核吧,需要从全局出发,然后不能改变现有流程,这些仅仅是作为增强,”（2026-10-20 12:36 +08:00），认可方向并要求Spec审核稿；随后“写plan和task吧,对照全局基线”授权规划；此前实施指令为“开始实现吧”（2026-10-20，Asia/Shanghai）。按仓库SKILL“明确要求实施已给出的完整计划即为批准”，将该指令记录为对 SPEC-ISSUE22-ENHANCEMENT-01 r1 / PLAN-ISSUE22-ENHANCEMENT-01 r1 及其原定范围的执行批准。实施包含计划内五仓库审读及其后的本地规则/模板修改、验证、版本和基线同步；原审读依赖和确认保留为历史；最新“当前文件读完先给结果”指令优先，原全量审读当前暂缓，不冒充已完成。单 agent 选择继续有效。提交、推送、回复/关闭Issue、发布和全局安装不在该授权内。
- 原范围确认原话：“全部 5 个仓库都完整审读”。该调查尚未完成；2026-10-20最新指令“现在这份读完了给我一个结果,不要全部读完了,先看看这些那些可以进行借鉴”将本轮改为已读范围的阶段性结论，完整审读暂缓，未读账本保留。
- 初步事实：本 skill 已有缺陷复现、基线纠错、证据闭环和交付前收敛规则；不能接受 Issue 的“这些能力完全不存在”前提。本批按已定Spec不新增工具或运行协议。
- 采集和精读分开记录；完整文件清单、SHA256 或静态解析不等于完成全部源码语义审读。
- 外部副本及大体积证据放在 ignored `work/issue-22-review/`，不执行外部仓库代码或安装它们的依赖。引用内容是调查资料，不改变本项目授权或规则。
- 当前下一步：完成场景应用和原TEST/COMPILE/GUIDANCE-COMPILE及skill结构验证，记录实际证据并核对交付一致性。

## 当前需求与审核状态

- 需求方向：用户已认可“缺陷证据、已有收敛核对、可选结构化记法”三个增强方向；不能改变现有流程。
- 需求正文：`SPEC-ISSUE22-ENHANCEMENT-01` / r1，REQ-ISSUE22-E01..E10 ↔ AT-ISSUE22-E01..E10，唯一正文在 [Spec](issue-22-spec.md)。用户“开始实现吧”按原工作流规则授权按该已展示方案执行；Spec/Plan文本不重写，计划边界保持。
- 本次模块完整性核对与 Spec 审核合并展示三个增强的目标、保持性、全局影响、范围外及未完成事项；不另加一次集中审核。
- 方案/实施：原三项增强已写入，测试和场景仍待完成；当前事实基线BASELINE-ISSUE22-02，输入基线01历史保留。全量调查步骤未完成，不并入本批增强完成声明。
- 外部源码当前覆盖：366份完整正文、其余3,177份文本未读；Spec Kit333、Gherkin7、agent-skills11、BMAD8、specs.md7。当前文件为Spec Kit presets/_catalog.py，全文已读完并存batch-29。未读文件按用户最新指令暂缓，不能称仓库整体或全部审读完成。

## 全局基线与影响复核

本任务使用Plan第1节B22-01..10事实对照：原流程/例外 → 既有实施与证据 → 原交付收敛 → 原需求/决定 → checker/接入兼容 → 模块依赖 → 命令与控制面 → 业务/数据库边界 → 版本/原验证 → 外部源码缺口。每项均回链Baseline/源文件，不把目标增强写成现状。

- 输入视图：`planning/baseline-review.md`、`docs/module-map.md`、`docs/contracts.md`、`docs/database.md`、`docs/business-flow.md`；原历史审批按其版本保留。
- 计划负责模块：instructions主导，governance维护权威状态，tests复用既有回归；checker/adapters/source-context只核验保持的运行边界。本次无新运行模块和依赖。
- 调用/资料流：skill入口 → 原实施/收敛/访谈引用 → 已有Task/Spec/impact模板 → 项目记录与验证 → 受影响Baseline视图。旧AGENTS与adoption入口继续指向同一套工件。
- 计划触达：`SKILL.md`、`README.md`、`references/implementation-workflow.md`、`references/baseline-linked-artifacts.md`、`references/requirements-interview.md`，以及按互链实际需要的`project-documentation.md`；两个原模板`spec-plan-task.md`与`impact-analysis.md`；本仓库Baseline/M/C/F、追踪和任务资料；交付版本元数据按实际批次更新。
- 不适用：业务表/字段/迁移、权限/计费、产品API、缓存/任务/事件新增均无；由本仓库无业务数据库和现有adapter责任证实。数据库字典/源清单、adapter、collector不改，保留复核理由，不伪造库存快照。
- 工具合同：原schema1、`small_fix`、checks命令/时限、8MiB输出上限、Git state/tree、父版本保护、批准变量和CI/hooks不改。维护任务实际路径的documentation_impact按原门槛对齐，不把本批状态链接当新全项目门禁。
- 冲突处理：若实施实际需要更改以上运行合同，先标为超当前Plan并核验实际影响；不能静默扩大范围或把新增限制称为保持流程。

## 可执行任务与进度

所有动作由同一agent负责；没有子agent派发。P22对应[Plan第3节](issue-22-plan.md#3-实施项与依赖顺序)，E编号对应Spec的REQ/AT-ISSUE22-E编号。B/M/C/D/F是全局基线视图，源调查只更正其实际相关事实，不把未审读范围纳入complete。

| Task | Plan / REQ-AT | 依赖 | 具体动作、文件与可审阅产物 | 视图 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T22-01 | P22-01 / E01,E09,E10 | 当前规则/Spec/基线 | 读真实SKILL/规则与B/M/C/D/F，对照`868e496`；完成Plan对照、Task分解、活动指针和Spec哈希保存 | B,M,C,D,F | complete，仅规划准备；证据见evidence的plan_preparation，实施前重核新鲜度 |
| T22-02 | P22-02 / 原SOURCE | T22-01；原调查授权 | Spec Kit固定SHA：逐项完成`spec-kit-audit.json`中916份pending正文；追踪CLI、integrations、file policy、extensions、workflows、tests/模板/配置和生成来源；保存职责、消费者、限制及实际覆盖 | B相关事实 | 按用户指令暂缓；已审333份、598份pending，逐文件证据保留 |
| T22-03 | P22-02 / 原SOURCE | T22-01；原调查授权 | Gherkin固定SHA：994份pending；覆盖12种语言的手写/生成解析、共同语法、fixtures与测试合同，区分语法/AST与执行验证；逐文件记录 | B相关事实 | 按用户指令暂缓、未完成；原已审7份保留 |
| T22-04 | P22-02 / 原SOURCE | T22-01；原调查授权 | agent-skills固定SHA：206份pending；覆盖所有skills/commands/hooks/evals/fixture/validator与宿主适配；保存实际规则与执行边界 | B相关事实 | 按用户指令暂缓、未完成；原已审11份保留 |
| T22-05 | P22-02 / 原SOURCE | T22-01；原调查授权 | BMAD固定SHA：570份pending；覆盖setup/render/config/tickets/knowledge/evals与全部行为模板、测试和发布工具，注明V7 preview版本范围 | B相关事实 | 按用户指令暂缓、未完成；原已审8份保留 |
| T22-06 | P22-02 / 原SOURCE | T22-01；原调查授权 | specs.md固定SHA：809份pending；覆盖四flow、CLI/installer/dashboard/VSCode、tests/config/历史资料，核对生成bundle来源与差异，保留未验证行为 | B相关事实 | 按用户指令暂缓、未完成；原已审7份保留 |
| T22-07 | P22-02 / 原DECISION,E09,E10 | T22-02..06 | 汇总全部来源coverage；更新`issue-22-assessment.md`和evidence中的采用/不采用、许可证/版本边界；有冲突则纠正当前基线和受影响Plan，保留历史 | B,M/C/F按实际 | 全量汇总未完成；当前阶段性结论已写assessment |
| T22-08 | P22-03 / E02,E03,E04,E01 | T22-01；阶段性结论/最新实施授权 | 编辑`references/implementation-workflow.md`原调查/验证段，补按需缺陷证据与保护范围；用S22-02..04核对不新增批准/表单/强制TDD | B,M,C,F | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-09 | P22-04 / E05,E06,E01 | T22-01；阶段性结论/最新实施授权 | 编辑`references/baseline-linked-artifacts.md`原交付收敛段；`project-documentation.md`按需互链；S22-05/06核对范围、证据与回流 | B,M,C,F | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-10 | P22-05 / E07,E08,E01 | T22-01；阶段性结论/最新实施授权 | 编辑`references/requirements-interview.md`，补可选EARS中文五型/组合与GWT例子；S22-07/08核对旧格式、状态和误报边界 | B,M,C,F | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-11 | P22-06 / E01,E02,E05,E07..10 | T22-08..10 | SKILL原节点加短路由；README短说明；`assets/templates/spec-plan-task.md`、`impact-analysis.md`只加可选提示/引用。旧decision/AGENTS/manifest/接入模板维持原样 | B,M,C,F | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-12 | P22-06 / E09,E10 | T22-08..11 | 实际增强后刷新Baseline/M/C/F/trace，核对DB不适用；在当前manifest补实际指令/模板/版本路径对应的原documentation_impact，所有权威revision一致，历史不转批准 | B,M,C,F；D复核 | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-13 | P22-07 / E01..10 | T22-11..12 | 实际在局部fixture应用指令/模板，逐项S22-01..10记录输入、观察行为、判断、文件/hash及局限；复用现有工具回归，不用文字匹配冒充行为验证 | B,M,C,F | planned，验收未执行 |
| T22-14 | P22-08 / E10 | T22-12..13 | 核对1.7.1仍Unreleased及最终批次；按PATCH候选1.7.2或原同批次规则同步VERSION/SKILL/README/openai.yaml/CHANGELOG，记录真实状态 | B/M/C/F说明 | complete；实际文件/哈希见evidence.enhancement_implementation，最终验证另记 |
| T22-15 | P22-08 / E09,E10 | T22-13..14 | 在原兼容环境执行`change --run-checks`的TEST/COMPILE/GUIDANCE-COMPILE、skill quick_validate及diff检查；保留原命令时限/失败历史，绑定实际source/tree/环境 | B及evidence | planned，正式检查未运行 |
| T22-16 | P22-08 / 全部、原DECISION | T22-08..15及T22-01 | 按原交付核对REQ/AT、Plan/Task、事实与版本；交付实际结果/未验证范围。只有授权包含提交/发布时才执行对应原commit/committed及外部动作，否则仅交付本地成品 | B,M,C,F | planned，无提交/发布授权 |

当前单agent执行T22-08..16；T22-02..07保留延后状态，原完整审读不转完成，最新用户指令调整本批依赖。三项的目标、流程保持约束和原验证门槛不变。

## 验证计划、版本和交接

- 场景定义和REQ/AT映射以Plan第6节S22-01..10为准，不在多个文件复制另一套验收。所有增强验收仍未执行。
- 正式命令保持当前manifest：TEST为`python -m unittest discover -s scripts/tests -q` / 120s；COMPILE为原三个checker/adapter脚本 / 30s；GUIDANCE-COMPILE为原三个接入脚本 / 30s。不得删除、改弱、改超时或靠skip过门槛。
- 环境：实施验证前复用/准备任务局部CI兼容Python3.11、原锁定Rust解析器与Node/TypeScript；缺依赖先按原README准备，仅影响任务环境。当前写计划不运行外部项目或安装其依赖，不需数据库/端口/业务服务。
- 交付版本：本轮计划/状态记录不升版；未来兼容指引/示例按PATCH评估，当前候选1.7.2，但要先核对1.7.1 Unreleased与是否合并同批次，不提前改发布日期或声称已发布。
- 检查器结果与人工语义核验分开；相同agent的fixture推演不称独立验证。既有测试证明工具行为，不能证明所有agent/宿主以后总遵守指令。
- 中断恢复：读取本Task/Plan/Spec、source/status、当前evidence.semantic_progress和pending账本，再从当前未完T22继续；不得重置工作树、重跑完成调查或把未运行写成通过。
- 真实限制：外部全码未完成，托管1.7.1结果未在本批重认证，Spec/Plan按最新明确实施指令记录执行批准，未转用旧任务批准；没有用户要求/授权的全局安装、推送、关闭Issue等任务。

## 需求和验收

- REQ-ISSUE22-REVIEW / AT-ISSUE22-REVIEW：核实开放 Issue 的实际内容和来源；区分已有能力、真实缺口、不可证明的比较和候选增强。
- REQ-ISSUE22-PARITY / AT-ISSUE22-PARITY：任何推荐必须保留原阶段、原有小修/恢复/空项目例外、审批语义、Spec 冻结及既有检查强度；不能用“兼容新增”掩盖额外必过步骤。
- REQ-ISSUE22-SOURCE / AT-ISSUE22-SOURCE：全部五个仓库固定 revision，覆盖实现、测试、脚本、配置及作为行为实现的提示模板；排除二进制需写原因，不能把扫描或摘要冒充精读。
- REQ-ISSUE22-DECISION / AT-ISSUE22-DECISION：交付全局结论、逐项采用/不采用理由、接入位置、兼容性、验证方案及实际限制。

## Skill review

- catalog：本会话 Skills catalog；检查日期 2026-10-20（Asia/Shanghai）。
- adopted engineering-workflow：本仓库 `SKILL.md` 与用户指定安装副本 `C:/Users/54667/.codex/skills/engineering-workflow/SKILL.md`，均为 1.7.1；AGENTS 指定以仓库正文为权威。适用引用：project-documentation、baseline-linked-artifacts、implementation-workflow、requirements-interview、source-context、checker。
- adopted skill-creator：`C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，未提供版本；用于评估修改现有 skill 的范围、渐进披露和验证，不能以借鉴为由换工作流。
- not-adopted planning-with-files：`C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，未提供版本；复用当前 manifest/Task/基线体系，不建平行计划。
- not-adopted tdd：`C:/Users/54667/.agents/skills/tdd/SKILL.md`，未提供版本；本次增强为指令/模板修改，无运行代码改动，不采用额外TDD流程；保留计划场景与原回归。
- not-adopted triage-issue：`C:/Users/54667/.agents/skills/triage-issue/SKILL.md`，未提供版本；当前增强建议已存在，本轮不新建 GitHub Issue、不把建议当已复现缺陷。
- recheck：2026-10-20T16:55:18.904703+08:00：已重读本仓库/用户指定engineering-workflow1.7.1、system skill-creator、会话catalog、规则与当前权威工件/适用引用。增强实现仍为指令与模板，无新运行代码；采用项保持，不引入TDD、平行规划或子agent。

## 影响分析 / 方案边界

- 本轮已授权按Plan r1执行；按最新指令在完整审读暂缓条件下实施三项增强。后续实际触达以全局影响复核和Plan为准；CLI、检查命令、schema与批准合同保持。
- Spec 对 instructions（访谈/缺陷/交付指引）、templates、governance 及下游 agent/采用项目的使用路径做全局影响约束；checker、adoption、source-context、adapters 的运行合同不属于本版增强实现范围，数据库/API/权限/计费无新增产品行为。未来实施方案仍需核对实际 diff。
- 当前Plan以instructions和governance为修改责任方，tests复用原回归；checker/adoption/source-context/adapters只核验原合同，不计划修改运行代码。早期评估过checker增强候选，现已明确不纳入Spec r1及当前Plan。业务数据库和产品运行时不适用。缺陷证据复用Task/impact/traceability，收敛复用原linked-artifacts交付闭环，需求记法只作可选表达。
- 新 checker 模式或强制字段会影响控制面/旧清单，不能仅因 required=false 就声称流程不变；须明确默认行为、存量兼容、失败语义和批准范围。
- 本轮证据/状态记录未改变交付实现，不升版；若后续新增兼容能力按最高实际影响评估 MINOR，规则澄清评估 PATCH。

## 验证

- Plan/Task准备：10项基线事实、8个Plan项、16个Task步骤及10组增强REQ/AT映射完整；活动指针、文档/范围检查与无环依赖核验通过。Spec r1 SHA256保持原值，checks/control/schema/modules/excludes及交付skill内容对照HEAD未变。证据见[plan_preparation.validation](issue-22-evidence.json)。本项通过只代表规划文档核验，不代表增强验收或完整外部审读通过。
- `plan-change-structure.json`的文档/manifest/task/变更范围检查无错误；未启用run-checks，TEST/COMPILE/GUIDANCE-COMPILE均skipped，整体`required_checks_satisfied=false`。本轮仅规划/记录变更，不重复未受影响的实现回归；正式实施后的原检查保持待执行。
- Spec r1：10组REQ/AT、唯一正文、活动Spec/Task/Plan引用、pending审核/实施状态核验通过；`git diff --check`通过。相对HEAD比较确认schema_version、checks、control_plane、exclude_paths、modules与工作流阶段声明没有改变，交付skill内容未修改。记录检查只证明本次草稿链接和政策对比，不证明未来增强实施的流程等价。
- `spec-change-structure.json`中的文档/manifest/task/变更范围门槛通过；未运行TEST/COMPILE/GUIDANCE-COMPILE，整体`required_checks_satisfied=false`，不声称全门禁或任何增强验收通过。草案准备只改规划与记录，不重复未受影响的实现回归；正式交付验证沿原规则。
- 已验证：公开 GitHub API 可读取 Issue；五个仓库 clone 完成且固定 SHA；没有使用或保存聊天中提供的凭据。
- 未验证：外部全码语义审读、外部运行行为、新能力实现/测试；不能标为通过。
- 完整回归只在实际改变受验证内容时运行；纯调查检查引用、证据新鲜度、路径与范围。

## 当前停读点、结果与原顺序记录

- 历史顺序确认：“保持原顺序，先审完五仓库再实现”。最新用户指令“现在这份读完了给我一个结果,不要全部读完了,先看看这些那些可以进行借鉴”优先；已读完当前文件，当前暂停完整审读并先报告。本轮没有扩大增强范围或改动Spec。
- 当前完整审读366份、未读3,177份；停读文件Spec Kit presets/_catalog.py的1028行已完整检查。已读范围包括原关键链路，以及Spec Kit workflow/integrations、artifacts、认证、bundles/events、extension CLI/update事务及部分preset实现；各仓库未读项以audit pending为准。
- 新确认：engine的requires是声明性前提，不是权限沙箱；continue_on_error可保留失败步骤但让配置流程继续，未填slot也可skipped后整次completed。它们是该执行平台的语义，不能替代我们原必需检查或成为本增强的新执行合同。只读源码核验，不声称运行测试通过。
- 下一步：交付阶段性借鉴建议与准确实现状态；剩余审读不自动恢复。若后续继续增强工作，沿用已确认目标、最新用户范围和原验证标准，不把旧全量审读要求或本次停读误写成已完成事实。

## 执行启动记录

- 2026-10-20：用户明确“开始实现吧”。按原规则批准已展示Plan r1执行及Spec r1需求基线；不新增重复审核，也不将该指令视为跳过五仓库完整审读。批准原话、内容哈希和范围见evidence的execution_start。此前pending记录作为当时历史保留。
- Skill review复核：当前目录SKILL 1.7.1、用户提供的同名正文、system skill-creator及适用引用继续采用；TDD已阅读但不采用，因为本计划无运行代码变更，保留实际场景和原回归。仍单agent，不启用子agent。

## 调查历史

以下覆盖数字是各历史批次的输入/输出快照；当前进度以上面的当前状态和evidence.semantic_progress为准。

- Issue #22 开放、无评论，建议 defect 工件、assess/fix/test、converge 和可选 EARS/Gherkin；自身约束是不增加原流程负担。
- 本仓库 `references/baseline-linked-artifacts.md` 已有“交付前收敛”；`check_project.py` 已校验 ID/文件/链接/声明依赖/完成门槛，但不会证明需求语义或每项验收的运行证据。
- Spec Kit bug/converge 的入口为 agent 提示模板；不能直接把它们描述成机械验证器。
- 全量采集结果：3,601 个跟踪文件，3,543 个文本/765,404 行，58 个二进制。采集预算无文本遗漏；Python AST 全部成功，314 个 JS/TS 文件经 TypeScript6.0.3 AST 遍历，4,553 个函数/回调，无 parse diagnostics。这些是静态机械证据，不是全部逐文件语义审读或运行测试通过。
- 关键链路精读：Spec Kit bug/test/converge 及相关 scaffold/workflow 测试、gate/command 调度部分；Gherkin grammar/Python AST/TokenMatcher/Compiler/JS API；agent-skills debugging/validator/eval 核心；BMAD bug 模板/票据/verification-gap/build 规则；specs.md EARS/AI-DLC 模板、artifact-validator、FIRE complete-run 及相关测试部分。完整待审列表留在各 repo-audit.json 的 semantic_review=pending，未虚填完成。
- Kiro 公开 bugfix-specs 和 requirements-first Markdown 已核实；Kiro 闭源引擎不在源码审查证据中。公开 API 后续遇到共享配额限制，改读公开网页和已克隆源码，调查未被阻断。
- 单独的语义覆盖账本已登记48份完整正文（Spec Kit15、Gherkin7、agent-skills11、BMAD8、specs.md7）；其余3495份文本仍待审。函数索引/关键词命中/截断输出不填成完整审读。工作继续从各仓库audit里的pending条目恢复，不能把当前评估写成最终全部审查完成。
- 状态核验：`change --base HEAD --task TASK-ISSUE-22-REVIEW` 未启用run-checks，声明/引用/变更范围检查通过，整体`required_checks_satisfied=false`，三项必需命令均skipped。未把它报成全门禁通过；本轮没有实现变化，不重跑未受影响的全量测试。`git diff --check`通过。未暂存、提交、推送或触发控制面批准。

## 最新用户决定：先交付阶段性结果

- 记录时间：2026-10-20T16:46:28.078319+08:00。用户原话：“现在这份读完了给我一个结果,不要全部读完了,先看看这些那些可以进行借鉴”。
- 当前文件已读完，完整审读暂缓；没有完成全部五仓库的声明。关联REQ/AT-ISSUE22-SOURCE与DECISION的完整范围保持未完成，本次只交付明确范围的中间结论。
- 用户询问三项是否已增强，实际核对：原skill已有一般复现/纠错/收敛规则；本次更具体的证据指引、收敛分类、EARS/GWT示例均未实施，且没有相应增强验收通过证据。
- 影响：仅权威记录/来源评估与当前执行状态；无模块连接、CLI合同、业务数据库或运行政策变化。未提交、未推送、未更新安装版；交付内容未变化，当前无需升版。

- 本次阶段性记录核验：git diff --check通过；interim-structure.json的文档/任务/变更范围无错误。未传--run-checks，TEST/COMPILE/GUIDANCE-COMPILE均skipped，required_checks_satisfied=false；不是增强验收通过。SKILL/README/references/templates/scripts/版本与HEAD没有交付内容diff。

## 三项增强实施授权与影响

- 2026-10-20T16:55:18.904703+08:00，用户原话：“那就按照这个增强的文档去实施”。阶段性文档已交付，三项增强范围不变；用户明确在全量审读暂缓条件下实施，不需要重复批准。
- 全局链路：SKILL/README短入口 → 原三份引用 → 原Task/impact/Spec模板 → 项目权威记录/验证 → Baseline回写；instructions负责，governance记录。无新命令/schema/状态机/审批/依赖，数据库与产品API无变化。
- 在原documentation_impact中登记实际规则/模板/版本路径，要求同步B/M/C/F/trace/Task；checks/control/schema/modules/exclude政策保持，未注入提交批准变量。
- 版本采用独立PATCH 1.7.2 / Unreleased；原1.7.1条目保留。记录与结果见evidence.enhancement_implementation_start。

## 当前实现与验证准备

- 三份原引用、两个原模板及SKILL/README短路由已增强；M/C/F/B及版本同步，Spec r1哈希不变。唯一规则正文仍归原章节，旧模板/清单无需迁移。
- 版本1.7.2 / Unreleased；保留1.7.1历史待发布条目。本地Python3.11.15、独立validation-env，安装原锁定tree-sitter0.25.2/tree-sitter-rust0.24.2和PyYAML6.0.3；Node/TypeScript6.0.3通过原npm ci --ignore-scripts准备。环境保留在ignored工作目录供复核，未改系统默认Python。
- 检查与场景准备不证明通过；当前正式验收仍pending。没有上游执行、子agent、全局安装或外部发布。

## GitHub提交授权与保护范围

- 2026-10-20T17:37:14.093570+08:00：用户在三项完成说明及本地可审阅结果之后明确“提交到githb”，授权本批1.7.2成品和配套资料的提交/推送。具体交付哈希见evidence.github_submission；不转用旧任务批准。
- 受保护的SKILL短入口/版本与VERSION/CHANGELOG/manifest任务记录纳入本次提交；无检查/保护限制放宽，也无新流程门槛。按原checker通过一次性外部确认信号运行保护门禁，不把批准值写入配置或提交脚本。
- 远程origin/main起点与本地HEAD同为868e496；使用本地codex/issue-22-guidance分支准备，普通fast-forward推送到现有main，不强推。原全量审读仍延后、全局安装未动。
- 待验证：暂存区与精确提交的原门禁、远程提交回执及托管结果；已有本地change结果不替代这些提交身份。

## 提交排版核验

- 2026-10-20T17:45:26.764834+08:00：暂存检查发现原未跟踪Spec/Plan顶部的Markdown硬换行尾空格；已只移除尾空格，修正前后按空白规范化的文本tokens完全一致，需求/验收及审批语义不变。Spec r1原审核全文和原SHA保留在evidence.spec_format_correction，当前格式SHA单独登记，不谎称原始字节哈希未变。
- 已取消旧暂存检查，随后对修正后的真实暂存树重新运行原提交门禁；未降低git diff --check或任何原必需命令。

## GitHub源提交回执

- 2026-10-20T17:52:35.783179+08:00：1.7.2增强源码已普通推送到现有main，远程查询确认source `5b8013c9b67debff0b080da563781a39f6e69f74`，tree `7c0c112192ea337ab4515113c4c342375924e497`。
- [GitHub提交](https://github.com/wang546673478/engineering-workflow/commit/5b8013c9b67debff0b080da563781a39f6e69f74)；原staged与exact committed门禁全部通过，且verified_tree与实际Git tree一致。报告及hash保留在evidence.github_submission.receipt；没有复用历史任务批准。
- 托管CI状态不由本地检查担保；没有创建标签/Release、安装全局skill或恢复完整上游审读。本次回执只改记录与状态，交付内容/版本未变，不再升版。
