# TASK-ISSUE-23-PROPOSAL：真实会话审批与验证失真整改方案

## 当前状态

- 日期：2026-10-21（Asia/Shanghai）。输入源码：`d214021`，engineering-workflow `1.7.2`；开始时工作树干净。
- 本轮授权：在已展示完整Plan r1及兼容性影响说明之后，用户于2026-10-21T10:38:03+08:00明确“那就开始实施吧”，授权本地实现和验证。最初“需要你拿出方案，把细节写清楚”是前序调查范围，已由后续指令推进。
- 当前阶段：本地实施与验证完成；用户批准范围内T23-01..08完成，版本1.8.0 / Unreleased。最终实现原门禁required_checks_satisfied=true；源码已上传GitHub main，全局安装/外部项目迁移未执行。
- 输入：[Issue #23](https://github.com/wang546673478/engineering-workflow/issues/23)，创建时间 2026-10-21 03:24:00+08:00；最新目标会话 `01a15a6d-3a4a-7713-94c6-4b2e757294f6`，读取时仍 active，已读三个 turn。本结论绑定读取快照，不推断之后的行为。
- 已证实：需求选择后直接开始实现；目标项目仍引用旧任务/旧 Plan 的授权；当前检查器对启用生命周期的清单已有证据文件存在性校验，但未验证原话、时间、范围，legacy 无 stage 不启用生命周期门槛。
- 当前链路：BASELINE-ISSUE23-02 → [SPEC-ISSUE23-01](issue-23-spec.md) → [PLAN-ISSUE23-01 r1](issue-23-plan.md) → 本Task / T23-01、02 → [调查证据](issue-23-evidence.json)。
- 当前结果：按用户“上传github”完成原暂存区及提交门槛，实现源9723921已上传origin/main并核对一致；当前补源上传回执。全局安装、目标项目迁移、tag/Release未执行。

## skill_review

清单来源：本会话 Skills catalog，检查日期 2026-10-21。恢复读取本仓库 AGENTS、SKILL、manifest、Baseline、上一任务及总 Spec/Plan；按阶段读取 implementation-workflow、requirements-interview、checker、baseline-linked-artifacts、project-documentation、adoption-lifecycle。

| 候选 | 来源/版本 | 决定与理由 |
| --- | --- | --- |
| engineering-workflow | `SKILL.md` 与本机已安装 `C:/Users/54667/.codex/skills/engineering-workflow/SKILL.md`，均 1.7.2；仓库基点 d214021 | 采用；用户明确调用，继续本仓库权威状态体系 |
| skill-creator | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`，未提供版本 | 采用；评估 skill 改进范围、渐进披露与可验证性；本轮不改 skill、不委派 |
| planning-with-files | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md`，2.37.0 | 不采用；复用现有 Baseline/Spec/Plan/Task 和清单，避免另建平行台账 |
| triage-issue / request-refactor-plan / to-issues | 本会话清单中的同名技能，正文未加载 | 不采用；任务是调查现有 issue 并在本地写方案，不是创建 issue、重构访谈或发工单 |

没有安装、运行外部代码或创建子 agent。GitHub 公共只读 API 已足够获取 issue，未使用 PAT，也未写入文档。目标项目只读；其活动会话继续独立运行。

## 调查进度与限制

1. 已读取仓库现行流程和当前完成的 Issue 22 记录；原三项增强及其未完成的全量上游审读范围保留，不挪用其批准。
2. 已读取 GitHub 最新非 PR issue #23 正文；无评论；#22 是前序增强，非本次新增批准。
3. 已通过 read_thread 读取目标会话三个 turn，并读取目标项目任务/清单、需求和交付回执；不复制账号、企业名称、口令或完整原始工具输出。
4. 已核对检查器函数、调用点、兼容入口、测试与报告语义。五项真实CLI隔离反例均复现现有checker放行：空证据、占位证据、当前Plan不匹配、未来批准时间、legacy无效旧授权；这不是修复通过。本地临时Git夹具已自动清理，复现脚本与摘要保存在evidence。
5. 详细Plan覆盖D1..D7逐项结论、结构与scope绑定、原例外/批准复用、迁移/降级保护、顺序证据边界、汇报和原测试计划。候选八项REQ/AT及Plan/Task映射已入清单和traceability；旧批准未转移到本任务。
6. 单次案例不支持 issue 的90/50分量化评分，也不能证明所有agent都会如此。目标第三轮仍active，尚未核验其后数据操作或完成结果。目标文件独立读取并记录摘要，不声称得到全工作树一致快照。

## 影响与发布

本轮实现可选批准合同与相应CLI参数/模板/迁移工具，scope和snapshot核验对strict有意变严。保持required checks、control_plane声明/外部信号与原stage、sync、command/timeout不变。旧清单只显示非必需覆盖诊断，新初始化默认diagnostic；不自动迁移外部项目，不改产品数据库。实际影响已按用户审阅的Plan执行。

版本：本批新增兼容能力从1.7.2升至1.8.0 / Unreleased，五处原元数据同步；无提交、推送、GitHub评论/关闭、全局安装或部署。

## 验证

- `git diff --check`通过；本批JSON可解析、Markdown本地链接存在、REQ/AT与document引用及change-scope/文档影响检查通过。
- 当前原checker执行：`python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base HEAD --task TASK-ISSUE-23-PROPOSAL --report work/issue-23-review/impact-confirm.json`，exit=1、errors=[]、required_checks_satisfied=false。原因为TEST/COMPILE/GUIDANCE-COMPILE未运行；旧legacy生命周期及database/contracts可选清单为非必需partial。没有required fail/partial被隐藏。
- 原准备批次仅调查和方案、未跑全量的记录保留在proposal_validation。当前已改runtime/skill并执行完整回归；正式三项结果见本Task最终实施验证。本记录不把结构检查通过说成整个工程门禁通过，也不复用上一批报告。
- checks/control_plane/exclude_paths/modules/inventories相对HEAD逐项一致；当前change模式不需要提交控制面的外部信号，没有设置该信号。当前检查只能证明声明的文档/范围覆盖，不能批准候选方案或证明其未来行为。
- 调查反例、原报告摘要和静态验证结果汇总在[机器证据](issue-23-evidence.json)。

## 决定记录

- 2026-10-21：用户原话“需要你拿出方案，把细节写清楚”，授权本轮调查与方案文件；不表示批准尚未展示的候选实现。
- 本轮采用的工程建议：原节点澄清 + 显式启用的结构/范围检查；顺序先辅助诊断。它们是agent提出的候选，不写成用户决定。
- 2026-10-21：用户询问“如果按照这个plan进行更改,会不会改变原有skill检查校验同步等流程?” 已记录为重要范围/兼容性关注。本答复结论写入Plan第1节：审批校验会影响strict模式的门槛结果；原required测试命令、工程检查执行合同和影响分析后的文档同步顺序保留。新项目初始化默认是否启用strict仍为待定，不能静默决定。
- 本轮交付内容为proposal和证据，1.7.2不变。未来完整新增能力建议1.8.0 Unreleased；文字澄清单独批次才适用1.7.3。具体版本与控制面批准待实施范围获批后执行。

- 验证历史：复查时重复使用已存在的report路径被原checker正确拒绝（exit=2）；先用final-confirm.json取得fresh结果（exit=1），本次方案补充后再用impact-confirm.json取得fresh结果（exit=1）。旧路径拒绝不作为本次成功证据，原始状态保留于evidence。


## 实施授权与进度 / 2026-10-21

- 用户原话：“那就开始实施吧”。前序已审Plan r1及最后说明明确兼容策略，本指令按原skill规则同时覆盖方案与实施，不重复审核；Spec/Plan批准时字节在work/issue-23-review/approved-r1留存。
- T23-03..08进入实施；新合同为diagnostic/strict，默认diagnostic，旧清单无policy保持兼容；有意收紧strict审批校验、保留原工程测试和同步合同。
- 首轮焦点测试先失败（缺功能），首切片5项已通过；测试失败/修正过程保留为开发记录，不作为最终完成证据。


## Implementation progress before final verification (history)

- T23-03: complete in source; original guidance now distinguishes goal/choice from unseen Plan approval, preserves explicit conflict sources and reports checker versus manual verification separately.
- T23-04: source implemented; structured record/reference/subject/scope/REQ/AT/current revision, optional task approval and explicit reuse validation. Strict failure prevents commands; original legacy behavior retained with nonrequired coverage diagnostic.
- T23-05: source implemented; diagnostic initialization, explicit strict option, migration preview then atomic apply, historical policy weakening guard and optional hook capability argument. Preview uses in-memory proposed manifest checks, never a stale on-disk version.
- T23-06: source implemented; declared same-timeline sequence gives pass/fail/partial, default nonrequired; timestamps are not proof of ordering.
- T23-07: in progress; focused actual CLI tests passed in multiple slices, original full regression running in task venv with pinned Rust parsers and script-disabled npm installation. Development failures/fixtures corrected; final source needs fresh required-check evidence.
- T23-08: in progress; version 1.8.0 Unreleased synchronized in five metadata sources; B/M/C/F and active artifact references updated. No commit, push, global skill install or external project mutation.


### 原回归问题与修正（阶段记录，最终结果见下）

- 首轮原全量命令223项、148.782秒，6项失败，未当作通过。历史检查前置改变了缺Git/浅克隆诊断，已移动到原作用域/控制门槛之后；原JSON深度及损坏历史断言在Python3.14暴露解码器行为变化，已按解释器现有递归预算保持原拒绝边界，不调高限制、不引入文件大小限额。四个原失败测试方法复测通过。
- 新增strict/diagnostic/legacy、当前scope/revision、未来时间/重复JSON/路径、复用、小修例外、sequence、真实commit/committed、迁移预览/保留失败及工具能力测试。原断言未降级，已更正的开发失败与最初原报告保留。
- 当前正在重新执行原全量命令；只有原120秒正式TEST及两个编译门槛实际满足后才交付通过结论。

- 修正后Python3.14全量225项全部通过，耗时134.907秒，超过原TEST=120秒，不能作为正式门禁通过；正减少重复Git历史读取和静态合同测试的额外解释器启动，保持原断言与覆盖。沿此前已验证的Python3.11范围准备任务局部运行时，仍执行原命令/原超时；没有改系统Python、注册表或全局PATH。


## 最终实施验证与交付 / 1.8.0 Unreleased

- T23-01..08完成：原节点指引、结构化批准/审阅快照/当前范围/有效复用、policy历史保护、顺序诊断、初始化/迁移预览与原子应用、hook能力参数、原回归及全局文档/版本同步。
- 最终正式命令：任务局部CPython3.11.15，原 `check_project.py --mode change --base HEAD --task TASK-ISSUE-23-PROPOSAL --run-checks --report work/issue-23-review/formal-final.json`，exit=0、errors=[]、required_checks_satisfied=true。TEST=225项通过，119.750秒；COMPILE=0.219秒；GUIDANCE-COMPILE=0.218秒。原120/30/30秒及命令/控制面声明未改。
- 最终报告还有四个非必需partial：本仓库旧生命周期未迁移、批准内容legacy_unverified、手工数据库清单、手工接口清单。它们如实保留，未写成自动语义核验成功；strict实现已由真实CLI/Git的独立合成项目回归覆盖。
- skill-creator quick_validate通过；JSON/链接、五处版本、PowerShell hook语法及git diff --check通过。最终原检查后只补状态/证据文档；runtime/测试/模板摘要复核未变，因此不再重复未受影响的全量测试。
- 保留首轮失败及Python3.14功能全过但134.907秒超过原TEST上限的证据。最终正式通过基于CPython3.11.15；当前环境3.14没有达到120秒正式门槛，不将其说成两环境正式全绿。119.750秒接近原上限，较慢环境仍可能超时；不得通过升上限或诊断重跑冒充原结果。
- 原批准原话、实际会话消息ID、10:38:03+08:00事件时间、记录时间和批准时文件SHA在evidence/manifest中分开保留。所有需求按SPEC-ISSUE23-01冻结范围实施，Plan技术细则和事实基线BASELINE-ISSUE23-02同步；未迁移采用项目，未改业务数据库。
- 同agent源码/桌面场景复核S23-01..05记录其边界；不是独立模型行为认证。工具仍不能证明真实人类批准、语义等价、漏声明源码或所有后续agent遵守。


## GitHub源上传 / 源提交完成

- 2026-10-21T13:35:58.671837+08:00，用户原话：“上传github”。覆盖前述完整已审实现和文档，执行原commit/committed、必要一次性外部控制面批准及推送核对；不创建标签/Release，不改全局安装或外部项目，不发送issue评论。
- 远端main起点仍d214021d8c462d5b7733d0cb3f04a26f8f3bb35b；当前分支codex/issue-23-approval-contract，保持原全部变更与验证。36项待上传文件未发现PAT模式，runtime/模板/测试摘要与最终正式报告一致。
- 控制面影响按已审Plan：strict证据/范围/策略降级更严格，新旧项目兼容与原TEST/超时/同步/外部批准来源保持；本次明确上传指令覆盖这些已展示变更，检查只使用本进程一次性批准信号。
- 状态/回执本身不改变已交付内容，不另升1.8.0；暂存和提交门槛结果随后记录。


### 源上传回执 / 2026-10-21T13:42:38.686116+08:00

- 实现源提交 `9723921ceac69db363fb4b655d761bc61b956e0f`，tree `4165482e1a8b8cf781e1de56a545128540dcbdf2`；origin/main已由ls-remote核对同SHA。版本1.8.0仍Unreleased，只上传Git源码，未创建Release/tag。
- 原commit/committed检查均exit=0、required_checks_satisfied=true，TEST各116.500秒、两个编译检查通过，control-plane/树一致性通过；报告与完整结果保存于evidence.github_upload.submission_gates。原四项非必需partial继续保留。
- 当前回执仅更新事实/状态，不改变产品或验证对象，不另升版；后续回执提交仍运行原提交门槛，结果不替换上述实现源证据。托管CI另行记录，不把本地单次批准转移为GitHub环境审批。

- 2026-10-21T13:51:44.770519+08:00：实现源9723921的GitHub run39551012856已完成，reviewed Ubuntu、Windows与quality全部success。回执暂存门槛upload-receipt-commit首次TEST在120.016秒超时，保持失败证据，不改原命令/超时，不复用实现源/托管成功充当该次回执通过；当前重新执行新回执树的原完整门槛。

- 2026-10-21T13:58:26.867773+08:00：回执第二次原TEST仍120秒超时，随后完整诊断225项通过但127.107秒，不算门槛通过。已核对当前默认Git为旧版2.47；后续使用应用打包Git2.53，在任务进程PATH内选择，原命令/用例/上限不变。所有失败及诊断独立保存。


### 同批保持行为的性能修正 / 2026-10-21T14:04:47.303332+08:00

- 原实现源9723921已上传且本地/双平台CI通过；上传回执原门禁重复超时，所有失败保持。当前同批补充：control-plane与approval-policy-history在一次CLI调用内复用已安全读取的同一历史manifest，缓存每次main新建，跨调用/仓库不共享；各原Git历史/浅克隆/损坏策略检查仍先执行。
- 静态批准合同测试复用原公开main入口，保留同样用例/断言；真实commit/committed仍用独立CLI/Git仓库。原checks、120/30/30秒、控制面和业务边界不变。该修正仅缩减重复技术工作，不变Spec用户行为，不新增审核；按既有同批开发规则保持1.8.0 Unreleased。
- 本次两个源码摘要已改变，原报告保留为9723921历史证据；新源码必须重新通过原commit/committed门槛才提交和推送，不能沿用旧通过。
