# TASK-GITDIAGRAM-ASSESS-01：GitDiagram局部代码功能调研

## 当前状态

- 日期：2026-10-18（Asia/Shanghai）；阶段：源码能力调查、相关上游测试、受控验证和本项目既有门槛完成，研究complete；正式接入未授权。
- 用户原话：“先记录下来,然后调研 https://github.com/ahmedkhaleel2004/gitdiagram 这个仓库,做法和调研gitingest一样,不影响现在skill的流程下,看看那些功能适合接入”。授权：完整源码研究、受控试验和记录；正式接入not_authorized。
- 已先记录省Token展示原则：优先精简行号/重复来源标记、按需展开；保留所选源码、完整清单和遗漏原因；现有流程/审核/验证继续。上一轮临时试验Task保留该记录，不修改正式SKILL或候选程序来冒充已实现节省。
- 工作流来源：本仓库SKILL.md，1.5.0 / c21e715及现有工作树；输入Baseline为BASELINE-LINKED-02，产品Spec/Plan原批准边界不变。本文件合并本轮研究Spec/Plan/Task/影响/证据，候选功能不写成已批准需求或已实现事实。
- 对照：Gitingest研究与Pi隔离试验，后者候选已移至C:/Users/54667/.codex/experiments/gitingest-pilot-pi-20261018/engineering-workflow以避免宿主列入skills目录；报告/原始证据仍在原work试验根。
- GitDiagram来源：main `310e2e696b1953cec0e76560cad5e9cd7ca5d964`，2026-10-14T01:20:09Z；GitHub branch API与clone一致，package.json版本0.1.0，MIT。源码位于C:/Users/54667/.codex/experiments/gitdiagram-assessment-20261018/upstream；工作树无源码改动，不执行上游生产服务或模型调用。
- 当前结论：值得选取源码引用线索、关系出处/未核验状态、结构化图校验、确定性Mermaid及文字视图输出；不能把正则引用、路径存在或图合法当成业务关系已证实。保留四项Gitingest候选，GitDiagram在其上增加可核对的关系视图，未来接入仍需用户决定。
- 下一步：用户审阅本报告的功能选择、范围与限制；如之后授权，再形成适用试验/接入方案。没有自动实施或发布动作。

## 研究 Spec（ASSESS-GITDIAGRAM-01）

- REQ-GITDIAGRAM-ASSESS-01：调查GitDiagram全部主要功能，区分确定性代码能力、模型推断/提示、展示与托管服务；挑选能为现有调查、模块地图、契约和影响分析补充的代码，不改流程顺序/审核/验证职责，与已有Gitingest候选去重。
- AT-GITDIAGRAM-ASSESS-01：固定来源revision和许可，提供实际源码路径/调用链、适用本地/外部模型条件、测试与受控复现；给出功能通俗说明、优先级、局部复用点、代价/风险、缺口与未验证项、低Token展示边界和候选接入形态。源码或测试可回答的问题由agent调查，不将未知功能效果转交用户猜测。
- 研究不是对上游业务系统的正式接管、生产认证或对本skill的实现授权。用户后续决定是否试验/采纳。

## Plan / Task

| 项 | 动作 / REQ和AT-GITDIAGRAM-ASSESS-01 | 状态 |
| --- | --- | --- |
| GD-01 | 恢复规则/基线/近期决定，记录省Token原则与来源 | complete |
| GD-02 | 固定上游版本，能力/入口/依赖/消费者/许可盘点 | complete |
| GD-03 | 相关既有测试、确定性函数与边界fixture验证 | complete |
| GD-04 | 对照已存在能力，形成局部代码复用矩阵与建议 | complete |
| GD-05 | 权威记录、引用/影响、项目既有门槛及交付 | complete |

## Skill review

