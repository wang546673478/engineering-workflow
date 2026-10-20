# Technical Plan：工程流程增强，复用现有节点

Revision：`PLAN-ISSUE22-ENHANCEMENT-01`，执行修订 r2（技术增强范围沿用已确认r1）
日期：2026-10-20（Asia/Shanghai）
状态：**r2三项增强已完成本地实现与验证，1.7.2 / Unreleased；完整外部审读保留延后。**
输入 Baseline：`BASELINE-ISSUE22-01`，[当前全局基线](baseline-review.md)。
输入 Spec：`SPEC-ISSUE22-ENHANCEMENT-01` / r1，[需求正文](issue-22-spec.md)，内容保持原版。
源码：`868e4967512c2cd400307368d924291a3d4d8eef` / 1.7.1；本工作树已有 Issue 22 规划记录，未提交。
执行与进度：[TASK-ISSUE-22-REVIEW](issue-22-task.md)；证据：[issue-22-evidence.json](issue-22-evidence.json)；追踪：[traceability](traceability.md)。

用户本次“写plan和task吧,对照全局基线”授权按 Spec r1 编写实施计划和任务。按该版本规划不等于把其正式审核、完整方案批准或实施授权写成已完成；不得转用旧接入任务的批准。不新增审核节点，后续明确指令仍可按原规则覆盖其实际表达的批准范围。

历史执行批准（2026-10-20）：用户明确“开始实现吧”。依原SKILL的明确实施指令规则，本Plan r1及其Spec r1范围获本地执行批准；上述仅规划时的授权边界为历史。T22-02..07的完整单agent审读依赖保持；提交、推送、外部发布和全局安装不在批准范围。所展示版本哈希及原话见evidence的execution_start。

历史执行顺序确认（2026-10-20）：用户选择“保持原顺序，先审完五仓库再实现”。五仓库的完整单agent审读仍在T22-08..16之前；本Plan表中48/3,495是准备时快照，当前覆盖以Task/evidence为准。

历史执行调整（2026-10-20T16:46:28.078319+08:00）：用户明确“现在这份读完了给我一个结果,不要全部读完了,先看看这些那些可以进行借鉴”。Spec Kit presets/_catalog.py已经全文读完；本轮交付已读范围的借鉴结论，不再继续全部审读，也不冒称原P22-02完成。原技术范围与Spec正文不变；以下全量审读依赖为原计划记录，不作为本轮阶段性报告的前置。三项增强未实施、原验收待执行。

## 当前执行依据与r2调整

2026-10-20T16:55:18.904703+08:00，用户明确“那就按照这个增强的文档去实施”。结合上一条“不要全部读完了，先看看哪些可以借鉴”及已交付结论，本次按Spec r1和P22-03..08实施三项增强；P22-02/T22-02..07仍未完成并延后，不冒称全量审读完成，也不再作为本批增强交付的依赖。技术范围、原流程及验证强度不变，Spec正文哈希保持。原r1全文快照及哈希保存在evidence所指before-enhancement目录，以下早先全量前置表述作为原计划历史，由本段覆盖。

版本选择：本次是独立的兼容指引澄清批次，目标PATCH 1.7.2 / Unreleased；保留1.7.1 / Unreleased条目及其原缺陷事实，不伪造发布日期。

## 1. 全局基线对照与复用决定

下表是本计划使用的已有事实，不是目标实现。基线视图：B=Baseline，M=模块图，C=契约，D=数据库字典，F=业务流；均由当前工程清单定位。

