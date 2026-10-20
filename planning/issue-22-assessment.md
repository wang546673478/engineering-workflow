# 当前交付结果：三项增强已在本地实施

2026-10-20。用户在阶段性结论之后明确“那就按照这个增强的文档去实施”。原实施指引、交付收敛段、访谈指引中的三项增强，以及两个原模板和短入口已经写入；全局基线/模块图/契约/业务流和版本已同步。候选版本1.7.2 / Unreleased。

原正式TEST/COMPILE/GUIDANCE-COMPILE最终通过，skill结构、链接/版本/策略核验和S22同agent手工场景已完成；前两次缺解析器及后一次触及原时限的失败记录保留，补齐任务运行时依赖并诊断耗时后独立重跑原门槛，没有弱化验证。

这次完成的是三项本地增强。完整五仓库审读仍按用户决定延后，未读账本没有标完成；已安装skill、托管CI、提交与发布均不包含在本次完成声明。当前实际结果见[Task](issue-22-task.md)与[证据](issue-22-evidence.json)。以下“尚未实施”的阶段性表述为当时历史。

## 历史：当前文件读完后的阶段性判断

### 当时的阶段性结果：三项值得增强，尚未实施

2026-10-20。按用户最新“当前文件读完先给结果”的指令，已读完Spec Kit `src/specify_cli/presets/_catalog.py`；停止继续全量审读。当前累计366份文本完整审读，3,177份未读并暂缓，不能称任何未覆盖仓库已完整审查。输入仍为本仓库`868e496` / skill 1.7.1。

**结论：建议实施已定的三项增强，嵌入原有节点。三项目前都只有方案和执行授权，尚未写入skill规则与模板，未完成增强验证，也未更新全局安装。** 原skill已有一般复现定位、持续纠错和交付前收敛要求；“原本有原则”与“本次具体增强已实现”必须分开。

| 借鉴内容 | 已读依据与判断 | 加入自己的skill的位置 | 当前状态 |
| --- | --- | --- | --- |
| 缺陷证据和保持行为 | Spec Kit bug模板强调原复现、根因证据、前后结果与回归；agent-skills debugging和BMAD bug模板有同类证据纪律；Kiro公开资料区分应改/应保持行为 | 原implementation-workflow，复用Task/impact；按实际影响记录，不强制另建BUG文件或再批诊断 | 值得采用；未实施 |
| 更具体的交付核对 | Spec Kit converge的missing/partial/contradicts/unrequested可帮助发现遗漏；本skill本来已有四层核对与六步收敛 | 原baseline-linked-artifacts交付段，补差异分类、证据过期及归属；事实回Baseline、技术回Plan、执行回Task，目标/验收改变才重开Spec | 值得采用；未实施 |
| 可选需求与验收示例 | specs.md Simple模板含EARS五型/组合型；Gherkin grammar/compiler只提供语法/AST/pickle，不执行业务验收 | 原requirements-interview及原模板可选提示；提供中文等价句式与前置/操作/结果例子，沿用原REQ/AT | 值得采用；未实施 |

新读实现进一步支持原边界：artifact catalog/MCP能验证组成、标识符和协议，不能证明实现满足业务目标；bundle validate会将离线/不可达引用留作warning并允许ok；event找不到命令或脚本可return0；extension更新虽有备份和回滚，仍存在中断/部分成功及后续event刷新边界；preset update是先remove再add，失败不恢复旧版。它们是各自平台的实现选择，不能转成本skill必需检查的成功标准。

因此，本批借鉴证据纪律、差异分类和表达示例即可；自动hook、宿主调度/权限默认、bundle/preset安装系统、额外状态机和审核轮次均不纳入。无需复制这些平台的源码或引入其运行依赖。保持原流程、小修/恢复/空项目例外、已批准Spec边界和原TEST/COMPILE/GUIDANCE-COMPILE命令及强度。

来源锚点：

- [Spec Kit bug验证模板](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/extensions/bug/commands/speckit.bug.test.md) 与 [converge](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/templates/commands/converge.md)。
- [bundle引用验证边界](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/src/specify_cli/bundles/references.py)、[event执行边界](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/src/specify_cli/events/__init__.py)、[preset更新](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/src/specify_cli/presets/command_update.py)。
- 其余已审关键链路与固定SHA来源见下方原评估；逐文件笔记和hash见[证据](issue-22-evidence.json)登记的batch-02..29及原账本。