- 清单来源：本会话Skills catalog；检查日期2026-10-18；范围由Gitingest候选讨论切换为GitDiagram仓库源码研究。
- adopted：engineering-workflow，来源本仓库SKILL.md，1.5.0 / c21e715；用户沿用流程，已重读正文、AGENTS、manifest/当前任务、基线/Plan/模块地图，project-documentation、requirements-interview、implementation-workflow、checker、baseline-linked-artifacts适用条款。
- not-adopted：skill-creator，C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md，版本未提供；本轮只调研，不创建/更改skill行为；沿用上一轮已读指导，不启动实施。
- not-adopted：planning-with-files，C:/Users/54667/.agents/skills/planning-with-files/SKILL.md，版本未提供；现有manifest和本Task是唯一研究状态，不新增重复台账。
- not-adopted：design-an-interface，C:/Users/54667/.agents/skills/design-an-interface/SKILL.md，版本未提供；本轮不是多个接口方案设计。
- not-adopted：visualize:visualize，C:/Users/54667/.codex/plugins/cache/openai-bundled/visualize/1.0.50/skills/visualize/SKILL.md，版本1.0.50（清单路径）；当前评估图形工具代码，不需要制作独立可视化产品。
- 其他未采用项以当前清单描述筛选；无适用则不加载。若进入图形交互、特定文档产物、模型API实际调用或正式实施，先重新review适用技能/影响和授权。

## 影响与版本

- 只更新研究文档、manifest任务注册/活动指针和traceability；正式SKILL、引用规则、脚本、模板、VERSION、CHANGELOG、门禁必需命令和保护集合不改。
- 当前模块连接、契约、数据库和业务流实现无变化；对产品MAP/CONTRACT/DB/FLOW更新不适用，研究事实作为有revision的附件。默认所有未来功能均为候选，不转移历史批准。
- 无升版：本轮是研究/状态与证据记录，不改变正式交付行为。无提交/推送/部署/外发消息。

## 研究结论

**GitDiagram最值得借鉴的是“把源码线索和已有分析整理成有出处、可校验、可展示的关系视图”。**它比Gitingest多了关系提取与图形输出代码；现版本的源码引用分析主要用正则、文件名和路径规则，生成架构关系的核心仍包含模型推断。它的图AST指结构化图数据，不是源语言的完整语法树。不能据图已生成就跳过本skill的全局调查、源码语义核验或用户审核。

用户已要求记录的省Token方向继续有效：优先缩短重复展示，完整证据留在清单，所选源码与遗漏保持可追溯；不通过删除必要调查来省Token。GitDiagram的默认源码抽样与过滤策略有明确局限，不能直接成为本workflow的完整基线采集策略。

## 实际结构与主要能力

本版本是一个Next.js16/React19/TypeScript应用，Bun1.3.14管理依赖，不是早期FastAPI后端形态。根CLAUDE.md、README、docs/architecture、源文件与测试相互对照。对generate、diagram、mcp、generation组件四个直接相关目录的71个非测试模块建立定义/hash索引，深入阅读关键流程；视频/运维/账务等按入口、配置、调用方和存储边界盘点。本轮没有声称逐文件接管整个生产项目。

核心流程：

1. `github.ts`获取GitHub默认分支、目录树、README及blob元数据；公开树有ETag缓存，过大的递归树可补最多8个缺失顶层目录的一层内容，保留treeTruncated；这不保证已还原完整深层树。
2. `repository-context.ts`按路径/文件名/大小及目录多样性排序，选择12个候选摘录文件、最多28个引用读取、20个仅列名文件。模型侧树最多24000字符，README最多8500字符。
3. `source-context.ts`读取有大小和Git blob哈希校验的正文，公开raw与私有API路径分离；限512000字节/文件、6并发、12秒采集预算。生成摘录、已读/未读索引及引用线索，总source context最多48000字符。
4. `stream/route.ts`及`graph-planner.ts`调用模型生成overview/结构化图；默认合并输出与配置下的两阶段路径并存。最多3次图尝试，部分无效路径可直接清空而不再调用模型。模型客户端、定价、配额不是本轮拟接入部分。
5. `graph.ts`验证IDs、分组、边端点、路径；`applyEdgeEvidence`检查或补文件出处；compiler将结构化数据确定性转Mermaid。图中路径与关系仍须语义审查。
6. 浏览器做Mermaid源码/链接过滤、SVG清理和链接二次约束，提供缩放、拖动、点击源码、关系列表、复制、PNG/Mermaid/README导出。readout/Markdown与图共用结构化数据。
7. R2持久化公私图，Redis负责配额、取消、失败记录与分布式写锁；SSE输出进度、失败阶段和最终结果。公共MCP只读既有公开图/名称搜索/已有视频，不会直接生成新图。视频、计费/赞助/分析、管理台和Workers部署属于独立产品配套。

## 值得选择的局部代码功能

以下为agent建议，未获正式采纳或实施授权。

