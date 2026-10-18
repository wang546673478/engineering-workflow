# Assessment status update

On 2026-10-19 the user adopted this bounded recommendation and authorized implementation, GitHub upload, issue replies and closure. Current execution and fresh verification are in [TASK-ISSUES-17-18](issues-17-18-task.md). The assessment below is retained as the original decision input; its candidate/not-authorized wording and 1.6.2 evidence describe that earlier stage.

# GitHub #17 / #18 全局修复建议评估

## 当前状态、来源与授权

- 评估 revision：ASSESS-17-18-01；2026-10-19，Asia/Shanghai。阶段：评估完成、可审阅；修复需求/方案为候选，实施未开始。结论：两项均值得处理，#17优先；issue建议需要收敛，不能照单采用。[机器证据](issues-17-18-evidence.json)绑定实际远程源码及运行环境。
- 用户原话：“查看github issue,进行评估是否值得修复,也给了修复建议,修复建议是否值得采用,你最好从全局来看这个修复建议”。本轮范围是调查、验证和建议，不沿用历史发布任务的修复/上传批准。
- 当前任务入口：[TASK-CONTEXT-RELEASE-01](source-context-task.md)，由根清单定位；此文件是其新的评估子阶段，不另建重复权威台账。
- 本地源码：`a407b112410e8717511d62fda8eead66d18cf043`（1.6.1，初始工作树干净、detached HEAD）。只 fetch，未切换/覆盖工作树。
- 最新远程：`origin/main=0216e4c`（1.6.2）。与本地相比，#17/#18 涉及的 initializer、checker、collector、Rust/JS 关系聚合实现及对应测试均未改变；远程另外有 CI finalizer 和三个测试。评估不把本地160项冒充远程163项。
- GitHub API读取于2026-10-19约01:22–01:26+08:00；当时仅两个open issue，均无comment：[17](https://github.com/wang546673478/engineering-workflow/issues/17)、[18](https://github.com/wang546673478/engineering-workflow/issues/18)。`gh` 不在PATH，改用公开REST API；不创建/修改/评论issue。

## Skill review

- 清单来源：本次会话 Skills catalog；复核时间2026-10-19T01:26+08:00；范围为现有issue与建议的源码、运行行为、全局兼容及检查可信度评估。
- adopted `engineering-workflow`：用户指定 `C:/Users/54667/.codex/skills/engineering-workflow/SKILL.md`，1.6.1；项目权威来源为本仓库 `SKILL.md`，1.6.1 / a407b11。两者正文已读；已读项目规则、清单、当前任务、Baseline、模块地图、Spec/Plan相关记录，以及 source-context、checker、project-documentation、baseline-linked-artifacts、implementation-workflow、requirements-interview 适用部分。远程1.6.2只变版本行，不改变本轮工作流语义。
- not-adopted `triage-issue`：`C:/Users/54667/.agents/skills/triage-issue/SKILL.md`，未提供版本；已读。用户要求评估现有issue，不要求创建新issue或TDD实施；其创建issue和委派流程不适用。
- not-adopted `planning-with-files`：`C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，2.37.0；已读。沿用现有manifest/Task/评估工件，避免再建三份重复状态文件。
- 其余清单：本轮不创建skill、接口重设计、前端、文档媒体或完整架构重构；无新增适用候选，无多agent工作。

## 现状链路和已核实事实

### #17 初始化排除缺口

`init_manifest.manifest()` → 生成 `exclude_paths` → `check_project.build_exclude_specs()` → `iter_module_paths()` 在安全路径校验前做词法剪枝；同一排除政策还用于Git change/commit范围过滤。

- 初始化器两个profile共用根级 `node_modules`；`source_paths` 可发现整个 `packages`，不会自动排除其中依赖目录。
- `**/node_modules` 的零层/多层glob已实现；示例清单已有该规则，README也有说明。问题是入口默认值未对齐已有能力，不是缺一种workspace识别能力。
- source-context collector 已按目录名剪枝各层 `node_modules`，但它是可选阅读工具，不能据此静默改变checker的显式排除契约。
- 候选建议：新生成清单使用显式 `**/node_modules`；保持checker按清单工作。不要仅在依赖目录已存在时推断政策，否则初始化前/后结果不同。

### #18 解析依赖与检查可信度

`analyze_rust()` → `analyze_result()` → `build_relation_outputs()` → JSON/文字/图 → collector CLI；独立的全量unittest经checker required TEST与CI结果门槛消费。

- Rust adapter 已捕捉ImportError并逐文件返回 `unsupported[].status=rust_parser_unavailable`；JS也区分 `node_runtime_missing` / `js_parser_unavailable`。
- 聚合输出全无解析文件时已有 `status=unsupported`；详细JSON可区分“未解析”与“解析后零引用”。摘要只有unsupported数量，缺直接原因与恢复提示；CLI成功码反映采集政策完成，不能证明引用覆盖完成。
- 部分语言成功时，聚合status只由 `analysis.files` 是否非空决定，仍会显示 `complete_for_read_supported_files`；须结合unsupported计数和详细项理解覆盖边界。
- README验证段直接给全量测试命令；依赖安装说明在深层source-context指南；CI三路均已安装固定Python解析依赖和script-disabled TypeScript运行时。
- 候选建议：复用既有unsupported字段，在终端/汇总暴露具体原因和安装指引；区分可选产品能力与仓库完整回归的必需环境。不统一把语法回归缺依赖改成skip。

## 逐条建议取舍

| Issue原建议 | 评估 | 全局理由与替代方案 |
| --- | --- | --- |
| #17 自动识别pnpm/lerna/npm/Cargo workspace并追加排除 | 不作为本次主方案 | 已有glob可跨根目录、apps、packages及任意深度，不依赖workspace格式、依赖是否已安装或目录名。增加多种配置解析会带来新的维护/异常路径；Cargo的target、可配置输出目录及其他build/dist目录不是本次已证明的故障，不能顺带扩大排除范围。 |
| #17 发现已有嵌套node_modules时给提示 | 仅适合作补充 | README已给glob示例，示例清单已经采用；只加文档或依赖安装后才提示不能修复“先初始化，后安装”的默认旅程。优先让生成默认值一致；已有清单的迁移提示可另外评估。 |
| #17 checker对任意层node_modules无声明剪枝 | 不采用隐式checker规则 | 排除是可审阅的项目政策，还会影响Git变更检查；静默增加忽略会改变已有项目的检查边界。改成新清单显式生成 `**/node_modules` 就能达到相同易用性，不修改checker语义或已有清单。 |
| #18 增加parser_unavailable状态 | 采用意图，复用已有契约 | Rust/JS/Node已逐文件标明不可用；再造通用顶层枚举既重复又不能准确表达“JS成功、Rust缺失”。把既有原因及恢复提示提升到终端/汇总，保留详细unsupported记录和部分成功数据。 |
| #18 缺依赖时测试skip | 不用于当前必需全量回归 | checker已将unittest skip识别为partial，required TEST仍失败；改skip不解决现有门槛。若再允许partial通过，就实际放宽完整验证。语法功能测试应在依赖准备好后执行；缺环境时集中给安装指引、明确失败，避免后续空图索引异常。模拟缺依赖的降级行为本身仍应测试且通过。 |
| #18 README/检查器给pip安装指引 | 采用README和实际能力入口，调整范围 | Python锁定依赖只解决Rust，JS/TS还需Node及本工具固定TypeScript运行时。README验证段与collector/测试前置诊断提供两种指引；不让通用checker硬编码对所有项目的解析器要求，不给普通盘点强加依赖。 |

#17不是#2/#13能力回退：已关闭的[#2](https://github.com/wang546673478/engineering-workflow/issues/2)修复剪枝时机，[#13](https://github.com/wang546673478/engineering-workflow/issues/13)增加显式glob；本次缺口是初始化器没有消费这项能力。保持旧清单不变也符合#13当时记录的显式opt-in兼容边界。新生成清单默认排除各层node_modules会收窄其扫描范围，需要在说明中写清；把自有源码放在此目录的特殊项目应自行审阅修改默认值。

#18不是“解析器完全静默返回正常空图”：原始references.json已经有原因，relations-status也有unsupported。真实缺口是使用者最先看到的摘要、退出码及测试错误没有把原因讲清。结构校验 `validation.valid=true` 仅说明现有图证据一致，空图也可满足它，不能证明解析执行或覆盖完成。混合语言仍应保留已成功的边，明确未覆盖部分；不要把全部结果改为空，也不要把可选分析失败一律升级为采集失败。

## 候选最小方案和验收（未实施）

1. #17：只调整full/lite共用的初始化默认值，将根级node_modules换成 `**/node_modules`；与示例清单和README保持一致。既有清单只给人工审阅后的显式迁移建议，不自动改写，不引入workspace解析或checker隐式排除。
2. #18：保持逐文件unsupported状态和核心采集可用；终端/汇总按既有原因给出解析覆盖缺口和恢复指引。优先兼容增加诊断信息，不无审阅替换既有status枚举。混合成功应清楚说明“仅已成功语言/文件完成”；真正解析后零引用与缺解析器分别展示。
3. README验证入口给出任务隔离环境、Python固定requirements和 `npm ci --ignore-scripts --prefix scripts/context-runtime`；提醒使用该环境的Python运行测试/门禁。仅Rust分析时无需安装JS依赖，普通盘点无需二者；但本仓库全量回归需要两类依赖。不要自动安装被分析项目的依赖或执行其包脚本。
4. 功能测试前明确诊断实际解析能力是否可用，缺失时集中失败并给出指引；不能只用“包能被发现”判断可用性，也不能吞掉其他执行/解析错误并都标成安装问题。补充在依赖已准备环境中模拟缺Rust、缺Node、缺TypeScript的降级回归。

候选验收覆盖：初始化前/安装后结果一致；root、apps、packages、多层node_modules被明确排除；相似目录名及普通源码仍覆盖；排除外链接继续拒绝；full/lite及示例一致；已有清单不改写。解析侧覆盖Rust/JS单独缺失、混合成功、真正零引用、核心盘点无依赖可用、终端提示和JSON一致、required TEST不靠skip变绿。按既有要求执行完整TEST/编译/影响检查；若进入提交阶段，另行满足控制文件及实际commit/committed门槛。

本次本地隔离诊断已证明候选方向，但这些候选验收尚不是新实现的通过证据。未来如实施，按最新正式版本评估兼容PATCH（当前远程1.6.2，若无其他发布则候选1.6.3），同步实际受影响Baseline/Plan/Task/模块图/契约/业务流、版本与CHANGELOG。本轮不冻结新Spec、不改变既有批准。

## 实际验证与限制

环境：Windows，Python3.13.5，Node24.21.0，npm11.13.0；隔离副本为精确远程 `0216e4cd341bee534ccc85a8824c83a40a7e9840`，源码未改。TypeScript6.0.3、tree-sitter0.25.2、tree-sitter-rust0.24.2按项目锁定来源安装；仅放在忽略的 `work/issues-17-18`，未全局安装，无目标项目安装/服务。

| 验证 | 真实结果 | 结论范围 |
| --- | --- | --- |
| full/lite生成清单 + 真实Windows目录连接模拟pnpm链接 | 默认均exit2，symlink path is not allowed | #17已复现，不依赖mock |
| 同一fixture清单仅将node_modules改为glob | 两种profile均不再出现路径错误；exit1只余未运行的required TEST | 证明候选排除修正路径问题；不宣称整体门禁通过 |
| glob在root/apps/packages/更深层及相似目录名上的匹配；源码内未排除连接 | 正常目录精确匹配；普通源码/相似名不匹配；未排除连接仍exit2 | 保留已有安全边界；真实pnpm安装和Linux没有执行 |
| 已装TypeScript、缺Rust依赖时运行原完整测试范围 | 163项，77.144s，2失败2错误 | 缺Rust确实导致功能测试失败，但数量不同于issue |
| 已装Rust依赖、缺TypeScript时运行原JS/TS测试范围 | 15项，0.386s，3失败7错误 | 单独缺JS解析器即可复现issue所述错误数及空图IndexError，不能只归因于Python依赖 |
| 补齐固定Python和JS解析依赖后运行原完整测试范围 | 163项，76.201s，全部通过，无skip | 验证原实现和环境；不是候选补丁的回归结果，也不是提交/托管门禁 |
| 缺Rust时Rust分析及CLI | JSON逐文件rust_parser_unavailable；汇总unsupported；CLI仍0，空图可通过结构校验 | 应改善可见原因，不能把采集成功误作解析覆盖成功 |
| JS成功、Rust缺失 | status=complete_for_read_supported_files，source_files=1，resolved=1，unsupported_files=1 | 保留部分成功，清楚展示剩余覆盖缺口 |
| 安装后Rust/混合/真正零引用 | Rust解析2边；混合3边；真正零引用source_files=1且unsupported=0 | 现有详细结构已可区分未解析和无引用 |
| required TEST执行真正unittest skip夹具 | 子命令exit0；checker exit1、TEST=partial、skip_marker_detected=true | 不采用skip作为完整回归修复；不修改checker门槛 |

原始日志和诊断脚本位于忽略的 `work/issues-17-18`，源码blob、摘要、结果和日志SHA256保存在[机器证据](issues-17-18-evidence.json)。Windows的Git archive按core.autocrlf=true生成CRLF；初次逐字节核对发现这一差异后，已核对相关文件规范化换行后与远程blob一致，并保存副本原始字节摘要。未对产品源码做实质修改；为保留证据，局部环境/夹具未删除。补充诊断首轮遗漏checker必需的manifest参数而触发JSON读取错误，已补参数后重跑，失败不充当产品缺陷证据。

本轮仅运行调查所需对照、完整原测试范围与文档/引用检查；没有执行/宣称本地当前1.6.1工作树的163项测试或新补丁验证，也没有执行commit、committed、handoff或上传。对照中预期的缺依赖失败和未运行TEST保持失败/未完成事实；全依赖通过不覆盖它们。

## 影响边界和当前决定状态

- 模块：instructions（初始化/使用说明）、checker（显式路径排除的消费者）、source-context（可选解析与输出）、tests、governance（完整测试/CI可信度）。无业务数据库、权限、HTTP接口或数据迁移。
- 本轮只更新评估/任务/有范围的Baseline补充与证据，不改源码、测试、控制清单、版本、发布状态或既有批准。保持原必需门槛；文档评估没有新发布内容，无需升版。
- 已完成：实际故障复现、源码及历史边界核对、两类依赖对照、全局建议取舍和候选验收。
- 候选决定：优先处理#17，再同批收敛#18提示与测试前置诊断；这是agent建议，尚无用户采纳/实施决定。
- 保留待定/延后：checker隐式排除明确不建议；workspace自动识别、Cargo构建目录政策、旧清单自动迁移均无本轮实施范围，相关模块为instructions/checker，只有新增真实场景及明确范围后再评估；可选分析的严格退出模式属于新接口需求，当前无需引入。没有业务数据库/权限/迁移问题待决。
- 下一步：将评估提交用户审阅；修复不是本轮交付目标，不将未实施记为阻塞，也不复用过去发布任务的批准。
