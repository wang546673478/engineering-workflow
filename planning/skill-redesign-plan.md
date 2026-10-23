# Engineering Workflow Skill 改造方案（审阅稿）

状态：用户已审核完整方案，并于 2026-10-23 明确允许开始实施。本轮据此启动本仓库本地改造；授权记录在独立的 [Spec](skill-redesign-spec.md)、[Plan](skill-redesign-implementation-plan.md)、[Task](skill-redesign-task.md) 与 manifest 活动指针中。本文保留为已审设计，不扩展到 Issue #24 范围、外部项目迁移或远程发布。附件原文和现状差异见 [评估记录](skill-redesign-assessment.md)。

用户确认的根本意图（2026-10-23，Asia/Shanghai）：「我的本意写这个engineering workflow skill是为了让ai在每一步都能查询,然后进行纠偏纠错,所以需要全局基线也就是代码功能地图,数据库结构,前后端契约等文档,而且这些东西是动态的,也就是改代码途中,发现哪里不对然后对全局基线进行更改,这些门槛也只是为了不让ai自动跑偏,spec/plan/task也是这样」。随后用户补充：不是每个微小操作都需要重复查询；Agent 可复用当前上下文或仍新鲜的缓存。Spec/Plan/Task 指导本轮作业，生成代码时会使用相关 Baseline 事实；发现不一致时，再对受影响部分比较、校准和纠偏。本方案据此将“随时可查询”解释为低成本按需读取和新证据触发校准，而非每一步重复读取；门槛仍是防止 Agent 跑偏的方向反馈，不是留痕仪式。

## 1. 目标和成功标准

把工作流从“证明文档齐全”调整为“用当前代码和证据发现偏差，并在偏差影响动作前纠正”。保留 Baseline、Spec、Plan、Task 四种不同用途，减少维护这些工件时的重复操作，不把程序检查结果当作业务正确性证明。

### 根本目的与运行原则

本 skill 的根本目的，是让 AI 在工作中每一步都能基于当前上下文或按需读取当前系统和任务状态，并及时纠偏、纠错。Global Baseline 是系统当前事实的可查询模型，至少覆盖代码功能/模块地图、数据库结构、前后端契约及其来源和边界；它随代码、测试和运行证据变化而持续更新，不是首次接管时写完后冻结的文档。Spec、Plan、Task 也都是当前可查询、可被新证据纠正的工作模型：Spec 表达用户要什么以及哪些决定已确认，Plan 表达当前如何实现，Task 表达正在做什么、结果、阻塞与下一步。三者语义不同，但必须通过稳定引用保持为同一条纠偏链。

工作遵循同一纠偏闭环：**加载本轮需要的上下文 → 按 Spec/Plan/Task 作业，并使用相关 Baseline 事实 → 新证据出现时与当前事实/目标比较 → 必要时更正受影响的 Baseline、Spec、Plan 或 Task → 继续作业**。Agent 不必在每个微小操作前重复查询；同一轮中已读取且来源指纹仍有效、上下文未被新证据推翻的切片可以复用。只有开始/恢复任务、范围改变、需要的事实尚未载入，或源码/测试/运行结果等新证据表明所用结论可能过时或矛盾时，才重新读取对应切片。这样保留上下文和缓存的效率，同时让差异在影响后续实现前被发现。写入只更正受影响的权威切片，不为同步而复制全文或增加登记步骤。

**上下文复用建议**：这里的“缓存”主要指当前会话中已读取且仍有效的内容，以及工具自身缓存；不新建需要维护的持久缓存系统。当前任务、同一工作树/source revision 下，已查询且来源未变、没有反例的切片可复用。分支/提交/工作树切换、相关源文件变化、测试/运行出现反例、用户改变范围/决定，或恢复时无法确认上下文绑定的 revision，才使受影响切片失效并重新读取/计算。失效按视图传播，无关切片继续可用。没有可信 hash 时不声称已验证新鲜，按风险标记未核实；不能仅因跨会话就清空全部上下文。

门槛是这个循环里的方向反馈：在 AI 即将依赖错误事实、越过已确认目标或执行危险动作时，给出具体 delta 和下一步修正，让 AI 在当下纠偏。门槛不以“材料是否齐全”作为目的，不应只在任务末尾把整批工作判成 pass/fail。终点验证仍可确认已声明检查和交付边界，但不能替代过程中的查询与纠偏。

### 稳定 ID 查询与示例项目验证

- 一次稳定 ID 查询是按一个 table、route 或 module ID 读取该对象的事实切片，并同时返回与其关联的判断和证据。例如按 route ID 查询，可一次得到 method/path/request/response/handler 事实，以及关联该 route 的权限判断与核验依据。
- 本方案中提到的示例项目，是被外部采用此 skill 的项目所维护的 Baseline/Spec/Plan/Task 和派生文档，不代表用户要在采用时新增强制迁移步骤或额外文档台账。该仓库需提供可运行的示例测试：改变样例 schema 后，一次 table ID 查询即反映新字段，并返回关联文档视图；无需人工重写 inventory/mapping。权限语义仍是关联到 route ID 的判断层结论，由证据核验，不让代码生成器擅自推断。

沿用附件验收目标，并补充可验证口径。本批先实现数据库元数据和静态依赖的按需查询；路由、前后端契约和权限查询是否纳入本批以最终方案批准及实际 adapter 验证为准。在 route adapter 未通过 fixture/项目证据前，附件第 6 项只能记录为未交付/未验证，不得以接口预留或人工判断关联冒称已满足。

