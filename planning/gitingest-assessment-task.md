# TASK-GITINGEST-ASSESS-01：Gitingest 能力与集成价值调研

## 当前状态

- 日期：2026-10-18（Asia/Shanghai）；阶段：源码调查、隔离验证、候选评估与项目必需检查完成，研究状态 complete。
- 授权：用户请求调研 gitingest 中代码感知及其他功能的集成价值；仅授权调查、试验和研究记录，正式集成未授权。需求状态：研究目标 confirmed，采纳候选未确认；实施状态：not_started。
- 工作流来源：本仓库 `SKILL.md`，1.5.0；输入源码 `c21e715`，保留开始时已有 manifest/version-policy-task 修改和四份未跟踪 assessment/pilot 文档。
- 当前任务由 manifest 指向本文件；本文件合并本轮调研 Spec、Plan、Task、影响、证据与决策。已发布产品 Spec/Plan/Baseline 保持原版本，不将研究候选写成已批准设计。
- 输入基线：[BASELINE-LINKED-02](baseline-review.md)、[模块地图](../docs/module-map.md)、[已发布 Spec](../docs/spec.md)、[已实施 Plan](../docs/plan.md)。本轮研究事实作为有版本的附件，不替代产品基线。
- 上游：`https://github.com/coderamp-labs/gitingest`；default main `4e259a02fe72115bee538271622f1234a81c8e1a`（GitHub branch API 与本地克隆一致），包版本 0.3.1。隔离源码在忽略的 `work/research/gitingest`。
- 当前结论：按用户补充的“挑选有用代码功能、保持现有流程”原则，优先候选为源码清单/目录统计、按任务的源码阅读包、受控读取与遗漏记录；Token统计其次，Notebook按项目需要。具体局部函数的复用/改造和现有能力去重见下方“选择性代码接入”。
- 下一步：讨论增量采集是否有实际必要。当前agent建议不纳入接入范围，先用全局盘点和按任务读取；该取舍仍待讨论，未写成用户最终决定。原研究complete，产品代码接入not_started。

## 研究 Spec（ASSESS-GITINGEST-01）

用户原话：“调研 https://github.com/coderamp-labs/gitingest 有没有价值把里面的一些**代码感知的代码**集成到engineering workflow中?当然不仅仅是感知,其他的功能也需要调研”。日期：2026-10-18；范围：工程工作流可复用价值研究，不等于修改正式 skill。

- REQ-GITINGEST-ASSESS-01：调查代码发现、内容处理、远程/本地输入、过滤、资源控制、格式/token、Notebook、CLI/API、服务端/缓存、测试/依赖/许可/维护，以及未提供的语义能力；对照现有 workflow 的真实缺口。
- AT-GITINGEST-ASSESS-01：固定上游 revision、源码证据与实际验证，区分事实/实测/候选/未知；给出采纳优先级、具体集成落点、替代方案、成本/风险、验收建议与不建议项，持久化结论。
- 研究完成不代表采纳、实施、提交或发布批准。上游为外部候选库研究，不对其进行工程接管或声称已完成其生产认证。

### 2026-10-18 用户范围澄清：选择性代码接入

用户原话：“我们肯定不是原样接入这个仓库的内容,我们只挑选有用的进行代码接入,能明白我的意思吗?在不影响现有skill的流程的情况下,进行接入代码功能,有哪些是值得接入的?”

- 已确认的约束：选择有用局部代码并适配到本skill；保留现有工程流程。本轮回答具体功能收益、代码来源和最小接入位置，不继续以整仓引入为主要比较对象。
- 原研究REQ/AT继续覆盖该问题，不新增重复需求ID。需求约束confirmed；下列功能仍为agent建议，未将此次问询解释为已批准功能清单或开始编码。
- 范围影响：补充研究决策和当前摘要，不修改正式SKILL、脚本、模板、验证规则或版本。原事实证据仍有效；历史整包比较保留为调查背景。
- Skill review于2026-10-18T04:08+08:00复核会话清单：继续采用本仓库engineering-workflow1.5.0 / c21e715并重读正文、规则、相关联动/需求/实施引用和任务。其余候选、来源、未提供版本和不采用理由沿用本文件；尚无新增实施或新产物类别，不启动skill创建或接口设计工作流。

## 选择性代码接入：具体值得做什么

