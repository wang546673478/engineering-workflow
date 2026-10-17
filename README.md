# Engineering Workflow

Version: `1.5.0` · License: [MIT](LICENSE) · Changes: [CHANGELOG.md](CHANGELOG.md)

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

项目决定采用本流程时，先把持久化入口写入项目根部的 `AGENTS.md`。保留项目已有规则，只加入带 `engineering-workflow:start/end` 标记的管理区：

```powershell
python <skill-dir>/scripts/install_agents_guidance.py --root <project>
```

`AGENTS.md` 保存共享规则；项目现有清单和状态文件保存联动的 Global Baseline、Spec、Plan、Task、决定、进度、影响分析、验证及交接。新清单通过活动指针和任务 `artifact_links` 连接这些工件。安装器始终更新 `AGENTS.md`；显式追加 `--file CLAUDE.md` 或 `--file .github/copilot-instructions.md` 时，只写指向它的相对链接。其他 agent 按实际规则文件格式和加载范围接入；Cursor 等宿主可能需要专有文件扩展名或前言，普通 Markdown 引用不代表自动加载。不要把规则目录作为 `--file` 传入。

安装器只处理规则入口；接入 agent 还需在项目现有状态中记录 skill 来源/版本和当前任务路径，可用 `--skill` 指定可定位的来源描述、`--manifest` 与 `--state-dir` 指向实际位置。开始、恢复、接手、上下文压缩或不完整、切换 agent、范围变化时，重新读取 skill 正文、适用引用与状态文件，并核对工作树；范围变化还要重新做 `skill_review` 和影响分析。小修复复用现有记录，避免重复建档。

首次接入可以先生成可审阅的清单骨架：

```powershell
python <skill-dir>/scripts/init_manifest.py --root <project> --profile lite
```

`lite` 省略源清单并使用影响记录，`full` 额外登记可选数据库/契约清单和跨层文档门槛。两种配置都要求联动的 Baseline、Spec、Plan、Task、追踪和基线视图文档存在；不适用视图记录原因。生成结果仍处于 `planned`，必须补齐实际路径、权威验证命令、skill review、基线和批准记录；默认不会覆盖已有清单。

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

## 自主调查与动态基线

基线不是功能需求的附录，而是 Spec/Plan/Task 的输入和实现后的回写目标。推荐链路为 `Baseline → Spec → Plan → Task → Code/Evidence → Baseline`：批准的 Spec 在本批次内冻结，技术变化更新 Plan，执行变化更新 Task，源码或测试发现的事实错误先校正 Baseline。新增业务目标才创建新的 Spec revision。升级工作流后，应核对当前权威文档、清理过时的当前状态、补齐引用并保留历史与原审批范围；更新 skill 不会自动迁移外部项目。详细规则见[基线与工件联动模型](references/baseline-linked-artifacts.md)。

基线调查获得授权后，Agent持续调查、验证并保存记录，进度汇报后继续，不要求用户反复说“继续”。需要运行依赖、数据库或缓存时，在已有授权内自主准备局部隔离环境并测试；有真实权限、凭据、工具或业务决定阻塞时，说明证据并先完成独立工作。

Agent负责源码和字段语义核验，用户审核具体版本、调查范围、主要结论及限制。基线区分当前事实、运行验证、已知缺陷和外部未知；首次审阅不等于生产认证，也不自动授权修复所有历史问题。影响结论或后续工作的关键未知仍需解决。

后续测试、调查或模块修改发现基线错误时，即使源码未改，也立即标记并查证，证实后主动修正所有受影响的权威文档，保留旧结论、依据和原审阅范围。事实更正自主完成；若推翻已批准需求或方案依据，只暂停与重审依赖该结论的部分。细则见[基线文档](references/project-documentation.md)；本批范围与验证见[TASK-BASELINE-01](planning/baseline-workflow-task.md)。

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

## 目录结构

```text
SKILL.md                         Agent 入口规则
agents/openai.yaml               Codex 界面元数据
assets/templates/                项目清单、文档和 hook 模板
assets/templates/AGENTS.engineering.md  跨 agent 持久化接入片段
references/                      分阶段工作流说明
scripts/check_project.py         项目清单与提交门禁检查器
scripts/install_agents_guidance.py  幂等更新 AGENTS.md 管理区
scripts/init_manifest.py             生成 full/lite 清单骨架
scripts/extract_database.py      MySQL、PostgreSQL、Redis 元数据适配器
scripts/extract_sqlite.py        SQLite 元数据提取器
scripts/tests/                   检查器和适配器测试
```

## 验证

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