本次只核对源码和更新记录，未运行上游项目或新增强场景；记录/结构检查结果不能当作增强验收通过。原全量SOURCE验收仍未完成。本轮已按最新范围提供阶段性结果，不以剩余全量审读阻止该报告交付。

## 以下为原阶段性评估及历史范围

### 原评估：Issue #22已有能力、真实缺口与兼容方案

日期：2026-10-20（Asia/Shanghai）
输入：本仓库 `868e496` / 1.7.1；[Issue #22](https://github.com/wang546673478/engineering-workflow/issues/22)。
状态：**有源码依据的阶段性评估；五仓库全部逐文件语义审读尚未完成，不能作为完成该项前置要求或开始外部方案移植的证明。**
当前执行、授权、覆盖与后续工作以 [Task](issue-22-task.md) 为准。

后续状态（2026-10-20）：用户已认可三项增强方向并要求编写 Spec 供审核；当前需求草稿见 [SPEC-ISSUE22-ENHANCEMENT-01](issue-22-spec.md)。本文保留调查时的判断与证据范围；不再作为待审需求正文。外部完整语义审读的未完成状态保持。

执行继续（2026-10-20）：用户已授权完整Plan r1实施，并明确保持“先审完五仓库再实现”的原顺序。当前覆盖326份完整文本、3,217份待审；下面48份关键链路是原评估时的历史覆盖。新增源码审读及每批文件清单见evidence.execution_review_batches，逐文件语义结论保留在审读账本。尚无增强规则/脚本/模板或版本改动。

## 目前可确认的结论

值得补强缺陷证据和需求表达，但不应照 Issue 原方案增加三条独立流程。现有 skill 已有复现定位、事实纠错、四层联动和交付前收敛；问题是操作指引与证据结构仍可更具体，而不是完全没有这些能力。

保持原流程的适配方向是：在原调查/影响分析中整理缺陷证据，在原实施与验证中核验修复及保护范围，在原交付收敛中复查双向追踪；EARS / Given–When–Then 作为可选记法。是否开发新 CLI 不是本轮已确认的需要。新的机械必过项、状态机或三次人工批准不能以“只增不改”名义直接加入。

这不是“全部外部代码已经审读完毕”的最终采纳结论。当前没有修改 skill 指令、脚本、模板、测试、版本或已安装副本，没有回复或关闭 Issue。

## 本仓库已有能力

| 议题 | 当前实现 / 规则 | 真实边界 |
| --- | --- | --- |
| 缺陷诊断 | SKILL 要求复现与定位；implementation-workflow 要求源码/测试证据、先区分测试期望与实现错误，不削弱断言 | 没有统一的缺陷记录示例；checker 不验证每个缺陷的原复现与回归证据 |
| 文档与实现一起错 | project-documentation 的 continuous correction 和 Baseline 回流：测试、运行、源码调查可推翻当前事实，保留原结论及证据 | 当前声明式门禁不证明测试充分，也不证明需求本身正确；新增 verdict 字段也不能自动解决 |
| 收敛 | baseline-linked-artifacts 已有“交付前收敛”六步，核对源码、批准 Spec、Plan、Task、证据和 Baseline | 既有 checker 主要检查声明 ID、链接、文件、依赖、差异范围和真实命令结果；没有通用的业务语义证明器 |
| 结构化需求 | 现有 REQ/AT、追踪文档、artifact_links、模块审核、候选/确认/延后及实施状态分离 | 自由 Markdown 不等于无结构；句式模板仍可帮助表达触发条件、响应与可验证结果 |
| 缺陷工件注册 | documents.kind 只要求非空字符串；可以登记 defect 文档，ID 不是一个写死的 BUG / DOCUMENT_IDS 枚举 | 给文档增加 kind 不会自动产生缺陷语义检查，也不需要仅为此升级 schema |
| 小修路径 | workflow_lifecycle_gaps 中 proposal 豁免明确依赖 task.workflow_kind=small_fix | 用 defect 替换 small_fix 会破坏既有路径，须让缺陷分类与变更规模正交 |

来源：[SKILL](../SKILL.md)、[联动模型](../references/baseline-linked-artifacts.md)、[实施](../references/implementation-workflow.md)、[基线规则](../references/project-documentation.md)、[检查器](../scripts/check_project.py)。

## 五个外部仓库：版本与覆盖事实

| 仓库 | 固定提交 | 跟踪文件 | 文本 | 已完成的机械覆盖 |
| --- | --- | ---: | ---: | --- |
| github/spec-kit | f68ffcab37a253d42a226bc9bcf4fef451efa38c | 937 | 931 | 全文件清单、完整文本采集、SHA256、Python AST |
| cucumber/gherkin | 5a217be5b8dbd918d3ca0fa0f4ae3829346d73f1 | 1,004 | 1,001 | 同上及 JS/TS AST |
| addyosmani/agent-skills | aeac41d4d005999432bb7312f7ff06383a91d59d | 217 | 217 | 同上及 JS/TS AST |
| bmad-code-org/BMAD-METHOD | 61e01f82644c4bb533750cfa0d6d61ab61d2cc9b | 584 | 578 | 同上及 JS/TS AST |
| fabriqaai/specs.md | c9c2ba8e80b809787d80a202ee394e1c5847dddf | 859 | 816 | 同上及 JS/TS AST |

合计 3,601 个跟踪文件，3,543 个文本文件、765,404 行。58 个二进制是图片、动画、PDF 或签名资源，未当作源码精读。所有文本在足够预算下完整采集，没有因文件大小/总量/个数而省略；这是采集覆盖，不是语义理解覆盖。Python AST 无解析错误；314 个 JS/TS 文件、4,553 个函数/回调经 TypeScript 6.0.3 静态遍历，无 parse diagnostics；这不是类型检查或运行测试。

完整副本、逐文件哈希与仍为 pending 的语义状态保留在 ignored `work/issue-22-review/`。仓库均是 shallow clone，范围为固定提交的全部跟踪文件，不包括全部 Git 历史、未初始化外部子模块或整个生态。

## 已精读关键链路所得事实

### Spec Kit

- bug extension 的 assess/fix/test 是 agent 命令模板；产物是 assessment.md、fix.md、test.md。test 模板明确要求重跑原复现和相关测试，没跑原复现不能 verified。这个证据纪律值得借鉴。
- bundled bugfix/workflow.yml 在 assess 与 fix 之间另有一个人工 gate；GateStep 会在非交互环境暂停，CommandStep 调度宿主 CLI 并把退出码等写回运行结果。这是它自己的执行模型，不能照搬成我们每个小修都新增一次诊断批准。
- converge 模板不是 Issue 建议的“只读 checker”：它会追加 tasks.md，分类 missing / partial / contradicts / unrequested；不修改 Spec/Plan/产品代码。它依靠 agent 阅读代码和意图进行判断，不是通用可执行的源码语义对齐算法。
- test_converge_template_scaffold.py 明确说明只检查提示模板，不执行 LLM、不证明实际收敛行为；bundled workflow 测试核对步骤顺序与 gate。模板测试通过与修复已验证应分开。
- 它有 CLI、文件边界、integrations、认证、catalogs、extensions、presets、bundles、workflows、MCP 等完整平台。当前需求只涉及证据纪律，不需要引入这套平台或其自动 hooks。

证据：[bug test](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/extensions/bug/commands/speckit.bug.test.md)、[converge](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/templates/commands/converge.md)、[bugfix workflow](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/workflows/bugfix/workflow.yml)、[scaffold tests](https://github.com/github/spec-kit/blob/f68ffcab37a253d42a226bc9bcf4fef451efa38c/tests/test_converge_template_scaffold.py)。

### Gherkin

- 仓库包含 12 种语言的解析实现、共同语法、方言字典、生成解析器及共享 golden fixtures。主要链路为 token scanner/matcher → parser → AST builder → pickle compiler / message envelopes。
- gherkin.berp 允许 Scenario 的 Step*；Parser/Compiler 产生语法和场景结构，不执行业务步骤，也不要求每个场景按 Given/When/Then 具备完整因果意义。Python Compiler 处理 Background/Rule/Scenario Outline、参数替换、标签、步骤类型、表和 DocString；JS public API 暴露同类能力。
- 因此“写成 Gherkin”与“已有可运行验收”不同；还需要项目自己的步骤实现、断言和测试运行器。这里需要借鉴表达方式，没有理由引入多语言解析器或把解析成功当验收通过。

证据：[grammar](https://github.com/cucumber/gherkin/blob/5a217be5b8dbd918d3ca0fa0f4ae3829346d73f1/gherkin.berp)、[Python compiler](https://github.com/cucumber/gherkin/blob/5a217be5b8dbd918d3ca0fa0f4ae3829346d73f1/python/src/gherkin/pickles/compiler.py)、[JS API](https://github.com/cucumber/gherkin/blob/5a217be5b8dbd918d3ca0fa0f4ae3829346d73f1/javascript/src/index.ts)。

### agent-skills

- 已有 debugging-and-error-recovery：保留证据、复现、定位、缩减、修根因、防回归、端到端验证；有对应的行为评估 fixture。适合借鉴“原症状与根因证据分开”的表达。
- skill-lint / command / reference / artifact-path / version 工具核验的是 skill 结构、调用面和路径；run-evals 的默认层是词项相似度路由、碰撞、fixture/schema 及排名约束，另有显式选择的 headless agent 执行与 grader。它们不等于业务项目的 traceability 或 defect verdict 引擎。
- 当前 skills/scripts 中没有 systems-engineering-traceability 实现；Issue 引用 #103 属社区提案来源，不能仅凭 Issue 存在就列为已交付能力。该 Issue 网页已保存，API 后续遇到公开配额限制，未用凭据绕过，不影响本地仓库继续审查。
- 不采用其“遇到任何意外全线停止”、统一测试比例/提交粒度、强制 TDD 等规则作为本 skill 新默认，这些会覆盖我们按影响推进独立工作的现有规则。

证据：[debugging skill](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/debugging-and-error-recovery/SKILL.md)、[eval runner](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/scripts/run-evals.js)、[artifact validator](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/scripts/validate-artifact-paths.js)。

### BMAD-METHOD

- 此 SHA 的 main 是 V7 Preview Alpha；README 同时说明稳定 v6.12 是另外的源码线。比较必须固定版本，不能把一个分支的观察推广到整个产品历史。
- 当前 bug-template.md 已有症状、复现、原因假设、Given/When/Then 验收、缺陷与修复前后对比测试，以及“证据说明不需要改”的分支。ticket.md 区分假设与修复方案，要求缺陷票据保留复现和 cause hypothesis。
- build 与 build-auto 有验证缺口审查，明确以消费者可能观察到的回归和现有测试实际断言作为依据；不是仅有泛泛 QA。Issue 比较表对该版本不成立。
- setup/config/render、票据存储、知识记录、评估器和文档站都是平台本身的能力；不需要把其分步文件引擎、票据状态或强制 subagent 审核引入本 skill。

证据：[bug template](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-agent-po/assets/bug-template.md)、[ticket rules](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-agent-po/references/ticket.md)、[verification gaps](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build-auto/review-prompts/verification-gap.md)。

### specs.md

- 包含 Ideation / Simple / FIRE / AI-DLC 四条流程、installer 的宿主适配、CLI/TUI/Web dashboard 和 VS Code 扩展。不同流程不是同一套门禁，不能只凭 README 的综合描述判定某个功能已强制执行。
- Simple requirements 模板已有 EARS 五型及组合型；AI-DLC requirements 模板采用 FR、验收、优先级、故事引用和 NFR，并非所有流程都统一强制 EARS。
- artifact-validator.cjs 核验命名、ID 与文件名、引用存在和时间格式；--fix 可以改写部分字段。不能作为代码↔业务需求的语义收敛器。
- FIRE complete-run.cjs 接收 testsAdded/coverage 等调用参数，依据运行状态/phase 完成并同步 YAML/Markdown，有 --force 分支；没有通过这些统计值实际执行测试。这种完成记录不能替代本仓库已有的命令执行、Git tree 绑定和受保护批准。
- installer 中的 Kiro adapter 只是 steering 安装及 Simple specs 链接，不是 Kiro 产品 bugfix spec 的实现。

证据：[Simple template](https://github.com/fabriqaai/specs.md/blob/c9c2ba8e80b809787d80a202ee394e1c5847dddf/src/flows/simple/templates/requirements-template.md)、[artifact validator](https://github.com/fabriqaai/specs.md/blob/c9c2ba8e80b809787d80a202ee394e1c5847dddf/src/flows/aidlc/scripts/artifact-validator.cjs)、[completion](https://github.com/fabriqaai/specs.md/blob/c9c2ba8e80b809787d80a202ee394e1c5847dddf/src/flows/fire/agents/builder/skills/run-execute/scripts/complete-run.cjs)。

## Kiro 与 EARS 资料的边界

公开 [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs.md) 明确区分错误行为、期望行为、保持行为，以及诊断、设计、任务中的对应验证。值得参考其“哪些应该变化，哪些应保持”的记录方式。它沿用自己产品的需求/设计/任务阶段，不是对本 skill 新加相同阶段的理由。公开 [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first.md) 确认 EARS 与 requirements/design/tasks；本轮只验证公开资料，没有 Kiro 闭源执行引擎源码。

EARS 是帮助表达的记法，不证明需求无歧义。始终型只有系统与响应，不能因无触发条件报警；状态型、可选型、事件型、异常型和组合型的条件也不同。Gherkin 同理不能从关键词出现推断已经有有效测试。

## 对 Issue 原建议应做的修正

1. 将“缺失缺陷流程”改为“缺陷证据指引不够具体”；先复用 Task / impact / traceability 的同一权威条目，复杂缺陷才按项目需要拆文件。
2. 将“完全没有 converge”更正为“已有语义收敛规则，可增加更明确的差异归属与证据提示”。机械脚本只能输出其实际可检查的一致性，不能承诺 Converged 就证明业务正确。
3. 将 Spec Kit converge 标为可追加任务的 agent 命令，而不是只读 checker。若开发我们自己的只读诊断，它是新的本地设计，不是原样移植。
4. 更正 BMAD 比较并绑定源码 SHA；不给任何工具作“唯一/全部同类都没有”的无充分证据比较。
5. 保留 workflow_kind=small_fix 的规模语义；缺陷分类另记，不因 defect 取代规模而消除例外。
6. 新字段为可选不代表没有行为改变：若 handoff 从此强制要求新报告，就已经加了必过步骤。与用户“不改原流程”约束冲突。
7. schema_version 不为文档补强自动升级。当前 kind、impact 和 artifact_links 可承载记录；真正改变协议再设计迁移，旧清单默认行为保持。
8. 不能将 unsupported 理由作为 required 回归的豁免；必需项仍未满足。不能用文档彼此一致、verdict 自填或解析器通过推断修复成功。
9. converge 不依赖 EARS 才能工作：现有 REQ/AT/Task ID 与语义核验已经可以建立追踪关系；EARS 改善内容表达，不是完成收敛的逻辑前提。

## 保持原流程的候选接入方案

以下是待最终审读后定稿的具体方案，不是已实施或已批准的新功能。

| 位置 | 候选调整 | 保持性约束 |
| --- | --- | --- |
| requirements-interview + 原 Spec/Plan/Task 模板 | 增加可选 EARS/中文等价句式和 Given–When–Then 示例；有状态/来源/范围/AT | 不改历史需求、不重审已有效批准；新增原话与时间留在原记录 |
| implementation-workflow + 原 impact/Task 模板 | 缺陷记录包含症状/期望/实际、版本/环境、原复现、根因证据与假设、修复范围、保持行为、前后结果和残余风险 | 嵌入现有调查→方案→实现→验证；已授权修复不再要一次诊断批准；小修按影响处理 |
| baseline-linked-artifacts 的交付前收敛 | 显式核对缺失、部分、矛盾、无需求归属及证据过期；回到其权威层修正 | 不追加独立阶段；事实更正回 Baseline，技术调整回 Plan，目标变更才重开 Spec |
| checker / manifest / adoption | 第一批不改；后续仅在有明确机械检查需求时做独立设计 | 不新加 required，不更换执行合同、超时、输出上限、Git tree 验证和父版本控制面保护 |
| 文档和版本 | 若最终只澄清已有纪律，评估 PATCH；若提供可选新诊断能力，评估 MINOR | 实际 diff 决定，不因 Issue 建议直接承诺 1.8.0；沿原版本与控制面规则 |

候选验收包括：已有有效基线/恢复、小修、greenfield、缺陷未复现、测试无法运行、文档与源码一起错、修复改变保持行为、过期测试报告、EARS 始终型/组合型以及重复收敛不扩大已批准范围。程序测试验证真实 CLI/fixture 行为；提示规则需现实场景核验，不能仅匹配句子就宣称流程保持。

## 尚未完成

全部五个仓库的逐文件语义审读还没有完成，语义账本保持 pending；全量采集、AST 遍历、关键路径精读和本报告不替代该用户要求。外部项目测试没有执行，依赖没有安装；静态源码结论与运行验证分开。

下一步继续按覆盖账本检查每个模块及测试/生成来源，完成剩余代码语义记录后，再将上述候选改为最终采用/不采用结论。此前不移植外部实现，不宣称完成全部审读，不请求用户重复授权调查。