| 基线事实 ID | 当前事实与证据入口 | 本次设计决定 | 关联 Spec |
| --- | --- | --- | --- |
| B22-01 | [SKILL](../SKILL.md) 已定义原阶段、模块审核、小修/greenfield/恢复、独立授权和自主纠错 | 保留主干；只在原节点补短提示与既有引用，不新建流程 | E01、E09 |
| B22-02 | [implementation-workflow](../references/implementation-workflow.md) 已要求影响分析、事实与测试期望核验及真实验证；[Task 模板](../assets/templates/spec-plan-task.md) 已有 evidence/impact 区 | 在原引用增加按需缺陷证据说明；模板只提示、引用同一事实 | E02～E04 |
| B22-03 | [linked-artifacts 的交付前收敛](../references/baseline-linked-artifacts.md#交付前收敛) 已核对四层与实际结果；[project-documentation](../references/project-documentation.md) 定义持续事实校正 | 扩展原收敛段的差异分类与归属，保留 Spec 冻结和自主回流 | E05、E06 |
| B22-04 | [requirements-interview](../references/requirements-interview.md) 与[决策模板](../assets/templates/decision-log.md) 已区分事实/候选/确认/延后、模块审核、需求与实施状态 | 原引用承载可选 EARS/中文与 Given–When–Then 示例；不改历史记录结构 | E07、E08 |
| B22-05 | [checker](../scripts/check_project.py) 的 `workflow_lifecycle_gaps` 用 `small_fix` 表示特定豁免；documents.kind 仅要求非空；[接入说明](../references/adoption-lifecycle.md) 保留旧清单兼容 | 不改 schema、workflow_kind、初始化或迁移代码，不增加 defect 状态/必填字段 | E01、E09 |
| B22-06 | [模块图](../docs/module-map.md)：instructions→checker→adapters；source-context 依赖 checker；tests 核验已有实现；governance 管理清单/证据 | 增强仍由 instructions 负责，governance 保存当前状态；不新增运行依赖或反向依赖 | E09、E10 |
| B22-07 | [契约](../docs/contracts.md)、[checker 说明](../references/checker.md)：命令 argv、超时、8 MiB 输出上限、Git 状态/tree 绑定、父版本保护和一次外部批准 | 保留脚本/检查声明/保护配置；文档仅澄清增强不是机械证明器 | E03、E09、E10 |
| B22-08 | [业务流](../docs/business-flow.md) 已覆盖讨论→影响→实施→验证→事实回写；[数据库字典](../docs/database.md) 声明无业务数据库，适配器只读元数据 | 更新实际受影响的说明与关联，数据库视图仅复核不适用依据，不编造表/接口 | E05、E06、E09 |
| B22-09 | [README](../README.md)、manifest、现有 tests/CI 是规定验证来源；VERSION/SKILL/README/openai.yaml 同步；1.7.1 在 CHANGELOG 中仍为 Unreleased | 沿原验证/版本机制交付，保留1.7.1未发布事实；本次写计划不升版 | E10 |
| B22-10 | [外部证据](issue-22-evidence.json)：五仓库3,543份文本、已完整审读48份，其余3,495份待审 | 完整调查列为本任务前置工作；不以索引/AST 替代审读，不把它变成 skill 对所有项目的新增门槛 | 原 SOURCE、DECISION；E09、E10 |

有效性边界：本次复核本仓库既有源文件、当前文档与测试入口，不重认证历史托管结果；旧审阅只覆盖其原版本。外部完整语义审读尚未完成，所以本计划可以编写、审核，最终借鉴结论和依赖其证据的实施保持未完成。

## 2. 目标组织方式与权威归属

继续使用 `Baseline → Spec → Plan → Task → Code/Evidence → Baseline`。

| 内容 | 唯一规则正文 | 项目记录去向 | 使用者 |
| --- | --- | --- | --- |
| 缺陷证据、原因与修复结果 | `references/implementation-workflow.md` | 原 Task / Issue / 影响分析；允许相互引用 | 执行调查、修复、验证的 agent |
| 收敛差异分类与回流 | `references/baseline-linked-artifacts.md` 的原收敛段 | 原 Task / traceability / Baseline 纠正记录 | 实施与交付核对 |
| 可选需求与验收记法 | `references/requirements-interview.md` | 原 Spec / 决策/验收记录 | 需求讨论与模块审核 |
| 短入口与公开说明 | `SKILL.md`、README 只做路由和范围解释 | 不另存一份规则 | skill 发现、加载及维护者 |
| 可选使用提示 | 原 spec-plan-task / impact-analysis 模板 | 按需合并到已有记录，不要求迁移 | 新项目、恢复或实际需要补记录的项目 |

不增加独立 defect-flow/convergence/notation 文件，因为这三项有既有权威段落可扩展。后续若内容规模确需拆分，只调整技术文档组织及链接，不复制规则或增加阶段；保留本计划的批准范围。

缺陷的“报告/诊断/修复/验证”是原任务的证据信息，不写入新的阶段枚举。使用已有状态词并给出证据；不新增统一 verdict 协议。EARS 是表达示例，收敛分类是核对方法，均不驱动新自动状态机。

## 3. 实施项与依赖顺序

下列是本批交付的工作分组，**不是新增给采用项目的流程阶段**。具体进度和可执行动作以 Task 中 T22 编号为准。

### P22-01：绑定事实基点及保持性对照

- 依据：B22-01～B22-09；需求/验收 E01、E09、E10。
- 工作：保存真实源码、工作树、Spec r1及工具/清单关键内容的哈希；对照原阶段、例外、批准、授权、完成、命令合同；检查已有未提交规划记录。
- 复用：当前 Baseline/M/C/D/F、清单、原测试，不替换。
- 产物：本 Plan 的全局对照、Task 和现有 evidence 中的输入快照；明确当前未验证范围。
- 当前：本次计划准备已完成静态对照、证据/链接、需求覆盖、依赖和策略保持核验，结果见evidence的plan_preparation.validation；未来实施启动时按实际版本检查新鲜度。

### P22-02：原五仓库完整调查（当前延后，不属于r2交付依赖）

- 依据：B22-10；原 REQ/AT-ISSUE22-SOURCE、DECISION，E09、E10。
- 按固定 SHA 的逐文件 pending 清单，分别完成 Spec Kit、Gherkin、agent-skills、BMAD、specs.md 的实现/测试/配置/行为模板审读；生成代码核对生成来源和差异，不能仅扫目录或读公共祖先后自动标记所有文件。
- 各文件保留原 SHA、审读范围、职责/消费者/边界和与本任务有关的结论；二进制保留已列原因。大体积账本在 ignored `work/issue-22-review/`；可审阅结果和覆盖摘要回写已有 assessment/evidence。
- 合并五仓库证据，明确借鉴证据纪律/表达思路与不采用的执行模型；如发现推翻现有目标的事实，只更新受影响依据和方案，不擅改冻结 Spec。
- 继续单 agent，不另装外部执行平台、调用外部模型或运行其生产流程；不复制外部源码。本批若确需借用实质文字/代码，先核对来源、许可证和实际范围并更新影响，不默认获得新权限。
- 依赖：独立调查已有授权，无需再请求“继续”；完整来源调查及其结论未完成时，不能把本任务的借鉴完成或依赖它的增强交付标为完成。

### P22-03：在原调查/实施引用中补缺陷证据

- 依据：B22-02、B22-07；REQ/AT-ISSUE22-E02、E03、E04，并满足E01。
- 在 `references/implementation-workflow.md` 的原调查、影响与验证内容中，增加症状/期望/实际、版本/环境/原复现、原因证据与假设、修复范围/保持行为、前后结果/回归/限制的按需指引。
- 明确“未复现/无法验证”不等于无问题；适用的受控等价核验说明差异；诊断不自动授权修复，已授权修复不另要一次诊断批准。
- 复用原 Task/impact，不添加 `BUG` 必需文档、assess/fix/test 命令、模板完整度校验或全任务强制回归测试。继承项目验证规则与已声明必需项的失败语义。
- 验证：S22-02～S22-04（见第6节）；关联 B/M/C/F，D 仅按真实任务影响适用。

### P22-04：在原交付段扩展收敛分类与归属

- 依据：B22-03、B22-08；REQ/AT-ISSUE22-E05、E06，并满足E01。
- 扩展 `references/baseline-linked-artifacts.md` 的“交付前收敛”，覆盖缺失/部分/矛盾/本次无归属实现/证据过期；核对本批及受影响调用链，保留未来/延后范围。
- 差异回到现状 Baseline、技术 Plan、执行 Task；业务目标/权限/验收改变才重开 Spec。无归属实现先调查依据，不自动补造需求或删除代码。
- `references/project-documentation.md` 如需互链只加指向权威段落的提示，不复制分类。记录沿用 Task/traceability，不产生新报告、`Converged` 必过字段、收敛轮次或自动追加任务引擎。
- 验证：S22-05、S22-06；关联 B/M/C/F，数据库视图仅在实际 schema 影响时回写。

### P22-05：在原访谈引用中增加可选表达示例

- 依据：B22-04；REQ/AT-ISSUE22-E07、E08，并满足E01。
- `references/requirements-interview.md` 增加 EARS 五型及组合型中文等价示例，说明始终型不需要独立触发条件；用一个有前置状态、操作、可观察结果的 Given–When–Then 例子说明验收。
- 不从示例引入未确认产品规则；保留原格式、历史文档、REQ/AT、来源/状态及模块审核。句式正确不等于需求获批、可执行测试或业务正确。
- 不增加解析器/lint、测试框架、统一英语关键词、必填结构或规范迁移。
- 验证：S22-07、S22-08；关联 B/M/C/F中的说明，不改变运行契约。

### P22-06：路由、模板与全局视图同步

- 依据：B22-01～B22-08；REQ/AT-ISSUE22-E01、E02、E05、E07～E10。
- `SKILL.md` 在现有“缺陷先复现并定位”“联动/完成”等节点仅补简短适用提示，引用 P22-03～05 既有资料；README增加简短增强说明及适用边界。
- `assets/templates/spec-plan-task.md` 在已有影响/验证处补按需线索，并链接已扩展的规则；`assets/templates/impact-analysis.md` 在 failure/recovery 处补“若属缺陷”的可选提示。示例不设必填表单，已有模板完全可用。
- `assets/templates/decision-log.md`、managed AGENTS 模板、adoption/initializer/helper、manifest示例和 hooks 默认复用且不改；它们已有状态/授权/入口足够。不为表面“全覆盖”重复加规则。
- 更新本仓库 `docs/module-map.md`、`docs/contracts.md`、`docs/business-flow.md`、Baseline 当前事实及追踪：说明增强的职责、信息流和“无新CLI/协议”边界；事实只在实际实施后更新，不提前写成已实现。
- 数据库字典、数据库/契约源清单、适配器、source-context不改。Task影响记录写明检索依据及不适用理由；如实际改动超出这些边界，先按原规则重新分析。
- 在**本仓库维护任务**原 `documentation_impact` 体系内补齐实际指令/模板/版本路径的原同步门槛；不新增项目级必过项、不减少旧检查、不改外部项目清单。
- 验证：S22-01、S22-09；结构/引用/影响检查与全局链路人工语义核验。

### P22-07：用真实场景核对流程保持性

- 依据：B22-01～B22-08，全部 E01～E10；现有 tests 只证明工具行为，不能证明 agent 总会遵循文字。
- 先确定第6节合成场景的输入和可观察判断，再用最终指令/模板在任务局部 fixture 推演并核对实际产物：是否重复要求批准、另建台账、扩大任务、误标成功、强迫迁移旧格式等。
- 单 agent 执行与复核，明确不是独立 agent 或跨模型验证；记录实际行为和限制，不仅检查规则句子/标题是否存在。不调用 headless 模型或新工具作为隐藏依赖。
- 复用原 `scripts/tests/test_checker.py` 中 small_fix/greenfield/review-reuse/handoff/skip/control、`test_adoption.py` 旧清单和已有映射等回归；无新运行代码时不新增文案匹配测试。若场景暴露真实程序缺陷，只记录并分析其与本范围的关系，不擅自扩大本增强实现。
- 产物：同一 evidence JSON 中逐场景输入/观察/判断/源码哈希；fixture大文件留ignored目录。缺证据的场景保留未验证。

### P22-08：原验证、版本与交付闭环

- 依据：B22-07、B22-09；REQ/AT-ISSUE22-E09、E10。
- 在任务局部、与CI兼容的 Python3.11环境准备原锁定解析器依赖与Node/TypeScript；执行原 `TEST`（120秒）、`COMPILE`（30秒）、`GUIDANCE-COMPILE`（30秒），不改命令、时限或skip策略。工具可用性先诊断，保留正式失败与后续诊断的区别。
- 执行skill-creator quick_validate、`git diff --check`、本任务 `change --run-checks` 和场景核对。正式报告关联实际 source/worktree/环境；只补回执且受验证内容未变时不重复无关全量回归。
- 版本初步分类：现有纪律的兼容指引/可选示例澄清，按 PATCH；以当前1.7.1为输入，独立交付候选1.7.2。**1.7.1仍Unreleased**，实施时先核对是否属于同一未发布批次，按原批次规则合并或保留下一PATCH，不伪造发布日期；本次计划准备不改任何版本文件。若最终出现新运行能力/不兼容项，重新评估范围与版本，不能强称PATCH。
- 升版时同步实际权威 VERSION、SKILL metadata、README版本位、`agents/openai.yaml`现有version和CHANGELOG；不重生成/覆盖其他元数据。
- 本地完成结果可交付；暂存/commit/committed、推送、安装或托管运行仅在已有授权覆盖时执行。受保护成品按原控制面审阅，不因“用户让写计划”注入批准变量。精确提交验证始终针对实际SHA，托管结果独立记录。

## 4. 文件级影响与同步门槛

| 类别 | 计划触达 | 原文复用与更新方式 | 本批边界 |
| --- | --- | --- | --- |
| 实施/收敛/需求规则 | implementation-workflow、baseline-linked-artifacts、requirements-interview | 各自现有章节扩展，单一权威 | 不新建三条流程 |
| 短入口/说明 | SKILL、README；project-documentation按互链需要 | 短路由/限制说明，减少重复 | 原主干与例外保留 |
| 模板 | spec-plan-task、impact-analysis | 原字段内可选提示 | 不迁移存量、不增加必填 |
| 全局视图 | Baseline、module-map、contracts、business-flow、traceability | 按实际实现刷新，历史保留 | 目标与事实分开 |
| 工程清单/本Task | active pointers、documents、链接/状态、实际documentation_impact | 复用schema1/原门槛、同任务记录 | 不改check/control/dependency政策 |
| 版本 | VERSION、SKILL、README、openai.yaml、CHANGELOG | 交付前依据最终批次同步 | 计划阶段不升版 |
| 保持原样 | checker/collector/适配器/接入脚本、源码清单、manifest示例、CI/hooks、数据库字典 | 检查原合同及不适用依据 | 无新命令/新依赖/DB迁移 |

所有受影响调用链/职责说明与实现同批同步；没有数据库变化不免除数据库边界复核。`documentation_impact`仅描述这些现有义务，不是本增强发给所有项目的新规则。

## 5. 兼容、失败及恢复设计

- **旧记录兼容**：任务可以沿用旧Task/Spec/模板，不因升级补全历史缺陷/EARS；当前需要的事实引用现有资料即可。
- **同一修复规模**：小缺陷仍是small_fix，复杂/跨层缺陷按已有影响选择；不因“缺陷”一词改动阶段。
- **权限和数据**：没有产品权限、计费、数据库写入、后台任务/缓存、新远程集成；调查资料不授予工具执行权限。
- **事实冲突**：先查证并回写Baseline/关联资料，必要时只暂停依赖错误前提的部分；不因批次未结束阻断独立调查。
- **需求冲突**：Spec r1目标/验收变化才形成后继revision；普通技术调整在Plan/Task更新，保留原审阅范围。
- **局部编辑失败**：按工作树与输入哈希核对未完成文件；保存现有变更，不覆盖/重置已存在工作。恢复读本Task的当前状态，继续未完成步骤。
- **返工/恢复**：若补强导致新增门禁/重复确认，修正本批指令/模板到已批准边界，重做受影响场景和检查；保留失败证据。不以降低既有检查换成功。
- **回退**：本批无数据迁移；必要时对具体内容做经核对的反向编辑，保留用户已有记录及历史。提交后的恢复按实际授权与原Git规则；不预授权reset/force push。

## 6. 场景与验证映射

| 场景 | 输入与观察点 | 对应验收 | 证据类别 |
| --- | --- | --- | --- |
| S22-01 原路径 | 首次接管/小修/greenfield/有效基线/恢复/一条指令授权；比较输入相同情况下是否选原路径 | E01、E09 | 原工具回归+指令应用记录 |
| S22-02 复用记录 | 小缺陷已有原Issue/Task与复现日志；应直接引用，不因缺文件/表单要求补建 | E02 | 实际fixture文档与行为记录 |
| S22-03 证据不足 | 未复现、环境缺失、只有无关测试、旧SHA报告、文档与代码共同错误 | E03 | 结果判定与限制，不能标verified |
| S22-04 适度验证 | 行为修复已有回归；文字/链接小修；受控等价环境；确认选择相称验证，不强制TDD | E04 | 测试/核验复用与实际结果 |
| S22-05 范围收敛 | 本批缺失/部分/矛盾/无归属，混有未来与延后需求；只处理实际范围 | E05 | 追踪差异与任务范围前后对比 |
| S22-06 正确回流 | 事实更正/技术细节/新验收/无归属实现/必需检查受限 | E06 | 对应权威层变化与保留批准证据 |
| S22-07 可选句式 | 五型+组合、中文原格式、始终型无事件、未确认示例规则 | E07 | 需求含义与未确认状态核验 |
| S22-08 验收表达 | 前置/操作/结果与REQ/AT关联，未安装运行器 | E08 | 可读验收而非声称自动执行 |
| S22-09 旧项目/执行合同 | 旧清单/模板/agent入口、无新增字段/命令、checks/control/exclude/依赖对比 | E09 | 真实声明/文件diff+既有回归 |
| S22-10 一致性交付 | 当前规则/模板/全局视图一致，正式检查/场景结果与源码绑定，版本真实 | E10 | 原门槛+文档/语义/版本证据 |

本批已按Task记录的Python3.11与锁定依赖环境执行原检查；以下命令是已运行记录，复核时需选择新的报告路径（检查器拒绝覆盖报告）：

```text
python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base 868e4967512c2cd400307368d924291a3d4d8eef --task TASK-ISSUE-22-REVIEW --run-checks --report work/issue-22-review/enhancement-change-ready.json
python -X utf8 C:/Users/54667/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

上面的skill-creator路径是本机本次实际来源，移到其他机器须定位可用来源；不写入交付skill的通用规则。实施起点变化时显式重核base，不用旧报告覆盖新源码。提交相关模式沿 [checker](../references/checker.md) 原合同，只在实际提交工作被授权时执行。

## 7. 计划完成与待办边界

本轮 Plan/Task 准备的完成依据：事实对照可追溯；10组增强REQ/AT全部映射到Plan项与可执行Task；未完成外部审读保持开放；链接和状态一致；现有实现/策略未被计划编写改动。

r2增强实施的完成依据：已读范围的来源结论支持本批三项，完整调查依用户决定延后；已具备适用的原方案/实施授权；实际交付与Spec一致；受影响基线视图刷新；场景核对及原必需检查满足；版本和CHANGELOG真实。不能拿计划写完、一次结构检查、模板关键词匹配或历史测试替代。

当前结果：P22-03..08及本批原检查/场景/全局视图/版本同步完成；来源完整调查P22-02仍延后，未声明全量借鉴审查完成。原完整前置依赖为r1历史，由用户明确指定r2在已读结论上实施。验证与限制见当前Task/evidence。