| 功能 | 通俗解释与实际局部代码 | 现有流程落点 | 判断 |
| --- | --- | --- | --- |
| **源码引用关系索引** | 找出“这个文件引用了哪些文件”，为调查提供起点；`source-references.ts/createReferenceResolver` | 基线模块调查、调用方查找、改前影响分析 | **值得适配**。输出必须标为引用线索，并补语言/项目配置识别；不是调用图或完整依赖证明 |
| **关系出处与核验状态** | 让每条箭头旁能找到来源文件，缺出处时明确显示推断/未核对；`edge-evidence.ts`、`connection-rows.ts`、`diagram-connections.tsx` | 模块地图、业务流和影响记录 | **优先借鉴**。字段/展示有价值；上游自动补出处规则需更严格，不能直接沿用“有文件=关系正确” |
| **结构化关系图和机械校验** | 先保存模块/连线数据，再查重名节点、断开的引用、未知分组和不存在路径；`features/diagram/graph.ts`、`generate/graph.ts` | 已有分析结果的可选输出与自检 | **值得接入**。只校验图数据，不新增基线批准条件或取代当前checker；固定34节点/48边限制要按视图范围调整 |
| **确定性生成Mermaid关系图** | 将已核对的同一份关系数据稳定画成图，减少反复让模型写图语法；`compileDiagramGraph`及标签转义 | 模块地图、业务流的可选图形视图 | **优先借鉴**。不需要照搬模型API流程；本地源码与来源版本链接需要适配 |
| **同份数据生成文字/关系表/Markdown** | 图给人看，模块与关系可用紧凑文字给agent读取；`readout.ts`、`markdown.ts`、`connectionRows` | 用户审阅、文档维护、恢复与交接 | **优先借鉴**。一次只按需要输出，避免图、长说明和表格重复进入上下文；保留完整事实与证据 |
| **节点和关系关联源码位置** | 看见模块或箭头时，能定位相应文件；`buildGitHubUrl`、`evidenceUrl`、`diagramSourceLinks` | 调查证据回查 | **值得适配**。上游主要生成GitHub分支/HEAD链接；需要本地路径、行段、不可变revision/hash映射 |
| 阅读顺序/目录多样性建议 | 先看入口、调度和核心服务，避免一个目录占全部阅读预算；`rankSourcePaths` | 现有源码盘点之后的阅读安排 | 可借鉴排序，不采用其排除测试/迁移/配置及抽样数量作为基线覆盖规则 |
| 分段摘录与紧凑来源索引 | 只标每段起始行、显式说明间隙；区分excerpt/read/not-read，列引用摘要；`excerptSource`、`formatSourceIndex` | 可选预览/大文件导航 | 有展示思路，但**不作为当前默认完整阅读包方案**。它实际省略正文，与“所选文件先完整保留”有边界差异 |
| 渲染/导出安全约束 | 文本转义、GitHub链接限制、SVG清理；`mermaid-security.ts`、`mermaid-config.ts`、`export.ts` | 若未来增加独立HTML图形浏览器 | 随渲染方式采用。仅生成Mermaid/Markdown时不必引入整个React应用；自行渲染时须保持多层约束 |

### 推荐的最小组合

在已有Gitingest四项候选之上，先考虑“引用线索和出处清单 → agent按原流程核验关系 → 一份结构化关系数据 → 按需生成Mermaid或紧凑文字”。目录盘点、路径安全、源码hash、读取限额继续复用现有能力；不再搭一套GitHub下载/过滤/缓存来重复本地采集。

核心是辅助代码与输出视图。不会加入新的常规访谈/审批阶段，不因图合法就将Baseline标complete，也不为画图另发固定的模型请求。正式集成前，需在已有Spec/Plan/Task中确定字段、状态、引用解析覆盖与文档落点，并更新实际受影响的模块/契约/业务流视图。若新增图检查作为强制门禁，属于另一个明确控制规则决定；本轮没有提出或批准该变化。

## 实测与能力限制

### 相关上游回归

- 在未修改源码的固定commit上运行18个相关测试文件，**208项通过、0失败、0跳过**（8.365秒）。涉及引用、摘录、读取/排序、GitHub边界、图解析/编译、图重试、紧凑输出、读出/Markdown、安全链接、导出/关系列表与MCP文本。
- 这是选定功能测试，未运行全部应用门槛、Workers、实际R2/Redis、线上部署、真实模型/视频或浏览器全链认证。上游测试中的外部边界用替身；测试子进程移除了相关凭据环境变量，没有调用付费模型。
- 环境：Windows，Node24.21.0、Bun1.3.14；上游CI声明Node22，因此不将本机结果扩展到所有平台/Node22。按bun.lock frozen和ignore-scripts局部安装；未运行prepare钩子/部署脚本、未改全局配置。
- 首次安装在原镜像缓存的patched minimatch重命名处遇ENOTEMPTY；保留失败日志，使用新局部缓存、官方registry、copyfile和单网络并发重试，冻结版本/patch保留后成功。上游git status为空，lock/source未改。不是通过删除patch或降级断言获得通过。

