# TASK-CONTEXT-RELEASE-01：双项目组合/顺序比较与1.6.0发布

## 当前状态和用户授权

- 2026-10-18T16:32+08:00；调查按用户要求暂停于全局原因复盘。本机已推送版本仍为1.6.1提交a407b11；JSON/task回执误写已修复，修复前内容另存备份，失败记录保留。a407工作副本有一个未提交、未完整验证的reparse fixture路径改动，不代表已交付。Hosted run39110935645：Ubuntu原TEST artifact直接通过；Windows原TEST 160项中1项失败。后续全量本地命令另有1项JSONDecodeError，根因是本地manifest在回执写入时被污染，不作为代码回归结论。用户明确要求暂停，不继续改代码、测试或上传，等待复盘决定。旧run39109363841原TEST失败artifact保持历史，诊断重跑通过不替代原门禁。
- 用户原话：“这样你把多测试几个功能组合和排序,这几个功能都是需要只不过要完善使用规则,应该怎么组合,然后进行测试,E:\pi-main和D:\agent-harness-research\codex 这几个应该够你测试了,你找出最优,在不改变skill流程的情况下,把最优的上传github”。明确授权比较、完善规则、在已讨论辅助功能内择优正式实现并提交上传；不要求额外同范围批准。排序限辅助能力的调用/展示顺序，原阶段/需求确认/方案批准/门槛职责不变。
- 保留七项组合：盘点、树/统计、完整紧凑阅读包、限额/遗漏、引用分析、出处/图校验、图/文字/表格与源码定位；Token计量仅实验，Notebook/增量缓存/云模型链不引入。
- 本轮原清单/研究文档有未提交工作，完整备份在外部primary-original。发布从干净远程基点构建，只带本批实现/文档/摘要证据；保留旧评估原文件，不把它们混作新审批。
- 两个目标仅作只读语料；不运行其产品/模型/依赖安装、不改Git状态或源码。初始hash和实际Git状态在外部evidence，按每项目规则读取适用文件。
- 下一步：暂停。等待用户对CI门槛、测试环境隔离、跨平台路径验证和回执写入的全局处理方式作出决定；未验证的 fixture 工作副本不视为交付。

## 规格和验收（SPEC-CONTEXT-01）

- REQ-CONTEXT-01 / AT-CONTEXT-01：完整清单、可选树/统计、完整紧凑阅读包、预算和每项遗漏，来源hash/行段清楚；读取边界及采集完整性有行为验证。
- REQ-CONTEXT-02 / AT-CONTEXT-02：引用索引和可核对方向/类型/出处，JS/TS按语法和配置定位，Rust按语法和模块/Cargo元数据定位；未知动态/跨语言/cfg条件保留，不冒充调用图/业务认证。
- REQ-CONTEXT-03 / AT-CONTEXT-03：一份图数据派生文字/表/局部图/包概览，拆清调用/展示条件。保持原流程/必需检查/批准与保护职责，仅新增简短入口和辅助资源；Token/Notebook不作产品功能。
- REQ-CONTEXT-04 / AT-CONTEXT-04：冻结四个顺序、两项目三类场景和评价口径；覆盖/正确性为硬约束，其后比较时间/读取/上下文/冗余；按实际场景选择，不声称对所有任务全局最优。真实项目内容/hash/来源不变。
- REQ-CONTEXT-05 / AT-CONTEXT-05：正式版本1.5.0→1.6.0 MINOR，版本/CHANGELOG/当前Baseline/Spec/Plan/Task/trace同步；完整测试、commit/committed、GitHub上传及实际远程SHA核对，托管CI单独报告。

## 方案和执行（PLAN-CONTEXT-01）

| 项 | 方案/需求验收 | 状态 |
| --- | --- | --- |
| CR-01 | 核对已有事实/规则/前期决定和源码指纹，保留脏工作树 | complete |
| CR-02 | 固定对照矩阵，完善统一采集/引用/输出接口 | complete |
| CR-03 | 两项目比较，多语言/安全/图及原有回归 | complete |
| CR-04 | 选择默认调用/展示规则、收敛正式工件/版本 | complete |
| CR-05 | 本地门槛、精确提交、上传和回执 | complete |

## Skill review

