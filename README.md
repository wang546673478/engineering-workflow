# Engineering Workflow

Version: `1.11.0` · License: [MIT](LICENSE) · Changes: [CHANGELOG.md](CHANGELOG.md)

一个面向软件工程与持续需求讨论的 Codex skill。它帮助 Agent 从功能变化的讨论开始，维护需求、模块关系、接口契约、业务流程、数据库字典和验证证据。

## 适用场景

- 接管缺少文档的陌生项目
- 功能模块新增、修改、删除，以及行为、权限、计费或数据关系变化的持续讨论
- 跨前端、后端、数据库或后台任务的功能变更
- 影响范围不明确的缺陷定位
- 需要迁移、接口兼容、回滚和恢复记录的改动
- 需要在 Git 提交时确认代码与关联文档同步的项目

## 安装

将仓库克隆到 Codex 的 skills 目录：

```powershell
git clone https://github.com/wang546673478/engineering-workflow.git `
  "$HOME/.codex/skills/engineering-workflow"
```

Windows PowerShell 也可以使用完整路径：

```powershell
git clone https://github.com/wang546673478/engineering-workflow.git `
  "C:\Users\<user>\.codex\skills\engineering-workflow"
```

安装后，使用 `$engineering-workflow` 或让 Codex 根据任务自动选择该 skill。项目已采用流程时，当前任务中的后续短答和需求变更继续沿用该流程，无需每轮再次点名。实际技能选择和项目规则加载由宿主决定；文本指令不保证模型或宿主自动执行。

## 项目接入与持久化

项目决定采用本流程时，可以先维护根部 `AGENTS.md` 的持久入口；需要同时建立工程清单骨架时使用下方接入命令。保留已有规则，仅维护标记管理区：

```powershell
python <skill-dir>/scripts/install_agents_guidance.py --root <project>
```

`AGENTS.md` 保存共享规则；项目现有清单和状态文件保存联动的 Global Baseline、Spec、Plan、Task、决定、进度、影响分析、验证及交接。新清单通过活动指针和任务 `artifact_links` 连接这些工件。安装器始终更新 `AGENTS.md`；显式追加 `--file CLAUDE.md` 或 `--file .github/copilot-instructions.md` 时，只写指向它的相对链接。其他 agent 按实际规则文件格式和加载范围接入；Cursor 等宿主可能需要专有文件扩展名或前言，普通 Markdown 引用不代表自动加载。不要把规则目录作为 `--file` 传入。

安装器只处理规则入口；清单尚缺时明确报告接入未完成。adoption helper 可一并生成真实 JSON manifest 和入口，Markdown 任务索引不能作为 JSON manifest。接入时记录 skill/checker 来源、版本和当前任务路径；开始、恢复、接手、上下文压缩或不完整、切换 agent、范围变化时，重新读取 skill 正文、适用引用与状态文件，并核对工作树；范围变化还要重新做 `skill_review` 和影响分析。小修复复用现有记录，避免重复建档。

完整接入示例：

```powershell
python <skill-dir>/scripts/adopt_project.py --root <project> `
  --skill-source <skill-dir>/SKILL.md --skill-version 1.7.2 --profile lite
```

命令创建 `initialized_incomplete` 的接入骨架，并返回实际 bootstrap 诊断；不会执行项目检查命令、完成基线或批准实现。已有 manifest 默认保留，显式 `--upgrade-legacy-manifest` 才补生命周期字段；原文档、检查和历史保持。用重复的 `--document ID=path` 映射已有工件，完成映射后运行 `check_project.py --mode discovery --run-checks`。基线审阅、Spec/Plan 批准和实施授权按原规则分别记录，可复用仍有效的原话，不增加审核轮次；空项目、小修等例外与字段、迁移和退出码见[完整接入与阶段门禁](references/adoption-lifecycle.md)。

首次接入可以先生成可审阅的清单骨架：

```powershell
python <skill-dir>/scripts/init_manifest.py --root <project> --profile lite
```

