# 项目自动检查

## 结构化批准证据合同

1.8.0增加可选 `workflow.approval_policy`：`{"record_contract":1,"enforcement":"diagnostic","sequence_enforcement":"diagnostic","minimum_checker_version":"1.8.0"}`。未声明policy的旧清单仍按原规则检查，另给非必需 `approval-evidence:partial / legacy_unverified`。新初始化和显式legacy迁移默认diagnostic，缺字段给非必需partial；明确选择strict后，证据缺口是required fail并阻止声明命令执行。pending允许自主调查；已声称approved的记录不能因处在调查阶段逃避结构核对。既有stage、task approval、依赖、文档影响、测试/超时及树复核继续执行。

证据继续位于原项目文件，不强制另建审批台账。可选：Markdown中唯一的命名JSON块，或JSON文件的单个record对象 / `{"records":[...]}`。拒绝重复ID/键、损坏fence、越界或链接路径；缺失不当作通过。Markdown形状：

````text
<!-- engineering-approval:APP-01 -->
```json
{"id":"APP-01","status":"pending"}
```
````

声明通过 `evidence` + `evidence_record_id`引用record。approved必须包含非占位的user_statement、scope、带时区且非未来的approved_at与recorded_at，以及 `source:{kind:"conversation"|"manual",reference:"可追溯原消息/记录"}`。recorded_at是记录时间，不能冒充原事件时间。可复用同一用户指令，但不制造未发生的批准。

三类原批准分别绑定：baseline_review.subject.revision等于当时source_revision，不强制等于后续事实基线；proposal_approval.subject.revision等于批准的Plan；implementation_authorization.plan_revision等于proposal且record.subject对应它。启用原task.approval_required时，task.approval也检查同一结构。除基线审阅外，record和声明需与选中task_id、batch_id匹配，record.requirement_ids/acceptance_ids精确覆盖选中Task范围；Task artifact_revisions记录当前plan/spec，并由artifact_links或workflow.active_plan/spec定位文档。只批准子集时选择范围明确的子任务，不能让大Task的部分批准替其余需求背书。

subject与spec_basis使用 `{document:"PLAN文档ID",revision:"PLAN-r1",section_id:"REVIEW-01",sha256:"64位摘要"}`；proposal/implementation/task批准都须有spec_basis。哈希内容优先取唯一成对 `<!-- engineering-review:REVIEW-01 -->` / `<!-- /engineering-review:REVIEW-01 -->` 之间文本，规范化CRLF/CR到LF，去两端空白并加一个末尾LF，再用UTF-8 SHA256；也可用唯一标题slug（section_id为合法ID），到下一同级/更高标题。不存在或歧义拒绝。进度追加到块外，不对整份活跃Task做hash。可用导入checker后的approval_subject_hash(text,id)计算同一规则；摘要是内容绑定，不能证明用户看过它。

纯技术等价调整可用Task.review_basis_revision `{plan:"原批准Plan",spec:"原批准Spec",reason:"为何仍在批准边界"}`保留依据；新权限/验收不得借此跳过重审。跨批次复用创建新record，附 `reuse_of:{evidence,evidence_record_id,reason}`，task/batch/范围按当前填写；来源必须仍approved且未invalidated，当前REQ/AT不能超出原集合，subject/spec_basis不能替换，原user_statement/approved_at/source保留。循环和超过16层的复用拒绝；关系的业务等价性仍由agent核验。

not_applicable继续沿原例外：空项目基线及small_fix方案要有reason/evidence，合同记录仍有scope/subject；不伪造用户原话/批准时间。small_fix方案仍绑定Task/REQ/AT和Plan/Spec依据，implementation_authorization不允许not_applicable。

`approval-sequence`只比对同时间轴的声明事件：Task.approval_sequence的presented/approved/implementation分别给timeline_id、reference、非负整数position。顺序应严格递增；不同轴/缺来源partial，不拿Git时间或mtime猜pass。默认诊断非必需；sequence_enforcement=strict仅在implementation/verification/complete时将其列为required。它不带宿主签名，手工摘录不认证真实批准。