1. **表结构维护**：对可从项目源码/schema 直接计算的表结构，查询返回当前字段，逐字段人工同步为零；需要补业务含义时，只在判断层写一次。
2. **效率收益**：以同类 feature 配对试点测量工具调用、重复读写、失败重试和实际用时；成功工具调用数中位数目标下降至少 50%。日志或配对样本不足时标为未验证，不以单元测试、叙述估算或单例结果代替。
3. **可执行差异**：任何阻断结果指出对象、代码/来源现状、基线值、证据、建议动作和阻断范围。不能比对时标为 unsupported/unknown，不能伪装成 pass。
4. **可达门槛**：每个 required gate 都有受支持且可达到的通过路径。manual inventory 的可通过条件是其来源、边界可定位且 mapping 与列出的条目一致；报告需明确它不证明范围内绝无遗漏。
5. **依赖**：资料整理等顺序偏好不挡子任务开工；只有缺少被本次实现实际读取的技术产物时，才阻止相关实现。
6. **中途查证**：对可计算视图里的模块、表、字段、接口/路由，可通过稳定 ID 一次 query 返回精确切片、来源证据和计算版本；权限等需要判断的内容通过同一 ID 关联并随一次 query 返回。
7. **基线新鲜度**：上下文或缓存中的切片在来源未变化且没有新证据冲突时可以复用；相关源码、schema、契约输入变化或运行/测试证据推翻当前结论时，使受影响缓存失效，比较并刷新或核实更正后再继续依赖该结论的工作。提交/交付检查只是最后一次兜底。

### 附件需求覆盖索引

| 附件要求 | 本方案位置 | 自检结论 |
| --- | --- | --- |
| 4.1 Baseline 派生事实 / 判断 / 状态三层；派生事实不手写 | §3.1、§3.2 | 唯一事实/需求/状态权威；派生按需只读计算，不维护手写生成副本。 |
| 4.2 自动修复 / 语义 delta / 少数硬阻塞 | §3.2、§3.4、B2 | 有范围的新证据触发受影响部分比较纠偏；只有指定危险项硬阻塞。 |
| 4.3 锚点查询 | §3.3、§3.4 | 稳定 ID 与 route/table/field 切片读取已定义，未支持的 adapter 不宣称通过。 |
| 4.4 保留 Spec/Plan/Task，减少同步和 revision 负担 | §3.5、§6、B4 | 单一 change set operation 类型和投影规则已定义；只更正受影响权威视图，批准边界变化才升语义 revision。 |
| 4.5 任务规模和 applies_to | §4、B3 | 任务规模矩阵明确每种门槛；安全 finding 跨规模适用。 |
| 4.6 depends_on / after | §5、§6、B3 | 具体技术产物可阻塞使用它的工作；治理顺序只提示。 |
| 4.7 checker 独立治理 | §5 Checker 治理、§11 | 区分被检查项目的发布版与本仓库自检，不把宿主只读能力说成事实。 |
| 4.8 change-scope、报告保留、成本自查 | §5 变更范围、§6 报告输出和成本自查 | staged 与 worktree 分开；current 报告按任务/模式覆盖，只清理本次运行创建的临时文件；不自动删除历史用户文档。 |
| 验收 1：表结构人工同步 ≤1 | §1 指标 1、§3.1、B1 | 查询视图直接来自源码时结构字段人工同步为 0；确需补业务判断时在判断层写一次。 |
| 验收 2：feature 调用下降 ≥50% | §1 指标 2、§7 B5 | 只以同类配对 feature 和完整宿主日志验证，不能靠估算。 |
| 验收 3：任何门槛失败给可执行 delta | §3.4、§8 Delta 测试 | 所有阻止当前 Task 的结果均有对象、当前/预期或缺失值、证据和解除动作。 |
| 验收 4：required 无必然失败 | §3.4、§5 手工 inventory、§8 required fixtures | manual 清单通过路径复用 checker 现有 pass 状态，limitation 明示核对范围；不要求手工来源证明无遗漏。 |
| 验收 5：治理依赖不挡开工 | §5 依赖、§8 依赖测试 | after 永不阻止开工；真实技术产物只阻止依赖它的 Task。 |
| 验收 6：一次读取查对象和权限 | §3.3 稳定 ID、§3.1 本批覆盖、§8 锚点测试 | route adapter 已覆盖时一次返回 route 事实和链接判断；无 adapter 时明确未交付。 |
| 验收 7：代码变化同批更新派生层 | §3.1、§4 query 新鲜度、§6 工具、B1 | 默认不落盘；代码变化后同批下一次按需 query 从当前代码重算；不支持的输入明确标 unsupported。 |

## 2. 范围、保留项与非目标

### 本批目标范围

- 重写 SKILL.md 中 Baseline、Spec/Plan/Task 更新、任务规模和阶段规则；细节放入现有 references，不建立平行工作流。
- 为 checker 增加结构化 delta finding；修正手工 inventory 不可达状态；拆分技术依赖和顺序提示；区分开发中和提交时的变更范围，并按 Task 作用域检查实施授权。
- 优先扩展现有 workflow_state.py 的精确切片读取、单一 change set 分发和差异展示；派生事实默认只读按需计算；不另建通用状态数据库。
- 更新 manifest 示例、采用/迁移说明、README、checker reference、基线/实施文档、版本记录和测试。
- 明确 checker 独立版本与控制面保护的可验证边界。

### 必须保留

- Baseline（事实）、Spec（目标）、Plan（实现策略）、Task（执行状态）继续分开表达并互相引用。
- 不从目标设计推断当前事实，不从代码检查通过推断业务正确，不从用户确认需求推断实施授权。
- 真实密钥入库、权限越界、适用的 required 测试未运行/失败，以及项目既有明确的危险操作保护，仍阻止受影响动作；新政策不再把“文档不完整”本身扩展成安全硬阻塞。
- 真实技术前置条件仍可阻止依赖它的实现；“资料整理已完成”本身不是技术前置条件。
- 用户已明确批准同一完整范围时，不重复索要批准。模块核对与模块审核合并；确有需要的接管基线审阅和重大方案批准仍保留。
- 沿用现有新项目例外：先记录空实现起点和外部约束；不能要求空项目先提供不存在的代码事实地图。首次实现前仍须核实本次实现实际依赖的约束/现有脚手架，首批实现后将事实基线转为 partial，交付前补齐项目声明范围内的 complete 基线；目标设计不得写成当前事实，也不因此增加审核轮次。
- `task.scale`、`workflow.policy_version`、gate applies-to 和 `after` 均须在相关错误出现时纠正具体偏差：避免小任务套用全局门槛、让新旧 checker 误读字段，或把资料顺序误判为技术前置；不以增加字段为目的。

### 不在本批实现