本节为用户澄清后的当前建议。重点是现有阶段中可调用的代码功能，原有Baseline→Spec→Plan→Task顺序、用户审核、语义核验与门禁保持其职责。

| 建议功能 | 上游可提取的局部代码 | 现有流程的落点与实际收益 | 复用方式 / 优先级 |
| --- | --- | --- | --- |
| 源码清单、目录树与规模统计 | ingestion.py的节点遍历/统计；FileSystemNode.sort_children；output_formatter._create_tree_structure | 首次基线调查时得到文件/目录/大小清单和可读树，便于安排阅读及核对遗漏 | 第一批。提取纯排序/树格式化；遍历结合已有安全路径/枚举能力，不复制节点模型全部依赖 |
| 按任务范围提取源码阅读包 | output_formatter._gather_file_contents、FileSystemNode.content_string和include筛选入口 | 基线深入阅读、改前影响分析、恢复/交接时，把已选模块/入口/配置/测试集中输出，减少逐文件搬运 | 第一批。复用有路径边界的组织/格式化代码，改为分段输出；行号、文件哈希、Task关联由本项目新增 |
| 受控读取、大小/数量/深度预算与遗漏记录 | config限额、ingestion.limit_exceeded和逐文件处理、filesystem.content的读取状态分支 | 同一轮调查里约束读取量，明确哪些文件未读/失败，支持后续继续补查 | 第一批。复用预算/分类的局部结构，修正限额与编码缺陷；结构化遗漏原因是本项目补强，不是上游现成功能 |
| 阅读量/token估算 | output_formatter._format_token_count的编码/计数部分 | 大仓阅读前估算当前选取量，决定分批读取；小任务可不启用 | 第二批可选。分离数值和显示、编码器可选；预算分片与相关性选择不是该函数已有功能 |
| Notebook源码提取 | utils/notebook.process_notebook、_process_cell的源码/markdown处理 | 基线调查遇到ipynb时直接读代码单元和说明，纳入普通阅读包 | 按项目需要。保留cell来源，默认不含输出；图片/字符串输出处理必须改造 |

### 接入时先复用本skill已有代码

本仓库已存在check_project.py的file_hash、is_link、safe_path、glob_segments_match、iter_module_paths，以及git_paths/staged/committed路径收集。它们与新增文件发现/来源追踪有重合，应评估能否小幅提取成共享内部函数或复用等价逻辑，不能再照搬一套更弱的路径、链接和变更检测实现。采集内容过滤与检查器的exclude_paths用途不同，不能把“阅读时未选取”反向用作检查豁免。

基于这些已有能力，**第一批推荐一个小型本地采集能力，包含上表前三项**：产出机器可读文件/遗漏清单和带来源的阅读包，由现有调查、影响分析、恢复与交接步骤按需调用。技术入口可以是skill内的脚本和简短引用；用户照常使用现有流程，不增加新的常规人工审核步骤。先只补代码工具及必要调用说明；是否增加新的强制门禁需另行讨论，不能夹带进辅助采集功能。

源码版本/文件指纹用于绑定证据来源，可以独立于缓存保留。“变更后只刷新受影响内容”的上一轮增强建议现降为待讨论、当前不推荐纳入：尚无重复采集成本瓶颈证据，必要性见下节。它不是gitingest现成的增量分析代码。目录可见、文件可读依然不能直接推出调用关系或业务事实；新增功能的输出是agent调查输入。

### 2026-10-18：全局扫描之后是否还需要增量采集

用户原话：“源码变化后只刷新受影响的采集结果这个真的需要吗?我们考虑下,已经有全局扫描了,还需要这个嘛,我们讨论下”。记录时间：2026-10-18T04:14+08:00。状态：需求/方案取舍open；用户提出必要性质疑，尚未作出取消或采纳决定；本节是agent建议。

