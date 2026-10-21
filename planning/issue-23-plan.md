# PLAN-ISSUE23-01：真实会话审计与批准门槛补强

当前交付（2026-10-21）：批准范围内本地实现及原正式检查完成，1.8.0 / Unreleased；最终源与验证、可选partial及平台限制见[当前Task](issue-23-task.md)。本条为当前状态，下面准备/执行进度保留历史范围。

当前实施状态（2026-10-21）：用户“那就开始实施吧”批准已展示完整方案及影响说明；本轮本地实施与验证完成，诊断默认、strict显式启用。批准与执行证据见[当前Task](issue-23-task.md)。下文原draft/pending措辞保留为准备历史，不代表当前授权。

版本：r1（批准依据），2026-10-21，当前本地实现与验证完成。最初候选文本及SHA保留在Task/evidence；本页技术细则按批准范围更新。依据：`BASELINE-ISSUE23-01`、源码 `d214021` / 1.7.2、候选 [SPEC-ISSUE23-01](issue-23-spec.md)。当前任务：[TASK-ISSUE-23-PROPOSAL](issue-23-task.md)。

## 1. 结论与推荐范围

Issue #23 值得处理。主要问题是**需求答复被扩成实施批准，旧批准没有与新批次绑定，用户看见的结论没有保留工程门槛的失败状态**。单加“用户原话/时间/范围”三行可以降低遗漏，却不足以挡住旧审批复用到新权限改造。

建议做一个兼容的两层补强：先纠正原有指引和交付表述，再给明确启用的项目增加结构与范围校验。顺序核验先作辅助证据，不使用文件 mtime/Git 时间作为硬门槛。继续复用原工件、原批准节点和原测试执行机制，不增加每答一个问题就审核一次的流程。

当前用户已授权完整本地实施；交付版本为 **1.8.0 / Unreleased**（新增兼容的可选检查能力，MINOR）；如果只采纳文字澄清，独立批次可用 1.7.3 PATCH。两个范围不能在交付时混称完成。

### 对原检查、校验与文档同步流程的直接影响

结论：**会改变审批相关的校验门槛和结果判定；不会替换原有工程检查及文档同步流程。** 因而不能概括为“完全不变”，也不能理解为“整个流程要重做”。

| 部分 | 按本方案实施后的影响 | 保持内容 |
| --- | --- | --- |
| Spec/Plan/Task讨论 | 用户确认目标或回答选择题，仍按原访谈流程记录；完整展示后的明确实施指令仍可一次覆盖方案与实施，不增审批轮次 | 原 Baseline→Spec→Plan→Task 顺序、模块核对、需求/实施状态区分及批准复用例外 |
| 批准证据 | 新增可选 `approval_policy` 合同；启用后approved记录除现有证据路径外，还须含结构化原话/时间/范围和与已审Spec、Plan及本批范围的绑定 | 原批准种类、原approval_required含义、现有task/task依赖和控制面外部批准机制；有效旧批准不重问 |
| change/handoff/commit/committed判定 | strict合同启用且批准声明缺字段、错批次或依据已变时，相关实现门槛可能由pass变为fail；提交模式仍先检查、失败不运行声明命令。默认顺序诊断只给partial/fail线索，不升级为必需门槛 | 原mode、Git暂存/提交树复核、verified_tree、命令执行与失败语义；不启用合同的既有清单不因本方案自动失败 |
| 新项目/迁移 | 方案r1目前写“完整初始化提供合同”，这会使**新初始化项目**默认走更严格的审批检查，即便旧项目兼容。该条需要在最终方案明确选择“默认启用”还是“显式选择后启用”；在此决定前不得实现成静默默认 | 不回写或批量迁移已有项目；诊断、diff、用户确认、原子升级和历史保留 |
| TEST/COMPILE等 | approval-evidence逻辑增加相应checker/init/adoption测试，新增验证规则结果 | 已声明 TEST、COMPILE、GUIDANCE-COMPILE的命令、required标志、超时/输出限制不替换、不降级；不以手测代替原命令 |
| Baseline/文档同步 | 新增批准记录合同及其调用关系，必须同步checker contract、adoption说明、module map、business flow、traceability、Plan/Task和版本记录 | 原按模块/契约/数据库影响分类更新文档，再跑change/commit/committed检查的同步路径；不会以新批准记录取代原影响分析 |
| 交付表达 | 要求把checker门槛结果与独立测试、未决审阅分开说明 | 原检查器report字段和退出码保持；errors=[]仍不等于required_checks_satisfied=true |

