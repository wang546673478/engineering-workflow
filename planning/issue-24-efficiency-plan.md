# PLAN-ISSUE24-EFFICIENCY-01：可重建目录与批量状态工具（r1 用户批准的超时修订）

状态：approved and in verification；基准 revision `PLAN-ISSUE24-EFFICIENCY-01 r1`，现依用户 2026-10-22 明确决定附加一项执行政策修订：本仓库 TEST timeout 120s→240s。功能方案与基线 `BASELINE-ISSUE23-02`、`SPEC-ISSUE24-EFFICIENCY-01 r1` 保持。用户完整原话、门槛边界及最新证据见 [Task](issue-24-efficiency-task.md)。

## 根因与责任层

现场会话快照显示重复读取/搜索、多文件同步、写入锚点失败后重试，以及宿主 cwd 启动失败并存。日志不含逐调用耗时，issue的耗时比例仍为作者估算。Skill工具只能处理自身的读写操作，不能修复宿主未能创建cwd进程的问题。

- 工程状态工具负责索引、批量读取、精确更新、幂等和冲突报告。
- 现有task_archive负责可选备份/历史/恢复；它不是批量同步接口。
- Host负责稳定workspace/file API和cwd恢复策略；缺公开接口时报告unsupported/blocker，不得由helper同一错误cwd无限重试。
- Agent/用户继续负责正文语义和现有审核节点；机械revision不代表批准。

## 候选模块

批准方案采用可选 `scripts/workflow_state.py` CLI，直接读取现有 manifest、active pointers、Task/Spec/Plan/decision 文件作为唯一权威源，不建立第二业务状态库：

1. index：从manifest documents、active Task、artifact_links/revisions生成JSON/表格；字段含document ID、精确路径、kind/owner、状态、revision/basis、源hash、上下游links。默认输出而不写文件；若物化Markdown页，必须可从源工件重建。
2. 生命周期状态：目录同时显示current、draft、completed、superseded/obsolete、deferred、unverified/unknown。completed要有对应Task/acceptance完成证据；obsolete要有明确superseded标注、原因和替代条目；deferred显示模块、结论、问题、依赖/影响和恢复条件。只因文件旧/不在active pointer不能自动obsolete。需求、批准、实施、验证、发布状态分列。
3. read-snapshot：一次按active Task/document IDs/section IDs返回当前摘要和精确章节，附source hash/semantic revision；同round可复用未变hash，源变后立刻失效，不能缓存覆盖新变更。
4. apply-batch：单一JSON操作带operation ID、manifest和每目标expected hash、精确document/section/JSON key操作；先校验全批路径/唯一anchor/JSON/REQ/AT/revision关系并生成完整dry-run diff。任一冲突则整批不写；禁止模糊前缀/全文替换。
5. 应用：snapshot/journal可复用现有archive；所有目标都验证通过后在同一文件系统写临时文件并提交；operation ID保证重放幂等。跨多个原子rename不视为天然atomic；中途失败必须恢复旧集或报告partial并可重建。
6. cwd故障：检查稳定workspace handle；宿主报告invalid cwd则停止同路径重试，尝试host file API或重新解析一次；仍失败明确block，不修改任何文件。当前公开host工具能力未确认。

目录只是导航/状态读模型；过时/完成内容仍能从目录定位及打开。它不复制权威正文、不触发审核、不更改active pointer。历史内容不迁入新格式，除非未来独立审核迁移方案。

## 流程与兼容

Baseline→Spec→Plan→Task→Evidence、一次一问、持续需求记录、模块审核、Spec冻结、完整Plan批准、实施授权、required checks及其余 timeout 均保持。用户随后明确批准将本仓库 TEST timeout 从 120 秒改为 240 秒；TEST 命令/覆盖/断言/required 状态以及 COMPILE、GUIDANCE-COMPILE 的 30 秒 timeout 不变。Batch只合并已确认的mechanical updates，不把需求答案提升为批准。工具是opt-in；未采用项目按旧格式与门槛运行，不自动迁移、不strict化、不要求Git。

首批不把大型 Task 改造成“当前摘要+JSONL历史”，也不迁移旧历史；这会改变权威格式和链接兼容，需另立方案。配对实际工作流 pilot 延后；现有合成测试不证明实际效率提升。

## TDD和验收顺序

1. RED/GREEN：manifest驱动index同时保留completed/obsolete/draft/deferred条目；obsolete显示原因/替代链接，unknown不猜测。
2. RED/GREEN：index每次从权威manifest/Task实时重建并返回source hashes；不写源文件或维护陈旧的物化索引。
3. RED/GREEN：read-snapshot按精确章节返回当前正文和source hash；CLI不持久化或跨调用缓存，调用方只可在同一轮hash未变时复用已读结果；hash变化后batch的expected-hash校验拒绝旧内容。
4. RED/GREEN：一个batch精确同步Task/Spec摘要/manifest状态并给diff；锚点缺失、重复、JSON坏、hash过期任一出现都整批拒绝。
5. RED/GREEN：operation重放幂等；两个writer旧head同时写只准一个成功，另一个看到冲突及diff。
6. RED/GREEN：archive/临时写/部分rename注入失败；事务失败后旧head保留，重启能识别partial并恢复。
7. RED/GREEN：需求答复不变更approval/task gate；原1.8阶段、checks 和命令逐项保持。唯一获批的验证政策调整为当前仓库 TEST timeout 120→240 秒；COMPILE 和 GUIDANCE-COMPILE 保持 30 秒。
8. RED/GREEN：cwd无效停止无限重试；无host API时整批不写并标unsupported。
9. 配对pilot：同一匿名化需求片段比较原法和候选工具的命令数、成功读/写次数、重复读取、失败重试、实耗时间、最终diff和审批状态；多次结果之前不宣称普遍节省。