- **当前建议：先不做增量采集。** 全局枚举/统计用于建立当前文件全貌；按任务读取用于控制本次阅读内容；增量缓存只在重复处理相同文件明显昂贵时节省I/O/转换工作，并不补充全局覆盖或语义理解。已有前两种能力时，它不是必需条件。
- 全局盘点不要求每次将整仓源码重新放入模型上下文。应先发现文件/配置变化，再按当前任务选取相关源码及调用方，保留遗漏记录。若全量读取和重新生成所需结果本身就很便宜，直接重做更简单。
- 本轮唯一性能观察是该Windows小仓、68文件默认包约0.76秒；这不是新采集器、大仓或冷启动基准，不能推广为所有项目都快，但也没有证据支持现在增加缓存系统。此前35.6k vs102.3k token的差异来自选取范围，不能归因于增量缓存。
- “只复用未变文件的原文”与“复用模块分析/影响结论”复杂度不同。原文缓存也要处理删除/重命名、分支/未提交内容、过滤/预算/提取器版本；后者还需处理依赖失效。共享类型改变时，调用方文件即使未改也可能必须重新阅读、核验。增量采集不能替代现有改前影响分析或动态基线校正。
- 延后项owner为未来本地采集模块；已有结论是没有必要性证据，未决是实际大仓重复读取/Notebook转换是否成为瓶颈。恢复条件是先测出重复处理的具体耗时/内存/读取量，并证明缓存收益超过失效维护成本；没有预设“未来一定实现”。该延后项不阻塞当前核心功能讨论。
- 本轮沿用REQ/AT-GITINGEST-ASSESS-01，补充工程取舍记录；skill_review于本时间复核宿主Skills清单并重读workflow、根规则、任务、相关需求/联动引用、当前基线/Plan/模块地图和工作树。采用来源/版本及其余不采用项沿用上文。仅更新本研究文档，正式流程/门禁/实现/证据数据/版本不变，无需升版或重跑未受影响的程序测试。

本轮只是补充选择与落点，原始代码及已验证行为没有变化。复核引用/JSON/范围即可，不重复上轮121项上游测试和105项本项目测试；其通过记录保留原版本和时间边界。

补充验证：`work/research/followup-selection-structure.json`中的文档、manifest、change-scope等已执行结构门槛全部pass，本地链接和git diff --check通过；三个程序检查在该结构复核中显式skipped，未把该报告称为新的全套测试通过。

## 研究 Plan / 执行追踪

| 项 | 动作 / 验收 | 状态 | 证据 |
| --- | --- | --- | --- |
| GP-01 | 恢复规则/基线/技能/工作树，登记范围 | complete | 根规则、skill、manifest、已有权威文档和初始 status |
| GP-02 | 上游能力、入口/依赖/消费者和许可盘点 | complete | 27 个核心 Python 模块、15 个服务模块的定义/依赖索引；关键流程逐段读取；main/tag/wheel 对照 |
| GP-03 | 相关上游回归和隔离边界场景 | complete | 121 个本地/模拟测试通过；固定提交远程 tree/blob；受控缺陷复现；联网失败与超时保留 |
| GP-04 | 对照 workflow，形成候选、影响、限制和成本 | complete | 下方能力矩阵、建议方案、验收与延后项 |
| GP-05 | 核对研究记录与现有必需门槛 | complete | project-final-check-v2.json整体通过；引用/差异/政策复核 |

以上全部关联 REQ-GITINGEST-ASSESS-01 / AT-GITINGEST-ASSESS-01；受影响 Baseline 视图仅 governance 的研究状态，产品模块/契约/数据库事实未变。

## Skill review

- 清单：本次会话 Skills catalog；检查时间 2026-10-18T03:47+08:00；范围：第三方仓库源码调研与可复用能力研究。
- adopted：engineering-workflow，来源本仓库 `SKILL.md`，1.5.0 / `c21e715`；用户显式指定。已读正文、project-documentation、baseline-linked-artifacts、checker、implementation-workflow、requirements-interview，复用现有状态和门槛。
- not-adopted：planning-with-files，来源 `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，清单未提供版本；本项目已有 manifest 与 Task 权威，不新增重复台账。
- not-adopted：skill-creator，来源 `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，清单未提供版本；本轮不创建/修改 skill 行为。
- not-adopted：improve-codebase-architecture，来源 `C:/Users/54667/.agents/skills/improve-codebase-architecture/SKILL.md`，清单未提供版本；本轮评估外部工具，不做本仓库重构设计。
- not-adopted：tdd，来源 `C:/Users/54667/.agents/skills/tdd/SKILL.md`，清单未提供版本；运行实际工具行为与既有测试，不增加产品功能。
- 不采用项以清单描述筛选，未加载其执行流程。没有需要 Codex/OpenAI 产品事实、UI、文档二进制或多 agent 的子任务；不使用相应技能。
- 后续若授权集成、修改规则或设计接口，须重新检查 skill、范围、许可和方案批准；当前不派生正式实施授权。

## 本轮影响与版本

