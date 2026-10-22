# SPEC-ISSUE24-EFFICIENCY-01：工程状态目录与低开销读写

状态：Approved as `SPEC-ISSUE24-EFFICIENCY-01 r1`, implementation in progress; human decision and scope are recorded in the linked Task. The delivered helper remains optional and does not change the existing workflow.

依据：[Issue #24 现场评估](issue-24-efficiency-assessment.md)及用户 2026-10-22 的原话：“我们从全局来看这个问题,只要不改变流程,那么我们替换更好的工具能不能减少搜索\写入\替换的工作量?” 后续明确：“是的,过时或已完成的就应该在目录性文档中”。该确认仅涵盖目录应包含已完成/过时记录及其状态，不代表批准实现工具。

## 目标

在不改变既有 1.8 工作流、审批节点、门槛和记录内容的前提下，减少项目需求讨论中反复寻找/读取权威文件、逐文件同步和因命令/定位失败而重复尝试的机械工作。

## 已确认流程约束

- Baseline → Spec → Plan → Task → Evidence 链、一次一问、持续记录、候选/确认/延后状态、模块完整性审核、完整Plan批准、实施授权及原验证门槛保持不变。
- 工具生成目录、保存机械 revision、成功执行批量更新都不自动把需求改为approved、不冻结Spec、不批准Plan，也不授权实现。
- 已完成或已过时/被替代的工件仍必须出现在目录中，显示其生命周期状态和历史关系；不能因非当前而隐藏或删除。

实施批准记录：用户于 2026-10-22 先表示“批准方案”，后指示“一次性根据spec/plan/task把engineering workflow 全部改完吧,然后上传github”。该授权批准本 SPEC r1 和 PLAN r1 的本地实施及原门槛通过后的 GitHub 上传，不授权外部项目迁移、宿主 API/OS 权限变更或 Release。完整原话、thread 时间和执行范围见 [Task](issue-24-efficiency-task.md)。

## 候选需求

- **REQ-ISSUE24-E01（用户确认目标）**：减少需求讨论中的搜索、读取、写入、替换成本，不改变既有工作流节点与授权意义。
- **REQ-ISSUE24-E02（候选）权威导航目录**：依据已有 manifest、active pointers、Task artifact links/revisions 生成项目文档目录，至少显示 document ID、路径、kind/owner、lifecycle status、revision/basis、最后变更摘要和关联工件；同时发现并列出 `planning/` 下未在 manifest 注册的 Markdown，状态为 unknown/unverified。
- **REQ-ISSUE24-E03（用户确认）历史可见**：目录必须包含 current、draft、completed、superseded/obsolete、deferred、unverified 等适用状态的条目；完成/过时项目保留原路径、原因/替代项与证据链接，不删除记录。若来源没有足够状态证据，标为unknown/unverified，不猜测。
- **REQ-ISSUE24-E04（候选）目录非第二权威源**：目录为可重建的 read model。状态来自 manifest/Task/Spec/Plan 的明确字段；修改目录文本本身不能变更审批或生命周期状态。对已有历史记录进行初次分类须保留来源证据；来源不足时保持unverified。
- **REQ-ISSUE24-E05（候选）read snapshot**：一次返回 active Task、当前 Spec/Plan 摘要、待决项和明确请求章节，附文件摘要/revision；缓存须在源摘要变化时失效。
- **REQ-ISSUE24-E06（候选）apply batch**：一次处理一组精确的 manifest 对象/命名 Markdown 区段更新；带稳定 operation ID 和预期源摘要；同 ID 重放幂等；任何文件冲突/歧义锚点/JSON引用失败时整批不写并返回可读 diff。
- **REQ-ISSUE24-E07（候选）操作校验**：manifest、文档ID、REQ/AT、active revision/pointer、目录状态关系可做机械一致性检查；状态冲突显示conflict交Agent/用户处理，工具不得自动选定“最新”语义。
- **REQ-ISSUE24-E08（Host依赖）cwd/文件接口**：宿主命令cwd错误后不应对同一无效目录无限重试。优先使用稳定workspace handle/file API；宿主无可用恢复接口时明确报unsupported/blocker。Skill内helper不能声称修好宿主cwd。
- **REQ-ISSUE24-E09（验收目标）效率度量**：用配对pilot测量成功工具调用数、重复读取/写入、失败/重试和实际用时；Issue单次会话的估值不当成总体量化保证。
- **REQ-ISSUE24-E10（兼容）**：工具可选；未启用项目继续原文件工作流，旧项目不自动迁移、不强制Git、不自动strict化、不增加required checks。

## 候选验收标准

- 目录包含manifest声明文档及按明确规则发现的项目规划条目；完成和obsolete/superseded条目在索引中可检索，显示状态、原因/替代关系和历史证据；unknown条目显示unverified。
- 目录每行来源可追溯；重建目录后状态等价；源文件hash/revision改变时目录刷新并暴露冲突。
- 一次多文档batch更新只产生一份可审阅diff和一条机械批次revision；重复operation不重复写入；任一前置检查失败则所有目标原样不变。
- 工具不改变Spec/Plan/Task审批字段或status，除非另有现有流程已经确认/批准的更新操作；不会从用户的需求答案推断实施授权。
- 失效cwd时停止重试同一错误路径，尝试重解析workspace或host file API；宿主不支持时返回明确错误。
- 配对pilot报告旧法/新法调用量、重复路径、失败/重试、耗时、文件diff及审核流程一致性；不声称单次试点证明所有项目均提速。

批准边界：REQ-E01、REQ-E03已确认；REQ-E02、REQ-E04–E10作为实施细节在批准Plan `PLAN-ISSUE24-EFFICIENCY-01 r1` 范围内采纳。实现不得改变 1.8 workflow stages、approval meanings/reuse、diagnostic/strict defaults、required checks、测试命令/覆盖或自动迁移边界；不会触碰 Issue #23 外部会话中的用户项目。timeout 原约束由以下用户批准的执行政策修订覆盖。实现状态及用户原话见 [TASK-ISSUE24-EFFICIENCY-01](issue-24-efficiency-task.md)。当前代码、关联文档和验证状态以该 Task 的当前执行记录为准。

### 用户批准的执行政策修订（2026-10-22）

用户明确要求：“把 TEST 超时改为 240 秒，其余检查和流程保持不变，并据此更新方案后继续”。仅当前仓库正式 TEST timeout 从 120 秒调整到 240 秒；TEST 命令、全部测试/断言、required 状态、COMPILE 与 GUIDANCE-COMPILE 的 30 秒 timeout、工作流阶段和审批语义保持不变。此修订限于门槛时限，不改 REQ/AT 功能范围；证据与实施进度记录在 [Task](issue-24-efficiency-task.md)。