- 为所有语言/框架承诺通用路由、权限或业务语义提取。
- 迁移或重写外部项目历史工件；外部项目是否采用新政策另行选择。
- 自动证明业务正确、代替用户判断需求或从文档推断人工批准。
- 将派生事实默认落盘为人工维护的第二套文档；默认从当前代码按需计算只读视图。
- 把成本自查变成 required gate，或以模型自报调用数作为精确度量。
- 删除用户维护的 planning 历史文档、用户报告或未标记文件；检查重跑只覆盖同任务/模式 current 报告，不增加自动历史清理步骤。

## 3. 目标模型

### 3.1 Baseline 三层

| 层 | 保存什么 | 维护者 | 更新触发 | 纠偏用途 |
| --- | --- | --- | --- | --- |
| 派生事实 | 可从明确技术来源提取的表/字段/索引、声明式路由/类型、静态模块关系及来源元数据 | 受支持 adapter 按需计算只读视图，默认不落盘 | 查询相关切片或其来源指纹失效时 | 代码与结构事实比较、定位 |
| 判断 | 模块目的、不变量、业务含义、权限解释、已知坑和“为何不改”；已确认需求正文仍以 Spec 为唯一权威，Baseline 只可引用对应 ID | Agent 依据证据起草；用户确认业务决定 | 语义 delta 或新决定出现 | 解释代码不能恢复的含义 |
| 状态 | Baseline 只提供当前状态的索引/摘要；任务/阶段/阻塞/下一步的唯一正文权威是 Task | Agent 维护 Task 顶部摘要；Baseline/目录按需链接或投影，不复制另一份可编辑状态 | 任务状态或下一步变化 | 恢复上下文、避免重复工作 |

**所有权**：派生视图不得手改或作为事实源；每次返回附 adapter/tool 版本、输入指纹、覆盖/排除范围和未知项。判断层引用事实 ID，不复制生成事实。Task 不复制 Spec 正文，只指出受影响 requirement/Plan 项与当前状态。

**能力边界**：adapter 声明准确观察与不能观察的范围。checker 只比较有证据的字段；无法可靠提取时标 unsupported，再按风险和影响决定是否需要人工判断。unsupported 不等于空集合或完整。

**首批适配器建议**：复用现有 SQLite/SQL 元数据提取器按需查询表/字段视图；复用已有 JS/TS 与 Rust 静态引用采集按需返回静态依赖切片。路由、OpenAPI/声明式契约和请求响应类型通过独立 adapter 接口分批接入；每种支持格式以 fixture 测试证明范围。首批不声称从任意业务代码还原权限或业务流程，也不把静态引用等同于运行时调用。

本批覆盖必须诚实标注：已接入且可验证的表/字段与静态依赖视图可作为本批派生事实；路由、请求/响应类型、权限和运行时业务链，只有相关 adapter 已实现且经 fixture/项目证据覆盖时才标 supported。未实现 adapter 的视图显示 unsupported/unknown 与影响，不得以空输出通过验收。接口权限的单次读取，是按 route ID 一次返回派生接口切片和关联人工判断；若本批没有 route adapter，该能力明确为未交付，不得宣称整项验收已满足。

**生成形式建议**：派生事实默认按需从当前源码/配置/schema 计算成只读视图，稳定 JSON 作为工具返回格式，可即时渲染终端/Markdown 切片；不把生成 JSON 默认写回仓库。缓存以参与计算的源码指纹为键；hash 未变且无新证据冲突则复用，变化或冲突则只重算该切片。正常 query 不修改项目文件，不产生第二真相。持久生成物不属于默认实现；若以后证明其必要性，再单独定义写入执行器与同批保证。无法即时计算的视图返回 unsupported 与影响/恢复动作，不以陈旧值冒充事实。

### 3.2 实施中发现 Baseline 语义不符时的回写规则

在使用已载入的 Baseline 生成或修改代码时，以及编码、测试或运行过程收到新证据时，只要发现当前代码行为/结构与 Baseline 的语义记述不一致，Agent 必须立即把它当作当前任务的纠偏事件处理，不能只把差异留在日志、测试输出或最终待补清单中，也不能继续依赖可能过时的 Baseline 扩展相关实现。先核实差异，再更新 Baseline，之后才继续依赖该结论的工作。无需因为没有新证据而重复检查；但一旦出现冲突信号，就必须对受影响部分重新比较。这个规则同样适用于 Baseline 与 Spec、Plan、Task 当前内容之间的矛盾。Spec/Plan/Task 中有关现状的文字只能作为链接或有来源的局部摘要，事实权威仍在 Baseline；冲突时按证据修正摘要，不复制成第二事实源。

按证据区分三种情况：

| 发现 | Baseline / Spec 处理 | 对实施的影响 |
| --- | --- | --- |
| 代码现状与 Baseline 记述不符，源码、迁移、测试或运行证据可确定当前事实 | 将 Baseline 更正为经核实的当前实现；生成层刷新派生事实，判断层修正受影响语义；保留原结论、证据、源码版本和纠正原因 | 暂停依赖旧结论的实现，完成受影响视图和引用更新后恢复；不依赖该差异的工作继续 |
| Baseline 与代码一致，但当前代码行为违反已批准 Spec/验收 | Baseline 如实记录实际行为/缺陷；Spec 不得为了匹配现状而改写。把它作为相对已批准目标的 defect/requirement delta，按现有授权修复或标记受影响工作 | 已授权修复可继续；超出已批准目标、权限或数据边界时暂停该扩展并呈现具体影响，不能以更新 Baseline 冒充已满足 Spec |
| 源码、测试和运行证据互相矛盾，或目前无法判定语义 | 在受影响对象标记 conflict/unknown，列出相互冲突证据、需要的核验动作和阻塞范围；不选一个方便的解释写成当前事实 | 只暂停依赖该结论且可能因此做错的工作；继续独立工作。只有仓库/工具无法回答的产品决定才问用户 |

经证实的回写更新唯一权威切片，并在当前 Task 顶部状态保留纠偏后的结论和下一步；如现有 Task 历史不足以解释纠正，再补最小旧/新结论、来源证据和影响视图，不创建平行 delta 台账。Spec 是需求正文唯一权威，Plan 是技术路径唯一权威，Task 是当前执行状态唯一权威；Baseline 不复制这些正文/状态，只保留必要 ID/链接或查询投影。Baseline 判断层可据证据更正既有业务描述的事实错误；新增业务规则、权限选择或目标决定仍按既有规则交用户确认。派生事实由只读 query 从当前代码重算，不手改文件。纠正事实不自动改用户目标或重做无关审核；若推翻已批准方案的关键前提，只复核受影响部分并暂停依赖工作。历史批准继续绑定原版本，不静默转移。