- 本地只新增研究文档/证据，注册任务和切换 manifest 当前任务，更新追踪入口；不改 checker 规则、必需命令、保护路径、批准机制或 exclude_paths。
- instructions/checker/adapter 的模块连接、路由/协议、数据结构不变，对产品 MAP/CONTRACT/DB/FLOW 更新不适用。依据：本轮改动范围与源码对照；最终核对 diff。
- 不修改已发布 Spec/Plan/Baseline 的批准范围。研究候选单独保存，未来批准的实施才进入正式工件。
- VERSION 1.5.0 保持；仅研究与状态记录不改变交付行为，无需升版/CHANGELOG。没有提交、推送或发布操作。

## 结论与研究边界

**值得借鉴，但它提供的主要是“让代码更容易被读取”的工具能力。当前仓库没有自动理解架构、调用关系和业务规则的分析器。** 对 engineering-workflow 的增量是把部分人工收集过程做成可复现的工具产物，而不是再增加一批同义提示词。已有 `git`、`rg` 和逐文件阅读能完成不少同类工作；价值最大的场景是首次接管、跨模块阅读包、交接与受限上下文输入。正在本地开发的小变更，直接定位源码通常更轻便。

调查固定于 2026-10-18 的默认分支 main `4e259a02fe72115bee538271622f1234a81c8e1a`。其最新 commit 日期为 2025-08-16；GitHub 仓库 pushed_at 为 2026-10-17，并不表示默认分支源码在该日更新。最新 release 是 2025-07-31 的 v0.3.1 / `45b068bd5e650ac99f99b26f0767c825f8c5ce95`。main 的 pyproject 也写 0.3.1，但与 tag / 实际下载的 PyPI 0.3.1 包在 clone/git_utils 上不同，不能只按包版本转移测试结论。核心扫描、过滤、格式化、Notebook 等 7 个关键文件与 wheel 的文本相同，比较证据已保存。

覆盖：README、pyproject、LICENSE、27 个 core / 15 个 server Python 模块的定义/导入索引，深入阅读入口→解析/clone→忽略规则→遍历→文件/Notebook→格式/token→输出，以及服务器 query→S3→下载、配置/限流/日志和相关测试；补看网页结果复制/下载入口。没有接管上游生产系统，也没有验证浏览器扩展、线上服务、真实私有仓库、多租户隔离、AWS/S3、全平台性能或全部联网测试。

## 能力矩阵：不只代码感知

优先级表示研究建议，不代表用户已确认需求。