已启用policy的删除、strict降级、收缩实现范围/删除stage以及strict顺序降级会被approval-policy-history发现；change对比base，其余使用HEAD或提交父版本。缺历史/损坏数据不当作无policy。降级沿既有一次性外部控制面批准，不在仓库保存永久信号。commit/committed仍拒绝与暂存/提交树不一致的工作区证据；声明命令执行后的原漂移检查仍有效。

旧checker不认识新字段，严格项目的实际hook/CI应启用 `--require-approval-contract 1`（旧checker会因未知参数失败）并核对运行的tool_version，不可只相信manifest声称的minimum_checker_version；部署入口示例见现有hook模板。policy和命令调用都不能阻止漏声明实现路径或编辑器写文件。

程序只证明声明结构、文件/快照和绑定一致。不能认证作者、真实批准、用户理解、技术等价或全部业务覆盖；report的required_checks_satisfied与独立手测必须分开汇报。

检查器仅依赖 Python 标准库。默认只读，`--report` 仅创建新报告文件，拒绝覆盖；`--run-checks` 才执行项目明确声明的命令。命令是非空参数数组，使用 `shell=False`，不解释管道或命令拼接，运行前需核对项目命令与授权。

```text
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode discovery --run-checks
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode baseline
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode change --base <commit> --task TASK-01
python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode handoff --base <commit> --task TASK-01 --run-checks --report new-handoff-report.json
ENGINEERING_TASK_ID=TASK-01 python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode commit
ENGINEERING_TASK_ID=TASK-01 python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode committed --commit-ref <commit-sha> --run-checks
ENGINEERING_CONTROL_PLANE_APPROVED=1 python <skill-dir>/scripts/check_project.py --root <project> --manifest engineering-manifest.json --mode committed --commit-ref <commit-sha> --task TASK-01 --allow-control-plane-change --run-checks
python <skill-dir>/scripts/extract_sqlite.py <checkpointed-project.sqlite> --output new-database-inventory.json
python <skill-dir>/scripts/extract_sqlite.py <checkpointed-project.sqlite> --output planning/database-inventory.json --update
python <skill-dir>/scripts/extract_database.py mysql --url-env ENGINEERING_DATABASE_URL --schema app --output new-database-inventory.json
python <skill-dir>/scripts/extract_database.py postgresql --url-env ENGINEERING_DATABASE_URL --schema public --output new-database-inventory.json
python <skill-dir>/scripts/extract_database.py redis --url-env ENGINEERING_DATABASE_URL --output new-database-inventory.json
```

discovery 检查首次接管中的不完整事实基线，明确返回 `completion_ready=false`；它不是基线批准。baseline 核对声明结构和资料；change/handoff 必须提供 Git base 和任务，包含删除、重命名前后路径及未跟踪文件。base 先解析为 commit OID，不能传 Git 选项。handoff 还核对批准、前置任务、完成状态与本次实际验证。基线不要求 Git；首版无 Git 项目无法完成自动变更范围核对，保持未验证，不以基线检查替代完整交付。

`commit` 是本地提交门禁：验证输入读取前绑定HEAD和index tree；声明检查结束后新增必需的verification-state，拒绝HEAD/index/工作树和未忽略新文件的持久漂移，失败不自动还原用户修改。只读取当前 Git index 中已暂存的路径，拒绝空暂存区和任何未暂存的工作树差异，防止从工作区读取到与提交内容不一致的文档或清单。它会将源代码路径与 `task.documentation_impact` 中的触发路径关联，源代码变更未声明门槛也会失败；遗漏任一文档时退出失败。初始提交使用空树比较，删除和重命名同时检查旧路径与新路径。任务 ID 可用 `--task` 指定，也可通过 `ENGINEERING_TASK_ID` 提供；命令行参数优先。