- 来源：当前会话Skills catalog；检查时间2026-10-18T06:17:47.851388+08:00；范围由隔离融合转为双项目多顺序实测与用户授权正式发布。
- adopted engineering-workflow：PRIMARY/SKILL.md1.5.0/c21e715，正文/AGENTS/manifest/当前任务、Baseline/Plan/模块地图、requirements-interview、project-documentation、baseline-linked-artifacts、implementation-workflow、checker已读。
- adopted skill-creator：C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md，版本未提供；已读正文，保留渐进披露/原语义、验证脚本实际行为和按需规则；沿用UI设置。
- not-adopted planning-with-files：C:/Users/54667/.agents/skills/planning-with-files/SKILL.md，版本未提供；本项目联动工件是唯一权威，不建重复台账。
- not-adopted design-an-interface：C:/Users/54667/.agents/skills/design-an-interface/SKILL.md，版本未提供；在已授权辅助能力内比较调用组合，不需要并行接口设计。
- not-adopted tdd：C:/Users/54667/.agents/skills/tdd/SKILL.md，版本未提供；行为fixture和独立源码oracle验证，未要求强制TDD。
- 没有显式多agent授权；单agent完成，不把oracle脚本说成独立模型审查。语言/产物/范围变化再review。

## 比较预注册

- P1全量优先：全局盘点→全量可读文本/引用→全部图表，再选任务材料。
- P2任务优先：全局盘点→任务文件完整包→相关引用→全部局部图表。
- P3引用优先：全局盘点→任务入口引用→向直接本地目标扩展完整包→证据和适用视图。
- P4分场景：全局盘点→直接定位/任务包；小修跳过引用；跨模块按疑点补引用/必要目标；审阅时才给图表，平时简短文字。功能保留，按需调用，不增加审批。
- 两项目各小修/跨模块/审阅三场景；固定目标源码与预期文件/引用样本。每种组合实际执行，完整性/证据可核验为前提，再比较耗时/读取量/离线上下文。P1较贵不代表可省略原要求的全局基线调查。
- 全局枚举与全量正文分析分开；正文只在需要时读取。实现支持一次运行中复用同份inventory，省重复扫描而非新增跨运行缓存。
- Rust多数的Codex不能只用JS/TS结果冒充覆盖；新增按需Rust语法适配与明确的unresolved/cfg语义，受控fixture验证后才做结论。不读取业务秘密或执行Cargo构建。

## 影响和发布边界

- 源码辅助新模块与文档、样例/测试/optional runtime依赖；模块图/契约/业务流/基线和Spec/Plan/Task同步。无业务数据库或业务数据迁移。
- 保护规则、旧required命令、批准变量、既有流程顺序不放宽。若新增CI依赖安装，只作用本工具自身可选解析回归，不安装被分析项目或执行包生命周期脚本；在此记录具体差异。
- 用户已明确授权在不改变流程下择优上传。审批信号仅在该具体变更本地门槛单次子进程使用，不写永久设置。额外托管环境审批若真实需要独立人类决定则不伪造。
- 最终“最优”限本试验的候选/场景；不把生成图或工具成功当Baseline语义完成。目标项目完整业务基线/产品测试不是本工具试验的验收范围。

## 验证和结果

24次实际对照已完成，全部目标文本/hash核对和cross/review目标引用一致性通过，汇总见[benchmark](source-context-benchmark.md)和[机器摘要](source-context-evidence.json)。最终选择P4分场景顺序，保留必要时的P3扩展和明确要求的P2多视图，不删除已确认辅助功能。

两个源项目hash/文件集合在比较结束后再次核对无变化；原check_project.py、原必需命令、保护/排除声明未变；原SKILL阶段/审核正文移除新增短入口并还原版本后逐字一致。源码说明/CLI新增了显式--views和Rust按需适配，配置/条件/未知保留，非运行时调用图。

CI变更只增加Node22准备、script-disabled npm ci和固定Python解析依赖安装，三条原检查/审批路径保持；不放宽门槛，也不自动批准任何环境。原任务和目标项目规则继续有效。使用1.6.0 MINOR，CHANGELOG保持Unreleased至真实发布。

实测后补了same-run inventory政策一致性拒绝和Rust条件边标记，已通过受影响focused回归；这些防护不改变本次默认政策下的已测范围，最终全量回归覆盖当前源码。首次结构检查把报告目标误放仓库外，原检查拒绝后改为work内；未绕过根边界。完整change/commit/committed和远程事实在后续更新，未执行的项目保持未验证。


### 当前源码最终change验证