### 受控函数与Pi源码观察

| 编号 | 真实运行的输入/结果 | 对接入的含义 |
| --- | --- | --- |
| DG-01 | JS普通相对import解析到正确文件；同样语句放在注释或字符串中也被解析成依赖 | 正则是线索，需过滤注释/字符串或用语言语法解析，再人工核验 |
| DG-02 | 自定义tsconfig别名、变量动态import、包名与目录不同的workspace导入未解析 | 必须读项目真实配置和package映射；不支持项保留未知，不能默认为无依赖 |
| DG-03 | Pi1941文件上，read.ts提取7个本地引用、args.ts提取3个、agent-loop.ts提取2个；@earendil-works/pi-*跨包引用未由该规则补齐 | 说明在真实多包项目有局部用途，也存在可观察缺口；不是完整准确率/召回率评分 |
| DG-04 | `applyEdgeEvidence`在引用方向相反的图边上仍能补出处；无引用时只因文件属于节点也能保留出处；README可不在readPaths中仍保留 | 出处是候选材料，不证明边的方向、动词、业务作用或README具体陈述成立 |
| DG-05 | 重复节点ID被拒；未知路径被识别，但清空path后图仍可接受；孤立节点/环也可合法 | “图验证通过”是结构/路径契约；并不证明模块连通性、无循环、所有节点真实或业务正确 |
| DG-06 | 普通图和含引号/脚本形文本/反引号等标签的图均由真实Mermaid parser接受；输入被转义，URL固定GitHub | compiler是可独立复用的确定性能力；若展示原始模型Mermaid，仍需配套清理/链接约束 |
| DG-07 | 图节点链接使用传入main，关系链接用HEAD；生产调用传githubData.defaultBranch而非固定commit | 链接可随分支变化；工作流需要绑定已调查版本和本地来源 |
| DG-08 | rank/filter排除了测试、迁移、lock、tsconfig等；Pi前12还包含testing目录的辅助代码；tree上下文截到23984字符并标partial | 名称/路径启发式可能遗漏关键调查材料或误排优先级；不能替代全局盘点与项目语义核验 |
| DG-09 | 10817字符fixture在1400预算下摘录1058字符，带省略标记；budget=5时fallback返回27字符 | 长文件分段有导航价值，但并非保留全文；极小预算也不总是严格输出长度上限，不能照搬资源保证 |
| DG-10 | 紧凑图fixture由382字符JSON变287字符，补默认字段后仍符合图契约 | 可借鉴删除冗余字段，但只是一个fixture的字符观察，不是模型Token/质量测量；不能据此承诺总体节省 |

原始probe-source-results.json、probe-graph-results.json、upstream-tests.json与source-index在本次外部实验目录；受控图是人为构造，用于验证边界，没有冒充模型生成质量。首次probe-graph的Bun参数顺序没实际执行，保留该日志；plain文件执行后真实产物和parser结果才作为证据。

## 其他能力与不建议当前接入项

- **整套自动模型生成/多次修复请求**：能生成架构概览，但依赖上游模型/提示、取样和外部费用；本skill已有agent分析步骤，优先复用结构化输出/本地编译，避免重复模型链和批准含义混淆。当前未实测生成准确率。
- **GitHub远程采集/公私凭据/ETag**：有blob一致性、限额、失败恢复和部分树标记；当前本地采集已有路径/版本证据，主要属于重复能力。未来明确远程输入需求时再适配；partial不能变成完整基线。
- **缓存/持久化/分布式锁/取消/SSE**：适合其Web产品；当前skill的本地辅助脚本不需要R2、Upstash及服务生命周期。增量缓存此前未纳入，不能借此重新作为默认需求。
- **MCP与插件/公共已生成图搜索**：当前工具只读缓存，不直接生成图；图可能不是当前源码版本，源文本也可能含赞助/推广。可作为明确指定的外部参考，不设为必经入口，不安装上游插件/skills或把其描述当本项目规则。
- **交互Web、PNG/README分享**：用户审阅需要独立图形界面时再按需选用；本轮优先Mermaid/Markdown文件及源码链接，不引入Next/React站点。
- **讲解视频、TTS/FFmpeg/浏览器渲染、支付/配额/赞助/分析与后台**：独立产品/运营能力，与本次软件工程工作流辅助目标关联低，不推荐接入。