| 能力与源码 | 实际提供什么 | 对 workflow 的增量与建议 |
| --- | --- | --- |
| 本地输入，entrypoint/query_parser | 接收目录或单文件，不要求本地目录是 Git 仓库；读取工作树当前文件 | P0：首次接管/局部收集可复用；须补 revision、dirty/untracked 和文件哈希 |
| 文件发现与目录树，ingestion/filesystem/output_formatter | 递归扫描、计数、排序，README 优先；输出树和带路径分隔的内容 | P0：形成可核对的阅读目录；文件数不代表语义覆盖，目录关系也不代表模块依赖 |
| 过滤，pattern_utils/ignore_patterns/ingestion_utils | 默认排除、用户 include/exclude、递归加载 `.gitignore`/`.gitingestignore` | P0：很有用的入口，但忽略语义有实测偏差，默认表也不适合直接充当工程调查清单 |
| 文件/深度/总量限制，config/ingestion | 默认 10 MiB 单文件、深度20、10,000文件、500 MiB原文件总量 | P0：借鉴显式限制；需增加结构化跳过/截断记录和真正的 token 预算，不能静默省略 |
| 文本和二进制，filesystem/file_utils | 先读1024字节判断可否UTF-8解码；空文件/二进制/错误变为文字占位 | P0：借鉴状态分类；不能照搬判定与异常转字符串后继续成功的策略 |
| 阅读包与导出，output_formatter/entrypoint | `(summary, tree, content)` 三个字符串；CLI默认digest.txt、文件/stdout，库默认不写文件 | P0：按任务/模块生成阅读包，需加结构化索引、稳定行号和来源；不要每次全仓塞入上下文 |
| Token统计，output_formatter | 用tiktoken `o200k_base`计算tree+content的token数，返回舍入后的可读数值 | P1：用于选择阅读范围；属于特定编码估算，没有语义压缩、相关性排序、预算分配或自动切片 |
| Python同步/异步API，entrypoint | `ingest`/`ingest_async`；异步环境可直接await | P1：可做可选适配器，优先进程隔离；main中GitPython和本地读取仍有同步阻塞，async签名不等于高并发扫描 |
| 远程引用和子路径，query_parser/clone/git_utils | HTTP(S)、slug探测、branch/tag/commit、tree/blob；浅克隆，子路径可用sparse/partial clone | P1：外部库调查有价值；必须核对请求ref与实际checkout SHA，远程取数不是本地改动分析的替代 |
| 私有仓库，auth/git_utils | token参数或GITHUB_TOKEN，主要针对GitHub/GitHub Enterprise | P2：本工作流通常已有本地checkout；全托管平台凭据支持并不完整，发布包还存在凭据日志问题 |
| Submodule，clone | 可选递归初始化，默认关闭 | P2：仅确有依赖时开启，逐个记录路径/ref/来源；不是默认扫描全部外部代码 |
| Notebook，utils/notebook | markdown/raw转注释，保留代码，可附输出；不执行Notebook | P2：数据/科学项目有价值；默认包含输出且有实测缺陷，需要按cell保留来源并默认关闭输出 |
| 可复用缓存，server/query_processor/s3_utils | 可选S3 digest/metadata；缓存key包含host/repo/commit/subpath/include/exclude | P2：借鉴“来源版本+选取策略”思路；不是增量语义分析，缓存键尚缺max_file_size/引擎版本/身份维度 |
| Web/API/分享，server/static/templates | FastAPI GET/POST ingest、复制/下载、结果展示裁切、本地或S3存储 | P3：当前skill无Web服务需求；不建议引入整套产品/存储/访问治理成本 |
| 运维，server/main/server_utils/metrics_server | 健康检查、TrustedHost、10次/分钟限流、Prometheus、Sentry/结构化日志、Docker/CI | P3：有服务才有价值；这些不补工作流的源码理解缺口 |
| 浏览器扩展，README | 链接到独立仓库的Chrome/Firefox/Edge扩展 | 本仓库不是扩展源码，未调查其实现；对本地工程skill暂不采用 |

源码中未发现 AST/Tree-sitter 解析、符号定义/引用索引、真实依赖图/调用图、类型推导、相关性搜索/向量检索、变更影响传播、自动路由/数据库契约提取。这里的统计摘要是目录/数量/引用/token等元数据，不是由模型生成的语义摘要。网页可读、支持多种代码文件，不意味着理解这些语言的语法与业务。

## 已实测的集成边界

以下是当前调查的复现结果，不把上游issue的说法直接当成事实。原始日志与受控fixture在忽略的work/research，关键结果另存[持久化证据](gitingest-assessment-evidence.json)。

| 编号 | 场景与实测结果 | 对集成的影响 |
| --- | --- | --- |
| GF-01 | 默认忽略package-lock.json、Cargo.lock、build.gradle、.gitmodules；保留uv.lock/go.sum。精确include可恢复package-lock，但include_gitignored仍保留默认忽略表 | 工程接管必须读真实依赖/构建/submodule配置，不能复制默认表；“包含gitignored”也不是包含所有文件 |
| GF-02 | `*.log`后跟`!important.log`装入set后，用8种PYTHONHASHSEED测试；seed2/6排除了important，其余保留；原生Git保留important | 顺序丢失影响可复现性和覆盖；应使用保留层级/顺序的规则或Git原生语义 |
| GF-03 | sub/.gitignore的`*.private`漏排除sub/deep/child.private；根规则`/root-only.txt`错误排除deep/root-only.txt；原生Git结果相反 | 支持ignore文件不等于与Git完整兼容；深层过滤与根锚点需要契约测试 |
| GF-04 | 1023个ASCII字符后紧接中文，1024字节探测截断UTF-8字符，被标为Binary；有效UTF-16也被标为Binary；普通UTF-8中文正确读取 | 必须处理跨字节边界/BOM/解码失败；否则文本遗漏可能伪装成已分析 |
| GF-05 | 单文件100字节、max_file_size=10仍完整读入；目录路径同限制会跳过大文件 | 限额在不同入口不一致，不能直接作为资源保证；上游issue609同类 |
| GF-06 | 文件数、深度、总字节预算触发后仍返回三字符串，没有machine-readable的partial/omission清单；binary占位仍计入Files analyzed | 不能把Files analyzed当完整基线证据；限制必须回写included/skipped/truncated/failed状态 |
| GF-07 | Windows目录连接的is_symlink=False、is_junction=True，实际遍历到根外fixture内容 | 当前检查器拒绝链接/目录连接旁路，采集器必须保持同等根边界；测试目标全在隔离研究目录 |
| GF-08 | 默认可收集合成的.env.production、credentials.json和id_rsa；.env本身被排除 | 默认忽略不是秘密扫描/脱敏，不能把原始dump作为默认外发数据；需要独立敏感策略与输出审查 |
| GF-09 | Notebook默认包含输出；image-only输出使整个文件变为Error processing notebook，源代码丢失；字符串输出HELLO拆成逐字符行 | 基础Notebook转换可借鉴，默认只取source并容忍无text/plain输出；issue608/603经本机复现 |
| GF-10 | URL先解析为HEAD提交，再覆盖为一个不存在的branch，resolve_commit仍返回旧HEAD，而非报错 | branch参数与实际来源可不一致；本轮实测限参数覆盖，不将issue606对所有tree URL的主张当作已验证 |
| GF-11 | main与PyPI0.3.1的clone/git_utils不同；发布包在合成token/边界替身测试中，日志含可逆认证header，透传命令错误也含该header | 上游issue605对应发布代码；main改为GitPython/认证URL，需另行审核，不能推断“同版本已安全” |
| GF-12 | S3 key按commit/subpath/过滤器构造，签名与调用路径没有max_file_size或引擎版本 | 参数不同可能复用不对应结果；这是源码级缓存键分析，未连接S3或声称已复现线上泄露 |