- `work/release-change-verified.json`整体通过，required_checks_satisfied=true；157 tests（原105+采集29+JS/TS关系15+Rust8），原COMPILE/GUIDANCE-COMPILE通过；新Python脚本编译、Node语法和skill-creator UTF8结构验证通过。manifest/change-scope无缺口，可选manual清单仍partial。
- 原full regression曾失败于Rust条件边可视化去重，诊断复现后修复compiler键，保留条件/关系类型。JSON完整证据不丢；全部保存视图重绘/重计量，相关Rust focused和完整157 tests通过。旧helper耗时保留原测量日期，图重绘分别测得每份小于1ms，不拿旧时间冒充修正后全链重测。
- 最终P4审阅图3份真实Mermaid parser均通过。全量辅助分析/目标引用比较是采集工具试验，Rust宏/cfg/符号重导出和业务事实仍未验证；相关要求未降级。
- 下一步：记录原话授权具体发布范围后，按完整commit与committed门槛执行和上传；不在仓库内设置批准信号。只有已授权版本/范围对应的一次子进程可传外部信号。云审批不伪造，实际远程CI单独核实。
- 两次此前declared TEST未满足：Windows裸python子进程优先找到base interpreter，未见局部venv的可选Rust依赖。直接venv全157项用于诊断，同时将task-local兼容site-packages仅传入本次检查子进程PYTHONPATH，保留原命令不变；最终change/commit/committed均核对所用环境。没有全局安装或降低缺依赖条件。


### 本批具体提交/上传批准范围

本文件顶部本轮用户原话明确要求“这几个功能都是需要”“多测试几个功能组合和排序”“不改变skill流程”“把最优的上传github”。它批准本批全部七项辅助能力、按需/顺序规则、两项目中用Rust/JS/TS证明真实覆盖的局部语法适配、兼容MINOR1.6.0及发布。不是仅同意调查；也没有批准删除原工程流程或放宽门槛。

本次控制文件实际差异：SKILL只加短入口/升版；manifest注册模块/文档/Task与活动指针；VERSION/CHANGELOG记录新增兼容能力；CI只准备新测试所需的固定可选解析器，保留原ordinary/reviewed/manual路径、控制环境、required命令、保护范围和批准变量。CI会安装本工具自己的依赖但禁止npm lifecycle，目标语料项目不安装。所有这些属于实现/验证/发布所需配套，不改变用户要求的流程。单次本地外部信号仅用于本份已完成可审阅差异的commit/committed检查，不存入环境/仓库设置；不伪造托管环境的人类review。

程序完成/Task complete表示本地辅助内容及证据已达门槛；精确提交和远程上传回执随后记录，未执行部分不作为成功证据。已完成Spec/Plan/Baseline与本批用户授权关联，旧审阅仍按旧范围保留。


### 1.6.0源码上传回执