## 实施范围收敛

- 使用独立可选 CLI `scripts/workflow_state.py`，把 manifest index、read snapshot 与精确 apply-batch 放在同一状态工具边界；复用 checker 的安全路径与严格 JSON 基础函数；保留 `task_archive.py` 作为快照历史、冲突恢复与本地归档 owner。
- 索引默认为 stdout JSON，也提供 Markdown 展示；不落盘成第二权威文档。生命周期状态优先来自 active pointers、Task 状态与显式的 document lifecycle 元数据；证据不足显示 `unknown/unverified`。已完成和已明确标记过时/替代的工件仍逐条输出并保留来源、原因及链接。`planning/` 下未登记 Markdown 也纳入索引并显示 unknown。不会仅凭年龄或不在 active pointer 中而判为 obsolete。
- snapshot 根据精确 document ID 和唯一 Markdown 标题返回整份文件或指定章节及 SHA-256；调用方用返回摘要复用本轮结果，hash 变化后拒绝旧 batch，不建立跨调用缓存；保持原文件 UTF-8/BOM 仅读取不写缓存。
- apply-batch 需要显式 request、manifest/document expected hashes、稳定 operation ID、已初始化归档及 expected archive head；先做完整 dry-run diff，再整批校验和准备。复用归档的不可变revision及 head CAS，通过同目录临时文件替换；运行时失败回滚已替换文件和归档事务，崩溃残留由 `check` 检出并通过现有 `restore --project-head` 恢复。幂等标记存于归档 revision provenance，不改归档 schema。
- Apply 操作仅支持唯一精确 Markdown 标题区块替换及 manifest 内精确 JSON Pointer 的 lifecycle 写入；不支持模糊/全文替换。拒绝改 task/workflow approval、stage、gate、required check、timeout、task status 等门槛字段；lifecycle status 不能持久写 `conflict`（该状态由 active pointer 冲突派生）。增量 lifecycle 必须通过证据、replacement、deferred impact/depends_on 等引用校验。Markdown 保留 BOM 与现有换行格式。
- 当前宿主进程在命令启动前失败不在本地 CLI 可捕获范围内；本轮仅让工具在显式 root 不存在时立即返回 unsupported/error 证据，不重试错误 cwd。没有可验证的 host workspace/file API，因此不交付 host 集成，保留 unsupported 边界。
- 当前工具同步检查 manifest 中的 active pointers、task ID、REQ/AT、artifact links/revisions 和 lifecycle 引用；检测到冲突时失败或标 conflict，不自动选择“最新”。
- 普通 file replacement 失败会尝试恢复所有已处理目标，且将失败目标也纳入恢复；恢复本身失败时报告 workspace 可能 partial 和现有 archive restore 命令。提交 SQLite 前再比较完整文件集与待提交 snapshot，检测批次中的无关文件漂移。
- 1.8 工作流节点、审批含义、批准复用规则、检查命令与覆盖保持；只有当前仓库 TEST timeout 经用户明确批准由 120 秒调整为 240 秒，其余 timeout 不变。工具可选，不自动迁移项目或启用 strict，不改外部仓库/项目。用户随后明确授权本批在门槛通过后上传该 GitHub 仓库；GitHub Release 未授权。

### 批准的验证时限变更（2026-10-22）

用户在发现完整测试集在原 TEST 120 秒门槛边界波动后，明确要求：“把 TEST 超时改为 240 秒，其余检查和流程保持不变，并据此更新方案后继续”。据此，仅将当前仓库 manifest 的 TEST timeout 由 120s 调至 240s；COMPILE 与 GUIDANCE-COMPILE 仍为 30s，command argv、测试数量/断言、required 状态、workflow stages、审批/strict-default、CI/hook 均保持原状。此项是对 Spec r1 中 timeout 不变约束的用户批准执行政策修订，不改变其功能需求、工作流目标或测试覆盖。当前 Task、manifest、change-impact 和验证报告都记录该明确范围，不借机拆分或减少测试。

## 未决与下一步

宿主是否提供 workspace/file transaction API 和 cwd 恢复接口仍未验证；本次实现只覆盖本地 CLI，不声称修复宿主启动失败。实际耗时分布需可用配对样本后再测。本次不自动批量分类旧历史；来源不足的目录状态保持 `unknown/unverified`。当前实现状态与正式验证仍见 [Task](issue-24-efficiency-task.md)。

### Windows reviewed 路径别名修复（Task 后续实现）

Actions run `39787233509` 证实 Windows 在 TemporaryDirectory 的长路径与 8.3 短路径别名间切换时，公共 `safe_path` 把同一 project root 下文件误拒为越界；Ubuntu reviewed 同一提交通过。修复在 checker 公共路径边界仅对含 `~N` 短名片段的路径逐组件调用 Win32 `GetLongPathNameW` 展开已有 alias 后做 root containment 比较；普通路径保留原快速比较。原 candidate/component link 检查、词面 `..` 拒绝和最后 resolved-root 校验均保留；不使用 `Path.resolve` 代替 link 防护。POSIX containment 不变。checker 与 workflow-state/archive 两层都有 Windows 短路径回归，含越界 alias 拒绝。保留双平台 matrix、正式 checker、诊断器和 240/30/30 秒时限；详见当前 Task 的 Actions 缺陷记录。最终报告显示全部 262 tests 与 required checks 通过。