这是贯穿工作的规则，不是只在提交/交付时运行的末尾门禁。Agent 复用仍新鲜的上下文；当新证据触发缓存失效或暴露冲突时，立即校准。提交前的 delta 检查只是确认最近一次代码变化之后，没有受影响 Baseline 视图仍未刷新；它不能替代实施中的按需比较和即时纠偏。

### 3.3 稳定 ID 与一次读取

- ID 优先由技术来源派生，例如 db:<schema>.<table>、field:<schema>.<table>.<column>、route:<method>:<normalized-path>、symbol:<language>:<qualified-name>。
- 查询返回精确切片、证据路径/位置、源指纹、adapter、生成标识、覆盖边界和状态；一次请求可以指定多个 ID，不必读完整 Baseline。
- 普通改名显示为新 ID 的增删 delta；仅在被确认判断或跨模块引用依赖的改名时维护 alias，不强制给每个对象手工建索引。
- ID 无法无歧义生成时显示冲突并用来源位置区分，不擅自合并。
- 查询一个接口/路由 ID 时，返回 adapter 生成的 method/path/request/response/handler 事实，以及以该 ID 为锚点的人工核验权限判断、证据和最近核验状态；权限判断缺失或过期时同一响应显示 unknown/delta。一次读取是一次查到两层信息，不表示权限可由 extractor 自动决定。

### 3.4 Delta 合同和门槛

每条 finding 至少包含：finding ID、类别、对象 ID、当前来源值、已有派生/判断值、双方证据、差异说明、建议动作、风险级别、影响范围、是否阻塞及原因。终端可摘要显示，机器报告保留完整内容。常规待补证据进入 Task 清单且不阻止无关进度；只有继续依赖已被反证或无法判定的事实会导致错误实现时，才局部暂停该依赖动作以便核验，这不是新增通用硬门槛。

| 类别 | 处理 | 阻塞规则 | 示例 |
| --- | --- | --- | --- |
| 可自动修复 | 从当前来源重算派生只读视图，显示代码/视图 delta | 重算成功即消除该结构差异；无须人工同步文件 | 表字段、声明式类型、静态依赖边变化 |
| 需要语义判断 | 提交最小差异和证据；Agent 先比较源码、判断层和已批准 Spec，再更正唯一权威切片或记录为何不改 | 只暂停正要依赖该结论的动作直到完成比较；非阻塞项仍可并行 | 权限含义、数据所有者、兼容性解释变化 |
| 待补证据 | 在现有 Task 记录 owner/恢复条件和所欠依据 | 默认不阻塞 | 不影响当前决定的外部运行证据 |
| 硬阻塞 | 给出证据和修复路径 | 阻止直接受影响的危险动作；测试失败/未运行阻止依赖该结果的提交或交付，允许在授权范围继续诊断和修复 | 附件明确的密钥入库、越权、适用的 required 测试未运行/失败；项目已存在的明确危险规则 |
| 不支持/未知 | 标出缺少的 adapter/来源和范围边界，不当作空结果或通过 | 默认 pending；仅当它使正在进行的实现无法对已批准目标作安全/正确判断，或触发上述硬阻塞条件时，阻塞该依赖动作 | 私有路由 DSL 无 adapter |

任何会阻止当前 Task 动作的 checker 结果，包括 fail、error 或 blocking unsupported/stale/conflict，都必须给 actionable finding：对象/路径、当前值、预期值或缺失输入、证据、影响动作和解除条件。纯待补证据为 warning/pending。测试未运行与测试失败分开。新增硬阻塞仅限附件列明的密钥入库、越权访问、适用必测未跑/失败；项目既有明确危险操作规则继续有效，不扩展成泛化风险清单。业务语义正确性由 Agent/用户按证据判断。

### 3.5 Spec / Plan / Task 低同步写入

- 保留三者不同责任：Spec 的业务边界、Plan 的技术路径、Task 的执行状态。
- 所有需要改变权威工件的语义变更都从同一个 change set 入口提交；四类 operation 明确为 baseline.fact_correction、spec.requirement_change、plan.technical_decision、task.progress。工具将一次操作分发到唯一权威及实际受影响的引用视图，并返回单一完整 diff。Spec 决定只写 Spec，技术选择只写 Plan，执行状态只写 Task，代码事实更正写 Baseline；其余视图只更新必要引用，不复制正文。操作只触及一个权威视图时也走同一入口，但不强迫改写无关文档。批量 apply 对所有目标做 hash/引用校验，冲突时全批拒绝；不判断业务语义、不提升批准状态。
- 只将不同受众确需的结论投影到对应工件，不复制聊天正文。若变更只影响 Task，单一入口只更新 Task 并引用现有 Spec/Plan，不强制无意义的多文件更新。
- Spec、Plan、Task 的当前视图在讨论、实施和验证中持续更新：新证据可触发现状摘要的 Baseline 引用修正、Plan 技术路径调整、Task 进度/待决项更新。现状事实归 Baseline，Spec 只记录用户目标/需求决定，Plan 只记录技术决定，Task 只记录执行状态。Spec 中已确认的目标/权限/验收边界不可被 Agent 为迁就代码而静默改写；只有用户改变目标或批准范围时才产生新的边界 revision。Plan 可随实现证据调整技术路径，只要不改变用户可见行为和批准范围；Task 状态随真实进展更新。一次 change set 更新每个被实际影响的视图，不在 Spec/Plan/Task 之间复制同一段正文。日常事实/状态变化更新时间或进度，不升语义 revision。
- Baseline 新鲜度由源码提交/输入指纹和生成记录表达。历史审阅仍绑定原源码版本和范围，不随当前 Baseline 自动转移。Task.scale、policy_version、applies_to 与 after/depends_on 均须由具体任务错误触发条件说明其纠偏用途；不能仅为增加记录字段。