`lite` 省略源清单并使用影响记录，`full` 额外登记可选数据库/契约清单和跨层文档门槛。两种配置都要求联动的 Baseline、Spec、Plan、Task、追踪和基线视图文档存在；不适用视图记录原因。生成结果仍处于 `planned`/`takeover_discovery`，必须补齐实际路径、权威验证命令、skill review、基线和批准记录；默认不会覆盖已有清单。初始化器用于底层骨架，完整采用优先使用上面的 adoption helper。

从零开始的新项目显式使用 `--project-kind greenfield`，例如：

```text
python scripts/init_manifest.py --root <project> --project-kind greenfield --profile full
```

先记录空实现起点和约束，核验后将基线从 planned 转为 not_applicable；写出首批实现后转 partial，交付前转 complete/approved。模块、接口和数据库的目标设计先写入 Plan，只有实现事实和证据进入当前 Baseline。临时状态允许继续开发，不能用于任务完成或 handoff；已有代码但缺少文档仍需调查。实现范围默认 src/tests，可通过重复的 `--implementation-path` 指定。初始化器只写清单，不创建实现、文档或审批。

示例与full初始化的源清单默认可选；数据库字典、接口文档和语义覆盖仍须完成。接入时先核对来源与检查器能力，只有存在受支持验证路径的来源才设为必需。手工来源始终partial，检查器没有通用路由源码适配器；已启用项目不能自行降低原有门槛，须准备具体调整方案并按项目规则审阅。

## 工作流内容

Skill 会引导 Agent：

1. 读取项目规则和现有 Global Baseline、Spec、Plan、Task 及其链接。
2. 检查当前任务可用的其他 skills，并记录采用或不采用的理由。
3. 在功能讨论中持续更新权威需求和当前状态，保留候选、确认与延后事项。
4. 在模块讨论结束时集中核对需求及关联影响，再交用户审核；完整实施方案仍按既有门槛确认。
5. 分析页面、接口、业务逻辑、数据库、事件和消费者之间的影响链，在实现后刷新受影响 Baseline，并同步 Spec/Plan/Task 的引用和状态。
6. 运行项目检查，并记录通过、失败、跳过、未支持和未验证状态。

已批准项目可按需启用结构化批准证据合同，核对批准记录和已审方案/本批范围绑定；新项目初始化为diagnostic，旧项目不自动迁移，strict需明确选择。它只强化审批相关检查，不替代原需求访谈、项目门禁、验证命令或文档同步。旧版本行为增强说明见 [Issue 23 Task](planning/issue-23-task.md)。

