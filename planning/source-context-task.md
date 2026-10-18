# TASK-CONTEXT-RELEASE-01：来源辅助功能交付与受保护 CI 判定修复

## 当前状态和用户授权

- 2026-10-18恢复实施：远程 `main` 仍为已发布的1.6.1提交 `a407b112410e8717511d62fda8eead66d18cf043`。用户授权按全局根因修复并上传。当前确认 reviewed 与 manual-reviewed 两路会在原始 checker 失败后重跑测试，并允许诊断成功覆盖原始失败；这会让汇总 job 误报通过。当前批次修正这两条最终判定路径，诊断仍保留用于定位；旧命令、测试范围、120秒时限和人工批准职责不变。保留未提交的 Windows reparse fixture 路径规范化修正并纳入本批验证。SPEC-CONTEXT-03不变，候选发布版本1.6.2 PATCH。Task保持 `in_progress`，直到精确提交、本地门禁、上传及可核验的托管结果更新完毕。
- 下一步：将已通过门禁的暂存树提交，随后运行 committed 检查；上传后核对新 SHA 的原始 hosted artifacts。新 SHA 的环境人工审批不能从旧 run 继承。
- 历史暂停记录（2026-10-18T16:32+08:00）：当时尚未完成Windows fixture follow-up 验证；暂停状态只适用于此前回合。run39110935645 的 Ubuntu 原 TEST artifact 通过、Windows 160 项中1项失败，JSON回执污染已从备份恢复；这些历史失败保留，不作为当前版本通过证据。旧run39109363841原TEST失败artifact也保留；诊断重跑成功不替代原始门槛。
- 用户原话：“这样你把多测试几个功能组合和排序,这几个功能都是需要只不过要完善使用规则,应该怎么组合,然后进行测试,E:\pi-main和D:\agent-harness-research\codex 这几个应该够你测试了,你找出最优,在不改变skill流程的情况下,把最优的上传github”。明确授权比较、完善规则、在已讨论辅助功能内择优正式实现并提交上传；不要求额外同范围批准。排序限辅助能力的调用/展示顺序，原阶段/需求确认/方案批准/门槛职责不变。
- 保留七项组合：盘点、树/统计、完整紧凑阅读包、限额/遗漏、引用分析、出处/图校验、图/文字/表格与源码定位；Token计量仅实验，Notebook/增量缓存/云模型链不引入。
- 本轮原清单/研究文档有未提交工作，完整备份在外部primary-original。发布从干净远程基点构建，只带本批实现/文档/摘要证据；保留旧评估原文件，不把它们混作新审批。
- 两个目标仅作只读语料；不运行其产品/模型/依赖安装、不改Git状态或源码。初始hash和实际Git状态在外部evidence，按每项目规则读取适用文件。

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


### Windows reparse fixture path normalization follow-up

- 2026-10-18T16:24:58.110504+08:00：新Actions run39110935645 的Ubuntu原artifact直接通过；Windows报告TEST fail1/160，唯一失败test_reparse_directory_without_junction_api_is_not_followed，原始日志保存在外部experiment。原因是fixture target使用临时目录原路径，而采集器root已resolve，Windows路径别名下两Path不相等，模拟lstat未命中。
- 不改产品逻辑。fixture先创建目录再resolve target，只规范化测试比较的目标。已在本机以真实Windows短路径root运行两项reparse-focused用例通过；接下来在完整WindowsPython3.11和真实CI环境变量下执行160项及提交门禁，并以新提交重新取hosted artifacts。


## 受保护 CI 判定修复（1.6.2）

### 当前决定、范围和授权