Spec/Plan/Task 与 Baseline 一样是动态工作模型，不是静态审批表单：Agent 将本轮相关部分载入上下文并在有效期间复用；当证据或实现进展改变了相应视图时才更新它。结构化批准和历史仅固定“当时批准了什么范围”，不冻结后续的事实、技术方案和执行状态。

这表示“一次输入、精确分发”，不宣称工具能自动证明三份文档语义一致。

**批准节点合并原则**：一次完整方案审阅同时展示 Spec 业务边界、Plan 技术路径、Task 执行/验证映射及其影响，不再把同一方案拆成重复的 Spec 批准、Plan 批准和 Q-01/Q-02 等多个用户节点。模块需求收敛时将完整性核对与模块审核合并。只保留解决不同风险的节点：首次接管且基线不可信时审阅当前系统范围、主要结论和限制；重大变更批准完整方案；实施授权仅在将实际改动产品或受保护代码的 Task 开始时检查；安全/控制面门槛阻止真实危险修改。有效且范围仍一致的批准可复用，不因普通进度、基线事实纠正或 revision 文案变化重复请批；若批准边界的关键前提被新证据推翻，只重审受影响部分。checker 的 applies_to 和 scale 只决定门槛是否适用于当前 Task，不创造新的用户审批点。

## 4. 任务规模与门禁

新项目模板声明 workflow.policy_version=delta-v1 和 task.scale；每个命令可声明 applies_to，Task 可用 gate_policy 覆盖该任务的具体应用范围。Task 实际声明 required 的检查和安全/控制面门槛不被规模跳过。delta-v1 支持 after 与指向真实项目内文件 artifact_path 的 depends_on。未声明新 policy 的旧 manifest 继续用旧 dependencies 和 required checks 语义，不要求迁移。无 scale 时按旧行为并在任务记录中标 inferred；跨边界影响使 Agent 升级 scale。

规模描述实现范围，不代表风险级别；安全、权限和数据保护 finding 独立应用于所有规模。

| 门槛/动作 | hotfix | minor | feature | takeover |
| --- | --- | --- | --- | --- |
| 影响分析与测试 | 聚焦缺陷链 | 聚焦模块 | 覆盖受影响链 | 覆盖调查范围 |
| 安全、权限、项目既有危险规则 | 始终评估；只按具体 finding 阻断 | 同左 | 同左 | 同左 |
| 派生事实查询 | 按当前输入查询受支持切片 | 同左 | 查询并核实适用全局 Baseline | 建立/复核项目声明范围视图 |
| 语义 delta | 仅本缺陷相关时 | 核对本模块受影响判断 | 核对受影响规则/模块 | 审阅全局判断和边界 |
| Spec / Plan / Task | 复用已批准范围；更新 Task | 更新 Task，边界变化才改 Spec/Plan | 关联需求/方案/执行项；目标变化需新 Spec 边界 | 只记录调查，不臆造产品 Spec |
| 全局 Baseline | 不要求重建全局基线 | 不要求重建全局基线 | 必须复用可信完整全局 Baseline；缺失时先建立项目声明范围基线再开展依赖事实的实现 | 已有实现必须建立/复核项目声明范围全局基线；空项目记录起点与约束 |
| Baseline 更新范围 | 发现受影响切片事实错误时必须纠正；不要求全局重建 | 同左 | 更新受影响视图；缺失可信全局基线时先完成声明范围调查 | 覆盖声明的全局适用范围；空项目按阶段从起点转 partial/complete |
| skill_review | 技术类别变化才重查 | 按范围变化重查 | 必需，限定相关候选 | 必需，限定调查/技术范围 |
| 适用验证命令 | 适用的 required checks | 同左 | 同左 | 调查范围内可运行检查；缺环境标 unsupported |

feature/takeover 接管已有实现时，若没有可复用且可信的完整 Baseline，必须先建立项目声明适用范围的全局基线，覆盖功能地图、数据库结构、前后端契约及模块关系，再开始依赖这些事实的功能实现；不能因某个 feature 只影响一个模块而跳过缺失的全局基线。空项目不要求先造不存在的代码事实地图，按新项目生命周期记录空实现起点和外部约束；首次实现仍须核实实际依赖事实，随后更新 partial 基线，交付前形成 complete。完整只表示声明范围内各适用视图都有来源、状态、边界和影响说明；允许明确的 unsupported/unknown，不代表所有视图均受支持或已获运行时验证。不得留空或把 unknown 当空/完整。Agent 应先调查填充代码可回答的未知；仍无法判断时只阻止依赖该事实的动作，独立工作继续。已有可信完整基线时只更新受影响视图，不重做无关接管。

表中的派生事实不靠代码之后人工同步文件来维持。代码或其声明来源变化会使相关缓存切片失效；同一批次中，在再次依赖该切片前，query 必须核验输入指纹并按当前输入重算，不能复用已失效的旧值，也不需要另设人工 refresh 步骤。来源无法可靠指纹化时，必须重新核对或标记新鲜度未验证后再决定是否可依赖。持久生成物不属于本批默认方案；未来若经证据证明必要，再单独定义生成和兼容机制。

“必须执行”指当前 Task 实际适用的动作，不新增全局检查命令。项目既有 required 测试在相关实现提交/交付前必须运行且通过；失败时可在授权范围继续诊断修复。对当前 Task 未触发的文档覆盖、语义记录、inventory 或检查命令，不因它们在全局 manifest 中存在就拦截无关工作，而应给出说明差异和适用范围的 finding。对 Task 明确 required 且确实适用的检查，测试未运行或失败时仍阻止依赖该结果的提交/交付。真实安全、权限、数据保护和控制面约束继续保留；scale 不是风险级别，安全与数据 finding 不受规模裁剪。

**防误分级**：Agent 根据接口、数据、权限和模块影响初判。实际范围超出时自动升级并说明证据；无法判断时按较高合理规模处理。规模升级不重开已解决的产品问题。低规模不豁免安全 finding、required checks、控制面历史保护或已有用户决定。已有有效 Baseline 时，feature 只刷新受影响视图，不重复 takeover。