## 许可、投入与约束

- 源码MIT，Copyright (c)2024 Ahmed Khaleel；允许局部复制改造，需保留版权与许可。依赖是独立许可：本机Zod4.6.5/Mermaid12.1.0/jsdom30.1.2为MIT，DOMPurify3.4.16为MPL-2.0 OR Apache-2.0；实际选择的依赖与许可随未来接入范围复核。
- 轻量候选：关系字段/校验、Mermaid/文字派生输出，成本低至中，能直接服务已有文档。跨语言可靠引用解析成本中至高，需配置/语言适配和误报/漏报验证。网页和托管生成系统投入高，当前收益不足。
- 现代码主要TypeScript，现skill检查器是Python标准库。可选Node小工具或局部Python适配需按未来方案决定；不将Next、云存储或模型SDK变成现有checker必需依赖。
- 省上下文优先采用一份事实/证据数据和按需视图，避免同样内容反复生成长说明/图/表；代码保留已选源码和遗漏清单。任何摘录/筛选都说明范围，图用于审阅不等于隐藏正文或字段语义。

## 延后项

| 所属 | 已有结论 / 未决事项 | 影响与恢复条件 |
| --- | --- | --- |
| 源码引用线索 | 有用但误报/漏报已复现；首批语言、别名/workspace解析、线段证据待定 | 用户授权试验后选项目和真值，先补规则或语言解析，不自动追求全语言 |
| 关系图/证据格式 | 建议优先；字段、未核验状态、来源revision与本地链接待方案 | 若决定接入，更新现有工件并只改受影响辅助步骤；不新增审批层 |
| 摘录/阅读排序 | 可选预览，当前完整阅读原则有效 | 明确需要大文件预览并同意覆盖边界后再测，不能默认替换完整阅读 |
| Web/MCP/远程模型/视频 | 当前不采纳；保留上方能力事实 | 有明确外部服务或界面目标时重新核对技能、授权、费用、数据与验证范围 |

## 验证记录与下一步

- 相关上游208项、两个实际函数probe及Pi只读引用/排序观察已完成。持久化摘要见[研究证据](gitdiagram-assessment-evidence.json)，原始环境/完整日志在C:/Users/54667/.codex/experiments/gitdiagram-assessment-20261018。
- 本项目最终实际命令：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-GITDIAGRAM-ASSESS-01 --run-checks --report work/research/gitdiagram-project-final.json`，exit0，required_checks_satisfied=true。TEST为105项，74.093秒；COMPILE/GUIDANCE-COMPILE通过；manifest/change-scope通过，uncovered/documentation_gaps为空。可选手工数据库/契约清单仍partial；没有因此放宽要求。
- 复核正式SKILL、README、VERSION、CHANGELOG、references、scripts、assets、agents无实现diff；checks/control_plane/exclude_paths与HEAD一致。仅研究注册/活动指针/追踪和研究记录变化，原有未提交记录保留。Pi文件集合和1941文件hash与先前snapshot一致，上游git status为空。
- 最后只补实际结果和complete状态，再复核结构/链接/范围，不重复未受影响的105项程序测试。没有提交/实际提交门禁、托管CI、部署或发布操作；本轮程序通过不代替候选采纳决定。
- 下一步是交付本轮范围、主要结论和限制供审阅；正式试验或接入由用户之后决定，不把本报告视为已批准实施计划。

## 固定来源

- [README](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/README.md)、[架构](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/docs/architecture.md)、[MIT](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/LICENSE)、[依赖](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/package.json)。
- [引用提取](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/source-references.ts)、[出处补全](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/edge-evidence.ts)、[图校验/编译](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/graph.ts)、[关系表](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/components/generation/connection-rows.ts)。
- [源码索引/读取](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/source-context.ts)、[摘录](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/source-excerpt.ts)、[阅读排序](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/repository-context.ts)、[紧凑图输出](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/architecture-output.ts)。
- [文字读出](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/features/diagram/readout.ts)、[Markdown](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/features/diagram/markdown.ts)、[渲染安全](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/features/diagram/mermaid-security.ts)、[公共MCP](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/mcp/server.ts)。