补充源码观察：忽略规则每路径重建PathSpec，读取ignore文件先递归搜索再做采集剪枝，大目录成本需实测；遍历后才排序，受限文件集合不保证由稳定优先级选出。整包读取、拼接、再tokenize会同时持有大字符串；500MiB限制是原文件字节量，不是生成内容/内存/token硬上限。main的async timeout不能保证中断同步GitPython调用；真实超时/取消需独立进程或可取消执行边界。库导入会设置locale并全局配置日志，内嵌调用有宿主副作用。这些均为采用前的技术核对项，没有把未运行的大仓/负载测试记为通过。

## 候选集成方式与投入

| 方式 | 收益 | 成本与判断 |
| --- | --- | --- |
| 整包强制依赖/复制整个产品 | 快速得到现成CLI/API及Web配套 | 不建议：把采集、tokenizer、认证、服务端及维护边界带入原本标准库检查器；对语义分析没有额外帮助 |
| 可选外部gitingest适配器 | 少写上下文导出，适合可信的小型公开仓库 | 原型成本低，生产适配中等：固定main SHA或wheel哈希、验证ref/内容/完整性、进程隔离、降级与许可；包装三字符串无法恢复所有已遗漏文件，不能直接当权威证据 |
| **借鉴设计，做独立本地采集器** | 可复现清单、任务阅读包、覆盖/遗漏和源码版本证据直接服务本workflow | **推荐首个候选**；投入中等：Git原生枚举/规则、稳定路径/行号/哈希、敏感策略、预算/状态与回归。现有checker保持自己的职责，不承载重型解析依赖 |
| 仅补提示词，手工继续git/rg | 零运行依赖，可立即按现有流程调查 | 适合小任务；大量同义规则收益有限，也得不到机器产物。当前workflow已要求探索和证据，单纯改写价值不高 |

可选工具仍可调用上游维护良好的局部函数，但实际复制代码需要保留MIT版权与许可。上游MIT授权允许复用/修改/分发，不免除依赖各自的许可义务。main核心约3585行/27模块；本轮全dev+server测试环境安装92个包，这不是基础安装的依赖数量。pyproject列9项无条件直接依赖和条件依赖，没有锁定全部兼容版本；当前隔离环境pathspec1.1.1产生大量deprecated gitwildmatch警告，兼容/重复编译成本要计入维护。

### 建议的最小候选切片（尚未批准实施）