标准 gate 可由命令声明 applies_to；Task gate_policy 只在该 Task 中收窄或补充明确适用范围。适用范围外的非强制命令可报告 skipped，不影响完成；Task required_checks 中指定的命令始终运行/阻塞。规模不改变安全、用户决定或控制面保护。旧 checker 无法识别新 policy 时按旧行为，不静默跳过 required gate。

**调查/实施授权按 Task 作用域判定**：全局 implementation/verification 阶段不自动推出每个 Task 都需要 implementation_authorization。纯调查、Baseline 纠错和测试诊断不按代码实施处理。hotfix/minor 按缺陷/模块范围执行影响分析与测试，不强制新建完整 feature Spec/Plan；feature 在涉及新增目标、跨模块、公开契约、权限或持久数据时，完整 Spec/Plan 审阅后实施；takeover Task 只授权基线调查，进入产品实现时建立/升级为 feature Task 并核验授权。由此消除全局 stage 对所有 Task 的误阻塞，同时保留实际实现护栏。

## 5. 依赖、变更范围和 checker 治理

### 依赖

- depends_on 只表示真实技术输入，需指出具体产物/能力和来源 Task。阻塞条件是产物不存在、不可读或不满足约束，而非来源 Task 状态不是 complete。只阻塞使用该产物的实现，独立工作继续。
- after 表示文档整理、上游摘要等顺序偏好，只作进度提示，不阻止开始、变更检查、提交或交付。若事实证明它是技术硬依赖，将具体产物转成 depends_on 并写明原因。
- 未知引用、环和未满足依赖均作为 finding，指出引用方、目标产物、条件与解除动作。

### 变更范围

- 区分开发中的 worktree-impact 与提交 change-scope。前者看 staged、tracked 修改和 untracked 新源码；后者只判定 staged diff。
- 未跟踪项不得静默丢弃。明确可识别的编辑器 swap、.tmp、.bak 和报告输出项不进入阻塞式 scope，但在 excluded 报告可见；无法明确归类的 untracked 源文件按真实改动处理。自定义临时模式不得宽泛排除源码目录。
- 提交检查报告未暂存源码造成的工作树/提交差异；不把它误算成已暂存内容。

### 手工 inventory 的可达状态

- manual 来源在 mapping 与声明范围一致、来源和范围可定位时，沿用 checker 已有 pass 状态，并在 limitation 中说明“只核对列出的项目/字段，不证明声明范围内绝无遗漏”。不新增结果状态枚举，也不要求人工自证完整。
- 缺边界、路径或 mapping/source 不一致时报告具体 delta；若某项 required，则阻止依赖该清单的决定，直到修复差异或补充边界。
- required 表示本任务必须处理已声明来源/范围；手工来源 mapping 一致且边界可定位时有可达 pass 路径，并声明限制。

### Checker 治理

- 对被检查项目：checker 独立版本发布；任务调用带版本的 checker，不在项目中改一份临时 checker 让结果变绿。manifest 记录实际/最低能力版本，扩展能力通过版本发布。
- 对本仓库自身：checker 是本项目产品，可按经审阅的完整方案修改；控制面差异用上一已发布 checker/既有保护规则核验，并运行 checker 自身回归。
- 无法提供可信外部/已发布 checker 时标 unsupported，并继续独立可做的本地验证；不声称宿主强制只读挂载。
- 门槛变化在本方案审阅材料中一次展示旧/新行为及放宽/收紧范围，不再另设重复审批点。

## 6. Manifest 和工具接口建议

新增配置只服务于已定义行为。复用现有 inventories 和任务关系，不新增平行 derived_views 清单；新增 workflow.policy_version，task.scale/after/gate_policy/implementation_task，以及 delta-v1 下带 task_id+项目内 artifact_path 的 task.depends_on。after 引用任务且只表达顺序提示。旧 manifest 按兼容规则读取，不要求先迁移，也不额外维护重复依赖字段。adapter 的命令与支持范围由 checker 发布版定义，不让项目重复登记可由工具恢复的元数据。

示意：inventory 绑定 sqlite-metadata adapter，从声明来源按需返回主 schema 表/字段切片，不需配置手工同步的生成文件路径。Task 可声明 scale=minor、depends_on 中实际消费的 schema/table artifact 条件，以及 after 中的治理顺序任务。此处是目标形状，不是最终 JSON schema。

沿用当前工具边界，优先增量扩展而非另加 CLI：

- workflow_state index：列出文档和稳定对象 ID；
- workflow_state snapshot/query：按 ID 读取只读切片及来源指纹；缓存命中且无冲突时直接返回，过期时自动重算受影响切片，不要求 Agent 另记 refresh 步骤；
- workflow_state apply-batch：dry-run/apply 已确认的单一 change set，按明确 operation type 分发到实际受影响的权威/引用视图，并给出完整 before/after；
- 不增加常态 refresh 步骤：snapshot/query 按需从当前输入计算只读视图；不支持的来源返回 unsupported，不要求 Agent 手工生成文件。
- check_project change/commit：只读输出结构化 findings、阻塞范围和动作。

不新增常驻服务、第二权威索引缓存或报告配置字段。checker 将当前报告写入既有排除的 work/ 稳定路径（按 task/session 与 mode 区分），同一 task/session/mode 槽位重跑时原位覆盖 current，不在 planning 产生 rerun/rerun2 文件。当次运行创建的临时文件由创建者在正常结束/错误退出时清理；既有历史报告不自动删除。

### 报告保留和成本自查

- 同一 task/session/mode 使用固定 current 报告路径；重跑覆盖原位文件，不产生 rerun/rerun2 副本；只清理由本次运行创建的临时文件。
- 无标记的旧报告、planning 文档、未知文件和 task_archive 快照均不自动删除；不新增历史清理设置。
- 成本自查仅在宿主提供可信调用日志时汇总产出文件/变更项、工具调用、重复读取、失败和重试；不估算墙钟或让 Agent 自填精确计数。日志不完整时只显示 unavailable/unverified，不影响完成门槛。

## 7. 分批实施计划

### B0：冻结方案和兼容合同