`committed` 用于 CI/受保护分支复核已生成的提交：checkout 必须位于 `--commit-ref`，按该 commit 与父提交（根提交则用空树）比较，并拒绝工作树/index 偏离提交树。CI 应对待合并的每个提交运行该模式；本地 hook 可被跳过，不能作为唯一门禁。复制 [POSIX 模板](../assets/templates/pre-commit.engineering) 或 [PowerShell 模板](../assets/templates/pre-commit.engineering.ps1) 作为本地 hook；CI checkout 每个待检 commit 后可调用 [POSIX CI 模板](../assets/templates/ci-committed.engineering) 或 [PowerShell CI 模板](../assets/templates/ci-committed.engineering.ps1)。两个 CI 模板都要求显式指定 commit SHA 和该提交的任务 ID。

### 保护检查规则和清单

`commit` 和 `committed` 还会保护控制文件，默认包括传入的 manifest 和 `scripts/check_project.py`；manifest 可通过 `control_plane.protected_paths` 增加项目自己的规则文件、hook 和 CI 配置。版本文件和变更记录也属于本仓库的受保护范围。门禁会读取提交父版本的 manifest 来确定原有保护范围和批准变量名，因此本次提交不能靠删除保护配置或换一个批准变量来绕过检查。控制文件变更默认失败；人工检查变更后，需要在本地显式传入 `--allow-control-plane-change`，并在当前进程环境中设置父版本 manifest 声明的批准变量为 `1`。批准变量不能写在仓库文件或提交脚本里。

首次采用时，基线中没有 manifest 是预期的 bootstrap 情况，不是普通测试失败。检查器会在 `control-plane` 证据中标记 `first_adoption: true` 并给出一次性人工审阅提示。审阅 manifest、项目规则、文档清单和检查命令后，才在单次本地命令中提供 `--allow-control-plane-change` 及外部批准变量；这不会批准后续规则变更，也不会把批准写入仓库。

CI 不得在仓库可修改的 workflow 中把批准变量写成常量 `1`，也不得把可用于不受信任 PR 的 secret 传给该检查。若 CI 要接受控制文件更新，批准值必须由仓库外的受保护配置提供，并要求独立人工批准；GitHub 项目应另外用仓库设置保护检查器、manifest、workflow 等文件的审阅流程。任何同仓库代码都不能单独证明自己可信：若有人能同时改检查器和 CI，最终保护仍依赖仓库托管平台的分支规则、受保护的 reviewer/owner 审批和独立审阅。控制文件变更应单独解释、审阅并运行完整测试，不能把自我批准当成安全证明。

如果控制面检查失败，`commit`/`committed` 会跳过当前提交 manifest 声明的命令，避免执行未经审阅的命令；报告仍会明确显示检查未通过。`committed` 还要求完整 Git 历史，浅克隆无法证明父提交时必须先补齐历史。

本仓库的工作流先运行普通检查；控制面变更由 `pull_request_review` 在 reviewer 批准当前同仓库 PR head 后自动触发固定的 `engineering-control-review` environment，再运行受保护的 committed 检查。普通 push/PR、fork PR 和 review 事件本身都不得接收 `ENGINEERING_CONTROL_PLANE_APPROVED`；fork PR 不会进入执行受保护值的 reviewed job。该变量只能来自 environment-scoped 配置，不能写入 repository/organization 常量或 workflow。工作流必须确认 review 的 `commit_id` 等于当前 PR head，防止复用旧批准。`workflow_dispatch` 仍保留为历史提交或异常情况的 exact-SHA fallback；输入完整 commit SHA 和任务 ID。仓库所有者必须为 `engineering-control-review` 配置 required reviewers，并用 CODEOWNERS/分支保护保护 workflow、checker、manifest 和 CODEOWNERS。本环境审批记录 reviewer/时间，PR review 记录批准 commit，Actions artifact/日志记录实际检查，三者共同构成审计链。环境审批不替代对仓库控制文件的独立审阅，也不使不受信任 PR 代码获得批准值。