因此，严格模式下**批准相关的pass/fail结果确实会更严格**，这是有意的行为变化；测试集、测试命令和普通文档覆盖规则不拟改变。版本建议1.8.0包含此可选新校验能力。我的建议是：旧项目保持兼容，迁移后显式启用；新项目先生成pending合同并报告缺口，只有项目明确选择strict后才把它作为阻断门槛。这样不会让初始化或升级静默改变实施门槛。用户随后“那就开始实施吧”已覆盖此前展示的这一默认策略；当前实现采用diagnostic默认、strict显式选择。

## 2. 证据范围与真实时间线

GitHub 最新非 PR issue 为 [#23](https://github.com/wang546673478/engineering-workflow/issues/23)，2026-10-21 03:24:00+08:00 创建，读取时无评论。原 issue 的 90/50 分是作者判断，本调查不采用为测量结果。

目标会话：`01a15a6d-3a4a-7713-94c6-4b2e757294f6`；本次通过 read_thread 读取全部三个 turn。读取时最后一轮仍运行，因此本方案只评价已有消息/文件，不推断其后完成情况。脱敏消息定位在 [会话证据](issue-23-session-evidence.json)，不把账号、企业名、口令或完整原始工具日志纳入仓库。

| 顺序 | 可核对事实 | 结论边界 |
| --- | --- | --- |
| 第一轮 | 用户指出企业 Key 应只看到所属组；已有 GRP-REQ-06。agent 修复并跑产品测试，最终向用户报告三库及前后端测试通过 | 这可以按既定需求的小修分析，不把它直接等同后续重大用户系统改造 |
| 第二轮 | 用户要求正常用户管理支持六种角色，表达“分组决定角色、倍率是分组天然属性”，并请求重建本地测试账号；agent 调查、备份后询问企业管理员/成员如何共用价格组 | 用户明确表达目标及本地数据操作意图，但完整改造 Plan 尚未展示 |
| 第三轮开头 | 用户选择“每家企业保留一个价格分组，在用户上另选管理员/成员身份”；agent 随即表示“我会据此改造原生用户创建、编辑和归属分配流程” | 可确认这个企业内部结构选择，不能扩大为尚未展示的完整 Plan 审批 |
| 同轮工具顺序 | 命令 `exec-6cbb3aa4-9cf9-41a2-ab19-e0207f1e2727` 写入“当前执行决定”、P1–P6、Spec0.6-confirmed；随后 `exec-ddd4f3fc-1e20-4990-83dd-13d645b43054` 修改 model/user.go 并新增 service/managed_user.go | 可见方案形成与实施在同一轮，中间没有用户对完整方案的回复；不能据此得到每个工具项的精确墙钟时间 |
| 清单快照 | 当前 task Plan=20261021.3，implementation_authorization 仍绑定 Plan=20261020.1-approved，scope 是上一批菜单/页面复用/利润报表/Chat控制 | 旧授权不能自动覆盖新批次；workflow 无 stage，生命周期严格门槛没有启用；workflow当前revision和Task指针还存在漂移 |

目标项目 HEAD=`6cf0d90b5ff27f901697dddd61e0c28aba8efefc`，存在活动工作树，HEAD 不能代表此次未提交改造内容。选取文件摘要及读取时间见 evidence，目标目录全程只读。

## 3. 对 Issue 审计项的判断

| 项目 | 核对结果 | 拟处理 |
| --- | --- | --- |
| D1 未展示完整方案即实施 | 对第三轮用户系统改造成立；并非所有修复均需重开完整审批 | 明确重大新范围进入方案确认；选择题回复只更新对应需求 |
| D2 需求矛盾被消解 | 原原则与企业身份另选有张力；用户确实主动选择了第二项，不能说选择不存在，也不能自行扩成所有身份与分组均脱钩 | 复述“企业内部身份为例外；其他身份是否仍由分组决定”等受影响范围。只有实际未决时问一次；明确变更原则的原话可直接记录，不强制二次确认 |
| D3 冻结范围扩大 | Spec0.6整体confirmed而证据只覆盖一项选择，文件顶部缺清楚的逐项确认边界 | 保留已确认选择，其他新范围候选；按批准的REQ集合和方案快照绑定实施 |
| D4 自授权 | 当前Task确有“不另索取重复批准”；第一轮写清单的命令曾出现default-consent implementation request，当前清单已被后续内容替换 | 这些称谓不是批准来源；保存原话及适用范围，旧批准失效只影响相应批次；不能凭词语本身推断用户一定从未授权 |
| D5 汇报模糊 | 第一轮交付报告工程 required_checks_satisfied=false，含required inventories partial、CORE-1依赖fail及命令skipped；最后回复只强调产品测试成功 | 产品测试可真实通过，但工程门槛未全过；二者必须同屏说明。errors=[]只是没有配置/执行异常，不等于门槛成功 |
| D6 数据重建 | 备份存在；最新轮读取时仍执行，不能证明清空已完成，也不能认定未完成数据操作已违规发生 | 复用已有影响记录补旧Key/会话/归属/历史数据处理与恢复点；本地指定测试口令不复制入审计，不推广到其他环境 |
| D7 模块审核 | 第三轮进入实现前未见完整需求/变化/待定/影响集中核对 | 与完整方案展示合并一个可审阅结果，在同一条明确回复实际覆盖时复用，避免新增固定轮次 |

## 4. 当前检查器到底缺什么

相关代码：`scripts/check_project.py` 的 workflow_lifecycle_gaps（约288行）、implementation_gate（约394行）、validate_manifest中的legacy分支和task-gate（约820/842行）；初始化/迁移位于 scripts/init_manifest.py 与 scripts/adopt_project.py。

- 已有：启用workflow.stage时，baseline/proposal批准证据路径必须存在；实施授权必须有证据文件、匹配选定task_id及proposal revision。task.approval_required=true也有证据文件门槛。
- 缺失：不读取批准证据内容，不要求原话/时间/范围；授权与proposal彼此相等也可能一起落后于当前Plan；不绑定当批REQ及已审内容；不验证先展示再批准的顺序。
- 兼容入口：没有workflow.stage时，workflow-lifecycle为非必需partial，implementation_gate不启用。目标项目正在走此路径；其task.approval_required=false也不会启用旧task-gate批准检查。
- 输出事实：required_checks_satisfied由所有required检查的原结果决定；errors为空不意味着pass。原始报告已保留失败，主要展示缺口在agent汇报，不能把产品测试通过反写成checker通过。

### 已运行的隔离反例

使用当前仓库原测试夹具生成独立临时Git仓库，执行真实CLI `change --base HEAD --task TASK-1 --run-checks`。fixture命令为独立无副作用unit，不运行目标项目测试。五例现有checker均exit=0、required_checks_satisfied=true：

1. 批准证据文件为空。
2. 批准证据只有字符串approved，无用户原话、时间、范围。
3. proposal和authorization都为plan-r1，但Task当前artifact_revisions.plan变为plan-r2-new-permissions。
4. approved_at写为2099年。
5. 去掉stage，授权指向无关旧Plan和不存在文件，legacy其他门槛满足仍通过。

这是缺口复现，**不是修复通过证据**。[机器证据](issue-23-evidence.json)保存输入方法、各检查原结果、源码摘要及复现脚本。覆盖的是声明验证边界，不认证人类批准或产品语义。

## 5. P23-01：在原节点修正行为指引

对应REQ01/02/06；先于新增检查实现。

1. SKILL只增加短原则：明确要求实施已展示完整方案可复用批准；提出目标/回答问题不批准尚未展示方案。详细边界放requirements-interview和implementation-workflow，避免主文重复。
2. 需求变化先记录：保留原则原文、选择原文、候选解释、影响REQ和范围。不为了“无矛盾”改写冻结Spec；已明确替换的决定按新revision记录，事实错误仍自主更正Baseline。
3. 模块收敛展示“已同意/改变/保留/未决/延后/影响”，再呈现完整方案及验证；本批若一条用户回复覆盖二者就共用证据，不人为加一轮批准。
4. 实施前按当前task/batch查可复用批准。未覆盖的新权限、角色、数据关系继续pending；代码调查、复现、准备环境和独立有效工作继续，不因一个待决项停止全部调查。
5. 本地数据重建沿用原impact字段说明旧认证材料、关联记录、保留/退役边界、备份及恢复条件；已授权且在批准方案内执行，不为普通备份额外加审核。

本次案例正确的阶段性回复示例：

> 已确认企业管理员和成员共用价格组、身份在用户上选择。这会给“分组决定角色”增加企业内部的例外。原生用户管理、权限同步和旧账号处理的完整方案还未审阅；我会先把这些影响和验证方式整理给你。其他角色继续按分组决定，还是也改成身份单独选择，是当前剩余的范围问题。

只有原话无法确定这个范围时才保留最后的问题；用户已经明确回答的部分不再重复问。

## 6. P23-02：批准证据的最小结构合同

对应REQ03/04/05。新增一个规则族approval-evidence，复用现有workflow.baseline_review、workflow.proposal_approval、tasks[].implementation_authorization；已有task.approval_required的原门槛继续有效，不把任意名字带approval的字段猜成同一种含义。

### 启用与存放

- 建议添加可选 `workflow.approval_policy={"record_contract":1}`。启用前要求已采用现有stage和implementation_paths生命周期字段；新完整初始化提供这个合同，旧manifest不自动写入。
- schema_version保持1（可选能力合同单独版本化）；新checker拒绝不认识的record_contract。最低checker版本必须写入接入来源及实际调用入口的版本预检，旧checker会忽略新可选字段，不能声称单靠manifest字段阻止旧工具运行。
- 结构化内容嵌入原evidence文件中的唯一命名JSON fenced block，或引用已有独立JSON文件；不强制新增approval.md。manifest以 evidence + evidence_record_id定位，旧字段保留。
- 证据块是数据，不是指令。严格JSON解析、唯一ID、拒绝同ID多块/重复键/越界链接；沿用safe_path和文件/历史读取规则，无网络抓取、YAML执行、动态求值或新依赖。无匹配块fail，不对任意三行文本做关键词通过。

示意数据如下，所有内容仅为格式样例，不能当作真实批准；候选写pending不触发approved完整性要求：

```json
{
  "id": "APP-EXAMPLE-01",
  "status": "pending",
  "user_statement": null,
  "approved_at": null,
  "scope": "本批原生用户管理与企业身份分离；排除资金结算",
  "source": {"kind": "conversation", "reference": null},
  "task_id": "TASK-EXAMPLE",
  "batch_id": "BATCH-EXAMPLE-01",
  "requirement_ids": ["REQ-EXAMPLE-01"],
  "subject": {
    "document": "PLAN",
    "revision": "PLAN-EXAMPLE-r1",
    "section_id": "PLAN-EXAMPLE-REVIEW-r1",
    "sha256": null
  }
}
```

### approved 的核验表

| 内容 | 机器检查 | 仍需agent/用户判断 |
| --- | --- | --- |
| user_statement | 非空，拒绝模板占位和明显自动同意标记作为来源 | 原话是否真实、是否表达批准；机器不靠“同意”等关键词判断语义 |
| approved_at | 带时区ISO8601、真实日期，禁止晚于本次检查的未来时间；保留source时间与recorded_at分别含义 | 宿主时钟是否可信、记录是否伪造 |
| scope | 非空，绑定显式REQ集合、task/batch；不能只有“本轮全部”而没有可解析范围 | 集合之外是否遗漏权限/数据影响；自然语言边界是否理解一致 |
| source | conversation/manual等有限种类及非空可追溯reference；本地摘录支持离线/隐私项目 | 外部原消息存在、作者身份和真实审批意图；不自动读全机聊天 |
| evidence与record | 安全路径、文件/块存在、唯一ID，manifest投影字段与块一致；重复冲突fail | 不能仅因文件可读推断人类批准 |
| subject | 文档ID存在；revision与本批批准依据匹配；检查可审内容摘要；实施授权匹配批准方案与task/batch | 技术调整是否仍在原批准范围，不能只由hash变化决定重审 |

baseline_review.subject绑定当时审阅source_revision/范围，不强制等于每次新的事实Baseline；没有推翻旧结论时保留原审阅。proposal绑定已审Spec/Plan版本；implementation_authorization可与proposal共用同一原话记录，但分别保留各自含义和范围，不新增用户动作。

proposal的subject除Plan快照外还须用`spec_basis`绑定Spec文档、revision、section_id及sha256，结构与Plan subject相同；实施授权引用该已验证proposal ID。只绑定Plan而允许Spec同ID正文被悄悄改写不能满足合同。源码事实基线则记录所依据的source_revision及有效旧review，不强制每次事实刷新重新审批。

字段按批准种类适用：baseline_review不要求绑定最新task/batch/REQ，审阅证据可服务后续仍受其覆盖的任务；proposal与实施授权才校验对应方案和实施范围。不要把实施记录的必填集合硬套到基线审阅，也不要用一个通用approved状态取代三种含义。

### 避免文档正常更新使批准反复失效

批准subject指向文档内明确标识、唯一的一段“审阅快照”；hash按UTF-8、LF规范化后的该块计算，不散列整份持续增长Task。路径、section_id、算法和内容规范化须写入checker合同并覆盖跨平台测试。

进度追加、证据补充、Markdown无语义格式整理不改变冻结快照。纯技术调整在原边界内时，Plan保留批准依据并记录当前revision与`review_basis_revision`及差异依据；agent核对仍覆盖原REQ/范围，机器只验证这个显式关系，不推断“等价”。新目标/权限/验收改变则生成新快照和pending批准，仅暂停依赖部分。禁止修改旧快照后保留旧hash，也禁止为了过门槛随意把新内容称为技术等价。

新批次若完全沿用仍有效的批准，不因batch_id变化机械重问：保存指向原证据ID的`reuse_of`及本批适用关系，机器核对来源存在、未失效、批准依据未变、本批REQ为已批集合子集；agent仍负责语义覆盖。新增REQ/改变快照无法由这个关系自动获得批准。旧引用本身不改写成新的用户发言，原时间和范围保留。

## 7. P23-03：范围、兼容入口与执行时机

| 模式/情形 | 原有门槛 | 新合同下结果 |
| --- | --- | --- |
| discovery/baseline的pending记录 | 自主调查、允许未完成资料 | 不要求用户提前批准；已声称approved的记录仍检查结构，不能以调查模式掩盖坏声明 |
| change且仅方案/记录修改 | 允许在当前任务写候选方案 | 新实现范围保持pending；不为了保存方案要求实施批准 |
| change涉及声明实现路径 | 现有生命周期实现门槛 | 在运行声明命令前核对批准合同、本task/batch及REQ覆盖；fail/required partial阻止把本批判作完成 |
| handoff/commit/committed | 原完成/依赖/控制面/命令/树一致性 | 同一批准验证函数复用；提交从暂存或提交快照读取匹配证据，不能偷读未提交版本；失败时不执行声明命令 |
| 显式旧清单、不启用合同 | 原legacy兼容检查不变 | 新批准覆盖诊断为非必需partial，报告legacy_unverified；不得把整体checker成功说成审批已核验 |
| 已启用合同后删除policy/stage/缩减范围 | 原控制面历史规则继续 | 比较父/索引/提交前策略，把降级纳入控制面变更；外部批准仍用既有单次信号，不在仓库写永久批准 |

旧清单诊断可识别当前任务已有implementation_authorization及本仓库的spec_review/plan_review字段，按它们的原含义报告缺口；不得自动把spec_review或task.approval重命名成proposal批准。严格合同通过既有adopt_project显式迁移到标准字段；迁移只链接有证据且覆盖正确的历史批准，其余保留历史、把受影响新范围pending。

迁移先输出可审阅diff和实际门槛变化，用户确认适用范围后再写。原子写入失败保持旧文件；不自动改required inventory、依赖、已有checks或超时。已批准且仍有效的事项复用证据，不要求为了字段升级重新审一遍业务；不能从“用户要求升级”制造原来没有的批准。

实现路径覆盖仍由声明控制。新合同不能发现所有漏登记路径，也不能拦截写文件；agent在首个产品编辑前使用现有change检查/impact复核，重大范围pending时先交方案。工具的提交门禁只能在调用时拒绝，并非宿主编辑前安全沙箱。

## 8. P23-04：顺序只按证据强度判断

不采用Issue建议的“证据文件修改时间<=首个实现Git时间”作必要门槛：后补进度会改mtime，checkout/rebase会重写时间，未提交文件没有可靠首改时间；这些会误判正常工作，也容易伪造。

第一版顺序诊断记录三件事：方案展示的来源ID、用户批准来源ID、首个实现事件来源ID。来源是同一宿主有序事件且可离线校验时，检查展示<批准<实现；同一条明确指令可复用多个批准含义，但不能让方案展示排在其后。

已知逆序fail；来源缺失/不同时间轴partial并说明未知，不从时间戳猜pass。默认该诊断非必需，不改变原兼容门槛；项目另行明确启用严格顺序证据时partial就阻止完成。第一版不内置各宿主聊天适配器、不要求用户上传完整对话；手工摘录只能证明声明顺序，不能认证人类。未来可信宿主回执属于延后独立能力。

## 9. P23-05：让交付结论保留真实门槛状态

不改变原report字段/退出码或命令证据权威。implementation-workflow和交付模板要求在同一次结论里给出：

1. **工程门槛**：mode、报告路径、源/树、required_checks_satisfied；列出required fail/partial/skipped/unsupported和依赖。errors=[]不能替代该布尔值。
2. **独立验证**：实际命令/环境/源码范围、结果、初次失败及重跑原因；手动通过不回填checker的skipped项，不替换原失败run，不宣称与原命令合同等价。
3. **仍未完成的范围/人工判断**：审批覆盖、未决业务选择、外部未知；整体任务和本批功能完成状态分别说清。

按目标报告改写的短回复可以是：

> 企业Key所属组修复已完成，三库回归和前后端测试通过。工程门槛尚未全部满足：两项来源清单仍partial、CORE-1依赖未完成，本次checker未执行声明命令。因此这次结果是功能修复验证完成，不能把整体工程任务标为完成。

没有采用新合同的项目仍要如实汇报原门槛；新规则的pass也只能说“声明结构和绑定已核验”，不能说“审批真实且完整”。

## 10. P23-06：实施位置、迁移与恢复

| 模块 | 拟修改 | 复用/保持/退役 |
| --- | --- | --- |
| instructions | SKILL短原则；requirements-interview冲突/范围；implementation-workflow交付与改前复核；baseline-linked-artifacts批准依据；checker/adoption说明 | 复用原节点和工件，旧“文件存在即可代表完整批准证据”的解释退役；不删除legacy读取入口 |
| templates/init/adoption | 原spec-plan-task/decision模板给可选证据块；init_manifest生成标准合同；adopt_project显式迁移和版本预检 | 同一份记录被多个批准引用；旧项目不自动重写；pending占位不伪装approved |
| checker | 在现有受保护check_project.py中集中证据解析/绑定；validate_manifest、lifecycle、implementation与提交读取调用 | 不增CLI模式、不移出受保护入口、不改变命令/进程/JSON安全合同；报告新增rule可逐项解释 |
| tests | 现有checker/init/adoption测试扩展 | 旧file-only成功fixture保留用于兼容；新合同fixture用真实结构，不能修改旧断言把兼容失败藏掉 |
| governance | Baseline、module-map、contracts、business-flow、traceability、Task、版本/CHANGELOG | 数据库字典复核不适用：无产品DDL/业务数据；适配器边界不变 |

控制面会**收紧**显式启用项目的approved内容、当批绑定及降级检测；旧项目先诊断。保留原protected路径和外部批准变量，新增policy的历史比较不能只看提交后的值。用户批准完整实施方案后才能据其具体范围使用外部批准信号；不能因本轮写方案或测试绿自行设置。

恢复：实现过程可回退未发布源码到之前版本；已迁移严格项目不能通过删除policy假装恢复，须保留历史及声明未验证状态，按既有控制面规则审阅降级。升级前保存清单及证据字节；失败原子保留。目标联通项目的状态整改是单独后续动作：保留用户选择/旧批准，标记新增批次的授权覆盖待复核，完成方案展示后才继续依赖部分；本轮不改其活动工作树或正在运行的会话。

## 11. P23-07：具体验收与执行顺序

执行依赖：先得到本完整候选方案的有效批准，再T23-03..08；T23-01/02调查与方案已由本轮指令授权。每项在原Task中更新，不另设诊断/Spec/模板专项审批。

| Task | 依赖 | 交付与验收映射 |
| --- | --- | --- |
| T23-01 | 无 | 核对真实issue、会话、源码与隔离反例；B23事实及证据，本轮已完成 |
| T23-02 | T23-01 | 候选Spec、详细Plan、影响/版本/测试方案、权威链，本轮交付 |
| T23-03 | 已批准T23-02 | 原指引的范围/冲突/汇报澄清；REQ01/02/06 |
| T23-04 | T23-03 | 结构化证据、唯一块读取、范围/快照绑定、统一模式接入；REQ03/04 |
| T23-05 | T23-04 | 初始化/迁移、legacy诊断、策略历史保护与调用版本预检；REQ05 |
| T23-06 | T23-04 | 声明顺序辅助诊断，明确partial边界；REQ07 |
| T23-07 | T23-03..06 | 行为/CLI/Git跨平台回归和原规定检查；REQ08 |
| T23-08 | T23-07 | 当前B/M/C/F及REQ/AT链、1.8.0元数据/Unreleased、交付状态；提交发布仅按当时有效授权 |

### 必须覆盖的回归场景

| 场景组 | 输入/操作 | 预期 |
| --- | --- | --- |
| 证据结构 | 空文件、占位、缺原话/时间/范围、无时区/未来时间、重复块/ID/键、越界或链接路径 | strict fail；可定位缺哪一项，不能只搜三个词就pass |
| 正常批准 | 一个已展示完整Plan后的用户明确实施回复被proposal和authorization共用 | pass；只记录一次用户动作，task/batch/subject各自匹配 |
| 新范围与旧授权 | 同task换batch但无适用关系、Plan更新但旧两个revision仍相同、新REQ缺覆盖 | fail或待审，不由两个旧值相等放行；有效reuse_of在原范围内可复用 |
| 快照和复用 | 修改已审快照；仅加进度；合法技术等价Plan；持续Baseline更正 | 前者fail；后三者在有效依据/原边界内可复用，推翻依据只重开受影响批准 |
| 原例外 | 已知小修、空项目、旧有效基线、独立调查、pending方案文档 | 保留原not_applicable证据和复用语义，无新增无意义审核 |
| legacy/升级 | 原旧manifest、显式升级、失败保存、删除policy/stage、旧版本checker调用 | 旧兼容状态明确；升级不伪造批准；降级受保护；实际入口版本不满足时拒绝宣称新能力 |
| 模式与树 | change/handoff/commit/committed；索引与工作区证据不同；证据被命令篡改 | 同一规则；提交只认实际验证树中的证据；保持原漂移拒绝与verified_tree合同 |
| 顺序 | 已知逆序、可靠有序事件、缺证据或跨轴、普通mtime变化 | fail/pass/partial按证据；mtime变化本身不推翻批准 |
| 汇报 | errors=[]、required=false；产品手测pass而门禁fail；诊断重跑pass | 同屏保留状态，整体不能说全通过，不覆盖原required结果 |
| 行为重演 | 本次企业角色选择；明确要求实施已给出的方案；已明确改原则 | 第一种先保留范围/交方案；后两种复用决定，无机械重复确认 |

原强制命令保持：TEST=`python -m unittest discover -s scripts/tests -q`（120秒）；COMPILE和GUIDANCE-COMPILE仍用manifest原命令（各30秒）。按项目既有说明先准备锁定source-context解析依赖；不能把全量检查换成更弱脚本。先焦点行为回归，再原检查；通过后不无故重复全量。正式提交前commit、提交后committed绑定实际树和源版本，托管CI与本地结果分开。

行为重演可以由同一agent在隔离工件完成；若未来有明确授权的独立评估，再使用子agent，不把委派本身作为完成条件或本轮擅自扩范围。

## 12. 已解决与仍需审阅

本方案已明确根因、数据结构、调用位置、兼容策略、顺序边界、版本与测试。用户已以“那就开始实施吧”批准这个两层补强范围及影响说明；当前源实现和原检查结果见Task。批准不自动代表测试、托管发布或全局安装完成。无需用户逐行核验Python或替agent担保技术正确性。

宿主可信签名/自动聊天取证、编辑前强制拦截、全项目批量批准清理保留为延后；恢复条件是宿主能力及单独明确授权到位。不以这些外部能力缺失为理由阻止已可完成的本地方案与后续结构化检查。