- 2026-10-18T06:41:11.316319+08:00核对origin/main=`502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`，与本地主提交一致，上传成功。commit和committed报告均required_checks_satisfied=true，各含157项测试、原编译、作用域与控制规则检查。原审批信号只用于相应子进程，没有持久化。
- CHANGELOG现在填写真实源码上传日期2026-10-18；本次只补完成状态和证据，不改变发布实现，仍为1.6.0，无需再升版。
- GitHub hosted CI已启动：[当前run](https://github.com/wang546673478/engineering-workflow/actions/runs/39076043405)，尚未据本地通过推断其结果。回执变更继续按同等门槛核对后上传。


### 最终Windows换行边界更正

- 收尾复现多行Rust CRLF语句在出处验证时被splitlines归一化后误判。现在仅对比时归一化行尾，原文/hash/行段不变；新增独立回归，Rust9项focused通过。该变更不影响已测LF语料引用集合和组合选择，但原157项报告只覆盖修正前版本。当前158项全量提交/已提交门槛会重新验证。
- 已上传502fd69主提交保留为历史；未上传的纯回执cfd8e83仅在专用release副本软退回并保留index内容，以便合并此同批纠正，未触及原skill或目标语料。正式仍为同批1.6.0，最终发布SHA在实际回执核对。

- 2026-10-18T06:49:58.869485+08:00：第一轮最终commit检查的TEST达到原120秒时限，required_checks_satisfied=false，原报告保留；逐项诊断运行158 tests/73.806s全部通过，无skip。没有改动既有命令、测试范围或超时；继续用原门槛重试，诊断结果不替代提交检查。托管原run仍等待既有engineering-control-review人类环境审批。

- 2026-10-18T06:51:42.310804+08:00：未改变原命令/120秒时限的最终commit重试通过，required_checks_satisfied=true；158项源码与直接诊断一致，COMPILE/GUIDANCE-COMPILE、控制和文档作用域全部通过。此次仅补验证记录，源码hash不变，记录更新后复核链接/暂存区；最终实际提交仍执行完整committed门槛。

## Windows Actions失败修复（2026-10-18T15:48:16.378745+08:00）

用户本轮“看下github actions 报错了”延续已授权的辅助功能集成与上传；完成同范围兼容修复并上传，不删除失败测试或降低门槛。失败run39076867717/commit21f9aa2：Ubuntu reviewed通过，Windows158项中2项失败，环境审批已完成，不是审批拒绝。

- 已复现：Python3.11.9没有Path.is_junction，采集器依赖的旧predicate未识别目录连接；外部路径仍被safe_path拒绝，但标记为path_unavailable，内部目录连接也需要明确拒绝。采集器局部补充lstat reparse属性识别，覆盖扫描、根祖先及输出路径；旧检查器保持不变。
- 已复现：以Windows真实8.3别名路径调用读取失败fixture，target与采集时resolve后的长路径不相等，故模拟PermissionError未触发。fixture先resolve目标后注入失败，仍要求unreadable且源码不导出；不将included视为正确结果。
- 方案：保持所有现有工程阶段/批准/检查、原TEST120秒和CI配置；为旧Python补兼容识别，增加真实/模拟内部连接和根边界行为覆盖；用隔离官方Python3.11.9及现有3.13验证。只修该辅助模块/测试/当前文档，两个测试语料不改。规格/用户目标未变，继续SPEC-CONTEXT-03/REQ-CONTEXT-01..05。
- 发布影响：1.6.0已交付，后续兼容修复为PATCH1.6.1；同步VERSION/SKILL/README/agents/CHANGELOG，保留1.6.0证据及失败日志。原检查器/CI/必需命令/保护规则不改。
- Skill review重新核对：当前会话catalog，engineering-workflow正式1.6.1正文/AGENTS/活动Task、implementation-workflow/checker及BASELINE-CONTEXT-05/PLAN-CONTEXT-05/模块图已读；skill-creator正文已读，用于窄范围兼容修复及元数据验证。不采用新的规划台账或多agent，沿用本Task权威。范围限定为CI测试fixture隔离；当前本地原门槛通过，精确committed及新托管验证尚未完成。

- 2026-10-18T15:51:42.328831+08:00：官方WindowsPython3.11.9原commit门槛通过；现有Python3.13.5完整160 tests/80.748s通过，无skip，原COMPILE/GUIDANCE-COMPILE通过。31项采集focused通过，Windows真实8.3路径fixture复现修正后通过。代码hash不再变化；仅更新当前状态/版本/记录并做结构/引用/index复核，实际提交再运行完整原committed门槛。24次组合结果是原1.6.0测量，本次不重复全量比较或声称新的耗时结果。


## 同批1.6.1托管报告复核与夹具环境隔离（2026-10-18T16:07:05.423454+08:00）

用户确认“已在GitHub批准”run39109363841；API确认审批已解除。进一步下载Ubuntu的原checker artifact发现required_checks_satisfied=false/TEST失败，而原有诊断路径重跑通过，因此作业success不能转写为原报告pass。Windows也进入相同诊断路径。

本地带ENGINEERING_TASK_ID=TASK-CONTEXT-RELEASE-01复现：checker fixture临时项目只含TASK-1，默认任务/partial生命周期测试误用主项目任务；init fixture的lite/full也同样误报。该问题来自旧fixture继承CI环境，非采集器或产品规则变更。方案只在这两个TestCase的setUp隔离外部任务/批准变量，并在cleanup恢复；显式测试环境变量优先级的用例仍自行设置值。保留全部断言、160项范围、原检查器/CI/时限。携带CI外部任务与批准变量跑完整commit/committed，确保原report直接满足必需门槛。

这是当前1.6.1托管验收尚未闭环时发现的同批测试可靠性修正；版本维持1.6.1，CHANGELOG补充实际修正，不改工程流程或重开用户规格。Skill review：沿用本轮已读engineering-workflow1.6.1及checker/implementation引用；范围仅旧fixtures环境隔离/验证回执，其他技能和多agent不适用。影响为tests与当前基线/Task证据，文档按已有门槛同步。


### CI fixture 隔离最终本地验证

- 已在真实外层变量`ENGINEERING_TASK_ID=TASK-CONTEXT-RELEASE-01`及`ENGINEERING_CONTROL_PLANE_APPROVED=1`下运行原160项TEST：官方Windows Python3.11.9为64.596秒，Python3.13.5为73.842秒，均全部通过。checker原commit门禁使用同一变量/原TEST命令与120秒时限，required_checks_satisfied=true；TEST67.485秒，COMPILE及GUIDANCE-COMPILE均通过，保护与commit-scope通过。未删测试、未降门槛。
- 修改只是在checker与initializer单测setUp隔离这两个由fixture拥有的变量，并以addCleanup恢复外层环境。显式的task ID环境变量优先级测试仍自设任务并通过。旧run39109363841的原checker artifact记录TEST fail；之后诊断重跑成功不等于原artifact通过，现作为失败历史保留。
- 当前Baseline/Plan更新至BASELINE-CONTEXT-05/PLAN-CONTEXT-05；SPEC-CONTEXT-03及需求范围不变。下一步以当前精确提交重跑committed并推送同一1.6.1批次；新的protected run需对精确SHA人工审批后才能验证两平台直接artifact。


## 保留的本地1.6.0交付回执（历史，不替代当前CI状态）

### 最终交付和本机安装回执（2026-10-18T06:54:32.139156+08:00）

- 最终提交`21f9aa23375b82866a35eea2c783da78eca63857`已正常推送origin/main并核对远程一致；原主提交502fd69保留。该实际提交的完整committed门槛通过，158项测试及原COMPILE/GUIDANCE-COMPILE、控制保护、变更/文档作用域通过；没有修改原120秒TEST时限。源码未再变化。
- 本机skill已经fast-forward到同一提交/1.6.0；原未提交研究文档、注册和版本任务改动保留。Windows同步首次被Git因checkout换行/状态拒绝，完整恢复备份后使用Git原生过滤重新物化并成功快进，没有reset/clean/stash。安装后结构/链接无错误、官方skill验证通过；Codex CLI三文件冒烟采集完整，91条可定位引用、24条未解析，出处验证通过。
- Pi1941文件/24880527字节、Codex6739文件/70764425字节，结束快照/文件集合/hash与初始完全一致；两目标Git状态仍为空。没有执行目标项目构建/产品测试或安装依赖。
- 最新[GitHub run](https://github.com/wang546673478/engineering-workflow/actions/runs/39076867717)的protected-path检测通过，Windows/Ubuntu reviewed作业等待既有engineering-control-review人类审批；不能记为托管全通过，未代替人类审批。
- 本次仅在本地补最终事实回执，原发布源码不变，不另升版本或反复提交回执。完整本机回执：`C:/Users/54667/.codex/experiments/context-release-1.6.0/evidence/final-receipt.json`；外部实验总结：`C:/Users/54667/.codex/experiments/context-release-1.6.0/REPORT.md`。这些本机路径不写入公开源码。


### 1.6.1实际交付回执（2026-10-18T15:54:50.214440+08:00）

- 最终提交`c6c3b2faafbf9b3c8a5fe2305b61dedf90549b0c`已正常推送并核对origin/main一致，安装副本同步同一版本，原本地研究/注册/1.6.0回执保留。原committed门槛在WindowsPython3.11.9通过，160项测试；3.13完整160项亦通过，skill官方结构及安装后manifest/引用检查通过。只修采集器兼容与测试fixture，原SKILL正文仅升版本；检查器、CI、原命令/时限和保护规则保持。
- [新Actions run](https://github.com/wang546673478/engineering-workflow/actions/runs/39109363841)目前protected-path通过，Windows/Ubuntu reviewed作业等待既有engineering-control-review人类审批。原失败run39076867717不能改记通过；已分别复现并纠正其中两项失败。当前未声称托管测试通过。
- 本机外部实际回执`C:/Users/54667/.codex/experiments/context-release-1.6.0/evidence/ci-fix-final-receipt.json`保存精确提交与测试报告；本段为结果记录，不再次上传无变化源码或重复未受影响测试。


### 1.6.1最终fixture隔离提交及Actions运行

- 2026-10-18T16:20:37.642034+08:00：精确提交`a407b112410e8717511d62fda8eead66d18cf043`已推送origin/main并核对一致。本地WindowsPython3.11.9 committed门禁通过：160 TEST、COMPILE、GUIDANCE-COMPILE、保护与committed-scope均pass；在提交前用同一实际CI外层变量执行原命令也全通过。安装skill已同步a407b11，官方结构验证及manifest/links验证通过，原未提交研究与版本任务保留。
- 新[GitHub Actions run](https://github.com/wang546673478/engineering-workflow/actions/runs/39110935645)：protected-path通过；Ubuntu reviewed作业的原检查直接通过、诊断重跑跳过；Windows reviewed作业仍在执行。待其完成后读原始artifact，不以job摘要替代报告。
- 老run39109363841保留为历史失败：其Ubuntu原TEST报告失败，而诊断后作业才通过；这是修复fixture变量继承的起因，不改写为成功。