这仍然是普通误改和绕过的防护，不是对同仓库恶意检查器的沙箱。最终检查器/workflow 的可信版本、受保护的审批设置由维护者控制。没有 GitHub 的项目可在本地审阅同一份差异，再在单次命令环境中传递批准；不需要上传源码。

GitHub Actions 是可选的托管检查方式，不是每个使用本 skill 的项目都必须拥有 GitHub 仓库或启用 Actions。项目可以只使用本地 hook，也可以接入 GitLab CI、Jenkins 等其他 CI；只要在合并或发布前运行等价的 `committed` 检查即可。只有选择 GitHub Actions 的项目才需要复制或启用对应 workflow；没有远程 CI 时，仍应在本地运行 `commit` 门禁并保留验证记录。本 skill 不要求上传项目源码，也不会因为没有 GitHub Actions 就把项目判为失败。

The JSON result contains `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, `errors`, and nullable `verified_tree` / `verification_head`. Successful commit/committed results bind those fields to the index tree and pre-verification HEAD; other/failed results leave them null. `verification-state` records before/after IDs and drift paths after declared checks and before report-file creation. This evidence is not a signed attestation or an atomic final commit. Exit code 0 means every required check passed; 1 means a declared check or validation requirement failed, including an output-limit failure; 2 means malformed configuration, unavailable environment, or an unsupported capability before a check can run. `pass`, `fail`, `partial`, `unsupported`, `skipped`, and `error` are reported separately. Partial, skipped, or unsupported required checks cannot satisfy completion.

## 本地工程记录归档与恢复

`python <skill-dir>/scripts/task_archive.py --root <project> --manifest engineering-manifest.json --project-id <stable-local-id> --store <absolute-path-outside-project> init` 将工程 manifest 与其 `documents` 声明的文档按原始字节存入指定的本地 SQLite archive，创建初始 revision。工具拒绝把 archive 放在 project root 内；不会创建或清除 Git 状态，不会自动迁移其他项目。首次 init 前应检查工件清单与路径，并选择有本地访问控制/备份责任的外部目录。archive 不加密，不云同步，也不管理保留/清理策略。

- `... check` 对比工作区与最新 revision，显示 missing/new/changed 文件。直接覆盖可被发现，但此动作不是持续监视，也不会拦截写入。
- 审核当前内容后，以 `... check --save --expected-head <revision> --reason <reason>` 创建不可变 revision。期望 head 不匹配时拒绝，避免基于旧版本保存；checkpoint 本身不代表用户审批。
- `... history` 列 revision、父版本、时间、操作者标签、原因与 restore 来源。
- `... restore <revision> --reason <reason>` 只有工作区与当前 archive head 完全一致时才运行。它先保存新的 restore revision，再逐文件原子重建视图；失败可能报告 partial。`... restore --project-head` 可在工作区偏离时按当前 head 修复视图，也会记录新 restore revision。

SQLite 事务保护 archive 内 revision/head 一致性；不保证外置磁盘不会损坏。工作区文件在 archive 记录后逐个重建，恢复中断可能留下 partial projection，重试 `restore --project-head` 可重建。archive 损坏/丢失时 fail closed，不会把未验证工作区自动写入历史。内容摘要用于检测字节变化，不认证操作者、语义或真实批准。

project ID 必须在 archive 生命周期内稳定唯一；更换项目身份要创建新 archive。archive 保护显式列入 manifest 的 documents，不自动保存未声明文件、Git 状态、附件、数据库或宿主会话。首次 adoption 与计划检查点均由项目显式运行，不增加用户审核节点，也不影响 BASELINE → SPEC → PLAN → TASK → EVIDENCE 流程。当前宿主允许任意 shell/editor 写入，强制拒绝绕过入口为 unsupported。

PowerShell 示例（将路径/ID 换成项目实际值）：

```powershell
python C:/path/to/engineering-workflow/scripts/task_archive.py --root C:/path/to/project --manifest engineering-manifest.json --project-id customer-app --store C:/Users/you/AppData/Local/EngineeringState/customer-app.sqlite init
python C:/path/to/engineering-workflow/scripts/task_archive.py --root C:/path/to/project --manifest engineering-manifest.json --project-id customer-app --store C:/Users/you/AppData/Local/EngineeringState/customer-app.sqlite check
```

这些命令只读写显式指定的工程文档及本地 archive；不更改 OS 权限、不访问网络、不需要 API key。

## 项目清单字段

从 [清单示例](../assets/templates/project-manifest.example.json) 调整实际路径；示例状态为 planned，直接复制不会被视为已完成。

接入时先核对来源与适配能力。示例和full初始化均将数据库/接口源清单默认为可选，数据库字典、接口文档和agent语义核验仍按基线范围要求完成；只有真实来源有受支持、可达的验证路径并经项目审阅时才设置required。manual永远partial，当前没有通用接口/路由源码适配器；将它直接设为required会产生无法通过的门槛。既有项目的required不能自行删除或降级：先完成独立调查，准备具体适配器或验收范围调整方案，再按该项目控制面规则审阅。用户接受基线范围不会使partial变成pass，重复无关全量测试也不能解决适配能力冲突。

| 字段 | 含义及关联 |
| --- | --- |
| schema_version | 整数 1；不是字符串或布尔值 |
| documents | id、path、kind、required；声明文档，required 为布尔值；被需求/模块/任务引用的文档即使标可选也必须存在 |
| requirements / acceptance | id、document；document 指规范正文文档 ID。默认编号必须出现在正文；也可用 `index` 指向独立追踪索引，或用 `anchor` 指向正文标题/HTML/Markdown 锚点。`index` 与 `anchor` 同时声明时都必须满足 |
| modules | id、source_paths、document、depends_on、allowed_dependencies；文档为 ID，实际依赖必须属于允许依赖且无循环；此图仅为声明图 |
| inventories | id、kind、path、documentation、required；path 指源清单 JSON，documentation 指文档映射 JSON，不是文档 ID |
| checks | id、command、required、timeout_seconds、working_directory；command 是参数数组且不能含 NUL，超时为有限正数，合并输出固定限制为 8 MiB；working_directory 默认为项目根，必须是项目内已存在且不经过符号链接/目录连接的目录；无隐式 shell |
| workflow | 可选对象；`active_task` 指向当前 CI/提交任务，新的清单还可声明 `active_baseline`、`active_spec`、`active_plan` 指向 documents。没有显式 `--task` 或 `ENGINEERING_TASK_ID` 时，commit/committed/handoff 使用 active_task；切换任务只需更新这些字段及任务记录，不要在 workflow 文件复制历史任务 ID |
| tasks | id、requirement_ids、acceptance_ids、module_ids、depends_on、status、impact_document、required_checks、approval_required、approval、documentation_impact；可选 `artifact_links` 将任务连接到 Baseline/Spec/Plan/Task/Traceability 文档。commit 门禁通过 `--task`、`ENGINEERING_TASK_ID` 或 `workflow.active_task` 选择任务 |
| task.status | planned、in_progress、blocked、complete；handoff 要求 complete，但状态不证明人已审查 |
| task.impact_document | 已声明的文档 ID；对应修改前影响记录 |
| task.required_checks | 已声明检查 ID；选定任务的必需检查强制生效，不能由检查自身 required=false 绕过 |
| task.approval | 需要批准时为 `{status: approved, evidence: 项目内文件路径}`；证据引用用户原话/时间/范围，不能伪造或仅自行写 approved |
| baseline | 既有项目 status 为 complete/approved；新项目临时状态见下节。evidence 指已存在的基线记录；可选 `document_ids` 列出当前 Baseline 视图，`source_revision` 和 `scope` 绑定源码/工作树与审阅范围；状态与证据存在不能自动证明业务完整性 |
| exclude_paths | 明确排除并在报告列出；可用项目相对的段级 glob（`*`、`?`、字符类和完整段 `**`），不能排除项目根，不得用宽泛排除隐藏业务改动 |
| control_plane | 可选对象；`protected_paths` 声明额外受保护的控制文件，`approval_env` 为批准环境变量名（默认 `ENGINEERING_CONTROL_PLANE_APPROVED`）。manifest 和 checker 始终受保护；需人工审阅并通过外部批准才能提交变更 |

路径限定在项目根内，不允许符号链接/目录连接旁路。manifest 路径的 `/` 与 `\\` 都按路径分隔符处理；POSIX 上的 Windows 盘符/UNC 路径、越界路径和链接旁路仍拒绝。source_paths、排除路径、检查工作目录和文档路径可为项目内绝对路径，匹配 Git 时规范化为项目相对路径。`exclude_paths` 的 `*`、`?` 和字符类只匹配一个路径段，`**` 匹配零个或多个完整段；命中的目录及其后代会在解析链接前剪枝，因此 `**/node_modules` 可安全跳过 pnpm 链接。根匹配、绝对 glob 和包含 `.`/`..` 段的 glob 被拒绝；排除项不会成为变更白名单，排除范围外的链接仍会失败。Markdown 的普通项目内相对链接可跨目录；模板中的外部链接不代表代码依赖。未登记的源路径必须补模块归属，不能为了通过而添加全项目排除。

`task.documentation_impact` 可声明变更触发器与必须同步的文档：`{ "kind": { "when_paths": ["backend/migrations"], "document_ids": ["DB", "FLOW"] } }`。`when_paths` 保持字面路径；它可以是项目内模块 `source_paths`、规则所引用文档的路径，或一个严格非根的公共父目录，前提是该父目录包含所选任务中至少两个不同模块的 source scope。例如 `packages/api` 与 `packages/web` 可用 `packages` 聚合触发。公共父目录只触发文档门槛，不扩大变更覆盖范围；无关目录、单模块父目录、glob 和项目根仍非法。触发后 `document_ids` 中的每一份文档都必须出现在本次 diff 中，这是 AND 语义；需要“至少一份”时应拆分任务或明确记录例外，不使用未定义的 OR 语义。manifest、planning、影响分析和规则文件属于治理（governance）模块，若它们自身变化，应在任务中声明治理文档和影响记录，不能靠全局排除隐藏。commit/committed 还要求每个受影响的模块源路径命中至少一条规则，漏声明不能通过。只有实现细节变化时，可声明 `implementation-only` 规则，将对应源路径映射到影响分析文档，并在该文档中写明不更新模块/数据库文档的依据；该记录需与代码同一提交。常见类别包括模块/调用链（module map、business flow、contract）和数据库（database dictionary、business flow）。这是声明式门槛，仍不能自动发现未登记的动态依赖或判断语义是否真实。

需求和验收 ID 默认必须出现在 `document` 指向的正文中。原有文档不适合插入机器 ID 时，可在条目增加 `index`，指向 `documents` 中的独立追踪索引；checker 只要求该索引包含 ID，并保留 `document` 作为规范正文归属。需要定位正文章节时可再声明 `anchor`（HTML/Markdown anchor 或标题）；`anchor` 与 `index` 都是 AND 条件。示例使用 `planning/traceability.md` 作为独立索引。

## 新项目的临时基线

`init_manifest.py --root <project> --project-kind greenfield --profile full` 显式选择从零起步，默认实现位置为 `src` 和 `tests`，可重复 `--implementation-path backend --implementation-path frontend` 替换。初始化仍生成 `planned`，不创建文档、批准或完成证据；先补齐权威文档、实际检查和调查证据。默认 `existing` 继续要求已有系统调查。已有平铺源码按实际顶层入口生成候选作用域；空目录须显式选择 greenfield。

在确无既有实现时，agent 核验全仓库后可记录：

```json
{
  "status": "not_applicable",
  "origin": "greenfield",
  "reason": "No prior implementation; recorded repository inspection",
  "evidence": "planning/baseline-review.md",
  "source_revision": "<actual source or empty-worktree identifier>",
  "scope": "<inspected scope and external constraints>",
  "implementation_paths": ["src", "tests"],
  "document_ids": ["BASELINE", "MAP", "DB", "CONTRACT", "FLOW"]
}
```

检查器要求临时状态的 origin、reason、source_revision、scope、evidence 和非空 implementation_paths。后者必须是项目内非根字面路径；not_applicable 时范围内任何文件都会触发失败，不受 exclude_paths 影响。实现出现后转 partial 并补真实基线；不存在的 source_paths 仅在这两种状态且与 implementation_paths 对应时允许。完成基线后恢复正常路径存在性检查。

新增 `baseline-lifecycle` 结果明确 `completion_ready`。临时状态可通过 baseline/change/commit/committed 的生命周期校验，但其他批准、影响、保护和必需测试门槛仍执行。handoff 或选中任务 complete 时，临时状态失败；交付需 complete/approved。检查器仅核对已声明范围，不能发现全部漏登记实现或证明 origin 真实性；agent 必须按[联动模型](baseline-linked-artifacts.md)核验。

full/lite 都要求已链接的基线视图和追踪文档存在；不适用视图写原因，不能靠 required=false 隐藏被引用文件。lite 省略源清单并使用影响记录；full 对实现范围保守触发基线/地图/契约/数据库/业务流更新，审阅实际项目后再收敛路径规则。两者都不生成项目验证政策，不把默认测试命令当作实际完整测试。

## 源清单与文档映射

源清单参见 [示例](../assets/templates/inventory.example.json)。包含 `kind`、`provenance` 和 `items`：

- kind：清单种类，例如 database、contract。
- provenance.type/scope/complete/evidence：提取方法、明确范围、布尔完整性与证据；manual 永远只能报告已声明范围 partial，不能自行声明完整。
- provenance.source_files：`{path, sha256}` 列表，核对来源新鲜度；来源路径须在项目根内。
- items：`{id, fields:[字段名]}` 列表。数据库 id 表示表/视图，接口可用稳定的 method+path 标识；禁止重复条目和字段。

[文档映射示例](../assets/templates/inventory-doc-mapping.example.json) 包含同一种 kind 和 `items:[{id,document,fields}]`。document 是实际 Markdown 路径。源与映射的对象、字段双向核对；映射引用存在不证明字段含义正确，逐字段语义在数据字典人工审查。

内置适配器包括 `sqlite-metadata`、`mysql-metadata`、`postgresql-metadata` 和 `redis-metadata`。SQLite 从受控文件快照只读提取；MySQL/PostgreSQL 只读 `information_schema`；Redis 只读 `INFO keyspace`，不执行 `SCAN`，不读取 key 或 value。远程适配器需要显式调用、可选驱动和环境变量连接 URL，输出带 `source_ref`、`captured_at`、`query_sha256`、`snapshot_sha256` 的 JSON 快照；普通 baseline 不会自动连接数据库。检查器离线核对远程快照的摘要与结构，缺少驱动/凭据或连接失败报告 unsupported，不把未知适配器视为通过。输出默认拒绝覆盖；显式 `--update` 只接受同一工具版本生成的 `kind=database` JSON，并通过同目录临时文件和原子替换更新。

## 结果的能力限制


检查器核对文件/本地引用、编号、已声明模块图、任务依赖和变更路径、对象字段清单及执行结果。它只证明 manifest 中声明的命令在声明的目录执行并返回成功，不能证明命令选择覆盖了项目真正的验证政策，也不能证明所有动态调用已被发现、文档语义正确、认真阅读过资料、达到真实概率 95%、架构合理或整个产品完成。项目应把权威验证命令写入 `AGENTS.md`、项目 README 或 CI 规则；若任务选择替代检查，必须在影响/决定记录中说明差异、理由和未覆盖风险。不要用机械扫描把自声明命令伪装成完整验证。只有声明图的循环得到检查，不是所有语言 import 图。

执行证据包含退出码、耗时、命令与输出摘要；为避免凭据泄露不展示原始参数/输出。常见测试 skip 汇总标记会成为 partial，但没有匹配标记不证明任何框架都没有跳过；人工仍需核对实际测试行为。历史报告不是本次执行证据。必需检查未执行、部分支持或失败都不得标为完成。

## Hosted diagnostic and finalizer contract

For protected reviewed and manually reviewed runs, the original committed checker invocation is authoritative. A verbose diagnostic rerun may run only after the report proves the control-plane and committed-scope checks passed and TEST alone failed. The rerun supplies debugging evidence; even when it passes, the finalizer and aggregate quality job must remain failed because the original required check failed. Only a successful original checker invocation satisfies that required check.

SQLite 提取使用只读 immutable 快照和 table_xinfo，覆盖 main schema 的用户表、视图及隐藏/生成字段，附字段类型等详情；不读业务行、不写数据库。活跃 WAL、外部附加库和快照范围外状态不支持；使用项目自身受控的 checkpointed 测试快照，不能自动清空或修改真实库来满足检查。提取器默认只能创建新文件；目标已存在时必须显式使用 `--update`。更新模式仅接受包含匹配 `tool_version`、`kind=database` 且能解析为 JSON 的本工具快照，写入同目录临时文件并原子替换；普通 JSON、手工清单或数据库/sidecar 路径都会拒绝，失败不改变原文件。complete 仅指这个元数据范围，不含字段业务含义、触发器、索引约束、迁移与全系统读写关系。
远程适配器同样只证明声明的元数据快照，没有证明实时数据库状态；快照不得包含连接密码、业务行、Redis key 或 value。


## 1.6.4 输入、状态和进程生命周期合同

- 文件和Git历史JSON共用可预期解析异常处理，深度/整数保护及manifest非对象根产生结构化配置错误。历史文件真实缺失与存在但不可读/损坏分别处理，后者不能静默替代旧保护政策。没有新增任意大小上限或提高解释器保护设置。
- commit与committed均执行前后状态复核；合法的Git忽略产物可生成，源码/未忽略文件漂移仍失败。verified_tree用于结果与实际提交树比对；后续hook、并发修改、临时篡改后恢复和同权限恶意代码仍需要可信CI/OS隔离。
- CLI声明命令执行期间捕获SIGINT/SIGTERM（Windows另含SIGBREAK），finally终止拥有的普通进程家族，限时等待输出线程并恢复原handler；取消报告不成功，退出码为128+信号号，KeyboardInterrupt为130。
- POSIX沿用独立会话/进程组清理。Windows先创建kill-on-close Job Object，子进程挂起创建、赋予job后才恢复；约束建立失败时清理且拒绝执行命令。正常退出、超时、取消均清理普通后代。Job已建立后父进程被强制结束也由OS关闭句柄触发清理。
- 此合同不是全平台SIGKILL保证：POSIX SIGKILL无法捕获，Windows赋予job前的启动窗口及恶意同权限攻击也不作绝对保证；更强生命周期需要外部监督/OS约束。导入函数调用者自行管理信号策略，CLI只在主线程临时注册handler。

历史缺陷和原始复现保留在[ASSESS-19-21-01](../planning/issues-19-21-assessment.md)；当前实现、测试与发布证据见[TASK-ISSUES-19-21](../planning/issues-19-21-task.md)。原工作流、TEST/编译命令、120秒和审批职责保持。

## 接入和原流程声明（1.7.0）

可选stage及基线/方案/实施授权字段核验原流程，不能创造额外审核轮次。空项目的baseline_review可带证据not_applicable；小修任务可用带既定需求/影响证据的proposal_approval=not_applicable；有效旧审阅保留原revision可复用，失效时显式pending/invalidated；完整方案与实施可共用明确覆盖二者的原话。complete/handoff继续允许complete/approved事实基线，不增加handoff阶段。

原必需任务批准、依赖、影响文档、控制面和实际检查门槛保持。discovery支持不完整基线调查但不代表完成；change/handoff/commit/committed拒绝未授权实现路径，两个提交模式失败不执行声明命令。字段与场景见[adoption-lifecycle.md](adoption-lifecycle.md)。