- 用户原话：“那就进行修复然后上传github”。该指令承接此前“从全局看流程是否有疏漏”的根因调查，授权修正已展示的保护 CI 判定缺陷并上传；实现范围为 reviewed 与 manual-reviewed 两路的最终结果规则、共享终结脚本、针对性回归和直接受影响的权威文档。
- Run `39110935645` 的原 Windows checker artifact 为 `TEST=fail`，诊断重跑为成功，而 job 为 success。两路 finalize 的条件均允许 `CHECK_OUTCOME=failure` 时只要 `DIAGNOSE_OUTCOME=success` 就成功；aggregate 因而把诊断结果当作原始必需检查结果。
- 采用统一的 Python finalizer，并由两条受保护路径调用。只有原始 checker 成功才成功；原始失败无论诊断重跑成功或失败都保持失败。诊断步骤继续输出详细错误以便调查，不改变原 TEST 的职责。
- 不改 Spec、阶段顺序、审核/批准门槛、checker 声明命令、测试范围或120秒超时；不新增依赖。恢复并保留先前未提交的 Windows reparse fixture 规范路径修正；测试目标项目仍只读。
- 版本从1.6.1升到1.6.2 PATCH：修复已发布的 CI 结果判定行为，不新增用户功能或改变兼容接口。同步 SKILL/README/agents/VERSION/CHANGELOG。
- 影响视图：治理流程、CI 合约、模块地图、Baseline、Plan、Task、Traceability 与机器证据。SPEC-CONTEXT-03、REQ-CONTEXT-01..05 和原测试义务保持不变。
- 对受保护 workflow/helper、manifest/CODEOWNERS、checker contract、版本元数据和 CHANGELOG 的本批授权来自上述用户指令；人工托管环境审批只对新精确 SHA 生效，不能继承旧 SHA 的批准。

### Skill review 与实现计划

- 检查来源：当前会话 Skills catalog，检查时间2026-10-18T16:50:42+08:00；采用当前发布副本的 engineering-workflow 1.6.1，并重读其 SKILL.md、AGENTS、manifest、活动 Task、checker、implementation-workflow、baseline-linked-artifacts、Baseline/Spec/Plan及受影响治理视图。
- engineering-workflow：adopted，授权范围内修复并按提交/committed/托管证据闭环。
- skill-creator：adopted；已读 SKILL.md 与 `references/openai_yaml.md`，用于同步1.6.2版本元数据并执行 package validator；不调整 invocation/UI 结构。
- PL-CI-01：修复两个受保护 finalizer 并防止逻辑分叉；PL-CI-02：验证脚本及 Windows/Ubuntu 运行兼容；PL-CI-03：完整跑原 TEST/COMPILE/GUIDANCE-COMPILE 和精确提交门禁；PL-CI-04：上传后按新 SHA 逐平台核验原始 artifact 与总 job。

### 验证与发布状态

- focused finalizer regressions：3/3通过；覆盖原始检查成功/失败与诊断跳过/成功/失败组合。
- Python 3.13.5 task-local isolated environment下原 TEST 命令163项通过，用时73.313秒，低于120秒；初次裸Python3.13运行因缺少锁定tree-sitter依赖4项失败，确认后复用已准备的隔离环境完整重跑通过，不修改产品源码或测试期望。Python3.11本机无安装，后续由 hosted Actions 的原Python3.11环境复核。
- Skill Creator `quick_validate.py` 在UTF-8模式下通过；workflow YAML由PyYAML解析通过，两个受保护job都调用同一finalizer；新文件Python编译与 `git diff --check` 通过。
- 第三次 commit 门禁通过：`required_checks_satisfied=true`；TEST 163项/72.78秒、COMPILE 0.11秒、GUIDANCE-COMPILE 0.12秒，control-plane 与 commit-scope 均通过。调用的是原声明命令，任务/批准变量仅在本次子进程中存在；为让Windows子进程可见锁定解析依赖，本地 `PYTHONPATH` 指向任务隔离环境。
- 两次未通过的准备报告保留：首次因 `.github/CODEOWNERS` 未被声明为文档影响路径而阻止检查执行；补上路径后，第二次因嵌套 Python 子进程解析到缺少解析依赖的基础环境而TEST失败。定位后通过任务局部 `PYTHONPATH` 重跑，未修改原命令、超时或测试范围。
- committed 报告：待提交后运行；受保护变更仅在此次本地检查子进程使用经用户授权的短时外部批准变量。
- GitHub 上传和远程 SHA：待执行。新 push 会触发新的 protected run；若环境要求人工批准，等待用户批准后再读原始 Ubuntu/Windows checker artifact 和 job 结果。