按用户审阅意见确定本批实施范围和验收边界；定义 finding JSON、沿用 checker 现有 pass 状态并以 limitation 说明核对范围、旧清单兼容和 adapter 输入/输出。批准只固定用户目标/权限/验收范围，不冻结 Baseline 事实、Plan 技术细节或 Task 进度；这些内容继续按证据动态纠正。固定旧 manifest 行为测试；确保没有 required 项只能永久 partial。本仓库内置 checker 对旧 manifest 默认使用 delta-v1 兼容推导，不要求先迁移；只有无法安全推导或会触碰旧批准边界时才报告具体 finding。外部 checker 能力按独立版本声明，不自动修改外部项目。

### B1：派生事实与锚点查询（核心 4.1）

实现派生事实只读视图、稳定 ID、coverage/limitations 和精确 ID 读取。接入有现成 extractor 的数据库元数据及静态依赖；其余标 unsupported。派生视图与手写判断分开；每次 query 按输入指纹判断新鲜度，发现源变化就重算所选视图，不能等到验证前才刷新。

退出条件：相同 fixture 重复 query 稳定；源码输入变化后下一次按需 query 自动发现指纹变化并重算；无新证据时可复用缓存；只读 query 无副作用；单个 table/field 可一次读到带证据切片；编码中制造“代码现状与 Baseline 不符”的 fixture 后，先核实并更正判断层及受影响引用，再允许依赖该对象的步骤继续。

### B2：Delta findings 与门槛纠偏（核心 4.2）

将路径 coverage 和 inventory 差异包装为统一 finding；区分自动修复、语义判断、待补证据、硬阻塞和 unsupported。自动可修先重算再重查；无关工作继续。手工 inventory 沿用现有 pass 状态，并以 limitation 明示声明范围及其不证明范围内绝无遗漏，保持真实测试和安全门槛。

退出条件：每个阻止当前 Task 的结果都可定位 delta 和解除动作；每个 required inventory fixture 有可达通过路径；回归证明新增硬阻塞限于附件明确类别且项目既有危险规则仍有效；另有行为测试覆盖“Baseline 与代码不符”“代码违反 Spec”“证据互相冲突”三种路径，验证不会把缺陷改写成需求，也不会在依赖旧事实时继续实现。

### B3：规模、依赖、Task 授权和变更范围

新增 task.scale 和 gate 适用矩阵；内置 checker 对旧 manifest 使用兼容推导，不要求先迁移。按 Task 是否实际实施代码判断实施授权，不从全局 stage 继承给纯调查任务。拆分 depends_on 与 after。提交 scope 看 staged；worktree-impact 看新源码；临时文件按窄规则排除且报告可见。

退出条件：治理型 after 父任务未完成不阻止子任务开工；真实技术 artifact 缺失只阻止依赖它的实现；纯调查 Task 在全局 implementation 阶段不被误要求实施授权；实际产品代码修改仍被正确授权门槛保护；untracked 新源码进入影响报告；.tmp 不造成提交 scope 假失败。

兼容验收：旧 manifest fixture 不迁移即可得到 delta 结果；旧项目原有明确审批、required checks 和安全政策不被静默删除；无法安全推导时给具体 finding；checker 不足以解释其能力时报告 unsupported，不改外部项目。

### B4：低同步批量写入、文档和迁移

以 workflow_state.apply-batch 承载一次 change set；按语义需要更新工件，不强制复制三份正文。语义 revision 仅绑定批准边界；更新 Skill references、模板、README 和版本记录；用旧 manifest fixture 验证内置 checker 兼容解释，不要求旧项目先迁移，也不自动修改外部项目。

退出条件：一个多视图变更由一个 change set operation 产生唯一完整 diff；需求正文/技术决定/执行状态进入唯一权威视图，其他视图只更新引用；hash 冲突整批拒绝；batch 不会把 approval 改为 approved；旧 manifest 不迁移也得到明确兼容结果。

### B5：正式验证、配对试点和发布

运行仓库要求的测试、compile、guidance compile，以及相关 checker 模式；控制面差异用可信上一版/保护流程核验。运行 skill validator、manifest fixture、适配器测试和用户场景 smoke test。匿名化同类 feature 做新旧流程配对：同一 feature 变更、同一输入 revision 和同等测试/交付标准；以宿主日志中的成功工具调用总数为主要指标，并分列读搜、写入、验证、失败和重试。比较新旧调用数中位数，目标下降至少 50%；实际用时和最终 diff/审批状态作为辅助指标。日志不完整或没有配对样本时标 unverified，不让 Agent 手工估算来通过验收。

退出条件：自动化合同通过；程序检查与业务语义复核分开记录；效率有实测或标 unverified；版本和 changelog 与最终发布范围一致。

## 8. 主要测试场景

- 数据库生成：表/字段新增、改名、删除；源缺失；输入顺序变化；源指纹变化；精确 ID 查询返回对应切片。
- 全局基线门槛：feature/takeover fixture 缺少适用模块图、schema 或契约视图时，在任何依赖其事实的实现前要求补齐或明确 unsupported 边界；独立测试/调查可继续。已有可信完整 Baseline 的单模块 feature 只更新受影响切片。
- 不完整提取：私有 DSL、动态路由或权限无法解析时显示 unsupported 与范围，不能将空结果当完整。
- Delta：过期视图刷新；手工判断冲突展示双方证据；低风险进入待补清单；高风险只阻止相关范围；每个 fail 有动作。
- 实施中 Baseline 纠偏：代码事实改变时先核实并回写派生/判断视图；代码违反 Spec 时保持 Baseline 与 Spec 的区别并报告缺陷；证据冲突时标 conflict、限定阻塞范围；三种情况都检查独立工作可继续，原批准不静默转移。
- 手工清单：来源/边界可定位且 mapping 与列出的条目一致时沿用 pass，并附 limitation；缺映射/证据产生具体 finding；required 有可达路径。
- 单一 change set：一个操作包含需求决定、技术决定和任务进度时，分别更新对应权威视图并保留引用；只改相关视图，不复制正文；hash 冲突时全批拒绝；审批状态不被自动提升。
- 同批自动可见：源码变化后同批下一次 query 按当前代码重算只读视图；查询无仓库写入；未支持的来源返回 unsupported，不把 Agent 手工同步计作自动化。
- 支持声明：每个 adapter fixture 输出其 supported fields、excluded fields 与 limitation；关键所需视图为空、来源未知或 adapter 未识别时必须标 unsupported/unknown，不能将它当成完整。
- 规模：hotfix 不触发全局 takeover；feature 更新受影响工件；takeover 不误用未审基线；安全/数据保护适用于所有规模。
- 依赖：after 只提示；资料型 after 不阻止开工；缺少实际 schema 只阻止使用者；未知引用和环有定位。
- Task 授权：全局 implementation 阶段中的只读调查不触发实施授权阻塞；写产品代码的 Task 未获授权时仍阻止实施。
- 门槛作用域：manifest 中当前 Task 未触发的 inventory/doc impact 不阻止无关任务；明确适用的 required 测试未跑/失败仍阻止相关交付；所有阻塞 finding 有可执行 delta。
- 变更范围：staged 变更精确含 rename/delete；untracked 源码进入 worktree-impact；临时文件不阻塞提交；非临时 untracked 不静默忽略。
- 批量/修订：hash 冲突整批拒绝、operation 幂等、审批字段不变；日常进度不升语义 revision。
- 兼容：旧 manifest fixture 无迁移即可使用内置 checker 的 delta 兼容规则；原有明确审批和安全语义保留；无法推导时 actionable finding；外部 checker 能力不符时报 actionable unsupported。
- 报告重跑覆盖 work/ 下固定 current 路径；只清理本次运行创建的临时文件，不清理用户/规划/archive 历史；成本日志缺失时报告 unverified 而不失败。