本地工程文档可按项目选择使用 [task_archive.py](scripts/task_archive.py) 建立版本快照、检查漂移、查看历史和恢复。它不加入原检查门禁或审核流程；SQLite archive 文件不加密，宿主未提供文件权限隔离时，只能检测并恢复，不能阻止 shell/editor 直接写入。备份位置/清理由采用项目负责。详见[归档合同与命令](references/checker.md#本地工程记录归档与恢复)。

三项指引在这些原节点中使用：[缺陷证据](references/implementation-workflow.md#defect-evidence-within-the-existing-task)连接原复现、根因、修复前后结果与回归；[交付前收敛](references/baseline-linked-artifacts.md#交付前收敛)具体核对本批缺失、部分、矛盾、无归属实现和过期证据；[可选需求/验收示例](references/requirements-interview.md#optional-requirement-and-acceptance-examples)提供 EARS 中文等价句式及 Given–When–Then。沿用原记录与格式，不增加阶段、审批轮次或验证命令，也不要求旧项目迁移历史文档。

## 自主调查与动态基线

基线不是功能需求的附录，而是 Spec/Plan/Task 的输入和实现后的回写目标。推荐链路为 `Baseline → Spec → Plan → Task → Code/Evidence → Baseline`：批准的 Spec 在本批次内冻结，技术变化更新 Plan，执行变化更新 Task，源码或测试发现的事实错误先校正 Baseline。新增业务目标才创建新的 Spec revision。升级工作流后，应核对当前权威文档、清理过时的当前状态、补齐引用并保留历史与原审批范围；更新 skill 不会自动迁移外部项目。详细规则见[基线与工件联动模型](references/baseline-linked-artifacts.md)。

基线调查获得授权后，Agent持续调查、验证并保存记录，进度汇报后继续，不要求用户反复说“继续”。需要运行依赖、数据库或缓存时，在已有授权内自主准备局部隔离环境并测试；有真实权限、凭据、工具或业务决定阻塞时，说明证据并先完成独立工作。

Agent负责源码和字段语义核验，用户审核具体版本、调查范围、主要结论及限制。基线区分当前事实、运行验证、已知缺陷和外部未知；首次审阅不等于生产认证，也不自动授权修复所有历史问题。影响结论或后续工作的关键未知仍需解决。

后续测试、调查或模块修改发现基线错误时，即使源码未改，也立即标记并查证，证实后主动修正所有受影响的权威文档，保留旧结论、依据和原审阅范围。事实更正自主完成；若推翻已批准需求或方案依据，只暂停与重审依赖该结论的部分。细则见[基线文档](references/project-documentation.md)；本批范围与验证见[TASK-BASELINE-01](planning/baseline-workflow-task.md)。

### 实测：一次读取多个基线事实

在一个真实工程资料的只读试测中，`workflow_state.py query` 用一条 CLI 命令按对象 ID 返回 6 个基线切片，覆盖数据库结构和固定路由来源；单次查询耗时 **0.8965 秒**，同一查询重复运行 10 次的中位耗时为 **0.9205 秒**。查询读取了项目清单、带哈希的源码回执和仅含结构的 SQLite 快照；没有读取业务数据行、执行线上 handler 或验证部署环境的权限。去标识后的测量数据和完整统计限制见[试点记录](planning/real-session-efficiency-pilot.md)。

这表明在项目已接入、对象受支持时，Agent 可以一次取得一组带来源的当前事实。它**不能证明整场工程会话节省了多少时间或工具调用**：历史会话的命令统计覆盖需求讨论、实现和门禁，按文本匹配的类别会重叠，也不等于实际文件读取；本试测没有用同一功能配对重跑新旧流程，且没有可信的逐项耗时。因此不报告整体节省分钟数或百分比。

## 持续需求记录与模块审核

涉及功能变化的新信息在讨论过程中写入项目已有权威需求和 Task，不等到开始编码或模块结束。纯事实答复没有新增变化信息时复用已有记录。需求状态与实施状态分开维护；记录不等于确认，确认也不自动授权实施。阶段或范围变化时刷新当前摘要、下一步和依赖，历史原话另行保留，避免旧状态继续冒充现状。

延后讨论也保留所属功能、已有结论、待决问题、影响/依赖和恢复条件；进入依赖它的设计或实施前回看。模块讨论收敛时，集中核对需求摘要、本次变化、待定/延后事项及关联影响，再由用户审核该模块。讨论中持续保存，每轮不另设集中门禁或重复要求审核；后续只重审变化影响的部分。首次接管的基线审阅和新项目、重大变更的完整方案批准仍然适用。

Agent 应简短告知本轮更新位置和剩余待定项；保存失败时如实说明。检查器只核验已声明的机械证据，没有会话消息输入，无法发现完全未落盘的需求或替代用户判断。当前规则修改与验证状态见 [TASK-CONTINUITY-01](planning/continuous-requirements-task.md)。

## 版本与 CHANGELOG

每批有实质变化的交付按项目已有规则更新版本及 CHANGELOG；同一批内部编辑可合并升版。默认三段版本号按修复、兼容新增和不兼容变化选择 PATCH、MINOR、MAJOR。任务记录升版依据、权威来源、同步位置及验证/发布状态；仅进度或验证回执可说明无需再升版。未发布条目标为 Unreleased，实际发布才填写日期；版本更新不等于批准提交、推送或部署。细则见 [实施流程](references/implementation-workflow.md)。

## 和用户确认

需要用户决定的事情会先用通俗语言说明：发现了什么、为什么要决定、有哪些选项，以及每个选项的影响。技术名词、文件路径和检查结果会作为补充说明，不会直接替代解释。用户看不懂时，Agent 应换一种更简单的说法；用户确认后，Agent 会复述确认范围，并记录在任务或决定记录中。

## Git 提交门禁

检查器位于 `scripts/check_project.py`。

提交前检查当前暂存区：

```text
python scripts/check_project.py \
  --root <project> \
  --manifest engineering-manifest.json \
  --mode commit \
  --task TASK-01 \
  --run-checks
```

CI 检查已经生成的 commit：

```text
python scripts/check_project.py \
  --root <project> \
  --manifest engineering-manifest.json \
  --mode committed \
  --commit-ref <commit-sha> \
  --task TASK-01 \
  --run-checks
```

`commit` 模式确认代码变更和受影响的模块、业务流程、接口或数据库文档进入同一个提交。`committed` 模式用于 CI 或受保护分支复核实际提交树。可直接使用以下模板：

- `assets/templates/pre-commit.engineering`
- `assets/templates/pre-commit.engineering.ps1`
- `assets/templates/ci-committed.engineering`
- `assets/templates/ci-committed.engineering.ps1`

具体文档门禁由项目清单中的 `task.documentation_impact` 声明。检查器不会自动发现所有动态依赖，Agent仍须复核模块关联和字段语义，用户审核需决定的范围与结论。

清单路径支持 `/` 和 `\\` 两种分隔符。`exclude_paths` 可使用项目相对的段级 glob：`*`、`?`、字符类只匹配单个目录段，`**` 匹配零个或多个目录段；例如 `**/node_modules` 会在解析链接前剪枝任意层依赖目录。根匹配、绝对 glob 和 `..` 段会被拒绝，排除项不会扩大变更覆盖范围。

full/lite 初始化器默认显式生成 `**/node_modules`，无论初始化时是否已安装依赖，各层依赖目录均按该规则排除。已有清单保持原样；若需要相同政策，请审阅后将根级 `node_modules` 改为该glob。特殊项目若在此目录维护自有源码，应相应调整清单；检查器继续只按显式排除工作。

声明的检查命令参数不能包含空字节。检查输出固定限制为 8 MiB；超过上限会终止命令并将检查标记为失败，报告只保留字节数和摘要哈希。`VERSION` 与 `CHANGELOG.md` 在本仓库属于控制面文件，修改时需要外部审阅。

`documentation_impact.when_paths` 仍是字面路径。除了模块或文档自身范围，还可以使用包含至少两个不同所选模块 source scope 的严格公共父目录，例如 `packages/api` 与 `packages/web` 共用 `packages`。公共父目录只触发配置的文档更新门槛，不会让该目录下的其他路径自动通过覆盖检查。

## 数据库元数据适配器

入口：`scripts/extract_database.py`

支持：

- SQLite：受控文件快照
- MySQL：只读 `INFORMATION_SCHEMA`
- PostgreSQL：只读 `information_schema`
- Redis：只读 `INFO keyspace`

适配器只生成元数据快照，不读取业务行、Redis key/value 或连接凭据。MySQL、PostgreSQL 和 Redis 驱动是可选依赖；缺少驱动、凭据或连接不可用时会报告 `unsupported`。普通基线检查不会自动连接远程数据库。

示例：

```text
python scripts/extract_sqlite.py <checkpointed.sqlite> --output database-inventory.json
python scripts/extract_database.py mysql --url-env ENGINEERING_DATABASE_URL --schema app --output database-inventory.json
python scripts/extract_database.py postgresql --url-env ENGINEERING_DATABASE_URL --schema public --output database-inventory.json
python scripts/extract_database.py redis --url-env ENGINEERING_DATABASE_URL --output database-inventory.json
```

## 可选目录与批量状态工具

文档/任务较多时，可运行 scripts/workflow_state.py 从现有工程清单和 Task 生成 JSON/Markdown 目录、按 document ID 与精确标题读取正文/章节和 SHA-256，或按稳定对象 ID 查询当前声明事实：

    python scripts/workflow_state.py --root <project> index --format markdown
    python scripts/workflow_state.py --root <project> snapshot --document-id TASK-01 --section "当前状态"
    python scripts/workflow_state.py --root <project> query --id db:main.accounts --id field:main.accounts.email --id module:billing --relations

目录保留已完成、明确 superseded/obsolete、deferred 项及其证据；planning 下未登记的 Markdown 显示为 unknown/unverified。缺少状态证据时不根据时间或非当前状态猜测。apply-batch 支持按 Task 和 authority 精确路由的文档章节 change set 及 JSON lifecycle 更新；默认只给完整 diff，必须同时提供 archive head、所有目标的 expected hash、已初始化 task archive 并显式加 --apply 才会写入。文档操作必须匹配 Task 链接和 authority 类型；工具拒绝改审批、工作阶段、task status、门禁或超时，不增加 required checks，也不代替语义审查。宿主命令因无效 cwd 无法启动时，本地脚本无法介入；无可验证 host file API 时保持 unsupported。完整接口、安全和恢复边界见 [Checker reference](references/checker.md#可选文档目录快照与精确批量更新)。

该工具读取记录时遵守工程清单的安全路径与严格 JSON 检查；批量 request 文件应放在 manifest 管理文件之外。它用同目录原子替换单个文件，但多文件更新不提供整体原子可见性；中断或回滚失败时检查 archive drift，并按已保存 head 恢复。

## 目录结构

```text
SKILL.md                         Agent 入口规则
agents/openai.yaml               Codex 界面元数据
assets/templates/                项目清单、文档和 hook 模板
assets/templates/AGENTS.engineering.md  跨 agent 持久化接入片段
references/                      分阶段工作流说明
scripts/check_project.py         项目清单与提交门禁检查器
scripts/workflow_state.py        可选目录、快照、稳定 ID 事实查询和显式 hash-guarded 更新工具
scripts/install_agents_guidance.py  幂等更新 AGENTS.md 管理区
scripts/init_manifest.py             生成 full/lite 清单骨架
scripts/adopt_project.py             安装 managed guidance 与生命周期清单
scripts/extract_database.py      MySQL、PostgreSQL、Redis 元数据适配器
scripts/extract_sqlite.py        SQLite 元数据提取器
scripts/tests/                   检查器、适配器和 workflow-state CLI 测试
```

## 验证

本仓库完整回归需要 Rust 和 JS/TS 两类解析环境。在任务隔离环境中准备依赖，再使用该环境的 Python：

```text
python -m venv <task-work>/reference-env
<task-work>/reference-env/Scripts/python.exe -m pip install -r scripts/reference-requirements.txt
npm ci --ignore-scripts --prefix scripts/context-runtime
<task-work>/reference-env/Scripts/python.exe -m unittest discover -s scripts/tests -q
```

POSIX 使用 `reference-env/bin/python`；JS/TS 依赖需先安装 Node.js。门禁执行声明中的 `python` 时，应先激活同一环境或将其可执行目录加入本次命令的 PATH。缺依赖会集中提示准备方法并保持回归失败，不能用 skip 代替完整验证。

这些依赖对日常工具使用是可选的：普通盘点/阅读包不需要解析器，只分析 Rust 或 JS/TS 时准备对应环境即可。引用分析缺能力时，终端 JSON 和 `relations-summary.txt` 会显示原因、安装指引和覆盖缺口，已成功解析的部分保留。安装仅针对本工具，不安装被分析项目的依赖。

```text
python -m unittest discover -s scripts/tests -q
python -m py_compile scripts/check_project.py scripts/extract_database.py scripts/extract_sqlite.py
```

本仓库也维护自己的工程清单。可在仓库根目录运行：

```text
python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks
```

本仓库自带的 GitHub Actions 示例会在 Linux 和 Windows 上运行测试、编译检查和自身基线检查。GitHub Actions 对使用该 skill 的项目是可选能力：项目可以只用本地 hook，或接入其他 CI 服务；选择 GitHub Actions 的项目再复制模板并启用 workflow。无论是否使用远程 CI，提交前都应运行本地 `commit` 门禁，并在采用的 CI 中复核已生成的提交。

检查规则本身被修改时，自动提交检查会暂停，等待人工审阅。检查器会同时参考修改前后的保护范围，不能靠在本次提交中删除保护名单或更换批准变量来直接放行。获批后才能通过专用参数和单次外部批准信号继续；规则检查失败、历史缺失或工作区与提交内容不一致时，不执行该提交声明的项目命令。

本仓库的 Actions 将普通 PR 检查、控制面 PR 审阅和最终 push 复核分开。控制面 PR 需要 CODEOWNERS/分支保护批准；批准当前同仓库 PR head 后，工作流自动进入 `engineering-control-review` 环境并运行精确 commit 的受保护检查。批准值只存在于环境范围，普通或 fork PR 不会拿到它。PR review、环境批准和检查报告共同留下审计记录；`workflow_dispatch` 仍可用于历史提交的 exact-SHA 补救验证。

本仓库的 Actions 将普通 PR 检查、控制面 PR 审阅和最终 push 复核分开。控制面 PR 需要 CODEOWNERS/分支保护批准；批准当前 PR head 后，工作流自动进入 `engineering-control-review` 环境并运行精确 commit 的受保护检查。批准值只存在于环境范围，普通或 fork PR 不会拿到它。PR review、环境批准和检查报告共同留下审计记录；`workflow_dispatch` 仍可用于历史提交的 exact-SHA 补救验证。

本仓库另提供人工运行的 Actions 入口，要求指定审阅过的完整提交 SHA，并配置受保护的 GitHub environment。具体接入条件见 [检查器说明](references/checker.md)。这些配置不会自动安装到其他项目，也不代表 GitHub 仓库设置已经启用保护。

## 安全边界

- 不把密码、Token 或完整连接串写入计划、清单或快照。
- 不为满足检查自动修改、清空或迁移真实数据库。
- 不把检查器通过当成完整的业务语义审查。
- 项目自身的规则、用户决定和安全约束优先于本 skill 的默认流程。

## 首次接管的阶段顺序

首次接管已有代码且缺少有效全局基线时：**全局现状梳理 → 用户审阅基线 → 深入功能访谈 → 完整方案确认 → 实现与验证**。梳理前可澄清必要的基本目标，但不能只看局部页面就连续追问功能范围。任务记录当前阶段、基线版本和转换证据；已有有效基线及确认可复用，小修复按最小必要步骤执行。无既有实现的新项目先记录空实现起点和约束，再进入访谈，后续按临时基线到事实基线的生命周期推进。具体条件见 [SKILL.md](SKILL.md)。

## 源码辅助工具

1.6.0增加可选源码清单、目录统计、完整紧凑阅读包、预算/遗漏和JS/TS/Rust引用证据，按需输出文字、关系表和Mermaid。调用/范围/安装及限制见[说明](references/source-context.md)。原工程阶段、审批和验证要求保持；引用不是运行时调用或业务事实。


### 提交验证与取消（1.6.4）

两种提交检查都会核对声明命令前后的HEAD、暂存区和工作树。检查命令留下源码或未忽略文件的变化会失败，工具保留修改供调查；有意生成的构建/测试产物应由项目审阅后配置Git忽略。成功报告的verified_tree可与实际提交树核对，不能替代独立CI或恶意代码隔离。

深层JSON、解释器整数限制和错误manifest根类型会输出结构化配置错误。Ctrl-C/SIGTERM执行中断会清理拥有的普通进程家族并返回非成功，原检查/时限不变。Windows使用系统Job Object支持，无法建立约束时拒绝启动命令；POSIX强制SIGKILL等保证边界见[检查器说明](references/checker.md)。