1. **P0 / 采集可核对。** 增加独立可选入口，例如`scripts/collect_code_context.py`（候选名，当前不存在）。先输出结构化inventory：source revision、dirty/untracked指纹、扫描范围/策略版本、每文件路径/类型/大小/哈希、included/excluded/unreadable/binary/truncated及原因。将“源码枚举”“内容选取”“语义已核验”分开。
2. **P0 / 按任务打包。** 从模块/改动起点和现有文档选阅读集合，保留项目规则、入口、配置/锁文件、迁移和测试；允许agent循调用方扩展范围，输出带稳定来源/行号的阅读包。选取逻辑与现有权限/门槛分离，遗漏不能在完成报告里消失。
3. **P1 / 阅读量与复用。** 估算token，按预算分片，默认不强制安装tokenizer；若缓存，key覆盖revision+dirty哈希+选取/敏感策略+预算/编码+工具版本，报告fresh/stale。预算和缓存属于需新增设计，上游只有统计和服务端digest缓存。
4. **P2 / 场景适配。** 外部仓库输入和Notebook按需启用；只读引用固定实际SHA，Notebook默认source并保留cell映射；gitignored文件按真实用途显式选择，submodule默认关闭并记录各自版本。

候选数据流是“本地源码/受控checkout → 可核对文件清单 → 按任务的阅读包 → agent语义核验和测试 → 现有Baseline/影响/证据”，属于Baseline的辅助来源。清单不会自动写出已确认模块关系、API权限、字段含义或业务流，也不把现有manual/partial清单改成complete。

具体影响：若采用，须新增采集模块并更新module-map、CLI契约、业务流程、Baseline来源/覆盖说明和相关Plan/Task；元数据不读业务数据库，无业务数据迁移。引入源清单验证能力需要单独设计，不应通过改required/exclude或伪造provenance让现有门禁通过。`SKILL.md`只增加简短触发入口，详细操作放引用文档，避免扩大常驻提示词负担。若交付兼容新能力，按本项目约定评估MINOR；具体版本待未来批次决定。

## 如何验收候选才有意义

- 正确性：对照原生Git/受控目录，覆盖根/嵌套/否定ignore、tracked/untracked/dirty、文件名空格/Unicode、锁文件/构建入口、二进制/UTF边界、单文件/目录限额、symlink/junction、Notebook无文本输出与所有错误/省略原因；不读取fixture根外内容。
- 可信性：请求ref=实际SHA，输出可回溯到文件哈希/行段；缓存不因预算、策略或本地改动混用。格式标记只能划定来源，不能把仓库内文本提升为执行指令。
- 效益：与现有git/rg阅读流程做同任务对照，比较关键入口/调用方/配置召回、人工补读量、实际输入token、耗时/内存、错误遗漏和维护成本；能打包文件或减少token不等于答案更好。
- 兼容：工具不可用可回到既有调查流程，原必需门禁仍满足；任何新控制规则另行审阅。测试覆盖本地/模拟边界与必要真实远程行为，不能用mock结果替代ref正确性。

本轮成本观察：当前工作树默认阅读包68个文件、438232字节、约102.3k token；指定checker相关4个文件后148928字节、约35.6k token。两者是o200k_base估算且选取集合不同，约65%的token减少来自缩小范围，不是上游语义压缩或质量提升。热缓存下单次收集约0.76/0.75秒；一个Windows小仓样本不能推导大仓性能或稳定提速。没有测量模型答复质量/实际计费。

## 延后与未采用事项

| 所属 | 已有结论 / 待决问题 | 影响、依赖与恢复条件 |
| --- | --- | --- |
| 采集器 | 候选中价值最高；是否进入最小本地试验、最终字段/预算待定 | 完成本轮研究不依赖该决定；用户后续要求试验或集成后，先形成明确范围/方案和受影响工件 |
| 语义分析 | gitingest无此实现；是否需要符号/依赖/调用关系及支持哪些语言待定 | 若目标是自动生成模块/契约图，应另研AST、语言服务/编译器、框架注册和运行证据，不能沿用此次库选型结论 |
| 远程/私有输入 | 公共commit smoke通过，凭据/平台/取消/临时目录边界仍需方案 | 本地方案不依赖；有真实跨仓/私有需求才恢复，不默认把私有源码上传线上gitingest |
| Notebook | source提取有价值，输出缺陷已复现 | 仅数据科学项目启用；实施前修复MIME/str/list、默认输出策略和cell来源 |
| S3/Web/监控/浏览器 | 当前skill无服务化需求；缓存思路可借鉴 | 只有明确共享服务/产品界面目标时再研究租户、权限、存储、外部部署；本轮不引入 |

## 验证记录