## 9. 风险和缓解

| 风险 | 缓解 |
| --- | --- |
| extractor 漏报被当成不存在 | adapter 明示支持/排除范围；unknown 不转空集；高风险依赖未知时阻断相关动作 |
| 生成物成为第二真相 | 默认按需从代码生成只读视图，不把生成副本写回仓库；业务解释留在判断层 |
| scale 被填小以绕门槛 | scale 不是风险级别；触及权限/数据/API 自动升级或增加 finding；未知时按较高合理级别 |
| 非阻塞被误读为一切可忽略 | 分列 blocking/pending/unsupported；安全项跨规模适用；pending 有负责人和恢复条件 |
| staged-only 漏新文件 | worktree-impact 检查 untracked 新源码；提交 gate 只判断 staged 并报告工作树差异 |
| 旧审批被套到新内容 | 审批绑定原范围；旧 manifest 兼容解析不得改批准；边界变化才生成新批准/语义 revision |
| checker 自己给自己放宽 | 外部项目使用独立发布版；本 checker 仓库用上一发布版或现有控制信号核查 |
| 成本自查变新仪式 | 作为 optional diagnostic；无可信日志标 unverified，不阻塞 |

## 10. 影响文件和验证门槛

预计涉及：SKILL.md、references/checker.md、references/baseline-linked-artifacts.md、references/implementation-workflow.md、references/project-documentation.md、scripts/check_project.py、scripts/workflow_state.py、相关 tests、assets/templates/project-manifest.example.json、README.md、manifest、traceability、change-impact、Baseline、VERSION、CHANGELOG。实际 adapter/生成器只覆盖 B0 明确列入且能验证的输入类型。

方案获批前，当前 required commands 和 timeout 不动。实施若改变 manual inventory 或变更范围判断，完整 Plan 展示旧/新行为；不得删除 required checks、降低测试覆盖或复用旧 Issue24 批准。验证按仓库规则执行，环境缺失如实标 unsupported/unverified。

## 11. 工作范围收敛

本节只收敛本方案依赖的实现边界，不复制第二份路线图；批次顺序以第 7 节 B0–B5 为唯一维护位置。SPEC/PLAN/Task 将引用这些批次与第 8 节测试。

- 受支持的表/字段/静态依赖以只读 query 从当前源码/配置计算；无 adapter 的路由、权限或运行时行为标 unsupported，不把空结果当完整。本批未实现的 adapter 不计入已交付能力。
- feature/takeover 若无可信完整 Baseline，必须先建立项目声明适用范围的全局事实地图（功能模块、数据库结构、前后端契约及其边界），再做依赖这些事实的实现；不依赖缺失切片的调查和准备可继续并行。
- 一次 change set 操作类型为 baseline.fact_correction、spec.requirement_change、plan.technical_decision、task.progress；机械分发到唯一权威和必要引用，不能复制正文或自动批准。
- 手工 inventory 的可通过路径沿用 checker 现有 pass 状态：来源/边界已定位且 mapping 与列出的条目一致，并附 limitation 说明不证明范围内绝无遗漏；不增加状态枚举。
- 任务门槛按 scale、实际动作和适用范围；只读 Task 不因全局 implementation 阶段触发实施授权。技术依赖仅阻止消费缺失 artifact 的工作；治理 after 不阻止开工。
- 新增硬阻塞限于附件明确项目（密钥入库、越权、适用必测未跑/失败）；项目既有明确危险规则保留。阻止当前 Task 的所有门槛结果都给出 actionable delta。
- 检查报告同一 task/session/mode 槽位重跑覆盖 current；只清理本次运行创建的临时文件，不自动删除历史报告、用户文档或 archive。没有可信配对日志时成本目标标 unverified。

用户已审核改造方向；后续 Spec/Plan/Task 只固化实现接口、影响、验收与验证，不重新审核已确认目标。方案审阅与实施授权分开；不沿用 Issue24 实施批准。

## Windows source-path follow-up

The hosted reviewed Windows failure on commit `7612033` led to a path audit in the bounded `--relations` query. An extended-length Windows source spelling may be accepted by `safe_path` but fail a later plain `Path.relative_to` against the normal root. The follow-up uses the checker's canonical root-relative helper first and a safe retry against the original declared relative path only. It does not broaden scanning or relax source boundaries. Local tests cover the correction; the Windows runner result remains pending. This correction preserves the approved `feature` task scale and its declared documentation impact gates.

CI follow-up: run `40019503239` passes Windows but its Ubuntu diagnostic assertion fails because Windows-only methods registered with `skipUnless` make the Unix TEST summary partial. The test methods are now conditionally defined only on Windows, matching existing platform-specific tests. The updated local Unix TEST run completes 286 cases with no skip summary; a fresh dual-platform hosted run is pending. This test-registration correction does not change task scale, required checks, or the approved documentation impact map.