- 环境：Windows、Python3.13.5、Git2.47.0.windows.2；局部venv在work/research/venv，依赖版本清单work/research/dependencies.txt。没有安装全局依赖、改Git全局设置或使用真实token；测试子进程移除GITHUB_TOKEN。
- 本地/模拟上游测试：`run_focused.py offline` 64 passed（6.02秒），`run_focused.py clone` 57 passed（0.30秒），共121项。选择范围与命令参数在对应summary/log/xml；源码未改，未压低断言。
- 先前较宽选择包括真实跨托管平台的test_git_host_agnostic，240秒超时且出现失败；单独定位到Bitbucket测试仓库403，27 passed / 1 failed后停止。未将失败抹去或整套测试写成通过；外部平台/仓库可用性仍未验证。联网summary/server套件没有全跑；其生产行为不在本轮认证范围。
- 真实远程smoke：octocat/Hello-World的固定SHA `7fd1a60b01f91b314f59955a4e4d4e80d8edf11d`，tree和blob/README均读到Hello World，summary有同SHA；任务内临时checkout文件清理后为空。另测ref覆盖优先级，不借此声称所有branch/tag正确。
- 受控fixture：default/include、ignore顺序/嵌套/锚点、UTF编码、四类资源限制、单文件绕限、Notebook、async API、缓存key、Windows junction、公开包认证边界。Git oracle首版使用换行stdin受Windows CRLF影响，已改NUL分隔复核；早期`.tmp`样例被默认表遮蔽，已换`.private`独立验证，不沿用无效初测。
- 持久化摘要：[gitingest-assessment-evidence.json](gitingest-assessment-evidence.json)。原始源码、脚本、完整依赖、日志、XML和阅读包在忽略的work/research；它们是研究材料，不随skill分发，删除后仍可从本报告的固定来源和场景重建。合成token探针只保存布尔结果，不包含真实秘密。
- 首次本项目检查`project-final-check.json`中TEST/COMPILE/GUIDANCE-COMPILE通过，但整体失败：证据摘要生成器因Windows缺少tzdata失败，检查在摘要文件出现前已启动，文档/链接/影响门槛因而失败。已改用标准库UTC+08:00固定偏移并实际生成摘要；这不是上游缺陷。保留首轮失败，不把单项测试通过当成整体通过；现对完整工件重新执行最终门槛。
- 本轮最终命令：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-GITINGEST-ASSESS-01 --run-checks --report work/research/project-final-check-v2.json`，exit0，required_checks_satisfied=true；manifest/change-scope均pass，无uncovered/documentation_gaps；TEST通过（105项，78.671秒），COMPILE/GUIDANCE-COMPILE通过。运行使用本项目默认Python3.14.7，独立于上游Python3.13.5实验环境。
- 最后仅补实际结果和complete状态，复核JSON、相对链接、变更范围与git diff --check，不重复未受影响的全量测试。checks命令、control_plane、exclude_paths与HEAD一致，正式指令/脚本/模板/版本均无diff。可选manual数据库/接口清单仍partial，没有降级门槛；未运行commit/committed或hosted CI，未提交发布。

## 固定来源

- [README / main快照](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/README.md)、[pyproject](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/pyproject.toml)、[MIT LICENSE](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/LICENSE)。
- [扫描与限额](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/ingestion.py)、[文件与编码](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/schemas/filesystem.py)、[ignore规则](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/utils/ignore_patterns.py)、[输出/token](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/output_formatter.py)。
- [API入口与ref覆盖](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/entrypoint.py)、[Notebook](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/gitingest/utils/notebook.py)、[服务流程](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/server/query_processor.py)、[S3 key](https://github.com/coderamp-labs/gitingest/blob/4e259a02fe72115bee538271622f1234a81c8e1a/src/server/s3_utils.py)。
- [v0.3.1发布](https://github.com/coderamp-labs/gitingest/releases/tag/v0.3.1)、[发布clone实现](https://github.com/coderamp-labs/gitingest/blob/45b068bd5e650ac99f99b26f0767c825f8c5ce95/src/gitingest/clone.py)、相关未关闭报告 [609](https://github.com/coderamp-labs/gitingest/issues/609) / [608](https://github.com/coderamp-labs/gitingest/issues/608) / [606](https://github.com/coderamp-labs/gitingest/issues/606) / [605](https://github.com/coderamp-labs/gitingest/issues/605) / [603](https://github.com/coderamp-labs/gitingest/issues/603)。Issue为线索，实际验证范围以本报告为准。
